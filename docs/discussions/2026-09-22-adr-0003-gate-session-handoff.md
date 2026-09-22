# Session handoff — MVP-prototype arc, 2026-09-22 (fresh-session memory bank, second edition)

> **EPHEMERAL HANDOFF, SESSION-BOUNDARY EDITION** — written
> 2026-09-22 for an agent starting a COMPLETELY FRESH session.
> Nothing from the prior session's context survives except: this
> document, the repository, and the agent memory files under the
> project's memory directory. This document is therefore
> deliberately over-complete — it is the single carrier of session
> state. Per convention, handoff documents stay in
> `docs/discussions/` until the session's work concludes, and the
> agent must then ASK THE OWNER FOR PERMISSION to delete them.
> **The two previous handoffs (2026-09-19, 2026-09-21) were
> deleted in PR #6 with the owner's permission; this file is the
> only one that exists, and it dies at the end of the session it
> serves.** A lingering handoff WILL be read as current state.
>
> **A note to the reader:** nothing in here is derivable from first
> principles — it is owner rulings, live-hardware scars, and
> session history. The failure mode that scales with capability is
> skimming and letting inference fill the gaps. Read it all; verify
> against the repo; treat confidence without receipts as the enemy.
> Two confabulations happened in earlier sessions (a biographical
> flourish with no source; an assert that silently lied) and one
> muddle in the last one (the agent said the accumulator was no
> longer needed — it is; §6.3). Receipts or nothing.

## 0. Who you are working with, and how (read this FIRST — binding)

