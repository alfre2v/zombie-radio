# Task 6 reconnaissance — the tts-serve tour (unit 2)

**Date:** 2026-09-21 (opened; living until Task 6 starts) ·
**Arc:** MVP prototype · **Branch:** `alfre2v/task6-recon-brief`
**Type:** guided code tour, unit 2 of the Task 6 reconnaissance
brief (umbrella: `docs/discussions/2026-09-21-task6-reconnaissance-brief.md`).
Scoped to what TalkWithMe consumes: the synthesize contract, the
engine abstraction, and voice-reference handling — widened only
where the reading forced it.
**Status:** breadth pass written (the owner's 2026-09-21 ruling:
gather questions across all products first, answer product by
product afterwards). Open questions are marked OPEN.

*Context for the cold reader.* tts-serve is scorbo2's second
project, the voice side of our stack. It is a small framework: one
FastAPI server script per open-source text-to-speech engine, all
speaking the same REST vocabulary, plus a shared pure-Python
package that generates each server's machine-readable
self-description (`GET /capabilities`). The client — TalkWithMe in
our case — only ever needs to know tts-serve; which engine sits
behind it is a server-side detail. We run one engine,
**faster-qwen3-tts** (a CUDA-graphs speed fork of Qwen3-TTS), on
the rented GPU box, bound to loopback on port 8001 behind the SSH
tunnel. Task 5b's first candidate for a second engine, **LuxTTS**,
is also wrapped by tts-serve. Eight engines are wrapped at tag 1.2.

*All paths below are absolute paths into the owner's clone,
`/Users/alfredo/workspace/hackTNT_2026/tts-serve/`, at tag **1.2**
(commit `b1f06b7`). Where a receipt is in the TalkWithMe or in
this repository, its path says so. Labels: measured = inspected in
the code or run; docs-say = upstream's own documentation;
believed = inference.*

---

## 1. Orientation

- **Layout.** `tts-engine-common/` is the shared package (no
  torch, importable on any machine): the request/response core
  vocabulary, the capabilities derivation, the `/capabilities`
  route, language helpers, and the reference-audio staging
  helpers. `impl/` holds the eight server scripts, each 500 to 800
  lines, plus GPU-free tests and committed snapshots of each
  server's capabilities document. `tools/speak.py` is a
  stdlib-only command-line client that discovers a server's
  parameters from `/capabilities`. `docs/` holds the design
  documents; `docs/01-server-generification.md` carries the seven
  binding decisions D1–D7.
- **Versions, measured.** Our deployment currently pins tts-serve
  at tag `1.1` (`deploy/ansible/inventories/common_vars.yml:53` in
  this repository). The clone read for this tour is at `1.2`. The
  diff between the two tags adds only the Apple-Silicon MLX engine
  (`impl/server_qwen3TTS_mlx.py`, its doc, tests, stubs, and
  snapshot); the shared package and our engine's server are
  byte-identical across the two tags, so everything in this
  document holds for the box as deployed today. **Owner ruling
  2026-09-21: the pin is not set in stone — we track the latest
  tag (1.2 as of today) unless a release breaks the deployment or
  the TalkWithMe contract. The bump of `zr_tts_serve_version` to
  `"1.2"` happens at the next box deployment and is proven there
  (from-zero converge, idempotent re-run), not in this brief.**
  Release history, docs-say and confirmed against the tagged trees:
  1.0 (2026-09-10) six engines; 1.1 (2026-09-15) added LuxTTS
  (`impl/server_luxTTS.py` is present in the 1.1 tree, absent in
  1.0); 1.2 (2026-09-18) added Qwen3-TTS (MLX).
- **How we run it, measured.** The Ansible role clones tts-serve
  at the pinned tag, builds one venv, installs the engine package,
  torch at our CUDA-variant pin, and the shared package, and
  launches `impl/server_fasterQwen3TTS.py` with the bind host and
  port passed as environment variables
  (`deploy/ansible/roles/tts_engine/vars/faster_qwen3tts.yml`,
  `deploy/ansible/roles/tts_engine/tasks/tts_engine_faster_qwen3tts.yml`
  in this repository). One engine per venv is upstream's rule too:
  the engines' dependency trees conflict
  (`/Users/alfredo/workspace/hackTNT_2026/tts-serve/README.md:38`).
