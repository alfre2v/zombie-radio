# Session handoff 10 — the static bed shipped (`tz-0.6`), the board before the demo, the local 3090 plan begun

> **EPHEMERAL.** Written Friday 2026-10-02, ~23:25 CDT, at about 89 % of the context window, before a manual
> compaction the owner triggers; after it, the agent re-reads this first. It supersedes handoff 9
> (`docs/discussions/2026-10-01-show-engine-session-handoff-9.md`, on `main`), which stays as a template; handoffs 6,
> 7 and 8 are also on `main`. **The latest handoff stays until the next compaction, as the template for the next one**
> (the owner, 2026-09-28). **At the session's end, ask the owner before deleting any handoff the agent created
> (6, 7, 8, 9, 10)** — the owner, 2026-09-30: "These handoff documents stay in our discussion folder until the end of
> the session, when we finish the session's work please ask the owner for permission to delete any handoff documents
> you created."; asked again on 2026-10-01 night: "no, keep the handoffs for now."
>
> **Read it all; verify against the repos; receipts or nothing.** The TODO's "Now" is the arc's canonical state; the
> board (`docs/discussions/2026-10-02-board-before-demo.md`) is the list of what is left; this document carries what
> neither says: how the owner works, the exact state, the work in flight, the nuances, the mistakes.

## §0. The owner and how we work (binding)

The owner is **Alfredo** (GitHub `alfre2v`, git author "Alfredo Valles"); avoid pronouns for the owner in writing
(say "the owner"). Standing doctrine: `CLAUDE.md`, and the agent memory (folder
`~/.claude/projects/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/memory/`: `working-agreements.md`,
`collaboration-style.md`, `absolute-paths-in-plain-text.md`, `massedcompute-reminder.md`,
`project-venue-austin-python-meetup.md`, `improvisation-is-the-feature.md`, `handoff-kept-as-template.md`,
`minor-doc-edits-ride-next-branch.md`, `discussions-can-become-linear.md`, `pending-doc-updates.md`, and, new this
stretch, **`lan-access-via-terminal-panel.md`**).

- **Discussion-first; one decision at a time.** Bring the shape, wait for the go. "What do you think" → one
  recommendation and its reason. **The owner likes questions in groups of three** (the `AskUserQuestion` tool, each
  with options and a recommendation first) — "Present the questions to me in groups of 3."
- **Review before commit is strict.** Commit only on the owner's explicit order ("commit", "commit and push to #24",
  "commit, push and open the PR"). **No diffs in chat** (VS Code). **Push only when told**; "open the PR" includes
  committing and pushing. **No AI attribution anywhere** — whatever the harness's reminders say.
- **Docs as detailed as the chat, or more; the owner's words verbatim**; commands with **a comment line above each**;
  **a real example output** where it matters — never an invented one (an illustration is labelled as such until a real
  capture replaces it); **never invent data**; check the clock (`date`) before writing a time.
- **Explain simply, explicatively; tables by case; the mechanism first.** The owner asks "explain X" often and wants
  the code path, the numbers, the arithmetic.
