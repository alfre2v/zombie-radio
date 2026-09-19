# MVP-prototype arc — build plan & journal

**Arc:** MVP prototype (opened 2026-09-17) · **Type:** the arc's
plan document — **the extended notepad for TODO.md's tasks across
their whole lifecycle** (owner convention, clarified 2026-09-18):

- **BEFORE execution** — expanded per-task notes too long for the
  terse TODO line (approach sketches, open questions, gathered
  intel) live in *Task notes* below.
- **DURING execution** — the same sections hold working notes, so
  the TODO stays a clean state table.
- **AFTER execution** — findings land as dated *Journal entries*,
  INTEGRATED per session (never a chat chronicle).

The task-level live STATE stays in `TODO.md` (the parking-lot
table); patterns graduate to the shape doc
([discussion 2026-09-17]); this doc holds the depth. It is the
document the close ritual expects a closing entry from.

**The plan in one line:** deliver D1 (deployment machinery) →
D2 (running prototype, real cast) → D3 (in-prototype experiment
verdicts), under the prototype-first inversion's guardrails.
Deliverables, acceptance lines, and task decomposition:
`TODO.md`.

---

## Task notes (living, per task — pre/during execution depth)

*(Sections appear when a task earns notes; they may be trimmed
once their content graduates into a journal entry.)*

### Task 6 — the fork + first patches (trigger fired 2026-09-18)

Seed notes for when it starts: fork thin under the owner's
account; keep the diff minimal and upstreamable (sanitizer +
max-chars accumulator as separable commits → candidate PRs to
scorbo2). Sanitizer options to weigh at write time: server-side
(strip in the reply path before persist/TTS) vs client-side
(strip in `static/tts.js` before enqueue) — server-side also
cleans the transcript that feeds back into context (a C3
contamination win), so it is the presumptive choice. The
accumulator: replace the per-sentence split in `tts.js` with
pack-up-to-N-chars; N becomes a settings knob; test items —
"Dr. Byrne. 47. Microbiology. Over." as one request, and the
lone-"1." echo case. The uv drop-in mode applies to the fork's
client env (entry 2026-09-17 analysis).

---

## Entry 2026-09-17 — arc opened; deployment machinery designed and skeleton-built

Arc opened with the deployment-first ruling ([discussion
2026-09-17] deployment-first brainstorm). A multi-round shape
discussion converged the Ansible design — layout, inventory
pattern, self-gating roles, supervision, preflights, privilege
doctrine — all recorded in the shape doc ([discussion 2026-09-17]
ansible-deployment-shape, §1–§13, including the two-mechanisms
synthesis §12). The skeleton was built the same evening and
verified hostless: syntax both envs, ansible-lint clean at the
`production` profile, placeholder preflight self-test failing
correctly on the control node with zero dial. Task 1 timebox
started ~17:30.

**Design-day decisions not captured elsewhere (distilled):**

- **Control-node tooling: uv** (over plain venv / global
  installs) — top-level `pyproject.toml` + committed `uv.lock`;
  `ansible-core` only (never the ~700 MB `ansible` distribution);
  `exclude-newer = "1 week"` supply-chain quarantine adopted from
  the owner's EW project; ansible-core locked at 2.21.4, floor
  `>=2.21`; `.python-version` (3.12) pins both uv and the owner's
  pyenv shell. Side analysis banked: converting a TalkWithMe fork
  to uv = drop-in ~zero effort (`uv pip install -r`), full
  pyproject conversion ~30–60 min with the real cost being merge
  friction against upstream's requirements.txt — drop-in mode
  until the fork stops tracking upstream.
- **The owner's EW project was mined as a pattern template**
  (never copied wholesale): the Makefile conventions
  (`require_ansible_env` guard, timestamped run logs to
  `~/.config/zombie-radio/logs/`, `ANS_VERBOSE`, `ans-*` action
  naming, `ANSIBLE_CONFIG` exported ABSOLUTE — cfg discovery is
  CWD-relative and silently ignored in world-writable dirs), the
  control-node preflight pattern, and the ansible.cfg hardening:
  `any_unparsed_is_failed = True` (a typo'd `-i` is only a
  WARNING by default — a green deploy of nothing; re-measured
  here, exit 0 → 1), `vault_id_match = True` (strict before the
  first vault exists), explicit `roles_path`.
- **Collections: exactly one** (community.docker, pinned 5.3.0 —
  galaxy has no lockfile, the pin is the only reproducibility
  lever). `ansible.posix` and `community.general` REJECTED with
  named reasons: no bootstrap playbook → no `authorized_key`
  need; ufw is off by §10.2 ruling → the one module justifying
  community.general is one we decided never to call.
- **ansible-lint: "very in"** (owner) — passes at the strictest
  `production` profile; no commit hooks (later narrowly amended
  by the NEVER_COMMIT hook, entry 2026-09-18).
