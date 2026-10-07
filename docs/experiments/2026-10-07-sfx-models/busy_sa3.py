"""Keep Stable Audio 3 Small-SFX generating the ten sounds back to back for N seconds (the load for the voice test).

  HF_HOME=~/sfx-lab/hf HF_HUB_OFFLINE=1 .venv/bin/python busy_sa3.py sounds.json 75
"""

import json
import sys
import time
from pathlib import Path

import torch
from stable_audio_3 import StableAudioModel

sounds = json.loads(Path(sys.argv[1]).read_text())
model = StableAudioModel.from_pretrained("small-sfx", device="cuda")
print("loaded, generating", flush=True)
end, n = time.time() + float(sys.argv[2]), 0
while time.time() < end:
    sound = sounds[n % len(sounds)]
    model.generate(prompt=sound["prompt"], duration=sound["seconds"], seed=n, steps=8, cfg_scale=1.0)
    torch.cuda.synchronize()
    n += 1
print(f"{n} takes generated", flush=True)
