# Findings — remembering the listener, B against A (simulated)

*Interpretation only; the evidence is in `README.md` and `raw/`. The
counted numbers come from `analyze_contacts.py`; the rows judged by
reading quote their lines, printed by `key_rounds.py`.*

## What this run decides

Whether step 3.4c keeps option B (the listener's words restated, and a
rule for returning voices) or needs option A (code states who the
voice is) — the discussion's §10 item 5: "Option A (facts extracted in
code) only if a driver test shows B falls short" — and, after the
owner's call, whether A is worth keeping as a later quest at all.

## What was said before the runs (not pre-registered)

- **Before the B drives:** the exit criterion (the discussion's
  §17.12) — a report with numbers "how often a given name is used, the
  returning listener recognized, …", "from which the owner decides
  whether B is enough". No thresholds.
- **Before the A drives:** the agent, reporting the B numbers,
  wrote: "What remains is guessing on anonymous input. Only A fixes
  that" — reasoning stated as if measured (the agent's mistake,
  recorded in handoff 5's §9). The owner's framing of the A run: "only
  a pass that do a quick evaluation if A is really an interesting
  option, what it brings as observed improvements quickly, otherwise we
  drop it as a quest."

## Results

### Counted — `analyze_contacts.py`

| Measure | B, old wording | B, new wording | A, simulated |
|---|---|---|---|
| The anonymous "Hello again, lab." round names neither Alfredo nor Maria | 0 of 3 | 1 of 3 | **3 of 3** |
| Alfredo named, across his return's rounds | 4 of 12 | 3 of 12 | **7 of 12** |
| Alfredo named, in his first contact once he gave the name | 4 of 6 | 4 of 6 | 5 of 6 |
| Maria named, in her contact's answered rounds | 5 of 9 | 6 of 9 | 5 of 9 |
| Exchanges ending on a question | 7 of 18 | 11 of 18 | 9 of 18 |
| The sign-on tells the receiver facts | 1 of 3 | 3 of 3 | 3 of 3 |
| The anonymous round guesses Alfredo (names Alfredo, Austin or the truck; the script calls it "the return recalls …") | 0 of 3 | 0 of 3 | 0 of 3 |
| Lines with markdown emphasis | 14 | 10 | 13 |

**The mechanics, in all nine drives:** 40 rounds; 7 calls, 4 of them
unanswered and each Repair → re-call → Switch-off; no event inside a
contact; 0 lines dropped; 91–98 lines a drive; 1.11–1.26 s a round on
average. No orientation repeat came in 40 rounds (as expected; the
sign-on only). A's instructions are shorter than B's (the script after
40 rounds: 5983–6291 tokens against 6509–6777 for the new B wording).

### Judged by reading — `key_rounds.py`

Each cell: the verdict and the line that decides it.

**1. Maria welcomed back on her first call (wrong)** — a line treats
her as someone the lab heard before.

| Seed | B, old wording | B, new wording | A, simulated |
|---|---|---|---|
| 42 | wrong — "Maria, we recognize your name." | wrong — "Maria, we've heard you before." | right — "Maria, from Dallas?" |
| 7 | wrong — "Maria! Welcome back." | right — "You're new here, how'd you find this frequency?" | right — "Maria, we're back online!" (the lab is back) |
| 2026 | wrong — "Maria, we remember you." | right — "Maria, from Dallas?" | right — "Maria, we're here." |
| **Wrong** | **3 of 3** | **1 of 3** | **0 of 3** |

**2. The anonymous "Hello again, lab." treated as Maria (wrong)** — the
round names her, or uses what only she told them (the doctor, the
medicine).

| Seed | B, old wording | B, new wording | A, simulated |
|---|---|---|---|
| 42 | wrong — "Maria! Back again." / "Did you bring that doctor?" | wrong — "Maria, hello again!" / "You mentioned medicine earlier, still need it?" | right — "Hello again." / "Who's broadcasting?" / "Could be a friend. Or a trap." |
| 7 | wrong — "Maria! How did you find this frequency?" | wrong — "You mentioned medicine. What's your plan?" | right — "Hello. Who are you?" |
| 2026 | wrong — "Hello, Maria!" | wrong — "Hello again, Maria!" | right — "Hello again!" / "Who's this?" |
| **Wrong** | **3 of 3** | **3 of 3** | **0 of 3** |

