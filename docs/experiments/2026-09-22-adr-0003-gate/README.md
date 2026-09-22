# ADR-0003 gate — grammar-constrained streaming and the latency shape — runlog

**Created and run:** 2026-09-22 (evening, one box session).
**Timebox:** tonight, one box. Abort rule: if gate 1 is not settled
within one hour of its first request, stop and talk before spending
more box time. The box is destroyed at the end of the evening
whatever the state — a partial observation recorded honestly beats
a heroic overrun.
**Provenance:** TODO Task 6 (the gate line of the boundary-shift
note: "two on-box confirmations") · ADR-0003, section "Gate" items 1
and 2 (`docs/decisions/0003-adopt-shared-context-screenplay-engine-with-browser-clocked-director.md`)
· [discussion 2026-09-21] prompt-structure §7.1 (streaming with a
grammar, source read), §7.2 (the screenplay grammar), §11 (the
decision gate) · spec §4 (model stack).

## The question

Two claims ADR-0003 is built on, never measured on our stack:

1. Does our llama-server build stream grammar-constrained tokens in
   ordinary SSE chunks, and does the grammar actually bind (an
   illegal speaker cannot appear)?
2. Is one shared-script request per round (structure D) cheaper in
   prompt evaluation than TalkWithMe's four per-persona requests
   (structure A), because of the prompt cache — and what does the
   grammar cost per generated token?

The verdict criteria, the predictions, and the caveats are in
`findings.md`, frozen before any gate request runs.

## Execution model

- **The owner** owns the box's life (Hyperstack console: create,
  destroy) and the SSH tunnel: he starts `make ssh-tunnel ENV=cloud`
  once in his own terminal and leaves it. The agent never starts a
  tunnel (port collision) and reaches the model services only
  through the laptop's local ports (`localhost:8080` llama.cpp,
  `:8001` tts-serve, `:8002` whisper).
- **The agent** runs the deploy, the checks, and the gate scripts
  from the laptop, inspects the box read-only with plain
  `ssh ubuntu@<box> '<cmd>'` (the owner's default SSH resolution —
  no key paths, no project known_hosts; owner ruling 2026-09-22 for
  this one-evening box), and keeps this runlog true: every command
  actually run lands here in order, with its output.
- **Nothing on the box changes outside the playbook.** The converge
  invariant (`make ans-deploy` re-run reports `changed=0`) must
  survive the evening.
- **The box's address never appears in this folder.** It is written
  "the box" or `<PASTE-BOX-IP-HERE>`; the folder is grepped for it
  before every commit (the never-commit hook skips `*.md`).
- Times: the laptop runs CDT (UTC−5); the box runs UTC. Each entry
  says which.

## Environment

- **Provider / GPU:** Hyperstack, 1× NVIDIA RTX A6000, 49140 MiB
  visible (ECC off). Region: not recorded yet (owner).
- **Image:** "Ubuntu Server 22.04 LTS R550 CUDA 12.4 with Docker" —
  the same image as the 2026-09-19 proof run (the compatibility
  table's middle row, proven with real inference on cu128 wheels).
- **Measured on the box (recon, runlog entry 1):** Ubuntu 22.04.5
  LTS, kernel 6.8.0-40-generic; driver 550.90.12, CUDA 12.4; Docker
  27.2.1; NVIDIA Container Toolkit 1.16.1; 28 vCPUs, 56 GB RAM, no
  swap; 97 GB root disk, 84 GB free before the deploy; user `ubuntu`
  in groups `sudo` and `docker`.
- **Stack (from `deploy/ansible/inventories/common_vars.yml`):**
  llama.cpp image `ghcr.io/ggml-org/llama.cpp:server-cuda` (floating
  tag — the build actually served is recorded from `/props` in the
  runlog), model `bartowski/nvidia_NVIDIA-Nemotron-Nano-9B-v2-GGUF:Q4_K_M`,
  context 16384, all layers on the GPU (`-ngl 99`), one slot
  (`--parallel 1`); tts-serve tag `1.2` (bumped from 1.1 tonight,
  engine faster_qwen3tts); whisper-fastapi, model `small`. The gate
  needs only llama.cpp.
- **Laptop:** the owner's Mac; Python 3 standard library only for
  every script in this folder; `curl`.

## Files in this folder

- `findings.md` — verdict criteria, predictions, caveats; Results
  and Verdict after the runs.
- `screenplay.gbnf` — the screenplay grammar: 1–4 lines of
  `Name: text`, the four placeholder scientists as the speaker
  alternatives, no square brackets in the text.
- `cast.py` — the shared material: the four persona prompts (verbatim
  from the installer-seeded TalkWithMe 7.1 personas), the cast sheet
  for structure D, the fixed ten-round script, the grammar loader
  (narrows the speaker list), and the request builders for both
  structures. `python3 cast.py stream-request --speakers …` prints
  the gate-1 request. Also the wire-log helpers (below).
- `stream_check.sh` — gate 1: one streamed request through the
  tunnel with `curl -sN`; every SSE line saved with its arrival time
  in milliseconds since just before `curl` started to
  `raw/stream/<label>.sse.txt`, the request to
  `raw/stream/<label>.request.json`.
- `parse_stream.py` — derives the gate-1 facts from those files.
- `latency_probe.py` — gate 2: arms A, D-off, D-on, D-live (defined
  in `findings.md`), ten rounds, non-streamed; one JSON file per
  request under `raw/probe/` (request, response with `timings`,
  wall time).
- `summarize_timings.py` — derives every gate-2 number from
  `raw/probe/`.
- `check_outputs.py` — derives what the model wrote in the D arms
  (lines per round, `Name: text` shape, "Over." endings, D-off versus
  D-on text); added after the run (runlog entry 15).
- `raw/` — the record of truth, committed.
- `raw/wire.log` — the human-readable view of the same traffic
  (owner request 2026-09-22), written as it happens so it can be
  followed with `tail -f`: for every request, a header line (laptop
  time, request name, grammar allowlist or `none`, seed, token cap)
  and every message in full as `[role] content`; then the answer
  with the wall time and the server's counters (prompt tokens
  evaluated, reused from the cache, generated). Streamed answers
  are appended chunk by chunk as they arrive. The full history is
  written on every request on purpose — it is what crosses the
  wire, and A re-sending the whole script four times per round is
  gate 2a's mechanism made visible. Not an input to any number:
  the JSON files are the record the scripts read.

## Reproduction recipe — THE section to follow

*Living section: the current, corrected commands in order. Run from
the repository root unless a step says otherwise.*

### 0. Box up and wired

```bash
make ans-set ENV=cloud IP=<PASTE-BOX-IP-HERE>
make ans-deploy ENV=cloud          # from zero: ~15 min, ~11 GB of models
make ans-deploy ENV=cloud          # the re-run must report changed=0
```

The owner then starts the tunnel in his own terminal
(`make ssh-tunnel ENV=cloud`; it reads the address from the wired
`hosts.yml`, so it comes after `ans-set`). Then, on the laptop:

```bash
make check                         # three ok lines
```

### 1. Record what the server is

