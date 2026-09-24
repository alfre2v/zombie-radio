# Story loop — what makes the show take the next turn

**Date:** 2026-09-21 · **Arc:** MVP prototype · **Branch:**
`alfre2v/task6-recon-brief`
**Type:** design discussion — the second of the two decisions pulled
into this arc by the owner's 2026-09-21 ruling (TODO.md boundary
note); it follows [discussion 2026-09-21] prompt-structure because
the loop's shape depends on who assembles the prompt.
**Status:** **DECIDED 2026-09-21 (owner):** Placement 1 — the
browser is the metronome, the server is the director (§4, §8);
endless loop with cadence-based interaction beats (§9 Q2);
half-duplex microphone, hold-to-talk (§9 Q3–Q4); dead-air static
as explicit day-three polish (§9 Q5); the show on a separate page
(§9 Q6).

*Context for the cold reader.* Zombie-Radio is a live, audio-only
radio play performed by four LLM personas with an audience that can
talk back over push-to-talk. The prototype runs on TalkWithMe
(scorbo2's multi-persona chat app, tag 7.1) as the client and
director. TalkWithMe's unit of work is a chat turn: the browser
posts one user message, the server streams up to four persona
replies as server-sent events, and then everything stops until the
browser posts again. A radio show must keep turning with nobody
typing. The prompt-structure decision of the same day already
settled how one turn is generated (one shared context in
screenplay form, a code director in the server, a grammar-enforced
script streamed and re-emitted as the browser's existing events);
this document settles what makes the next turn happen and how the
audience's voice gets in. The fork is named TalkWithZombies.

*Path conventions:* sibling-clone files with full absolute paths;
this repository's files relative to its root. Labels: measured /
docs-say / believed.

---

## 0. The question in one sentence

**What makes the show take the next turn when no human has sent a
message, and how does the audience's voice enter the loop?**

## 1. Round one — the agent's presentation, kept verbatim at the owner's request

*(2026-09-21. The owner: "Very good presentation of the options …
I want all this answer persisted verbatim. I found your redaction
here very readable and to-the-point.")*

**What the loop must produce.** From spec §2.1: four characters
improvising continuously, a single push-to-talk control, and the
signature interactions, a name asked and remembered, a simple
question answered. From spec §5.3, the four open design questions:
who speaks next, pacing, when to open interaction beats, dead-air
texture between segments, plus a session length target still open.
From the 2024 code, a working answer to all four at prototype
quality: a four-state machine that answered a pending radio
message, closed the beat with the radio smoking, or drew a 95/5
coin between ordinary dialogue and a cry for help that opened the
microphone
(`/Users/alfredo/workspace/hackTNT_2026/zombie_radio_ai/zradio_local/zradio_local.py:686`
to 699). From the timebox's exit criterion: at least ten unattended
turns, one interaction beat that opens the mic and absorbs the
reply.

**What is already fixed.** The prompt-structure decision put the
director in the server, in code, assembling one streamed request
per round and emitting the browser's existing SSE events per parsed
line. So the director owns the story: beat choice, speaker
allowlist, line budget, directive text. What it does not own is
time. And the fact that shapes everything: TalkWithMe has no
server-initiated channel to the browser. Every SSE stream answers a
request the page made
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/chat.js:119`
to 159), the page refuses to send while a turn streams
(`chat.js:67`), and a grep of the whole app finds no EventSource,
no WebSocket, no background task, no timer beyond a retry. Upstream
never needed one.

**The three placements, Q13, with receipts.**

1. **Browser as metronome, server as director.** A small `show.js`
   in the page runs the clock: when a round's `complete` arrives
   and the audio queues drain, it requests the next round. The
   server gains one endpoint beside `/api/chat`, say
   `/api/show/round`, taking the room and an optional audience
   transcript, running the director and the grammar-constrained
   generation, and streaming the same events. The SSE reader in
   `sendMessage` (`chat.js:135` to 159) is extracted into a
   function both callers use; `handleSSEEvent` is untouched. The
   decisive fit argument: the only component that knows when a
   speaker has finished playing is the browser, whose audio queues
   and flags live in `state.js:43` to 46 and are drained by
   `tts.js:136` to 150. Pacing and dead air are decisions about
   playback, and playback is browser state. Cost: about one day.
   Weakness: the loop lives in a tab, so a backgrounded or sleeping
   tab pauses the show; on demo day the tab is foreground, and the
   fallback is the canned episode. A second weakness, mild: the
   director's state persists in the server, but the impulse to
   continue comes from the page, so a page reload restarts the
   clock, not the story.

2. **Server loop plus a push channel.** An asyncio task started in
   the FastAPI lifespan
   (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/main.py:80`
   to 120) runs the director on its own clock and publishes events
   to a long-lived SSE endpoint the browser subscribes to with
   EventSource, feeding the same `handleSSEEvent`. Fit: the server
   owns both story and time, and the show survives the tab. But the
   server does not know when audio finished playing, so pacing
   needs a back-channel, a `POST /api/show/played` from the
   browser, or estimation from tts-serve's `time_used` and `rtf`
   telemetry, which is seam question S5 arriving on schedule.
   Cost: one and a half to two days, for the endpoint, the
   EventSource consumer, the back-channel, and the lifecycle,
   start, stop, reconnect, one show at a time. The `isStreaming`
   guard and the mic path also need rewiring since nothing is "in
   flight" from the page's point of view.

3. **External director process plus polling.** The 2024
   architecture transplanted: a separate Python process posts
   rounds through the API and the page polls
   `GET /api/session/load-room/<room>` for new lines
   (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/routers/session.py:53`
   to 74). Poor fit: the history endpoint returns complete messages
   only, so token streaming to the page is lost, speech can start
   only after a whole line is persisted, and the polling interval
   adds latency on top. It also duplicates the director we just
   decided lives in the server. Cost moderate, value lowest. Ranked
   last; recorded so it is not re-proposed.

**The loop as a state machine, browser side.** Idle, generating,
playing, listening, dead air. Transitions: idle requests a round;
tokens stream while the first lines already play; when the last
`done` arrives and the queues drain, either open the mic if the
director's beat asked for it, or request the next round. Two
refinements worth the small cost. Prefetch: request round N+1 when
the last line of round N starts playing, not when it ends, so
generation overlaps playback and the 2024 blocking pause
disappears; the accumulator's pipelining already does this within a
round, this extends it across rounds. Dead air as a cover, not a
gap: while a round is in flight with nothing left to play, a static
loop plays through a second buffer source in the existing
AudioContext (`tts.js:205` to 219), which is challenge C8's mixer
already in hand, and it strengthens the fiction while buying the
pipeline time, exactly as the brainstorm proposed.

**The interaction beat and the microphone.** Today the mic is a
toggle whose transcript is auto-sent as a user message
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/stt.js:9`
to 98). Under the loop: the director decides when the radio
listens, the browser enters the listening state, the mic is gated
so it cannot open while audio plays, the C4 revisit, the transcript
rides along with the next round request as audience traffic, and
the director constrains that round to one speaker who answers.
Hold-to-talk replaces the toggle if you want the spec's "release
ends the utterance" literally. The 2024 escalation, five exchanges
and then the radio smokes, becomes director state rather than a
canned string appended to the line.

**Recommendation.** Placement 1, browser as metronome, server as
director. It puts each decision where its information is: story in
the server, time in the browser. It reuses the page's SSE machinery
and the events the prompt-structure decision already committed to,
it is the cheapest by a day, and its one real weakness, the tab
must stay alive, is a demo-day discipline we have anyway. Placement
2 is the right upgrade for the unattended booth of the future
vision, where no tab can be trusted, and nothing in placement 1
blocks that upgrade, because the director code is server-side in
both. I hold this more firmly than the prompt-structure lean was
held at first, because the browser-knows-playback argument is a
fact about the code, not a judgment.

**Against the three-day box, honestly.** Prompt structure about two
days, grammar half a day, this loop about one day. Three and a half
against three. The midpoint checkpoint exists for exactly this, and
the scope levers are clear: the minimal loop, request the next
round on `complete`, is hours; prefetch and dead-air cover are
day-three polish that the exit criterion does not demand.

**Questions only you can answer** *(as asked; answers in §9)*:

- The browser as the show's clock: does that sit right with you,
  given the tab must stay in the foreground on demo day, or do you
  want the server to own time from the start and pay the extra day?
- Loop shape: endless with beat probabilities, the 2024 coin, or an
  episode clock with acts and a target length? The spec left the
  length open; the MVP can run endless and let the hybrid scaffolds
  bring structure later.
- When the mic opens, does playback pause, radio half-duplex, or
  duck under the listener's voice?
- Hold-to-talk or keep the toggle for the MVP?
- Dead-air static between rounds: in the box, or explicitly
  day-three polish?
- Show mode as a room flag, following the echo-chamber precedent,
  or a separate page for the show and the chat UI left as the
  rehearsal tool?

## 2. What the loop must produce (requirements, consolidated)

- **Spec §2.1 (MVP):** four characters with distinct cloned voices
  improvising continuously; one push-to-talk control; signature
  interactions — ask and remember the listener's name (with the
  fiction-friendly confirmation loop, challenge C6), answer a
  simple question, ask for help locating the lab.
- **Spec §5.3 (the director's open questions):** who speaks next;
  pacing; when to open interaction beats; dead-air/static texture
  between segments; session/loop length target (open).
- **The 2024 state machine** (`zradio_local.py:686` to 699 and
  750 to 793): pending radio message → answer it; message consumed
  → the radio smokes, closing the beat; otherwise a 95/5 coin
  between a dialogue round and a cry for help that opened the mic;
  a scripted escalation of up to five exchanges; a fixed
  ten-second recording window; strictly blocking pipeline
  (generate → synthesize → play → record).
- **The timebox's exit criterion** (TODO.md, Task 6): at least ten
  unattended turns with the four placeholder personas; speakers
  chosen by the new structure; one audience interaction beat that
  opens the microphone and absorbs the reply; sentences accumulated
  rather than split; on the deployed stack through the tunnel.
- **Brainstorm §7 (2026-09-13), loop shape idea:** in-fiction dead
  air — static, emergency-broadcast tones, "signal lost…
  reconnecting" — between segments, buying the pipeline time while
  strengthening the fiction.

## 3. What the prompt-structure decision already fixed

The director is CODE in the SERVER. Per round it decides the beat,
the speaker allowlist, the line budget, the stage direction and the
entropy terms; assembles one request (system = cast sheet, history
= the script so far, user = the directive; `grammar` = the
screenplay grammar narrowed to the allowlist); streams the reply;
parses it at line breaks; and emits the browser's existing `start`,
`token`, `done`, `complete` events per speaker line. The director
owns the STORY. It does not own TIME, because the server has no
channel to the browser that the browser did not open.

## 4. The three placements (Q13) — fit and build cost

Full text in §1. Summary table:

| Placement | Who owns time | Who owns story | Streaming to the page | Knows when playback ended | Build cost | Verdict |
|---|---|---|---|---|---|---|
| 1. Browser metronome, server director | browser (`show.js`) | server (director) | yes — existing SSE per request | yes (audio queues are browser state) | ~1 day | **ADOPTED** |
| 2. Server loop + push channel | server (asyncio task) | server | yes — new long-lived SSE + EventSource | no — needs a back-channel or S5 telemetry | 1.5–2 days | the future booth's upgrade; nothing in 1 blocks it |
| 3. External process + polling | external process | external process | no — history has complete messages only | no | moderate | rejected; recorded so it is not re-proposed |

## 5. The loop as a state machine (browser side)

States: **idle → generating → playing → (listening | dead air) →
idle**.

- *idle:* request a round (`POST /api/show/round` with the room
  and, if the previous state was listening, the audience
  transcript).
- *generating:* the SSE stream arrives; `start`/`token`/`done` per
  line feed the existing bubble and TTS machinery; the first lines
  play while later ones are still being generated.
- *playing:* the audio queues drain (`state.js:43` to 46;
  `tts.js:136` to 150).
- *listening:* entered only when the director's beat asked for the
  audience AND the queues are empty; the push-to-talk control is
  enabled; on release the transcript is attached to the next round
  request.
- *dead air:* while a round is in flight with nothing left to play,
  a static loop plays through a second AudioContext buffer source
  (day-three polish, §9 Q5).

Refinements: **prefetch** — request round N+1 when the LAST line of
round N starts playing, so generation overlaps playback; **the
`isStreaming` guard** (`chat.js:67`) is the chat page's, not the
show page's — the show page's states replace it.

## 6. The interaction beat and the microphone

- The director decides WHEN the radio listens (a cadence, §9 Q2)
  and constrains the answering round to ONE speaker via the
  grammar's allowlist.
- The browser enters *listening* only with empty queues
  (half-duplex by construction, §9 Q3): nothing to pause, nothing
  to duck; the actors cannot be heard by the mic (challenge C4),
  and Whisper receives only the listener (C1).
- **Hold-to-talk** (§9 Q4): press = record, release = end of
  utterance — the spec's literal push-to-talk; replaces the
  click-start/click-stop toggle of `stt.js:9` to 14.
- The transcript rides with the next round request as AUDIENCE
  TRAFFIC in the directive (in-fiction: "a voice on the radio
  says…"), never as a bare user message; the C1 revisit's
  substituted "No response received from STT server" text must
  not reach the director (drop empty or low-confidence transcripts
  at the proxy).
- The 2024 escalation (five exchanges, then the radio smokes)
  becomes director STATE, not a canned string appended to a line.

## 7. Dead air

In-fiction static between rounds: a small looped audio asset
played through a second buffer source with a gain node in the
existing AudioContext (`tts.js:205` to 219 — challenge C8's mixer
already in hand), started when the queues are empty and a round is
in flight, stopped when the first line of the round starts. About
an hour of work; **explicitly day-three polish** (§9 Q5): outside
the exit criterion, built only if the midpoint checkpoint is
green, first on the polish list.

## 8. The decision

**Placement 1 — browser as metronome, server as director.** Each
decision sits where its information is: story in the server, time
in the browser. Reuses the page's SSE machinery and the events the
prompt-structure decision committed to; cheapest by a day; its one
real weakness — the tab must stay in the foreground — is a
demo-day discipline we have anyway, and the canned episode is the
fallback. Placement 2 remains the upgrade path for the unattended
booth, and nothing in Placement 1 blocks it, because the director
is server-side in both. **Owner, 2026-09-21: "Yes, let's go with
Placement 1, browser as metronome, server as director."**

## 9. The owner's answers and the agent's recommendations (2026-09-21)

- **Q1 — the browser as the show's clock.** Owner: yes, Placement 1.
- **Q2 — loop shape.** Owner: the agent's recommendation. **Agent:
  endless, but with a CADENCE, not a coin.** The MVP runs an
  endless loop with beats chosen by the director; episode structure
  arrives post-MVP through the trajectory scaffolds, as the spec
  planned. One correction to the 2024 shape: the interaction beat
  should be a cadence, not a five-percent coin — at 5 %
  (`zradio_local.py:693` to 699) an audience member waits ~20
  turns on average for an invitation to speak, fine for an
  unattended radio and wrong for a demo where people stand in front
  of the laptop. *(First formulation: "the director opens the radio
  to listeners every third or fourth round, on a clock it owns".)*
  **Owner pushback, accepted, same day:** (1) rounds are seconds
  long, so a round count opens the mic roughly every minute, and
  every listening window is a pause the audience hears — "the show
  will be on pause for a significant amount of time"; (2) a fixed
  count makes the show predictable — the interval needs randomness;
  (3) the parameter must be configurable and tuned from the owner's
  ear at a real voice performance. **Revised mechanism:** the
  director measures the time since the last interaction beat in
  PLAYED AUDIO, not rounds. Below a configurable MINIMUM interval it
  never opens the radio; above a configurable MAXIMUM it always
  does; in between, the probability rises linearly with elapsed
  time — the beat is guaranteed within the window and unpredictable
  inside it. Three yaml-only knobs to start: `interaction_min_s`,
  `interaction_max_s`, `listen_window_s` (names indicative). The
  entropy terms keep the dialogue rounds varied in between.
  **Consequence the owner named:** the listening state is silence by
  construction, so if the windows are frequent, in-fiction texture
  during listening (static, "anyone out there, over") stops being
  polish and becomes part of the beat — dead air (§7) is needed the
  day the cadence is tuned, still not on day one.
- **Q3 — mic versus playback.** Owner: the agent's recommendation.
  **Agent: half-duplex by construction.** Ducking keeps the actors'
  voices in the room while the listener speaks — exactly the
  self-hearing problem of C4 — and feeds Whisper mixed audio (C1);
  pausing mid-line is awkward. The mic can only open in the
  *listening* state, when the director has asked for the audience
  and the queues have drained, so there is nothing to pause or
  duck; the push-to-talk control is disabled in every other state.
  The radio fiction's own rule: one station transmits at a time,
  "over" hands the channel over.
- **Q4 — hold-to-talk.** Owner: "Definitely hold-to-talk"; later,
  low priority, explore opening the mic at key narrative moments as
  in 2024 — with the intuition that browser security will not
  allow a tab to open the mic when it wants. **Agent: the intuition
  is half right.** The browser requires a user gesture the FIRST
  time a page asks for the microphone (and for the AudioContext,
  which the first click already provides). Once the origin has been
  granted permission, a script may call `getUserMedia` again on its
  own, with the recording indicator showing, as long as the tab is
  foreground. So opening the mic at key moments without a click is
  feasible after the first grant — a post-MVP option, not a dead
  end. *Believed; one minute to verify in the browser on the fork.*
- **Q5 — dead air.** Owner: "I would love this, but only after we
  have accomplished our main objectives … explicitly day-three
  polish is my lean." **Agent: agreed, and first on the polish
  list** — the minimal version is about an hour in the existing
  AudioContext (§7); outside the exit criterion; built only if the
  midpoint checkpoint is green.
- **Q6 — room flag or separate page.** Owner: undecided, leaning
  to a separate page for the freedom it gives — "changing the look
  of the page to make it look more like an old radio transmitter,
  all black and white… a horror show from the 30s." **Agent:
  separate page, and it is also the easier one to reason about.** A
  `/show` route with its own template that includes the existing
  scripts it needs (`state.js`, `tts.js`, `stt.js`,
  `persistence.js`) and a new `show.js` for the loop and the
  push-to-talk control. The chat UI stays intact as the rehearsal
  and debugging tool; nothing in `chat.js`'s send path or the
  who-answers controls learns about show mode; the page is free to
  look like a 1930s radio transmitter. The room concept still
  serves server-side: the show runs in a room and its script
  persists there like any chat. The room-flag route (the
  echo-chamber precedent, `chat.py:234` to 250) would be fewer new
  files but would tangle show behavior into code built for
  something else. **Adopted.** *[note 2026-09-23: the server-side
  half is superseded — the show is one show decoupled from the chat
  rooms, with a folder per run under `shows/` and the trim as a flag
  ([discussion 2026-09-23] show-engine-design §3); the separate page
  stands.]*

## 10. What the fork builds (the loop's share of the timebox)

- **Server:** `POST /api/show/round` — a sibling of `_chat_stream`
  (`chat.py:208`) that runs the director (beat, allowlist, budget,
  directive, cadence state), the grammar-constrained request, the
  stream parser, and emits the existing SSE events; the audience
  transcript arrives in the request body.
- **Browser:** `templates/show.html` + `static/show.js` — the state
  machine of §5, the hold-to-talk control, a start/stop control, a
  transcript display; the SSE reader extracted from `sendMessage`
  (`chat.js:135` to 159) into a shared function; `handleSSEEvent`
  reused or a thin show-page variant.
- **Minimal loop (hours):** request the next round on `complete`
  once the queues drain. **Prefetch and dead air (day-three
  polish).**
- **Against the box:** prompt structure ~2 days + grammar ~0.5 +
  loop ~1 = 3.5 against 3; the midpoint checkpoint decides; the
  scope levers are prefetch, dead air, and the look of the page.

## 11. Open items

- The cadence knobs (minimum and maximum interval in played
  seconds, listening window length) — tuned from the owner's ear in
  rehearsal; yaml-only until they settle.
- What the show page shows (transcript, current speaker, a
  "transmitting / listening" indicator) versus the 1930s look —
  the look is polish.
- Whether the audience transcript should be shown as a line in the
  script (it is in-fiction radio traffic) — probably yes, as
  "Listener:".
- Programmatic mic opening (Q4) — post-MVP, verify the permission
  behavior once.
- The server-owned-time upgrade (Placement 2) for the booth vision
  — post-MVP; S5 telemetry is its pacing input.

## 12. Update trail

- **2026-09-21** — Document created after one conversation round:
  the agent's presentation (kept verbatim in §1 at the owner's
  request), the owner's six answers, the agent's recommendations
  for Q2, Q3, Q5, Q6 and the browser-permission correction for Q4;
  Placement 1 decided. Same day: the owner's pushback on the Q2
  cadence accepted — time-based, randomized within a min/max
  window, configurable; dead air re-ranked as needed when the
  cadence is tuned.
