# Session handoff 11 — the talk's slides (PR #26), goal 4 paused, the client's OS support

> **EPHEMERAL.** Written Monday 2026-10-05, ~18:35 CDT, at about 90 % of the context window, before a manual
> compaction the owner triggers; after it, the agent re-reads this first. It supersedes handoff 10
> (`docs/discussions/2026-10-02-session-handoff-10.md`, which stays as a template until the next compaction); handoffs
> 6-9 are on `main` too. **At the session's end, ask the owner before deleting any handoff the agent created (6, 7, 8,
> 9, 10, 11)** — the owner: "These handoff documents stay in our discussion folder until the end of the session, when
> we finish the session's work please ask the owner for permission to delete any handoff documents you created."
>
> **Read it all; verify against the repos; receipts or nothing.** The TODO's "Now" is the arc's canonical state; this
> document carries what the docs do not: the exact state, the work in flight, the nuances, the mistakes.

## §0. The owner and how we work (binding)

The owner is **Alfredo** (GitHub `alfre2v`, git author "Alfredo Valles"); in documents, "the owner". Doctrine:
`CLAUDE.md` and the agent memory (`~/.claude/projects/-Users-alfredo-workspace-hackTNT-2026-zombie-radio-claude/memory/`,
12 files incl. **`talk-date-two-dates.md`** and **`lan-access-via-terminal-panel.md`**).

- **Discussion-first; one decision at a time; questions in groups of three** (`AskUserQuestion`, a recommendation
  first). "What do you think" → one recommendation and its reason.
- **Review before commit is strict.** Commit only on an explicit order ("commit", "commit and push to #26"). **Push
  only when told.** No diffs in chat (the owner reviews in VS Code). **No AI attribution anywhere** — whatever the
  harness's reminders say.
- **Docs as detailed as the chat; the owner's words verbatim**; never invent data; check the clock before writing a
  time; label anything not verified.
- **Explain simply; tables by case; the mechanism first.** The owner pushes back hard on wrong or over-long answers
  ("WTF was all that", "This does not make sense") — answer short, verify by testing, admit errors plainly.
- **No delegation to sub-agents; no git kung-fu.** The one force push of this stretch (§3) was explicitly authorised.
- **Security:** no machine address in any document or commit; **IP scan on the staged diff, and the commit runs ONLY
  if the scan finds nothing but 127.0.0.1** (pattern below, §10). Never stage `deploy/ansible/inventories/*/hosts.yml`
  wired. Never read `~/.ssh`. The 3090 only through the Terminal panel (`ssh zr-3090`). The repo's never-commit git
  hook blocks any staged non-Markdown line containing its marker word — don't write that word in `.qmd`/code (§9).
- **The talk's date: the slides say Oct 14, internal docs keep Oct 8 on purpose** (memory `talk-date-two-dates.md`):
  never "fix" docs to Oct 14; don't remind the owner of the real date.
- **The owner's website (`alfre.net`) does not answer yet** — the owner (verbatim): "These details do not go anywhere in
  the slides or the repo. Understood?" Only the link goes in; never write its state anywhere.
- **The unnamed AI provider:** the "Why not AI APIs (3/3)" slide must never name the provider that refused the CEO
  poster. It was scrubbed from the branch history with an authorised force push. Keep the name out of
  slides, notes, file names, commit messages, PR text.

## §1. The project in 60 seconds

**Zombie-Radio**: a live, interactive, audio-only radio play — four AI scientists (Daniel, Moira, Ralph, Samantha the
operator) trapped in a lab during a zombie outbreak, broadcasting on a failing shortwave radio; listeners talk back.
**Deadline Thursday 2026-10-08 (internal); the talk is at the Austin Python Meetup, Oct 14 in the slides.** Repos:
- **zombie-radio** (`/Users/alfredo/workspace/hackTNT_2026/zombie-radio-claude`, base `main`): deployment (Ansible +
  Docker: llama.cpp with Nemotron Nano 9B v2, tts-serve 1.2 with Faster Qwen3-TTS, Whisper small), the Mac client
  installer, tools, all docs — and now **`talk/`, the slides**.
