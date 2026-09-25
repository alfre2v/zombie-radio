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

## SSH keepalives and polling for long silent deploy tasks — priority raised 2026-09-25 (was low, owner 2026-09-23)

- **Status 2026-09-25 — the tunnel drops while an interactive session
  survives (owner); priority raised:** the tunnel keeps breaking at
  certain times, while the owner's interactive SSH session to the box
  (running tmux) stays open most of the time. The lid-closing
  explanation below would kill both, so it no longer fits. The leading
  explanation — believed, not proven — is idle traffic: tmux redraws
  its status bar every 15 s by default, so the interactive session
  keeps talking, while the tunnel (`ssh -N`, the Makefile's
  `ssh-tunnel`, whose options carry no keepalive) is silent between
  rounds, and Wi-Fi routers and firewalls drop idle connections. Not
  checked: whether the owner's own ssh config gives the interactive
  session a keepalive (the owner's SSH directory is off limits to the
  agent). A drop now interrupts the work: the `/show` page stops with
  an error until Resume (slice 3). **Fix shape, the agent's picks:**
  (1) client side, in the Makefile's `ssh-tunnel`:
  `-o ServerAliveInterval=30 -o ServerAliveCountMax=3` — an idle
  tunnel keeps talking, and a dead link is detected within about 90 s,
  so ssh exits instead of lingering; (2) the tunnel restarts by itself:
  a small loop around the command (restart after an exit, a short
  pause) or `autossh` — with (1), a drop heals in seconds and the
  page's Resume picks up; (3) optional, later: `ClientAliveInterval`
  in the box's `sshd_config` through the playbook (belt and braces; it
  changes the box). Proof: count the drops over a day of use, before
  and after. **Fix (1) applied the same day, at the owner's request**
  ("this tunnel thing is too annoying already"): the Makefile's
  `ssh-tunnel` now passes `-o ServerAliveInterval=30
  -o ServerAliveCountMax=3`; a tunnel started before the change must be
  restarted to get it. (2) and (3) remain open.
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
  of a few hundred to ~1,600 tokens; (3), what a history edit costs
  on this hybrid model, was answered on 2026-09-24 (lessons §4.10
  question 3: a trim re-reads little but pays about 1.5 s of slot
  swapping once — see the next entry) and left this list; (4) **the
  believed reason a grammar is nearly free when the model agrees and
  ~10 % dearer when it must overrule it**: the sampler checks the
  chosen token first and applies the grammar to the whole
  vocabulary only on rejection — from memory, not read in the
  source.
- **Where flagged:** [discussion 2026-09-22]
  grammar-and-prompt-cache-lessons §3 and §4.3/§4.8;
  `docs/experiments/2026-09-22-adr-0003-gate/` (runlog entries
  12–14).
- **Trigger:** (1) and (2) when show latency is tuned, or the Task
  5a audition swaps the model; (4) whenever a grammar change is
  weighed on cost.
- **Fix shape:** a small probe reusing the gate's scripts, one
  server flag changed at a time through the playbook
  (`--ctx-checkpoints 0`, a smaller `--checkpoint-min-step`,
  `--cache-ram 0`); for (4), read the sampler in llama.cpp's
  `common/sampling.cpp` at the build we serve.
- **When an item resolves:** write the answer back as a dated note
  in [discussion 2026-09-22] grammar-and-prompt-cache-lessons §4.10
  (the lasting home of these questions), then delete the item here.

## Pauses the model server's timings do not show