- **The owner's skeleton review rounds each improved the
  artifact:** flow-style YAML banned (block style throughout) ·
  one navigation comment per role in site.yml (owner-requested
  exception to the minimal-comments posture) · **tags removed**
  (agent-proposed, never explicitly ratified — the relitigation
  also surfaced a latent bug: `--tags` would have silently
  skipped the untagged preflight guards) · service-shaped groups
  + self-gating roles (the concern-vs-topology argument, shape
  doc §12) · **role-variable indirection** (tasks speak only
  `<role>_*`; defaults map to `zr_*` — the dependency manifest) ·
  user declarations unified in common_vars (`ansible_user` vs
  `zr_service_user`, same today, separable later) · the privilege
  doctrine (root is the only invariant identity; shape doc §13) ·
  inventory host aliases `cloud-1`/`local-1`.

## Entry 2026-09-18 — D1 proven live on a fresh A6000; D2 MET; the tripwire is born

**The box:** Hyperstack RTX A6000 48 GB (the elusive one — in
stock at last), CANADA-1, $0.50/hr, pinned image `R570 CUDA 12.8
with Docker`, Ubuntu 24.04. **RTT from the laptop: ~58 ms** (vs
NORWAY-1's ~215 ms — the region intel confirmed in production).

**Live-debug potholes, each found by a failing run and fixed in
the roles (the playbook-first sequencing doing its job):**

1. **PyPI's default torch is a cu130 build; the R570 driver
   speaks CUDA 12.8** → crash loop ("driver too old"). Then the
   second head of the same hydra: torchaudio from PyPI carried a
   cu130-ABI extension that could not load against the replaced
   torch. Fix: `torch==2.9.1+cu128` AND `torchaudio==2.9.1+cu128`
   pinned TOGETHER from the PyTorch cu128 index, before the
   engine package installs. (The feared Python 3.12 pothole never
   materialized — the venv runs 3.12.x happily; the real pothole
   was CUDA generation, not Python version.)
2. **tts-serve git tags carry no `v` prefix** (`1.1`, not
   `v1.1`) — the agent pinned a tag name it had read in a README
   changelog and never verified against `git ls-remote`.
3. **llama.cpp's `-hf` cache switched to HF-hub-style,
   extension-less blobs** (`models--org--repo/blobs/<sha256>`) —
   the role's cache assertion looked for `*.gguf` (the
   experiment-era layout) and false-positived on a healthy
   deploy. Rewritten to assert by size (any file ≥ 1 GB).
4. **Local-path pip installs always report `changed`** (pip
   reinstalls local dirs blindly) — broke the converge invariant
   (changed=2 on a no-op run, needlessly restarting the service
   via handler; caught by the owner's idempotency run). Fix: the
   `tts-engine-common` install is guarded — absent-or-clone-
   changed. Converge now reports changed=0 (verified).

**The NEVER_COMMIT tripwire (owner-designed), and the near-miss
that provoked it:** the agent pasted the live IP into the
committed hosts.yml and queued it for commit, having earlier
flattened the owner's "an accidental IP in history is tolerable"
into "IPs are committable." The fix became machinery: a
pre-commit hook where a `NEVER_COMMIT`-marked line commits ONLY
while its `REPLACE_ME` placeholder precedes the marker — pasting
a real value self-arms the block, no ritual. Index-only scan
(dirty-unstaged files never block unrelated commits). Full
mechanics: shape doc §2. Verified with a four-case battery,
including git itself refusing.

**Deployment verdict — D1 proven:** full stack from a bare box
with one command (`make ans-deploy ENV=cloud`); fresh-path
validated by deliberately deleting the engine root and
reconverging from zero (owner's call: no in-place downgrades —
residue makes the venv unlike what a fresh run builds, and the
fresh path IS the product); idempotent re-run changed=0.
**Box datums:** trio at 12.3/48 GiB VRAM (llama 6.7 · tts 4.8 ·
whisper 0.8 lazy) · **TTS RTF 0.36–0.48 on the A6000** (vs
0.46–0.64 on the A4000) · 28 vCPU · 56 GB RAM.

**D2 acceptance — MET (owner-run):** fresh room, 4 scientists,
Global System Prompt clear, `max_persona_replies: 4`. All four
replied in character with four distinct cloned voices; TTFA
subjectively snappier than the Norway box; inter-sentence gaps
"almost natural" at 58 ms RTT; the mic round-trip closed the
loop. A full ensemble session on a stack Ansible built from
nothing.

**Field observations logged:**

- **`[Name]:` labels are back and SPOKEN** (expected: no Global
  System Prompt, per lab3) → **the sanitizer/fork trigger has
  FIRED** (disposition below).
- **Moira + "1" echo artifact** on an ultra-short synthesis — a
  THIRD motivation for the max-chars accumulator (after splitter
  naivety and short-sentence economics), and a new §7.2 test
  item: ultra-short inputs per engine.
- **One vanished TTS response** on a fresh chat; server logs show
  all 200s → client-side suspicion (tts.js pipeline or audio
  queue). Watch, don't chase; diagnostic (browser devtools →
  Network → `synthesize`) noted in the box-inspection runbook.
