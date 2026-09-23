"""Derives the facts of a streamed request from raw/stream/<label>.sse.txt (stdlib only).

usage: python3 parse_stream.py <label> [<label> ...]
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
LINE = re.compile(r"^(?P<name>[^:(\n]+?)(?: \((?P<emotion>[^)\n]*)\))?: (?P<text>[^\n\[\]]+)$")


def rule_values(request, rule_name):
    grammar = request.get("grammar")
    if grammar is None:
        return None
    rule = re.search(rf"^{rule_name}\s*::=(.*)$", grammar, flags=re.M)
    return re.findall(r'"([^"]+)"', rule.group(1)) if rule else None


def report(label):
    raw = HERE / "raw" / "stream"
    request = json.loads((raw / f"{label}.request.json").read_text())
    allowed = rule_values(request, "speaker")
    emotions = rule_values(request, "emotion")

    events = []
    for row in (raw / f"{label}.sse.txt").read_text().splitlines():
        stamp, _, rest = row.strip().partition(" ")
        if not rest.startswith("data: "):
            continue
        data = rest[len("data: "):]
        events.append((float(stamp), None if data.strip() == "[DONE]" else json.loads(data)))

    content_at, reasoning_chunks, finish, timings, errors, text = [], 0, None, None, [], ""
    for at, event in events:
        if event is None:
            continue
        if "error" in event:
            errors.append(event["error"])
            continue
        timings = event.get("timings", timings)
        for choice in event.get("choices", []):
            delta = choice.get("delta") or {}
            if delta.get("content"):
                content_at.append(at)
                text += delta["content"]
            if delta.get("reasoning_content"):
                reasoning_chunks += 1
            finish = choice.get("finish_reason") or finish

    print(f"== {label}")
    print(f"grammar allowlist        : {allowed if allowed is not None else 'none (no grammar sent)'}")
    print(f"grammar emotions         : {emotions if emotions is not None else 'none'}")
    print(f"data lines               : {len(events)} (incl. [DONE]: {any(e is None for _, e in events)})")
    print(f"errors                   : {errors or 'none'}")
    print(f"chunks carrying content  : {len(content_at)}")
    print(f"chunks carrying reasoning: {reasoning_chunks}")
    if content_at:
        first, last = content_at[0], content_at[-1]
        print(f"first content chunk at   : {first:.1f} ms")
        print(f"last content chunk at    : {last:.1f} ms")
        print(f"spread (last-first)/last : {(last - first) / last if last > 0 else 0.0:.2f}")
    print(f"finish_reason            : {finish}")
    print(f"content, verbatim        : {text!r}")

    body, _, tail = text.rpartition("\n")
    lines = body.split("\n") if body else []
    speakers, used = [], []
    for n, line in enumerate(lines, 1):
        m = LINE.match(line)
        name = m.group("name") if m else None
        emotion = m.group("emotion") if m else None
        legal = (m is not None and (allowed is None or name in allowed)
                 and (emotions is None or emotion in emotions))
        speakers.append(name)
        used.append(emotion)
        print(f"  line {n}: {'legal  ' if legal else 'ILLEGAL'} {line!r}")
    print(f"complete lines           : {len(lines)}")
    print(f"text after last newline  : {tail!r}")
    print(f"speakers used            : {sorted({s for s in speakers if s})}")
    print(f"emotions used, in order  : {used}")
    if timings:
        print(f"final timings            : {json.dumps(timings)}")
    print()


if __name__ == "__main__":
    for arg in sys.argv[1:] or ["main"]:
        report(arg)
