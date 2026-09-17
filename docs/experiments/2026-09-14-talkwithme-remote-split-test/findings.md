# TalkWithMe remote-split test ("the spike") — findings

**Status:** CLOSED — verdict **PASS**, 2026-09-16 (run
2026-09-15/16, inside the 2-day timebox; total cost $2.97).
Verdict criteria were frozen 2026-09-14, before any spike command
ran. Interpretation only; raw evidence lives in `README.md` (the
runlog).

## Verdict criteria (pre-registered — frozen before the data exists)

- **PASS** — all of: a 4-persona session with distinct voices is
  audible end-to-end on the laptop through the SSH tunnel;
  time-to-first-audio ≤ ~5 s per dialog line sustained over ≥10
  consecutive lines; no architectural blocker identified (an
  identified blocker = a defect that cannot be fixed with
  configuration or a localized patch).
  → **Consequence:** MVP proceeds on TalkWithMe; [ADR-0001]
  truth-audited and frozen to `accepted`.
- **PARTIAL** — the session works but with enumerable, fixable
  issues (each one listed with a rough fix shape and cost).
  → **Consequence:** proceed; the issues become TODO sub-steps;
  ADR-0001 frozen with the issues annotated.
- **FAIL** — structural localhost coupling: audio path unusable
  over WAN, pervasive blocking design, or code we cannot
  responsibly own within the deadline.
  → **Consequence:** the flip trigger fires — the MVP moves to
  Pipecat ([discussion 2026-09-13] framework survey; brainstorm
  §9 records the fallback rationale); ADR-0001 superseded.

## Predictions (register BEFORE the run; deaths recorded after)

**Agent (Claude, registered 2026-09-14):** PARTIAL, close to
PASS. Reasoning: TalkWithMe reaches model services by URL, so
the plumbing should survive relocation; but I expect 2–4 small
localhost-isms (a hardcoded `127.0.0.1` default, a timeout tuned
for LAN, a streaming buffer that stutters on first WAN jitter) —
all patchable. I put low probability on structural FAIL: the
FastAPI + browser + REST shape is WAN-shaped by construction.
Confidence: moderate. The measure I'm least sure about: (c) —
time-to-first-audio may land 3–8 s with a small LLM and one TTS
engine on an A6000, uncomfortably straddling the 5 s line.

**Owner (Alfredo):** declined to register a prediction
(2026-09-14, "I see no value in my prediction here") — noted so
the slot is closed, not forgotten. The agent's prediction above
stands alone for grading.

## Results (final — consolidated at close, 2026-09-16)

*Mapped to the pre-registered measures, from runlog evidence
only. (A preliminary snapshot written mid-experiment was
consolidated into this final section at close — findings.md is
the living interpretation, not an append-only log; the runlog
preserves the chronology.)*

- **(a) Audio over WAN — YES.** Single- and multi-persona
  sessions delivered cloned speech through the tunnel across
  multiple evenings and one hibernation cycle with no observed
  drops or stalls; streaming mode played a 6-fragment monologue
  gaplessly (client-side fetch-ahead pipeline, source-verified).
  The only audio complaints — inter-sentence pauses on short
  sentences — are per-request economics (see (e)), not WAN
  transport behavior.
- **(b) 4-persona session — YES.** The `Lab`/`lab2`/`lab3`
  group sessions ran 4 scientists with distinct cloned voices
  end-to-end (runlog step 6 entries; screenshots in owner
  archive), with routing, persona-to-persona replies, and mic
  round trips all working.
- **(c) Time-to-first-audio — PASS with data.** The harvested
  TTFA table (152 requests → 24 bursts,
  `extract_tts_timings.py`): median est. TTFA **0.9 s**, and
  **13 consecutive replies ≤ 5 s** in streaming mode — the
  ≥10-consecutive-lines clause met. Per-sentence RTF 0.46–0.64
  on normal sentences; tunnel cold-connection overhead 0.6–0.7 s,
  amortized by persistent connections. The only >5 s bursts
  (6.1–14.9 s) were the `streaming: false` A/B trials —
  **owner-confirmed** by wall-clock window (runlog post-close
  note). That A/B was itself a tested result: **non-streaming
  mode is WORSE for this show** (whole-utterance synthesis defers
  first audio; turn pipelining does not cross speaker turns) —
  streaming stays ON. All numbers carry the conservative ~215 ms
  NORWAY-1 RTT; a closer region only improves them.
- **(d) tts-serve adapter effort — ZERO.** TalkWithMe
  auto-detected the engine from `/capabilities` and rendered its
  parameter schema in the UI. The real integration cost was
  environment, not code: the documented potholes (apt packages,
  numpy-before-sox, `transformers==5.15.1` pin) in the runlog's
  deployment ledger.
