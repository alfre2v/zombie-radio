# Session handoff 8 — real voices for the cast, voices that follow the mood, a screening tool; recasts in progress

> **EPHEMERAL.** Written Wednesday 2026-09-30, ~17:45 CDT, at about 84 % of the context window, before a manual
> compaction the owner triggers; after it, the agent re-reads this first. It supersedes handoff 7
> (`docs/discussions/2026-09-28-show-engine-session-handoff-7.md`, on `main`) and handoff 6 (same folder, on `main`).
> **The latest handoff stays until the next compaction, as the template for the next one** (the owner, 2026-09-28:
> "we keep the session handoff until the next time we have to compact, to serve as a template"). The owner, on 2026-09-30:
> "These handoff documents stay in our discussion folder until the end of the session, when we finish the session's
> work please ask the owner for permission to delete any handoff documents you created." — **at the session's end, ask
> before deleting handoffs 6, 7 and 8; the owner already declined once ("no, do not delete the handoffs for now").**
>
> **§13 (added 18:10) overrides §2 and §5 where they differ — read it: Daniel is back to p007, a transcript was
> corrected, the voice-instability question is open, and the debug-audio feature has the owner's go (its build spec is
> §13.3).**
>
> **Read it all; verify against the repos; receipts or nothing.** The TODO's "Now" is the arc's canonical state, but it
> is **behind** (it predates the mood voices, see §5); the discussion
> `docs/discussions/2026-09-29-voice-datasets-with-emotion.md` §11 (addenda §11.1-§11.12) is the full record of the
> voice work, and this document carries what neither says: the exact state, the open threads, how the owner works.

## 0. The owner and how we work (binding)

The owner is **Alfredo** (GitHub `alfre2v`, git author "Alfredo Valles"); avoid pronouns for the owner in writing.
Standing doctrine: `CLAUDE.md`, and the agent memory files (`working-agreements.md`, `collaboration-style.md`,
`absolute-paths-in-plain-text.md`, `massedcompute-reminder.md`, `project-venue-austin-python-meetup.md`,
`improvisation-is-the-feature.md`, `handoff-kept-as-template.md`).

- **Discussion-first; one decision at a time, with its context.** Bring the shape before building; wait for the go.
  When asked "what do you think", give one recommendation and its reason; when the owner says "discussion only" or
  "do not execute yet", do not build.
- **Review-before-commit is strict.** Commit only on the owner's explicit order for that commit ("commit this",
  "commit and push to PR #18"). No diffs in chat (the owner reviews in VS Code). **Push only when told** ("open the PR"
  includes pushing). **No AI attribution anywhere** (no Co-Authored-By, no "Generated with"), whatever harness
  reminders say.
