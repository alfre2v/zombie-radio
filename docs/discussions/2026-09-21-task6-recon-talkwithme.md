# Task 6 reconnaissance — the TalkWithMe tour (unit 1)

**Date:** 2026-09-21 (opened; living until Task 6 starts) ·
**Arc:** MVP prototype · **Branch:** `alfre2v/task6-recon-brief`
**Type:** guided code tour, unit 1 of the Task 6 reconnaissance
brief (umbrella: `docs/discussions/2026-09-21-task6-reconnaissance-brief.md`).
**Status:** breadth pass COMPLETE — sections 1–7 written (sections
2–6 at question-gathering depth per the owner's 2026-09-21
breadth-first ruling). Open questions Q1–Q3 (§1.7) and Q8–Q13 (§8)
are marked OPEN; the answer pass comes later.

*Context for the cold reader.* TalkWithMe is scorbo2's local
multi-persona chat application: a FastAPI server with a plain
JavaScript web UI, in which several AI "personas" (each with its
own system prompt and its own cloned voice) answer the user in a
shared chat room. We use it unmodified, at tag **7.1** (commit
`93df6ca`), as the front end and director of the Zombie-Radio
prototype: it runs on the Mac laptop, talks through an SSH tunnel
to three model services on a rented GPU box — llama.cpp on
port 8080 (the LLM), tts-serve on port 8001 (text-to-speech by
voice cloning), whisper-fastapi on port 8002 (speech-to-text) —
and drives a cast of four placeholder personas (Daniel, Moira,
Ralph, Samantha) whose reference voices were generated with the
Mac's `say` command. Task 6 will fork it to (a) remove the speaker
label the personas have started emitting and (b) replace the
per-sentence speech split with a pack-up-to-N-characters
accumulator. This tour reads the 7.1 code to find where those
patches go and what else the fork should know.

*All paths below are absolute paths into the owner's working
clone, `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/`, which
is byte-identical to the pristine installer clone
`/Users/alfredo/TalkWithMe-client/` (both at `93df6ca`). Labels:
measured = inspected in the code or run; docs-say = upstream's
own documentation; believed = inference.*

---

## 1. The pipeline map — microphone to speaker

### 1.1 A turn in one paragraph

The audience member presses the microphone button and speaks; the
browser records, sends the audio to the TalkWithMe server, which
forwards it to the Whisper service and puts the transcript into
the input box and sends it as a chat message. The server picks a
first persona (by asking the LLM, at random, or as named by the
user), then loops: for each of up to `max_persona_replies`
personas, it builds a prompt from that persona's system prompt and
the room history, streams the LLM's tokens to the browser, and
stores the finished reply in the room's history file. The browser
shows the tokens as they arrive and, in streaming-TTS mode, cuts
complete sentences out of the running text and sends each to the
server's TTS endpoint, which attaches the persona's reference clip
and transcript and calls tts-serve; the returned audio is queued
and played in order. All of this happens inside one HTTP request
per user message, using server-sent events (SSE).

### 1.2 The eight hops

1. **Microphone to text, in the browser.** The mic button toggles
   a `MediaRecorder`
   (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/stt.js:9`);
   the keyboard shortcut Ctrl+Space does the same
   (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/app.js:134`).
   When recording stops, the browser base64-encodes the blob and
   posts it to the app's own `/api/stt` endpoint (`stt.js:61`).
   The transcript that comes back is appended to the input box
   (`stt.js:78`), the recording is uploaded for persistence under
   a message UUID generated on the spot (`stt.js:85`–`90`), and
   the message is **sent automatically** (`stt.js:98`). So the
   microphone is push-to-talk with no end-of-utterance detection
   and no confirmation step: what Whisper heard is what gets sent.
   *Measured.*

2. **The STT proxy.** The server decodes the audio and forwards it
   as a multipart upload to the OpenAI-compatible transcription
   endpoint `/v1/audio/transcriptions` on the STT server
   (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/services/stt_client.py:63`),
   with the timeout from settings (30 s in our seeded
   configuration). It returns text, language, and an optional
   language probability. Nothing else happens on this hop.
   *Measured.*

3. **Sending a message.** `sendMessage`
   (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/chat.js:65`)
   posts `{message, who_answers, chat_room, message_id}` to
   `/api/chat` (`chat.js:119`–`128`) and then reads the response
   body as a hand-parsed stream of `data: {json}` lines
   (`chat.js:135`–`159`), dispatching each to `handleSSEEvent`.
   Two things happen before the post:
   - *Mention detection* (`chat.js:80`–`91`): if the text contains
     a persona's name as a whole word, the "selected persona"
     radio is switched to that persona, so `who_answers` becomes
     that name. Controlled by the setting
     `general.persona_name_mentions` (true in our seed).
   - *The who-answers radio* (`chat.js:53`–`59`): `router`,
     `random`, or `selected` (the sidebar persona, falling back
     to `router` if none is selected).
   Sending is blocked while a turn is streaming (`chat.js:67`,
   `109`): the audience cannot interrupt mid-turn. *Measured.*

