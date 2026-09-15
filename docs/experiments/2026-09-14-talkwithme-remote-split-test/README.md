# TalkWithMe remote-split test ("the spike") — runlog

**Created:** 2026-09-14 (skeleton) · **Run started:** 2026-09-15
(first provisioning; folder keeps its creation date — the
one-day slip is noted here rather than churning a merged path).
**Timebox:** 2 days from first provisioning command → **abort by
end of 2026-09-17** regardless of state — a partial observation
recorded honestly beats a heroic overrun.
**Provenance:** TODO Task 3a · [spec §3.3], [spec §7.1],
[spec §10.3] · [ADR-0001] (freeze gated on this spike) ·
foundation debate (brainstorm §9).

## The question

How deep do TalkWithMe's localhost assumptions go? Can the
modified-TalkWithMe app run on the demo laptop while its model
services (llama.cpp LLM, one TTS engine, whisper-fastapi) live on
a remote GPU box across the real internet — through the decided
SSH-tunnel transport — well enough to carry a 4-persona audio
session?

## Execution model

Pairing session: the owner drives every credentialed step
(provider console, SSH keys, payments); the agent navigates,
records, and keeps this runlog true. **Every command actually run
lands here, in order, with its output.** Placeholders in
copy-paste blocks must be un-pasteable or guarded — write
`<PASTE-BOX-IP-HERE>` style markers, never plausible-looking
values.

## Environment (fill at provision time)

- Provider / GPU / flavor: **Hyperstack, 1× RTX A4000 16 GB**
  (deviation from plan: A6000s persistently out of stock — the
  survey's stock-volatility warning realized; A4000 accepted,
  which incidentally tests the 16 GB aspirational tier). ECC on
  → 15352 MiB visible. Passthrough (not vGPU). Driver
  535.183.06 (CUDA 12.2-era). Full baseline:
  `scouting-hyperstack-a4000.md` in this folder.
- Box OS image: Ubuntu with Docker + nvidia-container-toolkit
  1.16.1 preinstalled (Hyperstack "with Docker" image); ~82 GB
  free on root disk; user `ubuntu` (sudo + docker group).
- Laptop: *(TBD — expected: owner's Mac)*
- TalkWithMe version: *(TBD — expected v7.0)*
- tts-serve engine chosen for the spike: *(TBD — any one engine;
  quality irrelevant here, only the plumbing)*
- LLM model file: *(TBD — any small GGUF; quality irrelevant)*
- Network path: laptop ⇄ internet ⇄ box, via `ssh -L` tunnel

## Component inventory (agreed 2026-09-15)

*The system decomposed into its top-level components before
assembly, with our assumptions stated explicitly — right or
wrong. The point of writing assumptions down is that a stated
assumption can be challenged; an implicit one can't. (Proof it
works: drafting this list surfaced and killed the owner's
assumption that tts-serve proxies requests to the engines' own
inference servers — see component 2.) Container policy is MIXED,
decided per component by whatever stands it up fastest: the
spike tests plumbing, not packaging (Docker-optional ruling,
[spec §6]). Per-component gate: (i) service answers on
127.0.0.1, (ii) service answers a real request from the laptop
through the tunnel, (iii) rough latency jotted. Deep performance
measurement belongs to step 6, not the gates.*

**(1) LLM inference server — containerized llama.cpp
(`llama-server`), official image.**

- Choice: llama.cpp directly, NOT Ollama. Receipts: the LLM
  survey addendum's verified benchmark (Qwen3.5 ~100 tok/s
  under llama.cpp vs ~15–20 under Ollama, same 3090 Ti) —
  Ollama is a convenience wrapper that costs performance and
  interposes its own model management. `llama-server` natively
  speaks the OpenAI-compatible API TalkWithMe expects.
