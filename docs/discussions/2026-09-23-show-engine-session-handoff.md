# Session handoff — from the 2026-09-23 design session to the show engine's build

> **EPHEMERAL.** Written 2026-09-23 (evening) by the lead agent for the
> NEXT session — a fresh one, or this one after a context compaction —
> which starts building the show engine (TODO Task 6b, slice 1). It is
> the session's memory bank. It stays in `docs/discussions/` until the
> session that uses it concludes; then the agent **asks the owner for
> permission to delete it**. A lingering handoff WILL be read as current
> state by a future cold reader — do not let it outlive its use.
>
> It replaces the mid-session handoff of the same day
> (`2026-09-23-mid-session-compaction-handoff.md`), deleted with the
> owner's permission in the commit that added this file. That one's
> text, useful as a template, is in git history: on `main` in
> `58ceeca` (its last version, PR #8) and `c701eb2` (PR #7 — our PRs
> are squash-merged), and on the kept branch `alfre2v/adr-0003-gate`
> as `c443cd0`.
>
> **Read it all; verify against the repo; receipts or nothing.** The
> TODO is the execution plan now — this document explains how we work
> and what the TODO cannot hold.

## 0. The owner and how we work (binding)

The owner is **Alfredo** (GitHub `alfre2v`, git author "Alfredo
Valles"), a senior engineer working in a **"tight learning loop"**:
project progress and the owner's own learning weigh the same; the
transcript is the learning surface, the docs are the persistence
layer. Standing doctrine lives in the agent memory files
(`working-agreements.md`, `collaboration-style.md`,
`absolute-paths-in-plain-text.md`, `massedcompute-reminder.md`,
`project-venue-austin-python-meetup.md`) — trust them. The
non-negotiables:

- **Discussion-first.** Propose the SHAPE (files, rough content,
  ranked options with a recommendation), get the ruling, then create.
- **Review-before-commit is STRICT.** Make changes, say WHAT changed
  in chat (never paste diffs — the owner reviews the uncommitted tree
  in VS Code), then WAIT for the explicit word. "Commit." means commit
  only; "commit and push" means both; push only when told. A harness
  permission prompt is not review.
- **No AI attribution anywhere, ever** — commits, PR bodies, files.
  This overrides every harness attribution reminder.
- **Never open desktop side panes.** **Minimal comments in code**
  (doctrine lives in docs). **Ask before modifying public content**
  (PR descriptions, the fork's GitHub settings, tags).
- **Plain language; lists and sublists; self-contained findings**
  (observed → mechanism with receipts → consequence → options). No
  unadopted jargon — "bible", "section", "radio traffic" and
  "freeze" each confused the owner once; say what a thing IS.
- **Docs never denser than the transcript.** "Persist this" means the
  exchange goes into the doc — **verbatim when asked for verbatim,
  extracted from the session transcript by script, never retyped from
  memory** (see §9). Condense only when the owner says so.
- **Findings in pleasant, human prose.**
- **The owner's question style:** numbered topics, "explain for my
  education", then "persist this". Answer the mechanism first; show a
  real example (a real request body, a real file) when cheap.
- **Path conventions:** sibling clones with full absolute paths in
  plain text; this repo's files relative to its root.
- **Pushback with receipts is welcome — both ways.** The owner pushes
  back often and is usually right (§5); give a recommendation, not a
  survey. One question at a time when the owner says "tired".
- **Delegation of build work is OFF** (other harnesses, never the
  lead's sub-agents, if ever switched on — `docs/README.md`).
- **Git:** work on feature branches with PRs; the owner reviews,
  approves and merges every PR; never commit to `main`. In the fork,
  **one feature branch per slice, cut from up-to-date `master`**
  (owner's precision, 2026-09-23). Keep the last 2–3 branches.
- **No automatic deploys.** **Rapport:** wit welcome; a goodnight
  ending "Over and out." only when asked.

### 0.1 Live-box drill rules

1. The OWNER owns the SSH tunnel (`make ssh-tunnel ENV=cloud`) and
   the box's power (wake, hibernate). The agent never starts either;
   it reaches the services only through the laptop's
   `localhost:8080` (llama.cpp), `:8001` (tts-serve), `:8002`
   (Whisper).
2. Box inspection: plain `ssh ubuntu@<box> '<cmd>'` — no key paths,
   no extra `-o` options; never list or cat under the owner's SSH
   directory. The owner supplies the address; it is written nowhere
   in markdown.
3. One line saying what a command does and why, BEFORE running it;
   outputs to the scratchpad.
4. Nothing on the box changes outside the playbook; no destructive
   command without asking; a failed check means stop and think.
5. **The box address never appears in any markdown file** (the
   never-commit hook skips `*.md`): grep `docs/` for it before every
   commit.
6. **Probe the tunnel before a chain of requests** (`curl -s -m 3
   -o /dev/null -w '%{http_code}' localhost:8002/docs`); on `000`,
   STOP and tell the owner — it drops often (library Wi-Fi, laptop
   lid).

## 1. The project in 60 seconds

**Zombie-Radio**: an interactive, audio-only radio play — four AI
scientists trapped in a lab during a zombie outbreak, broadcasting on
shortwave; listeners talk back with hold-to-talk. **Hard deadline
2026-10-08;** it will be presented in a **talk at the Austin Python
Meetup in October 2026.** "hackTNT 2026" (the folder name) is the
owner's internal name for 2026 projects — **there is no hackathon.**

Architecture: the app runs on the owner's Mac (M1, 16 GB); a rented
Hyperstack A6000 box hosts only the model services behind the SSH
tunnel — llama.cpp (Nemotron Nano 9B v2 Q4_K_M, 16k context, one
slot), tts-serve 1.2 (engine Faster Qwen3-TTS, a systemd unit named
`tts-faster_qwen3tts`), whisper-fastapi (small). The app is
**TalkWithZombies**, our fork of scorbo2's TalkWithMe 7.1
([ADR-0002]); its show engine ([ADR-0003]) is being built now, as
designed in [discussion 2026-09-23] show-engine-design.

## 2. Exact state (2026-09-23, ~20:00 CDT)

- **zombie-radio:** `main` at `58ceeca` (PR #8 merged). **PR #9 open**
  (https://github.com/alfre2v/zombie-radio/pull/9) from
  `alfre2v/show-engine`: the design discussion, the lessons addendum
  §5, the TODO as execution plan, follow-ups, the roadmap's announcer,
  a story-loop note — plus the commit that adds THIS handoff (if the
  owner has committed it). Merged PRs so far: #1–#8.
- **The fork:** `alfre2v/TalkWithZombies` (public; parent
  scorbo2/TalkWithMe; `master` only). `master` at `1d41bab` (PR #1
  merged: provenance, house rules, `CLAUDE.md` → `@AGENTS.md`, the
  `audio/webm` pin). Tags: `7.1` (the fork point, `93df6ca`) and
  `tz-0.1` (on `1d41bab`). Clone:
  `/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`, on
  `master`, clean; remotes `origin` (the fork) and `upstream`
  (scorbo2, fetch only — push URL `NO_PUSH_TO_UPSTREAM`); its own
  `.venv` on Python 3.12.14 with the dev requirements. **No slice
  branch exists yet.**
- **Installed clients on the Mac:** `~/TalkWithZombies-client` (the
  fork at `tz-0.1`, installed by `make client-mac`, memories off);
  `~/TalkWithMe-client` (TalkWithMe 7.1, the fallback). The owner
  sometimes runs the reference clone
  `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe` on port 8000 —
  use another port (8010) for test boots.
- **The box:** HIBERNATED by the owner on 2026-09-23 evening (its IP
  kept). Waking is a cold boot; all three services rise on their own;
  the TTS warms up on first use. `hosts.yml` is UNWIRED
  (`ansible_host: REPLACE_ME_box_ip`); the owner re-wires with
  `make ans-set ENV=cloud IP=…` and starts the tunnel. The box is
  needed first at step **1.9** (ten rounds on the box).
- **The timebox:** started 2026-09-23 **14:46 CDT** (the fork's
  creation, owner's ruling) · checkpoint **2026-09-25 02:46** (in
  practice that morning) · end **2026-09-26 14:46**.
- **Scratchpad of this session:**
  `/private/tmp/claude-501/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18/scratchpad/`
  (logs, the verbatim extractions, the old TODO copy). The session
  transcript:
  `/Users/alfredo/.claude/projects/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18.jsonl`.
- **Agent memory** gained `project-venue-austin-python-meetup.md`.

## 3. What this session did (2026-09-23, with receipts)

**Before the compaction (morning–afternoon):** the gate's paperwork —
findings in prose, the lessons discussion and its addendum §4, ADR-0003
accepted, TODO/journal/follow-ups, a deep parity pass over spec,
roadmap and follow-ups, the delegation method recorded as not in use,
the mid-session handoff. PR #7 merged.

**After the compaction:**

1. **The box woken; "Luna hangs" diagnosed.** TalkWithMe's stock
   personas (Alex, Luna) and its "LLM decides" router have no
   `/no_think`: Nemotron spent the whole budget thinking (Luna 200 of
   200 tokens, the router 16 of 16), `content` came back empty, and the
   router fell back to `random.choice`. The box was healthy.
   Hibernation = a cold boot with the disk kept.
2. **The fork (Task 6a):** created with `gh repo fork … --fork-name
   TalkWithZombies --default-branch-only --clone=false` from the
   scratchpad (`--remote` is refused with a repository argument);
   upstream's `7.1` tag pushed (a master-only fork copies no tags);
   cloned. PR alfre2v/TalkWithZombies#1: README provenance, house
   rules, `CLAUDE.md`, and the `audio/webm` pin (newer Pythons map it
   to `.weba`; our Whisper ignores the name — tested live; OpenAI's
   API would reject `weba`) → suite 781/781. Tag `tz-0.1`.
3. **PR #8 (zombie-radio):** the installer installs the fork at
   `tz-0.1` into `~/TalkWithZombies-client` (fresh `changed=8` in
   21 s, re-run `changed=0`, HTTP 200, the four cast personas);
   `docs/README.md` "Where things live"; README status; the
   **framing correction** (a talk, not a hackathon). The clock start
   recorded.
4. **The show engine's seven decisions** — see §5 and
   [discussion 2026-09-23] show-engine-design (every exchange
   verbatim, each with build notes). Along the way: the emotion field
   ruled on; `/apply-template` verified; the Whisper server's fields
   verified; the announcer parked in the roadmap.
5. **The TODO reorganized** as the execution plan: "Now" on top;
   Task 6b as an ordered checklist by slice with done-when checks;
   done work moved whole under "Done in this arc".
6. **PR #9 opened** (the design branch, 7 commits), then this handoff.

## 4. Facts and numbers worth remembering (all checked 2026-09-23)

- **GPU memory on the box:** 13.0 of 46 GB used — llama.cpp 6.8 GB,
  TTS 5.3 GB, Whisper 0.9 GB. The model file declares a trained
  context of 1,048,576 tokens; the server runs 16,384.
- **`/apply-template`** exists on build `b11096`: ~120 ms, no
  generation, no slot; its output matches the lessons' §4.9
  reconstruction (`/no_think` removed, `<SPECIAL_1x>` markers,
  `<think></think>` at the end; earlier assistant turns rendered
  plainly).
- **Prompt reading speed:** a 687-token prompt at 0.61 ms per token
  (the llama log). The script grows ~125 tokens per round (the gate).
- **Whisper (`/v1/audio/transcriptions`) accepts:** `file, prompt,
  response_format, task, language, vad_filter, vad_threshold,
  vad_neg_threshold, vad_min_speech_duration_ms,
  vad_max_speech_duration_s, vad_min_silence_duration_ms,
  vad_speech_pad_ms, repetition_penalty, gpt_refine` — `prompt` yes,
  `initial_prompt`/`hotwords` no. With `prompt` set, the reply
  reports it as `initial_prompt`; `language=en` lifted certainty
  0.795 → 1; `vad_filter=true` kept 3.144 s of 4.44 s as speech.
  Replies carry per-segment `no_speech_prob` and `avg_logprob`.
- **tts-serve's capabilities** (faster-qwen3-tts): `text`,
  `audio_base64`, `reference_text`, `language`, `seed`,
  `temperature`, `top_p`, `repetition_penalty` — **no emotion or
  style input**; delivery comes from the reference clip.
- **The fork's code seams** (at `tz-0.1`, same lines as 7.1):
  `build_llm_messages` `app/session.py:123`; `_base_payload`
  `app/services/llm.py:69`; `_chat_stream` `app/routers/chat.py:208`;
  the SSE reader `static/chat.js:135-159`; the STT placeholder
  `app/services/stt_client.py:85`; `/api/stt` `app/routers/stt.py:30`;
  Jinja2Templates `app/main.py:148` (`jinja2==3.1.6` pinned).
- **The 2024 prototype:** one prompt with the characters enumerated
  (`/Users/alfredo/workspace/hackTNT_2026/zombie_radio_ai/zradio_local/zradio_local.py:511-539`,
  records at 470–509); a `Narrator:`-labelled directive (line 657);
  a random character answered the listener; "over and out" closed
  listening.

## 5. Rulings of this session (after the compaction)

- Plain SSH to the box; the owner hibernates and wakes it.
- The fork: master only, `7.1` tag pushed, `tz-` tags for our own
  versions (`tz-0.1` now, `tz-0.2` after slice 3); the audio/webm
  **pin** kept over loosening the tests (OpenAI's allow-list).
- The installer points at the fork; the old client stays as the
  fallback; the playbook's filename kept.
- The clock started at the fork's creation, 14:46 (the rule as first
  agreed).
- **The emotion field:** a yaml switch, default ON.
- **Decision 2:** the midpoint trim (90 % → 50 % of
  `show.context_budget`, whole rounds) — the owner's pushback against
  "it fits, no trim"; minimal episodes only after it works (the
  owner warned they may be harder than estimated).
- **Decision 3:** one show decoupled from the chat rooms (the owner's
  pushback against "per room"); a folder per run; the trim as a flag.
- **Decision 4:** the cast sheet as a Jinja template with visible
  placeholders (the owner asked for them), `stories/<story>/` with
  episodes (the owner raised multiplicity), `runs/` renamed, the cast
  in the story.
- **Decision 5:** no label on the instruction (the owner's
  preference); "Offstage:" for events (the owner caught that "radio
  traffic" sounded spoken); the addressed character answers (the
  owner's pushback against a single operator); three separate timers
  (the owner asked how listening extends — hold-to-talk answers it).
- **Decision 6:** the transcript filter; the cast names as Whisper's
  `prompt` (the owner asked for the check on the box); `language=en`,
  `vad_filter=true`; "Heard:" only in debug; **the owner's radio
  gauge** on the polish list.
- **Decisions 1 and 7:** skeleton first in three slices; the
  `app/show/` layout; one feature branch per slice from `master`.
- **The TODO** is the execution plan; the design doc is DECIDED and
  append-only.

## 6. The board ahead (canonical: `docs/TODO.md`, "Now" and Task 6b)

1. **PR #9** — the owner reviews and merges (the design and this
   handoff).
2. **Cut `alfre2v/show-slice-1-skeleton`** from the fork's up-to-date
   `master` (`git -C …/TalkWithZombies switch master && git pull
   --ff-only && git switch -c alfre2v/show-slice-1-skeleton`).
3. **Slice 1, steps 1.1 → 1.9** (target end of 2026-09-24): settings
   → story → grammar → parser → record and assembler → director v0 →
   the grammar key → endpoints → the driver and ten rounds on the box
   (the owner wakes the box and starts the tunnel for 1.9). Each step:
   discussion-first where a shape is open, tests green, the owner's
   review, a commit, the TODO ticked with the hash.
4. **Slice 2** (2.1–2.5) by the checkpoint; **the checkpoint verdict**
   recorded in the TODO; **slice 3** (3.1–3.6); polish only if green.
5. After the timebox: Tasks 5a/5b/5c (5a needs the owner's bibles, 5b
   the voice samples), Task 7 (the canned episode, a MUST), Task 8.
6. **Owner-side:** Task 4 (bibles → the cast entries of
   `stories/lab-outbreak/cast_sheet.md`; voice samples, never
   committed); the MassedCompute reminder after experiment PRs.

## 7. Risks

- **Time:** slice 1 is nine steps in one day; the checkpoint judges
  slices 1 and 2 together. The scale-down order is written in the
  TODO — use it early rather than late.
- **The tunnel drops** often; box steps (1.9, 2.2's pause, the
  checkpoint) need the owner present.
- **Identity bleed** (one voice taking over) — the director's
  silent-longest rule is the first defense.
- **Whisper on names** (challenge C6) — the model-decides answer rule
  and the `prompt` hint mitigate; unproven on hard names.
- **The trim's pause** on the hybrid model is unmeasured (2.2 measures
  it).

## 8. Nuances the docs alone won't give you

- **The owner reads jargon literally.** When a term from an ADR or a
  discussion confuses, explain what the thing IS with a real example
  (the 2024 prompt; run 2's cast sheet; a real request body).
- **Reuse arguments are suspect.** Twice today a TalkWithMe-era reuse
  argument (the room as the show's home; the persona files as the
  cast sheet) did not survive the new design. Check whether a reuse
  still fits before proposing it.
- **"Persist" means the doc gets the exchange** — the pattern in
  show-engine-design: the owner's messages quoted, the agent's answers
  with headings demoted, the ruling quoted, then authored build notes.
  Extract by script from the transcript (§10).
- **The owner likes live checks** when the box is up ("the VM is
  there wasting money for you to test things") — run the cheap check
  rather than hedging.
- **Experiment folders' findings** still say "awaiting the owner's
  review"; ask whether to mark them sealed at a natural moment (the
  close ritual).
- **Pronouns:** older docs call the owner "he"; new writing avoids
  pronouns for the owner.

## 9. My mistakes this session (do not repeat)

- **Wrote a "verbatim" section from memory** (lessons §5.3's first
  draft) — caught and replaced from the transcript. Verbatim = extract
  by script, then verify by script.
- **Stated times and counts unchecked:** the fork's creation "13:55"
  (it was 14:46); "8 commits" (it was 7). Look it up before saying it.
- **`git rev-parse --short A B`** fails (one revision only) — twice.
- **Chained requests after a failed tunnel probe** — the probe printed
  `000` and the script went on to throw tracebacks. Stop at `000`.
- **Read a pipe's exit code as grep's** (`grep … | head; echo $?`).
- **A reassembly script cut a two-line heading**, leaving a stray line
  — caught by reading the joins. Read the joins after any scripted
  restructure.
- **Proposed per-room records and persona-file cast sheets** — both
  reversed by the owner (§8).

## 10. Operational gotchas

- **zsh:** quote globs; `echo =====` fails; no `PIPESTATUS`.
  Foreground `sleep` is blocked.
- **Verbatim extraction:** the transcript is JSONL at the path in §2;
  each record's `message.role` and `message.content[].text`; pick the
  LAST block containing a distinctive phrase; a message split around
  tool calls is several blocks; some bridging text may be missing —
  note it rather than retype it.
- **The fork's tests:** `.venv/bin/python -m pytest -p
  no:cacheprovider` (`.pytest_cache` is not gitignored); `node
  tests/test_persona_form.js` and `node tests/test_tts_settings.js`;
  a clean run shows one Starlette deprecation warning.
- **Fork PRs:** `gh pr create --repo alfre2v/TalkWithZombies --base
  master --head <branch>` — never let `gh` pick the parent repo.
  Never push tags with `--tags` (upstream's tags are not wanted
  there).
- **The box:** `docker ps` shows only `llama` and `whisper`; the TTS
  is the systemd unit `tts-faster_qwen3tts`
  (`journalctl -u tts-faster_qwen3tts`). `docker logs llama` carries
  earlier runs' lines — task ids restart at 0 per server start.
- **Installer:** `make client-mac` (no ENV); test boots of an
  installed client on port 8010, then stop it.
- **Ansible:** `make ans-lint` (profile `production`); `make ans-set
  ENV=cloud IP=…` / `make ans-unset ENV=cloud` are the owner's.
- **Pre-commit ritual:** grep `docs/` for the box address; a
  key-like-strings scan on the diff; stage by explicit path (never
  `hosts.yml`).

## 11. Reading order for the next session

1. This document, in full.
2. `git log --oneline -10` in both repositories; `git status`; is PR
   #9 merged (`gh pr view 9`)?
3. `docs/TODO.md` — "Now", the owner action queue, and Task 6b's
   checklist.
4. [discussion 2026-09-23] show-engine-design — §7.3 (the slices),
   then the build notes of the decisions the next step touches
   (§2.4, §3.4, §4.5, §5.7, §6.7).
5. As needed: [ADR-0003]; [discussion 2026-09-22]
   grammar-and-prompt-cache-lessons §4.6–§4.9 and §5; the fork's
   `AGENTS.md` (upstream's testing rules).

## 12. Paste-ready prompt for the next session

```
We continue the Zombie-Radio MVP-prototype arc with the show engine's
build (TODO Task 6b, slice 1). Re-orient before doing anything else:

1. Read docs/discussions/2026-09-23-show-engine-session-handoff.md IN
   FULL — how we work (§0 is binding, including the live-box drill
   rules), the exact state (§2), what the last session did (§3), the
   facts (§4), the rulings (§5), the board ahead (§6), the nuances and
   your predecessor's mistakes (§8–§9), and the gotchas (§10).
2. Follow its reading order (§11) as far as needed to confirm the
   state: at minimum git log and status in both repositories, whether
   PR #9 is merged, and docs/TODO.md's "Now" and Task 6b checklist.
3. Then give me a compact summary: where the timebox stands (the
   clock), what is pending on my side, and the next step you propose
   (cutting the slice-1 branch, then step 1.1) with the shape of 1.1
   — and wait for my go.

Standing rules: strict review-before-commit (I review uncommitted
changes in VS Code — no diffs in chat, no commits without my explicit
word), no AI attribution anywhere, no side panes, minimal code
comments, discussion-first, pushback with receipts welcome, plain
language, no delegation to other agents for now, and one question at
a time when I say I am tired.
```
