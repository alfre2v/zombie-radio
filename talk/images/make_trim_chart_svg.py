import csv
import json
from pathlib import Path

RUN = "2026-10-01T17-48-37"
HERE = Path(__file__).parent
DATA = HERE.parent / "data" / f"trim-run-{RUN}.csv"
SOURCE = HERE.parents[2] / "TalkWithZombies" / "runs" / RUN / "script.json"
OUT = HERE / "_trim_chart.svg"
BUDGET, TRIGGER, TARGET, N_CTX = 34000, 0.9, 0.5, 32768
TEXT, DIM, GRID = "#eeeeee", "#b8b8b8", "#3a3a3a"
ORANGE, GREEN, RED, LINE = "#ff8c1a", "#8fd14f", "#d42a2a", "#b48cff"

if SOURCE.exists():
    rows = []
    for r in json.loads(SOURCE.read_text())["rounds"]:
        t = r.get("timings") or {}
        read = (t.get("prompt_n") or 0) + (t.get("cache_n") or 0)
        if read:
            rows.append((r["n"], read, 1 if r.get("trims") else 0))
    with DATA.open("w", newline="") as f:
        csv.writer(f).writerows([("round", "tokens_read", "trimmed_before")] + rows)
with DATA.open() as f:
    rows = [(int(n), int(t), int(x)) for n, t, x in list(csv.reader(f))[1:]]

X0, X1, Y0, Y1 = 110, 1560, 560, 40
last = rows[-1][0]
ymax = 35000


def x(n):
    return X0 + (X1 - X0) * (n - 1) / (last - 1)


def y(v):
    return Y0 - (Y0 - Y1) * v / ymax


parts = []
for v in range(0, ymax + 1, 5000):
    parts.append(f'<line x1="{X0}" y1="{y(v):.1f}" x2="{X1}" y2="{y(v):.1f}" stroke="{GRID}" stroke-width="1"/>')
    parts.append(f'<text x="{X0 - 12}" y="{y(v) + 6:.1f}" fill="{DIM}" font-size="17" text-anchor="end">'
                 f'{v:,}</text>')
for n in range(50, last + 1, 50):
    parts.append(f'<text x="{x(n):.1f}" y="{Y0 + 28}" fill="{DIM}" font-size="17" text-anchor="middle">{n}</text>')
parts.append(f'<text x="{(X0 + X1) / 2}" y="{Y0 + 58}" fill="{DIM}" font-size="18" text-anchor="middle">round</text>')
parts.append(f'<text x="30" y="{(Y0 + Y1) / 2}" fill="{DIM}" font-size="18" text-anchor="middle" '
             f'transform="rotate(-90 30 {(Y0 + Y1) / 2})">tokens the model read</text>')

for value, color, label in [(N_CTX, RED, f"the model's context: {N_CTX:,}"),
                            (BUDGET * TRIGGER, ORANGE, f"the trim fires: {BUDGET * TRIGGER:,.0f} (90 %)"),
                            (BUDGET * TARGET, GREEN, f"and cuts down to: {BUDGET * TARGET:,.0f} (50 %)")]:
    parts.append(f'<line x1="{X0}" y1="{y(value):.1f}" x2="{X1}" y2="{y(value):.1f}" stroke="{color}" '
                 f'stroke-width="2" stroke-dasharray="10 7"/>')
    dy = -10 if value != BUDGET * TRIGGER else 24
    parts.append(f'<text x="{X0 + 14}" y="{y(value) + dy:.1f}" fill="{color}" font-size="18">{label}</text>')

points = " ".join(f"{x(n):.1f},{y(t):.1f}" for n, t, _ in rows)
parts.append(f'<polyline points="{points}" fill="none" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/>')
for n, t, trimmed in rows:
    if trimmed:
        parts.append(f'<circle cx="{x(n):.1f}" cy="{y(t):.1f}" r="7" fill="{GREEN}"/>')
        parts.append(f'<text x="{x(n) + 12:.1f}" y="{y(t) + 30:.1f}" fill="{TEXT}" font-size="18">'
                     f'trim, round {n}</text>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 640" width="100%" '
       f'style="font-family: \'Open Sans\', Helvetica, Arial, sans-serif" role="img" '
       f'aria-label="The context of run {RUN}: tokens read per round, with two trims">' + "".join(parts) + "</svg>")
OUT.write_text(svg.replace("><", ">\n<") + "\n")
print(OUT, len(rows), "rounds")
