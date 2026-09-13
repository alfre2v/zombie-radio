# Product definition arc — Q&A log

**Started:** 2026-09-12 · **Arc:** Product definition
**Status:** append-only ledger, live for the duration of the arc.

*Purpose: during long exploratory Q&A sessions, this doc persists
the questions and answers the owner will need to go back to — the
owner does not hold a million-token context. Each entry is dated and
appended after a discussion round lands something worth keeping.
When content here settles, it graduates to the spec or an ADR; this
log remains as provenance.*

---

## Entry 1 — 2026-09-12: first ideation organized (agent's map of the owner's free-form input)

### What sounds close to settled (candidate principles, not yet ADRs)

1. **"Local AI first" is the soul** — open models you can run
   yourself. But this time with an escape hatch: the same backend
   must deploy to a rented cloud GPU box for people without a
   3090-class card. Note this is *"local-first, cloud-capable"* — a
   nice one-line identity for the spec.
2. **Client/server split.** One backend (GPU-heavy: LLM + TTS, maybe
   STT); at least a web client, maybe also a CLI client. This is
   *the* structural change vs. the 2024 CLI monolith.
3. **Deployment doctrine**: Dockerized model services, Ansible-driven,
   idempotent, targeting Linux only. Reuse deployment logic from the
   owner's other project — pointer to that repo still needed.
4. **Dependency skepticism as a stance**: evaluate LiveKit/Pipecat
   fairly, but don't let the project drown in complexity or marry
   one framework.

### What the agent verified about the fallback plan (receipts, fetched 2026-09-12)

Honestly, "backup plan" may be underselling it — these look like
strong primary candidates:

- **TalkWithMe** (MIT, v7.0 released *2026-09-10*, 209 stars):
  Python/FastAPI backend + modular JS frontend, connects to
  llama.cpp via OpenAI-compatible API. Crucially it already has
  **multi-persona group chats** with configurable routing
  (LLM-decided/random/manual), persona-to-persona replies,
  **streaming TTS playback** (sentence-chunked for fast first
  audio), optional STT via whisper-fastapi, voice cloning with
  reference audio, and per-room persistence. That's uncomfortably
  close to "4 AI voice actors talking to each other and a listener"
  already.
- **tts-serve** (MIT, young — first release Sep 2026, 17 stars, 36
  commits): FastAPI wrapper unifying six engines (Chatterbox,
  OmniVoice, Qwen3-TTS + a faster variant, dots.tts, Index-TTS)
  behind one REST API — `POST /synthesize` with
  text/reference-audio/seed, `GET /capabilities` for
  machine-discoverable params, returns base64 WAV plus timing/RTF
  metrics. **F5-TTS is not among the six**, so the owner's
  aspiration to add it is a real (and well-scoped) contribution.
  The RTF metrics it returns will be handy for latency experiments.

The main caution on both: bus-factor-one projects by one author;
young in tts-serve's case. That's an explicit tradeoff for the
survey, not a disqualifier.

### Research questions this raises (Task 2 fodder)

- Cloud GPU providers: which offer Docker **with** NVIDIA GPU
  passthrough cleanly (the owner's RunPod recollection needs
  checking — their container model historically constrained this),
  pricing, and Ansible-friendliness (do we get a plain SSH-able VM,
  or only their container abstraction? That difference decides how
  much of the existing deployment logic transfers).
- LiveKit vs Pipecat vs "TalkWithMe-and-friends": the fair
  evaluation. Early framing — LiveKit/Pipecat buy real-time
  *conversational* infrastructure (WebRTC transport, VAD, barge-in,
  turn-taking). Whether we need that depends entirely on the
  unanswered Task 1 questions: if the listener speaks rarely at
  story beats, plain WebSockets + streaming audio may be all the
  transport we need, and the frameworks' complexity buys little.
- F5-TTS vs the newer engines — quality/latency/voice-cloning
  comparison. Smells like our first `experiments/` folder.

### Open pushes at the end of Entry 1

Everything given so far is Task 2; Task 1 was still nearly empty —
and Task 1 decisions bound Task 2. The three questions to answer
next: (a) the Oct 8 demo scene, (b) the interaction mechanic and its
frequency, (c) live vs authored dialogue. Plus: the URL of the
owner's other project with the Ansible deployment pattern.

