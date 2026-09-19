# Zombie-Radio deployment (Ansible)

Converges a GPU box (SSH-able Ubuntu, docker + NVIDIA toolkit
present) to the full model-service stack: llama.cpp (LLM) +
tts-serve (TTS, engine selectable) + whisper-fastapi (STT), all
loopback-bound behind an SSH tunnel.

Design doctrine and rationale:
`docs/discussions/2026-09-17-ansible-deployment-shape.md`.
Operations: `docs/runbooks/service-restart-sequence.md` and
`docs/runbooks/box-inspection.md`.

## Quick start (from a fresh clone, all via the top-level Makefile)

```bash
make install      # uv venv + ansible + arms the NEVER_COMMIT git hook
make ans-deps     # pinned collections, project-local
# paste the box IP into inventories/cloud/hosts.yml (NEVER_COMMIT line)
# accept the host key once: ssh ubuntu@<ip> true
make ans-deploy ENV=cloud
make ssh-tunnel   # separate terminal, stays open
make check        # three ok lines = stack reachable from the laptop
```

`make help` lists everything else (`ans-lint`, `ans-check-syntax`,
`ans-config`).

## Layout in one breath

- `site.yml` — one play, `hosts: all`, play-level `become` (the
  privilege doctrine: roles assume root; `become_user` marks
  exceptions). Control-node preflights run BEFORE facts: an
  unwired or misdirected run fails having dialed nothing.
- `inventories/<env>/` — one directory per ENVIRONMENT (cloud,
  local), never targeted together; shared truth in
  `inventories/common_vars.yml`, symlinked as `00-common.yml`;
  `99-<env>.yml` overrides. Service-shaped groups (`llama`,
  `tts_engine`, `stt_engine`) state the topology.
- `roles/` — one role per service, SELF-GATING on its same-named
  group (`<role>_enabled`); `base` asserts Ubuntu + docker/NVIDIA
  tooling (asserted, never installed). The TTS engine is a
  variable (`zr_tts_engine`); its bespoke install lives in
  `roles/tts_engine/tasks/tts_engine_<engine>.yml` + a matching
  vars file.
- `collections/` — pinned, project-local (`ansible.cfg`
  `collections_path`).

## Conventions that bite if unknown

- `REPLACE_ME` values are sentinels; the placeholder preflight
  blocks deploys, and the NEVER_COMMIT hook blocks commits of a
  marked line whose placeholder was replaced by a real value.
- Torch and torchaudio are pinned to cu128 builds matching the
  R570 image's CUDA 12.8 — PyPI defaults (cu130) crash-loop on
  this driver. Details: the arc journal, entry 2026-09-18.
- Deploy runs log to `~/.config/zombie-radio/logs/`.