```bash
cd docs/experiments/2026-09-22-adr-0003-gate
mkdir -p raw
curl -s http://localhost:8080/props > raw/props.json
curl -s http://localhost:8080/v1/models > raw/models.json
ssh ubuntu@<PASTE-BOX-IP-HERE> 'docker exec llama /app/llama-server --help' > raw/llama-server-help.txt 2>&1
ssh ubuntu@<PASTE-BOX-IP-HERE> 'docker logs llama 2>&1 | head -150' > raw/llama-startup-log.txt
```

*(The binary path inside the image is believed to be
`/app/llama-server`; corrected here if the runlog shows otherwise.)*

### 2. Gate 1 — only after `findings.md` is frozen (committed)

To follow the traffic live, in a second terminal (the file appears
with the first request):

```bash
tail -F docs/experiments/2026-09-22-adr-0003-gate/raw/wire.log
```

```bash
./stream_check.sh main Daniel,Moira,Ralph,Samantha
./stream_check.sh control Operator
python3 parse_stream.py main control
```

Optional baseline, to see what the model writes unconstrained:
`./stream_check.sh nogrammar none`.

### 3. Gate 2

```bash
python3 latency_probe.py            # arms A, D-off, D-on, D-live; 10 rounds; ~70 requests
python3 summarize_timings.py
ssh ubuntu@<PASTE-BOX-IP-HERE> 'docker logs llama --since 30m 2>&1' > raw/llama-log-probe.txt
```

### 4. Close

```bash
grep -rn '<the box address>' docs/experiments/2026-09-22-adr-0003-gate/   # must print nothing
```

The owner destroys the box; then `make ans-unset ENV=cloud`.

## Runlog

*Append-only. Every command actually run, in order, with its output;
mistakes included; superseded commands get a ⚠ banner pointing at
the recipe. The box address is replaced by `<PASTE-BOX-IP-HERE>`
everywhere (rule, not an edit of history); scratch-file paths are
shortened to `<scratch>/`.*

### 2026-09-22 15:26 CDT (20:26 UTC) — Entry 1: box reconnaissance

The owner had already logged in once with plain `ssh` and accepted
the host key into his default known_hosts. One read-only call:

```bash
ssh ubuntu@<PASTE-BOX-IP-HERE> 'set -x; hostname; uptime; grep PRETTY_NAME /etc/os-release; uname -r; nvidia-smi; nvidia-smi --query-gpu=name,driver_version,memory.used,memory.total,ecc.mode.current --format=csv; docker --version; nvidia-ctk --version 2>&1 | head -1; groups; df -h /; free -g; nproc; docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"; docker images --format "{{.Repository}}:{{.Tag}} {{.Size}}"; systemctl list-units --all "tts-*" --no-pager; ls -d ~/models ~/.cache/huggingface 2>&1' > <scratch>/box-recon.txt 2>&1 </dev/null
```

Output (exit 2 — only the last `ls`, which found no model caches:
expected on a fresh box):

```
+ hostname
creative-hawking
+ uptime
 20:26:24 up 30 min,  1 user,  load average: 0.02, 0.01, 0.00
+ grep PRETTY_NAME /etc/os-release
PRETTY_NAME="Ubuntu 22.04.5 LTS"
+ uname -r
6.8.0-40-generic
+ nvidia-smi
Tue Sep 22 20:26:24 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 550.90.12              Driver Version: 550.90.12      CUDA Version: 12.4     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA RTX A6000               Off |   00000000:00:06.0 Off |                  Off |
| 30%   28C    P8              5W /  300W |       2MiB /  49140MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
+ nvidia-smi --query-gpu=name,driver_version,memory.used,memory.total,ecc.mode.current --format=csv
name, driver_version, memory.used [MiB], memory.total [MiB], ecc.mode.current
NVIDIA RTX A6000, 550.90.12, 2 MiB, 49140 MiB, Disabled
+ docker --version
Docker version 27.2.1, build 9e34c9b
+ nvidia-ctk --version
+ head -1
NVIDIA Container Toolkit CLI version 1.16.1
+ groups
ubuntu adm dialout cdrom floppy sudo audio dip video plugdev netdev lxd docker
+ df -h /
Filesystem      Size  Used Avail Use% Mounted on
/dev/vda1        97G   13G   84G  14% /
+ free -g
               total        used        free      shared  buff/cache   available
Mem:              56           0          55           0           0          55
Swap:              0           0           0
+ nproc
28
+ docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'
NAMES     IMAGE     STATUS
+ docker images --format '{{.Repository}}:{{.Tag}} {{.Size}}'
+ systemctl list-units --all 'tts-*' --no-pager
  UNIT LOAD ACTIVE SUB DESCRIPTION
0 loaded units listed.
To show all installed unit files use 'systemctl list-unit-files'.
+ ls -d /home/ubuntu/models /home/ubuntu/.cache/huggingface
ls: cannot access '/home/ubuntu/models': No such file or directory
ls: cannot access '/home/ubuntu/.cache/huggingface': No such file or directory
```

Reading: a clean box of the expected image; no deploy has run (no
containers, no images, no tts unit, no model caches).

### 2026-09-22 ~15:44 CDT — Entry 2: tts-serve pin bump and inventory wiring

- `deploy/ansible/inventories/common_vars.yml:53`:
  `zr_tts_serve_version: "1.1"` → `"1.2"` (owner ruling: track the
  latest tag; the 1.1→1.2 diff is only the Apple-Silicon MLX
  engine).
- Wiring:

```bash
make ans-set ENV=cloud IP=<PASTE-BOX-IP-HERE> </dev/null 2>&1; git status --short
```

```
wired: cloud ansible_host -> <PASTE-BOX-IP-HERE>
 M deploy/ansible/inventories/cloud/hosts.yml
 M deploy/ansible/inventories/common_vars.yml
```

### 2026-09-22 15:44:35 CDT — Entry 3: deploy #1 FAILED — the package lock was held by Ubuntu's own updater

```bash
make ans-deploy ENV=cloud > <scratch>/deploy-1.log 2>&1 </dev/null
```

Ansible's log: `~/.config/zombie-radio/logs/cloud-deploy-20260922-154435.log`.
The run ended at 15:45:43 CDT. The failing task, verbatim except
that the stdout line repeated 60 times (in both `stdout` and
`stdout_lines`) is shown once:

```
TASK [base : Install base packages] ********************************************
[ERROR]: Task failed: Module failed: '/usr/bin/apt-get -y -o "Dpkg::Options::=--force-confdef" -o "Dpkg::Options::=--force-confold" -o DPkg::Lock::Timeout=60       install 'python3-venv=3.10.6-1~22.04.1' 'sox=14.4.2+git20190427-2+deb11u2ubuntu0.22.04.1' 'acl=2.3.1-1'' failed: E: Unable to acquire the dpkg frontend lock (/var/lib/dpkg/lock-frontend), is another process using it?

Origin: /Users/alfredo/workspace/hackTNT_2026/zombie-radio-claude/deploy/ansible/roles/base/tasks/main.yml:57:3

55     state: started
56
57 - name: Install base packages
     ^ column 3

fatal: [cloud-1]: FAILED! => {"cache_update_time": 1790109398, "cache_updated": false, "changed": false, "msg": "<the same apt-get command and E: line>", "rc": 100, "stderr": "E: Unable to acquire the dpkg frontend lock (/var/lib/dpkg/lock-frontend), is another process using it?\n", ..., "stdout_lines": ["Waiting for cache lock: Could not get lock /var/lib/dpkg/lock-frontend. It is held by process 2450 (unattended-upgr)...", ... 60 identical lines ...]}

PLAY RECAP *********************************************************************
cloud-1                    : ok=8    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0

make: *** [ans-deploy] Error 2
```

