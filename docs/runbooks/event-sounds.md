# Runbook: give an event a sound

*Living, undated (runbooks convention). How a story's event gets a sound that plays when the event is read aloud — a
**sound cue**: find the events that name a sound, write a prompt for each, generate three takes on the GPU box with
Stable Audio 3 Small-SFX, audition them by ear, prepare the kept ones into the fork's library, and give them keywords
in the story. Why sound cues exist and how they were built: `docs/discussions/2026-10-07-the-world-outside.md`
§9-§9.11; the task: `docs/TODO.md`, Task 14.*

The owner (verbatim, 2026-10-07), on how event sounds should be made: "Maybe what we have to do is just to go event
by event, select the ones that can have good audio prompt, and generate 3 audios per each, and let me decide... It
would be more work, but ideally we leave the machinery in place to get more audios if we add more events". This
runbook is that machinery, written out: the first pass (2026-10-08) gave 29 sounds for 35 of the 289 events.

## 1. How a sound cue works (what this runbook feeds)

- The fork's **ambience library** (`Sounds/ambience/`: the MP3s, `ambience.json`, `CREDITS.md`) holds every clip. It
  is written by one tool only, this repository's `tools/sounds/prepare_ambience.py`, from the prompts file
  `tools/sounds/ambience.yaml` and the takes kept by ear. Nothing else touches it.
