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
   `<type>.txt` when the type has one. Files already there at their full size
   are not fetched again ("already here"). Each fetch writes a page of its
   own, `datasets/ears/index-<start time>.html` (e.g.
   `index-2026-09-29T11:30:11.html`; `-2`, `-3` … on a clash) — this run's
   files as a grid of players, one row per speaker, one column per type — to
   compare voices side by side (Chrome plays 32-bit float WAV).
5. Every emotion for a few speakers — `--types` takes patterns:
   `python3 fetch_ears.py --speakers 12,34,56,78 --types 'emo_*_sentences'`
   (a dry run), then the same with `--fetch`. About 46 MB per speaker for
   all 23 (`p001`: 46.18 MB).

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

**Run 5 — 2026-09-29, 11:09:12-11:11:48 CDT, the shortlist's clips
fetched.** On the owner's order, after the exact sizes ("commit the docs,
then fetch both groups"; 404.73 MB, CC BY-NC 4.0):

```
python3 fetch_ears.py --gender female --native "american english" --types emo_neutral_sentences,emo_fear_sentences --fetch
python3 fetch_ears.py --gender male --native "american english" --types emo_neutral_sentences,emo_fear_sentences --fetch
```

The women done at 11:10:48, the men at 11:11:48, both exiting 0. Full
outputs: `raw/run5-fetch-female.txt`, `raw/run5-fetch-male.txt`. Their last
lines:

```
fetched: 250.09 MB
[903 requests, 254.403 MB transferred]

fetched: 154.64 MB
[571 requests, 157.337 MB transferred]
```

Summarized by the committed `summarize_fetch.py`
(`python3 summarize_fetch.py raw/run5-fetch-female.txt raw/run5-fetch-male.txt`;
output in `raw/run5-summary.txt`):

```
files with CRC ok: 190; speakers: 95
formats (Hz, bits, channels, format): [('48000', '32', '1', '3')]
emo_fear_sentences: 95 files, 8.2-18.8 s, median 11.6 s
emo_neutral_sentences: 95 files, 7.5-14.8 s, median 9.7 s
transferred beyond each file: 0.00-0.07 MB
```

No error and no missing file in either output. `du -sh datasets/ears`:
391M — the 95 speakers and `p001` from run 3, with `index.html` listing all
96.

