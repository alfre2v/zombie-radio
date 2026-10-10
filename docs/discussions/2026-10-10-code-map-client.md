# A map of the TalkWithZombies browser client — the show page

**Date:** 2026-10-10 · **Arc:** MVP prototype · **Branch:** `alfre2v/talk-prep`
**Type:** reference — the one-page map the agent drew to open the client study session ([discussion 2026-10-10]
talk-preparation, workstream C), kept as the owner saw it. The companion of [discussion 2026-10-10] code-map-backend.
**Status:** a **snapshot** of the fork at **`tz-0.9`** (`b1d039c`): the line numbers are true there and drift with
every change to the code.

Paths are in the fork, `/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies/static/show/`.

## The one idea to hold first

**The browser is the show's clock.** One loop, `runShow` (`show.js:205`), repeats three steps:

1. **the listener's turn,** if the last round listens;
2. **one round:** ask the server for it, and voice its lines as they stream in;
3. **wait until the voice has said everything,** then go again.

**The scripts are classic scripts sharing globals.** Each file owns one global object (`show`, `voice`, `mic`,
`gauge`, `bed`, `amb`). The add-ons work **by wrapping the page's functions from outside**:

- `gauge.js` wraps `unlockAudio`, `openMic` and `closeMic`;
- `bed.js`, then `ambience.js`, wrap `setState`.

So the page's own scripts (`show.js` and the rest) don't know the sounds exist.

## The scripts, in load order

| Script | Holds | The key pieces |
|---|---|---|
| `sse.js` | **reading the stream** | `readSSE` (L35), `splitSSE` (L17): a response body becomes events, whatever the chunk boundaries |
| `player.js` | **the voice** | `voice` (L34): the queue's state; `speakLine` (L125), `synthesizeNext` (L179), `playNext` (L242), `playClip` (L265); `chunks` (L82): a line cut into chunks of whole sentences; `unlockAudio` (L109) |
| `mic.js` | **push-to-talk** | `mic` (L16); `primeMic` (L28), `openMic` (L41), `closeMic` (L53); `startRecording`/`stopRecording`; `hear` (L137): the recording sent to Whisper |
| `show.js` | **the show** | `show` (L52): the run, the state, the current round; `startShow` (L170), **`runShow`** (L205), **`playRound`** (L235), `playOut` (L348), **`listenerTurn`** (L397); **`setState`** (L496); `debugLine` (L132); the page's elements (`addLine`, `addDirection`…) |
| `gauge.js` | **the level, for the looks** (designs only) | `gauge` (L25); `tapContext` (L60), `tapMic` (L79): analysers on the voice and the mic |
| `bed.js` | **the static** (designs, or the plain page with `&bed=on`) | `bed` (L43); `bedWire` (L125), `bedFollow` (L172); its rules `bedShuffle`, `bedLevel`, `bedBetween`, `bedFadingTarget` |
| `ambience.js` | **the world outside, and the cues** | `amb` (L50); `ambWire` (L132), `ambFollow` (L178), `ambCue` (L321), `ambRotation` (L97); it reuses `bed.js`'s rules |
| `designs/<look>/design.js` | **a look's drawing** | its own decorations, fed by the gauge |

## The page's states (`setState`, `show.js:496`)

**idle → thinking → on air → (listening → recording → hearing) → thinking → …,** and also **stopped** and **error**:

- **thinking:** a round has been asked for;
- **on air:** the round's first line has started playing;
- **listening:** the window is open, counting down;
- **recording:** the button is held;
- **hearing:** Whisper is transcribing.

`setState` sets the buttons and the ON AIR light. Through their wraps, **the bed and the ambience follow it:** higher
between rounds, lower under a line, silent while you hold to talk, paused on Stop.

## One cycle of the loop

1. **`listenerTurn`** (L397), only if the last round's summary said `listens`:
   - `openMic`;
   - `waitForPress`: a countdown of `listen_window_s`;
   - `recordUntilRelease`: a `MediaRecorder`, up to `press_cap_s`;
   - `hear`: `POST /api/show/listen`;
   - `closeMic`.
2. **`playRound`** (L235): state **thinking**, then `POST /api/show/round` (`roundBody`: the run id, `played_s`, what
   was heard). Then `readSSE` handles each event:
   - `cue` → kept on the round;
   - `start` → the line's mood;
   - `done` → the line added (hidden) and **`speakLine`**;
   - `round` → the summary.
3. **The voice queue** (`player.js`), working while the stream still arrives:
   - **`speakLine`** cuts the line into chunks (at most 100 characters of whole sentences) and queues them in
     `pending`;
   - **`synthesizeNext`** fetches them **one at a time** (`POST /api/tts`) into `ready`, the next fetched while the
     current one plays;
   - **`playNext`** plays each one as an `AudioBufferSourceNode`, with **80 ms** between a line's chunks and
     **250 ms** between lines.
   - When a line's first chunk starts, `lineStarts` shows the line, lights the speaker, and sets **on air**.
4. **`playOut`** (L348) waits for **`drained()`**: every line said. Then the loop starts again.

**No prefetch:** the next round is asked for only after this one has finished playing. So the "thinking" gap between
rounds is the model's time to its first line, plus the first chunk's synthesis.

## The audio graph

There's one **`AudioContext`** (`voice.ctx`). It's created on the **Start** click (`unlockAudio`), because browsers
refuse to play sound before a user gesture.

- **The voice:** each chunk is an `AudioBufferSourceNode` → the speakers. The gauge's analyser taps it, by wrapping
  `createBufferSource`.
- **The mic:** the `MediaStream` → a `MediaRecorder` (the file sent to Whisper), and → the gauge's analyser. **Never to
  the speakers.**
- **The bed:** an `<audio>` element → `MediaElementSource` → the clip's gain → the layer (mono) → (the AM filter:
  high-pass → low-pass) → the fading → the silences' gate → **`bed.sounds`** (the **M** mute) → the speakers.
- **The ambience:**
  - a texture's `<audio>` → its gain → the silences' gate → the layer;
  - a spot's `<audio>` → its gain × `spot_volume` → the layer;
  - then the layer (mono) → (the bed's AM filter) → the fading → **the A mute** → the speakers.

## The data structures worth knowing

- **`show`** (`show.js:52`): `run` (the start reply), `state`, `current` (the round in progress), `playedS`,
  `listens`, `controller` (Stop's abort).
- **The round object** (inside `playRound`): `summary`, `lines`, `element`, the timings (`firstLineS`,
  `firstSoundS`), `cue`.
- **`voice`** (`player.js:34`): `ctx`, `pending`, `ready`, `fetching`, `playing`, `generation` (Stop moves it on, so
  late results from a stopped queue are dropped).
- **`mic`**, **`gauge`**, **`bed`**, **`amb`:** each the state of its own part.

## A finding for session D

`openMic` asks for the microphone (`getUserMedia`) **at every listening window**, and `closeMic` releases it after each
(`mic.js:41-65`). Starting the device takes a moment, and **with a Bluetooth headset, opening the mic switches it into
call mode,** which briefly interrupts the sound. It's a candidate cause for the pauses the owner heard when the mic
turns on or off, alongside OBS.
