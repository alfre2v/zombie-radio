# Storytelling coherence & structure adherence — the two axes of narrative health

**Date:** 2026-09-16 · **Arc:** Product definition (born inside
Task 3a, but deliberately promoted OUT of the experiment folder:
this question is central to the app and outlives any one
experiment)
**Type:** taxonomy + terminology (TWO named properties of the
system, the map they span, and the catalogue of ways they fail)
**Status:** v2, same day as v1 — v1 named a single property
(structure adherence); the lab3 dialog-state specimen (§4)
forced a second, orthogonal axis (storytelling coherence) within
hours. The rework is the finding. Cross-links: brainstorm
challenges C1–C10 · remote-split runlog (step 6 entries) ·
findings.md measure (e) · [discussion 2026-09-14] (LLM survey;
the Track 3 audition should adopt axes from §5 here).

*Context for the cold reader: Zombie-Radio is theatrical live
improvisation — four LLM personas performing a radio-play
fiction under a format (radio protocol), as distinct characters,
inside a story arc. The show only works if the performance stays
HEALTHY across a whole session. During the remote-split spike
the cast visibly failed in several distinct ways, which forced
the question this document answers: what ARE the properties
being violated, and what are all the ways they can fail?*

## 1. The two properties being named

The problem space turned out to need two axes, not one. Together
they span what this document calls **narrative health** — the
joint property an episode must hold to be a show.

### 1.1 Axis 1 — Structure adherence

**Structure adherence: the cast's obedience to the DECLARED
scaffold — the show's format, character identities, and intended
arc, as specified in prompts and conventions.** Colloquial
alias: **show discipline** ("Daniel broke show discipline").
Adherence is measured against something written down; its
failures are violations of a rule we can point to.

It decomposes into three layers:

| Layer | What must hold | Observed violations (receipts) |
|---|---|---|
| **Format** | The surface protocol: radio style, "Over.", no `[Name]:` labels spoken aloud, reply length appropriate to a transmission | Label mimicry (runlog 2026-09-16, step 6 first contact) |
| **Identity** | Each actor stays a distinct, consistent character — voice, knowledge, quirks | Daniel self-labeling with his surname (learned convention, not copying); voice-homogenization risk (§3 C4) |
| **Arc** | The performance serves the intended dramatic shape: acts, beats, scene goals as scaffolded | No clean specimen yet — placeholder personas carry almost no declared arc to violate |

### 1.2 Axis 2 — Storytelling coherence

**Storytelling coherence: the EMERGENT property that the
performance hangs together as one story — independent of any
declared rule.** Coherence is not obedience; nothing in a prompt
can fully specify it. It is measured against the story itself:

| Facet | What must hold | Observed violations (receipts) |
|---|---|---|
| **Dialog-state liveness** | Every speaker tracks which question/task is currently live | **The founding specimen (lab3, 2026-09-16):** asked for a five-sentence report, Ralph and Moira answered the PREVIOUS turn's zombie-count question — with Samantha's numbers, not even their own |
| **Task execution vs meta** | An accepted task gets DONE, not described | Samantha produced a plan *for* the report instead of the report — meta-level slippage |
| **World consistency** | Facts, counts, names, and geography stay stable across speakers and turns | Ralph reporting "Six. Seven." after his own "Two. Three." one turn earlier |
| **Contribution** | Each turn advances the story rather than echoing it | The degeneration round: Moira full report → shrinking acks → Daniel's bare "Over." |

Note the re-filing this axis forces: v1 called the degeneration
round a "narrative adherence failure with perfect format." That
was the one-axis frame straining. Properly stated: **perfect
adherence, dead coherence** — every reply was impeccable radio
protocol, and the story flatlined anyway.

### 1.3 Two axes, one map

The axes are semi-independent — a performance can sit anywhere
in the 2×2:

| | **Coherent** | **Incoherent** |
|---|---|---|
| **Adherent** | The show works | The degeneration round; the lab3 specimen — flawless "Over."s, no story |
| **Non-adherent** | `[Hayworth]:` prefixes in an otherwise-tracking dialogue — the show limps but lives (sanitizer-fixable) | Collapse |

