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

## Bump the tts-serve pin from 1.1 to 1.2 at the next box deployment

- **The gap:** `deploy/ansible/inventories/common_vars.yml` pins
  `zr_tts_serve_version: "1.1"`. Upstream's latest tag is `1.2`
  (2026-09-18; adds only the Apple-Silicon Qwen3-TTS MLX engine —
  the shared package and our engine's server are byte-identical
  between the two tags, verified by `git diff --stat 1.1 1.2` on
  2026-09-21).
- **Where flagged:** owner ruling 2026-09-21 during the Task 6
  reconnaissance brief ([discussion 2026-09-21] tts-serve tour §1):
  the pin is not set in stone — we track the latest tag unless a
  release breaks the deployment or the TalkWithMe contract. Not
  changed on the recon branch on purpose: a pin bump is a
  deployment change and must be proven on a box.
- **Trigger:** the next `make ans-deploy` against a fresh box
  (first experiment evening, Task 5c or 5a).
- **Fix shape:** edit the one line to `"1.2"`; deploy from zero;
  re-run must be `changed=0`; `make check` three-ok; one TalkWithMe
  synthesis through the tunnel. Then delete this entry and bank
  the version in the arc-plan journal.

## Measure TTS synthesis time against text length (tunes the accumulator's N and the director's line budget)

- **The gap:** the accumulator sends chunks of up to N characters;
  while chunk 1 plays, chunk 2 is being synthesized, and the
  listener hears no gap only if making the next chunk takes less
  time than playing the current one. We do not know (a) the fixed
  cost per synthesis request — the pause paid in full by every
  tiny fragment like "Dr." — nor (b) how the wait grows with longer
  text. Ten requests to tts-serve with texts of 20, 50, 100, 200,
  400 characters, recording the `time_used` and audio-duration
  fields every response already carries, give both numbers in one
  table, and the largest N whose next-chunk wait hides behind the
  current chunk's playback. The same table tells the director how
  far ahead to request the next round.
- **Where flagged:** the Task 6 reconnaissance brief (seam question
  S3, tts-serve tour F2/F4, question Q4); **dropped from the MVP
  arc by the owner on 2026-09-22** — "we have already committed to
  this path forward; this measurement will be useful later, after
  we have something working we can tweak; I can always change the
  TTS server."
- **Trigger:** the show loop runs end to end in the fork and the
  owner wants to tune pauses or prosody; or a TTS engine change
  (Task 5b) invalidates the provisional value.
- **Fix shape:** half an hour on a box with `tools/speak.py` or
  curl; then adjust `tts.accumulator_max_chars` (name indicative;
  provisional 100, tolerance ~20 %) and the director's line budget.

## Mac-local TTS probe with tts-serve's MLX engine (parked post-MVP)

- **The gap:** tts-serve ships a native Apple-Silicon engine
  (Qwen3-TTS via MLX, tag 1.2) and five engines accept PyTorch's
  `mps` device; llama.cpp runs on Metal; Whisper runs anywhere — so
  a Mac with enough unified memory could run the whole stack
  locally: a second emergency mode for demo day and a free
  rehearsal setup. **The demo laptop (M1, 16 GB) cannot run it**;
  the owner's second M1 with 64 GB could, if the speed is
  acceptable.
- **Where flagged:** tts-serve tour §8 Q5 (2026-09-21); parked by
  the owner 2026-09-22 ("until after the MVP").
- **Trigger:** after 2026-10-08, or if the cloud box becomes
  unavailable for the demo.
- **Fix shape:** one evening on the 64 GB machine — a venv,
  `impl/server_qwen3TTS_mlx.py`, point TalkWithZombies' TTS URL at
  it, read `rtf` from a few sentences; llama.cpp on Metal next.

## JavaScript test for the accumulator's packing rules

- **The gap:** upstream has Node test harnesses for the persona
  form and the TTS settings section but none for `static/tts.js`;
  the fork changes the accumulator (N = 100, ~20 % tail tolerance,
  hard flush at line end) and adds `show.js` untested.
- **Where flagged:** TalkWithMe tour §6 / Q11; ruled 2026-09-22: no
  new harness inside the three-day timebox.
- **Trigger:** the packing rules stop moving (after the timebox and
  the first rehearsal tuning).
- **Fix shape:** a third Node test in upstream's `vm.Context`
  pattern (`tests/test_tts_settings.js` as the template) covering
  the three packing rules and the line-end flush.

## Bounded scratchpad before the script — test the "room to reason" hypothesis

