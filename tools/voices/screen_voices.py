"""Screen EARS speakers before casting them: does each recording say its transcript, and stay in the speaker's range?

For each speaker and read emotion, the clip is transcribed by the box's Whisper (through the SSH tunnel) and compared
word by word with its transcript. Words heard before or after the transcript are stray speech: an aside, a restart,
another passage. A weak match is paraphrase or garbling. Both mislead the voice engine, which clones from the clip and
its transcript together. Each clip's pitch (a rough median of its voiced frames) is compared with the speaker's
neutral clip: a large climb, such as a man's voice rising into a woman's range when afraid, can make the cloned voice
drift. Standard library only; the clips must be downloaded first (fetch_ears.py).

  python3 tools/voices/screen_voices.py --speakers 85,54,88
  python3 tools/voices/screen_voices.py --speakers 7 --emotions distress,fear,anger

Prints a table and each flagged clip; writes screen-<start time>.json (everything) and a page of players for the
flagged clips, screen-<start time>.html, next to the clips.
"""

import argparse
import array
import difflib
import html
import json
import re
import statistics
import subprocess
import sys
import tempfile
import urllib.request
import uuid
import wave
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = REPO.parent / "zombie-radio-datasets" / "ears"
EMOTION = re.compile(r"emo_(?P<emotion>[a-z]+)_sentences")
SAME = [
    (r"\bi'm\b", "i am"), (r"\bwhat's\b", "what is"), (r"\bthat's\b", "that is"), (r"\bthere's\b", "there is"),
    (r"\bit's\b", "it is"), (r"\bwe're\b", "we are"), (r"\byou're\b", "you are"), (r"\bthey're\b", "they are"),
    (r"\bi've\b", "i have"), (r"\bi'll\b", "i will"), (r"\bdon't\b", "do not"), (r"\bcan't\b", "can not"),
    (r"\bisn't\b", "is not"), (r"\bdidn't\b", "did not"), (r"\bgonna\b", "going to"), (r"\bwanna\b", "want to"),
    (r"\b(\d+)\s*p\.?\s*m\b\.?", r"\1 pm"), (r"\b(\d+)\s*a\.?\s*m\b\.?", r"\1 am"), (r"(\d+)\s*%", r"\1 percent"),
]


def words(text):
    text = text.lower().replace("’", "'")
    for pattern, repl in SAME:
        text = re.sub(pattern, repl, text)
    return re.findall(r"[a-z0-9']+", text)


def parse_speakers(spec):
    chosen = []
    for part in spec.split(","):
        lo, _, hi = part.strip().lower().lstrip("p").partition("-")
        chosen += [f"p{n:03d}" for n in range(int(lo), int(hi or lo) + 1)]
    return chosen