And they are COUPLED, with field evidence: the lab3 A/B showed
that an adherence lever (the anti-label Global System Prompt, a
FORMAT instruction) damaged coherence (dialogue quality dropped
with the prompt in place). Levers pulled on one axis can move
the other, which is exactly why both must be on the map before
any tuning: optimizing adherence blind cost us coherence once
already.

Practical asymmetry worth recording: adherence failures are
CHEAP to patch mechanically (sanitizers, format levers) because
the rule is explicit; coherence failures are the expensive kind
— they implicate context assembly, model capability, and
orchestration (§3), and no output filter can restore a lost
dialog state.

## 2. The struggle to refine the terminology

*Recorded because the naming WAS the analysis — the owner asked
that the refinement effort itself be kept.*

### Round 1 — from "consistency" to "adherence" (v1)

The owner's starting formulation: **"modes of failure in
storytelling structure consistency"**, offered with the framing
question *"why would the model fail to follow the structure of
our storytelling exercise?"* and three candidate causes:
(a) poor model quality, (b) poor instructions, (c) the model not
receiving proper speaker identifiers.

Two refinements were made to that formulation:

**Refinement 1 — the property is adherence, not consistency.**
"Consistency" undersells the problem: a model can be
*consistently* off-structure (a cast that always speaks in
formal prose is perfectly consistent and completely off-format).
The property v1 named is **adherence** — staying ON the declared
structure.

**Refinement 2 — "storytelling structure" is three structures
wearing one coat.** The original phrase reads as one
undifferentiated blob. Decomposing it into format / identity /
arc layers (§1.1) turned a vague worry into a diagnostic
instrument. The owner's causes (a)–(c) also turned out to live
at different loci — (a) model capability, (b) instructions,
(c) context assembly — which seeded the locus grouping in §3.

**Ranked terminology candidates considered in round 1:**

1. **"Structure adherence"** — CHOSEN for axis 1. Short,
   layer-neutral, names the property itself, so derived phrases
   stay natural: "structure-adherence test",
   "structure-adherence budget".
2. **"Show discipline"** — the in-domain, memorable version.
   Adopted as the informal alias; slightly too cute as the
   primary technical term.
3. **"Narrative adherence"** — cleaner English, but it
   privileges one layer and would mislabel the label-mimicry
   finding (a format failure).
4. **"Theatrical structure adherence"** — precise but a
   mouthful; retained as the expanded first-mention form of #1.
5. **"Storytelling structure consistency"** (original) —
   workable, but "consistency" is the weaker property and the
   phrase doesn't decompose.

### Round 2 — the owner's "storytelling coherence" splits the space (v2, same day)

Hours after v1, the owner floated **"storytelling coherence"**
as an alternative name for the whole problem. The agent's first
instinct was to rank it below "adherence" as v1 had ranked
"narrative adherence" — and that instinct was WRONG in an
instructive way. Working the distinction honestly:

- **Coherence names an emergent property** — does the story hang
  together — measured against the story itself.
- **Adherence names obedience** — is the declared scaffold being
  followed — measured against a written rule.

Neither subsumes the other, and the day's specimens sorted
themselves cleanly: label mimicry is pure adherence-failure
(rule violated, story intact); the stale-question round is pure
coherence-failure (no rule violated — no rule COULD express
"track the live question" — story broken). The degeneration
round, awkward under one axis, is natural under two: adherent
and incoherent.

So the owner's "alternative terminology" was not an alternative
at all — it was the missing second axis. The resolution:
**keep both terms, as dimensions of one map (narrative
health)**, rather than crowning either. The v1 → v2 rework of
this document is the record of that resolution.

## 3. Taxonomy of failure mechanisms

The owner's (a)–(c) and the agent's mechanisms, merged and
de-duplicated, grouped by **locus** — where in the stack the
cause lives. Each entry: mechanism → **axis** (adherence /
coherence / both) and layer/facet attacked → evidence so far →
testability.

### Locus A — model capability

