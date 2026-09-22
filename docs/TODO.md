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
**Boundary shifted (owner ruling 2026-09-21, after the Task 6
reconnaissance):** two design decisions that belong to the
director's design are pulled INTO this arc because no source
patch can be shaped without them — (1) the **prompt structure**
sent to the LLM each turn (TalkWithMe's one-request-per-persona
with `[Name]:` history rewrite, versus a 2024-style single shared
context with a hidden narrator, versus a third structure not yet
thought of), and (2) the **story loop** (how to make the show
keep turning inside TalkWithMe's "one user message → up to four
replies → stop" design, given the app has no server-initiated
channel to the browser). Each gets its own discussion doc; the
next arc BUILDS on the two decisions instead of taking them.
**(1) DIRECTION ADOPTED 2026-09-21** — [discussion 2026-09-21]
prompt-structure: one shared context in screenplay form, code
director + per-round GBNF grammar (speaker allowlist, line
budget), one streamed request per round, SSE events synthesized
per parsed line; the sanitizer patch is dropped by construction.
Gate before final: two on-box confirmations (grammar + streaming
curl; per-round latency vs per-persona) and one audition item
(prose quality with/without the grammar). **(2) DECIDED
2026-09-21** — [discussion 2026-09-21] story-loop: the browser is
the metronome (a `/show` page with `show.js` requests the next
round when the audio queues drain), the server is the director
(`POST /api/show/round`); endless loop with interaction beats on a
randomized, configurable TIME window (min/max seconds of played
audio, never a round count — owner pushback); half-duplex
hold-to-talk mic enabled only in the listening state; prefetch is
day-three polish; dead-air static is needed the day the cadence is
tuned.
Both gating decisions are now taken; the fork may be created.

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
   Task 5b. **Spec confirmed 2026-09-22 (recon brief Q5):** about
   10 seconds of clean speech per actor — no music or crosstalk
   under the voice — plus an EXACT transcript per clip (covers both
   candidate engines: ours requires the transcript and ≥2 s;
   LuxTTS needs no transcript, ≥3 s, ~10 s clones best). Whisper on
   the box can draft the transcripts. A second clip per actor in
   another emotional register is optional until stage directions
   are wired to clip selection.
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
  **Disposition REVISED (owner ruling 2026-09-21, after the
  reconnaissance breadth pass):** we do NOT stay close to
  upstream. The clone becomes a NEW app, **TalkWithZombies** — a
  real GitHub fork of scorbo2/TalkWithMe at tag 7.1 (provenance
  and the MIT attribution kept; "forked from" labeled
  prominently in our README once forked), then modified as we
  please with no upstream-compatibility pretence. The two patches
  are now GATED on the two design discussions above: the
  **sanitizer's fate depends on the prompt structure** (its cause
  is the `[Name]:` history rewrite in `app/session.py:156-161`; a
  2024-style shared context turns the label into wire protocol
  and the sanitizer into a parser), while the **accumulator is
  design-independent** and may proceed any time. Contribution
  candidates re-ranked: the deployment machinery (site.yml + the
  Mac client installer) is the thing scorbo2 may want to adopt or
  advertise; the accumulator is the only plausible app-code
  patch; the sanitizer is no longer a candidate. Outreach still
  deferred past the deadline. Recorded in [discussion 2026-09-19]
  upstream-contribution-strategy (addendum) and [discussion
  2026-09-21] task6-reconnaissance-brief §1–§2.
  **REPOSITORY LAYOUT (owner decision 2026-09-21): two sibling
  repositories.** `zombie-radio` stays the deployment and
  documentation repo (the memory of record); `TalkWithZombies` is
  a GitHub fork of scorbo2/TalkWithMe at tag 7.1, cloned beside
  the other sibling clones at
  `/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`. Glue:
  the Mac installer already takes `client_repo` /
  `client_version` / `client_dir` as variables
  (`deploy/ansible/client-talkwithme-mac.yml:16-18`) — flip them
  to the fork; ADD a pin for the fork tag the deployment was
  proven against (the `zr_tts_serve_version` pattern); add a short
  pointer section in the docs saying where each kind of document
  lives (design and decisions here; the app's feature docs and
  AGENTS.md there). Rejected: a git submodule (nested detached
  checkout, a second place recording the version, buys nothing at
  deploy time since the installer clones from GitHub anyway); a
  subtree merge (the app inside a docs/deployment repo, our hooks
  and lint over its files, subtree splits to push anything back);
  copying files without history (ruled out by the attribution
  commitment).
  **TIMEBOX (owner proposal + agent conditions, agreed
  2026-09-21): 3 days to execute the two axes — prompt structure
  and story loop — in the fork.** Modeled on D1's 3-day box
  (finished in ~1.5). Terms:
  - **Start trigger:** the moment TalkWithZombies is actually
    forked. Deliberation is NOT timed: both discussion docs
    (prompt structure, story loop) are finished and ruled on
    BEFORE the fork exists, so day one is not spent talking.
    Realistic fork date ≈ 2026-09-24 → checkpoint ≈ 2026-09-27,
    leaving ~11 days for 5a/5b/5c, Task 7, and Task 8, with
    Task 4 (owner) in parallel throughout — no slack for a second
    attempt.
  - **Exit criterion, judged on MECHANISM, not narrative
    quality:** TalkWithZombies runs an unattended loop of at least
    ten turns with the four placeholder personas; speakers chosen
    by the new structure, not at random; one audience interaction
    beat that opens the microphone and absorbs the reply;
    sentences accumulated, not split; on the deployed stack
    through the tunnel. Placeholder voices, dumb dialogue, and
    yaml-only knobs are acceptable. Whether the story is GOOD is
    Task 5a's question (a small model's behavior under the chosen
    prompt structure is an audition matter, not an engineering
    one).
  - **Midpoint checkpoint at day 1.5:** continue, scale down, or
    stop — decided explicitly, as in D1.
  - **Fallback if the box is missed:** TalkWithMe 7.1 as it stands
    plus the canned episode (Task 7) is still a demo; the failure
    mode is a less ambitious show, not no show.
  - **Caution recorded:** the story-loop decision may be the
    arc's largest single build depending on which placement wins
    (browser-side timer ≈ a day; a server push channel is more;
    external process + polling in between) — the story-loop
    discussion ranks the placements by BUILD COST as well as fit,
    so the box is set knowing what it contains.
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
    arc-plan Task notes. **State 2026-09-22:** units 1–2 toured;
    unit 4 delivered as the prompt-structure + story-loop
    discussions; answer pass complete (every S and Q ruled); HTML
    visuals DROPPED (owner). **Remaining: unit 3, the synthesis —
    must land before PR #6 closes** (owner reminder request).
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
