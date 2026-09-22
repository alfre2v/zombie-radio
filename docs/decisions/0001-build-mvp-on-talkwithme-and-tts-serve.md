# Build the MVP on TalkWithMe and tts-serve
**Date:** 2026-09-13
**Status:** accepted (2026-09-16 — the validation gate passed;
see Validation below)

## Context

Zombie-Radio's MVP — a 4-actor improvised radio drama on
self-hosted open models, with push-to-talk listener interaction,
laptop web client + cloud GPU backend — must ship by 2026-10-08
(~3 weeks), built by a solo engineer whose scarce resource is
owner-hours and who must understand every architectural layer
(the project's working method).

A foundation had to be chosen: adopt a voice-agent framework, or
adapt existing small open-source applications. The framework
landscape was surveyed with online research
([discussion 2026-09-13] `audio-framework-survey.md`: LiveKit,
Pipecat, Dograh) and the choice was stress-tested in an
adversarial debate ([discussion 2026-09-13] brainstorm §9). Key
findings that forced the choice:

- **No surveyed framework has the ensemble shape.** All three
  model one human ↔ one assistant; a 4-character ensemble is
  novel composition work in every one of them. TalkWithMe
  (MIT, FastAPI + JS) already ships multi-persona group chats
  with routing, persona-to-persona replies, per-persona cloned
  voices, and sentence-chunked streaming TTS.
- **The MVP's traffic shape neutralizes the frameworks' core
  value.** Their engineering centers on sub-second full-duplex
  conversation (VAD, barge-in, endpointing). Our broadcast
  tolerates seconds of buffering, and the push-to-talk ruling
  (brainstorm §5) already solves endpointing, self-hearing, and
  addressee detection by construction.
- **The learning budget is decisive.** Pipecat (the best
  framework surveyed) means a new mental model plus tracked
  breaking changes; TalkWithMe + tts-serve are small codebases in
  a stack the owner already knows, absorbed by forking rather
  than tracked as dependencies.
- **The coveted framework components are standalone.** Silero VAD
  and Pipecat's smart-turn endpointing model are BSD-2 and
  importable without the framework — graftable onto any stack
  later.

## Decision

Build the MVP by **adapting TalkWithMe** (base for the web client
and persona/ensemble orchestration) **and tts-serve** (unified
REST abstraction over local TTS engines), rather than adopting
LiveKit, Pipecat, or Dograh. Owner engineering effort concentrates
on the deployment layer (Docker + Ansible, local/cloud-GPU
symmetric) and on adapting the ensemble into a radio broadcast.

The decision is a **bet with a validation gate**: the
TalkWithMe remote-split test ("the spike", TODO Task 3a; timeboxed 2 days,
verdict criteria pre-registered) must confirm the backend can be
split from the localhost-born client across real internet.
**Flip trigger:** if the spike FAILS on structural grounds
(audio path unusable over WAN, pervasive blocking design,
unownable code), the MVP moves to Pipecat — the survey's
framework verdict — at a cost of days, not weeks.

## Consequences

**What it costs:**

- Two bus-factor-one upstreams (TalkWithMe ~209 stars, tts-serve
  ~17 stars, same single author); we mitigate by forking and
  owning rather than tracking.
- We inherit code of unverified quality and unknown WAN behavior
  until the spike reports (the largest open risk — hence the
  gate).
- Post-MVP features (always-listening, live multi-source mixing,
  multi-listener scale) get hand-built or grafted, where Pipecat
  would have provided primitives.

**What it buys:**

- The ensemble engine — the product's hard 20% — largely exists
  on day one.
- A small, fully-ownable codebase in a familiar stack: maximal
  owner understanding per hour, no framework churn tax during the
  3-week window.
- Integration seams already aligned with the local stack:
  OpenAI-compatible LLM (llama.cpp), whisper-fastapi STT, HTTP
  TTS (tts-serve is one thin adapter away).
- A well-scoped potential upstream contribution (F5-TTS engine
  for tts-serve).

**Reversibility:** high until the spike verdict (flip costs
days); moderate during the build (show logic — director, prompts,
personas — stays behind our own interfaces, so a later port
loses wiring, not soul); the decision is explicitly scoped to the
MVP — the post-MVP booth arc (always-listening) re-opens the
framework question, where partial Pipecat adoption (smart-turn
first) is anticipated. Supersede via a new ADR if that happens.

## Validation (2026-09-16) — gate passed, decision frozen

The spike ran 2026-09-15/16 (Hyperstack RTX A4000, NORWAY-1) and
returned **PASS** against its pre-registered criteria
(`experiments/2026-09-14-talkwithme-remote-split-test/`,
findings.md Verdict). Truth-audit of this ADR's claims against
the evidence:

- "Unknown WAN behavior until the spike reports" (the largest
  open risk) — resolved BETTER than claimed: the split needed
  **zero upstream modifications**; TalkWithMe reaches all model
  services by URL through the SSH tunnel.
- "tts-serve is one thin adapter away" — overcautious: **zero
  adapter** was needed; TalkWithMe auto-detected the engine from
  `/capabilities`.
- "We inherit code of unverified quality" — partially retired:
  the spike's source audits (session/round machinery, tts.js
  pipeline) found readable, patchable code; two small designated
  patches are already scoped (output sanitizer for `[Name]:`
  labels; max-chars sentence accumulator in `static/tts.js`).
- The ensemble-exists-on-day-one claim held (4-persona group
  sessions with distinct cloned voices, end-to-end), with the
  honest amendment that ensemble NARRATIVE quality is now a
  mapped problem of its own ([discussion 2026-09-16], narrative
  health).

The **Pipecat flip trigger expires unfired.** This ADR is frozen;
changes from here go through a superseding ADR.

---

*Annotation 2026-09-21 (dated note; the text above is frozen):* the
"forking and owning rather than tracking" clause of Consequences,
and the F5-TTS upstream contribution mentioned under "what it
buys", are sharpened by **ADR-0002** (fork TalkWithMe as
TalkWithZombies, diverging, in a sibling repository; contribution
ledger re-ranked — deployment machinery first, the sentence
accumulator as the one plausible app-code patch). The ensemble's
turn engine and prompt structure are redesigned in **ADR-0003**
(draft, gated).
