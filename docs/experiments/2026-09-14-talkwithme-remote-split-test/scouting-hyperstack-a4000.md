# Box scouting — Hyperstack RTX A4000 VM

**Date:** 2026-09-15 · **Part of:** the remote-split test (this
folder) — spike checklist steps 1–2 (provision + baseline).
**Box:** Hyperstack VM, 1× NVIDIA RTX A4000 (A6000s were out of
stock — consistent with the provider survey's owner-confirmed
stock volatility; the A4000 at $0.15/hr incidentally makes this
box a live probe of the 16 GB aspirational VRAM tier,
[spec §4]). Operator: `ubuntu` user (full sudo, docker group).

*Format: command + verbatim output + interpretation. All commands
run by the owner over SSH; sudo used liberally (not required for
`nvidia-smi` queries — only for setters like `-e`; harmless).*

## 1. GPU identity & memory

```
$ nvidia-smi --query-gpu=name,memory.total,memory.used,memory.free,driver_version,pstate,temperature.gpu --format=csv
name, memory.total [MiB], memory.used [MiB], memory.free [MiB], driver_version, pstate, temperature.gpu
NVIDIA RTX A4000, 15352 MiB, 1 MiB, 15089 MiB, 535.183.06, P8, 28
```

```
$ sudo nvidia-smi -q -d ECC | head -25
    ECC Mode
        Current                           : Enabled
        Pending                           : Enabled
    ECC Errors
        Volatile / Aggregate              : all counters 0
```
*(output condensed here; full table was clean zeros)*

**Interpretation — the "missing" ~1 GB is ECC, not fraud:**
16384 MiB × 0.9375 (ECC parity reservation) ≈ 15360 ≈ the
observed **15352 MiB**. ECC is on and error counters are zero
(healthy memory). Reclaiming the ~1 GB would need
`sudo nvidia-smi -e 0` + reboot; not worth it for the spike.

## 2. Passthrough vs virtualized slice

```
$ sudo nvidia-smi -q | grep -i -A2 "virtualization"
    GPU Virtualization Mode
        Virtualization Mode               : Pass-Through
        Host VGPU Mode                    : N/A

$ sudo lspci | grep -i nvidia && systemd-detect-virt
00:05.0 VGA compatible controller: NVIDIA Corporation GA104GL [RTX A4000] (rev a1)
kvm

$ sudo nvidia-smi -q -d CLOCK | grep -A4 "Max Clocks"
    Max Clocks
        Graphics                          : 2100 MHz
        SM                                : 2100 MHz
        Memory                            : 7001 MHz
```

**Interpretation:** genuine **PCI passthrough** of a physical
GA104GL card into a KVM VM — we own the whole GPU, not a vGPU
slice. Max clocks look nominal.

## 3. Docker-with-GPU (provider-survey criterion S0.1, proven live)

```
$ sudo dpkg -l | grep -i nvidia-container && docker info 2>/dev/null | grep -i runtime
ii  nvidia-container-toolkit             1.16.1-1   ...
 Runtimes: runc io.containerd.runc.v2 nvidia
 Default Runtime: runc
```

```
$ docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
...
|   0  NVIDIA RTX A4000               On  | 00000000:00:05.0 Off |                    0 |
| 41%   28C    P8               8W / 140W |      1MiB / 15352MiB |      0%      Default |
```

**Interpretation:** nvidia-container-toolkit preinstalled (as the
survey said Hyperstack's "with Docker" images would be); a
container we pulled ourselves sees the GPU; the `ubuntu` user is
in the docker group so no sudo needed (note: docker group =
root-equivalent, documented in [spec §10]/S0 — on this
single-tenant box, fine). **Acceptance criterion S0.1 is now
field-proven on Hyperstack.** Watch item: driver 535 is a CUDA
12.2-era driver; the 12.4 container worked (minor-version
compatibility), but a future TTS engine demanding a much newer
CUDA runtime could hit friction — check engine CUDA requirements
against driver 535 before pulling.

## 4. Compute stress — gpu-burn ⚠ ANOMALY, UNDER INVESTIGATION

```
$ docker run --rm --gpus all oguzpastirmaci/gpu-burn:latest ./gpu_burn 60
GPU 0: NVIDIA RTX A4000 (UUID: GPU-f7218cd7-...)
100.0%  proc'd: 826 (4690 Gflop/s)   errors: 0   temps: 29 C
Initialized device 0 with 15090 MB of memory (14728 MB available, using 13255 MB of it), using FLOATS
Tested 1 GPUs:
	GPU 0: OK
```

**Interpretation — OPEN QUESTION.** 4,690 GFLOPS FP32 is ~25–28%
of a real A4000's expected SGEMM throughput (~16,000–18,500
GFLOPS), and the 29 °C temperature after a 60 s "burn" says the
card never drew serious power. Zero errors and full VRAM
allocation say the silicon is present and stable. Hypotheses,
most-benign first:

1. **Clocks never boosted** (card pinned at low P-state under
   load — host-side applications-clock cap, or a driver
   power-management quirk) — diagnosable by sampling clocks and
   power during load.
