# The browser client — how a show runs: Web Audio, the loop, the voice queue

**Date:** 2026-10-10 · **Arc:** MVP prototype · **Branch:** `alfre2v/talk-prep`
**Type:** reference — three explanations from the client study session ([discussion 2026-10-10] talk-preparation,
workstream C), kept as the owner saw them: Web Audio explained on the app's own audio graph (Part 1); a walk through
the show's loop, `runShow` and `playRound` (Part 2); and the voice queue inside it, how `synthesizeNext` and `playNext`
overlap fetching and playing (Part 3). The session's map: [discussion 2026-10-10] code-map-client.
**Status:** a **snapshot** of the fork at **`tz-0.9`** (`b1d039c`): the line numbers are true there and drift with
every change to the code. Checked during the session: every function in `player.js` has the right doc comment above it
(a printout that cut through comment blocks had made them look shifted).

Receipts are in the fork's `static/show/` (`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies/static/show/`).

# Part 1: a Web Audio refresher

## The mental model

Web Audio is **a graph of nodes inside an `AudioContext`**: **sources** → **processing** → **the destination** (the
speakers). The sound itself is computed on a **separate real-time audio thread**. JavaScript only **builds and rewires
the graph** and **schedules changes** to it. That's why a fade can be perfectly smooth even while the page is busy.

## The `AudioContext`

- **One for the whole page:** `voice.ctx`, created in `unlockAudio` (`player.js:109`), and shared by the voice, the
  bed, the ambience and the gauge.
- **The autoplay policy:** a browser creates a context **suspended** until the user interacts with the page. That's why
  it's created and resumed on the **Start click** (`startShow`, `show.js:171`).
- **Its clock:** `ctx.currentTime`, in seconds, the time all scheduling is measured against. **`ctx.destination`** is
  the speakers.

## Sources: where sound comes from (four kinds here)

1. **`AudioBufferSourceNode`, a decoded clip held in memory.** The voice uses one per chunk:
   - `synthesize` (`player.js:225`) receives base64 WAV from `/api/tts`, turns it into bytes, then
     **`ctx.decodeAudioData`** into an `AudioBuffer`;
   - `playClip` (L265) creates a source, `connect`s it to the destination, calls `start()`, and waits for `onended`.

   **A buffer source plays once and can't be restarted,** so every chunk gets a new one. That's normal, and cheap.
2. **`MediaElementAudioSourceNode`, an `<audio>` element plugged into the graph.** The bed and the ambience use these:
   - the element **streams** its file (range requests, with no full download), and `play()`, `pause()` and `src` still
     control it;
   - once it's plugged in, its sound goes **only** through the graph, so gains and filters apply.

   One per element: `ambElement` (`ambience.js:122`).
3. **`MediaStreamAudioSourceNode`, the live microphone.** It's used only to feed the gauge's analyser (`tapMic`,
   `gauge.js:79`), never the speakers.
4. **Not Web Audio at all: `MediaRecorder`.** It records the mic's stream into a file (`webm`) for Whisper (`mic.js`).

## Processing nodes

- **`GainNode`, a multiplier, and the workhorse here.** At 1 the signal passes unchanged; at 0 it's silent; at 0.5 it's
  half the amplitude (≈ -6 dB, since dB = 20·log₁₀(gain)). Every level in the app is a gain:
  - each clip's measured gain from the manifest;
  - the level between rounds and under a line;
  - the silences' **gate**;
  - the **fading**;
  - the **M** and **A** mutes (`bed.sounds`, `amb.mute`).
- **`BiquadFilterNode`, the AM radio's band.** A **high-pass** at 300 Hz, then a **low-pass** at 3,000 Hz, together
  make a band-pass, a small speaker's range. `Q = √½` (`ambience.js:146`) is the "Butterworth" value: a flat band with
  no resonant peak at its edges.
- **`AnalyserNode`, a window for JavaScript.** It passes no sound on; it lets JS read the latest samples
  (`getFloatTimeDomainData`). The gauge computes an **RMS** level from them every frame (`rmsLevel`, `gauge.js:39`)
  for the looks.

## Connections

- **`a.connect(b)` / `a.disconnect()`.** Rewiring is cheap. The **F** key reroutes the layer through the filter or
  around it: `ambRoute` (`ambience.js:169`) does `layer.disconnect()`, then `layer.connect(highpass or fading)`.
- **Fan-in sums:** several nodes into one = a mix. The texture and the spot both feed `amb.layer`.
- **Fan-out copies:** one node into several. The gauge taps the voice by making every voice source *also* connect to
  its analyser. It wraps `createBufferSource` (`tapContext`, `gauge.js:60`), so `player.js` never knows.

