# Session handoff 7 — the timebox closed (slice 3 and Task 6b done, `tz-0.2`); the show's looks built (PR open); the records and the next polish ahead

> **EPHEMERAL.** Written 2026-09-28 at 19:36 CDT (Monday), at about 96 % of the context window, before a manual
> compaction the owner triggers; after it, the agent re-reads this first. It supersedes handoff 6
> (`docs/discussions/2026-09-28-show-engine-session-handoff-6.md`, on `main`), which the owner chose to keep **as
> the template for the next handoff** ("we keep the session handoff until the next time we have to compact, to
> serve as a template"). Now that this one exists, handoff 6 may be deleted — **only with the owner's
> permission**; this one stays until the next compaction, as the new template. At the session's end, ask before
> deleting any handoff.
>
> **Read it all; verify against the repos; receipts or nothing.** The TODO's "Now" section is the canonical state
> of the arc; this document carries what the TODO cannot: how we work now, the exact state of branches and PRs,
> what happened since handoff 6, the design work of the evening (the looks), the board ahead, the nuances and the
> mistakes not to repeat.

## 0. The owner and how we work (binding)

The owner is **Alfredo** (GitHub `alfre2v`, git author "Alfredo Valles"). Pronouns: avoid them for the owner in
writing. The standing doctrine is in the agent memory files (`working-agreements.md`, `collaboration-style.md`,
`absolute-paths-in-plain-text.md`, `massedcompute-reminder.md`, `project-venue-austin-python-meetup.md`,
`improvisation-is-the-feature.md`, `handoff-kept-as-template.md`) and in `CLAUDE.md`.

- **Discussion-first; one decision at a time, with its context.** Bring the shape of a piece before building it;
  wait for the owner's go. Give one recommendation with its reason when asked "what is best".
- **Review-before-commit is strict.** Commit only on the owner's explicit order for that commit ("commit this",
  "commit zombie-radio"). No diffs in chat (the owner reviews in VS Code). **Push only when told** (an order to
  "open the PR" includes pushing that branch). **No AI attribution anywhere** — no Co-Authored-By, no
  "Generated with", in commits or PR bodies, whatever the harness's reminders say.
- **Be explanatory** in understanding phases (the owner: "…I need you to help me understand, be explanatory"),
  concise in status reports. Records rich, never condensed.