- Container: yes — the one component where the container is the
  EASY path: `ghcr.io/ggml-org/llama.cpp:server-cuda` is
  prebuilt with CUDA, zero compilation. Run: mount `~/models`,
  `--host 127.0.0.1 --port 8080` *(revised 2026-09-15 after
  first contact: add `--parallel 1 -c 16384` — canonical command
  in the runlog)*.
- **Assumption (to verify first):** the image's newer CUDA
  runtime works on our CUDA-12.2-era driver 535 via
  minor-version compatibility (the 12.4 base image already
  worked on this box — believed transferable).
- (1.a) The tested pair: (`llama-server`,
  **Nemotron Nano 9B v2 Q4_K_M**, bartowski GGUF, ~6 GB) —
  rank 1 of the LLM shortlist; pulling it costs the same as a
  toy model on a datacenter pipe and makes latency measure (c)
  representative. **Flag:** its `nemotron_h` hybrid-Mamba
  architecture needs a recent llama.cpp build (support landed
  mid-2025; official image is fresh — believed sufficient).
  Fallback pair if the arch fights: any small Qwen GGUF —
  plumbing test proceeds unharmed.

**(2) TTS — ONE tts-serve-wrapped engine, bare on the VM.**

- **Corrected understanding (owner's prior assumption killed
  here):** tts-serve is NOT a proxy standing in front of each
  engine's own inference server. The tts-serve *implementation
  for an engine IS the server*: each `impl/server_<engine>.md`
  stands up a venv + the engine + the standardized
  `/synthesize` + `/capabilities` REST API on its own port.
  Testing one wrapped engine therefore IS testing tts-serve.
- Container: NO for the spike — deliberately bare
  (venv + tmux, bound to 127.0.0.1), following the engine's
  tts-serve instructions verbatim. Dockerizing a quirky TTS
  engine is exactly the packaging work the Docker-optional
  ruling deferred; friction encountered here feeds measure (d)
  directly.
- Engine choice: the one whose `impl/` doc looks cleanest
  against driver 535 (CUDA 12.2 era) — owner's hunch outranks
  the agent's doc-reading; TBD at execution.
- Voice quality: explicitly irrelevant to this experiment.

**(3) STT — Whisper as a persistent inference server.**

- Shape: a resident server (model loaded once into VRAM,
  requests hit an endpoint) — never load-per-call, which would
  add tens of seconds per utterance.
- Choice: **whisper-fastapi**, because it is TalkWithMe's
  documented STT integration — minimizing adapter friction
  outranks any other merit. Small Whisper checkpoint; bare venv
  expected.
- Fallback if whisper-fastapi fights: **Speaches** (ex
  faster-whisper-server; OpenAI-API-compatible; the container
  Dograh uses per our survey) in Docker.
- Noted for post-MVP, not this experiment: Whisper can run
  in-browser (whisper.cpp→WASM, transformers.js on WebGPU;
  tiny/base checkpoints only) — would free server VRAM and
  shrink uploads to text.

**(4) The SSH tunnel — transport as a first-class component.**

- One `ssh -L` invocation forwarding all three service ports
  (e.g. 8080 llama / 8001 tts / 8002 whisper) from
  `localhost:<port>` on the laptop to `127.0.0.1:<port>` on the
  box. The decided §10.3 transport: box exposes :22 only
  (externally verified during scouting).
- Gate: each service curl-able from the laptop through it.

**(5) TalkWithMe — the client+director, on the Mac laptop,
enters LAST.**

- Cloned v7.0; its LLM/TTS/STT endpoint URLs configured to the
  laptop-side tunnel ports. Serves its web UI at
  `http://localhost` (secure context → PTT mic works, no TLS).
