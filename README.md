# zombie-radio

An interactive, audio-only theater play performed live by **4 AI
voice actors**: scientists trapped in a lab during a zombie
breakout, broadcasting their struggle over the radio — a throwback
to Orson Welles' 1938 *War of the Worlds*. The twist: the radio
occasionally **listens**. Talk to it (push-to-talk), and the
characters answer back, remember your name, and ask for your help.

Two principles shape everything:

- **Local AI first, cloud-capable** — every show-time model
  (dialogue LLM, text-to-speech, speech recognition) is open and
  self-hosted; the backend deploys identically to a home Linux GPU
  box or a rented cloud GPU instance.
- **Theatrical live improvisation with LLMs** — the drama is
  improvised at broadcast time, not scripted.

## What the demo shows

The talk at the Austin Python Meetup sets out to show four things
([the goals, and where each one stands](docs/discussions/2026-09-30-demo-goals.md)):

1. **Story coherence and improvisation** — the LLM improvises the
   story as it goes, without repeating itself and without forgetting
   key parts of the interaction, including what a listener told the
   cast.
2. **Emotional voices in support of the narration** — speech
   synthesis with real human voices conveys credible emotions, in
   sync with the story.
3. **Automated deployment to a cloud GPU** — the whole AI side of the
   project installs easily on a cloud VM with Ubuntu, a capable CUDA
   GPU, and Docker with access to that GPU. *(Already demonstrated.)*
