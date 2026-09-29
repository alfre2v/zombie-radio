#!/usr/bin/env python3
"""List EARS speakers and files, and fetch single WAV files out of the per-speaker zips with HTTP range requests.

Standard library only. Nothing is downloaded without --fetch.

  python3 fetch_ears.py --speakers-info [--gender female] [--age 26-35] [--native english]
  python3 fetch_ears.py --list --speakers 1
  python3 fetch_ears.py --types emo_neutral_sentences,emo_fear_sentences --speakers 1-5          (a dry run)
  python3 fetch_ears.py --types emo_neutral_sentences,emo_fear_sentences --speakers 1-5 --fetch
"""

import argparse
import html
import io
import json
import re
import shutil
import struct
import sys
import urllib.request
import zipfile
from pathlib import Path

RAW = "https://raw.githubusercontent.com/facebookresearch/ears_dataset/main"
ZIP_URL = "https://github.com/facebookresearch/ears_dataset/releases/download/dataset/{speaker}.zip"
USER_AGENT = "zombie-radio-ears-fetch/0.1 (+https://github.com/alfre2v/zombie-radio)"
DEFAULT_OUT = Path(__file__).resolve().parent / "datasets" / "ears"
EMOTION = re.compile(r"^emo_(?P<emotion>[a-z]+)_(?P<kind>sentences|freeform)$")


class Stats:
    requests = 0
    transferred = 0


def _get(url, byte_range=None):
    headers = {"User-Agent": USER_AGENT}
    if byte_range:
        headers["Range"] = "bytes=%d-%d" % byte_range
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as resp:
        data = resp.read()
        Stats.requests += 1
        Stats.transferred += len(data)
        return resp, data


def get_json(name):
    return json.loads(_get(f"{RAW}/{name}")[1])


class RemoteFile(io.RawIOBase):
    def __init__(self, url):
        resp, _ = _get(url, (0, 0))
        if resp.status != 206:
            raise OSError(f"no range support at {url} (status {resp.status})")
        self.url = resp.geturl()
        self.size = int(resp.headers["Content-Range"].rsplit("/", 1)[1])
        self.pos = 0

    def readable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=io.SEEK_SET):
        base = {io.SEEK_SET: 0, io.SEEK_CUR: self.pos, io.SEEK_END: self.size}[whence]
        self.pos = max(0, base + offset)
        return self.pos

    def readinto(self, buf):
        if self.pos >= self.size or not len(buf):
            return 0
        end = min(self.pos + len(buf), self.size) - 1
        resp, data = _get(self.url, (self.pos, end))
        if resp.status != 206:
            raise OSError(f"range request refused (status {resp.status})")
        buf[: len(data)] = data
        self.pos += len(data)
        return len(data)


def open_zip(speaker):
    return zipfile.ZipFile(io.BufferedReader(RemoteFile(ZIP_URL.format(speaker=speaker)), buffer_size=1 << 16))


def members(zf):
    return {Path(info.filename).stem: info for info in zf.infolist() if info.filename.lower().endswith(".wav")}


def wav_info(path):
    with open(path, "rb") as f:
        riff, _, wave = struct.unpack("<4sI4s", f.read(12))
        if riff != b"RIFF" or wave != b"WAVE":
            return None
        fmt = None
        while True:
            head = f.read(8)
            if len(head) < 8:
                return None
            cid, size = struct.unpack("<4sI", head)
            if cid == b"fmt ":
                fmt = struct.unpack("<HHIIHH", f.read(16))
                f.seek(size - 16, io.SEEK_CUR)
            elif cid == b"data" and fmt:
                audio_format, channels, rate, byte_rate, _, bits = fmt
                return {"format": audio_format, "channels": channels, "rate": rate, "bits": bits,
                        "seconds": size / byte_rate}
            else:
                f.seek(size + (size & 1), io.SEEK_CUR)


def parse_speakers(spec, stats):
    if not spec:
        return list(stats)
    chosen = []
    for part in spec.split(","):
        part = part.strip().lower().lstrip("p")
        lo, _, hi = part.partition("-")
        for n in range(int(lo), int(hi or lo) + 1):
            chosen.append(f"p{n:03d}")
    return chosen


def filter_speakers(speakers, stats, args):
    keep = []
    for s in speakers:
        info = stats.get(s)
        if info is None:
            sys.exit(f"unknown speaker {s}")
        if args.gender and info["gender"] != args.gender:
            continue
        if args.age and info["age"] != args.age:
            continue
        if args.native and args.native not in info["native language"]:
            continue
        keep.append(s)
    return keep


def describe(info):
    return f'{info["gender"]}, {info["age"]}, {info["native language"]}, {info["ethnicity"]}'


def show_speakers(speakers, stats):
    for s in speakers:
        print(f"{s}  {describe(stats[s])}")
    genders = {}
    for s in speakers:
        genders[stats[s]["gender"]] = genders.get(stats[s]["gender"], 0) + 1
    print(f"\n{len(speakers)} speakers: " + ", ".join(f"{n} {g}" for g, n in sorted(genders.items())))


