#!/usr/bin/env python3
"""Summarize fetch_ears.py outputs: files, formats, lengths per type, bytes transferred beyond each file.

  python3 summarize_fetch.py raw/run5-fetch-female.txt raw/run5-fetch-male.txt
"""

import re
import sys

LINE = re.compile(r"^(p\d+)/(\S+)\.wav\s+([\d.]+) MB, CRC ok, ([\d.]+) MB transferred\s+"
                  r"\[(\d+) Hz, (\d+)-bit, (\d+) ch, format (\d+), ([\d.]+) s\]")

rows = []
for path in sys.argv[1:]:
    with open(path, encoding="utf-8") as f:
        rows += [m.groups() for m in map(LINE.match, f) if m]

print(f"files with CRC ok: {len(rows)}; speakers: {len({r[0] for r in rows})}")
print("formats (Hz, bits, channels, format):", sorted({r[4:8] for r in rows}))
for t in sorted({r[1] for r in rows}):
    s = sorted(float(r[8]) for r in rows if r[1] == t)
    print(f"{t}: {len(s)} files, {s[0]}-{s[-1]} s, median {s[len(s) // 2]} s")
extra = [float(r[3]) - float(r[2]) for r in rows]
print(f"transferred beyond each file: {min(extra):.2f}-{max(extra):.2f} MB")
