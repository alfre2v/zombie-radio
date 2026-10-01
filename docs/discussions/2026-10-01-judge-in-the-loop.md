# A judge in the loop — typed questions about the dialogue, answered fast, steering the director

**Date:** 2026-10-01 · **Arc:** MVP prototype (an idea for after it) · **Branch:**
`alfre2v/context-32k`
**Type:** discussion — the owner's idea of a fast "System One" judge that answers
the director's typed questions about what was said; the agent's research into
CLM, the model that prompted it; the agent's judgment and pushbacks; the owner's
answer.
**Status:** IDEA, NOT FOR THE DEMO — recorded in full for after 2026-10-08 (the
owner: "We are not going to execute on this before the demo. I just want to save
this idea well if we determine it is valuable."). The owner's leaning (§5): a
small LLM of its own as the judge (maybe a 3B), not Nemotron (the cost to the
show's cache) and not CLM yet (unproven). An experiment decides (§6). Pointed to
from `docs/roadmap.md`, "Ideas / parking lot".

## §1. The owner's idea (verbatim, 2026-10-01)

The owner, with a description of CLM pasted from elsewhere (kept here as the
owner gave it; its numbers were then checked by the agent, §2):

> Now, here is a new idea to record as a follow-up or if considered to far off,
> in roadmap. Let's discuss it among ourselves before saving it:
>
> There is new excitement in the field about "System One AI models", prime
> example being Jev (recent, probably after your knowledge cut off), but there
> are also local open source version of similar capabilities. Some context for
> you (but feel free to do your own quick search to learn more facts):
>
> ```
> CLM-8B is an ultra-fast open-weight "System One" decision-making AI model developed by researchers from Stanford and Nvidia Research that scores and ranks agent actions instead of generating text token by token.
> How It Works
> • Dual-Encoder Design: It utilizes a frozen Qwen3-8B base encoder combined with two small, trainable projection heads (roughly 20 million parameters each) disaggregating state and action representations.
> • Contrastive Scoring: Instead of reading a prompt and generating a sequence, it embeds the current state and compares it via dot-product similarity against candidate actions.
> • Action Caching: Reusable action representations can be computed once and cached, enabling up to 9× faster inference speeds compared to cross-reader models like Jev.
> Key Performance Details
> • Speed & Latency: Lowers decision-making latency down to roughly 16.5–79 milliseconds depending on the volume of choice options.
> • Benchmarks: Scores competitively on tool-calling and agent tasks (e.g., 95.2% on the Berkeley Function Calling Leaderboard) and achieves state-of-the-art results as an output verifier on coding benchmarks like DeepSWE (81.6%) and Terminal-Bench 2.1 (87.6%).
> • Licensing: Released under an open-source Apache 2.0 license for easy local self-hosting and fine-tuning.
>
> Links:
> - Huggingface: https://huggingface.co/Contrastive-LM/CLM-v0.1-8B
> ```
>
> Basically this model would allow us to make quick decisions, if we have each
> decision answers mapped to a list of possible answers, and the model will
> reply with a probability distribution for each answer given the input. So, for
> example, we can provide CLM with the last lines of dialog between a cast
> character and the listener during contact mode, and ask the model questions
> like:
>
> * "Does the character Moira answered the user question?" Options: [YES, NO].
> * "What was the character Ralph question about?" Options: ["Asking for
>   supplies", "Asking about the weather", "Asking about scientific facts"]
> * "Was the user asking for details about a Zombie outbreak?" Options: [YES,
>   NO].
> * "Was the user asking for details about the location of the lab?" Options:
>   [YES, NO].
> * "Was the user offered help with supplies, medicines or food?" Options:
>   [Supplies, Medicine, Food, Other].
>
> This model is supposedly very fast, so it would allow us to ask many questions
> (we would have to experiment with it first to evaluate if quality serve our
> purposes). The hope is that the model's answers would allow us to steer the
> narration back to a strong user interaction during the contact rounds. And
> maybe could be used outside of the contact mode to steer the narration, by
> adding more sentences to the prompt asking the model to insist on something,
> or talk/ask more about a topic, based on the discreet scores provided by CLM
> for each of our questions. We should be able to perform many requests to CLM
> for the cost of one nemotron extra request. (This of course, we would need to
> confirm with measurements).
>
> Do your own research, see what you learn about CLM, and come up with your own
> judgment if this feature I am describing is a good fit for our project.
> Push backs are welcome, and will be recorded in our document together with
> this initial and incomplete formulation of how I imagine the feature.
>
> The goal of this exercise is to discuss this as a potential feature, and
> saving all our discussion in full details for the future. We are not going to
> execute on this before the demo. I just want to save this idea well if we
> determine it is valuable.

**In short, the feature as the owner imagines it:** the director hands a fast
model the last lines of the dialogue and a set of typed questions, each with
its answers declared in advance (YES/NO, or a list of options); the model
returns a probability for each answer; code reads those numbers and steers —
in a contact, back to a strong exchange with the listener; outside one, by
adding sentences to the next instruction ("insist on…", "ask more about…").
Many such questions should cost less than one extra Nemotron request — to be
confirmed by measurement.

## §2. What the agent found about CLM (2026-10-01, from the model card and the news)

Checked against the model card and press coverage the same morning (sources at
the end). Where the pasted description and the sources differ, the sources win.

- **Who and when.** CLM ("Contrastive Language Models") v0.1 by the
  Contrastive-LM team — Stanford and NVIDIA Research — released about
  **2026-09-23** (MarkTechPost's article of that date), **Apache 2.0**. One
  week old at the time of this discussion. A multimodal **CLM-35B** is
  announced for October 2026.
- **Jev**, the model it is measured against: **the proprietary System One
  model of TypeSafe AI**, in limited early access since **2026-09-15**; it
  "returns typed values with probabilities instead of text". (A "cross-reader"
  reads the state and each candidate together; CLM embeds them apart, which is
  what lets it cache.)
- **Architecture.** A **frozen Qwen3-8B** used as an encoder (its last-token
  pooled embedding), plus **two small trained projection heads** — a state
  head and an action head, about **20M parameters each** — trained with a
  bidirectional InfoNCE (contrastive) loss. The downloadable heads weigh
  **75 MB**. Training: ~60M Nemotron question-answer pairs (pre-training),
  ~30M synthetic hard negatives made with Gemini 2.5 Flash-Lite
  (mid-training), ~1M agent trajectories (post-training).
- **How it answers.** It never generates text. It embeds the state once and
  each candidate answer once, scores each candidate by the **dot product** of
  the two embeddings, and turns the scores into probabilities with a
  **softmax**. Candidate embeddings can be cached and reused — the speed claim
  ("up to 9× faster than Jev"; "13×" with about 1,000 candidates).
- **Question types** — the owner's examples map onto them directly:
  - **`Noul`** — the probability that a statement is true (YES/NO);
  - **`Choice`** — one option from a declared set, with probabilities;
  - **`Score`** — an expected level on an ordered scale (e.g. "Calm",
    "Frustrated", "Very angry").

  The model card's example, verbatim:

  ```python
  from clm import CLMClient, Choice, Noul, Score

  client = CLMClient()
  r = client.system_one(
      state="Customer: my invoice was charged twice and nobody answers the phone!",
      questions={
          "urgency": Noul(instructions="Is this urgent?"),
          "department": Choice(instructions="Which team should handle this?",
                               criteria={"billing": "Charges, invoices, refunds",
                                         "technical": "Bugs and outages"}),
          "frustration": Score(instructions="How frustrated is the customer?",
                               criteria=["Calm", "Frustrated", "Very angry"]),
      },
  )
  print(r.answers["department"].choice)
  print(r.answers["department"].probabilities)
  ```
- **How it is served** (the model card):

  ```bash
  pip install contrastive-lm
  vllm serve Qwen/Qwen3-8B --served-model-name qwen3-8b --runner pooling --max-model-len 2048 --port 8090 &
  clm-serve
  ```

  — a **vLLM server running Qwen3-8B in "pooling" mode** (embeddings only),
  and CLM's own server (an API and a playground at port 8700). The state is at
  most **2,048 tokens** (`--max-model-len 2048`). "Runs on 1 NVIDIA GPU under
  Linux." The GPU memory it needs is **not stated**.
- **Speed** (zero-shot, against Jev): T-Rex **16.5 ms** (Jev 149.8), tool
  calling **76.8 ms** (125.5), WikiRacing **79.8 ms** (225), Super Mario
  **33.5 ms** (132.6). Cached lookups on an **RTX 4090** with 3 actions: a
  revisited state **1.7 ms → 0.6 ms**. Fine-tuned verifiers on an **H100**:
  DeepSWE **79 ms** (Jev 449), Terminal-Bench **32 ms** (131).
- **Accuracy, and its caveats** (the model card's own):
  - the base checkpoint's top-1 accuracy on **held-out questions**: **52.1 %**
    after pre-training, **69.2 %** after mid-training;
  - the headline results — **DeepSWE 81.6 %, Terminal-Bench 2.1 87.6 %** —
    come from **fine-tuned heads**, on "held-out subset results, not full
    leaderboard submissions";
  - "CLM only scores the candidates you give it, and its probabilities are
    relative to that set";
  - **encoder-locked**: "the heads require Qwen3-8B last-token-pooled
    embeddings";
  - the pasted description's **95.2 % on the Berkeley Function Calling
    Leaderboard** was not found in the sources the agent read — unverified.

## §3. The agent's judgment (2026-10-01)

**The idea is a strong fit for the project; CLM is not the first tool to try
for it.**

### §3.1 Why the idea fits

Today the director decides **what to ask** the model — who speaks, the event,
the agenda item, the mood — but it cannot check **what was actually said**:
the listener's words and the cast's replies go back into the prompt as text,
and every judgment about them is left to the model. A judge closes that loop:
code asks cheap, typed questions about the dialogue and acts on the answers.
It is the director's own philosophy — code decides, the model writes
([ADR-0003]) — reaching one step further. Concrete uses:

1. **The agenda's two branches.** Every agenda item already has two branches
   (the fork's `stories/lab-outbreak/agenda.yaml`: "Each item has two branches:
   ask for something, or, when the voice already gave it, use it."), and today
   **both reach the model in one sentence** — "Find out who the voice is. If the
   voice already said their name, greet them by it and ask how they found this
   frequency." — so **the model decides** which branch applies (checked in the
   fork's `app/show/director.py`, `_agenda_item`: code picks the item, never the
   branch). A judge could say which branch applies ("Did the caller say where
   they are?") and the instruction could carry only that branch.
2. **Holding a contact.** "Did Moira answer the caller's question?" — if not,
   the next instruction says to answer it first. The owner's first example.
3. **Steering outside a contact.** "Has the cure come up in the last ten
   rounds?" — if not, nudge the cast toward it; the owner's "insist on
   something, or talk/ask more about a topic".
4. **A bonus, for the sound effects** (the SFX idea of 2026-09-30, not yet
   recorded in a document: a library of AI-generated sounds, made offline, played
   under the events): ranking the stored sounds against an event's text is
   exactly CLM's cached-candidate case.

### §3.2 The pushbacks

1. **Memory — the biggest.** CLM brings **a second 8B model**. Qwen3-8B at
   full precision (bf16) is about **16 GB** by itself (8.2 billion parameters
   × 2 bytes — the agent's arithmetic); the stack already measured **14.0 of
   15.3 GiB** on an A4000 (the spec, §4). That breaks the owner's 16 GB wish,
   and even a 24 GB RTX 3090 at full precision. A quantized encoder (8-bit or
   4-bit) might bring it to roughly 5-9 GB — but the heads were trained on
   Qwen3-8B's exact embeddings, and what quantizing them costs in accuracy is
   unmeasured. vLLM also reserves about 90 % of the GPU for itself by default
   and would need tuning to share the card.
2. **We already have a judge on the GPU: Nemotron.** With a grammar that allows
   only `YES|NO` (or the declared options), a judgment is one prompt and **one
   generated token**, and llama.cpp can return that token's probabilities — a
   probability distribution with **no new memory and no new service**. **The
   real cost is the cache, not the speed:** the server runs **one slot**
   (`--parallel 1`, spec §4), and the slot holds the show's long script. A
   question with a different prompt would push the script out, and the next
   round would have to read it all again. The server's host-RAM prompt cache
   may make that cheap, and a second slot is an option — this was the
   measurement the agent proposed to decide between the two.
3. **We do not need its speed.** CLM's milliseconds matter to agents that make
   thousands of decisions. The show would ask perhaps 5-10 questions per round,
   and between rounds the model sits idle for seconds while the voice plays
   (the page asks for the next round only once the voice has said everything):
   a slower judge still fits.
4. **Quality on our material is unknown.** Improvised dialogue mixed with noisy
   Whisper transcripts; YES/NO probabilities that are relative to the set (so
   "NO" must cover everything else, and an option list needs an "Other");
   **69.2 %** zero-shot on held-out questions may need **fine-tuning** — on
   answers labelled by hand from our own runs.
5. **It is brand new** — v0.1, a week old. Adopting it means a new Python
   package, a vLLM container and an Ansible role for it — for a feature the demo
   does not need.
6. **Steering has limits.** An instruction can ask the cast to insist on a
   topic; the model may not comply. The judge tells us what happened; it cannot
   force what happens next. (The show has met this before: a grammar that
   contradicts its prompt changes the model's style and costs more — spec
   §6.3.)

### §3.3 What the agent proposed to record

"A judge in the loop: typed questions about the dialogue, answered fast,
steering the director", as a post-demo idea, with an experiment before any
build: (1) write the questions down and hand-label their answers on the
contacts recorded in the fork's `runs/`; (2) a baseline, Nemotron as the judge
(a one-token grammar and the token's probabilities) — accuracy, time per
question, and the cost to the show's cache; (3) a challenger, CLM with a
quantized encoder — memory, time, accuracy; (4) only then choose, and only then
build the steering. Saved as this discussion, with a line in the roadmap's
"Ideas / parking lot" — a future capability, not a small follow-up.

## §4. The owner's answer (verbatim, 2026-10-01)

> Let's open a new branch right now to increase the context size and adjust the
> settings to use close to 32k of context, and measure the memory. And first
> thing we will do in this branch is to create the documents about "A judge in
> the loop". I agree with your observations that CLM is unproven and that we
> already have a judge, however I am fully aware of the cache cost as we already
> encountered some delays after trim triggers, so I am very hesitant to add
> nemotron also as a judge, if anything I would prefer to add a smaller LLM model
> to the mix just to be a judge (maybe a 3b model can do the job).
> Please remember to record in the document all details or more that we have
> here in the transcript, I should be including my initial question and your
> research and conclusions.

The delays the owner refers to: when the trim fires, the model reads the
shortened script from the start — a pause of **about 5 s** before the round,
measured 2026-09-28 (the TODO's dead-air static item). A judge sharing
Nemotron's one slot would cause the same kind of re-read after every round
it is asked about.

## §5. Where the idea stands: three candidates for the judge

| Candidate | Memory | The show's cache | Tooling | Quality |
|---|---|---|---|---|
| **A small LLM of its own (~3B), the owner's leaning** | about 2-2.5 GB at 4-bit (the agent's estimate, unmeasured) | untouched: its own server, its own slot | the same as today: a second llama.cpp server, a GBNF grammar for the answer, the answer token's probabilities | unknown for a 3B on our dialogue — the experiment's question |
| **CLM-8B** | a second 8B encoder: ~16 GB at full precision, perhaps 5-9 GB quantized, with unmeasured accuracy loss | untouched | new: `contrastive-lm`, vLLM in pooling mode, a new container | 69.2 % zero-shot on held-out questions; better with fine-tuned heads |
| **Nemotron itself** | none | **evicted** by every question (one slot) — the owner's objection | already there | likely the best of the three (the same model that writes the show) |

**The small LLM, as the agent sees it:** it keeps the tooling the project
already masters — llama.cpp, a grammar, `n_probs` for the answer's
probabilities — and adds no new kind of service: the deployment would run a
second llama.cpp container with a small model, which the playbook's LLM role
might take as a parameter. It leaves the show's cache alone. Its memory
(~2-2.5 GB, estimate) fits a 24 GB 3090 beside the stack; against the owner's
16 GB wish it would sit just over (14.0 + ~2.5 GB) — to measure, with the 32k
context of this branch counted in. Candidates to look at when the time comes
(the agent's knowledge, to verify then — new models appear monthly): 3-4B
instruction models such as Qwen3-4B, Llama 3.2 3B or Phi-4-mini. The GPU is
still shared: a judge's question runs while the voice synthesizes the round
(the page plays each chunk while the next is made), so the two would compete
for the card — the experiment measures that too.

## §6. The experiment, when the time comes (after the demo)

1. **The questions.** Write the judge's questions down, typed: the owner's five
   examples (§1), the agenda's branch questions (§3.1, use 1 — one per agenda
   item), and a few steering questions outside contacts.
2. **The labels.** Hand-label the answers on the contacts recorded in the fork's
   `runs/` (`script.json` holds every round's lines and what Whisper heard) — a
   fixed set, the same for every candidate.
3. **The candidates** (§5): the small LLM first (the owner's leaning), CLM as
   the challenger; Nemotron only offline, as a reference for quality, never in
   the show's path (the owner's objection).
4. **What is measured:** accuracy per question against the labels; time per
   question (alone, and while the voice synthesizes); GPU memory, with the
   stack at its 32k context; and, for the winner, whether the round's latency
   changes.
5. **Then decide**, and only then build the steering: which questions, when
   they are asked (after each exchange; every N free rounds), and what each
   answer adds to the next instruction.

## §7. Sources

- [CLM-v0.1-8B — the model card on Hugging Face](https://huggingface.co/Contrastive-LM/CLM-v0.1-8B)
- [MarkTechPost, 2026-09-23 — "Contrastive-LM Releases CLM-8B: An Open System One Model That Scores Agent Actions Up to 9× Faster Than Jev"](https://www.marktechpost.com/2026/09/23/contrastive-lm-releases-clm-8b-an-open-system-one-model-that-scores-agent-actions-up-to-9x-faster-than-jev/)
- [Crypto Briefing — "Stanford and Nvidia's CLM-8B model runs up to 9x faster than Jev"](https://cryptobriefing.com/stanford-nvidia-clm-8b-faster-than-jev/)
- [AlphaSignal — "Stanford's CLM Turns Agent Decisions Into Vector Search 9x Faster"](https://alphasignal.ai/news/stanford-s-clm-turns-agent-decisions-into-vector-search-9x-faster)
- [nullbot — "CLM-8B: Open System One Model Scores Agent Actions at High Speed"](https://www.nullbot.ai/en/actu/clm-8b-contrastive-model-scores-agent-actions/)

[ADR-0003]: ../decisions/0003-adopt-shared-context-screenplay-engine-with-browser-clocked-director.md
