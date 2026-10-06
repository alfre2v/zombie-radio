# Runbook: the stack on the home 3090

*Living, undated (runbooks convention). How to deploy, start, stop,
reach and remove the model-service stack on the owner's Linux desktop
(hostname `aorusX570`, an RTX 3090 with 24 GB). **Proven on the 3090
(2026-10-06):** a deploy from zero with `ENV=local` (about 8½ minutes)
and a second run at `changed=0`; from the laptop, `lan` at `changed=0`
(on the box `local` had deployed), the tunnel, and a show. **Not yet
run there:** a `lan` deploy from zero, the reboot test, `make
ans-start` / `ans-stop`, the removal recipe. The
why: [discussion 2026-10-02] local-gpu-deployment-plan §10.*

## The box, and how it differs from the cloud

The 3090 passed every prerequisite the playbook asserts (Ubuntu
22.04.5, driver R580, Docker with the NVIDIA runtime, the NVIDIA
container toolkit; the plan's §9.2). It is a personal desktop, not a
rented box, so its two environments differ from `cloud` in four ways:

| | `cloud` | `local` and `lan` (the 3090) |
|---|---|---|
| The user | `ubuntu` | `alfredo` |
| sudo | no password | asks for the password: add `ANS_ARGS=-K` to deploys, starts and stops |
| At boot | the three services start by themselves | **nothing starts** (`zr_start_at_boot: false`); start them by hand |
| The downloads | spread under `/home/ubuntu` | **one folder**, `~/zombie-radio-data` (below) |

## Two environments, one box

Both deploy the same stack to the same 3090, with the same settings;
only the machine Ansible runs on differs.

- **`local`** — Ansible runs **on the 3090 itself** (`ansible_connection:
  local`, no SSH). Run every command in a terminal on the 3090. Its
  modules use the system Python (`ansible_python_interpreter:
  /usr/bin/python3`): a local run would otherwise pick the project's
  `.venv` Python, which lacks the `requests` the Docker modules need.
- **`lan`** — Ansible runs **on the laptop** and reaches the 3090 over
  SSH, like the cloud: the same playbook, from the same laptop, to a
  rented GPU or a GPU at home. Uses the key `~/.ssh/zombie_radio_3090`
  and the SSH alias `zr-3090` (the owner's `~/.ssh/config`).

## Once per clone (on the machine that runs Ansible)

```bash
# The project's own Ansible in .venv, and the never-commit git hook armed
make install
# The pinned Ansible collections, inside the repo
make ans-deps
```

For `lan`, once per laptop clone: wire the inventory to the SSH alias,
so no address ever appears in the file. The wired `hosts.yml` must
never be committed (the hook blocks it); `make ans-unset ENV=lan`
restores the sentinel.

```bash
make ans-set ENV=lan IP=zr-3090
```

## Deploy

On the 3090 (`local`), or on the laptop (`lan`); type the sudo password
at the `BECOME password:` prompt:

```bash
make ans-deploy ENV=local ANS_ARGS=-K
make ans-deploy ENV=lan ANS_ARGS=-K
```

The first deploy downloads about 11 GB of models, plus the two Docker
images (about 9.4 GB) and the voice's Python environment (7.6 GB); no
`--check` dry run on a never-deployed box: the health waits run for
real and poll servers a dry run never started. A second run must report
`changed=0` (the converge invariant, [box-inspection.md]). The deploy
ends with the three services running; the run's log lands in
`~/.config/zombie-radio/logs/` on the machine that ran it.

## Start and stop by hand

After a reboot of the 3090 nothing runs, and the GPU is free for other
work. Start the three services, and wait until they answer (llama
reloads its model, about 90 seconds):

```bash
make ans-start ENV=local ANS_ARGS=-K
make ans-stop ENV=local ANS_ARGS=-K
```

The same with `ENV=lan` from the laptop. `ans-start` fails on a box
that was never deployed: deploy first. (The two targets work for
`cloud` too, without `-K`; there the boot setting is unchanged.)

## Reach the services

- **A client on the 3090 itself:** no tunnel. The services listen on
  the 3090's loopback, `localhost:8080`, `:8001`, `:8002`; `make check`
  on the 3090 probes them.
- **The client on the laptop:** the SSH tunnel, after a `local` or a
  `lan` deploy alike (the tunnel needs only the wired `lan` inventory).
  Close the cloud's tunnel first: both forward the same local ports.

```bash
make ssh-tunnel ENV=lan    # own terminal, stays open
make check                 # expect three ok lines
```

## The GPU is shared

The 3090 also drives the desktop (about 0.5 GB in use when idle, the
plan's §9.2), and Ollama runs on it as a service. Measured on the 3090
right after the first deploy (2026-10-06): llama 6,966 MiB, the voice
4,736 MiB, Whisper 896 MiB — 12,598 MiB; the voice grows during shows
as it caches the clips it clones from (the A6000's stack reached 14,477
MiB). Before a show, check what else holds the GPU:

```bash
nvidia-smi
```

## Where everything lives

| What | Where |
|---|---|
| llama's model | `~/zombie-radio-data/models` |
| Whisper's model | `~/zombie-radio-data/whisper-cache` |
| The voice's checkpoint | `~/zombie-radio-data/voice-cache` (`HF_HOME` in the voice's unit) |
| The voice's Python environment and tts-serve | `~/zombie-radio-data/faster_qwen3tts` |
| The llama and Whisper images | Docker's own storage, `/var/lib/docker` (shared with every other container on the machine) |
| The voice's systemd unit | `/etc/systemd/system/tts-faster_qwen3tts.service` |
| pip's download cache | `~/.cache/pip` (the owner keeps it) |
| Two system packages from the base role | `python3-venv`, `sox` (apt) |

The containers run as root, so some files under `~/zombie-radio-data`
belong to root (as on the cloud box).

## Remove the stack from the 3090

On the 3090. The images first, while the containers still name them:

```bash
# The two images the containers run, noted before the containers go
img_llama=$(docker inspect -f '{{.Image}}' llama); img_whisper=$(docker inspect -f '{{.Image}}' whisper)
# The containers, then their images
docker rm -f llama whisper
docker rmi "$img_llama" "$img_whisper"
# The voice's unit: stopped, disabled, removed
sudo systemctl disable --now tts-faster_qwen3tts
sudo rm /etc/systemd/system/tts-faster_qwen3tts.service
sudo systemctl daemon-reload
# Every download in one go (sudo: the containers wrote some files as root)
sudo rm -rf ~/zombie-radio-data
```

Left in place on purpose: Docker itself, the two system packages
(`python3-venv`, `sox`), pip's cache, and the clone with its logs.
A later `make ans-deploy` rebuilds everything from zero.

## When the deploy fails (met on the first deploy, 2026-10-06)

- **`Failed to update apt cache after 5 retries:` with no reason** — a
  package source on the machine is broken, and the playbook's package
  step refreshes all of them. Find which one: `sudo apt-get update`
  (look for `Err:` and `E:` lines). On the 3090 it was HashiCorp's
  source, its signing key renewed (`NO_PUBKEY`): refresh the source's
  keyring from its vendor, then `sudo apt-get update` must be clean.
- **`Failed to import the required Python library (requests)` on the
  project's `.venv` Python** — the environment's modules run on the
  wrong Python: `ansible_python_interpreter` belongs in its
  `99-<env>.yml` (set in `local`'s).
- **`403 Client Error ... ghcr.io ... denied: denied`** pulling a public
  image — a stale ghcr.io login in **root's** Docker config (the
  playbook pulls as root). Check the registry names only: `sudo python3
  -c 'import json; print(list(json.load(open("/root/.docker/config.json")).get("auths", {})))'`;
  then `sudo docker logout ghcr.io` (the 3090's fix), or pull the image
  once as your own user (`pull: missing` then skips it).

[box-inspection.md]: box-inspection.md
