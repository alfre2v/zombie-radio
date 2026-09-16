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
- Laptop: owner's Mac (zsh; `say`/`afconvert`/`afplay` used from
  the stock toolset)
- TalkWithMe version: **tag 7.1**, commit
  `93df6ca522f2183a04d87065bfd05345ff4a9101`; client venv:
  Python 3.12 via pyenv (exact patch version not captured —
  minor gap, `python --version` output wasn't logged)
- tts-serve engine: **Faster Qwen3-TTS** (chosen via
  `tts-engine-ranking.md`; default checkpoint
  Qwen3-TTS-12Hz-1.7B-Base)
- LLM model: **Nemotron Nano 9B v2 Q4_K_M** (bartowski GGUF)
- STT: **whisper-fastapi** (heimoshuiyu image), model `small`
- Network path: laptop ⇄ internet ⇄ box, via `ssh -L` tunnel
- **Region: NORWAY-1** (resolved 2026-09-15 via Hyperstack's
  [flavors/regions doc](https://docs.hyperstack.cloud/docs/hardware/flavors/#family-rtx-a6000)
  — A4000s live in Norway-1; **the good GPUs, A6000 and up, live
  in CANADA-1**). ⚠ **Latency context for ALL measurements in
  this runlog:** every tunnel number includes a laptop↔Norway
  round trip; a demo-day A6000 box would sit in Canada-1 with
  different (likely better, for a North-America-side operator)
  network geometry. Measures (a)/(c) must be read with this in
  mind — our numbers are a conservative bound if the demo box is
  closer.

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
  decision** (Owner action queue) due. **RULED 2026-09-15:
  defer until the first patch** — the spike clones upstream
  read-only at a pinned SHA; if configuration alone suffices,
  the fork question waits for the adaptation arc; if the spike
  forces a patch, that moment decides fork-vs-vendor with data.
  Clone location: `~/workspace/hackTNT_2026/TalkWithMe`
  (outside this repo — upstream code, not ours). Interim
  4-scientist cast: macOS `say` voices doubling as character
  names (Daniel, Moira, Samantha, Ralph), agent-drafted
  placeholder personas, owner has veto.

**Assembly line, every arrow a gate:**
(1) up → curl on box → (4) tunnel → curl from laptop → (2) up →
both curls → (3) up → both curls → (5) TalkWithMe wired →
4-persona session → measures (a)–(f). Any failure has an
unambiguous owner.

## Step checklist

- [x] 1. Provision the box (on-demand, never spot) via console;
      record flavor, price, region. DONE 2026-09-15 (A4000,
      $0.15/hr; region resolved 2026-09-15: NORWAY-1).
- [x] 2. SSH in; baseline the box. DONE 2026-09-15 →
      `scouting-hyperstack-a4000.md`. Compute anomaly resolved
      (card genuine: fp16 60.5 TFLOPS; gpu-burn image was
      JIT-degraded). Residual: external :22-only port scan +
      network throughput, folded into steps 4/6 measures.
- [x] 3. All three model services UP, loopback-bound (DONE
      2026-09-15): llama.cpp/Nemotron (6.9 GB, 47.6 tok/s) ·
      Faster Qwen3-TTS (5.0 GB, rtf 0.455) · whisper-fastapi
      small (1.5 GB, 7.3 s audio in 1.85 s). Trio: 13.5/15.3 GiB.
- [x] 4. Tunnel verified for ALL services (DONE 2026-09-15):
      LLM chat, TTS synthesis (cloned voice audible on laptop),
      STT full-circle transcription of our own TTS output.
      Cold-connection overhead ~0.6–0.7 s, amortizable.
- [x] 5. Run TalkWithMe on the laptop against tunnel endpoints.
      DONE 2026-09-16 — Gates 5.1–5.4 all PASS (UI, text chat,
      cloned voices w/ streaming pipeline, mic round trip);
      zero upstream modifications needed: configuration only.
- [x] 6. Drive a 4-persona group session with distinct voices;
      record measures (a)–(f) below in the log. DONE 2026-09-16
      (group sessions in `Lab`/`lab2`/`lab3`; TTFA table
      harvested; all measures resolved — findings.md).
- [x] 7. (If time) Also test the plain `ws://`+token path for
      comparison, per TODO Task 3a setup note. SKIPPED 2026-09-16
      with recorded rationale (see runlog entry).
- [x] 8. Tear down the box; record final cost. DONE 2026-09-16
      (owner-executed; **total experiment cost: $2.97**).

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

## Reproduction recipe — THE section to follow

*Living section (amended whenever a command is corrected): the
CURRENT, working commands in execution order, from nothing to a
talking lab. The Runlog below is evidence and history — what
actually happened, warts included — and is NOT the thing to
follow. (Convention amended 2026-09-16 at the owner's request;
recorded in `experiments/README.md`.)*

### On the box (Hyperstack VM, SSH as `ubuntu`)

**R0 — provision:** Hyperstack console → VM with the standard
image (posture: `R570 CUDA 12.8 with Docker`, Ubuntu 24.04 —
[spec §6]; THIS run used the R535/22.04 image, an accepted
grandfathered exception). This experiment's box: 1× RTX A4000,
region NORWAY-1, $0.15/hr, on-demand.

**R1 — base packages:**

```
sudo apt-get update && sudo apt-get install -y python3.10-venv sox tmux
```

**R2 — tmux layout:** `tmux new -s radio`; create + rename
windows `llama`, `tts`, `whisper`, `ops` (see
`tmux-refresher.md`).

**R3 — LLM server (window `llama`)** — canonical v3; first run
downloads ~6 GB into the mounted `~/models`, later runs load
from disk (~90 s):

```
docker run --name llama --rm --gpus all --network host \
    -v "$HOME/models:/models" -e LLAMA_CACHE=/models \
    ghcr.io/ggml-org/llama.cpp:server-cuda \
    -hf bartowski/nvidia_NVIDIA-Nemotron-Nano-9B-v2-GGUF:Q4_K_M \
    --host 127.0.0.1 --port 8080 -ngl 99 -c 16384 --parallel 1
```

Verify the cache landed: `ls -lh ~/models/` shows the `.gguf`.

**R4 — TTS engine (window `tts`)** — fresh-box install, all
potholes pre-fixed (numpy before engine; transformers pinned):

```
mkdir -p ~/faster-Qwen3TTS && cd ~/faster-Qwen3TTS
python3 -m venv .venv && source .venv/bin/activate
pip install numpy
pip install faster-qwen3-tts
git clone https://github.com/scorbo2/tts-serve && cd tts-serve
pip install ./tts-engine-common fastapi uvicorn loguru soundfile
pip install "transformers==5.15.1" "huggingface-hub>=1.16,<2"
FASTER_QWEN3TTS_HOST=127.0.0.1 FASTER_QWEN3TTS_PORT=8001 python impl/server_fasterQwen3TTS.py
```

(Already installed? Just:
`cd ~/faster-Qwen3TTS/tts-serve && source ../.venv/bin/activate`
+ the launch line.)

**R5 — STT server (window `whisper`):**

```
docker run --rm --network host --gpus all \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  docker.io/heimoshuiyu/whisper-fastapi:latest \
  --model small --device cuda --host 127.0.0.1 --port 8002
```

**R6 — on-box gates (window `ops`):**

```
curl -s http://127.0.0.1:8080/health
curl -s http://127.0.0.1:8001/capabilities | head -c 200; echo
curl -s -o /dev/null -w "stt: %{http_code}\n" http://127.0.0.1:8002/docs
nvidia-smi --query-gpu=memory.used,memory.free --format=csv
```

Expect: ok / schema JSON / stt: 200 / ~13.5 GiB used with all
three loaded (whisper lazy-loads its model: ~12.3 GiB until the
first STT request, ~14.0 GiB once everything is warm and in use).

### On the laptop (Mac)

**R7 — tunnel (own terminal tab, stays open):**

```
ssh -N -L 8080:127.0.0.1:8080 -L 8001:127.0.0.1:8001 -L 8002:127.0.0.1:8002 ubuntu@<PASTE-BOX-IP-HERE>
```

**R8 — pulse check through the tunnel:**

```
curl -s http://localhost:8080/health && curl -s -o /dev/null -w "tts: %{http_code}\n" http://localhost:8001/capabilities && curl -s -o /dev/null -w "stt: %{http_code}\n" http://localhost:8002/docs
```

**R9 — TalkWithMe (first time only):**

```
cd ~/workspace/hackTNT_2026 && git clone https://github.com/scorbo2/TalkWithMe
cd TalkWithMe && pyenv local 3.12.<CHOSEN-PATCH>
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

**R10 — personas (first time only):** run the two factory blocks
in `placeholder-personas.md` (this folder).

**R11 — launch the app:**

```
cd ~/workspace/hackTNT_2026/TalkWithMe && source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**R12 — UI configuration** at `http://localhost:8000`: *Servers*
dialog → LLM `http://localhost:8080` · TTS enabled,
`http://localhost:8001` (engine auto-detects on URL entry;
streaming per taste) · STT enabled, `http://localhost:8002`.
Save.

**R13 — smoke gates:** pick a scientist → text chat answers in
character → voice plays → mic round-trips. You have a talking
lab.

---

## Runlog

*(Box provisioning + baseline: see `scouting-hyperstack-a4000.md`.)*

### 2026-09-15 — Component 1 (LLM server) up; Gates A and B PASS

**Start llama.cpp container (tmux window `llama`):**
*(⚠ SUPERSEDED — the `-v …/root/.cache/llama.cpp` mount is
misrouted and silently re-downloads the model every start; use
**canonical v3** in the 2026-09-16 pothole entry below. Kept
as-run for the historical record.)*

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
v2 — ⚠ ITSELF SUPERSEDED by v3 in the 2026-09-16 pothole entry
below: same flags, but the model-cache mount here is misrouted):**
single-stream slot + doubled context, both free
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

### 2026-09-15 — Component 2 (Faster Qwen3-TTS): two setup potholes on the documented path

Following `impl/server_fasterQwen3TTS.md` verbatim on the fresh
image hit two failures (both fixed; both feed measure (d) and
the future Ansible playbook):

1. **`python3 -m venv` failed** — `python3.10-venv` is not
   preinstalled on the Hyperstack "with Docker" image, and the
   apt cache starts empty (`apt-get update` required before any
   install).
2. **`pip install faster-qwen3-tts` failed at
   metadata-generation** — its dependency `sox` (Python wrapper)
   uses a legacy `setup.py` that imports numpy at build time
   without declaring it (pre-PEP-518); a pristine venv therefore
   explodes with `ModuleNotFoundError: numpy`. Additionally the
   `sox` pip package wraps the sox CLI, so the `sox` apt package
   is needed at runtime regardless.

**Recovery as actually executed (owner; leaner than the agent's
proposed venv-recreation — recreation proved unnecessary):**
`apt-get update` + install `python3.10-venv` and `sox` → create
venv (now succeeds) → `pip install numpy` → retry
`pip install faster-qwen3-tts` → SUCCESS. Clarified in review:
the sox *binary* is a runtime dependency of the pip `sox`
wrapper — install order relative to pip is irrelevant; only the
numpy-at-metadata-time failure was order-sensitive.
**Torch check (owner): `2.5.1+cu124 | CUDA 12.4 | available:
True`** — the engine's own dependency resolution landed exactly
the driver-safe pair without the manual pre-pin; question
CLOSED, launch cleared.

### 2026-09-15 — Component 2 launch: transformers version skew, resolved at 5.15.1; server UP

First launch crashed at model load:
`AttributeError: 'MimiConfig' object has no attribute
'rope_theta'` (inside `qwen_tts/_transformers_compat.py` under
transformers **5.17.0**). Diagnosis journey, errors included per
protocol: the agent's first fix (downgrade to transformers
4.57.3, based on QwenLM/Qwen3-TTS#237) was **mis-scoped** — that
issue concerns the old `qwen-tts` package; this stack uses
**`qwen-tts-hf` 0.1.1.post1** (the transformers-5 rewrite,
declared range `>=5.15.1,<6`), so 4.57.3 only produced resolver
conflicts and dragged huggingface-hub down. Correct read: API
drift WITHIN the 5.x series — the compat shim works at the
declared floor but not at 5.17.0's changed model-init path. Fix
that worked (fix #2 of the declared 2-fix limit):

```
pip install "transformers==5.15.1" "huggingface-hub>=1.16,<2"
```

**WORKING VERSION SET (reproduction record):** Ubuntu 22.04 /
Python 3.10 venv · apt: `python3.10-venv`, `sox` · pip seeded
with `numpy` before engine install · `faster-qwen3-tts==0.4.0` ·
`qwen-tts-hf==0.1.1.post1` · **`transformers==5.15.1`** (NOT
newer — 5.17.0 crashes) · `torch==2.5.1+cu124` /
`torchaudio==2.5.1` · `huggingface-hub` in `>=1.16,<2`. **Full lock committed:
`tts-freeze.md` in this folder** (owner-captured `pip freeze`;
boring by design — the pins above are the load-bearing subset).
Ansible note: PIN transformers for this engine; its own
constraint range (`<6`) is too loose to be safe.

**Box-side commands, verbatim (consolidated reproduction record
for component 2 — added by the pre-commit replication audit,
which found this sequence existed only in prose):**

```
sudo apt-get update && sudo apt-get install -y python3.10-venv sox
mkdir -p ~/faster-Qwen3TTS && cd ~/faster-Qwen3TTS
python3 -m venv .venv && source .venv/bin/activate
pip install numpy
pip install faster-qwen3-tts     # resolves torch==2.5.1+cu124 itself
git clone https://github.com/scorbo2/tts-serve && cd tts-serve
pip install ./tts-engine-common fastapi uvicorn loguru soundfile
pip install "transformers==5.15.1" "huggingface-hub>=1.16,<2"   # the 5.17-crash fix
FASTER_QWEN3TTS_HOST=127.0.0.1 FASTER_QWEN3TTS_PORT=8001 python impl/server_fasterQwen3TTS.py
```

(Run the server line inside tmux window `tts`. First start
downloads the checkpoint to `~/.cache/huggingface/hub/`. To
relaunch after a reconnect:
`cd ~/faster-Qwen3TTS/tts-serve && source ../.venv/bin/activate`
then the same server line. Gate probe:
`curl -s http://127.0.0.1:8001/capabilities`.)

**Gate A (capabilities) PASS.** Highlights of the schema:
engine `faster-qwen3-tts`, **model
`Qwen/Qwen3-TTS-12Hz-1.7B-Base`** (the default is the 1.7B, not
the 0.6B the ranking assumed), cuda, 24 kHz, NOT watermarked;
**reference audio required** (≥2 s, wav/mp3/ogg/flac, ~3 s
"enough for high-quality cloning") **plus exact
`reference_text`** — ICL mode, no speaker-embedding fallback,
0.5 s silence auto-appended to the reference; languages include
en + es; `seed` echoed in the response (nice for
reproducibility); sampler knobs exposed (temperature, top_p,
repetition_penalty).

**VRAM after load: 11 936 MiB used / 3 154 MiB free** → the TTS
stack took ~5.0 GB (11 936 − 6 888). **Prediction death, in
public:** the ranking doc estimated "~2 GB" based on the 0.6B
checkpoint; the engine's default is the 1.7B (~3.4 GB weights
fp16/bf16 + Mimi codec + CUDA-graph buffers ≈ 5 GB). Both models
DO currently coexist (LLM 6.9 + TTS 5.0 = 11.9 of 15.3 GiB);
what's tight is the remaining ~3.1 GiB for Whisper + headroom.
### 2026-09-15 — Component 2 Gate B PASS: cloned speech through the tunnel

Reference voice: synthesized on the Mac with `say -v Daniel`
(cloning a synth is valid plumbing; transcript exact by
construction), converted via `afconvert` to 24 kHz WAV.
Payload: 386 KB JSON (base64 reference inside). One operator
stumble first: the synthesize curl hit `channel 6: open failed:
connect failed: Connection refused` from the tunnel — the TTS
server simply wasn't running (operator forgot to start it;
relaunched inside tmux window `tts`; not a crash). Then:

