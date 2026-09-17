# Ansible deployment — the converged shape

**Date:** 2026-09-17 · **Arc:** MVP prototype (Task 1,
deliverable D1)
**Type:** design agreement — the patterns the deployment
machinery is built to, persisted so future sessions can re-ground
on the AGREED shape (the code and `deploy/ansible/README.md`
carry current usage; THIS doc carries the patterns and their
rationale as ratified).
**Status:** CONVERGED 2026-09-17 after a multi-round shape
discussion (owner + agent, both directions of pushback).
Companion doc: [discussion 2026-09-17] docker networking &
host mode (the connectivity analysis this shape depends on).

## 1. Directory layout (ratified)

Everything Ansible lives under **`deploy/ansible/`** — the extra
`ansible` level is a deliberate reservation: future deployment
artifacts that are NOT Ansible (e.g. a monitoring container's
`deploy/my-monitor/compose.yaml`) get sibling directories instead
of polluting one flat tree. The Makefile lives at the REPO TOP
LEVEL, not under deploy/.

```
Makefile                          # top level: the "what can I run" entrypoint
deploy/
└── ansible/
    ├── README.md                 # usage + current structure (living)
    ├── ansible.cfg               # no hardcoded inventory (Makefile passes -i);
    │                             #   sets collections_path to ./collections
    ├── site.yml                  # THE deployment play: base → llama → tts_engine → whisper
    │                             # (top level also hosts future standalone playbooks —
    │                             #  see "Reserved playbook slots" below)
    ├── collections/
    │   ├── requirements.yml      # collection deps (community.docker)
    │   └── ansible_collections/  # download target — GITIGNORED
    ├── inventories/
    │   ├── common_vars.yml       # the shared truth — ONE real file
    │   ├── cloud/
    │   │   ├── hosts.yml         # COMMITTED (owner ruling 2026-09-17: box IPs
    │   │   │                     #   are not secrets; real secrets → vault pattern)
    │   │   └── group_vars/all/
    │   │       ├── 00-common.yml → ../../../common_vars.yml   (SYMLINK)
    │   │       └── 99-cloud.yml  # real file: env-specific overrides
    │   └── local/
    │       ├── hosts.yml         # localhost, ansible_connection=local
    │       └── group_vars/all/
    │           ├── 00-common.yml → symlink to the same common_vars.yml
    │           └── 99-local.yml
    └── roles/
        ├── base/
        ├── llama/
        ├── tts_engine/
        └── whisper/
```

**Collections convention (owner, 2026-09-17):** dependencies are
declared in `collections/requirements.yml`; the collections
themselves install into `collections/ansible_collections/`
(gitignored) — the project is self-contained, nothing lands in
the user's global collections. `ansible.cfg` points
`collections_path` there.

**Reserved playbook slots (owner, 2026-09-17):** standalone
playbooks that run OUTSIDE the main role-driven deployment may
appear at the `deploy/ansible/` top level as needed. Named
example uses (none built in v1): `bootstrap.yml` (provider-SDK VM
creation) · `harden-ssh.yml` (SSH hardening for a fresh VM) ·
`lab.yml` (a local multipass-VM test environment — noting those
VMs have no GPU, so of limited use here) · `teardown-cloud.yml`
(bootstrap's opposite) · `validate.yml` (config health: syntax,
vault decryption against the current key, any post-change
checks).

## 2. The inventory pattern (owner's, adopted over the agent's)

**Environments, not groups.** Cloud and local are separate
inventory DIRECTORIES because they are *environments* — different
providers, different failure modes, different variable sets,
never targeted together. The safety property this buys: you
cannot accidentally deploy to both. The agent's original
one-file/two-groups proposal was withdrawn: it modeled them as a
fleet, which they are not.

**Shared truth lives at `inventories/common_vars.yml`** — one
real file, symlinked into every environment as
`group_vars/all/00-common.yml`. The agent's alternative (shared
truth in role defaults) was rejected: the owner's pattern keeps
ALL configuration truth in one visible tree under `inventories/`;
role defaults revert to their proper job — harmless fallbacks.

