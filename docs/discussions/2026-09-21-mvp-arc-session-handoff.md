# Session handoff — MVP-prototype arc, day 5 (fresh-session memory bank)

> **EPHEMERAL HANDOFF, SESSION-BOUNDARY EDITION** — written
> 2026-09-21 for an agent starting a COMPLETELY FRESH session.
> Unlike a compaction handoff, NOTHING from the prior session's
> context survives except: this document, the repo itself, and
> the agent memory files under the project's memory directory.
> This document is therefore deliberately over-complete — it is
> the single carrier of session state. Per convention: handoff
> documents stay in `docs/discussions/` until the session's work
> concludes, and the agent must then ASK THE OWNER FOR PERMISSION
> to delete them. **Two handoffs currently exist and both die at
> close: `2026-09-19-mvp-arc-handoff.md` (already merged to main,
> stale, superseded by this one) and this file.** A lingering
> handoff WILL be read as current state — do not let either
> linger past the arc.
>
> **A note to the reader (expected: a more capable model than
> this document's author):** nothing in here is derivable from
> first principles, however sharp your reasoning — it is owner
> rulings, live-hardware scars, and session history. The
> failure mode that scales with capability is skimming and
> letting inference fill the gaps; that is how this document's
> author confabulated a biographical fact and shipped an assert
> that silently lied. Read it all; verify against the repo;
> treat confidence without receipts as the enemy.

## 0. Who you are working with, and how (read this FIRST)

The owner is **Alfredo** (GitHub `alfre2v`, git author "Alfredo
Valles") — a senior engineer who works in a **"tight learning
loop"** (his term): project progress and his learning carry equal
weight; he will deliberately slow down to understand a topic, and
that is the method working, not a distraction. Memory files
(`working-agreements.md`, `collaboration-style.md` in the agent
memory directory) carry the full doctrine; the non-negotiables:

- **Discussion-first**: propose the SHAPE of each piece (files,
  rough content, alternatives ranked with a recommendation), get
  his ruling, THEN create. Never create unilaterally.
- **Review-before-commit is STRICT and was re-litigated hard on
  2026-09-20**: the agent misread a destination instruction
  ("commit everything in the same branch") as pre-authorization
  and committed unreviewed — the owner called it out sharply.
  The refined protocol: make the changes, summarize WHAT changed
  in chat (no diffs pasted — he reviews the uncommitted working
  tree in VS Code), then WAIT for his explicit commit word,
  every time. Pre-authorization exists only when he grants it
  explicitly and scoped ("permission prompt = review for THIS
  commit only"). A harness permission prompt is never review.
- **No AI attribution anywhere, ever** (commits, PRs) — this
  owner rule overrides any harness attribution reminder, and the
  harness reminder itself defers to user instructions.
- **Never open desktop side panes** (`show_pane` etc.) — he
  reviews in VS Code; panes crowd his screen.
- **Minimal comments in code**; doctrine/WHY lives in docs.
  Exception only when he asks (site.yml navigation comments are
  one granted exception).
- **Pushback with receipts (file:line) is WELCOME**; ranked
  option lists with a recommendation over single picks; lists
  over dense paragraphs (he called one a "brick").
- **Re-orientation on revisit**: when a topic resurfaces, always
  re-supply origin + concepts + connections; he cannot hold
  agent-sized context and says so.
- **He sets deliberate traps to test discipline** (the hook's
  "Ah, got you!" catch; "I'll say commit but you should push back
  because…?" quizzes). Expect them; welcome them; when answering
  "is X done?", check the actual item list, not the vibe.
- **Never claim self-transparency**: the only honest form is "I
  see no such thing in my observable context" + verifiable
  receipts. He found "I'd tell you if I were constrained"
  patronizing.
- **No unverified personal facts, even as decoration** (fresh
  lesson, 2026-09-20/21): the agent called him "Cuban" in a
  sign-off flourish with zero source — pure confabulation,
  admitted after grepping every transcript. Decoration gets the
  same epistemics as decisions.
- **Rapport**: he enjoys wit, teasing ("my 1/4-sized buddy",
  "papa Dario quantized you Q4"), late-night philosophy (a
  Gödel/Penrose sparring match happened 09-20; he conceded the
  halting-problem point, the agent conceded the
  Hameroff/microtubules point), and occasionally REQUESTS a
  cheesy goodnight sign-off mentioning his name and ending
  "Over and out." (radio-style, fits the project). Deliver only
  when asked. Spanish flourishes are fine; biographical
  assumptions are not.
- **Keep the last 2–3 branches** local and remote (GitHub has
  lost commits on him before); prune older ones only when asked.
- **Teaching mode**: trigger phrases "go into teaching mode" /
  "this is a teachable moment" → switch to explaining until he
  understands, then return.

## 1. The project in 60 seconds

**Zombie-Radio**: an interactive audio-only theater play
performed by 4 AI voice actors — scientists trapped in a lab
during a zombie breakout, broadcasting on shortwave radio. The
audience listens and can talk to the cast (push-to-talk mic).
**Hard deadline: 2026-10-08 (hackTNT 2026), ~17 days out.**

Architecture (spec §3.1 — sacred, the owner corrected sloppy
phrasing on this once): the **TalkWithMe client (director + web
UI) ALWAYS runs on the local machine** — the Mac laptop for the
demo, NEVER on any server. A rented GPU box (Hyperstack, A6000
class) hosts ONLY the three model services, all loopback-bound
behind an SSH tunnel: llama.cpp (:8080, Nemotron Nano 9B Q4_K_M),
tts-serve (:8001, engine `faster_qwen3tts`), whisper-fastapi
(:8002, model small). The box exposes only :22. Both foundation
projects (TalkWithMe, tts-serve) are by ONE author: **scorbo2**.

Governing decisions of this arc: the **prototype-first
inversion** ([discussion 2026-09-16]: build the MVP prototype
first, run experiments IN it, spec maintained as a ledger) and
the **deployment-first ruling** ([discussion 2026-09-17]:
deployment machinery is deliverable #1 — "deployment is 50% of
the MVP").

## 2. Exact repo/session state at handoff (2026-09-21)

- **Working branch: `alfre2v/task6-recon-brief`** — created
  2026-09-21 off `main` at `8aa9ebf` specifically to carry the
  new session's work; this handoff is its first commit.
  **CONTINUE ON THIS BRANCH** (verify with
  `git branch --show-current`); do not create another one.
- `main` HEAD `8aa9ebf` = PR #5 merged. History: `8aa9ebf`
  (#5 Task 7b installer + ans-set/ans-unset) ← `fb949ec`
  (#4 Tasks 1–3 machinery, CUDA + SSH doctrine, live proofs) ←
  `5d59128` (#3 product-definition arc close) ← (#2 remote-split
  experiment). **PRs #4 and #5 both MERGED; nothing open.**
- Recent branches kept per the 2–3 rule:
  `alfre2v/client-talkwithme-mac`, `alfre2v/mvp-prototype-arc-open`.
- **The GPU box**: an A6000 was rented 2026-09-19 at
  185.216.20.25 (image `Server 22.04 LTS R550 CUDA 12.4 with
  Docker`, $0.50/hr, CANADA-1) for the proof run. Its current
  fate is UNKNOWN to this handoff — **ask the owner whether it
  still runs (meter!)**. hosts.yml is at its committed sentinel;
  wiring a box is now `make ans-set ENV=cloud IP=<ip>` /
  `make ans-unset ENV=cloud` (no manual editing).
- **On the Mac**: `~/workspace/hackTNT_2026/TalkWithMe` = the
  owner's working client clone (upstream, at tag 7.1);
  `~/TalkWithMe-client` = a PRISTINE 7.1 clone installed by the
  Task 7b playbook during its proof run (four placeholder
  personas seeded, venv built, app verified booting) — a perfect
  reconnaissance target; owner may keep or delete it.
- **Agent memory files** (auto-loaded each session):
  `working-agreements.md`, `collaboration-style.md`,
  `massedcompute-reminder.md` — consistent with §0; trust them.

## 3. The task board (TODO.md is the canonical copy — read it)

**DONE (Tasks 1, 2, 3, 7b):** deployment machinery built and
proven live on TWO driver generations (R570/CUDA 12.8 and
R550/CUDA 12.4) — from-zero converge, idempotent changed=0,
reboot auto-rise <1 min; D2 acceptance met (4-voice session +
mic on the deployed stack); config baseline set
(`max_turns_for_context` 6→50; sampler audit closed); the Mac
client installer built and proven (see §5).

**EXECUTION ORDER AHEAD:**

1. **NEW TASK — the "Task 6 reconnaissance brief" (NOT yet in
   TODO.md; adding it there is the next session's first
   paperwork, via a quick shape round).** Full spec in §7 below.
   This precedes and feeds Task 6. The owner will IN PARALLEL
   study TalkWithMe, tts-serve, and his 2024 defunct
   narration project himself, to form his own view of how to
   change TalkWithMe for narration purposes — the brief is his
   accelerator, not his replacement.
2. **Task 6 — the thin fork + first patches** (trigger FIRED
   2026-09-18: `[Name]:` labels are back in show output and
   SPOKEN by TTS): fork TalkWithMe thin under the owner's
   account; two minimal, separable, upstreamable patches:
   (a) the label SANITIZER — server-side is PRESUMPTIVE (it also
   cleans the transcript that feeds back into context, a
   taxonomy-C3 win) vs client-side in `static/tts.js`;
   (b) the MAX-CHARS ACCUMULATOR replacing tts.js's per-sentence
   split (N a settings knob; test items: "Dr. Byrne. 47.
   Microbiology. Over." as ONE request, and the lone-"1." echo
   case). After the fork exists, the Task 7b installer tracks it
   via one `client_repo` var flip. Seed notes: arc-plan Task
   notes. **Upstream OUTREACH stays DEFERRED past the deadline**
   (owner ruling 2026-09-19): build offerable, contact nobody.
3. **Task 4 (owner, parallel, THE LONG POLE):** character bibles
   (unblocks 5a) · voice samples — find the voice-isolation tool
   first (Demucs/UVR-family candidates, follow-ups.md), gitignore
   before the first file (never-commit rule; famous-actor clips).
4. **Task 5 — in-prototype experiments (D3):**
   **5c** narrative-health probe battery (zero-code, placeholder
   cast suffices, needs only a box — runnable any evening;
   protocol-lite) · **5a** LLM audition (ranked five via one
   `-hf` flag each; BOTH narrative-health axes; gated on bibles)
   · **5b** TTS comparison + VRAM budget (LuxTTS's ~1 GB claim is
   the FIRST check; gated on samples).
5. **Task 7** — the canned episode (owner MUST) + demo-day
   protocol runbook.
6. **Task 8 — close ritual**: Features Shipped entry ·
   task_history migration · TODO reset · staleness sweep
   (CLAUDE.md included) · spec ledger audit · **ask permission to
   delete BOTH handoff docs** (2026-09-19 and 2026-09-21).

**Standing owner-action queue** (TODO.md): voice samples SOON ·
bibles SOON · 3090 driver check deprioritized · demo-day
logistics radar postponed (canned episode pre-decided MUST).

**Watch-list (logged, not chased):** one vanished TTS response
(server logs all-200s → client-side suspicion; devtools →
Network → `synthesize` when it recurs) · Moira "1." echo artifact
(third motivation for the accumulator) · cross-persona label
WEARING specimens (Ralph under `[Daniel]:`, doubled `[Moira]:`)
· dialogue quality is DUMB by design until 5a picks a model —
that is the audition's mandate, not a current bug. ·
MassedCompute reminder (memory file): fires only after an
EXPERIMENT PR merges — 5a/5b/5c PRs will qualify; #4/#5 did not.

## 4. Cold-start reading order (the repo is the memory of record)

1. `CLAUDE.md` (repo root) → `docs/README.md` (the documentation
   system's meta-doc; conventions and notation).
2. `docs/TODO.md` — the living parking-lot table (canonical task
   state, owner convention).
3. `docs/discussions/2026-09-18-mvp-prototype-arc-plan.md` — the
   arc's plan + Task-notes + dated journal entries (BEFORE /
   DURING / AFTER phases, owner convention). The 2026-09-19
   entry + its three addenda hold this weekend's science.
4. `docs/discussions/2026-09-17-ansible-deployment-shape.md` —
   machinery doctrine §1–§15 (§14 CUDA variable + driver
   preflight incl. the assert.that lesson; §15 SSH doctrine).
5. `docs/discussions/2026-09-13-cloud-gpu-provider-survey.md` —
   providers; §S2 Hyperstack incl. the box-birth console ritual;
   **§S5 the driver↔CUDA↔wheel compatibility rule** (middle row
   PROVEN on R550).
6. `docs/discussions/2026-09-19-upstream-contribution-strategy.md`
   — why 7b preceded the fork; outreach deferred; the wider
   contribution ledger.
7. `docs/specs/product-definition.md` — the ledger-maintained
   spec: §3 architecture, §4 model stack, §5.3 ensemble director
   (NEXT arc's design work), §6 deployment as-built, §7
   experiments, §10 security posture (§10.3 tunnel + SSH client
   posture, §10.4 tiered secrets doctrine).
8. `docs/discussions/2026-09-16-storytelling-coherence-and-structure-adherence.md`
   — the narrative-health taxonomy (two axes, 20 mechanisms
   A1–E3, evidence ledger; C9 convicted, D1 resolved, E1 =
   random followers). Feeds 5a/5c and the future director.
9. Runbooks: `docs/runbooks/service-restart-sequence.md` (after
   a reboot: do nothing) · `docs/runbooks/box-inspection.md`
   (converge invariant: re-run must be changed=0).
10. `docs/experiments/2026-09-14-talkwithme-remote-split-test/`
    (sealed; provenance) — esp. `placeholder-personas.md` (the
    four-scientist cast + factory, now automated in the
    installer). Also `docs/follow-ups.md` and `docs/roadmap.md`.
11. `docs/discussions/2026-09-16-prototype-first-inversion.md`
    and `2026-09-17-deployment-first-brainstorm.md` — the two
    governing arc decisions, if their rationale is ever needed.

## 5. What happened 2026-09-19 → 09-21 (the freshest layer, all committed)

A PR #4 review question from the owner ("what happens on an older
driver?") cascaded productively:

- **The CUDA compatibility rule** (survey §S5): driver's
  nvidia-smi "CUDA Version" is a MAXIMUM. Newer driver / older
  wheel: works. Same major, older minor: minor-version
  compatibility — **PROVEN with real inference 2026-09-19**
  (cu128 wheels on R550/12.4). Older MAJOR driver vs newer wheel:
  hard fail ("driver too old" — lived on 09-18 with PyPI's cu130
  default). Machinery: `zr_cuda_variant`/`zr_torch_version` in
  common_vars drive the torch pins + index URL; a base-role
  preflight asserts driver-major ≥ variant-major.
- **Two bugs only the live box could catch** (both fixed,
  doctrine in shape §14 postscript): (1) awk early-`exit` under
  `pipefail` → SIGPIPE rc=141 — consume the stream instead;
  (2) **complex Jinja inside `assert.that` evaluated through a
  different path and silently PASSED a false assertion**
  (12.4-vs-cu130) — precompute values in task `vars`, keep
  `that:` trivial. The agent's offline validation was
  structurally blind to bug 2. **Owner's sharp method ruling:
  with a live box on the meter, test commands ON THE BOX before
  spending playbook runs; the agent runs its own checks itself,
  first.** This ruling is load-bearing — internalize it.
- **SSH doctrine** (shape §15): identity DECLARED
  (`ansible_ssh_private_key_file: ~/.ssh/hyperstack_2026` in
  common_vars, a committable path) + `IdentitiesOnly=yes` (only
  that key offered) + TOFU (`StrictHostKeyChecking=accept-new`)
  + project-scoped known_hosts (`~/.config/zombie-radio/
  known_hosts`; recycled-IP failure → delete the file, rerun).
  No human ever ssh-logs-into a fresh box. Placement was
  RELITIGATED: all in common_vars (not 99-cloud) — identity and
  its enforcement live together.
- **Makefile evolution**: `ssh-tunnel ENV=x` (no hardcoded
  cloud) · `ensure_control_dirs` shared fragment ·
  `ZR_CONF_DIR` spelled explicitly (owner readability ruling
  over awk extraction — deliberately redundant with
  `zr_control_dir`, keep in sync) · **`ans-set ENV=x IP=y` /
  `ans-unset ENV=x`** wire/unwire hosts.yml (sed in, git-restore
  out, byte-identical round trip; refuses double-wiring).
- **The never-commit hook now has THREE production catches, all
  against the agent**: two live IPs, and — best of all — the
  literal marker string in a Makefile COMMENT (prose mention, no
  placeholder → blocked; reworded to "never-commit hook").
  Convention: outside markdown, never write the marker verbatim
  unless you mean it. Hook mechanics: a marked line commits only
  while REPLACE_ME precedes the marker on the SAME line;
  index-only scan; excludes `*.md` and `.githooks/*`.
- **`/props` residual RESOLVED**: llama-server default
  `repeat_penalty: 1.0` (off) — the penalty-vs-"Over." worry is
  moot without a fork. Full server defaults banked in the
  arc-plan journal (temp 0.8, top_k 40, top_p 0.95, min_p 0.05,
  DRY off, mirostat off).
- **Task 7b — `deploy/ansible/client-talkwithme-mac.yml`** built
  and PROVEN (PR #5): one self-contained inventory-free playbook
  (`make client-mac`), upstream TalkWithMe pinned at tag **7.1**
  (tags carry NO v prefix — scorbo2 house style, verified twice
  now across both his projects), plain venv+pip (no uv — the
  deliberate, recorded exception so it stays upstream-offerable),
  create-if-absent for settings.yaml and each Personas/<Name>/
  (verified by tamper test), placeholder-voice factory automated
  (say/afconvert, LEI16@24000), no supervisor. **Write-time
  discovery: upstream gitignores BOTH settings.yaml AND
  Personas/** — a fresh clone has neither, the seeding is
  load-bearing. Proof battery: fresh install changed=8 →
  idempotent changed=0 → user edits survive re-runs → app boots,
  serves 200.
- **Hyperstack box-birth ritual** (survey §S2, owner-dictated):
  console → Networking "Attach a public IP" → Firewall "Enable
  SSH Access" → "Enable ICMP Access" → ping + optional hardware
  eyeball. Then `make ans-set ENV=cloud IP=<ip>` and deploy. No
  manual host-key step anymore.

## 6. The machinery cheat-sheet (what the fresh agent will operate)

- `make install` (uv sync + arms the hook) · `make ans-deps` ·
  `make ans-set ENV=cloud IP=<ip>` · `make ans-deploy ENV=cloud`
  (logs to `~/.config/zombie-radio/logs/`) · re-run must be
  **changed=0** (converge invariant — any drift is a role bug,
  never shrug it off) · `make ssh-tunnel ENV=cloud` (own
  terminal) · `make check` (three ok lines through the tunnel) ·
  `make ans-unset ENV=cloud` when the box dies ·
  `make ans-lint` (MUST stay clean at the `production` profile) ·
  `make ans-check-syntax ENV=x` · `make client-mac`.
- Ansible doctrine in one breath: one play `hosts: all`,
  play-level `become` (roles assume root; `become_user` pairs
  mark exceptions); control-node preflights BEFORE facts;
  environments-not-groups inventories (cloud/, local/) with
  00-common symlink + 99-env overrides + reserved vault slots;
  service-shaped groups + SELF-GATING roles
  (`<role>_enabled: "{{ '<role>' in group_names }}"`);
  role-variable indirection (tasks speak `<role>_*`; defaults map
  to `zr_*` = the dependency manifest); NO tags; block YAML only.
- Box facts: pinned image posture (newest MATURE driver branch;
  R570 CUDA 12.8 preferred, R550 proven, never cross a CUDA
  major casually); A6000 48 GB = CANADA-1 = ~58–64 ms RTT,
  $0.50/hr; trio idles ~12.3/48 GiB; first deploy ~15 min
  (~11 GB models); reboot auto-rise <1 min; never hibernate;
  on-demand only for shows.
- Harness quirk: ansible/make commands run by the agent need
  stdio redirection to a scratchpad log file
  (`>"$LOG" 2>&1 </dev/null`) — Ansible refuses the harness's
  non-blocking stdio otherwise.

## 7. THE NEW TASK — "Task 6 reconnaissance brief" (owner-ratified 2026-09-21, tremendously important)

Before any Task 6 development, the agent produces a
**reconnaissance brief**: a guided tour of the fork-relevant
anatomy of TalkWithMe (plus its seams to tts-serve and to the
owner's 2024 defunct narration project), so the owner's own
three-codebase study starts oriented and the fork's shape round
argues from receipts. Not yet in TODO.md — **first paperwork of
the new session: a quick shape round for this brief, then add it
to TODO** (owner already green-lit the idea in principle; he was
interrupted saying yes by a session-guardrail failure).

Scope the brief should propose (shape round refines it):

1. **The server-side reply path, file:line** — where persona
   replies are generated, persisted, and fed to TTS; the exact
   insertion point for the `[Name]:` sanitizer; WHY server-side
   is presumptive (it also cleans the transcript that re-enters
   context — taxonomy C3 win). Known anchors from the 09-18
   source audit (verify against 7.1 — the pristine clone at
   `~/TalkWithMe-client` is ideal): `app/services/llm.py:75-76`
   (persona payload sends ONLY max_tokens + temperature),
   `llm.py:121-135` (`chat_completion`, router temp 0.1 /
   16 tokens), `app/routers/chat.py:98-124` (`_pick_persona` —
   "LLM decides" routes only the FIRST speaker),
   `chat.py:254-261` (followers are `random.choice` = taxonomy
   E1), `settings.yaml` wins over `app/config.py` defaults.
2. **`static/tts.js`** — the per-sentence splitter the max-chars
   accumulator replaces; the enqueue pipeline (relevant to the
   vanished-response watch item); where N-chars becomes a
   settings knob.
3. **Settings plumbing** — how a new knob travels
   settings.yaml → config → UI, so the accumulator's N and any
   sanitizer toggle land as proper settings.
4. **Seams for the narration future** — where a director loop
   would attach (router/follower code, room/turn model), mapped
   against spec §5.3's open design and the 2024 project's
   entropy-terms trick (spec §5.1 names it the baseline). The
   director is NEXT arc's design work — the brief only maps the
   seams, it does not design.
5. **Upstreamability audit** — how to keep the two patches
   separable, minimal, and offerable (strategy doc §4).

Deliverable form (proposal): a discussion doc
`2026-09-21-task6-reconnaissance-brief.md` (or dated as
written), every claim with a file:line receipt against tag 7.1.
Method note: READ the actual code; the anchors above are from a
9-day-old audit of an unpinned checkout — verify, never trust.

## 8. Paste-ready re-orientation prompt (for the FIRST message of the new session)

```
We are resuming the Zombie-Radio project (MVP-prototype arc) in a
FRESH session after the previous one ended. Nothing from that
session persists except the repo, your memory files, and the
handoff document written for you. Re-orient now:

1. Read docs/discussions/2026-09-21-mvp-arc-session-handoff.md
   IN FULL — it is your session memory bank: who I am and how we
   work (§0 is binding), project + arc state, the task board,
   the freshest science, and your first task (§7, the Task 6
   reconnaissance brief).
2. Follow its cold-start reading order (§4) as far as needed to
   confirm state — at minimum: docs/TODO.md, the arc-plan doc's
   2026-09-19 entry + addenda, and `git log --oneline -5`. Work
   continues on the already-created branch
   `alfre2v/task6-recon-brief` (verify you are on it; never
   create a new branch).
3. Then confirm to me in a compact summary: where the arc
   stands, the execution order ahead, the Task 6 reconnaissance
   brief's proposed scope (your §7 shape proposal — I will rule
   on it before you write anything), and the collaboration rules
   you will operate under.

Do not start any work until I confirm your summary. My standing
rules: strict review-before-commit (I review uncommitted changes
in VS Code — no diffs in chat, no commits without my explicit
word), no AI attribution anywhere, no side panes, minimal code
comments, discussion-first shape rounds, pushback with receipts
welcome.
```

## 9. Small print the next agent should not miss

- The deadline math: 2026-10-08 is ~17 days out. The critical
  path is the OWNER's Task 4 (bibles, samples); agent-side work
  (recon brief, fork, 5c support, canned episode) fits around it.
  If prioritization is ever unclear, ask him — do not guess.
- 5c needs NO cast and NO code — if a box is up and an evening
  is free, it is the cheapest science available.
- The spec is a LEDGER (inversion guardrail 3): every settled
  decision gets its as-built entry within a session. When in
  doubt whether something is "spec-worthy," ask.
- Experiment PRs (5a/5b/5c) trigger the MassedCompute reminder
  (memory file: parked provider, 50% code idea) — surface it
  gently after each such merge.
- The owner destroyed boxes are DISPOSABLE by doctrine: rebuild
  is one command + ~15 min. Never argue for keeping a box alive
  on rebuild-cost grounds.
- Fresh-path doctrine: no in-place downgrades in venvs — delete
  and reconverge (the fresh path IS the product).
- LuxTTS: a new tts-serve engine the owner flagged (less VRAM,
  ~1 GB claim) — 5b's first check; F5-TTS/Breeze upstream-PR
  ideas weakened accordingly (follow-ups.md).
- The 2024 defunct project: the owner's prior narration attempt
  (entropy-terms steering, spec §5.1). He is re-reading it
  himself; the recon brief maps TalkWithMe's seams to it, no
  more.
- Handoff hygiene at session close (Task 8 or earlier): ask
  permission to delete BOTH `2026-09-19-mvp-arc-handoff.md` and
  this file.
