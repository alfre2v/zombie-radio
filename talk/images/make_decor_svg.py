import math
from pathlib import Path

HERE = Path(__file__).parent


def spiderweb():
    grey = "#a8a8a8"
    radials = [math.radians(a) for a in (0, 15, 32, 48, 63, 78, 90)]
    length = 300
    parts = []
    for a in radials:
        parts.append(f'<line x1="300" y1="0" x2="{300 - length * math.cos(a):.1f}" y2="{length * math.sin(a):.1f}" '
                     f'stroke="{grey}" stroke-width="1.3"/>')
    for r in (45, 85, 130, 180, 235):
        for a1, a2 in zip(radials, radials[1:]):
            p1 = (300 - r * math.cos(a1), r * math.sin(a1))
            p2 = (300 - r * math.cos(a2), r * math.sin(a2))
            mid = (a1 + a2) / 2
            sag = r * 0.85
            c = (300 - sag * math.cos(mid), sag * math.sin(mid))
            parts.append(f'<path d="M{p1[0]:.1f},{p1[1]:.1f} Q{c[0]:.1f},{c[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" '
                         f'fill="none" stroke="{grey}" stroke-width="1"/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300" opacity="0.55">'
            + "".join(parts) + "</svg>")


for name, svg in [("_spiderweb.svg", spiderweb())]:
    (HERE / name).write_text(svg.replace("><", ">\n<") + "\n")
    print(HERE / name)
