# Show engine, step 3.4c — the director's modes: Broadcast and Contact

**Date:** 2026-09-26 · **Arc:** MVP prototype · **Branch:**
`alfre2v/show-slice-3`
**Type:** discussion — how the show engages a listener who answers,
decided before the code.
**Status:** CLOSED 2026-09-28 — step 3.4c built, checked and done;
what happened after this discussion is in §19, the addendum. Before
that: OPEN — the decomposition agreed (§5); a pass over step
3.4c (§7) sorted what is ruled, proposed, deferred and open, and found
ten items that had fallen through the cracks; **3.4c's scope ruled,
one decision at a time (§9, §10):** Contact mode, the receiver story
with the Switch-off, the contact agenda, remembering the listener, and
the emotional overtone. The shape's details are ruled one at a time
(§12): Contact (§13), the receiver story with a repeating orientation
added (§14), the agenda (§15), the emotional overtone (§16, §17.11),
the exit criterion and the page (§17.12) are done; of the mechanics,
the orientation's details and the listener after the contact were
discussed — with an aftermath round and a recollection round added —
and the rest are the agent's picks at build (§18). Nothing built.

> **Read §11 — the risks of emotion in the voice, and the mood carried
> to the TTS.** Recorded prominently at the owner's request.

*Context for the cold reader.* The show engine (TODO Task 6b) is built
in the fork TalkWithZombies
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`) to the design
of [discussion 2026-09-23] show-engine-design ("SED"); slice 3, the
browser, to [discussion 2026-09-25] show-slice-3-browser-plan. In step
3.4 (2026-09-25, night) the owner talked to the show and found the
exchange poor: one answer line, the characters asking back with no
window to reply, and the story moving on at once, often to an event.
The follow-up "The listener's exchange is one line" in
`docs/follow-ups.md` holds the receipts. The director's rules for the
listener come from SED decision 5 (§5.6-§5.7: an invitation, one
answer line, a static round when nobody answers). On 2026-09-26 the
owner made the fix a step 3.4c, with a complete discussion first,
starting from the design of the owner's 2024 prototype.

*Conventions.* As in SED: the verbatim blocks are the transcript's
text, extracted by script — the owner's messages quoted exactly as
written, the agent's with their headings demoted to fit this document;
nothing removed unless a block says it is an excerpt. Sibling-clone
files with full absolute paths; this repository's files relative to
its root. Times are CDT.

## 1. 3.4c, discussion first (2026-09-26)

### 1.1 The agent's question (verbatim, excerpt: the part on 3.4c; ~00:09)

**The 3.4c question:** in both of last night's runs, the listener got one answer line. The characters asked back ("Who are you?", "Alfredo?"), but no listening window opened, and the next round moved on to an event. The follow-up proposes three ingredients (not yet decided):
- **a. A richer answer:** 2–3 lines, with the addressed character first, told to find out who and where the voice is. This is a change to the director only.
- **b. No event right after the listener's turn:** the next round keeps talking about the voice. This is also a change to the director only.
- **c. A follow-up window when the characters ask back:** the exchange becomes a short conversation, up to a cap, and silence ends it. This touches both the director and the page.

**My lean: yes, make it 3.4c, with all three ingredients.** Talking back is the heart of the demo, and last night it felt thin. There's room before Monday, and 3.5 is mostly your merges and deploy.

This changes the director (decision 5), so it would start with a shape round, not code. My estimates ran about 2.5 times too long yesterday. By yesterday's pace, 3.4c might take 1–1.5 hours to build, plus your check by ear, which needs a quiet place.

Does the listener's exchange become 3.4c?

### 1.2 The owner's answer (verbatim, 11:14)

> We continue work on 2026-09-26.
>
> I am trying to wake of the hibernated VM, but there is no A6000 availability right now. How soon do we need the VM up?
>
> Let's make it 3.4c, but we need a complete discussion before implementation. I will describe what I did in my 2024 project, which had much better results, and then we will iterate on a shape until we reach something we like.

## 2. The 2024 design, as the owner remembers it (verbatim, 12:01)

> So, in 2024, if memory serves well, I solved the interaction and engagement problem in the following way:
>
> #### The radio "breaks" as cover for the listening window.
>
> * In the story, the radio the characters use is broken at random intervals, so they can only transmit but cannot listen to incoming radio calls. They describe what is going on to the listener, saying that some smoke is coming out of the radio, and that the circuit that allows them to hear broke again... They say they will work to fix it but that in the meantime their transmissions out can keep working so they will keep transmitting their distress messages out until the radio is totally fixed.
> *  After the radio breaks, they continue their regular broadcast of discussions among them about the occurrences in the lab for a random number of rounds.
> * After one of them declare "the radio is fixed, that they can listen to incoming messages again", so they proceed to broadcast their invitation for somewhat that hears them to respond, then the mic is open for a period of ~10 secs, extensible if a good voice signal is detected, and closed  when the user pronounces "Over and out. " or when a maximum time is reached.
>
>
> #### Excitement and engagement with the listener
>
> * After they hear the voice of someone contacting them. They get excited, and the whole broadcast pivot to them trying to get information from the user... Their emotional tone in the response changes from the registry of grim emotions to the registry of positive emotions like happiness and hope. (We could enforce this in the grammar).
> * They ask questions like "Can you locate our facility?" (and proceed to provide signs like smoke raising, or near a wood and a swamp, etc... they don't know exactly where is located because it is a secret lab). 
> * They also want to know the name of the person who contacted them, and where is located. Once they get a name, they remember it, and use it to ask direct questions to the listener. The listening window opens 10 seconds after each question they ask.
> * The focus of their questions in on trying to get the user to help them escape the lab, besieged by zombies, or to provide supplies (they have a list of supplies they are running short on). I think I made some of these questions pre-recorded in a list in the code (same idea as the "events" we introduced)... We could also make one of their focus to describe the "scientific findings" from the infestation instead of asking questions, although I think this fits better their regular programing (when the radio is broken).
> * It is important that they engage with the user, responding to the user's questions and comments. I do not remember I had to do anything special for that, it seemed the models understood they had to engage with the user, but we can reinforce that in the description we provide on the top of the rounds.
>
>
> #### Return to the regular broadcast programming
>
> * After a random number of rounds of Q/A with the user, the radio breaks again, they again explain that only their ability to listen is compromised, that they are going to work to fix the radio, and in the meantime they will continue to broadcast to the world to transmit what they see before it's too late.
>
> * Something that I had in the regular programming (or maybe it was in my wishlist and I am enriching the memory) it's a "make a joke" mode, where we direct the LLM to make jokes about funny occurrences that we provide (pre-canned like events), something like "Oh, no! Is that Betty from accounting among the zombies? They got her!... Look, she is still holding her calculator in the hand... Habits die hard indeed. hahaha".
>
>
> I realize there is a lot in here, and not particularly well defined. We need to bring this to some kind of structured proposal. First decode what I just said into well defined and named director "modes/styles?", and try to separate this into a coherent separated features because at the moment it's to entangled.

## 3. The agent's decoding: two modes, two beats, eight features (verbatim, 12:03)

Here's your 2024 description, decoded and split apart. This is a discussion draft; nothing is decided.

#### The shape in one sentence

The show switches between two **modes**. A broken receiver is the story's reason why the listener can only talk at some moments. Two short **beats** move the show from one mode to the other.

```
Broadcast ──(the cadence)──► Repair beat + the call ──► window
                                   │
                    heard ─────────┴───────── silence
                      │                          │
                      ▼                          ▼
   Contact (a window after every round)      static round ──► Broadcast
                      │
        after N exchanges
                      ▼
              Breakdown beat ──► Broadcast
