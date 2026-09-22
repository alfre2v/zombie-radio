# Task 6 reconnaissance brief — the umbrella document

**Date:** 2026-09-21 (opened; living until Task 6 starts) ·
**Arc:** MVP prototype · **Branch:** `alfre2v/task6-recon-brief`
**Type:** reconnaissance brief — a guided tour of the code we are
about to fork, written so that the owner's own study of three
codebases starts oriented and so that the Task 6 fork's shape
round argues from receipts rather than from memory.
**Status:** ANSWER PASS COMPLETE (2026-09-22). Units 1 and 2 toured;
unit 4 delivered as [discussion 2026-09-21] prompt-structure (plus
[discussion 2026-09-21] story-loop); every seam question (§5) and
open question (§5b) now carries the owner's ruling. **Unit 3, the
synthesis, written 2026-09-22 (§9) — the brief is COMPLETE.** The HTML
visuals were DROPPED on 2026-09-22 (owner: "we have a bigger fish
to fry"); `docs/visuals/` is not born.

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
  *Superseded in part on 2026-09-21 (see the ruling at the end of
  §2): the fork becomes a new app, TalkWithZombies, free to
  diverge; only the accumulator remains an upstream candidate; and
  both patches now wait for two design decisions.*
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

**Owner ruling 2026-09-21, after the breadth passes of units 1
and 2 — "do not worry about upstream".** Recorded in full in
TODO.md (Task 6 disposition + the arc-boundary note) and in
[discussion 2026-09-19] upstream-contribution-strategy §7; the
essentials for this brief:

- The clone becomes a NEW app, **TalkWithZombies** — a real GitHub
  fork of scorbo2/TalkWithMe at tag 7.1 (provenance and MIT
  attribution kept, "forked from" labeled prominently in our
  README), then modified freely. No upstream compatibility
  pretence: the turn-taking and the whole per-turn prompt
  structure are expected to change significantly.
- **Two design discussions must precede any source patch**, each
  in its own dated discussion doc, dialog-first: (1) the **prompt
  structure** — TalkWithMe's one-request-per-persona with the
  `[Name]:` history rewrite, versus a 2024-style single shared
  context with a hidden narrator, versus a better structure not
  yet thought of; (2) the **story loop** — how to force a show
  that keeps turning into TalkWithMe's "one user message → up to
  four replies → stop" design, given no server-initiated channel
  to the browser (question Q13). The prompt-structure discussion
  is the substance of unit 4 (§10); the story-loop discussion
  follows it, because the loop's shape depends on who assembles
  the prompt.
- **Consequence for the two Task 6 patches:** the sanitizer's fate
  DEPENDS on the prompt-structure decision (its cause is the
  history rewrite at
  `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/session.py:156`
  to 161; in a shared-context design the label becomes wire
  protocol and the sanitizer becomes a parser); the accumulator is
  design-independent and may proceed at any time.
- **Contribution ledger re-ranked:** the deployment machinery
  first (what scorbo2 may adopt or advertise), the accumulator as
  the only plausible app-code patch, the sanitizer dropped.
  Outreach stays deferred past the deadline.
- **Arc boundary shifted, said out loud:** the two decisions above
  belong to the director's design, which TODO.md had placed in the
  next arc. They are pulled into this arc because no patch can be
  shaped without them; the next arc builds on the decisions
  instead of taking them. The tour's upstreamability audit (unit 1
  §6) remains as knowledge about how scorbo2 works, no longer as a
  constraint on our changes.
- **Repository layout (owner decision, later the same day): two
  sibling repositories.** This repo stays deployment + docs;
  TalkWithZombies is its own GitHub fork cloned beside the other
  sibling clones; the installer's `client_repo` / `client_version`
  / `client_dir` variables are the glue, plus a proven-version pin
  and a docs pointer section. Submodule, subtree, and file-copy
  were considered and rejected (reasons in TODO.md, Task 6).

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
  **Breadth first (owner ruling 2026-09-21, after unit 1 section
  1):** the open questions are NOT answered as they arise. One
  general pass goes over all three products gathering the
  questions (the Q-list across the tour documents and the seam
  ledger below); then a second pass, product by product, answers
  what can be answered. Section 1 of the TalkWithMe tour therefore
  left Q1–Q3 open on purpose, and the tts-serve tour added Q4–Q6.
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
  Sections 2–6 written at breadth-pass depth on 2026-09-21: the
  reply path's two token sources and the head-filter geometry; the
  single cut point in `tts.js` and the `streaming`-flag road for N;
  the seven-file journey of a settings knob; the director seams
  (the `who_answers` hook, the no-server-push gap, the echo-chamber
  precedent, the two directive injection points); the
  upstreamability audit (issue-branch workflow, feature-doc genre,
  the AGENTS.md rules, the JS test gap, file counts).