4. **The reply loop, server side.** The endpoint is `POST /api/chat`
   (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/routers/chat.py:344`),
   which returns a `StreamingResponse` driven by the generator
   `_chat_stream` (`chat.py:208`). In order:
   - switch the session to the requested room (`chat.py:211`);
   - resolve the personas eligible in that room from the chat-room
     config — the "default" room means all personas
     (`chat.py:215`, function `_resolve_room_personas` at
     `chat.py:32`–`55`);
   - `max_replies = min(settings.general.max_persona_replies,
     number of eligible personas)` (`chat.py:223`) — 4 in our
     seed;
   - pick the **first** speaker with `_pick_persona`
     (`chat.py:226`, function at `chat.py:98`–`133`): for
     `router`, it builds a small prompt listing the eligible
     personas with their "router hints" and the recent history
     (`_build_router_prompt`, `chat.py:62`–`95`) and asks the LLM
     for a name with a non-streaming call of at most 16 tokens at
     temperature 0.1 and a 15 s timeout
     (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/services/llm.py:121`–`145`);
     any failure or an unknown name falls back to `random.choice`
     (`chat.py:122`–`125`);
   - persist the user message (`chat.py:232`);
   - check the room's echo-chamber flag (`chat.py:234`–`250`);
   - **loop over replies** (`chat.py:254`): reply 0 is the first
     speaker; every **follower** is `random.choice` of the eligible
     personas that have not yet replied (`chat.py:258`–`261`). Per
     reply: mint the assistant message UUID *before* anything is
     sent (`chat.py:284`), emit the SSE `start` event carrying
     persona name and both message IDs (`chat.py:289`), build the
     LLM messages (`chat.py:297`–`302`, see hop 5), stream tokens
     — appending each to `full_text` and emitting it as a `token`
     event in the same instant (`chat.py:328`–`330`; the tool-
     calling variant at `chat.py:305`–`321` does the same) —
     then persist the finished reply (`chat.py:337`) and emit
     `done` with the full text (`chat.py:339`). After the last
     reply, emit `complete` (`chat.py:341`).
   *Measured.*

5. **Context assembly.** `SessionManager.build_llm_messages`
   (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/session.py:123`–`163`)
   builds the messages list for one persona's request:
   - a `system` message = the persona's system prompt, then the
     persona's saved memories if enabled, then the global system
     prompt (assembled at `chat.py:298`–`299` by
     `_system_prompt_with_memories`, `chat.py:140`–`180`, and
     `_with_global_system_prompt`, `chat.py:183`–`201`);
   - the last N history **entries** (`session.py:144`; N is
     `general.max_turns_for_context`, 50 in our seed), each
     rewritten for the responding persona: the human's lines keep
     role `user`; the persona's own earlier lines keep role
     `assistant`; **every other persona's line becomes a `user`
     message whose text is `[Name]: what they said`**
     (`session.py:156`–`161`). The code comment explains why: it
     avoids consecutive `assistant` messages (which many servers
     reject) and stops the model treating another persona's words
     as its own.
   The request payload for a persona reply carries only `model`,
   `messages`, `max_tokens`, `temperature`, and `stream: true`
   (`llm.py:69`–`78`); everything else is the LLM server's default.
   *Measured.*

6. **The SSE consumer and the speech split.** `handleSSEEvent`
   (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/chat.js:175`–`289`):
   - on `start`: create or reuse the chat bubble, adopt the
     server-issued message ID (`chat.js:199`), and in streaming-TTS
     mode reset the sentence buffer (`chat.js:217`–`220`);
   - on `token`: append the token to the bubble (`chat.js:226`)
     and, if TTS is enabled and in streaming mode, hand it to
     `accumulateForTTS` (`chat.js:231`–`235`);
   - on `done`: flush whatever is left in the sentence buffer as
     one last synthesis request (`chat.js:249`–`256`), or in
     non-streaming mode enqueue the whole text at once
     (`chat.js:259`).
   In `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/tts.js`:
   `accumulateForTTS` (`tts.js:88`–`95`) appends the token to a
   buffer and calls `extractSentences` (`tts.js:72`–`83`), which
   applies the regular expression `/[^.!?]*[.!?]+/g` — "anything up
   to and including a run of `.`, `!` or `?`" — and enqueues each
   match immediately as one synthesis request. Two queues then run
   concurrently: `processTTSRequests` (`tts.js:111`–`129`) fetches
   **one request at a time, in order**; `processAudioBufferQueue`
   (`tts.js:136`–`150`) plays decoded buffers in order with an
   80 ms gap. Fetching sentence N+1 while sentence N plays is what
   gave the prototype its "almost natural" pauses. The non-
   streaming path (`enqueueTTS`, `tts.js:38`–`62`) fetches and
   plays serially with a 100 ms gap. *Measured.*

7. **The TTS proxy.** `POST /api/tts`
   (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/routers/tts.py:100`–`150`)
   receives `{text, persona_name}`. It looks the persona up
   (`tts.py:107`–`110`); a persona is "TTS-capable" only if it has
   both a reference clip and a transcript
   (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/config.py:287`–`289`);
   it refuses if the cached capabilities document says the engine
   cannot clone voices (`tts.py:122`–`131`); it **re-reads and
   base64-encodes `ref.wav` on every call** (`tts.py:134`, the
   function `encode_reference_audio` at
   `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/services/tts_client.py:615`–`626`)
   and reads `ref.txt` (`tts.py:135`); then calls `synthesize`
   (`tts_client.py:531`–`612`), which builds the JSON body from the
   engine's capabilities document — `text`, then `audio_base64`,
   `reference_text`, `language` if the engine advertises them,
   then every configured `tts.parameters` entry the engine
   advertises (`build_synthesis_payload`, `tts_client.py:452`–`510`)
   — posts it to `{tts.base_url}/synthesize` with the settings
   timeout (60 s in our seed), and on a 422 invalidates the
   capabilities cache, refetches, rebuilds, and retries exactly
   once (`tts_client.py:588`–`605`). The raw JSON reply is passed
   back; the browser reads only its `audio_base64` field
   (`tts.js:178`). *Measured.*

