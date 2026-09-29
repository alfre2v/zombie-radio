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
