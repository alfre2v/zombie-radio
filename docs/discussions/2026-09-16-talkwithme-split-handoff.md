# Mid-session handoff — remote-split experiment, day 2

> **EPHEMERAL HANDOFF** — compaction-survival dump created
> 2026-09-16 at ~76% context, mid-experiment. Per convention
> (discussions/README): delete at session close **with the
> owner's sign-off** once its content lives in the real docs.
> The agent must ASK the owner for deletion permission when the
> session's work concludes. A lingering handoff WILL be read as
> current state — do not let it linger.

## Where we are (30 seconds)

Product definition arc, **Task 3a: the TalkWithMe remote-split
test ("the spike")** — the experiment gating [ADR-0001]'s freeze.
Branch: `alfre2v/talkwithme-remote-split-experiment` (all work
committed & pushed through the group-degeneration entry; commit
`d849030` + later batch). Box: Hyperstack RTX A4000 (Norway-1,
~215 ms RTT today), full stack live: llama.cpp/Nemotron (:8080) +
Faster Qwen3-TTS (:8001) + whisper-fastapi (:8002), loopback-only
behind an `ssh -L` tunnel. TalkWithMe 7.1 runs on the owner's Mac
(:8000). **Steps 1–5 done, ALL gates PASS, zero upstream
modifications — the "configuration, not surgery" hypothesis is
winning.** Step 6 (ensemble) in progress; timebox aborts END OF
2026-09-17. Experiment is trending PASS; current findings are
show-quality issues, explicitly NOT architectural blockers
(scope guard in the runlog).

## Open RIGHT NOW (the immediate thread)

