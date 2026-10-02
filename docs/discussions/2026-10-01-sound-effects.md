# Sound effects — an AI model for the show's sounds: the idea, its history, the research

**Date:** 2026-10-01 (the idea: 2026-09-30) · **Arc:** MVP prototype · **Branch:**
`alfre2v/sound-effects`
**Type:** discussion — the owner's idea of adding an AI model for sound effects;
the project's earlier notes on sound effects; the agent's research into the
open text-to-audio models of 2026, checked at their sources; how a library of
sounds would fit the show; a recommendation.
**Status:** OPEN — **narrowed on 2026-10-01 evening (§8): first the static bed**
(5-15 clips of radio static at low volume, shuffled, the level moving with the
show, random silences, all in settings — the owner's design, §8.8), **from
Freesound**; the folder tree agreed; the
Freesound key in place and checked; nine CC0 candidates listed. **The fetch
tool built** (`tools/sounds/fetch_freesound.py`) and **the owner's 17 Freesound
finds downloaded** (previews, 28 MB, outside git — §8.9), waiting for the
owner's listening. The research on generated and recorded sounds (§4) and the
three-source listening test (§6.2) wait for the broader work: sounds per event.

## §1. The owner's idea (verbatim)

On 2026-09-30, after the voices with emotion were released (`tz-0.4`), asked
what to do next:

> Regarding what to execute next... I am getting a bit greedy here, but I was
> thinking to go beyond just adding radio static mixed in another channel...
> What if... We add a new AI component just for the SFX... I know there are a
> few popular ones that fit in the RAM budget of a 3090, even with the other
> services running, we measure 14gb or RAM used, that leave us a bit for
> experimenting with SFX models.
>
> What is your opinion? Pushbacks?

The agent's answer is in §3. The owner then asked for the presentation
poster first ("Before we do the research: …"), and the discussion was not
saved. On 2026-10-01 (verbatim): "let's start the SFX research. Do you remember
the discussion we where having about SFX? Did we save that somewhere? Is the
discussion still intact in your context?" — it was not saved, and still in the
agent's context, recorded here from it — and, on the plan: "Go ahead with your
proposed plan for the branch and then the research."

During the research the owner added the result of an online search of its own
(kept as the owner gave it; the agent's check of each claim is in §4.2):

> As of September 2026, an RTX 3090 with 24GB of VRAM is an excellent GPU for
> text-to-sound-effect (SFX) and Foley generation. It has enough memory to load
> even the largest open-weight audio models in 16-bit precision while leaving
> room for large batch sizes.
>
> Here are the best open-weight text-to-audio models specifically designed for
> generating environmental sounds and SFX that will run natively on your RTX
> 3090:
>
> ### 1. MOSS-SoundEffect (v2.0)
>
> Released in July 2026 by the OpenMOSS-Team, this is currently one of the most
> capable models for pure sound design.
>
> * **Architecture:** Uses a Diffusion Transformer (DiT) backbone with a DAC VAE
>   vocoder.
> * **Strengths:** Explicitly built for high-fidelity environmental sounds,
>   foley (like high heel footsteps on specific surfaces), and ambient
>   soundscapes. It is highly composable and accurately follows complex text
>   prompts.
> * **RTX 3090 Fit:** The 8B parameter version will consume roughly 16GB of VRAM
>   in FP16, fitting comfortably within your 24GB limit.
>
> ### 2. Stable Audio 3 Small SFX & Stable Audio Open 1.0
>
> Stability AI has released several variations of their audio models, but these
> two are tailored for SFX.
>
> * **Stable Audio 3 Small SFX:** Released in mid-2026, this is a highly
>   optimized 459M parameter (0.6B) latent diffusion model specialized for rapid
>   sound-effect generation and audio-to-audio variation.
> * **Stable Audio Open 1.0:** An older (mid-2024) 1B parameter model optimized
>   for up to 47 seconds of production elements and SFX.
> * **RTX 3090 Fit:** Extremely lightweight. They will use only a fraction of
>   your VRAM, allowing you to generate audio almost instantly or run them
>   concurrently with LLMs.
>
> ### 3. MMAudio
>
> A highly versatile multimodal audio generator that gained traction for its
> joint training approach.
>
> * **Strengths:** While it excels at standard text-to-audio generation for SFX
>   and ambient noise, its standout feature is the ability to generate audio
>   synchronized to a *video* input as well.
> * **RTX 3090 Fit:** Runs easily within 24GB, making it a great choice if you
>   are generating audio to match specific video clips.
>
> ### 4. Meta AudioGen (AudioCraft)
>
> Meta's foundational text-to-sound model, available through the AudioCraft
> repository.
>
> * **Strengths:** Unlike MusicGen (which focuses on melodies), AudioGen was
>   trained exclusively on environmental sounds and SFX (e.g., whistling wind,
>   sirens, footsteps). It is an autoregressive model that produces highly
>   realistic acoustic scenes.
> * **RTX 3090 Fit:** Very efficient and well-supported across many UI wrappers,
>   easily fitting your hardware.
>
> ### 5. AudioLDM 2
>
> A robust latent diffusion model from 2023 that remains a staple in the
> open-source community.
>
> * **Strengths:** Offers excellent zero-shot capability for manipulating sounds
>   based on text. It provides a lot of granular control over compression levels,
>   which allows you to dial in the exact texture of the sound (e.g., the
>   crunchiness of footsteps).
> * **RTX 3090 Fit:** Lightweight and broadly integrated into user interfaces
>   like ComfyUI or Gradio web interfaces.
>
> **Recommendation:** If you want the absolute highest fidelity and texture
> detail for a prompt like *"the sound of steps of a woman in high heels,"*
> start with **MOSS-SoundEffect**. If you need rapid iteration and extreme
> speed, use **Stable Audio 3 Small SFX**.

## §2. The history: sound effects in the project before this

- **2026-09-13, the product's brainstorm**
  (`docs/discussions/2026-09-13-product-definition-brainstorm.md`):
  - **§6, "Beyond recognition: sound-effects generation (feature target)"** —
    "open models specialized in generating *sound effects* from text
    descriptions … For a radio drama this is atmosphere gold: doors, zombies
    pounding, static, lab equipment." Leads then (unverified): AudioGen,
    AudioLDM 2, Stable Audio Open. "Likely out of scope for the Oct 8 MVP;
    pre-generating a small library of effects offline (rather than live
    generation) would be the cheap version. **Status: identified feature
    target, parked; revisit after the MVP ships or if the schedule opens up.**"
  - **C8, "Audio mixing — many sources, one radio stream"**, and the owner's
    pushback of that day: streaming several audio streams is wasteful. The
    design that survived: "only the *voice* track streams; sound effects and
    ambience are mostly **static assets shipped once** at page load and
    triggered client-side by tiny control events ("play static loop", "duck
    under voice") — near-zero extra bandwidth, and the browser decodes
    compressed audio natively".
- **The spec** (`docs/specs/product-definition.md` §2.2): "generated sound
  effects and live audio mixing" are out of the first release.
- **The dead-air static** — the TODO's polish item since 2026-09-28: a soft
  radio hiss generated in the browser while a round is generated, off while
  the page listens (so Whisper does not hear it), kept apart from the looks'
  gauge (which taps every sound of the page's audio context).
- **2026-09-28, the narration challenges, C11**
  (`docs/discussions/2026-09-28-narration-quality-challenges.md`): the model
  wrote sound effects as starred words (`*crackle*`) and the voice read them as
  words; "the sound effects open". **Checked 2026-10-01** — the owner: "I have
  not seen that behavior recently, so maybe it was cured by some of the prompt
  massaging we did after." The records agree: in every recorded run of the
  fork's `runs/` from 2026-09-25 to 2026-10-01, the only starred sounds are five
  `*crackle*` in one run, `2026-09-27T00-34-00`, before the calls became fixed
  lines; since then every starred word is emphasis ("now", "please", "fast") —
  across runs of 400-500 model lines. Cured by the fixed calls, which C11 named
  as "the main source".

## §3. The agent's answer of 2026-09-30

**Why it fits:** events read aloud on air would land harder with a sound under
them (a helicopter's rotor under "A helicopter drops a crate…"); the story has
289 events filed by overtone and theme; it is another "AI behind the curtain"
for the talk (a highlight the owner chose, [discussion 2026-09-30] demo-goals
§6); and a 24 GB 3090 has about 10 GB beside the stack's 14 GB.

**The pushbacks:**

1. **One GPU, three jobs, live.** The language model, the voice and an SFX
   model on one card: generating a sound takes seconds, and it would compete
   with the voice for the GPU between rounds — the dead air the static was meant
   to hide.
2. **A new live service is a big build:** no server like tts-serve exists for it
   — a wrapper, a Docker image, an Ansible role, a memory check, deploy proofs
   on both targets, the page mixing a second stream: two to four days (the
   agent's guess), against one to two hours for the static.
3. **The order of risk:** the 3090 (goal 4) had never run; a new service would
   land on it before it was proven, and the headroom was measured on an A4000.
4. **Curation is the boring work the owner had just set aside:** sound models
   are uneven; someone listens and picks — the same kind of "find and clean the
   samples" work the owner had postponed for the voices.

**The recommendation:** generate the sounds **offline**, once, before the demo —
a sound or two per kind of event, and a few ambiences — listen, keep the good
ones, store them as a small library; in the show, the page plays the right one
under the line. No new runtime service, no competition for the GPU, no added
latency, no deployment change; it absorbs the static; a live service could come
after the demo if the library proves its worth. The first step: this research.
The same shape as the brainstorm's "cheap version" and the owner's C8 design of
2026-09-13.

## §4. The research (2026-10-01): open text-to-audio models for sound effects

### §4.1 The candidates, checked at their sources

| Model | By, released | Size | Output | Length | Licence of the weights | Memory, speed | Notes |
|---|---|---|---|---|---|---|---|
| **Stable Audio 3 Small-SFX** | Stability AI, 2026-05-20 | 459M (diffusion) + 108M (codec) ≈ 0.6B; text encoder T5Gemma | 44.1 kHz stereo | up to 2 min | Stability AI Community License (free for research, non-commercial, and organisations under US$1M a year); **gated** — the terms must be accepted on Hugging Face; T5Gemma under Gemma's terms | 8 steps, no guidance needed; 0.44 s for up to 2 min on an H200; "a few seconds" on a MacBook Pro M4 (runs without a GPU) | Made for sound effects; trained on licensed audio (AudioSparx) and Creative Commons Freesound, screened for copyright. 5-second SFX: FAD 0.395, CLAP 0.351, quality 3.35 — better than Stable Audio Open Small (FAD 0.500) and TangoFlux (0.760) on the paper's tests; "noticeably worse" than Medium |
| **Stable Audio 3 Medium** | Stability AI, 2026-05-20 | 1.4B | 44.1 kHz stereo | up to 380 s | the same Community License | about 6.5 GB at 120 s (a review); under 2 s on an H200 | Music and sound effects; the best of the open Stable Audio 3 models on the SFX test (FAD 0.369, CLAP 0.369, quality 3.65) |
| **MOSS-SoundEffect v2.0** | OpenMOSS, 2026-05-26 | 1.3B (diffusion transformer, flow matching; DAC codec; Qwen3 text encoder) | 48 kHz | up to 30 s | **Apache 2.0** | not stated; bfloat16; the first call compiles for minutes; 100 steps recommended | Environmental, urban, creature and human-action sounds; English and Chinese prompts; duration controllable. (Its v1, February 2026, was an 8B model of another architecture.) |
| **Woosh** (Flow, DFlow distilled) | Sony AI, 2026-04 | not stated | not stated | not stated | CC-BY-NC | not stated | A sound-effects foundation model: text-to-audio and video-to-audio, distilled versions for speed; claims parity or better than Stable Audio Open and TangoFlux |
| **TangoFlux** | DeCLaRe Lab, 2024-12 | 515M | 44.1 kHz stereo | up to 30 s | **non-commercial research only** (Stability AI Community License, Stable Audio Open's and WavCaps's terms) | 30 s in 3.7 s on an A40 | Fast and faithful in its paper; behind Stable Audio 3 Small-SFX on Stability's test |
| **MMAudio** | 2024-12 (CVPR 2025) | not stated | 44.1 kHz (or 16 kHz versions) | 8 s (trained) | CC-BY-NC 4.0 | about 6 GB at 16-bit | Mainly video-to-audio; text-to-audio by omitting the video; known faults: unintelligible speech, unwanted music |
| **AudioGen** (AudioCraft) | Meta, 2023 | 1.5B (medium; the agent's memory, not re-checked) | 16 kHz mono | about 5-10 s | CC-BY-NC 4.0 (code MIT) | — | Environmental sounds only; autoregressive; low fidelity by today's standard |
| **AudioLDM 2** | 2023 | — | 16 kHz mono (a 48 kHz variant) | — | (not checked) | — | A staple of 2023; superseded |
| **Stable Audio Open 1.0** | Stability AI, 2024 | about 1.2B (the agent's memory, not re-checked) | 44.1 kHz stereo | up to 47 s | Community License | 8 steps/s on an RTX 3090 | Superseded by Stable Audio 3 |

### §4.2 The owner's search, checked

- **MOSS-SoundEffect v2.0, "8B, roughly 16 GB":** the model card and the
  README say v2.0 is **1.3B**, released **2026-05-26** (the search said July);
  the **8B** model is **v1** (February 2026, `MossTTSDelay`). The search joined
  v1's size to v2.0's architecture. It matters for the box: 16 GB beside the
  stack's 14.5 GB would not fit a 24 GB card at once; 1.3B would.
- **"Run them concurrently with LLMs":** true of the small models' memory, but
  it is the 2026-09-30 pushback 1 — on one GPU, a live sound model competes with
  the voice between rounds. Offline generation avoids it (§5).
- **Stable Audio 3 Small-SFX (459M, 0.6B), Stable Audio Open 1.0, AudioGen,
  AudioLDM 2, MMAudio:** consistent with their sources (MMAudio checked: mostly
  video-to-audio, 8 s, CC-BY-NC).

### §4.3 What decides the choice for us

- **Licence:** the project is non-commercial — a talk at a meetup — and
  already runs on non-commercial assets (the EARS voices, CC BY-NC 4.0), so
  CC-BY-NC weights are acceptable; Apache 2.0 is the cleanest. A **gated**
  model (Stable Audio 3) needs the owner to accept its terms on Hugging Face —
  the agent must not accept terms on the owner's behalf.
- **The training data:** Stable Audio 3 is trained on licensed and Creative
  Commons audio, screened for copyright — the safest for sounds played in a
  public talk. MOSS-SoundEffect's training data is not stated in what the agent
  read.
- **Fidelity:** a radio play through a laptop's speakers or a room's PA does
  not need 48 kHz; 44.1 kHz stereo is plenty, and the show's voices are 24 kHz
  mono. 16 kHz mono (AudioGen) would sound thin next to them.
- **Speed and memory:** for an offline library, generation time hardly
  matters; every candidate fits the A6000 (and a 3090) beside the stack.

### §4.4 Recorded sounds instead: datasets and libraries (the owner's aside)

The owner (verbatim, 2026-10-01): "As another aside relevant to the task of
providing SFX: If we decide not to generate the SFX audios live, but pre-record
them, maybe besides resarching AI models for SFX, we should also research open
source or generous license research datasets of ambient sounds and SFX. Id such
a thing exists." They exist — real recordings, the radio play's traditional
material:

| Source | What | Licence (as published) | Redistribute the raw files? | Access |
|---|---|---|---|---|
| **Freesound** (freesound.org) | the largest open library of sound effects and field recordings, searchable by text and tags | **per sound**: CC0, CC-BY or CC-BY-NC — chosen by each uploader | CC0 and CC-BY yes (CC-BY with credit); CC-BY-NC for non-commercial use | a free account; an API (APIv2) that searches and **filters by licence**; the original files need OAuth2 (the owner's account), the previews do not |
| **FSD50K** | 51k Freesound clips, over 100 h, human-labelled in 200 sound classes (the AudioSet ontology) | the dataset CC-BY; each clip its own CC licence — **84.7 % CC0 or CC-BY** | per clip, as on Freesound | Zenodo, Hugging Face — a research dataset (classes, not curated effects) |
| **Sonniss GDC Game Audio Bundles** | professional sound effects, a bundle a year (2026: 7.47 GB, 347 WAV files; the archive of earlier years over 200 GB) | **royalty-free, commercial use, no attribution**, "for media production (games, film, TV, interactive projects)"; **AI/ML training prohibited** | not as raw files (the licence is for use in productions) | a free download |
| **BBC Sound Effects** | over 33,000 effects from the BBC's archive, WAV and MP3 | **RemArc licence**: personal, educational or research use only, non-commercial; formal education for students and staff | no | a free download per sound; individual sounds purchasable for other uses |
| **Pixabay sound effects** | a stock library of short effects | the Pixabay Content License: free, commercial use, no attribution | **no** — "don't resell or redistribute sounds as-is" | a free download per sound |
| **The Internet Archive** | old-time radio shows and wartime recordings, some with period static and effects | "public domain" as each uploader states it — **to verify per item** | per item | free; uneven, uncatalogued for effects |

**What it changes:**

- **The licence decides where a clip may live.** The fork's repository is
  public: a clip committed there is redistributed as a raw file. Only CC0 and
  CC-BY clips (Freesound, FSD50K) allow that (CC-BY with credit, as the old
  radio photograph is credited). Sonniss, BBC and Pixabay clips — and any clip
  under a licence that forbids it — would live **outside git**, installed on the
  laptop like the cast's voices (`~/TalkWithZombies-client/…`, never committed),
  or not be used. Generated sounds avoid the question if the model's licence
  gives the outputs to the user (the agent believes Stable Audio's Community
  License and Apache 2.0 do — **to verify** before relying on it).
- **The BBC's licence is the doubtful one** for a talk at a meetup: personal or
  research use, or "formal education" for students and staff — a public talk is
  none of these clearly. The agent would not rely on it without the owner's
  reading of the terms.
- **Real recordings beat generated ones for well-defined sounds** — a door, a
  switch, glass, radio static, wind, a generator — and Freesound has most of
  them under CC0. A model earns its place for what is hard to record or find:
  a horde of the dead at a fence, a specimen tank cracking, the lab's own
  machines.
- **The API makes Freesound tool-friendly:** a script in `tools/` could search
  per tag, filter to CC0 (or CC0 and CC-BY), and write a page of players with
  the candidates — the same review as for generated takes (§5).

## §5. How a library would fit the show

**What the sounds would be:**

1. **Under the events** — the director reads an event aloud as a fixed line
   (spec §6.5); a sound under (or just before) that line. The story has **289
   events**, plain sentences in 35 theme groups by overtone
   (`stories/lab-outbreak/events.yaml`: e.g. "The dead outside" 24, "The radio
   itself" 19, "The building" 20 among the negative), **without ids**. Many
   cannot be heard ("A convoy of survivors on the radio says they have fuel to
   share"), so the library hangs on **sound tags**, not on every event: each
   event optionally names a tag (`pounding`, `rotor`, `glass`, `generator`,
   `howl`…), and the library holds a few takes per tag — on the order of 30-50
   tags, 2-3 takes each (the agent's estimate, to settle by reading the events).
2. **Ambience beds** — a quiet loop per overtone (a positive, a neutral, a
   negative bed), under the whole round.
3. **The radio itself** — the dead-air static while a round is generated (the
   polish item, absorbed), the receiver's switch on and off, the burn-out of the
   Breakdown, a tuning sweep at the call.

**Where each piece lives** (the owner's C8 design of 2026-09-13):

- **The clips** — static assets beside the story (e.g.
  `stories/lab-outbreak/sounds/<tag>-<n>.ogg`, compressed: Ogg/Opus or MP3, which
  the browser decodes natively), loaded by the page once; the tags in
  `events.yaml` and the beds in `overtones.yaml` (data where it is central, the
  owner's preference — like the voices' map).
- **The trigger** — the server already tells the page each line as it streams;
  the fixed line that reads an event could carry the event's tag (as the
  stream's `start` event carries the mood), and the round's summary carries its
  overtone; the page plays the clip.
- **The mixing** — the page's Web Audio context: a second source per sound,
  its gain under the voice ("duck under voice"), **silent while the page
  listens** (Whisper must not hear it), and kept apart from the looks' gauge,
  which taps every sound of the context (or deliberately included, if the
  needle should move with the sounds).
- **The generation** — a script in this repository's `tools/` (like the voice
  tools): prompts per tag, N takes each, written to a datasets-like folder
  outside git, a **page of players** to pick from (the owner's favourite way to
  review), the chosen takes converted and copied into the story's folder. Run
  on the box (or the 3090) with the stack up — the small models need a few GB —
  or on the laptop's CPU (Stable Audio 3 Small-SFX runs without a GPU).

## §6. The agent's judgment and recommendation

### §6.1 Judgment

The idea is a good fit **as an offline library**, and the research makes it
cheaper than on 2026-09-30: a model made for sound effects (Stable Audio 3
Small-SFX) appeared in May 2026 — 0.6B, 8 steps, a laptop's CPU is enough —
with licensed training data; and an Apache-licensed alternative (MOSS-SoundEffect
v2.0, 1.3B, 48 kHz). The pushbacks of §3 still hold for a **live** service and
are avoided by the library. What remains is curation — someone listens and picks
— bounded by keeping the library small (tags, not events) and reviewing on a
page of players.

**Rough cost** (the agent's estimate): the listening test half a day; the
generation tool and the library one day; the show's side (tags in the story,
the page's player, ducking, silence while listening, the gauge) one to two days.
Against the deadline (2026-10-08) and the board's other items — the 3090 (goal
4), names-only A, Task 7 (the canned episode, a MUST), Task 9 (the talk) — the
library is the one most likely to slip; the static alone (one to two hours)
remains the fallback.

### §6.2 Recommendation: a listening test before any build

The test is an experiment in the project's sense (the TODO's guardrail 1: a
question, a timebox, the pick criteria written down before listening, a
runlog), in its own folder,
`docs/experiments/2026-10-0N-sfx-listening-test/`. It answers one question,
listens to ten sounds from three sources, and ends with a decision. Nothing of
the show is touched.

#### The question

For the show's sounds — under the events, the dead outside, and the radio
itself — **which source gives usable sounds: Stable Audio 3 Small-SFX
(generated), MOSS-SoundEffect v2.0 (generated), or Freesound's CC0 recordings?
And is a curated library worth building before the demo, or only the static?**

Not in this test: generating sounds live; anything in the show (the tags, the
page, the mixing); Stable Audio 3 Medium (only in a second round, if Small-SFX
sounds thin); the models of §4.1 left out (TangoFlux: research only; Woosh,
MMAudio, AudioGen, AudioLDM 2, Stable Audio Open: older, narrower or weaker).

#### The ten sounds

Each comes from a real line of the story's `events.yaml` (quoted), or from the
radio's own moments; the prompt is what the models get, the search what
Freesound gets, the length what each clip should last. Five sounds under
events, two of the dead, three of the radio — the three kinds of §5.

| # | Tag | What it serves (verbatim, or the moment) | Prompt for the models | Freesound search | Length |
|---|---|---|---|---|---|
| 1 | `glass-rain` | "A fluorescent tube in the main corridor pops, and glass rains onto the floor." | A fluorescent light tube pops overhead and broken glass rains onto a hard corridor floor, indoors, close | `fluorescent tube pop glass break` | 4 s |
| 2 | `sirens-far` | "Far away a siren wails, then another joins it, then another." | Distant emergency sirens wailing across a city at night, one joining after another, heard from far away | `distant sirens city night` | 10 s |
| 3 | `helicopter` | "A helicopter drops a crate marked with a red cross onto the lawn." | A helicopter passes low overhead, the rotor thumping, then fades into the distance | `helicopter flyby` | 8 s |
| 4 | `fans-howl` | "The server room fans spin up to full speed with a rising howl." | Server room cooling fans spin up from silence to full speed, a rising mechanical howl | `server fans spin up` | 6 s |
| 5 | `thunder-alarms` | "Thunder rolls over the lab, and every alarm in the building answers it." | A deep roll of thunder, then several building alarms ringing at once | `thunder` (and `building alarm` — two clips) | 8 s |
| 6 | `tapping-glass` | "A shambler at the front doors is tapping on the glass in a slow rhythm, like Morse code." | Slow tapping of a fingernail on a glass door, a rhythmic pattern, a quiet night | `tapping on glass` | 6 s |
| 7 | `moaning-crowd` | "The moaning outside stops all at once, and the silence is worse." | A crowd of zombies moaning outside a building at night, low and continuous, then sudden silence | `zombie horde moan` | 8 s |
| 8 | `radio-static` | the static on the air — the dead air between rounds, and the event "The static on the frequency falls into a rhythm…" | Shortwave radio static, crackle and hiss from an old analogue receiver, steady | `shortwave radio static` | 10 s, loopable |
| 9 | `receiver-on` | the Repair: the receiver comes back | An old valve radio switched on: a mechanical click, a rising hum, then tuning static | `old radio turn on` | 4 s |
| 10 | `receiver-dies` | the Breakdown: the receiver burns out | An old radio receiver failing: a loud electrical crackle, a fizz, then dead silence | `electrical short circuit spark` | 3 s |

**Takes:** three per model per sound — seeds 1, 2 and 3 — and Freesound's three
best CC0 matches per search (sorted by rating, 1 to 15 seconds long): 30 clips
per source, **90 in all**.

#### Where each source runs, and how

**A. Stable Audio 3 Small-SFX — on the laptop** (an Apple M1 Pro, 16 GB).
It runs without a GPU, so the gated model and the owner's Hugging Face login
stay on the laptop and never touch the box.

1. The owner accepts the licence and logs in (§6.3, steps 1-2).
2. The agent installs the model's package (`stable-audio-3`, Stability AI's
   repository; the exact install for a Mac checked then — the README asks for
   PyTorch, CUDA 12.6 and Flash Attention 2 on a GPU, and the paper says the
   small models run on a MacBook) in a virtual environment **outside both
   repositories**, in `zombie-radio-datasets/sfx-test/.venv`.
3. A dry run lists the download: **3.49 GB** (`model.safetensors` 2.27 GB,
   T5Gemma 1.18 GB — measured on Hugging Face's listing, 2026-10-01); the owner
   approves it.
4. The agent's script (in the experiment folder) generates each take with the
   card's settings — `StableAudioModel.from_pretrained("small-sfx")`, **8
   steps**, the table's length — and writes `<tag>/sa3-<seed>.wav` (44.1 kHz
   stereo) with a `.json` beside it (the prompt, the seed, the steps, the
   seconds of audio, the seconds it took).
5. The first take is timed: the paper's "a few seconds on a MacBook Pro M4" is
   not an M1 Pro; if one take takes more than about a minute, the rest move to
   the box (step B's role, with the owner's Hugging Face token there — the
   owner's call).

**B. MOSS-SoundEffect v2.0 — on the box.** It needs CUDA (bfloat16, and a
first call that compiles for minutes with Triton). **Nothing changes on the box
outside the playbook** (the project's rule), so:

1. A small Ansible role, `sfx_lab`, opt-in — **not** part of `site.yml`'s
   normal run; its own playbook, `deploy/ansible/sfx-lab.yml`: a uv virtual
   environment in `/home/ubuntu/sfx-lab`, the `moss_soundeffect_v2` package
   from the MOSS-TTS repository pinned to a commit, the model cached in the
   same models folder as the LLM (`zr_models_dir`), the generation script
   copied in. A `state: absent` run removes it all after the test.
2. A dry run lists the download: **11.23 GB** (the transformer 5.66 GB, the
   Qwen3 text encoder 4.06 GB in two files, the 48 kHz codec 1.49 GB); the
   model is **not gated** — no token on the box. The owner approves, then runs
   the playbook (deploys are the owner's).
3. The agent runs the script over SSH (`ssh ubuntu@<box> '…'`, the address the
   owner gives), with the card's settings — **100 steps, CFG 4.0, sigma shift
   5.0**, the table's length, seeds 1-3 — and copies the 30 takes back
   (`<tag>/moss-<seed>.wav`, 48 kHz, and the `.json`).
4. Memory, measured while it runs (`nvidia-smi`, as in
   `docs/runbooks/box-inspection.md`): about 6-8 GB in bfloat16 is the agent's
   estimate beside the stack's 14.5 GB — fine on the A6000, and the number that
   says whether the 3090 could do it too.

**C. Freesound — on the laptop.**

1. The owner opens a Freesound account and asks for an API key (§6.3,
   step 3), and sets it in the shell — `export FREESOUND_API_KEY=…` — never in a
   file in git.
2. The agent's script searches each sound's query through the API (the text
   search, filtered to the CC0 licence and to 1-15 seconds, sorted by rating;
   the exact filter syntax checked against the API's documentation then) and
   downloads the **previews** (MP3), which need no OAuth — enough to judge; the
   original file only for the clips finally chosen.
3. Each clip is written as `<tag>/fs-<n>.mp3` with a `.json`: its Freesound id
   and page, its author, its licence, its length, its rating.

#### Making the takes comparable

- **The same loudness**: every clip normalised as the casting normalises the
  voices (RMS -20 dBFS, the peak under -1 dBFS) — otherwise the louder clip
  wins.
- **The same length**: trimmed to the table's length (a Freesound clip may run
  long).
- **The same format on the page**: converted to WAV 44.1 kHz stereo for
  listening; the originals kept beside them.
- **Outside git**: everything in
  `/Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/sfx-test/`, one
  folder per tag; the experiment folder keeps the scripts, the `.json`
  records and the results, not the audio.

#### The page of players

`sfx-test/index.html`, the kind of page the owner reviewed the voices with:
one row per sound — the event's text and the prompt — then three groups of
three players, one group per source, each player with its details (the seed and
the generation time; or the Freesound link, author and licence). A **blind
switch** hides the sources and shuffles them within each row, so the owner
judges the sound, not the source; switched off, it shows them.

#### How the owner judges — the criteria, written before listening

For each sound: the **best take of all**, and, for each source's best take, a
score from 1 to 5 on

1. **the event** — does it sound like what the line says?
2. **real** — does it sound like a real sound, not a synthetic one?
3. **the radio** — would it work under a voice on an old broadcast?
4. **clean** — free of faults (clicks, a cut-off, music or speech that should
   not be there)?

The owner gives the picks and scores in the chat (or the page collects them
and prints them to copy); the agent records them in the experiment's findings.

**The decision, fixed in advance:**

- A source that gives the best take in **at least 6 of the 10** sounds is the
  library's main source; another fills its gaps.
- A sound is **usable** if its best take scores at least 3 on "real" and "the
  radio". If **fewer than 7 of the 10** are usable from any source, the library
  waits until after the demo, and the show gets only the static (§2).
- If the generated sounds win only where Freesound had no good CC0 match, the
  library is mostly recorded — fewer licence questions (§4.4) — with generated
  sounds for the rest.

#### Timebox and cost

- **The agent:** about 3-4 hours — the three scripts, the role, the
  normalising, the page, the findings.
- **The owner:** the three steps of §6.3 (about 15 minutes), the playbook run,
  and the listening (about 30-45 minutes for 90 clips).
- **The box:** 30 MOSS generations (time unknown until the first is measured:
  100 steps, and a first compile of minutes); the 11.23 GB download.
- **The laptop:** 30 Stable Audio generations (timed on the first); the
  3.49 GB download; 30 Freesound previews (small).

#### After the test

- **The library goes ahead** (before the demo, if the board allows): the
  generation and fetching tools move into this repository's `tools/sfx/` (like
  `tools/voices/`), a tag per event where one fits in `events.yaml`, a bed per
  overtone in `overtones.yaml`, the radio's sounds; the show's side in the fork
  (the tag carried by the event's fixed line, the page's player, the ducking
  under the voice, silence while the page listens, the gauge); each clip stored
  where its licence allows (§4.4). Estimated in §6.1.
- **Or it waits:** this discussion records the result; the show gets the
  dead-air static only (the TODO's polish item, one to two hours).
- **Either way:** `sfx_lab` is removed from the box (`state: absent`); the
  downloads stay in `zombie-radio-datasets/` until the owner deletes them.

### §6.3 What the owner does first, step by step

1. **Accept Stable Audio 3's licence.** On
   <https://huggingface.co/stabilityai/stable-audio-3-small-sfx>, logged in to
   Hugging Face: read the Stability AI Community License (and the Gemma terms of
   the bundled text encoder) and accept. The repository is gated "auto": access
   is granted at once. The agent must not accept terms on the owner's behalf.
2. **Log the laptop in to Hugging Face** — in a terminal, `hf auth login` (or
   the older `huggingface-cli login`) with a **read** token from
   <https://huggingface.co/settings/tokens>. The token stays in the owner's
   Hugging Face settings on the laptop; the agent never sees or handles it.
3. **Open a Freesound account and ask for an API key** — at
   <https://freesound.org>, then the API credentials page in the account's
   settings (believed to be <https://freesound.org/apiv2/apply/> — to check);
   then, in the terminal the agent's scripts run in,
   `export FREESOUND_API_KEY=<the key>`. The agent must not create the account.
4. **Approve the downloads** — the laptop's 3.49 GB (Stable Audio 3
   Small-SFX), the box's 11.23 GB (MOSS-SoundEffect v2.0) — after the agent's
   dry run shows them, with their sources and licences.
5. **Approve the `sfx_lab` role and run its playbook** on the box (or decide to
   leave MOSS-SoundEffect out of the test: then two sources, and no change on
   the box).
6. **Listen and score** (§6.2's page and criteria).

## §8. Addendum, 2026-10-01, evening — narrowed to background radio sound; Freesound first; the folder tree

**This addendum overrides §6.2-§6.3 for now:** the three-source listening test
is set aside, not cancelled — it returns when the work broadens to sounds for
the events.

### §8.1 The owner's narrowing (verbatim)

On the full test of §6.2: "This is a too ambitious plan to advance in so many
fronts at the same time... I want to explore first the downloading of a limited
number of audios from freesound."

Then, on what to build first:

> Wait. Before we initiate the download, lets agree in a proper folder tree to
> organize our audios, I propose something akin to what we did with the EARS
> (divide by dataset name, or AI model at top level), then subfolders by type of
> sounds, then the audiofiles themselves with a small metadata file for
> attribution and other metadata we need to save.
> Feel free to add your improvements in this organization schema.
>
> I am thinking that instead of trying to tackle at once all types of sounds your
> proposed, let's start by trying to deliver just static and audio sounds playing
> in the background... this idea was multiple times surfaced appart from the more
> general SFX one, and to solve it we still need to download a few audios (as we
> cannot just play a small clip in repeat, it would be too boring, and I have
> found myself a few radio sounds in freesound that I would like to use, we can
> play a list of audio files related to radio static and radio sounds in the
> background)... This will give us plenty to be busy already as we have to solve
> the problem of mixing the 2 sources of audio (our TTS voices with the SFX
> sounds, in this case only radio static)... When we manage to make this work we
> can get ambitious and broaden the type of audios, and maybe assign a list of
> audios for each event (some events will have many audios to pick from, other
> will have none, as no sound applies to them).
>
> What do you think? This is the time to bring all the pushback and also to be
> creative and put on the table fresh ideas.

And, on the agent's answer: "I like your shape in general."

**The goal now:** background radio sound — static and radio sounds — playing
under the show from **a list of clips** (one clip on repeat would be boring),
**mixed with the voices**. Later: a list of sounds per event (many for some
events, none for others).

### §8.2 Words: "bed" — first avoided, then adopted as "the static bed"

The agent first called it a "bed" — the sound-production term (a *sound bed*,
an *ambience bed*: a continuous background layer under the foreground). The
owner (verbatim): "I do not understand why you call it "the bed" explain. Do
you mean the background noise we are going to add occasionally?" The documents
said **background radio sound** for a while. **Then settled (§8.8):** the owner
adopted the word once its meaning was clear — "I am ok with adopting the term
"bed", I was unaware of the sound-production meaning" — and described the design;
a bed is defined by its role, a quiet layer *under* the foreground moved up and
down around it, not by being unbroken, so a bed with silences in it is still a
bed. The project's term: **the static bed** (§8.8).

### §8.3 The folder tree (the owner's shape, the agent's improvements)

Like EARS (`zombie-radio-datasets/ears/<speaker>/<type>.wav` + `.txt`):
**source** at the top (a dataset, a library or a model), then **the kind of
sound**, then the files, each with a small metadata file.

```
zombie-radio-datasets/              (outside git, beside the checkouts)
  README.txt                        + a "sounds/" section: what is here, the licences, the tools
  ears/ …                           (unchanged)
  sounds/
    freesound/                      a source: a dataset, a library, or a model
      radio-static/                 a kind of sound, in our own words (kebab-case)
        675937-shortwave-radio-with-electrical-noises.mp3
        675937-shortwave-radio-with-electrical-noises.json
      radio-bleed/                  other stations, Morse, voices leaking through
      sirens/
    stable-audio-3-small-sfx/       (later) a model is a source too
      radio-static/
        shortwave-crackle-seed1.wav + .json
    pages/
      index-<start time>.html       pages of players, one per fetch, as with EARS
```

**The agent's improvements (accepted with the shape):**

- **A file's name starts with the source's own id** (Freesound's), then a short
  readable slug: unique, sortable, and it leads back to its page. A generated
  file: the prompt's slug and the seed.
- **One `.json` per audio file**, with: the source, its id and page; the name,
  the author and the author's page; the licence — its name, its link and a
  simple class (`cc0`, `cc-by`, `cc-by-nc`) — and, for CC-BY, **the credit line
  ready to paste**; the length, sample rate and channels; whether the file is a
  **preview** (`preview-hq-mp3`) or the **original**; when it was downloaded,
  and its SHA-256; the source's own tags and description; and ours — the kind of
  sound, the owner's verdict (keep or reject) and notes.
- **Two stages, as with the voices.** `sounds/` is **the pool**: everything
  downloaded, raw. What the show plays is **the chosen set**, made by a tool —
  as `tools/voices/cast_voices.py` turns EARS recordings into the personas'
  `ref-*.wav`: a small decision file (e.g. `tools/sounds/background.yaml`:
  which clips make the background radio sound) and a tool that trims,
  normalises the loudness, converts to OGG/Opus and copies them where the show
  reads them.
- **Where the chosen set lives, by licence:** CC0 clips may be committed beside
  the story in the fork (`stories/lab-outbreak/sounds/`; small OGGs, about
  100 KB each); CC-BY with a credits page (as the old-radio look credits its
  photograph); anything stricter outside git, like the cast's voices. The
  owner's call when we get there.

### §8.4 The pushbacks, and the owner's answers

1. **Whisper and the microphone.** The agent: a background sound from the
   speakers would reach the microphone and Whisper. **The owner (verbatim):**
   "No it won't, because of course we are going to turn off the background noises
   when the user pushes the push-to-talk button, and maybe even disable it
   completely in the contact rounds." **Decided:** silent while the
   push-to-talk button is held; perhaps off for the whole contact.
2. **Listening fatigue:** continuous static over a 20-minute demo tires an
   audience — low under the voices, changing shape (louder in the pauses, lower
   under a voice, silent while recording). (Open, with §8.2's question.)
3. **The looks' gauge** (`static/show/gauge.js`) taps every sound of the page's
   audio context, so the magic eye and the meters would move with the static:
   keep the background sound out of the gauge, or let it in (a magic eye
   flickering with static is period-true). **Open, the owner's.**
4. **The plain page** changes only with the owner's word: the agent proposes the
   background sound in the looks only, the plain page left silent as the working
   and debugging page. **Open, the owner's.**
5. **Every number a setting** (the house rule): on or off, the level, the level
   under a voice, the fades, the crossfade.
6. **The canned episode (Task 7):** played by the page, it gets the background
   sound for free; a recording would have to include it.

### §8.5 The ideas (the agent's, for the owner to keep or drop)

- **Fill the dead air** — the most valuable use: the background sound rises
  while the page waits for the model (3.7-4.9 s between rounds; 8.4 s after a
  trim, 2026-10-01) and dips when a voice starts; the pauses measured today
  become atmosphere — a slide for the talk.
- **Mixing by events, not a compressor:** the page already knows when each voice
  clip starts and ends (`static/show/player.js`, `playClip`), so ducking is a
  gain ramp at those moments (Web Audio's `GainNode` and its automation) — the
  simple shape of "mixing the two sources"; no second stream from the server
  (the owner's C8 design: assets loaded once, triggered on the page).
- **No repetition:** a shuffled list, crossfades of 1-2 s, each clip starting at
  a random point, a small random variation in level — a dozen clips can sound
  endless.
- **Two layers:** steady static, and a rarer **radio bleed** (faint other
  stations, Morse, a distant voice) — the owner's own Freesound finds would go
  in `radio-bleed/`.
- **Later, the story's state:** a tuning sweep when the show starts (the
  listener finding the frequency), a surge of static at the Breakdown, the static
  clearing a little at the Repair, harsher under a negative overtone — the
  bridge to the per-event sounds.

### §8.6 Freesound: access, the key, and the first candidates

**The key, handled without the chat** (the owner: "How can I paste this in the
terminal you will use? You are not using my own terminal sessions"). The agent's
first suggestion — an environment variable in a terminal — was wrong: the
agent's commands run in its own shell. Instead the owner put the key in a file
only the owner can read, outside both repositories, typed at a hidden prompt so
it stays out of the shell's history:

```bash
# A private folder for the project's secrets
mkdir -p ~/.config/zombie-radio && chmod 700 ~/.config/zombie-radio
# The key, typed at a hidden prompt, written to a file only the owner can read
read -s "?Freesound API key: " FSKEY && printf '%s' "$FSKEY" > ~/.config/zombie-radio/freesound.key && chmod 600 ~/.config/zombie-radio/freesound.key && unset FSKEY
```

The agent's scripts read `~/.config/zombie-radio/freesound.key`, never print it,
and send it in a request header (`Authorization: Token …`), not in the URL. To
revoke: delete the file, or the credential on Freesound's API page. The
credential: created at <https://freesound.org/apiv2/apply> (from Freesound's API
documentation), named "zombie-radio sound test", URL and callback left blank
(the callback is only for OAuth2).

**The API's facts** (Freesound's API documentation): with the key alone, the
text search and the **previews** (high-quality MP3) — enough to listen; the
original files need OAuth2 on the owner's account; limits 60 requests a minute
and 2,000 a day (originals: 30 and 500).

**Checked, 2026-10-01:** HTTP 200 for a search; the CC0 filter works
(`license:"Creative Commons 0"`); a duration filter is needed (the first match
for "shortwave radio static" was 238 s long). The searches, filtered to CC0 and
1-15 s, sorted by rating:

| Search | CC0 matches of 1-15 s |
|---|---|
| shortwave radio static | 33 |
| old radio turn on | **0** |
| radio switch on / radio turn on / radio on off click | 2 (a digital rack's knob) |
| valve radio | 15 (one radio switch; the rest a game's voice lines) |
| old radio | 68 |
| radio knob | 6 |
| distant sirens | 4 |
| sirens city | 20 |

**The nine candidates** (details from the API, nothing downloaded; all **CC0**;
previews 1.39 MB in all) — kept by the agent in
`<scratchpad>/fs-picks.json`, to be re-made by the download tool:

| Kind | Freesound id | Name | Author | Length | Rating | Original | Preview |
|---|---|---|---|---|---|---|---|
| radio static | 675937 | S30-42 Shortwave radio with electrical noises | craigsmith | 11.9 s | 5.0 (10) | WAV 48 kHz mono | 256 KB |
| radio static | 717474 | Shortwave radio FX001 | knasterask1 | 10.8 s | 5.0 (8) | WAV 7.1 kHz mono (lo-fi) | 74 KB |
| radio static | 436121 | Lo-fi AM/FM radio (Two stations mixed) | dersinnsspace | 7.8 s | 5.0 (7) | WAV 44.1 kHz stereo | 182 KB |
| receiver on | 369964 | Old radio switch | eneibol | 4.6 s | 4.9 (22) | WAV 48 kHz stereo | 109 KB |
| receiver on | 528272 | Turning a radio on | pfranzen | 2.0 s | 4.7 (15) | OGG 48 kHz stereo | 42 KB |
| receiver on | 629301 | Press radio knob | greatsoundstube | 6.4 s | 5.0 (13) | WAV 44.1 kHz mono | 149 KB |
| sirens | 717560 | Siren, ambulance, short distant pass | TRP | 7.8 s | 4.7 (14) | MP3 48 kHz stereo | 168 KB |
| sirens | 451068 | Siren ambulance European, distant echo | kyles | 11.3 s | 4.7 (10) | WAV 48 kHz stereo | 264 KB |
| sirens | 724115 | Sirens in distance | TSP-Talk | 8.0 s | unrated | WAV 192 kHz stereo | 177 KB |

Notes: CC0 period radio sounds are scarce (a CC-BY search would widen the field,
with credits); 451068 is a European siren; the static bed needs **more static
and radio clips** than these three — the owner's own Freesound finds (ids or
links to come) plus a wider static search — and **longer ones**: these searches
kept clips of 1-15 s (a sound effect's length); a bed wants clips of **20-240 s**
(§8.8, refinement 1).

### §8.7 The order agreed

1. **This tree**, and a small download tool in this repository
   (`tools/sounds/fetch_freesound.py`, standard library, like
   `tools/voices/fetch_ears.py`): ids or a search in, the previews and their
   `.json` out into `zombie-radio-datasets/sounds/freesound/<kind>/`, a page of
   players per fetch; a dry run first (the files, their sizes and licences), the
   owner's approval, then the download. **Done 2026-10-01, night (§8.9):** the
   tool built; the owner's 17 finds downloaded.
2. **The owner's picks** for the background radio sound (the owner's finds and
   the static candidates).
3. **The shape of the static bed in the fork**, discussion first — the owner's
   design and the settings draft are in §8.8; still to settle: where it plays (the looks, the plain page —
   §8.4.4); the ducking under the voice and the rise in the pauses (§8.5);
   silent while push-to-talk is held, perhaps off for the contact (§8.4.1); the
   gauge (§8.4.3); the settings (§8.4.5); where the chosen clips live (§8.3).
4. **Build it and listen.**
5. **Then broaden:** sounds per event (a list per event, many or none), and the
   generated sounds of §4-§6 for what Freesound lacks.

The TODO's polish item "Dead-air static while a round is generated" becomes
part of this (§8.5, the first idea).

### §8.8 The static bed — the owner's design (2026-10-01, later that evening)

**The owner (verbatim):**

> I am ok with adopting the term "bed", I was unaware of the sound-production
> meaning... However if it clashes with the "occasional bursts of static and radio
> sounds with silence in between" then probably we should not adopt bed in our
> project's terminology. How I see it: I see us playing in very low volume a few
> audio clips of radio static (maybe 5 to 15 different audios, which we play in
> random order, and we reshuffle the order or audios when we reach the end of the
> list)... But importantly, I want to experiment with the volume going up or down
> depending if the cast is talking or if we are in between rounds... And I want to
> have a random period of silence from time to time... All configurable in the
> fork settings.
>
> What do you think about this general vision of the feature? Does this design
> respond to your bed terminology?

**The term.** It does not clash. In sound production a *bed* is defined by its
role — a quiet layer under the foreground (here the voices), moved up and down
around it — not by being unbroken; beds with gaps are common. **The project's
term: the static bed** — defined by the owner's design below.

**The owner's design:**

1. **A few clips of radio static** — 5 to 15 — played at **very low volume**,
   in **random order**; at the end of the list, **reshuffled** and played again.
2. **The volume moves with the show:** one level while the cast is talking,
   another between rounds — for the owner to experiment with.
3. **Random periods of silence** from time to time.
4. **Every number configurable** in the fork's settings.
5. (From §8.4.1) **silent while push-to-talk is held**, and perhaps off for the
   whole contact.

**The agent's judgment:** the right vision, buildable in small steps — a
shuffled list, levels tied to the show, random silences, all in settings — and
the cheapest way to solve the hard part, mixing the voices with a second sound,
before the sounds per event.

**The agent's refinements:**

1. **Longer clips.** The Freesound searches of §8.6 kept clips of 1-15 s, a
   sound effect's length; a bed wants clips of **20-240 s**, so the joins are
   rare — the first match for "shortwave radio static" was 238 s long. With 5-15
   clips that length, about half an hour of static before a repeat.
2. **No clicks at the joins:** a short fade out and in, or a 1-2 s crossfade,
   between clips — and when entering and leaving a silence. Static cut mid-wave
   clicks audibly.
3. **The reshuffle does not repeat across its seam:** the first clip of the new
   order is never the one that just ended.
4. **One loudness for every clip**, normalised when the clips are prepared (as
   the casting normalises the voices: RMS -20 dBFS, the peak under -1 dBFS) —
   otherwise the shuffled list jumps in level, and the owner's experiment with
   the volume drowns in the clips' own differences.
5. **Three states, each with its level, and a ramp between them** (a fraction of
   a second, never a jump):

   | State | When | Level |
   |---|---|---|
   | **under a voice** | a voice clip is playing (the page's `playClip`) | low |
   | **between rounds** | the page waits for the next round — 3.7-4.9 s, 8.4 s after a trim (measured 2026-10-01) | higher |
   | **listening** | push-to-talk held — and, with `bed_off_in_contact`, the whole contact | silent |

6. **Random silences, two numbers each:** how often — a random time between a
   minimum and a maximum (e.g. 30-120 s) — and how long — a random length (e.g.
   3-15 s); both with fades.

**The settings — a first draft of names** (in the fork's `show:` section;
the page gets them in the start reply, as it gets the voices' map):

| Setting | Example | What it does |
|---|---|---|
| `bed` | `true` | the static bed on or off |
| `bed_volume_voice` | 0.05 | the level under a voice |
| `bed_volume_between` | 0.15 | the level between rounds |
| `bed_ramp_s` | 0.5 | how fast the level moves from one state to another |
| `bed_crossfade_s` | 1.5 | the fade between two clips |
| `bed_silence_every_s` | [30, 120] | a silence comes after a random time in this range |
| `bed_silence_s` | [3, 15] | and lasts a random time in this range |
| `bed_off_in_contact` | `false` | silent through the whole contact, not only while recording |

The values are the agent's starting guesses, to tune by ear; the names to
settle when the feature is shaped in the fork.

**Still open, the owner's** (from §8.4): where the bed plays — the looks only,
the plain page silent (the agent's suggestion), or everywhere; the looks'
gauge — the bed kept out of it, or moving the needle; where the chosen clips
live (§8.3, by licence).

### §8.9 The owner's finds fetched: the tool, the dry run, the download (2026-10-01, night)

**The owner's finds (verbatim)** — "Some sounds of radio static of mixed radio
stations that I like:"

1. https://freesound.org/people/medialint/sounds/11859/
2. https://freesound.org/people/AlexMurphy53/sounds/719588/
3. https://freesound.org/people/theplax/sounds/615189/
4. https://freesound.org/people/-CASK-/sounds/730109/
5. https://freesound.org/people/wwstudioswastaken/sounds/625095/
6. https://freesound.org/people/ERH/sounds/34418/
7. https://freesound.org/people/vedas/sounds/396902/
8. https://freesound.org/people/exsil/sounds/652596/
9. https://freesound.org/people/acclivity/sounds/30302/
10. https://freesound.org/people/cognito%20perceptu/sounds/722884/
11. https://freesound.org/people/finneganmilla/sounds/557532/
12. https://freesound.org/people/nlux/sounds/624412/
13. https://freesound.org/people/kwahmah_02/sounds/255775/
14. https://freesound.org/people/NebulousRoyale/sounds/343740/
15. https://freesound.org/people/bassimat/sounds/855480/
16. https://freesound.org/people/thearchiveguy99/sounds/658932/
17. https://freesound.org/people/wtermini/sounds/546450/

And: "When you download them, beware not to send all the requests at once, we
do not want to be throttled." Then, on the dry run: "yes, download all 17 into
radio-static"; and on the tool's two flaws (below): "yes, fix both and write
§8.9".

#### The tool: `tools/sounds/fetch_freesound.py`

Step 1 of §8.7, built. Standard library only, like `tools/voices/fetch_ears.py`.

- **In:** Freesound ids or sound links (`--ids`, comma-separated, or
  `--ids-file`, one per line, `#` comments allowed), or a text search
  (`--search`, with `--license cc0|cc-by`, `--duration 20-240`, `--max N`; the
  best rated first). `--kind` names the folder, in our words (kebab-case).
- **Ids in one request:** all the ids go into a single search, filtered by id
  (`filter=id:(11859 OR 719588 OR …)`, up to 50 per request) — 17 sounds cost
  one API request, not 17. An id Freesound does not know is reported, not fatal.
- **The key:** read from `~/.config/zombie-radio/freesound.key`, sent in the
  `Authorization: Token …` header, never printed, never in a URL (§8.6).
- **Paced:** every request waits `--pause` seconds after the one before (2 by
  default) — at most 30 a minute, half of Freesound's 60. A `429 Too Many
  Requests` stops the tool with a message, no retry.
- **A dry run by default:** the table of what would be fetched — id, name,
  author, licence, length, rating, the original's format, and the preview's
  size **measured** (a `HEAD` request to the preview, no audio) — and the total.
  Nothing is downloaded without `--fetch`.
- **With `--fetch`:** each preview (`preview-hq-mp3`) into
  `zombie-radio-datasets/sounds/freesound/<kind>/<id>-<slug>.mp3` (written to a
  `.part` file first, renamed when complete), its `.json` beside it, and a page
  of players for the fetch, `sounds/pages/index-<start time>.html`.
- **Already here:** a file is skipped, with no request, when it and its `.json`
  exist and its size and SHA-256 match the `.json`'s.
- **The `.json`** (the fields of §8.3): `source`, `id`, `page`, `name`,
  `author`, `author_page`; `licence` — `name`, `url`, `class` (`cc0`, `cc-by`,
  `cc-by-nc`, `sampling-plus`, `other`) and `credit`, the credit line ready to
  paste (for every licence but CC0); `file` — what it is (`preview-hq-mp3`), its
  URL, bytes, SHA-256 and when it was downloaded; `original` — the uploaded
  file's type, bytes, length, rate, channels and bit depth; `rating`;
  `uploaded`; Freesound's `tags` and `description`; and ours — `kind`,
  `verdict` (empty until the owner listens) and `notes`.

How to run it, from this repository's root:

```bash
# A dry run: what would be fetched, with each preview's size and licence; downloads nothing
python3 tools/sounds/fetch_freesound.py --kind radio-static --ids-file picks.txt
# The download, after the owner's approval of the dry run
python3 tools/sounds/fetch_freesound.py --kind radio-static --ids-file picks.txt --fetch
# A search instead of ids: the 15 best-rated CC0 sounds of 20-240 s (a dry run)
python3 tools/sounds/fetch_freesound.py --kind radio-static --search "shortwave radio static" --license cc0 --duration 20-240
```

The first dry run on the owner's 17 links, 2026-10-01 (the real output; the
preview sizes in KB of 1,024 bytes, the total in MB of 1,000,000):

```
  11859  analog_noise_arped_radio_static.wav           medialint           Sampling+ 1.0    11.7 s  4.3 (38)    WAV 96000 Hz 2 ch       preview    309 KB  (would fetch)
 719588  Handheld radio music and static               AlexMurphy53        CC BY 4.0        41.8 s  4.7 (11)    MP3 48000 Hz 2 ch       preview    976 KB  (would fetch)
 615189  radio11.wav                                   theplax             CC BY 4.0        14.1 s  4.9 (11)    WAV 48000 Hz 2 ch       preview    328 KB  (would fetch)
 730109  Shortwave Radio static with indistinguishabl  -CASK-              CC BY 4.0       172.1 s  4.8 (8)     FLAC 44100 Hz 2 ch      preview   3999 KB  (would fetch)
 625095  radio_static_01.flac                          wwstudioswastaken   CC0 1.0          84.7 s  4.9 (19)    FLAC 96000 Hz 1 ch      preview   1815 KB  (would fetch)
  34418  morse static.wav                              ERH                 CC BY 4.0         4.9 s  4.2 (36)    WAV 44100 Hz 2 ch       preview    103 KB  (would fetch)
 396902  Full radio sweep.wav                          vedas               CC0 1.0         296.8 s  4.9 (42)    WAV 44100 Hz 2 ch       preview   6117 KB  (would fetch)
 652596  Vintage Radio Tuning 5.WAV                    exsil               CC0 1.0         110.8 s  4.7 (21)    WAV 44100 Hz 2 ch       preview   2435 KB  (would fetch)
  30302  CS3B_beacon.wav                               acclivity           CC BY-NC 4.0     11.9 s  3.5 (11)    WAV 44100 Hz 1 ch       preview    262 KB  (would fetch)
 722884  harsh analog fm radio flips                   cognito perceptu    CC0 1.0          21.3 s  5.0 (6)     WAV 44100 Hz 2 ch       preview    491 KB  (would fetch)
 557532  radio tuning fm.mp3                           finneganmilla       CC0 1.0         165.3 s  4.1 (14)    MP3 44100 Hz 2 ch       preview   3064 KB  (would fetch)
 624412  Radio Music - A MakeNoise Morphagene Reel     nlux                CC0 1.0         156.2 s  5.0 (18)    WAV 48000 Hz 2 ch       preview   3299 KB  (would fetch)
 255775  S06Russian.wav                                kwahmah_02          CC BY 3.0       110.0 s  4.7 (14)    WAV 7119 Hz 1 ch        preview    744 KB  (would fetch)
 343740  Radio transmission morse code @4606.2kHz Pol  NebulousRoyale      CC0 1.0          76.3 s  4.7 (51)    WAV 8000 Hz 1 ch        preview    499 KB  (would fetch)
 855480  Radio — Generative Sound by Glorb             bassimat            CC0 1.0         120.0 s  5.0 (1)     WAV 44100 Hz 2 ch       preview   1865 KB  (would fetch)
 658932  Dial-up_sound.mp3.flac                        thearchiveguy99     CC0 1.0          19.3 s  4.9 (102)   FLAC 96000 Hz 1 ch      preview    427 KB  (would fetch)
 546450  The Sound of dial-up Internet                 wtermini            CC0 1.0          28.7 s  4.9 (150)   MP3 48000 Hz 2 ch       preview    657 KB  (would fetch)

17 sounds, 24.1 minutes in all; licences: cc-by 5, cc-by-nc 1, cc0 10, sampling-plus 1
would fetch: 28.05 MB

[18 requests, 0.018 MB transferred]
```

#### The 17 sounds (from Freesound's API)

| # | Id | Name | Author | Licence | Length | Rating | Original |
|---|---|---|---|---|---|---|---|
| 1 | [11859](https://freesound.org/people/medialint/sounds/11859/) | analog_noise_arped_radio_static.wav | medialint | Sampling+ 1.0 | 11.7 s | 4.3 (38) | WAV, 96000 Hz, 2 ch |
| 2 | [719588](https://freesound.org/people/AlexMurphy53/sounds/719588/) | Handheld radio music and static | AlexMurphy53 | CC BY 4.0 | 41.8 s | 4.7 (11) | MP3, 48000 Hz, 2 ch |
| 3 | [615189](https://freesound.org/people/theplax/sounds/615189/) | radio11.wav | theplax | CC BY 4.0 | 14.1 s | 4.9 (11) | WAV, 48000 Hz, 2 ch |
| 4 | [730109](https://freesound.org/people/-CASK-/sounds/730109/) | Shortwave Radio static with indistinguishable foreign chatter and static | -CASK- | CC BY 4.0 | 172.1 s | 4.8 (8) | FLAC, 44100 Hz, 2 ch |
| 5 | [625095](https://freesound.org/people/wwstudioswastaken/sounds/625095/) | radio_static_01.flac | wwstudioswastaken | CC0 1.0 | 84.7 s | 4.9 (19) | FLAC, 96000 Hz, 1 ch |
| 6 | [34418](https://freesound.org/people/ERH/sounds/34418/) | morse static.wav | ERH | CC BY 4.0 | 4.9 s | 4.2 (36) | WAV, 44100 Hz, 2 ch |
| 7 | [396902](https://freesound.org/people/vedas/sounds/396902/) | Full radio sweep.wav | vedas | CC0 1.0 | 296.8 s | 4.9 (42) | WAV, 44100 Hz, 2 ch |
| 8 | [652596](https://freesound.org/people/exsil/sounds/652596/) | Vintage Radio Tuning 5.WAV | exsil | CC0 1.0 | 110.8 s | 4.7 (21) | WAV, 44100 Hz, 2 ch |
| 9 | [30302](https://freesound.org/people/acclivity/sounds/30302/) | CS3B_beacon.wav | acclivity | CC BY-NC 4.0 | 11.9 s | 3.5 (11) | WAV, 44100 Hz, 1 ch |
| 10 | [722884](https://freesound.org/people/cognito%20perceptu/sounds/722884/) | harsh analog fm radio flips | cognito perceptu | CC0 1.0 | 21.3 s | 5.0 (6) | WAV, 44100 Hz, 2 ch |
| 11 | [557532](https://freesound.org/people/finneganmilla/sounds/557532/) | radio tuning fm.mp3 | finneganmilla | CC0 1.0 | 165.3 s | 4.1 (14) | MP3, 44100 Hz, 2 ch |
| 12 | [624412](https://freesound.org/people/nlux/sounds/624412/) | Radio Music - A MakeNoise Morphagene Reel | nlux | CC0 1.0 | 156.2 s | 5.0 (18) | WAV, 48000 Hz, 2 ch |
| 13 | [255775](https://freesound.org/people/kwahmah_02/sounds/255775/) | S06Russian.wav | kwahmah_02 | CC BY 3.0 | 110.0 s | 4.7 (14) | WAV, 7119 Hz, 1 ch |
| 14 | [343740](https://freesound.org/people/NebulousRoyale/sounds/343740/) | Radio transmission morse code @4606.2kHz Poland | NebulousRoyale | CC0 1.0 | 76.3 s | 4.7 (51) | WAV, 8000 Hz, 1 ch |
| 15 | [855480](https://freesound.org/people/bassimat/sounds/855480/) | Radio — Generative Sound by Glorb | bassimat | CC0 1.0 | 120.0 s | 5.0 (1) | WAV, 44100 Hz, 2 ch |
| 16 | [658932](https://freesound.org/people/thearchiveguy99/sounds/658932/) | Dial-up_sound.mp3.flac | thearchiveguy99 | CC0 1.0 | 19.3 s | 4.9 (102) | FLAC, 96000 Hz, 1 ch |
| 17 | [546450](https://freesound.org/people/wtermini/sounds/546450/) | The Sound of dial-up Internet | wtermini | CC0 1.0 | 28.7 s | 4.9 (150) | MP3, 48000 Hz, 2 ch |

**The licences, and what they mean for us.** All of them allow keeping the
previews in `zombie-radio-datasets/`, outside git; the licence matters only for
what may later be committed to the public fork (§8.3):

| Licence | Sounds | What it allows us |
|---|---|---|
| **CC0** | 10 — #5, 7, 8, 10, 11, 12, 14, 15, 16, 17 | public domain: commit and play them, no credit needed |
| **CC BY** | 5 — #2, 3, 4, 6 (4.0), 13 (3.0) | commit and play them **with a credit** — the `.json`'s `licence.credit` |
| **CC BY-NC** | 1 — #9 (the beacon) | non-commercial only: it stays outside git, like the EARS voices |
| **Sampling+ 1.0** | 1 — #1 | a retired Creative Commons licence made for sampling and remixing; the agent's suggestion: treat it like CC BY-NC — outside git |

**What the agent noticed, for the owner's listening** (not objections):

- **Length.** Five are shorter than the 20 s a bed clip wants (§8.8, refinement
  1): #1 (11.7 s), #3 (14.1 s), #6 (4.9 s), #9 (11.9 s), #16 (19.3 s) — frequent
  joins if used as bed clips, or short bursts between long ones. #7 (296.8 s) is
  longer than 240 s — fine.
- **Kind.** All 17 went to `radio-static/`, as the owner named them. Some are
  Morse (#6, #14), a beacon (#9) and dial-up modems (#16, #17) — candidates for
  the rarer second layer of §8.5 ("radio bleed") if the owner wants it apart.

#### The download (2026-10-01, 22:14:36 to 22:21:13 CDT)

Approved by the owner ("yes, download all 17 into radio-static"). The real
output's last lines:

```
17 sounds, 24.1 minutes in all; licences: cc-by 5, cc-by-nc 1, cc0 10, sampling-plus 1
fetched: 28.05 MB
page: /Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/sounds/pages/index-2026-10-01T22:14:37.html

[35 requests, 28.064 MB transferred]
```

**No throttling, no error.** 6 minutes 37 seconds for 28 MB: Freesound's CDN
served the larger previews at about 40-60 s each; the pauses were at most 70 s
of it (2 s × 35, and none after a request that itself took longer than 2 s).

**Checked after the download:**

- 17 `.mp3` and 17 `.json` files, no `.part` left; the folder 27 MB (`du -sh`).
- **Each file's size and SHA-256 equal its `.json`'s:** 17 of 17. (The agent's
  first check also tested how each file begins and flagged #13 and #14 — a
  mistake in the check, not the files: they begin `ff e3`, an MPEG-2 frame, as
  low-rate MP3s do, where the others begin `ff fb`; the check was re-run on the
  size and hash alone.)
- **Every MP3 reads, and its length matches Freesound's** to 0.2 s (macOS
  `afinfo`):

| # | File | Preview bytes | Length (afinfo) | Bit rate | Preview's rate |
|---|---|---|---|---|---|
| 1 | `11859-analog-noise-arped-radio-static.mp3` | 316,032 | 11.7 s | 215 kbps | 48,000 Hz, 2 ch |
| 2 | `719588-handheld-radio-music-and-static.mp3` | 999,312 | 41.8 s | 191 kbps | 48,000 Hz, 2 ch |
| 3 | `615189-radio11.mp3` | 335,904 | 14.1 s | 190 kbps | 48,000 Hz, 2 ch |
| 4 | `730109-shortwave-radio-static-with-indistinguishable-foreign-chatte.mp3` | 4,094,696 | 172.2 s | 190 kbps | 44,100 Hz, 2 ch |
| 5 | `625095-radio-static-01.mp3` | 1,858,368 | 84.8 s | 175 kbps | 48,000 Hz, 1 ch |
| 6 | `34418-morse-static.mp3` | 105,414 | 4.9 s | 171 kbps | 44,100 Hz, 2 ch |
| 7 | `396902-full-radio-sweep.mp3` | 6,264,252 | 296.8 s | 169 kbps | 44,100 Hz, 2 ch |
| 8 | `652596-vintage-radio-tuning-5.mp3` | 2,493,758 | 110.8 s | 180 kbps | 44,100 Hz, 2 ch |
| 9 | `30302-cs3b-beacon.mp3` | 268,001 | 11.9 s | 180 kbps | 44,100 Hz, 1 ch |
| 10 | `722884-harsh-analog-fm-radio-flips.mp3` | 502,278 | 21.4 s | 188 kbps | 44,100 Hz, 2 ch |
| 11 | `557532-radio-tuning-fm.mp3` | 3,137,048 | 165.4 s | 152 kbps | 44,100 Hz, 2 ch |
| 12 | `624412-radio-music-a-makenoise-morphagene-reel.mp3` | 3,377,760 | 156.2 s | 173 kbps | 48,000 Hz, 2 ch |
| 13 | `255775-s06russian.mp3` | 762,336 | 110.2 s | 55 kbps | 8,000 Hz, 1 ch |
| 14 | `343740-radio-transmission-morse-code-4606-2khz-poland.mp3` | 510,768 | 76.5 s | 53 kbps | 8,000 Hz, 1 ch |
| 15 | `855480-radio-generative-sound-by-glorb.mp3` | 1,909,588 | 120.0 s | 127 kbps | 44,100 Hz, 2 ch |
| 16 | `658932-dial-up-sound-mp3.mp3` | 436,992 | 19.3 s | 181 kbps | 48,000 Hz, 1 ch |
| 17 | `546450-the-sound-of-dial-up-internet.mp3` | 672,792 | 28.7 s | 187 kbps | 48,000 Hz, 2 ch |

#13 and #14 are the lo-fi ones (about 55 kbps, 8 kHz mono): their originals
were recorded at 7,119 Hz and 8,000 Hz — the recordings, not the download; a
shortwave radio sounds like that.

**Where they are:**
`/Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/sounds/freesound/radio-static/`;
the page of players `sounds/pages/index-2026-10-01T22:14:37.html` (one row per
sound: the id linked to its page, the name and author, the licence, the length,
a player). The datasets folder's `README.txt` gained a `sounds/` section (the
tree, the licences, the tool).

```bash
# Listen: open the fetch's page of players in the browser
open "/Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/sounds/pages/index-2026-10-01T22:14:37.html"
```

#### The tool's two flaws, found in the download and fixed

1. **A wasted request per file:** the first version measured each preview with a
   `HEAD` request even when downloading it — 35 requests where 18 would do. Now
   a download is a single `GET` (its size known from the bytes), the `HEAD` only
   in a dry run, and a file already here costs no request.
2. **Silent until the end:** Python holds its printed lines back when the output
   goes to a pipe (`| tee`), so the download looked stuck for minutes. Now the
   output is written line by line.

**Checked:** the dry run again on the 17 — `17` lines "(already here)", `[1
requests, 0.018 MB transferred]` (the one API request; before the fix, 18);
and the download path with the network stubbed (no real request): a new file —
one `GET`, no `HEAD`; the same fetch again — no request; a dry run — no
request; the credit line written.

#### Next

The owner's listening: 5-15 clips for the bed (§8.7, step 2) — said in chat, or
written into each `.json`'s `ours.verdict` (`keep` / `reject`) and `ours.notes`.
Then the shape in the fork (§8.7, step 3).

## §7. Sources

- [Stable Audio 3 — the paper (arXiv 2605.17991)](https://arxiv.org/html/2605.17991)
- [stabilityai/stable-audio-3-small-sfx — the model card](https://huggingface.co/stabilityai/stable-audio-3-small-sfx)
- [Stable Audio 3 Review — ChatForest](https://chatforest.com/reviews/stability-ai-stable-audio-3-open-weight-music-sfx-generation/)
- [OpenMOSS/MOSS-TTS — the family's README (MOSS-SoundEffect v1 and v2.0)](https://github.com/OpenMOSS/MOSS-TTS)
- [OpenMOSS-Team/MOSS-SoundEffect-v2.0 — the model card](https://huggingface.co/OpenMOSS-Team/MOSS-SoundEffect-v2.0)
- [SonyResearch/Woosh](https://github.com/SonyResearch/Woosh) and [Introducing Woosh — Sony AI](https://ai.sony/blog/introducing-woosh-sony-ais-sound-effect-foundation-model)
- [TangoFlux](https://tangoflux.github.io/) and [declare-lab/TangoFlux — the model card](https://huggingface.co/declare-lab/TangoFlux)
- [hkchengrex/MMAudio](https://github.com/hkchengrex/MMAudio)
- [AudioGen Model Card](https://facebookresearch.github.io/audiocraft/model_cards/AUDIOGEN_MODEL_CARD.html) and [facebookresearch/audiocraft](https://github.com/facebookresearch/audiocraft/)
- [Stable Audio Open (arXiv 2407.14358)](https://arxiv.org/html/2407.14358v1)
- [Freesound — FAQ](https://freesound.org/help/faq/), [APIv2 overview](https://freesound.org/docs/api/overview.html) and [resources](https://freesound.org/docs/api/resources_apiv2.html)
- [FSD50K: an Open Dataset of Human-Labeled Sound Events (arXiv 2010.00475)](https://ar5iv.labs.arxiv.org/html/2010.00475)
- [Sonniss — GDC 2026 Game Audio Bundle](https://gdc.sonniss.com/) and [Bedroom Producers Blog on the 2026 bundle](https://bedroomproducersblog.com/2026/03/16/sonniss-gdc-2026-bundle/)
- [The BBC's sound effect archive, 33,000 samples (Mixmag)](https://mixmag.net/read/bbc-sound-effect-archive-free-audio-samples-news) and [BBC Sound Effects library for non-commercial use (Gearspace)](https://gearspace.com/board/new-product-alert-2-older-threads/1212518-bbc-sound-effects-library-avail-non-commercial-use.html)
- [Pixabay — FAQ](https://pixabay.com/service/faq/)
- [Internet Archive — Old-Time Radio Collection](https://archive.org/details/old-time-radio-collection)
- [Ultimate Guide — The Best Open Source Models for Sound Design in 2026 (SiliconFlow)](https://www.siliconflow.com/articles/best-open-source-models-for-sound-design)
