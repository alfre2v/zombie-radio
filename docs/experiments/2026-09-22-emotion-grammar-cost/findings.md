# Emotion field in the screenplay grammar — findings

**Status:** DRAFT — criteria and predictions to be committed before
the first request of this run. Interpretation only; the evidence
lives in `README.md` (recipe + runlog) and `raw/`.

## What this run decides

Whether an emotion field in the screenplay grammar — every line
written as `Name (emotion): text`, the emotion one of nine — is
affordable for TalkWithZombies. It does not adopt the field: that
stays the owner's decision (`docs/follow-ups.md`, "Emotion field in
the screenplay grammar"), made with these numbers and, for prose
quality, the Task 5a audition.

## Criteria (pre-registered)

Every number named below is printed by a committed script over the
raw files: `summarize_timings.py` for times, `check_outputs.py` for
what the model wrote, `parse_stream.py` for the streamed requests.

### E1 — the shipping cost (graded)

*Quantity.* The median generation cost per token (`predicted_ms /
predicted_n` per round, median over the ten rounds) of **D-aligned**
against **D-aligned-off** — the same taught prompt and tagged
history, with and without the emotion grammar: `O = (D-aligned −
D-aligned-off) / D-aligned-off`.

- **PASS** — `O ≤ 10 %`.
  → **Consequence:** the emotion field is affordable; it stays a live
  option for the fork's grammar builder, and its cost is quoted
  when the owner decides.
- **PARTIAL** — `10 % < O ≤ 25 %`.
  → **Consequence:** affordable with the cost noted in the decision
  and in the fork's latency budget.
- **FAIL** — `O > 25 %`.
  → **Consequence:** before adopting it, try a lighter form — an
  optional tag, or a shorter list — and measure again.

### Sanity check — the grammar binds (stop condition, not a grade)

Under the emotion grammar (D-forced, D-aligned, D-aligned-live and
both streamed requests), every line must carry a legal tag. If any
line does not, the grammar was not applied, the other numbers are
meaningless, and the run stops to find out why.

### Reported, not graded

- **E2 — the steering cost.** The same quantity for **D-forced**
  against **D-simple**: the same plain prompt, the emotion grammar
  against the simple one. Here the grammar must insert tags the
  prompt never asked for — the case run 1 could not measure.
- **E3 — willing compliance.** In **D-aligned-off** (taught, no
  grammar), the share of lines that carry a legal tag. High means the
  grammar is a guarantee in the shipping configuration; low means it
  steers.
- **E4 — variety.** Per arm, the emotions used, how many distinct,
  and the share of the most frequent one — the "every line is
  *afraid*" indicator.
- **Time and cache.** Per arm: median prompt time and wall time per
  round, reuse at round 10; D-aligned-live's reuse per round. Set
  beside run 1's D-on.
- **Reproducibility.** Whether D-simple writes the same text as run
  1's D-on, request for request (the requests are byte-identical,
  runlog entry 2).

## Caveats, written before the data

1. **The fixed script's emotions were chosen by the agent** (ten
   `calm`, seven `afraid`, six `urgent`, five `doubtful`, three each
   `happy`, `sad`, `exhausted`, two `angry`, one `terrified`). In the
   taught arms the model sees them as examples, so E3 and E4 are
   partly shaped by that choice.
2. **Round 1 has no examples.** In the taught arms, round 1's history
   is empty: its compliance comes from the instruction alone, later
   rounds from the instruction plus tagged examples.
3. **A small inconsistency in the taught cast sheet.** It says
   "nothing else in parentheses" while Ralph's own description reads
   "counts things (doors, cans, shamblers)" (inherited from run 1's
   cast sheet). The emotion grammar forbids parentheses in the spoken
   text anyway.
4. **Per-token costs are compared across different text.** Except for
   D-simple, each arm writes its own words; the per-token median
   absorbs length, but not everything (context length also differs
   slightly with tagged history).
5. **One box, one seed, ten rounds** — as in run 1.

## Predictions (registered before the run)

**Agent (Claude, registered 2026-09-22):**

- **E1: PASS**, `O` under 10 %. The mask cost is per token and
  small; the tags add a handful of structural tokens per line.
- **E2: small in compute too** (under 10 %): forcing changes which
  token wins, not how much the checking costs. The visible effect
  will be in the text — with nothing in the prompt about emotions,
  I expect the forced tags to collapse onto one or two values
  (most frequent at or above 50 %).
- **E3: high** — at least 90 % of D-aligned-off's lines carry a legal
  tag. The model followed the simple format perfectly in run 1, and
  here it is told the format and shown it.
- **E4: in the taught arms, at least four distinct emotions**, the
  most frequent under 50 %.
- **Time and cache:** unchanged from run 1 within noise; D-simple
  writes the same text as run 1's D-on in all ten rounds.

**Owner (Alfredo):** declined to register a prediction (2026-09-22)
— noted so the slot is closed, not forgotten.

## Results

*Filled only from README evidence after the run.*

## Verdict

*After Results.*
