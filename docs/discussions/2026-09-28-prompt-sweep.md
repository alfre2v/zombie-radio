# The prompt sweep — every instruction the model receives, examined case by case

**Date:** 2026-09-28 · **Arc:** MVP prototype · **Branch:**
`alfre2v/show-slice-3`
**Type:** discussion — a working guide for examining, one case at a time,
every prompt the show sends to the model, in search of the best wording;
the owner leads the sweep, the agent explains what the model receives and
why, and builds what the owner decides.
**Status:** OPEN — three cases reviewed and changed on 2026-09-28 (the
event, the call, the Breakdown; the fork's `4d051ba`); every other case
still to examine (§5, the checklist).

**The owner's request (verbatim, 2026-09-28, 12:00):** "I want you to save
to a discussion file the output you produced in sections: "A. The
instruction for a round with a fixed line (app/show/director.py)" and "B.
How past rounds are replayed to the model (app/show/script.py, all
uncommitted today)". This document will guide me in sweeping the prompts
we provide to the model in different situations of the story. As of now
we only reviewed until `3. The Breakdown: director.py:320-321
(committed). Today, round 6`, but I want to continue until i have
examined each and every prompt case, in search of a optimal wording
together with you. Make the document wide and expressive, do not reduce
the details from the transcript, if anything expand the level of
details."

*Context for the cold reader.* The show engine (TODO Task 6b) lives in
the fork TalkWithZombies
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`). A director in
code plans each round of the radio play; a small model (Nemotron Nano 9B
v2, served by llama.cpp) writes the lines under a screenplay grammar.
**The model has no memory between requests.** Every request carries the
whole show so far as a conversation:

- **system** — the cast sheet: the premise, the four characters, and the
  format rule (`Name (emotion): spoken words`, one or two short sentences
  ending with "Over.");
- then, for every round kept in the script, a **user** turn — the
  director's instruction for that round — and an **assistant** turn —
  the lines the model wrote for it;
- and last, a **user** turn with the new round's instruction.

The model reads the whole conversation and continues it. **Fixed lines**
(step 3.4c.6, 2026-09-27) are lines the director writes itself and a
cast member says word for word — an event read out, the call, the
Breakdown's and the Switch-off's key line — so the listener hears them
for certain. How those lines appear in the conversation is what this
sweep started from. llama.cpp wraps the turns in the model's chat
template (`<SPECIAL_10>System`, `<SPECIAL_11>User`,
`<SPECIAL_11>Assistant`, `<SPECIAL_12>` between turns, and
`<think></think>` opening the reply, the model's "no thinking" mode).
With `debug: true` under `show:` in the fork's `settings.yaml`, each
round leaves `runs/<run-id>/debug/rNNN.txt` holding "the prompt as the
model read it", rendered by the server's own `/apply-template`, and a
token check against the size the server reported — so what this document
quotes as "the prompt" is what the model read, not a reconstruction.
Runs are the fork's `runs/<run-id>/` (kept on the laptop, not in git).

## 1. How the sweep started (2026-09-28, morning)

Step 3.4c.7 — keep fixed lines out of the model's own turns — was built
that morning after the owner's go ("It is a great idea. Let's implement
it. But before implementing, record well this idea and the reason why we
need to try this."; the idea and its evidence are in the TODO's 3.4c.7
entry). Before reviewing it, the owner stopped on one sentence it
introduced:

> **The owner (10:28):** "Wait, I do not like that you introduced the
> concept of a round to the nemotron LLM, I think that will confuse it
> more. Before doing any more changes, simulate for me a complete
> exchange and show me exactly what the model will receive as prompts."

The agent ran one real scripted contact on the box with debug on (the
fork's run `2026-09-28T10-28-57`: the sign-on, an event, the call, two
exchanges, the Breakdown, the aftermath, a call left unanswered to the
Switch-off) and showed round 11's prompt exactly as rendered (1829
tokens; the server read 1829). It confirmed the owner's worry and showed
a worse problem:

- **"round" reached the model twice**, both from the Breakdown's closing
  line — "Samantha closes the **round**, telling the listeners the lab can
  no longer hear them: do not say that for Samantha." (the Breakdown's
  instruction, committed the day before) and "Samantha closed that
  **round**, telling the listeners on air: "…"" (the replay, that
  morning's change). Nothing in the prompt ever tells the model what a
  round is; the system prompt speaks of "the script", "lines" and
  "transmissions". A model-free run of the director over 300 rounds found
  no other sentence with the word.
- **The call, folded into the next turn, read as an order to do it
  again.** With 3.4c.7 the call (which has no model line) joined the first
  exchange's user turn, worded in the present tense — "Daniel **tells**
  the listeners on air: "…" Then Samantha **calls out** to anyone
  listening: "…"" — the grammar of an order. The model obeyed it:
  "Samantha (excited): We've got the receiver—it's working! Over. /
  Daniel (relieved): Static's clearing. Over. / Moira (happy): Finally.
  Over." — and never answered "Hello? Is anyone there?".

The agent proposed rewording both; the owner:

> **The owner (10:40):** "I think we are doing a crappy job here. Stop
> modifying the model instructions. Instead I will do it case by case.
> How many places of prompt modifications with fixed lines do we have in
> the code? For each case, show me the file name, line number, and give
> me a short example of how the lines the model receive look form the
> actual run."

The agent listed eight places (sections A, B, C below) with short
examples; the owner asked for the full turns:

> **The owner (10:49):** "This is a good way to show me case by case, but
> the actual text you show of hoe the prompts look is not enough for me to
> make a decision. Show me more context (for each case you showed above, I
> want to see the full instruction that goes to the model in each case,
> committed and now). Other than that keep the same format you used
> above."

## 2. The eight places, as presented (verbatim, 10:49-10:52)

*The agent's output, in full. "Committed" is the fork at `07669dc`
(2026-09-27), taken from the owner's listen of 2026-09-27 (run
`2026-09-27T02-06-50`) and the check drive `2026-09-27T01-59-04`, their
messages rebuilt with the committed assembler — every round's
instruction as the user turn, all its lines, fixed ones included, as the
model's reply. "Now" is the uncommitted code of that morning (run
`2026-09-28T10-28-57`), rebuilt with the current assembler (its debug
prompt, token count matching the server's, confirms it). Line numbers are
those of that morning; §4 gives the current ones. Lines are wrapped for
reading; the words are exact. `USER` and `ASSISTANT` are the turns the
model reads; "→ the round, as said" is what the listener heard, `[fixed]`
marking the fixed lines. The file `cases.txt` sent to the owner held the
same text.*

**There are 8 places, in 3 files.** Four write the instruction for a
round that has a fixed line. Three decide how past rounds are replayed to
the model. One is the route, which says the fixed lines and records them.
Four of them are committed (`07669dc`, the day before). The replay
changes and the call's new quoting were that morning's uncommitted work,
and that morning's run used them.

### A. The instruction for a round with a fixed line (`app/show/director.py`)

**1. An event: `director.py:164-167`.** The wording is the same committed
and now; only the runs differ.

```
COMMITTED — the request, yesterday r2
USER (the last turn):
  Something happens that the listeners cannot see, and Ralph has just told them on air: "Footsteps cross the floor
  above, where the roof access was welded shut." Carry on from there. Samantha speaks first, then Ralph: the next
  two lines, each with the emotion in its voice, one of: sad, afraid, terrified, angry, exhausted. Let the tone
  be: haunted.
→ the round, as said:
  [fixed] Ralph (sad): Footsteps cross the floor above, where the roof access was welded shut. Over.
  Samantha (sad): The airlock's sealed. We can't move. Over.
  Ralph (angry): They're coming. We don't have time to count anymore. Over.

NOW — the request, today r2
USER (the last turn):
  Something happens that the listeners cannot see, and Moira has just told them on air: "The tissue in specimen
  jar seven is warmer than the room around it." Carry on from there. Ralph speaks next: the next line, with the
  emotion in its voice, one of: sad, afraid, terrified, angry, exhausted. Let the tone be: tight-lipped.
→ the round, as said:
  [fixed] Moira (terrified): The tissue in specimen jar seven is warmer than the room around it. Over.
  Ralph (afraid): Jar seven... it shouldn't be warm. Over.
```

With a budget of one line, only the quote remained and the model was not
asked (that morning's round 12: "…Moira has just told them on air: "The
antenna cable on the roof is swaying…"").

**2. The call: `director.py:240-241`.** It is never sent as a request,
since there is no model line. The model only meets it in later turns (see
7).

```
COMMITTED — yesterday r15
instruction:
  Something happens that the listeners cannot see: the lab has fixed the receiver, the part of the radio that
  hears. The receiver crackles back to life. Daniel tells the listeners on air, then Samantha calls out to anyone
  listening.
→ the round, as said:
  [fixed] Daniel (happy): We got the receiver running again. The static's clearing. Over.
  [fixed] Samantha (happy): We're listening now. Whoever hears this, answer us. Over.

NOW — today r3
instruction:
  Something happens that the listeners cannot see: the lab has fixed the receiver, the part of the radio that
  hears. The receiver crackles back to life. Daniel tells the listeners on air: "We got the receiver running
  again. The static's clearing." Then Samantha calls out to anyone listening: "We're listening now. Whoever hears
  this, answer us."
→ the round, as said:
  [fixed] Daniel (happy): We got the receiver running again. The static's clearing. Over.
  [fixed] Samantha (hopeful): We're listening now. Whoever hears this, answer us. Over.
```

**3. The Breakdown: `director.py:320-321`.** The wording is the same
committed and now.

```
COMMITTED — the request, yesterday r21
USER (the last turn):
  A voice on the frequency says: "Yes, everything is normal here. Do you guys have a UPS coordinate of the lab?"
  Earlier in this contact the voice said: "Hello, this is from Texas. What kind of problems are you guys
  experiencing?" / "My name is Captain Gonzalez of the Mounted Travellery" / "Sure, I can't relay a message. I
  could also provide some ammunition for you guys to fight the zombies." / "Yes, everything is normal here. We
  haven't heard any problem with zombies" / "Do you guys know your location?" The first line answers what the
  voice just said, speaking to them directly. Then something happens that the listeners cannot see: Smoke pours
  from the receiver, and it goes dead. The second line reacts to it. Samantha closes the round, telling the
  listeners the lab can no longer hear them: do not say that for Samantha. Moira speaks first, then Daniel or
  Ralph: the next two lines, each with the emotion in its voice, one of: sad, afraid, terrified, angry, exhausted.
  Let the tone be: gruesome.
→ the round, as said:
  Moira (sad): We have their coordinates—it's a mile east of the smoke. Over.
  Daniel (afraid): The radio's dead. Over.
  [fixed] Samantha (terrified): Smoke's pouring out of the receiver, it's dead! We can't hear you anymore, but
  we're still on the air. Over.

NOW — the request, today r6
USER (the last turn):
  A voice on the frequency says: "I'm in Austin, Texas, and I have a pickup truck." Earlier in this contact the
  voice said: "Hello? Is anyone there?" / "My name is Alfredo." The first line answers what the voice just said,
  speaking to them directly. Then something happens that the listeners cannot see: Smoke pours from the receiver,
  and it goes dead. The second line reacts to it. Samantha closes the round, telling the listeners the lab can no
  longer hear them: do not say that for Samantha. Ralph speaks first, then Daniel or Moira: the next two lines,
  each with the emotion in its voice, one of: sad, afraid, terrified, angry, exhausted. Let the tone be:
  inconsolable.
→ the round, as said:
  Ralph (sad): The receiver's gone. Over.
  Daniel (afraid): Smoke's everywhere. Over.
  [fixed] Samantha (exhausted): Sparks, and the receiver's gone dark. We can't hear anyone anymore, but keep
  listening: we're still on the air. Over.
```

**4. The Switch-off: `director.py:395-399`.** The wording is the same
committed and now.

```
COMMITTED — the request, drive 01-59-04 r24
USER (the last turn):
  Nobody answered the call. Samantha has just told the listeners on air: "Nobody's answering, so we're switching
  the receiver off to save power. We won't hear you until it's back on, but we're still on the air." The next line
  reacts to it. Daniel, Moira and Ralph speak next: the next line, with the emotion in its voice, one of: calm,
  doubtful, urgent, curious, determined. Let the tone be: forensic.
→ the round, as said:
  [fixed] Samantha (curious): Nobody's answering, so we're switching the receiver off to save power. We won't hear
  you until it's back on, but we're still on the air. Over.
  Daniel (determined): We'll keep the transmitter running. If anyone's out there, we'll find them. Over.

NOW — the request, today r11
USER (the last turn):
  Nobody answered the call. Samantha has just told the listeners on air: "No one's out there right now. We're
  turning the receiver off to save it, so we can't hear you until we switch it back on, but we keep broadcasting."
  The next line reacts to it. Daniel, Moira and Ralph speak next: the next line, with the emotion in its voice,
  one of: sad, afraid, terrified, angry, exhausted. Let the tone be: aching.
→ the round, as said:
  [fixed] Samantha (angry): No one's out there right now. We're turning the receiver off to save it, so we can't
  hear you until we switch it back on, but we keep broadcasting. Over.
  Daniel (sad): We'll try again later. Over.
```

### B. How past rounds are replayed to the model (`app/show/script.py`, all uncommitted that morning)

**5. The model's reply without the fixed line: `script.py:136-138`
(`reply_text`).**

```
COMMITTED — in yesterday's r24 request, the turns of r23
USER:
  Something happens that the listeners cannot see, and Moira has just told them on air: "A door that was locked an
  hour ago is standing wide open." Carry on from there. Daniel speaks next: the next line, with the emotion in its
  voice, one of: sad, afraid, terrified, angry, exhausted. Let the tone be: snide.
ASSISTANT:
  Moira (sad): A door that was locked an hour ago is standing wide open. Over.
  Daniel (angry): Of course it is. Over.

NOW — in today's r3+ requests, the turns of r2
USER:
  Something happens that the listeners cannot see, and Moira has just told them on air: "The tissue in specimen
  jar seven is warmer than the room around it." Carry on from there. Ralph speaks next: the next line, with the
  emotion in its voice, one of: sad, afraid, terrified, angry, exhausted. Let the tone be: tight-lipped.
ASSISTANT:
  Ralph (afraid): Jar seven... it shouldn't be warm. Over.
```

**6. The Breakdown's last line: `script.py:141-147` (`_said_after`).**

```
COMMITTED — in yesterday's r23 request: r21's reply, then r22's turns
ASSISTANT:
  Moira (sad): We have their coordinates—it's a mile east of the smoke. Over.
  Daniel (afraid): The radio's dead. Over.
  Samantha (terrified): Smoke's pouring out of the receiver, it's dead! We can't hear you anymore, but we're still
  on the air. Over.
USER:
  The voice on the frequency told you: "Hello, this is from Texas. What kind of problems are you guys
  experiencing?" / "My name is Captain Gonzalez of the Mounted Travellery" / "Sure, I can't relay a message. I
  could also provide some ammunition for you guys to fight the zombies." / "Yes, everything is normal here. We
  haven't heard any problem with zombies" / "Do you guys know your location?" / "Yes, everything is normal here.
  Do you guys have a UPS coordinate of the lab?" Talk among yourselves about what it means for you. Daniel, Ralph
  and Samantha speak next: the next three lines, each with the emotion in its voice, one of: sad, afraid,
  terrified, angry, exhausted. Let the tone be: gruesome.
ASSISTANT:
  Daniel (angry): We *knew* there was smoke from the east wing—why didn't they tell us sooner? Over.
  Ralph (afraid): If the receiver's dead, they might've overheard us. Over.
  Samantha (exhausted): We're broadcasting into the void now. Over.

NOW — in today's r8 request: r6's reply, then r7's turns
ASSISTANT:
  Ralph (sad): The receiver's gone. Over.
  Daniel (afraid): Smoke's everywhere. Over.
USER:
  Samantha closed that round, telling the listeners on air: "Sparks, and the receiver's gone dark. We can't hear
  anyone anymore, but keep listening: we're still on the air." The voice on the frequency told you: "Hello? Is
  anyone there?" / "My name is Alfredo." / "I'm in Austin, Texas, and I have a pickup truck." Talk among
  yourselves about what it means for you. Moira and Samantha speak next: the next three lines, each with the
  emotion in its voice, one of: sad, afraid, terrified, angry, exhausted. Let the tone be: inconsolable.
ASSISTANT:
  Moira (terrified): We can't reach them. Over.
  Samantha (afraid): Sparks… it's failing. Over.
  Moira (exhausted): Alfredo… we don't even know if they're alive. Over.
```

**7. The call joining the next user turn: `script.py:202-222`
(`assemble_messages`).**

```
COMMITTED — in yesterday's r17 request, the turns of r15 (the call) and r16 (the first exchange)
USER:
  Something happens that the listeners cannot see: the lab has fixed the receiver, the part of the radio that
  hears. The receiver crackles back to life. Daniel tells the listeners on air, then Samantha calls out to anyone
  listening.
ASSISTANT:
  Daniel (happy): We got the receiver running again. The static's clearing. Over.
  Samantha (happy): We're listening now. Whoever hears this, answer us. Over.
USER:
  A voice on the frequency says: "Hello, this is from Texas. What kind of problems are you guys experiencing?"
  Speak to the voice directly. Answer what the voice said, then: Find out who the voice is. If the voice already
  said their name, greet them by it and ask how they found this frequency. The last line asks the voice a
  question. Samantha speaks first, then Daniel, Moira or Ralph: the next three lines, each with the emotion in its
  voice, one of: happy, hopeful, excited, relieved. Let the tone be: madcap.
ASSISTANT:
  Samantha (happy): Hello! We're having a zombie siege and a broken radio. Over.
  Daniel (excited): We've fixed the receiver! We can talk now. Over.
  Moira (relieved): Who's this? Over.

NOW — in today's r5 request, the turns of r3 (the call) and r4 (the first exchange), joined
USER:
  Something happens that the listeners cannot see: the lab has fixed the receiver, the part of the radio that
  hears. The receiver crackles back to life. Daniel tells the listeners on air: "We got the receiver running
  again. The static's clearing." Then Samantha calls out to anyone listening: "We're listening now. Whoever hears
  this, answer us." A voice on the frequency says: "Hello? Is anyone there?" Speak to the voice directly. Answer
  what the voice said, then: Find out who the voice is. If the voice already said their name, greet them by it and
  ask how they found this frequency. The last line asks the voice a question. Samantha speaks first, then Daniel,
  Moira or Ralph: the next three lines, each with the emotion in its voice, one of: happy, hopeful, excited,
  relieved. Let the tone be: exultant.
ASSISTANT:
  Samantha (excited): We've got the receiver—it's working! Over.
  Daniel (relieved): Static's clearing. Over.
  Moira (happy): Finally. Over.
```

One thing only the full turns show: **even committed**, the first
exchange re-announced the fix ("We've fixed the receiver! We can talk
now."). It is worse now: nobody answers the voice at all.

### C. The source (`app/routers/show.py`, committed)

**8. Saying and recording the fixed lines: `routers/show.py:187-206`.**
Each fixed line is recorded in the model's own format, for example
`Daniel (happy): We got the receiver running again. The static's
clearing. Over.` In the committed code, that text is exactly what the
replay presents as the model's own reply: the `ASSISTANT` turns of 5 and
7 committed above. The route feeds a fixed line through the same parser
as the model's stream, so its raw text, its spoken text and its page
events are exactly a model line's, marked `fixed`.

## 3. The decisions of the sweep so far (2026-09-28)

### 3.1 Case 1, the event — (a) kept, (b) removed: an event round always leaves the model a line

> **The owner (10:53):** "Let's analyze the case (1) an event. Did you
> today modified in any way the prompt? (Except to remove the fixed
> line)? It does not seem to be different in visual inspection."

**The answer, with the diff:** no. The event's own instruction was
exactly what was committed — same text, same line numbers; that
morning's only change in the director was the call's instruction. For
events, the changes were only in how past event rounds are replayed, with
two effects:

- **(a)** an event round where the model also wrote lines: the fixed
  reading is removed from the replayed model reply (case 5); the event
  itself stays quoted in the user turn ("Ralph has just told them on air:
  "…"").
- **(b)** an event round with no model line (a budget of one): committed,
  it is replayed as the event's user turn plus an assistant turn holding
  only the fixed line; with 3.4c.7, it has no reply turn, and its
  instruction joins the next user turn, so the two instructions read as
  one. The owner's run of 2026-09-27, round 11, rebuilt both ways:

```
COMMITTED — in the r13 request, the turns of r11 (the event alone) and r12
USER:
  Something happens that the listeners cannot see, and Ralph has just told them on air: "A line of salt has been
  poured along the threshold of every door in the west wing."
ASSISTANT:
  Ralph (urgent): A line of salt has been poured along the threshold of every door in the west wing. Over.
USER:
  Daniel and Ralph speak next: the next line, with the emotion in its voice, one of: calm, doubtful, urgent,
  curious, determined. Let the tone be: inquisitive.
ASSISTANT:
  Daniel (calm): The salt's a barrier—something's avoiding it. Over.

NOW — in the r13 request, the same two rounds
USER:
  Something happens that the listeners cannot see, and Ralph has just told them on air: "A line of salt has been
  poured along the threshold of every door in the west wing." Daniel and Ralph speak next: the next line, with the
  emotion in its voice, one of: calm, doubtful, urgent, curious, determined. Let the tone be: inquisitive.
ASSISTANT:
  Daniel (calm): The salt's a barrier—something's avoiding it. Over.
```

> **The owner (10:57):** "I like (a) let's keep it. I do not understand
> (b). How can an event line have no model line? Show me that round 11
> (where above)?"

**The explanation.** A free round draws how many lines it gets from
`free_lines` [1, 2, 3, 4], weighted 1 : 3 : 3 : 1. When it draws 1 and an
event is due, the fixed reading used that one line, so the model was left
zero lines and not asked at all — the rule of the fixed-lines build ("the
fixed line counts within the round's drawn budget (1-4). A budget of 1 is
just the event read aloud, with no model call"). About one event round in
eight (here 1 of 9). Round 11 of the owner's run, from the record: kind
free, `max_lines` 0, no timings, no finish reason — the listener heard
only Ralph read the event; the reaction came in the next round, a plain
free round ("The salt's a barrier, something's avoiding it."). Three ways
were offered: keep (b) as it was (consistent with (a)); go back to the
committed replay for this case only (the model's reply then holds a line
it never wrote); or remove the case — an event round always leaves the
model at least one line.

> **The owner (10:58):** "3, the event round always leaves the model one
> line. Correct this."

**Built** (the fork's `4d051ba`): a drawn budget of 1 becomes 2 when an
event is due — the reading, then one reaction in the same round, opened by
the second speaker; budgets of 2-4 are unchanged. "At least one line" is
a rule, not a setting: the minimum that makes the round a reaction at
all. Case (b) no longer happens for events.

### 3.2 Cases 2 and 7, the call — told as already said, in the event's words, running on with "Then"

> **The owner (11:07):** "I am turning my attention to "2. The call:
> director.py:240-241" I see the problem now: Why are there 2 fixed lines?
> I do not like this, but do not change anything yet, just help me
> understand the implementation. Do we ever get 2 fixed lines in events?
> No, right?"

**The answer.** Events: never two. Each kind of round got its fixed lines
in exactly one place — the event one, before the model's lines (the
reading); the Breakdown one, after them (then); the Switch-off one,
before; the call **two, and no model line at all**. Why two: before fixed
lines, the call was already two lines (the owner's ruling on the receiver
story, the 3.4c discussion's §14.13: someone from the rest of the cast
says the receiver works, then Samantha's call, pinned last because the
listening window follows it); fixed lines made both fixed (decision 1 of
2026-09-27, "Go with all four as shown": the call is a functional moment,
like radio protocol, and fixing the announcement too ended
"\*crackle\*"); so the story's `beats.yaml` stores the call as pairs — an
announcement and a call — drawn without repeats, told apart by how the
receiver went off. The code (then `director.py:235-242`) picks the pool,
draws a pair, gives the announcement to whoever of Daniel, Moira and
Ralph has been silent longest, makes both lines with moods from the
call's overtone, and plans zero model lines: no grammar, no request, the
round takes about 0.35 s. Its instruction is written only for the record
and for replaying the history later. Consequences: the call never asks
the model; `beat_max_lines` no longer affects the call (the docstring and
the settings comment still said it did — the agent's inaccuracy); and,
because the model wrote nothing, replaying the call is awkward — case 7.

> **The owner (11:13):** "So, now, in the uncommitted code, The call round
> makes no request to nemotron. Right? Ok, I can leave with that. The model
> can improvise from there in the next free round."

**A correction:** the call is a listening round, so what comes next is not
a free round: an **exchange** if the listener answers, a **re-call** if
they are silent — and that request carries the call in its history. The
owner then asked for a plain, explanatory walk-through (11:16: "…I need
you to help me understand, be explanatory."), which the agent gave: after
a call, the first time the model "wakes up" is when it must respond to
the listener or to the silence; it reads the whole show as a
conversation; the call is something it never wrote, and the question is
how to present it. Committed, the call is replayed as the model's own
reply — clean in order, but telling the model it said what it did not,
the pattern removed for events in case 1 (a). With 3.4c.7, it joined the
next user turn in the present tense, which read as orders — the model
announced the receiver again. (To be fair to the new approach: even
committed, the first exchange once re-announced the fix.) Two options: go
back to the committed way for the call; or keep it out of the model's
turns but describe it as something that has already happened, in the past
tense, the way events already do.

> **The owner (11:20):** "Yes, (2) keep this approach, but "describe it
> as something that has already happened, in the past tense, the way the
> events already do", this is the key part, copy the formula of events,
> it seems to work there."

**Built:** the call copies the event formula word for word, and the old
present-tense stage direction ("…the lab has fixed the receiver, the part
of the radio that hears. The receiver crackles back to life.") goes —
"crackles" was the likely source of "\*crackle\*"; the announcement
already says what happened:

> Event: Something happens that the listeners cannot see, and Moira has
> just told them on air: "…" Carry on from there.
> Call: Something happens that the listeners cannot see, and Daniel has
> just told them on air: "…" Samantha has just called out to anyone
> listening: "…" Carry on from there.

> **The owner (11:26):** "I think in the case of calling out, the `Carry
> on from there` segment is wrong, instead we should put `Then `, because
> there are more events the model has to incorporate `A voice on the
> frequency says`"

**Built:** the call ends on "Then", and the assembler joins it into the
next user turn with the next text's first letter in lower case
(`script.py`, `_joined`: when a text ends in "Then", the text joined after
it starts in lower case; none of the instructions that can follow a call
starts with a name). The two continuations, rebuilt from the morning's
run with the same call drawn:

```
── the call, then the first exchange
   Something happens that the listeners cannot see, and Daniel has just told them on air: "We got the receiver
   running again. The static's clearing." Samantha has just called out to anyone listening: "We're listening
   now. Whoever hears this, answer us." Then a voice on the frequency says: "Hello? Is anyone there?" Speak to
   the voice directly. Answer what the voice said, then: Find out who the voice is. …

── the call, then the re-call (nobody answered)
   Something happens that the listeners cannot see, and Daniel has just told them on air: "The receiver's back!
   New fuse, fresh wiring, and it's picking up the band again." Samantha has just called out to anyone
   listening: "We can hear you again. Anyone listening, talk to us now." Then only static answers. Samantha
   calls out once more to anyone listening, asking them to answer now; the receiver is still on. …
```

"Then" makes the voice's answer, or the silence, the next event in the
same chain as the call; the instruction proper comes only after the whole
sequence of what happened.

### 3.3 Cases 3 and 6, the Breakdown — split in two: the last exchange, then the beat

> **The owner (11:28):** "yes, let's look at the Breakdown now. Give me
> again an example of how the prompt changed committed and now."

The agent showed the Breakdown's own request (the same wording committed
and now — the texts of case 3 above) and how it was replayed in the next
request (case 6 above), and noted that neither first line really answered
the listener (challenge C4 of the narration-quality discussion: the smoke
in the same instruction pulls the first line toward the failure).

> **The owner (11:39):** "These instructions are too complex and are
> confusing nemotron. The mistake we did here is to mix the breakdown
> round with an answer to the last user round (exchange). They should be
> separated completely. So, new adjustment to make: If the user has
> replied to the last message, and the time for a breakdown comes
> randomly, we still make round to answer to the user, normally, but then
> do not open the mic. Instead we go straight to a round that is only for
> the breakdown, this round could be made only from beat lines, or we can
> give the model some lines to react to the beat, this last seems more
> close to what we have right now. Do you understand? If so, give me a
> proposal to fix this (do not make any changes yet)"

**The proposal.** From the listener's side: (1) the last answer of the
contact, known by the count the director already keeps; (2) **the last
exchange** — the cast answer like any exchange (the character named first,
2-3 lines) but ask nothing (no agenda item, no "the last line asks the
voice a question") and the microphone does not open; (3) **the Breakdown**
straight after — the stage direction "[Smoke pours from the receiver, and
it goes dead.]", Samantha's fixed line, and the rest of the cast react.
Two plain instructions instead of one tangled one; everything about the
old Breakdown disappears ("Samantha closes the round… do not say that for
Samantha", "The first line answers… The second line reacts…", the fixed
line after the model's lines and with it "Samantha closed that round…");
every fixed line in the show then comes **first** in its round, quoted as
"has just told them". Three picks: the Breakdown takes Samantha's line
plus one reaction, like the Switch-off, both on `beat_max_lines`
(`breakdown_lines` goes); the RECEIVER sign stays lit through the last
exchange (a small page change: the round summary tells the page the
receiver is still on); the new kind of round is called `last-exchange`.

> **The owner (11:43):** "Go with your picks, build it."

**Built** (the fork's `4d051ba`): a new kind of round, `last-exchange`;
the director's rule "the N-th answer brings the last exchange, and the
round after a last exchange is always the Breakdown"; the Breakdown as a
receiver beat told like an event's reading; `breakdown_lines` removed;
the after-line mechanism removed from the director, the route and the
assembler; the round summary's `receiver`; the page's sign; a test that
no instruction in 200 rounds of a show contains the word "round". **One
real run on the box** (the fork's `2026-09-28T11-50-15`, the scripted
contact, debug on; round 12's prompt 1830 tokens, the server read 1830)
showed:

- **the first exchange after the call no longer re-announced the
  receiver** — "Samantha (excited): Hello! Over. / Daniel (relieved):
  We're alive. Over. / Moira (hopeful): Someone's here. Over." — thin, not
  finding out who the voice is, but no repeat (one sample);
- **the last exchange answered Alfredo directly, by name** — "Ralph
  (calm): Alfredo, we're in a lab under siege—you're in Austin? Over." —
  **but still asked questions** ("Do you have a radio?", "tell us what we
  should say"), the habit of every exchange before it, though the
  microphone does not open: an open point for the sweep (§4, case 11);
- **the Breakdown is one clean beat** — Samantha's line quoted as "has
  just told them on air", Daniel's reaction "We lost the receiver… Over."
  — and "round" is gone from every prompt.

## 4. The prompts as they stand now (the fork's `4d051ba`)

*Every case, in the order a show meets them. For each: the code (current
line numbers in the fork), its place in the sweep, the text exactly as
sent, and the model's reply where a run has one. Cases marked "run" come
from the fork's run `2026-09-28T11-50-15` (the request as sent, from its
debug files); cases marked "director only" come from the director
without the model (its instruction, and the fixed line where there is
one) because that run did not reach them. The notes under each case are
observations to take up when the sweep reaches it — not decisions.*

**Every request ends with the same tail**, written by `_turns`
(`director.py:770`) and `_count` (`director.py:760`) and the tone
sentence (`director.py:750`): who speaks ("Samantha speaks first, then
Daniel, Moira or Ralph", "Moira and Ralph speak next"), how many lines
("the next line", "the next three lines"), "each with the emotion in its
voice, one of: <the round's overtone's moods>", and "Let the tone be:
<tone word>." — every constraint the grammar enforces is also said in
words.

### 0. The system prompt — every request · to examine

The story's cast sheet (the fork's `stories/lab-outbreak/cast_sheet.md`)
with its premise and cast, and the format rule
(`app/show/rules/format_moods.md`), rendered once per run:

```
You write a live radio play. Four scientists are trapped in a besieged research lab during a zombie outbreak,
speaking over the lab's shortwave radio. The radio's receiver keeps failing: while it is down they can only
transmit, and when they get it working they call out for anyone listening to answer.

The cast:
- Daniel: Dr. Daniel Hayworth, systems engineer. Dry British understatement; competent, tired, quietly heroic.
- Moira: Dr. Moira Byrne, microbiologist. Irish lilt in her phrasing; grimly fascinated by the science of the
  outbreak, sometimes forgetting to be afraid.
- Ralph: Dr. Ralph Okafor, security officer. Deep, deliberate, a little paranoid; counts things (doors, cans,
  shamblers) because counting keeps him calm.
- Samantha: Dr. Samantha Reyes, communications lead running the broadcast. Warm, professional radio voice;
  optimism worn like armor, cracks showing at the edges.

Format: write the next lines of the script, one line per transmission, as `Name (emotion): spoken words`. The
emotion in parentheses is the one the listener should hear in the speaker's voice, exactly one of: happy,
hopeful, excited, relieved, calm, doubtful, urgent, curious, determined, sad, afraid, terrified, angry,
exhausted. Each transmission is one or two short spoken sentences ending with "Over." No narration, no
markdown, and nothing else in parentheses.
```

*Notes:* the cast are placeholders until the owner's character bibles
(Task 4); the model is told it writes "the script" in "lines" and
"transmissions" — the vocabulary the instructions may use; nothing about
the lab's location (see the narration-quality discussion, C7).

### 1. The sign-on — round 1 · `_orientation`, `director.py:192` (line 206) · to examine · run r1

```
USER (the last turn, exactly as sent):
  The broadcast begins. Samantha opens it and tells anyone listening, in their own words, that the lab's
  receiver is dead — they can only transmit, and will call out for listeners when it works — and who they are
  and where: Four scientists, Daniel, Moira, Ralph and Samantha, are trapped in a secret research lab, besieged
  by the dead since the outbreak began, and broadcasting on the lab's shortwave radio. The radio's receiver is
  dead: they can only transmit, not hear. When they get it working, they will call out for anyone listening, and
  whoever hears them can answer then. Samantha speaks first, then Daniel, Moira or Ralph: the next two lines,
  each with the emotion in its voice, one of: calm, doubtful, urgent, curious, determined. Let the tone be:
  stiff-upper-lip.
→ the round, as said:
  Samantha (urgent): We're broadcasting from Sector 9, Lab 7-B. The receiver's dead—we can only transmit. If you
  hear this, respond Over.
  Daniel (calm): Our power's holding, but the contamination levels are rising. Over.
```

*Notes:* present tense ("tells"), as an order — right here, since the
model is meant to write it; the receiver facts are given twice (the
"that the lab's receiver is dead…" clause and the story's facts); the
model invents "Sector 9, Lab 7-B" and ends with "If you hear this,
respond" while the receiver is dead — every seed-42 run opens with these
same words (narration-quality C7, C15).

### 2. The orientation repeat — every 20 ± 5 free rounds · `_orientation`, line 209 · to examine · director only

```
instruction:
  For listeners just tuning in, Ralph tells them, in their own words, that the lab's receiver is dead — they can
  only transmit, and will call out for listeners when it works — and who they are and where: Four scientists,
  Daniel, Moira, Ralph and Samantha, are trapped in a secret research lab, besieged by the dead since the
  outbreak began, and broadcasting on the lab's shortwave radio. The radio's receiver is dead: they can only
  transmit, not hear. When they get it working, they will call out for anyone listening, and whoever hears them
  can answer then. Ralph speaks first, then Daniel, Moira or Samantha: the next two lines, each with the emotion
  in its voice, one of: calm, doubtful, urgent, curious, determined. Let the tone be: rapid-fire.
```

*Notes:* the same body as the sign-on, opened by whoever has been silent
longest; a candidate for a fixed line, like the beats (C7).

### 3. A free round, plain — `_free`, `director.py:150` → `instruction_for` (`director.py:785`) · to examine · run r9

```
USER (the last turn, exactly as sent):
  Moira and Samantha speak next: the next three lines, each with the emotion in its voice, one of: sad, afraid,
  terrified, angry, exhausted. Let the tone be: apologetic.
→ the round, as said:
  Moira (sad): We can't reach him. Over.
  Samantha (afraid): The receiver's dead again. Over.
  Moira (exhausted): This is happening too fast. Over.
```

*Notes:* only the tail — the model carries on from the history; this is
where self-copying and echoes of the line before happen (C1, C2).

### 4. A free round with an event — `_free`, lines 173-180 · **reviewed** (case 1) · run r2

```
USER (the last turn, exactly as sent):
  Something happens that the listeners cannot see, and Moira has just told them on air: "The tissue in specimen
  jar seven is warmer than the room around it." Carry on from there. Ralph speaks next: the next line, with the
  emotion in its voice, one of: sad, afraid, terrified, angry, exhausted. Let the tone be: tight-lipped.
→ the round, as said:
  [fixed] Moira (terrified): The tissue in specimen jar seven is warmer than the room around it. Over.
  Ralph (afraid): Jar seven... it shouldn't be warm. Over.
```

*Status:* reviewed — the formula kept; the fixed reading out of the
replayed reply (case 5, (a)); always at least one model line. *Open
elsewhere:* the event texts as narration (the follow-up "Event texts
reworded as lines of dialog").

### 5. The aftermath — the first free round after a contact · `_free`, line 183 · to examine · run r8

```
USER (the last turn, exactly as sent):
  The voice on the frequency told you: "Hello? Is anyone there?" / "My name is Alfredo." / "I'm in Austin,
  Texas, and I have a pickup truck." Talk among yourselves about what it means for you. Moira and Ralph speak
  next: the next two lines, each with the emotion in its voice, one of: sad, afraid, terrified, angry,
  exhausted. Let the tone be: apologetic.
→ the round, as said:
  Moira (sad): We're trapped. Over.
  Ralph (afraid): If he's in Austin… Over.
```

*Notes:* "the voice on the frequency" is never said to be a listener who
called the lab; the aftermath has misread callers before (C9).

### 6. The recollection — every 15 ± 5 free rounds · `_free`, line 186 · to examine · director only

```
instruction:
  Earlier, a voice on the frequency told you: "Hello, this is Maria from Dallas." / "We have a doctor." / "Do
  you need medicine?" Talk among yourselves about what they told you, and imagine how they could help you if
  they call again. Daniel, Ralph and Samantha speak next: the next four lines, each with the emotion in its
  voice, one of: sad, afraid, terrified, angry, exhausted. Let the tone be: accusatory.
```

### 7. The call — `_repair`, `director.py:225` (lines 251-254) · **reviewed** (cases 2 and 7) · run r3 (not sent)

No request: two fixed lines. Its instruction exists for the replay, where
it joins the next user turn (8 and 13):

```
instruction (not sent; joins the next user turn):
  Something happens that the listeners cannot see, and Daniel has just told them on air: "We got the receiver
  running again. The static's clearing." Samantha has just called out to anyone listening: "We're listening now.
  Whoever hears this, answer us." Then
→ the round, as said:
  [fixed] Daniel (happy): We got the receiver running again. The static's clearing. Over.
  [fixed] Samantha (hopeful): We're listening now. Whoever hears this, answer us. Over.
```

### 8. The first exchange of a contact — `_exchange`, `director.py:290` (lines 303-305) · to examine · run r4

As sent, the call's text before it (7), joined with "Then":

```
USER (the last turn, exactly as sent):
  Something happens that the listeners cannot see, and Daniel has just told them on air: "We got the receiver
  running again. The static's clearing." Samantha has just called out to anyone listening: "We're listening now.
  Whoever hears this, answer us." Then a voice on the frequency says: "Hello? Is anyone there?" Speak to the
  voice directly. Answer what the voice said, then: Find out who the voice is. If the voice already said their
  name, greet them by it and ask how they found this frequency. The last line asks the voice a question.
  Samantha speaks first, then Daniel, Moira or Ralph: the next three lines, each with the emotion in its voice,
  one of: happy, hopeful, excited, relieved. Let the tone be: exultant.
→ the round, as said:
  Samantha (excited): Hello! Over.
  Daniel (relieved): We're alive. Over.
  Moira (hopeful): Someone's here. Over.
```

*Notes:* no longer re-announces the receiver (one sample), but thin: it
neither finds out who the voice is nor ends on a question; the agenda
item's two branches in one sentence ("Find out who the voice is. If the
voice already said their name, greet them by it and ask how they found
this frequency.").

### 9. An exchange later in the contact — `_exchange`, with `_restatement` (`director.py:488`, line 495) · to examine · run r5

```
USER (the last turn, exactly as sent):
  A voice on the frequency says: "My name is Alfredo." Earlier in this contact the voice said: "Hello? Is anyone
  there?" Speak to the voice directly. Answer what the voice said, then: Ask the voice whether they have a radio
  that can transmit, to relay the lab's calls further. If the voice already said what they have, ask them to
  repeat the lab's message on it. The last line asks the voice a question. Moira speaks first, then Daniel,
  Ralph or Samantha: the next three lines, each with the emotion in its voice, one of: calm, doubtful, urgent,
  curious, determined. Let the tone be: spellbound.
→ the round, as said:
  Moira (curious): Alfredo, can you hear us? Over.
  Daniel (determined): Do you have a transmitter? We need to relay this. Over.
  Ralph (calm): If you can't send it, describe how we can use your radio. Over.
```

*Notes:* Moira uses the name but answers nothing ("can you hear us?");
three questions in three lines.

### 10. An exchange that restates earlier callers — `_restatement`, line 498 · to examine · director only

```
instruction:
  A voice on the frequency says: "It's Alfredo again." Voices that reached you before, oldest first — 1: "Hello,
  this is Maria from Dallas." / "We have a doctor." / "Do you need medicine?" Only a voice that says the name of
  one of them is someone you spoke with before: greet them as a returning friend and use what they told you. Any
  other voice is someone new. Speak to the voice directly. Answer what the voice said, then: Find out who the
  voice is. If the voice already said their name, greet them by it and ask how they found this frequency. The
  last line asks the voice a question. Samantha speaks first, then Daniel, Moira or Ralph: the next three lines,
  each with the emotion in its voice, one of: happy, hopeful, excited, relieved. Let the tone be: triumphant.
```

*Notes:* the owner kept this wording on 2026-09-28 ("I reviewed the
`_restatement`, keep it as it is."); names-only A, which states who the
voice is, is ruled for the show fixes before the talk (C5 and the
follow-up "A listener memory keyed by identity").

### 11. The last exchange — `_last_exchange`, `director.py:310` (lines 322-323) · **reviewed** (built from case 3) · run r6

```
USER (the last turn, exactly as sent):
  A voice on the frequency says: "I'm in Austin, Texas, and I have a pickup truck." Earlier in this contact the
  voice said: "Hello? Is anyone there?" / "My name is Alfredo." Speak to the voice directly. Answer what the
  voice said. Ralph speaks first, then Daniel, Moira or Samantha: the next three lines, each with the emotion in
  its voice, one of: calm, doubtful, urgent, curious, determined. Let the tone be: spellbound.
→ the round, as said:
  Ralph (calm): Alfredo, we're in a lab under siege—you're in Austin? Over.
  Daniel (curious): Do you have a radio? We need to relay our location. Over.
  Moira (determined): If you can transmit, tell us what we should say. Over.
```

*Open:* it still asks questions — the habit of every exchange before it —
though the microphone does not open after it. Telling it outright ("ask
nothing, they cannot answer now") would be a new instruction sentence:
the owner's call.

### 12. The Breakdown — `_breakdown`, `director.py:328` (lines 342-345) · **reviewed** (built from cases 3 and 6) · run r7

```
USER (the last turn, exactly as sent):
  Something happens that the listeners cannot see, and Samantha has just told them on air: "The receiver just
  burned out. We can't hear you now, but we're still transmitting." Carry on from there. Daniel, Moira and Ralph
  speak next: the next line, with the emotion in its voice, one of: sad, afraid, terrified, angry, exhausted.
  Let the tone be: apologetic.
→ the round, as said:
  [fixed] Samantha (afraid): The receiver just burned out. We can't hear you now, but we're still transmitting.
  Over.
  Daniel (sad): We lost the receiver… Over.
```

### 13. The re-call before anyone answered — `_re_call`, `director.py:361` (line 373) · to examine · run r11

As sent, the second call's text before it, joined with "Then":

```
USER (the last turn, exactly as sent):
  Something happens that the listeners cannot see, and Daniel has just told them on air: "Good news: the
  receiver works again. We patched the burnt circuit." Samantha has just called out to anyone listening: "The
  receiver's on, so we can hear you. Please, answer." Then only static answers. Samantha calls out once more to
  anyone listening, asking them to answer now; the receiver is still on. Samantha speaks next: the next line,
  with the emotion in its voice, one of: calm, doubtful, urgent, curious, determined. Let the tone be: pedantic.
→ the round, as said:
  Samantha (calm): The receiver is functioning, but the input is only static. We must be precise—if you answer,
  we can confirm. Over.
```

*Notes:* "Samantha calls out once more…" is an order in the present
tense, as it should be (the model writes it); a candidate for a fixed
line (the call's second attempt is as functional as the first).

### 14. The re-call inside a contact — `_re_call`, line 379 · to examine · director only

```
instruction:
  The voice has gone quiet. Earlier in this contact the voice said: "Hello, this is Maria from Dallas." Daniel
  speaks to the voice, calls them by name if they gave one, and asks again: "Where are you? Over." Daniel speaks
  next: the next line, with the emotion in its voice, one of: calm, doubtful, urgent, curious, determined. Let
  the tone be: telegraphic.
```

*Notes:* the quoted question is the last line of the round before (here
the director-only run's placeholder "Where are you? Over."); never yet
heard by ear (C6).

### 15. The Switch-off, nobody answered — `_switch_off`, `director.py:386` (lines 402-413) · to examine · run r12

```
USER (the last turn, exactly as sent):
  Nobody answered the call. Samantha has just told the listeners on air: "Still nothing. We're switching off the
  receiver to spare it for later. We won't hear you for now, but we're still on the air." The next line reacts
  to it. Daniel, Moira and Ralph speak next: the next line, with the emotion in its voice, one of: sad, afraid,
  terrified, angry, exhausted. Let the tone be: haunted.
→ the round, as said:
  [fixed] Samantha (sad): Still nothing. We're switching off the receiver to spare it for later. We won't hear you
  for now, but we're still on the air. Over.
  Daniel (exhausted): We'll keep trying. Over.
```

*Notes:* the same shape as the event and the Breakdown, but not the same
words: it opens "Nobody answered the call." instead of "Something happens
that the listeners cannot see, and…", and closes "The next line reacts to
it." instead of "Carry on from there." — a candidate for the event
formula.

### 16. The Switch-off, the voice lost — `_switch_off`, line 402 · to examine · director only

```
instruction:
  The voice is gone. Samantha has just told the listeners on air: "We've lost you. We're switching the receiver
  off to save it for later. We won't hear you until it's back on, but we're still on the air." The next line
  reacts to it. Daniel, Moira and Ralph speak next: the next line, with the emotion in its voice, one of: calm,
  doubtful, urgent, curious, determined. Let the tone be: clipped.
  [fixed] Samantha (calm): We've lost you. We're switching the receiver off to save it for later. We won't hear
  you until it's back on, but we're still on the air. Over.
```

### 17. When fixed lines are off, or a story has no `beats.yaml` · to examine if kept

`fixed_lines: false` (or a story without `beats.yaml`) gives back the
model-written versions: the call (`_repair`, lines 255-265: "First, <the
rest> tells the listeners on air, in detail, what just happened to the
receiver: what they see and hear. Last, Samantha tells anyone listening,
in their own words: "We can hear you now. Answer us.""), the Breakdown
(`_breakdown`, lines 348-358: "Something happens that the listeners
cannot see: <the story's direction> The first line tells the listeners
on air, in detail, what is happening to the receiver: what they see and
hear. The last line tells them, in their own words: "We can't hear you
anymore, but we're still on the air.""), the Switch-off (lines 414-425),
and events worded by `event_report` (`instruction_for`: "Something
happens that the listeners cannot see: <event> The first to speak tells
the listeners on air what is happening." or "Offstage: <event>"). These
are the fallback, not the show; the sweep may decide whether they stay.

## 5. The checklist

| # | Case | Where (the fork, `4d051ba`) | State |
|---|---|---|---|
| 0 | The system prompt | `stories/lab-outbreak/cast_sheet.md`, `app/show/rules/format_moods.md` | to examine |
| 1 | The sign-on | `director.py:206` | to examine |
| 2 | The orientation repeat | `director.py:209` | to examine |
| 3 | A free round, plain | `director.py:150`, `instruction_for` 785 | to examine |
| 4 | A free round with an event | `director.py:173-180` | **reviewed** (case 1: (a) kept, (b) removed) |
| 5 | The aftermath | `director.py:183` | to examine |
| 6 | The recollection | `director.py:186` | to examine |
| 7 | The call | `director.py:251-254` | **reviewed** (cases 2 and 7) |
| 8 | The first exchange | `director.py:303-305` | to examine |
| 9 | A later exchange | `director.py:303-305`, `_restatement` 495 | to examine |
| 10 | An exchange restating earlier callers | `_restatement` 498 | wording kept by the owner; names-only A later |
| 11 | The last exchange | `director.py:322-323` | **reviewed** (new); open: it still asks questions |
| 12 | The Breakdown | `director.py:342-345` | **reviewed** (new) |
| 13 | The re-call before anyone answered | `director.py:373` | to examine |
| 14 | The re-call inside a contact | `director.py:379` | to examine |
| 15 | The Switch-off, nobody answered | `director.py:402-413` | to examine (case 4 of §2 shown, not decided) |
| 16 | The Switch-off, the voice lost | `director.py:402-413` | to examine |
| 17 | The fallbacks (fixed lines off) | `director.py:255-265, 348-358, 414-425` | to examine if kept |
| — | The replay: fixed lines out of the model's turns | `script.py:136` (`reply_text`), 193 (`assemble_messages`), 216 (`_joined`) | **reviewed** (case 5 (a) kept; case 6 gone with the split; case 7 with the call) |
| — | The route: fixed lines said and recorded | `routers/show.py:189-199` | shown (case 8); no change asked |
| — | The shared tail (who, how many, moods, tone) | `director.py:750, 760, 770` | to examine |

## 6. How a case is examined (the method of 2026-09-28)

1. **Look at the full turns, committed and now, from real runs** — never a
   description: the request exactly as sent (the debug files of a run with
   `debug: true`), and how the round is replayed in later requests
   (rebuilt from the run's record with the assembler of each version).
2. **Understand before deciding.** The agent explains the implementation
   and the history of the decision behind the wording (which ruling, which
   measurement); the owner asks until it is clear.
3. **The owner decides the wording**; the agent builds exactly that, with
   the tests pinning the new sentence.
4. **Check with a real run** — the scripted contact on the box with debug
   on, the prompt as the model read it (token count matching the
   server's), the model's replies read; nothing committed before the owner
   has seen it.
5. **Measure when a claim needs numbers** (the driver test and its counts,
   the experiments' conventions), and read the lines: counts miss
   phrasings and can count the reverse.

## 7. What the sweep has taught so far

- **The event formula works:** "Something happens that the listeners
  cannot see, and <name> has just told them on air: "…" Carry on from
  there." — something already said, quoted, in the past tense, then what
  to do now. The call and the Breakdown now use it.
- **Past tense for what already happened; the present only for what the
  model must do.** Present-tense descriptions of things already said read
  as orders, and the model obeys them (the call redone).
- **"Then" continues a chain of events** where more happens before the
  model speaks (the call, then the voice's answer or the silence).
- **One job per round.** An answer to the listener and the receiver's
  failure in one instruction confused the model; split, each is plain.
- **No words the model was never taught.** "Round" is the show's word, not
  the model's; the model knows "the script", "lines", "transmissions".
- **A fixed line is never the model's own line** in the replayed history —
  otherwise the model learns to repeat what it was just told.
- **The model carries habits across rounds:** after exchanges that end on
  a question, the last exchange asked questions too, though no instruction
  asked it to.