- The **story** (the fork's `stories/lab-outbreak/ambience.yaml`) chooses: which clips play, a level by ear
  (`gain_db`), the **keywords** that cue a clip, and **`cue_only`**.
- When a free round's event says one of a clip's keywords (a whole word or phrase, any case), the server sends a cue
  before the round's first line, and the page plays that clip as the event is read: a spot at once, a texture in
  place of the current one, to its end. Several clips match: one at random, with the run's seed.
- **A cue can only play a clip that is already in the library.** An event that names a sound no clip has cues
  nothing. That is why an event needs its own sound — this runbook.
- **Every event sound is `cue_only: true`** (the owner: "The event sounds are too specific to be general ambience"):
  in the library and sent to the page, but never in the random rotation — heard only when its event is read.

## 2. The test: distinct and recognizable

The owner (verbatim, 2026-10-07): "each sound must be "distinct" and "recognizable", I could not say what the glass
rain audio was if I did not know the prompt. So, a smoke detector, a fire alarm and a freezer beeping can be good
cues if the sound has those properties." Not inside or outside the lab: "why would a radio mic only pick sounds from
outside and not others happening inside the lab?"

**Would you name the sound if you did not know the prompt?** What passed and what failed on 2026-10-08:

- **Passed** (the sound *is* the event): a helicopter, a jet, sirens, a train horn, a fire alarm, a smoke detector's
  chirp, a freezer alarm's beeping, a telephone, a clock's chime, a PA chime, a music box, a typewriter, a Geiger
  counter, a truck engine starting, fireworks, Morse code, the emergency broadcast tone, knocking, a rooster, crows, a
  galloping horse, an armored vehicle, wind howling, hail, tapping on glass, a dog whining, an owl, a church bell, a
  drone.
- **Failed by ear:** feedback squeal (not distinct enough), footsteps, rats, a generator coughing — and before them,
  the glass rain of the sound-effect experiment.
- **Not tried:** voices and music (a choir, a dance band, a lullaby, the radio's callers — the model is unreliable
  with them), and silent events (a searchlight, fog, a balloon drifting).

## 3. Find the events that name a sound

Print every event with its number, overtone and theme (from the fork's clone; its `.venv` has the YAML reader):

```bash
# Every event of the story, numbered, under its overtone and theme
cd /Users/alfredo/workspace/hackTNT_2026/TalkWithZombies && .venv/bin/python - <<'EOF'
import yaml
events = yaml.safe_load(open("stories/lab-outbreak/events.yaml"))["events"]
i = 0
for overtone, themes in events.items():
    for theme, items in themes.items():
        print(f"## {overtone} / {theme}")
        for e in items:
            i += 1
            print(f"{i:3} {e}")
EOF
```

Read them all and keep those that pass §2. **Several events can share one sound** (the three helicopter events need
one prompt, not three). **When you write a new event**, write it with its sound in mind: an event that says
"a helicopter passes low overhead" can be cued; one that says "a shape crosses the sky" cannot.

## 4. Write the prompt

Each sound becomes one entry at the end of `tools/sounds/ambience.yaml`, in the section "Event sounds", with the
events it cues quoted in comments above it and `keep: []` until the audition:

```yaml
  #   "A jet passes very high overhead, blinking, as if nothing were wrong."
  #   "A plane drops leaflets that flutter down and cover the lawn."
  - {tag: jet, kind: spot, seconds: 10, keep: [], prompt: "A jet airliner flying overhead, a loud deep rumbling roar of its engines"}
```

- **`tag`**: unique in the whole file (the preparation finds a take by its tag and seed; two folders holding the same
  tag and seed stop it).
- **`kind`**: `spot` for a single event (3-10 s), `texture` for something continuous (20-25 s; it replaces the
  background while it plays).
- **The prompt — what worked and what did not** (the sound-effect experiment and 2026-10-08):
  - **one sound per prompt**; a sequence ("thunder, *then* alarms") usually fails (the helicopter's "then fades into
    the distance" is the exception that worked);
  - **concrete sound words**, not mood words: "the high-pitched buzz of its four spinning propellers";
  - **"in the distance" makes a sound quiet** — avoid it unless far is the point;
  - **never "single"** unless one hit is what you want: "a single church bell ringing slowly" gave one bell bang;
  - **name an occasion** when the sound belongs to one: the church bell failed twice as a description and passed as
    "Church bells ringing out in celebration at the Vatican, many large bells pealing continuously";
  - **"The sound of …" and "very loud"** turned the drone and the Geiger counter from unrecognizable into kept.

## 5. Check the keywords against every event

Decide each sound's keywords now, and check them against all the events with the fork's own matching — a loose word
cues a sound where it does not belong (the first draft of 2026-10-07 had "the moaning outside *stops*" cue a moan,
and "shot" would catch "a shot of whiskey"):

```bash
# Which events these keywords cue (fork clone): whole words or phrases, any case
cd /Users/alfredo/workspace/hackTNT_2026/TalkWithZombies && .venv/bin/python - 'jet' 'a plane' <<'EOF' 2>/dev/null
import sys
from app.show.story import load_story
from app.show.cues import says
events = load_story("lab-outbreak").events
for i, e in enumerate(events, 1):
    if says(e, sys.argv[1:]):
        print(f"{i:3} {e}")
EOF
```

- List every form: "explosion" does not match "explosions".
- Prefer a phrase when a word is shared: `flock of crows` (not "crows": "a rooster crows"), `in perfect morse code`
  (not "morse code": a shambler taps "like Morse code"), `rats stream` (not "rats": the lab rats gnaw at their cages).
- Check that no other clip's keywords already cue the same event, unless you want either to play.

## 6. Generate three takes on the box

On the GPU box with `~/sfx-lab/` (the A6000; how it was installed: `docs/experiments/2026-10-07-sfx-models/`, Entry
7). The owner's tunnel is not needed; plain ssh with the owner's own key resolution (never a key path). `<box>` is
the box's address, from `deploy/ansible/inventories/cloud/hosts.yml` — it never goes into a document.

```bash
# Copy the prompts file and the generation script to the box
scp tools/sounds/ambience.yaml tools/sounds/gen_ambience.py ubuntu@<box>:~/sfx-lab/
```

```bash
# Three takes (seeds 1-3) of the new tags, into a new folder; about 0.5 s a take on the A6000
ssh ubuntu@<box> 'cd ~/sfx-lab/stable-audio-3 && HF_HOME=~/sfx-lab/hf HF_HUB_OFFLINE=1 .venv/bin/python ../gen_ambience.py ../ambience.yaml ~/sfx-lab/ambience/<folder> --seeds 1-3 --only <tag>,<tag>'
```

```bash
# Copy the takes back beside the others, outside git
scp -r ubuntu@<box>:~/sfx-lab/ambience/<folder> /Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/ambience/
```

- **A new folder name for each batch** (`events`, `events-retry`, `events-retry2` on 2026-10-08), never one that
  exists.
- **A retry with a new prompt keeps the tag, takes new seeds** (4-6, then 7-9) into a new folder, and keeps the old
  prompt as a comment ("was: …, seeds 1-3, dropped") — so the takes of two prompts are never confused.
- **The same prompt and seed on the same box give the same take to the ear, not to the byte** (the GPU's rounding
  differs between runs; measured 2026-10-08 on the experiment's helicopter, sirens and tapping: at most 1-11 % of the
  peak at the worst sample).

## 7. Audition

```bash
# The audition page of a batch: keep or drop each take
uv run python tools/sounds/ambience_page.py tools/sounds/ambience.yaml /Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/ambience/<folder>
```

The owner opens `<folder>/index.html` in the browser, keeps or drops each take, and pastes the page's summary back;
the ratings stay in the browser only. The kept seeds go into the entry's `keep:` list; a sound with no take kept is
dropped (a comment says so) or retried (§6).

## 8. Prepare the kept takes into the fork's library

On a branch of the fork. Needs macOS (`afconvert`, to measure) and Homebrew's `ffmpeg` (to encode); run from
`tools/sounds/`, since it imports `prepare_bed.py`'s measuring:

```bash
# A dry run: every kept take found, encoded and measured; nothing written
cd tools/sounds && uv run python prepare_ambience.py
```

```bash
# Write: the MP3s (mono, 96 kbps, brought to -20 dBFS, the peak capped at -1 dBFS), ambience.json, CREDITS.md
cd tools/sounds && uv run python prepare_ambience.py --write
```

The existing clips come out byte-identical (git shows no change); only the new MP3s, the manifest and the credits
change. A quiet take gets a large gain (the freezer alarm +18.6 dB): its background hiss rises with it — trim it by
ear with the story's `gain_db` if it shows.

## 9. Give it keywords in the story

In the fork's `stories/lab-outbreak/ambience.yaml`, section "Event sounds (cue only)", one entry per kept take, its
comment giving the kind, the length and the prompt as the manifest has them:

```yaml
  # spot · 10 s · A jet airliner flying overhead, a loud deep rumbling roar of its engines
  - file: jet-1.mp3
    enabled: true
    gain_db: 0
    keywords: [jet, a plane]
    cue_only: true
```

Several takes of one sound share the keywords (a cue picks one of them). Then check, in the fork's clone:

```bash
# The tests: every clip the story enables is on disk, in the manifest with a kind, CC0, credited
.venv/bin/python -m pytest -p no:warnings tests/test_show_ambience.py tests/test_show_cues.py
```

## 10. Hear it

Waiting for a cue is a lottery (about 4 cues in a 27-event show). Rig one instead (the owner's idea, 2026-10-07: "We
have seed, so we know what the lines will be"): with `seed: 42`, every run reads the same events in the same rounds —
round 2 is always "Footsteps cross the floor above, where the roof access was welded shut." In the fork's clone:

1. Add a test keyword unique to a known event to the clip you want to hear (`footsteps` on it, for round 2).
2. In the clone's `settings.yaml`, under `show:`: `event_every: 1`, `event_jitter: 0` (an event every free round),
   `debug: true` (the console says `Show: ambience cue, spot: <file>`; the debug line under the round, `cue <file>`).
3. Start the app, reload the page, press Start; the app's log says `round 2: the event cues <file> (spot)`, and the
   page then fetches that file.
4. **Unrig:** `git checkout -- stories/lab-outbreak/ambience.yaml`, the three settings removed.

## 11. Release

As any change to the shipped sounds: the fork's PR merged, a `tz-<n>` tag, the installer pinned to it, the owner's
re-proof (`make client-mac` twice). The library grows about 0.8 MB for every ten event takes (84 KB a take on
2026-10-08: the 42 event takes are 3.5 MB).
