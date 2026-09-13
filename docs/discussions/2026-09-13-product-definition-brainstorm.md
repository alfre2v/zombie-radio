# Product definition brainstorm

**Started:** 2026-09-13 · **Arc:** Product definition
**Status:** living while the arc is open. Settled content graduates
to the spec; this doc remains as provenance.

*Purpose: the organized working surface of the Product definition
arc — the current state of everything discussed, arranged as one
rational arc. Written to be **human-readable and self-contained**: a
reader with no other context should understand everything here from
this file alone. (The chronological record of who said what and when
lives in the companion Q&A log, `2026-09-12-product-definition-qa-log.md`;
this doc is the synthesis.)*

## 1. What we are building

Zombie-Radio is a Halloween experience: what sounds like an old
radio drama — four scientists broadcasting from a hidden lab while
a zombie apocalypse unfolds around them (a deliberate throwback to
Orson Welles' 1938 *War of the Worlds* broadcast, the Mercury
Theatre's Halloween episode). The twist: the radio occasionally
*listens*. Listeners discover the characters can hear them and
answer back — ask their name and remember it, ask what day it is,
ask for help locating the lab.

Two identity phrases have crystallized, worth preserving verbatim:

- **"Local AI first, cloud-capable."** Every model that runs at
  show time (dialogue LLM, text-to-speech, speech recognition) is
  open and self-hosted — the project's soul, inherited from 2024.
  But the owner recognizes most people cannot afford a strong-GPU
  PC (the owner's own reference machine: a ~5-year-old 12-core AMD
  Ryzen, 64 GB RAM, Nvidia RTX 3090 with 24 GB VRAM — it runs the
  2024 demo). So this time the backend must deploy *identically* to
  a home Linux box or a rented cloud GPU instance. Big commercial
  LLMs may appear as **offline authoring tools** (see §7) but never
  at show time.
- **"Theatrical live improvisation with LLMs."** The dialogue is
  improvised by models during the broadcast, not scripted — see §7
  for the decision and its planned guard-rails.

Two stagings, decided 2026-09-13:

- **First release (Oct 8 demo)**: the client runs on a simple
  laptop (probably a Mac) at the hackTNT event; the server runs on
  a cloud instance with an Nvidia GPU. Interaction via
  **push-to-talk**.
- **Future vision**: a visually cool unattended booth — the radio
  playing for hours at a party until someone approaches and talks
  to it. Out of scope for the first release, but several challenges
  in §5 exist mainly in this staging, and we keep them documented
  so MVP choices don't paint us into a corner.

Hard deadline: **2026-10-08** (~3 weeks from project start). Every
scope decision below is shaped by that clock; the standing rule is
*MVP first, adventurous things only if time remains*.

## 2. What the 2024 predecessor taught us

A first incarnation was built for a local hackathon in 2024
(<https://github.com/alfre2v/zombie_radio_ai>, discontinued — it
captures the idea; its code quality is deliberately not carried
forward). It was a single-machine Python **CLI monolith**: Whisper
(tiny) for speech recognition, F5-TTS for expressive voices, and a
small local LLM generating the dialogue (the owner recalls Qwen
~9B; the old README says Ollama/Nemotron-mini — owner's
recollection wins as the more recent memory, flagged as
owner-recalled). It required a CUDA card with ≥12 GB VRAM.

Its mechanics, and what they teach:

- **The listening mechanic**: the mic opened only when a character
  asked for interaction and paused ~10 seconds; if sound arrived,
  it kept listening until the user said **"over and out"**.
  Lessons: (a) the fixed listening window is primitive; (b) the
  spoken stop-phrase did not work as well as hoped; (c) *but* the
  half-duplex design accidentally solved the self-hearing problem
  (§5 C4), and "over and out" is a genuinely sound idea — explicit
  turn markers are how real radio operators solved endpointing over
  noisy channels.
- **The dialogue loop**: fully live, one line at a time — the LLM
  was given the preceding dialog lines and asked for the next line
  for a given character. To fight repetitiveness, each request
  injected **entropy terms**: randomly drawn words from
  pre-compiled themed lists (action verbs, adjectives, nature
  concepts/animals, …) that the line had to relate to. A poor-man's
  plot generator. Lesson: small local LLMs left alone "loop like
  crazy" (owner's words); they need externally injected direction —
  a disease the 2026 design must treat more systematically (§7).
- **The architecture**: a monolith couples the show to one physical
  machine with a big GPU. Lesson: the single biggest structural
  change for 2026 is the client/server split (§3).

## 3. Architecture direction

**Client/server split.** One backend owns all the GPU-heavy AI
(LLM, TTS, speech recognition) and exposes its services over an
API (REST and/or WebSockets — one job of the API layer is to
abstract away the peculiarities of individual TTS engines behind a
uniform interface). At least one frontend: a **web app**; possibly
also a simple **CLI client**. The Oct 8 demo laptop only runs the
client — anything with a browser is a candidate stage.

**Chosen foundation (decided 2026-09-13, to be ratified in the
spec): adapt two existing open-source projects** rather than build
from scratch or adopt a big framework. Both are by the same author
(scorbo2), from the local-AI community around the YouTube channel
"No place like localhost". Facts below verified from their GitHub
pages on 2026-09-12:

- **TalkWithMe** (MIT, v7.0 released 2026-09-10, ~209 stars) — "a
  local single-user chat web application that connects to a locally
  running llama.cpp server". Python/FastAPI backend, modular JS
  frontend, talks to any OpenAI-compatible LLM endpoint. Already
  provides: **multi-persona group chats** with configurable routing
  (LLM-decided / random / manual), persona-to-persona replies,
  **streaming TTS playback** (responses chunked by sentence so the
  first audio plays before the rest is synthesized — our main
  latency lever), optional speech recognition via whisper-fastapi,
  voice cloning from reference audio, per-room persistence. This is
  uncomfortably close to "4 AI voice actors talking to each other
  and a listener" already; it becomes the base of our client and
  persona orchestration.
- **tts-serve** (MIT, young: first release Sep 2026, ~17 stars) —
  "a wrapper framework that turns local, open-source TTS engines
  into one consistent REST API with machine-discoverable
  configuration". FastAPI; wraps six engines (Chatterbox, OmniVoice,
  Qwen3-TTS + a faster variant, dots.tts, Index-TTS); every server
  exposes `POST /synthesize` (text, reference audio, seed, …) and
  `GET /capabilities`; responses carry base64 WAV plus timing and
  real-time-factor metrics (useful for our latency experiments).
  It becomes our TTS abstraction layer. **F5-TTS is not among its
  engines** — adding it is a well-scoped potential upstream
  contribution (aspirational; depends on whether F5-TTS still holds
  up against the newer engines, an open question in §8).

