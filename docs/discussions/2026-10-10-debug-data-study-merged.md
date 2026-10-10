# The debug data — a study, question by question

**Date:** 2026-10-10 · **Arc:** MVP prototype · **Branch:** `alfre2v/talk-prep`
**Type:** discussion — the debug study session ([discussion 2026-10-10] talk-preparation, workstream D): first the
outputs and the questions the owner chose and copied by hand (Parts 1-5, with the owner's follow-up questions added
before the answers to them), then what else the session produced that those parts do not already hold (Part 6).
**Status:** the session done; its improvements written down as the follow-up "Debug and observability improvements",
not to be built before the demo. The code's line numbers are the fork's at **`tz-0.9`** (`b1d039c`); paths starting
`app/` or `static/` are in the fork, `/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`; the runs are in the
installed client's `~/TalkWithZombies-client/runs/`.

## Part 1. The session's summary (the agent)

### The run's folder, and the fields worth knowing (4.a)

| File | What it holds | The most useful fields |
|---|---|---|
| `script.json` | **the record:** one entry per round | `kind`, `speakers`, `event`, `tone`, `overtone`, `cue`; `lines` (`raw` as the model wrote it, `spoken` as voiced, `fixed`); `played_s`; `timings` (token counts only); `tokens`, `trims` |
| `debug/rNNN.txt` | **the round, readable:** what the model was asked | the seed, `finish`, the **token check** (the prompt's size as rendered against what the server read: "difference 0"); the **grammar**; **the prompt exactly as the model read it** |
| `debug/rNNN.request.json` | **the request** to llama.cpp, raw | `messages`, `grammar`, `seed`, `max_tokens`, `temperature` |
| `debug/audio/rNNN-lL-cC-<who>-<clip>.wav` | **every voice chunk,** as heard | the audio itself |
| `debug/audio/….json` | **the chunk's record** | `text`, `persona`, the reference clip asked for and used (and its SHA-256 and transcript), `seed_asked`; **`kept`** (when, to the ms); `reply`: **`time_used`** (synthesis seconds), **`rtf`** (below 1 = faster than real time), the seed used |

### The console in debug mode (4.b)

The console is **quieter than you might expect:**
- **with debug on,** only **the sounds** speak:
  - the bed: each shuffle, each clip with its gain, each silence;
  - the ambience: each shuffle, each texture, each spot, **each cue** (`cue, spot: <file>`), each silence, the A and F keys;
- **always, debug or not,** the problems: a voice chunk that couldn't be said, a microphone that couldn't open, a failed transcription, a sound that wouldn't play, a broken stream event, and the show's errors.
- **The rounds themselves log nothing.** Their information (kind, event, tone, cue, timings, which clip spoke each line) is in the **debug line under each round** on the page, and in the files above.

### Easy improvements, in order of value (4.c)
1. **Keep llama.cpp's times** (`app/services/llm.py:166-168`): two more keys. The record would then say how long the model spent reading and writing each round, the one timing missing today.
2. **Log the mic's open and close in the console,** with how long `getUserMedia` took. It tests hypothesis 1 directly, a few lines in `mic.js`.
3. **One console line per round:** its kind, event and cue, time to the first line, time to the first sound, and the gap before it. The page already computes those numbers for the debug line.
4. **A script that does today's analysis** from any run's folder (the real-time factor, the stalls, the gaps between rounds), so the next investigation doesn't start from scratch.

**Three questions:**
1. **During that long run,** were you on a **Bluetooth** headset, wired, or the Mac's speakers? And did the pauses sound like **the voice going silent,** or like **all the sound** (static and ambience too) cutting out briefly? The answer points at the mic or away from it.
2. **Which improvements** do you want, and when? 1 and 2 are small, and 2 would settle hypothesis 1 in the next show.
3. **Save this session** like the others, as `2026-10-10-debug-data-and-the-pauses.md`?

## Part 2. The owner's questions

Some questions from me:

* Correct me if I am wrong: what you can observe directly is `debug/rNNN.request.json`, which is our request to llama server. In contrast `debug/rNNN.txt` is an internal state of llama server, after it parses the requests we send it. Right? How do we get access to `debug/rNNN.txt`? I remember there was an endpoint for this, right?
* Explain the timings that we requests llama.cpp to add to the response, and show me where I can see them in our debug data from a previous run. I remember there was an alternative representation that was OpenAI compatible but we chose to go with the llama representation... A lot of our functionality depends on those llama provider timing measurements... Can you list which?
* On whisper, I remember we added some special fields to declare the name of the cast as possible words so the model would make less mistakes with the cast names... Please remind me the details, and can we see an example of the actual format in our debug data?
* On the TTS side, did we expand the request to include any special fields to give us some extra data?

## Part 3. The agent's answers

Good: a Bluetooth headset fits hypothesis 1 well. I'll hold the file until our discussion settles, and the improvements go into one follow-up.

Your four questions are about exactly what the app sends and receives, so I'll answer them from the code rather than from memory. First, how `rNNN.txt` is made, and where the app uses llama.cpp's timings:

Now every place the app uses llama.cpp's timings, and the Whisper and voice requests (the fields the app adds, and what it reads back):

I've confirmed llama.cpp's endpoints and Whisper's hint. Now I'll trace how script.py tallies timings into the context, check the app's tts-serve request/response, and pull a Whisper example from a listener turn in the long run.

I still need to confirm whether the app explicitly requests timings or if they're always sent by default. I'll check the round's request body (`round_payload`) and pull up a round from your long run where a listener spoke, using the Whisper example.

Here are your four questions, each from the code. `app/...` paths are in the fork.

### 1. `rNNN.request.json` and `rNNN.txt`

The first half is right; the second needs a correction.
- **`rNNN.request.json`** is exactly **our request** to llama.cpp: the body we post (`messages`, `grammar`, `seed`, `max_tokens`, `temperature`), kept so a round can be replayed with `curl`.
- **`rNNN.txt` is not llama.cpp's internal state.** It's **written by our app** (`app/show/debug.py`, `write_round`). To build it, the app makes **two extra calls** to llama.cpp, after the round:
  - **`POST /apply-template`** (`app/services/llm.py:176`): *"render these messages the way the model reads them"*. llama.cpp applies the model's **chat template** and returns the exact prompt text, with the special tokens and role markers, and without generating anything. **That's the endpoint you remember.** It gives the file's "the prompt as the model read it" section.
  - **`POST /tokenize`** (`llm.py:190`): counts that rendered prompt's tokens, for the **token check**. It compares that count with what the server says it read (`prompt_n + cache_n`). "Difference 0" means our view of the prompt and the model's agree exactly.
  - The rest of the file is ours: the seed, `finish`, the `timings` line, the grammar, and the reply as it streamed.

### 2. llama.cpp's timings
- **We don't ask for them.** The round's request body (`round_payload`, `llm.py:135`) is the chat payload plus `grammar`, `max_tokens` and `seed`. **llama.cpp adds a `timings` object to the stream's last chunk by itself.** It's llama.cpp's own extension to the OpenAI-style response.
- **The OpenAI-style alternative** is `usage`. In a stream it comes only if asked for (`stream_options`), and we don't ask (`llm.py:153`: *"a stream carries no usage unless asked for, and we do not ask"*). So you remember right: we chose **llama.cpp's representation.** Its advantage is that it splits **what was read fresh** from **what came from the cache.**
- **The three numbers we keep** (`llm.py:166-168`):
  - **`prompt_n`:** tokens of the prompt read **fresh** this time;
  - **`cache_n`:** tokens of the prompt **reused from the cache** (the script so far, unchanged since the last round);
  - **`predicted_n`:** tokens the model **wrote.**

  llama.cpp also sends the **times** (`prompt_ms`, `predicted_ms`, and per-second rates); **we drop them.**
- **Where to see them:** `script.json`, each round's `timings`; and line 2 of each `debug/rNNN.txt`. Round 9 of your long run had `{"prompt_n": 186, "cache_n": 1368, "predicted_n": 16}`: it read 186 new tokens, reused 1,368, and wrote 16.
- **What depends on them:**
  1. **The script's size** (`_size`, `app/show/script.py:148`): `prompt_n + cache_n + predicted_n` is the whole script's size in tokens, as the model actually counted it.
  2. **The trim** (`trim`, L177): when that size reaches the trigger (90% of the budget), whole rounds are cut until it's back to the target (50%). It's what keeps the show from overflowing the 32k context.
  3. **Each round's share** (`round_share`, L201): how many tokens a round added, recorded as its `tokens`. The trim uses it to know how much cutting a round frees.
  4. **Rounds the model didn't write** (`known_size`, L160): a Repair is all fixed lines and gets no timings, so the size steps back to the last round that has them.
  5. **The token check** in the debug files (`debug.py:129`).

  The start's check against the model's context uses **`/props`** (`n_ctx`), not the timings.

### 3. Whisper: the cast's names as a hint
- **The request** (the listen route, `app/routers/show.py:271`, and `transcribe_for_show`, `app/services/stt_client.py:104`):
  - **`prompt`: the cast's names, joined** (`", ".join(story.cast)`), i.e. **"Daniel, Moira, Ralph, Samantha"**. Whisper's prompt is text it treats as "what came just before", so it nudges the decoding toward those words and spellings;
  - `language`: the show's `stt_language`;
  - `vad_filter: true`: silence is cut before decoding;
  - `response_format: json`: our Whisper server rejects `verbose_json`, but its `json` already carries the per-segment confidence.
- **What comes back and is kept:** the text; `no_speech_prob` (the highest across segments); `avg_logprob` (their average); each word with its probability. The transcript filter uses them to decide words or silence.
- **In your debug data:** the **request isn't kept anywhere,** only its result. An example from your long run, **round 16** (an exchange), in `script.json`:

  ```json
  "heard": {
   "text": "Hello, hello, can you hear me? This is saiyun pepper",
   "no_speech_prob": 0.1248779296875,
   "avg_logprob": -0.4986979067325592,
   "silence": null
  }
  ```

  And in `debug/r016.txt`, line 4: `listener: heard '…' | no_speech_prob … | avg_logprob … | words …`, with every word's probability. ("Saiyun pepper" is the hint's limit: it helps the cast's names, not yours.)

### 4. The voice: any special fields?

**Not on the voice server's side.** We added fields only between **the page and our app.**
- **The page → our app** (`POST /api/tts`, built by `voiceRequest` in `player.js`): `text` and `persona_name` (upstream's); then ours:
  - **`reference`:** the mood's clip, e.g. `ref-fear.wav`;
  - **`seed`:** when `voice_seed` is on;
  - **`debug`:** the tag `<run-id>/r009-l2-c1`, which tells our app to keep the chunk.
- **Our app → tts-serve** (`build_synthesis_payload`, `app/services/tts_client.py:452`): `text`, the reference clip as `audio_base64`, its `reference_text` (the transcript), `language`, the engine's parameters, and `seed`. Each is sent **only if the engine advertises it** in its capabilities.
- **What comes back:** `audio_base64`, `sample_rate`, **`seed`** (the one used), **`time_used`**, **`rtf`** and `fid`. These are **tts-serve's standard reply;** we didn't ask for anything extra. What we added is **keeping** them: in debug mode the whole reply, minus the audio, goes into each chunk's `.json`. And our app tells the page which clip it used (`reference`).

**For the improvements follow-up,** your questions add one: **keep the Whisper request** (the prompt and the language) in the debug files, next to what it heard.

Anything more to discuss before I write the session file and the follow-up?

## Part 4. The owner's follow-up questions

> Just checking if I understand "1. rNNN.request.json and rNNN.txt":
>
> * Saying it was "llama.cpp internal's state" may not have been the best phrase, but I meant that we had to ask llama
>   for it (POST /apply-template), we do not build that file ourselves, therefore, in my book, it's a llama.cpp
>   generated file, computed from its internal state, not by us, we save what llama gives us.
> * What do you mean "The rest of the file is ours"... The rest of what file?
>
> On "2. llama.cpp's timings":
>
> * Ok, so we do not have to add anything to the request to llama.cpp for it to include the timings. However we could
>   ask for the the OpenAI-style alternative `usage` ... (would that be in addition to timings, or replacing the
>   timings?)

## Part 5. The agent's answers to the follow-up questions

### 1. The two files

**The prompt section is llama.cpp's own output, saved verbatim.** That's how you meant it, and it's right. We send the messages to `POST /apply-template`, llama.cpp renders them with the model's chat template, and we save exactly the text it returns. We don't build that text. (A precision on "internal state": `/apply-template` is a pure rendering, the model's template applied to our messages. It doesn't read the model's live memory, like its cache. But it's llama.cpp's rendering, not ours.)

**"The rest of the file"** meant **the other sections of `rNNN.txt`.** The file is written by our app (`write_round`, in `debug.py`), and it's assembled from several sources:

| Section of `rNNN.txt` | Where it comes from |
|---|---|
| line 1: the round, its kind, the run | our record |
| line 2: the seed, `max_tokens`, `finish`, **`timings`** | our request, and the last chunk of llama.cpp's stream |
| line 3: **the token check** | computed by us: llama.cpp's `/tokenize` count against its `prompt_n + cache_n` |
| the listener line (after a turn) | Whisper's result, as we kept it |
| **the grammar** | ours (`build_grammar`) |
| **the prompt as the model read it** | **llama.cpp's `/apply-template`, verbatim** |
| the reply as it streamed | llama.cpp's tokens, as we received them |

So the file is ours, and one of its sections is llama.cpp's rendering, kept untouched.

### 2. `usage`: in addition, not instead

As far as I know, **llama.cpp sends `timings` regardless,** and `usage` would come **in addition** when asked for, with `stream_options: {"include_usage": true}` in the request. It would arrive as one more piece of data at the end of the stream. But `usage` carries less:
- **`usage`:** `prompt_tokens` (everything read, fresh and cached **together**), `completion_tokens` (written) and `total_tokens`;
- **`timings`:** the same counts, but with the prompt **split** into `prompt_n` (fresh) and `cache_n` (reused), plus the **times**.

So `usage` would add nothing we need. And the split is what showed today that the model reads only about 200 new tokens a round thanks to its cache. (The arithmetic: our script's size, `prompt_n + cache_n + predicted_n`, equals `usage`'s `total_tokens`.)

This is from memory of llama.cpp's API, not checked on our server. If you want it confirmed, one `curl` with and without `include_usage` settles it, next time the 3090 or the A6000 is up.

## Part 6. More from the session

### The owner's closing remark

The owner (verbatim): "I am glad that I asked this follow up, I did not look carefully enough to the `rNNN.txt` files to
realize there were these other fields you document above, I only remembered that we saved there the output of
`/apply-template`... This is a very important information to save."

### Where the session started

The owner's plan of 2026-10-10 (verbatim), its fourth item:

> (4) You and me explore together the information stored in the last run debug:
> (4.a) Help me navigate the stored debug js file. What are the most useful fields stored per row?
> (4.b) Remind me all the information that comes in the console when we are in debug mode.
> (4.c) Any easy improvements we could do the debugging? Things we could easily add to the debug console for example
> that would proof useful?

### Earlier: how to know a sound cue worked (2026-10-07)

During the first live check of sound cues, the owner (verbatim): "How would I even know that the feature worked? What
message should I expect in the console?"

The agent (verbatim):

> Here's exactly what you'd see, from the code. **Debug is on in this app, so both logs are active.**
>
> **1. The browser's console** (Chrome: View → Developer → JavaScript Console, or ⌥⌘J). When a cue plays,
> `ambience.js` writes one line:
>
> ```
> Show: ambience cue, spot: explosion-4.mp3
> Show: ambience cue, texture: thunderstorm-2.mp3
> ```
>
> The random ambience writes lines without the word "cue", so you can tell them apart:
>
> ```
> Show: ambience spot: dead-shriek-1.mp3
> Show: ambience texture 3 of 16: dead-restless-1.mp3
> ```
>
> Typing `cue` in the console's filter box leaves only the cues. These are `console.info` lines, which Chrome shows at
> its default levels.
>
> **2. The app's log**, which I'm watching (it does show INFO lines; I checked). The server writes the line the moment
> it matches the event, before the round's first line streams:
>
> ```
> … INFO     app.routers.show: Show run 2026-10-07T18-…, round 7: the event cues explosion-4.mp3 (spot)
> ```
>
> **3. By ear and on the page:** the sound starts as the reader starts speaking the event, and the same event appears as
> that round's stage direction.
>
> **4. Afterwards, in the run's record:** each round in `runs/<run>/script.json` has `"cue": "explosion-4.mp3"`, or
> `null`.
>
> **A gap I'd close now:** the **debug line under each round** on the page (round, kind, speakers, event, tone…) doesn't
> mention the cue. It's the place you look anyway, so it should say `cue explosion-4.mp3` when there is one. That's one
> line in `debugLine` (`static/show/show.js`) plus an assertion in its test. The page picks it up on a reload, with no
> restart.

The owner: "yes, add the cue to the debug line, then catch-all test". The debug line now names a round's cue after its
event — e.g. `round 7 · free · speakers Daniel, Moira · event An explosion rattles the windows. · cue explosion-4.mp3 ·
tone grim · first line 0.5 s · round 2.0 s · run 2026-10-07T18-40-00` (the page test "debugLine: a cued round names its
cue after the event"); shipped in the fork's `tz-0.9`.

### Earlier: what `debug: true` turns on (2026-10-08)

Asked for the settings of the live test of 2026-10-07 ("Show me the settings as you had them for the live demo
yesterday"), the agent listed its three test lines; the third (verbatim):

> - `debug: true`: the debug line under each round (with `cue <file>`), the console's `Show: ambience cue…` lines, and
>   the run's debug files in `runs/<run>/debug/`, including every voice chunk.

### The run studied

The agent (verbatim): "Your long 3090 run is **`2026-10-08T14-57-55`: 206 rounds, with debug, and 518 voice chunks
kept.** The evening runs (22:16 and 22:31, the OBS recordings) have no debug files, so you'd taken the test lines out by
then."

### The examples behind the folder's table: the record

The run's folder holds `script.json` and `debug/`; `debug/` holds 413 entries (two files per round, and `audio/`). The
record's top-level fields: `run_id`, `started`, `story`, `cast` (4), `moods`, `seed` (651594682), `systems`, `episode`,
`rounds` (206). One round in full — round 9, a free round with an event and a cue (its instruction and lines shortened
here as they were shown):

```json
{
 "n": 9,
 "kind": "free",
 "played_s": 80.63979591836734,
 "instruction": "Something happens that the listeners cannot see, and Daniel has just told them on air: \"Far away a siren wails, then another joins it, then another.\" Carry on f…",
 "listener": null,
 "heard": null,
 "speakers": ["Daniel", "Moira", "Samantha"],
 "max_lines": 1,
 "event": "Far away a siren wails, then another joins it, then another.",
 "tone": "darkly comic",
 "lines": [
  {"speaker": "Daniel", "mood": "curious",
   "raw": "Daniel (curious): Far away a siren wails, then another joins it, then another. Over.",
   "spoken": "Far away a siren wails, then another joins it, then another. Over.", "fixed": true},
  {"speaker": "Samantha", "mood": "doubtful",
   "raw": "Samantha (doubtful): Sirens? Over.  ", "spoken": "Sirens? Over.", "fixed": false}
 ],
 "dropped": [],
 "timings": {"prompt_n": 186, "cache_n": 1368, "predicted_n": 16},
 "finish_reason": "stop",
 "trimmed": false,
 "tokens": 98,
 "trims": [],
 "episode": "",
 "overtone": "neutral",
 "agenda": null,
 "slot": null,
 "recollects": null,
 "cue": "sirens-1.mp3"
}
```

The agent (verbatim):

> The record holds, per round:
>
> - **what the director chose:** kind, speakers, line budget, event, tone, overtone, `cue`;
> - **what was said:** each line's speaker, mood, `raw` text as the model wrote it, `spoken` text as voiced, and `fixed`
>   (a line read word for word, like the event);
> - **the context's accounting:** `timings`, `tokens`, `trims`;
> - **`played_s`:** the audio played before this round was asked for.
>
> Round 9 above is a free round whose event was the sirens, and it cued `sirens-1.mp3`.

And, said about the same record: `timings` holds only **token counts** (`prompt_n`, `cache_n`, `predicted_n`), **no
milliseconds** — the record cannot say how long the model took (below: "The app drops llama.cpp's times").

### The examples behind the folder's table: a round's debug files, and a voice chunk's record

As shown in the session — round 9's `debug/r009.txt` (its head):

```
round 9 (free) of run 2026-10-08T14-57-55
seed 651594691 | max_tokens 512 | finish stop | timings {"prompt_n": 186, "cache_n": 1368, "predicted_n": 16}
token check: the rendered prompt has 1554 tokens; the server read 1554 (prompt_n + cache_n); difference 0

== grammar ==
root    ::= pinned
pinned  ::= "Samantha" " (" emotion "): " text "\n"
emotion ::= "calm" | "doubtful" | "urgent" | "curious" | "determined"
text    ::= [^\n\[\]()]+

== the prompt as the model read it (/apply-template) ==
<SPECIAL_10>System
You write a live radio play. Four scientists are trapped in a besieged research lab during a zombie outbreak, …
```

(74 lines in all.) `debug/r009.request.json`'s keys: `model` (`default`), `messages` (18), `max_tokens` (512),
`temperature` (0.8), `stream` (true), `grammar`, `seed` (651594691). Round 9's voice chunks in `debug/audio/`:
`r009-l1-c1-Daniel-ref-realization.json` and `.wav`, `r009-l2-c1-Samantha-ref-confusion.json` and `.wav`. The first
chunk's `.json`:

```json
{
 "tag": "2026-10-08T14-57-55/r009-l1-c1",
 "kept": "2026-10-08T14:59:42.996",
 "persona": "Daniel",
 "text": "Far away a siren wails, then another joins it, then another. Over.",
 "language": "en",
 "reference_asked": "ref-realization.wav",
 "reference_used": "ref-realization.wav",
 "clip": "/Users/alfredo/TalkWithZombies-client/Personas/Daniel/ref-realization.ogg",
 "clip_sha256": "be56480536c197cd9a4ac174585e4ca2ede8f6386f819d7d2945f9bd0a113093",
 "transcript": "Wow, I never know that the body was made up of 75% water. Did you know that a flamingo is actually white but turns pink because it eats too many shrimp? Apparently dolphins sleep with one eye open.",
 "seed_asked": 651594682,
 "reply": {
  "sample_rate": 24000,
  "seed": 682,
  "time_used": 1.7690350830000625,
  "rtf": 0.4335870301470741,
  "fid": "8e021e9e-cbf2-48c8-9829-baa90b3215f8"
 }
}
```

The agent (verbatim):

> These are the most useful fields. Each voice chunk's `.json` holds:
>
> - **`kept`:** when the app saved the chunk, to the millisecond;
> - **`time_used`:** how long the voice server took to synthesize it, here **1.77 s**;
> - **`rtf`, the real-time factor:** synthesis time divided by the audio's length, here **0.43**. Below 1 means faster
>   than real time: this 4.1-second chunk was made in 1.8 s.

### The app drops llama.cpp's times

The agent checked whether llama.cpp sends times and the app drops them (verbatim): "Confirmed: **the app drops
llama.cpp's times.** `app/services/llm.py:166-168` keeps only `prompt_n`, `cache_n` and `predicted_n` from llama.cpp's
`timings`. llama.cpp also reports how long it spent reading the prompt and writing, but those are thrown away."

### The console's messages, file by file

The page's console messages, as listed in the session (`static/show/`):

```
mic.js:34          console.warn("Show microphone: not available:", err);
mic.js:46          console.warn("Show microphone: could not open:", err);
bed.js:205      if (show.run && show.run.debug) console.info(`Show: bed ${message}`);
bed.js:235          played.catch((err) => console.warn("Show: the static bed could not play:", err));
bed.js:243          console.warn("Show: no clip of the static bed would load; the bed is off for this page");
sse.js:28              console.warn("Failed to parse SSE event:", json, e);
ambience.js:223      if (show.run && show.run.debug) console.info(`Show: ambience ${message}`);
ambience.js:258          played.catch((err) => console.warn("Show: the ambience could not play:", err));
ambience.js:268          console.warn("Show: no texture of the ambience would load; the textures are off for this run");
ambience.js:308              console.warn("Show: an ambience spot could not play:", err);
show.js:413              console.warn("Show: the transcription failed; counted as silence:", err);
show.js:470      console.error("Show:", message);
player.js:193              console.warn("Show voice: a chunk could not be said:", item.persona, item.text, err);
```

The debug-only messages go through `bedLog` (`bed.js:204`) and `ambLog` (`ambience.js:222`): the bed's "shuffled: a new
pass of N clips", "clip i of N: <file> (gain …)", "silence: N s"; the ambience's "shuffled: a new pass of N textures",
each texture, spot and cue ("<what>: <file>"), "silence: N s", and the A and F keys.

### The owner's ruling on the improvements

The owner (verbatim): "Improvements: Let's write down all the improvements in a follow up task. I am not going to
execute them before the demo day." From the owner's questions (Part 2), one more: **keep the Whisper request** in the debug files.
They are the follow-up "Debug and observability improvements", with a sixth item from the follow-up questions (Parts 4-5): confirm `usage` against
`timings` with one `curl`.
