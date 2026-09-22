#!/usr/bin/env bash
# usage: ./stream_check.sh <label> <speakers|none> [seed]
set -euo pipefail
cd "$(dirname "$0")"
label=${1:?label, e.g. main}
speakers=${2:?grammar allowlist, e.g. Daniel,Moira,Ralph,Samantha (or none)}
seed=${3:-42}
mkdir -p raw/stream
req="raw/stream/$label.request.json"
out="raw/stream/$label.sse.txt"
test ! -e "$out" || { echo "$out exists; pick another label"; exit 2; }

python3 cast.py stream-request --speakers "$speakers" --seed "$seed" > "$req"
curl -sN http://localhost:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d @"$req" \
  | python3 -u -c '
import sys, time
t0 = time.monotonic()
for line in iter(sys.stdin.readline, ""):
    print(f"{(time.monotonic() - t0) * 1000:9.1f} {line}", end="", flush=True)
' | tee "$out"
