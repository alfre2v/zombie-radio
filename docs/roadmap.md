# Zombie-Radio roadmap

*Living document. Arcs are referenced by NAME, never by list
position. See [docs/README.md](README.md) for conventions.*

## Product definition

**Zombie-Radio**: an interactive audio-only theater play performed by
4 AI voice actors — scientists trapped in a lab during a zombie
breakout. A Halloween project with a hard deadline: **2026-10-08**
(~3 weeks from project start), to be presented in a talk at the
Austin Python Meetup in October 2026. "hackTNT 2026" is the owner's
internal name for projects built hackathon-style in 2026, not an
event.

The MVP is defined in `specs/product-definition.md` — written by the
**Product definition** arc and kept since as a living ledger of what
the prototype settles.

### Context and prior art

- **Previous incarnation** (2024 local hackathon, discontinued;
  captures the idea, not the code — quality too low to reuse):
  <https://github.com/alfre2v/zombie_radio_ai>. It was a CLI app
  where users spoke voice commands to influence the narrative, built
  entirely on local open-source models (Ollama Nemotron-mini for
  dialogue, F5-TTS for expressive speech, Whisper tiny for speech
  recognition); required a ≥12GB-VRAM CUDA card. *(believed — from
  the repo README, 2026-09-12)*
- **Foundational technology: decided and VALIDATED**
  (decided 2026-09-13; validated 2026-09-16). The MVP builds on
  **TalkWithMe + tts-serve** ([ADR-0001], **accepted** — the
  remote-split spike returned PASS with zero upstream
  modifications); the originally named candidates LiveKit and
  Pipecat were surveyed ([discussion 2026-09-13] audio-framework
  survey) and not adopted — the Pipecat flip trigger expired
  unfired, and the survey marks two framework-independent
  borrowings (smart-turn model, SmallWebRTC pattern) for
  post-MVP. Sharpened on 2026-09-21: the app becomes our own fork,
  **TalkWithZombies**, free to diverge ([ADR-0002]), and its show
  engine is redesigned around one shared script, a director in
  code, a GBNF screenplay grammar and the browser as the clock
  ([ADR-0003], accepted 2026-09-23 after its gate).

## Features Shipped

- **2026-09-17 — Product definition** (arc closed, PR #3; started
  2026-09-12). The project went from an empty repo and an idea to:
  a product spec (`specs/product-definition.md`, wrapped with
  explicitly-deferred questions) · a validated foundation —
  TalkWithMe + tts-serve, proven by the remote-split experiment
  to run split across laptop + cloud GPU with ZERO modifications
  ([ADR-0001] accepted; experiment verdict PASS, total cost
  $2.97) · surveys with rulings (audio frameworks, 13 cloud GPU
  providers, LLM ranked shortlist of five, TTS engine ranking) ·
  a security posture (SSH tunnel, single-operator, no-secrets
  repo) · the narrative-health framework (two axes, 20 failure
  mechanisms) born from live ensemble testing · a reproduction
  recipe + restart runbook that rebuild the whole stack from
  nothing · and the prototype-first inversion that shapes the
  next arc.

## Feature build order

1. **Product definition** — DONE (2026-09-12 → 2026-09-17,
   closed PR #3; see Features Shipped). Ending reshaped by the
   **prototype-first inversion** ([discussion 2026-09-16]): the
   two remaining experiments moved into arc 2 rather than
   preceding it.
2. **MVP prototype** — IN PROGRESS since 2026-09-17 (named
   2026-09-16 by the inversion; execution state lives in
   TODO.md, never here). **Deliverable #1 is the deployment
   machinery** ([discussion 2026-09-17]): Ansible + Docker
   automation standing up the full model-service stack
   identically on a cloud GPU VM and on a local GPU machine
   (`delegate_to: localhost`) — "deployment is 50% of the MVP"
   (owner) — delivered and proven live on 2026-09-18. Then the
   arc's boundary moved (2026-09-21): the show engine's design,
   first meant for a later arc, was pulled in because no patch
   could be shaped without it — so the prototype becomes
   **TalkWithZombies** ([ADR-0002]) running the new engine
   ([ADR-0003]; its gate passed 2026-09-22), built under a 3-day
   timebox. Then the prototype as the experiment platform, with
   the real cast: in-prototype experiments in the new engine (LLM
   audition [spec §7.3] · TTS comparison + VRAM budget [spec
   §7.2], LuxTTS in the pool · the narrative-health probes
   [discussion 2026-09-16]) and the canned episode, a MUST for
   demo day. Guardrails riding along: experiments keep the
   protocol skeleton; prompt work stays disposable until the
   audition; the spec is updated as a ledger during the build.
3. *(further arcs emerge as the prototype teaches us)* — the
   **show arc** was named at this one's opening: story and episode
   authoring (the trajectory scaffolds, [spec §5.2]) and the full
   demo rehearsal. Its director-design half moved into the MVP
   prototype on 2026-09-21.

## Ideas / parking lot

- **Browser-side STT (Whisper in the browser)** — parked
  2026-09-15, surfaced during the remote-split experiment's
  component inventory. Whisper genuinely runs client-side:
  whisper.cpp compiled to WebAssembly, or transformers.js
  running tiny/base checkpoints on WebGPU. If the web client
  transcribed locally, the server would shed Whisper's VRAM and
  the push-to-talk upload would shrink from audio to text —
  helping both the 16 GB VRAM aspiration and flaky venue
  networks. Costs that park it: only the small checkpoints run
  at usable speed (accuracy hit — proper names especially, our
  challenge C6), and browser/WebGPU behavior varies by machine.
  Trigger to consider: post-MVP, if server VRAM gets tight or a
  multi-listener staging makes server-side STT a bottleneck.
- **An announcer voice** — parked 2026-09-23, surfaced while
  designing the show engine's director ([discussion 2026-09-23]
  show-engine-design, decision 5). Today the director's events
  ("Offstage: something is scratching at the loading dock door")
  are never spoken: they reach the model as instructions, and the
  audience learns of them only through the characters' reactions.
  An announcer would be a fifth voice with its own reference clip
  that reads some events aloud, the way 1930s radio plays had one
  ("Meanwhile, in the cold room…"). Mechanically small: the
  grammar allows `"Announcer"` as a speaker in the rounds the
  director chooses, and the story's cast lists it with a voice.
  Costs that park it: a voice sample to find and clear, the
  writing to make it sound period-true, and one more voice
  competing for airtime. Trigger to consider: the 1930s radio look
  (day-three polish) or the show arc, if the events feel too
  hidden.