---

## Entry 2 — 2026-09-12: strategy inversion + the audience experience

### Decision (candidate, to be ratified in the spec): the backup plan is now the main plan

The owner concluded there is no time (~3 weeks) to explore and
understand LiveKit/Pipecat well enough. Inverted plan of attack:

- **Main plan**: adapt **TalkWithMe** (base for the client + persona
  orchestration) and **tts-serve** (unified TTS API), focusing the
  owner's effort on the **deployment side** and possibly on
  **bringing more TTS engines under tts-serve** (e.g. F5-TTS) — a
  potential upstream contribution.
- **LiveKit/Pipecat**: deprioritized from "candidates to adopt" to,
  at most, a brief comparison note in the survey.
- Trigger to revisit: TalkWithMe's architecture proves unadaptable
  to the radio-show format, or its single-maintainer model blocks us.

### The audience experience (Task 1 — now mostly defined)

- It's a **Halloween project meant to be fun in a shared
  environment**: played at an event gathering, in a **booth**, on a
  computer **running unattended** — playing like a radio until
  someone approaches and talks to it.
- **Fiction frame**: the 4 scientist-heroes reach out **via radio**
  from their hidden lab, narrating their struggle to survive the
  zombie apocalypse. Throwback to Orson Welles' 1938 *The War of the
  Worlds* — the Mercury Theatre on the Air Halloween broadcast.
- **The surprise**: from time to time the actors actually *listen*
  and answer back, engaging in a somewhat limited dialog with the
  user(s) — asking for help locating their secret lab, asking what
  day it is, asking the user's name so they can address them by
  name later.
- **The 2024 listening mechanic** (baseline to improve): the mic
  only listened when a voice actor asked for interaction and paused
  ~10 seconds; if sound arrived it kept listening until the user
  said **"over and out"**; STT was a Whisper model. The owner flags
  the listening-stop method as primitive — an improvement target
  for this version (modern endpointing/VAD).

### Still missing after Entry 2

- **Live vs authored dialogue** balance (the 2024 version improvised
  with a small LLM inside a story frame — is that still the model?).
- Session/loop shape: how long does the radio narration run before
  an interaction beat? Does the story loop for a whole evening?
- **Booth acoustics**: an unattended mic at a noisy Halloween event
  is a hard VAD/endpointing environment — how do we avoid the
  actors reacting to crowd noise? (Push-to-talk button in the booth?
  Directional mic? Wake mechanic?)
- Multi-user handling: several people talking at the booth at once.
- Oct 8 logistics: what hardware is physically in the booth, and is
  the GPU box local there or remote?
- Pointer to the owner's other project with the Ansible deployment
  logic (still owed).

---

## Entry 3 — 2026-09-13: voice challenges, dialogue spectrum, deferrals

- **Voice/sound challenges enumerated and homed.** The owner listed
  four hard problems (noise/Whisper nonsense, end-of-speech
  detection, speaker identification, sound-effects generation) and
  the agent added three (self-hearing/echo, addressee detection,
  proper-name capture). Their permanent home is
  [discussion 2026-09-13] `product-definition-brainstorm.md` §2–3 —
  this log only records that the list exists there.
- **Push-to-talk ruling context**: the owner considered a physical
  button in 2024 and rejected it as not magical — the wow effect is
  the radio *just hearing you*. Kept as fallback only.
- **2024 dialogue loop described** (now recorded in the brainstorm
  doc §4): fully live, one line at a time from a small LLM (owner
  recalls Qwen ~9B, correcting the earlier Nemotron-mini belief from
  the old repo README), conditioned on preceding lines, with random
  "entropy terms" drawn from themed word lists injected into each
  request to fight repetitiveness. Live-vs-authored for 2026 is now
  a framed decision (brainstorm §4), leaning hybrid, pending.
- **Ansible deployment project: deliberately deferred.** It lives in
  a private repo of the owner; this repo is public, so no content
  spills over. The owner will be surgical about what transfers, at
  deployment time. Do not ask again until the deployment sub-step
  opens.

---

## Entry 4 — 2026-09-13: MVP rulings (push-to-talk, laptop demo, live-first dialogue) + VAD explanation preserved

