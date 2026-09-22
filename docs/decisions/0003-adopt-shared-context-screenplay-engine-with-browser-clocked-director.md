# Adopt a shared-context screenplay engine with a browser-clocked server director
**Date:** 2026-09-21
**Status:** draft — direction adopted by the owner 2026-09-21;
becomes *accepted* when the gate below passes (the ADR-0001
pattern: a truth audit re-read immediately before freezing)

## Context

TalkWithMe generates a show turn as one LLM request PER PERSONA:
the persona's own system prompt, and a history rewritten so that
every other persona's line becomes a `user` message reading
`[Name]: text` (`app/session.py:146-161`, TalkWithMe 7.1). A round
is a router call plus up to four persona calls, followers drawn at
random (`app/routers/chat.py:226`, `:261`), and the loop stops
until the browser posts again; the app has no server-initiated
channel to the page.

The narrative-health taxonomy ([discussion 2026-09-16]) charged
this structure with five field-observed mechanisms: labels leak
into speech and re-seed themselves (C1, C3); a two-role chat
template wearing a four-actor play (C2); a nameless director (C6);
random followers (E1); nobody owns the story (E3). The owner's
2024 prototype used the opposite structure — one shared context, a
script in `Name: line` form, a hidden narrator as the `user` — and
he remembers the narrator as what "brought the narration alive",
with repetition as the enemy and no observed character bleed
(weak evidence: thin characters, poor lines).

Two design discussions on 2026-09-21 compared the alternatives
with code receipts and online research:
[discussion 2026-09-21] prompt-structure and
[discussion 2026-09-21] story-loop. Three facts weighed more than
taste: llama-server's prompt cache reuses only an identical prefix,
so per-persona system prompts defeat it (believed, to be measured);
the browser's SSE protocol (`start`/`token`/`done`/`complete`,
tagged with a persona) can be synthesized per parsed script line,
so the page needs no changes; and the only component that knows
when a speaker has finished PLAYING is the browser.

The research settled two red flags: llama.cpp applies a grammar in
the sampler on every token regardless of the `stream` flag (read
in `tools/server/server-context.cpp`, `process_token()`, where
`stream` gates only `send_partial_response`); and the reported
quality cost of constrained decoding comes from the model
CONDITIONING on a JSON-looking prefix, not from the mask itself —
which a screenplay grammar avoids by keeping the model inside the
text distribution it was trained on.

## Decision

**Prompt structure (unit of generation).**

1. One shared context in screenplay form. `system` = the cast
   sheet (one section per character, the bibles) plus the show's
   rules and format; the history = the script so far as alternating
   turns — director directive (`user`), script lines (`assistant`);
   `[Name]:` history rewriting disappears.
2. A DIRECTOR IN CODE, in the server, assembles each round: beat,
   speaker allowlist, line budget, stage direction, entropy terms,
   written into the `user` directive.
3. One streamed request per round asks for the whole exchange
   (several speakers), under a GBNF SCREENPLAY GRAMMAR sent in the
   request's `grammar` field: `line ::= speaker ": " text "\n"`,
   with the `speaker` alternatives narrowed to the director's
   allowlist and the line count bounded with `{0,N}`; optional
   parenthetical stage directions from a small enum carry the
   emotional register. NOT JSON — the owner's reason: the grammar
   must not confine the model to the distribution of JSON it saw
   in training.
4. The server parses the stream at line breaks and emits the
   existing SSE events per speaker line; browser, TTS pipeline and
   audio persistence are unchanged. The label sanitizer is not
   built — there is no label to strip. The sentence accumulator's
   unit becomes the script line.
5. Room to reason before the constrained part (a bounded,
   non-spoken `# note:` line capped by the grammar) is a
   REGISTERED HYPOTHESIS, not part of the decision
   (`docs/follow-ups.md`).

**Story loop (what makes the next turn happen).**

