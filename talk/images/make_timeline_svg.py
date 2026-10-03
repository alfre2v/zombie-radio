from html import escape as e
from pathlib import Path

OUT = Path(__file__).with_name("_timeline.svg")
ORANGE, GREEN, PURPLE, GREY = "#ff8c1a", "#8fd14f", "#b48cff", "#9a9a9a"
TEXT, DIM, BLOOD = "#eeeeee", "#b8b8b8", "#d42a2a"

EVENTS = [
    ("Oct 2024", "zombie_radio_ai", ["a hackathon, by hand,", "in a couple of days,", "no AI assistant:", "the show's first ideas"], GREY),
    ("Jul 2026", "TalkWithMe", ["scorbo2's chat app:", "“Functional V1", "written by Qwen”"], GREY),
    ("Sep 12", "zombie-radio", ["starts: the docs", "come first"], ORANGE),
    ("Sep 23", "the fork", ["TalkWithZombies", "tz-0.1"], GREEN),
    ("Sep 28", "the show engine", ["and the looks", "tz-0.2 · tz-0.3"], GREEN),
    ("Sep 30", "voices with", ["emotions", "tz-0.4"], GREEN),
    ("Oct 1", "a 32k context", ["tz-0.5"], GREEN),
    ("Oct 2", "radio static", ["tz-0.6"], GREEN),
    ("Oct 14", "this talk", ["Austin Python", "Meetup"], BLOOD),
]


def text(x, y, s, size, fill, weight=400):
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="middle">{e(s)}</text>')


AXIS = 290
xs = [110 + i * 172.5 for i in range(len(EVENTS))]
parts = [f'<line x1="40" y1="{AXIS}" x2="1560" y2="{AXIS}" stroke="{DIM}" stroke-width="3"/>']
gap = (xs[0] + xs[1]) / 2
parts.append(f'<rect x="{gap - 26}" y="{AXIS - 14}" width="52" height="28" fill="#191919"/>')
parts.append(f'<path d="M{gap - 26},{AXIS} l9,-12 l9,24 l9,-24 l9,24 l9,-24 l7,12" fill="none" '
             f'stroke="{DIM}" stroke-width="3"/>')
parts.append(text(gap, AXIS + 48, "almost two years", 17, DIM))
for i, ((when, name, lines, color), x) in enumerate(zip(EVENTS, xs)):
    up = i % 2 == 0
    parts.append(f'<circle cx="{x}" cy="{AXIS}" r="11" fill="{color}"/>')
    tick_end = AXIS - 46 if up else AXIS + 46
    parts.append(f'<line x1="{x}" y1="{AXIS}" x2="{x}" y2="{tick_end}" stroke="{color}" stroke-width="2"/>')
    top = AXIS - 222 if up else AXIS + 80
    parts.append(text(x, top, when, 22, color, 700))
    parts.append(text(x, top + 32, name, 21, TEXT, 700))
    for j, line in enumerate(lines):
        parts.append(text(x, top + 60 + j * 24, line, 17, DIM))

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 30 1600 520" width="100%" '
       f'style="font-family: \'Open Sans\', Helvetica, Arial, sans-serif" role="img" '
       f'aria-label="How the project came to be: from a 2024 hackathon to this talk">'
       + "".join(parts) + "</svg>")
OUT.write_text(svg.replace("><", ">\n<") + "\n")
print(OUT)
