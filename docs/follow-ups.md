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

## SSH keepalives and polling for long silent deploy tasks — low priority (owner, 2026-09-23)

- **Status 2026-09-23 — explained, not a significant worry (owner):**
  the owner works on public library Wi-Fi and closes the laptop's lid
  during breaks, probably without closing the tunnel first — which
  accounts for the drops below better than an idle cutoff. The
  pre-PR reminder is withdrawn. One note kept for demo day (owner
  action queue item 4, logistics radar): a live show over a venue's
  Wi-Fi is where a dropped tunnel would stop the show, so a tunnel
  that reconnects by itself (`ServerAliveInterval` keepalives, or
  `autossh`) is cheap insurance to weigh then. The original entry
  follows unchanged.

- **The gap:** on 2026-09-22 a deploy's SSH session dropped after
  about 14 minutes of silence ("Data could not be sent to remote
  host … UNREACHABLE") while the base role's apt task waited for the
  package lock held by Ubuntu's first-boot unattended-upgrades run
  (43 minutes, 259 packages). The cause is NOT proven. The leading
  candidate is an idle-connection cutoff somewhere between the
  laptop and the box: during the wait the session carries no
  traffic, and none of our SSH settings send keepalives —
  `deploy/ansible/inventories/common_vars.yml` `ansible_ssh_common_args`
  sets only `IdentitiesOnly`, `StrictHostKeyChecking`,
  `UserKnownHostsFile`; `deploy/ansible/ansible.cfg` sets only
  `pipelining`; the Makefile's `ssh-tunnel` options (`SSH_TOFU_OPTS`)
  carry no keepalive either, so a quiet tunnel may drop the same way.
  Ruled out on the box: a reboot, an sshd restart at that moment, a
  Docker restart.
  Second datum, same evening: the owner's own tunnel was found dead
  at 19:05 CDT after about 70 idle minutes, the box and its services
  healthy (`docs/experiments/2026-09-22-emotion-grammar-cost/README.md`,
  runlog entry 1).
- **Where flagged:** `docs/experiments/2026-09-22-adr-0003-gate/README.md`,
  runlog entries 3–8. The interim fix of that evening: the apt lock
  wait became `zr_apt_lock_timeout` (300 s) with a clear error
  message when it expires (base role, block/rescue).
- **Trigger:** owner request 2026-09-22 — the agent RAISES this
  discussion right after the ADR-0003 gate evening closes (before
  that branch's PR), even if the owner does not ask.
- **Fix shape (candidates for the discussion, none decided):**
  (1) `-o ServerAliveInterval=30 -o ServerAliveCountMax=4` in
  `ansible_ssh_common_args` and in the tunnel's options — keeps any
  long task's session talking; (2) a base-role task that waits for
  the first-boot updater with short, repeated checks
  (`systemctl is-active apt-daily-upgrade.service` until it is no
  longer `activating`, e.g. every 20 s for up to ~45 min), so no
  single SSH command stays silent for long, and the operator sees a
  retry counter instead of silence; (3) whether the base role should
  switch the updater off on these disposable boxes (a
  security-policy call); (4) whether to act on the
  `/var/run/reboot-required` flag the updater leaves behind (seen
  2026-09-22; the playbook never reboots).

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

## llama.cpp unknowns the ADR-0003 gate left open

- **The gap:** four things measured or believed on 2026-09-22 that
  we cannot yet explain, all on llama.cpp build `b11096` with the
  hybrid Nemotron Nano 9B v2 (Mamba-2 plus attention layers):
  (1) **a fixed prompt cost of about 350 ms per request**, whether
  it evaluates 130 or 270 tokens — slow for an A6000, and the
  reason one request per round beats one per line; (2) **the host-RAM
  prompt cache's entries are large** — 417 MiB to 1.8 GB for prompts
  of a few hundred to ~1,600 tokens; (3) **what a history edit costs
  on this hybrid model**: trimming the script breaks the cached
  prefix from the edit point on, and with recurrent-state
  checkpoints at least 8,192 tokens apart by default the server may
  re-evaluate from much further back — unmeasured; (4) **the
  believed reason a grammar is nearly free when the model agrees and
  ~10 % dearer when it must overrule it**: the sampler checks the
  chosen token first and applies the grammar to the whole
  vocabulary only on rejection — from memory, not read in the
  source.
- **Where flagged:** [discussion 2026-09-22]
  grammar-and-prompt-cache-lessons §3 and §4.3/§4.8;
  `docs/experiments/2026-09-22-adr-0003-gate/` (runlog entries
  12–14).
- **Trigger:** (3) during Task 6b, once the midpoint trim exists —
  its pause measured with a low `show.context_budget` (reframed
  2026-09-23: the owner ruled for the trim, so the design no longer
  waits on it — [discussion 2026-09-23] show-engine-design §2); (1)
  and (2) when show
  latency is tuned, or the Task 5a audition swaps the model; (4)
  whenever a grammar change is weighed on cost.
- **Fix shape:** a small probe reusing the gate's scripts, one
  server flag changed at a time through the playbook
  (`--ctx-checkpoints 0`, a smaller `--checkpoint-min-step`,
  `--cache-ram 0`), plus one history-trim arm; for (4), read the
  sampler in llama.cpp's `common/sampling.cpp` at the build we
  serve.
- **When an item resolves:** write the answer back as a dated note
  in [discussion 2026-09-22] grammar-and-prompt-cache-lessons §4.10
  (the lasting home of these questions), then delete the item here.

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
- **Lesson from the ADR-0003 gate (2026-09-22) that shapes the
  test:** the cast sheet must TEACH the note line — say that one
  `# note:` line may come first and is never spoken. A grammar rule
  the prompt does not describe is a forced grammar: about 10 % more
  per token and a changed writing style in the emotion-field run
  ([discussion 2026-09-22] grammar-and-prompt-cache-lessons §4.2–§4.4).
  Test the scratchpad taught, or the arm measures the fight, not
  the idea.

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

## Upstream contributions to scorbo2 — deferred past the deadline

- **The statement:** two things we built may be worth offering to
  the author of TalkWithMe and tts-serve, in this order ([ADR-0002]
  contribution ledger): (1) **the deployment machinery** — `site.yml`
  standing up the model services on a rented GPU box in one command,
  and the standalone Mac client installer (`make client-mac`) —
  the part scorbo2 may want to adopt or advertise; (2) **the
  max-chars sentence accumulator** in `static/tts.js` (whole
  sentences packed up to about 100 characters instead of one TTS
  request per sentence — fixes "Dr. Byrne" becoming four requests,
  the short-sentence pauses, and the echo on a lone "1."), once
  proven in TalkWithZombies. Two **bug reports** joined the list on
  2026-09-23: (3) **thinking models break the router and some
  personas silently** — the "LLM decides" router asks for a name
  with `max_tokens=16` and no `/no_think`
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/routers/chat.py:117`),
  so Nemotron spends the budget thinking, the name comes back empty
  and the code falls back to `random.choice`; a persona prompt
  without `/no_think` can spend the whole `max_tokens` thinking, and
  since llama.cpp returns the thinking in `reasoning_content` while
  the app reads only `content`, the reply is an empty bubble (seen
  live 2026-09-23 with the stock Alex and Luna: 200 of 200 tokens,
  `content: ''`); (4) **the STT upload name for `audio/webm`** —
  `mimetypes.guess_extension` answers `.weba` on newer Pythons, so
  recordings go out as `audio.weba`; OpenAI's transcription API
  checks the extension and lists `webm` but not `weba` (our Whisper
  ignores the name — tested live); two upstream tests fail on those
  Pythons; our fix is TalkWithZombies commit `c46c3bf`.
  **No longer candidates:** the `[Name]:`
  output sanitizer (moot under [ADR-0003] — [spec §9]) and the
  `max_turns_for_context` raise (done in our config, 6 → 50, on
  2026-09-18 — a setting, not a patch).
- **Where flagged:** the remote-split spike (2026-09-16) designated
  the first patches; re-ranked 2026-09-21 ([discussion 2026-09-19]
  upstream-contribution-strategy, addendum; [discussion 2026-09-21]
  task6-reconnaissance-brief §1–§2; [ADR-0002]).
- **Trigger:** after 2026-10-08 — outreach deferred past the
  deadline by the owner ("build offerable, contact nobody yet").
- **Fix shape:** (1) as a pull request or a README pointer to the
  deployment repo; (2) a focused pull request against upstream's
  `static/tts.js`, with the packing rules' Node test (entry above)
  as its proof; (3) and (4) as GitHub issues with the receipts
  above, (4) with our commit as the proposed fix.

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
  Austin Python Meetup talk's motivation section, and (b) a possible
  standalone write-up/README section aimed at the community.
- **Fix shape:** a short "why cloud deployment matters for
  self-hosters" narrative — the agent helps draft it from this
  entry + the deployment-first discussion + real playbook usage
  numbers (deploy time, cost per session — we already have
  $2.97/experiment as a datum, and a from-zero deploy of the whole
  model stack in 7 minutes on an A6000, measured 2026-09-22).
