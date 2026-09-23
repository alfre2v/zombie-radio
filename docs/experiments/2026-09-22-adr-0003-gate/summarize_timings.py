"""Derives every gate-2 number in findings.md from raw/probe/*.json (stdlib only).

usage: python3 summarize_timings.py [raw/probe]

Per request the server's `timings` object gives: prompt_n (prompt tokens evaluated),
cache_n (prompt tokens reused from the cache), prompt_ms, predicted_n, predicted_ms.
usage.prompt_tokens is the full prompt size. A round of arm A is four requests; its
figures are sums over them.
"""
import json
import pathlib
import statistics
import sys
from collections import defaultdict

HERE = pathlib.Path(__file__).resolve().parent
EARLY, LATE = (2, 3, 4), (8, 9, 10)


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


def mean_over(ratios, ks):
    values = [ratios[k] for k in ks if k in ratios]
    return statistics.mean(values) if len(values) == len(ks) else None


def main():
    folder = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "raw" / "probe"
    rounds = load(folder)
    for arm in ("A", "D-off", "D-on", "D-live"):
        if arm in rounds:
            table(arm, rounds[arm])

    if "A" in rounds and "D-off" in rounds:
        print("== gate 2a: R_k = D-off prompt_ms / A prompt_ms (A = sum of its four requests)")
        ratios, wall = {}, {}
        for k in sorted(set(rounds["A"]) & set(rounds["D-off"])):
            a, d = rounds["A"][k], rounds["D-off"][k]
            ratios[k] = d["prompt_ms"] / a["prompt_ms"]
            wall[k] = d["wall_ms"] / a["wall_ms"]
            print(f"  round {k:>2}: R = {ratios[k]:.3f}   (wall-time ratio, reported only: {wall[k]:.3f})")
        print(f"  R_early (mean of rounds {EARLY}) = {fmt(mean_over(ratios, EARLY), '.3f')}")
        print(f"  R_late  (mean of rounds {LATE}) = {fmt(mean_over(ratios, LATE), '.3f')}")
        print("  thresholds: PASS R_late <= 0.50 and R_late <= R_early; PARTIAL R_late < 1.0; FAIL R_late >= 1.0")
        print()

    if "D-off" in rounds and "D-on" in rounds:
        off = [ms_per_token(r) for r in rounds["D-off"].values() if ms_per_token(r)]
        on = [ms_per_token(r) for r in rounds["D-on"].values() if ms_per_token(r)]
        med_off, med_on = statistics.median(off), statistics.median(on)
        print("== gate 2b: grammar overhead on generation, median over rounds of predicted_ms / predicted_n")
        print(f"  D-off median ms/token = {med_off:.3f}")
        print(f"  D-on  median ms/token = {med_on:.3f}")
        print(f"  O = (on - off) / off  = {(med_on - med_off) / med_off * 100:.1f} %")
        print("  thresholds: PASS O <= 10 %; PARTIAL 10 % < O <= 25 %; FAIL O > 25 %")
        print()

    if "D-live" in rounds:
        rows = rounds["D-live"]
        later = [reuse(rows[k]) for k in sorted(rows) if k >= 2 and reuse(rows[k]) is not None]
        print("== D-live (reported, not graded): share of the prompt reused from the cache, rounds >= 2")
        print(f"  per round: {[fmt(x * 100, '.0f') for x in later]} %")
        print(f"  minimum  : {fmt(min(later) * 100 if later else None, '.0f')} %")


if __name__ == "__main__":
    main()
