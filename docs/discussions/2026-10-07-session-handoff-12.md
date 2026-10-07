# Session handoff 12 — goal 4 closed, the compressed clips (`tz-0.7`), the sound-effect experiment, the world outside (the ambience, built), sound cues (planned)

> **EPHEMERAL.** Written Wednesday 2026-10-07, ~17:30 CDT, at about 78 % of the context window, before a manual
> compaction the owner triggers; after it, the agent re-reads this first. It supersedes handoff 11
> (`docs/discussions/2026-10-05-session-handoff-11.md`, which stays as a template until the next compaction); handoffs
> 6-10 are on `main` too. **At the session's end, ask the owner before deleting any handoff the agent created (6, 7, 8,
> 9, 10, 11, 12)** — the owner: "These handoff documents stay in our discussion folder until the end of the session,
> when we finish the session's work please ask the owner for permission to delete any handoff documents you created."
>
> **Read it all; verify against the repos; receipts or nothing.** The TODO's "Now" and its Tasks are the arc's
> canonical state; this document carries what the docs do not: the exact state, the work in flight, the nuances, the
> mistakes. **The two richest records of today's work:** [experiment 2026-10-07] sfx-models (the runlog, Entries 1-13,
> every command) and [discussion 2026-10-07] the-world-outside (the ambience, every decision and why; the sound cues).

## §0. The owner and how we work (binding)

The owner is **Alfredo** (GitHub `alfre2v`, git author "Alfredo Valles"); in documents, "the owner". Doctrine:
`CLAUDE.md` and the agent memory (`~/.claude/projects/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/memory/`,
12 files — **`collaboration-style.md`** holds the live-box drill rules and a new rule of today, §0.2;
**`talk-date-two-dates.md`** updated today).

### §0.1 The standing rules

