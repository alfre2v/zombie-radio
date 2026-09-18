# TODO — MVP prototype arc

**Arc:** MVP prototype · **Started:** 2026-09-17 ·
**Opening branch:** `alfre2v/mvp-prototype-arc-open`
**Governing decisions:** the prototype-first inversion
([discussion 2026-09-16]) and the deployment-first ruling
([discussion 2026-09-17]): the prototype is the experiment
platform, and the deployment machinery is deliverable #1.
**Spec:** `specs/product-definition.md` continues as the living
LEDGER (inversion guardrail 3) — as-built entries land within a
session of each settled decision; no new spec for this arc.

**Deliverables:** **D1** — deployment machinery (Ansible +
Docker, cloud VM ≡ localhost) · **D2** — the running prototype
(the spike's configuration as a product, real cast).
**Acceptance:** a full 4-persona session runs on a stack stood
up ENTIRELY by the playbook — machinery proven end-to-end, not
curl-deep · **D3** — the in-prototype experiment verdicts (LLM
default, two TTS engines, Whisper size, VRAM budget).

**NOT in this arc (deliberate boundary, 2026-09-17):** the
ensemble-director design ([spec §5.3]), story/episode authoring,
and the full demo rehearsal — that is the next arc's material
("the show arc"), shaped by what this prototype teaches. This
arc builds the platform, picks the components, and patches the
worst rough edges.

**Parallelism note:** Task 4 (the owner's cast work) has ZERO
dependency on Tasks 1–3 — it is the long pole and can start
immediately, any day, box or no box.

**Notation recap** (full conventions in [docs/README.md](README.md)):
`[ ]` open · `[x]` done (with commit SHA in parentheses) · `[~]`
re-scoped/moved to another arc (says where) · `Task N` is a
sub-step here, never a PR number · cite discussions as
`[discussion YYYY-MM-DD]`, specs as `[spec §X.Y]`.

*This file is the living parking-lot table of the task landscape
(owner convention, 2026-09-16): updated at every execution or
decision; the re-orientation surface when revisiting any topic.*

## Owner action queue

*Actions only the owner can take. Items get DELETED when done;
the agent keeps this current. These carry across arcs.*

1. **Gather 4 reference voice samples** — EXECUTING SOON.
   Famous-actor movie clips likely → **NEVER committed to the
   repo** (gitignore before the first file; hygiene entry +
   voice-isolation-tool search in follow-ups.md). Unblocks
   Task 5b.
2. **Seed the character bibles** — EXECUTING SOON. Names,
   personalities, quirks, voice descriptions; rough is fine;
   model-neutral (guardrail 2). Unblocks Task 5a.
3. **Check the home 3090 box's NVIDIA driver** — DEPRIORITIZED
   (cloud-only demo), but note: it partially revives the day we
   test the playbook's localhost target ([discussion 2026-09-17]
   ruling 4).
4. **Demo-day logistics radar** — POSTPONED until the MVP works.
   Pre-decided: the **"canned episode" emergency mode is a
   MUST** (Task 7).

## Sub-steps

- [ ] **Task 1 — Deployment machinery v1 (deliverable D1).**
  **TIMEBOX: started 2026-09-17 ~17:30 → abort by end of
  2026-09-20** ([discussion 2026-09-17] ruling 1). Skeleton
  committed (site.yml + preflights + inventories + base role +
  Makefile; llama/tts_engine/whisper roles stubbed). NEXT: install
  Ansible on the laptop (owner: brew/pipx) → syntax checks →
  write the three service roles → live debug on a fresh R570 box. Playbook-first, debugged
  live against a fresh R570 box; source material = the sealed
  Reproduction recipe (R0–R13). Boundary (owner ruling
  2026-09-17): the playbook starts at "SSH-able **Ubuntu** box
  exists" — VM provisioning stays manual/console; assuming
  Ubuntu everywhere is a named portability bet (safe across most
  GPU providers).
  - [ ] `deploy/` skeleton in THIS repo (ruling 3): playbook,
    roles, example inventory; real inventory/host_vars
    gitignored.
  - [ ] **One role per service** (owner ruling 2026-09-17):
    `base` · `llama` (canonical v3 command as template) ·
    `tts_engine` (**parametrized** — engine name/launch line are
    variables) · `whisper`. Idempotent re-runs.
  - [ ] Two targets: cloud VM (Hyperstack R570 image) +
    `delegate_to: localhost` (BUILT now, TESTED later — ruling
    4).
  - [ ] First live run against a fresh R570 box = the image
    validation run; deltas amend the playbook in place.
  - [ ] On first success: rewrite
    `runbooks/service-restart-sequence.md` to point at the
    playbook (single source of truth — ruling 2).
- [ ] **Task 2 — Laptop client wiring + smoke gate.** TalkWithMe
  on the Mac (manual — the Mac client is OUT of Ansible v1
  scope): tunnel to the new box, server URLs, the
  text→voice→mic smoke gate. Mostly recipe R7–R13.
- [ ] **Task 3 — Cheap config wins, BEFORE experimenting.** So
  every experiment measures the improved baseline, not known
  defects: raise `max_turns_for_context` from 6 (taxonomy C9) ·
  fresh rooms, Global System Prompt cleared (lab3 lesson) · read
  the sampler params TalkWithMe sends (taxonomy D1, never done).
- [ ] **Task 4 — Real cast replaces placeholders.** Character
  bibles → the four `Personas/<Name>/prompt.md` (keep
  `/no_think` while on Nemotron; no heavy prompt tuning yet —
  guardrail 2) · voice samples → isolation tool first
  (follow-ups) → gitignore → replace the `say`-generated
  ref.wavs.
- [ ] **Task 5 — In-prototype experiments (deliverable D3;
  protocol skeleton per guardrail 1: question, timebox,
  pre-registered pick criteria, runlog).**
  - [ ] **5a — LLM audition** ([spec §7.3]): the ranked five via
    one `-hf` flag each; identical scenario; scored on BOTH
    narrative-health axes; name-memory retest at the raised
    window. Picks the working default. Needs Task 4 bibles.
  - [ ] **5b — TTS comparison + VRAM budget** ([spec §7.2]):
    engines via the parametrized role; **LuxTTS's ~1 GB claim is
    the first check**; picks two engines + Whisper size;
    measures the two-engine stack vs 24 GB target / 16 GB
    aspiration. Needs Task 4 samples.
  - [ ] **5c — Narrative-health probe battery**
    ([discussion 2026-09-16] taxonomy §5): the zero-code,
    owner-run probes — `[Director]:` prefix (C6) · named
    addressee (E2) · in-fiction phrasing (C8) · long-form escape
    hatch (B4) · fixed responder (E1) — one variable flipped per
    run against the same two-round protocol. Protocol-lite (a
    dated runlog section, no full experiment folder). Runnable
    as soon as Task 2 completes — does NOT need the real cast;
    findings feed prompt and config choices before 5a.
- [ ] **Task 6 — First patches, on trigger.** The `[Name]:`
  output sanitizer (fires on label contamination) · the
  max-chars accumulator in `static/tts.js`. The first one
  required decides fork-vs-upstream with data (fork strategy).
- [ ] **Task 7 — The canned episode (owner MUST) + demo-day
  protocol runbook.** Recorded from the working prototype; the
  runbook promotion deferred from the last arc lands here.
- [ ] **Task 8 — Close ritual in the closing PR.** Features
  Shipped entry · task_history migration · TODO reset ·
  staleness sweep (CLAUDE.md included) · spec ledger audit
  (every settled decision has its as-built entry).

## Standing cross-arc notes

- Hard deadline **2026-10-08** (hackTNT 2026): ~3 weeks out at
  arc open; the prototype is the critical path, and D1's 3-day
  timebox is its first checkpoint.
- Keep the last 2–3 branches, local and remote (owner rule,
  2026-09-16).
- Ops rules that carry over: never hibernate a show box · pinned
  image `R570 CUDA 12.8 with Docker`, Ubuntu 24.04 · on-demand,
  never spot · destroy-vs-keep is a per-evening cost call.