### Three rulings from the owner

1. **MVP interaction is push-to-talk.** The advanced always-listening
   pipeline (VAD → Whisper → semantic endpointing, preserved verbatim
   below) is tempting but NOT decided; it is post-MVP, attempted only
   if time remains. Push-to-talk gets us to an MVP fast. Side
   effects: by construction it solves endpointing (button release =
   end of speech), self-hearing (mic open only while held), and
   addressee detection (pressing the button IS addressing the radio)
   for the MVP — see brainstorm §2 for how each challenge is
   affected.
2. **Oct 8 demo is a laptop, not a booth.** The client runs on a
   simple laptop (probably a Mac); the server runs on a **cloud
   instance with an Nvidia GPU**. The visually cool unattended booth
   remains the future vision, explicitly out of scope for the first
   release. (New risk noted by the agent: the demo now depends on
   venue internet reaching a cloud GPU — worth a fallback thought
   before Oct 8.)
3. **Dialogue is live-first: "theatrical live improvisation with
   LLMs"** (the owner's phrase — a good product identity). The three
   weeks go to engineering, not storyline writing. Post-MVP hybrid
   idea: collect stories offline from bigger commercial LLMs, used
   NOT literally but as trajectory scaffolds to keep small local
   LLMs from looping ("they tend to loop like crazy"). Note this
   keeps local-AI-first intact: big commercial LLMs would be
   offline authoring tools; nothing commercial runs at show time.

### Preserved verbatim: the VAD / endpointing / thresholds explanation (agent, 2026-09-13)

*(kept word-for-word at the owner's request, for future revisiting;
"your challenge (a)/(b)" refers to the owner's enumeration that
became brainstorm §2 C1/C2)*

These are three separate problems that casual usage mushes together.
Untangling them:

**1. VAD (Voice Activity Detection)** answers one narrow question,
continuously: *"is this instant of audio human speech, or not?"* A
VAD processes tiny frames (~10–30 ms each) and emits a yes/no or a
probability for each frame. It does not transcribe, does not know
words — it's a speech/non-speech classifier, nothing more.

The *old* way (what most "silence detection" libraries do): measure
frame **energy** — loudness, roughly. If energy is above a
threshold, call it speech. This is what fails at a party: a door
slam, music, and crowd chatter are all high-energy, so the energy
VAD says "speech" constantly, and your downstream logic drowns.

The *modern* way: a small neural network trained on thousands of
hours of speech-vs-everything-else. **Silero VAD** is the standard
open one — a ~2 MB model that runs in real time on a CPU, eats
30 ms chunks, and outputs `P(speech)` between 0 and 1 for each
chunk. Because it learned what human speech *sounds like*
(harmonics, formants, cadence) rather than how *loud* things are,
it correctly rejects music and door slams that fool energy
detectors.

**2. Thresholds, and what "aggressive" means.** Since Silero gives
you a probability, *you* choose the cutoff. The default is ~0.5:
balanced. Setting it "aggressively" — say 0.8, plus rules like
"require at least 250 ms of consecutive speech frames before
believing it" — means you only accept clear, close, confident
speech. The trade: you'll miss some mumbled or distant speech
(false negatives) in exchange for almost never triggering on
background chatter (false positives). In a booth, that trade is
exactly right, *especially* combined with a directional mic placed
so visitors naturally lean in — physics does half the filtering,
the threshold does the rest. This directly attacks your challenge
(a): if the VAD gate never opens for noise, Whisper never sees the
noise, and never gets the chance to hallucinate a transcript from
it. (Second line of defense: Whisper itself reports
`no_speech_prob` and an average log-probability per segment —
discard transcripts where those look bad.)

**3. Endpointing** is the different, harder question: *"has the
person finished their utterance?"* — i.e., when to close the mic
and let the actors respond. A VAD only tells you "speech stopped";
endpointing must decide "speech stopped *and they're done*". The
naive rule you tried — end after N ms of continuous silence — fails
for two independent reasons:

- **Humans pause mid-sentence.** "My name is… uh…" has an 800 ms
  gap in the middle. Any N short enough to feel responsive (say
  700 ms) cuts these people off; any N long enough to be safe
  (2 s+) makes every exchange feel laggy.