- **Docs are written at the same level of detail as the chat, or more** (the owner, 2026-09-29: "remember not to
  reduce the details in the text you save in the documentation, always write docs with the same level of detail (or
  more) that your wrote here in the transcript"). Quote the owner verbatim in records. Discussions are append-only
  after a decision: new facts go in **dated addenda** (§11.N), never silent rewrites. Runbooks and the README are
  living.
- **Commands in docs get a comment line above each** (what it does), and **an example of the output** after a
  command whose output matters (the owner asked both, 2026-09-30).
- **No test may pin the shipped story's mood mapping** (the owner, 2026-09-30: "do not hardcore tests to the
  particular mapping of emotions, that will change, instead mock the file if your tests rely in a particular
  mapping"). Test the shape; mock the file when a mapping matters.
- **Decoupling is a value**: the owner dislikes hidden links between tools and files (the casting script reading the
  story's file was removed for that — §4). Data maps belong where they are central (the story), not in tool configs.
- **The owner leads the wording of what the model receives**; **improvisation is the feature** (2026-09-28: invented
  places and details are wanted, not bugs).
- **Live checks on the box cost the owner's time**: run them when asked, and say what they cost (requests, seconds).
- **Every number in settings** for the show engine; tools take their numbers as options or config.
- **Code comments per repository**: minimal in zombie-radio; in the fork (TalkWithZombies), upstream's docstring
  style, lines ≤ 120 characters, no en dash in code.
- **No delegation** to sub-agents; **no git kung-fu**.
- **PRs**: fork `gh pr create --repo alfre2v/TalkWithZombies --base master`; zombie-radio `--base main`; check with
  `mcp__ccd_pr__get_status`; the owner merges.
- **Check the clock with `date`** before writing a time. **Verify before claiming state.** **Never invent example
  data** (a made-up timestamp was caught on 2026-09-30 — use real outputs).
- **Security (the owner, 2026-09-30):** no inbound connection to the laptop, ever — no open port, no firewall
  exception on a venue's network ("Who do you think I am... A frontend dev? 😛"); audience interaction only through a
  third-party gateway read over outbound HTTPS.

### 0.1 The box and the laptop (binding, unchanged)

1. The OWNER owns the SSH tunnel, the box's power, and deploys. The agent reaches only `localhost:8080` (llama.cpp),
   `:8001` (tts-serve), `:8002` (Whisper).
2. Box inspection only as plain `ssh ubuntu@<box> '<cmd>'` with an address the owner gives in chat; never read the
   owner's SSH directory.
3. One line saying what a command does, before running it.
4. Probe before any chain of requests (anything but 200: stop, tell the owner):
   `for u in localhost:8080/health localhost:8001/capabilities localhost:8002/docs; do printf '%s ' "$u"; curl -s -m 3 -o /dev/null -w '%{http_code}\n' "$u"; done`
5. **No box address in any markdown or commit, ever.** `deploy/ansible/inventories/cloud/hosts.yml` is `NEVER_COMMIT`
   and is **wired (modified) right now** — never stage it; stage by explicit path. **Pre-commit IP scan on the STAGED
   diff only: `git diff --cached | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}'`** — on 2026-09-30 a `git diff` of the whole
   tree read the wired `hosts.yml` and printed the box's address into tool output (no file, no commit; the agent's
   mistake).
6. Nothing changes on the box outside the playbook.
7. **Scratch files go in the session's scratchpad only**:
   `/private/tmp/claude-501/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18/scratchpad/`
   (one file was written one level above it on 2026-09-30 and deleted — the agent's mistake). Never `/tmp`.
8. **Downloads**: state the file, source, size and licence before; the owner approves. The dry runs of `fetch_ears.py`
   give exact sizes (an estimate once came out 2× wrong — always dry-run).

## 1. The project in 60 seconds

**Zombie-Radio**: an interactive, audio-only radio play — four AI scientists (Daniel, Moira, Ralph, Samantha the
operator) trapped in a secret lab during a zombie outbreak, broadcasting; listeners talk back (hold to talk) when the
lab's receiver works. **Deadline 2026-10-08** (8 days from this writing); a talk at the **Austin Python Meetup** in
October 2026. The app is **TalkWithZombies** (`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`,
`github.com/alfre2v/TalkWithZombies`), the owner's fork of scorbo2's TalkWithMe 7.1; **zombie-radio** (this repo,
checkout folder `zombie-radio-claude`) holds the deployment, the docs, and now the voice tools. Models on a rented
Hyperstack A6000 ("the box"): llama.cpp (Nemotron Nano 9B v2), tts-serve 1.2 (Faster Qwen3-TTS,
`Qwen/Qwen3-TTS-12Hz-1.7B-Base`), Whisper. The spec: `docs/specs/product-definition.md` (linear, as built).

**The demo's goals** (the owner, 2026-09-30; README "What the demo shows"; `docs/discussions/2026-09-30-demo-goals.md`):
1. story coherence and improvisation; 2. **emotional voices in support of the narration** (the work of this session);
3. automated deployment to a cloud GPU (done); 4. automated deployment to a local GPU (a 3090; built, never run).
The discussion also holds the agent's pool of ten creative goals, classified by the owner (§5-§6), and idea 8 (the
audience writes the news) — only through a third-party gateway, deferred (§7).

## 2. Exact state (2026-09-30, 17:41 CDT)

- **zombie-radio**: `main` at `7a76bed` (PR #17 merged). Branch **`alfre2v/mood-voices-shape`**, **PR #18 open**
  ("not to merge yet"), last pushed `431663f`; **this handoff's commit adds**: the screening tool
  `tools/voices/screen_voices.py`, `cast.yaml` (Daniel p085), the README and runbook's screening step, the
  discussion's §11.12, the follow-ups' updates (the degraded-voice status, the debug-audio-and-seed entry), and this
  handoff. `hosts.yml` wired, unstaged.
- **The fork**: `master` at `4b2da26` (tag `tz-0.3` at `0ec33c1`, two README-only commits after). Branch
  **`alfre2v/mood-clips`**, **PR #8 open** ("not to merge before the owner's listening test"), at `1dfb5ac`, clean.
  Suite **1148 passed**; Node `test_persona_form.js` 17, `test_tts_settings.js` 91, `test_show_page.js` 38,
  `test_show_gauge.js` 8.
- **The dev server**: the fork's checkout on `alfre2v/mood-clips`, **running on port 8010, pid 76234**, started
  15:22 with **temporary dev settings**: the fork's `settings.yaml` has `show: {debug: true}` instead of
  `seed: 42`. **Restore when done**: `cp <scratchpad>/settings.yaml.before-trim settings.yaml` in the fork, then
  `cmp`; stop the server with `kill $(lsof -nP -iTCP:8010 -sTCP:LISTEN -t)`. It reads the client's Personas folder
  (`personas_directory: /Users/alfredo/TalkWithZombies-client/Personas`).
- **The installed client** `~/TalkWithZombies-client`: at **`tz-0.3`** (no mood voices yet — they arrive with
  `tz-0.4`); its `settings.yaml` has `show: {debug: true}`, added by the agent on the owner's order that morning
  (backup `<scratchpad>/client-settings.yaml.before-debug`; to remove, delete the two lines). **Its Personas folder
  holds the current cast**, every character with `ref.wav` + 23 `ref-<emotion>.wav`/`.txt` + `ref.source` +
  `ref.placeholder.*`: **Daniel p085** (recast 17:27:44), **Moira p026**, **Ralph p017**, **Samantha p063** (recast
  16:46:49).
- **The downloads**: `/Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/` (outside git, 1.2 GB):
  `README.txt`; `ears/<speaker>/` for 96 speakers (95 native American English with neutral + fear; **20 shortlisted
  with all 23 emotions**: women p106, p100, p092, p063, p062, p059, p033, p026; men p102, p101, p095, p088, p087,
  p086, p085, p057, p054, p046, p017, p007); pages `index_all_speakers_2emo.html` (the owner's rename), 
  `index-2026-09-29T14:06:44.html` (the 20 × 23 pick page), `screen-2026-09-30T17:29:11.html` and `.json` (the tool's
  test), `stray-speech-2026-09-30.html` (built by hand for the owner's ear check).
- **The box**: up; all three services 200 at 17:09.

## 3. What happened since handoff 7 (2026-09-28 19:36 → 2026-09-30 17:45)

1. **2026-09-28 night**: the looks recorded (PR #14); `tz-0.3` tagged (the fork's looks, PR #5 merged) and the
   installer pinned to it (PR #15); a pass over TODO/follow-ups/roadmap (Task 6 moved to "Done in this arc").
2. **The voice-dataset research** (`docs/discussions/2026-09-29-voice-datasets-with-emotion.md`): real human voices
   recorded in several emotions, licences checked at the source; four finalists — **EARS** (CC BY-NC 4.0, 107
   speakers, 22 emotions + neutral, 48 kHz anechoic), CREMA-D, JL-Corpus (added by the owner), Expresso (added by the
   owner).
3. **The EARS remote-fetch experiment** (`docs/experiments/2026-09-29-ears-remote-fetch/`, **PASS**): single WAV files
   pulled out of the per-speaker GitHub-release zips with HTTP range requests; runs 1-7 in its runlog; the audio lives
   outside the repo.
4. **The casting** (§11.3-§11.5): option A (a casting script, the mapping as data; the owner discarded option B, the
   app reading the experiment folder); `tools/voices/cast_voices.py` + `cast.yaml`; the first cast (p007, p026,
   p017, p033). PR #17 merged.
5. **2026-09-30**: the demo goals (PRs #16 and the fork's #6); the downloads moved to `zombie-radio-datasets/`
   (§11.6; the fetch script's working copy in `tools/voices/`; the experiment keeps its own as the record); the
   runbook `docs/runbooks/cast-voices.md` and the README's "Voices for the cast"; the fork README's screenshots
   (PR #7); the reference-format measurement (§11.7: size and format do not explain the delay between lines; MP3 and
   Ogg/Opus accepted, no audible loss; the follow-up "Compressed reference clips", re-examine before demo day, Task 7
   reminds of it).
6. **The voices follow the mood** — shape (§11.8), built (§11.9, fork PR #8): the story maps moods to recordings,
   the page names the clip, the voice route uses it or `ref.wav`; **decoupled** — the casting copies all 23
   emotions (`--all-emotions`), the story's `voices` map is the only mapping; the owner's first listen: "It works!"
   (§11.11); the owner's remaps; "Wow, the show is very good now. What a difference since we started."
7. **Recasts and the screening** (§11.11-§11.12): Samantha p033 → **p063** (livelier); Daniel's feminine drift →
   stray speech found in p007's distress clip; a screening (Whisper + pitch) found more; **the screening became a
   tool** (`tools/voices/screen_voices.py`); Daniel p007 → **p085**.
8. **Another feminine Daniel line** ("Daniel (excited): Candles! …", run `2026-09-30T17-28-18`, round 9): the owner
   suspected Samantha's clip was sent; the agent checked — the app picked Daniel's own `ref-extasy.wav` (p085, clean:
   138 Hz, match 1.00), and the voice server's cache key includes the clip's path (content hash):
   `faster_qwen3_tts/model.py:430`, `cache_key = (str(ref_audio), ref_text, xvec_only, append_silence)` (version
   0.5.3; the playbook does not pin the library). Leading explanation: the engine drifting off the speaker on one line
   (suspect 3). **The replay test was proposed, not run.** The owner then asked to save the audio in debug mode: the
   follow-up "Keep every synthesized chunk in debug mode, and send a seed with every voice request" — **decided (yes,
   seed always), not built**.

## 4. The voice system, as built

**Three tools in zombie-radio's `tools/voices/`** (README "Voices for the cast"; runbook `docs/runbooks/cast-voices.md`):

- `fetch_ears.py` (python3, stdlib): `--speakers-info` (filters `--gender`, `--age` bracket, `--native`),
  `--list --speakers 7`, `--types 'emo_*_sentences' --speakers 7,17` (dry run; `--fetch` downloads), "already here"
  skips, a page of players per fetch (`index-<start time>.html`). Default output `../zombie-radio-datasets/ears`.
- `screen_voices.py` (python3, stdlib, needs the tunnel): `--speakers 85,54,88` [`--emotions fear,distress`];
  Whisper transcribes each clip, words compared with the transcript (contractions/times normalized); pitch against
  the speaker's neutral; flags **stray speech** (≥ 2 extra words, `--extra-words`), **weak match** (< 0.80,
  `--min-match`), **pitch climbs** (> 1.5 × neutral, `--pitch-rise`; a rise of exactly ×2.00 may be an estimator
  octave error); writes `screen-<start time>.json` and a page of players for the flagged clips. ~20 s per speaker.
- `cast_voices.py` (`uv run python`, needs PyYAML): reads `cast.yaml` — `source: ../zombie-radio-datasets/ears`,
  `personas: ~/TalkWithZombies-client/Personas`, `cast:` (character → speaker), `voice: emo_neutral_sentences`,
  `loudness_dbfs: -20`, `peak_dbfs: -1`; writes `ref.wav`/`ref.txt` (+ with `--all-emotions` every
  `ref-<emotion>.wav`/`.txt`), `ref.source` (the record of what was written); keeps `ref.placeholder.*`; checks
  everything before changing anything; `--only Moira`, `--dry-run`. Loudness: RMS to -20 dBFS unless the peak would
  pass -1 dBFS (80 of 96 clips were peak-limited; results -26.9 to -20.0 dBFS). **Always cast with
  `--all-emotions`** (without it every mood falls back to `ref.wav`).
- **Who voices whom**: `cast.yaml` is the decision (in git); `Personas/<Name>/ref.source` is what was written (the
  truth if they disagree). One-line check:
  `for f in ~/TalkWithZombies-client/Personas/*/ref.source; do echo "$f: $(sed -n 2p "$f")"; done`.

**The app** (the fork, PR #8): the story's `stories/lab-outbreak/overtones.yaml` has `voices` per overtone — **the
owner's current map**: calm `ref.wav`; happy `ref-amusement.wav`; hopeful `ref-amazement.wav`; excited
`ref-extasy.wav`; relieved `ref-relief.wav`; doubtful `ref-confusion.wav`; **urgent `ref-anger.wav`**; curious
`ref-realization.wav`; determined `ref-pride.wav`; sad `ref-sadness.wav`; afraid `ref-fear.wav`; terrified
`ref-distress.wav`; angry `ref-anger.wav`; exhausted `ref-pain.wav`. Unassigned: adoration, contentment, cuteness,
desire, disappointment, disgust, embarassment, guilt, serenity. (EARS spells `extasy`, `embarassment`.) The loader
(`app/show/story.py`, `voice_map()`) enforces all-or-nothing, a voice per mood, plain clip names
(`persona_store.REFERENCE_CLIP`: `ref.wav` or `ref-<word>.wav`); `show.mood_voices` (default on) — off, every line
`ref.wav`; the start reply carries `voices`; the page (`player.js`, `show.js`: `voiceOf(mood)`) posts
`{text, persona_name, reference}` for every chunk; the route (`app/routers/tts.py`) uses the persona's own clip
(`reference_clip()`) or `ref.wav`, and replies with `reference` (the clip used); **the debug line shows
`voices Daniel ref-extasy.wav, …`** once a round has been said. Debug files (`runs/<run-id>/debug/`) hold only the
model's side; the run record holds each line's mood, not the clip.

## 5. Open threads and the board ahead

**Immediate (in this order unless the owner says otherwise):**

1. **The owner's ear check of the stray speech** — page
   `/Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/ears/stray-speech-2026-09-30.html` (five real cases +
   two false alarms). **Then** correct two cast transcripts to what was said, in the downloaded copies:
   `zombie-radio-datasets/ears/p017/emo_confusion_sentences.txt` ("Appreciate it" before — Ralph's *doubtful*) and
   `…/p063/emo_pride_sentences.txt` ("I'm amazed." before — Samantha's *determined*), then recast Ralph and Samantha
   `--all-emotions --only …`. Also p063's disappointment has stray speech (unused).
2. **Moira sounds too similar to the new Samantha** (the owner: "I actually prefer Samantha now … I might have to
   replace Moira's voice"). Candidates (different age from p063, 36-45): p062 18-25, p059 26-35, p106 56-65, p033
   56-65 (the old Samantha); p092, p100 are 36-45. **Screen before casting** (`screen_voices.py`).
3. **Daniel p085**: one screening flag — confusion climbs ×1.75 (his *doubtful* lines); worth a listen.
4. **The debug-audio-and-seed feature** (follow-up, decided: yes, seed always) — **build when the owner says go**, in
   the fork (probably on `alfre2v/mood-clips` or its own branch; ask). The "Candles!" replay test — pending.
5. **Merge and release**: PR #18 (zombie-radio) and PR #8 (fork) when the owner is satisfied; then **tag `tz-0.4`**,
   bump `client_version` in `deploy/ansible/client-talkwithme-mac.yml` (as done for `tz-0.3`: tag commands shown step
   by step), the owner's re-proof (`make client-mac`, re-run `changed=0`, `git describe`), and record it.
6. **Records still behind**: the TODO (Task 4 says "a first cast"; nothing about mood voices, the screening, the
   recasts; "Now" needs an update); **the spec** (`docs/specs/product-definition.md`) has no mood voices yet (§6 — the
   page and the voice) — update after PR #8 merges; the roadmap maybe.
7. **At the end of listening**: stop the dev server, restore the fork's dev settings (§2); decide about the client's
   `show: debug: true`.
8. **Branch cleanup** (the owner's rule: keep the last 2-3 branches) — offered, not done; list before deleting.

**The rest of the board (8 days):** goal 4 (the 3090: driver check, first run of the local target) · goal 1:
names-only A (~1.5-3 h), the trim thresholds in settings · **Task 7, the canned episode (a MUST)** — best recorded
after the voices settle · the dead-air static (polish) · the compressed-reference switch before demo day (follow-up) ·
the degraded-voice follow-up (postponed; note the line or round next time).

## 6. Facts and numbers worth keeping

- EARS files per speaker: 161 (46 emotional: `emo_<emotion>_sentences` with transcripts, `_freeform` without); an
  `emo_*_sentences` clip is ~7-15 s (pride and realization longer, up to 31.6 s); 48 kHz 32-bit float mono; the whole
  set 69.2 GB (107 zips, 564-804 MB each).
- Reference clips after casting: mono 24 kHz 16-bit, ~0.45-0.8 MB; the app base64s the clip into every voice request.
- Measured (§11.7): the request size (52-643 KB) barely changes the time on this link (~0.5 s outside synthesis);
  synthesis ~1.7-2.0 s per chunk; tts-serve's formats: wav, mp3, ogg, flac (all eight engines declare them; proven on
  Faster Qwen3-TTS only).
- The show's overtone shares (§11.11): a 31-round show ~35 % negative rounds; the 113-round seed-42 listen 47 %; the
  director's drift weights 1 : 2 : 3 (positive : neutral : negative).
- The screening's findings (§11.12, follow-up): stray speech in p007 distress, p017 confusion, p063 pride, p046
  confusion, p101 realization, p063 disappointment; low-pitched men (highest negative median): p054 118 Hz, p088 131,
  p085 133; p007's negatives reach 235 Hz (a woman's range ~ 180-250).
- Runs of 2026-09-30 in the fork's `runs/`: `15-23-48` (first mood voices, 31 rounds), `16-23-45` (57),
  `16-47-31` (50, Daniel's "not human" line round 45), `17-28-18` (Daniel's "Candles!" round 9), plus an empty
  `15-22-29` (the agent's start-reply check).

## 7. Nuances

- The owner listens on the dev server in Chrome and reports lines by text; when a line goes wrong, find it in the
  run's `script.json` (mood → the story's map → the persona's file → `ref.source`), then measure — the owner's first
  hypotheses (a long clip; a wrong clip sent) were both ruled out by evidence, and the real causes (stray speech,
  pitch) were found by the owner's ear and the screening together.
- The owner edits files directly (the story's `voices`) and asks the agent to check spelling — load the story and
  check every named clip exists for all four characters.
- The owner likes pages of players (the fetch pages, the stray-speech page, the screening page) and explicit example
  outputs; loves when a convenience is explained ("it would be shame to go unnoticed").
- The owner jokes ("my robot buddy 😛") and is patient, but calls out slowness and repeated mistakes.
- EARS voices are calm, with a reading rhythm (volunteers reading sentences in an anechoic chamber); livelier sources
  for after the demo: EARS's free-form clips (need Whisper transcripts), Expresso (actors, dialogue).

## 8. Mistakes this stretch (do not repeat)

- Scanning `git diff` of the whole tree (read the wired `hosts.yml`) — scan `git diff --cached` only.
- A file written outside the scratchpad; an invented timestamp in a doc example; an estimate given as a size before a
  dry run (130 MB said, 250 MB real); tests pinned to the shipped mapping; a pointer left stale (the README's cast
  command without `--all-emotions` — the owner caught it); the casting coupled to the story's file (the owner:
  "Took you a while, but I am patient with my robot buddy 😛").

## 9. Techniques

- **Find a line in a run**: python over `runs/<run-id>/script.json` (rounds → lines: `speaker`, `mood`, `spoken`,
  `fixed`; rounds: `n`, `kind`, `overtone`).
- **Load the story's map**: in the fork, `.venv/bin/python -c "import logging; logging.disable(logging.WARNING);
  import app.show.story as s; print(s.voice_map(s.load_story('lab-outbreak')))"`.
- **Clip facts**: `afinfo <wav>` (format, duration); pitch — `screen_voices.py`, or the scratch `pitch.py`.
- **Fork checks**: `.venv/bin/python -m pytest -p no:cacheprovider > <scratchpad>/x.log; tail -1` (grep the
  summary: output is buffered); Node `node tests/<file>.js | grep -E 'ℹ (pass|fail) '`; remove `__pycache__`;
  `awk 'length > 120'`; `grep -c '–'` on the added lines.
- **zsh**: a variable holding options or files does not split — write commands out; quote URLs with `?`.
- **Background runs** notify on completion; Python's output is buffered to a file until the end.

## 10. Reading order after the compaction

1. This document, in full (§11 included).
2. `git status -sb` and `git log --oneline -6` in both repos; `gh pr view 18 --repo alfre2v/zombie-radio`,
   `gh pr view 8 --repo alfre2v/TalkWithZombies`; `lsof -nP -iTCP:8010 -sTCP:LISTEN -t` (the dev server).
3. `docs/discussions/2026-09-29-voice-datasets-with-emotion.md` §11.8-§11.12 (the mood voices and the screening).
4. `docs/follow-ups.md`: "Keep every synthesized chunk in debug mode…", "A cloned line came out badly degraded,
   once…", "Compressed reference clips…".
5. `docs/runbooks/cast-voices.md` (the procedure, the screening step 4b, who voices whom).
6. `docs/discussions/2026-09-30-demo-goals.md` §1 and §3 (the goals and where each stands).
7. Then report: the clock, the tunnel (probe first), both PRs, the dev server, the cast, and **§5's open threads** —
   and ask what to do next. Wait for the go.

## 11. Paste-ready prompt

```
We continue the Zombie-Radio work of 2026-09-30 after a compaction. Today we gave the cast real human voices from
the EARS dataset, made the voices follow each line's mood (fork PR alfre2v/TalkWithZombies#8, zombie-radio PR
alfre2v/zombie-radio#18, both open), built a screening tool for stray speech and pitch, and recast Samantha (p063) and
Daniel (p085). Re-orient before doing anything else:

1. Read docs/discussions/2026-09-30-show-engine-session-handoff-8.md IN FULL — §0 is binding (how we work, the box
   and laptop rules in §0.1), then the exact state (§2), what happened (§3), the voice system as built (§4), the open
   threads (§5), facts (§6), nuances and mistakes (§7-§8), techniques (§9) — and §13, the addendum after 17:45, which
   overrides §2 and §5 where they differ (Daniel back to p007, the voice-instability question, the build spec of the
   debug-audio-and-seed feature, which has my go).
2. Follow its reading order (§10): both repos' status and log, PRs #18 and #8, the dev server on port 8010, the
   voice-datasets discussion §11.8-§11.12, the three voice follow-ups, the cast-voices runbook, the demo goals.
3. Then give me a compact summary — the clock, the tunnel (probe it first), both PRs, the dev server and its
   temporary settings, the current cast, and the open threads of §5 — and ask what to do next. Wait for my go.

Standing rules: strict review-before-commit (I review in VS Code — no diffs in chat, no commit without my explicit
order for that commit), push only when told, no AI attribution anywhere, discussion-first (one decision at a time,
with its context), docs as detailed as the chat and with my words verbatim, no test pinning the story's mapping,
improvisation is the feature, plain and explanatory language, no delegation, no git kung-fu, code comments per
repository (minimal in zombie-radio; upstream's docstring style in the fork), IP scans on the staged diff only, never
stage hosts.yml, scratch files only in the scratchpad.
```

## 12. The owner's words of this stretch (verbatim, from the transcript)

- On the voices: "Wow, this is really good. Our hard work is paying off. The audio quality of the voices is amazing."
  · "Wow, the show is very good now. What a difference since we started. The emotions work very well, and I have not
  seen more incidents of voice degradation."
- On the mapping's home: "I do not like that the map for something as central to the app as voice emotion be defined
  in such an unexpected place." · On the decoupling: "Bingo!, you finally understood the decoupling of the mapping
  with the file names. Took you a while, but I am patient with my robot buddy 😛"
- On tests: "Please do not hardcore tests to the particular mapping of emotions, that will change, instead mock the
  file if your tests rely in a particular mapping."
- On EARS: "the voices are too calm, and a bit unnatural rhythm, in general, probably due to the strange studio
  settings it was recorded".
- On screening: "the number of deviations I've found is noticeable. Therefore we need some automated method to
  narrow our search space. Please incorporate this script into our project and document well how to use it."
- On the recasts: "I actually prefer Samantha now, she sounds louder and have more emotion." · "I think we need to
  replace Daniel." · "recast Daniel with p085".
- On debug audio: "We should save them so we can trace back this problems." · "yes to 1 and 2, seed always; record
  the follow-up. But do not execute yet".

## 13. Addendum, 18:10 CDT — after 17:45 (overrides §2 and §5 where they differ)

### 13.1 State changes

- **zombie-radio**: `db97a71` (the handoff commit) pushed to PR #18. The commit of this addendum adds `cast.yaml`
  (**Daniel: p007**) and this section.
- **Daniel back to p007** (17:46:05, `--all-emotions --only Daniel`). The owner (verbatim): "I think I want to go back
  to the previous Daniel. […] I like that his voice is way different than Ralph, and if the TTS is going to make voices
  feminine sometimes it's less notable with his old voice." **The current cast: Daniel p007, Moira p026, Ralph p017,
  Samantha p063.**
- **p007's distress transcript corrected** (17:51, outside git, in the datasets folder). The owner: "fix Daniel's
  transcript now, but make sure to leave a note next to the changed transcript explaining why we deviated from the
  original dataset." In `/Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/ears/p007/`:
  `emo_distress_sentences.txt` (corrected: "Can just eat all of them. Oh God, I'm not sure if we're gonna make this
  flight on time. …" — Whisper's text, the aside confirmed by the owner's ear), `emo_distress_sentences.txt.original`
  (EARS's), `emo_distress_sentences.CORRECTION.txt` (what, why, source, how it reaches the app, how to undo, the
  re-fetch warning). **The convention for the next corrections** (p017 confusion, p063 pride — still waiting for the
  owner's ear check): the same three files, and a line in `zombie-radio-datasets/README.txt`, section "Corrected
  transcripts" (added now). Daniel recast at 17:51:29; `screen_voices.py --speakers 7 --emotions distress,neutral` →
  **0 flagged** (was 6 extra words). **Not yet in the repo's docs**: record the correction and Daniel's return in the
  voice-datasets discussion (a dated addendum) at the next commit.

### 13.2 The voice-instability question (open)

- **The report** (~17:53, verbatim): "Oh, wow, now things are much worse in the TTS. Instability in all the voices. I
  do not think it has anything to do with the transcript change in Daniel... Maybe your audio normalization is making
  things bad."
- **Evidence gathered**: Moira's and Ralph's clips unchanged since 15:21-15:22, Samantha's since 16:46 — all sounded
  good after ("the show is very good now"); the normalization unchanged since 2026-09-29; the dev server continuous
  since 15:22, its voice requests 200.
- **Seeds**: the app sends **none** (checked: `app/routers/tts.py`, `app/services/tts_client.py`, `app/models.py`,
  `static/show/player.js`; `tts.parameters` is `{}` in both `settings.yaml`). tts-serve picks one per request —
  `seed = req.seed if req.seed is not None else random.randint(SEED_MIN, SEED_MAX)` (1..1000,
  `impl/server_fasterQwen3TTS.py:458`), `torch.manual_seed(seed)` inside the synthesis lock (line 497) — and **echoes
  the seed in its reply**. The owner asked "Did you change anything related to a seed for the TTS server?" — no.
- **The engine is healthy** (the one-request test, ~18:05): Moira's `ref.wav`, the 13:00 sentence, seed 42 →
  **byte-identical** to the 13:00 reply (249,644 bytes, 5.20 s; server 1.73 s). Files in the scratchpad's `refs/`
  (`out-new_wav-2.wav`, `out-now-seed42.wav`).
- **The owner's observation (verbatim)**: "when I reload the page from `http://127.0.0.1:8010/show` and pick the skin
  page again, the voices stabilities are perfect. But if instead I just reload the skin page
  `http://127.0.0.1:8010/show?design=old-radio` and run the show again there, the instability appears". **No mechanism
  found**: the page sends only `{text, persona_name, reference}` per chunk. Hypotheses: (1) **randomness** — a random
  seed per chunk and a new story per run, a streak read as a pattern (leading); (2) **a real difference in requests
  after a reload** (e.g. cached old scripts sending no `reference` — would sound calmer, not unstable). Checks: compare
  `/api/tts` request bodies in both paths (Chrome's Network tab, or the built-in browser); properly: the feature below.
- **The owner's decision**: "Ok, we are going to build that feature" — after the compaction.

### 13.3 Build spec — keep every chunk's audio in debug mode, and a seed with every voice request (the owner's go)

The follow-up "Keep every synthesized chunk in debug mode, and send a seed with every voice request" (in
`docs/follow-ups.md`) has the agreed shape; the details found since:

- **Where**: the fork. **Ask the owner** whether it goes on `alfre2v/mood-clips` (PR #8, not merged; the same page
  code) or a new branch cut from it. Tests in the fork's style; no test pins the story's mapping.
- **Knowing the chunk's place early**: every line's stream events already carry `message_id =
  "<run-id>-r<NNN>-l<L>"` (the fork's `app/routers/show.py:227`) — the page has the round and line numbers when it
  requests the voice, before the round's summary; the chunk number is the index in `speakLine`'s parts
  (`static/show/player.js`).
- **The seed, always**: derive it from the run's seed and the chunk's place (round, line, chunk) — **within 1..1000**,
  the server's range (`SEED_MIN`/`SEED_MAX`; a value outside is refused) — send it with every chunk. The voice payload
  builder (`app/services/tts_client.py`, `advertised()` / the parameters loop near line 508) passes any parameter the
  capabilities advertise, and `seed` is advertised. The reply echoes the seed used — record that one.
- **The save, debug only**: with `show.debug`, the page adds a tag to each voice request
  (e.g. `debug: "2026-09-30T17-28-18/r009-l2-c1"`); `TTSRequest` gains optional `debug` and `seed`; the route checks the
  tag strictly (the run id's own pattern, numbers only, the run's folder must exist — nothing can name another folder)
  and writes `runs/<run-id>/debug/audio/r009-l2-c1-<Persona>-<clip stem>.wav` (the reply's audio, decoded) and a `.json`
  beside it: the text, the persona, the clip asked for and used, the seed (echoed), `time_used`, the sample rate. Debug
  off, or no tag (TalkWithMe's chat UI): nothing changes. ~35-45 MB per 50-round run (`runs/` is gitignored).
- **Replay**: document how to resend one chunk from its `.json` (the clip, the text, the seed) — the recipe of
  the one-request test above; maybe a small script.
- **Docs**: the fork's runbook `docs/runbooks/show-page.md` ("The debug line" and the audio folder); zombie-radio's
  follow-up marked built; the voice-datasets discussion (an addendum). Estimate 1.5-2 h with tests.
- **Then use it**: run the show both ways (via the chooser; reloading the look's page) with debug on and compare the
  saved chunks and their requests — settle §13.2.

### 13.4 The screening tool — how to use it (the owner: "I have no idea how to use it")

Documented in the runbook `docs/runbooks/cast-voices.md`, **step 4b** (why, what it checks, the flags, an example
output, what to do with a flag), the README's "Voices for the cast" (step 4), and the discussion's §11.12. In short,
with the tunnel open, from the repo's root:

```bash
python3 tools/voices/screen_voices.py --speakers 62,59,106
python3 tools/voices/screen_voices.py --speakers 7 --emotions distress,fear
```

It prints a line per speaker and each flagged clip (stray speech, weak match, pitch climbs) with what Whisper heard,
and writes `screen-<start time>.json` and a page of players for the flagged clips (`screen-<start time>.html`) in
`zombie-radio-datasets/ears/`. ~20 s per speaker. Use it before casting anyone (e.g. Moira's replacement).

### 13.5 The open threads, in order now

1. **Build §13.3** (go given; ask the branch first).
2. **Use it to settle §13.2** (the instability, the reload observation).
3. **The owner's ear check** of the stray-speech page, then correct p017 confusion and p063 pride with the §13.1
   convention, and recast Ralph and Samantha.
4. **Moira's replacement** (too similar to Samantha p063): screen the candidates first (§5 item 2).
5. **Record** Daniel's return and the transcript correction in the voice-datasets discussion.
6. **Merge PR #8 and #18; `tz-0.4`; the installer's pin; the owner's re-proof**; then the TODO's "Now", Task 4, and
   the spec's mood voices.
7. At the end of listening: stop the dev server, restore the fork's dev settings (§2); the client's
   `show: debug: true`.
8. The rest of the board (§5): goal 4 (the 3090), goal 1 (names-only A, trim settings), Task 7 (the canned episode,
   a MUST), the static, the compressed-reference switch before demo day.