- **The gap (measured 2026-09-24, two identical 28-round drives on
  the box, the fork's trim with `show.context_budget` 1500):** two
  kinds of pause, neither in the `timings` the show records.
  (1) **The slot swap.** When a request keeps only a small share of
  what the server's one slot holds — `f_keep` 0.37-0.38 in the log
  after a trim, 0.22 on a new run's first round — the server spends
  1.1-1.5 s between choosing the slot and starting the work (about
  1 ms otherwise): believed to be the save and restore through the
  host-RAM prompt cache that the ADR-0003 gate saw (about 1.7 s).
  One trim of four paid only 174 ms — believed: that round's prompt
  was identical to the first drive's (same seed), so the server
  restored a matching state from its host-RAM cache; a third
  identical drive (2.3's check) then reused 777 cached tokens after
  its trim, not 512. So identical repeat drives understate a trim's
  cost; the first drive's 1.3-1.5 s is the number. The owner's hunch
  (the gate's "evictions") pointed at it. (2) **A stall before the
  request reaches the server:** once in 56 requests (round 8 of the
  first drive, not in the repeat), 1.5 s passed between one round's
  end and the server even seeing the next request. *Ruled out the
  same day, on the owner's question: an idle unload of the model
  (ollama's `keep_alive`). llama.cpp has the knob,
  `--sleep-idle-seconds`, but it defaults to -1 (disabled) and the
  box's container does not set it (`docker inspect`); the previous
  round had ended only 1.5 s before; and the round's prompt was read
  in the normal 364 ms, with no server log line during the stall.*
- **Where flagged:** Task 6b step 2.2's measurement ([discussion
  2026-09-22] grammar-and-prompt-cache-lessons §4.10 question 3,
  answered that day); the runs `runs/2026-09-24T17-12-04/` and
  `runs/2026-09-24T17-15-15/` in the fork.
- **Trigger:** (1) if the trim's pause is heard in rehearsal, or a
  show needs trims often; (2) if stalls show up again in drives or in
  the browser.
- **Fix shape:** (1) one server flag at a time through the playbook,
  measured the same way — `--cache-ram 0` first (no host-RAM cache
  to save to; what the slot then does on a trim is itself the
  question); (2) time the phases of the app's request to llama.cpp
  (connect, first byte) to see whether the stall is in the app or in
  the SSH tunnel — upstream's LLM client opens a new connection per
  call, so each round opens a new tunnel channel. How to read the
  server's side: `docker logs llama`, the lines `selected slot`,
  `launch_slot_` and `release` (their timestamps and `f_keep`).

## Prefetch the next round — hide the silence between rounds

- **The gap:** the `/show` page asks for round N+1 only when round
  N's audio has drained (the browser is the clock, SED), so every
  round boundary is silent while the model writes the first line
  (0.76-0.94 s through the app and the tunnel in the checkpoint
  drive; 2.37 s after a trim) and the voice synthesizes the first
  chunk (1-3 s for short lines): about 2-4 s, estimated — not yet
  heard in a browser.
- **Where flagged:** [discussion 2026-09-25]
  show-slice-3-browser-plan §2-§3 (the owner: "worth documenting");
  the TODO's polish list ("prefetch round N+1").
- **Trigger:** the page plays rounds by ear (slice 3) and the silence
  between rounds bothers the listener.
- **Fix shape:** request N+1 on N's `complete` (its text streamed),
  with `played_s` = the seconds played + the duration of the audio
  still queued (exact from the decoded clips); never after an
  invitation (the listening window is the gap). Measure first whether
  the model and the voice slow each other on the shared GPU.

## Resume the same run after a page reload

- **The gap:** a reload of the `/show` page forgets the run and Start
  opens a new one (the owner's ruling for slice 3); the old run's
  record stays on disk. A crash mid-show restarts the story.
- **Where flagged:** [discussion 2026-09-25]
  show-slice-3-browser-plan §6 (item 5, question 3).
- **Trigger:** a reload or a crash during a long show hurts — above
  all near the talk.
- **Fix shape (about an hour with tests, estimated):** keep the run id
  in the URL (`/show?run=...`); a read route (for example
  `GET /api/show/run/<id>`) gives back what the page loses — the
  played seconds so far (restarted at 0, the cadence would count the
  time since the last invitation as negative, and no invitation would
  come for minutes) and whether the last round was an invitation (the
  listening window opens first). Two gaps remain: the last round's
  own audio length is never recorded, so the resumed clock is an
  estimate; and a round whose text arrived but whose audio never
  played is skipped.

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

## An "exchange" round — the director has one character address another

- **The gap:** the characters report to the room; they rarely talk
  to each other. In the first real run of the show engine (the
  fork's `runs/2026-09-24T02-18-51/`, 10 rounds, seed 42), none of
  the 24 lines named another character — first names, surnames and
  "Dr." checked by script — and only one spoke to anyone at all
  ("You should've locked the east wing when we still had power!",
  the addressee unnamed). Director v1's rule "anyone named in the
  last round is allowed next" ([discussion 2026-09-23]
  show-engine-design §5.7) therefore has little to act on. One run,
  one seed: a tendency observed, not established.
- **The idea:** a fifth kind of round beside free, invitation,
  answer and static — **`exchange`** (the name proposed
  2026-09-24; "cross-talk", the radio word for on-air banter, was
  the alternative, set aside because it also means signal
  interference). The director picks two characters and says who
  addresses whom: "Moira asks Ralph something; Ralph answers: the
  next two lines, each with the emotion in its voice." The grammar
  can enforce the order, not only who is allowed:
  ```
  root   ::= first second
  first  ::= "Moira" " (" emotion "): " text "\n"
  second ::= "Ralph" " (" emotion "): " text "\n"
  ```
  The verb could come from a short list, like the tone words: asks,
  warns, blames, reassures, teases, confides in.
- **Why the director and not the format rules:** asking for it in
  the cast sheet's format paragraph would change the texts pinned
  byte for byte to the proven prompts (the fork's
  `tests/test_show_story.py`) and lose that anchor; the director's
  instruction is per round and leaves the anchor alone. The
  character bibles (Task 4) may change the picture by giving the
  characters relationships to talk across — believed, not measured.
- **Where flagged:** the owner, 2026-09-24, reviewing director v1
  (Task 6b step 2.1): record it "if the need arises and we have
  time"; execution undecided.
- **Trigger:** drives on the box, or the listening test of slice 3,
  show the characters still rarely speaking to each other, the
  owner's ear minds, and there is time after the timebox's
  essentials.
- **Fix shape:** in the fork, the director gains the kind (how often
  — a chance per free round, a yaml knob) and its instruction
  words; `build_grammar` gains an ordered form (a sequence of named
  lines instead of `line{1,N}`); tests in the manner of step 2.1's
  (words and grammar agree; the order is enforced). About the size
  of one checklist step (estimate).

## Events that stay on topic for a few rounds

- **The gap:** the director draws each event at random from the
  whole pool (without repeats until the pool is used up), so the
  story jumps between unrelated threads — a flooded basement, then
  a listener in Anchorage, then a specimen jar — and the lab's
  backstory can drift ("a sample logged here eleven years ago" and
  "the university burned the same sample" may both come up). How
  often events come: in free rounds with an odd round number only
  (the fork's `app/show/director.py`, `n % 2 == 1`) — about every
  other round; at the driver's 20 s of audio per round, roughly one
  event per 40 s of show (the real audio per round is unmeasured).
- **Two ideas, the owner's (2026-09-24):**
  1. **Semantic neighbors.** Embed every event once and draw the
     next one near the last one, so a thread continues for a few
     events before the story moves on. At the pool's size (289
     events, 2026-09-24) a vector database is more than needed: the
     embeddings, computed once and stored as a file in the story
     folder, and a nearest-unused-neighbor pick do the same job; a
     database pays off only with thousands of events or episodes
     written on the fly.
  2. **Topic runs, almost free.** The pool is already written in
     14 topic groups, and the director stays in one group for a few
     events, then jumps to another. The groups are only YAML
     comments today, which the loader discards — they must become
     data first (`events:` as a mapping of group to list, the loader
     accepting both forms). Within a run, pick at random rather than
     in file order: the order inside a group is the writing order,
     not a story arc, and a fixed walk would repeat the same sequence
     every show. The current group and the run's length are derived
     from the record, like all of the director's memory, so a seed
     still replays a run.
- **Where flagged:** the owner, 2026-09-24, after the events pool
  grew from 10 to 289 ("which we will probably never have time to
  execute, but I do not want to forget it").
- **Trigger:** listening to real rounds (on the box or in slice 3),
  the events feel scattered and the story never settles on a
  thread — and there is time after the timebox's essentials. Idea 2
  first; idea 1 only if 2 is not enough. Episode beats
  ([discussion 2026-09-23] show-engine-design §2.4, §5.7) are the
  ordered, authored form of the same wish.
- **Fix shape (idea 2):** the loader reads grouped events into
  `Story.events` plus each event's group; `_next_event` stays in the
  last event's group with a chance that falls as the run grows (a
  yaml knob for the typical run length); tests: runs occur, no
  repeats until the pool is used up, the same seed replays.

## Events the listener cannot hear — the characters react to what only the model was told (owner, 2026-09-25)

- **The gap:** the director gives an event to the model at the head of
  a free round's instruction ("Offstage: The blood samples … Daniel and
  Moira speak next: …" — the fork's `app/show/director.py`,
  `instruction_for`), and nothing says the listeners cannot see it; so
  the characters react like people who saw it together, and a listener
  hears reactions to things never told. The show engine's design
  assumed the reactions would carry the event (SED §5.7: "the audience
  learns of an event through the characters' reactions" — dated note
  2026-09-25). The `/show` page's captions hide the gap: they show the
  event as a stage direction in brackets. By ear there is no bracket —
  so the by-ear checks (slice 3's step 3.4) are judged with captions
  off. The jumps between unrelated events (the entry "Events that stay
  on topic for a few rounds") make it worse.
- **The owner's evidence** (the page, the fork's run
  `2026-09-25T14-57-06`, rounds 55-58, debug on; as pasted):

  ```
  [The infected at the south gate are tearing at a car, but the car is empty.]

  Daniel (calm): They're wasting energy. Over.

  Samantha (calm): Let them chew on a rusted shell. Over.

  Daniel (calm): We'll move when we're ready. Over.

  round 55 · free · speakers Daniel, Samantha · event The infected at the south gate are tearing at a car, but the car is empty. · tone swaggering · first line 1.1 s · round 2.4 s · run 2026-09-25T14-57-06

  [The blood samples from the first victims have separated into three layers instead of two.]

  Daniel (calm): Three layers? That's new. Over.

  Moira (calm): It's either a mutation or a trick. Over.

  round 56 · free · speakers Daniel, Moira · event The blood samples from the first victims have separated into three layers instead of two. · tone swaggering · first line 1.2 s · round 2.4 s · run 2026-09-25T14-57-06

  Moira (calm): We'll test it. Over.

  Ralph (calm): If it's a trick, we'll laugh. Over.

  Moira (calm): Either way, it's our problem. Over.

  round 57 · free · speakers Moira, Ralph · event — · tone swaggering · first line 1.3 s · round 3.1 s · run 2026-09-25T14-57-06

  Moira (calm): We'll crack it. Over.

  round 58 · free · speakers Moira, Samantha · event — · tone swaggering · first line 1.0 s · round 1.9 s · run 2026-09-25T14-57-06

  [A dark handprint appears on the inside of the observation window.]

  Ralph (urgent): We need to seal that window. Over.

  Samantha (urgent): The handprint's recent. Over.

  Ralph (urgent): Could be a trap. Over.

  Samantha (urgent): We'll reinforce it. Over.
  ```

  The owner: after "[The blood samples from the first victims have
  separated into three layers instead of two.]", Daniel's "Three
  layers? That's new. Over." — the listener will never know what
  these layers are: a context-sharing problem.
- **Options** (1-3 the owner's, 4 the agent's):
  1. **A narrator.** The owner hesitates: a voice outside the fiction
     breaks the emergency-broadcast frame that imitates Orson Welles's
     *The War of the Worlds* (1938), which played on the ambiguity
     between a radio play and a real newsfeed. The agent agrees; the
     in-world announcer already exists — the operator (Samantha), whose
     job is reporting — which is option 3 with her as the describer.
  2. **An event round**, a new kind with its own instruction (the
     owner's wording: "The characters describe the event that just
     happened and comment to each other the consequences of this
     event."); then rounds continue as usual.
     Costs a round kind in the director, the record, the summary and
     the page; no extra request if it replaces the free round.
  3. **A describe-it round trip** per event: one character describes
     the event in their own words; then rounds continue as usual. The
     most control; costs one more request per event (another
     round-boundary gap of ~2-4 s, [discussion 2026-09-25]
     show-slice-3-browser-plan §2) and one more line, about every other
     free round.
  4. **The wording alone, in the same round** — the agent's lean: for
     example "Something happens that the listeners cannot see: X.
     Daniel tells the listeners on air what is happening; then Daniel
     and Moira speak: …". The characters are on air, so reporting is
     what they would do — the device the Welles broadcast is built on
     (reporters describing to the audience what they witness). One
     sentence in `instruction_for`; the director already picks the
     speakers, so it can name the reporter (the first speaker, or the
     operator when she is in the round). Risk: the model may skip or
     bury the description — the grammar enforces who speaks, not what
     is said; then option 3 with the operator.
- **Where flagged:** the owner, 2026-09-25, watching the `/show` page
  during slice 3's step 3.1 (the plan's discussion, [discussion
  2026-09-25] show-slice-3-browser-plan).
- **Trigger:** before the by-ear exit criterion (slice 3's step 3.4),
  or whenever the owner wants to hear the show make sense.
- **Fix shape — decide by an A/B test:** the driver at seed 42, 20
  rounds each, today's wording against option 4's; read the first line
  after each event and count the events a listener could follow without
  the caption. If option 4 falls short, try option 3 the same way.

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

## Markdown emphasis in spoken lines — kept for now; re-test with any new TTS engine

- **The finding (2026-09-24):** the model sometimes marks emphasis
  the way chat text does. In the first live drive of director v1
  (the fork's `runs/2026-09-24T14-43-54/`, round 7, tone word
  "impish"), Moira's line came back as `How *charming*.` Nothing
  stops the marks on their way to the voice: the grammar's text rule
  (`[^\n\[\]()]+`) allows `*` and `_`; the format rules forbid
  markdown only in words; the parser's voice-only replacements
  (the fork's `app/show/parser.py`, `_SPOKEN`) cover curly quotes,
  dashes and the ellipsis; upstream's browser and server TTS code do
  no text cleanup (checked 2026-09-24).
- **The listening test (the owner, by ear, 2026-09-24):** the same
  line three times in Moira's voice through the fork's `/api/tts` —
  plain, with `*charming*`, with `_charming_` — on tts-serve 1.2 with
  Faster Qwen3-TTS and the `say`-made reference voice. All three
  sounded poor, believed to be the artificial reference voice; but
  the ranking was clear: the asterisks most natural, then the
  underscores, the plain line least natural. The engine seems to
  read the marks as emphasis and inflect the word.
- **Ruling (the owner, 2026-09-24):** keep the marks; no action for
  now.
- **The risk:** another TTS engine — on the owner's wishlist (this
  file: "Add new TTS engines", "LuxTTS landed upstream") — may react
  differently: read the marks aloud, pause on them, or ignore them.
- **Trigger:** any TTS engine change, or the real reference voices
  (Task 5b): re-run the three-line test and listen.
- **The test, to repeat it:** with the fork's app serving (the
  runbook `docs/runbooks/show-driver.md`), three
  `POST /api/tts` calls with `{"text": …, "persona_name": "Moira"}`;
  each reply's `audio_base64` decodes to a WAV file.
- **Fix shape if an engine mishandles them:** strip `*` and `_` from
  the spoken text only; the history keeps the model's raw text.
  Forbidding them in the grammar instead would break the
  byte-identical anchor and force the model.
- **The replacements must be per TTS engine** (the owner,
  2026-09-24): a single table changed for each new engine would
  leave the previous engine misconfigured, since engines react
  differently to the same characters (this test: Faster Qwen3-TTS
  inflects on `*` and `_`). The shape, refined in discussion: a
  shared base table (the replacements every engine takes, today's
  `_SPOKEN`) plus per-engine exceptions, each engine's re-checked by
  ear with the three-line test; the table chosen by the engine the
  TTS server reports — `engine` in tts-serve's `/capabilities` (the
  box, 2026-09-24: `faster-qwen3-tts`, model
  `Qwen/Qwen3-TTS-12Hz-1.7B-Base`), a document the app already
  caches — never by a setting to keep in sync, so an engine switch
  in Settings brings its table along, and an engine without one gets
  the base table.

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
