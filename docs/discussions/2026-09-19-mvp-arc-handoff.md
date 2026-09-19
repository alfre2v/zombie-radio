# Mid-session handoff — MVP-prototype arc, day 3

> **EPHEMERAL HANDOFF** — compaction-survival dump created
> 2026-09-19 (~74% context), mid-arc. Per convention: delete at
> session close **with the owner's sign-off** once its content
> lives in the real docs. The agent must ASK for deletion
> permission when the session's work concludes. A lingering
> handoff WILL be read as current state — do not let it linger.

## Where we are (30 seconds)

**MVP-prototype arc** (opened 2026-09-17), branch
`alfre2v/mvp-prototype-arc-open`, everything committed through
`173fdcd`, working tree CLEAN. **PR #4 is OPEN**
(https://github.com/alfre2v/zombie-radio/pull/4 — "deployment
machinery built and proven live, Tasks 1–3") awaiting the owner's
review/merge. **Tasks 1, 2, 3: DONE** — the Ansible deployment
machinery is built and proven live on a fresh A6000 (from-zero
converge, idempotent changed=0, reboot auto-rise <1 min), the
client loop works, the config baseline is set, and **D2's
acceptance was met** (4-persona voice session + mic on the
deployed stack). The infrastructure risk is retired at half its
timebox. Deadline: **2026-10-08**, ~19 days out.

**The live box:** A6000 at 185.216.22.236 (CANADA-1, $0.50/hr)
may still be ALIVE — the owner said "destroying soon." If it
still runs, gently remind (meter). `hosts.yml` is restored to its
committed sentinel state; when working with a live box the IP is
pasted locally and NEVER committed (see hook, below).

## Execution order AFTER the PR merges (agreed)

1. **Task 7b — `client-talkwithme-mac.yml`** (NEXT; shape round
   FIRST — discussion-first always). Standalone top-level
   playbook installing the TalkWithMe CLIENT on the Mac laptop.
   Hard constraints (all owner-ratified): inventory-FREE (no
   `-i`, `hosts: localhost` inline, must never read the deploy
   inventories — EW `lab.yml` precedent) · **upstream-vanilla**
   (plain `python3 -m venv` + `pip install -r requirements.txt`,
   NO uv imposed — deliberate exception to our uv tooling,
   reason recorded) · **create-if-absent** (never clobber
   settings.yaml or Personas/) · in-play vars `client_repo` /
   `client_version` / clone-dir (default upstream; fork later =
   one var flip; upstream+fork clones can coexist) · the
   placeholder-voice factory automated (`say`/`afconvert` blocks
   from the experiment's `placeholder-personas.md`) · no
   supervisor (uvicorn by hand at showtime). **Upstream OUTREACH
   IS DEFERRED past the deadline** — build offerable, contact
   nobody ([discussion 2026-09-19] upstream-contribution-strategy
   §6).
2. **Task 6 — the thin fork + first patches** (trigger FIRED:
   `[Name]:` labels are back in show output and SPOKEN by TTS).
   Seed notes in the arc-plan doc's Task-notes section:
   server-side sanitizer is PRESUMPTIVE (also cleans the
   transcript that feeds context — a C3 win) vs client-side in
   tts.js; the max-chars accumulator replaces the per-sentence
   split in `static/tts.js` (N a settings knob; test items:
   "Dr. Byrne. 47. Microbiology. Over." as ONE request, and the
   lone-"1." echo case). Separable, upstreamable commits.
3. **Task 4 (owner, parallel, the long pole):** character bibles
   (unblocks 5a) · voice samples — find the voice-isolation tool
   scorbo2 mentioned on his podcast FIRST (Demucs/UVR-family are
   the survey candidates; follow-ups entry), gitignore before the
   first file (never-commit rule).
4. **Task 5 — experiments (D3):** 5c narrative-health probe
   battery (zero-code, placeholder cast suffices, next box) ·
   5a LLM audition (gated on bibles; ranked five; both
   narrative-health axes) · 5b TTS comparison + VRAM budget
   (gated on samples; LuxTTS ~1 GB claim first check).
5. Task 7 (canned episode MUST + demo-day runbook), Task 8
   (close ritual: Features Shipped, task_history, TODO reset,
   staleness sweep, plan-doc closing entry, ASK TO DELETE THIS
   HANDOFF).

## Fresh science (2026-09-18 evening, all documented but easy to miss)

- **C9 CONVICTED:** owner raised `max_turns_for_context` 6→50;
  keyword recall now WORKS ("Arrow" test) — the memory signature
  feature is within reach; the model is exonerated on recall,
  still suspect on dialogue quality ("characters still very
  dumb" → the audition's mandate).
- **D1 sampler audit:** persona requests send ONLY max_tokens
  (live 200, settings.yaml wins over config.py's 1024) +
  temperature (live 0.8); everything else = llama-server
  defaults → **temperature is the only no-fork sampling knob**.
  The persona "router" (Settings: "LLM decides") picks only the
  FIRST speaker per round via `chat_completion` at temp 0.1 /
  16 tokens (`app/services/llm.py:121-135`,
  `app/routers/chat.py:98-124`); followers are `random.choice`
  (chat.py:254-261 = taxonomy E1).
- **New specimens:** cross-persona label WEARING (Ralph replying
  under `[Daniel]:`, Daniel under doubled `[Moira]: [Moira]:`) —
  identity bleed; and clean C8 (the meta-request "remember the
  code word" absorbed as an in-fiction event: "The lab is
  destroyed. Over.").
- **Deployment potholes fixed in-role** (journal has the full
  story): torch AND torchaudio pinned together `2.9.1+cu128`
  from the cu128 index (PyPI defaults are cu130 and crash-loop on
  the R570 driver) · tts-serve tags have NO v prefix (pin "1.1")
  · llama's -hf cache = HF-style extension-less blobs (assert by
  size, not *.gguf) · local-path pip installs always report
  changed (guarded install for tts-engine-common).

## The machinery's conventions (violating these gets caught)

- **NEVER_COMMIT hook** (`.githooks/pre-commit`, armed by
  `make install`): a marked line commits only while `REPLACE_ME`
  precedes the marker on the same line; excludes `*.md` and the
  hook itself; scans the INDEX only. Routine while a box lives:
  `git add -A && git restore --staged
  deploy/ansible/inventories/cloud/hosts.yml`. The hook has TWO
  production catches, both against the agent.
- Make targets: `ans-deploy ENV=cloud|local`, `ans-check-syntax`,
  `ans-lint` (clean at `production` profile — keep it so),
  `check` (through tunnel), `ssh-tunnel` (reads IP from
  inventory), `install`, `ans-deps`, `ans-config`. Deploy runs
  log to `~/.config/zombie-radio/logs/`.
- Ansible doctrine (shape doc §1–§13): environments-not-groups
  inventories with 00-common symlink + 99-env overrides ·
  service-shaped groups + SELF-GATING roles
  (`<role>_enabled: "{{ '<role>' in group_names }}"`) —
  conditional gating chosen over per-play binding
  (concern-vs-topology, §12) · role-variable indirection (tasks
  speak `<role>_*` only; defaults map to `zr_*` = the dependency
  manifest) · privilege doctrine §13 (play-level `become: true`
  stays; roles assume root; `become_user` marks exceptions) · NO
  tags · block YAML only · minimal comments in code (doctrine
  lives in docs).
- The plan doc (`2026-09-18-mvp-prototype-arc-plan.md`) is the
  TODO's extended notepad across BEFORE/DURING/AFTER phases
  (owner convention) — Task-notes sections + dated journal
  entries. TODO stays terse state.

## Collaboration reminders (owner: Alfredo — he TESTS the agent)

Strict review-before-commit (he explicitly authorized
permission-prompt-as-review for THIS handoff commit only, same as
last time). NO AI attribution in commits/PRs, ever. Never open
desktop side panes. Minimal code comments unless asked. He sets
deliberate traps to verify discipline (the "Ah, got you!" hook
test; the "you should push back because…?" quiz whose answer was
his own review rule) — expect it, welcome it. He wants hard
pushback WITH receipts (file:line), ranked lists over single
picks, integrated outcomes over chronicles, and re-orientation
(origin + concepts + connections) when a topic resurfaces —
never assume he holds the context. Recent agent misses he called
out (avoid repeats): sloppy "TalkWithMe on the box" phrasing
(the client NEVER runs on a server — spec §3.1), presenting
play-binding as the ONLY group→role mechanism, flattening his
IP-commit ruling. When answering "is X done?", check the actual
item list, not the vibe.

## Cold-start reading order

1. This handoff.
2. `docs/TODO.md` — the parking-lot table (live state).
3. `docs/discussions/2026-09-18-mvp-prototype-arc-plan.md` —
   plan + Task-notes + journal (the arc's depth).
4. `docs/discussions/2026-09-17-ansible-deployment-shape.md` —
   the machinery's doctrine (§9 preflights, §11 amendments,
   §12 binding mechanisms, §13 privilege).
5. `docs/discussions/2026-09-19-upstream-contribution-strategy.md`
   — why 7b precedes the fork; outreach deferred.
6. `docs/specs/product-definition.md` §3, §6, §10 (ledger
   entries) · runbooks (`service-restart-sequence.md`,
   `box-inspection.md`) · taxonomy
   (`2026-09-16-storytelling-coherence-and-structure-adherence.md`)
   for the science.

## Paste-ready re-orientation prompt

```
We are mid-session on the Zombie-Radio project (MVP-prototype
arc), resuming after a manual context compaction. Re-orient now:

1. Read docs/discussions/2026-09-19-mvp-arc-handoff.md in full —
   the compaction-survival handoff you wrote minutes before
   compaction: state, execution order, fresh science, machinery
   conventions, collaboration rules.
2. Follow its cold-start reading order (TODO, the arc-plan doc,
   the shape doc as needed).
3. Then confirm to me in a few sentences: where the arc stands,
   what executes next after PR #4 merges, and the constraints on
   the client-talkwithme-mac.yml playbook.

Do not start new work until you've confirmed. My rules stand:
strict review-before-commit, no AI attribution anywhere, no side
panes, minimal code comments, pushback with receipts welcome.
```

## Postscript (fill only if reality drifts after this snapshot)

*(empty)*
