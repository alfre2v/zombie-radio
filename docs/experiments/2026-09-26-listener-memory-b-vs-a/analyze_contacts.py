"""The driver test's numbers, and a transcript of each seed's scripted contacts.

python3 analyze_contacts.py LABEL  — reads raw/drive-LABEL-<seed>.txt for the run ids, then raw/runs/<id>/script.json;
prints the numbers and writes transcript-LABEL.md. Dependency-free.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
LABEL = sys.argv[1]
SEEDS = [42, 7, 2026]
FACTS = re.compile(r"Alfredo|Austin|truck|pickup", re.I)
RECEIVER = re.compile(r"receiver|transmit|can't hear|cannot hear|can not hear|only send|listen", re.I)


def run_of(seed):
    text = (RAW / f"drive-{LABEL}-{seed}.txt").read_text()
    run_id = re.search(r"record: runs/(\S+)/script.json", text).group(1)
    return run_id, json.loads((RAW / "runs" / run_id / "script.json").read_text())["rounds"]


def contacts(rounds):
    """Each contact: the rounds from a Repair to the next Breakdown or Switch-off, inclusive."""
    found, current = [], None
    for r in rounds:
        if r["kind"] == "repair":
            current = [r]
            found.append(current)
        elif current is not None:
            current.append(r)
            if r["kind"] in ("breakdown", "switch-off"):
                current = None
    return found


def said(r):
    return " ".join(line["spoken"] for line in r["lines"])


def text_of(r):
    return "\n".join(f"    {line['speaker']} ({line['mood']}): {line['spoken']}" for line in r["lines"])


def who(cs, words):
    return next((c for c in cs if any(r.get("listener") == words for r in c)), None)


tally = {k: [0, 0] for k in ("alfredo named after he gave it", "maria named", "alfredo named on his return",
                             "the return recalls Alfredo, Austin or the truck", "exchanges ending on a question",
                             "sign-on tells the receiver facts", "orientation repeats tell them",
                             "the anonymous 'Hello again, lab.' asked, not guessed")}
mechanics, markdown, out = [], 0, [f"# Driver test ({LABEL}) — scripted conversations, seeds {SEEDS}\n"]
for seed in SEEDS:
    run_id, rounds = run_of(seed)
    cs = contacts(rounds)
    out.append(f"\n## Seed {seed} — run {run_id}\n")
    sign_on = rounds[0]
    out.append(f"**Sign-on** (round 1):\n{text_of(sign_on)}\n")
    tally["sign-on tells the receiver facts"][0] += bool(RECEIVER.search(said(sign_on)))
    tally["sign-on tells the receiver facts"][1] += 1
    for r in rounds[1:]:
        if r["kind"] == "orientation":
            tally["orientation repeats tell them"][0] += bool(RECEIVER.search(said(r)))
            tally["orientation repeats tell them"][1] += 1
    markdown += sum("*" in line["spoken"] for r in rounds for line in r["lines"])
    c1, c2 = who(cs, "My name is Alfredo."), who(cs, "This is Maria, from Dallas.")
    c3 = who(cs, "Hello again, lab.")
    for c, label in ((c1, "Contact 1 — Alfredo"), (c2, "Contact 2 — Maria"), (c3, "Contact 3 — Alfredo returns")):
        if c is None:
            out.append(f"\n**{label}**: not reached\n")
            continue
        out.append(f"\n**{label}** (rounds {c[0]['n']}-{c[-1]['n']}):\n")
        for r in c:
            heard = f' — heard: "{r["listener"]}"' if r.get("listener") else (" — heard: silence" if r["kind"] in (
                "re-call", "switch-off") else "")
            extra = f" · asks: {r['agenda'][:60]}…" if r.get("agenda") else ""
            out.append(f"- round {r['n']} **{r['kind']}** ({r.get('overtone')}){heard}{extra}\n{text_of(r)}")
        after = next((r for r in rounds if r["n"] == c[-1]["n"] + 1), None)
        if after is not None and after.get("slot") == "aftermath":
            out.append(f"- round {after['n']} **aftermath** ({after.get('overtone')})\n{text_of(after)}")
        for r in c:
            if r["kind"] == "exchange":
                tally["exchanges ending on a question"][0] += "?" in r["lines"][-1]["spoken"] if r["lines"] else 0
                tally["exchanges ending on a question"][1] += 1
    if c1:
        after_name = [r for r in c1 if r.get("listener") and r["n"] >= next(
            x["n"] for x in c1 if x.get("listener") == "My name is Alfredo.")]
        tally["alfredo named after he gave it"][0] += sum("Alfredo" in said(r) for r in after_name)
        tally["alfredo named after he gave it"][1] += len(after_name)
    if c2:
        answered = [r for r in c2 if r.get("listener")]
        tally["maria named"][0] += sum("Maria" in said(r) for r in answered)
        tally["maria named"][1] += len(answered)
    if c3:
        spoken = [r for r in c3 if r["kind"] != "repair"]
        tally["alfredo named on his return"][0] += sum("Alfredo" in said(r) for r in spoken)
        tally["alfredo named on his return"][1] += len(spoken)
        first = next(r for r in c3 if r.get("listener") == "Hello again, lab.")
        tally["the return recalls Alfredo, Austin or the truck"][0] += bool(FACTS.search(said(first)))
        tally["the return recalls Alfredo, Austin or the truck"][1] += 1
        tally["the anonymous 'Hello again, lab.' asked, not guessed"][0] += not re.search(r"Alfredo|Maria",
                                                                                           said(first))
        tally["the anonymous 'Hello again, lab.' asked, not guessed"][1] += 1
    quiet = [c for c in cs if not any(r.get("listener") for r in c)]
    mechanics.append(f"seed {seed}: {len(cs)} calls; the unanswered ones: "
                     + ("; ".join(" → ".join(r["kind"] for r in c) for c in quiet) or "none")
                     + f"; events inside a contact: {sum(1 for c in cs for r in c if r.get('event'))}")

print(f"driver test ({LABEL}), seeds {SEEDS}:")
for name, (hit, of) in tally.items():
    print(f"  {name}: {hit} of {of}")
print(f"  lines with markdown emphasis: {markdown}")
for line in mechanics:
    print("  " + line)
(HERE / f"transcript-{LABEL}.md").write_text("\n".join(out) + "\n")
print(f"transcript: transcript-{LABEL}.md")
