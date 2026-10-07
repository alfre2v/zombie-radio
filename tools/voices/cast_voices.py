"""Cast EARS voices as the show's characters: tools/voices/cast.yaml says who voices whom.

For each character, the chosen speaker's clip becomes Personas/<Name>/ref.wav (mono 24 kHz 16-bit, loudness
evened out) with its transcript in ref.txt; ref.source says where it came from. The first cast keeps the
placeholder voice as ref.placeholder.wav / .txt. With --all-emotions, it also writes every read emotion the speaker
recorded, named after the recording: ref-fear.wav from emo_fear_sentences, and so on (23 with EARS). Which mood speaks
with which recording is the story's to say (the voices of its overtones.yaml), not this tool's.

  uv run python tools/voices/cast_voices.py --dry-run
  uv run python tools/voices/cast_voices.py
  uv run python tools/voices/cast_voices.py --only Moira --all-emotions
"""

import argparse
import array
import math
import re
import struct
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
EMOTION = re.compile(r"emo_(?P<emotion>[a-z]+)_sentences")
CREDIT = "EARS, CC BY-NC 4.0 (Richter et al., Interspeech 2024)"


def read_wav(path):
    with open(path, "rb") as f:
        riff, _, wave = struct.unpack("<4sI4s", f.read(12))
        if riff != b"RIFF" or wave != b"WAVE":
            raise ValueError(f"{path}: not a WAV file")
        fmt = None
        while True:
            head = f.read(8)
            if len(head) < 8:
                raise ValueError(f"{path}: no audio data")
            cid, size = struct.unpack("<4sI", head)
            if cid == b"fmt ":
                fmt = struct.unpack("<HHIIHH", f.read(16))
                f.seek(size - 16, 1)
            elif cid == b"data" and fmt:
                audio_format, channels, rate, _, _, bits = fmt
                if (audio_format, bits, channels) != (3, 32, 1):
                    raise ValueError(f"{path}: expected mono 32-bit float, got format {audio_format}, "
                                     f"{bits}-bit, {channels} channels")
                samples = array.array("f")
                samples.frombytes(f.read(size))
                return samples, rate
            else:
                f.seek(size + (size & 1), 1)


def write_float_wav(path, samples, rate):
    data = samples.tobytes()
    with open(path, "wb") as f:
        f.write(struct.pack("<4sI4s", b"RIFF", 36 + len(data), b"WAVE"))
        f.write(struct.pack("<4sIHHIIHH", b"fmt ", 16, 3, 1, rate, rate * 4, 4, 32))
        f.write(struct.pack("<4sI", b"data", len(data)))
        f.write(data)


def db(x):
    return 20 * math.log10(x) if x > 0 else float("-inf")


def level(samples, loudness_dbfs, peak_dbfs):
    rms = math.sqrt(sum(s * s for s in samples) / len(samples))
    peak = max(abs(s) for s in samples)
    if loudness_dbfs is None:
        return 1.0, rms, peak
    gain = min(10 ** (loudness_dbfs / 20) / rms, 10 ** (peak_dbfs / 20) / peak)
    return gain, rms, peak


def convert(src, dst, loudness_dbfs, peak_dbfs):
    samples, rate = read_wav(src)
    gain, rms, peak = level(samples, loudness_dbfs, peak_dbfs)
    with tempfile.TemporaryDirectory() as tmp:
        scaled = Path(tmp) / "scaled.wav"
        write_float_wav(scaled, array.array("f", (s * gain for s in samples)), rate)
        part = dst.with_name(dst.name + ".part")
        subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16@24000", "-c", "1", str(scaled), str(part)],
                       check=True)
        part.replace(dst)
    return len(samples) / rate, db(rms), db(rms * gain), db(peak * gain)


