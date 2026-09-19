# Upstream contribution strategy — offering our deployment work to scorbo2

**Date:** 2026-09-19 · **Arc:** MVP prototype
**Type:** strategy discussion (owner proposal + agent analysis,
synthesized; the ruling it produced is executed in TODO.md —
Task 7b reordered before Task 6)
**Status:** DECIDED as to sequencing; the actual approach to
upstream stays open (§6).

*Context for the cold reader: both foundation projects —
TalkWithMe and tts-serve — are by the same single author
(scorbo2). We are about to fork TalkWithMe (Task 6; the sanitizer
trigger fired 2026-09-18) and have just built Ansible deployment
machinery for the model backend, with a Mac client-install
playbook (`client-talkwithme-mac.yml`, Task 7b) planned as a
tangential helper. The question this discussion settled: in what
order, and in what shape, so that our work stays OFFERABLE
upstream?*

## 1. The owner's proposal (2026-09-19)

Execute **Task 7b BEFORE the fork (Task 6)**, and build the
client playbook **against upstream TalkWithMe**, not against our
future fork. Motivation: the deployment machinery may be a nice
contribution to the upstream projects — "maybe scorbo2 wants to
add our `deploy` into one of these two projects. Who knows?" —
and a playbook that demonstrably installs the UPSTREAM project is
the honest, directly usable offer; one that installs our fork is
not.

The proposal came with its own key technical insight: after the
fork exists, **the same playbook serves the fork by changing only
the repository address**, held as a variable at the top of the
play (`client_repo`, plus `client_version`). The agent's
previously recorded dependency ("Task 7b depends on the fork,
since the role clones the fork") is thereby **dissolved rather
than deferred** — the playbook is fork-agnostic by construction,
upstream today, fork tomorrow, one variable apart.

## 2. The contribution framing changes the design (agent's thoughts 1 and 3, adopted)

If upstream adoption is on the table, three design choices follow
that would NOT have been forced by a purely internal helper:

1. **Upstream-vanilla tooling.** The playbook must use plain
   `python3 -m venv` + `pip install -r requirements.txt` — NOT
   our uv tooling. uv is OUR control-node choice (this repo's
   pyproject/lock); an upstream contribution must not impose a
   package manager on the subject project or its users. (The
   distinction matters because we DID adopt uv everywhere else;
   this playbook is deliberately the exception, and the reason is
   recorded here so nobody "modernizes" it into unofferable.)
2. **Polite about user state — create-if-absent semantics.** The
   playbook must never overwrite an existing `settings.yaml` or
   an existing `Personas/` tree. An installer that clobbers a
   user's configured personas or saved server settings would be
   rejected on sight by any upstream maintainer — and rightly.
   Template/seed only what is missing.
3. **The clone directory is a variable** (default something like
   `~/TalkWithMe-client`), so the upstream checkout and the
   future fork checkout can coexist side by side during the
   transition instead of fighting over one path.

These join the constraints Task 7b already carried: standalone
top-level playbook (reserved-slots pattern), run with NO `-i`,
`hosts: localhost` inline, **never aware of the deployment
inventories in any way**; no supervisor (uvicorn is launched by
hand at showtime); the placeholder-voice factory automated (the
`say`/`afconvert` blocks from the experiment's
`placeholder-personas.md`) so the synthetic cast ships with
audio; the REAL cast stays manual (never-committed samples,
private-assets-dir variable).

## 3. Calibration (agent's mild pushback, accepted)

Expectations, stated so the effort is sized honestly:

- **The client-mac playbook is a PLAUSIBLE but MODEST offer.**
  Upstream may prefer a shell script, or nothing — the manual
  install is ~4 commands, and reasonable maintainers decline
  dependencies (Ansible!) for small installers. Offer it cheaply;
  treat adoption as a bonus, never the goal.
- **The genuinely valuable contribution story is the BACKEND
  deployment** — one command from bare GPU box to the full
  llama + tts-serve + whisper stack is something the tts-serve
  README could only dream of. BUT it is coupled to our repo's
  shape: the environment-directory inventories, the `zr_*`
  variable namespace, the Makefile, the NEVER_COMMIT hook.
  Extracting an upstream-shaped version would be real work, and
  it is NOT scheduled — that story's designated vehicle is the
  **self-hosted-community write-up** (follow-ups.md), which
  showcases the machinery without requiring upstream to adopt
  anything.
- The owner's "who knows?" posture is exactly right: build the
  small thing offerable, surface it, and let interest (or
  silence) decide the next step.

## 4. The wider contribution ledger (for one-place orientation)

Everything currently pointed at upstream, across docs:

- **The two Task 6 patches** — the `[Name]:` output sanitizer
  and the max-chars TTS accumulator — designed from day one as
  separable, upstreamable commits; candidate PRs to TalkWithMe
  once proven in our fork (follow-ups: "TalkWithMe
  upstream-contribution candidates").
- **`client-talkwithme-mac.yml`** (this discussion) — the small
  installer offer, built against upstream first.
- **New tts-serve engines (F5-TTS, Breeze TTS 2)** — soft goal,
  candidate upstream PRs (follow-ups entry; LuxTTS's arrival
  weakened the Breeze case).
- **The community write-up** — not a code contribution but the
  narrative one: cloud deployment as the on-ramp for self-hosted
  AI enthusiasts (follow-ups entry with the $2.97 datum).

## 5. Consequences executed

- TODO Task 7b reordered BEFORE Task 6, its entry rewritten with
  the fork-agnostic var design and the three contribution-shaped
  constraints; the arc-plan journal carries the dated ruling.
- The fork (Task 6) now follows 7b; after it lands, the playbook
  tracks the fork via one `client_repo` flip — and keeping BOTH
  targets working costs nothing, which is itself part of the
  offer's credibility.

## 6. Open questions

- **How to approach scorbo2: DEFERRED (owner ruling, 2026-09-19,
  same day):** no outreach for now — it would distract from
  executing the fork and reaching the 2026-10-08 deadline for the
  app's own goals. The strategy stands as PREPAREDNESS, not a
  schedule: the playbook stays general (in-play `client_repo` /
  `client_version` / clone-dir vars serve upstream, our fork, or
  any future client), the fork proceeds without worry, and the
  outreach question reopens after the MVP ships — plausibly
  bundled with the Task 6 patch PRs, issue-first etiquette
  presumed.
- Whether the offer is aimed at TalkWithMe (it installs that
  client) or tts-serve (whose users need exactly this stack) —
  or simply linked from our community write-up for either to
  take. Undecided.
- Licensing/attribution mechanics if anything is adopted
  (both upstreams are MIT; our repo is public) — expected
  trivial, verify at PR time.