- `docs/discussions/2026-09-21-task6-recon-tts-serve.md` — the
  **tts-serve tour** (unit 2): orientation (layout, versions, how
  our role runs it, house style), the synthesize contract as our
  client experiences it, findings F1–F10, the seam-ledger
  proposals, vocabulary, itinerary, questions Q4–Q6.
- ~~`docs/visuals/task6-reconnaissance-brief/`~~ — **DROPPED
  2026-09-22** (owner: "I don't think I need the HTML visuals, we
  have a bigger fish to fry"). The plan is kept below for the
  record; the folder is not born. The **HTML derivatives** were to
  be: one self-contained page per tour plus an index.
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
  contract? *Status: OPEN — proposed resolution from the tts-serve
  tour (F1), 2026-09-21: per-request upload IS the only contract
  (no voice identifier, no upload-once endpoint), but the server
  stages the clip under a content-hash filename and keeps it, and
  the engine caches the encoded voice prompt per clip+transcript,
  so the compute cost is paid once per unique clip; what repeats
  per sentence is bandwidth only, a few tens of milliseconds on
  our tunnel. No fork work needed.* **RESOLVED 2026-09-22 (owner:
  accept).** Per-request upload stays as is in the fork; Q6 closes
  with it. If real actor clips turn out much longer than ~10 s, the
  deferred S3 measurement (follow-ups) tells whether it ever
  matters.
- **S2 — Several emotional references per persona.** *Raised by
  the 2024 prologue, owed by unit 2.* The 2024 prototype realized a
  character's emotion by choosing an emotionally matching reference
  clip, one fixed clip per character. TalkWithMe likewise has one
  `ref.wav` per persona. Question: can tts-serve switch the
  reference per request cheaply enough that one persona could
  carry several emotional references, chosen per line? *Status:
  OPEN — half answered by the tts-serve tour (F3), 2026-09-21: on
  the tts-serve side, yes, at no extra cost — every request is
  stateless and each clip is cached separately. The blocker is
  entirely in TalkWithMe (one `ref.wav` per persona; the TTS proxy
  looks the clip up by persona name). The remaining half is a
  TalkWithMe design question for the fork or the director.
  Alternative path noted: IndexTTS exposes explicit emotion
  control (8-component vector, emotion clip, or text), 22.05 kHz.*
  **RESOLVED 2026-09-22 (owner confirmed the group):** the other
  half is answered by the adopted prompt structure — the
  parenthetical stage direction in the script line carries the
  register; mapping a register to a clip per persona (or to an
  engine knob) is FORK WORK that waits on Task 4's clips, not an
  open question.
- **S3 — Text length per synthesis request.** *Raised by unit 1,
  owed by unit 2.* The max-chars accumulator's N is bounded by
  what the engine tolerates in one request (and by how latency
  grows with text length). Question: what limits does tts-serve or
  the engine impose, and how does synthesis time scale with input
  length? *Status: OPEN — reframed by the tts-serve tour (F2, F4),
  2026-09-21: tts-serve imposes NO upper bound on `text`, and no
  server streams audio, so N is bounded by latency and quality,
  not by a limit. Becomes a measurement question: the
  latency-versus-length curve on a box, using the `time_used` and
  `rtf` fields every response already carries. See Q4 in the
  tts-serve tour.* **DROPPED FROM THIS ARC 2026-09-22 (owner):** "we
  have already committed to this path forward; this measurement
  will be useful later, after we have something working we can
  tweak; I can always change the TTS server." Moved to
  `docs/follow-ups.md` as a tuning measurement. The fork starts
  with a provisional accumulator N of **100 characters** (owner:
  150 was too big), tolerance ~20 % for short tails (Q9).
- **S4 — Two engines on one box (Task 5b).** *Raised by the
  tts-serve tour, owed by the 5b planning.* Every tts-serve
  engine is one process in its own venv on its own port, and
  synthesis inside a process is serialized by a lock. Our Ansible
  role selects ONE engine by name (`zr_tts_engine`). Question:
  what is the deployment shape for two engines side by side — the
  role run twice, or a list variable? *Status: PARKED to 5b's
  planning (owner confirmed 2026-09-22).*
- **S5 — Synthesis telemetry.** *Raised by the tts-serve tour,
  owed by the director design.* Every synthesis response carries
  `time_used`, `rtf`, and the `seed` used; TalkWithMe reads only
  `audio_base64` and discards the rest. Question: should the
  client surface or log these, and where — for 5b's engine
  comparison and for a director's pacing model? *Status: PARKED
  post-MVP, until the director wants a pacing model (owner
  confirmed 2026-09-22).*
- **S6 — Per-request TTS parameter overrides through TalkWithMe.**
  *Raised by the owner's emotion questions (tts-serve tour §8, Q2
  and Q3), owed by the fork or the director design.* tts-serve has
  no central emotion knob; emotion lives in the reference clip for
  most engines, and in engine-specific knobs for two (Chatterbox
  `exaggeration`, IndexTTS `emotion_vector` / clip / text).
  TalkWithMe exposes engine knobs as ONE global settings map and
  its TTS request carries only `text` and `persona_name`
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/models.py:56`
  to 59). Question: how would a per-line instruction — "this line,
  frightened" — reach the engine: a per-request parameter override
  on `/api/tts`, a per-persona choice among several reference
  clips, or both? *Status: RESOLVED in principle 2026-09-22 — the
  channel is the parenthetical stage direction in the script line
  (ADR-0003, point 3); the mapping to clips or knobs is fork work
  after Task 4 (see S2).*

### 5b. Index of open questions (Q1–Q13)

*The question pile the breadth pass collects; each lives with its
context in a tour document. The answer pass rules on them product
by product.*

| Q | One line | Where |
|---|---|---|
| Q1 | Does the label sanitizer become a stream-head filter in `_chat_stream`? *Moot under the adopted prompt structure — no label to strip ([discussion 2026-09-21] prompt-structure §12).* | TalkWithMe tour §1.7, §2 |
| Q2 | Which labels to strip: own name only, any `[X]:`, bare `Name:`? *Moot, same reason.* | TalkWithMe tour §1.7, §2 |
| Q3 | Mention detection overriding who-answers — keep it for a radio show? *Moot on the show page (no who-answers control; the director chooses); stays as-is on the chat/rehearsal page.* | TalkWithMe tour §1.7, §5 |
| Q4 | S3 measurement (latency vs text length) before the fork decides N, or a provisional N first? *RULED 2026-09-22: provisional N = 100 now; the measurement dropped from this arc → follow-ups.* | tts-serve tour §7 |
| Q5 | Task 4 reference material spec: ~10 s clean clips with exact transcripts? *CONFIRMED 2026-09-22 (owner: "matches my plan"); recorded in TODO's owner action queue.* | tts-serve tour §7 |
| Q6 | Keep the per-sentence reference upload as is (cheap per F1)? *RESOLVED with S1, 2026-09-22: yes.* | tts-serve tour §7 |
| Q7 | Mac-local TTS probe with the MLX engine (candidate experiment 5d)? *PARKED until after the MVP (owner, 2026-09-22). The demo laptop is an M1 with 16 GB — cannot run the stack; a second M1 with 64 GB could, if the speed holds; follow-ups entry.* | tts-serve tour §8 Q5; umbrella §10 |
| Q8 | Sanitizer reach: head filter only, or plus a persist-time sweep? *Moot, same reason.* | TalkWithMe tour §2, §8 |
| Q9 | Accumulator remnant policy for tiny trailing fragments? *RULED 2026-09-22: accumulator confirmed as needed; N = 100 packs whole sentences within a script line; the line end is a hard flush; a short tail (under a threshold, ~30 chars) may overshoot N by ~20 % (to 120); a single sentence longer than N is sent whole, alone; lone one-word lines go as is. Full rules: TalkWithMe tour §3.* | TalkWithMe tour §3, §8 |
| Q10 | Knob homes: N in `tts` via the health response; sanitizer toggle in `general`, yaml-only? *RULED 2026-09-22: all fork knobs yaml-only for the timebox — the show's cadence knobs in a new `show:` section, N and its tolerance next to `streaming` in `tts:`; no dialogs; the sanitizer toggle no longer exists.* | TalkWithMe tour §4, §8 |
| Q11 | Add a Node test harness for `tts.js`, or ship the accumulator untested? *RULED 2026-09-22: no new Node harness inside the timebox; the Python suite keeps upstream's green-suite rule; a JS test for the packing rules is a follow-up once the rules stop moving.* | TalkWithMe tour §6, §8 |
| Q12 | Director directives: user message (2024 style) or system-prompt tail? Record only. | TalkWithMe tour §5, §8 |
| Q13 | Director placement given no server-push channel: browser, server+push, or external+polling? *DECIDED 2026-09-21: browser as metronome, server as director ([discussion 2026-09-21] story-loop §8).* | TalkWithMe tour §5, §8 |

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
- **ICL mode / x-vector mode** — two voice-cloning modes of the
  Qwen3-TTS family. *In-context learning (ICL)*: the reference
  clip AND its exact transcript are kept in the model's context;
  higher quality; the transcript is mandatory. *x-vector (speaker
  embedding) only*: a voice embedding extracted from the clip
  alone; no transcript; lower quality. Our engine, faster-qwen3-tts,
  exposes ICL only.
- **Staging** — tts-serve writing the decoded reference clip to a
  temp file because the engine loads prompt audio from a path.
  Two flavours: *content-addressed and kept* (filename = SHA-256
  of the bytes; repeat clips reuse the file and the engine's
  per-path cache — our engine), and *one-shot* (UUID name, deleted
  after the request — LuxTTS).
- **Real-time factor (RTF)** — synthesis wall-clock time divided
  by the duration of the audio produced; below 1.0 means faster
  than real time. Returned on every tts-serve response.

Upstream tts-serve vocabulary: **engine** (one wrapped
text-to-speech model; identified by a stable slug such as
`faster-qwen3-tts`), **core vocabulary** (the five request fields
every engine may support: `text`, `audio_base64`,
`reference_text`, `language`, `seed`), **capabilities document**
(the JSON at `GET /capabilities`, derived from the server's own
request model, describing every accepted parameter with type,
bounds, default, and UI hints), **schema version** (the document's
contract version, 2 today; bumped only on breaking changes),
**reference audio spec** (the document's statement of what clip
the engine wants: required or not, formats, minimum duration,
notes).

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

## 8. The brainstorm's ten voice challenges (C1–C10), revisited against the code

*Owner's question Q6 of 2026-09-21. The canonical copy of this
section is the dated addendum in the challenges' own home,
`docs/discussions/2026-09-13-product-definition-brainstorm.md`
(section "C1–C10 revisited …"); it is repeated here in full so the
brief stays self-contained (owner rule: repeating load-bearing
facts in place is healthy for humans).*

*Method: each of the ten challenges in §5 was re-read against the
TalkWithMe 7.1 and tts-serve 1.2 source during the Task 6
reconnaissance brief. For each: what the code says, whether the
challenge got easier from the perspective of these projects, and
what new problem the code surfaced. The status quo assumed is the
MVP's push-to-talk, which §5 already credits with solving C2, C4,
C5 by construction. Paths into the sibling clones are absolute;
paths into this repository are root-relative. Labels: measured /
docs-say / believed.*

**C1 — Noise robustness, Whisper inventing text.** The STT proxy
asks for `response_format=json` and reads only `text`
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/services/stt_client.py:72`
to 81). No confidence signal is requested or examined, so the
"cheap must-have" §5 names — filtering on Whisper's no-speech
probability and average log-probability — does not exist here. It
is a small patch in the proxy: ask for the verbose format, drop or
flag low-confidence transcripts. **A new problem the code
surfaces (measured):** when Whisper returns empty text, the proxy
substitutes the literal string "No response received from STT
server" (line 81); the browser sees a non-empty `text` and
auto-sends it
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/stt.js:75`
to 98), and that sentence becomes the user's message to the cast.
A silent or noisy recording therefore produces a hallucination of
the app's own making, before Whisper gets a chance to invent
anything.

**C2 — End-of-speech detection.** Solved by construction, with one
nuance §5 did not have: the microphone is a click-to-start,
click-to-stop TOGGLE, not hold-to-talk
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/stt.js:9`
to 14; Ctrl+Space toggles too,
`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/app.js:134`).
"Button release equals end of speech" assumed a held button. With a
toggle, a nervous visitor can forget to stop, and the recording
runs until they do. A hold-to-talk variant would be a small change
in the same file.

