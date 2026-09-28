# Session handoff 6 — the show engine's slice 3: step 3.4c done through fixed lines; the owner's prompt sweep under way; the timebox ends today

> **EPHEMERAL.** Written 2026-09-28 ~12:15 CDT (Monday, the timebox's
> last day), at about 90 % of the context window, before a manual
> compaction the owner triggers; after it, the agent re-reads this first.
> It supersedes handoff 5 (`2026-09-26-show-engine-session-handoff-5.md`),
> which is now **stale** — do not read it as current state. Both
> handoffs were written in this session: at the session's end, ask the
> owner's permission to delete **both** (the owner's rule: "These handoff
> documents stay in our discussion folder until the end of the session,
> when we finish the session's work please ask the owner for permission
> to delete any handoff documents you created.").
>
> **Read it all; verify against the repos; receipts or nothing.** The
> TODO's "Now" section and its step 3.4c entry are the canonical state;
> the two discussions of 2026-09-28 (`narration-quality-challenges`,
> `prompt-sweep`) hold today's substance. This document carries what they
> cannot: how we work now (and what changed today), the exact state, the
> board ahead with what is pending on the owner's side, the nuances, the
> mistakes not to repeat, and the working techniques.

## 0. The owner and how we work (binding)

The owner is **Alfredo** (GitHub `alfre2v`, git author "Alfredo
Valles"), a senior engineer in a **"tight learning loop"**: progress and
the owner's own learning weigh the same. The agent memory files hold the
standing doctrine (`working-agreements.md`, `collaboration-style.md`,
`absolute-paths-in-plain-text.md`, `massedcompute-reminder.md`,
`project-venue-austin-python-meetup.md`). The non-negotiables, as
practiced — **today's additions in bold**:

- **Discussion-first; one decision at a time, each with its context**
  (what it is, what it fixes, how it connects, what it touches), then a
  lean and one question.
- **Plans are made in discussion, never improvised.** Cite a settled
  ruling before re-opening it.
- **Review-before-commit is strict:** a commit needs the owner's explicit
  order for that commit, given after the changes exist ("commit the fork,
  then commit zombie-radio" orders both). **For this handoff the owner
  said: "After you create said document, go ahead and commit all changes.
  I will review it when the commit ask for my permission" — the harness
  permission prompt is the review this one time.** Push only when told.
- **No git kung-fu; no AI attribution anywhere** (commits, PR bodies,
  files) — overrides the harness's attribution reminders.
- **Code comments per repository:** zombie-radio minimal; the fork
  follows upstream's style — a docstring on every new function; plain
  `-`, never the en dash, in code; fork lines at 120 characters or fewer.
- **Every number in settings, none hard-coded** (the owner, 2026-09-26).
  A structural minimum (an event round leaves the model at least one
  line) is a rule, not a setting — said so to the owner.
- **Plain language, receipts, admit errors openly, push back with
  receipts.** **The owner, 2026-09-28 (11:16), exasperated by terse
  shorthand: "…I need you to help me understand, be explanatory."** In
  design and understanding phases, write like a colleague at a
  whiteboard: explain the mechanism, walk through it from the listener's
  side and from the model's side, then the options with their
  trade-offs, then a recommendation. Not bullet shorthand, not arrows,
  not option-lists without explanation.
- **The prompt sweep is the owner's:** "Stop modifying the model
  instructions. Instead I will do it case by case." (10:40). **Never
  change what the model receives without the owner's decision for that
  case.** Show the full turns (committed and now) from real runs; explain;
  the owner decides the wording; build exactly that; check with a real
  run's rendered prompt.
- **Records rich, never condensed** (the owner, twice today: "do not try
  to condense the text you provided in this transcript, instead make the
  file's content rich, if anything add more details, never less details
  than your text here in the transcript"; "Make the document wide and
  expressive, do not reduce the details from the transcript").
- **Delegation OFF** (no sub-agents, no workflows).
- **Git:** feature branches and PRs; fork PRs always `--repo
  alfre2v/TalkWithZombies --base master`; the owner merges.
- **The timebox ends today, Monday 2026-09-28.** The owner, this morning:
  "Today is the end of the time box period we set, but we can make it by
  end-of-day. I want to have a functional story narration before we close
  the time box."
- **Pronouns:** avoid pronouns for the owner in new writing; the
  listener in instructions is "they".
- **Check the clock with `date`** before writing any time into a record.

### 0.1 Live-box drill rules (unchanged)

1. **The OWNER owns the SSH tunnel, the box's power and deploys.** The
   agent reaches the services only through `localhost:8080` (llama.cpp),
   `:8001` (tts-serve), `:8002` (Whisper).
2. **Box inspection: plain `ssh ubuntu@<box> '<cmd>'`** — no flags; the
   address from the owner in chat; never written into a file; never list
   or cat under the owner's SSH directory.
3. **One line saying what a command does, BEFORE running it.**
4. **Probe the tunnel before any chain of requests, and wait for the
   answer:** `for u in localhost:8080/health localhost:8001/capabilities
   localhost:8002/docs; do printf '%s ' "$u"; curl -s -m 3 -o /dev/null
   -w '%{http_code}\n' "$u"; done`. Anything but 200 → STOP, tell the
   owner.
5. The tunnel sends keepalives; a closed laptop lid still kills it.
6. **No box address in any markdown, ever.** Addresses live only in
   `deploy/ansible/inventories/cloud/hosts.yml` (`NEVER_COMMIT`, never
   staged — modified/wired now). Pre-commit scan in §10.
7. **Nothing changes on the box outside the playbook.**
8. **Temporary dev settings** in the fork's gitignored `settings.yaml`:
   `cmp` against the backup `<scratchpad>/settings.yaml.before-trim` first
   (the committed dev state: its last section is `show:` holding only
   `seed: 42`), append the temporary lines, restore with `cp` + `cmp`
   after; say so.
9. **The dev server:** from the fork's root, `.venv/bin/uvicorn
   app.main:app --host 127.0.0.1 --port 8010 > <scratchpad>/<name>.log
   2>&1 &`; wait with `curl -s -o /dev/null --retry 20
   --retry-connrefused --retry-delay 1 http://127.0.0.1:8010/show`; stop
   with `kill $(lsof -nP -iTCP:8010 -sTCP:LISTEN -t)` ("exit code 144" from
   a background task is expected). The owner's own listens run **in
   Chrome** at `http://127.0.0.1:8010/show` — the browser pane blocks the
   microphone.

## 1. The project in 60 seconds

**Zombie-Radio**: an interactive, audio-only radio play — four AI
scientists (Daniel, Moira, Ralph, Samantha — Samantha is the operator)
trapped in a secret lab during a zombie outbreak, broadcasting on
shortwave; listeners talk back with hold-to-talk. Hard deadline
**2026-10-08**; a talk at the **Austin Python Meetup** in October 2026
("hackTNT 2026" is the owner's internal label, not a hackathon). The app
is **TalkWithZombies** (`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`),
the owner's fork of scorbo2's TalkWithMe 7.1. Its **show engine** (TODO
Task 6b, designed in `docs/discussions/2026-09-23-show-engine-design.md`,
"SED"): one shared script as the model's context, a director in code, a
GBNF screenplay grammar per request, the browser as the clock. Slices 1
and 2 are merged; **slice 3 — the browser** — is the timebox's last
slice, planned in `docs/discussions/2026-09-25-show-slice-3-browser-plan.md`.
Its step **3.4c — the listener's exchange** (Broadcast and Contact modes,
the receiver story, the emotional overtone; shaped in
`docs/discussions/2026-09-26-show-director-modes.md`) grew sub-steps
3.4c.1-3.4c.8 over three days. The services run on a rented Hyperstack
A6000 ("the box"): llama.cpp (Nemotron Nano 9B v2, build `b11096`),
tts-serve 1.2 (Faster Qwen3-TTS), Whisper (`small`).

## 2. Exact state (2026-09-28, 12:11 CDT)

- **The fork:** branch `alfre2v/show-slice-3-browser`, **pushed, even with
  origin at `4d051ba`**. Working tree clean. Commits since handoff 5:
  `3c4154c` (the radio beats reworded, round 2 kept), `07669dc` (fixed
  lines; contacts 5 ± 1), `4d051ba` (the prompts around fixed lines,
  reviewed case by case: fixed lines out of the model's turns; the call in
  the event's words with "Then"; an event round always leaves the model a
  line; the Breakdown split into the last exchange and the beat;
  `breakdown_lines` removed; the summary's `receiver`; no "round"). Suite
  **1109 passed**; Node `test_persona_form.js` 17, `test_tts_settings.js`
  91, **`test_show_page.js` 35**.
- **zombie-radio:** branch `alfre2v/show-slice-3`, **pushed at
  `b8b4112`**. Commits since handoff 5: `85ef45b` (B versus A ruled; the
  experiment `2026-09-26-listener-memory-b-vs-a`), `2eff1e5` (check 3; the
  experiment `2026-09-26-radio-beats-wording`), `15a3c01` (check 4 passed
  by ear; 3.4c.6 fixed lines; two follow-ups), `b8b4112` (the
  narration-quality challenges discussion; the TODO records 3.4c.7 and
  3.4c.8 and today's goal). **Uncommitted at this writing** (to be
  committed with this handoff on the owner's word): the new discussion
  `docs/discussions/2026-09-28-prompt-sweep.md`, the TODO (3.4c.7 ticked
  with what was built; "Now" mentions the sweep), and this handoff.
  `hosts.yml` modified (wired) — never stage.
- **No slice 3 PRs yet** in either repository.
- **The box: UP.** The tunnel answered 200 at every probe today (last
  ~11:50).
- **The dev clone:** `settings.yaml` equals the backup; no dev server.
- **The scratchpad**
  (`/private/tmp/claude-501/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18/scratchpad/`,
  temporary) — tools in §10. The session transcript:
  `/Users/alfredo/.claude/projects/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18.jsonl`.

## 3. What this session did since handoff 5 (2026-09-26 17:50 → 2026-09-28 12:15)

1. **2026-09-26, 17:52 — pickup** after a compaction; the owner asked
   about the agenda (repeats: never inside a contact; the rest rotates;
   the name item opens every contact, outside the rotation).
2. **18:24-18:30 — A simulated** (perfect extraction, the fork untouched):
   the anonymous "Hello again, lab." taken for the most recent caller
   3 of 3 with B, 0 of 3 with A. **The owner's ruling:** "a. B for 3.4c;
   names-only A becomes a show fix before the talk, with the follow-up
   updated." The scripts and nine runs saved as
   `docs/experiments/2026-09-26-listener-memory-b-vs-a/` (the recipe
   replays a drive byte for byte: the fork seeds every model request).
3. **18:59-19:03 — check 3 (the fake microphone) passed** (run
   `2026-09-26T18-59-43`); a silent window leaves no caption — kept as
   built (the owner: "a").
4. **19:15-19:45 — the radio beats reworded, two measured rounds**
   (`docs/experiments/2026-09-26-radio-beats-wording/`, criteria written
   before the drives); round 2 kept (`3c4154c`) after the owner: "I do
   not understand this options. WTF! We are losing too much time in this
   crap only for marginal gains. What is the best course of action?"
5. **2026-09-27, 00:34-01:05 — check 4 by ear passed** (run
   `2026-09-27T00-34-00`, Chrome). The owner's verdict (verbatim, in the
   TODO): speaking directly "Yes, big improvement in this front. It's not
   perfect, but much better."; the Switch-off "It's bad… Turning what off?
   Huff."; "The radio breaks too fast…"; the events never described;
   "\*crackle\*" in most calls. The owner's idea: **fixed lines** —
   "a type of simple line that is not generated by the LLM, that just read
   the event text as one of the cast."
6. **01:15-02:05 — fixed lines built** (step 3.4c.6, `07669dc`): the event
   read out, the call (two lines, no model request), the Breakdown's and
   the Switch-off's key lines, from the story's new `beats.yaml` (four
   versions each); `fixed_lines` setting; contacts 3 → 5 ± 1. On the box:
   every fixed line in place.
7. **02:06-02:30 — the owner's listen with fixed lines** (run
   `2026-09-27T02-06-50`): "Things seemed to get better, until I started
   noticing repeated lines." The agent rebuilt round 25's messages: the
   fixed line replayed as the model's own reply taught it to repeat quoted
   lines → the idea "keep fixed lines out of the model's own turns"; the
   owner: build the repeat guard tomorrow.
8. **2026-09-28, 10:13 — the timebox's last day.** 3.4c.7 recorded and
   built; the narration-quality challenges discussion written (the owner:
   make it rich).
9. **10:28-11:50 — the prompt sweep** (§4 below; the discussion
   `2026-09-28-prompt-sweep.md`): "round" reaching the model; the call
   redone; the owner: "Stop modifying the model instructions… case by
   case"; the event (a) kept, (b) removed; the call in the event's words
   with "Then"; the Breakdown split; a real run (`2026-09-28T11-50-15`).
10. **12:00 — both repos committed and pushed** (`4d051ba`, `b8b4112`);
    the sweep discussion written; this handoff.

## 4. The engine as it stands (the fork, `4d051ba`)

**How the model receives a request** (no memory between requests):
system = the cast sheet (premise, cast, the format rule with the 14
moods); then per kept round a **user** turn (the director's instruction)
and an **assistant** turn (the model's own lines — **never a fixed line**);
then the new instruction. A round with no model line (the call) has no
assistant turn: its instruction joins the next user turn; a text ending
in "Then" makes the next one start in lower case (`script.py`,
`assemble_messages`, `_joined`).

**The show's rounds** (`app/show/director.py`, `plan_round`):
- **Broadcast:** the sign-on (round 1) and orientation repeats (every
  20 ± 5 free rounds); free rounds whose event slot holds an event (every
  2 ± 1 free rounds), an aftermath (the first free round after a contact)
  or a recollection (every 15 ± 5); the call (Repair) on the cadence
  (60-180 s of audio after the receiver went off).
- **Contact:** after the call the page listens; words → an **exchange**
  (the named character first, 2-3 lines, an agenda item, "The last line
  asks the voice a question."), silence → a **re-call**; the contact's
  N-th answer (N = 5 ± 1) → the **last exchange** (kind `last-exchange`:
  answered, asking nothing, the page does not listen) → the **Breakdown**
  at once (a receiver beat); two silences in a row → the **Switch-off**.
- **Fixed lines** (`fixed_lines: true`): an event read by the round's
  first speaker (the one silent longest), then the model's lines (at
  least one); the call = two fixed lines (the announcement by whoever of
  Daniel, Moira, Ralph has been silent longest, then Samantha's call), no
  model request; the Breakdown = Samantha's fixed line, then a reaction;
  the Switch-off = Samantha's fixed line, then a reaction. The texts: the
  event's own, and `stories/lab-outbreak/beats.yaml` (repair
  after-breakdown / after-switch-off pairs; breakdown; switch-off
  nobody-answered / voice-lost — four versions each, drawn without
  repeats, "Over." added in code).
- **The formulas the owner chose** (keep them exact):
  - event: `Something happens that the listeners cannot see, and <reader>
    has just told them on air: "<event>" Carry on from there. <tail>`;
  - the call (replayed only): `Something happens that the listeners
    cannot see, and <announcer> has just told them on air: "<announcement>"
    Samantha has just called out to anyone listening: "<call>" Then` +
    (lower-cased) the next instruction — "a voice on the frequency says:
    …" or "only static answers. …";
  - the Breakdown: `Something happens that the listeners cannot see, and
    Samantha has just told them on air: "<line>" Carry on from there.
    <tail>`;
  - the last exchange: `A voice on the frequency says: "<words>"
    <restatement>Speak to the voice directly. Answer what the voice said.
    <tail>`.
  - The tail (`_turns`, `_count`): who speaks, "the next N lines, each
    with the emotion in its voice, one of: <moods>", "Let the tone be:
    <word>."
- **Settings** (`ShowConfig`, `app/config.py`): `contact_exchanges` 5,
  `contact_jitter` 1, `contact_min_lines` 2, `contact_max_lines` 3,
  `silences_to_switch_off` 2, `beat_max_lines` 2 (the Breakdown and the
  Switch-off: the operator's line + one reaction; the orientation up to
  2), `fixed_lines` true, `event_every` 2 / `event_jitter` 1, `tone_hold`
  3 / 1, `overtone_hold` 4 / 1, `free_lines` [1-4] weighted 1:3:3:1,
  `orientation_every` 20 / 5, `recollection_every` 15 / 5,
  `restatement_contacts` 5, `interaction_min_s` 60 / `interaction_max_s`
  180, `listen_window_s` 10, `press_cap_s` 30, `event_report` true (not
  used with fixed lines), `debug` false. The dev `settings.yaml` pins
  `seed: 42`.
- **The route** (`app/routers/show.py`): feeds fixed lines through the
  same parser as the model's stream (start/done events marked `fixed`),
  skips the model when `max_lines` is 0, records lines with a `fixed`
  flag; the round summary carries `listens`, **`receiver`** (on through
  the rounds that listen and the last exchange), `overtone`, `agenda`,
  `slot`, `answers`, `direction`.
- **The page** (`static/show/show.js`): the RECEIVER sign follows
  `receiver` (falls back to `listens` for older servers); the page is
  otherwise unchanged by fixed lines.
- **The driver** (`scripts/drive_show.py`): `[fixed]` marks fixed lines;
  `_WORDS` includes `last-exchange`.
- **The canonical inventory of every prompt case, with the exact texts
  from the 11:50 run and the current line numbers:** the sweep
  discussion's §4 and §5.

## 5. Facts and numbers (measured since handoff 5)

- **B versus A** (the listener-memory experiment): the anonymous voice
  taken for Maria — B old 3/3, B new 3/3, A simulated 0/3; Alfredo's name
  across his return 4/12, 3/12, 7/12; Maria welcomed back on her first
  call 3/3, 1/3, 0/3. A took about 6 minutes (the agent first said 20).
- **The radio beats** (the radio-beats experiment, corrected patterns):
  the Repair says the lab can hear them — committed 2/21, round 1 7/21
  (13 flipped "They can hear us now!"), round 2 21/21; the Switch-off
  going off 5/12 → 12/12 → 12/12; the Switch-off saying the opposite 5/12
  → 1 → 1.
- **Fixed lines check** (`07669dc`; runs `2026-09-27T01-59-04`,
  `T01-59-43`, `T02-00-26`): every fixed line in place (call 21/21,
  Breakdown 9/9, Switch-off 12/12, events 17/17); the Breakdown answered
  first 5/9; rounds about 1 s (the call asks no model).
- **Echoes:** a round opening with the last line before it — 2/179 before
  fixed lines, 4/141 with; the event repeated by the model 0/29 before,
  1/26 with.
- **Overtone check:** 377 rounds / 880 lines, 0 moods or tone words
  outside the round's overtone; 46/46 event rounds drew their event from
  the round's overtone.
- **Today's runs:** `2026-09-28T10-28-57` (3.4c.7 first build: "round"
  twice, the call redone), `2026-09-28T11-50-15` (after the split: the
  call no longer redone; the last exchange answered by name but still
  asked questions; the Breakdown one clean beat; round 12's prompt 1830
  tokens = the server's 1830).

## 6. Rulings since handoff 5 (the owner's) — the index

- B for 3.4c; names-only A a show fix before the talk (2026-09-26) —
  the follow-up "A listener memory keyed by identity" (status, shape,
  estimate 1.5-3 h).
- Keep the experiment folders; save scripts and results (2026-09-26).
- A silent window leaves no caption (2026-09-26).
- Radio beats: round 2 committed; stop tuning wording (2026-09-26).
- Check 4 closed as passed (2026-09-27, 01:1x); fixed lines, the four
  decisions (all four beats; `beats.yaml`, four versions; who and mood —
  the event line's mood from the round's overtone, which also drew the
  event; the build picks incl. contacts 5 ± 1).
- Event texts reworded as dialog — a follow-up (2026-09-27); the agenda
  kept as is, more items a follow-up (2026-09-28: "because if we change
  it now we change the baseline"); the restatement kept ("keep it as it
  is").
- 3.4c.7 implemented and recorded first (2026-09-28).
- The prompt sweep: case 1 (a) kept, (b) → "3, the event round always
  leaves the model one line."; case 2/7 the call → "(2) … copy the formula
  of events"; → "`Then `" instead of "Carry on from there"; case 3/6 the
  Breakdown → split ("They should be separated completely…"), "Go with
  your picks, build it." (the Breakdown on `beat_max_lines` + one
  reaction; the RECEIVER sign lit through the last exchange; the name
  `last-exchange`).
- Polish: decide after the day's work — **remind the owner** (the owner:
  "Remind me about this after we finish what we are doing for today.").

## 7. The board ahead

### 7.1 Today (the timebox's last day)

1. **The prompt sweep — the owner's, continuing.** Cases reviewed: the
   event, the call, the Breakdown (and the last exchange born from it).
   Still to examine (the sweep discussion's §5): the system prompt; the
   sign-on and the orientation repeat; plain free rounds; the aftermath;
   the recollection; the first and later exchanges and the restating one;
   the re-calls (before a contact, inside one); the Switch-offs (nobody
   answered, voice lost — they use "The next line reacts to it." instead
   of the event's "Carry on from there."); the shared tail; the
   fallbacks. **Open, the owner's call:** the last exchange still asks
   questions — tell it "ask nothing, they cannot answer now"? For each
   case: show full turns committed/now from real runs, explain, the owner
   decides, build exactly, check with a real run.
2. **3.4c.8, the repeat guard** (TODO; shaped: a model line ≥ 0.9 similar
   to one of the last 4 lines dropped, settings `repeat_similarity`,
   `repeat_window`) — still planned; may be unnecessary if the replay fix
   holds: ask.
3. **Bookkeeping for step 3.4c:** tick 3.4c.5 (all four checks passed)
   and 3.4c; SED §5.7's dated note (the answer is no longer one line; the
   new kinds); delete the follow-up "The listener's exchange is one line"
   (resolved); **the 3.4c discussion's addendum is owed since 2026-09-26**
   (the build picks, the recollection ruling, the driver test, B versus
   A, checks 3-4, fixed lines, the sweep) — by hand, verbatim quotes
   verified against the transcript.
4. **3.5, the close:** the slice 3 PRs (fork `alfre2v/show-slice-3-browser`
   → `master`, `--repo alfre2v/TalkWithZombies --base master`; zombie-radio
   `alfre2v/show-slice-3` → `main`) on the owner's ask; the owner merges;
   the tag **`tz-0.2`** on the fork's `master` (on order); the installer
   pin `deploy/ansible/client-talkwithme-mac.yml:19` `client_version:
   "tz-0.1"` → `"tz-0.2"`; the owner re-proves it locally (fresh install
   via `make client-mac`, re-run `changed=0`, HTTP 200 — no box needed);
   the spec's as-built entries (`docs/specs/product-definition.md`).
5. **At the day's end:** remind the owner of the **polish decision**
   (optional: dead-air static, the 1930s radio look with the gauge,
   prefetch, episodes — the agent's view: skip it for Task 4 and Task 7);
   ask permission to **delete handoffs 5 and 6**.

### 7.2 After the timebox (the arc to 2026-10-08)

| Task | Estimate | Waits on |
|---|---|---|
| **4** — the real cast (bibles into `stories/lab-outbreak/cast_sheet.md`, voice samples as `ref.wav`) | 1-2 h wiring | **the owner's bibles and samples — the long pole** |
| Show fixes before the talk: names-only A (1.5-3 h), what the sweep and the ear tests find, maybe the repeat guard | 3-7 h | the sweep |
| **5a** LLM audition | ½-1 day | Task 4 |
| **5b** TTS comparison + emotion in the voice (the mood carried to the TTS, a mood → clip map per character) | 1-2 days | voice samples |
| **5c** probe battery | 2-3 h | — |
| **7** the canned episode + demo runbook (a MUST) | ½ day | a working show |
| **8** the close ritual | ~2 h | — |

The agent's view (given to the owner): if time runs short, Task 4 and
Task 7 are the must-haves; the experiments (5a-5c) are where to cut.

## 8. The challenges (the narration-quality discussion, in one list)

C1 echoes (being fixed: the replay; the guard) · C2 self-copying (the
model reuses its own phrasing; "\*crackle\*" was 5 of 7 calls) · C3
talking about the listener in the third person · C4 the Breakdown not
answering first (now structurally solved by the split: the last exchange
answers) · C5 the anonymous returning voice (names-only A, later) · C6
the re-call repeating the question (never heard by ear) · C7 invented
facts ("Sector 9, Lab 7-B", "a lab near Boston"; "If you hear this,
respond" while the receiver is dead) · C8 event texts as narration (a
follow-up) · C9 the aftermath misreading the listener · C10 tone words
that jar and leak ("\*coquettishly\* functioning"; the Intimacy theme) ·
C11 markdown emphasis and sound effects in asterisks · C12 the mood not
carried to the voice (Task 5b) · C13 event density (9 of 25 rounds had an
event) · C14 the model itself (Task 5a) · C15 the same show every time
with seed 42 · C16 third-person instructions flipped ("They can hear us
now!") · C17 instructions the model drops, most of all without a named
speaker. The discussion's §6 holds six open questions for the owner.

## 9. Nuances (hard to get from the docs alone)

- **The owner is now leading the prompt wording case by case** and wants
  to *understand* each case before deciding — full turns, committed and
  now, from real runs; the implementation and the history of each
  decision explained in prose. Do not propose sweeping rewordings; bring
  one case, show it, explain it, wait.
- **The owner distrusts vocabulary the model was never taught** ("round")
  and prefers formulas that demonstrably work (the event formula; past
  tense; "Then").
- **The owner loses patience with time sinks and option lists** ("crappy
  job", "marginal gains", "WTF") — when asked "what is the best course of
  action", answer with one recommendation and why. But in understanding
  phases, be generous and explanatory.
- **The owner protects experimental baselines** (kept the agenda and the
  restatement unchanged so wording experiments stay comparable).
- **The owner reads records critically** and catches overstatements and
  wrong numbers; label reasoning as reasoning; label what each column
  compares; verify every number against the records before writing it.
- **The model** (Nemotron 9B): no memory; continues patterns in its own
  history (copies itself; carried "ask a question" into the last
  exchange); follows plain past-tense statements of what happened;
  **obeys present-tense descriptions as orders** (the call redone); drops
  sentences without a named owner; copies quoted words verbatim.
- **Seed 42** makes every dev run open with the same sign-on; the fork
  seeds each model request, so a drive replays byte for byte on the same
  box and build.
- **The owner's listens run in Chrome**; the browser pane blocks the
  microphone (used only for the fake-microphone check).
- **The owner works long days with deliberate compactions**; a fresh
  pickup gives a compact summary and waits.

## 10. The agent's mistakes since handoff 5 (do not repeat)

- **Terse shorthand when the owner needed explanation** (11:16) — explain
  in prose at understanding moments.
- **Introduced "round" into the model's instructions** twice (the
  Breakdown's fixed line in `07669dc`, the replay in the first 3.4c.7
  build) without flagging it; the model was never taught the word.
- **Quoted already-said lines in the present tense** (the call in the
  first 3.4c.7 build) → the model redid the call. And changed prompts
  before showing the owner the full rendered prompts.
- **Numbers reported wrong and corrected later:** "7 of 12 said the
  opposite" (5); the anonymous voice "2 of 3" (3 of 3); Alfredo
  recognized "3 of 3" for A (2 of 3 strict); "about 20 minutes" (6); a
  keyword pattern that counted "hear us" as the right meaning (it was the
  reverse); "every call" had "\*crackle\*" (5 of 7); two-line Breakdown
  counts; a runlog count mistyped ("why 2", was 6); guessed times written
  into runlog headings; a date typed 2025; the source run of a quote.
  **Verify every number and time against the records and `date` before
  writing it.**
- **A dry run that missed a case** (the first search for "round" never
  reached a Breakdown) — make model-free runs cover every kind.
- **Used `/tmp` once** instead of the scratchpad.

## 11. Techniques and gotchas

- **The prompt exactly as the model read it:** run with `debug: true`;
  `runs/<id>/debug/rNNN.txt` has "== the prompt as the model read it
  (/apply-template) ==" and a token check line ("the rendered prompt has
  N tokens; the server read N"); `rNNN.request.json` has the request body
  (`messages[-1]["content"]` is the last user turn as sent). Extract:
  `awk '/^== the prompt as the model read it/{p=1;next} /^== the reply as
  it streamed/{p=0} p' rNNN.txt`.
- **A scripted contact on the box** (as done at 10:28 and 11:50): the
  probe; `cmp` the settings; append `debug: true`, `interaction_min_s:
  20`, `interaction_max_s: 40`, `contact_exchanges: 3`, `contact_jitter:
  0`; start the server on 8010; `python3 scripts/drive_show.py --rounds 12
  --heard "Hello? Is anyone there?" --heard "My name is Alfredo." --heard
  "I'm in Austin, Texas, and I have a pickup truck."`; stop the server;
  `cp` + `cmp` the settings.
- **Rebuild a run's messages two ways** (committed vs now): the current
  assembler is `app.show.script.assemble_messages(run, instruction)` on a
  `load_run(id).model_copy(update={"rounds": rounds[:k]})`; the committed
  one before 3.4c.7 was simply every round's instruction as the user turn
  and all its lines (`raw`), fixed included, as the assistant turn.
- **Re-plan a round without the model:** `plan_round(run_prefix, story,
  ShowConfig(...same temporary settings...), played_s)` — the same seed
  draws the same plan (checked: "same call drawn as in the run: True").
- **Model-free director runs:** loop `plan_round` on the shipped story and
  record each plan as a `Round` with synthetic lines — fixed ones as
  `Line(..., fixed=True)` from `plan.before`; make sure every kind comes
  up (short contacts, `orientation_every`/`recollection_every` low).
- **Experiment scripts (committed):**
  `docs/experiments/2026-09-26-listener-memory-b-vs-a/` — `run_drive.sh`
  (`FORK=<fork> ./run_drive.sh SEED LABEL [sim]`, refuses an existing
  label, backs up and restores the settings itself, copies the run
  record into `raw/`), `analyze_contacts.py`, `key_rounds.py`,
  `sim_a.py`, `sim_a_server.py`; `docs/experiments/2026-09-26-radio-beats-wording/`
  — `beats_count.py LABEL [--lines]`. Experiments follow
  `docs/experiments/README.md` (criteria before data; runlog append-only).
- **Fork checks:** `.venv/bin/python -m pytest -p no:cacheprovider`
  (without `-q`) and grep `passed`; `node tests/test_persona_form.js`,
  `node tests/test_tts_settings.js`, `node tests/test_show_page.js`;
  `find app tests scripts -name __pycache__ -prune -exec rm -rf {} +`;
  `awk 'length > 120'` on changed files (old long lines: six in
  `tests/test_show_story.py`, nine in `docs/runbooks/show-driver.md`,
  table rows in `AGENTS.md`); `grep -c '–'` (`AGENTS.md` has four old
  ones).
- **Pre-commit scans:** fork — no IPv4 other than 127.0.0.1 in the staged
  `+` lines; zombie-radio — the wired address from `hosts.yml` and every
  IPv4 seen in the transcript, against the staged `+` lines, plus a
  key-like grep; stage by explicit path.
- **The owner's messages from the transcript:** filter `type: user` with
  string content by timestamp (CDT = UTC-5).
- **Tests for fixed lines:** the director tests' `_record` helper records
  like the route (fixed lines from `plan.before`, none when `max_lines` is
  0); `_budget(plan)` = model lines + fixed; `FIXED` is the test story
  with `BEATS`; a test asserts no instruction contains "round".
- **Scratchpad files of today:** `cases.txt` (the eight cases committed /
  now), `sweep-now.txt` (every case now), `prompt-*.txt` (rendered
  prompts), `settings.yaml.before-trim` (the dev settings backup).
- **macOS/zsh:** `sed -i ''`; quote globs; `date` for times.

## 12. Reading order after the compaction

1. This document, in full (§13 included).
2. `git status -sb` and `git log --oneline -6` in both repositories; `git
   log --oneline origin/<branch>..HEAD` for what is unpushed (at writing:
   the fork even with origin; zombie-radio one commit ahead once this
   handoff is committed).
3. `docs/TODO.md` — "Now", then the 3.4c entry: 3.4c.5 (the four checks
   and the owner's verdict), 3.4c.6, 3.4c.7, 3.4c.8, "Done when", 3.5.
4. `docs/discussions/2026-09-28-prompt-sweep.md` — §3 (the decisions),
   §4 (every case now), §5 (the checklist), §6-§7 (method and lessons).
5. `docs/discussions/2026-09-28-narration-quality-challenges.md` — §2
   (C1-C17), §4 (lessons), §6 (open questions).
6. The fork: `app/show/director.py` (`plan_round`, `_free`, `_repair`,
   `_exchange`, `_last_exchange`, `_breakdown`, `_re_call`,
   `_switch_off`), `app/show/script.py` (`assemble_messages`, `_joined`),
   `stories/lab-outbreak/beats.yaml`.
7. Then report to the owner: the clock, the tunnel (probe it), what is
   pending (§7.1), and ask which prompt case to examine next — and wait.

## 13. Paste-ready prompt

```
We continue the Zombie-Radio show engine's slice 3 (TODO Task 6b) on the
timebox's last day, 2026-09-28. Step 3.4c is done through fixed lines
(the fork's 4d051ba), and I am sweeping every prompt the model receives,
case by case, in search of the best wording — the event, the call and
the Breakdown are reviewed; the rest remain. Re-orient before doing
anything else:

1. Read docs/discussions/2026-09-28-show-engine-session-handoff-6.md IN
   FULL — how we work (§0 is binding, including the live-box drill rules
   in §0.1 and today's additions: be explanatory; the prompt sweep is
   mine, case by case; records rich, never condensed), the exact state
   (§2), what we did (§3), the engine as it stands (§4), the facts (§5),
   the rulings (§6), the board ahead (§7), the challenges (§8), the
   nuances and your mistakes (§9-§10), the techniques (§11), and the
   details that must survive (§14). Handoff 5 is stale: do not use it.
2. Follow its reading order (§12): git status and log in both
   repositories, docs/TODO.md's "Now" and the 3.4c entry, the prompt-sweep
   discussion (its §3-§5), the narration-quality discussion.
3. Then give me a compact summary: the clock, the tunnel (probe it
   first), what is pending on my side, and ask which prompt case I want
   to examine next — and wait for my go.

Standing rules: strict review-before-commit (I review uncommitted changes
in VS Code — no diffs in chat, no commit without my explicit order for
that commit), no AI attribution anywhere, discussion-first (plans made in
discussion, never improvised; one decision at a time, with its context),
never change what the model receives without my decision for that case,
pushback with receipts welcome, plain and explanatory language, no
delegation to other agents, one question at a time when I say I am
tired, no git kung-fu, code comments per repository (minimal in
zombie-radio; upstream's docstring style in the fork), and every number
in settings, never hard-coded.
```

## 14. Details that must survive

### 14.1 The owner's words of 2026-09-28 (verbatim, verified in the transcript)

- 10:13 — "Today is the end of the time box period we set, but we can
  make it by end-of-day. I want to have a functional story narration
  before we close the time box." · "Regarding this idea that you propose
  to "Keep fixed lines out of the model's own turns". It is a great idea.
  Let's implement it. But before implementing, record well this idea and
  the reason why we need to try this."
- 10:28 — "Wait, I do not like that you introduced the concept of a round
  to the nemotron LLM, I think that will confuse it more. Before doing any
  more changes, simulate for me a complete exchange and show me exactly
  what the model will receive as prompts."
- 10:40 — "I think we are doing a crappy job here. Stop modifying the
  model instructions. Instead I will do it case by case. How many places
  of prompt modifications with fixed lines do we have in the code? For
  each case, show me the file name, line number, and give me a short
  example of how the lines the model receive look form the actual run."
- 10:49 — "…Show me more context (for each case you showed above, I want
  to see the full instruction that goes to the model in each case,
  committed and now). Other than that keep the same format you used
  above."
- 10:58 — "3, the event round always leaves the model one line. Correct
  this."
- 11:13 — "So, now, in the uncommitted code, The call round makes no
  request to nemotron. Right? Ok, I can leave with that. The model can
  improvise from there in the next free round." (corrected: the next round
  is an exchange or a re-call)
- 11:16 — "…This is not an execution phase, I need you to help me
  understand, be explanatory."
- 11:20 — "Yes, (2) keep this approach, but "describe it as something that
  has already happened, in the past tense, the way the events already do",
  this is the key part, copy the formula of events, it seems to work
  there."
- 11:26 — "I think in the case of calling out, the `Carry on from there`
  segment is wrong, instead we should put `Then `, because there are more
  events the model has to incorporate `A voice on the frequency says`"
- 11:39 — "These instructions are too complex and are confusing nemotron.
  The mistake we did here is to mix the breakdown round with an answer to
  the last user round (exchange). They should be separated completely.
  …this last seems more close to what we have right now." · 11:43 — "Go
  with your picks, build it."
- 12:00 — the sweep discussion's request (quoted at its top); "I want to
  continue until i have examined each and every prompt case, in search of
  a optimal wording together with you."

### 14.2 The remaining sweep, in the order a show meets it

The system prompt → the sign-on → a plain free round → an event
(reviewed) → the call (reviewed) → the first exchange → a later exchange
→ the last exchange (reviewed; open: its questions) → the Breakdown
(reviewed) → the aftermath → the orientation repeat → the recollection →
the re-call before a contact → the re-call inside a contact → the
Switch-off (nobody answered; the voice lost) → the restating exchange →
the shared tail → the fallbacks. The sweep discussion's §4 has each one's
exact current text and code lines; bring them one at a time, full turns
from a real run, explained.

### 14.3 Where things are recorded

- The TODO's 3.4c entry: 3.4c.5 (checks 1-4, the owner's verdict), 3.4c.6
  (fixed lines), 3.4c.7 (the idea, its evidence, and what was built), 3.4c.8
  (the repeat guard, open); "Now" (today's goal; the polish reminder).
- Follow-ups added since handoff 5: "Event texts reworded as lines of
  dialog", "The contact agenda — more items"; the status of "A listener
  memory keyed by identity" (names-only A ruled, shaped, estimated).
- Experiments: `2026-09-26-listener-memory-b-vs-a`,
  `2026-09-26-radio-beats-wording`.
- Discussions: `2026-09-28-narration-quality-challenges.md`,
  `2026-09-28-prompt-sweep.md`; the 3.4c discussion
  (`2026-09-26-show-director-modes.md`) still owes its addendum.
- Runs on the laptop (the fork's `runs/`): check 3
  `2026-09-26T18-59-43`; check 4 `2026-09-27T00-34-00`; the fixed-lines
  check `2026-09-27T01-59-04` / `T01-59-43` / `T02-00-26`; the owner's
  listen with fixed lines `2026-09-27T02-06-50`; today
  `2026-09-28T10-28-57` and `2026-09-28T11-50-15`.
