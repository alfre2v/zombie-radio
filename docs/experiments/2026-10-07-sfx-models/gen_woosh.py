"""Generate the ten sounds with Woosh-DFlow, seeds 1-3: <out>/<tag>/woosh-<seed>.wav and a .json beside each.

Run from the Woosh checkout (it loads checkpoints/Woosh-DFlow), with its environment:
  .venv/bin/python gen_woosh.py sounds.json ~/sfx-lab/takes
The settings are Woosh's own test script's: 4 steps, renoise [0, 0.5, 0.5, 0.3], cfg 4.5; 100 latent frames a second.
"""

import json
import sys
import time
from pathlib import Path

import torch
import torchaudio
from woosh.components.base import LoadConfig
from woosh.inference.flowmap_sampler import sample_euler
from woosh.model.flowmap_from_pretrained import FlowMapFromPretrained

SETTINGS = {"num_steps": 4, "renoise": [0, 0.5, 0.5, 0.3], "cfg": 4.5}
RATE = 48000

sounds = json.loads(Path(sys.argv[1]).read_text())
out = Path(sys.argv[2]).expanduser()

t = time.perf_counter()
ldm = FlowMapFromPretrained(LoadConfig(path="checkpoints/Woosh-DFlow")).eval().to("cuda")
torch.cuda.synchronize()
print(f"loaded in {time.perf_counter() - t:.1f} s")

for sound in sounds:
    for seed in (1, 2, 3):
        torch.manual_seed(seed)
        noise = torch.randn(1, 128, int(sound["seconds"] * 100) + 1, device="cuda")
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.synchronize()
        t = time.perf_counter()
        with torch.inference_mode():
            cond = ldm.get_cond({"audio": None, "description": [sound["prompt"]]}, no_dropout=True, device="cuda")
            x = sample_euler(model=ldm, noise=noise, cond=cond, **SETTINGS)
            audio = ldm.autoencoder.inverse(x)
        torch.cuda.synchronize()
        took = time.perf_counter() - t
        audio = audio[0].float().cpu()
        audio = audio / max(1.0, audio.abs().max().item())
        folder = out / sound["tag"]
        folder.mkdir(parents=True, exist_ok=True)
        torchaudio.save(str(folder / f"woosh-{seed}.wav"), audio, RATE)
        record = {"model": "Woosh-DFlow", "tag": sound["tag"], "prompt": sound["prompt"], "seed": seed,
                  "settings": SETTINGS, "seconds_asked": sound["seconds"], "seconds_audio": audio.shape[-1] / RATE,
                  "seconds_took": round(took, 3),
                  "peak_gib_torch": round(torch.cuda.max_memory_allocated() / 2**30, 2)}
        (folder / f"woosh-{seed}.json").write_text(json.dumps(record, indent=1) + "\n")
        print(f"{sound['tag']:15} seed {seed}: {took:.2f} s for {record['seconds_audio']:.1f} s of audio")
