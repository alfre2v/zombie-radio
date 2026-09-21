# Task 6 reconnaissance brief — the umbrella document

**Date:** 2026-09-21 (opened; living until Task 6 starts) ·
**Arc:** MVP prototype · **Branch:** `alfre2v/task6-recon-brief`
**Type:** reconnaissance brief — a guided tour of the code we are
about to fork, written so that the owner's own study of three
codebases starts oriented and so that the Task 6 fork's shape
round argues from receipts rather than from memory.
**Status:** IN PROGRESS. Unit 1 (TalkWithMe) under way; units 2–4
not started. Open questions are marked OPEN where they stand.

*Context for the cold reader.* Zombie-Radio is an interactive,
audio-only theater play performed by four AI voice actors:
scientists trapped in a lab during a zombie outbreak, broadcasting
on shortwave radio. The audience listens and can talk back through
a push-to-talk microphone. The prototype is built on two open
source projects by one author, scorbo2: **TalkWithMe** (a local
multi-persona chat application with a web UI, which we run on the
Mac laptop) and **tts-serve** (a REST wrapper around voice-cloning
text-to-speech engines, which we run on a rented GPU box together
with llama.cpp and a Whisper server). The owner also wrote a
prototype of the same idea in 2024, `zombie_radio_ai`, a single
Python script that ran everything on one PC. Task 6 of the current
arc is to fork TalkWithMe thinly and apply two small patches; this
brief is the reconnaissance that precedes that fork.

---

## 1. Why this brief exists

Two facts triggered it:

- **The fork moment arrived on 2026-09-18.** In the live prototype,
  persona replies started with their own name tag (`[Moira]: …`)
  and the text-to-speech engine read the tag aloud. Cleaning that
  requires a code change in TalkWithMe, hence a fork. A second
  patch was already queued: the browser cuts a reply into
  sentences for speech synthesis, and very short fragments ("1.",
  "Dr.") produce audio artifacts; the fix is to pack text up to a
  maximum number of characters instead. Both patches are meant to
  be small, separable, and offerable upstream to scorbo2.
- **The owner wants to understand the codebases himself** before
  the fork is shaped: TalkWithMe, tts-serve, and his own 2024
  project, to form his own view of how TalkWithMe should change
  for narration purposes. This brief is his accelerator, not his
  replacement: it points at the code, states what it does with
  line-number receipts, and leaves the open questions open so they
  can be settled in dialog.

The brief is deliberately produced in **exploration and discovery
mode** (owner ruling 2026-09-21): section by section, findings
reported in conversation first, discussed, and only then written
down. Speed is not the objective; understanding is.

## 2. Scope: four units, each with its own deliverable

The owner divided the work by software project (2026-09-21), with
one refinement per unit accepted after the agent's pushback:

1. **Unit 1 — TalkWithMe, deep.** The project we fork. Seven
   sections, listed in §4 below under the tour document. Unit 1
   alone unblocks Task 6: the two patches touch TalkWithMe only.