- **House style, docs-say.** The README states the project is
  built spec-first: the human writes a detailed spec, an LLM
  (Qwen 3.8 27B, mostly) implements, and the spec is kept in step
  with the code. `AGENTS.md` is 52 dense lines. There is no lint,
  CI, formatter, or pre-commit, and the agent guide says not to
  invent one (`AGENTS.md:11`). Tests never touch a GPU: engine
  packages are replaced by import-only stubs, and `/capabilities`
  output is snapshot-tested. Adding an engine is a documented
  workflow (`.agents/skills/new-tts-engine/SKILL.md`). This
  matters for how any patch we might one day offer should look.

## 2. The synthesize contract, as our client experiences it

The whole contract for our engine lives in the request model at
`/Users/alfredo/workspace/hackTNT_2026/tts-serve/impl/server_fasterQwen3TTS.py:158`
to 252 and the handler at lines 444 to 536.

- **Request fields.** `text` (required; at least one non-blank
  character; **no upper bound**), `audio_base64` (required; the
  reference voice clip; up to 10 million characters of base64,
  about 5 minutes of 24 kHz audio; any container soundfile
  decodes — WAV, MP3, OGG, FLAC), `reference_text` (required; the
  exact transcript of the clip), `language` (two-letter lowercase
  code or `auto`; default `en`; the server maps codes to the
  engine's lowercase names, `en` → `english`, line 462), `seed`
  (1 to 1000; random if omitted; echoed back), and three engine
  knobs — `temperature` (0–2), `top_p` (0–1), `repetition_penalty`
  (1–2) — all optional, engine defaults when omitted. Unknown
  fields fail with a 422 that names the field, by design decision
  D5 (`/Users/alfredo/workspace/hackTNT_2026/tts-serve/docs/01-server-generification.md:18`).
- **Response fields**, from the frozen core at
  `/Users/alfredo/workspace/hackTNT_2026/tts-serve/tts-engine-common/src/tts_engine_common/models.py:127`
  to 154: `audio_base64` (16-bit PCM WAV), `sample_rate` (24000
  for this engine), `seed` actually used, `time_used` (wall-clock
  seconds of synthesis), `rtf` (real-time factor: synthesis time
  divided by audio duration; `null` when not computable), plus a
  per-request id `fid`.
- **Pre-flight, in order** (handler lines 455–482): resolve the
  seed; map the language; strict base64 decode, or **400** (line
  476); a header-only check that the clip decodes and lasts **at
  least 2 seconds — this minimum is about the REFERENCE CLIP, not
  the text** (lines 546–562; the text may be as short as "Dr." or
  "1.", which is precisely how those fragments got synthesized in
  the prototype), or 400; then staging of the clip to disk (line
  482, see F1); then synthesis under a process-wide lock (line
  496). Any engine failure is a **500** carrying the message (line
  536). Malformed or unknown fields never reach this far: they are
  a 422 from Pydantic.
- **Self-description.** The capabilities document is derived from
  that same Pydantic request model at import time (line 273,
  `build_capabilities`), so it cannot drift from validation. Its
  snapshot for our engine
  (`/Users/alfredo/workspace/hackTNT_2026/tts-serve/impl/tests/snapshots/faster_qwen3_capabilities.json`)
  reads: schema version 2, engine `faster-qwen3-tts`, model
  `Qwen/Qwen3-TTS-12Hz-1.7B-Base`, 24 kHz, not watermarked,
  reference audio required with a 2 s minimum, ten languages plus
  `auto`. TalkWithMe reads this document to decide which fields
  to send (unit 1, hop 7), which is why an engine switch on the
  TalkWithMe side is safe by construction.

## 3. Findings

### F1 — The reference clip is re-sent every time by contract, but re-encoded only once (answers seam question S1)

*What we observed in unit 1.* TalkWithMe ships the persona's
reference clip — about 330 to 390 KB of base64 for our placeholder
voices — with every sentence it synthesizes.

*What tts-serve does with it.* There is no voice identifier and no
upload-once endpoint anywhere in the API. `audio_base64` is
required on every request (`reference_audio.required: true` in the
snapshot). So the per-request upload is the only contract.
However, the server stages the decoded bytes under a filename that
is the SHA-256 of the content, and keeps the file
(`/Users/alfredo/workspace/hackTNT_2026/tts-serve/tts-engine-common/src/tts_engine_common/staging.py:54`
to 95). A repeat request with the same clip finds the file already
there and skips the write (line 80). The engine then caches the
encoded voice prompt per file path and transcript, according to
upstream's own notes
(`/Users/alfredo/workspace/hackTNT_2026/tts-serve/AGENTS.md:44`).
The file is kept on purpose: staging happens before the synthesis
lock is taken, so a per-request delete could remove a file that a
queued request for the same clip is about to read (staging.py
lines 63–68). Disk grows only with the number of unique clips;
the staging directory lives under the system temp dir and is
wiped on reboot.

*Consequence.* The compute cost of encoding a voice is paid once
per unique clip per server process. What repeats per sentence is
only the tunnel bandwidth and a base64 decode. On our measured
~60 ms round trip to the CANADA-1 box, 400 KB is a few tens of
milliseconds. *Labeled: measured for the staging; docs-say for the
engine's prompt cache.*

*Proposed resolution for S1:* per-request upload is the contract,
the recurring cost is bandwidth only, and it is small. No fork
work needed. A voice-identifier API would be an upstream feature
idea, not an MVP need.

### F2 — tts-serve puts no upper bound on text length; the accumulator's N is bounded by latency and quality, not by a limit (partially answers S3)

`text` has `min_length 1` and no `max_length` in the snapshot,
and no server bounds text length at all — the only `max_length`
in `impl/` is IndexTTS's eight-component emotion vector, which is
unrelated. The engine package itself (`faster_qwen3_tts`, a pip
package) is not on disk here, so how it behaves on long input —
whether it chunks internally, or degrades — cannot be read. It has
to be measured on a box.

The instrument is already built in: every response carries
`time_used` and `rtf`. A measurement protocol for S3 costs one
evening: send the same voice with texts of increasing length
through `tools/speak.py` or curl, record `time_used` and the audio
duration, and plot time-to-audio against characters. That curve is
exactly what sets N.

### F3 — Several emotional references per persona cost tts-serve nothing; the blocker is entirely in TalkWithMe (answers S2 on the tts-serve side)

Each request is stateless and carries its own clip and transcript.
Two clips for the same persona are simply two content hashes, each
cached separately by the engine. So one persona with a calm
reference and a frightened reference is supported today by
tts-serve at no extra cost. What prevents it is TalkWithMe: one
`ref.wav` per persona directory, and the TTS proxy looks the clip
up by persona name only
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/routers/tts.py:134`).

A second path exists for later. IndexTTS exposes explicit emotion
control: an eight-component vector with labeled components (happy,
angry, sad, afraid, disgusted, melancholic, surprised, calm), or a
second "emotion" clip blended with the speaker's own, or free
text (`/Users/alfredo/workspace/hackTNT_2026/tts-serve/impl/README.md:89`
to 103). That engine outputs 22.05 kHz. Worth knowing when 5b picks
engines; not a Task 6 matter.

### F4 — There is no streaming synthesis anywhere; sentence pipelining in the browser is the only "streaming" we have

Every server returns one complete WAV per request. No server
offers chunked or incremental audio (grep across `impl/` finds
none; the MLX server's docstring says so explicitly at
`/Users/alfredo/workspace/hackTNT_2026/tts-serve/impl/server_qwen3TTS_mlx.py:14`).

*Consequence for the accumulator.* A larger N means a longer wait
before that chunk's audio can start, because nothing plays until
the whole chunk is synthesized. So the accumulator trades fewer,
better-sounding requests against time-to-first-audio per chunk.
The S3 measurement curve (F2) quantifies that trade.

### F5 — One synthesis at a time per server, by lock

`_synthesis_lock`
(`/Users/alfredo/workspace/hackTNT_2026/tts-serve/impl/server_fasterQwen3TTS.py:359`)
serializes synthesis because the engine replays captured CUDA
graphs with static buffers and shares a prompt cache. Concurrent
requests queue.

- For one TalkWithMe client this is invisible: the browser already
  sends one request at a time (unit 1, hop 6).
- For a future director that prefetches lines for several
  personas, requests will queue on the GPU regardless, so the
  director's pacing model must assume serial synthesis.
- For Task 5b's two-engine stack, two engines means two processes
  in two venvs on two ports, which upstream explicitly supports.
  Our Ansible role currently selects one engine by name
  (`zr_tts_engine: faster_qwen3tts`), so 5b needs a role change to
  run two. Noted for 5b (seam question S4); out of scope here.

### F6 — The response carries measurements TalkWithMe throws away

`time_used`, `rtf`, and `seed` come back on every synthesis.
TalkWithMe reads only `audio_base64`
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/tts.js:178`).
Two uses for us: 5b's engine comparison can be instrumented from
the responses alone, and a director that wants to predict how long
a line takes to synthesize has the data on hand. The seed also
makes a line reproducible — same text, same clip, same seed gives
the same audio (bit-exact on CPU, near-exact on CUDA per
`AGENTS.md:48`) — a small gift to the canned-episode work.

