# decisions/ — Architecture Decision Records

Reserved for decisions with real tradeoffs, hard to reverse, or that
shape future code. Not every choice deserves one — **ask the owner
before drafting**. Immutable once accepted: corrections happen via a
dated annotation note or a superseding ADR, never by rewriting.
Immediately before an ADR is frozen, give it a "truth audit" re-read —
stale claims WILL have crept in during the build.

Filenames: `NNNN-short-slug.md`, zero-padded, monotonically
increasing (e.g. `0001-adopt-pipecat-for-voice-pipeline.md`).

Format:

```markdown
# Title (verb-noun, e.g. "Adopt X for Y")
**Date:** YYYY-MM-DD
**Status:** draft | accepted | superseded by ADR-NNNN | deprecated

## Context      <- the problem/constraint that forced a choice
## Decision     <- what we chose
## Consequences <- what it costs, what it buys; call out reversibility
```