Known cost of this choice, accepted with eyes open: both are
**bus-factor-one** projects (one author), and tts-serve is very
young. Trigger to revisit the foundation: TalkWithMe's architecture
proves unadaptable to the radio-show format, or the
single-maintainer model blocks us.

**The road not taken: LiveKit and Pipecat.** These were the
original candidates — mature frameworks offering ready-made
client/server communication, good separation of concerns, and
async execution out of the box; specifically they buy real-time
*conversational* infrastructure: WebRTC transport, voice activity
detection, barge-in, turn-taking. Two reasons they were demoted
(2026-09-13) to at most a comparison footnote: (a) ~3 weeks is not
enough to explore and understand them properly, and (b) a standing
**dependency-skepticism stance** — don't let the project drown in
complexity or marry one framework. The demotion is also technically
defensible: with push-to-talk and rare interaction beats (§5),
plain WebSockets + streaming audio likely suffice; the frameworks'
hard problems (barge-in, continuous turn-taking) are ones the MVP
deliberately avoids having.

## 4. Deployment & operations doctrine

- **Linux-only** server targets — no Windows or other non-Unix OS.
- Model services (TTS engines, LLM server, STT) are **Dockerized**
  for portable deployment; **Ansible** drives deployment
  reproducibly and idempotently.
