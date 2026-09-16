#!/usr/bin/env python3
"""Measure-(c) extraction: TTFA table from the tts-serve window capture.

Protocol: every derived number in the experiment record comes from a
committed, dependency-free script over the raw output files — no human
or LLM arithmetic. Python 3 stdlib only.

Input:  raw-tts-window-tail.txt — a `tmux capture-pane` dump of the
        `radio:tts` window (terminal-wrapped lines; mixed shell noise,
        uvicorn lines, and loguru records).
Output: a Markdown report on stdout — per-burst table + short-sentence
        economics summary.

Method notes (constants below are part of the record):
- The capture wraps records at terminal width, so lines are re-joined:
  a new record starts at a loguru timestamp or an uvicorn "INFO:" line
  or a shell prompt; anything else continues the previous line.
- Requests are paired: each "Synthesizing: ... text_len=N" record with
  the next "Synthesis complete: W s wall-clock, A s audio, RTF=R".
- Requests are grouped into BURSTS (one burst ~= one spoken reply):
  a gap > BURST_GAP_S between one request's completion and the next
  request's start opens a new burst. TalkWithMe's streaming client
  fetches sentences of a reply back-to-back (small gaps); separate
  replies are separated by LLM generation and user turns (large gaps).
- Server wall-clock excludes the network: client-perceived TTFA for a
  reply ~= first-sentence wall + network toll (>= 1 RTT ~ 0.215 s to
  NORWAY-1 measured 2026-09-16, plus ~300 KB reference upload).
"""

import re
import sys

RAW_FILE = "raw-tts-window-tail.txt"
BURST_GAP_S = 8.0   # completion->next-start gap that opens a new burst
RTT_S = 0.215       # measured laptop->NORWAY-1 avg, runlog 2026-09-16
SHORT_LEN = 25      # text_len threshold for "short sentence" bucket

REC_START = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} \|")
NEW_LINE = re.compile(r"^(?:\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} \||INFO:|\S*ubuntu@|\$)")
SYNTH_REQ = re.compile(
    r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}).*Synthesizing: seed=\d+, text_len=(\d+)"
)
SYNTH_DONE = re.compile(
    r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}).*Synthesis complete: "
    r"([\d.]+) s wall-clock, ([\d.]+) s\s*audio, RTF=([\d.]+)"
)


def ts_to_s(ts: str) -> float:
    """Timestamp -> seconds since midnight (capture spans one evening)."""
    hh, mm, rest = ts.split(" ")[1].split(":")
    return int(hh) * 3600 + int(mm) * 60 + float(rest)


def unwrap(path):
    """Re-join terminal-wrapped lines into whole records."""
    records = []
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if NEW_LINE.match(line) or not records:
            records.append(line)
        else:
            records[-1] += " " + line.lstrip()
    return records


def parse(records):
    """Pair each request with its completion; return per-request dicts."""
    requests, pending = [], None
    for rec in records:
        m = SYNTH_REQ.match(rec)
        if m:
            pending = {"start": ts_to_s(m.group(1)),
                       "start_ts": m.group(1),
                       "text_len": int(m.group(2))}
            continue
        m = SYNTH_DONE.match(rec)
        if m and pending is not None:
            pending.update(end=ts_to_s(m.group(1)),
                           wall=float(m.group(2)),
                           audio=float(m.group(3)),
                           rtf=float(m.group(4)))
            requests.append(pending)
            pending = None
    return requests


def group_bursts(requests):
    bursts, cur = [], []
    for r in requests:
        if cur and r["start"] - cur[-1]["end"] > BURST_GAP_S:
            bursts.append(cur)
            cur = []
        cur.append(r)
    if cur:
        bursts.append(cur)
    return bursts


def main():
    records = unwrap(RAW_FILE)
    requests = parse(records)
    if not requests:
        sys.exit("no synthesis records parsed — check the raw file")
    bursts = group_bursts(requests)

    print(f"Parsed {len(requests)} synthesis requests -> "
          f"{len(bursts)} bursts (gap > {BURST_GAP_S:.0f} s).\n")
    print("| Burst | Start (box time) | Sents | 1st-sent wall (s) "
          "| Est. TTFA (s)* | Total wall (s) | Total audio (s) "
          "| RTF min-max |")
    print("|---|---|---|---|---|---|---|---|")
    ttfa_estimates = []
    for i, b in enumerate(bursts, 1):
        first_wall = b[0]["wall"]
        ttfa = first_wall + RTT_S
        ttfa_estimates.append(ttfa)
        rtfs = [r["rtf"] for r in b]
        print(f"| {i} | {b[0]['start_ts'].split(' ')[1][:8]} | {len(b)} "
              f"| {first_wall:.1f} | {ttfa:.1f} "
              f"| {sum(r['wall'] for r in b):.1f} "
              f"| {sum(r['audio'] for r in b):.1f} "
              f"| {min(rtfs):.2f}-{max(rtfs):.2f} |")
    print(f"\n*Est. TTFA = first-sentence server wall + 1 RTT "
          f"({RTT_S} s). Excludes the ~300 KB reference upload and "
          f"response download; treat as a lower bound.")

    n = len(ttfa_estimates)
    under = sum(1 for t in ttfa_estimates if t <= 5.0)
    print(f"\nVerdict input: {under}/{n} bursts have est. TTFA <= 5.0 s; "
          f"max {max(ttfa_estimates):.1f} s, "
          f"median {sorted(ttfa_estimates)[n // 2]:.1f} s.")

    short = [r for r in requests if r["text_len"] <= SHORT_LEN]
    longer = [r for r in requests if r["text_len"] > SHORT_LEN]
    print(f"\nShort-sentence economics (server-side only; the "
          f"per-request network toll makes the real gap worse):")
    for name, bucket in (
        (f"text_len <= {SHORT_LEN}", short),
        (f"text_len  > {SHORT_LEN}", longer),
    ):
        if not bucket:
            continue
        mean_rtf = sum(r["rtf"] for r in bucket) / len(bucket)
        over1 = sum(1 for r in bucket if r["rtf"] > 1.0)
        print(f"- {name}: {len(bucket)} requests, mean RTF "
              f"{mean_rtf:.2f}, {over1} with RTF > 1")


if __name__ == "__main__":
    main()