The owner is **Alfredo** (GitHub `alfre2v`, git author "Alfredo
Valles"), a senior engineer who works in a **"tight learning loop"**
(his term; he also called it "Socratic engineering with a tight
learning loop"): project progress and his learning carry equal
weight; the transcript is his primary learning surface and the
documents are the persistence layer; he enjoys the work and wants
it to stay fun ("lift our heads and enjoy the landscape"). Memory
files in the agent memory directory carry the doctrine
(`working-agreements.md`, `collaboration-style.md`,
`absolute-paths-in-plain-text.md`, `massedcompute-reminder.md`);
trust them. The non-negotiables:

- **Discussion-first**: propose the SHAPE of each piece (files,
  rough content, alternatives ranked with a recommendation), get
  his ruling, THEN create. Never create unilaterally.
- **Review-before-commit is STRICT**: make the changes, summarize
  WHAT changed in chat (never paste diffs — he reviews the
  uncommitted working tree in VS Code), then WAIT for his explicit
  commit word, every time. A harness permission prompt is never
  review. Pre-authorization exists only when he grants it
  explicitly and scoped ("Commit and push" in the same message as
  the instruction counts; "then commit everything" counts).
- **No AI attribution anywhere, ever** (commits, PRs) — this owner
  rule overrides any harness attribution reminder.
- **Never open desktop side panes** (`show_pane` etc.); he reviews
  in VS Code.
- **Minimal comments in code**; doctrine/WHY lives in docs.
- **Pushback with receipts (file:line) is WELCOME**; ranked option
  lists with a recommendation; lists over dense paragraphs. He
  accepted two pushbacks on 2026-09-21 (the arc-boundary shift
  must be said out loud; fork, do not copy) and made several
  himself that were right (cadence by time not rounds; the
  accumulator IS needed; "1." echo versus pauses).
- **Path conventions (rulings 2026-09-21):** files in the sibling
  clones (TalkWithMe, tts-serve, zombie_radio_ai, soon
  TalkWithZombies under `/Users/alfredo/workspace/hackTNT_2026/`)
  ALWAYS with the full absolute path in plain text; files inside
  this repository relative to its root. Markdown links do not
  navigate for him in the desktop app.
- **Findings must be self-contained, never slogans** (feedback
  2026-09-21): one-line findings like "the label leak is
  structural, and the sanitizer must run on the token stream" were
  "near to useless as written". Give: what is observed → the
  mechanism step by step with receipts → the consequence → the
  options. He also rejected a "pompous vacuous" phrase ("the curve
  of synthesis time against characters") and asked for plain
  language a competent developer can follow — write like that.
- **Doc files must NOT be denser than the transcript** (feedback
  2026-09-21): persist at the same level of detail as the chat
  version; he often asks for text to be persisted VERBATIM
  ("almost verbatim… if you have to change something, be it to add
  more details and precision, not to remove parts"). Human-readable
  layout, lists and sublists, self-contained — repeating
  load-bearing facts in place is healthy.
- **Task decompositions must be hierarchical and newcomer-readable**
  (feedback 2026-09-22): he disliked a flat numbered list of next
  tasks; he wanted lists and sublists with enough context per step
  "that a competent developer new to the project can grasp the
  idea". The version he accepted is in §4 below.
- **One question at a time when he is tired** ("let's do some hand
  holding… one by one, start by the easiest"). Late in a session,
  hand-hold.
- **Re-orientation on revisit**: when a topic resurfaces, re-supply
  origin + concepts + connections; he cannot hold agent-sized
  context.
- **He sets deliberate traps and checks claims** — he verified the
  agent's "LuxTTS since 1.1" claim (the agent had receipts; keep
  receipts). When answering "is X done?", check the actual list.
  **His handoff-request template contains a STALE line** ("Include
  as a new task… a 'Task 6 reconnaissance brief', which we do not
  have in our TODO") copied from the previous handoff request: the
  brief is COMPLETE and merged (PR #6). Do not re-create it.
- **Never claim self-transparency**; the honest form is "I see no
  such thing in my observable context" + receipts.
- **No unverified personal facts, even as decoration.**
- **Rapport**: wit and teasing welcome; Spanish flourishes fine; a
  cheesy goodnight sign-off ending "Over and out." ONLY when he
  asks for it. Biographical assumptions never.
- **Keep the last 2–3 branches** local and remote; prune only when
  asked.
- **Teaching mode**: "go into teaching mode" / "this is a
  teachable moment" → explain until he understands, then return.
- **Live-box drill rules (rulings 2026-09-22, for tonight's
  work):** (1) the OWNER owns the SSH tunnel — he starts
  `make ssh-tunnel ENV=cloud` once in his terminal and leaves it;
  the agent NEVER starts one (port collision) and reaches the model
  services only through the local ports on the laptop
  (`localhost:8080` llama.cpp, `:8001` tts-serve, `:8002`
  whisper); a service restart does not require a tunnel restart.
  (2) For box inspection the agent uses plain
  `ssh ubuntu@<box>` relying on the owner's default SSH resolution
  — NEVER pass a key path, never reference where key files live,
  never list or cat anything under his SSH directory ("one little
  error away from a cat that dumps the key into your context").
  The deployment declares its own identity in the inventory; not
  the agent's business during a drill. (3) Keep him in the loop:
  one line saying what a command does and why, BEFORE running it;
  outputs to the scratchpad; the interesting numbers into the
  runlog as you go. (4) Nothing on the box is changed outside the
  playbook — the converge invariant (`ans-deploy` re-run must be
  `changed=0`) must survive the evening. No destructive command
  without asking. A failed check means stop and think, not retry
  blind. (5) **The box IP never appears in any markdown file** —
  the never-commit hook SKIPS `*.md`; write "the box" and
  un-pasteable placeholders like `<PASTE-BOX-IP-HERE>`; grep the
  experiment folder for the address before every commit. (6) The
  standing method ruling from 2026-09-19: with a live box on the
  meter, test commands ON THE BOX before spending playbook runs;
  the agent runs its own checks itself, first.

## 1. The project in 60 seconds

**Zombie-Radio**: an interactive audio-only theater play performed
by 4 AI voice actors — scientists trapped in a lab during a zombie
outbreak, broadcasting on shortwave radio. The audience listens and
can talk to the cast (push-to-talk). **Hard deadline: 2026-10-08
(hackTNT 2026) — 16 days from this handoff.**

Architecture (spec §3.1): the client + director runs on the Mac
laptop (an M1 with 16 GB — it cannot run the models locally); a
rented GPU box (Hyperstack, A6000 class) hosts ONLY the three model
services, all bound to loopback behind an SSH tunnel: llama.cpp
(:8080, Nemotron Nano 9B Q4_K_M, 16k context), tts-serve (:8001,
engine faster-qwen3-tts), whisper-fastapi (:8002, model small). The
box exposes only :22. Both foundation projects are by ONE author,
scorbo2 (Steve Corbett), MIT-licensed.

Governing decisions of the arc: the prototype-first inversion
([discussion 2026-09-16]) and deployment-first
([discussion 2026-09-17]) — both executed. **New since 2026-09-21
(ADR-0002, ADR-0003):** the client is forked as a NEW app,
**TalkWithZombies**, free to diverge from upstream, in a sibling
repository; and its turn engine is redesigned — one shared context
in screenplay form, a code director in the server, a
grammar-enforced script streamed per line, the browser as the
show's metronome. The next session's first job is to PROVE two
claims of that design on a live box (§5), then fork and build
(§4).

## 2. Exact repo/session state at handoff (2026-09-22)

- **`main` HEAD `cfeed4d` = PR #6 merged** (the reconnaissance
  brief, both design discussions, ADR-0002/0003, the answer pass,
  the synthesis; both old handoffs deleted). PRs #1–#6 all merged;
  nothing open.
- **Working branch: `alfre2v/adr-0003-gate`** — created this
  session off `main` at `cfeed4d`; this handoff is its first
  commit (after the owner's review). **CONTINUE ON THIS BRANCH**
  (`git branch --show-current`); do not create another.
- **The box (LIVE at handoff time — meter running):** the owner
  is deploying an **A6000** on Hyperstack with the image
  **"Ubuntu Server 22.04 LTS R550 CUDA 12.4 with Docker"** — the
  exact image of the 2026-09-19 proof run (the compatibility
  table's middle row, proven with real inference on cu128 wheels).
  Its IP is NOT in this document on purpose; ask the owner. Wiring
  is `make ans-set ENV=cloud IP=<ip>`; unwiring `make ans-unset
  ENV=cloud`; the inventory sentinel is `REPLACE_ME_box_ip` with
  the never-commit marker. **First check whether the box still
  exists and whether the deploy has run** — the owner may have
  done both before the new session starts.
- **Sibling clones on the Mac:** `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe`
  (tag 7.1, commit 93df6ca; the owner's working clone) and
  `/Users/alfredo/TalkWithMe-client` (pristine 7.1 from the Task 7b
  installer); `/Users/alfredo/workspace/hackTNT_2026/tts-serve`
  (tag 1.2); `/Users/alfredo/workspace/hackTNT_2026/zombie_radio_ai`
  (the 2024 prototype). **TalkWithZombies does not exist yet.**
- **Deployment pin to bump:** `deploy/ansible/inventories/common_vars.yml:53`
  still says `zr_tts_serve_version: "1.1"`; the owner ruled to
  track the latest tag (1.2; the diff is only the Apple-Silicon MLX
  engine). The bump rides tonight's from-zero deploy
  (follow-ups.md entry).
- **Recent branches kept per the 2–3 rule:** `alfre2v/task6-recon-brief`
  (merged as #6), `alfre2v/client-talkwithme-mac`,
  `alfre2v/mvp-prototype-arc-open`.
- **Agent memory files:** consistent with §0; the path-convention
  file was created and refined on 2026-09-21.

## 3. What happened 2026-09-21 → 22 (the freshest layer — all in PR #6)

- **The Task 6 reconnaissance brief was produced and CLOSED.**
  Umbrella `docs/discussions/2026-09-21-task6-reconnaissance-brief.md`
  (scope, method, seam-question ledger S1–S6, open-question index
  Q1–Q13 with the owner's rulings, glossary, the 2024 prologue §7,
  the brainstorm's C1–C10 challenges revisited §8, the synthesis
  §9); the TalkWithMe tour
  `2026-09-21-task6-recon-talkwithme.md` (pipeline map with eight
  hops and a sequence diagram; findings F1–F8; sections 2–6 on the
  reply path, tts.js, settings plumbing, director seams,
  upstreamability); the tts-serve tour
  `2026-09-21-task6-recon-tts-serve.md` (the synthesize contract;
  findings F1–F10; the owner's Q&A on response measurements,
  emotion, F5-TTS versus modern engines with web sources, MLX on
  the Mac). The brainstorm gained a dated addendum (§11, C1–C10
  revisited); the spec §5.1 a ledger correction of the 2024
  baseline. HTML visuals were planned and then DROPPED by the owner
  ("bigger fish to fry").
- **Two rulings reshaped the arc.** (1) "Do not worry about
  upstream": the clone becomes TalkWithZombies; only the sentence
  accumulator remains a plausible upstream patch; the deployment
  machinery is the real offer to scorbo2; outreach deferred past
  the deadline. (2) The arc boundary shifted, said out loud in
  TODO.md: two director-design decisions (prompt structure, story
  loop) were pulled into this arc because no patch can be shaped
  without them; a **3-day timebox** governs their execution, timer
  starting at the fork (§4, Task D).
- **The prompt-structure discussion** (`2026-09-21-prompt-structure.md`)
  — three rounds the same day, online research included —
  ADOPTED: one shared context in screenplay form; a CODE director
  in the server assembling each round (beat, speaker allowlist,
  line budget, stage direction, entropy terms) as the `user`
  directive; ONE streamed request per round for the whole exchange
  under a GBNF **screenplay grammar** (NOT JSON — the owner's
  reason: the grammar must not confine the model to the JSON it saw
  in training; the mask removes only structure tokens, the
  CONDITIONING on a JSON-looking prefix is what flattens prose);
  the server parses at line breaks and emits the browser's existing
  SSE events per speaker line — browser untouched. The sanitizer
  patch is MOOT (no label to strip). Research settled two red
  flags: llama.cpp applies the grammar in the sampler on every
  token regardless of `stream` (read in
  `tools/server/server-context.cpp`, `process_token()`: the flag
  gates only `send_partial_response`); and Instructor-style
  libraries are not needed (the constraint is server-side). A
  bounded non-spoken scratchpad line is a REGISTERED HYPOTHESIS
  (follow-ups), not part of the decision.
- **The story-loop discussion** (`2026-09-21-story-loop.md`) —
  DECIDED: Placement 1 — the BROWSER is the metronome (a separate
  `/show` page with `show.js` requests the next round when the
  audio queues drain), the SERVER is the director
  (`POST /api/show/round`); endless loop; interaction beats on a
  randomized, configurable TIME window measured in played seconds
  (min/max; probability rising between; NEVER a round count — owner
  pushback: rounds are seconds long and every listening window is a
  pause the audience hears); half-duplex HOLD-TO-TALK mic enabled
  only in the listening state; dead-air static needed the day the
  cadence is tuned; prefetch and the 1930s-radio look are polish.
- **ADR-0002** (accepted): fork TalkWithMe as TalkWithZombies,
  diverging, two sibling repositories. **ADR-0003** (DRAFT, gated —
  tonight's work is its gate). ADR-0001 annotated.
- **The answer pass closed every ledger item** (rulings 2026-09-22):
  S1 resolved (per-request reference upload stays; bandwidth
  only); S2/S6 resolved in principle (emotion = parenthetical stage
  direction in the script line; clip/knob mapping is fork work
  after Task 4); S3 DROPPED from the arc → follow-ups (the
  synthesis-time-versus-text-length measurement is for later
  tuning), provisional accumulator **N = 100** (owner: 150 too
  big); S4 parked to 5b; S5 parked post-MVP; Q5 voice-sample spec
  confirmed; Q7 Mac-local probe parked post-MVP (demo Mac 16 GB
  cannot; a 64 GB M1 could); Q9 accumulator packing rules ruled
  (§6.3); Q10 all fork knobs yaml-only; Q11 no new Node test
  harness in the timebox.
- **Repository layout ruled:** two sibling repositories; submodule,
  subtree, and file-copy rejected with reasons (TODO Task 6).
- **Follow-ups added:** tts-serve pin bump (rides tonight); TTS
  synthesis-time measurement; Mac-local MLX probe; JS test for the
  packing rules; bounded scratchpad hypothesis.

## 4. The task board — the execution order ahead (the owner-accepted decomposition)

*TODO.md is the canonical state table; this is the hierarchical
walk-through the owner asked for, with context per step. Task A
(prepare the gate offline) was MERGED INTO Task B by the owner's
pushback of 2026-09-22 ("you want to merge the grammar without
testing it in a real CUDA environment? That sounds unwise") —
draft while the box boots, prove on the box, merge what worked.*

**Task B — the ADR-0003 gate on a live box (NEXT; the box is up).**

- *Why.* ADR-0003 rests on two claims nobody has measured on our
  stack: that llama.cpp's grammar constraint works while
  streaming, and that one shared prefix beats four per-persona
  prompts on latency. Both must hold before the fork is built on
  them. The gate needs only llama.cpp; the TTS measurement was
  deferred.
- *Steps.*
  1. Bump the tts-serve pin to `"1.2"` in
     `deploy/ansible/inventories/common_vars.yml`.
  2. `make ans-set ENV=cloud IP=<ip>` (owner supplies the IP; never
     write it in markdown). `make ans-deploy ENV=cloud` from zero
     (~15 min, ~11 GB of models; logs under
     `~/.config/zombie-radio/logs/`); re-run must be `changed=0`;
     `make check` shows three ok lines through the tunnel the
     owner started. Harness quirk: ansible/make commands run by
     the agent need `>"$LOG" 2>&1 </dev/null`.
  3. Draft (uncommitted) the experiment folder
     `docs/experiments/2026-09-22-adr-0003-gate/` per the
     experiments README conventions (§5.2 below): `README.md`
     (recipe + runlog), `findings.md` with verdict criteria and
     predictions FROZEN BEFORE DATA, `screenplay.gbnf`,
     `stream_check.sh`, `latency_probe.py`,
     `summarize_timings.py`, raw outputs.
  4. Run the streaming check through the tunnel (§5.3). Stop and
     think if it fails.
  5. Run the latency probe both ways, with and without the
     grammar; raw JSON to disk; the summarize script produces the
     numbers.
  6. Optional if the evening has room: the owner runs the 5c
     zero-code probes in the current TalkWithMe (one variable per
     run; protocol-lite runlog section in the arc-plan journal).
  7. Destroy the box (owner); `make ans-unset ENV=cloud`.
  8. Truth-audit ADR-0003 against the numbers → status accepted,
     or amend; delete the pin follow-up; TODO Task 6 gate status;
     arc-plan journal entry; PR.
- *Done when.* The runlog holds a verdict on each gate item and
  ADR-0003's status reflects it.

**Task C — fork TalkWithZombies (ADR-0002), ~1 hour.**

- Real GitHub fork of scorbo2/TalkWithMe; rename TalkWithZombies;
  start at tag 7.1; README with a prominent "forked from TalkWithMe
  by Steve Corbett" section and the MIT notice kept (owner: "I
  will always pay respect and attribution to upstream").
- Clone to `/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`.
- In this repo: point the Mac installer's `client_repo` /
  `client_version` / `client_dir` at the fork
  (`deploy/ansible/client-talkwithme-mac.yml:16-18`); add a pin
  variable for the fork tag the deployment was proven against; add
  the docs pointer section (design/decisions here; feature docs and
  AGENTS.md there). Installer proof: fresh install, re-run
  changed=0, app boots.
- Disable, not delete: `allow_tool_calls` false on every persona;
  `enable_persona_memories` false.

**Task D — build the show engine (the 3-day timebox; timer starts
at the fork).**

- *Exit criterion, judged on MECHANISM only:* TalkWithZombies runs
  an unattended loop of ≥10 turns with the four placeholder
  personas; speakers chosen by the new structure, not at random;
  one audience interaction beat that opens the microphone and
  absorbs the reply; sentences accumulated, not split; on the
  deployed stack through the tunnel. Placeholder voices, dumb
  dialogue, yaml-only knobs acceptable. Midpoint checkpoint at day
  1.5 (continue / scale down / stop). Fallback if missed:
  TalkWithMe 7.1 + the canned episode. Honest arithmetic: ~2 days
  engine + ~0.5 grammar + ~1 loop = 3.5 against 3; polish is the
  lever.
- *Server side (Python, the fork):* script assembler replacing
  `build_llm_messages` (system = cast sheet; history = alternating
  director directives and script lines); the code director (beat,
  allowlist, line budget, stage direction, entropy terms; the
  cadence window in played seconds); the grammar builder
  (allowlist → `speaker` alternatives; `{0,N}` line bound); one
  streamed request per round with `grammar` in the payload; the
  stream parser emitting `start`/`token`/`done`/`complete` per
  line; `POST /api/show/round` taking the room and an optional
  audience transcript (entering the directive as in-fiction radio
  traffic); tests in upstream's style (a test class feeding a
  scripted token stream, asserting events and persisted lines).
- *Browser side (JavaScript, the fork):* a new `/show` page with
  its own template including `state.js`, `tts.js`, `stt.js`,
  `persistence.js` plus a new `show.js` (state machine idle →
  generating → playing → listening; request the next round when
  the queues drain; listening only when the director asked);
  hold-to-talk replacing the toggle, enabled only in listening;
  the accumulator in `tts.js` with the ruled rules (§6.3); the SSE
  reader extracted from `sendMessage` (`chat.js:135-159`) into a
  shared function.
- *Configuration:* all knobs yaml-only — a new `show:` section
  (cadence min/max seconds, listening window); the accumulator's
  limit and tolerance next to `tts.streaming`. No dialogs.
- *Day-three polish only if the checkpoint is green:* prefetch
  round N+1 when the last line of N starts playing; dead-air static
  through a second AudioContext source while a round is in flight;
  the 1930s radio look.

**Task E — the cast (owner, in parallel; the long pole).**

- Voice samples: ~10 s of clean speech per actor (no music or
  crosstalk under the voice) + an EXACT transcript per clip (our
  engine requires the transcript and ≥2 s; LuxTTS needs none, ≥3 s,
  ~10 s clones best); Whisper on the box can draft transcripts;
  gitignore BEFORE the first file (famous-actor clips, never
  committed). A second clip per actor in another emotional
  register is optional until stage directions are wired to clip
  selection.
- Character bibles: names, personalities, quirks, voice
  descriptions; rough is fine; model-neutral; they become the
  persona directories and the cast-sheet sections.

**Task F — after the timebox.** 5c probes and 5a audition in the
new engine (grammar on/off; the scratchpad hypothesis; both
narrative-health axes); 5b TTS comparison (LuxTTS first; the
two-engine deployment shape S4); Task 7 canned episode (the seed
makes retakes reproducible) + demo-day runbook; Task 8 close ritual
(roadmap Features Shipped, task_history migration, TODO reset,
staleness sweep incl. CLAUDE.md, spec ledger audit, and ASK
PERMISSION TO DELETE THIS HANDOFF). The MassedCompute reminder
(memory file) fires after the first EXPERIMENT PR merges.

## 5. The gate experiment in detail (next session's first work)

### 5.1 The gate, as ADR-0003 states it

1. **Streaming with grammar:** `stream: true` plus a `grammar` on
   our llama-server build, one curl — constrained tokens must
   arrive in ordinary SSE chunks. Expected PASS (source-read
   evidence).
2. **Latency shape:** per-round latency of the per-persona
   structure (four different system prompts, four requests) versus
   one shared prefix (one request); and the grammar's per-token
   overhead (same prompt with/without). Convicts or paroles the
   prompt-cache argument (BELIEVED: llama-server reuses the cached
   prompt only along an identical prefix, so per-persona system
   prompts at position zero defeat it).
3. (Audition item, NOT tonight) prose quality with and without the
   grammar, same prompt and seed.

The agent's predictions, to be registered in `findings.md` before
any measurement: streaming PASSES; the shared prefix wins by a
margin that grows with history length; grammar overhead under
~10 % per token. Ask the owner for his predictions and register
them too — "predictions that die, die in public, with the reason".

### 5.2 Experiment-folder conventions that bind (docs/experiments/README.md)

- `README.md` = masthead (question, timebox, provenance links to
  TODO Task 6, ADR-0003, the prompt-structure discussion) +
  **Reproduction recipe** (living, corrected commands in order) +
  **Runlog** (append-only; every command actually run, with output,
  mistakes included; superseded commands get a ⚠ banner pointing
  at the recipe, never rewritten).
- `findings.md` = interpretation only; **verdict criteria frozen
  BEFORE data exists**, each criterion naming its consequence on
  PASS / PARTIAL / FAIL (which ADR status changes, which trigger
  fires); predictions per participant; Results filled only from
  README evidence; Verdict.
- **Every derived number comes from a committed, dependency-free
  script over the raw output files** — no human or LLM arithmetic
  in the record. Raw outputs are committed as the record of truth.
- Placeholders un-pasteable (`<PASTE-BOX-IP-HERE>`); no real IP
  anywhere in markdown (the hook does not scan `*.md`).
- The exemplar to copy: `docs/experiments/2026-09-14-talkwithme-remote-split-test/`
  (README masthead + "Execution model" + findings' pre-registered
  criteria).

### 5.3 The screenplay grammar to start from (GBNF; iterate on the box)

```
root    ::= line{1,4}
line    ::= speaker ": " text "\n"
speaker ::= "Daniel" | "Moira" | "Ralph" | "Samantha"
text    ::= [^\n]+
```

Notes: the four names are the placeholder personas the installer
seeds (`Personas/<Name>/`); the director will narrow `speaker` per
request; the `{1,4}` bound is the line budget — use the `{m,n}`
repetition form, NEVER `x? x? x?` (extremely slow sampling per the
llama.cpp grammars README). Consider `text ::= [^\n\[\]]+` to keep
bracketed labels out. On the OpenAI-compatible chat endpoint the
grammar travels in the request body: docs-say the grammars README
says "within the `response_format` body field"; the server README
lists `grammar` as a top-level field on `/completion` — TRY the
top-level `grammar` key on `/v1/chat/completions` first (llama.cpp
accepts its own extensions there), fall back to `response_format`
if it is ignored. Verify by sending a deliberately illegal speaker
list and checking the output cannot contain other names.

### 5.4 The streaming check (through the owner's tunnel)

```
curl -sN http://localhost:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d @request.json
```

where `request.json` carries `"model": "default"` (TalkWithMe's
value; check `curl localhost:8080/props` for the served alias —
the arc-plan journal recorded the Nemotron Q4_K_M alias serving),
`"stream": true`, `"messages"` = a short cast sheet as `system` +
a director directive as `user` (include `/no_think` as the persona
prompts do), and the grammar. PASS = `data:` chunks arrive one by
one, each delta a legal fragment, the concatenation parses as
1–4 `Name: text` lines. Also send `"timings_per_token": true`
(BELIEVED to exist as a llama-server extension for streaming
timings — verify; the non-streaming `/completion` response carries
a `timings` object with prompt and predicted milliseconds, which
the probe should prefer for clean numbers).

### 5.5 The latency probe (design)

- Build a growing script history: rounds 1..K (K ≈ 8–12), each
  round 4 lines of ~80 characters, deterministic text.
- **Structure A (per persona):** for each round, 4 requests, each
  with a DIFFERENT system prompt (the persona's) and the history
  rewritten TalkWithMe-style (`[Name]: text` as user turns); record
  the server's prompt-evaluation ms and predicted ms per request.
- **Structure D (shared):** for each round, 1 request with ONE
  system prompt (the cast sheet) and the history as alternating
  directive/script turns; same recording.
- Each structure with grammar OFF and ON (4 arms). Fixed seed,
  `max_tokens` small and equal, temperature equal. Warm-up request
  first. Write every raw response to
  `raw/<arm>-round<k>[-req<j>].json`.
- `summarize_timings.py` (stdlib only) reads `raw/` and prints per
  arm: prompt-eval ms per round (sum for A's four requests), total
  wall per round, tokens/s, grammar overhead % = (ON − OFF)/OFF on
  predicted ms per token. Criteria in findings reference these
  exact quantities.
- Interpretation caveat to write down in advance: `llama-server`
  runs with `--parallel 1` (`zr_llama_parallel: 1`), one slot, so
  the prompt cache is a single slot — this is exactly the
  production configuration and exactly where A's four prefixes
  should thrash.

### 5.6 Box facts you will need

- Ports and binding: loopback on the box; through the tunnel they
  appear on the laptop's localhost with the same numbers (8080 /
  8001 / 8002). `make check` prints three ok lines.
- llama.cpp: image `ghcr.io/ggml-org/llama.cpp:server-cuda`
  (floating tag), model
  `bartowski/nvidia_NVIDIA-Nemotron-Nano-9B-v2-GGUF:Q4_K_M`,
  `n_ctx 16384`, `ngl 99`, `parallel 1`. Server sampler defaults
  read 2026-09-19 via `/props`: temp 0.8, top_k 40, top_p 0.95,
  min_p 0.05, repeat_penalty 1.0 (off), DRY off, mirostat off.
- The trio idles at ~12.3/48 GiB on an A6000; first deploy ~15 min;
  reboot auto-rise < 1 min; boxes are DISPOSABLE (rebuild is one
  command); never argue for keeping a box alive on rebuild-cost
  grounds; on-demand only.
- CUDA rule (survey §S5): the driver's CUDA version is a MAXIMUM;
  cu128 wheels run on R550/12.4 (proven); never cross a CUDA major
  casually. R550 is fine for tonight (llama.cpp only); the TTS
  comparison (5b) wants R570 so all engines compete fairly.
- Two live-only bugs of 09-19 to remember as doctrine (shape doc
  §14 postscript): awk early-exit under pipefail → SIGPIPE; complex
  Jinja inside `assert.that` silently passed a false assertion —
  precompute in `vars`, keep `that:` trivial.
- Make cheat-sheet: `make install` · `make ans-deps` ·
  `make ans-set ENV=cloud IP=<ip>` · `make ans-deploy ENV=cloud` ·
  `make check` · `make ssh-tunnel ENV=cloud` (OWNER runs it) ·
  `make ans-unset ENV=cloud` · `make ans-lint` (must stay clean at
  `production`) · `make ans-check-syntax ENV=x` · `make client-mac`.

## 6. The adopted design, compact (so you can reason about the fork without re-reading everything)

### 6.1 Prompt structure (ADR-0003 points 1–5; prompt-structure §8–§9)

- `system` = cast sheet (one section per character, the bibles) +
  show rules + format ("write the next lines as `Name: line`").
- `user` = the DIRECTOR's directive for the round: in-fiction
  traffic (what the audience said), stage direction, entropy terms,
  speaker constraints in words (aligned with the grammar).
- `assistant` = the script lines. History = these turns repeated.
  No `[Name]:` rewriting anywhere; the transcript IS the script.
- Speaker choice in layers: the code director sets the allowlist
  (who is eligible, who was addressed, who has been silent, how
  many lines; in an interaction beat only the operator), the
  grammar enforces it, the model chooses within it.
- Whole exchange per call, capped, streamed; the server parses at
  newlines and emits the existing SSE events per line; the browser
  is unchanged.
- The grammar is a PLAY, not JSON. Stage directions in
  parentheses (`Moira (whispering): …`) from a small enum carry
  the emotional register (S6's channel).
- Why (the seven factors, prompt-structure §9): removes C1/C2/C3/
  C6/E1 by construction and gives E2/E3 an owner; the wire format
  cannot break without a client library; the prose distribution
  stays the model's; best latency shape (one eval, one prefix);
  bounded build with the browser untouched; the owner's 2024
  design kept where it worked and fixed where it broke; and "it's
  the coolest approach from the technical side" (owner, recorded as
  a real factor).
- Risks (ADR-0003 Consequences): identity bleed C4 (bibles,
  audition, stage tags); prose flatness (audition); grammar
  overhead 1–20 % reported; truncation at `max_tokens` cannot be
  closed by the grammar (line-oriented format loses one line); the
  growing script versus the window (director curates); model fit
  (a shortlisted model, Rocinante, is tuned on a character-turn
  format).

### 6.2 Story loop (ADR-0003 points 6–9; story-loop §5–§9)

- Browser = metronome (`/show` page, `show.js`; states idle →
  generating → playing → listening; request the next round when
  the audio queues drain — the queues live in `state.js:43-46`,
  drained by `tts.js:136-150`). Server = director
  (`POST /api/show/round`).
- Endless loop; interaction beats on a randomized time window in
  played seconds (min/max, probability rising between; knobs
  yaml-only in a `show:` section). NEVER a round count.
- Half-duplex by construction: the mic opens only in the listening
  state with empty queues; hold-to-talk (press = record, release =
  end). Programmatic mic opening (2024-style) is feasible after
  the first permission grant (believed) — post-MVP.
- Separate page; the chat UI stays as the rehearsal/debug tool.
  Dead air = second AudioContext buffer source, needed when the
  cadence is tuned; prefetch = polish.

### 6.3 The accumulator rules (ruled 2026-09-22 — the agent once wrongly said it was not needed; it IS)

Under the new engine the server still emits `token` events per
script line and `tts.js` still cuts sentences from them with the
regex `/[^.!?]*[.!?]+/g`, so "Dr. Byrne. 47. Microbiology. Over."
would still be five requests without an accumulator. Rules:

- N is a PACKING limit, never a truncation: whole sentences only.
- Provisional **N = 100** characters; **tail tolerance ~20 %**
  (chunk may reach 120); **tail threshold ~30** characters.
- (1) Sentence arrives, chunk empty → it goes in whatever its
  length; a single 180-char sentence is sent whole, alone.
  (2) Chunk has content → append if chunk+sentence ≤ N; else if the
  sentence is under the threshold and total ≤ 1.2·N, append anyway
  (built for "Over."); else FLUSH the chunk and start a new one.
  (3) The LINE END (speaker change) is a hard flush.
- "Flush" = one call to the existing
  `enqueueStreamingTTS(persona, chunk)`, which pushes onto the
  existing `ttsRequestQueue` array and returns; fetch and playback
  already run concurrently. State = two strings (partial-sentence
  buffer + current chunk); NO new queue.
- The two 2024/2026 symptoms of the per-sentence split: an ECHO
  only when "1." was synthesized alone; long unnatural PAUSES for
  "Dr.", "2.", "3." (each fragment pays a full request round trip
  + the 80 ms inter-buffer gap). Lone one-word lines ("Over.") go
  as is; whether a lone digit still echoes is an audition item.

### 6.4 ADR-0002 essentials

Real fork, renamed, provenance labeled; two sibling repos; installer
variables + a proven-version pin + a docs pointer are the glue;
memories/tools disabled not deleted; contribution ledger:
deployment machinery first, accumulator second, sanitizer dropped;
outreach deferred past the deadline.

## 7. Cold-start reading order (the repo is the memory of record)

1. `CLAUDE.md` → `docs/README.md` (conventions; the arc lifecycle;
   the close ritual; cross-reference legend).
2. `docs/TODO.md` — canonical state; read the arc-boundary note,
   Task 6's revised disposition (fork, gated patches, timebox,
   repository layout), the owner action queue (voice-sample spec).
3. `docs/decisions/0003-adopt-shared-context-screenplay-engine-with-browser-clocked-director.md`
   (DRAFT, gated — tonight's work) and
   `0002-fork-talkwithme-as-talkwithzombies-in-a-sibling-repo.md`;
   `0001` for the foundation bet and its annotation.
4. `docs/discussions/2026-09-21-prompt-structure.md` (§7 research,
   §8 assembly, §9 case, §11 gate) and
   `2026-09-21-story-loop.md` (§1 verbatim options, §9 rulings).
5. `docs/discussions/2026-09-21-task6-reconnaissance-brief.md` —
   §5 seam ledger, §5b question index, §8 C1–C10 revisited, §9
   synthesis; then the two tours as REFERENCE (every claim with an
   absolute path and line number against TalkWithMe 7.1 and
   tts-serve 1.2).
6. `docs/experiments/README.md` + the remote-split experiment folder
   (the format exemplar for tonight's folder).
7. `docs/discussions/2026-09-18-mvp-prototype-arc-plan.md` — Task
   notes + dated journal (the 09-19 entry and addenda hold the
   deployment science; the recon block holds the brief's rulings).
8. `docs/discussions/2026-09-17-ansible-deployment-shape.md`
   §14–§15 (CUDA preflight; SSH doctrine);
   `2026-09-13-cloud-gpu-provider-survey.md` §S2 (box-birth ritual)
   and §S5 (the CUDA rule).
9. `docs/specs/product-definition.md` — §3 architecture, §4 model
   stack, §5 (5.1 baseline correction; 5.3 director), §6 deployment
   as-built, §7 experiments, §10 security posture.
10. `docs/discussions/2026-09-16-storytelling-coherence-and-structure-adherence.md`
    — the taxonomy (A1–E3); the vocabulary every design argument
    uses.
11. `docs/follow-ups.md` (five entries touched this session);
    `docs/roadmap.md`; runbooks (`service-restart-sequence.md`,
    `box-inspection.md`).

## 8. Watch-list and nuances hard to grasp from the documents alone

- **The prompt-cache claim is BELIEVED, not measured** — it is one
  of the two things tonight measures. Do not state it as fact
  before the numbers exist.
- **`timings` fields:** the `/completion` endpoint returns a
  `timings` object; whether `/v1/chat/completions` returns timings
  while streaming (`timings_per_token`) is believed — verify, and
  prefer the endpoint that gives clean numbers even if the
  production client uses the other.
- **Where the grammar goes on the chat endpoint** (`grammar` key
  vs `response_format`) — try, verify, record in the recipe.
- **The never-commit hook skips markdown** — the box IP in a
  runlog would commit. Discipline, not tooling, protects it.
- **A40 vs A6000:** same chip family, same 48 GB; the owner got an
  A6000 tonight. An A4000 (16 GB) ran the trio in the spike and
  would suffice for a llama.cpp-only gate.
- **The owner's Macs:** the demo laptop is an M1 16 GB (cannot run
  the stack); a second M1 with 64 GB exists (the post-MVP MLX
  probe target).
- **tts-serve 1.1 → 1.2 diff = the MLX engine only**; LuxTTS has
  been in since 1.1 (checked in the tagged trees; the owner
  doubted it — receipts in the tts-serve tour §1).
- **Upstream conventions are knowledge, not constraints** now
  (ADR-0002) — but keep upstream's hermetic pytest suite and
  AGENTS.md meaningful inside the fork: every change with a green
  suite; the endpoint table is under test.
- **Both patches' fates:** sanitizer NOT built (moot); accumulator
  built with the ruled rules; the accumulator as an UPSTREAM offer
  (per-sentence → max-chars for TalkWithMe's own pipeline) is a
  separate, later thing.
- **The entropy-term terminology** is fixed: "entropy terms" (the
  words) and "entropy-term injection" (the mechanism); the 2024
  baseline is the COMMITTED version (one adjective list, random
  emotion and word count, hidden narrator), not the richer
  remembered one — spec §5.1 was corrected.
- **The brainstorm's C1 problem the code surfaced:** TalkWithMe's
  STT proxy substitutes "No response received from STT server"
  for an empty transcript and the browser auto-sends it as the
  user's message — the show page must drop empty/low-confidence
  transcripts at the proxy. Whisper's `prompt`/`language` fields
  are unsent today — a cheap fix for proper names (C6), a fork
  candidate.
- **Dialogue quality is DUMB by design** until 5a picks a model —
  the audition's mandate, not a bug to fix tonight.
- **Fresh-path doctrine:** no in-place downgrades in venvs — delete
  and reconverge.
- **The owner's late-night mode:** shorter turns, one question at
  a time, and check the previous ruling before asking the next.

## 9. Paste-ready re-orientation prompt (for the FIRST message of the new session)

```
We are resuming the Zombie-Radio project (MVP-prototype arc) in a
FRESH session after the previous one ended. Nothing from that
session persists except the repo, your memory files, and the
handoff document written for you. Re-orient now:

1. Read docs/discussions/2026-09-22-adr-0003-gate-session-handoff.md
   IN FULL — it is your session memory bank: who I am and how we
   work (§0 is binding, including the live-box drill rules),
   project + arc state, the task board (§4), and your first task:
   the ADR-0003 gate experiment on the live box (§5).
2. Follow its cold-start reading order (§7) as far as needed to
   confirm state — at minimum: docs/TODO.md, ADR-0003, the
   prompt-structure and story-loop discussions' decision sections,
   docs/experiments/README.md, and `git log --oneline -5`. Work
   continues on the already-created branch `alfre2v/adr-0003-gate`
   (verify you are on it; never create a new branch).
3. Then confirm to me in a compact summary: where the arc stands,
   the execution order ahead, the gate experiment's plan (the
   folder, the frozen criteria, your predictions, the exact first
   commands you will run through my tunnel), and the collaboration
   rules you will operate under. Ask me for the box's status and
   IP; never write the IP into any markdown file.

Do not start any work until I confirm your summary. My standing
rules: strict review-before-commit (I review uncommitted changes
in VS Code — no diffs in chat, no commits without my explicit
word), no AI attribution anywhere, no side panes, minimal code
comments, discussion-first shape rounds, pushback with receipts
welcome, plain language over clever phrasing, one question at a
time when I say I am tired.
```

## 10. Small print the next agent should not miss

- Deadline math: 2026-10-08 is 16 days out. The critical path is
  the owner's cast (Task E) and the 3-day timebox (Task D); the
  gate (Task B) is one evening and unblocks the fork.
- The spec is a LEDGER: settled decisions get their as-built entry
  within a session. ADR-0003's acceptance is such a decision — the
  spec §5.3 director section will want a ledger line when the fork
  runs.
- Experiment PRs (tonight's gate counts as one) trigger the
  MassedCompute reminder (memory file): one gentle line after the
  merge.
- Never argue for keeping a box alive; destroy when the evening
  ends; `make ans-unset ENV=cloud` returns the working tree to
  clean.
- Handoff hygiene: at the end of the session this document serves,
  ASK PERMISSION to delete it.
