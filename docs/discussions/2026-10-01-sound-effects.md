# Sound effects — an AI model for the show's sounds: the idea, its history, the research

**Date:** 2026-10-01 (the idea: 2026-09-30) · **Arc:** MVP prototype · **Branch:**
`alfre2v/sound-effects`
**Type:** discussion — the owner's idea of adding an AI model for sound effects;
the project's earlier notes on sound effects; the agent's research into the
open text-to-audio models of 2026, checked at their sources; how a library of
sounds would fit the show; a recommendation.
**Status:** OPEN — **back on the table on 2026-10-07 (§9): the owner's two-part plan, an experiment with
sound-effect models, then sounds per event; pending discussion.** Earlier: **narrowed on 2026-10-01 evening (§8): first the static bed**
(5-15 clips of radio static at low volume, shuffled, the level moving with the
show, random silences, all in settings — the owner's design, §8.8), **from
Freesound**; the folder tree agreed; the
Freesound key in place and checked; nine CC0 candidates listed. **The fetch
tool built** (`tools/sounds/fetch_freesound.py`) and **the owner's 17 Freesound
finds downloaded** (previews, 28 MB, outside git — §8.9). **How to play the
bed** — the owner's seven questions and the agent's analysis (§8.10), and **the
event sounds as a layer of their own beside the bed** (§8.11); **the owner's
first decisions** (§8.12: constantly, the level moving; the files untouched, a
gain per clip; one list; shuffled; the filter as a switch; no trimming), and
**the rest settled three at a time** (§8.13: the looks only, silences on a
timer, the clips copied unchanged into the client's `Sounds/bed/`, silent while
push-to-talk is held, a live mute key, the gauge for the voices only, built
now). **The first build's plan** is in §8.13; **step 1 built** (§8.14: the list `tools/sounds/bed.yaml`, the tool `prepare_bed.py`, the 17 clips and `bed.json` in the client's and the dev checkout's `Sounds/bed/`). The research on generated and recorded sounds (§4) and the
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

### §8.10 How to play the bed: the owner's questions, the agent's analysis (2026-10-01, night)

**The owner (verbatim)**, after the commit of §8.9:

> Picking the clips is the least interesting thing... What I want to discuss
> with you is proposals to how implement playing these audios.
>
> * Do we play them constantly? Or at certain moments in the play (e.g. in
>   between rounds)?
> * Do we normalize the volume of those audios?... My inclination is no
>   normalization.
> * Do we apply some transformations to those audios?... Maybe to lower the
>   bitrate or to make them mono?
> * During the play: Do we keep the volume of the bed stable or do we modify the
>   volume to better suit our narrative... My inclination is yes, we have to move
>   the volume up and down. Specifically we turn the volume down slowly every
>   time a cast voice starts to speak, but we keep some random brief
>   fluctuations of volume up and down.
> * Do we allow a different list of background audios for different types of
>   rounds?
> * What strategy do we follow to rotate the audios? ... My lean is to do a
>   random shuffle every time we consume the whole list.
> * What strategy do we follow to insert silence between the background audios?
>
> Do you have more questions to settle?

Then, on the answer below: "Wow, there is a lot of information here. I cannot
possibly answer all of those in one go." — **nothing in this section is decided
yet**; the owner answers one question at a time. The owner's one answer so far
is on question 5, in §8.11.

#### What the agent read and measured first

**How the page plays the voices today** (the fork at `tz-0.5`):

- `static/show/player.js` — one `AudioContext` for the page (`voice.ctx`),
  created on the first click (`unlockAudio`; browsers allow sound only after
  one). Each voice chunk comes from `/api/tts` as base64 WAV and is **decoded
  whole** into raw samples (`decodeAudioData`), then played by `playClip`: a
  buffer source connected straight to the speakers (`ctx.destination`). Between
  the chunks of one line, a pause of **80 ms** (`pauseInLineMs`); after a line,
  **250 ms** (`pauseBetweenLinesMs`).
- `static/show/show.js` — the round loop (`runShow`): the listener's turn if the
  last round listens → ask for the next round (`playRound`) → wait until it has
  all been said (`playOut`, which awaits `drained()`). **The next round is asked
  for only after the last one has been said** — so the time between rounds is
  the model writing the next round plus the first chunk's synthesis: measured
  **3.7-4.9 s**, and **8.4 s** after a trim (2026-10-01).
- `static/show/gauge.js` — the looks' gauge **wraps `createBufferSource`** of
  the page's context (`tapContext`): every buffer source connected to the
  speakers also feeds the gauge's analyser. A sound played another way (an
  `<audio>` element through `createMediaElementSource`, or a source connected
  to a gain node rather than straight to the speakers) does not reach the
  gauge.
- The round kinds (`app/show/script.py`): `orientation`, `free`, `repair`,
  `exchange`, `last-exchange`, `re-call`, `breakdown`, `switch-off`,
  `invitation`; `answer` and `static` are only in older records, kept loadable
  (the `static` kind has nothing to do with the bed).

**The 17 clips' loudness**, measured with ffmpeg (installed on the laptop,
`/opt/homebrew/bin/ffmpeg`); `volumedetect` reads the whole file and reports its
average level (`mean_volume`, the RMS in dB below full scale) and its loudest
sample (`max_volume`):

```bash
# From the folder of the clips: the average and the peak level of each, quietest first
cd /Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/sounds/freesound/radio-static
for f in *.mp3; do r=$(ffmpeg -hide_banner -nostats -i "$f" -af volumedetect -f null - 2>&1 | awk '/mean_volume/{m=$5} /max_volume/{x=$5} END{printf "%6.1f %6.1f", m, x}'); printf '%s  %s\n' "$r" "${f%%-*}"; done | sort -n
```

| # (§8.9) | Id | Name | Average (RMS) | Peak |
|---|---|---|---|---|
| 6 | 34418 | morse static | −31.1 dB | −7.8 dB |
| 4 | 730109 | Shortwave Radio static with indistinguishable foreign chatter | −29.4 dB | −7.9 dB |
| 11 | 557532 | radio tuning fm | −26.5 dB | −4.5 dB |
| 17 | 546450 | The Sound of dial-up Internet | −26.4 dB | −8.1 dB |
| 8 | 652596 | Vintage Radio Tuning 5 | −25.7 dB | −0.1 dB |
| 13 | 255775 | S06Russian | −25.3 dB | −8.6 dB |
| 5 | 625095 | radio_static_01 | −22.3 dB | −0.3 dB |
| 3 | 615189 | radio11 | −21.2 dB | −3.3 dB |
| 2 | 719588 | Handheld radio music and static | −21.1 dB | −1.2 dB |
| 10 | 722884 | harsh analog fm radio flips | −19.5 dB | −0.4 dB |
| 16 | 658932 | Dial-up_sound | −18.9 dB | −3.2 dB |
| 1 | 11859 | analog_noise_arped_radio_static | −17.4 dB | 0.0 dB |
| 14 | 343740 | Radio transmission morse code @4606.2kHz Poland | −17.3 dB | 0.0 dB |
| 12 | 624412 | Radio Music - A MakeNoise Morphagene Reel | −17.0 dB | −0.3 dB |
| 7 | 396902 | Full radio sweep | −16.5 dB | 0.0 dB |
| 9 | 30302 | CS3B_beacon | −15.2 dB | −5.8 dB |
| 15 | 855480 | Radio — Generative Sound by Glorb | −11.0 dB | 0.0 dB |

**The spread of the averages is 20 dB** (−31.1 to −11.0): the loudest clip's
amplitude is 10 times the quietest's (20 dB = a factor of 10 in amplitude), and
it sounds roughly 4 times as loud (each 10 dB sounds about twice as loud).

#### The agent's answers, question by question (proposals, not decisions)

**1. Constantly, or at certain moments?** *Recommendation: constantly, with the
level moving.* In the fiction the audience listens to a shortwave receiver, and
a receiver hisses all the time. A bed only between rounds would switch on and
off every 20-40 seconds, and the audience would hear an effect being switched,
not a radio. **The choice need not be made now:** with the level under a voice
as a setting, "only between rounds" is that setting at 0 — the two versions
are one number apart, and the owner can compare them by ear.

**2. Normalize the volume?** (The owner leans no.) The measurement above says
the shuffle would jump by up to 20 dB at every change of clip, and that jump
would drown the experiment the owner wants — moving the level with the show.
*Recommendation, which keeps the owner's "no": the files are not touched;
instead each clip carries one gain number* in the list that names the clips —
measured by a tool to bring every clip to a common level, and overridable by ear
(a clip deliberately louder, say). The files stay as they are; what each clip
contributes is visible and tunable.

**3. Transformations (bitrate, mono)?**

- **Mono: yes.** The voices are mono; a radio's speaker is mono; and memory —
  the reason that matters most. Decoded whole as the voices are
  (`decodeAudioData`: raw 32-bit samples), the 17 clips would take **about
  555 MB** of the browser's memory: 24.1 minutes = 1,446 s × 48,000 samples a
  second × 2 channels × 4 bytes = 555,264,000 bytes (at 44,100 samples a second,
  about 510 MB). Mono halves it — but the better answer is **not to decode the
  bed whole at all**: play each clip through an `<audio>` element connected to
  the page's context (`createMediaElementSource`), which streams the file and
  holds only a little of it at a time.
- **Bitrate: it hardly matters for playing.** The page loads the clips from the
  app on the same laptop; the venue's network never carries them. A lower
  bitrate matters only for size, if the chosen clips are committed to the fork:
  10 clips of about 90 s, mono, at 64 kbps = 900 s × 8,000 bytes a second ≈
  7.2 MB.
- **Trimming: yes, where needed** — a bad start or end, a stretch the owner
  does not like.
