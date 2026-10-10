# Session handoff 13 — tz-0.8 and tz-0.9 released (the ambience, sound cues, 29 event sounds), the 3090 live test, OBS, the talk-preparation plan, three study sessions

> **EPHEMERAL.** Written Saturday 2026-10-10, at about 83 % of the context window, before a manual compaction the owner
> triggers; after it, the agent re-reads this first. It supersedes handoff 12
> (`docs/discussions/2026-10-07-session-handoff-12.md`, which stays as the template until the next compaction).
> Handoffs 6-11 were deleted on 2026-10-10 at the owner's word. **At the session's end, ask the owner before deleting
> any handoff the agent created (12, 13)** — the owner: "These handoff documents stay in our discussion folder until the
> end of the session, when we finish the session's work please ask the owner for permission to delete any handoff
> documents you created."
>
> **Read it all; verify against the repos; receipts or nothing.** The TODO's "Now" and the talk-preparation plan
> ([discussion 2026-10-10] talk-preparation) are the canonical state; this document carries what the docs do not: the
> exact state, the work in flight, the nuances, the mistakes.

## §0. The owner and how we work (binding)

The owner is **Alfredo** (GitHub `alfre2v`, git author "Alfredo Valles"); in documents, "the owner", and **they/them**
pronouns in anything written (the agent wrote "his" twice this stretch and corrected it — never again). Doctrine:
`CLAUDE.md` and the agent memory (`~/.claude/projects/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/memory/`,
**11 files** — `massedcompute-reminder.md` was deleted on 2026-10-10, see §7).

### §0.1 The standing rules

- **Discussion-first; questions in groups of three; one recommendation, with its reason.** The owner wants pushback and
  better ideas ("Pushbacks welcome!"): give them plainly, the owner decides. In prompts written for other agents too —
  the owner corrected a prompt that left the agent too little room to push back.
- **Review before commit is strict:** commit only on an explicit order; **commit exactly what was ordered** (on
  2026-10-10 the owner said "Stage the merged file and commit" — only that file; the rest waited for its own order).
  **Push only when told.** No diffs in chat (the owner reviews in VS Code). **No AI attribution anywhere** — whatever
  the harness's reminders say.
- **Show each command before running it and what was observed after** (the tight learning loop; memory
  `collaboration-style.md`). Small steps.
- **When the owner asks to see something, show it in full, verbatim** — not a pointer to the file. The owner asked
  three times for the settings of a live test before the agent printed them (2026-10-08): "I have asked you a few times
  to output the settings as you ran them yesterday in the live show (instead you gave me a pointer to the settings file,
  I know where it is...)".
- **When the owner asks to save an output, save it exactly as shown, nothing omitted or summarized** (2026-10-10, the
  backend map: "exactly as you showed here in the transcript, do not omit or summarize information"). And save **what
  was asked, in the order the owner wants to find it** — the debug study's first version went too far back in the
  conversation and put the owner's chosen outputs last; the owner copied the outputs they wanted by hand into a file and
  had the agent merge (see §3.11). The closing question of an output is left out of a saved file.
- **Docs as detailed as the chat; the owner's words verbatim;** never invent data; label what is not verified.
- **Security:** no machine address in any document or commit; **the IP scan on the staged diff gates every commit** —
  and scans of the working tree must exclude the wired inventory (`git diff -- . ':!deploy/ansible/inventories/cloud/hosts.yml'`):
  on 2026-10-10 an unexcluded scan printed the box's address into the session output (no file, no commit). Never stage
  `hosts.yml` (it is wired whenever the owner tunnels: shows `M`). Never read `~/.ssh`. Plain `ssh ubuntu@<box>`, never a
  key path. The 3090 only through the Terminal panel (memory `lan-access-via-terminal-panel.md`).
- **The owner's home network is never recorded in this repository** — the owner is setting up remote SSH access to the
  3090 in a **separate project** (the agent wrote its kick-off prompt on 2026-10-10); nothing about it goes in these
  docs.