2. **Unit 2 — tts-serve, scoped to what we consume.** TalkWithMe
   calls tts-serve over HTTP and never edits it, so a full tour of
   its ~95 files buys little. The unit covers three things:
   - the synthesize contract — request shape, text-length limits
     (they bound the accumulator's maximum), streaming or not,
     error behavior;
   - the engine abstraction — Task 5b will add a new engine
     (LuxTTS) and measure a two-engine VRAM budget, so how an
     engine plugs in tells us how big 5b's code side is;
   - voice-reference handling — Task 4's real voice samples flow
     through it.
   The scope widens only on evidence found while reading.
3. **Unit 3 — synthesis.** Resolve every question in the
   seam-question ledger (§5) that could not be answered inside one
   project.
4. **Unit 4 — the 2024 prototype, integration pass.** How the ideas
   of `zombie_radio_ai` (a hidden in-prompt narrator, random
   "entropy terms", scripted interaction beats) would map onto the
   chassis of TalkWithMe plus tts-serve. A short *prologue read* of
   the 2024 code happened before unit 1 (§7 below), so that unit
   1's "seams for narration" section maps against the real code
   rather than against a one-line description in the spec; the
   dialog exploration of the 2024 design stays in unit 4.

**Explicitly out of the brief:** creating the fork, writing patch
code, designing the ensemble director (that is the next arc's
work; the brief only maps where a director would attach).

## 3. Method

- **Read the actual code.** TalkWithMe at tag `7.1` (commit
  `93df6ca`), which is both the owner's working clone
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe`) and the
  pristine clone the Task 7b installer produced
  (`/Users/alfredo/TalkWithMe-client`). tts-serve at tag `1.2`
  (`/Users/alfredo/workspace/hackTNT_2026/tts-serve`). The 2024
  project at its only branch, commit `8d86f20`
  (`/Users/alfredo/workspace/hackTNT_2026/zombie_radio_ai`).
- **Every claim carries a receipt**: a file path with a line
  number, quoted source, or a measurement, and is labeled
  *measured* (we ran or inspected it), *docs-say* (the project's
  own documentation says so), or *believed* (inference, marked as
  such). Anchors from the earlier 2026-09-18 source audit were
  re-verified against 7.1, never copied.
- **Path conventions** (owner rulings 2026-09-21): files in the
  sibling clones are always given with their full absolute path,
  because clickable links do not work for them in the desktop app;
  files inside this repository are given relative to the repo
  root; the HTML visuals use absolute paths everywhere because they
  drive `vscode://file/…` deep links.
- **Cadence:** reconnaissance for one section is reported in
  conversation, discussed until settled or explicitly parked, then
  written. The owner reviews the uncommitted files in VS Code;
  commits happen on his word, however many that turns out to be.
- **Writing rule for these documents** (owner, 2026-09-21): the
  files must not be denser than the conversation that produced
  them. Same level of detail, human-readable layout, self-contained
  — a reader should not need the agent's context window, and
  load-bearing facts are repeated in place rather than only linked.

## 4. The documents of the brief

- **This file** — scope, method, the seam-question ledger, the
  glossary, the 2024 prologue, and later the synthesis (unit 3)
  and the integration pass (unit 4).
- `docs/discussions/2026-09-21-task6-recon-talkwithme.md` — the
  **TalkWithMe tour** (unit 1), seven sections:
  1. the pipeline map, microphone to speaker, every hop with a
     receipt;
  2. the server-side reply path and where the label sanitizer
     goes, including the persistence and message model, and why
     a server-side placement is presumptive;
  3. the anatomy of `static/tts.js` — the sentence splitter the
     accumulator replaces, the two queues, where the "vanished
     sentence" watch item is observable, where the maximum-chars
     knob enters;
  4. settings plumbing — how a new knob travels from
     `settings.yaml` through the config module and the settings
     router to the UI;
  5. seams for the narration future — where a director loop
     would attach, mapped against the spec's open questions and
     the 2024 baseline; maps only, designs nothing;
  6. upstreamability audit — how to keep the two patches
     separable, minimal, and offerable, using upstream's own
     `AGENTS.md` and test conventions as house-style receipts;
  7. what is explicitly out.
- `docs/discussions/2026-09-21-task6-recon-tts-serve.md` — the
  **tts-serve tour** (unit 2), to be created when unit 2 starts.
- `docs/visuals/task6-reconnaissance-brief/` — the **HTML
  derivatives**: one self-contained page per tour plus an index.
  Diagrams as inline Mermaid (single-sourced from the markdown),
  annotated code excerpts (HTML only, so the reader does not have
  to leave the page), `vscode://file/<absolute path>:<line>` deep
  links on every receipt, a reading itinerary and the open
  questions per section, and a glossary of upstream's vocabulary.
  Written after sections 1–3 of unit 1 exist. This folder is the
  first use of `docs/visuals/`, the home the documentation
  system's README reserves for presentation derivatives of a
  textual source (`docs/reports/` stays for incidents).

## 5. The seam-question ledger

A *seam question* is one that cannot be answered by reading a
single project because it concerns the boundary between two. Each
gets an ID, the unit that raised it, the unit that owes the answer,
and — when answered — a dated resolution written beside the
question, never over it.

- **S1 — Reference audio per request.** *Raised by unit 1, owed by
  unit 2.* TalkWithMe re-reads the persona's `ref.wav`, base64-
  encodes it, and includes it in EVERY synthesis request — one
  request per sentence in streaming mode. Measured on the four
  placeholder voices: the clips are 246–290 KB (5.0–6.0 s of
  24 kHz, 16-bit mono), i.e. roughly 330–390 KB of base64 per
  sentence over the SSH tunnel to the GPU box. Real actor clips may
  be longer. Question: does tts-serve offer any reference caching
  or a voice identifier, or is per-request upload the only
  contract? *Status: OPEN.*
- **S2 — Several emotional references per persona.** *Raised by
  the 2024 prologue, owed by unit 2.* The 2024 prototype realized a
  character's emotion by choosing an emotionally matching reference
  clip, one fixed clip per character. TalkWithMe likewise has one
  `ref.wav` per persona. Question: can tts-serve switch the
  reference per request cheaply enough that one persona could
  carry several emotional references, chosen per line? *Status:
  OPEN.*
- **S3 — Text length per synthesis request.** *Raised by unit 1,
  owed by unit 2.* The max-chars accumulator's N is bounded by
  what the engine tolerates in one request (and by how latency
  grows with text length). Question: what limits does tts-serve or
  the engine impose, and how does synthesis time scale with input
  length? *Status: OPEN.*

## 6. Glossary

Project terms coined or fixed in this brief:

- **Entropy terms** — randomly drawn words and numbers (an
  adjective, an emotional register, a word count) injected into a
  generation request so that consecutive requests never share a
  prompt. Named after their purpose: raising the diversity of the
  model's output.
- **Entropy-term injection** — the mechanism that places entropy
  terms into each turn's directive. This is the standardized name
  for what earlier documents call "the entropy-terms trick" or
  "random-terms injection" (owner ruling 2026-09-21: the idea
  matters, not the 2024 implementation). Its neighbours in the
  literature: *prompt-side diversity* (prompt perturbation,
  stochastic prompt augmentation — a cultural cousin is Brian
  Eno's Oblique Strategies, a deck of random constraint cards drawn
  to break creative loops); *decoder-side diversity* (temperature,
  repetition penalty, presence and frequency penalties, llama.cpp's
  DRY sampler); and *output-side rejection* (generate, compare with
  recent lines by n-gram overlap, resample on a near-duplicate).
- **Stream-head filter** — a small state machine placed at the
  head of a streamed reply that holds back the first few tokens
  until it can decide whether they form a speaker label, drops the
  label if so, and passes everything else through unchanged. The
  presumptive shape of the Task 6 label sanitizer (see the tour
  document, section 1 findings).
- **Seam question** — see §5.

Upstream TalkWithMe vocabulary (the words the fork discussion will
use, in upstream's sense): **persona** (a character: prompt,
voice reference, avatar, living in `Personas/<Name>/`), **chat
room** (a named set of personas with its own persisted history),
**echo chamber** (a room mode that bypasses the LLM and echoes the
user), **who answers** (the client's choice of first speaker:
`router` = ask the LLM, `random`, or a named persona),
**max persona replies** (how many personas answer one user
message), **history entry** (one message in the room history — the
context window is measured in entries, not in user turns),
**streaming TTS** (speech synthesized sentence by sentence while
the reply is still being generated), **capabilities document**
(the JSON a tts-serve engine publishes describing the parameters
it accepts), **message ID** (a UUID stamped on every message and
on every audio file that belongs to it).

## 7. Prologue — the 2024 baseline (`zombie_radio_ai`)

*Read 2026-09-21 by the agent; discussed with the owner the same
day. Repository: `/Users/alfredo/workspace/hackTNT_2026/zombie_radio_ai`,
only branch `main`, HEAD `8d86f20` ("Add TheaterPlay class"). The
substance is one file, `zradio_local/zradio_local.py` (970 lines);
`zradio_local/readme.md` holds prompt-experiment notes. All line
numbers below refer to `/Users/alfredo/workspace/hackTNT_2026/zombie_radio_ai/zradio_local/zradio_local.py`.*

### 7.1 What the code does

1. **One chat context plays the whole cast.** A single Ollama
   conversation holds the initial prompt and every turn
   (`LargeLanguageModel.chat`, line 438). The prompt tells the
   model to answer as exactly one character per turn in the wire
   format `Character Name: Dialog Line` (line 512 onwards). This
   is the opposite of TalkWithMe's design, where every persona
   reply is its own LLM request with its own system prompt. It is
   also why the name tag was the *protocol* in 2024 and is a *leak*
   in 2026.

2. **The narrator is a hidden director living inside the prompt.**
   The prompt defines a Narrator who "is not a character in the
   play", must not be spoken as, and may name the next speaker
   (line 520). Every turn's user message is a narrator directive
   generated by code. This is the direct ancestor of the
   `[Director]:` prefix probe (mechanism C6) in the narrative-
   health taxonomy of [discussion 2026-09-16].

3. **The entropy-term injection, as committed, is smaller than our
   documents describe.** The product-definition brainstorm says
   "themed lists (action verbs, adjectives, nature
   concepts/animals, …)". The code at HEAD has one adjective list
   of about seventy words (`descriptive_words_str`, line 557) plus
   three short inline lists: thirteen emotional registers, three
   verbs, nine topics (line 642 onwards). The topic is drawn but
   never used, because the query that used it is commented out
   (line 656). The live query (line 657) is: a random character, a
   random verb, a random emotional register, a random word count
   between 5 and 50, and one random adjective. *Labeled: code-shows
   vs docs-say.* The owner checked the repository on 2026-09-21: no
   other branch exists; the richer version was a memory that grew.

