"""Time the same voice request to tts-serve through the tunnel: N requests, one after another.

  python3 time_voice.py ~/TalkWithZombies-client/Personas/Moira/ref-fear 8 alone
The reference is <path>.wav with its transcript <path>.txt; the seed is fixed, so every request is the same work.
"""

import base64
import json
import statistics
import sys
import time
import urllib.request
from pathlib import Path

ref, n, label = Path(sys.argv[1]).expanduser(), int(sys.argv[2]), sys.argv[3]
body = json.dumps({"text": "We are still here. The doors are holding, but the generator is failing. Over.",
                   "audio_base64": base64.b64encode(ref.with_suffix(".wav").read_bytes()).decode(),
                   "reference_text": ref.with_suffix(".txt").read_text().strip(), "seed": 7}).encode()
times = []
for _ in range(n):
    t = time.time()
    with urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:8001/synthesize", body,
                                                       {"Content-Type": "application/json"})) as r:
        r.read()
    times.append(time.time() - t)
print(f"{label}: median {statistics.median(times):.2f} s, min {min(times):.2f}, max {max(times):.2f} "
      f"({', '.join(f'{x:.2f}' for x in times)})")