def keep_placeholder(folder, dry_run):
    ref, source, kept = folder / "ref.wav", folder / "ref.source", folder / "ref.placeholder.wav"
    if not ref.exists() or source.exists() or kept.exists():
        return
    print(f"  keeps the placeholder voice as {kept.name}")
    if not dry_run:
        ref.replace(kept)
        if (folder / "ref.txt").exists():
            (folder / "ref.txt").replace(folder / "ref.placeholder.txt")


def cast_clip(src_dir, speaker, clip_type, folder, stem, cfg, dry_run):
    wav, txt = src_dir / f"{clip_type}.wav", src_dir / f"{clip_type}.txt"
    if not wav.exists() or not txt.exists():
        print(f"  {stem}: {speaker}/{clip_type} is not downloaded (fetch it with fetch_ears.py)")
        return None
    if dry_run:
        print(f"  {stem}.wav <- {speaker}/{clip_type}")
        return f"{stem}.wav <- {speaker}/{clip_type}"
    seconds, before, after, peak = convert(wav, folder / f"{stem}.wav", cfg.get("loudness_dbfs"),
                                           cfg.get("peak_dbfs", -1))
    (folder / f"{stem}.txt").write_text(txt.read_text(encoding="utf-8").strip() + "\n", encoding="utf-8")
    print(f"  {stem}.wav <- {speaker}/{clip_type}: {seconds:.1f} s, "
          f"RMS {before:.1f} -> {after:.1f} dBFS, peak {peak:.1f} dBFS")
    return f"{stem}.wav <- {speaker}/{clip_type}"


def recorded_emotions(src_dir):
    found = (EMOTION.fullmatch(wav.stem) for wav in src_dir.glob("emo_*_sentences.wav"))
    return sorted(m["emotion"] for m in found if m and (src_dir / f"{m.string}.txt").exists())


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", type=Path, default=Path(__file__).resolve().parent / "cast.yaml")
    p.add_argument("--only", help="comma-separated character names (default: the whole cast)")
    p.add_argument("--all-emotions", action="store_true",
                   help="also write every read emotion the speaker recorded, as ref-<emotion>.wav")
    p.add_argument("--dry-run", action="store_true", help="show what would be written, change nothing")
    args = p.parse_args()

    cfg = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    source = Path(cfg["source"]).expanduser()
    source = source if source.is_absolute() else REPO / source
    personas = Path(cfg["personas"]).expanduser()
    cast = cfg["cast"]
    names = [n.strip() for n in args.only.split(",")] if args.only else list(cast)

    for name in names:
        if name not in cast:
            sys.exit(f"{name} is not in the cast of {args.config}")
        if not (personas / name).is_dir():
            sys.exit(f"{personas / name} does not exist: the persona must exist before it is cast")
        clip = source / cast[name] / cfg["voice"]
        if not clip.with_suffix(".wav").exists() or not clip.with_suffix(".txt").exists():
            sys.exit(f"{cast[name]}/{cfg['voice']} is not downloaded (fetch it with fetch_ears.py); nothing changed")

    for name in names:
        speaker, folder = cast[name], personas / name
        print(f"{name} <- {speaker}")
        keep_placeholder(folder, args.dry_run)
        if not args.dry_run:
            for old in [*folder.glob("ref-*.*"), *folder.glob("ref.ogg")]:
                old.unlink()
        written = [cast_clip(source / speaker, speaker, cfg["voice"], folder, "ref", cfg, args.dry_run)]
        if args.all_emotions:
            emotions = recorded_emotions(source / speaker)
            print(f"  {len(emotions)} read emotions downloaded for {speaker}")
            for emotion in emotions:
                written.append(cast_clip(source / speaker, speaker, f"emo_{emotion}_sentences", folder,
                                         f"ref-{emotion}", cfg, args.dry_run))
        if not args.dry_run and written[0]:
            lines = [f"cast {datetime.now():%Y-%m-%dT%H:%M:%S} from {CREDIT}"] + [w for w in written if w]
            (folder / "ref.source").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if args.dry_run:
        print("\n(dry run: nothing written)")


if __name__ == "__main__":
    main()
