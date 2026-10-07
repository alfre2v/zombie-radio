"""Write a compressed copy of each character's reference clips, beside the originals: ref-fear.ogg beside ref-fear.wav.

The copies are Opus in an Ogg file (ffmpeg's libopus), mono, 48 kbps by default. The WAVs are never written or
deleted, and each copy shares its WAV's transcript (ref-fear.txt). Which of the two the app sends is the client's
setting show.reference_format (wav or ogg). A recast (cast_voices.py) removes the copies; run this again after it.

  uv run python tools/voices/compress_voices.py --dry-run
  uv run python tools/voices/compress_voices.py
  uv run python tools/voices/compress_voices.py --only Moira --kbps 32
  uv run python tools/voices/compress_voices.py --remove
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml

CLIP = re.compile(r"ref(?:-[a-z]+)?\.wav")


def clips(folder):
    return sorted(wav for wav in folder.glob("ref*.wav") if CLIP.fullmatch(wav.name))


def compress(wav, kbps):
    ogg = wav.with_suffix(".ogg")
    part = ogg.with_name(ogg.name + ".part")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(wav), "-ac", "1",
                    "-c:a", "libopus", "-b:a", f"{kbps}k", "-f", "ogg", str(part)], check=True)
    part.replace(ogg)
    return ogg


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", type=Path, default=Path(__file__).resolve().parent / "cast.yaml")
    p.add_argument("--only", help="comma-separated character names (default: the whole cast)")
    p.add_argument("--kbps", type=int, default=48, help="the Opus bitrate (default 48)")
    p.add_argument("--remove", action="store_true", help="delete the compressed copies; the WAVs stay")
    p.add_argument("--dry-run", action="store_true", help="show what would be written or deleted, change nothing")
    args = p.parse_args()

    cfg = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    personas = Path(cfg["personas"]).expanduser()
    cast = cfg["cast"]
    names = [n.strip() for n in args.only.split(",")] if args.only else list(cast)
    for name in names:
        if name not in cast:
            sys.exit(f"{name} is not in the cast of {args.config}")
        if not (personas / name).is_dir():
            sys.exit(f"{personas / name} does not exist")

    total_wav = total_ogg = 0
    for name in names:
        folder = personas / name
        if args.remove:
            copies = sorted(wav.with_suffix(".ogg") for wav in clips(folder) if wav.with_suffix(".ogg").exists())
            print(f"{name}: {len(copies)} compressed copies to delete")
            if not args.dry_run:
                for ogg in copies:
                    ogg.unlink()
            continue
        wavs = clips(folder)
        print(f"{name}: {len(wavs)} clips")
        for wav in wavs:
            if args.dry_run:
                print(f"  {wav.with_suffix('.ogg').name} <- {wav.name}")
                continue
            ogg = compress(wav, args.kbps)
            a, b = wav.stat().st_size, ogg.stat().st_size
            total_wav, total_ogg = total_wav + a, total_ogg + b
            print(f"  {ogg.name}: {a // 1024} KB -> {b // 1024} KB")
    if total_wav:
        print(f"\nall clips: {total_wav // 1024} KB -> {total_ogg // 1024} KB ({total_wav / total_ogg:.1f} times smaller)")
    if args.dry_run:
        print("\n(dry run: nothing written)")


if __name__ == "__main__":
    main()