8. **The persistence side channel.** Each audio buffer the browser
   receives is uploaded for storage without waiting for the result
   (`tts.js:181`–`189`, via `uploadAudio` in
   `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/persistence.js:64`–`85`,
   endpoint `POST /api/persist/audio`). On the server
   (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/persistence.py`),
   audio that arrives before its message row exists — the normal
   case in streaming mode, where sentences are synthesized while
   the reply is still being generated — is written under a
   `<id>_pending_<random>` filename and attached to the row when
   `persist_message` creates it (`persistence.py:41`–`53`, `202`).
   Rooms live under `chatrooms/<room>/history.json` plus the audio
   files. Personas live under `Personas/<Name>/` as `prompt.md`
   (YAML front matter with name, description, router hints, avatar
   color, tool flag, memory budget, followed by the system prompt
   body), `ref.wav`, `ref.txt`, optional `memories.txt` and an
   avatar image
   (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/services/persona_store.py:9`–`15`
   and `49`–`53`). *Measured.*

### 1.3 The turn as a sequence diagram

```mermaid
sequenceDiagram
    autonumber
    participant B as Browser (stt.js, chat.js, tts.js)
    participant S as TalkWithMe server (FastAPI)
    participant W as whisper-fastapi :8002
    participant L as llama.cpp :8080
    participant T as tts-serve :8001

    B->>S: POST /api/stt (audio base64)
    S->>W: POST /v1/audio/transcriptions (multipart)
    W-->>S: text
    S-->>B: text (auto-sent as the message)
    B->>S: POST /api/chat {message, who_answers, room, message_id}
    S->>L: router call (16 tokens, temp 0.1) when who_answers = router
    L-->>S: first persona name (or random fallback)
    loop up to max_persona_replies (followers chosen at random)
        S-->>B: SSE start {persona, message_id}
        S->>L: POST /v1/chat/completions (stream, persona prompt + history with [Name]: lines)
        L-->>S: tokens
        S-->>B: SSE token (one per LLM token)
        B->>S: POST /api/tts {sentence, persona} as soon as a sentence completes
        S->>T: POST /synthesize {text, audio_base64 = ref.wav, reference_text, language}
        T-->>S: audio_base64
        S-->>B: audio (queued, played in order)
        B->>S: POST /api/persist/audio (fire and forget)
        S-->>B: SSE done {full text} after persisting the reply
    end
    S-->>B: SSE complete
```

### 1.4 Findings

#### F1 — Why personas speak their own name tag, and where a fix has to sit

*What we observe.* In the live show, a persona's reply starts with
`[Moira]:` and the TTS engine reads that tag aloud. Sometimes a
persona wears another persona's tag (the "cross-persona label
wearing" specimens on the watch list: Ralph under `[Daniel]:`, a
doubled `[Moira]:`).

*Why it happens.* TalkWithMe sends one LLM request per persona
reply. For Moira to know what Ralph and Daniel said, their lines
must appear in Moira's request. `build_llm_messages`
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/session.py:146`–`161`)
does this by rewriting history for the responding persona: the
human's lines keep role `user`; Moira's own earlier lines keep role
`assistant`; every other persona's line becomes a `user` message
whose text is `[Ralph]: what Ralph said` (`session.py:159`). So the
model sees a transcript in which almost every incoming line looks
like `[Name]: text`. A small model imitates the format it is shown
and opens its own answer with `[Moira]:`. That is the leak. It is
not a prompt bug and the Global System Prompt cannot fully
suppress it, because the pattern is present in every request by
construction. It also explains the cross-persona wearing: the model
copies a format, and sometimes copies the wrong name with it.
*Measured (the mechanism); believed (that imitation is the cause —
consistent with every specimen so far).*

*Consequence one.* The fix cannot be "remove the labels from the
context". Those labels are the only thing telling the model who
said what. The fix must remove the label from the persona's **own
output**, and leave the context labels alone.

*Where the output flows, and why placement matters.* In
`_chat_stream`
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/routers/chat.py:328`–`330`),
tokens arrive from the LLM one at a time; each is appended to
`full_text` and, in the same instant, sent to the browser as an
SSE `token` event. Only when the stream ends does the server
persist `full_text` (`chat.py:337`) and send `done` with the whole
text (`chat.py:339`). In the browser (`chat.js:223`–`237`), each
`token` event goes into the chat bubble and — because our settings
have streaming TTS on — into `accumulateForTTS`
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/tts.js:88`–`95`),
which cuts complete sentences out of the running token text and
sends each to `/api/tts` immediately, while the LLM is still
generating. So the first sentence, `[Moira]: We need to check the
generator.`, has been synthesized and is probably already playing
before the `done` event exists.

*Consequence two.* A sanitizer that strips the label at
`chat.py:337`, just before persisting, would clean the stored
transcript and therefore the context of every later reply — the
taxonomy C3 win we wanted. But the label would **still be spoken**,
because speech is cut from the token stream, not from the stored
text. To clean speech as well, the server has to filter tokens
*before* yielding them as SSE events. The label arrives split
across several tokens (something like `[`, `Mo`, `ira`, `]:`,
` We`), so the filter cannot judge one token at a time: it must
hold back the first few tokens of each reply until it can decide
whether they form a label, drop the label if so, then pass
everything else through unchanged. That is a **stream-head
filter**: a small state machine that runs only at the head of each
reply.

*Options (decision OPEN, see §1.7 Q1):*

1. **Server stream-head filter inside `_chat_stream`**
   (recommended). One place; cleans both the spoken stream and the
   stored transcript. Cost: it touches the SSE loop, and the first
   token reaches the browser a few tokens later than today.
2. **Server strip at persist time only.** Trivial; cleans the
   transcript; does nothing for speech. Not sufficient alone.
3. **Browser-side strip in `tts.js` before enqueue, plus option 2
   for the transcript.** Two patches in two languages for one
   defect; worse for upstreaming.

#### F2 — What happens when a reply hits the 200-token cap

*What is configured.* Our seeded `settings.yaml` sets
`llm.max_tokens: 200`. That number is copied into every persona
request
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/services/llm.py:75`).

