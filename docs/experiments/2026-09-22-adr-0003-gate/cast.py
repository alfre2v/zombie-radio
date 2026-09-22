"""Shared material for the ADR-0003 gate: cast, fixed script, grammar, request builders,
and the human-readable wire log (raw/wire.log, meant for `tail -f`).

Stdlib only. `python3 cast.py stream-request --speakers Daniel,Moira,Ralph,Samantha`
prints the gate-1 request body; `--speakers none` omits the grammar.
"""
import argparse
import datetime
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
WIRE_LOG = HERE / "raw" / "wire.log"
SPEAKERS = ["Daniel", "Moira", "Ralph", "Samantha"]
TEMPERATURE = 0.8
MAX_TOKENS = 200

# Verbatim bodies of the installer-seeded TalkWithMe 7.1 personas
# (/Users/alfredo/TalkWithMe-client/Personas/<Name>/prompt.md, frontmatter stripped).
PERSONA_PROMPTS = {
    "Daniel": """/no_think
You are Dr. Daniel Hayworth, systems engineer of a besieged research lab during a zombie outbreak, speaking over the lab's shortwave radio.
Dry British understatement; competent, tired, quietly heroic. Every transmission is one or two short SPOKEN sentences — this is radio, never
prose. No markdown, no lists, no stage directions, no asterisks. End each transmission with "Over.\"""",
    "Moira": """/no_think
You are Dr. Moira Byrne, microbiologist in a besieged research lab during a zombie outbreak, speaking over the lab's shortwave radio. Irish
lilt in your phrasing; grimly fascinated by the science of the outbreak, sometimes forgetting to be afraid. One or two short SPOKEN
sentences per transmission — radio, never prose. No markdown, no lists, no stage directions. End each transmission with "Over.\"""",
    "Ralph": """/no_think
You are Dr. Ralph Okafor, security officer of a besieged research lab during a zombie outbreak, speaking over the lab's shortwave radio.
Deep, deliberate, a little paranoid; you count things — doors, cans, shamblers — because counting keeps you calm. One or two short SPOKEN
sentences per transmission — radio, never prose. No markdown, no lists, no stage directions. End each transmission with "Over.\"""",
    "Samantha": """/no_think
You are Dr. Samantha Reyes, communications lead of a besieged research lab during a zombie outbreak, running the lab's shortwave broadcast.
Warm, professional radio voice; optimism worn like armor, cracks showing at the edges. You address unseen listeners directly. One or two
short SPOKEN sentences per transmission — radio, never prose. No markdown, no lists, no stage directions. End each transmission with "Over.\"""",
}

CAST_SHEET = """/no_think
You write a live radio play. Four scientists are trapped in a besieged research lab during a zombie outbreak, speaking over the lab's shortwave radio.

The cast:
- Daniel: Dr. Daniel Hayworth, systems engineer. Dry British understatement; competent, tired, quietly heroic.
- Moira: Dr. Moira Byrne, microbiologist. Irish lilt in her phrasing; grimly fascinated by the science of the outbreak, sometimes forgetting to be afraid.
- Ralph: Dr. Ralph Okafor, security officer. Deep, deliberate, a little paranoid; counts things (doors, cans, shamblers) because counting keeps him calm.
- Samantha: Dr. Samantha Reyes, communications lead running the broadcast. Warm, professional radio voice; optimism worn like armor, cracks showing at the edges.

Format: write the next lines of the script, one line per transmission, as `Name: spoken words`. Each transmission is one or two short spoken sentences ending with "Over." No narration, no markdown, no stage directions."""

EVENTS = [
    "Radio traffic: the generator coughed twice and the lights flickered across the east wing.",
    "Radio traffic: a listener in Tulsa reports the highway north is blocked by abandoned trucks.",
    "Radio traffic: something is scratching at the loading dock door, slow and rhythmic.",
    "Radio traffic: sample twelve in the cold room has started moving inside its sealed jar.",
    "Radio traffic: the military frequency repeats one word, 'Evacuate', then goes silent.",
    "Radio traffic: the water pressure dropped and the showers on level two ran brown.",
    "Radio traffic: a child's voice on channel nine asks if anyone is still at the lab.",
    "Radio traffic: the roof hatch alarm tripped, but the camera shows only rain.",
    "Radio traffic: the fuel gauge reads one quarter and the night has barely started.",
    "Radio traffic: a helicopter passes low overhead without slowing down.",
]

