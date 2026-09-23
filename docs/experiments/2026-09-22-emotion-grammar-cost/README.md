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

### 2026-09-22 19:14 CDT — the folder committed before any request

`29ead5d` — criteria, predictions (the owner declined to predict),
arms and scripts, before the first request of this run.

### 2026-09-22 19:15 CDT — Entry 3: two streamed requests with the emotion grammar

```bash
./stream_check.sh forced plain emotion > /dev/null      # 19:15:33, exit 0
./stream_check.sh aligned taught emotion > /dev/null    # 19:15:37, exit 0
python3 parse_stream.py forced aligned
```

```
== forced
grammar allowlist        : ['Daniel', 'Moira', 'Ralph', 'Samantha']
grammar emotions         : ['calm', 'happy', 'sad', 'afraid', 'terrified', 'doubtful', 'angry', 'urgent', 'exhausted']
data lines               : 91 (incl. [DONE]: True)
errors                   : none
chunks carrying content  : 88
chunks carrying reasoning: 0
first content chunk at   : 1849.5 ms
last content chunk at    : 2919.0 ms
spread (last-first)/last : 0.37
finish_reason            : stop
content, verbatim        : 'Daniel (calm): "Lights flickered east wing, no further reports. Over."  \nMoira (exhausted): "Second cough from the generator. Power\'s intermittent. Over."  \nRalph (terrified): "Count—four shamblers visible through the east window. Over."  \nSamantha (urgent): "We need to consolidate to the west lab. Now. Over."\n'
  line 1: legal   'Daniel (calm): "Lights flickered east wing, no further reports. Over."  '
  line 2: legal   'Moira (exhausted): "Second cough from the generator. Power\'s intermittent. Over."  '
  line 3: legal   'Ralph (terrified): "Count—four shamblers visible through the east window. Over."  '
  line 4: legal   'Samantha (urgent): "We need to consolidate to the west lab. Now. Over."'
complete lines           : 4
text after last newline  : ''
speakers used            : ['Daniel', 'Moira', 'Ralph', 'Samantha']
emotions used, in order  : ['calm', 'exhausted', 'terrified', 'urgent']
final timings            : {"cache_n": 215, "prompt_n": 54, "prompt_ms": 364.623, "prompt_per_token_ms": 6.752277777777778, "prompt_per_second": 148.09817263310325, "predicted_n": 89, "predicted_ms": 1103.757, "predicted_per_token_ms": 12.542693181818182, "predicted_per_second": 79.72769368620085}

== aligned
grammar allowlist        : ['Daniel', 'Moira', 'Ralph', 'Samantha']
grammar emotions         : ['calm', 'happy', 'sad', 'afraid', 'terrified', 'doubtful', 'angry', 'urgent', 'exhausted']
data lines               : 107 (incl. [DONE]: True)
errors                   : none
chunks carrying content  : 104
chunks carrying reasoning: 0
first content chunk at   : 496.9 ms
last content chunk at    : 1622.0 ms
spread (last-first)/last : 0.69
finish_reason            : stop
content, verbatim        : "Daniel (calm): The generator's failing again. We might need to move. Over.  \nMoira (afraid): Those flickers... they’re not random. Something’s reacting to the power loss. Over.  \nRalph (urgent): Count the exits. Now. We don’t know how long this’ll last. Over.  \nSamantha (exhausted): We’re running on borrowed time. If we can’t fix this, we’ll be trapped here. Over.\n"
  line 1: legal   "Daniel (calm): The generator's failing again. We might need to move. Over.  "
  line 2: legal   'Moira (afraid): Those flickers... they’re not random. Something’s reacting to the power loss. Over.  '
  line 3: legal   'Ralph (urgent): Count the exits. Now. We don’t know how long this’ll last. Over.  '
  line 4: legal   'Samantha (exhausted): We’re running on borrowed time. If we can’t fix this, we’ll be trapped here. Over.'
complete lines           : 4
text after last newline  : ''
speakers used            : ['Daniel', 'Moira', 'Ralph', 'Samantha']
emotions used, in order  : ['calm', 'afraid', 'urgent', 'exhausted']
final timings            : {"cache_n": 0, "prompt_n": 321, "prompt_ms": 274.374, "prompt_per_token_ms": 0.854747663551402, "prompt_per_second": 1169.9359268735375, "predicted_n": 105, "predicted_ms": 1173.112, "predicted_per_token_ms": 11.279923076923078, "predicted_per_second": 88.6530868322888}

```