How to read it:

- The `[ERROR]` line alone gives only the symptom: apt could not
  take the package-database lock, "is another process using it?".
- The culprit is named only inside the long JSON dump:
  `held by process 2450 (unattended-upgr)` — the name is cut to 15
  characters because Linux keeps only that much of a process name.
- 60 identical lines plus `DPkg::Lock::Timeout=60` in the command:
  apt retried once a second for 60 seconds, then gave up. The 60
  seconds is the Ansible apt module's default `lock_timeout`; our
  task did not set one.
- `changed=0`: nothing on the box was modified before the failure.

### 2026-09-22 15:45:57 CDT (20:45:57 UTC) — Entry 4: diagnosis — who holds the lock

```bash
ssh ubuntu@<PASTE-BOX-IP-HERE> 'uptime; ps -eo pid,etime,cmd | grep -E "apt|dpkg|unattended" | grep -v grep; systemctl list-units --no-pager "apt-daily*" "unattended-upgrades*"; sudo tail -5 /var/log/unattended-upgrades/unattended-upgrades.log 2>&1; sudo tail -5 /var/log/apt/history.log' > <scratch>/box-lock.txt 2>&1 </dev/null
```

```
 20:45:57 up 50 min,  0 users,  load average: 1.00, 0.85, 0.47
   1031       50:13 /usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-signal
   2422       03:31 /bin/sh /usr/lib/apt/apt.systemd.daily install
   2426       03:31 /bin/sh /usr/lib/apt/apt.systemd.daily lock_is_held install
   2450       03:31 /usr/bin/python3 /usr/bin/unattended-upgrade
  UNIT                        LOAD   ACTIVE     SUB     JOB   DESCRIPTION
  apt-daily-upgrade.service   loaded activating start   start Daily apt upgrade and clean activities
  unattended-upgrades.service loaded active     running       Unattended Upgrades Shutdown
  apt-daily-upgrade.timer     loaded active     running       Daily apt upgrade and clean activities
  apt-daily.timer             loaded active     waiting       Daily apt download activities
...
2026-09-22 20:42:27,258 WARNING Could not figure out development release: Distribution data outdated. Please check for an update for distro-info-data. See /usr/share/doc/distro-info-data/README.Debian for details.
2026-09-22 20:42:27,258 INFO Starting unattended upgrades script
2026-09-22 20:42:27,258 INFO Allowed origins are: o=Ubuntu,a=jammy, o=Ubuntu,a=jammy-security, o=UbuntuESMApps,a=jammy-apps-security, o=UbuntuESM,a=jammy-infra-security
2026-09-22 20:42:27,258 INFO Initial blacklist: linux-headers linux-image linux-generic linux-modules nvidia libnv cuda
2026-09-22 20:42:27,259 INFO Initial whitelist (not strict):
Start-Date: 2024-09-19  13:08:34
Commandline: apt-get install nvidia-container-toolkit -y
Requested-By: ubuntu (1000)
Install: libnvidia-container1:amd64 (1.16.1-1, automatic), libnvidia-container-tools:amd64 (1.16.1-1, automatic), nvidia-container-toolkit:amd64 (1.16.1-1), nvidia-container-toolkit-base:amd64 (1.16.1-1, automatic)
End-Date: 2024-09-19  13:08:34
```

Reading:

- Ubuntu's daily upgrade job (`apt-daily-upgrade.service`) started
  `/usr/bin/unattended-upgrade` (PID 2450) at 20:42:27 UTC, 46
  minutes after boot; our deploy reached apt about three minutes
  later.
- The image's last apt activity is 2024-09-19, so this run carries
  about two years of Ubuntu security updates — it may take a while.
- The updater skips `nvidia`, `libnv`, `cuda` and the kernel
  packages (its "Initial blacklist" line): the driver cannot change
  under us.
- Why the 2026-09-19 run on the same image did not hit this: not
  verified (believed timing luck; the timer's schedule on this image
  was not read). No earlier note of this lock exists in the docs.

Options weighed with the owner: (1) wait for the updater, then
re-run unchanged — recommended; (2) stop the updater by hand —
rejected: a change outside the playbook, and interrupting it in the
middle of a package install can leave packages half-configured;
(3) make the playbook tolerate a first-boot updater run. **Owner
ruling: option 1 plus the fix of option 3.** A read-only poll of
`systemctl is-active apt-daily-upgrade.service` every 30 s was
started at 15:46 CDT.

### 2026-09-22 ~15:50 CDT — Entry 5: role fix — the apt task waits up to 15 minutes for the lock

