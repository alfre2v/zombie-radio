#!/usr/bin/env bash
# usage: ./stream_check.sh <label> <plain|taught> <none|simple|emotion> [seed]
set -euo pipefail
cd "$(dirname "$0")"
label=${1:?label, e.g. main}
prompt=${2:?prompt: plain or taught}
grammar=${3:?grammar: none, simple or emotion}
seed=${4:-42}
mkdir -p raw/stream
req="raw/stream/$label.request.json"
out="raw/stream/$label.sse.txt"
test ! -e "$out" || { echo "$out exists; pick another label"; exit 2; }

python3 cast.py stream-request --prompt "$prompt" --grammar "$grammar" --seed "$seed" > "$req"
python3 -c '
import cast, json, sys
cast.wire_request(sys.argv[1], json.load(open(sys.argv[2])))
cast.wire(f"----- {sys.argv[1]} <- streaming\n")
' "stream-$label" "$req"
start=$(python3 -c 'import time; print(time.time())')
curl -sN http://localhost:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d @"$req" \
  | python3 -u -c '
import sys, time
import cast
t0 = float(sys.argv[1])
for line in iter(sys.stdin.readline, ""):
    print(f"{(time.time() - t0) * 1000:9.1f} {line}", end="", flush=True)
    cast.wire_stream_line(line)
' "$start" | tee "$out"
