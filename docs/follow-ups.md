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

- **Status 2026-09-25 — partly measured, by the `/show` page's voice**
  (slice 3's step 3.2; the fork's run `2026-09-25T16-04-56`; each
  chunk timed in the browser, through the app's `/api/tts` and the
  tunnel): 8 chunks of 27-55 characters took 2.4-3.2 s each to
  synthesize (one 4.6 s), for clips of 2.0-3.6 s — synthesis time over
  clip length 0.8-1.4. **The cost is mostly fixed per request**
  (27 characters: 2.5 s; 55: 2.95 s), about 2.3 s. So: a short line
  cannot hide behind the one before it (silences of 1.2-1.9 s inside
  rounds, where the next chunk was not ready; 250 ms otherwise, the
  configured pause); the gap between rounds is 3.7-4.9 s once warm
  (the first line ~1.0-1.2 s, then its synthesis); and smaller chunks
  would cost more, not less (the "Over." entry below). A suspect for
  the fixed cost — believed, not measured: the app sends the persona's
  reference clip to tts-serve with every request, through the tunnel
  (tts-serve tour F3); tts-serve's `time_used` would split the server's
  time from the transport's. Not measured yet: 100-400 characters. The
  owner, listening: "The pauses do not feel so bad actually."

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

- **Status 2026-09-28 — post-timebox, behind Task 4 and Task 7** (the
  owner, ruling the polish at the timebox's close: "I want to pull forward items: "1. Dead-air static while a round is generated" and "2. The 1930s radio look, with your gauge" , right after Task 4, and leave the rest as post-timebox follow-ups behind Task 4 and Task 7.").
- **The gap:** the `/show` page asks for round N+1 only when round
  N's audio has drained (the browser is the clock, SED), so every
  round boundary is silent while the model writes the first line
  (0.76-0.94 s through the app and the tunnel in the checkpoint
  drive; 2.37 s after a trim) and the voice synthesizes the first
  chunk (1-3 s for short lines): about 2-4 s, estimated. **Measured
  2026-09-25 with the voice** (step 3.2): 3.7-4.9 s once warm (6.8 s
  for a run's first round, the TTS cold) — see the entry "Measure TTS
  synthesis time against text length". Prefetch would hide this gap,
  not the silences inside a round (the voice synthesizes one request at
  a time, tts-serve tour F5).
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

## Episodes — a story arc, with a recap between episodes (owner, 2026-09-23; post-timebox, 2026-09-28)

- **The idea (the owner, 2026-09-23):** the show as a series of
  episodes, each starting fresh with the cast sheet, a "previously
  on…" recap and a new scene set for the model to improvise in; it ends
  at a story beat, or at a size limit as a backstop ([discussion
  2026-09-23] show-engine-design: the owner's words verbatim in §2.1,
  the option — number 5 — in §2.2). The recap comes from the episode file, written in advance,
  not from the model.
- **What it gives:** a story arc instead of an endless loop; a clean
  reset of the history between episodes — the trim's job, with no pause
  mid-show; clean start and stop points for the talk; the canned
  episode (Task 7) becomes one recorded episode.
- **Where flagged:** the design discussion above (the stretch of the
  timebox; the `{{ episode }}` placeholder in the cast sheet is already
  there, empty); the TODO's polish list until 2026-09-28.
- **Status 2026-09-28 — post-timebox, behind Task 4 and Task 7** (the
  owner, ruling the polish at the timebox's close: "I want to pull forward items: "1. Dead-air static while a round is generated" and "2. The 1930s radio look, with your gauge" , right after Task 4, and leave the rest as post-timebox follow-ups behind Task 4 and Task 7.").
- **Fix shape:** the minimal mechanism — the director knows it is in an
  episode (a scene setup and a recap from an episode file), ends it at
  a beat or a size limit, and starts the next fresh; one hand-written
  episode ships; writing more stories is later show work (the spec's
  post-release scaffolds). A day or more (estimate).

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

## Talk anytime — the listener breaks in while a round plays (polish; the owner's preference, 2026-09-25)

- **The idea:** with a push-to-talk button, the listener should be able
  to break in at any moment, not only when the operator invites them.
  A press interrupts the round's voices — the round's text stays
  recorded as complete — and makes silence for the microphone to
  listen; the message rides the next round request, and the director
  forces that next round to answer the listener. The listening window after an invitation stays: it tells
  the listener that talking back is possible.
- **Decided for the MVP (2026-09-25, slice 3's step 3.3):** keep the
  listening window as designed; talk anytime is a polish follow-up.
  The agent had argued that the window does two jobs push-to-talk
  alone does not — it is the show's pause for an answer (without it, an
  answer is used only after the next round, 10-15 s of audio later),
  and it is the clock that declares silence (the static round). **The
  owner disagrees with both reasons** and records the preference
  (verbatim):

  > But I want to record that I disagree with your two reasons under "Is the listening window unnecessary with push-to-talk?". 
  > (1) The pause in the show was necessary because in my 2024 prototype I did not have a push-to-talk button, as it was a CLI app.
  > (2) I am not saying to remove the listening window, that can stay always, is a way to explain to the listener that the option to talk back exists. What I am saying is that with a push-to-talk capability it follows that the user should be able to interject his message  anytime, the message can be recorded while the round is playing, and in the next round the director forces a type of round that answers to the user.
  >
  > But, let's keep this as a polish follow-up. Agreed with your posture here.

  The owner then corrected one point of that message (verbatim):

  > Actually, I correct myself "the message can be recorded while the round is playing" this is not correct, I meant that the playing of the round voices can be interrupted (even if the round text is recorded as complete), and make silence for the mic to listen.

- **What it would take (the agent's first sketch, not decided):**
  (1) the server accepts a transcript at any round — today one that
  arrives outside a listening window is ignored with a warning (the
  fork's `app/routers/show.py`, `_round_stream`) — and the director
  plans an answer round whenever words are heard, not only after an
  invitation (`app/show/director.py`, `plan_round`); (2) the page
  enables the talk button while rounds play; a press cuts the voice
  (`stopVoice()` in the fork's `static/show/player.js`), records in the
  silence, and sends the recording with the next round request — so the
  show's own voices are never in the recording (on speakers they would
  be, and Whisper would transcribe the actors with the listener), which
  the owner's correction settles by design; (3) the lines cut short stay
  in the record, so the model builds on words the listener never heard
  (as with a Stop after the server kept a round, step 3.1) — to be
  judged by ear. About 1-2 h, estimated.
- **Where flagged:** the owner, 2026-09-25, while shaping step 3.3
  ([discussion 2026-09-25] show-slice-3-browser-plan; the page's
  microphone opens only during listening windows, as step 3.3 builds
  it).
- **Trigger:** polish, after slice 3's exit criterion (step 3.4 — met
  2026-09-25); before the talk if time allows.

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

## An "exchange" round — the director has one character address another

- **Status 2026-09-28 — the name is taken; the idea stands.** Since
  step 3.4c, "exchange" names the round where the cast answers a
  listener (spec §6.4, Contact mode), and the round kinds named below
  (free, invitation, answer, static) are director v1's, which step
  3.4c reorganized into Broadcast and Contact. The idea — one character
  addressing another, in order, in the free rounds of Broadcast —
  needs a new name when it is taken up.

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
  repeats until the pool is used up, the same seed replays. The tone
  words get the same treatment in step 3.4c — their themes kept as
  data (the follow-up "The tone themes as data — five uses waiting for
  them", use 4: theme runs); one shape for both files.

## Comic relief — the cast jokes about a funny happening (owner, 2026-09-26; postponed from step 3.4c)

- **The idea:** from the owner's 2024 prototype, as the owner remembers
  it (verbatim, 2026-09-26):

  > * Something that I had in the regular programming (or maybe it was in my wishlist and I am enriching the memory) it's a "make a joke" mode, where we direct the LLM to make jokes about funny occurrences that we provide (pre-canned like events), something like "Oh, no! Is that Betty from accounting among the zombies? They got her!... Look, she is still holding her calculator in the hand... Habits die hard indeed. hahaha".
- **Where flagged:** [discussion 2026-09-26] show-director-modes — the
  owner's 2024 design (§2) and feature 6 of the agent's decoding (§3).
  Postponed with feature 7 (the next entry), the owner (§4): "yes, this
  is not about engagement so can be postponed." And later the same day:
  "I did not retire "6. Comic relief", I postponed it, so it should have
  a proper follow-up entry. We are going to execute on this at some
  point."
- **Where it fits:** the Broadcast mode of that discussion — the cast
  talking among themselves while the receiver is down. It does not
  involve the listener.
- **Fix shape (the agent's, not yet discussed):** a story list of funny
  happenings (e.g. `stories/lab-outbreak/jokes.yaml` in the fork),
  drawn like the events — without repeats until the list is used up
  (`_fresh` in the fork's `app/show/director.py`), paced every few free
  rounds with jitter (a knob like `show.event_every`) — and worded as an
  instruction to joke about it on air. Like an event, the listeners
  cannot see it, so the first to speak says what they see
  (`show.event_report`). Open: whether a joke takes an event's place in
  its round or has its own pacing. The tone words already hold the
  palette: `stories/lab-outbreak/tones.yaml` has the groups "Gallows
  humor and wit" and "Levity and play", drawn only at random today
  (from step 3.4c on, themes kept as data — the follow-up "The tone
  themes as data — five uses waiting for them", use 2).
  Tests like the events'.
- **Trigger:** after step 3.4c and slice 3's close (both done
  2026-09-28); a candidate for the show fixes before the talk or for the
  show arc (stories and episodes) — the owner's call.

## Scientific findings — the cast reports what the lab learns about the infection (owner, 2026-09-26; postponed from step 3.4c)

- **The idea:** from the owner's 2024 design (verbatim, 2026-09-26),
  said while describing what the cast asks a listener:

  > We could also make one of their focus to describe the "scientific findings" from the infestation instead of asking questions, although I think this fits better their regular programing (when the radio is broken).
- **Where flagged:** [discussion 2026-09-26] show-director-modes —
  feature 7 of the agent's decoding (§3); postponed with feature 6 (the
  entry above), the owner (§4): "yes, this is not about engagement so
  can be postponed."
- **Where it fits:** the Broadcast mode, as the owner said — not the
  conversation with a listener.
- **Fix shape (the agent's, not yet discussed):** a list of findings,
  drawn like the events and worded as a finding one scientist reports on
  air. Either a story file of its own or a group of `events.yaml` — the
  pool already holds lab happenings such as "Sample twelve in the cold
  room has started moving inside its sealed jar." A finding could
  continue across rounds (the follow-up "Events that stay on topic for a
  few rounds").
- **Trigger:** the same as comic relief's.

## Pace the calls in rounds, not seconds — one unit for all pacing (owner, 2026-09-26)

- **The idea (the owner, verbatim, 2026-09-26, while shaping step
  3.4c):** "I am proposing that we unify all pacing measurements on
  count of number of round, and not time." And: "Maybe not for right
  now, but to keep it as an identified follow-up..."
- **Today:** the only pacing counted in time is the cadence of the
  calls — seconds of played audio since the last invitation (the
  fork's `app/show/director.py:68-80`, `_time_to_listen`;
  `show.interaction_min_s` 60, `show.interaction_max_s` 180), from the
  round request's `played_s`, which the page reports because only the
  page knows what has played. From step 3.4c on, counted from the
  moment the receiver goes off ([discussion 2026-09-26]
  show-director-modes). Every other pacing is already in rounds: the
  event gap (`event_every` ± `event_jitter`, free rounds), the tone
  hold (`tone_hold` ± `tone_jitter`), and 3.4c's contact length (the
  listener's answers) and silence count. Not pacing, and staying in
  seconds either way: the listening window (`listen_window_s`) and the
  press cap (`press_cap_s`) — wall-clock timers.
- **History:** seconds came from the owner's own pushback on
  2026-09-21 ([discussion 2026-09-21] story-loop §9 Q2) against the
  agent's "every third or fourth round": (1) rounds are seconds long,
  so that count opens the microphone about every minute and pauses the
  show; (2) a fixed count is predictable; (3) the interval must be
  configurable and tuned by ear. A round count with jitter, in
  settings, meets (2) and (3); (1) asks for larger counts, e.g. 10-30
  rounds.
- **For rounds:** one unit for all pacing; the director a function of
  the record and the seed alone, with no number from the page (the
  round request's `played_s` would then feed only the debug line and
  the record); the driver no longer invents played seconds (`--played`,
  20 s per round by default, the fork's `scripts/drive_show.py:213`).
- **Against:** rounds vary in length — 1 to 4 lines, a one-line re-call
  against a three-line exchange — so the time between chances to talk
  gets less even; over the 10-30 rounds between calls it mostly
  averages out.
- **No help to step 3.4c's testing** (the owner asked): the driver
  already reports a fixed 20 s per round, so under the driver the
  cadence is already a round count (60 s = 3 rounds); the unit tests
  pass `played_s` directly; by ear, temporary settings bring the calls
  forward either way. 3.4c's "count from the receiver going off" works
  in either unit.
- **Trigger:** after step 3.4c, when the calls' spacing is tuned by ear
  — if seconds buy nothing audible over rounds, simplify to rounds.
- **Fix shape:** `_time_to_listen` counts broadcast rounds since the
  receiver went off; the two settings become round counts (names
  indicative: `call_min_rounds`, `call_max_rounds`), the linearly
  rising chance kept; tests; the runbook `docs/runbooks/show-driver.md`;
  a dated note on SED §5.7 and on story-loop §9 Q2.

## The tone themes as data — five uses waiting for them (owner, 2026-09-26)

- **What exists from step 3.4c on:** the 24 themes of the tone words
  ("Hope and warmth", "On the air, 1930s", "Fever and chaos", …) are
  keys inside each overtone of the story's overtones file, which
  replaces `tones.yaml` in the fork's `stories/lab-outbreak/`; a mixed
  theme appears under two overtones. The loader reads each word with
  its overtone and its theme; 3.4c's draw uses only the overtone
  ([discussion 2026-09-26] show-director-modes, the overtone's
  details). The owner, who asked to keep the themes (verbatim): "I like
  this grouping of therms a lot and I think we should preserve this in
  some way." — and to store these uses "in a prominent but adequate
  position in our docs".
- **The uses (the agent's, 2026-09-26):**
  1. **The orientation round** draws its tone word from "On the air,
     1930s" ("broadcast-polished", "newsreel", "static-laced") — the
     station-identification register.
  2. **Comic relief** (the follow-up "Comic relief — the cast jokes
     about a funny happening") draws from "Gallows humor and wit" and
     "Levity and play".
  3. **The Breakdown** leans on "Fever and chaos" or "Nerves and
     tension".
  4. **Theme runs:** hold one theme for a few rounds — the same wish as
     the follow-up "Events that stay on topic for a few rounds" (its
     idea 2: the events' groups as data).
  5. **The debug line** shows the theme next to the tone word.
- **Trigger:** each use when its feature is built (comic relief, theme
  runs), or when listening shows a need (the orientation's register,
  the Breakdown's). Use 5 is small enough to fold into 3.4c's build if
  convenient.
- **Fix shape:** per use, a director rule "in a round of kind K, draw
  the tone word from theme T, when the round's overtone holds it" — a
  kind-to-theme mapping in the story's overtones file, so another story
  brings its own; tests like the tone word's.

## A listener memory keyed by identity — revisit how the show remembers a returning listener (owner, 2026-09-26)

- **Status 2026-09-26, evening — measured; RULING: names-only A, a show
  fix before the talk.** Step 3.4c.5's driver test ran B in two
  wordings and A simulated with a perfect extractor, on the same
  script and seeds ([experiment 2026-09-26] listener-memory-b-vs-a:
  the scripts, the raw runs, the findings). An anonymous "Hello again,
  lab." was treated as the most recent caller, Maria, in 3 of 3 drives
  with B in both wordings, and in 0 of 3 with A — A's cast asked who it
  was; Alfredo's name, across his return's rounds, 3 of 12 with the
  committed B against 7 of 12 with A; the rest within noise. The gains
  come from knowing who is speaking, not from the facts. The owner:
  "We are going to do: "a. B for 3.4c; names-only A becomes a show fix
  before the talk, with the follow-up updated.""
- **The shape to build (names-only A):**
  - **detect the caller's name, or its absence, for each answer**, in
    code — the only new piece: a second small model request with a
    grammar that allows only one of the known callers' names, "new:
    ‹Name›", or "none", which also maps Whisper's spellings ("Alfred")
    to a known caller; plain patterns are the fallback (about 30
    minutes, brittle: "this is crazy" matches "this is …"); the delay
    it adds per answer is unmeasured;
  - **keep it in the run's record** — one optional field per round, so
    the director stays a function of the record and old runs load;
  - **the restatement states who the voice is** — anonymous ("This
    voice has not said who they are. Callers you know: … Do not guess
    which one this is."), new ("This is Maria, a new caller."),
    returning ("This is Alfredo, who called before. Greet them as a
    returning friend, by name."); the facts stay the listener's quoted
    words, grouped under the caller's name. The simulation's
    `sim_a.py` is the draft.
  - **Estimate:** about 3 hours — detection about 1 h, the record
    15 minutes, the director about 1 h, a driver test on the box with
    the words spoken and heard by Whisper about 30 minutes; the agent's
    build estimates ran high lately (3.4c's four sub-steps took about
    1 h 07 against 4-6 h), so 1.5-3 h.
  - **Test first:** detection on real speech — names Whisper mangles,
    "I'm Alfredo's friend", nicknames. A small model follows a wrong
    conclusion as faithfully as a right one: a misheard name would have
    the cast greet the wrong person with confidence.
- **The decision to revisit:** in step 3.4c the restatement — the
  listener's words repeated, verbatim, in each contact instruction —
  reaches over the whole run, grouped by contact, oldest first, capped
  at the last few contacts (a setting), with one line asking the model
  to greet a voice it spoke with before as a returning friend and use
  what they told it. The model does the matching; no identity in code
  ([discussion 2026-09-26] show-director-modes, the agenda's details).
- **The owner's idea behind it (verbatim, 2026-09-26):** "What if we
  keep in memory a cache of all answers provided by each user (once the
  user has identified itself), that way we can provide even more context
  for returning users. Otherwise the model will forget who the user is
  between subsequence contacts. This can complicate things a bit, but I
  think giving some sort of a memory of past interactions with the user
  is worth it."
- **The alternative to consider (the agent's option c, which the owner
  asked to keep, verbatim):** "A memory keyed by identity, with names
  extracted in code and matched across contacts. It's the most exact,
  but it needs A's extraction and fuzzy name matching. A follow-up, tied
  to A, if b falls short." The owner: "Add a follow-up entry to revisit
  this decision in the future and consider implementing instead".
- **What it needs:**
  - **extraction** — the listener's name (and maybe place) pulled out
    of the transcript in code: option A of feature 5 in that discussion
    (§5.1), with the ways the agent listed — a second small request to
    the model with a grammar after each listener turn, a hidden "facts"
    line at the top of the answer's grammar, or plain patterns ("my
    name is …", "this is …");
  - **fuzzy matching** — Whisper may spell one name differently from
    one contact to the next (SED §6.3: a misspelled cast name, "Maura"
    for "Moira", defeats an exact match);
  - **a per-listener store** — derived from the run's record like all
    of the director's memory, or a new field in it.
- **Not identity by browser:** at a demo, many people talk through one
  laptop — one browser, many listeners.
- **Across runs:** both b and c last one run; a page reload starts a new
  run. Memory across runs is a feature of its own (see also "Resume the
  same run after a page reload").
- **Trigger:** ~~the driver test or the owner's ear shows b falls short —
  the model misses a returning voice, mixes two listeners up, or the cap
  drops a listener who comes back later — or option A comes back for
  feature 5~~ — **fired 2026-09-26** (the driver test: B takes an
  anonymous returning voice for the most recent caller). Now: among
  the show fixes before the talk (slice 3 closed 2026-09-28).

## Event texts reworded as lines of dialog — a personal account from the cast (owner, 2026-09-27)

- **The gap:** with the fixed lines ruled on 2026-09-27 (after step
  3.4c.5's test by ear), a cast member reads an event's text word for
  word on air. The texts in the fork's `stories/lab-outbreak/events.yaml`
  (289: positive 29, neutral 94, negative 166) are written as narration
  in the third person, not as something a person says.
- **The owner (verbatim, 2026-09-27):** "I expect some percentage of the
  event lines may need to be re-written to better suite a line of
  dialog, providing a more personal account, and more details of what
  is happening. e.g. `- A dusty guitar turns up in the security office,
  with all six strings.`, clearly this line is not a good dialog line to
  be told in first person, instead it should be something like `- Guys!
  A dusty guitar turned up in the security office, with all six
  strings!`. Seems small, but it's important.... However, this is not
  the time to fix this, we can do later... But we should save this as a
  follow up to not forget."
- **Trigger:** after the fixed lines are built — the owner's call.
- **Fix shape:** go through the events and reword those that do not
  read as speech — said by someone in the lab, to the others or to the
  listeners, about what just happened, with a concrete detail; the
  agent drafts, the owner reviews. Rewording events changes the
  baseline of the wording experiments (the driver test), so it is a
  measured step of its own.
- **Also (2026-09-28): events heard on the radio while the receiver is
  off.** About twenty events describe something heard over the radio —
  "A boy on the frequency says his parents went out to find food and
  haven't come back.", "A school choir on the frequency sings for the
  lab.", "The military frequency repeats one word, 'Evacuate', then goes
  silent." — yet events come only in the broadcast, while the receiver
  is dead or switched off. Seen in the owner's listen of 2026-09-28 (the
  fork's run `2026-09-28T13-43-28`): round 112 read the boy's event two
  rounds after the Switch-off. The owner (verbatim): "Let it be. This is
  a minor issue, and I do not think it has an easy fix. You can make a
  small addition to the "Event texts reworded as lines of dialog"
  follow-up to not forget this detail, but I do not think it's worth
  acting on this." — noted, not planned; if the events are reworded,
  these could be reworded as something the cast heard earlier, or left
  out while the receiver is off.

## The contact agenda — more items (owner, 2026-09-27)

- **The list:** the fork's `stories/lab-outbreak/agenda.yaml`, nine
  two-branch items, the name item first (step 3.4c; [discussion
  2026-09-26] show-director-modes §15.9). Reviewed by the owner before
  the test by ear.
- **The owner (verbatim, 2026-09-27):** "I reviewed the agenda items.
  They could be improved with more items, but I want to keep it as is
  for the moment, because if we change it now we change the baseline
  for comparing prompt wording improvements like the last experiments
  we just did. So any improvements ti agenda items would be a follow
  up."
- **Trigger:** once the wording work measured against the driver
  test's baseline is done — the owner's call.
- **Fix shape:** the agent drafts more items in the same two-branch
  form (ask for something; if the voice already gave it, use it); the
  owner reviews; a driver test before and after.

## Events the listener cannot hear — the characters react to what only the model was told (owner, 2026-09-25) — option 4 adopted

- **Status 2026-09-28 — resolved; kept for its receipts.** After option
  4, the fixed lines (step 3.4c.6, 2026-09-27; the fork's `07669dc`)
  settled it: the round's first speaker now reads the event's own text
  word for word on air, and the model reacts (spec §6.5) — a listener
  hears every event told. Nothing here is open; the entry stays
  because the TODO and [discussion 2026-09-23] show-engine-design cite
  its A/B receipts — deleting it waits for the owner's word. What is
  left of events is in the follow-ups "Event texts reworded as lines
  of dialog" and "Events that stay on topic for a few rounds".

- **Status 2026-09-25 (night) — the A/B test decided it: option 4, the
  wording.** Two driver drives on the box, seed 42, 30 rounds each at
  20 s, the same 10 events at the same rounds (the fork's runs
  `2026-09-25T22-34-16`, A, "Offstage: <event> …", and
  `2026-09-25T22-35-07`, B, "Something happens that the listeners
  cannot see: <event> The first to speak tells the listeners on air
  what is happening. …"; 63 lines each, none dropped). Round 1 rebuilt
  from the records and counted by the model server: 315 and 333 tokens,
  exactly what the server read for each (the requests identical but for
  the user message). A rough hint — the round's first line shares a
  content word with the event — gave A 4/10, B 8/10. The agent's reading
  as a listener: B clearly better in 5 (the laughing voice, the owl on
  the mast, the old forecast, the Newfoundland request, the child's
  voice), somewhat better in 3 (the silence, the flooding, the gate),
  equal in 2 (the fish, the warm shape), A never better; B's lines a
  little more descriptive, the script 5 % longer after 30 rounds (2879
  tokens against 2740). The owner (verbatim): "B wins, flip the default
  and record it." — `show.event_report`, on by default in the fork
  (`c55d25b`); `false` keeps "Offstage:". Still open: B names
  the event more often but not always fully (the burst pipe became
  "a swamp"; the single file became "coming through the gate"); if by
  ear (step 3.4) events still puzzle, option 3 (the operator reports,
  one extra round per event) is next. Seen on the wire: the system
  prompt says "No narration" — one more reason against option 1.

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
  also triggered if the [spec §9] engine comparison experiment
  finds the existing seven inadequate for 4 distinct character
  voices. *(Pointer corrected 2026-09-16: was "§8.4", a stale
  pre-spec number.)*
- **Fix shape:** implement a tts-serve server module per engine
  following the existing `impl/server_*.md` pattern
  (<https://github.com/scorbo2/tts-serve/tree/master/impl>);
  expose via the standard `/synthesize` + `/capabilities` API;
  F5-TTS first (known quantity), Breeze TTS 2 second (newer,
  unproven locally). Consider upstreaming as PRs to scorbo2.

## The sign-off "Over." sometimes runs into the line — keep the accumulator at 100; re-test with any new TTS engine

- **The gap:** listening to the `/show` page with voices (2026-09-25,
  slice 3's step 3.2), the owner heard a few lines — not many — where
  the voice said the closing "Over." without the pause after the
  sentence before it: "Daniel (sad): They're not coming. Over." sounded
  like "coming over". The engine: Faster Qwen3-TTS (tts-serve 1.2).
  Every line ends with "Over." (the cast sheet's rule), and the
  accumulator packs it into the line's last chunk.
- **The owner's idea:** lower the accumulator's length to about 20
  characters, so "Over." goes as a request of its own — not worth much
  time now; perhaps a new TTS engine fixes it.
- **The agent's view (2026-09-25): keep 100.** Measured the same day,
  each request costs 2.4-3.2 s almost whatever its length (the entry
  "Measure TTS synthesis time against text length"). At 20 characters,
  "Over." and most sentences become requests of their own: about twice
  the requests per line, and the silences inside rounds grow from 1-2 s
  to several seconds; very short requests also bring back the fragment
  artifacts the accumulator exists to avoid ("Testing. 1. 2. 3.").
  **The owner agreed**, from another case: "Could this be... a
  distraction? Over." is better said whole than cut at the "..." — the
  accumulator keeps it whole (verbatim): "Trying to fix where to cut sentences with different punctuations so that TTS pronunciation is better is too complicated. In practice I feel the accumulator is the practical best solution."
- **Cheaper options, for later:** (a) a pause cue in the spoken text
  before "Over." (an ellipsis, a comma), per engine, in the tables of
  the entry "Markdown emphasis in spoken lines"; test by ear. (b) One
  "Over." clip per persona, synthesized once per run and played after
  each line with a short pause, the text's "Over." left out of the
  request — four requests per run; the same "Over." every time, which
  suits radio protocol but not a line's mood. (c) Re-test with any new
  TTS engine (Task 5b).
- **Where flagged:** the owner, 2026-09-25, by ear, during step 3.2's
  check.
- **Trigger:** a TTS engine change; or the owner's ear asks for it
  before the talk.

## A line broken off with an em dash sounds and reads cut — the dash becomes a comma in the spoken text

- **The gap:** the model sometimes breaks a line off on purpose with an
  em dash, and the spoken text turns the dash into a comma, so the line
  sounds — and, in the captions, reads — as if it had been cut. Seen by
  the owner on the `/show` page, 2026-09-25 (slice 3's step 3.3 check;
  the fork's run `2026-09-25T17-50-50`, round 5, an answer round):
  - the model wrote (`debug/r005.txt`, the record's `raw`):
    `Moira (doubtful): "I don’t know. The samples were aerosolized, but—Over."`
    — `—` U+2014 between "but" and "Over"; `finish: stop`, 24 tokens of
    512, nothing cut;
  - the spoken text (the record's `spoken`, the `done` event, the
    caption): `I don't know. The samples were aerosolized, but, Over.`;
  - sent to the voice, one request (54 characters, one chunk):
    `{"text": "I don't know. The samples were aerosolized, but, Over.", "persona_name": "Moira"}`.
- **Why:** the parser's `_SPOKEN` table maps `—` to `, ` (the fork's
  `app/show/parser.py`), chosen on 2026-09-22 because the em dash
  dropped the pause before "Over." on Faster Qwen3-TTS (the TODO's
  Task 5b note). Right for a dash in mid-sentence ("the lab — or what is
  left of it — is…"); wrong for a dash that breaks a sentence off.
- **Options, for later:** (a) the captions show what the model wrote
  ("but—Over.", curly quotes and all) and only the voice gets the
  normalized text — the `done` event would carry a display text too (a
  small server change); (b) a dash that ends a clause (before "Over." or
  a capital letter) becomes `...` — trailing off — in the spoken text,
  a mid-sentence dash stays `, `: engine-dependent, to judge by ear, and
  close to the punctuation rabbit hole of [discussion 2026-09-25]
  show-slice-3-browser-plan §8.4. The owner declined a listening test
  of the three versions for now ("but, Over." · "but—Over." · "but...
  Over.") and asked for this note.
- **Where flagged:** the owner, 2026-09-25, reading the captions.
- **Trigger:** polish; or a TTS engine change (Task 5b), with the tables
  of the entry "Markdown emphasis in spoken lines".

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
- **Trigger:** any TTS engine change (Task 5b), or the real reference
  voices (Task 4's first part, the owner's, next): re-run the
  three-line test and listen.
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

## The trim's thresholds in settings — the 90 % trigger and the 50 % target are hard-coded (owner, 2026-09-28) — resolved 2026-10-01

- **Status 2026-10-01 — resolved; kept for its receipts.** In the fork's
  `f9aa73d` (alfre2v/TalkWithZombies#9, branch `alfre2v/context-32k`):
  `show.trim_trigger` (0.9), `show.trim_target` (0.5),
  `show.trim_keep_first` (2) and `show.trim_keep_last` (4) replace the
  four constants of `app/show/script.py`; the defaults are the old
  values; `ShowConfig` refuses a target at or above the trigger, and the
  bounds (both in 0-1, the kept rounds from 0). `trim()` reads them from
  the show's settings. The whole story — how the app counts the
  script's tokens and decides — in [discussion 2026-10-01]
  the-app-from-the-outside §2.

- **The gap:** the trim fires when the script reaches 90 % of
  `show.context_budget` and cuts whole rounds from the middle until it
  is back to 50 % — but those two numbers are constants in the fork's
  `app/show/script.py` (`_TRIGGER = 0.9`, `_TARGET = 0.5`, lines
  143-144; also `_KEEP_FIRST = 2`, `_KEEP_LAST = 4`, lines 141-142), against the rule
  that every number is a setting.
- **The owner (verbatim, 2026-09-28):** "I do agree we need to put
  trim thresholds in settings." Not wanted: trimming deeper ("No, I do
  not want to trim deeper, I want to keep as much context as
  possible.") nor leaner instructions ("these are working fine").
- **Where flagged:** the owner's listen of the installed `tz-0.2`
  client, 2026-09-28 (run `2026-09-28T15-31-44` in
  `~/TalkWithZombies-client/runs/`), while looking for a long gap.
- **Trigger:** with the budget follow-ups below, or any change to the
  trim.
- **Fix shape:** `show.trim_trigger` (0.9), `show.trim_target` (0.5)
  and the kept rounds at each end as settings, checked in
  `ShowConfig`'s validators (target below trigger, both in 0-1); the
  defaults unchanged.

## A context budget near the full 16k (owner, 2026-09-28) — overtaken 2026-10-01 by the 32k context

- **Status 2026-10-01 — overtaken; kept for its receipts.** The
  context went to 32,768 (below) and the budget with it: **34,000** in
  the fork's `f9aa73d` (alfre2v/TalkWithZombies#9). The room this
  entry asked to measure, measured: the largest round in 82 recorded
  runs (1,824 rounds) added **741 tokens** (an exchange, instruction
  and reply); the new `show.instruction_room` keeps 1,000 above the
  trigger, plus `show.max_tokens` (512) for the reply. Since the trim
  fires at 90 % of the budget, the budget may exceed the context:
  0.9 × 34,000 + 1,000 + 512 = 32,112 fits 32,768. A run now opens only
  if that fits the server's real context (llama.cpp's `/props`), with
  the arithmetic in the refusal. The confirming drive (run
  `2026-10-01T13-43-41`, 220 rounds): the largest request 30,694
  tokens, no overflow, one trim (before round 140). Details:
  [discussion 2026-10-01] the-app-from-the-outside §2.4-§2.6.

- **The gap:** `show.context_budget` is 14,000 against the server's
  16,384-token context (`zr_llama_ctx` in
  `deploy/ansible/inventories/common_vars.yml`), so the trim fires at
  12,600 tokens and cuts back to 7,000. Measured in the owner's listen
  of 2026-09-28 (run `2026-09-28T15-31-44`, 189 rounds, about 21
  minutes of audio): trims at rounds 79, 101, 133 and 169 — every 22-36
  rounds, not the "roughly 50 rounds" estimated on 2026-09-23 ([discussion
  2026-09-23] show-engine-design §2.2, at 16k and 125 tokens a round).
  Rounds average 165 tokens since step 3.4c: exchanges 508, last
  exchanges 425 (each restates the voice's earlier words, earlier
  callers' words and an agenda item), free rounds 70-90; contact rounds
  are 17 % of the rounds and more than half of the tokens. After each
  trim the server re-read the whole remaining script (4,369-6,580
  tokens; only 43 served from the cache — Nemotron is a hybrid model,
  and llama.cpp cannot keep the cached start when the middle changes).
  Replayed cold, round 169's 5,008-token request took 5.1 s of wall
  time (1.7 s of prompt reading; the rest server overhead, not yet
  explained) — close to the 2026-09-23 estimate of "around 5
  seconds". Three of the four trims fell in contact rounds, right after
  the listener spoke.
- **The owner (verbatim, 2026-09-28):** "I want to explore pushing the
  budget from 14k to near the full 16k."
- **Trigger:** the owner's call, after the timebox.
- **Fix shape:** the room a request needs above the budget — the
  reply (`show.max_tokens`, 512) plus the next instruction (an exchange
  instruction is about 500 tokens and grows with the restatement) plus
  a margin — measured on the heaviest rounds, then the budget raised
  to 16,384 minus that room; a long drive or listen to confirm no
  request overflows the server's context, and the trims counted.

## A 32k context, so the show forgets past callers less often (owner, 2026-09-28) — done 2026-10-01

- **Status 2026-10-01 — done; kept for its receipts.** `zr_llama_ctx`
  32768 (this repository's `a89d0fa`, alfre2v/zombie-radio#20),
  deployed on the box by the owner (`/props`: `n_ctx 32768`); the
  budget 34,000 in the fork (alfre2v/TalkWithZombies#9). Measured on
  the A6000: **the GPU memory** — llama-server 6,764 → 6,970 MiB when
  it started (the context is reserved upfront), 7,046 MiB after the
  first minute of use, then flat through a full context and a trim;
  the stack 14,195 → **14,477 MiB** (under the 16 GB wish and the 24 GB
  target). **The trims** — at 16k, every 22-36 rounds; at 32k, the
  first before round 114 (budget 31,000) or 140 (34,000), then roughly
  every 100 rounds (estimated): about 3-4 times rarer. **The pause of
  a trim** — 8.2-8.4 s (12,209-13,922 tokens re-read), against 5.1 s at
  16k: about 1.6 times, not the twice expected below. **The prompt
  reading per round** — served from the cache between trims (about 200
  tokens fresh, the rest cached; a round about 1.6 s, first line under
  1 s). **Not measured:** the model's quality deep into a long context
  — by ear, in the owner's next long listen. Details: [discussion
  2026-10-01] the-app-from-the-outside §2.6; how to measure the memory:
  `docs/runbooks/box-inspection.md`.

- **The gap:** at 16k, a long show trims every few minutes (above),
  and each trim drops the middle of the script — the contacts with
  earlier callers among it; the contact instructions still restate
  earlier callers' words, but the conversations themselves go.
- **The owner (verbatim, 2026-09-28):** "Separately I want to explore
  making the context 32k, so the model does not forget past user
  interactions so frequently."
- **Trigger:** the owner's call, after the timebox; independent of the
  16k budget follow-up above.
- **A data point:** on 2026-09-23 the A6000 box used 13.0 of 46 GB of
  GPU memory, and even 64k was believed cheap on this hybrid model — not
  measured ([discussion 2026-09-23] show-engine-design §2.4).
- **Fix shape:** `zr_llama_ctx` 32768 in
  `deploy/ansible/inventories/common_vars.yml` and a converge on the
  box; `show.context_budget` raised to match (and the trim's
  thresholds, once they are settings). To measure: the stack's memory
  against the 24 GB target (at 16k, with one voice engine, 14.0 of
  15.3 GiB on an A4000); the pause of a trim, since the whole remainder
  is re-read and would be about twice as long; the model's quality
  deep into a long context; the prompt reading per round as the script
  grows (mostly served from the cache between trims).

## Resume does not re-check the model server's context (owner, 2026-10-01) — low priority

- **The gap:** since 2026-10-01 (the fork's `f9aa73d`,
  alfre2v/TalkWithZombies#9) a run opens only if the show's budget fits
  the model server's context: `POST /api/show/start` asks llama.cpp's
  `/props` for `n_ctx` and refuses the run when `trim_trigger ×
  context_budget + instruction_room + max_tokens` does not fit
  ([discussion 2026-10-01] the-app-from-the-outside §2.4). **Resume does
  not go through `/start`:** it continues the same run — the page's
  `resumeShow()` calls `runShow()`, which goes straight back to
  `POST /api/show/round` — so the check is not made again.
- **When it matters:** only if the box is **redeployed with a smaller
  context while a show is paused** — for example, a target that needs
  `zr_llama_ctx` 16384 (a 3090 that cannot fit 32k, overridden in its
  `99-local.yml`) taking over mid-show. Then the first request larger
  than the new context fails with the model server's own error (not
  observed here), the page marks the round "(this round failed: …)",
  and every Resume fails the same way until the app is restarted with a
  smaller budget or the box gets a larger context. A mid-show redeploy is
  not a case the show meets today.
- **The owner (verbatim, 2026-10-01):** "I think (6) "Resume doesn't
  re-check the server's context" is low priority for us, we should
  document in follow ups but mark as low priority."
- **Where flagged:** the agent's answer to the owner's question whether
  `server_context()` is called once or periodically ([discussion
  2026-10-01] the-app-from-the-outside §2.4).
- **Trigger:** a target deployed with a smaller context than the others,
  or any change that makes the server's context vary during a show.
- **Fix shape:** the running app remembers which runs it has checked;
  a round for a run it has not checked (a Resume, or a run continued
  after the app restarted) checks `/props` first — or, simpler, every
  round checks it — one tiny request each
  (`server_context()` in the fork's `app/services/llm.py` and
  `context_problem()` in `app/routers/show.py` already exist); on a
  mismatch, the round fails with the same message as the start, instead
  of the model server's error.

## The settings API does not show the show's settings (owner, 2026-10-01) — after the demo

- **The gap:** `GET /api/settings` returns only `llm`, `tts`, `stt` and
  `general` (the fork's `SettingsResponse` in `app/models.py`) — **not
  `show:`**, and not `mcp:` either: both are "yaml-only" by design
  (`ShowConfig`'s docstring: "The show engine's settings — yaml-only,
  like mcp."). Found in the endpoint survey ([discussion 2026-10-01]
  the-app-from-the-outside §3.6), where the reply's `llm.max_tokens`
  (200, the chat's) could be mistaken for the show's (512).
- **What it costs:** nothing in the app can say which show settings a
  **running** app loaded — the budget and the trim's numbers, the seed,
  `debug`, `mood_voices`, `voice_seed`, the pacing. `settings.yaml` says
  what is in the file, which is not always what is running: the settings
  are read when the app starts, so an edit since then is not in effect
  (exactly the case of 2026-10-01, when a temporary budget of 40,000 was
  removed from the file while the running app still had it). Today the
  only views of the running values are partial: a run's start reply
  (`seed`, `debug`, `voice_seed`, the voices) and its record. FastAPI's
  `/docs` page cannot show them either, and TalkWithMe's settings page
  never shows them.
- **What is safe already:** saving from the chat's settings page
  (`PUT /api/settings`) keeps the `show:` section in `settings.yaml` —
  the fork's `tests/test_show_config.py`,
  `test_save_then_load_keeps_the_show_section`.
- **The owner (verbatim, 2026-10-01):** "(7) GET /api/settings doesn't
  show the show's settings" is more serious, but I do not mind to
  postpone it until after the demo day. But we should record it well!"
- **Trigger:** after the demo (2026-10-08); sooner if a test or a listen
  is misread because the running settings differ from the file.
- **Fix shape:** a read-only `show` section in `GET /api/settings`'s
  reply (and `mcp`, for completeness), or a separate
  `GET /api/show/settings` returning the running `ShowConfig` — readable
  with `curl` and on `/docs`; not editable through the API (the show's
  settings stay yaml-only, edited in the file and applied by a restart),
  so the chat's settings page and its `PUT` are untouched. Tests: the
  reply carries the loaded values, not the file's.

## A long silence between two lines of one round, not explained (owner, 2026-09-28)

- **What was seen:** in the owner's listen of the installed `tz-0.2`
  client (run `2026-09-28T15-31-44`), round 187, "a way too long gap"
  between the event's reading and the first model line — "[The canned
  peaches, the last luxury, have swollen lids.] Ralph (determined):
  The canned peaches, the last luxury, have swollen lids. Over. /
  Samantha (curious): Why are the peaches swollen? Over." No trim in
  that round (the last was round 169).
- **What was measured afterwards** (2026-09-28, through the tunnel):
  round 187's own request, rebuilt from the record and replayed —
  0.84 s in all (204 new prompt tokens read in 0.35 s, 8,530 from the
  cache, 15 tokens written); Samantha's line synthesized three times
  with her installed voice — 1.26-1.44 s; Ralph's line — 2.0 s to
  synthesize, about four seconds of audio. Both of Samantha's parts
  normally finish while Ralph's line plays: no gap expected.
- **Not known:** where the time went — the run records token counts,
  not clock times; the installed client had debug off; the server's
  log was not kept. The tunnel is a suspect (the follow-up "SSH
  keepalives and polling…"), not a finding.
- **Trigger:** the next listen with a long gap.
- **Fix shape:** listen with `debug: true` under `show:` in the
  client's `settings.yaml` (the page's line under each round shows the
  first line, the round and the first sound), or have the record keep
  llama.cpp's own `prompt_ms` and `predicted_ms` (the server returns
  them; the fork keeps only the token counts) — the owner's call.

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
  Pythons; our fix is TalkWithZombies commit `c46c3bf`. A fifth
  joined on 2026-09-25: (5) **the sentence splitter cuts inside
  numbers** — upstream's `extractSentences`
  (`/Users/alfredo/workspace/hackTNT_2026/TalkWithMe/static/tts.js:72`,
  regex `/[^.!?]*[.!?]+/g`) ends a sentence at any dot, so "Take 3.5
  milligrams every day. Over." becomes "Take 3." · "5 milligrams every
  day." · "Over." — whole or token by token — and each sentence goes
  as its own TTS request, the number split across two (run as is on
  2026-09-25; found by the owner's questions about the show's
  accumulator, [discussion 2026-09-25] show-slice-3-browser-plan §8).
  **No longer candidates:** the `[Name]:`
  output sanitizer (moot under [ADR-0003] — [spec §10]) and the
  `max_turns_for_context` raise (done in our config, 6 → 50, on
  2026-09-18 — a setting, not a patch).
- **Where flagged:** the remote-split spike (2026-09-16) designated
  the first patches; re-ranked 2026-09-21 ([discussion 2026-09-19]
  upstream-contribution-strategy, addendum; [discussion 2026-09-21]
  task6-reconnaissance-brief §1–§2; [ADR-0002]); (5) added 2026-09-25
  ([discussion 2026-09-25] show-slice-3-browser-plan §8).
- **Trigger:** after 2026-10-08 — outreach deferred past the
  deadline by the owner ("build offerable, contact nobody yet").
- **Fix shape:** (1) as a pull request or a README pointer to the
  deployment repo; (2) a focused pull request against upstream's
  `static/tts.js`, with the packing rules' Node tests as its proof
  (the fork's `tests/test_show_page.js`, step 3.2); (3) and (4) as GitHub issues with the receipts
  above, (4) with our commit as the proposed fix; (5) a small bugfix
  pull request of its own against `extractSentences`, apart from (2) —
  a pure fix is easier to accept: a sentence ends only where a run of
  marks meets whitespace, `(?=\s)` while streaming (the growing buffer
  ends at "Take 3." just before the "5" arrives, so its end is not a
  sentence end; the tail is flushed on `done`, as today) — simulated
  with upstream's loop: "Take 3.5 milligrams every day." · "Over." —
  with a Node test; our version, for whole lines, is the fork's
  `static/show/player.js` `sentencesOf` (step 3.2).

## LuxTTS landed upstream — presumptive candidate for the TTS comparison (Task 5b)

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
- **Trigger:** the TTS comparison's scoping (Task 5b; the spec's §9,
  "The voices" — it was §7.2 before the spec's rewrite of 2026-09-28) —
  LuxTTS enters the candidate pool automatically (it is now a
  wrapped engine) and its VRAM/RTF claims are exactly what Task 5b
  measures. Its Apache-2.0 weights also weaken the case for the
  Breeze TTS 2 soft-goal addition (non-commercial weights, same
  lightweight niche) — re-evaluate that entry when this trigger
  fires.
- **Fix shape:** nothing to build — include in Task 5b's harness;
  verify the VRAM claim first (it's the cheapest check and the
  biggest prize).

## Mood clips — several reference clips per character, one per mood (owner, 2026-09-28)

- **Status 2026-09-30 — the shape is agreed, and it supersedes the one
  below:** the clips are named after what was recorded (`ref-fear.wav`,
  not `ref-afraid.wav`), the story declares the complete mood → clip map
  (`voices` in `overtones.yaml`), the page names the clip, and the voice
  route falls back only to `ref.wav` ([discussion 2026-09-29]
  voice-datasets-with-emotion §11.8). The design below is kept as history.

- **The idea (the owner, verbatim, 2026-09-28):** "In the near future,
  I will want to have several audio clips per persona, difference on the
  mood... So `Moira-happy.way`, `Moira-urgent.wav`, `Moira-afraid.wav`
  ... I want to discuss how to change our code to implement this, but I
  do not want to execute yet." The naming, ruled the same day:
  "ref-afraid.wav next to ref.wav, record the shape as a follow-up."
- **Already decided** ([discussion 2026-09-26] show-director-modes §11,
  the owner, verbatim): "In the end the mood provided by the grammar
  will have to be the signal carried around until the moment we send the
  text to TTS, so we can decide what reference audio to send, and there
  will have to be a different mapping to decide mood -> audio file, as I
  will never manage to get it one to one." tts-serve needs no change:
  every synthesis request carries its own reference clip, cached by its
  content, so switching clips per line costs nothing extra; the emotion
  lives in the clip ([discussion 2026-09-21] task6-recon-tts-serve, F3
  and Q2).
- **Where the mood stops today** (checked 2026-09-28 in the fork, at
  `tz-0.2`): the parser sends each line's mood with its start event; the
  page reads it (`static/show/show.js:252`) and shows it in the caption;
  `speakLine(persona, text, hooks)` (`static/show/player.js:111`) posts
  only `{text, persona_name}` to `/api/tts` (line 190); `TTSRequest`
  (`app/models.py:56`) has no mood; the route loads the persona's one
  `ref.wav` and `ref.txt`.
- **The shape:**
  1. **Files** — in each persona folder, `ref.wav` and `ref.txt` stay
     the default voice; mood clips sit next to them as
     `ref-<mood>.wav` with their exact transcript in `ref-<mood>.txt`
     (e.g. `Personas/Moira/ref-afraid.wav`, `ref-afraid.txt`), `<mood>`
     one of the story's fourteen. Any subset per character; clips can
     arrive one at a time.
  2. **The mapping, with fallbacks** — for a line in mood M: the
     character's `ref-M` clip if it exists; else the clip of the mood M
     falls back to (e.g. terrified → afraid, relieved → happy), then
     that mood's own fallback; else the default `ref.wav`. The
     mood-to-mood fallback belongs to the story (the moods are the
     story's, `overtones.yaml`); the clips belong to the personas.
     **Where the clips come from (2026-09-29):** a casting script copies
     the chosen EARS clips into each persona folder, driven by a mapping
     file — the cast, the clip for `ref.wav`, and each show mood's EARS
     emotion, drafted with a confidence per mood ([discussion 2026-09-29]
     voice-datasets-with-emotion §11.3, option A; the owner's ruling:
     "go with A").
  3. **The page sends the mood** — `speakLine(persona, text, mood)`
     posts `{text, persona_name, mood}`; the voice queue already cuts
     chunks at each line's end, so a chunk always has one mood.
  4. **The TTS route picks the clip** — `TTSRequest` gains an optional
     `mood`; the route resolves the clip and its transcript for the
     persona and mood, with the fallbacks; without a mood, today's
     behavior (upstream's chat UI unaffected).
- **Risks** (§11 of the 3.4c discussion, plus): how much of a clip's
  emotion carries into the cloned voice with Faster Qwen3-TTS is
  unmeasured — test it as soon as one character has two clips; clips
  from different speakers or recordings would make one character sound
  like two people; clips at different loudness would make the voice jump
  (normalize when preparing them).
- **Where it sits:** Task 5b's "mood → clip map per character"; needs
  the reference voices (Task 4, part 2) first.
- **Trigger:** the owner's call, after the default clips are in place.
- **Estimate:** 2-3 hours for the four pieces with tests (the agent's,
  not measured).

## Compressed reference clips, switchable on and off — MP3 or Ogg/Opus instead of WAV (owner, 2026-09-30) — re-examine before demo day

- **The ask (the owner, verbatim, 2026-09-30):** "what I do want out of
  this is a clear follow up task to remind me to execute on the option (can
  be switched on/off) to provide ogg/mp3 compression for our audio samples,
  to be re-examined before the demo day (possibly)."
- **Why it may matter:** the app sends each character's reference clip,
  base64-encoded, with **every** synthesis request, and a line can take two
  or three requests. The EARS clips are WAV, 439-562 KB — about 590-750 KB
  per request. On the owner's connection that cost is lost in a fixed
  ~0.5 s per request, but on a slow uplink — a crowded venue's Wi-Fi on demo
  day — it could add a second or more to every request. Compressed, the same
  clip is 6 to 12 times smaller.
- **What is already known** ([discussion 2026-09-29]
  voice-datasets-with-emotion §11.7, measured 2026-09-30 on the A6000):
  tts-serve's Faster Qwen3-TTS accepts WAV, FLAC, MP3 and Ogg/Opus
  references (all eight tts-serve engines declare them; proven only on this
  one); Moira's 482 KB WAV became FLAC 221 KB, MP3 64 kbps 80 KB, Opus
  48 kbps 57 KB, Opus 32 kbps 38 KB; the synthesis time did not change; and
  the owner's listening test found **no audible degradation** in the cloned
  voice ("The quick quality voice test is successful, I do not notice any
  voice degradation."). Encoding on the Mac: Homebrew's `ffmpeg`
  (`libmp3lame`, `libopus`; no Vorbis encoder, so "ogg" means Opus).
- **Where flagged:** the owner's first show with the EARS voices,
  2026-09-30, hearing a bit more delay between lines (§11.7 of the
  discussion — the delay itself is not explained by the clip's size).
- **Trigger:** **before demo day** — the owner's call, ideally once the
  venue's network is known: if its uplink is slow (a speed test on the
  laptop at the venue, or on the fallback hotspot), switch it on.
- **The fix shape — a switch in one place, off by default:**
  1. **The switch:** one line in `tools/voices/cast.yaml`, e.g.
     `reference_format: wav` (or `mp3`, `ogg`), with the bitrate beside it
     (`reference_kbps: 48`); switching it on or off is that line plus a
     recast (`uv run python tools/voices/cast_voices.py`).
  2. **The casting script** encodes accordingly — WAV as today (`afconvert`),
     MP3 or Ogg/Opus with `ffmpeg` — writes `ref.<ext>`, and removes any
     other `ref.wav` / `ref.mp3` / `ref.ogg`, so a character only ever has
     one reference (and `ref.source` records the format).
  3. **The fork** looks for the reference as `ref.wav`, `ref.mp3`, `ref.ogg`
     or `ref.flac`, whichever exists — today it reads a fixed `ref.wav`
     (`app/services/persona_store.py`, `REFERENCE_AUDIO_FILENAME`, the scan
     at line 291), and the Personas editor's upload and the legacy migration
     accept only `.wav` (`app/routers/personas.py:113`,
     `persona_store.py:807`); the TTS route passes the bytes through
     unchanged (`encode_reference_audio` only base64-encodes them). Tests in
     the fork's style; the placeholder voices keep working (WAV).
  4. **Verify:** a recast in each format and one show line per format by
     ear; a request timed on a throttled or slow link to confirm the gain.
- **Alternative, not preferred:** the app itself encoding `ref.wav` to Opus
  when it loads it (a setting in the fork) — it would need an audio encoder
  inside the app, where the casting script already has one.
- **Estimate:** about 1-2 hours in the fork plus 30 minutes in the casting
  script, with tests (the agent's, not measured).

## A cloned line came out badly degraded, once — Samantha, in the first show with mood voices (owner, 2026-09-30) — postponed

- **Status 2026-09-30, evening — suspect 1 confirmed, and screened for.** The
  owner heard Daniel's voice drift feminine on "Daniel (terrified): That
  figure, it's not human. Over." (the fork's run `2026-09-30T16-47-31`, round
  45, mood terrified → `ref-distress.wav`, from p007 — the right clip was
  sent), and found the cause by listening (verbatim): "the audio of Daniel's
  `ref-distress.wav` have an artifact in the beginning, the voice actor said
  something in low voice just before reading the transcript." Whisper heard
  it: "*can just eat all of them.* Oh God, I'm not sure…" — words the
  transcript does not have. p007's negative recordings also pitch into a
  woman's range (median, by a rough standard-library estimate: neutral 133
  Hz; fear 235, anger 211, distress 190 — Moira's neutral voice is 195-200).
  The owner (verbatim): "I think we need to replace Daniel."
  **The screening** (2026-09-30, 17:09-17:12 CDT, on the owner's go): for 14
  speakers — the ten other men of the shortlist, the current cast (p026,
  p017, p063) and p007 as the control — each of the 13 recordings the story
  uses was transcribed by the box's Whisper (`/v1/audio/transcriptions`, no
  voice-activity filter, language en) and compared word by word with its
  transcript, and the neutral and four negative recordings were
  pitch-estimated (autocorrelation, 50 ms frames, voiced frames only) — 182
  requests, from the downloaded originals converted to 16 kHz. The control
  was flagged (6 extra words at the start), as it must be. **Stray speech
  found:** p007 distress ("can just eat all of them."), **p017 (Ralph)
  confusion** ("Appreciate it" — Ralph's *doubtful* lines), **p063
  (Samantha) pride** ("I'm amazed." — Samantha's *determined* lines), p046
  confusion (its first sentence read twice), p101 realization (a different,
  longer passage). Every other flag was a false alarm — "I'm" heard as "I
  am" at the start of anger and relief. EARS speakers also paraphrase a
  little ("too many shrimp" read "so much shrimp"). **Men whose negative
  recordings stay low** (highest negative median): p054 118 Hz, p088 131,
  p085 133 — and no stray speech; the rest reach 167-222 Hz. **Still to
  decide:** Daniel's new speaker (the owner's pick; p054 sits as low as
  Ralph's p017, 89 Hz neutral); and the two cast clips with stray speech —
  the simplest fix is to correct their transcripts to what was said.
  **The method is the fix for suspect 1:** screen a speaker before casting
  them — now the tool `tools/voices/screen_voices.py` (the runbook
  `docs/runbooks/cast-voices.md`, step 4b; [discussion 2026-09-29]
  voice-datasets-with-emotion §11.12). **Done the same evening:** Daniel
  recast with p085 (the owner's pick); the two transcript fixes wait for the
  owner to confirm the flags by ear.

- **What was heard:** the owner's first listen to the mood voices
  (2026-09-30, the fork's `alfre2v/mood-clips` on the dev server, run
  `2026-09-30T15-23-48` in the fork's `runs/`, 31 rounds, 19 lines by
  Samantha): "It works! However, there was one instance of severe voice
  degradation with Samantha's voice. Her is the more plain voice, I think,
  the other are more vibrant." Which line is not known — the owner: "I do
  not remember the exact line that had the problem."
- **Checked, and ruled out:** that her reference clips are too long (the
  owner's first guess). Across all 24 clips, Samantha (EARS p033): 7.3-16.0
  s, median 11.6 s; Daniel 6.3-15.8 s (median 10.4), Moira 8.1-16.6 s
  (10.9), Ralph 6.4-16.2 s (11.5); the nine clips she used in that run are
  within the others' range each.
- **The suspects, most likely first** (the agent's reasoning, not measured):
  1. **A clip whose transcript does not match what was said** — the voice
     engine clones from the clip and its exact transcript together; EARS's
     transcripts are the sentences the speakers were asked to read, so a
     changed word, a laugh or a restart in one recording would mislead the
     engine for that mood's lines only;
  2. **a very short line** ("Do you have any of those? Over.") — ultra-short
     inputs have glitched before (the "1." echo, the TODO's Task 5b notes);
  3. **the engine's randomness** — it samples, so a line can come out
     garbled once and fine the next time;
  4. **her loudness boost** — p033 recorded the quietest of the four (-41
     dBFS RMS), raised about 21 dB to -20, the most of anyone, which also
     raises any background hiss — more likely to affect her whole voice than
     one line.
- **Why postponed:** the owner (verbatim): "Let's postpone investigations
  in this direction, as it is not clear to me we would have a good remedy
  for it. At the moment it seems to be a sparse problem. My first try would
  be to replace Samanthat's voice by another more vibrant one. She seems to
  be falling asleep."
- **Trigger:** it happens again — **note the line's text, or the round's
  number from the debug line**, whose "voices" names the clip that spoke.
- **The two quick tests, then:**
  1. **The transcripts, checked by Whisper:** transcribe each character's
     `ref*.wav` with the box's Whisper (`localhost:8002` through the tunnel)
     and compare with its `.txt` — 24 short requests per character; a
     mismatch points at suspect 1, and the fix is that clip's transcript
     corrected by hand or the mood remapped in the story.
  2. **The line replayed:** the same text, sent to `/synthesize` three times
     with the clip that spoke and once with `ref.wav` (the measurement
     script of [discussion 2026-09-29] voice-datasets-with-emotion §11.7 is
     the pattern) — the same degradation every time points at the clip,
     once only at randomness.

## Recast Daniel and Moira, and correct two stray-speech transcripts (owner, 2026-09-30) — postponed past the demo

- **The statement:** three voice chores are left from the casting, and
  the owner postponed them all on the evening of 2026-09-30, after the
  live checks of the voices kept in debug mode (verbatim):
  "I can live with the audio instabilities for the moment. I wan to make progress in other areas. We postpone recasting more voices, as far as I am concerned we have achieved TTS of voices with emotions with great success. The remaining boring "find and clear the audio samples" do not interest me for the demo."
  1. **Daniel (p007)** — two of his clips spoil his lines: his *afraid*
     clip (`ref-fear.wav`, EARS p007 fear) is pitched in a woman's range
     (246 Hz), and lines cloned from it land anywhere from a man's voice
     to a woman's depending on the seed (107-235 Hz over four seeds); his
     *determined* clip (`ref-pride.wav`, p007 pride) has stray words at
     its start, which the screening tool missed. The live show will now
     and then give Daniel a woman's voice on those two moods — accepted.
  2. **Moira (p026)** sounds too like the new Samantha (p063) (the owner,
     §11.11). Candidates named then: p062, p059, p106, p033.
  3. **Two transcripts with stray speech** in the current cast: Ralph's
     *doubtful* clip (p017 confusion, "Appreciate it" before) and
     Samantha's *determined* clip (p063 pride, "I'm amazed." before) — to
     correct after the owner's ear check of
     `zombie-radio-datasets/ears/stray-speech-2026-09-30.html`, with the
     convention of §11.13 (`.txt.original`, `.CORRECTION.txt`, a line in
     the datasets' `README.txt`).
- **Where flagged:** [discussion 2026-09-29] voice-datasets-with-emotion
  §11.11-§11.14; the follow-up "Keep every synthesized chunk in debug
  mode…" (the live runs that found Daniel's two clips).
- **Trigger:** after the demo (2026-10-08), or a bad voice the owner
  will not accept in a recording. For the canned episode (Task 7) a
  recast is not needed: record with `show.debug` on, and say any bad
  line again with the fork's `scripts/replay_chunk.py --seed N` until it
  sounds right.
- **The fix shape:** screen the candidates (`python3
  tools/voices/screen_voices.py --speakers 62,59,106`), listen to every
  emotion the story's `voices` use, the negative ones above all (the
  screening misses quiet stray speech: the ear stays the last check);
  change a line of `tools/voices/cast.yaml` and run `uv run python
  tools/voices/cast_voices.py --all-emotions --only <Name>`; the runbook
  `docs/runbooks/cast-voices.md`.

## Keep every synthesized chunk in debug mode, and send a seed with every voice request (owner, 2026-09-30) — built (the fork's `799d005`, alfre2v/TalkWithZombies#8)

- **The gap:** the voice server's audio for each chunk goes to the page,
  plays, and is forgotten — debug mode keeps only the model's side
  (`runs/<run-id>/debug/rNNN.txt`, `.request.json`). When a line goes wrong
  (Daniel's "Candles!" in a woman's voice, 2026-09-30, run
  `2026-09-30T17-28-18` round 9), the audio heard is gone. And the app sends
  the voice server **no seed**, so every synthesis is random and a bad line
  cannot be reproduced.
- **The owner's question (verbatim):** "What do we do with the received
  audios for each round in debug mode. We should save them so we can trace
  back this problems." **Decisions (verbatim):** "yes to 1 and 2, seed
  always; record the follow-up. But do not execute yet".
- **The shape agreed:**
  1. **In debug mode, keep every chunk with its round** —
     `runs/<run-id>/debug/audio/r009-l2-c1-Daniel-ref-extasy.wav` (round,
     line, chunk, persona, clip used) and a `.json` beside it: the text
     sent, the persona, the clip asked for and the clip used, the voice
     server's `time_used`, the seed. How: with debug on, the page tags each
     voice request (e.g. `debug: "2026-09-30T17-28-18/r009-l2-c1"`); the
     voice route checks the tag strictly (the run id's own pattern, numbers
     only — nothing that can name another folder) and writes the audio it
     returns into that run's `debug/audio/`. Debug off, or TalkWithMe's chat
     UI (no tag): nothing changes. About 35-45 MB per 50-round run, in
     `runs/` (gitignored).
  2. **A seed with every voice request, always** — derived from the run's
     seed and the chunk's position (round, line, chunk), recorded in the
     `.json`; tts-serve's Faster Qwen3-TTS accepts `seed`. Any saved line can
     then be replayed exactly (same clip, text and seed → the same audio),
     and a run with a pinned seed reproduces its voices, not only its words.
  3. Optional: a link from the debug line to the round's audio folder.
- **Where it sits:** the fork (TalkWithZombies): `static/show/player.js`
  and `show.js` (the tag, the seed), `app/models.py` (`TTSRequest`: `debug`,
  `seed`), `app/routers/tts.py` (the save, the seed passed to
  `synthesize`), tests; the runbook `docs/runbooks/show-page.md`. About 1.5-2
  hours with tests (the agent's estimate).
- **Status 2026-09-30, 18:10 — the go is given** (the owner: "Ok, we are
  going to build that feature", after the voices became unstable and the
  engine was shown healthy — byte-identical to its 13:00 reply for the same
  clip, text and seed). Found since: tts-serve picks a random seed in
  **1..1000** per request when none is sent, and **echoes the seed** in its
  reply — record the echoed one; a derived seed must stay within 1..1000.
  Every line's stream events already carry `message_id =
  "<run-id>-r<NNN>-l<L>"` (the fork's `app/routers/show.py:227`), so the page
  knows the round and line when it requests the voice. The build spec:
  `docs/discussions/2026-09-30-show-engine-session-handoff-8.md` §13.3.
- **Trigger:** the owner's go — "do not execute yet" (2026-09-30, before a
  context compaction). Related: the replay test proposed for "Candles!" (the
  line sent 4 times with Daniel's clip and once with Samantha's) — not run;
  with this built, the next incident arrives with its own evidence.
- **Status 2026-09-30, 19:42 — built and checked live; the seed is a
  switch, off by default.** In the fork, `799d005` on
  `alfre2v/mood-clips` (alfre2v/TalkWithZombies#8):
  1. **Debug keeps every chunk, as shaped.** With `show.debug` on, the
     page tags each chunk's voice request with its run and place
     (`debug: "<run-id>/r009-l2-c1"`, the place read from the line's
     `message_id`), and the voice route keeps it in
     `runs/<run-id>/debug/audio/`: `r009-l2-c1-Daniel-ref-fear.wav` (the
     audio as the engine returned it) and a `.json` (the text, the
     persona, the language, the clip asked for and used, the clip's file,
     SHA-256 and transcript, `seed_asked`, the engine's reply without the
     audio: the seed it used, `time_used`, the sample rate). The tag is
     checked strictly (the run id's pattern, now one definition in the
     fork's `app/show/script.py`, and a run folder that exists); debug
     off or no tag keeps nothing, with the same single request per chunk
     (the owner asked for that check — "I want you to double check that
     when debug is off, we are not doing unnecessary round trips of
     requests" — and the live runs below confirm it). The audio is 48 KB
     per second of speech; a 50-round run keeps an estimated 35-45 MB.
  2. **The seed — changed from "always" to a switch.** A seed per chunk
     (from the run's seed and the chunk's place) was built first; the
     owner (verbatim): "I want to have a way to switch ON/OFF this TTS
     seed that you are sending now, in case it proof to add to the
     instability of the voices... I am not 100% percent sure that the
     strategy you picked to rotate the seed, and when to keep it the same
     is correct. And less if this strategy will prove correct for other
     TTS engines which we may support in the future." Then, once a replay
     showed the engine's echoed seed is enough to say any kept chunk
     again: "Ok, so then, all this new functionality you created when
     voice_seed is not off is wrong, no? [...] I do not see how is any of
     the other strategies you made to rotate the seed is going to be
     helpful." The agent agreed that no seed strategy steadies a voice —
     a seed makes it reproducible (the same clip, text and seed give the
     same audio, byte for byte, a bad chunk as much as a good one) — and
     proposed one seed per run; the owner: "on/off with the run's seed,
     go ahead." **`show.voice_seed`** (off by default): on, every chunk
     is asked for with the run's seed, so with `show.seed` set a run is
     said the same way twice, voice included; off, none is sent, as
     before. The app fits the seed into the range the engine advertises
     for `seed` (`fit_seed` in the fork's `app/services/tts_client.py`:
     kept within the range, wrapped around outside — 4000000001 becomes 1
     in Faster Qwen3-TTS's 1..1000), and sends none to an engine that
     advertises no `seed`; a request's seed wins over a `seed` in
     `tts.parameters`.
  3. **Replay:** `scripts/replay_chunk.py` in the fork says a kept chunk
     again through the app's `/api/tts` (the seed the page sent, or the
     one the engine said it used; `--seed N` tries another) and tells
     whether it is byte-identical. The link from the debug line (item 3
     of the shape) was not built.

  **Checked live** on the dev server, the owner playing in Chrome:

  | Run | Settings | Result |
  |---|---|---|
  | `2026-09-30T18-51-36` | debug on, requests sent by the agent | a tagged chunk kept, an untagged one not; 4000000001 reached the engine as 1; both kept chunks replayed byte-identical |
  | `2026-09-30T19-08-07` | debug on, seed off | 7 rounds, 15 lines: 16 chunks kept for 16 `POST /api/tts`, every line's text and speaker matching `script.json`; 16 different seeds picked by the engine |
  | `2026-09-30T19-20-04` | debug on, seed on | 17 rounds, 37 lines: 39 chunks kept for 39 requests; every chunk asked for the run's seed (1696878277), and the engine used 277 on all 39 |
  | `2026-09-30T19-32-32` | debug off, seed off — the demo's configuration | 19 rounds, 49 lines, a full contact: only `script.json` written, no `debug/` folder; 50 requests for the 50 chunks the page's `chunks()` gives; the owner: "it sounded normal, very well actually" |

  With debug and the seed both off, the voice seeds are not kept anywhere
  (the run's own seed always is, in `script.json`): a bad line in such a
  run cannot be said again exactly. **Not shown live yet:** a whole show
  said twice byte-identical with `show.seed` and `voice_seed` on — to do
  when it is needed (Task 7, the canned episode). What the kept chunks
  found at once — Daniel's two bad lines, both his clips' doing — is in
  [discussion 2026-09-29] voice-datasets-with-emotion §11.13. **For Task 7**
  (the agent's suggestion): record the canned episode with debug on, and
  say again any line that comes out wrong with `replay_chunk.py --seed N`
  until it sounds right.

## The three dropped page designs — kept in the fork's history, not in its tree (owner, 2026-09-28)

- **The statement:** five looks for the show page were drawn as
  mock-ups on 2026-09-28 (the fork's `alfre2v/radio-look`, commit
  `8624662`, "Five show page designs as mock-ups"): the owner's two,
  `old-radio` and `amateur-radio-transmitter`, and three of the
  agent's — `broadcast-studio` (a 1940s station's control room: an
  ON AIR light box, a console with a VU meter per character, the
  transcript as a typed script on a clipboard), `lab-terminal` (the
  lab's own early-1980s terminal: amber phosphor on a curved screen,
  the transcript as its log) and `field-radio` (a WWII backpack radio
  in olive drab, the transcript on a torn message pad, a handset
  beside the PRESS TO TALK button). The owner kept two (the
  owner, verbatim: "Ok, let's not get too carried away. I think one
  design with real photos is enough. I actually want to keep your
  `amateur-radio-transmitter` design. [...] Let's build these 2.");
  the other three were removed from the tree in `23472e5`.
- **Where flagged:** the TODO's polish item "The 1930s radio look,
  with the owner's gauge"; alfre2v/TalkWithZombies#5.
- **Trigger:** the owner wants another look — for the talk, for
  variety, or to replace one.
- **The fix shape:** bring a mock-up's folder back from `8624662`
  (`git show 8624662:static/show/designs/<name>/design.css`, and the
  same for its `design.js`), add a `design.yaml` (title, about, order)
  so the chooser lists it, and build it on the gauge the way the two
  kept looks are built (`static/show/gauge.js`: the `--level`
  variables and `onGaugeLevel`); the plain page stays untouched. The
  fork's `tests/test_routers_show.py` runs its checks on every look in
  the folder, and pins the list of looks and the chooser's order —
  add the new name to both. Mock-ups were drawn without the gauge or checks on small
  windows, so count a few hours per look (the agent's estimate).

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
- **Status 2026-09-28 — the place is settled, outside both
  repositories:** the clips go in `~/TalkWithZombies-client/Personas/<Name>/`
  as `ref.wav` with `ref.txt` (the TODO's Task 4); the fork gitignores
  `Personas/`, this repository never sees them, and the Mac installer
  never overwrites an existing persona folder. What is left of the
  fix shape below: the source clips and cleaned intermediates kept
  somewhere private too, and a note of the expected layout for a cold
  rebuild — the installer does not copy voices; they are placed by
  hand.
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
