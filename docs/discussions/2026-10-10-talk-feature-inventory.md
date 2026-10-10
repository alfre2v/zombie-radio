# The talk's feature inventory — the app's features against the slides

**Date:** 2026-10-10 · **Arc:** MVP prototype · **Branch:** `alfre2v/talk-prep`
**Type:** reference — the inventory of workstream A, step 1 ([discussion 2026-10-10] talk-preparation): every feature
of the app, where the deck covers it, and the agent's lean; the owner's item (1.b), verbatim: "Do a deep pass over
every slide to see if we are covering all the important aspects of the app (for example: Do we even enumerate
anywhere all the types of rounds we have in the app?... I don't think so)." Kept exactly as the owner saw it.
**Status:** **awaiting the owner's rulings** — the "Your call" (slide, aloud, backup, out) is the owner's; no slide was
changed. A **snapshot**: the spec at `tz-0.9` (`docs/specs/product-definition.md` §1-§9), the six files of
`talk/sections/` read in full, notes included, and the text of the four diagrams (`talk/images/_machines.svg`,
`_components.svg`, `_round_flow.svg`, `_timeline.svg`).

The inventory, built from the spec at `tz-0.9` and a full read of the six slide files (notes included) plus the text
in the four diagrams. **I haven't changed any slide.**

**How to read the "Where today" column:**
- **Screen:** in a slide's body or a diagram's labels.
- **Notes:** speaker notes only; the audience hears it only if you say it.
- **Demo:** heard or seen live during the show, but never named on a slide.
- **—:** nowhere in the deck.

The **"Your call"** options are: slide, aloud, backup, out. **"My lean"** is my recommendation and its reason; the call
is yours.

### 1. The show's shape (the director)

| # | Feature | Where today | My lean |
|---|---|---|---|
| 1 | **Two modes**, Broadcast and Contact, driven by the receiver | Notes (Components, the director). The Components diagram says "the mode, the receiver" without naming them | **Slide.** They're the show's whole logic, in two words |
| 2 | **The eight round kinds**: sign-on/orientation, free, the call (repair), exchange, re-call, last exchange, breakdown, switch-off | Partly on screen: the director slide's code shows `_orientation`, `_repair`, `_breakdown`, `_free`; the round diagram says "an exchange, or a re-call". All eight are listed only in the director's notes. **Your suspicion is confirmed** | **Backup** (a diagram of the modes and kinds), merged with #1 if that becomes a slide |
| 3 | **A free round's slot**: an event, the aftermath of a contact, a recollection of an earlier caller | Screen (the code shows `slot="aftermath"` and `"recollection"`); explained in notes | Aloud, from the director slide |
| 4 | **The call's window** (60-180 s of audio), **a contact's length** (5 ± 1 answers), two silences → switch-off | Notes (Components, the director, the demo) | Aloud, during the demo |
| 5 | **The agenda**: nine things the cast want from a caller, "who are you" first | Screen (one word, "agenda", in the Components diagram); notes | Aloud, during the demo, when the cast ask your name |
| 6 | **Orientation repeats** every 20 ± 5 rounds; the speaker chosen as whoever has been silent longest | Notes | Out (backup at most) |
| 7 | **The emotional overtone**: three overtones, 14 moods, ~500 tone words, the drift | Screen (the grammar slide shows the negative five; the diagram says "the mood"); notes | Aloud, from the grammar slide |
| 8 | **Events**: 289, one every 2 ± 1 free rounds | Screen (one word, "events", in the diagram); notes; the demo | Aloud. It's also the hook for the sound cues (#24) |
| 9 | **Fixed lines**: what the listener must not miss, said word for word, never written by the model | Notes (Components) only | **Backup.** It's a good answer to "how do you stop the model mangling key moments?" |
| 10 | **The story is data** (`cast_sheet.md` as a Jinja template, `overtones`, `events`, `agenda`, `beats` YAML) | Screen (the diagram: "lab-outbreak: the cast, agenda, beats, events, moods") | As is |

### 2. The model's side

| # | Feature | Where today | My lean |
|---|---|---|---|
| 11 | **One shared screenplay, one request per round** (ADR-0003), not one chat per persona | Notes (the director) | Aloud, from the director slide. It's the key design decision |
| 12 | **The GBNF grammar** | **Screen** (its own slide) | As is |
| 13 | **The grammar agrees with the instruction** (0.3-0.5 % per token, against 10 % when it overrules) | Notes (the grammar) | Aloud, one sentence |
| 14 | `/no_think` and reading the chat template first | Notes | Out (a Q&A answer) |
| 15 | **The 32k context and the trim** | **Screen** (its own slide) | As is |
| 16 | **Counting from the server's own timings**; the start check (`/props`) | Notes (the trim) | Out (a Q&A answer) |
| 17 | **Streaming**: the parser cuts lines, SSE, the voice starts before the model finishes | **Screen** (the round diagram) | As is |

### 3. The voices

| # | Feature | Where today | My lean |
|---|---|---|---|
| 18 | **Cloned real voices, one recording per mood** (EARS; the voice follows the mood) | **Screen** (Local AI, both diagrams, the commands, the credits) | As is |
| 19 | Lines cut into chunks of about 100 characters | Screen (Components: "each line cut into chunks") | As is |
| 20 | **The compressed reference clips** (Opus, `reference_format: ogg`, `tz-0.7`) | — (and **wrong in notes**: "The machines" calls it "a follow-up") | Aloud at most; fix the note |
| 21 | **The voice's seed** (`voice_seed`: a run said the same way twice) | — | Out, or one clause beside the seed (#33) |

### 4. The sound (the biggest gap)

| # | Feature | Where today | My lean |
|---|---|---|---|
| 22 | **The static bed** (8 Freesound clips; rises between rounds, ducks under the voice, silent while you talk; fading, the AM filter, M/F keys) | **Screen** (both diagrams; the timeline "Oct 2, radio static"; the credits) | As is |
| 23 | **The ambience**: textures and spots, 31 clips, the world outside (`tz-0.8`) | **Demo only** (`ambience: bool = True` in the fork's `app/config.py:319`, so it plays). On no slide, in no note | **Slide.** The four-levels slide (#26) covers it |
| 24 | **Sound cues**: an event that names a sound plays it (keywords, seeded dice; `tz-0.9`) | **Demo only.** Nowhere in the deck | **Slide**, or within #26. Your inversion is a good story to tell |
| 25 | **The event sounds**: 29 sounds, 42 takes, cue-only, chosen by ear | **Wrong on screen**: "What's next" lists "Event sounds" as *future* | Within #24; take it off "What's next" |
| 26 | **The four levels of sound immersion** (bed, textures, spots and cues, voices) | — | **Slide** (your 1.a) |
| 27 | **The sound-effects experiment** (models on the box; Stable Audio 3 Small-SFX chosen) | — | Aloud or backup. It's where #23-25 came from |
| 28 | The gauge (Web Audio analysers drive the magic eye and the oscilloscope) | Notes (Components) | Aloud, during the demo |

### 5. The listener

| # | Feature | Where today | My lean |
|---|---|---|---|
| 29 | **Hold to talk, half-duplex** (10 s window, 30 s press cap) | **Screen** (both diagrams: "Hold Space", "hold to talk") | As is |
| 30 | **Whisper with the cast's names as a hint; the transcript filter** (inventions count as silence) | Screen (Whisper); the filter in notes | Aloud, one sentence |
| 31 | Captions with doubtful words marked | Notes (the demo) | Demo |

### 6. The page, the record, the seed

| # | Feature | Where today | My lean |
|---|---|---|---|
| 32 | **The browser is the clock** (a state machine) | **Screen** (the round diagram, Components) | As is |
| 33 | **The seed replays the show** word for word (same box and build); cues are seeded too | Screen (the code line `random.Random(f"{run.seed}:{n}")`); explained in notes | **Aloud, stressed.** It's one of your "highlight" items (Task 9) |
| 34 | **The looks** (the 1950 radio, the ham transmitter; the chooser with live miniatures) | **Screen** (Halloween's photo, Components) | As is |
| 35 | **The run's record and debug mode** (every prompt, request, reply and voice chunk kept) | Screen (Components: "script.json, the trim, the debug files"); notes | **Backup.** Session D gave you the material |
| 36 | **Every number is a setting**; defaults are the demo's | — | Out (a Q&A answer) |
| 37 | Stop and Resume; the keys Space, M, F, **A** | Notes (the demo), **without A** | Aloud, in the demo; add A to the notes |
| 38 | The tools: show driver (a scripted listener), chunk replay, casting, Freesound fetch, `prepare_ambience`… | Notes (slide 5: the 7 tools as of 10-03) | In the recount (A.5) |

### 7. Deployment (well covered)

| # | Feature | Where today | My lean |
|---|---|---|---|
| 39 | One Ansible command, four roles, `changed=0` on a re-run | **Screen** | As is |
| 40 | The 3090 at home (`lan`/`local`; nothing at boot) | **Screen** | As is |
| 41 | The client installer pinned to a fork tag | Screen (Machines, Commands) | As is; the notes say "today tz-0.6", which is stale |
| 42 | The SSH tunnel and the security posture (loopback, key-only, port 22, the never-commit hook) | Screen (the tunnel); security in notes | As is |

## Found in passing: stale facts on the slides (none changed)

1. **"What's next"** lists **event sounds** as future work (built, `tz-0.9`). It's already on the plan's list.
2. **The timeline** (slide 5's diagram) **stops at `tz-0.6` (Oct 2)**: no `tz-0.7`, `0.8` or `0.9`.
3. **"The machines" notes:** "today tz-0.6"; "a compressed-clips switch is a follow-up" (built, `tz-0.7`).
4. **"The components" notes:** "1,284 Python tests" (1,337 at `tz-0.9`, per handoff 13); the keys lack A; no ambience.
5. **"Live demo" notes:** the keys lack A. "No static: M was pressed" is right, but nothing covers the ambience being
   quiet (A).
6. **The director slide's notes** say "The highlighted line is why the same seed replays". But the code block has no
   line-highlight attribute, and `talk.css` has no highlight rule (`grep -c highlight` = 0). The line is probably
   **not** highlighted on screen. I haven't checked on the published site.
7. **Slides 5 and 27's counts** (known; A.5).