- **In noise there is no silence.** The VAD (or energy detector)
  keeps flickering "speech" from the background, so the N ms of
  quiet never arrives and the mic never closes. This is why the fix
  for (a) and the fix for (b) are coupled: a good VAD with
  aggressive thresholds *creates* the reliable silence signal that
  endpointing needs.

The state of the art adds a **semantic** layer: feed the running
transcript to a model and ask "does this look like a completed
thought?" — "my name is" → keep waiting even through a long pause;
"my name is Alfredo, over" → done, respond now. This can be a
purpose-built small model (Pipecat's ecosystem has "smart turn"
models for exactly this) or simply a cheap prompt to the LLM you
already run. And note your 2024 instinct was genuinely good:
**"over and out" is a human-driven endpointing protocol** — CB
radio operators invented explicit turn markers precisely because
endpointing over a noisy channel is hard. The 2026 version can keep
it as the fiction-native primary signal, with VAD + semantic
endpointing as the safety net for visitors who don't play along.

So the pipeline shape that falls out:
`mic → neural VAD (aggressive) → buffer speech segments → Whisper →
confidence filter → semantic endpoint check → actors respond`.
Each stage kills one failure mode.

---

## Entry 5 — 2026-09-13: TTS goal agreed; follow-ups.md activated

- **TTS goal** (owner proposal + agent refinement, recorded in
  brainstorm §3): tts-serve is the interface — all six wrapped
  engines reachable by construction; the MVP *deploys* only the
  one or two engines that win the §8.4 comparison experiment
  (deciding criterion: 4 distinct stable character voices via
  cloning). Agent's refinement distinguished API-level support
  (free, comes with tts-serve) from deployment-level support
  (per-engine Docker/VRAM work) — "support all engines" is a
  compatibility property, not a deployment goal.
- **Soft goal**: add F5-TTS and **Breeze TTS 2** (verified real
  2026-09-13: 3B real-time model, code Apache-2.0, weights
  non-commercial — acceptable here) to tts-serve; registered as
  the **first entry in `follow-ups.md`**, activating that file.
- **Terminology flag** (agent): this settles the *TTS* axis;
  the ledger item "LLM/STT choices" — dialogue LLM (model,
  quantization, llama.cpp serving) and STT pick (Whisper size or
  newer open ASR) — remains open.

---

## Entry 6 — 2026-09-13: pushbacks assimilated; Docker-optional ruling; STT decided; LLM narrowed

- **Both agent pushbacks accepted in full**: (1) MVP prepares
  deployment for exactly TWO TTS engines, chosen by experiment
  (brainstorm §3 updated); (2) the TTS/LLM/STT category slip
  acknowledged — LLM & STT handled below.
- **Deployment ruling: Docker preferred, not mandatory**
  (brainstorm §4). Per-engine bare-metal-via-Ansible is a
  sanctioned fallback for quirky engines. Agent pushback,
  accepted into the wording: the "providers may not support
  Docker+GPU" reason is retired (provider-survey criterion S0.1
  guarantees it; only Massed Compute's vGPU caveat remains), and
  a bare-metal engine still requires per-engine venv/conda
  isolation — dependency collision between TTS stacks is the
  disease Docker cures, so escaping Docker doesn't escape
  isolation.
- **STT DECIDED**: Whisper via whisper-fastapi
  (TalkWithMe-native); size is an open config knob for the VRAM
  experiment. Owner confirmed sizes are interchangeable behind
  the same API (correct). 2024 recollection: owner says "small",
  old README says "tiny" — noted, harmless.
- **LLM NARROWED, not settled** (owner's stance: no single
  answer needed to execute; agent agrees with one caveat):
  candidates Gemma 4 small / Qwen 3.5 / Nemotron-if-fits /
  LFM2-class (owner wrote "LMF2" — agent reads this as Liquid
  AI's LFM2 family; flag if wrong). Swappable behind llama.cpp's
  OpenAI-compatible API, so deferral is cheap. Agent's caveat:
  choose a working default before prompt-engineering starts —
  prompts overfit to a model's voice, so "swappable API" does
  not mean "swappable show".
- **TODO Task 2 restructured** into checkbox sub-lists at the
  owner's request (formatting, plus keeps LLM/STT in view).
