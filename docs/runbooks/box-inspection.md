# Runbook: inspect a deployed GPU box

*Living, undated (runbooks convention). The quick-scout commands
for a box the playbook has converged: what runs, is it what we
expect, where the logs are. Everything here is read-only. SSH in
as `ubuntu` (or run one-offs via `ssh ubuntu@<ip> '<cmd>'`).*

## Containers (llama, whisper)

```bash
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'
```

Expect `llama` and `whisper`, both `Up`. Verify the supervision
config actually landed:

```bash
docker inspect -f '{{.Name}}: restart={{.HostConfig.RestartPolicy.Name}} net={{.HostConfig.NetworkMode}}' llama whisper
```

Expect `restart=unless-stopped net=host` on both.

## The tts systemd unit

```bash
systemctl status tts-faster_qwen3tts --no-pager
systemctl is-enabled tts-faster_qwen3tts docker
```

Expect `active (running)`, and `enabled` twice (both switches the
reboot auto-rise depends on). A crash-looping unit shows
`activating (auto-restart)` and a rising "restart counter" —
go straight to its journal.

## Logs, one command per service

```bash
docker logs -f llama          # or --tail 100 for a snapshot
docker logs -f whisper
sudo journalctl -u tts-faster_qwen3tts -f    # -n 100 for a snapshot
```

## GPU

```bash
nvidia-smi        # driver/CUDA versions, per-process VRAM
nvtop             # live cockpit (NOT preinstalled — owner installs when
                  # wanted; apt dry-run verified: zero driver deps)
```

Healthy full stack (one TTS engine): llama ~6.7 GiB · tts
~4.8 GiB · whisper ~0.8 GiB idle (lazy-loads at first STT
request, grows after first mic use).

## Health gates

On the box (what the playbook's own gates poll):

```bash
curl -s http://127.0.0.1:8080/health
curl -s http://127.0.0.1:8001/capabilities | head -c 200; echo
curl -s -o /dev/null -w "stt: %{http_code}\n" http://127.0.0.1:8002/docs
```

From the laptop, through the tunnel: `make check`.

## Disk and model caches

```bash
df -h /
du -sh ~/models ~/.cache/huggingface
```

`~/models` = llama's GGUF cache (HF-hub-style blobs, no .gguf
extension). `~/.cache/huggingface` = TTS checkpoint + whisper
model, shared tree.

## The converge invariant

A re-run of `make ans-deploy ENV=cloud` against a healthy,
unchanged box must report **changed=0**. Any `changed` on a
no-op converge is a bug in a role (it also needlessly restarts
services via handlers) — diagnose which task and fix the role;
do not shrug it off.
