# The app from the outside — how it counts the script's tokens and trims, and every endpoint to test it without the page

**Date:** 2026-10-01 · **Arc:** MVP prototype · **Branch:** `alfre2v/context-32k`
**Type:** discussion — two requests of the owner on the same day, both about
seeing the app's inner workings from outside its page: (A) how the app keeps the
tally of the tokens in the model's context and decides when to trim, in depth;
(B) a survey of every HTTP endpoint the app (and the model services under it)
offers, and how each serves to test a part of the app in isolation, without the
JavaScript.
**Status:** CURRENT VIEW — written as a reference, to be kept a linear story of
the current state when the app changes (the owner, 2026-10-01: "when a
discussion becomes very interesting we sometimes update it to make them less a
log and more a linear story that describe the current view of the issue
documented"). Part A describes the fork's branch `alfre2v/context-32k` (the
trim's numbers as settings, the 34,000 budget, the start check) — `tz-0.5` once
released; part B was surveyed on the same branch.

## §1. The owner's requests (verbatim, 2026-10-01)

After the agent's explanation of how the trim decides (§2.2-§2.4), the owner:

> Thanks, this is way clearer now. I remember we kind of documented these
> timings somewhere... could you remind me where? And if not found, or what you
> found is not explicative enough, then add this explanation to the appropriate
> document to explain the question: "How does the app keeps track of the token
> use and to trigger when to trim ".

And, after the agent added it to the fork's driver runbook:

> You know what, I agree to add that documentation piece to the fork's show
> driver.
>
> #### Document in zombie-radio how the app keeps the tally of tokens in the context
>
> I also think we need to add this info (in depth) as a new discussion document
> in zombie-radio. Let's create a new discussion document to persist the inner
> workings of the trim trigger, and also one new documentation request that I am
> going to ask now (maybe both documentation tasks can be saved in the same
> discussion doc, we ca discuss the doc names). Here is my new request:
>
> ### Survey the fastapi endpoints and establish each use for testing the app
>
> I seek more info about this way you used to run the test:
>
> ```
> How I'd run the show without a browser: no headless Chrome. The fork's scripts/drive_show.py plays the show through the app's own API: it opens a run, asks for round after round, and prints what streams back.
>
> It answers the listening windows with text you give it (--heard), or with silence.
> It doesn't synthesize voices; each round counts as 20 s played (--played).
>
> For this test, the voices don't matter. The trim depends only on how many tokens the script holds, and the voice's memory doesn't change with the context. A browser would only add voice requests to the box. I'd give it about 20 listener lines, so the run has many contacts: those are the heaviest rounds, about 500 tokens each, the ones that fill the context fastest.
> ```
>
> Actually, I should know this, but I guess I forgot, regardless, I want to be
> aware of each api endpoint our client provides and how it could be used to
> test the app inner workings separately without the complexity of the
> javascript files. I guess it is time to make a survey all all the fastapi
> endpoints and how you use them to diagnose problems and run parts of the app
> in relative isolation.

The decision on the document (the owner, verbatim): "one doc,
the-app-from-the-outside, in zombie-radio, run the read-only calls." Then, on
the first draft: "Feel free to run anything you need to make the documents more
complete if you deem it necessary." Every example output here is from a real
call — on 2026-10-01 against the dev server (the fork's `alfre2v/context-32k`,
seed 42, debug on) and the box, unless dated otherwise. Beyond the read-only
calls, the agent made the ones the document needed: a run opened, one round
(its raw stream, §3.2), one voice chunk (§3.3), two transcriptions (§3.4), a
round's request replayed to llama.cpp and the grammar check (§4.1) — two model
requests, one voice request, two Whisper requests. The calls that edit
personas, rooms, the chat or the settings were **not** made (§3.7): nothing
here needs them, and they would change the owner's files.

## §2. Part A — how the app counts the script's tokens, and when it trims

The same explanation, in the fork's terms and with a command, lives in the
fork's `docs/runbooks/show-driver.md`, section "How the app tracks the script's
size, and when it trims" (added on the same branch). This part keeps the whole
story: the questions, the answers, the history, the measurements.

### §2.1 The problem

The show is **one growing script**: every round, the model reads the whole
script so far — the cast sheet (the system message), then every kept round's
instruction (a user turn) and reply (an assistant turn) — plus the new
round's instruction. All of it must fit the model server's context: llama.cpp's
`-c`, set by this repository's `zr_llama_ctx`
(`deploy/ansible/inventories/common_vars.yml`): **16,384** tokens until
2026-10-01, **32,768** since. The **trim** keeps the script inside: when it grows
too big, whole rounds from its middle stop being read.

### §2.2 The owner's questions (verbatim) and where the numbers lived

> Wait, how is it that all these trim related config params were not already in
> the code that loads the settings? How was the app deciding when to trim until
> now then? Where the values came from?
>
> What about the function `server_context` you added in llm? Is that only called
> once in the start of the show? Or is it called periodically to re-check the
> context size against our own internal calculation of the token size?
> How do we actually keep the tally of how many tokens are in our current
> context?

**Where the numbers lived.** Until this branch they were **constants in the
code**, at the top of the trim in the fork's `app/show/script.py`:

```python
_KEEP_FIRST = 2
_KEEP_LAST = 4
_TRIGGER = 0.9
_TARGET = 0.5
```

`trim(run, budget)` read them directly; only the budget came from the settings
(`show.context_budget`, 14,000 by default). The trim was written that way in
slice 2 (2026-09-25); the owner spotted it on 2026-09-28, and it was recorded
as the follow-up "The trim's thresholds in settings — the 90 % trigger and the
50 % target are hard-coded" (`docs/follow-ups.md`), against the rule that every
number is a setting. On this branch they became settings, with the same values
as defaults (§2.5).

### §2.3 The tally: the model server counts, the app keeps its numbers

**The app does not count tokens itself. It takes the model server's own count,
after every round.**

1. **The server reports.** When the model finishes a round, llama.cpp's last
   streamed chunk carries `timings`; the app keeps them with the round in the
   run's record, `runs/<run-id>/script.json`:
   - `prompt_n` — tokens of the prompt the server read **fresh** this time;
   - `cache_n` — tokens of the prompt it **reused from its cache** (the start of
     the script, unchanged since the last round);
   - `predicted_n` — tokens it **generated**: the reply.
2. **Their sum is the script's size after that round** — what the model will
   read next time, before the next instruction (`script_size()`): the next
   round's prompt is exactly this round's prompt plus this round's reply, plus
   the new instruction. Round 113 of the drive of 2026-10-01 at 12:54: 203 fresh
   + 27,653 cached + 50 written = **27,906**.
3. **Each round records its share** (`tokens`, `round_share()`): its size less
   the size before it — what the round added to the script, its instruction and
   its reply. The largest share in 82 recorded runs (1,824 rounds, measured
   2026-10-01): **741 tokens**, an exchange (an exchange's instruction restates
   the caller's words, earlier callers' words and an agenda item).
4. **Before planning each round, the trim reads the last reported size**
   (`trim()`, called by the round route, `app/routers/show.py`):
   - below `trim_trigger × context_budget` (0.9 × 34,000 = **30,600**):
     nothing happens;
   - at or above it, the rounds the model still reads become candidates, except
     the first `trim_keep_first` (2) and the last `trim_keep_last` (4); the
     **middle** candidate is flagged `trimmed`, again and again, outwards; each
     takes **its recorded share** off the size, until the estimate is down to
     `trim_target × context_budget` (**17,000**) or no candidate is left. A
     flagged round stays in the record; the model no longer reads it, and the
     driver prints `trimmed before this round: rounds …`.
5. **The server reads the shortened script from the start.** Its cache holds
   only an unbroken start of the prompt; once the middle changed, everything
   after the first changed token is read fresh — **the pause after a trim**
   (§2.6).
6. **The next round's report is the truth.** The shares are an estimate; the
   server's next count is the real size, and the next decision starts from it.
   An error never adds up.

**Two rounds without a count.**

- **A round with no model request** — the Repair, both of its lines fixed — has
  no `timings`: the size is unknown after it, and the trim skips that round.
  Its lines still reach the model: its instruction, which quotes its two fixed
  lines, joins the next round's user turn (`assemble_messages()`).
- **Its share, and the share of the round after it, are unknown** (`None`), and
  the trim counts an unknown share as 0. So when trimmed rounds include them,
  **the trim removes more than it estimates and cuts below its target.** Seen in
  both drives of 2026-10-01: aiming at 15,500 (50 % of 31,000) it landed at
  12,269; aiming at 17,000 (50 % of 34,000) it landed at 14,017. The next
  round's share shows the correction as a negative number (−2,837 and −2,966).
  Harmless — the model reads a little less for a while — and the count is right
  again from the next round. (A possible refinement, not built: estimate an
  unknown share as the average share.)

**Not the tally:** the **token check** in the debug files (`show.debug` on) is a
separate verification: after each round the app renders the prompt itself
through the server's `/apply-template`, counts it with `/tokenize`, and compares
with `prompt_n + cache_n`, to prove that the prompt shown in `debug/rNNN.txt`
is the one the model read ("difference 0"). The trim never uses it. A round
with no model request has nothing to compare: its debug file says "the server
reported no size".

### §2.4 The start check: `server_context`, once per run

The size the trim watches is the script **before** the next round; the request
also carries that round's instruction and room for its reply. So the largest
request is about `trim_trigger × context_budget + an instruction + the reply`.
On this branch, **when a run opens** (`POST /api/show/start`), the app asks the
model server its real context (`server_context()` in `app/services/llm.py`:
llama.cpp's `GET /props`, `default_generation_settings.n_ctx`) and refuses the
run if

`trim_trigger × context_budget + instruction_room + max_tokens > n_ctx`

with the arithmetic in the message (HTTP 422; the page shows "Error: the show
could not start: …"). Measured live on 2026-10-01 with a temporary budget of
40,000:

```
{"detail":"show.context_budget 40000 does not fit the model server's context of 32768 tokens: the trim lets the script reach 36000 tokens (show.trim_trigger 0.9), plus 1000 for the next instruction (show.instruction_room) and 512 for the reply (show.max_tokens) = 37512. Lower show.context_budget, or give the server a larger context."}
```

With the defaults: 30,600 + 1,000 + 512 = **32,112**, which fits 32,768 (the
run started). **Why once per run, not per round:** the server's context changes
only when the box is redeployed with another `-c`, and the budget only when the
app restarts; a mid-show redeploy is not a real case. The one gap: **Resume**
continues a run without `/start`, so it does not re-check — after a mid-show
redeploy to a smaller context, a round would fail with the server's error and
the page would show "this round failed". A check before every round would close
it for one tiny request a round; left out. If the server cannot say (no
`/props`), the run starts and the app's log warns. Before this check, the budget
(in the fork's settings) and the server's context (in this repository's
deployment) were tied by nothing — a mismatch would have surfaced only as a
failed round deep into a show.

### §2.5 The settings (the fork's `ShowConfig`, `app/config.py`)

| Setting | Default | What it does |
|---|---|---|
| `context_budget` | **34,000** (14,000 before) | the script's size the trim works against |
| `trim_trigger` | 0.9 | the trim fires at this fraction of the budget |
| `trim_target` | 0.5 | it cuts until the script is back to this fraction (below the trigger: checked when the settings load) |
| `trim_keep_first` | 2 | rounds at the start never trimmed |
| `trim_keep_last` | 4 | rounds at the end never trimmed |
| `instruction_room` | 1,000 | tokens kept free above the trigger for the next instruction (the largest share seen: 741) |
| `max_tokens` | 512 | the reply's budget (unchanged; also part of the start check) |

Why 34,000 and not 32,768: the trim fires at 90 % of the budget, so the budget
may exceed the context as long as 90 % of it plus the room fits — the most
context the show can keep (the owner, 2026-09-28: "I want to keep as much
context as possible").

### §2.6 What the change measured (2026-10-01, the A6000)

**GPU memory** (`nvidia-smi`; how to measure: this repository's
`docs/runbooks/box-inspection.md`, "The LLM: how much is the model, how much is
the context"):

| | llama-server | the whole card |
|---|---|---|
| 16k context, idle | 6,764 MiB (of which the model file: 6,223 MiB) | 14,195 MiB |
| 32k context, just started (empty) | 6,970 MiB | 14,401 MiB |
| 32k, during and after full drives (to 30,694 tokens) | **7,046 MiB, flat** | **14,477 MiB** (≈ 14.1 GiB) |

llama.cpp reserves the context's memory when it starts: doubling the context
cost **206 MiB** at once, plus **76 MiB** allocated on first use during the first
minute of the first drive, then nothing more, through a full context and a
trim — on this hybrid model (Nemotron Nano 9B v2: few attention layers). The
owner's field observation that memory grows as the context fills (2026-10-01:
"I often see in practice that the memory of LLM models served with llama.cpp
increase somehow as you push info into the context") was not seen on the GPU
here; llama-server's **system** memory was 10.6 GB after the drives (the mapped
model file and, probably, the prompt cache kept in RAM) — no reading from
before, so its growth is unknown. The stack stays under the owner's 16 GB wish
and the 3090's 24 GB.

**Two drives** (the fork's `scripts/drive_show.py`, seed 42, 36 listener
answers, debug on, no voices):

| Run | Budget | Rounds | Trim | The pause (first line after the trim) |
|---|---|---|---|---|
| `2026-10-01T12-54-40` | 31,000 (settings) | 190 | once, before round **114**, at 27,906 tokens; 58 rounds; landed at 12,269 | **8.2 s** (12,209 tokens read fresh) |
| `2026-10-01T13-43-41` | 34,000 (the new default) | 220 | once, before round **140**, at 30,694 tokens; 56 rounds; landed at 14,017 | **8.4 s** (13,922 fresh) |

The largest request of the second drive: **30,694 tokens** (round 139, read
plus written), about 2,000 below the context. No request failed; the server
logged no error. For comparison, at 16k with a 14,000 budget (the owner's
listen of 2026-09-28, run `2026-09-28T15-31-44`): trims at rounds 79, 101, 133
and 169 — every 22-36 rounds — each about 5 s (5,008 tokens re-read, 5.1 s).
**Now: trims about 3-4 times rarer, each about 60 % longer; the model keeps about
2.2 times as much of the show.**

## §3. Part B — the endpoints, and what each is good for

The app (the fork, TalkWithZombies) is a FastAPI server; the page is only one of
its clients. Everything the page does goes through these endpoints, so each part
of the app can be exercised alone with `curl` or a short script. The dev server
runs at `http://127.0.0.1:8010` (`.venv/bin/uvicorn app.main:app --host
127.0.0.1 --port 8010` in the fork's checkout); the installed client the same
way from `~/TalkWithZombies-client`. The model services are reached through the
SSH tunnel at `localhost:8080` (llama.cpp), `:8001` (tts-serve), `:8002`
(Whisper). The survey (2026-10-01): **36 API routes** in nine routers, four
pages, the static files, and FastAPI's own documentation.

### §3.1 Start here: FastAPI's interactive documentation

FastAPI documents every endpoint by itself: **<http://127.0.0.1:8010/docs>**
(Swagger UI) lists them all with their request bodies, and each has a "Try it
out" button that sends a real request from the browser and shows the reply —
a form for every body. `/redoc` is the same, read-only; `/openapi.json` the
machine-readable schema.

```bash
# The schema: every path the app documents (the title is still upstream's, "TalkWithMe")
curl -s http://127.0.0.1:8010/openapi.json | head -c 200
```

```
{"openapi":"3.1.0","info":{"title":"TalkWithMe","description":"A local multi-persona group chat application","version":"0.1.0"},"paths":{"/api/personas":{"get":{"tags":["personas"],"summary":"List Per
```

The schema has 32 paths (a path with several methods counts once): every API
route, and the pages `/show` and `/talkwithme`; only `GET /` (the redirect) and
FastAPI's own pages are left out.

### §3.2 The show — the core (`app/routers/show.py`)

| Endpoint | What it does | Body |
|---|---|---|
| `GET /show` | the page: the chooser, a look (`?design=old-radio`), the plain page (`?design=plain`), text only (`&voice=off`), a preview (`&mock=1`) | — |
| `POST /api/show/start` | opens a run: loads the story, checks the budget against the server's context (§2.4), renders the cast sheet, picks the seed, writes `runs/<run-id>/script.json`; replies with the run's id, title, cast, seed, timers, `debug`, the mood→clip `voices`, `voice_seed` | `{"story": "lab-outbreak"}` or `{}` |
| `POST /api/show/round` | plays the run's next round: the trim, the director's plan, one model request (none for a Repair), the record; replies with a **stream** of events (Server-Sent Events): `start` (a line begins: persona, mood), `token` (its text as it streams), `done` (the line, with its `message_id`), `round` (the round's summary: number, kind, speakers, event, trims, timings…), `error`, then `complete` | `{"run_id": "…", "played_s": 20}`, plus `"transcript"` (and Whisper's `no_speech_prob`, `avg_logprob`) after a listening window |
| `POST /api/show/listen` | transcribes what the listener said, with the cast's names as Whisper's hint; replies with the text, the confidence numbers and each word's probability | `{"run_id": "…", "audio_base64": "…", "audio_mime_type": "audio/webm"}` |

**What they isolate:** `start` + `round` are the whole show engine — the
director, the grammar, the model, the parser, the trim, the record and the
debug files — **without the voice and without the page**. That is what the
fork's `scripts/drive_show.py` does (§4.2). `listen` is Whisper as the show uses
it, without the microphone.

From 2026-10-01, a start (the reply, cut):

```
{"run_id":"2026-10-01T13-20-20","story":"lab-outbreak","title":"The Lab at the End of the Frequency","cast":["Daniel","Moira","Ralph","Samantha"],"operator":"Samantha","seed":42,"listen_window_s":10.0
```

A round's raw stream — what the page reads — with `curl`:

```bash
# Open a run and keep its id
RUN=$(curl -s -X POST -H 'Content-Type: application/json' -d '{}' http://127.0.0.1:8010/api/show/start | python3 -c "import json,sys; print(json.load(sys.stdin)['run_id'])")
# Play its next round: the raw stream of events, printed as they arrive (-N)
curl -s -N -X POST -H 'Content-Type: application/json' -d "{\"run_id\": \"$RUN\", \"played_s\": 0}" http://127.0.0.1:8010/api/show/round
```

The first round of run `2026-10-01T14-05-43` (92 lines, 40 of them `token`
events; the middle cut):

```
data: {"type": "start", "persona": "Samantha", "mood": "calm", "message_id": "2026-10-01T14-05-43-r001-l1"}
data: {"type": "token", "persona": "Samantha", "token": "We"}
data: {"type": "token", "persona": "Samantha", "token": " are"}
data: {"type": "token", "persona": "Samantha", "token": " scientists"}
…
data: {"type": "done", "persona": "Samantha", "text": "We are scientists trapped in a lab near a wood and a swamp. Our radio is dead, only transmission. Over.", "message_id": "2026-10-01T14-05-43-r001-l1"}
data: {"type": "start", "persona": "Daniel", "mood": "doubtful", "message_id": "2026-10-01T14-05-43-r001-l2"}
…
data: {"type": "done", "persona": "Daniel", "text": "The virus... it's mutating. We don't know how. Over.", "message_id": "2026-10-01T14-05-43-r001-l2"}
data: {"type": "round", "n": 1, "kind": "orientation", "speakers": ["Daniel", "Moira", "Ralph", "Samantha"], "event": null, "tone": "stiff-upper-lip", "heard": null, "trimmed": [], "dropped": [], "finish_reason": "stop", "listens": false, "receiver": false, "overtone": "neutral", "agenda": null, "slot": null, "answers": null, "direction": null}
data: {"type": "complete"}
```

Reading it: each line is a `start` (who, in which mood), its `token`s, and a
`done` with the line as the voice gets it — the page sends each `done` to the
voice; the `round` summary tells the page what the director chose (the kind,
whether the page listens next, whether the receiver is on); the model's
`timings` stay in the record. The `done` text is the parser's: the model wrote
"dead—only" and "it’s" (the record's `raw`, §4.1), the voice gets "dead, only"
and "it's".

### §3.3 The voice (`app/routers/tts.py`)

| Endpoint | What it does |
|---|---|
| `GET /api/tts/health` | is the voice on and reachable, and which engine |
| `GET /api/tts/capabilities` | tts-serve's capabilities document, passed through (the engine, the model, the parameters it takes — `seed` among them, with its range) |
| `POST /api/tts` | one chunk of voice: `{"text", "persona_name"}`, plus optional `"reference"` (a clip, e.g. `ref-fear.wav`), `"seed"`, `"debug"` (the show's tag `<run-id>/r009-l2-c1`); replies with the audio (base64 WAV), the seed the engine used, `time_used`, and the clip used |

**What it isolates:** one line in one voice, with a chosen clip and seed —
without the show or the page. The fork's `scripts/replay_chunk.py` uses it to
say a kept chunk again (§4.3).

```bash
# One chunk in Moira's voice, from her "relief" clip, with seed 7; the reply printed without its audio
curl -s -X POST -H 'Content-Type: application/json' -d '{"text": "Hello, this is Marta. I can hear you from a farmhouse outside Bastrop.", "persona_name": "Moira", "reference": "ref-relief.wav", "seed": 7}' http://127.0.0.1:8010/api/tts | python3 -c "import json,sys; d=json.load(sys.stdin); d['audio_base64']=f\"<{len(d['audio_base64'])} characters of base64>\"; print(json.dumps(d))"
```

```
{"audio_base64": "<286780 characters of base64>", "sample_rate": 24000, "seed": 7, "time_used": 1.535343086001376, "rtf": 0.34271051026816424, "fid": "d94d3a9e-9d19-4036-aa55-858cd485a0eb", "reference": "ref-relief.wav"}
```

The audio is a WAV (215,084 bytes here, 4.5 s at 24 kHz): decode
`audio_base64` to a file to hear it. `seed` is the seed the engine used (the
one sent, fitted into its range), `time_used` the engine's seconds, `reference`
the clip the app spoke with (`ref.wav` when the persona lacks the one asked
for).

```bash
# Is the voice on, and which engine answers?
curl -s http://127.0.0.1:8010/api/tts/health
```

```
{"enabled":true,"available":true,"streaming":true,"server_type":"faster-qwen3-tts"}
```

```bash
# The engine's capabilities, through the app (the start of 3,671 bytes)
curl -s http://127.0.0.1:8010/api/tts/capabilities | head -c 300
```

```
{"schema_version":2,"engine":"faster-qwen3-tts","model":"Qwen/Qwen3-TTS-12Hz-1.7B-Base","device":"cuda","sample_rate":24000,"watermarked":false,"endpoint":"/synthesize","reference_audio":{"required":true,"formats":["wav","mp3","ogg","flac"],"min_duration_s":2.0,"max_duration_s":null,"note":"referenc
```

### §3.4 Whisper (`app/routers/stt.py`)

| Endpoint | What it does |
|---|---|
| `GET /api/stt/health` | is speech recognition on and reachable |
| `POST /api/stt` | transcribes audio, `{"audio_base64", "audio_mime_type"}` — the chat's microphone; the show uses `/api/show/listen` instead (the cast's names as a hint, the confidence numbers) |

```bash
# Is Whisper on and reachable?
curl -s http://127.0.0.1:8010/api/stt/health
```

```
{"enabled":true,"available":true}
```

Both transcription routes take the audio as base64 in a JSON body. With a WAV
file — here, the chunk of §3.3: Moira's voice saying a listener's words:

```bash
# The body of /api/stt from a WAV file (the audio as base64)
python3 -c "import base64,json,sys; print(json.dumps({'audio_base64': base64.b64encode(open(sys.argv[1],'rb').read()).decode(), 'audio_mime_type': 'audio/wav'}))" marta.wav > stt-body.json
# Transcribe it, as the chat does
curl -s -X POST -H 'Content-Type: application/json' -d @stt-body.json http://127.0.0.1:8010/api/stt
```

```
{"text":" Hello, this is Marta. I can hear you from a farmhouse outside Bastrop.","language":"en","language_probability":0.99658203125}
```

```bash
# The same audio as the show hears it: add the run's id to the body, and send it to /api/show/listen
python3 -c "import json,sys; d=json.load(open('stt-body.json')); d['run_id']=sys.argv[1]; print(json.dumps(d))" "$RUN" > listen-body.json
curl -s -X POST -H 'Content-Type: application/json' -d @listen-body.json http://127.0.0.1:8010/api/show/listen
```

```
{"text":"Hello, this is Marta. I can hear you from a farmhouse outside Bastrop.","no_speech_prob":0.039093017578125,"avg_logprob":-0.22176845913583582,"words":[{"word":"Hello,","probability":0.70947265625},{"word":"this","probability":0.98095703125},{"word":"is","probability":0.99609375},{"word":"Marta.","probability":0.9814453125},{"word":"I","probability":0.994140625}, …
```

The show's route returns what the show's silence filter and the page's caption
need: `no_speech_prob` and `avg_logprob` (the filter: words or silence) and each
word's probability (the caption's three bands of confidence); the chat's route
returns the text and the language. Both heard the voice word for word.

### §3.5 The personas — the voices the app found (`app/routers/personas.py`)

Eight routes, upstream TalkWithMe's persona editor: list, detail, create, update,
delete, clone, the avatar, the reference audio. For the show, the read-only
ones answer "which characters and voices did the app load?":

```bash
# Every persona the app found, and whether each has a voice
curl -s http://127.0.0.1:8010/api/personas
```

```
[{"name":"Daniel","description":"Dr. Daniel Hayworth, systems engineer keeping the lab alive","avatar_color":"#B5651D","avatar_image":false,"tts_capable":true},{"name":"Moira","description":"Dr. Moira Byrne, microbiologist studying the outbreak","avatar_color":"#4A7C59","avatar_image":false,"tts_capable":true},{"name":"Ralph","description":"Dr. Ralph Okafor, security officer holding the perimeter" …
```

```bash
# One persona in full: its system prompt (the chat's; the show uses the story's cast sheet), its voice files (the start)
curl -s http://127.0.0.1:8010/api/personas/Daniel/detail | head -c 300
```

```
{"name":"Daniel","description":"Dr. Daniel Hayworth, systems engineer keeping the lab alive","system_prompt":"/no_think\nYou are Dr. Daniel Hayworth, systems engineer of a besieged research lab during a zombie outbreak, speaking over the lab's shortwave radio.\nDry British understatement; competent, tired, quietly heroic. Every transmission is one or two short SPOKEN sentences — this is radio, n
```

```bash
# A persona's reference voice (ref.wav), saved to listen to: the HTTP status, the type and the size
curl -s -o /tmp/daniel-ref.wav -w '%{http_code} %{content_type} %{size_download}\n' http://127.0.0.1:8010/api/personas/Daniel/reference-audio
```

```
200 audio/wav 439270
```

(On 2026-10-01 the call was made with the bytes counted, not saved.) The
avatar: `GET /api/personas/Daniel/avatar` → **404** "No avatar configured" —
the cast has none.

### §3.6 Settings (`app/routers/settings.py`)

```bash
# The settings the app loaded (llm, tts, stt, general)
curl -s http://127.0.0.1:8010/api/settings
```

```
{"llm":{"base_url":"http://localhost:8080","model":"default","max_tokens":200,"temperature":0.8},"tts":{"enabled":true,"base_url":"http://localhost:8001","timeout":60.0,"streaming":true,"parameters":{}},"stt":{"enabled":true,"base_url":"http://localhost:8002","timeout":30.0},"general":{"persona_name_mentions":true,"max_persona_replies":4,"max_turns_for_context":50,"show_tool_calls":true,"enable_pe …
```

**A gap:** the reply has only `llm`, `tts`, `stt` and `general` — **not the
show's settings** (`show:` is yaml-only; `llm.max_tokens` 200 here is the
chat's, not the show's 512). The show's settings are seen in the fork's
`settings.yaml`, or in a run's start reply (`debug`, `voice_seed`, the seed) and
its record. `PUT /api/settings` writes `settings.yaml` (the chat's settings
page) — not called.

### §3.7 The chat (upstream TalkWithMe): rooms, session, chat, history

`/api/chatrooms` (8 routes), `/api/session` (4), `POST /api/chat` (a streamed
reply), `/api/persist/…` (4: audio, a message, a room's history) — the chat UI
at `/talkwithme`. Not the show's; read-only calls on 2026-10-01:

```bash
# The rooms, including the implicit default
curl -s http://127.0.0.1:8010/api/chatrooms/all
```

```
[{"name":"default","persona_names":["Daniel","Moira","Ralph","Samantha"],"echo_chamber":false}]
```

```bash
# The chat session (empty), and a room's stored history
curl -s http://127.0.0.1:8010/api/session
curl -s http://127.0.0.1:8010/api/persist/history/default
```

```
{"history":[],"active_personas":["Daniel","Moira","Ralph","Samantha"],"current_room":"default"}
{"room":"default","message_count":0}
```

**Not called, because they change state:** every `POST`, `PUT` and `DELETE`
of personas, rooms, session, chat, persistence and settings — and one **`GET`
that is not read-only**: `GET /api/session/load-room/{room}` replaces the active
session's history with the room's stored one.

### §3.8 The pages

`GET /` → **307**, a redirect to `/show`. `GET /talkwithme` — upstream's chat UI.
`GET /show` — the show (§3.2). `/static/…` — the page's scripts, styles and
images.

## §4. Recipes — a part of the app at a time, layer by layer

Three layers: **the model services** (on the box, through the tunnel), **the
app's routes**, **the page**. Test the lowest layer that can show the problem.

### §4.1 The model services alone (no app)

```bash
# The tunnel and the three services (each must say 200)
for u in localhost:8080/health localhost:8001/capabilities localhost:8002/docs; do printf '%s ' "$u"; curl -s -m 3 -o /dev/null -w '%{http_code}\n' "$u"; done
```

```
localhost:8080/health 200
localhost:8001/capabilities 200
localhost:8002/docs 200
```

```bash
# llama.cpp: the context it runs with, and its slots
curl -s localhost:8080/props | python3 -c "import json,sys; d=json.load(sys.stdin); print('n_ctx', d['default_generation_settings']['n_ctx'], '| slots', d['total_slots'])"
```

```
n_ctx 32768 | slots 1
```

```bash
# llama.cpp: how many tokens a text is (the start token included)
curl -s localhost:8080/tokenize -H 'Content-Type: application/json' -d '{"content": "Over.", "add_special": true, "parse_special": true}'
```

```
{"tokens":[1,5238,1046]}
```

```bash
# llama.cpp: the prompt exactly as the model reads it, for some messages (no generation)
curl -s localhost:8080/apply-template -H 'Content-Type: application/json' -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

```
{"prompt":"<SPECIAL_10>System\n\n<SPECIAL_11>User\nHello\n<SPECIAL_11>Assistant\n<think>\n"}
```

**A round's model request, again, without the app.** With `show.debug` on,
each round leaves `runs/<run-id>/debug/rNNN.request.json`, the exact body the
app sent — the messages, the grammar, `max_tokens`, the seed, `"stream": true`
(the fork's `docs/runbooks/show-driver.md`, "Look inside a round"). One model
request:

```bash
# Send round 1's request again, straight to llama.cpp (from the fork's root); the reply streams back as data: lines
curl -s localhost:8080/v1/chat/completions -H 'Content-Type: application/json' -d @runs/2026-10-01T14-05-43/debug/r001.request.json
```

The stream (116 lines) is llama.cpp's own (OpenAI-style `choices[].delta`),
the first two:

```
data: {"choices":[{"finish_reason":null,"index":0,"delta":{"role":"assistant","content":null}}],"created":1790881578,"id":"chatcmpl-AA6tN7zuCc5MORfJ8VkiaegyWkrgRG05","model":"bartowski/nvidia_NVIDIA-Nemotron-Nano-9B-v2-GGUF:Q4_K_M","system_fingerprint":"b11096 …
data: {"choices":[{"finish_reason":null,"index":0,"delta":{"content":"S"}}], …
```

Joined, the deltas give the reply **word for word as the run recorded it** —
the request carries its seed (43): "Samantha (calm): We are scientists trapped
in a lab near a wood and a swamp. Our radio is dead—only transmission. Over."
and "Daniel (doubtful): The virus… it’s mutating. We don’t know how. Over." —
and the last chunk's `timings`: `prompt_n` 4, `cache_n` 555, `predicted_n` 56
(the prompt was still in the server's cache from the round itself). The same
request and seed gave the same words here, minutes later — as they did 80
minutes apart on 2026-09-22 (the TODO's Task 7). It is how a bad round is
studied without the app.

**Does the grammar bind?** The driver's `--control` sends one request straight
to llama.cpp, with a run's cast sheet and a grammar that allows only a speaker
absent from the cast — "Operator"; every line must come back as Operator's (the
same runbook, "Check that the grammar binds"). One model request:

```bash
# The grammar check, with the cast sheet of a run (default: the newest), from the fork's root
.venv/bin/python scripts/drive_show.py --control --run-id 2026-10-01T14-05-43
```

```
control, with the cast sheet of runs/2026-10-01T14-05-43/script.json
control reply:
  Operator (calm): We're running low on supplies. Over.  
  Operator (urgent): We need more than just food—we need a way to stop this. Over.
control: PASS — every line is Operator's
```
- **The voice engine, the memory:** this repository's
  `docs/runbooks/box-inspection.md` (`nvidia-smi`, the services' logs, the model
  against its context).

### §4.2 The show engine without the voice or the page: `scripts/drive_show.py`

The fork's driver uses only `POST /api/show/start` and `POST /api/show/round`:
it opens a run, asks for round after round, prints each line as it streams and
each round's summary, and can judge the drive (`--report`). It **does not
synthesize voices**: the page normally reports the seconds of audio played,
which the director's cadence counts (when the receiver comes back); the driver
reports `--played` seconds per round instead (20 by default). It answers each
listening window with the next `--heard` text (`-` is a silent window), or with
silence; `--speak` sends those words the real way instead — spoken by the app's
voice, transcribed by `/api/show/listen`.

```bash
# 220 rounds with 36 listener answers (only two shown here), and the report (from the fork's root, the app serving)
.venv/bin/python -u scripts/drive_show.py --base http://127.0.0.1:8010 --rounds 220 --played 20 --report --heard "Hello? This is Marta, I can hear you. I'm in a farmhouse outside Bastrop." --heard "Yes, I'm alone with my two dogs. The roads east are blocked by cars."
```

From the drive of 2026-10-01 (`2026-10-01T13-43-41`), the end:

```
220 rounds · 529 lines · 0 dropped · average round 1.65s · script after the last round: 22595 tokens
record: runs/2026-10-01T13-43-41/script.json
  PASS  220 of 220 rounds played and recorded (10 needed)
  PASS  speakers and line counts obey the director: 529 lines (127 fixed, outside the director's limits), 0 dropped
  …
6 of 6 criteria pass
```

**Why it was the right tool for the 32k test:** the trim depends only on how
many tokens the script holds, and the voice's memory does not change with the
context; a browser would only add voice requests to the box. Listener answers
make contacts — the heaviest rounds (an exchange's share: a median of 263
tokens, up to 741, over 218 exchanges recorded), so the context fills fastest. Cost: one model request
per round (about 1.6 s each); no voice requests. The report's two checks that
failed on the first drive were the report's own gaps — it predated the fixed
lines — fixed on the same branch (the fork's `scripts/drive_show.py`: the
director's limits checked on the model's lines only; a round without a model
request has no size to check).

### §4.3 The voice alone: `POST /api/tts` and `scripts/replay_chunk.py`

With `show.debug` on, every chunk the page asked for is kept in
`runs/<run-id>/debug/audio/` — the audio and a `.json` of what made it (the
fork's `docs/runbooks/show-page.md`, "Every chunk the voice said, kept"). The
fork's `scripts/replay_chunk.py` asks `POST /api/tts` for it again — the same
persona, clip, text and seed — and tells whether the new audio is
byte-identical; `--seed N` tries another seed. One voice request per chunk.

```bash
# Say one kept chunk again, with the seed it was said with (the app must be serving)
python3 scripts/replay_chunk.py runs/2026-09-30T18-51-36/debug/audio/r001-l1-c1-Daniel-ref-fear.json
```

```
r001-l1-c1-Daniel-ref-fear.json: seed 97 (kept: 97), 3.28 s (kept: 3.28 s), engine 1.1230215200012026 s; byte-identical to the kept chunk
  -> runs/2026-09-30T18-51-36/debug/audio/r001-l1-c1-Daniel-ref-fear.replay-seed97.wav
```

(Output of 2026-09-30.) That is how Daniel's "It's watching us. Over." was
traced to his fear clip on 2026-09-30 (the voice-datasets discussion, §11.13).

### §4.4 Whisper alone

`POST /api/show/listen` (with a run's id) or `POST /api/stt` transcribe a
recording sent as base64 — commands and outputs in §3.4, with the app's own
voice as the speaker (a chunk from `POST /api/tts`). The driver's `--speak`
does the same inside a drive: it has the operator's voice say each `--heard`
item and sends the audio to `/api/show/listen`. One Whisper request each.

### §4.5 The page

Only what the layers below cannot show — timing by ear, the looks, the
microphone, the browser's cache (a reload must fetch new scripts: Cmd+Shift+R)
— needs the page: the fork's `docs/runbooks/show-page.md`.

## §5. What this exercise found

- **FastAPI's `/docs`** — an interactive list of every endpoint, with a form for
  each body — was there all along and is the fastest way to try one endpoint.
- **`GET /api/settings` does not show the show's settings** (§3.6).
- **A `GET` that changes state:** `GET /api/session/load-room/{room}` (§3.7) —
  upstream's; worth knowing before calling it "to look".
- **The trim cuts below its target** when the trimmed rounds include a Repair
  (§2.3) — harmless; a refinement noted, not built.
- **The driver's report predated the fixed lines** (§4.2) — fixed.
