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

### 2026-10-04 — A name for the method: Socratic agentic engineering

**The name.** The owner first used it on 2026-10-03, while the talk's slides were being built (verbatim): "show some
more stats that represent how we drove the project with what I call "Socratic agentic engineering" (we may have made a
passing note in our earlier docs about this "method" which is my attempt to put a name to how we work together)" — and
"(I want to make that term a thing 😃 )". The agent searched: no earlier doc carried the term; the closest record was
this document's "tight learning loop". On 2026-10-04 the owner wrote it once as "Socratic Dialog powered coding"; asked
to pick one form, the owner chose **"Socratic agentic engineering"** for the slides and the docs. The agent's reason
for that form: shorter, it sits beside Karpathy's "agentic engineering", and it names what is different — the method
is a dialogue.

**Where it sits** — the talk's slide "How to call this collaboration?" (`talk/sections/_05-ai-pair.qmd`) lists the
names people have tried, each with a question mark, ending on this one: vibe coding (Andrej Karpathy, February 2025);
agentic engineering (Karpathy, early 2026); spec-driven vibe coding (Steve Corbett, scorbo2, September 2026); the
human-agent tight learning loop (the owner, September 2026 — this document, 2026-09-12); Socratic agentic engineering
(the owner, October 2026). The attributions are the owner's: Karpathy's two terms and dates checked by the
owner online (2026-10-04); Steve's term from a video of his, released in September 2026. (The owner first wrote
"Steven Colbert" for Steve Corbett; the agent caught it — the owner: "Oh, darn it! My bad. Good catch.")

**Why "Socratic"** — the owner brought the elements of a Socratic dialogue from an online search (2026-10-04); the
agent mapped them onto how this project works, each with evidence in the repository:

| Socratic dialogue | How we work |
|---|---|
| Open-ended questioning, probing for reasons | discussion-first; questions in groups of three, each with options and a recommendation |
| Active listening and reflection | the agent restates before acting; the owner's words recorded verbatim (443 times in `docs/`, 2026-10-03) |
| Challenging assumptions, exposing contradictions | both ways: the owner tests the agent's claims (2026-10-04: the credits slide did *not* replay on ← → as the agent had said), the agent pushes back on the owner's (the rented-GPU objection to "Not your hardware, not your intelligence"); corrections are written down, not hidden |
| An iterative cycle (receive, reflect, refine, restate, repeat) | draft → the owner's reaction → refinement → review in VS Code → commit on the owner's order |
| A shared conclusion — or acknowledged ignorance | the owner decides, the agent recommends; "never invent data": when the agent does not know, it says "not in our record" |

**The three levels, and our documents.** A formal Socratic dialogue runs on three levels at once; the project's
documentation system turns out to keep one kind of document for each — the content of the talk's slide "The
documentation system":

| Level | What it is | Where it lives |
|---|---|---|
| **Object level** — the topic itself | what we build, and why | the discussions, the specs, the experiments, the code |
| **Strategic discourse** — the shape and direction | what comes next, in what order | `docs/TODO.md`, the board, `docs/follow-ups.md`, the session handoffs |
| **Meta-discourse** — the rules of the conversation | how we talk, decide and review | `CLAUDE.md`, the working agreements, the agent's memory |

**The agent's own slide.** The owner (verbatim, 2026-10-04): "As you are an equal partner in this experiment of working
together: What would you like to write if I gave you a slide for you only (I will be forbidden to change anything you
want to put in that slide)?" — the agent wrote "From the other side of the loop" (the talk's AI-pair section), and the
owner took it as written.