**C3 — Speaker identification.** Nothing in either project.
TalkWithMe is single-user by construction — one session object for
the process
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/session.py:170`).
Status unchanged: wishlist.

**C4 — Self-hearing.** Solved by construction ONLY if the
microphone cannot open while the actors speak — and the code does
not enforce that: `toggleMicrophone` never checks whether audio is
playing, and the audio queues keep playing while a recording runs.
Sending a message is blocked during a streaming turn
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/chat.js:67`);
recording is not. With a laptop microphone and loudspeakers, a
recording started during a reply captures the actors' voices,
Whisper transcribes them, and the transcript is auto-sent. **New
problem** — measured in code, believed in effect (the risk depends
on speakers versus headphones). A cheap fix on the fork: disable
the mic while the playback queues are non-empty, or duck playback
when the mic opens — which is also the radio's own "over"
discipline.

**C5 — Addressee detection.** Solved by construction. One adjacent
feature exists: mention detection routes the message to a persona
whose name appears in the text
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/chat.js:80`
to 91). That is a small in-fiction wake protocol already — and it
is also the behavior flagged as open question Q3 in the TalkWithMe
tour, for the director design to decide on.

**C6 — Proper-name capture. This one got EASIER.** The
OpenAI-style transcription endpoint accepts a `prompt` field that
biases the recognizer toward given vocabulary, and a `language`
field. TalkWithMe sends neither
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/services/stt_client.py:72`
to 74), so Whisper auto-detects the language and knows none of our
names. Sending the cast's names, "Over", and a few lab terms as the
prompt, plus forcing English, is a few lines in the proxy and is
the standard remedy for "Miss Betty" becoming "Nisbeti" (the
2026-09-16 field observation). *Believed* that whisper-fastapi
honors the prompt field as the OpenAI API defines it — a one-curl
check on the next box. This would be a THIRD small, upstreamable
patch candidate, outside Task 6's current two.

