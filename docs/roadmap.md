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
- **Foundational technology: evaluated and decided**
  (2026-09-13, during the Product definition arc). The MVP
  builds on **TalkWithMe + tts-serve** ([ADR-0001], draft —
  freeze gated on a validation spike); the originally named
  candidates LiveKit and Pipecat were surveyed
  ([discussion 2026-09-13] audio-framework survey) and not
  adopted — Pipecat remains the named fallback if the spike
  fails, and the survey marks two framework-independent
  borrowings (smart-turn model, SmallWebRTC pattern) for
  post-MVP.

## Features Shipped

*(nothing yet — dated, user-facing narrative entries land here as
arcs close)*

## Feature build order

1. **Product definition** — IN PROGRESS since 2026-09-12
   (execution state lives in TODO.md, never here): conduct the
   discussions about what we want to build and land
   `specs/product-definition.md`. Surveys done; preliminary spec
   drafted; validation spike pending.
2. *(subsequent arcs emerge from the Product definition arc)*

## Ideas / parking lot

*(empty)*