## Channels: the mono mix

`layer.channelCount = 1`, `channelCountMode = "explicit"` and `channelInterpretation = "speakers"`
(`ambience.js:143-145`) make the layer **mix a stereo clip down to mono**, (left + right) / 2. A radio has one speaker.

## Scheduling a change: `AudioParam` automation

A gain's `gain` is an **`AudioParam`**. Setting `.value` directly jumps instantly, and an instant jump in level
**clicks**. So every level change here is **scheduled** on the audio thread (`ambRamp`, `ambience.js:113`; `bedRamp`
in `bed.js`):

```js
param.cancelScheduledValues(now);              // forget what was planned
param.setValueAtTime(param.value, now);        // start from where it is now
param.linearRampToValueAtTime(target, now + s) // glide to the target in s seconds
```

The audio thread then computes the ramp **sample by sample**: smooth, exact, independent of the page's busyness.

## Two clocks, two jobs

- **JavaScript timers** (`setTimeout`) decide **when to do something:** the next silence, the next spot, the 80 ms and
  250 ms pauses between the voice's chunks and lines.
- **The audio thread** decides **how it sounds:** ramps, mixing, filtering.

# Part 2: the loop (`runShow` and `playRound`)

## Starting: `startShow` (`show.js:170`)

1. `unlockAudio()`: the context, on the click.
2. `primeMic()`: asks for the microphone **now**, so the permission prompt never eats a listening window.
3. `POST /api/show/start` → **`show.run`** (the start reply: the cast, the voices, the settings, the bed, the ambience);
   `voice.run` (the run id, the seed, whether to send it, debug).
4. The counters are reset (`playedS`, `listens`…), then **`runShow()`**.

## The loop: `runShow` (`show.js:205`)

```js
const controller = new AbortController();      // Stop's handle on this loop
show.controller = controller;
while (true) {
    const heard = show.listens ? await listenerTurn(controller.signal) : null;
    const round = await playRound(controller.signal, heard);
    show.listens = Boolean(round.summary.listens);
    if (show.voice) await playOut(round, controller.signal);
    else await onAir(round, controller.signal);
}
```

- **The `AbortController`:** every wait in the loop gets its `signal` (the fetch, the sleeps, the listening window).
  **Stop** (`stopShow`, L449) calls `abort()`, so whatever the loop is waiting on fails at once, the `catch` runs, and
  the state becomes **stopped**. `stopVoice()` also cuts the clip that's playing.
- **`show.listens`** comes from **the server's summary** of the round just played. The server decides whether the radio
  listens next; the page just obeys. Because it's kept across iterations, a **Resume** after a stop during a listening
  window opens the window again.
- **`playOut`** waits for `drained()`, until the voice queue is empty. `onAir` is the `?voice=off` mode: it simulates
  the time the lines would take.
- **The guard in the `catch`:** `if (show.controller !== controller) return;`. A Resume starts a *new* loop with a new
  controller, and the old loop's late failure must not overwrite the new one's state.

## One round: `playRound` (`show.js:235`)

1. **`setState("thinking")`:** the buttons update, and through the wraps the bed and ambience rise to their
   between-rounds level.
