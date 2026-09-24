# Session handoff 3 — the show engine's build: slice 2 nearly done, 2.5 and the checkpoint next

> **EPHEMERAL.** Written 2026-09-24 ~18:30 CDT, mid-session, as a
> compaction-survival dump: the owner compacts the context deliberately
> (the window stood at 82 %) and then asks the agent to re-read this.
> It replaces handoff 2 (`2026-09-23-show-engine-session-handoff-2.md`),
> deleted with the owner's permission in the same commit. When the
> session that uses this one concludes, the agent **asks the owner for
> permission to delete it**.
>
> **Read it all; verify against the repos; receipts or nothing.** The
> TODO's "Now" section is the canonical state; this document carries
> what the TODO cannot: how we work, the code as built, the wire and
> box facts, today's rulings, the nuances, and the mistakes not to
> repeat.

## 0. The owner and how we work (binding)

The owner is **Alfredo** (GitHub `alfre2v`, git author "Alfredo
Valles"), a senior engineer in a **"tight learning loop"**: progress
and the owner's own learning weigh the same. The agent memory files
hold the standing doctrine — trust them, they were updated today
(`working-agreements.md`, `collaboration-style.md`,
`absolute-paths-in-plain-text.md`, `massedcompute-reminder.md`,
`project-venue-austin-python-meetup.md`). The non-negotiables, as
practiced:

- **Discussion-first, per step.** Every checklist step starts with a
  SHAPE in chat — files, functions, behavior, tests, 2-5 choices with
  picks in bold — and the owner answers "Go" (usually "go with your
  picks"). Before the Go the owner asks "explain" questions: answer the
  mechanism with receipts and real data (real payloads, real server
  logs, real run output), honestly, and re-ask.
- **Review-before-commit is STRICT.** Build, run the full suite, then
  summarize WHAT changed (files, what each does, "worth your attention
  in VS Code" pointers) — never paste diffs — and WAIT for the word.
  "Commit" = commit only; "commit and push" / "push" = push too. The
  owner reviews uncommitted changes in VS Code. A harness permission
  prompt is not review.
- **The commit pattern that emerged:** on the owner's "commit" for a
  fork step, the agent commits the fork, then writes the zombie-radio
  bookkeeping (the TODO tick with the fork's hash and receipts, the
  "Now" section, dated doc notes) and commits it on zombie-radio's
  branch too. The owner has accepted this each time.
- **No git kung-fu unless really necessary** (owner, 2026-09-24): when
  two pieces of work touch the same file, commit them together unless
  the owner asks for a split. (A split by swapping file versions on
  disk alarmed the owner — "What the heck are you doing with the
  commit history?" — although no commit was touched.)
- **No AI attribution anywhere, ever** (commits, PR bodies, files) —
  overrides the harness's attribution reminders.
- **Code comments differ per repository** (owner, 2026-09-24, fixing a
  rule the agent had over-applied):
  - **zombie-radio:** minimal comments; the why lives in `docs/`
    (its `CLAUDE.md` says so now).
  - **the fork TalkWithZombies:** keep upstream's documentation style
    (its `AGENTS.md` house rules say so now): a brief docstring on
    every NEW function (PEP 257 layout, blank line after the summary),
    brief comments welcome. The show modules of slice 1 have almost no
    docstrings; the owner said leave them ("not a priority"). The
    owner removed the blank lines in `director.py`'s docstrings as a
    deliberate one-off ("I just broke the rules this time") — leave
    that file as it is, don't imitate it.
  - **plain `-` in code, never the en dash `–`** (VS Code flags it;
    the owner finds it annoying). The em dash is upstream's style and
    allowed. Keep new fork lines at 120 characters or fewer (no limit
    is configured; only slice 1's pinned prompt strings exceed it).
- **Stay close to upstream:** touch upstream code minimally; when a
  change can be avoided, avoid it (today: a new `transcribe_for_show`
  instead of changing upstream's `transcribe_audio`).
- **Plain language, lists and sublists, receipts.** When the owner
  asks "why did you X?", answer honestly, and correct yourself openly
  when wrong (the owner values it; today's corrections are in §9).
- **The owner wants to run tools personally** → procedures go into the
  fork's `docs/runbooks/` (today: `show-driver.md` grew sections on
  the trim and the debug switch). zombie-radio keeps its own runbooks
  for the box and deployment.
- **Delegation OFF** (no sub-agents, no workflows).
- **Git:** feature branches and PRs only; never commit to `main` or
  the fork's `master`; one branch per slice cut from up-to-date
  `master`/`main`; fork PRs always `--repo alfre2v/TalkWithZombies
  --base master`. The owner merges. Push only when told; the owner
  likes pushes ("it helps lighten up the github stats"), PRs only
  when asked.
- **"Forget about the time constraint, let me worry about that"**
  (owner) — don't ration by the clock, but mention it when planning.
  When the owner says "tired": short answers, one question at a time.
- **Records of discussions:** agreed terms, rulings and measured
  numbers go into the docs the same day (TODO ticks, SED dated notes,
  lessons dated notes, follow-ups).
- **Rapport:** wit welcome; the owner jokes ("The day you see me
  propose this ... you can shoot me right there") and is warm ("Ok,
  good job!").

### 0.1 Live-box drill rules

1. **The OWNER owns the SSH tunnel, the box's power and deploys**
   (wake, hibernate, `make ans-set ENV=cloud IP=...`,
   `make ans-unset ENV=cloud`, `make ssh-tunnel ENV=cloud`,
   `make ans-deploy ENV=cloud`). The agent reaches the services only
   through `localhost:8080` (llama.cpp), `:8001` (tts-serve), `:8002`
   (Whisper), and inspects the box read-only over plain ssh.
2. **Box inspection: plain `ssh ubuntu@<box> '<cmd>'`** — no key
   paths, no `-o` options, and no other flags (the agent used `-n`
   once today and owned it); never list or cat under the owner's SSH
   directory. `<box>` is the address the owner gives in chat — never
   write it into a file.
3. **One line saying what a command does and why, BEFORE running it.**
4. **Probe the tunnel before any chain of requests**
   (`curl -s -m 3 -o /dev/null -w '%{http_code}\n' localhost:8080/health`;
   for STT/TTS work also `:8001/capabilities` and `:8002/docs`), **and
   wait for the answer before starting anything else** — on anything
   but 200, STOP and tell the owner (today the agent once started the
   app in parallel with the probe; the probe failed; no harm, but it
   broke the rule). Exit 7 / `000` = nothing listening (tunnel down);
   exit 52 = empty reply (the tunnel dying).
5. **No box address in any markdown, ever** (the never-commit hook
   skips `*.md`). Addresses live only in `hosts.yml` (`NEVER_COMMIT`,
   never staged). Pre-commit scan — see §10 for the script: the wired
   address (guarded: only while `hosts.yml` is wired), plus every IPv4
   address that appears in the session transcript, checked against the
   staged lines, printing counts only.
6. **Nothing changes on the box outside the playbook.**
7. **Temporary dev settings** (`show.context_budget: 1500`,
   `show.debug: true` in the fork's gitignored `settings.yaml`):
   back up first (the scratchpad holds `settings.yaml.before-trim`,
   identical to the committed state of the dev file: `show:` has only
   `seed: 42`), check with `cmp`, restore after, and say so.

## 1. The project in 60 seconds

**Zombie-Radio**: an interactive, audio-only radio play — four AI
scientists (Daniel, Moira, Ralph, Samantha) trapped in a lab during a
zombie outbreak, broadcasting on shortwave; listeners talk back with
hold-to-talk. Hard deadline **2026-10-08**; presented in a **talk at the
Austin Python Meetup in October 2026** ("hackTNT 2026" is only the
owner's internal label, not a hackathon).

The app is **TalkWithZombies**
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`), the owner's
fork of scorbo2's TalkWithMe 7.1. Its **show engine** is TODO Task 6b,
designed in `docs/discussions/2026-09-23-show-engine-design.md` ("SED",
seven decisions + today's §8 terms): one shared script as the model's
context, a director in code, a GBNF screenplay grammar per request, the
browser as the clock. The model services run on a rented Hyperstack
A6000 ("the box") behind the owner's SSH tunnel: llama.cpp (Nemotron
Nano 9B v2 Q4_K_M, 16k context, one slot, build `b11096`), tts-serve 1.2
(Faster Qwen3-TTS), Whisper (whisper-fastapi, model `small`).

**The arc** is "MVP prototype" (TODO header). Its deliverables: D1 the
deployment machinery (Ansible + Docker), D2 the running prototype, D3
the in-prototype experiment verdicts. The show engine was pulled into
this arc on 2026-09-21; story/episode authoring and the full demo
rehearsal belong to the next arc ("the show arc").

## 2. Exact state (2026-09-24, ~18:30 CDT)

- **The timebox (Task 6b):** started 2026-09-23 **14:46** · checkpoint
  **2026-09-25 02:46** (in practice that morning) · end **2026-09-26
  14:46**. At 18:26 on 09-24, about 27.7 of 72 hours were used.
  Slice 1 finished early on 09-24 (~02:30), well ahead of its target.
- **Slice 2 — the rules: 5 of 6 steps done.** 2.1, 2.1b, 2.2, 2.3, 2.4
  done and proven on the box; **2.5 is next (its shape is proposed and
  awaits the owner's Go — §7.1)**, then the checkpoint run.
- **The fork:** branch **`alfre2v/show-slice-2-rules`**, cut from
  `master` `4a62e18` (slice 1's merge). Commits since:

  | Hash | What |
  |---|---|
  | `ce8bd71` | 2.1 director v1 (four kinds, cadence, tone words) |
  | `22a0af2` | story content: 500 tone words, 289 events |
  | `3540d88` | house rules: upstream's documentation style |
  | `2f76b34` | 2.1b pacing knobs + the static round's new wording |
  | `35f34e0` | tone words don't repeat until the list is used up |
  | `57a08c9` | 2.2 the trim |
  | `129d3de` | 2.3 the debug switch |
  | `d6ab1b9` | 2.4 the listener's turn on the server — **not pushed** |

  Pushed up to `129d3de`. Suite **980 passed**; both Node tests pass.
  Working tree clean.
- **zombie-radio:** branch **`alfre2v/show-slice-2`**, cut from `main`
  `59ca874` (slice 1's merge). Commits: `51f14c8` (2.1 tick, 2.1b
  added, two follow-ups, comment rule scoped), `b36c28c` (image pins +
  dry-run fix), `038615e` (pins proven live, markdown emphasis
  follow-up), `124cf99` (2.1b tick, SED §8 terms, static wording
  note), `ce93f8d` (tone guard bookkeeping), `7031932` (2.2 tick,
  lessons 4.10 Q3, pauses follow-up), `2c3e5eb` (2.3 tick), `0c2db34`
  (2.4 tick, SED §6.7 note) — **`0c2db34` not pushed**, plus the commit
  carrying this handoff. `hosts.yml` is modified (wired by the owner) —
  NEVER stage it.
- **Slice 1 PRs** (#2 fork, #10 zombie-radio) were merged by the owner
  on 2026-09-24. No slice 2 PRs yet.
- **The box: UP**, woken by the owner in the afternoon after a failed
  wake (Hyperstack had no A6000 in stock — the "restore-stock lottery";
  `docs/runbooks/service-restart-sequence.md`: "Never hibernate a show
  box"). It came back **on the same address**. `hosts.yml` is wired.
  **The tunnel is up but drops** (at least three times today); the
  owner restarts it when told. Sanity (ssh, 14:36): A6000 visible,
  12.3 GB of 46 GB used, `llama` and `whisper` containers up, the TTS
  unit active, `/props` build `b11096-c550d2f60`.
- **Image pins are live** (`b36c28c`, proven by the owner's deploy at
  ~15:02: `changed=2`, then an idempotency run `changed=0`): llama.cpp
  `ghcr.io/ggml-org/llama.cpp:server-cuda-b11096` (digest
  `sha256:0192ab2545ef...`), Whisper
  `docker.io/heimoshuiyu/whisper-fastapi@sha256:e6ea4a5ca181...` (the
  `latest` of 2025-12-28; no version tag names it). Dry runs work
  (`make ans-deploy ENV=cloud ANS_ARGS="--check --diff"`), with one
  known false alarm (the torch pip task reports "changed").
- **The dev clone (the fork)** holds, gitignored: `settings.yaml`
  (tunnel ports; `general.personas_directory:
  /Users/alfredo/TalkWithZombies-client/Personas`; `show:` only
  `seed: 42`, restored after every experiment) and `runs/` with today's
  records: `2026-09-24T02-18-51` (slice 1's first run),
  `T14-43-54` (2.1 live), `T15-57-21` and `T16-05-03` (2.1b and the
  static wording), `T17-12-04` and `T17-15-15` (the trim measurement,
  budget 1500, identical drives), `T17-37-14` (2.3 debug on, 16 rounds,
  `debug/` folder), `T17-59-32` (a failed listen loop — one invitation
  only, junk), `T18-01-23` (2.4's live loop). No dev server is running.
- **Scratchpad** (`/private/tmp/claude-501/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18/scratchpad/`,
  temporary): `listen_loop.py` (2.4's live loop: TTS -> listen ->
  round; reusable for 2.5), `build_tones.py` / `build_events.py` (the
  story generators), `settings.yaml.before-trim` (the dev settings
  backup), drive outputs (`drive-*.txt`), dev-server logs, `q.wav`
  (a `say`-made "Moira, is the virus airborne?"). The session
  transcript:
  `/Users/alfredo/.claude/projects/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18.jsonl`.
- **Agent memory** was updated today: comment rules per repo and the
  docstring layout (`collaboration-style.md`), "no git kung-fu"
  (`working-agreements.md`). A temporary "image pins live test"
  reminder was created and deleted (the test happened).

## 3. What this session did (2026-09-24)

1. **Early hours (00:06-02:49):** slice 1 finished — 1.4 parser, 1.5
   record and assembler, 1.6 director v0, 1.8 endpoints, 1.9 driver
   and the first real run; the fork's first runbook. Handoff 2 written.
2. **After the owner's compaction (from 12:17):** re-orientation;
   slice 1 PRs merged; slice 2 branches cut.
3. **2.1 director v1** — shaped (picks a-e), built, a live drive
   (invitation at round 8, static at 9, as computed offline).
4. **Story content at the owner's creative request** — 500 tone words
   in 24 groups (the 2024 list pruned to 25 and extended), 289 events
   in 14 groups (the gate's 10 + 279).
5. **Comment rule scoped** — zombie-radio minimal, the fork upstream's
   style; docstrings added to `director.py`.
6. **Two follow-ups** — the "exchange" round; events that stay on
   topic (semantic neighbors or topic runs).
7. **2.1b pacing knobs** (events every 2+/-1 free rounds, tone words
   held 3+/-1 rounds) and **the static round's wording**; live-proven
   twice; **SED §8** terms (gap, hold, jitter; "stretch" retired) with
   a script-built timeline.
8. **The tone-repeat guard** (`_fresh`, shared with events).
9. **The box saga:** the A6000 was out of stock, then woken; sanity
   check; **image pins** (llama.cpp tag, Whisper digest); the **dry
   run fixed** (six read-only tasks `check_mode: false`); live deploy
   and idempotency proven.
10. **Markdown emphasis** — the model wrote "How \*charming\*."; the
    owner's TTS listening test (three WAVs sent to the owner) ranked
    the marked lines more natural; kept; per-engine replacement tables
    noted for a future TTS engine change.
11. **2.2 the trim** — middle-out (the owner's order); measured: the
    pause is the server's slot swap (~1.5 s), found on the owner's
    hunch after the agent first got it wrong; lessons 4.10 Q3 answered;
    a follow-up for pauses the timings don't show; an idle-unload
    hypothesis (the owner's) ruled out.
12. **2.3 the debug switch** — with a token check proven exact.
13. **2.4 the listener's turn** — the show's listen route, the filter,
    live mouth to ear (TTS -> Whisper -> Moira answers; silence ->
    static).
14. **2.5 shaped** (awaiting Go), then this handoff.

## 4. The code as built (the fork, slices 1 and 2)

**Conventions:** Pydantic for data that crosses a boundary (disk,
HTTP): `Run`, `Round`, `Line`, `Heard`, the API models; frozen
dataclasses for in-memory values: `Story`, `ScriptLine`, `RoundPlan`.
Paths resolved at call time from `app.config._PROJECT_ROOT` (the test
isolation fixture needs nothing new). Upstream's rules: new routes in
`AGENTS.md`'s endpoint table (checked by `tests/test_docs.py`); stubs at
the router's import site; one test module per module.

- **`app/config.py` — `ShowConfig`** (`show:`, yaml-only, carried over
  on Settings-dialog saves): `story="lab-outbreak"`, `episode=None`,
  `model_prefix="/no_think"`, `max_tokens=512`, `context_budget=14000`,
  `seed=None`, `emotion_tags=True`, `debug=False`, **`event_every=2`,
  `event_jitter=1`, `tone_hold=3`, `tone_jitter=1`** (0 turns events or
  tone words off), `interaction_min_s=60`, `interaction_max_s=180`,
  `listen_window_s=10`, `press_cap_s=30`, `no_speech_max=0.6`,
  `logprob_min=-1.0`, `stt_language="en"`.
- **`app/show/grammar.py`** — `MOODS` (calm, happy, sad, afraid,
  terrified, doubtful, angry, urgent, exhausted);
  `build_grammar(speakers, max_lines, moods=None)` (the proven GBNF,
  byte for byte; text excludes `\n [ ] ( )` — `*` and `_` pass).
- **`stories/lab-outbreak/`** — `cast_sheet.md` (front matter `title`,
  `cast: [Daniel, Moira, Ralph, Samantha]`, `operator: Samantha`; Jinja
  body), `events.yaml` (289, the gate's 10 first, group headers are
  YAML comments — the loader reads a flat list), `tones.yaml` (500 in
  24 groups; optional file — no file, no tone words).
- **`app/show/story.py`** — `Story(name, title, cast, operator,
  template, events, tones=())`; `load_story`; `_load_tones` (optional);
  `format_rules`; `render_cast_sheet`.
- **`app/show/parser.py`** — `LineParser`: `raw` for the history,
  `spoken` for the voice (`_SPOKEN`: curly quotes, em dash to ", ",
  ellipsis to "..."). `*` and `_` are NOT replaced (owner's ruling).
- **`app/show/script.py`** — `Line`; **`Heard(text, no_speech_prob,
  avg_logprob, silence)`**; `Round` (n, **kind** free/invitation/
  answer/static, **played_s** — the running total the request
  reported, instruction, listener, **heard**, speakers, max_lines,
  event, **tone**, lines, dropped, timings {prompt_n, cache_n,
  predicted_n}, finish_reason, trimmed, **tokens** — the round's share
  of the size, **trims** — rounds flagged just before it, episode);
  `Run` (run_id, started, story, cast, moods, seed, systems per
  episode, episode, rounds). `new_run`, `save_run` (atomic),
  `load_run`, `append_round`, `reply_text`, **`script_size`** (last
  round's prompt_n + cache_n + predicted_n), **`trim(run, budget)`**
  (at 90 % flags the middle candidate again and again until <= 50 %;
  candidates = rounds the model reads except the first 2 and last 4;
  returns the sorted flagged numbers), **`round_share`**,
  `assemble_messages` (skips trimmed, line-less, other-episode rounds).
- **`app/show/director.py`** — `RoundPlan(kind, speakers, max_lines,
  event, tone, listener, instruction, grammar)`;
  **`plan_round(run, story, show, played_s, transcript)`**, pure,
  seeded `random.Random(f"{seed}:{n}")`:
  - after an invitation: words -> **answer** (`_answer`: whole cast,
    1 line; cast names found in the words, whole word and exact case,
    narrow it — `names_in`), none -> **static** (`_static`, the
    operator, 1 line, "Only static answers; the broadcast goes on.");
  - otherwise the **cadence** (`_time_to_listen`: seconds since the
    last invitation's `played_s`; never below min, always at max,
    linear chance between) -> **invitation** (`_invitation`, the
    operator, 1 line) or **free** (`_free`: silent-longest + named in
    the last round + random fill, 2-3 names, budget 1-4 weighted
    1:3:3:1; an event when its gap has passed — `_event_due`; the tone
    of the hold — `_tone`);
  - `_drawn(seed, what, start, mean, jitter)` — a gap's or hold's
    length, seeded by where it began; `_fresh(pool, used)` — no
    repeats until the pool is used up (events and tone words);
  - `instruction_for(speakers, max_lines, event, moods, tone)`.
- **`app/show/listen.py`** — `usable(text, no_speech_prob,
  avg_logprob, show)` -> (words, None) or (None, reason): "nothing
  heard" (<= 1 character after normalizing), "no speech
  (no_speech_prob ... > 0.6)", "an unsure reading (avg_logprob ... <
  -1.0)", "a known Whisper hallucination" (`_KNOWN_NOISE`: thank you,
  thanks for watching, subtitles by the amara org community, you,
  upstream's placeholder, ...). Missing numbers skip their checks.
- **`app/show/debug.py`** — `write_round(...)`: `runs/<run-id>/debug/
  rNNN.txt` (numbers, token check, listener line, error, grammar, the
  prompt as the model read it, the reply as it streamed) and
  `rNNN.request.json`; never raises.
- **`app/services/llm.py`** — `stream_chat` = upstream's code;
  **`round_payload`** (the round's request body), **`stream_round`**
  (tokens, then {timings, finish_reason}), **`render_prompt`**
  (`/apply-template`), **`count_tokens`** (`/tokenize`, add_special and
  parse_special on).
- **`app/services/stt_client.py`** — upstream's `transcribe_audio`
  untouched; **`transcribe_for_show(audio, mime, *, prompt,
  language)`**: `response_format=json` (NOT verbose_json — see §5),
  `vad_filter=true`; returns {text, no_speech_prob (max), avg_logprob
  (mean)} or None; logs the server's error body.
- **`app/routers/show.py`** — `_load(run_id)` (404/422);
  **`POST /api/show/start`**; **`POST /api/show/listen`**
  (`{run_id, audio_base64, audio_mime_type}` -> {text, no_speech_prob,
  avg_logprob}; prompt = cast names joined, language =
  show.stt_language; 503/400/404/502); **`POST /api/show/round`**
  (`{run_id, played_s, transcript?, no_speech_prob?, avg_logprob?}`)
  -> `_round_stream`: filter the transcript (only after an invitation;
  otherwise warn "outside a listening window; ignored") -> measure ->
  trim -> plan -> assemble -> stream (`start` +mood +message_id,
  `token`, `done`) -> record the Round -> debug files if on -> `round`
  event {n, kind, speakers, event, tone, trimmed, dropped,
  finish_reason} -> `complete`. Errors: `error` + `complete`, nothing
  recorded (debug file written with the error).
- **`app/models.py`** — `ShowStartRequest/Response`,
  `ShowRoundRequest` (+ the two numbers), `ShowListenRequest`,
  `ShowListenResponse`.
- **`scripts/drive_show.py`** (stdlib only) — `--base` (8010),
  `--llm`, `--rounds`, `--story`, `--played` (seconds per round; the
  app receives the running total), `--runs-dir`, `--control`,
  `--run-id`; prints each line, a round summary (kind, speakers, event,
  tone, dropped, finish, first-line time) and "trimmed before this
  round: ..." lines; totals at the end.
- **`docs/runbooks/show-driver.md`** — what you need, the settings,
  play rounds, the trim note, "Look inside a round (the debug
  switch)", the control check, troubleshooting.
- **`AGENTS.md`** — house rules at the top (incl. upstream's
  documentation style); the endpoint table has the three show routes.
- **Tests** (980 in all): `test_show_config.py`, `test_show_grammar.py`,
  `test_show_story.py` (pinned prompts byte for byte; counts 289/500),
  `test_show_parser.py` (the real 42-token recording),
  `test_show_script.py` (record, assembler, `TestTrim`),
  `test_show_director.py` (every kind, free rules, `TestPacing`,
  cadence, listener turn, names, wording), `test_show_listen.py`,
  `test_show_debug.py`, `test_routers_show.py` (start, round, listener
  turn, transcript filter, listen route, trim, debug), plus additions in
  `test_llm.py` and `test_tts_stt_clients.py`.

## 5. Facts and numbers (measured 2026-09-24 unless noted)

- **Round share:** each round adds 51-121 tokens to the script (about
  80); the cast sheet is about 260 tokens; the script is about 395
  tokens after round 1. A 40-minute show (~120 rounds at 20 s of audio
  each) would reach ~10,000 tokens.
- **Determinism:** the same seed replays a drive word for word (rounds
  1-8 identical across drives; the llama seed is `run.seed + n`).
- **Cadence:** at 20 s of audio per round and 60/180, invitations come
  115.0 s apart on average (80 min, 180 max; 2,000 simulated seeds).
  Seed 42: invitations at rounds 8 and 13, statics at 9 and 14.
- **Pacing (live, seed 42):** gaps of 1, 3, 2, 2 free rounds; holds of
  2, 4, 3, 4 rounds; the churn gone; the tone word also steers the
  emotion tags ("tremulous" -> 6 x terrified).
- **Tone repeats:** without the guard 78 % of simulated 40-minute
  shows (~40 words each) repeated a word; with it, none of 300.
- **The trim** (budget 1500, 28-round drives): trims before rounds 14
  (rounds 3-9) and 22 (10-17). The re-read is small (the cache reused
  512 of 516 tokens up to the cut; 308-316 tokens read in 453-474 ms vs
  ~365 ms normally), but **the slot swap between "selected slot" and
  "launch_slot" costs 1.3-1.5 s** in 3 trims of 4 (f_keep 0.37-0.38);
  a new run's first round pays 1.1-1.4 s (f_keep 0.22); the next round
  is normal (~1 ms). The one 174 ms trim is believed restored from the
  host-RAM cache (its prompt identical to an earlier drive's): **identical
  repeat drives understate a trim's cost**. At the default budget the
  first trim comes ~50 minutes into a show, then ~every 25 (estimates).
- **One stall of 1.5 s before a request reached the server** (round 8,
  first trim drive only); cause unknown; the idle-unload knob
  (`--sleep-idle-seconds`) exists but defaults to -1 (off) and the box
  doesn't set it. Tunnel round trip ~170 ms per new connection (max
  440 ms in 40 tries); on the box ~0.
- **Server prompt eval has a floor of ~360-375 ms per request** (90 to
  186 fresh tokens).
- **The token check:** `/tokenize` of `/apply-template`'s rendering
  (add_special + parse_special) equals `prompt_n + cache_n` to the
  token (7 rebuilt rounds; 16 live rounds with a trim). `/apply-template`
  and `/tokenize` take ~130-170 ms each and don't use the slot. A debug
  round costs ~0.35 s more.
- **Rebuilding a past round's exact request** from the record: use
  `trims` (which rounds had been trimmed by then), not the final
  `trimmed` flags (those reflect the end state).
- **Whisper (whisper-fastapi):** `response_format=json` already carries
  `segments` with `no_speech_prob` and `avg_logprob`;
  **`verbose_json` is rejected** (400, `"Invailed response_format"`).
  `prompt`, `language`, `vad_filter` all accepted. The cast-names
  prompt raised confidence on the same clip (no_speech_prob
  0.018 -> 0.005, avg_logprob -0.24 -> -0.19). The live loop:
  "Moira, is the virus airborne?" (TTS, Samantha's voice) -> heard
  "Moira is the virus airborne" in 0.33 s (0.010 / -0.30); 2 s of
  silence -> "" with no segments.
- **TTS:** `/api/tts` {text, persona_name} -> {audio_base64 (WAV),
  sample_rate 24000}; ~1.8-2.8 s per short line. The personas'
  reference voices are `say`-made placeholders (they sound poor).
- **Markdown emphasis:** the model wrote `*charming*`, `*alive*` (both
  with the tone "impish"); nothing strips them before the voice.
- **Static round** with the bare "Only static answers." signed off in
  both drives ("This is a dead end.", "Farewell, dear listeners...");
  with "; the broadcast goes on." it continued ("We'll keep
  broadcasting.").
- **Box:** A6000, driver 550.90.12 (CUDA 12.4), disk 44 % used, GPU
  12.3 GB in use at idle; llama container args `-hf ... --host
  127.0.0.1 --port 8080 -ngl 99 -c 16384 --parallel 1`; the app's 5
  startup warnings (4 personas without `language.txt`, cleartext http)
  are normal.
- **Hyperstack prices** (survey 2026-09-13): A6000 $0.50/h, L40
  $1.00/h (48 GB like the A6000).

## 6. Rulings today (the owner's)

- **2.1:** `played_s` is a running total; tone words from the story's
  optional `tones.yaml` ("Let the tone be: X."); names matched whole
  word, exact case; the static round is the operator's one line; the
  page learns to listen from `kind` on the `round` event.
- **Story content:** 500 tone words / 289 events (agent's creative
  pass, owner-requested); the palette note (group size = how often a
  color comes up).
- **Comments per repo; docstrings in the fork; plain `-`** (§0).
- **2.1b:** hold (not spacing out) for tone words; bounded jitter drawn
  once per gap/hold; defaults events 2+/-1, tones 3+/-1; the first free
  round opens with an event; the tone knob named `tone_hold`.
- **Terms:** gap, hold, jitter; "stretch" retired (SED §8).
- **Static wording:** "Only static answers; the broadcast goes on."
- **Tone-repeat guard:** yes (the events' rule shared).
- **No git kung-fu.**
- **Image pins:** yes, llama.cpp and Whisper; test live — done.
- **Dry-run fix:** attempted with a budget of 3 errors — fixed with 0.
- **Markdown marks:** kept (the owner's ear preferred them); per-engine
  replacement tables if a future engine mishandles them.
- **2.2:** share recorded from timings; keep first 2 / last 4 as
  constants; **middle-out order (the owner's)**; visibility on record,
  event and driver; the measurement budget 1500 (the owner allowed
  adjusting and repeating measurements freely: "we have the VM
  precisely for this").
- **A periodic `/tokenize` drift check:** not needed (the accounting
  self-corrects); the check lives in the debug switch.
- **2.3:** a readable text file + the exact request JSON; the token
  check included; files written after the round; failed rounds too.
- **2.4:** the show's own listen route with the filter in the round;
  a new client function, upstream's untouched; the cast's first names
  as the prompt; the noise list in code; `heard` recorded.
- **Follow-ups recorded today** (zombie-radio `docs/follow-ups.md`):
  "An exchange round", "Events that stay on topic for a few rounds"
  (idea 1 semantic neighbors, idea 2 topic runs), "Markdown emphasis
  in spoken lines" (with per-engine tables), "Pauses the model
  server's timings do not show" (slot swap: try `--cache-ram 0`;
  pre-server stall: time the app's request phases).

## 7. The board ahead

### 7.1 NEXT: step 2.5 (shape proposed, awaiting the owner's Go)

**The driver, extended** — what the checkpoint needs. As proposed:

- `--heard "Moira, is it airborne?" --heard - --heard "..."`: each
  invitation takes the next item in turn; `-` = a silent window (no
  transcript -> static); no `--heard` = all windows silent (today's
  behavior).
- **How the words get in:** by default as text straight into the next
  round request; **`--speak`** sends them through the real path (the
  app's `/api/tts` speaks the line, `/api/show/listen` transcribes it,
  the result goes into the round request — the code exists in the
  scratchpad's `listen_loop.py`).
- Prints: kind per round; on an answer `listener: "..."`; on a static
  round `heard: "..." -> silence: <reason>`.
- **`heard` on the `round` SSE event** (text and verdict) — the driver
  prints it now; the page needs it for its debug-only "Heard: ..." in
  slice 3.
- **`--report`**: after the drive, read the record and the debug
  folder and print each checkpoint criterion pass/fail: every line's
  speaker allowed and no round over its budget; an invitation answered
  from the injected words and one gone static from silence; a trim
  fired; every round has its debug files and every token check says
  `difference 0`.
- **The checkpoint's settings** (`debug: true`, `context_budget: 1500`)
  set by hand in the fork's `settings.yaml`; the runbook gains "Run the
  checkpoint" with the exact settings and command.
- Picks: a text by default + `--speak`; b `heard` on the event; c
  `--report`; d settings by hand. About an hour (estimate).

### 7.2 Then: the checkpoint (TODO, "Checkpoint — 2026-09-25")

On the box, no browser: ten unattended rounds; speakers and line
counts obey the director; an invitation, then an answer from an
injected transcript; a silent window giving the static round; the trim
firing; the debug files written. **Verdict recorded in the TODO:**
continue · scale down (the tone word and the events first, then the
cadence rules — keep the microphone, simplify when it opens) · stop
(the fallback: TalkWithMe 7.1 + the canned episode). Most criteria are
already shown piecemeal today; the checkpoint shows them together in
one run.

### 7.3 Then: slice 2 PRs, slice 3, the rest

- **Slice 2 PRs** (fork and zombie-radio) — the owner reviews and
  merges; push first (unpushed: fork `d6ab1b9`, zombie-radio `0c2db34`
  and the handoff commit).
- **Slice 3 — the browser** (branch `alfre2v/show-slice-3-browser`,
  target the end of the timebox, 2026-09-26 14:46) — **the biggest
  remaining risk, the least explored**: 3.1 the SSE reader extracted
  from `sendMessage` into `static/sse.js`; 3.2 the `/show` page and
  `show.js` (idle -> generating -> playing -> listening; next round on
  drain, with the played seconds; listen only when the director asks
  — i.e. after `kind == "invitation"`); 3.3 the accumulator in
  `static/tts.js` (~100 characters, whole sentences, ~20 % tail
  tolerance, flush at line end); 3.4 hold-to-talk (press to record,
  release to end; the waiting window stops on a press; the press cap;
  upload to `/api/show/listen`; send the result with the next round;
  "Heard: ..." only while debug is on); 3.5 the exit criterion by ear
  (ten unattended turns, one interaction beat, sentences not split);
  3.6 close the timebox (tag `tz-0.2`, the installer's pin bumped and
  re-proven, the spec's as-built entries).
- **Polish, only if the checkpoint is green:** dead-air static; the
  1930s look with the owner's gauge; prefetch round N+1; episodes.
- **After the timebox:** Tasks 5a/5b/5c in the new engine (5a needs
  the owner's character bibles, 5b the voice samples) -> Task 7, the
  canned episode (a MUST for the talk) -> Task 8, the close ritual.
- **Owner-side, any time:** Task 4 — the character bibles (they become
  the cast entries of `stories/lab-outbreak/cast_sheet.md`) and the
  voice samples (never committed). The box's fate after the timebox
  (keep hibernating vs destroy; never hibernate during demo week).
- **At the session's end:** ask permission to delete this handoff.

### 7.4 Challenges of this arc (the ones to keep in view)

- **Slice 3 is browser work** — audio queues, MediaRecorder, drain
  timing, the SSE reader shared with the chat — none of it explored
  in this arc yet.
- **Pacing by ear** — the knobs exist (event_every, tone_hold, the
  cadence, max lines); their right values will only be found by
  listening in slice 3.
- **Hidden pauses** — the trim's ~1.5 s slot swap, the first-round
  swap of a new run, the occasional pre-server stall; the tunnel adds
  ~170 ms per request and drops now and then.
- **Voices** — the placeholder `say` voices sound poor; real samples
  are the owner's Task 4/5b.
- **The model's writing** — characters rarely name each other (the
  "exchange" follow-up); markdown emphasis; lore drift across random
  events; all tolerable for the MVP.
- **Box availability** — the A6000 stock lottery; the L40 fallback;
  the images are now pinned so a fresh box behaves the same.

## 8. Nuances (hard to get from the docs alone)

- **The owner catches drift and tests claims.** Examples today: "Why
  `sorted`? Does `in` use it?" (no), "don't n values change after
  trim?" (no — flags only), "what is a stretch?" (casual — renamed),
  "why did you remove commits?" (none removed). Answer with receipts;
  admit errors plainly.
- **The owner's hunches are often right** — "cache ejected from
  memory" found the trim's real pause. Take them seriously and test
  them against the server log.
- **Live checks catch what unit tests can't** — the Whisper
  `verbose_json` error was invisible to tests that faked the server
  the way the agent believed it behaved.
- **Explain with the real thing** — the owner loved real SSE lines,
  real run output, the server log table, the WAV files.
- **Byte-identical anchors** (the grammar, the cast sheet prompts) are
  pinned by tests; changing those texts loses the anchor — say so.
- **Records:** `trimmed` flags are end-state; `trims` tells when; the
  director's memory reads all rounds (trimmed included).
- **Background app tasks end with "exit code 144"** when the agent
  kills the dev server — expected; say so briefly.
- **The tunnel drops** — on `000`/exit 7/exit 52, stop and ask the
  owner to restart it; the box itself is usually fine (check over
  ssh).
- **Seed 42 in the dev settings** makes drives repeatable; for timing
  measurements, beware the host-RAM cache remembering identical
  prompts from earlier drives.
- **Pronouns:** avoid pronouns for the owner in new writing (use "the
  owner").
- **The MassedCompute reminder** (memory): remind about the 50 % code
  after each *experiment* PR merges — none today.

## 9. The agent's mistakes today (do not repeat)

- **A hand-drawn ASCII timeline mislabeled a hold** ("wry, hold 2"
  shown on three rounds) — build diagrams from the rules by script.
- **Git kung-fu** — splitting commits by swapping reviewed files on
  disk; correct history, but it alarmed the owner. Commit together.
- **"A trim costs 0.1-0.2 s"** — read only prompt-eval time and missed
  the select->launch phase; the owner's hunch corrected it. Read the
  whole server-side timeline before concluding.
- **Assumed Whisper needs `verbose_json`** (true for OpenAI, false for
  our server) and faked the server that way in the unit test — the
  live loop caught it. Probe the real server before designing on it.
- **Started the app in parallel with the tunnel probe** — sequence
  them.
- **Used `ssh -n`** — plain ssh only.
- **Suggested a dry run without checking the playbook's check-mode
  support** — read the roles first.
- **Over-applied "minimal comments" to the fork**, omitted docstrings,
  and used en dashes.
- **Rebuilt past rounds with end-state `trimmed` flags** — wrong
  prompts at first; use `trims`.
- **Dead code in a test fixture** (`calls.reply` on a list) — re-read
  before running.
- **Casual terms leaking into design** ("stretch"; `tone_every` for a
  hold) — name things precisely.
- **Tool-call slips:** zsh `eval` quoting, wrong awk columns, `git
  rev-parse` with two revisions, `grep -P` on macOS, Edit on a file
  created by a shell command without reading it first.
- **Confusing counts** ("3 unpushed commits" when there were 2).

## 10. Operational gotchas and commands

- **Fork tests:** `.venv/bin/python -m pytest -p no:cacheprovider`
  (grep `passed` — `-q` hides the summary); `node
  tests/test_persona_form.js`, `node tests/test_tts_settings.js` (grep
  `^ℹ (pass|fail)`); then `find app tests scripts -name __pycache__
  -prune -exec rm -rf {} +`. One Starlette deprecation warning is
  normal.
- **The dev server:** from the fork's root, background:
  `exec .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8010 >
  <scratchpad>/dev-server-8010-<name>.log 2>&1`; wait with `curl -s -o
  /dev/null -w '%{http_code}' --retry 20 --retry-connrefused
  --retry-delay 1 http://127.0.0.1:8010/`; stop with `kill $(lsof -nP
  -iTCP:8010 -sTCP:LISTEN -t)` and re-check the port.
- **The driver:** `python3 scripts/drive_show.py --rounds 14`;
  `--control` for the grammar check (no app needed).
- **The listen loop** (2.4's live check, reusable):
  `python3 <scratchpad>/listen_loop.py` from the fork's root with the
  app up.
- **Ansible (zombie-radio):** `make ans-lint` (limit 160 characters per
  line); `make ans-check-syntax ENV=cloud`; deploys are the owner's:
  `make ans-deploy ENV=cloud [ANS_ARGS="--check --diff"]`; logs in
  `~/.config/zombie-radio/logs/cloud-deploy-<stamp>.log`.
- **Reading llama.cpp's side:** `ssh ubuntu@<box> 'docker logs --since
  25m llama 2>&1 | grep -E "get_availabl|launch_slot_|release:|prompt
  eval time"'` — timestamps are minutes.seconds.ms since the server
  started; `selected slot by LCP similarity, f_sim_best, f_keep`;
  select->launch > ~100 ms = a slot swap.
- **Whisper by hand:** `curl -s localhost:8002/v1/audio/transcriptions
  -F "file=@x.wav;type=audio/wav" -F response_format=json -F
  vad_filter=true -F "prompt=Daniel, Moira, Ralph, Samantha" -F
  language=en` (make a WAV with `say -o x.aiff "..."` then `afconvert
  -f WAVE -d LEI16@24000 x.aiff x.wav`).
- **The pre-commit address scan** (zombie-radio; prints counts only):
  `ip=$(grep -oE '[0-9]+(\.[0-9]+){3}'
  deploy/ansible/inventories/cloud/hosts.yml | head -1)`; if `[ -n
  "$ip" ]`, `git diff --cached | grep '^+' | grep -cF "$ip"` must be
  0; plus a Python check of every IPv4 found in the session transcript
  against the staged `+` lines (must be 0); plus a key-like scan
  (`sk-...`, `BEGIN ... PRIVATE`, `password =`); stage by explicit
  path; `hosts.yml` never staged.
- **macOS/zsh:** `sed -i ''`; quote globs (no-match globs error out);
  no `eval`-built argument lists; `git rev-parse` one revision per
  call; foreground `sleep` is blocked; system `python3` lacks `yaml`
  (use the repo's `.venv/bin/python`).
- **Editing:** a file created or changed by a shell command must be
  read with the Read tool before the Edit tool will touch it.

## 11. Reading order after the compaction

1. This document, in full.
2. `git status -sb` and `git log --oneline -10` in both repositories
   (the fork: `alfre2v/show-slice-2-rules`; zombie-radio:
   `alfre2v/show-slice-2`); what's unpushed.
3. `docs/TODO.md` — "Now", the slice 2 checklist (2.1-2.4 ticked with
   receipts, 2.5 open), the checkpoint, slice 3.
4. SED (`docs/discussions/2026-09-23-show-engine-design.md`) §5.7 (the
   director), §6.7 (the listener's turn, with today's dated note), §8
   (the timeline terms), **§9 (why slice 2 was built this way — the
   owner's words verbatim, step by step)**; lessons
   (`docs/discussions/2026-09-22-grammar-and-prompt-cache-lessons.md`)
   §4.10 question 3 (the trim's pause).
5. `docs/follow-ups.md` — today's four entries.
6. The code (§4) — `app/routers/show.py` is the hub; the fork's
   `docs/runbooks/show-driver.md` for running it.
7. Then report to the owner and continue with 2.5 (§7.1) on the
   owner's Go.

## 12. Paste-ready prompt

```
We continue the Zombie-Radio show engine's build (TODO Task 6b): slice 2
is 5 of 6 steps done (2.1, 2.1b, 2.2, 2.3, 2.4); step 2.5 — the driver,
extended — is shaped and waits for my Go; then the checkpoint. Re-orient
before doing anything else:

1. Read docs/discussions/2026-09-24-show-engine-session-handoff-3.md IN
   FULL — how we work (§0 is binding, including the live-box drill
   rules in §0.1), the exact state (§2), what we did today (§3), the
   code as built (§4), the facts and numbers (§5), today's rulings
   (§6), the board ahead with 2.5's proposed shape and the arc's
   challenges (§7), the nuances and your mistakes today (§8-§9), and
   the gotchas (§10).
2. Follow its reading order (§11) to confirm the state: git status and
   log in both repositories (what is unpushed), docs/TODO.md's "Now",
   slice 2 and the checkpoint.
3. Then give me a compact summary: where the timebox stands (the
   clock), what is pending on my side (the box, the tunnel, pushes,
   PRs), and 2.5's shape as proposed (the picks) — and wait for my go.

Standing rules: strict review-before-commit (I review uncommitted
changes in VS Code — no diffs in chat, no commits without my explicit
word), no AI attribution anywhere, discussion-first, pushback with
receipts welcome, plain language, no delegation to other agents, one
question at a time when I say I am tired, no git kung-fu, and code
comments per repository (minimal in zombie-radio; upstream's docstring
style in the fork).
```
