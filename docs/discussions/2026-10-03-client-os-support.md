# The client's operating systems — macOS proven, Linux likely, Windows unknown

**Date:** 2026-10-03 · **Arc:** MVP prototype · **Branch:** `alfre2v/talk`
**Type:** discussion — on which operating systems the client (TalkWithZombies, the app on the laptop) runs, what in
our system ties it to macOS, and how to prove Linux and Windows; the idea of a `make client-linux`.
**Status:** OPEN — the code read, nothing tried on Linux or Windows yet. The Linux try is Task 11.2 in `docs/TODO.md`;
the wider proof is the follow-up "The client on Linux and Windows" in `docs/follow-ups.md`.
**Trigger to revisit:** the manual client install on the 3090 (Task 11.2), or a decision on `make client-linux`.

## §1. How it came up

While building the talk's slide "The machines" ([discussion 2026-10-03] the-talk), the laptop was labelled "the
client: macOS". The owner (verbatim, 2026-10-03):

> One detail I don't like: `the client: macOS` ... Actually the client can be installed in Linux too easily (we just do
> not provide an ansible playbook for that, but it is easy to install, the mac installer could populate the voices from
> the "say" mac command, which does not exist on linux... Not sure if this is still relevant now that we have the EARS
> database audios, but yeah, I think it's not automatic as to copy the EARS audios you have to run the tool by hand from
> zombie-radio repo)...
>
> One question: I have no Windows computer anywhere, but there are many poor souls running that awful OS, do we even
> know if TalkWithMe supports Windows? Do you think any of our features interfere with running TalkWithZombies in Linux
> or Windows?

The label became **"the client: macOS or Linux"** — with the caveat that the client has never run on Linux (§3).

## §2. What the code says (read 2026-10-03)

**Upstream:** TalkWithMe's README lists "Python 3.10+" among its prerequisites and names no operating system; neither
upstream nor this project has ever said Windows works, or tried it.

**The fork's app** (`app/`): no operating-system-specific code — no `subprocess`, no platform checks, no hard-coded
path separators found; its packages are plain Python (FastAPI, uvicorn, httpx, Jinja2, pydantic, PyYAML,
python-multipart, aiofiles — `requirements.txt`). The run folders are named like `2026-10-02T17-27-56`
(`app/show/script.py`: `strftime("%Y-%m-%dT%H-%M-%S")`) — hyphens, not colons, which Windows forbids in file names.

| Part | macOS | Linux | Windows |
|---|---|---|---|
| **The app** (the fork's `app/`) | proven | no OS-specific code; standard Python packages | the same; the run folders' names are legal there |
| **The page** (Web Audio, the microphone) | proven | standard browser features; the OS does not matter | the same |
| **The installer** (`make client-mac`, `deploy/ansible/client-talkwithme-mac.yml`) | proven | **macOS only:** it makes each character's starter voice with `say` and converts it with `afconvert` | the same; and Ansible does not run on Windows as the controlling machine (only through WSL) |
| **The voices** (the EARS clips copied by hand with `tools/voices/cast_voices.py`, screened by `screen_voices.py`) | proven | **both call `afconvert`, macOS only**; `ffmpeg` could replace it | the same |
| **The static bed** | proven | its clips ship with the app (`Sounds/bed/`); the `afconvert` in `tools/sounds/prepare_bed.py` is the maintainers' tool, not the user's | the same |
| **Starting it** | `.venv/bin/uvicorn app.main:app --port 8000` | the same | `.venv\Scripts\uvicorn`; no `make` |
| **The SSH tunnel** | proven | `ssh` | Windows ships OpenSSH; `make ssh-tunnel` would not run, but the `ssh` command it builds would |

## §3. The agent's reading

- **None of our features break Linux or Windows for the app itself.** What ties us to macOS is the tooling around it —
  the installer and the voice tools — both through `afconvert` (and the installer through `say`).
- **Linux:** likely works; never tried.
- **Windows:** plausible; never tried; the setup would be by hand.

## §4. A `make client-linux`? (the owner's idea)

The owner (verbatim, 2026-10-03):

> You are right, we should be able to add a `make client-linux`   and the ansible playbook, to at least install the app
> and yells to the user after the app is cloned that there are manual steps to perform, and list them for the user to
> copy and paste. What do you think?
> Add a Task featured prominently in the TODO near (or inside the Task group for the 3090) to evaluate if the
> `client-linux` route is wise, or in any case, to exercise a manual client install in the 3090 and see how it all works
> together.

**The agent's view: yes, in two steps.**
1. **A manual install on the 3090 first**, every step written down as it happens — the evidence: which steps are the
   Mac's, which differ (the voices: no `say`, no `afconvert`), what breaks.
2. **Then the decision on the playbook, from what step 1 found.** If it is mostly the Mac's playbook without `say`, a
   `client-linux` as the owner describes it — clone, environment, settings, then a printed list of the manual steps to
   copy and paste — is small. If the steps are messy, a written runbook from step 1 may be enough for now.

**What makes the 3090 a rich test:** there, the client and the GPU stack would run on **the same machine**. No tunnel:
the client's settings already point at `localhost:8080`, `:8001`, `:8002`, where the deployed services listen (bound
to loopback). A third way to run the show — beside the cloud box through a tunnel — worth a line in the talk.

**Recorded as:** Task 11 in `docs/TODO.md` — "Goal 4, the 3090": 11.1 the deploy (paused), **11.2 the client on Linux**
(the owner's choice, 2026-10-03: a task group for the 3090).

## §5. Proving it, after the demo (the follow-up)

1. **Linux:** the manual install on the 3090 (Task 11.2).
2. **Windows:** the fork's test suite on a Windows machine borrowed from GitHub — the `windows-latest` runner of GitHub
   Actions, free for public repositories; nobody needs to own a Windows PC.
3. **The voice tools without `afconvert`:** `ffmpeg` in its place (or a choice of the two), so the cast can be made on
   Linux.

Recorded in `docs/follow-ups.md`: "The client on Linux and Windows — proven, and the voice tools without `afconvert`".

## §6. Naming

The owner (verbatim): "Finally: I feel we should have this of OS support saved somewhere in our docs... I lean a new
discussion titled `{date}-client-OS-support.md` (but throw in your names too)." The agent offered
`where-the-client-runs` and `client-platforms`; the owner kept `client-os-support` (lowercased, like every discussion's
file name).
