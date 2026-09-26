# Session handoff 4 — the show engine's slice 3: built through 3.4b; the listener's exchange (3.4c?) and the close next

> **EPHEMERAL.** Written 2026-09-25 ~18:10 CDT and refreshed
> 2026-09-26 ~00:05 CDT (after the events A/B, 3.4 and 3.4b), before the owner's
> evening break, as a compaction-survival dump: if the context is
> compacted, the agent re-reads this first. It replaces handoff 3
> (`2026-09-24-show-engine-session-handoff-3.md`, which covered only
> the work up to step 2.5), deleted with the owner's permission in the
> same commit. When the session that uses this one concludes, the
> agent asks the owner for permission to delete it.
>
> **Read it all; verify against the repos; receipts or nothing.** The
> TODO's "Now" section is the canonical state; this document carries
> what the TODO cannot: how we work (and what changed today), the code
> of slice 3 as built, the numbers measured today, today's rulings,
> the board ahead with the pending shapes, the nuances, the mistakes
> not to repeat, and the working techniques (live checks in the
> browser pane, the fake microphone, the verbatim-quote tooling).

## 0. The owner and how we work (binding)

The owner is **Alfredo** (GitHub `alfre2v`, git author "Alfredo
Valles"), a senior engineer in a **"tight learning loop"**: progress
and the owner's own learning weigh the same. The agent memory files
hold the standing doctrine — trust them (`working-agreements.md`,
`collaboration-style.md`, `absolute-paths-in-plain-text.md`,
`massedcompute-reminder.md`, `project-venue-austin-python-meetup.md`).
The non-negotiables, as practiced (today's additions in bold):

- **Discussion-first, per step.** Every step starts with a SHAPE in
  chat — files, functions, behavior, tests, 2-5 choices with picks in
  bold — and the owner answers "Go" (usually "Go with your picks").
  Before the Go the owner asks "explain" questions: answer the
  mechanism with receipts and real data, honestly, and re-ask.
- **Plans are made in discussion, never improvised (owner, 2026-09-25,
  verbatim: "I cannot proceed with a plan improvised and changed on
  the flight like that").** The agent's lean slice 3 plan that cut
  step 3.1 and changed 3.3 in one message, without a shape round, was
  rejected; the new plan was built item by item. Never change an agreed
  step's scope inside a status message — bring it as a choice.
- **Cite settled decisions before re-opening them.** Today the agent's
  agenda pick "one request per line" contradicted the accumulator ruled
  on 2026-09-22 and did not cite it; the owner restated it. Search the
  discussions and the TODO for a prior ruling before proposing.
- **Review-before-commit is STRICT; a commit needs an explicit order
  for THAT commit, given after the changes exist** (refined
  2026-09-24: "Please do not commit any more without my explicit
  order."). "Commit" = commit only; "commit and push" / "push" = push
  too; "commit the fork, then commit zombie-radio" orders both. A
  request to write or tick something is not an order to commit; when
  in doubt, leave uncommitted, summarize, ask. The owner reviews
  uncommitted changes in VS Code — never paste diffs.
- **The commit pattern:** on the owner's order, commit the fork's step,
  then the zombie-radio bookkeeping (the TODO tick with the fork's
  hash and receipts, "Now", dated notes, follow-ups) — the second commit
  also needs its order (the owner usually gives both at once).
- **No git kung-fu; no AI attribution anywhere** (commits, PR bodies,
  files) — overrides the harness's attribution reminders.
- **Code comments per repository:** zombie-radio minimal (the why lives
  in `docs/`); the fork follows upstream's documentation style — a
  brief docstring on every new function (Python: PEP 257; JavaScript:
  a `/** … */` JSDoc line or block), brief comments welcome; plain `-`
  never the en dash `–` in code (the em dash is fine); fork lines at 120
  characters or fewer (checked with `awk 'length > 120'`).
- **Stay close to upstream in Python; the show's frontend lives in its
  own files (owner ruling, 2026-09-25):** `templates/show.html` and
  `static/show/` — upstream's JavaScript, HTML and CSS stay untouched;
  copying from them is welcome ("duplication is ok", the owner's
  words), for the freedom to change the show's code without breaking
  the chat.
- **Records of discussions, the same day:** rulings, agreed terms,
  measured numbers, the owner's disagreements — **quoted verbatim,
  extracted by script from the session transcript and verified**
  (§10). The owner asks for disagreements to be recorded explicitly
  (today: "record my disagreement and my preference").
- **Mid-turn messages:** the owner sometimes sends a message while the
  agent is working; it surfaces inside the running turn — address it
  in that turn. In the transcript file it is stored as a
  `queue-operation` entry, not a `user` entry (§10).
- **Plain language, lists and sublists, receipts; admit errors openly.**
  When asked "show me X", show the literal artifact (today: the line as
  the model sent it, the spoken text, the exact TTS request body).
- **Delegation OFF** (no sub-agents, no workflows).
- **Git:** feature branches and PRs only; one branch per slice, cut
  from the fork's up-to-date `master` / zombie-radio's `main`; fork PRs
  always `--repo alfre2v/TalkWithZombies --base master`; the owner
  merges. Push only when told; PRs only when asked.
- **"Forget about the time constraint"** — don't ration by the clock,
  but mention it when planning. The timebox's end moved to **Monday
  2026-09-28** (owner, 2026-09-25: "do not push back on this one").
- **Pronouns:** avoid pronouns for the owner in new writing.

### 0.1 Live-box drill rules

1. **The OWNER owns the SSH tunnel, the box's power and deploys.** The
   agent reaches the services only through `localhost:8080` (llama.cpp),
   `:8001` (tts-serve), `:8002` (Whisper).
2. **Box inspection: plain `ssh ubuntu@<box> '<cmd>'`** — no flags; the
   address is the one the owner gives in chat; never write it into a
   file; never list or cat under the owner's SSH directory.
3. **One line saying what a command does, BEFORE running it.**
4. **Probe the tunnel before any chain of requests, and wait for the
   answer:** `for u in localhost:8080/health localhost:8001/capabilities
   localhost:8002/docs; do printf '%s ' "$u"; curl -s -m 3 -o /dev/null
   -w '%{http_code}\n' "$u"; done`. On anything but 200 (`000` / exit
   7 = nothing listening) STOP and tell the owner. Today the tunnel was
   found down three times; the owner restarts it.
5. **The tunnel now sends keepalives** (the Makefile's `ssh-tunnel`:
   `-o ServerAliveInterval=30 -o ServerAliveCountMax=3`, zombie-radio
   `bfe88d5`): an idle tunnel keeps talking, and a dead link makes ssh
   exit within ~90 s (it may print "Timeout, server not responding").
   **A closed laptop lid still kills it** — expected, not the case the
   fix targets (the owner: "This is an expected failure, as opposed to
   the tunnel failing when the ssh session (tmux driven) does not").
6. **No box address in any markdown, ever.** Addresses live only in
   `deploy/ansible/inventories/cloud/hosts.yml` (`NEVER_COMMIT`, never
   staged — it is modified/wired now). Pre-commit scan in §10.
7. **Nothing changes on the box outside the playbook.**
8. **Temporary dev settings** in the fork's gitignored `settings.yaml`
   (e.g. `debug: true`; `interaction_min_s: 20` / `interaction_max_s:
   40` to bring invitations forward): check it equals the backup first
   (`cmp settings.yaml <scratchpad>/settings.yaml.before-trim` — the
   committed state of the dev file: `show:` has only `seed: 42`), append
   the temporary lines, and restore with `cp` + `cmp` after. Say so.
9. **The dev server:** from the fork's root, in the background:
   `exec .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8010 >
   <scratchpad>/dev-server-8010-<name>.log 2>&1`; wait with `curl -s -o
   /dev/null -w '%{http_code}\n' --retry 20 --retry-connrefused
   --retry-delay 1 http://127.0.0.1:8010/show`; stop with `kill $(lsof
   -nP -iTCP:8010 -sTCP:LISTEN -t)` and re-check the port (a second
   later). The background task then reports "exit code 144" — expected.

## 1. The project in 60 seconds

**Zombie-Radio**: an interactive, audio-only radio play — four AI
scientists (Daniel, Moira, Ralph, Samantha — Samantha is the operator)
trapped in a lab during a zombie outbreak, broadcasting on shortwave;
listeners talk back with hold-to-talk. Hard deadline **2026-10-08**; a
talk at the **Austin Python Meetup** in October 2026 ("hackTNT 2026" is
the owner's internal label, not a hackathon). The imitated style: Orson
Welles's *The War of the Worlds* (1938) — the ambiguity between a radio
play and a real emergency broadcast.

The app is **TalkWithZombies**
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`), the owner's
fork of scorbo2's TalkWithMe 7.1 (upstream checkout:
`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe`). Its **show engine**
is TODO Task 6b, designed in
`docs/discussions/2026-09-23-show-engine-design.md` ("SED"): one shared
script as the model's context, a director in code, a GBNF screenplay
grammar per request, the browser as the clock. Slice 1 (the skeleton)
and slice 2 (the rules, the checkpoint passed 2026-09-24, verdict
continue) are merged. **Slice 3 — the browser — is planned in
`docs/discussions/2026-09-25-show-slice-3-browser-plan.md` (DECIDED)
and 3 of its 5 steps are done.** The services run on a rented
Hyperstack A6000 ("the box"): llama.cpp (Nemotron Nano 9B v2, build
`b11096`), tts-serve 1.2 (Faster Qwen3-TTS), Whisper (whisper-fastapi
`small`).

## 2. Exact state (2026-09-26, ~00:05 CDT, Saturday)

- **The timebox (Task 6b):** started 2026-09-23 14:46; checkpoint
  passed 2026-09-24; **end Monday 2026-09-28** (moved by the owner).
- **Slice 3: 3.1, 3.2, 3.3, 3.4 (met by ear) and 3.4b done;** the
  events A/B decided (events worded for the broadcast). **Next: the
  owner decides whether the listener's exchange becomes step 3.4c**
  (§7.1), then 3.5 (close).
- **The fork:** branch **`alfre2v/show-slice-3-browser`**, cut from
  `master` `5b2485f` (slice 2's merge, PR #3). Commits, all pushed:

  | Hash | When | What |
  |---|---|---|
  | `8bca58b` | 15:55 | 3.1 the page, text only, on a simulated clock (+ fixes a, b) |
  | `a2d942e` | 16:53 | 3.2 the voice (+ the sentence-splitter fix) |
  | `57dce7f` | 18:00 | 3.3 the listener's turn |
  | `c55d25b` | ~22:40 | events worded for the broadcast (`show.event_report`, on by default) |
  | `500debe` | ~23:55 | 3.4b the listener's words in the captions, per-word confidence |

  Suite **1011 passed**; Node tests `test_persona_form.js` 17,
  `test_tts_settings.js` 91, **`test_show_page.js` 31**. Working tree
  clean.
- **zombie-radio:** branch **`alfre2v/show-slice-3`**, cut from `main`
  `b9e4d18` (slice 2's merge, PR #11, which also carried slice 3's plan
  discussion). Commits: `bfe88d5` (3.1 tick, tunnel keepalives, the
  events follow-up), `fbd1c46` (3.2 tick, the splitter addendum §8,
  follow-ups), `e3fe622` (follow-ups: talk anytime, the em dash),
  `be9bdb4` (3.3 tick; the real button folded into 3.4), then `5664d96` (this handoff,
  the TODO's corrected quote, handoff 3 deleted), `1e45611` (the A/B's
  records), `d8790aa` (3.4 met, 3.4b ticked, the exchange follow-up)
  — all pushed; this refresh of the handoff is uncommitted until the
  owner orders it. `hosts.yml` modified (wired) — never stage.
- **Slice 2 PRs merged** (fork #3 → `5b2485f`; zombie-radio #11 →
  `b9e4d18`). No slice 3 PRs yet.
- **The box: UP**, and the owner keeps it running overnight ("I'll even
  keep the VM running so we can go back in business when I'm back").
  `hosts.yml` wired. **The tunnel is probably down** after the owner's
  break (a closed lid ends it) — probe first; ask the owner to restart
  it.
- **The dev clone (the fork):** `settings.yaml` restored (only `seed:
  42` under `show:`); no dev server running; `runs/` holds today's
  records: `2026-09-25T14-55-49` (offline smoke, junk), `T14-57-06`
  (3.1 live: 53+ rounds, invitations 15/32/53, the double Stop at round
  44, the owner's tunnel drop at round 53), `T15-48-26` (3.1 fix a live:
  stops between lines at rounds 1-3, the kept round 16), `T16-04-56`
  (3.2 by ear: 42 rounds, 245 s of audio), `T22-34-16` / `T22-35-07`
  (the A/B's drives A and B), `T23-00-20` (3.4 by ear, the owner's voice),
  `T23-40-48` (3.4b fake microphone), `T23-43-42` (the owner's 3.4b
  check), `T17-50-50` (3.3 fake
  microphone: invitation 4 → answer 5, invitation 11 → static 12).
- **The browser pane** (the agent's built-in browser; the owner sees
  the same pane) has `http://127.0.0.1:8010/show` open, with the fake
  microphone installed in that page — reload before any real use.
- **Scratchpad**
  (`/private/tmp/claude-501/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18/scratchpad/`,
  temporary): `settings.yaml.before-trim` (the dev settings backup),
  `build_slice3_doc.py` + `slice3_body.md` + `slice3_msgs.json` (the
  slice 3 discussion doc's generator — §10), `today_msgs.py` (finds
  messages in the transcript), `sentences.js` / `upstream_split.js` /
  `stream_fix.js` (the splitter probes), `invitations.py` (the cadence
  simulator), `listen_loop.py` (2.4's loop), dev-server logs, drive
  outputs, PR bodies. The session transcript:
  `/Users/alfredo/.claude/projects/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18.jsonl`.

## 3. What this session did (2026-09-25)

1. **12:39 — pickup** (handoff 3 re-orientation happened the night
   before). The agent proposed a lean slice 3 plan (skip 3.1's
   extraction, one TTS request per line instead of 3.3's accumulator,
   "dead air 3-4 s"); **rejected** by the owner, who moved the timebox
   to Monday, ruled the frontend into its own files, and asked why the
   gap between rounds.
2. **The gap and `done` explained** — `done` marks one line (not the
   round); the round ends with `round` + `complete`; how events reach
   the page (two SSE hops; `LineParser.feed` returns a list per piece,
   no queue needed). Prefetch documented.
3. **The slice 3 plan, item by item** (the doc
   `2026-09-25-show-slice-3-browser-plan.md`, §1-§7): the eight-item
   agenda; the accumulator restated (fed each whole line from its
   `done` event — a plain function); what the page shows (the sketch,
   captions toggle, events as stage directions, a reload = a new run);
   the five steps with a simulated clock for 3.1. Status DECIDED; the
   TODO's slice 3 rewritten; PR #11 carried it; merged.
4. **3.1 the page, text only** — built (~1 h 05 from Go to commit),
   smoke-tested offline, then live: cadence, window, Stop/Resume, a
   real tunnel drop recovered by Resume. **Two fixes from the live
   check**: (a) a Stop landing after the server recorded the round is
   now reported ("stopped, but the server kept this round"); (b) a
   kept round's debug files survive the client leaving
   (`asyncio.shield`). The stray Stop at round 44 — the owner "may have
   pushed the stop button", verbatim "LEt's keep an eye on this".
5. **Two side quests recorded:** "Events the listener cannot hear" (the
   owner's evidence pasted from the page; four options; the agent's
   lean: reporting on air by the wording; an A/B test); the tunnel
   keepalive (the owner: "this tunnel thing is too annoying already")
   — fix (1) applied in the Makefile.
6. **3.2 the voice** (~53 min) — player.js with `chunks()`, the queue,
   the drain; live by ear: **"I cannot find any problem. Well executed!
   We can call this a success."** Measurements of synthesis time. The
   "Over." observation (keep 100). **The splitter defect** found by the
   owner's questions ("3.5" → "3. 5"), fixed, documented as the plan
   doc's §8 addendum and as upstream candidate (5).
7. **Progress review** (the owner asked "where do you see us"); the
   arc estimate (§7.4).
8. **3.3 the listener's turn** — the window discussion (kept; talk
   anytime recorded as polish, with the owner's disagreement and
   correction verbatim); built; checked live with a **fake
   microphone**; the em dash line researched and recorded; committed;
   ticked with the real-button check folded into 3.4.
9. **The events A/B shape** proposed; deferred to the evening ("this
   A/B test looks like needs a quiet place" — the agent noted it is
   reading only; 3.4 is the step that needs quiet).

10. **Evening: the events A/B test** (after the owner's Go): the knob
    `show.event_report`; two 30-round drives (A "Offstage:", B the
    broadcast wording), the same 10 events; round 1 rebuilt from the
    records and shown to the owner as it went over the wire (315 / 333
    tokens, exact); the owner: "B wins, flip the default and record it."
11. **3.4 by ear** (the owner, real microphone, invitations at 20-40 s):
    met — "It does what we planed. It is a success." Two findings: the
    listener's words not in the captions (→ 3.4b); the exchange is one
    line and the story moves on (→ a follow-up; maybe 3.4c).
12. **3.4b the listener's words in the captions** — shaped (the owner
    asked to explain picks c-e), built, fake-mic check, the owner's
    check found two CSS issues (no hover tooltip; a broken wavy
    underline), fixed, committed with the owner's order.
13. **Handoff 4 refreshed** (this), context at 87 %.

## 4. Slice 3's code as built (the fork, `static/show/` + server bits)

**Server (3.1):**
- `app/routers/show.py` — `page_router` (no prefix) with `GET /show`
  serving `templates/show.html` through its own `Jinja2Templates`
  (`Path(__file__)…/templates`); included in `app/main.py` with one
  line (`app.include_router(show.page_router)`). The start response
  (`ShowStartResponse`, `app/models.py`) gains `listen_window_s`,
  `press_cap_s`, `debug`. The debug write after a recorded round is
  `await asyncio.shield(write_round(...))` (fix b).
- Tests in `tests/test_routers_show.py`: `TestPage` (the page and its
  files served, no `chat.js`), the start response's fields, and the
  cancellation test (`test_a_client_leaving_while_the_files_are_written_still_gets_them`
  — passes with the shield, fails without; proven).

**Page — classic scripts sharing globals, loaded in order by
`templates/show.html`: `sse.js`, `player.js`, `mic.js`, `show.js`;
`show.css`.** At load time the scripts only define functions and wire
the page on `DOMContentLoaded` (so Node can load them).
- **`sse.js`** — `splitSSE(buffer)` → `{events, rest}` (pure);
  `readSSE(resp, onEvent)` (copied from `chat.js:135-159`).
- **`player.js`** — `VOICE` config object (`chunkMax` 100, `tailMax`
  30, `tailTolerance` 1.2, `pauseInLineMs` 80, `pauseBetweenLinesMs`
  250 — an object so tests can change it); `voice` state;
  `sentencesOf(text)` — a sentence ends where `[.!?…]+` meets
  whitespace or the end (`/[.!?…]+(?=\s|$)/g`), the text between cuts
  kept as written; `chunks(line)` — the 2026-09-22 accumulator over a
  whole line; `unlockAudio()` (AudioContext on a click);
  `speakLine(persona, text, hooks)` (hooks: `onStart()` at the line's
  first clip, `onFail(err)` per failed chunk — skipped);
  `drained()`; `stopVoice()`; internal `synthesizeNext` (one at a time,
  back to back, independent of playback — the next chunk is fetched
  while the current plays), `synthesize` (`POST /api/tts {text,
  persona_name}`), `playNext`, `playClip`, `wakeWaiters`, `isIdle`; a
  `generation` counter drops late results after a stop.
- **`mic.js`** — `mic` state; `primeMic()` (permission at Start,
  released at once); `openMic()` / `closeMic()` (open only while the
  radio listens; closing discards a recording and counts a held button
  as released); `startRecording()` / `stopRecording()` (MediaRecorder;
  the MIME the browser chose); `talkPress()` / `talkRelease()`,
  `nextPress()` / `nextRelease()`; `blobToBase64()` (via
  `blob.arrayBuffer()` + `btoa`, not FileReader — testable in Node);
  `hear(blob, mime, runId, signal)` → `POST /api/show/listen` (an empty
  recording is heard as `""` without a request; throws on HTTP error).
- **`show.js`** — `show` state (`run`, `playedS`, `voice`,
  `current`, `lastKind`, `lastN`, `unsure`, `controller`, `state`);
  `RUNNING_STATES` (thinking, on air, listening, recording, hearing);
  `TURN.tickMs` (1000; tests shorten it). Pure helpers:
  `speakingSeconds`, `keptAttempts`, `roundBody`, `formatSeconds`,
  `debugLine`. The loop: `startShow()` (unlockAudio, primeMic, `POST
  /api/show/start`), `runShow()` (per round: the listener's turn after
  an invitation → `playRound(signal, heard)` → `playOut` (voice:
  `await drained()`) or `onAir` (`?voice=off`: the simulated clock);
  its catch: `stopVoice()`, then "stopped" or `fail()`, only if still
  the current loop), `playRound()` (lines hidden until their voice
  starts; `lineStarts` shows them and lights the speaker;
  `voiceFailed` notes with debug; the stage direction on `round`;
  `settleUnsure`), `listenerTurn()` → `waitForPress()` /
  `recordUntilRelease()` / `hear()` (a failed transcription = silence,
  noted), `canTalk()`, `stopShow()`, `resumeShow()`, `countPlayed()`,
  `sleep()`; DOM helpers (`setState` also drives the talk button:
  enabled only while listening/recording with the mic open;
  `renderCast`, `lightSpeaker`, `addRoundElement`, `addLine`,
  `addDirection`, `addDebugLine`, `addNote`, `scrollToEnd`); captions
  (`applyCaptions`, `toggleCaptions`, `savedCaptions` — localStorage
  key `show.captions`, in try/catch); `wireTalk()` (pointer events with
  capture, the space bar with key repeat ignored and `preventDefault`,
  no context menu).
- **`show.css`** — dark, plain; `.captions-off` hides `.line` and
  `.direction`; `#on-air.lit`; `#btn-talk.window-open` / `.recording`.
- **`tests/test_show_page.js`** (plain Node, upstream's `vm`
  technique; 26 tests): the splitter and reader, the simulated clock,
  the debug line, `keptAttempts`, `sentencesOf` / `chunks` (incl.
  "Testing. 1. 2. 3. Over.", a 180-character sentence, 60+60, 98 +
  "Over.", "3.5", "e.g."/"U.S.", "What??? …"), the voice queue with
  stubbed `fetch` / `AudioContext` (order, start once, played seconds,
  drain, stop, failed chunk), `roundBody`, `hear()`, and the listener's
  turn with a stub microphone / recorder / route (press+release, no
  press, the cap, a stop mid-recording, a failed transcription). The
  sandbox needs `setTimeout`, `clearTimeout`, `AbortController`,
  `atob`, `btoa`, `Blob`, `performance`, `TextDecoder`.
- **Docs:** `docs/runbooks/show-page.md` (open the page, what you see,
  the voice, `?voice=off`, talk back, the debug line, Stop/Resume/a
  reload, troubleshooting); `AGENTS.md` (the "show page" file table,
  the Node test and its run rule, the start-response row).

**Added in the evening:**
- `app/config.py` `ShowConfig.event_report: bool = True`;
  `director.instruction_for(…, report)`: with an event, `Something
  happens that the listeners cannot see: <event> The first to speak
  tells the listeners on air what is happening. <speakers …>`; `false`
  gives `Offstage: <event> …`; `_free` passes `show.event_report`.
- `app/services/stt_client.py` `transcribe_for_show` also returns
  `words: [{word, probability}]` (from `segments[].words`, trimmed);
  `app/models.py` `ShowHeardWord`, `ShowListenResponse.words` (to the
  page only). `static/show/show.js`: `WORD_BANDS` (0.8 / 0.5),
  `wordBand()`, `heardWords()`, `addHeardCaption()` (a `.line
  .listener` "You: …", word spans `word word-<band>` with
  `data-percent`), `addVerdict()`, `settleHeard(summary)` (the verdict
  when the next summary says silence), `show.heardCaption`. CSS: a
  hover tooltip from `data-percent` (`::after`), bands with
  `text-decoration-skip-ink: none`, doubtful dimmed by color (not
  opacity — the tooltip would inherit it).

## 5. Facts and numbers (measured 2026-09-25)

- **Pace today:** 3.1 estimated 2.5-3 h → ~1 h 05 (Go 14:50, commit
  15:55); 3.2 estimated 2-2.5 h → ~53 min (Go 16:00, commit 16:53);
  3.3 estimated 1.5-2 h → built and checked in well under an hour after
  the green light (commit 18:00). The morning's replanning took ~1 h
  40.
- **The page's timings:** first line 0.9-1.4 s in the browser (the
  driver saw 0.76-0.94 s on 09-24; the box had just been woken — to
  watch); a new run's round 1: first line 2.9 s, first sound 6.8 s
  (the TTS cold).
- **The voice (run `T16-04-56`, probe in the page):** 8 chunks of 27-55
  characters took **2.4-3.2 s each to synthesize** (one 4.6 s), clips
  2.0-3.6 s, ratio 0.8-1.4 — **a mostly fixed cost per request, ~2.3
  s**. Gaps between clips: 250 ms (the configured pause), **1.2-1.9 s**
  inside a round where a short line could not be ready, **3.7-4.9 s**
  between rounds once warm. The owner: "The pauses do not feel so bad
  actually." A suspect for the fixed cost (believed, not measured):
  the app sends the persona's reference clip with every request
  through the tunnel.
- **The fake-microphone check (run `T17-50-50`, invitations at 20-40
  s):** fake voice 1.92 s ("Moira, is the virus airborne?", Samantha's
  voice); heard word for word in 1.2 s (upload + Whisper); round 5,
  Moira: "I don't know. The samples were aerosolized, but, Over."
  (the em dash — §6); round 11 invitation → round 12 static ("We'll
  adapt. Over.").
- **Stops:** a Stop between lines leaves the round unrecorded ("abandoned
  by the client; nothing recorded"); a Stop during the ~0.3 s debug
  write after the last line keeps the round (seen live twice: round 44
  in `T14-57-06`, round 16 in `T15-48-26`; and once during the owner's
  listening in `T16-04-56`). Timing-based stops cannot target the last
  line (gaps between lines ≈ the debug write) — use the one-line round
  after an invitation.
- **Upstream's splitter** (`TalkWithMe/static/tts.js:72`,
  `/[^.!?]*[.!?]+/g`): "Take 3.5 milligrams every day. Over." →
  "Take 3." · "5 milligrams every day." · "Over." — two TTS requests
  for one number, whole or streamed. The fix for upstream's streaming
  mode needs `(?=\s)` (not `(?=\s|$)`) plus the flush on `done`
  (simulated).
- **Round 5's em dash:** the model wrote `Moira (doubtful): "I don’t
  know. The samples were aerosolized, but—Over."` (U+2014, `finish:
  stop`, 24 tokens of 512); the spoken text `…aerosolized, but, Over.`;
  the TTS request `{"text": "I don't know. The samples were
  aerosolized, but, Over.", "persona_name": "Moira"}`.
- **Prices:** the A6000 about $0.50/h (the 2026-09-13 survey).

- **The A/B (runs `T22-34-16` A, `T22-35-07` B):** the first line shared
  a content word with the event in 4/10 (A) vs 8/10 (B); the agent's
  reading: B clearly better in 5, somewhat in 3, equal in 2, A never;
  B's script 5 % longer (2879 vs 2740 tokens). The chat template eats
  `/no_think` (it becomes `<think></think>`); the system prompt says
  "No narration".
- **3.4 (run `T23-00-20`):** 33 rounds, 5 invitations, 3 answers
  (no_speech_prob ≤ 0.024), each ONE line ("Who's there?", "Who are
  you?", "They think we should go south."), the next round an event.
- **Whisper's words** come free in the plain json (`segments[].words`:
  word, start, end, probability); e.g. "Moira 94 · is 77 · the 99 ·
  virus 92 · airborne 98"; "Thank you." → the hallucination verdict.

## 6. Rulings today (the owner's)

- **Timebox end Monday 2026-09-28;** the show's frontend in its own
  files; plans made in discussion.
- **The agenda (plan doc §4-§7):** 1 the files (`static/show/`); 2 the
  accumulator as ruled 2026-09-22, fed each whole line from its `done`
  event ("a simple javascript function, no streams involved"); 3 the
  next round on drain, prefetch a follow-up; 4 the listener's turn; 5
  the page (the sketch; Q1 captions behind a toggle under ON AIR, built
  in slice 3; Q2 events as stage directions with the captions, the tone
  debug-only; Q3 a reload starts a new run, same-run resume a
  follow-up); 6 failures: stop and say so, Resume; 7 Node tests for the
  pure pieces; 8 the five steps; Qa 3.1 on a simulated clock; Qb classic
  scripts; Qc the start response's fields in 3.1.
- **3.1:** picks a-e (page router; the direction placed on `round`; the
  window shown in 3.1; Stop aborts; a new runbook); fixes a and b.
- **Tunnel:** fix (1) keepalives applied; (2) self-restart and (3)
  server-side remain open.
- **3.2:** picks a-e (a failed chunk skipped; `?voice=off` kept; 80 /
  250 ms pauses; "first sound" and "played" in the debug line; tests of
  `chunks` and the queue); the splitter fixed and documented (plan doc
  §8; upstream candidate 5 — a small bugfix PR of its own, after the
  deadline); **the accumulator stays at 100** — the owner: "Trying to
  fix where to cut sentences with different punctuations so that TTS
  pronunciation is better is too complicated. In practice I feel the
  accumulator is the practical best solution."
- **3.3:** the mic open only during windows, primed at Start; one press
  per window; a failed transcription = silence; "heard" as a debug
  line; the turn tested with stubs. **The listening window stays** for
  the MVP; **talk anytime** is a polish follow-up — the owner disagrees
  with the agent's two reasons for the window and prefers that a press
  interrupts the round's voices (text recorded as complete) and records
  in the silence, the next round answering (both messages verbatim in
  the follow-up). The em dash: a follow-up, no listening test now.
- **3.3 ticked** with the real button and microphone checked in 3.4's
  session.

- **Evening:** the A/B — "B wins, flip the default and record it."; 3.4
  met ("It does what we planed. It is a success."); 3.4b added at the
  owner's request, picks a label `You:`, b three bands + hover %, c
  words to the page only, d the filter's verdict on the caption, e the
  caption under the invitation; approved after the owner's live check;
  the listener's exchange: "Let's decide after 3.4b if we included as
  3.4.c."; the owner's rule for this kind of step: "Once approved we
  commit and push the branch."

## 7. The board ahead

### 7.1 NEXT: the owner decides on 3.4c — the listener's exchange

The follow-up "The listener's exchange is one line — the characters ask
back, but no window opens" holds the evidence (three runs' receipts; the
model folded the owner's name into an event) and the agent's proposed
ingredients: a richer answer (2-3 lines, the addressed character first,
an instruction to find out who and where the voice is); a follow-up
window when the characters ask back (a conversation, capped, silence
ending it); no event right after the listener's turn. Close to "Talk
anytime". If it becomes 3.4c: a SHAPE first (a director change,
decision 5), then build, then the owner by ear.

### 7.2 Then: 3.5, close the timebox (the end is Monday 2026-09-28)

Push; the slice 3 PRs (fork `alfre2v/show-slice-3-browser` → `master`,
`--repo alfre2v/TalkWithZombies --base master`; zombie-radio
`alfre2v/show-slice-3` → `main`), on the owner's ask; the owner merges;
the tag **`tz-0.2`** on the fork's `master` (on the owner's order); the
installer's pin `deploy/ansible/client-talkwithme-mac.yml:19`
`client_version: "tz-0.1"` → `"tz-0.2"`; the owner re-proves it (a fresh
install via `make client-mac`, a re-run `changed=0`, HTTP 200); the
spec's as-built entries (`docs/specs/product-definition.md` ledger).

### 7.4 After slice 3 — the arc (estimates given to the owner today)

| What | Estimate | Depends on |
|---|---|---|
| Task 4 — the real cast (bibles into `stories/lab-outbreak/cast_sheet.md`, voice samples as `ref.wav`) | ~1-2 h of wiring | **the owner's bibles and samples — the long pole** |
| D2 accepted (a real-cast session on a playbook-built stack) | ~2 h after Task 4 | Task 4 |
| Show fixes before the talk (events wording; maybe prefetch) | 2-4 h | — |
| 5a LLM audition | ½-1 day | Task 4; the owner's scoring |
| 5b TTS comparison + VRAM | 1-2 days, likely to balloon | voice samples |
| 5c probe battery | 2-3 h | the owner |
| Task 7 canned episode + demo runbook (a MUST) | ½ day | a working show |
| Task 8 close ritual | ~2 h | — |

About 5-7 working days of agent time; fits 2026-10-08 only if Task 4
arrives in the next few days. Story/episode authoring and the demo
rehearsal belong to the NEXT arc ("the show arc") — "MVP done" is not
"talk-ready". The agent recommended: close slice 3 in one more sitting,
then prioritize Task 4.

### 7.5 Follow-ups recorded today (zombie-radio `docs/follow-ups.md`)

"Prefetch the next round" (the measured gap added); "Resume the same
run after a page reload"; "Events the listener cannot hear" (the
owner's pasted evidence, four options, the A/B); the SSH keepalives
entry (dated status, priority raised, fix 1 applied); "Measure TTS
synthesis time against text length" (dated partial answer); "The
sign-off 'Over.' sometimes runs into the line" (keep 100; the owner's
view); "Talk anytime — the listener breaks in while a round plays"
(the owner's preference, disagreement and correction verbatim); "A
line broken off with an em dash sounds and reads cut"; "Upstream
contributions to scorbo2" candidate (5) — the splitter bugfix; "Events
the listener cannot hear" (option 4 adopted after the A/B); "The
listener's exchange is one line" (new, 3.4). Deleted (resolved):
"JavaScript test for the accumulator's packing rules".

### 7.6 Open with the owner right now

- **3.4c or not?** (§7.1)
- **Commit this refreshed handoff** — on the owner's order.
- **At the session's end:** ask permission to delete this handoff.

## 8. Nuances (hard to get from the docs alone)

- **The owner reads the page like a listener** and catches what tests
  cannot: the events' missing context, "coming over", the em dash cut.
  Take each seriously, research with the literal artifacts (record,
  debug file, request body), and record it.
- **The owner's questions find real defects** — "What happens to
  repeated punctuations?" led to the "3.5" bug, also in upstream. When
  asked "how would you parse X", run the real function on X.
- **"You call"** = the agent decides and says so.
- **The owner values upstream contributions** — when a defect also
  affects upstream, document it as a candidate with receipts (the
  follow-up "Upstream contributions to scorbo2").
- **Stray Stops:** a Stop the agent did not press happened twice while
  the owner watched; the owner "may have pushed" it — keep an eye on
  it; if "(stopped mid-round)" appears with nobody pressing, dig in.
- **The owner's setting:** public places, sometimes noisy (no talking
  then — pick tasks that need no voice), closing the lid to move (the
  tunnel ends); the owner restarts the tunnel when told.
- **The same browser pane:** the owner sees and can use the agent's
  built-in browser pane; say which tab and run you are driving.
- **Estimates:** the agent's estimates ran ~2.5× long today; say so
  when estimating, don't pad silently.

## 9. The agent's mistakes today (do not repeat)

- **An improvised plan** — cut 3.1 and changed 3.3 in one message
  without a shape round; rejected ("I cannot proceed with a plan
  improvised and changed on the flight like that").
- **Weekday slips** — "12:40 on Thursday … the timebox ends Friday":
  2026-09-25 is a Friday, 2026-09-26 a Saturday. Check with `date`.
- **Re-opened a settled ruling without citing it** (the accumulator of
  2026-09-22).
- **The "3-4 s" dead air** used the whole round's generation time
  instead of the first line's (~0.8 s); corrected.
- **Unclear wording** — "the accumulator works on each whole line, from
  its done event" confused the owner (the event name `done` vs the
  word "Done."); say what the page receives, with an example.
- **The debug line showed "first sound — s · played 0.0 s"** before a
  round was said; fixed before commit.
- **Test harness slips** — a helper read a DOM note before it existed;
  `clearTimeout` missing in the vm sandbox; timing-based Stops could
  not hit the last line.
- **Stale TODO** — after the owner merged #11 the TODO still called it
  open; keep ticks in step with merges.

- **Unverified UI claims** — "the percentage on hover" relied on a
  `title` tooltip that did not show in the owner's Chrome, and the wavy
  underline broke under descenders; verify visual features in the pane
  (hover, screenshot) before handing them over.

## 10. Operational gotchas and techniques

- **Fork tests:** `.venv/bin/python -m pytest -p no:cacheprovider`
  (grep `passed`); `node tests/test_persona_form.js`, `node
  tests/test_tts_settings.js`, `node tests/test_show_page.js` (grep
  `^ℹ (pass|fail)`); then `find app tests scripts -name __pycache__
  -prune -exec rm -rf {} +`; `awk 'length > 120 {print FILENAME": "FNR":
  "length}'` on changed fork files; `grep -c "–"` for en dashes.
- **The vm sandbox:** `const`/`let` at a script's top level are NOT
  properties of the sandbox — reach them with
  `vm.runInContext("VOICE.pauseInLineMs = 0", sandbox)`; function
  declarations ARE (`sandbox.chunks(...)`). Objects from the sandbox
  have other prototypes: compare via `JSON.parse(JSON.stringify(x))`.
- **Live checks in the browser pane:** `mcp__Claude_Browser__*`. Use a
  REAL click (`computer` `left_click` with a `ref`) for Start — the
  AudioContext needs a user gesture; `element.click()` from JavaScript
  is untrusted. The `javascript_tool` times out at ~45 s: split waits
  (≤40 s per call) or run a watcher in the page that stores results in
  `window.*` and poll it. The page's globals can be wrapped from the
  console for probes (`addLine`, `synthesize`, `playClip`,
  `startRecording` are function declarations — reassigning them changes
  what the page calls). To stop a round in flight at a known point,
  use the one-line round after an invitation.
- **The fake microphone** (3.3's check): before Start,
  `navigator.mediaDevices.getUserMedia = async () =>
  (fakeMic.dest = voice.ctx.createMediaStreamDestination()).stream`;
  after Start, fetch `/api/tts` for the listener's words, decode into
  `voice.ctx`, and wrap `startRecording` to play that buffer into
  `fakeMic.dest` when it starts; drive the turn with `talkPress()` /
  `talkRelease()` from a watcher. Reload the page to drop it.
- **The driver:** `python3 scripts/drive_show.py --rounds N [--played
  S] [--heard "…" --heard - --speak] [--report]`; `--control` for the
  grammar check.
- **Verbatim quotes from the transcript:** user messages are `type:
  user` entries (content string or text blocks); **mid-turn messages
  are `type: queue-operation` entries with a `content` string**. The
  scratchpad's `today_msgs.py <keys…>` lists matching messages with
  timestamps. **The slice 3 plan doc is GENERATED:**
  `build_slice3_doc.py` fills `slice3_body.md` (a `str.format`
  template — literal braces doubled) with messages from the transcript
  by timestamp (`want` map), writes the doc, and the verification
  snippet checks every quote. To add a section: edit `slice3_body.md`,
  add the timestamps, rebuild, verify. **If the scratchpad is gone,
  edit the doc directly** (it is committed) and verify quotes by
  searching the transcript.
- **The pre-commit address scan** (zombie-radio; counts only): the
  wired address from `hosts.yml` against the staged `+` lines; every
  IPv4 in the transcript (minus 127.0.0.1) against the staged lines;
  a key-like grep (`sk-…`, `BEGIN … PRIVATE`, `password =`); stage by
  explicit path; `hosts.yml` never staged. In the fork: no IPv4 other
  than 127.0.0.1 in the staged lines.
- **Dry-run the tunnel target:** `make -n ssh-tunnel ENV=cloud` — mask
  addresses in the output (`sed -E 's/[0-9]+(\.[0-9]+){3}/<box>/g'`).
- **macOS/zsh:** `sed -i ''`; no `--include=*.x` globs in zsh without
  quotes; `date -j -f %Y-%m-%d <d> '+%A'` for weekdays.

- **Showing a past request "as it went over the wire"** without debug
  files: rebuild it from the run's record with the app's own code
  (`assemble_messages` on the run with `rounds` cut to those before, the
  instruction, `build_grammar(speakers, max_lines, MOODS if moods else
  None)`, `round_payload(…, seed=run.seed + n)`), render it with
  `render_prompt` (`/apply-template`) and prove it with
  `count_tokens` (`/tokenize`) against the round's `prompt_n + cache_n`.
- **The browser pane's `zoom` action is not supported** (it returns the
  full screenshot); use `hover` then `screenshot` to see a tooltip.

## 11. Reading order after the compaction

1. This document, in full.
2. `git status -sb` and `git log --oneline -6` in both repositories
   (the fork `alfre2v/show-slice-3-browser`, zombie-radio
   `alfre2v/show-slice-3`); anything unpushed or uncommitted since this
   was written (at writing, both branches were pushed and clean, but
   `hosts.yml`).
3. `docs/TODO.md` — "Now", the slice 3 checklist (3.1-3.3 ticked with
   receipts; 3.4's text now includes the real button), the polish list.
4. `docs/discussions/2026-09-25-show-slice-3-browser-plan.md` — §1.3
   (rulings), §4-§7 (the agenda and its rulings), §8 (the splitter).
5. `docs/follow-ups.md` — today's entries (§7.5), above all "Events the
   listener cannot hear" (the A/B's source) and "Talk anytime".
6. The fork's `docs/runbooks/show-page.md` and `static/show/*.js`.
7. Then report to the owner: the clock, the tunnel (probe), what is
   pending (§7.6), and ask about 3.4c.

## 12. Paste-ready prompt

```
We continue the Zombie-Radio show engine's slice 3 (TODO Task 6b, the
browser): 3.1-3.4b are done and the events A/B is decided; next I decide
whether the listener's exchange becomes 3.4c; then 3.5 (close).
Re-orient before doing anything else:

1. Read docs/discussions/2026-09-25-show-engine-session-handoff-4.md IN
   FULL — how we work (§0 is binding, including the live-box drill
   rules in §0.1), the exact state (§2), what we did today (§3), the
   code of slice 3 as built (§4), the facts and numbers (§5), today's
   rulings (§6), the board ahead with the 3.4c question and the arc's
   estimates (§7), the nuances and your mistakes today (§8-§9), and the
   techniques and gotchas (§10).
2. Follow its reading order (§11) to confirm the state: git status and
   log in both repositories (what is unpushed and uncommitted),
   docs/TODO.md's "Now" and slice 3.
3. Then give me a compact summary: the clock, the tunnel (probe it
   first), what is pending on my side, and the 3.4c question — and wait
   for my go.

Standing rules: strict review-before-commit (I review uncommitted
changes in VS Code — no diffs in chat, no commit without my explicit
order for that commit), no AI attribution anywhere, discussion-first
(plans made in discussion, never improvised), pushback with receipts
welcome, plain language, no delegation to other agents, one question at
a time when I say I am tired, no git kung-fu, and code comments per
repository (minimal in zombie-radio; upstream's docstring style in the
fork).
```
