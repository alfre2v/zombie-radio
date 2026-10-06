# Zombie-Radio — Product specification

**Status:** living. This document describes the product as it is
built — the fork TalkWithZombies at tag `tz-0.6` (`5347ead`)
and this repository's deployment — in the order someone
would build it again. It is rewritten in place when the product
changes; it carries no history. Why each choice was made, and when,
lives in the decisions, discussions and experiments listed in §11.

## §1. Product

**Zombie-Radio** is a Halloween audio experience: what sounds like an
old radio drama — four scientists broadcasting from a hidden lab
during a zombie outbreak, a deliberate throwback to Orson Welles'
1938 *War of the Worlds*. The twist: the radio sometimes listens.
When the lab gets its receiver working, anyone in the audience can
answer on the frequency, and the cast talk to them — ask who they
are and where, ask for help, and remember what they said.

Two identity phrases; every decision is tested against them:

- **"Local AI first, cloud-capable."** Every model the show uses is
  open and self-hosted; the backend deploys identically to a home
  Linux GPU box or a rented cloud GPU. Commercial LLMs may appear only
  as offline authoring tools, never at show time.
- **"Theatrical live improvisation with LLMs."** The dialogue is
  improvised at broadcast time, not scripted. The show gives the
  model loose direction and lets it invent — places, names, details,
  backstory. What is judged is whether the story works for the
  listener: it hangs together, it speaks to them, it holds attention.

The first release is demonstrated at the Austin Python Meetup in
October 2026; its deadline is 2026-10-08.

## §2. Scope

### §2.1 The first release

- **Staging:** the web client on a laptop at the venue (a Mac; the
  demo machine is an M1 with 16 GB and cannot run the models); the
  models on a cloud GPU. Audience: whoever is in the room; one
  microphone control.
- **The broadcast:** four characters with distinct cloned voices
  improvise the drama continuously on a dedicated show page — an
  endless loop, a few lines per round, the next round asked for when
  the last one has been heard.
- **The listener's turn:** hold-to-talk, half-duplex. The listener
  holds a control to speak and releases it to finish. The control is
  enabled only while the lab's receiver is on and the cast have
  stopped speaking — which solves endpointing, self-hearing and who
  is being addressed by construction.
- **What the cast do with a caller:** answer them directly, find out
  who and where they are, ask for help (finding the lab, supplies, a
  vehicle, a relay), and use what the caller told them later in the
  show.
- **The canned episode:** a recording of the working show, played if
  the live stack fails on the day. Required.

### §2.2 Out of the first release

An always-listening microphone (voice activity detection and turn
taking) · an unattended booth · generated sound effects and live
audio mixing · speaker identification · overlapping speakers ·
several listeners at once · the microphone opened by the show at
narrative moments · episodes with a story arc beyond the endless
loop · stories written ahead by larger models and used as
guide-rails for the small one (a registered post-release idea: it
keeps the local-first rule, since the authoring is offline).

## §3. Architecture

### §3.1 Shape

The app runs on the demo laptop; the GPU box hosts only the model
services, reached through an SSH tunnel (§8.3). Inside the app, each
decision sits where its information is: the app's server is the
show's **director** (it knows the story), and its page in the
browser is the show's **clock** (only the browser knows when a line
has finished playing).

```
[demo laptop]
   └─ TalkWithZombies (our fork of TalkWithMe 7.1)
        ├─ server: the director — plans each round, sends ONE
        │    grammar-constrained streamed request, parses the script
        │    line by line (§6)
        └─ page /show at http://localhost — the clock: plays the lines,
             asks for the next round, hold-to-talk (a browser secure
             context, so the microphone needs no TLS); plain or in a
             look (§6.10)
        ⇅ SSH tunnel over the internet (§8.3)
[GPU box (Linux — cloud instance or home GPU box)]
   ├─ LLM: llama.cpp server (OpenAI-compatible API, GBNF grammars)   :8080
   ├─ TTS: tts-serve (a uniform REST API over voice engines)         :8001
   └─ STT: Whisper via whisper-fastapi                                :8002
```

The model services' APIs are the contract: anything a client needs is
reachable over them, never through shared local state. A round
crosses the internet once for its text (one streamed request writes
the whole round) and once per chunk of speech for its voice. Measured
on the deployed stack: the first streamed text arrives 0.3-0.6 s
after the request, and a four-line round takes about 1.4-2.0 s.

### §3.2 The two repositories

