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
  the gate-1 request.
- `stream_check.sh` — gate 1: one streamed request through the
  tunnel with `curl -sN`; every SSE line saved with its arrival time
  in milliseconds to `raw/stream/<label>.sse.txt`, the request to
  `raw/stream/<label>.request.json`.
- `parse_stream.py` — derives the gate-1 facts from those files.
- `latency_probe.py` — gate 2: arms A, D-off, D-on, D-live (defined
  in `findings.md`), ten rounds, non-streamed; one JSON file per
  request under `raw/probe/` (request, response with `timings`,
  wall time).
- `summarize_timings.py` — derives every gate-2 number from
  `raw/probe/`.
- `raw/` — the record of truth, committed.

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