4. **Speaker selection was random.** Every generated narrator line
   names a character drawn with `random.randrange` (line 648). The
   prompt's clause allowing the model to choose who speaks (line
   535) is never exercised by the loop. So 2024 had no "LLM
   decides" path either — the same mechanism the taxonomy calls E1
   (random followers) in TalkWithMe.

5. **The director loop is a four-state machine**
   (`get_next_line_narrator`, line 686): a pending radio message
   from the audience gets answered; a just-consumed message makes
   the radio "smoke", closing the interaction beat; otherwise a
   95/5 coin picks ordinary dialog or a cry-for-help beat that
   opens the microphone. Against the four open questions of the
   spec's ensemble-director section (§5.3):
   - *Who speaks next:* random.
   - *Pacing:* the random word count, plus a fixed two-second pause
     after each line (line 793).
   - *When to open interaction beats:* the 5 % coin, then a
     scripted escalation of up to five exchanges with canned
     sentences appended to the character's line (line 750 onwards),
     a fixed ten-second recording window (line 732), and an ASR
     gate of "any four-letter word and the word 'bye' absent"
     (line 785).
   - *Dead-air texture:* none. The pipeline is strictly blocking —
     LLM, then TTS, then playback, then recording — with no
     prefetch (lines 740–793).

6. **A contamination ancestor.** When the reply fails the
   `Name: line` parse, the turn is skipped (line 748), but the
   malformed reply was already appended to the conversation
   (line 442) and stays in context. The 2024 edition of taxonomy
   mechanism C3 (contaminated transcript).

