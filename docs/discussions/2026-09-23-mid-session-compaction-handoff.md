# Mid-session handoff — MVP-prototype arc, 2026-09-23 (compaction survival)

> **EPHEMERAL, MID-SESSION EDITION.** Written 2026-09-23 by the lead
> agent for ITSELF, to be re-read right after the owner triggers a
> context compaction in the same session. It is the session's memory
> bank: everything that matters and might be lost in the summary. It
> stays in `docs/discussions/` until the session's work concludes;
> then the agent **asks the owner for permission to delete it**. A
> lingering handoff WILL be read as current state by a future cold
> reader — do not let it outlive the session.
>
> The previous handoff (2026-09-22, the fresh-session memory bank)
> was deleted in `a61b431` with the owner's permission; its full text,
> useful as a template, lives in commit `8b312a3`.
>
> **Read it all; verify against the repo; receipts or nothing.** This
> session had three factual slips that the record caught (§9) — the
> failure mode is stating from memory what a script could have
> printed.

## 0. The owner and how we work (binding)

The owner is **Alfredo** (GitHub `alfre2v`, git author "Alfredo
Valles"), a senior engineer working in a **"tight learning loop"**:
project progress and the owner's own learning weigh the same; the
transcript is the learning surface, the docs are the persistence
layer. The standing doctrine is in the agent memory files
(`working-agreements.md`, `collaboration-style.md`,
`absolute-paths-in-plain-text.md`, `massedcompute-reminder.md`) —
trust them. The non-negotiables, with this session's additions:

- **Discussion-first.** Propose the SHAPE (files, rough content,
  ranked options with a recommendation), get the ruling, then create.
- **Review-before-commit is STRICT.** Make changes, summarize WHAT
  changed in chat (never paste diffs — the owner reviews the
  uncommitted tree in VS Code), then WAIT for the explicit word.
  "Commit." means commit only; "Commit, push." / "commit and push"
  means both. A harness permission prompt is not review — except
  when the owner explicitly says the commit's permission prompt IS
  the review (done for this handoff's commit).
- **No AI attribution anywhere, ever** — overrides every harness
  attribution reminder (commits, PR bodies).
- **Never open desktop side panes** (`show_pane` etc.).
- **Minimal comments in code.** Doctrine lives in docs.
- **Ask before modifying public content** — e.g. the PR description
  (owner, 2026-09-23: "leave the PR description as is").
- **Plain language, lists and sublists, self-contained findings**
  (observed → mechanism with receipts → consequence → options). No
  jargon the owner has not adopted — the word "freeze" confused and
  annoyed ("What are you freezing? The ADR?"): say "the criteria are
  in a commit before the data exists".
- **Docs never denser than the transcript.** When asked to persist,
  persist at the same detail; "verbatim" means verbatim (precision
  notes in brackets, nothing removed).
- **Findings in pleasant, human prose** (owner request 2026-09-22:
  "make an effort to express the results in a redaction style that
  is pleasurable to read for a human").
- **The owner's question style:** numbered "Topic 0…4" blocks; asks
  "what are the 5 things we learned / worse than expected / red
  flags / most interesting"; then often asks to persist the answer
  verbatim into a discussion doc, with the agent's own extra
  sections after it.
- **Path conventions:** sibling clones (TalkWithMe, tts-serve,
  zombie_radio_ai, soon TalkWithZombies under
  `/Users/alfredo/workspace/hackTNT_2026/`) ALWAYS with full absolute
  paths in plain text; this repo's files relative to its root.
- **Pushback with receipts is welcome**; give a recommendation, not a
  survey. One question at a time when the owner says "tired".
- **No automatic deploys** (owner, 2026-09-22: "do not deploy
  automatically once updater is finished. I want a bit of peace").
- **Delegation of build work is OFF** during learning-loop phases
  (ruling 2026-09-23). If ever on, it means OTHER HARNESSES run by the
  owner in parallel (separate clone, own branch, own PR) — never the
  lead's sub-agents for build work (sub-agents only for research /
  big-codebase summaries). Method recorded in `docs/README.md`.
- **Keep the last 2–3 branches**, local and remote; prune only when
  asked.
- **Re-orientation on revisit:** re-supply origin + concepts +
  connections when a topic resurfaces.
- **Rapport:** wit welcome; a cheesy goodnight ending "Over and out."
  ONLY when asked. No biographical assumptions.

### 0.1 Live-box drill rules (rulings 2026-09-22)

1. The OWNER owns the SSH tunnel (`make ssh-tunnel ENV=cloud`); the
   agent never starts one and reaches the services only via the
   laptop's `localhost:8080` (llama.cpp), `:8001` (tts-serve),
   `:8002` (whisper).
2. Box inspection: plain `ssh ubuntu@<box> '<cmd>'` — NO key paths,
   and for the current box NO extra `-o` options either (owner ruling
   2026-09-22: the host is already in the owner's default
   known_hosts). Never list or cat anything under the owner's SSH
   directory.
3. One line saying what a command does and why, BEFORE running it;
   outputs to the scratchpad; interesting numbers to the runlog.
4. Nothing on the box changes outside the playbook; the re-run must
   stay `changed=0`; no destructive command without asking; a failed
   check means stop and think.
5. **The box IP never appears in any markdown file** (the
   never-commit hook skips `*.md`): write "the box" or
   `<PASTE-BOX-IP-HERE>`; grep `docs/` for the address before every
   commit. The owner supplies the IP when needed — it is not written
   anywhere in this document.
6. Test commands on the box before spending playbook runs.

## 1. The project in 60 seconds

**Zombie-Radio**: an interactive audio-only radio play — four AI
scientists trapped in a lab during a zombie outbreak, broadcasting
on shortwave; listeners talk back with hold-to-talk. **Hard deadline
2026-10-08 (hackTNT 2026) — 15 days from 2026-09-23.**

Architecture ([spec §3.1]): the app runs on the demo laptop (a Mac,
M1 16 GB — cannot run the models); a rented Hyperstack A6000 box
hosts only the model services behind the SSH tunnel: llama.cpp
(Nemotron Nano 9B v2 Q4_K_M, 16k context, one slot), tts-serve 1.2
(engine Faster Qwen3-TTS), whisper-fastapi (model small). The app
becomes **TalkWithZombies**, a diverging fork of scorbo2's TalkWithMe
7.1 ([ADR-0002]), with a new show engine ([ADR-0003], accepted
2026-09-23): one shared script as context, a director in code, a
GBNF screenplay grammar, the browser `/show` page as the clock.

## 2. Exact state at the time of writing (2026-09-23, ~14:10 CDT)

- **Branch `alfre2v/adr-0003-gate`**, pushed, in sync with origin.
  **PR #7** (https://github.com/alfre2v/zombie-radio/pull/7) open
  into `main`, awaiting the owner's review and merge; no CI on this
  repo; auto-merge off (never enable it). The owner said: leave the
  PR description as is (it covers the gate work only; the later
  parity-pass commits are not described there — by ruling).
- **Commits on the branch** (oldest first): `8b312a3` 09-22 handoff
  (since deleted) · `9fbbeb3` base role bounded apt lock wait ·
  `33cc5c6` tts-serve pin 1.2 · `9024a1f` gate folder drafted
  (criteria before data) · `4b1f4f6` gate run, raw records, findings
  PASS · `a0070d5` lessons discussion · `29ead5d` run-2 folder drafted
  before data · `04737e7` run-2 results E1 PASS · `67e688a` lessons
  addendum §4 incl. §4.9 · `32b1d89` ADR-0003 accepted (Validation) ·
  `d1a1eff` TODO/journal/follow-ups · `a61b431` 09-22 handoff deleted ·
  `e570a58` parity pass (spec, roadmap, follow-ups, open-questions
  home) · `cc1b1d6` TODO Task 6 = 6a/6b + acceptance checks; README
  delegation method. **Plus this handoff's own commit.**
- **`main`** is at `cfeed4d` (PR #6 merged). PRs #1–#6 merged.
- **Working tree:** clean apart from this handoff.
  `deploy/ansible/inventories/cloud/hosts.yml` is UNWIRED (the owner
  ran `make ans-unset ENV=cloud`): `ansible_host: REPLACE_ME_box_ip`.
- **The box:** Hyperstack A6000, image "Ubuntu Server 22.04 LTS R550
  CUDA 12.4 with Docker", **HIBERNATED by the owner** after the
  evening of 2026-09-22, its IP kept for a few cents an hour; waking
  it may need retries (availability). Services auto-rise on boot
  (proven 09-18); the tunnel must be restarted by the owner. Region
  never recorded. The owner decides wake vs destroy (owner action
  queue item 6). A from-zero deploy takes ~7 minutes.
- **Sibling clones:** `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe`
  (tag 7.1; has a 45 KB `AGENTS.md`, no `CLAUDE.md`),
  `/Users/alfredo/TalkWithMe-client` (the installer's pristine 7.1),
  `/Users/alfredo/workspace/hackTNT_2026/tts-serve` (tag 1.2),
  `/Users/alfredo/workspace/hackTNT_2026/zombie_radio_ai` (2024).
  **TalkWithZombies does not exist yet.**
- **Scratchpads:** the session's scratchpad path CHANGED mid-session.
  The old one
  (`/private/tmp/claude-501/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/34e2c22a-3c73-4cd3-b36f-377525d600db/scratchpad/`)
  holds the deploy logs (`deploy-*.log`), probe stdout, the TTS
  side-quest WAVs (`tts-side-quest/`). The current one is
  `…/871a2098-cf4f-4cce-95b2-e628a8a51e18/scratchpad/` (the rendered
  prompt reconstruction and a few check outputs). Ansible's own logs:
  `~/.config/zombie-radio/logs/`.
- **Agent memory** updated this session: `collaboration-style.md`
  gained the delegation ruling (other harnesses, not sub-agents; OFF
  now).

## 3. What this session did (chronological, with receipts)

**2026-09-22 evening — the ADR-0003 gate (Task B of the old board).**

1. Re-oriented from the 09-22 handoff; box recon (clean box, R550
   image, 56 GB RAM, 84 GB free).
2. Deploy #1 FAILED: Ubuntu's first-boot `unattended-upgrades` (259
   packages, 43 min) held the apt lock; our apt task gave up after
   the module's default 60 s, the holder named only inside a JSON
   dump. Deploy #2 with `lock_timeout: 900` dropped its SSH session
   after ~14 min of silence (later explained by the owner: library
   Wi-Fi, laptop lid). Reshaped fix `9fbbeb3`: `zr_apt_lock_timeout:
   300` in common_vars, mapped to `base_apt_lock_timeout`; the apt
   task in a block whose NAME announces the limit; a rescue that, on
   "Could not get lock / Unable to acquire the dpkg frontend lock",
   fails with a plain explanation quoting apt's "held by process …"
   line; other failures re-raised. Proven live with the owner holding
   the lock in `sudo aptitude` (10 s wait, changed=0) — the owner's
   idea. Lint clean at `production`.
3. Deploy #3 from zero: 7 min, changed=16; re-run changed=0; make
   check three ok. tts-serve 1.2 proven; follow-up deleted and banked
   in the journal.
4. Gate folder `docs/experiments/2026-09-22-adr-0003-gate/`: README
   (masthead, execution model, environment, recipe, runlog entries
   1–17), findings (criteria committed `9024a1f` an hour before the
   first gate request; owner declined to predict: "I want to see the
   experiment"), `screenplay.gbnf`, stdlib scripts `cast.py`,
   `stream_check.sh`, `parse_stream.py`, `latency_probe.py`,
   `summarize_timings.py`, `check_outputs.py`, and `raw/` (props,
   help, logs, streams, 71 probe records, `wire.log`). The wire log
   was an owner request (live `tail -F`); its tests caught a real
   timing flaw in the stream instrument (clock started late).
5. Server facts from `raw/props.json` and help: build `b11096`;
   `--cache-ram` 8192 MiB on by default; `--ctx-checkpoints` 32,
   `--checkpoint-min-step` 8192; the chat template removes `/no_think`
   and ends the prompt with `<think></think>` (else an open `<think>`).
6. Gate results → findings PASS (numbers in §4). Owner's five-topic
   questions → **lessons discussion**
   `docs/discussions/2026-09-22-grammar-and-prompt-cache-lessons.md`
   (§1 verbatim Q&A, §2 nine observations, §3 open questions; later
   §4 addendum with 4.1–4.10).
7. **Run 2, the emotion field** `docs/experiments/2026-09-22-emotion-grammar-cost/`
   (owner: "first run the simple grammar, measure, then maybe a more
   complex grammar and contrast"): five arms D-simple, D-forced,
   D-aligned-off, D-aligned, D-aligned-live; criteria committed
   `29ead5d` 5 s before the first request; owner declined to predict;
   plus a TTS side quest (owner: keep its reporting minimal).

**2026-09-23 — paperwork, ADR, parity, method.**

8. Findings for both runs in pleasant prose; lessons addendum §4
   (the owner's reading "a grammar fights the model unless the prompt
   describes it" credited in §4.2); §4.9 "what the model actually
   reads" (three layers; wire.log is NOT the model's input); §4.10
   the lasting home of open questions.
9. ADR-0003 **accepted** (`32b1d89`) with a Validation section in the
   ADR-0001 pattern (draft text untouched); gate item 3 (prose with
   and without the grammar) recorded as "answered by identity for
   this model" — the owner accepted by committing. ADR-0001 got a
   dated annotation; prompt-structure §9 point 4 and §11 got dated
   notes.
10. TODO, arc-plan journal "Entry 2026-09-22", follow-ups updated
    (`d1a1eff`); 09-22 handoff deleted (`a61b431`); PR #7 opened.
11. **Deep parity pass** (`e570a58`) at the owner's request:
    `docs/specs/product-definition.md` (§2–§10, §5.3 rewritten as the
    decided engine, §9 six parked items, §10.1 as-built: NO app token
    was ever built), `docs/roadmap.md`, `docs/follow-ups.md` (new
    entry "llama.cpp unknowns the ADR-0003 gate left open", with a
    write-back rule to lessons §4.10).
12. **TODO restructure** (`cc1b1d6`): Task 6 = history + repository
    layout + timebox + [x] recon brief + [x] gate + **6a fork (NEXT)**
    + **6b show engine**, each item with an acceptance check and a
    "delegable later" mark; "Delegation: OFF" ruling line. The build
    breakdown had lived ONLY in the deleted handoff — restored here.
13. `docs/README.md`: "Delegating a unit of work to another agent —
    an option, NOT in use", with "What crosses over: a work order,
    not a handoff" (comparison table + work-order skeleton).

## 4. Numbers worth remembering (all from committed scripts/raw files)

**Gate (run 1, 2026-09-22):**

- Gate 1: `main` 72 content chunks, first 552 ms, last 1,367 ms,
  spread 0.60; `control` (only `Operator` allowed) → every line
  `Operator:` (the model addressed Ralph and Samantha in the text);
  `nogrammar` → the SAME four lines as `main`, character for
  character; grammar in the top-level `grammar` field of
  `/v1/chat/completions`.
- Gate 2a: `R_late` 0.234, `R_early` 0.257 (D-off prompt ms / A's);
  wall-time ratio 0.59 → 0.16 over ten rounds; A's wall per round 4.4
  → 9.4 s; D-off 1.5–2.0 s; D-live 1.35–1.53 s; reuse A 44→88 %,
  D-off 52→88 %, D-live 55→88 % (rounds 2–10).
- Mechanism: host-RAM prompt cache rescues A; A pays a state swap
  outside `timings` (~1.7 s by round 10: `A-r10-0-Moira`, 13.40.800
  → 13.42.493 in the server log); ~350 ms prompt floor per request
  (130 or 270 tokens alike); RAM evictions 417/422/1,824 MiB at arm
  boundaries.
- Gate 2b: 11.260 vs 11.298 ms/token → **0.3 %**; D-off and D-on
  wrote identical text all ten rounds.
- Every D reply: exactly four lines, all `Name: text`, all ending
  "Over." — "up to four" is read as four.
- Server: largest prompt 1,550 tokens (slot max 1,635 of 16,384);
  all 74 requests `truncated = 0`.

**Run 2 (emotion field, 2026-09-22):**

- **E1 0.5 %** (D-aligned 11.316 vs D-aligned-off 11.263 ms/token),
  PASS; D-aligned and D-aligned-off identical text all ten rounds.
- **E2 10.4 %** (D-forced 12.444 vs D-simple 11.269; 12.38–12.54
  every round).
- E3 40/40 tagged unaided; E4 eight of nine emotions per arm, top
  32 % forced (`calm`), 20 % aligned (`terrified`), 18 % live (`sad`);
  `happy` never used when taught; forced arm never used `afraid`.
- Forced round 1 (empty history) → quoted dialogue, 4 lines only
  (same as the forced stream); rounds 2–10 plain. Seven of 200 lines
  lack a final "Over." (4 quoted, 1 omission in forced round 6, 1
  "Over to logistics—…" line present in both aligned arms).
- D-simple reproduced run 1's D-on text in all ten rounds, 80 min
  later (determinism on one slot).
- Forced stream: first chunk 1,850 ms though prompt 365 ms (likely a
  state swap — not checked in the log).
- Side quest: `’`/`—` in a line → TTS drops the pause before "Over."
  (owner's ear; clips 4.00 vs 4.64 s and 4.08 vs 4.72 s); ellipsis
  harmless (2.08 s both).

## 5. Rulings and decisions of this session (quick list)

- Plain ssh without options for this box; no automatic deploy after
  the updater; lock wait 5 min configurable + clear error (owner
  spec); owner declined predictions in both runs; emotion run not in
  run 1, done as run 2; five arms (D-aligned-live included); side
  quest minimal reporting; wire log added; the emotion list (nine
  values) "very good — tempted to copy to the app"; ADR-0003
  accepted; pin follow-up deleted (proven; synthesis via tts-serve,
  not TalkWithMe — owner ruled it proven); keepalive follow-up
  downgraded (library Wi-Fi, lid closed); handoff deleted; PR
  description left as is; delegation OFF (other harnesses, not
  sub-agents, when ever on); open questions' lasting home = lessons
  §4.10 (+ journal snapshot), follow-ups = the to-do copy with a
  write-back rule.

## 6. The board ahead (canonical state: `docs/TODO.md`)

Mapping from the old handoff's letters: Task B = the gate (DONE) ·
Task C = **TODO Task 6a** (the fork) · Task D = **TODO Task 6b** (the
show engine, 3-day timebox) · Task E = TODO Task 4 (the cast, owner)
· Task F = TODO Tasks 5 (5a/5b/5c), 7 (canned episode + runbook), 8
(close ritual).

1. **PR #7:** the owner reviews and merges. **After the merge: send
   the MassedCompute reminder** (memory file; one gentle line — PR #7
   carries two experiments).
2. **Owner action queue decisions** (TODO): #5 decide the emotion
   field for the fork (measured E1 PASS; lean: yaml switch, default
   on, parser strips the tag before the TTS; the owner said "tempted
   to copy this to the app if the experiment works well" — it worked,
   but ASK); #6 wake or destroy the hibernated VM; #1 voice samples;
   #2 character bibles (they become the cast sheet's sections).
3. **Task 6a — fork TalkWithZombies (~1 hour, NEXT).** Step 1 (the
   GitHub fork under the owner's account) is outward-facing: the
   owner's go, or the owner does it. Then README provenance ("forked
   from TalkWithMe by Steve Corbett (scorbo2)", MIT kept), clone to
   `/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`, installer
   vars (`deploy/ansible/client-talkwithme-mac.yml:16-18`) + a fork
   pin + docs pointer, `allow_tool_calls`/`enable_persona_memories`
   false, **house rules into the fork's `AGENTS.md`**. Acceptance in
   TODO. **The 3-day timebox starts when 6a is done.** Presumably a
   new branch in this repo for the installer change (ask the owner;
   the working rule "never create a new branch" applied to the gate
   work only).
4. **Task 6b — the show engine (3 days; checkpoint at day 1.5:
   continue / scale down / stop).** Exit criterion: an unattended
   loop of ≥10 turns with the four placeholder personas; speakers by
   the new structure, not random; one audience interaction beat that
   opens the mic and absorbs the reply; sentences accumulated, not
   split; on the deployed stack through the tunnel. Server side:
   script assembler (replaces `build_llm_messages`,
   `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/session.py:123`),
   code director (states every grammar constraint in words; line
   budget via `{1,N}`), grammar builder (+ emotion switch), one
   streamed request with top-level `grammar` (`_base_payload`,
   `…/app/services/llm.py:69`), stream parser (trim; strip tag for
   TTS, keep in history; normalize `’‘`→`'`, `“”`→`"`, `—`→`, `,
   `…`→`...`; tolerate quotes), `POST /api/show/round` (sibling of
   `_chat_stream`, `…/app/routers/chat.py:208`; drop empty/placeholder
   STT transcripts — story-loop §6), debug switch (rendered prompt via
   `/apply-template` if it exists, else verbose log; grammar logged in
   full), tests (scripted token streams). Browser: `/show` + `show.js`
   state machine, hold-to-talk, accumulator (~100 chars, ~20 % tail
   tolerance, line-end flush — recon TalkWithMe tour ≈ line 617), SSE
   reader extracted from `sendMessage` (`…/static/chat.js:135-159`).
   Config yaml-only (`show:` section). Polish only if the checkpoint
   is green: prefetch, dead-air static, 1930s look. Fallback:
   TalkWithMe 7.1 + canned episode.
5. **Tasks 5a/5b/5c** after the timebox, in the new engine (5c
   re-scoped: two probes moot). **Task 7** canned episode (seed makes
   retakes reproducible). **Task 8** close ritual (Features Shipped,
   task_history, TODO reset, staleness sweep incl. CLAUDE.md, spec
   BUILT-AND-SHIPPED stamp, **ask permission to delete this
   handoff**).
6. Open questions (lessons §4.10): the 350 ms floor; RAM entry sizes;
   **history-edit cost on the hybrid model — needed before 6b's
   transcript curation**; the check-first sampler belief; whether
   `/apply-template` exists — **verify before 6b's debug switch**;
   the director's constraint cost; single-line beats; the scratchpad
   (must be TAUGHT in the cast sheet).

## 7. Challenges and risks of the arc

- **Time:** 15 days; the timebox (~3.5 days of estimated work in a
  3-day box) is the critical path, with the owner's cast (voices +
  bibles) as the long pole in parallel. No slack for a second
  attempt; the canned episode is the safety net and is a MUST.
- **Identity bleed (taxonomy C4)** is the main risk of the shared
  context; defenses: bibles, audition, stage tags, a director that
  refuses to let one voice dominate.
- **Transcript curation vs the cache** on a hybrid model — unknown
  cost; design must respect it.
- **Prose quality** is Task 5a's question, not the engine's; don't
  tune prompts before the audition (guardrail 2).
- **TTS:** punctuation normalization is required; the accumulator's
  N is provisional (100); ultra-short inputs echo.
- **Demo day:** venue Wi-Fi and the tunnel (a self-reconnecting
  tunnel is cheap insurance); one conversation per server slot (keep
  the chat UI off the show's server); a sleeping browser tab pauses
  the show.
- **Box availability:** hibernated boxes may not wake instantly;
  from-zero deploy is ~7 min, but a fresh box may spend its first
  hour in Ubuntu's updater (the deploy now waits 5 min, then stops
  with a clear message).

## 8. Nuances hard to grasp from the docs alone

- **Experiment folders' findings still say "awaiting the owner's
  review; the folder seals once he accepts it."** The owner committed
  both; at a natural moment (e.g. the close ritual), ask whether to
  mark them sealed — do not edit sealed folders except dated notes.
- **Runlogs are append-only;** fixes to one's own just-written,
  uncommitted entry are fine; after commit, add a dated entry
  (entries 16/17 in the gate folder, 7/8 in run 2's are examples).
- **Discussions are append-only after decisions** (dated addenda);
  ADRs are frozen (dated annotations or supersede). The lessons
  discussion is OPEN; its §1 is verbatim and must stay so.
- **wire.log's header hides which grammar was sent** (only the
  speaker list) — the JSON `request` fields are the truth.
- **The "freeze" of criteria** = the commit carrying them before any
  data; it is NOT the ADR. Do not insist on "freeze" wording.
- **"Up to N lines" is read as N** by Nemotron — the grammar's bound
  must enforce budgets.
- **The model re-reads its own habits** (two trailing spaces, curly
  apostrophes) because the history feeds them back; normalizing the
  history costs no cache (the reply is re-evaluated anyway).
- **`/no_think` is removed by the template** and only flips the
  prompt's ending; keep it in the cast sheet on Nemotron.
- **The spec §10.1 as-built:** no app token exists; the SSH key is
  the whole auth.
- **Pronouns:** existing docs refer to the owner as "he"; new
  writing in this session avoided pronouns for the owner where
  practical.
- **The owner reviews at the permission prompt** only when explicitly
  said so; otherwise wait for the word in chat.
- **The owner likes to test understanding** ("how do you check the
  progress of X?", "is wire.log what the LLM receives?") — answer with
  the mechanism and a live demonstration when cheap.
- **Handoff vs work order** (docs/README.md): this document is a
  session handoff — broad, over-complete, for the lead.

## 9. Mistakes made this session (do not repeat)

- Said in chat that forced lines put "Over." inside quotes "5 of 40";
  the record said 4, all in round 1 → corrected in run 2's runlog
  entry 6. **Lesson: derive with a script before claiming.**
- Mislabeled two server-log tasks (said `A-r09-1-Moira` and
  `D-off-r06`; they were `A-r10-0-Moira` and `D-on-r06`) → corrected
  by counting launches and matching token counts.
- Transcription slip 12.39 vs 12.38; a hand-computed "~30 tokens per
  round" removed from findings. **No hand arithmetic in the record.**
- A poll that ended at its 60-check cap was nearly read as "done" —
  check WHY a loop exited.
- Insisted on "the freeze commit" twice → owner frustration. Explain
  plainly, once.

## 10. Operational gotchas (tools, shell, harness)

- **zsh:** `echo =====` fails (`=` expansion) — use `'-----'`;
  unquoted globs like `--include=*.md` fail ("no matches found") —
  quote them; `PIPESTATUS` does not exist (zsh uses `pipestatus`).
- **Foreground `sleep` is blocked** — use `run_in_background` or a
  background poll loop; polls for the box: read-only, capped.
- **ansible/make from the agent:** `>"$LOG" 2>&1 </dev/null`; long
  deploys in the background; Ansible logs in
  `~/.config/zombie-radio/logs/`.
- **Local Ansible tests:** a scratch playbook run from the scratch
  dir with the project's `.venv/bin/ansible-playbook` and
  `-e ansible_python_interpreter=<repo>/.venv/bin/python` (pyenv
  shims break interpreter discovery; `ANSIBLE_CONFIG=/dev/null` is
  rejected).
- **Python imports in experiment folders leave `__pycache__`** —
  remove before committing; test scripts in scratch COPIES of the
  folder (never write `raw/` during tests); fake local servers on
  ports 18080–18090, never 8080.
- **`.venv/bin/python` has jinja2** (Ansible dependency) — used to
  render the chat template offline (lessons §4.9 has the snippet).
- **Pre-commit ritual:** `grep -rn '<box address>' docs/` (the owner
  supplies the address) plus a key-like-strings scan; `git status`
  to keep `hosts.yml` out; stage by explicit path.
- **`gh`** works; PR tools: `mcp__ccd_pr__get_status` reads the bound
  PR (no CI configured).
- **Wiring:** `make ans-set ENV=cloud IP=<ip>` (refuses if already
  wired) / `make ans-unset ENV=cloud`; `make ssh-tunnel ENV=cloud` is
  the owner's; `make check` prints three ok lines through the
  tunnel.

## 11. Reading order after compaction (verify, don't assume)

1. This document, in full.
2. `git log --oneline -16` and `git status` (branch
   `alfre2v/adr-0003-gate`; is PR #7 merged? `gh pr view 7`).
3. `docs/TODO.md` — owner action queue and Task 6 (6a/6b).
4. `docs/specs/product-definition.md` §5.3 (the engine) and §7.4–§7.5.
5. `docs/decisions/0003-…md` — the Validation section.
6. `docs/discussions/2026-09-22-grammar-and-prompt-cache-lessons.md`
   §4 (esp. 4.2, 4.3, 4.6, 4.9, 4.10).
7. `docs/README.md` — the delegation section (for reference only;
   delegation is OFF).
8. `docs/follow-ups.md` — the llama.cpp unknowns entry; the emotion
   entry; the keepalive entry (low priority).
9. As needed: the two experiment folders' findings; the arc-plan
   journal's last entry (`docs/discussions/2026-09-18-mvp-prototype-arc-plan.md`,
   "Entry 2026-09-22" + its 2026-09-23 snapshot); story-loop and
   prompt-structure discussions for design detail.

## 12. Paste-ready re-orientation prompt (for the owner, after compaction)

```
The context was just compacted. Re-orient before doing anything else:

1. Read docs/discussions/2026-09-23-mid-session-compaction-handoff.md
   IN FULL — it is your mid-session memory bank: how we work (§0 is
   binding, including the live-box drill rules), the exact state
   (§2), what this session did (§3), the numbers (§4), the rulings
   (§5), the board ahead (§6), the nuances and your own mistakes to
   avoid (§8–§9), and the operational gotchas (§10).
2. Follow its reading order (§11) as far as needed to confirm the
   state: at minimum `git log --oneline -16`, `git status`, whether
   PR #7 is merged, and docs/TODO.md's owner action queue and Task 6.
3. Then give me a compact summary: where the arc stands, what is
   pending on my side (PR #7 review/merge, the emotion-field decision,
   the hibernated VM), and the next step you propose (Task 6a, the
   fork) with the first actions you would take — and wait for my go.

Standing rules: strict review-before-commit (I review uncommitted
changes in VS Code — no diffs in chat, no commits without my
explicit word), no AI attribution anywhere, no side panes, minimal
code comments, discussion-first, pushback with receipts welcome,
plain language, no delegation to other agents for now, and one
question at a time when I say I am tired.
```