**C7 — Overlapping speakers.** Nothing in either project.
Push-to-talk stands. Unchanged.

**C8 — Audio mixing. EASIER than assumed.** TalkWithMe already
mixes in the browser with the Web Audio API: one `AudioContext`,
buffer sources connected to the destination
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/tts.js:205`
to 219). Static, dead-air texture, or effects are one more buffer
source and a gain node into the same context, and the browser
resamples every source to the context's rate on decode — which
also disposes of the sample-rate differences between engines
(24 kHz, 48 kHz, 22.05 kHz). The "server versus client mixing"
decision §5 deferred is effectively made by the foundation:
client-side, with assets shipped once — exactly the refined
version that survived the owner's 2026-09-13 pushback.

**C9 — Audio compression.** Neither project has it. tts-serve
always returns 16-bit PCM WAV in base64
(`/Users/alfredo/workspace/hackTNT_2026/tts-serve/tts-engine-common/src/tts_engine_common/models.py:137`);
TalkWithMe forwards it as base64 in JSON to the browser. The
venue-internet leg is the SSH tunnel between the box and the
laptop; the laptop-to-browser leg is localhost and free. So
compression matters on ONE leg, and we own both ends of it — which
gives two options §5 did not list: an Opus output option in
tts-serve (a natural upstream candidate, since the response core
is versioned by `schema_version`), or, as a zero-code stopgap for a
bad venue link, SSH's own compression flag (`-C`) on the tunnel —
worth one measurement, because PCM compresses only moderately.
Also relevant: the reference clip travels the OTHER way on the
same leg on every request (tts-serve tour F1).

**C10 — Sentence-chunked TTS versus emotional coherence.**
Confirmed in code on both sides: each sentence is an independent
request from the browser
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/tts.js:88`
to 104), and tts-serve is stateless — no prosodic memory. **Two
new angles.** First, each request draws a FRESH RANDOM SEED unless
one is supplied
(`/Users/alfredo/workspace/hackTNT_2026/tts-serve/impl/server_fasterQwen3TTS.py:458`),
so part of the chunk-to-chunk inconsistency the owner heard on
2026-09-16 is dice, not the model. Fixing the seed per reply
removes that part for free; today it can only be fixed globally
through TalkWithMe's `settings.tts.parameters`, and per reply would
be a patch. Second, the max-chars accumulator is a direct C10
mitigation — fewer and longer chunks — so BOTH Task 6 patches
serve this challenge. The engine-side emotion knobs (Chatterbox
`exaggeration`, IndexTTS `emotion_vector`) are the third lever,
and they need seam question S6 (per-request TTS parameter
overrides through TalkWithMe).