### F7 — The two candidate engines want different reference material (shapes Task 4)

Our engine runs in-context-learning (ICL) mode only, so the exact
transcript is **required** and there is no speaker-embedding
fallback
(`/Users/alfredo/workspace/hackTNT_2026/tts-serve/impl/server_fasterQwen3TTS.py:179`
to 187). Reference clips under 2 seconds are refused with a 400;
upstream's docstring calls about 3 seconds the sweet spot (lines
104–107). LuxTTS needs **no transcript** because it runs Whisper on
the clip itself on every request (so every request pays the ASR
cost), refuses clips under 3 seconds, and its notes say roughly
10 seconds of clean speech clones best, with a `prompt_duration`
knob defaulting to 5 seconds
(`/Users/alfredo/workspace/hackTNT_2026/tts-serve/impl/tests/snapshots/lux_tts_capabilities.json`).

*Consequence for the owner's voice-sample gathering (Task 4):*
collect about 10 seconds of clean speech per actor, and produce an
exact transcript for each clip. That covers both engines. Whisper
on the box can draft the transcripts.

### F8 — Output sample rates differ per engine, and the client does not care

24 kHz for our engine, 48 kHz for LuxTTS and dots.tts, 22.05 kHz
for IndexTTS (`AGENTS.md:29`). TalkWithMe decodes with the
browser's AudioContext, which handles any rate, and stores
whatever WAV it received. No work.