*What happens at the cap.* When the model has not finished after
200 tokens, llama-server stops it wherever it is — often mid-
sentence — and marks the stream with finish reason `length`.
TalkWithMe does not look at that marker on the plain streaming
path: `stream_chat` (`llm.py:107`–`118`) reads only the token
text. The application therefore never knows a reply was cut.
*Measured.*

*Three consequences, one per hop:*

- **Stored transcript:** the truncated text is persisted as if
  complete (`chat.py:337`) and re-enters every later persona's
  context as `[Name]: …half a sent`. Fragments in context teach
  the model that fragments are acceptable output — a mild form of
  taxonomy C3 contamination.
- **Speech:** the tail of a reply with no terminal punctuation
  never matches the sentence regex, so it waits in the sentence
  buffer until `done`, where it is flushed to TTS as-is
  (`chat.js:249`–`256`). The audience hears a sentence that stops
  in mid-air.
- **Display:** the bubble shows the cut text with no marker.

*Why it matters.* Not a bug in TalkWithMe — it is the intended
contract. For a radio play it is a lever we control and should
decide on: `max_tokens` is effectively the line-length knob a
director would use for pacing, and a cut mid-sentence can sound
like a radio dropout — possibly even in-fiction — but it should be
a choice, not an accident. It is also a Task 5a consideration: the
models under audition differ in verbosity, so a fixed 200 will
truncate some and not others, and the truncation itself would
change the narrative-health scores.

#### F3 — The "1." echo artifact is the sentence splitter, confirmed

The regex `/[^.!?]*[.!?]+/g` (`tts.js:74`) treats any run of
`.`, `!`, `?` as a sentence end. A numbered list therefore yields
`1.` as a complete "sentence", and `Dr.` does the same. Each such
fragment becomes its own synthesis request. **Two symptoms, one
cause (owner correction 2026-09-22):** the ECHO artifact happened
only when "1." was synthesized as a lone sentence; what "Dr.",
"2.", "3." produced was LONG UNNATURAL PAUSES — each fragment pays
a full request round trip plus the 80 ms inter-buffer gap. The
accumulator's motivation is now a receipt, not a suspicion.
*Measured (the splitter); owner-observed (the two symptoms).*

#### F4 — The vanished sentence has a silent failure path

`fetchTTS` returns `null` on any non-OK HTTP status or when the
reply lacks `audio_base64` (`tts.js:172`–`178`), and the fetch loop
skips a `null` without retry and without any UI signal
(`tts.js:118`); the only trace is a `console.warn`. On the server
side, a synthesis timeout (60 s) or any exception makes
`synthesize` return `None` (`tts_client.py:606`–`612`) and the
router answers 502 (`tts.py:147`–`148`). When the item recurs, the
browser devtools console will show `TTS request failed: 502` (or
another status) and the Network tab the failing `/api/tts` call.
The 09-19 observation that the tts-serve log showed only 200s is
consistent with this only if the failure was on the client side or
the request to tts-serve never went out — which is where to look.
*Measured (the paths); believed (which one fired on 09-19).*

#### F5 — Every sentence ships the reference clip

Every `/api/tts` call re-reads `ref.wav` from disk, base64-encodes
it, and puts it in the request body (`tts.py:134`;
`tts_client.py:482`–`483`). In streaming mode that is one copy per
sentence. Measured on the four placeholder voices in
`/Users/alfredo/TalkWithMe-client/Personas/`:

| Persona | ref.wav size | duration | format |
|---|---|---|---|
| Daniel | 277,318 B | 5.7 s | 24 kHz, 16-bit mono |
| Moira | 246,042 B | 5.0 s | 24 kHz, 16-bit mono |
| Ralph | 246,580 B | 5.1 s | 24 kHz, 16-bit mono |
| Samantha | 290,450 B | 6.0 s | 24 kHz, 16-bit mono |

Base64 adds one third, so roughly 330–390 KB per sentence travels
over the SSH tunnel to the GPU box; real actor clips may be
longer. Whether tts-serve can cache references or address a voice
by identifier is seam question **S1** in the umbrella document.
*Measured.*

#### F6 — The context window counts entries, not user turns

N is a slice of the last N history messages (`session.py:144`),
and a history message is one persona reply or one user line. With
4 replies per user message, our N = 50 is about 10 user turns. The
router prompt uses the same slice (`chat.py:75`–`76`). Relevant to
Task 5a's "name-memory retest at the raised window": the window is
smaller in turns than the number suggests. *Measured.*

#### F7 — The 2026-09-18 audit anchors hold at 7.1

The four anchors from the earlier, unpinned source audit were
re-verified: the persona payload sends only `max_tokens` and
`temperature` besides model/messages/stream (`llm.py:69`–`78`);
the router call `chat_completion` runs at temperature 0.1 with
16 tokens (`llm.py:121`–`145`, called from `chat.py:117`);
`_pick_persona` routes only the first speaker (`chat.py:98`–`133`,
called at `chat.py:226`); followers are `random.choice`
(`chat.py:261`). *Measured.*

#### F8 — One user, one room, one turn at a time