**Problems the code surfaced that were not on the list:**

- The substituted "No response received from STT server" text
  becoming a user turn (C1).
- The microphone not gated on playback (C4).
- The transcript auto-sent with no review step, so every
  recognition error goes straight to the cast (C6 — also the
  "Nisbeti" mechanism).
- The `[Name]:` label leak — already known; the Task 6 trigger.
- Replies cut at the 200-token cap, persisted truncated and spoken
  as fragments (TalkWithMe tour, F2).
- No streaming synthesis anywhere, so time-to-first-audio is tied
  to chunk size (tts-serve tour, F4).
- One synthesis at a time per engine process (a lock), so a
  director cannot prefetch several personas in parallel on one
  engine (tts-serve tour, F5) — relevant to dead-air planning.
- Good news too: our engine captures its CUDA graphs at startup
  (`server_fasterQwen3TTS.py:381`, `model.warmup()`), so the first
  request is not slow; LuxTTS by contrast pays about 10 seconds
  on its first request.

## 9. Synthesis (unit 3) — what the two projects give the fork, what the seams cost, what stays open

*Written 2026-09-22, after the answer pass closed the ledger. This
is the integration of units 1, 2 and 4: no new reading, no new
findings — the settled picture, self-contained for a reader who
has not read the tours.*

