# LLM working-default survey

**Date:** 2026-09-14 · **Arc:** Product definition (Task 2)
**Type:** survey (candidate models compared and adjudicated)
**Status:** Tracks 1–2 RUN (2026-09-14); §6 delivers a RANKED
SHORTLIST of five (owner ruling: no single-model conclusion
without an experiment — the Track 3 audition makes the pick);
Track 3 not started. The
method in §1–§3 was registered and committed before the research
ran (deliberate echo of the experiments protocol: registering
the method before the data exists keeps the data from bending
the method).

*Context for the cold reader: Zombie-Radio's dialogue is
improvised live by a small local LLM served by llama.cpp behind
an OpenAI-compatible endpoint ([spec §4], brainstorm §3). The
final model choice is deliberately deferred — swapping is a
config change — but a **working default** must be picked before
prompt-engineering starts, because prompts overfit to a model's
voice. The owner's shortlist, from hands-on experience on his own
hardware: a small **Gemma 4**, **Qwen 3.5**, **Nemotron** (if
VRAM fits), or an **LFM2-class** very small model.*

## 1. Methodological principle (learned 2026-09-14)

The agent's first proposed method was a *verification* protocol —
confirm llama.cpp support, GGUF availability, VRAM fit. The owner
rejected it: those facts are already known **by experience** for
the shortlisted models; verification axes only earn their keep
against *unknown* models. Principle adopted: **match the method
to the epistemic state** — verification axes filter unknowns;
known-and-trusted models need *differentiation* axes that speak
to this application specifically.

## 2. The comparison axes

For a 4-character improvised horror radio drama:

1. **Context length — and its real cost.** Raw maximum window;
   *effective* context (small models often degrade well before
   the advertised limit, and our story-so-far grows all
   evening); and **KV-cache VRAM cost at the target context** —
   a 32k window can quietly eat gigabytes the TTS engines need.
2. **Loop-proneness.** The owner's named disease from 2024
   ("they loop like crazy"): repetition/degeneration tendencies
   over long generation runs.
3. **Persona stability.** Can one model voice 4 distinct
   characters over a long session without them bleeding into
   each other? The roleplay community measures this (RP
   leaderboards, EQ-Bench creative writing) — the axis most
   correlated with the show being good.
4. **Steerability under a director.** Obedience to mid-stream
   system commands ("mention the generator failing", "speak as
   MARCUS only", entropy-term injection) AND structured-output
   discipline: reliably emitting parseable `CHARACTER: line`
   format without drift.
5. **Horror tolerance & positivity bias.** Safety-tuned models
   may refuse peril, soften violence, tone-police a zombie
   apocalypse — or exhibit the RP community's most-hated
   failure, relentless positivity, which kills drama. Models
   differ a lot here.
6. **Assistant-voice contamination.** Does it slip into "As an
   AI…" / bullet-list / helpful-assistant register mid-drama?
   Dialogue naturalness vs. chatbot-speak.
7. **Latency profile for our traffic shape.** Our pattern is
   long-growing-prompt → short completion: **prefill-dominated**.
   Prefill throughput at our quantization on A6000/3090-class
   hardware matters more than headline tokens/s.
8. **RP-finetune ecosystem depth.** If a base model disappoints,
   does a well-regarded community roleplay finetune of it exist?
   A deep bench is insurance.

**Epistemic caveat (drives the method):** axes 2, 3, 5, 6 are
only *weakly* researchable — community signal yields priors, not
answers. The real answers come from the audition (Track 3).

## 3. The method, in three tracks

- **Track 1 — Discovery sweep** (research). Hunt for models NOT
  on the owner's list (small-class releases through 2026 with a
  creative/multi-character lean). Unknown models first pass
  through the *verification* filters (llama.cpp/GGUF support,
  VRAM at quantization, license) — the axes that are useless for
  knowns are exactly right for disqualifying unknowns — then
  survivors get scored on §2 axes via community signal. Output:
  **1–2 newcomers** brought forward to stand next to the known
  four in a later comparison round.
- **Track 2 — Known-models table** (research-lite). For the
  owner's four: fill ONLY the researchable cells — axis 1 in
  full (context + KV cost), community priors on 2/3/5/6/8,
  published prefill numbers where they exist (7). No
  re-verification of what the owner already knows.
