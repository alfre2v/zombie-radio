# TODO — Product definition arc

**Arc:** Product definition · **Started:** 2026-09-12 ·
**Branch:** `alfre2v/product-definition`
**Spec:** none going in — this arc is special: its deliverable IS
`specs/product-definition.md`. The arc closes when that spec is
reviewed and its PR merges.

**Notation recap** (full conventions in [docs/README.md](README.md)):
`[ ]` open · `[x]` done (with commit SHA in parentheses) · `Task N`
is a sub-step here, never a PR number · cite discussions as
`[discussion YYYY-MM-DD]`, specs as `[spec §X.Y]`.

## Sub-steps

- [ ] **Task 1 — Vision & interaction model discussion.** What the
  audience experiences: what "interactive" means this time (voice
  input? choices? live vs generated-ahead), the 4-actor format, one
  play-through's shape, and what is OUT of scope for a 3-week build.
  Output: `discussions/2026-09-12-vision-and-interaction-model.md`
  (or dated when it happens).
- [ ] **Task 2 — Architecture & foundational tech survey.**
  IN PROGRESS (2026-09-13). Audio-framework landscape survey
  (LiveKit vs Pipecat vs Dograh) DRAFTED →
  `discussions/2026-09-13-audio-framework-survey.md`, pending
  owner review. Verdict: Pipecat if forced to pick; TalkWithMe
  MVP decision reaffirmed; smart-turn model + SmallWebRTC pattern
  flagged as framework-independent borrowings. Still ahead:
  cloud-GPU provider survey (critical path) · LLM/STT choices ·
  latency/VRAM budget. Load-bearing choices graduate to ADRs.
- [ ] **Task 3 — Experiments (conditional).** Fires when a survey
  leaves a question needing measurement. Each gets a timeboxed
  `experiments/YYYY-MM-DD-*/` folder per conventions (runlog
  README + findings.md with pre-registered verdict criteria).

  - [ ] **Task 3a — TalkWithMe WAN-decoupling spike.** PRIORITY:
    first in the experiment queue; run as soon as the cloud
    provider survey lands (or sooner using a stand-in remote box).
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
      hardcoded localhost, tight client-server coupling).
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
    - **Output:** `experiments/2026-09-XX-talkwithme-wan-spike/`
      with self-contained runlog README.md (every command + its
      output) and findings.md (interpretation only).
- [ ] **Task 4 — Draft `specs/product-definition.md`.** Synthesize
  Tasks 1–3 into the record of intent: MVP definition, architecture
  direction, follow-on arc candidates for the roadmap build order.
- [ ] **Task 5 — Owner review of the spec; ADRs frozen.** Truth
  audit on any draft ADRs, then mark accepted.
- [ ] **Task 6 — Close ritual in the PR.** Roadmap Features Shipped
  entry, task_history migration, TODO reset, staleness sweep
  (CLAUDE.md included). PR reviewed, approved, and merged by the
  owner.

## Task definition status

*How well-defined each sub-step is; updated as discussions fill the
gaps. The agent keeps pushing on "missing" cells.*

| Task | Definition | What's still missing |
|---|---|---|
| Task 1 — Vision & interaction model | **defined — ready for spec write-up** | All majors settled (QA log Entries 2–4; brainstorm §1–2, §4): radio-show fiction, laptop-client + cloud-GPU-server demo for Oct 8 (booth = future vision), push-to-talk MVP interaction, live-first dialogue ("theatrical live improvisation with LLMs", hybrid trajectory-scaffolds post-MVP). Residual smalls: session/loop length target · client form (browser page vs native) |
| Task 2 — Architecture & tech survey | **partial, direction set** | Main plan inverted (QA log, Entry 2): adapt TalkWithMe + tts-serve; owner effort on deployment + new TTS engines for tts-serve; LiveKit/Pipecat demoted to comparison note. Demo confirmed on a cloud GPU instance (QA log, Entry 4) → provider survey now on the critical path. Missing: LLM & STT choices · latency/VRAM budget · cloud-GPU provider survey (Docker+GPU passthrough) · F5-TTS vs newer engines. Ansible-deployment project: deferred by ruling (private repo; surgical extraction at deployment time — QA log, Entry 3) |
| Task 3 — Experiments | **vague by design** | Fires only if Task 2 leaves measurable questions; candidates so far: TTS engine quality/latency, provider GPU-in-Docker check |
| Task 4 — Draft spec | shape known | Blocked on Tasks 1–2 content |
| Task 5 — Spec review, ADR freeze | defined | — |
| Task 6 — Close ritual in PR | defined | — |

## Completed

*(none yet)*

## Open questions (acute, arc-specific)

*(none yet — standing questions will live in the spec once it exists)*

## Standing cross-arc notes

- Hard deadline **2026-10-08**: every decision in this arc should be
  weighed against ~2 weeks of build time remaining after it closes.
