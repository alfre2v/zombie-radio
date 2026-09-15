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
  `--host 127.0.0.1 --port 8080`.
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
- [ ] 3. Stand up model services on the box, loopback-bound:
      llama.cpp server (small model), one tts-serve engine,
      whisper-fastapi.
- [ ] 4. Open the `ssh -L` tunnel from the laptop; verify each
      service answers through it (`curl` through the tunnel).
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

*(empty — begins with the first provisioning command)*
