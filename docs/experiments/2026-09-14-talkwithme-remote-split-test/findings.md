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

## Headline findings — five positives, five negatives

*(Distilled 2026-09-16, owner-requested exercise; PRELIMINARY
like the Results above — to be confirmed or amended at verdict
time. Interpretation from runlog evidence only; receipts cited.)*

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
3. **The full trio fits the 16 GB card** — 13.5/15.3 GiB with
   llama + TTS + whisper resident. The "16 GB aspirational" tier
   is empirically real, which reprices the whole provider space
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
   adherence — two axes, 17 candidate failure mechanisms). The
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

## Verdict

*(empty until the run)*