1. **The lab3 A/B test** — owner is running it: fresh room
   `lab3` with the Global System Prompt CLEARED, repeat the
   identical "≥5-sentence report" request. Question it settles:
   group-degeneration (replies shrank to Daniel's bare "Over.")
   — owner's hypothesis: the anti-label prompt breaks
   multi-speaker identity; agent's hypothesis: task-convergence
   + imitation collapse (labels still exist in history via
   `session.py:135/159`, which weakens owner's theory but
   doesn't kill it). Persisting degeneration exonerates the
   prompt; health implicates it → then strategy flips to
   allow-labels + output sanitizer patch (fork trigger).
2. Then, in rough order: harvest the `tts` tmux window tail →
   agent builds the measure-(c) TTFA table (annotate with the
   215 ms RTT baseline) · **name-memory micro-test** (tell a
   scientist a name, reclaim it turns later — signature feature,
   persona memories are ON) · owner's pick of the three creative
   tests (wire-cut mid-session tunnel kill · Spanish
   native-language exchange · unattended echo-chamber broadcast
   soak ~10–15 min, "the pilot episode") · step 7 = SKIP with
   recorded rationale (tunnel already decided + validated) ·
   step 8 teardown: final VRAM/cost, console billing glance,
   destroy VM · complete `findings.md` Results + **Verdict
   against the FROZEN criteria** (PASS/PARTIAL/FAIL each with
   pre-wired consequences; agent's registered prediction —
   PARTIAL close to PASS, 2–4 localhost-isms — is trending
   WRONG in the happy direction: zero found; grade it in
   public) · ADR-0001: truth-audit then freeze to `accepted`
   on PASS/PARTIAL.
3. After the experiment: PR for this branch (owner reviews,
   merges) — NOTE: an experiment PR merging is the owner's
   chosen trigger for the one-line **MassedCompute 50% code
   reminder** (see agent memory + follow-ups.md).

## Locked decisions — do NOT relitigate

- Foundation: **TalkWithMe + tts-serve** ([ADR-0001], draft;
  this spike gates its freeze). Pipecat = named flip-trigger
  fallback only.
- Transport: **SSH tunnel** (`ssh -L`), box exposes :22 only;
  provider security group is the enforced firewall; ufw off.
- MVP: **push-to-talk**, live-first dialogue ("theatrical live
  improvisation with LLMs"), laptop client + cloud GPU server
  (client NEVER hosted on the cloud box — local-first symmetry).
- LLM: ranked shortlist of five ([discussion 2026-09-14]);
  Nemotron Nano 9B v2 = rank-1 presumptive; **the audition
  experiment picks the default** — owner rule: no single-model
  conclusions without an experiment.
- TTS: tts-serve is the interface; MVP deploys the TWO engines
  the §7.2 comparison picks; F5-TTS/Breeze additions = soft goal
  (follow-ups.md).
- Provider posture: new VMs = pinned image **`R570 CUDA 12.8
  with Docker`, Ubuntu 24.04** ([spec §6]); THIS box is a
  grandfathered R535 exception that dies at teardown.
- Fork strategy: **defer until the first patch** (none needed
  yet). Clone at `~/workspace/hackTNT_2026/TalkWithMe`, tag 7.1,
  SHA `93df6ca...`.
- Streaming TTS stays **ON** (non-streaming tested worse).
- VRAM: 24 GB target, 16 GB aspirational (this box is the living
  16 GB probe: full trio = 13.5/15.3 GiB).

## Fresh gotchas (hard to reconstruct from docs alone)

- **Transcript contamination:** the `[Name]:` label fix (Global
  System Prompt) works ONLY in a fresh room — history examples
  beat instructions; one slipped label re-seeds forever. Rooms:
  `Lab` (contaminated), `lab2` (clean, labels gone), `lab3`
  (A/B, prompt cleared).
- **The sentence splitter is naive** — split "Dr. Byrne" at the
  abbreviation. Owner's designated upstream patch:
  **max-chars sentence accumulator** in TalkWithMe `static/tts.js`
  — NOT to be built during the spike (adaptation-arc backlog).
- **Short-sentence economics:** per-request fixed costs (~215 ms
  RTT + ~300 KB reference re-upload per sentence —
  `app/routers/tts.py:134`, stateless API + engine floor) make
  effective RTF > 1 for short sentences; "Over." is pathological.
- **Agent prediction deaths so far:** streaming:false would suit
  radio (WORSE — turn pipelining doesn't cross speaker turns);
  TTS "~2 GB" (default checkpoint is 1.7B → ~5 GB); llama cache
  mount guess v1/v2 (fixed by **canonical v3**:
  `-v $HOME/models:/models -e LLAMA_CACHE=/models`); the
  /dev/null STT probe (bad gate design). All graded in the
  runlog.
- **Nemotron MUST run reasoning-off** — `/no_think` as line 1 of
  every persona prompt.md (works through TalkWithMe's prompt
  assembly); watch for empty `content` if it ever regresses.
- **tts-serve engine pins:** `transformers==5.15.1` exactly
  (5.17.0 crashes on MimiConfig/rope_theta); numpy must be
  pip-installed BEFORE `faster-qwen3-tts` (legacy sox setup.py);
  apt needs `python3.10-venv sox` + `apt-get update` first.
- **Hyperstack hibernation = stop+boot-with-disk** (no process
  survives, restore is a stock lottery); never hibernate a show
  box; disk caches survive (models don't re-download).
- **The experiment README has TWO sections by owner decree:**
  "Reproduction recipe — THE section to follow" (living,
  R0–R13, always-current commands) vs "Runlog" (append-only
  history with ⚠ superseded banners). Convention codified in
  `docs/experiments/README.md`. Never point the owner at the
  runlog for commands.
- Whisper lazy-loads its model at first request (VRAM reads low
  until first mic use). STT quality specimen: "Miss Betty" →
  "Nisbeti" (C6 field-observed; character absorbed it
  in-fiction — delightful, documented).
- Box user `ubuntu` (sudo + docker group); tmux session `radio`,
  windows llama/tts/whisper/ops; `tmux-refresher.md` exists.

## Collaboration reminders (owner: Alfredo)

Tight learning loop — progress and owner-learning carry EQUAL
weight; "go into teaching mode" switches goals. **Persisting a
discussion = the integrated outcome, never a chronicle** (twice
corrected). Ranked lists over single winners; experiments make
picks. He wants hard pushback and receipts (`file:line`). STRICT
review-before-commit (permission-prompt review was explicitly
authorized for THIS handoff commit only). **No AI attribution in
commits/PRs, ever.** Never open desktop side panes
(`mcp__ccd_view__show_pane`) — he reviews in VS Code. Chronology
belongs only in the per-arc Q&A log.

## Cold-start reading order

1. This handoff (you are here).
2. `docs/experiments/2026-09-14-talkwithme-remote-split-test/README.md`
   — masthead, Reproduction recipe, then the LAST ~5 runlog
   entries (2026-09-16 ones).
3. Same folder: `findings.md` (frozen criteria + preliminary
   results), `tts-engine-ranking.md`, `placeholder-personas.md`,
   `scouting-hyperstack-a4000.md`.
4. `docs/TODO.md` — arc state, Owner action queue.
5. `docs/specs/product-definition.md` §3, §7, §10 (topology,
   gates, security) — the spec this all serves.
6. Deeper history only if needed: brainstorm (§5 challenges C1–
   C10, §9 debate), the two provider/framework surveys, QA log.

## Arc-level task map (beyond this experiment)

- Task 2 residue: **LLM audition** (Track 3; needs character
  bibles; runs on owner's 3090) · **§7.2 TTS comparison + VRAM
  budget** (needs R570 box so all six engines qualify + owner's
  4 voice samples; C10 emotional-coherence is an explicit test
  item).
- Task 4: fold experiment results into the spec, replace
  `[UNKNOWN]` markers, derive follow-on arc candidates for the
  roadmap.
- Task 5: spec review + ADR-0001 truth-audit & freeze.
- Task 6: close ritual IN the closing PR (roadmap Features
  Shipped, task_history migration, TODO reset, staleness sweep,
  **runbook promotions**: post-restore restart sequence +
  demo-day protocol are flagged candidates; **ask owner to
  delete this handoff**).
- Owner action queue (TODO.md): voice samples · character bibles
  · home 3090 driver check · demo-day logistics radar.

## Paste-ready re-orientation prompt

```
We are mid-session on the Zombie-Radio project, resuming after a
manual context compaction. Re-orient yourself now:

1. Read docs/discussions/2026-09-16-talkwithme-split-handoff.md
   in full — it is the compaction-survival handoff you wrote
   minutes before compaction and it holds the session state,
   locked decisions, fresh gotchas, and the immediate open
   thread.
2. Follow its cold-start reading order (experiment README's
   recipe + last runlog entries, findings.md, TODO.md).
3. Then confirm to me in a few sentences: where the experiment
   stands, what the lab3 A/B test is deciding, and what remains
   before teardown and verdict.

Do not start any new work until you've confirmed. My rules
still stand: strict review-before-commit, no AI attribution
anywhere, no side panes, pushback welcome.
```

## Postscript (fill only if reality drifts after this snapshot)

*(empty)*
