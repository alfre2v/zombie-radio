# TalkWithMe remote-split test ("the spike") — findings

**Status:** VERDICT CRITERIA FROZEN by the commit landing this
line (2026-09-14), before any spike command has run.
Interpretation only; raw evidence lives in `README.md` (the
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

## Results

### PRELIMINARY (2026-09-16 — experiment in progress; steps 6–8 outstanding; nothing here is a verdict)

Mapped to the pre-registered measures, from runlog evidence only:

- **(a) Audio over WAN** — partial: single-persona sessions
  deliver cloned speech through the tunnel with no observed
  drops/stalls; streaming mode played a 6-fragment monologue
  gaplessly (client-side fetch-ahead pipeline, source-verified).
  PENDING: sustained multi-persona session behavior.
- **(b) 4-persona session** — PENDING (step 6); all four
  personas exist with distinct cloned voices; single-persona
  chat proven for text + voice + mic.
- **(c) Time-to-first-audio** — partial: non-streaming
  single-line ≈ 5 s to first sound; streaming mode makes
  first-audio ≈ first-sentence synth; per-sentence RTF 0.46–0.64
  (gapless threshold cleared 2×); tunnel cold-connection
  overhead 0.6–0.7 s, amortized by persistent connections.
  PENDING: the formal ≥10-consecutive-lines table in ensemble
  conditions (GPU contention included).
- **(d) tts-serve adapter effort** — answered by observation:
  **ZERO adapter needed** — TalkWithMe auto-detected the engine
  from `/capabilities` and rendered its parameter schema in the
  UI. The real integration cost was environment, not code: the
  documented potholes (apt packages, numpy-before-sox,
  transformers==5.15.1 pin) in the runlog's deployment ledger.
- **(e) Architectural red flags** — collected: reference audio
  re-uploaded per sentence (stateless API; WAN tax;
  `app/routers/tts.py:134`); sentence-chunked synthesis severs
  prosodic continuity (→ brainstorm C10); Nemotron reasoning
  toggle must be managed per persona prompt; model reload ≈90 s
  windows on container restart. NONE structural — all
  configuration-level or upstream-improvable.
- **(f) Security observations** — every service in the stack is
  unauthenticated (llama-server warns openly; tts-serve and
  whisper-fastapi offer nothing); without the tunnel, ports
  8080/8001/8002 would all need public exposure. The SSH-tunnel
  posture ([spec §10.3]) is thereby validated as load-bearing,
  not optional.
- **Bonus observations**: full 3-service trio fits the 16 GB
  card at 13.5/15.3 GiB (16 GB-aspiration datum); challenges
  C1/C6 field-observed ("Miss Betty"→"Nisbeti") with the
  in-fiction absorption mitigation firing unprompted; the
  owner's headline interim reading: "TalkWithMe + tts-serve can
  be separated into local client / remote cloud GPU without any
  local modifications."

### FINAL (2026-09-16 — experiment closed inside the timebox)

The preliminary section above is kept as written (honest
snapshot); this section resolves its PENDING items from runlog
evidence:

- **(a) Audio over WAN** — RESOLVED, yes: multi-persona group
  sessions delivered cloned speech through the tunnel across
  multiple evenings with no drops or stalls observed; the only
  audio complaints (inter-sentence pauses on short sentences)
  are per-request economics, not WAN transport behavior.
- **(b) 4-persona session** — RESOLVED, yes: the `Lab`/`lab2`/
  `lab3` group sessions ran 4 scientists with distinct cloned
  voices end-to-end (runlog step 6 entries, screenshots in owner
  archive).
- **(c) Time-to-first-audio** — RESOLVED, PASS with data: the
  harvested TTFA table (152 requests → 24 bursts,
  `extract_tts_timings.py`) shows median est. TTFA 0.9 s and
  **13 consecutive replies ≤ 5 s** in streaming mode, meeting
  the ≥10-consecutive-lines clause; the only >5 s bursts were
  the deliberately-tested (and rejected) non-streaming A/B
  trials. Numbers carry the conservative ~215 ms NORWAY-1 RTT.
- **(d), (e), (f)** — as in the preliminary section (zero
  adapter; red flags all non-structural; tunnel load-bearing).

Show-quality issues found (become adaptation-arc backlog per the
PARTIAL/PASS machinery, listed with fix shapes): output sanitizer
for `[Name]:` labels (one line, designated first fork patch) ·
max-chars sentence accumulator in `static/tts.js` (designated
upstream patch; fixes both splitter naivety and short-sentence
economics) · narrative-health fragility (framework + 20-mechanism
taxonomy + zero-code test battery in [discussion 2026-09-16]) ·
`max_turns_for_context: 6` amnesia (pure config lever — raise it;
taxonomy C9).

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
