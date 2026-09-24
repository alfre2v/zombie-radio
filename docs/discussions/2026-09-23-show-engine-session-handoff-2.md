# Session handoff 2 — the show engine's build: slice 1 done, slice 2 next

> **EPHEMERAL.** First written 2026-09-24 ~02:15 CDT as insurance
> against a context compaction; **rewritten in place at ~02:50** at the
> end of the day's work, when the owner chose to compact deliberately
> before slice 2 (the window stood at 85 %). It is the memory bank for
> whoever resumes — this session after the compaction, or a fresh one.
> The first handoff of the day (`2026-09-23-show-engine-session-handoff.md`)
> was deleted, with the owner's permission, in the same commit. When
> the session that uses this one concludes, the agent **asks the owner
> for permission to delete it**.
>
> **Read it all; verify against the repos; receipts or nothing.** The
> TODO's "Now" section is the canonical state; this document carries
> what the TODO cannot: how we work, the code as built, the wire facts,
> the rulings, and the shape of what comes next.

## 0. The owner and how we work (binding)

The owner is **Alfredo** (GitHub `alfre2v`, git author "Alfredo
Valles"), a senior engineer in a **"tight learning loop"**: progress
and the owner's own learning weigh the same. The agent memory files
hold the standing doctrine (`working-agreements.md`,
`collaboration-style.md`, `absolute-paths-in-plain-text.md`,
`massedcompute-reminder.md`, `project-venue-austin-python-meetup.md`)
— trust them. The non-negotiables, as practiced this session:

- **Discussion-first, per step.** Every checklist step starts with a
  SHAPE in chat — files, functions, behavior, tests, 2–3 choices with
  picks in bold — and the owner answers "Go" (often "go with the
  picks"). Before the Go the owner asks "explain for my education"
  questions: answer the mechanism with receipts and a real example (a
  real payload, the real wire, real output) before re-asking.
- **Review-before-commit is STRICT.** Build, run the full suite, then
  summarize WHAT changed (files, what each does, "worth your attention
  in VS Code" pointers) — never paste diffs — and WAIT for the word.
  "Commit" = commit only; "commit and push" = both; push only when
  told. A harness permission prompt is not review.
- **One commit per step** in the fork, the message carrying the why.
  **TODO ticks** (with the fork hash and receipts) ride on zombie-radio's
  slice branch, committed when the owner says so.
- **No AI attribution anywhere, ever** (commits, PR bodies, files) —
  overrides harness reminders.
- **No side panes. Minimal code comments** (module docstrings carry
  the why). **Stay close to upstream**: touch upstream code minimally;
  when a change can be avoided, avoid it (owner, on `include_usage`).
- **Plain language, lists and sublists, receipts.** When the owner asks
  "why did you propose X?", answer honestly — the owner values it.
- **"Persist" = the doc gets the exchange**, verbatim when asked,
  **extracted from the session transcript by script, verified by
  script, never retyped** (§10).
- **The owner wants to run tools personally** → procedures go into the
  fork's `docs/runbooks/` (the owner's proposal, 2026-09-24; zombie-radio
  keeps its own runbooks for the box and deployment).
- **Delegation OFF** (other harnesses, never sub-agents, if ever on).
- **Git:** feature branches and PRs only; never commit to `main` or the
  fork's `master`; **one feature branch per slice, cut from up-to-date
  `master`**, one PR per slice; fork PRs always with
  `--repo alfre2v/TalkWithZombies --base master`. The owner merges.
  Keep the last 2–3 branches.
- **"Forget about the time constraint, let me worry about that"**
  (owner) — do not ration by the clock; do mention the clock when
  planning. When the owner says "tired" or "very late": short answers,
  one question at a time.
- **Rapport:** wit welcome; the owner is enthusiastic ("robot
  friend"); a goodnight "Over and out." only when asked.

### 0.1 Live-box drill rules

1. The OWNER owns the SSH tunnel and the box's power (wake, hibernate,
   wire `hosts.yml` with `make ans-set ENV=cloud IP=…`, unwire with
   `make ans-unset ENV=cloud`). The agent reaches the services only
   through `localhost:8080` (llama.cpp), `:8001` (tts-serve), `:8002`
   (Whisper).
2. Box inspection: plain `ssh ubuntu@<box> '<cmd>'` — no key paths, no
   `-o` options; never list or cat under the owner's SSH directory.
3. One line saying what a command does and why, BEFORE running it.
4. **Probe the tunnel before any chain of requests**
   (`curl -s -m 3 -o /dev/null -w '%{http_code}' localhost:8080/health`);
   on anything but 200, STOP and tell the owner.
5. **No box address in any markdown, ever** (the never-commit hook skips
   `*.md`). Addresses live only in `hosts.yml` (`NEVER_COMMIT`, never
   staged). Pre-commit check, without writing an address anywhere:
   `grep -rn "$(grep -oE '[0-9]+(\.[0-9]+){3}' deploy/ansible/inventories/cloud/hosts.yml)" docs`
   — **only while wired**: unwired, the pattern is empty and grep
   matches every file (a false alarm that happened on 2026-09-24).
   Guard it (`[ -n "$ip" ]`) and also scan for the older addresses the
   owner mentioned in chat, typed in the command, never in a file.

## 1. The project in 60 seconds

**Zombie-Radio**: an interactive, audio-only radio play — four AI
scientists trapped in a lab during a zombie outbreak, broadcasting on
shortwave; listeners talk back with hold-to-talk. Hard deadline
**2026-10-08**; presented in a **talk at the Austin Python Meetup in
October 2026** ("hackTNT 2026" is only the owner's internal label).

The app is **TalkWithZombies**
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`), our fork of
scorbo2's TalkWithMe 7.1. Its show engine is being built (TODO Task 6b)
as designed in `docs/discussions/2026-09-23-show-engine-design.md`
("SED"): one shared script as the model's context, a director in code,
a GBNF screenplay grammar per request, the browser as the clock. The
model services (llama.cpp with Nemotron Nano 9B v2 Q4_K_M, 16k context,
one slot; tts-serve 1.2; Whisper) run on a rented Hyperstack A6000 box
behind the owner's SSH tunnel.

## 2. Exact state (2026-09-24, ~02:50 CDT)

- **The timebox:** started 2026-09-23 **14:46 CDT** · checkpoint
  **2026-09-25 02:46** (in practice that morning) · end **2026-09-26
  14:46**. **Slice 1 finished at ~02:30 on 09-24**, well ahead of its
  end-of-day target; slice 2 has the day of 09-24 before the
  checkpoint.
- **The fork:** branch **`alfre2v/show-slice-1-skeleton`**, 11 commits,
  **pushed; PR alfre2v/TalkWithZombies#2 OPEN** into `master`
  (`1d41bab`, tag `tz-0.1`):
  `b538828` 1.1 settings · `a268bcd` 1.3 grammar · `cf6f8e7` 1.7
  (keys later moved into `stream_round`) · `4444aa4` 1.2 story ·
  `b64e5b4` `max_tokens` 512 · `d30d7ab` 1.4 parser · `8b39b17` 1.5
  record and assembler · `ac0de25` 1.6 director v0 · `9ae374a` 1.8
  endpoints · `4f1d908` 1.9 driver · `78cfee7` runbook. Suite **876
  passed**; both Node tests pass.
- **zombie-radio:** branch **`alfre2v/show-slice-1`** from `main`
  (`60ab99a`, PR #9 merged), **pushed; PR #10 OPEN** into `main`:
  `c785ba5` (ticks, probe findings, raw-history ruling), `e4b8d88`
  (ticks, handoff 2 first version), `1f5e6bf` (slice 1 complete),
  plus the commit carrying this rewrite and handoff 1's deletion.
- **When both PRs merge:** slice 2 starts on
  `alfre2v/show-slice-2-rules`, cut from the fork's updated `master`;
  zombie-radio's ticks for slice 2 on a new branch (e.g.
  `alfre2v/show-slice-2`) from updated `main`.
- **The box: HIBERNATED** by the owner (2026-09-24 ~02:45), and
  **`hosts.yml` reverted by the owner to the committed placeholder**
  (`ansible_host: REPLACE_ME_box_ip`; no local change left). Its
  address changed on the 09-23 wake (the IP was not kept). Waking it
  (possibly on a new address again), re-wiring and the tunnel are the
  owner's.
- **The dev clone** (the fork) holds, gitignored: **`settings.yaml`**
  (tunnel ports; `general.personas_directory:
  /Users/alfredo/TalkWithZombies-client/Personas`; `show.seed: 42`) and
  **`runs/2026-09-24T02-18-51/`** (the first real run). No dev server
  is running.
- **Installed clients on the Mac:** `~/TalkWithZombies-client` (the
  fork at `tz-0.1` — no show code; its `Personas/` holds the four cast
  personas with `say`-made voices, used by the dev settings above);
  `~/TalkWithMe-client` (7.1, fallback).
- **Scratchpad** (`/private/tmp/claude-501/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18/scratchpad/`,
  temporary — nothing depends on it now): `probe-round-1.json` (the
  first probe: messages, grammar, seed 42, tokens with arrival times,
  every SSE line), `probe-round-1-include-usage.json`,
  `drive-10-rounds.txt`, `drive-control*.txt`, `dev-server-8010.log`,
  `show-personas/` (an unused copy). The session transcript:
  `/Users/alfredo/.claude/projects/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18.jsonl`.

## 3. What this session did (2026-09-23 evening → 2026-09-24 ~02:50)

1. PR #9 (the design) merged; slice branches cut in both repos.
2. **Slice 1, step by step,** each shaped, discussed, built, reviewed
   and committed: 1.1 settings (with the Settings-dialog trap closed),
   1.3 grammar, 1.7 grammar key, 1.2 story (proven prompts byte for
   byte), **a one-round probe on the box** (§5), `max_tokens` 512, 1.4
   parser (raw vs spoken), 1.5 record and assembler, 1.6 director v0,
   1.8 endpoints and `stream_round`, **1.9 the driver and ten real
   rounds on the box**.
3. **The owner's rulings along the way** (§6), notably: size from
   `timings`; the history keeps the model's raw text.
4. **The fork's first runbook** (`docs/runbooks/show-driver.md`), at
   the owner's proposal; the fork's `docs/README.md` and README's
   "Where things live" point to it.
5. **Slice 1 closed:** both branches pushed, PRs #2 (fork) and #10
   (zombie-radio) opened.
6. This handoff, rewritten; the owner chose to compact before slice 2.

## 4. The code as built (the fork, slice 1)

**Conventions across `app/show/`:** Pydantic for data that crosses a
boundary (disk, HTTP): `Run`, `Round`, `Line`, the API models; frozen
dataclasses for in-memory values: `Story`, `ScriptLine`, `RoundPlan`.
Paths resolved at call time from `app.config._PROJECT_ROOT` — no new
module-level state, so upstream's isolation fixture (`tests/conftest.py`)
needs nothing new. Upstream's rules honored: new routes in `AGENTS.md`'s
endpoint table (checked by `tests/test_docs.py`); stubs at the router's
import site; tests per module.

- **`app/config.py` — `ShowConfig`** (`show:` in `AppSettings`, loaded
  and saved like `mcp`): `story="lab-outbreak"`, `episode=None`,
  `model_prefix="/no_think"`, **`max_tokens=512`**, `context_budget=14000`,
  `seed=None` (random at start, stored in the run), `emotion_tags=True`,
  `debug=False`, `interaction_min_s=60`, `interaction_max_s=180` (min ≤
  max), `listen_window_s=10`, `press_cap_s=30`, `no_speech_max=0.6`,
  `logprob_min=-1.0`, `stt_language="en"`. `app/routers/settings.py`
  carries `show=current.show` over on a UI save.
- **`app/show/grammar.py`** — `MOODS` (calm, happy, sad, afraid,
  terrified, doubtful, angry, urgent, exhausted);
  `build_grammar(speakers, max_lines, moods=None)` → the proven GBNF
  byte for byte.
- **`stories/lab-outbreak/`** — `cast_sheet.md` (front matter `title`,
  `cast: [Daniel, Moira, Ralph, Samantha]`, `operator: Samantha`; body
  with `{{ model_prefix }}`, `{{ format_rules }}`, `{{ episode }}`);
  `events.yaml` (`events:` — the gate's ten, plain sentences).
  `app/show/rules/format_plain.md`, `format_moods.md` (`{{ moods }}`).
- **`app/show/story.py`** — `Story`; `load_story(name, root=None)`
  (upstream's `parse_frontmatter` + required keys; unique cast; operator
  in cast; a persona with `reference_audio` per cast name via
  `app_config.get_personas()`; events) → `StoryError`;
  `format_rules(emotion_tags)`; `render_cast_sheet(story, show, episode="")`
  (Jinja strict, stripped).
- **`app/show/parser.py`** — `LineParser(moods)`: `feed(piece)` →
  events, `finish()`; character by character. `ScriptLine(speaker,
  mood, raw, spoken)`: `raw` for the history; `spoken` for the voice
  (`’‘`→`'`, `“”`→`"`, `—`→`, `, `…`→`...`, spaces trimmed and
  collapsed, wrapping quotes removed). Events: `start {persona, mood}`
  once `Name (mood): ` is complete; `token {persona, token}` (spoken
  text; whitespace and a closing quote held back); `done {persona,
  text}`. A line without its `\n` or a valid prefix → `dropped`.
- **`app/show/script.py`** — `Line`, `Round` (n, instruction, listener,
  speakers, max_lines, event, lines, dropped, timings {prompt_n,
  cache_n, predicted_n}, finish_reason, trimmed, episode), `Run`
  (run_id, started, story, cast, moods, seed, **`systems` per
  episode**, episode, rounds). `runs_root()`, `new_run(...)` (id
  `%Y-%m-%dT%H-%M-%S`, `-2`… on collision), `save_run` (temp + rename),
  `load_run`, `append_round`, `reply_text`, **`assemble_messages(run,
  instruction)`** (system = current episode's text; kept rounds as
  user/assistant; skips trimmed, line-less, other-episode rounds).
- **`app/show/director.py`** — `RoundPlan(kind, speakers, max_lines,
  event, instruction, grammar)`; **`plan_round(run, story, moods)`**,
  pure, `random.Random(f"{run.seed}:{n}")`: 2–3 speakers (cast order),
  2–3 lines, an event on odd rounds without repeats until the pool is
  used; `instruction_for(speakers, max_lines, event, moods)` →
  `"Offstage: <event> Moira and Ralph speak next: the next two lines,
  each with the emotion in its voice."`
- **`app/services/llm.py`** — `_iter_sse_chunks` (whole chunks) under
  `_iter_completion_chunks` (unchanged behavior); **`stream_chat` =
  upstream's code**; **`stream_round(messages, *, grammar, max_tokens,
  seed)`** → `{"token": …}` per piece, then `{"timings": …,
  "finish_reason": …}`.
- **`app/routers/show.py`** (registered in `app/main.py`; models in
  `app/models.py`) — `POST /api/show/start` (`{story?}` → `{run_id,
  story, title, cast, operator, seed}`; 422 on `StoryError`);
  `POST /api/show/round` (`{run_id, played_s=0, transcript=None}`; run
  id pattern-checked → 404; SSE `start` (+mood, message_id), `token`,
  `done` (+message_id `<run-id>-r003-l1`), `round {n, speakers, event,
  dropped, finish_reason}`, `complete`; per-round seed `run.seed + n`;
  error → `error` + `complete`, nothing recorded; a disconnect →
  logged, re-raised, nothing recorded — untested). **Slice 1 does not
  use `played_s` or `transcript` yet.**
- **`scripts/drive_show.py`** — standard library only: `--base`
  (default `http://127.0.0.1:8010`), `--rounds`, `--story`, `--played`,
  `--runs-dir`; **`--control`** (no app, no new run: borrows the newest
  run's cast sheet or `--run-id`'s, one request straight to llama.cpp
  allowing only `"Operator"`). `.gitignore` gains
  `app/show/__pycache__/`.
- **`docs/runbooks/show-driver.md`** — how to drive the show and run the
  control check (settings, commands, real output, troubleshooting).
- **Tests:** `test_show_config.py`, `test_show_grammar.py`,
  `test_show_story.py`, `test_show_parser.py` (the real 42-token
  recording as `REAL_ROUND`, `REAL_TEXT`, `REAL_LINES`),
  `test_show_script.py`, `test_show_director.py`,
  `test_routers_show.py`, additions in `test_routers_settings.py` and
  `test_llm.py`.

## 5. Facts and numbers (measured 2026-09-23/24)

- **The first real run** (`runs/2026-09-24T02-18-51/`, seed 42, through
  the app on port 8010 and the tunnel): 10 rounds, 24 lines, 0
  dropped, every round `stop`, every round within its speakers and
  **filling its line budget exactly** ("the next two lines" → two);
  first line ~0.8 s, round ~1.0–1.4 s (average 1.16 s); the script
  1,164 tokens after round 10; each round re-reads only ~115–150 tokens
  while `cache_n` grows 259 → 976 (the prompt cache works); `raw` kept
  curly punctuation in 21 lines and trailing spaces in 14, `spoken`
  none; the characters react to the events. Control: PASS (twice, same
  seed → same two Operator lines).
- **The first probe** (one round, before the app existed): 42 tokens,
  first at 673 ms; names and tags split across tokens; two trailing
  spaces before a line break; `'.\n'` glued; tokens arrive in bursts.
- **The wire (SSE):** `data: {chunk}` lines; a first chunk announcing
  the assistant role; one token per middle chunk in
  `choices[0].delta.content`; a final chunk with `finish_reason:
  "stop"`, an empty delta, and llama.cpp's **`timings`** at the top
  level; `data: [DONE]`. **No `usage`** unless
  `stream_options.include_usage` (which adds an empty-`choices` chunk
  and moves `timings` onto it — unused). **Script size =
  `prompt_n + cache_n`, + `predicted_n` after the round.**
- **Browser TTS:** with `tts.streaming` on, the voice is fed from
  `token` events (`static/chat.js:230-235` → `accumulateForTTS`);
  `done` flushes the rest.
- **The app's startup** reads the Personas folder without writing into
  it (verified); it warns that the cast folders lack `language.txt`
  and defaults to English.
- **Sizes:** a round ≈ 0.9–1.4 KB of JSON; a 40-minute run ≈ 150–200 KB.
- **Whisper's fields** (`/v1/audio/transcriptions`): `file, prompt,
  response_format, task, language, vad_filter, vad_threshold,
  vad_neg_threshold, vad_min_speech_duration_ms,
  vad_max_speech_duration_s, vad_min_silence_duration_ms,
  vad_speech_pad_ms, repetition_penalty, gpt_refine`; replies carry
  per-segment `no_speech_prob` and `avg_logprob`.
- `/apply-template` exists on the box's llama.cpp (~120 ms, no slot).

## 6. Rulings this session

- The Settings-dialog trap closed (carry `show` over like `mcp`).
- `MOODS` is the mood list's one home; the "Over." style sentence
  stays in the format snippets to keep the proven text byte for byte
  (revisit with the bibles, Task 4).
- Probe on the box whenever it is up ("the VM is there wasting money
  for you to test things").
- **Size from `timings`, no `include_usage`** (stay close to upstream).
- **The history keeps the model's raw text; normalization only for the
  voice** (every event the browser receives).
- `show.max_tokens` = 512 (a round's guard, not a line's).
- A line cut short is dropped and reported.
- 1.5: write at Start and once per round, atomically; one file per run;
  `systems` per episode; a line-less round stays out of the history;
  Pydantic.
- 1.6: a generator per round from seed + round number; `event` on
  `Round`; events on odd rounds.
- 1.8: no show state on the server; a disconnect records nothing;
  `stream_chat` restored to upstream.
- `--control` must open nothing; the empty run it once created was
  deleted; the dev settings point at the installed client's Personas.
- **Runbooks for the fork live in the fork's `docs/runbooks/`.**
- SQLite: the owner's choice for "anything more serious" than the
  MVP's JSON files (not yet a follow-up entry; the agent offered).
- Repetition detection stays out of the MVP.
- **Compact deliberately at a clean boundary** (slice 1 closed) rather
  than start slice 2 at 85 %.

## 7. The board ahead

### 7.1 NEXT, after the compaction

1. **Re-orient** (§11), then report and wait for the owner's go.
2. **PRs #2 and #10** — the owner reviews and merges (if not already).
3. **Cut `alfre2v/show-slice-2-rules`** from the fork's updated
   `master`, and a zombie-radio slice-2 branch from updated `main`.
4. **Shape 2.1** first, as usual (§7.2 has the questions to settle).

### 7.2 Slice 2 — the rules (target: the checkpoint, 09-25 morning)

From the TODO's checklist, with what each step's shape must settle:

- **2.1 Director v1** (SED §5.7). The full rules: free rounds allow
  2–3 names (silent-longest always, anyone named in the last round or
  in the listener's words, random fill) and 1–4 lines weighted to 2–3;
  one tone word per round; invitation (the story's `operator`, one
  line), answer (whole cast allowed, one line, "the character the
  voice addressed answers; if it addressed no one, whoever fits best
  answers", narrowed to an exact cast-name match), static ("Only static
  answers."); the cadence on played seconds. *To settle in the shape:*
  where the played seconds accumulate (a `played_s` per `Round`, summed
  since the last listening round?); where the tone-word list lives (the
  story folder, a default in code?); how the director tells the page to
  listen (a field on the `round` event?); the round kinds as data.
- **2.2 The trim** (SED §2.4 and its dated note). At 90 % of
  `context_budget`, flag whole middle rounds `trimmed` until 50 %;
  keep the cast sheet, the opening rounds, the recent rounds. *To
  settle:* how many opening and recent rounds to keep; how to know each
  round's share of the size (the difference between consecutive
  rounds' recorded `prompt_n + cache_n + predicted_n` is exact); then
  **measure the pause on the box** with `context_budget` near 3,000 —
  the number goes to lessons §4.10 question 3 as a dated note.
- **2.3 The debug switch** (lessons §4.9, §5). With `show.debug` on,
  each round writes `runs/<run-id>/debug/` — the messages sent, the
  grammar in full, the rendered prompt from `/apply-template`, the raw
  reply.
- **2.4 The STT client and the transcript filter** (SED §6.7).
  `app/services/stt_client.py`: empty text instead of the placeholder
  (line 85), `no_speech_prob`/`avg_logprob` returned, `prompt`/
  `language`/`vad_filter` passed; `app/show/listen.py`: the filter.
  *To settle:* how the confidence numbers reach the filter — the page
  sends the whole STT result with the round request, or the show gets
  its own transcribe route (SED §6.7 left it "settled in code").
- **2.5 The driver extended** — fake transcripts at invitations (one
  naming a character, one not), a silent window, the played seconds.
- **The checkpoint** (on the box, no browser): ten unattended rounds;
  speakers and budgets obeyed; an invitation then an answer from an
  injected transcript; a silent window giving the static round; the
  trim firing; debug files written. Verdict recorded in the TODO:
  continue · scale down (tone word and events first, then the cadence
  rules) · stop (fallback: TalkWithMe 7.1 + the canned episode).

### 7.3 Then

Slice 3 (the browser: SSE reader, `/show` page, accumulator,
hold-to-talk, the exit criterion by ear, tag `tz-0.2` and the
installer's pin); polish if the checkpoint was green; Tasks 5, 7, 8.
Owner-side: Task 4 (bibles → the cast entries of
`stories/lab-outbreak/cast_sheet.md`; voice samples, never committed);
the box's fate after the timebox. **At the session's end:** ask
permission to delete this handoff.

## 8. Nuances

- **The owner catches drift.** Suggestions of the agent's own became
  "facts" in later docs twice (lessons §2.8; `usage.prompt_tokens`).
  When a doc says "decided", check who decided it.
- **The owner reads the code** and asks about data modeling
  (Pydantic vs dataclass), persistence frequency, loop costs, and the
  wire. Point to the few lines that matter.
- **Explain with the real thing** — the owner loved seeing real SSE
  lines and real run output.
- **Byte-identical anchors** (grammar, cast sheet) are pinned by tests;
  any change to those texts loses the anchor — say so.
- **The owner's box habits:** hibernates at night, wakes it for a
  session; the address may change; `hosts.yml` gets re-wired.
- **The owner wants to run things personally** — keep runbooks current
  when a procedure changes.
- **Pronouns:** avoid pronouns for the owner in new writing.

## 9. My mistakes this session (do not repeat)

- **Proposed `stream_options.include_usage`** to make the wire fit the
  design text; check the wire first, fix the doc.
- **Let an unruled suggestion (normalize the history) become a TODO
  rule.**
- **Claimed "the file's shape won't change"** with a single `system`;
  episodes need one per episode — corrected before building.
- **The driver's first `--control` opened a run** (an empty record);
  a check must leave nothing behind — fixed.
- A draft of the driver carried dead variables (caught on re-read,
  before running). Re-read before running.
- A pytest summary hidden by `-q` output — re-ran to see "passed"
  rather than assume.
- **An address scan with an empty pattern** (after the owner unwired
  `hosts.yml`) listed every file in `docs/` — alarming and meaningless.
  Guard empty patterns.
- A scratch script importing the fork needs `PYTHONPATH=<fork>`.
- Earlier (09-23): a from-memory "verbatim", unchecked times and
  counts, chained requests after a failed probe, a pipe's exit code
  read as grep's, a cut heading in a scripted restructure, two reversed
  reuse proposals.

## 10. Operational gotchas

- **Fork tests:** `.venv/bin/python -m pytest -p no:cacheprovider`
  (then `grep passed`); `node tests/test_persona_form.js`,
  `node tests/test_tts_settings.js`; then
  `find app tests scripts -name __pycache__ -prune -exec rm -rf {} +`.
  One Starlette deprecation warning is normal.
- **The dev server:** from the fork's root,
  `.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8010`
  (background, log to the scratchpad); wait with
  `curl --retry 20 --retry-connrefused --retry-delay 1`; stop with
  `kill $(lsof -nP -iTCP:8010 -sTCP:LISTEN -t)` and re-check the port.
  The driver: `python3 scripts/drive_show.py --rounds 10`;
  `python3 scripts/drive_show.py --control`.
- **macOS/zsh:** `sed -i ''`; quote globs; `pipestatus` not
  `PIPESTATUS`; foreground `sleep` is blocked.
- **Verbatim extraction:** the transcript JSONL (§2); pick
  `message.content[].text` blocks by a distinctive phrase (LAST match);
  insert by script; assert presence. A missing bridging block is noted,
  never retyped.
- **The box:** `docker ps` shows `llama` and `whisper`; the TTS is the
  systemd unit `tts-faster_qwen3tts`.
- **Pre-commit ritual:** the address grep (§0.1 rule 5); a key-like
  scan of the diff; stage by explicit path; never `hosts.yml`.

## 11. Reading order after the compaction

1. This document, in full.
2. `git status -sb` and `git log --oneline -5` in both repositories;
   `gh pr view 2 --repo alfre2v/TalkWithZombies` and `gh pr view 10`
   (merged yet?).
3. `docs/TODO.md` — "Now", slice 2 and the checkpoint.
4. SED §5.7 (the director), §2.4 (the trim, with its dated note), §6.7
   (the listener's turn); lessons §4.9 (what the model reads).
5. The code (§4) — `app/routers/show.py` is the hub; the fork's
   `docs/runbooks/show-driver.md` for running it.

## 12. Paste-ready prompt

```
We continue the Zombie-Radio show engine's build (TODO Task 6b): slice 1
is done and closed, slice 2 is next. Re-orient before doing anything
else:

1. Read docs/discussions/2026-09-23-show-engine-session-handoff-2.md IN
   FULL — how we work (§0 is binding, including the live-box drill
   rules), the exact state (§2), the code as built (§4), the facts
   (§5), the rulings (§6), the board ahead with what slice 2's shapes
   must settle (§7), the nuances and your predecessor's mistakes
   (§8–§9), and the gotchas (§10).
2. Follow its reading order (§11) to confirm the state: git status and
   log in both repositories, whether PRs #2 (fork) and #10 are merged,
   and docs/TODO.md's "Now" and slice 2.
3. Then give me a compact summary: where the timebox stands (the
   clock), what is pending on my side (merges, the box), and the shape
   of step 2.1 as your first proposal — and wait for my go.

Standing rules: strict review-before-commit (I review uncommitted
changes in VS Code — no diffs in chat, no commits without my explicit
word), no AI attribution anywhere, no side panes, minimal code
comments, discussion-first, pushback with receipts welcome, plain
language, no delegation to other agents for now, and one question at
a time when I say I am tired.
```