The session is a process-wide singleton (`session.py:170`–`171`);
one room is current at a time; the SSE response keeps the HTTP
request open for all replies of a turn; and the browser refuses to
send while a turn streams (`chat.js:67`). For a radio show this
means the audience cannot interject during a multi-persona turn,
and a director loop will have to either live with that or change
the turn model. Noted for section 5. *Measured.*

### 1.5 Upstream vocabulary met in this section

Persona · chat room · echo chamber · who answers (modes `router`,
`random`, `selected`) · max persona replies · history entry ·
streaming TTS · capabilities document · message ID · staged
(pre-row) audio. Definitions in the umbrella document's glossary.

### 1.6 Reading itinerary for the owner (one sitting)

1. `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/chat.js:65`
   — `sendMessage`: what the browser owns before the server sees
   anything (mention detection, who-answers, the message UUID).
2. `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/routers/chat.py:208`
   — `_chat_stream`: the whole reply loop, top to bottom.
3. `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/session.py:123`
   — `build_llm_messages`: where the labels are born.
4. `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/chat.js:175`
   — `handleSSEEvent`: where speech is cut from live tokens.
5. `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/tts.js:72`
   to `150` — the splitter and the two queues.
6. `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/routers/tts.py:100`
   and `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/services/tts_client.py:531`
   — the synthesize contract as the client sees it.

Question to hold while reading: where would you cut so that both
the spoken stream and the stored transcript come out clean, with
one patch?

### 1.7 Open questions from section 1

- **Q1 — OPEN. Does the sanitizer become a stream-head filter?**
  It is a bigger patch than a regex at persist time and it touches
  the SSE loop (see F1, options 1–3). Agent's recommendation:
  option 1.
- **Q2 — OPEN. Which labels should it strip?** Only the persona's
  own name (`[Moira]:` when Moira speaks); any bracketed `[X]:`
  prefix (the cross-persona wearing specimens argue for this); or
  also a bare `Name:` without brackets, the 2024 wire format.
- **Q3 — OPEN, parked for section 5. Mention detection.** The
  browser overrides who-answers when the user names a persona
  (`chat.js:80`–`91`). In a radio show, should the audience saying
  "Moira" force Moira to answer? A director may want that power
  for itself.

---

## 2. The server-side reply path and the sanitizer insertion point

*Breadth-pass depth (2026-09-21): findings and questions, no
decisions. Section 1 walked the reply path hop by hop; this
section adds the exact geometry the sanitizer question needs.
Paths are absolute under
`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/`.*

- **There are two token sources, not one.** The plain path streams
  from `stream_chat`
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/routers/chat.py:328`
  to 330). The tool-calling path streams token events from
  `stream_chat_with_tools` (`chat.py:316` to 319; the tokens are
  produced in
  `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/services/llm.py:274`).
  Our personas have tool calls off, but a patch that filters only
  the plain path leaves a hole upstream would notice. The clean
  single point is a small async-generator wrapper applied to
  whichever token source is in use, right where the loop reads it,
  so both paths pass through the same filter. *Measured.*
- **The echo chamber bypasses the LLM** (`chat.py:291` to 294) and
  echoes the user's text as one token. The filter must not run
  there, or a user typing "[Moira]: hello" would be altered.
  Trivial to skip; worth stating.
- **The stored shape.** In memory, a reply is a `ChatMessage` with
  role, content, persona, and id
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/models.py:287`
  to 298). On disk it is a row with id, sender, text, audio
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/persistence.py:198`
  to 203). On room load the stored text is pushed straight back
  into history
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/session.py:47`
  to 64). *Consequence:* a sanitizer cleans NEW replies only. Every
  existing `history.json` keeps its labels and feeds them back into
  context whenever that room is loaded. Our fresh-rooms practice
  already covers this, but it means "clean transcript" is true
  from the fork forward, not retroactively.
- **What the head of a reply can look like.** From the watch-list
  specimens: `[Moira]:`, a doubled `[Moira]: [Moira]:`, the wrong
  name `[Daniel]:` under Ralph. From the 2024 wire format, a bare
  `Moira:` is plausible. The filter has to hold tokens until it has
  seen either a complete label pattern or enough non-label text to
  give up — a few tokens of delay, invisible in practice. This is
  what open question Q2 asks: which of these shapes to strip.
- **A shape the head filter cannot catch.** If the model switches
  speaker mid-reply — "[Moira]: I agree. [Ralph]: No." — the label
  appears mid-text. Only a full-text pass at persist time
  (`chat.py:337`) catches that, and it would come after the
  sentence was already spoken. → **Q8** (§1.7 / §8 of this
  document): head filter only, or head filter plus a persist-time
  sweep.
- **Testability upstream is good.** The SSE endpoint has a dedicated
  suite,
  `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/tests/test_chat_sse.py`,
  with one test class per behavior: request validation, single
  reply, persona selection, multi-persona replies, echo chamber,
  tool calls, persona memory, global system prompt, stream errors.
  The LLM is stubbed at the router's import site (upstream's rule,
  `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/AGENTS.md:35`),
  so a test can feed the token sequence `[`, `Mo`, `ira`, `]:`,
  ` We` and assert what reaches the SSE stream and what gets
  persisted. A sanitizer patch gets its own test class in the
  existing pattern. *Measured.*

## 3. The anatomy of `static/tts.js`, and where N enters

*Breadth-pass depth (2026-09-21). The file is 221 lines and has
exactly one cut point.*

