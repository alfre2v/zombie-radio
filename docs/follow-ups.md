# Follow-ups

*Small items, known limitations, explicit deferrals. Scan this file
at every work pickup. Items resolve and get DELETED; deferrals stay
until their trigger fires. Cross-arc deferrals live HERE, never in
the arc-scoped TODO.md — an arc close would silently lose them. When
an item becomes a real arc it graduates to the roadmap and leaves
this file.*

Entry anatomy (every entry self-contained enough to rescue a cold
reader's memory):

- the gap/statement
- where it was flagged (file/commit/discussion)
- the **trigger** for acting
- the rough fix shape (commands if known)
- optionally a RULING (decided now, executed at the trigger) and a
  priority tag on the header when the owner ranks items

---

## Add new TTS engines to tts-serve (F5-TTS, Breeze TTS 2) — soft goal

- **The gap:** tts-serve wraps six engines (Chatterbox, OmniVoice,
  Qwen3-TTS, Faster Qwen3-TTS, dots.tts, Index-TTS) but not
  F5-TTS (the 2024 version's engine, owner has hands-on
  experience) or Breeze TTS 2 (3B real-time model, ~133 ms
  first-audio, 50 languages; code Apache-2.0, **weights
  non-commercial research only** — acceptable for this
  non-commercial project; verified 2026-09-13,
  <https://github.com/breezeblue-ai/breeze-tts>). Either would be
  a candidate upstream contribution (wrapper code can be MIT; the
  weights license rides separately).
- **Where flagged:** owner, 2026-09-13 conversation; TTS-goal
  agreement recorded in [discussion 2026-09-12] QA log Entry 5
  and brainstorm §3.
- **Trigger:** time allows after the MVP's TTS path works
  end-to-end with an existing engine — explicitly a SOFT goal;
  also triggered if the §8.4 engine comparison experiment finds
  the existing six inadequate for 4 distinct character voices.
- **Fix shape:** implement a tts-serve server module per engine
  following the existing `impl/server_*.md` pattern
  (<https://github.com/scorbo2/tts-serve/tree/master/impl>);
  expose via the standard `/synthesize` + `/capabilities` API;
  F5-TTS first (known quantity), Breeze TTS 2 second (newer,
  unproven locally). Consider upstreaming as PRs to scorbo2.
