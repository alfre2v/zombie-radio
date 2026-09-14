# experiments/ — empirical artifacts

One dated folder per experiment: `YYYY-MM-DD-short-slug/`, dated
by the day the experiment *runs* (rename before commit if the
start slips). Self-contained and preserved for provenance — an
experiment folder is never edited after its verdict lands, except
to fix a factual transcription error (dated note).

Before starting, every experiment has a **timebox and abort
criteria written down** — a partial observation recorded honestly
beats a heroic overrun.

## Required files

- **`README.md` — the runlog.** A self-contained record: every
  command actually run, in order, with its output — readable
  start-to-finish by a human with no other tabs open, and
  copy-paste repeatable. Placeholders in copy-paste blocks must
  be un-pasteable or guarded (write `<PASTE-BOX-IP-HERE>`, never
  a plausible-looking value — a placeholder pasted verbatim once
  cost a whole measurement run in the system this convention
  comes from). Masthead carries: the question, the timebox, and
  provenance links (TODO task, spec §, related discussions/ADRs).
- **`findings.md` — interpretation ONLY.** Its **verdict criteria
  are written and frozen BEFORE the data exists** (the freeze is
  the commit that carries them plus the filled prediction slots),
  so numbers cannot be rationalized afterward. Contains: verdict
  criteria with per-verdict consequences · **predictions** from
  each participant, registered before the run — predictions that
  die, die in public, with the reason · Results (filled only from
  README.md evidence) · Verdict.

## Rules with teeth

- **Every derived number comes from a committed, dependency-free
  script** over the raw output files — no human or LLM arithmetic
  in the record.
- **Raw outputs are the record of truth**; never trust an
  instrument's own summary beyond the fields you have verified.
- Verdicts route consequences: each criterion names what happens
  on PASS / PARTIAL / FAIL (which ADR freezes, which trigger
  fires), so the experiment ends decisions instead of starting
  debates.
