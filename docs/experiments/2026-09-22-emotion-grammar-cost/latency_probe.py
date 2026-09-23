"""Emotion-grammar run: per-round cost of the shared script under three prompt/grammar pairings.

Stdlib only. Writes one JSON file per request under raw/probe/ (request, response,
wall time); summarize_timings.py and check_outputs.py derive every number from them.

Arms (prompt, grammar, history):
  D-simple       plain,  simple,  fixed   the ADR-0003 gate's D-on, re-run as the baseline
  D-forced       plain,  emotion, fixed   the grammar must insert tags the prompt never asked for
  D-aligned-off  taught, none,    fixed   the prompt teaches the tags; no grammar
  D-aligned      taught, emotion, fixed   the configuration the fork would ship
  D-aligned-live taught, emotion, live    as D-aligned, each round's script is the model's own output

usage: python3 latency_probe.py [--arms D-simple,...] [--rounds 10] [--out raw/probe]
"""
import argparse
import json
import pathlib
import sys
import time
import urllib.request

import cast

HERE = pathlib.Path(__file__).resolve().parent
ARMS = {
    "D-simple": ("plain", "simple", False),
    "D-forced": ("plain", "emotion", False),
    "D-aligned-off": ("taught", "none", False),
    "D-aligned": ("taught", "emotion", False),
    "D-aligned-live": ("taught", "emotion", True),
}


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
        cast.wire_request(name, body)
        try:
            result, wall_ms = post(self.url, body)
        except Exception as exc:
            detail = exc.read().decode(errors="replace") if hasattr(exc, "read") else ""
            cast.wire(f"!!!!! {name} failed: {exc} {detail}\n")
            raise
        cast.wire_response(name, result, wall_ms)
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

    def arm(self, name, rounds):
        prompt, grammar_kind, live_history = ARMS[name]
        grammar = None if grammar_kind == "none" else cast.grammar(cast.SPEAKERS, grammar_kind)
        live = [] if live_history else None
        for k in range(1, rounds + 1):
            content = self.send(f"{name}-r{k:02d}", {"arm": name, "round": k, "req": 0},
                                cast.payload(cast.d_messages(k, prompt, live), seed=self.seed,
                                             grammar_text=grammar))
            if live is not None:
                live.append(content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--arms", default=",".join(ARMS))
    parser.add_argument("--rounds", type=int, default=cast.ROUNDS)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--url", default="http://localhost:8080/v1/chat/completions")
    parser.add_argument("--out", default=str(HERE / "raw" / "probe"))
    args = parser.parse_args()

    arms = args.arms.split(",")
    unknown = [a for a in arms if a not in ARMS]
    if unknown:
        sys.exit(f"unknown arms {unknown}")
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    probe = Probe(args.url, out, args.seed)
    probe.send("warmup", {"arm": "warmup", "round": 0, "req": 0},
               cast.payload([{"role": "user", "content": "/no_think Say: ready. Over."}],
                            seed=args.seed))
    for arm in arms:
        probe.arm(arm, args.rounds)


if __name__ == "__main__":
    main()
