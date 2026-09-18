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
    ├── site.yml                  # THE deployment play: base → llama → tts_engine → stt_engine
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
        └── stt_engine/
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
level if a dynamic environment ever appears).

**Service-shaped groups (owner's pattern, adopted 2026-09-17,
superseding the agent's single `gpu` group):** each environment
declares one group PER SERVICE — `llama`, `tts_engine`,
`stt_engine` — listing the hosts that run it, plus an `all.hosts`
block carrying per-host connection data (the inventory NAME stays
stable; `ansible_host` chases the ephemeral IP). The inventory
thereby states the topology: moving a service to another box is a
pure inventory edit (see §11 for how roles read the groups). One
playbook, identical execution, `-i` picks the world:

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
`hosts.yml` carries the `REPLACE_ME_box_ip` sentinel (owner's
sentinel convention, §9), guarded by the placeholder preflight.

## 3. Role anatomy (owner's convention)

Standard, full role structure per role: `defaults/ files/ tasks/
templates/ handlers/ vars/` as needed. One role per service
(owner ruling 2026-09-17): **`base` · `llama` · `tts_engine` ·
`stt_engine`** *(renamed from `whisper` 2026-09-17: the role↔group
naming is 1:1, and whisper is an implementation the way
faster_qwen3tts is — the STT engine slot is swappable, Speaches
being the named fallback)*.

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

- `llama` and `stt_engine` (whisper-fastapi): **detached Docker
  containers with
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

## 9. The preflight pattern (adopted 2026-09-17 from the owner's other project)

The play runs `gather_facts: false` and imports two guard task
files as its first pre_tasks; `ansible.builtin.setup` gathers
facts explicitly AFTER them. The property this buys: `assert`
executes on the CONTROL NODE and needs no connection, so a
misdirected or unwired run **fails before Ansible dials the host
at all**. Guards live as bare task files in `deploy/ansible/
tasks/` — not roles, because nothing in them is composed against
host groups ("composition against host groups is what earns a
role", the owner's criterion, adopted).

- **`tasks/preflight-environment.yml`** — asserts
  `zr_environment == inventory_dir | basename` (each
  `99-<env>.yml` states its environment). Today the drift it
  prevents is mild; it becomes load-bearing the day the reserved
  vault slots fill (env would then select keys/secrets).
- **`tasks/preflight-placeholders.yml`** — asserts no
  deploy-critical variable still carries a **`REPLACE_ME`**
  sentinel (owner ruling: this spelling over `<PASTE-…-HERE>` —
  catches the eye faster; the `<PASTE-…>` convention remains for
  PROSE docs like recipes). Especially load-bearing here because
  `cloud/hosts.yml` is COMMITTED carrying
  `REPLACE_ME_box_ip` at rest between provisions — the guard
  turns a far-away getaddrinfo error into a named, zero-dial
  failure. List starts at `ansible_host`; grows only with real
  contract variables.

Companion conventions adopted in the same round: **`zr_` prefix**
on all project variables · **`ans-` prefix** on the Makefile's
Ansible action targets (file stays `site.yml` per Ansible
convention) · **minimal comments in deployment code** (owner
posture 2026-09-17: doctrine lives in these docs, not in the
YAML; more comments only on explicit request).

## 10. Timebox ledger

- **Task 1 clock started 2026-09-17 ~17:30** (skeleton commit) →
  **abort by end of 2026-09-20** (3 days, late-day start counted
  fairly). First live-debug run against a fresh R570 box is the
  next session's opening move; Ansible itself still needs
  installing on the laptop (the control node).

## 11. Amendments from the skeleton review round (2026-09-17, late)

Settled during the owner's line-level review of the skeleton;
each supersedes anything above that contradicts it.

- **Self-gating roles (owner's pattern, from his `stack_` role):**
  site.yml stays ONE play (`hosts: all`); each service role gates
  ITSELF via a role-prefixed variable in its own defaults —
  `<role>_enabled: "{{ '<role>' in group_names }}"` — checked by
  its tasks. The inventory's service groups drive execution
  through the gate, not through per-group plays or playbook-level
  `when`s. Property this buys: role reusability — drop the role
  into any playbook and it acts only where the inventory says, or
  force it anywhere with `-e <role>_enabled=true`. (The agent's
  one-play-per-group alternative was discussed and rejected:
  equivalent power, more scaffolding; the agent initially — and
  wrongly — presented plays as the ONLY group→role binding
  mechanism.)
- **Tags: REMOVED.** They were agent-proposed, never explicitly
  ratified, and with self-gated roles a full idempotent run is
  the re-run story. Removing them also removed a latent bug the
  relitigation surfaced: `--tags <role>` would have skipped the
  untagged preflight guards (they would have needed `always`).
- **`whisper` role renamed `stt_engine`** (1:1 with its group).
- **`hosts.example.yml` dropped**: hosts.yml is committed and
  carries the REPLACE_ME sentinel between provisions; the
  placeholder preflight is the guard.
- **YAML style ruling:** block style throughout — no flow-style
  `{ }` / one-liner collections in playbooks (short inline tag
  lists were the only tolerated exception, now moot). One
  navigation comment per role in site.yml (owner-requested
  exception to the minimal-comments posture).
- **ansible.cfg additions** (from the EW template): explicit
  `roles_path`, `vault_id_match = True` (strict before the first
  vault exists), `any_unparsed_is_failed = True` (a typo'd -i
  must fail, not green-deploy nothing — re-measured here, exit
  0 → 1).
- **Verification state at freeze:** syntax checks pass (both
  envs) · ansible-lint clean at the `production` profile ·
  placeholder preflight self-test fails correctly on the control
  node (`unreachable=0`) · bad-inventory probe exits 1 ·
  collections pinned (community.docker 5.3.0) · ansible-core
  2.21.4 locked via uv (floor >=2.21, 1-week supply-chain
  quarantine) · ansible-lint in, no commit hooks (owner ruling).
- **Role-variable indirection (owner pattern, 2026-09-17, during
  the llama-role review):** role TASKS use only `<role>_*`
  variables; the role's `defaults/main.yml` maps each one to its
  project variable (`llama_service_user: "{{ zr_service_user }}"`)
  — the defaults file IS the role's declared dependency manifest
  on the outside context. Lazy Jinja evaluation keeps group_vars
  authoritative; direct `<role>_*` overrides still work at
  role-application time.
- **User declarations unified in `common_vars.yml`:**
  `ansible_user` (who Ansible connects as) and `zr_service_user`
  (who services run as) sit side by side there — same user today,
  deliberately separable later; hosts.yml carries connection
  ADDRESSES only.

## 12. Synthesis: the two group→work binding mechanisms (added 2026-09-18)

*The §11 bullet compressed a discussion the owner ruled worth
keeping whole. This section is the agreed synthesis — including a
reframing (2026-09-18) that upgraded the conclusion itself.*

### The model

An Ansible playbook is a list of PLAYS; a play binds a host set
(`hosts:`) to work (roles/tasks). Everything in a play runs on
every host the play targets. GROUPS (inventory) say where things
run; TAGS filter what work runs at invocation time — an
orthogonal axis that neither mechanism below depends on. The
question both mechanisms answer: the inventory says host X is in
group `llama` — what translates that membership into "the llama
work executes on X and nowhere else"?

### Mechanism 1 — play-level binding

One play per group: `hosts: llama` + `roles: [llama]`. The host
set is resolved before the play starts; non-members never see the
play's tasks. This is the textbook-native mechanism, and during
the skeleton review the agent initially presented it as the ONLY
mechanism — which is false, and the record keeps the error.

### Mechanism 2 — conditional gating (ADOPTED)

One play (`hosts: all`); every role listed; each role gates its
own tasks on a predicate over `group_names` (the per-host magic
variable listing that host's groups). Our idiom: the gate is a
role-prefixed variable in the role's defaults —

```yaml
# roles/llama/defaults/main.yml
llama_enabled: "{{ 'llama' in group_names }}"
# roles/llama/tasks/main.yml — one block, gated once
- name: Deploy the llama.cpp LLM server
  when: llama_enabled
  block: ...
```

— which is also overridable (`-e llama_enabled=true` forces the
role anywhere), the property that makes roles reusable drop-in
units.

### The decisive argument (owner's reframing, 2026-09-18)

The first recorded reason for Mechanism 2 was role portability.
That is true but it is a COROLLARY. The root reason:

**A role encapsulates a CONCERN; a group encodes TOPOLOGY — and
nothing guarantees the two dimensions align.** Example: "deploy
the webapp" is ONE concern that legitimately touches THREE
topological places — the `webapp` hosts (install the backend),
the `proxy` host (render the vhost forwarding to those backends),
the `monitors` hosts (define the health checks watching them).

- Mechanism 1 silently assumes concern boundaries coincide with
  group boundaries. In the 1:1 case (our current stack:
  llama-concern = llama-group) it works and looks clean. For a
  cross-cutting concern it forces you to SHATTER the role along
  topology lines — per-group role fragments, or one concern
  choreographed across several plays: the playbook becomes a
  hand-maintained join table between what and where. And that
  join table ENGRAVES A COPY OF THE TOPOLOGY INTO CODE: the
  inventory already states where things run; the play structure
  now states it again — two sources of truth for one fact.
- Mechanism 2 keeps the concern whole and expresses the join as
  DATA: per-task predicates over `group_names`, resolved per host
  at runtime against the inventory. The what stays cohesive in
  the role; the where stays solely in the inventory; the binding
  is LATE (runtime) rather than STRUCTURAL (frozen play
  boundaries). The cross-cutting webapp role is just one role
  whose task clusters carry different gates
  (`'webapp' in group_names`, `'proxy' in group_names`,
  `'monitors' in group_names`).

Corrected power claim: the mechanisms are equivalent ONLY in the
degenerate 1:1 concern↔group case. For cross-cutting concerns,
Mechanism 2 is strictly more expressive with no structural
surgery. Portability follows: a role whose where-logic is
late-bound data never welded itself to a partitioning scheme, so
it survives transplantation.

### Honest costs and the boundary where plays stay right

- Mechanism 2's costs, all cosmetic at our scale: `skipping:`
  output for gated tasks on non-member hosts (zero on one box);
  topology read from inventory + gates instead of announced by
  play headers (site.yml's per-role navigation comments carry
  that load); per-task predicate evaluation (microseconds).
- Ordering across groups is NOT a Mechanism-1 exclusive: within
  one play, each task completes across all applicable hosts
  before the next task starts, so "backends installed before the
  proxy vhost renders" holds naturally.
- Plays remain the right tool when you need ORCHESTRATION
  SEMANTICS — `serial` rolling batches, `max_fail_percentage`,
  distinct strategies, deliberate phases ("DB tier fully
  converged before the app tier starts"). That is plays doing
  their real job (sequencing phases), not standing in as a
  concern→topology map.

### What this settled here

site.yml is ONE play (`hosts: all`) with self-gating roles; the
service groups in each environment's hosts.yml are the sole
statement of topology; moving a service to another box is a pure
inventory edit; and tags were removed (§11) — with self-gated
roles a full idempotent run is the re-run story, and `--tags`
would have silently skipped the untagged preflight guards.

## 13. Privilege doctrine (owner ruling, 2026-09-18)

**Roles assume root.** `become: true` is declared ONCE, at the
play level in site.yml, and stays there. Any task that must run
as a lesser user — including ansible_user — says so explicitly
with `become_user` on that task (paired with its own
`become: true`, which the partial-become lint rule requires at
the same level).

Why this is the right default: **root is the only user identity
that never varies across systems.** An unmarked task therefore
has an unambiguous answer to "who is executing this?" — root,
always. If the default were ansible_user instead, every unmarked
task would raise a per-system question ("who IS ansible_user on
this box?"), and the answer would change between environments.
Explicit-when-not-root makes the exceptions visible and the
default constant.

Consequences: roles do NOT carry their own blanket
`become: true` (an earlier agent hardening pass added block-level
and per-task becomes; relaxed back under this ruling) — a role
transplanted into a foreign playbook assumes that playbook also
grants root at play level, and that assumption is now documented
here rather than encoded redundantly per task. Handlers likewise
rely on the play-level become.
