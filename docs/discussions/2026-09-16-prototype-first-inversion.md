# The prototype-first inversion

**Date:** 2026-09-16 (same evening the remote-split experiment
closed) · **Arc:** Product definition — this decision RESHAPES
the arc's ending and names the next arc.
**Type:** working-method decision (owner-proposed, agent-endorsed
with guardrails, agreed same day)
**Status:** DECIDED. The consequences below are executed in the
same PR that carries this document.

*Context for the cold reader: the original plan was
experiments → polished spec → build. Two standalone experiments
remained on that path (spec §7.2 TTS comparison, §7.3 LLM
audition), followed by spec completion. The remote-split
experiment ([experiments/2026-09-14-talkwithme-remote-split-test],
verdict PASS) changed the economics of that plan, and the owner
proposed inverting it.*

## 1. The decision

**Build the MVP prototype FIRST — the exact component
configuration the experiment validated (recipe R0–R13 +
TalkWithMe local) — then run the remaining experiments ON the
prototype, and write the spec's remaining parts alongside the
build.** The prototype is the experiment platform; the spec
follows the build as a ledger instead of leading it as a
blueprint.

## 2. Why (the rationale, integrated)

- **The spike changed the epistemics.** Experiments-before-build
  was the right order while the foundation was unproven. It is
  now proven with ZERO upstream modifications — a working
  prototype costs roughly "follow the recipe and add personas."
  When the prototype is nearly free, a synthetic experiment
  harness is MORE expensive than the real thing.
- **In-prototype experiments measure the truth better.** Proven
  by our own data: the name-memory failure looked like model
  stupidity and was actually `max_turns_for_context: 6` (taxonomy
  C9). A standalone LLM-audition harness would have auditioned
  models under DIFFERENT context machinery than the show uses and
  mis-attributed exactly that class of failure. In the prototype,
  swapping the LLM is one `-hf` flag; swapping TTS is one URL.
- **Tracer-bullet fit.** End-to-end working system first, then
  iterate components under real conditions — the right shape for
  a 3-week deadline; polish loops on paper are where owner-hours
  die.

## 3. The three guardrails (owner-accepted)

1. **Experiments become lighter, not looser.** The owner's rule —
   no single-model (or single-engine) pick without an experiment —
   survives. §7.2 and §7.3 become IN-PROTOTYPE experiments: same
   protocol skeleton (question, timebox, pre-registered pick
   criteria, results in a runlog), run on the prototype instead
   of a bespoke harness. Freeze-criteria-before-data stays.
2. **Prompt work stays disposable until the audition runs.**
   Prompts overfit to a model's voice. Building the prototype on
   Nemotron is fine; heavy prompt polish before the in-prototype
   model swap-off is where effort would bleed. Character bibles
   are safe (model-neutral); tuned prompts are not.
3. **The spec becomes a ledger, not a blueprint — but decisions
   still get written.** The failure mode of build-first is silent
   architecture. As prototype decisions settle they land in the
   spec as short as-built entries (ADRs for load-bearing ones).
   The spec may follow the build — it never lags by more than a
   session.

## 4. Consequences (executed with this document)

- **Product definition arc wraps quickly:** fast final spec pass
  marking remaining `[UNKNOWN]`s as *deferred-to-prototype*
  rather than blocking → owner review (Task 5) → Task 6 close
  ritual. A spec with explicitly-open questions is a legitimate
  deliverable.
- **Next arc named: "MVP prototype"** (roadmap build order):
  deploy the experiment's exact configuration as a repeatable
  setup; opening material = the in-prototype experiments (LLM
  swap-off §7.3, TTS comparison §7.2, the narrative-health
  zero-code probe battery) + the follow-ups backlog (sanitizer ·
  max-chars accumulator · `max_turns_for_context` lever).
- **Owner action-queue rulings (2026-09-16):**
  - Voice samples: executing soon; famous-actor clips are likely
    → **never committed to the repo** (curated, used, gitignored
    — follow-ups.md carries the hygiene entry).
  - Character bibles: executing soon (safe under guardrail 2).
  - Home 3090 driver check: **deprioritized** — the demo runs
    cloud-only; the 3090 leaves the MVP fleet, which also retires
    the fleet-minimum-driver worry (all show boxes are pinned
    R570).
  - Demo-day logistics: postponed until a working MVP exists;
    the **"canned episode" emergency mode is ruled a MUST**
    (recorded from the prototype once it works).
- **TODO.md becomes the living parking-lot table** of the task
  landscape (owner-requested): updated at every execution or
  decision; the re-orientation surface when the owner returns to
  a topic.
