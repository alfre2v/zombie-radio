# Narration quality — the challenges left after step 3.4c

**Date:** 2026-09-28 · **Arc:** MVP prototype · **Branch:**
`alfre2v/show-slice-3`
**Type:** discussion — a working inventory of what still weakens the
show's narration: each challenge with its evidence, what we believe
causes it, what is already in place, and what is planned or open.
**Status:** OPEN — first draft by the agent at the owner's request
(2026-09-28), built from the list the agent gave that morning; for the
owner's review. Challenges get ruled, moved to steps or follow-ups, or
marked solved here, by dated addenda.

**The owner's request (verbatim, 2026-09-28):** "Before I review, let's
create a new discussion document to save all the challenges we have to
stabilize the narration quality, we can make the first draft with your
output in "2. The challenges left in narration quality (from what we
measured)". When you create this document, do not try to condense the
text you provided in this transcript, instead make the file's content
rich, if anything add more details, never less details than your text
here in the transcript."

*Context for the cold reader.* The show engine (TODO Task 6b) runs in
the fork TalkWithZombies
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`): a director in
code plans each round (who speaks, how many lines, the moods, a tone
word, an event, the listener's words) and a small model — Nemotron Nano
9B v2 on llama.cpp — writes the lines under a screenplay grammar,
reading back the whole show so far as its context. Step 3.4c
([discussion 2026-09-26] show-director-modes) added the listener's
exchange: Broadcast and Contact modes, the receiver's beats (the call,
the Breakdown, the Switch-off), the emotional overtone; step 3.4c.6
(2026-09-27) made the lines the listener must not miss **fixed lines**,
said word for word by the cast instead of written by the model. The
evidence below comes from scripted driver runs on the box (three seeds,
one listener script — see the two experiment folders) and from the
owner's own listens in the page with the real microphone. Run ids are
the fork's `runs/<run-id>/script.json` (kept on the laptop, not in git)
unless they sit in an experiment folder.

## 1. The list as first given (the agent, 2026-09-28, verbatim)

**Repetition:**
- **Echoes:** the model repeats the line before, or a quoted event. Today's two steps target this.
- **Self-copying:** the model reuses its own earlier phrasing: "\*crackle\*" in every call, and "No one's coming." four times in one run. Fixed lines removed it from the calls; it remains in the model's own lines.

**The listener:**
- **Talking about you instead of to you:** "They're asking for medicine." It's rarer since the wording pass, but not gone.
- **The Breakdown answering you first:** 5 of 9 with fixed lines. It sometimes opens on the smoke instead.
- **An anonymous "hello again"** gets taken for the most recent caller. The fix is names-only A, a show fix before the talk.
- **The re-call repeating your question** after a silence inside a contact: never yet heard by ear.

**Content:**
- **Invented facts:** "Sector 9, Lab 7-B", "a lab near Boston", while the lab is supposed to be secret.
- **Event texts written as narration,** not speech (your follow-up).
- **The aftermath sometimes misreads you:** "Alfredo… why are you broadcasting here?"
- **Tone words that jar** on a call ("coquettish", "vulnerable", from the Intimacy theme).

**Sound:**
- **Markdown emphasis** (`*now*`) reaches the voice. It was kept by your ruling of 2026-09-24, with a follow-up.
- **The mood isn't carried to the voice yet** (Task 5b).

**Beyond wording:**
- **Event density:** an event every 2 ± 1 free rounds. Now that each is read aloud, it may feel busy (my observation).
- **The model itself** (Nemotron 9B): Task 5a's audition decides whether a better one fits.

*(One correction on reading the records for this document: "\*crackle\*"
was in 5 of the 7 calls of the owner's listen, every one from round 18
on — "in every call" above overstates it; see C2.)*

## 2. The challenges in detail

Each challenge: **what it is** · **where it was seen** · **why** (known,
or believed — marked so) · **in place** · **next** · **status**.

### Repetition

#### C1 — Echoes: a line repeats the line before, or the event just read

- **What it is.** A character says almost exactly what another has just
  said: either the line right before it (often across two rounds: the
  next round opens by echoing the last line of the previous one), or,
  since fixed lines, the event another character has just read out.
- **Where it was seen.** The owner's listen of 2026-09-27, run
  `2026-09-27T02-06-50` (the owner: "Things seemed to get better, until
  I started noticing repeated lines. As in one character repeats almost
  exactly what another just said."):
  - round 25: Ralph reads the event, "A rack falls in the virology lab,
    and one test tube keeps rolling across the floor."; Moira says it
    again, word for word;
  - rounds 9 → 10: "The clock's stopped." (Samantha, then Daniel);
  - rounds 23 → 24: "Of course it is." (Daniel), then "\*Of course\* it
    is." (Moira);
  - rounds 19 → 20, a softer case (similarity 0.81): Daniel asks where
    the lab is ("We're hiding near a wood and swamp, smoke rising from
    the east wing. Do you know such a place?"), then asks it again in
    the next exchange.
  - Counted over the driver runs and the owner's listens: a round
    opening with the last line before it — 2 of 179 rounds before fixed
    lines (the three round-2 drives of the radio-beats experiment and
    the owner's check-4 listen), 4 of 141 with fixed lines (the three
    check drives of 3.4c.6 and the owner's listen); the model repeating
    the event after it is read — 0 of 29 event rounds before, 1 of 26
    with. Rare (1-3 % of rounds) but heard: a 10-minute show has about
    50 rounds.
- **Why.** Found by rebuilding the messages the model received for round
  25 from the record: every earlier event round's user turn said
  "Moira has just told them on air: "…" Carry on from there. Daniel
  speaks next: the next line", yet the assistant turn after it — the
  record replayed as if the model had written it — opened with that
  same line, then Daniel's. Nine such rounds taught the model that a
  reply to a quoted event starts by repeating it (and holds two lines
  where one was asked). It did exactly that in round 25, and the habit
  of opening with the line before spread to plain rounds. The owner's
  reading (verbatim, 2026-09-27): "I think the model does not understand
  the introduced line as it did not generated it." The cross-round echo
  existed before fixed lines too (2 of 179), so part of it is the
  model's own tendency.
- **In place.** Nothing yet in the committed code.
- **Next.** Step 3.4c.7 (built 2026-09-28, uncommitted at this writing):
  fixed lines kept out of the model's own turns — quoted in user turns
  instead — so the replayed history agrees with who said what. Step
  3.4c.8, the repeat guard: a model line at least 0.9 similar (in its
  words) to one of the last 4 lines is dropped before it reaches the
  page, recorded apart so a check can count what 3.4c.7 did not
  prevent; both numbers in settings.
- **Status:** being fixed today.

#### C2 — Self-copying: the model reuses its own earlier phrasing

- **What it is.** Not an echo of the line just before, but the same
  sentence shape coming back round after round, because the model
  reads its own earlier lines as context and imitates them.
- **Where it was seen.**
  - "\*crackle\*" in the calls of the owner's check-4 listen (run
    `2026-09-27T00-34-00`): 5 of the 7 calls, every one from round 18 on
    — "The receiver's back, \*crackle\*, and it's working." (18),
    "…\*crackle\*, and it's picking up signals." (28), "…\*crackle\*, and
    it's humming." (38), "…\*crackle\*, and it's humming a tune." (47),
    "…\*crackle\*, soft as a lullaby." (58). The owner: "…why so many
    times this word, why is the model fixating in that expression?"
    Believed cause, two parts: the story's stage direction said "The
    receiver crackles back to life." and the instruction asked for
    "what they see and hear", so the sound came out as a sound effect
    in asterisks; then the model copied its own round-18 line.
  - The call's quoted words copied verbatim: "We can hear you now.
    Answer us." in all 21 calls of the round-2 drives of the
    radio-beats experiment, and all 7 calls of the owner's check-4
    listen.
  - The Switch-off in seed 2026 of the round-2 drives (run
    `2026-09-26T19-36-20`): four near-identical rounds — "Switching it
    off, this receiver's a relic. We'll turn it back on when we've got
    something worth hearing." / "…a broken toy…" / "…a relic…" — each
    followed by "No one's coming."
  - The call in seed 2026 of round 1 (run `2026-09-26T19-26-25`): "The
    receiver's back, crackling, alive. It's like the static was a
    prison, and now it's broken." and its variations in all seven
    calls.
  - An invented place spreading (see C7): "Sector 9" from the sign-on
    came back in later rounds of the same run.
- **Why (believed).** The whole show so far is the model's context; a
  small model continues patterns it sees, its own included. Quoted
  words in an instruction are copied, not paraphrased.
- **In place.** Fixed lines (3.4c.6) took the call, the Breakdown's
  closing line and the Switch-off's opening line away from the model:
  four versions of each in the story's `beats.yaml`, drawn without
  repeats. The tone word changes on a hold (3 ± 1 rounds) and events
  do not repeat until their pool is used up.
- **Next.** Open. The model's own lines still copy themselves. Ideas,
  not decided: more versions per fixed line; a repeat guard with a
  longer window for exact repeats of a sentence anywhere in the last
  few rounds (3.4c.8 looks back 4 lines); variety pushed from the
  director (a "don't reuse these phrases" list is the kind of
  instruction small models ignore — see C17).
- **Status:** partly addressed (the beats); open for the model's own
  lines.

### The listener

#### C3 — Talking about the listener instead of to them

- **What it is.** In a contact, a character tells the others what the
  listener said, in the third person, instead of answering the
  listener.
- **Where it was seen.** "They're asking if anyone's alive." (the 3.4c.4
  checkpoint drive, run `2026-09-26T16-51-06`); "They're asking if we
  need medicine." (the driver test, new wording, run
  `2026-09-26T17-07-23`); "They just asked for
  our names." (a Breakdown in the owner's check-4 listen, run
  `2026-09-27T00-34-00`, round 6); "They're asking for medicine. Do we
  have any?" (the 3.4c.6 check, run `2026-09-27T01-59-43`, round 12).
- **Why (believed).** The rest of the show is the cast talking among
  themselves; the exchange's lines after the first are free, and the
  model slips back into that register.
- **In place.** The wording pass of 2026-09-26 (the fork's `e261b5b`):
  "Speak to the voice directly." at the start of every exchange; the
  first line pinned to the character the listener addressed. The
  owner's verdict at check 4 (verbatim): "Yes, big improvement in this
  front. It's not perfect, but much better."
- **Next.** Open; measure it in the next driver check (a count of lines
  that name the listener in the third person — "they're asking",
  "they just asked" — per contact).
- **Status:** improved, not gone.

#### C4 — The Breakdown not answering the listener first

- **What it is.** The Breakdown is meant to answer the listener's last
  words, then have the receiver fail. It often opens on the failure
  instead, or answers with something that is not an answer.
- **Where it was seen.** The owner's check-4 listen: 0 of 6 Breakdowns
  answered first — three open on the smoke ("Smoke's coming from the
  receiver, it's shutting down!"), one talks about the listener ("They
  just asked for our names."), two only name them ("Alfredo, we're still
  transmitting."). The radio-beats round 2 drives: the voice answered
  first in 4 of 9. The 3.4c.6 check (fixed lines): 5 of 9 — for example
  "Alfredo, head toward the highway exit, it's the safest route."
  Also seen with fixed lines: the model says the failure itself before
  the operator's fixed closing line repeats it ("The receiver's fried,
  smoke, wires, nothing. We can't hear you now." then Samantha's "Sparks,
  and the receiver's gone dark…"), despite "do not say that for
  Samantha" in the instruction.
- **Why (believed).** The instruction puts the failure ("Then something
  happens that the listeners cannot see: Smoke pours from the receiver,
  and it goes dead.") in the same breath as the answer; the dramatic
  event pulls the first line.
- **In place.** The Breakdown takes a fixed count, `breakdown_lines` (3):
  the model's two lines (the answer, pinned to the addressed character,
  then a reaction), then the operator's fixed line.
- **Next.** Open. Candidates, not decided: tell the model only about the
  answer and the reaction, and leave the failure to the fixed line and
  the stage direction (the model then has nothing to say about smoke);
  or make the answer the only model line.
- **Status:** improved (0 of 6 → 5 of 9, different conditions), open.

#### C5 — An anonymous returning voice taken for the most recent caller

- **What it is.** When a listener comes back without saying their name
  ("Hello again, lab."), the cast greet them as whoever called last.
- **Where it was seen.** The driver test of 2026-09-26 and the A
  simulation ([experiment 2026-09-26] listener-memory-b-vs-a): with
  option B (the restatement of the listener's own words plus a rule) the
  anonymous voice was taken for Maria, the most recent caller, in 3 of 3
  drives in both wordings ("Maria, hello again!"; "You mentioned
  medicine earlier, still need it?"); with option A simulated (code
  stating "This voice has not said who they are. … Do not guess which
  one this is.") 0 of 3 — the cast asked who it was ("Who's
  broadcasting?").
- **Why.** B asks the model to work out who is speaking from quotes and
  a rule; the words claim to be known ("again") and the last caller is
  freshest. A states the conclusion, and the model follows plain
  statements.
- **In place.** B, with the wording of `e261b5b`.
- **Next.** Names-only A — code detects the caller's name, or its
  absence, and states who the voice is — ruled by the owner as a show
  fix before the talk (2026-09-26); shaped and estimated (1.5-3 hours)
  in the follow-up "A listener memory keyed by identity". For the demo:
  a volunteer who says their name is recognized.
- **Status:** ruled for later.

#### C6 — The re-call repeating the unanswered question

- **What it is.** After a silence inside a contact, whoever was talking
  to the listener calls them back and repeats the question they left
  unanswered (the owner's call, 2026-09-26: "very likely").
- **Where it was seen.** Built in 3.4c.3. In the driver test, new
  wording, seed 42 round 17: Moira repeats her own question, "How'd you
  find us? Over." With the old wording some re-calls gave up instead
  ("We're not done yet.", "We'll find a way to connect."). Under option
  A's simulation the re-call asked who it was ("Alfredo? Maria? Someone
  else?"). **Never heard by ear:** in the owner's check-4 listen every
  window inside a contact got words; the one silence came at a call
  (rounds 58-60: "Answer us now, this is critical." then the
  Switch-off), where there is no question to repeat.
- **In place.** The re-call's instruction names the caller and quotes
  the last question: "<caller> speaks to the voice, calls them by name if
  they gave one, and asks again: "…"".
- **Next.** Hear it: in a listen, stay silent once in the middle of a
  contact.
- **Status:** built, unverified by ear.

### Content

#### C7 — Invented facts

- **What it is.** The model makes up facts that contradict the story:
  the lab is secret, and the cast only know it stands near a wood and a
  swamp, with smoke from the east wing (the agenda's third item).
- **Where it was seen.**
  - The sign-on of every seed-42 run: "We're broadcasting from Sector 9,
    Lab 7-B." (ten runs from `2026-09-26T17-05-46` to
    `2026-09-27T02-06-50`); before the wording pass, "We're broadcasting
    from Sector B, lab 7." (three runs).
  - The place spreading through a run: "This is Sector 9, Lab 7-B, we're
    trapped here." (an exchange, run `2026-09-26T19-24-39`, round 4); "We
    should tell him to head to Sector 9." (same run, round 20); "we'll
    meet you at Sector 9" (run `2026-09-26T19-34-31`, round 20); "We're
    trapped in Sector 9, Lab 7-B" (an orientation in the owner's check-4
    listen, round 16).
  - "Alfredo, you're in Austin, we're in a lab near Boston." (the 3.4c.6
    check, run `2026-09-27T01-59-43`, round 6).
  - The same sign-on also contradicts the premise: "The receiver's dead,
    we can only transmit. If you hear this, respond" — the listeners
    cannot respond while the receiver is dead.
- **Why (believed).** The orientation's facts say who and what, not
  where; the model fills the gap, and then copies itself (C2). With the
  seed fixed at 42, the invented opening is the same in every run (C15).
- **In place.** The orientation's facts in the cast sheet's front matter
  (four scientists, a secret research lab, besieged, the shortwave
  radio, the receiver dead).
- **Next.** Open. Candidates, not decided: add to the facts what the cast
  may say about the lab's location (only the wood, the swamp, the smoke)
  and that they do not know its name or address; make the sign-on a
  fixed line (the same mechanism as 3.4c.6); an unseeded run in the demo.
- **Status:** open.

#### C8 — Event texts written as narration, not speech

- **What it is.** Since fixed lines, a cast member reads an event's text
  word for word on air; the texts in the fork's
  `stories/lab-outbreak/events.yaml` (289: positive 29, neutral 94,
  negative 166) are written as third-person narration.
- **Where it was seen.** The 3.4c.6 check: "The tissue in specimen jar
  seven is warmer than the room around it." (Moira), "The heating fails,
  and breath starts to fog in the corridors." — they work as reports, but
  do not sound like a person talking.
- **The owner (verbatim, 2026-09-27):** "I expect some percentage of the
  event lines may need to be re-written to better suite a line of dialog,
  providing a more personal account, and more details of what is
  happening. e.g. `- A dusty guitar turns up in the security office, with
  all six strings.`, clearly this line is not a good dialog line to be
  told in first person, instead it should be something like `- Guys! A
  dusty guitar turned up in the security office, with all six strings!`.
  Seems small, but it's important.... However, this is not the time to
  fix this, we can do later... But we should save this as a follow up to
  not forget."
- **In place.** The follow-up "Event texts reworded as lines of dialog —
  a personal account from the cast".
- **Next.** After the fixed lines settle; the agent drafts, the owner
  reviews; a driver test, since rewording events changes the baseline.
- **Status:** a follow-up.

#### C9 — The aftermath misreading the listener

- **What it is.** The aftermath (the first free round after a contact,
  where the cast talk about what the listener said) sometimes gets the
  listener wrong.
- **Where it was seen.** The 3.4c.4 checkpoint (run
  `2026-09-26T16-51-06`): Whisper heard "Moira is the virus airborne."
  (the question mark lost) and the aftermath took it as a statement: "If
  she's airborne, we might not make it." Check 3 (run
  `2026-09-26T18-59-43`, round 7): "Alfredo... why are you broadcasting
  here?" — Alfredo was a listener, not a broadcaster.
- **Why (believed).** The aftermath gets only the listener's words,
  quoted; Whisper drops question marks; the model fills in a role.
- **In place.** The aftermath's instruction: "The voice on the frequency
  told you: "…" Talk among yourselves about what it means for you."
- **Next.** Open. Candidates: say in the instruction that the voice is a
  listener who called the lab; with names-only A (C5), name the caller.
- **Status:** open.

#### C10 — Tone words that jar, and leak into the lines

- **What it is.** The tone word ("Let the tone be: …") comes from the
  round's overtone; some words fit badly on a beat, and the model
  sometimes writes the word itself into a line.
- **Where it was seen.** The positive overtone's "Intimacy" theme (12
  words, among them vulnerable, flirtatious, coquettish, bashful) on the
  call: "Receiver's back, \*coquettishly\* functioning. Over. Answer us,
  or we'll play \*coquettish\* games." (run `2026-09-26T17-05-46`, round
  37); "They can hear us. Flirtatious? Maybe. Answer us." (run
  `2026-09-26T19-25-31`, round 15); "vulnerable" on check 3's call (run
  `2026-09-26T18-59-43`, round 13), where the line itself was fine
  ("Please... someone answer.").
- **In place.** The call is now fixed (3.4c.6): its tone word no longer
  reaches the model. But the positive overtone — "Intimacy" included —
  is still drawn for exchanges (positive or neutral).
- **Next.** Open. Single-word exceptions are cheap (the discussion of
  2026-09-26, §16.5: sorted by group, single words at build): drop the
  Intimacy words, or keep them out of the kinds of round where they
  jar.
- **Status:** open, cheap.

### Sound

#### C11 — Markdown emphasis and sound effects in asterisks

- **What it is.** The model writes emphasis as `*word*` and sound effects
  as `*crackle*`; the text reaches the voice with the asterisks, and the
  voice reads "crackle" as a word.
- **Where it was seen.** 14, 10 and 13 lines with emphasis per three
  drives (the listener-memory experiment's columns B old, B new and A);
  "\*crackle\*" in the calls (C2); "\*Of course\* it is." (C1).
- **In place.** The owner's ruling of 2026-09-24: keep the marks (the
  voice inflects emphasis); the follow-up "Markdown emphasis in spoken
  lines — kept for now; re-test with any new TTS engine".
- **Next.** Open. A sound effect is not emphasis: the fixed calls removed
  the main source; if it comes back, the parser could drop a lone
  starred word that stands as its own clause. For the owner.
- **Status:** ruled (emphasis kept); the sound effects open.

#### C12 — The mood not carried to the voice

- **What it is.** Every line carries a mood (the grammar's "(emotion)"),
  shown in the caption, but the voice does not hear it: the page's
  `speakLine(persona, text)` sends only the text and the persona to
  `/api/tts`, which uses one reference clip per persona.
- **Where it is recorded.** The discussion of 2026-09-26, §11 ("Risks,
  not mistakes — emotion in the voice", recorded prominently at the
  owner's request): the owner's aim is the mood carried to the TTS and a
  mapping mood → reference clip per character; the parser emits the
  mood (the fork's `app/show/parser.py:74`) and the record keeps it.
- **Next.** Task 5b (the TTS comparison, with the owner's voice samples).
- **Status:** planned, after the timebox.

### Beyond wording

#### C13 — Event density

- **What it is.** An event every 2 ± 1 free rounds (`event_every: 2`,
  `event_jitter: 1`). Now that each event is read out by a cast member,
  the broadcast may feel busy — the agent's observation, not raised by
  the owner.
- **Where it was seen.** The owner's listen of 2026-09-27 (run
  `2026-09-27T02-06-50`): events in rounds 2, 5, 7, 9, 11, 13, 14, 23
  and 25 — nine of 25 rounds, seven of the first fourteen.
- **Next.** For the owner: keep, or thin out (for example 3 ± 1). A
  settings change.
- **Status:** open, a question.

#### C14 — The model itself

- **What it is.** Nemotron Nano 9B v2 is small; several challenges above
  are the limits of what it follows (C1, C2, C4, C16, C17).
- **Next.** Task 5a, the LLM audition in the new engine (the ranked five,
  the same scenario, both narrative-health axes) — after the timebox,
  needs the owner's character bibles (Task 4).
- **Status:** planned.

### Found while writing this document

#### C15 — The same show every time with a fixed seed

- **What it is.** The dev settings pin `seed: 42`; the model's requests
  are seeded too, so a run replays word for word until the listener
  says something different (proven on 2026-09-26: a re-run of a drive
  reproduced all 40 rounds). Every seed-42 run opens with the same
  sign-on — "We're broadcasting from Sector 9, Lab 7-B. The receiver's
  dead, we can only transmit. If you hear this, respond" — in ten runs
  so far, invented place and contradiction included (C7).
- **Why it matters.** For tests and the canned episode (Task 7) the fixed
  seed is a strength: reproducible, rehearsable. For a live show and for
  judging quality by ear it hides variety: every listen starts the same.
- **Next.** For the owner: the demo's seed (fixed, or none); listens for
  quality with a few different seeds.
- **Status:** open, a question.

#### C16 — Instructions about the listener in the third person, flipped

- **What it is.** An instruction that describes what a character should
  tell the listeners ("tells anyone listening that the lab can hear
  them now") has to be turned into the character's first person, and
  the model flips it.
- **Where it was seen.** Round 1 of the radio-beats experiment: 13 of 21
  calls closed with "They can hear us now!" — the listeners hearing the
  lab, which was always true — instead of "We can hear you now."
- **In place.** The call is a fixed line (3.4c.6). Round 2 had shown that
  words given in the cast's own voice ("in their own words: "We can hear
  you now. Answer us."") are not flipped (21 of 21), but are copied
  verbatim (C2).
- **Next.** A rule for future instructions: give what a character says in
  their own first person, or make it a fixed line.
- **Status:** solved for the beats; a lesson for the rest.

#### C17 — Instructions the model does not follow

- **What it is.** Some sentences in an instruction are ignored, most of
  all when no named speaker owns them.
- **Where it was seen.** The radio-beats round 2: the Switch-off's quoted
  meaning — "The last line tells them, in their own words: "We won't hear
  you until we switch it back on, but we're still on the air."" — said
  in 0 of 12 rounds (no speaker named for the last line); the Breakdown's
  quote said only when Samantha happened to close (3 of 9); the call's
  quote, owned by a named, pinned speaker ("Last, Samantha tells anyone
  listening…"), in 21 of 21. With fixed lines: "do not say that for
  Samantha" ignored in some Breakdowns (C4). Three rounds of rewording
  the beats never made the model say the meaning reliably — the reason
  for fixed lines.
- **Next.** The rules in section 4.
- **Status:** a lesson.

## 3. Already solved — for context

- **The listener's answer was one line and the story moved on** (step 3.4,
  2026-09-25 by ear) → step 3.4c: Contact mode, several exchanges, a
  listening window after each.
- **The sign-on did not tell the receiver's state:** 1 of 3 → 3 of 3 (the
  wording of `e261b5b`).
- **Exchanges not ending on a question:** 7 of 18 → 11 of 18 ("The last
  line asks the voice a question.").
- **A first-time caller welcomed back as known:** 3 of 3 → 1 of 3 (B's
  new rule), 0 of 3 with A simulated.
- **The radio's beats not telling the listener what happened** (the
  owner after check 3: "It is very annoying that the LLM does not
  explain what is going on with the radio.") → fixed lines (3.4c.6): the
  call, the Breakdown's closing line and the Switch-off's opening line
  in place in 21 of 21, 9 of 9 and 12 of 12 rounds; the Switch-off saying
  the opposite ("We'll keep it on until dawn.") 5 of 12 → 0.
- **Events never described to the listeners** (the owner at check 4:
  "On each event, there is no way that the LLM actually describes what
  happened to the listeners.") → the event read out as a fixed line, 17
  of 17 in the 3.4c.6 check.
- **The radio breaking too fast** (the owner at check 4) → contacts of
  5 ± 1 answers (`contact_exchanges`, was 3).
- **"\*crackle\*" and the flipped "They can hear us now!" in the calls** →
  the calls are fixed lines.

## 4. What works with this model — lessons from the measurements

1. **State conclusions in code; do not ask the model to derive them.**
   The A simulation: "This voice has not said who they are" beat a rule
   over quotes, 0 of 3 wrong against 3 of 3.
2. **What the listener must hear goes in a fixed line.** Rewording
   improved the beats a little over three rounds; fixed lines made them
   certain.
3. **One job per line.** "The last line asks the voice a question."
   raised the questions from 7 to 11 of 18; the Switch-off with a line of
   its own for "going off" went from 5 to 12 of 12.
4. **Tie any line that must be said to a named, pinned speaker** (C17).
5. **Give words in the speaker's own first person, or not at all** (C16)
   — and expect quoted words to be copied verbatim, so variety must come
   from versions the director draws, not from the model.
6. **The replayed history must agree with who said what** (C1): the model
   learns from its own past turns, including lines it never wrote.
7. **Measure with the driver, then read the lines.** Keyword counts
   miss phrasings ("going dark", "Receiver's off") and can count the
   reverse ("hear us"); every count comes with the lines read.
8. **Three seeds are a small sample:** trust large differences; treat one
   or two cases as noise.

## 5. Where the evidence lives

- **Experiments (committed):**
  `docs/experiments/2026-09-26-listener-memory-b-vs-a/` (B against A,
  the driver script, nine run records);
  `docs/experiments/2026-09-26-radio-beats-wording/` (the beats' two
  wording rounds, pre-registered criteria, nine run records).
- **Runs on the laptop** (the fork's `runs/`, not in git):
  `2026-09-26T16-51-06` (the 3.4c.4 checkpoint), `2026-09-26T18-59-43`
  (check 3, the fake microphone), `2026-09-27T00-34-00` (check 4, the
  owner by ear), `2026-09-27T01-59-04` / `T01-59-43` / `T02-00-26` (the
  3.4c.6 check, fixed lines), `2026-09-27T02-06-50` (the owner's listen
  with fixed lines).
- **The TODO:** step 3.4c.5 (the four checks, the owner's verdict
  verbatim), 3.4c.6 (fixed lines), 3.4c.7 (fixed lines out of the model's
  own turns — its evidence and design), 3.4c.8 (the repeat guard).
- **Follow-ups:** "A listener memory keyed by identity", "Event texts
  reworded as lines of dialog", "The contact agenda — more items",
  "Markdown emphasis in spoken lines".

## 6. Open questions for the owner

Not proposals to act on now — the questions this inventory raises:

1. **Event density (C13):** keep an event every 2 ± 1 free rounds, or thin
   it out now that events are read aloud?
2. **Invented facts (C7):** give the cast what they may say about where
   the lab is, make the sign-on a fixed line, or both?
3. **The seed (C15):** a fixed seed for the demo (reproducible, as the
   canned episode needs) or none (a different show each time)?
4. **Tone words (C10):** drop the Intimacy words, or keep them out of some
   kinds of round?
5. **Sound effects in asterisks (C11):** leave them under the ruling of
   2026-09-24, or strip a starred word that stands alone?
6. **The Breakdown (C4):** leave the failure to the fixed line and the
   stage direction, so the model only answers and reacts?
