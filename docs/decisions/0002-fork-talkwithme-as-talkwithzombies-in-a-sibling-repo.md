# Fork TalkWithMe as TalkWithZombies, diverging, in a sibling repository
**Date:** 2026-09-21
**Status:** accepted (owner decisions of 2026-09-21; sharpens the
"fork and own" clause of ADR-0001's Consequences — see the
annotation there)

## Context

ADR-0001 chose to build the MVP by adapting TalkWithMe and
tts-serve, mitigating their bus-factor-one upstreams "by forking
and owning rather than tracking", and named a possible upstream
contribution. The Task 6 reconnaissance brief
([discussion 2026-09-21] task6-reconnaissance-brief and its two
tour documents) then read both codebases at tag 7.1 / 1.2 and
found that the show's observed failures are consequences of HOW
TalkWithMe assembles each LLM request (one request per persona;
other personas' lines rewritten into `[Name]:` user turns —
`app/session.py:156-161`) and of its chat-shaped turn model (one
user message → up to four replies → stop; no server-initiated
channel to the browser). Fixing those means changing the turn
engine and the prompt structure — not patching around them. Two
facts constrained the choice of how to hold the fork:

- Both upstream projects are MIT-licensed (© 2026 Steve Corbett):
  renaming, diverging, and keeping the attribution is exactly what
  the license permits.
- The deployment machinery already treats the client as three
  variables — repository, tag, directory
  (`deploy/ansible/client-talkwithme-mac.yml:16-18`, built
  fork-agnostic on 2026-09-19) — and pins tts-serve by tag
  (`zr_tts_serve_version`).

The owner ruled on 2026-09-21: "we do not have to concern
ourselves much about staying close to upstream"; the clone becomes
a new app, TalkWithZombies; the only plausible app-code
contribution is the sentence accumulator; the deployment machinery
is the real offer to scorbo2. The same day he chose how the fork
relates to this repository.

## Decision

1. **Fork, do not copy.** TalkWithZombies is a real GitHub fork of
   scorbo2/TalkWithMe taken at tag 7.1, renamed, with the MIT
   attribution kept and the "forked from" provenance labeled
   prominently in its README. The owner: "I will always pay
   respect and attribution to upstream, we stay clearly a fork,
   and prominently label that fact in our README."
2. **Diverge freely.** No upstream-compatibility pretence: the
   turn-taking and the per-turn prompt structure change
   (ADR-0003). Upstream merges are not planned; small commits off
   7.1 keep a rebase possible but nothing is designed around it.
3. **Two sibling repositories.** `zombie-radio` stays the
   deployment and documentation repository — the memory of
   record; TalkWithZombies lives beside the other sibling clones
   (`/Users/alfredo/workspace/hackTNT_2026/TalkWithZombies`) with
   its own tests, its own `AGENTS.md`, and its own release tags.
   The glue: the installer's three client variables point at the
   fork; the deployment repo records the fork tag it was proven
   against (the tts-serve pin pattern); a docs pointer section
   says where each kind of document lives — design, decisions,
   experiments here; the app's feature docs and agent guide there.
4. **Contribution ledger re-ranked** ([discussion 2026-09-19]
   upstream-contribution-strategy §7): the Ansible deployment
   machinery first (what scorbo2 may adopt or advertise); the
   sentence accumulator as the one plausible app-code patch; the
   label sanitizer dropped. Outreach stays deferred past the
   2026-10-08 deadline.
5. **Upstream's per-persona features we do not use** (persona
   memories, tool calls) are disabled in the fork, not deleted,
   until the timebox is over.

Rejected: a git submodule inside this repo (a nested detached
checkout and a second place recording the version, buying nothing
at deploy time since the installer clones from GitHub anyway); a
subtree merge (the app inside a docs/deployment repo, our hooks
and lint over its files, subtree splits to push anything back); a
fresh repository with copied files (no provenance — ruled out by
the attribution commitment).

## Consequences

**What it costs:**

- Upstream's future fixes (TalkWithMe shipped eight releases,
  1.0 → 7.1, and issue numbers past 120 in weeks) stop arriving
  for free once the engine diverges.
- Two repositories to review, commit, and tag; two PR flows —
  already the practice with tts-serve.
- The accumulator, if ever offered upstream, is a manual port from
  a divergent tree rather than a cherry-pick.

**What it buys:**

- Freedom to rebuild the turn engine and the prompt (ADR-0003)
  without contorting around chat-app assumptions or a sanitizer
  layer.
- Provenance and attribution preserved at zero cost; the
  accumulator remains offerable from a branch sharing history.
- A clean separation of concerns: the deployment repo installs a
  pinned version of an application that owns its own quality
  gates (upstream's hermetic pytest suite and agent guide stay
  meaningful inside the fork).
- The layout the owner already works in — three sibling clones,
  absolute paths in the docs, one memory of record.

**Reversibility:** the fork mechanics are cheap to undo before
divergence (a fork is a clone with a label). Divergence itself is
the point and is not meant to be reversed; re-converging with
upstream would be a new decision. The repository layout is
reversible at any time by moving a clone — the pin and the
installer variables are the only coupling.
