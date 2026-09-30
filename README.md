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

## Status

**Building the MVP prototype** (since 2026-09-17). MVP targeted
for **2026-10-08**; the project will be presented in a talk at the
Austin Python Meetup in October 2026.

- **Foundation (validated):**
  [TalkWithMe](https://github.com/scorbo2/TalkWithMe) and
  [tts-serve](https://github.com/scorbo2/tts-serve), with llama.cpp
  serving the dialogue LLM and Whisper for speech recognition.
- **The app:** [TalkWithZombies](https://github.com/alfre2v/TalkWithZombies),
  our fork of TalkWithMe, where the show engine is being built: one
  shared script, a director in code, a screenplay grammar, and the
  browser as the show's clock.
- **The deployment:** Ansible + Docker stand up the model services
  on a rented cloud GPU box (or a local GPU machine) in about seven
  minutes; the app runs on a Mac laptop and reaches them through an
  SSH tunnel.

## Voices for the cast

The four characters speak with real human voices, cloned from short
reference clips of the [EARS](https://github.com/facebookresearch/ears_dataset)
dataset (CC BY-NC 4.0 — never committed here). Two tools in
[`tools/voices/`](tools/voices/) take them from the dataset to the
TalkWithZombies client, run from this repository's root:

```bash
# 1. Look at the speakers: gender, age, native language (here, the native American English women)
python3 tools/voices/fetch_ears.py --speakers-info --gender female --native "american english"

# 2. Download a neutral and a fearful clip for each of them, and write a page of players to listen
python3 tools/voices/fetch_ears.py --gender female --native "american english" --types emo_neutral_sentences,emo_fear_sentences --fetch

# 3. Download every emotion for the speakers you liked, and write a page of players for them
python3 tools/voices/fetch_ears.py --speakers 7,17,26,33 --types 'emo_*_sentences' --fetch

# 4. Choose the cast in tools/voices/cast.yaml, then preview what the cast would write
uv run python tools/voices/cast_voices.py --dry-run

# 5. Cast: write each character's voice into the app's Personas folder
uv run python tools/voices/cast_voices.py
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
every emotion for your favourites; choose the cast in
[`tools/voices/cast.yaml`](tools/voices/cast.yaml); cast. Each fetch
works as a dry run without `--fetch`. The clips land in
`../zombie-radio-datasets/`, beside this checkout; the voices land in
`~/TalkWithZombies-client/Personas/<Name>/ref.wav`, and the app speaks
with a new voice from its next line. Every step, with what to expect:
[the runbook](docs/runbooks/cast-voices.md).

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
