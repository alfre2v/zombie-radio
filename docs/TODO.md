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
(prose quality with/without the grammar). **GATE PASSED
2026-09-22; ADR-0003 ACCEPTED 2026-09-23** — see Task 6's gate
sub-item below. **(2) DECIDED
2026-09-21** — [discussion 2026-09-21] story-loop: the browser is
the metronome (a `/show` page with `show.js` requests the next
round when the audio queues drain), the server is the director
(`POST /api/show/round`); endless loop with interaction beats on a
randomized, configurable TIME window (min/max seconds of played
audio, never a round count — owner pushback); half-duplex
hold-to-talk mic enabled only in the listening state; prefetch is
day-three polish; dead-air static is needed the day the cadence is
tuned.
Both gating decisions are taken and the gate passed
(2026-09-22); the fork is next (Task 6a).

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
   model-neutral (guardrail 2). They become the sections of the
   show's cast sheet ([spec §5.3]). Unblocks Task 5a.
3. **Check the home 3090 box's NVIDIA driver** — DEPRIORITIZED
   (cloud-only demo), but note: it partially revives the day we
   test the playbook's localhost target ([discussion 2026-09-17]
   ruling 4).
4. **Demo-day logistics radar** — POSTPONED until the MVP works.
   Pre-decided: the **"canned episode" emergency mode is a
   MUST** (Task 7). Candidate on the radar: a tunnel that reconnects by
   itself (follow-ups, SSH keepalives — low priority).
5. **Decide on the emotion field for the fork** — measured
   2026-09-22 (0.5 % per token when taught, E1 PASS; the model
   used eight of nine emotions). The agent's lean: a yaml switch,
   default on, the parser stripping the tag before the TTS. Needed
   before Task 6b's grammar builder (follow-ups entry).
6. **The hibernated Hyperstack VM** (2026-09-22; its IP kept for a
   few cents an hour) — wake it for the next box session (`make
   ans-set ENV=cloud IP=…`, then the tunnel) or destroy it; a
   from-zero deploy takes about 7 minutes.

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
  bibles → the sections of TalkWithZombies' cast sheet ([spec
  §5.3]; where they live in the fork — the persona files or one
  cast file — is a Task 6b design choice), keeping `/no_think`
  while on Nemotron (the chat template needs it even under the
  grammar — [spec §4]); no heavy prompt tuning yet — guardrail 2 ·
  voice samples → isolation tool first (follow-ups) → gitignore →
  replace the `say`-generated ref.wavs in the persona
  directories.
- [ ] **Task 5 — In-prototype experiments (deliverable D3;
  protocol skeleton per guardrail 1: question, timebox,
  pre-registered pick criteria, runlog).**
  - [ ] **5a — LLM audition** ([spec §7.3]): the ranked five via
    one `-hf` flag each; identical scenario; scored on BOTH
    narrative-health axes; name-memory retest at the raised
    window. Picks the working default. Needs Task 4 bibles.
    **Runs in the fork's engine, after the timebox.** Added
    2026-09-23: does each candidate write the screenplay format on
    its own (if not, the grammar steers — ~10 % per token and style
    drift)? The gate's "prose with and without the grammar" item is
    answered for Nemotron by identity and re-checked for any other
    finalist; the bounded-scratchpad cell rides along
    (follow-ups).
  - [ ] **5b — TTS comparison + VRAM budget** ([spec §7.2]):
    engines via the parametrized role; **LuxTTS's ~1 GB claim is
    the first check**; picks two engines + Whisper size;
    measures the two-engine stack vs 24 GB target / 16 GB
    aspiration. Needs Task 4 samples. Per-engine test items from
    the field: ultra-short inputs (the "1." echo) and typographic
    punctuation (`’`/`—` dropped the pause before "Over." on Faster
    Qwen3-TTS, 2026-09-22 — the parser normalizes anyway).
  - [ ] **5c — Narrative-health probe battery**
    ([discussion 2026-09-16] taxonomy §5): the zero-code,
    owner-run probes — `[Director]:` prefix (C6) · named
    addressee (E2) · in-fiction phrasing (C8) · long-form escape
    hatch (B4) · fixed responder (E1) — one variable flipped per
    run against the same two-round protocol. Protocol-lite (a
    dated runlog section, no full experiment folder). Does NOT
    need the real cast. **Re-scoped 2026-09-23 to the fork's
    engine:** the battery was written against TalkWithMe's
    per-persona structure; under [ADR-0003] two probes are moot by
    construction (the `[Director]:` prefix — the director now IS
    the user turn; the fixed responder — the director picks the
    speakers), and the others (named addressee, in-fiction
    phrasing, long-form escape hatch) become director settings to
    try. Runs after Task 6b, alongside 5a.
