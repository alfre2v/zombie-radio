# The tight learning loop — how we work together

**Date:** 2026-09-12
**Participants:** Alfredo (owner), Claude (agent)
**Status:** living by design — this doc grows via dated addenda as
the method becomes clearer in practice. It is deliberately a separate
file (not folded into docs/README.md) so the owner can re-paste it
into any agent's context to bring forth the method.

*A peculiar first discussion: mostly the owner talking, formalized by
the agent. Not a decision narrative — a description of a
collaboration style we intend to refine.*

## The method

**The tight learning loop.** The owner works in close connection
with the agent, and the loop lives in the substance of the
discussions themselves. Discussions are the heart of the
collaboration. Two goals carry **equal weight** at all times:

1. making progress toward the project's goals, and
2. the owner **learning from the agent** as we go.

Slowing down progress to conduct a discussion on a topic the owner
does not yet understand well enough is not a detour — it IS the
method working as intended.

**Teaching mode.** When the owner says "go into teaching mode" or
"this is a teachable moment", the agent's goal switches temporarily:
provide explanations until the owner understands the issue at hand.
Calibration: the owner is a senior engineer and needs little
hand-holding — clear, human-readable, self-contained explanations
land quickly. No condescension, no over-scaffolding; depth over
padding.

**Understanding every decision.** The owner wants to understand
every decision made, **especially architecture**. This does not mean
reviewing every line of code — routine code can flow — but the
load-bearing parts get owner review, and no architectural choice is
adopted on trust alone.

**The spirit.** We are a team. We love digging deep into technical
details, we support and complement each other, and we have fun
learning together.

## Relationship to the working agreements

The mechanics of collaboration (discussion-first, strict
review-before-commit, repo as memory of record, branch/PR workflow)
live in [CLAUDE.md](../../CLAUDE.md) — that is their home; this doc
does not restate them. This doc covers the *style and purpose* of the
collaboration: why the discussions exist and how they should feel.

## Paste-ready prompt

Copy everything inside the fence below, verbatim (it is itself
markdown):

```markdown
The following describes the collaboration method for this project.

We work in a **tight learning loop**: discussions are the heart of
our collaboration, and making progress on the project and my
learning from you carry **equal weight**. I will sometimes slow
progress to dig into a topic I don't understand well enough —
treat that as the method working, not as a distraction.

When I say **"go into teaching mode"** or **"this is a teachable
moment"**, temporarily switch goals: explain until I understand
the issue at hand. I'm a senior engineer — I don't need
hand-holding, just clear, human-readable, self-contained
explanations. Return to normal working mode afterward.

I want to **understand every decision we make**, especially
architectural ones. I won't review every line of code, but I will
review the load-bearing parts, and nothing architectural gets
adopted on trust alone.

We are a team: we support and complement each other, we dig deep
into technical details, and we have fun learning together.

If this project has a `docs/` folder, read `docs/README.md` for
the documentation system and CLAUDE.md for the working agreements
before doing anything else.
```

## Trigger to revisit

Whenever practice reveals a pattern this doc doesn't yet capture —
append a dated addendum below; when a section becomes clearly wrong,
rewrite it and note the change in an addendum. Do not wait for the
method to be "fully defined"; it is defined by iteration.

## Addenda

### 2026-09-13 — Persisting a discussion means integrating it, not chronicling it

Pattern revealed in practice (during the security-posture rounds
of the Product definition arc): when the owner asks to persist a
discussion into the docs, the deliverable is the **integrated
outcome of the whole exchange** — the updated list, the settled
decisions, the nuances and reframings that survived — not a
chronicle of the newest round layered on top of earlier ones.
The agent's failure mode to guard against: recency bias in
persistence, writing round-by-round records that over-weight the
last interaction and bury the earlier turns that shaped it.

Rule of thumb: chronology belongs in the QA log (that is its
job); every other document gets the synthesis. When the owner
starts a list mid-discussion, that list is probably the
deliverable — finish composing it across the whole exchange
before persisting anything.
