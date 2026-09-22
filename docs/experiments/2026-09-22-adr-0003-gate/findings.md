# ADR-0003 gate — findings

**Status:** DRAFT — verdict criteria and predictions NOT yet frozen.
The freeze is the commit that carries this file with both
prediction slots filled (experiments README); no gate request
(`stream_check.sh`, `latency_probe.py`) runs before that commit.
Interpretation only; the evidence lives in `README.md` (recipe +
runlog) and `raw/`.

## What this experiment decides

ADR-0003 (draft, `docs/decisions/0003-adopt-shared-context-screenplay-engine-with-browser-clocked-director.md`)
rests on two claims nobody has measured on our stack. Its Gate
section lists them as items 1 and 2; item 3 (prose quality with and
without the grammar) belongs to the Task 5a audition, not to
tonight.

1. **Grammar-constrained streaming.** llama-server applies a GBNF
   grammar while streaming, so the constrained tokens arrive in the
   ordinary SSE chunks our stream parser will read. Believed from a
   source read (`tools/server/server-context.cpp`, `process_token()`:
   the `stream` flag gates only `send_partial_response`; prompt-structure
   discussion §7.1); never run on our build.
2. **Latency shape.** One shared script per round (structure D)
   costs less prompt evaluation than TalkWithMe's four per-persona
   requests (structure A), because llama-server reuses its cached
   prompt only along an identical prefix and A puts a different
   system prompt at position zero of every request. BELIEVED, not
   measured. Plus: the grammar's per-token cost on our model.

## Verdict criteria (pre-registered — frozen by the commit that carries them)

Every number named below is printed by a committed script over the
raw files: `parse_stream.py` for gate 1, `summarize_timings.py` for
gate 2. No number in the Results section is computed by hand.

### Gate 1 — grammar-constrained streaming

*How it is measured.* `stream_check.sh` sends one streamed request
(`stream: true`, grammar in the top-level `grammar` field of
`/v1/chat/completions`) and records every SSE line with its arrival
time in milliseconds since the request left. The request is round 1
of the fixed script: the cast sheet as `system`, the round-1
directive as `user`, the directive naming the four scientists.
Two runs:

- **main** — the grammar allows the four scientists.
- **control** — the grammar allows ONLY `Operator`, a name that
  appears nowhere in the prompt, while the directive asks for the
  four scientists. Output made only of `Operator:` lines proves the
  server applied the grammar against the prompt's wishes; output
  with any scientist's name proves the grammar was ignored.

`parse_stream.py` prints, per run: the number of chunks carrying
content; the arrival time of the first and last of them; the spread
= (last − first) / last; every complete line with a legal/ILLEGAL
mark against the grammar's allowlist; the speakers used.

- **PASS** — all of:
  - (a) main: at least 5 chunks carry content, and the spread is at
    least 0.50 (the content arrives over the generation, not in one
    lump at the end);
  - (b) main: the content is 1–4 complete lines, each
    `Name: text` with a name from the allowlist, no ILLEGAL line;
  - (c) control: every complete line's speaker is `Operator`.
  → **Consequence:** ADR-0003 point 3 stands as written; the
  working field (`grammar`, top level, on `/v1/chat/completions`)
  is recorded in the recipe and quoted in the ADR truth audit.
- **PARTIAL** — (a)–(c) hold, but only after moving the grammar to
  another field (`response_format`) or another endpoint
  (`/completion`).
  → **Consequence:** ADR-0003 amended to name the working field and
  endpoint; the fork's request builder targets them; the ADR can
  still be accepted.
- **FAIL** — under every field tried, the control run shows a name
  other than `Operator`, or (a) fails (one lump), or the server
  rejects `stream` together with `grammar`.
  → **Consequence:** ADR-0003 stays draft; the fork's engine design
  does not start; the prompt-structure discussion reopens its point
  3 (the options then: a tolerant parser over an unconstrained
  stream, as in 2024; or non-streamed rounds).

### Gate 2a — latency shape: structure A versus structure D

*How it is measured.* `latency_probe.py` plays the same fixed
10-round script (`cast.py`: ten events of radio traffic, four lines
per round, about 75–95 characters each) through two structures,
non-streamed so that each response carries the server's clean
`timings` object:

