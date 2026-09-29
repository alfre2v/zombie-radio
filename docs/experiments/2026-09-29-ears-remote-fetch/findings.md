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

## Verdict
