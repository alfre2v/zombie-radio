# Lessons from the ADR-0003 gate — the screenplay grammar, llama.cpp's prompt cache, and what the model writes

**Date:** 2026-09-22 · **Arc:** MVP prototype · **Branch:**
`alfre2v/adr-0003-gate`
**Type:** discussion — the owner's questions after the ADR-0003 gate
run and the agent's answers, kept verbatim (§1), followed by the
agent's further observations (§2) and the questions the run leaves
open (§3).
**Status:** OPEN — lessons collected (§4, a dated addendum, adds the
emotion-field run of the same evening; §5, a second addendum on
2026-09-23, records the owner's ruling on the emotion field and
explains how one round's request carries the grammar). It
feeds the ADR-0003 truth audit, the fork's stream parser and text
normalizer, and the follow-up run with an emotion field in the
grammar.

*Why a discussion and not the experiment's findings.* The experiment
folder, `docs/experiments/2026-09-22-adr-0003-gate/`, is the record
of what was measured; its `findings.md` carries the verdict. This
document is the conversation that came after: the owner's own
observations and doubts about the results, and the effort to turn
them into lessons we can apply to TalkWithZombies — and to learn how
grammar-constrained generation actually behaves inside llama.cpp.

*Context for the cold reader.* ADR-0003 adopts, for the fork of
TalkWithMe (TalkWithZombies), a new way of generating the show: one
shared script as the LLM's context, a director in code writing each
round's instructions, and the model writing the round's lines under
a GBNF "screenplay grammar" (`Name: text`, one line per speaker)
while the answer streams. Before accepting the ADR, a gate
experiment on a rented A6000 box measured two things on our stack
(llama.cpp build `b11096`, Nemotron Nano 9B v2 Q4_K_M, one server
slot, 16k context):

- **Gate 1** — does the grammar work while streaming, and does it
  bind? Three streamed requests: `main` (the four scientists
  allowed), `control` (only a name absent from the prompt,
  `Operator`, allowed), `nogrammar` (the same request without a
  grammar).
- **Gate 2** — how much prompt work does a round cost? Four "arms"
  replaying the same fixed ten-round script:
  - **A** — TalkWithMe's structure today: four requests per round,
    one per persona, each with its own system prompt and the other
    personas' lines rewritten as `[Name]: text`;
  - **D-off** — the adopted structure: one request per round, the
    cast sheet as system prompt, the script as alternating
    director/script turns, no grammar;
  - **D-on** — D-off with the screenplay grammar;
  - **D-live** — D-on with the model's own output fed back as
    history, the loop the fork would actually run.

The verdict was PASS on every graded item: the grammar streams and
binds; D spends about a quarter of A's prompt time; the grammar cost
0.3 % per generated token. The answers below explain what lies
underneath those numbers.

*Path conventions:* sibling-clone files with full absolute paths;
this repository's files relative to its root. Labels where they
matter: measured / docs-say / believed.

---

## 1. The owner's questions and the agent's answers (2026-09-22, kept verbatim)

*Editorial note.* The answers are the transcript's text, verbatim,
with only these changes: file paths are written from the repository
root (the transcript wrote them relative to the experiment folder);
the one sibling-clone file is given its absolute path; and a few
bracketed notes, marked **[note: …]**, add precision. Nothing was
removed. The owner's questions are quoted before each answer, lightly
tidied (two typos corrected, one code block written inline).

### Topic 0: the run in plain words

> **Owner:** Give me a human-readable short message about the run.
> Was it better than expected? What 5 things we learned? What was
> worse than expected? Any red flags for transplanting this method to
> our forked app?

**The one-line message:** the screenplay grammar works while
streaming and costs almost nothing, and one shared request per round
is about 4× cheaper in prompt time than TalkWithMe's four requests,
and about 6× faster in wall time by round 10. But the reason it's
faster isn't the one we believed.

**Better than expected:**
- **The grammar costs 0.3 %** per generated token. I'd predicted
  under 10 %.
- **The model already writes the format on its own.** With the same
  prompt and seed, no grammar produced identical text. Here the
  grammar was a guarantee, never a correction.
- **The prompt cache works in the real loop.** With the model's own
  output fed back (D-live), 88 % of the prompt was reused by round 10,
  even on this hybrid model.
- **The from-zero deploy took 7 minutes,** not 15.

**Five things we learned:**
1. **The grammar goes in the top-level `grammar` field** of
   `/v1/chat/completions`. It streams (72 chunks) and it binds even
   against the prompt: in the control run, "Operator" was the only
   name allowed, and the model spoke to Ralph and Samantha by name
   instead of writing their lines.
2. **llama.cpp keeps per-persona prompts in RAM and swaps them in,**
   so TalkWithMe's structure is not hopeless on this build. But each
   swap costs about 1.7 s by round 10, and the server's own `timings`
   don't report it. **[note: the 1.7 s is read off one request's
   timestamps in the server log — `A-r10-0-Moira`, between choosing
   the slot at 13.40.800 and starting the task at 13.42.493 —
   runlog entry 14; a script over the whole log was proposed, not
   written.]**
3. **Every request pays a fixed prompt cost of about 350 ms** here,
   whether it evaluates 130 or 270 tokens. The number of requests
   per round matters more than their size.
4. **`/no_think` matters even with a grammar.** Without it, the chat
   template opens a thinking block, and the grammar would force the
   script to be written inside it.
5. **The model's habits:** two trailing spaces before each newline,
   and typographic punctuation (Topic 2).

**Worse than expected:**
- The 350 ms floor. That's slow for this GPU, and I can't explain it
  yet (Topic 1).
- `timings` hide part of the real cost. Gate 2a's criterion was
  based on them, so it understated the difference.
- Early-show cache reuse is only about 55 %.
- The evening lost about an hour to Ubuntu's updater.

**Red flags for the fork:**
- **Editing the history breaks the cache from the edit point on.**
  The director will have to trim the script before it reaches 16k
  tokens. Our history grew about 125 tokens per round, so that's
  roughly 120 rounds, around 40 minutes of show. **[note: the 40
  minutes assumes about 20 seconds of audio per four-line round — an
  assumption, not a measurement.]** Each trim forces a re-evaluation
  from the edit point. On a hybrid model it may be a full
  re-evaluation, because checkpoints are at least 8,192 tokens apart
  by default. Unmeasured.
- **Don't run the chat UI and the show against the same server at
  the same time.** With one slot, they'd make the server swap states
  back and forth, paying the same swap cost A paid.
- **Everything here was measured with placeholder prompts,** 10
  rounds and one seed. The real character bibles make the shared
  prefix bigger.

### Topic 1: the cache, the "evictions", and the context size

