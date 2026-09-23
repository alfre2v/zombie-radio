# Zombie-Radio

Interactive audio-only theater play performed by 4 AI voice actors:
scientists trapped in a lab during a zombie breakout. Hard deadline:
2026-10-08. The project will be presented in a talk at the Austin
Python Meetup in October 2026. "hackTNT 2026" (as in the folder name)
is the owner's internal name for projects built hackathon-style in
2026, not an event.

## When picking up cold

Scan [docs/README.md](docs/README.md) first — it is the meta-doc for
the documentation system (the project's memory of record). Then
follow its cold-start order: `docs/TODO.md` → the active arc's spec →
`docs/roadmap.md` Features Shipped → `git log --oneline -10`.

## Working agreements

- **Discussion-first**: propose the shape of each piece, get the
  owner's input, then create.
- **Review-before-commit is strict**: show the diff and wait for
  explicit review. A harness permission prompt is not review.
- **The repo is the memory of record**: facts that matter across
  sessions belong in `docs/`, never only in agent memory.
- **Git workflow**: work happens on branches (usually feature
  branches) with PRs; every PR is reviewed, approved, and merged by
  the owner. Direct commits to main were allowed only for the initial
  repo-structure setup (2026-09-12).
- **No Claude/AI attribution lines** in commit messages or PR
  descriptions — no "Co-Authored-By: Claude", no "Generated with"
  footers, anywhere, ever (owner rule, 2026-09-14).
