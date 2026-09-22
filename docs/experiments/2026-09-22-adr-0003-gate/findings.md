# ADR-0003 gate — findings

**Status:** verdict **PASS** on all three graded items (gates 1, 2a
and 2b), written 2026-09-22 and awaiting the owner's review; the
folder seals once he accepts it. The criteria below were committed in
`9024a1f` at 16:45:59 CDT, an hour before the first gate request
(17:50:37); the owner's decline to predict was recorded afterwards
and changes no criterion. This file decides the experiment, not
ADR-0003: the ADR's truth audit is a separate step that reads this
verdict. Interpretation only; the evidence lives in `README.md`
(recipe + runlog, entries 12–15 for the gates) and `raw/`.

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

**Owner (Alfredo):** declined to register a prediction
(2026-09-22: "I want to see the experiment") — noted so the slot is
closed, not forgotten. The agent's predictions above stand alone
for grading.

## Results

*Everything below comes from the runlog — entries 12 to 15, which
carry the scripts' output verbatim — and from the raw files they
point to. Times are the laptop's (CDT).*

### The evening in one paragraph

The box was deployed from zero at 17:40 and answered through the
tunnel eight minutes later. Three streamed requests went out at
17:50 for gate 1; seventy-one plain requests ran between 17:54 and
17:56 for gate 2. Every graded number came back on the right side of
its threshold, most of them comfortably. The surprise was not in
the numbers but underneath them: the reason the shared script is
faster turned out to be different from the one ADR-0003 believed,
and part of the cost it avoids never shows up in the server's own
accounting.

### Gate 1 — the grammar streams, and it binds

- **The script was typed out, not delivered in one block.** In the
  `main` run, 72 chunks carried text, the first arriving at 552 ms
  and the last at 1,367 ms after the request left — a spread of
  0.60 against a threshold of 0.50. What the browser will receive is
  a stream of small pieces, exactly as with unconstrained text.
- **The shape was right.** Four complete lines, every one of them
  `Name: text` with a legal name, and all four scientists used.
- **The grammar wins an argument with the prompt.** In the `control`
  run the prompt asked for the four scientists while the grammar
  allowed only `Operator`. Every line began `Operator:` — and the
  text shows the model looking for its cast and being refused:
  *"Operator: Ralph, you're counting the shamblers, right? Need to
  know if they're closing in. Over."*
- **The field that works** is the plain top-level `grammar` key on
  `/v1/chat/completions`, the endpoint TalkWithMe already calls. No
  fallback to `response_format` or `/completion` was needed.
- **Without a grammar, the model wrote the very same lines.** The
  `nogrammar` baseline — same prompt, same seed — produced the same
  four lines character for character. With this cast sheet the model
  already writes the format on its own; here the grammar was a
  guarantee, never a correction.

### Gate 2a — one request per round costs about a quarter of four

- **The ratio is steady.** Round by round, D's prompt-evaluation time
  was between 0.224 and 0.264 of A's; `R_early` (rounds 2–4) is
  0.257 and `R_late` (rounds 8–10) is 0.234. D spends about a
  quarter of A's prompt time, and the gap does not shrink as the
  script grows.
- **But A's cache did not collapse.** The belief behind the
  criterion was that four different system prompts would keep
  evicting each other from the server's single slot. They did not:
  this build keeps a second-level prompt cache in the box's RAM
  (`--cache-ram`, 8,192 MiB by default) and restores each persona's
  saved state when its turn comes. A's share of reused prompt climbed
  from 44 % in round 2 to 88 % in round 10 — much the same curve as D's (52 % to 88 %).
- **The rescue has a price the server does not report.** Before each
  of A's requests the server saves the slot's state to RAM and loads
  another one. The only entries whose size the log reports — the
  three it evicted when the RAM cache filled up — were 417 MiB,
  422 MiB and 1.8 GB. In the excerpt of the runlog, about 1.7 s pass between
  choosing the slot and starting the work on a round-10 request of
  A, while the same step for D takes under a millisecond. That time
  is not part of the `timings` the criterion reads — which is why
  A's prompt time stays flat (about 1.4–1.6 s per round) while its
  wall time per round doubles, from 4.4 s in round 1 to 9.4 s in
  round 10. D's rounds take 1.5–2.0 s (D-off) and 1.35–1.53 s
  (D-live) throughout. The wall-time ratio, reported but not graded,
  falls from 0.59 to 0.16: in what the audience would actually wait
  for, D is about six times faster by round 10, and the margin grows
  with the script.
- **Every request pays a fixed toll.** The prompt phase costs about
  350 ms whether it evaluates 130 tokens or 270, in both structures.
  Four requests pay it four times. Why the floor sits there is not
  known yet; the leading suspect is how this hybrid model's recurrent
  state is handled per request.

