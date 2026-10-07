"""Generate the ambience's takes with Stable Audio 3 Small-SFX: <out>/<tag>/sa3-<seed>.wav and a .json beside each.

Runs on the GPU box, from the stable-audio-3 checkout, with its environment, offline (the weights already in HF_HOME):

  HF_HOME=~/sfx-lab/hf HF_HUB_OFFLINE=1 .venv/bin/python gen_ambience.py ambience.yaml ~/sfx-lab/ambience/round1 --seeds 1
  HF_HOME=~/sfx-lab/hf HF_HUB_OFFLINE=1 .venv/bin/python gen_ambience.py ambience.yaml ~/sfx-lab/ambience/round2 \\
      --seeds 1-5 --only dead-crowd-far,gun-burst-far
"""

import argparse
import json
import time
from pathlib import Path

import torch
import torchaudio
import yaml
from stable_audio_3 import StableAudioModel

SETTINGS = {"steps": 8, "cfg_scale": 1.0}
RATE = 44100


def seeds(spec):
    first, _, last = spec.partition("-")
    return range(int(first), int(last or first) + 1)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("prompts", type=Path)
    p.add_argument("out", type=Path)
    p.add_argument("--seeds", default="1", help="a seed or a range, e.g. 1 or 1-5")
    p.add_argument("--only", help="comma-separated tags (default: every prompt)")
    args = p.parse_args()

    prompts = yaml.safe_load(args.prompts.read_text())["prompts"]
    if args.only:
        wanted = set(args.only.split(","))
        prompts = [x for x in prompts if x["tag"] in wanted]
    out = args.out.expanduser()

    t = time.perf_counter()
    model = StableAudioModel.from_pretrained("small-sfx", device="cuda")
    print(f"loaded in {time.perf_counter() - t:.1f} s", flush=True)

    for x in prompts:
        for seed in seeds(args.seeds):
            torch.cuda.synchronize()
            t = time.perf_counter()
            audio = model.generate(prompt=x["prompt"], duration=x["seconds"], seed=seed, **SETTINGS)
            torch.cuda.synchronize()
            took = time.perf_counter() - t
            audio = audio[0].float().cpu()
            audio = audio / max(1.0, audio.abs().max().item())
            folder = out / x["tag"]
            folder.mkdir(parents=True, exist_ok=True)
            torchaudio.save(str(folder / f"sa3-{seed}.wav"), audio, RATE)
            record = {"model": "Stable Audio 3 Small-SFX", **x, "seed": seed, "settings": SETTINGS,
                      "seconds_audio": audio.shape[-1] / RATE, "seconds_took": round(took, 3)}
            (folder / f"sa3-{seed}.json").write_text(json.dumps(record, indent=1) + "\n")
            print(f"{x['tag']:20} seed {seed}: {took:.2f} s for {record['seconds_audio']:.0f} s", flush=True)


if __name__ == "__main__":
    main()
