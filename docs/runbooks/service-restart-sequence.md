# Runbook: (re)start the model-service stack

*Living, undated. REWRITTEN 2026-09-18 the day the playbook first
succeeded, per the single-source-of-truth ruling ([discussion
2026-09-17] ansible-deployment-shape §4/§11): the deployment
truth lives in `deploy/ansible/`; this runbook just tells you
which command to run when. The tmux-era manual sequence this file
used to contain is preserved in the sealed remote-split
experiment folder (its Reproduction recipe) as provenance.*

## After a VM reboot: do nothing

The stack rises unattended — Docker restart policies + enabled
systemd units (proven 2026-09-18: full auto-rise in under a
minute). Just re-open the tunnel and verify:

```bash
make ssh-tunnel ENV=cloud    # own terminal, stays open
make check             # expect three ok lines
```

## Fresh box, drifted box, post-restore, or "something is off"

One command converges it — from zero or from any intermediate
state (idempotent; a healthy box reports changed=0):

```bash
make ans-deploy ENV=cloud     # or ENV=local
```

Prerequisites (once per clone): `make install` + `make ans-deps`.
Per box: `make ans-set ENV=cloud IP=<box-ip>` (wires hosts.yml;
the `NEVER_COMMIT` hook guards the wired file, and
`make ans-unset ENV=cloud` restores the sentinel when the box
dies) — nothing else: host keys are accepted automatically on
first contact (TOFU, changed-key alarm kept; shape doc §15), and
the SSH identity is declared in common_vars. First-ever deploy
downloads models (~11 GB total); budget ~15 min.

## The manual bits (laptop side, by design)

- The tunnel: `make ssh-tunnel ENV=cloud`.
- TalkWithMe: `cd ~/workspace/hackTNT_2026/TalkWithMe &&
  source .venv/bin/activate && uvicorn app.main:app
  --host 127.0.0.1 --port 8000` → http://localhost:8000
  (saved server config points at the tunnel ports already).

## When something looks wrong

`runbooks/box-inspection.md` — status, logs, GPU, health gates,
cache anatomy. Deploy run logs live on the laptop at
`~/.config/zombie-radio/logs/`.

## Standing rules that survive from the tmux era

- **Never hibernate a show box** (Hyperstack hibernation =
  stop+boot behind a restore-stock lottery). Reboot is fine —
  see above. Destroy + redeploy is also fine: it is one command
  and ~15 minutes.
- llama's model reload takes up to ~90 s on a cold start — don't
  diagnose before `docker logs llama` shows "model loaded".
