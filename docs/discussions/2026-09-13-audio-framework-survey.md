# Audio framework landscape survey: LiveKit · Pipecat · Dograh

**Date:** 2026-09-13 · **Arc:** Product definition (Task 2)
**Type:** survey (candidate tools compared and adjudicated)
**Method:** three parallel research agents, one per framework; all
claims verified online 2026-09-13 with sources linked inline.
Anything the research could not confirm is labeled *uncertain*.
**Trigger to revisit:** the post-MVP arc that adds always-listening
or multi-listener capability; or any of these projects shipping a
first-party multi-character/ensemble example.

*Context for the cold reader: Zombie-Radio (see
`2026-09-13-product-definition-brainstorm.md`) is an audio-only
radio drama improvised live by 4 AI voice actors on self-hosted
open models, with occasional listener talk-back via push-to-talk.
The MVP (deadline 2026-10-08) is already decided to build on
TalkWithMe + tts-serve; this survey maps the adjacent framework
landscape — as due diligence on that decision, and as the menu for
post-MVP building blocks.*

---

## S1. General findings, sources, and first feelings

**The headline discovery: these are not three parallel options —
they are three layers of one family tree.** LiveKit's core is
transport infrastructure (a WebRTC media server). Pipecat is a
pipeline *orchestration* framework that can ride on LiveKit (or
other transports). Dograh is a *product* built on a **fork of
Pipecat**. So the real decision space is "which layer do you enter
at," not "which of three rivals do you pick." Dograh's founders
choosing Pipecat as their foundation is itself a data point in
Pipecat's favor.

**Second finding: all three share the same blind spot for us.**
Every one models a session as *one human ↔ one assistant*. None
ships an example of several autonomous characters performing
together for an audience. Our 4-actor ensemble is a novel
composition in every framework — which independently validates the
MVP decision to adapt TalkWithMe (which *does* have multi-persona
group chats) instead.

**Third finding: the open-source/self-hosting story is real in all
three** (Apache-2.0 / BSD-2 licenses, documented vendor-free
paths), but each has a commercial gravity well — LiveKit Cloud,
Pipecat Cloud (Daily), Dograh's hosted app — and the premium
"batteries" (best noise cancellation, best turn-detection model)
are where the cloud pull concentrates.

Quick feelings:

- **LiveKit** — industrial WebRTC infrastructure with an agents
  framework on top. Adopting it feels like adopting a small
  datacenter: immensely capable, real ops weight.
- **Pipecat** — a Python-native asyncio pipeline kit; feels like a
  library, not a platform. The open voice-AI community's center of
  gravity (NVIDIA built its ACE voice microservice on it).
- **Dograh** — a polished call-center product wearing open-source
  clothes. Impressive execution, one year old, selling a different
  movie than ours.