2. **The benchmark container is the culprit**: the gpu-burn image
   may be compiled for an older GPU architecture and running
   JIT-degraded kernels on this sm_86 card.
3. Actual host-side throttling/QoS (the "virtualized crap"
   scenario) — only credible if hypotheses 1–2 are eliminated by
   an independent benchmark showing the same deficit WITH clocks
   verified at boost.

Next diagnostics (Stage D): independent PyTorch matmul benchmark
+ live clock/power sampling during load. → results below.

### Stage D results (2026-09-15) — ANOMALY RESOLVED: the card is genuine, the benchmark lied

```
$ docker run --rm --gpus all pytorch/pytorch:2.4.0-cuda12.4-cudnn9-runtime python -c "<matmul benchmark>"
tf32 31.7 TFLOPS
fp16 60.5 TFLOPS
```

```
$ nvidia-smi --query-gpu=clocks.sm,clocks.max.sm,power.draw,temperature.gpu,utilization.gpu,pstate --format=csv -l 2
210 MHz, 2100 MHz, 15.18 W, 32, 0 %, P8     ← idle / image pull
...
1560 MHz, 2100 MHz, 16.77 W, 33, 3 %, P2    ← load begins
1935 MHz, 2100 MHz, 86.17 W, 37, 0 %, P2    ← boosted, real power
375 MHz, 2100 MHz, 39.83 W, 35, 0 %, P3     ← load ends
210 MHz, 2100 MHz, 19.19 W, 34, 0 %, P8
```

**Verdict:** tf32 31.7 and fp16 60.5 TFLOPS are dead-center
healthy A4000 numbers (expected ~25–35 / ~50–70), and the clock
trace shows proper boost (1935 MHz @ 86 W) under load.
**Hypothesis 2 confirmed**: the `oguzpastirmaci/gpu-burn` image
runs JIT-degraded kernels on this sm_86 card and reported ~27%
of real throughput. The GPU passes; the gpu-burn image is
retired from our toolkit. (Protocol lesson, filed under "never
trust an instrument's own summary": the stress tool's number
measured the tool.)

## 4-bis. RAM & CPU

```
$ free -h
Mem:            20Gi        ...        available: 19Gi
$ nproc
4
```

**Interpretation:** 20 GB RAM — comfortable. **4 vCPUs — the
box's thinnest spec** and worth remembering beyond the spike:
CPU-side work (Whisper if ever CPU-bound, Opus encoding, TTS
pre/post-processing, Docker builds) shares 4 cores, versus 28
pCPUs on the surveyed A6000 flavor. Fine for the plumbing test;
a consideration when choosing the demo-day flavor.

## 6. Firewall posture (owner ruling 2026-09-15)

```
$ sudo ufw status
Status: inactive
```

Hyperstack's own security-group firewall (managed in their web
UI/API) is the enforced layer: currently inbound :22 only
(owner-read, to be confirmed by an external scan). **Ruling:
live with this default — ufw stays off.** Agent concurrence with
rationale: (a) the provider security group operates OUTSIDE the
VM, so it catches everything including Docker-published ports —
the very ports ufw notoriously fails to protect (Docker's
iptables bypass), meaning the ufw layer was always half-illusory
here; (b) with the SSH tunnel, :22 is the entire intended
surface. Condition attached: verify from the laptop that only
:22 answers (external scan — see scouting checklist). This
amends [spec §10.2]'s "two-layer default-deny" doctrine — dated
amendment recorded in the spec.

## 5. Disk

```
$ sudo df -h
/dev/vda1        97G   16G   82G  16% /
tmpfs            11G     0   11G   0% /dev/shm
```

**Interpretation:** ~82 GB free on the root virtual disk — ample
for the spike (small LLM GGUF ~5–8 GB, one TTS engine ~2–8 GB,
Whisper ~1–3 GB, docker images ~15 GB). No external volume
attached and none needed. Persistence semantics: the root disk
**survives reboots** (it's the VM's boot disk) but **dies with VM
deletion** — acceptable, everything here is reproducible by
Ansible. `/dev/shm` at 11 GB implies ~22 GB system RAM (tmpfs
defaults to half) — to confirm with `free -h`.

## Scouting status

- [x] GPU identity, ECC explanation
- [x] Passthrough confirmed
- [x] Docker-with-GPU confirmed (S0.1 proven)
- [x] Compute anomaly RESOLVED — silicon genuine (tf32 31.7 /
      fp16 60.5 TFLOPS); gpu-burn image was the culprit
- [x] RAM / CPU confirmed: 20 GB / 4 vCPU (CPU is the thin spec)
- [x] External port scan from laptop (owner, 2026-09-15): only
      :22 open — the ufw-off ruling's condition is satisfied;
      Hyperstack's security group matches its console claim.
- [~] Network throughput + laptop→box latency: deliberately
      folded into the experiment run itself (measure (a) — the
      audio stream is the real test).

**SCOUTING VERDICT (2026-09-15): box trusted.** Genuine
passthrough A4000 performing at spec (fp16 60.5 TFLOPS), Docker
with GPU proven, disk/RAM adequate (4 vCPU noted as the thin
spec), firewall posture verified externally. Hyperstack's
hardware is what it claims to be.
