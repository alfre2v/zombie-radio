"""What the model wrote in the D arms of raw/probe/ (stdlib only).

Prints, per arm, the lines per round, how many lines do not match `Name: text`,
how many end in "Over.", and whether D-off and D-on wrote the same text.
"""
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
PROBE = HERE / "raw" / "probe"
LINE = re.compile(r"^(Daniel|Moira|Ralph|Samantha): [^\n\[\]]+$")


def content(name):
    record = json.loads((PROBE / f"{name}.json").read_text())
    return record["response"]["choices"][0]["message"]["content"] or ""


def main():
    rounds = range(1, 11)
    same = [k for k in rounds if content(f"D-off-r{k:02d}") == content(f"D-on-r{k:02d}")]
    print(f"rounds where D-off and D-on wrote identical text: {same}")
    for arm in ("D-off", "D-on", "D-live"):
        counts, malformed, over = [], 0, 0
        for k in rounds:
            lines = [line for line in content(f"{arm}-r{k:02d}").split("\n") if line.strip()]
            counts.append(len(lines))
            malformed += sum(1 for line in lines if not LINE.match(line))
            over += sum(1 for line in lines if line.rstrip().endswith("Over."))
        print(f"{arm:6} lines per round: {counts}  not `Name: text`: {malformed}  "
              f"ending in 'Over.': {over} of {sum(counts)}")


if __name__ == "__main__":
    main()
