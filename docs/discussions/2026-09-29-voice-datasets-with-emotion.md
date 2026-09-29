# Voice datasets with emotion — real voices for the cast, one speaker in several moods

**Date:** 2026-09-29 (the research began the night before) · **Arc:** MVP
prototype · **Branch:** `alfre2v/voice-datasets`
**Type:** discussion — online research into datasets of real human voices
recorded in several emotions, as the source of the cast's reference clips;
the owner asks and decides, the agent researches and verifies.
**Status:** OPEN — four finalists (§6): **EARS**, **CREMA-D**,
**JL-Corpus** and **Expresso**. **EARS single files can be fetched without
the zips** — an experiment passed on 2026-09-29, with a script anyone can
run (§11, the addendum of that day, has how to use it); the owner's
shortlist of EARS voices is next, then the listening test (§9). This
document is updated as the real audio files are tried: each
finding lands as a dated addendum (§11), never as a silent rewrite.

**The owner's request (verbatim, 2026-09-29):** "I think it is time to open a
new discussion document to save this research results and our back and forth
in the matter. We will probably have to update this document frequently based
on what we discover when we try to use the actual audio files." And: "I want
JL corpus to be in the finalist datasets too. Add it to the results to be
saved to the file." And, on Expresso: "yes, add Expresso as the fourth
finalist."

**Where it fits:** the TODO's Task 4, the reference voices (the owner's, next
after the timebox), and the follow-up "Mood clips — several reference clips
per character, one per mood" (`ref-<mood>.wav` next to `ref.wav`).

## §1. The question

The owner (verbatim, the night of 2026-09-28):

> I have been thinking how to find good quality reference audios without
> losing time searching for individual audio clips online and having to clean
> them of background noises.
>
> It's time for you to change hats and go into online research mode, question:
>
> Is there any real human voices dataset, that:
>
> (a) provide audio samples of the same speaker in different emotional
> entonation (e.g. speaker1: emotion happy, speaker 1: emotion anger, etc.)
> (b) that is free to use for commercial / non-commercial projects (MIT
> license compatible).

The two costs the owner wants to avoid: hunting for individual clips, and
cleaning background noise out of them (the follow-up "Find the
voice-isolation tool from scorbo2's podcast" exists for that cleaning). A
dataset recorded for research is clean by construction and labelled by
emotion, and one speaker in several emotions gives the mood clips of one
character in one voice.

## §2. What a reference clip needs

What the show's voice engine takes (Faster Qwen3-TTS through tts-serve 1.2;
the TODO's owner action queue, item 1, and Task 4):

- **Length:** about 10 seconds of clean speech — no music or crosstalk under
  the voice; the engine requires at least 2 s, and a transcript.
- **Transcript:** exact, word for word, in `ref.txt`.
- **Format:** mono 24 kHz 16-bit is the safest
  (`afconvert -f WAVE -d LEI16@24000 -c 1 in.wav ref.wav` on the Mac).
- **Place:** `~/TalkWithZombies-client/Personas/<Name>/ref.wav` and `ref.txt`,
  outside both repositories — the fork gitignores `Personas/`, and the Mac
  installer never overwrites an existing persona folder. Mood clips, when
  built: `ref-<mood>.wav` and `ref-<mood>.txt` next to them.
- **The show's moods** — the fourteen of the story (the fork's
  `stories/lab-outbreak/overtones.yaml`): positive — happy, hopeful, excited,
  relieved; neutral — calm, doubtful, urgent, curious, determined; negative —
  sad, afraid, terrified, angry, exhausted.

Because a dataset's licence covers files that stay outside both
repositories, no licence mixes with the MIT code; what remains is using the
clips within their licence — for the talk, crediting the dataset.

## §3. Round 1 — commercial use allowed (the night of 2026-09-28)

Each licence was checked at the dataset's official source, not at a mirror
or a list (see §5 for why).

| Dataset | Voices | Emotions | Audio | Licence |
|---|---|---|---|---|
| **JL-Corpus** | 4 trained voice actors, 2 women and 2 men, New Zealand English | 10: angry, anxious, apologetic, assertive, concerned, encouraging, excited, happy, neutral, sad | 44.1 kHz, 16-bit | **CC0** (public domain) |
| **CREMA-D** | 91 actors (48 men, 43 women), ages 20-74, of diverse races and ethnicities, English | 6: anger, disgust, fear, happy, neutral, sad, with intensity levels | 16 kHz WAV | ODbL, with the clips under the DbCL |
| **EMNS** | 1 woman, British English | 8 acted emotions, with intensity labels | WebM (compressed); 42 MB cleaned | Apache 2.0 |