6. Placement 1 of three: the BROWSER is the metronome, the SERVER
   is the director. A `/show` page (`show.js`) requests the next
   round from `POST /api/show/round` when the audio queues drain;
   the server runs the director and the generation and streams the
   events. Rejected: a server-side loop with a push channel (the
   future booth's upgrade — the server cannot know when playback
   ended without a back-channel; nothing here blocks it); an
   external director process with polling (loses streaming;
   duplicates the director).
7. Endless loop; interaction beats on a randomized, configurable
   TIME window measured in played audio (minimum and maximum
   seconds, probability rising in between; never a round count —
   owner pushback: rounds are seconds long and every listening
   window is a pause the audience hears). Episode structure comes
   post-MVP through trajectory scaffolds.
8. Half-duplex microphone by construction: hold-to-talk, enabled
   only in the listening state when the queues are empty; the
   transcript rides with the next round request as in-fiction
   audience traffic; the director constrains the answering round to
   one speaker.
9. The show runs on a separate page, not a room flag; the chat UI
   remains the rehearsal and debugging tool. Dead-air static
   (second AudioContext source) and cross-round prefetch are
   polish: outside the timebox's exit criterion, dead air needed
   the day the cadence is tuned.

## Consequences

**What it costs:**

- Identity bleed (C4) becomes the main identity risk: four
  characters in one context. Defenses: the bibles, the audition,
  stage-direction tags, a director that refuses to let one voice
  dominate.
- Possible prose flatness under the grammar — expected small
  (the mask barely touches prose tokens), unmeasured for dialogue
  by anyone; an audition item.
- Per-token grammar overhead, reported 1–20 % by backend; the
  `x? x? …` repetition pattern must be avoided (`{0,N}`).
- Truncation at `max_tokens` cannot be closed by the grammar; the
  line-oriented format loses at most its last line.
- One growing script versus the context window (C9 in a new
  form): the director owns transcript curation.
- The show lives in a foreground tab; a sleeping tab pauses it
  (demo-day discipline; the canned episode is the fallback).
- Build: ~2 days for the generation strategy, ~0.5 for the
  grammar, ~1 for the loop — 3.5 against the 3-day timebox; the
  midpoint checkpoint and the polish levers absorb the gap.

**What it buys:**

- Five failure mechanisms removed by construction (C1, C2, C3,
  C6, E1) and E2/E3 given an owner; no sanitizer layer.
- A wire format that cannot break, without a client library; an
  illegal speaker cannot be sampled.
- The best latency shape available: one prompt evaluation per
  round, one cache prefix, first line after one evaluation.
- The browser untouched beyond the accumulator and the new show
  page; each decision where its information is — story in the
  server, time in the browser.
- The emotional register as data (seam question S6) via the
  parenthetical, without leaving the screenplay distribution.
- The owner's 2024 design kept where it worked and fixed where it
  broke — and, recorded as a real factor on a learning-loop
  project, the approach the owner is eager to build.

**Reversibility:** high until the fork's engine is written; low
afterwards within the arc (the three-day box is spent on it).
Falling back is not "return to TalkWithMe's structure" but "run
TalkWithMe 7.1 as it stands plus the canned episode" — a less
ambitious show, not no show. The story-loop placement is the more
reversible half: Placement 2 is an additive upgrade, not a
rewrite.

## Gate (must pass before this ADR is frozen as accepted)

1. On a box: `stream: true` plus `grammar` on our llama-server
   build, one curl — constrained tokens arrive in ordinary SSE
   chunks.
2. On a box: per-round latency, per-persona structure versus one
   shared prefix — convicts or paroles the prompt-cache argument;
   the grammar's per-token overhead on our model.
3. In the audition (Task 5a): dialogue quality with and without the
   screenplay grammar, same prompt, same seed. (The bounded
   scratchpad comparison rides along as a fourth item; it is a
   hypothesis, not a gate.)

None of the three needs the fork to exist. On pass: truth-audit
this ADR against what was measured, then set Status to accepted.
