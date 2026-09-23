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

## Delegating a unit of work to another agent — an option, NOT in use

*Recorded 2026-09-23 as a method for later. **Ruling (owner,
2026-09-23): no delegation during the fork's first steps** — the
work stays in a tight learning loop between the owner and the lead
agent. Revisit only on the owner's word.*

**What delegation means here.** A unit of build work executed by
another model **in another harness, in parallel** with the lead
agent: the owner opens a separate clone of the repository, starts a
new branch, runs the unit there with whatever harness he chooses,
and the delegate submits its own pull request. The owner sees the
execution and can converse with the delegate throughout. It does
**not** mean sub-agents launched by the lead inside its own harness:
those are fine for online research or for summarizing a large
codebase, but not for units of build work — their execution is
invisible to the owner and they cannot be talked to.

The lead agent keeps the dialog with the owner, the discussions, the
experiments and every load-bearing design question. A unit can be
delegated only when three things hold: its design is settled, its
change is contained, and a **check proves it done** — a test or a
command, never a paragraph. The method, if it is ever switched on:

- **Contract-first.** Before hand-off, the lead lands the unit's
  interface (stubs, signatures) and its tests — failing, or precise
  test cases in the work order — on the main branch. The delegate
  implements to green. A weaker model does well against a failing
  test and badly against prose; and a frozen interface is what lets
  two branches move in parallel without colliding.
- **A work order the owner can carry to any harness.** One
  self-contained markdown file, harness-agnostic: the goal in two
  sentences; the commit to branch from; the files the unit may
  touch and the ones it must not (disjoint from the lead's current
  work); the contract; the acceptance check; the branch name and
  pull-request title; what to report back. It is handed over by
  the owner (pasted, or committed at the branch's start) and dies
  with the unit's pull request, like a session handoff.
- **House rules where every harness looks.** The work order does not
  repeat them. In TalkWithZombies they live in `AGENTS.md` (a
  convention many harnesses read); in this repository they live in
  `CLAUDE.md`, which Claude Code reads — so switching the method on
  here means adding an `AGENTS.md` that carries or points to the
  same rules.
- **Review on the delegate's pull request.** The owner reviews and
  merges it as any other — his review rule is unchanged; the lead
  can make a review pass on the pull request when asked, and
  rebases its own branch after the merge.
- **What stays with the lead:** anything on a live box (the
  drill rules), experiments, the design itself.
- **When it pays:** units of more than about an hour of work that
  come with a real check. Below that, writing the work order costs
  more than the work.
- **The knobs, already in place:** build items in `TODO.md` carry an
  *Acceptance* check and a *delegable later* mark (first applied to
  Task 6 of the MVP-prototype arc). The acceptance checks serve the
  lead's own work now; the marks wait for the owner's word.

### What crosses over: a work order, not a handoff

When a unit is delegated, three things cross to the other harness:
**the work order**; **the repository clone**, which already holds the
house rules (`AGENTS.md`) and the interface and tests the lead landed
first; and **the owner**, who answers the delegate's questions. The
clone and the tests carry most of the weight; the work order is the
map that ties them together.

A work order is not a session handoff. Both are throwaway documents
that carry context across a boundary, but for different readers
doing different jobs. A session handoff (written before a new
session or a compaction) carries the LEAD across a context boundary:
its reader takes over the whole role — converse with the owner,
weigh designs, decide what comes next — so it must carry everything
that must not be lost, and is deliberately long and over-complete. A
work order carries ONE CLOSED JOB to an implementer who must not
design:

| | Session handoff (for the lead) | Work order (for a delegate) |
|---|---|---|
| **Reader** | the lead, in a fresh context | another model, possibly weaker, in another harness |
| **Reader's role** | continue the whole project: converse, design, decide | execute one bounded unit; decide nothing beyond it |
| **Content** | everything that must survive: the owner, the way of working, history, state, nuances, the task board | only what the unit needs: the goal, the starting commit, the files, the contract, the check |
| **Size** | long on purpose (the 2026-09-22 handoff ran about 800 lines) | a page or two |
| **Design context** | points to the docs, with a reading order | **copies in** the few design facts the unit needs, so the delegate never has to read the spec |
| **When something is unclear** | the reader proposes and discusses with the owner | the reader **stops and asks the owner**, and never redesigns |
| **Finished when** | never; the reader keeps going | the acceptance check passes and a pull request exists |
| **Lifetime** | until the session it serves ends (deleted with the owner's permission) | until the unit's pull request merges |

**The work order's skeleton:**

```
# Work order — <unit>
Issued <date> by the lead, carried by the owner to <harness>.
Start from: <branch> at <commit>. Your branch: <name>. Pull request into <branch>, titled "<…>".

## The job                — two sentences
## What you need to know  — the few design facts, copied in (not links to read)
## The contract           — interfaces already on the start commit (file:line); do not change them
## Files                  — you may change: …   you must not touch: …
## Done when              — `pytest tests/test_<unit>.py` green; the whole suite green; no new dependencies
## Rules                  — AGENTS.md at the repository root; plus: if anything is ambiguous or the
                            contract looks wrong, STOP and ask the owner — do not redesign
## Report back            — in the pull request: what changed, the test output, anything you were unsure of
```

The load-bearing line is "stop and ask; do not redesign": it keeps
the design with the owner and the lead even when the typing happens
elsewhere.

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
- **2026-09-23** — "Delegating a unit of work to another agent"
  recorded as an option NOT in use (owner ruling: no delegation
  during the fork's first steps — tight learning loop): units run
  by other models in other harnesses, in parallel, in separate
  clones and branches, each submitting its own pull request —
  never sub-agents of the lead for build work; its knobs
  (acceptance checks, delegable-later marks) placed in `TODO.md`.
  Same day: "What crosses over" added — the work order versus a
  session handoff, and the work order's skeleton.
