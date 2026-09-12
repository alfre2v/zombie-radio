# TODO — Product definition arc

**Arc:** Product definition · **Started:** 2026-09-12 ·
**Branch:** `alfre2v/product-definition`
**Spec:** none going in — this arc is special: its deliverable IS
`specs/product-definition.md`. The arc closes when that spec is
reviewed and its PR merges.

**Notation recap** (full conventions in [docs/README.md](README.md)):
`[ ]` open · `[x]` done (with commit SHA in parentheses) · `Task N`
is a sub-step here, never a PR number · cite discussions as
`[discussion YYYY-MM-DD]`, specs as `[spec §X.Y]`.

## Sub-steps

- [ ] **Task 1 — Vision & interaction model discussion.** What the
  audience experiences: what "interactive" means this time (voice
  input? choices? live vs generated-ahead), the 4-actor format, one
  play-through's shape, and what is OUT of scope for a 3-week build.
  Output: `discussions/2026-09-12-vision-and-interaction-model.md`
  (or dated when it happens).
- [ ] **Task 2 — Architecture & foundational tech survey.** Local
  vs cloud stance (the 2024 version was all-local, ≥12GB VRAM);
  LiveKit vs Pipecat vs alternatives; candidate LLM/TTS/STT choices.
  Output: a survey discussion; load-bearing choices graduate to ADRs.
- [ ] **Task 3 — Experiments (conditional).** Only if Task 2 leaves
  a question that needs measurement (e.g. TTS latency/quality,
  Pipecat pipeline viability). Each gets a timeboxed
  `experiments/YYYY-MM-DD-*/` folder per the conventions.
- [ ] **Task 4 — Draft `specs/product-definition.md`.** Synthesize
  Tasks 1–3 into the record of intent: MVP definition, architecture
  direction, follow-on arc candidates for the roadmap build order.
- [ ] **Task 5 — Owner review of the spec; ADRs frozen.** Truth
  audit on any draft ADRs, then mark accepted.
- [ ] **Task 6 — Close ritual in the PR.** Roadmap Features Shipped
  entry, task_history migration, TODO reset, staleness sweep
  (CLAUDE.md included). PR reviewed, approved, and merged by the
  owner.

## Completed

*(none yet)*

## Open questions (acute, arc-specific)

*(none yet — standing questions will live in the spec once it exists)*

## Standing cross-arc notes

- Hard deadline **2026-10-08**: every decision in this arc should be
  weighed against ~2 weeks of build time remaining after it closes.