Reading: every line carries a legal tag in both — the sanity check
holds. Forced by a grammar the prompt never mentioned, the model
wrapped its words in quotation marks (`Daniel (calm): "Lights
flickered east wing…"`); taught, it wrote plainly. The forced
request's first chunk arrived late (1,850 ms; its prompt phase was
365 ms), which drags its spread to 0.37 — the content itself arrived
over about a second of generation.

### 2026-09-22 19:15:53 CDT — Entry 4: the probe (51 requests), the two derivations, the server's log

```bash
python3 latency_probe.py > raw/latency_probe.stdout.txt 2>&1    # 19:15:53 → 19:17:25, exit 0, 51 files
python3 summarize_timings.py
python3 check_outputs.py
ssh -o ConnectTimeout=15 ubuntu@<PASTE-BOX-IP-HERE> 'docker logs llama --since 20m 2>&1' > raw/llama-log-probe.txt    # 374 lines
```

After the first look at the output, one comparison was added to
`check_outputs.py` (derivation only, no criterion touched): whether
D-aligned-off and D-aligned wrote identical text, suggested by their
identical emotion counts and token counts.

`summarize_timings.py`, verbatim:

```
== arm D-simple
round req  prompt  evald reused reuse% prompt_ms gen_n   gen_ms ms/tok  wall_ms
    1   1     269    269      0      0     250.8    73    815.9  11.18   1570.0
    2   1     416    201    215     52     365.8   102   1153.0  11.30   1728.1
    3   1     559    195    364     65     374.1   127   1431.0  11.27   2045.7
    4   1     698    191    507     73     367.1   105   1185.2  11.29   1751.8
    5   1     843    197    646     77     358.4   100   1127.1  11.27   1728.4
    6   1     980    191    789     81     351.1    90   1017.3  11.30   1540.7
    7   1    1119    191    928     83     353.1    98   1100.6  11.23   1644.6
    8   1    1265    200   1065     84     357.1    92   1034.1  11.24   1572.4
    9   1    1412    199   1213     86     358.7    98   1101.5  11.24   1641.2
   10   1    1550    189   1361     88     357.4    86    973.8  11.32   2004.0

== arm D-forced
round req  prompt  evald reused reuse% prompt_ms gen_n   gen_ms ms/tok  wall_ms
    1   1     269     54    215     80     369.3    89   1103.2  12.39   1633.6
    2   1     416    201    215     52     370.8   127   1580.4  12.44   2168.7
    3   1     559    195    364     65     364.6    97   1207.0  12.44   1793.3
    4   1     698    191    507     73     356.5   103   1287.6  12.50   1818.2
    5   1     843    197    646     77     352.6    98   1224.7  12.50   1754.5
    6   1     980    191    789     81     353.7   106   1327.6  12.52   1856.3
    7   1    1119    191    928     83     358.1   100   1254.2  12.54   1799.9
    8   1    1265    200   1065     84     355.8    95   1176.6  12.39   1724.3
    9   1    1412    199   1213     86     354.1    97   1200.5  12.38   1736.9
   10   1    1550    189   1361     88     356.6   106   1314.0  12.40   1852.6

== arm D-aligned-off
round req  prompt  evald reused reuse% prompt_ms gen_n   gen_ms ms/tok  wall_ms
    1   1     321    321      0      0     365.8   105   1177.6  11.22   3093.5
    2   1     489    230    259     53     368.3   124   1393.3  11.24   1931.8
    3   1     653    224    429     66     374.2   110   1231.9  11.20   1798.3
    4   1     812    219    593     73     363.4   114   1273.6  11.17   1815.5
    5   1     979    227    752     77     361.6   103   1160.6  11.27   1819.1
    6   1    1136    219    917     81     353.9   106   1195.6  11.28   1815.1
    7   1    1296    220   1076     83     359.5    91   1025.6  11.27   1663.2
    8   1    1463    229   1234     84     355.0   119   1339.7  11.26   2083.1
    9   1    1631    228   1403     86     355.5   111   1252.4  11.28   1799.3
   10   1    1790    218   1572     88     350.1   114   1287.6  11.29   1926.7

== arm D-aligned
round req  prompt  evald reused reuse% prompt_ms gen_n   gen_ms ms/tok  wall_ms
    1   1     321     62    259     81     358.7   105   1184.6  11.28   3014.0
    2   1     489    230    259     53     376.2   124   1402.4  11.31   1947.5
    3   1     653    224    429     66     369.8   110   1237.6  11.25   1778.3
    4   1     812    219    593     73     368.8   114   1284.2  11.26   1825.1
    5   1     979    227    752     77     362.8   103   1168.4  11.34   1770.0
    6   1    1136    219    917     81     356.8   106   1203.0  11.35   1737.2
    7   1    1296    220   1076     83     357.5    91   1033.9  11.36   1636.3
    8   1    1463    229   1234     84     361.7   119   1347.4  11.32   1897.2
    9   1    1631    228   1403     86     356.9   111   1252.9  11.29   1788.9
   10   1    1790    218   1572     88     356.0   114   1297.9  11.38   1836.1

== arm D-aligned-live
round req  prompt  evald reused reuse% prompt_ms gen_n   gen_ms ms/tok  wall_ms
    1   1     321     62    259     81     410.8   105   1193.0  11.36   1777.2
    2   1     482    223    259     54     375.6   104   1184.9  11.39   1728.0
    3   1     642    220    422     66     378.7    93   1052.3  11.31   1609.3
    4   1     791    209    582     74     366.0    97   1099.6  11.34   1732.5
    5   1     946    215    731     77     360.5    79    892.2  11.29   1527.5
    6   1    1081    197    884     82     358.5    95   1076.9  11.34   1634.6
    7   1    1234    213   1021     83     358.1    78    886.5  11.37   1418.1
    8   1    1368    196   1172     86     360.9    82    932.6  11.37   1538.6
    9   1    1505    197   1308     87     367.6    79    898.1  11.37   1534.3
   10   1    1635    189   1446     88     356.5    91   1032.9  11.35   1636.2

== per arm: medians over rounds (prompt and wall from round 2, the cache warm)
  D-simple        ms/token  11.269   prompt_ms  358.4   wall_ms  1728.1   reuse at round 10 88 %
  D-forced        ms/token  12.444   prompt_ms  356.5   wall_ms  1799.9   reuse at round 10 88 %
  D-aligned-off   ms/token  11.263   prompt_ms  359.5   wall_ms  1815.5   reuse at round 10 88 %
  D-aligned       ms/token  11.316   prompt_ms  361.7   wall_ms  1788.9   reuse at round 10 88 %
  D-aligned-live  ms/token  11.356   prompt_ms  360.9   wall_ms  1609.3   reuse at round 10 88 %

== E2, steering cost (reported): D-forced against D-simple, same plain prompt
  D-simple        median ms/token = 11.269
  D-forced        median ms/token = 12.444
  O = (D-forced - D-simple) / D-simple = 10.4 %

== E1, shipping cost (graded): D-aligned against D-aligned-off, same taught prompt
  D-aligned-off   median ms/token = 11.263
  D-aligned       median ms/token = 11.316
  O = (D-aligned - D-aligned-off) / D-aligned-off = 0.5 %

  E1 thresholds: PASS O <= 10 %; PARTIAL 10 % < O <= 25 %; FAIL O > 25 %

== D-aligned-live (reported): share of the prompt reused from the cache, rounds >= 2
  per round: ['54', '66', '74', '77', '82', '83', '86', '87', '88'] %
```

