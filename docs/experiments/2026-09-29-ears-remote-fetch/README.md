# EARS remote fetch — single WAV files out of the per-speaker zips, without downloading them — runlog

**Question:** can we choose EARS voices and fetch single lossless WAV files
without downloading the dataset — (a) what the speaker metadata tells us
(how many speakers, who is who), (b) what file types each speaker has and
whether the emotion can be read from the file name, (c) whether one file can
be pulled out of a speaker's zip with HTTP range requests?
**Timebox:** 1.5 hours from the first run. **Abort criteria:** if single
files cannot be pulled out of the zips within the timebox — the server
refusing ranges, or the zips unreadable this way — stop and record it; the
fallback is whole per-speaker zips (564-804 MB each) for a short list chosen
by ear.
**Provenance:** `docs/discussions/2026-09-29-voice-datasets-with-emotion.md`
(§6.1, EARS; §9, the listening test this feeds) · `docs/TODO.md`, Task 4,
the reference voices · `docs/follow-ups.md`, "Mood clips" and "Voice-sample
hygiene".

**The owner's request (verbatim, 2026-09-29):** "I think it is time for an
experiment: Let's create a new experiment folder in zombie-radio and write
some python (or bash, whatever fits best) to see if we can actually fetch:
(a) Do we have metadata about speakers? To answer things like: How many
speakers are there? Can we know anything about each speaker, e.g which one is
male or female? (b) Do we have metadata about the audio types? To answer
things like: How many audio types are there for each speaker, and what are
their name format. Can we map the file name format to the emotion? (c) You
mentioned the possibility of being able to request from the server a single
audio file without having to download the whole database files... Let's
exercise this". Why: the Hugging Face viewer is slow, pages through many
voices the owner dislikes, cannot line up the same file type across speakers,
and plays lossy copies.

## Execution model

Everything runs on the laptop; no box, no tunnel. The script reads two
public JSON files from the EARS repository and the zips' tables of contents
(a few kilobytes each), and fetches WAV files only with `--fetch`, after the
owner approved the list and the sizes. **The audio never enters the
repository:** EARS is CC BY-NC 4.0 and this repository is public (the
follow-up "Voice-sample hygiene"); fetched files land in `datasets/`, which
this folder's `.gitignore` excludes.

## Reproduction recipe

From this folder, with Python 3.12 (standard library only):

1. The speakers and their metadata (a):
   `python3 fetch_ears.py --speakers-info` — filters: `--gender female`,
   `--age 26-35`, `--native english`.
2. One speaker's files and sizes (b): `python3 fetch_ears.py --list --speakers 1`;
   several speakers' types compared: `--list --speakers 1-5`.
3. What a fetch would bring, and its size (c), without downloading:
   `python3 fetch_ears.py --types emo_neutral_sentences,emo_fear_sentences --speakers 1-5`.
4. The fetch itself, after the owner's approval: the same with `--fetch`;
   files land in `datasets/ears/<speaker>/<type>.wav`, with the transcript in
   `<type>.txt` when the type has one, and `datasets/ears/index.html` — every
   fetched file as a grid of players, one row per speaker, one column per
   type — to compare voices side by side (Chrome plays 32-bit float WAV).

Every run ends with the number of requests and the bytes transferred, the
evidence that a zip was not downloaded. The zip module checks each fetched
file's CRC-32 against the one stored in the zip; "CRC ok" means the file is
byte for byte what EARS published.

## Runlog

*Every command actually run, in order, with its output.*

**Run 1 — 2026-09-29, 10:42:58 CDT, the speakers (a).** After the freeze
(`2359962`), on the owner's order ("commit, then run the first two
commands"):

```
python3 fetch_ears.py --speakers-info
```

Full output: `raw/run1-speakers-info.txt` (one line per speaker: id,
gender, age bracket, native language, ethnicity). Its last lines:

```
107 speakers: 60 female, 43 male, 1 non-binary / third gender, 3 prefer not to answer

[1 requests, 0.024 MB transferred]
```

Seen in the file: ages come as brackets (18-25 … 66-75); native languages
are mostly American English, with British English (p008), German (p001),
Mandarin (p005), Ukrainian (p013), Spanish (p042), Dari (p067) and Russian
(p107); two speakers answered "prefer not to answer" to everything (p072,
p103).