- **A1. Raw model quality** *(owner's (a))*. A 9B model may
  simply lack the capacity to juggle persona + format + story
  simultaneously. Axis: BOTH. Evidence: none isolated yet —
  every observed failure has a competing explanation below.
  Test: the LLM audition (Track 3) across the ranked shortlist;
  if all five fail the same way, the cause is probably NOT A1.
- **A2. Quantization damage** — distinct from A1: the *same*
  model at Q8/fp16 might hold structure fine. Instruction
  adherence and long-form coherence both degrade faster under
  aggressive quant (we run Q4_K_M) than surface fluency does —
  the model still *sounds* good while quietly failing on both
  axes. Extra exposure: Nemotron's `nemotron_h` hybrid-Mamba
  layers are recent in llama.cpp; quant quality for state-space
  blocks is less battle-tested. Axis: BOTH. Test: same model,
  same prompts, Q4 vs Q8 on the 3090 (audition axis).
- **A3. Reasoning-off cost.** We run Nemotron with `/no_think`
  because latency demands it — but tracking dialog state,
  planning a five-sentence report, and knowing what THIS line
  must do are planning-shaped work, precisely what the reasoning
  pass buys. We amputated the model's planning to make it fast.
  Axis: COHERENCE above all (Samantha's plan-instead-of-report
  is the signature move of a model that can't plan silently);
  adherence second. Test: `/think` vs `/no_think` comparison
  (audition axis; latency disqualifies `/think` for the show,
  but the delta measures what reasoning was worth).

### Locus B — instructions

- **B1. Poor or under-specified instructions** *(owner's (b))*.
  The persona prompts are placeholders; the scaffold is
  described, not operationalized (no examples of a GOOD round,
  no explicit "when you have nothing to add, do X"). Axis:
  ADHERENCE primarily — instructions can only declare scaffold;
  coherence can't be fully specified by prompt (§1.2). Test:
  iterate prompts against a fixed scenario — cheap, but
  confounded with everything below, so test LAST, not first
  (the instinct to "just fix the prompt" hides mechanical
  causes).
- **B2. Instruction dilution / attention decay.** The persona
  prompt sits at position zero; the transcript grows toward the
  16k window. Lost-in-the-middle attention effects plus simple
  ratio (200 tokens of instruction vs 10,000 of chatter) mean
  the scaffold fades exactly when the episode needs it most —
  late. Axis: ADHERENCE, with a time signature (decay over
  session length). Test: measure adherence early vs late in a
  long soak (the broadcast-soak creative test doubles as this).
- **B3. Instruction stacking / cross-axis interference.**
  Prompt assembly is persona `prompt.md` + Global System Prompt
  + `/no_think` line; every lever added competes for a small
  model's limited instruction-following budget — and levers
  pulled on ONE axis can damage the OTHER
  (**field-observed:** the anti-label prompt, a format-adherence
  lever, degraded coherence; lab3 A/B, §4). Axis: the coupling
  channel between the two. Test: ablate levers one at a time in
  fresh rooms — the lab2/lab3 pattern, generalized.
- **B4. Format–task conflict: the scaffold itself forbids the
  task.** Field-observed in the report round: the radio format
  demands telegraphic brevity ("Two. Three. Shamblers. Over."),
  the task demanded ≥5 sentences — and **adherence won**: not
  one persona produced five sentences; the closest (Samantha)
  spent hers on a plan. Distinct from B3: this isn't two
  instructions colliding in the attention budget, it's the
  DECLARED FORMAT being intrinsically anti-task — the two axes
  competing for the same tokens, and the trained-in/prompted-in
  brevity prior outranking an explicit, recent instruction.
  Axis: COHERENCE (task execution), suppressed BY adherence.
  Test: same report request with an in-format escape hatch
  ("long-form transmissions are authorized for official
  reports") vs without.

### Locus C — context assembly (the transcript as an actor)

- **C1. Missing/weak speaker identifiers** *(owner's (c))*.
  Partially SUPPORTED by lab3: identity signals in context are
  load-bearing; suppressing the label convention (even only in
  output) correlated with worse dialogue. Axis: COHERENCE
  (dialog state needs to know who said what) + identity
  adherence. Standing consequence: the strategy flips to
  allow-labels-in-context + output sanitizer before TTS (the
  fork-trigger firebreak patch).
- **C2. Two-role chat template misfits a four-actor play** —
  the structural cousin of C1, but distinct: the chat template's
  ontology has only user/assistant, so each persona sees the
  other three as USER-role messages (`app/session.py:135/159`).
  The model's training says "user messages are the human I
  serve," and three-quarters of its world arrives wearing that
  costume; consecutive user-role messages (out-of-distribution
  for alternating-turn training) tend to fuse, with attention
  going to the LAST one. Axis: COHERENCE primarily. Test: hard
  to A/B without patching prompt assembly (adaptation-arc
  experiment: single-completion "screenplay mode" vs per-persona
  chat mode).
- **C3. Examples beat instructions — transcript contamination,
  generalized.** Field-proven with labels (runlog 2026-09-16):
  whatever pattern appears in recent history becomes an
  in-context few-shot that outweighs the system prompt, and it
  compounds — each slip re-seeds itself. This is why the
  degeneration was *progressive*: every short reply taught the
  next speaker to be shorter, and why Ralph reported SAMANTHA's
  zombie count. Axis: BOTH; the amplifier for every other
  mechanism. Mitigation shape: fresh-room hygiene now;
  transcript curation/summarization later (adaptation arc).
- **C4. Persona voice homogenization.** All four share one
  transcript, so each persona's in-context examples are mostly
  OTHER personas; styles converge toward whoever talks most.
  Axis: identity ADHERENCE. Evidence: none clean yet
  (placeholder personas are too thin to diverge much — the
  character bibles will make this measurable). Test:
  style-distinctiveness check late in a long session.
- **C5. Context-window mechanics.** llama.cpp context-shift /
  eviction when the window fills can drop early tokens; if the
  system prompt isn't pinned, the scaffold literally leaves the
  building mid-session. Axis: BOTH, cliff-edge time signature
  (sudden, not gradual). Test: verify llama-server's
  prompt-retention behavior at window overflow before any long
  soak.
- **C6. The invisible director.** Field-observed 2026-09-16,
  receipt `app/session.py:147-148`: the human user's messages
  keep role `user` with NO prefix and no identity — only
  PERSONAS get `[Name]:` labels. So the one voice whose
  instructions should outrank everything is the only participant
  with no name, one anonymous line drowned between labeled,
  longer, more locally salient dialogue turns. The lab3
  stale-question specimen is this mechanism's signature: the new
  instruction lost the attention contest to `[Samantha]:`'s
  adjacent turn. Axis: COHERENCE (dialog-state liveness — the
  live task never registers). Test: zero-code — the owner
  manually prefixes his typed messages with a marker (e.g.
  `[Director]: …`) and repeats the two-round protocol; if
  stale-question answering drops, C6 is convicted.
- **C7. No per-persona world state — facts belong to the
  transcript, not to the observer.** Field-observed: Ralph
  reported "Six. Seven." — SAMANTHA's round-1 count, after his
  own "Two. Three." one turn earlier. Mechanism: a persona's
  only scene memory IS the shared transcript; there is no data
  structure distinguishing "what I saw" from "what someone
  said," so every stated fact is equally available to every
  speaker as their own. (TalkWithMe's persona-memories feature
  is long-term character memory, not per-scene observational
  state — it doesn't cover this.) Distinct from C3: imitation
  explains COPYING a style; C7 explains a persona sincerely
  ADOPTING another's observations as its own — no amount of
  anti-imitation prompting gives Ralph a place to keep his own
  zombie count. Axis: COHERENCE (world consistency) + identity.
  Test: give two personas contradictory private facts via their
  prompt.md files, then ask each to report — do the facts stay
  with their owners?
- **C8. No diegetic/meta channel separation — stage directions
  arrive as radio traffic.** The director's messages mix two
  levels with no marking: in-fiction content ("how many zombies
  do you see") and out-of-fiction stage direction ("it must be
  at least five sentences long. Please proceed"). A character
  inside the fiction cannot coherently "hear" a sentence-count
  requirement over the radio — the cast must silently infer
  which level each utterance lives on, per utterance. Related to
  C6 but orthogonal: C6 is about WHO is speaking (the director
  has no name); C8 is about WHICH WORLD the message belongs to —
  a labeled director message would still be ambiguous between
  "order from HQ (in-fiction)" and "note from the show-runner
  (out-of-fiction)." Axis: COHERENCE (dialog-state + task
  execution). Test: rephrase the same task fully in-fiction
  ("HQ demands a five-line incident report, read it on the
  net") vs the meta phrasing — zero code.

### Locus D — decoding / serving parameters

- **D1. Sampler settings fight the show.** We have never audited
  what temperature/top_p/repeat_penalty TalkWithMe sends. A
  repetition penalty actively *punishes* format adherence —
  radio protocol REQUIRES repeating "Over.", call signs, and
  boilerplate every turn — while low temperature encourages the
  echo-collapse that kills coherence. Axis: BOTH, via different
  knobs. Test: cheapest in the whole taxonomy — read the request
  TalkWithMe sends (one look), then sweep.

### Locus E — orchestration (the machinery around the model)

- **E1. Routing conscripts speakers who have nothing to say —
  and conscripts them AT RANDOM.** Receipt sharpened by source
  audit (`app/routers/chat.py:254-261`): only the FIRST speaker
  of a round is picked by the configured strategy ("LLM
  decides"/router); replies 2..N are **`random.choice`** among
  the personas who haven't spoken. The report round was one
  chosen speaker plus three random draftees, each handed the mic
  after the task might already be done — Daniel's bare "Over."
  may be the *correct* utterance for a station with nothing to
  add; the failure is the director's, not the actor's. A real
  radio net wouldn't make all four stations report when one
  report covers it. Axis: COHERENCE (apparent contribution
  failure), caused upstream of the model entirely. Test: repeat
  the report round with `max_persona_replies: 1` / routing fixed
  to a single responder.
- **E2. Unaddressed tasks — everyone's job is no one's job.**
  The report request named no addressee, and the machinery has
  no addressee-resolution step (the router picks who SPEAKS
  first, not who OWNS the task). Each conscripted persona must
  privately guess whether the task is theirs; the observed round
  is four different guesses: Samantha resolved the ambiguity by
  coordinating ("I'll compile the data"), Ralph and Moira by
  treating it as not-mine-so-repeat-the-net-status, Daniel by
  protocol filler. Classic diffusion of responsibility, executed
  by language models. Distinct from E1 (being forced to speak)
  — E3 is not knowing what speaking is FOR. Axis: COHERENCE
  (task execution + contribution). Test: zero code — address the
  task to a named persona ("Moira, write the report") and
  compare against the unaddressed phrasing.
- **E3. Nobody owns the story.** The deepest one. TalkWithMe is
  a chat app; the theatrical structure exists ONLY as prose
  inside persona prompts, and NOTHING tracks story state — no
  stage manager holding acts, beats, scene goals, or the live
  task. We ask a 9B model to implicitly be its own director
  across turns. Coherence drift is not a malfunction; it is the
  DEFAULT OUTCOME of an architecture with no component whose job
  coherence is. This is what the spec's post-MVP "hybrid
  trajectory scaffolds" idea exists for; the spike's evidence
  suggests scaffolding may migrate from nice-to-have toward
  load-bearing. Axis: COHERENCE, and eventually everything (an
  unmanaged story starves adherence of material too).

*Ruled OUT by the same source audit (recorded so it isn't
re-suspected): round-generation concurrency. Replies within a
round are serial and each speaker's context "already includes
prior personas' replies" (`app/routers/chat.py:296`). Later
speakers in the report round genuinely SAW Samantha's plan —
which makes the echoes a C3/C7/E2 story, not a stale-snapshot
artifact.*

## 4. Evidence ledger (what's field-observed vs suspected)

- **lab3 A/B, round 1 (2026-09-16, owner-run):** fresh room
  WITHOUT the Global System Prompt, identical ≥5-sentence report
  request → dialogue held up better. Per the pre-wired
  discriminator: health implicates the prompt → **B3
  field-observed** (an adherence lever damaged coherence — the
  coupling evidence of §1.3) and **C1 supported**. The agent's
  task-convergence hypothesis (C3+E1 as sole cause) is
  **wounded — graded honestly**: implicated-not-convicted caveat
  stands (single trial). Standing consequence adopted: allow
  labels in context, strip before TTS (sanitizer firebreak).
- **lab3 two-round specimen (2026-09-16, owner-run) — the
  founding specimen of the coherence axis.** Round 1
  ("report how many zombies you see"): all four answered
  correctly, in character, in format. Round 2 ("write a report,
  at least five sentences"): Samantha produced a PLAN for the
  report instead of the report (A3 signature, resolving E2's
  who-owns-this ambiguity by coordinating); Ralph and Moira
  answered the STALE round-1 question — with Samantha's numbers,
  not their own (C6 + C3 + C7); Daniel degenerated to protocol
  filler (E1/C3); nobody produced five sentences (B4 — the
  format's brevity prior beat the explicit instruction). Perfect
  adherence throughout — the failure is invisible to any format
  check. One specimen, SIX suspected mechanisms — the richest
  single observation of the spike. Receipts: `app/session.py:
  147-148` (unlabeled director) vs `:153-159` (labeled
  personas); `app/routers/chat.py:254-261` (random follower
  conscription); `chat.py:296` (serial rounds — the echoers SAW
  the completed task).
- **Label mimicry + transcript contamination:** field-observed
  with receipts (`app/session.py:135/159`; the lab→lab2
  fresh-room result) → **C3 proven** as a mechanism, magnitude
  TBD.
- **Group degeneration round:** observed once; re-filed under
  the coherence axis (contribution facet); attributed to some
  mix of B3/C3/E1 pending further lab3 rounds.
- Everything else in §3: **suspected**, with a named test.

## 5. Which experiments discriminate what

Ordered by cost, cheapest first:

1. **Read the sampler params** TalkWithMe sends → D1. (Minutes;
   can happen inside the current spike without scope creep.)
2. **The two-round protocol as a reusable probe, with one
   variable flipped per run** (all zero-code, all owner-typed;
   each rerun of §4's exact protocol with ONE change):
   - `[Director]:` prefix on the owner's messages → C6;
   - task addressed to a named persona ("Moira, write the
     report") → E2;
   - task phrased fully in-fiction ("HQ demands a five-line
     incident report, read it on the net") → C8;
   - in-format escape hatch ("long-form transmissions are
     authorized for official reports") → B4;
   - `max_persona_replies: 1` / fixed responder → E1.
   The unmodified protocol is the control; it has already run
   once.
3. **lab3 confirmation round** (second identical report request
   in the healthy room) → convicts or paroles B3/C1.
4. **Private-facts probe** (contradictory facts planted in two
   personas' prompt.md, each asked to report) → C7.
5. **Broadcast soak** (the "pilot episode" creative test) →
   B2's time signature + C4 homogenization + C5 cliff, all in
   one session — and the first end-to-end read on BOTH axes at
   episode length.
6. **LLM audition (Track 3)** — should ADOPT narrative-health
   axes: same scenario across the shortlist (A1), Q4 vs Q8
   (A2), `/think` vs `/no_think` (A3), lever ablation (B3) —
   scored separately on adherence and coherence.
7. **Adaptation-arc experiments** — screenplay-mode vs chat-mode
   prompt assembly (C2); transcript curation (C3); per-persona
   private facts (C7); stage-manager prototype (E3).

## 6. Open questions

- Does E3 (trajectory scaffolding / stage manager) graduate from
  post-MVP to load-bearing? The spike says "watch it"; the
  audition + soak should say yes/no before the spec freezes its
  MVP scope. The two-axis frame sharpens the question: a stage
  manager is a COHERENCE component — nothing else in the stack
  owns that axis.
- What are the cheapest metrics — one PER AXIS? (Today: the
  owner's ear for both.) Adherence is the countable one: replies
  matching radio format, labels leaked, mean reply length by
  turn index. Coherence resists counting — candidate proxies:
  stale-question answers per round, fact drift across speakers,
  fraction of turns that add information.
- Where does the sanitizer firebreak land — fork patch or
  upstream PR? (Fork strategy: defer until the first patch;
  this may be the first patch.) Same question now applies to a
  `[Director]:`-style user-message label if C6 convicts —
  another one-line session.py candidate.