- **`accumulateForTTS` is the only place text is cut**
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/tts.js:88`
  to 95). It appends the token to a buffer, calls
  `extractSentences` (lines 72 to 83, the regex
  `/[^.!?]*[.!?]+/g`), and enqueues each complete sentence. The
  accumulator replaces exactly this: keep appending complete
  sentences into a chunk until adding the next one would exceed N
  characters, then enqueue the chunk. Nothing downstream changes —
  the two queues (`processTTSRequests`, lines 111–129;
  `processAudioBufferQueue`, lines 136–150) and playback stay as
  they are.
- **The flush on `done` is the second touch point**
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/chat.js:249`
  to 256). Today it flushes the partial sentence left in the
  buffer. With an accumulator there is also a packed chunk
  waiting, so the flush must send both — chunk first, then the
  remainder — in order.
- **N makes the abbreviation problem mostly disappear, but not the
  lone fragment.** With N around 100 characters or more, "Dr." gets
  packed with the sentence that follows it, so it is never
  synthesized alone. Two cases remain: a fragment at the very end
  of a reply, and a reply that consists of only "1." or "Over.".
  → **Q9**: the policy for tiny remnants — send as is, hold them
  for a minimum length, or drop below a threshold.
- **Both extremes of N already exist as configuration.** Streaming
  mode is N = one sentence. Streaming OFF (`enqueueTTS`,
  `tts.js:38` to 44, reached from `chat.js:259`) sends the whole
  reply as one request, which is N = infinity. The patch adds the
  middle. *Consequence for Q4, the latency measurement:* the
  N-infinity end can be measured tonight on any box by flipping
  `tts.streaming` to false in the Servers dialog — no code needed.
- **RULED 2026-09-22 (answer pass, Q9 / Q4) — the accumulator's
  rules for the fork.** The accumulator is CONFIRMED as needed: under
  the adopted engine the server still emits `token` events per
  script line and `tts.js` still cuts sentences from them, so a
  line like "Dr. Byrne. 47. Microbiology. Over." would still be
  five requests without it. N is a PACKING limit, never a
  truncation: the regex hands whole sentences, the accumulator only
  groups them. Provisional **N = 100 characters** (owner: 150 too
  big), **tail tolerance ~20 %** (to 120), **tail threshold
  ~30 characters**. Rules: (1) a sentence arrives and the chunk is
  empty → it goes in whatever its length; a single 180-character
  sentence is sent whole, alone, oversize — splitting mid-sentence
  would sound worse than one longer wait; (2) a sentence arrives
  and the chunk has content → append if chunk + sentence ≤ N;
  else, if the sentence is under the tail threshold and the total
  ≤ N × 1.2, append anyway (built for "Over."); else FLUSH the
  chunk and start a new one with the sentence; (3) the LINE END is
  a hard flush — the next line is another speaker, another voice,
  so a chunk never crosses it. "Flush" = one call to the existing
  `enqueueStreamingTTS(persona, chunk)`, which pushes the string
  onto the existing `ttsRequestQueue` array and returns
  immediately; the fetch and playback pipelines already run
  concurrently, so the accumulator's own state is two strings (the
  partial-sentence buffer that exists today, plus the current
  chunk) — no new queue. Lone one-word lines ("Over.") go as is;
  whether a lone digit still echoes on the chosen engine is an
  audition item, not a browser rule. If the model writes
  200-character sentences, the fix is a director instruction about
  line length, not a splitter. The measurement that would tune N
  (synthesis time versus text length) is deferred to follow-ups.
- **How the browser learns TTS settings today is the pattern for
  N.** The `streaming` flag travels: `settings.yaml` → `TTSConfig`
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/config.py:75`)
  → the health response
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/routers/tts.py:41`;
  model `TTSHealthResponse` at
  `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/models.py:157`
  to 160) → the browser at startup
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/app.js:80`)
  → the `start` handler (`chat.js:217`). N would ride the same
  road. *Measured.*
- **Where the vanished sentence is observable** — finding F4 in
  §1.4: `fetchTTS` returns `null` on non-OK or missing
  `audio_base64` (`tts.js:172` to 178) and the fetch loop skips it
  silently (`tts.js:118`); devtools console and the Network tab's
  `/api/tts` entry are the places to look when it recurs.

## 4. Settings plumbing — the journey of one knob

*Breadth-pass depth (2026-09-21). Tracing `max_turns_for_context`
and `streaming` end to end gives the recipe. A knob touches seven
files, and two of the steps are manual mappings that upstream's own
notes warn about.*

1. **The config model.**
   `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/config.py`:
   `GeneralConfig` (lines 167 to 189) for chat behavior,
   `TTSConfig` (71 to 146) for speech. A missing YAML key takes the
   model default, so old files keep working. `save_settings` (474
   to 487) dumps every section with `exclude_none=False`, so a new
   key is written to `settings.yaml` on the first save after the
   upgrade. `personas_directory` (line 189) shows a yaml-only knob
   with no UI at all.
2. **The API models.**
   `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/models.py`:
   `GeneralSettingsRequest` (213 to 231) is a PARTIAL update —
   every field optional, omitted means keep. `TTSSettingsRequest`
   (188 to 203) is a FULL replacement. Each has a response twin
   (241 to 280).
3. **The router.**
   `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/routers/settings.py`:
   `_to_response` (24 to 53) maps every field BY HAND, so a new
   field that is not added there never reaches the browser.
   `update_settings` (86 to 155): the general section merges
   automatically via `model_dump(exclude_none=True)` (116 to 118)
   — upstream added this precisely because a hand-rebuilt section
   once reset `show_tool_calls` on every save
   (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/AGENTS.md:90`);
   the tts section is rebuilt field by field (127 to 133), so a new
   tts field must be added there too.
