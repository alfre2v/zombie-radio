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