- **TalkWithZombies** (`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`,
  `github.com/alfre2v/TalkWithZombies`) — a real fork of
  scorbo2/TalkWithMe at tag 7.1 (MIT; provenance and notice kept),
  free to diverge from upstream. Upstream's chat UI stays as a
  rehearsal and debugging tool, at `/talkwithme`; the root `/` opens
  the show. The show lives in its own files (`app/show/`,
  `app/routers/show.py`, `static/show/`, `templates/show.html`,
  `templates/show_design.html`, `templates/show_choose.html`,
  `stories/`). Released as tags named `tz-<n>`.
- **zombie-radio** (this repository) — the deployment (`deploy/`,
  the `Makefile`), the documentation, the decisions and the
  experiments.

## §4. The model services

- **LLM:** llama.cpp's server, image
  `ghcr.io/ggml-org/llama.cpp:server-cuda-b11096` (pinned), serving
  **Nemotron Nano 9B v2** at `Q4_K_M`
  (`bartowski/nvidia_NVIDIA-Nemotron-Nano-9B-v2-GGUF`), a **32,768-token
  context** (`zr_llama_ctx`), every layer on the GPU, **one slot**
  (`--parallel 1`), and
  the server's host-RAM prompt cache. The show sends one request per
  round to `/v1/chat/completions` with a GBNF grammar in the top-level
  `grammar` field; constrained tokens stream in ordinary chunks. The
  system message starts with `/no_think`: Nemotron's chat template
  turns it into an empty, closed `<think></think>`, so the reply — and
  the grammar — start in the script, not in the model's reasoning. A
  grammar costs 0.3-0.5 % per token when the model already writes what
  it allows, about 10 % when it has to overrule the model; the show's
  grammar says exactly what the prompt asks for (§6.3). One
  conversation per slot: the chat UI and the show do not share the
  server at the same time.
- **TTS:** tts-serve at tag `1.2`, engine **Faster Qwen3-TTS**; each
  character's voice is cloned from a reference clip (`ref.wav`) in its
  persona folder. Typographic punctuation (`’`, `—`) makes this engine
  drop the pause before the final "Over.", so the app normalizes
  punctuation before synthesis (§6.8).
- **STT:** whisper-fastapi (image pinned by digest), model `small`, on
  the GPU. The app sends the cast's names as Whisper's prompt.
- **Memory budget:** the whole stack must fit a 24 GB card (the
  owner's RTX 3090 class); fitting 16 GB is a wish, not a target.
  Measured with one voice engine: 14.0 of 15.3 GiB on an A4000 (16k
  context); on the A6000, 14,195 MiB at 16k and **14,477 MiB at 32k**,
  flat through a full context — llama.cpp reserves the context's memory
  when it starts, and this hybrid model's context is small (about
  0.3 GB more for 32k). How to measure: `docs/runbooks/box-inspection.md`.

## §5. The story

A story is a folder, `stories/<name>/` in the fork; the show plays
`lab-outbreak`, "The Lab at the End of the Frequency".

- **`cast_sheet.md`** — a Jinja template (strict mode). Its **body**
  is the system message: the premise, one entry per character, and
  the placeholders `{{ model_prefix }}` (the setting `/no_think`),
  `{{ format_rules }}` (the format paragraph, filled in by code so
  that its words match the grammar) and `{{ episode }}` (empty until
  episodes exist). Its **front matter** is read only by code: the
  title, the cast (Daniel, Moira, Ralph, Samantha — each name a
  persona folder holding the voice), the **operator** (Samantha, who
  runs the radio), the facts an orientation tells newcomers, and a
  stage direction per receiver beat.
- **The premise** (in the body): four scientists trapped in a
  besieged research lab during a zombie outbreak, speaking over the
  lab's shortwave radio; the lab is secret, and all they know is that
  it stands near a wood and a swamp; the receiver keeps failing —
  while it is down they can only transmit, and when it works they
  call out for anyone listening; a listener who answers is a voice on
  the frequency, and the cast talk to them directly; the scientists
  try to explain the strange events that led to the lab's accident,
  hoping someone can find a cure, and ask the listeners for help.
  The four cast entries are placeholders until the character bibles
  are written.