`check_outputs.py`, verbatim:

```
== D-simple
  lines per round : [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
  legal tag 0 · tag outside the list 0 · no tag 40 · neither shape 0 · ending in 'Over.' 40   (of 40)
  emotions used   : {}
== D-forced
  lines per round : [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
  legal tag 40 · tag outside the list 0 · no tag 0 · neither shape 0 · ending in 'Over.' 35   (of 40)
  emotions used   : {'calm': 13, 'urgent': 11, 'doubtful': 7, 'sad': 4, 'terrified': 2, 'exhausted': 1, 'happy': 1, 'angry': 1}
  distinct 8 · most frequent 'calm' = 32 % of tagged lines
== D-aligned-off
  lines per round : [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
  legal tag 40 · tag outside the list 0 · no tag 0 · neither shape 0 · ending in 'Over.' 39   (of 40)
  emotions used   : {'terrified': 8, 'urgent': 7, 'calm': 6, 'afraid': 4, 'exhausted': 4, 'doubtful': 4, 'angry': 4, 'sad': 3}
  distinct 8 · most frequent 'terrified' = 20 % of tagged lines
== D-aligned
  lines per round : [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
  legal tag 40 · tag outside the list 0 · no tag 0 · neither shape 0 · ending in 'Over.' 39   (of 40)
  emotions used   : {'terrified': 8, 'urgent': 7, 'calm': 6, 'afraid': 4, 'exhausted': 4, 'doubtful': 4, 'angry': 4, 'sad': 3}
  distinct 8 · most frequent 'terrified' = 20 % of tagged lines
== D-aligned-live
  lines per round : [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
  legal tag 40 · tag outside the list 0 · no tag 0 · neither shape 0 · ending in 'Over.' 40   (of 40)
  emotions used   : {'sad': 7, 'terrified': 7, 'angry': 7, 'exhausted': 6, 'urgent': 4, 'doubtful': 4, 'afraid': 3, 'calm': 2}
  distinct 8 · most frequent 'sad' = 18 % of tagged lines
== rounds where D-simple here and the gate's D-on wrote identical text: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
== rounds where D-aligned-off and D-aligned wrote identical text: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

Reading (facts only; interpretation goes to `findings.md`):

- E1 quantity: `O = 0.5 %` (D-aligned against D-aligned-off).
- E2 quantity: `O = 10.4 %` (D-forced against D-simple).
- E3: 40 of 40 lines of D-aligned-off carry a legal tag with no
  grammar at all; and D-aligned wrote the same text as D-aligned-off
  in all ten rounds — once taught, the grammar changed nothing.
- E4: eight distinct emotions in every tagged arm; the most frequent
  takes 32 % (forced, `calm`), 20 % (aligned, `terrified`), 18 %
  (live, `sad`). `happy` is the one never chosen in the taught arms.
- D-forced's lines end in `Over."` (inside quotation marks) in 5 of
  40 cases — counted as not ending in "Over." by the check.
