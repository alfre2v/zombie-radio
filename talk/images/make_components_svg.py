from html import escape as e
from pathlib import Path

OUT = Path(__file__).with_name("_components.svg")
ORANGE, GREEN, PURPLE = "#ff8c1a", "#8fd14f", "#b48cff"
TEXT, DIM = "#eeeeee", "#b8b8b8"

def zone(x, y, w, h, color, title, sub):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{color}" fill-opacity="0.07" '
            f'stroke="{color}" stroke-width="3"/>'
            f'<text x="{x+20}" y="{y+34}" fill="{color}" font-size="25" font-weight="700">{e(title)}</text>'
            f'<text x="{x+20}" y="{y+58}" fill="{DIM}" font-size="16">{e(sub)}</text>')

def box(x, y, w, h, color, name, lines, name_size=23, line_size=17):
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#111111" fill-opacity="0.85" '
         f'stroke="{color}" stroke-width="1.5"/>'
         f'<text x="{x+16}" y="{y+32}" fill="{TEXT}" font-size="{name_size}" font-weight="700">{e(name)}</text>')
    for i, line in enumerate(lines):
        s += f'<text x="{x+16}" y="{y+58+i*22}" fill="{DIM}" font-size="{line_size}">{e(line)}</text>'
    return s

def arrow(x1, y, x2, color):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="3" '
            f'marker-start="url(#tip-{color[1:]})" marker-end="url(#tip-{color[1:]})"/>')

def vlabel(x, y, color, text, size=17):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" text-anchor="middle" '
            f'transform="rotate(-90 {x} {y})">{e(text)}</text>')

parts = []
defs = "".join(
    f'<marker id="tip-{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
    f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
    for c in (GREEN, PURPLE))

z1 = [zone(10, 70, 430, 740, ORANGE, "The browser", "the /show page, on the laptop")]
for i, (name, lines) in enumerate([
    ("The looks", ["the 1950 radio, the ham transmitter"]),
    ("The clock", ["show.js asks for one round", "after another"]),
    ("The voice player", ["each line cut into chunks,", "played in order"]),
    ("The microphone", ["hold to talk"]),
    ("The static bed", ["radio static under the voices", "(Web Audio)"]),
]):
    z1.append(box(28, 150 + i * 132, 394, 118, ORANGE, name, lines))

z2 = [zone(540, 70, 530, 740, GREEN, "TalkWithZombies", "FastAPI, Python, on the laptop")]
for i, (name, lines) in enumerate([
    ("The director", ["chooses each round: the mode, the receiver, the mood"]),
    ("The story", ["lab-outbreak: the cast, agenda, beats, events, moods"]),
    ("The GBNF grammar", ["one round, written as a screenplay"]),
    ("The stream parser", ["the reply, line by line, to the page (SSE)"]),
    ("The run's record", ["script.json, the trim, the debug files"]),
    ("The voice proxy", ["each line + the character's clip for its mood"]),
    ("The speech-to-text proxy", ["the listener's words"]),
]):
    z2.append(box(556, 150 + i * 94, 498, 84, GREEN, name, lines, name_size=21, line_size=16))
z2.append(arrow(444, 440, 536, GREEN))
z2.append(vlabel(490, 440, GREEN, "HTTP · 127.0.0.1:8000"))
z2[-1] = z2[-1].replace('x="490" y="440"', 'x="490" y="300"', 1).replace('rotate(-90 490 440)', 'rotate(-90 490 300)', 1)

z3 = [zone(1160, 70, 430, 740, PURPLE, "The GPU box", "A6000 (Hyperstack) or 3090 (home)")]
z3.append(f'<text x="1180" y="150" fill="{DIM}" font-size="16">Ubuntu · Docker · NVIDIA</text>')
z3.append(box(1176, 170, 398, 120, PURPLE, "llama.cpp  :8080",
              ["Nemotron Nano 9B v2 (Q4_K_M)", "a 32k context"]))
z3.append(box(1176, 620, 398, 84, PURPLE, "tts-serve 1.2  :8001", ["Faster Qwen3-TTS"], name_size=21, line_size=16))
z3.append(box(1176, 714, 398, 84, PURPLE, "Whisper small  :8002", ["speech to text"], name_size=21, line_size=16))
z3.append(f'<text x="1375" y="430" fill="{DIM}" font-size="17" text-anchor="middle">one GPU, the whole stack:</text>')
z3.append(f'<text x="1375" y="458" fill="{TEXT}" font-size="22" font-weight="700" text-anchor="middle">'
          f'14,477 MiB</text>')
for y in (192, 662, 756):
    z3.append(arrow(1056, y, 1174, PURPLE))
z3.append(vlabel(1115, 440, PURPLE, "SSH tunnel · localhost :8080 :8001 :8002"))

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 60 1600 760" width="100%" '
       f'style="font-family: \'Open Sans\', Helvetica, Arial, sans-serif" role="img" '
       f'aria-label="The components of Zombie-Radio: the browser, TalkWithZombies, the GPU box">'
       f'<defs>{defs}</defs>'
       f'<g class="fragment" data-fragment-index="1">{"".join(z1)}</g>'
       f'<g class="fragment" data-fragment-index="2">{"".join(z2)}</g>'
       f'<g class="fragment" data-fragment-index="3">{"".join(z3)}</g>'
       f'</svg>')
svg = svg.replace("><", ">\n<")
OUT.write_text(svg + "\n")
print(OUT)