**Numeric prefixes are the precedence dial.** Ansible loads
`group_vars/all/*` lexicographically, later overriding earlier:

- `00-common.yml` — the symlinked shared truth
- `10-vault.yml` — RESERVED: the encrypted vault (when secrets
  ever exist; none do in v1)
- `20-vault-vars.yml` — RESERVED: plain-name → `vault_*` mapping,
  so the vault's *contents* are greppable without decrypting
- `99-<env>.yml` — env-specific overrides, always winning

**Hosts files are YAML** (`hosts.yml`), static — no dynamic
inventory script needed for this project (the slot exists at that
level if a dynamic environment ever appears). Both environments
define the same group name, **`gpu`**, which is what `site.yml`
targets — one playbook, identical execution, `-i` picks the
world:

```
ansible-playbook -i inventories/cloud site.yml
ansible-playbook -i inventories/local site.yml
```

Gitignore ruling (owner, 2026-09-17, reversing the agent's
proposal): **hosts files are COMMITTED, both environments** — a
box IP accidentally committed is acceptable; anything genuinely
secret goes through the vault pattern instead. The only
gitignored deployment path is `collections/ansible_collections/`
(downloaded artifacts). Until the first provision, the cloud
`hosts.yml` carries an un-pasteable placeholder
(`<PASTE-BOX-IP-HERE>`, per the placeholder discipline).

## 3. Role anatomy (owner's convention)

Standard, full role structure per role: `defaults/ files/ tasks/
templates/ handlers/ vars/` as needed. One role per service
(owner ruling 2026-09-17): **`base` · `llama` · `tts_engine` ·
`whisper`**.

**Engine dispatch in `tts_engine`:** `tasks/main.yml` handles
what is genuinely common (venv creation, tts-serve clone, systemd
unit, health check) and dispatches the bespoke install with
`include_tasks: tts_engine_{{ tts_engine }}.yml` — the per-engine
task files live FLAT in `tasks/` (no subdirectory). v1 ships
exactly one: `tts_engine_faster_qwen3tts.yml` (encoding the
proven potholes: numpy before the engine package,
`transformers==5.15.1` pin). A future engine = one new task file
(+ its vars), zero conditionals rotting meanwhile. Rationale for
task-files over a pure-variables surface: engine installs are
bespoke in SHAPE, not just in values (LuxTTS needs a git clone
with `--no-deps` plus a codec dep — not the same steps with
different strings).

## 4. Supervision (decided: option a)

- `llama` and `whisper`: **detached Docker containers with
  `--restart unless-stopped`** — Docker is the supervisor. With
  the Docker service enabled, they also rise on VM reboot.
- `tts-serve` engine (bare venv process): **systemd unit**
  managed by the `tts_engine` role; enabled, so it too survives
  reboot and crashes unattended.
- **Zero tmux anywhere in the deployment** (owner: hard no).
  tmux remains a human convenience when SSHing in; the deployment
  neither creates, assumes, nor touches it.
- Logs: `docker logs -f llama` / `journalctl -u tts-serve -f`.
- Uniform property, all three services: survive SSH disconnects,
  crashes, and reboots without an operator.
- **Known deviation from the sealed recipe:** the canonical v3
  llama command uses `--rm`, which is mutually exclusive with
  `--restart` — the playbook drops `--rm`, names the containers,
  and lets the restart policy own the lifecycle.

## 5. Rejected alternatives (recorded so they aren't re-litigated)

- **tmux-driven services via Ansible** — hard no (not a
  supervisor, not idempotent, fragile to verify).
- **docker-compose, including the owner's "static compose files +
  env-var-driven, merged with `-f`, Ansible only edits env
  files" pattern from his private project** — a genuinely good
  pattern (compose files stay runnable without Ansible; env file
  as the single dynamic surface), but its preconditions are
  absent here: we have two containers with short, battle-tested
  `docker run` commands, `--network host`, no inter-service
  traffic, one operator, a 3-day timebox. DISCARDED for v1 as
  overkill, by agreement. **Flip trigger:** a future arc adds
  services with dependency ordering/profiles → revisit, with the
  private project's pattern as the template.