- **The gap:** the adopted prompt structure ([discussion
  2026-09-21] prompt-structure §7.5) makes it possible to let the
  model write ONE non-spoken line before the script (`# note: …`),
  capped by the GBNF grammar with `{0,N}`, which the stream parser
  drops instead of speaking — a bounded scratchpad. The hypothesis
  (from the dottxt "Say What You Mean" finding that room to reason
  before a constrained field helped on reasoning benchmarks; the
  taxonomy's A3 says we amputated planning with `/no_think` for
  speed): a few planning tokens per round improve storytelling
  coherence at a latency cost small enough not to hear. UNPROVEN
  for dialogue by anyone; it may equally be disproved.
- **Where flagged:** owner, 2026-09-21, after the prompt-structure
  discussion ("this paragraph can lead to an experiment task later
  to try to disprove the hypothesis, or accept it… I fear we have
  no time"). Registered here for visibility, not scheduled.
- **Trigger:** the fork runs the shared-context structure with the
  grammar, AND a Task 5a session is already open on a box (the
  experiment is one extra cell in the audition, not a session of
  its own).
- **How to measure — the coherence problem, addressed with what the
  taxonomy already has** ([discussion 2026-09-16] §5–§6): coherence
  resists counting, but it has proxies — stale-question answers per
  round, fact drift across speakers, fraction of turns that add
  information — and the lab3 two-round protocol (report the zombie
  count; then write a five-sentence report) is the fixed probe that
  produced the founding specimen. Protocol-lite: same model, same
  seed, grammar ON; scratchpad PRESENT vs ABSENT; run the two-round
  protocol three times per arm; count the three proxies by ear;
  read time-to-first-line off the stream. Adopt only if the
  coherence gain is audible and the latency cost is not; otherwise
  record the null result and delete this entry.
- **Fix shape if adopted:** one grammar rule and one parser branch
  in the fork; a yaml-only knob for the scratchpad's token cap.

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
  chunking in `static/tts.js` — fixes the naive splitter
  ("Dr. Byrne" → four requests), the short-sentence economics
  (effective RTF > 1; quantified in the spike's TTFA data), AND
  ultra-short-input audio artifacts (field-observed 2026-09-18:
  an echo on a lone "1." — also a §7.2 per-engine test item). A third config-only lever rides along: raise
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

## Voice-sample hygiene — famous-actor clips NEVER enter the repo

- **The gap/rule:** the owner will likely source the four
  reference voice samples from famous actors' movie audio (comedy
  value). RULING (owner, 2026-09-16): these files are curated and
  used locally but **never committed** to this public repo
  (rights + hygiene). Same logic extends to any derived cleaned
  clips.
- **Where flagged:** owner, 2026-09-16, while ruling on the
  action queue ([discussion 2026-09-16] prototype-first
  inversion).
- **Trigger:** the moment the first sample file exists.
- **Fix shape:** add a `.gitignore` block for the samples
  directory (e.g. `voices/` or `samples/` — name it when
  created); keep the curated set in a local/private location the
  Ansible deployment can copy from; document the expected
  directory layout in the prototype's setup notes so a cold
  rebuild knows what to supply.

## Find the voice-isolation tool from scorbo2's podcast

- **The gap:** extracting a clean voice from noisy movie audio
  (music, effects) needs a voice-isolation/separation tool. The
  author of TalkWithMe/tts-serve (scorbo2) mentioned on his
  podcast an open-source solution he uses for exactly this — the
  owner forgot the name and asked to be reminded to search for
  it.
- **Where flagged:** owner, 2026-09-16 (side note while ruling on
  voice samples).
- **Trigger:** BEFORE curating the voice samples (item above) —
  the tool is what makes movie-sourced clips usable as TTS
  references.
- **Fix shape:** re-listen to / search the podcast episode, or
  survey the obvious candidates (the open-source
  vocal-separation space: Demucs-family, UVR-family) and confirm
  against what he mentioned; record the pick and the one-line
  usage in the prototype's setup notes.

## Communicate the cloud-deployment story to the self-hosted AI community

- **The gap/idea (owner, 2026-09-17):** the deploy/ playbook is
  useful beyond this project — a middle ground for self-hosted AI
  enthusiasts: deploy TalkWithMe + tts-serve predictably on a
  rented cloud GPU to experiment BEFORE committing to a local
  install. This framing belongs in a future talk/write-up on the
  project's motivations, and the owner asked that the idea not be
  lost ("annotate somewhere we need to communicate at some point
  the significance of the cloud deployment automation").
- **Where flagged:** [discussion 2026-09-17] deployment-first
  brainstorm §5.
- **Trigger:** the project goes well — concretely: the MVP works
  and the deploy/ playbook is proven; then this feeds (a) the
  hackTNT presentation's motivation section, and (b) a possible
  standalone write-up/README section aimed at the community.
- **Fix shape:** a short "why cloud deployment matters for
  self-hosters" narrative — the agent helps draft it from this
  entry + the deployment-first discussion + real playbook usage
  numbers (deploy time, cost per session — we already have
  $2.97/experiment as a datum).
