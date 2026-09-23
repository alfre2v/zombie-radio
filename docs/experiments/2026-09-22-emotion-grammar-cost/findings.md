# Emotion field in the screenplay grammar — findings

**Status:** E1 **PASS** (0.5 %), the sanity check held, written
2026-09-22 and awaiting the owner's review; the folder seals once he
accepts it. The criteria and predictions were committed in `29ead5d`
at 19:15:28 CDT, before the first request of this run (19:15:33).
This run informs the owner's decision on the emotion field; it does
not take it. Interpretation only; the evidence lives in `README.md`
(recipe + runlog, entries 3–6) and `raw/`.

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

*Everything below comes from the runlog — entries 3 to 6, which
carry the scripts' output verbatim. Times are the laptop's (CDT).*

### The run in one paragraph

Two streamed requests at 19:15, then fifty-one plain ones between
19:15:53 and 19:17:25, on the same box and model as the ADR-0003
gate an hour and a half earlier. The emotion field turned out to be
cheap and well used whenever the prompt explained it — and noticeably
more expensive when it did not. That difference is the real finding
of the evening: a grammar costs almost nothing when it agrees with
the model, and about a tenth more per token when it has to overrule
it.

### The sanity check — the grammar binds

Every line written under the emotion grammar carried a legal tag:
both streamed requests, and all 120 probe lines of D-forced,
D-aligned and D-aligned-live. No tag outside the list, no line
without one. The numbers below are therefore about a grammar that
was really in force.

### E1 — the shipping cost is negligible

With the taught prompt and the tagged history, the median cost of a
generated token was 11.263 ms without the grammar (D-aligned-off)
and 11.316 ms with it (D-aligned): `O` = **0.5 %**, far inside the
10 % line. And as in run 1, the comparison is on identical output:
D-aligned wrote the same text as D-aligned-off in all ten rounds
(`check_outputs.py`). Once the prompt teaches the tags, the grammar
does not change a word — it is insurance, and it costs almost
nothing to carry.

### E2 — the steering cost is real

With the plain prompt, which never mentions emotions, the emotion
grammar has to insert a tag the model did not intend on every line.
The median cost per token rose from 11.269 ms (D-simple) to 12.444
ms (D-forced): `O` = **10.4 %**. It was not a fluke of one round:
D-forced's cost sat between 12.38 and 12.54 ms in every one of the
ten. The model also wrote a different amount — 89 to 127 tokens a
round against D-simple's 73 to 127 — which the per-token median
absorbs.

Forcing also touched the style, but less than it first seemed. In
round 1, where the history is still empty, the model answered the
forced tags by turning its lines into quoted dialogue:

> `Daniel (calm): "Lights flickered east wing, no further reports. Over."`

— all four lines of that round, the same four as the streamed
request. From round 2 on, with plain lines in the history to copy,
the quotation marks disappeared, although the tag was still forced
on every line. The examples in the context outweighed the pull of
the forced tokens.

### E3 — once taught, the model tags on its own

With the taught prompt and no grammar at all, **40 of 40** lines of
D-aligned-off carried a legal tag. The grammar in D-aligned then had
nothing left to correct — hence the identical text above.

### E4 — varied emotions, no collapse

| Arm | Distinct emotions | Most frequent | Never used |
|---|---|---|---|
| D-forced | 8 of 9 | `calm`, 32 % | `afraid` |
| D-aligned (and D-aligned-off) | 8 of 9 | `terrified`, 20 % | `happy` |
| D-aligned-live | 8 of 9 | `sad`, 18 % | `happy` |

Even unprompted, the forced model spread its choices over eight
emotions. Taught, it spread them further and never once reached for
`happy` in a zombie outbreak. Whether the chosen emotions fit their
lines is a listening question for the audition; the counts show only
that the field is being used, not parroted.

### Time, cache and reproducibility

Every arm's median prompt time per round was 356–362 ms and its reuse
reached 88 % by round 10, as in run 1; D-aligned-live's reuse climbed
from 54 % in round 2 to 88 %. The taught prompts were larger — 1,790
tokens by round 10 against D-simple's 1,550 — too little to show in
the times. D-simple wrote
the same text as run 1's D-on in all ten rounds, eighty minutes
later: on this box, same request and seed give the same words.

One cost that is not in the table: the forced streamed request — the
first in over an hour, arriving at a slot that still held run 1's
last conversation — waited 1,850 ms for its first chunk, though its
prompt phase took 365 ms. Most likely it is the state swap of run 1's
arm A, met once more (not checked in the server log).

### Where the model forgot "Over."

In 200 lines, seven did not end in "Over.": the four quoted lines of
D-forced's round 1 (`Over."`), one plain omission in D-forced's round
6, and one line that hands over mid-sentence, written identically in
D-aligned-off and D-aligned — *"We need supplies, but the truck line’s
full. Over to logistics—anyone got spare meds or fuel?"*

### Predictions, graded

**Agent:**

- *E1 PASS, under 10 %* — **survived** (0.5 %).
- *E2 small in compute, under 10 %* — **died**, narrowly (10.4 %).
  The reasoning behind it — that forcing changes which token wins
  but not how much the checking costs — was wrong; the likely
  reason is in the addendum to the lessons discussion.
- *E2, forced tags collapse onto one or two values* — **died**. The
  model spread its forced choices over eight emotions, the top one
  at 32 %.
- *E3, at least 90 % tagged when taught* — **survived** (100 %).
- *E4, at least four distinct, top under 50 % when taught* —
  **survived** (eight distinct, top 20 %).
- *Time and cache unchanged; D-simple reproduces run 1's D-on* —
  **survived**, both.

**Owner:** declined to predict.

### The side quest, in one line

Typographic `’` and `—` in a line make the TTS drop the pause before
"Over." (owner's ear; those clips are 0.64 s shorter); the ellipsis
does no harm (runlog entry 5).

## Verdict

**E1 — PASS.** The emotion field is affordable in the configuration
the fork would ship: taught in the cast sheet and carried in the
history, it costs 0.5 % per token and the model uses it on every
line with eight of the nine emotions. It stays a live option for the
fork's grammar builder, with this cost quoted when the owner decides.

What the reported numbers add to that decision:

- **Always teach what the grammar enforces.** Imposed on a prompt
  that does not describe it, the same grammar cost 10.4 % per token
  and, with no examples to follow, changed the way the model wrote.
  In the fork this applies to every constraint the director puts in
  the grammar — the emotion tag, but also a narrowed speaker list or
  a one-line budget: each must be said in the directive as well.
- **The field is used, not parroted** — eight emotions in every arm,
  none dominating.
- **The TTS side must normalize typographic punctuation** before
  synthesis (side quest). This holds with or without the emotion
  field.

Not decided here: whether to adopt the field (the owner's call); the
prose quality with and without tags and whether the chosen emotions
fit their lines (the Task 5a audition); how the voice expresses an
emotion — reference clips or engine knobs (seam question S6, fork
work after Task 4).