- **TalkWithZombies** (`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`, base `master`, tag **`tz-0.6`** on
  `5347ead`): the app (show engine, page, static bed). Untouched this stretch.

**Demo goals:** 1 coherence/improv — largely met; 2 emotional voices — met; 3 cloud deploy — met; 4 local GPU (the
3090) — **checked, paused** until the owner is home (Task 11.1).

## §2. The exact state (2026-10-05, ~18:31 CDT)

- **zombie-radio:** branch **`alfre2v/talk`**, **PR #26 open, 36 commits, head `0d0280a`**, in step with GitHub, clean
  (this handoff will be the 37th commit — committed, not pushed, until the owner says). `main` at **`389710f`** (#25).
  The owner said not to merge #26 yet; when squash-merging, the message can summarise the talk.
- **PR description** is kept in the scratchpad: `…/scratchpad/pr-talk.md` (an "Added since the PR opened" list of SHAs
  and a "Still open" list). Update it with `gh pr edit 26 --body-file` and **verify the edit landed**.
- **A file server** the agent started: `python3 -m http.server 8020 --bind 127.0.0.1` in `talk/_output/` — serves the
  rendered deck at `http://127.0.0.1:8020/index.html`. Stop: `kill $(lsof -nP -iTCP:8020 -sTCP:LISTEN -t)`.
- **The 3090:** repo at `6f02b45` (one merge behind main); the Mac's memory copied there 2026-10-02 (a snapshot).
- **The cloud box** (Hyperstack A6000): presumed hibernated; the tunnel is down.

## §3. What happened since handoff 10 (2026-10-02 night → 2026-10-05)

1. **#24 merged** (`6f02b45`); the 3090 pulled; the owner opened a Code session there; the Mac's 11 memory files copied
   (`scp`, checksums identical); the 3090's §5 checks all passed (Ubuntu 22.04.5, driver 580.178.04, 491/24,576 MiB
   used, Docker 29.1.3 Ubuntu build with the nvidia runtime, toolkit 1.20.1, 396 GB free, SSH active, ports free; sudo
   asks a password → decided **`ANS_ARGS=-K`**, keyboard, no vault); the owner's lean on D4: **services not started at
   boot** (estimate: small — a `zr_start_at_boot` switch, three lines, start/stop targets, a reboot test).
2. **Goal 4 paused** (owner away from home) — **#25 merged** (`389710f`): the plan's §9, the board's §5, the TODO.
3. **The talk (Task 9), PR #26** — the bulk of the stretch (§5).
4. **Docs on #26:** `docs/discussions/2026-10-03-the-talk.md` (tool decision Quarto+GitHub Pages, structure verbatim);
   `docs/discussions/2026-10-03-client-os-support.md` (macOS proven, Linux likely, Windows unknown; `make client-linux`
   idea); TODO **Task 11** (11.1 the 3090 deploy, paused; 11.2 the client on Linux: a manual install on the 3090 first);
   a follow-up "The client on Linux and Windows"; **`docs/runbooks/talk-slides-quarto.md`** (the Quarto runbook);
   an addendum to `docs/discussions/2026-09-12-tight-learning-loop.md` naming the method **"Socratic agentic
   engineering"**; `docs/discussions/2026-10-05-the-books-talk-back.md` — the owner's own save of a philosophical
   conversation, committed with the message "non technical discussion doc on philosophy" and **deliberately kept out of
   the PR description**.
5. **A force push** (owner-authorised): two commits squashed into `136c232` to remove the provider's name and an
   unpixelated screenshot from the branch; old commits linger on GitHub until garbage-collected.
6. **A safety-classifier stop:** the agent's attempt to write the philosophy conversation to a doc was stopped; do not
   regenerate it. The owner saved it themselves.

