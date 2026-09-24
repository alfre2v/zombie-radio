# Session handoff 2 — the show engine's build, slice 1 at eight of nine steps

> **EPHEMERAL.** Written 2026-09-24 at ~02:15 CDT by the lead agent,
> mid-session, at the owner's request, as insurance against a context
> compaction (the window stood at 78 %). It is the memory bank for
> whoever resumes: this session after a compaction, or a fresh one.
> It stays in `docs/discussions/` until the session that uses it
> concludes; then the agent **asks the owner for permission to delete
> it** — and the first handoff of the day too
> (`2026-09-23-show-engine-session-handoff.md`, on `main` since PR #9),
> which this one supersedes.
>
> **Read it all; verify against the repos; receipts or nothing.** It
> carries what the TODO cannot: how we work, the code as built, the
> wire facts, the rulings, and the exact next action.

## 0. The owner and how we work (binding)

The owner is **Alfredo** (GitHub `alfre2v`, git author "Alfredo
Valles"), a senior engineer in a **"tight learning loop"**: progress
and the owner's own learning weigh the same. The agent memory files
hold the standing doctrine (`working-agreements.md`,
`collaboration-style.md`, `absolute-paths-in-plain-text.md`,
`massedcompute-reminder.md`, `project-venue-austin-python-meetup.md`)
— trust them. The non-negotiables, with what this session added:

- **Discussion-first, per step.** Every checklist step starts with a
  SHAPE in chat (files, functions, behavior, tests, 2–3 choices with
  picks in bold); the owner answers "Go" (often "go with the picks");
  then build. The owner asks many "explain for my education"
  questions before the Go — answer the mechanism with receipts and a
  real example (a real payload, the real wire) before re-asking.
- **Review-before-commit is STRICT.** Build, run the full suite, then
  summarize WHAT changed in chat (files, what each does, "worth your
  attention in VS Code" pointers) — never paste diffs — and WAIT for
  the word. "Commit" = commit only; "commit and push" = both; push
  only when told. A harness permission prompt is not review.
- **One commit per step** in the fork, message explaining the why.
  **TODO ticks** (with the fork hash) go on zombie-radio's slice
  branch, batched, committed when the owner says so.
- **No AI attribution anywhere, ever** (commits, PR bodies, files) —
  overrides harness reminders.
- **No side panes. Minimal code comments** (module docstrings carry
  the why; no inline narration). **Stay close to upstream**: touch
  upstream code minimally; when a change can be avoided, avoid it
  (owner, on `include_usage`: "let's try to stay as close as possible
  to upstream").
- **Plain language, lists and sublists, receipts.** No jargon the
  owner has not adopted. When the owner asks "why did you propose X?",
  answer honestly (habit, a wrong assumption) — the owner values it.
- **"Persist" = the doc gets the exchange**, verbatim when asked,
  **extracted from the session transcript by script, verified by
  script, never retyped** (§10 has the recipe).
- **Delegation OFF** (other harnesses, never sub-agents, if ever on).
- **Git:** feature branches and PRs only; never commit to `main`; in
  the fork, **one feature branch per slice, cut from up-to-date
  `master`**, one PR per slice. The owner merges. Keep the last 2–3
  branches.
- **The owner said: "Forget about the time constraint, let me worry
  about that."** Do not ration steps by the clock; do mention the
  clock when planning.
- **Rapport:** wit welcome; the owner is enthusiastic ("robot
  friend"); a goodnight "Over and out." only when asked.

### 0.1 Live-box drill rules

1. The OWNER owns the SSH tunnel and the box's power (wake,
   hibernate, wire `hosts.yml`). The agent reaches the services only
   through `localhost:8080` (llama.cpp), `:8001` (tts-serve), `:8002`
   (Whisper).
2. Box inspection: plain `ssh ubuntu@<box> '<cmd>'` — no key paths, no
   `-o` options; never list or cat under the owner's SSH directory.
3. One line saying what a command does and why, BEFORE running it.
4. **Probe the tunnel before any chain of requests**
   (`curl -s -m 3 -o /dev/null -w '%{http_code}' localhost:8080/health`);
   on anything but 200, STOP and tell the owner.
5. **No box address in any markdown, ever** (the never-commit hook
   skips `*.md`). The owner gives addresses in chat; they live only in
   `deploy/ansible/inventories/cloud/hosts.yml` (marked
   `NEVER_COMMIT`, never staged). Pre-commit check without writing an
   address anywhere:
   `grep -rn "$(grep -oE '[0-9]+(\.[0-9]+){3}' deploy/ansible/inventories/cloud/hosts.yml)" docs`
   (only while wired) — plus the older addresses the owner mentioned
   in this session's chat.

## 1. The project in 60 seconds

**Zombie-Radio**: an interactive, audio-only radio play — four AI
scientists trapped in a lab during a zombie outbreak, broadcasting on
shortwave; listeners talk back with hold-to-talk. Hard deadline
**2026-10-08**; presented in a **talk at the Austin Python Meetup in
October 2026** ("hackTNT 2026" is only the owner's internal label —
no hackathon).

The app is **TalkWithZombies**
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`), our fork of
scorbo2's TalkWithMe 7.1. Its show engine is being built now (TODO
Task 6b) as designed in `docs/discussions/2026-09-23-show-engine-design.md`
("SED"): one shared script as the model's context, a director in code,
a GBNF screenplay grammar per request, the browser as the clock. The
model services (llama.cpp with Nemotron Nano 9B v2 Q4_K_M, 16k context,
one slot; tts-serve 1.2; Whisper) run on a rented Hyperstack A6000 box
behind the owner's SSH tunnel.

## 2. Exact state (2026-09-24, ~02:15 CDT)

- **The timebox:** started 2026-09-23 **14:46 CDT** · checkpoint
  **2026-09-25 02:46** (in practice that morning) · end **2026-09-26
  14:46**. Slice 1 targets the end of 09-24 — it is ahead: eight of
  nine steps done.
- **The fork**, branch **`alfre2v/show-slice-1-skeleton`** (cut from
  `master` = `1d41bab`, tag `tz-0.1`), **9 commits, NOT pushed**,
  working tree clean:
  - `b538828` 1.1 the `show:` settings
  - `a268bcd` 1.3 the grammar builder
  - `cf6f8e7` 1.7 grammar key (its keys later moved into
    `stream_round`, see `9ae374a`)
  - `4444aa4` 1.2 the story
  - `b64e5b4` `show.max_tokens` 300 → 512
  - `d30d7ab` 1.4 the stream parser
  - `8b39b17` 1.5 the run record and assembler
  - `ac0de25` 1.6 director v0
  - `9ae374a` 1.8 the endpoints and `stream_round`
  - Full suite: **876 passed**; both Node tests pass.
- **zombie-radio**, branch **`alfre2v/show-slice-1`** (cut from `main`
  = `60ab99a`, PR #9 merged), 1 commit `c785ba5` (ticks 1.1–1.4 and
  1.7; the probe's findings; the raw-history ruling), **NOT pushed**.
  **Uncommitted:** `docs/TODO.md` — ticks for 1.5 (`8b39b17`), 1.6
  (`ac0de25`), 1.8 (`9ae374a`), 1.7's note updated, "Next" → 1.9 —
  plus this handoff (new file). `hosts.yml` is WIRED to the box
  (uncommitted, never stage it).
- **PRs:** zombie-radio #1–#9 merged; fork PR #1 merged. No slice PR
  yet.
- **The box:** UP (woken 2026-09-23 evening by the owner, on a NEW
  address — the IP was not kept this time); the owner re-wired
  `hosts.yml`, SSH'd in (its host key is in the owner's known_hosts),
  and the tunnel is UP; all three services answered 200 at ~01:00.
- **Installed clients on the Mac:** `~/TalkWithZombies-client` (the
  fork at `tz-0.1`, no show code — the four cast personas with
  `say`-made voices in `Personas/`), `~/TalkWithMe-client` (7.1,
  fallback). The dev clone has NO `settings.yaml`, NO `Personas/`, NO
  `runs/` (tests write only to temporary folders).
- **Scratchpad** (`/private/tmp/claude-501/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18/scratchpad/`):
  `probe_round.py` (the one-round probe script), `probe-round-1.json`
  (the real round: messages, grammar, seed 42, `tokens_a` with arrival
  times, `raw_b` = every SSE line), `probe-round-1-include-usage.json`
  (the same with `include_usage`), test logs. The session transcript:
  `/Users/alfredo/.claude/projects/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18.jsonl`.
- **Approved and pending (owner, 2026-09-24 ~02:10):** the
  permissions for step 1.9 — see §7.1.

## 3. What this session did since the first handoff

1. PR #9 (the design, seven decisions, the TODO as execution plan,
   handoff 1) opened and merged. zombie-radio branch
   `alfre2v/show-slice-1` and the fork's slice-1 branch cut.
2. **1.1, 1.3, 1.7** shaped together and built. The 1.1 trap: the chat's
   Settings dialog rebuilds `AppSettings` from its form and
   `save_settings` wrote only five sections — a UI save would have
   erased `show:`; fixed by carrying `show=current.show` over in
   `app/routers/settings.py` like upstream does for `mcp`, and writing
   it in `save_settings`.
3. **1.2**: the story renders run 1's and run 2's proven system
   prompts byte for byte (tested; cross-checked against the gate's
   `cast.py`); mood list filled from `MOODS` (one home); the voice
   check goes through upstream's persona list.
4. **The one-round probe** (read-only, scratchpad script, fork on
   `PYTHONPATH`) proved 1.1+1.2+1.3+1.7 together on the real model and
   recorded the stream (§5). It overturned an assumption: a stream has
   no `usage` by default.
5. **`include_usage` explained and dropped** (the owner asked why it
   was proposed: honestly, habit — the design text said
   `usage.prompt_tokens`; staying with the default `timings` is closer
   to upstream).
6. **The raw-history ruling** (owner): the history keeps exactly what
   the model wrote; normalization only for the voice. Lessons §2.8's
   suggestion to normalize the history had drifted into the TODO
   unruled — corrected with a dated note.
7. **`show.max_tokens` 300 → 512** (the owner saw it bounds a whole
   round, not a line).
8. **1.4, 1.5, 1.6, 1.8** shaped, discussed, built, committed (details
   in §4).
9. This handoff, at the owner's request.

## 4. The code as built (the fork, `alfre2v/show-slice-1-skeleton`)

**Conventions used across `app/show/`:** Pydantic for data that crosses
a boundary (disk, HTTP): `Run`, `Round`, `Line`, the API models;
frozen dataclasses for in-memory values made and used by our code:
`Story`, `ScriptLine`, `RoundPlan`. Paths resolved at call time from
`app.config._PROJECT_ROOT` — no new module-level state, so upstream's
isolation fixture (`tests/conftest.py`) needs nothing new. Upstream's
rules honored: new routes listed in `AGENTS.md`'s endpoint table
(checked by `tests/test_docs.py`); stubs applied at the router's
import site; tests per module.

- **`app/config.py` — `ShowConfig`** (yaml-only `show:` section in
  `AppSettings`, loaded and saved like `mcp`): `story="lab-outbreak"`,
  `episode=None`, `model_prefix="/no_think"`, **`max_tokens=512`**,
  `context_budget=14000`, `seed=None` (random at start, stored in the
  run), `emotion_tags=True`, `debug=False`, `interaction_min_s=60`,
  `interaction_max_s=180` (min ≤ max validated), `listen_window_s=10`,
  `press_cap_s=30`, `no_speech_max=0.6`, `logprob_min=-1.0`,
  `stt_language="en"`. The accumulator's knobs come in 3.3.
- **`app/routers/settings.py`** — carries `show=current.show` over on
  a UI save (the trap).
- **`app/show/grammar.py`** — `MOODS` (run 2's nine: calm, happy, sad,
  afraid, terrified, doubtful, angry, urgent, exhausted);
  `build_grammar(speakers, max_lines, moods=None)` → the proven GBNF
  byte for byte (`root ::= line{1,N}`; `line ::= speaker " (" emotion
  "): " text "\n"` or `speaker ": " text "\n"`; `text` excludes
  `\n [ ]` and, with moods, `( )`); rejects empty, duplicate, quoted
  or newline names and `max_lines < 1`.
- **`stories/lab-outbreak/`** (tracked) — `cast_sheet.md`: front
  matter `title: The Lab at the End of the Frequency`, `cast: [Daniel,
  Moira, Ralph, Samantha]`, `operator: Samantha`; body = run 2's world
  and cast with `{{ model_prefix }}`, `{{ format_rules }}`,
  `{{ episode }}`. `events.yaml`: `events:` = the gate's ten events as
  plain sentences (no "Radio traffic:"/"Offstage:" prefix).
- **`app/show/rules/format_plain.md`, `format_moods.md`** — the proven
  "Format: …" paragraphs; the moods one has `{{ moods }}`.
- **`app/show/story.py`** — `Story` (name, title, cast, operator,
  template, events); `load_story(name, root=None)` (checks front matter
  via upstream's `parse_frontmatter` + required keys, cast non-empty
  and unique, operator in cast, **a persona with a `reference_audio`
  for every cast name** via `app_config.get_personas()`, events
  non-empty) → `StoryError`; `format_rules(emotion_tags)`;
  `render_cast_sheet(story, show, episode="")` (Jinja strict, result
  stripped).
- **`app/show/parser.py`** — `LineParser(moods)`: `feed(piece)` →
  events, `finish()`; **character by character** (chunking cannot
  matter). Per line `ScriptLine(speaker, mood, raw, spoken)`: `raw` =
  exactly what the model wrote (history), `spoken` = for the voice
  (`’‘`→`'`, `“”`→`"`, `—`→`, `, `…`→`...`, spaces trimmed and
  collapsed, wrapping quotes removed). Events: `start {persona, mood}`
  once the prefix `Name (mood): ` is complete; `token {persona, token}`
  with spoken text only (whitespace and a closing quote held back until
  something follows); `done {persona, text}`. A line without its `\n`
  or without a valid prefix goes to `dropped`, no `done`.
- **`app/show/script.py`** — `Line`, `Round` (n, instruction, listener,
  speakers, max_lines, **event**, lines, dropped, timings {prompt_n,
  cache_n, predicted_n}, finish_reason, trimmed, episode), `Run`
  (run_id, started, story, cast, moods, seed, **`systems` per
  episode** — `""` = no episode, episode, rounds). `runs_root()`,
  `new_run(story, show, system, seed, now=None)` (id =
  `%Y-%m-%dT%H-%M-%S`, `-2`, `-3` on collision), `save_run` (temp file
  then `os.replace`), `load_run`, `append_round` (saves), `reply_text`
  (`"".join(raw + "\n")`), **`assemble_messages(run, instruction)`**:
  system = `run.systems[run.episode]`, then user/assistant per kept
  round (skips trimmed, line-less, other-episode rounds), then the new
  instruction. `runs/` in the fork's `.gitignore`.
- **`app/show/director.py`** — `RoundPlan(kind, speakers, max_lines,
  event, instruction, grammar)`; **`plan_round(run, story, moods)`**:
  pure; `random.Random(f"{run.seed}:{n}")`; 2–3 speakers (cast order),
  2–3 lines, an event on odd rounds from the pool without repeats
  until used up (`_next_event` reads `Round.event`);
  `instruction_for(speakers, max_lines, event, moods)` →
  `"Offstage: <event> Moira and Ralph speak next: the next two lines,
  each with the emotion in its voice."` (one line: "…speaks next: the
  next line, with the emotion in its voice."; moods off drops the
  tail).
- **`app/services/llm.py`** — `_iter_sse_chunks` (whole chunks) under
  `_iter_completion_chunks` (unchanged behavior); **`stream_chat`
  identical to upstream**; **`stream_round(messages, *, grammar,
  max_tokens, seed)`** → `{"token": …}` per piece, then
  `{"timings": {prompt_n, cache_n, predicted_n}, "finish_reason": …}`.
- **`app/routers/show.py`** (registered in `app/main.py`) —
  `POST /api/show/start` (`ShowStartRequest{story?}` →
  `ShowStartResponse{run_id, story, title, cast, operator, seed}`;
  422 on `StoryError`); `POST /api/show/round`
  (`ShowRoundRequest{run_id, played_s=0, transcript=None}`; run id
  matched against `^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}(-\d+)?$` → else
  404; streams SSE: `start` (+mood, message_id), `token`, `done`
  (+message_id `<run-id>-r003-l1`), then `round {n, speakers, event,
  dropped, finish_reason}`, `complete`; per-round seed = `run.seed +
  n`; error → `error` + `complete`, nothing recorded; disconnect →
  logged, re-raised, nothing recorded — untested). Models in
  `app/models.py`.
- **Tests added:** `test_show_config.py`, `test_show_grammar.py`,
  `test_show_story.py`, `test_show_parser.py` (embeds the real 42-token
  recording as `REAL_ROUND`, `REAL_TEXT`, `REAL_LINES`),
  `test_show_script.py`, `test_show_director.py`,
  `test_routers_show.py` (fakes `app.routers.show.stream_round` with
  the recording), plus additions in `test_routers_settings.py` and
  `test_llm.py`.

## 5. Facts and numbers (measured 2026-09-23/24 unless marked)

- **The probe round** (seed 42, lab-outbreak cast sheet with moods,
  grammar Ralph|Moira, 2 lines): 42 tokens, first at 673 ms, last at
  1,188 ms:
  `Ralph (urgent): We’ve got something outside, rhythmic pounding. It’s not human. Over.  \nMoira (afraid): It’s adapting. Or maybe it’s learning. Over.\n`
  — the same text three times with the same seed (determinism).
- **Token shapes:** names and tags split (`'R' 'alph' ' (' 'urg' 'ent'
  '):'`); curly apostrophes; **two trailing spaces before a line
  break** (`'  ' '\n'`); a final `'.\n'` glues punctuation and break;
  tokens arrive **in bursts** through the tunnel (several with the same
  arrival millisecond).
- **The wire (SSE):** `data: {chunk}` lines; first chunk `delta:
  {role: assistant, content: null}`; middle chunks one token each in
  `choices[0].delta.content`; last chunk `finish_reason: "stop"`, empty
  delta, and llama.cpp's **`timings`** at the top level; then
  `data: [DONE]`. **No `usage` unless `stream_options.include_usage`**
  — which adds a chunk with empty `choices` (upstream's reader would
  warn and drop it) and moves `timings` there. **The script's size =
  `prompt_n + cache_n`** (probe: 4 + 303 = 307; `prompt_n` alone counts
  only fresh tokens), **after the round + `predicted_n`** (43 → 350).
- **Browser TTS:** with `tts.streaming` on (the installed client), the
  voice is fed from `token` events (`static/chat.js:230-235` →
  `accumulateForTTS`, `static/tts.js:88`); `done` only flushes the
  rest.
- **Sizes:** a two-line round ≈ 0.9 KB of JSON, four lines ≈ 1.4 KB; a
  40-minute run (~120 rounds) ≈ 150–200 KB. The gate's four-line
  rounds generated 72–82 tokens; ~125 tokens of history per round.
- **Whisper fields** (`/v1/audio/transcriptions`): `file, prompt,
  response_format, task, language, vad_filter, vad_threshold,
  vad_neg_threshold, vad_min_speech_duration_ms,
  vad_max_speech_duration_s, vad_min_silence_duration_ms,
  vad_speech_pad_ms, repetition_penalty, gpt_refine`.
- **The box's GPU:** 13.0 of 46 GB used (llama.cpp 6.8, TTS 5.3,
  Whisper 0.9) — on the previous boot. `/apply-template` exists
  (~120 ms, no slot).

## 6. Rulings this session (after the first handoff)

- 1.1/1.3/1.7 batched; the settings trap closed.
- The mood list's one home is `MOODS`; the style sentence ("Over.")
  stays inside the format snippets to keep the proven text byte for
  byte (a flagged deviation from decision 4's sketch; revisit with
  the bibles, Task 4).
- Probe first when the box is up ("the VM is there wasting money for
  you to test things").
- **Size from `timings`, not `usage`; no `include_usage`** (stay close
  to upstream). SED §2.4 has a dated note; TODO 1.8 and 2.2 follow.
- **The history keeps the model's raw text; normalization only for the
  voice** (every event the browser receives); lessons §2.8 dated note.
- `show.max_tokens` = 512 (a round's guard).
- A line cut short: dropped and reported; the recording embedded in
  the test file.
- 1.5: write at Start and once per round, atomically; one file per
  run; `systems` per episode; a line-less round skipped in history;
  Pydantic.
- 1.6: a generator per round from seed + round number; `event` on
  `Round`; events on odd rounds.
- 1.8: no show state on the server (run id from the caller); a
  disconnect records nothing; errors → `error` + `complete`;
  `stream_chat` restored to upstream.
- SQLite noted by the owner as the tool for "anything more serious"
  (not recorded as a follow-up yet — the agent offered; no answer).
- Repetition detection: out of the MVP (detection is cheap, reaction
  costs a round).

## 7. The board ahead

### 7.1 NEXT: step 1.9 — the driver, and ten rounds on the box

**Owner-approved permissions (2026-09-24 ~02:10):** create the dev
clone's `settings.yaml`; copy the installed client's `Personas/` into
the scratchpad; start and stop the dev server on port 8010; ~10 + 1
real requests to the box through the tunnel. The driver script is code:
it gets the owner's review before its commit.

1. **Tunnel probe** (§0.1 rule 4).
2. **Personas copy:** `cp -R ~/TalkWithZombies-client/Personas <scratchpad>/show-personas`
   (a copy, because it is unverified whether the app's startup scan
   writes into the folder).
3. **`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies/settings.yaml`**
   (gitignored): `llm.base_url http://localhost:8080`, `tts` enabled at
   `http://localhost:8001`, `stt` at `http://localhost:8002`,
   `general.personas_directory` = the scratchpad copy,
   `show.seed: 42` (the rest default). Check what the app writes on
   startup; nothing else in the clone may change except `runs/`.
4. **Start** `cd <fork> && .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8010`
   in the background (log to the scratchpad); wait for HTTP 200 with
   `curl --retry`.
5. **Write `scripts/drive_show.py`** (standard library only):
   `--base http://127.0.0.1:8010`, `--rounds 10`, `--story`, `--control`.
   Start a run; for each round POST `/api/show/round` with `run_id` and
   `played_s: 20`, read the SSE stream line by line (urllib), print each
   `done` as `Speaker (mood): text` with its arrival time, the time to
   the first line and the round's total; print the `round` summary; at
   the end totals (lines, dropped, average round time, the last round's
   `prompt_n + cache_n + predicted_n` from `script.json`) and the
   record's path. `--control`: one request straight to
   `http://localhost:8080/v1/chat/completions` with the rendered cast
   sheet, an instruction, and a grammar allowing only `"Operator"` —
   every line must come back as `Operator`.
6. **Run** ten rounds, then `--control`. Save the output to the
   scratchpad. Stop the server (`lsof -nP -iTCP:8010 -sTCP:LISTEN -t`,
   `kill`, re-check).
7. **Report** to the owner (lines, timings, anything dropped, the
   control result), then review of the driver, commit, tick 1.9 (the
   run's receipts in the tick).
8. **Slice 1 closes:** push the fork's branch and open the fork's PR
   (`gh pr create --repo alfre2v/TalkWithZombies --base master --head
   alfre2v/show-slice-1-skeleton`) — only when the owner says; commit
   and push zombie-radio's `alfre2v/show-slice-1` (ticks + this
   handoff) and its PR — only when the owner says. **The owner merges.**

### 7.2 Then

- **Slice 2** (branch `alfre2v/show-slice-2-rules`, cut from the fork's
  `master` after slice 1 merges): 2.1 director v1 · 2.2 the trim (size
  from `timings`; pause measured with a low `context_budget`) · 2.3 the
  debug switch (`/apply-template`) · 2.4 the STT client and the
  transcript filter · 2.5 the driver extended. Then the **checkpoint**
  on the box (TODO has what it judges and the scale-down order).
- **Slice 3** (browser), polish if green, then Tasks 5, 7, 8.
- **Owner-side:** Task 4 (bibles → the cast entries of
  `stories/lab-outbreak/cast_sheet.md`; voice samples, never
  committed); decide the box's fate after the timebox.
- **At the session's end:** ask permission to delete BOTH handoffs
  (this one and `2026-09-23-show-engine-session-handoff.md`).

## 8. Nuances

- **The owner catches drift.** Twice a suggestion of the agent's own
  (lessons §2.8; `usage.prompt_tokens`) turned into a "fact" in a later
  doc. When a doc says "decided", check who decided it.
- **The owner reads the code** ("I saw something you said about adding
  a field…"): point to the few lines that matter; expect questions on
  data modeling (Pydantic vs dataclass), persistence frequency, cost
  of loops.
- **Explain the wire with the wire.** The owner loved seeing real SSE
  lines; show real bytes (the probe files are in the scratchpad).
- **Byte-identical anchors:** the grammar and the cast sheet reproduce
  proven text byte for byte, and tests pin it; any change to those
  texts loses the anchor — say so when it happens.
- **The owner's box habits:** hibernates at night, wakes it for a
  session; the IP may change (not kept on 2026-09-23 night).
- **Pronouns:** avoid pronouns for the owner in new writing.

## 9. My mistakes this session (do not repeat)

- **Proposed `stream_options.include_usage`** because the design text
  said `usage.prompt_tokens` — made the wire fit the doc instead of
  fixing the doc. Check the wire first.
- **Let an unruled suggestion (normalize the history) become a TODO
  rule.**
- **Claimed "the file's shape won't change later"** for 1.5 with a
  single `system` — episodes need one per episode; corrected before
  building.
- Earlier today (handoff 1 §9): a from-memory "verbatim"; unchecked
  time and count; chained requests after a failed tunnel probe; a
  pipe's exit code read as grep's; a cut heading in a scripted
  restructure; two TalkWithMe-era reuse proposals reversed.
- **A scratch script importing the fork** needs `PYTHONPATH=<fork>`
  (it failed once with `No module named 'app'`).

## 10. Operational gotchas

- **Fork tests:** `.venv/bin/python -m pytest -p no:cacheprovider`
  (`.pytest_cache` is not gitignored); `node tests/test_persona_form.js`,
  `node tests/test_tts_settings.js`; then
  `find app tests -name __pycache__ -prune -exec rm -rf {} +`. One
  Starlette deprecation warning is normal.
- **macOS:** `sed -i ''`; zsh: quote globs, no `PIPESTATUS`,
  foreground `sleep` blocked (use `curl --retry` to wait for a
  server).
- **Verbatim extraction:** read the transcript JSONL (§2), pick
  `message.role` / `message.content[].text` blocks by a distinctive
  phrase (LAST match), write to the scratchpad, insert by script, then
  assert each block is present in the doc. A bridging text block may
  be missing from the transcript — note it, never retype it.
- **Fork PRs:** always `--repo alfre2v/TalkWithZombies --base master`.
- **The box:** `docker ps` shows `llama` and `whisper`; the TTS is the
  systemd unit `tts-faster_qwen3tts`; `docker logs llama` carries
  earlier runs' lines.
- **Pre-commit ritual:** the address grep (§0.1 rule 5); a key-like
  scan of the diff; stage by explicit path; never `hosts.yml`.

## 11. Reading order after a compaction

1. This document, in full.
2. `git -C <fork> log --oneline master..HEAD`; `git status -sb` in both
   repos (expect §2's state; if the owner acted since, trust the repo).
3. `docs/TODO.md` — "Now", Task 6b's slice 1 (1.9) and slice 2.
4. SED §7.3 (the slices) and the build notes of the step at hand;
   the fork's `AGENTS.md` (upstream's test rules).
5. The code (§4) as needed — `app/routers/show.py` is the hub.

## 12. Paste-ready prompt

```
We continue the Zombie-Radio show engine's build (TODO Task 6b, slice
1, step 1.9). Re-orient before doing anything else:

1. Read docs/discussions/2026-09-23-show-engine-session-handoff-2.md IN
   FULL — how we work (§0 is binding, including the live-box drill
   rules), the exact state (§2), the code as built (§4), the facts
   (§5), the rulings (§6), the board ahead (§7 — 1.9's approved plan
   is in §7.1), the nuances and your predecessor's mistakes (§8–§9),
   and the gotchas (§10).
2. Follow its reading order (§11) to confirm the state: git log and
   status in both repositories, and docs/TODO.md's "Now" and slice 1.
3. Then give me a compact summary: where slice 1 and the clock stand,
   what is pending on my side, and whether the box and tunnel are
   needed now — and wait for my go before running anything on the box.

Standing rules: strict review-before-commit (I review uncommitted
changes in VS Code — no diffs in chat, no commits without my explicit
word), no AI attribution anywhere, no side panes, minimal code
comments, discussion-first, pushback with receipts welcome, plain
language, no delegation to other agents for now, and one question at
a time when I say I am tired.
```
