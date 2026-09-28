# Findings — the radio beats reworded

*Interpretation only; the evidence is in `README.md` and `raw/`. Every
count comes from `beats_count.py`. The sections down to "Predictions"
were written before the first drive of the new wording (README, runlog
entry 2).*

## What this run decides

Whether the draft wording of the three receiver beats — the Repair,
the Breakdown and the Switch-off, reworded at the owner's order
("Reword now, before check 4; bring the draft"; "Go with the draft,
including both line-count changes") — makes the cast tell the
listeners what happened to the radio and what it means for them,
before the owner's test by ear (step 3.4c.5, check 4).

## Criteria (written before the new drives)

Measured by `beats_count.py` over three drives of the new wording
(the saved script of `../2026-09-26-listener-memory-b-vs-a`, seeds 42,
7 and 2026, calls at 20–40 s, contacts of exactly 3 answers), against
the committed wording's three drives on the same script and seeds
(`beats_count.py old`):

| Criterion | The committed wording | Passes at |
|---|---|---|
| C1 — the Repair says what it means (the lab can hear them) | 2 of 21 | at least 2 of 3 Repairs |
| C2 — the Breakdown says what it means (the lab cannot hear them; the broadcast goes on) | 3 of 9 | at least 2 of 3 Breakdowns |
| C3 — the Switch-off says the receiver is going off | 5 of 12 | at least 2 of 3 Switch-offs |
| C4 — the Switch-off says what it means | 0 of 12 | at least 2 of 3 Switch-offs |

**Reported, not graded:** each beat says what happened (the Repair 15
of 21, the Breakdown 6 of 9); the Switch-off gives the reason (2 of 12)
and says the opposite, keeping the receiver on (5 of 12); the lines as
read (`beats_count.py LABEL --lines`).

**The verdict and what follows:**

- **PASS** (C1–C4 all met): the new wording goes to the owner's review
  and commit, then check 4.
- **PARTIAL** (some met): the beats that miss get one more look with
  the owner — for the Breakdown, the lever named in the draft: its own
  line count, so each job has a line.
- **FAIL** (none met): back to the committed wording; the discussion
  reopens.

## Caveats (written before the new drives)

- **Keywords, not meaning.** A line can say it in words the patterns
  miss, or match a pattern while saying something else; the counts
  come with the lines (`--lines`), and a reading that disagrees is
  noted, never silently replaces the count.
- **The keyword patterns were widened once**, before this file, after
  reading the committed wording's Switch-offs ("going dark",
  "deactivated" say it goes off), so the baseline above uses the same
  patterns as the new drives.
- **Small sample.** Three seeds, one script: about 21 Repairs, 9
  Breakdowns and 12 Switch-offs a column.
- **The plans differ a little between columns.** The same seed gives
  the same draws for the same round, but the lines change the played
  time, so calls can land on different rounds.

## Predictions (the agent's, registered before the new drives)

- **C1 passes** — the operator's line now carries "the lab can hear
  them now", and the call line already worked.
- **C3 and C4 pass** — each has its own line now, and naming the
  receiver and the transmitter apart should stop "keep it on".
- **C2 is the risk** — the Breakdown draws 2 or 3 lines; with 2, the
  last line carries both the description and the meaning, and may drop
  the meaning. Expected about 60–70 %: a narrow pass or a PARTIAL.

## Results

*Written after the drives (README, runlog entry 3). The counts are
`beats_count.py`'s; "read" is the agent's reading of every beat round's
lines (`beats_count.py new --lines`), stated where it disagrees.*

| Criterion | Committed wording (count) | Draft wording (count) | Draft wording (read) | Met? |
|---|---|---|---|---|
| C1 — the Repair says what it means | 2 of 21 | 20 of 21 | **7 of 21** — 13 say the reverse, "They can hear us now!" | **no** (by reading; the count is wrong) |
| C2 — the Breakdown says what it means | 3 of 9 | 3 of 9 | 5 of 9 say the broadcast goes on or "broadcasting blind"; 2 say the lab cannot hear them | no |
| C3 — the Switch-off says the receiver is going off | 5 of 12 | 8 of 12 | 12 of 12 ("Receiver's off", "Receiver offline" escape the patterns) | **yes** |
| C4 — the Switch-off says what it means | 0 of 12 | 2 of 12 | 7 of 12 say the broadcast goes on; 2 say the lab will not hear anyone | no |

