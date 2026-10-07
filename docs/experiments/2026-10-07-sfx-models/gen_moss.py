"""Generate the ten sounds with MOSS-SoundEffect v2.0, seeds 1-3: <out>/<tag>/moss-<seed>.wav and a .json beside each.

Run from moss_soundeffect_v2 in the MOSS-TTS checkout, with its environment, offline, compiling off:
  TORCHDYNAMO_DISABLE=1 HF_HOME=~/sfx-lab/hf HF_HUB_OFFLINE=1 .venv/bin/python gen_moss.py sounds.json ~/sfx-lab/takes
The settings are the pipeline's defaults, the model card's: 100 steps, cfg 4.0, sigma shift 5.0; bfloat16; 48 kHz mono.
Saved with soundfile: torchaudio 2.9 writes through TorchCodec, which needs FFmpeg on the system (not on the box).
"""

import json
import sys
import time
from pathlib import Path

import soundfile as sf
import torch
from moss_soundeffect_v2 import MossSoundEffectPipeline

SETTINGS = {"num_inference_steps": 100, "cfg_scale": 4.0, "sigma_shift": 5.0}

sounds = json.loads(Path(sys.argv[1]).read_text())
out = Path(sys.argv[2]).expanduser()

t = time.perf_counter()
pipe = MossSoundEffectPipeline.from_pretrained("OpenMOSS-Team/MOSS-SoundEffect-v2.0", torch_dtype=torch.bfloat16,
                                               device="cuda")
torch.cuda.synchronize()
print(f"loaded in {time.perf_counter() - t:.1f} s", flush=True)

for sound in sounds:
    for seed in (1, 2, 3):
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.synchronize()
        t = time.perf_counter()
        audio = pipe(prompt=sound["prompt"], seconds=sound["seconds"], seed=seed, progress_bar_cmd=lambda x, **k: x,
                     **SETTINGS)
        torch.cuda.synchronize()
        took = time.perf_counter() - t
        audio = audio[0].float().cpu()
        audio = audio / max(1.0, audio.abs().max().item())
        folder = out / sound["tag"]
        folder.mkdir(parents=True, exist_ok=True)
        sf.write(str(folder / f"moss-{seed}.wav"), audio.T.numpy(), pipe.sample_rate, subtype="FLOAT")
        record = {"model": "MOSS-SoundEffect v2.0", "tag": sound["tag"], "prompt": sound["prompt"], "seed": seed,
                  "settings": SETTINGS, "seconds_asked": sound["seconds"],
                  "seconds_audio": audio.shape[-1] / pipe.sample_rate, "seconds_took": round(took, 3),
                  "peak_gib_torch": round(torch.cuda.max_memory_allocated() / 2**30, 2)}
        (folder / f"moss-{seed}.json").write_text(json.dumps(record, indent=1) + "\n")
        print(f"{sound['tag']:15} seed {seed}: {took:.2f} s for {record['seconds_audio']:.1f} s of audio", flush=True)