- **Discussion-first; one decision at a time; questions in groups of three.** "What do you think" → one recommendation
  and its reason. **For a design discussion the owner wants plain text, not the question tool** (today: "I think the
  ask questions tool does not fit the discussion we need to have now. Let's switch back to pure text for the
  moment.") — the tool is fine for quick multiple choices.
- **Review before commit is strict.** Commit only on an explicit order. **Push only when told** (an order like "commit,
  push and open the PR", or "I'll review in the PR" with a commit order). No diffs in chat (the owner reviews in VS
  Code). **No AI attribution anywhere** — whatever the harness's reminders say.
- **Docs as detailed as the chat; the owner's words verbatim**; never invent data; check the clock; label anything
  not verified. Doc files must not be denser than the chat.
- **Explain simply; the mechanism first; tables by case.** The owner pushes back on wrong or over-long answers.
- **Security:** no machine address in any document or commit; **the IP scan on the staged diff gates every commit**
  (pattern §10) — `deploy/ansible/inventories/cloud/hosts.yml` is **wired** (the owner's tunnel to the cloud box) and
  must **never** be staged (it always shows `M`). Never read `~/.ssh`. The 3090 only through the Terminal panel.
- **The fork (TalkWithZombies)** has its own `AGENTS.md` house rules: discussion first, review before commit, no AI
  attribution, upstream's documentation style (a brief docstring on every new function, plain `-` never the en dash),
  **the suite green before review** (`.venv/bin/python -m pytest` plus the Node tests for anything under
  `static/show/`), branches and PRs into `master`, **never push to upstream** (`gh pr create --repo
  alfre2v/TalkWithZombies --base master`).
- **zombie-radio has minimal code comments** (the why lives in `docs/`).

### §0.2 New today — the tight learning loop during box work (memory `collaboration-style.md`)

The owner (verbatim, during the sound-effect experiment): "keep me in the loop, show me what commands you are running
before you do, and what are your preliminary observation and findings. Otherwise I learn nothing during the exercise.
Remember we have to keep the tight learning loop, I want to grow, learn and have fun together with you, not just get
some result." **Before each step: the command and what is expected; after it: what was observed.** Small steps.

### §0.3 The live-box drill rules (2026-09-22, re-learned today)

- **SSH with plain `ssh ubuntu@<box>`** — the owner's own key resolution. **Never pass a key path** (`-i …`), never
  reference key-file locations. (The agent broke this today in a helper script; caught and fixed; recorded.)
- The owner owns the tunnel (`make ssh-tunnel ENV=cloud`, running since 12:03 today, pid of an `ssh -N`); the agent
  uses only the laptop's local ports.
- The box's address never goes into any markdown.

### §0.4 The dates

- **The talk moved again by one week** (the owner, 2026-10-07): "I do not want to keep track of the exact date in our
  docs. No need to correct the docs that say the presentation was on Oct 8." — never write the new date anywhere;
  internal docs keep Oct 8; **the slides keep "Oct 14"** (the owner: "Leave it as it is"). Memory
  `talk-date-two-dates.md`. The extra days are for features: "now we have a few more days to help me decide what other
  features we can add to the project."
- **The owner's website** (`alfre.net`): only the link in the slides; never write its state.
- **The unnamed AI provider** (the talk's "Why not AI APIs (3/3)"): never named anywhere.

## §1. The project in 60 seconds

**Zombie-Radio**: a live, interactive, audio-only radio play — four AI scientists (Daniel, Moira, Ralph, Samantha the
operator) trapped in a lab during a zombie outbreak, broadcasting on a failing shortwave radio; listeners talk back.
The talk at the Austin Python Meetup (internal deadline Oct 8; the slides say Oct 14; the real date one week later,
untracked). Repos:

- **zombie-radio** (`/Users/alfredo/workspace/hackTNT_2026/zombie-radio-claude`, base `main`): deployment (Ansible +
  Docker: llama.cpp with Nemotron Nano 9B v2, tts-serve 1.2 with Faster Qwen3-TTS, Whisper small), the Mac client
  installer (`make client-mac`, pinned to a fork tag), tools (`tools/voices/`, `tools/sounds/`), the talk (`talk/`,
  Quarto, published on GitHub Pages), all docs.
- **TalkWithZombies** (`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`, base `master`): the app (show engine,
  pages, static bed, now the ambience). **Released: `tz-0.7`** (`f2c0edb`).
- **The installed client:** `~/TalkWithZombies-client` (at `tz-0.7`, the owner's; its `settings.yaml` — §2).
- **Outside git:** `/Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/` (EARS voices; `sfx-test/takes/` —
  the experiment's 120 takes; `ambience/round1/`, `ambience/extra/` — the ambience's takes with audition pages).

**Demo goals:** 1 coherence/improv — largely met; 2 emotional voices — met; 3 cloud deploy — met; **4 local GPU (the
3090) — met and closed** (reboot proven 2026-10-07).

## §2. The exact state (2026-10-07, 17:26 CDT)

- **zombie-radio:** branch **`alfre2v/ambience`**, **PR #34 open** (head `16cf799`); uncommitted: `docs/TODO.md`
  (Task 14, the clip-length ruling) and the new `docs/discussions/2026-10-07-the-world-outside.md` — **and this
  handoff** (all to be committed together, on the owner's order, onto #34). `main` at **`ad9c7c9`** (#33). Wired:
  `cloud/hosts.yml` (never stage).
- **The fork:** branch **`alfre2v/ambience`**, **alfre2v/TalkWithZombies#12 open** (head `2197c1c`, 48 files);
  `master` at `f2c0edb` = **`tz-0.7`**. The clone's `settings.yaml` (gitignored): `show:` holds only `seed: 42`.
- **Merge order when the owner merges:** the fork's #12 first, then #34; then the agent tags **`tz-0.8`** on the
  fork's merge (check the merge's tree equals the tested head `2197c1c`, run the suite on `master`), pins the
  installer (`deploy/ansible/client-talkwithme-mac.yml` `client_version`, the README's tag, the spec's header and a
  paragraph — the `tz-0.7` pin, #32, is the model), opens that PR; the owner re-proves (`make client-mac` twice:
  `changed=1` then `changed=0`; `git -C ~/TalkWithZombies-client describe --tags`).
- **Running now:** the fork's `alfre2v/ambience` app on **port 8010** (`uvicorn`, pid 19963 at this writing; a
  background task of the agent) — the owner listens to shows there (`http://localhost:8010/show?design=old-radio`).
  **Never restart it while the owner may be listening without asking.** Stop it when the owner is done.
- **The tunnel** to the cloud box: the owner's (`ssh -N`, since 12:03). `make check` → three ok.
- **The cloud box (A6000):** **up since the morning, billing** — the owner woke it (the plan had been to hibernate
  until the day). Re-hibernating risks the wake lottery (2026-09-24: no A6000 in stock). The owner's call.
  **`~/sfx-lab/` on the box: 39 GB, kept by the owner's ruling** ("in case we want to generate more audios later");
  the disk 17 GB free (the owner: "We cannot leave the disk so tight" — undecided). Inside: `bin/uv`, `uv-cache`
  (~20 GB, hard-linked into the envs), `python/` (3.12), `woosh/` (env + weights), `stable-audio-3/` (env + Flash
  Attention 2.6.3 wheel installed), `moss-tts/` (env; **MOSS weights deleted**), `hf/` (Small-SFX and Medium weights),
  `takes/`, `ambience/`, the scripts.
- **The owner's Hugging Face token stays active** (the owner: "No, I want to keep the HF token active"). It was used
  only at hidden prompts on the box (`read -rsp`), never written anywhere.
- **Task 12 is done end to end:** `tz-0.7` re-proven by the owner (`changed=1`, then `changed=0`; `git describe`
  `tz-0.7`) and switched on in the client — recorded in the TODO's Task 12 in the last commit before the compaction.
- **The installed client's `settings.yaml`** (the owner's; gitignored; the installer never overwrites it):
  `show: # seed: 33767163 / seed: 651594682  # good show 3090 / voice_seed: true / reference_format: ogg`.
- **GitHub Pages:** the talk is live at `https://alfre2v.github.io/zombie-radio/` (a Quarto **website** project since
  #27; republished after #28). `robots.txt`/`sitemap.xml` written by the publish itself.
- **The agent's memory:** 12 files; `talk-date-two-dates.md` and `collaboration-style.md` updated today.

## §3. What happened since handoff 11 (2026-10-05 evening → 2026-10-07)

1. **The talk published** (2026-10-05): #26 merged; `gh-pages` created; `quarto publish gh-pages` refused a `default`
   project → published as a document → the CSS-only decorations missing → **#27 made it a website project**
   (`render: [index.qmd]`), republished; **#28** dropped the director slide's invisible line-4 step (the transparent
   code background hid the highlight) and corrected the runbook's §10. The owner deleted many old remote branches;
   `gh-pages` must stay.
2. **Seeds:** a good show on the A6000 (seed 33767163) and on the 3090 (651594682); **a seed replays a show only on
   the box it was found on** (different GPUs → different sums → different words; the owner: "I know this", not to be
   recorded). `voice_seed` replays the voice too; the same clip + seed gives byte-identical audio.
3. **Goal 4 met and closed:** #29 (Linux deploy, `lan` env, nothing at boot, the Makefile's macOS `sed` fixed), #30;
   the owner's reboot test (2026-10-07: "So we can 100% put to rest all the 3090 exercise. It's done."); Task 11.2 (the
   client on Linux) deferred past the demo.
4. **The extra days' plan** (#31): Task 12 decided; follow-ups "The audience writes the news" (a site on
   `zombieradio.net`, not executed — "I do not want to expend the days before the project worrying about hosting and
   filtering adversarial prompts"; the laptop never accepts inbound connections) and "Send each reference clip only
   once" (a tts-serve change, undecided); "a scientist turns" found to need a story line (demo-goals §9).
5. **Task 12, the compressed reference clips — released as `tz-0.7`** (#11 in the fork, #31, #32): the originals kept,
   `tools/voices/compress_voices.py` writes `ref-*.ogg` (Opus 48 kbps) beside each WAV; `show.reference_format: ogg`
   chooses; 8.4× smaller; no difference to the owner's ear; no speed gain on a fast link. Re-proven; switched on in the
   client.
6. **The sound-effect experiment** (#33; `docs/experiments/2026-10-07-sfx-models/`, Entries 1-13): four models on the
   A6000 — **Stable Audio 3 Small-SFX the model to use** (0.44 s a take, 2.9 GB beside the stack, no effect on the
   voice, 87 % usable); Woosh-DFlow disqualified; MOSS-SoundEffect v2.0 complements Small on two sequences; Stable Audio
   3 Medium set aside (same misses as Small). The live criterion corrected mid-run (live, nobody picks the take). The
   licences of generated audio read (Stability: the user owns the outputs).
7. **Task 13, the world outside — built and heard** (the fork's #12, this repository's #34; the whole story in
   [discussion 2026-10-07] the-world-outside, Part 1): 31 clips (16 textures, 15 spots); an ambience channel inside the
   broadcast; defaults raised by ear to 0.3/0.12; the owner: "it sounds amazing! Very spooky 😃".
8. **Task 14, sound cues — planned** (the-world-outside, Part 2): event rounds only; keywords per clip; a spot plays
   once at the round's start, a texture replaces the current one for its clip's length; ~2½-3 h.

## §4. The systems (pointers)

- **The docs system:** `docs/README.md` (meta), `docs/TODO.md` ("Now"; Tasks 4-14; the owner action queue),
  `docs/follow-ups.md`, `docs/roadmap.md`, `docs/specs/product-definition.md` (describes `tz-0.7`; the ambience not
  yet in it — to add with the `tz-0.8` pin).
- **Today's records:** `docs/experiments/2026-10-07-sfx-models/README.md` (Results table at the top; the runlog);
  `docs/discussions/2026-10-07-the-world-outside.md`; `docs/discussions/2026-10-01-sound-effects.md` §9 (the SFX
  plan, §9.5 the dead outside); `docs/discussions/2026-09-29-voice-datasets-with-emotion.md` §11.15 (the compressed
  clips heard); `docs/discussions/2026-09-30-demo-goals.md` §9 (a scientist turns).
- **The ambience's tools (zombie-radio `tools/sounds/`):** `ambience.yaml` (39 prompts; `keep:` lists = the owner's
  picks), `gen_ambience.py` (on the box, Small-SFX), `ambience_page.py` (audition page), `prepare_ambience.py` (MP3,
  levels, manifest, credits → the fork's `Sounds/ambience/`).
- **The ambience in the fork:** `static/show/ambience.js`, `app/show/bed.py` (generalized), `app/config.py`
  (`ambience_*`), `app/routers/show.py` (`_ambience`, `/api/show/ambience/<file>`), `stories/lab-outbreak/ambience.yaml`
  (31 clips, `enabled`, `gain_db: 0`), `Sounds/ambience/`, tests (`test_show_ambience.py`, `.js`), runbooks
  (`docs/runbooks/show-settings.md`, `show-page.md`).
- **The voices:** `tools/voices/cast_voices.py`, `compress_voices.py`, `cast.yaml`; the fork's `show.reference_format`.
- **The talk:** `talk/`, the runbook `docs/runbooks/talk-slides-quarto.md` (§10 publishing).

## §5. The ambience as built (the essentials; details in the-world-outside §5)

- **Two kinds:** textures (continuous, shuffled) and spots (one every 20-60 s, never the same twice in a row).
- **The chain:** texture → its gain → the silences' gate ─┐ spot → gain × spot_volume ─┴→ level (mono; 0.12 under a
  line, 0.3 between rounds, 0 while push-to-talk) → the bed's AM filter (F flips both) → fading → **A** mute →
  speakers. Never through the bed's mute (M mutes the static only). Silences gate the textures only. Goes on while the
  receiver is on.
- **Why it was quiet at first:** equal RMS is not equal loudness (a moan vs a hiss); "far away" prompts make quiet
  sounds. The proper fix (LUFS in both preparation tools) is noted, not done.
- **Tests:** pytest **1,312** passed; Node ambience 15, bed 29, page 42, gauge 8, persona 17, TTS 91.
- **The ambience is not seeded** — the soundscape differs every run (matters for Task 7's retakes).

## §6. What is left (the board)

1. **Commit** the world-outside document, Task 14 and this handoff onto #34 (the owner's order pending — §2).
2. **Task 13's release:** the owner merges #12 then #34; `tz-0.8`; the installer pin (+ the spec: the ambience);
   re-proof. (§2.)
3. **Task 14, sound cues:** open — **the name** ("sound cues", proposed); **the release order** (the agent's lean:
   `tz-0.8` first, cues as `tz-0.9`). Ruled: event rounds only, keywords in `ambience.yaml`, the clip's kind decides,
   a texture for its clip's length.
4. **Task 9, the talk:** recount the numbers (slides 5 and 27), the A6000's price, republish, rehearse. **The "What's
   next" slide is now stale** (it lists event sounds, comic relief, a scientist turns, new voice engines…; the ambience
   and the compressed clips are built, the sound-effect experiment ran) — and the new features may deserve slides (the
   world outside, the experiment's results). Not discussed yet. Republish after any slide change (runbook §10).
5. **Task 10.1:** the narrower-filter test (the owner's ear, ~20 min).
6. **Task 7, the fallback video:** **last**, once the features are released (the owner: "Features first, video last");
   plus a show against the 3090.
7. **The box:** billing; `sfx-lab/` 39 GB and the disk tight (17 GB free) — the owner to decide; hibernate or not.
8. **The app on 8010:** stop it when the owner is done listening.
9. **Task 8:** the close ritual, after the demo. **Handoffs 6-12:** ask before deleting, at the session's end.

## §7. Facts worth keeping

- **Stable Audio 3 Small-SFX** (`stabilityai/stable-audio-3-small-sfx`, gated, Community License): 433M params; 8
  steps, `cfg_scale` 1.0 (post-trained); half precision; 44.1 kHz stereo; `duration_padding_sec` 6.0 (so a take's time
  is flat across lengths); on the A6000 0.42-0.57 s a take; no Flash Attention needed. Code `Stability-AI/stable-audio-3`
  (MIT), commit `3a82c80`, `uv sync` from its lock (PyTorch 2.7.1+cu126). Its `hf` CLI needs `HF_HOME=~/sfx-lab/hf`;
  run with `HF_HUB_OFFLINE=1`.
- **Medium** needs Flash Attention 2 — the community wheel `flash_attn-2.6.3+cu126torch2.7-cp310` (SHA-256 checked);
  9.7 GB beside the stack.
- **Three CUDA builds (12.6, 12.8) ran on the box's 12.4 driver (550.90.12).**
- **`uv` vs `pip`:** `uv` uses only the first index that has a package (dependency-confusion defence) — split installs:
  PyTorch from its index first, the rest from PyPI. `uv` hard-links packages from its cache into envs.
- **PyTorch 2.9's `torchaudio.save` needs FFmpeg** (TorchCodec); write WAVs with `soundfile` instead.
- **The ambience's levels:** clips at -20 dBFS RMS, peaks capped at -1 dBFS; the defaults 0.3/0.12.
- **Event keyword data (Task 14):** 31 of 289 events (11 %) match a sound group; a real show's lines 11 of 179 (6 %);
  misfires seen ("fire alarm", "feedback shrieks", "rain fills the tanks", "the radio's screaming").
- **Test counts:** the fork 1,312 pytest at `2197c1c` (1,295 at `tz-0.7`).
- **`prepare_ambience.py` (like `prepare_bed.py`) needs macOS** (`afconvert`, for measuring) **and Homebrew's
  `ffmpeg`** (for MP3); it imports `measure` from `prepare_bed.py`, so it runs from `tools/sounds/`.
- **The audition pages keep the ratings in the owner's browser** (localStorage) — the agent cannot read them; the
  owner copies the page's summary and pastes it. The experiment's page is
  `docs/experiments/2026-10-07-sfx-models/listen.html` (four columns; relative paths to the datasets folder).
- **The 3090 has its own Claude Code session** (the owner's "Linux agent"), which built #29; it found the Makefile's
  macOS-only `sed`.
- **Task 14's build notes** (verified in the code): the event is the round's first, fixed line; the reply streams
  per-line `start`/`done` events — **no single "round start message"** (an earlier claim of the agent, corrected); the
  round's `random.Random(f"{run.seed}:{n}")` can pick among matches so a seed replays the cues — the-world-outside
  §9.8, with the keyword data per clip family.

## §8. Nuances

- The owner decides fast when tired and wants results ("I will trust your prompts, I want to see results soon"); still
  wants the loop (§0.2). Celebrate the wins briefly; no gushing.
- The owner offered sudo on the box ("I would even let you issue sudo commands") and FFmpeg ("I can install ffmpeg in
  a second if you need it") — **offer the choice instead of working around alone**; today's constraints still: no
  sudo, everything in `~/sfx-lab/`.
- The owner challenges estimates — answer with what the time is for; the cues went from "half a day" to "2½-3 hours"
  once the owner's simpler design (event rounds only) was adopted.
- The owner values the agent's original points ("This is your most interesting point here") and wants every decision
  recorded with its *why*.
- Prompts: one sound per prompt, no "then"; concrete sound words; "in the distance" makes a sound quiet.
- The client's settings belong to the owner: edit only on an explicit ask ("add those three lines").

## §9. Mistakes this stretch (do not repeat)

- **Passed `-i <key path>` in an SSH helper** (broke the 2026-09-22 drill rule) and wrote the path in a runlog —
  caught, fixed, recorded.
- **Ran box steps as a batch and reported only results** — the owner asked for the loop (§0.2).
- **Restarted the app while the owner listened** → errors on his page. Ask first.
- **Left helper servers running** (8041, 8042) past their use; their timeouts did not stop them. Stop helpers at once.
- **A one-take test that never saved a file** missed the FFmpeg crash; test the whole path.
- **A shell loop broken by zsh's non-splitting of `$c`** (`set -- $c`) — use Python for loops with structured data.
- **`pkill -f` matched its own SSH shell** (the pattern was in the command line) — use `pkill -x nvidia-smi`.
- **Guessed a shuffle order in a test** — compute it.
- **An over-big first estimate** (sound cues) — size the simplest design first.
- **Said "uv's cache keeps its own copy"** — wrong; it hard-links (corrected in Entry 10).
- **Claimed the 3090 had higher clocks than the A6000** — wrong (the A6000's boost is higher; the 3090's memory
  faster); corrected before commit.

## §10. Techniques

- **The box helpers** (recreate in the scratchpad if gone): `box.sh` — `host="$(awk '/ansible_host:/ {print $2;
  exit}' …/inventories/cloud/hosts.yml)"; exec ssh -o BatchMode=yes -o ConnectTimeout=15 "ubuntu@$host" "$@"`;
  `boxcp.sh` — the same with `scp -q` (and a `get` mode: `scp -q -r "ubuntu@$host:$2" "$3"`). Pipe outputs through
  `sed -E 's/([0-9]{1,3}\.){3}[0-9]{1,3}/<box>/g'`.
- **Gated commit:** `git add <paths> && hits=$(git diff --cached | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' | grep -v
  '^127\.0\.0\.1$' | sort -u); if [ -n "$hits" ]; then echo "SCAN HIT"; echo "$hits"; else git commit -q -m "…"; fi`.
  Never `git add -A` (the wired `hosts.yml`).
- **Generating on the box:** `cd ~/sfx-lab/stable-audio-3 && HF_HOME=~/sfx-lab/hf HF_HUB_OFFLINE=1 .venv/bin/python
  ../gen_ambience.py ../ambience.yaml ~/sfx-lab/ambience/<folder> --seeds 1-5 --only <tags>`; copy back with
  `boxcp.sh get`; `uv run python tools/sounds/ambience_page.py tools/sounds/ambience.yaml <folder>`; the owner opens
  `<folder>/index.html` and pastes the summary.
- **Preparing:** `cd tools/sounds && uv run python prepare_ambience.py` (dry run), `--write` (into the fork's
  `Sounds/ambience/`, on a fork branch).
- **The fork's checks:** `.venv/bin/python -m pytest -p no:warnings | tail -1`; `node tests/test_show_ambience.js`
  (and bed, page, gauge, persona_form, tts_settings).
- **A fork PR:** `gh pr create --repo alfre2v/TalkWithZombies --base master …`; PR bodies in the scratchpad.

## §11. Reading order after the compaction

1. This document in full.
2. `git status -sb` and `git log --oneline -3` in both repos; `gh pr list` in both; `lsof -iTCP:8010`.
3. [discussion 2026-10-07] the-world-outside (both parts).
4. `docs/TODO.md` — "Now", Tasks 12, 13, 14, 7, 9, 10.
5. The experiment's README, the Results table (skim).
6. Then report the state and the next steps (§6), and wait for the owner.

## §12. Paste-ready prompt

```
We continue the Zombie-Radio work of 2026-10-07 after a compaction. Today we closed goal 4 (the 3090), released the compressed reference clips (tz-0.7), ran the sound-effect experiment (Stable Audio 3 Small-SFX chosen), built and heard Task 13 "the world outside" — an ambience channel in the fork (PR alfre2v/TalkWithZombies#12, and zombie-radio's #34) — and planned Task 14 "sound cues". Re-orient before doing anything:

1. Read docs/discussions/2026-10-07-session-handoff-12.md IN FULL — §0 is binding (how we work, the loop during box work, the SSH rules, the dates), then the state (§2), what happened (§3), what is left (§6), facts, nuances and mistakes (§7-§9), techniques (§10).
2. Follow its reading order (§11), including docs/discussions/2026-10-07-the-world-outside.md.
3. Then give me a compact summary — the clock, both PRs, the app on port 8010, the box — and the next steps (§6). Wait for my go.

Standing rules: strict review-before-commit (I review in VS Code — no diffs in chat, no commit without my explicit order), push only when told, no AI attribution anywhere, discussion-first, questions in groups of three, explain simply, show me each command before you run it and what you observe after, never invent data, no machine address in any document or commit (IP scan on the staged diff, gating the commit), never stage hosts.yml, never read ~/.ssh, plain ssh without a key path, scratch files only in the scratchpad.
```