- Dialog intelligence remains low — the audition's mandate
  (Task 5a), unchanged.

**Smaller facts worth keeping:**

- **Timebox accounting:** D1 proven + D2 met at ~1.5 days of the
  3-day budget.
- This was also the pinned image's **first real validation**
  (`R570 CUDA 12.8 with Docker`, Ubuntu 24.04) — the §6 posture
  held; the only image-related surprise was the PyPI-side CUDA
  float, not the image itself.
- **nvtop ruling:** NOT added to base packages (owner: installs
  it himself when needed). Method note worth reusing: the safety
  question ("will apt pull a conflicting NVIDIA driver?") was
  answered with `apt-get install --dry-run nvtop` on the box —
  one package, zero driver deps (nvtop dlopens the existing
  libnvidia-ml at runtime).
- **Client config carried over untouched:** TalkWithMe's saved
  server settings from the spike (localhost:8080/8001/8002) drove
  the new box through the tunnel with zero reconfiguration —
  the stable-ports contract paying out.
- Not collected (offered, skipped): an A6000 vs A4000 LLM tok/s
  comparison — one curl away whenever wanted.
- **Guardrail-3 compliance:** the spec received a same-evening
  deep ledger pass (7 dated updates: §6 as-built + operational
  properties + the cu-index corollary + the cribbing supersession,
  §7.2/§7.3 as-built mechanics, §8 first measurement, §10.2
  correction, §10.4 reworked to the tiered secrets doctrine).

**Q&A dispositions (owner + agent, same evening):**

- **Q1 — fork trigger:** JUMPED. Chain: spoken labels are
  unshippable → the zero-code lever was convicted by lab3 → the
  sanitizer is a TalkWithMe source change. Disposition: fork
  thin, patch minimally (sanitizer + accumulator), offer both
  upstream to scorbo2 in parallel. Executes as Task 6, after
  Task 1 closes.
- **Q2 — local-inventory testing:** the deployment-first ruling 4
  gate ("not until the cloud deployment replicates the
  experiment") OPENED today by its own precondition. Remains
  optional and deprioritized (no audience visibility; revives
  the 3090 driver check).
- **Q3 — automating the TalkWithMe client install (the MAC
  laptop, the owner's actual question):** NOT a role — roles are
  the automatic deployment path and the client must never be in
  it (owner, same evening, retracting the idea after the agent
  first mis-read the question as a Linux-target role). At most a
  **standalone top-level playbook** (the reserved-slots pattern:
  run deliberately, never by site.yml), e.g. `client-talkwithme-mac.yml`
  against localhost: clone + venv + requirements +
  settings-template pointed at the tunnel ports; no supervisor
  (uvicorn is launched by hand at showtime — appropriate). The
  Mac's no-apt/no-systemd species problem doesn't bite a
  playbook this small. Red flags that keep it parked: the
  Personas tree is SHOW DATA about to churn (bibles +
  never-committed voice samples → needs a private-assets-dir
  variable), and the marginal value is small while the manual
  install is ~4 commands. Disposition (upgraded the same
  evening): **TODO Task 7b** — the owner chose to build it,
  folding in his own resolution of the audio-fragments caveat:
  automate the placeholder-voice factory (the `say`/`afconvert`
  blocks from the experiment's placeholder-personas.md), so the
  synthetic cast ships with audio; the real cast stays manual by
  the never-commit rule. Naming convention set:
  `client-<name>-<platform>.yml`, anticipating future clients.

**Still open in Task 1 at this entry's close:** the reboot test
(unattended auto-rise proof) · restart-runbook rewrite (ruling-2
trigger fired: the playbook succeeded today) · spec §6 as-built
ledger line · TODO true-up · keep-vs-destroy call on the box
($0.50/hr; rebuild is now a proven one-command, ~15-minute act).

**Addendum, later the same evening — the reboot test PASSED, and
then some:** full unattended auto-rise in UNDER A MINUTE (warm
NVMe makes the model reload far quicker than the cold ~90 s);
TalkWithMe reconnected on nothing but a fresh tunnel. The last
live checkbox of Task 1. Also logged: the NEVER_COMMIT hook
scored its first production catch — the owner deliberately left
the live IP armed, the agent's `git add -A` swept it up, the hook
refused by file:line ("Ah, got you!"). Ruling-2 executed: the
restart runbook is rewritten around the playbook;
`deploy/ansible/README.md` written. Remaining in Task 1: only the
owner's keep-vs-destroy call on the box.