- **`overtones.yaml`** — the emotional palette: three **overtones**
  in order — positive, neutral, negative — each with the **moods** a
  line may carry (fourteen in all) and its **tone words** grouped by
  theme; which overtones each kind of round may use; the weights
  with which free rounds drift to a neighboring overtone; and the
  **voices** — for each mood, the reference clip its lines are spoken
  with, named after what was recorded (`afraid: ref-fear.wav`,
  `calm: ref.wav`). The voices are optional, but all or nothing: once
  one overtone names them, every overtone names one for each of its
  moods; one map serves all four characters.
- **`events.yaml`** — 289 things that happen in and around the lab,
  filed by overtone, then by theme.
- **`agenda.yaml`** — nine things the cast want from a caller, each
  in two branches: ask for something, or, if the caller already gave
  it, use it. The first ("find out who the voice is") opens every
  contact.
- **`beats.yaml`** — the **fixed lines** of the receiver beats (§6.5):
  the call, in two pools of announcement-and-call pairs (after a
  Breakdown, after a Switch-off); the Breakdown; the Switch-off, in
  two pools (nobody answered, the caller went quiet). Four versions
  each. Optional: without it, the model writes the beats.

## §6. The show engine

### §6.1 The loop

The page runs a small state machine — idle, generating, playing,
listening — and asks the server for the next round when the voice
has drained. The server's director plans the round, the model writes
it, and the lines stream back as they are written. The loop is
endless. The server's endpoints (`/api/show/`):

- `POST start` — opens a run: loads and checks the story, renders its
  cast sheet, picks the seed.
- `POST round` — plans and streams the next round. The page sends the
  seconds of show audio played so far and, after a listening window,
  what the listener said. Each line arrives as the page's existing
  events (`start`, `token`, `done`, `complete`); the round ends with
  a summary: its kind, whether the page must now listen (`listens`),
  whether the receiver is on (`receiver`), its overtone, its agenda
  item, its slot, what was heard.
- `POST listen` — transcribes a press (§6.6).

### §6.2 What the model receives

The model has no memory between requests; every request carries the
whole show so far as one conversation:

- **system** — the cast sheet, identical in every request (so the
  server's cache serves it);
- then, for every round still kept, a **user** turn — the director's
  instruction for that round — and an **assistant** turn — the lines
  **the model itself wrote** for it, as `Name (mood): words`;
- last, a **user** turn with the new round's instruction.

A **fixed line** (§6.5) is never part of an assistant turn; it
appears only quoted in the instruction, as something already said
("Moira has just told them on air: "…""). A round with no model line
— the call — has no assistant turn: its instruction joins the next
user turn, running on with "Then". Instructions use only the words
the system message teaches — the script, lines, transmissions, the
listeners, a voice on the frequency.

### §6.3 The format and the grammar

Every line is `Name (mood): spoken words`, one or two short sentences
ending with "Over." — no narration, no markdown, nothing else in
parentheses. Each request carries a **GBNF grammar** that allows
only:

- the round's speakers, and optionally one of them pinned to the
  first (or the last) line;
- between the round's minimum and maximum number of lines;
- the round's moods — the four or five of its overtone;
- spoken text with no line break, bracket or parenthesis.

Every constraint the grammar enforces is also said in the
instruction, in the same words each time — who speaks ("Moira speaks
first, then Daniel or Ralph"), how many lines ("the next three
lines"), "each with the emotion in its voice, one of: …" — followed
by a tone word ("Let the tone be: haunted."). A grammar that
contradicts its prompt changes the model's style and costs more; one
that agrees changes no word. The line budget is the grammar's bound,
not a request: asked for up to four lines, the model writes four.

### §6.4 The director: Broadcast and Contact

The director (the fork's `app/show/director.py`) plans each round
from the run's record and the story. The show alternates between two
modes, driven by the lab's **receiver** — the part of the radio that
hears.

**Broadcast — the receiver is off.**

- **The sign-on** (round 1): Samantha tells anyone listening who the
  cast are, where they are, and that the receiver is dead — they can
  only transmit, and will call out when it works; a second voice adds
  a line.
- **Orientation repeats**, every 20 ± 5 free rounds, opened by
  whoever has been silent longest: the same facts for listeners just
  tuning in, with the receiver told as it went off — dead after a
  Breakdown, switched off after a Switch-off.
- **Free rounds:** the cast talk among themselves — two or three
  speakers (always whoever has been silent longest, then anyone just
  named, then chance), one to four lines weighted toward two and
  three. A free round's **slot** may hold:
  - an **event** (every 2 ± 1 free rounds, no repeats until the pool
    is used up), drawn from the round's overtone and read aloud as a
    fixed line;
  - the **aftermath** (the first free round after a contact): the
    cast talk about what the caller told them;
  - a **recollection** (every 15 ± 5 free rounds, once someone has
    called): the cast recall an earlier caller and imagine how they
    could help if they call again.
- **The call** (the Repair): between 60 and 180 seconds of played
  audio after the receiver went off — never before the first, always
  by the second, with a rising chance in between — the receiver
  comes back: someone announces it and Samantha calls out to anyone
  listening (two fixed lines). The page then listens.

**Contact — the receiver is on.** After every round that listens, the
listener's words or silence decide the next round:

- **An exchange** — the listener spoke: the character they addressed
  (or the one who asked last) answers first, 2-3 lines, speaking to
  the voice directly; the instruction quotes what the voice said,
  restates what it said earlier in the contact and, when earlier
  contacts exist, what earlier voices said, and adds one **agenda
  item** (the name item first, then the rest at random, never twice
  in a contact); the last line asks the voice a question. The page
  listens again.
- **A re-call** — a silence: Samantha calls once more (before anyone
  answered), or the cast repeat their unanswered question to the
  caller. The page listens again.
- **The last exchange** — the contact's N-th answer (N = 5 ± 1, drawn
  when the contact starts): answered like an exchange, and the page
  does not listen.
- **The Breakdown** — straight after the last exchange: the receiver
  fails; Samantha's fixed line tells the listeners, one reaction
  follows. Back to Broadcast.
- **The Switch-off** — two silences in a row: Samantha's fixed line
  (nobody answered, or the caller went quiet), switching the receiver
  off to save it; one reaction. Back to Broadcast.

**The emotional overtone.** Every round has one — positive, neutral
or negative — which sets its moods, its tone word and its event. The
beats and contact rounds take the overtones the story allows for
their kind; free rounds hold one for 4 ± 1 rounds, then drift to a
neighbor. A tone word is held for 3 ± 1 rounds and not repeated until
its list is used up.

### §6.5 Fixed lines

The lines the listener must not miss are said word for word by a cast
member instead of written by the model (`show.fixed_lines`, on):

- **an event** — read by the round's first speaker, its mood from the
  round's overtone; the model then reacts, at least one line;
- **the call** — an announcement by whoever of Daniel, Moira and Ralph
  has been silent longest, then Samantha's call; no model request;
- **the Breakdown** and **the Switch-off** — Samantha's line, then
  one reaction.

The texts are the event's own and the story's `beats.yaml`, drawn
without repeats; "Over." is added in code. Fixed lines stream to the
page through the same parser as the model's, are recorded with a
`fixed` flag, and reach the model only as described in §6.2 — never
as its own lines, which would teach it to repeat what it was just
told.

### §6.6 The listener's words

The page holds the microphone only while it listens: a window of
`listen_window_s` (10 s) that stops counting when the button goes
down, a press capped at `press_cap_s` (30 s). `POST /api/show/listen`
sends the audio to Whisper with the cast's names as the prompt and
the show's language. What Whisper most likely invented is treated as
silence: empty text, a high no-speech probability (`no_speech_max`),
a low average confidence (`logprob_min`), or one of Whisper's known
hallucinations. The page shows the words in the captions, each marked
by Whisper's confidence.

### §6.7 The trim

The script must stay within the model's context. The app does not count
tokens itself: after every round it keeps the model server's own count
(`timings`: `prompt_n` read fresh, `cache_n` reused from the cache,
`predicted_n` written), whose sum is the script's size, and each round's
share of it. Before each round, when the size reaches `trim_trigger` (90 %)
of `context_budget` (34,000 tokens), whole rounds leave the model's
reading, from the middle outwards — never the first `trim_keep_first` (2)
or the last `trim_keep_last` (4) — each taking its share off the size,
until the estimate is back to `trim_target` (50 %); the next round's count
is the real size. A round with no model request (the Repair) has no count:
the round after it counts its share from the last size the server reported,
so it takes in the Repair's tokens too, and the trim fires only before a
round that asks the model — the trim's estimate is exact to a few tokens,
and it lands up to one round under its target. The server then reads the
shortened script from the start: a pause of about 8.4 s at 32k (13,922
tokens), once every 100 rounds or more. When
a run opens, the app asks the model server its context (llama.cpp's
`/props`) and refuses the run if `trim_trigger × context_budget +
instruction_room` (1,000, for the next instruction) `+ max_tokens` does
not fit. In depth: [discussion 2026-10-01] the-app-from-the-outside §2.

### §6.8 The stream parser and the voice

The server cuts the model's stream at line breaks, trims trailing
whitespace, tolerates a line wrapped in quotation marks, keeps the
mood tag in the record and strips it from the spoken text, and
normalizes typographic punctuation for the voice (`’` and `‘` to `'`,
`“` and `”` to `"`, `—` to `, `, `…` to `...`). The page packs the
spoken text into chunks of whole sentences of up to about 100
characters (about 20 % of slack for a short ending such as "Over.",
a hard break at the end of each line) and plays each through
tts-serve in the speaker's voice. Asterisks the model writes for
emphasis are left in; the voice reads the emphasis.

**The voice follows the mood** (`show.mood_voices`, on). A persona's
folder holds its neutral voice, `ref.wav` with its transcript
`ref.txt`, and a recording per emotion, `ref-<emotion>.wav` with its
`.txt` (23 from the EARS dataset, cast by this repository's
`tools/voices/cast_voices.py --all-emotions`). The start of a run
gives the page the story's voices map; the page names the clip of
each line's mood with every chunk of the line, and the app's voice
route clones from that clip if the persona has it, else from
`ref.wav` (only `ref.wav` or `ref-<word>.wav`, inside the persona's
folder), and says which clip it used. Off, every line uses `ref.wav`.

**The seed of the voice** (`show.voice_seed`, off). Off, the page
sends no seed and tts-serve draws one per chunk. On, every chunk is
asked for with the run's seed, which the app fits into the range the
engine advertises for `seed` (Faster Qwen3-TTS: 1..1000) — so with
`show.seed` set, a run is said the same way twice. A seed makes a
voice reproducible, not steadier: the same clip, text and seed give
the same audio.

### §6.9 The record, the debug switch and the seed

Every run is recorded in `runs/<run-id>/script.json`: every round's
kind, instruction, speakers, lines (fixed ones flagged), what was
heard, timings and size. With `show.debug` on, each round also leaves
`runs/<run-id>/debug/`: the prompt exactly as the model read it
(rendered by the server's own template), the request body (replayable
with curl), the reply as it streamed, and a check that the rendered
prompt's size equals the size the server reported; the page shows a
line under each round with what the director chose and which clip
each line was spoken with. With debug on, every chunk the voice says
is kept too, in `runs/<run-id>/debug/audio/`, named by its place in
the run (`r009-l2-c1-Daniel-ref-fear.wav`: round 9, line 2, chunk 1),
with a `.json` of what made it (the text, the clip, the seed asked
for and the seed the engine used); the fork's
`scripts/replay_chunk.py` says one again and tells whether the audio
is byte-identical. The run's seed
(`show.seed`, or a random one) drives every choice the director makes
and seeds every model request, so a run replays exactly on the same
box and build.

### §6.10 The page and its looks

The page comes in looks; the show is the same in each. `/show`
opens a chooser: a card per look, each a live miniature of that look
playing a recorded stretch of a run, and the plain page last; below
the cards, a link to upstream's chat UI at `/talkwithme`. The root
`/` redirects to `/show`.

- **The plain page** — `/show?design=plain` (and any name that is
  not a look): `templates/show.html` with `static/show/`'s scripts
  and stylesheet — the text of the script, every control at hand. It
  is the working page, and the looks never change it: tests pin its
  HTML and its element ids.
- **A look** — `/show?design=<name>`, one folder per look in
  `static/show/designs/<name>/`: a `design.yaml` (its title, a line
  about it, its place in the chooser), a `design.css`, optionally a
  `design.js` and images with their credits.
  `templates/show_design.html` carries the plain page's elements with
  the same ids, so the same scripts run the show; the look restyles
  and rearranges those elements and adds its own drawing on top.
- **The gauge** — `static/show/gauge.js`, loaded in every look: it
  taps the page's audio from outside (the voice's output, and the
  microphone while the button is held) through Web Audio analysers,
  and publishes the level, smoothed, each frame, as CSS variables
  (`--level`, `--level-voice`, `--level-mic`) and to the look's
  script.
- **The static bed** — `static/show/bed.js`, loaded in every look (and
  on the plain page with `&bed=on`): radio static played quietly under
  the show, from the clips that ship with the app in `Sounds/bed/` —
  eight Freesound clips chosen by ear, CC0 and CC BY only, credited in
  `Sounds/bed/CREDITS.md`, each with the gain that evens it out
  (`bed.json`, written by this repository's
  `tools/sounds/prepare_bed.py`, which refuses any other licence); the
  story's `bed.yaml` switches each clip on or off and changes its level
  by ear. Shuffled, never the same clip across a reshuffle; each clip
  streamed through an `<audio>` element into the page's audio, mixed to
  mono. It follows the page's state from outside, as the gauge does:
  higher while the page waits, lower under a round, silent while the
  listener holds to talk, paused on Stop; silences on a timer give the
  ear rest; a slow fading (QSB) and an optional AM filter (a radio
  speaker's band) make it a receiver's. Keys: M mutes it, F flips the
  filter. The gauge never hears it.
- **The two looks:** `old-radio`, a photograph of a 1950 Philips
  Sirius BD 400 A (Wikimedia Commons, CC BY-SA 3.0, credited on the
  page) with the transcript on the speaker cloth, the magic eye as
  the receiver's light and the gauge, the dial lit while on air, a
  knob per character glowing while that character speaks, and the
  keys on the side panels; and `amateur-radio-transmitter`, a rack
  drawn in CSS with the transcript on an oscilloscope whose trace
  follows the gauge, a meter for the voice and one for the
  microphone, and a desk microphone.
- **A preview** — `&mock=1` on any look fills it from
  `static/show/designs/mock.js` (a recorded stretch, no server
  calls), for the chooser's miniatures and for designing.

### §6.11 Settings

Every number is a setting, under `show:` in the fork's
`settings.yaml` (`ShowConfig` in `app/config.py`): the story, the
model prefix, the token budgets (the reply, the context budget, the
instruction room), the trim's trigger, target and kept rounds, the seed,
the emotion tags, debug,
the mood voices, the voice's seed, the static bed (on or off, its two volumes, the dip and the rise, the
silences, the AM filter's band, the fading), the event and tone pacing, the free rounds' line budgets and weights,
the overtone's hold, the contact's length and line budgets, the
silences before a Switch-off, the beats' lines, the orientation and
recollection cadences, the restatement's reach, fixed lines, the
call's window, the listening window, the press cap and the Whisper
filter. Without a `show:` section every setting takes its default,
and the defaults are the demo's configuration. What to change to get
something done, recipe by recipe, with the address switches and the
keyboard shortcuts: the fork's `docs/runbooks/show-settings.md`. How
to run the show: `docs/runbooks/show-page.md` (the page) and
`docs/runbooks/show-driver.md` (a scripted listener, no browser).

## §7. Deployment and operations

- **Targets:** Linux only; the same Ansible deployment for a cloud
  box and a home GPU box (`deploy/ansible/`), one inventory per
  environment: `cloud`; `lan`, the home box deployed from the laptop
  over SSH; `local`, the same box deployed from itself, without SSH
  (its modules run on the box's system Python, not on the project's
  `.venv`, which a local run would otherwise pick from the PATH).
  Ansible runs from macOS or Linux. One command,
  `make ans-deploy ENV=<env>`, converges a box that has only SSH,
  Ubuntu and Docker to the whole model stack; a second run changes
  nothing. On a box already deployed, `ANS_ARGS="--check --diff"` shows
  what a deploy would change without applying it; on a box never
  deployed, a dry run stalls at the first health check, because it
  starts no service. The box's address is wired with
  `make ans-set ENV=<env> IP=<address>` (for the home box, the SSH
  alias `zr-3090`, so no address enters the file) and removed with
  `make ans-unset`. Each environment's `99-<env>.yml` overrides the
  shared settings (`common_vars.yml`): the user, the SSH key, and the
  two settings below.
- **The box:** a pinned provider image with a mature NVIDIA driver
  branch — `R570 CUDA 12.8 with Docker` on Ubuntu 24.04, or
  `Ubuntu Server 22.04 LTS R550 CUDA 12.4 with Docker`. The contract
  any provider must meet: Ubuntu, Docker, nvidia-container-toolkit, a
  driver for CUDA 12 (R525 or newer). A driver runs any CUDA runtime
  up to the version it reports, within its major version, so wheels
  built for 12.8 run on a 12.4 driver; a driver older than a wheel's
  major version fails. The CUDA generation is one variable
  (`zr_cuda_variant`, `cu128`) from which every torch pin and index
  derives; the base role checks the driver can run it before anything
  installs. Every engine that carries torch pins torch and its
  companions together from the matching PyTorch index (PyPI's default
  wheels float to the newest CUDA major). Each engine lives in its own
  container or virtual environment. A fresh box may hold the apt lock
  in Ubuntu's own updater for its first hour; the base role waits up
  to five minutes for it and then says why it stopped.
- **The home box:** the owner's Linux desktop with an RTX 3090
  (24 GB), Ubuntu 22.04 and a driver of the R580 branch, also used for
  other work. Its user's sudo asks for a password, typed at each
  deploy, start or stop (`ANS_ARGS=-K`). How to operate it:
  `docs/runbooks/home-gpu-3090.md`.
- **The services:** containers for llama.cpp and Whisper, a systemd
  unit for tts-serve, all bound to the box's loopback, all pinned
  (§4). Whether they come back after a reboot is one setting,
  `zr_start_at_boot`: on the cloud box they do, by themselves, in
  under a minute; on the home box nothing starts at boot. A deploy
  starts them either way; `make ans-start ENV=<env>` starts them by
  hand and waits until each answers, `make ans-stop` stops them. Where
  the downloads go is the other: on the cloud box, under the
  service user's home (`~/models`, `~/.cache/huggingface`, the voice's
  environment in `~/faster_qwen3tts`); on the home box, every model and
  the voice's environment in one folder, `~/zombie-radio-data`
  (`zr_data_dir`; the voice's checkpoint through `HF_HOME`), apart from
  the Docker images. A box is disposable: destroying it and deploying a new one
  takes one command and about 7-15 minutes, most of it model
  downloads.
- **The laptop:** `make client-mac` installs TalkWithZombies at a
  pinned fork tag into `~/TalkWithZombies-client`, from a standalone
  playbook that never reads the deployment inventories
  (`deploy/ansible/client-talkwithme-mac.yml`): the clone, a virtual
  environment, and seeded settings pointing at the tunnel's ports.
  `make ssh-tunnel ENV=<env>` opens the tunnel, as the environment's
  user and with its key; `make check` asks all three services for
  their health through it.
- **Providers:** Hyperstack first (proven), Scaleway as the European
  alternate, Vast.ai for development; the deployment starts at "an
  SSH-able Ubuntu box exists", so nothing in it is specific to a
  provider.
- **The day of the show:** an on-demand box provisioned the evening
  before and left running; the canned episode ready if the venue's
  network or the box fails; a fixed seed makes a retake reproducible.

## §8. Security

The box is short-lived but on the public internet. The realistic
adversaries are port scanners, people hunting free GPU time,
accidental leaks through this public repository, and hecklers — not
targeted attackers. The posture is sized for exactly that.

### §8.1 Authentication

None of the services (llama.cpp, tts-serve, whisper-fastapi, the
app) authenticates anyone. The SSH key is the whole authentication:
the services are bound to the box's loopback and reached only through
the tunnel. The system has one user — the person running the show —
so there is no rate limiting, no multi-user handling and no audit
log.

### §8.2 Firewall

The provider's security group is the enforced layer: inbound port 22
only. ufw stays off and is not relied on (Docker's published ports
bypass it; with every container bound to `127.0.0.1`, nothing is
published anyway). SSH is key-only, by the provider image's defaults.
After provisioning, check from outside that only port 22 answers.

### §8.3 Transport

The page is served from `http://localhost` on the laptop, which is a
secure context, so the microphone works without a certificate, a
domain or TLS. The laptop reaches the box through an SSH tunnel
(`ssh -L`): encryption, authentication and a single open port in one
move, the same on every provider and at home. The deployment offers
only its own key (`IdentitiesOnly=yes`), accepts a new box's host key
on first contact and fails on a changed one
(`StrictHostKeyChecking=accept-new`), and keeps its own `known_hosts`
under `~/.config/zombie-radio/`.

### §8.4 Secrets

- **Real secrets** (provider keys, tokens — none exist yet) belong in
  the reserved ansible-vault files.
- **Box addresses** are committed only as a `REPLACE_ME` sentinel. A
  real address lives only in the working tree, guarded by the
  repository's `NEVER_COMMIT` pre-commit hook (`.githooks/pre-commit`);
  the deploy refuses to run on a sentinel. Markdown is not scanned by
  the hook, so documents never carry a box address.
- **Voice samples and show assets** are never committed.

### §8.5 Abuse and hecklers

The tunnel closes the services to the internet, which is the whole
answer to free-compute abuse. A heckler's words reach the model as
in-fiction radio traffic; the cast are expected to absorb them in
the story.

### §8.6 Audience data

The show hears names and voices from strangers at a public event. The
app keeps no audio: a press goes to Whisper and only the words come
back. The words are kept, as text, in the run's record on the
laptop.

## §9. Open

What the first release still needs, or has not settled:

- **The real cast** — the four character bibles in the cast sheet and
  a reference voice clip per character.
- **The model** — an audition of the shortlisted LLMs in this engine
  (Nemotron Nano 9B v2 · Gemma 4 12B, a role-play variant ·
  Rocinante-X-12B · Qwen3.5-9B · Wayfarer-2-12B), including whether
  each writes the screenplay format on its own.
- **The voices** — a comparison of voice engines through tts-serve
  (a second engine deployed), the Whisper size, the stack's memory
  with two engines, and the line's mood carried into the voice.
- **Who a returning caller is** — code telling the model which
  earlier caller a voice is, by name.
- **The canned episode** and the demo runbook.
- **Polish** — the next round prefetched, episodes. (The dead-air
  static is done: the static bed rises while the page waits.)
- **Operations** — a tunnel that reconnects by itself, and a fallback
  for the venue's network.

## §10. Not chosen

- **TalkWithMe's one prompt per persona for the show** — a router
  call plus a call per persona, each seeing the others' lines
  relabeled: failure-prone by construction and slower (§11,
  [ADR-0003]).
- **A `[Name]:` output sanitizer** — under the shared screenplay
  context no line is ever relabeled, so there is no label to strip.
- **A voice-agent framework (Pipecat)** — TalkWithMe and tts-serve
  adapted instead ([ADR-0001]).
- **JSON-constrained output** — a JSON costume pulls the model toward
  code-like prose; the screenplay grammar keeps it in the text it
  writes best.
- **A thin fork close to upstream** — the show engine rewrites the
  core ([ADR-0002]).
- **Listening windows by round count** — rounds last seconds, and
  every window is a pause the audience hears; the window is timed in
  played audio.
- **An ASCII-only grammar** to keep typographic punctuation from the
  voice — it would make the grammar steer prose; the parser
  normalizes instead.
- **A repeat guard** that drops near-repeated lines — once fixed lines
  stopped appearing as the model's own lines, repeats stopped.
- **Wording that pins facts down** so the model cannot invent — the
  improvisation is the point (§1).

## §11. Decisions and evidence

- **Decisions:** [ADR-0001] build on TalkWithMe and tts-serve;
  [ADR-0002] fork TalkWithMe as TalkWithZombies in a sibling
  repository; [ADR-0003] one shared screenplay context, a director in
  code, the browser as the clock (`docs/decisions/`).
- **The product's shaping:** [discussion 2026-09-13]
  product-definition-brainstorm and audio-framework-survey;
  [discussion 2026-09-14] llm-default-survey (the LLM shortlist);
  [discussion 2026-09-16] prototype-first-inversion and
  storytelling-coherence-and-structure-adherence (the narrative-health
  framework).
- **The show engine:** [discussion 2026-09-21] prompt-structure and
  story-loop; [discussion 2026-09-22]
  grammar-and-prompt-cache-lessons; [discussion 2026-09-23]
  show-engine-design; [discussion 2026-09-25]
  show-slice-3-browser-plan; [discussion 2026-09-26]
  show-director-modes; [discussion 2026-09-28]
  narration-quality-challenges and prompt-sweep; [discussion 2026-09-29]
  voice-datasets-with-emotion (the cast's voices, the mood voices);
  [discussion 2026-10-01] the-app-from-the-outside (how the app counts
  the script's tokens and trims; every endpoint, for testing);
  [discussion 2026-10-01] sound-effects (the research, then the static
  bed: its design, its build, the clips chosen by ear).
- **Deployment:** [discussion 2026-09-17] ansible-deployment-shape;
  [discussion 2026-09-13] cloud-gpu-provider-survey; [discussion
  2026-10-02] local-gpu-deployment-plan (the home box);
  `deploy/ansible/README.md`.
- **Measurements:** `docs/experiments/` — the remote-split test
  (2026-09-14), the ADR-0003 gate and the emotion-field cost
  (2026-09-22), the listener memory and the radio beats (2026-09-26).
- **Where the work stands:** `docs/TODO.md`, `docs/roadmap.md`,
  `docs/follow-ups.md`.
