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
- TalkWithMe version: *(TBD — step 5; expected v7.0)*
- tts-serve engine: **Faster Qwen3-TTS** (chosen via
  `tts-engine-ranking.md`; default checkpoint
  Qwen3-TTS-12Hz-1.7B-Base)
- LLM model: **Nemotron Nano 9B v2 Q4_K_M** (bartowski GGUF)
- STT: **whisper-fastapi** (heimoshuiyu image), model `small`
- Network path: laptop ⇄ internet ⇄ box, via `ssh -L` tunnel
- STILL TO RECORD (owner, from console): exact Hyperstack flavor
  name + region for the A4000 VM (step 1 residual)

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
- [x] 3. All three model services UP, loopback-bound (DONE
      2026-09-15): llama.cpp/Nemotron (6.9 GB, 47.6 tok/s) ·
      Faster Qwen3-TTS (5.0 GB, rtf 0.455) · whisper-fastapi
      small (1.5 GB, 7.3 s audio in 1.85 s). Trio: 13.5/15.3 GiB.
- [x] 4. Tunnel verified for ALL services (DONE 2026-09-15):
      LLM chat, TTS synthesis (cloned voice audible on laptop),
      STT full-circle transcription of our own TTS output.
      Cold-connection overhead ~0.6–0.7 s, amortizable.
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