7. **Context pruning kept the head and the tail.** Past 90 % of an
   estimated 4096-token budget it pops the *middle* message until
   50 % (line 454), so the initial prompt always survives and the
   most recent lines stay. Contrast: TalkWithMe uses a sliding
   window of the last N history entries, which we raised from 6 to
   50 in Task 3.

8. **Voice was clone-by-reference with a fixed emotion per
   character.** Each cast entry carries a reference clip, its
   transcript, and an emotion label (line 470 onwards); the emotion
   is realized by choosing an emotionally matching reference clip,
   not by any per-line control. Same shape as TalkWithMe's
   `Personas/<Name>/ref.wav` plus `ref.txt`. → Seam question S2.

9. **Dead scaffolding shows intent.** `plot_twists` (line 542) and
   `user_radio_interaction` (line 552) are defined and never
   referenced. The twists read "the next 5 dialog lines will
   revolve around this event" — an authored-beat mechanism, the
   ancestor of the spec's post-MVP hybrid idea (§5.2: offline-
   authored trajectory scaffolds as guide-rails).

10. **Small receipts.** A duplicated `elif asr_interactions == 4`
    (lines 759 and 761) makes the "we are losing you" line
    unreachable. Whisper tiny is reloaded from disk on every call
    (line 319). "Over and out" as a voice stop command is already
    here (line 253) — the origin of the radio-endpointing idea in
    the brainstorm. The model default is `nemotron-mini` with a
    4096-token context (line 430); the 2026-09-12 Q&A log records
    the owner's later recollection of a Qwen model around 9B. No
    answer-deduplication code exists anywhere in the file; the
    only anti-repetition measures are the entropy terms and one
    prompt sentence, "Be creative, try not to repeat the same
    lines" (line 538) — the "hashmap of answers" the owner recalls
    considering never reached the code.

