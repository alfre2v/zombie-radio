# Task history — engineering log of closed arcs

*Append-only. When an arc closes, its TODO.md content migrates here
verbatim under `## <Arc> (closed YYYY-MM-DD, PR #N)`, so the log of
what-landed-when survives.*

## Product definition (closed 2026-09-17, PR #3)

# TODO — Product definition arc

**Arc:** Product definition · **Started:** 2026-09-12 ·
**Branch:** `alfre2v/product-definition`
**Spec:** none going in — this arc is special: its deliverable IS
`specs/product-definition.md`. The arc closes when that spec is
reviewed and its PR merges.

**Notation recap** (full conventions in [docs/README.md](README.md)):
`[ ]` open · `[x]` done (with commit SHA in parentheses) · `[~]`
re-scoped/moved to another arc (says where) · `Task N` is a
sub-step here, never a PR number · cite discussions as
`[discussion YYYY-MM-DD]`, specs as `[spec §X.Y]`.

## ⚡ THE PROTOTYPE-FIRST INVERSION (2026-09-16) — read this first

The arc's ending was reshaped by owner decision the evening the
spike closed ([discussion 2026-09-16] prototype-first inversion):
**build the MVP prototype first (the spike's exact validated
configuration), run the remaining experiments ON the prototype,
write the spec's remaining parts alongside the build.** Three
guardrails accepted: experiments lighter-not-looser (protocol
skeleton survives) · prompt work disposable until the
in-prototype audition · spec as ledger (decisions still get
written, lag ≤ one session). Consequences: §7.2/§7.3 experiments
MOVE to the next arc ("MVP prototype", roadmap); this arc now
wraps quickly — spec quick-pass → Task 5 review → Task 6 close.

This file is the **living parking-lot table** of the task
landscape (owner-requested 2026-09-16): updated at every
execution or decision; the re-orientation surface when revisiting
any topic.

## Owner action queue

