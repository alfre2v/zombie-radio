# Deployment-first: the plumbing is deliverable #1

**Date:** 2026-09-17 (arc-opening discussion) · **Arc:** MVP
prototype — this decision sets the arc's first deliverable.
**Type:** working-method + scope decision (owner-proposed,
agent-endorsed with four shape rulings, all settled same day)
**Status:** DECIDED. Executed starting in the PR that carries
this document.

*Context for the cold reader: the prototype-first inversion
([discussion 2026-09-16]) said "deploy the spike's exact
configuration as a repeatable prototype." The first draft of the
arc plan read "repeatable" as "follow the Reproduction recipe by
hand each time." The owner pushed back: hand-replication does not
scale to an arc full of experiments, and deployment was never an
afterthought in this project — it is half the MVP.*

## 1. The decision

**The deployment machinery — Ansible + Docker automation that
stands up the full model-service stack — is deliverable #1 of
the MVP-prototype arc, built NOW, before the experiments.** One
playbook, two targets: the cloud GPU VM and a local GPU machine
(`delegate_to: localhost`), executing identically on both.

## 2. Why (integrated rationale)

- **It was always the plan — the draft had drifted.** ADR-0001,
  verbatim: "Owner engineering effort concentrates on the
  deployment layer (Docker + Ansible, local/cloud-GPU
  symmetric)." Spec §8 records deployment as the believed effort
  center. The arc plan had quietly demoted the project's declared
  effort-center to manual paste; the owner caught the drift.
- **Our own ops posture guarantees high redeploy frequency.**
  Never-hibernate (restore lottery) + destroy-per-evening cost
  discipline + stock-volatile flavors ⇒ every working session may
  begin with a full stack deployment. The recipe was hand-replayed
  twice during the spike at ~30–45 min each; the coming
  experiments (LLM swap-off, TTS comparison) multiply restarts.
  Manual effort doesn't amortize; a playbook does, fast.
- **Cloud/local symmetry is the project's soul made executable.**
  "Local-AI-first" ([spec §1]) becomes a testable claim when the
  same playbook provisions both targets.
- **Owner's framing, adopted: "deployment is 50% of the MVP."**
  Demo-day risk is almost entirely operational (box up, services
  up, tunnel up, under time pressure, in a venue); the playbook
  is the only rehearsal that counts.

## 3. Shape rulings (the four pushbacks, all settled 2026-09-17)

1. **Timebox and scope-guard v1.** Timebox: **3 days** (owner
   ruling — same budget the spike got; the spike finished in 2).
   Scope = exactly the spike's stack: base packages · llama.cpp
   container · tts-serve engine as a **parametrized role** (§7.2
   will swap engines — the engine is a variable, never a role
   rewrite) · whisper container. Idempotent re-runs. Two
   inventory targets. Explicitly OUT: Molecule/testing
   frameworks, galaxy-grade generality, premature vault plumbing
   (nothing on the box is secret yet; ansible-vault the day a
   secret appears, per [spec §10.4]).
2. **Single source of truth moves to the playbook.** The
   experiment's Reproduction recipe stays sealed as provenance;
   `runbooks/service-restart-sequence.md` is REWRITTEN the day
   the playbook first succeeds ("run the playbook + the few
   manual bits"). Dual-maintained deployment docs are how one
   silently rots.
3. **The code lives in THIS repo: `deploy/`** (owner ruling) —
   public, no secrets by construction; inventory/host_vars
   gitignored; keeps the memory-of-record unity. The owner's
   private Ansible project is cribbed FROM, surgically (the
   QA-log-Entry-3 trigger, now fired), never imported wholesale.
4. **The 3090/localhost tension, flagged and ruled.** The
   localhost target is BUILT now but NOT TESTED until the cloud
   deployment replicates the experiment exactly. Owner's
   reasoning: the 3090 doesn't travel to the October
   presentation, so it has zero audience visibility — "I will
   come back to the 3090, it's my baby." Known consequence: the
   day localhost testing starts, the 3090 driver check
   (deprioritized queue item) partially revives.

## 4. Sequencing (agreed)

**Playbook-first, debugged live against the fresh R570 box.**
The battle-tested recipe (R0–R13) is the playbook's source
material; the first R570 provision does double duty as the
image-validation run (the recipe has never run on the new image —
expect small deltas around CUDA and Ubuntu 24.04's Python).
Deviations amend the playbook directly, which becomes the living
deployment truth per ruling 2.

## 5. The community significance (owner note, to communicate later)

The cloud-deployment playbook is genuinely useful beyond this
project: a middle ground for the **self-hosted AI community** —
letting enthusiasts deploy and experiment with TalkWithMe +
tts-serve predictably on a rented, more capable cloud GPU
*before* committing to a local install. This motivates a future
talk/write-up on the project's motivations. Parked with a trigger
in follow-ups.md; not the moment now, but it must not be lost.