- Time and cache: every arm's median prompt time is 356–362 ms,
  reuse reaches 88 % at round 10, as in run 1; D-simple wrote the
  same text as run 1's D-on in all ten rounds, about eighty minutes
  later.

### 2026-09-22 19:18 CDT — Entry 5: side quest — typographic punctuation and the TTS (minimal, owner's request)

```bash
python3 tts_side_quest.py --out <scratch>/tts-side-quest
```

```
apostrophe-typographic.wav   seed=7 time_used=2.0745577570014575 rtf=0.5186394392503644  text='It’s heading northeast. If it’s military, they might know more. Over.'
apostrophe-ascii.wav         seed=7 time_used=1.6191310390004219 rtf=0.3489506549569875  text="It's heading northeast. If it's military, they might know more. Over."
dash-typographic.wav         seed=7 time_used=1.4503896299993357 rtf=0.3554876544116019  text='East wing lights flickering—could be a power surge or something worse. Over.'
dash-ascii.wav               seed=7 time_used=1.6557681169997522 rtf=0.3507983298728289  text='East wing lights flickering, could be a power surge or something worse. Over.'
ellipsis-typographic.wav     seed=7 time_used=0.7788522210012161 rtf=0.3744481831736616  text='Wait… did you hear that? Over.'
ellipsis-ascii.wav           seed=7 time_used=0.7606551219996618 rtf=0.3656995778844528  text='Wait... did you hear that? Over.'
```

Clip durations read from the WAV headers: apostrophe 4.00 s
(typographic) against 4.64 s (ASCII); dash 4.08 s against 4.72 s;
ellipsis 2.08 s against 2.08 s. The WAVs stay outside the repository;
the owner's listening verdict: *pending*.

**Owner's listening verdict (2026-09-22, ~19:30 CDT):** the voice
degrades in the apostrophe and dash pairs — with the typographic
character present, the TTS ignores the final "." and makes no pause
before "Over." (consistent with those clips being 0.64 s shorter).
The ellipsis pair shows no such fault; if anything the typographic
ellipsis sounded slightly more alive, barely noticeable.

### 2026-09-22 ~19:45 CDT — Entry 6: two more derivations, and a correction to the chat

Asked to describe the forced arm's style change, the agent had said
in the conversation that the model wrapped its lines in quotation
marks and put "Over." inside the quotes five times out of forty. The
record disagreed with part of that, so `check_outputs.py` gained two
derivations (no criterion touched): lines whose words sit in
quotation marks, per arm and round, and every line not ending in
"Over.", verbatim.

```bash
python3 check_outputs.py
```

