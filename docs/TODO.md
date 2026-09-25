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

**Arc boundary, in one line:** the show engine's design was pulled
into this arc on 2026-09-21 and is now decided; story and episode
authoring and the full demo rehearsal stay with the next arc, "the
show arc". The full story of the boundary shift is under "Done in
this arc".

## Now — where the arc stands

*Updated 2026-09-24, evening. Read this section first; everything
below it is detail.*

- **The critical path is Task 6b, the show engine,** built in the
  fork TalkWithZombies under a 3-day timebox — clock started
  2026-09-23 14:46 CDT · checkpoint 2026-09-25 02:46 (in practice
  that morning) · end 2026-09-26 14:46. Its design is fully decided
  ([discussion 2026-09-23] show-engine-design); its ordered checklist
  is the next section but one.
- **Slice 1 is done and merged** (2026-09-24; ten real rounds ran on
  the box through the app). **Slice 2 is built and the checkpoint
  passed** (2026-09-24 ~18:57, about eight hours ahead of its clock:
  6 of 6 criteria; **verdict: continue**). All six steps are done
  and proven on the box: 2.1 director v1 (`ce8bd71`), 2.1b the
  pacing knobs (`2f76b34`) and tone words that do not repeat
  (`35f34e0`), 2.2 the trim (`57a08c9`, about 1.5 s once per trim),
  2.3 the debug switch (`129d3de`), 2.4 the listener's turn on the
  server (`d6ab1b9`), 2.5 the driver extended (`86dc1df`). **Its
  pull requests are open:** alfre2v/TalkWithZombies#3 and this
  repository's for `alfre2v/show-slice-2`. **Next:** the owner
  merges them; then slice 3, the browser, on a branch cut from the
  fork's fresh `master` (target: the end of the timebox). How to
  drive the show yourself, and run the checkpoint: the fork's
  `docs/runbooks/show-driver.md`.
- **The order after the timebox:** Tasks 5a / 5b / 5c in the new
  engine (5a needs the owner's character bibles, 5b the voice
  samples) → Task 7, the canned episode (a MUST for the talk) →
  Task 8, the close ritual. Hard deadline 2026-10-08; the talk at
  the Austin Python Meetup is in October 2026.
- **In parallel, the owner's long pole — Task 4:** the character
  bibles (they land as the cast entries of the fork's
  `stories/lab-outbreak/cast_sheet.md`) and the voice samples. No
  dependency on the build; any day, box or no box.
- **The box** (the A6000) **is up**: on 2026-09-24 a first wake
  failed (Hyperstack had no A6000 in stock), a later one succeeded
  on the same address, and the llama.cpp and Whisper images are now
  pinned (owner action queue, item 5). Slice 3 needs it for its exit
  criterion by ear (3.5) and the installer's re-proof (3.6).
- **At a session's end:** a fresh-session handoff replaces any
  mid-session one, and a handoff is deleted only with the owner's
  permission.

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
   show's cast sheet ([spec §5.3]) — concretely, each character's
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
5. **The Hyperstack VM — hibernated, woken per box session.** Woken
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

## The critical path — Task 6b

