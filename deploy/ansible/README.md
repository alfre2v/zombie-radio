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
make ans-deploy ENV=cloud
make ssh-tunnel ENV=cloud   # separate terminal, stays open
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
- Torch-family wheels are pinned to the CUDA generation in
  `zr_cuda_variant` (`cu128` today, matching the R570 image) —
  PyPI defaults float to the newest CUDA major and crash-loop on
  older-major drivers. The base role asserts the box's driver can
  run the pinned generation before anything installs; a different
  provider/driver is a one-line `99-<env>.yml` override of
  `zr_cuda_variant`. The rule: provider survey §S5; the events:
  the arc journal, entries 2026-09-18/19.
- Deploy runs log to `~/.config/zombie-radio/logs/`.
- SSH: the identity is declared (`ansible_ssh_private_key_file`
  in common_vars) and is the only key offered; unknown host keys
  are accepted automatically on first contact (TOFU — no manual
  `ssh` before deploying), recorded in
  `~/.config/zombie-radio/known_hosts`. Providers recycle IPs: a
  "REMOTE HOST IDENTIFICATION HAS CHANGED" failure means a stale
  entry there — delete the file (or the line) and rerun.
