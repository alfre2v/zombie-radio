# Lessons from the ADR-0003 gate — the screenplay grammar, llama.cpp's prompt cache, and what the model writes

**Date:** 2026-09-22 · **Arc:** MVP prototype · **Branch:**
`alfre2v/adr-0003-gate`
**Type:** discussion — the owner's questions after the ADR-0003 gate
run and the agent's answers, kept verbatim (§1), followed by the
agent's further observations (§2) and the questions the run leaves
open (§3).
**Status:** OPEN — lessons collected, no decision taken here. It
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

## 4. Update trail

- **2026-09-22** — Document created after the ADR-0003 gate run: the
  owner's five questions and the agent's answers kept verbatim (§1,
  with bracketed precision notes and repository-root paths), the
  agent's further observations (§2), and the open questions (§3).
  File name proposed by the agent instead of the owner's working
  title `{date}-lessons-grammar-llm.md`, to say what the lessons are
  about.
