# The radio beats reworded — do the cast tell the listeners what happened to the radio? — runlog

**Created:** 2026-09-26, 19:24 CDT, before the first drive of the new
wording; **run** the same evening.
**Timebox:** about 45 minutes, 5 of them on the box.
**Provenance:** `docs/TODO.md`, Task 6b, step 3.4c.5 (between check 3,
the fake microphone, and check 4, the owner by ear) ·
`docs/discussions/2026-09-26-show-director-modes.md` §14.13 (the
receiver story: the Repair, the Breakdown, the Switch-off — "up to two
lines", changed here at the owner's order) ·
`../2026-09-26-listener-memory-b-vs-a/` (the driver-test script, and
the committed wording's drives, the baseline) · the fork TalkWithZombies
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`), branch
`alfre2v/show-slice-3-browser`.

## The question

After check 3 the owner: "It is very annoying that the LLM does not
explain what is going on with the radio. … We will have to reword the
instructions in those special rounds to explain to the LLM to describe
what just occured with the radio in detail for the listeners which
cannot see it." The committed wording's beats rarely say what the
change means for the listeners (the Repair 2 of 21, the Breakdown 3 of
9, the Switch-off 0 of 12), and the Switch-off often says the opposite
of what happens ("We'll keep it on until dawn."). Does the draft
wording fix it?

## Execution model

As in `../2026-09-26-listener-memory-b-vs-a/` (its "Execution model"):
the owner's box and tunnel, text only through llama.cpp at
`localhost:8080`, the fork's dev server on `127.0.0.1:8010` for each
drive, no box address in this folder. Times CDT.

## The arms — two columns, one script

| Column | Label | The fork at | The three beats |
|---|---|---|---|
| The committed wording | `old` | `e261b5b` | the drives `b-new` of `../2026-09-26-listener-memory-b-vs-a/raw/` (17:05–17:08), read in place |
| The draft wording | `new` | `e261b5b` plus the uncommitted change of 19:19–19:24 (`app/show/director.py`, `app/config.py`'s comment, the tests, the runbooks) | run here |

**The draft, in short** (the director's text; ‹…› is filled in):

- **Repair** (`beat_max_lines` lines, 2 — before: a literal 2 in the
  code; the operator pinned last): "Something happens that the
  listeners cannot see: the lab has fixed the receiver, the part of the
  radio that hears. ‹The receiver crackles back to life.› First,
  ‹Daniel, Moira or Ralph› tells the listeners on air, in detail, what
  just happened to the receiver: what they see and hear. Last,
  ‹Samantha› tells anyone listening that the lab can hear them now, and
  asks them to answer." After a Switch-off: "…the lab switches the
  receiver, the part of the radio that hears, back on."
- **Breakdown** (2–3 lines, drawn): "The first line answers what the
  voice just said, speaking to them directly. Then something happens
  that the listeners cannot see: ‹Smoke pours from the receiver, and it
  goes dead.› The second line tells the listeners on air, in detail,
  what is happening to the receiver: what they see and hear. The last
  line tells them what it means for them: the lab can no longer hear
  them, but the transmitter still works, so the broadcast goes on while
  they fix the receiver." With two lines, the last line tells both.
- **Switch-off** (exactly `beat_max_lines` lines, 2 — before: up to 2;
  the caller pinned first): "Nobody answered the call. First,
  ‹Samantha› tells the listeners on air that the lab is switching the
  receiver off now, and why: to save power, or to spare the fragile
  receiver for a time when someone is more likely to be listening. The
  last line tells them what it means for them: the lab will not hear
  anyone until the receiver is back on, but the transmitter stays on,
  so the broadcast goes on." Inside a contact it opens "The voice is
  gone. First, ‹Moira› tells the listeners on air that the lab has lost
  them and is switching the receiver off now, and why: …"

Everything else as in the baseline: the listener's script, seeds 42, 7
and 2026, 40 rounds, calls at 20–40 s, contacts of exactly 3 answers
(`contact_jitter: 0`).

## Files in this folder

- `run_drive.sh` — copied unchanged from
  `../2026-09-26-listener-memory-b-vs-a/` (its `sim` argument unused
  here): `FORK=<the fork> ./run_drive.sh SEED LABEL`.
- `beats_count.py` — the counts; `--lines` prints every beat round's
  lines. `old` reads the baseline in place.
- `raw/` — each drive's output and a copy of its run record (the
  server's log stays local: the repo's `*.log` rule).
- `findings.md` — the criteria, caveats and predictions, written before
  the new drives; the results and the verdict after.

## Reproduction recipe — THE section to follow

1. The fork at `3c4154c` (round 2's wording, the one kept; round 1's
   was never committed — `findings.md` quotes it); its dev
   `settings.yaml` ending with `show:` and `seed: 42` only.
2. The tunnel, then the probe (anything but 200 on `localhost:8080`,
   stop):

   ```bash
   for u in localhost:8080/health localhost:8001/capabilities localhost:8002/docs; do printf '%s ' "$u"; curl -s -m 3 -o /dev/null -w '%{http_code}\n' "$u"; done
   ```

3. The drives, with a new label (the committed `raw/` files are the
   record):

   ```bash
   export FORK=/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies
   for seed in 42 7 2026; do ./run_drive.sh $seed new2-rerun; done
   ```

4. The counts:

   ```bash
   python3 beats_count.py old; python3 beats_count.py new
   ```

## Runlog

*Append-only.*

### 2026-09-26 19:11–19:19 CDT — Entry 1: the ask, the baseline, the draft, the order

After check 3 (the fork's run `2026-09-26T18-59-43`), the owner asked
for the beats to be reworded, "before check 4". The agent counted the
committed wording's beats with an early version of `beats_count.py` (the
three `b-new` drives plus check 3's run), read the Switch-offs, and
drafted the three instructions; the owner: "Go with the draft,
including both line-count changes" (19:19).

### 19:19–19:24 CDT — Entry 2: the change built; this folder, before any new drive

The fork: `_repair`, `_breakdown`, `_switch_off` reworded; the Repair's
line count read from `beat_max_lines`; the Switch-off takes exactly
`beat_max_lines` lines; the one-line forms (a setting of 1, or a cast
of one) worded too. Tests: the pinned wordings updated, five new
(the Repair at 1 and 3 lines, the Breakdown at 2 and 1, the one-line
Switch-off). Checks:

```
1087 passed, 1 warning
test_persona_form ℹ pass 17 ℹ fail 0
test_tts_settings ℹ pass 91 ℹ fail 0
test_show_page ℹ pass 34 ℹ fail 0
```

(the warning: `starlette.testclient`'s deprecation of `httpx`, a
library's, not this change's). No line over 120 characters, no en
dash, in the changed files.

This folder: `beats_count.py` with its Switch-off patterns widened
after reading ("going dark", "deactivated"), and the baseline counted
on the three `b-new` drives only:

```bash
python3 beats_count.py old
```

```
radio beats (old), seeds [42, 7, 2026]:
  repair: 21 rounds · says what happened 15 · says what it means 2
  breakdown: 9 rounds · says what happened 6 · says what it means 3
  switch-off: 12 rounds · says what happened 5 · says what it means 0 · why 2 · the opposite (keep it on) 5
```

`findings.md`'s criteria, caveats and predictions written.

### 19:24 CDT — Entry 3: the probe, three drives of the draft wording, the counts

```bash
for u in localhost:8080/health localhost:8001/capabilities localhost:8002/docs; do printf '%s ' "$u"; curl -s -m 3 -o /dev/null -w '%{http_code}\n' "$u"; done
```

```
localhost:8080/health 200
localhost:8001/capabilities 200
localhost:8002/docs 200
```

```bash
export FORK=/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies && for seed in 42 7 2026; do ./run_drive.sh $seed new; grep '^[0-9]* rounds' raw/drive-new-$seed.txt; done; lsof -nP -iTCP:8010 -sTCP:LISTEN -t || echo "port 8010: nothing listening"; cmp $FORK/settings.yaml <scratch>/settings.yaml.before-trim && echo "dev settings equal the backup"; python3 beats_count.py new
```

```
drive exit 0 -> raw/drive-new-42.txt
record copied -> raw/runs/2026-09-26T19-24-39/script.json
settings.yaml restored
40 rounds · 91 lines · 0 dropped · average round 1.26s · script after the last round: 7463 tokens
drive exit 0 -> raw/drive-new-7.txt
record copied -> raw/runs/2026-09-26T19-25-31/script.json
settings.yaml restored
40 rounds · 98 lines · 0 dropped · average round 1.31s · script after the last round: 7535 tokens
drive exit 0 -> raw/drive-new-2026.txt
record copied -> raw/runs/2026-09-26T19-26-25/script.json
settings.yaml restored
40 rounds · 92 lines · 0 dropped · average round 1.33s · script after the last round: 7583 tokens
port 8010: nothing listening
dev settings equal the backup
radio beats (new), seeds [42, 7, 2026]:
  repair: 21 rounds · says what happened 21 · says what it means 20
  breakdown: 9 rounds · says what happened 7 · says what it means 3
  switch-off: 12 rounds · says what happened 8 · says what it means 2 · why 6 · the opposite (keep it on) 1
```

Then every beat round read (`python3 beats_count.py new --lines`): the
Repair's count is wrong — 13 of its 20 say "They can hear us now!", the
reverse meaning, which the pattern's "hear us" accepts. The results and
the verdict (PARTIAL) in `findings.md`.

### 19:31–19:34 CDT — Entry 4: round 2 — the counting fixed, the second draft built, before any drive

The owner (19:31): "Go with the second pass as proposed. Then let's stop
and re-evaluate if we keep the last state committed."

**The counting, first.** `beats_count.py` rewritten: the Repair's
meaning counts only "we can hear you" (round 1's "hear us" took the
reverse); the Breakdown's and the Switch-off's meaning is counted as
two halves ("cannot hear", "on air"); "the receiver's off" and
"offline" count as going off. Round 1's counts with round 1's patterns
stay quoted in entry 3. Recounted:

```
radio beats (old), seeds [42, 7, 2026]:
  repair: 21 rounds · happened 15 · hears them 2
  breakdown: 9 rounds · happened 6 · cannot hear 3 · on air 0
  switch-off: 12 rounds · happened 5 · cannot hear 0 · on air 0 · why 2 · the opposite 5
radio beats (new), seeds [42, 7, 2026]:
  repair: 21 rounds · happened 21 · hears them 7
  breakdown: 9 rounds · happened 7 · cannot hear 4 · on air 3
  switch-off: 12 rounds · happened 12 · cannot hear 2 · on air 7 · why 6 · the opposite 1
```

(These agree with entry 3's reading: the Repair 7 of 21 in the right
direction; the Switch-off 12 of 12 going off.)

**The fork.** The three meanings given as the cast's own words to
paraphrase; the Breakdown's lines from a new setting, `breakdown_lines`
(3), instead of the exchange's 2–3; the tests (the pinned wordings, the
new setting's default, override and bound); `show-driver.md` lists the
setting. Checks:

```
1088 passed, 1 warning
test_persona_form ℹ pass 17 ℹ fail 0
test_tts_settings ℹ pass 91 ℹ fail 0
test_show_page ℹ pass 34 ℹ fail 0
```

No new line over 120 characters (the nine long lines of
`show-driver.md` are its log excerpts, the same at `HEAD`), no en dash.
`findings.md`'s round 2 criteria and predictions written.

### 19:34 CDT — Entry 5: round 2 — the probe, three drives, the counts

```bash
for u in localhost:8080/health localhost:8001/capabilities localhost:8002/docs; do printf '%s ' "$u"; curl -s -m 3 -o /dev/null -w '%{http_code}\n' "$u"; done
```

```
localhost:8080/health 200
localhost:8001/capabilities 200
localhost:8002/docs 200
```

```bash
export FORK=/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies && for seed in 42 7 2026; do ./run_drive.sh $seed new2; grep '^[0-9]* rounds' raw/drive-new2-$seed.txt; done; lsof -nP -iTCP:8010 -sTCP:LISTEN -t || echo "port 8010: nothing listening"; cmp $FORK/settings.yaml <scratch>/settings.yaml.before-trim && echo "dev settings equal the backup"; python3 beats_count.py new2
```

```
drive exit 0 -> raw/drive-new2-42.txt
record copied -> raw/runs/2026-09-26T19-34-31/script.json
settings.yaml restored
40 rounds · 92 lines · 0 dropped · average round 1.33s · script after the last round: 7480 tokens
drive exit 0 -> raw/drive-new2-7.txt
record copied -> raw/runs/2026-09-26T19-35-26/script.json
settings.yaml restored
40 rounds · 98 lines · 0 dropped · average round 1.31s · script after the last round: 7491 tokens
drive exit 0 -> raw/drive-new2-2026.txt
record copied -> raw/runs/2026-09-26T19-36-20/script.json
settings.yaml restored
40 rounds · 93 lines · 0 dropped · average round 1.36s · script after the last round: 7567 tokens
port 8010: nothing listening
dev settings equal the backup
radio beats (new2), seeds [42, 7, 2026]:
  repair: 21 rounds · happened 21 · hears them 21
  breakdown: 9 rounds · happened 8 · cannot hear 4 · on air 3
  switch-off: 12 rounds · happened 12 · cannot hear 0 · on air 1 · why 4 · the opposite 1
```

Then every beat round read (`python3 beats_count.py new2 --lines`); the
results and the verdict (PARTIAL) in `findings.md`. Stopped here, as
the owner asked, to decide what to keep.

### 19:43 CDT — Entry 6: kept and committed

The owner kept round 2 and ordered "commit the fork, then commit
zombie-radio": the fork's `3c4154c` carries round 2's wording.
