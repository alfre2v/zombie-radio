# Sound-effect models — live beside the stack, and the best offline — runlog

**Run:** 2026-10-07, about 13:25-15:37 CDT, on the A6000 cloud box — **closed**.
**Timebox:** half a day, the agent's proposal, accepted with the rest of the plan; kept.
**Provenance:** [discussion 2026-10-01] sound-effects — the research (§4.1, the candidates and their licences), the
first design of a listening test (§6.2, never run), the owner's two-part plan of 2026-10-07 (§9);
`docs/follow-ups.md`, "Event sounds as a layer of their own beside the static bed".

## Results

| | Woosh-DFlow | **Stable Audio 3 Small-SFX** | MOSS-SoundEffect v2.0 | Stable Audio 3 Medium |
|---|---|---|---|---|
| Part | 1 (live) | 1 (live) | 2 (offline) | 2 (offline), added |
| Time per take, warm (A6000) | 0.09-0.16 s | **0.42-0.44 s** | 19.5-20.0 s | 0.76-0.84 s |
| GPU memory, the process | 4.0 GB, beside the stack | **2.9 GB, beside the stack** | 18.3 GB, alone | 9.7 GB, beside the stack |
| On a 3090 (24 GB) | fits beside the stack | **fits beside the stack, ~8 GB to spare** | fits alone, ~6 GB to spare | beside the stack ~1.7 GB to spare |
| The voice under constant load | no effect | **no effect** | — (the stack stopped) | 4-5 % slower |
| The owner's ear: good / usable / unusable | 3 / 10 / 17 | **21 / 5 / 4** | 11 / 10 / 9 | 14 / 7 / 9 |
| Sounds with a good take | 1 of 10 | **8 of 10** | 9 of 10 | 8 of 10 |
| Verdict | disqualified (43 % of takes usable) | **passes every live criterion; the model to use** | complements Small on two sequences | set aside (same misses as Small, worse elsewhere) |

- **Live sound generation is feasible** with Stable Audio 3 Small-SFX: 0.44 s a take, 2.9 GB beside the stack, no
  effect on the voice, 87 % of takes usable or good (Entries 8-9).
- **For an offline library**, Small-SFX's good takes cover eight of the ten sounds; MOSS's add the two sequences
  (`thunder-alarms`, `fans-howl`) — together, all ten (Entries 11, 13).
- **The weak prompts are sequences** ("thunder, then alarms"; a rise from silence) — a hypothesis from three prompts.
- **What is generated can ship:** Stability's Community License gives the user the outputs and keeps them outside its
  "Derivative Works"; MOSS's weights are Apache 2.0 (Entry 11).
- **The live criterion was corrected** mid-run: live, nobody picks the take — what counts is the share of takes
  usable, not the best of three (Entry 6).
- **Side lessons:** `uv` does not mix package indexes the way `pip` does (Entry 10); PyTorch 2.9's `torchaudio.save`
  needs FFmpeg on the system (Entry 10); three CUDA builds (12.6, 12.8) ran on the box's 12.4 driver.

## The question

The owner's plan (verbatim, 2026-10-07): "I think the best way to approach this is to open an experiment, for us to
tinker without altering the app." Then, choosing the shape (verbatim):

> Let's divide the experiment in 2 parts:
> (Part 1) We only test models that can run "beside the stack", with "live" as the goal. We test "Small-SFX" and
> "Woosh-DFlow".
>
> (Part 2) We test only one model that would give us the best quality and still be able to run in the 3090 (alone
> and even slow)... This would be for generating the sound effects off the show, and using them as recordings that
> we add to the client, as in the case of the bed audios.
>
> That way we explore the two directions.

The owner's hard requirement (verbatim): "any model has to be able to run well in a RTX3090 and fit in its 24gb of
vram." And on recordings (verbatim): "for this task I do not want to use recordings downloaded from freesound...
That defeats the purpose of exercising a new AI component."

- **Part 1 — live:** can a small model make a usable sound **fast enough, beside the running stack, without hurting
  the voice**, within the 3090's room beside the stack (about 11 GB: the stack measured 12,598 MiB on the 3090)?
- **Part 2 — offline:** what is the **best sound** a model can make on a 3090 **alone** (the stack stopped), however
  slow — sounds generated once, judged, and shipped with the client like the static bed's clips?

Nothing in the show changes in this experiment: no tags in the story, no player in the page, no mixing.

## The models

Weights measured on Hugging Face's file listings, 2026-10-07 (Woosh: from re-uploads, see below).

| Part | Model | By, released | What it is | Weights | Licence | Steps |
|---|---|---|---|---|---|---|
| 1 | **Stable Audio 3 Small-SFX** | Stability AI, 2026-05-20 | diffusion, about 0.6B, made for sound effects; 44.1 kHz stereo, up to 2 min; trained on licensed audio (AudioSparx) and Creative Commons Freesound, screened for copyright | **3.49 GB** (`model.safetensors` 2.27 GB, the T5Gemma text encoder 1.18 GB) | Stability AI Community License (free for non-commercial use); **gated** — the owner accepts the terms on Hugging Face | 8 (the card) |
| 1 | **Woosh-DFlow** | Sony AI, 2026-04 | the distilled ("for speed") text-to-audio model of Sony's sound-effect family; claims parity or better than Stable Audio Open and TangoFlux | about **3.7 GB** for text-to-audio (the model 1.38 GB, the codec Woosh-AE 0.88 GB, the text encoder 1.43 GB — sizes from re-uploads on Hugging Face; Sony ships the weights as GitHub releases of `SonyResearch/woosh-sfx`, not listed here) | weights **CC-BY-NC**; code MIT | per its test script (to read) |
| 2 | **MOSS-SoundEffect v2.0** | OpenMOSS, 2026-05-26 | diffusion transformer with flow matching, 1.3B, a Qwen3 text encoder, a DAC codec; environmental, urban, creature, human-action sounds; 48 kHz, up to 30 s | **11.23 GB** (the transformer 5.66 GB, the text encoder 4.06 GB, the codec 1.49 GB) | **Apache 2.0**, not gated | 100, CFG 4.0, sigma shift 5.0 (the card) |

