# The Zombie-Radio documentation system

This folder is the project's shared human/agent memory. The goal is
**continuity**, not documentation for its own sake: a session ending
today must leave enough context for the next session, contributor, or
agent to pick up cold. The repo — not any agent's private memory — is
the memory of record: any fact that matters across machines, sessions,
or contributors lives here.

Three working agreements power everything else:

1. **Discussion-first**: propose the shape of each piece, get the
   owner's input, then create.
2. **Review-before-commit is strict**: show the diff, wait for
   explicit review. A harness permission prompt is not review.
3. **The repo is the memory of record**: agent memory holds only
   working agreements and collaboration preferences; project facts
   live in `docs/`.

Context that shapes everything below: this project has a **hard
deadline (2026-10-08, ~3 weeks from adoption)**. The system is
deliberately lightweight — every piece here earns its keep by saving
more time than it costs. When in doubt, write less but write it true.

## The pieces and their mutability

Every document type has a **declared mutability**, so nothing is ever
ambiguously stale — each file announces whether it may change.

| Piece | Purpose | Lifecycle |
|---|---|---|
| `decisions/` (ADRs) | "We chose X over Y because Z" | **Immutable once accepted**; superseded by a NEW ADR, never rewritten |
| `discussions/` | How we reasoned to X — alternatives weighed, pushbacks, why-not | **Append-only after the decision lands**: reality reports back via dated addendum sections, never silent rewrites |
| `specs/` | What we intend to build, per significant feature | Living during its arc; stamped BUILT-AND-SHIPPED (with as-built pointers) at arc close, then preserved as the record of intent |
| `experiments/` | Empirical artifacts: measurements, comparisons, prototypes | Self-contained, preserved for provenance |
| `runbooks/` | Procedures executed repeatedly (deploy, restore, rotate keys) | Living, undated; updated as the procedure evolves |
| `reports/` | Incidents, recoveries, notable events — "this happened once" (vs a runbook's "do this each time") | Dated filename; **immutable once written** |
| `visuals/` | Presentation derivatives (HTML pages, decks); the textual doc is the source | Self-contained per artifact; regenerated when the source drifts. *(Folder created when first needed.)* |
| `roadmap.md` | Strategic: what shipped, what's next | Living; arcs referenced by NAME, never by list position |
| `TODO.md` | THE active arc's execution state | Rewritten when an arc opens; persists across mid-arc PR splits; reset to a between-arcs skeleton when the arc closes |
| `task_history.md` | Sub-step engineering log of CLOSED arcs | Append-only |
| `follow-ups.md` | Small items, known limitations, explicit deferrals | Items resolve and get DELETED; deferrals stay until their trigger fires |
| `refactoring-opportunities.md` | Working code we'd redo with budget | Append-only in spirit; entries get RESOLVED/DROPPED date markers, never silent deletion. *(File created when the first candidate appears.)* |

Division of labor among READMEs: each subfolder's short README
explains the format expected INSIDE it; this file explains the
RELATIONSHIPS between the pieces — the workflow.

## The cross-reference legend (use everywhere)

- `[spec §X.Y]` — a spec section (topic-organized, so stable)
- `[ADR-NNNN]` — a decision record (immutable)
- `[discussion YYYY-MM-DD]` (optionally `Part N`) — a discussion doc
- `[experiment YYYY-MM-DD]` — an experiment folder
- bare SHA in parentheses — a commit (immutable)
- `Task N` — a sub-step of the active arc; `PR #N` — a pull request
  (never conflate the two)
- **Never cite by list position** ("item 3", roadmap numbers) —
  positions renumber and the citation rots. Arcs by NAME, sections by
  topic-stable numbers, everything else by the bracketed forms above.

## The arc lifecycle

Work happens in **arcs**: named, scoped efforts that open, run, and
close. The lifecycle keeps the docs true.

**Open**: roadmap entry at the top of the build order → write
`docs/specs/<arc>.md` → rewrite `TODO.md` with the arc's sub-steps.

**During**: one discussion doc per major design question; an ADR per
load-bearing decision; an experiment folder when a question needs
measurement; every commit message cites its `[spec §]`; TODO updated
with each commit — it is the single source of "where are we", and
it carries an **Owner action queue** (actions only the owner can
take, deleted when done, so they never drown in chat scrollback). Inside
a build plan, small decisions are decided inline in the ledger; big
ones (surveys, tool selections) get their own dated discussion doc,
with the ledger entry linking it.

**Close — the ritual lives IN the closing PR, never post-merge**:

- roadmap gains its Features Shipped entry
- `task_history.md` gains the arc section (TODO content migrated
  verbatim)
- TODO resets to the between-arcs skeleton
- the build plan/journal gets its closing entry
- the spec gets its BUILT-AND-SHIPPED stamp
- a staleness sweep runs over the living docs (CLAUDE.md included),
  plus a self-generated list of "documents I would most likely forget
  to update", checked one by one

The PR's merge IS the arc's end.

## Writing principles

- **Every fact has exactly one home**; every other document links to
  it. When two docs both explain something, one is already stale —
  designate the owner and demote the other to a pointer.
- **Self-contained writing for humans**: docs serve human recall, not
  just agent orientation. Spell facts out in place; when a
  conversation produced a good map, preserve it verbatim in a
  "for human eyes" section rather than compressing it away.
- **Receipts**: claims carry `file:line`, quoted source, or a URL —
  and are labeled measured / docs-say / believed.
- **Linear reading over change-logs**: when a living doc accretes
  corrections, periodically rewrite it as one coherent story instead
  of stacking INVALIDATED/UPDATE banners. Exception: ADRs and reports
  (immutable) and discussions (dated addenda).
- **Chronology has exactly one home too**: a per-arc Q&A log (a
  discussions sub-genre) records who said what and when; every
  other document gets the *synthesis* — the integrated outcome of
  a whole exchange, never a round-by-round chronicle. When a
  discussion produces a list, the finished list is the
  deliverable.
- Comment/document the non-obvious WHY, never restate the what.

## Anti-patterns (paid for elsewhere; do not re-buy)

- **Date-stamped task files** (`tasks-2026-09-12.md`): each session
  spawns a new one, old ones rot unread. Fix: ONE stable filename
  (`TODO.md`) replaced per arc, never accumulated.
- **Order-implying references** ("see item #2"): rot silently when
  lists renumber. Fix: the legend above.
- **Conflating intent with status**: specs do not track execution;
  the roadmap does not list sub-steps. Each layer answers exactly one
  question.
- **The close ritual scheduled post-merge**: janitorial work after
  the merge gets forgotten. Fix: ritual commits ride the closing PR.

## Cold-start navigation

Picking up cold, read in order:

1. `TODO.md` — what's active (30 seconds)
2. the active arc's spec — the shape (5 minutes)
3. `roadmap.md` Features Shipped — recent history (2 minutes)
4. `git log --oneline -10` — what actually landed

For any unclear decision: *why is X this way* → the ADR; *how did we
get there* → the discussion; *what did we try first* → the experiment.

## Update trail

- **2026-09-12** — System adopted at project start (empty repo).
- **2026-09-14** — Conventions that emerged in practice recorded:
  the chronology-vs-synthesis principle (per-arc Q&A logs hold
  the round-by-round record; all other docs get the integrated
  outcome) and TODO's Owner action queue.
