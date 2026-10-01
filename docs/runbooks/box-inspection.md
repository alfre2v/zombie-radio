# Runbook: inspect a deployed GPU box

*Living, undated (runbooks convention). The quick-scout commands
for a box the playbook has converged: what runs, is it what we
expect, where the logs are. Everything here is read-only. SSH in
as `ubuntu` (or run one-offs via `ssh ubuntu@<ip> '<cmd>'`).*

## Containers (llama, whisper)

```bash
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'
```

Expect `llama` and `whisper`, both `Up`. Verify the supervision
config actually landed:

```bash
docker inspect -f '{{.Name}}: restart={{.HostConfig.RestartPolicy.Name}} net={{.HostConfig.NetworkMode}}' llama whisper
```

Expect `restart=unless-stopped net=host` on both.

## The tts systemd unit

```bash
systemctl status tts-faster_qwen3tts --no-pager
systemctl is-enabled tts-faster_qwen3tts docker
```

Expect `active (running)`, and `enabled` twice (both switches the
reboot auto-rise depends on). A crash-looping unit shows
`activating (auto-restart)` and a rising "restart counter" —
go straight to its journal.

## Logs, one command per service

```bash
docker logs -f llama          # or --tail 100 for a snapshot
docker logs -f whisper
sudo journalctl -u tts-faster_qwen3tts -f    # -n 100 for a snapshot
```

## GPU

```bash
nvidia-smi        # driver/CUDA versions, per-process VRAM
nvtop             # live cockpit (NOT preinstalled — owner installs when
                  # wanted; apt dry-run verified: zero driver deps)
```

Healthy full stack (one TTS engine), measured 2026-10-01 on the
A6000 with a 16k context: llama 6,764 MiB · tts 6,530 MiB (Faster
Qwen3-TTS, after a day of shows) · whisper 888 MiB — 14,195 MiB in
all. Whisper lazy-loads at the first STT request and grows after the
first microphone use; the voice engine grows as it caches the clips it
clones from.

### The LLM: how much is the model, how much is the context

llama-server holds two things on the GPU: **the model's weights** (fixed
by the model file) and **the context** — the memory for the
conversation it is reading (`-c`, the deployment's `zr_llama_ctx`),
plus its compute buffers and CUDA's own overhead. Its load log does not
print the buffer sizes at this verbosity, so measure by subtraction:
the process's GPU memory minus the model file's size. Run on the box
(or each as a one-off, `ssh ubuntu@<ip> '<cmd>'`):

```bash
# 1. The whole card: memory in use and its size
nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv

# 2. Per process: /app/llama-server is the LLM; the faster_qwen3tts python is the voice; python3 is Whisper
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv

# 3. The model file: its size is (about) the weights llama-server holds on the GPU
find /home/ubuntu/models -size +1G -type f -exec ls -l {} \;
```

And from the laptop, through the tunnel, the context llama.cpp is
actually running with:

```bash
# 4. The context size and the number of slots, as the server reports them
curl -s localhost:8080/props | python3 -c "import json,sys; d=json.load(sys.stdin); print('n_ctx', d['default_generation_settings']['n_ctx'], '| slots', d['total_slots'])"
```

For example, on 2026-10-01 (the A6000, a 16k context):

```
name, memory.used [MiB], memory.total [MiB]
NVIDIA RTX A6000, 14195 MiB, 49140 MiB
pid, process_name, used_gpu_memory [MiB]
1291, /app/llama-server, 6764 MiB
1298, python3, 888 MiB
884, /home/ubuntu/faster_qwen3tts/.venv/bin/python, 6530 MiB
-rw-r--r-- 1 root root 6525629280 Sep 22 22:43 /home/ubuntu/models/models--bartowski--nvidia_NVIDIA-Nemotron-Nano-9B-v2-GGUF/blobs/be84528231457f766a35612386e2638d9af10beb10a9d8d23f0cc73c20818da7
n_ctx 16384 | slots 1
```

Reading it: the model file is 6,525,629,280 bytes = 6,223 MiB (divide by
1,048,576); llama-server uses 6,764 MiB; so **the context, its buffers
and CUDA's overhead take about 541 MiB** at 16k. The weights on the GPU
are close to the file's size, not exactly it (llama.cpp may keep a
small part, such as the token embeddings, in the host's memory), so
treat the difference as an estimate. Nemotron Nano 9B v2 is a hybrid
model — few attention layers — which is why its context is so cheap.
To see what a bigger context costs: measure, change `zr_llama_ctx`,
`make ans-deploy ENV=cloud`, measure again, and compare llama-server's
line; the model file does not change.

## Health gates

On the box (what the playbook's own gates poll):

```bash
curl -s http://127.0.0.1:8080/health
curl -s http://127.0.0.1:8001/capabilities | head -c 200; echo
curl -s -o /dev/null -w "stt: %{http_code}\n" http://127.0.0.1:8002/docs
```

From the laptop, through the tunnel: `make check`.

## Disk and model caches

```bash
df -h /
du -sh ~/models ~/.cache/huggingface
```

`~/models` = llama's GGUF cache (HF-hub-style blobs, no .gguf
extension). `~/.cache/huggingface` = TTS checkpoint + whisper
model, shared tree.

## The converge invariant

A re-run of `make ans-deploy ENV=cloud` against a healthy,
unchanged box must report **changed=0**. Any `changed` on a
no-op converge is a bug in a role (it also needlessly restarts
services via handlers) — diagnose which task and fix the role;
do not shrug it off.