**Change — 2026-09-29, ~11:30 CDT, the script (recipe steps 4-5 amended).**
On the owner's order: "yes, add the `emo_*_sentences` convenience so we can
get all emotions like: `python3 fetch_ears.py --speakers 12,34,56,78 --types
'emo_*_sentences' --fetch`"; and, for the page: "No, no javascript. This is a
one time run script. Instead let's differentiate the index.html by the
datetime it was initiated, so a new run produces:
`index-2026-09-29T11:30:11.html` (and if there are collisions in the seconds
- unlikely - just add a `-2`, `-3`, etc... )". The owner had renamed the page
of runs 3 and 5 to `datasets/ears/index_all_speakers_2emo.html`. What
changed: `--types` takes patterns (`*`, `?`, `[…]`, matched against each
speaker's files); a file already on disk at its full size is skipped
("already here"); each fetch writes `index-<start time>.html` listing that
run's files — fetched or already here — instead of rewriting `index.html`
from everything on disk. Checked offline: the pattern `emo_*_sentences`
picks `emo_extasy_sentences`; a type named twice is kept once; a pattern
matching nothing is reported; page names on a clash come out `…-3.html` for
the third. The frozen criteria covered runs 1-5; the change is a
convenience, not a new question.

**Run 6 — 2026-09-29, 11:35:29 CDT, a dry run with the pattern.**

```
python3 fetch_ears.py --types 'emo_*_sentences' --speakers 1
```

Full output: `raw/run6-dryrun-p001-all-emotions.txt` — 23 files listed,
`emo_fear_sentences` and `emo_neutral_sentences` "(already here)", the other
21 "(would fetch)"; its last lines:

```
would fetch: 42.18 MB

[5 requests, 0.040 MB transferred]
```

**Run 7 — 2026-09-29, 14:05:13-14:10:53 CDT, every emotion for the owner's
20 speakers.** The owner decoupled the download from the casting script
(`docs/discussions/2026-09-29-voice-datasets-with-emotion.md` §11.4) and
named the shortlist — women p106, p100, p092, p063, p062, p059, p033, p026;
men p102, p101, p095, p088, p087, p086, p085, p057, p054, p046, p017, p007.
Only the `sentences` clips: the unscripted `emo_*_freeform` ones have no
transcript and are set aside (the owner: "Correct, we have no use for those
now (maybe in the future)"). The dry run first, 14:05:13-14:05:26:

```
python3 fetch_ears.py --speakers 106,100,92,63,62,59,33,26,102,101,95,88,87,86,85,57,54,46,17,7 --types 'emo_*_sentences'
```

Full output: `raw/run7-dryrun-20-speakers.txt` — 420 files "(would
fetch)", 40 "(already here)" (neutral and fear, from run 5), none missing;
its last lines:

```
would fetch: 911.14 MB

[81 requests, 0.344 MB transferred]
```

Then, on the owner's approval ("Fetch the files."), 14:06:43-14:10:53, exit
0:

```
python3 fetch_ears.py --speakers 106,100,92,63,62,59,33,26,102,101,95,88,87,86,85,57,54,46,17,7 --types 'emo_*_sentences' --fetch
```

Full output: `raw/run7-fetch-20-speakers.txt` — 420 lines "CRC ok", 40
"(already here)", no error; its last lines:

```
fetched: 911.14 MB
page: /Users/alfredo/workspace/hackTNT_2026/zombie-radio-claude/docs/experiments/2026-09-29-ears-remote-fetch/datasets/ears/index-2026-09-29T14:06:44.html

[2581 requests, 924.951 MB transferred]
```

Summarized by `python3 summarize_fetch.py raw/run7-fetch-20-speakers.txt`
(`raw/run7-summary.txt`; the 40 files already here are not in it):

```
files with CRC ok: 420; speakers: 20
formats (Hz, bits, channels, format): [('48000', '32', '1', '3')]
emo_adoration_sentences: 20 files, 8.9-19.1 s, median 12.7 s
emo_amazement_sentences: 20 files, 6.1-12.1 s, median 9.0 s
emo_amusement_sentences: 20 files, 8.0-15.6 s, median 11.1 s
emo_anger_sentences: 20 files, 9.0-17.2 s, median 12.7 s
emo_confusion_sentences: 20 files, 4.5-15.7 s, median 8.1 s
emo_contentment_sentences: 20 files, 6.9-14.0 s, median 9.2 s
emo_cuteness_sentences: 20 files, 6.4-14.7 s, median 9.3 s
emo_desire_sentences: 20 files, 8.4-14.8 s, median 11.1 s
emo_disappointment_sentences: 20 files, 9.2-19.1 s, median 12.3 s
emo_disgust_sentences: 20 files, 6.9-14.2 s, median 10.9 s
emo_distress_sentences: 20 files, 7.3-17.5 s, median 11.3 s
emo_embarassment_sentences: 20 files, 9.4-15.3 s, median 11.7 s
emo_extasy_sentences: 20 files, 7.4-12.9 s, median 9.6 s
emo_guilt_sentences: 20 files, 6.6-12.1 s, median 9.2 s
emo_interest_sentences: 20 files, 6.8-14.6 s, median 10.0 s
emo_pain_sentences: 20 files, 8.0-16.5 s, median 11.6 s
emo_pride_sentences: 20 files, 9.6-17.6 s, median 14.1 s
emo_realization_sentences: 20 files, 10.9-31.6 s, median 15.7 s
emo_relief_sentences: 20 files, 8.6-14.6 s, median 10.7 s
emo_sadness_sentences: 20 files, 8.3-16.6 s, median 12.8 s
emo_serenity_sentences: 20 files, 8.2-17.8 s, median 12.5 s
transferred beyond each file: 0.00-0.07 MB
```

Checked by listing each speaker's folder: all 20 hold 23
`emo_*_sentences.wav` and 23 `emo_*_sentences.txt`. `du -sh
datasets/ears`: 1.2G. The owner's review page:
`datasets/ears/index-2026-09-29T14:06:44.html` — 20 rows, 23 columns.

