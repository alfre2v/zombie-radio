# Runbook: give the cast real voices — from EARS to the app's Personas folder

*Living, undated (runbooks convention). The whole procedure, in order: find
voices in the EARS dataset, download only the clips you need, and cast them
as the show's four characters in the TalkWithZombies client. Why it is done
this way, and how it was proven: `docs/discussions/2026-09-29-voice-datasets-with-emotion.md`
(§11) and `docs/experiments/2026-09-29-ears-remote-fetch/`.*

## What goes where

```
hackTNT_2026/                              (the folder holding the clones side by side)
├── zombie-radio-claude/                   this repository's checkout (any name) — the tools
│   └── tools/voices/
│       ├── fetch_ears.py                  downloads EARS clips
│       ├── cast.yaml                      who voices whom — the only file you edit
│       └── cast_voices.py                 writes the voices into the app
└── zombie-radio-datasets/                 the downloads, outside git
    ├── README.txt                         what is here, and the licence
    └── ears/<speaker>/<type>.wav, .txt    one folder per EARS speaker; index-*.html pages

~/TalkWithZombies-client/Personas/<Name>/  the app's personas: ref.wav, ref.txt (and ref.source)
```

- **EARS** (Expressive Anechoic Recordings of Speech): 107 speakers, 22
  emotions plus neutral, recorded in an anechoic chamber at 48 kHz.
  **Licence CC BY-NC 4.0** — credit, non-commercial use only. The clips are
  never committed: this repository is public.
- **The app reads one clip per character**, `Personas/<Name>/ref.wav`, with
  its exact transcript in `ref.txt`, and reads it again on every line it
  speaks — a recast is heard from the next line, without restarting.

## Before you start

- A Mac with Python 3.12 and [uv](https://docs.astral.sh/uv/) (the cast
  script needs PyYAML, which comes with this repository's environment:
  `uv run` sets it up).
- This repository checked out; every command below runs **from its root**.
- The TalkWithZombies client installed (`make client-mac`), so that
  `~/TalkWithZombies-client/Personas/` holds the four characters' folders —
  the cast script never creates a persona.
- Internet access: the clips come from GitHub, where EARS publishes one zip
  per speaker; the fetch script pulls single files out of those zips with
  HTTP range requests, without downloading the zips.

## 1. Look at the speakers

```bash
python3 tools/voices/fetch_ears.py --speakers-info
```

One line per speaker — id, gender, age bracket, native language, ethnicity —
and the counts. Narrow it with filters, which work on every command below:

```bash
python3 tools/voices/fetch_ears.py --speakers-info --gender female --native "american english"
```

- `--gender female` or `--gender male`;
- `--age 36-45` — a bracket exactly as printed (18-25, 26-35, 36-45, 46-55,
  56-65, 66-75);
- `--native english` — any part of the native language;
- `--speakers 7,17,26-33` — speaker numbers or ranges.

## 2. Look at what one speaker recorded

```bash
python3 tools/voices/fetch_ears.py --list --speakers 7
```