```
% time curl -s http://localhost:8001/synthesize ... -d @payload.json > resp.json
... 0% cpu 5.771 total
```

resp.json 455 KB → decoded WAV ≈ 340 KB ≈ **~7 s of audio at
24 kHz**. **Owner's ear verdict: "surprisingly less robotic
than I feared."**

**Warm-timing series (same payload, repeated):** 5.771 → 8.531
(outlier) → 5.612 → 4.582 → 4.628 s — steady state **~4.6 s
wall**. Server metadata: `time_used 3.13 s`, **`rtf 0.455`**,
seed 768 echoed, plus a `fid` field (possible server-side
reference handle — unverified). So: ~3.1 s compute for ~6.9 s
of audio; the ~1.5 s wall–compute gap is OUR overhead (386 KB
reference upload through the tunnel + connection setup + 455 KB
response download).

**Interpretation (measure (c)):** RTF 0.455 clears the gapless-
broadcast threshold (RTF < 1) with 2.2× headroom — while line N
plays, line N+1 synthesizes faster than playback, so a
pipelined radio never runs dry after its first line; TalkWithMe's
sentence-chunked streaming is exactly that pipeline, making
first-audio ≈ first-sentence synth (~1 s) + overhead. The flat
"5 s per line" reading was an artifact of a long test line +
whole-utterance API + WAN payload. **Architectural finding: the
stateless API re-uploads the reference voice (386 KB) from the
laptop every call** — a per-line WAN tax in our topology;
mitigations: ~3 s reference (~120 KB, capabilities says
sufficient), or server-side reference caching (investigate
`fid`). Hardware note (estimate): the home RTX 3090's ~2.1×
memory bandwidth should run this engine ~1.5–2× faster (rtf
~0.25–0.3) — the A4000 is sufficient, not generous.