- **(e) Architectural red flags — collected; NONE structural.**
  All are configuration-level or upstream-improvable:
  - Reference audio re-uploaded per sentence (~300 KB; stateless
    API; WAN tax; `app/routers/tts.py:134`) — combined with the
    naive sentence splitter (splits at every period, "Dr."
    included) this makes effective RTF > 1 on short sentences,
    and radio style is made of short sentences.
  - Sentence-chunked synthesis severs prosodic continuity
    (→ brainstorm C10).
  - Group-history format induces speaker-label mimicry: other
    personas injected as `[Name]:`-prefixed user messages
    (`app/session.py:135/159`); one leaked label re-seeds the
    convention permanently (transcript contamination — examples
    beat instructions). The human director is the only UNLABELED
    participant (`session.py:147-148`), implicated in
    stale-question answering; and the anti-label prompt lever
    itself degraded dialogue quality (lab3 A/B) — the sanitizer,
    not the prompt, is the right fix.
  - `max_turns_for_context: 6` (app-side, counted in single
    messages) = amnesia-by-design in a 4-persona room; we
    provision 16k tokens of LLM context and feed it ~1k.
  - Round routing: first speaker by strategy, followers by
    `random.choice` (`app/routers/chat.py:254-261`) — conscripts
    speakers with nothing to say.
  - Nemotron's reasoning toggle must be managed per persona
    prompt (`/no_think` line 1); model reload ≈ 90 s windows on
    container restart.
  The ensemble-narrative dimension of these findings is mapped
  in full in [discussion 2026-09-16] (narrative health: two
  axes, 20 mechanisms, zero-code test battery).
- **(f) Security observations — assumption VERIFIED.** Every
  service in the stack is unauthenticated (llama-server warns
  openly; tts-serve and whisper-fastapi offer nothing); without
  the tunnel, ports 8080/8001/8002 would all need public
  exposure. The SSH-tunnel posture ([spec §10.3]) is thereby
  validated as load-bearing, not optional.
- **Bonus observations:** full 3-service trio fits the 16 GB
  card — 13.5/15.3 GiB loaded, **14.0/15.3 GiB fully warm**
  (whisper lazy-loads its model at first STT request: VRAM reads
  ~12.3 GiB until then — confirmed across the hibernation cycle);
  challenges C1/C6 field-observed ("Miss Betty"→"Nisbeti") with
  the in-fiction absorption mitigation firing unprompted; the
  owner's headline reading, which the verdict upheld:
  "TalkWithMe + tts-serve can be separated into local client /
  remote cloud GPU without any local modifications."

**Show-quality issues found** (adaptation-arc backlog per the
PASS machinery; each with fix shape and rough cost):

1. Output sanitizer for `[Name]:` labels — one line; designated
   FIRST fork patch (cost: minutes, plus the fork decision).
2. Max-chars sentence accumulator in `static/tts.js` — replaces
   per-sentence chunking; fixes splitter naivety AND
   short-sentence economics (cost: a small, local JS patch;
   candidate upstream PR).
3. Raise `max_turns_for_context` from 6 — pure settings.yaml
   lever, cap 50 (cost: one line; watch latency as context
   grows).
4. Narrative-health fragility — not one fix but a mapped design
   space: [discussion 2026-09-16], with its zero-code probe
   battery as the cheap next moves (cost: adaptation-arc design
   work; the §5.3 director question).

## Prediction grading (in public, per protocol)

**Agent's registered prediction: WRONG — in the happy
direction.** Predicted PARTIAL with 2–4 small localhost-isms;
reality: **zero** localhost-isms — the split was pure
configuration, and the verdict is a clean PASS. The (c) worry
(TTFA "3–8 s, uncomfortably straddling the 5 s line") was also
wrong for streaming mode (median 0.9 s), though it would have
been roughly right had non-streaming mode been the design —
partial credit only in an alternate universe. Lesson recorded:
the agent over-weighted "localhost-born app" as a risk category
and under-weighted the evidence that FastAPI + REST + browser
shapes are WAN-shaped by construction — its own stated reasoning
argued for a braver prediction than it registered.

**Owner:** declined to predict (slot closed 2026-09-14).

## Verdict

**PASS** (2026-09-16, against the frozen criteria, from runlog
evidence):

1. 4-persona session with distinct voices audible end-to-end on
   the laptop through the SSH tunnel — MET (step 6 group
   sessions).
