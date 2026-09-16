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

## Verdict

*(empty until the run)*