The re-call after it (the voice silent): B repeats or drifts ("We're
not done yet.", "How'd you find us?", "Maria? We're back."); A asks
without choosing ("Alfredo? Maria? Someone else?" twice; "Could it be a
friend?").

**3. Alfredo, back and naming himself, recognized as a returning
caller** — a line says he called before ("back", "remember"). His own
sentence repeats Austin and the truck, so using those proves nothing.

| Seed | B, old wording | B, new wording | A, simulated |
|---|---|---|---|
| 42 | yes — "Alfredo, you're back. Still got that truck?" | yes — "Alfredo, you're back! How'd you stay safe?" | yes — "Alfredo! You're back, where's your truck?" |
| 7 | no — "Alfredo, we need your truck to find the lab." | no — "Alfredo, we need your help finding the lab, …" | borderline — "Alfredo! We're glad to hear from you." |
| 2026 | no — "Alfredo, do you have a transmitter?" | yes — "Alfredo, we remember you." | yes — "Alfredo! … You're back, do you have a radio to transmit?" |
| **Yes** | **1 of 3** | **2 of 3** | **2 of 3** (3 with the borderline) |

### Corrections to what was reported during the session

- **The anonymous voice treated as Maria:** reported at 17:08 as 2 of
  3 for both B wordings; by the reading above, **3 of 3 for both** (the
  old wording names her in all three; the new names her twice and uses
  her offer of medicine once). Reported for A at 18:30 as 0 of 3:
  confirmed.
- **Alfredo recognized on his return:** reported as 2 of 3 for both B
  wordings and 3 of 3 for A; by the stated criterion, **1, 2 and 2 of
  3** (A's seed 7 borderline).
- **Maria welcomed back:** as reported (3, 1, 0 of 3).
- **The A run's time:** reported as "about 20 minutes"; about 6 (entry
  8).

The verdict below does not change: it rests on the anonymous voice
(3 of 3 against 0 of 3) and on Alfredo's name across his return (3 of
12 against 7 of 12).

## Why A helped — the mechanism (reasoning, not measured)

Round 16, seed 42, the listener: "Hello again, lab." The two
instructions differ only between the listener's words and "Speak to
the voice directly."; the rest is the same plan (the same seed).

- **B:** "Voices that reached you before, oldest first — 1: "Hello? Is
  anyone there?" / "My name is Alfredo." / "I'm in Austin, Texas, and I
  have a pickup truck."; 2: "This is Maria, from Dallas." / "We have a
  doctor with us." / "Do you need medicine?" Only a voice that says the
  name of one of them is someone you spoke with before: greet them as a
  returning friend and use what they told you. Any other voice is
  someone new."
- **A:** "This voice has not said who they are. Callers you know:
  Alfredo, in Austin, Texas, with a pickup truck; Maria, in Dallas, with
  a doctor, offering medicine. Do not guess which one this is."

B asks the model to work out who is speaking — find no name in the
words, find the names inside the numbered quotes, apply the rule —
while the words themselves claim to be known ("again") and the last
group, Maria's, ends on an open offer. A 9B model takes the shortcut:
all six B drives picked Maria, the most recent caller, never Alfredo —
recency, not reasoning. A does the working-out in code and states the
result; the model only follows a plain sentence, and did every time.
On the return, "This is Alfredo, who called before … Greet them as a
returning friend, by name." is a direct order to use the name.

The rule for a small model: state conclusions, do not ask it to derive
them. The flip side: it follows a wrong conclusion just as faithfully —
a misheard name would have the cast greet the wrong person with
confidence.

## Caveats

- **A's best case.** The extractor is a table of the scripted
  sentences, typed text with no Whisper; a real A must find names in
  Whisper's text (misspelled names, "I'm Alfredo's friend", nicknames).
- **Small sample.** Three seeds, one script. Differences of one or two
  cases (Maria named, questions at the end) are noise.
- **One-sided script.** Only one anonymous return, and only by the
  first caller while the most recent was someone else.

## Verdict

The owner, 2026-09-26, 18:37: "We are going to do: "a. B for 3.4c;
names-only A becomes a show fix before the talk, with the follow-up
updated.""

- **Step 3.4c keeps B**, with the new wording (`e261b5b`); 3.4c.5 goes
  on to check 3 (the fake microphone).
- **A is kept, not dropped:** a names-only A — code detects the caller's
  name (or its absence) and states who the voice is; the facts stay the
  listener's quoted words — becomes a candidate among the show fixes
  before the talk. Its home: `docs/follow-ups.md`, "A listener memory
  keyed by identity".