### 7.2 The owner's recollections (2026-09-21, labeled owner recollection)

- The **hidden in-prompt narrator** is what made the narration feel
  alive.
- **Entropy-term injection** was the anti-repetition measure: with
  models around 9 GB the answers "got very repetitive really fast".
- The code supports this reading: the narrator directive carries
  the who, the emotional register, and the length, while the
  adjective is one word of seasoning.

### 7.3 The corrected baseline

Spec §5.1 names "the 2024 entropy-terms trick" as the baseline
for steering a small model against looping. The baseline is
therefore the **committed** version — a hidden in-prompt narrator
issuing per-turn directives that carry a random speaker, a random
emotional register, a random word count, and one random adjective
— not the richer remembered one. A ledger correction to that
effect was added to the spec on 2026-09-21.

### 7.4 What this means for the rest of the brief

- The tour's "seams for narration" section (unit 1, section 5) maps
  TalkWithMe against the four §5.3 questions using the 2024
  answers above as the crude baseline: random speaker, word-count
  pacing, coin-flip interaction beats, no dead-air handling.
- Both diversity families are available in the 2026 stack and both
  are untried: prompt-side (entropy-term injection, which needs a
  director to inject anything) and decoder-side (llama-server's
  repetition penalty, presence/frequency penalties, and DRY sampler
  — all read at neutral in the 2026-09-19 `/props` check). That is
  a Task 5c / 5a question, not a Task 6 one.
- The output-side rejection idea (the never-built hashmap) is
  parked here as a one-liner: it costs a second generation per
  rejected line, the most expensive of the three families.

## 8. Synthesis (unit 3)

*Not started. Will resolve S1–S3 and any seam questions raised
later, each with a dated resolution beside its ledger entry in §5.*

## 9. Integration pass (unit 4)

*Not started. Will map the 2024 mechanisms (§7) onto TalkWithMe's
seams (tour document, section 5) and tts-serve's contract (unit 2).*

## 10. Update trail

- **2026-09-21** — Document created after the shape rulings of the
  same day (units, seam ledger, documents, visuals folder, cadence,
  path and writing rules). Prologue (§7) written from the read of
  `zombie_radio_ai` and the owner's recollections. Seam questions
  S1–S3 opened. Glossary opened with the entropy-term decision.