- [ ] **Task 6 — The fork and the show engine: TalkWithZombies
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
  - [ ] **6b — Build the show engine, as three slices. NEXT.**
    **Read this first.** The design is decided and lives in
    [discussion 2026-09-23] show-engine-design — cited below as
    **SED §n** — with its roots in [ADR-0003], [spec §5.3], and the
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

    - [ ] **Slice 2 — the rules** (built 2026-09-24, all six steps,
      the checkpoint passed that evening; its pull requests await the
      owner's merge). Branch
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
      - [ ] **Slice 2 pull request** — alfre2v/TalkWithZombies#3
        (opened 2026-09-24) and this repository's pull request for
        `alfre2v/show-slice-2`; the owner reviews and merges.

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

    - [ ] **Slice 3 — the browser.** Branch
      `alfre2v/show-slice-3-browser`, cut after slice 2 merges.
      **Target: the end of the timebox, 2026-09-26 14:46.**
      - [ ] **3.1 The SSE reader, extracted** — from `sendMessage`
        (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/chat.js:135-159`)
        into `static/sse.js`, shared by the chat and the show. *Done
        when:* the chat UI still works end to end and upstream's Node
        tests stay green. *Delegable later: yes* (a mechanical
        refactor).
      - [ ] **3.2 The `/show` page and `show.js`** —
        `templates/show.html` including `state.js`, `tts.js`,
        `stt.js`, `persistence.js` and the new `sse.js`; `show.js`:
        idle → generating → playing → listening; the next round
        requested when the audio queues drain, with the played
        seconds; listening only when the director asked.
        ([discussion 2026-09-21] story-loop §5.) *Done when:* by hand,
        the states cycle and the next round is requested on drain
        (visible in the console). *Delegable later: no.*
      - [ ] **3.3 The accumulator** in `static/tts.js` — about 100
        characters, whole sentences, ~20 % tail tolerance, a hard
        flush at each line end ([discussion 2026-09-21]
        task6-recon-talkwithme, around line 617). *Done when:* "Dr.
        Byrne. 47. Microbiology. Over." leaves as one chunk; a
        180-character sentence goes whole and alone; the line end
        always flushes. *Delegable later: yes*, once the follow-up's
        Node test exists.
      - [ ] **3.4 Hold-to-talk and the listener's path** —
        `static/stt.js`: press to record, release to end, enabled
        only while listening; the waiting window stops counting on a
        press; the press cap; the upload with the show's Whisper
        parameters; the transcript sent with the next round; "Heard:
        …" only while `show.debug` is on. (SED §5.7, §6.7.) *Done
        when:* by hand — the button works only while listening, and
        an answer follows a spoken question. *Delegable later: no.*
      - [ ] **3.5 The exit criterion, by ear** — on the deployed
        stack through the tunnel, per the timebox terms above: at
        least ten unattended turns with the four placeholder
        personas; speakers chosen by the director; one interaction
        beat that opens the microphone and absorbs the reply;
        sentences accumulated, not split.
      - [ ] **3.6 Close the timebox** — slice 3's pull request merged;
        tag `tz-0.2`; the installer's `client_version` bumped to it
        and re-proven (fresh install, re-run `changed=0`, HTTP 200);
        the spec's as-built entries for the engine.

    - [ ] **Polish — only if the checkpoint was green**, in this
      order: dead-air static through a second AudioContext source
      while a round is in flight; the 1930s radio look with the
      owner's gauge (a "magic eye" or a VU needle driven by Web
      Audio's analyser — the microphone while the button is held,
      the actors' audio while it plays — SED §6.7); prefetch round
      N+1 when the last line of N starts playing; episodes (SED §2,
      the stretch).

## Other open tasks

- [ ] **Task 4 — Real cast replaces placeholders.** Character
  bibles → the sections of TalkWithZombies' cast sheet ([spec
  §5.3]; where they live in the fork — decided 2026-09-23: the
  cast entries of `stories/<story>/cast_sheet.md`, not the persona
  files — [discussion 2026-09-23] show-engine-design §4), keeping `/no_think`
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
- [ ] **Task 7 — The canned episode (owner MUST) + demo-day
  protocol runbook.** Recorded from the working prototype; the
  runbook promotion deferred from the last arc lands here. The
  seed makes retakes reproducible: on one server slot, the same
  request and seed gave the same words 80 minutes apart
  (2026-09-22) — record with the settings it will be replayed
  with.
- [ ] **Task 8 — Close ritual in the closing PR.** Features
  Shipped entry · task_history migration · TODO reset ·
  staleness sweep (CLAUDE.md included) · spec ledger audit
  (every settled decision has its as-built entry).

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
(2026-09-22); the fork exists (Task 6a, done 2026-09-23); the show
engine is next (Task 6b).


## Standing cross-arc notes

- Hard deadline **2026-10-08** (the talk at the Austin Python Meetup
  is in October 2026): ~3 weeks out at
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
