# The board before the demo — what is left, who does it, and what was deferred

**Date:** 2026-10-02 · **Arc:** MVP prototype · **Branch:**
`alfre2v/todo-2026-10-02`
**Type:** discussion — a snapshot of the work left before the demo (Thursday
2026-10-08, the talk at the Austin Python Meetup), item by item, with the
owner's rulings of 2026-10-02; persisted for visibility at the owner's ask.
**Status:** OPEN — the snapshot of 2026-10-02, evening. The TODO
(`docs/TODO.md`, "Now" and "Open tasks") stays the canonical state; as items
close, dated addenda here record them. **Trigger to revisit:** each item done,
or a ruling changed; at the latest on demo day.

## §1. Why this document

The owner, 2026-10-02 (verbatim), after the board was shown as a table in the
chat: "I think this table should be persisted for visibility as a new
discussion document: `{date}-board-before-demo.md` (feel free to propose a
better name)." — the agent kept the owner's name.

Where the arc stands (the TODO's "Now"): the demo's four goals — 1. story
coherence and improvisation, **largely met**; 2. emotional voices, **met**;
3. automated deployment to a cloud GPU, **met**; 4. automated deployment to a
local GPU (the 3090), **built, never run**. The latest release: the fork's
**`tz-0.6`** (the static bed), installed and re-proven by the owner on
2026-10-02.

## §2. The board (2026-10-02, evening; six days to the deadline)

"Needs the box" — whether the item needs the A6000 up and the tunnel open:
the static plays only while a show runs (a failed round pauses it), and the
video records a live show. **The owner keeps the box hibernated until demo
day (item 7), so the items that need it are done before the box is
hibernated, or need another wake.**

| # | Item | What it is | Why it matters | State | The next step | Who | Needs the box |
|---|---|---|---|---|---|---|---|
| 1 | **Task 10.1 — the narrower-filter test** | the static heard through bands narrower than today's 300-3,000 Hz: A 300-2,700 Hz (a ham's SSB voice filter), **B 400-2,000 Hz** (a narrow receiver) first, C 500-1,500 Hz (poor reception), D 600-1,000 Hz (the extreme) | static tires the ear; a narrower band may tire it less and sound more like an old radio with poor reception (the ear is most sensitive around 2-5 kHz) | open; the recipes in the fork's `docs/runbooks/show-settings.md` ("The AM filter") | a band under `show:` in the client's `settings.yaml` (`bed_filter: true`, `bed_filter_low_hz`, `bed_filter_high_hz`), a restart of the app, a show, the F key to compare; a narrower band sounds quieter (raise `bed_volume_*` a little for a fair test). For the demo the client's local setting is enough; making it the app's default would be a small code change and a new tag | the owner (by ear, about half an hour); the agent, if it becomes the default | **yes** |
| 2 | **Task 7 — the canned episode** (the owner's MUST, 2026-09-16) | **a video of the app working, the owner explaining some of its functionality** (the owner, 2026-10-02: "Yes, recording a video of the app working, while I explain some of the functionality is enough...Let's keep it simple."); and the demo-day runbook | the fallback if the live show fails at the venue — the network, the tunnel, the box: the video is shown instead | open; its form recorded in the TODO (#24) | `seed: 42` under `show:` so a retake replays the same story; a few takes in a look, the best kept; **check that the screen recording captures the browser's sound** (macOS's own may need a tool); the static's credits line in the description if published. The agent can draft the demo-day runbook | the owner (the video); the agent (the runbook's draft) | **yes** |
| 3 | **Task 9 — the talk** | the slides and the script for the Austin Python Meetup | the deliverable itself | open | the owner's content; what to highlight is listed (demo-goals §1, §3, §6 — the director, the grammar, the debug files; the same seed replaying the same show; the looks; built with an AI pair and a memory that survives; what it costs) — now with the static bed. **The last slide carries the static's credits line** (a link to the fork's `Sounds/bed/CREDITS.md`: CC BY's "Share" includes public performance). The agent helps with material, figures and checks | the owner, with the agent | no (yes for any live material) |
| 4 | **Goal 4 — the 3090** (deployment to a local GPU) | the same stack (llama.cpp, the voice, Whisper) deployed by the playbook to the owner's home 3090 instead of the cloud | one of the demo's **four goals**; "built, never run" today | blocked on its first step | **first, the owner checks the 3090's NVIDIA driver** (owner action queue, item 3); then `make ans-deploy ENV=local`, proven from zero and a second run at `changed=0`; how the laptop reaches it (LAN or a tunnel) to decide. The stack measured 14.5 GB on the A6000; the 3090 has 24 GB | the owner (the driver check); then the owner and the agent | no (the 3090 is the box) |
| 5 | **The voices over a slow uplink** (re-examine — the follow-up "Compressed reference clips, switchable on and off") | each voice request sends the character's reference clip, a WAV of 0.6-0.75 MB, over the venue's network | on a crowded venue's Wi-Fi it could add a second or more to every line | to re-examine before demo day | learn the venue's network (or test a phone hotspot); if slow, build the switch that sends compressed clips (6-12 times smaller). The static's clips do not matter here: the laptop serves them | the owner (the venue's facts); the agent (the switch, if needed) | to test it, yes |
| 6 | **The owner's decision: demo-day logistics** (owner action queue, item 4) | the venue's network and a hotspot fallback, the laptop and its sound, the fallback order (live, then the video) | the show runs on a live box over a tunnel | due | the owner decides; the agent turns it into the demo-day runbook (Task 7) | the owner | — |
| 7 | **The owner's decision: the Hyperstack box** (owner action queue, item 5) — **decided 2026-10-02** | the A6000 kept hibernated, woken on demo day | demo day needs a box at 32k up and reachable | **decided** (below) | on demo day, about 4 hours before the talk: wake the box; if the wake fails — or by the owner's choice that day — a new VM, deployed from zero (about 7 minutes; the playbook deploys the 32k context by default), then `make ans-set ENV=cloud IP=…` and the tunnel | the owner | — |
| 8 | **Task 8 — the close ritual** | the arc's closing PR: the Features Shipped entry, the task history, the TODO reset, a staleness sweep, the spec check | keeps the memory of record clean for the next arc | after the demo | — | the agent | — |