**The count that is wrong — C1.** The pattern's "hear us" accepts the
reverse meaning. Seeds 42 and 7 closed 13 of their 14 Repairs with
Samantha saying "They can hear us now!" (or "again") — the listeners
can hear the lab, which was always true — and one with "They're
listening!"; seed 2026 closed all 7 with "We can hear you now." The
instruction says "Samantha tells anyone listening that the lab can hear
them now"; the model has to turn that into the lab's first person, and
flips it. The pattern is left as frozen; a next pass counts only the
right direction, on every column.

**Reported:**

- **What happened:** the Repair's first line describes the receiver in
  21 of 21 ("The receiver's back, crackling, static, then clear.") —
  but repeats itself: in seed 2026 all seven Repairs are near copies
  ("The receiver's back, crackling, alive. It's like the static was a
  prison…" / "We can hear you now. If you're out there, answer."). The
  Breakdown shows the failure in 7 of 9. Of the three two-line
  Breakdowns, **two (round 19, seeds 42 and 7) dropped the failure
  altogether** and only answered Alfredo's "Where should I drive?"; the
  third (seed 2026, round 6) showed it but did not answer the voice. Of
  the six three-line ones, two did not answer the voice first (seed 7
  round 6, seed 2026 round 19).
- **The Switch-off:** a reason in 11 of 12 by reading (6 by count);
  the opposite ("We'll keep it on.") in 1 of 12, against 5 of 12.
- **The mechanics:** 40 rounds a drive, 0 dropped, 1.26–1.33 s a round.

**Predictions, graded:** C1 predicted to pass — it did not (the
direction flipped). C3 predicted to pass — it did. C4 predicted to pass
— it did not: the model says the broadcast goes on, rarely that the lab
cannot hear. C2 predicted as the risk — it failed, and the two-line
draws failed worst.

## Verdict

**PARTIAL** — C3 met; C1 (by reading), C2 and C4 not. By the rule
above, the beats that miss get one more look with the owner.

What the numbers point at: **the meaning sentences are written from
outside the lab** ("the lab can hear them", "the lab can no longer hear
them", "the lab will not hear anyone") and the model must turn them
into its own first person; it drops them, or flips them. The failure
itself is said when it has a line of its own, and lost when two lines
must carry three jobs.

---

# Round 2 — the meanings in the cast's own words

*At the owner's order after round 1 ("Go with the second pass as
proposed. Then let's stop and re-evaluate if we keep the last state
committed."). The sections down to "Predictions" were written before
the first drive of round 2 (README, runlog entry 4).*

## What changed (the fork, uncommitted, on top of round 1)

- **The meanings as the cast's own words**, to paraphrase — so the
  model need not turn "the lab can hear them" into its first person:
  the Repair's last line, "Last, ‹Samantha› tells anyone listening, in
  their own words: "We can hear you now. Answer us.""; the Breakdown's,
  "…tells them, in their own words: "We can't hear you anymore, but
  we're still on the air.""; the Switch-off's, "…tells them, in their
  own words: "We won't hear you until we switch it back on, but we're
  still on the air.""
- **The Breakdown takes a fixed count**, a new setting
  `breakdown_lines` (3), instead of drawing 2–3 like an exchange — the
  answer, the failure and what it means each have a line.
- **The counting, fixed before these drives** (`beats_count.py`, runlog
  entry 4): the Repair's meaning counts only the lab hearing them
  ("we can hear you"); the Breakdown's and the Switch-off's meaning is
  counted in its two halves — the lab cannot hear them, the lab is
  still on the air; "the receiver's off" and "offline" count as going
  off. The same patterns on every column:

| Measure | The committed wording | Round 1 |
|---|---|---|
| The Repair: the lab can hear them | 2 of 21 | 7 of 21 |
| The Breakdown: the lab cannot hear them | 3 of 9 | 4 of 9 |
| The Breakdown: still on the air | 0 of 9 | 3 of 9 |
| The Switch-off: going off | 5 of 12 | 12 of 12 |
| The Switch-off: the lab cannot hear them | 0 of 12 | 2 of 12 |
| The Switch-off: still on the air | 0 of 12 | 7 of 12 |

## Criteria (written before round 2's drives)

The same script, seeds and settings as round 1; label `new2`.

| Criterion | Passes at |
|---|---|
| C1 — the Repair says the lab can hear them | at least 2 of 3 Repairs |
| C2 — the Breakdown says the lab cannot hear them | at least 2 of 3 Breakdowns |
| C3 — the Switch-off says the receiver is going off | at least 2 of 3 Switch-offs |
| C4 — the Switch-off says the lab cannot hear them | at least 2 of 3 Switch-offs |

**Reported, not graded:** still on the air (the Breakdown, the
Switch-off); what happened (the Repair, the Breakdown); the reason and
the opposite (the Switch-off); by reading — the Breakdown answering the
voice first, and **repetition**: the quoted words copied verbatim round
after round.

**The verdict and what follows:** whatever it is, the owner decides
next whether to commit round 2, keep the committed wording, or go on
(the owner's "stop and re-evaluate"). PASS makes committing round 2 the
agent's recommendation.

## Predictions (the agent's, registered before round 2's drives)

- **C1–C4 all pass.** Quoted first-person words leave nothing to flip,
  and the Breakdown's three fixed lines give the meaning a line of its
  own.
- **The risk is monotony:** the model tends to copy the quoted words
  verbatim, so the same Repair and Switch-off lines may recur in every
  call of a run — already seen in round 1 without quotes.

## Results (round 2)

*Written after the drives (README, runlog entry 5). Counts by
`beats_count.py new2`; "read" where the reading disagrees.*

| Criterion | Committed wording | Round 1 | Round 2 (count) | Round 2 (read) | Met? |
|---|---|---|---|---|---|
| C1 — the Repair: the lab can hear them | 2 of 21 | 7 of 21 | 21 of 21 | 21 of 21 | **yes** |
| C2 — the Breakdown: the lab cannot hear them | 3 of 9 | 4 of 9 | 4 of 9 | 4 of 9 — the count's seed 7 round 19 is "If you can't hear us" (the reverse); seed 7 round 12's "we just lost you" says it | no |
| C3 — the Switch-off: going off | 5 of 12 | 12 of 12 | 12 of 12 | 12 of 12 | **yes** |
| C4 — the Switch-off: the lab cannot hear them | 0 of 12 | 2 of 12 | 0 of 12 | 0 of 12 | no |

**Reported:**

- **The Repair copies the quote verbatim:** all 21 calls close with
  "We can hear you now. Answer us."; the first line repeats too
  ("crackling like a dying star. We think it's fixed." twice in seed
  42).
- **The Breakdown, now always three lines:** the failure in 7 of 9 —
  round 19 lost it again in seeds 42 and 7 (the cast answered "Where
  should I drive?" instead); the quoted meaning, said word for word by
  Samantha, in each seed's first Breakdown (round 6) and never after;
  still on the air 3 of 9 (those three). The voice answered first in 4
  of 9 (seed 42 rounds 12 and 19, seed 7 round 19, seed 2026 round 12);
  the round-6 Breakdowns and seed 2026's round 19 open on the smoke.
- **The Switch-off:** the quoted words never appear. The model keeps
  "switch it back on" ("We'll flip it back on when we spot a signal.",
  "We'll turn it back on when we've got a better signal.") and drops
  the rest; still on the air 0 of 12 by reading (the count's 1 is "no
  point broadcasting into the void", the reverse) — against 7 of 12 in
  round 1. A reason in 10 of 12 by reading; the opposite ("We'll keep
  the line open as long as we can.") 1 of 12. Seed 2026's four
  Switch-offs are near copies ("Switching it off, this receiver's a
  relic…" / "No one's coming.").
- **The mechanics:** 40 rounds a drive, 0 dropped, 1.31–1.36 s a round.

**Predictions, graded:** C1 and C3 passed as predicted; C2 and C4
failed — predicted to pass. The predicted risk, monotony, came true for
the Repair's call.

## Verdict (round 2)

**PARTIAL** — C1 and C3 met, C2 and C4 not. Against the committed
wording, round 2 is better on the Repair (2 → 21 of 21 saying the lab
hears them) and on the Switch-off going off (5 → 12 of 12, the opposite
5 → 1), and no worse on the rest; against round 1, better on the
Repair, worse on the Switch-off's "still on the air" (7 → 0 of 12).

What the lines suggest (reasoning, not measured): the quoted words are
said when a **named, pinned speaker** owns them — the Repair's
Samantha, pinned last — and in the first Breakdown, where Samantha
happened to close; where the instruction says only "the last line tells
them", the second speaker says something of their own. By the rule
above, the owner decides next.

**The owner's decision:** keep round 2 — committed as the fork's
`3c4154c`; the missing "we can't hear you" goes to the test by ear.
