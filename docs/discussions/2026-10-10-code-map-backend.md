# A map of the TalkWithZombies FastAPI territory — the backend

**Date:** 2026-10-10 · **Arc:** MVP prototype · **Branch:** `alfre2v/talk-prep`
**Type:** reference — the one-page map the agent drew to open the backend study session ([discussion 2026-10-10]
talk-preparation, workstream B), kept as the owner saw it.
**Status:** a **snapshot** of the fork at **`tz-0.9`** (`b1d039c`): the line numbers are true there and drift with
every change to the code. Its companion: [discussion 2026-10-10] code-map-client (session C). The seam between the
two — the four channels from the server to the browser, and the round's SSE events: [discussion 2026-10-12]
server-browser-channels.

Paths are in the fork, `/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`.

## The one idea to hold first

**The server keeps no show state between requests.** A show is a **run**, kept on disk in `runs/<run-id>/script.json`.
**The browser is the clock:** it asks for each round when it's ready. Each request reloads the run and the story from
disk, plans one round, streams it, appends it to the record, and forgets everything.

## The modules and the abstraction each holds

| Module | Holds | The key pieces |
|---|---|---|
| `app/show/story.py` | **the story**: what the show is about | `Story` (L92): the cast, the operator, the cast sheet's template, the events filed by overtone and theme, the tones, the agenda, the beats, the bed's and ambience's clips. `load_story` (L118) reads `stories/<name>/*.yaml` |
| `app/show/script.py` | **the record**: what has happened | `Run` (L90), `Round` (L55), `Line` (L35), `Heard` (L44); `new_run`, `load_run`, `append_round`; **`assemble_messages`** (L214): the shared screenplay the model reads; `trim` (L177) and `known_size` (L160), the context's budget |
| `app/show/director.py` | **the director**: what happens next | **`plan_round`** (L96) → a **`RoundPlan`** (L61): the round's kind, speakers, line budget, event, tone, instruction, grammar and fixed lines (`FixedLine`, L53). One function per kind: `_free`, `_orientation`, `_repair`, `_exchange`, `_last_exchange`, `_breakdown`, `_re_call`, `_switch_off` |
| `app/show/grammar.py` | **the format's guard** | `build_grammar` (L28): a grammar that lets the model write only `Name (mood): text` lines, for those speakers, within the budget |
| `app/show/parser.py` | **the stream into lines** | `LineParser` (L35): tokens in, `start` and `done` events out, one line at a time |
| `app/show/listen.py` | **the listener's words** | `usable` (L36): does a transcript count as words, or as silence? |
| `app/show/cues.py` | **sound cues** | `cue_for` (L33), `cue_dice` (L20), `says` (L25) |
| `app/show/bed.py` | **the sounds' manifests** | `bed_clips`, `bed_play_list`, `clip_path` |
| `app/show/debug.py` | **debug files** | `write_round` (L40), `write_chunk` (L67) |
| `app/services/llm.py` | **the model's door** | **`stream_round`** (L142): calls llama.cpp with the messages, the grammar and the seed, and streams the tokens; `server_context` (L196) |
| `app/routers/show.py` | **the routes** | below |

## The routes the page uses

- **`GET /show`** (`show_page`, L115): the chooser, a look, or the plain page.
- **`POST /api/show/start`** (L156): loads and checks the story, checks the model's context against the budget, picks
  the seed, opens the run (`new_run`). It returns everything the page needs: the cast, the voices per mood, the
  settings, the bed and the ambience.
- **`POST /api/show/round`** (L276 → `_round_stream`, L291): plays one round as a **stream of events (SSE)**.
- **`POST /api/show/listen`** (L258): the listener's recording through Whisper, with the show's settings.
- **`POST /api/tts`** (`app/routers/tts.py`, L103): one **chunk** of a line's voice. The page calls it, not the round.
- **`GET /api/show/bed/{name}`** and **`/api/show/ambience/{name}`** (L235, L226): the sound clips.

## The path of one round

1. **The page** sends `POST /api/show/round` with `{run_id, played_s, transcript?}`: how much audio has played, and
   what the listener said, if this follows a listening window.
2. **`_load`** reads the run and the story back from disk.
3. **`usable`** decides whether the transcript counts as words or as silence.
4. **`plan_round`** returns the **`RoundPlan`**, seeded by `"<seed>:<n>"`.
5. **`_cue`** checks the event against the clips' keywords.
6. **`trim`** runs if the script is near its budget.
7. **`assemble_messages`** builds the shared screenplay plus this round's instruction.
8. **The stream:** the `cue` first; then the **fixed lines**, through the parser; then **`stream_round`**, whose tokens
   go through the **`LineParser`** → `start`, `token` and `done` events per line.
9. **The record:** `append_round` writes the new `Round` to `script.json`, plus the debug files if debug is on.
10. **The summary:** a `round` event (kind, event, tone, whether the page should listen next…), then `complete`.

Meanwhile **the page** sends each `done` line to `POST /api/tts`, chunk by chunk, and plays the audio as it arrives.
That's why the voice starts before the model has finished the round.

## The session's outcome

The owner (verbatim, 2026-10-10): "I think this presentation you made allowed me to answered most of my questions. I
went through the code myself based on this map you presented and I feel I got myself the picture together."
