# Preparing the talk — the plan

**Date:** 2026-10-10 · **Arc:** MVP prototype · **Branch:** `alfre2v/talk-prep`
**Type:** plan — how the days before the talk at the Austin Python Meetup are spent: the slides, three study sessions
(the backend, the browser client, the debug data), the rehearsals, and the demo day's readiness.
**Status:** **DRAFT** — proposed by the agent, for the owner to inspect; iterated until agreed.
**Trigger to revisit:** each workstream's end; anything that moves the talk.

## §0. Why this document

The owner (verbatim, 2026-10-10), after listing five kinds of work — a pass over the slides, a study session of the
FastAPI backend, one of the JavaScript client, one of the debug data, and recording the talk to improve the delivery:

> I think it is best if you propose one document with the re-organized plan for preparation for the talk. That way we
> have something tangible to guide us... Feel free to draft a proposal, I will inspect it and we will iterate on it if
> necessary.

The study sessions are also the preparation for the questions after the talk: an audience of Python developers will ask
how things work, and the owner wants to answer from understanding, not from memory.

## §1. Where we stand

- **The app:** every feature planned for the talk is built and released — the fork's **`tz-0.9`**, re-proven by the
  owner on 2026-10-08 (the voices with emotion, the 32k context, the static bed, the compressed reference clips, the
  ambience, sound cues with 29 event sounds). Both demo machines proven: the A6000 in the cloud (hibernated since
  2026-10-08; a wake can fail), and the 3090 at home over the LAN (a long debug show and a recorded one on 2026-10-08,
  "the rtx3090 has hold its ground very well").
- **The deck** (`talk/`, Quarto, published on GitHub Pages): **25 slides in six sections** — the intro (9), the tech
  overview (2), the demo (2), the deep dive (6), built with an AI pair (3), the future and credits (3). Its time budget
  ([discussion 2026-10-03] the-talk §4.1): intro 5, overview 5, demo 10, deep dive 6-8, AI pair 4-5, future 1 — **about
  33 minutes, plus questions**.
- **Known slide work** (`docs/TODO.md`, Task 9): the "What's next" slide is stale (it still lists event sounds as
  future work); the numbers on slides 5 and 27 to recount; the A6000's price — **checked, right as it is** (the owner,
  2026-10-08).
- **Recording:** OBS Studio set up on 2026-10-08 (the full display; the Mac's sound through Desktop Audio Capture, the
  screen capture's own sound muted; the headset's mic; Chrome ducked under the voice). Thirteen recordings from
  2026-10-08 in `~/Movies/zombie-radio-rehearsals/` (outside git). Lessons: run `caffeinate -d` while recording (a
  locked screen freezes the capture), check the sound bar moves before each take.
- **Task 7's fallback video:** ruled by the owner on 2026-10-08 — the demo part cut from a recorded rehearsal.

## §2. The workstreams

### A. The slides