- The same automation must deploy to a **local strong-GPU Linux
  box** (the owner's 3090 machine) and to a **cloud GPU instance**
  interchangeably — this symmetry IS the "cloud-capable" half of
  the identity.
- The owner has an existing project with this exact deployment
  methodology to crib from. **Ruling (2026-09-13): deferred** — it
  lives in a private repo and this repo is public, so nothing is
  copied wholesale; the owner will surgically extract what
  transfers, at deployment time. Do not ask for it until then.
- **Open research (critical path — the demo runs on it): the cloud
  GPU provider survey.** Which providers give Docker containers
  real access to the Nvidia GPU (the owner recalls RunPod
  historically restricting this — needs verification), whether we
  get a plain SSH-able VM (Ansible-friendly) or only a proprietary
  container abstraction (which would strand much of the existing
  automation), and at what price.
- **Demo-day risk, new with the cloud decision**: the Oct 8 demo
  depends on venue internet reaching the cloud server. Fallback
  thinking owed before the event — e.g. a phone hotspot as backup
  link, and/or a "canned episode" mode: pre-rendered audio the
  client can play if the link dies.

## 5. Challenges for voice recognition & audio processing ⭐

The (future) booth environment is the hard part: an unattended,
always-on microphone at a noisy party, users who don't know the
rules, and loudspeakers blasting the actors' own voices right next
to the mic.

**MVP ruling (2026-09-13): push-to-talk.** The owner considered a
push-to-talk button in 2024 and disliked it — the wow moment is
the radio *just hearing you* — but for the first release
pragmatism wins: push-to-talk gets us to an MVP fast (and can be
themed as an authentic radio transmit control). The "magical"
always-listening pipeline (neural VAD → Whisper → confidence
filter → semantic endpointing; explained in full in
[discussion 2026-09-12] QA log, Entry 4) is a post-MVP adventure,
attempted only if time remains. Push-to-talk changes each
challenge's status for the MVP, noted per item below: it solves
C2, C4 and C5 *by construction* (button release = end of speech;
mic open only while held; pressing the button IS addressing the
radio) and largely defuses C7, while C1 and C6 remain live
concerns even with a button. C8 stands apart: it is an
*output-side* audio problem, listed here for completeness.

Each challenge: what it is → why it bites us → what we know about
solutions → status.

### C1. Noise robustness — Whisper transcribing nonsense

Whisper (our speech-to-text model in 2024) is a generative
sequence-to-sequence model: fed non-speech audio — crowd noise,
music, a cough — it does not output "no speech", it *invents*
plausible text. Worse, it "does not know when to stop" (owner's
observation, matches Whisper's known hallucination behavior).
Approaches: never feed Whisper raw mic audio — gate it behind a
voice-activity detector (see C2) so only probable-speech segments
reach it; additionally filter Whisper's own confidence signals
(its per-segment `no_speech_prob` and average log-probability) to
discard low-confidence transcripts. **Status: still relevant even
with the MVP's push-to-talk — noise arrives while the button is
held (event chatter behind the speaker); confidence filtering is
the cheap must-have for 2026.**

### C2. End-of-speech detection (endpointing)

Deciding *when the user has finished talking* so the actors can
respond. The classic method — "end after N milliseconds of
silence" — failed the owner in another project, and fails in noise
generally: background chatter never reads as silence, and humans
pause mid-sentence, so any fixed N either cuts people off or waits
awkwardly. The 2024 workaround (listen for a fixed 10 s window,
then require the spoken phrase "over and out" to close) was
charming but unreliable. Modern toolbox: neural VAD (e.g.
**Silero VAD** — a tiny CPU-real-time network that outputs a
speech probability per ~30 ms frame, with tunable thresholds and
minimum-duration rules) for far better speech/non-speech decisions
than energy-based silence detectors; on top of it, *semantic*
endpointing — letting the language model judge whether the
transcript so far looks like a completed utterance — is the
emerging fix for the mid-sentence-pause problem. The radio fiction
also permits keeping "over, and out" as an in-world protocol with
smarter detection behind it. **Status: solved by construction in
the MVP — push-to-talk means button release = end of speech. The
smart pipeline above is the post-MVP path and the booth-vision
requirement.**

### C3. Speaker identification (who is talking)

Recognizing *which person* is speaking across turns — e.g. the
actors greeting a returning visitor by name without asking again.
The owner's intuition is right and matches the field: modern
speaker ID computes a fixed-size **speaker embedding** from a short
sample of speech (models like ECAPA-TDNN; text-independent, so no
canonical words needed) and matches it against stored embeddings by
cosine similarity — directly analogous to face-recognition
embeddings for images. **Status: wishlist since 2024; almost
certainly out of scope for 2026 too. Documented so it stays on the
radar.**

### C4. Self-hearing — the actors transcribing themselves *(agent-added)*

The booth loudspeakers play loud synthetic voices centimeters from
an always-on mic: without countermeasures the system hears its own
TTS output, transcribes it, and the actors start responding to
themselves. The 2024 design dodged this *accidentally* — the mic
only opened while the actors were silent (half-duplex). If 2026
keeps any always-listening ambition, we need either the same strict
half-duplex gating (never listen while playing) or acoustic echo
cancellation (AEC — subtracting the known playback signal from the
mic input, as speakerphones do). Half-duplex is vastly simpler and
fits the radio fiction ("over" = channel handover). **Status:
solved-by-accident in 2024, solved by construction in the MVP (mic
open only while the button is held); needs an explicit design only
for the future always-listening booth.**

### C5. Addressee detection — talking *to* the radio vs. talking *near* it *(agent-added)*

At a party booth, most speech the mic hears is people chatting with
each other, not with the radio. Even with perfect noise filtering
(C1), grammatically valid bystander speech would trigger responses
and break the fiction. Options: a wake protocol that lives inside
the fiction (the actors say "if anyone can hear us — respond with
'calling the lab', over"), proximity staging (a visibly placed
vintage-radio mic that people must lean into — directional and
close-range, so bystander speech stays below threshold), or classic
wake-words. The fiction-native protocol doubles as user onboarding:
the characters *teach* visitors how to talk to them. **Status:
solved by construction in the MVP (pressing the button IS
addressing the radio); the fiction-native wake protocol remains
the leading idea for the future booth.**

### C6. Proper-name capture *(agent-added)*

A signature feature is the actors asking a visitor's name and using
it later. Short utterances containing rare proper names are exactly
where speech-to-text is weakest — "Alfredo" may come back as
"Alfred", "a fraido", or worse, and there is no language-model
context to correct it. Practical mitigations are dialog-level, and
happily fiction-friendly: the radio-operator confirmation loop
("say again? … did I copy that right, *Alfredo*? Over.") and
graceful degradation (if confidence stays low, the character uses
"survivor" or a nickname instead of a garbled name). **Status: new
observation; cheap to handle if designed in from the start.**

### C7. Overlapping speakers — several people at once *(agent-added)*

A group approaches the radio together and two people talk over each
other; speech recognition models transcribe mixed speech poorly,
and the actors cannot tell voices apart (see C3). State of the art
(honest assessment, believed): the "cocktail party problem" is
*partially* cracked — neural **source separation** models
(Conv-TasNet / SepFormer lineage) cleanly split 2–3 overlapping
voices on benchmark and near-field audio, and **target-speaker
extraction** can pull out one enrolled voice using the same speaker
embeddings as C3 — but all of it degrades badly on a single distant
mic in real party noise. What actually works in production (smart
speakers) is *hardware*: microphone arrays with beamforming, which
separate speakers spatially before any model runs. Single cheap
mic + open models = still research territory. Practical stance for
us: the fiction absorbs it — a radio operator naturally says "one
at a time, please, over" — and push-to-talk physically enforces one
speaker per transmission if one person holds the control. **Status:
mostly designed away by the MVP's push-to-talk; a real open problem
only for the future booth; no engineering planned.**

### C8. Audio mixing — many sources, one radio stream *(output-side)*

The near-inverse of C7, and unlike C7 it is well-trodden ground: if
sound effects (§6) or background atmosphere ever ship, the app must
mix several audio sources — character voices, effects, static and
dead-air texture (§7) — into the single stream the listener hears.
Digital mixing is fundamentally simple: resample all sources to a
common rate, sum the sample arrays with per-source gain, and avoid
clipping. The constraint: the owner wants most of the app in
Python. Viable options (names + maturity, breadth-first — no deep
dive yet):

- **ffmpeg** (via subprocess or the thin `ffmpeg-python` wrapper),
  `amix`/`adelay` filters — the battle-tested industry workhorse
  for file/offline mixing; rock-solid maturity.
- **pydub** — pleasant high-level Python API (`overlay()`), uses
  ffmpeg underneath; mature and popular; file-oriented, not for
  real-time streams.
- **numpy + soundfile** (with `soxr` for resampling) — mixing is
  just array summation; zero exotic dependencies, fully in our
  control; fine at our scale for offline or chunk-at-a-time work.
- **sounddevice** (PortAudio bindings) + numpy — mature route for
  *real-time* playback mixing in Python if the server ever streams
  a live mix.
- **GStreamer** via PyGObject — industrial real-time multimedia
  pipelines (`audiomixer` element); very mature but a heavyweight
  learning curve; only if we outgrow everything above.
- **Web Audio API** (not Python — the browser): if the client is a
  web app, the *client* can mix natively — per-source gain nodes,
  ducking effects under voices — keeping the server simpler.
  **Owner pushback (2026-09-13)**: streaming N parallel audio
  streams to the client is wasteful — it forces on-the-fly
  compression server-side and decompression client-side. Agreed
  for the naive version. The refined version that survives the
  pushback: only the *voice* track streams; sound effects and
  ambience are mostly **static assets shipped once** at page load
  and triggered client-side by tiny control events ("play static
  loop", "duck under voice") — near-zero extra bandwidth, and the
  browser decodes compressed audio natively (no decoder to write).
  Note we will likely compress the voice stream anyway (Opus via
  ffmpeg is cheap next to TTS cost) — raw WAV over venue internet
  is the truly wasteful option. Server-side mixing remains the
  simpler-to-sync alternative. Decision deferred until §6
  activates.

**Status: not an MVP need; becomes relevant the moment
sound-effects (§6) or dead-air texture (§7) ship; low technical
risk — the work is choosing where mixing lives (server vs.
client), not how.**

### C9. Audio compression for the voice stream *(output-side)*

Not a hard technical challenge, but a mandatory pipeline stage that
was off the radar until 2026-09-13: the server-to-client voice
stream should never travel as raw audio. Raw PCM at 24 kHz /
16-bit mono (typical TTS output) is ~384 kbps *per stream*; over
uncertain venue internet (§4's demo-day risk) that is the truly
wasteful design. The tool of choice is **Opus**: a *lossy*, open,
royalty-free codec (RFC 6716) — not to be confused with FLAC, the
well-known open *lossless* codec, which only shrinks audio ~50%
and is the wrong tool for streaming speech. Opus was designed for
low-latency interactive voice (it is *the* codec inside WebRTC,
Discord, Zoom): speech is excellent at **24–32 kbps** mono
(~12–16× smaller than raw), and even music-grade quality sits at
64–128 kbps. Frame sizes go down to 2.5–60 ms, so it adds
essentially no latency to a streaming pipeline.

The envisioned pipeline: each TTS engine produces WAV/PCM
server-side (tts-serve returns base64 WAV); the server encodes on
the fly to Opus — via ffmpeg or a Python binding — as part of the
same sentence-chunked streaming that TalkWithMe already does for
fast first audio; chunks travel over the WebSocket (framed in an
Ogg/WebM container) or plain HTTP streaming. Encoding cost is a
rounding error next to the TTS inference that produced the audio.
On the client, **decoding is free**: browsers natively decode Opus
(`<audio>` elements, `decodeAudioData`, Media Source Extensions) —
hardware-supported, nothing for us to write. **Status: must-have
for the v1 voice stream; low risk; the only real decision is the
container/transport framing, which falls out of the client
architecture choice (§8).**

## 6. Beyond recognition: sound-effects generation (feature target)

There are open models specialized in generating *sound effects*
from text descriptions ("footsteps of a woman in high heels on a
wood floor") rather than voices. For a radio drama this is
atmosphere gold: doors, zombies pounding, static, lab equipment.
Candidate models to verify when the time comes (leads, believed —
not yet checked): **AudioGen** (Meta, part of AudioCraft),
**AudioLDM 2**, **Stable Audio Open** (Stability AI, open weights).
Likely out of scope for the Oct 8 MVP; pre-generating a small
library of effects offline (rather than live generation) would be
the cheap version. **Status: identified feature target, parked;
revisit after the MVP ships or if the schedule opens up.**

## 7. Dialogue generation: the live ↔ authored spectrum

The question: who writes the play? The poles:

- **Fully authored**: the play is written by humans in advance
  (possibly with branches); models only *perform* it (TTS). Maximum
  writing control and reliability; zero adaptivity — the radio
  cannot answer a question it wasn't scripted for.
- **Fully live**: a language model improvises every line during the
  broadcast, given the story-so-far. Maximum adaptivity and
  surprise; risks incoherence, latency, and demo-day failure modes.
- **Hybrid**: an authored narrative spine (episode outlines, key
  beats, character bibles) with live-generated lines inside it —
  or authored narration segments alternating with live interactive
  beats.

The choice decides how the three weeks are spent (writing vs.
engineering) and sets the latency and VRAM budgets for the backend:
a live pipeline needs the LLM and TTS resident and fast
*simultaneously* on one GPU (on the reference 24 GB card: LLM +
4 TTS voices + STT sharing VRAM — an unmeasured budget, see §8),
while an authored one barely needs the LLM at show time. The 2024
baseline was fully live (§2's dialogue loop). One boundary is
fixed regardless: the interactive beats (answering a visitor,
using their name) *must* be live — that is the product's soul.

**Decision (owner, 2026-09-13): live-first.** The MVP aims at
**"theatrical live improvisation with LLMs"**: the three weeks go
to engineering, not storyline writing, like 2024. The hybrid layer
comes **post-MVP**: the owner's idea is to collect stories offline
from bigger commercial LLMs and use them *not literally* but as
**trajectory scaffolds** — guide-rails that keep small local LLMs
on a story arc, because left alone "they tend to loop like crazy"
(the 2024 entropy-terms trick attacked the same disease at line
granularity; trajectory scaffolds attack it at plot granularity).
Note this preserves local-AI-first: commercial LLMs would be
offline authoring tools only; nothing commercial runs at show
time. **Trigger to revisit: the MVP's live narration proves too
incoherent to demo.**

**Filling the hours (loop shape, idea stage).** An unattended radio
(and even a long demo) needs texture between story beats. A cheap,
atmospheric, and engineering-friendly idea: in-fiction *dead air* —
static, emergency-broadcast tones, "signal lost… reconnecting"
interludes between generated segments. It buys the pipeline
breathing room (time to generate/synthesize the next segment) while
*strengthening* the fiction instead of breaking it. Not yet
discussed in depth; the 2026 session/loop length target is still
open (§8).

## 8. Open questions ledger

The consolidated feed for the remaining survey/spec work (Task 2)
and candidate experiments (Task 3):

1. **Cloud GPU provider survey** (critical path, §4): GPU-in-Docker
   support, SSH-able VMs vs. container abstractions, pricing.
2. **LLM choice** for dialogue: which small local model, at what
   quantization, served how (llama.cpp per TalkWithMe's default?).
3. **STT choice**: which Whisper size/variant (2024 used tiny), or
   a newer open ASR model; plus the C1 confidence-filter design.
4. **F5-TTS vs. the newer engines** wrapped by tts-serve
   (Chatterbox, OmniVoice, Qwen3-TTS, dots.tts, Index-TTS):
   quality, latency, voice-cloning fidelity for 4 distinct
   characters. Candidate first experiment — tts-serve's
   real-time-factor metrics help here.
5. **VRAM/latency budget** on a 24 GB card: LLM + 4 TTS voices +
   STT resident together — measure, don't guess. Candidate
   experiment.
6. **Session/loop shape**: target episode length, dead-air texture
   (§7), what a whole-evening run looks like post-MVP.
7. **Client form**: browser page vs. simple native/CLI client for
   the demo laptop; and whether a CLI client ships at all in v1.
8. **Demo-day network fallback** (§4): hotspot? canned episode
   mode?

## 9. The foundation debate: TalkWithMe-and-friends vs. Pipecat (2026-09-13)

*Context: after the framework survey
(`2026-09-13-audio-framework-survey.md`) crowned Pipecat "the one
to pick if forced to pick a framework," the owner ordered a
rhetorical debate exercise: (1) hold the position
"TalkWithMe-and-friends over Pipecat" with 5 strong technical
arguments and a one-sentence punchline; (2) hold the opposite
position with 3 strong arguments and a punchline; (3) then
reconcile honestly — would the agent still recommend
TalkWithMe-and-friends? The agent's answer is preserved verbatim
below. (Postscript: the owner later revealed the 5-vs-3 argument
asymmetry was a deliberate framing trick; the agent's honest
audit: the asymmetry went unnoticed during the exercise, but the
stronger anchor was incumbency — the decision already lived in
the QA log — while the reconciliation's decisive facts, latency
asymmetry and getUserMedia-AEC, are count-independent. The
resulting spike-with-flip-trigger is itself the anti-anchor
mechanism.)*

---

### Position 1: TalkWithMe-and-friends, and I'll hear no more of this framework talk

**1. The hard 20% of our app already exists in TalkWithMe and
does not exist in Pipecat.** Strip everything away and
Zombie-Radio's irreducible core is an *ensemble engine*: multiple
personas with distinct voices taking turns, replying to each
other, routed by an LLM or a director. TalkWithMe ships that
today — multi-persona group chats, LLM-decided/random/manual
routing, persona-to-persona replies, per-persona voices with
cloning. Pipecat ships a one-bot-one-human loop, and its own
example gallery contains no ensemble. Adopting Pipecat means
adopting a framework *in order to rebuild the one feature our
current base already has*. That's backwards.

**2. Our traffic shape makes Pipecat's crown jewels worthless to
us.** Pipecat's engineering value is concentrated in the
low-latency full-duplex loop: VAD, barge-in, sub-second
turn-taking, interruption-safe frame discarding. Now look at our
MVP's actual traffic: a *one-directional broadcast* where seconds
of latency between actor lines is not just tolerable but
fictionally exploitable (static, "signal lost…"), and an inbound
path that is **push-to-talk** — which, per our own brainstorm §5,
solves endpointing, self-hearing, and addressee detection *by
construction*. We would be importing 15k stars' worth of
machinery whose primary benefits our design already eliminated by
pressing a button. The only latency tech we genuinely need —
sentence-chunked streaming TTS — TalkWithMe already has.

**3. Inversion of control is the wrong trade for a solo
three-week build.** Pipecat is a framework: our show logic would
live *inside* its FrameProcessors, scheduled by its runner,
debugged through its frame semantics (bidirectional flows,
system-vs-data frame priority, interruption discard rules).
TalkWithMe is an app: plain FastAPI + asyncio that a senior
engineer reads top to bottom in an afternoon and then *owns*. At
2 a.m. on October 7th, debugging your own 2,000 lines beats
debugging a framework's task scheduler through a stack of
abstractions you adopted three weeks ago.

**4. The learning-budget arithmetic is brutal and it's not
close.** The scarce resource is not lines of code, it's
owner-hours — and by our own working method, the owner must
*understand* every architectural layer, not just run it.
TalkWithMe's stack (FastAPI, JS, REST) is already understood;
Pipecat demands a new mental model *plus* ongoing churn tax (1.0
landed only in April 2026; breaking changes still appear in minor
releases; pin and migrate forever). Three weeks buys
understanding a small app *and* building the show, or
understanding a framework *instead of* building the show.

**5. The integration seams are already aligned — and Pipecat's
jewels are stealable without the crown.** TalkWithMe natively
speaks OpenAI-compatible LLM (llama.cpp: check), whisper-fastapi
STT (check), and HTTP TTS with voice cloning (tts-serve is one
thin adapter away). Meanwhile the two Pipecat components we'd
actually covet — Silero VAD and the smart-turn model — are
**standalone, BSD-2 imports**. We can graft the crown jewels onto
our stack without swallowing the tree they grew on.

> **Punchline:** *We're building a theater, not a call center —
> TalkWithMe hands us a stage with four actors already on it,
> while Pipecat hands us the world's finest telephone.*

### Position 2: Pipecat, and the chat app will betray you

**1. Your demo path is the open internet, and TalkWithMe has
never left the house.** The word is in its own README: a
**local** single-user chat app. Our MVP's actual topology is a
cloud GPU server streaming audio across venue Wi-Fi to a laptop —
jitter, packet loss, buffering, reconnects. Pipecat's
SmallWebRTCTransport gives broadcast-grade delivery out of the
box: Opus, jitter buffers, loss concealment, browser AEC,
reconnection — vendor-free. On TalkWithMe you will discover,
mid-hackathon, exactly which localhost assumptions run deepest,
and you'll end up reimplementing WebRTC's worst chapters by hand,
badly, the week of the demo.

**2. You're doubling down on bus-factor one, twice.** The MVP
plan stakes the demo on *two* single-maintainer projects (209 and
17 stars) — one of which released v7.0 two days before we found
it, with no migration guides, no contributor bench, and no
accountability for what v8 breaks. Pipecat has Daily's paid
maintainers, ~15.5k stars, hundreds of contributors' worth of
already-fixed async-audio edge cases, and NVIDIA building its ACE
product line on top. When you hit the inevitable subtle streaming
bug, one of these ecosystems has seen it before. The other one is
a guy with a YouTube channel.

**3. Every item on your post-MVP roadmap is native Pipecat
territory, and your fork will rot.** Always-listening (Silero +
smart-turn: integrated), background SFX and dead-air texture
(`SoundfileMixer`: exists), multi-listener scale (swap in the
LiveKit transport: supported), barge-in (core competency). On the
TalkWithMe path each of these is a hand-bolted addition to a chat
UI progressively contorted into a radio station — the classic
sunk-cost architecture, ripening toward a full rewrite at exactly
the moment you'll have an audience and momentum. And don't
romanticize the ensemble head start: TalkWithMe's persona routing
is *text-chat-turn* logic — you'll rewrite it for continuous
audio broadcast anyway, so write it once, on primitives built for
audio.

> **Punchline:** *TalkWithMe saves you the first week; Pipecat
> saves you every week after — and the internet between your GPU
> and the venue doesn't care how charming your personas are.*

### Position 3: the honest reconciliation

Both advocates scored real hits. Let me now weigh the exchange
without a client to represent.

**Where Position 2 genuinely wounded Position 1.** The WAN
argument is the strongest thing the Pipecat side said. TalkWithMe
*is* localhost-born, our topology *is* cloud-to-venue, and this
is an untested assumption sitting under the whole MVP plan — the
single biggest unknown in the TalkWithMe path. The
bus-factor-squared point is also real, as is the observation that
the multi-persona routing is chat-shaped, not broadcast-shaped:
our head start is smaller than it looks.

**Where Position 1's case survives scrutiny — on facts, not
vibes.** Three load-bearing observations:

1. **The latency-tolerance asymmetry is decisive for the MVP.**
   Pipecat's engineering is built for conversation (<1 s or the
   illusion dies). Radio drama tolerates — even *wants* — seconds
   of buffer, and PTT input has no realtime constraint at all
   (record fully, then upload). Ordinary web audio streaming with
   a generous client buffer handles jittery Wi-Fi *better* than
   low-latency WebRTC does, because it's allowed to buffer.
   Position 2's transport argument, examined closely, mostly
   evaporates for a broadcast: WebRTC optimizes the thing we
   don't need (latency) at the cost of the thing we do
   (simplicity).
2. **The AEC point is a red herring, and this took me a moment.**
   Browser echo cancellation is a `getUserMedia` audio constraint
   (`echoCancellation: true`) — it comes from the browser's media
   stack, **not** from using WebRTC transport. Our plain web
   client gets it too. Position 2 was quietly bundling a free
   good into its product.
3. **The dependency risks have different shapes, and one is
   milder.** TalkWithMe is a *starting codebase we absorb*: we
   fork, we own, upstream can vanish tomorrow and nothing breaks.
   Pipecat is a *dependency we must track*: breaking minors,
   migrations, upstream decisions forever. For a project whose
   owner wants to understand every layer, "inherit and own small
   code" fits the working method; "track a large framework"
   fights it.

**So: would I honestly still recommend TalkWithMe-and-friends?**

**Yes — but I'm converting the recommendation from a belief into
a bet with an exit clause.** The reasoning: the MVP's hard
problem is the *ensemble director*, where TalkWithMe is closer;
the MVP's traffic shape neutralizes Pipecat's core value; the
learning budget is real; and the jewels (smart-turn, Silero) are
stealable regardless. But Position 2 identified a genuine unknown
that must not remain one:

- **The bet must be validated by a timeboxed spike** — our first
  `experiments/` folder, per protocol with abort criteria written
  first: clone TalkWithMe, deploy backend on a remote box, client
  on a laptop over real internet, wire llama.cpp + one tts-serve
  engine, run a 4-persona session. Budget: ~2 days. It answers
  the only question the survey couldn't: *how deep do the
  localhost assumptions go?*
- **Named flip trigger:** if the spike reveals structural
  localhost coupling (audio delivery unusable over WAN, blocking
  architecture) or code we can't responsibly own, we flip to
  Pipecat immediately — losing days, not weeks, and with the
  survey already done.
- **One honest confession for the record:** this recommendation
  is *for the 3-week MVP*. For the post-MVP always-listening
  booth, the calculus genuinely shifts toward Pipecat's
  primitives, and partial adoption (smart-turn first) is more
  likely than not. Position 2 doesn't lose the war; it loses this
  battle on the clock.

Two process notes: this decision now smells strongly like
**ADR-0001** ("Build the MVP on TalkWithMe + tts-serve over
voice-agent frameworks") — per our rules I'm asking before
drafting: shall I? And this debate deserves persistence (QA log
entry, or appended to the survey as an adjudication addendum) —
say the word and where, and whether the spike experiment should
be the next thing we scope.

*[Outcome, 2026-09-13: the owner confirmed the TalkWithMe path
("we really do not have the time for Pipecat"), ordered this
debate persisted here, the spike documented as a Task 3 sub-task
in TODO.md, and ADR-0001 drafted.]*
