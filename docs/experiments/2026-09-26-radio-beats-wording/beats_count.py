"""The radio beats' counts: whether each Repair, Breakdown and Switch-off says what happened to the radio, and what
it means for the listeners. Keywords over the lines, case-insensitive; dependency-free.

python3 beats_count.py LABEL [--lines]  — reads the run ids from the drives' outputs: for "old", the committed
wording's drives in ../2026-09-26-listener-memory-b-vs-a/raw (its b-new column); for any other label, this
folder's raw/drive-LABEL-<seed>.txt. --lines prints every beat round's lines, for reading.

The patterns of round 2 (runlog entry 4): the Repair's meaning counts only the lab hearing the listeners ("we can
hear you" — round 1's "hear us" took the reverse); the Breakdown's and the Switch-off's meaning is counted in its
two halves, the lab cannot hear them and the lab is still on the air; the Switch-off's "going off" also takes
"the receiver's off" and "offline". Round 1's counts, with round 1's patterns, are quoted in runlog entry 3.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEEDS = [42, 7, 2026]
HAPPENED = {
    "repair": r"\b(receiver|radio|it)('s| is)? .{0,20}\b(fixed|working|works|back|online|on|alive|up|repaired)\b",
    "breakdown": r"\b(smok\w*|spark\w*|burn\w*|fried|dead|died|fail\w*|broke\w*|gone)\b",
    "switch-off": r"\b(switch\w*|turn\w*|shut\w*|pow\w*)\b.{0,25}\b(off|down)\b|going dark|deactivat\w*"
                  r"|receiver('s| is)? (off|offline|down)\b",
}
HEARS_THEM = r"\b(we|i) (can |do )?hear you\b|\bwe're (hearing|listening to) you\b"
NOT_HEAR = r"(can'?t|cannot|can no longer|won'?t|will not|don'?t|not) hear|hear nothing|cut off from|\bblind\b|\bdeaf\b"
ON_AIR = (r"still (transmit\w*|broadcast\w*|on (the )?air)|keep (broadcasting|transmitting|sending)|broadcast\w* "
          r"(goes|will go|will keep|continues|will continue|into)|transmitter('s| is)? (still|stays|remains|active|on"
          r"|working)|on the air")
WHY = r"\b(power|battery|batteries|save|spare|fragile|later|better time)\b"
OPPOSITE = r"keep (it|the line|the receiver|the radio)? ?(on|open)\b"
MEASURES = {
    "repair": (("happened", HAPPENED["repair"]), ("hears them", HEARS_THEM)),
    "breakdown": (("happened", HAPPENED["breakdown"]), ("cannot hear", NOT_HEAR), ("on air", ON_AIR)),
    "switch-off": (("happened", HAPPENED["switch-off"]), ("cannot hear", NOT_HEAR), ("on air", ON_AIR),
                   ("why", WHY), ("the opposite", OPPOSITE)),
}


def records(label):
    raw = HERE.parent / "2026-09-26-listener-memory-b-vs-a" / "raw" if label == "old" else HERE / "raw"
    name = "b-new" if label == "old" else label
    for seed in SEEDS:
        text = (raw / f"drive-{name}-{seed}.txt").read_text()
        run_id = re.search(r"record: runs/(\S+)/script.json", text).group(1)
        yield seed, json.loads((raw / "runs" / run_id / "script.json").read_text())["rounds"]


label = sys.argv[1]
tally = {kind: {"rounds": 0, **{key: 0 for key, _ in measures}} for kind, measures in MEASURES.items()}
for seed, rounds in records(label):
    for r in rounds:
        kind = r["kind"]
        if kind not in MEASURES:
            continue
        said = " ".join(line["spoken"] for line in r["lines"])
        t = tally[kind]
        t["rounds"] += 1
        marks = [key for key, pattern in MEASURES[kind] if re.search(pattern, said, re.I)]
        for key in marks:
            t[key] += 1
        if "--lines" in sys.argv:
            print(f"seed {seed} round {r['n']} {kind} ({len(r['lines'])} lines) [{', '.join(marks)}]")
            for line in r["lines"]:
                print(f"    {line['speaker']}: {line['spoken']}")
print(f"radio beats ({label}), seeds {SEEDS}:")
for kind, t in tally.items():
    print(f"  {kind}: {t['rounds']} rounds · " + " · ".join(f"{key} {t[key]}" for key, _ in MEASURES[kind]))
