# Zombie-Radio roadmap

*Living document. Arcs are referenced by NAME, never by list
position. See [docs/README.md](README.md) for conventions.*

## Product definition

**Zombie-Radio**: an interactive audio-only theater play performed by
4 AI voice actors — scientists trapped in a lab during a zombie
breakout. A Halloween project with a hard deadline: **2026-10-08**
(hackTNT 2026, ~3 weeks from project start).

The MVP definition is deliberately not written yet: producing it is
the job of the **Product definition** arc (first in the build order).

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
  post-MVP.

## Features Shipped

*(nothing yet — dated, user-facing narrative entries land here as
arcs close)*

## Feature build order

1. **Product definition** — IN PROGRESS since 2026-09-12,
   WRAPPING (execution state lives in TODO.md, never here):
   conduct the discussions about what we want to build and land
   `specs/product-definition.md`. Surveys done; spec drafted with
   spike results folded; validation spike DONE (2026-09-16,
   verdict PASS). The arc's ending was reshaped by the
   **prototype-first inversion** ([discussion 2026-09-16]): the
   two remaining experiments moved to the next arc; this arc now
   closes with a spec quick-wrap + review + close ritual.
2. **MVP prototype** — NEXT (named 2026-09-16 by the inversion):
   deploy the spike's exact validated configuration (experiment
   recipe R0–R13 + TalkWithMe local + 4 personas) as a
   repeatable, easily re-deployable prototype — then use it as
   the experiment platform. Opening material: the in-prototype
   experiments (LLM audition over the ranked five [spec §7.3] ·
   TTS comparison + VRAM budget [spec §7.2], LuxTTS in the pool ·
   the narrative-health zero-code probe battery
   [discussion 2026-09-16]) and the follow-ups backlog (label
   sanitizer · max-chars accumulator · `max_turns_for_context`
   lever). Guardrails riding along: experiments keep the protocol
   skeleton; prompt work stays disposable until the audition;
   the spec is updated as a ledger during the build.
3. *(further arcs emerge as the prototype teaches us)*

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
