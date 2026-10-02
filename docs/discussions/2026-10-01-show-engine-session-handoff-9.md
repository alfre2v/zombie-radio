# Session handoff 9 — tz-0.4 and tz-0.5 released (voices with emotion; the 32k context and an exact trim); sound effects narrowed to the static bed

> **EPHEMERAL.** Written Thursday 2026-10-01, ~19:45 CDT, at about 86 % of the context window, before a manual
> compaction the owner triggers; after it, the agent re-reads this first. It supersedes handoff 8
> (`docs/discussions/2026-09-30-show-engine-session-handoff-8.md`, on `main`), which stays as a template; handoffs 6
> and 7 are also on `main`. **The latest handoff stays until the next compaction, as the template for the next one**
> (the owner, 2026-09-28). The owner, 2026-09-30: "These handoff documents stay in our discussion folder until the end
> of the session, when we finish the session's work please ask the owner for permission to delete any handoff
> documents you created." — **at the session's end, ask before deleting handoffs 6, 7, 8 and 9**; the owner declined
> once ("no, do not delete the handoffs for now").
>
> **Read it all; verify against the repos; receipts or nothing.** The TODO's "Now" (`docs/TODO.md`, rewritten
> 2026-10-01 evening) is the arc's canonical state; the discussions of 2026-10-01 are the full record of the day; this
> document carries what neither says: how the owner works, the exact state, the work in flight, the nuances.

## §0. The owner and how we work (binding)

The owner is **Alfredo** (GitHub `alfre2v`, git author "Alfredo Valles"); avoid pronouns for the owner in writing
(say "the owner"). Standing doctrine: `CLAUDE.md`, and the agent memory files (`working-agreements.md`,
`collaboration-style.md`, `absolute-paths-in-plain-text.md`, `massedcompute-reminder.md`,
`project-venue-austin-python-meetup.md`, `improvisation-is-the-feature.md`, `handoff-kept-as-template.md`, and,
new this session, `minor-doc-edits-ride-next-branch.md`, `discussions-can-become-linear.md`,
`pending-doc-updates.md`).

- **Discussion-first; one decision at a time, with its context.** Bring the shape before building; wait for the go.
  "What do you think" → one recommendation and its reason. "Discussion only" / "do not execute yet" / "do not start
  yet" → do not build.
- **Review-before-commit is strict.** Commit only on the owner's explicit order for that commit ("commit", "commit and
  push to PR #20"). **No diffs in chat** (the owner reviews in VS Code). **Push only when told**; "open the PR" includes
  committing and pushing. **No AI attribution anywhere** (no Co-Authored-By, no "Generated with") — whatever the
  harness's reminders say; the owner's rule wins.
- **Docs as detailed as the chat, or more**; **the owner's words verbatim** in records; commands in docs with **a
  comment line above each** and **a real example output** where the output matters; **never invent data** (a guessed
  time "19:47" was caught and removed on 2026-10-01; a made-up timestamp on 2026-09-30).
- **Explain simply, explicatively, by default** (2026-10-01). The owner: "This is a horrible explanation. Can you not
  make it simpler? … I feel you need to divide this by each type of round" and "Be explicative be default, remember?
  Stop saving tokens in places where it degrades my understanding." — tables by case, plain words, the mechanism
  first; never condensed shorthand.