> **Owner:** So, why is the memory being evicted from the vRAM into
> the system RAM? Is it because of the caching of multiple prompts?
> Like in this case we have 4 different prompts that keep growing.
> What llama.cpp policy controls this cache and the moving to system
> memory? What about the context size we are running this experiment
> with? What is it? 16k? Are we sure some of the strange behavior is
> not attributable to the prompt getting longer than the max context
> size?

**Nothing was moved out of VRAM because it ran out of room.** Here is
what the server does, as far as the help text and the log show:

- **The slot's working state** (its attention cache plus the model's
  recurrent Mamba state) lives in VRAM.
- **When a request doesn't match the slot's contents,** the server:
  - picks the slot "by LRU" rather than "by LCP similarity"
    (`--slot-prompt-similarity`, default 0.10,
    `docs/experiments/2026-09-22-adr-0003-gate/raw/llama-server-help.txt:702-704`);
  - saves the slot's current state to host RAM
    (`--cache-idle-slots`, default on,
    `docs/experiments/2026-09-22-adr-0003-gate/raw/llama-server-help.txt:441-445`);
  - restores the RAM entry that best matches the new prompt;
  - evaluates only the part that doesn't match.

  That's the swap.
- **Yes, it's because of the four growing prompts.** Every change of
  persona in A means a save plus a restore. D never changes: each new
  prompt extends what's already in the slot, so the log shows "by LCP
  similarity, f_sim_best = 0.855" and nothing moves.
- **The three log lines saying "removing oldest entry"** are
  evictions from the host-RAM cache itself. It's capped at
  `--cache-ram` 8192 MiB
  (`docs/experiments/2026-09-22-adr-0003-gate/raw/llama-server-help.txt:434`).
  They happened exactly at arm boundaries:
  - log line 321: between A's last request and D-off's first;
  - log lines 392–393: between D-off's last and D-on's first.

  **[note: the log is
  `docs/experiments/2026-09-22-adr-0003-gate/raw/llama-log-probe.txt`.]**
- **Entry sizes were 417 MiB to 1.8 GB.** **[note: these are the
  three entries the log shows being evicted; the log reports no other
  sizes.]** I haven't verified why they're so large. My guess is that
  an entry holds the whole saved slot state, including the recurrent
  state and its checkpoints, not just the attention cache.

**Which settings control this:**

| Flag | What it does | Default |
|---|---|---|
| `--cache-ram` | RAM cache size in MiB; `0` disables it | 8192 |
| `--cache-idle-slots` | save the slot's state to RAM when a new request arrives | on |
| `--slot-prompt-similarity` | how closely a prompt must match to reuse a slot directly | 0.10 |
| `--cache-prompt` | reuse the slot's own prefix | on |
| `--ctx-checkpoints` | recurrent-state checkpoints per slot | 32 |
| `--checkpoint-min-step` | minimum spacing between checkpoints, in tokens | 8192 |
| `--parallel` | number of slots | we run 1 |

Our deployment passes none of the cache flags. The llama role only
sets `-hf`, host, port, `-ngl`, `-c` and `--parallel`, so everything
is at the defaults. **[note: `deploy/ansible/roles/llama/tasks/main.yml:30-34`.]**

**Context size: yes, 16k (`n_ctx_slot = 16384` in the startup log),
and we came nowhere near it.**
- The most the slot ever held was 1,635 tokens, about 10 %.
- All 74 requests ended with `truncated = 0`.

So none of the odd behaviour comes from running out of context. The
one real unexplained item is the 350 ms floor. My unverified guess is
recurrent-state handling on this hybrid model. It's worth a small
experiment later: the same probe with checkpoints tuned or turned
off.

### Topic 2: non-ASCII characters

> **Owner:** The very last line of the wire.log is:
> `Samantha: It’s heading northeast. If it’s military, they might
> know more. Over.` My editor is highlighting that character as it
> is non-ascii. I wonder what the effect of those non-ascii
> characters will have in the TTS models. Any opinions on this? One
> possible improvement is to use the grammar to constrain the
> outputs of characters the model can produce. Do you think this is
> wise?

- **The characters:**
  - `’` (U+2019), a typographic apostrophe;
  - `—` (U+2014), an em dash;
  - `…` (U+2026), an ellipsis.
- **They're the model's own habit, not copied from our prompts.** D's
  cast sheet and the fixed script are pure ASCII, yet D's outputs are
  full of `’` and `—`. A's persona prompts do contain `—`, but D
  produced them without any.
- **For the TTS, I believe `’` and `—` are harmless.** They're
  everywhere in web text, and a byte-level tokenizer like Qwen's
  should read them as an apostrophe and a pause. That's untested on
  our engine, and cheap to test: synthesize the same line with `’`
  versus `'` and listen. It takes 5 minutes while the box is up, if
  you want it.
- **The real risk is our own code.** TalkWithMe's sentence cutter
  (`/[^.!?]*[.!?]+/g` in `tts.js`
  **[note: `/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/tts.js:74`]**)
  doesn't treat `…` as a sentence end. The accumulator's end-of-line
  flush would cover it, but it's a trap.
- **Constraining characters with the grammar: I wouldn't.** An ASCII
  allowlist in `text` would make the grammar block prose tokens,
  which is exactly what we chose a screenplay grammar to avoid
  (prompt-structure §7.2 **[note:
  `docs/discussions/2026-09-21-prompt-structure.md`]**). It would
  change how the model samples its prose and rule out accented names.
- **Better: normalize in the fork's line parser, before TTS.** Map
  `’‘` to `'`, `“”` to `"`, `—` to `, ` and `…` to `...`, and trim
  trailing spaces. That's deterministic, doesn't affect the model at
  all, and fits the fork's pytest suite.
- **Keep the grammar structural.** Use it only for a short denylist
  of characters that must never be spoken, as we did with `[` and
  `]`.

### Topic 3: did D, the structure we adopted, measurably help?

> **Owner:** Does the prompt structure we decided to adopt for
> TalkWithZombies (D, right?) bring measurable improvements in
> response time and cache hits?

**Response time: yes, clearly.**
- **Prompt time:** D's per round is 22–26 % of A's, flat across all
  10 rounds.
- **Wall time per round:**
  - A grows from 4.4 s to 9.4 s;
  - D-off takes 1.5–2.0 s;
  - D-live takes 1.35–1.53 s.
- **Time to the first streamed text** (gate 1): 552 ms cold, 271–291
  ms when the prompt was cached.

**Cache hit rate: no difference.** A reused 44 % to 88 %, D-off 52 %
to 88 %, D-live 55 % to 88 %. **[note: rounds 2 to 10; round 1 is a
cold start.]** On this build the hit rate doesn't separate the two
structures. What does:
1. **Requests per round:** 4 against 1, each paying the 350 ms floor
   and its own tunnel round trip.
2. **How the hit is obtained:** A restores from RAM with a costly
   swap; D reuses what's already in the slot.

