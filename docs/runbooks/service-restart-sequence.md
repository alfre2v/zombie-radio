# Runbook: restart the model-service stack (box already installed)

*Living, undated (runbooks convention). Promoted 2026-09-17 from
the remote-split experiment's post-restore entries, where it was
executed twice (once after hibernation, once as a recipe replay).
Scope: a box that ALREADY has the software installed — after a
reboot, stop/start, or Hyperstack "hibernation" (which kills all
processes but keeps the disk). For a FRESH box, follow the full
Reproduction recipe (R0–R13) in
`experiments/2026-09-14-talkwithme-remote-split-test/README.md`
first; this runbook is its fast path.*

**Topology reminder:** all three model services bind to
`127.0.0.1` on the box (nothing public but :22); the laptop
reaches them through one SSH tunnel; TalkWithMe runs ON the
laptop at `http://localhost:8000`.

## On the box (SSH as `ubuntu`)

**1. tmux layout** (see the experiment's `tmux-refresher.md`):

```bash
tmux new -s radio
```

Windows: `llama`, `tts`, `whisper`, `ops`.

**2. Window `llama` — LLM server** (model loads from the disk
cache in ~90 s; first-ever run downloads ~6 GB instead):

```bash
docker run --name llama --rm --gpus all --network host \
    -v "$HOME/models:/models" -e LLAMA_CACHE=/models \
    ghcr.io/ggml-org/llama.cpp:server-cuda \
    -hf bartowski/nvidia_NVIDIA-Nemotron-Nano-9B-v2-GGUF:Q4_K_M \
    --host 127.0.0.1 --port 8080 -ngl 99 -c 16384 --parallel 1
```

Verify the cache is mounted right: `ls -lh ~/models/` shows the
`.gguf`.

**3. Window `tts` — TTS engine:**

```bash
cd ~/faster-Qwen3TTS/tts-serve && source ../.venv/bin/activate
FASTER_QWEN3TTS_HOST=127.0.0.1 FASTER_QWEN3TTS_PORT=8001 python impl/server_fasterQwen3TTS.py
```

**4. Window `whisper` — STT server:**

```bash
docker run --rm --network host --gpus all \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  docker.io/heimoshuiyu/whisper-fastapi:latest \
  --model small --device cuda --host 127.0.0.1 --port 8002
```

**5. Window `ops` — monitor:**

```bash
watch -n2 nvidia-smi
```

**6. On-box gates** (run in `ops`):

```bash
curl -s http://127.0.0.1:8080/health
curl -s http://127.0.0.1:8001/capabilities | head -c 200; echo
curl -s -o /dev/null -w "stt: %{http_code}\n" http://127.0.0.1:8002/docs
```

VRAM expectation: ~13.5 GiB with all three loaded; ~12.3 GiB
until the first STT request (whisper lazy-loads); ~14.0 GiB fully
warm.

## On the laptop (Mac)

**7. Tunnel** (own terminal tab, stays open):

```bash
ssh -N -L 8080:127.0.0.1:8080 -L 8001:127.0.0.1:8001 -L 8002:127.0.0.1:8002 ubuntu@<PASTE-BOX-IP-HERE>
```

**8. Pulse check through the tunnel:**

```bash
curl -s http://localhost:8080/health && curl -s -o /dev/null -w "tts: %{http_code}\n" http://localhost:8001/capabilities && curl -s -o /dev/null -w "stt: %{http_code}\n" http://localhost:8002/docs
```

**9. TalkWithMe** (if not already running):

```bash
cd ~/workspace/hackTNT_2026/TalkWithMe && source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**10. Smoke gate:** open `http://localhost:8000`, pick a
scientist → text chat answers in character → voice plays → mic
round-trips.

## Gotchas that earned their lines

- **Never hibernate a show box** — Hyperstack hibernation is
  stop+boot-with-disk behind a restore-stock lottery; every
  resume is a full restart via this runbook (disk caches survive;
  processes never do).
- The llama container takes **~90 s** to reload the model —
  don't diagnose before the "model loaded" line.
- If `~/models/` is empty after a llama start, the cache mount is
  wrong — the model silently re-downloads every start (the
  `LLAMA_CACHE` env in the command above is the fix; don't guess
  container cache paths).
- Server URLs in TalkWithMe's Servers dialog point at
  `http://localhost:<port>` (the tunnel's laptop side), never at
  the box IP.
