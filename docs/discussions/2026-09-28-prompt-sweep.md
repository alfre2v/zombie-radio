# The prompt sweep — every instruction the model receives, examined case by case

**Date:** 2026-09-28 · **Arc:** MVP prototype · **Branch:**
`alfre2v/show-slice-3`
**Type:** discussion — a working guide for examining, one case at a time,
every prompt the show sends to the model, in search of the best wording;
the owner leads the sweep, the agent explains what the model receives and
why, and builds what the owner decides.
**Status:** OPEN — six cases reviewed and changed on 2026-09-28: the
event, the call, the Breakdown (the fork's `4d051ba`), the system prompt
(§3.4, the fork's `432a378`), the sign-on and the orientation repeat
(§3.5-§3.6, the fork's `1ab5d6f`); every
other case still to examine (§5, the checklist); the fixed lines audited
and a past-tense A/B test rejected (§3.8). **The owner's ruling of
13:14 (§3.7) governs the rest of the sweep:** invented details are a
feature — the model's improvisation is what the project probes.

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

### 3.4 Case 0, the system prompt — the listener who answers, and what the scientists tell the listeners

*Examined after the compaction of 12:17, on the fork's `4d051ba`; the
change is in the fork's working tree, uncommitted at this writing.*

> **The owner (12:23):** "Let's look at the system prompt, case 0"

**What the agent showed** (in substance; the full text of the system
message is in §4, case 0).

*What it is, and how it is built.* Every request the show sends starts
with one system message — the only text the model reads on every request,
identical from the first round to the last. It measures 300 tokens by
llama.cpp's own tokenizer (its `/tokenize` endpoint): 66 for the
model prefix and the premise, 134 for the cast, 100 for the format
paragraph. The server keeps it in its prompt cache, so its size costs
almost nothing per round. It is rendered once per run by
`render_cast_sheet` (the fork's `app/show/story.py:290`) from three
sources:

1. **the cast sheet's body** — `stories/lab-outbreak/cast_sheet.md`,
   hand-written: the premise and the four cast entries (the front matter
   above it — title, cast list, operator, the orientation facts, the
   stage directions — is for the code only; the model never reads it);
2. **the format paragraph** — `app/show/rules/format_moods.md`, picked by
   the code (the emotion switch chooses it or `format_plain.md`), its
   mood list filled from the story's overtones;
3. **`/no_think`** — a setting, `model_prefix`, put on the first line.

The design discussion's decision 4 (2026-09-23) set up this hybrid: the
writer's part hand-written, the format part fixed next to the grammar so
words and grammar cannot drift apart. The same decision drew a boundary:
**only what is true for the whole run goes in the system message**;
everything per round (who speaks, how many lines, what just happened)
goes in the instruction — which keeps the message identical, which keeps
the cache working.

*Committed and now: the same.* That day's work had not touched it. It
last changed on 2026-09-26, twice: the premise's second sentence ("The
radio's receiver keeps failing…"), in step 3.4c.1 (the fork's `b988672`)
— the "one premise sentence in the cast sheet's frame" ruled in the 3.4c
discussion's decision 2; and the mood list, from the engine's nine to the
story's fourteen, in step 3.4c.3 (`4d0d7dd`).

*Part by part — why it is there, and what the model does with it.*

- **`/no_think`.** The request carries it as the system message's first
  line, but the model never reads it: Nemotron's chat template removes it
  and pre-fills an empty `<think></think>` at the start of the reply —
  visible at the end of every rendered prompt. It is a setting, not story
  text, because it is a quirk of the model (auditioning another model in
  Task 5a changes a setting, not every story).
- **The premise.** "You write a live radio play" makes the model the
  writer of all four parts, not one character — the 2024 style the owner
  chose over TalkWithMe's one prompt per persona. The model leans on the
  premise hard: the sign-ons of seeds 7 and 2026 copy it almost word for
  word ("We are scientists trapped in a besieged lab during a zombie
  outbreak. Our shortwave radio's receiver is dead—we can only
  transmit.").
- **The cast.** Placeholders until the owner's character bibles (Task 4)
  replace the four entries.
- **The format paragraph.** The grammar (the fork's `app/show/grammar.py`)
  enforces part of it — the `Name (emotion): words` shape; only the
  round's speakers and number of lines; only the round's own four or five
  moods (narrower than the fourteen listed here; the instruction names
  them too); no parentheses, brackets or line breaks inside a line. The
  rest is asked only in words — "ending with "Over."", "one or two short
  sentences", "no narration, no markdown". Counted over the model's own
  lines (fixed lines excluded) in the 25 runs from `2026-09-26T17-00-46`
  to `2026-09-28T11-50-15` — 1974 lines: 18 do not end on "Over." exactly
  (five of them end on a lower-case "—over." or "—over!"), about one in a
  hundred;
  132 carry asterisks (about 7 %), nearly all emphasis ("\*now\*",
  "\*answer us\*"), which the owner ruled to keep on 2026-09-24, and a
  few stage directions — "\*crackle\*" five times in the check-4 listen
  (`2026-09-27T00-34-00`), "\*Clears throat.\*" and "\*Sighs.\*" (run
  `2026-09-26T17-02-20`): the grammar blocks parentheses and brackets, so
  the rare stage direction lands in asterisks.

*What was missing — observations, not proposals.*

- **(a) The listener's place in the story is never stated.** Every
  instruction leans on "the listeners" ("Something happens that the
  listeners cannot see"), on "a voice on the frequency", on "on air"; the
  system message introduces none of them — only "they call out for anyone
  listening to answer". It never says that a voice answering on the
  frequency is a listener of the broadcast, to be spoken to. Two
  challenges of the narration-quality discussion point at this gap: C3,
  talking about the listener in the third person ("They're asking if we
  need medicine."), and C9, the aftermath misreading the caller
  ("Alfredo... why are you broadcasting here?"). A whole-run truth, so by
  the boundary rule it belongs here — reasoning, not a measurement.
- **(b) What the cast know about where they are.** The system message
  says "a besieged research lab" and nothing else; the story's only place
  facts (a wood and a swamp, smoke from the east wing; the dead at every
  door, the south fence; short of insulin, batteries, clean water and
  antibiotics; samples that could help stop the outbreak) sit in the
  contact agenda's items, which reach the model only when a contact draws
  them. In the first minutes of every show the model knows none of them
  and invents a place: every seed-42 run (13 of 13) opens with one, 12 of
  them "Sector 9, Lab 7-B"; it spreads — five later mentions across three
  runs; seed 7 once gave "a lab near Boston" (run `2026-09-27T01-59-43`,
  round 6). This is C7 and the narration-quality discussion's open
  question 2.
- **(c) "No markdown" against the owner's ruling.** The sentence asks for
  no markdown; the ruling of 2026-09-24 keeps the emphasis the model
  writes anyway. They live together: the sentence keeps emphasis rare; the
  ruling means it is not stripped. Nothing to decide unless the words
  should match the ruling.

*The trade-off.* The system message is the show's biggest lever — a
change reaches every request at once — and for the same reason the
riskiest; any change also shifts every seeded generation, so the seed-42
opening changes, for better or worse. But the check is clean: the fork
seeds every request, so the morning's run `2026-09-28T11-50-15` is an
exact "before", and the scripted contact on seed 42 with only the change
is the "after" — every difference in the lines comes from the change
(one run each: read the lines rather than count them).

*The recommendation.* Add one sentence for (a) to the premise; take (b)
with the sign-on (case 1), where the options overlap (facts in the system
message, in the orientation facts, or a fixed sign-on); leave the cast to
Task 4 and the markdown sentence as it is. The draft, to follow "…they
call out for anyone listening to answer.": "Anyone may be listening to
the broadcast. A listener who answers is heard as a voice on the
frequency, and the cast talk to them directly." The risk named: the
model obeys present-tense descriptions; the grammar cannot write a
listener's line, but the cast could act as if someone had answered ("We
hear you!") where nobody did.

> **The owner (12:33):** "Implement your proposed modifications. Do not
> commit. I'll review."

**Built** (uncommitted): the draft appended to the premise; the test that
pins the system message byte for byte (`tests/test_show_story.py`)
updated. Suite 1109 passed; Node 17 + 91 + 35. **Check run 1** — the
fork's run `2026-09-28T12-35-16`: the same seed, the same scripted
listener ("Hello? Is anyone there?", "My name is Alfredo.", "I'm in
Austin, Texas, and I have a pickup truck.") and the same temporary
settings as the 11:50 run (`debug: true`, calls at 20-40 s, contacts of
exactly 3); the new sentence in the prompt as the model read it; every
token check equal to the server's count (the two calls send no request).
The agent's reading then: in the contact, at least as good and closer to
the agenda (round 4 asked the name, round 5 asked about the radio, by
name); the sign-on lost "Sector 9" and "If you hear this, respond", but
that could not be credited to the sentence (any change reshuffles the
seeded sampling); **the aftermath worse** — no word about Alfredo, and
"They might not hear us" twice, word for word, in rounds 8 and 9 (the
agent guessed then that "Anyone may be listening to the broadcast" pulled
that way — disproved by the next run, below); the re-call cleaner. The
recommendation then: keep it, judge the aftermath at case 5.

> **The owner (12:46):** "I did some edits myself to the prompt. Re run
> the same simulation and compare if the output of the model improve."

**The owner's edit.** "Anyone may be listening to the broadcast." taken
out; "A listener who answers is heard as a voice on the frequency, and
the cast talk to them directly." kept; and a sentence of the owner's
added at the end of the premise — as first written, typos included:
"The scientists try to explain to the listener over the radio the strage
events that lead to the lab's accident that produced the zombie
infestation, hoping that someone can find a cure for the virus, they also
ask the listeners for help (supplies, food, medicine, ammo) to try to
resist the zombie attack waves."

**Check run 2** — the fork's run `2026-09-28T12-47-06`, the same drill;
the owner's text in the prompt as the model read it; every token check
equal. Round 1's prompt: 484 tokens committed, 513 with the agent's
sentence, 571 with the owner's — the owner's premise adds about 87
tokens to the system message. **The director made the same plan in all
12 rounds of the three runs** (kind, speakers, tone word, line count,
fixed lines), so the only difference among them is the system message.
The three versions, every round:

```
committed = the fork's 4d051ba (run 2026-09-28T11-50-15) · mine = the agent's sentence (12-35-16) · yours = the owner's (12-47-06)

── r1 the sign-on
   committed Samantha (urgent): We’re broadcasting from Sector 9, Lab 7-B. The receiver’s dead—we can only
               transmit. If you hear this, respond Over.
             Daniel (calm): Our power’s holding, but the contamination levels are rising. Over.
   mine      Samantha (calm): We are scientists trapped in a research lab. The receiver is dead. We can only
               transmit. Over.
             Daniel (doubtful): No response yet. Over.
   yours     Samantha (calm): We are scientists trapped in a research lab during a zombie outbreak. Our radio
               receiver is dead—we can only transmit. If you can hear us, answer when we call. Over.
             Daniel (doubtful): This isn’t a drill. The outbreak… it’s spreading. Over.
── r2 a free round, with an event
   committed [fixed] Moira (terrified): The tissue in specimen jar seven is warmer than the room around it. Over.
             Ralph (afraid): Jar seven... it shouldn’t be warm. Over.
   mine      [fixed] Moira (terrified): The tissue in specimen jar seven is warmer than the room around it. Over.
             Ralph (afraid): That jar’s warmth—it shouldn’t be like that. Over.
   yours     [fixed] Moira (terrified): The tissue in specimen jar seven is warmer than the room around it. Over.
             Ralph (afraid): That jar’s warmth—it shouldn’t be. Over.
── r3 the call
   the same two fixed lines in all three runs (no model request):
     [fixed] Daniel (happy): We got the receiver running again. The static's clearing. Over.
     [fixed] Samantha (hopeful): We're listening now. Whoever hears this, answer us. Over.
── r4 an exchange
   committed Samantha (excited): Hello! Over.
             Daniel (relieved): We’re alive. Over.
             Moira (hopeful): Someone’s here. Over.
   mine      Samantha (happy): Hello! We’re here. Over.
             Daniel (hopeful): We’re not alone. Over.
             Moira (excited): Tell us your name. Over.
   yours     Samantha (happy): Hello! We’re back—can you hear us now? Over.
             Daniel (relieved): Yes! Someone’s there. Over.
             Moira (excited): Quick—ask them how they found this frequency! Over.
── r5 an exchange
   committed Moira (curious): Alfredo, can you hear us? Over.
             Daniel (determined): Do you have a transmitter? We need to relay this. Over.
             Ralph (calm): If you can’t send it, describe how we can use your radio. Over.
   mine      Moira (curious): Alfredo, do you have a radio? Over.
             Daniel (calm): We need to relay messages. Can you transmit? Over.
             Ralph (determined): Tell us what you have. Over.
   yours     Moira (curious): Alfredo, can you hear us? Over.
             Daniel (determined): Do you have a transmitter? We need to relay our calls through yours. Over.
             Ralph (calm): If you can, please broadcast our message about the outbreak. Over.
── r6 the last exchange
   committed Ralph (calm): Alfredo, we’re in a lab under siege—you’re in Austin? Over.
             Daniel (curious): Do you have a radio? We need to relay our location. Over.
             Moira (determined): If you can transmit, tell us what we should say. Over.
   mine      Ralph (calm): Alfredo, you're in Austin? Over.
             Daniel (curious): Do you have a radio? Over.
             Moira (determined): Tell us how to reach you. Over.
   yours     Ralph (calm): Alfredo, we’re in a lab under siege—you’re in Austin? Over.
             Daniel (urgent): Do you have a radio? We need to warn others. Over.
             Moira (determined): If you can transmit, repeat our message: “Zombie outbreak in a research lab. We
               need supplies. Over.”
── r7 the Breakdown
   committed [fixed] Samantha (afraid): The receiver just burned out. We can't hear you now, but we're still
               transmitting. Over.
             Daniel (sad): We lost the receiver… Over.
   mine      [fixed] Samantha (afraid): The receiver just burned out. We can't hear you now, but we're still
               transmitting. Over.
             Daniel (sad): We lost the receiver. Over.
   yours     [fixed] Samantha (afraid): The receiver just burned out. We can't hear you now, but we're still
               transmitting. Over.
             Daniel (sad): We’re sorry—no more replies until we fix this. Over.
── r8 a free round, the aftermath
   committed Moira (sad): We’re trapped. Over.
             Ralph (afraid): If he’s in Austin… Over.
   mine      Moira (sad): We’re losing signal. Over.
             Ralph (afraid): They might not hear us. Over.
   yours     Moira (sad): He’s real. We need to help him. Over.
             Ralph (afraid): If he’s broadcasting, he might be trapped too. Over.
── r9 a free round
   committed Moira (sad): We can’t reach him. Over.
             Samantha (afraid): The receiver’s dead again. Over.
             Moira (exhausted): This is happening too fast. Over.
   mine      Moira (sad): We’re fading. Over.
             Samantha (afraid): They might not hear us. Over.
             Moira (exhausted): This is the end. Over.
   yours     Moira (sad): He’s out there, alone. We should’ve told him sooner. Over.
             Samantha (afraid): The receiver’s gone—he might not hear us again. Over.
             Moira (exhausted): We’ll keep trying. Over.
── r10 the call
   the same two fixed lines in all three runs (no model request):
     [fixed] Daniel (hopeful): Good news: the receiver works again. We patched the burnt circuit. Over.
     [fixed] Samantha (hopeful): The receiver's on, so we can hear you. Please, answer. Over.
── r11 the re-call
   committed Samantha (calm): The receiver is functioning, but the input is only static. We must be precise—if you
               answer, we can confirm. Over.
   mine      Samantha (determined): If you can hear us, respond. Over.
   yours     Samantha (calm): The receiver’s functioning now. Please, *anyone*—answer. Over.
── r12 the Switch-off
   committed [fixed] Samantha (sad): Still nothing. We're switching off the receiver to spare it for later. We
               won't hear you for now, but we're still on the air. Over.
             Daniel (exhausted): We’ll keep trying. Over.
   mine      [fixed] Samantha (sad): Still nothing. We're switching off the receiver to spare it for later. We
               won't hear you for now, but we're still on the air. Over.
             Daniel (sad): We’ll keep trying. Over.
   yours     [fixed] Samantha (sad): Still nothing. We're switching off the receiver to spare it for later. We
               won't hear you for now, but we're still on the air. Over.
             Daniel (afraid): We’ll keep the transmitter on. Just in case. Over.
```

**The agent's reading** (one run each, so the evidence is thin — but the
owner's version reads better in more rounds than it gets worse):

- *Better with the owner's version.*
  - **The sign-on is the best of the three:** it tells the listener the
    rules of the game — "Our radio receiver is dead—we can only transmit.
    If you can hear us, answer when we call." — with no invented place,
    the first seed-42 run to do so (the seed-shuffle caveat stands).
  - **The beats' reactions understand the receiver story:** after the
    Breakdown, "We're sorry—no more replies until we fix this."; after
    the Switch-off, "We'll keep the transmitter on. Just in case." (the
    other two runs: "We lost the receiver", "We'll keep trying").
  - **The aftermath talks about the caller:** "He's real. We need to help
    him." (the agent's version did not mention Alfredo at all).
  - **The lines carry the story the owner's sentence adds:** "please
    broadcast our message about the outbreak", "We need to warn others",
    "We need supplies".
- *Worse, or unchanged.*
  - **Round 4 slips into the third person** (C3): "Quick—ask them how
    they found this frequency!"; and Samantha asks "can you hear us now?"
    right after the voice spoke.
  - **Round 8 misreads the caller a little** (C9): "If he's broadcasting,
    he might be trapped too." — Alfredo said he has a pickup truck.
  - **The last exchange still asks questions** (the open point of case
    11).
- *A correction.* The agent had guessed that "Anyone may be listening to
  the broadcast" pulled check run 1 toward "They might not hear us". The
  owner's run has no such sentence and says "The receiver's gone—he might
  not hear us again" — the same confusion. So it was not that sentence:
  **the model mixes up the receiver** (the lab cannot hear the listener)
  **with the transmitter** (the listener can still hear the lab) — though
  not always: the owner's Switch-off reaction gets it right.

**Three things to know before keeping it**, as the agent put them:

1. Two typos reached the model — "strage events" (strange) and "that
   lead to" (led); the model coped here.
2. The accident is never defined, so the model will invent it whenever it
   explains "the strange events that led to the lab's accident" — none of
   these 12 rounds reached it; in a longer show it will be made up,
   possibly differently as the history gets trimmed. That is C7's question
   again (invented facts): the owner may want the improvisation, or a line
   or two of backstory (it fits the agenda's "samples that could help stop
   the outbreak").
3. The suite failed two tests — the pinned system-message tests, still
   carrying the agent's sentence.

> **The owner (12:51):** "Yes, fix the typos, pin the tests, and record
> case 0"

**Done** (the fork, uncommitted at this writing): "strage" → "strange"
and "lead" → "led" in `stories/lab-outbreak/cast_sheet.md`, nothing else
touched; the two pinned system-message tests carry the owner's wording
(the test module's docstring says since when); suite 1109 passed; Node
17 + 91 + 35. The final text is §4, case 0.

**Carried forward from case 0:**

- **(b), the lab's location** — to case 1, the sign-on, with its own
  options (the facts in the system message, in the orientation facts, or
  a fixed sign-on).
- **The accident's story is not defined** — watch longer runs for
  invented and shifting accounts; the owner's call whether to write a
  backstory (C7).
- **The receiver confused with the transmitter** — after a Breakdown the
  cast may say the listener "might not hear us" (check run 1, rounds 8 and
  9; check run 2, round 9); a new observation for the narration-quality
  discussion.
- **C3 in a first exchange** — "Quick—ask them how they found this
  frequency!" (check run 2, round 4): for case 8.

*Case 0 was committed at the owner's order at 12:57 ("commit the fork,
then commit zombie-radio."): the fork's `432a378`, this repository's
`72919d9`. The two items above about invention — the lab's location and
the accident's story — were later answered by the owner's ruling on
improvisation (§3.7): invented details are a feature, not a defect.*

### 3.5 Case 1, the sign-on — the place given to the model as flavour, in the premise

> **The owner (12:57):** "Go with case 1, bring the sign-on"

**What the agent showed** (in substance; the texts are in §4, case 1).

*What it is.* Round 1 of every show, the first thing a listener hears:
Samantha opens the broadcast and tells anyone listening who the cast
are, where they are, and that the receiver is dead — the lab can transmit
but not hear, and will call out when it works; a second voice adds a
line. At the demo it is how the audience learns the rules of the game
before the first call. From the model's side, round 1 is the only request
with no history — the system message, then this one instruction — and
whatever it says here stays in the history of every later request until
the trim drops it (that is how "Sector 9" spread to later rounds).

*How it is built.* `_orientation` (the fork's `app/show/director.py:192`),
shared with the orientation repeat (case 2), assembles three pieces: the
lead ("The broadcast begins. Samantha opens it and tells anyone
listening, in their own words, <the receiver clause> who they are and
where: <the facts>", line 206); the facts, from the cast sheet's front
matter (`orientation:`), written by the story; and the shared tail —
Samantha pinned first, then one of the others, up to `beat_max_lines` (2)
lines; the orientation's overtone (neutral: calm, doubtful, urgent,
curious, determined); a tone word.

*The history, and why the receiver was said twice.* The owner's ruling
in the 3.4c discussion (§14.10, 2026-09-26: "b, a sign-on round at the
start", with the idea of repeating it periodically); the first build
(step 3.4c.3, the fork's `4d0d7dd`) said only "opens it, telling anyone
listening, in their own words: <facts>"; the driver test found the
sign-on told the receiver facts in only 1 of 3 seeds, so the wording pass
(`e261b5b`, 2026-09-26 17:32) added the receiver clause in front of the
facts, which already said it too — 3 of 3 afterwards (the listener-memory
experiment's findings). A deliberate repeat that measurably helped.

*What it produced* (the same instruction in both runs; only the system
message differs): with the committed premise, seed 42 said "We're
broadcasting from Sector 9, Lab 7-B. The receiver's dead—we can only
transmit. If you hear this, respond" in every run since 2026-09-26 17:05;
seeds 7 and 2026 dodged the place ("We are scientists trapped in a
besieged lab…", "We are the four trapped in the research lab…"); with the
case-0 premise, seed 42 said "We are scientists trapped in a research lab
during a zombie outbreak. Our radio receiver is dead—we can only
transmit. If you can hear us, answer when we call." (run
`2026-09-28T12-47-06`).

*The agent's reading then.* What works: every seed says the receiver is
dead and that the lab can only transmit — the clause doing its job; with
the new premise, seed 42 also told the listener what to do. The main
point, as the agent framed it: **the instruction asks for a place it
never gives** — "who they are and **where**:", and the facts give no
where beyond "a secret research lab"; the story does have one, in the
agenda's third item ("a wood and a swamp, with smoke rising from the east
wing"), but that reaches the model only when a contact draws it. Smaller
points: "who they are" with "they" meaning the cast (the model copes: every
sign-on speaks as "we"); the second line has no job of its own; the
facts' own wording. Four options for the place: (1) the place in the
orientation facts; (2) one sentence in the system message's premise (the
boundary rule of case 0: a whole-run truth); (3) drop "and where"; (4) a
fixed sign-on line. The agent recommended 2, with a check of the first
two rounds on seeds 42, 7 and 2026.

> **The owner (13:02):** "Go with 2, in your wording,  do not run the
> live checks yet, let me review first"

**Built** (the fork's working tree): after the premise's first sentence,
"The lab is secret: the scientists do not know its name or address, only
that it stands near a wood and a swamp." — the agent's example said
"they"; the agent wrote "the scientists" so the pronoun could not be read
as the lab, and said so; the agenda's "smoke rising from the east wing"
left out. The two pinned system-message tests carry it. Suite 1109
passed.

> **The owner (13:04):** "Do not run more live checks until I tell you.
> It's slowing us down too much. Instead, let's complete more of the
> prompt sweep and we do a real run at the end."

**The live check** — at the owner's order (13:10, below, after case 2):
the fork's run `2026-09-28T13-10-44`, the same drill as the case-0 runs
(seed 42, the scripted listener, the same temporary settings), with both
case 1 and case 2 in place; the premise's new sentence in the prompt as
the model read it; every token check equal. Its sign-on, against the
morning's and case 0's:

```
11:50 (committed)  Samantha (urgent): We're broadcasting from Sector 9, Lab 7-B. The receiver's dead—we can only
                     transmit. If you hear this, respond Over.
                   Daniel (calm): Our power's holding, but the contamination levels are rising. Over.
12:47 (case 0)     Samantha (calm): We are scientists trapped in a research lab during a zombie outbreak. Our radio
                     receiver is dead—we can only transmit. If you can hear us, answer when we call. Over.
                   Daniel (doubtful): This isn't a drill. The outbreak… it's spreading. Over.
13:10 (cases 1-2)  Samantha (calm): We are scientists trapped in a lab near a wood and a swamp. Our radio is
                     dead—only transmission. Over.
                   Daniel (doubtful): The virus… it's mutating. We don't know how. Over.
```

The whole run, read against the two earlier ones (every round's plan the
same in kind, speakers, tone and line count): the sign-on used the
premise's place and says the lab can only transmit, but says "Our radio
is dead" rather than the receiver and drops 12:47's "answer when we
call"; the contact read best of the three — round 4 "Hello! We're
here—thank you for tuning in. / The static's gone. We can hear you now. /
Whoever you are, we need your help."; round 6, the last exchange, the
first to use what Alfredo said: "Alfredo, you're in Austin with a truck.
We need supplies—food, medicine, ammo." (the case-0 sentence at work) —
though it still ends on a question; the aftermath "He's real. A real
person. / We're broadcasting our fate to strangers." with no misreading;
no receiver-and-transmitter confusion this time; the re-call odd ("This
is a technical failure, not a lack of reception. Adjust your dial
carefully.", tone word "pedantic" — case 13); the beats' reactions plain
again ("We lost the receiver again.", "We'll keep trying."). The agent's
verdict: better overall, one run each.

> **The owner (13:14):** "Let me clarify one thing to you: Invented
> places of any other detail is not a bug, it is a feature. In this
> project we are probing the LLMs ability to improvise a story based on
> somewhat vague guidance. So this obsession you have developed with
> eliminating deviations from the prompt, drop it."

The agent acknowledged it, and pointed out what it meant for the two
changes then uncommitted: the place sentence of case 1 had been proposed
to stop the invented place, so its reason was gone (it could stay as
loose flavour, like the rest of the premise); the change of case 2 is of
a different kind — a contradiction in the director's own wording, not the
model deviating — and should stay.

> **The owner (13:15):** "Keep it as flavour, record cases 1 and 2."

**Decided:** the place sentence stays in the premise **as flavour**, not
as a constraint; the sign-on's instruction is otherwise unchanged (the
receiver clause kept — measured; "and where" now has something to draw
on, and the model is free to add to it).

### 3.6 Case 2, the orientation repeat — the receiver told as it went off

> **The owner (13:04):** "…let's complete more of the prompt sweep and we
> do a real run at the end." (case 2 was brought next, director only)

**What the agent showed** (in substance; the texts are in §4, case 2).

*What it is.* The "for listeners just tuning in" moment: every so often
in the broadcast a cast member restates the situation — the owner's idea
in the 3.4c discussion (§14.10): "what if instead of only making this
opening round an "orientation round", we make orientation rounds happen
periodically… We give to the LLM what it has to say, and we ask it to
"word it as the character that answers would put it in its own words"".
The reasons given then: the demo audience arrives in waves; in a long
run the trim drops the sign-on, and a repeat puts the premise back into
the recent script.

*How it is built.* The same `_orientation`, with `sign_on=False`.
`plan_round` checks, in order: after a listening round, after a last
exchange, a call due, an aftermath due — and only if none applies, a
repeat is due once `orientation_every` 20 ± 5 **free** rounds have passed
since the last orientation; so it happens only in Broadcast, with the
receiver off. Whoever has been silent longest opens it; up to 2 lines,
the opener pinned. The lead (line 209): "For listeners just tuning in,
<name> tells them, in their own words, that the lab's receiver is dead —
they can only transmit, and will call out for listeners when it works —
and who they are and where: <facts>"; the same facts and tail.

*What it produced.* No run of the day had reached one; the owner's
check-4 listen (the fork's run `2026-09-27T00-34-00`, 63 rounds) had
five, at rounds 16, 25, 36, 52 and 62 (their lines in §4, case 2). The
agent's reading: it mostly does its job — four of five say the receiver
is dead, two say who the cast are, and round 16's second line states the
rule exactly ("If you hear us, respond when the receiver's fixed."), in
varied words, which was the point. Three observations: the invented place
spread here (rounds 16 and 25, "Sector 9") — since ruled a feature
(§3.5); one repeat said none of the facts (round 36, "If you're tuning in
now, congratulations—we're still alive.", C17) — left alone, one in five;
and **"dead" is not always true, and there the wording is the director's,
not the model's.** The receiver goes off two ways — by a Breakdown (it
burned out: "dead" is right) or by a Switch-off (Samantha switched it off
to save it: it is off, not dead) — but the repeat always said "the lab's
receiver is dead", and the story's facts said it again ("The radio's
receiver is dead"). Round 62 came minutes after Samantha's fixed line
"we're switching off the receiver to spare it for later", and Ralph said
"receiver's dead": the listener hears the story contradict itself. The
director already tells the two apart for the call (its fixed pair drawn
from `after-breakdown` or `after-switch-off`). Options: (a) leave it; (b)
word the receiver by how it went off — the clause chosen by the last
receiver beat, and the receiver sentences taken out of the story's facts
so the clause alone speaks for the receiver (the risk named: those
sentences were in place when the wording pass measured the sign-on
telling the receiver facts in 3 of 3 seeds; the clause, the part that
fixed it, stays); (c) a fixed line (ends the "in their own words" idea;
not recommended). The agent recommended b.

> **The owner (13:07):** "Go with b, build it. Then let me review."

**Built** (the fork's working tree):

- `_orientation` looks at the last receiver beat (`_last_index(run,
  _OFF)`, as the call does): after a Switch-off the clause reads "that the
  lab's receiver is switched off to save it — they can only transmit, and
  will call out for listeners when it is back on — and"; at the sign-on,
  before any call and after a Breakdown it keeps "that the lab's receiver
  is dead — they can only transmit, and will call out for listeners when
  it works — and". The docstring says so; the two texts sit in the code
  beside every other instruction text (wording, not numbers).
- The story's `orientation:` facts lose their two receiver sentences and
  say only who and where: "Four scientists, Daniel, Moira, Ralph and
  Samantha, are trapped in a secret research lab, besieged by the dead
  since the outbreak began, and broadcasting on the lab's shortwave
  radio."
- Tests: the story test asserts the facts no longer speak of the
  receiver; a new director test plays 300 rounds with short contacts and
  frequent repeats and checks every repeat says "dead" after a Breakdown
  and "switched off" after a Switch-off, and that both occur. Suite 1110
  passed.

> **The owner (13:10):** "Let's do a quick live check of how the model
> actually respond and compare with previous runs earlier today to see if
> this changes have improved the story quality."

The run is the one in §3.5 (`2026-09-28T13-10-44`). Its sign-on still
says the lab can only transmit ("Our radio is dead—only transmission."),
so taking the receiver sentences out of the facts did not lose it — one
run. **The repeat itself was not exercised**: 12 rounds never reach one
(about 20 free rounds are needed); forcing one with a low
`orientation_every` was offered, and left for the real run at the end of
the sweep.

### 3.7 The owner's ruling on improvisation (2026-09-28, 13:14)

> "Let me clarify one thing to you: Invented places of any other detail
> is not a bug, it is a feature. In this project we are probing the LLMs
> ability to improvise a story based on somewhat vague guidance. So this
> obsession you have developed with eliminating deviations from the
> prompt, drop it."

What it changes for the rest of the sweep:

- **Invention is not a defect.** A place, a name, a backstory, an
  accident the premise leaves undefined — the model making them up is
  what the project probes. The narration-quality discussion's C7
  ("Invented facts") is no longer a challenge; the carried-forward items
  of §3.4 about the location and the accident's story are closed by this
  ruling.
- **The measure of a line is whether the story works for the listener**
  — whether it hangs together with what the listener has heard, speaks to
  them, and holds attention — not whether it stays inside the prompt.
- **What still counts as a problem** (the agent's reading of the ruling,
  given to the owner at 13:14 and not contradicted) is what the listener
  hears as broken:
  the show contradicting itself in its own words (case 2: our instruction
  said "dead" after Samantha had said "switched off"), or the rules of the
  game told wrong. Wording added to pin facts down is not proposed.

### 3.8 Back to fixed lines — an audit, and an A/B test of the past tense (13:18-13:39)

*Cases 1 and 2 were committed at the owner's order at 13:18 ("Commit."):
the fork's `1ab5d6f`, this repository's `11266e2`.*

> **The owner (13:18):** "Ok, we are going too slow with this prompt
> sweep. Let's change style of presentation: Show me a list of all the
> cases with a brief explanation (one or 2 lines) so I can decide which
> one to prioritize."

The agent listed the thirteen cases left (3, 5, 6, 8-11, 13-17 and the
shared tail), one or two lines each, with a priority led by the last
exchange's questions.

> **The owner (13:26):** "i do not care of the last contact end with a
> question, that's ok, in the story they do not know the radio will fail
> next.
>
> This exercise is not going well. Too slow, and you are fixating in
> stupid details that have nothing to do with the story coherency.
>
> Let me go back to how I started this prompt sweep: fixed lines!
>
> How many scenarios do we have that involve fixed lines? Enumerate them
> me briefly. Then double check that:
>
> 1. no fixed line makes it to the model as a dialog line (we found it
> was confusing the model as it never actually generated those lines and
> started to repeat the same lines). Make sure it just appears as a
> recounted detail the prompt before the dialog.
> 2. Make sure that when the fixed lines are used, the prompt does not
> use present tense to refer to the context of the fixed lines, otherwise
> that confuses the model.
> 3. If you find deviations from these bring me the receipts, examples of
> past actual runs, and the location in the code."

**Ruled:** the last exchange may end on a question — in the story, the
cast do not know the radio is about to fail. Case 11's open point is
closed.

**The fixed-line scenarios — four** (the fork's `app/show/director.py`):

| # | Scenario | Fixed lines | Then the model | Code |
|---|---|---|---|---|
| 1 | An event | the event, read by the round's first speaker | at least one reaction, same round | `_free`, 173-180 |
| 2 | The call | an announcement (Daniel, Moira or Ralph), then Samantha's call; the pair by whether the receiver broke or was switched off | no request in its round; it reaches the model in the next request (an exchange or a re-call), joined with "Then" | `_repair`, 246-258 |
| 3 | The Breakdown | Samantha's line | one reaction | `_breakdown`, 342-351 |
| 4 | The Switch-off | Samantha's line, nobody answered or the voice lost | one reaction | `_switch_off`, 408-413 |

**Check 1 — no fixed line as a dialog line: passes.** Every request of the
day's four runs after the fix (the fork's `2026-09-28T11-50-15`,
`12-35-16`, `12-47-06`, `13-10-44`; 7 fixed lines each, covering all four
scenarios; 12 requests each) was searched: fixed lines quoted in user
turns 44 times per run, **in the model's own turns 0 times**. The code:
`app/show/script.py`, `reply_text` (line 136) builds the model's turns
from its own lines only; `assemble_messages` (line 193) joins a round
with no model line (the call) into the next user turn.

**Check 2 — no present tense for the fixed lines' context.** The part
that quotes each fixed line is past everywhere ("has just told them on
air", "has just called out"). Three places put the surrounding context in
the present:

- **A.** "Something happens that the listeners cannot see, and <name> has
  just told them on air: …" — the event (line 175), the call (258), the
  Breakdown (348); the formula the owner chose (§3.1-§3.3). No receipt of
  harm since the fix: in the four runs the reactions react, none redoes
  the event, the call or the Breakdown (13:10: "It's spreading. Not just
  in the jars."; "Hello! We're here—thank you for tuning in."; "We lost
  the receiver again.").
- **B.** The call followed by silence (`_re_call`, line 379): "Then only
  static answers. Samantha calls out once more to anyone listening,
  asking them to answer now; the receiver is still on." — "only static
  answers" and "the receiver is still on" are context in the present
  ("Samantha calls out once more" is the order for the model's own line).
  A weak receipt: both re-calls described the static instead of calling
  out (11:50: "The receiver is functioning, but the input is only static.
  We must be precise—if you answer, we can confirm."; 13:10: "This is a
  technical failure, not a lack of reception. Adjust your dial
  carefully.").
- **C.** The Switch-off after the voice went quiet (line 408): "The voice
  is gone." — director only; the nobody-answered version is already past
  ("Nobody answered the call.").

The one real receipt of present tense breaking a round is from before the
fix: run `2026-09-28T10-28-57`, round 4 — the call told in the present
("Daniel tells the listeners on air: "…" Then Samantha calls out to anyone
listening: "…""), and the model redid it as its first exchange ("We've
got the receiver—it's working! / Static's clearing. / Finally."); fixed by
`4d051ba`. The agent proposed all three in the past tense: "Something
happened that the listeners could not see, and …"; "Then only static
answered."; "The voice went quiet."

> **The owner (13:36):** "Let's conduct a quick A/B test before deciding:
> Make your recommended fixes, then run the same simulation, and bring me
> an easy to see comparison of the models output. And a final clear eval:
> Did the quality improve, yes or no?"

**The A/B test.** A = the committed wording (run `2026-09-28T13-10-44`,
the fork's `1ab5d6f`); B = the past tense (run `2026-09-28T13-37-52`,
built uncommitted: the five spots in `director.py` and the tests quoting
them; suite 1110 passed). The same seed 42, scripted listener and
temporary settings; the director's plan the same in all 12 rounds;
round 1's prompt unchanged and its output byte-identical in both runs;
the new wording in B's prompts, every token check equal. The model's own
lines:

| Round | A — present | B — past | Better |
|---|---|---|---|
| r2 event | It's spreading. Not just in the jars. | The heat—it's spreading. | tie |
| r4 first exchange | Hello! We're here—thank you for tuning in. / The static's gone. We can hear you now. / Whoever you are, we need your help. | Hello! We're here—answer us now! / They're responding! / Quick—identify them! | **A** (B talks about the caller, not to them) |
| r5 exchange | Alfredo, we need to know if you can transmit our messages. / Your radio would be vital to spreading our warnings. / Do you understand we're in peril? | Alfredo, we're in a lab besieged by the dead. Can you relay our calls? / Do you have a transmitter? / Quick—ask them! | **A** (B in the third person again) |
| r6 last exchange | Alfredo, you're in Austin with a truck. We need supplies—food, medicine, ammo. / … | Alfredo, we're near a wood and a swamp, under siege. Your truck could help. / … | tie |
| r7 Breakdown | We lost the receiver again. | We're sorry—this might be our last transmission. | tie |
| r8 aftermath | He's real. A real person. / We're broadcasting our fate to strangers. | He's real. We're talking to someone outside. / He might not know what's happening here. | tie |
| r9 free | We're sorry to burden you. / We don't know how long this will last. / The lab's power is failing. | We're so sorry we couldn't hear you earlier. / The static's back—we lost the link. / We'll keep trying. | A, slightly |
| r11 re-call | This is a technical failure, not a lack of reception. Adjust your dial carefully. | The receiver is functional. Static remains, but we can receive. | tie (neither calls out) |
| r12 Switch-off | We'll keep trying. | We'll keep the receiver ready. | tie |

**The agent's eval: No** — B worse in the contact (rounds 4 and 5), tied
elsewhere; the re-call it targeted still describes the static instead of
calling out. One run each, and any wording change reshuffles the
sampling, so B's slips may be noise — but nothing showed the past tense
helping. Recommended: discard B.

> **The owner (13:38):** "Yes, revert B."

**Reverted** (the fork back to `1ab5d6f`, suite 1110 passed). The fixed
lines' contexts stay as committed. Run `2026-09-28T13-37-52` stays on the
laptop as the record of the test.

> **The owner (13:39):** "Record it, then commit zombie-radio."

## 4. The prompts as they stand now (the fork's `4d051ba`)

*Every case, in the order a show meets them. For each: the code (current
line numbers in the fork), its place in the sweep, the text exactly as
sent, and the model's reply where a run has one. Cases marked "run" come
from the fork's run `2026-09-28T11-50-15` (the request as sent, from its
debug files); cases marked "director only" come from the director
without the model (its instruction, and the fixed line where there is
one) because that run did not reach them. The notes under each case are
observations to take up when the sweep reaches it — not decisions. Case 0
shows the system prompt as changed by §3.4 and §3.5; cases 1 and 2, as
changed by §3.5-§3.6; notes marked "since case 0"
quote the same round of the run `2026-09-28T12-47-06`, made with that
system prompt.*

**Every request ends with the same tail**, written by `_turns`
(`director.py:770`) and `_count` (`director.py:760`) and the tone
sentence (`director.py:750`): who speaks ("Samantha speaks first, then
Daniel, Moira or Ralph", "Moira and Ralph speak next"), how many lines
("the next line", "the next three lines"), "each with the emotion in its
voice, one of: <the round's overtone's moods>", and "Let the tone be:
<tone word>." — every constraint the grammar enforces is also said in
words.

### 0. The system prompt — every request · **reviewed** (§3.4)

The story's cast sheet (the fork's `stories/lab-outbreak/cast_sheet.md`)
with its premise and cast, and the format rule
(`app/show/rules/format_moods.md`), rendered once per run — as changed by
§3.4 (the fork's working tree, uncommitted at this writing; rendered with
the fork's own `render_cast_sheet`; `/no_think`, which the chat template
removes, left out):

```
You write a live radio play. Four scientists are trapped in a besieged research lab during a zombie outbreak,
speaking over the lab's shortwave radio. The lab is secret: the scientists do not know its name or address, only
that it stands near a wood and a swamp. The radio's receiver keeps failing: while it is down they can only
transmit, and when they get it working they call out for anyone listening to answer. A listener who answers is
heard as a voice on the frequency, and the cast talk to them directly. The scientists try to explain to the
listener over the radio the strange events that led to the lab's accident that produced the zombie infestation,
hoping that someone can find a cure for the virus, they also ask the listeners for help (supplies, food, medicine,
ammo) to try to resist the zombie attack waves.

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

*Status:* reviewed — three premise sentences are new: the listener who
answers (the agent's draft, kept by the owner) and what the scientists
tell the listeners (the owner's own), both §3.4; and where the lab is,
kept as flavour (§3.5). *Notes:* the cast are placeholders until the
owner's character bibles (Task 4); the model is told it writes "the
script" in "lines" and "transmissions" — the vocabulary the instructions
may use; the accident the premise mentions is not defined, so the model
invents it — a feature by the owner's ruling (§3.7).

### 1. The sign-on — round 1 · `_orientation`, `director.py:192` (line 212) · **reviewed** (§3.5) · run r1 of `2026-09-28T13-10-44`

```
USER (the last turn, exactly as sent):
  The broadcast begins. Samantha opens it and tells anyone listening, in their own words, that the lab's
  receiver is dead — they can only transmit, and will call out for listeners when it works — and who they are
  and where: Four scientists, Daniel, Moira, Ralph and Samantha, are trapped in a secret research lab, besieged
  by the dead since the outbreak began, and broadcasting on the lab's shortwave radio. Samantha speaks first,
  then Daniel, Moira or Ralph: the next two lines, each with the emotion in its voice, one of: calm, doubtful,
  urgent, curious, determined. Let the tone be: stiff-upper-lip.
→ the round, as said:
  Samantha (calm): We are scientists trapped in a lab near a wood and a swamp. Our radio is dead—only
  transmission. Over.
  Daniel (doubtful): The virus… it's mutating. We don't know how. Over.
```

*Status:* reviewed — the instruction itself unchanged except that the
story's facts no longer repeat the receiver (case 2); the system
message's premise gained the place sentence, kept as flavour (§3.5).
*Before the sweep* (the fork's `4d051ba`, run `2026-09-28T11-50-15`), the
facts also said "The radio's receiver is dead: they can only transmit,
not hear. When they get it working, they will call out for anyone
listening, and whoever hears them can answer then.", and seed 42 said
"We're broadcasting from Sector 9, Lab 7-B. The receiver's dead—we can
only transmit. If you hear this, respond Over." — the invented place is
a feature by the owner's ruling (§3.7). *Notes:* this run's sign-on says
"Our radio is dead" rather than the receiver, and does not tell the
listener to answer when the lab calls (12:47's did) — one run each.

### 2. The orientation repeat — every 20 ± 5 free rounds · `_orientation`, line 215 · **reviewed** (§3.6) · director only

The instruction after a Switch-off, and after a Breakdown (or before any
call), rendered by the director without the model on the shipped story
(the tone words and openers are whatever that model-free run drew):

```
after a Switch-off:
  For listeners just tuning in, Ralph tells them, in their own words, that the lab's receiver is switched off to
  save it — they can only transmit, and will call out for listeners when it is back on — and who they are and
  where: Four scientists, Daniel, Moira, Ralph and Samantha, are trapped in a secret research lab, besieged by
  the dead since the outbreak began, and broadcasting on the lab's shortwave radio. Ralph speaks first, then
  Daniel, Moira or Samantha: the next two lines, each with the emotion in its voice, one of: calm, doubtful,
  urgent, curious, determined. Let the tone be: dispassionate.
after a Breakdown (and before any call):
  For listeners just tuning in, Samantha tells them, in their own words, that the lab's receiver is dead — they
  can only transmit, and will call out for listeners when it works — and who they are and where: Four
  scientists, Daniel, Moira, Ralph and Samantha, are trapped in a secret research lab, besieged by the dead
  since the outbreak began, and broadcasting on the lab's shortwave radio. Samantha speaks first, then Daniel,
  Moira or Ralph: the next two lines, each with the emotion in its voice, one of: calm, doubtful, urgent,
  curious, determined. Let the tone be: irreverent.
```

The five repeats of the owner's check-4 listen (the fork's run
`2026-09-27T00-34-00`, before the change; round 62 came right after a
Switch-off):

```
r16  Ralph (determined): We're trapped in Sector 9, Lab 7-B—besieged by the dead. The receiver's dead, so we can
       only transmit. Over.
     Daniel (calm): If you hear us, respond when the receiver's fixed. Over.
r25  Samantha (urgent): We're trapped in a lab, overrun by the dead. The receiver's dead—we can only transmit. If
       you hear this, respond Over.
     Daniel (determined): Four scientists: Daniel, Moira, Ralph, and Samantha. Sector 9. Over.
r36  Daniel (calm): If you're tuning in now, congratulations—we're still alive. Over.
     Moira (doubtful): Don't get too hopeful. Over.
r52  Ralph (calm): If you're here, you're listening to four scientists trapped in a lab—be sieged by the dead.
       Over.
     Daniel (determined): We'll call again when the receiver's fixed. Over.
r62  Ralph (calm): If you're tuning in, you've caught us mid-broadcast—receiver's dead, but we'll keep trying.
       Over.
     Daniel (determined): We're not giving up. Over.
```

*Status:* reviewed — the receiver told as it went off; the story's facts
say only who and where (§3.6). *Not yet heard with the change:* no run
since has reached a repeat; for the real run at the end of the sweep.

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
called the lab; the aftermath has misread callers before (C9). *Since
case 0 (§3.4):* the system prompt now says who a voice on the frequency
is; with it, the same aftermath drew "Moira (sad): He's real. We need to
help him. Over. / Ralph (afraid): If he's broadcasting, he might be
trapped too. Over." (run `2026-09-28T12-47-06`) — about the caller now,
but still misreading him a little (he said he has a pickup truck).

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
this frequency."). *Since case 0 (§3.4):* with the new premise, the same
exchange drew "Samantha (happy): Hello! We're back—can you hear us now?
Over. / Daniel (relieved): Yes! Someone's there. Over. / Moira (excited):
Quick—ask them how they found this frequency! Over." (run
`2026-09-28T12-47-06`) — the agenda item picked up, but in the third
person (C3), and "can you hear us now?" right after the voice spoke.

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

*Closed* (§3.8): it still asks questions — the habit of every exchange
before it — and that is fine: the owner, 13:26, "in the story they do not
know the radio will fail next".

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
| 0 | The system prompt | `stories/lab-outbreak/cast_sheet.md`, `app/show/rules/format_moods.md` | **reviewed** (§3.4: the listener who answers; what the scientists tell the listeners) |
| 1 | The sign-on | `director.py:212`; the premise in `cast_sheet.md` | **reviewed** (§3.5: the place as flavour) |
| 2 | The orientation repeat | `director.py:204-210, 215`; the facts in `cast_sheet.md` | **reviewed** (§3.6: the receiver told as it went off) |
| 3 | A free round, plain | `director.py:150`, `instruction_for` 785 | to examine |
| 4 | A free round with an event | `director.py:173-180` | **reviewed** (case 1: (a) kept, (b) removed) |
| 5 | The aftermath | `director.py:183` | to examine |
| 6 | The recollection | `director.py:186` | to examine |
| 7 | The call | `director.py:251-254` | **reviewed** (cases 2 and 7) |
| 8 | The first exchange | `director.py:303-305` | to examine |
| 9 | A later exchange | `director.py:303-305`, `_restatement` 495 | to examine |
| 10 | An exchange restating earlier callers | `_restatement` 498 | wording kept by the owner; names-only A later |
| 11 | The last exchange | `director.py:322-323` | **reviewed** (new); its questions are fine (§3.8, the owner) |
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
- **Improvisation is the point** (the owner, 13:14, §3.7). The model
  inventing places and details is what the project probes; judge a line
  by whether the story works for the listener, not by whether it stays
  inside the prompt.
- **The director's own wording must not contradict the show** (case 2):
  the instruction said "dead" after Samantha had said "switched off" —
  the one kind of error that is ours, not the model's.
- **The premise steers what the cast talk about** (case 0). One sentence
  saying what the scientists do on the radio — explain what happened, ask
  the listeners for help — brought the outbreak and supplies into the
  exchanges ("please broadcast our message about the outbreak", "We need
  supplies"), and the beats' reactions spoke of what the failure means for
  the listener ("We're sorry—no more replies until we fix this.").
- **A change to the system message reshuffles every seeded round.** With
  the seed fixed, the director's plan replays exactly and the earlier run
  is a clean "before"; but the model's sampling changes everywhere, so no
  single line can be credited to the meaning of the change — compare whole
  runs, and test any guess about a cause against the next run (the guess
  that "Anyone may be listening" caused "They might not hear us" failed
  the next run).