The router call that A left out would add a fifth request per round,
favouring D further.

### Topic 4: a second run with the emotion grammar

> **Owner:** I think we are in a position to do a second run, as we
> discussed, with a more complex grammar, as we discussed, with
> emotions, and measure the impact in response time and cache hits,
> compared with experiment 1. What do you think? Complexity low to
> run, right?

Agreed. It's low complexity: about an hour of preparation and about 5
minutes of box time. Two clarifications first:

1. **Grammar complexity changes generation cost, not cache hits.**
   Cache reuse depends on the prompt and history, not on the grammar.
   So the comparison is the per-token cost and time per round. I'll
   report reuse too, but expect it to be unchanged.
2. **Run 1's grammar never had to intervene; this one will**, unless
   the prompt teaches the tags. So there are two different things to
   measure, and I'd do both.

**The arms I'd propose, all on the same box, same seed, 10 rounds:**
- **D-simple:** the run-1 grammar, re-run tonight as the baseline.
- **D-emotion-forced:** unchanged prompt plus the emotion grammar.
  This measures the cost of the grammar actually forcing tokens, and
  what the model does when forced.
- **D-emotion-aligned:** a cast sheet that describes the tags,
  history lines carrying tags, plus the emotion grammar. This is the
  configuration the fork would really ship.
- **Plus one streamed request** with tags, to watch them arrive.

**The work:**
- a new experiment folder, because the gate folder seals once its
  verdict lands;
- short criteria and predictions written before the run;
- a cast-sheet variant, and emotions assigned to the 40 fixed lines
  (I'd draft these);
- the `(emotion)` group added to the parser's line pattern;
- generic arm names in the summary script.

**I'd do it tonight while the box is up.** A new box tomorrow costs a
deploy, and possibly another 43 minutes of updater. The gate's
paperwork (findings, ADR audit, PR) needs no box and can come after.

Shall I draft the shape for the second run (folder name, the three
arms, the emotion list from the follow-up, criteria and predictions)
for your review? And do you want the 5-minute `’` versus `'` TTS
listening test in the same session?

> **Owner's reply (2026-09-22):** "yes, we will draft the shape for
> the second run soon." First the gate's results were to be
> persisted — the experiment's findings, and this document.

---

## 2. Further observations (agent, 2026-09-22)

*Lessons the run suggests beyond the owner's five questions. Each one
says what was seen, why it matters, and what to do about it.*

### 2.1 A grammar the model already agrees with costs nothing — and teaches nothing about steering

The grammar works at sampling time: before each token is drawn, the
server removes from the candidates every token that would break the
structure, then samples from what is left. When the model's own
preferred token is already legal, removing the illegal ones changes
nothing, and the same seed draws the same token. That is exactly
what happened: the `nogrammar` baseline wrote the same four lines as
`main`, and D-off and D-on wrote identical text in all ten rounds
(`docs/experiments/2026-09-22-adr-0003-gate/check_outputs.py`,
runlog entry 15). *Measured.*

So the 0.3 % we measured is the cost of the bookkeeping alone —
checking tokens against the grammar — on output the model would have
written anyway. It tells us the mechanism is cheap on this server; it
tells us nothing about what happens when the grammar has to overrule
the model, which is where a richer grammar (an emotion field the
prompt does not mention, a one-line budget) will live. That is the
real question for the second run, and the reason to keep a
"forced" arm in it.

### 2.2 Read the chat template before designing a grammar

The grammar constrains only what the model generates, and generation
starts wherever the chat template leaves off. For Nemotron, the
template (in `docs/experiments/2026-09-22-adr-0003-gate/raw/props.json`,
`chat_template`) ends the prompt differently depending on one word:
with `/no_think` it writes an empty, already-closed `<think></think>`
and the model starts in the answer; without it, it writes an open
`<think>` and the model starts inside its private reasoning. A
grammar that begins with `Name:` would, in the second case, force
the script into what the model believes is scratch space. *Read from
the template; not run.*

The general lesson: the template's last few tokens are part of the
grammar's context. Whenever the model or the template changes (the
Task 5a audition will try other models), read the new template before
trusting the old grammar.

### 2.3 The server's timings measure the work, not the wait

`timings` count what happens inside a task: evaluating the prompt and
generating tokens. Everything before the task starts — choosing a
slot, saving the old state to RAM, loading another — is outside
them, and so is the tunnel. For D those extras were negligible; for
A they grew to seconds. *Measured* (runlog entry 14: flat prompt
time, doubling wall time, and the gap in the server log).

For the fork this means two things. The show's pacing telemetry
(seam question S5) should record wall time as seen by the browser or
the server's HTTP layer, not only the model's `timings`. And any
future latency comparison should grade on wall time, or at least
report it next to `timings` — the gate's criterion read the honest
but incomplete number.

### 2.4 "Cache hit rate" is the wrong headline

A and D reused almost the same share of their prompts (88 % each by
round 10), yet D was six times faster in wall time. What differed was
where the reused state came from: already in the slot for D, fetched
from RAM for A. A hit that costs a copy of hundreds of megabytes is
not the same hit as one that costs nothing. *Measured.*

When we tune the fork (transcript curation, prefetch, a second model
for the audition), watch the cost of reuse, not only its rate: the
server log's "selected slot by LCP similarity" (in place, cheap)
versus "selected slot by LRU" (swap coming) is the quickest tell.

### 2.5 A fixed toll per request argues for whole exchanges

Every request paid about 350 ms of prompt time whatever its size
(130 to 270 new tokens). *Measured*; the cause is not known. With a
toll like that, fewer and bigger requests win, which is one more
reason behind ADR-0003's choice of "the whole exchange per call"
over one request per line. It also tells the director what a
single-line beat costs: an interaction beat that asks for one line
still pays the full toll, so a round should rarely be smaller than
it needs to be.

### 2.6 "Up to four lines" means four

In every round of every D arm the model wrote exactly four lines
(`check_outputs.py`). The prompt said "up to four"; the model heard a
quota. *Measured.* The practical consequence: the director cannot
ask politely for fewer lines and expect them. When a beat needs one
voice — answering a listener, a single stage whisper — the grammar
has to enforce it with its bound (`line{1,1}`), and the prompt
should say the same thing plainly. The line budget is a grammar
parameter, not a suggestion.

### 2.7 Same seed, same prompt, same words

On this build, one slot, no batching, a repeated request with the
same seed produced the same text, even across a restore of the
cached prompt (`main` versus `nogrammar`, D-off versus D-on).
*Measured.* That is good news for Task 7's canned episode, which
counts on the seed to make retakes reproducible. The caveat is the
configuration: more slots or batched requests can break bit-for-bit
determinism, so the canned episode should be recorded with the same
settings it will be replayed with.

### 2.8 How the cache follows a growing script — and why normalizing the history is free