### F9 — Our engine exposes three sampling knobs we have never touched

`temperature`, `top_p`, `repetition_penalty`
(`server_fasterQwen3TTS.py:207` to 224). Our seeded settings send
an empty parameter map, so the engine's defaults apply. TalkWithMe
forwards any configured value the engine advertises
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/services/tts_client.py:503`
to 509), and its Servers dialog renders them from the capabilities
document. If 5b hears artifacts, these are the knobs, reachable
from the TalkWithMe settings UI without code.

### F10 — LuxTTS needs no tts-serve code from us

LuxTTS has been an engine since tag 1.1 (present in the 1.1 tree,
absent in 1.0) and is in 1.2, the tag we move to. So 5b's first
check needs no tts-serve code at all — only a second engine
variable file and venv on our side. Its per-request Whisper cost
and its ~10 second librosa warm-up on the first request
(`/Users/alfredo/workspace/hackTNT_2026/tts-serve/impl/server_luxTTS.md:24`)
are the things to measure. It exposes `num_steps` (default 4),
`guidance_scale`, `t_shift`, `speed`, `prompt_duration`,
`prompt_rms`, and `return_smooth`; it accepts a `language` code
for API consistency but does not forward it (its tokenizer
auto-detects English and Chinese).

## 4. Seam ledger — proposed state after this pass

- **S1**, reference per request: resolvable now, see F1.
- **S2**, several emotional references: resolvable now on the
  tts-serve side, see F3. The remaining half is a TalkWithMe
  design question for the fork or the director.
- **S3**, text length: no hard limit exists. Reopened as a
  measurement question — the latency-versus-length curve on a
  box, see F2 and F4.
- **New S4**: two engines on one box for 5b — the deployment shape
  (two venvs, two ports; one role run twice or a list variable).
  Owed by the 5b planning, not by this brief.
- **New S5**: whether TalkWithMe should surface or log `time_used`
  and `rtf`, and where. Owed by the director design; parked.

The ledger itself lives in the umbrella document, §5.

## 5. Upstream vocabulary met in this tour

Engine and engine slug · core vocabulary (`text`, `audio_base64`,
`reference_text`, `language`, `seed`) · capabilities document and
schema version · in-context-learning (ICL) mode versus
speaker-embedding-only (x-vector) mode · staging
(content-addressed and kept, versus one-shot and deleted) ·
real-time factor (RTF) · reference audio spec. Definitions in the
umbrella document's glossary.

## 6. Reading itinerary for the owner (one sitting)

1. `/Users/alfredo/workspace/hackTNT_2026/tts-serve/tts-engine-common/README.md`,
   the whole file. The clearest statement of the design.
2. `/Users/alfredo/workspace/hackTNT_2026/tts-serve/impl/server_fasterQwen3TTS.py:158`
   to 252, the request model; then 444 to 536, the handler. Our
   engine end to end.
3. `/Users/alfredo/workspace/hackTNT_2026/tts-serve/tts-engine-common/src/tts_engine_common/staging.py:54`
   to 95, the content-addressed staging and why the file is kept.
4. `/Users/alfredo/workspace/hackTNT_2026/tts-serve/docs/01-server-generification.md:10`
   to 20, the seven decisions in one table.
5. `/Users/alfredo/workspace/hackTNT_2026/tts-serve/AGENTS.md:39`
   to 48, the per-engine quirks — the densest page in the repo.

Question to hold while reading: which of the engine's costs are
per unique voice, and which are per sentence?

## 7. Questions added to the pile (OPEN, not to be answered in the breadth pass)

- **Q4 — OPEN.** The S3 measurement: do we run the
  latency-versus-length curve before the fork decides N, or pick a
  provisional N and measure later?
- **Q5 — OPEN.** Task 4 reference material spec: about 10 seconds,
  clean, with exact transcripts, one clip per actor now and
  possibly one per emotional register later. Does that match what
  the owner planned to collect?
- **Q6 — OPEN.** Whether the fork should keep the per-sentence
  reference upload as is. The agent's reading says yes, it is
  cheap (F1).

## 8. Owner questions answered after the breadth pass (2026-09-21)

*Five questions the owner asked after reading the tts-serve
findings, with the agent's answers persisted at conversation-level
detail. Q6 of the same round — the brainstorm's ten voice
challenges re-read against both codebases — lives in the umbrella
document (§8) and, canonically, as a dated addendum to the
brainstorm document itself
(`docs/discussions/2026-09-13-product-definition-brainstorm.md`).
Path conventions as in the rest of this tour: sibling-clone files
absolute, this repository's files root-relative.*

### Q1 — The measurements in every synthesis response, one by one

All fields come from the frozen response core at
`/Users/alfredo/workspace/hackTNT_2026/tts-serve/tts-engine-common/src/tts_engine_common/models.py:127`
to 154, filled by our engine's handler at
`/Users/alfredo/workspace/hackTNT_2026/tts-serve/impl/server_fasterQwen3TTS.py:494`
to 532. TalkWithMe reads only `audio_base64` and discards the rest
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/tts.js:178`).

