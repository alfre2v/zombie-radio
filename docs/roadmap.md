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
- **Candidate foundational technologies** the owner wants to
  evaluate, likely via `experiments/`:
  - LiveKit — <https://github.com/livekit/livekit>
  - Pipecat — <https://github.com/pipecat-ai/pipecat>

## Features Shipped

*(nothing yet — dated, user-facing narrative entries land here as
arcs close)*

## Feature build order

1. **Product definition** — conduct the discussions about what we
   want to build (interaction model, architecture direction,
   local-vs-cloud stance, scope for 3 weeks) and land
   `specs/product-definition.md`. Likely includes a survey discussion
   of LiveKit vs Pipecat and possibly timeboxed experiments.
2. *(subsequent arcs emerge from the Product definition arc)*

## Ideas / parking lot

*(empty)*
