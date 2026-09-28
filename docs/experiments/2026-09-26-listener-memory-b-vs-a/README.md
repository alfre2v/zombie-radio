# Remembering the listener — B (the restatement) against A (conclusions in code), simulated — runlog

**Run:** 2026-09-26, 17:00–17:08 CDT (B, two wordings) and 18:27–18:29
CDT (A, simulated); **folder assembled** the same evening, 18:43–18:50,
at the owner's request ("I don't want us to lose the tests results and
the scripts you have produced").
**Timebox:** for A, the owner's framing: "only a pass that do a quick
evaluation if A is really an interesting option, what it brings as
observed improvements quickly, otherwise we drop it as a quest." About
6 minutes, 3 of them on the box.
**Provenance:** `docs/TODO.md`, Task 6b, step 3.4c.5, check 2 (the
driver test) · `docs/discussions/2026-09-26-show-director-modes.md` §5.1
(the owner's options A and B), §10 item 5 ("Option A (facts extracted
in code) only if a driver test shows B falls short"), §15.9 (the
restatement), §17.12 (the exit criterion: the driver test, "from which
the owner decides whether B is enough") · `docs/follow-ups.md`, "A
listener memory keyed by identity" · the fork TalkWithZombies
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`), branch
`alfre2v/show-slice-3-browser`.

> **Not pre-registered.** The runs were made in the session's
> scratchpad as step 3.4c.5's driver test; this folder was assembled
> afterwards so they would not be lost. No verdict criteria or
> predictions were frozen before the data (the convention of
> `docs/experiments/README.md`); `findings.md` says what was claimed
> before each run, and marks the rows judged by reading.

## The question

Step 3.4c remembers a listener with **option B**: every contact
instruction restates the listener's own words (this contact's, then
the last few earlier contacts'), and one sentence asks the model to
greet a returning voice. **Option A** would have code extract facts
from the words (a name, a place, what they have) and state conclusions
instead. Two questions:

1. Does B do its job, and does a reworded B do better than the first
   wording? (the driver test of check 2)
2. Would A do better — at its best, with a perfect extractor? (A,
   simulated)

## Execution model

As in the earlier experiments: the owner owns the box and the SSH
tunnel; the agent runs from the laptop through the tunnel's local
ports; nothing on the box changes; the box's address never appears in
this folder. Only llama.cpp is used — text only: the driver sends the
listener's words as the transcript, with no TTS and no Whisper. The
fork's dev server runs on the laptop, on `127.0.0.1:8010`, one per
drive. Times CDT.

## Environment

The box as on 2026-09-26 (Hyperstack, one RTX A6000): llama.cpp build
`b11096`, Nemotron Nano 9B v2, reached at `localhost:8080`. The fork's
dev `settings.yaml` in its committed dev state (its `show:` section,
the file's last, holds only `seed: 42`), plus the drive's temporary
lines. The fork sends a seed with every round's request
(`app/services/llm.py:138`), so **a drive replays byte for byte** on
the same box, model and build: the verification drive of entry 10
reproduced all 40 rounds of `a-sim` seed 42, instructions and lines.

## The arms — three columns, one script

| Column | Label | The fork at | What the contact instructions say about the listener |
|---|---|---|---|
| B, old wording | `b-old` | `90ec1e8` (step 3.4c.4) | the listener's words quoted, then "If this voice is one you spoke with before, greet them as a returning friend and use what they told you." |
| B, new wording | `b-new` | `e261b5b` (step 3.4c.5; the working tree at the time, committed unchanged at 17:32) | the words quoted, then "Only a voice that says the name of one of them is someone you spoke with before: greet them as a returning friend and use what they told you. Any other voice is someone new." — five more sentences reworded (the commit's message) |
| A, simulated | `a-sim` | `e261b5b`, with `sim_a.py` swapped in at launch, in memory | conclusions instead of the quotes: "This voice has not said who they are. … Do not guess which one this is.", "This is Maria, a new caller: …", "This is Alfredo, who called before: … Greet them as a returning friend, by name." |

The same in all three: the seeds 42, 7 and 2026; 40 rounds; the
temporary settings (calls at 20–40 s, `interaction_min_s: 20`,
`interaction_max_s: 40`; contacts of exactly 3 answers,
`contact_jitter: 0`); the system prompt (checked identical, entry 10).
The same seed gives the same plans in every column — the same rounds,
speakers, agenda items and tone words — so only the restatement
differs.

**The listener's script** (`run_drive.sh`'s `--heard` items, answering
every round that listens, in order; `-` is a silent window):

1. Contact 1, Alfredo: "Hello? Is anyone there?" · "My name is
   Alfredo." · "I'm in Austin, Texas, and I have a pickup truck." (the
   third answer brings the Breakdown)
2. Contact 2, Maria: "This is Maria, from Dallas." · "We have a doctor
   with us." · "Do you need medicine?"
3. Contact 3, Alfredo back, anonymous at first: "Hello again, lab." ·
   `-` · "It's me, Alfredo, from Austin. I still have the truck." ·
   "Where should I drive?"
4. Contact 4, nobody: `-` · `-` (a re-call, then the Switch-off)

After that the items run out, and every later call goes unanswered.

**A's perfect extractor** is a table in `sim_a.py`: each scripted
sentence and the facts it gives (a name, "in …", "with …", "offering
…", "asking …"); any other words give nothing. A contact's caller is
the first name in its words so far; the known callers are the earlier
contacts that gave a name, their facts merged. `sim_a_server.py`
replaces the director's `_restatement` at launch and wraps the round
route's `plan_round` to hand it the round's words, which the director
does not pass to `_restatement`.

## Files in this folder

- `run_drive.sh` — one drive: `FORK=<the fork> ./run_drive.sh SEED LABEL [sim]`.
- `sim_a.py`, `sim_a_server.py` — option A simulated (above).
- `analyze_contacts.py` — the counted numbers over `raw/`, and
  `transcript-<label>.md` (every contact of every seed).
- `key_rounds.py` — the rounds behind the rows judged by reading
  (Maria's first round, the anonymous voice and the re-call after it,
  Alfredo's return), and the system prompt compared.
- `transcript-b-old.md`, `transcript-b-new.md`, `transcript-a-sim.md`
  — derived by `analyze_contacts.py`.
- `raw/drive-<label>-<seed>.txt` — the driver's output;
  `raw/runs/<run id>/script.json` — the run record: every instruction
  as sent, every line as parsed. Nine drives. The dev server's log
  (`raw/dev-server-8010-<label>-<seed>.log`) stays local — the repo's
  `*.log` rule leaves it out; it holds the server's startup, the round
  requests and the silences, which the run records also hold.
- `findings.md` — the numbers, the readings, the verdict.

## Reproduction recipe — THE section to follow

1. **The fork at the column's commit** (the table above), its tree
   clean; its dev `settings.yaml` ending with a `show:` section that
   holds only `seed: 42` (`run_drive.sh` checks, backs the file up,
   and restores it after the drive, even on failure).
2. **The tunnel** (the owner's), then the probe; anything but 200 on
   `localhost:8080`, stop:

   ```bash
   for u in localhost:8080/health localhost:8001/capabilities localhost:8002/docs; do printf '%s ' "$u"; curl -s -m 3 -o /dev/null -w '%{http_code}\n' "$u"; done
   ```

3. **The drives**, from this folder, with a **new label** — the
   committed `raw/` files are the record, and `run_drive.sh` refuses to
   overwrite them:

   ```bash
   export FORK=/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies
   for seed in 42 7 2026; do ./run_drive.sh $seed b-new-rerun; done        # the fork at e261b5b
   for seed in 42 7 2026; do ./run_drive.sh $seed a-sim-rerun sim; done    # the fork at e261b5b
   ```

   About a minute a drive. Each writes `raw/drive-<label>-<seed>.txt`,
   the server's log, and a copy of the run record under `raw/runs/`.
4. **The numbers and the readings:**

   ```bash
   for l in b-old b-new a-sim; do python3 analyze_contacts.py $l; done
   python3 key_rounds.py
   ```

   `key_rounds.py` reads the three committed columns; for a rerun,
   change its `LABELS`.

## Runlog

*Append-only. The commands as run, with their output; the
scratchpad's path shortened to `<scratch>/`. The scratchpad's labels
were `before` (now `b-old`) and `after` (now `b-new`); the files were
renamed when copied here in entry 10, their contents unchanged. The
scratch versions of the scripts differ from this folder's only in
their paths (entry 10).*

### 2026-09-26 17:00 CDT — Entry 1: the probe, and three drives with the old wording

The fork at `90ec1e8`, its tree clean. `run_drive.sh` written in the
scratchpad (the drive script of this folder, with the scratchpad's
paths and a fixed settings backup).

```bash
for u in localhost:8080/health localhost:8001/capabilities localhost:8002/docs; do printf '%s ' "$u"; curl -s -m 3 -o /dev/null -w '%{http_code}\n' "$u"; done
```

```
localhost:8080/health 200
localhost:8001/capabilities 200
localhost:8002/docs 200
```

```bash
S=<scratch>; chmod +x $S/run_drive.sh; for seed in 42 7 2026; do $S/run_drive.sh $seed before; done; lsof -nP -iTCP:8010 -sTCP:LISTEN -t || echo "port 8010: nothing listening"; tail -3 $S/drive-3.4c.5-before-42.txt
```

```
drive exit 0 -> drive-3.4c.5-before-42.txt
settings.yaml restored
drive exit 0 -> drive-3.4c.5-before-7.txt
settings.yaml restored
drive exit 0 -> drive-3.4c.5-before-2026.txt
settings.yaml restored
port 8010: nothing listening

40 rounds · 92 lines · 0 dropped · average round 1.11s · script after the last round: 6290 tokens
record: runs/2026-09-26T17-00-46/script.json
```

### 17:03 CDT — Entry 2: the numbers, old wording

`analyze_contacts.py` written (this folder's, without the last measure
of entry 7).

```bash
cd <scratch> && python3 analyze_contacts.py before
```

```
driver test (before), seeds [42, 7, 2026]:
  alfredo named after he gave it: 4 of 6
  maria named: 5 of 9
  alfredo named on his return: 4 of 12
  the return recalls Alfredo, Austin or the truck: 0 of 3
  exchanges ending on a question: 7 of 18
  sign-on tells the receiver facts: 1 of 3
  orientation repeats tell them: 0 of 0
  lines with markdown emphasis: 14
  seed 42: 7 calls; the unanswered ones: repair → re-call → switch-off; repair → re-call → switch-off; repair → re-call → switch-off; repair → re-call → switch-off; events inside a contact: 0
  seed 7: 7 calls; the unanswered ones: repair → re-call → switch-off; repair → re-call → switch-off; repair → re-call → switch-off; repair → re-call → switch-off; events inside a contact: 0
  seed 2026: 7 calls; the unanswered ones: repair → re-call → switch-off; repair → re-call → switch-off; repair → re-call → switch-off; repair → re-call → switch-off; events inside a contact: 0
transcript: driver-test-before.md
```

### 17:04–17:05 CDT — Entry 3: the wording pass

Six sentences of the fork's `app/show/director.py` reworded by the
agent, and the tests with them (three small scripts, 17:04:38–17:05:21);
left uncommitted for the owner's review. They were committed unchanged
at 17:32 as `e261b5b`: no tool touched the director between entry 4's
drives and that commit (checked in the session's transcript).

### 17:05 CDT — Entry 4: the probe, three drives with the new wording, the numbers

```bash
for u in localhost:8080/health localhost:8001/capabilities localhost:8002/docs; do printf '%s ' "$u"; curl -s -m 3 -o /dev/null -w '%{http_code}\n' "$u"; done
```

```
localhost:8080/health 200
localhost:8001/capabilities 200
localhost:8002/docs 200
```

```bash
S=<scratch>; for seed in 42 7 2026; do $S/run_drive.sh $seed after; done; lsof -nP -iTCP:8010 -sTCP:LISTEN -t || echo "port 8010: nothing listening"; cd $S && python3 analyze_contacts.py after
```

```
drive exit 0 -> drive-3.4c.5-after-42.txt
settings.yaml restored
drive exit 0 -> drive-3.4c.5-after-7.txt
settings.yaml restored
drive exit 0 -> drive-3.4c.5-after-2026.txt
settings.yaml restored
port 8010: nothing listening
driver test (after), seeds [42, 7, 2026]:
  alfredo named after he gave it: 4 of 6
  maria named: 6 of 9
  alfredo named on his return: 3 of 12
  the return recalls Alfredo, Austin or the truck: 0 of 3
  exchanges ending on a question: 11 of 18
  sign-on tells the receiver facts: 3 of 3
  orientation repeats tell them: 0 of 0
  lines with markdown emphasis: 10
  seed 42: 7 calls; the unanswered ones: repair → re-call → switch-off; repair → re-call → switch-off; repair → re-call → switch-off; repair → re-call → switch-off; events inside a contact: 0
  seed 7: 7 calls; the unanswered ones: repair → re-call → switch-off; repair → re-call → switch-off; repair → re-call → switch-off; repair → re-call → switch-off; events inside a contact: 0
  seed 2026: 7 calls; the unanswered ones: repair → re-call → switch-off; repair → re-call → switch-off; repair → re-call → switch-off; repair → re-call → switch-off; events inside a contact: 0
transcript: driver-test-after.md
```

### 17:08–17:32 CDT — Entry 5: read, reported, ruled

The transcripts read by the agent and reported to the owner, with a
table whose read rows are corrected in `findings.md`. The owner asked
for the literal prompts and a plain label for each column, then ordered
the new wording committed (`e261b5b`, 17:32) and said: "Do not run the
A simulation yet."

### 18:24 CDT — Entry 6: the owner's order for A

After the compaction, the owner: "I want you to run "b. First run the
A simulation described in handoff §7.2. …" But only a pass that do a
quick evaluation if A is really an interesting option, what it brings
as observed improvements quickly, otherwise we drop it as a quest."
The spec: `docs/discussions/2026-09-26-show-engine-session-handoff-5.md`
§7.2 (an ephemeral handoff; this folder now holds what it specified).

### 18:26 CDT — Entry 7: A built in the scratchpad, and checked with no model

`sim_a.py` and `sim_a_server.py` written (as in this folder);
`run_drive.sh` gained the optional `sim` argument; `analyze_contacts.py`
gained the measure "the anonymous 'Hello again, lab.' asked, not
guessed". Then `sim_a.restatement` replayed over the recorded `b-new`
seed-42 run (`load_run("2026-09-26T17-05-46")`, truncated before each
round the listener spoke in, and this round's words stashed), with the
fork's `.venv/bin/python` from the fork's root:

```
round 4 exchange heard 'Hello? Is anyone there?'
  -> This voice has not said who they are. 
round 5 exchange heard 'My name is Alfredo.'
  -> This is Alfredo, a new caller. 
round 6 breakdown heard "I'm in Austin, Texas, and I have a pickup truck."
  -> This is Alfredo, a new caller: in Austin, Texas, with a pickup truck. 
round 10 exchange heard 'This is Maria, from Dallas.'
  -> This is Maria, a new caller: in Dallas. Callers you knew before: Alfredo, in Austin, Texas, with a pickup truck. 
round 11 exchange heard 'We have a doctor with us.'
  -> This is Maria, a new caller: in Dallas, with a doctor. Callers you knew before: Alfredo, in Austin, Texas, with a pickup truck. 
round 12 breakdown heard 'Do you need medicine?'
  -> This is Maria, a new caller: in Dallas, with a doctor, offering medicine. Callers you knew before: Alfredo, in Austin, Texas, with a pickup truck. 
round 16 exchange heard 'Hello again, lab.'
  -> This voice has not said who they are. Callers you know: Alfredo, in Austin, Texas, with a pickup truck; Maria, in Dallas, with a doctor, offering medicine. Do not guess which one this is. 
round 17 re-call heard None
  -> This voice has not said who they are. Callers you know: Alfredo, in Austin, Texas, with a pickup truck; Maria, in Dallas, with a doctor, offering medicine. Do not guess which one this is. 
round 18 exchange heard "It's me, Alfredo, from Austin. I still have the truck."
  -> This is Alfredo, who called before: in Austin, Texas, with a pickup truck. Greet them as a returning friend, by name. 
round 19 breakdown heard 'Where should I drive?'
  -> This is Alfredo, who called before: in Austin, Texas, with a pickup truck. Greet them as a returning friend, by name. New in this contact: asking where to drive.
```

### 18:27 CDT — Entry 8: the probe, three drives with A

```bash
for u in localhost:8080/health localhost:8001/capabilities localhost:8002/docs; do printf '%s ' "$u"; curl -s -m 3 -o /dev/null -w '%{http_code}\n' "$u"; done
```

```
localhost:8080/health 200
localhost:8001/capabilities 200
localhost:8002/docs 200
```

```bash
bash <scratch>/run_drive.sh 42 a-sim sim; tail -3 <scratch>/drive-3.4c.5-a-sim-42.txt
```

```
drive exit 0 -> drive-3.4c.5-a-sim-42.txt
settings.yaml restored

40 rounds · 93 lines · 0 dropped · average round 1.18s · script after the last round: 5983 tokens
record: runs/2026-09-26T18-27-13/script.json
```

A's wording checked in the record before the other two seeds (rounds
10, 16 and 18 of `2026-09-26T18-27-13`, the first 260 characters):

```
10 exchange A voice on the frequency says: "This is Maria, from Dallas." This is Maria, a new caller: in Dallas. Callers you knew before: Alfredo, in Austin, Texas, with a pickup truck. Speak to the voice directly. Answer what the voice said, then: Find out who the voice
16 exchange A voice on the frequency says: "Hello again, lab." This voice has not said who they are. Callers you know: Alfredo, in Austin, Texas, with a pickup truck; Maria, in Dallas, with a doctor, offering medicine. Do not guess which one this is. Speak to the voice di
18 exchange A voice on the frequency says: "It's me, Alfredo, from Austin. I still have the truck." This is Alfredo, who called before: in Austin, Texas, with a pickup truck. Greet them as a returning friend, by name. Speak to the voice directly. Answer what the voice sai
```

```bash
S=<scratch>; for seed in 7 2026; do bash $S/run_drive.sh $seed a-sim sim; tail -2 $S/drive-3.4c.5-a-sim-$seed.txt; done
```

```
drive exit 0 -> drive-3.4c.5-a-sim-7.txt
settings.yaml restored
40 rounds · 97 lines · 0 dropped · average round 1.26s · script after the last round: 6291 tokens
record: runs/2026-09-26T18-28-12/script.json
drive exit 0 -> drive-3.4c.5-a-sim-2026.txt
settings.yaml restored
40 rounds · 92 lines · 0 dropped · average round 1.21s · script after the last round: 5992 tokens
record: runs/2026-09-26T18-29-04/script.json
```

Then the numbers of all three columns (the scratch `analyze_contacts.py`
with entry 7's measure; the output as in `findings.md`), the fork
checked untouched (`git status --short` empty, `settings.yaml` equal to
its backup, nothing on port 8010), and the key rounds of `b-new` and
`a-sim` read (as `key_rounds.py` prints them). Reported to the owner
at 18:30 as "about 20 minutes": the transcript's times say about 6
(the order at 18:24:54, the report at 18:30:47).

### 18:37 CDT — Entry 9: the ruling

The owner: "We are going to do: "a. B for 3.4c; names-only A becomes a
show fix before the talk, with the follow-up updated."" — and asked
for the scripts and results to be kept; this folder, on the owner's
"Go with the experiment folder, the follow-up and the TODO as
proposed" (18:42).

### 18:43–18:47 CDT — Entry 10: the folder assembled and checked

The nine drives' raw files copied into `raw/` (renamed to the column
labels) with their run records from the fork's `runs/`; the scripts
copied and made folder-relative: `run_drive.sh` takes `FORK` from the
environment, writes into `raw/`, backs the settings up itself
(`mktemp`), refuses an existing label, and copies the run record;
`analyze_contacts.py` reads only `raw/` and writes
`transcript-<label>.md`. `key_rounds.py` added.

This folder's `analyze_contacts.py` against the scratch one, the
numbers compared for each column:

```
b-old: numbers identical to the scratchpad's
b-new: numbers identical to the scratchpad's
a-sim: numbers identical to the scratchpad's
```

`python3 key_rounds.py` — its last lines (the rounds themselves are
quoted in `findings.md`):

```
seed 42: the system prompt identical in the three columns: True
seed 7: the system prompt identical in the three columns: True
seed 2026: the system prompt identical in the three columns: True
```

**The recipe verified:** the probe (200 × 3), then one drive from a
scratch copy of this folder (so `raw/` here stays the record), the fork
at `e261b5b`:

```bash
FORK=/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies <scratch>/exp-copy/run_drive.sh 42 verify sim
```

```
drive exit 0 -> raw/drive-verify-42.txt
record copied -> raw/runs/2026-09-26T18-46-47/script.json
settings.yaml restored
```

```
40 rounds · 93 lines · 0 dropped · average round 1.17s · script after the last round: 5983 tokens
40 40 rounds; rounds whose instruction or lines differ: none
```

The verification drive against `a-sim` seed 42 (`2026-09-26T18-27-13`),
round by round: identical. The dev settings equal their backup,
nothing on port 8010, the fork's tree clean.