Primary sources (full links inline in S2): the three GitHub repos,
docs.livekit.io, docs.pipecat.ai, docs.dograh.com, pricing pages
(livekit.com/pricing, daily.co/pricing/pipecat-cloud), the
[Dograh Show HN](https://news.ycombinator.com/item?id=46189836),
Hugging Face model licenses, and funding announcements.

---

## S2. Per-framework findings

### S2.1 LiveKit

Sources: [livekit/livekit](https://github.com/livekit/livekit) ·
[livekit/agents](https://github.com/livekit/agents) ·
[docs.livekit.io](https://docs.livekit.io/agents/) ·
[pricing](https://livekit.com/pricing) ·
[turn-detector license](https://huggingface.co/livekit/turn-detector/blob/main/LICENSE)

**Q1 — What is it? Fit?** Three layers under one brand: (a) the
open-source **LiveKit Server**, a distributed WebRTC SFU in Go
(Apache-2.0, ~20.9k stars) that routes realtime audio/video
between people, devices, and AI; (b) client SDKs (JS, mobile,
Unity…) that handle mic capture, Opus, playback, reconnection;
(c) **LiveKit Agents** (~14.2k stars, Python-first), a framework
where an agent joins a room as a participant and runs
STT→LLM→TTS. LiveKit-the-company sells LiveKit Cloud (managed
hosting + extras); OpenAI's ChatGPT voice mode is a flagship
customer. **Fit: plausible but oversized for the MVP; genuinely
interesting later.** It solves wholesale the exact problem we
deferred (browser listener ↔ server AI, echo-managed, with manual
turn control that maps directly to push-to-talk), but its
AgentSession is one-user-one-assistant shaped, and production
self-hosting means domain + SSL, Redis, TURN, a big UDP port
range, and a separate Egress service — real ops burden for a
3-week solo build.

**Q2 — Core abstractions:** Room (the virtual space) ·
Participant (humans, agents, services alike) · Track/publication
(media streams, selectively subscribed) · data channels · JWT
access tokens · agent worker → job (subprocess that joins a room)
· **AgentSession** (wires VAD + STT + LLM + TTS + turn detection
for one conversation, with Agent handoffs) · overridable
`stt_node`/`llm_node`/`tts_node` hooks · Egress/Ingress
(server-side compositing/recording/streaming).

**Q3 — Advantages / disadvantages:**
*Advantages:* (1) listener talk-back solved wholesale — WebRTC +
Opus + browser AEC + push-to-talk semantics
(`interrupt()`/`commit_user_turn()`) pre-built; (2) local models
genuinely supported — OpenAI-compatible `base_url` (llama.cpp
qualifies), Ollama helper, node overrides for arbitrary REST like
tts-serve; (3) the correct scale path if the show ever has
hundreds of concurrent listeners (SFU + Egress→HLS broadcast);
(4) very active, Python-first.
*Disadvantages:* (1) wrong center of gravity — "multi-agent"
means sequential handoffs, not four simultaneous voices; 4 agent
participants would fight turn-taking machinery designed for
humans; (2) heaviest ops footprint of the three; (3) API churn —
a breaking 0.x→1.0 rewrite (April 2025) plus ~weekly minors; (4)
premium audio features are cloud-gated (Krisp noise cancellation,
full turn-detector model).

**Q4 — Lock-in risk: LOW–MEDIUM** (low for transport, medium for
the agents batteries). SFU + framework fully Apache-2.0 and
self-hostable; air-gapped operation plausible (models
pre-fetchable at Docker build). But: the **turn-detector model
weights are under a proprietary "LiveKit Model License"** —
usable only inside LiveKit Agents, a deliberate lock-in point —
and Krisp/Inference/observability live in the cloud. Company is
heavily VC-funded (Series B $45M @ $345M, Apr 2025; Series C
~$100M @ ~$1B, Jan 2026), so expect sustained cloud monetization
pull.

**Q5 — Challenge coverage** (our C-numbers from the brainstorm
doc's §5):

- **C1 noise robustness — partial.** Browser-side
  `noiseSuppression` comes free with the client SDKs.
  Best-in-class cancellation (Krisp NC/BVC) is **cloud-only**; a
  third-party open-source DTLN plugin exists (Aloware) for
  self-hosters.
- **C2 endpointing — yes, with a license catch.** Silero VAD via
  `livekit-plugins-silero` (local, free), plus a semantic
  turn-detector model on top. The full `v1` model runs only on
  LiveKit's cloud inference; the local `v1-mini` is free to run
  but its weights are license-restricted to use *inside LiveKit
  Agents only*.
- **C3 speaker identification — partial, outsourced.** Real-time
  diarization only via cloud STT providers (Speechmatics plugin);
  no local diarizer.
- **C4 self-hearing / echo — yes.** WebRTC-native
  `echoCancellation` in the client SDKs: the browser cancels show
  audio leaking into the listener's mic, no work on our side.
- **C7 overlapping speakers — partial.** `MultiSpeakerAdapter`
  picks a primary speaker by loudness and can suppress background
  speakers; no true separation of simultaneous speech.
- **C8 audio mixing — yes, twice over.** Every client natively
  mixes all subscribed tracks on playback (notably: our
  "client-side mixing" C8 idea, already productized), and
  Room-Composite Egress can mix the whole room server-side into
  one file/stream.
- **C9 Opus + streaming transport — core competency.** WebRTC/
  Opus end-to-end with jitter buffers, simulcast, selective
  subscription; RTMP/HLS broadcast via Egress.

**B1 abstraction half-life:** one breaking rewrite in ~2.5 years
+ weekly minors → expect migration work if we return to code
months later. **B2 demo-to-app distance:** far — flagship demos
are telephony assistants, kiosks, call centers; an ensemble show
is a novel composition. **B3 exit cost:** transport layer exits
cleanly (SFU is framework-independent); AgentSession
orchestration and turn-detector config die with it; local
services survive if kept behind our own REST.

### S2.2 Pipecat

Sources: [pipecat-ai/pipecat](https://github.com/pipecat-ai/pipecat) ·
[docs.pipecat.ai](https://docs.pipecat.ai/guides/learn/pipeline) ·
[smart-turn](https://github.com/pipecat-ai/smart-turn) ·
[SmallWebRTC](https://docs.pipecat.ai/api-reference/server/services/transport/small-webrtc) ·
[Pipecat Cloud pricing](https://www.daily.co/pricing/pipecat-cloud/) ·
[1.0 migration guide](https://docs.pipecat.ai/pipecat/migration/migration-1.0)

**Q1 — What is it? Fit?** A Python **realtime pipeline
orchestration framework** for voice AI (BSD-2, ~15.5k stars),
created and maintained by Daily.co: it wires streaming audio →
VAD → STT → LLM → TTS → audio out into a low-latency,
interruptible loop. Its own README lists **"interactive
storytelling"** as a target application. NVIDIA built its ACE
Controller microservice on it (`nvidia-pipecat` on PyPI). **Fit:
the best conceptual match of the three** — Python-first, runs
fully local (local Whisper, llama.cpp via `base_url`, self-hosted
HTTP TTS — the Piper HTTP service is nearly a template for
wrapping tts-serve), lightest ops of the three. Same caveat as
everywhere: its canonical shape is one bot ↔ one human; the
4-actor ensemble would be custom orchestration from its
primitives (`ParallelPipeline`, multiple TTS service instances, a
custom mixer) — parts exist, no ensemble example does.

**Q2 — Core abstractions:** **Frames** (typed data flowing
bidirectionally: audio, transcriptions, LLM text, control) ·
**FrameProcessor** (the building block; own task, ordered
delivery) · **Pipeline** / `ParallelPipeline` (processor chains;
canonical order: transport.input → stt → user-context → llm → tts
→ transport.output) · **Transports** (the I/O edge: Daily,
LiveKit, vendor-free `SmallWebRTCTransport`, FastAPI WebSocket,
telephony serializers) · **Services** (pluggable STT/TTS/LLM
classes, swappable ~one line) · PipelineTask/Runner (execution).

**Q3 — Advantages / disadvantages:**
*Advantages:* (1) the hard realtime plumbing — interruption,
streaming hand-offs, VAD, resampling — is solved, exactly what a
solo 3-week build can't reinvent; (2) local-first is a supported
path, not a hack (Pipecat-maintained local Whisper, Ollama,
`base_url` overrides, self-hosted HTTP TTS); (3) vendor-free
browser transport: `SmallWebRTCTransport` = P2P WebRTC via
aiortc, zero external infrastructure, browser AEC + Opus for
free; (4) BSD-2, huge community, NVIDIA endorsement.
*Disadvantages:* (1) 1:1 assistant shape — ensemble drama means
custom work (the official storytelling example is single-narrator
and cloud-service-based); (2) large abstraction stack to learn +
real API churn (~2 years of breaking 0.0.x; 1.0 April 2026 with a
formal migration guide; minors every 2–4 weeks still flagging
breaking changes); (3) flagship integrations optimize for cloud
providers — local combos are supported but less traveled (e.g.
local Whisper is segmented, not streaming — fine for
push-to-talk); (4) small trap: the in-process `piper-tts` extra
is GPL-3.0 — use the HTTP variant.

**Q4 — Lock-in risk: LOW** (leaning low of low–medium). BSD-2
framework; Daily sells Pipecat Cloud (hosted agent runtime, from
$0.01/agent-minute) and its WebRTC platform, classic open-core —
but the framework runs with zero Daily involvement
(SmallWebRTC/WebSocket transports; community-documented fully
self-hosted deployments). The smart-turn model is BSD-2 **and
standalone-usable** — the philosophical opposite of LiveKit's
model license. Daily: $40M Series B (2021), ~$70M total.

**Q5 — Challenge coverage** (our C-numbers from the brainstorm
doc's §5):

- **C1 noise robustness — partial, honest open options.** Input
  audio filters ship in-tree: **RNNoise** and **noisereduce**
  (open, local) plus commercial Koala/Krisp filters. Open options
  are real but not best-in-class.
- **C2 endpointing — best-in-class open, the crown jewel.**
  `SileroVADAnalyzer` built in, and **Smart Turn**: an open
  (BSD-2) semantic turn-detection model — ~8M params,
  Whisper-Tiny backbone, 23 languages, ~10 ms CPU inference, runs
  fully local (`LocalSmartTurnAnalyzerV3`). Crucially it is
  **importable standalone, without Pipecat** — usable in our
  TalkWithMe-based stack directly.
- **C3 speaker identification — cloud-only.** Diarization only
  through cloud STT services (e.g. Deepgram's `diarize` flag);
  no local component.
- **C4 self-hearing / echo — delegated to the transport.** WebRTC
  transports (SmallWebRTC, Daily, LiveKit) inherit browser AEC;
  the plain WebSocket transport gets **none** — choose transport
  accordingly.
- **C7 overlapping speakers — no.** Bot barge-in/interruption is
  handled; separating simultaneous humans is not.
- **C8 audio mixing — basic, extensible.** `SoundfileMixer` mixes
  file audio (background loops, SFX, runtime volume control) into
  the output — enough for our dead-air texture idea. Mixing four
  *live* TTS streams into one broadcast means writing a custom
  `BaseAudioMixer` — supported extension point, real work.
- **C9 Opus + streaming transport — yes via WebRTC.** Its WebRTC
  transports negotiate Opus natively (up to 48 kHz); WebSocket
  paths carry raw PCM or telephony codecs through pluggable
  serializers, with auto-resampling utilities.

**B1 abstraction half-life:** short historically (0.0.x era),
improving post-1.0 (April 2026) but minors still break — pin
versions. **B2 demo-to-app distance:** medium — examples skew
call-center/telephony, but "storytelling" is at least in the
README and the primitives (parallel pipelines, mixers, multiple
service instances) map to our needs. **B3 exit cost:** low-ish
*if disciplined* — keep show logic out of FrameProcessors and
services behind our own REST (llama.cpp, tts-serve), and what
dies with Pipecat is wiring, not soul. Smart-turn survives any
exit (standalone BSD-2).

### S2.3 Dograh

Sources: [dograh-hq/dograh](https://github.com/dograh-hq/dograh) ·
[docs.dograh.com](https://docs.dograh.com/core-concepts/how-dograh-works.md) ·
[Show HN, Dec 2025](https://news.ycombinator.com/item?id=46189836) ·
[interruption/audio docs](https://docs.dograh.com/configurations/interruption.md)

**Q1 — What is it? Fit?** A ~1-year-old (repo created 2025-09)
open-source, self-hostable **voice-AI agent platform** — "the
self-hosted alternative to Vapi and Retell": visual workflow
builder (ReactFlow), campaigns, call transfer, post-call QA,
8+ telephony providers, Python backend + React UI + Postgres +
MinIO via Docker Compose. Built by YC-alumni founders (Zansat
Technologies; funding undisclosed) who left Vapi over platform
fees eating 60–70% of spend. **The owner's hypothesis
("telephony agentic thing, not storytelling") is CONFIRMED**: the
core loop is caller→STT→LLM→TTS→caller until an end-node
terminates *the call*; the audio pipeline is **hard-capped at
8/16 kHz** (telephone-grade); no multi-voice, no multi-character,
no live mixing, nothing storytelling-adjacent anywhere in docs or
marketing. Fairness nuance: it isn't telephony-*only* (browser
test audio + embeddable web widget exist), but everything above
the transport optimizes for one-agent business calls. **Fit:
poor.** Its product layer is dead weight for us and its session
model actively fights the ensemble format. *(One ironic footnote:
a zombie-apocalypse broadcast at 8 kHz would sound
atmospherically like a distressed shortwave transmission — but an
unliftable fidelity ceiling is the wrong constraint to inherit
for a show whose product IS audio.)*

**Q2 — Core abstractions:** Workflow (graph of nodes/edges) ·
node types (Start/Agent/Global/End, Tools incl. MCP, Knowledge
Base, Pre-recorded Audio, QA) · Runs/Calls (transcript,
recording, variables, cost) · Campaigns · provider configs
(speech-to-speech / managed / BYOK). **Crucially: built on a
forked Pipecat** (git submodule; founders confirm custom event
model + concurrency fixes) — so it inherits Pipecat's engine and
adds a call-center superstructure; fork drift from upstream is an
unquantified risk.

**Q3 — Advantages / disadvantages:**
*Advantages:* (1) genuinely self-hostable and local-AI-first
friendly (one Docker Compose; OpenAI-compatible LLM endpoints;
Speaches for local Whisper/TTS); (2) interruption/barge-in solved
out of the box (Silero VAD, per-node toggles; ~500–600 ms
reported end-to-end latency); (3) excellent iteration UX (visual
editing, browser testing, tracing) *for the app shape it serves*.
*Disadvantages:* (1) wrong session model — one agent voice per
call, no ensemble path without hacking their Pipecat fork (at
which point: use Pipecat); (2) telephone-grade 8/16 kHz audio
ceiling; (3) youth — docs thin on internals (audio formats, noise
handling undocumented), community small (Show HN: 16 points),
commit concentration extreme (top 2 of 60 contributors ≈ 700 of
800 commits), heavy unused surface (Postgres, MinIO, campaigns).

**Q4 — Lock-in risk: LOW** for the software (BSD-2 verified;
hosted offering exists but self-hosting is the headline; BYOK
everywhere). The real risk is **company viability**, not lock-in:
young startup, undisclosed funding — but BSD-2 + a Pipecat
foundation means abandonment ≠ entrapment. Telemetry defaults
unverified.

**Q5 — Challenge coverage** (our C-numbers from the brainstorm
doc's §5 — the sparseness of this list is itself a finding about
the docs):

- **C1 noise robustness — nothing documented.** No mention of
  noise handling anywhere in the docs.
- **C2 endpointing — basic.** Silero VAD detects start/end of
  user speech, with per-node interruption toggles. No semantic
  turn model surfaced (whether Pipecat's smart-turn is exposed
  through the fork is *uncertain* — not mentioned).
- **C3 speaker identification — no.** Nothing found.
- **C4 self-hearing / echo — undocumented.** Browser paths
  presumably inherit browser AEC, but Dograh claims nothing.
- **C7 overlapping speakers — no.** Nothing found.
- **C8 audio mixing — no.** "Pre-recorded Audio" hybrid playback
  exists (recorded clips + TTS in one flow), but no live
  multi-source mixing.
- **C9 Opus + streaming transport — no Opus mention.** The Agent
  Stream is a WebSocket with Twilio-compatible framing (telephony
  codec territory, μ-law/PCM); codecs unspecified in docs, and
  the pipeline's 8/16 kHz cap bounds quality regardless.

**B1 abstraction half-life:** short — 26 minor releases in ~9
months, auth still changing; pin everything. **B2 demo-to-app
distance:** maximal — every example is an outbound campaign or
support line. **B3 exit cost:** low for us because entry never
happens; for its actual audience, workflows are portable-ish
JSON, but the QA/campaign layer is Dograh-shaped.

---

## S3. Side-by-side comparison

Axes chosen to decompose the products along what matters to us:
layer of the stack, freedom (license/lock-in/local), fit
(ensemble/audio quality), and adoption cost (ops/churn/exit).

| Axis | LiveKit | Pipecat | Dograh |
|---|---|---|---|
| Stack layer | Transport infra (SFU) + agents framework | Pipeline orchestration library | Product/platform (on Pipecat fork) |
| Primary language | Go server; Python-first agents | Python | Python backend + React UI |
| License | Apache-2.0 (⚠ turn-model weights proprietary) | BSD-2 (⚠ one GPL extra: in-process Piper) | BSD-2 |
| Maturity (2026-09) | ~20.9k ★ server / 14.2k ★ agents; ~4 yrs | ~15.5k ★; ~2.5 yrs; 1.0 Apr 2026 | ~5.6k ★; 1 yr |
| Sponsor & funding | LiveKit Inc — ~$150M+, ~$1B val | Daily.co — ~$70M | Zansat — undisclosed |
| Lock-in risk | **Low–medium** (cloud-gated batteries, model license) | **Low** (open smart-turn, vendor-free transport) | **Low** software / young-company risk |
| Fully local/air-gapped | Yes (minus Krisp + full turn model) | Yes (demonstrated path) | Yes (≤16 kHz) |
| Wraps our local stack (llama.cpp / tts-serve / Whisper) | Yes (base_url + node overrides) | Yes (base_url + service subclass; closest templates) | Partly (OpenAI-compatible only) |
| 4-character ensemble fit | Custom composition, fighting AgentSession | Custom composition, best primitives | Structural mismatch |
| Audio quality ceiling | 48 kHz Opus | 48 kHz via WebRTC transports | **8/16 kHz** |
| C2 endpointing offer | Turn-detector (full = cloud; mini = local, restrictive license) | **Smart Turn: open, local, standalone** | Silero only |
| C4 echo / C9 Opus | Browser AEC + Opus native | Same via SmallWebRTC | Undocumented / telephony codecs |
| C8 mixing | Client-native track mixing + Egress composite | `SoundfileMixer` (files); custom for live | No |
| Ops footprint (self-host) | **Heavy** (SFU, Redis, TURN, SSL, Egress) | **Light** (pip package; P2P transport) | Medium (Docker Compose suite) |
| B1 API churn | 1 breaking rewrite + weekly minors | 0.0.x churn era; 1.0 stabilizing; breaking minors | 26 minors/9 months |
| B2 demo-to-our-app distance | Far (assistants, kiosks) | Medium ("storytelling" in README; parts map) | Maximal (call campaigns) |
| B3 exit cost | Medium (transport exits clean; agents code dies) | Low if show logic kept outside processors | N/A (no entry) |

---

## S4. Verdict

**If we had to build on exactly one: Pipecat.** The reasoning
compresses to four points: (1) it is the right *layer* — a
library we compose, not a platform that swallows us; (2) lowest
lock-in of the three, with the only genuinely open+standalone
semantic endpointing model (smart-turn) — the philosophical
opposite of LiveKit's license-restricted weights; (3) lightest
ops for a solo builder (pip + vendor-free P2P WebRTC transport vs
LiveKit's SFU/Redis/TURN estate); (4) independently validated —
Dograh, a funded team building a commercial voice product, chose
it as their foundation. LiveKit would win a different question
("how do we serve 500 concurrent talk-back listeners"), and
that question may genuinely arrive post-MVP — it is the scale
path, not the starting point. Dograh is confirmed out: wrong
genre, wrong audio ceiling, and anything we'd want from it is
Pipecat underneath.

**Are they complementary? Yes, in one specific stack:** Pipecat
explicitly supports LiveKit as a transport, so a future
Zombie-Radio could run Pipecat pipelines over a LiveKit SFU when
audience scale demands it — entering LiveKit at its
infrastructure layer while keeping orchestration in Pipecat, and
skipping LiveKit Agents entirely. Dograh is not complementary for
us: it *contains* a Pipecat, and its additions point at call
centers.

**Standing recommendation for the MVP (unchanged, now with
receipts):** stay on TalkWithMe + tts-serve — none of the three
offers the ensemble shape, so the frameworks would cost learning
budget without dissolving our actual hard problem. **Two concrete
borrowings regardless of framework choice:** (1) the standalone
**smart-turn model** (BSD-2, ~10 ms CPU) as the C2 upgrade when we
outgrow push-to-talk; (2) Pipecat's `SmallWebRTCTransport`
pattern — browser WebRTC with zero vendor infrastructure — as the
reference for upgrading our listener channel beyond WebSocket
audio, with browser-native AEC (C4) and Opus (C9) falling out for
free. LiveKit's client-native track mixing is also prior art for
our C8 "client mixes voice + effects" idea.
