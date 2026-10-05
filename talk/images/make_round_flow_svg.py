from html import escape as e
from pathlib import Path

OUT = Path(__file__).with_name("_round_flow.svg")
ORANGE, GREEN, PURPLE = "#ff8c1a", "#8fd14f", "#b48cff"
TEXT, DIM = "#eeeeee", "#b8b8b8"
W, H = 340, 128


def step(x, y, color, n, name, line1, line2=""):
    s = (f'<rect x="{x}" y="{y}" width="{W}" height="{H}" rx="12" fill="{color}" fill-opacity="0.10" '
         f'stroke="{color}" stroke-width="2.5"/>'
         f'<circle cx="{x + 30}" cy="{y + 32}" r="17" fill="{color}"/>'
         f'<text x="{x + 30}" y="{y + 39}" fill="#111" font-size="20" font-weight="700" text-anchor="middle">{n}</text>'
         f'<text x="{x + 58}" y="{y + 40}" fill="{TEXT}" font-size="22" font-weight="700">{e(name)}</text>'
         f'<text x="{x + 18}" y="{y + 78}" fill="{DIM}" font-size="17">{e(line1)}</text>')
    if line2:
        s += f'<text x="{x + 18}" y="{y + 102}" fill="{DIM}" font-size="17">{e(line2)}</text>'
    return s


def arrow(x1, y1, x2, y2, color=DIM):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="3" '
            f'marker-end="url(#tip)"/>')


XS = [40, 430, 820, 1210]
R1, R2, R3 = 40, 250, 500
parts = ['<defs><marker id="tip" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
         f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{DIM}"/></marker></defs>',
         step(XS[0], R1, ORANGE, 1, "The page asks", "for the next round:", "the browser is the clock"),
         step(XS[1], R1, GREEN, 2, "The director plans", "mode, speakers, moods,", "line budget — plain Python"),
         step(XS[2], R1, GREEN, 3, "Prompt + grammar", "the script so far, the", "instruction, a GBNF grammar"),
         step(XS[3], R1, PURPLE, 4, "llama.cpp writes", "Nemotron Nano 9B v2,", "streamed token by token"),
         step(XS[3], R2, GREEN, 5, "The parser cuts lines", "line by line to the page,", "as server-sent events"),
         step(XS[2], R2, PURPLE, 6, "tts-serve speaks", "each line, with the clip", "of the line's mood"),
         step(XS[1], R2, ORANGE, 7, "The page plays it", "the static bed under it;", "then asks again"),
         f'<text x="{XS[0] + W / 2}" y="{R2 + 58}" fill="{TEXT}" font-size="22" font-weight="700" '
         f'text-anchor="middle">next round</text>',
         f'<text x="{XS[0] + W / 2}" y="{R2 + 86}" fill="{DIM}" font-size="17" text-anchor="middle">'
         f'back to 1, until Stop</text>']
for a, b in zip(XS, XS[1:]):
    parts.append(arrow(a + W + 4, R1 + H / 2, b - 6, R1 + H / 2))
parts.append(arrow(XS[3] + W / 2, R1 + H + 4, XS[3] + W / 2, R2 - 6))
for a, b in [(XS[3], XS[2]), (XS[2], XS[1]), (XS[1], XS[0])]:
    parts.append(arrow(a - 4, R2 + H / 2, b + W + 6, R2 + H / 2))
parts.append(arrow(XS[0] + W / 2, R2 - 4, XS[0] + W / 2, R1 + H + 6))

parts.append(f'<text x="40" y="{R3 - 22}" fill="{TEXT}" font-size="22" font-weight="700">'
             f'When the radio listens:</text>')
parts += [step(XS[1], R3, ORANGE, "A", "Hold Space", "the listener talks;", "the page records"),
          step(XS[2], R3, PURPLE, "B", "Whisper", "turns the recording", "into words"),
          step(XS[3], R3, GREEN, "C", "The director", "plans the answer:", "an exchange, or a re-call")]
parts.append(arrow(XS[1] + W + 4, R3 + H / 2, XS[2] - 6, R3 + H / 2))
parts.append(arrow(XS[2] + W + 4, R3 + H / 2, XS[3] - 6, R3 + H / 2))

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 20 1600 640" width="100%" '
       f'style="font-family: \'Open Sans\', Helvetica, Arial, sans-serif" role="img" '
       f'aria-label="One round of the show, end to end">' + "".join(parts) + "</svg>")
OUT.write_text(svg.replace("><", ">\n<") + "\n")
print(OUT)