**Run 2 — 2026-09-29, 10:43:04 CDT, one speaker's files (b).**

```
python3 fetch_ears.py --list --speakers 1
```

Full output: `raw/run2-list-p001.txt`. Its first and last lines:

```
p001: 161 WAV files, 592 MB
...
[5 requests, 0.040 MB transferred]
```

Seen in the file: 161 types for `p001` — 46 emotional files,
`emo_<emotion>_sentences` and `emo_<emotion>_freeform` for 22 emotions plus
neutral, the `sentences` files 1.30-2.89 MB; six `freeform_speech_01`…`06`
of 34.6-35.8 MB; interjections (agreement, anger, congratulations, filler,
greetings); nonverbal sounds (cheering, crying, laughter, screaming,
yelling); `rainbow_01`…`08` and `sentences_01`…`24` read in the reading
styles (fast, highpitch, loud, lowpitch, regular, slow, whisper); vegetative
sounds (coughing, eating, sneezing, throat, yawning); one song
(`melodic_happy_birthday`). No file is marked "(compressed)": the zip stores
them uncompressed. Two emotion names are spelled in the files unlike in the
paper: `embarassment` and `extasy`. The table of contents of a 592 MB zip
was read with 5 requests and 40 KB.

**Run 3 — 2026-09-29, 10:45:18 CDT, two files fetched (c).** On the owner's
approval ("yes, fetch the two files for p001"; 3.99 MB, CC BY-NC 4.0):

```
python3 fetch_ears.py --types emo_neutral_sentences,emo_fear_sentences --speakers 1 --fetch
```

Full output (`raw/run3-fetch-p001.txt`):

```
p001/emo_neutral_sentences.wav  1.79 MB, CRC ok, 1.84 MB transferred  [48000 Hz, 32-bit, 1 ch, format 3, 9.3 s]
p001/emo_fear_sentences.wav  2.20 MB, CRC ok, 2.23 MB transferred  [48000 Hz, 32-bit, 1 ch, format 3, 11.4 s]

fetched: 3.99 MB
index: /Users/alfredo/workspace/hackTNT_2026/zombie-radio-claude/docs/experiments/2026-09-29-ears-remote-fetch/datasets/ears/index.html

[17 requests, 4.129 MB transferred]
```

Format 3 is IEEE float: 48 kHz, 32-bit float, mono. On disk (`ls -l`):
`emo_neutral_sentences.wav` 1,793,994 bytes, `emo_fear_sentences.wav`
2,197,966 bytes, with their transcripts beside them:
`emo_neutral_sentences.txt` — "That wall in the living room is white. There
is one more piece of bread in the pantry. The store closes at 8pm tonight.";
`emo_fear_sentences.txt` — "Did you hear that sound? I'm afraid someone or
something is outside. Oh my gosh, what is that? What do you think is going to
happen if we don't run?". `git status --ignored` lists `datasets/` as ignored
(`!!`).

**The verdict — 2026-09-29, the owner (verbatim):** "This is a PASS indeed.
Good job!" (`findings.md`).

**Run 4 — 2026-09-29, 10:55:56-10:56:55 CDT, dry runs for the owner's
shortlist.** The owner asked for the fetch the agent had proposed ("Ok,
let's run the sampling command you propose for me to create my shortlist");
the dry runs came first:

```
python3 fetch_ears.py --gender female --native "american english" --types emo_neutral_sentences,emo_fear_sentences
python3 fetch_ears.py --gender male --native "american english" --types emo_neutral_sentences,emo_fear_sentences
```

Full outputs: `raw/run4-dryrun-female.txt`, `raw/run4-dryrun-male.txt`.
Their last lines:

```
would fetch: 250.09 MB
[233 requests, 0.950 MB transferred]

would fetch: 154.64 MB
[149 requests, 0.615 MB transferred]
```

116 files for 58 women and 74 for 37 men, none missing — both types exist in
every one of those 95 zips. The agent had told the owner about 130 MB and
140 MB, having miscounted the women (32 instead of 58); the fetch waits for
the owner's word on the exact sizes. Speakers per age bracket, counted in
`raw/run1-speakers-info.txt`: women 18-25: 13, 26-35: 12, 36-45: 7, 46-55:
14, 56-65: 10, 66-75: 2; men 18-25: 12, 26-35: 9, 36-45: 8, 46-55: 4,
56-65: 4.