- **A creative idea, the owner's call:** a band-pass filter — only the middle
  frequencies, the band of a small AM speaker — would make the 8 kHz Russian
  recording (#13) and the 48 kHz FM sweep (#7) sound as if through the same
  receiver. Worth one A/B listen before adopting it.

**4. The bed's volume steady, or moving with the story?** *Agreed: moving.* The
owner's shape — down when a voice starts, with small random ups and downs.
Shortwave listeners have a word for those ups and downs: **fading** (radio
amateurs call it QSB) — the signal swelling and sinking; period-true, and a
slide for the talk. The agent's refinements:

1. **The level changes per round, not per voice clip.** The page pauses 80 ms
   between the chunks of a line and 250 ms between lines, and longer when the
   voice engine lags behind the playing; a bed rising in each of those gaps
   would pump audibly. Two states the page already knows:
   - **"voice"** — from the round's first clip starting until the round has all
     been said (`playOut`'s `drained()`, `show.js`);
   - **"between"** — from then until the next round's first clip.

   The gap between rounds — 3.7-4.9 s, 8.4 s after a trim — is long enough for
   the bed to rise noticeably and dip again.
2. **"Down slowly" — one caution:** a slow dip covers the first words of the
   line. A start: about 0.5 s down, 1.5 s back up — both settings, tuned by ear.
3. **The fading:** every few seconds, a random change of plus or minus a few dB,
   glided to (never a jump), in every state — two settings: how deep, and how
   often.

**5. Different lists for different kinds of round?** *Not in the first build —
but the data allows it from day one:* the list is a **named list** (`default`
only, for now), so a list for one kind of round later is a change of data, not
of code. The natural candidates are already in the story: the **breakdown**
(the receiver dies — harsher, louder static); the **repair** (the owner's tuning
sweeps, #7, #8, #11 — someone finding the frequency); the **contact** (the bed
off, as the owner said in §8.4.1). **Where the list lives: in the story**
(`stories/lab-outbreak/`), beside the voices' map in `overtones.yaml` — the
owner's rule that data maps live where they are central, not in a tool's
configuration. *(The owner's answer to this question, and the angle it adds —
event sounds — is §8.11.)*

**6. How to rotate the clips?** *Agreed: shuffle, and reshuffle when the list is
used up* — with the guard of §8.8 (refinement 3): the first clip of the new order
is never the one that just ended. An option, left out of the first build: start
each clip at a random point, so the first minute of a long clip is not always
the one heard.

**7. How to insert the silences?** Two shapes:

| Shape | How it works | Weakness |
|---|---|---|
| **A. At the joins** | after a clip ends, a silence with some probability | with clips up to 5 minutes long, silences can be minutes apart |
| **B. On a timer** | every 30-120 s (random), the bed fades out, the clip **pauses**, 3-15 s of silence (random), then it fades back in **where it stopped** | none that matters; as simple with an `<audio>` element (pause, then play) |

*Recommendation: B* — the signal dropping out and coming back — always with
fades (a hard cut sounds like a bug). Between two clips, a short crossfade and
no silence. (This is the timer the settings draft of §8.8 already names:
`bed_silence_every_s`, `bed_silence_s`.)

#### More questions to settle (the agent's, each with its recommendation)

1. **Where it plays.** The looks only; the plain page silent, as the working and
   debugging page — with a switch in the address, `?bed=on`, like `?voice=off`,
   to hear it there.
2. **The listener's turn.** Before push-to-talk is held: the "between" level
   (atmosphere while the audience thinks); **silent while it is held** (the
   owner's rule, §8.4.1); back when released; `bed_off_in_contact` stays a
   setting.
3. **A live mute for the presenter:** one key on the page that silences the bed
   at once — the venue's speakers are unknown, and the bed may have to go
   mid-demo. Cheap; recommended.
4. **The gauge.** The gauge hears only what is played the voices' way
   (`gauge.js` wraps `createBufferSource`): a bed played through an `<audio>`
   element **stays out of the gauge with no extra code**; letting it in is one
   more connection. Recommendation: out — the needle shows the voices.
5. **Which clips may be used, and where they live** — **the one answer that
   changes the build.** A demo set drawn only from the CC0 and CC BY clips (15
   of the 17) can live in the fork beside the story, with a credits list, and
   the installer needs nothing new; #9 (CC BY-NC) and #1 (Sampling+) would need
   a home outside git, like the cast's voices.
6. **Start and end:** the bed fades in at Start (the click that unlocks the
   page's audio), stops on Stop, and fades out when the show ends (the
   switch-off).
7. **Its level against the voices:** the first numbers by ear on the laptop; the
   venue's sound will differ — the live mute and the settings are the safety
   net.
8. **The canned episode (Task 7):** if the page plays it, it has the bed for
   free.
9. **Tests:** the shuffle, the no-repeat guard, the silence timer and the
   state's changes as small pure functions with Node tests, like the page's
   text splitter (`chunks`, `tests/test_show_page.js`).

#### The order proposed (smallest step first)

1. **The first build:** one list, shuffled; mono files with a gain per clip;
   two states (voice / between) with the dip and the rise; silent while
   push-to-talk is held; the live mute; the looks only.
2. **Then, by ear:** the fading, the silences, the crossfade.
3. **Later:** lists per kind of round — and the event sounds (§8.11).

### §8.11 Event sounds — a layer of their own beside the bed (2026-10-01, night)

**The owner (verbatim)**, on §8.10's question 5:

> I mostly agree with you, but there is an angle you are forgetting:
>
> Remember that eventually we want also to have SFX audios for event rounds, and
> the sound of the event cannot just be active in one round or it would be
> strange... The question arises how do we plan to eventually implement the
> event sounds:
>
> * As another type of background noise (replacing the static audios), or,
> * As another audio channel completely independent of the bed channel, this
>   gives us the most flexibility but is the more complex as we have to mix 3
>   sources of audio.... Yet this is my lean.
>
> What do you think about how we position ourselves for the eventual
> introduction of event SFX, and reconcile it with the bed audio.

And, on the documents: "Remember to always save to our documents carrying the
same level of details that you use in this transcript (or even more), the
documents are very important."

#### The facts the answer stands on (the fork at `tz-0.5`)

- **The story has 289 events in 35 themes** (`stories/lab-outbreak/events.yaml`,
  counted), filed by overtone (`positive`, `neutral`, …) then by theme. Each is
  a sentence of free text — *"A fire alarm in the east wing rings once, loud as
  a church bell, and stops."*, *"The calendar in the break room says today is
  someone's birthday."* — with no sound attached and no id.
- **An event comes often:** in a free round, every `event_every` 2 ± 1
  (`event_jitter`) free rounds (`app/config.py`; `_event_due`,
  `app/show/director.py`). It lives in **one round** (`RoundPlan.event`; the
  round's summary carries it). With `fixed_lines` on (the default), the first
  to speak **reads the event word for word as the round's first line**, and the
  rest react.
- **Many events have a natural sound** (an alarm, glass raining down, an
  elevator, a helicopter, a choir, the server fans' howl); **many have none**
  (a birthday on a calendar, a stash of chocolate) — the owner's "some events
  will have many audios to pick from, other will have none" (§8.1).

#### The agent's answer: agreed — a channel of its own; why it costs less than it seems

**The bed and the event sounds are different things in the fiction:**

| Layer | What it is in the story | What changes it | How long |
|---|---|---|---|
| **The bed** | **the radio** — what the receiver does: static, fading, a tuning sweep | the radio's state: a breakdown, a repair, a contact | always there |
| **An event's sound** | **the room** — what happens in the lab, heard through the transmitter: the alarm, the glass, the rotor | an event | its own length, across rounds |

**Why not "another kind of background, replacing the static":** the bed would
stop being the radio. Each time something happened in the lab the static would
vanish — as if the receiver cleared up because a fire alarm rang. And with an
event every 2-3 free rounds, the bed would be replaced most of the time.
Replacing the bed's *list* stays the right tool for **the radio's own states**
(§8.10 question 5: harsher static at the breakdown, sweeps at the repair) —
the radio changing, not the room.

**Why three sources is cheaper than it sounds:** in Web Audio, mixing is not
something we write. Every sound goes through its own **gain node** (a volume
knob the code can turn, with smooth ramps), and every gain node connected to
the speakers is **summed by the browser**. Three sources are three knobs into
the same speakers:

```
voice chunks ──(buffer sources, as today)──────────────────────────► speakers   (+ the gauge's tap)
bed clips   ──<audio>── clip gain ── bed layer gain ───┐
event sound ──<audio>── clip gain ── event layer gain ─┴─ sounds gain ─► speakers
                                                          (the live mute; the dip under a voice)
```

**The real work is the rules, not the mixing** — who dips under whom, when an
event's sound starts, how long it lasts — and those can be added one at a time.
A first set, to tune by ear:

| While… | the bed | an event's sound |
|---|---|---|
| a voice is talking | low | lower, but heard (the alarm still ringing under the line) |
| between rounds | the "between" level | up — the gap of 3.7-4.9 s before the reporter speaks is where the sound is heard best |
| an event's sound is playing | dips a little | — |
| push-to-talk is held | silent | silent |
| the live mute | silent | silent |

**How the event sounds would work, later** (a sketch, to argue over when we get
there, not now):

1. **Which sound:** the story says it — each event (or each theme) may name a
   kind of sound (`alarm`, `glass`, `rotor`…) or none; a kind is a list of clips
   in the pool (`sounds/<source>/<kind>/`), many or none, as the owner said. The
   director picks the clip, as it picks the event, and **sends it to the page at
   the round's start** (in the stream's first message, before the event's
   reading) — the page plays, it does not decide; the same split as the voices
   (the story maps a mood to a clip, the page plays it).
2. **When it starts:** a beat **before** the event is read — the sound happens,
   then someone reports it. The page plays it when the round's first message
   arrives, during the dead air before the first voice.
3. **How long — the owner's point:** **its own length, not the round's.** The
   sound plays to its clip's end, across round boundaries (a siren of 40 s spans
   two or three rounds), up to a maximum, then fades out. A new event's sound
   crossfades over the old one; one event sound at a time.
4. **Through the radio:** the event's sound reaches the audience through the
   lab's transmitter, so it could carry the same coloring as the bed (§8.10,
   question 3's band-pass) — and sit under the static rather than above it.

**How to position ourselves now — the agent's recommendation:** build the bed
**as the first layer of this structure, and nothing more**: one "sounds" gain
for all non-voice sound (the live mute, the dip under a voice), and the bed as
one layer below it, written so that a second layer is a second instance, not a
rewrite. The cost now is close to nothing (a gain node and a little care in
naming); the event layer, its data in the story and its rules come after the
bed works — and, with the deadline seven days away (2026-10-08), most likely
after the demo.

**Open, the owner's:** the bed's other questions (§8.10), one at a time.

### §8.12 The owner's pass over §8.10: decided, and the agent's answers (2026-10-01, night)

**The owner (verbatim)**, opening: "Ok, I feel we are in agreement. Yet, let me
make a quick pass over your decomposition above providing my observations". And,
at the end: "I'll look at the "More questions to settle (my recommendation for
each)" later. This is getting too long." — **§8.10's nine further questions
stay open.**

#### Decided

| §8.10 question | The owner (verbatim) | Decided |
|---|---|---|
| 1. Constantly, or at moments? | "Ok, let's implement "My recommendation: constantly, with the level moving"." | **Constantly, the level moving with the show** |
| 2. Normalize? | "Ok, let's build this: don't change the files. Instead, give each clip one gain number in the list that names the clips. A tool would measure it to bring every clip to a common level, and you can override any number by ear (for example, to leave one clip deliberately louder). The files stay untouched, and what each clip contributes is visible and easy to tune." | **The files untouched; one gain per clip in the list — measured by a tool, overridable by ear** |
| 3. Bitrate | "So let's go with you lean here." | **No bitrate work** — the page loads the clips from the laptop |
| 3. Trimming | "I do not want to lose time manually massaging the files... I am interested in the technical achievements in this project, not in producing studio quality sounds. Unless you can do the trimming automatically, we postpone it!" | **Postponed** (the agent's answer below) |
| 3. The band-pass filter | "This is very interesting! Yet I fear we are ballooning complexity. We could build this, and ydo an A/B test, but in any case it has to be a feature we can switch ON/OFF in the settings." | **Built only as a setting, on or off — an A/B by switching it** |
| 4. The level moving | "Agreed with your agreement 😃 … I agree with your 3 proposals to raise and lower the volume." | **Per round (voice / between), not per clip; dip about 0.5 s, rise about 1.5 s, both settings; the fading** |
| 5. Lists per kind of round | "Agreed. Let's start with one single list for all the show. We can refine this design later." | **One list for the whole show**; named, so more lists later are data (and the event sounds a layer of their own, §8.11) |
| 6. Rotation | "We agree." | **Shuffle; reshuffle when used up; never the same clip across the seam** |

On the fading and its name: "I love your explanation about "fading" and "QSB",
we need a small mention about this in our docs for sure. If e are doing a radio
show, we need to embrace the terminology and learn about the culture." — the
words are below ("Radio words").

#### Still open, with the agent's answers

**3A. Mono — how, with which tool, and where the files go.** The owner (verbatim):
"Mono: yes ... A/ Ok. How do we do this transformation? Do we need a new tool
for that? And where do we keep the modified audio files, we should never
overwrite the originals downloaded from freesound, so we need a new path in my
fielsystem to store the actual files modified for the app to use.... A
gitignored folder inside the TalkWithZombies client folder?"

**The agent's answer: no transformed files at all — the browser does the mono.**
§8.10 gave memory as mono's main reason; that reason went away with the
`<audio>` element (it streams the file instead of decoding it whole). What is
left is the sound — one channel, as from a radio's speaker — and the browser
does that with **one property of the bed's gain node** (`channelCount = 1`,
`channelCountMode = "explicit"`: a stereo clip is mixed down to mono as it
passes). The same goes for the filter: a band-pass is **one more node**
(`BiquadFilterNode`) on the bed's path, in or out by the setting. So the files
the page plays are **the Freesound previews, byte for byte**.

**A tool is still needed** — not to change the audio, but to put the chosen
clips where the app reads them and to measure their gains. It follows the
voices' pattern exactly (`tools/voices/cast.yaml` → `cast_voices.py` →
`~/TalkWithZombies-client/Personas/`):

| Piece | What | Where |
|---|---|---|
| **The list** — the decision, the only file the owner edits | which clips play in the bed (by Freesound id), and an optional gain per clip that overrides the measured one | `tools/sounds/bed.yaml`, in this repository (its history is the record of every past choice) |
| **The tool** | **copies** each listed clip, unchanged, from the pool into the app's folder, measures its average level, and writes a manifest: the file, its length, its gain (measured, or the list's override), its licence and credit line | `tools/sounds/prepare_bed.py`, in this repository |
| **The app's copy** | the clips and the manifest the page reads | **`~/TalkWithZombies-client/Sounds/bed/`** — the owner's idea: a folder inside the client, gitignored by the fork (a `Sounds/` line in its `.gitignore`, beside `Personas/`); the dev checkout gets its own the same way |

**The originals are never touched:** the pool (`zombie-radio-datasets/sounds/`)
stays as downloaded; the app's folder holds copies, and can be wiped and
remade from the list at any time. **A gift of this shape:** the files stay
outside git, so **all 17 clips may be used in the demo**, whatever their
licence (the CC BY-NC and Sampling+ ones included — a meetup talk is not
commercial); the credit lines of the seven that are not CC0 go on a slide, or a
credits note the page can show. To check when built: that the installer (its
`git` task, `force: false`) is not upset by an untracked `Sounds/` folder in the
client before the fork's `.gitignore` names it.

**3. Trimming, automatically?** Only the easy part could be automatic — cutting
silence at a clip's start and end (a level threshold). Choosing the
*interesting* stretch cannot. And it is not needed: the bed fades in and out at
every join (the crossfade) and every silence, so a dull or quiet start is
heard for a second at most, under a fade. **Postponed, as the owner said** — no
trimming at all.

**7. The silences — the owner's question (verbatim):** "So, you recommend: `B.
On a timer: every 30-120 s (random), the bed fades out, the clip pauses, stays
silent for 3-15 s (random), then fades back in where it stopped` This adds
complexity. And how do you pick the slice? Because I do not suppose you want to
always start the slice from the beginning of the audio file, where the least
interesting signal usually is... You will need to make available for the code
the length of each audio file, and be ready to make a seek inside the file to
locate the slice you want... Have you thought this well? Sound very complex for
me..."

**The agent's answer: shape B picks no slice — §8.10 said it too briefly.**
Nothing is cut, chosen or sought: the clip plays from its start to its end, as
it would without silences; a silence only **interrupts** it, like a
pause button. An `<audio>` element remembers where it was paused, so the
silence is:

```
clip #4 playing ─────────────╲ (fade out, 0.5 s)
                    pause()   ▏ … silence of 3-15 s (random) …
                    play()    ▕ the same clip, from the very sample it stopped at
                             ╱ (fade in, 0.5 s) ─────────────── to its end, then the next clip
```

| What shape B needs | How |
|---|---|
| when the next silence comes | a timer, `setTimeout`, with a random delay in the setting's range (30-120 s) |
| the fade out | a gain ramp to 0 on the bed's gain node (`linearRampToValueAtTime`), the same as the dip under a voice |
| the silence | `audio.pause()`, then a second timer of 3-15 s |
| coming back | `audio.play()` — it resumes where it paused — and a gain ramp back up |
| the clip's length | **not needed**; the element plays to the end and says so (its `ended` event), which starts the next clip |
| a seek | **none** |

It is about as small as shape A. **What did need a seek** was a different idea —
§8.10's question 6 option, starting each clip at a random point — and that one
was already left out of the first build. (Even that one is small in the
browser — `audio.duration` is known once the file starts loading, and
`audio.currentTime = x` is the seek — but it stays out.) The decision is the
owner's.

#### Radio words (the owner: "we need to embrace the terminology and learn about the culture")

Radio operators have shared a set of three-letter **Q-codes** since the
radiotelegraph days of the early twentieth century — short codes for the
questions they asked each other most, fast to send in Morse and understood in
any language. Asked with a question mark, a code is a question; sent plain, it
is the answer. Three of them describe exactly what the static bed is made of:

| Code | As a question | In the bed |
|---|---|---|
| **QRN** | "Are you troubled by static?" — natural noise: lightning, the atmosphere | **the bed itself** — the hiss and crackle of the static clips |
| **QRM** | "Is my transmission being interfered with?" — man-made interference: other stations bleeding in | the owner's finds of "radio static of mixed radio stations" (#2, #4, #13), the Morse (#6, #14) — and the "radio bleed" layer of §8.5 |
| **QSB** | "Are my signals fading?" — the signal swelling and sinking as the ionosphere shifts | **the fading** — the bed's slow random ups and downs (§8.10, question 4, refinement 3) |

Ham operators still use them on the air, in Morse and by voice ("lots of QRN
tonight"). The settings may borrow the words when the bed is built (the
fading's settings as `bed_qsb_…`, say) — the owner's call; and a slide for the
talk. *(Decided in §8.13: plain words in the settings; the codes in the docs.)*

### §8.13 The open questions, settled three at a time; the first build's plan (2026-10-01, night)

**The owner (verbatim):** "Ok, I need your help with so many questions. Present
the questions to me in groups of 3." The agent asked them in three groups, each
question with its options and a recommendation; the owner chose one option per
question. The questions and the chosen options, as asked:

**Group 1**

| Question | Chosen | What it means |
|---|---|---|
| "Where should the static bed play?" | **Looks only** (the recommendation) | the bed plays in `old-radio` and `amateur-radio-transmitter`; the plain page stays silent as the working and debugging page; an address switch `?bed=on` turns it on there when wanted |
| "How should the random silences work?" | **B: on a timer** (the recommendation) | every 30-120 s (random) the bed fades out and the clip pauses; after 3-15 s (random) it resumes where it stopped and fades back in — no slicing, no seek, no clip lengths needed (§8.12, question 7) |
| "Do you approve this shape for getting the clips to the app: a list (`tools/sounds/bed.yaml`), a tool that copies the clips unchanged and measures their gains (`tools/sounds/prepare_bed.py`), the copies in `~/TalkWithZombies-client/Sounds/bed/` (gitignored by the fork), mono and the filter done in the browser?" | **Yes, this shape** (the recommendation) | like the voices (`cast.yaml` → `cast_voices.py` → `Personas/`); the originals never touched; the copies can be wiped and remade; all 17 clips usable, since nothing goes into git (§8.12, 3A) |

**Group 2**

| Question | Chosen | What it means |
|---|---|---|
| "What should the bed do during the listener's turn (the contact rounds, when the audience may talk back)?" | **Up, silent while held** (the recommendation) | while the page waits for the listener: the "between" level (atmosphere while the audience thinks); silent while push-to-talk is held, back when released; `bed_off_in_contact` stays a setting to silence the whole contact |
| "Should the page have a live mute for the bed, for the presenter at the venue?" | **Yes, one key** (the recommendation) | one keyboard key on the page turns the bed (and later the event sounds) off and on at once, with a short fade; invisible to the audience. The key proposed: **M** — the page already uses **Space** for push-to-talk (`static/show/show.js`, its `keydown`/`keyup` listeners) |
| "Should the looks' gauge (the magic eye and meters) react to the bed?" | **Out: voices only** (the recommendation) | the needle moves only with the voices, as today; no code — a bed played through an `<audio>` element stays out of the gauge by itself |

**Group 3**

| Question | Chosen | What it means |
|---|---|---|
| "How should the bed start and end with the show?" | **Fade in, stop, fade out** (the recommendation) | fades in at Start (the click that unlocks the page's audio); stops at once on Stop (and resumes on Resume); fades out over a few seconds when the show ends (the switch-off) |
| "Should the bed's settings borrow the radio words?" | **Plain words** (the recommendation) | `bed_fading_db`, `bed_fading_every_s` and so on; the Q-codes explained in the docs and on a slide, not in the settings' names |
| "When should the static bed be built, against the rest of the board (the 3090, names-only A, the canned episode, the talk) with the deadline on 2026-10-08?" | **Now, first build only** (offered without a recommendation) | next: the list, the tool and the first build in the fork; the fading, the silences and the filter after a first listen; then the rest of the board |

**Not asked — the agent's working assumptions** (§8.10's remaining three, which
are not choices): the bed's level against the voices is set **by ear** on the
laptop, the venue's sound handled by the live mute and the settings (§8.10,
7); the canned episode, if the page plays it, has the bed for free (§8.10, 8);
the bed's logic is written as small pure functions with Node tests (§8.10, 9).

#### The whole design, as decided (§8.8 and §8.10-§8.13 together)

- **What:** a shuffled list of radio static clips, played constantly, quietly,
  under the show — **the static bed**, the first layer of a small structure
  that event sounds can join later as a second layer (§8.11).
- **The clips:** the Freesound previews, unchanged; one list for the whole show
  (all 17 to start; the owner prunes by ear); one gain per clip, measured to a
  common level and overridable in the list.
- **The path:** `tools/sounds/bed.yaml` (the list) → `tools/sounds/prepare_bed.py`
  (copies, measures, writes a manifest) → `~/TalkWithZombies-client/Sounds/bed/`
  (gitignored by the fork) → the app serves it → the page plays it.
- **In the browser:** each clip through an `<audio>` element (streamed, not
  decoded whole) → its clip gain → the bed's gain (mixed down to mono there) →
  the "sounds" gain (the live mute) → the speakers; the gauge not tapped.
- **The level:** two states by round — **voice** (low) from the round's first
  clip to the end of its playing, **between** (higher) until the next round's
  first clip — a dip of about 0.5 s and a rise of about 1.5 s; during the
  listener's turn the "between" level; **silent while push-to-talk is held**.
- **The order:** shuffle; reshuffle when used up; never the same clip across
  the seam.
- **Later, after a first listen:** the fading (random slow ups and downs), the
  silences on a timer (shape B), the crossfade at the joins, the AM filter as a
  switch.
- **Where:** the looks only (`?bed=on` for the plain page). **Start and end:**
  fade in at Start, stop on Stop, fade out at the show's end. **The live mute:**
  the M key. **The gauge:** voices only. **The settings:** in the fork's
  `show:` section, plain names, sent to the page in the start reply.
- **No trimming; no bitrate work; no normalization of the files.**

#### The first build's plan (to be approved before it starts)

**Step 1 — zombie-radio, this branch (`alfre2v/sound-effects`):**

1. `tools/sounds/bed.yaml` — the list: the pool's folder, the app's folder
   (`~/TalkWithZombies-client/Sounds/bed`), the common level, and the clips by
   Freesound id (all 17 to start), each with an optional `gain_db`.
2. `tools/sounds/prepare_bed.py` — for each listed clip: find it in the pool by
   its id, copy it unchanged, measure its average level (decoded with macOS's
   built-in `afconvert`, as `cast_voices.py` does — no new dependency), and
   write `bed.json` beside the copies: the file, its length, its gain (measured,
   or the list's), its licence class and credit line. A dry run by default; it
   removes from the app's folder only the files it wrote before.
3. Run it (dry run → the owner's approval → for real) into the installed client
   and into the dev checkout.

**Step 2 — the fork, a new branch (`alfre2v/static-bed`):**

1. `.gitignore`: `Sounds/`, beside `Personas/`.
2. **Settings** (`ShowConfig`, plain names, the first build's only): `bed`
   (on/off), `bed_volume_voice`, `bed_volume_between`, `bed_dip_s`,
   `bed_rise_s`, `bed_off_in_contact` — sent to the page in the start reply.
3. **Serving the bed:** the app serves `Sounds/bed/` (the clips and
   `bed.json`); no `bed.json`, no bed — the show runs as today.
4. **The page:** a new module `static/show/bed.js` — the sounds gain, the bed
   layer, the shuffle with its seam guard, the states (voice, between,
   listening, muted), short fades at the joins; hooks in `show.js` (the round's
   first clip, the end of its playing, push-to-talk held and released, Start,
   Stop, the show's end, the M key); loaded by the looks, and by the plain page
   only with `?bed=on`.
5. **Tests:** pytest (the settings, the serving, the start reply) and a Node
   test for the shuffle and the states.
6. **Runbook:** the fork's `docs/runbooks/show-page.md`, a section "The static
   bed" — the settings, the M key, `?bed=on`, how the clips get there.

**Step 3 — listen** (the owner, with the box up): tune the numbers by ear; then
the second build (the fading, the silences, the crossfade, the filter switch)
and a release.

### §8.14 Step 1 built: the list, the tool, the clips in the app (2026-10-01, night)

**The owner:** "commit, then start step 1" — §8.10-§8.13 committed; then step 1
of §8.13's plan, in this repository.

#### The two files

*(Changed in §8.16: which clips play, and a change of level by ear, moved to the
story — the fork's `stories/lab-outbreak/bed.yaml`; this list lost its
`gain_db`, and `bed.json` its `gain_from`, its `gain_db` renamed
`measured_gain_db`. Below, the state of step 1.)*

- **`tools/sounds/bed.yaml` — the list, the only file the owner edits:** the
  pool (`../zombie-radio-datasets/sounds/freesound`), the app's folder
  (`~/TalkWithZombies-client/Sounds/bed`), the common level (`loudness_dbfs:
  -20`), and the clips by Freesound id — all 17 to start. A clip may carry its
  own gain, which replaces the measured one: `- {id: 11859, gain_db: -3}`.
- **`tools/sounds/prepare_bed.py` — the tool** (run with `uv run`, for PyYAML,
  like `cast_voices.py`). For each listed id: it finds the clip in the pool
  (`<pool>/<kind>/<id>-*.mp3`), checks the file's SHA-256 against its `.json`,
  measures its level on the **mono mix the page will play**, and computes the
  gain to `loudness_dbfs`. With `--write` it **copies each clip unchanged**
  into the app's folder (skipping a copy already identical) and writes
  `bed.json` beside them (written to `bed.json.part` first, then renamed).
  Without `--write`, a dry run. It removes only files that an earlier
  `bed.json` listed and the list no longer names; nothing else in the folder is
  touched. `--app` points it at another folder (the dev checkout's).

**`bed.json`** — what the page will read: when it was prepared, the list it came
from, the common level, and per clip: `file`, `id`, `name`, `author`, `page`,
`seconds`, `channels`, `rms_dbfs` and `peak_dbfs` (of the mono mix), `gain_db`
and `gain` (the same as a factor, for the page's gain node), `gain_from`
(`measured` or `list`), `licence`, `licence_class`, `credit`. One clip's entry,
as written:

```json
{
 "file": "730109-shortwave-radio-static-with-indistinguishable-foreign-chatte.mp3",
 "id": 730109,
 "name": "Shortwave Radio static with indistinguishable foreign chatter and static",
 "author": "-CASK-",
 "page": "https://freesound.org/people/-CASK-/sounds/730109/",
 "seconds": 172.14,
 "channels": 2,
 "rms_dbfs": -29.4,
 "peak_dbfs": -7.93,
 "gain_db": 9.4,
 "gain": 2.9521,
 "gain_from": "measured",
 "licence": "CC BY 4.0",
 "licence_class": "cc-by",
 "credit": "\"Shortwave Radio static with indistinguishable foreign chatter and static\" by -CASK- (https://freesound.org/people/-CASK-/sounds/730109/), licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)"
}
```

#### A trap found: `afconvert -c 1` keeps the left channel, it does not mix

To measure a clip, the tool must first turn the MP3 into samples Python can
read — macOS's `afconvert` (built in; `cast_voices.py` uses it). The obvious
call asks for one channel (`-c 1`), expecting the two to be mixed. **They are
not: `afconvert -c 1` keeps the left channel and drops the right.** Found by a
test before relying on it — a 440 Hz tone at half volume, put on one side of a
stereo MP3 (ffmpeg's `pan` filter), then decoded with `afconvert -c 1`:

| Test clip | `afconvert -c 1` gave | Meaning |
|---|---|---|
| the tone on the **left** only | −27.36 dB — the tone's full level (the tone alone: −27.1 dB) | the left channel, kept whole |
| the tone on the **right** only | **silence** (the RMS was 0) | the right channel, dropped |

(Two real clips, #15 and #4, had shown nothing: their two channels are nearly
alike, so left-only and the mix measure the same — −10.98 / −11.0 dB and
−29.38 / −29.4 dB against ffmpeg's mix-down. Only a one-sided signal tells.)

Measured that way, a clip with more static on the right would measure too
quiet and get too much gain, and a clip with sound only on the right would
measure as silence — while the page plays **the mix of both channels**
(§8.12, 3A: the browser mixes a stereo clip down to mono as it plays).

**How the tool avoids it** (`measure()` in `tools/sounds/prepare_bed.py`):

1. **Decode without `-c 1`**, keeping every channel —
   `afconvert -f WAVE -d LEF32 <clip> <temp>.wav` changes only the format (MP3
   → 32-bit float WAV), not the number of channels. The WAV lives in a
   temporary folder and is deleted after measuring; it is never copied
   anywhere.
2. **Split the channels.** A stereo WAV stores its samples interleaved, left
   and right in turn — `L0 R0 L1 R1 L2 R2 …`; `samples[0::2]` is every left
   sample, `samples[1::2]` every right one
   (`frames = [samples[c::channels] for c in range(channels)]`).
3. **Mix them as the browser does** — the average at each instant,
   `(L0+R0)/2, (L1+R1)/2, …`
   (`mix = array.array("f", (sum(frame) / channels for frame in zip(*frames)))`);
   a mono clip is used as it is.
4. **Measure that mix** — its RMS and peak — and the gain to −20 dBFS.

**Checked** on test tones through `measure()` itself:

| Test clip | The tool's mix | Why |
|---|---|---|
| the tone on **both** channels | −27.36 dB | (L + L) / 2 = L: the tone itself |
| the tone on the **left** only | **−33.38 dB** | (L + 0) / 2 = half the amplitude = **6.02 dB less** — exactly |

**The tool does not make the clips mono:** the copies in the app are the
original MP3s, byte for byte; mono happens only in the browser, as decided. The
tool measures that mix in advance, so the gain in `bed.json` fits what is
heard.

**The mono mix against §8.10's table:** §8.10's loudness table measured the
stereo files as they are (ffmpeg's `volumedetect`, both channels together).
For four clips whose channels differ, the mono mix is about 3 dB quieter — the
figure that counts:

| # | Clip | §8.10 (stereo as is) | The mono mix |
|---|---|---|---|
| 2 | Handheld radio music and static | −21.1 dB | −24.5 dB |
| 7 | Full radio sweep | −16.5 dB | −19.5 dB |
| 8 | Vintage Radio Tuning 5 | −25.7 dB | −28.7 dB |
| 15 | Radio — Generative Sound by Glorb | −11.0 dB | −13.9 dB |

#### The owner's question: are the cast's voices hit by the same trap?

**The owner (verbatim):** "Are you sure about this "since EARS recordings are
already mono"... I thought the EARS recording where all studio quality and
therefore I doubt they are mono. Instead I seem to remember that the agent
performed some transformation to make them mono, maybe creating an error by
using afconvert without noticing. We need to research this question."

**Researched — the EARS recordings are mono at the source; the voices are not
affected:**

| What was checked | Result |
|---|---|
| all **612** EARS files on disk (`zombie-radio-datasets/ears/`), their WAV headers | **612 × mono** — 32-bit float, 48,000 Hz, 1 channel |
| **the source:** p007's `emo_neutral_sentences.wav`, its header read straight from EARS's zip on GitHub (with `fetch_ears.py`'s range reader: 5 range requests, 81 KB read, nothing saved) | **mono** (format 3 = float, 1 channel, 48,000 Hz, 32-bit); the zip member 1,740,754 bytes, the file on disk 1,740,754 bytes — `fetch_ears.py` copies it out of the zip unchanged (`zf.open` → `shutil.copyfileobj`, the zip's CRC checked) |
| `cast_voices.py`'s reader (`read_wav`, `tools/voices/cast_voices.py:48`) | it **refuses** anything but mono 32-bit float, with an error ("expected mono 32-bit float…"): a stereo file would have stopped the cast loudly, never passed silently |
| the cast's **100** `Personas/*/ref*.wav` in the installed client | **100 × mono**, 16-bit PCM, 24,000 Hz — as the cast writes them |

**Why studio quality is still mono:** EARS's quality is elsewhere — an anechoic
chamber (no echo), 48 kHz, 32-bit float. Speech datasets are recorded with one
microphone in front of the speaker; a second channel would add nothing for one
voice. (EARS's README does not name the channel count; the files do.) So the
`afconvert … -c 1` in `cast_voices.py` only ever receives mono — the trap is
real only for stereo input, like the Freesound clips.

#### The dry run, then the write (approved: "yes, write into both folders")

The dry run measured the 17 clips (24.1 minutes of audio) in 13 seconds. The
real write, 2026-10-01 at 23:39 CDT — into the installed client, then into the
dev checkout (`--app`); the client's output, in full:

```
pool /Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/sounds/freesound
app  /Users/alfredo/TalkWithZombies-client/Sounds/bed
loudness -20 dBFS (the mono mix's average level)

  11859  analog_noise_arped_radio_static.wav         11.7 s  2 ch  RMS  -17.4  peak   0.0  gain   -2.5 dB (measured)  Sampling+ 1.0
 719588  Handheld radio music and static             41.8 s  2 ch  RMS  -24.5  peak  -6.4  gain   +4.5 dB (measured)  CC BY 4.0
 615189  radio11.wav                                 14.1 s  2 ch  RMS  -21.2  peak  -3.3  gain   +1.2 dB (measured)  CC BY 4.0
 730109  Shortwave Radio static with indistinguis   172.1 s  2 ch  RMS  -29.4  peak  -7.9  gain   +9.4 dB (measured)  CC BY 4.0
 625095  radio_static_01.flac                        84.7 s  1 ch  RMS  -22.3  peak  -0.3  gain   +2.3 dB (measured)  CC0 1.0
  34418  morse static.wav                             4.9 s  2 ch  RMS  -31.1  peak  -7.9  gain  +11.1 dB (measured)  CC BY 4.0
 396902  Full radio sweep.wav                       296.8 s  2 ch  RMS  -19.5  peak  -0.1  gain   -0.5 dB (measured)  CC0 1.0
 652596  Vintage Radio Tuning 5.WAV                 110.8 s  2 ch  RMS  -28.7  peak  -6.1  gain   +8.7 dB (measured)  CC0 1.0
  30302  CS3B_beacon.wav                             11.8 s  1 ch  RMS  -15.2  peak  -5.8  gain   -4.8 dB (measured)  CC BY-NC 4.0
 722884  harsh analog fm radio flips                 21.3 s  2 ch  RMS  -19.9  peak  -0.8  gain   -0.1 dB (measured)  CC0 1.0
 557532  radio tuning fm.mp3                        165.3 s  2 ch  RMS  -26.5  peak  -4.5  gain   +6.5 dB (measured)  CC0 1.0
 624412  Radio Music - A MakeNoise Morphagene Ree   156.2 s  2 ch  RMS  -17.0  peak  -0.2  gain   -3.0 dB (measured)  CC0 1.0
 255775  S06Russian.wav                             110.0 s  1 ch  RMS  -25.4  peak  -8.6  gain   +5.3 dB (measured)  CC BY 3.0
 343740  Radio transmission morse code @4606.2kHz    76.3 s  1 ch  RMS  -17.3  peak   0.0  gain   -2.7 dB (measured)  CC0 1.0
 855480  Radio — Generative Sound by Glorb          120.0 s  2 ch  RMS  -13.9  peak  -0.1  gain   -6.0 dB (measured)  CC0 1.0
 658932  Dial-up_sound.mp3.flac                      19.3 s  1 ch  RMS  -18.9  peak  -3.2  gain   -1.1 dB (measured)  CC0 1.0
 546450  The Sound of dial-up Internet               28.7 s  2 ch  RMS  -26.4  peak  -8.1  gain   +6.4 dB (measured)  CC0 1.0

17 clips, 24.1 minutes, 28.05 MB

written: 17 clips and bed.json in /Users/alfredo/TalkWithZombies-client/Sounds/bed
```

**The gains run from −6.0 dB** (#15, the loudest) **to +11.1 dB** (#6, the
quietest). A gain of +11 dB alone would push a clip's peaks past full scale,
but the bed is then multiplied by its own volume — 0.05-0.15 in the settings
draft, −26 to −16 dB — so what reaches the speakers stays far below it.

**Checked after the write**, in both folders:

- 17 clips and `bed.json`, nothing else; 27 MB (`du -sh`).
- **Each copy identical to the pool's file**, byte for byte (Python's
  `filecmp.cmp`, `shallow=False`): 17 of 17, in both.
- `bed.json`: 17 clips, `loudness_dbfs` −20; prepared 23:39:46 (the client)
  and 23:39:59 (the dev checkout).
- **The checkouts:** right after the write, in the installed client (still at
  `tz-0.5`) and in the dev checkout, `Sounds/` showed as untracked
  (`?? Sounds/`). Ansible's git module ignores untracked files
  (`has_local_mods` filters the `??` lines of `git status --porcelain`), so
  `make client-mac` would not be upset by the folder.
- **Ignored at once, on the owner's word** (verbatim: "Why don't you gitignore
  the audio file now. If I say commit you may commit them."), two ways, one per
  checkout:
  - **The dev checkout:** the fork's branch **`alfre2v/static-bed`** created
    from `master` (step 2's branch), and `Sounds/` added to the fork's
    `.gitignore` beside `Personas/` (step 2's first item) — git ignores the
    folder from that moment, before any commit (`git check-ignore -v`:
    `.gitignore:11:Sounds/`).
  - **The installed client:** **not** its `.gitignore` — a tracked file; editing
    it would make the clone "locally modified", and the installer's git task
    (`force: false`) would then fail. Instead `Sounds/` went into
    `.git/info/exclude`, git's local ignore list, which is not tracked and
    which the installer never reads (`git check-ignore -v`:
    `.git/info/exclude:7:Sounds/`). Once the client moves to a release whose
    `.gitignore` names `Sounds/`, the line there is redundant and harmless.
  - **zombie-radio:** no audio file anywhere in its tree (the clips live in
    `zombie-radio-datasets/` and in the fork's `Sounds/`).
- **A second run** copies nothing (each copy's SHA-256 already matches) and
  rewrites only `bed.json` (its `prepared` time).

```bash
# Prepare the bed: a dry run (the clips, their mono-mix levels and gains), then the write
uv run python tools/sounds/prepare_bed.py
uv run python tools/sounds/prepare_bed.py --write
# The same into the dev checkout of the fork
uv run python tools/sounds/prepare_bed.py --write --app /Users/alfredo/workspace/hackTNT_2026/TalkWithZombies/Sounds/bed
```

**Next — step 2, the fork** (§8.13): a new branch `alfre2v/static-bed`.

### §8.15 Step 2 built: the static bed in the fork (2026-10-01, night)

**The owner:** "commit, then start step 2" — step 1 committed in this
repository (`0ac89d5`); step 2 built in the fork, on
`alfre2v/static-bed` (from `master` at `tz-0.5`). Nothing committed in the
fork yet.

#### A correction first: the show has no end

§8.13's group 3 offered "fade out over a few seconds when the show ends (the
switch-off)", and the owner chose it. **Wrong premise, the agent's:** the
Switch-off only turns the lab's **receiver** off — the director's own words
(`app/show/director.py`, its docstring): "after enough silences in a row a
Switch-off turns the receiver off by choice. Both return the show to
Broadcast". The broadcast goes on; **the show runs until Stop.** So the bed
rises from silence at Start and Resume and pauses at once on Stop — the
owner's choice — and there is no end to fade out at.

#### What was built (the fork, uncommitted)

| File | What |
|---|---|
| `.gitignore` | `Sounds/`, beside `Personas/` (§8.14: the dev checkout ignores it from then) |
| `app/config.py` | six settings in `ShowConfig`, plain names (§8.13): `bed` (on by default), `bed_volume_voice` 0.05, `bed_volume_between` 0.15, `bed_dip_s` 0.5, `bed_rise_s` 1.5, `bed_off_in_contact` false — with their comment; and `get_bed_directory()`, `<project root>/Sounds/bed` |
| `app/show/bed.py` (new) | reads `bed.json`: the clips the disk holds, each `{file, gain}`; a missing or broken manifest, or an entry with an unsafe name, a bad gain or no file, gives fewer clips or none — logged, **never a failed start**; `clip_path()` serves only a file the manifest lists and the folder holds |
| `app/models.py` | `ShowBedClip`, `ShowBed`; `ShowStartResponse.bed` (`null` when `bed` is off or no clip is there) |
| `app/routers/show.py` | the start reply carries the bed (the clips and the `bed_*` settings without their prefix); **`GET /api/show/bed/{name}`** serves a clip (a `FileResponse`: range requests answered, as an `<audio>` element asks); `GET /show` passes `?bed=on` to the plain page |
| `templates/show.html` | `bed.js` only with `?bed=on` — the plain page unchanged otherwise |
| `templates/show_design.html` | `bed.js` in every look, after `gauge.js`; not with `&mock=1` |
| `static/show/bed.js` (new) | the bed in the page (below) |
| `tests/test_show_bed.py` (new), `tests/test_routers_show.py`, `tests/test_show_config.py` | the manifest's reading, the start reply, the clip route, the pages, the settings' defaults and bounds |
| `tests/test_show_bed.js` (new) | the page's bed in plain Node (below) |
| `AGENTS.md` | the API table (the start reply's fields; the new route — `tests/test_docs.py` checks it), the show page's files (`bed.js`), the Node tests to run |
| `docs/runbooks/show-page.md` | a section "The static bed", a row in the settings table, an entry in "When something looks wrong" |

**How the page's bed follows the show** (`static/show/bed.js`): like
`gauge.js`, it is loaded after the page's own scripts and **wraps two of
their functions from outside** — `show.js` is not edited. `setState` says what
the show is doing; `setReceiver` whether the receiver is on. The level for
each state of the page (`bedLevel()`):

| The page's state | When | The bed |
|---|---|---|
| `thinking` | waiting for the next round | `volume_between` (0.15) |
| `on air` | from the round's first voice clip until the next `thinking` | `volume_voice` (0.05) |
| `listening` | the window open, waiting for the press | `volume_between` |
| `recording` | push-to-talk held | **0**, in 0.15 s — the clip keeps playing silently, so letting go resumes it in place |
| `hearing` | Whisper transcribing | `volume_between` |
| `stopped`, `error`, `idle` | the show not running | **paused** at once, level 0; the next state rises from silence |
| any running state, with `off_in_contact` and the receiver on | — | 0 |

A dip takes `dip_s`, a rise `rise_s` (linear ramps on the bed's gain, from
wherever it is). The clips: `bedShuffle()` — every clip once per pass, the
first of a new pass never the clip that just ended; a clip that ends gives way
to the next; a clip that fails to load is skipped; when every clip fails in a
row, the bed gives up for the page (logged). The graph: `<audio>` element →
the clip's gain (its `gain` from `bed.json`, faded in over 0.3 s at each new
clip) → **the bed's gain, one channel** (`channelCount` 1, `explicit`,
`speakers`: the browser mixes a stereo clip to (left + right) / 2) → **the
"sounds" gain** (the M key's mute, 0.3 s; the slot of §8.11's future event
layer) → the speakers. The gauge's tap wraps only `createBufferSource`, so the
bed never reaches it.

**Three numbers are constants in `bed.js`, not settings** (`BED`: the silence
on the press 0.15 s, a clip's fade-in 0.3 s, the mute's fade 0.3 s) — like
`player.js`'s pauses (`VOICE`) and `gauge.js`'s (`GAUGE`). The owner's house
rule is "every number is a setting"; **the owner's call** whether these three
become settings too.

**`bed: true` by default** — the agent's choice, to confirm: the defaults are
the demo's configuration, so once released the installed client plays the bed
in the looks (its `Sounds/bed/` is prepared); `bed: false` under `show:`
turns it off.

#### Checked

- **The tests:** pytest **1232 passed** (1210 at `tz-0.5`: 22 new — the
  manifest's reading 6, the start reply 3, the clip route 4, the plain page
  1, the settings' bounds 8; extended: the defaults, the designs' and the mock's
  pages); Node
  `test_show_page.js` 42, `test_persona_form.js` 17, `test_tts_settings.js`
  91, `test_show_gauge.js` 8, and **`test_show_bed.js` 16** (the shuffle, the
  levels, the wiring, the levels following the states, Stop and Resume,
  `off_in_contact`, the clips' turns and failures, a new run, the M key, the
  gauge never tapping it, the plain page's scripts untouched).
- **The tests catch a wrong bed:** two mutations of `bed.js` (in a copy
  backed up in the scratchpad, restored and `cmp`-identical) — the seam guard
  removed, and the bed left at `volume_between` while recording — each failed
  2 of the 16 tests.
- **The fork's style:** no added code line over 120 characters, no en dash.
- **The real server** (the dev checkout, port 8010; the tunnel down, so no
  model): the start reply carried **17 clips** and the settings; a clip served
  whole (200, `audio/mpeg`, 105,414 bytes — the file's size), a range of it
  (206, 1,024 bytes), an unlisted name refused (404).
- **A real browser** (the app's built-in Chromium, `?design=old-radio`, Start
  pressed): the bed wired into the page's audio, the first clip loaded
  (`readyState` 4 — decoded), its gain 2.95 (+9.4 dB, #4's); the first round
  failed (no model), the page went to `error`, and the bed paused, as it
  should. Then, **muted with the M key** (nothing reached the speakers), the
  states driven by hand:

| Step | Measured |
|---|---|
| `thinking`, 2.5 s | playing; the clip advanced 2.50 s; the bed's gain at **0.15** |
| `on air`, 0.8 s later | the bed's gain at **0.05** |
| `recording`, 0.4 s later | the bed's gain at **0**; the clip still playing |
| `stopped` | paused at 3.70 s; gain 0 |
| the bed's gain node | `channelCount` 1, `explicit`, `speakers` |

  The only console error: the round's "All connection attempts failed" (no
  model). The dev server stopped after; the checks left three short runs in
  the dev checkout's `runs/` (gitignored): `2026-10-01T23-52-08`,
  `23-52-19`, and one more for the runbook's example output.

#### Next

**Step 3 — listen** (§8.13): with the box up and the tunnel open, a show in a
look, by ear — the two levels, the dip and the rise, the clips (which to keep,
which gain to change in `tools/sounds/bed.yaml`); the second build after
(the fading, the silences on a timer, the crossfade, the AM filter as a
switch); then a release.

### §8.16 The clips switched on and off in the story; which clip plays, in the console (2026-10-02, after midnight)

**The owner (verbatim):**

> (1) A mechanism for me to easily enable/disable bed audios.
> Initially I thought we should add a new key under each audio in bed.json:
> `enabled: true|false` so I can easily activate the audios I like....
> But now I do not think that `Sounds/bed/bed.json` fits the role of a place to
> add configurations, you now add there a lot of parameters that will change the
> way the app runs (gains). I feel we should have a yaml equivalent of this
> bed.json inside `stories/lab-outbreak/` maybe `stories/lab-outbreak/bed.yaml`.
> but at the same time, the bed audio files are ignored, so it may not fit the
> pattern after all. I am torn here. What do you recommend?
>
> (2) An easy way for me to know what bed audiofile is playing (maybe when debug
> is on, print the name of the bed audio playing to the console?)

And: "I wired the hosts.yml and made the tunnel up, but let's hold the tests
until we have discussed this two items." With two questions — "Did you
already build the whole thing? I do not think so, right?" and "Did you already
add the M shortcut to mute/unmute the bed audio play?" — the agent's answers:
step 2's first build was built in full (uncommitted); the second build (the
fading, the silences, the crossfade, the filter) was not; the M key was built
and tested.

#### The agent's answer to (1): facts apart from decisions

| | What it holds | Who writes it | Where |
|---|---|---|---|
| **Facts about the files** | which files are there, their length, their measured level, the gain that evens them out, the licence, the credit | the tool, by measuring; never edited by hand | `Sounds/bed/bed.json`, beside the files it describes (as `ref.source` in `Personas/`) |
| **Decisions about the show** | which clips play, and a change of a clip's level by ear | the owner | the story, in git |

The measured gain **is** a fact — like a clip's length, a measurement of the
file; the owner's "a touch quieter" is a decision. **The doubt — a committed
story naming files that git ignores — is already the pattern:** the story's
`overtones.yaml` names `ref-fear.wav` and the rest, which live outside git in
`Personas/`. Recommendation: **`stories/lab-outbreak/bed.yaml`**, as the owner
proposed — read at every Start, so a change plays at the next Start, with no
restart; a clip enabled but not on disk skipped and logged; no file, every
clip on disk plays; `gain_db` added to the measured gain; zombie-radio's
`tools/sounds/bed.yaml` keeps only what to copy into the app, its `gain_db`
gone.

**The owner (verbatim):** "Agreed in your proposal, with one small change: Like
in overtones, I propose we use the full audio filename (instead of just the
id) … I think that would make it easy for me to recognize from the log
messages on debug what is the actual file that is playing." — the owner's
example wrote the key as `id:` with the file name as its value; the agent
named the key **`file:`** (the value is a file name, and `bed.json` calls the
same thing `file`), and said so.

#### The agent's answer to (2): the console, with debug on

With `show.debug` on, a line in the browser's console each time a clip starts —
its place in the pass, its file, its gain in dB — and at each new shuffle and
each press of the M key; nothing with debug off. (Not the round's debug line: a
clip spans rounds.) **The owner:** "Agreed." Then: "Build these two small
additions."

#### What was built

**The fork** (`alfre2v/static-bed`, uncommitted):

- **`stories/lab-outbreak/bed.yaml`** (new) — all 17 clips, `enabled: true`,
  each with a comment above it (Freesound's name, the licence, the length),
  generated from the real `bed.json`, no name typed by hand:

  ```yaml
  clips:
    # analog_noise_arped_radio_static.wav (Sampling+ 1.0, 12 s)
    - file: 11859-analog-noise-arped-radio-static.mp3
      enabled: true
      gain_db: 0
    # Handheld radio music and static (CC BY 4.0, 42 s)
    - file: 719588-handheld-radio-music-and-static.mp3
      enabled: true
      gain_db: 0
  ```

  (The comments sit above the entries: beside them, the lines ran past the
  fork's 120 characters.) **Then, the owner (verbatim):** "Please expand the
  yaml list items in bed.yaml to each item use several lines, instad of the
  short one line version `{...}`." and "What is the neutral value of gain_db?
  (The one that does nothing to the signal). Is it 0 or 1? I think we should
  explicitly add the gain_db key to each item already with the neutral
  value." — **0**: `gain_db` is in decibels, and the app multiplies the
  measured gain by 10^(gain_db / 20); 10⁰ = 1, nothing changes (−3 dB ≈ ×0.71,
  a little quieter; −6 dB ≈ ×0.50, half the amplitude; +6 dB ≈ ×2.0). The 1 is
  the neutral *factor* — `bed.json`'s `gain`. The file was regenerated as above
  — one key per line, `gain_db: 0` on all 17 — and its header explains the
  three keys; it loads as 17 clips, all enabled, all at 0 dB.
- **`app/show/story.py`** — `BedClip(file, enabled, gain_db)`; `Story.bed`
  (`None` without the file); `_load_bed()`: `clips` a list; `file` a plain clip
  name (the same pattern the clip route checks); `enabled` true or false
  (default true); `gain_db` a number within ±40 dB (default 0); **any other
  key fails**, so a misspelled `enable: false` is never silently ignored; a
  clip named twice fails. A malformed `bed.yaml` refuses the Start (HTTP 422,
  the line at fault), like any broken story file.
- **`app/show/bed.py`** — `bed_play_list()`: every clip on disk when the story
  has no `bed.yaml`; else the story's enabled clips, in its order, each gain
  multiplied by `10^(gain_db / 20)`; a clip enabled but not on disk skipped
  with a warning.
- **`app/routers/show.py`** — the start reply's bed uses it.
- **`static/show/bed.js`** — `bedLog()` (only with the run's `debug`),
  `bedDb()` (a gain as signed dB); the lines: `Show: bed shuffled: a new pass
  of N clips`, `Show: bed clip K of N: <file> (gain ±X.X dB)`, `Show: bed
  muted (M)` / `unmuted (M)`.
- **Tests:** the story's `bed.yaml` (read when present, 12 malformed cases),
  the play list (4), the start reply (the story's choice and gains, read at
  every Start, a malformed file refused); the Node tests: `bedDb`, the console
  lines with debug on, silence with debug off. The router tests write their
  own `bed.yaml` into the run's copy of the story, or remove it — **never the
  shipped mapping** (the owner's rule).
- **Docs:** `docs/runbooks/show-page.md` ("Which clips play is the story's
  choice", "Which clip is playing", the troubleshooting line); `AGENTS.md`
  (the start reply).

**This repository** (`alfre2v/sound-effects`, uncommitted):
`tools/sounds/bed.yaml` lists only Freesound ids (its header points to the
story); `prepare_bed.py` takes no `gain_db` (an entry that is not an id stops
it, naming the story's file), and `bed.json` lost `gain_from` and renamed its
`gain_db` to **`measured_gain_db`** — so the story's `gain_db` (by ear) and the
manifest's (measured) are never confused. Re-run with `--write` into both
folders (2026-10-02, 00:19 CDT): nothing copied, `bed.json` rewritten; checked
— 17 clips each, clip 730109's `measured_gain_db` 9.4 and `gain` 2.9521.

#### Checked

- The fork: pytest **1252 passed** (1232 before: 20 new — the story's
  `bed.yaml` 13, the play list 4, the start reply 3); Node `test_show_page.js`
  42, `test_persona_form.js` 17, `test_tts_settings.js` 91, `test_show_gauge.js`
  8, **`test_show_bed.js` 19** (3 new). No new code line over 120 characters,
  no en dash.
- The runbook's console lines are labelled as the lines' **form** (clip
  730109's file and gain as `bed.json` gives them) — not yet a capture from a
  real run; the owner's listening (step 3) will give one.

**Next:** step 3, the owner's listening, with the tunnel up (the owner wired
`hosts.yml` for it — never staged).

### §8.17 Step 3, the first listen; the volume's scale (2026-10-02, night)

Committed (the fork's `c5288bf`, this repository's `5db744c`) and opened as
alfre2v/TalkWithZombies#10 and alfre2v/zombie-radio#22 (the owner: "Let's
open the PRs too, I would like to review the diffs on github too."). The dev
server on port 8010 with `debug: true` added under `show:` (the dev
checkout's `settings.yaml` backed up in the scratchpad, to restore with
`cmp`); the tunnel probed (200 on all three; `/props`: `n_ctx 32768`, one
slot).

**The owner, listening (verbatim):** "I am testing the audio. Man it's
amazing." Then: "Let's keep the settings as they are. If anything I think I
will end up lowering the bed volume in general... turns out listening to
static is annoying... even on purpose... 😃 So, technically the results are
very impressive... But for my ear the static is very annoying... Regardless,
let's leave the volume as it is."

**The volume moving with the voices — already built** (the owner asked):
0.15 while the page waits, 0.05 from a round's first voice clip to the end of
its playing, a dip over 0.5 s and a rise over 1.5 s, silent while push-to-talk
is held — per round, not per line, so it does not pump in the 80-250 ms gaps
between chunks and lines. From 0.15 to 0.05 is a third of the amplitude,
−9.5 dB: audible, gentle by design. **Not built yet:** the random brief ups
and downs (the fading, QSB) — the second build.

#### The volume's scale

**The owner (verbatim):** "So, explain the "Bed level" scale that we have in
our settings. This is the volume control. Right? … Is this in decibels? If I
wanted to lower the volume of all the bed audio play all across the board, what
values would you propose to try?"

`bed_volume_voice` and `bed_volume_between` are the volume controls — **plain
multipliers on the sound's amplitude, not decibels.** 0 is silence; 1 is a
clip at the clips' common level (−20 dBFS, the average every clip is first
brought to by its own gain in `bed.json`); 0.15 multiplies that sound by 0.15.
`bed_dip_s` and `bed_rise_s` are not volumes: they are the seconds a change
takes. The owner asked for the explanation as a comment above the settings
(verbatim): "bed_volume_voice and bed_volume_between are the volume controls.
They are plain multipliers on the sound's amplitude (not decibels). bed_dip_s
and bed_rise_s are the seconds a change takes" — added to the fork's
`app/config.py`, and to its runbook (`show-page.md`, "The static bed").

**In decibels:** 20 × log₁₀(value). Rules of thumb: −6 dB is half the
amplitude; −10 dB sounds about half as loud.

| Setting | Value | In dB |
|---|---|---|
| `bed_volume_between` | 0.15 | −16.5 dB |
| `bed_volume_voice` | 0.05 | −26.0 dB |

**To lower the whole bed, multiply both by the same factor** — the dip keeps
its shape ("between" stays 3 times "voice", 9.5 dB apart):

| Try | `bed_volume_between` | `bed_volume_voice` | Change |
|---|---|---|---|
| a little quieter (× 2/3) | 0.10 (−20.0 dB) | 0.035 (−29.1 dB) | about −3.5 dB |
| **half the amplitude** (× 1/2; the agent's first suggestion) | **0.075** (−22.5 dB) | **0.025** (−32.0 dB) | **−6 dB** |
| about half as loud (× 1/3) | 0.05 (−26.0 dB) | 0.017 (−35.4 dB) | about −9.5 dB |

(In the chat the last row read 0.015 and "−10 dB", rounded; a third of 0.05 is
0.017, and × 1/3 is −9.5 dB.) Under `show:` in `settings.yaml`, with a restart
of the app. **The owner kept the defaults for now.**

**Other levers against "annoying"** (the agent's): switch off the harshest
clips in the story's `bed.yaml` (the dial-up modems #16 and #17, the "harsh
analog fm radio flips" #10 are candidates) — the owner: "Agreed, will do
eventually"; and the second build: the silences on a timer give the ear
regular breaks, and the AM filter takes the hiss's sharp high end off.

#### "No restart" — and a correction

**The owner (verbatim):** "but what do you mean with "no restart"?" The app
reads `settings.yaml` **once, when it starts** (the uvicorn process): a
change of a setting needs the app stopped and started again. It reads the
story — `stories/lab-outbreak/bed.yaml` among its files — **each time a run
opens** (the start route calls `load_story`): a change of `bed.yaml` needs
only a new run, the app left running. **The correction:** §8.16 and the
first runbook text said "change a line, press Start"; but the page shows
Start only on a fresh page (`setState`: Start is visible in `idle`, or after
a failed first start) — after a run has opened, the page offers Stop and
Resume, and **Resume continues the same run, with the list it opened with**.
So: change the line, **reload the show page, press Start**. Corrected in the
fork's `bed.yaml` header and runbook.

### §8.18 The second build: silences, the AM filter, the fading (2026-10-02, night)

**The owner (verbatim):** "Let's focus now on completing the second part of
the build, because, as you said: the silences on a timer give the ear
regular breaks, and the AM filter takes the hiss's sharp high end off. Both
directly target "annoying"." And, mid-build: "Oh, if you can commit the state
of the code before you start the part 2." — part 2's files were already in
the working tree; they were set aside in the scratchpad, the committed versions
put back, the state before part 2 committed (the fork's `af0b9c4`: the volume
comment, the `bed.yaml` header, the runbook; this repository's `0584a34`:
§8.17), and part 2 restored, `cmp`-identical.

**The shape proposed, then three questions, the owner's choices:**

| Question | Chosen |
|---|---|
| "How should the AM filter be switched, for your A/B listening?" | **Setting + live F key** (the recommendation): `bed_filter` decides how a run starts (off by default until the owner picks); the F key flips it live on the page; with debug on, the console says so |
| "Which parts of the second build now?" | **Silences, filter, fading** (the recommendation); the crossfade (two audio elements taking turns) later, if the joins bother the ear |
| "Are the starting numbers right (all settings, tunable by ear later)?" | **Yes, as proposed** (the recommendation): silences every 30-120 s, lasting 3-15 s, 1 s fades; the filter 300-3,000 Hz; the fading ±3 dB every 2-6 s |

#### What was built (the fork, uncommitted)

**The chain** in `static/show/bed.js`, each stage a Web Audio node:

```
the clip → its gain → the bed's level (mono) → [AM filter: highpass 300 Hz → lowpass 3,000 Hz] → the fading
         → the silence gate → the mute → the speakers
```

- **The silences** (`bed_silences` on; `bed_silence_every_s` [30, 120],
  `bed_silence_s` [3, 15], `bed_silence_fade_s` 1.0): a timer runs while the
  bed plays; when it fires, the gate fades to 0 over the fade, then the clip
  pauses (`audio.pause()`); after the silence's length, `audio.play()` resumes
  it where it stopped and the gate fades back to 1; the next silence is set. A
  state change in a silence moves the level and plays nothing; a clip that ends
  in a silence's fade loads the next, which waits for the silence's end; Stop
  cancels the silence (the gate back to 1 at once, so Resume comes back with
  sound and a new silence set). Console, with debug: `Show: bed silence: 9.0 s`.
- **The AM filter** (`bed_filter` off; `bed_filter_low_hz` 300,
  `bed_filter_high_hz` 3000): two `BiquadFilterNode`s, a highpass and a
  lowpass, each with Q = √½ (flat, no bump at the edge). Off, the bed's level
  connects straight to the fading; on, through the two filters — the switch
  re-routes the connection (`bedRoute()`). **The F key** flips it live (not
  before the bed plays); console: `Show: bed filter on, 300-3000 Hz (F)` /
  `filter off (F)`.
- **The fading** (`bed_fading_db` 3, 0 turns it off; `bed_fading_every_s`
  [2, 6]): each step draws a length in the range and a level within ±3 dB, and
  glides the fading's gain to it over that length; Stop ends it.
- **The settings** (`app/config.py`, with a comment explaining them; a check
  that each range is two seconds above 0 and in order, and the filter's band in
  order) reach the page in the start reply's `bed` (every `bed_*` setting,
  without its prefix: `app/models.py` `ShowBed`, `app/routers/show.py`).
- **The dice** (`bed.random`, `Math.random` on the page) are one property, so
  the tests load their own.

#### Checked

- pytest **1280 passed** (1252 before: 28 new — the ranges 18 (three
  settings × six bad pairs), a one-value range, the filter's band 2, the
  bounds 7); the defaults and the start reply's fields extended.
- Node **`test_show_bed.js` 29** (19 before: 10 new — the two dice functions;
  a silence from fade to resume; a clip ending in a silence; Stop in a
  silence; silences off; the filter off and the F key; the filter on from the
  settings, at the settings' band; F before the bed plays; the fading's glide
  and its next step, ended by Stop; the fading off), with **fake timers**
  (`setTimeout` queued, fired by the test) and the dice at 0.5 (a silence after
  75 s, 9 s long; a glide of 4 s). The others unchanged: 42 / 17 / 91 / 8.
- **The tests catch a wrong build:** two mutations of `bed.js` (backed up,
  restored, `cmp`-identical) — the silence never pausing the clip, and the F
  key flipping nothing — each failed a test.
- No new code line over 120 characters, no en dash.
- **A real browser** — the owner: "yes, restart the dev server". Restarted
  (debug still on); the start reply carried the 17 clips and every new
  setting. In the app's built-in Chromium (`?design=old-radio`), **without
  Start** — no round asks the model, so the owner's show keeps the model's one
  slot: a click on the speaker cloth (the page may then play), the page's
  audio unlocked, **the bed muted with M first** (nothing reached the
  speakers), a run opened by `/api/show/start`, **its silences shortened for
  the check only** (every 3 s, 2 s long), the state set to `thinking`, and the
  bed sampled every 0.5 s:

  | Time | Measured |
  |---|---|
  | 0-2.5 s | playing; the clip advancing 0.5 s per 0.5 s; the gate at 1 |
  | 3.0 s | the silence begins: `silent` true; the gate 0.989 |
  | 3.5 s | the gate 0.488 — the 1 s fade half way |
  | 4.0 s | the gate 0; **the clip paused at 4.0 s** |
  | 4.0-5.5 s | paused; the clip held at 4.0 s |
  | 6.0 s | **playing again from 4.0 s**; the gate 0.016, rising |
  | 6.5-7.0 s | the gate 0.517, then 1; the clip at 4.5, 5.0 s |
  | 9.0 s | the next silence beginning, 3 s after the last one ended |

  The fading glided smoothly all along (1.000 → 0.802 over 9 s, within ±3 dB).
  **The F key** (a real `keydown`): the filter on — a highpass at 300 Hz with
  Q 0.7071 and a lowpass at 3,000 Hz — the clip playing on through it, then
  off. Stop: the clip paused, no silence pending, the gate back at 1. **The
  console, as it printed** (the M key pressed before the run opened, so its
  line is not there):

  ```
  Show: bed shuffled: a new pass of 17 clips
  Show: bed clip 1 of 17: 730109-shortwave-radio-static-with-indistinguishable-foreign-chatte.mp3 (gain +9.4 dB)
  Show: bed silence: 2.0 s
  Show: bed silence: 2.0 s
  Show: bed silence: 2.0 s
  Show: bed filter on, 300-3000 Hz (F)
  Show: bed filter off (F)
  ```

  This real capture replaced the runbook's illustration of the console lines.
  The check left two short runs in the dev checkout's `runs/` (gitignored):
  `2026-10-02T01-08-33` (the start reply's check) and `01-08-54` (the
  browser's), neither with a round.

### §8.19 Does the bed change the voices' volume? Checked: no — the mood clips do (2026-10-02, night)

**The owner (verbatim):** "I want you to inspect the changes that you made. Is
there any way that you may have altered by mistake the volume of the TTS
voices. I notice wide volume changes in some of the voices, especially the
females... Could be just another manifestation of the voice instability of the
TTS engine, but we need to be sure it's not this volume control feature
spilling over to the TTS voices."

#### The code: the voice's path is untouched

- **Nothing on the voice's path changed since `tz-0.5`** (`git diff --stat
  tz-0.5` on the committed and the working tree): `static/show/player.js`
  (which decodes and plays each chunk), `show.js`, `gauge.js`, `mic.js`,
  `app/routers/tts.py`, `app/services/tts_client.py`, `app/show/debug.py`,
  the story's `overtones.yaml` — no line. The branch changed only the bed's
  files, the settings, the start reply, the story's loader (`bed.yaml`), the
  templates (which load `bed.js`), tests and docs.
- **What `bed.js` touches outside its own state:** it reads `voice.ctx` (the
  page's one AudioContext) to plug its chain into it, and connects its last
  node, the mute, to the speakers (`ctx.destination`); it wraps `setState` and
  `setReceiver` (calling them unchanged first). It never touches
  `createBufferSource`, `playClip` or any of the voice's nodes. The voice's
  chunks still go `buffer source → ctx.destination` (`playClip`), at their
  own level; at the speakers the browser adds the two sounds — no gain of the
  bed sits on the voice's path.

#### The measurement: the voice as the engine returned it

With `debug` on, the voice route keeps every chunk **as the TTS engine returned
it**, before the page decodes or plays it (`runs/<run-id>/debug/audio/`,
mono 24 kHz 16-bit) — so a difference in those files cannot come from the
page. Each chunk's speech level, in dBFS: the RMS of its 20 ms frames above
−45 dBFS (so the pauses do not lower it), per speaker
(`<scratchpad>/chunk_levels.py`):

| Speaker | Before the bed — 2026-09-30: `18-52-59`, `19-08-07`, `19-20-04` (chunks · mean · stdev · min..max · range) | With the bed — 2026-10-02: `00-29-11`, `01-10-49` (the owner's listening) |
|---|---|---|
| Daniel | 19 · −21.0 · 2.7 · −27.7..−15.5 · 12.2 dB | 55 · −21.2 · 3.1 · −31.7..−15.6 · 16.1 dB |
| Moira | 18 · −25.6 · 2.4 · −30.5..−21.1 · 9.4 dB | 44 · −26.0 · 3.8 · −35.4..−20.3 · 15.1 dB |
| Ralph | 13 · −21.2 · 2.5 · −25.4..−15.6 · 9.8 dB | 49 · −20.7 · 3.2 · −28.0..−12.8 · 15.2 dB |
| Samantha | 18 · −24.5 · 2.6 · −30.8..−20.3 · 10.5 dB | 47 · −24.0 · 2.2 · −30.7..−19.8 · 10.9 dB |

The means agree within 0.5 dB; the engine's chunks varied as widely before the
bed existed (ranges of 9-12 dB); the wider ranges tonight come with three times
the chunks (more chances for an extreme). **The women are about 4 dB quieter on
average** (Moira −26, Samantha −24.5, the men −21), before and after alike.

**Where the swings come from — the mood clips** (all five runs, per speaker
and reference clip, `<scratchpad>/chunk_levels_by_clip.py`; the average, the
number of chunks):

| Speaker | Quietest moods | Loudest moods | Spread of the averages |
|---|---|---|---|
| Moira | `ref-fear` −32.7 (5), `ref-distress` −28.5 (5) | `ref-sadness` −23.7 (4), `ref` −23.6 (5) | **9.1 dB** |
| Samantha | `ref-amusement` −29.7 (2), `ref-fear` −27.6 (2) | `ref-sadness` −22.7 (8), `ref-confusion` −20.2 (4) | **9.5 dB** |
| Daniel | `ref-amusement` −24.0 (2), `ref-fear` −23.9 (3) | `ref-pain` −19.0 (9), `ref-confusion` −18.7 (11) | 5.3 dB |
| Ralph | `ref-realization` −26.3 (2), `ref-amazement` −25.4 (1) | `ref-sadness` −19.2 (3), `ref-confusion` −16.0 (10) | 10.3 dB |

**The cause:** the mood voices (`tz-0.4`). Every reference clip was cast at the
same level (`cast_voices.py`: RMS −20 dBFS), but the engine clones the
**delivery** of a clip, not its level: Moira's *fear* recording is near a
whisper, and the lines said with it come out about 9 dB below her *sadness*.
On top, chunks said with the same clip still vary by 5-10 dB (the engine's
instability, known since 2026-09-30). The bed adds and removes nothing; it can
only change how the voice **seems** next to it (the static dipping under a
line, its ±3 dB fading) — a matter of perception, not of the voice's level.

**A remedy, if wanted (not built; the owner's call):** level each chunk to a
common speech level before it plays — the page has every chunk decoded already
(`decodeAudioData`), so a gain per chunk from its RMS is a few lines in
`player.js`; or the voice route could do it on the server. It would flatten
the whispered *fear* too: a partial levelling (halfway to the target) keeps
some of the delivery. **The owner (verbatim):** "Humm, this is an interesting
feature. but I think it belongs in a follow up." — recorded in
`docs/follow-ups.md`, "Even out each voice chunk to a common speech level",
with the sketch (the samples scaled in place, not a gain node on the voice's
path, which would leave the gauge still), **not a priority, undecided whether
to build it** (the owner: "make it as not a priority and undecided if we will
execute on it").

### §8.20 The verdict after a longer listen; what is left; narrower filters to try (2026-10-02, night)

**The owner (verbatim):** "I listened to the show a bit longer. Very good
impressions. I think technically we have met and exceeded our goals." And:

> * I think the silence works well in reducing the fatigue of listening to
>   static.
> * The filter I am not sure if it helps. Maybe we could do a test with a
>   narrower band of frequencies to see if:
>
> 1. The bed noises cause less fatigue
> 2. The bed noises become more old radio poor reception style.
>
> I do not want to execute the narrower filter test right now because it is
> really late here and I need to go to bed, but I want you to give me a few
> recommendations for ranges of frequencies to try.

#### What is left of what we set out to do (§8.7, §8.10-§8.13)

| Item | Where it was set | State |
|---|---|---|
| The crossfade at the joins (1.5 s, two audio elements taking turns) | §8.8 refinement 2; §8.18 (the owner chose to leave it out) | **not built** — only if the joins bother the ear |
| The filter's default (on or off) and its band | §8.12; §8.18 | **open** — the narrower-band test below |
| The owner's picks of the clips (5-15 of the 17; the harshest switched off) | §8.7 step 2; §8.17 | **open** — the story's `bed.yaml`, `enabled: false` ("will do eventually") |
| Three timings as settings or constants (the silence on the press 0.15 s, a clip's fade-in 0.3 s, the mute's fade 0.3 s) | §8.15 | **open**, the owner's call |
| The credits of the CC BY clips (and the CC BY-NC and Sampling+ ones) — on a slide, or a credits note | §8.12, 3A | **open** — for the talk (Task 9); each credit line is in `bed.json` |
| A release: merge #10 and #22, tag, pin the installer, `make client-mac` | §8.13 step 3 | **after review** — the installed client already has `Sounds/bed/` prepared |
| Lists per kind of round (the breakdown, the repair, the contact) | §8.10, question 5 | later — the data allows it |
| Event sounds as a layer of their own | §8.11 | after the demo |
| Even out each voice chunk's level | §8.19; `docs/follow-ups.md` | not a priority, undecided |

#### Narrower bands to try (the agent's recommendations)

Why narrower could help on both counts: **fatigue** — the ear is most sensitive
around 2-5 kHz (the ear canal's resonance, near 3 kHz), and the hiss's sharpest
energy sits from there up; an upper edge at 2-2.7 kHz takes out most of what
the ear finds harsh. **The old-radio sound** — a shortwave receiver passes a
narrow band: a ham's single-sideband (SSB) voice filter is about 2.4 kHz wide
(roughly 300-2,700 Hz), a communications receiver set to "narrow" less, and a
Morse (CW) filter a few hundred hertz around a tone. The less band, the more
"poor reception". The current band, 300-3,000 Hz, is the telephone's — clean
enough that it may not sound like a radio at all, which would fit the owner's
"not sure if it helps".

| Try | `bed_filter_low_hz` | `bed_filter_high_hz` | Width | What to expect |
|---|---|---|---|---|
| A — the shortwave voice band | 300 | 2,700 | 2.4 kHz | a ham's SSB filter: the classic shortwave sound; the harsh top just gone |
| **B — a narrow receiver** (the agent's first pick) | **400** | **2,000** | 1.6 kHz | tinny and boxy, clearly "radio"; much less hiss |
| C — poor reception | 500 | 1,500 | 1 kHz | a cheap, distant receiver; the static becomes a mid-range rush |
| D — the extreme, to know the limit | 600 | 1,000 | 0.4 kHz | close to a Morse filter: almost a tone; only to hear where it breaks |

**How to run it:** each pair under `show:` in `settings.yaml` (with
`bed_filter: true`, or the F key to A/B against no filter), then a restart of
the app; listen a few minutes each, B first. Two cautions: a narrower band also
**sounds quieter** (less energy passes), so a fair comparison may want
`bed_volume_*` raised a little with it; and the edges are gentle (one filter
per edge, 12 dB per octave) — if B and C still sound too "full", a steeper
edge (two filters per edge) is a small change in `bed.js`.

#### Wrapped up for the night

The owner: "Let's wrap up for the night. Commit and push. Make sure the PRs
are in order to be reviewed." The dev server stopped; its `settings.yaml`
restored (`cmp`-identical to the backup: `show: seed: 42`). Part 2, §8.17-§8.20
and the follow-up committed and pushed; both PRs' descriptions brought up to
date.

### §8.21 The leftovers ruled; the clips in the repo (Task A, under discussion); a settings runbook (Task B, built) (2026-10-02)

**The owner (verbatim)**, on "What's left of the bed's plan": "no, keep the
handoffs for now." (asked whether to delete handoffs 6-9), then:

> Of your "What's left of the bed's plan", we will execute before the demo (so,
> they are priority, but not to execute today... We need to document them in
> TODO properly): (1) The filter test you described (bands below). It may change
> the filter's default or its band. (2) Your picks of the clips: switch off the
> harshest ones in the story's bed.yaml. (I will add one task related to this
> soon). (3) Credits for the talk: the 7 clips that aren't CC0 need a slide or a
> credits note. Each credit line is already in bed.json. (I will add one task
> related to this soon).
>
> The rest we will execute today: (4) A release: merge both PRs, tag the fork,
> pin the installer to the tag, run make client-mac. … (As soon as I merge the
> PRs)
>
> (5) Not built by choice: the crossfade at the joins (only if they bother you),
> and whether three short timings become settings.... A/ Correct. I do not see
> any value in implementing crossfade for our app. You can close any follow-up
> that may exist about crossfade with a note that we decided not to implement.
>
> (6) lists of clips per kind of round, event sounds as a second layer, and the
> voice-levelling follow-up (undecided).... A/ Same thing. I do not see any
> value in implementing this right now. Keep it in a follow up but mark it as
> very low priority and undecided if worth executing... Keeping it only to
> conserve as a ledger of all our ideas.

**Recorded:** (1)-(3) as **Task 10, "The static bed before the demo"**, in
`docs/TODO.md`; (5) — no crossfade follow-up existed, so one was written to
record the decision, closed: **not to be implemented**; the three timings stay
constants (closed); (6) — two new follow-ups (lists per kind of round; event
sounds as a second layer) and the voice-levelling one, all **very low
priority, undecided whether worth executing, kept as a ledger of ideas**.

#### Task A — the clips in the repo, only the incompatible ones ignored (under discussion)

**The owner (verbatim):** "I decided this bed audio feature is too good not to
come out of the box with the app when someone deploy it. So, what we are going
to do is: Give me a list of all the audios we cannot include in the repo for
license reasons. Then we are going to set these audios with problematic
licenses to `enabled: false` in `stories/lab-outbreak/bed.yaml`. Finally we
are going to modify our gitignore to ignore only those files with problematic
licenses, instead of the whole audio bed folders. This way users get a
functional app with the limited range of bed audios available that respect
licensing, but we still provide the names and the metadata of all the bed audio
files we considered, if someone wants them they can find and download
themselves. What is your opinion? Pushbacks?"

**The list — 2 of the 17:** 11859 *analog_noise_arped_radio_static*
(**Sampling+ 1.0**: the whole work shared only non-commercially) and 30302
*CS3B_beacon* (**CC BY-NC 4.0**). The fork is **MIT** (upstream's licence,
kept): anyone may use it commercially, which non-commercial clips would
contradict. The other 15 may go in: 10 CC0, and 5 CC BY (#2, #3, #4, #6, #13)
**with their attribution shipped**. Committable: 27.46 MB (the two excluded:
0.58 MB).

**The agent's opinion: yes — with these points to settle:** (1) **credits are
mandatory** for CC BY: a `Sounds/bed/CREDITS.md` generated from `bed.json` (as
the old-radio look's `CREDITS.md` for its photograph), and a line in the
README's licence section; (2) **27.46 MB into git's history for good** —
fine for GitHub, heavier clones; mono 64 kbps copies would be ~9 MB but break
the owner's "files untouched" (the agent's recommendation: accept the 27 MB);
(3) **a release trap:** the installed client holds the 17 copies untracked; a
tag that tracks 15 of them makes `git checkout` refuse to overwrite them, so
`make client-mac` would fail — the release must delete the client's
`Sounds/bed/` copies (and the `Sounds/` line of its `.git/info/exclude`)
first; (4) **the tool's target changes:** `prepare_bed.py` must never again
write into the installed client (tracked files modified there would break the
installer the same way) — it writes into the fork's dev checkout, and the
result goes through a PR; (5) **quiet logs:** a `bed.json` entry whose file is
missing should be skipped quietly unless the story enables it (else every
clone logs 2 warnings per Start); (6) **`.gitignore` by explicit name**, two
lines with a comment naming the licences, and a check in `prepare_bed.py`
that warns when a clip that is not CC0 or CC BY is missing from it; (7) the
two set to `enabled: false` in `bed.yaml`, with a comment why.

**The owner:** "Let's start by implementing "Task B: a practical settings
runbook, and the keyboard shortcuts" After we finish with this one, we will
discuss in more detail the Task A." — **Task A waits for that discussion.**

#### Task B — a practical settings runbook, and the keyboard shortcuts (built)

**The owner (verbatim):** "Now that we have so many configuration knobs in the
fork app, the need arises to document well what they are and give recipies of
how to change them (like the scenarios we discussed for the bed audios of
several audio volume levels, and several filter settings). This file should be
practical oriented, to show the user quickly what knob to change to achieve
something in the app. Also we should document well the keyboad shortcuts we
have for the app. (Possibly these shortcuts also documented in a top level
README section) Opinion? Pushbacks?"

**The agent's pushbacks, taken:** no duplicate of all ~60 settings — the
comments of `ShowConfig` stay the complete reference, the runbook holds
recipes and points there; `show-page.md`'s settings table points to the new
runbook (one source); a small docs test against drift.

**Built (the fork, uncommitted):**

- **`docs/runbooks/show-settings.md`** (new) — "the show's settings — recipes",
  organized by what one wants: how a setting changes (the file, `show:`, a
  restart — with the command — and a new run; what needs no restart: the
  story's files, the address switches, the keys; **a misspelled setting is
  ignored without a word, a value out of bounds stops the app at start** —
  both checked: `ShowConfig(bed_volume_betwen=0.3)` keeps 0.15;
  `bed_volume_between: 1.5` raises "1 validation error for ShowConfig /
  bed_volume_between" from `load_settings()`, which the app's start does not
  catch); the demo, or a test show; **the static bed** — quieter or louder
  (the ×2/3, ×1/2, ×1/3, ×1.5 table), a deeper or gentler dip, no static (the
  setting, the M key, the contacts only), more rest or fewer breaks (the
  silences), a steadier or livelier signal (the fading), **the AM filter's
  bands A-D**, the static on the plain page, a clip switched off or changed
  by ear (the story's `bed.yaml`); **the listener's turn** (the window, the
  press cap, the calls sooner or later, longer or shorter contacts); **the
  story's pace** (events, orientations); **the model server's context** (a
  16k server: `context_budget` 16,500 — 0.9 × 16,500 + 1,000 + 512 =
  16,362); **the address switches**; **the keyboard shortcuts** (Space held:
  talk, only while the radio listens; M: the bed's mute; F: the bed's filter;
  M and F ignore a held key and Cmd, Ctrl or Alt — those three are every key
  the page has; the captions toggle is a button).
- **`README.md`** — a fork section "The show page: keyboard shortcuts and
  settings": the three keys, and the three runbooks (settings, the page, the
  driver), above the upstream README, which stays unchanged.
- **`docs/runbooks/show-page.md`** — "The show's settings" shortened to where
  the settings live and a pointer to the new runbook (its heading kept: cited
  elsewhere); the static bed's volume note points to the recipes.
- **`tests/test_docs.py`** — **a drift test:** every name under `show:` in a
  YAML example of `docs/runbooks/*.md` or the README must be a field of
  `ShowConfig` (34 names found, in `show-settings.md`, `show-page.md` and
  `show-driver.md`); a renamed setting would otherwise leave a recipe that
  silently does nothing. **Proven:** a misspelled `bed_volume_betwen` added to
  a backed-up copy of the runbook made it fail ("Settings in the docs' YAML
  examples that ShowConfig does not have: bed_volume_betwen
  (show-settings.md)"); the runbook restored, `cmp`-identical.
- **`AGENTS.md`** — the coverage map's line on `test_docs.py`.

**Checked:** pytest **1281 passed** (1280 before: the drift test).

### §8.22 The clips chosen by ear, one by one; Task A done — the bed ships with the app (2026-10-02)

Task B committed and pushed (the fork's `07ca8e7`, this repository's
`6625289`). **The owner (verbatim)**, opening Task A: "Now, for Task A, before
starting executing, I should eliminate audio files that do not perform well or
with incompatible licenses: We will remove the files with the problematic
licenses: `CS3B_beacon.wav` and `analog_noise_arped_radio_static.wav` (we can
remove them completely from `bed.yaml` and even their entries in metadata
bed.json). They are not good quality anyway. Then, we will go together one by
one with the rest of the files examining which ones we could remove. You had a
shortlist of files that you thought were not a good fit for several reasons.
Let's start by revisiting that list."

#### Two measures, to back the agent's ear-less guesses

On the mono mix the page plays (ffmpeg): **the share of energy above 4 kHz**
(two highpass filters at 4 kHz, then `volumedetect`, against the clip's full
level) — where hiss stings; and **the loudness range** (LRA, EBU R 128,
`ebur128`) — how much the level jumps inside the clip.

| # | Id | Clip | Length | Above 4 kHz | LRA |
|---|---|---|---|---|---|
| 2 | 719588 | Handheld radio music and static | 42 s | 5.6 % | 9.9 LU |
| 3 | 615189 | radio11 | 14 s | 1.5 % | 3.0 LU |
| 4 | 730109 | Shortwave Radio static with indistinguishable foreign chatter | 172 s | 6.0 % | 4.7 LU |
| 5 | 625095 | radio_static_01 | 85 s | 1.6 % | 11.9 LU |
| 6 | 34418 | morse static | 5 s | 0.2 % | 2.0 LU |
| 7 | 396902 | Full radio sweep | 297 s | **24.5 %** | 11.3 LU |
| 8 | 652596 | Vintage Radio Tuning 5 | 111 s | 11.7 % | 9.3 LU |
| 10 | 722884 | harsh analog fm radio flips | 21 s | 7.8 % | 4.4 LU |
| 11 | 557532 | radio tuning fm | 165 s | 1.3 % | 5.3 LU |
| 12 | 624412 | Radio Music - A MakeNoise Morphagene Reel | 156 s | 0.5 % | 9.5 LU |
| 13 | 255775 | S06Russian | 110 s | 0.0 % | 2.6 LU |
| 14 | 343740 | Radio transmission morse code @4606.2kHz Poland | 76 s | 0.0 % | 3.4 LU |
| 15 | 855480 | Radio — Generative Sound by Glorb | 120 s | 6.8 % | 3.7 LU |
| 16 | 658932 | Dial-up_sound | 19 s | 2.1 % | 5.8 LU |
| 17 | 546450 | The Sound of dial-up Internet | 29 s | 1.5 % | **13.8 LU** |

(#13 and #14 have nothing above 4 kHz: their recordings were made at 7,119
and 8,000 Hz.)

#### The review, clip by clip

Each presented with its uploader's own description (read from its `.json`),
the two measures, the case for and against, and the agent's lean; the owner's
answer verbatim.

| # | The agent's lean | The owner (verbatim) | Verdict |
|---|---|---|---|
| 1, 9 | — (licences: Sampling+ 1.0, CC BY-NC 4.0; the fork is MIT) | "They are not good quality anyway." | **out** |
| 17, 16 | remove: computer modems, not a radio; #17 the busiest (13.8 LU) | "yes, remove both dial-up modems." | **out** |
| 10 | lean remove: harsh by its own name (7.8 %), abrupt band flips | "yes, remove #10" | **out** |
| 7 | lean remove: the harshest by far (24.5 %), busy, the longest (a fifth of a pass) | "yes, remove #7" | **out** |
| 13 | lean keep: S06, a real numbers station (numbers read in groups of three) — iconic shortwave; a faint murmur under a line | "yes, keep #13. The fact that the voice is speaking in Russian adds to the mystery and the atmosphere." | **kept** |
| 2 | lean keep: "voices and static… perfect for any Silent Hill-esque project" (the uploader) — the horror games' radio that crackles when monsters near | "yes, keep #2. As an interesting note: in the beginning of this clip you can hear a voice talking in what I think is a slavic language, maybe Russian too." | **kept** |
| 12 | lean keep: ten splices of real shortwave from the WebSDR in Enschede (the same receiver as #13), soft on the ear; abrupt joins, some music | "yes, keep #12. Sounds very intriguing, and it's not so aggressive to my ears." | **kept** |
| 6 | lean remove: 5 s, a switch click that may pass for a glitch; Morse covered by #14 | "yes, remove #6" | **out** |
| 3 | lean keep, mildly: an old multiband receiver, tuning and voices; short (14 s) | "lets remove #3" | **out** |
| 8 | lean keep: a real vintage receiver swept across every band; the harshest kept (11.7 %) — the filter test may tame it | "yes, keep #8." | **kept** |
| 4 | lean keep: the textbook "other stations bleeding in" (QRM) | "yes, keep #4. As a note: the foreign voices speak in an Asian language, probably Chinese." | **kept** |
| 5 | lean keep: the only pure static; the busiest left (11.9 LU) | "yes, keep #5. I do not find it so easy on the ears. But it sounds like the real deal. I can always disable it later in the bed.yaml if I dislike it." | **kept** |
| 11 | lean keep: someone tuning FM by hand, Italian and French talk; FM, not shortwave | "yes, keep #11" | **kept** |
| 14 | lean keep: a real Morse transmission at 4,606.2 kHz, "sent by a human" (the uploader) | "Keep #14. Make a note to lower this one in the control we have in the gain_db, it annoys my ears, but it is the real thing, so we keep it." | **kept, `gain_db` −6** |
| 15 | lean keep: synthesized by GLORB in Python (NumPy, SciPy) — a gift for a Python talk; may sound artificial | "No, let's remove #15, now that I hear it better it sounds very artificial." | **out** |

Asked along the way — "Remind me what is Task 10.1. and why we depend on it?"
— the agent: the narrower-filter test (TODO Task 10, item 1); #8's harshness
sits above 4 kHz, the very band the AM filter removes: if the test turns the
filter on by default, keeping #8 costs nothing; if not, #8 is the first to drop
if the bed still tires the ear — a soft dependency, not a blocker.

**The result: 8 kept, 9 out.** Kept: #2, #4, #5, #8, #11, #12, #13, #14 — 15.3
minutes, **17.23 MB**, 5 CC0 and 3 CC BY (#2, #4, #13: their credit lines
required). With the two incompatible clips gone entirely, **every clip kept may
ship**: `.gitignore` needs no list of exceptions, and the guard moves into the
tool.

#### "What pool?" — and the two last choices

**The owner (verbatim):** "I like the shape. But, I don't understand this. What
pool?" — the pool is §8.3's term for **the raw downloads**,
`zombie-radio-datasets/sounds/freesound/radio-static/` (outside git, beside
the checkouts): all 17 clips as fetched, each with its `.json`, whose last
section (`ours`: `kind`, `verdict`, `notes`) was left empty for us; the chosen
set is the fork's `Sounds/bed/`, copied from it by `prepare_bed.py`. Step 3
would fill each `ours` with the verdict and the reason — a convenience beside
each file; the record is this section. **The owner:** "keep step 3 and add the
consistency test, go ahead".

#### Task A, executed

**This repository** (uncommitted):

- `tools/sounds/bed.yaml` — the 8 ids; the target **the fork's checkout**
  (`app: ../TalkWithZombies/Sounds/bed`, resolved from this repository), never
  an installed client again (a tracked file changed there would make the
  installer refuse the clone).
- `tools/sounds/prepare_bed.py` — **the licence guard:** a clip that is not
  CC0 or CC BY stops the tool, naming it, and nothing changes; **`CREDITS.md`**
  written beside `bed.json` (the CC BY credit lines under "Credit required by
  the licence", the CC0 clips "credited with thanks"; the files described as
  Freesound's high-quality MP3 previews, converted by Freesound from the
  uploaded originals, otherwise unchanged).
- **The guard, tested:** a scratch copy of the list with 30302 and 11859 added
  → "not redistributable in the fork (only CC0 and CC BY): 30302 (CC BY-NC
  4.0), 11859 (Sampling+ 1.0); nothing changed" (the folder still 18 files).
- **The dry run, then the write** into the fork's dev checkout: 8 clips, 15.3
  minutes, 17.23 MB; the 9 rejected copies removed; checked — 8 entries in
  `bed.json`, 8 copies byte-identical to the pool, licence classes only `cc0`
  and `cc-by`. The installed client untouched (still its 17 copies and
  `bed.json`: 18 files).
- **The pool** (outside git): each of the 17 `.json`s' `ours` filled —
  `verdict` (9 `reject`, 8 `keep`), `notes` (the reason, with the owner's words
  where there were some), `reviewed` (the date and this section).

**The fork** (uncommitted):

- **`Sounds/bed/`**, committed for the first time: the 8 clips, `bed.json`,
  `CREDITS.md`; **`.gitignore`** loses its `Sounds/` line.
- **`stories/lab-outbreak/bed.yaml`** — the 8 clips (all enabled), #14 at
  `gain_db: -6` under a comment quoting the owner; the header: the clips ship
  with the app, chosen by ear on 2026-10-02.
- **Docs:** the README's licence paragraph (the eight clips from Freesound,
  under their own licences, CC0 and CC BY, with a link to `CREDITS.md`);
  `show-page.md` ("The clips": shipped, chosen by ear, credited; a change goes
  through a pull request; the tool's licence guard); the docstrings of
  `app/config.py`, `app/show/bed.py`, `app/show/story.py`; `AGENTS.md`'s
  coverage map.
- **The consistency test** (`tests/test_show_bed.py`, `TestShippedBed`, on the
  committed files): every clip the shipped story enables is on disk and in the
  manifest (the play list equals the story's enabled list — which clips is not
  pinned); every shipped clip is CC0 or CC BY; `CREDITS.md` names every clip
  and carries every CC BY credit line. **Proven:** one entry of a backed-up
  copy of the story's `bed.yaml` pointed at a clip not shipped (#7) → "1
  failed"; restored, `cmp`-identical.
- **Checked:** pytest **1284 passed** (1281 before: the three shipped-bed
  tests); Node 42 / 17 / 91 / 8 / 29; no added code line over 120 characters.

**The release, after the owner merges** (the trap of §8.21): delete the
installed client's untracked `Sounds/bed/` copies and the `Sounds/` line of its
`.git/info/exclude`; then the tag, the installer pinned to it,
`make client-mac`, and a check that the client holds the 8 tracked clips.

### §8.23 The release, `tz-0.6`; and a correction: the "trap" was not one (2026-10-02)

Task A committed and pushed (the fork's `c898d21`, this repository's
`8e63dab`), after the owner's check: "Please check that the content of
bed.yaml is identical to what you produced... I may have pressed a key in
vscode and altered the file, though I think I undo it, check anyway." —
`cmp` against the copy saved right after it was generated: identical (2,385
bytes); 8 clips, all enabled, #14 at −6 ("If check ok: keep -6, commit and
push both."). Asked "What component perform "5. The consistency test"? the
script tool, I suppose." — no: a pytest test in the fork
(`tests/test_show_bed.py`, `TestShippedBed`), run with the fork's suite on the
committed files; the tool's licence guard is the other layer, at preparation
time.

**The owner:** "Both PRs merged, go ahead with the release. We are going to do
this together: Delete the installed client's untracked Sounds/bed/ copies and
the Sounds/ line in its .git/info/exclude. Without this, make client-mac would
refuse the new release."

#### Two ignore lists — and the owner's questions

**The owner (verbatim):** "Why do we have to edit
`~/TalkWithZombies-client/.git/info/exclude`? I thought we created a gitignore
file." Git has two ignore lists:

| | `.gitignore` | `.git/info/exclude` |
|---|---|---|
| What it is | a file **in the project**, tracked and committed | a file **inside the clone's private `.git` folder**, never tracked, never committed |
| Who sees it | everyone who clones the repository | that one clone, on that one machine |
| Where we used it | the fork's dev checkout: `Sounds/` added (`c5288bf`), removed by Task A (`c898d21`) | **the installed client only**: one line, `Sounds/` (§8.14) |

The client got the second because its `.gitignore` is tracked (a checkout of
`tz-0.5`): edited there, the clone would be "locally modified", and the
installer's git step (`force: false`) refuses a locally modified clone.

**The owner (verbatim):** "What does this mean "the installed client only:
Sounds/ on line 7" ... Show me the lines of code where we make use of this." …
"Well, now we do not need that way. Do we still depend in any way of that way
to ignore files or is there any code that uses or sets it?" — **no code uses or
sets it.** "Line 7" is the seventh line of that plain text file (lines 1-6 are
git's template comments). It was written once, by hand, by the agent, on the
night of 2026-10-01 (`printf 'Sounds/\n' >> ~/TalkWithZombies-client/.git/info/exclude`);
only git itself reads it, at every `git status`, `git add` or `git checkout`
in that clone. A search of both repositories: the fork mentions
`info/exclude` nowhere; this repository only in this discussion (§8.14,
§8.21, §8.22) — the installer and the Makefile never.

#### The correction: git overwrites ignored files

§8.21 and §8.22 said that without the cleanup "`git checkout` would refuse
to overwrite them, so `make client-mac` would fail". **True only for files
that are untracked and not ignored.** Tested in a scratch repository (git
2.55.0): a release tag that tracks `Sounds/bed/clip.mp3`, and a local copy at
that path:

| The local copy | `git checkout` of the release |
|---|---|
| untracked, **not ignored** | **refused:** "The following untracked working tree files would be overwritten by checkout: Sounds/bed/clip.mp3 — Please move or remove them before you switch branches." |
| the same, **ignored** through `.git/info/exclude` | **switched silently**, the copy overwritten by the release's file |

Git treats ignored files as expendable. The installed client was the second
case (its line 7), so `make client-mac` would have succeeded without the
cleanup. **The cleanup was still worth doing, as tidiness:** without it the 9
rejected clips (13 MB) would stay in the client's `Sounds/bed/` for good,
unused (the new `bed.json` does not list them), and line 7 would keep hiding
them — and any future stray file under `Sounds/` — from `git status`: a
silent rule nobody would remember.

#### Done, together

1. **The client cleaned, by the owner** (verbatim: "I removed the Sounds
   folder and removed the line from `~/TalkWithZombies-client/.git/info/exclude`"),
   with the agent's check, as the owner ran it:

   ```
   % ls ~/TalkWithZombies-client/Sounds; tail -2 ~/TalkWithZombies-client/.git/info/exclude; git -C ~/TalkWithZombies-client status --short
   ls: /Users/alfredo/TalkWithZombies-client/Sounds: No such file or directory
   # *.[oa]
   # *~
   ?? .DS_Store
   ```

   (Before it, the agent's inspection: the client at `tz-0.5`, `Sounds/bed/`
   holding the 17 clips and the old `bed.json`, 27 MB — every file also in
   the pool; the `.DS_Store` is Finder's, left alone.)
2. **The merges checked:** the fork's `master` at `5347ead` (#10), its
   content identical to the tested branch head `c898d21`; this
   repository's `main` at `429d8c2` (#22), identical to its branch.
3. **The fork's tests on `master`:** pytest 1284 passed; Node 42 / 17 / 91
   / 8 / 29; 10 files tracked under `Sounds/` (the 8 clips, `bed.json`,
   `CREDITS.md`).
4. **The tag:** **`tz-0.6`**, annotated (`56e56cb`), on `5347ead`, pushed —
   "TalkWithZombies 0.6: the static bed — radio static played quietly under
   the show by the looks, from eight Freesound clips chosen by ear and
   shipped with the app (CC0 and CC BY, credited in Sounds/bed/CREDITS.md),
   shuffled, lower under a round, silent while the listener holds to talk,
   with silences on a timer, a slow fading and an AM filter (the F key); the
   M key mutes it; the story's bed.yaml chooses the clips; a settings
   runbook with recipes and the keyboard shortcuts".
5. **The installer pinned** (`client_version: "tz-0.6"`), on a new branch
   `alfre2v/installer-tz-0.6`, with the README's and the spec's tag, the
   static bed described in the spec (§6.10, §6.11, §9, §11), the TODO's
   "Now", and this section.
6. **Next, the owner's:** `make client-mac`, then the agent checks the
   client (`git describe` at `tz-0.6`, the 8 clips tracked, nothing
   untracked but `.DS_Store`, a second run `changed=0`).

#### The re-proof, five checks from the API, and a live test

**The owner (verbatim):** "Ran make client-mac the two times, all as
expected." — `git describe`: `tz-0.6`; "Clips are in the bed folder."; "hosts.yml
wired, tunnel is up." The agent's look at the client (read-only): `tz-0.6`;
tracked under `Sounds/bed/`: the 8 clips, `bed.json`, `CREDITS.md`; nothing
untracked but `.DS_Store`; **no `show:` section** in its `settings.yaml` — the
demo's configuration. Then (the owner: "Before we do an actual test. Is there
some test you want to drive yourself from the api…" — "start it yourself and
run all five checks"), the client's own app started by the agent on port 8000
(`uvicorn` from `~/TalkWithZombies-client`), the five checks, the app stopped:

| # | Check | Result |
|---|---|---|
| 1 | the start reply | the run opened (the start check passed on the 32k server); debug off, voice seed off, a random story seed; the bed: the demo's settings (silences on, filter off), 8 clips at their measured gains, **#14 at exactly 0.5012 of its own — 10^(−6/20)** |
| 2 | the clips served | all 8: 200, `audio/mpeg`, byte-exact; a range: 206; **12 refused** (404): the 9 rejected names, `bed.json`, `CREDITS.md`, a traversal |
| 3 | the pages | both looks load `bed.js`; the plain page not, with `&bed=on` yes, `&mock=1` not; the served `bed.js` byte-identical to `tz-0.6`'s (15,052 bytes) |
| 4 | a scripted show (`drive_show.py --rounds 6 --report`) | 6 rounds in 5.8 s, 14 lines, 0 dropped, the director's limits kept; two events as fixed lines, the Repair at round 6. The report's other five criteria (10 rounds, the listener's words, a silence, the trim, debug files) belong to a full checkpoint drive and cannot pass on a short drive in the demo's configuration — by design |
| 5 | the voice (`/api/tts`) | 200; a line with the story's *calm* clip (`ref.wav`), 4.6 s of speech; a line with `ref-fear.wav`, used as asked, 2.7 s of speech, synthesized in 1.1 s. (The agent's first request asked for a guessed `ref-calm.wav`, which does not exist; the app fell back to `ref.wav`, as designed.) |

Two short runs left in the client's `runs/` (gitignored): `17-23-32` (check 1)
and `17-23-57` (the drive).

**The owner's live test** (the demo's configuration): "All works well". One
oddity — Daniel saying Samantha's introduction in an exchange (round 18 of run
`2026-10-02T17-27-56`): traced from the run's record (debug was off) to the
grammar, which pins Samantha to the first line and lets only the others speak
after it — the model wrote her intended words under Daniel's name. Recorded in
`docs/follow-ups.md`, "A cast member says another's line — Daniel introduces
himself as Samantha", with the evidence and three options (none chosen).

## §9. Addendum, 2026-10-07 — the sound effects back on the table: the owner's two-part plan

### §9.1 Why it came back

With more days before the talk, the owner asked what to add to the project; the agent's first lists left the sound
effects out, filtering by "seen on stage" and taking the follow-up's label ("very low priority; undecided") at face
value. The owner (verbatim):

> The SFX effects: This is truly something technically interesting, we have some time to explore some of this. Not
> sure we have enough time, last time we discussed this you said it is a huge endeavor, that we need to create the web
> server to talk to the services, etc. We said that maybe we could generate some of the audio sounds offline and save
> them in the same way we do for the bed audio. Where are these features stored, why are you not proposing these
> features?

The agent's answer: the "huge endeavour" was a **live** sound service (§3, the pushbacks of 2026-09-30); the
**offline library** of §6.1 avoids it — sounds generated once, stored and played like the static bed — and §6.1's
estimate stands: the listening test half a day, the generation tool and the library one day, the show's side one to
two days.

### §9.2 The owner's plan (verbatim)

> Ok, that leaves the sound effects... I think the best way to approach this is to open an experiment, for us to
> tinker without altering the app. I brought the VM up, we can try deploying several sfx engines and testing what we
> get as effects... As I see it this task would have two parts:
> (1) The experiment: where we try running the sfx models and evaluate their effectiveness for our project.
> (2) Identifying the "events" in our event list that would benefit from SFX effects. And modifying our way to store
> the events so that we can store per event one or more SFX audio files to play just before that particular event.
> What do you think? Did I forget anything important?
>
> The only feature I have decided to execute for sure now is the voice compress... The other SFX is still pending
> discussion.

### §9.3 The agent's additions

**Part 1, the experiment** — much of it is already designed in §6.2 (never run):

- **The question, and the criteria written before listening** (§6.2: ten sounds, several sources, a page of players,
  the owner judging by ear).
- **A baseline:** the same sounds from Freesound (§4.4) — if recorded sounds beat the generated ones, the models are
  not worth their trouble.
- **Licences** — of the weights and of what they generate (§4.1, §4.3): MOSS-SoundEffect v2.0 is Apache 2.0; Stable
  Audio 3 is gated behind Stability AI's Community License, which the owner must accept on Hugging Face (never the
  agent). The credits matter for the talk.
- **The box:** every candidate fits the A6000 beside the stack (about 14.5 GB of 48), and the stack can be stopped
  while generating; Stable Audio 3 Small-SFX also runs on a laptop's CPU (§4.1) — a second, fair test.
- **A timebox**, so the tinkering does not eat the days before the talk.

**Part 2, the events** — beyond one or more sounds stored per event:

- **Where they play:** in the page, from the laptop — unlike the voices, the sounds never cross the network, so the
  venue's Wi-Fi does not matter.
- **When:** each event is read aloud on air, word for word, by a cast member (the fixed lines, 2026-09-27), so the
  sound comes just before that line, capped in length.
- **The mix:** the sound joins the bed's "sounds" gain, so the M key mutes it with the static; it stays quiet under
  the voices and silent while the listener holds to talk (the follow-up "Event sounds as a layer of their own…" holds
  the shape of §8.11).
- **Levels:** the clips evened out to one level, as the bed's are (`bed.json`).
- **Credits:** a `CREDITS.md` for the sounds, as for the bed.

**Part 3 (missing from the plan): the release** — a fork tag, the installer pinned to it, the owner's re-proof — before
Task 7's video, which the owner wants last ("Features first, video last").

**The box:** up since the owner woke it (2026-10-07), billing while up; hibernating it again risks the wake lottery
(2026-09-24, no A6000 in stock — `docs/runbooks/service-restart-sequence.md`). The owner's call.

### §9.4 Status

**Pending discussion** — nothing ruled beyond the owner's plan. The compressed reference clips (Task 12) come first.

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
