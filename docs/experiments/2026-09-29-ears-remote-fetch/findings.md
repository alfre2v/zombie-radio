# EARS remote fetch — findings

*Interpretation only. The verdict criteria and the predictions below are
frozen before the first run: the freeze is the commit that carries them.*

## Verdict criteria

- **PASS** — all three: (a) the metadata gives every speaker's gender;
  (b) the zips' tables of contents list the files by type name, and the
  emotion can be read from the name of every emotional file; (c) for each
  speaker asked, a requested file arrives with its CRC-32 matching the zip's,
  a WAV header that reads, and no more than 1 MB transferred beyond the
  file's own size. **Consequence:** the script is how EARS voices are
  shortlisted (its `index.html`) and how the listening test's EARS clips are
  fetched ([discussion 2026-09-29] voice-datasets-with-emotion, §9).
- **PARTIAL** — (c) works but (a) or (b) falls short (for example, file
  types differ between speakers, or names do not say the emotion).
  **Consequence:** fetch by listing each speaker first; record what is
  missing.
- **FAIL** — (c) does not work: no range requests on the final URL, or the
  zips cannot be read this way. **Consequence:** the fallback of the abort
  criteria — whole per-speaker zips for a short list chosen by ear in the
  Hugging Face viewer.

## Predictions

**The agent's** (2026-09-29, before the first run):

1. (a) 107 speakers, every one with a gender; roughly half women.
2. (b) Every speaker has the same set of types; the emotional ones are
   `emo_<emotion>_sentences` and `emo_<emotion>_freeform` for 22 emotions
   plus neutral; the zips store the WAV files uncompressed.
3. (c) One `emo_*_sentences` file per speaker arrives with its CRC ok, at
   48 kHz, 32-bit float, mono, **10-15 s long** (the estimate in the
   discussion, §6.1), about 2-3 MB; each speaker costs a handful of requests
   and well under 1 MB beyond the files.

**The owner's:** *(the owner's slot — to fill before the first run, or left
empty)*

## Results

*Filled only from the README's runlog.*

- **(a) The speakers** (run 1): 107 speakers, each with a gender field — 60
  female, 43 male, 1 non-binary / third gender, 3 "prefer not to answer";
  ages as brackets; native languages mostly American English. Prediction 1
  held: every speaker has the field, and 60 of 107 are women; three withheld
  it — the owner: "Don't worry about the 3 persons with "prefer not to
  answer" in the gender, we will not use them. We just need 4 that we like."
- **(b) The types** (run 2, `p001`): 161 WAV files, named by type; the 46
  emotional ones are `emo_<emotion>_sentences` and `emo_<emotion>_freeform`
  for 22 emotions plus neutral, so the emotion reads from the name (two
  spelled unlike the paper: `embarassment`, `extasy`); stored uncompressed.
  Prediction 2 held for `p001`; "every speaker has the same set" is checked
  only for the two types fetched — both present in all 95 zips of run 4 —
  not for the other 159.
- **(c) The fetch** (run 3, `p001`): both files arrived with "CRC ok";
  48 kHz, 32-bit float (format 3), mono; `emo_neutral_sentences` 1.79 MB,
  9.3 s, 1.84 MB transferred; `emo_fear_sentences` 2.20 MB, 11.4 s, 2.23 MB
  transferred; the whole run 17 requests and 4.129 MB, transcripts included.
  Prediction 3 held for the format, the checksum and the cost; it missed
  narrowly on the neutral file, **9.3 s and 1.79 MB** against a predicted
  10-15 s and 2-3 MB.

## Verdict

**PASS** — the owner, 2026-09-29 (verbatim): "This is a PASS indeed. Good
job!" All three criteria met: (a) every speaker the cast would use has a
gender; (b) the types are named, the emotion in the name; (c) single files
arrive intact, lossless, at their own size plus 0.03-0.05 MB each.
**Consequence** (as frozen): the script is how EARS voices are shortlisted
(its `index.html`) and how the listening test's EARS clips are fetched
([discussion 2026-09-29] voice-datasets-with-emotion, §9 and its addendum
of 2026-09-29).
