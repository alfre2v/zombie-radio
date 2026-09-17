# TODO — between arcs

**State:** the **Product definition arc CLOSED 2026-09-17**
(PR #3; full engineering log migrated to
[task_history.md](task_history.md)). The next arc, **MVP
prototype**, is named and scoped in the [roadmap](roadmap.md)
build order but not yet opened — it opens with its own branch and
a fresh arc TODO here.

**Notation recap** (full conventions in [docs/README.md](README.md)):
`[ ]` open · `[x]` done (with commit SHA in parentheses) · `[~]`
re-scoped/moved to another arc (says where) · `Task N` is a
sub-step here, never a PR number · cite discussions as
`[discussion YYYY-MM-DD]`, specs as `[spec §X.Y]`.

*This file is the living parking-lot table of the task landscape
(owner convention, 2026-09-16): updated at every execution or
decision; the re-orientation surface when revisiting any topic.*

## Owner action queue

*Actions only the owner can take, so they never get lost in chat
scrollback. Items get DELETED when done; the agent keeps this
current. These carry across arcs.*

1. **Gather 4 reference voice samples** — EXECUTING SOON (owner,
   2026-09-16). Likely famous-actor movie clips for comedy value
   → **NEVER committed to the repo** (curated and used locally;
   gitignore rule + voice-isolation-tool search in
   follow-ups.md). Unblocks the in-prototype TTS comparison.
2. **Seed the character bibles** — EXECUTING SOON (owner,
   2026-09-16). Names, personalities, quirks, voice descriptions
   for the four scientists; rough is fine. Model-neutral (safe
   under inversion guardrail 2); unblocks the in-prototype LLM
   audition.
3. **Check the home 3090 box's NVIDIA driver** — DEPRIORITIZED
   (owner ruling 2026-09-16): the demo is cloud-only; revisit
   only if local development on the 3090 resumes.
4. **Demo-day logistics radar** — POSTPONED until a working MVP
   exists (owner ruling 2026-09-16). Pre-decided piece: the
   **"canned episode" emergency mode is a MUST**, recorded from
   the prototype once it works.

## Next arc: MVP prototype (not yet opened)

Scope lives in the [roadmap](roadmap.md) (build order, arc 2);
the governing decision is the **prototype-first inversion**
([discussion 2026-09-16]): deploy the spike's exact validated
configuration (experiment recipe R0–R13 +
`runbooks/service-restart-sequence.md` + TalkWithMe local +
4 personas) as a repeatable prototype, then experiment IN it.
Opening material waiting:

- **In-prototype experiments** (protocol skeleton per guardrail
  1): LLM audition over the ranked five ([spec §7.3]) · TTS
  comparison + VRAM budget ([spec §7.2]; LuxTTS in the pool —
  follow-ups.md) · the narrative-health zero-code probe battery
  ([discussion 2026-09-16] §5).
- **Backlog from follow-ups.md**: `[Name]:` output sanitizer
  (first fork patch candidate) · max-chars TTS accumulator ·
  raise `max_turns_for_context` from 6.
- **Deferred promotion**: the demo-day protocol runbook (written
  once the prototype is smoke-tested; [spec §6]).

## Standing cross-arc notes

- Hard deadline **2026-10-08** (hackTNT 2026): ~3 weeks out as of
  arc close; the prototype is now the critical path.
- Keep the last 2–3 branches, local and remote (owner rule,
  2026-09-16) — recent branches double as backup against GitHub
  hiccups.
