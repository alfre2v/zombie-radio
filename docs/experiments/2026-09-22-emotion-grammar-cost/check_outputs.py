"""What the model wrote in each arm of raw/probe/ (stdlib only).

Per arm: lines per round; lines carrying a legal emotion tag, a tag outside the list,
no tag, or neither shape; lines ending in "Over."; which emotions were used, how many
distinct, and the share of the most frequent one. Also: does D-simple reproduce the
text of the ADR-0003 gate's D-on (same prompt, grammar and seed)?
"""
import collections
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
PROBE = HERE / "raw" / "probe"
GATE_PROBE = HERE.parent / "2026-09-22-adr-0003-gate" / "raw" / "probe"
ORDER = ["D-simple", "D-forced", "D-aligned-off", "D-aligned", "D-aligned-live"]
EMOTIONS = {"calm", "happy", "sad", "afraid", "terrified", "doubtful", "angry", "urgent", "exhausted"}
NAMES = "Daniel|Moira|Ralph|Samantha"
TAGGED = re.compile(rf"^({NAMES}) \(([^)\n]*)\): [^\n\[\]]+$")
UNTAGGED = re.compile(rf"^({NAMES}): [^\n\[\]]+$")


def content(folder, name):
    path = folder / f"{name}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())["response"]["choices"][0]["message"]["content"] or ""


def main():
    for arm in ORDER:
        texts = [content(PROBE, f"{arm}-r{k:02d}") for k in range(1, 11)]
        if all(t is None for t in texts):
            continue
        counts, legal, other_tag, untagged, malformed, over = [], 0, 0, 0, 0, 0
        used = collections.Counter()
        for text in texts:
            lines = [line.rstrip() for line in (text or "").split("\n") if line.strip()]
            counts.append(len(lines))
            for line in lines:
                over += line.endswith("Over.")
                tagged = TAGGED.match(line)
                if tagged and tagged.group(2) in EMOTIONS:
                    legal += 1
                    used[tagged.group(2)] += 1
                elif tagged:
                    other_tag += 1
                elif UNTAGGED.match(line):
                    untagged += 1
                else:
                    malformed += 1
        total = sum(counts)
        top = used.most_common(1)
        print(f"== {arm}")
        print(f"  lines per round : {counts}")
        print(f"  legal tag {legal} · tag outside the list {other_tag} · no tag {untagged} · "
              f"neither shape {malformed} · ending in 'Over.' {over}   (of {total})")
        print(f"  emotions used   : {dict(used.most_common())}")
        if top:
            print(f"  distinct {len(used)} · most frequent '{top[0][0]}' = "
                  f"{top[0][1] / legal * 100:.0f} % of tagged lines")

    same = [k for k in range(1, 11)
            if content(PROBE, f"D-simple-r{k:02d}") is not None
            and content(PROBE, f"D-simple-r{k:02d}") == content(GATE_PROBE, f"D-on-r{k:02d}")]
    print(f"== rounds where D-simple wrote the same text as the gate's D-on: {same}")


if __name__ == "__main__":
    main()