**Why these** (the discussion of 2026-10-07): Part 1's two are the only candidates small enough (about 3.5 GB each)
to sit beside the stack on the 3090 and built for speed; Stable Audio 3 Medium (10.45 GB) would leave too little room
beside the stack, MOSS (11.23 GB) none. For Part 2 the agent first proposed Stable Audio 3 Medium (the best on
Stability's own test); the owner asked: "Why not "MOSS-SoundEffect v2.0" for Part 2. Isn't the license much better
for us? Is the quality difference so big?" — the difference is unknown (no published comparison of the two), and
MOSS's Apache licence leaves its sounds free to ship in the MIT fork, which Stability's terms may not. MOSS it is.

**Licences of what is generated:** Part 1 ships nothing — a live sound is played at a non-commercial talk, which
both licences cover. Part 2's sounds would ship in the fork, under Apache-licensed weights. **Read on 2026-10-07
(Entry 11):** Stability's Community License gives the user ownership of the outputs and keeps them outside its
"Derivative Works" — Stable Audio's sounds can ship too.

**Left out** ([discussion 2026-10-01] sound-effects §4.1): TangoFlux (research-only licence), MMAudio (mainly
video-to-audio), Stable Audio Open 1.0 (superseded), AudioGen and AudioLDM 2 (16 kHz mono, low fidelity); Stable
Audio 3 Medium (see above); Freesound recordings (the owner's ruling above).

## The ten sounds

The table of [discussion 2026-10-01] sound-effects §6.2, unchanged: each from a real line of the story's
`events.yaml` (quoted) or a radio moment; five under events, two of the dead, three of the radio.

| # | Tag | What it serves (verbatim, or the moment) | Prompt | Length |
|---|---|---|---|---|
| 1 | `glass-rain` | "A fluorescent tube in the main corridor pops, and glass rains onto the floor." | A fluorescent light tube pops overhead and broken glass rains onto a hard corridor floor, indoors, close | 4 s |
| 2 | `sirens-far` | "Far away a siren wails, then another joins it, then another." | Distant emergency sirens wailing across a city at night, one joining after another, heard from far away | 10 s |
| 3 | `helicopter` | "A helicopter drops a crate marked with a red cross onto the lawn." | A helicopter passes low overhead, the rotor thumping, then fades into the distance | 8 s |
| 4 | `fans-howl` | "The server room fans spin up to full speed with a rising howl." | Server room cooling fans spin up from silence to full speed, a rising mechanical howl | 6 s |
| 5 | `thunder-alarms` | "Thunder rolls over the lab, and every alarm in the building answers it." | A deep roll of thunder, then several building alarms ringing at once | 8 s |
| 6 | `tapping-glass` | "A shambler at the front doors is tapping on the glass in a slow rhythm, like Morse code." | Slow tapping of a fingernail on a glass door, a rhythmic pattern, a quiet night | 6 s |
| 7 | `moaning-crowd` | "The moaning outside stops all at once, and the silence is worse." | A crowd of zombies moaning outside a building at night, low and continuous, then sudden silence | 8 s |
| 8 | `radio-static` | the static on the air — the dead air between rounds, and the event "The static on the frequency falls into a rhythm…" | Shortwave radio static, crackle and hiss from an old analogue receiver, steady | 10 s |
| 9 | `receiver-on` | the Repair: the receiver comes back | An old valve radio switched on: a mechanical click, a rising hum, then tuning static | 4 s |
| 10 | `receiver-dies` | the Breakdown: the receiver burns out | An old radio receiver failing: a loud electrical crackle, a fizz, then dead silence | 3 s |

**Takes:** three per model per sound, seeds 1, 2 and 3 — **30 clips per model, 90 in all**. Each take is written as
`<tag>/<model>-<seed>.wav` with a `.json` beside it: the prompt, the seed, the steps, the seconds of audio, the
seconds it took, the peak GPU memory.

## Where it runs

**All on the box** (the owner, 2026-10-07: "Both on the box"; the A6000 on Hyperstack, woken by the owner the same
day). The A6000 is not a 3090: its memory numbers carry over (the requirement is a memory budget), its speeds only
roughly (the 3090 has 82 compute units to the A6000's 84 and faster memory, GDDR6X; the agent's expectation of
similar speeds, not measured).

**Installed by hand over SSH — an exception to the project's rule** that nothing changes on the box outside the
playbook. The agent first planned an opt-in Ansible role (`sfx_lab`); the owner weighed three ways — the agent's
commands over SSH, the owner typing the agent's commands, a playbook written on the fly ("That way we end up with
the installed also... But it adds complexity") — and the agent recommended SSH: installing research code is trial
and error, and a playbook pays off only for what is kept. The owner (verbatim): "Very acceptable. I would even let
you issue sudo commands, but let's beginng with the constrains that you impose and we can relax them later." The
constraints:

1. **Everything in one folder**, `/home/ubuntu/sfx-lab/` — a uv virtual environment per model (their dependencies
   differ: Stable Audio's package, Woosh's `uv sync --extra cuda`, MOSS's `moss_soundeffect_v2` from the MOSS-TTS
   repository), each source pinned to a commit or release; the weights; the scripts; the takes. Cleaning up is
   deleting that folder.
2. **No sudo:** no system packages, no Docker changes, nothing that touches the GPU driver or the stack's services; if
   something needs root, the agent stops and asks.
3. **Every command in the runlog** as it is run, so the install can be repeated — or become an Ansible role, if Part 1
   passes and a live service is built.
4. **Downloads over 1 GB only after the owner approves** the dry run's size.
5. **The stack stops and starts through the Makefile** (`make ans-stop` / `ans-start ENV=cloud`).

The agent reaches the box with plain `ssh ubuntu@<box>` — the owner's own key resolution, never a key path — the
address read from the wired `cloud/hosts.yml`, never written in a file.

**Downloads, each listed by a dry run and approved by the owner before it starts:** about **18.4 GB** in all —
Small-SFX 3.49 GB, Woosh about 3.7 GB, MOSS 11.23 GB; the box's free disk checked first (`df -h`).

**Stable Audio's gate:** the owner accepts Stability's terms on the model's page (only the owner — the agent never
accepts terms), then makes a **fine-grained, read-only Hugging Face token** for this download alone; it is typed at
a prompt on the box, never written in a file, in git or in a log, and revoked after the experiment.

**Running:** the agent runs the generation scripts over SSH and copies the takes back to the laptop, outside both
repositories:
`/Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/sfx-test/`.

## Part 1 — live, beside the stack

The stack **running** (as in a show). For each of Small-SFX and Woosh-DFlow, the 30 takes, and per take:

1. **The time to generate** it, the model already loaded (the first, cold call timed apart).
2. **The peak GPU memory** the model adds beside the stack (`nvidia-smi` sampled while it runs, as in
   `docs/runbooks/box-inspection.md`).
3. **The voice while it generates:** the same voice request timed alone and while a take is being generated (the
   voice's own route through the tunnel, as in [discussion 2026-09-29] voice-datasets-with-emotion §11.15) — the
   question of the 2026-09-30 pushback, "one GPU, three jobs, live".

**The criteria, proposed by the agent — for the owner to confirm or change before any listening:**

| | Proposed pass |
|---|---|
| Speed | a take of the sound's length in **2 s or less** (median, warm): the gap between rounds measured 3.7-4.9 s, so a sound asked for when a round's text arrives would be ready before its line is said |
| Memory | **8 GB or less** added beside the stack — inside the 3090's room of about 11 GB, with margin |
| The voice | its request **no more than 20 % slower** while a take is generated |
| The ear | ~~at least six of the ten sounds usable in at least one of their three takes~~ — **revised in Entry 6:** at least **two in three takes usable or good** (live, nobody picks the take) |

## Part 2 — offline, the best quality

The stack **stopped** (`make ans-stop ENV=cloud`; `make ans-start ENV=cloud` after), MOSS alone on the GPU — the
3090's situation when it generates offline. The 30 takes, each timed, and the peak GPU memory.

**The criteria, proposed:**

| | Proposed pass |
|---|---|
| Fit | peak GPU memory **under 24 GB**, the 3090's whole card |
| Speed | none — "even slow" (the owner) |
| The ear | each sound judged on its own: the takes the owner rates **good** form the first library; a sound with no good take is dropped or re-prompted |

## Judging

A page of players (`listen.html` in this folder; the clips from the datasets folder): the ten sounds as rows, each
model's three takes side by side, the event's line above each row. The owner rates each take **good / usable /
unusable**, by ear, against the criteria written above — not against each other alone.

## What each part decides

- **Part 1 passes** → a live sound service becomes a candidate for after the talk (a server like tts-serve, a role,
  the page's mixing — the 2026-09-30 pushback 2: a big build). **Fails** → live is dropped; the reasons recorded.
- **Part 2 passes** → Part 2 of the owner's plan: the events that would benefit from a sound, stored per event, played
  just before the event's line ([discussion 2026-10-01] sound-effects §9.3). **Fails** → sound effects stay a
  follow-up.

## Open risks

- **MOSS's training data is not stated** anywhere the agent read (2026-10-07): the model card describes the
  architecture and what it generates; the sound-effect README covers installing and fine-tuning; the family's
  technical report (arXiv 2603.18090) is about the speech model; the family's "3 million hours" is the audio
  tokenizer's. Its weights are Apache 2.0; where its training audio came from is unknown — a question for sounds
  played in public and shipped.
- **Woosh's training data** was not checked; its weights are non-commercial (fine for the talk, never shipped).
- **Installs:** Stable Audio's package asks for PyTorch, CUDA 12.6 and Flash Attention 2; MOSS's first call compiles
  for minutes (Triton); Woosh's speed figures are not published — all three measured here.
- **The box is billing** while up; hibernating it again risks the wake (2026-09-24, no A6000 in stock).

## Files in this folder

- `README.md` — this runlog.
- (to come) the generation scripts, one per model; `sample_gpu.sh` (the memory sampling); `listen.html`; `raw/` with
  the takes' `.json` records (the audio stays in the datasets folder, outside git).

## Runlog

Commands are run from the laptop with plain `ssh ubuntu@<box>` and `scp`, the owner's own key resolution (the
live-box drill rules of 2026-09-22: never a key path); the address is read from the wired `cloud/hosts.yml` and never
written down. (Entries 1-5 first ran through a helper that passed the Makefile's key path — a breach of that rule,
caught and corrected before Entry 6.)

### 2026-10-07 — Entry 1: the box, read-only

```bash
df -h / /home
nvidia-smi --query-gpu=name,memory.used,memory.total,driver_version --format=csv,noheader
python3 --version; command -v uv; git --version; nproc; free -g
```

- **Disk:** 55 GB free of 97 GB — room for the weights (about 18.4 GB) and the Python environments.
- **GPU:** the RTX A6000, **14,805 MiB used** of 46,068 MiB by the running stack; driver **550.90.12**, which
  supports **CUDA 12.4**. The models ask for newer CUDA builds (Stable Audio 12.6, MOSS's and Woosh's PyTorch 12.8):
  newer CUDA libraries usually run on a 12.x driver, not always — the first install tells.
- **Python 3.10.12** (the system's), **no `uv`**, git 2.34.1; 28 CPUs, 56 GB of RAM (44 available).

### Entry 2: `uv`, inside `sfx-lab/` only

```bash
mkdir -p ~/sfx-lab/bin
curl -LsSf https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL=$HOME/sfx-lab/bin sh
~/sfx-lab/bin/uv --version   # uv 0.12.23
```

`UV_UNMANAGED_INSTALL` puts the binaries in that folder and changes no shell file (`~/.bashrc` and `~/.profile`
checked: no mention of `sfx-lab`). The folder: 47 MB.

**Woosh's sources, read before installing:** the official weights are GitHub release assets of `SonyResearch/Woosh`
(v1.0.0, 2026-03-16): `Woosh-DFlow.zip` 1.28 GB, `Woosh-AE.zip` 0.82 GB, `TextConditionerA.zip` 1.30 GB (the text
encoder for text-to-audio; `TextConditionerV` is the video one), `Woosh-CLAP.zip` 1.62 GB. Its test script for
DFlow: **4 steps** (`num_steps=4`, `cfg=4.5`), 48 kHz output. Its `pyproject.toml`: Python 3.12 or newer, PyTorch
2.8.0 from PyTorch's CUDA 12.8 index.

### Entry 3: Woosh's environment and weights (the owner: "go ahead with the Woosh downloads")

```bash
cd ~/sfx-lab && git clone https://github.com/SonyResearch/Woosh.git woosh   # commit 7f238bb (2026-09-11), v1.0.1-1
export UV_CACHE_DIR=~/sfx-lab/uv-cache UV_PYTHON_INSTALL_DIR=~/sfx-lab/python
cd woosh && ~/sfx-lab/bin/uv sync --extra cuda   # 130 packages in 14 s; Python 3.12 into sfx-lab/python
.venv/bin/python -c "import torch; ..."           # torch 2.8.0+cu128, CUDA available, a 4096x4096 matmul on the A6000
mkdir -p checkpoints && cd checkpoints
for z in Woosh-DFlow Woosh-AE TextConditionerA; do
  curl -sSfL -o $z.zip https://github.com/SonyResearch/Woosh/releases/download/v1.0.0/$z.zip
  ../.venv/bin/python -m zipfile -e $z.zip . && rm $z.zip
done
for m in Woosh-DFlow Woosh-AE TextConditionerA; do mv checkpoints/$m/weights.safetensors $m/; done; rm -r checkpoints
```

- **The environment: 7.0 GB**, not the 4 GB the agent estimated (PyTorch and NVIDIA's CUDA libraries); disk left 47 GB.
- **CUDA 12.8 runs on the box's 12.4 driver** — the first question of Entry 1, answered.
- **The weights: 3.40 GB** (the zips; 1.38 + 0.88 + 1.43 GB unpacked). The archives hold a `checkpoints/` folder of their
  own, so they unpacked one level too deep; the repository already holds each model's `config.yaml`, identical to the
  archives' — the weights were moved beside them. **DFlow's config names only `TextConditionerA` and `Woosh-AE`**: the
  CLAP model (1.62 GB) is not needed and was not fetched.
- **The codec:** mono, 48 kHz, a hop of 480 samples — **100 latent frames a second**; a sound's length is its frames.

### Entry 4: Woosh-DFlow, the 30 takes, beside the running stack

```bash
cd ~/sfx-lab/woosh
../sample_gpu.sh ../gpu-woosh.csv &               # nvidia-smi, every process, every 200 ms
.venv/bin/python ../gen_woosh.py ../sounds.json ~/sfx-lab/takes
```

(`sounds.json`, `gen_woosh.py`, `sample_gpu.sh` from this folder, copied to `~/sfx-lab/`; the settings Woosh's own test
script uses: 4 steps, renoise [0, 0.5, 0.5, 0.3], cfg 4.5.) A first try, Woosh's test as is: the model loads in about
10.5 s; **0.36 s cold, 0.08 s warm for 5 s of audio**.

- **Speed: 0.09-0.16 s per take, warm** — 0.09 s for 3-4 s of audio, 0.15-0.16 s for 10 s; the first take 0.54 s
  (cold). About 60 times faster than real time.
- **Memory: Woosh's process peaked at 4,002 MiB** (`nvidia-smi`, the CUDA overhead included; PyTorch alone counts 3.50
  GiB), beside the stack's 14.8 GB (llama.cpp 7,036 MiB, the voice 6,868, Whisper 888). On a 3090 (the stack 12,598
  MiB): about 16.6 GB of 24.
- **The takes:** 30 WAVs, 37 MB, copied to
  `/Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/sfx-test/takes/<tag>/woosh-<seed>.wav`, each with its
  `.json`.

### Entry 5: the voice while Woosh generates

`busy_woosh.py` keeps Woosh generating the ten sounds back to back on the box; `time_voice.py` times the same voice
request (Moira's `ref-fear`, a fixed seed) to tts-serve's `/synthesize` through the tunnel, one after another.

| | Median | Range |
|---|---|---|
| Alone, 8 requests | 2.00 s | 1.78-2.37 |
| Woosh generating (498 takes in the minute), 8 requests | 2.02 s | 1.81-3.48 |
| Alone, 12 requests | 1.78 s | 1.69-2.42 |
| Woosh generating (572 takes), 12 requests | 1.80 s | 1.72-1.85 |

**No measurable effect on the voice**, under a load hundreds of times a show's (a show would ask for a sound per
event, about one a minute). The spikes come alone too (2.42 s), so they are the network or the server, not Woosh.

**Woosh-DFlow against Part 1's proposed criteria, before listening:** speed — pass (0.16 s at most, against 2 s);
memory — pass (about 4 GB, against 8 GB); the voice — pass (about 1 % slower, against 20 %). **The ear: next.**

### Entry 6: Woosh-DFlow by ear — disqualified; the live criterion corrected

The owner rated the 30 takes on `listen.html` (verbatim, the page's summary):

```
Woosh-DFlow (Part 1): 3 good, 10 usable, 17 unusable; sounds with a usable take: 7/10
  glass-rain      usable / unusable / usable
  sirens-far      unusable / unusable / unusable
  helicopter      unusable / unusable / usable
  fans-howl       unusable / usable / usable
  thunder-alarms  unusable / unusable / unusable
  tapping-glass   good / good / good
  moaning-crowd   unusable / usable / unusable
  radio-static    usable / usable / usable
  receiver-on     unusable / unusable / unusable
  receiver-dies   usable / unusable / unusable
```

The owner (verbatim): "Now, for the woosh, god that was bad... I guess this disqualifies woosh for any part in our
show... Sad, but now we can move on."

**The numbers and the verdict disagreed, and the criterion was at fault.** By the proposed criterion — six of the ten
sounds with a usable take — Woosh passed (seven). But "a usable take among three" assumes someone picks the best
take, which is Part 2's situation (the owner keeps the good ones). **Live, nobody picks:** the model makes one take
when the event comes, and the audience hears it. What matters live is the **share of takes usable or good**: Woosh's
is **13 in 30, 43 %** — more than half the time the audience would hear an unusable sound. **The Part 1 criterion is
revised to at least two in three takes usable or good**; Part 2's stays (there, the owner picks).

**Woosh-DFlow: disqualified** — it passed on speed (0.09-0.16 s), memory (about 4 GB) and the voice (no slowdown), and
failed on quality. Its only good sound was `tapping-glass` (three good takes of three).

**Not tried, noted for completeness:** the undistilled Woosh-Flow (more steps, maybe better, still fast enough) and
short prompts (Woosh's demo prompt is a short caption; ours are long sentences). The owner moved on.

### Entry 7: Stable Audio 3 Small-SFX — what its README says, the code, the environment

**From Stability's README** (`Stability-AI/stable-audio-3` on GitHub; the model card's files are gated, HTTP 401
without a login): Small-SFX has **433M parameters** (the research's "about 0.6B" counted the text encoder) and its own
small codec, SAME-Small; 44.1 kHz **stereo**, up to 120 s; Stability's table gives **0.41 s for 5 s of sound on an
H200 and 1.69 GB of GPU memory at peak** (0.70 s on a Mac's CPU). **Flash Attention is needed only by Medium**, not
Small. PyTorch 2.7.1 for CUDA 12.6, Python 3.10 or newer; usage: `StableAudioModel.from_pretrained("small-sfx")`,
then `model.generate(prompt=…, duration=…)`.

```bash
cd ~/sfx-lab && git clone https://github.com/Stability-AI/stable-audio-3.git stable-audio-3   # commit 3a82c80 (2026-09-29)
export UV_CACHE_DIR=~/sfx-lab/uv-cache UV_PYTHON_INSTALL_DIR=~/sfx-lab/python
cd stable-audio-3 && ~/sfx-lab/bin/uv sync     # from the repository's pinned uv.lock: 62 packages in 10 s
.venv/bin/python -c "import torch; ..."        # torch 2.7.1+cu126, CUDA available, the matmul on the A6000
```

- **Where the weights come from** (`stable_audio_3/model_configs.py`): `small-sfx` is the Hugging Face repository
  `stabilityai/stable-audio-3-small-sfx` (gated) — `model.safetensors` (2.27 GB) and the T5Gemma text encoder in a
  subfolder (1.18 GB). The code names a separate codec repository, `stabilityai/SAME-S` (not gated), but uses it only
  when no full Stable Audio 3 checkpoint is cached: **the Small-SFX checkpoint contains the codec**, so one gated
  download of 3.49 GB is all.
- **The environment: 5.2 GB** (less than the agent's 6-7 GB estimate); `uv` used the system's Python 3.10.12. Disk:
  39 GB left — 9 GB less, more than the environment, because `uv`'s cache keeps its own copy of the packages.
- **CUDA 12.6 runs on the 12.4 driver**, the second CUDA build to (Woosh's 12.8 was the first).

### Entry 8: Small-SFX — the owner's download, one take, the 30 takes, the voice

**The weights, downloaded by the owner** (the gate accepted, a fine-grained read-only token; in the owner's own SSH
session on the box):

```bash
cd ~/sfx-lab/stable-audio-3 && read -rsp "HF token: " HF_TOKEN && echo && HF_TOKEN="$HF_TOKEN" HF_HOME=~/sfx-lab/hf .venv/bin/hf download stabilityai/stable-audio-3-small-sfx; unset HF_TOKEN
```

`read -s` keeps the token off the screen; the history records the literal `$HF_TOKEN`, never its value; nothing is
written to a file. Checked after: 3.3 GB in `sfx-lab/hf/` (the 3.49 GB, counted in GiB), both weight files; no token
file in either Hugging Face location; no line in the shell history with `hf_` (the prefix of every token). An `xet/`
folder beside `hub/`: Hugging Face's newer download system keeps its chunk cache there.

**`generate()`'s settings** (`stable_audio_3/model.py`): `steps=8` and `cfg_scale=1.0` (no guidance — post-trained not
to need it) by default, a `seed`, a `duration`; `from_pretrained` loads in half precision. Also
`duration_padding_sec=6.0`: every request is computed 6 s longer, then trimmed.

**One take first** (`try_sa3.py`, the helicopter, 8 s, seed 1, three times), with Hugging Face's offline switch:

```bash
cd ~/sfx-lab/stable-audio-3 && HF_HOME=~/sfx-lab/hf HF_HUB_OFFLINE=1 .venv/bin/python ../try_sa3.py
```

- **Loaded offline in 9.0 s** — no network error, so the token was no longer needed (the owner can revoke it).
- `flash_attn not installed, disabling Flash Attention` — expected: Small does not need it.
- **1.07 GiB on the GPU** loaded, **2.13 GiB at peak** (PyTorch's count; Stability's table: 1.69 GB on an H200).
- **0.44 s warm** for 8 s of sound (about 20 steps a second), **1.33 s cold**.
- The output: shape (1, 2, 352,800) — one take, stereo, 8.0 s at 44.1 kHz (the model has no `sample_rate`
  attribute; 44,100 from the README).

**The 30 takes** (`gen_sa3.py`, the card's defaults, offline; the memory sampler alongside, stopped with
`pkill -x nvidia-smi` this time):

```bash
cd ~/sfx-lab/stable-audio-3
(../sample_gpu.sh ../gpu-sa3.csv &)
HF_HOME=~/sfx-lab/hf HF_HUB_OFFLINE=1 .venv/bin/python ../gen_sa3.py ../sounds.json ~/sfx-lab/takes
pkill -x nvidia-smi
```

- **Speed: 0.42-0.44 s per take, whatever the length** — 3 s and 10 s alike (Woosh's grew with length): the cost is
  the 8 fixed steps and the prompt's encoding, and the 6 s of padding makes short sounds cost like long ones. The first
  take 1.31 s (cold). About 3 times slower than Woosh, 4 times inside the 2 s budget.
- **Memory: the process peaked at 2,948 MiB** (Woosh: 4,002), beside the stack's unchanged 14.8 GB. On a 3090: about
  15.6 GB of 24.
- **The takes:** 30 WAVs, stereo, 44.1 kHz, 32-bit float, copied to the datasets folder beside Woosh's (106 MB now).

**The voice** (`busy_sa3.py`, Small-SFX generating back to back for 75 s — 171 takes; `time_voice.py`, 12 requests
each way):

| | Median | Range |
|---|---|---|
| Alone | 1.75 s | 1.71-1.85 |
| Small-SFX generating | 1.75 s | 1.69-1.85 |

**No measurable effect** — against the agent's expectation of a small one (each take keeps the GPU busy about 4 times
longer than Woosh's). The likely reason: the voice model does not fill the A6000's compute — its work is a long chain
of small steps, each waiting on the one before — and a second process fits into the gaps. A 3090, with slightly fewer
compute units, may have a thinner margin; not measured.

**Small-SFX against Part 1's criteria, before listening:** speed — pass (0.44 s); memory — pass (2.9 GB); the voice —
pass (no change). **The ear: next** (the revised criterion: two in three takes usable or good).

### Entry 9: Small-SFX by ear — Part 1 passes; the thunder prompt kept; the dead outside

The owner rated the 30 takes on `listen.html` (verbatim, the page's summary): "It's much better:"

```
Stable Audio 3 Small-SFX (Part 1): 21 good, 5 usable, 4 unusable; sounds with a usable take: 10/10
  glass-rain      good / good / good
  sirens-far      usable / unusable / good
  helicopter      good / good / good
  fans-howl       usable / usable / unusable
  thunder-alarms  unusable / usable / unusable
  tapping-glass   good / good / good
  moaning-crowd   good / good / good
  radio-static    good / good / good
  receiver-on     good / good / good
  receiver-dies   usable / good / good
```

| | Woosh-DFlow | Small-SFX |
|---|---|---|
| good | 3 | 21 |
| usable | 10 | 5 |
| unusable | 17 | 4 |
| usable or good (the live criterion: two in three, 67 %) | 13 / 30, 43 % — fail | **26 / 30, 87 % — pass** |
| sounds with a good take | 1 | 8 of 10 |

**Stable Audio 3 Small-SFX passes Part 1 on all four criteria:** speed (0.44 s), memory (2.9 GB beside the stack),
the voice (no change), the ear (87 % of takes usable or good). Seven sounds are reliable — every take good, or two
good and one usable: glass rain, the helicopter, tapping on glass, the moaning crowd, radio static, the receiver on,
the receiver dying.

**The weak spots share a kind of prompt** (the agent's reading, three prompts — a hypothesis): `thunder-alarms` (one
usable take of three; Woosh's worst too) asks for two events in sequence ("a deep roll of thunder, **then** several
building alarms"); `fans-howl` (a rise from silence to full speed) and `sirens-far` ("one joining after another")
describe a change over time. A few seconds of generated sound handle a texture or a single event well, a sequence
badly. The one sound both models got right, `tapping-glass`, is the simplest prompt: one small sound, repeated, close.

**The thunder prompt stays as written.** The owner (verbatim): "The `thunder-alarms` prompt is just a bad prompt,
however to be impartial we should not change it now." Changed now, MOSS (Part 2) would get a better prompt than the
two models already judged; its scores are the prompt's as much as the models'.

**The dead outside — the owner's idea** (verbatim): "The zombie moan was very good. We need more of this on the show.
It's a show about a zombie appocalipse and we do not hear any zombies in the background... Now we can fix that!"
Recorded in [discussion 2026-10-01] sound-effects §9.5.

**Part 1's verdict: live sound generation is feasible with Small-SFX** — a live service becomes a candidate for after
the talk (still a big build: a server like tts-serve, a role, the page's mixing — the 2026-09-30 pushback 2), now on
measured numbers. For Part 2 the question shifts: Small-SFX already has a good take for eight sounds of ten, so MOSS
must show it is **noticeably better**, and whether its Apache licence matters for shipping the sounds (Stability's
terms on generated audio not yet read).

### Entry 10: MOSS-SoundEffect v2.0 — the install, one take, the 30 takes (the stack stopped)

The owner stopped the stack before the install (`make ans-stop ENV=cloud`; "I can see with nvtop the GPU memory
released"); the GPU read 2 MiB, no process.

```bash
cd ~/sfx-lab && git clone https://github.com/OpenMOSS/MOSS-TTS.git moss-tts   # commit 934d682 (2026-09-06), 12 MB
export UV_CACHE_DIR=~/sfx-lab/uv-cache UV_PYTHON_INSTALL_DIR=~/sfx-lab/python
cd moss-tts/moss_soundeffect_v2 && ~/sfx-lab/bin/uv venv --python 3.12 .venv   # the 3.12 fetched for Woosh, reused
```

**The README's install failed in 0.4 s** — `uv pip install --extra-index-url https://download.pytorch.org/whl/cu128
-e ".[torch-cu128]"`: "there is no version of tqdm==4.67.3". The README is written for `pip`, which merges every index
and takes the best version anywhere; **`uv` uses, for each package, only the first index that has it at all** — a
defence against "dependency confusion" (a fake package under a trusted name on a second index). PyTorch's index also
hosts `tqdm`, not at MOSS's pinned 4.67.3, so `uv` stopped there. Two fixes: `--index-strategy unsafe-best-match`
(behave like `pip`, the protection off for every package), or **split the install** — the agent's choice, the
protection kept:

```bash
# (a) the PyTorch builds alone, from PyTorch's index only (the versions of the torch-cu128 extra in pyproject.toml)
~/sfx-lab/bin/uv pip install --python .venv --index-url https://download.pytorch.org/whl/cu128 \
  torch==2.9.0+cu128 torchaudio==2.9.0+cu128 torchvision==0.24.0+cu128          # 30 packages in 17 s
# (b) MOSS and the rest, from PyPI only; the installed PyTorch satisfies the extra's pins
~/sfx-lab/bin/uv pip install --python .venv -e ".[torch-cu128]"                  # 121 packages
```

(b) replaced numpy 2.5.2 and pillow 12.3.0 (pulled in by PyTorch) with MOSS's pins, numpy 1.26.4 and pillow 12.2.0.
The GPU check: **torch 2.9.0+cu128 on the A6000** — the third CUDA build to run on the 12.4 driver; transformers 4.57.1;
the pipeline imports. **The environment: 7 GB** (`uv`'s cache from 13 to 20 GB).

**A correction to Entry 7:** `uv` hard-links packages from its cache into each environment, so a file exists once on
disk and `du` counts it at the first place it meets it — the environments show as 57 MB and 92 MB, the cache as 13 GB.
The cache does not "keep its own copy"; the 9 GB of Entry 7 were Stable Audio's packages landing in it. And the
Hugging Face `xet/` folder held 772 KB — no second copy of the weights.

```bash
HF_HOME=~/sfx-lab/hf .venv/bin/hf download OpenMOSS-Team/MOSS-SoundEffect-v2.0   # 17 files, 11 GB in 23 s
```

Snapshot `e35df4d`; 17 GB of disk left. **The pipeline's call** (`pipeline_moss_soundeffect.py`): its defaults are the
card's — 100 steps, `cfg_scale=4.0`, `sigma_shift=5.0` — with a `seed` (0 by default), mono by default (`num_channels=1`),
48 kHz; it always denoises a fixed-size latent and crops it to the length asked; it appends `" duration: <X>s"` to every
prompt (its training convention). Guidance 4.0 runs the model twice a step — 200 passes a take, against Small-SFX's 8.

**One take** (`try_moss.py`, the helicopter, seed 1; compiling off, `TORCHDYNAMO_DISABLE=1`, as MOSS's own scripts
do — speed does not matter in Part 2, and the compile takes minutes and may fail):

```bash
TORCHDYNAMO_DISABLE=1 HF_HOME=~/sfx-lab/hf HF_HUB_OFFLINE=1 .venv/bin/python ../../try_moss.py
```

Loaded in 18.1 s, every weight matched (`missing=0, unexpected=0`), **9.88 GiB on the GPU**; **22.4 s cold, 19.4 s
warm** for 8 s of sound (2.4 times slower than real time; about 45 times slower than Small-SFX); 14.51 GiB at peak by
PyTorch's count.

**The 30 takes** (`gen_moss.py`, the card's defaults, in the background):

- **The first run crashed on its first save.** In PyTorch 2.9, `torchaudio.save` writes through a new library,
  TorchCodec, which needs FFmpeg on the system — the box has none (PyTorch 2.8 and 2.7, Woosh's and Stable Audio's,
  still wrote WAVs themselves). The one-take test had not saved a file, so it did not catch it. **Fixed without touching
  the system:** `soundfile`, already among MOSS's dependencies, writes the WAV (`sf.write(…, subtype="FLOAT")`); a
  silent file saved and deleted first, to prove the fix. The owner offered to install FFmpeg ("I can install ffmpeg in
  a second if you need it") — not needed; the agent should have offered the choice instead of deciding alone.
- **The rerun:** loaded in 16.6 s; **19.5-19.96 s per take, flat** — 3 s and 10 s of sound alike — about 10 minutes
  for the 30.
- **Memory: MOSS's process peaked at 18,274 MiB** (`nvidia-smi`; more than PyTorch's 14.5 GiB, because PyTorch keeps a
  reserve it has asked CUDA for and `nvidia-smi` counts it). **Under the 3090's 24 GB, about 6 GB to spare — Part 2's
  fit criterion met.** Beside the stack it would not fit (12.6 + 18.3 > 24) — never Part 2's question.
- **The takes:** 30 WAVs, mono, 48 kHz, 32-bit float, copied beside the others (143 MB in all).

The owner restarted the stack afterwards (`make ans-start ENV=cloud`).

### Entry 11: MOSS by ear; the three compared; the licences of what is generated

The owner rated the 30 takes (verbatim): "MOSS-SoundEffect is a hit-or-miss kind of model."

```
MOSS-SoundEffect v2.0 (Part 2): 11 good, 10 usable, 9 unusable; sounds with a usable take: 10/10
  glass-rain      good / good / good
  sirens-far      unusable / unusable / good
  helicopter      usable / usable / good
  fans-howl       usable / usable / good
  thunder-alarms  good / unusable / usable
  tapping-glass   usable / unusable / unusable
  moaning-crowd   usable / usable / good
  radio-static    unusable / unusable / good
  receiver-on     good / unusable / unusable
  receiver-dies   usable / usable / good
```

| | Woosh-DFlow | Small-SFX | MOSS |
|---|---|---|---|
| good | 3 (10 %) | 21 (70 %) | 11 (37 %) |
| usable | 10 | 5 | 10 |
| unusable | 17 (57 %) | 4 (13 %) | 9 (30 %) |
| usable or good | 13 / 30 | 26 / 30 | 21 / 30 |
| sounds with a good take | 1 | 8 | **9** |
| time per take (A6000) | 0.09-0.16 s | 0.44 s | 19.9 s |
| GPU memory, the process | 4.0 GB | 2.9 GB | 18.3 GB |

**Take by take, Small-SFX is the reliable one** (seven in ten good; MOSS fewer than four). **For Part 2, where the
owner picks, MOSS reaches a good take for nine sounds, Small-SFX for eight — and they miss differently:**

- **MOSS got the two sequences Small-SFX could not:** `thunder-alarms` (a good take, seed 1 — on the prompt the owner
  called bad) and `fans-howl` (the rise from silence). It fits Entry 9's hypothesis that a bigger model handles a sound
  that changes over time better — two sounds, a hint.
- **Small-SFX got the simple sounds MOSS fumbled:** `tapping-glass` (three good against none) and `radio-static`.
- **Together, every one of the ten sounds has a good take.**

**Part 2's verdict: MOSS meets the criteria** (fits a 3090 alone; good takes for nine sounds) — **and Small-SFX nearly
matches it offline too**, 45 times faster. Not yet tested: asking Small-SFX for 10-20 takes a sound and keeping the
best, which might close its gap on sequences.

**The licences of what is generated** — read 2026-10-07:

- **Stable Audio 3** (the weights: the Stability AI Community License; read at `stability.ai/community-license-agreement`,
  "Last Updated: July 5, 2024" — the Hugging Face copy is gated; the GitHub repository's `LICENSE` is the code's, MIT):
  "**Ownership of Outputs.** As between You and Stability AI, You own any outputs generated from the Models or
  Derivative Works to the extent permitted by applicable law." Its "Derivative Works" end "but do not include the output
  of any Model" — so the licence's limits on the model do not follow the sounds. Two strings do: outputs may not be
  used "to create or improve any foundational generative AI model", and their use must follow the law and Stability's
  acceptable-use policy.
- **MOSS:** Apache 2.0 weights; its training data not stated (Open risks).
- **For the fork** (shipped clips must be CC0 or CC BY): picks from either model can be released by us, as CC0 for
  instance. "To the extent permitted by applicable law" is a real caveat — purely machine-made audio may not be
  copyrightable in the US at all. A reading, not legal advice; the copy the owner accepted on Hugging Face may be newer
  than the July 2024 page — its "Ownership of Outputs" clause is worth confirming there.

### Entry 12: Stable Audio 3 Medium — added to Part 2; MOSS's weights deleted; Flash Attention; the 30 takes

**Medium added** — the owner (verbatim): "I feel that if we are doing all this effort, we may as well also do for the
Part 2 the Medium version that you were pushing for before and measure how it compares to Moss." The agent agreed,
and added a reason: Stability's table (5.07-6.49 GB, 0.60 s for 5 s on an H200) made Medium a possible live candidate
too. **Kept:** the owner's Hugging Face token stays active, and everything stays in `sfx-lab/` ("in case we want to
generate more audios later").

**MOSS's weights deleted** — the owner (verbatim): "My lean right now is to delete the Moss model weight, I was
underwhelmed with it." The agent agreed: public, re-downloaded in 23 s if ever needed; its code and environment kept.

```bash
rm -rf ~/sfx-lab/hf/hub/models--OpenMOSS-Team--MOSS-SoundEffect-v2.0   # 27 GB free after
```

**Flash Attention 2, required by Medium** (not by Small). Stability's README points to a pre-built wheel from a
community repository, `mjun0812/flash-attention-prebuild-wheels` (1,760 stars, since 2024-10) — a third-party binary,
approved by the owner ("yes, approved, check the wheel first"). Its file for our environment (CUDA 12.6, PyTorch 2.7,
Python 3.10) — the README's own example — exists in release v0.7.16 (2026-01-28): 185 MB, 2,749 downloads, its SHA-256
published by GitHub. Kept at 2.6.3, the version the README names, over the newer 2.7.4 and 2.8.3.

```bash
W=flash_attn-2.6.3+cu126torch2.7-cp310-cp310-linux_x86_64.whl
cd ~/sfx-lab && curl -sSfL -o "$W" https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/download/v0.7.16/$W
echo "85909aa24df69b530111cde4c878bb866538211911af46c21676ef48437c0307  $W" | sha256sum -c   # OK
cd stable-audio-3 && ~/sfx-lab/bin/uv pip install --python .venv "../$W"                     # 1 package, no others
```

One call on the GPU (`flash_attn_func` on half-precision tensors): the right shape, every value finite, on GPU
capability (8, 6) — Ampere, the 3090's generation too. (A plain `uv sync` would remove it — it is not in the lock file;
`--inexact` keeps it.)

**The weights, downloaded by the owner** (the same hidden-prompt line, `stabilityai/stable-audio-3-medium`): 9.8 GB on
disk (10.45 GB in decimal units); 17 GB free after. **Medium's settings are Small's:** the CLI defaults to 8 steps and
`cfg_scale` 1.0 ("try 7.0 for base models"); the model overview: `small-sfx` and `medium` are the post-trained
checkpoints — an adversarial post-training taught them to work in a few steps without guidance. Small-SFX is a
sound-effect specialist; Medium is general (music and sound effects).

**One take** (`try_sa3.py medium`, beside the running stack — llama.cpp 6,970 MiB, the voice 4,756, Whisper 804; the
voice about 2 GB less than in the morning, freshly restarted): no "flash_attn not installed" line — Flash Attention in
use; loaded in 22.7 s, **4.34 GiB on the GPU**; **0.83 s warm, 2.02 s cold** for 8 s of sound (about 11 steps a
second, Small 20); 8.70 GiB at peak by PyTorch's count — above Stability's 5.07-6.49 GB (H200, long sounds; the
difference not explained).

**The 30 takes** (`gen_sa3.py`, now taking the model's name; Medium's takes saved as `<tag>/sa3m-<seed>.wav`):

```bash
cd ~/sfx-lab/stable-audio-3
(nohup ../sample_gpu.sh ../gpu-sa3m.csv > /dev/null 2>&1 < /dev/null &)
HF_HOME=~/sfx-lab/hf HF_HUB_OFFLINE=1 .venv/bin/python ../gen_sa3.py ../sounds.json ~/sfx-lab/takes medium
pkill -x nvidia-smi
```

- **Speed: 0.76-0.84 s per take, warm** (0.77 s for 3-4 s of sound, 0.82 s for 6-10 s); the first 1.70 s, cold.
- **Memory: the process peaked at 9,716 MiB** beside the stack. On a 3090 (the stack 12,598 MiB): **about 22.3 GB of
  24 — 1.7 GB to spare** (Small left about 8 GB). Against Part 1's proposed criterion (8 GB or less beside the
  stack): **a fail, by 1.7 GB**; Part 2's (under 24 GB alone): a pass.
- **The voice** (`busy_sa3.py … medium`, 96 takes in 80 s; 12 requests each way):

| | Median | Range |
|---|---|---|
| Alone | 1.76 s | 1.68-2.40 |
| Medium generating | 1.84 s | 1.74-2.00 |

  **The experiment's first measurable effect on the voice — about 4-5 %**, inside the 20 % criterion; most requests a
  little higher under Medium (the 2.40 s alone was the first request, a familiar outlier). Medium is the heaviest of
  the four on the GPU's compute, the first that does not fit wholly into the voice model's idle gaps — under a load
  far beyond a show's.

**The ear: next** — the fourth column of `listen.html`.

### Entry 13: Medium by ear — set aside; the experiment closed

The owner rated Medium's 30 takes (verbatim, the page's summary) — "Darn, I know what you are going to say: It does
not replaces Moss, they complement each other... Ok on that observation... My question is: Is it even worth it to use
the medium, or Stable Audio 3 Small is as good as this one?"

```
Stable Audio 3 Medium (Part 2): 14 good, 7 usable, 9 unusable; sounds with a usable take: 9/10
  glass-rain      good / good / usable
  sirens-far      good / unusable / good
  helicopter      good / good / good
  fans-howl       usable / unusable / unusable
  thunder-alarms  unusable / unusable / unusable
  tapping-glass   good / unusable / usable
  moaning-crowd   good / good / unusable
  radio-static    good / usable / good
  receiver-on     good / usable / usable
  receiver-dies   usable / unusable / good
```

**It does not complement Small-SFX — it misses the same two sounds** (`fans-howl`, one usable take; `thunder-alarms`,
none) **and does worse elsewhere:**

| | Small-SFX | Medium |
|---|---|---|
| good | 21 (70 %) | 14 (47 %) |
| unusable | 4 (13 %) | 9 (30 %) |
| sounds with a good take | 8 of 10 | 8 of 10 (the same two missing) |
| time per take | 0.44 s | 0.84 s |
| GPU memory beside the stack | 2.9 GB | 9.7 GB |
| Flash Attention | not needed | needed |

Sound by sound, Medium beats Small only on `sirens-far` (two good takes against one); Small is equal or better on the
other nine (`tapping-glass` three good against one, `moaning-crowd` three against two, `receiver-on` three against
one). The agent's reading: **Small-SFX is a sound-effect specialist, Medium a generalist** (music and sound effects) —
Stability's test scored Medium higher on its own mix, not on ten radio-play effects. **MOSS stays the one model that
complements Small** — on the two sequences only. Three takes a sound, one listener, ten prompts: a clear pattern, not
proof — but it supports the cheap decision. **Medium: set aside.**

**The box, as left** (the owner's ruling: everything kept in `sfx-lab/` "in case we want to generate more audios
later"; the Hugging Face token kept active): `sfx-lab/` holds 39 GB — the three environments (Woosh, Stable Audio,
MOSS), the weights of Woosh, Small-SFX and Medium (MOSS's deleted, Entry 12), the takes; 17 GB of the disk free. The
owner: "We cannot leave the disk so tight" — to be decided.

**The experiment is closed.** The owner's next step, chosen from three: the zombie ambience, the event sounds, or more
Small-SFX takes a sound.

