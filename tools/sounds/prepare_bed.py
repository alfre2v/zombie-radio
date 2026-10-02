"""Prepare the static bed for the app: tools/sounds/bed.yaml says which clips are copied into it.

For each listed Freesound id, the clip is found in the pool (fetched by fetch_freesound.py), measured and copied
unchanged into the app's folder (bed.yaml's app:, the fork's checkout beside this one: ../TalkWithZombies/Sounds/bed).
The clips ship with the app, so the folder is committed in the fork through a pull request; never write into an
installed client, whose tracked files would then differ from its release. Only clips whose licence allows
redistribution in the fork (CC0, CC BY) are copied: any other stops the tool, and nothing changes.

Beside the copies, bed.json holds the facts about them: each clip's file, length, level and gain, the gain bringing
the clip's average level to loudness_dbfs; the level is measured on the mono mix the page plays, (left + right) / 2,
decoded with macOS's afconvert. CREDITS.md credits every clip, the CC BY credit lines marked as required. Which clips
play, and any change of a clip's level by ear, is the story's to say (the fork's stories/<story>/bed.yaml). Nothing
is written without --write; files of an earlier bed.json that are no longer listed are removed, and nothing else in
the folder is touched.

  uv run python tools/sounds/prepare_bed.py
  uv run python tools/sounds/prepare_bed.py --write
"""

import argparse
import array
import hashlib
import json
import math
import shutil
import struct
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
MANIFEST = "bed.json"
CREDITS = "CREDITS.md"
REDISTRIBUTABLE = {"cc0", "cc-by"}


def read_float_wav(path):
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
                if (audio_format, bits) != (3, 32):
                    raise ValueError(f"{path}: expected 32-bit float, got format {audio_format}, {bits}-bit")
                samples = array.array("f")
                samples.frombytes(f.read(size))
                return samples, channels, rate
            else:
                f.seek(size + (size & 1), 1)


def db(x):
    return 20 * math.log10(x) if x > 0 else float("-inf")


def measure(path):
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "decoded.wav"
        subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEF32", str(path), str(wav)], check=True)
        samples, channels, rate = read_float_wav(wav)
    if channels == 1:
        mix = samples
    else:
        frames = [samples[c::channels] for c in range(channels)]
        mix = array.array("f", (sum(frame) / channels for frame in zip(*frames)))
    rms = math.sqrt(math.fsum(s * s for s in mix) / len(mix))
    peak = max(abs(s) for s in mix)
    return {"seconds": len(mix) / rate, "channels": channels, "rate": rate, "rms_dbfs": db(rms),
            "peak_dbfs": db(peak)}


def find_clip(pool, clip_id):
    found = sorted(pool.glob(f"*/{clip_id}-*.mp3"))
    if len(found) != 1:
        return None
    return found[0]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_clips(entries):
    clips = []
    for entry in entries:
        if isinstance(entry, bool) or not isinstance(entry, int):
            sys.exit(f"not a Freesound id: {entry!r} (a change of level by ear goes in the story's bed.yaml)")
        clips.append({"id": entry})
    ids = [c["id"] for c in clips]
    if len(ids) != len(set(ids)):
        sys.exit("a clip is listed twice")
    return clips


def previous_files(app):
    manifest = app / MANIFEST
    if not manifest.exists():
        return set()
    return {c["file"] for c in json.loads(manifest.read_text(encoding="utf-8"))["clips"]}