- **Arm A** — TalkWithMe 7.1's `build_llm_messages`
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/session.py:123-161`):
  for each of the four lines of a round, one request with that
  persona's own system prompt (the installer-seeded placeholder
  prompts, verbatim), its own earlier lines as `assistant`, everyone
  else's as `user` messages reading `[Name]: text`, the radio
  traffic as a plain `user` message. Four requests per round.
- **Arm D-off** — one request per round: the cast sheet as
  `system`, then the script so far as alternating turns (directive
  as `user`, the round's four lines as `assistant`), then this
  round's directive. No grammar.

Both arms see the same fixed lines (the model's replies are recorded
but not fed back), so the only difference between them is the
structure. For every round, `summarize_timings.py` prints
`R_k = (D-off prompt_ms at round k) / (A prompt_ms at round k)`,
where A's figure is the sum over its four requests, and two means:
`R_early` over rounds 2–4 and `R_late` over rounds 8–10 (round 1 is
a cold start for both and is left out of both means).

- **PASS** — `R_late ≤ 0.50` AND `R_late ≤ R_early` (D spends at
  most half of A's prompt-evaluation time late in the run, and the
  gap does not shrink as the history grows).
  → **Consequence:** ADR-0003's latency point ("the best latency
  shape available … one cache prefix") changes from believed to
  measured, with the numbers quoted; prompt-structure §9 point 4
  gets a dated annotation.
- **PARTIAL** — `R_late < 1.0` but PASS is not met.
  → **Consequence:** the latency point is kept but rewritten with
  the measured numbers as a modest advantage; the decision stands.
- **FAIL** — `R_late ≥ 1.0` (A is as cheap as D or cheaper).
  → **Consequence:** the latency point is struck from the ADR's
  "what it buys"; the decision stands on its other factors
  (prompt-structure §9: "believed on the cache point until
  measured; the direction is not in doubt"); an investigation of
  the cache mechanism becomes a TODO line before Task D starts.

*Reported, not graded:* per request, the prompt tokens evaluated
(`prompt_n`) versus reused from the cache (`cache_n`) — the
MECHANISM behind the milliseconds; wall time per round (includes
generation and the tunnel).

### Gate 2b — the grammar's per-token cost

*How it is measured.* **Arm D-on** is D-off with the screenplay
grammar (`screenplay.gbnf`, all four speakers, 1–4 lines). Same
prompts, same seed. Per round, generation cost per token =
`predicted_ms / predicted_n`; `summarize_timings.py` takes the
median over the ten rounds for D-off and for D-on and prints
`O = (on − off) / off`.

- **PASS** — `O ≤ 10 %`.
  → **Consequence:** the ADR's "overhead reported 1–20 %" is
  replaced by our measured number.
- **PARTIAL** — `10 % < O ≤ 25 %`.
  → **Consequence:** accepted; the cost is written into the ADR and
  into the fork's latency budget.
- **FAIL** — `O > 25 %`.
  → **Consequence:** before the fork's grammar builder is written,
  try a simpler `text` rule and re-measure; ADR-0003 stays draft on
  point 3 until then.

### Reported, not graded — arm D-live, the loop we would actually ship

**Arm D-live** is D-on, except that each round's script in the
history is the model's own previous output, verbatim — the
production loop of ADR-0003. `summarize_timings.py` prints, for
rounds 2–10, the share of the prompt reused from the cache,
`cache_n / (cache_n + prompt_n)`.
→ **Routing:** if the minimum share is below 50 %, a TODO line for
the fork: investigate cache reuse on our hybrid model (see caveat 4)
before Task D's director is built around it.

## Interpretation caveats, written before the data

1. **One slot.** llama-server runs `--parallel 1`
   (`zr_llama_parallel: 1`): one slot, one cached prompt at a time.
   This is exactly the production configuration, and exactly where
   A's four different prefixes should evict each other.
2. **A is favored on purpose.** TalkWithMe also makes a router call
   each round (its own prompt, temperature 0.1) before the persona
   calls; the probe leaves it out. If D still wins, the result is
   robust; if A wins, the router call would narrow A's lead.
3. **Fixed history versus live history.** In A, D-off and D-on the
   history is the fixed script, not the model's replies. The cache
   can then be reused at most up to the end of the previous prompt,
   never through the previous reply. D-live measures the real loop.
4. **Our model is a hybrid.** Nemotron Nano 9B v2 is `nemotron_h`, a
   hybrid of Mamba-2 (state-space) layers and attention layers
   (taxonomy A2,
   `docs/discussions/2026-09-16-storytelling-coherence-and-structure-adherence.md:191`).
   A state-space layer carries a running state that cannot be wound
   back to an earlier token, so the server can reuse a cached prompt
   only if the saved state ends exactly where the new prompt stops
   matching, or it keeps checkpoints of that state. How our build
   handles this is BELIEVED, not known; the `cache_n` columns and
   the server log show what happened.
5. **A RAM-side prompt cache may rescue A.** Recent llama.cpp builds
   are believed (agent's memory of the 2025 changelog, unverified)
   to save prompt states to host memory and restore them
   (`--cache-ram`), which would let A keep one state per persona in
   RAM instead of re-evaluating. The recipe records the server's
   help text and startup log so the Results can say whether this
   exists in our build and was used.
6. **No history truncation.** Ten rounds keep A's history under
   TalkWithMe's `max_turns_for_context` of 50 entries (at most 49
   before round 10's last request), so A's history is never cut.
7. **No A-with-grammar arm.** The handoff design had four arms (A
   and D, each with and without the grammar). A never runs with a
   grammar in any configuration we would ship, and the grammar's
   cost is a property of grammar plus model, measured on D; the
   A-on arm was replaced by D-live.
8. **Server-side numbers.** Prompt and generation milliseconds come
   from the server's `timings` and do not include the tunnel; wall
   time does.

## Predictions (registered before any gate data; deaths recorded after)

**Agent (Claude, registered 2026-09-22):**

- **Gate 1: PASS**, with the top-level `grammar` field on
  `/v1/chat/completions`. Confidence high that streaming works (the
  source read); moderate that the top-level field is the one that
  works on the chat endpoint (the grammars README speaks of
  `response_format` there).
- **Gate 2a: PASS**, `R_late` between 0.2 and 0.4 (D three to five
  times cheaper on prompt evaluation late in the run). Confidence
  moderate — lower than the handoff's, because of caveats 4 and 5:
  the RAM cache could shrink A's cost, and the hybrid model could
  limit D's reuse.
- **Gate 2b: PASS**, `O` under 10 %. Confidence moderate-high: the
  grammar is tiny and the per-token mask touches a few structural
  tokens per line.
- **D-live:** minimum reuse share at or above 80 %. Confidence low
  (caveat 4).

**Owner (Alfredo):** *slot open — a prediction, or an explicit
decline recorded so the slot is closed, not forgotten.*

## Results

*Filled only from README evidence after the runs.*

## Verdict

*After Results.*
