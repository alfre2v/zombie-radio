# Show engine design (Task 6b) — the seven decisions

**Date:** 2026-09-23 · **Arc:** MVP prototype · **Branch:**
`alfre2v/show-engine`
**Type:** discussion — the design of TalkWithZombies' show engine,
decided one question at a time before the code: the agent's agenda of
seven decisions (§1), then one section per decision as the owner
rules on it.
**Status:** OPEN — decisions 2 (the show's growing script), 3 (where
the show's record lives) and 4 (where the cast sheet comes from)
ruled 2026-09-23; decisions 1 and 5–7 pending.

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
