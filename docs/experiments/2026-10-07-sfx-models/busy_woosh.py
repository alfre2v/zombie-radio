"""Keep Woosh-DFlow generating the ten sounds back to back for N seconds (the load for the voice test).

  .venv/bin/python busy_woosh.py sounds.json 120
"""

import json
import sys
import time
from pathlib import Path

import torch
from woosh.components.base import LoadConfig
from woosh.inference.flowmap_sampler import sample_euler
from woosh.model.flowmap_from_pretrained import FlowMapFromPretrained

sounds = json.loads(Path(sys.argv[1]).read_text())
ldm = FlowMapFromPretrained(LoadConfig(path="checkpoints/Woosh-DFlow")).eval().to("cuda")
print("loaded, generating", flush=True)
end, n = time.time() + float(sys.argv[2]), 0
while time.time() < end:
    sound = sounds[n % len(sounds)]
    noise = torch.randn(1, 128, int(sound["seconds"] * 100) + 1, device="cuda")
    with torch.inference_mode():
        cond = ldm.get_cond({"audio": None, "description": [sound["prompt"]]}, no_dropout=True, device="cuda")
        ldm.autoencoder.inverse(sample_euler(model=ldm, noise=noise, cond=cond, num_steps=4,
                                             renoise=[0, 0.5, 0.5, 0.3], cfg=4.5))
    torch.cuda.synchronize()
    n += 1
print(f"{n} takes generated", flush=True)