- [ ] **Task 6 — The fork and the show engine: TalkWithZombies
  ([ADR-0002], [ADR-0003]).** *How it got here, in four steps:*
  - **2026-09-18 — the trigger fired:** labels were back in the
    show's output and SPOKEN (no Global System Prompt per lab3), so
    the first patch was required and the fork moment arrived. First
    disposition: fork thin, patch minimally (the `[Name]:`
    sanitizer + the max-chars accumulator), offer both upstream
    ([discussion 2026-09-18] arc-plan, Q1).
  - **2026-09-21 — the disposition revised** after the
    reconnaissance: no upstream-compatibility pretence — the clone
    becomes a NEW app, **TalkWithZombies**, a real GitHub fork of
    scorbo2/TalkWithMe at tag 7.1 with provenance and the MIT
    attribution kept and labeled ([ADR-0002]). Contribution
    candidates re-ranked: the deployment machinery (site.yml + the
    Mac client installer) first, the accumulator second, the
    sanitizer out; outreach deferred past the deadline
    ([discussion 2026-09-19] upstream-contribution-strategy
    addendum; [discussion 2026-09-21] task6-reconnaissance-brief
    §1–§2).
  - **2026-09-21 — the engine decided** ([ADR-0003]): one shared
    script, a director in code, a screenplay grammar, the browser
    as the clock. The sanitizer became moot by construction (no
    `[Name]:` label left to strip); the accumulator is built in the
    fork.
  - **2026-09-22/23 — the gate passed and ADR-0003 was accepted**
    (sub-item below). The fork (6a) is next.
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
    so the box is set knowing what it contains. *Resolved
    2026-09-21: Placement 1, the browser as the clock — the
    cheapest, about a day ([ADR-0003]).*
  - [x] **Reconnaissance brief FIRST** (`cfeed4d`, PR #6) (owner-ratified
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
    visuals DROPPED (owner). Unit 3, the synthesis, landed as the
    umbrella's §9 before PR #6 closed — the brief is complete.
  - [x] **ADR-0003 gate on a live box** (branch
    `alfre2v/adr-0003-gate`, 2026-09-22, Hyperstack A6000): **PASS**
    on both on-box items — the screenplay grammar streams and binds
    through the top-level `grammar` field of `/v1/chat/completions`;
    one shared script per round costs about a quarter of the
    per-persona structure's prompt time (reason corrected: a
    host-RAM prompt cache rescues per-persona prompts, which pay
    instead in state swaps and a per-request toll); the grammar costs
    0.3 % per token. The audition item was answered for this model by
    identity (same prompt and seed → the same text with and without
    the grammar, 20 of 20 rounds). A second run measured an
    `(emotion)` tag: 0.5 % per token when taught, 10.4 % when forced
    (E1 PASS; adoption is the owner's call, follow-ups). **ADR-0003
    accepted 2026-09-23** (Validation section). Records:
    `experiments/2026-09-22-adr-0003-gate/`,
    `experiments/2026-09-22-emotion-grammar-cost/`; lessons:
    [discussion 2026-09-22] grammar-and-prompt-cache-lessons.
    Deployment by-products: tts-serve pin 1.2 proven; the base
    role's apt lock wait bounded with a clear error (`9fbbeb3`).
  - [ ] **6a — Fork TalkWithZombies ([ADR-0002]), about an hour.
    NEXT.**
    - *Why:* the engine is built in our own app, free to diverge;
      the 3-day timebox starts the moment the fork exists.
    - *Steps:*
      1. Fork scorbo2/TalkWithMe on GitHub as
         **TalkWithZombies** (the owner's account — an outward-facing
         action, done by the owner or with his explicit go), based
         at tag 7.1.
      2. README: a prominent "forked from TalkWithMe by Steve
         Corbett (scorbo2)" section; the MIT notice kept (owner: "I
         will always pay respect and attribution to upstream").
      3. Clone to `/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`.
      4. In this repository: point the Mac installer's
         `client_repo` / `client_version` / `client_dir` at the fork
         (`deploy/ansible/client-talkwithme-mac.yml:16-18`); add a
         pin variable for the fork tag the deployment was proven
         against (the `zr_tts_serve_version` pattern); add the docs
         pointer section (design and decisions here; the app's
         feature docs and AGENTS.md there). Installer proof: fresh
         install, re-run `changed=0`, the app boots.
      5. Disable, do not delete: `allow_tool_calls` false on every
         persona, `enable_persona_memories` false.
      6. The fork's `AGENTS.md` (upstream ships one) gains our house
         rules — no AI attribution anywhere, minimal code comments,
         absolute paths for files in sibling clones, the suite green
         before review, review before every commit. Any agent that
         opens the fork in a harness that reads `AGENTS.md` gets
         them — a fresh session of the lead first of all, and any
         parallel harness if delegation is ever switched on.
    - *Done when:* the fork exists with its provenance labeled, the
      installer installs it (proven), and the timebox clock is
      running.
    - *Acceptance:* `gh repo view alfre2v/TalkWithZombies` names
      scorbo2/TalkWithMe as its parent; the README's "forked from"
      section and the unchanged MIT `LICENSE` are on the default
      branch; `make client-mac` from a clean state installs the fork
      at its pinned tag, a re-run reports `changed=0`, and the app
      answers HTTP 200. *Delegable later:* the installer variables
      and the pin (step 4) — yes; the fork itself and its README —
      no (outward-facing, the owner's).
  - [ ] **6b — Build the show engine (the 3-day timebox; the clock
    starts when 6a is done).** Design: [spec §5.3], [ADR-0003] and
    its Validation section; the lessons behind the rules marked
    (L): [discussion 2026-09-22] grammar-and-prompt-cache-lessons.
    **Delegation: OFF** (owner ruling 2026-09-23 — this work stays
    in the tight learning loop; the method is recorded in
    `docs/README.md` for later). The acceptance checks at the end
    serve our own work now.
    - *Server side (Python, in the fork):*
      - **Script assembler** replacing `build_llm_messages`
        (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/session.py:123`):
        `system` = the cast sheet; history = alternating director
        directives and script lines; the model's lines written back
        as parsed and normalized (costs no cache — L §2.8).
      - **The code director:** beat, speaker allowlist, line
        budget, stage direction, entropy terms, and the
        interaction-beat cadence measured in played seconds. **It
        states in words every constraint it puts in the grammar**
        (L §4.2 — a grammar that disagrees with its prompt costs
        ~10 % per token and drifts the style); the line budget is
        enforced by the grammar's bound, since "up to N" is read as
        N (L §2.6).
      - **Grammar builder:** allowlist → `speaker` alternatives;
        budget → `line{1,N}`; square brackets out of `text`; the
        optional `(emotion)` rule behind a yaml switch (the owner
        decides adoption — action queue).
      - **One streamed request per round** with the grammar in the
        top-level `grammar` field, one more key in `_base_payload`
        (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/services/llm.py:69`).
      - **Stream parser:** `start` / `token` / `done` / `complete`
        per script line; trims trailing whitespace; strips the
        emotion tag before the TTS but keeps it in the history;
        **normalizes typographic punctuation before the TTS**
        (`’‘` → `'`, `“”` → `"`, `—` → `, `, `…` → `...` — required,
        L §4.6); tolerates a line wrapped in quotation marks.
      - **`POST /api/show/round`**, a sibling of `_chat_stream`
        (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/routers/chat.py:208`):
        takes the room and an optional audience transcript, which
        enters the directive as in-fiction radio traffic; empty or
        low-confidence transcripts are dropped at the STT proxy
        (the "No response received from STT server" pitfall —
        [discussion 2026-09-21] story-loop §6).
      - **Debug switch:** save the rendered prompt next to each
        round's messages — `/apply-template` if this llama.cpp
        build has it (verify first), otherwise the server's verbose
        log — and log the grammar in full, not a summary (L §4.9).
      - **Tests in upstream's style:** a test class feeding a
        scripted token stream, asserting the events, the persisted
        lines and the normalizer's mapping.
    - *Browser side (JavaScript, in the fork):*
      - A new `/show` page with its own template including
        `state.js`, `tts.js`, `stt.js`, `persistence.js`, plus a new
        `show.js`: idle → generating → playing → listening; the
        next round requested when the audio queues drain
        ([discussion 2026-09-21] story-loop §5); listening only
        when the director asked.
      - **Hold-to-talk** replacing the toggle, enabled only in the
        listening state.
      - **The accumulator** in `tts.js` with the ruled rules (about
        100 characters, whole sentences, ~20 % tail tolerance, a
        hard flush at each line end — [discussion 2026-09-21]
        task6-recon-talkwithme, around line 617).
      - The SSE reader extracted from `sendMessage`
        (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/chat.js:135-159`)
        into a shared function.
    - *Configuration:* all knobs yaml-only — a `show:` section
      (cadence minimum and maximum in played seconds, the listening
      window, the emotion switch); the accumulator's limit and
      tolerance next to `tts.streaming`. No dialogs.
    - *Operating notes (measured 2026-09-22):* one conversation per
      server slot — keep the chat UI off the show's server during
      show runs; a round that meets a slot holding another
      conversation first pays a state swap (~1.8 s).
    - *Day-three polish, only if the midpoint checkpoint is green:*
      prefetch round N+1 when the last line of N starts playing;
      dead-air static through a second AudioContext source while a
      round is in flight; the 1930s radio look.
    - *Acceptance checks, item by item* (with the "delegable later"
      mark — a knob for the future, not in use):
      - **Script assembler** — a unit test: for a room's history,
        the messages are the cast sheet, then alternating directive
        and script turns, and no `[Name]:` appears anywhere.
        *Delegable later: yes.*
      - **Code director** — unit tests: the round's allowlist and
        line budget appear both in the directive's words and in the
        grammar; with a seeded random source, no interaction beat
        before the minimum played seconds and always one after the
        maximum. *Delegable later: no* (design-heavy).
      - **Grammar builder** — unit tests: the exact GBNF text for a
        given allowlist and budget, with the emotion switch on and
        off; then, on a box, one control request (only a name absent
        from the prompt allowed) that must come back in that name
        alone. *Delegable later: yes* (the box step stays with the
        lead).
      - **Streamed request** — a unit test: the payload carries the
        grammar as a top-level `grammar` key. *Delegable later: yes.*
      - **Stream parser and normalizer** — tests feeding scripted
        token streams: `start` / `token` / `done` / `complete` per
        line; trailing whitespace trimmed; the emotion tag stripped
        from what goes to the TTS and kept in the history; the
        punctuation mapping, character by character; a line wrapped
        in quotation marks handled. *Delegable later: yes* — the
        best first candidate.
      - **`POST /api/show/round`** — an API test with the LLM stream
        mocked: the expected SSE events; an empty or placeholder STT
        transcript dropped. *Delegable later: yes*, once the director
        exists.
      - **Debug switch** — switched on, each round leaves its rendered
        prompt (or the verbose log's) and the full grammar next to
        its messages. *Delegable later: yes.*
      - **`/show` page and `show.js`** — by hand in the browser: the
        states cycle, the next round is requested when the audio
        queues drain (visible in the console), listening only when
        the director asked. *Delegable later: no* (integration,
        judged by ear).
      - **Hold-to-talk** — by hand: the control is enabled only in
        the listening state. *Delegable later: no.*
      - **Accumulator** — "Dr. Byrne. 47. Microbiology. Over." leaves
        as one chunk; a 180-character sentence goes whole and alone;
        the line end always flushes; later the Node test of the
        follow-up "JavaScript test for the accumulator's packing
        rules". *Delegable later: yes*, once that test exists.
      - **SSE reader extraction** — the chat UI still works end to
        end, and upstream's Node tests stay green. *Delegable later:
        yes* (a mechanical refactor).
      - **yaml configuration** — the `show:` keys and the
        accumulator's limits are read, with defaults when absent (a
        unit test). *Delegable later: yes.*
      - **Every item:** the fork's pytest suite green before review.
    - *Done when:* the timebox's exit criterion above holds, on the
      deployed stack through the tunnel.
- [ ] **Task 7 — The canned episode (owner MUST) + demo-day
  protocol runbook.** Recorded from the working prototype; the
  runbook promotion deferred from the last arc lands here. The
  seed makes retakes reproducible: on one server slot, the same
  request and seed gave the same words 80 minutes apart
  (2026-09-22) — record with the settings it will be replayed
  with.
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
- Ops rules that carry over: never hibernate a show box · proven
  images: `R570 CUDA 12.8 with Docker` (Ubuntu 24.04, 2026-09-18)
  and `Ubuntu Server 22.04 LTS R550 CUDA 12.4 with Docker`
  (2026-09-19 and 2026-09-22) · a fresh box may spend its first
  hour in Ubuntu's own updater (the deploy now waits 5 minutes for
  the apt lock, then stops with a clear message) · on-demand,
  never spot · destroy-vs-keep is a per-evening cost call.