### Gate 2b — the grammar is free here

The median cost of a generated token was 11.260 ms without the
grammar (D-off) and 11.298 ms with it (D-on): `O` = 0.3 %. And because
D-off and D-on wrote identical text in all ten rounds
(`check_outputs.py`), the comparison is as clean as a measurement
gets: same tokens, with and without the mask. That same fact sets
the limit of what was measured — this is the cost of a grammar that
never had to change the model's mind. What a grammar costs when it
does steer is the question of the next run.

### D-live — the loop we would ship

With the model's own output fed back as history, the share of the
prompt reused from the cache rose from 55 % in round 2 to 88 % in
round 10; each round evaluated 169–184 tokens, roughly what the round had
added. The minimum, 55 %, is above the 50 % routing line:
no investigation is owed before the fork. The low start is
arithmetic, not a fault: early in a show the new lines are a large
share of a short script.

### What the model wrote

In all three D arms, with or without the grammar and with its own
output fed back, every reply had exactly four lines, every line was
well-formed, and every one of the forty per arm ended in "Over."
(`check_outputs.py`). The prompt said "up to four lines"; the model
read it as "four". Two habits worth knowing for the fork: it ends
lines with two spaces before the newline, and it writes typographic
punctuation — curly apostrophes, em dashes, the odd ellipsis — even
though the cast sheet and the fixed script are plain ASCII.

### The caveats, revisited

1. **One slot** — as expected; it is where A had to swap.
2. **A without its router call** — stands; the router would add a
   fifth request per round and widen D's lead.
3. **Fixed versus live history** — did not mislead: D-live's reuse
   tracks D-off's closely.
4. **The hybrid model** — did not bite where feared: reuse works,
   through the live loop too. It remains the suspect for the 350 ms
   floor (unverified).
5. **The RAM-side prompt cache** — materialized, and it decided the
   mechanism: it rescued A's reuse and moved A's real cost outside
   the server's timings.
6. **No truncation** — confirmed: the largest prompt, 1,550 tokens
   (D-off, round 10), is under a tenth of the 16,384-token context,
   and every `stop processing` line in the server log reads
   `truncated = 0`.
7. **No A-with-grammar arm** — no consequence.
8. **Server-side numbers** — the caveat that mattered most. The
   criterion read `prompt_ms`, which is honest but incomplete; the
   wall time and the server log tell the rest.

### Predictions, graded

**Agent:**

- *Gate 1 PASS, through the top-level `grammar` field* — **survived**,
  both halves.
- *Gate 2a PASS, `R_late` between 0.2 and 0.4* — **survived on the
  number** (0.234). The belief underneath did not fare as well: the
  handoff's expectation that "the shared prefix wins by a margin that
  grows with history length" **died for prompt time** (flat at about
  a quarter) and survives only in wall time; and ADR-0003's premise
  that per-persona prompts defeat the cache **died on this build** —
  the RAM cache rescues them, at a price paid elsewhere.
- *Gate 2b PASS, `O` under 10 %* — **survived** (0.3 %), with the
  limit noted above: the grammar never had to steer.
- *D-live, minimum reuse at or above 80 %* — **died** at 55 %. The
  reason is the early rounds' arithmetic, not a cache that fails;
  the prediction forgot how short a script is at the start of a
  show.

**Owner:** declined to predict.

## Verdict

**PASS** on all three graded items. The pre-registered consequences
follow, with one amendment the evidence demands.

- **Gate 1 — PASS.** ADR-0003 point 3 stands as written. The fork
  sends the screenplay grammar in the top-level `grammar` field of
  `/v1/chat/completions` and streams as TalkWithMe does today.
- **Gate 2a — PASS.** ADR-0003's latency point changes from believed
  to measured. The truth audit must also rewrite its reason: not
  "per-persona system prompts defeat the prompt cache", but
  "per-persona prompts force a state swap before every request —
  hundreds of megabytes moved between GPU and RAM, paid outside the
  server's timings — on top of a fixed prompt cost per request; one
  shared script per round pays neither". Prompt-structure §9 point 4
  gets a dated annotation to the same effect.
- **Gate 2b — PASS.** The ADR's "overhead reported 1–20 %" is
  replaced by the measured 0.3 %, noted as the cost of a grammar that
  did not have to intervene.
- **D-live — above its routing line.** No TODO line for the fork.

Not decided here: ADR-0003's status (its truth audit comes next and
reads this verdict); the prose quality with and without the grammar
(the Task 5a audition); what a richer grammar with an emotion field
costs (the follow-up run).
