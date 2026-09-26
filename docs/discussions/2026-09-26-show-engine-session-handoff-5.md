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

A launcher in the scratchpad starts the app with the director's
`_restatement` swapped in memory for an A-style one: a hand-written
table of what a perfect extractor returns for each scripted sentence
(name, place, what they have; "Hello again, lab." → nothing), and
instructions that state conclusions ("This voice has not said who they
are. Callers you know: Alfredo, in Austin, Texas, with a pickup truck;
Maria, in Dallas, with a doctor."; "This is Alfredo, who called before:
… Greet them as a returning friend, by name."). The same three seeds,
script and measurements, a third column "A, simulated" — A's best case.
The fork untouched, nothing committed. About 20 minutes and 5 minutes
of box.

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

1. This document, in full.
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
   and your mistakes today (§8-§9), and the techniques and gotchas
   (§10).
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