Every file of the speaker, with its size, and the emotion read from its name.
The ones the cast uses are the read emotions, `emo_<emotion>_sentences` — the
same three sentences for every speaker, with a transcript. Two names are
spelled unlike the paper: `embarassment` and `extasy`. The unscripted
`emo_<emotion>_freeform` files are **not used** — they have no transcript
(the owner's decision, 2026-09-29).

## 3. Download a shortlist to listen to

A dry run first — each file and its size, and the total, nothing downloaded:

```bash
python3 tools/voices/fetch_ears.py --gender female --native "american english" --types emo_neutral_sentences,emo_fear_sentences
```

Then the same with `--fetch`:

```bash
python3 tools/voices/fetch_ears.py --gender female --native "american english" --types emo_neutral_sentences,emo_fear_sentences --fetch
```

- Each file is reported with "CRC ok" (byte for byte what EARS published),
  the bytes transferred, and its format and length.
- Files already downloaded are skipped ("already here").
- About 4 MB per speaker for these two clips.
- The run writes a page of players, `zombie-radio-datasets/ears/index-<start time>.html`:
  one row per speaker, one column per clip. **Open it in Chrome** (it plays
  32-bit float WAV) and listen.

## 4. Download every emotion for your favourites

```bash
python3 tools/voices/fetch_ears.py --speakers 7,17,26,33 --types 'emo_*_sentences'
python3 tools/voices/fetch_ears.py --speakers 7,17,26,33 --types 'emo_*_sentences' --fetch
```

The dry run, then the fetch: all 23 read emotions, about 46 MB per speaker.
The quotes around `'emo_*_sentences'` matter (the shell would expand the `*`).
The run's page shows those speakers with every emotion.

**The pages of players — listen before you choose.** Every fetch ends by
writing a web page next to the clips it downloaded, named by the time the
fetch started — for example
`zombie-radio-datasets/ears/index-2026-09-29T14:06:44.html` — and prints its
path on its last lines (`page: …`). Open it in Chrome: one row per speaker,
labelled with their gender, age bracket, native language and ethnicity; one
column per emotion fetched; a player in every cell. You can hear the same
emotion from ten speakers in a row, or one speaker across all 23 emotions,
without hunting for files. Each fetch writes a new page and never touches
the earlier ones, so the page of a broad shortlist (step 3) stays next to the
page of your favourites (step 4); rename a page to keep it recognizable (the
first one of this project is `index_all_speakers_2emo.html`). The pages play
the original lossless clips (32-bit float WAV); they were used in Chrome,
other browsers untested.

## 5. Choose the cast

Edit `tools/voices/cast.yaml`:

```yaml
cast:
  Daniel: p007
  Moira: p026
  Ralph: p017
  Samantha: p033

voice: emo_neutral_sentences
```

- `cast` — who voices whom: a character's name as in the Personas folder,
  and an EARS speaker whose clips are downloaded.
- `voice` — the clip that becomes each character's `ref.wav`.
- `loudness_dbfs` (-20) and `peak_dbfs` (-1) — the loudness target, so the
  four voices sound equally loud; `loudness_dbfs: null` keeps each clip's
  own level.
- `moods` — each show mood's EARS emotion, used only with `--with-moods`
  (step 6).
- `source` and `personas` — where the downloads and the app's personas are;
  leave them unless your layout differs.

## 6. Cast

A dry run first — what would be written, nothing changed:

```bash
uv run python tools/voices/cast_voices.py --dry-run
```

Then the cast — the whole cast, or only some characters:

```bash
uv run python tools/voices/cast_voices.py
uv run python tools/voices/cast_voices.py --only Moira
uv run python tools/voices/cast_voices.py --only Moira,Ralph
```

For each character it prints the clip, its length and its loudness before
and after. What it does:

- checks first, for every character, that the persona folder exists and the
  chosen clip and its transcript are downloaded — **if anything is missing it
  stops before changing anything**;
- on a character's first cast, keeps the placeholder voice as
  `ref.placeholder.wav` and `ref.placeholder.txt`;
- removes any earlier mood clips, so nothing of a previous voice survives a
  recast;
- converts the clip to mono 24 kHz 16-bit (with the Mac's `afconvert`),
  evens out its loudness, and writes `ref.wav`, `ref.txt` (the transcript)
  and `ref.source` (where the voice came from, with the EARS credit);
- never touches `prompt.md`, `language.txt` or `memories.txt`.

**With mood clips** — `ref-<mood>.wav` and `.txt` for each mood of
`cast.yaml`; the app does not use them until the "Mood clips" feature is
built (`docs/follow-ups.md`):

```bash
uv run python tools/voices/cast_voices.py --with-moods
```

## 7. Check

```bash
ls ~/TalkWithZombies-client/Personas/Moira
cat ~/TalkWithZombies-client/Personas/Moira/ref.source
afinfo ~/TalkWithZombies-client/Personas/Moira/ref.wav
```

Expect `ref.wav`, `ref.txt`, `ref.source` (and `ref.placeholder.*` after the
first cast); `ref.source` naming the speaker and the clip; `afinfo` reporting
`1 ch, 24000 Hz, Int16` and a length of about 7-15 s.

## 8. Listen

With the tunnel to the model services open (`make ssh-tunnel ENV=cloud`):

```bash
cd ~/TalkWithZombies-client && .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8765
```

Open <http://127.0.0.1:8765/> in Chrome, choose a look, and press Start. To
try another voice: edit a line of `cast.yaml` and run step 6 with `--only`
— the character speaks with the new voice from the next line, no restart.

## Going back to a placeholder voice

The script has no switch for it; copy by hand, and remove `ref.source`,
which would otherwise still name the EARS voice:

```bash
cd ~/TalkWithZombies-client/Personas/Moira && cp ref.placeholder.wav ref.wav && cp ref.placeholder.txt ref.txt && rm ref.source
```

A later cast keeps the existing `ref.placeholder.*` as they are.