def show_types(speakers):
    seen = {}
    for s in speakers:
        with open_zip(s) as zf:
            found = members(zf)
        print(f"{s}: {len(found)} WAV files, {sum(i.file_size for i in found.values()) / 1e6:.0f} MB")
        if len(speakers) == 1:
            for stem, info in sorted(found.items()):
                m = EMOTION.match(stem)
                label = f'emotion "{m["emotion"]}", {m["kind"]}' if m else ""
                compressed = "" if info.compress_type == zipfile.ZIP_STORED else "  (compressed)"
                print(f"  {stem:40s} {info.file_size / 1e6:6.2f} MB  {label}{compressed}")
        for stem in found:
            seen[stem] = seen.get(stem, 0) + 1
    if len(speakers) > 1:
        common = [t for t, n in seen.items() if n == len(speakers)]
        print(f"\n{len(seen)} types in all; {len(common)} present for every speaker listed")
        for t, n in sorted(seen.items()):
            if n != len(speakers):
                print(f"  {t}: {n} of {len(speakers)} speakers")


def fetch(speakers, types, out, stats, do_fetch):
    transcripts = get_json("transcripts.json") if do_fetch else {}
    plan_bytes = 0
    for s in speakers:
        with open_zip(s) as zf:
            found = members(zf)
            for t in types:
                info = found.get(t)
                if info is None:
                    print(f"{s}/{t}: not in the zip")
                    continue
                plan_bytes += info.compress_size
                target = out / s / f"{t}.wav"
                if not do_fetch:
                    print(f"{s}/{t}.wav  {info.file_size / 1e6:.2f} MB  (would fetch)")
                    continue
                before = Stats.transferred
                target.parent.mkdir(parents=True, exist_ok=True)
                tmp = target.with_suffix(".part")
                with zf.open(info) as src, open(tmp, "wb") as dst:
                    shutil.copyfileobj(src, dst, 1 << 20)
                tmp.replace(target)
                if t in transcripts:
                    target.with_suffix(".txt").write_text(transcripts[t] + "\n", encoding="utf-8")
                w = wav_info(target)
                shape = (f'{w["rate"]} Hz, {w["bits"]}-bit, {w["channels"]} ch, format {w["format"]}, '
                         f'{w["seconds"]:.1f} s') if w else "not a WAV header I can read"
                print(f"{s}/{t}.wav  {info.file_size / 1e6:.2f} MB, CRC ok, "
                      f"{(Stats.transferred - before) / 1e6:.2f} MB transferred  [{shape}]")
    print(f"\n{'fetched' if do_fetch else 'would fetch'}: {plan_bytes / 1e6:.2f} MB")
    if do_fetch:
        write_index(out, stats)


def write_index(out, stats):
    files = sorted(out.glob("p[0-9][0-9][0-9]/*.wav"))
    speakers = sorted({f.parent.name for f in files})
    types = sorted({f.stem for f in files})
    rows = []
    for s in speakers:
        cells = []
        for t in types:
            f = out / s / f"{t}.wav"
            cells.append(f'<td><audio controls preload="none" src="{s}/{t}.wav"></audio></td>' if f.exists()
                         else "<td></td>")
        label = html.escape(describe(stats[s])) if s in stats else ""
        rows.append(f"<tr><th>{s}<br><small>{label}</small></th>{''.join(cells)}</tr>")
    head = "".join(f"<th>{html.escape(t)}</th>" for t in types)
    page = ("<!doctype html><meta charset=utf-8><title>EARS clips</title>"
            "<style>body{font-family:sans-serif}td,th{padding:6px;border-bottom:1px solid #ddd;text-align:left}"
            "small{font-weight:normal;color:#555}</style>"
            "<p>EARS (CC BY-NC 4.0) — Richter et al., Interspeech 2024. Local files, not for redistribution.</p>"
            f"<table><tr><th>speaker</th>{head}</tr>{''.join(rows)}</table>")
    (out / "index.html").write_text(page, encoding="utf-8")
    print(f"index: {out / 'index.html'}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--speakers-info", action="store_true", help="list speakers with their metadata")
    p.add_argument("--list", action="store_true", help="list the WAV files in the chosen speakers' zips")
    p.add_argument("--types", help="comma-separated file types, e.g. emo_fear_sentences")
    p.add_argument("--speakers", help="e.g. 1,2,5-9 (default: all, after the filters)")
    p.add_argument("--gender", choices=["female", "male"])
    p.add_argument("--age", help='an age bracket as in the metadata, e.g. "26-35"')
    p.add_argument("--native", help='a substring of the native language, e.g. "english"')
    p.add_argument("--fetch", action="store_true", help="download; without it, only show what would be fetched")
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = p.parse_args()

    stats = get_json("speaker_statistics.json")
    speakers = filter_speakers(parse_speakers(args.speakers, stats), stats, args)
    if args.speakers_info:
        show_speakers(speakers, stats)
    elif args.list:
        show_types(speakers)
    elif args.types:
        fetch(speakers, [t.strip() for t in args.types.split(",")], args.out, stats, args.fetch)
    else:
        p.print_help()
    print(f"\n[{Stats.requests} requests, {Stats.transferred / 1e6:.3f} MB transferred]")


if __name__ == "__main__":
    main()
