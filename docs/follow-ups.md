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

- **The gap:** tts-serve wraps seven engines (Chatterbox,
  OmniVoice, Qwen3-TTS, Faster Qwen3-TTS, dots.tts, Index-TTS,
  and — since upstream v1.1, 2026-09-15 — LuxTTS; count updated
  2026-09-16) but not
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
  also triggered if the [spec §7.2] engine comparison experiment
  finds the existing seven inadequate for 4 distinct character
  voices. *(Pointer corrected 2026-09-16: was "§8.4", a stale
  pre-spec number.)*
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

## TalkWithMe upstream-contribution candidates — two designated patches

- **The gap:** the remote-split spike closed with zero forks and
  two small, fully-scoped patches designated but NOT built
  (deliberate scope guard): (1) a one-line output sanitizer
  stripping leading `[Name]:` labels before display/TTS — the
  firebreak for label mimicry, and the fork-vs-upstream decision
  point per the fork strategy ("defer until the first patch");
  (2) a max-chars sentence accumulator replacing per-sentence
  chunking in `static/tts.js` — fixes both the naive splitter
  ("Dr. Byrne" → four requests) and the short-sentence
  economics (effective RTF > 1; quantified in the spike's TTFA
  data). A third config-only lever rides along: raise
  `max_turns_for_context` from 6 (amnesia-by-design in a
  4-persona room — taxonomy C9).
- **Where flagged:** remote-split runlog + findings (2026-09-16);
  mechanisms C1/C9 and the economics receipts in
  [discussion 2026-09-16] (narrative health).
- **Trigger:** the adaptation arc opens (these are its first
  backlog items); the sanitizer fires EARLY if a show room gets
  label-contaminated and fresh-room hygiene stops sufficing.
- **Fix shape:** sanitizer = one line in the reply path (or
  client-side before TTS enqueue); accumulator = replace the
  sentence-split loop in `static/tts.js` with
  pack-up-to-N-chars; both are candidate PRs to scorbo2 once
  proven in our fork.

## LuxTTS landed upstream — presumptive §7.2 candidate

- **The gap/news:** tts-serve v1.1 (2026-09-15) added **LuxTTS**
  (<https://github.com/ysharma3501/LuxTTS>): ZipVoice distilled
  to 4 sampling steps, 48 kHz custom vocoder, **Apache-2.0 code
  AND weights**, claimed **~1 GB VRAM** and **150× realtime on
  GPU**. Cloning from ≥3 s reference, NO transcript needed (the
  tts-serve wrapper auto-transcribes the reference with Whisper).
  Why it matters here: ~1 GB vs Faster Qwen3-TTS's ~5 GB reshapes
  the two-engine VRAM budget (16 GB aspiration), and 150×
  realtime would collapse the engine-floor share of the
  short-sentence economics problem (the ~215 ms network toll per
  request remains). Caveats, verified 2026-09-16 from upstream +
  wrapper docs: English/Chinese ONLY (other scripts silently
  dropped; non-EN/ZH reference clips 500); ~10 s one-time librosa
  warmup on first request; two days old and unproven — all claims
  are the author's, unmeasured by us.
- **Where flagged:** owner heads-up 2026-09-16 (upstream PR
  merge); agent verified against
  <https://github.com/scorbo2/tts-serve> README/v1.1 and
  `impl/server_luxTTS.md`.
- **Trigger:** the §7.2 TTS comparison experiment scoping —
  LuxTTS enters the candidate pool automatically (it is now a
  wrapped engine) and its VRAM/RTF claims are exactly what §7.2
  measures. Its Apache-2.0 weights also weaken the case for the
  Breeze TTS 2 soft-goal addition (non-commercial weights, same
  lightweight niche) — re-evaluate that entry when this trigger
  fires.
- **Fix shape:** nothing to build — include in the §7.2 harness;
  verify the VRAM claim first (it's the cheapest check and the
  biggest prize).