4. **The form.**
   `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/templates/index.html`:
   inputs with ids `gsf-*` for the General dialog (lines 411 to
   440) and `sf-*` for the Servers dialog (292 to 382).
   `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/state.js`
   holds a DOM reference per input (128 to 170) and a global per
   runtime value (12 to 22).
5. **The dialog scripts.**
   `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/gen-settings.js`
   loads (44 to 64) and submits (75 to 140);
   `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/settings.js`
   populates (274 to 299), collects (331 to 366), validates (368
   to 402). *One stale leftover for the audit:* the General dialog
   still sends `seed: current.tts.seed ?? 0` with a comment about
   an API contract that no longer exists (`gen-settings.js:101`
   to 102); the request model ignores the unknown key, so it is
   harmless, but it is a receipt that this file predates the TTS
   generification.
6. **The runtime consumers.** The browser reads general values at
   startup
   (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/app.js:35`
   to 48) and TTS flags from the health check (`app.js:74` to 92);
   the server reads `get_settings()` on every request
   (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/routers/chat.py:222`),
   so saves take effect immediately with no restart.
7. **Tests and docs.**
   `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/tests/test_config.py`,
   `tests/test_models.py`, `tests/test_routers_settings.py`, and a
   Node test if the TTS wiring in `settings.js` is touched
   (`AGENTS.md:33`).

**Where our two knobs would live — options for Q10.** N belongs in
the `tts` section next to `streaming`, reported through the health
response like `streaming` is, and probably exposed in the Servers
dialog since people will tune it. The sanitizer toggle belongs in
`general`, where the partial-update merge picks it up with no
router change, and it could start yaml-only like
`personas_directory` — zero frontend files, and an opt-in shape
upstream tends to accept.

## 5. Seams for the narration future

*Breadth-pass depth (2026-09-21). Mapped against the four open
questions of spec §5.3 (who speaks next, pacing, when to open
interaction beats, dead-air texture), plus two structural facts
that matter more than any of them. Maps only; designs nothing —
the director is the next arc's work.*

- **Who speaks next.** Two lines decide it: the first-speaker
  strategy in `_pick_persona`
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/routers/chat.py:98`
  to 133) and the follower `random.choice` (line 261). A director
  replaces those two decisions. BUT the existing request field
  `who_answers`
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/models.py:17`
  to 20) is already an external hook: a process outside TalkWithMe
  can POST a message with `who_answers` set to a persona name and
  `max_persona_replies` at 1, and it has chosen the speaker with
  no fork at all. That process would be the 2024 Narrator reborn:
  its directive arrives as a user message, exactly as in 2024, and
  the narrative-health taxonomy's `[Director]:` probe (mechanism
  C6, Task 5c) is this experiment done by hand.
- **The structural gap that decides where a director can live.**
  TalkWithMe has NO server-initiated channel to the browser. Every
  SSE stream answers a request the browser itself made
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/chat.js:119`
  to 159). An external director's posts would get their own SSE
  streams that the browser never sees, so nothing would be spoken.
  Three placements follow, and this is the next arc's central
  question, recorded as **Q13**: (a) a director inside the
  browser — a timer that auto-sends narrator turns through the
  existing send path; (b) a director inside the server with a new
  push channel (WebSocket or a long-lived SSE) to the browser; (c)
  an external director plus a browser that polls the room history
  (`GET /api/session/load-room/<room>`) and speaks new lines.
- **Pacing.** The only levers are `max_tokens` (global; §1.4 F2),
  the 80 ms inter-sentence gap
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/tts.js:143`),
  and the LLM-side word-count directive, which is prompt content.
  There is no attach point for timing in the reply loop.
- **Interaction beats.** The browser blocks sending while a turn
  streams (`chat.js:67`) and the microphone is not gated on
  playback (umbrella §8, C4). A director that wants "now the radio
  listens" has to wait for `complete` and would want to gate the
  mic. **The echo chamber is the precedent to copy:** a per-room
  flag read in the reply loop that changes its behavior
  (`chat.py:234` to 250 and 291 to 294, set through
  `PUT /api/chatrooms/{name}/echo-chamber`). A "show mode" room
  flag would follow the same pattern, and upstream's own feature
  doc for it
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/docs/feature_echo_chamber.md`)
  shows the shape.
- **Two injection points for directives.** The 2024 way is a USER
  MESSAGE, which persists, re-enters context as a user turn, and
  is visible in the chat. The other is the SYSTEM-PROMPT TAIL:
  `_with_global_system_prompt` (`chat.py:183` to 201) appends text
  after the persona prompt and memories on every call, so a
  per-turn stage direction — or the entropy terms — could enter
  there without ever appearing in the transcript. About five lines
  of change. → **Q12** records the choice for the director arc.
- **Dead-air texture.** Browser only, via the existing
  AudioContext (umbrella §8, C8). The server has nothing to offer
  here.
- **Persona-to-persona is upstream's own multi-reply design.** Its
  feature doc
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/docs/feature_persona_to_persona.md`)
  states the rules we observed — followers random and
  non-repeating, "who should answer" applies to the first responder
  only — and its addendum explains WHY history is rewritten to the
  `user` role (consecutive assistant messages produced 400 errors
  from the LLM server) and why the audio queues were refactored to
  stamp message ids (audio landing on the wrong persona). Useful as
  a receipt that the label mechanism is deliberate, not accidental.

## 6. Upstreamability audit

*Breadth-pass depth (2026-09-21). How scorbo2 works, read from the
repository, and what it implies for two offerable patches.
Alignment target: [discussion 2026-09-19] upstream-contribution
strategy §4 (outreach deferred past the deadline; build offerable,
contact nobody).*