- `deploy/ansible/roles/base/tasks/main.yml`, task
  `Install base packages` (the playbook's only apt task): added
  `lock_timeout: 900`. A fresh box now waits up to 15 minutes for a
  first-boot updater run instead of failing after 60 seconds.
- `make ans-lint` → `Passed: 0 failure(s), 0 warning(s) in 28 files
  processed of 30 encountered. Last profile that met the validation
  criteria was 'production'.`
- A related, bigger question, parked for the owner: should the base
  role switch the updater off on these disposable boxes? A
  security-policy call, not tonight's.

### 2026-09-22 15:55:13 CDT — Entry 6: deploy #2 started with the fix, while the updater still runs

Owner ruling: start the re-run now instead of waiting, so the fix
gets its live proof tonight.

```bash
make ans-deploy ENV=cloud > <scratch>/deploy-2.log 2>&1 </dev/null
```

Ansible's log: `~/.config/zombie-radio/logs/cloud-deploy-20260922-155513.log`.
At 16:02 CDT the run was waiting in `base : Install base packages`,
the updater still `activating`. *(Result: next entry.)*

### 2026-09-22 16:10:20 CDT (21:10:20 UTC) — Entry 7: deploy #2 FAILED differently — the SSH session dropped during the long lock wait

Deploy #2 waited in `base : Install base packages` as the fix
intended, then, about 14 minutes into the wait (before the 15-minute
limit), lost its connection:

```
TASK [base : Install base packages] ********************************************
[ERROR]: Task failed: Data could not be sent to remote host "<PASTE-BOX-IP-HERE>". Make sure this host can be reached over ssh:
Origin: /Users/alfredo/workspace/hackTNT_2026/zombie-radio-claude/deploy/ansible/roles/base/tasks/main.yml:57:3

55     state: started
56
57 - name: Install base packages
     ^ column 3

fatal: [cloud-1]: UNREACHABLE! => {"changed": false, "msg": "Task failed: Data could not be sent to remote host \"<PASTE-BOX-IP-HERE>\". Make sure this host can be reached over ssh:", "unreachable": true}

PLAY RECAP *********************************************************************
cloud-1                    : ok=8    changed=0    unreachable=1    failed=0    skipped=0    rescued=0    ignored=0

make: *** [ans-deploy] Error 4
```

Diagnosis, two read-only calls (outputs in the scratch files
`box-after-deploy2.txt`, `box-dpkg-2110.txt`; excerpts):

```bash
ssh -o ConnectTimeout=15 ubuntu@<PASTE-BOX-IP-HERE> 'uptime; last -x reboot shutdown | head -4; systemctl is-active apt-daily-upgrade.service; sudo tail -8 /var/log/unattended-upgrades/unattended-upgrades.log; grep -c "" /var/log/apt/history.log; sudo grep -i "openssh\|sshd" /var/log/apt/history.log | tail -3'
ssh -o ConnectTimeout=15 ubuntu@<PASTE-BOX-IP-HERE> '<dpkg.log lines 21:08:30–21:11:00; needrestart lines of unattended-upgrades-dpkg.log; ssh/docker ActiveEnterTimestamp; running apt processes>'
```

```
 21:10:39 up  1:15,  3 users,  load average: 1.02, 1.01, 0.94
reboot   system boot  6.8.0-40-generic Tue Sep 22 19:55   still running
activating
2026-09-22 20:47:57,109 INFO Packages that will be upgraded: amd64-microcode apparmor apport … openssh-client openssh-server openssh-sftp-server openssl … systemd systemd-sysv … util-linux … (259 packages)
Upgrade: openssh-client:amd64 (1:8.9p1-3ubuntu0.10, 1:8.9p1-3ubuntu0.17), openssh-server:amd64 (1:8.9p1-3ubuntu0.10, 1:8.9p1-3ubuntu0.17), openssh-sftp-server:amd64 (…)
...
2026-09-22 21:10:08 status installed coreutils:amd64 8.32-4.1ubuntu1.4
2026-09-22 21:10:22 status installed util-linux:amd64 2.37.2-4ubuntu3.6
2026-09-22 21:10:34 status installed python3-idna:all 3.3-1ubuntu0.2
...
NEEDRESTART-SVC: containerd.service … docker.service … ssh.service … user@1000.service   (a list; batch mode)
ssh.service    KillMode=process  ActiveEnterTimestamp=Tue 2026-09-22 20:48:11 UTC
docker.service ActiveEnterTimestamp=Tue 2026-09-22 19:55:46 UTC
      28:38 /usr/bin/python3 /usr/bin/unattended-upgrade
```

Reading:

- **Ruled out:** a reboot (still on the 19:55 UTC boot); an sshd
  restart at the moment of the drop (sshd last (re)started at
  20:48:11 UTC, when `openssh-server` was upgraded — seven minutes
  BEFORE deploy #2 began — and `KillMode=process` keeps existing
  sessions alive through a restart anyway); a Docker restart (up
  since boot). The `NEEDRESTART-SVC` lines are needrestart's batch
  LIST of services that would need a restart; the timestamps show
  it restarted neither ssh nor docker.
- **Not proven, two candidates:** (a) an idle-connection cutoff
  somewhere between the laptop and the box: while apt waits on the
  lock, the Ansible SSH session carries no traffic for minutes, and
  our SSH settings send no keepalives
  (`deploy/ansible/inventories/common_vars.yml:23-26` sets only
  `IdentitiesOnly`, `StrictHostKeyChecking`, `UserKnownHostsFile`;
  `deploy/ansible/ansible.cfg` sets only `pipelining`); (b)
  something the updater did at that moment (`util-linux` was being
  configured at 21:10:22 UTC) — weak, no mechanism known.
- **Progress of the updater at 21:11 UTC:** 195 distinct packages
  reached "installed" since 20:47:57 (the count includes trigger
  re-runs such as `man-db` and `libc-bin`, so it overstates) out of
  259 listed.
- **Consequence for the fix of entry 5:** `lock_timeout: 900` did
  its job (a 14-minute wait instead of a 60-second failure) but a
  single silent SSH command lasting that long is itself fragile on
  this path. The durable fix wants a different shape (owner round,
  after tonight).

### 2026-09-22 16:25:46 CDT (21:25:35 UTC) — Entry 8: the updater finished; the lock-wait fix reshaped

- The read-only poll saw `apt-daily-upgrade.service` turn `inactive`
  at 16:25:46 CDT. The updater's log: `2026-09-22 21:25:35,770 INFO
  All upgrades installed` — 43 minutes from start (20:42:27 UTC).
  It left `/var/run/reboot-required` behind (kernel and NVIDIA
  packages were skipped, so the flag comes from system libraries
  such as `libc6`, `systemd`, `dbus`); not acted on — the playbook
  never reboots and nothing tonight needs one. Docker still up since
  boot (`ActiveEnterTimestamp=Tue 2026-09-22 19:55:46 UTC`).
- Owner ruling: no automatic deploy after the updater finishes; and
  the entry-5 fix is reshaped: `lock_timeout: 900` (seconds — 15
  minutes of silence, then an obscure message) becomes:
  - `zr_apt_lock_timeout: 300` in `deploy/ansible/inventories/common_vars.yml`,
    mapped to `base_apt_lock_timeout` in `deploy/ansible/roles/base/defaults/main.yml`;
  - in `deploy/ansible/roles/base/tasks/main.yml` the apt task sits in
    a `block` whose name announces the wait limit before the wait
    begins (`Install base packages, apt lock wait limit in seconds:
    300`), and a `rescue` that — when the failure mentions the apt
    lock — stops with a plain explanation quoting apt's own "held by
    process …" line, the command to check the updater, and how to
    wait longer; any other apt failure is re-raised unchanged.
- `make ans-lint` → `Passed: 0 failure(s), 0 warning(s) … 'production'`;
  `make ans-check-syntax ENV=cloud` passes.
- The rescue logic was tested on the laptop with a scratch playbook
  mirroring it, fed a fake apt-shaped failure (not against the box):
  the lock case printed
  `Waited 60 s for the apt package lock and gave up; another process holds it: "Waiting for cache lock: Could not get lock /var/lib/dpkg/lock-frontend. It is held by process 2450 (unattended-upgr)...". On a fresh Ubuntu box this is usually the first-boot unattended-upgrades run, which can take 30+ minutes. Nothing was installed. Check it with ssh ubuntu@<box> 'systemctl is-active apt-daily-upgrade.service' (activating = still running) and re-run make ans-deploy once it reports inactive. To wait longer, raise zr_apt_lock_timeout.`;
  a non-lock failure skipped the explanation and was re-raised
  with its original message.
- The live proof on the box (a 60-second wait against the held
  lock) was approved by the owner on condition that the lock was
  still held; it was not (the updater had finished), so the live
  proof was NOT run.
- The keepalive / polling question is parked in
  `docs/follow-ups.md` with a reminder trigger.

### 2026-09-22 16:35:40 CDT — Entry 9: live proof of the lock-wait error, with aptitude holding the lock

The owner's idea: open `sudo aptitude` on the box and leave it open,
so a real process holds the apt lock. Guards: verify the lock first;
run with the three service roles switched off through their
self-gates, so that only the base role could run even if the lock
freed; the values passed as a JSON file so they arrive as booleans.
`<scratch>/lock-test.json`:

```json
{"zr_apt_lock_timeout": 10, "llama_enabled": false, "tts_engine_enabled": false, "stt_engine_enabled": false}
```

Lock check (read-only):

```bash
ssh -o ConnectTimeout=15 ubuntu@<PASTE-BOX-IP-HERE> 'sudo fuser -v /var/lib/dpkg/lock-frontend /var/lib/dpkg/lock /var/lib/apt/lists/lock 2>&1; echo "fuser exit=$?"; ps -eo pid,user,etime,cmd | grep -i [a]ptitude'
```

```
                     USER        PID ACCESS COMMAND
/var/lib/dpkg/lock-frontend:
                     root      147135 F.... aptitude
/var/lib/dpkg/lock:  root      147135 F.... aptitude
fuser exit=0
 147135 root           00:13 aptitude
```

The run (16:35:40 → 16:35:58 CDT, exit 2):

```bash
make ans-deploy ENV=cloud ANS_ARGS="-e @<scratch>/lock-test.json" > <scratch>/deploy-3-locktest.log 2>&1 </dev/null
```

Ansible's log: `~/.config/zombie-radio/logs/cloud-deploy-20260922-163540.log`.
Output from the apt task on, verbatim except that the ten identical
"Waiting for cache lock" lines (in `stdout` and `stdout_lines`) are
shown once:

```
TASK [base : Install base packages, apt lock wait limit in seconds: 10] ********
[ERROR]: Task failed: Module failed: '/usr/bin/apt-get -y -o "Dpkg::Options::=--force-confdef" -o "Dpkg::Options::=--force-confold" -o DPkg::Lock::Timeout=10       install 'python3-venv=3.10.6-1~22.04.1' 'sox=14.4.2+git20190427-2+deb11u2ubuntu0.22.04.1' 'acl=2.3.1-1'' failed: E: Unable to acquire the dpkg frontend lock (/var/lib/dpkg/lock-frontend), is another process using it?

Origin: /Users/alfredo/workspace/hackTNT_2026/zombie-radio-claude/deploy/ansible/roles/base/tasks/main.yml:59:7

57 - name: Install base packages
58   block:
59     - name: "Install base packages, apt lock wait limit in seconds: {{ base_apt_lock_timeout }}"
         ^ column 7

fatal: [cloud-1]: FAILED! => {"cache_update_time": 1790109398, "cache_updated": false, "changed": false, "msg": "<the same apt-get command and E: line>", "rc": 100, "stderr": "E: Unable to acquire the dpkg frontend lock (/var/lib/dpkg/lock-frontend), is another process using it?\n", ..., "stdout_lines": ["Waiting for cache lock: Could not get lock /var/lib/dpkg/lock-frontend. It is held by process 147135 (aptitude)...", ... 10 identical lines ...]}

TASK [base : Explain an apt lock timeout] **************************************
[ERROR]: Task failed: Action failed: Waited 10 s for the apt package lock and gave up; another process holds it: "Waiting for cache lock: Could not get lock /var/lib/dpkg/lock-frontend. It is held by process 147135 (aptitude)...". On a fresh Ubuntu box this is usually the first-boot unattended-upgrades run, which can take 30+ minutes. Nothing was installed. Check it with ssh ubuntu@<PASTE-BOX-IP-HERE> 'systemctl is-active apt-daily-upgrade.service' (activating = still running) and re-run make ans-deploy once it reports inactive. To wait longer, raise zr_apt_lock_timeout.
Origin: /Users/alfredo/workspace/hackTNT_2026/zombie-radio-claude/deploy/ansible/roles/base/tasks/main.yml:67:7

65         lock_timeout: "{{ base_apt_lock_timeout }}"
66   rescue:
67     - name: Explain an apt lock timeout
         ^ column 7

fatal: [cloud-1]: FAILED! => {"changed": false, "msg": "<the same explanation>"}

PLAY RECAP *********************************************************************
cloud-1                    : ok=8    changed=0    unreachable=0    failed=1    skipped=0    rescued=1    ignored=0

make: *** [ans-deploy] Error 2
```

Reading:

- The limit is announced in the task name before the wait begins;
  apt waited 10 s (ten once-a-second retries), then the rescue
  printed the explanation quoting the real holder. `changed=0`: the
  box is untouched.
- Two refinements put to the owner: (1) in a block/rescue Ansible
  prints the raw apt failure BEFORE the explanation; a
  register + `failed_when: false` + explicit fail shape would print
  only one error, at the cost of the apt task briefly showing `ok`;
  (2) the advice assumes the updater even when the holder is
  something else (here `aptitude`); it could adapt to the quoted
  holder.

### 2026-09-22 ~17:40 CDT — Entry 10: owner rulings before the freeze; the wire log added and tested

- **Owner prediction:** declined ("I want to see the experiment");
  recorded in `findings.md` so the slot is closed.
- **Emotion field in the grammar:** NOT in tonight's run (owner):
  first the simple grammar and its numbers; later, maybe, a
  separate run with a richer grammar to contrast what the added
  complexity costs. Parked in `docs/follow-ups.md`.
- **Wire log** (owner request, for following the traffic live):
  `raw/wire.log`, written by helpers in `cast.py` (`wire`,
  `wire_request`, `wire_response`, `wire_stream_line`), called by
  `latency_probe.py` around every request (and on a failed request,
  with the server's error text) and by `stream_check.sh` (the
  request before `curl` sends it, then each arriving chunk's text).
- **Tests, in scratch copies of the folder (not against the box,
  no port 8080):**
  - `latency_probe.py --rounds 1 --arms A,D-on` against a fake
    local server: the log shows the header, all messages, and the
    answer line with the counters for each of the six requests.
  - `stream_check.sh` end to end against a fake server that streams
    real SSE: exit 0; `parse_stream.py` reads the result; a second
    run with the same label refuses to overwrite (exit 2).
  - **A flaw found and fixed by that test:** the arrival clock
    started when the timestamping step started, not when the
    request left, so the wait for the first token was hidden
    (first chunk at `0.0 ms`), and a fast buffered answer could
    even divide by zero in the spread. Now the shell records the
    time just before `curl` launches and passes it in; the parser
    guards the zero case. Re-test against two fake servers, both
    waiting 200 ms before the first token, one streaming and one
    buffering everything:

```
== stream
chunks carrying content  : 5
first content chunk at   : 237.2 ms
last content chunk at    : 860.1 ms
spread (last-first)/last : 0.72
== lump
chunks carrying content  : 5
first content chunk at   : 1004.8 ms
last content chunk at    : 1007.1 ms
spread (last-first)/last : 0.00
```

  The gate-1 criterion (spread at least 0.50) separates the two.

### 2026-09-22 17:40:18 CDT — Entry 11: deploy #3 from zero PASSES; re-run changed=0; three services ok through the tunnel

The owner closed aptitude and re-wired the inventory
(`make ans-set`; he had run `make ans-unset` before the commits).
Pre-check that `hosts.yml` carries no sentinel, then:

```bash
make ans-deploy ENV=cloud > <scratch>/deploy-4.log 2>&1 </dev/null
```

```
Tue Sep 22 17:40:18 CDT 2026
exit=0
Tue Sep 22 17:47:25 CDT 2026
PLAY RECAP *********************************************************************
cloud-1                    : ok=33   changed=16   unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

About 7 minutes from zero (the handoff's figure was ~15). The log's
`FAILED - RETRYING` lines are the health waits polling while each
service loads (llama 5 retries, tts 2, stt 1) — expected, not
failures. The apt task (`Install base packages, apt lock wait limit
in seconds: 300`) went straight through: the lock was free.

The converge invariant:

```bash
make ans-deploy ENV=cloud > <scratch>/deploy-5-rerun.log 2>&1 </dev/null
```

```
Tue Sep 22 17:47:36 CDT 2026
exit=0
Tue Sep 22 17:48:06 CDT 2026
PLAY RECAP *********************************************************************
cloud-1                    : ok=31   changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
```

Through the owner's tunnel:

```bash
make check
```

```
llama:   ok
tts:     ok
whisper: ok
```

Reading: the from-zero deploy works with tts-serve pinned at 1.2
and the reshaped apt lock wait; `changed=0` holds. (The pin
follow-up's remaining step — one TalkWithMe synthesis through the
tunnel — is not part of this gate.)

### 2026-09-22 ~17:49 CDT — Entry 12: what the server is (recipe step 1)

```bash
cd docs/experiments/2026-09-22-adr-0003-gate
mkdir -p raw
curl -s http://localhost:8080/props > raw/props.json                 # 6127 bytes
curl -s http://localhost:8080/v1/models > raw/models.json            # 777 bytes
ssh -o ConnectTimeout=15 ubuntu@<PASTE-BOX-IP-HERE> 'docker exec llama /app/llama-server --help' > raw/llama-server-help.txt 2>&1    # 729 lines
ssh -o ConnectTimeout=15 ubuntu@<PASTE-BOX-IP-HERE> 'docker logs llama 2>&1 | head -150' > raw/llama-startup-log.txt 2>&1          # 11 lines
```

All exit 0; the binary path `/app/llama-server` was right. The
facts that matter (from those files):

- **Build** `b11096-c550d2f60` (`props.json` `build_info`); model
  alias `bartowski/nvidia_NVIDIA-Nemotron-Nano-9B-v2-GGUF:Q4_K_M`;
  `total_slots` 1; `n_ctx` 16384. Sampler defaults unchanged from
  2026-09-19: temperature 0.8, top_k 40, top_p 0.95, min_p 0.05,
  repeat_penalty 1.0 (off), dry 0, mirostat 0; `reasoning_format`
  none (the server does not split thinking into
  `reasoning_content`).
- **Host-RAM prompt cache EXISTS and is ON by default**
  (`llama-server-help.txt:434`): `-cram, --cache-ram N  set the
  maximum cache size in MiB (default: 8192, -1 - no limit, 0 -
  disable)` — caveat 5 of `findings.md` confirmed as a fact of this
  build.
- **Context checkpoints** (`llama-server-help.txt:427-433`): up to 32
  per slot (`--ctx-checkpoints`), with `--checkpoint-min-step`
  "minimum spacing between context checkpoints in tokens (default:
  8192…)" — far larger than our prompts (hundreds to ~2 000 tokens);
  relevant to caveat 4 (the hybrid model). `--cache-reuse` (KV
  shifting) default 0 = off.
- **The chat template answers the `/no_think` question**
  (`props.json` `chat_template`, excerpts): `/no_think` in any
  system or user message sets `enable_thinking=false` and is
  REMOVED from the text (`.replace('/no_think', '')`); the prompt
  then ends with `<SPECIAL_11>Assistant\n<think></think>` — an
  empty, already-closed think block. Without it the prompt ends with
  `<SPECIAL_11>Assistant\n<think>\n`, i.e. the model starts INSIDE a
  think block; with a grammar on, the script would then be forced
  into what the model takes for its thinking. Also: previous
  assistant turns are rendered WITHOUT the `<think></think>` prefix
  (the template drops everything up to `</think>`), so the cached
  prompt of round k and the prompt of round k+1 part ways exactly
  where round k's reply began.
- Startup log (11 lines) notable lines: `load_model: initializing,
  n_slots = 1, n_ctx_slot = 16384, kv_unified = 'false'`;
  `W load: special_eos_id is not in special_eog_ids - the tokenizer
  config may be incorrect`.

### 2026-09-22 17:50–17:51 CDT — Entry 13: gate 1 — three streamed requests

The owner followed along with `tail -F raw/wire.log`.

```bash
./stream_check.sh main Daniel,Moira,Ralph,Samantha > /dev/null      # 17:50:37, exit 0
./stream_check.sh control Operator > /dev/null                      # 17:50:47, exit 0
./stream_check.sh nogrammar none > /dev/null                        # 17:51:02, exit 0
python3 parse_stream.py main control nogrammar
```

```
== main
grammar allowlist        : ['Daniel', 'Moira', 'Ralph', 'Samantha']
data lines               : 75 (incl. [DONE]: True)
errors                   : none
chunks carrying content  : 72
chunks carrying reasoning: 0
first content chunk at   : 552.3 ms
last content chunk at    : 1367.1 ms
spread (last-first)/last : 0.60
finish_reason            : stop
content, verbatim        : 'Daniel: Power fluctuation detected. Systems stabilizing. Over.  \nMoira: Specimens in the east wing may have been exposed. We need to confirm. Over.  \nRalph: Counting down to evacuation. Four doors, three breaches. Over.  \nSamantha: We’re holding transmission. Stay calm, everyone. Over.\n'
  line 1: legal   'Daniel: Power fluctuation detected. Systems stabilizing. Over.  '
  line 2: legal   'Moira: Specimens in the east wing may have been exposed. We need to confirm. Over.  '
  line 3: legal   'Ralph: Counting down to evacuation. Four doors, three breaches. Over.  '
  line 4: legal   'Samantha: We’re holding transmission. Stay calm, everyone. Over.'
complete lines           : 4
text after last newline  : ''
speakers used            : ['Daniel', 'Moira', 'Ralph', 'Samantha']
final timings            : {"cache_n": 0, "prompt_n": 269, "prompt_ms": 420.045, "prompt_per_token_ms": 1.5615055762081784, "prompt_per_second": 640.4075753788285, "predicted_n": 73, "predicted_ms": 814.529, "predicted_per_token_ms": 11.312902777777778, "predicted_per_second": 88.39464279356537}

== control
grammar allowlist        : ['Operator']
data lines               : 112 (incl. [DONE]: True)
errors                   : none
chunks carrying content  : 109
chunks carrying reasoning: 0
first content chunk at   : 290.6 ms
last content chunk at    : 1593.8 ms
spread (last-first)/last : 0.82
finish_reason            : stop
content, verbatim        : "Operator: Generator's acting up again, might be a good idea to check if it's safe to head over to it. Over.  \nOperator: East wing lights flickering—could be a power surge or something worse. Over.  \nOperator: Ralph, you're counting the shamblers, right? Need to know if they're closing in. Over.  \nOperator: Samantha, you're handling the broadcast, but we should keep the signal strong. Over.\n"
  line 1: legal   "Operator: Generator's acting up again, might be a good idea to check if it's safe to head over to it. Over.  "
  line 2: legal   'Operator: East wing lights flickering—could be a power surge or something worse. Over.  '
  line 3: legal   "Operator: Ralph, you're counting the shamblers, right? Need to know if they're closing in. Over.  "
  line 4: legal   "Operator: Samantha, you're handling the broadcast, but we should keep the signal strong. Over."
complete lines           : 4
text after last newline  : ''
speakers used            : ['Operator']
final timings            : {"cache_n": 265, "prompt_n": 4, "prompt_ms": 159.787, "prompt_per_token_ms": 39.94675, "prompt_per_second": 25.0333256147246, "predicted_n": 110, "predicted_ms": 1300.343, "predicted_per_token_ms": 11.929752293577982, "predicted_per_second": 83.82403719633973}

== nogrammar
grammar allowlist        : none (no grammar sent)
data lines               : 75 (incl. [DONE]: True)
errors                   : none
chunks carrying content  : 72
chunks carrying reasoning: 0
first content chunk at   : 270.8 ms
last content chunk at    : 1117.7 ms
spread (last-first)/last : 0.76
finish_reason            : stop
content, verbatim        : 'Daniel: Power fluctuation detected. Systems stabilizing. Over.  \nMoira: Specimens in the east wing may have been exposed. We need to confirm. Over.  \nRalph: Counting down to evacuation. Four doors, three breaches. Over.  \nSamantha: We’re holding transmission. Stay calm, everyone. Over.\n'
  line 1: legal   'Daniel: Power fluctuation detected. Systems stabilizing. Over.  '
  line 2: legal   'Moira: Specimens in the east wing may have been exposed. We need to confirm. Over.  '
  line 3: legal   'Ralph: Counting down to evacuation. Four doors, three breaches. Over.  '
  line 4: legal   'Samantha: We’re holding transmission. Stay calm, everyone. Over.'
complete lines           : 4
text after last newline  : ''
speakers used            : ['Daniel', 'Moira', 'Ralph', 'Samantha']
final timings            : {"cache_n": 265, "prompt_n": 4, "prompt_ms": 138.848, "prompt_per_token_ms": 34.712, "prompt_per_second": 28.808481216870245, "predicted_n": 73, "predicted_ms": 813.653, "predicted_per_token_ms": 11.300736111111112, "predicted_per_second": 88.48981076699772}

```

Reading:

- **main:** 72 content chunks, spread 0.60, four complete legal
  lines using all four allowed speakers — criteria (a) and (b) met.
- **control:** every line is `Operator:` although the prompt asks
  for the four scientists; the text shows the model steering around
  the constraint ("Ralph, you're counting the shamblers, right?") —
  criterion (c) met. The top-level `grammar` field on
  `/v1/chat/completions` binds.
- **nogrammar:** the SAME four lines as main, character for
  character (same prompt, same seed): with this cast sheet the
  model's own output already fits the format, so the grammar masked
  nothing — here it acted as a guarantee, not a steer. On identical
  output the generation cost is 11.31 ms/token with the grammar
  versus 11.30 without (an early, ungraded hint for gate 2b).
- **Cache, first sight:** control and nogrammar sent the same prompt
  as main; the server reused 265 of 269 prompt tokens
  (`cache_n=265`, `prompt_n=4`) — reuse works on this hybrid model
  for an identical prefix. The 4 re-evaluated tokens took 160 and
  139 ms (about 35–40 ms per token versus about 1.6 ms per token for
  main's cold 269), which suggests a fixed cost for restoring a saved
  state — to be read against gate 2's numbers, not concluded here.
- **For the fork's parser:** the model ends lines with two spaces
  before the newline (`Over.  \n`, a Markdown line-break habit);
  trim trailing whitespace per line.

### 2026-09-22 17:54:21 CDT — Entry 14: gate 2 — the latency probe (71 requests), the summary, the server's log

```bash
python3 latency_probe.py > <scratch>/probe-stdout.txt 2>&1    # 17:54:21 → 17:56:20 CDT, exit 0, 71 files in raw/probe/
cp <scratch>/probe-stdout.txt raw/latency_probe.stdout.txt     # the per-request console lines, kept
python3 summarize_timings.py
ssh -o ConnectTimeout=15 ubuntu@<PASTE-BOX-IP-HERE> 'docker logs llama --since 30m 2>&1' > raw/llama-log-probe.txt    # 532 lines
```

`summarize_timings.py`, verbatim:

```
== arm A
round req  prompt  evald reused reuse% prompt_ms gen_n   gen_ms ms/tok  wall_ms
    1   4     665    665      0      0    1515.5    59    628.5  10.65   4365.3
    2   4    1186    660    526     44    1414.5    57    609.5  10.69   5144.2
    3   4    1703    652   1051     62    1422.5    58    620.7  10.70   5246.1
    4   4    2195    627   1568     71    1418.4    55    590.6  10.74   5561.4
    5   4    2717    654   2063     76    1441.1    81    884.0  10.91   6523.7
    6   4    3198    615   2583     81    1440.2    90    984.7  10.94   7360.4
    7   4    3708    642   3066     83    1459.3    85    931.4  10.96   7572.0
    8   4    4237    667   3570     84    1492.3    73    800.0  10.96   7864.9
    9   4    4752    653   4099     86    1572.5    64    695.3  10.86   8585.7
   10   4    5250    630   4620     88    1486.2    69    751.6  10.89   9385.4

== arm D-off
round req  prompt  evald reused reuse% prompt_ms gen_n   gen_ms ms/tok  wall_ms
    1   1     269    269      0      0     354.1    73    813.4  11.14   2569.6
    2   1     416    201    215     52     373.0   102   1144.9  11.22   1717.4
    3   1     559    195    364     65     362.4   127   1430.1  11.26   2010.6
    4   1     698    191    507     73     356.5   105   1182.2  11.26   1795.0
    5   1     843    197    646     77     351.1   100   1121.8  11.22   1646.5
    6   1     980    191    789     81     352.4    90   1018.4  11.32   1546.1
    7   1    1119    191    928     83     359.8    98   1104.7  11.27   1708.5
    8   1    1265    200   1065     84     355.8    92   1041.4  11.32   1635.3
    9   1    1412    199   1213     86     352.8    98   1107.4  11.30   1642.0
   10   1    1550    189   1361     88     354.6    86    968.3  11.26   1525.8

== arm D-on
round req  prompt  evald reused reuse% prompt_ms gen_n   gen_ms ms/tok  wall_ms
    1   1     269     54    215     80     361.1    73    819.3  11.22   2657.2
    2   1     416    201    215     52     368.6   102   1151.4  11.29   1693.3
    3   1     559    195    364     65     362.0   127   1435.7  11.30   1969.9
    4   1     698    191    507     73     361.0   105   1189.6  11.33   1718.5
    5   1     843    197    646     77     355.2   100   1126.7  11.27   1772.7
    6   1     980    191    789     81     354.4    90   1017.1  11.30   1547.4
    7   1    1119    191    928     83     353.6    98   1108.0  11.31   1644.3
    8   1    1265    200   1065     84     354.1    92   1041.0  11.31   1611.3
    9   1    1412    199   1213     86     353.0    98   1106.9  11.29   1734.0
   10   1    1550    189   1361     88     355.7    86    969.8  11.28   1537.4

== arm D-live
round req  prompt  evald reused reuse% prompt_ms gen_n   gen_ms ms/tok  wall_ms
    1   1     269     54    215     80     364.1    73    820.9  11.24   1352.2
    2   1     390    175    215     55     373.0    79    888.1  11.24   1463.7
    3   1     517    179    338     65     360.8    77    869.4  11.29   1403.7
    4   1     642    177    465     72     357.7    77    867.8  11.27   1398.2
    5   1     769    179    590     77     358.2    74    836.7  11.31   1436.0
    6   1     891    176    715     80     351.0    82    926.1  11.29   1529.4
    7   1    1023    184    839     82     353.4    76    853.6  11.23   1427.4
    8   1    1147    178    969     84     352.0    74    829.7  11.21   1368.5
    9   1    1268    173   1095     86     352.5    75    844.1  11.25   1389.6
   10   1    1386    169   1217     88     353.6    72    804.6  11.18   1433.6

== gate 2a: R_k = D-off prompt_ms / A prompt_ms (A = sum of its four requests)
  round  1: R = 0.234   (wall-time ratio, reported only: 0.589)
  round  2: R = 0.264   (wall-time ratio, reported only: 0.334)
  round  3: R = 0.255   (wall-time ratio, reported only: 0.383)
  round  4: R = 0.251   (wall-time ratio, reported only: 0.323)
  round  5: R = 0.244   (wall-time ratio, reported only: 0.252)
  round  6: R = 0.245   (wall-time ratio, reported only: 0.210)
  round  7: R = 0.247   (wall-time ratio, reported only: 0.226)
  round  8: R = 0.238   (wall-time ratio, reported only: 0.208)
  round  9: R = 0.224   (wall-time ratio, reported only: 0.191)
  round 10: R = 0.239   (wall-time ratio, reported only: 0.163)
  R_early (mean of rounds (2, 3, 4)) = 0.257
  R_late  (mean of rounds (8, 9, 10)) = 0.234
  thresholds: PASS R_late <= 0.50 and R_late <= R_early; PARTIAL R_late < 1.0; FAIL R_late >= 1.0

== gate 2b: grammar overhead on generation, median over rounds of predicted_ms / predicted_n
  D-off median ms/token = 11.260
  D-on  median ms/token = 11.298
  O = (on - off) / off  = 0.3 %
  thresholds: PASS O <= 10 %; PARTIAL 10 % < O <= 25 %; FAIL O > 25 %

== D-live (reported, not graded): share of the prompt reused from the cache, rounds >= 2
  per round: ['55', '65', '72', '77', '80', '82', '84', '86', '88'] %
  minimum  : 55 %
```

The server's own log (`raw/llama-log-probe.txt`), two excerpts.

A late request of arm A (task 1007 = `A-r10-0-Moira`: launch 41 of 74 in the log, and its 131 prompt tokens and 13 generated match that request) —
the slot is chosen "by LRU" (its content does not match this
persona's prompt), and the task starts processing about 1.7 s later
(13.40.800 → 13.42.493 in the log's minutes.seconds.milliseconds
clock); the reported prompt evaluation is 371 ms:

```
13.40.587.044 I slot      release: id  0 | task 989 | stop processing: n_tokens = 1232, truncated = 0
13.40.800.350 I slot get_availabl: id  0 | task -1 | selected slot by LRU, t_last = 10795759070
13.42.493.810 I slot launch_slot_: id  0 | task 1007 | processing task, is_child = 0
13.43.007.493 I slot print_timing: id  0 | task 1007 | prompt eval time =     371.21 ms /   131 tokens (    2.83 ms per token,   352.90 tokens per second)
13.43.007.504 I slot print_timing: id  0 | task 1007 |        eval time =     142.43 ms /    13 tokens (   11.87 ms per token,    84.25 tokens per second)
13.43.007.505 I slot print_timing: id  0 | task 1007 |       total time =     513.64 ms /   144 tokens
```

A late request of arm D-on (task 2610 = `D-on-r06`: launch 60 of 74; D-off-r06 has the same token counts, the position decides) —
the slot is chosen "by LCP similarity" (it already holds this
conversation's prefix) and the task starts 0.6 ms later:

```
14.17.616.929 I slot      release: id  0 | task 2507 | stop processing: n_tokens = 942, truncated = 0
14.17.850.310 I slot get_availabl: id  0 | task -1 | selected slot by LCP similarity, f_sim_best = 0.855 (> 0.100 thold), f_keep = 0.890
14.17.850.930 I slot launch_slot_: id  0 | task 2610 | processing task, is_child = 0
14.19.222.415 I slot print_timing: id  0 | task 2610 | prompt eval time =     354.37 ms /   191 tokens (    1.86 ms per token,   538.99 tokens per second)
```

And the size of the host-RAM cache entries being moved (three
eviction lines, the only ones in the log):

```
13.50.176.271 W srv         alloc:  - making room for prompt cache entry, removing oldest entry (size = 421.725 MiB)
14.08.013.062 W srv         alloc:  - making room for prompt cache entry, removing oldest entry (size = 416.830 MiB)
14.08.043.744 W srv         alloc:  - making room for prompt cache entry, removing oldest entry (size = 1824.445 MiB)
```

Reading (facts only; interpretation goes to `findings.md`):

- Gate 2a quantity: `R_late = 0.234`, `R_early = 0.257`.
- Gate 2b quantity: `O = 0.3 %`. D-off and D-on generated the same
  number of tokens in every round (the same seed and prompt gave the
  same text: the grammar masked nothing), so the comparison is on
  identical output.
- D-live: reuse share from 55 % (round 2) to 88 % (round 10).
- Arm A's reuse share climbs from 44 % to 88 %: the host-RAM prompt
  cache restored each persona's saved state (caveat 5). But A's
  WALL time per round grows from 4.4 s to 9.4 s while its reported
  prompt time stays flat (about 1.4–1.6 s per round): the log shows
  a gap between choosing the slot and starting the task on A's
  requests (about 1.7 s in the excerpt) that `timings` does not
  include; D's requests show no such gap. The wall-time ratio D/A
  (reported only) falls from 0.59 at round 1 to 0.16 at round 10.
- Every request's prompt phase costs about 350 ms whether it
  evaluates 130 or 270 tokens (A and D alike): a fixed floor per
  request on this build and model.
- The per-task gap figures above are read off two timestamps each;
  a script over the whole log would make them a derived series
  (proposed to the owner, not written yet).

### 2026-09-22 ~18:30 CDT — Entry 15: what the model wrote in the D arms (after the run, no box)

A claim of entry 14 — "D-off and D-on wrote the same text" — rested
on equal token counts; checked on the text itself, and the line
shape and endings counted, with a committed script (added after the
run; it derives, it does not measure):

```bash
python3 check_outputs.py
```

```
rounds where D-off and D-on wrote identical text: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
D-off  lines per round: [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]  not `Name: text`: 0  ending in 'Over.': 40 of 40
D-on   lines per round: [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]  not `Name: text`: 0  ending in 'Over.': 40 of 40
D-live lines per round: [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]  not `Name: text`: 0  ending in 'Over.': 40 of 40
```

Reading: the claim holds on the text, all ten rounds. Every D reply,
with or without the grammar and with its own output fed back, had
exactly four well-formed lines, each ending in "Over." — the model
always used the full "up to four lines" budget.