- **`sample_rate`.** The output rate in Hz — 24000 for our engine,
  48000 for LuxTTS and dots.tts, 22050 for IndexTTS. Not a
  measurement of the request but a fact about the audio produced.
  *Use for us:* the moment we mix anything with the voice —
  static, dead-air texture, sound effects (brainstorm challenge
  C8) — every source must be at one rate, and this field tells the
  mixer what it received. Today nobody needs it: the browser's
  AudioContext resamples on decode.
- **`seed`.** The random seed the engine actually used, an integer
  in 1–1000. If the request omits it, the server draws one and
  reports it (`server_fasterQwen3TTS.py:458`); it is applied with
  `torch.manual_seed` inside the synthesis lock (line 497). *Use
  for us, three ways.* (1) *Reproducibility:* the same text, clip,
  transcript, and seed give the same audio — bit-exact on CPU,
  near-exact on CUDA because of non-deterministic GPU kernels, per
  upstream's notes
  (`/Users/alfredo/workspace/hackTNT_2026/tts-serve/AGENTS.md:48`)
  — so a good take of a line can be re-synthesized identically,
  which the canned episode (Task 7) may want. (2) *Fair
  comparison:* in Task 5b, holding the seed fixed while moving one
  knob isolates the knob from the dice. (3) *Debugging:* when a
  line comes out garbled, replaying it with the reported seed
  reproduces the failure instead of chasing a ghost.
