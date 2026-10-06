# Deploying to the local 3090 — the scouting, the decisions, and the plan (the demo's goal 4)

**Date:** 2026-10-02 · **Arc:** MVP prototype · **Branch:**
`alfre2v/todo-2026-10-02`
**Type:** discussion — the plan document for the demo's goal 4 (automated
deployment to a local GPU, the owner's 3090): what is already built, what the
playbook requires and does to a machine, the decisions to make, the facts to
gather, and an executable plan; meant to guide the task when it opens.
**Status:** IN PROGRESS (since 2026-10-06; paused 2026-10-03 to 10-05) — scouting done (2026-10-02, evening).
**§8 (the same night):** an SSH key
login from the Mac to the 3090 (`ssh zr-3090`, done), the repo cloned there,
a Claude session there with the Mac's memory copied and a ready prompt
(§8.4). **§9 (2026-10-02 night to 10-03):** the memory copied and checked,
**the §5 checks all passed**, sudo by keyboard (`-K`) decided, the owner's
lean on D4 (no start at boot) estimated; **paused by the owner while away
from home** (§9.5). **§10 (2026-10-06): resumed** from a Claude session on
the 3090 — D1 (both `local` and a new `lan`), D3 and D4 (nothing at boot;
`make ans-start` / `ans-stop`) decided and built on `alfre2v/linux-3090`,
every download in `~/zombie-radio-data`, the Makefile's macOS-only `sed`
fixed. **§10.10 (the same night): deployed** with `ENV=local` — three
failures on the way (a stale apt key, Ansible picking the project's
Python, a stale ghcr.io login), then `changed=16` and a second run at
`changed=0`; the reboot test postponed. **§10.12: D2 (the tunnel) and D5
(proven at home) ruled** — goal 4 is met when a show runs from the laptop
against the 3090 and is recorded.
**Trigger to revisit:** `lan` from the laptop, or the reboot test (§10.11).

## §1. Why this document

**The owner (verbatim), 2026-10-02:** "Before I merge #24... I want to
tentatively start discussing how to implement: (4) Goal 4, the 3090
(deployment to a local GPU). I am not necessarily opening the task yet, just
scouting the way to decide how to proceed." Then, on the scouting: "record this
scouting in a discussion document, it will be not just for the scouting but
this will be our plan document to eventually guide us to implement the task of
deploying to the local 3090. I was thinking to call it
`{date}-local-deployment-plan.md` (propose other names if you dislike this
one)." — the agent offered `local-gpu-deployment-plan` ("local" alone may
read as the laptop, where the client already runs); the owner: "I like more
your name, change the name." — this document's name.

**The goal:** the demo's goal 4 (the owner, 2026-09-30; [discussion
2026-09-30] demo-goals) — automated deployment to a local GPU — "built, never
run". The 3090 has 24 GB. The board: [discussion 2026-10-02]
board-before-demo, item 4.

## §2. What is already built (checked 2026-10-02)

