"""Generate the ten sounds with Stable Audio 3 Small-SFX, seeds 1-3: <out>/<tag>/sa3-<seed>.wav and a .json beside each.

Run from the stable-audio-3 checkout, with its environment, offline (the weights already in HF_HOME):
  HF_HOME=~/sfx-lab/hf HF_HUB_OFFLINE=1 .venv/bin/python gen_sa3.py sounds.json ~/sfx-lab/takes
The settings are the model's defaults: 8 steps, cfg_scale 1.0 (no guidance); half precision; 44.1 kHz stereo.
"""

import json
import sys
import time
from pathlib import Path

import torch
import torchaudio
from stable_audio_3 import StableAudioModel

SETTINGS = {"steps": 8, "cfg_scale": 1.0}
RATE = 44100

sounds = json.loads(Path(sys.argv[1]).read_text())
out = Path(sys.argv[2]).expanduser()

t = time.perf_counter()
model = StableAudioModel.from_pretrained("small-sfx", device="cuda")
torch.cuda.synchronize()
print(f"loaded in {time.perf_counter() - t:.1f} s")

for sound in sounds:
    for seed in (1, 2, 3):
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.synchronize()
        t = time.perf_counter()
        audio = model.generate(prompt=sound["prompt"], duration=sound["seconds"], seed=seed, **SETTINGS)
        torch.cuda.synchronize()
        took = time.perf_counter() - t
        audio = audio[0].float().cpu()
        audio = audio / max(1.0, audio.abs().max().item())
        folder = out / sound["tag"]
        folder.mkdir(parents=True, exist_ok=True)
        torchaudio.save(str(folder / f"sa3-{seed}.wav"), audio, RATE)
        record = {"model": "Stable Audio 3 Small-SFX", "tag": sound["tag"], "prompt": sound["prompt"], "seed": seed,
                  "settings": SETTINGS, "seconds_asked": sound["seconds"], "seconds_audio": audio.shape[-1] / RATE,
                  "seconds_took": round(took, 3),
                  "peak_gib_torch": round(torch.cuda.max_memory_allocated() / 2**30, 2)}
        (folder / f"sa3-{seed}.json").write_text(json.dumps(record, indent=1) + "\n")
        print(f"{sound['tag']:15} seed {seed}: {took:.2f} s for {record['seconds_audio']:.1f} s of audio")