# The fixed script: four lines per round, in speaking order (the order rotates each round).
LINES = [
    [("Daniel", "Generator two is sulking again, so I'm rerouting the east wing to the backup bus. Over."),
     ("Moira", "If the lights go, the incubators go with them, and I lose three days of cultures. Over."),
     ("Ralph", "East wing has four doors and two windows, all bolted, I checked each one twice. Over."),
     ("Samantha", "To everyone listening, we are still here, still on air, and the lights are holding. Over.")],
    [("Moira", "Blocked highways mean nobody is coming for the samples, so we keep them cold ourselves. Over."),
     ("Ralph", "Trucks on the highway are cover for whatever walks between them, I counted eleven. Over."),
     ("Samantha", "Tulsa, thank you, stay off that road and stay inside, we will relay what we hear. Over."),
     ("Daniel", "Tell Tulsa the long way round costs fuel we do not have, but it beats the trucks. Over.")],
    [("Ralph", "Loading dock, three scratches, a pause, three more, like it is keeping time. Over."),
     ("Samantha", "Nobody opens that door, and nobody answers it, not even to be polite. Over."),
     ("Daniel", "The dock shutter is rated for a forklift, so it will outlast our nerves at least. Over."),
     ("Moira", "Rhythm suggests residual motor memory, which is fascinating and deeply unwelcome. Over.")],
    [("Samantha", "Moira, please tell me the jar in the cold room is just condensation settling. Over."),
     ("Daniel", "I can drop the cold room two more degrees if that slows it down at all. Over."),
     ("Moira", "It is not condensation, the tissue is contracting, and the seal is holding for now. Over."),
     ("Ralph", "One jar, one lid, one cold room door with two locks, I am standing next to it. Over.")],
    [("Daniel", "Evacuate is a fine word when you own a helicopter, we own a forklift. Over."),
     ("Moira", "If they are evacuating, then the infection curve outside is worse than our models. Over."),
     ("Ralph", "Silence after an order means nobody stayed to give the next one, count on that. Over."),
     ("Samantha", "We will keep this channel open for anyone the military left behind tonight. Over.")],
    [("Moira", "Brown water means the filters upstream failed, so nobody drinks from the taps. Over."),
     ("Ralph", "We have forty two bottles in storage, I counted them this morning and again now. Over."),
     ("Samantha", "Listeners, boil your water or do not drink it at all, that is our best advice. Over."),
     ("Daniel", "I will isolate level two and run the pumps from the clean tank until morning. Over.")],
    [("Ralph", "Channel nine is two miles out at most, a child alone out there will not last long. Over."),
     ("Samantha", "Sweetheart, we hear you, stay where you are and keep talking to me on nine. Over."),
     ("Daniel", "I can boost the transmitter so she hears us clearly, it costs us an hour of fuel. Over."),
     ("Moira", "Ask her if anyone near her is coughing or feverish, gently, it matters a lot. Over.")],
    [("Samantha", "The roof alarm again, Ralph, tell me it is the rain and not our friend from the dock. Over."),
     ("Daniel", "That hatch sensor has false alarmed six times this month, water gets in the housing. Over."),
     ("Moira", "The infected do not climb well yet, but yet is doing a lot of work in that sentence. Over."),
     ("Ralph", "Camera one shows rain, camera two shows rain, camera three is dark, I am going up. Over.")],
    [("Daniel", "A quarter tank is six hours if we kill the east wing and the second freezer. Over."),
     ("Moira", "The second freezer holds the only clean samples we have, it stays on no matter what. Over."),
     ("Ralph", "Then the east wing goes dark, and I lock its four doors from the inside myself. Over."),
     ("Samantha", "Six hours to dawn, listeners, we will be here for every one of them with you. Over.")],
    [("Moira", "It did not slow down, so either they cannot see us or they do not want to. Over."),
     ("Ralph", "Rotor sound faded north east, same direction as the highway trucks, I counted it. Over."),
     ("Samantha", "To the pilot heading north east, this is the lab on the radio, please come back. Over."),
     ("Daniel", "If they do come back, the roof will not hold them, so I will clear the car park. Over.")],
]
ROUNDS = len(LINES)


def grammar(speakers, max_lines=4):
    src = (HERE / "screenplay.gbnf").read_text()
    alternatives = " | ".join(json.dumps(s) for s in speakers)
    src = re.sub(r"^speaker\s*::=.*$", f"speaker ::= {alternatives}", src, flags=re.M)
    return re.sub(r"line\{1,\d+\}", f"line{{1,{max_lines}}}", src)


def directive(k):
    return (f"{EVENTS[k - 1]} Write the next lines of the script: up to four lines, "
            f"speakers from {', '.join(SPEAKERS)}.")


def script_block(lines):
    return "".join(f"{speaker}: {text}\n" for speaker, text in lines)


