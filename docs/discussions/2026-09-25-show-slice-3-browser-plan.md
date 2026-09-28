# Show engine, slice 3 — the browser: the plan

**Date:** 2026-09-25 · **Arc:** MVP prototype · **Branch:**
`alfre2v/show-slice-2` (recorded in slice 2's open pull request, at
the owner's request: "in the interest of time")
**Type:** discussion — how slice 3 of the show engine, the browser, is
built, decided before the code.
**Status:** DECIDED — three rulings (§1.3), then the eight-item
agenda (§4) ruled on 2026-09-25: five items in one pass (§5), what the
page shows (§6), the steps (§7). Append-only from here — reality
reports back through dated addenda. The build is the TODO's slice 3.

*Context for the cold reader.* The show engine (TODO Task 6b) is built
in the fork TalkWithZombies
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`) to the design
of [discussion 2026-09-23] show-engine-design ("SED"). Slices 1 and 2
built the server side: the story, the grammar, the record, the
director, the trim, the debug switch, the listener's route, and a
driver that plays rounds without a browser. The checkpoint passed on
2026-09-24 (6 of 6 criteria; verdict: continue). Slice 3 is the
browser's part: the `/show` page that plays the rounds aloud, asks for
the next one, and lets a listener talk back. On 2026-09-25 the agent
proposed a lean slice 3 that changed two of the TODO's steps without a
shape round; the owner rejected it, moved the timebox's end, ruled
that the show's frontend lives in its own files, and asked for a
proper plan (§1). The gap between rounds, raised on the way, is §2-§3.

*Conventions.* As in SED: the verbatim blocks are the transcript's
text, extracted by script — the owner's messages quoted exactly as
written, the agent's with their headings demoted to fit this
document; nothing removed. Sibling-clone files with full absolute
paths; this repository's files relative to its root.

## 1. A plan rejected, and three rulings (2026-09-25)

### 1.1 The agent's proposal (verbatim)

Here's where things stand, and a leaner plan for slice 3 that fits a few hours.

**The clock:** it's 12:40 on Thursday. About 46 of the 72 hours are used, so about 26 remain; the timebox ends Friday at 14:46.

**One blocker on your side:** both slice 2 PRs are still open ([TalkWithZombies#3](https://github.com/alfre2v/TalkWithZombies/pull/3), [zombie-radio#11](https://github.com/alfre2v/zombie-radio/pull/11)). Slice 3's branch gets cut from the fork's `master` once #3 is merged.

**Slice 3, trimmed to what the exit criterion needs.** I checked upstream's `static/tts.js`. It already has an ordered fetch-then-play pipeline, but it's tied to the chat: every clip is uploaded to the current chat room. So I'd give the show its own small player and leave the chat's files alone:

- **a. Skip 3.1, the SSE reader extraction.** `show.js` gets its own reader, about 20 lines copied from `chat.js`, and `chat.js` stays untouched, which is closer to upstream. The extraction becomes a follow-up.
- **b. Replace 3.3's accumulator with one voice request per line.** Each `done` event is already a whole spoken line, usually one or two sentences. The next line's audio is fetched while the current one plays. The accumulator becomes a follow-up, for when lines grow long.
- **c. 3.2, the `/show` page and `show.js`.** The page moves through idle → generating → playing → listening. It asks for the next round when the audio drains. It reports the played seconds as the exact sum of the audio clips' durations.
  - With this alone, you can already hear ten unattended rounds.
  - About 1.5–2 h (my estimate).
- **d. 3.4, hold-to-talk.** It records only after an invitation, with a 10 s window and a 30 s press cap. The audio goes to `/api/show/listen` and the result rides the next round. "Heard: …" shows only while debug is on. About 1–1.5 h.
- **e. 3.5, the exit test by ear, with you listening.** About 30 min.
- **f. 3.6, closing the timebox:** the `tz-0.2` tag and the installer re-proof on the box. This can slip past the timebox without hurting anything.

**Order:** c, d, e, f. After c, you can hear the show; after d, you can talk to it. If time runs out, only f is left undone.

**Tradeoff:** there'll be about 3–4 s of dead air between rounds: generating the round (~1.5 s), then voicing its first line (~2 s). Prefetching and static fill-in stay on the polish list, as planned.

Go with a–f as proposed? Once you've merged #3, I'll cut the branch and bring 3.2's detailed shape.

*[Two slips in it, corrected in chat the same day: 2026-09-25 is a
Friday (not Thursday) and the old timebox ended on Saturday
2026-09-26 (not Friday).]*

### 1.2 The owner's reply (verbatim)

> No, you plan is NOT accepted.
>
> However there are aspects of it that we can use for a new plan.
>
> #### Removing the time pressure
>
> I am going to change rules on the flight, do not push back on this one: I have decided to drop the time box constrain. We have already passed the thorniest part of the development and now it's all about the browser, we can make this work. I hereby decree (king of the hill style) that the new time box limit is Mon, Sep 28, 2026. 
>
>
> #### Revision of plan for browser work (Slice 3)
>
> I general I like the idea of separating our frontend  code from the upstream, let's leave upstream js, html, and css files alone and add our own. It is ok to copy as much code as we want from the upstream files (duplication is ok), but it buys os the freedom to change things to fix our use case without worry to break upstream. 
>
> So, you ideas are good, and we are going to build on them, but I cannot proceed with a plan improvised and changed on the flight like that. 
>
>
> #### Clarification question to kickstart the new plan
>
> "there'll be about 3–4 s of dead air between rounds: generating the round (~1.5 s), then voicing its first line (~2 s). Prefetching and static fill-in stay on the polish list, as planned" ... Why? Explain why this added time?

### 1.3 The rulings

- **The timebox's end moves to Monday 2026-09-28** (from Saturday
  2026-09-26 at 14:46; the checkpoint already passed). The owner:
  "do not push back on this one".
- **The show's frontend lives in its own files.** Upstream's
  JavaScript, HTML and CSS stay untouched; copying from them is
  welcome (duplication accepted), for the freedom to fit the show
  without breaking the chat.
- **Slice 3's plan is made in discussion, not improvised.** The
  agent's two unshaped changes — skip the extraction of the stream
  reader (TODO 3.1) and voice one line at a time instead of the
  accumulator (TODO 3.3) — are candidates on the agenda (§4), not
  decisions.

## 2. The gap between rounds, and what `done` means

### 2.1 The agent's answer to the owner's question (verbatim)

Understood on both changes:
- **The new deadline is Mon 2026-09-28.**
- **Our own frontend files, leaving upstream's JS, HTML and CSS alone** (copying from them is fine).

I'll write both into the docs when you say so. And you're right about the plan: I cut 3.1 and changed 3.3 in a single message, without a shape round.

#### Why there's a gap between rounds

**The short answer:** at the boundary between two rounds, three things happen one after another, and nothing is playing while they do:

1. **The page waits for the audio to drain before asking for the next round.** That's the design ("the browser is the clock", SED; the TODO's 3.2 says "the next round requested when the audio queues drain"). Two reasons:
   - the `played_s` sent with the request is only exact once the audio has actually played, and the cadence runs on it;
   - after an invitation, the next round depends on what the listener said, which doesn't exist yet.
2. **The model writes the first line.** Measured in yesterday's checkpoint drive, through the app and the tunnel (the same path the browser will use): the first line was complete after **0.76–0.94 s**, and **2.37 s** on the round right after a trim (the slot swap).
3. **The voice synthesizes that line**, and only then can it play. Measured through the app's `/api/tts`:
   - **1.08 s and 1.28 s** for the two short spoken questions in yesterday's `--speak` run;
   - **~1.8–2.8 s** for short cast lines on 2026-09-24 (handoff 3, §5).

So the silence at the boundary is roughly **0.8 s + 1–3 s ≈ 2–4 s**, and about 1.5 s more after a trim.

**A correction to my own number:** I wrote "generating the round (~1.5 s)", but that's the whole round's time. Only the first line matters here: it can go to the voice as soon as its `done` event arrives (~0.8 s), while the rest of the round keeps streaming. My "3–4 s" was the pessimistic end.

**Why there's no gap inside a round:** the same costs exist there, but they're hidden:
- line 2's text arrived long ago (a whole round streams in ~1.1–1.9 s);
- its audio is fetched while line 1 plays.

At the boundary there's nothing to hide behind, because by design nothing is requested until the audio drains.

**One thing not yet measured:** whether the voice synthesizes faster than the audio plays. If it doesn't, small gaps can open inside a round too. We'll only know from the browser.

**How the boundary gap could be hidden** (the "prefetch round N+1" item on the polish list):
- Request round N+1 when round N's text has finished streaming, not when its audio has.
- Send `played_s` as the seconds already played plus the length of the audio still queued. That length is known exactly once the clips are decoded.
- Then N+1's first clip is ready before N's audio ends.
- Two limits:
  - **after an invitation**, the page must still wait, because the listening window is the gap;
  - **the model and the voice share one GPU**, so running them at the same moment may slow both. That hasn't been measured.

Over to you for the new plan.

### 2.2 The owner's follow-up (verbatim)

> "Only the first line matters here: it can go to the voice as soon as its done event arrive"... Wait, I do not understand this. The done event happens at the end of the full round generation, no? That's the llm signal that it finished the full generation. Before, in TalkWithMe, a done event corresponded to a character finishing to speak, but not in our design. Am I correct here?
>
>   I like your proposals in "How the boundary gap could be hidden"... Not sure it is worth to worry about this now, but worth documenting.
>
> Why don't we, in the interest of time, open the discussion of this new plan for slice 3 (we kind of already opened actually), and save the new discussions in the currently open PR of zombie-radio... I know, not ideal, but it's only you and me here... I won't tell anyone 😃

### 2.3 `done` marks one line, not the round

The owner's reading — that `done` comes once, when the model has
finished the whole round — is the natural one, since the round is a
single request to the model; but the show kept the chat's events on
purpose, and `done` marks **the end of one script line**. The round's
end is marked by two later events, `round` (the summary) and
`complete`. The receipts:

- **The parser** (`app/show/parser.py`, `_end_line`, line 111 in the
  fork): at each line's end it emits
  `{"type": "done", "persona": ..., "text": <the spoken line>}`.
- **The router's test** (`tests/test_routers_show.py`, line 106): a
  two-line round streams exactly `start, done, start, done, round,
  complete` (the `token` events aside).
- **The checkpoint drive** (2026-09-24): the driver prints each line
  when its `done` arrives, with the seconds since the request left —
  round 1: Moira at 0.83 s, Ralph at 1.21 s, Samantha at 1.53 s; the
  whole round took 1.87 s.
- **Upstream's chat** (`app/routers/chat.py`, lines 339 and 341):
  `done` after each persona's reply, `complete` after all of them. In
  TalkWithMe each persona's reply is its own request to the model; in
  the show, one request writes every line and the parser cuts it into
  lines as the tokens stream — so a show line plays the part a
  persona's reply plays in the chat.

So the first line can go to the voice at about 0.8 s, while the rest
of the round is still being written.

### 2.4 How the events reach the page

The owner (verbatim):

> Ah, I see, this events are meant to guide the browser UI. Right? I am surprised that the events are stored in a `List[Dict]`, I would have expected a queue, as this is an async functions. Right?  Did you copy this pattern from upstream? How do this events make their way to the browser?

The agent's answer, condensed:

- **Yes, the events are the protocol between the server and the
  page:** `start` (who speaks, the mood), `token` (the text as it is
  written), `done` (the line is complete — for the show, the moment it
  can go to the voice), `round` (the summary: the kind — after an
  invitation the page listens — and `heard`), `complete` (the round's
  text is over).
- **A list, not a queue:** `LineParser.feed` is a plain method — one
  piece of text in, the events it completes out (zero while a
  speaker's name is still arriving, one `token`, or a `token` and a
  `done` when a piece like "Over.\n" ends a line); the router yields
  each at once. A queue joins two tasks running at the same time; here
  one task pulls a chain of async generators from the socket end, each
  step suspending while it waits for the network — the generators are
  the pipe, and back-pressure comes free.
- **From upstream:** the pattern (an async generator of
  `data: <json>` strings into a `StreamingResponse`, as
  `app/routers/chat.py` does) and the event names and shapes; the
  reader of the model's stream (upstream's `_iter_completion_chunks`,
  its line reading moved into `_iter_sse_chunks` in slice 1). **Ours:**
  the parser, and its list per piece.
- **The path:**

  ```
  llama.cpp on the box
    │  SSE over HTTP, through the tunnel (OpenAI format)
    ▼
  _iter_sse_chunks   httpx client.stream + aiter_lines: one parsed chunk per "data:" line (app/services/llm.py)
    ▼
  stream_round       yields {"token": ...}, then {"timings", "finish_reason"}
    ▼
  _round_stream      parser.feed(token) → events → yield "data: <json>" (app/routers/show.py)
    ▼
  StreamingResponse  each string to the socket as it is yielded; text/event-stream, no-cache, X-Accel-Buffering: no
    ▼
  the browser        fetch POST → resp.body.getReader() → TextDecoder → "data: " lines → JSON.parse → by type
  ```

  Two SSE hops — the model to the app, the app to the page — and the
  app translates. The browser end is upstream's `static/chat.js`
  (lines 135-159): `fetch` with the body read by hand, because
  `EventSource` only does GET and a round is a POST.

## 3. Hiding the gap: prefetch — documented, not scheduled

The owner (verbatim, from §2.2):

> I like your proposals in "How the boundary gap could be hidden"... Not sure it is worth to worry about this now, but worth documenting.

The idea, as the agent proposed it (§2.1):

- **When:** request round N+1 as soon as round N's text has finished
  streaming (its `complete` event), not when its audio has drained.
- **The clock stays honest:** `played_s` is sent as the seconds
  already played plus the duration of the audio still queued — known
  exactly once the clips are decoded. The director's cadence then
  sees what the listener will have heard when N+1 starts playing.
- **The gain:** N+1's first clip is ready before N's audio ends; the
  boundary's ~2-4 s of silence (§2.1) disappears whenever generation
  and voicing together are shorter than the audio still queued.
- **The limits:** after an invitation the page must wait — the
  listening window is the gap, and the next round depends on what is
  heard; and the model and the voice share one GPU, so running them
  at the same moment may slow both (not measured).
- **Where it stands:** the TODO's polish list keeps "prefetch round
  N+1"; this section is its design note. Nothing in slice 3's plan
  depends on it.

## 4. The agenda (the agent's proposal, 2026-09-25, verbatim)

Eight decisions, each with my pick in bold. Attack any of them; then we go one at a time.

1. **The files.** Ruled: our own, upstream's untouched. Pick: **`templates/show.html` plus a `static/show/` folder** — `show.js` (the loop and its states), `sse.js` (the stream reader, copied from `chat.js`), `player.js` (the voice queue), `mic.js` (hold-to-talk), `show.css` — served by `GET /show` in the show router.
2. **How lines get their voice.** The TODO's 3.3 plans an accumulator (about 100 characters of whole sentences, flushed at each line end). The alternatives: one voice request per line, on its `done` event; or per sentence as the tokens arrive (upstream's streaming style). Pick: **one request per line first**, the next line fetched while the current one plays; the accumulator or per-sentence only if the ear asks for it.
3. **The loop and the clock.** Pick: **as designed — the next round is requested when the audio drains**, and `played_s` is the sum of the played clips' durations (exact, from the decoded audio). Prefetch stays documented (§3), for later.
4. **The listener's turn.** After an invitation's audio drains, the listening window opens (`listen_window_s`, 10 s) with the talk button enabled; a press stops the window's count and records; release or the press cap (`press_cap_s`, 30 s) ends it; the audio goes to `/api/show/listen` and the result rides the next round request; no press, and the next round goes without a transcript (static). How the page learns the timers and the debug switch: pick **the start response carries them** (`listen_window_s`, `press_cap_s`, `debug`).
5. **What the page shows.** Pick: **the minimum** — Start/Stop, the state (on air, listening, thinking), the talk button, and the lines as they are spoken; "Heard: …" only while debug is on; the 1930s look stays polish.
6. **Failures** (a round error, a dropped tunnel). Pick: **stop and say so, with a Resume button** that continues the same run — the record holds everything the next round needs.
7. **Tests.** Pick: **Node tests in upstream's style for the pure pieces** (reading the stream, the played-seconds count, the state changes); the page itself by hand and by ear.
8. **The steps, cut again after 1-7.** Pick: 3.1 the page, the route and the reader (lines shown, no voice yet); 3.2 the voice (lines voiced in order, the loop on drain, the played seconds); 3.3 the listener's turn; 3.4 the exit criterion by ear; 3.5 close (the `tz-0.2` tag, the installer's pin, the re-proof on the box).

## 5. The agenda's first pass (2026-09-25)

### 5.1 The owner's reactions (verbatim)

> Thanks. This is very useful.
>
> Ok, let's analyze "The agenda for slice 3 (also §4 of the doc)":
>
> Here is my initial reaction to the items you wrote above. I already accept most of them to be executed with your lean, but there are a couple that I want you to bring to me one by one for a detailed discussion:
>
> 1. the files: Looks ok to me.
> 2. How lines get their voice: We need the accumulator, it's not optional. Why? Because if we don't then Lines like "Testing. 1. 2. 3. Done." result in 5 requests to the TTS engine with very short sentences, this makes the pauses between sentences uncomfortably long, and break the pronunciation of the TTS engine (weird voice artifacts start appearing for such short sentences).... And why not send the whole character line at once?... For starters, some TTS engines have limits in how many tokens it can synthesize at once, and second, it also lead to too long pauses between sentences, although in this case, because the whole text of the round is already present, it may not be a factor, if we do as upstream does and start sending the next TTS line while the current one is still being played in the browser. Do you concur, or am I missing something?
> 3. The loop and the clock. Yes, as designed (but document Prefetch and maybe even add it as follow up as a potential improvement later? )
> 4. The listener's turn. You lean is ok.
> 5. What the page shows...Let's dig in this one a bit more together.
> 6. Failures (a round error, a dropped tunnel). I like "stop and say so, with a Resume button". 
> 7. Tests. You lean is ok.
> 8. The steps, cut again after 1-7. We need to discuss this with calm.

### 5.2 The rulings

- **Adopted with the agent's picks:** item 1 (the files), item 3 (the
  loop and the clock: the next round on drain — prefetch documented in
  §3 and recorded as the follow-up "Prefetch the next round" in
  `docs/follow-ups.md`), item 4 (the listener's turn), item 6
  (failures: stop and say so, with a Resume button), item 7 (Node
  tests for the pure pieces; the page by hand and by ear).
- **Item 2: the accumulator, not optional** — the owner restated the
  ruling of 2026-09-22; it takes each line whole, from the line's
  `done` event (§5.3).
- **Open, to be discussed one at a time:** item 5 (what the page
  shows) and item 8 (the steps).

### 5.3 Item 2 — the accumulator, as ruled on 2026-09-22 (the agent's answer, condensed)

- **The agent's pick re-opened a settled decision without citing it.**
  The accumulator was confirmed on 2026-09-22 ([discussion 2026-09-21]
  task6-recon-talkwithme, the ruling on Q9 and Q4): N = 100
  characters, a packing limit, never a truncation; a remainder under
  ~30 characters may ride along up to N plus ~20 % (built for
  "Over."); a single sentence longer than N goes whole and alone; the
  line end is a hard flush, since the next line is another voice.
- **The owner's reasons hold, with one precision.** One request per
  line would send "Testing. 1. 2. 3. Done." as one request; five
  requests is what upstream's per-sentence split does. The case
  against one request per line is the long line: nothing plays until
  a whole chunk is synthesized (no engine streams its audio —
  [discussion 2026-09-21] task6-recon-tts-serve, F4), so the wait
  before a chunk grows with its length, about r × N / 15 seconds at a
  real-time factor r (same document); and some engines bound the text
  length — tts-serve sets no bound (F2), but engines of Task 5b may.
- **The seams inside a round:** with chunk k+1 fetched while chunk k
  plays, they stay short as long as the voice synthesizes faster than
  it plays (r < 1) — not measured yet (the follow-up "Measure TTS
  synthesis time against text length").
- **Where the accumulator takes its text (settled 2026-09-25).** The
  page hands it each line whole — the full spoken text that the line's
  `done` event carries — and gets the line's chunks back: a plain
  function, no stream. Upstream's `accumulateForTTS` is fed instead
  each `token` piece as it arrives (a chat reply is long and slow to
  write), and the 2026-09-22 ruling described the fork's accumulator
  that way, inside upstream's `static/tts.js`. With the show's own
  files the whole line is simpler; it costs at most a few tenths of a
  second on a round's first line (a round is written in ~1.1-1.9 s,
  faster than it can be voiced); and item 7's Node tests can pin the
  function (resolving the follow-up "JavaScript test for the
  accumulator's packing rules"). The agent's first wording of this
  point confused the owner; the owner put it plainly (verbatim): "Yes,
  we have the whole line for the accumulator, its a simple javascript
  function, no streams involved". The event's name, `done`, has
  nothing to do with the word "Done." in the owner's example, which
  the owner later corrected (verbatim): "I actually should have said
  "Testing. 1. 2. 3. Over"."

  **The agreement, confirmed by the owner (verbatim):**

  > Ok, I get it now "Your way: wait for the done event, which carries the whole line, and pass that text to a plain function that returns the chunks. No stream." Perfect. Please record this agreement in our discussion docs.

## 6. Item 5 — what the page shows (2026-09-25)

### 6.1 The agent's proposal (verbatim)

A sketch to react to:

```
┌───────────────────────────────────────────────────────────┐
│ The Lab at the End of the Frequency              ● ON AIR  │
│ Daniel   Moira   [Ralph]   Samantha                        │
├───────────────────────────────────────────────────────────┤
│ Moira (doubtful): Could this be... a distraction? Over.    │
│ Samantha (doubtful): It's either a trap or a fluke. Over.  │
│ ▶ Ralph (terrified): We've counted four shamblers. Over.   │
│   round 7 · free · event: A pipe bursts… · tone: wry       │ ← debug only
├───────────────────────────────────────────────────────────┤
│ [ Stop ]           Listening… 7 s          [ HOLD TO TALK ] │
└───────────────────────────────────────────────────────────┘
```

**Who the page is for first:** us, testing by ear now; the talk's projector later. The debug switch separates the two.

1. **Controls:** Start, Stop, Resume. Start opens a run, and the click also unlocks audio: browsers refuse to play sound before a user gesture.
2. **The state:** on air, thinking, listening (with the window's countdown), recording (with the press cap's countdown), stopped, or error.
3. **The talk button:** hold it with the mouse, a touch or the space bar. It's enabled only while listening.
4. **The lines:** speaker, mood and text. Each line appears when its voice starts, not when it's written; otherwise the text would run a whole round ahead of the sound. The line being voiced is marked.
5. **The cast strip:** the four names, with the speaker lit.
6. **Debug only:** a line per round (kind, allowed speakers, event, tone, trims, dropped lines, timings), plus "Heard: …" with its verdict.
7. **The look:** plain and readable. The 1930s look and the gauge stay polish.

**Where I'm least sure, and would like your view:**
- **Q1. Captions:** always on, a toggle, or debug only? It's an audio play, so text on a projector might compete with the voices. But it also helps a room follow along.
- **Q2. Events:** they're the director's notes, which the listener never hears. Should they appear anywhere outside debug?
- **Q3. A page reload:** start a new run, or pick up the same one, with the run id in the URL?

### 6.2 The owner's reply (verbatim)

> Reacting to "Item 5: what the page shows":
>
> This is a very good proposal. I love it. Accepted.
>
> You questions:
>
> (Q1)  Captions: always on, a toggle, or debug only? A/ I think a toggle, with a small button somewhere small in the UI is not hard to implement.  It could be just under your "ON AIR" sign (nice touch btw). But if you think it complicates things, we can leave it as a polish later. You call.
>
> (Q2) Events: A/ Given that you proposed the page layout. What's your lean here?
>
> (Q3) A page reload: start a new run, or pick up the same one, with the run id in the URL. .. A/ Humm. This maybe require some more discussion. I feel the simplest way is "start a new run", but probably we want to continue the same one... How complex it is to do each of these options? Do you have a lean?

### 6.3 The agent's answers (condensed)

- **Q1, captions — a toggle, in slice 3 (the agent's call, as the
  owner asked).** Small: a button under the ON AIR sign that hides or
  shows the lines (one CSS class), on by default, remembered by the
  browser. The lines keep being added while hidden, so switching back
  on shows the whole story so far.
- **Q2, events — lean: shown with the captions, as stage
  directions.** Closed captions do this for sounds ("[helicopter
  passing]"); without the events, a reader of the captions sees the
  characters react to nothing. One italic line in brackets before the
  round's first line, appearing when that line's voice starts, hidden
  with the captions. The tone word stays debug-only: a note on how to
  perform, not something that happens in the story. Against: a purist
  radio listener hears only voices — hence tied to the captions
  toggle.
- **Q3, a reload — lean: a new run in slice 3; the same run as a
  follow-up.**
  - *A new run* costs nothing: the page keeps the run id in memory; a
    reload forgets it; Start opens a new run; the old record stays on
    disk.
  - *The same run* costs a small server addition and page wiring
    (about an hour with tests, estimated): the run id kept in the URL
    (`/show?run=...`); a read route (for example
    `GET /api/show/run/<id>`) to give back what the page loses — the
    played seconds so far (restarted at 0, the cadence would count the
    time since the last invitation as negative, and no invitation
    would come for minutes) and whether the last round was an
    invitation (then the listening window opens first). Two gaps it
    cannot close: the last round's own audio length is never recorded
    (the page reports played seconds with the next request), so the
    resumed clock is an estimate; and a round whose text arrived but
    whose audio never played is skipped.
  - Item 6's Resume (after an error, on the same page) needs none of
    this: the page still holds the run id and the played seconds.
  - Why the lean: a reload while testing is cheap to restart; at the
    talk an improvised show can start over, and the canned episode
    (Task 7) is the emergency mode. The run id goes in the debug line,
    so any run's record can be found.

### 6.4 The rulings

- **Item 5 adopted** as proposed (§6.1).
- **Q1:** captions behind a small toggle under the ON AIR sign, built
  in slice 3.
- **Q2, events:** shown with the captions, as stage directions (the
  agent's lean, adopted); the tone word debug-only.
- **Q3, a page reload:** starts a new run (the agent's lean, adopted);
  resuming the same run is the follow-up "Resume the same run after a
  page reload" in `docs/follow-ups.md`; the run id shows in the debug
  line.
- The owner (verbatim), answering "On Q2 and Q3, do my leans
  stand?": "Q2 and Q3, my leans stand."

## 7. Item 8 — the steps (2026-09-25)

### 7.1 The agent's proposal (verbatim)

The branch is `alfre2v/show-slice-3-browser`, cut from the fork's `master` (`5b2485f`) on your Go. There are five steps. Each one ends by hand (by ear from 3.2 on), with the suite passing, your review and your commit order.

**3.1 The page, text only.** This is the frame everything else hangs on.
- **Server:**
  - `GET /show` in the show router, serving `templates/show.html`. It gets its own `Jinja2Templates`, like upstream's in `app/main.py:149`.
  - The start response gains `listen_window_s`, `press_cap_s` and `debug`.
  - Tests, and the AGENTS.md rows.
- **Page:**
  - the sketch's layout (`show.html`, `show.css`);
  - `sse.js`, the stream reader copied from `chat.js:135-159`;
  - `show.js`, with the states and the loop.
- **The clock is simulated, since there's no voice yet.** After each round, the page waits as long as the round's text would take to say, at about 15 characters per second (the speech rate the TTS recon used), and sends that as the played seconds. The loop then paces like a show, and invitations come on the cadence. The round after an invitation goes static, since there's no microphone yet.
- **Included:**
  - Start, Stop and Resume, and the state line;
  - the cast strip, with the speaker lit;
  - the captions and their remembered toggle, with events as stage directions;
  - the debug line per round (kind, speakers, event, tone, trims, dropped lines, timings, run id);
  - failures: stop, say so, offer Resume.
- **Node tests:** the stream reader (including lines split across network chunks) and the simulated clock.
- **Done when (by hand):**
  - rounds play with lines appearing;
  - invitations and static rounds come on the cadence;
  - the toggle hides and shows lines and events;
  - Stop and Resume continue the same run;
  - a dropped tunnel shows the error, and Resume recovers.
- About 2.5–3 h (estimate).

**3.2 The voice.**
- **`chunks(line)`,** the accumulator as a plain function, following the 2026-09-22 rules. Node tests pin them, including "Testing. 1. 2. 3. Over." going as one chunk and a 180-character sentence going whole and alone.
- **`player.js`:**
  - fetch chunks in order, the next one while the current one plays, then play them in order;
  - count the played seconds from each decoded clip's duration;
  - copied from upstream's `tts.js`, minus the chat's audio upload.
- **The loop on drain:**
  - the next round is requested when the audio empties, with the real played seconds replacing the simulated ones;
  - a line's caption appears when its first chunk starts playing;
  - the speaker is lit while their voice plays.
- **Done when (by ear):**
  - lines play in order, with short sentences packed and none split;
  - the next round follows the drain;
  - the played seconds match the audio (logged).
- About 2–2.5 h.

**3.3 The listener's turn.**
- **`mic.js`:** hold to talk with the mouse, a touch or the space bar, recording code copied from upstream's `stt.js`.
  - The window's countdown stops on a press, and the press cap ends a long hold.
  - The recording is uploaded to `/api/show/listen`, and the result rides the next round.
  - "Heard: …" with its verdict appears in the debug line.
- **Done when (by hand):**
  - the button works only while listening;
  - a spoken question gets its answer;
  - silence gives the static round;
  - the cap ends a long press.
- About 2 h.

**3.4 The exit criterion, by ear.** This is the TODO's 3.5 as written: on the box, through the tunnel, at least ten unattended turns with the four placeholder personas.
- The director chooses the speakers.
- There's one interaction beat, where the microphone opens and the reply gets answered.
- Sentences are packed, not split.
- You listen, and the verdict goes into the TODO. About 30–60 min.

**3.5 Close the timebox.** This is the TODO's 3.6 as written:
- slice 3's pull request merged;
- the `tz-0.2` tag;
- the installer's `client_version` bumped, then re-proven with your deploy: a fresh install, a re-run with `changed=0`, and HTTP 200;
- the spec's as-built entries.
- About 1 h.

**Total:** about 8–9.5 h (estimates), against Monday.

**Not in slice 3:**
- **the polish list:** static in the gaps, the 1930s look and the gauge, prefetch, episodes;
- **the follow-up:** resuming the same run after a reload.

**Three questions, with my picks:**
- **Qa. The clock in 3.1:** simulated (characters ÷ 15 per second), or a "Next round" button? Pick: **simulated.** The page behaves like the show from day one, and 3.2 only swaps where the clock gets its number.
- **Qb. The scripts:** classic scripts sharing globals, like upstream's (loaded in order by `index.html:456-468`), or ES modules? Pick: **classic scripts.**
  - Upstream's Node test technique already works with them: `tests/test_tts_settings.js` loads files into a `vm` context.
  - Copied code fits without changes.
- **Qc. The three new start-response fields:** in 3.1 or 3.3? Pick: **3.1.** The debug line needs `debug` from the start, and adding all three at once means touching the route once.

Once item 8 is agreed, I'll rewrite the TODO's slice 3 checklist to match. The docs then wait for your commit order into #11.

### 7.2 The owner's reply (verbatim)

> Go with your picks on Qa, Qb, Qc

### 7.3 The rulings

- **The five steps adopted as proposed** (§7.1): 3.1 the page, text
  only, on a simulated clock; 3.2 the voice (the accumulator as a
  plain function, the player, the loop on drain); 3.3 the listener's
  turn; 3.4 the exit criterion by ear; 3.5 closing the timebox. The
  owner answered the three questions and raised no objection to the
  steps.
- **Qa:** 3.1's clock is simulated — the round's characters ÷ 15 per
  second, waited for real and sent as the played seconds.
- **Qb:** classic scripts sharing globals, as upstream's, tested in
  Node with upstream's `vm` technique (`tests/test_tts_settings.js`).
- **Qc:** the start response's three new fields (`listen_window_s`,
  `press_cap_s`, `debug`) land in 3.1.
- **The plan is complete:** `docs/TODO.md`'s slice 3 checklist is
  rewritten to it (2026-09-25). Each step still opens with its build
  shape in chat (files, functions, tests) before the code.

## 8. Addendum 2026-09-25 — the sentence splitter: a defect found in step 3.2

### 8.1 The owner's questions (verbatim)

> I notice your accumulator regex does not separate sentences by `...`, this does not necessarily need a fix. Was this intentional?  What happens to repeated punctuations in general. How would you parse sentences like "What??? They are here!!! ... Let's go"?
>
>  And what about non-ascii equivalent of punctuation marks? (I actually do not use them, but given that LLM seem to love non-ascii, I wonder if there is something there).

### 8.2 What the splitter did (the agent's probe, condensed)

The agent ran the real functions — `sentencesOf` and `chunks` in the
fork's `static/show/player.js`, then still with upstream's regex
`/[^.!?]*[.!?]+/g` — on the owner's examples and a few more:

| Text | Sentences | Chunks (what the voice gets) |
|---|---|---|
| `Could this be... a distraction? Over.` | `Could this be...` · `a distraction?` · `Over.` | the text, whole |
| `What??? They are here!!! ... Let's go` | `What???` · `They are here!!!` · `...` · `Let's go` | the text, whole |
| `Wait?! No!? Over.` | `Wait?!` · `No!?` · `Over.` | the text, whole |
| `Really‽ Over.` | one sentence: `‽` is not a mark to the regex | the text, whole |
| `Take 3.5 milligrams. Over.` | `Take 3.` · `5 milligrams.` · `Over.` | **`Take 3. 5 milligrams. Over.`** |

- **`...` does end a sentence:** the regex takes a run of marks
  (`???`, `!!!`, `?!`, `...`) as one end, and the packing joins the
  short pieces back, so it did not show. A free-standing `...` becomes
  a sentence of its own and rides along with its neighbour.
- **Non-ASCII marks mostly never reach the page:** the parser's spoken
  text maps `…` to `...`, curly quotes to straight ones and `—` to
  `, ` (the fork's `app/show/parser.py`, `_SPOKEN`). The rarer marks
  (`‽`, `‼`) are not sentence ends to the regex; that only changes the
  packing, never cuts text. How an engine pronounces them is the
  per-engine question of the follow-up "Markdown emphasis in spoken
  lines".
- **The defect:** the regex also cuts inside numbers and abbreviations
  whose dot is followed directly by a character, and the packing
  rejoins the pieces with a space: the voice received "3. 5" for
  "3.5" (and would have received "e. g." for "e.g.").

### 8.3 The fix, folded into step 3.2 at the owner's word

- A sentence ends only where a run of `.`, `!`, `?` or `…` meets
  whitespace or the end of the line (`/[.!?…]+(?=\s|$)/g`), and the
  text between the cuts is kept as written: "Take 3.5 milligrams." and
  "Over."; `e.g.` and `U.S.` are not cut inside; "Dr. Byrne." still
  splits at the space and packs back as written. Our show splits whole
  lines (the text of each line's `done` event), so the end of the line
  is a true end.
- Two Node tests pin it: the sentence ends, and the chunks reproducing
  the text as written for `3.5`, `e.g.` / `U.S.` and the owner's
  example.

### 8.4 The owner's conclusion (verbatim)

> Yes, fold the fix into 3.2.
> Notice also that in your example "Could this be... a distraction? Over." Although the regex was doing its intended work, in this specific case for sending to a TTS engine, it would have been better not to split at the `...` because that degrades the pronunciation of the sentences. I think this defends our case for the accumulator, and keeping the 100 split decision. Trying to fix where to cut sentences with different punctuations so that TTS pronunciation is better is too complicated. In practice I feel the accumulator is the practical best solution.

It also settles the owner's "Over." observation of the same day (the
follow-up "The sign-off 'Over.' sometimes runs into the line"): the
accumulator stays at 100 characters.

### 8.5 Upstream has the same defect — a candidate bugfix

- **Upstream's `extractSentences`** (TalkWithMe `static/tts.js`, lines
  72-83, the same regex), run as is: "Take 3.5 milligrams every day.
  Over." gives `Take 3.` · `5 milligrams every day.` · `Over.` —
  whether the text comes whole or token by token — and upstream sends
  each sentence as its own TTS request, so the number is split across
  two requests.
- **The fix needs one change for upstream's streaming mode:** there
  the sentences are cut from a growing buffer, and the buffer ends at
  "Take 3." just before the "5" arrives, so the end of the buffer must
  not count as a sentence end while streaming (`(?=\s)`); the tail is
  flushed on `done`, as upstream already does. Simulated with
  upstream's loop: with `(?=\s|$)` the result is still `Take 3.` ·
  `5 milligrams every day.` · `Over.`; with `(?=\s)` and the flush,
  `Take 3.5 milligrams every day.` · `Over.`.
- **Recorded as candidate (5)** of the follow-up "Upstream
  contributions to scorbo2", to be offered after the deadline as a
  small bugfix pull request of its own.

## Update trail

- **2026-09-25** — Document created on the owner's request, recorded
  in slice 2's open pull request ("I know, not ideal, but it's only
  you and me here... I won't tell anyone"): the rejected plan and the
  owner's three rulings (§1), the gap between rounds and what `done`
  means (§2), prefetch documented (§3), the agenda proposed (§4).
- **2026-09-25 (later)** — §2.4 added: how the events reach the page.
  §5 added: the agenda's first pass — items 1, 3, 4, 6 and 7 adopted,
  the accumulator restated (item 2), items 5 and 8 open.
- **2026-09-25 (later still)** — §5.3's last point reworded after it
  confused the owner: the accumulator takes each line whole, a plain
  function (the owner's words, and the corrected example); the
  owner's confirmation of the agreement added, verbatim.
- **2026-09-25 (evening)** — §6 added: item 5, what the page shows —
  adopted; captions behind a toggle; events with the captions; a
  reload starts a new run (the same-run resume a follow-up).
- **2026-09-25 (evening, later)** — §7 added: item 8, the steps —
  five steps adopted, with the agent's picks on the simulated clock,
  classic scripts, and the start response's new fields in 3.1. The
  agenda is complete; status DECIDED; the TODO's slice 3 checklist
  rewritten to it.
- **2026-09-25 (night)** — §8 added, a dated addendum: the sentence
  splitter's defect found during step 3.2 ("3.5" reached the voice as
  "3. 5"), the owner's questions and conclusion verbatim, the fix, and
  the same defect in upstream — a candidate bugfix.