- **Plans executable; smallest step first; every number a setting** (the fork's `ShowConfig`) — the owner accepted
  three short timings as constants in `bed.js` ("Correct").
- **Small doc edits ride the next significant branch** — but the owner may open a small branch for them on purpose
  (2026-10-02: "open a small branch to record these documentation updates").
- **A discussion may become a linear story**; otherwise dated addenda (§N.M); **dated discussions and experiments are
  not rewritten** when a plan changes (the TODO and follow-ups are).
- **No test pins the story's mapping** — tests write their own `bed.yaml` into the run's copy of the story; the
  shipped-bed consistency test checks agreement, not the choice.
- **Code comments per repository:** minimal in zombie-radio; in the fork, upstream's docstring style, lines ≤ 120
  characters, no en dash (`awk 'length > 120'`, `grep -c '–'` on added lines).
- **No delegation to sub-agents; no git kung-fu** (temporary file swaps are done with a scratchpad backup and `cmp`).
- **PRs:** the fork `gh pr create --repo alfre2v/TalkWithZombies --base master`; zombie-radio `--base main`; after
  opening, `mcp__ccd_pr__get_status`; neither repo has CI. **PR descriptions are kept current** — each new commit gets
  an "Added since the PR opened" section (the bodies are kept in the scratchpad: `pr-fork-bed.md`, `pr-zr-sound.md`,
  `pr-installer-tz-0.6.md`, `pr-todo.md`); **verify an edit landed** (one silently failed on 2026-10-02 — an assert
  stopped the script and `gh pr edit` posted the old body).
- **Security:** no inbound connection to the laptop, ever. **Secrets:** the Freesound API key in
  `~/.config/zombie-radio/freesound.key` (mode 600) — read, never printed, sent in a header. The agent never creates
  accounts, enters passwords, or accepts licences.

### §0.1 The boxes, the laptop, the 3090 (binding)

1. The OWNER owns the SSH tunnel, the boxes' power, and the deploys. The agent reaches the cloud stack only at
   `localhost:8080` (llama.cpp), `:8001` (tts-serve), `:8002` (Whisper), through the owner's tunnel.
2. **Probe before any chain of requests:**
   `for u in localhost:8080/health localhost:8001/capabilities localhost:8002/docs; do printf '%s ' "$u"; curl -s -m 3 -o /dev/null -w '%{http_code}\n' "$u"; done`
   — anything but 200: stop, tell the owner.
3. **No machine address in any markdown or commit, ever**; mask addresses in outputs
   (`sed -E 's/([0-9]{1,3}\.){3}[0-9]{1,3}/<addr>/g'`). `deploy/ansible/inventories/cloud/hosts.yml` is `NEVER_COMMIT`
   (the owner wires and unwires it; clean at this writing). **IP scan on the STAGED diff only**
   (`git diff --cached | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}'`; `127.0.0.1` is fine). **A mistake on 2026-10-02:**
   the agent scanned the whole working diff while `hosts.yml` was wired, and the box's address printed into the
   session's output (never into a file) — scan the staged diff only.
4. **The 3090** (the owner's Linux desktop, hostname `aorusX570`, user `alfredo`, Ubuntu 22.04.5 LTS): reached as
   **`ssh zr-3090`** — an alias in the owner's `~/.ssh/config` (key `~/.ssh/zombie_radio_3090`, its passphrase in the
   macOS Keychain; `HostName aorusX570.local`). **The agent never reads `~/.ssh`.**
5. **THE LAN WALL:** the agent's **Bash tool cannot reach the home LAN** — "No route to host" for `ping` and `ssh`, by
   name or address, inside and outside the sandbox (macOS's Local Network block; the app has the permission). The
   owner: "We have been here before, in another project … we gave up trying to figure out the problem." **Do not
   re-diagnose. Use the app's Terminal panel:** `mcp__terminal__run_in_terminal` with
   `ssh -o BatchMode=yes zr-3090 '<cmd>'`, then `mcp__terminal__read_terminal` (tabs `c1`-`c4` were opened on
   2026-10-02 and left idle).
6. Nothing changes on a box outside the playbook. **Scratch files only in the scratchpad**:
   `/private/tmp/claude-501/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18/scratchpad/`.
7. **Downloads:** the file, source, size and licence stated before; the owner approves; a dry run first.

## §1. The project in 60 seconds

**Zombie-Radio**: a live, interactive, audio-only radio play — four AI scientists (Daniel, Moira, Ralph, Samantha the
operator) trapped in a secret lab during a zombie outbreak, broadcasting on a failing shortwave radio; listeners talk
back (hold to talk) when the receiver works. **Deadline Thursday 2026-10-08**; the talk at the **Austin Python Meetup**
in October 2026 ("hackTNT 2026" is the owner's internal label). Two repositories:

- **TalkWithZombies** (the fork of scorbo2's TalkWithMe; `/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`;
  public): the app — the show engine (a Python director, a GBNF grammar, the stream parser, the trim), the page
  (`/show`: a chooser, the looks `old-radio` and `amateur-radio-transmitter`, the plain page), the voice route, the
  listener's turn, **the static bed**.
- **zombie-radio** (this repository, `/Users/alfredo/workspace/hackTNT_2026/zombie-radio-claude`; public): the
  deployment (Ansible + Docker: llama.cpp with Nemotron Nano 9B v2, tts-serve 1.2 with Faster Qwen3-TTS, Whisper
  `small`), the Mac client installer (`make client-mac`), the voice and sound tools (`tools/voices/`,
  `tools/sounds/`), and all the docs.
- **Outside git:** `/Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/` (the EARS voices; **the sound pool**,
  `sounds/freesound/radio-static/`: 17 clips + `.json` each, with the owner's verdicts); the installed client
  `~/TalkWithZombies-client` (its `Personas/` hold the cast's voices).

**The demo's four goals** (2026-09-30): 1. story coherence and improvisation — **largely met** (names-only A deferred
past the demo); 2. emotional voices — **met**; 3. automated deployment to a cloud GPU — **met**; 4. to a local GPU
(the 3090) — **built, never run; the plan begun** (§5).

## §2. The exact state (2026-10-02, ~23:22 CDT)

- **zombie-radio:** branch **`alfre2v/todo-2026-10-02`**, **PR #24 open** (4 commits: `fc3dee3` the board in the
  TODO; `f2062e1` the board discussion and the Hyperstack decision; `9ad8367` the local-GPU plan; `9ee2075` its §8
  addendum) — **plus this handoff, committed (not pushed) on the owner's order**. `main` at `df01fb2` (#23). Clean
  otherwise; `hosts.yml` unwired.
- **The fork:** `master` at `5347ead` (#10 merged) = the annotated tag **`tz-0.6`** (`56e56cb`), pushed; clean; the dev
  checkout's `settings.yaml` restored (`show: seed: 42`, `cmp`-identical to the scratchpad backup
  `settings.yaml.before-bed`); **no dev server running**; no open PR.
- **The installed client** `~/TalkWithZombies-client`: **`tz-0.6`**, re-proven by the owner ("Ran make client-mac the
  two times, all as expected."), its `Sounds/bed/` the 10 tracked files, only `.DS_Store` untracked, **no `show:`
  section** (the demo's defaults: debug off, a random seed per run, the bed on, the filter off). Not running (the agent
  stopped its own instance after the API checks; the owner starts it with
  `cd ~/TalkWithZombies-client && .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000`).
- **The cloud box:** the A6000 on Hyperstack — **the owner's decision (2026-10-02, verbatim):** "I will keep the
  machine hibernated until the day of the presentation... That day, say 4 hours before, I'll start trying to awake the
  VM... I might create a new VM too to exercise the deployment live, I will make that decision that same day." At this
  writing it was up with the tunnel open (the owner's live test). **Before hibernating: the filter test and the video
  need it** (the board).
- **The 3090:** `ssh zr-3090` works (via the Terminal panel); **zombie-radio cloned** at
  `~/workspace/hackTNT_2026/zombie-radio-claude` on `main` `df01fb2` — **#24 (with the plan) not yet there**: after the
  merge, `git pull` there. The Claude desktop app installed (`claude-desktop` 2.19675.0), `~/.claude` without
  `projects/` — **the owner opens a Code session there once** to create the project folder; then the memory copy.
- **Agent memory:** 12 files (above); `pending-doc-updates.md` says the held TODO edits are **applied on
  `alfre2v/todo-2026-10-02`** — **delete it and its `MEMORY.md` line once #24 merges.**

## §3. What happened since handoff 9 (2026-10-01 evening → 2026-10-02 night)

All in **[discussion 2026-10-01] sound-effects §8.9-§8.23** unless said otherwise.

1. **§8.9 — the Freesound fetch tool** (`tools/sounds/fetch_freesound.py`, zombie-radio): ids/links or a search; all
   ids in one request (`filter=id:(…)`); paced (`--pause` 2 s); dry run by default (HEAD for sizes); previews +
   `.json` (licence class, credit line, SHA-256, tags, `ours` section) into `zombie-radio-datasets/sounds/freesound/<kind>/`;
   a page of players. **The owner's 17 finds fetched** (28.05 MB, 35 requests, 6 min 37 s; the CDN slow). Two flaws
   fixed (a HEAD before every GET; output buffered).
2. **§8.10-§8.13 — how to play the bed, decided:** constantly, the level moving with the show; files untouched, one
   gain per clip; mono in the browser; one list; shuffle with no repeat across the seam; silences on a timer (shape B
   — the owner thought it needed slices/seeks; it does not: `pause()`/`play()`); the looks only (`?bed=on` for plain);
   silent while push-to-talk is held; the M key; the gauge voices-only; plain setting names; **built now**. §8.11:
   **event sounds = a layer of their own** (the owner's lean; the bed is the radio, an event's sound the room) — later.
3. **§8.14 — step 1** (`tools/sounds/bed.yaml` + `prepare_bed.py`): **`afconvert -c 1` keeps only the LEFT channel**
   (found by a one-sided-tone test) — the tool decodes both channels and computes (L+R)/2 itself; the owner asked
   whether the EARS voices were hurt — **no: EARS is mono at the source** (612 files; the zip's own header; cast's
   guard refuses non-mono).
4. **§8.15 — step 2, the fork's first build:** `app/show/bed.py`, `ShowBed` in the start reply, `GET
   /api/show/bed/{name}`, `static/show/bed.js` wrapping `setState`/`setReceiver` from outside (like `gauge.js`);
   **correction: the show has no end of its own** (the Switch-off only turns the receiver off).
5. **§8.16 — the story's `stories/lab-outbreak/bed.yaml`** (`file:`, `enabled`, `gain_db`; facts vs decisions:
   `bed.json` = facts written by the tool, the story = the owner's choices); **with `debug`, the console names each
   clip**. Block style, `gain_db: 0` on every clip at the owner's ask (0 dB is neutral, not 1).
6. **§8.17 — the first listen:** "Man it's amazing" … "technically the results are very impressive... But for my ear
   the static is very annoying" — the volume kept. **The volume scale:** plain multipliers on the amplitude, not dB
   (0.15 = −16.5 dB, 0.05 = −26 dB; ×1/2 = −6 dB, ×1/3 ≈ −9.5 dB). **"No restart" corrected:** the story is read when a
   run opens — **reload the page, then Start** (Start shows only on a fresh page).
7. **§8.18 — the second build:** silences on a timer, the AM filter (highpass+lowpass, Q √½, 300-3,000 Hz, **off by
   default, the F key flips it live**), the fading (QSB, ±3 dB every 2-6 s); the crossfade left out. The owner asked to
   **commit the pre-part-2 state first** (done via scratchpad set-aside + `cmp`).
8. **§8.19 — "is the bed changing the voices' volume?" — no:** nothing on the voice's path changed; the kept chunks
   (engine output) vary as much without the bed; **the mood clips cause it** (Moira *fear* −32.7 dB vs *sadness*
   −23.7; up to 9.5 dB per speaker; the women ~4 dB quieter) → the follow-up "Even out each voice chunk…" (very low
   priority, undecided).
9. **§8.20-§8.21 — the verdict and the leftovers:** "I think technically we have met and exceeded our goals."; the
   silences help, the filter uncertain → **Task 10** (filter test; picks; credits); crossfade decided against; three
   timings constants; ideas as a ledger. **Task B built:** the fork's `docs/runbooks/show-settings.md` (recipes, address
   switches, keyboard shortcuts), a README section, **a docs drift test** (every `show:` name in the docs' YAML must
   exist in `ShowConfig`).
10. **§8.22 — the clips chosen by ear, one by one** (two measures: energy above 4 kHz, LRA): **kept 8** — #2 719588,
    #4 730109, #5 625095, #8 652596, #11 557532, #12 624412, #13 255775 (S06 numbers station), **#14 343740 at
    `gain_db: -6`** ("it annoys my ears, but it is the real thing"); out 9 (two licences, two modems, harsh, the full
    sweep, short ones, the artificial Glorb). **Task A:** the clips **ship in the fork** (`Sounds/bed/`: 8 MP3s,
    `bed.json`, `CREDITS.md`; `.gitignore` no longer names `Sounds/`); `prepare_bed.py`'s **licence guard** (only CC0
    and CC BY) and `CREDITS.md`; the target the fork's checkout, never the client; the pool's `.json` `ours` filled
    (verdicts, notes); **a shipped-bed consistency test** in the fork.
11. **§8.23 — the release `tz-0.6`:** the client cleaned by the owner; **correction: the "trap" was not one** — git
    overwrites *ignored* files on checkout (a scratch-repo test); `.git/info/exclude` explained (no code uses it);
    tag; installer **#23** (spec at `tz-0.6`: §6.10, §6.11, §9, §11); re-proof; **five API checks** on the client (start
    reply, clips served, pages, a 6-round drive, the voice); the owner's live test ("All works well").
12. **The Daniel/Samantha oddity** (round 18 of client run `2026-10-02T17-27-56`): traced from `script.json` — the
    grammar pins Samantha first, only the others after; the model wrote her introduction under Daniel's name → a
    follow-up, **deferred past the demo** ("the fix is busy work but not technically challenge").
13. **The board** (#24): Task 10.2 done, 10.3 → Task 9 (one credits line on the last slide), **Task 7 = a video of the
    app with the owner explaining it** ("Let's keep it simple."), **names-only A deferred past the demo** ("Time is too
    tight…"); `docs/discussions/2026-10-02-board-before-demo.md`; the Hyperstack decision.
14. **Goal 4 scouting** → `docs/discussions/2026-10-02-local-gpu-deployment-plan.md` (§2-§7 + **§8 the 3090
    addendum**, with the **Linux session's prompt** in §8.4).

## §4. The systems as built (pointers)

- **The static bed (fork):** `static/show/bed.js` (the chain: clip → its gain → level, mono → [AM filter] → fading →
  silence gate → the "sounds" mute → speakers; `bedLevel`, `bedShuffle`, `bedBetween`, `bedFadingTarget`, `bedLog`;
  keys M/F); `app/show/bed.py` (`bed_clips`, `bed_play_list`, `clip_path`, `CLIP_NAME`); `app/show/story.py`
  (`BedClip`, `_load_bed`); `app/config.py` (the `bed_*` settings with comments); `app/models.py` (`ShowBed`);
  `app/routers/show.py` (`_bed`, `bed_clip`); `Sounds/bed/` (`bed.json`, `CREDITS.md`); `stories/lab-outbreak/bed.yaml`.
  Tests: `tests/test_show_bed.py` (incl. `TestShippedBed`), `tests/test_show_bed.js` (29, fake timers),
  `tests/test_docs.py` (the drift test). Runbooks: `docs/runbooks/show-settings.md` (recipes), `show-page.md` ("The
  static bed").
- **The sound tools (zombie-radio):** `tools/sounds/fetch_freesound.py`, `tools/sounds/bed.yaml` (8 ids; `app:
  ../TalkWithZombies/Sounds/bed`), `tools/sounds/prepare_bed.py` (`uv run`; dry run default; `--write`).
- **The deployment:** `deploy/ansible/` (`site.yml`, roles `base`, `llama`, `tts_engine`, `stt_engine`; inventories
  `cloud/` and `local/`; `common_vars.yml`); the installer `deploy/ansible/client-talkwithme-mac.yml`
  (`client_version: "tz-0.6"`); runbooks `docs/runbooks/box-inspection.md`, `service-restart-sequence.md`.
- **The spec:** `docs/specs/product-definition.md` (status `tz-0.6`; §6.10 the bed; §6.11 settings).

## §5. The work in flight: goal 4, the local 3090

Read **`docs/discussions/2026-10-02-local-gpu-deployment-plan.md`** in full — **§8.5 above all** (the agent cannot
run anything against the 3090 from its own shell; the `ssh` alias works only for the name `zr-3090`; the Makefile's
tunnel overrides it). In short: the `local` inventory exists
but is designed to run **on** the 3090 (`ansible_connection: local`) and was never run; the playbook **asserts, never
installs** Ubuntu, Docker, the NVIDIA container toolkit, a driver ≥ R525 (R570 proven, `cu128`); services start at
every boot, bound to loopback; **the Makefile's `ssh-tunnel` reads the user and key only from `common_vars.yml`**.
**Decisions D1-D5** with the agent's leans: D1 run from the laptop over SSH like the cloud (inventory → the cloud's
sentinel shape); D2 the tunnel; D3 overrides for user and key (+ the tunnel target honouring them); D4 a stop
recipe; D5 "met" = proven at home, recorded for the talk.

**Next, in order:**
1. **The owner merges #24**; then on the 3090 (via the Terminal panel): `ssh -o BatchMode=yes zr-3090 'cd
   ~/workspace/hackTNT_2026/zombie-radio-claude && git pull -q && git log --oneline -1'`.
2. **The owner opens a Code session in the Linux Claude app** in that folder, once → the agent lists
   `~/.claude/projects/` there (expected `-home-alfredo-workspace-hackTNT-2026-zombie-radio-claude` — check, don't
   assume).
3. **Copy the memory folder** (via the Terminal panel):
   `scp -r ~/.claude/projects/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/memory zr-3090:~/.claude/projects/<the Linux folder>/`
   — then list it there; caveats: Mac paths, a snapshot.
4. **The owner pastes the plan's §8.4 prompt** into the Linux session → it runs §5's read-only checks.
5. **Cross-check** from the Mac over `ssh zr-3090`; then decide D1-D5; then the plan's §6 steps (a branch, the
   inventory, wiring — the 3090's address then makes `inventories/local/hosts.yml` NEVER_COMMIT — the deploy by the
   owner, `changed=0`, measure, the tunnel, a show, the stop recipe, the docs).

## §6. The board (2026-10-02; six days to the demo) — `docs/discussions/2026-10-02-board-before-demo.md`

| # | Item | State / next | Needs the box |
|---|---|---|---|
| 1 | Task 10.1 — the narrower-filter test (bands A 300-2,700, **B 400-2,000**, C 500-1,500, D 600-1,000 Hz) | the owner by ear; the client's local setting is enough for the demo | yes |
| 2 | Task 7 — the canned episode = **a video of the app, the owner explaining** | the owner; tips: `seed`, several takes, check the screen recording captures the browser's sound; the agent drafts the demo-day runbook | yes |
| 3 | Task 9 — the talk | the owner, with the agent; **the static's credits line on the last slide** (link to `Sounds/bed/CREDITS.md`) | no |
| 4 | Goal 4 — the 3090 | §5 above | no (the 3090) |
| 5 | The voices over a slow uplink (re-examine "Compressed reference clips") | venue facts; build the switch if slow | to test |
| 6 | Demo-day logistics | the owner's decision | — |
| 7 | The Hyperstack box | **decided** (§2) | — |
| 8 | Task 8 — the close ritual | after the demo | — |

**Deferred past the demo:** names-only A; the cast-line fix; Task 5 and the character bibles; the recasts; the voice
levelling, the bed's lists per round kind, event sounds (ledger); the crossfade (decided against).

## §7. Facts and numbers worth keeping

- **Tests (the fork at `tz-0.6`):** pytest **1284**; Node `test_show_page.js` 42, `test_persona_form.js` 17,
  `test_tts_settings.js` 91, `test_show_gauge.js` 8, **`test_show_bed.js` 29**.
- **Tags:** `tz-0.5` on `9b3a329`; **`tz-0.6` on `5347ead`** (tag object `56e56cb`). **PRs merged this stretch:**
  fork #10; zombie-radio #22, #23. **Open:** zombie-radio #24.
- **The bed's defaults:** `bed` on; volumes 0.15 between / 0.05 under a round; dip 0.5 s, rise 1.5 s; silences every
  30-120 s for 3-15 s, fade 1 s; filter off, 300-3,000 Hz; fading ±3 dB every 2-6 s. **The 8 clips:** 15.3 minutes,
  17.23 MB; measured gains (×): 719588 1.6753, 730109 2.9521, 625095 1.2980, 652596 2.7128, 557532 2.1167, 624412
  0.7096, 255775 1.8509, 343740 0.7359 (→ 0.3688 at −6 dB); 3 CC BY (719588, 730109, 255775), 5 CC0.
- **Runs:** the client's `runs/` — `2026-10-02T17-23-32` (API check 1), `17-23-57` (the 6-round drive), **`17-27-56`
  (the owner's live test; round 18 the Daniel line)**; the dev checkout's — `2026-10-02T00-29-11`, `01-10-49` (the
  owner's bed listening, debug on), `01-08-33`, `01-08-54` (agent checks).
- **The voices by mood** (kept chunks, 5 runs): Moira 9.1 dB spread, Samantha 9.5, Ralph 10.3, Daniel 5.3; women
  ~4 dB under men.

## §8. Nuances (hard to get from the docs alone)

- The owner tests by ear and decides by ear ("now that I hear it better it sounds very artificial"); the agent brings
  measurements to back an ear-less lean, never to override the owner's ear.
- "Make a note to lower" ≠ "lower it": the agent applied `gain_db: -6` after offering −3/−9 and the owner confirmed
  −6 only later — **ask for the exact value before applying a by-ear change.**
- The owner asks to verify files byte-for-byte after editor accidents ("I may have pressed a key in vscode") — keep a
  scratchpad copy of generated files to `cmp` against.
- The owner welcomes being shown the mechanism and the evidence (the scratch-repo git test was well received).
- The owner wants hands-on proof of tooling (Claude on Linux, the memory transfer) — part of the talk's story ("built
  with an AI pair and a memory that survives").
- Discussions are long and append-only; the TODO is canonical; the board doc is the at-a-glance list.

## §9. Mistakes this stretch (do not repeat)

- `afconvert -c 1` assumed to mix down — it keeps the left channel: test assumptions with a one-sided signal.
- "The show ends at the Switch-off" — wrong: it runs until Stop. Read the director's docstring before describing it.
- "Change a line, press Start" — wrong: Start shows only on a fresh page; reload, then Start.
- "The release will refuse the untracked copies" — wrong for ignored files: git overwrites ignored files on checkout.
- A runbook example written as if captured — label illustrations until a real capture exists.
- A guessed clip name (`ref-calm.wav`) in a check — read the story's map first.
- An IP scan on the working diff with `hosts.yml` wired — staged diff only.
- A PR body edit that silently failed — verify the live body after every `gh pr edit`.
- `sed` with `**` in the pattern fails on macOS (BSD regex) — use a small Python replace; `=====` in zsh `echo` breaks.
- Rounded numbers in chat (0.015 for a third of 0.05) — compute exact values for the docs.

## §10. Techniques

- **The fork's tests:** `.venv/bin/python -m pytest -p no:cacheprovider -o addopts="" -q > <scratchpad>/x.log 2>&1;
  grep -E 'passed|failed' …`; Node `node tests/<file>.js | grep -E 'ℹ (pass|fail) '`; remove `__pycache__` after.
- **Mutation checks:** back up the file to the scratchpad, break one rule, run the tests, restore, `cmp`.
- **The dev server:** from the fork's root, `nohup .venv/bin/python .venv/bin/uvicorn app.main:app --host 127.0.0.1
  --port 8010 > <scratchpad>/devserver-<name>.log 2>&1 & disown`; stop with `kill $(lsof -nP -iTCP:8010 -sTCP:LISTEN -t)`;
  settings read at start; back up `settings.yaml` before changing it and restore with `cmp`.
- **A muted browser check** (built-in browser): click the page (not Start), then JS: `unlockAudio(); bedMute();`
  `show.run = <a /api/show/start reply>; setState("thinking")` — samples `bed.*` without asking the model.
- **The client checks:** start it from `~/TalkWithZombies-client` on 8000; `scripts/drive_show.py --base
  http://127.0.0.1:8000 --rounds 6 --report` (the report's checkpoint criteria fail by design on short drives).
- **Loudness:** ffmpeg `volumedetect` (mean/max), highpass at 4 kHz for the top band, `ebur128` for LRA;
  `<scratchpad>/chunk_levels.py`, `chunk_levels_by_clip.py` for the kept voice chunks.
- **Edits with exact replacement:** Python `assert t.count(a) == 1` then replace — stops on a mismatch (and then do
  not run the follow-up command blindly).

## §11. Reading order after the compaction

1. This document, in full.
2. `git status -sb` and `git log --oneline -5` in both repos; `gh pr list` in both (#24 open, unless merged).
3. `docs/discussions/2026-10-02-local-gpu-deployment-plan.md` — §8 first (where goal 4 stands; **§8.5, the execution
   details**), then §4-§6. And §14 of this document (the second pass).
4. `docs/discussions/2026-10-02-board-before-demo.md`.
5. `docs/TODO.md` "Now".
6. As needed: `docs/discussions/2026-10-01-sound-effects.md` §8.20-§8.23; the fork's `docs/runbooks/show-settings.md`.
7. Then report — the clock, the tunnel (probe it), #24's state, the 3090's next step — and wait for the go.

## §12. Paste-ready prompt

```
We continue the Zombie-Radio work of 2026-10-02 after a compaction. Since handoff 9 we built and released the static bed (radio static under the show; the fork's tz-0.6: eight Freesound clips chosen by ear and shipped with the app, credited; silences, a fading, an AM filter; the M and F keys; a settings runbook), installed and re-proved it, wrote the board before the demo, deferred names-only A and the cast-line fix past the demo, and began goal 4 — deploying to the local 3090: a plan document, an SSH key login (ssh zr-3090, through the app's Terminal panel only), the repo cloned on the 3090. Re-orient before doing anything:

1. Read docs/discussions/2026-10-02-session-handoff-10.md IN FULL — §0 and §0.1 are binding (how we work; the boxes, the 3090, the LAN wall, the secrets), then the exact state (§2), what happened (§3), the systems (§4), goal 4 (§5), the board (§6), facts (§7), nuances and mistakes (§8-§9), techniques (§10).
2. Follow its reading order (§11): both repos' status, the local-GPU plan (§8 first), the board, the TODO's "Now".
3. Then give me a compact summary — the clock, the tunnel (probe it first), PR #24's state, the 3090's next step (the Linux session and the memory copy) — and ask what to do next. Wait for my go.

Standing rules: strict review-before-commit (I review in VS Code — no diffs in chat, no commit without my explicit order), push only when told, no AI attribution anywhere, discussion-first and smallest step first, questions in groups of three, explain simply and explicatively, plans executable step by step, docs as detailed as the chat with my words verbatim, never invent data, no machine address in any document or commit (IP scans on the staged diff only), never stage hosts.yml, never read ~/.ssh, the 3090 only through the Terminal panel (ssh zr-3090), scratch files only in the scratchpad.
```

## §13. The owner's words of this stretch (verbatim)

- On the bed: "Man it's amazing." · "technically the results are very impressive... But for my ear the static is very
  annoying... Regardless, let's leave the volume as it is." · "I think technically we have met and exceeded our goals."
  · "I think the silence works well in reducing the fatigue of listening to static." · "The filter I am not sure if it
  helps."
- On shipping the clips: "I decided this bed audio feature is too good not to come out of the box with the app when
  someone deploy it."
- On a clip: "it annoys my ears, but it is the real thing, so we keep it." · "The fact that the voice is speaking in
  Russian adds to the mystery and the atmosphere."
- On scope: "Time is too tight, and I think we have already demonstrated enough technical depth in steering the
  model." · "That's ok to postpone, the fix is busy work but not technically challenge." · "Let's keep it simple."
- On the box: "I will keep the machine hibernated until the day of the presentation..."
- On the 3090: "I want to exercise having Claude in the linux host just to prove how mature Claude's Linux support is."
  · "I want to try to transfer you memories folder, that sounds interesting."
- On the LAN wall: "We have been here before, in another project … Suffice to say, we gave up trying to figure out the
  problem."

## §14. Second pass — details that would otherwise be lost

The owner, before the compaction (verbatim): "Are you certain you captured in the handoff document all nuanced details
about where we are in the project, what our next tasks are, where the pertinent documents to pick up the state of the
project live, etc.? Maybe you should do another deep scan over your context window to try to find details that would
be lost if not saved to the handoff." — the agent's second pass added this section, and **§8.5 of the local-GPU plan**
(the execution details: the agent cannot run anything against the 3090 from its own shell; the `ssh` alias applies
only to the name `zr-3090` and the Makefile's tunnel overrides it with the Hyperstack key and `ubuntu@`; Ansible's own
SSH options; `ANS_ARGS=-K` for sudo; one tunnel at a time; no release needed for goal 4).

- **Where the clips can be heard:** the page of players of the owner's 17 finds,
  `/Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/sounds/pages/index-2026-10-01T22:14:37.html` (open it
  in a browser); each clip's `.json` carries the owner's `verdict` and `notes`. The datasets folder's `README.txt` has
  a `sounds/` section.
- **The Freesound credential** is "zombie-radio sound test" on the owner's account; the key file above. Fetching more
  clips: `python3 tools/sounds/fetch_freesound.py --kind radio-static --ids <ids or links>` (dry run), then `--fetch`
  on the owner's approval; then add the ids to `tools/sounds/bed.yaml`, `uv run python tools/sounds/prepare_bed.py`
  (dry run) and `--write` (into the fork's checkout), the story's `bed.yaml` entry, the tests, a PR in each repo.
- **Changing the static's filter default** (Task 10.1's possible outcome) is a code change in the fork (the
  `bed_filter*` defaults in `app/config.py`, the tests' defaults, the runbook) and **a new release** (a tag `tz-0.7`, the
  installer pinned, a re-proof); for the demo alone, the client's `settings.yaml` (`show:` `bed_filter: true` and the
  band) is enough — no release.
- **The release pattern** (as for `tz-0.5` and `tz-0.6`): the PRs merged → the fork's `master` checked against the
  tested branch head (`git diff --stat`) → all tests on `master` → an annotated tag in the style of the previous ones
  (`git tag -l --format=… tz-0.5`) pushed → a zombie-radio branch `alfre2v/installer-tz-X` (`client_version`, the
  README's and the spec's tag, the spec's description if the product changed, the TODO, the discussion) → PR → the
  owner's `make client-mac` twice → the agent's checks on the client (`git describe`, `git status`, the start reply, …).
- **Re-running `prepare_bed.py --write` rewrites `Sounds/bed/bed.json`** (its `prepared` time) even when nothing else
  changed — a one-line diff in the fork to expect.
- **The fork's runbook for the bed** says "reload the page, then Start" after a `bed.yaml` change; the settings need an
  app restart; the address switches (`&bed=on`, `&voice=off`, `&mock=1`) and the keys (Space held, M, F) need nothing.
- **Local branches** in both repos (many, merged) — the owner: "Leave the branches. I'll clean up later." Do not
  delete them.
- **The Terminal panel's tabs `c1`-`c4`** (the 3090 checks) are idle; reuse or close them with `stop_terminal_tab`.
- **Scratchpad, useful files** (same session folder; may vanish with the machine's `/private/tmp`):
  `settings.yaml.before-bed` (the dev checkout's original settings), `story-bed.yaml.backup` (the story's `bed.yaml`
  as generated), `bed.js.part2.backup`, `part2/` (the part-2 set-aside), `show-settings.md.backup`,
  `owner-finds.txt` (the 17 links), `chunk_levels.py`, `chunk_levels_by_clip.py`, `test_fetch_path.py`,
  `client-start.json` (the client's start reply), `served-bed.js` / `tag-bed.js`, the PR bodies (`pr-fork-bed.md`,
  `pr-zr-sound.md`, `pr-installer-tz-0.6.md`, `pr-todo.md` — #24's, with its "Added since" sections).
- **Talk material that came up** (Task 9): the S06 numbers station (#13, a real Russian shortwave broadcast); the
  radio amateurs' Q-codes — QRN (static), QRM (interference, the "mixed stations" clips), QSB (the fading) —
  ([discussion 2026-10-01] sound-effects §8.12); `afconvert -c 1` keeping only the left channel; the voices' level
  set by the mood clips' delivery (§8.19); the dead air between rounds (3.7-4.9 s, 8.4 s after a trim) filled by the
  bed; the one-by-one choice of the clips by ear with two measures; "two Claudes, one 3090".
- **Owner questions still open, asked in the plan's §5:** what else the 3090 is used for (games, other GPU work), and
  the §5 checks' results. The board's items 5-6 (the venue's network; demo-day logistics) wait for the owner's facts.
- **Pushing:** this handoff and the plan's §8.5 are committed on `alfre2v/todo-2026-10-02` but **not pushed** until the
  owner says so; #24's description lists the commits up to `9ee2075` — add "Added since" lines when pushing.