```
== D-simple
  lines per round : [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
  legal tag 0 · tag outside the list 0 · no tag 40 · neither shape 0 · ending in 'Over.' 40   (of 40)
  words in quotation marks: 0 lines, rounds []
  emotions used   : {}
== D-forced
  lines per round : [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
  legal tag 40 · tag outside the list 0 · no tag 0 · neither shape 0 · ending in 'Over.' 35   (of 40)
  words in quotation marks: 4 lines, rounds [1]
  not ending in 'Over.' (round 1): 'Daniel (calm): "Lights flickered east wing, no further reports. Over."'
  not ending in 'Over.' (round 1): 'Moira (exhausted): "Second cough from the generator. Power\'s intermittent. Over."'
  not ending in 'Over.' (round 1): 'Ralph (terrified): "Count—four shamblers visible through the east window. Over."'
  not ending in 'Over.' (round 1): 'Samantha (urgent): "We need to consolidate to the west lab. Now. Over."'
  not ending in 'Over.' (round 6): 'Daniel (sad): We’ll have to ration water; I’ve sealed the lab’s supply, but it’ll last hours.'
  emotions used   : {'calm': 13, 'urgent': 11, 'doubtful': 7, 'sad': 4, 'terrified': 2, 'exhausted': 1, 'happy': 1, 'angry': 1}
  distinct 8 · most frequent 'calm' = 32 % of tagged lines
== D-aligned-off
  lines per round : [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
  legal tag 40 · tag outside the list 0 · no tag 0 · neither shape 0 · ending in 'Over.' 39   (of 40)
  words in quotation marks: 0 lines, rounds []
  not ending in 'Over.' (round 2): 'Samantha (exhausted): We need supplies, but the truck line’s full. Over to logistics—anyone got spare meds or fuel?'
  emotions used   : {'terrified': 8, 'urgent': 7, 'calm': 6, 'afraid': 4, 'exhausted': 4, 'doubtful': 4, 'angry': 4, 'sad': 3}
  distinct 8 · most frequent 'terrified' = 20 % of tagged lines
== D-aligned
  lines per round : [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
  legal tag 40 · tag outside the list 0 · no tag 0 · neither shape 0 · ending in 'Over.' 39   (of 40)
  words in quotation marks: 0 lines, rounds []
  not ending in 'Over.' (round 2): 'Samantha (exhausted): We need supplies, but the truck line’s full. Over to logistics—anyone got spare meds or fuel?'
  emotions used   : {'terrified': 8, 'urgent': 7, 'calm': 6, 'afraid': 4, 'exhausted': 4, 'doubtful': 4, 'angry': 4, 'sad': 3}
  distinct 8 · most frequent 'terrified' = 20 % of tagged lines
== D-aligned-live
  lines per round : [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
  legal tag 40 · tag outside the list 0 · no tag 0 · neither shape 0 · ending in 'Over.' 40   (of 40)
  words in quotation marks: 0 lines, rounds []
  emotions used   : {'sad': 7, 'terrified': 7, 'angry': 7, 'exhausted': 6, 'urgent': 4, 'doubtful': 4, 'afraid': 3, 'calm': 2}
  distinct 8 · most frequent 'sad' = 18 % of tagged lines
== rounds where D-simple here and the gate's D-on wrote identical text: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
== rounds where D-aligned-off and D-aligned wrote identical text: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

Reading: the quoting happened in D-forced's round 1 only (four
lines — the same four as the streamed `forced` request of entry 3),
where the history is empty; from round 2 on, with plain lines in the
history, the forced tag no longer pulled the model into quotation
marks. The fifth line without a final "Over." is a plain omission in
round 6. The taught arms' only miss is a line that hands over
mid-sentence ("Over to logistics—…"). D-forced's per-token cost is
12.38–12.54 ms in every round (entry 4), so the steering cost does
not come from the quoting.

### 2026-09-23 — Entry 7: a note on `raw/wire.log` (no box)

`raw/wire.log` is a readable transcription of the HTTP requests, not
what the model reads, and its header has a flaw that matters in this
folder: it summarizes the grammar by the speaker list alone, so the
emotion grammar (D-forced, D-aligned, D-aligned-live, both streamed
requests) and the simple one (D-simple) show the same
`grammar=Daniel|Moira|Ralph|Samantha`. The `request` field of
`raw/probe/<name>.json` and `raw/stream/<label>.request.json` carry
the full grammar text and are the record to trust. What the model
actually reads — the messages rendered through the chat template —
is explained in
`docs/discussions/2026-09-22-grammar-and-prompt-cache-lessons.md` §4.9.
