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

## Who voices whom — where it is kept

Two files say which EARS speaker is behind each character; keep both in
mind.

| | What it says | Where | In git? |
|---|---|---|---|
| `tools/voices/cast.yaml` | **the decision**: `cast:` maps each character to an EARS speaker (`Daniel: p007`); `voice:` names the recording that becomes `ref.wav` | this repository | **yes** — every past cast is in its history (`git log -p tools/voices/cast.yaml`) |
| `Personas/<Name>/ref.source` | **what was actually written**: when, the EARS credit, and one line per file | each persona's folder in the client, beside the audio | no |

A `ref.source` after a cast with `--all-emotions` (Daniel's, from the test
of 2026-09-30 on a copy of the Personas folder; 25 lines — the header,
`ref.wav`, and the 23 recordings):

```
cast 2026-09-30T14:55:31 from EARS, CC BY-NC 4.0 (Richter et al., Interspeech 2024)
ref.wav <- p007/emo_neutral_sentences
ref-adoration.wav <- p007/emo_adoration_sentences
ref-amazement.wav <- p007/emo_amazement_sentences
...
ref-serenity.wav <- p007/emo_serenity_sentences
```

It is rewritten at every cast, so it always describes exactly the files in
its folder. **If the two disagree** — `cast.yaml` edited but the character
not recast — `ref.source` is the truth about what the app speaks with, and
`cast.yaml` only the intention. The current cast at a glance:

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

**How `cast_voices.py` uses `cast.yaml`**, followed for Daniel:

```yaml
source: ../zombie-radio-datasets/ears        # where the EARS downloads are (relative to the checkout)
personas: ~/TalkWithZombies-client/Personas  # where the app's personas are
cast:
  Daniel: p007                               # which EARS speaker voices which character
voice: emo_neutral_sentences                 # which recording becomes ref.wav
```

1. **Who, and from where:** `cast` gives Daniel → p007; the clips are read
   from `source` + the speaker: `../zombie-radio-datasets/ears/p007/`.
2. **To where:** `personas` + the character's name:
   `~/TalkWithZombies-client/Personas/Daniel/` — the folder must exist (the
   script never creates a persona), and the name must match it exactly.
3. **The voice:** the `voice` recording becomes `ref.wav` —
   `p007/emo_neutral_sentences.wav` → `Daniel/ref.wav`, its transcript →
   `ref.txt`.
4. **With `--all-emotions`:** every `emo_<emotion>_sentences.wav` in
   `p007/` that has its `.txt` becomes `Daniel/ref-<emotion>.wav` and
   `.txt`.
5. **Recorded:** all of it in `Daniel/ref.source`.

`--only Moira` limits a run to the characters named; everything else comes
from `cast.yaml`. Which of the show's moods is spoken with which recording
is neither file's business: it is the story's (`voices` in TalkWithZombies'
`stories/<story>/overtones.yaml`).

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
- Which show mood is spoken with which recording is **not** here: it is
  the story's, in TalkWithZombies' `stories/<story>/overtones.yaml`, under
  `voices` (`afraid: ref-fear.wav`). This file only says whose voice; the
  casting copies every recording (step 6, "With every emotion"), so a
  mood can be remapped in the story at any time without recasting.
- `source` and `personas` — where the downloads and the app's personas are;
  leave them unless your layout differs.

## 6. Cast

A dry run first — what would be written, nothing changed:

```bash
uv run python tools/voices/cast_voices.py --all-emotions --dry-run
```

Then the cast — the whole cast, or only some characters — each with its
voice and every emotion it recorded (see "With every emotion" below):

```bash
uv run python tools/voices/cast_voices.py --all-emotions
uv run python tools/voices/cast_voices.py --all-emotions --only Moira
uv run python tools/voices/cast_voices.py --all-emotions --only Moira,Ralph
```

Without `--all-emotions` only `ref.wav` is written — every mood then falls
back to it, and the voices carry no emotion of their own.

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

**With every emotion** (`--all-emotions`) — every read emotion the
speaker recorded, copied as recorded and named after it: `ref-fear.wav` and
`ref-fear.txt` from `emo_fear_sentences`, `ref-distress.wav` from
`emo_distress_sentences`, and so on — all 23 with EARS, neutral included,
about 12 MB per character. `ref.wav`, the voice, is written as always.

The app speaks each line with the recording its mood names in the story's
`voices`, when `show.mood_voices` is on (the TalkWithZombies runbook
`docs/runbooks/show-page.md`, "The voice"). Because every recording is
there, remapping a mood in the story needs no recast; a recording the story
names that a persona lacks falls back to `ref.wav` (the debug line shows
which clip spoke). An emotion that is not downloaded for the speaker is
simply not copied — the script says how many it found; fetch the rest
(step 4) and recast.

## 7. Check

```bash
ls ~/TalkWithZombies-client/Personas/Moira
cat ~/TalkWithZombies-client/Personas/Moira/ref.source
afinfo ~/TalkWithZombies-client/Personas/Moira/ref.wav
```

Expect `ref.wav`, `ref.txt`, `ref.source` (and `ref.placeholder.*` after the
first cast; with `--all-emotions`, a `ref-<emotion>.wav` and `.txt` for each
of the 23 read emotions); `ref.source` naming the speaker and each clip;
`afinfo` reporting `1 ch, 24000 Hz, Int16` and a length of about 7-15 s.

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
