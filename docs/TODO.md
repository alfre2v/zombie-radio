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

## Task definition status

*How well-defined each sub-step is; updated as discussions fill the
gaps. The agent keeps pushing on "missing" cells.*

| Task | Definition | What's still missing |
|---|---|---|
| Task 1 — Vision & interaction model | **defined — ready for spec write-up** | All majors settled (QA log Entries 2–4; brainstorm §1–2, §4): radio-show fiction, laptop-client + cloud-GPU-server demo for Oct 8 (booth = future vision), push-to-talk MVP interaction, live-first dialogue ("theatrical live improvisation with LLMs", hybrid trajectory-scaffolds post-MVP). Residual smalls: session/loop length target · client form (browser page vs native) |
| Task 2 — Architecture & tech survey | **partial, direction set** | Main plan inverted (QA log, Entry 2): adapt TalkWithMe + tts-serve; owner effort on deployment + new TTS engines for tts-serve; LiveKit/Pipecat demoted to comparison note. Demo confirmed on a cloud GPU instance (QA log, Entry 4) → provider survey now on the critical path. Missing: LLM & STT choices · latency/VRAM budget · cloud-GPU provider survey (Docker+GPU passthrough) · F5-TTS vs newer engines. Ansible-deployment project: deferred by ruling (private repo; surgical extraction at deployment time — QA log, Entry 3) |
| Task 3 — Experiments | **vague by design** | Fires only if Task 2 leaves measurable questions; candidates so far: TTS engine quality/latency, provider GPU-in-Docker check |
| Task 4 — Draft spec | shape known | Blocked on Tasks 1–2 content |
| Task 5 — Spec review, ADR freeze | defined | — |
| Task 6 — Close ritual in PR | defined | — |

## Completed

*(none yet)*

## Open questions (acute, arc-specific)

*(none yet — standing questions will live in the spec once it exists)*

## Standing cross-arc notes

- Hard deadline **2026-10-08**: every decision in this arc should be
  weighed against ~2 weeks of build time remaining after it closes.
