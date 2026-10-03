# Deploying to the local 3090 — the scouting, the decisions, and the plan (the demo's goal 4)

**Date:** 2026-10-02 · **Arc:** MVP prototype · **Branch:**
`alfre2v/todo-2026-10-02`
**Type:** discussion — the plan document for the demo's goal 4 (automated
deployment to a local GPU, the owner's 3090): what is already built, what the
playbook requires and does to a machine, the decisions to make, the facts to
gather, and an executable plan; meant to guide the task when it opens.
**Status:** OPEN — scouting done (2026-10-02, evening), nothing built; the
owner's facts (§5) and decisions (§4) next; the task not opened yet.
**Trigger to revisit:** the owner's facts from the 3090 (§5), or the task
opening.

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