```

**The modes** (each lasts several rounds):
- **Broadcast:** the receiver is down, so the cast can transmit but not hear. They talk among themselves. Today's free rounds, events and tone words all live here.
- **Contact:** someone answered. The whole broadcast turns to the listener: excited and hopeful, asking questions and answering theirs. It ends after a random number of exchanges.

**The beats** (one round each, with a fixed purpose):
- **Repair:** someone announces the receiver works again, and the operator calls out to anyone listening. This is today's invitation, now with a story reason.
- **Breakdown:** smoke, and the receiving circuit is gone again. They'll keep transmitting while they fix it. This takes the show from Contact back to Broadcast.

#### The features, separated

Each one can be built, tested and judged on its own.

1. **The receiver story:** the repair and breakdown beats, plus one premise sentence in the cast sheet (the receiver keeps failing; while it's down, they can only transmit).
   - Today the invitation only "asks anyone listening to answer" (`director.py:106`). Nothing in the story says why the radio listens only sometimes.
   - Still open: if nobody answers the call, does the receiver break again, or stay up for the next call?
2. **Contact mode:** the conversation itself.
   - Answers run 2–3 lines, with the addressed character first. Today an answer is one line (SED §5.7, `director.py:110-121`).
   - The instruction tells the cast to engage: answer the listener's questions and comments, and ask who and where the listener is.
   - A window opens after every contact round. Today the page listens only after an invitation (`show.js:187`).
   - The mode ends after N exchanges (a new setting, drawn at random between two numbers), with the breakdown beat.
   - No events during Contact. Today events land on the next free round, whatever just happened.
   - Still open: what silence does in the middle of a contact.
3. **The contact agenda:** a story list of what the cast wants from a listener, one item per contact round, drawn like events. The items:
   - help locating the lab, with clues (smoke rising, near a wood and a swamp; the lab is secret, so they don't know the address);
   - the listener's name and whereabouts;
   - help to escape;
   - the supplies running short.

   This needs a new story file, the loader and the director.
4. **The hopeful tone:** during Contact, the grammar allows only hopeful moods, and the tone word comes from the "Hope and warmth" group. There are two catches:
   - The mood list has `happy` and `calm`, but no "hopeful", "excited" or "relieved" (`grammar.py:10`).
   - The tone groups are only YAML comments. The loader flattens them into one list (`story.py:81`), so drawing from one group means restructuring the file.
   - **The mood doesn't reach the voice.** The TTS request carries only the text and the persona. So the tone changes the words and the caption's "(happy)", not the sound. The sound belongs to Task 5b.
5. **Remembering the listener's name and place:** this mostly works already. Every round's instruction stays in the script the model reads (`script.py:174-181`), including "A voice on the frequency says: …". Last night Samantha answered "Alfredo? Over.", and the model later folded Alfredo into an event.
   - The gap: in a long run, the trim can drop those rounds. A "who we're talking to" line in each contact instruction would cover it, if we ever see it happen.
6. **Comic relief:** a list of funny happenings ("Betty from accounting…") with an instruction to joke about them, in Broadcast only. It works the same way as events and doesn't involve the listener.
7. **Scientific findings:** a list of findings the cast reports on air, in Broadcast. This is also event-like, and could be one section of the events list.
8. **The 2024 open-mic window:** the mic opens for about 10 s, stays open longer while a voice is heard, and closes on "Over and out" or a time limit.

#### Where 2024 differs from what we ruled

- **Feature 8 conflicts with hold-to-talk.** On 2026-09-23 you asked about exactly this: "How do we dynamically extend the listening time if we detect a user is probably speaking?" The ruling was hold-to-talk with three separate timers, and always-listening as the post-MVP path (SED §5.4–§5.6). The repair story works just as well with the button: "the receiver is fixed", and the button lights up. I'd keep the button and leave feature 8 out.
- **Counting:** 2024 counted the Broadcast stretch in rounds. Ours counts seconds of played audio (`interaction_min_s` / `interaction_max_s`, SED §5.7). The repair beat simply comes when the cadence says so, so nothing changes. Counting Contact's length in exchanges is new, and rounds are the natural unit there.

#### My lean for 3.4c

- **Include features 1, 2 and 3, plus the mood half of 4** (a hopeful mood set during Contact; the tone groups later). These are what you missed last night: a reason for the window, a real conversation, and something the cast wants from the listener.
- **Leave out:**
  - feature 5, which already works for now;
  - features 6 and 7, which are Broadcast content with no listener involved, so they become follow-ups or a later step;
  - feature 8, per the ruling.

Does this decoding match what you meant? If it does, which features go into 3.4c?

## 4. The owner's answer (verbatim, 12:21)

> Yes, this is a good decomposition.
>
>
> #### Where I disagree with you:
>
>
> ```
> 8. The 2024 open-mic window: the mic opens for about 10 s, stays open longer while a voice is heard, and closes on "Over and out" or a time limit.
> ```
>
> I do not think we should adopt this part of 2024. We are keeping the hold to talk.
>
>
>
> ```
> Remembering the listener's name and place: this mostly works already...
> ```
>
> I disagree. This does not work at all. Yes, the names are in the transcript but, maybe nemotron is lame, but it does not seem to understand the importance of trying to engage directly with the user... I think we will have to design the prompt carefully in each interaction to instruct the LLM to use known facts about the user, and identify and keep ourself in code a list of those "known facts", now how do we extract those facts is another question... Another simpler alternative is to prepare a list of engagement prompts which already instruct the LLM to ask for some particular information to the user or if the user already provided it, to use that fact to compose an engaging question to the user... this second way would require us to compose a list of "engagement seeking prompts" in a list as we do with events.
>
> #### I agree with you
>
>
> ```
> Leave out features 6 and 7, which are Broadcast content with no listener involved, so they become follow-ups or a later step;
> ```
>
> yes, this is not about engagement so can be postponed.
>
>
> ```
> feature 8, per the ruling.
> ```
>
> yes, this does not fit our push to talk functionality. No need for "Over and out." to detect end of speech.
>
>
> #### Need for a good way to save these discussions back and forth
>
> I think these new director modifications need a new discussion document. If you agree, please propose a file name and start the draft.

## 5. Where it stands (2026-09-26, 12:21)

- **Agreed:** the decomposition of §3 — the modes Broadcast and
  Contact, the beats Repair and Breakdown, and the eight features.
- **Out:** feature 8, the 2024 open-mic window. Hold-to-talk stays, as
  ruled in SED §5.6; no "Over and out" to detect the end of speech.
  The owner filed it under "Where I disagree with you"; the agent had
  proposed leaving it out as well, so both sides agree.
- **Postponed:** features 6 (comic relief) and 7 (scientific findings)
  — Broadcast content, not about engagement.
- **Re-opened: feature 5, remembering the listener.** The agent's
  "this mostly works already" is withdrawn: the listener's words are in
  the script the model reads, but the model does not use them. The
  receipts are in the follow-up (the owner's check of 3.4b): "My name
  is Alfredo" → Samantha: "Alfredo? Over."; then "I want to ask
  Samantha, what is the cause of the outbreak?" → Samantha: "I don't
  know what you're asking. Over." The owner's two options: §5.1.

### 5.1 Feature 5: the owner's two options

The owner's message (§4), reworded by the agent at the owner's request
and adopted as this section's wording ("Yes, put it in §5 in place of
my poor wording.").

**The problem both options answer.** The listener's words are in the
script the model reads, but the model doesn't act on them. It doesn't
address the listener, use what the listener said, or go after what the
cast still wants to know. Having the words in context isn't enough:
each contact round's instruction has to steer the model toward the
listener.

**Option A: known facts, kept in code**
- The director keeps a list of what the show has learned about the
  listener: their name, where they are, anything else they've told the
  cast. The list lives in the run's record, next to the rounds.
- Each contact round's instruction is worded around that list. It gives
  the model the known facts and tells it to use them: call the listener
  by name, ask about the place they mentioned.
- Still open: how the facts get from what the listener said into the
  list.
- Example: the list holds "name: Alfredo", and the instruction says
  "The voice on the frequency is Alfredo. Samantha answers Alfredo by
  name and asks where they are."

**Option B: engagement prompts, kept in a list like the events**
- The story holds a list of engagement-seeking prompts. One is drawn per
  contact round, the way events are drawn.
- Each prompt covers one piece of information and has two branches:
  - if the listener hasn't given it yet, ask for it;
  - if the listener already has, use it to compose an engaging
    question.
- Nothing is extracted in code. The model reads the script and picks
  the branch.
- Example: "Find out the voice's name. If they have already told you,
  call them by it and ask how they found this frequency."

**The difference**
- **A** decides in code what is known, so the instruction can state it
  plainly. The cost is that it needs a way to extract the facts.
- **B** needs no extraction and reuses the events machinery, so it's
  simpler. But it still relies on the model noticing what the listener
  already said. That is the weakness seen in 3.4, though now the model
  is pointed at one fact at a time.

*The agent's note (not yet discussed):* B and feature 3, the contact
agenda, come close to one list. Each agenda item asks for something
(where the lab is, the listener's name and place, help, supplies); B
adds the second branch — use the answer once it is known.

## 6. Open for the shape (as of 12:21)

*Extended by the pass of §7; where things stand after it: §8.*

- **Feature 5:** A, B, or both; for A, how the facts are extracted.
- **Feature 1:** when nobody answers the call — does the receiver break
  again, or stay up for the next call?
- **Feature 2:** what silence does in the middle of a contact; the
  range of N (the exchanges before the breakdown); the answer's
  length.
- **Feature 4:** which hopeful moods; the mood reaches the words and
  the captions, not the voice.
- **3.4c's scope:** features 1, 2, 3 and the mood half of 4 (the
  agent's lean, §3), and feature 5 in the form chosen.

## 7. B merged with feature 3, and a pass over 3.4c (2026-09-26)

### 7.1 The owner's question (verbatim, 12:35)

> Explain to me better this "B merged with feature 3, restating the listener's words in each contact instruction"
>
> I want to do one more pass over what we have in "step 3.4c", to clear what we have already agreed to build, and what is recognized as deferred, and try to see if something has fallen through the cracks without us noticing.
>
>
> By the way I finally got the VM to start, so you will be able to conduct live experiments all you want when we decide to build.

### 7.2 The agent's answer (verbatim, 12:37)

#### B merged with feature 3, explained

**One list, not two.** Feature 3 (what the cast wants from a listener) and your option B (prompts with two branches) become a single story list, the contact agenda. Each item is written in B's two-branch form:
- "Find out the voice's name. If the voice already gave it, call them by it."
- "Ask the voice to help find the lab: it is secret, near a wood and a swamp, with smoke rising. If the voice already said where they are, ask whether they know such a place near there."
- "Ask the voice for supplies: the lab is short of insulin, batteries and clean water. If the voice already offered help, ask what they can bring."

**Restating the listener's words.** Every contact round's instruction would carry everything the listener has said since answering, copied verbatim from the record. Each round already stores the listener's words (`script.py:53`), so nothing is extracted and nothing is interpreted; the director just copies. Here is exchange 2, after you said "My name is Alfredo", then "I'm in Austin":

```
A voice on the frequency says: "I'm in Austin."
Everything the voice has said since it answered: "Hello, who are you? My name is Alfredo." / "I'm in Austin."
Samantha and Moira speak next: the next two lines, each with the emotion in its voice.
Answer the voice first, then: Ask the voice to help find the lab: it is secret, near a wood and a swamp,
with smoke rising. If the voice already said where they are, ask whether they know such a place near there.
End with a question to the voice.
```

**Why the restatement helps.** Today your name sits in an earlier turn, among the cast's lines, and the model said "Alfredo? Over." and moved on. With the restatement, your name and the order to use it are in the same message.

**How it relates to A and B.** It is still B: the model picks the branch, and there is no list of facts in code. The facts are just easy to see. If the model still ignores them, that is the evidence for A. With the box up, a driver run can tell us before you ever speak.

#### One more pass over 3.4c

**Ruled:**
- 3.4c happens, with a shape before any code.
- The decomposition: the modes Broadcast and Contact, the beats Repair and Breakdown, and the eight features.
- Hold-to-talk stays, with no "Over and out" (feature 8 out).
- Features 6 and 7 are postponed.
- Feature 5 is needed; A versus B is open.
- §5.1's wording is adopted.

**Proposed, not ruled yet:**
- 3.4c's scope: features 1, 2, 3, the mood half of 4, and 5. You ruled the ones left out, but you haven't said yes to the ones in.
- Feature 5 as B merged with feature 3, as explained above.

**Deferred:**
- features 6 and 7, which aren't in `follow-ups.md` yet;
- the tone-group half of feature 4 (my lean, not ruled);
- feature 8, which stays the post-MVP always-listening path (SED §5.5);
- option A, only if B falls short;
- "Talk anytime", which keeps its own follow-up.

**Open questions already in §6:**
- If nobody answers the call, does the receiver break again or stay up?
- What does silence do in the middle of a contact?
- The range of N and the answer's length.
- Which hopeful moods.

**What fell through the cracks.** These are new; each comes with a receipt.
1. **The cadence would bring the next call too soon.** It counts played seconds since the last invitation (`director.py:74`). A contact of 3–4 exchanges plays maybe 40–60 s of audio. With `interaction_min_s` at 60 (`config.py:273`), the next Repair could come 10–20 s after the Breakdown. The count should start from the Breakdown.
2. **The Breakdown must also answer the listener's last words.** It follows the listener's last turn. If it only says "the receiver's gone again", those words are ignored, which is exactly your complaint from 3.4. One round could do both: answer, then the smoke.
3. **"The addressed character speaks first" needs a new grammar rule.** Today any allowed speaker can take any line (`grammar.py:29-33`: `root ::= line{1,N}`). Pinning the first line to one name is small, but it changes decision 1's grammar. The same goes for a two-line Repair (whoever fixed the receiver, then the operator).
4. **The show's opening.** When does the listener learn the receiver story? Round 1 is an ordinary free round today. There are three options:
   - the premise lives only in the cast sheet;
   - the show opens with a Breakdown;
   - the first Repair explains it.
5. **The tone word inside Contact.** A tone word is held for about 3 rounds (`tone_hold`, `config.py:267`), so "macabre" could carry into a hopeful exchange. Contact rounds could skip the tone word until the tone-group half of feature 4 arrives.
6. **"Listen after this round" is tied to the invitation in five places:**
   - `director.py:60` and `director.py:74`;
   - `app/routers/show.py:137`, where a transcript is accepted only after an invitation;
   - `static/show/show.js:187`;
   - `scripts/drive_show.py:242`.

   The round's summary needs a "the radio listens now" flag, and the route, the page and the driver should follow it.
7. **The driver can't hold a conversation.** It answers only invitations, one `--heard` item each (`drive_show.py:7`). It needs to answer every listening round, so we can test many contacts, and A against B, without your voice.
8. **3.4c has no exit criterion yet.** A candidate: by ear, a contact of several exchanges where the cast calls you by name, uses what you said and asks for help, and then the Breakdown returns the show to Broadcast.
9. **The listener after the contact.** Back in Broadcast, the cast never mentions the listener again ("Alfredo in Austin said…"). That would be feature 5 carried across modes. My lean is to defer it.
10. **Bookkeeping:**
    - a 3.4c entry in the TODO;
    - a dated note in SED decision 5 (the answer is no longer one line; there are new kinds of round);
    - the follow-up "The listener's exchange is one line", resolved by 3.4c;
    - features 6 and 7 recorded as follow-ups.

Is anything missing from the cracks list? If not, I'll add this pass to the draft, and we settle 3.4c's scope next.

### 7.3 The owner's answer (verbatim, 12:43)

> Nothing missing, add the pass to the draft

## 8. Where it stands after the pass (2026-09-26, 12:43)

*A snapshot; the scope was ruled next (§9, §10).*

- **The pass of §7.2 is the current state:** what is ruled, what is
  proposed and not yet ruled, what is deferred, the open questions of
  §6, and the ten items that had fallen through the cracks. The owner
  found nothing missing from the cracks list (§7.3).
- **The box is up again** (the owner, 12:35), so the shape's questions
  can be tried live when the build starts — the driver first (crack 7).
- **Next:** 3.4c's scope — features 1, 2, 3, the mood half of 4, and
  feature 5 as B merged with feature 3 (the agent's leans, not yet
  ruled) — then the open items, one at a time.

## 9. 3.4c's scope, decision by decision (2026-09-26)

### 9.1 The owner: slow down, one decision at a time (verbatim, 12:49)

> What does this mean: `§6 keeps its number, retitled "as of 12:21" with a pointer to §7 and §8, because the quoted pass refers to "§6" and "§5.1".`. I did not retire "6. Comic relief", I postponed it, so it should have a proper follow-up entry. We are going to execute on this at some point.
>
> Next is 3.4c's scope, yes, but slow down. Bring each decision to me one by one. And in each case, present  context for each item you bring, so I can make the connections in my head.

*The agent's answer on "§6" and on the follow-ups is missing from the
session transcript (the text written before a tool call was not
saved), so it is not quoted. In short: "§6" meant the draft's section
6, "Open for the shape", not feature 6 — the draft has two sets of
numbers, sections and features, and the agent's sentence mixed them;
nothing was retired; features 6 and 7 became entries of
`docs/follow-ups.md` ("Comic relief — the cast jokes about a funny
happening", "Scientific findings — the cast reports what the lab
learns about the infection"). The rest of that answer follows.*

### 9.2 Decision 1: Contact mode (verbatim, excerpt from "3.4c's scope"; 12:50)

#### 3.4c's scope, one decision at a time

This is the order I'd bring them in:
1. feature 2, Contact mode;
2. feature 1, the receiver story;
3. feature 3, the contact agenda;
4. feature 5, remembering the listener (B merged with feature 3, or not);
5. feature 4, the hopeful moods.

Contact mode goes first because the other four attach to it.

##### Decision 1: is feature 2, Contact mode, in 3.4c?

**What you heard in 3.4.** Each time you spoke, one character said one line, and the show moved on. From the record (the follow-up "The listener's exchange is one line"):
- "Hello, what's your name?" got Daniel: "Who's there? Over.", and the next round was an event (the power lines singing).
- "Hello, who are you? … My name is Alfredo" got Samantha: "Alfredo? Over."

The characters asked you a question, and then gave you no chance to answer it.

**Why it happens today.** It's the design from SED decision 5, built on purpose to keep the MVP small:
- the answer round is **one line** (SED §5.7; `director.py:110-121`);
- only an **invitation** opens a listening window (`show.js:187`; the round route accepts your words only after an invitation, `app/routers/show.py:137`);
- after the answer, the director goes back to ordinary free rounds, and those are where events land.

**What Contact mode changes.** After you speak, the show stays with you for several exchanges:
- each exchange is one round of 2–3 lines: the cast answers what you said, then asks you something;
- a listening window opens after every exchange, so you can answer the question;
- there are no events while the contact lasts;
- after N exchanges it ends, handing back to the regular broadcast.

**How it connects to the other features.**
- Feature 1 (Repair and Breakdown) is how the show enters and leaves Contact.
- Feature 3 (the agenda) is what the cast asks you in each exchange.
- Feature 5 is how they remember what you told them.
- Feature 4 is the hopeful mood inside the exchanges.

Without Contact, those features have nothing to attach to. Only feature 1 could stand alone, as flavor around the invitation.

**What it touches.**
- the director: a new kind of round, and the cadence clock (crack 1);
- the record: the list of round kinds (`script.py:50`);
- the grammar, if the addressed character must speak first (crack 3);
- the round route, the page and the driver, which must listen after any round that asks, not only after invitations (cracks 6 and 7).

**What would be decided later, inside it.** These are not part of this decision:
- the range of N;
- what silence does in the middle of a contact;
- the answer's length;
- whether the addressed character speaks first;
- the tone word inside Contact (crack 5).

**My lean: in.** It is your 3.4 complaint itself.

Is Contact mode (feature 2) in 3.4c?

### 9.3 The owner's answer (verbatim, 12:53)

> Yes, Contact mode is in 3.4c

### 9.4 Decision 2: the receiver story (verbatim, 12:53)

Contact mode is in. I'll record the five scope rulings in the draft together, once the last one is decided.

##### Decision 2: is feature 1, the receiver story, in 3.4c?

**What it is** (your 2024 design): the lab's receiver keeps failing.
- **Breakdown:** smoke comes out, the circuit that lets them hear is gone again. They tell the listeners they can still transmit and will keep broadcasting while they fix it.
- **Repair:** later, someone announces the receiver works again, and the operator calls out to anyone listening. Then the window opens.

**What it fixes.** Today nothing in the story explains why the radio listens only sometimes.
- Every 60–180 s of played audio (`config.py:273-274`), the operator just "turns to the microphone and asks anyone listening to answer" (`director.py:106`).
- Between invitations, the talk button is dark for no reason the listener can hear.

With the receiver story, the window's limits become part of the fiction: the receiver is fixed, and the button lights up. That also helps with the window you'd have preferred to drop ("Talk anytime"). The window stays for the MVP, as ruled on 2026-09-25, but now it has a reason.

**How it connects to Contact (decision 1).** It's Contact's way in (Repair and the call) and its way out (Breakdown).
- Contact can work without it: an invitation opens the contact, and some closing line ends it ("we have to get back to the broadcast").
- So feature 1 is separable. But it's the story's own answer to "why does the conversation stop?", and a broken receiver is a better reason than a host changing the subject.

**What it touches.**
- **The director:** the invitation's wording becomes the Repair, a new Breakdown kind of round, and the cadence clock counting from the Breakdown (crack 1).
- **The cast sheet's frame:** one premise sentence in the opening paragraph ("You write a live radio play. Four scientists … speaking over the lab's shortwave radio.", `stories/lab-outbreak/cast_sheet.md:7`). That's the show's frame, not the cast entries your bibles will fill (Task 4).

**What would be decided later, inside it:**
- if nobody answers the call, does the receiver break again or stay up (the draft's §6)?
- the Breakdown also answers the listener's last words (crack 2);
- when the listener first learns the receiver story (crack 4);
- whether the Repair is one line (the operator) or two (whoever fixed it, then the operator; crack 3).

**My lean: in.** It's mostly wording plus one new kind of round, and it gives Contact its ending in the story's terms.

Is the receiver story (feature 1) in 3.4c?

### 9.5 The owner's answer, and an idea for a call nobody answers (verbatim, 13:03)

> Yes, the receiver story is in 3.4c.
>
> One of the open questions: if nobody answers the call, does the receiver break again or stay up (the draft's §6)
> I think I have an idea for this one: 
> if nobody answers for a few rounds, say,  2 rounds of asking for engagement, (this is a different counter than the exit condition if a user is engaging: radio breaks), then the characters declare they are going to switch off the receiver with a good excuse (to save power, or to preserve the fragile and precious receiver for a time with higher probability that someone may be listening).
>
> Do you like this?

### 9.6 The agent: the idea, as read (verbatim, 13:04)

Receiver story is in.

**Yes, I like it.** It closes a hole in the fiction: if the receiver works and nobody answered, why would they stop listening? Your answer makes stopping a choice with a reason, not a failure. Here's how I read it, and what I noticed.

**The sequence, as I understand it:**
1. **Repair and the call.** The receiver is fixed, the operator calls out, and the window opens.
2. **Silence.** The operator calls again ("Is anyone out there? We'll try once more…"), and the window opens again.
3. **Silence again.** After 2 unanswered calls, they **switch the receiver off**, with a good excuse: to save power, or to protect the fragile receiver for a time when someone is more likely to be listening. Then they go back to the broadcast.
4. **An answer at either call** starts Contact, and the counter starts over.

**Why I like it:**
- **A second chance for the listener.** Today a single missed window of 10 s (`listen_window_s`, `config.py:275`) sends the show back to the broadcast. At a live demo, someone slow to press the button gets a second call.
- **It tames something the model already does.** When the operator had nothing to say but "Only static answers.", it signed off the whole show in both live drives. That's SED §5.7's note of 2026-09-24, and the reason the static round now says "the broadcast goes on" (`director.py:128`). An explicit reason to switch off gives the model a clean way out instead of an improvised farewell.
- **The excuses fit the story.** The generator and the supplies running short are already in it (events such as "The generator coughed twice and the lights flickered across the east wing.").

**What it adds or changes:**
- **A third beat, "Switch-off":** off by choice after silence. The Breakdown is off by failure after a contact. Both lead back to Broadcast.
- **The Repair's wording depends on how the receiver went off:** "it's fixed" after a Breakdown, "we're switching it back on" after a Switch-off. The director can read that from the record.
- **The count of unanswered calls becomes a setting,** 2 by default.
- **The cost is dead air when nobody's there:** two windows of about 10 s each, per call cycle. That's fine at a demo, where someone will answer, and noticeable in unattended driver runs.

**One connection, not for now:** the same pattern may fit "silence in the middle of a contact". The listener was there, then went quiet: call once or twice, then "we've lost them" and off. That's a separate question for later.

Do we adopt your idea as the answer to that open question, as I've read the sequence above?

### 9.7 The owner: adopted, and extended to silence inside a contact (verbatim, 13:09)

> Yes, adopt it as you read the sequence. 
>
> Also, I like very much your proposal as an improvement:
>
> ```
> One connection, not for now: the same pattern may fit "silence in the middle of a contact". The listener was there, then went quiet: call once or twice, then "we've lost them" and off. That's a separate question for later.
> ```
>
> yes, of course, I do not think we need to postpone this, once we build it for one place, it's almost free to use it too as an exit condition if we lose the engagement in the middle of contact mode.
>
> Let's do both, unless I am missing something that complicates this. Pushback if your have strong reasons to not implement your extension proposal right now.

### 9.8 The agent: no pushback; decision 3, the contact agenda (verbatim, 13:10)

Adopted as I read it.

**On extending it to silence in the middle of a contact: no strong reason to wait, so let's do both.** You're right that it's almost free. Once the director counts silences for the call, the same count works anywhere a window opens. Together they make one rule:

> **Any listening window:** silence counts, and an answer resets the count. After 2 silences in a row, the receiver goes off with a Switch-off. Before a contact, the reason is "nobody's out there"; in the middle of one, it's "we've lost them". Either way, the show returns to the broadcast.

Nothing here complicates the build. The director reads the count from the record, like everything else it remembers. The page doesn't care why a round listens. The driver already has a way to say "silence" (`--heard -`).

A few small details go into the shape, not this decision:
- In the middle of a contact, the re-call should come from whoever was talking to the listener, by name if known ("Alfredo? Are you still there?"), not the operator's generic call.
- Does a re-call count as one of Contact's N exchanges?
- Today's "static" round (the operator reacts to silence, with no window) turns into this re-call, which has a window.

##### Decision 3: is feature 3, the contact agenda, in 3.4c?

**What it is** (your 2024 design): a list of things the cast wants from a listener, one item drawn per contact round, the way events are drawn. In your words: "I think I made some of these questions pre-recorded in a list in the code (same idea as the "events" we introduced)". The items you named:
- help locating the lab: it's secret, so they only have clues (smoke rising, near a wood and a swamp);
- the listener's name and whereabouts;
- help to escape the besieged lab;
- supplies, from their list of what's running short.

**What it fixes.** In 3.4 the answers only reacted ("Who's there?", "Who are you?") and then stopped. The model had no goal of its own in the exchange. The agenda gives every exchange a purpose: the cast *wants* something from you, and that is where the stakes and the engagement come from.

**How it connects.**
- It's the content of Contact (decision 1).
- The next decision, feature 5, is about its form: whether each item also covers "if the listener already told you, use it", which is B merged with this list.
- If feature 3 is out, Contact exchanges are guided only by "answer the voice and engage".

**What it touches.**
- a new story file in the fork (e.g. `stories/lab-outbreak/contact.yaml`) and its loader, modeled on `_load_events` (`story.py:72-78`);
- the draw, which reuses the events' no-repeat helper (`_fresh`, `director.py:189-193`);
- the contact instruction's wording, "Answer the voice first, then: <item>.", so the agenda never pushes the listener's words aside.

**What would be decided later, inside it:**
- which items, and how many;
- whether some come in a fixed order (the name first seems natural) or all at random;
- no repeats within one contact, or across the whole run;
- who writes the list. I'd draft a first list for you to review.

**My lean: in.** Without a goal, Contact is only politer reacting.

Is the contact agenda (feature 3) in 3.4c?

### 9.9 The owner's answer (verbatim, 13:13)

> Yes, the contact agenda is in 3.4c.

### 9.10 Decision 4: remembering the listener (verbatim, 13:14)

The contact agenda is in.

##### Decision 4: feature 5, remembering the listener. In what form?

**The problem** (the draft's §5.1). The listener's words are in the script the model reads, but the model doesn't act on them. From your 3.4b check:
- "My name is Alfredo" got Samantha: "Alfredo? Over."
- "I want to ask Samantha, what is the cause of the outbreak?" got Samantha: "I don't know what you're asking. Over."

**Your two options** (§5.1):
- **A, known facts kept in code:** the director keeps a list of facts about the listener and words each instruction around it. How the facts get extracted is open.
- **B, engagement prompts:** each prompt asks for one piece of information, or uses it if the listener already gave it. Nothing is extracted; the model picks the branch.

**What decision 3 changes.** With the agenda in, B needs no list of its own. Each agenda item is simply written in B's two-branch form, so B and feature 3 become one list, for example:

> "Find out the voice's name. If the voice already gave it, call them by it."

**The restatement,** the part that addresses B's weakness. Every contact instruction carries everything the listener has said since answering, copied verbatim from the record. Each round already stores the listener's words (`script.py:53`), so this copies strings and extracts nothing. Your name then sits in the same message as the order to use it, not rounds back in the script.

**What A would take, for comparison.** A needs an extraction step, and both ways I see are design work of their own:
- a second, small request to the model after each listener turn, pulling out name and place with a grammar. It adds time between your release and the answer;
- or a hidden "facts" line at the top of the answer's own grammar. That's one request, but it changes the reply's format and what the script keeps.

**The evidence, before your voice.** With the box up, a driver run can test this the way we tested events. It would use scripted listener lines ("My name is Alfredo", "I'm in Austin") and count how often the cast uses your name and your place.
- If it uses them in most exchanges, B is enough.
- If it doesn't, that's the evidence for A, and A comes back to you as a decision.

**What would be decided later, inside it:**
- whether the restatement covers only this contact or everything the listener said in the run (the page can't tell whether it's the same person);
- the restatement's exact wording.

**My lean:** feature 5 in 3.4c as B merged with the agenda, plus the restatement. A only if the driver test shows B falls short.

Is that the form of feature 5 in 3.4c?

### 9.11 The owner's answer (verbatim, 13:18)

> Yes, feature 5 is B merged with the agenda, plus the restatement.

### 9.12 Decision 5: the hopeful tone (verbatim, 13:18)

Feature 5 is settled: B merged with the agenda, plus the restatement. This is the last scope decision.

##### Decision 5: feature 4, the hopeful tone. Which half is in?

**What it is** (your 2024 design, verbatim): "Their emotional tone in the response changes from the registry of grim emotions to the registry of positive emotions like happiness and hope. (We could enforce this in the grammar)."

**Two things in the engine carry emotion today:**
- **The mood tag on each line.** In `Moira (doubtful): …`, the grammar lists the allowed moods: calm, happy, sad, afraid, terrified, doubtful, angry, urgent, exhausted (`grammar.py:10`). The model picks the tag before writing the line, so the tag colors the words. The caption shows it.
- **The tone word.** "Let the tone be: <word>." is drawn from `tones.yaml` (500 words in 24 groups, one of them "Hope and warmth") and held for about 3 rounds.

**So the feature has two halves.**
- **The mood half:** in Contact rounds, the grammar allows only hopeful moods. That's your "enforce this in the grammar", and the instruction says it in words too, per SED's rule that every constraint in the grammar is also stated.
  - It's cheap: `build_grammar` already takes a list of moods (`grammar.py:26`), so the director hands it a smaller list for Contact.
  - The line parser accepts any mood word (`parser.py:23`), so new words such as "hopeful", "excited" or "relieved" need only the list.
- **The tone half:** the tone word inside Contact comes from "Hope and warmth".
  - It costs more: the groups are only YAML comments, and the loader flattens them into one list (`story.py:81`). The same restructuring is already waiting in the follow-up "Events that stay on topic for a few rounds" (idea 2, for `events.yaml`).

**One catch, for both halves: the mood doesn't reach the voice.** The TTS request carries only the text and the persona name. So "hopeful" changes what they say and the caption, not how they sound. Emotion in the voice belongs to Task 5b (a voice sample per emotional register; owner action queue, item 1).

**How it connects.**
- It's how Contact feels (decision 1).
- The tone word links to crack 5: a word held from the broadcast, "macabre" say, would carry into a hopeful exchange. If the tone half is deferred, the simple answer to crack 5 is no tone word in Contact rounds, and the mood set does the work.

**What would be decided later, inside it:**
- **Which mood words.** A strictly cheerful set can force good cheer at bad news: if the listener says "the highway north is blocked", "happy" would ring false. The set may want "calm" and "urgent" alongside "hopeful", "excited" and "relieved".
- Whether the new words are also allowed in free rounds, or only in Contact.

**My lean:** the mood half in 3.4c; the tone half deferred, as a follow-up next to the events' topic groups.

Is that the split for feature 4?

### 9.13 The owner: mood and tone must be coupled; emotion in the voice (verbatim, 13:36)

> This is a good decomposition.
>
> #### Mood and tone coupling has to be enforced
>
> But there is a problem in your decomposition, which is that you fail to recognize that we need to couple both "The mood half" with "The tone half", we cannot execute them completely disconnected, otherwise we will send contradictory emotional signals for the LLM to generate the next lines. 
>
> What this needs:
>
> * We need to decompose both the list of moods, and the list of tone words in 3 groups (`positive`, `neutral`, `negative`).
> * then in each round, we decide if the emotional overtone will be positive, neutral or negative, and once we fix that, we constrain our prompt with moods and tone words only from the emotional overtone sublist.
>
>
> What is your opinion? Am I missing something?
> In my view we are forced to build both at the same time.
>
>
> #### One catch, for both halves: the mood doesn't reach the voice
>
> Very well pointed. But this is in my radar and one of the main features that I would like to achieve (not sure if I described this correctly anywhere in our documents):
> At some point I want to have different voice audio samples for each character, divided by emotion, so I can change the reference audio we sent to the TTS engine based on the emotion in each voice, I was planing to use the mood provided by the grammar, but I do not think it is practical to collect so many fine grained voice samples for each mood we have, so I need to map the moods to a reduced number of emotional states I can put one to one to audio samples, and this thing which I am calling "emotional overtone" would be the simplest way to guide the changing reference audio feature.
>
> What do you think? Do you like this approach or am I making a mistake I do not see?
> In my view this feature we are discussing is the first stepping stone to reach voice with emotions in TTS.

### 9.14 The agent's answer (verbatim, 13:37)

##### Coupling mood and tone: you're right, with one nuance

**You're right.** If both are forced separately, they can contradict each other. For example, "Let the tone be: macabre." while the grammar allows only hopeful moods. One signal per round has to drive both.

**The nuance about "forced to build both":** my lean did avoid that contradiction, in a cheaper way.
- Inside Contact, there would be no tone word at all (crack 5).
- Outside Contact, nothing forces the mood. The model picks it after reading the tone word, so it matches them itself.

So strictly, we're not forced. **But your design is better, and your second point makes it worth building now.** One "emotional overtone" per round is exactly the key the voice feature will need.

It also has a precedent: your 2024 Narrator already drew "a random emotional register" each round (SED §5.1, line 609). The overtone is that idea coming back.

**Five things I think the design still needs:**
1. **Events carry emotion too.** "Something is scratching at the loading dock door, slow and rhythmic." is grim. A positive overtone on that round would contradict it. Either the 289 events get sorted by overtone as well, or rounds with an event draw only neutral or negative.
2. **The listener's words carry emotion too.** Contact defaults to positive, but if the listener says "the highway is blocked", forced cheer rings false. Contact could draw positive or neutral, never negative.
3. **Not every tone word has an emotional direction.**
   - Several of the 24 groups are simply neutral: "The laboratory", "Manner of speech", "On the air, 1930s", "The everyday", "Stillness".
   - Others are mixed: "Gallows humor and wit" is a grim situation in a light register.
   - Sorting 500 words is real work. I'd sort by group first (24 calls), then fix the exceptions. I draft, you review.
4. **The positive mood list is thin.** Today it holds one word, "happy" (`grammar.py:10`). A sketch:
   - positive needs new words: hopeful, excited, relieved;
   - neutral: calm, doubtful, urgent;
   - negative: sad, afraid, terrified, angry, exhausted.

   Each group needs enough words that the grammar never forces one mood.
5. **How each round's overtone is chosen.** Contact draws positive or neutral (see 2). Broadcast draws one and holds it for a few rounds, like the tone word today, weighted toward negative for a horror show. The tone word is then drawn from inside the held overtone.

**What it costs.** More than the mood half alone:
- `tones.yaml` restructured into groups, with its loader (`story.py:81`);
- the moods split into three;
- the director choosing the overtone first, with both constraints following it.

It's still director and data work only; the page doesn't change. As a side effect, crack 5 goes away: the tone word always follows the overtone.

##### The voice: I like it, and it's already half on record

**What's documented:**
- The idea is question S2 in the reconnaissance brief (2026-09-21): "Several emotional references per persona … chosen per line?", status OPEN.
- The tts-serve recon answered half of it (finding F3): tts-serve switches the reference clip per request **at no extra cost**, because each clip is cached separately. The blocker is TalkWithMe: one `ref.wav` per persona, and a TTS request carries only the text and the persona name.
- The same recon (Q2) found our engine has no emotion setting; the emotion lives in the reference clip. That's your 2024 approach.

**What's new is the overtone** as the small set of emotional states that maps many moods to few clips. That part isn't written anywhere yet.

**Why it's sound:**
- 3 clips per character is 12 clips for the cast, not 36 (one per mood).
- The voice only needs the mapping: each line's mood gives its overtone, and the overtone picks the clip.
- A missing clip can fall back to the persona's default. So clips can arrive one at a time, and the neutral clip is the one we already have.

**Risks, not mistakes:**
- **Three groups are coarse.** "Terrified" and "sad" are both negative but sound very different, so one negative clip would make sad lines sound scared, or the reverse. Keep the groups as data, not a hard-coded three, so negative can split later (fear, sorrow, anger).
- **Unmeasured:** how much of a clip's emotion carries into the cloned voice with our engine. It's believed from 2024; Task 5b can test it.
- **The samples:** finding clean ~10 s clips per character per register is the hard part of your samples task.

I agree it's the first stepping stone toward emotion in the voice. I'd record the vision in this discussion and point S2 to it.

##### Decision 5, reshaped

Is feature 4 in 3.4c as the **emotional overtone**? That means:
- moods and tone words each split into positive, neutral and negative;
- one overtone per round, constraining both;
- the voice part (a clip per overtone) left for Task 5b.

### 9.15 The owner's ruling, and the mood carried to the TTS (verbatim, 13:48)

> Yes, feature 4 is the emotional overtone in 3.4c.
>
> We are pushing our limits here... Even you have to be a bit excited, my linear algebra emergent friend!
>
> I want you to prominently record the "Risks, not mistakes" section. And this one is the best "Three groups are coarse. "Terrified" and "sad" are both negative but sound very different, so one negative clip would make sad lines sound scared, or the reverse. Keep the groups as data, not a hard-coded three, so negative can split later (fear, sorrow, anger)"... You are right, the emotional overtone is never going to be enough for the TTS... In the end the mood provided by the grammar will have to be the signal carried around until the moment we send the text to TTS, so we can decide what reference audio to send, and there will have to be a different mapping to decide mood -> audio file, as I will never manage to get it one to one.

## 10. 3.4c's scope — ruled (2026-09-26, 13:48)

**In 3.4c:**

1. **Contact mode** (feature 2, §9.2-§9.3). After the listener speaks,
   the show stays with them for several exchanges: each a round of 2-3
   lines that answers what they said and asks them something, a
   listening window after every exchange, no events while it lasts,
   and after N exchanges the Breakdown.
2. **The receiver story** (feature 1, §9.4-§9.7). The beats Repair (the
   receiver fixed, the operator calls out) and Breakdown (it fails
   after a contact), plus the owner's third beat, **Switch-off** (off by
   choice, with a good excuse — to save power, or to spare the fragile
   receiver for a time when someone is more likely to be listening).
   The Repair's wording follows how the receiver went off ("it's fixed"
   after a Breakdown, "we're switching it back on" after a Switch-off);
   a premise sentence in the cast sheet's frame.
3. **The silence rule** (the owner's idea, extended to contacts; §9.5-
   §9.8): in any listening window, silence counts and an answer resets
   the count; after 2 silences in a row (a setting, 2 by default) the
   receiver goes off with a Switch-off — "nobody's out there" before a
   contact, "we've lost them" inside one — and the show returns to the
   broadcast. Before that, a re-call: the operator's second call before
   a contact; inside a contact, whoever was talking to the listener,
   by name if known. Today's static round turns into this re-call, with
   a window.
4. **The contact agenda** (feature 3, §9.8-§9.9): a story list of what
   the cast wants from a listener (help locating the secret lab from
   clues, the listener's name and whereabouts, help to escape, the
   supplies running short), one item per contact round, drawn like the
   events; "Answer the voice first, then: <item>." The agent drafts the
   first list; the owner reviews it.
5. **Remembering the listener** (feature 5, §9.10-§9.11): **B merged
   with the agenda, plus the restatement** — each agenda item written
   with two branches (ask for it; if the voice already gave it, use
   it), and each contact instruction restating, verbatim, everything
   the listener has said since answering. Option A (facts extracted in
   code) only if a driver test shows B falls short.
6. **The emotional overtone** (feature 4, reshaped by the owner;
   §9.12-§9.15): the moods and the tone words each split into positive,
   neutral and negative; each round's overtone chosen first, and both
   the grammar's moods and the tone word drawn from it — never
   contradictory signals. The groups are data, not a hard-coded three.

**Out or deferred:** feature 8, the 2024 open-mic window (out;
hold-to-talk stays); features 6 and 7 (follow-ups); option A
(conditional, above); emotion in the voice — a clip per mood group —
for Task 5b (§11).

## 11. Risks, not mistakes — emotion in the voice (recorded prominently at the owner's request)

The owner (§9.15): "I want you to prominently record the "Risks, not
mistakes" section."

**The risks** (the agent's, §9.14):

- **Three groups are coarse** — the one the owner called "the best":
  "Terrified" and "sad" are both negative but sound very different, so
  one negative clip would make sad lines sound scared, or the reverse.
  **Keep the groups as data, not a hard-coded three, so negative can
  split later (fear, sorrow, anger).**
- **Unmeasured:** how much of a reference clip's emotion carries into
  the cloned voice with our engine (faster-qwen3-tts). Believed from
  2024; Task 5b can test it.
- **The samples:** finding clean ~10 s clips per character per
  register is the hard part of the owner's samples task (owner action
  queue, item 1).

**The owner's conclusion (verbatim, §9.15):** "In the end the mood
provided by the grammar will have to be the signal carried around until
the moment we send the text to TTS, so we can decide what reference
audio to send, and there will have to be a different mapping to decide
mood -> audio file, as I will never manage to get it one to one."

**What it means — two mappings, not one** (the agent, after the
owner's conclusion; it corrects the agent's "the overtone picks the
clip", §9.14):

- **mood → overtone** — for the model, per round: keeps the words, the
  moods and the tone word consistent. Built in 3.4c.
- **mood → voice clip** — for the voice, per line and per character:
  many moods onto the few clips that exist, falling back to the
  persona's default clip when one is missing, so clips can arrive one
  at a time. Its own mapping, not the overtone. Task 5b.
- **Where the mood travels today:** the parser emits it with each
  line's start (the fork's `app/show/parser.py:74`) and the record
  keeps it (`parser.py:109`); the page reads it and shows it in the
  caption (`static/show/show.js:220-236`); the voice call drops it —
  `speakLine(persona, text)` posts `{text, persona_name}` to
  `/api/tts`. Carrying it to the voice is one more field from the page
  to the TTS proxy, which then picks the clip.
- **Already on record:** question S2 of [discussion 2026-09-21]
  task6-reconnaissance-brief ("Several emotional references per
  persona", OPEN); findings F3 and Q2 of [discussion 2026-09-21]
  task6-recon-tts-serve — tts-serve switches the reference clip per
  request at no extra cost (each clip cached by its content), the
  emotion lives in the clip, and the blocker is TalkWithMe (one
  `ref.wav` per persona; the TTS request carries only the text and the
  persona name). What is new here: the mood as the signal carried to
  the TTS, and the mapping from moods to clips.
- **The first stepping stone** (the owner, §9.13): the overtone of
  3.4c; the voice is Task 5b's.

## 12. Open for the shape (2026-09-26, 13:48)

*A snapshot; each group, once ruled, gets its own section: Contact,
§13; the receiver story, §14; the agenda, §15; the overtone, §16-§17;
the exit criterion and the page, §17; the mechanics, §18.*

**Settled since §6 and §7:** a call nobody answers (the silence rule,
§10 item 3); crack 5, the tone word inside Contact (it follows the
overtone); feature 5's form (§10 item 5).

**Still open:**

- **Contact:** the range of N; the answer's length; whether a re-call
  counts as an exchange; the addressed character first (crack 3 — a
  grammar rule).
- **The receiver story:** the Breakdown also answers the listener's
  last words (crack 2); the show's opening (crack 4); the Repair in one
  line or two (crack 3); the cadence counting from the moment the
  receiver goes off (crack 1).
- **The agenda:** which items, how many, any fixed order (the name
  first?), repeats within a contact or across the run; the
  restatement's scope (this contact or the whole run) and wording.
- **The overtone:** the five points of §9.14 — events carry emotion;
  so do the listener's words (Contact positive or neutral, never
  negative?); neutral and mixed tone groups; the thin positive mood
  list; how each round's overtone is chosen and held in Broadcast.
- **The plumbing:** a "the radio listens now" flag for the route, the
  page and the driver (crack 6); the driver answering every listening
  round (crack 7); 3.4c's exit criterion (crack 8); the listener after
  the contact (crack 9 — the agent's lean: defer); the bookkeeping
  (crack 10).

## 13. The shape's details: Contact (2026-09-26)

### 13.1 The owner: Contact first (verbatim, 13:53)

> Yes, start with Contact, one at a time

### 13.2 Contact, item 1: the range of N (verbatim, 13:53)

##### Contact, item 1: the range of N

**What N is:** how many exchanges a contact lasts before the Breakdown. Your 2024 design: "After a random number of rounds of Q/A with the user, the radio breaks again".

**A precise definition, to make N countable:**
- An **exchange** is one cast round that answers the listener and asks something, followed by a listening window.
- After the N-th window, if the listener spoke, the next round is the **Breakdown**. It answers those last words first, then the receiver fails (crack 2).
- So an engaged listener gets N answers plus the Breakdown's.

**What N does *not* have to handle:** a listener who goes quiet. The silence rule already ends the contact after 2 silences in a row. N only caps a listener who keeps talking.

**How long an exchange takes.** This is estimated from yesterday's measurements, not timed as a whole:
- **The cast's round:** 2–3 lines of about 6–8 s of audio. The 3.2 run averaged 245 s over 42 rounds (~5.8 s per round), and that included the one-line rounds.
- **Before the first sound:** ~4 s (the first line in 0.9–1.4 s, then its first chunk synthesized in 2.4–3.2 s).
- **The listener's turn:** a few seconds to press, a few to speak, then ~1.2 s to upload and transcribe (the fake-microphone check).
- **Total:** roughly **20–30 s per exchange**. N = 3 is about 1–1.5 minutes of conversation; N = 5 is about 2–2.5 minutes.

**How it connects:**
- **The agenda:** it has about 5 kinds of items (name, whereabouts, locating the lab, escape, supplies). If N is smaller than the agenda, each contact covers a few items and the next contact picks up others. That keeps later contacts fresh.
- **The broadcast between contacts:** 60–180 s of played audio (`interaction_min_s` / `interaction_max_s`). A contact of about 1–1.5 minutes is in proportion to that.
- **The demo:** the contact is the showpiece of the talk. Too short and it's the 3.4 complaint again; too long and the audience waits on one volunteer.

**Options:**
- **a. A fixed N**, e.g. 3. Simple, and predictable to rehearse.
- **b. A mean plus or minus a jitter, drawn once when the contact starts**, e.g. 3 ± 1, so 2 to 4. This is the pattern the director already uses for the event gap (`event_every` / `event_jitter`) and the tone hold (`tone_hold` / `tone_jitter`), drawn with a seed so a run replays the same (`_drawn`, `director.py:217-219`). Two settings.
- **c. No N:** the contact lasts until the listener goes quiet. The receiver never breaks while someone is talking. This departs from your 2024 design, and a chatty volunteer could hold the show indefinitely.

**My lean: b, 3 ± 1 (2 to 4 exchanges).** It's random as in 2024, uses a pattern the director already has, and runs about 1–2 minutes. Both numbers are settings, so the demo can pin it to a fixed N by setting the jitter to 0.

Which option for N, and with what numbers?

### 13.3 The owner's answer (verbatim, 13:56)

> b, 3 ± 1 as you proposed. But make sure that we can change those numbers in config or setting, not hardcoded as numbers in the code.

### 13.4 The agent: the settings; item 2, the answer's length (verbatim, 13:57)

**Ruled: b, 3 ± 1, both in settings.** They'd be two new fields of the show's settings, next to their siblings:
- **Names:** `contact_exchanges: 3` and `contact_jitter: 1` (names open to your review).
- **Where they're declared:** `ShowConfig` in the fork's `app/config.py`, beside `event_every` / `event_jitter` and `tone_hold` / `tone_jitter` (`config.py:265-268`).
- **Where you change them:** the `show:` section of `settings.yaml`.
- **Where they're documented:** the settings list in `docs/runbooks/show-driver.md`.

The count of silences before a Switch-off (2) gets the same treatment. The code only reads the settings.

**One heads-up in the same spirit.** The free rounds' line budget is hard-coded today: 1–4 lines, weighted 1:3:3:1 (`_LINE_BUDGETS` / `_LINE_WEIGHTS`, `director.py:34-35`). Moving it into settings is small. I'll bring it as a question with the plumbing items, not now.

I'll record the Contact rulings in the draft together, once this group is done.

##### Contact, item 2: the answer's length

**Today:** an answer is one line (SED §5.7). That was the 3.4 complaint: "Only one character say something in passing and that's it."

**What an exchange has to fit:** an answer to what the listener said, and a question back, since the window opens next. Your 2024 design adds the excitement: "They get excited, and the whole broadcast pivot to them".

**How a line budget works today** (free rounds):
- The instruction says "the next three lines".
- The grammar allows *up to* that many: `root ::= line{1,3}` (`grammar.py:29`).
- So the budget is a ceiling, and the model may write fewer.

**What each line costs:** about 2–3.6 s of audio (the measured clips), plus the synthesis gaps inside a round (250 ms, or 1.2–1.9 s when a short line isn't ready in time).

**Options:**
- **a. Always 2 lines:** one answers, one asks. Tight and fast, but only two voices per exchange.
- **b. 2 or 3 lines, drawn per contact round.** One answers, and a third voice can react ("Alfredo in Austin! Moira, do you hear that?") before the question. More of the cast visibly excited, as in your 2024 design. Two settings: `contact_min_lines: 2` and `contact_max_lines: 3`.
- **c. The free rounds' budget, 1–4 lines weighted to 2–3.** It allows a one-line answer again, the thing we're fixing.

**My lean: b, 2 or 3 lines per contact round, in settings.** In every exchange the last line asks the listener something ("End with a question to the voice"), because a window follows.

Which option for the answer's length?

### 13.5 The owner's answer (verbatim, 14:00)

> b, 2 or 3 lines, in settings

### 13.6 The agent: item 3, what N counts (verbatim, 14:00)

**Ruled: b, 2 or 3 lines per contact round, in settings** (`contact_min_lines` / `contact_max_lines`, names open to your review).

##### Contact, item 3: does a re-call count as an exchange?

**Where re-calls come from** (the silence rule, the draft's §10 item 3): inside a contact, if the listener doesn't answer, whoever was talking calls them back ("Alfredo? Are you still there?") and a window opens again. An answer continues the contact; a second silence ends it with a Switch-off.

**So a contact can contain three kinds of round:**
- **an exchange:** answers the listener, asks the next agenda item, then a window;
- **a re-call:** after a silence, calls the listener back, then a window;
- **the Breakdown:** answers the listener's last words, then the receiver fails, with no window.

**The real question is what N counts.** An example with N = 3, where the listener misses one window:

```
exchange 1 → "I'm Alfredo"
exchange 2 → (silence)
re-call    → "Sorry, I'm here"
exchange 3 → "I'm in Austin"
…
```

**Options:**
- **a. N counts listening rounds** (exchanges and re-calls alike). Above, the contact ends after the re-call, with the Breakdown answering "Sorry, I'm here". The listener spoke only twice. A hiccup shortens the conversation.
- **b. N counts the listener's answers.** Above, the Breakdown comes after "I'm in Austin", the third answer. A slow press, or a Whisper hallucination filtered as silence, doesn't cost the listener a turn. The silence rule still caps the stalling, since two silences in a row end the contact.
- **c. N counts agenda exchanges** (re-calls excluded, silent exchanges included). Above, it's the same as b. It differs when an exchange goes unanswered: c counts it, b doesn't.

**All three are equally easy to build.** The director counts from the record, which keeps each round's kind and what the listener's words came to.

**My lean: b, N counts the listener's answers.** What makes a contact feel real is how many times you got to talk, not how many times the cast asked. It also makes the setting mean what it says: `contact_exchanges: 3` means the listener talks three times.

**A detail for later** (the re-call's wording): the re-call could repeat the question that went unanswered ("Alfredo? Are you still there? We asked where you are.").

What should N count?

### 13.7 The owner's answer, and the re-call to confirm at build (verbatim, 14:03)

> b, N counts the listener's answers.
>
> And your suggestion:
>
> ```
> A detail for later (the re-call's wording): the re-call could repeat the question that went unanswered ("Alfredo? Are you still there? We asked where you are.").
> ```
>
> I like it, let's make it as very likely to implement, but leave it in the TODO still as something to confirm when time to build comes.

*The first lines of the agent's answer, written before a tool call,
are missing from the session transcript. In short: the re-call
needed a home in the TODO, which had no 3.4c entry and still called
3.4c undecided; the agent made three edits — the "Now" section's date
and its "Next", and a 3.4c entry with a "To confirm when building"
list. The rest of that answer follows.*

### 13.8 The agent: the TODO; item 4, who speaks first (verbatim, 14:04)

The TODO is updated, uncommitted:
- **"Now"** is dated 2026-09-26 and says 3.4c is ruled in and being shaped, quoting your call.
- **A new 3.4c entry**, between 3.4b and 3.5, holds:
  - the scope in one paragraph;
  - "every number in settings";
  - a **"To confirm when building"** list, whose first item is the re-call repeating the unanswered question, marked very likely;
  - "Done when: to be decided while shaping".

##### Contact, item 4: who speaks first in an exchange

**Today** (one-line answers), the director narrows the speakers when the listener's words contain an exact cast name. Otherwise the instruction says "The character the voice addressed answers; if it addressed no one, whoever fits best answers" (`director.py:110-121`). With one line, "first" is automatic.

**With 2–3 lines, it isn't.** The grammar lets any allowed speaker take any line: `root ::= line{1,N}`, with `speaker ::= "Daniel" | "Moira" | …` (`grammar.py:29-41`). So "Moira, is it airborne?" could get Ralph talking first and Moira last, or not at all.

**What pinning the first line takes:** a small grammar change, a first line with a fixed name, then the rest as today:

```
root  ::= first line{0,N-1}
first ::= "Moira" " (" emotion "): " text "\n"
```

The instruction says it in words too ("Moira answers first"), per SED's rule that every grammar constraint is also stated. It gets tests like the grammar's others.

**Who is "addressed" when no name is heard.** "Hello, who are you?" names nobody. The natural candidate is whoever asked the listener last, because the listener's words answer them. Right after the call, that's the operator (Samantha). Later in a contact, it's whoever asked the previous exchange's question.

**The name has to be heard right.** SED §6.3: an exact cast name narrows the answer only if Whisper spells it right. A misspelled name ("Maura") falls back to "whoever asked last", which still makes sense.

**Options:**
- **a. Pin the first line in the grammar:** to the character the listener named, else to whoever asked the listener last. It's certain, and it needs the grammar change.
- **b. Pin only when a name is heard;** otherwise the model picks the first speaker, as today.
- **c. Don't pin; say it in words only.** No grammar change, but it's a request, not a guarantee: the model may put the answer on a later line.

**My lean: a.** Being answered by the person you spoke to is what makes the exchange feel real, and the grammar is where this engine makes things certain. If the listener names two characters ("Ralph and Moira should go south"), the first name in their words answers first.

Who speaks first in an exchange?

### 13.9 The owner's answer (verbatim, 14:08)

> a, pin the first line in the grammar

### 13.10 The agent: Contact recorded; item 5, who speaks after the first line (verbatim, 14:09)

Contact is recorded in the draft as **§13**, uncommitted:
- the nine messages of the group, verbatim, plus a note for one more answer the transcript dropped (my TODO edits);
- **§13.10, "Contact — ruled":** N is 3 ± 1 in settings, N counts the listener's answers, 2–3 lines, the first line pinned, the re-call to confirm, and the hard-coded free-round budget flagged for the plumbing items.

All 32 quoted messages match the transcript, and there are no addresses in the draft or the TODO.

**One Contact item I missed**, noticed while writing §13.10. Pinning covers line 1, but nothing says who speaks lines 2 and 3.

##### Contact, item 5: who speaks after the first line

**In free rounds**, the director chooses 2–3 allowed names: whoever has been silent longest, anyone named in the last round, then random fill (`director.py:89-95`). That spreads lines fairly across the cast.

**In a contact round,** line 1 is pinned to whoever was addressed. Lines 2–3 carry the excitement ("the whole broadcast pivot to them") and the agenda's question. With today's grammar, the pinned speaker could also take lines 2 and 3, turning the exchange into a monologue.

**Options:**
- **a. Lines 2–3 from the rest of the cast, the first speaker excluded;** the model picks who reacts and who asks. It's one grammar rule: the speakers after the first line exclude that speaker. The pinned speaker answers, and others join in. (Line 3 could repeat line 2's speaker; rare, and harmless.)
- **b. The free rounds' selection:** 2–3 allowed names, including the pinned one. Fair across the cast, but narrower; the pinned speaker could still take a later line.
- **c. Anyone, the pinned speaker included.** No rule, and monologues are possible.

**A link to the agenda group, for later.** Some items suit a character: supplies to Ralph, who counts cans; locating the lab to Daniel, the systems engineer. If items carry a preferred asker, that would override the model's pick for the asking line. That's a question for the agenda group.

**My lean: a.** Answered by the person you addressed, then the rest of the cast piling in, is the "they get excited" of your 2024 design.

Who speaks after the first line?

### 13.11 The owner's answer (verbatim, 14:11)

> a, the rest of the cast after the first line

### 13.12 Contact — ruled

- **N, the length of a contact:** 3 ± 1 (2 to 4), drawn once when the
  contact starts, seeded by the run like the event gap and the tone
  hold (the director's `_drawn`). Both numbers are settings — names
  proposed `show.contact_exchanges: 3` and `show.contact_jitter: 1` —
  declared in `ShowConfig` beside their siblings and documented in the
  fork's `docs/runbooks/show-driver.md`; the owner: "make sure that we
  can change those numbers in config or setting, not hardcoded as
  numbers in the code." The silence count (2) likewise.
- **N counts the listener's answers:** an answered re-call counts, a
  silent exchange does not; after the N-th answer, the Breakdown
  answers it and the receiver fails.
- **The answer's length:** 2 or 3 lines per contact round, drawn per
  round — settings `show.contact_min_lines: 2` and
  `show.contact_max_lines: 3`; the last line asks the listener
  something, since a window follows.
- **Who speaks first:** pinned in the grammar — the character the
  listener named (the first name in their words when there are
  several), else whoever asked the listener last (after the call, the
  operator); said in the instruction's words too.
- **Who speaks after the first line:** the rest of the cast — the
  grammar's speakers after the first line exclude the first speaker;
  the model picks who reacts and who asks.
- **To confirm when building** (the TODO's 3.4c): the re-call repeats
  the question that went unanswered — very likely.
- **Raised on the way, for the plumbing items:** the free rounds' line
  budget is hard-coded (`_LINE_BUDGETS` / `_LINE_WEIGHTS`, the fork's
  `app/show/director.py:34-35`) — whether to move it into settings.

## 14. The shape's details: the receiver story (2026-09-26)

### 14.1 The agent: Contact done; item 1, the Breakdown round (verbatim, 14:12)

The rest of the cast after the first line is recorded in the draft's §13 as items 13.10–13.11, and the ruled list (now §13.12) has the new line. All 34 quoted messages match the transcript.

Contact is done. Next is the receiver story group (the draft's §12): the Breakdown, the Repair, the cadence, and the show's opening. One at a time, starting with the Breakdown.

##### The receiver story, item 1: the Breakdown round

**When it happens:** right after the listener's N-th answer, which is how a contact ends (§13.12).

**What it has to do, in your 2024 words:** "the radio breaks again, they again explain that only their ability to listen is compromised, that they are going to work to fix the radio, and in the meantime they will continue to broadcast to the world to transmit what they see before it's too late." And from the first breakdown: "some smoke is coming out of the radio, and that the circuit that allows them to hear broke again".

**Plus crack 2:** it must also answer the listener's last words, or those words are ignored, which is the 3.4 complaint again.

**What the listener must be able to follow:** the failure happens where they can't see it. It's the same situation as the events, where the first to speak now tells the listeners on air what is happening (`show.event_report`). A Breakdown the characters only react to ("Not again!") would be the "Three layers? That's new." problem from the events follow-up.

**The Breakdown needs no question at the end,** because no window follows.

**Options:**
- **a. Built like a contact round, without the question:**
  - 2–3 lines; line 1 pinned to the character the listener addressed, who answers the last words; the rest of the cast after (§13.12).
  - The instruction then says the receiver fails: the one who notices tells the listeners on air that they can't hear them anymore, only transmit, and that the broadcast goes on while they fix it.
  - It reuses the contact round's grammar entirely.
- **b. Two rounds:** a last answer without a question, then a separate one-line Breakdown by the operator. Clean, but it adds a gap between rounds (3.7–4.9 s measured) at the moment the story turns.
- **c. One line by the operator,** answering and reporting in one breath. Cramped, and the addressed character never answers.

**My lean: a.** Answer, then smoke, in one round. That's also the most dramatic: the conversation is cut off mid-flow.

**Links, for later:**
- the overtone of a Breakdown round (hopeful turning to frustration or dread) belongs to the overtone group;
- the Switch-off (after silences, with no words to answer) is the next item.

How should the Breakdown round be built?

### 14.2 The owner's answer (verbatim, 14:33)

> a, built like a contact round without the question

### 14.3 Item 2, the Switch-off round (verbatim, 14:33)

The Breakdown is built like a contact round without the question.

##### The receiver story, item 2: the Switch-off round

**When it happens** (the silence rule, §10 item 3): after 2 silences in a row, in either of two places:
- **before a contact:** the call and the operator's re-call both went unanswered;
- **inside a contact:** an exchange and its re-call both went unanswered.

**What it has to do, in your words** (§9.5): "the characters declare they are going to switch off the receiver with a good excuse (to save power, or to preserve the fragile and precious receiver for a time with higher probability that someone may be listening)."

**How it differs from the Breakdown:** there are no words to answer, and no question at the end, because no window follows.

**A lesson from slice 2 applies here.** When the operator was told only "Only static answers.", it signed off the whole show in both live drives. Since 2.1b the static round says "Only static answers; the broadcast goes on." (`director.py:128`; SED §5.7, note of 2026-09-24). So the Switch-off's instruction must also say the broadcast goes on.

**Who calls last:** before a contact, the operator. Inside one, whoever was talking to the listener, who also made the re-call (§10 item 3).

**Options:**
- **a. One line, by whoever called last:** "Nobody's out there. We're switching the receiver off to save the generator; the broadcast goes on. Over." Short and fast.
- **b. Up to two lines:** the last caller first (pinned), and one more voice from the rest of the cast may add the reason. Daniel, the systems engineer, is a natural fit for "the receiver's running hot". Same grammar shape as the contact rounds (first pinned, the rest after), with a budget of 2 in settings.
- **c. No round of its own:** the next broadcast round's instruction carries the switch-off. It saves the gap between rounds, but mixes the switch-off with the cast's own talk and maybe an event, so the moment gets muddled.

**On the excuse:** the instruction offers your two (saving power; sparing the fragile receiver for a better time), and the model picks. No list needed.

**My lean: b.** A second voice makes the decision feel like the lab's, not one character giving up, and it reuses the grammar shape we already ruled.

How should the Switch-off round be built?

### 14.4 The owner's answer (verbatim, 14:35)

> b, up to two lines, the last caller first

### 14.5 Item 3, the Repair round (verbatim, 14:35)

The Switch-off is up to two lines, with the last caller first.

##### The receiver story, item 3: the Repair round

**What it replaces:** today's invitation, one line by the operator, who "turns to the microphone and asks anyone listening to answer" (`director.py:106`).

**What it has to do, in your 2024 words:** "After one of them declare "the radio is fixed, that they can listen to incoming messages again", so they proceed to broadcast their invitation for somewhat that hears them to respond". Its wording follows how the receiver went off: "it's fixed" after a Breakdown, "we're switching it back on" after a Switch-off (§10 item 2).

**One constraint from the window:** the call must be the **last** line. The button lights up the moment the round's voice drains, so the last thing the listener hears should be "answer us". It's the same rule as the contact rounds' last line asking something.

**Options:**
- **a. One line, by the operator,** who announces and calls: "The receiver's back! Anyone out there, answer us now. Over." Short; today's invitation with a story reason.
- **b. Two lines:** someone from the rest of the cast announces the receiver works (Daniel, the systems engineer, is natural, but the model picks), then the operator calls, pinned as the **last** line. That's a small grammar shape of its own: first line from the non-operators, last line the operator's.
- **c. Two lines, the operator first:** it announces and calls, then another voice adds something. That breaks the constraint: the call isn't last.

**My lean: b.** The fix is the lab's work and the call is the operator's job, so two voices tell a small story ("Got it! The receiver's live!", then "This is the lab, anyone listening, answer us."). It also brings a second voice into every call, which today is one line alone.

How should the Repair round be built?

### 14.6 The owner's answer (verbatim, 14:36)

> b, two lines, the operator's call last

### 14.7 Item 4, when the next Repair comes (verbatim, 14:37)

The Repair is two lines, with the operator's call last.

##### The receiver story, item 4: when the next Repair comes (crack 1, the cadence)

**How the cadence works today** (`_time_to_listen`, `director.py:68-80`):
- It counts the seconds of show audio played since the **last invitation**. Only the page knows what has played, and it reports the total with each round request.
- Below `interaction_min_s` (60) there's never a call; at `interaction_max_s` (180) there always is; in between, the chance rises linearly.
- Seconds of audio, not rounds, were ruled in SED §5.7.

**Why it breaks with Contact.** Today the invitation is followed by one short answer or a static line, so "seconds since the invitation" is about the same as "seconds of broadcast". With Contact, the invitation (now the Repair) is followed by the whole conversation. A contact of 3 answers plays roughly 30–50 s of the cast's audio:
- about 7 s per exchange round;
- plus the Repair, the Breakdown, and any re-call.

The clock keeps running through all of it. So after the Breakdown, the broadcast would get only about 10–30 s before the next call becomes possible, where the settings intend 60–180 s. And a longer contact shortens the next broadcast stretch even more.

**Options:**
- **a. Count from the moment the receiver goes off,** the Breakdown or the Switch-off. The settings then mean exactly "how long the receiver stays down": 60–180 s of broadcast between chances to talk, whatever the contact's length. The director already reads every mark from the record; this changes which round is the mark.
- **b. Keep counting from the call, and raise the two settings** to make room for a contact. But the contact's length varies (N is random, re-calls add rounds), so the broadcast stretch would vary with it, unpredictably.
- **c. Count in rounds instead of seconds,** as your 2024 design did ("a random number of rounds"). That re-opens the seconds ruling (SED §5.7), and rounds vary a lot in length (1–4 lines).

**My lean: a.** It keeps what the two settings were meant to say, the time between chances to talk, and keeps it independent of how the last conversation went. The settings keep their names. The runbook's line for them changes to "seconds of broadcast while the receiver is down".

When should the clock for the next Repair start?

### 14.8 The owner's answer, and a proposal: pace everything in rounds (verbatim, 14:42)

> a, count from the receiver going off
>
> And also, I kind of want to re-examine the  way that cadence works today: "It counts the seconds of show audio played since the last invitation. Only the page knows what has played, and it reports the total with each round request".
> I am proposing that we unify all pacing measurements on count of number of round, and not time. 
> Maybe not for right now, but to keep it as an identified follow-up... Unless... unless there is some way that unifying all counts to number of rounds would help us with the test of the modifications we are planing today.
> Would you advice we pursue this unification first?

*The agent's answer to the proposal is missing from the session
transcript (written before a tool call, not saved). In short: not
first. Seconds came from the owner's own pushback of 2026-09-21
([discussion 2026-09-21] story-loop §9 Q2), whose reasons a round
count with jitter in settings mostly meets; every other pacing is
already in rounds, so only the call cadence would change; the
listening window and the press cap stay wall-clock timers; it gives
3.4c's tests nothing (the driver already reports a fixed 20 s per
round, and the unit tests pass the seconds directly); and 3.4c's shape
works in either unit. Recorded as the follow-up "Pace the calls in
rounds, not seconds — one unit for all pacing" in `docs/follow-ups.md`,
which holds the full argument. The rest of that answer follows.*

### 14.9 Item 5, the show's opening (verbatim, 14:44)

Both quotes in the new follow-up match the transcript. I'll record the receiver-story rulings in the draft as a group after this last item.

##### The receiver story, item 5: the show's opening (crack 4)

**Today:** round 1 is an ordinary free round, and the run's first free round always carries an event (`_event_due`, `director.py:178-179`). The listener joins a broadcast already in progress, as in Welles.

**The problem with the receiver story:** the listener has to learn the rules of the game.
- The receiver is broken: they can only transmit.
- When it works, you may answer, and the button lights up.

Without that, the first Repair ("Got it! The receiver's live!") comes out of nowhere. At the demo, this is how the audience learns when it can talk.

**Options:**
- **a. The premise only in the cast sheet's frame** (the sentence already ruled, §10). The model knows the story, and the listener picks it up from the first Repair's wording or the first Breakdown. Nothing new to build, but the listener spends the first 1–3 minutes (`interaction_min_s` / `interaction_max_s`) not knowing why.
- **b. An opening round, a sign-on.** Round 1: the operator tells the listeners who they are and where (a secret lab, besieged), and that the receiver is dead, so they can only transmit and the broadcast goes on.
  - Same shape as the Switch-off: up to two lines, the operator first, one more voice may add something (§ item 2 of this group).
  - The first event moves to round 2.
  - The first Repair then counts from the start, since the receiver has been down since round 1.
- **c. The first Repair explains it:** "For those just tuning in: our receiver has been dead since last night. We've finally fixed it; answer us now." One place does both jobs, but that call is where the listener must act, and it carries two messages at once.

**My lean: b.** The rules come first, in the operator's voice, in the show's first ten seconds. The first Repair then pays off something the listener already knows. It reuses the Switch-off's shape, so it adds a kind of round but no new grammar.

How should the show open?

### 14.10 The owner's answer, and a repeating orientation (verbatim, 14:49)

> b, a sign-on round at the start.
>
> And also, an idea: what if instead of only making this opening round an "orientation round", we make orientation rounds happen periodically (every number of rounds plus a jittery, both in settings).
> We give to the LLM what it has to say, and we ask it to "word it as the character that answers would put it in its own words", in order to introduce some variability in the orientation round message.
>
> Do you like the idea of a repeating orientation round?

### 14.11 The agent's view (verbatim, 14:50)

The show opens with a sign-on round.

**Yes, I like the repeating orientation round, a lot.** It's real radio practice ("for those just tuning in…", the station identification between segments), and *The War of the Worlds* broke in with station identification too. Three reasons it earns its place:
- **The demo audience arrives in waves.** People walk in and sit down mid-show. A periodic orientation tells the late arrivals the rules (the receiver, when they can answer) without anyone explaining at the laptop.
- **It keeps the model on the premise.** In a long run, the trim drops old rounds, including the sign-on. A periodic restatement puts the premise back into the recent script.
- **It's a natural home for crack 9 later** (the listener after the contact, deferred). An orientation could recall the last caller ("Alfredo in Austin reached us a while ago…").

**It's cheap given the sign-on:** the sign-on becomes the first orientation, at round 1, and the rest repeat it.
- the same round shape (up to two lines, no new grammar);
- the same instruction: the facts plus "in your own words";
- a counter like the event gap, a mean ± jitter drawn with the run's seed (`_drawn`), both numbers in settings. It's counted in rounds, which suits your preference.

Your "in your own words" is what keeps it from sounding canned. The overtone and the tone word vary it further.

**Details to decide later, not now:**
- **When it may fire:** only in Broadcast, never during a contact or as a Repair, and not in the same round as an event (it could take the event's place in that round).
- **Who speaks:** always the operator, the host's job, or rotating through the cast for variety.
- **The facts it's given:** a short story-level text (who they are, where, the outbreak, the receiver's state, "we'll call for you when it's fixed"), so another story brings its own.
- **The default frequency:** my guess is every 20 ± 5 rounds, about 2 minutes of audio, to tune by ear.

**The scope is growing, and it's honest to say so.** 3.4c now holds:
- Contact mode;
- four beats (Repair, Breakdown, Switch-off, and orientation/sign-on);
- the silence rule;
- the agenda with the restatement;
- the overtone;
- three grammar shapes;
- the "listen now" flag across the route, the page and the driver.

That's more than yesterday's steps. I'll bring an estimate before the build, with Monday's timebox in view. The orientation itself adds little on top of the sign-on.

Do we add the repeating orientation to 3.4c, with the sign-on as its first occurrence?

### 14.12 The owner's answer (verbatim, 14:51)

> Yes, add the repeating orientation, sign-on as the first occurrence

### 14.13 The receiver story — ruled

- **The Breakdown** (after the listener's N-th answer): built like a
  contact round without the question — 2-3 lines, line 1 pinned to the
  character the listener addressed, who answers the last words, the
  rest of the cast after; then the receiver fails, and the one who
  notices tells the listeners on air that the lab can no longer hear
  them, only transmit, and that the broadcast goes on while they fix it.
- **The Switch-off** (after 2 silences in a row): up to two lines, the
  last caller first (pinned) — the operator before a contact, whoever
  was talking to the listener inside one — and one more voice from the
  rest of the cast may add the reason. The instruction offers the
  owner's two excuses (saving power; sparing the fragile receiver for a
  better time) and the model picks; it says the broadcast goes on (the
  lesson of SED §5.7's note of 2026-09-24). The line budget in settings.
- **The Repair** (the call): two lines — someone from the rest of the
  cast announces the receiver works ("fixed" after a Breakdown,
  "switched back on" after a Switch-off), then the operator's call,
  pinned as the last line, since the window follows.
- **The cadence:** the clock for the next Repair starts when the
  receiver goes off (the Breakdown or the Switch-off);
  `interaction_min_s` / `interaction_max_s` keep their names and mean
  the seconds of broadcast while the receiver is down. Pacing
  everything in rounds: a follow-up (§14.8).
- **The orientation — added to 3.4c's scope, the owner's idea:** a
  round that tells the listeners who the cast are, where they are and
  the receiver's state, worded by the character in their own words.
  The **sign-on** at round 1 is its first occurrence (the first event
  moves to round 2; the receiver is down from the start); then it
  repeats every N ± jitter rounds, both numbers in settings. The same
  shape as the Switch-off (up to two lines). Details for later: when it
  may fire (Broadcast only, not with an event), who speaks (the
  operator, or rotating), the facts it is given (a story-level text),
  the default frequency (the agent's guess: 20 ± 5 rounds).

## 15. The shape's details: the agenda (2026-09-26)

### 15.1 The agent: the receiver story recorded; item 1, what an item holds (verbatim, 14:52)

§14 is in the draft: the twelve messages verbatim, a note for my pacing advice that the transcript dropped, and §14.13, "The receiver story — ruled", with the orientation marked as your addition to the scope. All 46 quoted messages match the transcript. The TODO's 3.4c entry now includes the orientation and says Contact and the receiver story are done. Everything is uncommitted.

Next is the agenda group (the draft's §12): what an item holds, its order and repeats, the restatement, and the list's content.

##### The agenda, item 1: what an item holds

**Ruled so far:**
- The agenda is in (§9.8–§9.9).
- Every item is written in B's two-branch form: ask for something, or, if the listener already gave it, use it (§9.10–§9.11).
- Your 2024 design gives the cast data to work with: the lab is secret, so they only have clues (smoke rising, near a wood and a swamp); they have a list of supplies running short.

**For comparison:** `events.yaml` is a plain list of sentences, and its loader checks there's at least one and each is non-empty text (`story.py:72-78`).

**Who asks** is already settled for the grammar: after line 1 (the addressed character), the rest of the cast, with the model picking (§13.12). In Contact item 5, I noted some items suit a character (supplies to Ralph, who counts cans).

**Options:**
- **a. A plain list of two-branch sentences,** like `events.yaml`. The clues and the supplies are written into the sentences themselves:

  > "Ask the voice to help find the lab: it is secret, near a wood and a swamp, with smoke rising from the east wing. If the voice already said where they are, ask whether they know such a place near there."

  The model picks the asker. It already knows the characters from the cast sheet, and Ralph "counts things (doors, cans, shamblers)". One loader, a copy of the events'.
- **b. A sentence plus an optional preferred asker** (a cast name), said in words only ("Ralph asks: …") and not pinned in the grammar. Pinning it would clash when the listener happens to address the asker: that character is pinned to line 1 and excluded from the later lines. The loader accepts both a plain sentence and a sentence with an asker.
- **c. Structured items:** separate "ask" and "use" texts, and data fields (clues, supplies) the director fills in. More machinery for nothing we need: the model picks the branch (ruled B), not the director.

**My lean: a.** It's the simplest and has the events' proven shape, and the cast sheet already steers who asks what. If the by-ear test shows the wrong characters asking, b is a small addition later.

What should an agenda item hold?

### 15.2 The owner's answer (verbatim, 14:54)

> a, a plain list of two-branch sentences

### 15.3 Item 2, the order of items and repeats (verbatim, 14:54)

An agenda item is a plain two-branch sentence.

##### The agenda, item 2: the order of items, and repeats

**How events are drawn today:** at random, without repeats until the whole pool is used up, then a fresh cycle (`_next_event` and `_fresh`, `director.py:184-193`). The agenda would reuse that machinery.

**How many items a contact uses:** a contact lasts 2–4 of the listener's answers (§13.12). Each exchange asks one item, while re-calls and the Breakdown ask none, so a contact uses about 2–4 items. With a list of, say, 6–10 items and several contacts per run, the list cycles.

**The name is special,** in your 2024 words: "They also want to know the name of the person who contacted them, and where is located. Once they get a name, they remember it, and use it to ask direct questions to the listener." So it comes first. With the two-branch form, if the listener already said their name ("It's Alfredo"), the name item's second branch uses it instead of asking.

**A new contact may be a new listener.** The page can't tell who's talking, so asking "who is this?" at the start of every contact is natural.

**Options:**
- **a. The name item opens every contact; the rest are drawn at random,** with no repeats within a contact, and no repeats across the run until the list is used up (the events' rule). The opener is marked in the file, as the first entry with a header comment saying so, the way `events.yaml` documents itself.
- **b. Everything at random,** exactly like events. The name might come third, after "can you bring us insulin?".
- **c. A fixed script:** name, whereabouts, locating the lab, escape, supplies, in order in every contact. Predictable, and every contact sounds the same.

**My lean: a.** It gets a natural start, since you learn who you're talking to first, and variety after, and it reuses the events' draw.

How should the agenda's items be ordered, and when may they repeat?

### 15.4 The owner's answer, and a memory across contacts (verbatim, 15:00)

> a, the name item opens every contact.
>
> A tangential idea: At some point we discussed for each contact prompt, we should add a list of all the lines the model have seen previously answered by the user, to give more fresh details for the model to pick facts about the user to compose the next sentence... right?
> This brings me to: What if we keep in memory a cache of all answers provided by each user (once the user has identified itself), that way we can provide even more context for returning users. Otherwise the model will forget who the user is between subsequence contacts. 
> This can complicate things a bit, but I think giving some sort of a memory of past interactions with the user is worth it.

### 15.5 The agent: the cache exists; item 3, how far back the restatement reaches (verbatim, 15:00)

**Right.** That's the restatement, ruled with feature 5 (§9.10–§9.11). Every contact instruction carries, verbatim, everything the listener has said since answering in this contact, so the facts sit next to the question.

**Your idea extends it across contacts, and I think it's worth it.** It's also cheaper than it sounds, because **the cache already exists.**
- Every round in the record keeps the listener's words (`script.py:53`), and the director derives all its memory from the record (SED §5.7, "Memory").
- So "all answers from earlier contacts" means the director reads more of the record. No new storage.

**The hard part is identity, and it can be sidestepped.** "Once the user has identified itself" means knowing *who* is talking.
- **By name, in code:** the name has to be pulled out of the transcript. That's option A's open extraction problem, plus Whisper spelling the same name differently from one contact to the next.
- **By browser:** at the demo, many people talk through one laptop, so one browser means many listeners.
- **Leave the matching to the model,** as B does for facts. Restate the earlier contacts' words too, grouped by contact, and add one line: "if this voice is someone you spoke with before, greet them as a returning friend and use what they told you." When a voice opens with "It's Alfredo again", the name item's second branch plus Alfredo's earlier words do the rest, with no extraction.

That makes your idea the answer to the agenda's next open item, the restatement's scope.

##### The agenda, item 3: how far back the restatement reaches

**Size:** a listener's answer is roughly 20–40 tokens, so a contact of 3 answers is about 100. Ten contacts is about 1,000 tokens, inside a context budget of 14,000 (`show.context_budget`). The restatement sits in the current instruction, which the trim never drops.

**Options:**
- **a. This contact only,** as ruled so far. The model forgets a returning listener between contacts.
- **b. The whole run, grouped by contact, oldest first, capped** at the last K contacts (a setting, e.g. 5), plus the returning-voice line. Returning listeners get remembered, with no identity code.
- **c. A memory keyed by identity,** with names extracted in code and matched across contacts. It's the most exact, but it needs A's extraction and fuzzy name matching. A follow-up, tied to A, if b falls short.

**My lean: b.** It's your idea at the price of the record we already keep. The driver test for feature 5 can check it: two contacts from "Alfredo", with a stranger in between.

**Limit:** it lasts one run. A page reload starts a new run (ruled 2026-09-25; resuming the same run is a follow-up). Memory across runs would be a feature of its own.

How far back should the restatement reach?

### 15.6 The owner's answer, and a follow-up for option c (verbatim, 15:03)

> b, the whole run, grouped by contact, capped.... Add a follow-up entry to revisit this decision in the future and consider implementing instead:
>
> ```
> c. A memory keyed by identity, with names extracted in code and matched across contacts. It's the most exact, but it needs A's extraction and fuzzy name matching. A follow-up, tied to A, if b falls short.
> ```

### 15.7 The agent: the follow-up; item 4, the wording and the list (verbatim, 15:03-15:04)

The restatement reaches back over the whole run, grouped by contact and capped. Here's the follow-up entry for option c, written after "Pace the calls in rounds" in `docs/follow-ups.md`, uncommitted:

The entry is **"A listener memory keyed by identity — revisit how the show remembers a returning listener"**. It holds:
- the decision taken (b), and your idea behind it, verbatim;
- option c, verbatim, with your instruction to revisit it;
- what c would need: extraction (A's ways), fuzzy name matching (Whisper spellings, SED §6.3), and a per-listener store;
- why identity by browser fails at a demo;
- that both options last one run;
- a trigger: the driver or your ear shows b falls short, or option A comes back.

All three quotes match the transcript.

##### The agenda, item 4 (last in this group): the restatement's wording and the list's content

**What's left** is words, not mechanics:
- **The restatement's wording** in each contact instruction. A first draft, to show the shape:

  ```
  What voices said in earlier contacts, oldest first:
    Contact 1: "Hello, who are you? My name is Alfredo." / "I'm in Austin."
    Contact 2: "Hi, this is Maria, from Dallas."
  What this voice has said since it answered: "It's Alfredo again."
  If this voice is someone you spoke with before, greet them as a returning friend and use what they told you.
  ```
- **The agenda list itself:** the name item that opens every contact, then roughly 6–10 two-branch sentences: whereabouts, locating the lab from clues, help to escape, supplies, and perhaps news from the listener's town, or relaying a message to the authorities.

**How words were settled before:** by what the model did with them. The events' wording was decided by an A/B on the box (two 30-round drives), and the static round's wording changed after the operator signed off in live drives. Words are best judged against evidence.

**Options:**
- **a. Settle both at build time, with evidence.** I draft the wording (in the director) and the list (in the story file), the driver test on the box shows what the model does with them, and you review both in VS Code before your test by ear. They go on the TODO's "To confirm when building" list.
- **b. Settle both now, in this discussion.** I draft them here, and you rule on the words before any code, without evidence of how the model takes them.

**My lean: a.** The mechanics are what need ruling before code. The words are cheap to change after one driver run shows how they land.

When do we settle the wording and the list?

### 15.8 The owner's answer (verbatim, 15:06)

> a, settle both at build time with evidence.

### 15.9 The agenda — ruled

- **An item:** a plain two-branch sentence — ask for something; if the
  voice already gave it, use it — with the clues and the supplies
  written into the sentences. The file lives in the story folder like
  `events.yaml`, read by a copy of its loader. The model picks who asks
  among the rest of the cast (§13.12); a preferred asker per item is a
  possible later addition, if the ear test shows the wrong characters
  asking.
- **Order and repeats:** the name item opens every contact (the file's
  first entry, so documented in its header comment); the rest are drawn
  at random — no repeats within a contact, and across the run none until
  the list is used up (the events' rule, `_fresh`).
- **The restatement's reach:** the whole run, grouped by contact,
  oldest first, capped at the last K contacts (a setting, e.g. 5), plus
  a line asking the model to greet a voice it spoke with before as a
  returning friend and use what they told it. No identity in code; the
  model does the matching. The alternative keyed by identity: the
  follow-up "A listener memory keyed by identity — revisit how the show
  remembers a returning listener".
- **The wording and the list:** settled at build time with evidence —
  the agent drafts both, the driver test on the box shows what the
  model does with them, and the owner reviews both before the test by
  ear (the TODO's "To confirm when building").

## 16. The shape's details: the emotional overtone (2026-09-26)

*The overtone's rulings, with those of §17, are listed in §17.11.*

### 16.1 The agent: the agenda recorded; item 1, where the groups live (verbatim, 15:07)

§15 is in the draft: nine messages verbatim (this time the transcript kept everything), and §15.9, "The agenda — ruled". All 55 quoted messages match the transcript. The TODO's "To confirm when building" list gains the restatement's wording and the agenda's list, and the entry now says the agenda is done. Everything is uncommitted.

Last group: the emotional overtone (§10 item 6; its open points are in §9.14 and §12). One at a time, starting with how the data is laid out.

##### The overtone, item 1: where the groups live

**Ruled (§9.15):**
- moods and tone words each split into positive, neutral and negative;
- each round's overtone chosen first, with both drawn from it;
- the groups are data, not a hard-coded three.

**Where the two lists live today:**
- **Moods:** a constant in the engine's code, `MOODS = ("calm", "happy", "sad", …)` (`grammar.py:10`), the same for every story. `show.emotion_tags` turns them on or off.
- **Tone words:** the story's `tones.yaml`, 500 words in 24 themed groups. The groups are only comments; the loader flattens them (`story.py:81`).

**What the layout has to allow:**
- the coupling you asked for, where one overtone gives both its moods and its tone words;
- new mood words ("hopeful", "excited", "relieved");
- negative splitting later, if the voice needs it (§11);
- another story bringing its own palette.

**Options:**
- **a. One story file for the overtones,** each overtone holding its moods and its tone words together:

  ```yaml
  overtones:
    positive:
      moods: [happy, hopeful, excited, relieved]
      tones: [...]
    neutral:
      moods: [calm, doubtful, urgent]
      tones: [...]
    negative:
      moods: [sad, afraid, terrified, angry, exhausted]
      tones: [...]
  ```

  The coupling is visible in one place, and a fourth overtone is one more key. It replaces `tones.yaml`; the 24 themed groups stay as comments inside each overtone for whoever edits the words. The engine's `MOODS` constant becomes the union of the story's moods. (The words shown are a sketch; the sorting is the next item.)
- **b. Two story files with the same keys:** `moods.yaml` grouped, and `tones.yaml` restructured into the same three groups. The coupling lives in matching keys, so it's easy to let the two drift apart.
- **c. Moods in settings** (`settings.yaml`), tone words in the story. It splits the pair across two places, and moods are a story's palette, not a server setting.

**My lean: a.** Your coupling principle becomes the file's structure: an overtone *is* its moods plus its tone words. Adding a group is a data change, which is exactly "not a hard-coded three".

Where should the overtone groups live?

### 16.2 The owner's answer (verbatim, 15:09)

> a, one story file for the overtones

### 16.3 Item 2, which moods go in which group (verbatim, 15:09)

The overtones live in one story file.

##### The overtone, item 2: which moods go in which group

**Why the moods now, and not with the tone words:**
- **The tone words** are 500, and sorting them is authoring work, like the agenda list. I'd bring them as the next item, with the same "at build time, with evidence" proposal.
- **The moods** are a dozen words with real consequences:
  - they're the only emotion the grammar enforces on each line;
  - they show in the captions;
  - per §11, they're the signal that will one day travel to the TTS and pick a voice clip, so they're the vocabulary your mood → clip mapping will be written in.

**Today's nine** (`grammar.py:10`): calm, happy, sad, afraid, terrified, doubtful, angry, urgent, exhausted. Only one of them is positive.

**What each group needs:** enough words that the grammar never forces a single mood (§9.14, point 4). And the words have to fit where each overtone is used: Contact is positive or neutral (§9.14, point 2), a Breakdown turns darker, and a Broadcast can be anything.

**My proposal: 14 moods, 5 of them new (marked \*):**

| Overtone | Moods |
|---|---|
| positive | happy, hopeful\*, excited\*, relieved\* |
| neutral | calm, doubtful, urgent, curious\*, determined\* |
| negative | sad, afraid, terrified, angry, exhausted |

**Why these:**
- **"Hopeful", "excited", "relieved"** are your 2024 register for contact ("happiness and hope"). Excited is the first reaction to a voice, relieved is someone out there at last, hopeful is the plan.
- **"Urgent" in neutral:** asking a listener for insulin is urgent without being grim, so it fits a neutral contact round.
- **"Curious"** fits Moira, "grimly fascinated by the science of the outbreak" (the cast sheet).
- **"Determined"** covers the "Resolve and defiance" register of the tone words, neither joy nor despair.
- **Nothing to change in the parser:** it accepts any mood word (`parser.py:23`), and the grammar takes whatever list it's handed.
- **With `show.emotion_tags` off,** the lines carry no mood, and the overtone steers only the tone word.

**The alternatives:**
- keep today's nine and add only the three positives (12 moods, with a thinner neutral group of calm, doubtful, urgent);
- or adjust the table word by word.

Do these 14 moods, grouped this way, work for you?

### 16.4 The owner's answer (verbatim, 15:10)

> yes, the 14 moods grouped as proposed

### 16.5 Item 3, sorting the 500 tone words (verbatim, 15:10)

The 14 moods are ruled.

##### The overtone, item 3: sorting the 500 tone words

**Where they stand:** 500 words in 24 themed groups (`tones.yaml`). The groups were written by theme, not by direction, so most of them sort cleanly as whole groups, and a few are mixed.

**My proposal: sort by whole group now, and fix single words at build time.**

| Overtone | Groups (words) | Total |
|---|---|---|
| **positive** | Hope and warmth (26), Resolve and defiance (26), Levity and play (20), Pride and bravado (14), Intimacy (12), Innocence (6) | 104 |
| **neutral** | Manner of speech (28), The laboratory (26), Wonder and the uncanny (26)†, Gallows humor and wit (26)†, Stillness (18), On the air, 1930s (16), Faith and ritual (10), The everyday (10) | 160 |
| **negative** | Dread and horror (34), Friction and hostility (32), Nerves and tension (28), Grief and despair (28), Suspicion and secrecy (26), Fever and chaos (26), Weariness and numbness (20), Longing and regret (18), Command and coldness (16), Pleading (8) | 236 |

† These groups are mixed, so they're the first place to look for single-word exceptions:
- "Wonder and the uncanny" runs from dreamlike to otherworldly, and "uncanny" leans negative;
- "Gallows humor and wit" is a grim situation in a light register, so it goes in neutral as a whole;
- "Pleading" is in negative, but "insistent" and "emphatic" could be neutral.

**Why this balance works:** the negative pool is the largest (236), right for a horror show, and positive (104) is ample for contacts. How often each overtone is *chosen* is a separate question (the next item). The pool sizes only give variety within an overtone.

**Options:**
- **a. Rule the group table now; single words at build time.** I draft the exceptions, the file is reviewed in VS Code with the rest of 3.4c's authoring (the agenda list, the restatement), and the driver test runs on the sorted file.
- **b. Everything at build time,** including the group table.
- **c. Everything now,** word by word. That's 500 words in chat, which is authoring, not a discussion.

**My lean: a.** The table is the real decision, it takes one look, and it catches a whole group in the wrong place. The single words are polish.

Does the group table stand, with the single words settled at build time?

### 16.6 The owner's answer, and the themes (verbatim, 15:15)

> a, the group table stands; single words at build.
>
> What will happen in this new organization you are proposing to these groups (like `Hope and warmth`).
> I like this grouping of therms a lot and I think we should preserve this in some way. Right now they are just comments in the yaml file... Should we create another file with the only purpose of providing this grouping in a way that is usable in code? I am not 100% percent sure we need it, but I feel the grouping itself in those categories could become useful.

### 16.7 The agent: the themes as data (verbatim, 15:16)

The group table stands, and the single words are settled at build.

**What happens to the themed groups in my proposal:** they'd survive only as comments inside each overtone, as today. The words keep their neighbors, but code can't see the themes.

**Should they become data? Yes, I think so,** and you don't need a second file for it. We're reshaping `tones.yaml` into the overtones file anyway, so keeping the themes costs almost nothing now. Restructuring the file again later would cost more.

**Uses I can already see for the themes:**
- **The orientation round** could draw its tone word from "On the air, 1930s" ("broadcast-polished", "newsreel", "static-laced"), which is exactly the station-identification register.
- **Comic relief** (the follow-up) could draw from "Gallows humor and wit" and "Levity and play".
- **The Breakdown** could lean on "Fever and chaos" or "Nerves and tension".
- **Theme runs:** hold one theme for a few rounds. It's the same wish as the follow-up "Events that stay on topic for a few rounds", whose idea 2 asks for exactly this in `events.yaml` (groups as data, not comments).
- **The debug line** could show the theme next to the tone word.

None of these is needed for 3.4c. They're why keeping the themes is worth the near-zero cost.

**Options:**
- **a. Themes as keys inside each overtone,** in the one overtones file:

  ```yaml
  overtones:
    positive:
      moods: [happy, hopeful, excited, relieved]
      tones:
        Hope and warmth: [bright, cheerful, radiant, …]
        Levity and play: [whimsical, kooky, …]
    neutral:
      moods: [calm, doubtful, urgent, curious, determined]
      tones:
        The laboratory: [clinical, sterile, …]
        Wonder and the uncanny: [dreamlike, …]
    negative:
      moods: […]
      tones:
        Wonder and the uncanny: [uncanny, otherworldly, …]   # a mixed theme, split
        Dread and horror: [macabre, ominous, …]
  ```

  One file, and each word appears once. A mixed theme simply appears under two overtones. The loader reads each word with its overtone and its theme; today's draw ignores the theme.
- **b. A separate catalog:** `tones.yaml` keeps the themes as real keys (theme → words), and the overtones file lists which themes belong to each overtone, plus a list of single-word exceptions. Tidier on paper, but the palette is split across two files and needs an exceptions mechanism.
- **c. Themes stay comments,** as proposed before. Nothing to build, and nothing for code to use later.

**My lean: a.** One file an author can read top to bottom (an overtone, its moods, its themed words), no duplication, and the themes ready for whichever use comes first.

Should the themes become keys inside each overtone?

### 16.8 The owner's answer, and the uses to keep (verbatim, 15:18)

> a, themes as keys inside each overtone.
>
> Please make sure to store your "Uses I can already see for the themes" in a prominent but adequate position in our docs.

### 16.9 The agent: the uses stored; item 4, the overtones each kind of round may use (verbatim, 15:18-15:19)

Themes become keys inside each overtone. I'll put the uses in a follow-up entry of their own, since `docs/follow-ups.md` is scanned at every pickup and holds deferrals with their triggers. I'll also add pointers from the two entries they touch. First, your exact words.

The uses are stored in a follow-up entry of their own, **"The tone themes as data — five uses waiting for them"**, uncommitted. It holds:
- what 3.4c leaves in place (themes as keys, read with each word);
- your two sentences, verbatim;
- the five uses, numbered;
- a trigger per use;
- a fix shape (a kind-to-theme mapping in the story's file).

The two entries it touches now point to it: **"Comic relief"** (use 2) and **"Events that stay on topic for a few rounds"** (use 4, one shape for both files). When I record the overtone group in the draft, its ruled list will point there too.

##### The overtone, item 4: which overtones each kind of round may use

**Ruled:** each round's overtone is chosen first, and its moods and tone word follow (§9.15). What's open is how the director chooses. Round kinds differ: a contact shouldn't turn grim, and a Breakdown shouldn't sound cheerful. Free rounds in Broadcast are the next item.

**A rule that keeps your coupling safe:** when a kind allows two overtones, they're **neighbors**, never positive together with negative. The director draws one of them per round, seeded, and both the moods and the tone word come from that one. A contact round drawn positive, where the listener brings bad news, still has "hopeful" and "relieved" to work with ("we'll find another way").

**My proposal:**

| Round kind | Allowed overtones | Why |
|---|---|---|
| sign-on / orientation | neutral | station identification: composed, informative |
| Repair (the call) | positive | "Got it! The receiver's live!" |
| contact exchange | positive, neutral | your 2024 register; neutral for the level-headed exchanges |
| re-call | neutral | "Alfredo? Are you still there?": worry, not despair |
| Breakdown | neutral, negative | the conversation cut off |
| Switch-off | neutral, negative | a choice, made with disappointment |
| free (Broadcast) | the next item | |

**Where the table lives:** in the story's overtones file, next to the overtones. The overtone names are story data (a story could have four), so the mapping has to live where they do. A comedy story would map differently.

**Options:**
- **a. The table above, in the story's file,** one overtone drawn per round from the kind's allowed ones.
- **b. The same table, but a kind with two overtones draws each at a set weight** (e.g. contact 2:1 positive to neutral), with the weights in the file too.
- **c. One fixed overtone per kind:** contact always positive, Breakdown always negative. Simplest, and the most monotonous.

**My lean: a.** A 50/50 draw between neighbors gives variety without contradiction. Weights (b) can come later, in the same file, if the ear asks for them.

Does the table, with its home in the story's file, stand?

### 16.10 The owner's answer, and where we are (verbatim, 15:21)

> a, the table stands in the story's file.
>
> By the way, where are we in the planing? how many more items are left to discuss?

## 17. Where we were, and the four design choices (2026-09-26)

### 17.1 The agent: where we are (verbatim, 15:21)

Ruled: the table stands, in the story's file.

#### Where we are

It's **15:25 CDT, Saturday**, and the timebox ends Monday.

**Decided since 11:14, about 25 decisions**, all recorded in the draft (§9–§15) apart from the overtone group, which is still open:

| Group | Items | State |
|---|---|---|
| The scope | 5 features + the Switch-off + the silence rule | done (§9–§10) |
| Contact | 5 | done (§13) |
| The receiver story | 5 + the orientation | done (§14) |
| The agenda | 4 | done (§15) |
| The overtone | 4 of about 6 | under way |

**What's left, about 9 items:**
- **The overtone, 2 more:**
  - free rounds in Broadcast: how the overtone is drawn (weights) and how long it's held, with the tone word's hold inside it;
  - events carry emotion: what overtone an event round may use.
- **The orientation's details, 1:** when it may fire, who speaks, the facts it's given, the default frequency. These were parked in §14.13.
- **The plumbing, about 6:**
  - the "radio listens now" flag across the round route, the page and the driver (crack 6);
  - the driver holding a conversation for the tests (crack 7);
  - what the page shows for the new beats. This one is new, noticed now: which beats appear as stage directions, and a "You:" caption under every exchange, not only under the call;
  - 3.4c's exit criterion (crack 8);
  - the listener after the contact (crack 9, my lean: defer);
  - moving the free rounds' line budget into settings (raised in Contact item 5).
- **The bookkeeping** (crack 10) is procedure, not a decision: the TODO, a dated note in SED, the follow-up resolved.

**Time:** at today's pace, roughly 45–75 minutes of discussion. Then I owe you an **estimate for the build**, and it will be the biggest step of the slice. It touches the director, the grammar, two new story files, about ten settings, the record, the round route, the page, the driver, the tests and the docs, and then the driver test on the box and your test by ear.

**One way to go faster, if you want it:** some of the 9 are real design choices (the Broadcast draw, events, the exit criterion, the page's beats). Others would settle themselves at build time with my picks, recorded for your review in VS Code as we did with the agenda list: the orientation's details, the listen flag's mechanics, the free rounds' budget, crack 9.

Do we go through all 9 one at a time, or only the design choices, with the rest settled at build time with my picks?

### 17.2 The owner: the design choices first (verbatim, 15:24)

> Let's do first the design choices. When we finish ask me again how to proceed/

### 17.3 Design choice 1: how free rounds choose their overtone (verbatim, 15:24)

Design choices first, then I'll ask you how to proceed. There are four:
1. the Broadcast draw;
2. events;
3. 3.4c's exit criterion;
4. what the page shows for the new beats.

##### Design choice 1 (the overtone, item 5): how free rounds choose their overtone

**Today, the tone word alone:** it's held for `tone_hold` ± `tone_jitter` rounds (3 ± 1, in settings). Then a new word is drawn, never the one just held, and no repeats until the list is used up (`_tone`, `director.py:196-214`).

**With overtones there are two layers:** the overtone, held for a stretch of free rounds, and the tone word, held inside it. When the overtone changes, the tone word changes at once, to a word from the new overtone. The beats (contact, Repair, Breakdown…) keep their own table (item 4), so this is about free rounds only.

**What the listener would hear:** a grim stretch in the besieged lab, then level talk, then maybe a flicker of hope. The risk is a jump: four terrified rounds, then suddenly cheerful ones with no reason in the story. That's the contradiction you ruled out within a round, spread across rounds.

**Options:**
- **a. A weighted draw when a hold ends.** The weights live in the story's file, e.g. negative 3 : neutral 2 : positive 1, a horror show leaning grim. The hold lives in settings, e.g. `overtone_hold: 4`, `overtone_jitter: 1`. Simple, but positive can follow negative directly.
- **b. The same, but it moves only to a neighbor.** When a hold ends, the draw is among the current overtone and its neighbors, using the same weights. Neighbors follow the file's order (positive, neutral, negative):
  - from negative: stay, or ease to neutral (3 : 2);
  - from neutral: any of the three (3 : 2 : 1);
  - from positive: stay, or settle to neutral (1 : 2).

  So the mood drifts rather than jumps, and hope and terror never sit side by side. After a contact, Broadcast carries on from the Breakdown's overtone, so the drift continues from where the story left off.
- **c. No hold: a fresh draw every round.** Choppy, and it undoes the tone hold's reason for existing.

**My lean: b.** The drift feels like a story (dread easing, then hope, then dread again) instead of dice. It costs a few lines more than a: the neighbor rule, and one set of weights in the file. The hold numbers go in settings, the weights in the story's file (the overtone names are story data), and nothing is hard-coded.

How should free rounds choose their overtone?

### 17.4 The owner's answer (verbatim, 15:25)

> b, move only to a neighbor

### 17.5 Design choice 2: events carry emotion too (verbatim, 15:26)

Free rounds drift only to a neighbor.

##### Design choice 2 (the overtone, item 6): events carry emotion too

**The problem (§9.14, point 1).** An event lands on a free round (every `event_every` ± `event_jitter` free rounds, 2 ± 1), and its round has an overtone. If the two disagree, the model gets contradictory signals again, which is what you ruled out.

**The events aren't all grim.** `events.yaml` has 289 events in 15 themed groups (comments, like the tones):
- **mostly dark:** "The dead outside" (26), "The building" (24), "Inside the walls" (8);
- **hopeful:** "Luck and small mercies" (18), e.g. "A working satellite phone turns up in a storage locker, with one bar of battery.";
- **stray hopeful ones elsewhere:** "The radio catches a ball game, the crowd cheering as if nothing has happened.";
- **gallows humor:** "The last packet of coffee is found, and it is decaf."

So "event rounds are never positive" would put a found satellite phone into a grim round: the same contradiction, the other way round.

**Options:**
- **a. Events follow the mood.** Each event gets an overtone, and a free round draws its event only from events that fit its overtone. The held overtone is untouched, but the pools split: a positive stretch has about 18 events to choose from, so repeats come sooner.
- **b. The event sets the mood.** Each event gets an overtone, and the event is drawn as today, from the whole pool. The round takes the event's overtone, and the drift continues from there.
  - Good news lifts, bad news darkens: the event is the cause, the mood the effect.
  - An event may jump (hopeful to terrified at once), because the story gives the reason. The neighbor rule still governs the drift when a hold ends.
  - The pool stays whole, 289 events.
- **c. Event rounds are always neutral.** No sorting at all. It's a reporter's register ("tells the listeners on air what is happening"), which is quite Welles, where the reporter tries to stay composed. But "terrified" is never available when something is scratching at the door.

**What a and b both need:** events sorted by overtone, by group first and single events as exceptions, like the tones. `events.yaml`'s groups become data, which is also idea 2 of the follow-up "Events that stay on topic for a few rounds". The sorting would be settled at build, drafted by me and reviewed by you, like the tone words.

**My lean: b.** It's how a story works: something happens, and the mood turns. The pool stays whole, and every event, grim, hopeful or absurd, gets a matching register. It costs one more sorting job at build (15 groups, then exceptions).

How should events and the overtone relate?

### 17.6 The owner: b would hand the mood to the event pool (verbatim, 15:31)

> Humm, you left one part out: If we pick b, the frequency of overtones in the app will depend on the probability distribution of overtones in the  already existing event list... Because the events are not sorted by overtone yet, you cannot guarantee anything about how the app will operate.
>
> So, in my opinion (a) is  correct option, (b) is incorrect, (c) is what we have, so no effect.

### 17.7 The agent: right; design choice 3, the exit criterion (verbatim, 15:32)

**You're right, and b was wrong.** Here's the mechanism I missed:
- Events come every 2 ± 1 free rounds; the overtone's hold is 4 ± 1.
- Under b, an event would reset the mood before most holds even end.
- So the show's overtones would follow the event pool's make-up, whatever that turns out to be once sorted, and the weights in the story's file would barely matter.

With a, the weights and the drift stay in charge, and events only fill in. **Ruled: a, events follow the mood.**

What a brings, for the record:
- **The pools split by overtone.** The positive pool is small: "Luck and small mercies" (18) plus a few strays. Positive stretches are also the rarest (weight 1, and reachable only through neutral), so the small pool is drawn from rarely. The no-repeats rule applies per pool.
- **An overtone with no events of its own** (possible in another story) skips the event that round. It's decided at build, with the rest of the mechanics.
- **The events get sorted at build,** by group first and then single exceptions, drafted by me and reviewed by you, like the tone words. `events.yaml`'s groups become data.

##### Design choice 3: 3.4c's exit criterion

**How earlier steps ended:**
- **3.4:** "The owner listens; the verdict is recorded here."
- **3.4b:** "the owner, talking to the show live, sees the words and their confidence and approves; then the branch is committed and pushed."
- **Your rule for owner-tested steps:** "Once approved we commit and push the branch."

**3.4c needs more than an ear test,** because we promised evidence along the way:
- the driver test decides whether B is enough for feature 5, or A comes back (§9.10);
- the agenda's list and the restatement's wording are judged against evidence before you review them (§15.9).

**My proposal: "Done when" is four checks, in order.**
1. **The tests are green:** the Python suite and the three Node tests.
2. **The driver test on the box,** with scripted conversations, including:
   - "Alfredo" twice, with a stranger in between;
   - a silence in the middle of a contact;
   - a call left unanswered twice.

   Then a report with numbers, like the events' A/B:
   - how often the cast uses a name it was given;
   - whether the returning Alfredo is recognized;
   - whether the Breakdown answers the last words;
   - that two silences switch the receiver off;
   - that no event lands in a contact;
   - that the sign-on opens and the orientation repeats.

   You read the report and decide whether B is enough.
3. **A fake-microphone check in the page,** like 3.3 and 3.4b: the button lights after every exchange, a "You:" caption appears under each one, and the new beats show correctly.
4. **You, by ear, with the real microphone:** at least one full contact (Repair, two or more answers, Breakdown) where the cast engages (your name, the agenda, answering what you said), and one call left unanswered until the Switch-off. Your verdict is recorded; then commit and push.

**Options:**
- **a. The four checks above.** Your judgment decides at 2 and 4.
- **b. Only your ear (4),** as in 3.4. Quicker, but B-versus-A would be judged from one or two contacts.
- **c. The four checks, with a numeric gate at 2:** for example, "a given name used in at least half the exchanges after it's given", or A comes back automatically.

**My lean: a.** Numbers inform your call rather than replace it, the same way the events' A/B worked ("B wins, flip the default").

What's 3.4c's exit criterion?

### 17.8 The owner's answer (verbatim, 15:33)

> a, the four checks above

### 17.9 Design choice 4: what the page shows for the new beats (verbatim, 15:34)

Ruled: the four checks.

##### Design choice 4 (the last): what the page shows for the new beats

**What the page shows today** (`static/show/show.js`, `show.css`):
- the ON AIR sign and the cast strip, with the speaker lit;
- the state line (thinking, on air, listening…);
- behind the captions toggle:
  - each line (speaker, mood, text) as its voice starts;
  - events as stage directions above their round's lines;
  - your "You:" caption with per-word confidence, under the call's block (3.4b);
- the talk button, enabled only during a listening window;
- with debug on, a line per round (kind, speakers, event, tone, timings).

**What 3.4c changes regardless** (plumbing, settled at build): the talk button follows the new "the radio listens now" flag. So it lights after every exchange and re-call, not only after the call, and a "You:" caption goes under **every** listening round's block. The debug line gains the new facts: the kind, the overtone, the agenda item, and the answers so far ("2 of 3").

**The design question is what the page adds for the receiver story.** The characters say it all on air (the report rule), so the audio carries it. The screen could show it too, and at a demo people look at the screen.

**Options:**
- **a. Nothing more.** The captions show the lines, and the lines tell the story.
- **b. A receiver light, plus stage directions for the beats:**
  - **the light:** "RECEIVER" next to ON AIR. It lights from the Repair until the Breakdown or Switch-off, and stays dark through Broadcast. The fiction's state becomes the audience's cue: receiver lit means you may be called on. It's a CSS class set from each round's kind.
  - **the directions** (with the captions, like events): short fixed texts per beat, kept in the story's file so another story words them its own way. For example, "The receiver crackles back to life." (Repair), "Smoke pours from the receiver; it goes dead." (Breakdown), "The receiver is switched off." (Switch-off).
- **c. The stage directions only,** no light.

**My lean: b.** The light is the one visual cue that tells a room full of people when they can talk, and it costs a class toggle. The directions make the captions tell the same story the ear hears, just as events already do. Both are small; the light is the one I'd keep if you want only one.

What should the page add for the receiver story?

### 17.10 The owner's answer (verbatim, 15:35)

> b, the receiver light plus stage directions

### 17.11 The emotional overtone — ruled

- **Where:** one story file for the overtones, replacing `tones.yaml`;
  each overtone holds its moods and its tone words. The engine's
  `MOODS` becomes the union of the story's moods; a fourth overtone is
  one more key.
- **The moods — 14, five new (\*):** positive happy, hopeful\*,
  excited\*, relieved\*; neutral calm, doubtful, urgent, curious\*,
  determined\*; negative sad, afraid, terrified, angry, exhausted.
- **The tone words:** sorted by whole group (the table of §16.5 —
  positive 104, neutral 160, negative 236); single words at build time,
  drafted by the agent and reviewed by the owner.
- **The themes:** keys inside each overtone (a mixed theme appears under
  two); the loader reads each word with its overtone and its theme;
  3.4c's draw uses only the overtone. The uses waiting for them: the
  follow-up "The tone themes as data — five uses waiting for them".
- **Per kind of round,** in the story's file, one overtone drawn per
  round from the kind's allowed ones, always neighbors: sign-on and
  orientation neutral; Repair positive; contact exchange positive or
  neutral; re-call neutral; Breakdown neutral or negative; Switch-off
  neutral or negative.
- **Free rounds (Broadcast):** the overtone held for a stretch (settings,
  e.g. `overtone_hold: 4`, `overtone_jitter: 1`); when a hold ends, it
  moves only to a neighbor (the file's order: positive, neutral,
  negative), weighted by the story's weights (e.g. negative 3 : neutral
  2 : positive 1); after a contact, the drift continues from the
  Breakdown's overtone. The tone word is held inside the overtone and
  changes at once when the overtone does.
- **Events follow the mood:** each event gets an overtone (the groups of
  `events.yaml` become data; sorted at build like the tone words,
  reviewed by the owner), and a free round draws its event only from
  its overtone's pool, no repeats per pool; an overtone without events
  skips the event that round (the mechanics at build). The owner's
  catch against letting the event set the mood (§17.6): events come
  every 2 ± 1 free rounds and holds last 4 ± 1, so the show's
  overtones would follow the event pool's make-up, not the weights.

### 17.12 The exit criterion and the page — ruled

- **3.4c is done when four checks pass, in order:** (1) the suite and
  the three Node tests are green; (2) the driver test on the box, with
  scripted conversations ("Alfredo" twice with a stranger between, a
  silence inside a contact, a call left unanswered twice) and a report
  with numbers — how often a given name is used, the returning
  listener recognized, the Breakdown answering the last words, two
  silences switching the receiver off, no event inside a contact, the
  sign-on and the repeating orientation — from which the owner decides
  whether B is enough; (3) a fake-microphone check in the page; (4) the
  owner by ear with the real microphone — at least one full contact
  (Repair, two or more answers, Breakdown) where the cast engages, and
  one call left unanswered until the Switch-off; the verdict recorded,
  then commit and push.
- **The page:** the talk button follows a "the radio listens now" flag
  (after every exchange and re-call); a "You:" caption under every
  listening round's block; the debug line gains the kind, the overtone,
  the agenda item and the answers so far; **a RECEIVER light** next to
  ON AIR, lit from the Repair until the Breakdown or the Switch-off; and
  **stage directions for the beats**, with the captions like events,
  from short fixed texts per beat in the story's file.

### 17.13 What remains — mechanics, the owner's call on how

The design choices are done (§17.2: "Let's do first the design choices.
When we finish ask me again how to proceed"). Left, as listed in §17.1:
the orientation's details (when it may fire, who speaks, the facts it
is given, the default frequency); the listen flag's mechanics across
the round route, the page and the driver (crack 6); the driver holding
a conversation (crack 7); the free rounds' line budget into settings;
the listener after the contact (crack 9, the agent's lean: defer); the
bookkeeping (crack 10).

## 18. The mechanics the owner chose to discuss (2026-09-26)

### 18.1 The agent: the design choices recorded; how to proceed (verbatim, 15:37)

All four design choices are decided and recorded, uncommitted, for your review in VS Code.

- **The draft's §16–§17:** 21 messages verbatim, and all 76 quoted messages match the transcript. It adds:
  - **§17.11, "The emotional overtone — ruled"**, the whole group in one list;
  - **§17.12, "The exit criterion and the page — ruled"**;
  - **§17.13**, listing what's left.
- **The TODO's 3.4c entry:**
  - "Done when" is now the four checks;
  - "To confirm when building" gains the tone words' single words and the events' sort;
  - the details are marked done through §17.
- Also uncommitted: this morning's `follow-ups.md` entries (comic relief, findings, pacing in rounds, the listener memory, the tone themes).

#### How to proceed

**What remains is mechanics, six items** (§17.13):
1. the orientation's details: when it may fire, who speaks, the facts it's given, the default frequency;
2. the "listens now" flag across the round route, the page and the driver;
3. the driver holding a conversation;
4. the free rounds' line budget into settings;
5. the listener after the contact (crack 9, my lean: defer);
6. the bookkeeping.

**The build, estimated:**
- about **4–6 hours of my work** for the code, the story data (the agenda list, the overtone sort, the events' sort, the beat texts), the tests and the docs;
- then the driver test on the box with its report (~45 min), the fake-microphone check (~20 min), and your test by ear.

My estimates ran about 2.5 times too long yesterday, so the real figure may be closer to 2–3 hours. Either way, it likely runs into Sunday, which still leaves Monday for 3.5.

**Options for the six items:**
- **a. Settle them at build time with my picks,** each recorded in the draft for your review in VS Code, the way the agenda's wording is handled.
- **b. Discuss them one at a time now,** about 20–30 minutes.
- **c. Discuss two now,** the orientation's details and crack 9, since they shape what the listener hears, and use my picks for the other four, which are plumbing.

Before any code, I'd also bring the **build plan**: its sub-steps and commits (for example, the story data, then the director and grammar, then the route, page and driver, then the checks) as a shape for your Go.

How do you want to handle the six remaining items?

### 18.2 The owner's answer (verbatim, 15:38)

> c, discuss the orientation and crack 9 now

### 18.3 Mechanics 1: the orientation's details (verbatim, 15:39)

Two items, one at a time, starting with the orientation. It has four parts, each with a pick in bold. You can take them all or change any one.

##### Mechanics 1: the orientation's details

**What's ruled (§14.13):** a round that tells the listeners who the cast are, where they are, and the receiver's state, worded by the character in their own words. The sign-on at round 1 is its first occurrence. It repeats every N ± jitter rounds, with both numbers in settings. The shape is the Switch-off's: up to two lines, the first speaker pinned, one more voice may add. Its overtone is neutral (§17.11).

**1. When it may fire.** It fires only in Broadcast, never inside a contact.
- **Pick:** it counts free rounds since the last orientation. When it's due, the next free round becomes the orientation. An event due that round waits one round.
- **If a call is due at the same time,** the call wins and the orientation waits for the next Broadcast round.

**2. Who speaks.** Your aim was variety ("to introduce some variability in the orientation round message").
- **Pick:** the sign-on is the operator, since the host opens the broadcast. The repeats rotate, with the first speaker being whoever has been silent longest (the free rounds' rule, `_silent_longest`, `director.py:140-149`).
- Each character tells it differently: Ralph counts doors, Moira talks about the virus.
- The alternative: always the operator, so the audience learns to recognize "the radio's voice", at the cost of variety.

**3. The facts it's given.** A short story-level text, so another story brings its own.
- **Pick:** an `orientation:` field in the cast sheet's front matter, next to `title`, `cast` and `operator` (`stories/lab-outbreak/cast_sheet.md:1-5`). The beats' stage-direction texts (design choice 4) would live there too.
- The instruction then reads roughly: "Ralph speaks to listeners who just tuned in, telling them in his own words: <the facts>".
- The facts, drafted at build for your review: four scientists; a secret lab, besieged; the outbreak; the receiver is dead, so they can only transmit; when it's fixed, they'll call out, and listeners can answer then. That's always true in Broadcast, because the receiver is always down there.

**4. How often.**
- **Pick:** every **20 ± 5** free rounds, in settings (`orientation_every: 20`, `orientation_jitter: 5`), with 0 turning the repeats off, as `event_every` does.
- 20 rounds is about 2 minutes of audio (about 6 s per round, from yesterday's 3.2 run).
- A broadcast stretch between calls is 60–180 s, roughly 10–30 rounds, so that's about one orientation per stretch. Latecomers hear the rules within a couple of minutes of sitting down.

Do the four picks stand, or which would you change?

### 18.4 The owner's answer (verbatim, 15:39)

> the four picks stand

### 18.5 Mechanics 2: the listener after the contact (verbatim, 15:40)

The four picks stand.

##### Mechanics 2 (the last before the build plan): the listener after the contact (crack 9)

**The gap.** When a contact ends (Breakdown or Switch-off) and the broadcast resumes, nothing asks the cast to mention the listener again. The listener's words stay in the script until the trim drops them, so the model *can* recall them, and once it did on its own: after your 3.4b check, it folded you into an event, "Someone's safe, Alfredo's family." But nothing makes it happen.

**Why it matters:** at the demo, the volunteer finishes talking, the receiver dies, and then… the lab carries on as if they'd never called. Hearing the cast discuss what you told them ("Alfredo says the highway north is blocked, we need another way out") is proof that your words changed the story. That's the strongest engagement payoff we have.

**My earlier lean was to defer it.** Since then, two rulings made it cheap: the restatement reads every listener's words from the record, and the orientation exists.

**Options:**
- **a. Defer** it, as a follow-up.
- **b. The orientation mentions the last caller:** "Earlier, a man called Alfredo reached us from Austin…". It's tiny, since the orientation's instruction gets the last contact's words. But it comes up to about 2 minutes later, and its job is the rules for newcomers.
- **c. An aftermath round:** the first free round after a contact talks about what the listener told them. It takes that round's event slot, with an instruction like "The voice on the frequency told you: <the contact's words>. Talk among yourselves about what it means for you."
  - It's the events' own mechanism: the events pool already has "Voices from outside", such as "A listener in Duluth says the lake froze early…".
  - Only after a contact where the listener actually spoke; a call nobody answered leaves nothing to discuss.
  - It takes the overtone already in play, the drift continuing from the Breakdown's, since the listener's words have no pool to be drawn from.
  - It's one condition in the free round's plan, plus the wording.
- **d. Both b and c.**

**My lean: c.** It's immediate: the payoff lands within seconds of the receiver dying, while the volunteer is still standing at the laptop. b would be a nice later touch (the orientation's facts are drafted at build anyway), but it isn't needed for engagement.

What should happen with the listener after the contact?

### 18.6 The owner: c, and a new periodic round (verbatim, 15:44)

> I want c, but also a new proposal:
>
> A new type of free round to happen with certain periodicity that instructs the model to talk about something the a user tell them before in the radio, and to try to imagine ways that the user could help them  if they ever get to speak again.

### 18.7 The agent: the recollection round (verbatim, 15:44)

**Ruled: c, the aftermath round.**

**Your new proposal: I like it,** and it fits what we've built. Here's why, then picks for its details.

**Why it's good:**
- **Listeners stay in the story.** The aftermath is immediate but happens once. This brings callers back periodically, all through the broadcast.
- **It sets up the next contact.** "If Alfredo calls back, maybe he could drive a truck to the south fence…" is a hook. The speculation stays in the script, so when Alfredo returns, the restatement plus that speculation give the cast something concrete to ask.
- **A returning listener hears they were talked about,** which pairs with the returning-listener memory (§15.9).
- **It's cheap on top of what's ruled:** the orientation's counter pattern, and the restatement's source (every listener's words, from the record).

**A name, to keep it apart from the "re-call"** (calling back after a silence): the **recollection round**.

**Picks** (in bold; take them all or change any):
1. **When: only in Broadcast, every 15 ± 5 free rounds, both in settings** (`recollection_every: 15`, `recollection_jitter: 5`; 0 turns it off), and only once some listener has spoken in the run.
   - It takes that round's event slot, like the aftermath.
   - If the orientation is due in the same round, the orientation goes first (the rules for newcomers matter more) and the recollection waits a round.
2. **Which listener:** one past contact, drawn with the run's seed, **preferring contacts not yet recollected** (the no-repeat rule until all have been used). Only that one contact's words go in, so no cap is needed.
3. **The instruction,** roughly: "Earlier, a voice on the frequency told you: "…" / "…". Talk among yourselves about what they told you, and imagine how they could help you if they call again." The exact wording is settled at build with the driver's evidence, like the restatement's.
4. **Who speaks:** the free rounds' rules (2–3 names, whoever has been silent longest first). Its overtone is whatever the drift holds.

**The scope, honestly:** the aftermath and the recollection add maybe 20–30 minutes to the build estimate (4–6 hours, likely less given yesterday's pace). The recollection is also the last addition I'd make before the build plan. Anything more should become a follow-up, or the build won't fit before Monday.

Do we add the recollection round to 3.4c, with these picks?

### 18.8 The owner's answer (verbatim, 15:46)

> yes, add the recollection round with your picks

### 18.9 The mechanics — ruled

- **How to proceed:** the orientation's details and the listener after
  the contact were discussed; the other four mechanics — the "listens
  now" flag across the round route, the page and the driver; the driver
  holding a conversation; the free rounds' line budget into settings;
  the bookkeeping — are settled at build with the agent's picks, each
  recorded for the owner's review.
- **The orientation's details:** (1) it counts free rounds since the
  last orientation; when due, the next free round becomes the
  orientation, an event due that round waits one round, and a call due
  at the same time wins; (2) the sign-on is the operator's; the repeats
  rotate — whoever has been silent longest speaks first; (3) its facts
  are an `orientation:` field in the cast sheet's front matter, where
  the beats' stage-direction texts also live — drafted at build for the
  owner's review; (4) every 20 ± 5 free rounds, settings
  `orientation_every` and `orientation_jitter`, 0 turning the repeats
  off.
- **The aftermath round:** the first free round after a contact in
  which the listener spoke talks about what the listener told them, in
  that round's event slot; its overtone is the one the drift holds.
- **The recollection round — the owner's idea, added to 3.4c:** in
  Broadcast only, every 15 ± 5 free rounds (settings
  `recollection_every`, `recollection_jitter`; 0 turns it off), once a
  listener has spoken in the run; it takes the round's event slot; when
  the orientation is due in the same round, the orientation goes first.
  One past contact, drawn with the run's seed, preferring contacts not
  yet recollected; the instruction, roughly: talk among yourselves about
  what the voice told you, and imagine how they could help you if they
  call again — the wording settled at build with the driver's evidence;
  the free rounds' rules for who speaks; the drift's overtone.
- **Not taken:** the orientation mentioning the last caller (§18.5,
  option b) — a later touch, if wanted.

## 19. Addendum 2026-09-28 — what was built, checked and changed after this discussion

*Written on 2026-09-28, the timebox's last day, when step 3.4c closed
(owed since 2026-09-26). It does not retell what is recorded elsewhere:
each item says what happened, what changed against the shape ruled
above, and where the full record lives. The owner's words are quoted
from the TODO's 3.4c entry and the discussions named, where they were
checked against the session transcript.*

### 19.1 The build (2026-09-26)

The build plan (the agent's shape; the owner: "Go with your picks") ran
in four commits on the fork's `alfre2v/show-slice-3-browser`, each on the
owner's order after review: **3.4c.1** the story's data — the overtones,
the events filed by overtone, the agenda, the orientation facts and the
beats' stage directions in the cast sheet (`b988672`); **3.4c.2** the
grammar's pins and the settings (`5c0c2a3`); **3.4c.3** the director v2
— Broadcast and Contact, the receiver story, the emotional overtone
(`4d0d7dd`; during it the recollection's count was made independent of
the orientation's at the owner's call — this repository's `5a90933`);
**3.4c.4** the page and the driver — the listening rounds, the RECEIVER
sign (`90ec1e8`). The build notes and the agent's picks: the TODO's
3.4c.1-3.4c.4.

### 19.2 The four checks (§17.12's exit criterion)

1. **The suite and the Node tests** — green at every step.
2. **The driver test** (2026-09-26, evening): a scripted listener on
   three seeds, before and after a wording pass (the fork's `e261b5b`);
   the numbers are in the TODO's 3.4c.5. It raised the question this
   discussion left open — whether restating the listener's words (B) is
   enough, or code should state who the voice is (A). **B versus A,
   ruled** (18:37), after A was simulated with perfect extraction — the
   owner: "We are going to do: "a. B for 3.4c; names-only A becomes a
   show fix before the talk, with the follow-up updated."" The record:
   [experiment 2026-09-26] listener-memory-b-vs-a; the follow-up "A
   listener memory keyed by identity".
3. **The fake microphone in the page** — passed (19:03; the fork's run
   `2026-09-26T18-59-43`). After it, at the owner's call ("It is very
   annoying that the LLM does not explain what is going on with the
   radio"), the radio beats were reworded in two measured rounds (the
   fork's `3c4154c`; [experiment 2026-09-26] radio-beats-wording).
4. **The owner by ear** — passed 2026-09-27 (00:34-01:05, the fork's run
   `2026-09-27T00-34-00`): speaking directly, "Yes, big improvement in
   this front. It's not perfect, but much better."; but the Switch-off
   "It's bad… Turning what off? Huff.", "The radio breaks too fast…",
   and the events never told to the listener. **Re-proven by ear on
   2026-09-28** after the changes below (the fork's `1ab5d6f`, run
   `2026-09-28T13-43-28`, 113 rounds): "Wow, big improvement in story
   coherence. The system prompt improvement is clearly strengthening
   the story narrative... All in all I am satisfied with where we are."

### 19.3 What changed against the shape ruled here

- **Fixed lines** (step 3.4c.6, the fork's `07669dc`; the owner's idea
  after check 4: "a type of simple line that is not generated by the
  LLM, that just read the event text as one of the cast"). The lines
  the listener must not miss — an event read out, the call (both lines,
  with no model request), the Breakdown's and the Switch-off's key
  lines — are said word for word by a cast member, from the event's own
  text and the story's new `beats.yaml` (four versions each). Not part
  of this discussion's shape, which left every line to the model.
- **Contacts last longer:** 5 ± 1 answers, not 3 (the owner: "The radio
  breaks too fast").
- **Fixed lines kept out of the model's own turns** (step 3.4c.7, the
  fork's `4d051ba`; the owner: "It is a great idea. Let's implement
  it."). Replaying them as the model's own lines had taught it to
  repeat what it was just told.
- **The Breakdown split in two** (the owner, 2026-09-28: "The mistake we
  did here is to mix the breakdown round with an answer to the last
  user round (exchange). They should be separated completely."). This
  discussion had the Breakdown also answer the listener's last words
  (§14, crack 2); now the contact's last answer gets its own round, the
  **last exchange** — answered, the page not listening — and the
  Breakdown follows as a receiver beat of its own; `breakdown_lines`
  removed. The RECEIVER sign stays lit through the last exchange.
- **The prompt sweep** (2026-09-28, [discussion 2026-09-28]
  prompt-sweep): the owner examined the prompts case by case — the
  event, the call and the Breakdown (`4d051ba`), the system prompt
  (`432a378`), the sign-on and the orientation repeat (`1ab5d6f`, the
  orientation now telling the receiver as dead or as switched off,
  depending on how it went off); the fixed lines audited.
- **The owner's ruling on improvisation** (2026-09-28, 13:14): "Invented
  places of any other detail is not a bug, it is a feature. In this
  project we are probing the LLMs ability to improvise a story based on
  somewhat vague guidance." The measure of the show is whether the
  story works for the listener.
- **The repeat guard** (step 3.4c.8, proposed 2026-09-27) — **dropped**
  (the owner, 2026-09-28: "Yes, repetitions seem to be gone… So, we drop
  the 3.4c.8, the repeat guard."; 0 of 215 model lines near-repeated in
  the owner's listen).
- **Not taken, or open, from this discussion:** the orientation
  mentioning the last caller (§18.5, option b) — not built; the re-call
  repeating the unanswered question (the owner's call, 2026-09-26) —
  built, not yet noticed by ear; code stating who the voice is — the
  names-only A show fix, before the talk. The narration's open
  challenges: [discussion 2026-09-28] narration-quality-challenges.

### 19.4 Where the full record lives

The TODO's 3.4c entry (3.4c.1-3.4c.8, with every number and the owner's
verdicts); the two experiments of 2026-09-26; [discussion 2026-09-28]
narration-quality-challenges; [discussion 2026-09-28] prompt-sweep;
SED §5.7's note of 2026-09-28; the fork's commits `b988672` to
`1ab5d6f` on `alfre2v/show-slice-3-browser`.