**Mac-side commands, verbatim (reproduction record for the
synthesis test):**

```
say -v Daniel -o ref.aiff "The laboratory maintains constant temperature, and the radio equipment remains fully operational at this hour."
afconvert -f WAVE -d LEI16@24000 ref.aiff ref.wav
python3 -c "
import base64, json
audio = base64.b64encode(open('ref.wav','rb').read()).decode()
payload = {'text': 'This is Lab Station Seven. If anyone can hear this, the generators are failing and the dead are at the east door. Over.', 'audio_base64': audio, 'reference_text': 'The laboratory maintains constant temperature, and the radio equipment remains fully operational at this hour.', 'language': 'en'}
json.dump(payload, open('payload.json','w'))"
time curl -s http://localhost:8001/synthesize -H 'Content-Type: application/json' -d @payload.json > resp.json
python3 -c "
import json, base64
d = json.load(open('resp.json'))
k = [x for x in d if 'audio' in x.lower()][0]
open('out.wav','wb').write(base64.b64decode(d[k]))
print({x: d[x] for x in d if x != k})" && afplay out.wav
```

(For a real human reference instead of `say`: record a Voice
Memo, then `afconvert -f WAVE -d LEI16@24000 memo.m4a ref.wav`
— the `reference_text` must be the exact spoken sentence.
Diagnostic used when the tunnel refused: `ss -tlnp | grep -E
':(8080|8001|8002)'` on the box lists which services listen.)

### 2026-09-15 — Component 3 (whisper-fastapi): Gates PASS; full TTS→STT round trip

Server: `heimoshuiyu/whisper-fastapi` Docker image (name-matched
to TalkWithMe's recommended "whisper-fastapi"; the binding
contract is the OpenAI-compatible `/v1/audio/transcriptions`
endpoint either way), faster-whisper backend, model `small`:

```
docker run --rm --network host --gpus all \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  docker.io/heimoshuiyu/whisper-fastapi:latest \
  --model small --device cuda --host 127.0.0.1 --port 8002
```

(Adaptations from upstream's example: host-network + loopback
bind instead of `-p`; dropped optional OPENAI_* gpt-refine env
vars; dropped podman-syntax device flag.)

