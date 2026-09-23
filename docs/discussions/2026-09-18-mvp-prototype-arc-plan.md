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

**The reconnaissance brief (owner-ratified 2026-09-21, precedes
the fork; branch `alfre2v/task6-recon-brief`).** Before any
Task 6 code, a guided tour of the fork-relevant anatomy so the
owner's own three-codebase study starts oriented and the fork's
shape round argues from receipts. Shape rulings of 2026-09-21:

- *Sections of the TalkWithMe tour:* (1) pipeline map on one
  screen, mic to speaker, every hop a file:line · (2) the
  server reply path and the sanitizer insertion point, incl. the
  persistence/message model and why server-side is presumptive
  (taxonomy C3) · (3) `static/tts.js` anatomy — the splitter,
  the enqueue pipeline, where the vanished-response watch item
  would be observable, where N-chars enters · (4) settings
  plumbing, settings.yaml → config → router → UI · (5) seams for
  the narration future, mapped against spec §5.3 and the 2024
  entropy-terms baseline — maps only, designs nothing · (6)
  upstreamability audit (separable commits off 7.1, upstream's
  AGENTS.md and pytest conventions as house-style receipts,
  strategy doc §4) · (7) explicitly out: no fork, no patch code,
  no director design.
- *Units (owner's division, by project):* (1) TalkWithMe, deep
  · (2) tts-serve, scoped to what we consume — the synthesize
  contract (text-length limits bound the accumulator's N),
  the engine abstraction (Task 5b adds LuxTTS), voice-reference
  handling (Task 4 samples) — widened only on evidence · (3)
  synthesis: resolve the seam-question ledger · (4) the 2024
  `zombie_radio_ai` integration pass. A short prologue READ of
  the 2024 project happens before unit 1, so section 5 maps
  against the real thing, not the spec's one-liner; the dialog
  exploration of it stays in unit 4.
- *Seam questions:* one ledger for the whole brief, IDs S1,
  S2, …, each naming the unit that raised it and the unit that
  owes the answer; resolutions land as dated notes beside the
  question, never as rewrites.
- *Documents:* the ratified umbrella
  `2026-09-21-task6-reconnaissance-brief.md` (scope, method, the
  seam ledger, synthesis, integration) + one tour doc per
  project, dated as written. HTML derivatives live in
  `docs/visuals/task6-reconnaissance-brief/` — the folder is
  born here, per README's mutability table (`reports/` stays
  for incidents; the owner had forgotten the visuals row).
  One self-contained page per tour plus an index: inline
  diagrams (Mermaid text single-sourced from the markdown),
  annotated code excerpts (HTML only — the owner's favourite,
  keeps him in reading context), `vscode://file` deep links to
  every receipt, a reading itinerary and open questions per
  section, a glossary of upstream's own vocabulary.
- *Method and cadence:* read the actual 7.1 code (pristine
  clone `~/TalkWithMe-client` ≡ the working clone, both at
  93df6ca); the 09-18 anchors get re-verified, never copied;
  every claim labeled measured / docs-say / believed. Section by
  section: reconnaissance reported in chat first, back-and-forth
  until settled or parked, THEN written; the owner reviews in
  VS Code; commits on his word, count unplanned. Unit 1 alone
  unblocks the fork — whether Task 6 starts before units 2–4 is
  a decision taken at unit 1's close.
- *Box status:* the 09-19 A6000 is gone; experiments will spin a
  new VM. The brief needs no box.
- *2026-09-22:* the HTML visuals were dropped by the owner ("bigger
  fish to fry"); `docs/visuals/` is not born. The brief's design
  mandate produced two discussion docs and two ADRs instead
  (prompt structure, story loop; ADR-0002, ADR-0003). Unit 3's
  synthesis is the last item before PR #6 closes.

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

**Second addendum, end of day — Task 3's big lever already
pulled:** the owner raised `max_turns_for_context` 6→50 during
the post-deploy testing and ran the C9 retest inline: **PASSED**
— a planted code word ("Arrow") recalled across distractor
rounds. C9 convicted for the amnesia; the model exonerated on
recall. Coherence otherwise unchanged ("the characters are still
very dumb"), and the session yielded two new taxonomy specimens:
cross-persona label WEARING (Ralph under `[Daniel]:`, a doubled
`[Moira]: [Moira]:`) — identity bleed, more fuel for the
sanitizer — and a clean C8 case (the meta-request "remember the
code word" absorbed as an in-fiction event: "The lab is
destroyed. Over."). Box fate resolved: owner destroys it soon;
Task 1 marked DONE.

**Third addendum — Task 3 CLOSED:** the last item (the D1 sampler
read) turned out to need no box — a source audit answered it:
persona requests carry only `max_tokens` (live 200) +
`temperature` (live 0.8; both UI-settable, persisted in settings.yaml); no penalty/top_p/top_k are sent,
so llama-server defaults govern them (modern default:
repeat_penalty off — likely mooting the penalty-vs-"Over." worry;
one /props curl next box session confirms). Router calls run
near-deterministic (temp 0.1, 16 tokens). Practical upshot for
the audition: without a fork, temperature is the ONLY client-side
sampling knob.

**Reorder ruling (2026-09-19, owner): Task 7b executes BEFORE
Task 6.** Rationale: build `client-talkwithme-mac.yml` against
UPSTREAM TalkWithMe first — the deployment machinery might
interest scorbo2 as a contribution (to TalkWithMe or tts-serve),
and an upstream-targeting demo is the honest offer; after the
fork, the same playbook follows via one `client_repo` var flip.
Design constraints this framing adds (agent, agreed): stay
upstream-vanilla (plain venv+pip, no uv imposed on the playbook's
subject), create-if-absent semantics for settings.yaml and
Personas/ (an installer that clobbers user state is dead on
arrival), and a variable clone dir so upstream and fork coexist
during the transition. Expectation calibrated: a modest offer —
adoption is a bonus, not the goal; the bigger contribution story
(the backend deploy) stays with the community write-up
(follow-ups).

**Refinement (2026-09-19, owner): 7b executes NEXT, but upstream
outreach is DEFERRED past the deadline** — contribution readiness
without contribution distraction. The playbook is built GENERAL
(in-play vars: repo, version, clone dir — serves upstream, our
fork, or any future client); the fork then proceeds without
ceremony. Full strategy: [discussion 2026-09-19]
upstream-contribution-strategy.

## Entry 2026-09-19 — PR #4 review yields the CUDA rule; the hardware dependency becomes a variable + assert

Provenance: reviewing PR #4's torch/torchaudio task, the owner
asked what would happen on a VM with an OLDER driver than the
R570 we debugged against — and asked for the deployment to adapt
easily to other cloud GPU providers (assuming Ubuntu + Docker +
GPU access). The answer generalized the 09-18 pothole into a rule,
and the rule into machinery (green-lit and executed the same day).

**The rule — which devices we can deploy to.** The driver's
`CUDA Version` in nvidia-smi is the MAXIMUM runtime generation it
supports. For our cu128-pinned wheels:

| Box driver vs cu128 wheel | Result |
|---|---|
| Driver newer, even across majors (R595 / CUDA 13.2) | **Works** — drivers run older-CUDA apps unconditionally. |
| Same major, driver minor older (R550 / 12.4, R535 / 12.2) | **Expected to work, unproven by us** — CUDA 12 minor-version compatibility (wheels bundle their own runtime; driver ABI stable within a major; floor R525). Smoke-test before trusting. |
| Driver major older than the wheel's (R570 / 12.8 vs a cu130 wheel) | **Hard fail** — the exact "driver too old" crash loop of 09-18. CUDA 13 wheels need R580+. |

The 09-18 failure was therefore not "the pin is fragile" but
"PyPI's *default* floats to the newest major": a deliberate
one-major-behind pin like cu128 is close to the most portable
choice available — on Hyperstack's whole current image menu
(R535/R550/R570/R595 with Docker) it hard-fails nowhere, while
the floating default fails on everything below R595. The same
rule governs the two CUDA-built containers (llama, whisper): the
driver is the only thing outside our pinning reach. Distilled
portability contract for ANY provider: **Ubuntu + Docker +
nvidia-container-toolkit + a CUDA-12-capable driver (R525+)**.
Full analysis with the mapped Hyperstack menu: provider survey
§S5 ([discussion 2026-09-13]); spec §6 carries the ledger line.

**The machinery change (owner green-light, agent-built, this
entry's session):** `zr_cuda_variant: "cu128"` +
`zr_torch_version: "2.9.1"` in common_vars; the tts_engine role
derives its pins and index URL from them through the usual
defaults indirection; and the base role gained a driver preflight
— parse the driver's supported CUDA version from `nvidia-smi -q`,
assert driver-major ≥ variant-major (majors-only on purpose:
older-major is the hard failure, older-minor is tolerated
minor-compat). This converts the 09-18 experience — crash loop
discovered after a 5 GB model download — into a seconds-fast
named failure at the top of the run, and makes a new
provider/driver a one-line `99-<env>.yml` override. The assert
expression was verified offline against six driver/variant cases
(12.8·12.4·12.2·13.2 vs cu128 pass; 12.8 vs cu130 and 11.8 vs
cu128 fail). Doctrine recorded: shape doc §14. Verification:
syntax both envs + ansible-lint clean at `production`.

**Addendum, same day — the proof-box session births the SSH
doctrine.** The owner ruled the new preflight logic unproven-live
→ merge gate: a fresh from-zero deploy. He rented a deliberately
DIFFERENT image — `Server 22.04 LTS R550 CUDA 12.4 with Docker` —
to test the rule table's middle row (same-major/older-minor
minor-compat, plus a free confound: 22.04's Python 3.10 venv) at
the same time. Mid-box-birth, two rulings landed and were built
(shape doc §15): (1) **no human SSH on a fresh box, ever** — host
keys are TOFU (`accept-new` + project-scoped known_hosts under
`zr_control_dir`, all in common_vars' `ansible_ssh_common_args`;
the agent's initial 99-cloud scoping was relitigated to common
truth in the owner's review; recycled-IP remedy documented);
(2) **the SSH identity is declared, not ambient** —
`ansible_ssh_private_key_file` (+ `IdentitiesOnly=yes`,
owner-proposed) in common_vars; `make ssh-tunnel ENV=<env>`
(hardcoded cloud also caught in review) parses the same key and
mirrors the same options and dir. The Hyperstack box-birth console ritual
(attach IP / enable SSH / enable ICMP) was captured in the
provider survey's Hyperstack entry. Also fixed: the
box-inspection runbook falsely claimed nvtop ships in base
packages (it never did — 09-18 ruling).

**Second addendum — the R550 proof run: everything passes, and
the box catches two bugs no offline check could.** Results on the
`Server 22.04 LTS R550 CUDA 12.4 with Docker` A6000 (CANADA-1,
~64 ms avg RTT):

- **Two live-caught bugs in the new preflight, both fixed
  in-role and re-proven on the box:** (1) the CUDA probe died
  with rc=141 — SIGPIPE: awk's early `exit` closed the pipe on a
  still-writing `nvidia-smi -q` and `pipefail` (correctly kept)
  reported it; fixed by consuming the stream (first-match guard,
  no exit). (2) **The assert silently passed 12.4-vs-cu130** —
  the sabotage run (`-e zr_cuda_variant=cu130`) sailed through:
  complex Jinja inside `assert.that` evaluates through a
  different path than `{{ }}` templating and returned the wrong
  verdict, while the identical expression in a debug task said
  False; the agent's offline six-case validation was
  structurally incapable of catching it (a variant-major that
  silently degrades to 0 passes the same cases). Fix: precompute
  the majors in task `vars`, keep `that:` trivial — warning
  comment now in the role. **Method ruling (owner, sharp):
  with a live box on the meter, test the actual commands ON THE
  BOX before spending playbook runs — the agent runs its own
  checks first.**
- **Negative test PASSED (re-run post-fix):** the sabotage
  deploy dies at the assert, changed=0, full named message
  (12.4 vs cu130, both fixes offered).
- **The rule table's middle row is now PROVEN, not assumed:**
  from-zero converge (changed=13), idempotent re-run
  (**changed=0**), and a real TalkWithMe session — TTS synthesis
  and STT through the mic — on cu128 wheels over the CUDA 12.4
  driver. Minor-version compatibility carried actual inference,
  not just an install. The 22.04 confound also resolved: the
  engine venv built and ran on Python 3.10 (Python again a
  non-event). Dialogue quality unchanged-dumb, as expected —
  Task 5a's mandate, not this arc's.
- **TOFU + declared-key debut clean:** first contact with zero
  prompts, key recorded in the project known_hosts, only
  `hyperstack_2026` offered.
- **Task 3's last residual RESOLVED — `/props` read through the
  tunnel:** `repeat_penalty: 1.0` (neutral/off, llama-server
  modern default confirmed) → the penalty-vs-"Over." worry is
  moot without a fork. Server defaults banked: temp 0.8,
  top_k 40, top_p 0.95, min_p 0.05, repeat_last_n 64 (inert at
  penalty 1.0), DRY off, mirostat off; n_ctx 16384 and the
  Nemotron Q4_K_M alias confirmed serving.

**Third addendum — Task 7b executed the same evening (PR #4
merged in between; branch `alfre2v/client-talkwithme-mac`).**
`deploy/ansible/client-talkwithme-mac.yml` built to the ratified
constraints as ONE self-contained file (vars block = the whole
contract; the offerable shape). Facts the write-time
verifications produced:

- **Upstream TalkWithMe tags 1.0–7.1, no v prefix** (scorbo2
  house style confirmed twice now); default branch `master`.
  Pinned `client_version: "7.1"` — bit-identical to the owner's
  proven manual client (his clone `git describe` = 7.1).
- **Upstream gitignores BOTH `settings.yaml` and `Personas/`** —
  a fresh clone has neither, so the playbook's seeding is
  load-bearing, not decorative. settings.yaml is seeded once
  (create-if-absent) with the proven config: tunnel-port
  endpoints, max_tokens 200 / temp 0.8, window 50,
  max_persona_replies 4.
- **Create-if-absent granularity is the PERSONA:** an existing
  `Personas/<Name>/` is user state, skipped whole; an absent one
  is created complete (prompt.md + `say`-generated ref.wav
  LEI16@24000 + ref.txt — the experiment factory, now tasks with
  argv form and `creates:` guards). Clone protection too:
  `git force: false`, so a locally modified clone fails loudly.
- **Prompt bodies wrapped** to satisfy the 160-char lint line
  limit — newlines are semantically neutral in a persona prompt;
  no lint exception carved.
- **Proof battery on the Mac (all passed):** fresh install
  changed=8 → `~/TalkWithMe-client` at 7.1 · idempotent re-run
  **changed=0** (skipped=6) · tamper test: injected edits to
  settings.yaml and a persona ref.txt SURVIVED the re-run ·
  venv imports clean (plain venv + pip, no uv anywhere) · the
  app boots from the fresh install and serves HTTP 200.
- `make client-mac` added (inventory-free by design — no ENV,
  no -i; logs to the usual place). Upstream outreach stays
  DEFERRED: the playbook is now offerable, nobody is contacted.

## Entry 2026-09-22 — the ADR-0003 gate on a live A6000; a first-boot updater, two dropped SSH sessions, tts-serve 1.2 banked; ADR-0003 accepted 2026-09-23

Provenance: a fresh session opened on the handoff of 2026-09-22 and
ran Task 6's gate on a Hyperstack A6000 with the "Ubuntu Server 22.04
LTS R550 CUDA 12.4 with Docker" image — the 09-19 proof run's image.
The branch is `alfre2v/adr-0003-gate`; the records are two experiment
folders and a discussion (pointers at the end).

**The deployment science of the evening.**

- **A fresh box spends its first hour in Ubuntu's own updater.** At
  46 minutes after boot, `apt-daily-upgrade.service` started
  `unattended-upgrade` on two years of pending security updates (259
  packages, 43 minutes in all; it skips the kernel and NVIDIA
  packages by its own blacklist, so the driver was never at risk).
  Our deploy reached `base : Install base packages` three minutes
  into it and failed after the apt module's default 60-second lock
  wait — with an error that named the lock's holder
  (`unattended-upgr`) only inside a long JSON dump. Nothing on the
  box changed (`changed=0`). Why the 09-19 run on the same image did
  not hit it is not known (believed: timing luck).
- **A long silent wait is fragile on this network path.** With the
  wait raised to 900 seconds, the next deploy waited as designed —
  then lost its SSH session after about 14 minutes of silence
  (`UNREACHABLE … Data could not be sent to remote host`). Ruled out
  on the box: a reboot, an sshd restart at that moment, a Docker
  restart. The owner's tunnel later died too, after about 70 idle
  minutes. The owner's explanation (2026-09-23): public library
  Wi-Fi, and a laptop lid closed during breaks without closing the
  tunnel — not a significant worry. Kept as a low-priority
  follow-up (SSH keepalives), with one note for demo day: a tunnel
  that reconnects by itself is cheap insurance for a live show.
- **The fix that shipped (`9fbbeb3`):** the apt lock wait is now
  `zr_apt_lock_timeout` (common_vars, 300 s), announced in the task's
  name before the wait begins; on a lock timeout a rescue stops with
  a plain explanation quoting apt's own "held by process …" line, the
  command to check the updater, and how to wait longer. Proven live
  with the owner holding the lock in `sudo aptitude`: a 10-second
  wait, the explanation printed, `changed=0`.
- **From zero in 7 minutes.** Once the updater had finished, the
  from-zero deploy took 7 minutes (`ok=33 changed=16`), the re-run
  reported `changed=0` in 30 seconds, and `make check` printed three
  ok lines.
- **Banked: tts-serve 1.2** (`33cc5c6`). Deployed from zero with the
  converge invariant intact, and synthesizing through the tunnel (six
  clips in the emotion run's side quest, called on tts-serve
  directly rather than through TalkWithMe). The owner ruled the pin
  proven on 2026-09-23; its follow-up entry is deleted.
- **What the server is** (build `b11096-c550d2f60`, from `/props` and
  the server's help): a host-RAM prompt cache is on by default
  (`--cache-ram` 8,192 MiB); recurrent-state checkpoints up to 32 per
  slot, at least 8,192 tokens apart; and the chat template removes
  `/no_think` from the text and ends the prompt with an empty
  `<think></think>` — without `/no_think` it would end with an open
  `<think>`.
- **After the evening** the owner hibernated the VM, keeping its IP
  (a few cents an hour); the standing rule "never hibernate a show
  box" applies to demo day.

**The gate, in one paragraph.** Both on-box items passed against
pre-registered criteria: the screenplay grammar streams and binds
through the top-level `grammar` field; one shared script per round
costs about a quarter of the per-persona structure's prompt time, and
the grammar 0.3 % per token. The latency win's reason was not the one
believed — a host-RAM cache rescues per-persona prompts, which pay
instead in state swaps before each request and a fixed prompt toll
per request. A second run the same evening measured an `(emotion)`
tag in the grammar: 0.5 % per token when the prompt teaches it,
10.4 % when forced on a prompt that does not mention it. With the
same prompt and seed, the model wrote the same text with and without
the grammar in 20 of 20 rounds, which answered the gate's audition
item for this model. **ADR-0003 accepted 2026-09-23.**

**Process notes.** At the owner's request the probes wrote a live,
readable wire log for `tail -F`; it proved its worth at once — its
tests caught a timing flaw in the streaming instrument before the
box saw it — and it has a documented blind spot (it does not show
which grammar was sent). The owner declined to predict in both runs.

Records: `docs/experiments/2026-09-22-adr-0003-gate/`,
`docs/experiments/2026-09-22-emotion-grammar-cost/`, and
[discussion 2026-09-22] grammar-and-prompt-cache-lessons (the
owner's questions and the lessons for the fork). **Next: the fork
(TalkWithZombies, ADR-0002); the 3-day timebox starts when it
exists.**

*Open at this point (snapshot, 2026-09-23).* What the gate left
unexplained about the server, all on llama.cpp `b11096` with the
hybrid Nemotron: a fixed prompt cost of about 350 ms per request;
host-RAM cache entries of 417 MiB to 1.8 GB; the unmeasured cost of
editing the script's history on a model whose recurrent-state
checkpoints sit at least 8,192 tokens apart — which the director's
transcript curation depends on; why a grammar is nearly free when
the model agrees and ~10 % dearer when it must overrule it (believed:
check-first sampling); and whether the build has an
`/apply-template` endpoint. On the engine's side: the cost of the
director's per-round constraints, single-line beats, the bounded
scratchpad. The lasting list, with when each matters and where it is
tracked: [discussion 2026-09-22] grammar-and-prompt-cache-lessons
§4.10.