2. **A round object** is created and kept in `show.current`: the timings, the lines, the page element, the cue.
3. **`fetch("/api/show/round", …, signal)`** with `roundBody`: the run id, **`played_s`**, and what the listener said.
4. **`readSSE`** calls back per event:
   - **`cue`** → `round.cue`, which `ambience.js` plays when the page goes on air;
   - **`start`** → the line's **mood**, kept for its `done`;
   - **`done`** → the line is complete:
     - `firstLineS` is measured, the line is added to the page **hidden**;
     - then **`speakLine(persona, text, hooks, voiceOf(mood), placeOf(message_id))`**: the mood picks the reference
       clip (`voiceOf`, from the story's voices), and the message id gives the debug tag (`r009-l2`);
     - the hooks: **`onStart` → `lineStarts`** (show the line, light the speaker, the RECEIVER sign, and **on air** at
       the first line); `onFail` → a note; `onVoice` → which clip was used;
   - **`round`** → the summary; **`error`** → thrown.
5. **After the stream:**
   - `settleUnsure`: a Stop can land after the server **kept** a round but before its summary arrived, so the notes of
     such rounds are corrected;
   - `settleHeard`: the listener's caption gets its verdict if the words counted as silence;
   - `addDirection`: the event or the stage direction goes above the round's lines;
   - the RECEIVER sign, and the debug line.
6. **It returns when the *stream* ends, not when the voice does.** The voice may still be talking, which is exactly why
   `runShow` then waits in `playOut`.

## `played_s`: why the server needs it

Each time a chunk plays to its end, `voice.onPlayed` → **`countPlayed`** (L463) adds the chunk's duration to
`show.playedS`. The page sends it with every round. **The director times the radio call (the Repair) by audio actually
played, not by the wall clock,** so a slow model or a slow voice never makes the call come early.

# Part 3: the voice queue — how fetching and playing overlap

Receipts are in the fork's `static/show/player.js`.

## The data: two queues and two flags (`voice`, L34)

- **`pending`:** chunks waiting to be **synthesized**.
- **`ready`:** chunks synthesized, waiting to be **played** (each with its decoded `buffer`, or `null` if synthesis
  failed).
- **`fetching`:** a `/api/tts` request is in flight. **At most one at a time.**
- **`playing`:** a clip is playing. **At most one at a time.**
- **`generation`:** a counter that Stop moves on, so stale results are dropped (below).

## Step 0: a line becomes chunks (`chunks`, L82)

Whole sentences are packed into chunks of **at most 100 characters**. A short sentence (under 30 characters) may
**ride along** up to 120, and a long sentence goes alone. Why chunks rather than whole lines:

- each chunk is **one request**, and a shorter first chunk means **the voice starts sooner**;
- whole sentences keep the voice's intonation natural.

## The two workers

They're not threads, just two functions that **restart themselves** and **wake each other**.

**The fetcher, `synthesizeNext` (L179):**

1. If a fetch is already in flight, or nothing is pending → return.
2. Take the next pending chunk, `POST /api/tts` (`voiceRequest` adds the reference clip, the seed if `voice_seed` is
   on, the debug tag if debug is on), and decode the WAV.
3. Push it to **`ready`**, then call **`playNext()`** (in case the player was waiting) and **`synthesizeNext()`**
   (itself, for the next chunk).

**The player, `playNext` (L242):**

1. If a clip is already playing → return.
2. If nothing is ready → if *everything* is done (`isIdle`), wake whoever waits in `drained()`. Return.
3. Take the next ready chunk. If it's a line's **first** chunk, call its `onStart` hook: **the line appears, the
   speaker lights, and "on air" is set.**
4. Play it (`playClip`) and wait for its end. Count its seconds (`onPlayed` → `played_s`).
5. Pause **250 ms** after a line's last chunk, **80 ms** between a line's chunks.
6. `playNext()` again.

**Who kicks whom:**

- `speakLine` (each `done` line) kicks **the fetcher**;
- each finished fetch kicks **the player** and **the fetcher**;
- each finished clip kicks **the player**.

## The overlap, on a timeline

Take line A in two chunks, then line B in one:

```
the stream:  A done ─────── B done ───────────────────────────────────
fetcher:     [fetch A1]─[fetch A2]──[fetch B1]────────────────────────
player:                 [play A1 ··········][80 ms][play A2 ·······][250 ms][play B1 ······]
                        ↑ on air: A appears
```

- **The fetcher runs ahead of the player.** It doesn't wait for playback; it fetches every pending chunk as fast as the
  voice server answers. While A1 plays, A2 and B1 are being made.
- **The only unhidden wait is the first one:** the model's first line, plus the synthesis of its first chunk. After
  that, if synthesis is **faster than real time**, each next chunk is ready before the current one ends, and the voice
  flows with only the 80 ms and 250 ms beats.
- **If a chunk takes longer to make than the previous one takes to play,** the player finds `ready` empty and waits:
  **an audible stall.**

## Why that last point matters for the owner's pauses

On **the 3090, the model and the voice share one GPU.** While a round's lines are being voiced, the model is often
**still writing the rest of the round**, so synthesis competes with generation for the same GPU. And each round the
model first reads a **longer script** (the context grows with the show), so that early-round competition gets heavier
as the show goes on. That would fit "pauses that grow as the show advances". It's **a second hypothesis** for session
D, next to the mic opening. The debug files can tell them apart:

- each chunk's `time_used` is the synthesis time;
- compare it with the previous chunk's length, and a stall shows up wherever synthesis took longer than playback.

## Stop, and failures

- **Stop** (`stopVoice`, L147) moves `generation` on, empties both queues, aborts the fetch in flight, and cuts the
  clip playing. A fetch that was already returning checks `generation` after its `await` and **drops its result.**
  That's how a stopped queue never speaks a stale chunk.
- **A chunk whose synthesis fails** goes to `ready` with no buffer. The player skips it but still runs the line's
  `onStart`, so the text appears even if a piece of the voice is missing.
