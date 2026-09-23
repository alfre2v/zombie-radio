"""Derives every timing number in findings.md from raw/probe/*.json (stdlib only).

usage: python3 summarize_timings.py [raw/probe]

Per request the server's `timings` object gives: prompt_n (prompt tokens evaluated),
cache_n (prompt tokens reused from the cache), prompt_ms, predicted_n, predicted_ms.
usage.prompt_tokens is the full prompt size. Every arm here makes one request per round.
"""
import json
import pathlib
import statistics
import sys
from collections import defaultdict

HERE = pathlib.Path(__file__).resolve().parent
ORDER = ["D-simple", "D-forced", "D-aligned-off", "D-aligned", "D-aligned-live"]
PAIRS = [
    ("E2, steering cost (reported): D-forced against D-simple, same plain prompt", "D-simple", "D-forced"),
    ("E1, shipping cost (graded): D-aligned against D-aligned-off, same taught prompt", "D-aligned-off", "D-aligned"),
]


def load(folder):
    rounds = defaultdict(lambda: defaultdict(lambda: {
        "requests": 0, "prompt_size": 0, "prompt_n": 0, "cache_n": 0, "cache_missing": False,
        "prompt_ms": 0.0, "predicted_n": 0, "predicted_ms": 0.0, "wall_ms": 0.0}))
    for path in sorted(folder.glob("*.json")):
        record = json.loads(path.read_text())
        if record["arm"] == "warmup":
            continue
        t = record["response"]["timings"]
        row = rounds[record["arm"]][record["round"]]
        row["requests"] += 1
        row["prompt_size"] += record["response"].get("usage", {}).get("prompt_tokens", 0)
        row["prompt_n"] += t["prompt_n"]
        if "cache_n" in t:
            row["cache_n"] += t["cache_n"]
        else:
            row["cache_missing"] = True
        row["prompt_ms"] += t["prompt_ms"]
        row["predicted_n"] += t["predicted_n"]
        row["predicted_ms"] += t["predicted_ms"]
        row["wall_ms"] += record["wall_ms"]
    return rounds


def reuse(row):
    if row["cache_missing"]:
        return None
    total = row["cache_n"] + row["prompt_n"]
    return row["cache_n"] / total if total else None


def ms_per_token(row):
    return row["predicted_ms"] / row["predicted_n"] if row["predicted_n"] else None


def fmt(value, spec):
    return "n/a" if value is None else format(value, spec)


def table(arm, rows):
    print(f"== arm {arm}")
    print(f"{'round':>5} {'req':>3} {'prompt':>7} {'evald':>6} {'reused':>6} {'reuse%':>6} "
          f"{'prompt_ms':>9} {'gen_n':>5} {'gen_ms':>8} {'ms/tok':>6} {'wall_ms':>8}")
    for k in sorted(rows):
        r = rows[k]
        share = reuse(r)
        print(f"{k:>5} {r['requests']:>3} {r['prompt_size']:>7} {r['prompt_n']:>6} "
              f"{'n/a' if r['cache_missing'] else r['cache_n']:>6} "
              f"{fmt(share * 100 if share is not None else None, '.0f'):>6} "
              f"{r['prompt_ms']:>9.1f} {r['predicted_n']:>5} {r['predicted_ms']:>8.1f} "
              f"{fmt(ms_per_token(r), '.2f'):>6} {r['wall_ms']:>8.1f}")
    print()


def median_of(rows, key, first_round=1):
    values = [key(r) for k, r in rows.items() if k >= first_round and key(r) is not None]
    return statistics.median(values) if values else None


def main():
    folder = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "raw" / "probe"
    rounds = load(folder)
    arms = [a for a in ORDER if a in rounds]
    for arm in arms:
        table(arm, rounds[arm])

    print("== per arm: medians over rounds (prompt and wall from round 2, the cache warm)")
    for arm in arms:
        rows = rounds[arm]
        last = rows[max(rows)]
        print(f"  {arm:15} ms/token {fmt(median_of(rows, ms_per_token), '.3f'):>7}   "
              f"prompt_ms {fmt(median_of(rows, lambda r: r['prompt_ms'], 2), '.1f'):>6}   "
              f"wall_ms {fmt(median_of(rows, lambda r: r['wall_ms'], 2), '.1f'):>7}   "
              f"reuse at round {max(rows)} {fmt(reuse(last) * 100 if reuse(last) is not None else None, '.0f')} %")
    print()

    for title, base, other in PAIRS:
        if base in rounds and other in rounds:
            b = median_of(rounds[base], ms_per_token)
            o = median_of(rounds[other], ms_per_token)
            print(f"== {title}")
            print(f"  {base:15} median ms/token = {b:.3f}")
            print(f"  {other:15} median ms/token = {o:.3f}")
            print(f"  O = ({other} - {base}) / {base} = {(o - b) / b * 100:.1f} %")
            print()
    print("  E1 thresholds: PASS O <= 10 %; PARTIAL 10 % < O <= 25 %; FAIL O > 25 %")
    print()

    if "D-aligned-live" in rounds:
        rows = rounds["D-aligned-live"]
        later = [reuse(rows[k]) for k in sorted(rows) if k >= 2 and reuse(rows[k]) is not None]
        print("== D-aligned-live (reported): share of the prompt reused from the cache, rounds >= 2")
        print(f"  per round: {[fmt(x * 100, '.0f') for x in later]} %")


if __name__ == "__main__":
    main()