*Framing changed the same day (owner ruling, recorded in the
umbrella §2 and in the strategy doc §7): the fork becomes a new
app, TalkWithZombies, free to diverge from upstream; only the
accumulator remains a plausible upstream patch, and the
deployment machinery is the real offer. This section therefore
stands as KNOWLEDGE about how scorbo2 works — useful for reading
his code, for the accumulator offer, and for keeping his agent
guide and tests meaningful in our fork — and no longer as a
CONSTRAINT on what we change.*

- **Workflow, measured from git.** Topic branches named
  `issue_<N>_<topic>`, commits titled "Issue #N - description",
  merged by pull request into a per-release dev branch
  (`7.1-dev-branch`), then to `master`, then tagged `N.0` or `N.1`
  with no `v` prefix. Releases 1.0 through 7.1 exist; the default
  branch is `master`. An offerable change therefore starts as a
  GitHub issue.
- **The house genre is the feature doc.** Every feature has
  `docs/feature_<name>.md` with the same skeleton: "This document
  describes an addition to the TalkWithMe app", *Current state*,
  *Desired state*, then an addendum of problems discovered during
  implementation (examples:
  `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/docs/feature_persona_to_persona.md`,
  `docs/feature_echo_chamber.md`, `docs/feature_chat_rooms.md`).
  Spec first, then code, then the addendum — tts-serve's README
  says the same about itself. A patch offered with a feature doc
  in this shape speaks the maintainer's language and lets his own
  agent maintain it.
- **The rules an agent must obey.**
  `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/AGENTS.md` is
  45 KB. The binding ones for us: every code change needs a fully
  green `pytest` with no skips (line 33); new functionality needs
  new tests in the matching `test_*.py` before the change counts as
  done (line 34); routers are stubbed at the import site (line 35);
  the endpoint table in `AGENTS.md` is itself under test
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/tests/test_docs.py`),
  so a new endpoint must be documented or the suite fails.
  Dependencies are pinned exactly
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/requirements.txt`),
  no uv — which our Task 7b installer already respects.
- **Test-coverage asymmetry that changes patch (b)'s cost.** Python
  is fully covered (one `test_routers_*.py` per router, plus
  service and model suites). JavaScript has two Node tests — for
  the persona form (`tests/test_persona_form.js`) and for the TTS
  parameter section plus settings wiring
  (`tests/test_tts_settings.js`) — run with plain Node 20+, no
  packages, in a fresh `vm.Context` per test against a minimal DOM
  stub (`AGENTS.md:30`). **`static/tts.js` has no test at all.** So
  the accumulator either ships untested on the browser side —
  which upstream may accept, since the current splitter is
  untested too — or we add a third Node test in the existing
  harness. → **Q11.**
- **File counts — the surprise.** Patch (a), the sanitizer:
  `app/routers/chat.py` plus possibly `app/services/llm.py`, a
  `general` knob if toggleable, `tests/test_chat_sse.py`, a feature
  doc, one `AGENTS.md` paragraph. Patch (b), the accumulator:
  `static/tts.js`, `static/chat.js`, and — if N is a proper
  setting — the whole seven-file journey of §4 plus the health
  response, plus tests. The "small" patch is the BIGGER one by file
  count. Both stay separable because they share no file except
  possibly `app/config.py` and `app/models.py`, and even there they
  touch different sections.
- **Merge friction.** Eight release tags and issue numbers past
  120 say this upstream moves fast. Small commits off tag 7.1,
  rebased when we bump, are the way to keep the fork thin. Our
  installer already tracks the fork through one `client_repo`
  variable (Task 7b).

## 7. Explicitly out

No fork is created, no patch code is written, and no director is
designed in this tour.

## 8. Questions added by the breadth pass of sections 2–6 (OPEN)

- **Q8 — OPEN. Sanitizer reach.** Head filter only, or head filter
  plus a persist-time sweep for mid-reply labels (§2).
- **Q9 — RULED 2026-09-22. Accumulator remnant policy.** Soft
  limit with ~20 % tolerance for tails under ~30 characters; lone
  one-word lines sent as is; full rules in §3.
- **Q10 — RULED 2026-09-22. Knob homes.** All fork knobs yaml-only
  for the timebox: the show's cadence knobs in a new `show:`
  section; N and its tolerance next to `streaming` in `tts:`; no
  dialogs (§4). The sanitizer toggle no longer exists.
- **Q11 — RULED 2026-09-22. A Node test for `tts.js`.** No new
  harness inside the timebox; the Python suite keeps upstream's
  green rule; a JS test for the packing rules is a follow-up once
  the rules stop moving (§6).
- **Q12 — OPEN, record only. Directive injection point for the
  director arc.** User message, 2024 style, versus the
  system-prompt tail (§5).
- **Q13 — OPEN, record only. Director placement given no
  server-push channel.** Browser timer, server plus push channel,
  or external process plus polling — the next arc's question (§5).

## 9. Update trail

- **2026-09-21** — Document created. Section 1 (pipeline map,
  eight hops, sequence diagram, findings F1–F8, vocabulary,
  itinerary, open questions Q1–Q3) written after the section-1
  conversation, at conversation-level detail (owner rule).
- **2026-09-21, later** — Sections 2–6 written at breadth-pass
  depth (findings and questions, no decisions), after the owner's
  ruling to gather questions across all products before answering.
  Questions Q8–Q13 added (§8); update trail renumbered to §9.
  Unit 1's breadth pass is complete; §7 stands as written.
- **2026-09-22** — Answer pass: F3 corrected (echo for "1." only;
  pauses for the other fragments); §3 gained the ruled accumulator
  rules (N = 100, tolerance, hard flush at line end); Q9–Q11 marked
  ruled in §8.