- **Why:** the deck was written before the ambience, the sound cues and the event sounds existed, and the owner
  suspects it misses parts of the app ("Do we even enumerate anywhere all the types of rounds we have in the app?... I
  don't think so").
- **Steps:**
  1. **The inventory (1.b first):** the agent lists every feature of the app, from the spec's §6 — the eight round
     kinds (orientation, free, repair, exchange, last exchange, re-call, breakdown, switch-off), the director's two
     modes (Broadcast, Contact), fixed lines, events, tones and overtones, the trim, the listener's turn and the
     transcript filter, the seeds, the looks, the four levels of sound, the cues, debug mode — and marks the slide that
     covers each. A table, in this document or beside it.
  2. **The owner decides,** feature by feature: on a slide, said aloud only, a backup slide, or left out. The 33
     minutes are the constraint: what does not fit the talk can go to **backup slides after "Thank you"**, ready for
     questions (the eight round kinds are a natural one).
  3. **The four levels of sound immersion (1.a):** the static bed, the ambience's textures, its spots (and the cues),
     the cast's voices — a simple diagram of four stacked bands, in the deck's own HTML/CSS. Where it goes: the
     owner's call.
  4. **"What's next" rewritten:** what is now built comes off it; what stays future is the follow-ups (live sound
     generation, new events, the judge in the loop, the client on Linux…).
  5. **The recount** of "slides 5 and 27" — as Task 9 and the handoffs name them; the deck now has 25 titled slides,
     so which slides those are is checked first (a title slide or a different count may explain it).
  6. **Republish** (`docs/runbooks/talk-slides-quarto.md` §10) and look at it on the published site.
- **Done when:** the inventory table is ruled on, the slides are changed, the site is republished, and the owner has
  clicked through it once.
- **Estimate:** the inventory about 45 minutes (the agent); the slides 1-2 hours together.

### B. Study session: the backend (FastAPI)

- **Why:** to understand the app's server well enough to answer any question about it, and to see its load-bearing
  parts with one's own eyes.
- **Steps:**
  1. **A one-page map first** (the agent prepares it): the show's modules in the fork's `app/show/` (`story`,
     `director`, `grammar`, `parser`, `script`, `listen`, `bed`, `cues`, `debug`) and `app/routers/show.py`; the
     abstraction each holds; and **the path of one round**, from `POST /api/show/round` to the record on disk.
  2. **The routes** the page uses (2.b): `POST /api/show/start` (open a run), `POST /api/show/round` (play a round,
     an SSE stream), `POST /api/show/listen` (the listener's recording), `POST /api/tts` (a chunk of a line's voice),
     `GET /api/show/bed/{name}` and `/api/show/ambience/{name}` (the sounds); what each receives and returns.
  3. **The owner's questions** (2.a), at any point; the agent answers with `file:line` receipts.
  4. **The load-bearing parts** (2.c), chosen by the owner from the map — likely the director's plan of a round, the
     grammar, the stream parser, the trim, the run's record.
  5. **The fundamental abstractions** (2.d), named and located — written into this document's §4 as the session's
     result, in the owner's words where possible.
- **Done when:** the owner can trace one round end to end without the map.
- **Timebox:** 60-90 minutes.

### C. Study session: the browser client (JavaScript)

- **Why:** the browser is the show's clock — it decides when a round is asked for, plays the voice, listens, and
  mixes three kinds of sound; half of the app's behaviour lives there.
- **Steps:**
  1. **A one-page map first:** the page's scripts in `static/show/` (`show.js` — the state and the round loop;
     `sse.js` — reading the stream; `player.js` — the voice queue; `mic.js` — push-to-talk; `bed.js`, `ambience.js`
     — the sounds; `gauge.js` — the level for the looks), the page's states (idle, thinking, on air, listening,
     recording, hearing, stopped), and **the audio graph**.
  2. **A refresher of the Web Audio API** (3.b), on the app's own graph: `AudioContext`, `GainNode` (levels, mutes,
     fades), `BiquadFilterNode` (the AM filter), `MediaElementAudioSourceNode` (the bed and the ambience's clips),
     `AudioBufferSourceNode` (the voice's chunks), `AnalyserNode` (the gauge); why a page cannot play sound before a
     click.
  3. **The owner's questions** (3.a), with receipts.
  4. **The load-bearing parts** (3.c) — likely the round loop and its states, the voice queue, the listening window,
     the wraps of `setState` by `bed.js` and `ambience.js`.
  5. **The client's functions and data structures** (3.d), named and located, into §4.
- **Done when:** the owner can say what happens in the page from "Start" to the first line heard.
- **Timebox:** 60-90 minutes.

### D. Study session: the debug data — and the pauses

- **Why:** debug mode keeps a show's whole story (the record, every request to the model, every voice chunk), and an
  open question needs it: the **pauses of about 300 ms** the owner heard on the 3090 on 2026-10-08, growing as the
  show went on, mostly when the mic opened or closed — OBS suspected, not shown.
- **Steps:**
  1. **The run's folder** (4.a): `runs/<run-id>/script.json` (the record: each round's kind, speakers, event, tone,
     lines, timings, cue…) and `debug/` (`rNNN.txt`, `rNNN.request.json`, `audio/` — every chunk with its `.json`);
     the most useful fields, on the owner's long 3090 run (`~/TalkWithZombies-client/runs/`).
  2. **The console** (4.b): every message debug mode writes in the browser — the voice, the bed, the ambience, the
     cues — listed once.
  3. **The pauses:** from the run's timings, where the gaps are and whether they grow; then a short run with OBS
     closed and one with it recording, to test the suspicion.
  4. **Easy improvements** (4.c) — once the owner has seen what is there; candidates: each line's timings in the
     console, the gap before each line, the console grouped by round.
- **Done when:** the owner can find any line's voice, request and timings in a run's folder; the pauses have a cause
  or a measured "not OBS".
- **Timebox:** 60 minutes (the pauses may want more).

### E. The rehearsals

- **Why:** the owner, after the first recording (2026-10-08): "I am very disappointed with myself, I am not an
  effective communicator. I will have to practice giving the presentation at least 3 times I guess."
- **Steps:**
  1. **A baseline:** one of the 2026-10-08 recordings (the owner names it), **transcribed with Whisper** (on the 3090,
     or on the Mac). The agent cannot watch a video, but can read a transcript: the pace (words a minute, per
     section), the filler words, the time per section against §1's budget, where an explanation circles, where a step
     the audience needs is skipped.
  2. **Three sentences per section:** before rehearsing again, the owner says each section's point in three sentences
     — the agent helps tighten them; they become the speaker's notes.
  3. **Rehearsal 1, recorded and timed** (OBS, `caffeinate -d`, the 3090 for the demo), transcribed, measured against
     the baseline.
  4. **A Q&A drill:** the agent plays the audience (why not cloud AI APIs, what it costs, how the model is kept from
     breaking format, the licences of the voices and sounds, what the AI pair did and did not do) — the owner answers
     aloud. The study sessions (B-D) prepare it.
  5. **Rehearsals 2 and 3,** each transcribed and compared.
  6. **The fallback video:** the demo part cut from the best rehearsal (Task 7).
- **Done when:** a rehearsal fits about 33 minutes, the owner is content with it, and the fallback video is cut.

### F. The demo day's readiness (added by the agent)

- **Why:** the live show at the venue depends on things that are not code.
- **Steps:**
  1. **The client's demo settings** (`~/TalkWithZombies-client/settings.yaml`, the owner's file): the seed (the good
     3090 seed replays its show only on the 3090), `voice_seed`, `reference_format: ogg`, and the rehearsal's test
     lines removed (`event_every`, `event_jitter`, `debug`).
  2. **Which box:** the 3090 is reachable only on the home LAN — unless the owner's separate project on remote SSH
     access succeeds (kept out of this repository); otherwise the A6000. **Wake the A6000 the day before** as a check
     (a wake can fail: no A6000 in stock, 2026-09-24), and again about 4 hours before the talk.
  3. **A checklist for the venue:** the tunnel and `make check`; the browser's zoom and full screen; the audio output
     to the room; the deck on GitHub Pages (and offline, in case the venue's network fails); the fallback video ready
     to play; the laptop on power, notifications off.
- **Done when:** the checklist exists (a runbook, `docs/runbooks/demo-day.md`) and the A6000's day-before wake has
  worked.

## §3. The order

1. **A** — the inventory first: it may change what the study sessions should cover, and the rehearsals need the final
   deck.
2. **B, C, D** — in any order; each one also prepares the Q&A drill. D carries the pauses' question.
3. **E** — the baseline can be transcribed any time (it needs no decision but which file); rehearsals 1-3 after A.
4. **F** — written early (the checklist), executed at the end (the wake, the settings).

## §4. Results (filled in as the work goes)

- **B, the backend — done 2026-10-10** (moved ahead of A, the owner's choice: "I want to do the fastapi study session
  before reviewing the presentation"). The map the session opened with — the modules and the abstraction each holds,
  the routes, the path of one round — is kept whole in [discussion 2026-10-10] code-map-backend (a snapshot at
  `tz-0.9`). The owner walked the code from it: "I went through the code myself based on this map you presented and I
  feel I got myself the picture together."

- **C, the client — under way 2026-10-10.** Kept from the session, each a snapshot at `tz-0.9`: the map ([discussion
  2026-10-10] code-map-client: the scripts, the page's states, one cycle of the loop, the audio graph, the data
  structures); how a show runs ([discussion 2026-10-10] client-how-a-show-runs: a Web Audio refresher on the app's
  own graph; the loop, `runShow` and `playRound`; the voice queue, how fetching and playing overlap). Two hypotheses
  for the pauses came out of it, added to their follow-up for D.

- **D, the debug data — done 2026-10-10** ([discussion 2026-10-10] debug-data-study: a run's folder and the fields
  worth knowing; the console in debug mode; what the app sends to and receives from llama.cpp, Whisper and the voice —
  every question and answer, verbatim). The improvements, written down for after the demo: the follow-up "Debug and
  observability improvements". The pauses, measured in the same session: their follow-up, "Pauses of about 300 ms…".

*Still to come: the rehearsals' measurements (E).*

## §5. What the plan needs from the owner

1. **Which recording is the baseline** — the longest of 2026-10-08 are `2026-10-08 22-15-34.mp4` (54 MB) and
   `2026-10-08 22-30-50.mp4` (75 MB, about 12 minutes by the files' times); and where to run Whisper (the 3090, or the
   Mac).
2. **The timeboxes** (60-90 minutes a session) — right, or longer?
3. **Backup slides after "Thank you"** — wanted?

## §6. Riding this branch (housekeeping)

- **Task 10.1, the narrower-filter test** — pushed past the talk, a minor-priority follow-up (the owner, 2026-10-10).
- **The `tz-0.9` re-proof** recorded in Task 14, and Task 14 moved to "Done in this arc".
- **The box** — hibernated since the night of 2026-10-08.
- **The A6000's price** — checked, right as it is in the slides (the owner, 2026-10-08).
- **Three observations from the 3090 show of 2026-10-08,** as follow-ups: events that could cue a sound the library
  already has (keywords to add, cheaper than R3); the pauses (workstream D); some cues barely heard (the story's
  `gain_db`).
- **The old session handoffs** — the agent reminds the owner in this branch's PR and asks before deleting any; the
  latest stays as the template.
