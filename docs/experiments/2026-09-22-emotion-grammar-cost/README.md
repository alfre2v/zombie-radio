# Emotion field in the screenplay grammar — what it costs — runlog

**Created and run:** 2026-09-22 (same evening and same box as the
ADR-0003 gate).
**Timebox:** tonight. Building the folder may take up to about 1.5
hours from 19:00 CDT; past that, the box is destroyed and this run
folds into the Task 5a audition. The box is destroyed at the end of
the evening whatever the state.
**Provenance:** `docs/follow-ups.md`, "Emotion field in the screenplay
grammar" (owner, 2026-09-22) · ADR-0003 point 3 (a parenthetical
stage direction from a small enum carries the emotional register) ·
recon brief seam question S6 ·
`docs/experiments/2026-09-22-adr-0003-gate/` (run 1, whose D-on arm is
this run's baseline) ·
`docs/discussions/2026-09-22-grammar-and-prompt-cache-lessons.md`
(§1 Topic 4 shaped this run; §2.1 says why a "forced" arm is needed).

## The question

The ADR-0003 gate measured a grammar that never had to intervene:
the model already wrote `Name: text` on its own, so the grammar cost
0.3 % per token on identical output. This run adds a required
emotion tag to every line — `Name (emotion): text`, the emotion
drawn from a list of nine — and asks what that costs:

1. **when the grammar has to force the tags**, because the prompt
   never mentions them (the steering cost run 1 could not see);
2. **when the prompt and the history teach the tags**, the
   configuration the fork would actually ship.

Reported alongside: whether the model tags on its own once taught,
which emotions it picks and how varied they are, time per round and
cache reuse. Prose quality stays with the Task 5a audition.

The criteria, predictions and caveats are in `findings.md`, committed
before the first request of this run.

## Execution model

As in the ADR-0003 gate (its README, "Execution model"): the owner
owns the box and the SSH tunnel; the agent runs the scripts from the
laptop through the tunnel's local ports and inspects the box
read-only with plain `ssh ubuntu@<box> '<cmd>'`; nothing on the box
changes outside the playbook; the box's address never appears in
this folder (`<PASTE-BOX-IP-HERE>`). Times: laptop CDT, box UTC.

## Environment

The ADR-0003 gate's box, unchanged since its deploy at 17:40 CDT
(that folder's runlog entries 1, 11 and 12): Hyperstack, one RTX
A6000; Ubuntu 22.04.5, driver 550.90.12 / CUDA 12.4; llama.cpp build
`b11096-c550d2f60`, Nemotron Nano 9B v2 Q4_K_M, one slot, 16,384
context, sampler defaults (temperature 0.8, top_k 40, top_p 0.95,
min_p 0.05); tts-serve 1.2 (faster_qwen3tts) for the side quest.

## Files in this folder

- `findings.md` — criteria, caveats, predictions; Results and
  Verdict after the run.
- `screenplay.gbnf` — run 1's simple grammar, unchanged.
- `screenplay-emotion.gbnf` — the emotion grammar: 1–4 lines of
  `Name (emotion): text`; nine emotions (calm, happy, sad, afraid,
  terrified, doubtful, angry, urgent, exhausted); no square brackets
  or parentheses in the spoken text.
- `cast.py` — run 1's cast sheet, events and fixed lines, copied byte
  for byte, plus: the nine emotions; a "taught" cast sheet describing
  the tag and its values; an emotion for each of the 40 fixed lines
  (drafted by the agent); the choice of prompt (`plain` / `taught`)
  and grammar (`none` / `simple` / `emotion`); the wire-log helpers.
  The `plain` prompt with the `simple` grammar reproduces run 1's
  D-on requests byte for byte (checked, runlog entry 2).
- `latency_probe.py` — the five arms (below), ten rounds each,
  non-streamed; one JSON file per request under `raw/probe/`.
- `stream_check.sh` — one streamed request, `<label> <prompt>
  <grammar>`; raw SSE lines with arrival times under `raw/stream/`.
- `parse_stream.py` — the facts of a streamed request, now reading
  the optional `(emotion)` and judging it against the grammar's list.
- `summarize_timings.py` — every timing number: per-arm tables and
  medians, E2 (D-forced against D-simple), E1 (D-aligned against
  D-aligned-off), D-aligned-live's reuse.
- `check_outputs.py` — what the model wrote: tags legal / outside the
  list / missing, "Over." endings, emotions used and their variety,
  and whether D-simple reproduces run 1's D-on text.
- `tts_side_quest.py` — the side quest (owner's request; minimal
  reporting): three pairs of lines differing only in `’`/`'`,
  `—`/`,`, `…`/`...`, synthesized in the same voice and seed, WAVs
  written outside the repository for listening.
- `raw/` — the record of truth, committed; `raw/wire.log` — the
  readable view of the traffic, for `tail -F`.

### The arms

| Arm | Prompt and history | Grammar | Compared with |
|---|---|---|---|
| **D-simple** | plain (run 1's, no tags), fixed script | simple | — (baseline; run 1's D-on re-run) |
| **D-forced** | plain, fixed script | emotion | D-simple → **E2**, the steering cost |
| **D-aligned-off** | taught, fixed script with tags | none | — (baseline for E1; **E3**, willing compliance) |
| **D-aligned** | taught, fixed script with tags | emotion | D-aligned-off → **E1**, the shipping cost |
| **D-aligned-live** | taught, the model's own tagged output fed back | emotion | reported: the real loop with tags |

## Reproduction recipe — THE section to follow

*Living section. Run from this folder unless a step says otherwise.
The box must be deployed and the owner's tunnel up (`make check` in
the repository root prints three ok lines).*

```bash
cd docs/experiments/2026-09-22-emotion-grammar-cost
tail -F raw/wire.log        # optional, in a second terminal
```

### 1. Two streamed requests, to watch the tags arrive

```bash
./stream_check.sh forced plain emotion
./stream_check.sh aligned taught emotion
python3 parse_stream.py forced aligned
```

### 2. The probe

```bash
python3 latency_probe.py            # five arms × ten rounds + a warm-up = 51 requests
python3 summarize_timings.py
python3 check_outputs.py
ssh ubuntu@<PASTE-BOX-IP-HERE> 'docker logs llama --since 20m 2>&1' > raw/llama-log-probe.txt
```

### 3. Side quest — typographic punctuation and the TTS

```bash
python3 tts_side_quest.py --out <a folder outside the repository>
```

Then listen to each pair (`*-typographic.wav` against `*-ascii.wav`).

### 4. Close

```bash
grep -rn '<the box address>' .      # must print nothing
```

## Runlog

*Append-only. Every command actually run, in order, with its output;
the box address replaced by `<PASTE-BOX-IP-HERE>`; scratch paths
shortened to `<scratch>/`.*

### 2026-09-22 19:05 CDT — Entry 1: the owner's tunnel found down (before this run started)

While preparing the side quest, a request to the laptop's port 8001
failed to connect. Checks:

```bash
make check          # repository root
```

```
llama:   FAIL
tts:     FAIL
whisper: FAIL
```

```bash
ssh -o ConnectTimeout=15 ubuntu@<PASTE-BOX-IP-HERE> 'uptime; curl -s -o /dev/null -w "llama %{http_code}\n" http://127.0.0.1:8080/health; curl -s -o /dev/null -w "tts %{http_code}\n" http://127.0.0.1:8001/capabilities; curl -s -o /dev/null -w "stt %{http_code}\n" http://127.0.0.1:8002/docs'
```

```
 00:06:21 up  4:10,  3 users,  load average: 0.00, 0.00, 0.00
llama 200
tts 200
stt 200
```

Reading: the box and its three services are healthy; the SSH tunnel
on the laptop is down. The last traffic through it was the ADR-0003
gate's probe (ended 17:56 CDT); about 70 idle minutes later it was
gone. Consistent with the idle-cutoff suspicion in
`docs/follow-ups.md` ("REMIND THE OWNER: discuss SSH keepalives…"),
not proof of it: whether the tunnel was cut or exited is the owner's
terminal to tell. At 19:10 `make check` printed three ok lines again:
the owner had restarted the tunnel.

### 2026-09-22 19:06–19:10 CDT — Entry 2: the folder built and dry-run (no box)

- The gate's scripts copied and adapted (see "Files in this folder").
- **Baseline identity check:** for rounds 1–10, the request D-simple
  sends (`plain` prompt, `simple` grammar, seed 42) was compared with
  the request run 1's D-on sent, built by run 1's own `cast.py`:
  byte-identical in all ten rounds.
- **Dry run** in a scratch copy of the folder, against fake local
  servers (port 18090; never the box, never port 8080): the probe
  wrote the expected 11 files for two rounds (a warm-up plus five
  arms × two); both streamed variants ran; `parse_stream.py` read
  `Daniel (calm): …` as legal against the grammar's emotion list;
  D-aligned-live fed its own tagged lines back as history;
  `summarize_timings.py` and `check_outputs.py` printed every
  quantity the criteria name.
