"""ADR-0003 gate 2: per-round prompt cost, structure A (per persona) versus D (shared script).

Stdlib only. Writes one JSON file per request under raw/probe/ (request, response,
wall time); summarize_timings.py derives every number from those files.

Arms:
  A       TalkWithMe 7.1's structure, four requests per round, no grammar
  D-off   shared script, one request per round, no grammar
  D-on    shared script, one request per round, screenplay grammar
  D-live  as D-on, but each round's script is the model's own previous output

usage: python3 latency_probe.py [--arms A,D-off,D-on,D-live] [--rounds 10] [--out raw/probe]
"""
import argparse
import json
import pathlib
import sys
import time
import urllib.request

import cast

HERE = pathlib.Path(__file__).resolve().parent


def post(url, body):
    request = urllib.request.Request(url, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
    t0 = time.monotonic()
    with urllib.request.urlopen(request, timeout=300) as response:
        result = json.load(response)
    return result, (time.monotonic() - t0) * 1000


class Probe:
    def __init__(self, url, out, seed):
        self.url, self.out, self.seed = url, out, seed

    def send(self, name, meta, body):
        path = self.out / f"{name}.json"
        if path.exists():
            sys.exit(f"{path} exists; use another --out")
        result, wall_ms = post(self.url, body)
        if "timings" not in result:
            sys.exit(f"{name}: response carries no 'timings' object; stop and rethink the endpoint")
        path.write_text(json.dumps({**meta, "wall_ms": round(wall_ms, 1),
                                    "request": body, "response": result},
                                   indent=1, ensure_ascii=False))
        t = result["timings"]
        print(f"{name:24} prompt_n={t.get('prompt_n')} cache_n={t.get('cache_n')} "
              f"prompt_ms={t.get('prompt_ms', 0):.1f} predicted_n={t.get('predicted_n')} "
              f"wall_ms={wall_ms:.1f}", flush=True)
        return result["choices"][0]["message"].get("content") or ""

    def arm_a(self, rounds):
        for k in range(1, rounds + 1):
            for j in range(4):
                persona, messages = cast.a_messages(k, j)
                self.send(f"A-r{k:02d}-{j}-{persona}",
                          {"arm": "A", "round": k, "req": j, "persona": persona},
                          cast.payload(messages, seed=self.seed))

    def arm_d(self, arm, rounds):
        grammar = cast.grammar(cast.SPEAKERS) if arm in ("D-on", "D-live") else None
        live = [] if arm == "D-live" else None
        for k in range(1, rounds + 1):
            content = self.send(f"{arm}-r{k:02d}", {"arm": arm, "round": k, "req": 0},
                                cast.payload(cast.d_messages(k, live), seed=self.seed,
                                             grammar_text=grammar))
            if live is not None:
                live.append(content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--arms", default="A,D-off,D-on,D-live")
    parser.add_argument("--rounds", type=int, default=cast.ROUNDS)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--url", default="http://localhost:8080/v1/chat/completions")
    parser.add_argument("--out", default=str(HERE / "raw" / "probe"))
    args = parser.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    probe = Probe(args.url, out, args.seed)
    probe.send("warmup", {"arm": "warmup", "round": 0, "req": 0},
               cast.payload([{"role": "user", "content": "/no_think Say: ready. Over."}],
                            seed=args.seed))
    for arm in args.arms.split(","):
        if arm == "A":
            probe.arm_a(args.rounds)
        elif arm in ("D-off", "D-on", "D-live"):
            probe.arm_d(arm, args.rounds)
        else:
            sys.exit(f"unknown arm {arm}")


if __name__ == "__main__":
    main()
