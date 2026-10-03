import math
import random
from pathlib import Path

HERE = Path(__file__).parent


def zombie(x, base, s, grey, lean, stride):
    head_r = 7 * s
    hip = (x, base - 30 * s)
    neck = (x + lean * s, base - 58 * s)
    head = (neck[0] + 4 * s, neck[1] - head_r - 2 * s)
    shoulder = (neck[0] - 1 * s, neck[1] + 4 * s)
    hand1 = (shoulder[0] + 24 * s, shoulder[1] + 2 * s)
    hand2 = (shoulder[0] + 21 * s, shoulder[1] + 7 * s)
    foot1 = (x + stride * s, base)
    foot2 = (x - stride * s * 0.7, base)
    knee1 = (x + stride * s * 0.6, base - 15 * s)
    knee2 = (x - stride * s * 0.2, base - 14 * s)
    w = 3.2 * s

    def line(a, b, width):
        return (f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{grey}" '
                f'stroke-width="{width:.1f}" stroke-linecap="round"/>')

    torso = (f'<path d="M{hip[0] - 5 * s:.1f},{hip[1]:.1f} L{neck[0] - 6 * s:.1f},{neck[1]:.1f} '
             f'L{neck[0] + 6 * s:.1f},{neck[1] + 2 * s:.1f} L{hip[0] + 5 * s:.1f},{hip[1]:.1f} Z" fill="{grey}"/>')
    return "".join([
        line(hip, knee2, w), line(knee2, foot2, w), torso,
        line(hip, knee1, w), line(knee1, foot1, w),
        line(shoulder, hand2, w * 0.8), line(shoulder, hand1, w * 0.8),
        f'<circle cx="{head[0]:.1f}" cy="{head[1]:.1f}" r="{head_r:.1f}" fill="{grey}"/>',
    ])


def zombies():
    rng = random.Random(1938)
    rows = [(0.55, "#2c2c2c", 14), (0.8, "#3a3a3a", 9), (1.05, "#4a4a4a", 6)]
    parts = ['<defs><linearGradient id="fog" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#191919" stop-opacity="0"/>'
             '<stop offset="1" stop-color="#5a5a5a" stop-opacity="0.35"/></linearGradient></defs>',
             '<rect x="0" y="40" width="1600" height="80" fill="url(#fog)"/>']
    for depth, (s, grey, count) in enumerate(rows):
        base = 96 + depth * 10
        for i in range(count):
            x = (i + rng.uniform(0.1, 0.9)) * 1600 / count
            parts.append(zombie(x, base, s, grey, rng.uniform(4, 9), rng.uniform(6, 11)))
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 120">' + "".join(parts) + "</svg>"


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


for name, svg in [("_zombies.svg", zombies()), ("_spiderweb.svg", spiderweb())]:
    (HERE / name).write_text(svg.replace("><", ">\n<") + "\n")
    print(HERE / name)