- **Assumption under test (the experiment's core question):**
  TalkWithMe reaches all model services by URL, so the split is
  configuration, not surgery.
- Dependency: entering this step makes the **fork-strategy
  decision** (Owner action queue) due.

**Assembly line, every arrow a gate:**
(1) up → curl on box → (4) tunnel → curl from laptop → (2) up →
both curls → (3) up → both curls → (5) TalkWithMe wired →
4-persona session → measures (a)–(f). Any failure has an
unambiguous owner.

## Step checklist

- [x] 1. Provision the box (on-demand, never spot) via console;
      record flavor, price, region. DONE 2026-09-15 (A4000,
      $0.15/hr — region/flavor name to record).
- [x] 2. SSH in; baseline the box. DONE 2026-09-15 →
      `scouting-hyperstack-a4000.md`. Compute anomaly resolved
      (card genuine: fp16 60.5 TFLOPS; gpu-burn image was
      JIT-degraded). Residual: external :22-only port scan +
      network throughput, folded into steps 4/6 measures.
- [~] 3. Stand up model services on the box, loopback-bound:
      **llama.cpp UP** (Nemotron 9B v2 Q4, 6.9 GB VRAM, decode
      47.6 tok/s, reasoning-off confirmed; revised command
      adopted — see runlog); tts-serve engine PENDING (ranking
      in progress); whisper-fastapi PENDING.
- [~] 4. Tunnel OPEN (3 ports forwarded); **llama verified
      through it** (Gate B PASS, ~0.6–0.7 s cold-connection
      overhead); tts/whisper gates pending their services.
- [ ] 5. Run TalkWithMe on the laptop, configured to reach its
      LLM/TTS/STT through the tunnel endpoints.
- [ ] 6. Drive a 4-persona group session with distinct voices;
      record measures (a)–(f) below in the log.
- [ ] 7. (If time) Also test the plain `ws://`+token path for
      comparison, per TODO Task 3a setup note.
- [ ] 8. Tear down the box; record final cost.

## Measures to record

(a) audio delivery over WAN: buffering behavior, drops, stalls ·
(b) 4-persona session drivable end-to-end? · (c)
time-to-first-audio per dialog line, ≥10 consecutive lines,
rough numbers in a table · (d) effort estimate for a proper
tts-serve adapter · (e) architectural red flags (blocking calls,
hardcoded localhost, tight coupling) · (f) security observations
for [spec §10.1]: does anything in the stack provide auth? which
ports would need exposure without the tunnel?

---

## Runlog

*(Box provisioning + baseline: see `scouting-hyperstack-a4000.md`.)*

### 2026-09-15 — Component 1 (LLM server) up; Gates A and B PASS

**Start llama.cpp container (tmux window `llama`):**

```
$ docker run --name llama --rm --gpus all --network host \
    -v "$HOME/models:/root/.cache/llama.cpp" \
    ghcr.io/ggml-org/llama.cpp:server-cuda \
    -hf bartowski/nvidia_NVIDIA-Nemotron-Nano-9B-v2-GGUF:Q4_K_M \
    --host 127.0.0.1 --port 8080 -ngl 99 -c 8192
...
W srv  llama_server: CORS is set to allow all origins ('*') and no API key is set
W load: special_eos_id is not in special_eog_ids - the tokenizer config may be incorrect
I srv    load_model: initializing, n_slots = 4, n_ctx_slot = 8192, kv_unified = 'true'
I srv  llama_server: model loaded
I srv  llama_server: listening on http://127.0.0.1:8080
```

Build fingerprint: `b10975-4c9233c03`. **CUDA
minor-version-compatibility assumption from the component
inventory: VERIFIED** — the server-cuda image runs on driver
535. Two warnings noted: (a) no API key + open CORS — acceptable
on loopback-behind-tunnel for the spike; llama-server has
`--api-key` when §10.1 belt-and-suspenders is wanted; (b) the
`special_eos_id` tokenizer warning — believed benign metadata
noise on this quant; watch item: runaway generations that ignore
end-of-turn.

**Gate A (on box):** `/health` → `{"status":"ok"}`. Chat
completion round trip `real 1.309s`; server timings: prefill
130.6 tok/s, decode **47.6 tok/s**, VRAM **6888 MiB** used /
8202 MiB free (weights ~5.9 GB + KV@8k + buffers — matches the
survey's KV table; ~8 GB left for TTS + Whisper on this 16 GB
card).

**FINDING — reasoning mode is ON by default**, exactly as
flagged in the LLM survey: all 50 completion tokens landed in
`reasoning_content`, `content` came back EMPTY. Fix to apply
(next entry): Nemotron's reasoning toggle via system prompt
(`/no_think`). TalkWithMe must never see empty content.

**Gate B (from laptop through `ssh -L` tunnel):** same endpoint
via `localhost:8080` → identical server-side timings (decode
47.6 tok/s), wall time 1.919 s (zsh `time`: `1.919 total`).
**Tunnel overhead ≈ 0.63 s on a cold connection** (1.919 −
~1.29 s server work), which includes TCP setup through the
tunnel; persistent HTTP connections (what TalkWithMe will hold)
amortize most of it. First remote-split datum for measure (c).

**Clarification recorded (owner asked "only 4k context?"):** no
— `n_slots = 4` is the server's *parallel request slots*
(default), not context; context is the 8192 we requested
(`-c 8192`), shared across slots under `kv_unified`. The model
itself supports 128k, and Nemotron's KV is so cheap (~0.26 GB
@16k fp16) that raising `-c` is nearly free.

