# Show engine design (Task 6b) — the seven decisions

**Date:** 2026-09-23 · **Arc:** MVP prototype · **Branch:**
`alfre2v/show-engine`
**Type:** discussion — the design of TalkWithZombies' show engine,
decided one question at a time before the code: the agent's agenda of
seven decisions (§1), then one section per decision as the owner
rules on it.
**Status:** DECIDED — all seven decisions ruled on 2026-09-23 (in
the order 2, 3, 4, 5, 6, then 1 and 7 together); append-only from
here — reality reports back through dated addenda. The build is TODO
Task 6b.

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
  code. A unit test covers it. *[note 2026-09-23, measured on the
  box: a streamed reply carries no `usage` unless the request asks
  for it (`stream_options: {"include_usage": true}`), and then it
  arrives in an extra chunk with empty `choices`, which upstream's
  stream reader rejects. What llama.cpp sends by default is its own
  `timings` on the final ("stop") chunk: the prompt size is
  `timings.prompt_n + timings.cache_n` (4 + 303 = 307 in the probe —
  `prompt_n` alone counts only the tokens read fresh), and the script
  after the round adds `timings.predicted_n` (43 → 350). The trim
  reads those; `include_usage` stays unused, close to upstream — it
  would matter only if the show ever ran on a server other than
  llama.cpp.]*
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
- *[note 2026-09-23, decision 4: the run folder is renamed
  `runs/<run-id>/`, and the cast moves out of the `show:` settings
  into the story's front matter — §4.4.]*

## 4. Decision 4 — where the cast sheet comes from

### 4.1 The owner's opening question (verbatim)

> Them let's open "#4, where the cast sheet comes from".
>
> Let me start by saying I do not understand this "the character bibles become its sections".
> I think this was written in the style before we decided to adopt the 2024 style story prompt, instead of the TalkWithMe changing prompt for each persona.
>
> Ok, give me a more expanded explanation here.

### 4.2 The owner's follow-up: a template, and many files (verbatim)

> Ok, I think we are getting close. And you are right, I misinterpreted the word bible for the context of character play.
>
> I agree with you that the writing style of `Personas/<Name>/prompt.md` do not fit what we need for the show. I agree we need a separate file. And I feel that your recommendation "Hybrid: hand-written where a writer writes, generated where the grammar decides" is the right thing, so I am not pushing back, I just want to clarify my understanding...
>
> The example that you showed in "Our cast sheet is the same thing" is clear, this is what you refer as "the world and the portraits sit in one file you edit".  However, I do not know where in that example file we would place "The format-rules paragraph is written by code", the grammar I get it it can be written by code (or it can be a fixed string from a comment in the grammar file itself, we won't have so many grammars that we need to compose programmatically a description for each). 
> In any case, I would expect to see a placeholder for inserting this text in the human readable file (possibly a jinja var to substitute) so we can see the place where these generated text will be inserted and make the whole file a template of sorts.
>
> So, I guess what I am asking is, show me an example of how this file would look like, and if you agree to make it a template of sorts with  jinja (or other templating lang) placeholders to mark where inserted section go.
>
> ### Another angle: how to handle multiple files (for starting different shows)
>
> Then, another angle that you might not have considered: We may need not just one file, but many such files, for example we may want to have many show stories templates, so we can start different stories by pointing at a different file... And that entangles with the idea of running multiple episodes in a single show (as we discussed before)... So we need to give another thought to the multiplicity factor in these files.

### 4.3 The agent's answer (the two answers, condensed into one)

*Editorial note.* The owner asked for the two answers of this
exchange to be condensed into one entry without losing clarity. The
text below keeps every example and receipt of the two; it is not
verbatim.

#### "Bible" and "sections" — the 2024 style, not before it

The phrase comes from [ADR-0003] decision point 1, drafted on
2026-09-21 in the same breath as the switch away from TalkWithMe's
one-prompt-per-persona: "`system` = the cast sheet (one section per
character, the bibles) plus the show's rules and format". So it
describes the 2024 style. The confusion was the jargon:

- A **character bible** is a writer's term for everything known about
  a character — role, age, personality, quirks, how they talk, what
  they want, what they hide, who they clash with. The owner action
  queue asks the owner to write one per scientist ("rough is fine").
- **"Become its sections"** means only this: each bible, condensed to
  a short paragraph, replaces that character's one-line entry in the
  cast sheet.

The owner's 2024 prototype already had a cast sheet
(`/Users/alfredo/workspace/hackTNT_2026/zombie_radio_ai/zradio_local/zradio_local.py`):
one prompt for the whole play (lines 511–539) — the setting, the
rules of the game (`"Character Name: Dialog Line."`), the Narrator —
with the four characters enumerated inside it
(`__enumerated_characters_description__`), each filled from a small
record (lines 470–509):

```python
'name': 'Dr. Hanna Brie', 'gender': 'female', 'emotion': 'fearful',
'description': "A woman in her late 30s, research biologist specialized in exotic viruses.",
'ref_audio_orig': ..., 'ref_text': ...   # the voice clip, used only by the TTS
```

Our cast sheet is the same thing. The system message run 2 sent
(`CAST_SHEET_TAUGHT` in
`docs/experiments/2026-09-22-emotion-grammar-cost/cast.py`) has three
parts: **the world** ("You write a live radio play. Four scientists
are trapped…"), **the cast** (one entry per character, one-line
placeholders today), and **the format rules** (the line shape and,
with the switch on, the mood list). The bibles land in the second
part — the 2024 `description` field, richer.

What we left behind is TalkWithMe's style: each persona has its own
prompt file (`Personas/Moira/prompt.md`: `/no_think You are Dr. Moira
Byrne … End each transmission with "Over."`), and each request sends
one of them — the model plays one character at a time and never sees
the others. In the show, one request writes lines for any of the
four, so the model needs all four portraits in one system message.

#### Where the text lives: three options, the hybrid chosen

1. **Assembled from the persona files** — rejected: those bodies are
   written TalkWithMe-style (second person, one character, format
   rules inside); side by side they would tell one model "You are
   Daniel… You are Moira…". And after decision 3, the reuse argument
   fails the same way the room did.
2. **One hand-written file**, world, cast and rules together — simple,
   but hand-written rules can drift from what the grammar enforces.
3. **Hybrid: hand-written where a writer writes, generated where the
   grammar decides** — chosen. The world and the portraits sit in one
   file the owner edits; the format-rules paragraph comes from the
   code, so words and grammar never disagree (lesson §4.2) and the
   emotion switch changes both at once.

What still comes from `Personas/<Name>/` is only the **voice** — the
reference clip and its transcript, which the TTS needs.

#### The file is a template

The owner asked to see where the generated text goes; the answer is a
Jinja template with visible placeholders. Jinja costs nothing new —
the fork already pins `jinja2==3.1.6` (`requirements.txt`) and uses
it for its pages (`app/main.py:148`); it is rendered in strict mode,
so a misspelled placeholder raises an error instead of printing
nothing. The owner's simplification holds: the rules paragraph has
only two versions (moods on or off), so they are two fixed snippets
kept next to the grammar, not text composed by code.

`stories/lab-outbreak/cast_sheet.md`:

```markdown
---
title: The Lab at the End of the Frequency
cast: [Daniel, Moira, Ralph, Samantha]
---
{{ model_prefix }}
You write a live radio play. Four scientists are trapped in a besieged research lab during a zombie outbreak, speaking over the lab's shortwave radio.

The cast:
- Daniel: Dr. Daniel Hayworth, systems engineer. Dry British understatement; competent, tired, quietly heroic.
- Moira: Dr. Moira Byrne, microbiologist. Irish lilt in her phrasing; grimly fascinated by the science of the outbreak, sometimes forgetting to be afraid.
- Ralph: Dr. Ralph Okafor, security officer. Deep, deliberate, a little paranoid; counts things because counting keeps him calm.
- Samantha: Dr. Samantha Reyes, communications lead running the broadcast. Warm radio voice; optimism worn like armor.

Style: each transmission is one or two short spoken sentences ending with "Over." This is radio: no narration, no stage directions.

{{ format_rules }}

{{ episode }}
```

**The front matter** (between the `---` lines) is for the code — the
model never reads it; the same convention TalkWithMe uses in
`prompt.md`. `cast` names the speakers; each name must match a
`Personas/<Name>/` folder, where the voice clip lives. **Everything
below it is what the model reads**, except the three placeholders:

| Placeholder | Filled from | Why it is not hand-written in the story |
|---|---|---|
| `{{ model_prefix }}` | settings (today `/no_think`) | A quirk of the model, not of the story: auditioning another model (Task 5a) changes a setting, not every story. |
| `{{ format_rules }}` | one of the two fixed snippets, chosen by the emotion switch | It must say exactly what the grammar enforces (lesson §4.2). |
| `{{ episode }}` | the current episode file's text, or empty | Episodes, below. |

The two snippets. Moods off: "Format: write the next lines of the
script, one line per transmission, as `Name: spoken words`." Moods on:
"Format: … as `Name (emotion): spoken words`. The emotion in
parentheses is the one the listener should hear in the speaker's
voice, exactly one of: calm, happy, sad, afraid, terrified, doubtful,
angry, urgent, exhausted. Nothing else in parentheses."

**The boundary that matters.** The cast sheet holds only what is true
for the whole run: the world, the people, the line format. Everything
that changes per round — who may speak, how many lines, what just
happened — goes in the director's instruction for that round, never
in the cast sheet. That keeps the system message identical round
after round, so the prompt cache keeps working. "Over." sits in the
hand-written Style line: the grammar does not enforce it, so it is a
writer's choice, not a format rule.

#### Many files: stories, episodes, runs

The owner's angle: not one file but many — several stories to start
from, entangled with episodes within a show. Three things, kept apart:

- **A story** is authored content, like a series: a folder tracked in
  the fork, with its own cast (voices must exist in `Personas/`):

  ```
  stories/
    lab-outbreak/
      cast_sheet.md          ← the world and the people
      episodes/
        01-supplies.md
        02-pharmacy-run.md
    another-story/
      cast_sheet.md
  ```

- **An episode** is a chapter. Its front matter is for the
  **director**; its body is for the **model** (it fills
  `{{ episode }}`):

  ```markdown
  ---
  title: Supplies
  max_rounds: 30
  beats:
    - The generator fails for a minute and the lights go out.
    - Moira notices Ralph hiding a bite on his hand.
    - Samantha catches a stranger's voice on the frequency.
  ending: they agree to make a run for the pharmacy
  ---
  Previously: this is the first night of the siege.

  Tonight: the lab is running out of antibiotics and food. The pharmacy is two floors up, past the east stairwell, and nobody has been up there since the doors sealed.
  ```

  The director feeds the beats as radio traffic in its instructions
  and steers toward the ending; the model only ever sees the
  "Previously / Tonight" text. The owner's harvested outlines land
  here, one file per episode, the recap written in advance.

- **A run** is one performance of one story, starting at one episode
  (decision 3's folder). Its `script.json` records which story and
  episode each round belonged to, plus the exact system text each
  episode rendered — reproducibility, and the flight recorder. When a
  run moves to the next episode (decision 2's stretch), the script
  turns reset and the system message is re-rendered with the new
  episode's text.

- **Choosing:** `show.story: lab-outbreak` (optionally `show.episode`)
  in `settings.yaml`; `POST /api/show/start` may take a story and an
  episode to override it, so the page can offer a picker later.

Two knock-on changes to decision 3: the cast moves out of the
`show:` settings into the story's front matter (different stories,
different casts); and the run folder is renamed from `shows/` to
`runs/`, so that "show" does not mean three things beside `stories/`.

**For the timebox:** one story (the placeholder cast proven in
run 2), the three placeholders, front-matter parsing, the two rule
snippets; `{{ episode }}` renders empty until episode files exist.
Episode files and moving between them stay a stretch, as decision 2
ruled.

### 4.4 The ruling

The owner, 2026-09-23 (verbatim):

> Adopt all of it. Love it.

- **Adopted:** the hybrid cast sheet — a Jinja template (strict mode,
  `jinja2` already pinned) with front matter for the code and three
  placeholders, `{{ model_prefix }}`, `{{ format_rules }}` (two fixed
  snippets chosen by the emotion switch) and `{{ episode }}`;
  `stories/<story>/cast_sheet.md` plus `episodes/`, tracked in the
  fork (the installer's pinned tag pins the stories too; the owner's
  bibles and episode outlines arrive as pull requests); runs renamed
  to `runs/<run-id>/`; the cast moved into the story's front matter.
- **A note for newcomers:** "bible" and "section" in [ADR-0003] are
  writers' jargon; read as TalkWithMe-era per-persona prompt pieces,
  they mislead. §4.3's first part is the explanation to point to.

### 4.5 What it means for the build

- **Files in the fork:** `stories/lab-outbreak/cast_sheet.md` (the
  placeholder cast of run 2, turned into the template above); the two
  rule snippets beside the grammar templates in `app/show/`.
- **Loading a story:** parse the front matter (the persona-store code
  already parses `prompt.md` front matter — reuse its approach),
  check every `cast` name has a `Personas/<Name>/` folder with a
  voice, render the body with `model_prefix`, `format_rules` and
  `episode`.
- **Configuration:** `show.story` (and optionally `show.episode`)
  select what to play; `model_prefix` is a setting (today
  `/no_think`); the cast is no longer a setting.
- **Runs:** `runs/<run-id>/` (gitignored) instead of `shows/`;
  `script.json` gains the story, each round's episode, and the
  rendered system text per episode.
- **Tests:** rendering with the switch on and off (the snippet
  changes, nothing else does); a missing placeholder variable fails
  loudly; an unknown cast name fails at load, before any request.
- **Stretch (decision 2):** episode files, their beats fed by the
  director, moving from one episode to the next.

## 5. Decision 5 — the director

*The exchange in order, every message verbatim: the agent's proposal, the owner's first question (the message was cut off mid-sentence), the agent's answer, the owner's three questions, the agent's answer with the revisions, and the ruling.*

### 5.1 The agent's proposal (verbatim)

Here's the director: first what it is and what's already settled, then what it decides each round, a worked example, and the choices left for you.

#### What the director is

The director is **code in the server, not an LLM call**. Before every round it decides that round's constraints and **writes each one twice**:
- **in words**, in the instruction it sends as the `user` turn;
- **in the grammar** sent with that request.

It's your 2024 hidden Narrator ("Narrator: There is an update in the story…"), moved out of the prompt and into code. It also decides **when the radio listens**.

#### What's already settled (receipts)

- **ADR-0003, point 2:** the director is code; it sets the beat, who may speak, the line budget, a stage direction and entropy terms, all written into the `user` turn.
- **ADR-0003, point 7:** the mic opens on a random **time window of played audio** (a minimum and maximum number of seconds, with the probability rising in between), never a round count. That was your pushback.
- **ADR-0003, point 8:** the round that answers a listener has **one speaker**.
- **Lessons §4.2 and §2.6:** every rule in the grammar is also stated in words; "up to four lines" is read as four, so the grammar's bound is what enforces the budget.
- **Spec §5.1, entropy terms:** your 2024 Narrator named a random speaker, a random emotional register, a random word count (5–50) and one random adjective from a list of about 70. You recalled that it "brought the narration alive" and fought repetition.
- **Today's decisions:**
  - the director also runs the trim (#2);
  - per-round rules go in the instruction, never in the cast sheet (#4);
  - episode beats are fed in by the director, as a stretch (#2).

#### What it decides each round

**Three kinds of round:**
1. **Free round:** the scientists talk.
2. **Invitation round:** one voice calls out to the listeners, then the page starts listening.
3. **Answer round:** one voice answers what the listener said, or reacts to silence.

**The knobs, with my proposal for the timebox:**

| Knob | Proposal |
|---|---|
| **Who may speak** | 2–3 names in a free round, chosen by three rules in order: (a) whoever has been silent longest is always in; (b) anyone named in the last round (e.g. "Ralph, the doors?") is in; (c) random names fill the rest. Rule (a) is our cheapest defense against one voice taking over, the identity-bleed risk. The model picks the order and who speaks within the list. |
| **How many lines** | Random between 1 and 4, weighted toward 2–3. Exactly 1 for invitation and answer rounds. Enforced by `line{1,N}`, and said as "the next two lines". |
| **What happens** | An event from the story's pool of "radio traffic" (the gate's events are the seed), about every other round, with no repeats until the pool is used up. The other rounds get a plain "continue". The pool lives **in the story folder** (e.g. `stories/lab-outbreak/events.yaml`), since events are story content. Later, episode beats take this role. |
| **Entropy term** | One tone word per round from a list, as in 2024 ("Let the mood be: brittle"). It's cheap, and it's the proven repetition fighter. The mood tags already vary the **delivery**; this word varies the **content**. |
| **When the radio listens** | The browser reports seconds of audio played with each round request; only the browser knows what has actually played. Below the minimum, never; between minimum and maximum, a rising chance; at the maximum, always. |
| **Who talks to the listener** | An `operator` named in the story's front matter (for this story, Samantha, the comms lead) both invites and answers. |
| **Silence** | If the listening window closes with no usable transcript, the next round is told "only static answers", then play continues. |

**What the director remembers.** As little as possible, and **derived from `script.json`** every round: who spoke when, which events were used, the seconds played since the last listening window. Nothing kept on the side can fall out of sync. The one extra is the **random seed, stored in the run**, which makes a retake reproducible and supports the canned episode.

#### A worked example

**Free round.** Instruction (the `user` turn):

```
Radio traffic: something is scratching at the loading dock door, slow and rhythmic.
Ralph and Moira speak next: the next two lines, each with the emotion in its voice. Let the mood be: brittle.
```

Grammar, written from the same decision:

```
root    ::= line{1,2}
line    ::= speaker " (" emotion "): " text "\n"
speaker ::= "Ralph" | "Moira"
emotion ::= "calm" | ... | "exhausted"
text    ::= [^\n\[\]()]+
```

**Invitation round:** "Samantha turns to the microphone and asks anyone listening to answer: one line." The grammar allows `"Samantha"` only, with `line{1,1}`. The page then starts listening.

**Answer round:** "A voice on the frequency says: 'I'm in Austin, the bridges are down.' Samantha answers the voice: one line."

#### Your choices (my picks in bold)

- **a. Who may speak:** **silent-longest + named + random fill, 2–3 names**, or plain random.
- **b. Line budget:** **1–4 weighted to 2–3**, or a fixed number.
- **c. Events:** **the story's pool, about every other round, no repeats**, or every round.
- **d. Entropy terms:** **one tone word per round**, or none for now (keeping the audition's comparison cleaner).
- **e. The mic:** **played-seconds window, with an `operator` in the story who invites and answers**, or any cast member.
- **f. Silence:** **"only static answers", then carry on.**
- **g. Memory:** **derived from `script.json`, plus the seed stored in the run.**

Which do you want to challenge? Or adopt the set and adjust later?

### 5.2 The owner's first question (verbatim)

> This is a very good proposal. I will adopt it almost all but I have a few questions first.
>
> Questions to improve my understanding:
>
> * When you write "Radio traffic: something is scratching at the loading dock door, slow and rhythmic."... I assume this radio traffic line is not something we will reproduce as a TTS line, right? Otherwise we would need another voice, and based on the app, another persona for an unspecified character (radio traffic voice). 
> * In my 2024,

### 5.3 The agent's answer (verbatim)

**First question: no, that line is never spoken.**

- **Who hears what:** the audience only hears **script lines**, the `Name (mood): text` lines the model writes. The parser picks them out of the stream one at a time, and each finished line goes to the TTS in that character's voice.
- **What the instruction is:** the director's instruction, including its "Radio traffic: …" part, is the `user` turn of the request. It goes to llama.cpp as input and never passes through the parser, so it never reaches the TTS.
- **How the audience learns about an event:** only through the characters' reactions, for example "Ralph (afraid): Something's at the loading dock door. It's rhythmic. Over."

The same goes for a listener's words: they enter the next instruction as text, and nobody repeats them aloud. The listener already heard themselves.

So no extra voice and no extra persona. You've caught a naming problem, though: **"Radio traffic:" sounds like something heard on the radio.** In the gate it was only a framing for the model. I'd rename the two kinds of input so they say what they are:
- **"Offstage:"** for events: something happens, the characters react;
- **"A voice on the frequency says:"** for the listener's words only.

A possible later option, and not something I'm recommending now: an **announcer**, a fifth voice with its own reference clip that reads events aloud, the way 1930s radio plays had one. The grammar would simply allow `"Announcer"` as a speaker. It's worth remembering for the 1930s look, but it's outside the timebox.

**Your second question got cut off after "In my 2024,".** Please send the rest.

### 5.4 The owner's three questions (verbatim)

> Please document the idea of the announcer (as a follow up? or in the roadmap?).
>
> My other questions:
>
> * In my 2024 prototype, I think the narrator was actually identified also for the LLM as `Narrator: ....`, though I am not 100% sure (please confirm), will we be doing that here too, as `Director: ... ` or do you recommend against? I am more inclined to not do that, but just write the directors instructions before each round as you show in `Invitation round: "Samantha turns to the microphone and asks anyone listening to answer: one line."`, and otherwise this radio traffic thing you propose do not work.
> * About "Who talks to the listener", wait, I do not think only one character should answer the coms if an external user speaks for the whole story. What if the user asks a direct question to one of the characters? Maybe I do not understand what you mean.
> * About "When the radio listens": I don't really understand what you said there. My questions is: How do we dynamically extend the listening time if we detect a user is probably speaking? In my 2024 prototype I think I set a fixed max time to listen, but if a voice was talking, we detected the "Over and out" from the transcript and closed listening earlier... But I think this is not an option here as I do not think we have control in the browser of streaming the input in segments to send to STT for transcript, right? Anyway, this is a rabbit hole, we discussed some of the challenges in `docs/discussions/2026-09-13-product-definition-brainstorm.md` in section "5. Challenges for voice recognition & audio processing".

### 5.5 The agent's answer, with the revisions (verbatim)

The announcer is now in `docs/roadmap.md` under "Ideas / parking lot": what it is, how small the mechanism would be, what parks it, and what would bring it back. It's uncommitted.

#### 1. "Narrator:" in 2024, and whether we label the director

**Confirmed.** Every 2024 directive began with the label: `query = f"Narrator: {character['name']} {action} a {emotion} sentence of at least {num_words} words related to {descriptive} in the next line."` (`zradio_local.py:657`). The system prompt also introduced the Narrator to the model as "not a character in the play" (line 520).

**I agree with you: no label.**
- **The role already says it.** The director's text travels as the `user` turn, and the chat template marks it as a separate turn (`<SPECIAL_11>User`), distinct from the script lines. A label would say the same thing twice.
- **Our runs already did without one.** The gate and run 2 sent unlabeled instructions ("Radio traffic: … Write the next lines of the script: …"). The model reacted to the events, and every line came out in the right shape.
- **A label buys nothing and risks a little.** The grammar makes a "Director:" line impossible anyway, and the label only invites the model to treat the director as a character.

So the instruction is plain sentences:
- "Offstage: …" for events;
- "A voice on the frequency says: …" for a listener;
- then the constraint: who speaks, how many lines.

If "this radio traffic thing" in your message meant the label, agreed: it goes, and events become "Offstage:".

#### 2. Who answers the listener

**You're right; my proposal was wrong there.** I had the operator both invite and answer. Your 2024 code picked a **random** character to answer (`_narrator_user_message_received`); neither is right when the listener asks someone something. Revised:
- **Invitation:** one voice calls out to the listeners. By default that's the story's `operator` (Samantha, who runs the radio), since someone has to be at the microphone.
- **Answer:** **whoever the listener addressed**, done in two layers:
  1. **The model decides by default.** The answer round's grammar allows the **whole cast** and one line. The instruction says: "The character the voice addressed answers; if it addressed no one, whoever fits best answers." The model reads the listener's words, so "Moira, is the virus airborne?" gets Moira, and an unaddressed question gets whoever fits. This copes with Whisper misspelling names, which stays a live problem even with a button (challenge C6, brainstorm §5).
  2. **The code guarantees it when it's sure.** If the transcript contains a cast name exactly, the director narrows the grammar to that name.
- **Afterwards:** the next free round follows the usual "anyone named in the last round is in" rule, so the others react naturally.

#### 3. How long the radio listens

My table mixed up two different timers. There are three separate pieces, and none of them needs the 2024 "over and out" trick.

1. **Cadence: when the show opens the mic.** How much audio plays between invitations, set by `interaction_min_s` and `interaction_max_s` (story-loop §9 Q2). That's what I described before.
2. **The waiting window: how long the show waits for a press.** `listen_window_s`, for example 10 s. It **stops counting the moment the button goes down.**
3. **The press itself: hold-to-talk** ("Definitely hold-to-talk", your story-loop ruling Q4). Recording lasts exactly as long as the button is held; **release is the end of speech.** The brainstorm lists end-of-speech detection as challenge C2, "solved by construction" by the button.
   - There's no fixed limit to cut someone off, and no need to spot "over and out".
   - The one limit is a safety cap on a single press (say 30 s), against a stuck button.

A timeline:

```
Samantha: "Anyone out there? Tell us where you are. Over."
  → the queue drains → LISTENING: button enabled, window 10 s starts
  (a) nobody presses in 10 s → next round: "only static answers" → free rounds resume
  (b) press at 4 s → recording (window no longer counts) → release at 17 s
      → audio to Whisper (~1 s) → answer round with the listener's words
```

About streaming from the browser: it is actually possible. A browser can deliver the recording in chunks while it's running, and can measure the sound level live. So the 2024 approach could be rebuilt in the browser. **Hold-to-talk just makes it unnecessary for the MVP.** The always-listening version (voice detection, judging when a sentence is finished) stays the post-MVP path, as the brainstorm planned. A live level meter while the button is held ("we hear you") would be cheap polish.

Do you adopt #5 with these revisions: no label, "Offstage:", the addressed character answers (model by default, narrowed by an exact name), and the three separate timers?

### 5.6 The ruling

The owner, 2026-09-23 (verbatim):

> Yes, adopt #5 with these revisions: no label, "Offstage:", the addressed character answers (model by default, narrowed by an exact name), and the three separate timers.

- **Adopted:** the proposal of §5.1 with the revisions of §5.5 — no
  label on the director's instruction; events phrased "Offstage: …";
  the listener's words phrased "A voice on the frequency says: …";
  the character the listener addressed answers (the model decides by
  default, the director narrows to an exact cast-name match); three
  separate timers.
- **Parked:** an announcer voice that would read some events aloud —
  `docs/roadmap.md`, "Ideas / parking lot".

### 5.7 What it means for the build

- **Three kinds of round**, plus the silent case:
  - **free** — the scientists talk; **2–3 names** allowed, chosen in
    order: whoever has been silent longest (always), anyone named in
    the last round or in the listener's words, then random names;
    **1–4 lines, weighted to 2–3**;
  - **invitation** — the story's `operator` (a new field in the
    story's front matter; Samantha in `lab-outbreak`) calls out to
    the listeners; one line; the page then listens;
  - **answer** — the whole cast allowed, one line, the instruction
    saying "the character the voice addressed answers; if it
    addressed no one, whoever fits best answers"; an exact cast-name
    match in the transcript narrows the grammar to that name;
  - **silence** — the waiting window closed without a usable
    transcript: "Only static answers.", then free rounds resume.
    *[note 2026-09-24: worded "Only static answers; the broadcast
    goes on." in step 2.1b — with the bare sentence, the operator
    signed off in both live drives ("This is a dead end.",
    "Farewell, dear listeners…"); see the TODO's 2.1b.]*
- **The instruction** (the `user` turn) is plain sentences with no
  label: "Offstage: …" for an event, "A voice on the frequency says:
  …" for a listener, then the constraint in words ("Ralph and Moira
  speak next: the next two lines, each with the emotion in its
  voice."), then the entropy term ("Let the mood be: brittle.").
  Every constraint in the grammar is said in these words (lesson
  §4.2); the budget is enforced by `line{1,N}` and said as "the next
  N lines".
- **Events:** the story's pool (`stories/<story>/events.yaml`),
  about every other round, no repeats until the pool is used up; a
  plain "continue" otherwise; episode beats take this role later
  (decision 2's stretch). Never spoken — the audience learns of an
  event through the characters' reactions.
- **Entropy term:** one tone word per round from a list, the 2024
  trick (where the list lives is settled in code; a story may bring
  its own).
- **The three timers** (yaml knobs):
  - **cadence** — `interaction_min_s` / `interaction_max_s`, in
    seconds of played audio, reported by the browser with each round
    request (only the browser knows what has played): never below
    the minimum, a linearly rising chance in between, always at the
    maximum;
  - **the waiting window** — `listen_window_s`: how long the show
    waits for a press; it stops counting when the button goes down;
  - **the press** — hold-to-talk: release is the end of speech; the
    only limit is a safety cap on one press (about 30 s).
- **Memory:** derived from the run's `script.json` every round (who
  spoke when, which events were used, played seconds since the last
  listening window); the random seed stored in the run, so a retake
  is reproducible.
- **Tests** (the TODO's director acceptance, extended): the
  allowlist and the budget appear both in the instruction's words
  and in the grammar; the silent-longest name is always allowed in a
  free round; with a seeded random source, no invitation before
  `interaction_min_s` and always one by `interaction_max_s`; an
  exact cast name in a transcript narrows the answer round to that
  name; a silent window yields the static round.

## 6. Decision 6 — the listener's turn

*The exchange in order, every message verbatim: the agent's proposal, the owner's question and gauge idea, the agent's answer (the check could not run: the tunnel was down), the owner's request to run it, the agent's checks and results, and the ruling. One two-sentence bridge the agent wrote between its two checks is not in the session transcript and is not reproduced; its facts are restated in the results and in §6.7.*

### 6.1 The agent's proposal (verbatim)

**#6, the listener's turn, briefly.** Most of it was settled in #5: hold-to-talk, the three timers, who answers. What's left is the path from the button to the director, and how to throw away bad transcripts.

**Today's path** (the fork's code): the browser records WebM, sends it to `POST /api/stt` (`app/routers/stt.py:30`), which passes it to Whisper, and the text comes back. Two things in it are wrong for the show:
1. **An empty transcript becomes words.** `stt_client.py:85` substitutes the literal text "No response received from STT server", which the show would read as a listener speaking.
2. **Whisper's confidence is thrown away.** The client returns only text and language. Your live test earlier showed Whisper's reply carries per-segment `no_speech_prob` (0.068) and `avg_logprob` (−0.62), plus its own default cut-offs: `no_speech_threshold` 0.6 and `log_prob_threshold` −1.0.

**Proposal:**
- **One path to Whisper, made honest.** `transcribe_audio` returns empty text instead of the placeholder, plus two confidence numbers: the highest `no_speech_prob` and the average `avg_logprob`. The chat UI can show its own message for an empty result.
- **A filter in the show's round endpoint.** A transcript counts as **silence** if any of these is true:
  - it's empty or a single character;
  - no-speech is above 0.6, or confidence is below −1.0 (Whisper's own defaults, as yaml knobs);
  - it matches a short list of Whisper's classic hallucinations ("Thank you for watching.", "Subtitles by…").

  Silence leads to the static round from #5.
- **The browser flow:**
  1. listening;
  2. hold-to-talk;
  3. on release, upload to `/api/stt`;
  4. the page shows a small caption, "Heard: …", which is cheap and helps both the demo and debugging;
  5. `POST /api/show/round` with the text and the played seconds.
- **Names** (challenge C6, Whisper and proper names): the model-decides answer rule from #5 already tolerates misspellings. There's one possible cheap improvement: pass the cast names to Whisper as a hint (OpenAI's API has a `prompt` field for this, and our Whisper's options show `initial_prompt`/`hotwords` slots). I believe our endpoint accepts it; that's one request on the box to check.

**Your picks** (my lean in bold):
- **a.** **filter in the round endpoint, with Whisper's thresholds as knobs, plus a small hallucination list;**
- **b.** **unusable transcripts count as silence;**
- **c.** **"Heard: …" caption on the page;**
- **d.** **cast names as a Whisper hint, if the one-minute check passes.**

Adopt as is? Or do you want the name-hint check run first?

### 6.2 The owner's question, and the gauge idea (verbatim)

> I like it. I agree with almost everything.
> I do not understand: d. cast names as a Whisper hint, if the one-minute check passes.
>
> Small side quest UI idea: Instead of the dry "heard" caption on the page, add to the page a small gauge that goes up or down if speech is detected, similar to an old radio gauge.

### 6.3 The agent's answer (verbatim)

**(d) in plain words.** Whisper often mangles unusual names: "Moira" can come out as "Myra", and "Okafor" as "Oh, Kafer". Whisper accepts an optional **text hint**: a short piece of text it treats as "what was said just before this recording". If that hint contains "Daniel, Moira, Ralph, Samantha, Dr. Byrne, Dr. Okafor", Whisper becomes more likely to spell those names that way when it hears them. It's a nudge, not a rule.
- **Why it matters:** decision 5's guarantee (an exact cast name narrows the answer to that character) only kicks in if the name is spelled right. The fallback, where the model picks, still works when it isn't. The hint just makes the guarantee apply more often.
- **Why "if the check passes":** our Whisper server may call this field `prompt` (OpenAI's name) or something else, and I haven't seen it accept one. Its earlier reply listed an `initial_prompt` option set to `null`, which is suggestive but not proof.

The check is cheap. I'll send your 09-19 recording again, this time with the cast names as the hint, and see whether Whisper's reply echoes them back as its `initial_prompt`. First I need to see whether your tunnel is up.

*[The agent ran the check here; the tunnel was down.]*

Your tunnel is down again: the Whisper port answered nothing (HTTP 000). So the check **did not run**, and the two tracebacks are only my script failing on empty replies. I should have stopped after the tunnel probe instead of chaining the requests. The check waits until you bring the tunnel back; it takes one command.

**Your gauge: yes, and it's a better idea than my caption.** It's also period-true. Radios from the mid-1930s had a **"magic eye"** tuning tube, a green glow that narrowed as the signal got stronger. Later studio gear used a VU needle. Either one fits the 1930s look.
- **How it works:** the browser can measure loudness live from the microphone (Web Audio's analyser, read many times a second) and drive a needle or a glowing eye from it. No server involved.
- **A bonus:** the same meter can follow **the actors' voices** during playback, reading the TTS audio instead of the mic. The gauge then moves whenever anyone is on the air, and while you hold the button it shows "we hear you".
- **What happens to the caption:** the gauge shows that you're being heard, but not what Whisper understood. So I'd keep the "Heard: …" text **only when `show.debug` is on**, for us, and give the audience the gauge.
- **When:** it belongs with the day-three polish and the 1930s look. By my estimate it's about an hour for a simple version, so outside the exit criterion.

So #6 would be adopted with:
- the filter, silence handling and names hint as proposed (the hint pending the one-minute check);
- the caption kept for debug only;
- the gauge added to the day-three polish list.

Adopt that?

### 6.4 The owner: run the check now (verbatim)

> Wait, before adopting, the VM is there wasting money for your to test things... Tunnel is up now. Check that our whisper support what we need for feature d.

### 6.5 The agent's checks and results (verbatim)

The tunnel is up. Two checks:
1. **The Whisper server's own API description** (`/openapi.json`): which form fields `/v1/audio/transcriptions` accepts.
2. **The live test:** the same recording three times (no hint, the hint as `prompt`, the hint as `initial_prompt`), printing only the transcript and the `initial_prompt` Whisper reports having used.

*[The two checks ran here — §6.7 has the field list.]*

**(d) works.** Our Whisper takes the hint in a field called `prompt`, and actually uses it.

| Request | Transcript | Hint Whisper reports using | Language (certainty) | Audio kept as speech |
|---|---|---|---|---|
| 1. no hint | "I said hello, Daniel." | none | en (0.795) | 4.44 s |
| 2. `prompt` = cast names | "I said hello, Daniel." | "Daniel, Moira, Ralph, Samantha. Dr. Byrne, Dr. Okafor." | en (0.795) | 4.44 s |
| 3. + `language=en` + `vad_filter=true` | "I said hello, Daniel." | same | **en (1)** | **3.144 s** |

What that proves and what it doesn't:
- **The hint is accepted and applied:** Whisper echoes it back as the `initial_prompt` it decoded with.
- **The benefit on hard names is not shown by this recording.** It only says "Daniel", which Whisper already gets right. A recording that says "Okafor" or "Byrne" would show it, and any hold-to-talk test in 6b will do.

**Two bonus findings from the server's field list, both cheap to use:**
- **`language=en`:** the show is in English. Without it, Whisper was only 79.5 % sure and gave Latin 6 %. Forcing it removes one way to get garbage.
- **`vad_filter=true`:** Whisper's built-in voice-activity filter cuts the non-speech parts before decoding (4.44 s went down to 3.14 s). That's a direct help against challenge C1, Whisper inventing text from noise, and it works before our confidence filter even runs.

So #6, updated:
- **a.** the filter in the round endpoint: Whisper's thresholds as knobs, plus a short hallucination list;
- **b.** unusable transcripts count as silence;
- **c.** "Heard: …" only when `show.debug` is on, and the radio gauge (magic eye or VU needle) on the day-three polish list;
- **d.** the cast names sent as `prompt` (confirmed);
- **e.** every show transcription also sends `language=en` and `vad_filter=true`.

Adopt? And about the box: that was the last check I need tonight, so if you're done for the evening, hibernating it now saves the idle hours. Your call, as always.

### 6.6 The ruling

The owner, 2026-09-23 (verbatim):

> Beautiful. Adopt this last version.

- **Adopted:** the last version of §6.5 — (a) the filter in the round
  endpoint, Whisper's thresholds as knobs plus a short hallucination
  list; (b) unusable transcripts count as silence; (c) the "Heard: …"
  text only while `show.debug` is on, and the owner's radio gauge on
  the day-three polish list; (d) the cast names sent to Whisper as
  `prompt`; (e) every show transcription also sends `language=en` and
  `vad_filter=true`.

### 6.7 What it means for the build

- **Measured 2026-09-23** (the box, through the tunnel): the Whisper
  server's API description lists, for `/v1/audio/transcriptions`,
  the form fields `file, prompt, response_format, task, language,
  vad_filter, vad_threshold, vad_neg_threshold,
  vad_min_speech_duration_ms, vad_max_speech_duration_s,
  vad_min_silence_duration_ms, vad_speech_pad_ms,
  repetition_penalty, gpt_refine` — `prompt` yes, `initial_prompt`
  and `hotwords` no. With `prompt` set, the reply reports it as the
  `initial_prompt` it decoded with; `language=en` raised the
  language certainty from 0.795 to 1; `vad_filter=true` kept 3.144 s
  of the 4.44 s recording as speech. The benefit of the name hint on
  hard names (Okafor, Byrne) is believed, not yet shown: the test
  recording says only "Daniel".
- **The STT client** (`app/services/stt_client.py` in the fork):
  `transcribe_audio` returns empty text instead of the placeholder
  "No response received from STT server" (line 85), plus two
  confidence numbers from Whisper's segments — the highest
  `no_speech_prob` and the average `avg_logprob`; it passes
  `prompt`, `language` and `vad_filter` when the caller gives them.
  The chat UI shows its own message for an empty result.
  *[note 2026-09-24, as built in step 2.4 with the owner's picks:
  upstream's `transcribe_audio` stays untouched (stay close to
  upstream); the show calls a new `transcribe_for_show` instead, so
  the placeholder cannot reach the director — and it is on the
  filter's list of noise besides. The show reaches Whisper through
  its own route, `POST /api/show/listen`; the prompt is the cast's
  first names (surnames later if Whisper mangles them). The deployed
  Whisper server rejects `verbose_json` and carries the segments in
  plain `json` (found by the live check).]*
- **The show's transcription** sends `prompt` = the story's cast
  names (and the surnames the cast sheet uses), `language` (a knob,
  `en`), `vad_filter=true`. Whether the show page reaches Whisper
  through `/api/stt` with these optional fields or through a
  show-specific route is settled in code; the filter lives on the
  server either way.
- **The filter** (in the round endpoint): a transcript counts as
  silence if it is empty or one character, if `no_speech_prob` is
  above 0.6, if `avg_logprob` is below −1.0 (Whisper's own defaults,
  yaml knobs), or if it matches a short list of Whisper's known
  hallucinations. Silence leads to the static round of decision 5.
- **The page:** listening → hold-to-talk → on release, the audio to
  Whisper → `POST /api/show/round` with the text and the played
  seconds. "Heard: …" appears only while `show.debug` is on.
- **The radio gauge** (day-three polish, with the 1930s look): a
  "magic eye" tuning tube or a VU needle, driven in the browser by
  Web Audio's analyser — the microphone's level while the button is
  held, the actors' TTS audio while it plays; about an hour for a
  simple version (estimate).
- **Tests:** fake Whisper replies — empty, high no-speech, low
  confidence, a known hallucination — each yield the static round;
  the placeholder text can never reach the director; the show's
  transcription request carries `prompt`, `language` and
  `vad_filter`.

## 7. Decisions 1 and 7 — the build order and the module layout

### 7.1 The agent's proposal (verbatim)

One change from my agenda first: **I'm revising my own build order.** Decisions 2–6 added about seven pieces. Building all of them offline before touching the box would put the first real run on the evening of 09-24 at best, which leaves the checkpoint judging code that has never met the model. The better shape is a **thin end-to-end slice first**, then the rules layered on top.

#### #1: build order and what the checkpoint judges

**Timeline:** the clock started at 14:46 today; the checkpoint is 02:46 on 09-25, which in practice means the morning of the 25th; the end is 14:46 on 09-26.

**Slice 1, the skeleton. Target: end of day on 09-24.** Every piece is built in its simplest form, each tested offline first, then run on the box:
- the `show:` settings;
- the story loader, which renders the cast sheet template;
- the grammar builder (allowlist, budget, mood rule);
- the stream parser and punctuation normalizer;
- the run record (`script.json`) and the assembler, appending only;
- **director v0**: 2–3 random names, 2–3 lines, an "Offstage:" event every other round, **no mic yet**;
- `POST /api/show/start` and `/round` (streaming);
- a small **driver script** that plays ten rounds through the tunnel with no browser.

**Slice 2, the rules. Target: the checkpoint.**
- **director v1:**
  - silent-longest and just-named speakers;
  - the tone word;
  - the cadence, with invitation, answer and static rounds, fed by fake transcripts from the driver;
- the trim, with a low `context_budget`, measuring the pause;
- the debug switch (`/apply-template`);
- the transcript filter and the STT client changes.

**The checkpoint judges, on the box and with no browser:**
- ten unattended rounds;
- speakers and line counts obeying the director;
- one invitation followed by an answer from an injected transcript, and one silent window giving the static round;
- the trim firing;
- the debug files written.

Then **continue, scale down, or stop.** Scaling down would mean dropping the tone word or the events first, then the cadence rules: keep the mic, simplify when it opens. The fallback is still TalkWithMe 7.1 plus the canned episode.

**Slice 3, the browser. Days 2–3.**
- the `/show` page and `show.js` states (idle, generating, playing, listening);
- the SSE reader pulled out of `chat.js`;
- the accumulator in `tts.js`;
- hold-to-talk in `stt.js`, with the played seconds reported back;
- **the exit criterion judged by ear** on the real stack.

**Polish, only if the checkpoint is green:** prefetch, dead air, the 1930s look with your gauge, then episodes (the stretch from #2).

#### #7: module layout and branches

In the fork:

```
app/
  config.py            ← + the show: settings model, beside the existing ones
  show/                ← new package, one file per piece
    story.py           ← load stories/<story>/: front matter, Jinja (strict), voice check
    rules/             ← the two format snippets (moods off / on)
    grammar.py         ← GBNF builder
    parser.py          ← stream parser + normalizer
    script.py          ← the run record, the assembler, the trim
    director.py        ← round kinds, speakers, budget, events, tone word, cadence
    listen.py          ← the transcript filter
  routers/show.py      ← GET /show, POST /api/show/start, POST /api/show/round
  services/llm.py      ← + the grammar key in the request
  services/stt_client.py ← decision 6's changes
stories/lab-outbreak/  ← cast_sheet.md, events.yaml (tracked)
runs/                  ← gitignored
templates/show.html
static/show.js, static/sse.js (the extracted reader); tts.js, stt.js changed
scripts/drive_show.py  ← the driver for slices 1–2 (standard library only)
tests/test_show_*.py   ← one per module; conftest's fixture gains the runs/ and stories/ roots
```

**Branches and PRs:**
- **Fork:** branch `alfre2v/show-engine`, with **one PR per slice**, each merged before the next. That gives you three review points, and each merged slice is backed up on GitHub. The installer's pin moves to a new tag (`tz-0.2`) only after slice 3, once the show works in the browser.
- **zombie-radio:** the design doc's branch (same name, 6 commits so far) goes up as a PR once you're happy with the design. The TODO gains the slice plan.

Adopt #1 (skeleton first) and #7 as laid out?

### 7.2 The ruling

The owner, 2026-09-23 (verbatim):

> Yes, Adopt #1 (skeleton first) and #7 as laid out. 
> This is a very good grouping of tasks in slices to keep complexity from stopping progress.

- **Adopted:** skeleton first — three slices, each ending in a
  review point — and the module layout as laid out.
- **What changed from the agenda (§1):** the agenda's decision 1 put
  every box-free piece before the first box run. Decisions 2–6 added
  about seven pieces, so that order would have left the checkpoint
  judging code that had never met the model. The thin end-to-end
  slice first, rules layered after, is the correction.

### 7.3 What it means for the build

- **The three slices, in order** (clock: started 2026-09-23 14:46
  CDT; checkpoint 2026-09-25 02:46, in practice that morning; end
  2026-09-26 14:46):
  1. **The skeleton** — target end of day 2026-09-24: the `show:`
     settings; the story loader rendering the cast-sheet template
     (§4); the grammar builder; the stream parser and normalizer; the
     run record and the assembler, appending only (§3); director v0
     (2–3 random names, 2–3 lines, an "Offstage:" event every other
     round, no microphone); the request with the grammar key;
     `POST /api/show/start` and `/round`; the driver script — ten
     rounds on the box, through the tunnel, no browser.
  2. **The rules** — target the checkpoint: director v1 (§5.7 —
     silent-longest and just-named speakers, the tone word, the
     cadence with invitation, answer and static rounds, fed by fake
     transcripts from the driver); the trim with a low
     `context_budget`, its pause measured (§2.4); the debug switch
     with `/apply-template`; the transcript filter and the STT client
     changes (§6.7).
  3. **The browser** — days 2–3: the `/show` page and `show.js`
     states; the SSE reader extracted from `chat.js`; the accumulator
     in `tts.js`; hold-to-talk in `stt.js`, the played seconds
     reported back; the exit criterion judged by ear on the real
     stack.
- **What the checkpoint judges** (on the box, no browser): ten
  unattended rounds; speakers and line counts obeying the director;
  an invitation then an answer from an injected transcript; a silent
  window giving the static round; the trim firing; the debug files
  written. Verdict: continue, scale down, or stop. **Scale-down
  order:** the tone word and the events first, then the cadence
  rules (keep the microphone, simplify when it opens). **Fallback:**
  TalkWithMe 7.1 plus the canned episode.
- **Polish, only if the checkpoint is green:** prefetch, dead air,
  the 1930s look with the owner's gauge, then episodes (decision 2's
  stretch).
- **The layout** (in the fork): `app/show/` with `story.py`,
  `rules/` (the two format snippets), `grammar.py`, `parser.py`,
  `script.py` (record, assembler, trim), `director.py`, `listen.py`
  (the transcript filter); `app/routers/show.py` (`GET /show`,
  `POST /api/show/start`, `POST /api/show/round`); the show settings
  model in `app/config.py` beside the existing ones; the grammar key
  in `app/services/llm.py`; decision 6's changes in
  `app/services/stt_client.py`; `stories/lab-outbreak/`
  (`cast_sheet.md`, `events.yaml`, tracked); `runs/` (gitignored);
  `templates/show.html`; `static/show.js` and `static/sse.js`, with
  `tts.js` and `stt.js` changed; `scripts/drive_show.py` (standard
  library only); `tests/test_show_*.py`, one per module, the isolation
  fixture gaining the runs and stories roots.
- **Branches and pull requests:** in the fork, **one feature branch
  per slice, each cut from the fork's up-to-date `master`** —
  `alfre2v/show-slice-1-skeleton`, `alfre2v/show-slice-2-rules`,
  `alfre2v/show-slice-3-browser` — each with its own pull request,
  the next branch cut only after the previous one is merged (owner's
  precision on §7.1's "branch `alfre2v/show-engine`, with one PR per
  slice"); the installer's pin moves to `tz-0.2` only after slice 3. In this
  repository, the design's branch of the same name goes up as a pull
  request when the owner is happy with the design.

## 8. Terms for a show's timeline (agreed 2026-09-24)

*While shaping step 2.1b (the pacing knobs), the agent called a run of
rounds sharing a tone word, or lying between two events, "a stretch".
Asked by the owner whether that was an abstraction or casual language,
the agent answered it was casual and proposed two precise names
instead — gap and hold. The owner adopted them and asked that the
terms for a show's timeline be written down, so both sides speak of
timelines the same way. "Stretch" is retired.*

### 8.1 The terms

- **Run** — one performance: one `runs/<run-id>/script.json` in the
  fork, from Start to the last round.
- **Round** — one request to the model and the lines it returns,
  numbered from 1 within a run.
- **Kind** — every round has one (§5.7; built in step 2.1):
  - **free** — the cast talks;
  - **invitation** — the story's operator asks anyone listening to
    answer; the page listens next;
  - **answer** — after an invitation, the character the listener
    addressed answers;
  - **static** — after an invitation that heard nothing, the operator
    reacts to the silence.
- **Line budget** — the most lines a round may have: 1-4 in a free
  round (weighted to 2-3), 1 in the other kinds; said in the
  instruction ("the next two lines") and enforced by the grammar.
- **Event** — something that happens offstage, drawn from the story's
  pool (`events.yaml`) and given in a free round's instruction as
  "Offstage: ..."; never spoken — the characters react to it.
- **Gap** — how many free rounds pass from one event to the next:
  `show.event_every` (default 2) plus or minus `show.event_jitter`
  (default 1), never below 1. Only free rounds count; the other kinds
  neither count nor carry events. The run's first free round opens
  with an event. `event_every: 0` turns events off.
- **Tone word** — one word from the story's list (`tones.yaml`), given
  as "Let the tone be: brittle."; it colors *what* the characters say,
  while the emotion tag colors *how* they sound. Free, invitation and
  static rounds carry one; answer rounds carry none (the listener's
  words set their content).
- **Hold** — how many rounds one tone word is kept: `show.tone_hold`
  (default 3) plus or minus `show.tone_jitter` (default 1), never
  below 1. Only the rounds that carry a tone word count; the next word
  is always a different one. `tone_hold: 0` turns tone words off.
- **Jitter** — the plus-or-minus around a gap or a hold. Each gap and
  each hold is drawn once, when it begins, from a generator seeded by
  the run's seed and the round where it began: listeners cannot hear
  a fixed beat, and a seed still replays the run.
- **Played seconds** — the running total of show audio the page has
  played since the run started, sent with every round request
  (`played_s`).
- **Cadence** — when the radio invites the listeners, in played
  seconds since the last invitation: never before
  `show.interaction_min_s`, always by `show.interaction_max_s`, a
  linearly rising chance in between (§5.7).
- **Listening window** — after an invitation, how long the page waits
  for a press (`show.listen_window_s`); the **press** is hold-to-talk,
  capped by `show.press_cap_s` (§5.5).

### 8.2 A timeline with the defaults

```
round  1        2        3        4        5        6        7        8        9        10
kind   free     free     free     free     free     invite   answer   free     free     free
tone   brittle  -------- -------- wry      -------- funereal .        -------- -------- --------
event  *                 *                                            *                 *
```

`*` an event; a word where a tone word begins, `--------` while it is
held, `.` a round with no tone word.

- **Events** at rounds 1, 3, 8 and 10: the opening event, then gaps of
  2 (rounds 2 and 3), 3 (rounds 4, 5 and 8 — the invitation and the
  answer do not count) and 2 (rounds 9 and 10).
- **Tone words:** "brittle" held 3 rounds (1-3), "wry" held 2 (4-5),
  "funereal" held 4 (6, 8, 9 and 10). The answer at round 7 carries
  no tone word and does not count toward the hold; the invitation at
  round 6 carries one like a free round (a static round would too).
- Built by script from the 2.1b rules with these draws (gaps 2, 3, 2;
  holds 3, 2, 4), not by hand — an earlier hand-drawn version in chat
  mislabeled a hold.

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
- **2026-09-23 (later still)** — §4 added: decision 4, where the cast
  sheet comes from — the owner's two messages verbatim (what "the
  bibles become its sections" means; then a template with visible
  placeholders, and many files for many stories), the agent's two
  answers condensed into one at the owner's request, and the ruling:
  a Jinja template with front matter and three placeholders,
  `stories/<story>/` with `episodes/` tracked in the fork, runs
  renamed to `runs/`, the cast moved into the story. §3.4 gets a
  dated note for the two knock-on changes.
- **2026-09-23 (night)** — §5 added: decision 5, the director — the
  whole exchange verbatim (the proposal, two rounds of the owner's
  questions and the agent's answers) and the ruling: no label on the
  instruction, events as "Offstage:", the addressed character
  answers the listener (model by default, narrowed by an exact name),
  three separate timers; the announcer voice parked in the roadmap.
  §5.7 turns it into build notes; the story's front matter gains
  `operator`.
- **2026-09-23 (night, later)** — §6 added: decision 6, the listener's
  turn — the whole exchange verbatim (one bridging remark absent from
  the transcript, noted), including two checks against the Whisper
  server through the tunnel; the ruling: the transcript filter,
  silence as the static round, the debug-only "Heard" text, the
  owner's radio-gauge idea for the polish list, the cast names as
  Whisper's `prompt`, `language=en` and `vad_filter=true`.
- **2026-09-23 (night, last)** — §7 added: decisions 1 and 7 together
  — the agent's proposal verbatim (revising its own agenda: a thin
  end-to-end skeleton first, then the rules, then the browser; what
  the checkpoint judges; the module layout; one pull request per
  slice) and the ruling. All seven decided; status DECIDED.
- **2026-09-24** — §8 added: the terms for a show's timeline, agreed
  while shaping step 2.1b — gap and hold replace the agent's casual
  "stretch" — with a timeline built by script from the 2.1b rules.
- **2026-09-24 (later)** — §5.7 gains a dated note: the static round's
  sentence became "Only static answers; the broadcast goes on." in
  step 2.1b, after the operator signed off in both live drives.
- **2026-09-24 (evening)** — §6.7 gains a dated note: as built in step
  2.4, the show reaches Whisper through its own route and a new client
  function, leaving upstream's `transcribe_audio` untouched.