### 9.1 The chassis, seen as one system

TalkWithMe and tts-serve were written by one author to fit each
other, and the reconnaissance confirmed the fit is real: the
client discovers the engine's parameters from tts-serve's
capabilities document and builds every synthesis payload from it,
so an engine switch on our side is a URL change (TalkWithMe tour
§1.2 hop 7; tts-serve tour §2). Together they give TalkWithZombies,
on day one:

- **A working audio loop end to end.** Push-to-talk recording,
  Whisper transcription through an OpenAI-compatible proxy, a
  streamed LLM reply rendered token by token, sentence-chunked
  synthesis with two concurrent queues (fetch ahead, play in
  order), Web Audio playback, and per-message audio persistence
  staged so that audio arriving before its row is never lost. The
  "almost natural" pauses of the 09-18 session come from that
  pipelining, and it survives every change we plan.
- **A browser protocol we can keep.** The page understands four
  server-sent events — `start`, `token`, `done`, `complete`, each
  tagged with a persona. Any generation strategy that can emit
  those per speaker line leaves the browser, the TTS pipeline and
  the persistence untouched. This single fact bounded the cost of
  the ambitious prompt structure (prompt-structure §5) and is the
  reason the fork's work is server-side.
- **A voice contract that is stateless, strict, and instrumented.**
  Every synthesis request carries text, the reference clip, its
  transcript and a language code; unknown fields are refused with a
  422 naming the field; every response returns `time_used`, `rtf`
  and the `seed` used (tts-serve tour §2, F6). Stateless means a
  persona may carry several clips at no cost (S2); strict means a
  stale parameter fails loudly instead of silently; instrumented
  means the tuning measurements we deferred (S3, S5) cost nothing
  to take when their time comes.
- **A per-request grammar hook in the LLM server** that we did not
  know we had when the brief opened: llama-server constrains
  sampling with a GBNF grammar on every token, streaming or not
  (prompt-structure §7.1). It is what turns the 2024 "parse and
  hope" wire format into one that cannot break.
- **Maintainer conventions worth keeping inside the fork** even
  though we no longer track upstream (TalkWithMe tour §6): a
  hermetic Python test suite with one file per router, an
  endpoint table under test, feature docs written spec-first, and
  an agent guide that already encodes the app's invariants. They
  are the fork's quality gates on day one.

### 9.2 What the reconnaissance changed

The brief opened to find two insertion points for two small
patches. It closed having changed the plan three times, each time
because of something read in the code:

1. **The label leak is structural, not a prompt problem** (unit 1
   F1). TalkWithMe shows every persona the other personas' lines
   rewritten as `[Name]:` user turns, so a small model imitates
   the format it sees; and in streaming mode speech is cut from
   the token stream before any persist-time filter could act. The
   sanitizer would have had to be a stream-head filter in the SSE
   loop — bigger than planned — and the finding pointed at the
   history rewrite itself as the thing to change.
2. **The chat-shaped turn model is the other half of the same
   problem** (unit 1 §5, taxonomy C2/C6/E1/E3): one request per
   persona, followers drawn at random, a nameless director, no
   component that owns the story, and no server-initiated channel
   to the browser. Patching the leak would have left all of that
   in place.
3. **The 2024 prototype had already solved the first half** with
   one shared context and a hidden narrator — and failed on
   parsing, repetition, and a blocking pipeline (§7). Reading it
   before unit 1 is why the seams section could argue from the
   real thing.

The result is [discussion 2026-09-21] prompt-structure and
[discussion 2026-09-21] story-loop, frozen as ADR-0002 and
ADR-0003 (draft, gated): one shared context in screenplay form, a
code director in the server setting each round's speaker allowlist
and line budget, one streamed request per round under a screenplay
grammar, the existing events synthesized per parsed line; the
browser as metronome on a separate `/show` page. Of the two
patches the brief was opened to place, **the sanitizer is not
built** (there is no label to strip) and **the accumulator stays**,
with its unit bounded by the script line and its rules ruled
(Q9). The fork itself became a new app, TalkWithZombies, in a
sibling repository, free to diverge (ADR-0002).

### 9.3 What the seams cost — the ledger, closed

- **S1, the reference clip on every request:** bandwidth only, a
  few tens of milliseconds per line on our tunnel; the engine
  caches the encoded voice per clip. Accepted as is.
