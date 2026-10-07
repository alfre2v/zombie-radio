# The world outside — the ambience channel (built), and its sound cues (planned)

**Date:** 2026-10-07 · **Arc:** MVP prototype · **Branches:** `alfre2v/ambience` in both repositories (this
repository's #34, the fork's alfre2v/TalkWithZombies#12)
**Type:** discussion — Task 13 in `docs/TODO.md`: how a background of the world outside the lab (the dead, the
fighting, the people, the weather) came to be, every decision taken and why, what was built and heard; then Task 14,
"sound cues": an event round that names a sound plays it, planned and not built.
**Status:** **Part 1 built and heard** (the owner: "it sounds amazing! Very spooky 😃"); both PRs open, the fork's
release (`tz-0.8`) and the installer's pin left. **Part 2 planned** — the shape agreed point by point (§9); the name,
"sound cues", proposed by the agent, not yet ruled; its release order open.
**Trigger to revisit:** the PRs' review; Task 14's build; the proper loudness fix (§6.4).

# Part 1 — The world outside: the ambience channel

## §1. Where it came from

The sound-effect experiment of the same day ([experiment 2026-10-07] sfx-models) tested four open models for sound
effects; **Stable Audio 3 Small-SFX** passed every criterion for live use (0.44 s a take on the A6000, 2.9 GB beside
the stack, no effect on the voice, 87 % of its takes usable or good by the owner's ear). One of its ten test sounds,
a crowd of zombies moaning, came out good in all three takes. The owner, hearing it (verbatim):

> The zombie moan was very good. We need more of this on the show. It's a show about a zombie appocalipse and we do
> not hear any zombies in the background... Now we can fix that!

**The gap it named:** the show's only background sound was the radio static (the static bed, `tz-0.6`). The dead
existed only in the dialogue — the cast speak of the moaning outside; the audience never heard it.

The agent first filed it inside the sound-effects discussion; the owner asked for more (verbatim):

> Wait, the idea of the ambiance sounds should be recorded also in the TODO or in a follow up, don't you think? It is
> distinct to the SFX task, although it requires some sound SFX generation, it's not technically the same task, and
> your observation that is another channel, almost the same logic as the bed, but for ambience sounds that go up and
> down, it's genuinely a good idea to record as a task, even if we don't execute it now.

It became a follow-up ("the dead outside"), then, once the experiment closed, the owner chose it over the alternatives
— the event sounds (§2.3) and more Small-SFX takes per sound — as the next thing to build.

## §2. The plan, and how it grew

### §2.1 The owner's plan (verbatim)

> Implement ambience sounds: I think the best value for our time would be to implement the Ambience sounds, we would
> need to identify a list of maybe 10 to 30 "ambience sound prompts" that we could then make an inference in Stable
> Audio 3 Small and retrieve 3 audios as we did in the experiment... Then I do a quick audition test, pick one for
> each, and we implement a third audio channel with similar techniques that the bed audio... That is my view of the
> plan, but waiting for your corrections and/or additions to my plan.

### §2.2 Widened to the whole world outside

The owner (verbatim):

> Actually as ambiance I do not just want zombies sounds, but also: different types of zombie sounds, like getting
> louder, slow moaning, frantic screams. We need to experiment with different prompts to see what we get, I suppose
> we will need to throw away many of the prompts for lack of a good sound generated. Also: distant sounds of machine
> gun, and shots fired, explosions in the distance. screams in the distance, hysterical laughter in the distance, etc.

### §2.3 The event sounds, set aside — and the ruling on them

The other candidate, a sound per event, was sized by the agent as a library: 289 events, so tags shared by events, and
new page logic to play a sound just before its event's line — about two days. The owner (verbatim):

> As for the "The event sounds" feature, yeah, this one is too much for now. If I ever tackle this one, would be by
> adding stable audio 3 small server to the AI stack, not creating a huge library of sounds to download, that is
> technically boring... We can save this decision with the task.

(Recorded in `docs/follow-ups.md`, "Event sounds as a layer of their own beside the static bed". Part 2 below is a
cheaper cousin of it: no new sounds, the ambience's own clips cued by the event's words.)

### §2.4 The agent's corrections, accepted

- **Two kinds of sound with different behaviour.** The owner's list mixed **textures** — continuous, long, looping
  (a crowd moaning, a storm, warfare) — and **spots** — short single events at random moments (a burst of gunfire, an
  explosion, a scream, a laugh). Spots need silence between them: "a gunfight that never stops stops being
  frightening". One channel: textures continuously, spots sparsely on top, each with their own settings.
- **Prompts written for the channel:** textures steady, nothing that starts or stops abruptly, 20-30 s long (the model
  goes to 120 s at the same cost: fewer seams); spots short.
- **A two-round audition** (round 1, one take a prompt, to screen prompts; round 2, five takes of the kept prompts, to
  pick) — because generation is nearly free and the owner's ear is the only cost.
- **The same preparation as the bed's clips** (levels evened out, a manifest), and **credits** (the clips released as
  CC0 — see §4.3).

### §2.5 The rulings

The agent asked five design questions; the owner (verbatim):

- **Inside or outside the radio?** — "Inside, obviously." Heard through the scientists' microphone, so through the
  same AM filter as the static.
- **Levels and silences** — "Yes, separate from the bed's, as settings. And care should be put so that they do not
  raise and fall at the same time as the bed. They are different sources of audio."
- **The M key?** — "I would say no, the ambience is part of the story... But it my we wise to add a separate button to
  silence the ambience, for example the letter `A`."
- **A story file choosing the clips, like `bed.yaml`?** — "yes".
- **The two clarifications** (inside means through the AM filter, the F key flipping both; the ambience ducks a little
  under the voices so the cast stays easy to understand) — "Yes to your leans under "3. Two clarifications of your
  answers", you got it all right."
- **Three last choices** — MP3 mono 96 kbps: "Mono is good enough, I think, but we can go with your lean."; the F key
  for both: "Yes, both."; a spot every 20-60 s: "Go with your lean."

## §3. The sounds

### §3.1 The prompts

The agent drafted **36 prompts** (`tools/sounds/ambience.yaml`): 15 textures, 21 spots, in five groups — the dead
(textures and spots), the fighting, the people, the city. Written from the experiment's lessons: **one sound per
prompt** (sequences — "thunder, *then* alarms" — had failed); **textures say steady** ("continuous", "low", "rising and
falling"); **spots say what single thing happens**; **concrete sound words, not mood words**. One deliberate test,
`dead-swelling` ("slowly getting louder"), the owner's own wish and a sequence. Left out: a child crying (heavier than
the show's "fun and fake horror" tone; the owner could add it). The owner (verbatim): "Honestly, I will trust your
prompts, I want to see results soon and going one by one will slow me down too much. Let's see what we get as
audios."

### §3.2 Round 1, and the change of plan

`tools/sounds/gen_ambience.py` on the box (Small-SFX, 8 steps, no guidance, offline): 36 takes, seed 1, **0.52-0.57 s
each** (a little slower than the experiment's 0.44 s — longer textures, the stack's load; not measured).
`tools/sounds/ambience_page.py` built the audition page (keep or drop). The owner kept **22 of 36**: 13 of the 15
prompts of the dead; dropped every explosion and all but two of the guns, and most of the city. Then (verbatim):

> Let's simplify the next steps: Everything I picked we can use as it is. It sounds good enough. Now, I would like 3
> takes of thunderstorms sounds, and 5 more sounds of explosions (do not say in the distance, otherwise it gets too low
> volume) and gunfight (you probably have to say repeated gunshots sounds, otherwise it generates a single shot and
> what we want is an ambience of warfare happening outside the lab)

**So no round 2:** the 22 picks are final as they are. Three prompts added: `thunderstorm` (texture, 25 s),
`explosion` (spot, 5 s, no "in the distance"), `warfare` (a **texture**, 20 s — "an ambience of warfare happening
outside" is continuous; "repeated" and "continuous" ask for it).

**The owner's diagnosis, measured:** the new explosions average **-11.7 to -13.0 dB** against the dropped
`explosion-far`'s -16.9 dB and `explosion-muffled`'s -23.1 dB — 4 to 11 dB louder; the new warfare -17.3 and -20.4 dB
against `gunfight-far`'s -21.7 dB. Every take peaks at 0 dB (each is scaled to its own loudest moment), so "in the
distance" made the model produce a far sound — mostly quiet tail and one peak — as a far sound really is.

The owner kept **9 of the 13**: the three thunderstorms, two explosions (seeds 4, 5), four warfare (seeds 1, 3, 4, 5).

### §3.3 The library

**31 clips — 16 textures, 15 spots** (the picks are the `keep:` lists of `tools/sounds/ambience.yaml`; 14 prompts
dropped):

| | Textures | Spots |
|---|---|---|
| The dead | 6: the far crowd, the horde's murmur, a few close, the restless crowd, banging on the door, the swelling crowd | 7: a long moan, a shriek, a group screaming, a growl, a gurgle, a far howl, snarling |
| Fighting | 4 × warfare | a machine-gun burst, single shots, 2 × explosion |
| People | — | a woman screaming, a man screaming, hysterical laughter far and close |
| The world | 3 × thunderstorm, a car alarm, dogs, a crowd panicking | — |

## §4. The preparation (`tools/sounds/prepare_ambience.py`)

### §4.1 What it does

A sibling of `prepare_bed.py` (which is built around Freesound's ids and credits): it reads the `keep:` lists, finds
the takes in the datasets folder, **encodes each as MP3, mono, 96 kbps** (`<tag>-<seed>.mp3`), **measures the encoded
file** — what ships — with `prepare_bed.py`'s own `measure()` (macOS's `afconvert`, the mono mix's RMS and peak), and
writes `ambience.json` (each clip's file, tag, kind, length, level, gain, prompt, model, seed, licence) and
`CREDITS.md` into the fork's `Sounds/ambience/`. A dry run by default; `--write` to write.

### §4.2 The levels — and a cap for the spots

Every clip is brought to the bed's common average level, **-20 dBFS**. One addition: **the gain is capped so the peak
stays at -1 dBFS** — an explosion is mostly quiet tail around one boom, so raising its *average* to the common level
would push its peak far past full scale. Capped clips stay quieter than the common level (`gun-shots-far`: an average
of -26.8 dB, a peak at full scale — it would have needed +6.8 dB, it gets -1.0), which suits sparse spots; the story's
`gain_db` lifts one by ear if needed. **31 clips, 5.3 MB, 438 s of sound** (the agent's estimate: 5 MB; as WAV, about
120 MB). Gains from -9.9 dB (the explosions) to +10.6 dB (the quiet "few close" moaning).

### §4.3 The licence

The clips are **released by the project as CC0** (the fork's tests allow only CC0 or CC BY for shipped sounds; the
app is MIT). The basis, read on 2026-10-07 in the Stability AI Community License (the model's licence, at
`stability.ai/community-license-agreement`, "Last Updated: July 5, 2024"): "Ownership of Outputs. As between You and
Stability AI, You own any outputs generated from the Models or Derivative Works to the extent permitted by applicable
law", and its "Derivative Works" "do not include the output of any Model". A reading, not legal advice; the copy the
owner accepted on Hugging Face may be newer. `CREDITS.md` names the model, quotes the clause, and lists every clip's
prompt and seed.

## §5. The build in the fork (alfre2v/TalkWithZombies#12)

### §5.1 What the agent read first, and what it changed in the design

The agent read the bed's whole path before writing (`app/show/bed.py`, the route, `ShowConfig`, `ShowBed`, the story's
`bed.yaml` loader, `static/show/bed.js` in full, the templates, `test_show_bed.py` and `test_show_bed.js`). Three
findings shaped the code:

- **`bed.sounds` is "the gain of every sound but the voice"** — the M key's mute. The ambience must not go through it,
  or M would mute it too (the owner: M mutes the static only). It gets **its own mute node**, for the A key, straight
  to the speakers.
- **The AM filter's band lives in the bed's settings** (`bed_filter_low_hz`, `bed_filter_high_hz`). "Inside the
  broadcast" is one radio: the ambience uses **the bed's band**, copied into its start reply, and **the F key flips
  both** — `ambience.js` listens after `bed.js` and follows the bed's state, so the two never disagree.
- **`bed.js`'s pure rules are global functions** (the shuffle, a time in a range, the fading's target): `ambience.js`
  loads after it and **reuses them** rather than copying.

And one choice made while writing: **the silences mute only the textures; spots bypass them**, so a scream or a burst
of gunfire can come out of a lull, when it startles most. Not carried over from the bed: "silent while the receiver is
on" (`bed_off_in_contact`) — the world outside does not stop for a call.

### §5.2 The chain

```
a texture <audio> → its gain → the silences' gate ─┐
a spot <audio> → its gain × spot_volume ───────────┴→ the ambience's level (mono; volume_voice under a line,
volume_between between rounds, 0 while push-to-talk is held) → the AM filter (or straight on) → the fading
→ the A key's mute → the speakers
```

### §5.3 The files

- **The app:** `app/show/bed.py` — the manifest reader, the play list and the clip check take the folder, the
  manifest's name and the sound's name as parameters, and carry each clip's `kind` (texture or spot); the bed calls
  them as before (its tests unchanged). `app/config.py` — `get_ambience_directory()` and 15 `ambience_*` settings.
  `app/show/story.py` — the story reads `ambience.yaml` with the bed's loader (its error names the right file).
  `app/models.py`, `app/routers/show.py` — the start reply's `ambience` (its clips with their kind, its settings, the
  bed's filter band) and `GET /api/show/ambience/<file>` (only a file the manifest lists).
- **The page:** `static/show/ambience.js`, loaded after `bed.js` wherever it is (the designed pages; the plain page
  with `&bed=on`), wrapping `setState` after it.
- **The sounds:** `Sounds/ambience/` (31 MP3s, `ambience.json`, `CREDITS.md`); `stories/lab-outbreak/ambience.yaml`
  (the 31 clips, each with its prompt as a comment, `enabled: true` and `gain_db: 0` — the owner: "please add the
  `gain_db: 0` lines under each clip, I know it does nothing currently, but it makes it easier for me to add a volume
  correction later").
- **The defaults** (the silences and fading deliberately unlike the bed's, so the two never move together):

| Setting | Static bed | Ambience |
|---|---|---|
| Volume between rounds | 0.15 | **0.3** (§6) |
| Volume under a line | 0.05 | **0.12** (§6) |
| Dip / rise, s | 0.5 / 1.5 | 0.8 / 2.5 |
| A silence every / its length / its fade, s | 30-120 / 3-15 / 1 | 45-150 / 5-20 / 2 |
| Fading | ±3 dB every 2-6 s | ±4 dB every 5-15 s |
| Spots | — | every 20-60 s, × 1.0 |
| AM filter | off; 300-3,000 Hz | the bed's switch and band |
| Silent while the receiver is on | `bed_off_in_contact`, off | — (goes on) |

- **The tests:** `tests/test_show_ambience.py` (the kinds, the story's choice, the files served, the shipped clips: on
  disk, both kinds, all CC0, all credited), five tests in `tests/test_routers_show.py` (the start reply, the settings,
  the story's choice, the route, the templates), `tests/test_show_ambience.js` (15 tests: the levels, the wiring, the
  spots, the silences, the A, M and F keys). **pytest 1,312 passed; Node: ambience 15, bed 29, page 42, gauge 8,
  persona 17, TTS 91.** One Node test first failed on the agent's wrong guess of a shuffle's order (with the dice at
  0.5, two textures stay in order); the test was corrected, not the code.
- **The docs:** AGENTS.md (the endpoint, the `ambience.js` row, the test rules), `docs/runbooks/show-settings.md`
  ("The ambience", the A key), `docs/runbooks/show-page.md` ("The ambience").

## §6. Heard: too quiet, and why

### §6.1 The owner's first listen (verbatim)

> I am listening to the radio show. First of all, congratulations on a great execution. Now, the only issue I have is
> that I can barely hear the ambiance sounds, the bed sound louder must of the time... I am not sure if it is a volume
> level thing, or that the pauses are so big that most of the time there is nothing to hear.

### §6.2 The agent's diagnosis

1. **On paper the two were almost level:** both prepared to -20 dBFS; between rounds the ambience at 0.12 against the
   static's 0.15 — about 2 dB quieter; under a line both 0.05.
2. **Equal average level is not equal loudness.** The static is a broadband hiss with much of its energy at 2-5 kHz,
   where the ear is most sensitive; a low moan or a distant rumble of the same energy sounds much quieter, and the
   hiss partly masks it. Both preparation tools measure plain energy (RMS), which does not weight frequencies as the
   ear does.
3. **The prompts asked for distance** ("far away", "muffled") — the same effect as the explosions (§3.2).
4. **The pauses matter little:** the textures' silences average 12.5 s every 97.5 s — silent about 11 % of the time;
   spots every 40 s on average.

### §6.3 The fix, by ear

Raised in the clone's `settings.yaml`, about 8 dB (× 2.5): `ambience_volume_between` 0.3, `ambience_volume_voice` 0.12
— twice the static between rounds, more than twice under a line. The owner: "much better now, make those the
defaults." Made the defaults (the setting, the start-reply test, the runbook's recipe with the reason); the clone's
`settings.yaml` back to `seed: 42` alone.

### §6.4 The proper fix, for later

Measure **perceived loudness** (LUFS, the broadcast standard, which weights frequencies as the ear does) in both
preparation tools instead of raw RMS — then the static and the ambience would start genuinely level, and the settings
would mean what they say. Not done.

### §6.5 The verdict

After a reload (§8.1): "I have to say, it sounds amazing! Very spooky 😃"

## §7. What is left of Part 1

- **The release:** merge the fork's #12 (first) and this repository's #34; tag `tz-0.8`; pin the installer; the
  owner's re-proof (`make client-mac` twice).
- **The proper loudness fix** (§6.4), if ever wanted.

## §8. Lessons and mistakes of Part 1

1. **The agent restarted the app while the owner was listening** — to apply a settings change — and the page's next
   requests found no server. The owner: "Ups, we have errors while I was listening, maybe because you restarted the
   server?" The old app's log showed every request "200 OK" up to the stop; the run was safe on disk; a reload and
   Start (or Resume) recovers. **Never restart a server someone may be listening to without asking first.**
2. **Helper servers left running:** two small file servers (ports 8041, 8042) for the listening pages outlived their
   use — their timeouts did not stop them. The owner noticed. **Stop each helper as soon as its step is done.**
3. **The seed does not cover the ambience:** the dialogue is replayed by `show.seed` (the clone runs `seed: 42`), but
   which texture, which spot and when come from the browser's own random numbers — the soundscape differs every run.
   It matters for Task 7's video: a retake replays the words, not the ambience.
4. **Distance in a prompt is loudness in the sound** (§3.2), and **energy is not loudness** (§6.2).

# Part 2 — Sound cues (planned): the event's words call a sound

## §9. The idea and its shape

### §9.1 The owner's idea (verbatim)

> I am getting a bit greedy here, but one proposal: One thing that occurs to me is that there are keywords that we
> know are in the prompts, however we do not have a field for the text prompt in our clips... But we would add a
> keywords list under each clip, and if the event text contains any of the keywords then we immediately insert that
> audio to be played as ambience... What do you think? Discussion first, no execution yet.

### §9.2 The name

The agent proposes **"sound cues"** — the theatre and radio-drama word: when the script reaches a moment, the stage
manager calls the cue and the sound plays. (The owner's working name: "Ambience to event coupling?") Not yet ruled.

### §9.3 The data the agent gathered first

- **The story's events** (289, `stories/lab-outbreak/events.yaml`), against nine keyword groups (explosion, gunfire,
  scream, laughter, storm, dogs, alarm and siren, the dead's moans, banging and scratching): **31 events match at least
  one, 11 %**. With events about every other free round, cues from events alone would be rare — one every several
  minutes.
- **Keywords misfire**, even in that quick count: "gunfire" caught "A fire *alarm*"; "scream" caught "Feedback
  *shrieks* through the headphones" (a radio sound, not a person); "storm" caught "The *rain* fills the rooftop tanks
  with clean water" (good news, not a storm); "dogs" caught a dog that *whines*, not barks.
- **A real show's dialogue** (the owner's 73-round run on the 3090, `runs/2026-10-06T02-20-12`): **179 spoken lines (36
  of them fixed lines — events read aloud), 11 matching a group, about 6 %** — "An explosion rattles the windows from
  the direction of the chemical plant." (an event), "Far away a siren wails, then another joins it, then another." (an
  event), "A helicopter and **a chain gun**? Over." (the model's own line); one misfire: "We're picking up static again,
  like the radio's **screaming**." (The agent's first count read zero lines — a script reading the record wrongly;
  checked and redone.)

### §9.4 The agent's first answer, and the owner's pushback on its size

The agent proposed matching **every spoken line** in the browser (events and the cast's own mentions; on that show
about 11 cues in 73 rounds), with a cooldown, and estimated **half a day**. The owner (verbatim):

> I don't understand why you estimate such high effort for this task? In my opinion it's just to call a new route to
> the server before each round, and if we get an override the ambience we just change the ambience sound... How is
> that "half a day"?

**The agent's answer:** the half day was for the harder design — matching every line in the browser, timing a sound
against a line's audio, a cooldown. The owner's event-only version removes nearly all of it (§9.5).

### §9.5 The six points, as discussed (the owner's answers verbatim)

1. **Match the spoken lines, not just the events** — the owner: "Right, it's a valid idea, but I worry that it would
   lead to too many sound transitions (I know you propose a cooldown)... I am a bit skeptical... Do you see any
   simplification on execution if we do it just at the beginning of an event rounds, I would imagine yes, because we
   know the event text before the round executes, and we can keep the sound running as long as the audio is, to cover
   also the responses of the cast." **The agent agreed — event rounds only:**
   - **the server knows the event before the round runs** (the director picks it; the round's record has an `event`
     field): the match happens **once, on the server**, in Python — the event's text against the clips' keywords;
   - **no new route**: the round's reply already begins with a start message the page reads; the match goes in it as
     one more field, a cue such as `{"file": "explosion-4.mp3", "kind": "spot"}`, acted on when the round starts;
   - **no matching in the browser, no timing against a line, no cooldown** — events come at most every other free
     round, they cannot pile up;
   - **testable where it is easy**: the matching in pytest, only "the page plays the cue" in Node.
2. **Keywords per clip, in the story's `ambience.yaml`** (the owner's proposal) — "Yes, this is good." Whole words,
   case-insensitive; short, careful lists (`explosion`, `explodes`, `blast` — never a loose word like `fire`).
3. **Timing** — "correct": the cue acts when the round starts, as the event is read aloud.
4. **Keeping it from piling up** — "Ok, yes": a cued spot **resets the random spot timer** so two do not land
   together; several matching clips — one of them at random. (With event rounds only, the cooldown is no longer
   needed.)
5. **Misfires will happen** — "yes, but also now at random, so it's not worse."
6. **Spots first, textures later** — the owner: "This is your most interesting point here. I did not think about
   this. Very good." **Combined with point 1, the clip's kind decides what a cue does:**
   - **a matched spot** (an explosion, a scream) **plays once, at the round's start**, as the event is read;
   - **a matched texture** (the storm, the warfare, the moaning) **replaces the current texture** at the round's start
     and **plays to its end** (20-25 s), covering the cast's responses — the owner's "keep the sound running as long as
     the audio is" — then the shuffle resumes.

### §9.6 The estimate, for this design (the agent's)

| Piece | Estimate |
|---|---|
| `keywords:` per clip in `ambience.yaml`, the loader's validation, tests | 30 min |
| The server: the event's text matched (whole words, case-insensitive), one matching clip picked, the cue in the round's start message, tests | 45 min |
| The page: on a cue, the spot played (the random spot timer reset) or the texture swapped in, Node tests | 45-60 min |
| The keywords for the 31 clips (the agent drafts, the owner skims), the runbook | 30 min |
| **Total** | **about 2½-3 hours** — mostly the tests in both languages and the docs; the code perhaps 40 lines in the server, 30 in the page |

### §9.7 Open

- **The name** (§9.2).
- ~~"As long as the audio is": the clip's length or the round's length~~ — **ruled: the clip's length.** The owner
  (verbatim): "I lean the the clip's length, let's keep things simple... But I am open to pushbacks." The agent had
  none: a round is about three lines, 15-25 s with the gaps, and the textures 20-25 s, so a cued texture covers the
  event and the responses by itself; outlasting the round is a feature (the storm carries into the next one, as weather
  would); looping to the round's end would need the page to know when the round's audio ends and make a 20 s clip's
  seam audible. When the cued texture ends, the shuffle resumes with a random texture (the usual 0.6 s fade-in).
- **The release order:** this in the same release as the ambience (holding #12), or **#12 merged and released now as
  `tz-0.8`, the cues after as `tz-0.9`** — the agent's lean: a working release in hand while this is built.

## §10. Where things are

- **This repository:** `tools/sounds/ambience.yaml` (the prompts, the picks), `gen_ambience.py`, `ambience_page.py`,
  `prepare_ambience.py`; `docs/TODO.md` Task 13 (and Task 14, the cues); this document; the experiment
  `docs/experiments/2026-10-07-sfx-models/`.
- **The fork:** `static/show/ambience.js`, `app/show/bed.py`, `Sounds/ambience/`, `stories/lab-outbreak/ambience.yaml`,
  the tests, the runbooks (§5.3).
- **Outside git:** the takes in `/Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/ambience/` (`round1/`,
  `extra/`, each with its audition page `index.html`); on the box, `~/sfx-lab/` (the environments, the weights, the
  takes — kept by the owner's ruling, 39 GB; the disk 17 GB free).