def credits(rows):
    by = [r for r in rows if r["licence_class"] == "cc-by"]
    free = [r for r in rows if r["licence_class"] == "cc0"]
    lines = [
        "# The static bed's clips: credits",
        "",
        "The radio static the show plays under the voices. Every clip comes from Freesound (https://freesound.org),",
        "as the high-quality MP3 preview Freesound serves (converted by Freesound from the uploaded original),",
        "otherwise unchanged; `bed.json` beside this file lists them with their gains. Written by zombie-radio's",
        "`tools/sounds/prepare_bed.py`.",
        "",
        "## Credit required by the licence (CC BY)",
        "",
    ]
    lines += [f"- {r['credit']}" for r in by] or ["- (none)"]
    lines += ["", "## Public domain (CC0): no credit required, credited with thanks", ""]
    lines += [f"- \"{r['name']}\" by {r['author']} ({r['page']}), {r['licence']}" for r in free] or ["- (none)"]
    return "\n".join(lines) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", type=Path, default=Path(__file__).resolve().parent / "bed.yaml")
    p.add_argument("--app", type=Path, help="the app's bed folder (default: the list's app:)")
    p.add_argument("--write", action="store_true", help="copy the clips and write bed.json; without it, a dry run")
    args = p.parse_args()
    sys.stdout.reconfigure(line_buffering=True)

    cfg = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    pool = Path(cfg["pool"]).expanduser()
    pool = (pool if pool.is_absolute() else REPO / pool).resolve()
    app = (args.app or Path(cfg["app"])).expanduser()
    app = (app if app.is_absolute() else REPO / app).resolve()
    target = cfg["loudness_dbfs"]
    clips = parse_clips(cfg["clips"])

    for clip in clips:
        clip["src"] = find_clip(pool, clip["id"])
        if clip["src"] is None:
            sys.exit(f"{clip['id']}: not in the pool {pool} (fetch it with fetch_freesound.py); nothing changed")
        clip["meta"] = json.loads(clip["src"].with_suffix(".json").read_text(encoding="utf-8"))
        if sha256(clip["src"]) != clip["meta"]["file"]["sha256"]:
            sys.exit(f"{clip['src']}: its SHA-256 differs from its .json's; nothing changed")
    barred = [f"{c['id']} ({c['meta']['licence']['name']})" for c in clips
              if c["meta"]["licence"]["class"] not in REDISTRIBUTABLE]
    if barred:
        sys.exit(f"not redistributable in the fork (only CC0 and CC BY): {', '.join(barred)}; nothing changed")

    print(f"pool {pool}\napp  {app}\nloudness {target} dBFS (the mono mix's average level)\n")
    rows = []
    for clip in clips:
        m = measure(clip["src"])
        gain_db = target - m["rms_dbfs"]
        meta = clip["meta"]
        rows.append({
            "file": clip["src"].name,
            "id": clip["id"],
            "name": meta["name"],
            "author": meta["author"],
            "page": meta["page"],
            "seconds": round(m["seconds"], 2),
            "channels": m["channels"],
            "rms_dbfs": round(m["rms_dbfs"], 2),
            "peak_dbfs": round(m["peak_dbfs"], 2),
            "measured_gain_db": round(gain_db, 2),
            "gain": round(10 ** (gain_db / 20), 4),
            "licence": meta["licence"]["name"],
            "licence_class": meta["licence"]["class"],
            "credit": meta["licence"]["credit"],
        })
        r = rows[-1]
        print(f"{r['id']:>7}  {r['name'][:40]:40}  {r['seconds']:6.1f} s  {r['channels']} ch  "
              f"RMS {r['rms_dbfs']:6.1f}  peak {r['peak_dbfs']:5.1f}  gain {r['measured_gain_db']:+6.1f} dB  "
              f"{r['licence']}")

    stale = sorted(previous_files(app) - {r["file"] for r in rows})
    total = sum(clip["src"].stat().st_size for clip in clips)
    print(f"\n{len(rows)} clips, {sum(r['seconds'] for r in rows) / 60:.1f} minutes, {total / 1e6:.2f} MB")
    for name in stale:
        print(f"no longer listed, {'removed' if args.write else 'would be removed'}: {name}")
    if not args.write:
        print("\n(dry run: nothing written)")
        return

    app.mkdir(parents=True, exist_ok=True)
    for clip in clips:
        dst = app / clip["src"].name
        if not dst.exists() or sha256(dst) != clip["meta"]["file"]["sha256"]:
            shutil.copyfile(clip["src"], dst)
    for name in stale:
        (app / name).unlink(missing_ok=True)
    manifest = {
        "prepared": datetime.now().isoformat(timespec="seconds"),
        "list": "zombie-radio tools/sounds/bed.yaml",
        "loudness_dbfs": target,
        "clips": rows,
    }
    part = app / (MANIFEST + ".part")
    part.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    part.replace(app / MANIFEST)
    (app / CREDITS).write_text(credits(rows), encoding="utf-8")
    print(f"\nwritten: {len(rows)} clips, {MANIFEST} and {CREDITS} in {app}")


if __name__ == "__main__":
    main()