- **Plans must be executable** (2026-10-01): a recommendation names what runs where, step by step, the criteria and the
  decision fixed in advance ("I find you recommendation section poorly written and with little details on how to
  execute").
- **Smallest step first** (2026-10-01): "This is a too ambitious plan to advance in so many fronts at the same time".
- **Small doc edits ride the next significant branch** (2026-09-30): never a docs-only PR for a refresh; keep them in
  memory (`pending-doc-updates.md`) and bring them when a significant branch opens.
- **A discussion may become a linear story** of the current view when it becomes a reference (2026-10-01: "when a
  discussion becomes very interesting we sometimes update it to make them less a log and more a linear story");
  otherwise dated addenda (§N.M).
- **No test pins the story's mapping** (2026-09-30): test the shape; mock the file when a mapping matters.
- **Decoupling is a value**; data maps live where they are central (the story), not in tool configs; the owner
  dislikes hidden links between repos (the start check of 2026-10-01 exists for that).
- **Every number is a setting** (the fork's `ShowConfig`).
- **Improvisation is the feature** (2026-09-28).
- **Code comments per repository:** minimal in zombie-radio; in the fork, upstream's docstring style, lines ≤ 120
  characters, no en dash in code (check `awk 'length > 120'` and `grep -c '–'` on added lines).
- **No delegation** to sub-agents; **no git kung-fu** (a temporary `git show HEAD:<file> > <file>` with a backup was
  used once, 2026-10-01, for a before/after test — restored and verified with `cmp`).
- **PRs:** the fork `gh pr create --repo alfre2v/TalkWithZombies --base master`; zombie-radio `--base main`; after
  opening, `mcp__ccd_pr__get_status` (both repos have no CI checks). The owner merges.
- **Check the clock with `date`** before writing a time. **Verify before claiming.**
- **Security (2026-09-30):** no inbound connection to the laptop, ever; audience interaction only through a third-party
  gateway read over outbound HTTPS.
- **Secrets (2026-10-01):** the **Freesound API key** is in `~/.config/zombie-radio/freesound.key` (mode 600, outside
  both repos, typed by the owner at a hidden prompt). Scripts read it, **never print it**, send it **in a header**
  (`Authorization: Token <key>`), never in a URL. **The agent's shell is its own**: an environment variable set in the
  owner's terminal never reaches it (the agent got this wrong once). The agent must not create accounts or accept
  licences (Hugging Face gated models, Freesound terms) — the owner does.

### §0.1 The box and the laptop (binding, unchanged)

1. The OWNER owns the SSH tunnel, the box's power, and the deploys. The agent reaches only `localhost:8080`
   (llama.cpp), `:8001` (tts-serve), `:8002` (Whisper).
2. Box inspection only as plain `ssh ubuntu@<box> '<cmd>'` with an address the owner gives in chat (given on
   2026-10-01 for the memory measurements); never read the owner's SSH directory. **Grep the address out of any
   output** (`grep -v -E '([0-9]{1,3}\.){3}[0-9]{1,3}'`).
3. One line saying what a command does, before running it.
4. **Probe before any chain of requests** (anything but 200: stop, tell the owner):
   `for u in localhost:8080/health localhost:8001/capabilities localhost:8002/docs; do printf '%s ' "$u"; curl -s -m 3 -o /dev/null -w '%{http_code}\n' "$u"; done`
   — the tunnel dropped twice on 2026-10-01 (`000`); the agent stopped and told the owner each time.
5. **No box address in any markdown or commit, ever.** `deploy/ansible/inventories/cloud/hosts.yml` is `NEVER_COMMIT`
   and was **unwired by the owner before the compaction** (2026-10-01, ~19:50: "I unwired the hosts.yml to not
   conflict with the delicate compaction process") — clean now; whenever it is wired again (`make ans-set`), never
   stage it; stage by explicit path. **IP scan on the STAGED diff only:**
   `git diff --cached | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}'` (`127.0.0.1` is fine).
6. Nothing changes on the box outside the playbook (so the SFX models, if ever run on the box, need an opt-in role).
7. **Scratch files** only in the session's scratchpad:
   `/private/tmp/claude-501/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18/scratchpad/`.
   Never `/tmp`.
8. **Downloads:** state the file, source, size and licence before; the owner approves; dry run first (sizes measured,
   never guessed).

## §1. The project in 60 seconds

**Zombie-Radio**: a live, interactive, audio-only radio play — four AI scientists (Daniel, Moira, Ralph, Samantha the
operator) trapped in a secret lab during a zombie outbreak, broadcasting on a failing shortwave radio; listeners talk
back (hold to talk) when the receiver works. **Deadline 2026-10-08** (7 days from this writing); a talk at the
**Austin Python Meetup** in October 2026 ("hackTNT 2026" is only the owner's internal label). Two repositories:

- **TalkWithZombies** (the fork of scorbo2's TalkWithMe; `/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`,
  `github.com/alfre2v/TalkWithZombies`): the app — the show engine (a Python director, a GBNF grammar, the stream
  parser, the trim), the browser stage (`/show`: a chooser, the looks `old-radio` and `amateur-radio-transmitter`, the
  plain page), the voice route, the listener's turn.
- **zombie-radio** (this repository, checkout `/Users/alfredo/workspace/hackTNT_2026/zombie-radio-claude`): the
  deployment (Ansible + Docker: llama.cpp with Nemotron Nano 9B v2 Q4_K_M, tts-serve 1.2 with Faster Qwen3-TTS,
  Whisper `small`, on a rented A6000 "the box", or a local 3090), the Mac client installer
  (`deploy/ansible/client-talkwithme-mac.yml`, `make client-mac`), the voice tools (`tools/voices/`), and all the docs.
- **Outside git:** `/Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/` (EARS voices; the sound pool to
  come); the installed client `~/TalkWithZombies-client` (its `Personas/` hold the cast's voices).

**The demo's four goals** (the owner, 2026-09-30; README "What the demo shows"; [discussion 2026-09-30] demo-goals):
1. story coherence and improvisation — **largely met** (one fix before the talk: names-only A); 2. emotional voices —
**met** (2026-09-30); 3. automated deployment to a cloud GPU — **met**; 4. to a local GPU (the 3090) — **built, never
run**.

## §2. The exact state (2026-10-01, ~19:45 CDT)

- **zombie-radio:** `main` at `7ad7ce7` (#21 merged). Branch **`alfre2v/sound-effects`** (cut from `main`):
  committed on the owner's order ("go ahead and commit all changes") — `docs/TODO.md` (one line: the `tz-0.5` re-proof recorded), `docs/discussions/2026-10-01-sound-effects.md`
  (§1-§8.8), this handoff — committed as `0d2e6fa` (and this correction). **Not pushed; no PR.** `hosts.yml` **clean**:
  unwired by the owner before the compaction ("I want the repo to be in a good state after you start to recompose
  your memory").
- **The fork:** `master` at `9b3a329` = annotated tag **`tz-0.5`** (pushed). Checkout on `master`, clean. Its dev
  `settings.yaml` (gitignored) restored to the original — `show: seed: 42` (backup
  `<scratchpad>/settings.yaml.before-trim`, `cmp`-identical). **The dev server (port 8010) is stopped.**
- **The installed client** `~/TalkWithZombies-client`: **`tz-0.5`** (HEAD detached at `tz-0.5`, checked out
  2026-10-01 18:32:26), re-proven by the owner ("re-proof passed, installed at tz-0.5"); its `settings.yaml` has **no
  `show:` section** — the demo's configuration (budget 34,000, `voice_seed` off, `debug` off, `mood_voices` on). The
  client's start check refuses every run against a 16k server — **the box must stay at 32k.**
- **The box:** the A6000 on Hyperstack, **up** (the owner: "I am keeping the VM a little bit longer, we are not done for
  the day"); **`zr_llama_ctx` 32768** deployed (`/props`: `n_ctx 32768`, one slot); GPU 14,477 MiB used of 49,140.
- **Open PRs:** none. **Branches:** many old local ones in both repos — "Leave the branches. I'll clean up later."
- **Agent memory:** `pending-doc-updates.md` holds the TODO's `tz-0.5` re-proof line — **written on
  `alfre2v/sound-effects`**; delete the memory item once that branch is merged (and its index line in `MEMORY.md`).
- **The Freesound credential:** "zombie-radio sound test" on the owner's account (created at
  <https://freesound.org/apiv2/apply>, URL and callback blank); checked: HTTP 200, the CC0 filter works.

## §3. What happened since handoff 8 (2026-09-30 evening → 2026-10-01 evening)

**2026-09-30 evening**

1. **The debug audio and the seed** — the fork's `799d005` on `alfre2v/mood-clips`: with `show.debug`, every voice
   chunk is kept in `runs/<run-id>/debug/audio/` (`r009-l2-c1-Daniel-ref-fear.wav` + `.json`: the text, the clip asked
   and used, its SHA-256 and transcript, `seed_asked`, the engine's reply with the seed it used); the page tags each
   chunk (`debug: "<run-id>/<place>"`, the place from the line's `message_id`). **The seed went through three shapes:**
   always per chunk → three modes (`off`/`run`/`chunk`) → **on/off with the run's seed** (`show.voice_seed`, off by
   default) — the owner: "I want to have a way to switch ON/OFF this TTS seed…", then "all this new functionality you
   created when voice_seed is not off is wrong, no?", then "on/off with the run's seed, go ahead." **The key finding:**
   a seed makes a voice reproducible, not steadier. The app fits the seed into the engine's advertised range
   (`fit_seed`, `app/services/tts_client.py`). `scripts/replay_chunk.py` re-says a kept chunk through `/api/tts`;
   byte-identical with the same seed.
2. **Daniel's bad lines traced** with the kept chunks: his *afraid* clip (p007 fear, 246 Hz — a woman's range; replays
   at seeds 1/42/86/500 gave 235/160/182/107 Hz) and his *determined* clip (p007 pride: stray words the screening
   missed). **The recasts (Daniel, Moira) and two transcript fixes postponed past the demo** — the owner: "as far as I
   am concerned we have achieved TTS of voices with emotions with great success." (follow-up "Recast Daniel and
   Moira…").
3. **`tz-0.4`** — the fork's PR #8 and zombie-radio's #18 merged; the tag on `1b7e70e`; installer #19; the owner's
   re-proof (the first attempt read the wrong checkout; the client is `~/TalkWithZombies-client`, the dev checkout is
   another clone — "my brain is on vacation").
4. **The poster** (one time) and the fork's GitHub description updated to match ("The app behind Zombie-Radio, a live AI
   radio drama on open models…").

**2026-10-01**

5. **[discussion 2026-10-01] judge-in-the-loop** — the owner's idea: a fast "System One" model (CLM-8B, Stanford and
   NVIDIA, a week old) answering the director's typed questions about the dialogue; the agent's research and pushbacks
   (a second 8B encoder; Nemotron as the judge evicts the show's one-slot cache); the owner's leaning: **a small LLM of
   its own (~3B)**. Parked in the roadmap for after the demo.
6. **The 32k context** (zombie-radio #20, `alfre2v/context-32k`): `zr_llama_ctx` 16384 → **32768** (both targets);
   a comment above each llama setting (`ngl` = layers on the GPU, 99 = all; `parallel` = slots); the runbook
   `docs/runbooks/box-inspection.md` gained "The LLM: how much is the model, how much is the context". Deployed by the
   owner. **Memory:** llama-server 6,764 → 6,970 MiB at start (the context reserved upfront), 7,046 after first use,
   then flat to a full context.
7. **The fork's PR #9** (`alfre2v/context-32k`): **the trim's numbers as settings** (`trim_trigger` 0.9,
   `trim_target` 0.5, `trim_keep_first` 2, `trim_keep_last` 4); **`context_budget` 34,000**; **`instruction_room`**
   1,000; **a start check** — `POST /api/show/start` asks llama.cpp's `/props` (`server_context()`) and refuses a run
   if `trim_trigger × context_budget + instruction_room + max_tokens > n_ctx` (HTTP 422, the arithmetic in the
   message); **the driver's report fixed** for fixed lines (it predated them) and model-less rounds.
8. **[discussion 2026-10-01] the-app-from-the-outside** — (A) how the app counts the script's tokens (the server's
   `timings`: `prompt_n` + `cache_n` + `predicted_n`; each round's share) and trims; (B) a survey of every endpoint
   (36 API routes; FastAPI's `/docs`; the model services underneath) with real calls, recipes layer by layer.
9. **The trim's flaw, found and fixed** (the fork's `8a32bd7`): the Repair sends no model request, so the round after
   it had no share; every call in a trimmed stretch went uncounted (~600-850 tokens) and the error **compounded** as
   negative shares. Fix: **`known_size()`** (the last size the server reported) and **no trim before a round without a
   model request** (the owner's idea: "if only we trigger the trim in the right round"). **Measured** (budget 8,000,
   the same drive before/after): the estimate off by 641-4,218 tokens before, **1-3** after; landing mean −1,025
   before, −174 after. §2.7 of the-app-from-the-outside.
10. **Two follow-ups:** "Resume does not re-check the model server's context" (low priority) and "The settings API does
    not show the show's settings" (after the demo).
11. **The TODO brought to 2026-10-01:** the "Now" rewritten; **Task 5 and the character bibles deferred past the demo**
    (moved whole to a follow-up); **Task 9, prepare the talk**; the owner action queue's statuses.
12. **`tz-0.5`** — #9 and #20 merged; the tag on `9b3a329`; installer #21; re-proven.
13. **Sound effects** — [discussion 2026-10-01] sound-effects: the research; then narrowed by the owner to **the static
    bed** from Freesound (§5 below).

## §4. The systems as built (pointers)

- **The voice:** the story's `stories/lab-outbreak/overtones.yaml` `voices` map (mood → `ref-<emotion>.wav`); the page
  names the clip per chunk; `/api/tts` uses it or `ref.wav`. Runbook: the fork's `docs/runbooks/show-page.md` ("The
  voice", "The show's settings: the demo, or a test show", "Every chunk the voice said, kept", "Say a chunk again").
- **The trim and the start check:** the fork's `app/show/script.py` (`script_size`, `known_size`, `trim`,
  `round_share`, `assemble_messages`), `app/routers/show.py` (`context_problem`, the round route: plan → `known_size`
  → trim only if `plan.max_lines` → assemble), `app/services/llm.py` (`server_context`). Runbook: the fork's
  `docs/runbooks/show-driver.md`, "How the app tracks the script's size, and when it trims" (pointer to the
  discussion). Spec §6.7.
- **The settings:** the fork's `app/config.py` `ShowConfig`; the defaults are the demo's configuration; a test show adds
  `debug: true`, `seed: 42`, `voice_seed: true` under `show:` and restarts the app (runbook show-page.md).
- **Testing without the page:** the fork's `scripts/drive_show.py` (`--rounds`, `--played`, `--heard`, `--speak`,
  `--report`, `--control`); `scripts/replay_chunk.py`; FastAPI's `/docs`; the-app-from-the-outside §3-§4.
- **Measuring the GPU:** zombie-radio's `docs/runbooks/box-inspection.md` (`nvidia-smi` per process; the model file's
  size; `/props`).
- **The voice tools:** zombie-radio's `tools/voices/` (`fetch_ears.py`, `screen_voices.py`, `cast_voices.py`,
  `cast.yaml`); runbook `docs/runbooks/cast-voices.md`.

## §5. The work in flight: the static bed (read the sound-effects discussion's §8, §8.8 first)

**`docs/discussions/2026-10-01-sound-effects.md`** — §1-§3 the idea and its history (the 2026-09-13 brainstorm already
said "pre-generating a small library offline… the cheap version"; the owner's C8 design: sounds as static assets
loaded once, triggered on the page; C11's starred sounds — **cured**: five `*crackle*` in one run of 2026-09-27, none
since, checked); §3 the agent's answer of 2026-09-30 (an offline library, not a live service); §4 the research — the
generated models (**Stable Audio 3 Small-SFX**: 2026-05-20, 459M+108M, 44.1 kHz stereo, 8 steps, gated Community
License, 3.49 GB; **MOSS-SoundEffect v2.0**: 2026-05-26, 1.3B, 48 kHz, Apache 2.0, 11.23 GB; Woosh, TangoFlux,
MMAudio, AudioGen, AudioLDM 2, Stable Audio Open) and the recorded libraries (**Freesound** per-sound CC0/CC-BY/CC-BY-NC;
FSD50K; Sonniss; BBC RemArc; Pixabay; the Internet Archive) — the licence decides where a clip may live (the fork is
public: only CC0 and CC-BY may be committed); §5 how sounds fit the show; §6 the three-source listening test (set
aside); **§8 the narrowing and the plan**.

**The static bed — the owner's design (§8.8, verbatim there):** 5-15 clips of radio static at very low volume, random
order, reshuffled at the end of the list; the level moving with the show (the cast talking / between rounds); random
silences; every number in the fork's settings; silent while push-to-talk is held, perhaps off for the contact. **The
term:** "the static bed" (adopted by the owner: "we adopt the bed term based on your assessments").

**The agent's refinements (§8.8):** clips of **20-240 s** (not 1-15 s); fades or a 1-2 s crossfade at joins and
silences; no repeat across the reshuffle's seam; one loudness (RMS −20 dBFS, peak −1 dBFS); **three states** — under a
voice (low), between rounds (higher), listening (silent) — with a ramp; random silences with a how-often and a
how-long range. **Settings draft:** `bed`, `bed_volume_voice` (0.05), `bed_volume_between` (0.15), `bed_ramp_s`
(0.5), `bed_crossfade_s` (1.5), `bed_silence_every_s` ([30, 120]), `bed_silence_s` ([3, 15]), `bed_off_in_contact`
(false) — guesses to tune by ear.

**The folder tree (§8.3, agreed):** `zombie-radio-datasets/sounds/<source>/<kind>/<id>-<slug>.<ext>` + `.json`
(source, id, page, name, author, licence + class + credit line, preview or original, length, rate, channels, SHA-256,
tags, our kind/verdict/notes); pages of players in `sounds/pages/`; **a pool** (raw) and **a chosen set** made by a
tool (like `cast_voices.py`: a decision file, trimming, loudness, OGG/Opus); the chosen set stored by licence.

**The next step (§8.7):** a small tool `tools/sounds/fetch_freesound.py` (standard library, like `fetch_ears.py`): ids
or a search in; a **dry run** (files, sizes, licences) → the owner's approval → the previews (MP3, key only) and
their `.json` into the tree; a page of players. **Nothing downloaded yet.** Then: the owner's picks (the owner has
their own Freesound radio finds — ids or links to come) → the shape in the fork (discussion first) → build → listen
→ later, sounds per event (a list per event, many or none) and generated sounds for what Freesound lacks.

**Freesound facts (§8.6):** search by text with `filter=license:"Creative Commons 0" duration:[a TO b]`,
`sort=rating_desc`; previews `previews["preview-hq-mp3"]` need no OAuth; originals need OAuth2 (the owner's account);
limits 60/min, 2,000/day. The nine CC0 candidates of 1-15 s (ids 675937, 717474, 436121 static; 369964, 528272, 629301
receiver; 717560, 451068, 724115 sirens) — too short for a bed; the bed's search: 20-240 s.

**Still open, the owner's:** where the bed plays (the agent suggests the looks only, the plain page silent); the
looks' gauge (`static/show/gauge.js` taps every sound — keep the bed out, or let it move the needle); where the chosen
clips live. **The mixing idea:** ducking by events — the page knows when each voice clip starts and ends (`playClip`
in `static/show/player.js`) — gain ramps on a `GainNode`, no compressor, no second stream from the server.

## §6. Tasks and challenges of the arc (the board, from the TODO's "Now")

1. **Goal 4, the 3090** — the NVIDIA driver check first (owner action queue, item 3, now due), then a deployment proven
   from zero and `changed=0`; how the laptop reaches it (LAN or tunnel) to decide. The 32k context may need an override
   in `99-local.yml` if it does not fit (the stack measured 14,477 MiB on the A6000).
2. **Names-only A** — code tells the model which earlier caller a voice is (the follow-up "A listener memory keyed by
   identity"; ~1.5-3 h).
3. **The static bed** (§5).
4. **Task 7, the canned episode** — a MUST; record with `show.debug` on and re-say bad lines with
   `replay_chunk.py --seed N`; with the demo-day runbook; re-examine the compressed reference clips (venue uplink).
5. **Task 9, prepare the talk** — slides and script, the owner's content; what to highlight in
   [discussion 2026-09-30] demo-goals §1, §3, §6.
6. **Task 8, the close ritual.**
7. **The owner's decisions due:** keep or destroy the Hyperstack box; demo-day logistics (owner action queue, items
   4-5).
8. **After the demo:** the recasts; Task 5 (experiments) and the character bibles; the judge in the loop; the two new
   follow-ups; live SFX; the sounds per event.

## §7. Facts and numbers worth keeping

- **Memory (A6000):** 16k: llama 6,764 MiB (model file 6,223), tts 6,530, whisper 888, total 14,195; 32k: total
  14,401 at start, **14,477** through full drives (llama 7,046). Under the 16 GB wish; the 3090's 24 GB fine.
- **The budget arithmetic:** 0.9 × 34,000 + 1,000 + 512 = 32,112 ≤ 32,768. The largest share in 82 runs: 741 tokens
  (an exchange; before the fix, post-Repair rounds were missing); with the fix: 688. For a 16,384 context, a budget of
  about 16,500 fits.
- **Trims:** 16k/14,000: every 22-36 rounds, ~5 s pause; 32k/34,000: the first near round 115-140, then ~every 100
  rounds (est.), **8.2-8.4 s** pause (12-14k tokens re-read).
- **Run ids (the fork's `runs/`, gitignored):** 2026-10-01: `12-54-40` (190 rounds, budget 31,000, trim r114),
  `13-43-41` (220, 34,000, trim r140), `14-05-43` (the survey's raw round), `14-21-40` (the checkpoint, 1,500 —
  the runbook's example), `17-48-37` (270, the fix, trims r115/r246, landed 16,608/16,722), `17-57-41` (8,000 before
  the fix, 130 rounds — the tunnel dropped), `18-03-25` (8,000 after, 12 trims). 2026-09-30: `18-51-36` (the debug
  live check), `19-08-07` (debug, seed off — Daniel's "It's watching us"), `19-20-04` (seed on — Daniel's "determined"),
  `19-32-32` (debug and seed off — the demo's configuration).
- **Tests (the fork at `tz-0.5`):** pytest **1210**; Node `test_show_page.js` 42, `test_persona_form.js` 17,
  `test_tts_settings.js` 91, `test_show_gauge.js` 8.
- **Tags:** `tz-0.4` on `1b7e70e`; `tz-0.5` on `9b3a329`. **PRs merged today:** fork #9; zombie-radio #20, #21 (and
  yesterday fork #8, zombie-radio #18, #19).
- **The laptop:** Apple M1 Pro, 16 GB (Stable Audio 3 Small-SFX can run on it without a GPU).
- **Hugging Face sizes (measured 2026-10-01):** stable-audio-3-small-sfx 3.49 GB (gated "auto"), -medium 10.45 GB,
  MOSS-SoundEffect-v2.0 11.23 GB (not gated).

## §8. Nuances (hard to get from the docs alone)

- The owner reads what the agent writes closely and catches inconsistencies (a guessed time, a wrong range "541 to
  4,159" → 641 to 4,218, a report line cut at 200 characters that hid 87 items); show the numbers' arithmetic.
- The owner likes measured before/after comparisons (the 8k before/after drive was the owner's idea: "re-deploy
  temporarily with a much smaller context… observe many trims") — note: the trim works against the app's budget, so a
  smaller **budget** in settings did it without a redeploy.
- The owner wants to understand mechanisms in depth and asks "how does X actually work" — answer with the code's path
  and a worked example from a real run.
- The owner pushes back on scope and on hidden complexity, and welcomes pushback in return ("This is the time to bring
  all the pushback and also to be creative").
- The owner reviews in VS Code and orders commits explicitly; "commit and push both" covers both repos.
- The owner did their own online research (SFX models) and pasted it — check every claim at the source and say which
  disagree (MOSS v1 8B vs v2.0 1.3B; "July" vs 2026-05-26).
- Doc placement the owner prefers: a reference that ships with code → the fork's runbook; the story of a decision →
  a zombie-radio discussion; both linked.
- The dev server and the installed client are different clones; temporary dev settings are always backed up and
  restored with `cmp`.
- The owner keeps the box up during working sessions; "the VM a little bit longer".

## §9. Mistakes this stretch (do not repeat)

- A measurement that echoed its own estimate (the first landing script) — count independently (the server's
  `/tokenize`).
- A range typed wrong in two docs (541/4,159) — recompute numbers from the data before writing them.
- A report line cut at 200 characters, hiding most of its items — never truncate output you are reporting on.
- Explanations too tangled for the owner — the simple version first.
- An environment variable "in the terminal I'll run the scripts in" — the agent's shell is its own.
- A guessed time in a doc ("19:47") — check the clock or say "the evening".
- An assumed budget (14,000) for runs that used 1,500 — read the run's settings before computing targets.
- A seed design built per chunk before asking whether one per run would do — ask the simplest shape first.
- A running dev server with stale code after a change of the start reply's type (a string "off" read as true by the
  page) — restart the server after any change of the API's shape.

## §10. Techniques

- **The fork's tests:** `.venv/bin/python -m pytest -p no:cacheprovider -o addopts="" -q > <scratchpad>/x.log 2>&1;
  grep -E 'passed|failed' …` (`addopts = -q` in `pytest.ini` hides the summary without `-o addopts=""`); Node
  `node tests/<file>.js | grep -E 'ℹ (pass|fail) '`; remove `__pycache__` after.
- **The dev server:** from the fork's root, `nohup .venv/bin/python .venv/bin/uvicorn app.main:app --host 127.0.0.1
  --port 8010 > <scratchpad>/devserver-<name>.log 2>&1 & disown`; stop with
  `kill $(lsof -nP -iTCP:8010 -sTCP:LISTEN -t)`; the settings are read at start.
- **A long drive** (`<scratchpad>/drive8k.sh` holds a 280-round drive with 42 listener answers): run in the
  background; a notification arrives when it ends.
- **The trim's landing per trim:** `<scratchpad>/trim_landing.py <runs dir> <run-id> <budget>` (counts each
  instruction with the server's `/tokenize`).
- **A run's chunks against its script:** `<scratchpad>/check_run.py <run-id> [server log]`.
- **Freesound:** `<scratchpad>/fs_candidates.py` (a search with the key in a header, preview sizes by HEAD);
  `<scratchpad>/fs-picks.json` (the nine candidates).
- **zsh:** `=====` in `echo` breaks (equals expansion); variables do not word-split; quote URLs with `?`.
- **Python's YAML:** the system `python3` has no PyYAML — use the fork's `.venv/bin/python` (or `uv run`).
- **Hugging Face listings without downloading:** `curl -s "https://huggingface.co/api/models/<id>?blobs=true"`
  (sizes per file, `gated`, `cardData.license`).

## §11. Reading order after the compaction

1. This document, in full.
2. `git status -sb` and `git log --oneline -3` in both repos; `gh pr list` in both (none open expected; the branch
   `alfre2v/sound-effects` committed, not pushed).
3. `docs/discussions/2026-10-01-sound-effects.md` — §8.8, §8.3, §8.7, then the rest of §8, then §1-§6 as needed.
4. `docs/TODO.md` "Now".
5. `docs/discussions/2026-10-01-the-app-from-the-outside.md` §2 (the trim) and §3-§4 (the endpoints) if the work touches
   the show's internals.
6. Then report: the clock, the tunnel (probe first), the branch, the static bed's next step — and ask what to do next.
   Wait for the go.

## §12. Paste-ready prompt

```
We continue the Zombie-Radio work of 2026-10-01 after a compaction. Today we released tz-0.5 (the 32k context, the
trim's numbers as settings and its flaw fixed, a start check against the server's context), wrote three discussions
(judge-in-the-loop, the-app-from-the-outside, sound-effects), and narrowed the sound effects to "the static bed":
radio static played low under the show from a shuffled list of Freesound clips, mixed with the voices. Re-orient
before doing anything else:

1. Read docs/discussions/2026-10-01-show-engine-session-handoff-9.md IN FULL — §0 and §0.1 are binding (how we work;
   the box, the laptop, the secrets), then the exact state (§2), what happened (§3), the systems (§4), the static bed
   (§5), the board (§6), facts (§7), nuances and mistakes (§8-§9), techniques (§10).
2. Follow its reading order (§11): both repos' status, the sound-effects discussion's §8 (§8.8 first), the TODO's
   "Now".
3. Then give me a compact summary — the clock, the tunnel (probe it first), the branch alfre2v/sound-effects, the
   static bed's next step (the Freesound fetch tool, dry run first) — and ask what to do next. Wait for my go.

Standing rules: strict review-before-commit (I review in VS Code — no diffs in chat, no commit without my explicit
order), push only when told, no AI attribution anywhere, discussion-first and smallest step first, explain simply
and explicatively, plans executable step by step, docs as detailed as the chat with my words verbatim, never print
or commit secrets (the Freesound key file), never invent data, IP scans on the staged diff only, never stage
hosts.yml, scratch files only in the scratchpad.
```

## §13. The owner's words of this stretch (verbatim)

- On the voices: "as far as I am concerned we have achieved TTS of voices with emotions with great success." · "I can
  live with the audio instabilities for the moment. I wan to make progress in other areas."
- On the seed: "on/off with the run's seed, go ahead."
- On the trim's flaw: "this is the one that worries me the most... it makes the show forget more lines that we
  intended." · "if only we trigger the trim in the right round we may be able to avoid all this complexity. No?"
- On explanations: "Be explicative be default, remember? Stop saving tokens in places where it degrades my
  understanding."
- On documents: "when a discussion becomes very interesting we sometimes update it to make them less a log and more a
  linear story".
- On SFX: "I am getting a bit greedy here… What if... We add a new AI component just for the SFX" · "This is a too
  ambitious plan to advance in so many fronts at the same time" · "we can play a list of audio files related to radio
  static and radio sounds in the background" · "we adopt the bed term based on your assessments".
- On the box: "I am keeping the VM a little bit longer, we are not done for the day."
