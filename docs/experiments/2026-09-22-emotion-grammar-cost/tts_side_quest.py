"""Side quest: does tts-serve pronounce typographic punctuation the same as plain ASCII?

Stdlib only. Synthesizes three pairs of lines that differ ONLY in one character
(’ versus ', — versus a comma, … versus ...), same voice and seed, through the tunnel
(localhost:8001), and writes the WAV files to --out for listening.

usage: python3 tts_side_quest.py --out <folder>
"""
import argparse
import base64
import json
import pathlib
import urllib.request

VOICE = pathlib.Path("/Users/alfredo/TalkWithMe-client/Personas/Samantha")
PAIRS = [
    ("apostrophe", "It’s heading northeast. If it’s military, they might know more. Over.",
                   "It's heading northeast. If it's military, they might know more. Over."),
    ("dash", "East wing lights flickering—could be a power surge or something worse. Over.",
             "East wing lights flickering, could be a power surge or something worse. Over."),
    ("ellipsis", "Wait… did you hear that? Over.",
                 "Wait... did you hear that? Over."),
]


def synthesize(url, text, audio_b64, reference_text, seed):
    body = {"text": text, "audio_base64": audio_b64, "reference_text": reference_text,
            "language": "en", "seed": seed}
    request = urllib.request.Request(url, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=300) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--url", default="http://localhost:8001/synthesize")
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    audio_b64 = base64.b64encode((VOICE / "ref.wav").read_bytes()).decode()
    reference_text = (VOICE / "ref.txt").read_text().strip()
    for name, typographic, ascii_text in PAIRS:
        for variant, text in (("typographic", typographic), ("ascii", ascii_text)):
            result = synthesize(args.url, text, audio_b64, reference_text, args.seed)
            path = out / f"{name}-{variant}.wav"
            path.write_bytes(base64.b64decode(result["audio_base64"]))
            print(f"{path.name:28} seed={result.get('seed')} time_used={result.get('time_used')} "
                  f"rtf={result.get('rtf')}  text={text!r}", flush=True)


if __name__ == "__main__":
    main()