**Gate A postmortem:** the agent's `/dev/null` probe returned
`Internal Server Error` — a bad gate design (the agent's),
not a sick server: zero-byte input hit an unhandled decode
exception (confirmed in the server log). Lesson: probe with
real minimal input, not degenerate input.

**Gate B — the full-circle test — PASS:** transcribing OUR OWN
TTS output (out.wav) from the Mac through the tunnel:

```
% time curl -s http://localhost:8002/v1/audio/transcriptions -F file=@out.wav
... "text":" This is Lab Station 7. If anyone can hear this, the
generators are failing, and the dead are at the east door. Over."
... 1.845 total
```

**1.85 s wall** to upload ~340 KB and transcribe **7.28 s of
audio** — STT is emphatically not the latency bottleneck; the
PTT flow (record-then-upload) costs ~2 s end-to-end. Quality:
language en at 99.5 %, near-perfect text (only "Seven"→"7"
normalization; lowest word confidence "Lab" 0.49 — a whisper of
challenge C6's proper-noun weakness). Response includes word
timestamps and full language-probability table (elided here).

**VRAM, full trio resident: 13 485 MiB used / 1 605 free** —
LLM 6.9 + TTS 5.0 + Whisper-small ~1.5 on a 16 GB card, in
budget. Headline datum for the 16 GB aspiration ([spec §4]),
with the desktop-tax caveat noted earlier.

**Not quantized — full precision**: this engine offers no
quantized checkpoints; the size lever is the smaller model
(`FASTER_QWEN3TTS_MODEL` → the 0.6B checkpoint) if squeeze is
needed. Valuable datum for the 16 GB-aspiration ledger
([spec §4]). Owner context echoing 2024: this same
LLM+TTS-exhaust-the-card squeeze is why the 2024 build ran
whisper *tiny*. Fleet note for VRAM budgeting: the home RTX
3090 runs a desktop, and Chrome/terminal/GNOME permanently tax
~1 GB of its 24 GB — a headless cloud VM pays no such tax.

### 2026-09-16 — Step 5 phases 1–3: TalkWithMe up, Gate 5.1 + 5.2 PASS

**Phase 1 (box):** llama container restarted with the canonical
command (`--parallel 1 -c 16384`). Operational note: the model
reload takes ~90 s, during which the tunnel reports
`channel N: open failed: connect failed: Connection refused` —
expected, not a fault; wait and retry. Trio pulse-check through
the tunnel: `{"status":"ok"} / tts: 200 / stt: 200`.

**Phase 2 (Mac):** upstream pinned —
`93df6ca522f2183a04d87065bfd05345ff4a9101, tag 7.1` (upstream
moved past the expected 7.0; release notes not reviewed —
accepted as-is). Python: **3.12 via pyenv** (`pyenv local`
writes `.python-version`); rationale: the client venv is a pure
web stack (no torch), so the owner's 2024 lesson — TTS/torch
stacks prefer 3.10/3.11 — applies to the BOX, not here.
Mac-side commands, verbatim:

```
cd ~/workspace/hackTNT_2026 && git clone https://github.com/scorbo2/TalkWithMe
cd TalkWithMe && git log -1 --format="PINNED: %H %d %s"
pyenv install -l | grep -E '^\s+3\.12' | tail -3   # pick newest 3.12.x
pyenv local 3.12.<CHOSEN-PATCH>                    # writes .python-version
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

(loopback deviation from README's 0.0.0.0, deliberate).
**Gate 5.1 PASS** — UI loads.

**Phase 3 (config) — correction + UI intel:** `settings.yaml`
does NOT ship in the repo (the agent's briefing over-read the
README): it is **auto-generated when a settings dialog first
saves**. The UI splits configuration across dialogs: *Servers*
(LLM/TTS/STT endpoints — LLM URL defaulted to :8080 already,
owner only disabled TTS+STT), *Settings* (chat behavior:
`max_persona_replies` 1–4, max context turns, and a **Global
System Prompt appended to every persona's system prompt** — a
lever worth remembering for show-wide radio-style rules),
*Personas*, *Chat Rooms* (sidebar shows per-room "Echo chamber"
checkbox + who-should-answer routing). Generated settings.yaml, verbatim (post-save state before
Gates 5.3/5.4 filled the tts/stt URLs via the Servers dialog):

```yaml
llm:
  base_url: http://localhost:8080
  model: default
  max_tokens: 200
  temperature: 0.8
tts:
  enabled: false
  base_url: null
  timeout: 60.0
  streaming: false
  parameters: {}
stt:
  enabled: false
  base_url: null
  timeout: 30.0
general:
  persona_name_mentions: true
  max_persona_replies: 1
  max_turns_for_context: 6
  show_tool_calls: true
  enable_persona_memories: true
  global_system_prompt: ''
  personas_directory: null
mcp:
  servers: []
  max_tool_iterations: 8
```

(Step-6 note: `max_persona_replies` must go 1 → 4 for the
ensemble; `max_turns_for_context: 6` is a knob the radio show
will care about later.)

**Phase 4 prep:** persona factory run — 4 scientists created
(Daniel/Moira/Samantha/Ralph: prompt.md with `/no_think` line 1
+ radio-style constraints, `ref.wav` from macOS `say` voices,
`ref.txt` exact transcripts). **Full factory commands + cast
table: `placeholder-personas.md` in this folder** (added by the
2026-09-16 documentation audit — the commands had existed only
in chat). Upstream's default personas Alex + Luna kept alongside
(owner choice; they carry no radio constraints but sit outside
our chatroom).

**Gate 5.2 PASS — first in-app exchange, verbatim:** owner →
Daniel: "Status report." · Daniel: **"Equipment failing.
Zombies in sector three. Over."** — in-character, no markdown
fluff (persona prompt's anti-markdown clause working where the
raw curl showed `**Response:**`), no reasoning leak (the
`/no_think` toggle survives TalkWithMe's prompt assembly),
owner-reported "almost immediate". The core-question hypothesis
(configuration, not surgery) is now proven for the LLM leg
inside the real app.

### 2026-09-16 — Gate 5.3 PASS: voices in-app; streaming mechanics identified from source

**Servers dialog auto-detected the engine on URL entry**
(screenshot: engine faster-qwen3-tts, model 1.7B-Base, cuda,
24 kHz — TalkWithMe fetching tts-serve `/capabilities` v2 and
rendering its parameter schema as form fields: the fixture-based
integration working live). **Non-streaming:** reply text
instant; **~5 s to first sound** (whole-utterance synth + WAN).
**Streaming ON:** owner coaxed a 6-sentence monologue from
Daniel ("what do you want in your death report") — UI shows 6
audio fragments, **no perceptible inter-sentence lag**.

**Why gapless — from source, not vibes** (owner demanded code
evidence; three candidate explanations tested):

1. ✔ **TalkWithMe client-side pipelining** —
   `static/tts.js` header: "Streaming: split response into
   sentences, fetch and play in a pipeline"; fetch loop comment
   (~line 107): "Fetch TTS for queued sentences serially (to
   preserve order). Runs concurrently with audio playback so
   the next sentence's audio is ready by the time the current
   one finishes playing." Sentences are queued as LLM tokens
   stream in (synthesis starts before the LLM finishes the
   paragraph). Two independent queues: fetch-ahead + playback.
2. ✘ NOT tts-serve streaming — the `/synthesize` API is
   whole-utterance; no streaming exists to credit.
3. ✘ NOT parallel synthesis — fetches are explicitly serial
   (code comment above), confirmed by the tmux log timestamps:
   request N+1 starts ~1 s AFTER request N returns.
4. ✘ NOT a reference-reuse trick (owner's hypothesis,
   disproved): `app/routers/tts.py:134` calls
   `encode_reference_audio(persona.reference_audio)` on EVERY
   request — the ref clip is re-encoded and re-uploaded per
   sentence (log: `ref_text_len=96` on each call). The WAN-tax
   finding stands, now with file:line receipts.

The math that makes it work: per-sentence synth at RTF ≈ 0.5
(box log: `1.5 s wall / 3.0 s audio RTF=0.491`,
`0.3 s / 0.5 s RTF=0.644`) — fetch-ahead outruns playback, the
gapless-broadcast prediction observed in the real app.

```
05:55:08.153 Synthesizing: seed=840, text_len=48, ref_text_len=96
05:55:09.609 Synthesis complete: 1.5 s wall-clock, 3.0 s audio, RTF=0.491
05:55:10.608 Synthesizing: seed=702, text_len=5, ref_text_len=96
05:55:10.920 Synthesis complete: 0.3 s wall-clock, 0.5 s audio, RTF=0.644
```

**Owner's interim verdict:** "quite promising… it seems we have
proved that TalkWithMe + tts-serve can be separated into a local
client / remote cloud GPU without any local modifications to the
app." (Formal verdict still waits on the step-6 ensemble session
and findings.md.) **Owner worry recorded → brainstorm §5 C10**:
sentence-chunked synthesis may sever paragraph-level emotional
coherence on emotion-capable engines.

### 2026-09-16 — Gate 5.4 PASS: full voice loop — and challenges C1/C6 observed in the wild

STT enabled in the Servers dialog (`http://localhost:8002`).
Owner clicked the mic and spoke to Daniel. **The complete chain
worked**: browser mic → whisper (Norway) → Nemotron (Norway) →
Faster Qwen3-TTS (Norway) → browser speakers. Every component
of the §3.1 topology is now live simultaneously.

**The exchange, verbatim — a field specimen of our challenge
list:** owner said (accented English, imperfect conditions):
*"Oh no, the zombies got Miss Betty too."* → transcription:
*"Oh no, the zombie is called Nisbeti too."* → Daniel:
*"Containment protocols for Nisbeti are being reviewed.
Over."* — voice audio fine. Reading: (1) **C6 proper-noun
capture failing exactly as predicted** ("Miss Betty" →
"Nisbeti"; whisper-small + accent); (2) a brush of **C1**
robustness limits; (3) and — unplanned — the **in-fiction
absorption strategy working by accident**: the character
treated the garbled name as a fact of his world and carried on,
in character, unbroken. The C6 mitigation we designed on paper
(graceful degradation inside the fiction) just demonstrated
itself unprompted. Doubles as evidence for the [spec §10.5]
heckler-absorption posture.

**Step 5 complete.** Remaining: step 6 (4-persona ensemble
session + formal measures), optional step 7, teardown, verdict.

### 2026-09-16 (night) — Hibernation gamble taken; provider finding logged

Owner hibernated the box overnight (meter paused). Hyperstack's
own warning, captured verbatim before confirming: *"Hardware is
not reserved during hibernation. Restoring requires the same
flavor to be in stock. If unavailable, the VM cannot be restored
until resources become available."* → the last provider
red-flag check answered itself in documentation: hibernate is a
**restore-lottery** on a stock-volatile flavor. If tomorrow's
restore fails, the box state is lost — but this runlog's whole
purpose is that a rebuild costs ~30–45 min of paste (recorded
commands + cached HF downloads gone, models re-pull). Survey's
Hyperstack entry updated; demo-week rule hardened: never
hibernate the show box.

### 2026-09-16 (morning) — Restore lottery WON; hibernation semantics sharpened

The VM restored (same flavor back in stock). **Finding: Hyperstack
"hibernation" preserves DISK but not RAM/processes** — no process
survived, not even tmux. Operationally it behaves like
stop+boot-with-disk-kept, not a true suspend-to-disk resume.
Consequences: (a) every resume = full service restart — cheap
here because model caches survived on disk (no re-downloads) and
every launch command is in this runlog; (b) for Ansible, the
"resume" playbook and the "fresh boot" playbook are the SAME
playbook minus downloads — a simplification, if an annoying one;
(c) demo-week never-hibernate rule now double-underlined.

**Post-restore restart sequence (consolidated from earlier
entries — the de-facto resume runbook, promotion candidate for
`runbooks/` at arc close):** on the box: `tmux new -s radio`,
then per window — `llama`: the canonical docker command
(**v3**, in the 2026-09-16 pothole entry below) · `tts`:
`cd ~/faster-Qwen3TTS/tts-serve && source ../.venv/bin/activate`
+ the FASTER_QWEN3TTS launch line · `whisper`: the whisper-fastapi
docker command · `ops`: `watch -n2 nvidia-smi`. On the laptop:
the `ssh -N -L` tunnel; TalkWithMe via uvicorn if not still
running. Gates: the three-curl pulse check. (~90 s llama reload
window applies.)

### 2026-09-16 — Pothole: llama model cache mount was misrouted; canonical command v3

Post-restore, host `~/models` was EMPTY — the `-hf` download had
never landed on the mount. Diagnosis: the v1/v2 command's mount
target (`/root/.cache/llama.cpp`) was an agent assumption about
where the image caches; the image evidently uses a different
path, so the 6 GB GGUF lived in the ephemeral container layer
and died with `--rm` — meaning **every container start silently
re-downloaded the model** (yesterday's post-restart "wait a bit"
included). Contrast: whisper's HF-cache mount and the TTS venv's
host-side cache were routed correctly and survived hibernation.

**Fix — dictate the cache path instead of guessing it**, via
llama.cpp's `LLAMA_CACHE` env var. Canonical command **v3**
(supersedes v2):

```
docker run --name llama --rm --gpus all --network host \
    -v "$HOME/models:/models" -e LLAMA_CACHE=/models \
    ghcr.io/ggml-org/llama.cpp:server-cuda \
    -hf bartowski/nvidia_NVIDIA-Nemotron-Nano-9B-v2-GGUF:Q4_K_M \
    --host 127.0.0.1 --port 8080 -ngl 99 -c 16384 --parallel 1
```

Verification gate (new discipline: check the mount, don't assume
it): `ls -lh ~/models/` on the host must show the growing/final
`.gguf`. Ansible ledger: model caches are pinned to explicit
mounted paths via env (`LLAMA_CACHE`, `HF_HOME`-style), never
via assumptions about a container's HOME.

### 2026-09-16 — Services restored via the recipe; network baseline for measurement day

Full stack rebuilt post-hibernation by following the new
Reproduction recipe (its first real replay — passed). On-box
gates green; tunnel pulse green. VRAM read 12.3 GiB (vs 13.5
with the full trio yesterday) — believed: whisper lazy-loads its
model at first request; to re-check after first mic use.
Owner's subjective note: chat "feels a bit more delayed than
yesterday." **Network baseline for today's measures (laptop →
box, Norway):**

```
% ping -c 5 94.101.98.230
time=277.3 / 212.3 / 179.2 / 191.3 ms  (≈215 ms avg, high variance)
```

Every measure-(c) number today carries ≥1 RTT (~0.2 s) of
unavoidable network toll per request — annotate accordingly;
a Canada-1 demo box would re-price this.

### 2026-09-16 — Step 6 first contact: group chat works; speaker-label mimicry found (measure (e))

`Lab` room, 4 scientists, `max_persona_replies: 4`, routing
"LLM decides": multi-persona session WORKS (screenshot in owner
archive: Ralph/Moira/Samantha/Daniel trading perimeter chatter,
all in radio style with "Over."). Two findings:

1. **Speaker-label mimicry.** Some personas prefix replies with
   a bracketed name — e.g. Samantha: `[Samantha]: All access
   points are sealed. Over.`; Daniel used his SURNAME:
   `[Hayworth]: …`. Root cause found with receipt:
   `app/session.py:135/159` — in group rooms, other personas'
   turns are fed to the LLM as user-role messages prefixed
   `[Name]: <text>`, so the model adopts the convention for its
   own output (Daniel self-labeling from his system-prompt
   surname proves it's learned convention, not string copying).
   Pollutes TTS (labels get spoken). Fix attempt #1: a Global
   System Prompt counter-instruction (the Settings-dialog lever
   that appends to every persona prompt). If labels persist →
   the FORK TRIGGER fires: first patch = one-line output
   sanitizer stripping leading `[...]:` before display/TTS.
2. **Text→audio lag in group mode is mostly structural, not a
   fault**: all 4 text replies render fast; the audio queue is
   serial by design (one voice at a time — radio-appropriate),
   so the Nth speaker waits for N−1 spoken replies; each
   synthesis also pays today's ~215 ms Norway RTT. Re-priced by
   a closer region; unchanged by any code.

### 2026-09-16 — Label fix: works only on clean history; pause problem diagnosed to short-sentence fixed costs

**Speaker labels:** Global System Prompt counter-instruction
did NOT fix the existing `Lab` room, but after a server restart
+ fresh room `lab2`, no labels so far. Mechanism: **transcript
contamination** — the old history's `[Name]:` turns are
in-context examples, and examples beat instructions for small
models; one slipped label re-seeds the convention permanently.
Consequence: the prompt lever works prospectively only; the
one-line output sanitizer stays on the fork-trigger shortlist
as a FIREBREAK (not day-one required while lab2 stays clean).

**Inter-sentence pauses (owner's ear, sharpened):** the
annoying lag is not queue order — it's pauses WITHIN a reply,
worst before short sentences like "Over." Diagnosis: per-request
fixed costs (≈215 ms RTT + ~300 KB reference re-upload + ~0.3 s
engine floor ≈ 1 s+) dominate short sentences (~0.5 s audio) →
**effective RTF > 1 for short sentences**, and radio style is
MADE of short sentences. The gapless-broadcast math holds for
long sentences only. Two responses: (1) **zero-code first:
`streaming: false`** — radio transmissions are 1–2 sentences by
design, so whole-utterance = one request per transmission, no
intra-reply gaps, modest TTFA cost (~2.5 s est.); under test in
lab2. (2) **Owner's proposal, recorded as candidate upstream
patch**: replace per-sentence chunking with
"pack-sentences-up-to-max-chars" — the right algorithm for
longer monologues post-MVP (TalkWithMe tts.js chunker;
potential upstream contribution).

**C10 field note:** owner begins to notice emotional
inconsistency between chunks (weak signal — placeholder voices
are low-emotion to begin with) → logged to brainstorm C10.

### 2026-09-16 — Streaming A/B verdict; splitter naivety; group-degeneration mystery opened

**1. `streaming: false` is WORSE — agent prediction DIED.** The
agent predicted whole-utterance mode would suit short radio
transmissions; owner's ear: TTFA on moderate replies is "very,
very long." Owner's read of the mechanism (plausible, matches
the serial audio queue): pipelining does not cross speaker
turns — a turn's synthesis doesn't overlap the previous turn's
playback in non-streaming mode. Streaming stays ON; the real
fix is the chunker.
**2. The sentence splitter is naive** — specimen: Moira's
"Dr. Byrne. 47. Microbiology. Over." became FOUR requests with
audible gaps, including a split at the abbreviation "Dr." — the
splitter treats every period as sentence-end. Owner's
**max-chars accumulator** proposal is now doubly motivated: it
amortizes per-request fixed costs AND absorbs abbreviation
mis-splits. Standing as the designated upstream patch
(TalkWithMe `tts.js` chunker); NOT fixed during the spike —
this is adaptation-arc work.
**3. Group-degeneration observed (screenshot in owner archive):**
asked for a ≥5-sentence incident report, the four replies
shrank progressively — Moira full report → Ralph summary
ack → Samantha echo-ack → **Daniel's entire reply: "Over."**
Two live hypotheses: **(a) owner's** — the anti-label Global
System Prompt damages the model's grasp of multi-speaker
structure (labels may be load-bearing for identity); **(b)
agent's** — task-convergence + imitation collapse: the task was
singular, Moira completed it, followers pattern-matched into
shrinking acknowledgments (classic multi-agent echo). Evidence
against (a) being the whole story: the `[Name]:` labels in
HISTORY are still injected by `session.py` regardless — our
instruction only bans self-labeling in output, so identity
signal remains in context. **Discriminating A/B designed:**
fresh room `lab3` WITHOUT the Global System Prompt, repeat the
identical report request — degeneration persisting exonerates
the prompt; health implicates it.
**Scope guard (important):** none of these are architectural
blockers per the frozen verdict criteria — audio flows, the
session runs, the split holds. They are SHOW-QUALITY findings,
i.e. the adaptation arc's opening backlog, not spike failures.

**Deployment-notes ledger (feeds Ansible):** base packages a
fresh box needs before any tts-serve engine: `python3.X-venv`,
`sox`, plus `apt-get update` as step zero; venvs must be seeded
with `pip wheel setuptools numpy` before legacy-setup.py
engines. **Owner-raised alternative to per-engine venvs:
per-engine miniconda/miniforge** (batteries included — numpy
present, conda-forge ships the sox binary), which would have
dodged both potholes; counterweights: conda+pip mixing risk, and
the cu124 torch pin is pip-installed either way. Live question
for the deployment arc — venv path retained for this experiment
(the documented-path friction is itself the data).

### 2026-09-16 — lab3 A/B verdict; the stale-question specimen; source audit of the round machinery

**1. lab3 A/B (owner-run): the anti-label prompt is implicated.**
Fresh room `lab3`, Global System Prompt CLEARED, dialogue held up
better than the degenerated `lab2` round. Per the pre-wired
discriminator (previous entry): health implicates the prompt →
owner's hypothesis supported; agent's task-convergence hypothesis
wounded (caveat: single trial — implicated, not convicted).
Standing consequence adopted: allow `[Name]:` labels in context,
strip them before display/TTS — the one-line output sanitizer is
now the designated FIRST fork patch (or upstream PR).

**2. The stale-question specimen (owner-run, lab3, verbatim).**
Round 1 — owner: "Please report how many zombies you see."
Healthy replies:

```
Moira:    "Six in the lab. More outside. They're... not human
          anymore. Over."
Ralph:    Two. Three. Shamblers. Over.
Daniel:   Shamblers. Two. Over.
Samantha: Six. Seven. Over.
```

Round 2 — owner: "We need to write a report about the incident.
It must be at least five sentences long. Please proceed." Bad
replies:

```
Samantha: Understood. I'll compile the data we have. First,
          confirm the count of zombies inside and outside.
          Second, note the behavior changes—shamblers, not
          human. Third, mention the lab's current status.
          Fourth, assess if containment holds. Fifth, suggest
          next steps. Over.
Ralph:    Six. Seven. Containment breached. Over.
Moira:    Six. Seven. Containment breached. Over.
Daniel:   Containment breached. Prioritize securing the
          perimeter. Over.
```

Observed failures: Samantha produced a PLAN for the report, not
the report; Ralph and Moira answered the STALE round-1 question —
with Samantha's numbers ("Six. Seven."), not their own round-1
counts; Moira copied Ralph verbatim; nobody wrote five sentences.
Perfect radio format throughout — the failure is invisible to any
format check. Interpretation promoted OUT of this experiment to
[discussion 2026-09-16] (storytelling coherence & structure
adherence): this is the founding specimen of the COHERENCE axis,
mapping to six suspected mechanisms (A3, B4, C3, C6, C7, E2
there).

**3. Source audit triggered by the specimen (receipts):**

- `app/session.py:147-148` — the human user's messages keep role
  `user` with NO prefix or identity; only personas get `[Name]:`
  (lines 153–159). The director is the only unnamed participant
  in the transcript ("the invisible director", C6 in the
  discussion doc).
- `app/routers/chat.py:254-261` — only the FIRST speaker of a
  round is picked by the configured strategy; replies 2..N are
  `random.choice` among personas who haven't spoken. The report
  round was one chosen speaker + three random conscripts.
- `app/routers/chat.py:296` — rounds are SERIAL; each speaker's
  history "already includes prior personas' replies". Rules OUT
  stale-snapshot concurrency: the echoers saw the completed task.

Measure-(e) status unchanged by all of the above: show-quality
findings, not architectural blockers — the scope guard from the
previous entry stands. Zero-code follow-up probes (owner-typed,
one variable per run) are catalogued in the discussion doc §5.

### 2026-09-16 — Measure (c) harvested: the TTFA table (streaming mode passes; the A/B violators identified)

Raw evidence: `raw-tts-window-tail.txt` (812-line
`tmux capture-pane -t radio:tts -p -S -100000` dump, scp'd from
the box). Derived numbers: `extract_tts_timings.py` (committed,
stdlib-only; constants documented in its header). Reproduce:
`python3 extract_tts_timings.py`. Script output verbatim:

Parsed 152 synthesis requests -> 24 bursts (gap > 8 s).

| Burst | Start (box time) | Sents | 1st-sent wall (s) | Est. TTFA (s)* | Total wall (s) | Total audio (s) | RTF min-max |
|---|---|---|---|---|---|---|---|
| 1 | 20:01:18 | 2 | 1.3 | 1.5 | 1.7 | 1.5 | 0.67-1.48 |
| 2 | 20:01:53 | 2 | 0.3 | 0.5 | 0.6 | 0.6 | 0.79-0.81 |
| 3 | 20:02:39 | 2 | 0.3 | 0.5 | 0.6 | 0.8 | 0.72-0.78 |
| 4 | 20:03:55 | 6 | 3.5 | 3.7 | 14.5 | 31.5 | 0.46-0.72 |
| 5 | 20:15:55 | 3 | 0.7 | 0.9 | 1.8 | 3.3 | 0.51-0.75 |
| 6 | 20:16:55 | 2 | 0.6 | 0.8 | 0.9 | 1.6 | 0.54-0.69 |
| 7 | 20:17:45 | 1 | 0.7 | 0.9 | 0.7 | 1.3 | 0.57-0.57 |
| 8 | 20:18:51 | 8 | 0.7 | 0.9 | 5.0 | 9.0 | 0.52-0.69 |
| 9 | 20:26:34 | 8 | 1.8 | 2.0 | 5.7 | 9.7 | 0.48-0.78 |
| 10 | 20:29:10 | 11 | 1.2 | 1.4 | 5.4 | 9.5 | 0.51-1.12 |
| 11 | 20:30:36 | 12 | 0.5 | 0.7 | 5.3 | 8.1 | 0.55-1.07 |
| 12 | 20:40:02 | 9 | 0.4 | 0.6 | 3.3 | 5.4 | 0.55-1.10 |
| 13 | 20:40:45 | 18 | 1.1 | 1.3 | 9.0 | 15.5 | 0.53-0.78 |
| 14 | 20:48:35 | 1 | 14.7 | 14.9 | 14.7 | 29.9 | 0.49-0.49 |
| 15 | 20:49:23 | 1 | 6.6 | 6.8 | 6.6 | 14.5 | 0.45-0.45 |
| 16 | 20:49:47 | 1 | 5.9 | 6.1 | 5.9 | 13.0 | 0.46-0.46 |
| 17 | 20:50:09 | 1 | 0.3 | 0.5 | 0.3 | 0.5 | 0.68-0.68 |
| 18 | 21:00:37 | 1 | 10.2 | 10.4 | 10.2 | 18.3 | 0.56-0.56 |
| 19 | 21:01:08 | 1 | 6.7 | 6.9 | 6.7 | 14.7 | 0.45-0.45 |
| 20 | 21:01:33 | 1 | 4.4 | 4.6 | 4.4 | 9.6 | 0.46-0.46 |
| 21 | 21:01:50 | 1 | 0.3 | 0.5 | 0.3 | 0.4 | 0.73-0.73 |
| 22 | 21:10:03 | 25 | 0.6 | 0.8 | 14.1 | 24.9 | 0.49-0.95 |
| 23 | 21:21:55 | 16 | 0.7 | 0.9 | 6.4 | 10.7 | 0.51-0.75 |
| 24 | 21:34:44 | 19 | 0.5 | 0.7 | 14.4 | 26.8 | 0.48-0.74 |

*Est. TTFA = first-sentence server wall + 1 RTT (0.215 s). Excludes the ~300 KB reference upload and response download; treat as a lower bound.

Verdict input: 19/24 bursts have est. TTFA <= 5.0 s; max 14.9 s, median 0.9 s.

Short-sentence economics (server-side only; the per-request network toll makes the real gap worse):
- text_len <= 25: 125 requests, mean RTF 0.65, 5 with RTF > 1
- text_len  > 25: 27 requests, mean RTF 0.50, 0 with RTF > 1

**Reading (interpretation to be consolidated in findings.md at
verdict time):**

- **Median est. TTFA 0.9 s; 19/24 bursts ≤ 5 s.** Bursts 1–13
  are THIRTEEN CONSECUTIVE replies under the 5 s line — the
  frozen criterion's "sustained over ≥10 consecutive lines"
  clause is met on streaming-mode evidence.
- **The 5 violators are all single-sentence bursts carrying
  13–30 s of audio, clustered 20:48–20:50 and 21:00–21:01** —
  the fingerprint of whole-utterance (non-streaming) synthesis.
  Believed to be the `streaming: false` A/B trials (owner to
  confirm timing); if so, measure (c) independently convicts
  non-streaming mode: worst case 14.9 s est. TTFA, matching the
  owner's-ear verdict ("very, very long") from the earlier
  entry.
- **Short-sentence economics quantified:** 125 requests with
  text_len ≤ 25 → mean RTF 0.65, five already >1.0 SERVER-SIDE;
  27 longer requests → mean RTF 0.50, none >1.0. Add the
  ≥0.2 s/request network toll and short sentences routinely go
  effective-RTF > 1 — the max-chars accumulator's case, now
  with numbers.
- Caveat kept honest: Est. TTFA = server wall + 1 RTT only; the
  ~300 KB reference upload and response download are excluded,
  so real client TTFA is somewhat higher — and still clears the
  bar with margin in streaming mode.

### 2026-09-16 — Step 7 SKIPPED (rationale recorded); creative tests cut at timebox

**Step 7 (plain `ws://`+token transport variant): SKIP.** The
plan allowed testing the laptop↔box channel both ways "if cheap."
It is no longer cheap or informative: the SSH tunnel is DECIDED
([spec §10.3]), validated end-to-end by every gate and measure in
this runlog, and measure (f) showed the stack provides NO
authentication of its own — a plain-`ws://` variant would test a
transport we have already ruled out for a stack that cannot
survive it. Nothing the MVP will ship depends on the answer.

**Creative tests (wire-cut mid-session, Spanish exchange,
broadcast soak): CUT at the timebox.** Owner closed the
experiment 2026-09-16 evening (inside the abort-by-2026-09-17
timebox) with one hour of budget left; the discussion doc
([discussion 2026-09-16], narrative health §5) carries the soak
and the zero-code probe battery as designed future tests — they
are not lost, they are queued where the next arc will look.

### 2026-09-16 — Name-memory micro-test: FAILED, then half-exonerated by a config receipt; final VRAM; teardown initiated

**The test (owner-run, lab3, verbatim).** Setup: "Moira, the
survivor on the roof is called Callsign Vulture. Remember her."
In-round echo worked (all four wove "Vulture" in: "Vulture.
Roof. Secure. Over."). Then two distractor rounds and the recall:

```
User: Moira, the new head of accounting is Betty, she replaces
Anna, after she became a zombie herself. Remember her.
Moira:    Betty's not here anymore. Over.
Samantha: Accounting reports are paused. Over.
Daniel:   Accounting frozen. Over.
Ralph:    Count cans. Over.

User: No, I mean Anna became one of the creatures.
Moira:    Anna's body's gone feral. Over.
Ralph:    Cans in the east wing. Over.
Samantha: East wing secure. Over.
Daniel:   Secure for now. Over.

User: Moira, what was the name of the survivor on the roof?
Moira:    Clare. Over.
Daniel:   Clare was the last one on the roof. Over.
Samantha: Clare's radio signal went dark minutes ago. Over.
Ralph:    Clare's radio dead. Over.
```

Recall FAILED — "Clare" is a confabulated name, promptly adopted
by the whole cast within the round.

**The receipt that reframes it:** `app/config.py:171` and the
live `settings.yaml:19` — **`max_turns_for_context: 6`**, counted
in history ENTRIES (one message each), not rounds. In a 4-persona
room, six entries ≈ ONE round. At recall time the Vulture fact
sat ~14 messages back: physically absent from Moira's context.
"Clare" is not failed recall but FORCED confabulation — the model
was asked about a fact it was never shown and improvised
in-character; C3 imitation then locked all four onto the invented
name (locally coherent, globally amnesiac — the signature of a
tiny sliding window). Corollaries: (1) we provisioned -c 16384
and use ~1k of it — the fix is a pure config lever
(settings.yaml, cap 50); (2) the window counts turns, not rounds,
so it SHRINKS PER CAPITA as the cast grows — logged to
[discussion 2026-09-16] as mechanism C9; (3) it may recolor the
stale-question specimen: at round 2 the round-1 QUESTION sat
exactly at the 6-entry boundary — the conscripts likely saw
round-1's answers with their question already evicted.

**What the model does NOT get exonerated for:** the Betty/Anna
exchange garbled with everything in context ("Betty's not here
anymore" inverts the stated fact; the pronoun chain defeated it).
Owner's assessment on the day: "the intelligence of the dialog is
very low... we cannot rule out having to change the LLM model."
Exactly the ranked-shortlist design ([discussion 2026-09-14]):
the Track 3 audition picks the default; Nemotron's rank-1 is
presumptive, not settled — and the audition should re-run this
micro-test with a properly sized window.

**Final VRAM reading (full trio, post-mic-use, whisper loaded):**

```
memory.used [MiB], memory.total [MiB]
14009 MiB, 15352 MiB
```

14.0/15.0 GiB — the 16 GB card holds the full stack with ~1.3 GiB
headroom. The 16 GB-aspiration datum, final form.

**Teardown (step 8): initiated.** Owner defers the console
destroy + billing glance to later today (meter runs until then);
the tunnel is closed. Destroy checklist stands: full Delete (not
Hibernate/Stop) — this box is the grandfathered R535 exception
and dies by decree; final cost figure to be appended here when
read.

### 2026-09-16 — CLOSING ENTRY: final cost, loose threads trued, experiment sealed

**Final cost (step 8, owner-read from the Hyperstack console):
$2.97 total** for the whole experiment — two days of A4000 at
$0.15/hr with an overnight hibernation pause. The entire
foundation-validating spike cost less than a coffee; datum for
demo-week budgeting (a multi-day A6000 run will cost more, but
the order of magnitude is established).

**Loose threads trued at close:**

- **Whisper lazy-load: CONFIRMED** (was "believed, to re-check"
  in the post-restore entry): 12.3 GiB before any STT request →
  14.0/15.3 GiB final reading with everything warm and in use.
  Recipe R6 expectation amended accordingly.
- **Step checklist trued:** 6 done, 7 skipped (rationale
  above), 8 done. All steps closed.
- **Known hedge left standing (recorded, not resolved):** the
  TTFA table's five >5 s bursts are attributed to the
  `streaming: false` A/B trials by timing fingerprint
  (20:48–20:50, 21:00–21:01) — the owner has not separately
  confirmed those wall-clock windows. The attribution is marked
  "believed" in the measure-(c) entry and stays that way unless
  confirmed.
- Taxonomy count corrected in findings.md: the discussion doc
  holds **20** mechanisms (a stale "17" predated C9 and the
  coherence-axis pass).

**The experiment is sealed.** Per `experiments/README.md`, this
folder is now edited only to fix factual transcription errors
(dated note). Verdict: PASS (findings.md). The box is gone; the
recipe (R0–R13) is the box, whenever we need it again.

### 2026-09-16 (post-close dated note, per the sealed-folder rule)

The measure-(c) hedge is resolved: the owner CONFIRMED the
20:48–20:50 and 21:00–21:01 windows were the `streaming: false`
trials. The five >5 s TTFA bursts are now owner-confirmed (not
merely "believed") to be the rejected non-streaming mode — the
attribution in findings.md stands as written.