4. **Automated deployment to a local GPU** — the same installation
   works on a local PC running Ubuntu with an RTX 3090 (24 GB) or
   better. *(Demonstrated on the owner's RTX 3090.)*

## Status

**Building the MVP prototype** (since 2026-09-17). MVP targeted
for **2026-10-08**; the project will be presented in a talk at the
Austin Python Meetup in October 2026.

- **Foundation (validated):**
  [TalkWithMe](https://github.com/scorbo2/TalkWithMe) and
  [tts-serve](https://github.com/scorbo2/tts-serve), with llama.cpp
  serving the dialogue LLM and Whisper for speech recognition.
- **The app:** [TalkWithZombies](https://github.com/alfre2v/TalkWithZombies),
  our fork of TalkWithMe, where the show engine is built (tag
  `tz-0.7`): one shared script, a director in code, a screenplay
  grammar, and the browser as the show's clock.
- **The deployment:** Ansible + Docker stand up the model services
  on a rented cloud GPU box (or a local GPU machine) in about seven
  minutes; the app runs on a Mac laptop and reaches them through an
  SSH tunnel.

## Voices for the cast

The four characters speak with real human voices, cloned from short
reference clips of the [EARS](https://github.com/facebookresearch/ears_dataset)
dataset (CC BY-NC 4.0 — never committed here). Three tools in
[`tools/voices/`](tools/voices/) take them from the dataset to the
TalkWithZombies client, run from this repository's root:

```bash
# 1. Look at the speakers: gender, age, native language (here, the native American English women)
python3 tools/voices/fetch_ears.py --speakers-info --gender female --native "american english"

# 2. Download a neutral and a fearful clip for each of them, and write a page of players to listen
python3 tools/voices/fetch_ears.py --gender female --native "american english" --types emo_neutral_sentences,emo_fear_sentences --fetch

# 3. Download every emotion for the speakers you liked, and write a page of players for them
python3 tools/voices/fetch_ears.py --speakers 7,17,26,33 --types 'emo_*_sentences' --fetch

# 4. Screen them: does each clip say its transcript, and stay in the speaker's pitch? (Whisper, through the tunnel)
python3 tools/voices/screen_voices.py --speakers 7,17,26,33

# 5. Choose the cast in tools/voices/cast.yaml, then preview what the cast would write
uv run python tools/voices/cast_voices.py --all-emotions --dry-run

# 6. Cast: write each character's voice, and every emotion it recorded, into the app's Personas folder
uv run python tools/voices/cast_voices.py --all-emotions
```

**Listen before you choose — the page of players.** Every fetch ends by
writing a web page next to the clips it downloaded, named by the time
the fetch started — for example
`../zombie-radio-datasets/ears/index-2026-09-29T14:06:44.html` — and
prints its path on the last lines (`page: …`). Open it in Chrome: one
row per speaker, labelled with their gender, age bracket, native
language and ethnicity; one column per emotion fetched; a player in
every cell. So you can hear the same emotion — fear, say — from ten
speakers in a row, or one speaker across all 23 emotions, without
hunting for files. Each fetch writes a new page and never touches the
earlier ones, so the page of a broad shortlist (step 2) stays next to
the page of your favourites (step 3). The pages play the original
lossless clips (32-bit float WAV); they were used in Chrome, other browsers
untested.

In order: look at the speakers; download two clips each for a
shortlist, and listen on the page of players the fetch writes; download
every emotion for your favourites; screen them — some EARS speakers say
something before their sentence, or climb far above their normal pitch in
some emotions, and either can spoil a cloned line (the screening flags
those clips and writes a page of players to confirm them by ear,
`screen-<start time>.html`); choose the cast in
[`tools/voices/cast.yaml`](tools/voices/cast.yaml); cast. Each fetch
works as a dry run without `--fetch`. The clips land in
`../zombie-radio-datasets/`, beside this checkout; the voices land in
`~/TalkWithZombies-client/Personas/<Name>/` — `ref.wav`, the voice, and
with `--all-emotions` one `ref-<emotion>.wav` per recorded emotion
(`ref-fear.wav`, `ref-distress.wav`, … 23 with EARS). Which recording each
of the show's moods is spoken with is not decided here but in
TalkWithZombies' story (`stories/<story>/overtones.yaml`, under
`voices`), so a mood can be remapped there without recasting. The app
speaks with a new voice from its next line. Every step, with what to
expect: [the runbook](docs/runbooks/cast-voices.md).

**Who voices whom, and how to tell.** Two files keep track of which EARS
speaker is behind each character:

- [`tools/voices/cast.yaml`](tools/voices/cast.yaml) — **the decision**,
  in git (so every past cast is in its history): `cast:` maps each
  character to an EARS speaker (`Daniel: p007`), and `voice:` names the
  recording that becomes the character's `ref.wav`.
- `~/TalkWithZombies-client/Personas/<Name>/ref.source` — **what was
  actually written**, beside the audio (outside git): when the character
  was cast, the EARS credit, and one line per file — `ref.wav <-
  p007/emo_neutral_sentences`, `ref-fear.wav <- p007/emo_fear_sentences`,
  … It is rewritten at every cast, so it always describes the files in
  that folder. If it disagrees with `cast.yaml` (edited, not yet recast),
  `ref.source` is the truth about what the app speaks with.

To see the current cast at a glance:

```bash
for f in ~/TalkWithZombies-client/Personas/*/ref.source; do echo "$f: $(sed -n 2p "$f")"; done
```

Its output on 2026-09-30 (paths shortened), after the first cast:

```
…/Daniel/ref.source: ref.wav <- p007/emo_neutral_sentences
…/Moira/ref.source: ref.wav <- p026/emo_neutral_sentences
…/Ralph/ref.source: ref.wav <- p017/emo_neutral_sentences
…/Samantha/ref.source: ref.wav <- p033/emo_neutral_sentences
```

How `cast_voices.py` uses `cast.yaml`, for Daniel: it reads the
speaker's clips from `source:` + the speaker
(`../zombie-radio-datasets/ears/p007/`), writes into `personas:` + the
character's name (`~/TalkWithZombies-client/Personas/Daniel/`, which must
exist), turns the `voice:` recording into `ref.wav` and `ref.txt`, with
`--all-emotions` every `emo_<emotion>_sentences` into
`ref-<emotion>.wav` and `.txt`, and records it all in `ref.source`.

## Documentation

This repo's memory of record lives in [`docs/`](docs/README.md) —
start there: specs, architecture decision records, surveys,
experiments, and the active arc's state
([`docs/TODO.md`](docs/TODO.md)).

A 2024 predecessor of this idea lives at
[zombie_radio_ai](https://github.com/alfre2v/zombie_radio_ai)
(discontinued; the concept survived, the code did not).

## License

[MIT](LICENSE)
