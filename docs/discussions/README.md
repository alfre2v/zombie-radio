# discussions/ — decision narratives

Filenames: `YYYY-MM-DD-topic.md`. Narrative register: preserve the
alternatives, the owner's pushbacks, the why-not-X. **Append-only
after the decision lands** — reality reports back via dated addendum
sections, never silent rewrites.

Sub-genres, all living here:

- **Decision narratives** — how we reasoned to a choice.
- **Surveys** — candidate tools compared and adjudicated.
- **Q&A logs** — per-arc append-only ledgers persisting the
  questions and answers the owner will revisit (added 2026-09-12
  in practice, recorded here 2026-09-14). Division of labor:
  chronology lives HERE; every other doc gets the synthesis.
- **Build plans** for big sub-steps — narrative preamble +
  fine-grained checkbox ledger + an append-only per-session journal
  as the LAST section (the journal backs the ledger's ticks).
- **Retrospectives** after big sub-steps — findings may insert new
  sub-steps into the arc.
- **Handoffs** (`*-handoff.md`) — see below.

Conventions with teeth:

- Settled discussions carry an explicit "**trigger to revisit**" line
  so nobody re-litigates without cause. When enough is settled, the
  content graduates to an ADR or spec; the discussion remains as
  provenance.
- When a discussion's model or plan later meets reality, append a
  dated addendum scoring it — predictions that died die in public,
  with the reason.

## Handoff docs

Compaction-survival dumps written when a session's context is running
out. Canonical shape: where-we-are (30 seconds) · open RIGHT NOW ·
locked decisions (do not relitigate) · fresh gotchas · cold-start
reading order · a **paste-ready re-orientation prompt** (the
most-used part) · optional postscript if reality drifts after the
snapshot.

Handoffs are **ephemeral**: deleted at session close with the owner's
sign-off, once their content lives in the real docs — a lingering
handoff WILL be read as current state by a future session. Once we
have written a good one, exactly one deliberately stale exemplar
(banner on top) is kept as the style template.
