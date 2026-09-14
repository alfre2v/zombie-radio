# TalkWithMe remote-split test ("the spike") — findings

**Status:** VERDICT CRITERIA DRAFTED, NOT YET FROZEN — freeze =
the commit that also carries both filled prediction slots, made
BEFORE any spike command runs. Interpretation only; raw evidence
lives in `README.md` (the runlog).

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

**Owner (Alfredo):** *(TO FILL before the run — one paragraph:
expected verdict, why, and which measure you're least sure of.)*

## Results

*(empty until the run; filled only from README.md evidence)*

## Verdict

*(empty until the run)*