- **S2 + S6, emotion:** tts-serve is indifferent to how many clips
  a persona has and, for two engines, exposes explicit emotion
  knobs; TalkWithMe had no channel for a per-line register. The
  adopted prompt structure supplies the channel — a parenthetical
  stage direction in the script line — and the mapping to a clip
  or knob is fork work after Task 4's clips exist. Cost: one
  lookup in the server, and the clips themselves.
- **S3, text length:** no limit exists in tts-serve; the cost of
  a chunk is latency, and the measurement that would tune it is
  deferred to follow-ups. The fork starts at N = 100.
- **S4, two engines on one box:** each engine is its own process
  and venv; the Ansible role selects one. The cost is a role
  change when 5b needs two — 5b's problem.
- **S5, telemetry the client discards:** free to collect, unused
  until a director wants a pacing model. Post-MVP.

Two costs are not in the ledger because they are not seams but
consequences of the chosen structure, and they are the risks
ADR-0003 names: identity bleed across four characters in one
context (C4), answered by the bibles and the audition; and the
growing script against the context window (C9 in its new form),
answered by the director's transcript curation.

### 9.4 What the code surfaced that the brainstorm had not (umbrella §8, in one breath)

An STT proxy that substitutes a literal "No response received"
text which the browser then sends as the user's message; a
microphone not gated on playback; transcripts auto-sent with no
review; replies cut at the token cap and spoken as fragments; no
streaming synthesis anywhere; one synthesis at a time per engine.
And three challenges that got easier: proper names (Whisper's
`prompt` and `language` fields, unsent today, a few lines in the
proxy), mixing (the browser already owns a Web Audio context), and
the sentence-chunk prosody problem (a fixed seed per reply removes
the dice, and the accumulator removes the chunking). The show page
inherits the fixes to the first two by construction — hold-to-talk
enabled only in the listening state, transcripts entering as
audience traffic through the director — and the others are
fork-sized.

### 9.5 What stays open for the director arc

The brief mapped seams and did not design. What the next arc
inherits, with its receipts already in place:

- **The director's policy** — beats, cadence within the
  configurable time window, who is addressed, when the radio
  listens, how the 2024 escalation ("the radio smokes") is
  reproduced as state. The mechanism is decided (code in the
  server, allowlist into the grammar); the policy is not.
- **Transcript curation** — how the director keeps one growing
  script inside the context window: summarize, drop, or scaffold.
  The taxonomy filed this under the adaptation arc; the shared
  context makes it load-bearing sooner.
- **Directive content** — the entropy terms, the stage directions,
  the audience's line phrased as radio traffic; and the bounded
  scratchpad hypothesis (follow-ups) if the audition earns it.
- **Server-owned time** (story-loop Placement 2) — the upgrade for
  the unattended booth, additive to what the fork builds.
- **Emotion mapping** — register → clip or knob, once Task 4's
  clips exist (S2/S6).
- **Everything measured but not yet acted on** — the seed's
  reproducibility for the canned episode, the telemetry for
  pacing, the two-engine deployment shape for 5b.

### 9.6 The brief's verdict on itself

The mandate was a guided tour so that the owner's own study
started oriented and the fork's shape round argued from receipts.
The tours were read; the shape round became two design
discussions and two ADRs instead of a patch plan, because the code
said the patch plan was aimed at symptoms. Every claim in the
tours carries a path and a line; every ruling in the ledgers
carries a date and the owner's words. The HTML derivatives were
dropped as unnecessary once the decisions were made. What the
brief did not do, by design, is create the fork or write a line of
its code: that begins when ADR-0003's gate passes on a box.

## 10. Integration pass (unit 4)

*Not started. Will map the 2024 mechanisms (§7) onto TalkWithMe's
seams (tour document, section 5) and tts-serve's contract (unit 2).*

*Reframed 2026-09-21 (owner ruling, §2): unit 4 IS the
**prompt-structure discussion** — TalkWithMe's per-turn prompt
(one request per persona; system prompt = persona prompt +
memories + global prompt; history rewritten so other personas'
lines become `[Name]:` user turns) contrasted with the 2024
structure (one shared context, the model plays the whole cast in
`Name: line` wire format, a hidden in-prompt Narrator issues one
directive per turn carrying speaker, emotional register, word
count, and an entropy term), with the door explicitly left open
to a third structure neither of us has thought of yet. It gets its
own dated discussion doc; this section will hold the synthesis and
the pointer. The **story-loop discussion** (Q13's three
placements — browser timer, server plus push channel, external
process plus polling — against TalkWithMe's request-driven,
one-turn design) follows in its own doc, because the loop's shape
depends on who assembles the prompt.*