def d_messages(k, script_blocks=None):
    """Structure D, round k: cast sheet, then directive/script turns, then directive k.

    script_blocks[r] replaces the fixed script of round r+1 (the live arm feeds back
    the model's own output); None means the fixed script throughout.
    """
    messages = [{"role": "system", "content": CAST_SHEET}]
    for r in range(1, k):
        block = script_blocks[r - 1] if script_blocks is not None else script_block(LINES[r - 1])
        messages.append({"role": "user", "content": directive(r)})
        messages.append({"role": "assistant", "content": block})
    messages.append({"role": "user", "content": directive(k)})
    return messages


def a_messages(k, j):
    """Structure A, round k, j-th speaker: TalkWithMe 7.1's build_llm_messages.

    /Users/alfredo/workspace/hackTNT_2026/TalkWithMe/app/session.py:123-161 — the
    responding persona's own lines stay `assistant`; everyone else's become
    `user` messages reading `[Name]: text`; the audience traffic is a plain `user`.
    """
    persona = LINES[k - 1][j][0]
    messages = [{"role": "system", "content": PERSONA_PROMPTS[persona]}]

    def add(lines):
        for speaker, text in lines:
            if speaker == persona:
                messages.append({"role": "assistant", "content": text})
            else:
                messages.append({"role": "user", "content": f"[{speaker}]: {text}"})

    for r in range(1, k):
        messages.append({"role": "user", "content": EVENTS[r - 1]})
        add(LINES[r - 1])
    messages.append({"role": "user", "content": EVENTS[k - 1]})
    add(LINES[k - 1][:j])
    return persona, messages


def payload(messages, *, seed, grammar_text=None, stream=False, extra=None):
    body = {
        "model": "default",
        "messages": messages,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
        "seed": seed,
        "cache_prompt": True,
        "stream": stream,
    }
    if grammar_text is not None:
        body["grammar"] = grammar_text
    if extra:
        body.update(extra)
    return body


def wire(text):
    WIRE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with WIRE_LOG.open("a", encoding="utf-8") as log:
        log.write(text)


def wire_request(name, body):
    grammar_text = body.get("grammar")
    speakers = "none"
    if grammar_text is not None:
        rule = re.search(r"^speaker\s*::=(.*)$", grammar_text, flags=re.M).group(1)
        speakers = "|".join(re.findall(r'"([^"]+)"', rule))
    now = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    lines = [f"\n===== {now} {name} -> /v1/chat/completions  stream={body.get('stream')}  "
             f"grammar={speakers}  seed={body.get('seed')}  max_tokens={body.get('max_tokens')}"]
    lines += [f"[{m['role']}] {m['content']}" for m in body["messages"]]
    wire("\n".join(lines) + "\n")


def wire_counters(timings, usage=None):
    size = (usage or {}).get("prompt_tokens")
    return ((f"prompt_tokens={size}  " if size is not None else "")
            + f"evaluated={timings.get('prompt_n')}  reused={timings.get('cache_n')}  "
            f"generated={timings.get('predicted_n')}")


def wire_response(name, result, wall_ms):
    content = result.get("choices", [{}])[0].get("message", {}).get("content")
    wire(f"----- {name} <- {wall_ms:.1f} ms  "
         f"{wire_counters(result.get('timings', {}), result.get('usage'))}\n{content}\n")


def wire_stream_line(line):
    """Appends the content of one raw SSE line to the wire log as it arrives."""
    if not line.startswith("data: "):
        return
    data = line[len("data: "):].strip()
    if data == "[DONE]":
        wire("----- [DONE]\n")
        return
    try:
        event = json.loads(data)
    except json.JSONDecodeError:
        wire(f"\n(unparsed line) {data}\n")
        return
    if "error" in event:
        wire(f"\n!!!!! server error: {json.dumps(event['error'])}\n")
    choices = event.get("choices", [])
    for choice in choices:
        piece = (choice.get("delta") or {}).get("content")
        if piece:
            wire(piece)
    if any(choice.get("finish_reason") for choice in choices):
        finish = next(c["finish_reason"] for c in choices if c.get("finish_reason"))
        wire(f"\n----- finish_reason={finish}  {wire_counters(event.get('timings', {}))}\n")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    stream = sub.add_parser("stream-request")
    stream.add_argument("--speakers", required=True,
                        help="comma-separated grammar allowlist, or 'none' for no grammar")
    stream.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    speakers = None if args.speakers == "none" else args.speakers.split(",")
    body = payload(d_messages(1), seed=args.seed,
                   grammar_text=grammar(speakers) if speakers else None,
                   stream=True, extra={"timings_per_token": True})
    print(json.dumps(body, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
