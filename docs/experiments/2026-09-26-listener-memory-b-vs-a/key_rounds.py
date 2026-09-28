"""The rounds behind the rows judged by reading, for each column and seed, and the system prompt compared.

python3 key_rounds.py  — reads raw/drive-<label>-<seed>.txt and raw/runs/<id>/script.json. Dependency-free.
For each seed: Maria's first round, the anonymous "Hello again, lab." round and the re-call after it, and
Alfredo's return, with the lines the model wrote; then whether the three columns sent the same system prompt.
"""
import json
import re
from pathlib import Path

RAW = Path(__file__).resolve().parent / "raw"
LABELS = ["b-old", "b-new", "a-sim"]
SEEDS = [42, 7, 2026]
KEYS = [("Maria's first round", "This is Maria, from Dallas."), ("the anonymous voice", "Hello again, lab."),
        ("Alfredo's return", "It's me, Alfredo, from Austin. I still have the truck.")]


def record(label, seed):
    text = (RAW / f"drive-{label}-{seed}.txt").read_text()
    run_id = re.search(r"record: runs/(\S+)/script.json", text).group(1)
    return run_id, json.loads((RAW / "runs" / run_id / "script.json").read_text())


def show(r):
    heard = f' — heard "{r["listener"]}"' if r.get("listener") else ""
    print(f"  round {r['n']} {r['kind']}{heard}")
    for line in r["lines"]:
        print(f"      {line['speaker']}: {line['spoken']}")


systems = {}
for seed in SEEDS:
    for label in LABELS:
        run_id, data = record(label, seed)
        systems[(label, seed)] = data["systems"]
        rounds = data["rounds"]
        print(f"=== {label}, seed {seed} (run {run_id})")
        for name, words in KEYS:
            i = next(i for i, r in enumerate(rounds) if r.get("listener") == words)
            print(f" {name}:")
            show(rounds[i])
            if words == "Hello again, lab." and i + 1 < len(rounds):
                show(rounds[i + 1])
        print()
for seed in SEEDS:
    same = all(systems[(label, seed)] == systems[(LABELS[0], seed)] for label in LABELS)
    print(f"seed {seed}: the system prompt identical in the three columns: {same}")
