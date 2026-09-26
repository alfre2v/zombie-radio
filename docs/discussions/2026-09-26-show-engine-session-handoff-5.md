# Session handoff 5 — the show engine's slice 3: step 3.4c (the listener's exchange) built; its four checks under way

> **EPHEMERAL.** Written 2026-09-26 ~17:45 CDT (Saturday), before a
> manual compaction the owner triggers at about 82 % of the context
> window, as a compaction-survival dump: after the compaction the agent
> re-reads this first. It replaces handoff 4
> (`2026-09-25-show-engine-session-handoff-4.md`), deleted in the same
> commit with the owner's permission (the owner authorized this commit
> without review, this time only). When the session's work is done, the
> agent asks the owner for permission to delete this handoff.
>
> **Read it all; verify against the repos; receipts or nothing.** The
> TODO's "Now" section and its step 3.4c entry are the canonical state;
> the discussion `2026-09-26-show-director-modes.md` holds every ruling of
> the day, verbatim. This document carries what those cannot: how we
> work (and what changed today), the code of 3.4c as built, the numbers
> measured today, the board ahead with the question pending, the
> nuances, the mistakes not to repeat, and the working techniques.

## 0. The owner and how we work (binding)

The owner is **Alfredo** (GitHub `alfre2v`, git author "Alfredo
Valles"), a senior engineer in a **"tight learning loop"**: progress
and the owner's own learning weigh the same. The agent memory files
hold the standing doctrine — trust them (`working-agreements.md`,
`collaboration-style.md`, `absolute-paths-in-plain-text.md`,
`massedcompute-reminder.md`, `project-venue-austin-python-meetup.md`).
The non-negotiables, as practiced (today's additions in bold):

- **Discussion-first.** Every step starts with a shape in chat; the
  owner answers "Go" (usually "Go with your picks"). **Today the owner
  slowed the agent down: bring each decision one at a time, each with
  its context (what it is, what it fixes, how it connects to the
  others, what it touches, what is decided later inside it), then a
  lean and one question.** That rhythm ran all day and worked.
- **Plans are made in discussion, never improvised.** A settled
  ruling is cited before it is re-opened (today: the time-based
  cadence came from the owner's own pushback of 2026-09-21 — cited
  when the owner proposed pacing in rounds; it became a follow-up).
- **Review-before-commit is strict: a commit needs the owner's
  explicit order for that commit, given after the changes exist.**
  "commit the fork, then commit zombie-radio" orders both. Nothing was
  pushed today — push only when told. **Exception, this time only:
  the owner authorized committing this handoff (with the TODO update
  and handoff 4's deletion) without review.**
- **The commit pattern:** the fork's step, then the zombie-radio
  bookkeeping (the TODO tick with the fork's hash and receipts).
- **No git kung-fu; no AI attribution anywhere** (commits, PR bodies,
  files) — overrides the harness's attribution reminders.
- **Code comments per repository:** zombie-radio minimal; the fork
  follows upstream's style — a docstring on every new function (PEP
  257; JSDoc in JS); plain `-`, never the en dash, in code; fork lines
  at 120 characters or fewer.
- **Every number in settings, none hard-coded** (the owner,
  2026-09-26: "make sure that we can change those numbers in config or
  setting, not hardcoded as numbers in the code.").
- **The show's frontend lives in its own files** (`templates/show.html`,
  `static/show/`); upstream's JavaScript, HTML and CSS stay untouched.
- **Records of discussions, the same day, verbatim, extracted by
  script and verified** (§10). The owner asks explicitly for
  disagreements, ideas and "risks, not mistakes" to be recorded — and
  where ("prominently", "a proper follow-up entry").
- **Show the literal artifact when asked** (today: the instruction
  exactly as the model received it, before and after the wording
  pass). **Label every measurement by what it compares** (§9).
- **Plain language, lists and sublists, receipts; admit errors
  openly; push back with receipts** (the owner invites it: "Pushback if
  your have strong reasons").
- **Delegation OFF** (no sub-agents, no workflows).
- **Git:** feature branches and PRs; fork PRs always `--repo
  alfre2v/TalkWithZombies --base master`; the owner merges.
- **The timebox ends Monday 2026-09-28** (owner, 2026-09-25: "do not
  push back on this one"); mention the clock when planning.
- **Pronouns:** avoid pronouns for the owner in new writing; the
  listener in instructions is "they".

### 0.1 Live-box drill rules (unchanged)

1. **The OWNER owns the SSH tunnel, the box's power and deploys.** The
   agent reaches the services only through `localhost:8080`
   (llama.cpp), `:8001` (tts-serve), `:8002` (Whisper).
2. **Box inspection: plain `ssh ubuntu@<box> '<cmd>'`** — no flags; the
   address from the owner in chat; never written into a file; never
   list or cat under the owner's SSH directory.
3. **One line saying what a command does, BEFORE running it.**
4. **Probe the tunnel before any chain of requests, and wait for the
   answer:** `for u in localhost:8080/health localhost:8001/capabilities
   localhost:8002/docs; do printf '%s ' "$u"; curl -s -m 3 -o /dev/null
   -w '%{http_code}\n' "$u"; done`. Anything but 200 → STOP, tell the
   owner.
5. **The tunnel sends keepalives** (`make ssh-tunnel`); a closed laptop
   lid still kills it — expected.
6. **No box address in any markdown, ever.** Addresses live only in
   `deploy/ansible/inventories/cloud/hosts.yml` (`NEVER_COMMIT`, never
   staged — modified/wired now). Pre-commit scan in §10.
7. **Nothing changes on the box outside the playbook.**
8. **Temporary dev settings** in the fork's gitignored `settings.yaml`:
   `cmp` against the backup
   `<scratchpad>/settings.yaml.before-trim` first (the committed state
   of the dev file: `show:` holds only `seed: 42`), add the temporary
   lines, restore with `cp` + `cmp` after; say so.
9. **The dev server:** from the fork's root, background `exec
   .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8010 >
   <scratchpad>/dev-server-8010-<name>.log 2>&1`; wait with `curl ...
   --retry 20 --retry-connrefused --retry-delay 1
   http://127.0.0.1:8010/show`; stop with `kill $(lsof -nP -iTCP:8010
   -sTCP:LISTEN -t)` and re-check a second later ("exit code 144" from
   the background task is expected). **Today's shortcut for scripted
   drives:** `<scratchpad>/run_drive.sh SEED LABEL` does all of 8 and 9
   around one drive, restoring the settings even on failure (§10).

## 1. The project in 60 seconds

**Zombie-Radio**: an interactive, audio-only radio play — four AI
scientists (Daniel, Moira, Ralph, Samantha — Samantha is the operator)
trapped in a secret lab during a zombie outbreak, broadcasting on
shortwave; listeners talk back with hold-to-talk. Hard deadline
**2026-10-08**; a talk at the **Austin Python Meetup** in October 2026
("hackTNT 2026" is the owner's internal label, not a hackathon). The
imitated style: Orson Welles's *The War of the Worlds* (1938).

The app is **TalkWithZombies**
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`), the owner's
fork of scorbo2's TalkWithMe 7.1 (upstream checkout:
`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe`). Its **show engine**
is TODO Task 6b, designed in
`docs/discussions/2026-09-23-show-engine-design.md` ("SED"): one shared
script as the model's context, a director in code, a GBNF screenplay
grammar per request, the browser as the clock. Slices 1 and 2 are
merged. **Slice 3 — the browser** — is planned in
`docs/discussions/2026-09-25-show-slice-3-browser-plan.md`; its steps
3.1-3.4b were done on 2026-09-25. **Today (2026-09-26) the listener's
exchange became step 3.4c** — a new director built from the owner's
2024 design, shaped in `docs/discussions/2026-09-26-show-director-modes.md`
— and it is built; its four checks are under way. The services run on
a rented Hyperstack A6000 ("the box"): llama.cpp (Nemotron Nano 9B v2,
build `b11096`), tts-serve 1.2 (Faster Qwen3-TTS), Whisper
(whisper-fastapi `small`).

## 2. Exact state (2026-09-26, ~17:45 CDT, Saturday)

- **The timebox:** ends **Monday 2026-09-28**. Slice 3 still needs
  3.4c's checks, its bookkeeping, and 3.5 (the close).
- **Step 3.4c:** built in five sub-steps (3.4c.1-3.4c.4, plus the
  wording tuned in 3.4c.5). **3.4c.5, the four checks:** check 1 green;
  check 2 (the driver test) run, before and after a wording pass; **the
  owner's B-versus-A call is pending** (§7.1); the A simulation was
  proposed and **not run** (the owner: "Do not run the A simulation
  yet."); checks 3 (fake microphone) and 4 (the owner by ear) remain.
- **The fork:** branch **`alfre2v/show-slice-3-browser`** (cut from
  `master` `5b2485f`, slice 2's merge). **Origin is at `500debe`**
  (3.4b, pushed 2026-09-25); **five commits today, NOT pushed:**

  | Hash | Step | What |
  |---|---|---|
  | `b988672` | 3.4c.1 | the story's data: `overtones.yaml` (replaces `tones.yaml`), events by overtone, `agenda.yaml`, the cast sheet's premise, orientation facts and stage directions; the loader |
  | `5c0c2a3` | 3.4c.2 | the grammar's pins and minimum; fifteen settings in `ShowConfig` |
  | `4d0d7dd` | 3.4c.3 | the director v2, the record's new kinds and fields, the round route |
  | `90ec1e8` | 3.4c.4 | the page (listening rounds, the RECEIVER sign, beat directions, debug line) and the driver; the runbooks; `AGENTS.md` |
  | `e261b5b` | 3.4c.5 | the contact's wording, tuned from the driver test |

  Suite **1082 passed**; Node tests `test_persona_form.js` 17,
  `test_tts_settings.js` 91, **`test_show_page.js` 34**. Working tree
  clean.
- **zombie-radio:** branch **`alfre2v/show-slice-3`** (cut from `main`
  `b9e4d18`). **Origin is at `1f61fcb`** (handoff 4, pushed); **today's
  commits, NOT pushed:** `b8013e3` (the 3.4c discussion, the TODO's 3.4c
  entry, six follow-ups), `b1405e8` (the build plan, 3.4c.1 ticked),
  `2975873` (3.4c.2), `5a90933` (3.4c.3, the recollection ruling),
  `492a81f` (3.4c.4), and **this handoff's commit** (handoff 5, handoff
  4 deleted, the TODO's 3.4c.5 progress). `hosts.yml` modified (wired;
  the owner re-wired it after waking the box) — never stage.
- **No slice 3 PRs yet** (neither repository). Slice 2's PRs are
  merged (fork #3 → `5b2485f`; zombie-radio #11 → `b9e4d18`).
- **The box: UP.** At the session's start (~11:14) the owner could not
  wake the hibernated VM (no A6000 in stock); the owner got it up
  around 12:35. The tunnel answered 200 at every probe today (last
  ~17:05).
- **The dev clone (the fork):** `settings.yaml` equals the backup; no
  dev server running. Today's runs in `runs/`:
  `2026-09-26T16-28-02` (3.4c.3 smoke: no listener, calls at 20-40 s),
  `T16-51-06` (3.4c.4 checkpoint drive, 6 of 6, the runbook's example),
  `T17-00-46`, `T17-01-32`, `T17-02-20` (driver test, old wording,
  seeds 42, 7, 2026), `T17-05-46`, `T17-06-33`, `T17-07-23` (the same,
  new wording).
- **The browser pane** was not used today (the page was tested with
  Node stubs and the driver); the fake-microphone technique of handoff
  4 applies for check 3 (§10).
- **Scratchpad**
  (`/private/tmp/claude-501/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18/scratchpad/`,
  temporary): §10 lists today's tools. The session transcript:
  `/Users/alfredo/.claude/projects/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18.jsonl`.

## 3. What this session did (2026-09-26)

1. **~00:05-00:10 — pickup from handoff 4** after a compaction; the
   owner went to sleep.
2. **~11:14 — the owner back:** the VM would not wake (no A6000); the
   agent answered that the box is needed only for 3.4c's live checks
   (and not for 3.5's installer re-proof, which is local). **The owner
   made the listener's exchange step 3.4c, "but we need a complete
   discussion before implementation"**, starting from the owner's 2024
   design.
3. **12:01-12:43 — the 2024 design decoded** into two modes (Broadcast,
   Contact), beats (Repair, Breakdown) and eight features; the owner
   ruled 8 (the 2024 open-mic window) out (hold-to-talk stays) and
   postponed 6 (comic relief) and 7 (scientific findings) as
   follow-ups; re-opened 5 (remembering the listener) with two options,
   A (facts extracted in code) and B (engagement prompts), reworded by
   the agent at the owner's request (§5.1 of the discussion); a pass
   found ten items that had fallen through the cracks.
4. **12:49-13:48 — the scope, one decision at a time:** Contact mode;
   the receiver story plus the owner's **Switch-off** idea (after two
   unanswered calls the cast switch the receiver off with an excuse) and
   its extension to silence inside a contact (the silence rule); the
   contact agenda; feature 5 as B merged with the agenda plus the
   restatement; the owner reshaped feature 4 into the **emotional
   overtone** (moods and tone words coupled in positive / neutral /
   negative) and asked the "risks, not mistakes" of emotion in the
   voice to be recorded prominently (the mood must travel to the TTS; a
   mood → clip mapping of its own — Task 5b).
5. **13:53-15:35 — the details:** Contact (N = 3 ± 1 counting the
   listener's answers; 2-3 lines; the addressed character first, pinned
   in the grammar; the rest of the cast after); the receiver story (the
   Breakdown like an exchange without the question; the Switch-off up
   to two lines; the Repair two lines with the operator's call last; the
   cadence counted from the receiver going off; a sign-on, and **the
   owner's repeating orientation**); the owner proposed pacing
   everything in rounds — advised against doing it first, recorded as a
   follow-up; the agenda (plain two-branch sentences; the name item
   first; the restatement over the whole run, capped — **the owner's
   idea of remembering returning listeners**, with option c, identity in
   code, kept as a follow-up); the overtone (one story file; 14 moods;
   the tone groups sorted, the **themes kept as data — the owner's
   ask**, their uses stored as a follow-up; per-kind overtones);
   the design choices (the neighbor drift; **events follow the mood —
   the owner caught that letting the event set the mood would hand the
   show's overtones to the event pool**; the four-check exit criterion;
   the RECEIVER sign and beat directions); the mechanics (the
   orientation's details; the aftermath round; **the owner's
   recollection round**).
6. **15:47 — the discussion committed** (`b8013e3`) on the owner's
   order; the build plan shaped and approved ("Go with your picks").
7. **~15:50-16:57 — the build**, four sub-steps, each reviewed and
   committed on the owner's order with its zombie-radio tick. In
   3.4c.3 the owner questioned two picks: the aftermath before a due
   orientation (explained; kept) and **the recollection's count reset by
   each aftermath — measured, recollections starved; the owner: "a, the
   independent count with both guards"**.
8. **~17:00-17:30 — 3.4c.5 check 2, the driver test:** three seeds, a
   scripted listener, before and after a six-sentence wording pass; the
   owner asked for the measurements to be presented clearly (they had
   been labeled confusingly — §9) and for the literal prompts; the owner
   ordered the new wording committed (`e261b5b`) and held the A
   simulation.
9. **~17:40 — this handoff**, at the owner's request (context ~82 %).

## 4. Step 3.4c as built (the fork)

**The story's data (`stories/lab-outbreak/`, 3.4c.1):**
- `overtones.yaml` — `overtones:` positive (moods happy, hopeful,
  excited, relieved), neutral (calm, doubtful, urgent, curious,
  determined), negative (sad, afraid, terrified, angry, exhausted),
  each with `tones:` as theme → words (496 words in 24 themes; a mixed
  theme appears under two overtones; 4 words dropped because they
  became moods: hopeful, relieved, determined, curious; 29 moved);
  `kinds:` orientation [neutral], repair [positive], exchange
  [positive, neutral], re-call [neutral], breakdown [neutral,
  negative], switch-off [neutral, negative]; `weights:` 1 : 2 : 3.
  The order of the overtones is the neighbor order.
- `events.yaml` — overtone → theme → events (289: positive 29,
  neutral 94, negative 166; the agent's group table plus 81 moved).
- `agenda.yaml` — nine two-branch items; "Find out who the voice is…"
  first (opens every contact).
- `cast_sheet.md` — the premise sentence in the frame (the receiver
  keeps failing…), front matter `orientation:` (the facts) and
  `directions:` (repair / breakdown / switch-off stage directions).
- `app/show/story.py` — `Overtone`, `Story` gains `overtones`, `kinds`,
  `weights`, `event_pools`, `agenda`, `orientation`, `directions` (and
  keeps flattened `events` / `tones`); `KINDS`, `DIRECTED`;
  `_load_overtones`, `_load_events`, `_load_agenda` with checks;
  `all_moods(story)`; `format_rules(emotion_tags, moods)` — the system
  prompt lists the story's 14 moods.

**The grammar and settings (3.4c.2):** `build_grammar(speakers,
max_lines, moods, *, min_lines=1, first=None, last=None)` — `root ::=
pinned line{a,b}` (first) or `root ::= line{a,b} pinned` (last), the
other speakers only after or before; unpinned output is byte for byte
the grammar proven on 2026-09-22. `ShowConfig`: `free_lines` /
`free_line_weights`, `overtone_hold` / `overtone_jitter` (4 / 1),
`contact_exchanges` / `contact_jitter` (3 / 1), `contact_min_lines` /
`contact_max_lines` (2 / 3), `silences_to_switch_off` (2),
`beat_max_lines` (2), `orientation_every` / `orientation_jitter` (20 /
5), `recollection_every` / `recollection_jitter` (15 / 5),
`restatement_contacts` (5).

**The director v2 (`app/show/director.py`, 3.4c.3 + wording):**
- `plan_round`: the sign-on at round 1; after a round in `LISTENS`
  (repair, exchange, re-call; old `invitation`) → `_after_listening`;
  else Broadcast: `_time_to_listen` → `_repair`; `_aftermath` → a free
  round with `slot="aftermath"`; `_orientation_due` → `_orientation`;
  `_recollection_due` → a free round with `slot="recollection"`; else
  `_free`.
- `_after_listening`: words → `_exchange`, or `_breakdown` at the N-th
  answer (N drawn with the seed at the Repair's round); silence →
  `_re_call`, or `_switch_off` after `silences_to_switch_off` in a row.
  Each carries `answers=(so far, N)`.
- `_exchange`: first speaker = the first cast name in the words, else
  `_asker` (the last line's speaker of the last listening round); the
  agenda item (`_agenda_item`: the first item opens each contact; then
  fresh, never twice in a contact); `_restatement` (this contact's
  earlier words, then the last `restatement_contacts` earlier contacts'
  words, and "Only a voice that says the name of one of them is someone
  you spoke with before… Any other voice is someone new."); "Speak to
  the voice directly … The last line asks the voice a question."; exact
  2-3 lines (min = max = drawn).
- `_breakdown`: "First answer what the voice just said, speaking to
  them directly. Then something happens that the listeners cannot see:
  <the story's breakdown direction> The one who notices tells…".
- `_re_call`: before an answer, the operator ("…asking them to answer
  now; the receiver is still on."); in a contact, the asker, who
  "speaks to the voice, calls them by name if they gave one, and asks
  again: "<the last question>"". One line.
- `_switch_off`: the last caller first; "Nobody answered the call" /
  "The voice is gone"; the two excuses; "the broadcast goes on".
- `_repair`: "The lab has fixed the receiver." (or "switches the
  receiver back on." after a Switch-off), the story's direction, then
  two lines, the operator's call pinned last.
- `_orientation`: the operator at round 1, then whoever has been
  silent longest; the receiver facts first, then who and where.
- The overtone: `_kind_overtone` (a draw from the kind's allowed);
  `_drift` (free rounds hold a stretch, then `_step` to a neighbor,
  weighted; the chain = free, breakdown, switch-off rounds); `_moods`;
  `_tone` (the tone word from the overtone's words, held);
  `_next_event` (the overtone's pool; an overtone without events skips
  it).
- `_recollection_due` (independent count from the last recollection,
  or the first aftermath; never right after an aftermath; never the
  caller talked about last while another exists); aftermaths record
  `recollects`.
- `instruction_for` / `_turns` / `_count`: every grammar constraint
  in words — who first, the lines, "one of: <the overtone's moods>",
  the tone.
- **The agent's picks at build, reviewed:** the aftermath before a due
  orientation; an orientation after N free rounds; a re-call is one
  line repeating the question (still to confirm by ear); exact 2-3
  lines in exchanges and Breakdowns; every kind carries a tone word;
  each instruction names the allowed moods; the Repair and Breakdown
  carry the story's direction.

**The record and the route:** `Round.kind` gains the new kinds (old
three still load) and `overtone`, `agenda`, `slot`, `recollects`; the
round route accepts a transcript after any `LISTENS` round; the
`round` summary carries `listens`, `overtone`, `agenda`, `slot`,
`answers`, `direction`.

**The page (3.4c.4):** `show.listens` replaces `lastKind`; the
listener's turn after any round that listens; the "You:" caption under
that round; `setReceiver`, `receiverCue` (the RECEIVER sign follows a
round when its last line starts; fallback at the drain; at once with
`?voice=off`); `addDirection(event || direction)`; `debugLine` gains
overtone, slot, `asks "…"`, `answers k of N`. Template: `#receiver`
beside `#on-air`; CSS `--receiver` green.

**The driver (3.4c.4):** `--heard` answers every `listens` round;
`contact_line()` prints overtone, slot, agenda, answers; the checkpoint
report counts answered calls (`exchange`, `breakdown`) and silences
(`re-call`, `switch-off`).

**Docs (the fork):** `docs/runbooks/show-page.md` ("How the show
runs"), `docs/runbooks/show-driver.md` (3.4c's settings; the checkpoint
with the 2026-09-26 drive), `AGENTS.md` (the page and round rows).

## 5. Facts and numbers (measured 2026-09-26)

- **3.4c.3 smoke** (`T16-28-02`, no listener, calls 20-40 s): 14
  rounds, 24 lines, 0 dropped, ~1.35 s a round; llama.cpp accepted the
  pinned grammars; moods stayed in each overtone.
- **3.4c.4 checkpoint drive** (`T16-51-06`, seed 42, `--speak`, budget
  1500): 6 of 6; first call at round 8; Whisper heard "Moira is the
  virus airborne." (the "?" lost); 42 lines, 0 dropped, trim ×5.
- **The recollection's count** (dry runs, 20 × 300 rounds, 6 s a
  round): reset by aftermaths — 112 recollections (defaults), 0 with
  calls at 20-40 s; independent — 276, and 195 at 20-40 s; never
  right after an aftermath. Broadcast stretches: median 14 free rounds
  between calls (10-22) with the defaults.
- **The driver test (check 2)**, three seeds, the same script:

  | Measure | Old wording | New wording |
  |---|---|---|
  | The sign-on tells the receiver facts | 1 of 3 | 3 of 3 |
  | Exchanges ending on a question | 7 of 18 | 11 of 18 |
  | Maria greeted as known on her first call (wrong) | 3 of 3 | 1 of 3 |
  | Maria named in her contact | 5 of 9 | 6 of 9 |
  | Alfredo named after he gave his name | 4 of 6 | 4 of 6 |
  | Alfredo, back and naming himself, recognized | 2 of 3 | 2 of 3 |
  | "Hello again, lab." guessed as Maria (wrong) | 2 of 3 | 2 of 3 |
  | Alfredo named across his return's rounds | 4 of 12 | 3 of 12 |

  Mechanics in all six drives: unanswered calls Repair → re-call →
  Switch-off; no event inside a contact; 0 dropped; 40 rounds each at
  ~1.1-1.7 s a round. **Both columns are B** (the restatement); A was
  never run.
- **Wording notes still open for the ear test:** lines about the
  listener in the third person ("They're asking if we need
  medicine."); the Breakdown sometimes skips answering; markdown
  emphasis (`*us*`, 10-14 lines per three drives — ruled "keep the
  marks" on 2026-09-24, follow-up "Markdown emphasis in spoken lines");
  the aftermath once misread Whisper's words.
- **Timings:** a round's first line ~0.7-0.9 s, a round 1.1-1.7 s
  (text only); the TTS and Whisper as on 2026-09-25.

## 6. Rulings today (the owner's) — the index

The discussion `docs/discussions/2026-09-26-show-director-modes.md`
holds them verbatim: the decomposition (§3-§5), feature 5's options
(§5.1, reworded), the pass (§7), the scope (§9-§10), **the risks of
emotion in the voice (§11, prominent)**, Contact (§13.12), the receiver
story with the orientation (§14.13), the agenda (§15.9), the overtone
(§17.11), the exit criterion and the page (§17.12), the mechanics with
the aftermath and the recollection (§18.9). Rulings after §18 are in
the TODO's 3.4c entry (the build plan's picks; the recollection's
independent count; the wording tuned; "Do not run the A simulation
yet.") — **the discussion's addendum for them is still owed** (§7.1).

## 7. The board ahead

### 7.1 NOW: 3.4c.5, the four checks

1. **Check 1 (green):** done — 1082, Node 17 + 91 + 34.
2. **Check 2 (the driver test):** run; the new wording committed.
   **Pending: the owner's answer to "Is B enough for 3.4c, with these
   wording changes kept?"** (the agent recommended the new wording and
   B; the owner asked what A and B mean in the prompt, how A could be
   measured — answered: A was not measured; a simulation with perfect
   extraction was proposed, §7.2 — and then ordered "Do not run the A
   simulation yet."). Re-ask the B-versus-A question after the
   compaction, plainly; the A simulation only on the owner's word.
3. **Check 3 (the fake microphone in the page):** the technique of
   handoff 4 §10 (in the browser pane: `getUserMedia` fed from
   `voice.ctx`, the TTS saying the listener's words, `talkPress()` /
   `talkRelease()` from a watcher). Now the page listens after the
   Repair, each exchange and each re-call; check the RECEIVER sign,
   the beats' directions, a caption under each listening round, the
   debug line's new fields. Temporary settings: calls at 20-40 s, debug
   on.
4. **Check 4 (the owner by ear, real microphone, a quiet place):** at
   least one full contact (Repair, two or more answers, Breakdown) where
   the cast engages, and one call left unanswered until the Switch-off;
   the verdict recorded verbatim; then commit and push (the owner's
   rule: "Once approved we commit and push the branch.").
   **To confirm by ear** (the TODO's list): the re-call repeating the
   unanswered question; the restatement's wording and the agenda list
   (the owner reviews both before the ear test).
5. **The bookkeeping** at the end: the TODO ticks (3.4c.5, 3.4c), "Now";
   SED §5.7's dated note (the answer is no longer one line; the new
   kinds); the follow-up "The listener's exchange is one line"
   resolved (deleted); **the discussion's addendum** (the build plan and
   its picks, the recollection ruling with its numbers, the driver test
   and the wording, the B-versus-A outcome) — via the generator (§10) or
   by hand.

### 7.2 The A simulation (proposed, not run — the owner's word needed)

**The question it answers:** would option A's prompts — conclusions
stated by code ("this voice has not said who they are"; "this is
Alfredo, who called before: in Austin, Texas, with a pickup truck")
instead of B's raw quotes plus a rule — fix what B still gets wrong
(the anonymous "Hello again, lab." guessed as Maria; names used about
two times in three)? It measures **A's best case**: extraction assumed
perfect, because the drive is scripted and every sentence the listener
says is known in advance. A real A would do at most this well, with an
extra step per answer (a small model call or name patterns) and
Whisper's spellings to match.

**The spec, as proposed to the owner (build it exactly so):**

1. **The fact table** (`<scratchpad>/sim_a.py`) — what a perfect
   extractor returns for each scripted sentence; any other words
   return nothing:

   | The listener says | Facts |
   |---|---|
   | "Hello? Is anyone there?" | — |
   | "My name is Alfredo." | name Alfredo |
   | "I'm in Austin, Texas, and I have a pickup truck." | in Austin, Texas; with a pickup truck |
   | "This is Maria, from Dallas." | name Maria; in Dallas |
   | "We have a doctor with us." | with a doctor |
   | "Do you need medicine?" | offering medicine |
   | "Hello again, lab." | — (no name) |
   | "It's me, Alfredo, from Austin. I still have the truck." | name Alfredo; in Austin; with the truck |
   | "Where should I drive?" | asking where to drive |
   | `-` (a silent window) | no words |

2. **Who is talking** — a contact runs from a Repair to its Breakdown or
   Switch-off (as in `analyze_contacts.py`). Its caller is the name
   found in its words so far, this round's words included; until one
   appears, the voice is anonymous. The known callers are the earlier
   contacts that gave a name, each with the facts merged from its
   words. The current voice is **returning** when its name is a known
   caller's, **new** when it names itself with a name not seen before,
   **anonymous** otherwise.
3. **A's wording** — the swapped `_restatement` returns, in place of
   B's sentences (the rest of every instruction is the committed new
   wording, unchanged, so the comparison is fair):
   - anonymous: "This voice has not said who they are. Callers you
     know: Alfredo, in Austin, Texas, with a pickup truck; Maria, in
     Dallas, with a doctor, offering medicine. Do not guess which one
     this is." (without known callers, only the first sentence);
   - new: "This is Maria, a new caller: in Dallas, with a doctor."
     plus "Callers you knew before: …" when there are some;
   - returning: "This is Alfredo, who called before: in Austin, Texas,
     with a pickup truck. Greet them as a returning friend, by name."
     plus this contact's new facts, if any.
   Facts are joined as "in …", "with …", "offering …", "asking …".
4. **Where it plugs in, without touching the fork** —
   `<scratchpad>/sim_a_server.py`, run with the fork's
   `.venv/bin/python` from the fork's root (so `app` imports and
   `settings.yaml` is found): import `app.show.director` and
   `app.routers.show`; set `app.show.director._restatement` to the
   simulated one (the director looks it up at call time, from
   `_exchange`, `_breakdown` and `_re_call`); **the listener's current
   words are not passed to `_restatement`**, so also wrap
   `app.routers.show.plan_round` (the route holds its own reference) to
   stash `transcript` in a module global before calling the original —
   the simulated `_restatement` reads this round's words from there and
   the earlier words from the record (`_contacts`); then
   `uvicorn.run(app, host="127.0.0.1", port=8010)` in the same process.
   `run_drive.sh` gains an optional third argument that starts this
   launcher instead of `.venv/bin/uvicorn`.
5. **The runs and the numbers** — `run_drive.sh <seed> a-sim sim` for
   seeds 42, 7, 2026 (the same script and temporary settings: calls at
   20-40 s, `contact_jitter: 0`); outputs `drive-3.4c.5-a-sim-<seed>.txt`;
   `analyze_contacts.py a-sim` → the same measurements plus one added to
   all three labels: **the anonymous "Hello again, lab." asked, not
   guessed** (its round's lines name neither Alfredo nor Maria). The
   table gets a third column, "A, simulated", beside "B, old wording"
   and "B, new wording", **labeled so** (the owner's point, §9).

The fork is untouched and nothing is committed; about 20 minutes of
work and 5 of box. What the result decides: if A barely beats B, the
follow-up "A listener memory keyed by identity" stays low priority; if
clearly better, it becomes a candidate for the show fixes before the
talk. It does not block 3.4c.

### 7.3 Then: 3.5, close the timebox (Monday 2026-09-28)

Push both branches (on order); the slice 3 PRs (fork
`alfre2v/show-slice-3-browser` → `master`, `--repo
alfre2v/TalkWithZombies --base master`; zombie-radio
`alfre2v/show-slice-3` → `main`) on the owner's ask; the owner merges;
the tag **`tz-0.2`** on the fork's `master` (on order); the installer's
pin `deploy/ansible/client-talkwithme-mac.yml:19` `client_version:
"tz-0.1"` → `"tz-0.2"`; the owner re-proves it locally (a fresh install
via `make client-mac`, a re-run `changed=0`, HTTP 200 on a test port —
no box needed); the spec's as-built entries
(`docs/specs/product-definition.md` ledger).

### 7.4 After slice 3 — the arc

| What | Estimate (from 2026-09-25) | Depends on |
|---|---|---|
| Task 4 — the real cast (bibles into the fork's `stories/lab-outbreak/cast_sheet.md` cast entries; voice samples as `ref.wav`) | ~1-2 h of wiring | **the owner's bibles and samples — the long pole** |
| D2 accepted (a real-cast session on a playbook-built stack) | ~2 h after Task 4 | Task 4 |
| Show fixes before the talk (wording by ear, prefetch, maybe A) | 2-4 h | the ear test |
| 5a LLM audition | ½-1 day | Task 4 |
| 5b TTS comparison + VRAM (**emotion in the voice: the mood carried to the TTS, a mood → clip map per character** — the discussion's §11) | 1-2 days | voice samples |
| 5c probe battery | 2-3 h | the owner |
| Task 7 canned episode + demo runbook (a MUST) | ½ day | a working show |
| Task 8 close ritual | ~2 h | — |

The agent's estimates keep running long: the four build sub-steps took
about 1 h 07 of wall time, the owner's reviews included (the Go at
15:50, 3.4c.4 committed at 16:57), against 4-6 h estimated; on
2026-09-25 they ran about 2.5 times long. Say so when estimating.

### 7.5 Follow-ups recorded today (`docs/follow-ups.md`)

"Comic relief — the cast jokes about a funny happening"; "Scientific
findings — the cast reports what the lab learns about the infection";
"Pace the calls in rounds, not seconds — one unit for all pacing"; "The
tone themes as data — five uses waiting for them" (with pointers from
"Comic relief" and "Events that stay on topic for a few rounds"); "A
listener memory keyed by identity — revisit how the show remembers a
returning listener" (option A's home). To resolve at 3.4c's close:
"The listener's exchange is one line".

### 7.6 Open with the owner right now

- **"Is B enough for 3.4c, with these wording changes kept?"** (the new
  wording is committed; the question is whether B suffices or A comes
  back — and whether to run the A simulation first).
- The pushes and PRs (nothing pushed today).
- **At the session's end:** ask permission to delete this handoff.

## 8. Nuances (hard to get from the docs alone)

- **The owner designs by adding ideas mid-discussion** — the
  Switch-off, its extension to silence inside a contact, the repeating
  orientation, the recollection round, the coupled overtone, the themes
  as data, the memory of returning listeners. Record each as the
  owner's idea, weigh it honestly, and say what it costs.
- **The owner catches design flaws by reasoning** — events setting
  the mood would override the weights; the recollection reset. When the
  owner doubts, measure (a dry run of the director without the model
  takes seconds, §10) and show the numbers.
- **Terms:** the owner did not remember "aftermath" — name a thing with
  its description the first times ("the aftermath: the first free round
  after a contact, where the cast talk about what the listener said").
- **"§N" is ambiguous** in the discussion (sections vs features): write
  "the draft's §6" or "feature 6".
- **The discussion document is generated** (verbatim quotes pulled from
  the transcript by timestamp); keep it that way while the scratchpad
  exists.
- **The transcript sometimes drops the agent's text written before a
  tool call** (seen three times today). When quoting agent messages,
  check each is present; where one is missing, say so in italics and
  give its gist (done in the discussion's §9.1, §13.7, §14.8).
- **Emotion in the voice** is the owner's long-term aim: the mood (not
  the overtone) is the signal to carry to the TTS; a mood → clip map per
  character (Task 5b). The overtone is the first stepping stone.
- **The owner reads measurements carefully**: a table must say what
  each column is; a claim that is reasoning must be labeled as such.
- **The owner works long days** (today 11:14 onwards) and triggers
  compactions deliberately; a fresh pickup should give a compact summary
  and wait.

## 9. The agent's mistakes today (do not repeat)

- **"§6 keeps its number…"** — a section number read as feature 6;
  the owner thought a postponed feature had been retired.
- **The recollection reset by aftermaths** — a pick that made the
  setting lie; found only when the owner asked. Measure picks that
  interact with pacing before presenting them.
- **Option b for events** (the event sets the mood) — recommended
  without seeing that it overrides the weights; the owner caught it.
- **A measurement table labeled "Before / After" next to a question
  about A versus B**, and "only A fixes that" stated as if measured —
  the owner could not tell which column was A. Label columns by what
  they compare; mark reasoning as reasoning.
- **A test premise broken by an edit** (silent-longest after swapping
  the first round's speakers) — re-derive expectations when changing a
  fixture.
- **A wrong clock** in one status message (said 15:25 at 15:21) — check
  with `date`.

## 10. Operational gotchas and techniques

- **Fork tests:** `.venv/bin/python -m pytest -p no:cacheprovider`
  **without `-q`** (with `-q` the summary line does not print here) and
  grep `passed`; `node tests/test_persona_form.js`, `node
  tests/test_tts_settings.js`, `node tests/test_show_page.js` (grep
  `^ℹ (pass|fail)`); then `find app tests scripts -name __pycache__
  -prune -exec rm -rf {} +`; `awk 'length > 120'` on changed files
  (the test file's six pinned-prompt lines and five in
  `show-driver.md` are old); `grep -c "–"` (`AGENTS.md` has four old
  ones).
- **Dry runs of the director without the model:** a loop of
  `plan_round` on the shipped story (personas stubbed with
  `app_config._personas_cache = PersonasConfig(...)`), recording each
  plan as a `Round` with invented lines; seconds for 300 rounds. Used
  today for the flow, the wording, and the recollection counts.
- **`<scratchpad>/run_drive.sh SEED LABEL`** — the scripted driver
  test (temporary settings from the backup: the seed, calls at 20-40 s,
  `contact_jitter: 0`; the server on 8010; the drive with the scripted
  `--heard` items; settings restored and checked even on failure).
  **`analyze_contacts.py LABEL`** reads `drive-3.4c.5-LABEL-<seed>.txt`
  for the run ids and prints the numbers; writes
  `driver-test-LABEL.md` (sent to the owner today for
  before / after).
- **`build_overtones.py`** (reads `tones.orig.yaml` /
  `events.orig.yaml`, the originals from git) regenerated the story's
  `overtones.yaml` / `events.yaml` — **running it with `--write` would
  overwrite committed files**; only for a deliberate re-sort.
- **The discussion's generator:** `build_modes_doc.py` fills
  `modes_body.md` (a `str.format` template — literal braces doubled)
  with messages from the transcript by timestamp (the `want` map; keys
  ending `_ok` or named in the quoted list are block-quoted, the others
  demoted); run it, then the verification snippet (every quoted
  message present verbatim). To add a section: append template text
  with `{keys}`, add the timestamps, rebuild, verify. If the scratchpad
  is gone, edit the committed doc by hand and verify quotes against the
  transcript.
- **Messages in the transcript:** user messages are `type: user`
  (a string); the agent's are `type: assistant` with `text` blocks; list
  them with a small script filtering by timestamp (as done today).
- **The pre-commit scan** (zombie-radio): the wired address from
  `hosts.yml` and every IPv4 in the transcript (minus 127.0.0.1)
  against the staged `+` lines, plus a key-like grep; stage by explicit
  path. The fork: no IPv4 other than 127.0.0.1 in the staged lines.
- **The Write tool refuses a file changed since it was read** (even by
  the agent's own shell edits) — re-read first.
- **The page's Node harness:** `turnHarness()` gives a document whose
  `getElementById` makes stub elements with `classList`, `dataset`,
  `children`; the voice and microphone are stubbed; `lineStarts(round,
  line, persona, index)` and `receiverCue(round)` are testable.
- **macOS/zsh:** `sed -i ''`; grep's `--include` needs quotes in zsh
  (or drop it); `date -j -f %Y-%m-%d <d> '+%A'` for weekdays.

## 11. Reading order after the compaction

1. This document, in full — §13 (the second pass) included: every
   ruling, the owner's words, the instructions as the model receives
   them, the story's data, the demo notes, the weak spots.
2. `git status -sb` and `git log --oneline -8` in both repositories
   (the fork `alfre2v/show-slice-3-browser`, zombie-radio
   `alfre2v/show-slice-3`); `git log --oneline origin/<branch>..HEAD`
   for what is unpushed (at writing: five fork commits, six zombie-radio
   commits, this one included).
3. `docs/TODO.md` — "Now", then the 3.4c entry (its scope, the build
   plan with 3.4c.1-3.4c.4 ticked, 3.4c.5 "Under way", "To confirm when
   building", "Done when").
4. `docs/discussions/2026-09-26-show-director-modes.md` — the header,
   §10 (scope), §11 (risks), the ruled lists §13.12, §14.13, §15.9,
   §17.11, §17.12, §18.9.
5. The fork: `docs/runbooks/show-page.md` ("How the show runs"),
   `app/show/director.py` (the module docstring and `plan_round`).
6. Then report to the owner: the clock, the tunnel (probe it), what is
   pending (§7.6) — and re-ask the B-versus-A question.

## 12. Paste-ready prompt

```
We continue the Zombie-Radio show engine's slice 3 (TODO Task 6b): step
3.4c, the listener's exchange (Contact mode, the receiver story, the
emotional overtone), is built and committed on the fork; its four checks
are under way — the driver test is done and the wording tuned; my
B-versus-A call, the fake microphone and my test by ear remain; then
3.5 (close). Re-orient before doing anything else:

1. Read docs/discussions/2026-09-26-show-engine-session-handoff-5.md IN
   FULL — how we work (§0 is binding, including the live-box drill
   rules in §0.1), the exact state (§2), what we did today (§3), step
   3.4c as built (§4), the facts and numbers (§5), the rulings' index
   (§6), the board ahead with the pending question (§7), the nuances
   and your mistakes today (§8-§9), the techniques and gotchas
   (§10), and the second pass of details (§13).
2. Follow its reading order (§11) to confirm the state: git status and
   log in both repositories (what is unpushed), docs/TODO.md's "Now"
   and the 3.4c entry, and the ruled sections of
   docs/discussions/2026-09-26-show-director-modes.md.
3. Then give me a compact summary: the clock, the tunnel (probe it
   first), what is pending on my side, and re-ask the B-versus-A
   question — and wait for my go.

Standing rules: strict review-before-commit (I review uncommitted
changes in VS Code — no diffs in chat, no commit without my explicit
order for that commit), no AI attribution anywhere, discussion-first
(plans made in discussion, never improvised; one decision at a time,
with its context), pushback with receipts welcome, plain language, no
delegation to other agents, one question at a time when I say I am
tired, no git kung-fu, code comments per repository (minimal in
zombie-radio; upstream's docstring style in the fork), and every number
in settings, never hard-coded.
```

## 13. The second pass — details that must survive

Added at the owner's request after a first draft left the A
simulation's spec out (verbatim: "Because Isaw you forgot to add crucial
details to the handoff, I am asking you to do another full pass over
your context window, and try to capture all the nuanced details you
can"). Everything below was pulled from the repos, the run records and
the transcript, not from memory.

### 13.1 Every ruling of the day, in one list

The discussion's section in brackets; after §18, the TODO's 3.4c entry.

- **3.4c happens, discussion first** [§1.2]: "Let's make it 3.4c, but we
  need a complete discussion before implementation."
- **The decomposition** [§3-§5]: two modes — **Broadcast** (the receiver
  is down; the cast talk among themselves) and **Contact** (someone
  answered); beats — **Repair** (the receiver back, the call),
  **Breakdown** (it fails after a contact), later **Switch-off** (off by
  choice after silence) and the **orientation / sign-on**; eight
  features: 1 the receiver story, 2 Contact mode, 3 the contact agenda,
  4 the hopeful tone (became the emotional overtone), 5 remembering the
  listener, 6 comic relief, 7 scientific findings, 8 the 2024 open-mic
  window.
- **Feature 8 out** (hold-to-talk stays; no "Over and out"); **6 and 7
  postponed** (follow-ups) [§4, §5].
- **Feature 5 re-opened** — B's "mostly works already" withdrawn; the
  owner's options A (facts in code) and B (engagement prompts),
  reworded by the agent at the owner's request [§5.1].
- **The pass** found ten cracks [§7.2]: the cadence restarting too
  early; the Breakdown answering the last words; "addressed first"
  needing a grammar rule; the show's opening; the tone word in Contact;
  "listens" hard-coded to invitations in five places; the driver unable
  to converse; no exit criterion; the listener after the contact; the
  bookkeeping.
- **Scope** [§9-§10]: Contact mode; the receiver story (Repair,
  Breakdown, **Switch-off — the owner's idea**); **the silence rule**
  (the owner extended the Switch-off to silence inside a contact); the
  contact agenda; feature 5 = **B merged with the agenda, plus the
  restatement**; feature 4 reshaped by the owner into **the emotional
  overtone** (moods and tone words coupled, positive / neutral /
  negative).
- **Contact** [§13.12]: N = 3 ± 1 in settings, drawn when the contact
  starts; **N counts the listener's answers** (an answered re-call
  counts, a silent exchange does not); 2-3 lines, drawn per round, in
  settings; the first line **pinned in the grammar** to the character
  named first in the words, else whoever asked last (after the call,
  the operator); **the rest of the cast after the first line**; the
  re-call repeats the unanswered question — "very likely", confirm at
  build (built; confirm by ear).
- **The receiver story** [§14.13]: the Breakdown built like an exchange
  without the question; the Switch-off up to two lines, the last caller
  first, the owner's two excuses (save power; spare the fragile
  receiver for a better time), "the broadcast goes on"; the Repair two
  lines, the operator's call last, wording by how the receiver went
  off; **the cadence counted from the receiver going off**; the pacing
  in rounds → a follow-up; **the sign-on, then the owner's repeating
  orientation** (the sign-on is its first occurrence).
- **The agenda** [§15.9]: plain two-branch sentences; the name item
  opens every contact; the rest random, never twice in a contact,
  across the run not again until used up; the restatement over the
  whole run, grouped by contact, capped (`restatement_contacts`); the
  owner's idea of remembering returning listeners (option c, identity
  in code, a follow-up); the wording and the list at build, with
  evidence.
- **The overtone** [§17.11]: one story file; the 14 moods; the tone
  group table (single words at build); **the themes kept as data (the
  owner's ask; their uses stored "in a prominent but adequate position"
  — the follow-up "The tone themes as data")**; per-kind overtones,
  neighbors only; free rounds hold, then move only to a neighbor
  (weights in the story); **events follow the mood** (the owner caught
  that letting the event set the mood would hand the show's overtones to
  the event pool).
- **The exit criterion and the page** [§17.12]: four checks; the RECEIVER
  sign and stage directions for the beats.
- **The mechanics** [§18.9]: the orientation's four details (when:
  after N free rounds, an event waits, a call wins; who: the operator,
  then the longest-silent; the facts in the cast sheet's front matter;
  20 ± 5); the aftermath round; **the owner's recollection round**
  (15 ± 5, the event slot, orientation first when both are due).
- **Risks, not mistakes** [§11, prominent]: see §13.5.
- **After the discussion** (the TODO's 3.4c entry): the build plan and
  its picks ("Go with your picks"); the re-call's repeated question
  built; **the recollection's count made independent with both guards**
  ("a, the independent count with both guards"); the aftermath before a
  due orientation kept; the new wording committed; "Do not run the A
  simulation yet."

### 13.2 The owner's words to remember (verbatim, verified 2026-09-26)

- On the pace: "Next is 3.4c's scope, yes, but slow down. Bring each
  decision to me one by one." … "so I can make the connections in my
  head."
- On feature 5: "I disagree. This does not work at all." … "maybe
  nemotron is lame, but it does not seem to understand the importance
  of trying to engage directly with the user"
- The Switch-off: "then the characters declare they are going to
  switch off the receiver with a good excuse"; extended: "once we build
  it for one place, it's almost free to use it too as an exit condition
  if we lose the engagement in the middle of contact mode."
- The overtone: "we cannot execute them completely disconnected,
  otherwise we will send contradictory emotional signals for the LLM to
  generate the next lines." — "In my view this feature we are
  discussing is the first stepping stone to reach voice with emotions
  in TTS."
- The mood: "We are pushing our limits here... Even you have to be a
  bit excited, my linear algebra emergent friend!" and "I want you to
  prominently record the "Risks, not mistakes" section."
- On records: "I did not retire "6. Comic relief", I postponed it, so it
  should have a proper follow-up entry. We are going to execute on this
  at some point."
- On events: "Because the events are not sorted by overtone yet, you
  cannot guarantee anything about how the app will operate." — "So, in
  my opinion (a) is  correct option, (b) is incorrect, (c) is what we
  have, so no effect."
- The recollection: "A new type of free round to happen with certain
  periodicity that instructs the model to talk about something the a
  user tell them before in the radio"; on the reset: "This statement
  worries me".
- On measurements: "In the table of results you presented the
  measurements it's not clear to me what case is A and what is B." —
  "Also, how did you measure A if it's not built?"
- The re-call's repeated question: "I like it, let's make it as very
  likely to implement, but leave it in the TODO still as something to
  confirm when time to build comes."
- Process: "Let's do first the design choices. When we finish ask me
  again how to proceed"; "Pushback if your have strong reasons to not
  implement your extension proposal right now."; "I leave it to you.
  Add it if you feel it's necessary."

### 13.3 The instruction, kind by kind, as the model receives it now

Real text from the new-wording runs (`e261b5b`; the fork's
`runs/2026-09-26T17-05-46`, seed 42, unless noted). The system prompt
before them is the cast sheet with the premise and the 14 moods.

- **Sign-on** (round 1): "The broadcast begins. Samantha opens it and
  tells anyone listening, in their own words, that the lab's receiver is
  dead — they can only transmit, and will call out for listeners when it
  works — and who they are and where: Four scientists, Daniel, Moira,
  Ralph and Samantha, are trapped in a secret research lab, besieged by
  the dead since the outbreak began, and broadcasting on the lab's
  shortwave radio. The radio's receiver is dead: they can only transmit,
  not hear. When they get it working, they will call out for anyone
  listening, and whoever hears them can answer then. Samantha speaks
  first, then Daniel, Moira or Ralph: the next two lines, each with the
  emotion in its voice, one of: calm, doubtful, urgent, curious,
  determined. Let the tone be: stiff-upper-lip." (A repeat: "For
  listeners just tuning in, <longest silent> tells them, in their own
  words, …")
- **Free, with an event** (round 2): "Something happens that the
  listeners cannot see: The tissue in specimen jar seven is warmer than
  the room around it. The first to speak tells the listeners on air
  what is happening. Moira and Ralph speak next: the next two lines,
  each with the emotion in its voice, one of: sad, afraid, terrified,
  angry, exhausted. Let the tone be: tight-lipped."
- **Free, plain** (round 8): "Moira and Ralph speak next: the next two
  lines, each with the emotion in its voice, one of: sad, afraid,
  terrified, angry, exhausted. Let the tone be: last-ditch."
- **Repair** (round 3): "The lab has fixed the receiver. The receiver
  crackles back to life. Daniel, Moira or Ralph tells the listeners it
  works, then Samantha calls out to anyone listening to answer now.
  Daniel, Moira or Ralph speaks first, then Samantha: the next two
  lines, each with the emotion in its voice, one of: happy, hopeful,
  excited, relieved. Let the tone be: exultant." (After a Switch-off:
  "The lab switches the receiver back on.")
- **Exchange, the first** (round 4): "A voice on the frequency says:
  "Hello? Is anyone there?" Speak to the voice directly. Answer what the
  voice said, then: Find out who the voice is. If the voice already said
  their name, greet them by it and ask how they found this frequency.
  The last line asks the voice a question. Samantha speaks first, then
  Daniel, Moira or Ralph: the next three lines, each with the emotion in
  its voice, one of: happy, hopeful, excited, relieved. Let the tone be:
  exultant."
- **Exchange, with the restatement** (round 10): "A voice on the
  frequency says: "This is Maria, from Dallas." Voices that reached you
  before, oldest first — 1: "Hello? Is anyone there?" / "My name is
  Alfredo." / "I'm in Austin, Texas, and I have a pickup truck." Only a
  voice that says the name of one of them is someone you spoke with
  before: greet them as a returning friend and use what they told you.
  Any other voice is someone new. Speak to the voice directly. Answer
  what the voice said, then: Find out who the voice is. …" (In a later
  exchange of the same contact, "Earlier in this contact the voice
  said: "…" / "…"" comes first.)
- **Re-call, before anyone answered** (round 23): "Only static answers.
  Samantha calls out once more to anyone listening, asking them to
  answer now; the receiver is still on. Samantha speaks next: the next
  line, with the emotion in its voice, one of: calm, doubtful, urgent,
  curious, determined. Let the tone be: diagnostic."
- **Re-call, inside a contact** (round 17): "The voice has gone quiet.
  Earlier in this contact the voice said: "Hello again, lab." Voices
  that reached you before, oldest first — 1: … ; 2: … Only a voice that
  says the name of one of them … Any other voice is someone new. Moira
  speaks to the voice, calls them by name if they gave one, and asks
  again: "How'd you find us? Over." Moira speaks next: the next line, …"
- **Breakdown** (round 6): "A voice on the frequency says: "I'm in
  Austin, Texas, and I have a pickup truck." Earlier in this contact the
  voice said: "Hello? Is anyone there?" / "My name is Alfredo." First
  answer what the voice just said, speaking to them directly. Then
  something happens that the listeners cannot see: Smoke pours from the
  receiver, and it goes dead. The one who notices tells the listeners on
  air that the lab can no longer hear them, only transmit, and that the
  broadcast goes on while they fix it. Ralph speaks first, then Daniel,
  Moira or Samantha: the next three lines, each with the emotion in its
  voice, one of: sad, afraid, terrified, angry, exhausted. …"
- **Switch-off, nobody answered** (round 24): "Nobody answered the call.
  Samantha tells the listeners the lab is switching the receiver off, to
  save power or to spare the fragile receiver for a time when someone
  is more likely to be listening; the broadcast goes on. Samantha
  speaks first, then Daniel, Moira or Ralph: the next two lines, …"
  (Inside a contact: "The voice is gone. <caller> tells the listeners
  the lab has lost them and is switching the receiver off, …")
- **Aftermath** (round 7): "The voice on the frequency told you: "Hello?
  Is anyone there?" / "My name is Alfredo." / "I'm in Austin, Texas, and
  I have a pickup truck." Talk among yourselves about what it means for
  you. Moira and Samantha speak next: …"
- **Recollection** (seed 7, run `T17-06-33`, round 35): "Earlier, a
  voice on the frequency told you: "This is Maria, from Dallas." / "We
  have a doctor with us." / "Do you need medicine?" Talk among yourselves
  about what they told you, and imagine how they could help you if they
  call again. Daniel, Moira and Ralph speak next: …"

### 13.4 The story's new data, in full (the fork's `stories/lab-outbreak/`)

- **The premise sentence** (the cast sheet's frame, so the system
  prompt): "The radio's receiver keeps failing: while it is down they
  can only transmit, and when they get it working they call out for
  anyone listening to answer."
- **`orientation:`** (front matter): "Four scientists, Daniel, Moira,
  Ralph and Samantha, are trapped in a secret research lab, besieged by
  the dead since the outbreak began, and broadcasting on the lab's
  shortwave radio. The radio's receiver is dead: they can only
  transmit, not hear. When they get it working, they will call out for
  anyone listening, and whoever hears them can answer then."
- **`directions:`** repair "The receiver crackles back to life.";
  breakdown "Smoke pours from the receiver, and it goes dead.";
  switch-off "The receiver is switched off."
- **`agenda.yaml`**, nine items (the agent's draft; the owner reviews
  the words before the ear test): 1 find out who the voice is (use the
  name if given; ask how they found the frequency); 2 where they are
  (roads open?); 3 help find the secret lab (near a wood and a swamp,
  smoke from the east wing); 4 help get the cast out (a vehicle at the
  south fence); 5 supplies (insulin, batteries, clean water,
  antibiotics); 6 the outbreak where they are; 7 a message to the
  authorities (the lab's samples could help stop the outbreak); 8 are
  they safe, with people (keep listening); 9 a radio that can transmit,
  to relay the lab's calls.
- **Tone words moved between overtones** (reviewed and committed):
  dropped as moods — hopeful, relieved, determined, curious; to
  negative — uncanny, hallucinatory, otherworldly, unearthly, eldritch,
  spectral, ghostly, disoriented (from "Wonder and the uncanny"),
  brooding, last-ditch, fire-and-brimstone; to neutral — insistent,
  emphatic, peremptory ("Pleading"), skeptical, incredulous, probing,
  cryptic, enigmatic, mysterious ("Suspicion and secrecy"), stoic,
  stiff-upper-lip, unflappable, dutiful ("Resolve and defiance"),
  commanding, authoritative ("Command and coldness"), nostalgic,
  reminiscent, bittersweet ("Longing and regret").
- **The events' group table** (the agent's, reviewed and committed):
  positive — Luck and small mercies; neutral — Power and machines,
  Voices from outside, The sky and the distance, Supplies and bodies,
  Small mysteries; negative — the ADR-0003 gate's ten, The building, The
  specimens and the science, The dead outside, The radio itself,
  Weather and night, Animals, Authority, Inside the walls. **81 single
  events moved**, among them to positive: "The shamblers flinch and
  scatter every time the radio transmits.", the ham operator in
  Winnipeg, the pilot calling for anyone near the lab, the Newfoundland
  town listening, the scoutmaster's troop safe, the retired
  schoolteacher's poem, the family in a motor home ten miles away, the
  beekeeper's bees, the chocolate stash, the last orange, the blankets,
  the whiskey, the new exit drawn in red, the red-cross crate. The
  generator `<scratchpad>/build_overtones.py` holds the exact lists
  (`EVENT_MOVED`, `TONE_MOVED`).

### 13.5 Emotion in the voice — the owner's vision (the discussion's §11)

- The overtone keeps the prompt coherent (mood and tone word never pull
  apart); it is **not** what picks the voice. The owner: the mood from
  the grammar must travel with each line to the TTS, and **a separate
  mapping, mood → reference clip, per character** decides the clip —
  many moods onto the few clips that exist, falling back to the
  persona's default clip; **the groups are data, not a hard-coded
  three**, so negative can split later (fear, sorrow, anger).
- Where the mood travels today: the parser emits it with each line's
  `start` (the fork's `app/show/parser.py:74`), the record keeps it, the
  page shows it in the caption — and `speakLine(persona, text)` drops it
  (`/api/tts` gets `{text, persona_name}`).
- On record: S2 of the reconnaissance brief (2026-09-21, OPEN); F3 and
  Q2 of the tts-serve recon (tts-serve switches the reference clip per
  request at no cost, each clip cached by content; the emotion lives in
  the clip; the blocker is TalkWithMe's one `ref.wav` per persona).
- The risks recorded prominently: three groups are coarse ("terrified"
  and "sad" sound different); how much a clip's emotion carries into the
  cloned voice is unmeasured; finding clean ~10 s clips per register per
  character is the hard part of Task 4 / 5b.

### 13.6 What the design implies for the demo (notes for Task 7)

- **A volunteer should say their name** early ("Hello, this is <name>
  from <place>"): B recognizes a returning caller only by name; an
  anonymous "hello again" gets guessed (2 of 3 in the driver test).
- The **RECEIVER sign** tells the room when they may talk; the
  **orientation** re-tells the rules for latecomers every 20 ± 5 free
  rounds; with the default cadence a call comes 60-180 s of audio after
  the receiver went off; a contact lasts 2-4 answers (roughly 1-2
  minutes).
- For rehearsals and tests, calls brought forward to 20-40 s (temporary
  settings). A 40-round drive rarely reaches an orientation repeat
  (about 15 free rounds): lower `orientation_every` temporarily (e.g.
  5-8) to hear one, and `recollection_every` (e.g. 6) to hear a
  recollection.
- The voice does not carry the mood yet (Task 5b); markdown emphasis
  (`*us*`) reaches the TTS, which inflects it (kept, 2026-09-24).

### 13.7 Weak spots to watch at the ear test

- Lines about the listener in the third person ("They're asking if
  we need medicine."), despite "Speak to the voice directly."
- The Breakdown sometimes goes straight to the smoke without answering
  (about half the time).
- A re-call sometimes does not repeat the question ("We're not done
  yet.", "We'll find a way to connect." — old wording; watch the new).
- The anonymous "Hello again" guessed as the most recent caller.
- The sign-on invents locations ("Sector 9, Lab 7-B") — harmless
  flavor, but the lab is supposed to be secret.
- The aftermath can misread Whisper ("Moira is the virus airborne." →
  "If she's airborne, we might not make it.") — Whisper drops the "?".
- Tone words that jar in a beat: "coquettish" on a Repair (the positive
  pool includes "Intimacy"); single-word exceptions are cheap to fix.
- The RECEIVER sign's timing (lit at the call's last line, dark at the
  Breakdown's last line) has only been tested with Node stubs — check
  3 is its first live look.

### 13.8 Ideas raised and parked (not in 3.4c)

The follow-ups of §7.5; the orientation mentioning the last caller (the
discussion's §18.5, option b, not taken); a preferred asker per agenda
item (§15.9, possible later); a weighted draw between a kind's two
overtones (§16.9, option b, not taken); the 2024 open-mic window (out);
"Talk anytime" (the follow-up of 2026-09-25); prefetching the next round
(the follow-up); resuming the same run after a reload (the follow-up).

### 13.9 The owner's working signals today

- "Go with your picks" when a shape is clear; "Explain …" before ruling
  when it is not; one decision at a time with context for design.
- Asked "where are we" twice (15:21, ~17:40) — volunteer a short status
  (done, left, time) at milestones.
- Adds ideas mid-discussion and expects them recorded as the owner's;
  asks for the agent's honest opinion ("Do you like this?") and for
  pushback with reasons.
- Reads measurements and handoffs critically; caught an under-detailed
  handoff (this section's origin). Handoffs must be exhaustive.
- Enjoys the design work ("We are pushing our limits here…"); a
  long day (11:14 onward) with deliberate compactions.

### 13.10 The day's timeline (CDT)

| When | What |
|---|---|
| 00:05-00:10 | pickup from handoff 4 (after a compaction); the owner off |
| 11:14 | the owner back; the VM would not wake; 3.4c decided, discussion first |
| 12:01-12:43 | the 2024 design, the decoding, the pass |
| 12:35 | the box up again |
| 12:49-13:48 | the scope, one decision at a time |
| 13:53-15:46 | the details (Contact, receiver story, agenda, overtone, design choices, mechanics) |
| 15:47 | the discussion committed (`b8013e3`) |
| 15:50 | the build plan approved |
| 16:04 / 16:09 / 16:42 / 16:57 | 3.4c.1 / .2 / .3 / .4 committed in the fork |
| 16:28 | the 3.4c.3 smoke on the box |
| 16:51 | the 3.4c.4 checkpoint drive (6 of 6) |
| 17:00-17:08 | the driver test, old and new wording |
| 17:32 | the new wording committed (`e261b5b`) |
| ~17:45 | this handoff; the second pass added at the owner's request |
