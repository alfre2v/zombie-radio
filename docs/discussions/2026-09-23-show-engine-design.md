# Show engine design (Task 6b) — the seven decisions

**Date:** 2026-09-23 · **Arc:** MVP prototype · **Branch:**
`alfre2v/show-engine`
**Type:** discussion — the design of TalkWithZombies' show engine,
decided one question at a time before the code: the agent's agenda of
seven decisions (§1), then one section per decision as the owner
rules on it.
**Status:** OPEN — decisions 2 (the show's growing script) and 3
(where the show's record lives) ruled 2026-09-23; decisions 1 and 4–7
pending.

*Context for the cold reader.* [ADR-0003] (accepted 2026-09-23) fixes
the engine's shape: one shared script as the model's context (the
cast sheet as the system message, then alternating director
instructions and script lines), a director written in code, a GBNF
screenplay grammar on every request, and the browser `/show` page as
the clock. Task 6b in `docs/TODO.md` builds it in the fork
TalkWithZombies (`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`)
under a 3-day timebox — started 2026-09-23 at 14:46 CDT, checkpoint
2026-09-25 at 02:46, end 2026-09-26 at 14:46. The TODO lists the
pieces and their acceptance checks; this document decides how they
fit together. How one round's request carries the messages and the
grammar, the emotion switch, and the debug switch are explained in
[discussion 2026-09-22] grammar-and-prompt-cache-lessons §5.

*Conventions.* The verbatim blocks are the transcript's text: the
owner's messages quoted exactly as written, the agent's with their
headings demoted to fit this document; nothing removed. Sibling-clone
files with full absolute paths; this repository's files relative to
its root.

## 1. The agenda (the agent's proposal, 2026-09-23, verbatim)

### Item 3: the show engine

Here's an agenda: seven decisions, each with my pick. Attack any of them; then we go deeper one at a time.

1. **Build order and the checkpoint target.** I'd build the pieces that need no box first: grammar builder, parser, script assembler, director, all tested offline. Then by the checkpoint (morning of 09-25), a plain script drives **ten rounds on the box** through the real endpoint, with no browser. The browser comes after.
   - *Why:* the risk is in the engine, not the page. The checkpoint then judges the core mechanism with real numbers.
2. **Keep the whole script in the history for the timebox, with no trimming.** This is the big simplification, and I want your pushback on it.
   - *Why it's possible:* in the gate, the history grew by about 125 tokens per round. That makes about 120 rounds before the 16k context is full, roughly 40 minutes of show if a round is about 20 seconds of audio (an assumption, not a measurement).
   - A talk demo needs 5–15 minutes, so 120 rounds is enough. When a show nears the limit, the director ends the episode instead of cutting lines.
   - That makes trimming, and the open question about what editing the history costs on this hybrid model, **not needed for the timebox**. Both move to after it.
3. **Where the show's record lives.** Today each room stores a flat chat, `chatrooms/<room>/history.json`. The show needs rounds: the director's instruction, then lines with speaker, mood and text, plus any listener input.
   - I'd give each room its own show file, next to the existing chat, rather than bend the chat format.
   - The script assembler reads only that file.
4. **Where the cast sheet comes from.** The spec says the character bibles become its sections. I'd build it as a show preamble (one file: the setting, the format rules, the mood list when the switch is on) plus one section per persona, taken from the body of each `Personas/<Name>/prompt.md`.
   - Your bibles then slot in without code changes.
5. **What the first director decides**, kept deliberately small for the timebox:
   - who may speak this round (two or three names, with a fairness rule so no voice dominates);
   - how many lines (1 to 4);
   - one event from a yaml list of "radio traffic";
   - when to open the mic, by seconds of audio played, between a minimum and a maximum.

   Story shape (scaffolds, trajectories) belongs to the show arc, not here.
6. **The listener's turn.** Hold-to-talk records audio; Whisper turns it into text; the next round's instruction carries it as incoming radio traffic ("a voice on the frequency says: …"). Empty or placeholder transcripts are dropped, so a silent press changes nothing.
7. **Module layout and branch.**
   - An `app/show/` package with `grammar.py`, `parser.py`, `script.py` and `director.py`.
   - A new route file, `app/routers/show.py`.
   - `templates/show.html` and `static/show.js`.
   - Branch `alfre2v/show-engine` in the fork, the same name as this repo's docs branch.

Where do you want to start? I'd take #2 first, since it removes the most work and the most risk.

The owner chose to start with decision 2.

## 2. Decision 2 — the show's growing script

### 2.1 The owner's pushback (verbatim)

> Wow, this is a lot of information. this is going to take a long time.
>
> Ok, let's start with "2. Keep the whole script in the history for the timebox, with no trimming".
>
> Let me see if I understand: You are asking about the context trimming policy we will adopt, right?
>
> You main point seems to me: "A talk demo needs 5–15 minutes, so 120 rounds is enough. When a show nears the limit, the director ends the episode instead of cutting lines."
>
> This is certainly a possible way to address the problem of context grow.... however, may I point out it does not really solve the problem, because we have no guaranties that the limit won't be reached anyway (maybe the lines got longer for some reason)... Therefore I am not comfortable leaving this to "an estimate of how many minutes can the show runs"... And specially because trimming the context is no-brainer, at least in my primitive 2024 prototype I did the simple trick of when we reach a threshold  (say 90%) we remove lines in the midpoint of the dialog until the context size is back to 50% of the context window.   This is not so hard to impede progress to the MVP. Or am I missing something?
>
> Let's analyze quickly a few competing ways to solve this instead of sweeping it under the rug. Give me a brief list of 5 alternative ways you would solve the problem of the show's continuous context grow (you may include among them your lean: do nothing, it fits in our context).
>
> Side points: 
>
> * Nobody says we have to keep the max context at 16k, we have memory to go to 64k if we want to (I think, not verified)... This strengthen your proposal.
> * At some point I considered giving the show's narration some bigger arc structure, maybe harvesting more complex stories from a bigger commercial LLM and storing them, then using some of this stories as "episodes", setting the stage where the small LLM can improvise the dialogs. (I am not talking about many stories, nothing that would anger the commercial LLM providers, just a few stories we can reuse as scaffold to guide the petite nemotron)... I bring this up because, it's a bit related to the question of context management, if we decide to end each "episode" when the context window reaches some limit, we can start again a new episode with a new scene set for the LLM to improvise the dialogs... Say for example: first episode we describe they are just talking about the scarcity of supplies and discussing how to reach the lab's pharmacy, the episode finish with them agreeing to make a run for it... The next episode start anew with no dialogs, but a brief explanation of what happened before so the LLM can continue this episode with some connection to the previous one. What do you think about this? ... Sorry for my messy explanation, I hope you can understand.

### 2.2 The agent's answer (verbatim)

Yes, you understood it right: this is our policy for when the show's script outgrows the model's context. And your pushback holds. An estimate is not a guarantee, so a guard is needed whatever else we do, and trimming is not hard to write.

**What I was worried about.** Writing the trim is easy. Its cost on our stack is not a no-brainer, because of the prompt cache on this hybrid model:
- **How reuse works.** Every round, the server reuses what it already read up to the first place the new prompt differs.
- **What a trim does.** A cut in the middle changes everything after the cut, so the server has to read that part again.
- **Why a hybrid model makes it worse.** Nemotron's Mamba layers carry their memory of the text as a running state, which can only restart from a saved checkpoint. By default those are at least 8,192 tokens apart, so after a cut the server may have to re-read the whole prompt.
- **What that costs.** Today the server read a 687-token prompt at 0.61 ms per token. At that rate, re-reading about 8k tokens takes around 5 seconds. That's a rough, hand-computed estimate.
- **How often.** Trimming from 90 % down to 50 % of 16k frees about 6.5k tokens, which at 125 tokens per round is roughly 50 rounds between trims.

So a trim costs a pause of a few seconds about once every 50 rounds, and we can hide it inside the listening beat. It doesn't block the MVP. The open question shrinks from "what does an edit cost?" to "how long is the pause?", which is a ten-minute measurement on the box.

#### Five ways to handle a growing script

1. **Big enough, then stop** (my original lean, with a guard added): raise the server's context and have the director end the show at a hard limit.
   - Bounded for sure, but the show ends abruptly unless the ending is a planned episode ending.
2. **Midpoint trim** (your 2024 approach): at 90 %, remove whole rounds from the middle until the script is back to 50 %. The cast sheet, the opening rounds and the recent rounds stay.
   - Simple and bounded. It costs the pause above, and the model forgets the middle, so a character may repeat an old story.
3. **Sliding window:** keep only the last N rounds.
   - Simplest to write, but once full, the start of the prompt changes every round, so the cache breaks and the pause is paid **every round**. It also forgets the opening.
4. **Summarise the dropped part:** at the limit, replace the oldest rounds with a "story so far" paragraph, written by the model in an extra request or by the director from its own list of events.
   - It keeps what happened, at the price of an extra request. A 9B model's summaries may be unreliable.
5. **Episodes with a recap** (your idea): the show is a series of episodes. Each starts fresh with the cast sheet, a "previously on…" recap and a new scene. It ends at a story beat, or at a size limit as a backstop.
   - Resetting the history between episodes does the trim's job, and gives the story a shape.

**My recommendation: #2 as the safety net and #5 as the structure.** In the timebox:
- **The trim, built fully.** Whole rounds only, so the director-then-script alternation stays intact, with a unit test.
  - The size check needs no guessing: every llama.cpp response reports the exact prompt size (`usage.prompt_tokens`).
  - The limit is a yaml number of its own (`show.context_budget`), kept at or below the server's context. Setting it low, say 3,000 tokens, makes the trim fire early in tests on the box. That's also where we measure the pause.
- **Episodes, only the mechanism.** The director knows it's in an episode, with a scene setup and a recap, and one hand-written episode ships. Writing the stories is show-arc work.

#### Your side points

- **64k: yes, feasible.**
  - Right now the box uses 13.0 of 46 GB of GPU memory (llama.cpp 6.8 GB, the TTS 5.3 GB, Whisper 0.9 GB), so about 33 GB is free.
  - On a hybrid model only the few attention layers keep memory that grows with context; the Mamba layers' state is a fixed size. So 64k should be cheap, though I haven't measured it.
  - The model file declares a trained context of 1,048,576 tokens (the gate's `models.json`). I believe NVIDIA advertises 128k; either way it's well above 64k.

  I'd still keep 16k during the timebox, so the trim actually gets exercised, and raise it later if episodes need the room.
- **Your episodes idea is clear, and I think it's the right shape for the show.** It's the spec's "trajectory scaffolds" (§5.2, show arc) made concrete.
  - **Why it suits a 9B model:** the plot is authored in advance and the small model improvises the dialogue inside it. That plays to what it does well (local, in-character lines) and avoids what it does badly (long-range plot).
  - **Collecting a few outlines from a big commercial LLM** is ordinary use. We'd store them as files: scene setup, each character's goal, a few beats the director feeds in as events, and an ending condition such as "they agree to make a run for the pharmacy".
  - **The recap** would come from the episode file, written in advance, rather than from the model. That's reliable, and it gives the next episode a real link to the previous one.
  - **It helps the talk too:** clean start and stop points, and the canned episode (Task 7) becomes simply one recorded episode.

Do you adopt #2 plus the minimal #5, with the `show.context_budget` knob? Or would you rather change the mix?

A small aside: your tunnel dropped again. SSH to the box works, but `localhost:8080` doesn't answer.

### 2.3 The ruling

The owner, 2026-09-23 (verbatim):

> Now, back to your question: "Do you adopt #2 plus the minimal #5, with the show.context_budget knob".
> I say yes, but I think you are underestimating how complex the "minimal #5" can get... However, I am not too worried as once we add the Midpoint trim (2024 approach) we are in business even without reaching the "minimal #5".

- **Adopted:** option 2, the midpoint trim, as the always-on safety
  net; option 5, episodes, in its minimal form; and the
  `show.context_budget` knob.
- **The owner's caveat, agreed:** the minimal episodes may be more
  complex than the agent's estimate, and the trim alone already
  bounds the script — so episodes are not on the timebox's critical
  path. Where the complexity hides: deciding when an episode ends (a
  story beat is a judgment, not a counter); what the recap says and
  who writes it; what the director carries across episodes (who has
  spoken, which events were used, a listener's name); how episodes
  are stored in the show's record; and how the page shows the change.
- **Hence the order:** the trim first, built fully; episodes only
  after the trim works and the checkpoint is green, and then in the
  smallest form — one hand-written episode, its recap written in
  advance, its end triggered by the size limit or a round count, not
  by judging the story.

### 2.4 What it means for the build

- **The trim.** Before building a round, the director checks how full
  the script is, using the size the server reported for the last
  request (`usage.prompt_tokens` plus the tokens it generated) — no
  estimate. At 90 % of `show.context_budget` it removes **whole
  rounds** (a director instruction, its script lines, and any
  listener input it carried) from the middle, until the script is
  back to 50 %. It keeps the cast sheet, the opening rounds, and the
  most recent rounds; how many opening rounds to keep is settled in
  code. A unit test covers it.
- **The knob.** `show.context_budget` is a yaml number, kept at or
  below the server's context (16,384 tokens today). A low value
  (about 3,000) makes the trim fire within a few rounds, for tests on
  the box.
- **The pause.** A trim changes the prompt in the middle, so the
  server re-reads from the cut — possibly from the start, on this
  hybrid model. Measured once on the box with a low budget during
  6b. This reframes lessons §4.10 question 3: no longer a design
  blocker, only a number for the pacing (the pause can hide in the
  listening beat or under dead-air static).
- **The server's context stays 16k** through the timebox, so the trim
  is exercised for real. 64k is feasible (on 2026-09-23 the box used
  13.0 of 46 GB of GPU memory; believed cheap on a hybrid model, not
  measured) and is revisited if episodes need the room.
- **Episodes** — the minimal mechanism, after the trim, as a stretch.
  Authoring them (the owner's idea: a few story outlines harvested
  from a bigger LLM, stored as files — scene setup, each character's
  goal, beats the director feeds as events, an ending condition, a
  recap written in advance) is show-arc work.

## 3. Decision 3 — where the show's record lives

### 3.1 The owner's question (verbatim)

> Then let's pivot to "#3, where the show's record lives"
>
> Give me a brief recap of this point, but I think I like your "I'd give each room its own show file, next to the existing chat, rather than bend the chat format".
>
> Let me remind you, that we chose to create our own page(/view/controller?) for our show (instead of trying to bend the chat view of the app)... Maybe this contradicts a bit your previous statement, as in: why does each room needs its own show? Why not just one show, separated from the app chatrooms, which we will leave as an option, but not the meat of our "show"?

### 3.2 The agent's answer (verbatim)

**Recap of #3.** The show needs a record of its rounds, and three things read it:
1. **the script assembler**, which rebuilds the model's messages from it every round: cast sheet, then instruction, lines, instruction, lines…;
2. **the trim**, which removes whole rounds from it;
3. **people, later:** the debug flight recorder, the canned episode (Task 7 records a run so it can be replayed on demo day), and the talk itself.

The question is where that record lives and what shape it has.

**Where "per room" came from.** It's mine, from the story-loop discussion (09-21, Q6). There I recommended the separate `/show` page, which was adopted, and added one line: "The room concept still serves server-side: the show runs in a room and its script persists there like any chat." That was a **reuse argument, not a design need**. Rooms already name a group of personas and already have save code.

**You're right, and the reuse doesn't survive a closer look:**
- **The cast:** a room gives us a list of names, which one line of show config gives just as well.
- **Saving:** a room's `history.json` is a flat list of (sender, text). The show's record has rounds, instructions, moods and listener input. We'd write new save code anyway, or bend the chat format, which we already rejected.
- **What a room drags along:** its settings (who answers, echo chamber, max replies) mean nothing to the show. The chat UI could even open the show's room and write into it.

**So: one show, with its own home, and one refinement.** One show, but **each performance is its own run, in its own folder**, created when you press start. That buys:
- retakes and the canned episode for free, since a finished run is a recording;
- a natural place for the flight recorder's files;
- somewhere for episodes to live later (decision 2's stretch).

A sketch:
- **Config:** a `show:` section in `settings.yaml` holding the cast (persona names), `context_budget`, the emotion switch, `debug`, and the mic cadence. Voices still come from `Personas/<Name>/`.
- **Record:** `shows/<run-id>/`, gitignored like `chatrooms/`, with the run id a timestamp. Inside:
  - `script.json`, the rounds;
  - `debug/`, one file per round when the switch is on;
  - later, `audio/` for the canned episode.
- **`script.json`:**

  ```json
  {
    "run": "2026-09-24T10-15-03",
    "cast": ["Daniel", "Moira", "Ralph", "Samantha"],
    "rounds": [
      {"n": 1,
       "instruction": "Radio traffic: the generator coughed twice. Daniel, then Moira; two lines.",
       "listener": null,
       "lines": [{"speaker": "Daniel", "mood": "calm", "text": "Generator two is sulking again. Over."}],
       "trimmed": false}
    ]
  }
  ```

- **A useful consequence:** the trim becomes a **flag, not a deletion**. The assembler skips rounds marked `trimmed`, while the file keeps the complete show for replay and the record.
- **API:**
  - `POST /api/show/start` opens a new run;
  - `POST /api/show/round` plays the next round of the current run, with the listener's words when there are any.

  No room parameter, and one active run at a time, which the single server slot requires anyway.
- **Chat rooms stay untouched,** still a TalkWithMe feature. Just not at the same time as a show, on the same server.

Because this changes a point adopted on 09-21, the story-loop discussion gets a dated note, and the TODO's endpoint line (which says "takes the room") gets updated.

Do you adopt it: one show, a folder per run, the trim as a flag?

### 3.3 The ruling

The owner, 2026-09-23 (verbatim):

> Adopt it? I love it: one show, a folder per run, the trim as a flag.

- **Adopted:** one show, decoupled from the chat rooms; a folder per
  run; the trim as a flag.
- **What it supersedes:** the server-side half of the story-loop
  ruling of 2026-09-21 (Q6: "the show runs in a room and its script
  persists there like any chat"). The other half stands: the show
  runs on its own page, not a room flag ([ADR-0003] point 9). The
  story-loop discussion carries a dated note pointing here.

### 3.4 What it means for the build

- **Configuration:** a `show:` section in the app's `settings.yaml` —
  the cast (persona names; the voices still come from
  `Personas/<Name>/`), `context_budget` (decision 2), the emotion
  switch, `debug`, and the microphone cadence (minimum and maximum
  seconds of played audio, the listening window).
- **The record:** `shows/<run-id>/`, one folder per performance,
  created by a start action; the run id is the start time. The
  fork's `.gitignore` gains `shows/`, like upstream's `chatrooms/`.
  Inside:
  - `script.json` — the run id, the cast, and the rounds, each with
    its number, the director's instruction, the listener's words (or
    none), the lines (speaker, mood, text), and a `trimmed` flag;
  - `debug/` — one file per round while `show.debug` is on;
  - `audio/` — later, for the canned episode (Task 7).
- **The trim as a flag:** the trim marks whole rounds `trimmed`; the
  script assembler skips them; the file keeps the complete show, so a
  finished run is a full recording.
- **The API:** `POST /api/show/start` opens a new run;
  `POST /api/show/round` plays the next round of the current run,
  with the listener's words when there are any. No room parameter;
  one active run at a time (the single server slot requires it
  anyway).
- **The chat rooms stay untouched** — a TalkWithMe feature, used
  apart from the show (not against the same server at the same
  time).
- **Tests:** upstream's isolation fixture (`tests/conftest.py` in the
  fork) points every module-level global at per-test temporary state
  — the new root folder for `shows/` joins it (upstream's own rule
  for new globals).
- **Left to the code:** whether `mood` is absent or empty when the
  emotion switch is off.

## Update trail

- **2026-09-23** — Document created on the owner's request after
  decision 2 was argued: the agenda (§1) and decision 2 in full (§2)
  — the owner's pushback against leaving the script untrimmed, the
  agent's answer with five alternatives, and the ruling. Named for
  what it holds (all seven decisions, one section each) rather than
  as an agenda; a topic that grows into its own work spins off into
  its own document.
- **2026-09-23 (later)** — §3 added: decision 3, where the show's
  record lives — the owner's question (why per room, when the show
  has its own page?), the agent's answer, and the ruling: one show
  decoupled from the chat rooms, a folder per run, the trim as a
  flag; it supersedes the server-side half of the story-loop Q6
  ruling.