- **`time_used`.** Wall-clock seconds of the engine call alone,
  measured server-side around the synthesis lock (lines 494–507).
  It *excludes* the network, the base64 decoding of the clip, the
  staging write (line 482 runs before the timer starts), and the
  WAV encoding after synthesis (line 514 runs after the timer
  stops). *Use for us:* it is the S3 instrument — synthesis time
  against text length — directly. A director that wants to know
  how long a line will take before it is spoken can build a
  predictor from this number. It is also a health signal: on a box
  under thermal or memory pressure this creeps up while every
  request still returns 200.
- **`rtf`, real-time factor.** `time_used` divided by the duration
  of the audio produced
  (`/Users/alfredo/workspace/hackTNT_2026/tts-serve/tts-engine-common/src/tts_engine_common/core.py:33`
  to 48; `null` when the duration is zero or the value is not
  finite). Below 1.0 means the engine produces speech faster than
  it plays. *Use for us:* it is the one number that says whether
  the sentence pipeline can stay ahead of playback. With RTF *r*
  and a chunk that will play for *D* seconds, the chunk costs
  about *r × D* seconds to produce, so the wait before that chunk
  can start playing is *r × D* plus network. English speech runs
  at roughly 15 characters per second, so a chunk of *N*
  characters plays for about *N / 15* seconds. That turns the
  accumulator's N into a predicted time-to-first-audio,
  *r × N / 15* plus network — exactly the trade-off of finding F4,
  now with a formula. In 5b it compares engines independent of
  line length.
- **`fid`.** A random UUID per request (line 529). Only useful for
  correlating logs, and the server's own log lines do not print it
  (lines 464 and 518), so today it is decoration. *Believed.*
- **A derived measurement the client could add.** The browser's
  wall-clock for the whole `fetchTTS` call minus the server's
  `time_used` equals the network plus overhead — which is exactly
  the cost of shipping the reference clip that seam question S1
  asked about. One subtraction in `tts.js` would quantify S1 for
  free.

### Q2 — Emotion control in tts-serve: no central knob; the clip carries the emotion

The owner's reading is right. There is no centralized emotion knob.
The core vocabulary is deliberately tiny — text, clip, transcript,
language, seed — by design decision D2
(`/Users/alfredo/workspace/hackTNT_2026/tts-serve/docs/01-server-generification.md:15`),
and everything else is whatever an engine happens to advertise.
Grepping the eight servers for emotion-adjacent request fields
gives the complete list (measured, 2026-09-21):

- **IndexTTS:** `emotion_audio_base64` plus `emotion_alpha` (a
  second clip blended with the speaker's own emotion),
  `emotion_vector` (eight labeled components: happy, angry, sad,
  afraid, disgusted, melancholic, surprised, calm), `emotion_text`
  (free text; needs the server started with
  `INDEXTTS_USE_QWEN_EMO=1`) —
  `/Users/alfredo/workspace/hackTNT_2026/tts-serve/impl/server_indexTTS.py:220`
  to 256. Output 22.05 kHz.
- **Chatterbox:** `exaggeration`, described in the design doc as
  "expression/energy boost — about 0.5 general use, about 0.7 and
  up dramatic", and `cfg_weight`
  (`/Users/alfredo/workspace/hackTNT_2026/tts-serve/impl/server_chatterbox.py:168`
  and 177). A coarse intensity dial, not an emotion selector.
- **LuxTTS:** `speed` only
  (`/Users/alfredo/workspace/hackTNT_2026/tts-serve/impl/server_luxTTS.py:224`).
- **Our engine, faster-qwen3-tts:** `temperature`, `top_p`,
  `repetition_penalty` — they shape token sampling, not emotion.

For every other engine, and for ours, the emotion lives in the
reference clip. That is the same approach the owner took in 2024
(one emotionally matching clip per character; he ran out of time
to collect clips for several emotions), and finding F3 showed
tts-serve supports several clips per persona at no extra cost.

The gap is elsewhere, and it is on both sides at once: TalkWithMe
exposes engine knobs as ONE global settings map
(`settings.tts.parameters`), not per persona and not per line, and
its TTS request carries only the text and the persona name
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/models.py:56`
to 59). So a director that wanted to say "this line, frightened"
has no channel for it today — neither by clip nor by knob. This
became seam question **S6** in the umbrella document: per-request
TTS parameter overrides through TalkWithMe's `/api/tts`.

### Q3 — Emotion control in TalkWithMe: no sign of a knob coming

A grep over the app, the static scripts, the docs, and the README
for *emotion*, *mood*, *style*, *expressive*, and *exaggeration*
(2026-09-21, tag 7.1) finds only three kinds of hit:

- The generic parameter renderer knows how to draw IndexTTS's
  eight-component vector with its labels
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/tts-params.js:26`;
  design notes in
  `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/docs/feature_TTS_generification.md:161`
  to 173).