The agent's picks that night: **JL-Corpus** first (public domain, a high
sample rate, two women's and two men's voices, and emotions near a lab under
siege — angry, anxious, concerned, excited, sad); **CREMA-D** as the fallback
(many voices, lower quality: 16 kHz, some files with audio problems corrected
in 2020, every actor saying the same 12 short sentences); EMNS well rated for
expressiveness but a single voice.

## §4. Round 2 — non-commercial use (the night of 2026-09-28)

The owner (verbatim): "Let's relax the criteria b, let's consider databases
we can use for non-commercial projects like this one."

| Dataset | Voices | Emotions | Audio | Licence |
|---|---|---|---|---|
| **EARS** (Meta and the University of Hamburg, Interspeech 2024) | **107 speakers**, ages 18-75, with metadata (gender, age, first language) | **22**: adoration, amazement, amusement, anger, confusion, contentment, cuteness, desire, disappointment, disgust, distress, embarrassment, ecstasy, fear, guilt, interest, pain, pride, realization, relief, sadness, serenity — plus neutral | 48 kHz, 32-bit, recorded in an anechoic chamber | CC BY-NC 4.0 (the repository's `LICENSE` file) |
| **Expresso** (Meta, 2023) | 4 (2 men, 2 women) | read: confused, default, enunciated, happy, laughing, narration, sad, whisper; improvised dialogue: 26 styles, among them angry, fearful, calm, sleepy (§6.4) | 48 kHz / 24-bit, studio | CC BY-NC 4.0 |
| **RAVDESS** | 24 actors (12 men, 12 women) | 8 (neutral, calm, happy, sad, angry, fearful, surprise, disgust), two intensities | 48 kHz | CC BY-NC-SA 4.0 (a commercial licence can be bought) |

**Why EARS led:** it removes the problem the question started from — every
recording is clean, made in an anechoic chamber. For each emotion, each
speaker reads the same three sentences in one file
(`emo_<emotion>_sentences`), with transcripts in `transcripts.json` — about
10-15 seconds (the agent's estimate, not measured), close to what the voice
engine wants; each speaker also describes an image in each emotion, unscripted
(`emo_<emotion>_freeform`, no transcript — Whisper on the box can draft one).
Its emotions include fear, distress, anger, sadness, pain, relief, confusion
and amusement, and 107 speakers leave room to pick four that sound clearly
different. **Expresso**: set aside that night as "only four voices and a
single 36 GB download" — too quickly, and with an error: its angry and fearful
styles are only in the improvised dialogues, not in the read speech. The owner
questioned it the next day and it became a finalist (§6.4). **RAVDESS**: good quality, but every actor says the
same two sentences, in clips of 3-4 seconds — thin material for cloning.

**What CC BY-NC asks of us:** credit (the dataset's name and authors, on a
slide or in the credits) and no commercial use — both fit the talk at the
Austin Python Meetup. RAVDESS's share-alike would bind a redistributed
derivative; the clips are not redistributed.

## §5. Excluded, and the licence traps

| Dataset | Why it is out |
|---|---|
| ESD (Emotional Speech Dataset) | research only, under a signed licence agreement ("This database can only be used for research purpose.") — a public talk is a stretch |
| EmoV-DB | its own non-commercial licence ("research, teaching, scientific publication and personal experimentation") — arguable for a talk; no fear or sadness either |
| eNTERFACE'05 | released for scientific research; an audio-visual set of non-native speakers |
| MEAD | a video dataset (60 actors, 8 emotions, 3 intensities); a search called it MIT, but its README states no terms for the data — unknown terms |
| TESS | non-commercial; two actresses saying single words in a carrier phrase ("Say the word ____") |

**The traps, seen during the research:**

- **Mirrors mislabel licences.** A web search, drawing on a Kaggle mirror,
  reported ESD as Apache 2.0; ESD's own repository says research only, under
  an agreement. Only the dataset's own page counts.
- **A tool's licence is not the data's.** EMNS was first found as "Apache
  2.0" for its *collection tool*; the dataset's own page on OpenSLR then
  confirmed Apache 2.0 for the recordings too.
- **Different platforms, different licences.** TESS is listed as CC BY-NC 4.0
  on its official Borealis entry and as CC BY-NC-ND 4.0 elsewhere.
- **A repository without a licence file.** JL-Corpus's GitHub repository has
  none; its CC0 comes from the authors' own statements — their Interspeech
  paper and their own Kaggle upload (§6.3).

## §6. The finalists

**EARS** and **CREMA-D** from the research; **JL-Corpus** added by the owner
on 2026-09-29 (verbatim): "I want JL corpus to be in the finalist datasets
too."; **Expresso** the same day, after the owner asked (verbatim): "Humm, why
did we not pick Expresso? The range of emotions seems good, and maybe it's
possible to download the whole dataset, as it may not be that large." — and,
once the agent had rechecked it: "yes, add Expresso as the fourth
finalist."

### §6.1 EARS

- **Licence:** CC BY-NC 4.0 — credit, non-commercial.
- **Size, measured** (GitHub's listing of the release files, 2026-09-28): the
  whole dataset **69.2 GB** in 107 zips, one per speaker, **564-804 MB** each
  (median 643 MB). The README's loop fetches them all:
  `curl -L https://github.com/facebookresearch/ears_dataset/releases/download/dataset/p${X}.zip`.
- **A few clips, without the zips:** the file server accepts byte ranges
  (checked 2026-09-28: `accept-ranges: bytes`; `p001.zip` is 592,079,092
  bytes). A zip keeps its table of contents at the end, so a short Python
  script, standard library only (`urllib` and `zipfile` over a file object
  that fetches byte ranges on demand), can read one speaker's table of
  contents — a few kilobytes — and fetch only the files named, in the original
  lossless audio. **Estimated** (not measured): 2-3 MB per clip (10-15 s at
  48 kHz, 32-bit); four characters with a neutral clip and two moods each,
  about 12 clips, **roughly 30 MB**.
- **Listening before downloading:** the Hugging Face mirror
  ([philgzl/ears](https://huggingface.co/datasets/philgzl/ears)) plays clips
  in its dataset viewer, in the browser. Its audio is lossy Opus in Parquet
  shards of about 40 MB that are not grouped by speaker — fine for choosing
  voices, not for cloning. The speakers' metadata is in
  `speaker_statistics.json` in the official repository.
- **Transcripts:** `transcripts.json` covers the read portions, so `ref.txt`
  comes straight from it.

### §6.2 CREMA-D

- **Licence:** ODbL for the database, DbCL for the clips — commercial use
  allowed, with an attribution notice; the ODbL's share-alike applies to
  copies of the database, not to a show that uses a few clips.
- **Size, estimated:** about **0.62 GB** of WAV in 7,442 clips — the real
  sizes of 41 clips spread across the set (mean 82,920 bytes, about 2.6 s at
  16 kHz, 16-bit, mono), times the count. One actor's full set, about 82
  clips, is about **7 MB**.
- **A few clips:** each clip is its own file in Git LFS, fetchable by URL
  (range requests accepted; one clip checked at 72,862 bytes):
  `curl -L -O https://media.githubusercontent.com/media/CheyneyComputerScience/CREMA-D/master/AudioWAV/1001_DFA_ANG_XX.wav`.
  Do not `git clone` the repository: it also holds the videos, which Git LFS
  would pull.
- **File names:** `<actor>_<sentence>_<emotion>_<intensity>.wav` — emotions
  `ANG`, `DIS`, `FEA`, `HAP`, `NEU`, `SAD`; intensities `LO`, `MD`, `HI`, `XX`
  (unspecified); the sentence code maps to one of 12 fixed sentences (for
  example "I'm on my way to the meeting", `IOM`; "The surface is slick",
  `TSI`), so each clip's transcript is known exactly.
- **What it has that the others lack:** crowd ratings for every clip —
  `processedResults/summaryTable.csv` gives each clip's `VoiceVote`, the
  emotion most raters heard from the voice alone, with its level; so the clips
  where listeners heard fear as fear can be chosen. And
  `VideoDemographics.csv` gives each actor's age and sex, to shortlist voices.

### §6.3 JL-Corpus

- **Licence:** **CC0: Public Domain** — as the authors' own Kaggle upload
  states (its public metadata, checked 2026-09-29: owner `tli725`, the
  authors' account) and as their Interspeech 2018 paper says. The GitHub
  repository has no licence file. The authors ask for a citation: Jesin James,
  Li Tian, Catherine Watson, "An Open Source Emotional Speech Corpus for Human
  Robot Interaction Applications", in Proc. Interspeech, 2018.
- **Where the audio is:** on Kaggle only; the GitHub repository holds the
  documents and the picture prompts. What is published is the **raw corpus,
  "unchecked and unannotated"** — the README says the perceptually verified,
  annotated version "will be given public access soon" (written in 2018).
- **Size, from Kaggle's file listing** (2026-09-29): the dataset **948 MB**
  as Kaggle reports it; the audio **2,400 clips, 448 MB**, each with a `.txt`
  transcript, in `Raw JL corpus (unchecked and unannotated)/JL(wav+txt)/` (the
  upload also holds a partial lowercase copy of that folder, and the
  perception test's material).
- **Structure:** four speakers — `female1`, `female2`, `male1`, `male2` —
  each recording all ten emotions, **60 clips per speaker and emotion**, named
  `<speaker>_<emotion>_<sentence><a|b>_<take>.wav` (for example
  `male1_anxious_10a_1.wav`). **Estimated** clip length: about 2.1 s on
  average (the mean file size, 186,852 bytes, at the paper's 44.1 kHz and
  16 bits, assuming mono).
- **How to fetch:** a Kaggle account is needed — the whole dataset from the
  website, or single files with Kaggle's command-line tool:
  `kaggle datasets download -d tli725/jl-corpus -f "<path>"`. The tool reads
  the owner's Kaggle API key, which the agent never handles: the owner runs
  the downloads, or sets the key up so the tool finds it.

### §6.4 Expresso

- **Licence:** CC BY-NC 4.0 — credit, non-commercial. Cite: Nguyen, Hsu,
  D'Avirro, Shi et al., "EXPRESSO: A Benchmark and Analysis of Discrete
  Expressive Speech Resynthesis", Interspeech 2023.
- **Voices and quality:** four actors, two men and two women — as many as the
  cast, with no choice among voices; a professional studio with minimal
  background noise, 48 kHz, 24-bit.
- **Two halves, recorded differently** (the README's table of styles):
  - **read speech**, 11.5 h, mono, **with transcripts**
    (`read_transcriptions.txt`): confused, default, enunciated, happy,
    laughing, narration, sad, whisper;
  - **improvised dialogues**, 34.4 h, two actors talking, **stereo with one
    channel per actor, no transcripts**, in
    `conversational/{speaker pair}/{styles}/`: 26 styles, among them
    **angry (82 min)** and **fearful (98 min)**, calm, awe, bored, sleepy,
    sympathetic, sarcastic, disgusted, projected (speech raised to carry).
- **What that means for the show:** the moods it needs most — afraid,
  terrified, angry — exist only in the dialogues. Each such reference means
  taking the actor's own channel, cutting a clean stretch of about 10 s of
  that actor alone (listening for the other actor bleeding into the
  microphone), and having Whisper draft the transcript, checked by hand. More
  preparation per clip than the other finalists; in exchange, long, natural,
  continuous takes, which may clone better than joined 2-second sentences.
- **Size, measured** (2026-09-29): the whole dataset is one tar,
  `expresso.tar`, **38,441,031,680 bytes (38.4 GB)** — the README's "36GB"
  is the same figure counted in GiB; about 13 minutes at 50 MB/s, over an hour
  at 10 MB/s. The server accepts byte ranges, but a tar has no table of
  contents at its end: fetching one file means stepping through the archive's
  headers, one small request per file — doable, slower than EARS's zips, not
  tried. A Hugging Face copy, `ylacombe/expresso` (CC BY-NC 4.0), holds **the
  read speech only**: **5.76 GB** in 12 Parquet files — without angry or
  fearful.
- **Listening first:** the [demo page](https://speechbot.github.io/expresso/)
  plays samples of the styles, with nothing downloaded.

### §6.5 The finalists side by side

| | EARS | CREMA-D | JL-Corpus | Expresso |
|---|---|---|---|---|
| Licence | CC BY-NC 4.0 | ODbL / DbCL | CC0 | CC BY-NC 4.0 |
| Voices | 107, ages 18-75 | 91, ages 20-74 | 4 (2 women, 2 men) | 4 (2 women, 2 men) |
| Accent | English; speakers' first languages in the metadata | English (accents not checked) | New Zealand English | English (accents not checked) |
| Emotions | 22 + neutral | 6 | 10 | 8 read, 26 improvised |
| Audio | 48 kHz, 32-bit, anechoic | **16 kHz** | 44.1 kHz, 16-bit | 48 kHz, 24-bit, studio |
| One take | three sentences in one file, ~10-15 s (estimate) | one sentence, ~2.6 s | one sentence, ~2.1 s (estimate) | read: sentences; dialogue: long, one channel per actor |
| Transcripts | `transcripts.json` (read parts) | the 12 sentences, by code | a `.txt` per clip | read speech only |
| Quality signal | anechoic studio | crowd ratings per clip (`VoiceVote`) | a perception test (published results for the verified version only) | professional studio |
| Getting four voices | ~30 MB by range requests (estimate) | a few MB by URL | a few MB, through Kaggle with the owner's account | the whole 38.4 GB tar, or single files by stepping through it (not tried) |

**A first mapping to the show's moods** (the agent's draft, 2026-09-29; to be
judged by ear):

| Show mood | EARS | CREMA-D | JL-Corpus | Expresso |
|---|---|---|---|---|
| calm | neutral, serenity | NEU | neutral | calm, default |
| happy | amusement, contentment | HAP | happy | happy |
| excited | ecstasy, amazement | HAP (HI) | excited | laughing? |
| hopeful | — (interest?) | — | encouraging | sympathetic? |
| relieved | relief | — | — | — |
| doubtful | confusion | — | concerned | confused |
| curious | interest | — | — | awe? |
| urgent | — | — | assertive? | projected? |
| determined | pride? | — | assertive | — |
| sad | sadness, disappointment | SAD | sad | sad |
| afraid | fear | FEA | anxious | fearful |
| terrified | fear, distress | FEA (HI) | — | fearful |
| angry | anger | ANG | angry | angry |
| exhausted | pain? | — | — | sleepy, bored |

The mood-to-clip mapping with fallbacks is the follow-up "Mood clips"; a mood
without a clip falls back to a near one, then to `ref.wav`.

## §7. The same test for every finalist — the short-take problem

CREMA-D's and JL-Corpus's takes are single sentences of 2-3 seconds; the
engine wants about 10. The way through: join 3-4 sentences from the same
speaker in the same emotion, and join their transcripts in the same order.
The risk: separate takes joined may sound choppy or uneven, where an EARS
file is one continuous take. Expresso's dialogues have the opposite problem:
long continuous takes, but one actor must be cut out of a conversation, and
transcribed (§6.4). Whether a joined reference clones well is a
question for the ear (§9).

## §8. Open questions

1. **The sample rate.** The voice engine produces 24 kHz; a 16 kHz reference
   (CREMA-D) may carry its narrower, telephone-like sound into the cloned
   voice — believed, not tested. On a shortwave radio show that might even
   suit the fiction.
2. **The accent.** JL-Corpus's voices are New Zealand English; whether that
   matters for four scientists in an unnamed lab is the owner's call.
3. **Joined takes** (§7).
4. **Cutting one actor out of Expresso's dialogues** — whether the other
   actor bleeds into each channel, and whether a clean 10-second stretch of
   one actor alone is easy to find (§6.4).
5. **How much emotion carries into the cloned voice** with Faster Qwen3-TTS —
   unmeasured (the follow-up "Mood clips", its risks).
6. **Loudness:** clips from different recordings may differ in level;
   normalize when preparing them.

## §9. The proposed next step — a listening test

Proposed by the agent on 2026-09-28, before JL-Corpus and Expresso joined
the finalists; awaiting the owner's go. For one character, build one reference
from each finalist; have the voice engine speak the same show line with each; the owner
listens to them side by side. Downloads first listed with each file, its size
and its licence, for the owner's approval; JL-Corpus's files fetched by the
owner through Kaggle. The cost: a few megabytes and a few minutes on the box.
Before it, the owner can shortlist voices: EARS in the Hugging Face viewer,
CREMA-D from its demographics and ratings, JL-Corpus by listening to the four
speakers, Expresso on its demo page.

## §10. Sources

- EARS: [repository](https://github.com/facebookresearch/ears_dataset) ·
  [licence file](https://raw.githubusercontent.com/facebookresearch/ears_dataset/main/LICENSE) ·
  [release files](https://github.com/facebookresearch/ears_dataset/releases/tag/dataset) ·
  [project page](https://sp-uhh.github.io/ears_dataset/) ·
  [paper (arXiv)](https://arxiv.org/html/2406.06185v2) ·
  [paper (Interspeech 2024)](https://www.isca-archive.org/interspeech_2024/richter24_interspeech.pdf) ·
  [Hugging Face mirror](https://huggingface.co/datasets/philgzl/ears)
- CREMA-D: [repository](https://github.com/CheyneyComputerScience/CREMA-D) ·
  [Hugging Face copy (16 kHz)](https://huggingface.co/datasets/myleslinder/crema-d)
- JL-Corpus: [repository](https://github.com/tli725/JL-Corpus) ·
  [Kaggle](https://www.kaggle.com/datasets/tli725/jl-corpus) ·
  [paper, Interspeech 2018](https://www.isca-archive.org/interspeech_2018/james18_interspeech.pdf)
- EMNS: [OpenSLR](https://www.openslr.org/136/) · [paper](https://arxiv.org/abs/2305.13137)
- Expresso: [project page and demo samples](https://speechbot.github.io/expresso/) ·
  [dataset README](https://github.com/facebookresearch/textlesslib/tree/main/examples/expresso/dataset) ·
  [download (38.4 GB)](https://dl.fbaipublicfiles.com/textless_nlp/expresso/data/expresso.tar) ·
  [Hugging Face copy, read speech only](https://huggingface.co/datasets/ylacombe/expresso) ·
  [paper](https://arxiv.org/abs/2308.05725)
- RAVDESS: [Zenodo](https://zenodo.org/records/1188976)
- TESS: [Borealis](https://borealisdata.ca/dataset.xhtml?persistentId=doi%3A10.5683%2FSP2%2FE8H2MF)
- ESD: [official repository](https://github.com/HLTSingapore/Emotional-Speech-Data) ·
  [the Kaggle mirror that mislabels it](https://www.kaggle.com/datasets/nguyenthanhlim/emotional-speech-dataset-esd)
- EmoV-DB: [repository](https://github.com/numediart/EmoV-DB) ·
  [licence](https://raw.githubusercontent.com/numediart/EmoV-DB/master/LICENSE.md) ·
  [OpenSLR](https://openslr.org/115/)
- MEAD: [README](https://github.com/uniBruce/Mead/blob/master/README.md) ·
  [project page](https://wywu.github.io/projects/MEAD/MEAD.html)
- eNTERFACE'05: [paper](https://www.researchgate.net/publication/4238264_The_eNTERFACE05_Audio-Visual_Emotion_Database)
- A licence table across corpora: [CAMEO: Collection of Multilingual Emotional
  Speech Corpora](https://arxiv.org/html/2505.11051v1)

## §11. Addenda

*Dated findings from trying the real audio files land here, newest last.*

### §11.1 2026-09-29 — EARS: single files fetched out of the zips, without downloading them (experiment PASS)

**Why.** The owner, shortlisting voices in the Hugging Face viewer, found it
too slow; it paged through many voices the owner did not like; it could not
line up the same file type across speakers; and it played lossy Ogg copies
(verbatim: "I think it is time for an experiment: Let's create a new
experiment folder in zombie-radio and write some python (or bash, whatever
fits best) to see if we can actually fetch" — the speakers' metadata, the
files' types, and a single file without the whole dataset).

**The experiment:** `docs/experiments/2026-09-29-ears-remote-fetch/` — the
script `fetch_ears.py` (Python 3, standard library only), the recipe and
the runlog in its `README.md`, the criteria, predictions and verdict in its
`findings.md`, the raw outputs in `raw/`.

**The verdict: PASS** — the owner (verbatim): "This is a PASS indeed. Good
job!" What it established:

- **The speakers** — `speaker_statistics.json` in the EARS repository gives
  each of the 107 speakers a gender (60 female, 43 male, 1 non-binary, 3
  "prefer not to answer" — the owner: "we will not use them. We just need 4
  that we like."), an age bracket (18-25 … 66-75), a native language (mostly
  American English: 58 women and 37 men), an ethnicity, a height and a
  weight.
- **The files** — each speaker's zip holds 161 WAV files, named by type,
  stored uncompressed. The emotional ones are `emo_<emotion>_sentences` (the
  same three sentences for every speaker, read in that emotion) and
  `emo_<emotion>_freeform` (an image described in that emotion, unscripted),
  for 22 emotions plus neutral. **Two names are spelled unlike the paper:**
  `embarassment` and `extasy`. The rest: six long unscripted talks
  (`freeform_speech_01`…`06`, about 35 MB each), interjections, nonverbal
  sounds (crying, screaming, yelling, laughter), the "rainbow" passage and
  24 sentence files in seven reading styles (fast, highpitch, loud,
  lowpitch, regular, slow, whisper), vegetative sounds, a song.
- **A single file, fetched** — for `p001`, `emo_neutral_sentences` (9.3 s)
  and `emo_fear_sentences` (11.4 s) arrived byte for byte as published (the
  zip's CRC-32 checked), **48 kHz, 32-bit float, mono**, each at its own size
  plus 0.03-0.05 MB; reading a 592 MB zip's table of contents costs about 5
  requests and 40 KB. An `emo_*_sentences` file is 1.3-2.9 MB, about 7-15 s
  — one continuous take, the length the voice engine wants (§2).

**How it works.** The EARS files are GitHub release assets, one zip per
speaker; their server answers HTTP range requests (a request for bytes
*a*-*b* of a file returns only those bytes). A zip keeps its table of
contents at its end, so the script opens each remote zip as a file whose
reads become range requests, lets Python's `zipfile` read the table of
contents, and copies out only the files asked for.

**How to use the script** — from the experiment folder:

```bash
cd docs/experiments/2026-09-29-ears-remote-fetch
```

1. **Who the speakers are** — every speaker with gender, age bracket, native
   language and ethnicity, and the counts:

   ```bash
   python3 fetch_ears.py --speakers-info
   ```

   Filters narrow any command: `--gender female` or `--gender male`;
   `--age 36-45` (a bracket exactly as in the metadata); `--native english`
   (any part of the native language, e.g. `"american english"`);
   `--speakers 1,4,10-15` (speaker numbers or ranges; without it, every
   speaker that passes the filters).

2. **What files a speaker has** — every file of one speaker, with its size
   and the emotion read from its name:

   ```bash
   python3 fetch_ears.py --list --speakers 1
   ```

   With several speakers (`--speakers 1-5`), it compares their sets of files
   instead and names any file missing for some of them.

3. **What a fetch would bring** — a dry run: each file and its size, and the
   total, nothing downloaded:

   ```bash
   python3 fetch_ears.py --gender female --native "american english" --types emo_neutral_sentences,emo_fear_sentences
   ```

   `--types` takes file names without `.wav`, comma-separated, exactly as
   `--list` prints them.

4. **The fetch** — the same command with `--fetch`:

   ```bash
   python3 fetch_ears.py --types emo_neutral_sentences,emo_fear_sentences --speakers 1 --fetch
   ```

   Files land in `datasets/ears/<speaker>/<type>.wav`, with the transcript
   beside each in `<type>.txt` when the type has one (the `sentences` files
   do; the `freeform` ones do not). Each file is reported with its size, "CRC
   ok", the bytes transferred, and its format and length.

5. **Listen and compare** — every fetch rewrites
   `datasets/ears/index.html`: every file fetched so far, one row per speaker
   (with the speaker's metadata), one column per type. Open it in Chrome,
   which plays 32-bit float WAV.

Every run ends with its number of requests and bytes transferred. A dry run
reads only tables of contents — under 1 MB even across 58 speakers.

**Where the audio goes, and why it stays there.** `datasets/` inside the
experiment folder, which the folder's own `.gitignore` excludes: EARS is CC
BY-NC 4.0 and this repository is public, and voice clips never enter it
(the follow-up "Voice-sample hygiene"). `--out <folder>` puts them anywhere
else. The reference clips the show uses are later converted to mono 24 kHz
16-bit and copied to `~/TalkWithZombies-client/Personas/<Name>/` (§2).

**Next.** The owner's shortlist: the two emotions above, neutral and fear,
for the native American English speakers — dry runs measured 250.09 MB for
the 58 women and 154.64 MB for the 37 men (run 4); the fetch waits for the
owner's word on those exact sizes.
