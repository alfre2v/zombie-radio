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

## MassedCompute 50% code verification — parked

- **The gap:** MassedCompute sits on the provider shortlist only
  as a *conditional wildcard* ([discussion 2026-09-13] provider
  survey S4): with the owner's 50% affiliate code verified, its
  A6000 48 GB at ~$0.275/hr would be the survey's best
  VRAM-per-dollar. Unverified: the code's GPU-type coverage,
  Docker-with-GPU under their vGPU setup, and open ports.
- **Where flagged:** provider survey S2/S4; parked by owner
  ruling 2026-09-13 ("do not want to waste time on it — not in
  our top 2").
- **Trigger:** occasional reminder to the owner **after each
  experiment PR merges** (owner-requested cadence); acts only if
  the owner then feels like burning an hour on it, or if both
  top-2 providers (Hyperstack, Scaleway) disappoint.
- **Fix shape:** one-hour smoke test on a $0.35/hr A30 — check
  code coverage at deploy, `docker run --gpus all`, and port
  reachability; if all pass, promote to dev-workhorse candidate.