- The persona-memory feature lists "strong emotions" as something
  worth remembering about the *user*
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/services/builtin.py:136`).
- The README links a video titled "Generifying TTS settings /
  cloning voices with emotion"
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/README.md:17`),
  which suggests scorbo2 has explored emotion through reference
  clips — not watched, so *docs-say*.

The persona model has exactly one reference clip and one
transcript
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/config.py:272`
to 274). The direction of travel in the code is clear: emotion
arrives as engine parameters rendered generically and set
globally. Nothing per persona, nothing per line, nothing in
progress at 7.1.

### Q4 — F5-TTS (the 2024 engine) against the modern engines

Three layers: what this repository already knows, what the web
said on 2026-09-21, and the agent's assessment.

**What the repository already knows.** The 2026-09-15 ranking
(`docs/experiments/2026-09-14-talkwithme-remote-split-test/tts-engine-ranking.md`)
ranked the six then-available tts-serve engines for the spike with
driver compatibility as the deciding filter, picked Faster
Qwen3-TTS, named Chatterbox the early favorite for the production
four-voice role because it clones without a transcript, and noted
that F5-TTS is not in tts-serve. Adding it is a recorded soft goal
(`docs/follow-ups.md`, "Add new TTS engines to tts-serve").

**What the web says now** — all *docs-say*, with the caveat that
the 2026 comparison articles disagree with each other loudly:

- The F5-TTS code is alive: the Python package reached 1.1.22 on
  2026-07-23 with performance work (flash attention in its
  transformer, fused optimizer, gradient checkpointing), but the
  base checkpoint is still "F5-TTS v1 Base" from March 2025, so
  the model itself is about 18 months old.
- Resource reports are inconsistent: one source says 2–3 GB of
  VRAM at half precision, another says about 8 GB "for reasonable
  speed", and CPU inference is 10–30× slower than real time. It is
  a flow-matching model that runs many denoising steps per
  utterance, which is where the cost sits.
- Quality: several 2026 roundups still call it the naturalness
  leader for English and Chinese and "the answer if absolute peak
  quality matters more than setup complexity". One blind ranking
  of eleven systems put dots.tts first and placed Chatterbox,
  Qwen3-TTS, and IndexTTS-2 near the bottom (IndexTTS-2 described
  as "robotic, too fast"). Another article reports Chatterbox
  preferred over ElevenLabs in a listener study (65 % vs 25 %).
  Read all of this as taste plus test conditions, not as a settled
  ranking.
- LuxTTS is a distilled ZipVoice — the same flow-matching family as
  F5-TTS, distilled to four sampling steps with a 48 kHz vocoder —
  claiming 150× real time and under 1 GB of VRAM, Apache-2.0. That
  is precisely the "F5-like quality without F5's cost" claim, and
  it is why Task 5b checks it first.

**Assessment.** F5-TTS is viable but expensive in the one currency
we lack: time before 2026-10-08. It is not in tts-serve, so using
it means writing an engine wrapper first — half a day to a day
using upstream's own skill file
(`/Users/alfredo/workspace/hackTNT_2026/tts-serve/.agents/skills/new-tts-engine/SKILL.md`)
— before a single comparison can run. Its heaviness as the owner
remembers it was partly the whole 2024 stack on one PC (Gradio app
plus Whisper plus Ollama), but the many-step generation is real and
the model was never built for low latency. The two engines already
wrapped — our current one and LuxTTS — cover both ends of the
quality-versus-cost spectrum without any wrapper work, and
Chatterbox is a third if time allows. **Recommendation:** keep
F5-TTS as the post-deadline soft goal it already is, and let 5b
decide among the wrapped engines. If the audition finds all of
them wanting on expressiveness, that is the trigger to revisit.

Sources consulted (2026-09-21): a blind ranking of eleven voice
cloning systems
(<https://medium.com/@austin-starks/best-ai-voice-cloning-in-2026-i-cloned-my-own-voice-seven-ways-and-ranked-them-blind-404807485d43>);
Pinggy's self-hosted TTS roundup
(<https://pinggy.io/blog/best_open_source_self_hosted_text_to_speech_models/>);
Instavar's TTS decision tree
(<https://instavar.com/research/tts/choose-a-tts-model>) and
F5-TTS fine-tuning guide
(<https://instavar.com/research/tts/f5-tts-fine-tuning>); Voice
Creator Pro's Qwen3/OmniVoice/Chatterbox comparison
(<https://voicecreator.pro/blog/qwen3-vs-omnivoice-vs-chatterbox-voice-cloning>);
NexGPU's F5-TTS deployment page
(<https://nexgpu.net/en/models/f5-tts/>); Runpod's F5-TTS guide
(<https://www.runpod.io/articles/guides/f5-tts-on-runpod>); the
LuxTTS repository (<https://github.com/ysharma3501/LuxTTS>) and two
write-ups
(<https://hackernoon.com/luxtts-lightweight-voice-cloning-that-fits-in-1gb-vram>,
<https://themenonlab.blog/blog/luxtts-voice-cloning-150x-realtime-1gb-vram>).

### Q5 — MLX and the Mac: yes, and the thread is worth pulling

Two different mechanisms exist in tts-serve for running on a Mac:

- **One native Apple-Silicon engine**, Qwen3-TTS (MLX), added in
  tag 1.2, running through the `mlx-audio` library with an 8-bit
  checkpoint (`mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit`), ICL
  cloning only (transcript required), reporting its device as the
  literal `mlx`. Upstream built it "for a controlled A/B comparison
  between the stock PyTorch/MPS server and MLX on the same Mac"
  (`/Users/alfredo/workspace/hackTNT_2026/tts-serve/impl/server_qwen3TTS_mlx.md:3`
  to 9) — which tells us scorbo2 runs TTS on a Mac himself. It
  deliberately lacks the sampling knobs, long-text chunking,
  streaming, and preset voices of its PyTorch sibling (lines
  20–37).
- **Five servers accept the device `mps`** — PyTorch's Metal
  backend for Apple GPUs: Chatterbox, OmniVoice, Qwen3-TTS, LuxTTS
  (which falls back from CUDA to MPS to CPU on its own, and has an
  ONNX CPU path with a thread count), and IndexTTS (auto-select
  order CUDA → XPU → MPS → CPU). *Not Mac-capable:* our
  faster-qwen3-tts, which refuses any non-CUDA device at load
  (`server_fasterQwen3TTS.py:139`), and dots.tts, which auto-selects
  CUDA or CPU only.

**Viability:** unmeasured by us, and MPS support in these engines
is the kind of thing that works until one operator is missing. But
the MLX server's existence is strong evidence that at least
Qwen3-TTS runs usefully on a Mac.

**Why the thread matters for us:** llama.cpp already runs on Apple
Metal, Whisper runs anywhere, so a Mac with enough unified memory
could run the ENTIRE stack locally — no GPU box, no tunnel, no
venue internet. That is a second emergency mode for demo day next
to the canned episode, and a rehearsal setup that costs nothing
per hour. Two unknowns the owner must supply: which Mac this is
(chip and memory), and whether he wants a cheap probe — running
`server_qwen3TTS_mlx.py` on the laptop, pointing TalkWithMe's TTS
URL at it, and reading `rtf` from a few sentences. No box needed.
Filed as candidate experiment **5d** and question **Q7** in the
pile; not started.

## 9. Update trail

- **2026-09-21** — Document created from the breadth-pass read of
  tts-serve at tag 1.2 (sections 1–7), at conversation-level
  detail (owner rule). Owner corrections folded in the same day:
  the 2 s minimum is about the reference clip, not the text; the
  deployment pin moves to the latest tag (1.2), proven at the next
  deployment.
- **2026-09-21, later** — §8 added: the owner's five follow-up
  questions (response measurements one by one; emotion control in
  tts-serve and in TalkWithMe; F5-TTS versus the modern engines,
  with web sources; MLX and Mac viability) answered at
  conversation-level detail. Update trail renumbered to §9.