- **Cribbing from the owner's private Ansible repo** — ruled
  "nothing": this project is simple enough; the one idea imported
  is the top-level Makefile convention.

## 6. The Makefile convention

Variable-driven targets: **`make deploy ENV=cloud`**,
`make deploy ENV=local`, `make check`, `make ssh-tunnel`. Future
secret-lifecycle targets (create/rotate keys, verify vault
decryption) reserved but unbuilt (no secrets in v1). The
Makefile's stated purpose (owner): automate everything runnable
in the project so nothing must be remembered — it doubles as the
project's "what can I run" documentation.

## 7. Scope fence for v1 (from [discussion 2026-09-17] rulings + this round)

- Timebox: 3 days from first playbook commit.
- Starts at "SSH-able **Ubuntu** box exists" — VM provisioning
  stays in the provider console; Ubuntu-everywhere is a named
  portability bet.
- In: idempotent re-runs · post-role health checks (the curl
  gates as Ansible tasks) · lazy model downloads with pinned
  cache paths (`LLAMA_CACHE`, HF cache mount).
- Out: vault plumbing (no secrets exist) · Molecule ·
  multi-engine simultaneous deploys (§7.2's two-engine step runs
  the role twice with different vars when its time comes) · the
  Mac laptop client (manual; not an Ansible target) · installing
  Docker itself (the pinned cloud image ships it; see final-sweep
  decisions below).

## 8. Final-sweep decisions (the nuances caught at convergence, 2026-09-17)

- **Docker presence is asserted, not installed**: the `base` role
  verifies docker + nvidia-container-toolkit and fails with a
  clear message if absent. The pinned R570 image ships both; the
  local 3090 box is the owner's to prepare. Installing Docker is
  out of v1.
- **systemd unit is a SYSTEM unit** (`/etc/systemd/system/
  tts-serve.service`, `User=ubuntu`), not a `--user` unit — no
  lingering complexity; we have sudo.
- **Health checks must tolerate cold starts**: the llama
  container downloads ~6 GB on FIRST deploy and takes ~90 s to
  load on every start ( `/health` reports loading); the TTS
  engine downloads checkpoints on first launch. Health-check
  tasks use `retries`/`delay` sized for the cold path, with the
  first-deploy download window called out in the README.
- **Image tags float in v1, pinned at show-freeze**:
  `llama.cpp:server-cuda` and `whisper-fastapi:latest` are
  floating tags (freshness mattered for `nemotron_h` support).
  Conscious choice: float during the experiment-heavy arc;
  **demo-week rule: pin both images by digest when the show
  freezes** (recorded here so it fires later).
- **The tunnel's box IP has ONE source of truth**: the cloud
  inventory's `hosts.yml`. `make ssh-tunnel` reads it from there
  (never a second copy in the Makefile).
- **Two check layers, distinct jobs**: the playbook's health
  tasks verify ON the box (127.0.0.1); `make check` verifies from
  the laptop THROUGH the tunnel — the demo-day view.
- **Known live-run risk, accepted**: Ubuntu 24.04 ships Python
  3.12; the spike's venv ran 3.10 (22.04 image). Faster
  Qwen3-TTS on 3.12 is untested — expect the first live run to
  negotiate this (deadsnakes/pyenv fallback if it fights);
  whatever wins amends the role in place.
- **Reboot behavior is a new capability**: with restart policies
  + enabled units, the FULL STACK now rises unattended on VM
  reboot — something the tmux-era experiment never had.
- **Hosts files are committed, both environments** (owner ruling,
  reversing the agent's gitignore proposal): an accidentally
  committed box IP is acceptable; real secrets use the vault
  pattern (§2). Only `collections/ansible_collections/` is
  gitignored.
- **Timebox clock**: the 3 days run from the first PLAYBOOK
  commit — the shape/discussion docs don't start it; the clock
  starts when the skeleton (site.yml + roles) first lands.
- **TalkWithMe portability, settled** (owner, 2026-09-17): the
  client runs on ANY system that can open the SSH tunnel; on demo
  day it runs on the owner's laptop. No per-environment client
  assumption exists anywhere in the deployment.