**Item 7, the owner's decision (verbatim):** "I will keep the machine
hibernated until the day of the presentation... That day, say 4 hours before,
I'll start trying to awake the VM... I might create a new VM too to exercise
the deployment live, I will make that decision that same day."

What the agent noted with it, for the day: the runbook
`docs/runbooks/service-restart-sequence.md` warns "Never hibernate a show
box" — waking is a stock lottery: on 2026-09-24 Hyperstack had no A6000 to
wake on (it woke later that day). The owner's plan carries the fallback — a
new VM, deployed from zero, which also shows goal 3 (automated deployment to
a cloud GPU) live; a new VM gets a new address, so `make ans-set` and the
tunnel follow, and the installed client needs nothing else (its settings point
at the tunnel's local ports).

## §3. Deferred past the demo

Kept as follow-ups (`docs/follow-ups.md`); nothing to do before 2026-10-08.

| Item | The owner's ruling |
|---|---|
| **Names-only A** — code tells the model which earlier caller a voice is | 2026-10-02: "No, I have decided we are not going to execute "Names-only A" before the demo... Time is too tight, and I think we have already demonstrated enough technical depth in steering the model." |
| **A cast member says another's line** — Daniel saying Samantha's introduction, seen once in the live test of `tz-0.6` | 2026-10-02: "That's ok to postpone, the fix is busy work but not technically challenge." |
| **Task 5 (the in-prototype experiments) and the character bibles** | deferred 2026-10-01 |
| **Recasting Daniel and Moira; two transcript fixes** | postponed 2026-09-30: "I can live with the audio instabilities for the moment." |
| **Even out each voice chunk's level; the static bed's lists per kind of round; event sounds as a second layer** | 2026-10-02: very low priority, undecided whether worth executing — "Keeping it only to conserve as a ledger of all our ideas." |
| **A crossfade at the static bed's joins** | 2026-10-02: decided not to implement — "I do not see any value in implementing crossfade for our app." |

## §4. Closed on 2026-10-02 (for the record)

- **Task 10.2, the clips' picks** — done by the one-by-one review
  ([discussion 2026-10-01] sound-effects §8.22): "I like the ones we left. No
  need to execute this task."
- **Task 10.3, the credits** — moved into Task 9 (item 3 above).
- **The static bed** — released as `tz-0.6`, installed, re-proven, checked
  from the API and heard live: "All works well".