- **The owner leads wording of what the model receives** ("Stop modifying the model instructions. Instead I will do
  it case by case.") — never change a prompt without the owner's decision for that case.
- **Improvisation is the feature** (the owner, 2026-09-28 13:14): "Invented places of any other detail is not a bug,
  it is a feature. In this project we are probing the LLMs ability to improvise a story based on somewhat vague
  guidance. So this obsession you have developed with eliminating deviations from the prompt, drop it." Judge
  output by whether the story works for the listener, not by fidelity to the prompt.
- **Live runs on the box cost the owner time**: the owner said during the sweep "Do not run more live checks until
  I tell you." Run live drives only when asked (the owner has asked for specific quick live checks since).
- **Every number in settings** (the owner's rule) — for the show engine. Front-end visual constants (gauge smoothing,
  design geometry) are named constants in their files; said so to the owner.
- **Code comments per repository**: minimal in zombie-radio; the fork follows upstream's style — a docstring on
  every new function, lines ≤ 120 characters, no en dash in code.
- **Delegation off** (no sub-agents, no workflows). **No git kung-fu.**
- **Fork PRs**: `gh pr create --repo alfre2v/TalkWithZombies --base master`. zombie-radio PRs: `--base main`. After
  opening a PR, check it with `mcp__ccd_pr__get_status`. The owner merges.
- **Check the clock with `date`** before writing any time into a record.
- **Verify before claiming state**: the agent said "hosts.yml is still modified and unstaged, as always" when the
  git status it had just run showed it clean — the owner caught it ("What is wrong with you"). Report only state
  just checked.

### 0.1 Live-box drill rules (unchanged since handoff 6, still binding)

1. The OWNER owns the SSH tunnel, the box's power and deploys; the agent reaches services only at
   `localhost:8080` (llama.cpp), `:8001` (tts-serve), `:8002` (Whisper).
2. Box inspection only as plain `ssh ubuntu@<box> '<cmd>'` with the address the owner gives in chat; never list or
   cat under the owner's SSH directory.
3. One line saying what a command does, before running it.
4. Probe before any chain of requests: `for u in localhost:8080/health localhost:8001/capabilities
   localhost:8002/docs; do printf '%s ' "$u"; curl -s -m 3 -o /dev/null -w '%{http_code}\n' "$u"; done` — anything
   but 200: stop and tell the owner.
5. **No box address in any markdown, ever.** `deploy/ansible/inventories/cloud/hosts.yml` is `NEVER_COMMIT`; it is
   **wired (modified) in the working tree right now** — never stage it; stage by explicit path.
6. Nothing changes on the box outside the playbook.
7. Temporary dev settings: the fork's gitignored `settings.yaml` equals the backup
   `<scratchpad>/settings.yaml.before-trim` (its `show:` holds only `seed: 42`); `cmp` before, append, restore with
   `cp` + `cmp` after, and say so. **The seed stays pinned at 42 for testing** (the owner, 19:30: "leave it pinned
   for testing"); the installed client `~/TalkWithZombies-client` has no seed, so the demo is random.
8. Dev server: from the fork's root, `.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8010 --reload
   --reload-dir app --reload-dir templates > <scratchpad>/<name>.log 2>&1 &`; stop with
   `kill $(lsof -nP -iTCP:8010 -sTCP:LISTEN -t)`. **It is running now** (pid 20151 at writing), with the committed
   dev settings. The owner's own listens run in Chrome (the in-app browser blocks the microphone). Static files are
   cached by the browser: after a design change, a hard reload (Cmd+Shift+R).

The scratchpad: `/private/tmp/claude-501/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18/scratchpad/`
(never `/tmp`). The session transcript:
`/Users/alfredo/.claude/projects/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/871a2098-cf4f-4cce-95b2-e628a8a51e18.jsonl`.

## 1. The project in 60 seconds

**Zombie-Radio**: an interactive, audio-only radio play — four AI scientists (Daniel, Moira, Ralph, Samantha — the
operator) trapped in a secret lab during a zombie outbreak, broadcasting on shortwave; listeners talk back with
hold-to-talk when the lab's receiver works. Hard deadline **2026-10-08**; a talk at the **Austin Python Meetup** in
October 2026 ("hackTNT 2026" is the owner's internal label). The app is **TalkWithZombies**
(`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`, `github.com/alfre2v/TalkWithZombies`), the owner's fork of
scorbo2's TalkWithMe 7.1; this repository (`zombie-radio`) holds the deployment and the docs. Models on a rented
Hyperstack A6000 ("the box"): llama.cpp (Nemotron Nano 9B v2, Q4_K_M, 16k context, build `b11096`), tts-serve 1.2
(Faster Qwen3-TTS), Whisper `small`. **The spec** is `docs/specs/product-definition.md` — rewritten today as one
linear description of the product as built (no ledger).

## 2. Exact state (2026-09-28, 19:36 CDT)

- **The fork** (`TalkWithZombies`):
  - `master` at `ca37199` (slice 3 merged, PR #4), **tagged `tz-0.2`** (annotated, pushed).
  - **`alfre2v/radio-look`** at `6800c00`, pushed, **PR open: [alfre2v/TalkWithZombies#5](https://github.com/alfre2v/TalkWithZombies/pull/5)**
    ("The show's looks: a chooser, the old radio and the ham transmitter with a live gauge; the plain page
    untouched"), mergeable, no CI. Six commits: `8624662` five mock-ups · `077f824` old-radio on a photo ·
    `23472e5` gauge + both designs + tests · `0e0e27d` old-radio keys on the side panels · `de91f49` chooser +
    root redirect + `/talkwithme` · `6800c00` transmitter padding + microphone. Working tree clean.
  - Tests on the branch: suite **1129 passed**; Node `test_persona_form.js` 17, `test_tts_settings.js` 91,
    `test_show_page.js` 35, **`test_show_gauge.js` 8** (new).
- **zombie-radio**:
  - `main` at `e506b40` (PR #13 merged: slice 3 closed).
  - **`alfre2v/mood-clips-followup`** at `8312594` — **committed, NOT pushed, no PR**: the follow-up "Mood clips",
    the TODO's Task 4 split, the polish order ("after the reference voices"), the handoff-as-template rule. This
    handoff is committed on this branch too.
  - `hosts.yml` wired (modified) — never stage.
- **Merged today**: fork PR #4 (slice 3, `ca37199`); zombie-radio PR #12 (`2841065`) and PR #13 (`e506b40`).
- **The box: up** (all three services 200 at 19:36). The installed client `~/TalkWithZombies-client` is at `tz-0.2`
  (the owner's re-proof passed); its old install is at `~/TalkWithZombies-client.tz-0.1`.

## 3. What happened since handoff 6 (12:19 → 19:36)

1. **The prompt sweep, cases 0-2** (records: `docs/discussions/2026-09-28-prompt-sweep.md` §3.4-§3.8):
   - Case 0, the system prompt: the premise gained "A listener who answers is heard as a voice on the frequency, and
     the cast talk to them directly." (the agent's) and the owner's own sentence about the scientists explaining the
     accident and asking for help; typos fixed; fork `432a378`.
   - Case 1, the sign-on: "The lab is secret: the scientists do not know its name or address, only that it stands
     near a wood and a swamp." added to the premise — **kept as flavour** after the improvisation ruling.
   - Case 2, the orientation repeat: the receiver told as dead, or as "switched off to save it" after a Switch-off;
     the story's orientation facts lost their receiver sentences; fork `1ab5d6f`.
   - The owner's ruling on improvisation (13:14) — see §0; C7 ("invented facts") marked not a defect by an addendum
     in `docs/discussions/2026-09-28-narration-quality-challenges.md`.
   - The last exchange may end on a question (the owner: "in the story they do not know the radio will fail
     next").
   - Fixed lines audited: four scenarios (event, call, Breakdown, Switch-off); none reaches the model's own turns;
     a past-tense rewording of their context tried in a seeded A/B test and **rejected** (B worse in the contact).
2. **The owner's listen** (run `2026-09-28T13-43-28`, 113 rounds): "Wow, big improvement in story coherence… All in
   all I am satisfied with where we are." — 0 of 215 model lines near-repeated → **3.4c.8 (the repeat guard)
   dropped**. Step 3.4c done.
3. **Bookkeeping** (zombie-radio `6ca5e7f` via PR #12): TODO ticks, SED §5.7 dated note, follow-up "The listener's
   exchange is one line" deleted, the 3.4c discussion's addendum (§19).
4. **The spec rewritten** as one linear description (owner: "The specification is not a log, it should read as the
   guide to build the product."); `docs/README.md` convention changed accordingly; living docs' citations remapped.
5. **3.5, the close**: PRs merged; `tz-0.2` tagged (commands shown step by step at the owner's request); installer
   pin `tz-0.1` → `tz-0.2`; the owner's re-proof ("All four checks pass, installed at tz-0.2."); PR #13 merged.
6. **Findings from the owner's listen of the installed client** (run `2026-09-28T15-31-44` in
   `~/TalkWithZombies-client/runs/`): the trim fires every 22-36 rounds (not ~50 as estimated on 2026-09-23: the
   budget is 14k, rounds average 165 tokens, exchanges 508), each trim re-reads the whole script (~5 s cold); an
   unexplained long silence at round 187 (model 0.84 s and voice ~1.3 s when replayed — cause unknown). Follow-ups
   written (§6).
7. **The polish ruled**: the dead-air static and the 1930s radio look pulled forward, **right after Task 4's reference
   voices**; prefetch and episodes post-timebox follow-ups.
8. **Task 4 split** by the owner: (1) the character bibles — deferred ("today has been all about improving the
   prompt… I want to pivot to audio"); (2) the reference voices — the owner's, next. Mood clips shaped as a
   follow-up (`ref-<mood>.wav` next to `ref.wav`).
9. **The looks** (the evening, §4): five mock-ups → the owner chose two; `old-radio` rebuilt on a real photograph;
   the gauge; the chooser; the root redirect; PR #5 opened.

## 4. The looks — as built on `alfre2v/radio-look` (PR #5)

- **URLs**: `/` → 307 to `/show`. `/show` = the chooser (`templates/show_choose.html`, `static/show/choose.css`): a
  card per design (live miniature: the design's `?mock=1` page in an iframe, 1280 × 800 scaled by 0.28125), then
  "Plain", then the link "Or visit the old TalkWithMe interface that this project is built upon" → `/talkwithme`
  (TalkWithMe's chat UI, moved from `/`, page unchanged). `/show?design=plain` (or any unknown/unsafe name) = the
  plain page, **byte-identical** (`templates/show.html` untouched; tests pin it). `/show?design=plain&mock=1` = the
  design template with no design + mock.js (the plain miniature). `/show?design=<name>` = `templates/show_design.html`
  (same element ids as `show.html` — a test pins it) + `static/show/gauge.js` + the design's `design.css`/`design.js`.
  `&mock=1` loads `static/show/designs/mock.js` (rounds 63-66 of run `2026-09-28T13-43-28`; `&mockstate=listening`).
  `&voice=off` works on any look.
- **The owner's hard rule**: the plain page stays 100 % functional and untouched ("I want to have that boring view as
  a 100% functional view I can always work with"). No existing file of `static/show/` was edited; the designs work
  from outside.
- **`gauge.js`**: wraps the page's global functions `unlockAudio` (taps the AudioContext: `createBufferSource`
  sources connecting to the destination also feed an analyser), `openMic`/`closeMic` (a MediaStreamSource on a second
  analyser, never to the speakers). Each animation frame: RMS × gain 3.5, smoothing attack 0.5 / release 0.08; the
  microphone's level while `show.state === "recording"`, else the voice's; publishes `--level`, `--level-voice`,
  `--level-mic` on the root and calls `onGaugeLevel` listeners.
- **`old-radio`** (`static/show/designs/old-radio/`): `radio.jpg` = Philips Sirius BD 400 A (1950), Wikimedia Commons,
  by "Bin im Garten", **CC BY-SA 3.0**, scaled to 2560 px (1.2 MB); `CREDITS.md` + a credit line on the page
  (`design.js`). The stage shows the photo cropped to x 110-1905, y 100-1250 of the photo at 2000 × 1350; every
  overlay is a % of the stage (formula in the CSS header). The transcript on the speaker cloth; the photo laid twice
  (the second copy clipped to the magic eye, over the transcript); `#receiver` = the magic eye's green fan
  (`--wedge` from `--level`, faint when the receiver is off); `#on-air` = the dial's amber glow; the four knobs = the
  cast (glow while speaking); title engraved on the brass strip; keys: Start/Stop/Resume + Hold to talk stacked in one
  column (design.js moves `#btn-talk` into `.control-buttons`) on the right walnut panel (left 79.2 %, bottom 24.4 %,
  width 11.6 %), Captions mirrored on the left panel (left 9.2 %, bottom 24.4 %); the state label under the set
  (pointer-events none — it once covered the Captions key).
- **`amateur-radio-transmitter`**: CSS-drawn rack; transcript on a green oscilloscope; `design.js` redraws the trace
  from the level with an afterglow; PLATE meter = `--level-voice`, SIGNAL = `--level-mic`; the panel grows with the
  window (no max width), padding 50 px all round (clears the 38 px bevelled band), the desk microphone scales
  (80-130 px). The owner: "Very well done on the amateur-radio-transmitter. Incredible."
- **`design.yaml`** per design: `title`, `about`, `order` (old-radio 1, transmitter 2) — the chooser reads them.
- **Dropped mock-ups** (`broadcast-studio`, `lab-terminal`, `field-radio`) live in the branch's history at `8624662`.
- **Photo search facts**: Commons API search with a User-Agent; licences checked; 1930s photos low-res; the 1950s
  European sets best. Downloads need the owner's permission (file, source, size, licence stated). A real photo for
  the transmitter was searched and **declined by the owner** ("one design with real photos is enough").

## 5. The board ahead

1. **zombie-radio records for the looks** (on `alfre2v/mood-clips-followup`, then push + one PR, on the owner's word):
   the TODO's "Now" (the polish ruling) and "The order after the timebox" (both name "the 1930s radio look with the
   gauge") → mark the look built (the chooser, two designs, the gauge, root → `/show`, `/talkwithme`, PR #5); the
   spec (`docs/specs/product-definition.md`: §3.1's diagram line "page /show", §3.2's "Upstream's chat UI stays" →
   now at `/talkwithme`, and §6 where the page is described) learns the chooser and the looks; a follow-up for the
   dropped mock-ups (at `8624662`); maybe the installer note (the root opens the show). Ask whether a `tz-0.3` tag + installer
   pin follow PR #5's merge (not decided).
2. **The owner merges PR #5** (fork).
3. **The dead-air static** — the other pulled-forward polish item (a looping hiss through a second AudioContext
   source from a round's request to its first sound; off while listening; for the designs? or the plain page too —
   ask; the plain page must not change without the owner's word).
4. **Task 4 part 2 — the reference voices** (the owner's, in parallel): `ref.wav` + exact `ref.txt` per character in
   `~/TalkWithZombies-client/Personas/<Name>/` (the dev clone reads the same folder via `personas_directory`);
   ~10 s clean speech; mono 24 kHz 16-bit is safest (`afconvert -f WAVE -d LEI16@24000 -c 1 in.wav ref.wav`);
   `Personas/` is gitignored; the installer skips existing persona folders.
5. **Then**: Task 4 part 1 (bibles, deferred) → 5a (LLM audition) / 5b (TTS comparison, mood clips) / 5c → **Task 7,
   the canned episode (MUST)** → Task 8, the close ritual. Show fixes before the talk: names-only A.
6. **At the session's end**: ask permission to delete handoff 6 (and, later, this one); remind about pushing the
   zombie-radio branch.

## 6. Follow-ups written today (all in `docs/follow-ups.md`)

The trim's thresholds in settings (`_TRIGGER`/`_TARGET` hard-coded, fork `app/show/script.py:143-144`) · a context
budget near the full 16k · a 32k context (the owner: "so the model does not forget past user interactions so
frequently") · a long silence between two lines of one round, not explained · episodes (post-timebox) · prefetch
(post-timebox status) · mood clips (on the unpushed branch) · an addition, "events heard on the radio while the
receiver is off", inside the follow-up "Event texts reworded as lines of dialog" (noted, not planned). The owner **declined** trimming deeper and leaner instructions.

## 7. Nuances

- The owner is visual and decisive about looks: iterate with screenshots (headless Chrome at 1280 × 800 and
  1920 × 1080), small concrete moves ("move it 20 % smaller", "mirror the captions key"); verify clickability with
  `document.elementFromPoint` — overlays have covered buttons twice.
- The owner values safety of the working path (the plain page) over cleverness; design changes must work from outside.
- The owner prefers real photographs over drawn realism ("Can you not get an actual photo…?").
- The owner likes experiments but cuts scope when a thread sprawls ("let's not get too carried away").
- Test runs replay exactly with seed 42; the demo is random.

## 8. Mistakes since handoff 6 (do not repeat)

- Claimed stale state (`hosts.yml` "modified, as always") without reading the fresh status.
- Drew "photo-real" textures that the owner found cartoonish twice before switching to a real photo — for realism,
  propose photos first.
- Overlays with full width (`left:0; right:0`) swallowed clicks (the Captions key) — size overlays to content.
- Cached static files made a browser check look broken — use a fresh load (`fetch(..., {cache:'reload'})`, a new
  headless Chrome) before concluding.
- Wrote a scratch file to `/tmp` once; a `window.open` in a browser check navigated the tab.
- Numbers first stated imprecisely (a spec section "§2" instead of "§2.2", line numbers 142-143 instead of 143-144) —
  verify against the file before writing.

## 9. Techniques

- **Screenshots**: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu
  --hide-scrollbars --window-size=1280,800 --virtual-time-budget=4000 --screenshot=<scratchpad>/x.png "<url>"`;
  send with `SendUserFile` (display render).
- **Browser pane checks**: `mcp__Claude_Browser__javascript_tool` for `elementFromPoint`, forcing `--level` to see a
  gauge move; reset the viewport with `resize_window` preset desktop.
- **Commons**: `https://commons.wikimedia.org/w/api.php` (`generator=search`, `gsrnamespace=6`, `prop=imageinfo`,
  `iiprop=url|size|extmetadata`, `iiurlwidth`), a descriptive User-Agent; contact sheets rendered from thumbnails.
- **Fork checks**: `.venv/bin/python -m pytest -p no:cacheprovider` (grep `passed`); the four Node tests; remove
  `__pycache__`; `awk 'length > 120'` on changed files; `grep -l '–'`.
- **Pre-commit scans** (zombie-radio): the wired address from `hosts.yml` and any IPv4 against the staged `+` lines;
  stage by explicit path.
- **zsh**: a variable holding several file names does not split — pass files directly or use `find -exec`.

## 10. Reading order after the compaction

1. This document, in full (§11 included).
2. `git status -sb` and `git log --oneline -8` in both repositories; `gh pr view 5 --repo alfre2v/TalkWithZombies`.
3. `docs/TODO.md` — "Now", the order after the timebox, the polish entry, Task 4.
4. `docs/follow-ups.md` — the entries of 2026-09-28 (§6 above).
5. The fork's `docs/runbooks/show-page.md` ("Choosing a look") and `static/show/designs/`.
6. Then report to the owner: the clock, the tunnel (probe first), the state of PR #5 and the unpushed zombie-radio
   branch, and ask what to do next — and wait.

## 11. Paste-ready prompt

```
We continue the Zombie-Radio work of 2026-09-28 after a compaction. The show engine's timebox is closed (slice 3 and
Task 6b done, the fork tagged tz-0.2), and this evening we built the show's looks: a chooser at /show, the old-radio
design on a real photograph and the amateur-radio-transmitter design, both with a live gauge — PR
alfre2v/TalkWithZombies#5, open. Re-orient before doing anything else:

1. Read docs/discussions/2026-09-28-show-engine-session-handoff-7.md IN FULL — §0 is binding (how we work, the
   live-box rules in §0.1, the improvisation ruling), then the exact state (§2), what happened (§3), the looks as
   built (§4), the board ahead (§5), the follow-ups (§6), the nuances and mistakes (§7-§8), the techniques (§9).
2. Follow its reading order (§10): git status and log in both repositories, PR #5, the TODO's "Now", the
   follow-ups of 2026-09-28, the fork's show-page runbook.
3. Then give me a compact summary — the clock, the tunnel (probe it first), PR #5, the unpushed zombie-radio branch
   alfre2v/mood-clips-followup — and ask what to do next. Wait for my go.

Standing rules: strict review-before-commit (I review uncommitted changes in VS Code — no diffs in chat, no commit
without my explicit order for that commit), push only when told, no AI attribution anywhere, discussion-first (one
decision at a time, with its context), never change what the model receives without my decision for that case,
improvisation is the feature, plain and explanatory language, no delegation to other agents, no git kung-fu, code
comments per repository (minimal in zombie-radio; upstream's docstring style in the fork), every number in
settings, and never stage hosts.yml.
```

## 12. The owner's words of the evening (verbatim, from the transcript)

- On the plain page: "Do not change the part that goes into today's functional show, I want to have that boring view
  as a 100% functional view I can always work with."
- On realism: "Can you not get an actual photo of a real radio and use it as a background or something instead of
  producing this more and more cartoonish textures?" · "Ah, this is more like it. Yes, commit."
- On scope: "Ok, let's not get too carried away. I think one design with real photos is enough. I actually want to
  keep your `amateur-radio-transmitter` design."
- On the chooser: "when we open the show page without any arguments, instead of directly showing the old show page,
  we are given 3 screenshots to click to redirect to the visual design to use for starting the show." · the link
  text: "Or visit the old TalkWithMe interface that this project is built upon".
- On the seed: "leave it pinned for testing."
- On this handoff: "These handoff documents stay in our discussion folder until the end of the session, when we
  finish the session's work please ask the owner for permission to delete any handoff documents you created."