- **An inventory, `deploy/ansible/inventories/local/`**, beside `cloud/`:
  the same three groups (`llama`, `tts_engine`, `stt_engine`) on one host,
  `local-1`, with **`ansible_host: localhost` and `ansible_connection:
  local`** — designed for the playbook to run **on the 3090 itself**
  ([discussion 2026-09-17] ansible-deployment-shape: "localhost,
  ansible_connection=local").
- **`group_vars/all/00-common.yml`** — a symlink to the shared
  `common_vars.yml`: the same pinned versions (llama.cpp `server-cuda-b11096`,
  tts-serve 1.2 with Faster Qwen3-TTS, Whisper `small` by digest), the **32k
  context** (`zr_llama_ctx: 32768`), one slot, the ports 8080 / 8001 / 8002,
  `zr_cuda_variant: cu128`, `ansible_user` and `zr_service_user: ubuntu`, the
  SSH key `~/.ssh/hyperstack_2026`.
- **`group_vars/all/99-local.yml`** — a placeholder: `zr_environment: local`
  and "Local box overrides land here (e.g. zr_service_user, zr_models_dir) the
  day the localhost target gets tested." **Never run.**
- **The Makefile** takes `ENV=local` like `ENV=cloud` (`ans-deploy`,
  `ans-check-syntax`, `ans-set`, `ans-unset`, `ssh-tunnel`). **Two details
  matter for a LAN box:**
  - `ans-set` / `ans-unset` swap a sentinel, `REPLACE_ME_box_ip`, in the
    env's `hosts.yml` — the cloud's carries it (with `# NEVER_COMMIT`); the
    local one does not (it says `localhost`);
  - **`ssh-tunnel` reads the SSH user and key from `common_vars.yml` only**
    (`ubuntu`, `~/.ssh/hyperstack_2026`), not from a `99-<env>.yml` override.

## §3. What the playbook requires, and what it does to a machine

**Required, never installed** — the base role checks, and stops when one is
missing (`deploy/ansible/roles/base/tasks/main.yml`): **Ubuntu** (22.04 and
24.04 used in the cloud); **Docker**; **the NVIDIA container toolkit**; **an
NVIDIA driver R525 or newer** — the CUDA generation `cu128`: proven on R570,
backward compatible on R580+, unproven on R525-R565 (`common_vars.yml`); the
spec's contract (§7): "Ubuntu, Docker, nvidia-container-toolkit, a driver for
CUDA 12 (R525 or newer)". And: `become: true` (sudo), the service user's home
for the models.

**What it does:**

- installs a few apt packages (it waits up to 5 minutes for the apt lock);
- runs **llama.cpp and Whisper as Docker containers** with `network_mode:
  host`, restarted unless stopped — **so they start again at every boot**;
- installs **the voice (tts-serve) as a systemd unit, enabled — started at
  every boot**, in its own Python environment;
- binds all three **to the machine's loopback** (`zr_bind_host`): not
  reachable from the network without a tunnel;
- **touches no firewall and no SSH setting.**
- **Size:** the stack held 14,477 MiB on the A6000 at 32k (the 3090 has 24 GB);
  the first deploy downloads about 11 GB of models (plus the images and the
  voice's environment); on the cloud, a from-zero deploy took about 7 minutes.

## §4. The decisions to make

| # | Decision | The options | The agent's lean, and why |
|---|---|---|---|
| D1 | **Where Ansible runs** | **(a)** on the 3090 itself, as built: clone zombie-radio there, install `uv`, `make ans-deploy ENV=local`, the sudo password with `ANS_ARGS=-K`; **(b)** from the laptop over SSH, **like the cloud**: the 3090 one more box, at a LAN address | **(b)**: a small inventory change (the sentinel `REPLACE_ME_box_ip  # NEVER_COMMIT` in place of `localhost`, no `ansible_connection: local`) and the known flow works unchanged — `make ans-set ENV=local IP=…`, `make ans-deploy ENV=local`, `make ssh-tunnel ENV=local`, the installed client as it is; and it tells the better story: *the same playbook, from the same laptop, to a cloud GPU or a GPU at home*. Needs an SSH server on the 3090 and the laptop's key on it |
| D2 | **How the laptop reaches the services** | the SSH tunnel, as with the cloud; or the services exposed on the LAN (`zr_bind_host` overridden) | **the tunnel**: the client's settings stay `localhost:8080/8001/8002`, nothing listens openly on the home network, the security rules unchanged. One tunnel at a time (the cloud's and the 3090's use the same local ports) |
| D3 | **The 3090's user and key** | the playbook assumes `ubuntu` and the Hyperstack key | overrides in `99-local.yml` (`ansible_user`, `zr_service_user`, `ansible_ssh_private_key_file`; the models then under that user's home); and **`ssh-tunnel` taught to honour the env's overrides** (§2) — unless the 3090's user and key happen to match |
| D4 | **Living with it on a personal machine** | the services start at **every boot** and hold about 14.5 GB of the 3090's memory | a written way to stop them and keep them stopped after the demo (`docker stop llama whisper`, `docker update --restart=no`, `systemctl disable --now` for the voice), or an option not to start them at boot — the owner's call, by what else the 3090 is used for |
| D5 | **What "goal 4 met" means** | **(i)** proven at home: a deploy from zero, a second run at `changed=0`, a show from the laptop against the 3090 — recorded as evidence for the talk; **(ii)** used live at the venue, reaching home over the internet | **(i)**: reaching home from the venue opens a path into the home network and leans on two networks on demo day — after the demo, if ever |

## §5. The facts to gather on the 3090 (the owner; all read-only)

```bash
# 1. The OS (the playbook asserts Ubuntu)
lsb_release -ds
# 2. The GPU, its driver and its memory in use now (R525 or newer; R570+ ideal)
nvidia-smi --query-gpu=name,driver_version,memory.total,memory.used --format=csv
# 3. Docker, and whether it knows the NVIDIA runtime
docker --version; docker info 2>/dev/null | grep -i -E 'runtimes|nvidia'
# 4. The NVIDIA container toolkit
nvidia-ctk --version
# 5. Free disk where the models would go (about 11 GB of models, plus images and the voice's environment)
df -h /home
# 6. Whether an SSH server runs (needed for D1 option b)
systemctl is-active ssh
# 7. Whether anything already listens on the stack's ports (8080, 8001, 8002)
ss -ltnp | grep -E ':(8080|8001|8002)\b' || echo "ports free"
```

And in words: is the 3090 a desktop used for other things (games, other GPU
work; a desktop session holds some of the GPU's memory)? Is it on the same LAN
as the laptop? **Its address goes in chat only when the inventory is wired —
never in a document or a commit** (the rule for every box).

## §6. The plan (executable once §4 and §5 are settled; written for D1 = b, D2 = tunnel, D5 = i)

1. **The owner's facts** (§5). Any missing prerequisite — Docker, the
   toolkit, a driver older than R525 — is the owner's to install: the
   playbook never installs them. Stop here until they pass.
2. **The decisions** (§4), recorded in this document.
3. **A branch** in this repository:
   - `inventories/local/hosts.yml` — the cloud's shape: `ansible_host:
     REPLACE_ME_box_ip  # NEVER_COMMIT`, no `ansible_connection: local`;
   - `inventories/local/group_vars/all/99-local.yml` — the 3090's user and
     key (D3), and anything §5 calls for;
   - `Makefile` — `ssh-tunnel` (and any target that reads the user or key)
     honouring `99-<env>.yml` (D3), if the user or key differ;
   - a dry run first: `make ans-check-syntax ENV=local`, then
     `make ans-deploy ENV=local ANS_ARGS=--check` once wired;
   - lint clean on the `production` profile.
4. **Wire it:** `make ans-set ENV=local IP=<the 3090's LAN address>` — the
   owner gives the address in chat; **`inventories/local/hosts.yml` is then
   NEVER_COMMIT**, like the cloud's (staged by explicit path only; IP scan on
   the staged diff).
5. **Deploy from zero:** `make ans-deploy ENV=local` — the owner runs it (the
   owner owns the deploys); about 11 GB of models to download the first time.
6. **The converge invariant:** a second `make ans-deploy ENV=local` reports
   `changed=0`.
7. **Measure:** on the 3090, `nvidia-smi` per process (the runbook
   `docs/runbooks/box-inspection.md`), against the A6000's 14,477 MiB; and
   the context llama.cpp runs with (`/props`: `n_ctx 32768`).
8. **Reach it:** close the cloud's tunnel; `make ssh-tunnel ENV=local`; probe
   the three ports (200 each).
9. **A show against the 3090** — the installed client unchanged (its settings
   point at the tunnel's local ports): the API checks of the `tz-0.6` release
   ([discussion 2026-10-01] sound-effects §8.23) and the owner's listening;
   a recording for the talk (the evidence of goal 4).
10. **D4's recipe:** stop the services and keep them stopped (or the
    boot-time option), written in a runbook.
11. **The docs:** the runbook for a local box; the spec (§7, deployment: the
    local target as built); the TODO (goal 4 met); `make ans-unset ENV=local`
    after.

## §7. Risks and open questions

- **The driver:** a desktop may run an older or a newer driver branch than
  the cloud's R570; R525-R565 are "unproven" for `cu128`, below R525 the base
  role stops. Changing a desktop's driver is the owner's decision.
- **Docker and the toolkit may be missing** on a desktop — the owner installs
  them (the playbook only asserts).
- **The GPU's memory is shared** with a desktop session and anything else
  running; 24 GB less the desktop's share must still hold the stack's
  ~14.5 GB.
- **The services at every boot** (D4) — and the voice's systemd unit runs as
  the service user.
- **The ports** 8080, 8001, 8002 may already be taken on a home machine (§5,
  check 7).
- **Sudo:** the cloud's `ubuntu` has passwordless sudo; a home user may not —
  `ANS_ARGS=-K` asks for the password.
- **Time:** the demo is 2026-10-08; the deploy itself is minutes, the
  unknowns are the prerequisites (§5).

## §8. Addendum, 2026-10-02, night — working on the 3090: three tracks, and where they stand

**The owner (verbatim):** "So, I installed Claude Code also in the 3090 linux
desktop. My idea was to work from inside the machine with you to diagnose any
problem with a model. However, I do not see this project transcripts in the
linux Claude App. What is going on?"

**Why no transcripts:** Claude Code keeps each session **on the machine where
it ran** — the Mac's under
`~/.claude/projects/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/`
(a `.jsonl` per session), and the agent's memory in a `memory/` folder beside
them; local sessions are not synced between machines (only cloud sessions
live on a server), and the folder is named after the repo's path, which
differs on Linux. A session on the 3090 starts with no history and no memory —
but with **the memory of record**, `CLAUDE.md` and `docs/`, once the repo is
cloned there. (Checked on the 3090: `~/.claude` existed with **no
`projects/` folder** — no Code session had run there yet.)

**Three ways were offered** — A: this Mac session reaches the 3090 over SSH;
B: a fresh session on the 3090, started with a re-orientation prompt; C: the
Mac's memory folder copied to the 3090. **The owner (verbatim):** "I will go
with a combination of A, B and C. How about that? 😃 — I want to exercise
having Claude in the linux host just to prove how mature Claude's Linux support
is. — I want to try to transfer you memories folder, that sounds interesting.
— And I want to establish an ssh-key login between this machine and the linux
3090, for many reasons, but this will allow you also to issue commands there."

### §8.1 Track A — the SSH key login (done)

Run by the owner (passwords and keys are the owner's):

```bash
# On the 3090: an SSH server, started now and at every boot
sudo apt install -y openssh-server && sudo systemctl enable --now ssh
# On the Mac: a dedicated key for the 3090 (like ~/.ssh/hyperstack_2026 for the cloud), with a passphrase
ssh-keygen -t ed25519 -f ~/.ssh/zombie_radio_3090 -C "mac to 3090, zombie-radio"
# On the Mac: the key's public half onto the 3090 (asks the 3090's password once)
ssh-copy-id -i ~/.ssh/zombie_radio_3090.pub <user>@<the 3090's address>
# On the Mac: the key in the agent, its passphrase kept in the macOS Keychain (asked one last time)
ssh-add --apple-use-keychain ~/.ssh/zombie_radio_3090
```

The owner (verbatim), before the last step: "It asks to enter the passphrase
every time. I think the step of putting the key in the authority agent is
missing, no?" — yes. Then **an alias in the owner's `~/.ssh/config`** (the
owner's file, never read by the agent):

```
Host zr-3090
    HostName aorusX570.local
    User alfredo
    IdentityFile ~/.ssh/zombie_radio_3090
    IdentitiesOnly yes
    AddKeysToAgent yes
    UseKeychain yes
```

`ssh zr-3090 '<cmd>'` — no user, key or address typed, so **the address never
appears in a command or its output**; `aorusX570.local` (the machine's name on
the LAN) survives a new address from the router. The owner: "done, ssh zr-3090
works without passphrase." The same key is the one decision D3 needs for the
playbook.

**A wall, and the way around it.** From the agent's command shell (the Bash
tool), the 3090 was unreachable — `ping` and `ssh`, by name or by address,
inside and outside the sandbox: "No route to host" at once, though the name
resolved (IPv4 and IPv6) and the route was direct (`en0`, no gateway): the
signature of macOS's Local Network privacy check. **The owner (verbatim):**
"Claude already had the local network permission. We have been here before,
in another project, you probably have no memory off... Suffice to say, we gave
up trying to figure out the problem." **What works:** the app's **Terminal
panel** — the agent types `ssh zr-3090 '…'` into a tab of it and reads the
output: `aorusX570`, user `alfredo`. (Recorded in the agent's memory so no
session re-diagnoses it.)

**The 3090, as found over SSH (read-only):** hostname `aorusX570`; user
`alfredo`; **Ubuntu 22.04.5 LTS**; git 2.34.1; **the Claude desktop app**
installed (the `claude-desktop` package, 2.19675.0; no `claude` command on the
PATH, the app carries its own); `~/.claude` without `projects/`.

### §8.2 Track B — the repo on the 3090, and a session there (in progress)

**Done:** both repositories are public, so no credentials were needed;
`~/workspace/hackTNT_2026/zombie-radio-claude` cloned (the same relative place
as on the Mac), on `main` at `df01fb2` (#23), in step with GitHub. **This
document and the board are on #24, not yet merged:** after the merge, `git pull`
on the 3090 (or #24's branch checked out there).

**Next, the owner:** open a Code session in the Linux Claude app in
`~/workspace/hackTNT_2026/zombie-radio-claude` once, and close it — Claude Code
then creates its project folder for that path.

### §8.3 Track C — the memory folder copied (next)

Once that folder exists: list `~/.claude/projects/` on the 3090 for its exact
name (expected `-home-alfredo-workspace-hackTNT-2026-zombie-radio-claude`, by
the Mac's rule — every `/` and `_` becomes `-` — checked, not assumed); copy the
Mac's memory folder (its small markdown files: the index `MEMORY.md`, the
working agreements, the collaboration style, the path conventions, …) into it
with `scp`, through the Terminal panel, and list them there. **Caveats:** the
memory mentions Mac paths (`/Users/alfredo/…`); it is a snapshot — the two
copies drift apart from the day of the copy; the repo stays the shared memory
of record.

### §8.4 The Linux session's first prompt (to paste once the memory is copied)

```
We continue the Zombie-Radio work on the owner's Linux desktop (hostname aorusX570, Ubuntu 22.04.5, an RTX 3090). A Claude session on the owner's Mac has worked on this project for weeks; its memory folder was copied here (you may see it as recalled memories). Its paths mention the Mac (/Users/alfredo/...); here the repo is ~/workspace/hackTNT_2026/zombie-radio-claude. Re-orient before doing anything:

1. Read CLAUDE.md, then docs/README.md, then docs/discussions/2026-10-02-local-gpu-deployment-plan.md in full: it is our plan for the demo's goal 4 (deploying the stack to this 3090 with the Ansible playbook).
2. Run the plan's §5 read-only checks on this machine (the OS, the GPU and its driver, Docker and its NVIDIA runtime, the NVIDIA container toolkit, free disk, the SSH server, the ports 8080/8001/8002) and report each result, explained simply.
3. Then stop and wait for my go. Change nothing on this machine: no installs, no sudo, no services.

Standing rules: discussion-first; review before commit (I review in VS Code, no diffs in chat); never commit or push without my explicit order, and keep to one branch at a time (the Mac session also works on this repo); no AI attribution anywhere; my words verbatim in docs; never put any machine's IP address in a document or commit; never print or commit secrets; explain simply and explicatively; never invent data.
```

The prompt asks only for the read-only checks, and keeps the Linux session from
changing the machine or the repo until the owner's go. **Then** the two
sessions can cross-check: the Linux one from inside, the Mac one over
`ssh zr-3090`.

**Where the night stopped:** the context of the Mac session at 87 %; the owner
(verbatim): "Wait, the context window is at 87%, let's save this prompt you
created for the linux agent and any detail from this conversation that is
important in the new plan document, then commit and push to the PR."

### §8.5 Details for the execution, from the night's work (the agent's second pass)

The owner, before the compaction (verbatim): "Regarding the new plan document, make another deep pass trying to find
details in your context window about our discussion about the topic that would be lost in compaction that could serve
to enrich the document and better guide us during execution?" What the night taught, for §6's steps:

1. **The agent cannot run anything against the 3090 from its own command shell** (§8.1's wall). Every step that
   reaches the 3090 — `make ans-check-syntax` is hostless and fine, but `make ans-deploy ENV=local`, `make ssh-tunnel
   ENV=local`, `ssh`, `scp` — runs **in the owner's terminal, or in the app's Terminal panel** (the agent types it
   there with `run_in_terminal` and reads it with `read_terminal`). The deploys are the owner's anyway (§0.1 of the
   handoffs).
2. **The owner's `~/.ssh/config` alias applies only to the name `zr-3090`.** `ssh` reads the alias's options (user
   `alfredo`, the key, `UseKeychain`) when it is asked to dial **`zr-3090`**; dialling `aorusX570.local` or the
   address skips them. Two consequences for D1 and D3:
   - **wiring with the alias** — `make ans-set ENV=local IP=zr-3090` (the target takes any string; the sentinel is
     replaced by it) — would let Ansible's `ssh` find the user, the key and the Keychain through the owner's config,
     and keep any address out of the inventory file (even then, `hosts.yml` is wired and unwired like the cloud's);
   - **but the Makefile's `ssh-tunnel` forces its own user and key on the command line** — `-i
     ~/.ssh/hyperstack_2026` and `ubuntu@<host>` (read from `common_vars.yml`), plus `SSH_TOFU_OPTS` (`-o
     IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=~/.config/zombie-radio/known_hosts`)
     — and command-line options win over the config file: as it stands, the tunnel to the 3090 would offer the wrong
     key as the wrong user. **The fix stays D3's**: `ssh-tunnel` reads the user and key from the env's `99-<env>.yml`
     when set (and the same for the playbook's `ansible_user` / `ansible_ssh_private_key_file` in `99-local.yml`).
3. **Ansible's own SSH options apply to the 3090 too** (`common_vars.yml`): `IdentitiesOnly`, trust on first use
   (`accept-new`) into the project's own `~/.config/zombie-radio/known_hosts` (not `~/.ssh/known_hosts`), and only the
   declared key — so `99-local.yml` must declare `~/.ssh/zombie_radio_3090`; its passphrase comes from the macOS agent
   (Keychain), which `ssh` uses when run from the owner's shell.
4. **Sudo:** the cloud's `ubuntu` has passwordless sudo; the 3090's `alfredo` likely not — the deploy then needs
   `ANS_ARGS=-K` (Ansible asks the sudo password at the start), typed by the owner, never by the agent.
5. **One tunnel at a time:** the cloud's and the 3090's tunnels forward the same local ports (8080, 8001, 8002); close
   one before opening the other (the installed client points at those ports and needs no change).
6. **The 3090's facts so far** (§8.1): Ubuntu 22.04.5 LTS (the playbook's Ubuntu assert passes; 22.04 is one of the
   cloud images it was proven on); git 2.34.1; reachable on the LAN by name and key. **Still unknown — §5's checks:**
   the driver branch, Docker, the NVIDIA container toolkit, free disk, the ports, and whether the desktop session holds
   GPU memory; and the owner's answer on what else the 3090 is used for (D4).
7. **Two Claude sessions on one repository** (the Mac's and the 3090's): one branch at a time; the 3090's clone
   `git pull`s before work; neither commits without the owner's order (the §8.4 prompt says so).
8. **A release is not needed for goal 4** — the deployment lives in this repository (the inventory, `99-local.yml`,
   the Makefile); the app (`tz-0.6`) and the installed client stay as they are.
9. **The evidence for the talk** (D5): the deploy's log (`~/.config/zombie-radio/logs/`, as for the cloud), the second
   run's `changed=0`, `nvidia-smi` on the 3090 against the A6000's 14,477 MiB, and a short recording of a show running
   on it — and the story the owner wants to tell: the same playbook, from the same laptop, to a rented GPU or a GPU at
   home, with Claude working on both machines.

## §9. Addendum, 2026-10-02 night to 2026-10-03 — the memory copied, the 3090 checked, sudo decided; paused

### §9.1 Track B and Track C done (2026-10-02, night)

1. **#24 merged** (`6f02b45`), the plan with it; on the 3090, through the Terminal panel:
   `ssh -o BatchMode=yes zr-3090 'cd ~/workspace/hackTNT_2026/zombie-radio-claude && git pull -q && git status -sb && git log --oneline -1'`
   — on `main` at `6f02b45`, in step with GitHub.
2. **The owner opened a Code session** in the Linux Claude app in that folder ("done, opened a Code session on the
   3090"). Claude Code created **`~/.claude/projects/-home-alfredo-workspace-hackTNT-2026-zombie-radio-claude/`** —
   the name §8.3 expected by the Mac's rule (every `/` and `_` becomes `-`), now checked — holding the session's
   `.jsonl` and an **empty `memory/` folder** (so the copy overwrote nothing).
3. **The memory copied** (via the Terminal panel), then a checksum of every file on both sides:

   ```bash
   # The Mac's memory files into the 3090's empty memory folder
   scp -q -o BatchMode=yes ~/.claude/projects/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/memory/*.md zr-3090:.claude/projects/-home-alfredo-workspace-hackTNT-2026-zombie-radio-claude/memory/
   # A checksum of each file on the 3090, then on the Mac, to compare
   ssh -o BatchMode=yes zr-3090 'cd ~/.claude/projects/-home-alfredo-workspace-hackTNT-2026-zombie-radio-claude/memory && sha256sum *.md'
   (cd ~/.claude/projects/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/memory && shasum -a 256 *.md)
   ```

   **All 11 files identical** (the index `MEMORY.md` and ten memories; the two lists differ only in their order — Linux
   and macOS sort names differently). The Mac's `pending-doc-updates.md` had been deleted just before, its edits merged
   with #24, so it was not copied.
4. **A new session, not the first one:** a session reads `MEMORY.md` when it starts, and the owner's first session
   started before the copy — so the owner started **a new Code session** and pasted §8.4's prompt into it.

### §9.2 The §5 checks — all passed

The owner (verbatim): "done, the Linux session reported the checks. All positive." The Mac session then ran the same
checks over `ssh zr-3090` (read-only; the GPU's id left out here):

```bash
# §5's seven checks in one call, plus whether sudo asks for a password (-n: never prompt) and the account's groups
ssh -o BatchMode=yes zr-3090 'lsb_release -ds; nvidia-smi --query-gpu=name,driver_version,memory.total,memory.used --format=csv; docker --version; docker info 2>/dev/null | grep -i -E "runtimes|nvidia"; nvidia-ctk --version; df -h /home; systemctl is-active ssh; ss -ltn | grep -E ":(8080|8001|8002)\b" || echo "ports free"; sudo -n true 2>&1 | head -1; id -nG'
```

| # | Check | The result (2026-10-02, night) | The playbook's view |
|---|---|---|---|
| 1 | The OS | Ubuntu 22.04.5 LTS | passes the Ubuntu assert; 22.04 is a release the cloud images were proven on |
| 2 | The GPU, the driver, the memory | NVIDIA GeForce RTX 3090, driver **580.178.04**, 24,576 MiB in total, **491 MiB in use** | the base role asserts the driver can run the pinned CUDA generation (its CUDA major ≥ the pin's 12); R580 is newer than the R570 proven on the A6000; about 24 GB free for the stack's 14,477 MiB |
| 3 | Docker and its NVIDIA runtime | Docker 29.1.3 (`29.1.3-0ubuntu3~22.04.2`); `Runtimes: io.containerd.runc.v2 nvidia runc`; CDI devices `nvidia.com/gpu=0`, `=all` | the base role only asserts the `docker` command exists, and enables the Docker service (already enabled) |
| 4 | The NVIDIA container toolkit | `NVIDIA Container Toolkit CLI version 1.20.1` | asserted present (`nvidia-ctk`) |
| 5 | Free disk | `/` (the root volume, `/home` on it): 912 G, 396 G free | about 11 GB of models, plus the images and the voice's environment |
| 6 | The SSH server | `active` | needed for D1 (b), already used by `ssh zr-3090` |
| 7 | The ports 8080, 8001, 8002 | `ports free` | nothing to move |
| + | sudo | `sudo: a password is required` | §9.3 |

**Two things noticed in passing:**
- **Docker is Ubuntu's own build** (`docker.io`), not Docker's (`docker-ce`). The playbook does not care which (it
  asserts the command, and runs the containers with the `community.docker` modules); recorded in case anything odd
  shows up.
- **The owner's account is in the groups `ollama` and `ollama_access`** — Ollama seems installed. Idle, it holds no
  GPU memory; if it loads a model while a show runs, it competes for the 3090's 24 GB. **Open question for D4:** does
  Ollama (or anything else on the GPU) run while a show would?

### §9.3 Sudo — the password typed at the keyboard (decided)

The owner (verbatim): "The only thing that I saw in passing could be a problem is that my account in that machine does
ask for password for sudo... I know that is workable in ansible if I am willing to provide my sudo password to the
playbook... I'd be more happy providing  my password via safe keyboard input than writing it in a vault (I know ansible
has a way to ask for passwords interactively)"

**Decided: Ansible's `-K` (`--ask-become-pass`).** The playbook runs with `become: true` (`site.yml`), so sudo is needed
on the 3090; with `-K` Ansible asks `BECOME password:` once at the start, without echoing what is typed, and keeps it in
memory for that run only — nothing in a file or a vault. **The Makefile already passes `ANS_ARGS` through** (the
`ans-deploy` target), so no code change:

```bash
# The deploy to the 3090, asking the sudo password at the keyboard (run by the owner, in the owner's own terminal)
make ans-deploy ENV=local ANS_ARGS=-K
```

The owner types it, in the owner's own terminal (the prompt needs the keyboard); the agent never types it (§8.5 point
4, now confirmed). **Not chosen:** a vault (the password stored, which the owner does not want); a sudoers rule without
a password (it would weaken the machine for good). What needs sudo: the base packages (`apt`), the Docker service, the
voice's systemd unit, the containers.

### §9.4 D4 — the services not started at boot (the owner's lean; the effort estimated)

The owner (verbatim, 2026-10-02, night): "Because this machine is a desktop computer that I use for other stuff too, I
do not want to keep the services starting automatically on boot. What is your estimation of the effort to change
that?"

**What starts them at boot today** (three places, all in the playbook):

| The service | How it comes back at boot | Where |
|---|---|---|
| llama.cpp (`llama`) | a Docker container with `restart_policy: unless-stopped` — Docker brings it back at every boot | `deploy/ansible/roles/llama/tasks/main.yml:19` |
| Whisper (`whisper`) | the same | `deploy/ansible/roles/stt_engine/tasks/main.yml:19` |
| the voice (`tts-<name>`) | a systemd unit, `enabled: true` | `deploy/ansible/roles/tts_engine/tasks/main.yml:49` |

**The change (the agent's shape, not yet built or approved):**
1. **One switch**, e.g. `zr_start_at_boot` — `true` by default (the cloud box unchanged), `false` in the 3090's
   `99-local.yml`.
2. **Three lines follow it:** the containers' restart policy `no` instead of `unless-stopped`; the voice's unit
   `enabled: false`. A deploy still **starts** all three (a show can run right after); after a reboot they stay off.
3. **A way to start and stop them by hand:** two Makefile targets (`ans-start`, `ans-stop`) or a runbook recipe;
   starting the voice needs sudo, so `-K` again; llama reloads its model on start (about 90 s).
4. **The proof:** a deploy, a second run at `changed=0`, **a reboot of the 3090** — nothing running, the GPU free —
   then a start by hand, the three ports answering.

Docker itself stays enabled at boot (it already is on the 3090); with no container running it holds no GPU memory.
**The estimate:** small — about an hour or two of the agent's work, plus one reboot by the owner. It belongs on the
goal-4 branch with the inventory (§6 step 3).

### §9.5 Paused (2026-10-03)

The owner (verbatim, 2026-10-03): "We are going to pause for a time "Automated deployment to a local GPU (the 3090)"...
I am not at home now, so the only way to execute the AI heavy parts would be to awake the VM, which is ok..."

- **Resumes when the owner is home again** (the owner's choice, 2026-10-03); goal 4 stays a demo goal.
- **Where it resumes:** decisions D1-D5 (§4) — D4 with the owner's lean above, the Ollama question with it — then §6
  from step 2 (step 1, the facts, is done).
- **Meanwhile** the board's items that need a box — Task 10.1 (the filter test) and Task 7 (the video) — use the cloud
  box, woken for them (the owner: "which is ok"); the 3090 cannot stand in while the owner is away from it.
- **Left as is on the 3090:** the repo at `6f02b45`; the copied memory (a snapshot of 2026-10-02 — it drifts from the
  Mac's from now on); the Code session; the SSH server, enabled. Nothing deployed, nothing installed by the agent.

## §10. Addendum, 2026-10-06 — resumed from the 3090: D1, D3 and D4 decided, the branch `alfre2v/linux-3090`

### §10.1 A Claude session on the 3090, and what it saw

The session §8.4 prepared started on the 3090 (2026-10-02, night) and re-ran §5's checks from inside, read-only: the
same results as §9.2 (driver 580.178.04; 557 MiB of the GPU in use, all of it the desktop: Xorg, gnome-shell, Chrome,
the Claude app; the CUDA version the driver reports, which the base role compares with the pin's major 12: 13.0).
**New, from inside:**

- **Ollama is a system service, active and enabled at boot** (`systemctl is-active ollama`, `is-enabled`; §9.2 had
  only the account's groups). Idle, it held no GPU memory; a loaded model would compete with the stack's ~14.5 GB.
- **Two containers already run:** `mongodb` (27017) and `portainer` (8000 and 9443), both open on the network. Neither
  takes the stack's ports; **but 8000 is the client's port** (`uvicorn … --port 8000`), which matters for Task 11.2.
- **The never-commit hook was not armed on the 3090's clone** (`git config core.hooksPath` empty): `make install`, the
  only thing that arms it, had never run there (§10.6).

On 2026-10-05 the owner resumed goal 4 ("I have merged some PRs in the repo since you last look at it, but nothing
that changes this task"); the work below is of 2026-10-06.

### §10.2 D1 — both: `local` as built, and a new `lan`

The agent's summary of 2026-10-05 offered D1 (b) as if it worked today. **The owner (verbatim):** "It cannot run from
the laptop in our current inventory, the local inventory has `ansible_host: localhost`, so if you try running from
the laptop is not going to end well. I think you have not read our ansible inventories, have you?" — it had not: the
summary came from §2's description; §4's row for (b) names the inventory change it needs, and the summary dropped it.
`ansible_connection: local` makes Ansible run every task on the machine it runs on: from the laptop, the playbook would
target the Mac.

**The owner (verbatim):** "Now, on the other hand, we could easily copy the cloud inventory, change almost nothing,
and call it localnetwork or something like that, and then we could pretty much do it remote from the laptop." Asked to
build one or both: "(2) build both." The name: "(3) let's do `lan`. It's shorter."

**Decided:** two environments for the one box, both converging it to the same state.
- **`local`** — as built: Ansible on the 3090 itself, no SSH.
- **`lan`** — a copy of `cloud`: the sentinel `REPLACE_ME_box_ip  # NEVER_COMMIT`, wired with
  `make ans-set ENV=lan IP=zr-3090` (the SSH alias, so no address ever enters the file; §8.5 point 2). The story of
  §8.5 point 9: the same playbook, from the same laptop, to a rented GPU or a GPU at home.

Nothing in the Makefile or the playbook names the environments: `require_ansible_env` accepts any folder under
`inventories/`, and the preflight requires only `zr_environment` to equal the folder's name.

### §10.3 D3 — the user and the key

Both 3090 environments set `ansible_user: alfredo` and `zr_service_user: alfredo` in their `99-<env>.yml`; `lan` also
sets `ansible_ssh_private_key_file: "~/.ssh/zombie_radio_3090"`. **`make ssh-tunnel` now reads the user and key from
the env's `99-<env>.yml` first, then `common_vars.yml`** (one `awk` over both files, the first match wins; §8.5
point 2's fix). The tunnel works after a `local` deploy as well: it needs only the laptop's wired `lan` inventory.

### §10.4 D4 — nothing starts at boot; start and stop by hand, in every environment

**The owner (verbatim):** "On D4 "Should the services start at every boot?"...  You are right. I do not want the
starting on a new restart."

**Built as §9.4 shaped it:** a switch `zr_start_at_boot` — `true` in `common_vars.yml` (the cloud unchanged), `false`
in `99-local.yml` and `99-lan.yml`. The containers' restart policy follows it (`unless-stopped` or `no`), and so does
the voice unit's `enabled`. A deploy still starts all three.

**Starting and stopping by hand** — offered as `make` targets or a runbook recipe; **the owner (verbatim):** "(i) make
targets for start/stop. and why only make them work for `ENV=local|lan`? I may want to also stop and start the
services in the cloud environment. Any impediment to making this start/stop support cloud too?" — none: the new
playbook `services.yml` reads whatever inventory `ENV` names. `make ans-start ENV=<env>` starts the three services and
waits until each answers; `make ans-stop ENV=<env>` stops them; the 3090's need `ANS_ARGS=-K`. On the cloud, a stop
does not change the next boot: the voice comes back (its unit enabled), the containers stay stopped (Docker remembers a
manual stop); and stopped services still bill.

### §10.5 Every download in one folder

**Found:** the owner's home on the 3090 already holds **a 43 GB Hugging Face cache** (`~/.cache/huggingface`, mode
`0775`, 19 models). By default the Whisper role points its cache there: it would set the folder to `0755` and mount it
into a container that runs as root, leaving root-owned files in the owner's personal cache; the voice's checkpoint
(about 5 GB) lands there too (`docs/runbooks/box-inspection.md`: "TTS checkpoint + whisper model, shared tree").

Offered: (A) llama's models and Whisper's cache into a project folder; (B) the same, plus `HF_HOME` for the voice's
unit. **The owner (verbatim):** "(B) for the data: I want every downloaded model to sits in one folder." Then, of the
voice's Python environment (`~/faster_qwen3tts`, several GB): "I want fix (1) "The voice's environment
(~/faster_qwen3tts)". The pip cache does not worry me. That's ok."

**Built:** `zr_data_dir: ~/zombie-radio-data` in both 3090 environments, holding `models/` (llama), `whisper-cache/`,
`voice-cache/` (the voice's `HF_HOME`) and `faster_qwen3tts/` (the voice's environment and tts-serve). Two new project
settings, each defaulting to the cloud's current value: `zr_tts_hf_home` (empty: the user's default) and `zr_tts_root`.
Folders the file module creates on the way belong to the same owner (read in Ansible's `file` module). **Outside the
folder, by design:** the two Docker images (Docker keeps every image of the machine in one store, `/var/lib/docker`;
moving it is a machine-wide Docker setting the playbook never touches), the voice's systemd unit, pip's cache, and two
apt packages from the base role (`python3-venv`, `sox`, neither on the 3090 before). The removal recipe:
`docs/runbooks/home-gpu-3090.md`. **To check at the first deploy:** that the voice's checkpoint lands in
`voice-cache/` (believed, from `HF_HOME`; not yet seen).

### §10.6 The Makefile on Linux

`make ans-set` used `sed -i ''`, macOS's form; Linux's sed takes `''` as the script and the substitution as a file
name. **Measured** on the 3090 (GNU sed 4.8, on a scratch copy): `sed: can't read s/REPLACE_ME_box_ip/zr-3090/: No such
file or directory`, exit 2, the file unchanged. **The owner (verbatim):** "Really? So the agent coded a mac dependent
syntax into the Makefile ? Wow." The line came with #5 (`8aa9ebf`, 2026-09-21), when the Makefile only ever ran on the
Mac; a Mac session's handoff lists `sed -i ''` among its shell habits (session handoff 6) — a habit of the agent's
shell that reached shared code, never run on Linux. **Fixed:** `sed -i.bak … && rm -f ….bak || exit 2` (works with
both seds; a failed substitution now stops instead of printing "wired"). Tested on the 3090: wired, refused a second
wiring, unwired. The rest of the Makefile was read for macOS-only commands: none found. `ans-unset` (`git restore`)
was never affected.

`make ans-check-syntax` now also parses `services.yml`. **The owner (verbatim):** "Makefile lines 81 and 82. WTF is
that?" — the agent had added the second command without proposing it, and offered to revert it or fold it into one
line; the owner: "leave it as it is. On second thought is not so bad."

### §10.7 The 3090 as a control node — run by the owner

**The owner (verbatim):** "(4) Yes, but let me issue the commands, guide me one by one, I want to run them in my
console. (Later I will transfer this duties to you but for the first installs I wan to get a feel of it)" — on the
3090, in the owner's terminal: `make install` (the project's Ansible in `.venv`, `ansible [core 2.21.4]`; the hook
armed, `core.hooksPath` `.githooks`), then `make ans-deps` (`community.docker` 5.3.0, inside the repo). The owner:
"done, collections installed".

### §10.8 The branch

**The owner (verbatim):** "Ok, let's open a branch to do fix any Makefile portability issue and also to do anything we
need to get this thing running in linux." Its scope: "(1) Keep this branch to the deploy and do the client next, so
each PR stays reviewable." — `alfre2v/linux-3090`, from `main` at `5734dbc`; Task 11.2 (the client on Linux) gets its
own branch. And: "Green light to any runbook edits that you can do that explain the steps to operate the project."

**What it holds:** the Makefile (the `sed` fix, the tunnel reading the env's overrides, `ans-start` / `ans-stop`, the
syntax check of both playbooks); `services.yml`; the boot switch and the voice's two path settings in the three
roles and `common_vars.yml`; `inventories/lan/`; `99-local.yml`; a new runbook, `docs/runbooks/home-gpu-3090.md`;
updates to `service-restart-sequence.md`, `box-inspection.md` and `deploy/ansible/README.md`.

**Verified on the 3090 (no deploy):** the syntax parse of both playbooks for `cloud`, `local` and `lan`; `ansible-lint`
clean on the `production` profile; **the cloud's voice unit renders byte-identical to before** (so the next cloud
deploy does not restart the voice); each environment's resolved paths and users (the cloud's unchanged).

### §10.9 Next

D2 (the tunnel for the laptop's client; none for a client on the 3090) and D5 (proven at home) stay the agent's
leans; not yet ruled. Then §6 from step 5, on the owner's go:

1. **The first deploy, `local`**, by the owner on the 3090: `make ans-deploy ENV=local ANS_ARGS=-K`. **No `--check`
   dry run first:** in check mode the containers are not started, but the roles' health waits run anyway
   (`check_mode: false`): llama's would poll a server that never started, 60 × 15 s, and fail.
2. A second run at `changed=0`.
3. **D4's proof:** a reboot of the 3090 — nothing running, the GPU free — then `make ans-start ENV=local
   ANS_ARGS=-K`, the three ports answering.
4. Measure (§6 step 7); where the voice's checkpoint landed (§10.5).
5. **`lan` from the laptop**: `make ans-set ENV=lan IP=zr-3090`, `make ans-deploy ENV=lan ANS_ARGS=-K` (expected
   `changed=0`: the same box, the same settings), the tunnel, a show — the evidence for the talk; the slide "The 3090
   at home" updated.

### §10.10 The first deploy (2026-10-06, night): three failures, then `changed=16` and `changed=0`

Run by the owner on the 3090, `make ans-deploy ENV=local ANS_ARGS=-K`; the logs in `~/.config/zombie-radio/logs/`.

**A dry run first? No.** §10.9 had warned that `--check` stalls on a never-deployed box. **The owner (verbatim):** "I
think we had a similar problem before and we solved by adding  `check_mode: false` to the tasks..." — the fix of
2026-09-24 (`b9e4d18`, #11): under `--check` Ansible skips `command` and `shell` tasks, and `uri` has no check mode at
all (`check_mode: support: none`), so six read-only tasks were marked `check_mode: false` and the dry run passed — on
the A6000, where the services were already running. On a never-deployed box the same marking makes the health waits
poll servers that a dry run never started. A fix for fresh boxes (skip a health wait when a dry run reports it would
have started the service) was offered; the owner went on to the deploy.

**Failure 1 — the apt cache (01:20).** The base role's package step failed after five retries with an empty reason.
**The owner (verbatim):** "I tried doing the install, it failed in the apt cache, I do not understand why [...] Maybe
I entered the wrong password for become?" — no: the facts had already been gathered with sudo. An `apt-get update` run
by the agent into a scratch folder (no sudo, the system's lists untouched) showed the cause: **HashiCorp's apt source**
(`/etc/apt/sources.list.d/hashicorp.list`, for Vagrant) is now signed with a key, `FC9CA96ACA026560`, that the
machine's keyring for it (`AA16FCBCA621E701`, 2023-2028) did not hold — `NO_PUBKEY`, "The repository ... is not
signed". A machine problem, not the project's: any `apt-get update` failed. The owner refreshed the keyring from
HashiCorp after checking that it carried the new key: "done, key refreshed, apt update is clean."

**Failure 2 — no `requests` (01:27).** The llama container's task failed: "Failed to import the required Python
library (requests) on aorusX570's Python /home/alfredo/workspace/hackTNT_2026/zombie-radio-claude/.venv/bin/python3.12".
**The owner (verbatim):** "How is it possible that the request library is not installed here, but it did not fail on
the cloud?" — over SSH, Ansible's interpreter discovery searches **the box's** PATH (the cloud's Ubuntu: only its
system Python, which ships `requests`); with `ansible_connection: local` it inherits **`make`'s** PATH, where `uv run`
puts the project's `.venv/bin` first, and the discovery list (`python3.14`, `python3.13`, `python3.12`, …) finds the
control-side Python (Ansible and the linter, no `requests`). The base role had passed because the `apt` module
switches to the system Python by itself. **Fixed:** `ansible_python_interpreter: /usr/bin/python3` in `99-local.yml`
(measured: `requests` 2.25.1 there); `lan` goes over SSH and needs nothing.

**Failure 3 — ghcr.io "denied" (01:30).** Pulling `ghcr.io/ggml-org/llama.cpp:server-cuda-b11096`: `403 Forbidden`,
"denied: denied". The tag exists — an anonymous request for its manifest returned `200` — so the registry refused the
credentials sent with the pull: the playbook pulls as root, and **root's Docker config held a ghcr.io login** (the
owner checked it with sudo, registry names only: "Yes, it was that."), which GitHub rejected rather than fall back to
an anonymous pull. Offered: (a) `sudo docker logout ghcr.io`, or (b) the image pre-pulled as the owner's user (no
logins; the role's `pull: missing` then skips the pull). The owner: "ghcr.io error fixed with: (a) the logout."

**The deploy (01:33 to 01:41, about 8½ minutes).** The owner: "It seems it worked. `changed=16`". Checked by the agent
on the 3090, read-only:

| | Measured |
|---|---|
| The services | llama `Up (healthy)`, Whisper `Up`, the voice unit `active`; health `200` on 8080, 8001, 8002 |
| Bound to | `127.0.0.1` only (8080, 8001, 8002) |
| The context | `n_ctx 32768`, one slot |
| At boot (D4) | both containers `restart=no`; the voice unit `disabled`; Docker `enabled` |
| The GPU | llama-server 6,966 MiB · the voice 4,736 MiB · Whisper 896 MiB = **12,598 MiB**; the card 12,958 of 24,576 MiB with the desktop. (The A6000's 14,477 MiB had a voice after a day of shows, 6,530 MiB: the voice grows as it caches the clips it clones from.) |
| `~/zombie-radio-data` | `faster_qwen3tts` 7.6 GB · `models` 6.1 GB · `voice-cache` 4.3 GB (`Qwen3-TTS-12Hz-1.7B-Base`: **`HF_HOME` worked**, §10.5) · `whisper-cache` 464 MB (`faster-whisper-small`) |
| Outside it | the images: llama.cpp 4.35 GB, Whisper 5.08 GB (Docker's store) |
| The owner's own HF cache | untouched: mode `drwxrwxr-x`, last modified 2026-06-21, the same 20 entries; no `~/models`, no `~/faster_qwen3tts` |

**The converge invariant (01:44, 18 seconds).** The owner: "second run done, changed=0."

**The reboot test, postponed.** The owner (verbatim): "I won't reboot now, let's postpone this check, but I don't
expect it to fail." Still to prove: after a reboot nothing of ours runs, and `make ans-start ENV=local ANS_ARGS=-K`
brings the three back (its first real run).

### §10.11 Next

1. **`lan` from the laptop** (the Mac session): `make ans-set ENV=lan IP=zr-3090`, `make ans-deploy ENV=lan
   ANS_ARGS=-K` (expected `changed=0`, the same box and settings), the tunnel, **a show against the 3090** — the
   evidence for the talk; the slide "The 3090 at home" updated.
2. **The reboot test** and `ans-start`'s first real run, when the owner reboots.
3. **Task 11.2, the client on Linux**, on its own branch; Portainer already holds the client's port 8000 (§10.1).
4. **D2 and D5** to rule.

### §10.12 D2 and D5 ruled (2026-10-06)

Put to the owner again, each with the agent's lean (§4): **D2**, how the laptop's client reaches the 3090's services —
the SSH tunnel, as with the cloud (built: `make ssh-tunnel ENV=lan`; the client's settings unchanged; nothing listens
on the home network), or the services opened on the home network (`zr_bind_host` overridden: the client's settings
would carry the 3090's address, and every device on the network could reach services that have no login). **D5**, what
"goal 4 met" means — (i) proven at home: a deploy from zero, a second run at `changed=0`, a show from the laptop
against the 3090, recorded as evidence for the talk; or (ii) used live at the venue, reaching home over the internet
(port forwarding or a VPN; two networks on demo day).

**The owner (verbatim):** "tunnel and (i), record it in the plan"

**Decided:**
- **D2 — the tunnel.** No change to the deployment or the client. A client on the 3090 itself (Task 11.2) needs no
  tunnel: its `localhost` ports are the services' own.
- **D5 — (i), proven at home.** Done so far: the deploy from zero (`changed=16`) and the second run (`changed=0`),
  §10.10. **Left for goal 4:** `lan` from the laptop, the tunnel, a show against the 3090, and its recording — then the
  slide "The 3090 at home" says so. The demo itself runs on the cloud box.