**The tunnel command as actually run (laptop side, backfilled —
audit found it missing from the log):**

```
% ssh -N -L 8080:127.0.0.1:8080 -L 8001:127.0.0.1:8001 -L 8002:127.0.0.1:8002 ubuntu@<BOX-IP>
```

### 2026-09-15 — Reasoning toggle fixed (`/no_think`); revised canonical llama command

**Test through the tunnel** (Mac; zsh `time` — its `N total`
field is the wall-clock equivalent of Linux `real`):

```
% time curl -s http://127.0.0.1:8080/v1/chat/completions -H 'Content-Type: application/json' \
    -d '{"messages":[{"role":"system","content":"/no_think"},{"role":"user","content":"You are a radio operator in a besieged lab. One short line confirming the channel is open. Over."}],"max_tokens":50}'
{"choices":[{"finish_reason":"stop","index":0,"message":{"role":"assistant",
  "content":"**Response:**  \n\"Channel open. Proceed.\"\n"}}], ...
 "usage":{"completion_tokens":13, ...},
 "timings":{"prompt_ms":256.99,"prompt_per_second":128.4,
            "predicted_n":13,"predicted_per_second":46.8}}
... 1.254 total
```

**PASS**: with the `/no_think` system message, `content` carries
real speech, `reasoning_content` is empty, `finish_reason` is
`stop` — the survey's "reasoning OFF for the live loop" config
note is confirmed as both necessary and sufficient. Two
observations: (a) formatting fluff (`**Response:**` markdown
wrapper) around the line — filed as an axis-4
formatting-discipline datum for the LLM audition; (b) cold-curl
tunnel overhead again ~0.7 s (server work ~0.51 s vs 1.254 s
wall) — consistent with Gate B; persistent connections should
amortize it.

**Revised canonical llama-server command (adopted 2026-09-15;
supersedes the step-3.1 invocation for the rest of the
experiment):** single-stream slot + doubled context, both free
on Nemotron's cheap KV:

```
docker run --name llama --rm --gpus all --network host \
    -v "$HOME/models:/root/.cache/llama.cpp" \
    ghcr.io/ggml-org/llama.cpp:server-cuda \
    -hf bartowski/nvidia_NVIDIA-Nemotron-Nano-9B-v2-GGUF:Q4_K_M \
    --host 127.0.0.1 --port 8080 -ngl 99 -c 16384 --parallel 1
```

Rationale: `--parallel 1` — TalkWithMe is a single-stream
client, and one slot stops the 4-way sharing of context;
`-c 16384` — headroom for the growing story-so-far at ~0.26 GB
KV cost. Apply at the next natural container restart (no need
to interrupt a running session for it).