The template renders the model's past replies without the
`<think></think>` it put in front of them when they were generated.
So when round k+1 arrives, the cached state agrees with the new
prompt only up to the start of round k's reply; the reply itself is
evaluated again, this time as history, together with the new
directive. The counts are consistent with this — D-live evaluated
169–184 tokens per round while generating 72–82 — though the exact
split was not measured. *Believed, from the template and the counts.*

One practical consequence: since the reply is re-read as history
anyway, the fork can write the NORMALIZED text into the history
(plain apostrophes, trimmed spaces) at no extra cache cost. It would
also show the model plain punctuation in its own past lines, which
may gently wean it off the typographic habit. Worth a line in the
fork's design notes; cheap to verify when the fork runs.

*[note 2026-09-23, owner ruling: the history is NOT normalized. It
keeps exactly what the model wrote; normalization, trimming and quote
removal apply only to the text heading for the voice (every event the
browser receives — with streaming TTS the voice is fed from the
`token` events). The reason: rewriting the model's own past lines in
a style it would not produce steers it (§4.4 — what it reads, it
imitates), the same kind of interference Topic 2 rejected for the
grammar; and the cost argument above cuts both ways — the reply is
re-read whether raw or normalized. This suggestion had drifted into
the TODO as if decided; it was never ruled on until now.]*

### 2.9 The model's punctuation comes from training, not from us

The cast sheet and the fixed script are plain ASCII, and still the
model wrote curly apostrophes, em dashes and ellipses in every arm.
*Measured* (the texts in `docs/experiments/2026-09-22-adr-0003-gate/raw/probe/`).
Prompting will not reliably change a habit this deep; a normalizer
in the parser will. (Topic 2 above has the mapping.)

---

## 3. What the run leaves open

- **The 350 ms floor.** Why does a request's prompt phase cost the
  same for 130 and 270 tokens? Candidates: recurrent-state handling
  on the hybrid model, checkpoint creation, a fixed per-request setup
  cost. A small experiment: the same probe with `--ctx-checkpoints 0`,
  with a smaller `--checkpoint-min-step`, and with `--cache-ram 0`,
  one flag at a time.
- **Why the RAM cache entries are so large** (417 MiB to 1.8 GB for
  prompts of a few hundred to about 1,600 tokens).
- **What a history edit costs on this hybrid model.** Transcript
  curation (trimming or summarizing old rounds) will break the
  cached prefix; whether the server then re-evaluates from the edit
  or from zero depends on its checkpoints, spaced at least 8,192
  tokens apart by default. Needs measuring before the director's
  curation is designed.
- **What a grammar costs when it steers.** The emotion-field run
  (`docs/follow-ups.md`, "Emotion field in the screenplay grammar").
- **Whether our TTS engine minds typographic punctuation** — a
  five-minute listening test, `’` versus `'`, whenever a box is up.
- **Single-line beats.** Does the model behave with `line{1,1}`,
  and does the prose suffer when it must stop after one line?

---

## 4. Addendum, 2026-09-22 (later that evening) — the emotion-field run

*What changed after a second run on the same box, one question from
§1 Topic 4 answered, and one belief from §1 Topic 2 retracted. §1
stays verbatim; this section is where the evening talks back to it.*

### 4.1 The run, in brief

The follow-up of §1 Topic 4 ran at 19:15, about eighty minutes after
the gate, on the same box and model:
`docs/experiments/2026-09-22-emotion-grammar-cost/` (its `findings.md`
has the numbers and the verdict). It added a required emotion tag to
every line — `Name (emotion): text`, one of nine emotions (calm,
happy, sad, afraid, terrified, doubtful, angry, urgent, exhausted) —
and compared five arms of ten rounds each:

- **D-simple** — the gate's shared script with the simple grammar,
  re-run as the baseline (its requests byte-identical to the gate's);
- **D-forced** — the same plain prompt, which never mentions
  emotions, with the emotion grammar forcing the tags;
- **D-aligned-off** — a cast sheet that teaches the tags, history
  lines that carry them, no grammar;
- **D-aligned** — the same, with the emotion grammar: what the fork
  would ship;
- **D-aligned-live** — the same, with the model's own tagged output
  fed back.

In one breath: taught, the field is free (0.5 % per token, the E1
graded item, PASS), the model tags 40 lines of 40 on its own and
spreads them over eight of the nine emotions; forced on a prompt
that never mentions it, the same grammar costs 10.4 % per token.

### 4.2 The owner's reading: imposing a grammar fights the model unless the prompt describes it

When the owner asked what the most interesting thing learned was,
his own answer was this one, and it is the practical lesson of the
evening. A grammar that says the same thing as the prompt is a
guarantee that never has to act: in D-aligned it did not change a
single word of D-aligned-off's text, in any of the ten rounds. A
grammar that says something the prompt does not is a fight, and the
fight has a price and side effects (4.3 and 4.4).

For TalkWithZombies this becomes a rule for the director: every
constraint it writes into a round's grammar — the emotion tag, a
narrowed speaker list, a one-line budget — must also be said in that
round's directive. The gate's `control` run was already an example
of what happens otherwise: with only `Operator` allowed and the
prompt asking for the scientists, the model obeyed the grammar and
had the Operator speak *to* Ralph and Samantha instead.

### 4.3 The two prices of a grammar — and the likely reason

Measured this evening, per generated token:

- **about 0.3–0.5 %** when the model already wants what the grammar
  allows (the gate's D-on; this run's D-aligned);
- **10.4 %** when the grammar has to overrule it (D-forced), steady
  in every round (12.38–12.54 ms per token against about 11.3).

*The likely reason — believed from the agent's memory of llama.cpp's
sampler code, not yet read in our build:* by default the server does
not apply the grammar to the whole vocabulary at every step. It
samples a token the ordinary way, checks only that one token against
the grammar, and keeps it if it is legal. Only when the token is
rejected does it apply the grammar to every candidate — tens of
thousands of them — and sample again. Agreement costs one check;
disagreement costs a full pass. In D-forced, every line meets the
grammar where the model wanted `Name:` and the grammar demands
`Name (`, so the expensive path runs a few times per line, every
line. The numbers fit this picture; reading the sampler in the
llama.cpp source would confirm or kill it.

This also retires a prediction: the agent had expected forcing to
"change which token wins, not how much the checking costs". Both
change.

### 4.4 What the model reads, it becomes — until the examples say otherwise

In D-forced's first round, where the history is still empty, the
model met the forced tags by rewriting its whole line format as
quoted dialogue — `Daniel (calm): "Lights flickered east wing, no
further reports. Over."` — as if it had concluded, from its own
forced words, that it was writing a screenplay with quotations. That
is §7.2 of the prompt-structure discussion
(`docs/discussions/2026-09-21-prompt-structure.md`) seen on our own
model: what shifts the model is not the mask but what it sees itself
having written.

The run also showed the limit of that effect. From round 2 on, with
plain lines in the history to copy, the quotation marks disappeared,
though the tags were still forced on every line. The examples in the
context outweighed the pull of the forced tokens. Two practical
consequences: the history is the strongest steering wheel we have —
stronger than the grammar's side effects — and the first round of a
show, with no examples yet, is where the prompt must do all the work.

*A correction on record:* in the conversation the agent first said
the model put "Over." inside quotation marks five times out of
forty. The record disagreed: four times, all in round 1; the fifth
line without "Over." was a plain omission in round 6 (the run's
runlog, entry 6).

### 4.5 The model uses the emotions — it does not parrot them

Eight of the nine emotions appeared in every tagged arm, the most
frequent at 32 % (forced, `calm`), 20 % (taught, `terrified`) and
18 % (live, `sad`). Taught, the model never once chose `happy` in a
zombie outbreak. Whether each emotion fits its line is a listening
question for the Task 5a audition, and whether the voice can express
it is seam question S6 — but the field is carrying information, not
noise.

### 4.6 A belief that died: typographic punctuation is not harmless for our TTS

§1 Topic 2 said: "For the TTS, I believe `’` and `—` are harmless." It
was wrong. In the side quest (the run's runlog, entry 5) the same
line was synthesized twice in the same voice and seed, differing
only in one character, and the owner listened:

- with `’` or `—` anywhere in the line, the voice ignores the final
  period and makes no pause before "Over." — those clips are 0.64 s
  shorter, about the length of the missing pause;
- the ellipsis `…` did no harm; if anything it sounded slightly more
  alive.

The damage lands far from the character that causes it — the
character sits mid-line, the missing pause is at the end — so the
engine changes the rhythm of the whole line, by a mechanism not
known to us. And the model writes `’` all the time. The consequence
moves normalization from "better" to **required**: the fork's parser
maps `’‘` to `'`, `“”` to `"` and `—` to `, ` before any text reaches
the TTS. The ellipsis may stay for the voice's sake, but maps to
`...` anyway because TalkWithMe's sentence cutter does not treat `…`
as a sentence end
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/tts.js:74`).

### 4.7 What this means for the fork

- **The simple grammar: proceed, high confidence.** It binds and
  streams (the gate), costs about nothing, the model complies unaided
  and deterministically, and the cache works through the live loop.
- **The emotion grammar: proceed as an option, taught in the
  prompt.** Build the grammar builder with the emotion rule behind a
  yaml switch from day one; the agent leans to default on, with the
  parser stripping the tag before the TTS, so the tags become data
  for S6 even before the voice can use them. The adoption decision
  stays the owner's.
- **The director's rule:** say in words every constraint the grammar
  enforces (4.2).
- **The parser's duties:** strip the `(emotion)` tag before the TTS
  but keep it in the history the model reads; normalize typographic
  punctuation (4.6); trim trailing spaces; tolerate a line wrapped in
  quotation marks.
- **The first request of a conversation pays a swap.** The first
  streamed request after the idle hour, arriving at a slot that held
  another conversation, waited 1,850 ms for its first token though
  its prompt phase took 365 ms — most likely the state swap of the
  gate's arm A. Harmless mid-show, where one conversation owns the
  slot; worth knowing for the first round and for anything that
  shares the server.
- **Debug with what the model reads, not only with the messages**
  (4.9): a debug switch in the fork that fetches the rendered prompt
  for a round — through `/apply-template` if it exists, otherwise the
  server's verbose log — and writes it next to the round's messages.
  The fork's own wire log should also print the grammar in full, or
  at least name its rules, not just the speaker list.

### 4.8 Open, added to §3

- **Read llama.cpp's sampler** to confirm or kill the explanation of
  4.3 (check the chosen token first, full pass only on rejection).
- **The cost of the director's per-round constraints in practice:**
  narrowing the speaker list and the line budget, said in words and
  enforced by the grammar, should stay in the cheap regime — to be
  seen in the fork's first runs.

### 4.9 What the model actually reads — three layers (2026-09-23)

*The owner's question, the next morning: is `wire.log` what the LLM
receives, apart from the separators? It is not, and not only because
of the separators.* Between our script and the model there are three
layers, and each file in the experiment folders shows a different
one:

```
our script ──HTTP──> llama-server ──chat template──> the model
            layer 1                 layer 3
   raw/probe/*.json "request"   rendered text → tokens
   raw/wire.log (layer 1 made readable, with omissions)
```

- **Layer 1 — what our script sends over HTTP.** One JSON object per
  request: `model`, `max_tokens`, `temperature`, `seed`,
  `cache_prompt`, `stream`, the full grammar text, and `messages` — a
  list of role/content pairs. It is saved exactly in the `request`
  field of each `raw/probe/<name>.json` (and in
  `raw/stream/<label>.request.json` for streamed requests), together
  with the full response. These JSON files are the record of truth:
  every number in both experiments' findings is computed from them.
- **`wire.log` — layer 1 made readable,** written live so the owner
  could follow the traffic with `tail -F`. For each request: a header
  line of the agent's own making, each message as `[role] content`,
  then the answer with the server's counters. It omits temperature,
  `cache_prompt` and the grammar itself — and its header summarizes
  the grammar by the speaker list alone (`grammar=Daniel|Moira|Ralph|Samantha`),
  so **the emotion grammar and the simple one look the same in it**.
  A flaw, recorded in both experiments' runlogs; the JSON has the
  truth. It is not an input to any number.
- **Layer 3 — what the model reads.** Inside the server, the chat
  template (the Jinja text in `docs/experiments/2026-09-22-adr-0003-gate/raw/props.json`,
  `chat_template`) turns the message list into one text, and the
  tokenizer turns that into tokens. Neither file shows it.

**The last interaction of the evening, as the model read it.**
`D-aligned-live-r10` (19:17:23): 20 messages, 7,472 bytes of JSON,
rendered into 6,580 characters and read as 1,635 tokens (the server's
own count). Its beginning and end, reconstructed:

```
<SPECIAL_10>System
You write a live radio play. Four scientists are trapped in a besieged research lab …
…
Format: write the next lines of the script, one line per transmission, as `Name (emotion): spoken words`. …
<SPECIAL_11>User
Radio traffic: the generator coughed twice and the lights flickered across the east wing. Write the next lines …
   […]
<SPECIAL_11>Assistant
Daniel (angry): One quarter? We’re running on empty. Over.  
Moira (sad): The generators won’t last the night. Over.  
Ralph (terrified): We need to find a refill. Now. Over.  
Samantha (exhausted): Someone get the truck. We can’t stop here. Over.
<SPECIAL_12>
<SPECIAL_11>User
Radio traffic: a helicopter passes low overhead without slowing down. Write the next lines …
<SPECIAL_11>Assistant
<think></think>
```

**Six ways the model's view differs from `wire.log`:**

1. **`/no_think` is gone.** It is the first line of the system
   message in the JSON and in `wire.log`, but the template deletes it
   before the model reads anything. It works only as a switch — it
   decides how the prompt ends (point 3).
2. **The role labels are the model's own markers.** `[system]`,
   `[user]` and `[assistant]` are the agent's labels; the model reads
   Nemotron's special markers: `<SPECIAL_10>System`,
   `<SPECIAL_11>User`, `<SPECIAL_11>Assistant`, and `<SPECIAL_12>`
   closing each assistant turn — the model's end-of-turn token, the
   same one it emits when it finishes an answer (`eos_token` in
   `props.json`). User turns get no closing marker. Each marker is
   believed to be a single token of the model's vocabulary, not the
   letters shown.
3. **The ending exists in neither file.** The template appends
   `<SPECIAL_11>Assistant\n<think></think>` — an assistant turn with
   an empty, already-closed thinking block — and the model starts
   writing right after it. Without `/no_think` it would append an
   open `<think>` instead (§2.2).
4. **The grammar never reaches the model.** It travels in the JSON
   but is not part of the text the model reads; the server applies it
   while choosing each token (§4.3).
5. **The settings are not text either.** Temperature, seed, the token
   cap and caching are instructions to the server.
6. **One likely invisible extra:** a start token `<s>` (`bos_token` in
   `props.json`), believed to be added during tokenization.

What is faithful across all three layers are the message contents —
including the model's own habits fed back into its history verbatim:
the two trailing spaces after `Over.` and the curly `’`. Every round,
the model re-reads its own quirks.

**How the rendering was reconstructed** — offline, the box being
hibernated, with the Jinja engine that ships in the project's `.venv`
(an Ansible dependency) applied to the template the server reported.
llama.cpp uses its own Jinja implementation, so tiny whitespace
differences are possible; the structure is the server's:

```bash
.venv/bin/python - <<'EOF'
import json, jinja2
props = json.load(open("docs/experiments/2026-09-22-adr-0003-gate/raw/props.json"))
req = json.load(open("docs/experiments/2026-09-22-emotion-grammar-cost/raw/probe/D-aligned-live-r10.json"))["request"]
print(jinja2.Environment().from_string(props["chat_template"]).render(
    messages=req["messages"], add_generation_prompt=True, tools=None,
    bos_token=props["bos_token"]))
EOF
```

**For the fork.** When a round misbehaves, the messages are not
enough to see why — the model reads layer 3. Two ways to get it from
the live server: an `/apply-template` endpoint that returns the
rendered text for a list of messages (*believed* to exist in this
llama.cpp build — to verify in the server README before relying on
it), and the server's `-v` / `--verbose` flag, "log all messages,
useful for debugging" (docs-say, `raw/llama-server-help.txt:209`),
which would have to be switched on through the playbook. Listed in
§4.7.

### 4.10 Where the open questions stand (2026-09-23)

*This section is the lasting home of the open questions of this
stage of the build. Their to-do copies live in `docs/follow-ups.md`
and in `docs/TODO.md`, and are deleted when done; when one is
answered, the answer comes back here as a dated note, so the record
never goes quiet.*

**Answered since §3 was written:**

- *What a grammar costs when it steers* — 10.4 % per token when it
  must overrule the model (4.3), and a changed writing style when
  the history has no examples to follow (4.4).
- *Whether our TTS minds typographic punctuation* — it does: a `’`
  or `—` anywhere in a line makes the voice drop the pause before
  "Over." (4.6).

**Still open — llama.cpp and the model** (build `b11096`, the
hybrid Nemotron Nano 9B v2; tracked in the follow-up "llama.cpp
unknowns the ADR-0003 gate left open"):

1. **The fixed prompt cost of about 350 ms per request**, the same
   for 130 tokens as for 270 — slow for an A6000. Suspects: the
   handling of the recurrent (Mamba) state per request, checkpoint
   creation, a fixed setup cost. It is why one request per round
   beats one per line (§2.5). *When:* show-latency tuning, or when
   the audition swaps the model.
2. **Why the host-RAM cache entries are so large** — 417 MiB to
   1.8 GB for prompts of a few hundred to about 1,600 tokens.
   *When:* the same.
3. **What a history edit costs on this hybrid model.** Trimming the
   script breaks the cached prefix from the edit point on; with
   recurrent-state checkpoints at least 8,192 tokens apart by
   default, the server may re-read far more than the edited part.
   *When:* before the director's transcript curation is designed
   (TODO Task 6b) — the design depends on it. *Reframed 2026-09-23:
   the owner ruled for a midpoint trim ([discussion 2026-09-23]
   show-engine-design §2), so the design no longer waits on this; what
   remains is how long the pause after a trim lasts, measured on the
   box during Task 6b with a low `show.context_budget`.* *Answered
   2026-09-24 (measured on the box, build `b11096`, the fork's trim
   of step 2.2 with `show.context_budget` 1500, two trims per drive,
   two identical drives): the trims cut the script right after its
   first 516 tokens (the cast sheet and the first two rounds). The
   re-read itself is small: the cache was reused for 512 tokens and
   only what followed was read again — 308 and 316 tokens, in 474 and
   453 ms, against about 365 ms for a normal round. But the server
   log shows where the pause goes: between choosing the slot and
   starting the work — a phase `timings` does not report, the one
   where the ADR-0003 gate saw about 1.7 s of saving and restoring
   the slot's state in host RAM — three of the four trims spent
   1,498, 1,348 and 1,326 ms (the fourth 174 ms, unexplained),
   against about 1 ms for a normal round. It comes with a low
   `f_keep` in the log (0.37-0.38 after a trim; a new run's first
   round shows 0.22 and pays it too, 1.1-1.4 s), and the very next
   round is back to about 1 ms. So a trim costs about 1.5 s once. At
   the default budget (14,000 tokens, about 80 per round) the first
   trim comes roughly 50 minutes into a show, then about every 25
   (estimates, at 20 s of audio per round) — a pause that can hide
   in the listening beat. The owner's hunch pointed at the swap. That
   the reuse stopped at 512 rather than 516 is believed to be a block
   size of the cache, not measured. Separately, one stall of 1.5 s
   happened before a request even reached the server (round 8 of the
   first drive only), cause unknown (follow-ups: "Pauses the model
   server's timings do not show").*
4. **Why agreement is nearly free and disagreement costs ~10 %** —
   believed: the sampler checks the chosen token first and applies
   the grammar to the whole vocabulary only when that token is
   rejected (4.3). *When:* the next time a grammar change is
   weighed on cost; answered by reading `common/sampling.cpp` at
   the build we serve.
5. **Whether this build has an `/apply-template` endpoint** —
   believed (4.9). *When:* before the fork's debug switch (TODO Task
   6b). *Answered 2026-09-23 (measured): yes — it returns the
   rendered prompt in about 120 ms without generating and without
   occupying the slot, and its output matches the offline
   reconstruction of 4.9 (§5.1).*

**Still open — the show engine** (answered by building and running
the fork):

6. **The cost of the director's per-round constraints in practice**
   — a narrowed speaker list and a line budget, said in words and
   enforced by the grammar, should stay in the cheap regime (4.2,
   4.8). *When:* the fork's first runs.
7. **Single-line beats** — how the model behaves when the grammar
   bounds a round to one line (`line{1,1}`), and whether the prose
   suffers when it must stop there. *When:* the first interaction
   beat in the fork; the audition.
8. **The bounded scratchpad** — whether one non-spoken note line
   before the script improves coherence at an inaudible latency
   cost; it must be taught in the cast sheet, or the test measures
   a forced grammar (4.2). *When:* the Task 5a audition (follow-up
   "Bounded scratchpad before the script").

## 5. Addendum, 2026-09-23 — one round's request: the grammar, the emotion switch, and the flight recorder

*Context.* Written the day the fork TalkWithZombies was created
(TODO Task 6a) and before the show engine's design (Task 6b). The
agent brought two small items to settle first: whether the fork
adopts the emotion field of §4, and whether this llama.cpp build has
the `/apply-template` endpoint the fork's debug switch would use
(§4.10, question 5). The owner ruled on the first and asked how the
pieces fit together; the agent's answer is kept verbatim at the
owner's request (§5.3), after the ruling and the evidence behind it
(§5.1) and the owner's questions (§5.2).

### 5.1 The ruling, and what it rests on

- **Ruling (owner, 2026-09-23): the emotion field is built behind a
  yaml switch, default ON.** The options weighed: (1) a switch,
  default on; (2) the same switch, default off, dormant until
  something consumes the tag; (3) left out of the timebox. If the
  timebox runs tight at its day-1.5 checkpoint, flipping the switch
  falls back to (2) without touching code.
- **The measured case** (§4, run 2): taught in the cast sheet, the
  model writes the tag on 40 of 40 lines with no grammar at all;
  with the grammar on, the text is identical, character for
  character, for ten rounds, at 0.5 % per token. Forced on a cast
  sheet that does not describe it, the grammar costs 10.4 % and
  round 1 drifts into quoted dialogue. Each arm used eight of the
  nine emotions.
- **New finding: our TTS engine takes no emotion input** (measured
  2026-09-23, tts-serve's `/capabilities` through the tunnel). The
  engine, faster-qwen3-tts, advertises exactly these parameters:
  `text`, `audio_base64` (the reference clip), `reference_text` (its
  transcript), `language`, `seed`, `temperature`, `top_p`,
  `repetition_penalty`. It copies the delivery of the reference
  clip. So the tag can reach the voice only through **clip
  selection**: a second reference clip per actor in another
  register, chosen by the tag — the owner's optional second voice
  sample (TODO owner action queue) and Task 5b's territory, not the
  timebox's.
- **What the tag does before then:** it rides in the history the
  model reads (whether that steadies the tone across rounds is
  believed, not measured); it can show as a caption on the `/show`
  page; and it is a pacing signal the director could read later (the
  show arc).
- **What it costs in the timebox:** one grammar rule, one paragraph
  in the cast sheet (the teaching — §4.2), the parser removing
  `(mood)` before the text reaches the TTS while keeping it in the
  history (its own test: a failure would make the voice say
  "terrified"), and tests for both switch positions.
- **`/apply-template` verified** (measured 2026-09-23, through the
  tunnel): the endpoint exists on build `b11096`, answers in about
  120 ms without generating and without occupying the slot, and
  renders a two-round script exactly as §4.9 reconstructed it
  offline — `/no_think` removed, the `<SPECIAL_1x>` turn markers,
  `<think></think>` at the end. One new detail: earlier assistant
  turns are rendered plainly, with no think block, so the model
  reads back exactly the lines we wrote into the history.

### 5.2 The owner's questions (2026-09-23, verbatim)

*One typo corrected ("fell" → "feel").*

> #### 2a. The emotion field: should the script lines carry a mood tag?
>
> Very good presentation of the topic.
>
> I agree with you, I like Option: "(1) Build it behind a yaml
> switch, default ON" .
>
> However, for my education: how would you build "(2) Build it
> behind a switch, default OFF", I do not see how you can put this in
> a switch in the app? Can you change the llama response grammar
> on/off like that?
>
> How do you actually tell llama.cpp you want to use the grammar?
> Adding a (tag? section? fragment?) somewhere at the top of the
> system prompt declaring the grammar, right? Show me an example how
> it's actually done.
> I assume this grammar has to be added in each and every request to
> llama.cpp, correct?
>
> #### 2b. /apply-template: resolved, it exists
>
> I have to admit I do not follow, what is this `/apply-template`
> route? Is this a llama.cpp service route?
> What check did you do? Why is this useful to us?
>
> What is this: "the debug switch is off by default;"... What is this
> debug switch you are talking about here?
>
> Ok, I am reading your "Proposed design:"... So, this apply-template
> route is related to a debug capability you want to add? Correct?
>
> I like what I see, I just have trouble connecting all the pieces
> into a coherent narrative about what you are proposing... I see
> good fragments, without a proper introduction... But I feel it's
> all what I want... Please give me a bit more to connect the pieces.

### 5.3 The agent's answer (2026-09-23, verbatim)

*Editorial note.* The transcript's text, verbatim; only its headings
are demoted one level to fit this document. Nothing was removed.

I jumped into the middle of this with neither topic introduced. Here's the whole picture first, then each piece.

#### The picture in one paragraph

Every round of the show, our app (the director) sends **one HTTP request** to llama.cpp, and that request has **two separate parts**:
- **`messages`:** what the model **reads**. That's the cast sheet, the director's instructions, and the script lines so far.
- **`grammar`:** a rulebook the model **never reads**. llama.cpp uses it to block any next word that would break the format while the model writes.

Our code builds both parts fresh for every round. Two small 6b features come from that:
- the **emotion switch** changes what our code puts into both parts;
- the **debug switch** saves both parts to disk, plus the exact text the model read, so we can inspect a round afterwards.

#### 1. How we tell llama.cpp to use a grammar

It isn't in the system prompt. It's **its own field in the request body**, next to `messages`. Here's a real request from run 2 (round 2 of arm D-aligned), with the messages shortened:

```json
{
  "model": "default",
  "messages": [
    {"role": "system",    "content": "/no_think\nYou write a live radio play. Four scientists are trapped …"},
    {"role": "user",      "content": "Radio traffic: the generator coughed twice and the lights flickered …"},
    {"role": "assistant", "content": "Daniel (calm): Generator two is sulking again, so I'm rerouting …"},
    "… 1 more message"
  ],
  "max_tokens": 200,
  "temperature": 0.8,
  "seed": 42,
  "cache_prompt": true,
  "stream": false,
  "grammar": "root    ::= line{1,4}\nline    ::= speaker \" (\" emotion \"): \" text \"\\n\"\nspeaker ::= \"Daniel\" | \"Moira\" | \"Ralph\" | \"Samantha\"\nemotion ::= \"calm\" | \"happy\" | … | \"exhausted\"\ntext    ::= [^\\n\\[\\]()]+\n"
}
```

What llama.cpp does with the two parts:
1. **The chat template** turns `messages` into one long text. That text is all the model ever reads.
2. **The model** scores every possible next token.
3. **The grammar filter** removes every token that would break the rules. For example, right after `Daniel (`, only tokens that start one of the nine moods survive.
4. **The sampler** picks among the survivors, and the loop repeats for the next token.

The model never sees the rules, which is why the cast sheet has to describe them in words. Without that description, the model's favourite next words keep getting blocked. That's where run 2's 10.4 % cost and the drift into quoted dialogue came from.

**Yes, every request carries its own grammar.** The server remembers none between requests. That's what we want: the director changes the rules every round. Round 7 might allow only Ralph and Samantha, with at most two lines:

```
root    ::= line{1,2}
speaker ::= "Ralph" | "Samantha"
```

#### 2. What "the switch" is

It's a setting in the app's own `settings.yaml`, for example:

```yaml
show:
  emotion_tags: true
```

llama.cpp never knows it exists. Our code reads it every round and uses it in three places:
1. **The grammar builder** writes one of two rule sets:
   - off: `line ::= speaker ": " text "\n"`
   - on: `line ::= speaker " (" emotion "): " text "\n"`, plus the `emotion ::=` rule.
2. **The cast sheet** includes, or leaves out, the paragraph that explains the tag. That keeps the words and the grammar in agreement, per lesson §4.2.
3. **The parser** expects either `Name (mood): text` or `Name: text`.

So on and off is a choice our code makes while writing each request. Option 2 would be the same code with `false` in the yaml.

#### 3. `/apply-template` and the debug switch

**The problem it solves.** When the show misbehaves, the first question is always "what exactly did the model get?" Today's empty Luna bubble shows how costly the answer can be: it took SSH, box logs and a reproduction. During 6b, and later when auditioning other models (Task 5a), that question will come up constantly.

**The answer has three layers** (lessons §4.9):
1. **What our code sends:** the JSON above. Easy for us to log.
2. **What the model actually reads:** the long text the chat template produces from `messages`. This happens inside llama.cpp, and it changes things. It removes `/no_think`, adds special markers, and ends with `<think></think>`.
3. **The grammar**, which steers word choice but is in no text at all.

We can't see layer 2 unless llama.cpp shows it to us.

**`/apply-template` is llama.cpp's own route for that.** It's a URL on the same server as `/v1/chat/completions`, `/health` and `/slots`. You send it the same `messages`, and it answers with the text it would feed the model, without running the model.

**The check I ran** sent it a tiny two-round script. In 120 ms it answered with this (shown with real line breaks):

```
<SPECIAL_10>System
CAST SHEET: Moira, Ralph.
<SPECIAL_11>User
DIRECTOR: round 1, Moira then Ralph.
<SPECIAL_11>Assistant
Moira: Samples ready. Over.
Ralph: Doors holding. Over.
<SPECIAL_12>
<SPECIAL_11>User
DIRECTOR: round 2, Ralph only.
<SPECIAL_11>Assistant
<think></think>
```

That settled three things:
- our llama.cpp build has the route (the TODO said "verify first");
- the output matches what I reconstructed offline on 09-22: my `/no_think` was removed, and the prompt ends with `<think></think>`;
- it doesn't occupy the model's single slot.

**The debug switch** is item "Debug switch" in the TODO's 6b plan: a second yaml setting, e.g. `show.debug: false`. When it's `true`, each round also writes one file next to the room's saved chat, holding:
- the messages we sent (layer 1);
- the grammar, in full (layer 3);
- the text the model read, from `/apply-template` (layer 2);
- the raw reply.

It's off by default because it costs one extra request per round (about 0.1 s) and the files pile up. You turn it on when diagnosing something or during the audition.

**In short, it's a flight recorder for the show.** With it on today, the Luna diagnosis would have been one file to open.

#### How it fits together

Both switches are knobs on the same machine, the code that builds each round's request. `emotion_tags` changes **what goes in**. `debug` **records what went in**, including the one layer only llama.cpp can show us.

Is anything still disconnected? If not, we can move to item 3, the phases of 6b.

## 6. Update trail

- **2026-09-22** — Document created after the ADR-0003 gate run: the
  owner's five questions and the agent's answers kept verbatim (§1,
  with bracketed precision notes and repository-root paths), the
  agent's further observations (§2), and the open questions (§3).
  File name proposed by the agent instead of the owner's working
  title `{date}-lessons-grammar-llm.md`, to say what the lessons are
  about.
- **2026-09-22 (later)** — §4 added: a dated addendum after the
  emotion-field run (`docs/experiments/2026-09-22-emotion-grammar-cost/`)
  — the owner's reading (a grammar fights the model unless the prompt
  describes it), the two prices of a grammar and their likely reason,
  the style leak and its limit, the retracted TTS belief of §1 Topic
  2, what it means for the fork, and two new open questions. The
  update trail renumbered from §4 to §5.
- **2026-09-23** — §4.9 added at the owner's question ("is `wire.log`
  what the LLM receives?"): the three layers between our script and
  the model, the evening's last request rendered through the server's
  chat template (reconstructed offline), six differences from
  `wire.log`, and a debugging note for the fork (also in §4.7).
- **2026-09-23 (later)** — §4.10 added at the owner's request: the
  lasting home of this stage's open questions — two answered since
  §3, eight still open, each with when it matters and where it is
  tracked; answers return here as dated notes.
- **2026-09-23 (evening)** — §5 added, a second dated addendum,
  after the fork was created and before the show engine's design:
  the owner's ruling on the emotion field (a yaml switch, default
  on) with the evidence behind it, including the new finding that
  our TTS engine takes no emotion input (§5.1); the owner's
  questions (§5.2) and the agent's answer (§5.3) kept verbatim at the
  owner's request — how one round's request carries the grammar,
  what the emotion switch is, and `/apply-template` with the debug
  switch as a flight recorder. §4.10's question 5 answered with a
  dated note. The update trail renumbered from §5 to §6. Same
  evening: §4.10's question 3 reframed with a dated note, after the
  owner ruled for a midpoint trim ([discussion 2026-09-23]
  show-engine-design §2).