- **Track 3 — The audition** (candidate experiment; NOT started;
  spec'd when triggered). A prompt harness — 4 personas, N
  generated lines per candidate, identical seeds/settings — run
  on the owner's RTX 3090, counting loops, format breaks,
  refusals, and character bleed: the empirical answer to axes
  2/3/5/6. Doubly valuable: the harness is also the show's first
  prompt-engineering artifact. Feeds on the character bibles
  (owner action queue); follows the experiments protocol
  (timebox, runlog, pre-registered verdict criteria).

**Deliverable** *(reshaped 2026-09-14 by owner ruling — was
"one working default + runner-up")*: the combined table (knowns
+ newcomers) and a **ranked shortlist of ≥5 models** ordered by
preferability on the §2 axes; the Track 3 audition — not this
survey — picks the working default from that list, recorded
then in [spec §4]. No ADR: the choice is deliberately cheap to
reverse, the opposite of ADR material.

## 4. Track 1 results — Discovery sweep (run 2026-09-14)

Two newcomers survived the filters; both are Mistral-Nemo-12B
based (mature llama.cpp support, ~7.5 GB at Q4_K_M, 128k
context, cheap GQA KV cache) — and therefore drop-in
interchangeable with each other, making a later A/B nearly free.

- **[Rocinante-X-12B-v1](https://huggingface.co/TheDrummer/Rocinante-X-12B-v1)**
  (TheDrummer, Jan 2026) — *the RP specialist.* Community-adored
  character-dialogue tune ("first sub-24B creative model I
  actually enjoyed", "feels bigger than 12B", praised for
  character consistency). Supports the **Metharme** prompt
  format — literally a character-turn format, mapping naturally
  onto our `CHARACTER: line` schema. Tuned away from assistant
  register; refusals on zombie peril highly unlikely
  (TheDrummer is the de-facto uncensored-RP brand). Flags:
  license field formally **unspecified** on the repo (base is
  Apache 2.0); some community notes about recurring formatting
  patterns/GPT-isms (mitigated by rep-penalty ~1.05 + min_p).
- **[Wayfarer-2-12B](https://huggingface.co/LatitudeGames/Wayfarer-2-12B)**
  (Latitude/AI Dungeon, Aug 2025, Apache 2.0) — *the
  anti-positivity wildcard.* The only small model explicitly
  trained for "pessimism, where failure is frequent and plot
  armor does not exist for anyone… making death a distinct
  possibility for all characters" — a direct strike on axis 5,
  where assistant-tuned incumbents are weakest. Flag: trained
  almost exclusively on **second-person narrator** text ("you…")
  — it is a narrator engine, and bending it into 4-voice script
  format may fight the training.

Considered and rejected (one line each): Ministral 3 (role
overlap with incumbents + rough llama.cpp support at release);
Snowpiercer-15B (reasoning-model latency overhead, over the
band); Rocinante-XL-16B / Cydonia-24B / Orion-26B (VRAM);
Muse-12B (harder narrator lock than Wayfarer); Wayfarer v1
(superseded); Violet Lotus / RPMax 12B (no axis the shortlisted
two don't cover); Stheno/Lumimaid/MythoMax/Psyfighter (2024-era,
not newcomers).

## 5. Track 2 results — Known-models table (run 2026-09-14)

**Naming check** (owner names → actual current small variants):
"Gemma 4" ✓ (Apr 2026; relevant: **12B-it**, ~7 GB Q4);
"Qwen 3.5" ✓ small series (Mar 2026; relevant: **9B**, ~5.5 GB
Q4 — Qwen3.6/3.8 exist but have no ≤9B refresh); "Nemotron" →
**Nemotron Nano 9B v2** (Aug 2025 hybrid Mamba; the newer
Nemotron 3 Nano 30B-A3B MoE is over our slice, its dense 4B
fits as alternate); "LFM2" → superseded by **LFM2.5**, relevant
variant **2.6B** (~1.7 GB Q4; license: LFM Open v1.0, free
under $10M revenue).

| Axis | Gemma 4 12B-it | Qwen3.5-9B | Nemotron Nano 9B v2 | LFM2.5-2.6B |
|---|---|---|---|---|
| Native max context (no YaRN-style extension) | 256K advertised, via "Proportional RoPE" positional scaling — strictly-native training length **unverified** | **262K native (verified** — model card: "262,144 natively", YaRN only for extension to 1M) | 128K supported; native-vs-scaled **unstated** on card | 128K, trained via mid-training context extension (a trained capability, not inference-time scaling) |
| KV cache fp16 @16k/32k/64k/128k (calc.) | ~1.35 / 2.4 / 4.5 / 8.7 GB | ~0.5 / 1.0 / 2.1 / 4.2 GB | **~0.26 / 0.52 / 1.05 / 2.1 GB** | ~0.26 / 0.52 / 1.05 / 2.1 GB |
| KV cache Q8 @16k/32k/64k/128k (≈½ fp16) | ~0.7 / 1.2 / 2.3 / 4.4 GB | ~0.25 / 0.5 / 1.05 / 2.1 GB | ~0.13 / 0.26 / 0.52 / 1.05 GB | ~0.13 / 0.26 / 0.52 / 1.05 GB |
| KV cache Q4 @16k/32k/64k/128k (≈¼ fp16) | ~0.35 / 0.6 / 1.15 / 2.2 GB | ~0.13 / 0.26 / 0.52 / 1.05 GB | ~0.07 / 0.13 / 0.26 / 0.52 GB | ~0.07 / 0.13 / 0.26 / 0.52 GB |
| Loop-proneness | no reports; "thin templated output" when reasoning lapses | family-level long-context loop reports (27B/vLLM) *(weak)* | verbosity/drift, not loops *(weak)* | vendor ships anti-loop sampling defaults *(weak)* |
| Persona/RP quality | **best measured**: BenchLM RP 42.9, creative ≈ its 31B sibling; "insane" RP *with reasoning on* | unranked, assistant-first, thin RP sentiment *(weak)* | strong anecdotal SillyTavern praise for its size *(weak)* | weak; **vendor disclaims creative writing** |
| Horror tolerance (stock) | **worst**: heavy refusals on dark fiction; fixed by community tunes | moderate *(weak)* | **best: "no refusals" out of the box** | near-zero refusals but capability-limited |
| Assistant-voice risk | documented when reasoning disengages | think-block leak risk *(weak)* | reasoning-trace leak, not tone *(weak)* | agentic register likely *(weak)* |
| Steerability (IFEval) | **97.2** | 91.5 | 90.3 | IFStruct 85.5 (no IFEval) |
| 3090-class decode @Q4 | ~55 t/s *(est.)* | ~70–80 t/s *(scaled)*; llama.cpp is the fast engine — avoid Ollama serving (see addendum) | unpublished; only 4 quadratic layers → strong prefill scaling | fastest (est. 150–250 t/s) |
| RP-finetune bench | **rich** (Gryphe StyleTune 12B, heretic builds) | moderate, young | thin (barely needed) | ~none |

**KV-table calculation notes (all cells calculated from config
data, not measured):** growing KV per token — Gemma 64 KB (8
global layers × 8 KV heads × 256 dim; its 40 sliding-window
layers add a *fixed* ~0.33 GB, included above; caveat: the tech
report mentions "unified Keys and Values" on global layers,
which could HALVE these numbers — calc is conservative) · Qwen
32 KB (8 full-attn layers; + fixed Gated-DeltaNet state, tens
of MB, excluded) · Nemotron 16 KB (4 attn layers; + fixed Mamba
SSM state ~0.1–0.2 GB, excluded) · LFM2.5 16 KB. Quantized-KV
caveats: llama.cpp's `--cache-type-k/-v` flags cover only the
K/V tensors (SSM/GDN/conv states stay fp16); V-quantization
requires flash attention; and community practice warns **Q4 on
the K cache degrades quality noticeably** — the usual
compromise is K at Q8 + V at Q4/Q8, so treat the Q4 row as a
floor, not a plan. No "–" cells: all four support ≥128k.

Notable singles: Gemma 4 12B's hybrid attention makes its 256k
window affordable *only* with an SWA-aware cache (naive cache =
6.3 GB @16k); Qwen3.5 serving speed is **engine-dependent — and
llama.cpp is the fast path**: [ollama#14579](https://github.com/ollama/ollama/issues/14579)
measures Qwen3.5-35B-A3B at ~15–20 tok/s under Ollama vs
**~100 tok/s under llama.cpp on the same 3090 Ti** — an
Ollama-side gap, good news for our llama.cpp stack (an earlier
wording here blamed "llama.cpp/Ollama kernel maturity";
corrected 2026-09-14 after receipt verification — see addendum);
Nemotron's reasoning toggle must be off or budgeted for a live
loop. Full source list in the research transcript;
headline receipts:
[Gemma 4 card](https://ai.google.dev/gemma/docs/core/model_card_4),
[Gryphe StyleTune](https://huggingface.co/Gryphe/Gemma-4-12B-StyleTune),
[Nemotron 9B v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2-Base),
[Nemotron RP discussion](https://huggingface.co/bartowski/nvidia_NVIDIA-Nemotron-Nano-9B-v2-GGUF/discussions/2),
[Qwen3.5 long-context issue](https://github.com/QwenLM/Qwen3.5/issues/115),
[LFM2.5-2.6B card](https://huggingface.co/LiquidAI/LFM2.5-2.6B).

## 6. Recommendation: the ranked shortlist (reshaped 2026-09-14 by owner ruling)

*Owner ruling: no single-model conclusion can be made without
running an experiment. This section therefore delivers a
**ranked shortlist** — ordered by how preferable each model
looks on the §2 axes given today's evidence — and the actual
pick belongs to the Track 3 audition. Rank = presumptive order
of auditioning and nothing more; every rank below is falsifiable
by the harness.*

1. **Nemotron Nano 9B v2** — the only incumbent that is
   genre-ready *stock* (no refusals out of the box: our
   best-evidenced axis-5 result); cheapest KV cache of the
   9B-class (≈0.26 GB fp16 @16k — maximum VRAM left for TTS);
   only 4 quadratic attention layers → structurally matched to
   our prefill-dominated traffic; owner-trusted. Weaknesses:
   thin multi-character evidence; reasoning toggle must stay
   OFF for the live loop.
2. **Gemma 4 12B — as the Gryphe StyleTune or a heretic build,
   never stock.** Highest measured ceiling in the field:
   IFEval 97.2 (director obedience), best small-model RP
   scores, richest finetune ecosystem. The variant choice is
   load-bearing: stock is openly hostile to zombie horror, and
   its KV cost is the field's highest (mitigated by SWA-aware
   cache + Q8-K).
3. **Rocinante-X-12B-v1** — strongest *direct-fit* community
   evidence: character-dialogue specialist, praised
   consistency, Metharme format maps natively onto
   `CHARACTER: line`. Costs: unspecified license field (base
   Apache 2.0), newcomer status (no owner hands-on yet),
   reported GPT-ism/formatting tics.
4. **Qwen3.5-9B** — best verified context story (262k native),
   IFEval 91.5, fast under llama.cpp (~100 tok/s class on a
   3090 Ti per the corrected receipt — see addendum), Apache
   2.0. Ranked on unknowns, not known conflicts: its creative
   axes are simply unmeasured (genre-visibility bias), which is
   precisely what the audition fixes.
5. **Wayfarer-2-12B** — the axis-5 specialist: explicitly
   trained for peril, consequence, and character death; Apache
   2.0. Ranked last of the five because its second-person
   narrator training is a *known structural conflict* with our
   4-voice script format (axis 4) — high upside if prompting
   bends it, cheap to test since it shares Rocinante's Nemo
   base.

*Outside the shortlist:* **LFM2.5-2.6B** — not a lead-actor
candidate (vendor disclaims creative writing) but retained for
two named roles: the 16 GB-aspiration safety valve
([spec §4]) and utility sub-tasks (semantic endpointing,
director bookkeeping). *Alternate understudy:* **Nemotron 3
Nano 4B** (dense, 49k context) if the VRAM experiment demands a
smaller lead than 9B.

**Audition roster = the five ranked above.** The audition's
winner becomes the working default; until it runs, rank 1 is
only a presumption.

---

## Addendum 2026-09-14 — owner challenge on the Qwen treatment; a claim corrected

The owner challenged the near-absence of Qwen from the
recommendation (the local-hosting community's regard for the
Qwen family is real) and demanded receipts for the
"linear-attention kernel-maturity issues in llama.cpp/Ollama"
claim. Receipt verification found:

- [QwenLM/Qwen3.5#115](https://github.com/QwenLM/Qwen3.5/issues/115)
  is real but weak and mis-scoped: 27B on vLLM, thinking-mode
  degradation, closed-as-not-planned, no repro — correctly
  labeled weak in the table, kept.
- [ollama#14579](https://github.com/ollama/ollama/issues/14579)
  says the **opposite** of the original wording: llama.cpp is
  the FAST engine (~100 tok/s vs Ollama's ~15–20 on the same
  3090 Ti). The claim was a condensation error and is corrected
  above — on our llama.cpp stack, this receipt favors Qwen.

Two genuine method biases acknowledged: (a) **genre-visibility
bias** — the community-signal axes over-hear RP-branded models,
so a general model can score "unranked (weak signal)" while
being perfectly capable; the recommendation had quietly treated
absence of evidence as evidence of absence; (b) the agent's
training-recency handicap makes it dependent on research
condensation, where this error crept in. Remedy adopted:
**Qwen3.5-9B promoted to the full audition roster** — the
audition measures what community chatter doesn't. The
working-default recommendation (Nemotron) stands on its
*evidenced* stock horror-readiness, with the audition holding
the final word.

**Trigger to revisit:** the audition contradicting the
research-based recommendation; or a shortlist model releasing a
major new small variant before demo week.