2. TTFA ≤ ~5 s/line sustained over ≥10 consecutive lines — MET
   (TTFA table: 13 consecutive streaming bursts ≤ 5 s; median
   0.9 s).
3. No architectural blocker — MET (measure (e): every red flag
   is configuration-level or upstream-improvable; zero upstream
   modifications were needed for the split itself).

**Consequence executed per the frozen machinery:** the MVP
proceeds on TalkWithMe + tts-serve; [ADR-0001] truth-audited and
frozen to `accepted` (same commit); the Pipecat flip trigger
expires unfired. Show-quality issues route to the adaptation
arc's backlog as enumerated above.

**Post-verdict addendum (same evening, before teardown):** the
name-memory micro-test FAILED (confabulated recall), then was
half-exonerated by a config receipt — `max_turns_for_context: 6`
means the fact was physically outside the model's context
(runlog closing entries; taxonomy C9). This does not move the
verdict: recall is not a frozen criterion, and the cause is a
config lever, not architecture. It does sharpen two backlog
items: raise the history window, and re-run the micro-test inside
the LLM audition — the model remains suspect for in-context
quality (the Betty/Anna garble), not for the amnesia. Final
experiment cost, owner-read at teardown: **$2.97**.

## Headline findings — five positives, five negatives

*(Distilled 2026-09-16, owner-requested exercise; confirmed at
verdict time the same evening, then lightly amended at close:
final VRAM figure in positive 3, mechanism count and the C9
config-amnesia lever in negative 1. Interpretation from runlog
evidence only; receipts cited.)*

**Five positive findings:**

1. **Zero upstream modifications.** The full remote split —
   client on the laptop, all three model services behind the
   tunnel — worked with configuration alone. "Configuration, not
   surgery" won outright; the agent's predicted 2–4
   localhost-isms never materialized (runlog steps 1–5, all
   gates PASS).
2. **Zero tts-serve adapter needed.** TalkWithMe auto-detected
   the engine from `/capabilities` and rendered its parameter
   schema in the UI; the predicted integration effort (measure
   (d)) turned out to be environment potholes, not code (runlog
   deployment ledger).
3. **The full trio fits the 16 GB card** — 13.5/15.3 GiB loaded,
   14.0/15.3 GiB fully warm (final reading, whisper lazy-load
   included), ~1.3 GiB headroom. The "16 GB aspirational" tier is
   empirically real, which reprices the whole provider space
   downward.
4. **Latency works over a hostile baseline.** Streaming TTS is
   gapless for normal sentences (per-sentence RTF 0.46–0.64)
   *even with* ~215 ms Norway RTT — a Canada-1 demo box only
   improves on this. The tunnel added no observed instability
   (cold-connection 0.6–0.7 s, amortized).
5. **The documentation system paid for itself in-run.** The
   hibernation wipe cost ~30–45 min of paste because every
   command was recorded; the Reproduction recipe passed its
   first real replay. Honorable mention: in-fiction absorption
   fired unprompted ("Miss Betty" → "Nisbeti", carried
   in-character — the C6-challenge mitigation demonstrating
   itself).

**Five negative findings:**

1. **Narrative health is fragile** — label mimicry, transcript
   contamination, group degeneration, the stale-question round.
   Big enough to earn its own framework:
   [discussion 2026-09-16] (storytelling coherence & structure
   adherence — two axes, 20 candidate failure mechanisms). The
   adaptation arc's opening backlog; NOT an architectural
   blocker per the frozen criteria.
2. **Short-sentence economics are upside-down**: per-request
   fixed costs (RTT + ~300 KB reference re-upload per sentence,
   `app/routers/tts.py:134`, + engine floor) make effective
   RTF > 1 for short sentences, and the naive splitter makes
   FOUR requests of "Dr. Byrne. 47. Microbiology. Over." —
   while radio style is MADE of short sentences. Designated
   fix: the max-chars accumulator (upstream patch candidate).
3. **Nothing in the stack authenticates anything.** llama-server,
   tts-serve, whisper-fastapi — all open (measure (f)). The SSH
   tunnel is load-bearing, not defense-in-depth; there is no
   second layer.
4. **Provider fragility is real**: A6000s persistently out of
   stock (survey warning realized), and Hyperstack "hibernation"
   is a destructive stop plus a restore lottery. Demo-week rule
   hardened: never hibernate the show box.
5. **The environment is pothole-rich**: exact
   `transformers==5.15.1` pin, numpy-before-sox ordering, the
   R535 driver disqualifying three TTS engines, Nemotron
   demanding `/no_think` per persona prompt. All solvable, all
   in the Ansible ledger — and each one a demo-day landmine if
   undocumented.
