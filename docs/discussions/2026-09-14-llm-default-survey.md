# LLM working-default survey

**Date:** 2026-09-14 · **Arc:** Product definition (Task 2)
**Type:** survey (candidate models compared and adjudicated)
**Status:** METHOD AGREED, RESEARCH NOT YET RUN — this document
currently persists the agreed methodology; results sections are
placeholders. (Deliberate echo of the experiments protocol:
registering the method before the data exists keeps the data
from bending the method.)

*Context for the cold reader: Zombie-Radio's dialogue is
improvised live by a small local LLM served by llama.cpp behind
an OpenAI-compatible endpoint ([spec §4], brainstorm §3). The
final model choice is deliberately deferred — swapping is a
config change — but a **working default** must be picked before
prompt-engineering starts, because prompts overfit to a model's
voice. The owner's shortlist, from hands-on experience on his own
hardware: a small **Gemma 4**, **Qwen 3.5**, **Nemotron** (if
VRAM fits), or an **LFM2-class** very small model.*

## 1. Methodological principle (learned 2026-09-14)

The agent's first proposed method was a *verification* protocol —
confirm llama.cpp support, GGUF availability, VRAM fit. The owner
rejected it: those facts are already known **by experience** for
the shortlisted models; verification axes only earn their keep
against *unknown* models. Principle adopted: **match the method
to the epistemic state** — verification axes filter unknowns;
known-and-trusted models need *differentiation* axes that speak
to this application specifically.

## 2. The comparison axes

For a 4-character improvised horror radio drama:

1. **Context length — and its real cost.** Raw maximum window;
   *effective* context (small models often degrade well before
   the advertised limit, and our story-so-far grows all
   evening); and **KV-cache VRAM cost at the target context** —
   a 32k window can quietly eat gigabytes the TTS engines need.
2. **Loop-proneness.** The owner's named disease from 2024
   ("they loop like crazy"): repetition/degeneration tendencies
   over long generation runs.
3. **Persona stability.** Can one model voice 4 distinct
   characters over a long session without them bleeding into
   each other? The roleplay community measures this (RP
   leaderboards, EQ-Bench creative writing) — the axis most
   correlated with the show being good.
4. **Steerability under a director.** Obedience to mid-stream
   system commands ("mention the generator failing", "speak as
   MARCUS only", entropy-term injection) AND structured-output
   discipline: reliably emitting parseable `CHARACTER: line`
   format without drift.
5. **Horror tolerance & positivity bias.** Safety-tuned models
   may refuse peril, soften violence, tone-police a zombie
   apocalypse — or exhibit the RP community's most-hated
   failure, relentless positivity, which kills drama. Models
   differ a lot here.
6. **Assistant-voice contamination.** Does it slip into "As an
   AI…" / bullet-list / helpful-assistant register mid-drama?
   Dialogue naturalness vs. chatbot-speak.
7. **Latency profile for our traffic shape.** Our pattern is
   long-growing-prompt → short completion: **prefill-dominated**.
   Prefill throughput at our quantization on A6000/3090-class
   hardware matters more than headline tokens/s.
8. **RP-finetune ecosystem depth.** If a base model disappoints,
   does a well-regarded community roleplay finetune of it exist?
   A deep bench is insurance.

**Epistemic caveat (drives the method):** axes 2, 3, 5, 6 are
only *weakly* researchable — community signal yields priors, not
answers. The real answers come from the audition (Track 3).

## 3. The method, in three tracks

- **Track 1 — Discovery sweep** (research). Hunt for models NOT
  on the owner's list (small-class releases through 2026 with a
  creative/multi-character lean). Unknown models first pass
  through the *verification* filters (llama.cpp/GGUF support,
  VRAM at quantization, license) — the axes that are useless for
  knowns are exactly right for disqualifying unknowns — then
  survivors get scored on §2 axes via community signal. Output:
  **1–2 newcomers** brought forward to stand next to the known
  four in a later comparison round.
- **Track 2 — Known-models table** (research-lite). For the
  owner's four: fill ONLY the researchable cells — axis 1 in
  full (context + KV cost), community priors on 2/3/5/6/8,
  published prefill numbers where they exist (7). No
  re-verification of what the owner already knows.
- **Track 3 — The audition** (candidate experiment; NOT started;
  spec'd when triggered). A prompt harness — 4 personas, N
  generated lines per candidate, identical seeds/settings — run
  on the owner's RTX 3090, counting loops, format breaks,
  refusals, and character bleed: the empirical answer to axes
  2/3/5/6. Doubly valuable: the harness is also the show's first
  prompt-engineering artifact. Feeds on the character bibles
  (owner action queue); follows the experiments protocol
  (timebox, runlog, pre-registered verdict criteria).

**Deliverable:** the combined table (knowns + newcomers), a
recommended **working default** + runner-up — explicitly
revisable by demo week — blessed/vetoed by the owner, then
recorded in [spec §4]. No ADR: the choice is deliberately cheap
to reverse, the opposite of ADR material.

## 4. Track 1 results — Discovery sweep

*(placeholder — research not yet run)*

## 5. Track 2 results — Known-models table

*(placeholder — research not yet run)*

## 6. Recommendation

*(placeholder — follows Tracks 1–2; Track 3 audition may revise)*

**Trigger to revisit:** the audition contradicting the
research-based recommendation; or a shortlist model releasing a
major new small variant before demo week.