def transcribe(url, wav_bytes):
    b = uuid.uuid4().hex
    fields = [f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
              for k, v in (("response_format", "json"), ("language", "en"))]
    head = (f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="audio.wav"\r\n'
            "Content-Type: audio/wav\r\n\r\n").encode()
    body = b"".join(fields) + head + wav_bytes + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request(f"{url}/v1/audio/transcriptions", data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={b}"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read())["text"]


def pitch(path):
    w = wave.open(str(path))
    rate = w.getframerate()
    data = array.array("h", w.readframes(w.getnframes()))
    step = rate // 4000
    x = [float(v) for v in data[::step]]
    sr = rate // step
    win, hop, lo, hi = int(0.05 * sr), int(0.025 * sr), sr // 400, sr // 60
    frames = list(range(0, len(x) - win - hi, hop))
    energy = [sum(v * v for v in x[i:i + win]) for i in frames]
    gate = sorted(energy)[len(energy) // 2] if energy else 0
    found = []
    for k, i in enumerate(frames):
        if energy[k] < gate or not energy[k]:
            continue
        best, lag = 0.0, 0
        for L in range(lo, hi):
            c = sum(x[i + j] * x[i + j + L] for j in range(win))
            if c > best:
                best, lag = c, L
        if lag and best / energy[k] > 0.5:
            found.append(sr / lag)
    return statistics.median(found) if found else None


def compare(want, heard):
    a, h = words(want), words(heard)
    sm = difflib.SequenceMatcher(a=a, b=h, autojunk=False)
    blocks = [m for m in sm.get_matching_blocks() if m.size]
    before = blocks[0].b if blocks else len(h)
    after = len(h) - (blocks[-1].b + blocks[-1].size) if blocks else 0
    return round(sm.ratio(), 3), before, after


def screen(speaker, src, emotions, args, tmp):
    rows = []
    available = sorted(m["emotion"] for m in (EMOTION.fullmatch(p.stem) for p in src.glob("emo_*_sentences.wav"))
                       if m and (src / f"{m.string}.txt").exists())
    for emotion in [e for e in (emotions or available) if e in available]:
        wav = src / f"emo_{emotion}_sentences.wav"
        small = Path(tmp) / f"{speaker}-{emotion}.wav"
        subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16@16000", "-c", "1", str(wav), str(small)], check=True)
        want = wav.with_suffix(".txt").read_text(encoding="utf-8").strip()
        heard = " ".join(transcribe(args.whisper, small.read_bytes()).split())
        match, before, after = compare(want, heard)
        rows.append({"speaker": speaker, "emotion": emotion, "match": match, "extra_before": before,
                     "extra_after": after, "pitch_hz": pitch(small), "transcript": want, "heard": heard})
    neutral = next((r["pitch_hz"] for r in rows if r["emotion"] == "neutral"), None)
    for r in rows:
        r["pitch_rise"] = round(r["pitch_hz"] / neutral, 2) if neutral and r["pitch_hz"] else None
        r["flags"] = [f for f, on in (
            ("stray speech", r["extra_before"] >= args.extra_words or r["extra_after"] >= args.extra_words),
            ("weak match", r["match"] < args.min_match),
            ("pitch climbs", (r["pitch_rise"] or 0) > args.pitch_rise),
        ) if on]
    missing = [e for e in (emotions or []) if e not in available]
    return rows, missing


def marked(r):
    h = r["heard"].split(" ")
    b, a = r["extra_before"], r["extra_after"]
    middle = h[b:len(h) - a] if a else h[b:]
    return ((f"<mark>{html.escape(' '.join(h[:b]))}</mark> " if b else "") + html.escape(" ".join(middle))
            + (f" <mark>{html.escape(' '.join(h[len(h) - a:]))}</mark>" if a else ""))


def write_page(path, rows, started):
    flagged = [r for r in rows if r["flags"]]
    cells = "".join(
        f"<tr><th>{r['speaker']} {r['emotion']}<br><small>{', '.join(r['flags'])}; match {r['match']:.2f}"
        + (f"; pitch {r['pitch_hz']:.0f} Hz, x{r['pitch_rise']:.2f} of neutral" if r["pitch_rise"] else "")
        + f"</small></th><td><audio controls preload=none src='{r['speaker']}/emo_{r['emotion']}_sentences.wav'>"
        f"</audio></td><td><b>Transcript:</b> {html.escape(r['transcript'])}<br><b>Whisper heard:</b> {marked(r)}"
        "</td></tr>" for r in flagged)
    path.write_text(
        "<!doctype html><meta charset=utf-8><title>Voice screening</title><style>body{font-family:sans-serif;"
        "margin:24px}td,th{padding:8px;border-bottom:1px solid #ddd;text-align:left;vertical-align:top}"
        "small{color:#666;font-weight:normal}mark{background:#ffe08a}</style>"
        f"<h2>Voice screening, {started:%Y-%m-%d %H:%M}: {len(flagged)} flagged of {len(rows)} clips</h2>"
        "<p>Highlighted: words Whisper heard that the transcript does not have. EARS (CC BY-NC 4.0) - local files, "
        f"not for redistribution.</p><table>{cells}</table>", encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--speakers", required=True, help="e.g. 85,54 or 80-89")
    p.add_argument("--emotions", help="comma-separated, e.g. fear,distress (default: every read emotion downloaded)")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--whisper", default="http://localhost:8002", help="the Whisper service, through the tunnel")
    p.add_argument("--extra-words", type=int, default=2, help="words before or after the transcript that flag it")
    p.add_argument("--min-match", type=float, default=0.80, help="a word match below this flags the clip")
    p.add_argument("--pitch-rise", type=float, default=1.5, help="a pitch above this times the neutral flags it")
    args = p.parse_args()

    started = datetime.now()
    emotions = [e.strip() for e in args.emotions.split(",")] if args.emotions else None
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        for speaker in parse_speakers(args.speakers):
            src = args.source / speaker
            if not src.is_dir():
                print(f"{speaker}: not downloaded (fetch it with fetch_ears.py)")
                continue
            found, missing = screen(speaker, src, emotions, args, tmp)
            rows += found
            flagged = [r for r in found if r["flags"]]
            neutral = next((r["pitch_hz"] for r in found if r["emotion"] == "neutral"), None)
            highest = max((r["pitch_hz"] for r in found if r["pitch_hz"]), default=None)
            print(f"{speaker}: {len(found)} clips, {len(flagged)} flagged"
                  + (f"; pitch neutral {neutral:.0f} Hz, highest {highest:.0f} Hz" if neutral and highest else "")
                  + (f"; not downloaded: {', '.join(missing)}" if missing else ""), flush=True)
            for r in flagged:
                print(f"   {r['emotion']:13} {', '.join(r['flags'])}: match {r['match']:.2f}, "
                      f"extra {r['extra_before']} before / {r['extra_after']} after"
                      + (f", pitch x{r['pitch_rise']:.2f}" if r["pitch_rise"] else ""))
                print(f"      heard: {r['heard'][:150]}")
    if not rows:
        sys.exit("nothing screened")
    stamp = f"{started:%Y-%m-%dT%H:%M:%S}"
    report = args.source / f"screen-{stamp}.json"
    report.write_text(json.dumps(rows, indent=1), encoding="utf-8")
    page = args.source / f"screen-{stamp}.html"
    write_page(page, rows, started)
    print(f"\n{sum(1 for r in rows if r['flags'])} flagged of {len(rows)} clips\nreport: {report}\npage: {page}")


if __name__ == "__main__":
    main()
