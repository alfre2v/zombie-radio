from html import escape as e
from pathlib import Path

OUT = Path(__file__).with_name("_machines.svg")
ORANGE, GREEN, PURPLE = "#ff8c1a", "#8fd14f", "#b48cff"
TEXT, DIM, FRAME = "#eeeeee", "#b8b8b8", "#d0d0d0"
MONO = "font-family=\"'JetBrains Mono', Menlo, Consolas, monospace\""


def text(x, y, s, size=18, fill=TEXT, weight=400, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" {extra}>{e(s)}</text>')


def card(x, y, w, h, color, name, line, name_size=24, line_size=18):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{color}" fill-opacity="0.10" '
            f'stroke="{color}" stroke-width="2.5"/>'
            + text(x + 18, y + 36, name, name_size, color, 700)
            + text(x + 18, y + 64, line, line_size, DIM))


def link(x1, x2, y, color, dash, width, both=True):
    start = f' marker-start="url(#tip-{color[1:]})"' if both else ""
    return (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="{width}" '
            f'stroke-dasharray="{dash}"{start} marker-end="url(#tip-{color[1:]})"/>')


parts = [
    "<defs>" + "".join(
        f'<marker id="tip-{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
        f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
        for c in (PURPLE, FRAME)) + "</defs>",
    f'<rect x="90" y="40" width="460" height="320" rx="16" fill="#0c0c0c" stroke="{FRAME}" stroke-width="4"/>',
    card(118, 72, 404, 120, ORANGE, "The browser", "the /show page: the show you hear"),
    card(118, 210, 404, 120, GREEN, "TalkWithZombies", "FastAPI, Python · 127.0.0.1:8000"),
    f'<polygon points="60,366 580,366 620,400 20,400" fill="#2a2a2a" stroke="{FRAME}" stroke-width="3"/>',
    text(320, 444, "The laptop", 28, TEXT, 700, "middle"),
    text(320, 474, "the client: macOS", 18, DIM, 400, "middle"),
    f'<rect x="40" y="510" width="560" height="200" rx="12" fill="#151515" stroke="#555555" stroke-width="1.5"/>',
    text(64, 548, "From the laptop, one command each:", 19, DIM),
    text(64, 596, "make client-mac", 24, GREEN, 700, extra=MONO),
    text(64, 626, "installs TalkWithZombies on the laptop", 18, DIM),
    text(64, 670, "make ans-deploy ENV=cloud", 24, PURPLE, 700, extra=MONO),
    text(64, 700, "deploys the AI to the GPU box", 18, DIM),

    link(604, 1056, 150, PURPLE, "10 8", 3, both=False),
    text(830, 132, "make ans-deploy · Ansible over SSH", 20, PURPLE, 700, "middle"),
    text(830, 180, "once: about 7 minutes from a fresh VM", 17, DIM, 400, "middle"),
    link(604, 1056, 300, FRAME, "4 8", 5),
    text(830, 282, "SSH tunnel · during the show", 20, TEXT, 700, "middle"),
    text(830, 332, "localhost :8080  :8001  :8002", 18, DIM, 400, "middle", MONO),
    text(830, 380, "over the internet", 17, DIM, 400, "middle", 'font-style="italic"'),

    f'<rect x="1060" y="40" width="500" height="420" rx="16" fill="{PURPLE}" fill-opacity="0.07" '
    f'stroke="{PURPLE}" stroke-width="4"/>',
    text(1084, 80, "The GPU box: a VM on Hyperstack", 26, PURPLE, 700),
    text(1084, 108, "NVIDIA RTX A6000 (48 GB) · Ubuntu · Docker", 18, DIM),
    card(1084, 128, 452, 96, PURPLE, "llama.cpp", "the language model: Nemotron Nano 9B v2"),
    card(1084, 236, 452, 96, PURPLE, "tts-serve", "the voices: Faster Qwen3-TTS"),
    card(1084, 344, 452, 96, PURPLE, "Whisper", "the listener's ears: speech to text"),

    f'<rect x="1060" y="510" width="500" height="200" rx="16" fill="none" stroke="{PURPLE}" stroke-width="2.5" '
    f'stroke-dasharray="12 8"/>',
    text(1084, 556, "or: a home lab PC", 26, PURPLE, 700),
    text(1084, 590, "NVIDIA RTX 3090 (24 GB) · Ubuntu · Docker", 18, DIM),
    text(1084, 640, "the same three services,", 19, TEXT),
    text(1084, 668, "deployed by the same playbook", 19, TEXT),
]

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 20 1600 710" width="100%" '
       f'style="font-family: \'Open Sans\', Helvetica, Arial, sans-serif" role="img" '
       f'aria-label="The machines: the laptop, the SSH tunnel, and the GPU box">'
       + "".join(parts) + "</svg>")
svg = svg.replace("><", ">\n<")
OUT.write_text(svg + "\n")
print(OUT)