- **The fork (TalkWithZombies)** has its own `AGENTS.md` rules: upstream's documentation style (a brief docstring on
  every new function; plain `-`, never `–`); the suite green before review (pytest plus the Node tests for
  `static/show/`); PRs into `master` with `gh pr create --repo alfre2v/TalkWithZombies --base master`; never push to
  upstream.
- **Merges are squash merges.** A branch's own commits are not in `main`'s history; a reference into git history must
  use `main`'s commit (found with `git log --first-parent`). Handoff 5 survives only on the branch `alfre2v/show-slice-3`
  (commit `57c7fd7`) and is lost if that branch is deleted.
- **Don't be condescending.** On 2026-10-08 the agent told the owner that OBS filters change only the recording, not
  what one hears live — the owner knew ("The fu*ck! I know that"). Troubleshoot; don't lecture.

### §0.2 The dates and the names

- **The talk** at the Austin Python Meetup: internal docs keep **Oct 8**; the slides say **Oct 14**; the real date is
  one week later and **never written anywhere** (the owner: "I do not want to keep track of the exact date in our
  docs"; memory `talk-date-two-dates.md`).
- **The owner's website** (`alfre.net`): only the link in the slides; never write its state.
- **The unnamed AI provider** (the talk's "Why not AI APIs (3/3)"): never named anywhere.

## §1. The project in 60 seconds

**Zombie-Radio**: a live, interactive, audio-only radio play — four AI scientists (Daniel, Moira, Ralph, Samantha the
operator) trapped in a lab during a zombie outbreak, on a failing shortwave radio; listeners talk back. Repos:

- **zombie-radio** (`/Users/alfredo/workspace/hackTNT_2026/zombie-radio-claude`, base `main`): the deployment (Ansible +
  Docker: llama.cpp with Nemotron Nano 9B v2, tts-serve with Faster Qwen3-TTS, Whisper), the Mac client installer
  (`make client-mac`, pinned to a fork tag), the tools (`tools/voices/`, `tools/sounds/`), the talk (`talk/`, Quarto, on
  GitHub Pages), all the docs.
- **TalkWithZombies** (`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`, base `master`): the app. **Released:
  `tz-0.9`** (`b1d039c`).
- **The installed client:** `~/TalkWithZombies-client` (at `tz-0.9`, re-proven; its runs in `runs/`).
- **Outside git:** `/Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/` (the voices; `sfx-test/takes/`;
  `ambience/round1`, `extra`, `events`, `events-retry`, `events-retry2` — every take with its audition page);
  `~/Movies/zombie-radio-rehearsals/` (the OBS recordings).

**Demo goals:** all four met (1 coherence/improv, 2 emotional voices, 3 cloud deploy, 4 the 3090). **Every feature for
the talk is built and released.** What is left is the talk itself.

## §2. The exact state (2026-10-10, before the compaction)

- **zombie-radio:** branch **`alfre2v/talk-prep`** (from `main` at `ad4b520`, #35), **not pushed, no PR**. Its commits:
  `7518cda` (the plan, a draft; the housekeeping; handoffs 6-11 deleted), `9053e5c` (the backend map; two follow-ups),
  `b8bba42` (the client map and how a show runs), `333c74a` (the debug study, merged), `101b351` (renamed to
  `2026-10-10-debug-data-study.md`; the plan's §4; the improvements follow-up; the pauses measured) — and this handoff
  when committed. `main` at **`ad4b520`**. Wired: `hosts.yml` only when the owner tunnels.
- **The fork:** clone on **`master` at `b1d039c` = `tz-0.9`**, clean; the branches `alfre2v/ambience` and
  `alfre2v/sound-cues` kept (the owner keeps the last few branches as backups). The clone's `settings.yaml`: `show:`
  holds only `seed: 42`.
- **The installed client's `settings.yaml`** (the owner's; the agent edits it only when asked): `show: seed: 651594682`
  (the good 3090 show), `voice_seed: true`, `reference_format: ogg` — and possibly the three test lines (`event_every:
  1`, `event_jitter: 0`, `debug: true`) the owner was to add for the 3090 test of 2026-10-08; the evening recordings had
  no debug files, so `debug` at least was off by then. **Before the demo they come out** (talk-preparation, F).
- **The boxes:** the **A6000 hibernated since the night of 2026-10-08** (its next wake: the day before the talk, as a
  check, then about 4 hours before it; a wake can fail — no A6000 in stock on 2026-09-24). `~/sfx-lab/` kept on it (39
  GB; the disk 17 GB free; undecided). **The 3090** proven over the LAN on 2026-10-08 (a 206-round debug show and
  recordings); reachable only on the home LAN.
- **Nothing of the agent's is running:** no app on 8010, no monitor.
- **OBS Studio 32.2.2** installed (Homebrew) and set up (§7.4).

## §3. What happened since handoff 12 (2026-10-07 evening → 2026-10-10)

1. **`tz-0.8`, the ambience (Task 13):** the fork's #12 merged (`66e35d5`), tagged; the installer pinned (#34); the
   owner's re-proof (`changed=1`, then `changed=0`, `tz-0.8`). Task 13 done.
2. **Task 14, sound cues — the owner's inversion:** a clip's `keywords:` in the story's `ambience.yaml`, matched against
   a free round's event (whole words, any case); the server picks a clip with the round's own seeded dice
   (`"{seed}:{n}:cue"`), sends `{"type":"cue","file","kind"}` before the first line; the page plays it when the first
   line is heard (a spot at once; a texture in place of the current one, to its end). The owner asked why a string seed
   (answered: collisions with ints; SHA-512 seeding since Python 3.2; checked on 3.9-3.12).
3. **The sparse association:** only 8 of the 289 events named a sound the library had. Three refinements: **R2
   `cue_only`** (a story field: never in the random rotation), **R1 sounds for the events** (the owner's reshaping: event
   by event, three takes each, the owner's ear — 33 prompts, three audition rounds, **29 sounds, 42 takes kept**; the
   church bell passed only on its third prompt, "at the Vatican"), **R3 new events** — postponed past the demo (a
   follow-up). **43 of 289 events now cue a sound.** The runbook `docs/runbooks/event-sounds.md`.
4. **The owner's hearing test** (a seed-42 show, debug on): 67 rounds, 37 events, 5 cued, each fetched by the page, 37 of
   37 consistent with the keywords. **`tz-0.9` released** (the fork's #13, `b1d039c`) and the installer pinned (#35);
   **re-proven** by the owner on 2026-10-08.
5. **The event-sounds follow-up reshaped:** largely delivered by sound cues "by another route"; what is left is live
   generation by a Small-SFX server in the stack. **The inversion is credited to the owner** (§9.1 of the world-outside
   discussion, verbatim). The owner on it: "brilliant. Much more flexible."
6. **A staleness pass:** the TODO's next steps, the box's state, Tasks 4/11/12/13 moved to Done (4 done for the demo),
   follow-ups updated (mood clips built, compressed clips built, the voice-isolation tool not needed), the roadmap's arc
   brought up to date. **MassedCompute closed** (the owner: "We are committed now to hyperstack, it has worked well") —
   the agent's reminder memory deleted.
7. **2026-10-08 — the 3090 live test and OBS:** the installed client against the 3090 over the LAN; the owner's long
   debug show (`2026-10-08T14-57-55`, 206 rounds) and the first recordings. **OBS took the day** (the owner: "Today is
   been OBS day, I don't like it, but I guess it had to be done") — see §7.4 for every lesson.
8. **The owner's three observations** from the 3090 show, as follow-ups: events that could cue sounds the library has
   (keywords to add); **pauses of about 300 ms growing with the show, mostly at the mic's open and close**; some cues
   barely heard (`gain_db`).
9. **2026-10-10 — the talk-preparation plan** (a draft, the owner's five workstreams reorganized, plus the agent's F),
   and the housekeeping: Task 10.1 (the narrower filter test) pushed past the talk as a follow-up; Task 14 closed; the
   box hibernated; the A6000's price checked (right in the slides). **Handoffs 6-11 deleted** with the owner's
   permission; the two references to deleted handoffs pointed into git history.
10. **Study session B, the backend:** the agent's map; the owner walked the code from it ("I feel I got myself the
    picture together"). The owner's code-review questions became two follow-ups: no lock on a run's record (overlapping
    rounds would race), and the `"blas\xE9"` YAML escape in `overtones.yaml`.
11. **Study session C, the client:** the map; a Web Audio refresher; the loop; the voice queue (merged into one file at
    the owner's request); the owner asked how the JS side handles concurrency (one thread, cooperative `await`s, flags,
    the generation counter, `AbortController`, hand-made waiters — answered in chat, not saved). **Study session D, the
    debug data:** saved as the owner chose (see §0.1). The pauses measured: nothing in the long run's data grows (the
    voice's real-time factor flat at 0.38-0.41; 2 stalls in 206 rounds; the gap between rounds flat at 2.2-2.4 s thanks
    to the prompt cache) — so the pauses lie in the mic switching (a Bluetooth headset) or OBS.

## §4. The documents (pointers)

- **The meta-doc and the board:** `docs/README.md`; `docs/TODO.md` ("Now" — "Next (2026-10-10)" points to the plan;
  open tasks: **7, 9, 8**, and 5 deferred); `docs/follow-ups.md`; `docs/roadmap.md`;
  `docs/specs/product-definition.md` (describes `tz-0.9`, sound cues included).
- **The plan:** `docs/discussions/2026-10-10-talk-preparation.md` — **DRAFT**, workstreams A-F, §4 the results so far,
  §5 three questions still open for the owner.
- **The study sessions:** `2026-10-10-code-map-backend.md`, `2026-10-10-code-map-client.md`,
  `2026-10-10-client-how-a-show-runs.md` (Web Audio, the loop, the voice queue), `2026-10-10-debug-data-study.md` —
  snapshots of the fork at `tz-0.9`.
- **Sound cues and the ambience:** `docs/discussions/2026-10-07-the-world-outside.md` (§9-§9.11);
  `docs/runbooks/event-sounds.md`; `tools/sounds/ambience.yaml` (72 prompts; the event sounds' section with the events
  each cues).
- **The talk:** `talk/` (`index.qmd` + `sections/_01-intro` … `_06-future`), `docs/discussions/2026-10-03-the-talk.md`
  (§4.1 the minutes), `docs/runbooks/talk-slides-quarto.md` (§10 publishing).
- **The new follow-ups of this stretch:** "New events that name the library's sounds — sound cues' R3"; "Event sounds
  generated live by a Small-SFX server in the stack" (reshaped); "The narrower AM filter test"; "Events that could cue a
  sound the library already has"; "Pauses of about 300 ms…"; "Some cue sounds barely heard"; "No lock on a run's
  record"; "\"blas\\xE9\" in the story's overtones.yaml"; "Debug and observability improvements" (six items).

## §5. The plan for the days before the talk (talk-preparation)

| Workstream | Status | What is left |
|---|---|---|
| **A, the slides** | not started | the **feature inventory** first (the app's features against the slides — e.g. the eight round kinds are on no slide); the owner decides per feature (slide, aloud, backup, out); the **"four levels of sound immersion"** slide (the static bed, the ambience's textures, its spots and cues, the voices — a diagram of four bands; placement the owner's call); **"What's next" rewritten** (it still lists event sounds as future); **"recount slides 5 and 27"** (the deck has 25 titled slides — check which those are first); republish |
| **B, the backend** | done | — |
| **C, the client** | done (the plan's §4 says "under way") | mark it done |
| **D, the debug data** | done | its improvements are a follow-up for after the demo |
| **E, the rehearsals** | not started | the baseline (which recording? transcribed with Whisper — the agent reads transcripts, not videos: pace, fillers, time per section); "three sentences per section"; rehearsals 1-3 recorded and measured; a Q&A drill (the agent as the audience); **Task 7's fallback video cut from the best rehearsal** (the owner's ruling) |
| **F, demo-day readiness** | not started | the client's demo settings (the seed, `voice_seed`, the test lines removed); the A6000 woken the day before as a check; a venue checklist as `docs/runbooks/demo-day.md` |

**The plan's §5, still open:** which recording is the baseline and where to run Whisper; the timeboxes (60-90 minutes a
session — the sessions ran about that); backup slides after "Thank you" (yes or no).

**The owner on the rehearsals** (2026-10-08): "I am very disappointed with myself, I am not an effective communicator. I
will have to practice giving the presentation at least 3 times I guess." Be encouraging and concrete, never gushing.

## §6. The talk (facts)

- **25 slides, six sections** (`talk/sections/`): intro (9: Orson Welles, who I am, how it came to be, a Halloween
  broadcast, about this project, local AI only, why not AI APIs 1-3), tech overview (2: the machines, the components),
  demo (2: commands to go on air, live demo), deep dive (6: one round, the director, the grammar, the 32k context and the
  trim, one command to a GPU, the 3090 at home), AI pair (3), future (3: what's next, thank you, credits).
- **The budget:** intro 5, overview 5, demo 10, deep dive 6-8, AI pair 4-5, future 1 — **about 33 minutes plus
  questions**.
- **Publishing:** `quarto publish gh-pages` from `talk/` (a website project); republish after any slide change.
- **The static's credits** line on the last slide (three CC BY clips); the ambience and event sounds are CC0
  (generated), credited in the fork's `Sounds/ambience/CREDITS.md`.

## §7. Facts worth keeping

### §7.1 Sound cues and the library

- 73 ambience clips (31 in the rotation: 16 textures, 15 spots; 42 cue-only event sounds), 8.8 MB. The manifest
  (`Sounds/ambience/ambience.json`) is written only by `prepare_ambience.py`; the story's `ambience.yaml` holds the
  choices (`enabled`, `gain_db`, `keywords`, `cue_only`) — the owner's rule: "any extra fields that change how the story
  is told (like keywords) go to the yaml, nothing touches the json expect the tool that copy the files."
- **`kind` and `cue_only` are two axes:** kind = how a clip plays (texture/spot), cue_only = when (only on a cue, or
  also at random). A texture can be cued (the dogs, round 41 of the hearing test).
- **The seed-42 path is per box:** on the A6000 every seed-42 run reads round 2 "Footsteps cross the floor above…", round
  6 the drone, round 8 the smoke detector. Not on the 3090.
- **Prompt lessons** (in the runbook): one sound per prompt; no "single" (one bell bang); name an occasion (the Vatican);
  "the sound of…", "very loud"; no "in the distance" (quiet).

### §7.2 The debug data (details in the debug study)

- A run: `script.json` (the record) and `debug/` (`rNNN.txt`, `rNNN.request.json`, `audio/` with each chunk's `.wav`
  and `.json`). `rNNN.txt` is **written by our app**; one section is llama.cpp's `/apply-template` output verbatim;
  the token check uses `/tokenize`.
- llama.cpp's `timings` come without asking (we keep `prompt_n`, `cache_n`, `predicted_n`; we drop the times); they
  drive the script's size, the trim, each round's share, `known_size`, the token check. `usage` would come in addition,
  not instead (not checked on our server).
- Whisper gets `prompt` = the cast's names ("Daniel, Moira, Ralph, Samantha"), `language`, `vad_filter`, `json`; the
  request itself is not kept in the debug files (an improvement).
- The voice: the page adds `reference`, `seed`, `debug` to `/api/tts`; tts-serve's reply (`seed`, `time_used`, `rtf`,
  `fid`) is standard, kept in debug.

### §7.3 The pauses

Measured on the long 3090 run (not in the debug study by the owner's choice; in the follow-up "Pauses of about 300 ms…"):
nothing grows with the show. Hypotheses left: **the mic opened at every listening window** (`openMic` → `getUserMedia`
each time; a **Bluetooth headset** switches into call mode — the owner: "Yes, I was using a bluetooth headset for
recording the talk with OBS"), or **OBS**. The next test: log the mic's open and close, or a show with wired audio.

### §7.4 OBS (the owner's recording setup, 2026-10-08)

- Installed with `brew install --cask obs` (32.2.2, macOS ≥ 13). One scene: **macOS Screen Capture** (Display Capture,
  fitted with **⌘F** after setting the base canvas to the display's resolution and a same-shape output); **its audio
  muted** in the mixer (it captured the Mac's sound too — the agent had wrongly said it did not); **macOS Audio
  Capture** switched to **Desktop Audio Capture** (per-application capture of Chrome dropped the show's sound at times);
  the **headset's mic** (Mic/Aux); Chrome's source at about -10 dB with a **compressor ducking it under the voice**
  (threshold -40 dB, ratio 20:1, attack 6 ms, release 402 ms, sidechain Mic/Aux — it worked once the bleed was gone).
- Lessons: the MacBook's mic hears the speakers (use a headset); OBS has no echo canceller; a locked screen freezes the
  capture (`caffeinate -d` while recording); check the audio bar moves before each take; Do Not Disturb on; hotkeys
  for Start/Stop recording (Settings → Hotkeys; may need Accessibility permission); OBS saves its scene and profile by
  itself (renaming them and exporting the scene collection is optional).
- Recordings: `~/Movies/zombie-radio-rehearsals/`, 13 from 2026-10-08 (the longest `2026-10-08 22-15-34.mp4`, 54 MB,
  and `2026-10-08 22-30-50.mp4`, 75 MB).

### §7.5 The 3090 over the LAN (from the runbook `docs/runbooks/home-gpu-3090.md`)

`make ans-set ENV=lan IP=zr-3090`; `make ans-start ENV=lan ANS_ARGS=-K` (nothing starts at boot); `make ssh-tunnel
ENV=lan` in its own terminal; `make check`; the client: `cd ~/TalkWithZombies-client && source .venv/bin/activate &&
uvicorn app.main:app --host 127.0.0.1 --port 8000`; after: `make ans-stop ENV=lan ANS_ARGS=-K`, close the tunnel, `make
ans-unset ENV=lan`. For maximum visibility, under the client's `show:`: `event_every: 1`, `event_jitter: 0`, `debug:
true` (removed after).

## §8. Nuances

- The owner learns by **maps first, then questions, then saving the outputs** — the study sessions' pattern; the owner
  walked the code alone from the backend map. The owner confessed not reading the JS source ("don't save this detail in
  the docs").
- The owner's frustration peaks with tooling (OBS); answer short and practical then.
- The owner values the agent's original ideas and credits them; equally, credit the owner's ideas in the docs (the
  inversion; the rigged seed-42 cue; R1's reshaping; "distinct and recognizable").
- Plain lists with sublists; no "bricks"; the mechanism first; tables by case.
- The owner keeps the last few branches as backups — never suggest deleting fresh ones.

## §9. Mistakes this stretch (do not repeat)

- **Printed a pointer instead of the settings** the owner asked to see, three times (§0.1).
- **Condescension** about OBS ducking (§0.1).
- **Wrong facts about OBS:** that the screen capture carries no audio (it did, recorded twice); a "Capture audio"
  checkbox that does not exist in 32.2.
- **The debug study's first versions:** too far back in the conversation, the owner's chosen outputs last, the pauses
  included against the owner's wish.
- **Switched the zombie-radio clone to `main` in the middle of a docs pass** — read the stale docs; always work on the
  branch that holds the latest docs.
- **Shell slips:** `echo =====` in zsh (a leading `=` is command expansion); `cat -A` (not on macOS); a heredoc after
  `cmd1 || cmd2` feeds only `cmd2` (the first waited on stdin and hung); a `sed` range that cut through comment blocks
  and made doc comments look shifted (a false alarm).
- **An unexcluded IP scan** printed the box's address into the session output (§0.1).
- **"his"** in two documents (§0).
- **An estimate from memory** (2 MB per ten event takes — it is 0.8 MB); measure before writing.
- **Forgot the MassedCompute reminder** after the experiment PR (now retired).

## §10. Techniques

- **The gated commit:** `git add <paths> && hits=$(git diff --cached | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' | grep -v
  '^127\.0\.0\.1$' | sort -u); if [ -n "$hits" ]; then echo "SCAN HIT"; else git commit -q -m "…"; fi` — never `git add
  -A`.
- **Edits by script** (the fork's `.venv/bin/python`, which has PyYAML; zombie-radio's `uv` env lacks numpy): assert
  each old passage occurs exactly once before writing; move TODO blocks whole and check no line was lost (a `Counter`
  of the old file's lines against the new).
- **The box helpers** (scratchpad `box.sh`, `boxcp.sh`): plain ssh/scp, the address read from `hosts.yml`, never
  printed; generation: `cd ~/sfx-lab/stable-audio-3 && HF_HOME=~/sfx-lab/hf HF_HUB_OFFLINE=1 .venv/bin/python
  ../gen_ambience.py ../ambience.yaml ~/sfx-lab/ambience/<folder> --seeds 1-3 --only <tags>`.
- **The fork's checks:** `.venv/bin/python -m pytest -p no:warnings | tail -1` (**1,337**); Node: ambience 21, bed 29,
  page 44, gauge 8, persona 17, TTS 91 (`grep -E '^ℹ (pass|fail) '`).
- **Watching a live show:** a `Monitor` on the app's log for `opened|cues|GET /api/show/ambience/…|Traceback|ERROR`.
- **Rigging a cue:** a test keyword unique to a known seed-42 event; unrig with `git checkout -- stories/…/ambience.yaml`.

## §11. Reading order after the compaction

1. This document in full.
2. `git status -sb` and `git log --oneline -6` in zombie-radio (on `alfre2v/talk-prep`) and the fork (on `master`).
3. `docs/discussions/2026-10-10-talk-preparation.md` (the plan; its §4 and §5).
4. `docs/TODO.md` — "Now" and the open tasks (7, 9, 8).
5. Skim: the two code maps, `2026-10-10-client-how-a-show-runs.md`, `2026-10-10-debug-data-study.md`.
6. `talk/sections/` (the slide titles) — workstream A is next.
7. Then report the state and the next steps, and wait for the owner.

## §12. Paste-ready prompt

```
We continue the Zombie-Radio work of 2026-10-10 after a compaction. Since handoff 12 we released tz-0.8 (the ambience) and tz-0.9 (sound cues, cue-only clips, 29 event sounds), tested the show live on the 3090, set up OBS for recording, wrote a draft plan for the days before the talk, and ran three study sessions (the backend, the client, the debug data). Re-orient before doing anything:

1. Read docs/discussions/2026-10-10-session-handoff-13.md IN FULL — §0 is binding (how we work, including the new rules: show what I ask to see verbatim, save outputs exactly as shown, commit only what I order, they/them pronouns, exclude hosts.yml from IP scans), then the state (§2), what happened (§3), the plan (§5), facts, nuances and mistakes (§7-§9), techniques (§10).
2. Follow its reading order (§11), including the talk-preparation plan and the TODO.
3. Then give me a compact summary — the branches and commits, the boxes, the plan's workstreams and what is left — and the next steps. Wait for my go.

Standing rules: strict review-before-commit (I review in VS Code — no diffs in chat, no commit without my explicit order, and commit only what I name), push only when told, no AI attribution anywhere, discussion-first, questions in groups of three, explain simply, show me each command before you run it and what you observe after, never invent data, no machine address in any document or commit (IP scan on the staged diff, gating the commit), never stage hosts.yml, never read ~/.ssh, plain ssh without a key path, scratch files only in the scratchpad.
```
