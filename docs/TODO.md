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

- [x] **Task 1 — Deployment machinery v1 (deliverable D1).**
  DONE (2026-09-18, ~1.5 days of the 3-day timebox): all four
  roles written; **proven live on a fresh A6000/R570 box** — full
  stack from zero, one command, idempotent (changed=0); potholes
  fixed in-role and journaled ([discussion 2026-09-18] arc-plan);
  NEVER_COMMIT tripwire armed. **D2 acceptance MET the same day**
  (4 distinct voices + mic loop on the deployed stack; 58 ms
  CANADA-1 RTT, "almost natural" pauses). Remaining to close:
  - [x] Reboot test PASSED (2026-09-18): full unattended
    auto-rise in under a minute; client reconnected on a fresh
    tunnel alone.
  - [x] `runbooks/service-restart-sequence.md` rewritten around
    the playbook (ruling-2 executed, 2026-09-18).
  - [x] `deploy/ansible/README.md` written (2026-09-18).
  - [x] Owner call RESOLVED (2026-09-18): destroying soon —
    boxes are disposable now; rebuild is a proven ~15-min
    command. (When destroyed: restore the hosts.yml sentinel —
    the working tree goes clean by itself.)
- [x] **Task 2 — Laptop client wiring + smoke gate.** DONE
  2026-09-18: tunnel to the new box, `make check` three-ok,
  TalkWithMe smoke passed, saved server config carried over
  unchanged (same localhost ports as the experiment).
- [x] **Task 3 — Cheap config wins, BEFORE experimenting.** DONE
  (2026-09-18):
  - [x] `max_turns_for_context` raised 6→50 (owner, 2026-09-18)
    — and the C9 retest PASSED with it: keyword recall works;
    coherence otherwise unchanged (see taxonomy evidence ledger).
  - [x] Fresh rooms, Global System Prompt cleared — standing
    practice since lab3.
  - [x] Sampler params read (taxonomy D1, source audit — no box
    needed): persona requests send ONLY max_tokens (live: 200, UI-editable) +
    temperature (live: 0.8); everything else is llama-server
    defaults; router uses temp 0.1. Residual RESOLVED
    (2026-09-19, /props on the R550 box): `repeat_penalty: 1.0`
    = off — the penalty-vs-"Over." worry is moot without a fork
    ([discussion 2026-09-18] arc-plan journal has the full
    defaults).
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
- [ ] **Task 6 — First patches, on trigger.** **TRIGGER FIRED
  2026-09-18**: labels are back in show output and SPOKEN (no
  Global System Prompt per lab3) → the sanitizer is required →
  the fork moment arrived. Disposition ([discussion 2026-09-18]
  arc-plan, Q1): fork thin, patch minimally (sanitizer +
  max-chars accumulator — the accumulator now triply motivated,
  incl. the ultra-short-input echo artifact), offer both
  upstream. Executes after Task 1 closes.
  - [ ] **Reconnaissance brief FIRST** (owner-ratified
    2026-09-21; branch `alfre2v/task6-recon-brief`): a guided
    tour of the fork-relevant anatomy of TalkWithMe (tag 7.1),
    the tts-serve seam (tag 1.2), and the 2024 `zombie_radio_ai`
    prototype — every claim with a file:line receipt. Four
    units, each its own deliverable, dialog-driven: (1) the
    TalkWithMe tour · (2) the tts-serve contract-and-extension-
    points tour · (3) synthesis resolving the seam-question
    ledger (S1, S2, …) · (4) the 2024 prototype integration
    pass. Umbrella doc
    `discussions/2026-09-21-task6-reconnaissance-brief.md` + one
    tour doc per project; HTML derivatives (diagrams, annotated
    excerpts, VS Code deep links) under
    `visuals/task6-reconnaissance-brief/`. Unit 1 alone unblocks
    the fork. Shape, method, cadence: [discussion 2026-09-18]
    arc-plan Task notes.
- [ ] **Task 7 — The canned episode (owner MUST) + demo-day
  protocol runbook.** Recorded from the working prototype; the
  runbook promotion deferred from the last arc lands here.
- [x] **Task 7b — `client-talkwithme-mac.yml`: standalone Mac client-install
  playbook (tangential nice-to-have; NOT MVP).** DONE 2026-09-19
  (branch `alfre2v/client-talkwithme-mac`): built to every
  constraint below and proven on the Mac — fresh install
  (TalkWithMe pinned `7.1` = the exact proven client version;
  upstream tags carry no v prefix, verified), idempotent re-run
  changed=0, create-if-absent verified by tamper test
  (settings.yaml + persona edits survive), app boots and serves
  200 from the fresh install. `make client-mac` wraps it.
  Findings + final shape: [discussion 2026-09-18] arc-plan
  journal, entry 2026-09-19. Original scope kept for the record: A top-level
  playbook (reserved-slots pattern) that installs the TalkWithMe
  client on the Mac laptop, assuming the cloud backend.
  **Hard separation, stressed:** totally separate from site.yml —
  run with NO `-i`, hosts: localhost inline; it must never read,
  reference, or touch the deployment inventories in any way (the
  EW `lab.yml` precedent: deliberately inventory-free).
  Scope: clone (the fork, once it exists) + venv + requirements +
  settings template (tunnel ports) + **the placeholder-voice
  factory automated** — the `say`/`afconvert` blocks from the
  experiment's `placeholder-personas.md` — so the synthetic cast
  arrives with audio, resolving the audio-fragments caveat; the
  REAL cast stays manual (never-committed samples,
  private-assets-dir variable). No supervisor: uvicorn by hand at
  showtime. **REORDERED BEFORE Task 6 (owner, 2026-09-19): built
  first AGAINST UPSTREAM TalkWithMe** — the deploy machinery may
  interest scorbo2 as a contribution, so demonstrate it on the
  upstream repo; `client_repo`/`client_version` play vars make it
  fork-agnostic (the old fork dependency is dissolved, not
  deferred). **NEXT UP in execution order; upstream OUTREACH
  deferred past the deadline (owner, 2026-09-19) — build
  offerable, contact nobody yet.** Contribution-shaped
  constraints: plain venv+pip (no
  uv imposed), never clobber existing settings.yaml/Personas
  (create-if-absent), clone dir is a variable so upstream and the
  future fork can coexist. ([discussion 2026-09-18] arc-plan Q3 +
  Task-notes.)
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