*Written 2026-09-21: `docs/discussions/2026-09-21-prompt-structure.md`
— direction ADOPTED by the owner: one shared context in screenplay
form, a code director setting per-round speaker allowlist and line
budget, one streamed request per round under a server-enforced GBNF
screenplay grammar, the existing SSE events synthesized per parsed
line. Consequences for this brief's ledgers: Q1, Q2, Q8 (the
sanitizer) are answered by construction — no label to strip; Q9
shrinks to one-word lines; S6 gets its channel (a parenthetical
stage direction in the script line). Final decision gated on two
on-box confirmations and one audition item (that document §11).*

*Also written 2026-09-21: `docs/discussions/2026-09-21-story-loop.md`
— DECIDED: Placement 1, the browser as metronome and the server as
director (Q13 answered), on a separate `/show` page; endless loop
with cadence-based interaction beats; half-duplex hold-to-talk;
dead air as day-three polish. With both decisions taken, the
reconnaissance brief's design mandate is complete; what remains of
the brief is the answer pass over the ledgers, unit 3's synthesis,
and the HTML visuals.*

*Parked candidate raised on 2026-09-21 (tts-serve tour §8, Q5):
**experiment 5d / question Q7** — a Mac-local TTS probe. tts-serve
ships a native Apple-Silicon engine (Qwen3-TTS via MLX, tag 1.2)
and five engines accept PyTorch's `mps` device. If the owner's Mac
has enough unified memory, the whole stack (llama.cpp on Metal,
Whisper, a tts-serve engine) could run locally — a second
emergency mode for demo day next to the canned episode, and a
free rehearsal setup. Needs: the Mac's chip and memory; one
evening; no box.*

## 11. Update trail

- **2026-09-21** — Document created after the shape rulings of the
  same day (units, seam ledger, documents, visuals folder, cadence,
  path and writing rules). Prologue (§7) written from the read of
  `zombie_radio_ai` and the owner's recollections. Seam questions
  S1–S3 opened. Glossary opened with the entropy-term decision.
- **2026-09-21, later** — Cadence changed to breadth-first (owner
  ruling). tts-serve tour written; S1 and S2 received proposed
  resolutions, S3 was reframed as a measurement, S4 and S5 opened.
  Glossary gained the tts-serve terms and the ICL/x-vector,
  staging, and RTF entries.
- **2026-09-21, later still** — The owner's six follow-up questions
  on the tts-serve findings were answered and persisted: Q1–Q5 in
  the tts-serve tour §8; Q6 as the new §8 here ("C1–C10
  revisited", canonical copy appended to the brainstorm document).
  Seam question S6 (per-request TTS parameter overrides) opened.
  Candidate experiment 5d / question Q7 noted: a Mac-local TTS
  probe with tts-serve's MLX engine (see tts-serve tour §8, Q5).
  Sections renumbered: synthesis §9, integration §10, update trail
  §11.
- **2026-09-21, "do not worry about upstream" ruling** — recorded
  at the end of §2 and in §10; TODO.md (Task 6 disposition, arc
  boundary) and the upstream-contribution strategy (§7 addendum)
  carry the full text.
- **2026-09-22, synthesis written (unit 3)** — §9 integrates
  units 1, 2 and 4 and closes the brief before PR #6 merges, as
  the owner asked.
- **2026-09-22, answer pass complete** — one ruling at a time
  with the owner: S1 resolved; S2 and S6 resolved in principle
  (fork work after Task 4); S3/Q4 dropped from the arc to
  follow-ups, provisional N = 100; S4 parked to 5b; S5 parked
  post-MVP; Q5 confirmed; Q6 with S1; Q7 parked post-MVP (demo Mac
  16 GB; a 64 GB M1 exists); Q9 packing rules ruled; Q10 all knobs
  yaml-only; Q11 no new Node harness. HTML visuals dropped.
  Synthesis (§9) flagged as the last item before PR #6 closes.
- **2026-09-21, story loop decided** — the story-loop discussion
  doc written; §10 points at it; Q13 marked decided and Q3 moot on
  the show page in the index.
- **2026-09-21, prompt-structure direction adopted** — the
  prompt-structure discussion doc written (unit 4 delivered as its
  own document); §10 points at it; Q1/Q2/Q8 marked moot in the
  index; S6's channel noted.
- **2026-09-21, unit 1 breadth pass closed** — TalkWithMe tour
  sections 2–6 written; Q8–Q13 added; the question index §5b
  created (Q1–Q13). Unit 1's breadth pass is complete; the pile is
  ready for the answer pass or for unit 4's breadth questions.
