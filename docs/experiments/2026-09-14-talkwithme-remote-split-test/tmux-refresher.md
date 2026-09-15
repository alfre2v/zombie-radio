# tmux refresher for the experiment box

**Date:** 2026-09-15 · **Part of:** the remote-split test (this
folder). Preserved nearly verbatim from the working session at
the owner's request — the operational how-to for keeping the
model services alive on the VM. (If this outlives the
experiment, it graduates to `runbooks/`.)

**Why we need it at all:** every process you start over SSH dies
when the connection drops (SIGHUP on session end). Our three
model services must keep running while the laptop sleeps, the
Wi-Fi hiccups, or you simply disconnect for the night. tmux
detaches the processes from the SSH session — they live inside a
tmux *server* on the VM, and you re-attach to find everything
(including scrollback logs) exactly as you left it.

## One-time setup on the VM

Probably already installed — check first:

```bash
tmux -V || sudo apt-get update -qq && sudo apt-get install -y tmux
```

Then a 3-line quality-of-life config — mouse support (scroll and
click between panes) and deep scrollback for logs:

```bash
printf 'set -g mouse on\nset -g history-limit 100000\nset -g default-terminal "screen-256color"\n' > ~/.tmux.conf
```

## The experiment's layout — one named session, one window per component

```bash
tmux new -s radio
```

That drops you *inside* the session. The entire command
vocabulary needed — everything starts with the prefix
**`Ctrl-b`**, pressed-and-released, *then* the key:

| Keys | Effect |
|---|---|
| `Ctrl-b c` | new window |
| `Ctrl-b ,` | rename current window (name them `llama`, `tts`, `whisper`, `ops`) |
| `Ctrl-b 0`…`3` | jump to window by number |
| `Ctrl-b n` / `p` | next / previous window |
| **`Ctrl-b w`** | interactive tree of ALL sessions + their windows — arrows to navigate, Enter to jump (the "where am I" command; with mouse on, clickable) |
| `Ctrl-b s` | session list only (Enter switches) |
| **`Ctrl-b d`** | **detach** — session keeps running, you're back in plain SSH |
| `Ctrl-b [` | enter scroll mode (arrows/PgUp; `q` to leave) — or just mouse-scroll with this config |
| `Ctrl-b &` | kill current window (confirms first) |

From outside (after any reconnect):

```bash
tmux attach -t radio
```

```bash
tmux ls
```

## The working pattern for the services

Window `llama` runs the llama.cpp container in the foreground
(its logs live there) · window `tts` runs the engine venv ·
window `whisper` the STT server · window `ops` keeps a
`watch -n2 nvidia-smi` and a spare shell. Each service's window
*is* its log viewer. Detach with `Ctrl-b d` whenever; everything
survives.

**One boundary note:** the SSH **tunnel** is the exception — it
runs on the *laptop* side (it's your laptop reaching in), so it
lives in an ordinary local terminal tab, not in the VM's tmux.
If it drops, just rerun it; the services on the box never notice.

## Two-minute practice loop

Create session → make and rename two windows → run `watch date`
in one → detach → `tmux ls` → reattach → scroll back → kill the
watch. Once that feels smooth, the muscle memory is back.