*Actions only the owner can take, so they never get lost in chat
scrollback. Items get DELETED when done; the agent keeps this
current. (Added 2026-09-14 at the owner's request.)*

1. **Gather 4 reference voice samples** — EXECUTING SOON (owner,
   2026-09-16). Likely famous-actor movie clips for comedy value
   → **NEVER committed to the repo** (curated and used locally;
   gitignore rule in follow-ups.md). Unblocks the in-prototype
   TTS comparison. Related: find the voice-isolation tool
   scorbo2 mentioned on his podcast (follow-ups.md).
2. **Seed the character bibles** — EXECUTING SOON (owner,
   2026-09-16). Names, personalities, quirks, voice descriptions
   for the four scientists; rough is fine. Model-neutral, so safe
   under guardrail 2; unblocks the in-prototype LLM audition.
3. **Check the home 3090 box's NVIDIA driver** — DEPRIORITIZED
   (owner ruling 2026-09-16): the demo is cloud-only; the 3090
   leaves the MVP fleet, retiring the fleet-minimum-driver worry
   (show boxes are pinned R570 per [spec §6]). Revisit only if
   local development on the 3090 resumes.
4. **Demo-day logistics radar** — POSTPONED until a working MVP
   exists (owner ruling 2026-09-16). One piece pre-decided: the
   **"canned episode" emergency mode is a MUST** — recorded from
   the prototype once it works; the rest (venue internet,
   hotspot fallback) stays on radar.

*(SSH-keypair item deleted 2026-09-16: done — the spike ran its
whole life through that key.)*

## Sub-steps

- [x] **Task 1 — Vision & interaction model discussion.** DONE
  (2026-09-13). What the audience experiences, the 4-actor
  format, interaction mechanic, and 3-week scope. Note: the
  originally planned standalone output doc was never created —
  the discussion happened iteratively and its record lives in
  the QA log Entries 2–4 (chronology) and brainstorm §1–§2
  (synthesis); the settled result is [spec §1]–[spec §2].
  Residual smalls (session/loop length target, client form)
  are tracked in the spec's unknowns, not here.
- [ ] **Task 2 — Architecture & foundational tech survey.**
  IN PROGRESS (2026-09-13). Load-bearing choices graduate to ADRs.
  - [x] **Audio framework survey** (LiveKit / Pipecat / Dograh) →
    `discussions/2026-09-13-audio-framework-survey.md` (edac920).
    Verdict: Pipecat if forced to pick; TalkWithMe MVP decision
    reaffirmed; smart-turn model + SmallWebRTC pattern flagged as
    framework-independent borrowings.
  - [x] **Foundation debate + ADR-0001 drafted** (edac920) —
    freeze gated on the Task 3a spike verdict.
  - [x] **Cloud GPU provider survey** (13 providers) →
    `discussions/2026-09-13-cloud-gpu-provider-survey.md`
    (af6b94b). S0 criteria agreed with owner; shortlist:
    Hyperstack primary, Scaleway EU alternate, Vast.ai dev
    workhorse, Massed Compute conditional on 50%-code
    verification; provider-agnostic-Ansible hedge + demo-day
    protocol.
  - [x] **TTS goal settled** (QA log Entry 5; brainstorm §3):
    tts-serve = interface; MVP deploys the TWO engines that win
    the comparison experiment; F5-TTS + Breeze TTS 2 additions =
    soft goal in follow-ups.md.
  - [x] **STT decision** (QA log Entry 6; brainstorm §3): Whisper
    via whisper-fastapi (TalkWithMe-native); model SIZE left
    deliberately open — checkpoints are interchangeable, the
    VRAM experiment sets the knob.
  - [x] **Deployment doctrine amendment** (QA log Entry 6;
    brainstorm §4): Docker preferred, NOT mandatory — per-engine
    bare-metal-via-Ansible is a sanctioned fallback, with
    per-engine isolation required either way.
  - [~] **LLM choice** — RE-SCOPED to the MVP-prototype arc by
    the inversion (2026-09-16). What this arc delivered: the
    RANKED SHORTLIST of five ([discussion 2026-09-14] §4–§6) —
    (1) Nemotron Nano 9B v2, (2) Gemma 4 12B StyleTune/heretic,
    (3) Rocinante-X-12B, (4) Qwen3.5-9B, (5) Wayfarer-2-12B;
    LFM2.5-2.6B reserved for utility roles. The audition that
    picks the working default now runs IN the prototype
    (guardrail 1: protocol skeleton retained). Field intel: the
    rank-1 presumptive showed dialog-quality concerns in the
    spike (spec §4).
  - [~] **Latency/VRAM budget** — RE-SCOPED to the MVP-prototype
    arc (in-prototype §7.2 experiment). PARTIAL DATA already
    from the spike (2026-09-16): full trio fits 16 GB
    (14.0/15.3 GiB warm); streaming TTFA median 0.9 s over a
    ~215 ms WAN. Remaining there: per-engine numbers (LuxTTS now
    in the pool — follow-ups.md), two-engine stack, 24 GB-tier
    budget, Whisper size.
- [x] **Task 3 — Experiments (conditional).** CLOSED for this arc
  (2026-09-16): Task 3a ran and PASSED; the two remaining
  candidates (§7.2 TTS comparison, §7.3 LLM audition) moved to
  the MVP-prototype arc as in-prototype experiments per the
  inversion — they keep the protocol skeleton (timebox,
  pre-registered pick criteria, runlog) per guardrail 1.

  - [x] **Task 3a — TalkWithMe remote-split test ("the spike").**
    DONE (2026-09-16): **verdict PASS** against the frozen
    criteria; ADR-0001 frozen to `accepted`; Pipecat flip trigger
    expired unfired. Full record:
    `experiments/2026-09-14-talkwithme-remote-split-test/`
    (runlog + findings + TTFA data); show-quality issues routed
    to the adaptation-arc backlog; narrative-health framework
    spawned → [discussion 2026-09-16]. Residue: owner completes
    the console destroy + billing glance (final cost appended to
    the runlog when read). Original brief kept below for
    provenance. SKELETON CREATED
    2026-09-14 →
    `experiments/2026-09-14-talkwithme-remote-split-test/` (runlog
    template + draft verdict criteria + agent prediction
    registered; freeze pending owner's prediction slot — Owner
    action queue). Box plan: Hyperstack A6000 first, Vast RTX
    PRO 4000 VM alternate.
    Born from the foundation debate ([discussion 2026-09-13]
    brainstorm §9): the single biggest untested assumption under
    the MVP plan is that TalkWithMe — a localhost-born app — can
    be split into a remote backend + laptop browser client over
    real internet.
    - **Question:** how deep do TalkWithMe's localhost assumptions
      go? Can the computational backend live on a remote machine
      with the client on a laptop across a WAN?
    - **Setup:** clone TalkWithMe (v7.0); deploy its backend on a
      remote Linux box — the surveyed cloud GPU instance if
      available by then, otherwise the owner's Linux PC reached
      over a non-LAN path (e.g. tailscale/port-forward, so real
      internet characteristics apply); llama.cpp server with a
      small model; ONE tts-serve engine wired through TalkWithMe's
      existing TTS support or a minimal adapter; client in a
      browser on the Mac laptop.
    - **Measures:** (a) does audio delivery survive WAN
      (buffering behavior, drops, stalls)? (b) is a 4-persona
      group session with distinct voices drivable end-to-end?
      (c) time-to-first-audio per dialog line (rough numbers,
      recorded); (d) effort estimate for a proper tts-serve
      adapter; (e) architectural red flags (blocking calls,
      hardcoded localhost, tight client-server coupling);
      (f) security observations for [spec §10.1]: does anything
      in the stack provide auth? which ports must be public?
    - **Setup note (corrected per [spec §10.3] and the §3.1
      topology):** modified TalkWithMe runs ON the laptop (page
      at `http://localhost` = secure context, mic works, no TLS
      needed); the remote box hosts only model services. Test
      the laptop↔server channel BOTH ways if cheap: plain
      `ws://`+token, and through an `ssh -L` tunnel (the §10.3
      recommended transport) — the tunnel variant is the one the
      MVP will likely ship.
    - **Timebox: 2 days.** Abort at end of day 2 regardless of
      state; a partial observation recorded honestly beats an
      overrun.
    - **Verdict criteria (pre-registered, per protocol — final
      wording frozen in findings.md BEFORE running):** PASS =
      4-persona audio session over WAN, time-to-first-audio
      ≤ ~5 s/line, no structural blocker → MVP proceeds on
      TalkWithMe. PARTIAL = works with enumerable fixable issues
      → proceed, issues become sub-steps. FAIL = structural
      localhost coupling (audio path unusable over WAN, pervasive
      blocking design, unownable code) → **flip trigger fires:
      MVP moves to Pipecat** (survey already done, brainstorm §9
      records the fallback rationale).
    - **Predictions to register before starting** (owner + agent
      each, per experiment protocol).
    - **Output:** `experiments/2026-09-14-talkwithme-remote-split-test/`
      with self-contained runlog README.md (every command + its
      output) and findings.md (interpretation only).
- [x] **Task 4 — Draft `specs/product-definition.md`.** DONE
  (2026-09-17, PR #3): quick-wrapped under the inversion — spike
  results folded (§3.3 resolved, §10.1 verified, §7.1 PASS);
  remaining `[UNKNOWN]`s marked *deferred-to-prototype* (LLM
  default, TTS winners + Whisper size, §5.3 director, §6 demo-day
  fallback); next arc derived (MVP prototype — roadmap). The spec
  lives on as a LEDGER during the build (guardrail 3).
- [x] **Task 5 — Owner review of the spec; ADRs frozen.** DONE
  (2026-09-17): ADR-0001 truth-audited and accepted at the spike
  verdict; the spec review IS the owner's review of PR #3, which
  carries the spec's final wrapped form — merging it executes
  this task.
- [x] **Task 6 — Close ritual in the PR.** DONE (2026-09-17,
  PR #3, this commit): roadmap Features Shipped entry ·
  task_history migration · TODO reset · staleness sweep
  (CLAUDE.md included) · runbook promotion — the post-restore
  restart sequence graduates to
  `runbooks/service-restart-sequence.md`; the demo-day protocol
  promotion is DEFERRED to the MVP-prototype arc (it cannot be
  written before the prototype exists; spec §6 already requires
  it to graduate once smoke-tested).

## Task definition status

*How well-defined each sub-step is; updated as discussions fill the
gaps. The agent keeps pushing on "missing" cells.*

| Task | Definition | What's still missing |
|---|---|---|
| Task 1 — Vision & interaction model | **defined — ready for spec write-up** | All majors settled (QA log Entries 2–4; brainstorm §1–2, §4): radio-show fiction, laptop-client + cloud-GPU-server demo for Oct 8 (booth = future vision), push-to-talk MVP interaction, live-first dialogue ("theatrical live improvisation with LLMs", hybrid trajectory-scaffolds post-MVP). Residual smalls: session/loop length target · client form (browser page vs native) |
| Task 2 — Architecture & tech survey | **done for this arc** (2026-09-16, via the inversion) | Settled: foundation (ADR-0001 accepted via the spike) · provider survey + Docker/GPU verified · STT (whisper-fastapi) · TTS goal (tts-serve + two winning engines) · LLM ranked shortlist of five. The two picks that remained (LLM default, TTS winners) are re-scoped to in-prototype experiments in the MVP-prototype arc |
| Task 3 — Experiments | **closed for this arc** | Task 3a (remote split) DONE — verdict PASS. §7.2 + §7.3 moved to the MVP-prototype arc (guardrail 1: protocol skeleton retained) |
| Task 4 — Draft spec | **quick-wrap** | Spike results folded (2026-09-16); remaining: mark open `[UNKNOWN]`s deferred-to-prototype; the spec becomes a ledger during the build (guardrail 3) |
| Task 5 — Spec review, ADR freeze | defined | — |
| Task 6 — Close ritual in PR | defined | — |

## Completed

*(none yet)*

## Open questions (acute, arc-specific)

*(none yet — standing questions will live in the spec once it exists)*

## Standing cross-arc notes

- Hard deadline **2026-10-08**: every decision in this arc should be
  weighed against ~2 weeks of build time remaining after it closes.

