# TTS engine ranking for the spike slot (component 2)

**Date:** 2026-09-15 · **Part of:** the remote-split test.
**Method:** research agent read the tts-serve README + all six
`impl/server_*.md` docs (raw markdown) plus upstream engine
repos/PyPI where docs were thin; all claims cited in the agent
transcript; key receipts inline. **Ranking axes, in priority
order (agreed with owner):** (1) setup friction · (2) CUDA/torch
compatibility with our fixed driver 535 — the deciding filter ·
(3) VRAM footprint (~8 GB free beside the LLM) · (4)
latency/RTF · (5) reference-audio cloning (project-goal
relevance) · (6) doc/impl maturity.

**Shared facts from tts-serve's README:** one venv per engine
(dependency trees conflict); every engine defaults to
`0.0.0.0:7500` — **set `<ENGINE>_HOST=127.0.0.1`** per our §10
posture; `/synthesize` reports RTF. None of the six impl docs
pins torch/CUDA — every compatibility call below comes from the
upstream engine.

## Top 3 (descending favorability)

### 1. Faster Qwen3-TTS — recommended for the spike

- Friction: **lowest** — 5 steps, `pip install faster-qwen3-tts`,
  model auto-downloads.
- Driver-535: **PASSES, and is the only engine that documents an
  older-driver path explicitly**: upstream prescribes
  `torch==2.5.1 torchaudio==2.5.1 --index-url …/whl/cu124` for
  exactly our case (cu124 runs on driver 535). Skip the
  experimental GGML backend.
- VRAM: ~2 GB (0.6B checkpoint, FP16; third-party figure).
- Latency: purpose-built for real-time (CUDA-graph fast path,
  streaming); the only engine with published speed benchmarks.
- Cloning: yes, but `reference_text` is REQUIRED (no
  speaker-embedding fallback) — fine, we'd have transcripts of
  reference clips.

### 2. Chatterbox — fallback for the spike; arguably the keeper for the 4-voice goal

- Friction: moderate (8 steps, zero version fiddling — package
  carries its own pins).
- Driver-535: **PASSES** — hard pin `torch==2.6.0` (verified in
  upstream pyproject), whose default PyPI wheel is cu124. Use
  Python 3.10–3.13.
- VRAM: ~2.3–3.5 GB (NVIDIA model card, TTS-only); third-party
  claims up to 8–16 GB for the original model — unverified
  spread, budget ~3.5 GB and check.
- Cloning: **best of the six** — transcript-free, conditions
  purely on the first 10 s of reference audio; 23 languages.
  Note: output is PerTh-watermarked by the library.
- Doc: the most battle-tested-looking impl doc of the six.

### 3. Qwen3-TTS vanilla — good engine, DIY safety work

- Driver-535: **conditional pass** — nothing pins torch, so a
  naive install pulls current cu128-era wheels (risk); the
  mitigation is pre-installing `torch==2.6.0` cu124 in the venv
  BEFORE `pip install qwen-tts`. FlashAttention is optional —
  skip it. Ranked below 1–2 because the safety work is on us
  instead of documented.

## Disqualified by the driver-535 filter (3 of 6!)

- **OmniVoice** — upstream pins torch==2.8 (cu128-default
  wheels); reports of silent CPU-only downgrades.
- **dots.tts** — targets torch 2.8 + CUDA 12.8 with compiled
  kernels and Triton; worst compatibility profile here; impl doc
  offers no device override.
- **Index-TTS** — upstream demands CUDA Toolkit ≥12.8; ~8 GB
  minimum VRAM = zero headroom beside our 6.9 GB llama.cpp.

*(Nuance on the filter: CUDA 12 minor-version compatibility
means cu126/cu128 wheels sometimes run on a 535 driver for plain
kernels — but flash-attn/Triton/custom compiled kernels, exactly
what the disqualified three lean on, is where it breaks.)*

## Consequences beyond the spike

1. **The §7.2 TTS comparison experiment's roster is
   driver-dependent — and the driver is a dropdown, not a fact
   of life** (owner-verified 2026-09-15 from the Hyperstack
   deploy console). The image list encodes the driver↔CUDA
   ladder directly:

   | Hyperstack image | Driver branch | CUDA |
   |---|---|---|
   | Server 22.04 LTS **R535** CUDA 12.2 with Docker ← our box | R535 | 12.2 |
   | Server 22.04 LTS **R550** CUDA 12.4 (± Docker) | R550 | 12.4 |
   | Server 22.04 / 24.04 LTS **R570** CUDA 12.8 (± Docker) | R570 | 12.8 |

   (Matches NVIDIA's official minimums: CUDA 12.2 ≥ 535.x,
   12.4 ≥ 550.x, 12.8 ≥ 570.x. Why our cu124 containers still
   ran on R535: CUDA 12.x *minor-version compatibility* lets
   12.x-built apps run on older 12.x drivers for standard
   kernels — it's flash-attn/Triton/custom-compiled kernels
   where that breaks, i.e. exactly the disqualified engines.)

   **Ruling for §7.2 and future boxes: provision with the R570
   / CUDA 12.8 "with Docker" image** so all six engines — plus
   F5-TTS/Breeze from follow-ups — can compete fairly. For THIS
   spike box: staying on R535 is recommended (services already
   up; the plumbing test needs one engine, and rank 1 passes) —
   rebuild only if the owner prefers.
2. Chatterbox's transcript-free cloning makes it the early
   favorite for the *production* 4-voice role regardless of what
   the spike uses — noted for §7.2, not decided.