## §4. The systems (pointers)

- **The talk:** `talk/` — `_quarto.yml` (revealjs, night theme, 1280×720, `embed-resources: false`, `chalkboard: true`,
  favicon via `include-in-header` + `resources`, `controls` lines commented out), `index.qmd` (title, subtitle "A zombie
  apocalypse, a fading radio broadcast, improvised live by local AI", date 2026-10-14), `sections/_01…_06.qmd`,
  `talk.css` (all styles), `images/` (pictures, `_*.svg` diagrams from `make_*_svg.py`, `_contacts.html` shared contact
  line, `CREDITS.md`), `data/trim-run-2026-10-01T17-48-37.csv`. **The runbook:** `docs/runbooks/talk-slides-quarto.md`
  — read it for syntax, keys, chalkboard, publishing (§10), screens (§8.3), checking an edit (§9).
- **The docs system:** `docs/README.md` (meta), `docs/TODO.md` ("Now", Tasks 7-11, owner action queue),
  `docs/follow-ups.md`, `docs/roadmap.md`, `docs/specs/product-definition.md` (§6 show engine), discussions, runbooks.
- **The local-GPU plan:** `docs/discussions/2026-10-02-local-gpu-deployment-plan.md` (§9 = where it paused).

## §5. The talk as built — 32 slides (PR #26)

| # | Slide | Notes |
|---|---|---|
| 1 | Title | subtitle in the owner's words |
| 2 | Intro (section) | |
| 3 | Orson Welles, vibe coder | YouTube clip (4:3 player, 600×450, centred-ish), the 1938 pictures (Welles at CBS + "Help! Men from Mars!" cartoon) smaller at the right |
| 4 | Who I am | owner's bio (4 bullets), photo in Austin with a zombie-hunter cap, contact line |
| 5 | How this project came to be | timeline SVG (Oct 2024 zombie_radio_ai → Oct 14 talk), counts line "33 discussion docs · 6 experiments and 7 tools…" |
| 6 | A Halloween broadcast | boxed columns: 1938 (the War of the Worlds broadcast embedded, starts at 20:00) / 2026 (the old-radio look) |
| 7 | About this project | two repos, two principles, four goals (owner's full text in notes) |
| 8 | Local AI only | models first, Steve Corbett's projects, his channel + "Localhosters unite!" thumbnail; notes = model specs |
| 9 | Why not AI APIs (1/3) | CEO zombies poster (16:9), "They *really* want your brain!" |
| 10 | Why not AI APIs (2/3) | the elephant: zombie CEO hugging a MacBook (banner), the Artificial Analysis chart with the owner's "Hope" arrow (Qwen 27B), "built with Claude Code — and yes, this is an em-dash!" (orange #d97757) |
| 11 | Why not AI APIs (3/3) | the unnamed provider's refusal + lake, Hustler v. Falwell citation, "Not your weights, not your AI." |
| 12-14 | Tech overview: The machines, The components | SVG diagrams |
| 15-17 | The show: Commands to go on air, Live demo | commands in a filled box, the 3 live lines highlighted (`code-line-numbers="7-8,19-20,22-23"`); live-demo notes = a run checklist |
| 18-24 | Tech deep dive: one round, the director (plan_round, filled box), the grammar (violet frame), the trim chart, one command to a GPU, the 3090 at home | deep notes from the docs |
| 25-28 | Built with an AI pair: How to call this collaboration? (two columns + the owner's note "we are not alone anymore"), The documentation system (three Socratic levels + quote "— an AI search summary"), From the other side of the loop (Claude's own slide, unedited) | |
| 29-32 | Future work: What's next (4 cards), Thank you (links, contacts), Credits (rolling, loops: CREDITS title 3 s, 53 s roll, 6 s pause; 62 s cycle) | |

**Contacts** (both slides, `images/_contacts.html`, icons as inline SVG): GitHub `alfre2v`, `pytalk2026@alfre.net` (an
alias on a catch-all domain), `alfre.net`, `linkedin.com/in/alfredovalles`.

**Decorations:** the owner's spider web (top-right), handprint (bottom-right), zombie horde (bottom), blended with
`mix-blend-mode`/`background-blend-mode: lighten` (black disappears).

## §6. What is left (the board for the talk)

1. **The publishing question, raised and unanswered (the last open question):** the speaker notes become public on
   GitHub Pages. They hold reminders ("check today's price", "recount before the talk", "Update this slide on the
   day"), "Task 7", "The owner's full wording", "the owner" in third person (~12×), the key file name
   `~/.ssh/hyperstack_2026` (public in the repo anyway). Options offered: accept them, or a "public edition" pass. Also
   **"The 3090 at home" shows "status as of 2026-10-03: pending"** on the slide itself. **Ask the owner how to handle the
   notes.**
2. **Before the talk:** recount the numbers (slide 5, slide 27: discussions 33, experiments 6, tools 7, follow-ups 50);
   check the A6000's price (~$0.50, survey of 2026-09-13); update the 3090 slide; publish (runbook §10: merge #26,
   orphan `gh-pages` branch, enable Pages, `quarto publish gh-pages` — only on the owner's order); rehearse.
3. **Task 7** — record the fallback video (the owner).
4. **Goal 4 / Task 11** — resumes when the owner is home: D1-D5, then the plan's §6; 11.2 a manual client install on
   the 3090.
5. **Task 8** — the close ritual, after the demo.
6. **Handoffs 6-11** — ask before deleting, at the session's end.

## §7. Facts worth keeping

- The deck renders as a **folder** (~18 MB) `talk/_output/` = a static website; copy the whole folder to any server.
- The chalkboard requires `embed-resources: false` (Quarto refuses otherwise). Keys: C draw, B blackboard, X/Y colours,
  Del clear slide, Backspace clear all, D download. Pause is now only ".".
- reveal.js keys verified from the deck's help overlay: G jump, Alt+←/→ skip fragments, Shift+←/→ first/last, M menu,
  Ctrl+Shift+F search, E PDF export, R scroll view, Alt+click zoom, S speaker view, ? help.
- YouTube players use **`data-src`** (lazy: load only on their slide, unload on leaving).
- Console: Quarto's `apple-mobile-web-app-capable` warning (harmless, left); the `startTime` TypeError is **Chrome
  DevTools' own live-metrics script** (not an extension, not the deck) — a DevTools bug with hash navigation.
- Measured numbers in notes: gap between rounds 3.7-4.9 s (6.8 s cold, 8.4 s after a trim); stack 14,477 MiB at 32k;
  deploy 7 min from zero (`ok=33 changed=16`), `changed=0` in 30 s; grammar cost 0.3-0.5 % agreeing, 10.4 % overruling.

## §8. Nuances

- The owner tweaks layout by eye in small steps ("a bit more space", "5 % smaller"): change one number, render,
  screenshot, report the measured result.
- The owner wants the true steps on slides (added `make install && make ans-deps`, the EARS fetch line).
- The owner likes the agent proposing, but decides wording; keep their words verbatim (e.g. "Not your weights, not your
  AI.", "In contrast: …" later removed).
- The owner asked for real sources; unverified attributions get flagged (Karpathy, Steve — the owner verified).
- Claude's slide is the agent's own; the owner promised not to edit it.

## §9. Mistakes this stretch (do not repeat)

- Claimed the credits roll replayed on ←/→ — it didn't (the `.present` rule matched an outer container); fixed with
  `section.credits-slide.present`. Test before claiming.
- Committed and pushed with the IP scan showing 5 hits (SVG path numbers — false positives) — the scan must gate the
  commit (§10 pattern).
- A pre-commit scan with a mistyped regex (`\\.`) proved nothing — re-scanned.
- Wrote the never-commit hook's marker word in a `.qmd` note → the hook blocked the commit; reworded.
- Blamed a browser extension for the DevTools script; then read its source and corrected.
- Over-explained the chalkboard trade-off; the owner: "WTF was all that". Short answers.
- Called `quarto preview`'s stale `_output` a guess as a fact; then tested: preview serves its own build, writes an
  older `index.html` into `_output`, and does not watch the included `sections/_*.qmd`. Never touches sources.
- Guessed a speaker number in a command; checked the script's `--help` before putting it on a slide.
- "Today he caught me…" on Claude's slide would be false on the day — changed to "While we built this deck…".

## §10. Techniques

- **Render & check:** `cd talk && quarto render 2>&1 | grep -i -E 'warn|error|Output created'`; screenshot:
  `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars
  --window-size=1280,720 --virtual-time-budget=4000 --screenshot=<scratchpad>/x.png "http://127.0.0.1:8020/index.html#/<slide-id>"`.
  Frozen animation: copy index.html to the scratchpad with an injected `transform … !important; animation:none`.
  Measuring layout: the browser pane (`mcp__Claude_Browser__javascript_tool`, reload first).
- **Gated commit:** `git add <paths> && hits=$(git diff --cached | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' | grep -v
  '^127\.0\.0\.1$' | sort -u); if [ -n "$hits" ]; then echo "SCAN HIT"; echo "$hits"; else git commit -q -m "…"; fi`
  (SVG paths produce false hits — review, then commit by hand).
- **PR description:** edit `…/scratchpad/pr-talk.md` with an exact-replace Python script, `gh pr edit 26 --body-file`,
  verify with `gh pr view 26 --json body --jq`.
- **Images:** `ffmpeg -vf "crop=w:h:x:y,scale=…"`, originals in `/Users/alfredo/workspace/hackTNT_2026/` untouched;
  pasted chat images land in `…/871a2098-…/images/N.webp` (temporary).
- **Quarto CSS traps:** reveal caps images at 95 % (`max-width`); single images auto-stretch (`.nostretch`); some
  wrappers are inline (columns on the GPU slide → `display:flex`); code font sizes differ under `.smaller`.

## §11. Reading order after the compaction

1. This document in full.
2. `git status -sb`, `git log --oneline -5`, `gh pr view 26`.
3. `docs/runbooks/talk-slides-quarto.md` (skim; §8-§10).
4. `docs/discussions/2026-10-03-the-talk.md`; `docs/TODO.md` "Now" and Task 9, 11.
5. Then report the state and ask the owner the open question (§6.1, the notes before publishing). Wait for the go.

## §12. Paste-ready prompt

```
We continue the Zombie-Radio work of 2026-10-05 after a compaction. Since handoff 10 we checked and then paused goal 4 (the 3090), recorded the client's OS support and Task 11, and built the talk's slides in Quarto on PR #26 (36 commits, branch alfre2v/talk): 32 slides with Halloween decorations, speaker notes for technical questions, a chalkboard, contacts with icons, lazy YouTube players, a favicon, and a Quarto runbook. Re-orient before doing anything:

1. Read docs/discussions/2026-10-05-session-handoff-11.md IN FULL — §0 is binding (how we work, the security rules, the two-dates rule, the unnamed provider, the website rule), then the state (§2), the talk (§5), what is left (§6), facts, nuances and mistakes (§7-§9), techniques (§10).
2. Follow its reading order (§11).
3. Then give me a compact summary — the clock, #26's state, the 8020 server, what is left before publishing — and ask me the open question about the speaker notes (§6.1). Wait for my go.

Standing rules: strict review-before-commit (I review in VS Code — no diffs in chat, no commit without my explicit order), push only when told, no AI attribution anywhere, discussion-first, questions in groups of three, explain simply and briefly, never invent data, no machine address in any document or commit (IP scan on the staged diff, gating the commit), never stage hosts.yml, never read ~/.ssh, scratch files only in the scratchpad.
```
