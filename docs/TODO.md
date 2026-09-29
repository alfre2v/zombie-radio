# TODO — MVP prototype arc

**Arc:** MVP prototype · **Started:** 2026-09-17 ·
**Opening branch:** `alfre2v/mvp-prototype-arc-open`
**Governing decisions:** the prototype-first inversion
([discussion 2026-09-16]) and the deployment-first ruling
([discussion 2026-09-17]): the prototype is the experiment
platform, and the deployment machinery is deliverable #1.
**Spec:** `specs/product-definition.md` — since 2026-09-28 a linear
description of the product as built, rewritten in place when the
product changes (the owner: "The specification is not a log, it
should read as the guide to build the product."); until then it was
kept as a living ledger of as-built entries (inversion guardrail 3).
No new spec for this arc.

**Deliverables:** **D1** — deployment machinery (Ansible +
Docker, cloud VM ≡ localhost) · **D2** — the running prototype
(the spike's configuration as a product, real cast).
**Acceptance:** a full 4-persona session runs on a stack stood
up ENTIRELY by the playbook — machinery proven end-to-end, not
curl-deep · **D3** — the in-prototype experiment verdicts (LLM
default, two TTS engines, Whisper size, VRAM budget).

**Arc boundary, in one line:** the show engine's design was pulled
into this arc on 2026-09-21 and is now decided; story and episode
authoring and the full demo rehearsal stay with the next arc, "the
show arc". The full story of the boundary shift is under "Done in
this arc".

## Now — where the arc stands

*Updated 2026-09-28, night. Read this section first; everything below
it is detail.*

- **Task 6, the fork and the show engine, is done (2026-09-28).** The
  engine (6b) was built in the fork TalkWithZombies under a timebox —
  clock started 2026-09-23 14:46 CDT · checkpoint passed 2026-09-24
  ~18:57 (6 of 6 criteria; verdict: continue) · closed Monday
  2026-09-28 (the end the owner moved there on 2026-09-25; it was
  2026-09-26 14:46). Three slices: the skeleton
  (alfre2v/TalkWithZombies#2), the rules (#3), the browser (#4,
  `ca37199`) — the page with text and voices, the listener's turn,
  events worded for the broadcast (the owner: "B wins, flip the default
  and record it."), the exit criterion by ear (the owner: "It does what
  we planed. It is a success."), the listener's exchange (step 3.4c:
  Broadcast and Contact, [discussion 2026-09-26]
  show-director-modes), fixed lines, and the owner's sweep of every
  prompt the model receives ([discussion 2026-09-28] prompt-sweep; the
  owner's ruling, 13:14: invented details are a feature — the model's
  improvisation is what the project probes). The owner's last listen
  (run `2026-09-28T13-43-28`): "Wow, big improvement in story
  coherence… All in all I am satisfied with where we are." Released as
  the fork's `tz-0.2`; the installer pinned to it and re-proven by the
  owner ("All four checks pass, installed at tz-0.2."). The whole
  record, step by step, is under "Done in this arc", Task 6; the
  design, [discussion 2026-09-23] show-engine-design.
- **The show's looks, the same night — the fork's `tz-0.3`:** a
  chooser at `/show` (the root `/` opens it), two looks — `old-radio`
  on a photograph of a 1950 Philips Sirius, and
  `amateur-radio-transmitter` — with a live gauge, the plain page
  untouched, TalkWithMe's chat UI moved to `/talkwithme`
  (alfre2v/TalkWithZombies#5, merged as `0ec33c1`). The installer's pin
  to `tz-0.3` is this repository's #15, open; the owner's re-proof of
  the install is pending. Details under "Open tasks", Polish. How to
  drive the show: the fork's `docs/runbooks/show-page.md` (the page;
  "Choosing a look") and `docs/runbooks/show-driver.md` (no browser).
- **Next, in order:** Task 4's reference voices (the owner's) → the
  dead-air static (the polish's other item; the radio look is built)
  → Tasks 5a / 5b / 5c in the new engine (5a needs the character
  bibles, 5b the voices) → Task 7, the canned episode (a MUST for the
  talk) → Task 8, the close ritual. Hard deadline 2026-10-08; the talk
  at the Austin Python Meetup is in October 2026. **Among the show
  fixes before the talk:** names-only A — code states who the voice
  is (the owner's ruling, 2026-09-26; shaped and estimated in the
  follow-up "A listener memory keyed by identity"). Prefetch and
  episodes wait as post-timebox follow-ups, behind Task 4 and Task 7.
- **Task 4, split in two by the owner (2026-09-28):** the reference
  voices first — one clip per character with its exact transcript, in
  `~/TalkWithZombies-client/Personas/<Name>/` (owner action queue,
  item 1); the character bibles deferred ("I want to pivot to audio,
  which is the weak spot now.").
- **Follow-ups written 2026-09-28**, from the owner's listen of the
  installed `tz-0.2`: the trim's thresholds in settings; a context
  budget near the full 16k; a 32k context; a long silence between two
  lines of one round, not explained. Also that day: mood clips (several
  reference clips per character); the three dropped page designs.
- **The box** (the A6000 on Hyperstack) is woken per box session
  (owner action queue, item 5); the choice left for after the timebox
  — keep hibernating it or destroy it — is now due.
- **At a session's end:** a fresh-session handoff replaces any
  mid-session one, and a handoff is deleted only with the owner's
  permission. The latest handoff stays until the next compaction, as
  the template for the next one (the owner, 2026-09-28: "we keep the
  session handoff until the next time we have to compact, to serve as
  a template").

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

1. **Gather 4 reference voice samples** — NEXT (Task 4's first part,
   the owner, 2026-09-28). Where they go: each character's clip as
   `ref.wav`, with its exact transcript in `ref.txt`, in
   `~/TalkWithZombies-client/Personas/<Name>/` — outside both
   repositories (the fork gitignores `Personas/`; the installer never
   overwrites an existing persona folder), replacing the `say`-made
   placeholders; mono 24 kHz 16-bit is the safest format.
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
   are wired to clip selection — its shape is the follow-up "Mood
   clips" (`ref-<mood>.wav` next to `ref.wav`).
2. **Seed the character bibles** — DEFERRED by the owner
   (2026-09-28, Task 4's split: the voices first). Names,
   personalities, quirks, voice descriptions; rough is fine;
   model-neutral (guardrail 2). They become the sections of the
   show's cast sheet ([spec §5]) — concretely, each character's
   entry under "The cast:" in the fork's
   `stories/lab-outbreak/cast_sheet.md`, arriving as a pull request
   ([discussion 2026-09-23] show-engine-design §4). Unblocks Task 5a.
3. **Check the home 3090 box's NVIDIA driver** — DEPRIORITIZED
   (cloud-only demo), but note: it partially revives the day we
   test the playbook's localhost target ([discussion 2026-09-17]
   ruling 4).
4. **Demo-day logistics radar** — POSTPONED until the MVP works.
   Pre-decided: the **"canned episode" emergency mode is a
   MUST** (Task 7). Candidate on the radar: a tunnel that reconnects by
   itself (follow-ups, SSH keepalives — low priority).
5. **The Hyperstack VM — hibernated, woken per box session.**
   **Due now:** the timebox closed on 2026-09-28, so the choice it
   waited for — keep hibernating the box or destroy it — is open. Woken
   from hibernation 2026-09-23 on the same IP; hibernation is a full
   shutdown with the disk kept, so the box boots cold and every
   service comes back by itself (the TTS warms up on first use).
   Kept up during the day for quick live tests, hibernated again
   that evening (owner, 2026-09-23). For each box step of Task 6b
   (first 1.9): wake it, `make ans-set ENV=cloud IP=…`, start the
   tunnel; `make ans-unset ENV=cloud` after. Decide after the
   timebox: keep hibernating (its IP kept for a few cents an hour)
   or destroy; a from-zero deploy takes about 7 minutes.
   **2026-09-24: the wake failed — Hyperstack had no A6000 in
   stock** (the "restore-stock lottery" of
   `docs/runbooks/service-restart-sequence.md`, "Never hibernate a
   show box"). The options, the owner's call: retry the wake through
   the day (the 2026-09-13 survey saw A6000 stock come and go within
   one sitting); or rent an L40 (48 GB like the A6000; $1.00/h
   against $0.50/h in that survey) and deploy from zero. The agent's
   advice: retry first, the L40 only if the checkpoint arrives
   without an A6000; keep the A6000 hibernated until the timebox
   ends (its disk holds the llama.cpp image). **Later that day the
   owner woke it, on the same address**; a sanity check over SSH
   found it healthy (the A6000 visible with the models loaded, all
   three services answering, llama.cpp build `b11096-c550d2f60`).
   **The llama.cpp and Whisper images are now pinned** (2026-09-24,
   at the owner's call) in
   `deploy/ansible/inventories/common_vars.yml`: llama.cpp to the
   tag `server-cuda-b11096`, Whisper by digest to the `latest` of
   2025-12-28 (it has no version tag) — both the exact images the
   box was running (same digests). **Proven live the same day**
   (`b36c28c`): a deploy on the A6000 changed only the llama and
   Whisper containers (their image names), and the box then reported
   llama.cpp build `b11096-c550d2f60` and the pinned Whisper digest;
   a second run changed nothing (`changed=0`).

## Open tasks

- [ ] **Task 4 — Real cast replaces placeholders.** **Split in two
  (the owner, 2026-09-28):** (1) **the character bibles** — not now:
  "today has been all about improving the prompt, and right now the
  narration holds together more or less, ok. I want to pivot to audio,
  which is the weak spot now."; (2) **the reference voices** — one clip
  per character, the owner's, next: each character's clip as
  `Personas/<Name>/ref.wav` with its exact transcript in `ref.txt`, in
  `~/TalkWithZombies-client/Personas/` (the dev clone reads the same
  folder through its `personas_directory`); `Personas/` is gitignored in
  the fork and the installer skips an existing persona folder. Several
  clips per character by mood: the follow-up "Mood clips". **Where the
  clips may come from (2026-09-29):** datasets of real voices recorded
  in several emotions, instead of clips hunted one by one and cleaned of
  background noise — four finalists, EARS, CREMA-D, JL-Corpus and
  Expresso, and a listening test proposed ([discussion 2026-09-29]
  voice-datasets-with-emotion, OPEN). The detail
  as first written: character
  bibles → the sections of TalkWithZombies' cast sheet ([spec
  §5]; where they live in the fork — decided 2026-09-23: the
  cast entries of `stories/<story>/cast_sheet.md`, not the persona
  files — [discussion 2026-09-23] show-engine-design §4), keeping `/no_think`
  while on Nemotron (the chat template needs it even under the
  grammar — [spec §4]); no heavy prompt tuning yet — guardrail 2 ·
  voice samples → isolation tool first (follow-ups) → gitignore →
  replace the `say`-generated ref.wavs in the persona
  directories.
- [ ] **Polish — two items, right after Task 4's reference voices**
  (the owner, once Task 4 was split: "After the reference voices"; ruled
  2026-09-28, at the timebox's close; the owner: "I want to pull forward items: "1. Dead-air static while a round is generated" and "2. The 1930s radio look, with your gauge" , right after Task 4, and leave the rest as post-timebox follow-ups behind Task 4 and Task 7."):
  - [ ] **Dead-air static while a round is generated** — a soft,
    looping radio hiss through a second AudioContext source,
    generated in the browser, from the round's request until its
    first line plays, off while the page listens (so Whisper does
    not hear it). It covers the 3.7-4.9 s between rounds (measured
    2026-09-25), a trim's pause (about 5 s, measured 2026-09-28)
    and stalls. About 1-2 hours (estimate). Open since the looks
    (2026-09-28): the looks only, or the plain page too — the plain
    page changes only with the owner's word; and the looks' gauge
    (`static/show/gauge.js`) taps every sound the page's audio
    context plays, so a hiss there would move the magic eye and the
    meters unless it is kept apart.
  - [x] **The 1930s radio look, with the owner's gauge** (the
    fork's `alfre2v/radio-look`, `8624662`..`6800c00`;
    alfre2v/TalkWithZombies#5, merged as `0ec33c1`; tag `tz-0.3`)
    — as planned: the
    `/show` page restyled as an old radio set (cabinet, lit dial,
    period type, the captions as a panel) and a "magic eye" or a
    VU needle driven by Web Audio's analyser — the microphone
    while the button is held, the actors' audio while it plays
    (SED §6.7). The gauge about an hour in a simple form; the look
    open-ended (estimate).
    **Built 2026-09-28, the evening, ahead of the reference voices**
    — the owner: "You know what: we will work in parallel. While I
    work in finding the audios for the real voices, you will start
    working on the polish: "The 1930s radio look, with the owner's
    gauge". I think this one is isolated to the frontend, so it
    carries little risk of impacting the app functionality already
    working, only risk is that is looks ugly, then we discard it."
    How it went, in order:
    1. **Interchangeable looks** (the owner: "We do not need to
       implement only one look, you can generate 5 proposals, show
       me screenshots and then we decide which one to build.") —
       each design in its own folder, chosen with
       `/show?design=<name>`. The owner's two (`old-radio`,
       `amateur-radio-transmitter`) and three of the agent's
       (`broadcast-studio`, `lab-terminal`, `field-radio`) became
       mock-ups (`8624662`), filled by a recorded stretch
       (`?mock=1`: rounds 63-66 of run `2026-09-28T13-43-28`).
    2. **The plain page untouched** — the owner's condition: "Do
       not change the part that goes into today's functional show,
       I want to have that boring view as a 100% functional view I
       can always work with." `templates/show.html` and every
       existing file of `static/show/` are unchanged; a design
       gets the same elements with the same ids and works on them
       from outside; tests pin both.
    3. **A real photograph for the old radio** — two rounds of
       drawn textures were rejected ("This is even worse. Can you
       not get an actual photo of a real radio and use it as a
       background or something instead of producing this more and
       more cartoonish textures?"); 1930s photos on Wikimedia
       Commons were too small, so the set is a 1950 Philips Sirius
       BD 400 A (by "Bin im Garten", CC BY-SA 3.0; credited in the
       design's `CREDITS.md` and on the page) (`077f824`).
    4. **Two built, three dropped** (the owner: "Ok, let's not get
       too carried away. I think one design with real photos is
       enough. I actually want to keep your
       `amateur-radio-transmitter` design. [...] Let's build these
       2.") — the gauge (`static/show/gauge.js`: the voice's level,
       or the microphone's while the button is held) drives the
       old radio's magic eye and the transmitter's oscilloscope
       trace and meters (`23472e5`); the old radio's keys moved to
       its side panels, to the owner's placing (`0e0e27d`); the
       transmitter's contents cleared its bevelled edge
       (`6800c00`). The owner: "Very well done on the
       amateur-radio-transmitter. Incredible." The three dropped
       mock-ups stay in the branch's history (the follow-up "The
       three dropped page designs").
    5. **The chooser** (the owner: "when we open the show page
       without any arguments, instead of directly showing the old
       show page, we are given 3 screenshots to click") — `/show`
       now shows a card per look with a live miniature, the plain
       page last; `/show?design=plain` is the plain page. The root
       `/` opens the chooser, and TalkWithMe's chat UI moved to
       `/talkwithme`, linked from the chooser as "Or visit the old
       TalkWithMe interface that this project is built upon" (the
       owner's words) (`de91f49`).
    Checked on the dev copy at `127.0.0.1:8010` by screenshots and
    by the owner in the browser; the fork's suite 1129 passed and
    the page's Node tests (a new `tests/test_show_gauge.js`, 8).
    Released the same evening: PR #5 merged (`0ec33c1`), the tests
    green on `master` (1129 passed; Node 17 / 91 / 35 / 8), the fork
    tagged `tz-0.3` (annotated, on `0ec33c1`, pushed on the owner's
    order: "Let's get the tz-0.3 tag and the installer pointed at
    it."), the installer's `client_version` → `"tz-0.3"`; the
    owner's re-proof of the install is pending. How to use it: the fork's `docs/runbooks/show-page.md`,
    "Choosing a look".
  - **Moved to follow-ups, post-timebox, behind Task 4 and Task 7:**
    prefetch round N+1 (the follow-up "Prefetch the next round");
    episodes (the follow-up "Episodes — a story arc, with a recap
    between episodes").

- [ ] **Task 5 — In-prototype experiments (deliverable D3;
  protocol skeleton per guardrail 1: question, timebox,
  pre-registered pick criteria, runlog).**
  - [ ] **5a — LLM audition** ([spec §9]): the ranked five via
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
  - [ ] **5b — TTS comparison + VRAM budget** ([spec §9]):
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
- [ ] **Task 7 — The canned episode (owner MUST) + demo-day
  protocol runbook.** Recorded from the working prototype; the
  runbook promotion deferred from the last arc lands here. The
  seed makes retakes reproducible: on one server slot, the same
  request and seed gave the same words 80 minutes apart
  (2026-09-22) — record with the settings it will be replayed
  with.
- [ ] **Task 8 — Close ritual in the closing PR.** Features
  Shipped entry · task_history migration · TODO reset ·
  staleness sweep (CLAUDE.md included) · spec check (it describes
  the product as built — since 2026-09-28 a linear description, no
  longer a ledger of as-built entries).

## Done in this arc

*Kept whole — each block moved here unchanged — for the close
ritual's migration to `task_history.md`.*

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
- **Task 6, the parts already done** ([ADR-0002], [ADR-0003]).
  *How it got here, in five steps:*
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
    (sub-item below).
  - **2026-09-23 — the fork exists** (6a below):
    `alfre2v/TalkWithZombies`, first tag `tz-0.1`, installed by
    `make client-mac`. The show engine (6b) is next.
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
  AGENTS.md there). *(Done 2026-09-23 — see 6a; the pointer
  section is `docs/README.md` "Where things live".)* Rejected: a git submodule (nested detached
  checkout, a second place recording the version, buys nothing at
  deploy time since the installer clones from GitHub anyway); a
  subtree merge (the app inside a docs/deployment repo, our hooks
  and lint over its files, subtree splits to push anything back);
  copying files without history (ruled out by the attribution
  commitment).
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
  - [x] **6a — Fork TalkWithZombies ([ADR-0002]) — done
    2026-09-23** (fork: PR alfre2v/TalkWithZombies#1, merge
    `1d41bab`, tag `tz-0.1`; this repository: branch
    `alfre2v/talkwithzombies-fork`).
    - **The fork:** `alfre2v/TalkWithZombies`, public, parent
      scorbo2/TalkWithMe, created with `gh repo fork
      --default-branch-only` (only `master`, which was exactly tag
      7.1 = `93df6ca`; upstream's `7.2-dev-branch` and issue branch
      not copied). A master-only fork copies no tags, so upstream's
      `7.1` tag was pushed to the fork as the fork-point marker.
    - **The clone:** `/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`;
      remotes `origin` (the fork) and `upstream` (scorbo2, fetch
      only — its push URL is set to `NO_PUSH_TO_UPSTREAM`); its own
      `.venv` on Python 3.12.14.
    - **Provenance and house rules** (`00eaf85`): the README's new
      top section ("Forked from TalkWithMe" by Steve Corbett, tag
      7.1, MIT `LICENSE` byte-identical to upstream's, where things
      live); `AGENTS.md` gains the house rules above upstream's
      text; a one-line `CLAUDE.md` (`@AGENTS.md`) — step 6's
      assumption corrected: Claude Code reads `CLAUDE.md`, not
      `AGENTS.md`, so the import is what makes a fresh session of
      the lead see the rules.
    - **Suite green from the start** (`c46c3bf`): 2 of 781 upstream
      tests failed on the untouched 7.1 code — `mimetypes` answers
      `.weba` for `audio/webm` on newer Pythons. Pinned to `webm`
      (OpenAI's transcription API rejects `weba`; our Whisper ignores
      the name — tested live). Now 781 passed, both Node tests pass.
      Upstream bug report candidate (follow-ups).
    - **Fork tags:** own version line with a `tz-` prefix, never
      upstream's bare numbers (upstream's next release will be `7.2`,
      with different code). `tz-0.1` = the merged setup PR.
    - **The installer** (`deploy/ansible/client-talkwithme-mac.yml`,
      filename kept): `client_repo` → the fork, `client_version` →
      `tz-0.1`, `client_dir` → `~/TalkWithZombies-client` (the old
      `~/TalkWithMe-client` stays as the 7.1 fallback). The pin
      lives in the playbook, not in `common_vars.yml`: the client
      playbook is inventory-free by design. Step 5: `allow_tool_calls`
      was already false (the code's default and our seeded personas);
      `enable_persona_memories: false` added to the seeded
      `settings.yaml`.
    - **Proof:** lint clean (`production`); fresh install
      `changed=8` in 21 s; re-run `changed=0`; the installed app at
      `tz-0.1` answers HTTP 200 on a test port and lists exactly the
      four cast personas.
    - *Acceptance:* all met — `gh repo view` names
      scorbo2/TalkWithMe as parent; the "forked from" section and
      the unchanged `LICENSE` are on `master`; `make client-mac`
      installs the fork at its pinned tag, re-run `changed=0`,
      HTTP 200.
- [x] **Task 6 — The fork and the show engine: TalkWithZombies
  ([ADR-0002], [ADR-0003]).** 6a (the fork) is done — its record and
  the road here are under "Done in this arc". The timebox's terms
  follow, then 6b's checklist.
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
    attempt. **Actual (owner ruling 2026-09-23, the rule as first
    agreed):** the fork was created 2026-09-23 at 14:46 CDT and the
    clock started then — checkpoint (day 1.5) 2026-09-25 at 02:46
    CDT, end 2026-09-26 at 14:46 CDT.
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
  - [x] **6b — Build the show engine, as three slices** — **done
    2026-09-28** (the fork's `tz-0.2`, `ca37199`).
    **Read this first.** The design is decided and lives in
    [discussion 2026-09-23] show-engine-design — cited below as
    **SED §n** — with its roots in [ADR-0003], [spec §6], and the
    lessons of
    [discussion 2026-09-22] grammar-and-prompt-cache-lessons (cited
    as **L §n**). This list is the ORDER and the STATE: each step
    says what to build, where, where it was decided, and when it is
    done. Tick a step with its commit hash; move "Next" in the Now
    section as you go.
    - **Branches:** one feature branch per slice in the fork, each
      cut from the fork's up-to-date `master` after the previous
      slice's pull request is merged (SED §7.3).
    - **Standing rules for every step:** the fork's pytest suite
      green before review, plus the Node tests when their files are
      touched; review before every commit; delegation OFF (owner
      ruling 2026-09-23 — the "delegable later" marks below are a
      knob for the future, not in use); tests in upstream's style
      (`tests/test_show_*.py`, one per module; upstream's isolation
      fixture in `tests/conftest.py` gains the `runs/` and `stories/`
      roots).
    - **Operating notes (measured 2026-09-22):** one conversation
      per server slot — keep the chat UI off the show's server
      during show runs; a round that meets a slot holding another
      conversation first pays a state swap (~1.8 s). The box stays
      up through 6b; the tunnel is the owner's.

    - [x] **Slice 1 — the skeleton** (done 2026-09-24 ~02:30, merged
      that day: the fork's `4a62e18`). Branch
      `alfre2v/show-slice-1-skeleton`. **Target: end of day
      2026-09-24.** Every piece in its simplest form, tested offline,
      then ten rounds on the box — no microphone, no browser.
      - [x] **1.1 The `show:` settings** (`b538828`; the section also
        survives saves from the chat's Settings dialog — carried over
        in the settings router like `mcp`, tested in memory and on
        disk) — `app/config.py`, a show
        settings model beside the existing ones; yaml-only, defaults
        when absent: `story`, `episode` (optional), `model_prefix`
        (`/no_think`), `context_budget`, the emotion switch (default
        on), `debug`, the three timers (`interaction_min_s`,
        `interaction_max_s`, `listen_window_s`) and the press cap, the
        transcript filter's two thresholds, the STT `language`; the
        accumulator's limit and tolerance next to `tts.streaming`.
        The cast is NOT here — it lives in the story. (SED §3.4,
        §4.5, §5.7, §6.7.) *Done when:* a unit test reads every key,
        with defaults when absent. *Delegable later: yes.*
      - [x] **1.2 The story** (`4444aa4`; the shipped story renders
        run 1's and run 2's proven system prompts byte for byte; the
        mood list filled from `MOODS`; the voice check goes through
        the persona list) — `stories/lab-outbreak/cast_sheet.md`
        (run 2's placeholder cast turned into the template: front
        matter `title`, `cast`, `operator: Samantha`; the body with
        `{{ model_prefix }}`, `{{ format_rules }}`, `{{ episode }}`);
        `stories/lab-outbreak/events.yaml` (the gate's ten events as
        the first pool, phrased "Offstage: …"); `app/show/rules/`
        (the two format snippets, moods off and on); `app/show/story.py`
        (front matter, Jinja in strict mode, each cast name checked
        against `Personas/<Name>/` for its voice). (SED §4.3–§4.5.)
        *Done when:* the cast sheet renders with the switch on and off
        and only the snippet changes; a missing variable fails
        loudly; an unknown cast name fails at load.
      - [x] **1.3 The grammar builder** (`a268bcd`; byte-identical to
        both grammars proven on the box) — `app/show/grammar.py`:
        allowlist → `speaker` alternatives; budget → `line{1,N}`;
        square brackets out of `text`; with the switch on, the
        `(emotion)` rule before the words, run 2's nine values, and
        parentheses out of `text`. (SED §5.7; L §5.1.) *Done when:*
        unit tests assert the exact GBNF text for a given allowlist
        and budget, with the switch on and off. *Delegable later:
        yes* (the box step, 1.9, stays with the lead).
      - [x] **1.4 The stream parser and normalizer** (`d30d7ab`;
        character by character, so chunking cannot matter; the real
        recording's `raw` byte-identical to the model's output; also
        `b64e5b4`, `show.max_tokens` 300 → 512 — a whole round's
        guard, not a line's) —
        `app/show/parser.py`: `start` (with the mood) / `token` /
        `done` per script line — the endpoint adds the ids and
        `complete`. Two texts per line (owner ruling 2026-09-23):
        **`raw`**, exactly as the model wrote it, for the history;
        **`spoken`**, for the voice — mood tag stripped, typographic
        punctuation normalized (`’‘` → `'`, `“”` → `"`, `—` → `, `,
        `…` → `...` — required, L §4.6), trailing whitespace trimmed,
        wrapping quotation marks removed. Every event the browser
        receives carries only spoken text: with streaming TTS on, the
        voice is fed from the `token` events (`static/chat.js:230-235`),
        so trailing spaces and a closing quote are held back until
        something follows. A line cut short (the stream ends
        mid-line; `finish_reason: "length"`) gets no `done`, is
        flagged, and stays out of the history. (L §4.6–§4.7.) *Done
        when:* the probe's real 42-token recording (2026-09-23)
        parses into both lines with `raw` byte-identical to the
        model's output and clean events; chunking makes no
        difference; the mapping character by character; quotes;
        moods off; a cut line. *Delegable later: yes — the best
        first candidate.*
      - [x] **1.5 The run record and the assembler** (`8b39b17`; one
        file per run, written at the start and atomically once per
        round; the cast sheet stored per episode, so episodes will not
        change the file's shape; the reply byte-identical to the
        model's output; a round with no lines stays out of the
        history) (append only) —
        `app/show/script.py`; `runs/` added to the fork's
        `.gitignore`. `script.json` holds the story, the cast, the
        seed, and the rounds (instruction, listener's words, lines
        with speaker, mood and text, a `trimmed` flag, the episode).
        The assembler replaces what `build_llm_messages` did
        (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/session.py:123`):
        `system` = the rendered cast sheet, then alternating
        instruction and script turns, the model's lines written back
        **exactly as the model wrote them** (`raw` from 1.4 — owner
        ruling 2026-09-23: normalization is for the voice only, so the
        history keeps the model's own distribution; either way costs
        the same cache — L §2.8), cut lines left out. (SED
        §3.4.) *Done when:* for a given `script.json`, the messages
        are the cast sheet then alternating turns, and no `[Name]:`
        appears anywhere; the record round-trips. *Delegable later:
        yes.*
      - [x] **1.6 Director v0** (`ac0de25`; a pure function — the
        generator seeded by the run's seed and the round number, so
        nothing extra is stored; `Round` gains `event`, which the
        no-repeat rule reads) — `app/show/director.py`, seeded: 2–3
        random names, 2–3 lines, an "Offstage:" event from the pool
        every other round, no microphone; the constraint said in
        plain words ("Ralph and Moira speak next: the next two
        lines, each with the emotion in its voice."), no label.
        (SED §5.7, the subset.) *Done when:* the allowlist and the
        budget appear both in the instruction's words and in the
        grammar; the same seed gives the same rounds.
      - [x] **1.7 The request with the grammar** (`cf6f8e7`; in 1.8
        the keys moved into `stream_round`, the show's own request,
        and `stream_chat` went back to upstream's exact code)
        — one more key,
        `grammar`, at the top level of the payload
        (`_base_payload`,
        `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/services/llm.py:69`);
        the chat path unchanged. ([ADR-0003].) *Done when:* a unit
        test shows the key in the show's payload and its absence in
        the chat's. *Delegable later: yes.*
      - [x] **1.8 The endpoints** (`9ae374a`; no show state on the
        server — the caller sends the run id; `stream_round` in
        `llm.py` over a split SSE iterator; an error or a disconnect
        mid-round records nothing; the disconnect path is not
        covered by a test) — `app/routers/show.py`:
        `POST /api/show/start` opens a run (a new `runs/<run-id>/`,
        returns the cast); `POST /api/show/round` runs the director,
        streams the SSE events, and appends the round — a sibling of
        `_chat_stream`
        (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/routers/chat.py:208`);
        no room parameter; it already accepts the played seconds and
        an optional transcript, used from slice 2. It needs a small
        stream reader of its own: upstream's hands over only
        `choices[0]` (`app/services/llm.py:101`), and the final
        ("stop") chunk's `timings` — the script's size, for the trim
        — sit beside `choices`; keep them and store them with the
        round (measured 2026-09-23; SED §2.4's note). (SED §3.4.)
        *Done when:* an API test with the LLM stream mocked sees the
        expected events, and the round with its `timings` in
        `script.json`.
      - [x] **1.9 The driver, and ten rounds on the box** (`4f1d908`;
        the runbook `78cfee7` — the fork's
        `docs/runbooks/show-driver.md`, a new folder for the fork's
        procedures, the owner's proposal). **The first real run,
        2026-09-24 ~02:19, on the box through the app (seed 42):** 10
        rounds, 24 lines, 0 dropped, every round `stop`; every round
        within its speakers and filling its line budget exactly; first
        line ~0.8 s, average round 1.16 s; the script 1,164 tokens
        after the last round (each round re-reads only ~115–150
        tokens — the prompt cache works); `raw` keeps the model's
        curly punctuation (21 lines) and trailing spaces (14),
        `spoken` none; the characters react to the events. Control:
        PASS (only `Operator` allowed → every line Operator's). The
        app's startup reads the Personas folder without writing into
        it. —
        `scripts/drive_show.py` (standard library only): start a
        run, then ten rounds through the tunnel, printing each line,
        simulating the played seconds. *Done when:* ten rounds on the
        box, every line parsed, the run folder written; plus one
        grammar control request (only a name absent from the prompt
        allowed) that comes back in that name alone.
      - [x] **Slice 1 pull request** — alfre2v/TalkWithZombies#2
        and this repository's #10, merged by the owner 2026-09-24.

    - [x] **Slice 2 — the rules** (built 2026-09-24, all six steps,
      the checkpoint passed that evening; both pull requests merged
      2026-09-25). Branch
      `alfre2v/show-slice-2-rules`, cut 2026-09-24 from the fork's
      `master` (`4a62e18`). **Target: the checkpoint.**
      - [x] **2.1 Director v1** (`ce8bd71`; suite 909 passed). As
        built, with the owner's picks of 2026-09-24: `played_s` is
        the running total since the run started (a failed round
        records nothing, so per-round seconds would be lost); the
        tone words live in the story's optional `tones.yaml` ("Let
        the tone be: brittle.", every kind but the answer; no file,
        no tone); cast names match whole words, exact case; the
        static round is the operator's one line; the page learns to
        listen from `kind` on the `round` event. **Computed with the
        real director:** over 2,000 seeds at 20 s of audio per round,
        invitations come 115.0 s apart on average (80 min, 180 max);
        seed 42's default ten-round drive invites at round 8 and
        plays the static round at round 9. **Observed in the first
        real run:** none of its 24 lines named another character, so
        the "named in the last round" rule has little to act on
        (follow-ups: the "exchange" round). **Story content**
        (`22a0af2`, the owner's request): 500 tone words in 24 groups
        (the 2024 list pruned to 25 and extended) and 289 events (the
        gate's ten plus 279 in 14 groups; follow-ups: events that
        stay on topic). The fork's house rules now keep upstream's
        documentation style (`3540d88`). — The full rules of SED §5.7: free
        rounds allow 2–3 names (whoever has been silent longest,
        always; anyone named in the last round or in the listener's
        words; random fill) and 1–4 lines weighted to 2–3; one tone
        word per round; the round kinds — invitation (the story's
        `operator`, one line), answer (the whole cast allowed, one
        line, "the character the voice addressed answers; if it
        addressed no one, whoever fits best answers", narrowed to an
        exact cast-name match), static ("Only static answers."); the
        cadence on played seconds (never below `interaction_min_s`,
        a rising chance between, always at `interaction_max_s`); the
        listener's words as "A voice on the frequency says: …";
        memory derived from `script.json`, the seed stored in the
        run. *Done when:* the allowlist and budget in words and
        grammar; the silent-longest name always allowed in a free
        round; with a seeded source, no invitation before the minimum
        and always one by the maximum; an exact cast name narrows the
        answer round; a silent window yields the static round.
        *Delegable later: no* (design-heavy).
      - [x] **2.1b Pacing knobs for events and tone words**
        (`2f76b34`; suite 927 passed). As built, with the owner's
        picks of 2026-09-24: `show.event_every` 2 / `event_jitter` 1
        (the gap, in free rounds) and `show.tone_hold` 3 /
        `tone_jitter` 1 (the hold: one tone word kept for a few
        rounds, the owner's pick over spacing it out); each gap and
        hold drawn once, seeded; the run's first free round opens with
        an event; 0 turns either off. The terms (gap, hold, jitter)
        and a timeline: SED §8. **On the box** (seed 42, 14 rounds,
        the fork's `runs/2026-09-24T15-57-21/`): gaps of 1, 3, 2, 2
        free rounds and holds of 2, 4, 3, 4 rounds, within bounds; the
        churn gone — "homesick" held four rounds gave one coherent
        nostalgic stretch; the tone word steers the emotion tags too.
        **The static round** read as a sign-off in both live drives
        ("This is a dead end.", "Farewell, dear listeners…"); worded
        now "Only static answers; the broadcast goes on." — re-driven
        with the same seed (rounds 1–8 identical,
        `runs/2026-09-24T16-05-03/`): "We'll keep broadcasting." and a
        station identification instead. **The tone-repeat guard**
        followed (`35f34e0`, the owner's go, 2026-09-24): no tone word
        again until the list is used up, the events' rule shared
        (`_fresh`); without it 78 % of simulated 40-minute shows
        repeated a word, with it none of 300. —
        The owner, 2026-09-24, reviewing 2.1: "Keep in mind to execute
        these two changes at the first opportunity we have. Remind me
        about them if we do not execute them soon." The worry: events
        and tone words switch the conversation's topic and color too
        fast. **Events:** `show.event_every` (default 2; 0 turns
        events off — the checkpoint's "scale down: the events first"),
        counted in free rounds since the last event, not in round
        numbers (v1's `n % 2 == 1` silently skips an event whenever an
        invitation, answer or static round lands on an odd number),
        plus a jitter setting so listeners cannot hear a fixed beat
        (each gap drawn once, seeded, within `event_every ± jitter`).
        **Tone words:** the same pair of knobs. *To settle in the
        shape:* whether the tone knob spaces the tone sentence out
        (rounds in between get none) or holds one word for the whole
        stretch (the agent's lean: hold — a steady color is what
        fixes the churn); the jitter's name and unit. *Done when:*
        seeded tests keep every gap within its bounds and replay
        identically; 0 turns each off.
      - [x] **2.2 The trim** (`57a08c9`; suite 936 passed). As built,
        with the owner's picks of 2026-09-24: each round records its
        share of the size (`tokens`) from `timings`; the first 2 and
        last 4 rounds the model reads are always kept; the rest
        flagged **from the middle outwards** (the owner's order: the
        early rounds survive as context, one contiguous span leaves);
        `trims` on the record and the `round` event; the driver
        prints the trim. **Measured on the box** (`context_budget`
        1500 instead of 3,000 — at about 80 tokens a round, 3,000
        would first trim near round 33; two identical 28-round
        drives, two trims each): the re-read is small (the cache
        reused up to the cut, 512 of 516 tokens; 308-316 tokens read
        in 453-474 ms against ~365 ms normally), but the slot swap
        between choosing the slot and starting the work costs
        1.3-1.5 s in three trims of four — a pause `timings` does
        not show, the one the ADR-0003 gate saw, spotted on the
        owner's hunch; the next round is normal again. Written to L
        §4.10 question 3; follow-ups: "Pauses the model server's
        timings do not show". — In `app/show/script.py`: before a
        round, the script's size from the last response's final
        ("stop") chunk — `timings.prompt_n + timings.cache_n +
        timings.predicted_n` (a stream carries no `usage` by default;
        measured 2026-09-23, SED §2.4's note); at 90 % of
        `context_budget`, whole rounds from the middle flagged
        `trimmed` until 50 %, keeping the cast sheet, the opening
        rounds and the recent rounds; the assembler skips flagged
        rounds. (SED §2.4, §3.4.) *Done when:* a unit test with token
        counts; on the box, with `context_budget` near 3,000, the trim
        fires within a few rounds and its pause is measured — the
        number goes to L §4.10 question 3 as a dated note.
      - [x] **2.3 The debug switch** (`129d3de`; suite 948 passed). As
        built, with the owner's picks of 2026-09-24: per round a
        readable `rNNN.txt` (numbers, grammar, the prompt as the model
        read it, the reply as it streamed) and the exact
        `rNNN.request.json` (replayable with curl); failed rounds
        included; written after the round (a debug round costs about
        0.35 s more). **The token-count check the owner asked about:**
        `/tokenize` of the rendered prompt (special markers parsed,
        start token added) against `prompt_n + cache_n`, a warning on
        a difference — checked before building on 7 rounds of an
        earlier drive rebuilt from its record (equal to the token,
        trim rounds included; the record's `trims` make the rebuild
        possible), then **live: 16 rounds with a trim, difference 0
        on all 16** (the fork's `runs/2026-09-24T17-37-14/`). The
        runbook gained "Look inside a round". — With `show.debug` on, each
        round writes `runs/<run-id>/debug/`: the messages sent, the
        grammar in full, the rendered prompt from `/apply-template`
        (verified 2026-09-23: ~120 ms, no generation, no slot), and
        the raw reply. (L §4.9, §5.) *Done when:* switched on, every
        round leaves its file. *Delegable later: yes.*
      - [x] **2.4 The STT client and the transcript filter**
        (`d6ab1b9`; suite 980 passed). As built, with the owner's
        picks of 2026-09-24: the show's own route, `POST
        /api/show/listen`, transcribes with the cast's first names as
        Whisper's prompt, `language` and `vad_filter`, and returns the
        text with the highest `no_speech_prob` and the average
        `avg_logprob`; the round request carries them and the round
        runs the filter (`app/show/listen.py`) before planning;
        `Round.heard` records what was heard and the verdict; a new
        `transcribe_for_show` beside upstream's `transcribe_audio`,
        which stays untouched (SED §6.7's dated note). The deployed
        Whisper rejects `verbose_json` and carries the segments in
        plain `json` — the live check found it. **Live, no browser**
        (the fork's `runs/2026-09-24T18-01-23/`): TTS spoke "Moira, is
        the virus airborne?" in Samantha's voice → heard "Moira is the
        virus airborne" (no_speech_prob 0.01, avg_logprob −0.30) →
        Moira answered; two seconds of silence → heard nothing → the
        static round. The cast-names prompt made Whisper surer of the
        same clip (no_speech_prob 0.018 → 0.005). — The STT client:
        `app/services/stt_client.py`: empty text instead of the "No
        response received from STT server" placeholder (line 85),
        the highest `no_speech_prob` and the average `avg_logprob`
        returned, `prompt` / `language` / `vad_filter` passed when
        given; the show's transcriptions send the cast names as
        `prompt`, `language=en`, `vad_filter=true`.
        `app/show/listen.py`: silence if empty or one character,
        `no_speech_prob` > 0.6, `avg_logprob` < −1.0, or a known
        Whisper hallucination. (SED §6.7.) *Done when:* fake Whisper
        replies — empty, high no-speech, low confidence, a known
        hallucination — each yield the static round, and the
        placeholder text never reaches the director. *Delegable
        later: yes.*
      - [x] **2.5 The driver, extended** (`86dc1df`; suite 1003
        passed). As built, with the owner's picks of 2026-09-24:
        `--heard` items answer the invitations in turn (`-` is a
        silent window; without them, or once they run out, nothing
        is sent, as before); by default as text, and with `--speak`
        the real path (the app's TTS in the operator's voice →
        `/api/show/listen` → the round request; a silent window
        sends two seconds of silence); the `round` event now carries
        `heard` (the text, Whisper's numbers, the silence reason) for
        the driver and the page's debug-only "Heard: …"; `--report`
        prints PASS or FAIL per checkpoint criterion from the record
        and the debug folder, and the driver exits 1 on a FAIL; the
        checkpoint's settings are set by hand; the fork's runbook
        gained "Run the checkpoint". **Computed offline first:** at
        seed 42 and 20 s a round, the invitations fall at rounds 8,
        13 and 18 (the cadence depends only on the seed and the
        played seconds), so the checkpoint's three listener windows
        need a 20-round drive, not ten. — Fake transcripts at the
        invitations (one naming a character, one not), a silent
        window, the played seconds simulated. *Done when:* it can
        run the checkpoint below.
      - [x] **Slice 2 pull request** — alfre2v/TalkWithZombies#3
        (opened 2026-09-24, merged by the owner 2026-09-25: the fork's
        `master` at `5b2485f`) and this repository's #11 for
        `alfre2v/show-slice-2` (it also carried slice 3's plan
        discussion, at the owner's request; merged 2026-09-25,
        `main` at `b9e4d18`).

    - [x] **Checkpoint — passed 2026-09-24 ~18:57, about eight hours
      ahead of its clock. Verdict: continue** (the owner counted
      this run as the checkpoint run and opened slice 2's pull
      requests). The fork's `runs/2026-09-24T18-56-59/`: seed 42,
      `context_budget` 1500, debug on, 20 rounds, the listener's
      words spoken and transcribed (`--speak`). **The driver's
      report: 6 of 6 criteria pass** — 20 of 20 rounds recorded; 38
      lines, 0 dropped, every speaker allowed, no round over its
      budget; invitations at rounds 8, 13 and 18 as computed: Moira
      answered "Moira, is the virus airborne?" (heard word for word,
      no_speech_prob 0.010, avg_logprob −0.225), the silent window
      gave the static round 14, and Samantha answered a question
      naming no one ("Who's asking?"); the trim fired before round
      14 (rounds 3–9), whose first line came at 2.37 s against about
      0.8 s (the slot swap, L §4.10 question 3); debug files for all
      20 rounds, token check difference 0 on each. — The plan:
      **2026-09-25, in practice that morning (clock
      02:46).** Judged on the box, no browser (SED §7.3): ten
      unattended rounds; speakers and line counts obey the director;
      an invitation, then an answer from an injected transcript; a
      silent window giving the static round; the trim firing; the
      debug files written. **Verdict, recorded here:** continue ·
      scale down (the tone word and the events first, then the
      cadence rules — keep the microphone, simplify when it opens) ·
      stop (the fallback: TalkWithMe 7.1 plus the canned episode).

    - [x] **Slice 3 — the browser** — **done 2026-09-28**: merged as
      alfre2v/TalkWithZombies#4 (`ca37199`) and this repository's #12
      (`2841065`); the fork tagged `tz-0.2`. Branch
      `alfre2v/show-slice-3-browser`, cut from the fork's `master`
      (`5b2485f`, slice 2's merge) on the owner's Go. **Target: Monday
      2026-09-28** (the timebox's end, moved by the owner on
      2026-09-25). **Planned 2026-09-25** ([discussion 2026-09-25]
      show-slice-3-browser-plan, DECIDED): the show's frontend in its
      own files — `templates/show.html` and `static/show/` (`show.js`,
      `sse.js`, `player.js`, `mic.js`, `show.css`), classic scripts
      sharing globals like upstream's — with upstream's JavaScript,
      HTML and CSS untouched and copying from them welcome. This
      replaces the first plan's six steps (a shared `static/sse.js`
      extracted from `chat.js`, the accumulator inside upstream's
      `static/tts.js`, hold-to-talk inside `static/stt.js`). Each step
      opens with its build shape in chat.
      - [x] **3.1 The page, text only** (`8bca58b`; suite 1007 passed,
        Node tests 17 + 91 + 8). As built, with the owner's picks of
        2026-09-25: `GET /show` on a second router with no prefix,
        included in `app/main.py` with one line; the stage direction
        placed above the round's lines when the `round` summary brings
        the event (no change to the stream); the listening window shown
        already, its countdown with the talk button disabled; Stop
        aborts the round in flight; the runbook
        `docs/runbooks/show-page.md`. **Live on the box**
        (2026-09-25; the fork's `runs/2026-09-25T14-57-06` and
        `T15-48-26`, seed 42, debug on): round 1 word for word as the
        checkpoint's; invitations at rounds 15, 32 and 53 on the
        simulated clock, each window counting down and the static
        round after it; Stop mid-round (the server: "abandoned by the
        client; nothing recorded") and Resume on the same run; a
        dropped tunnel (the owner's, ~30 s) shown as an error, and
        Resume replayed the failed round; the captions toggle. **Two
        fixes from that check**, at the owner's word: a Stop can land
        after the server recorded the round, before its summary reached
        the page (seen on a double Stop at round 44; the owner may have
        pressed it — "LEt's keep an eye on this", verbatim) — the page now learns
        it from the next round's number and notes "(stopped, but the
        server kept this round)"; and a recorded round's debug files
        are written even when the client leaves meanwhile (the write
        shielded; `r044.txt` had been cut short). Both proven live:
        stops between lines left rounds 1-3 unrecorded and their notes
        unchanged; a Stop during round 16's debug write kept the round,
        wrote its files, and the note said so. The first line took
        0.9-1.4 s in the browser against 0.76-0.94 s from the driver on
        2026-09-24 (the box just woken; watched in 3.2). The page also
        showed the events' flaw — the follow-up "Events the listener
        cannot hear". — `GET /show` in the show
        router (its own `Jinja2Templates`); the start response gains
        `listen_window_s`, `press_cap_s` and `debug`; the layout of the
        plan's sketch (§6.1): Start / Stop / Resume, the state line,
        the cast strip with the speaker lit, the captions behind a
        small toggle under the ON AIR sign (on by default, remembered),
        events as stage directions with the captions, and — only while
        `show.debug` is on — a line per round (kind, speakers, event,
        tone, trims, dropped, timings, run id); `sse.js`, the stream
        reader copied from upstream's `chat.js` (lines 135-159);
        `show.js`, the states and the loop on a simulated clock: after
        each round the page waits as long as its text would take to
        say (characters ÷ 15 per second) and sends that as the played
        seconds; the round after an invitation goes static (no
        microphone yet). Failures: stop, say so, and Resume continues
        the same run. A reload starts a new run (resuming the same run
        is a follow-up). *Done when:* by hand — rounds play with their
        lines, invitations and static rounds come on the cadence, the
        toggle hides and shows lines and events, Stop and Resume
        continue the same run, a dropped tunnel shows the error and
        Resume recovers; Node tests in upstream's `vm` technique
        (`tests/test_tts_settings.js`) for the stream reader (lines
        split across network chunks) and the simulated clock; the
        suite green.
      - [x] **3.2 The voice** (`a2d942e`; suite 1007 passed, Node
        tests 17 + 91 + 19). As built, with the owner's picks of
        2026-09-25: a chunk the voice cannot say is skipped and its line
        still appears; `?voice=off` keeps 3.1's simulated clock; 80 ms
        between the chunks of a line, 250 ms after a line; the debug
        line gains "first sound" and "played" once a round is said;
        Node tests for the packing rules and for the voice queue with
        `fetch` and the `AudioContext` stubbed — the follow-up
        "JavaScript test for the accumulator's packing rules" is
        resolved (entry deleted). **Live, by ear** (2026-09-25, the
        fork's `runs/2026-09-25T16-04-56`, 42 rounds, 245 s of audio):
        the owner found no problem — "I cannot find any problem. Well
        executed! We can call this a success." — and "The pauses do not
        feel so bad actually." Measured in the page: each chunk's
        synthesis costs 2.4-3.2 s almost whatever its length (27-55
        characters), so silences inside a round are 250 ms or, where a
        short line could not be ready in time, 1.2-1.9 s; 3.7-4.9 s
        between rounds (6.8 s for a run's first, the TTS cold) — the
        follow-ups "Measure TTS synthesis time against text length" and
        "Prefetch the next round". **A defect fixed on the way,** from
        the owner's questions: upstream's sentence regex cut inside
        numbers, and the voice got "3. 5" for "3.5"; a sentence now ends
        only where its marks meet whitespace or the line's end
        ([discussion 2026-09-25] show-slice-3-browser-plan §8; upstream
        has it too — candidate (5) of the follow-up "Upstream
        contributions to scorbo2"). The owner heard "Over." run into a
        few lines ("coming over"): the accumulator stays at 100 (the
        follow-up "The sign-off 'Over.' sometimes runs into the line").
        — `chunks(line)`: the accumulator as a
        plain function over each whole line (the text of its `done`
        event), with the rules of 2026-09-22 ([discussion 2026-09-21]
        task6-recon-talkwithme, the ruling on Q9 and Q4): chunks of up
        to 100 characters of whole sentences; a remainder under ~30
        characters rides along up to ~120; a sentence longer than 100
        goes whole and alone; never across lines. `player.js`, copied
        from upstream's `tts.js` without the chat's audio upload:
        chunks fetched in order, the next while the current plays,
        played in order; the played seconds counted from each decoded
        clip's duration. The loop on drain: the next round when the
        audio empties, with the real played seconds; a line's caption
        appears when its first chunk starts playing; the speaker lit
        while their voice plays. *Done when:* by ear — lines in order,
        short sentences packed, none split; the next round follows the
        drain; the played seconds match the audio (logged); Node tests
        pin the packing rules ("Testing. 1. 2. 3. Over." one chunk; a
        180-character sentence whole and alone), which resolves the
        follow-up "JavaScript test for the accumulator's packing
        rules".
      - [x] **3.3 The listener's turn** (`57dce7f`; suite 1007
        passed, Node tests 17 + 91 + 26). As built, with the owner's
        picks of 2026-09-25: the microphone asked for once at Start and
        open only while the radio listens (opened with each window,
        closed after — a press records at once, and no permission prompt
        eats a window); one press per window; a failed transcription
        counts as silence (noted with debug on); with debug on, the
        invitation's block shows what Whisper heard. **Checked live
        with a fake microphone** (the fork's run `2026-09-25T17-50-50`;
        the page's `getUserMedia` fed the TTS saying "Moira, is the virus
        airborne?"; invitations brought forward by temporary settings,
        20-40 s): the window opened with the microphone, the press
        recorded, Whisper heard the question word for word, and round 5
        was Moira's answer; a window left unpressed gave the static
        round (round 12); the microphone was closed outside the windows.
        **The real button and microphone are checked in 3.4's session**
        (the owner's call, 2026-09-25: 3.4 needs a real spoken exchange
        anyway). The owner kept the listening window for the MVP and
        recorded a preference for talking back at any moment — the
        follow-up "Talk anytime"; the check also surfaced the follow-up
        "A line broken off with an em dash sounds and reads cut". —
        `mic.js`: hold to talk
        (mouse, touch, the space bar), enabled only while listening,
        the recording code copied from upstream's `stt.js`; the
        window's countdown (`listen_window_s`) stops on a press; the
        press cap (`press_cap_s`) ends a long press; the upload to
        `/api/show/listen`; the transcript with Whisper's numbers rides
        the next round request; "Heard: …" with its verdict in the
        debug line. (SED §5.7, §6.7.) *Done when:* by hand — the button
        works only while listening; a spoken question gets its answer;
        a silent window gives the static round; the press cap ends a
        long press.
      - [x] **3.4 The exit criterion, by ear** (2026-09-25, night; the
        fork's run `2026-09-25T23-00-20`, invitations brought forward to
        20-40 s, captions off, the real talk button and microphone).
        **Met — the owner (verbatim): "It does what we planed. It is a
        success."** 33 rounds, 5 invitations: three answered from the
        owner's words, heard well by Whisper (no_speech_prob ≤ 0.024) —
        "Hello, what's your name?" → Daniel: "Who's there?"; "Hello,
        Samantha, are you there?" → Samantha: "Who are you?"; "I think
        Ralph and Moira should go to the south entrance." → Ralph: "They
        think we should go south." — and two static (no press; a press
        heard as nothing). The first listen to events worded for the
        broadcast. **Two findings:** the listener's own words do not
        show in the captions (→ 3.4b, the owner's request); and the
        exchange is poor — one answer line, the characters ask back but
        no window opens, and the next round moves on, often to an event
        (the follow-up "The listener's exchange is one line"; the owner:
        "Let's decide after 3.4b if we included as 3.4.c."). — On the
        deployed stack
        through the tunnel: at least ten unattended turns with the four
        placeholder personas; speakers chosen by the director; one
        interaction beat that opens the microphone and absorbs the
        reply — with the real talk button and microphone, which also
        closes 3.3's check by hand (hold, the press cap, a window left
        unpressed); sentences accumulated, not split. Judged with the
        captions off (the follow-up "Events the listener cannot hear").
        The owner listens; the verdict is recorded here.
      - [x] **3.4b Your words in the captions, with Whisper's confidence
        per word** (added 2026-09-25 at the owner's request, after 3.4;
        its shape discussed before building; done the same night, the
        fork's `500debe`; suite 1011 passed, Node tests 17 + 91 + 31).
        As built, with the owner's picks: the label `You:`; three bands
        by Whisper's word probability (plain from 0.80, a dotted
        underline from 0.50, dimmed with a wavy underline below), the
        percentage on hover; the words to the page only (the round
        request and the record keep the text and two averages); the
        filter's verdict added to the caption when the next summary
        says silence ("You: Thank you. (counted as silence: a known
        Whisper hallucination)" — seen live); the caption under the
        invitation's lines. Checked with a fake microphone, then by the
        owner talking to the show (run `2026-09-25T23-43-42`); from the
        owner's check, the hover moved to a CSS tooltip (the `title`
        tooltip did not show) and the wavy underline stopped breaking
        under descenders (`text-decoration-skip-ink: none`); approved
        with the owner's commit order. The page shows what the
        listener said as a caption line, each word marked by how sure
        Whisper was of it. Found while shaping it: the show's Whisper
        server already returns every word with its probability in the
        plain `json` the app asks for (`segments[].words[]`: word,
        start, end, probability — e.g. "Hello 0.87 · Samantha, 0.80 ·
        are 0.97 · you 1.00 · there? 1.00"); the fork's
        `transcribe_for_show` keeps only the text and two averages today.
        *Done when:* the owner, talking to the show live, sees the words
        and their confidence and approves; then the branch is committed
        and pushed.
      - [x] **3.4c The listener's exchange — Contact mode, the receiver
        story, the emotional overtone** (added 2026-09-26 at the owner's
        call; discussed before any code in [discussion 2026-09-26]
        show-director-modes, from the owner's 2024 design). **Scope ruled
        2026-09-26** (its §10): Contact mode — after the listener speaks,
        several exchanges with a listening window after each; the
        receiver story — the beats Repair, Breakdown and Switch-off, a
        repeating orientation round (the sign-on at round 1 its first;
        added while shaping, the owner's idea), and the silence rule
        (two silences in a row switch the receiver off); the listener
        kept in the story — an aftermath round after each contact, and
        a periodic recollection round (the owner's idea) in which the
        cast talk about what a caller told them and how that caller
        could help if they call again;
        the contact agenda — what the cast wants from a listener, one
        item per exchange; remembering the listener — each agenda item
        asks for something or, once the listener gave it, uses it, and
        each contact instruction restates the listener's words; the
        emotional overtone — moods and tone words split into positive,
        neutral and negative, one overtone per round constraining both.
        Every number in settings, none hard-coded. **Its details are
        being ruled one at a time** (its §12; Contact, the receiver
        story, the agenda, the overtone, the exit criterion, the page
        and the mechanics done, §13-§18 — the remaining mechanics are
        the agent's picks at build, recorded for review); **the build
        is under way** (the build plan below; 3.4c.1-3.4c.4 done), then a
        driver test on the box, and the owner by ear. Resolves the follow-up
        "The listener's exchange is one line". **Done 2026-09-28** (the
        fork's `b988672` … `1ab5d6f` on `alfre2v/show-slice-3-browser`):
        the four checks passed and the show re-proven by the owner's ear on
        the timebox's last day (3.4c.5); 3.4c.6 and 3.4c.7 built; 3.4c.8
        dropped; the follow-up deleted, SED §5.7's dated note and the
        discussion's addendum written.
        - **To confirm when building:**
          - the re-call repeats the question that went unanswered
            ("Alfredo? Are you still there? We asked where you are.")
            — very likely, the owner's call (2026-09-26); built in
            3.4c.3, to confirm by ear;
          - the restatement's wording and the agenda's list (the name
            item first, then two-branch sentences) — the agent drafts
            both, the driver test on the box shows what the model does
            with them, the owner reviews both before the test by ear
            (the owner's call, 2026-09-26);
          - ~~the tone words' single-word exceptions (the whole groups
            are sorted — its §16.5) and the events' sort by overtone
            (by group, then single events) — the agent drafts, the
            owner reviews~~ — drafted in 3.4c.1 and committed on the
            owner's order (below).
        - **The build plan** (the agent's shape, the owner's Go,
          2026-09-26: "Go with your picks"): five sub-steps on the
          fork's `alfre2v/show-slice-3-browser`, one commit each on the
          owner's order after review; the story's data first, so the
          owner reviews the authoring while the rest is built; the old
          round kinds (`invitation`, `answer`, `static`) stay loadable,
          so `runs/` and the test fixtures keep working; the old story
          shapes (a flat `tones.yaml`, a flat `events.yaml`) are
          dropped; the box kept up through Sunday (only 3.4c.5 strictly
          needs it). The remaining mechanics are the agent's picks,
          recorded for review: a `listens` flag on each plan and round
          summary; the driver's `--heard` items answering every
          listening round in turn; the free rounds' line budget as two
          settings; the bookkeeping at 3.4c.5.
          - [x] **3.4c.1 The story's data** (`b988672`; suite 1028
            passed, Node tests 17 + 91 + 31). `overtones.yaml` replaces
            `tones.yaml`: the three overtones in order with their 14
            moods and 496 tone words under the 24 themes (positive 96,
            neutral 167, negative 233 — the ruled group table, then 29
            single words moved and 4 dropped because they became moods:
            hopeful, relieved, determined, curious — a tone word is
            never an emotion tag), the per-kind table, the drift weights
            1 : 2 : 3. `events.yaml` filed by overtone, then theme
            (positive 29, neutral 94, negative 166 — the agent's group
            table, then 81 single events moved). `agenda.yaml`: nine
            two-branch items, the name item first. The cast sheet: the
            premise sentence (so the system prompt changed; the pinned
            prompts in `tests/test_show_story.py` updated and dated),
            the orientation's facts, a stage direction per receiver
            beat. The loader reads and checks all of it; the director
            still draws from the flattened events and tones until
            3.4c.3. Reviewed by the owner, committed on the owner's
            order.
          - [x] **3.4c.2 The grammar and the settings** (`5c0c2a3`;
            suite 1055 passed, Node tests 17 + 91 + 31).
            `build_grammar` gains a minimum line count and one pinned
            speaker — `first` (the addressed character opens, the other
            speakers follow: exchanges, the Breakdown, the Switch-off,
            the orientation) or `last` (the others lead up to the
            operator's call: the Repair); without pins it is still byte
            for byte the grammar proven on 2026-09-22. `ShowConfig`
            gains the fifteen settings of 3.4c with the ruled defaults:
            `free_lines` / `free_line_weights` (1-4 weighted 1:3:3:1 —
            the director now reads them instead of two constants, the
            same draws), `overtone_hold` / `overtone_jitter` (4 / 1),
            `contact_exchanges` / `contact_jitter` (3 / 1),
            `contact_min_lines` / `contact_max_lines` (2 / 3),
            `silences_to_switch_off` (2), `beat_max_lines` (2),
            `orientation_every` / `orientation_jitter` (20 / 5),
            `recollection_every` / `recollection_jitter` (15 / 5),
            `restatement_contacts` (5); checks for the contact's range
            and the free budgets. The rest of the settings are read from
            3.4c.3 on; the system prompt's mood list becomes the story's
            14 then; their runbook lines come in 3.4c.4. Committed on the
            owner's order.
          - [x] **3.4c.3 The director and the record** (`4d0d7dd`;
            suite 1077 passed, Node tests 17 + 91 + 31). The director
            v2 (`app/show/director.py`): the sign-on and repeating
            orientations; free rounds whose event slot holds an event,
            an aftermath or a recollection; the Repair on the cadence,
            counted from the moment the receiver went off; exchanges
            (the named character first, else whoever asked last; the
            next agenda item; the restatement, earlier contacts
            included); the Breakdown after N answers; re-calls and the
            Switch-off; each round's overtone from its kind's table or,
            for free rounds, a held drift to neighbors, with moods, tone
            word and event following it. The record: the new kinds (the
            old three still load) and `overtone`, `agenda`, `slot`,
            `recollects`; the round route listens after any round that
            listens and reports `listens`, `overtone`, `agenda`, `slot`,
            `direction`; the system prompt lists the story's 14 moods.
            **Smoke on the box** (the fork's run `2026-09-26T16-28-02`,
            no listener, calls at 20-40 s): 14 rounds, 24 lines, 0
            dropped, about 1.35 s a round; llama.cpp accepted every new
            grammar; the pins held (the Repair closed by Samantha's
            call); the moods stayed in each round's overtone. **The
            agent's picks at build, reviewed by the owner:** the
            aftermath comes before a due orientation (immediacy); an
            orientation comes after N free rounds; a re-call is one line
            and repeats the unanswered question (built; still to confirm
            by ear, above); exchanges and Breakdowns take exactly the
            drawn 2-3 lines; every kind carries a tone word from its
            overtone; each instruction names the allowed moods; the
            Repair and the Breakdown also give the model the story's
            stage direction. **One pick replaced by the owner:** the
            recollection's gap was counted from the last aftermath, so
            each contact reset it — measured, recollections came only in
            long stretches (112 in 20 runs of 300 rounds with the
            defaults, none with calls at 20-40 s); the owner: "a, the
            independent count with both guards" — the count runs from
            the last recollection, never directly after an aftermath,
            and never the caller talked about last while there is
            another (then 276, and 195 at 20-40 s; talk about callers
            about doubles — the default may want raising after the test
            by ear). **Wording notes for 3.4c.5**, from the smoke: the
            sign-on did not tell the receiver facts ("We're broadcasting
            from Sector B, lab 7…"); a re-call gave up ("We'll try again
            later."); one line had markdown emphasis ("Answer us,
            \*now\*!"). Until 3.4c.4 the page and the driver still
            listen only after the old `invitation` kind. Committed on
            the owner's order.
          - [x] **3.4c.4 The page and the driver** (`90ec1e8`; suite
            1082 passed, Node tests 17 + 91 + 34). The page listens
            after any round whose summary says `listens` (the call, an
            exchange, a re-call), the "You:" caption under that round;
            the RECEIVER sign (green, beside ON AIR) lights when the
            last line of a round that listens starts and goes dark when
            that of one that does not starts (the Breakdown, the
            Switch-off), with a fallback at the drain; a receiver beat's
            stage direction above its lines; the debug line gains the
            overtone, the slot, the agenda item and a contact's answers
            ("answers 2 of 3" — the director and the round summary now
            report `answers`, the agent's addition for that line). The
            driver answers every listening round with its `--heard`
            items, prints those facts under each round, and its
            checkpoint report counts answered calls and re-calls or
            Switch-offs. The fork's runbooks (a new "How the show runs"
            in `show-page.md`; the 3.4c settings and the checkpoint in
            `show-driver.md`) and `AGENTS.md` updated. **On the box**:
            the runbook's checkpoint drive (the fork's run
            `2026-09-26T16-51-06`, seed 42, the listener spoken by the
            TTS and heard by Whisper) passed 6 of 6 — two calls, two
            exchanges, three re-calls, two Switch-offs, an aftermath, the
            trim five times, 42 lines, 0 dropped; its output is now the
            runbook's example. **More wording notes for 3.4c.5**: an
            exchange talked about the listener instead of to them
            ("They're asking if anyone's alive."); the aftermath misread
            Whisper's "Moira is the virus airborne." ("If she's
            airborne, we might not make it."); markdown emphasis again
            ("it's \*us\*"); the sign-on again without the receiver
            facts. Committed on the owner's order.
          - [x] **3.4c.5 The four checks** (below), then the
            bookkeeping: SED §5.7's dated note, the follow-up "The
            listener's exchange is one line" resolved, the discussion's
            addendum. **Under way (2026-09-26, evening):** check 1 green
            (suite 1082, Node 17 + 91 + 34). Check 2, the driver test:
            a scripted listener (Alfredo, then Maria, then Alfredo back
            with a silence, then a call nobody answers) on three seeds
            (42, 7, 2026), calls at 20-40 s, contacts of exactly 3
            answers, before and after a wording pass (the fork's runs
            `2026-09-26T17-00-46` … `T17-07-23`). Old wording → new:
            the sign-on told the receiver facts 1 → 3 of 3; exchanges
            ended on a question 7 → 11 of 18; a first-time caller
            welcomed back 3 → 1 of 3; Maria named 5 → 6 of 9; Alfredo
            named after giving it 4 → 4 of 6; the anonymous "Hello
            again, lab." taken for Maria 3 → 3 of 3 (reported at the
            time as 2 → 2, corrected on re-reading: the experiment's
            findings, below); every unanswered call Repair → re-call →
            Switch-off; no event inside a contact. The new wording
            committed on the owner's order (the fork's `e261b5b`).
            **B versus A — ruled (2026-09-26, 18:37):** at the owner's
            order, A simulated with perfect extraction (a fact table for
            the scripted sentences, swapped in at launch, the fork
            untouched) on the same script and seeds: the anonymous voice
            taken for Maria 0 of 3 (the cast asked who it was); Alfredo
            named across his return 7 of 12, against 3 of 12; the rest
            within noise. The owner: "We are going to do: "a. B for
            3.4c; names-only A becomes a show fix before the talk, with
            the follow-up updated."" — B stays in 3.4c; names-only A is
            shaped and estimated in the follow-up "A listener memory
            keyed by identity". The scripts, the nine runs and the
            findings: [experiment 2026-09-26] listener-memory-b-vs-a
            (`docs/experiments/2026-09-26-listener-memory-b-vs-a/`).
            **Check 3 passed** (19:03; the fork's run
            `2026-09-26T18-59-43`, the fake microphone in the page): a
            full contact and an unanswered call to the Switch-off; the
            RECEIVER sign, the beats' directions, the captions and the
            debug line's fields as designed; a silent window leaves no
            caption — kept as built (the owner). **The radio beats
            reworded** at the owner's call after check 3 ("It is very
            annoying that the LLM does not explain what is going on with
            the radio"): two measured rounds ([experiment 2026-09-26]
            radio-beats-wording), the second kept (the fork's
            `3c4154c`): the Repair says the lab can hear them 2 → 21 of
            21, the Switch-off says the receiver is going off 5 → 12 of
            12; "we can't hear you" after a Breakdown or a Switch-off is
            still mostly missing — for the ear test. The Breakdown takes
            a new setting, `breakdown_lines` (3); the Repair and the
            Switch-off take `beat_max_lines`. **Check 4 passed**
            (2026-09-27, 00:34-01:05, the owner's call; the fork's run
            `2026-09-27T00-34-00`, 63 rounds, in Chrome with the real
            microphone: 16 answers over six contacts, then a call left
            unanswered — Repair, re-call, Switch-off, rounds 58-60). The
            owner's verdict, verbatim: speaking directly — "Yes, big
            improvement in this front. It's not perfect, but much
            better."; the Switch-off — "It's bad, they do not mention
            anyone by name, they don't even clearly explain what is
            happening "We're turning it off to conserve power, we can't
            keep this up forever. Over." ... Turning what off? Huff.";
            "The radio breaks too fast, we should leave more turns of
            interaction on average before the radio breaks."; "On each
            event, there is no way that the LLM actually describes what
            happened to the listeners. I think we will have to create a
            type of simple line that is not generated by the LLM, that
            just read the event text as one of the cast."; and
            "\*crackle\*" in almost every call. Read in the run: the
            Breakdown answered first in 0 of 6 and said the lab cannot
            hear in 1 of 6. The fixes: step 3.4c.6. **Re-proven by ear on
            2026-09-28** (13:43-14:12, the owner in Chrome with the real
            microphone, debug on; the fork's `1ab5d6f`, run
            `2026-09-28T13-43-28`: 113 rounds, about 13 minutes of audio,
            four contacts with 23 answers, four Breakdowns, one unanswered
            call to the Switch-off, the sign-on and three orientation
            repeats; 55 fixed lines, 215 model lines). The owner's verdict,
            verbatim: "Wow, big improvement in story coherence. The system
            prompt improvement is clearly strengthening the story
            narrative... And the more the user adds details about zombies
            the more the model plays along. Week parts still, the in the
            exchange rounds the model never remembers who they spoke to
            before, but if you ask about who contacted them, they suddenly
            remember. So it is nemotron's limits. But this is not something
            to fix today. All in all I am satisfied with where we are."
            Repeats: "I did not see a single case of repetition in the app
            run we did." — measured, 0 of 215 model lines at 0.9
            similarity or more to one of the four lines before. Two
            details asked about and left as they are (the owner): a
            speaker twice in a row in rounds 103 and 106 (the grammar
            allows it; "it adds a bit of unpredictability"), and an event
            heard on the frequency after the Switch-off (round 112; noted
            in the follow-up "Event texts reworded as lines of dialog").
            The bookkeeping done the same day.
          - [x] **3.4c.6 Fixed lines** (`07669dc`; added 2026-09-27 after check 4,
            the owner's idea; shaped one decision at a time, the owner:
            "Go with all four as shown", "Go with beats.yaml, four
            versions each, as shown", the who and the mood as proposed —
            the event line's mood from the round's overtone, which also
            picked the event — then "Go with your picks, build it now").
            The lines the listener must not miss are said word for word
            by the cast instead of written by the model: an event, read
            by the round's first speaker, the model writing the rest;
            the call, both lines, with no model request; the Breakdown's
            closing line, the operator's, after the model's answer and
            reaction; the Switch-off's opening line, the operator's,
            then one reaction. The texts: the event's own, and the
            story's new `beats.yaml` (four versions each, drawn without
            repeats — the agent's draft, for the owner's review). A
            setting, `fixed_lines` (on; off, the model writes every
            line); fixed lines recorded with a `fixed` flag and streamed
            as ordinary line events, so the page is unchanged. Ridden
            along: `contact_exchanges` 3 → 5 (the owner: "The radio
            breaks too fast"). Suite 1106 passed,
            Node 17 + 91 + 34. **On the box** (three drives of the saved
            driver script, contacts of 3 kept temporarily so the
            scenario matches the earlier ones; the fork's runs
            `2026-09-27T01-59-04`, `T01-59-43`, `T02-00-26`): every fixed
            line in place (the call 21 of 21, the Breakdown 9 of 9, the
            Switch-off 12 of 12, events 17 of 17); the Breakdown answered
            the voice first in 5 of 9, and sometimes says the failure
            before the operator's line repeats it; rounds 0.94-1.04 s on
            average (1.31-1.36 before), the call no longer asking the
            model. Follow-ups written: the event texts reworded as lines
            of dialog, and more agenda items (both the owner's).
          - [x] **3.4c.7 Fixed lines kept out of the model's own turns**
            (the agent's idea, 2026-09-27; the owner, 2026-09-28: "It is
            a great idea. Let's implement it. But before implementing,
            record well this idea and the reason why we need to try
            this."). **The idea:** in the script the model reads back,
            its own turns hold only the lines it wrote; a fixed line is
            quoted in a user turn, as something a character said.
            **Why — the evidence.** In the owner's listen of 2026-09-27
            (the fork's run `2026-09-27T02-06-50`), round 25: Ralph read
            the event ("A rack falls in the virology lab, and one test
            tube keeps rolling across the floor.") and Moira repeated it
            word for word; round 24 opened by echoing round 23's last
            line ("Of course it is." → "\*Of course\* it is."). The
            messages the model received, rebuilt from the record with the
            route's own code: every earlier event round's user turn says
            "Moira has just told them on air: "…" Carry on from there.
            Daniel speaks next: the next line", yet the assistant turn
            after it — the record replayed as if the model had written it
            — opens with that same line, then Daniel's: a reply that
            repeats what was just quoted, and two lines where one was
            asked. Nine such rounds taught the habit; the model then
            repeated the event itself, and echoed the line before in plain
            rounds. The owner's reading (verbatim, 2026-09-27): "I think
            the model does not understand the introduced line as it did
            not generated it." Measured over the driver runs and the
            owner's listens: a round opening with the last line before it
            2 of 179 rounds before fixed lines, 4 of 141 with; the model
            repeating the event 0 of 29 before, 1 of 26 with — rare, but
            heard. **The design** (the agent's picks, for review): the
            assistant turn carries only the model's lines; fixed lines
            said before them are quoted in the round's own instruction
            (the events and the Switch-off's already are; the call's
            instruction quotes its two lines); fixed lines said after
            them (the Breakdown's closing) are quoted at the top of the
            next user turn; a round with no model line joins the next
            user turn, so user and assistant turns still alternate. **The
            check:** the suite; three drives of the driver script, as for
            3.4c.6 — every fixed line still in place, the echo counts
            reported; then the owner by ear. The repeat guard (3.4c.8) is
            the safety net for what remains.
            **Built, then reshaped with the owner case by case** (the
            fork's `4d051ba`, 2026-09-28; the whole review in [discussion
            2026-09-28] prompt-sweep). A real run of the first build
            showed the word "round" reaching the model twice and the
            call, folded into the next turn in the present tense, read as
            an order to do it again; the owner: "Stop modifying the model
            instructions. Instead I will do it case by case." The
            outcome: the model's own turns hold only its lines; the call
            is told as already said, in the words an event's reading
            uses, and runs on with "Then" into the voice's answer or the
            silence; an event round always leaves the model a line; the
            Breakdown is split in two — the contact's last answer gets
            the last exchange (answered, asking nothing, no listening
            window), then the Breakdown as a receiver beat of its own
            (the operator's fixed line told like an event's reading, then
            a reaction, on `beat_max_lines`; `breakdown_lines` removed);
            the RECEIVER sign stays lit through the last exchange (the
            round summary's `receiver`); no instruction speaks of rounds.
            Suite 1109 passed, Node 17 + 91 + 35. On the box (the fork's
            run `2026-09-28T11-50-15`): the first exchange after the call
            no longer re-announced the receiver; the last exchange
            answered by name but still asked questions (an open point of
            the sweep); the Breakdown one clean beat. The sweep continues
            over every other prompt case (the discussion's checklist).
            **The sweep, the rest of 2026-09-28** ([discussion 2026-09-28]
            prompt-sweep, §3.4-§3.8): the system prompt's premise says who
            a voice on the frequency is, what the scientists tell the
            listeners (the owner's own sentence) and where the lab stands,
            as flavour (the fork's `432a378`); an orientation tells the
            receiver as it went off — dead, or switched off after a
            Switch-off (`1ab5d6f`); the owner's ruling (13:14): invented
            details are a feature, the model's improvisation is what the
            project probes; the last exchange may end on a question (the
            owner: "in the story they do not know the radio will fail
            next"); the fixed lines audited — none reaches the model's own
            turns — and a past-tense rewording of their context tried in a
            seeded A/B test and rejected. The remaining cases are not
            planned; the owner's listen of 2026-09-28 closed the day's
            goal (3.4c.5).
          - [~] **3.4c.8 The repeat guard** — **dropped 2026-09-28** (the
            owner: "Yes, repetitions seem to be gone: I did not see a
            single case of repetition in the app run we did. So, we drop
            the 3.4c.8, the repeat guard."; measured in the owner's
            listen, 0 of 215 model lines at 0.9 similarity or more to one
            of the four lines before). Was: the agent's proposal, the
            owner, 2026-09-27: "we will build the repeat guard
            tomorrow" — a line the model writes that nearly repeats one
            of the last few lines, fixed ones included, is dropped before
            it reaches the page — not shown, not spoken, not in the
            script, logged as dropped; the threshold in settings. Keeping
            fixed lines out of the model's own turns (3.4c.7) removed the
            cause.
        *Done when* (its §17.12): (1) the suite and the three Node
        tests are green; (2) the driver test on the box — scripted
        conversations and a report with numbers, from which the owner
        decides whether B is enough; (3) a fake-microphone check in the
        page; (4) the owner by ear with the real microphone — a full
        contact where the cast engages, and a call left unanswered
        until the Switch-off; the verdict recorded, then commit and
        push.
      - [x] **3.5 Close the timebox** — slice 3's pull request merged;
        tag `tz-0.2`; the installer's `client_version` bumped to it and
        re-proven (fresh install, re-run `changed=0`, HTTP 200 — the
        owner's deploy); the spec's as-built entries for the engine.
        **Done 2026-09-28:** the owner merged both pull requests
        (alfre2v/TalkWithZombies#4 → `ca37199`; this repository's #12
        → `2841065`); `tz-0.2`, an annotated tag on `ca37199`, pushed
        on the owner's order; `client_version` → `"tz-0.2"`
        (`deploy/ansible/client-talkwithme-mac.yml`, lint clean on the
        `production` profile). The owner's re-proof on the laptop (the
        old install moved aside): "All four checks pass, installed at
        tz-0.2." — a fresh install, a re-run with `changed=0`, `git
        describe` at `tz-0.2`, the show page answering HTTP 200 on a
        test port. The spec: not as-built entries but a rewrite — the
        product definition is now one linear description of the product
        as built (this repository's `5692052`; the owner: "The
        specification is not a log, it should read as the guide to
        build the product."). Found in the owner's listen of the
        installed client (run `2026-09-28T15-31-44`, 189 rounds): the
        trim fires every 22-36 rounds and costs about 5 s, and one
        unexplained long silence — recorded as follow-ups (the trim's
        thresholds in settings; a budget near 16k; a 32k context; the
        silence).

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
- **How the arc's boundary shifted** (moved from the top of this
  file, unchanged):

**NOT in this arc (deliberate boundary, 2026-09-17):** the
ensemble-director design ([spec §6]), story/episode authoring,
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
(2026-09-22); the fork exists (Task 6a, done 2026-09-23); the show
engine is next (Task 6b).


## Standing cross-arc notes

- Hard deadline **2026-10-08** (the talk at the Austin Python Meetup
  is in October 2026): ~3 weeks out at
  arc open, when the prototype was the critical path and D1's 3-day
  timebox its first checkpoint; ten days out on 2026-09-28, with the
  show engine and its looks done and Task 7, the canned episode (a
  MUST), still open.
- Keep the last 2–3 branches, local and remote (owner rule,
  2026-09-16).
- Ops rules that carry over: never hibernate a show box · proven
  images: `R570 CUDA 12.8 with Docker` (Ubuntu 24.04, 2026-09-18)
  and `Ubuntu Server 22.04 LTS R550 CUDA 12.4 with Docker`
  (2026-09-19 and 2026-09-22) · a fresh box may spend its first
  hour in Ubuntu's own updater (the deploy now waits 5 minutes for
  the apt lock, then stops with a clear message) · on-demand,
  never spot · destroy-vs-keep is a per-evening cost call.
