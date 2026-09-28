"""Step 3.4c.5: option A simulated with perfect extraction (scratch tool; the fork untouched).

The driver test's listener is scripted, so a perfect extractor is a table: each scripted sentence and the facts
it gives. restatement() replaces the director's _restatement at launch (sim_a_server.py): in place of B's raw
quotes and rule, it states conclusions — who this voice is (anonymous, new, returning) and what each caller
told the lab. CURRENT holds this round's words, stashed by the launcher, since the director does not pass them.
"""
from app.show.director import _contacts, _receiver_period

CURRENT = ""

FACTS = {
    "Hello? Is anyone there?": [],
    "My name is Alfredo.": [("name", "Alfredo")],
    "I'm in Austin, Texas, and I have a pickup truck.": [("austin", "in Austin, Texas"),
                                                         ("truck", "with a pickup truck")],
    "This is Maria, from Dallas.": [("name", "Maria"), ("dallas", "in Dallas")],
    "We have a doctor with us.": [("doctor", "with a doctor")],
    "Do you need medicine?": [("medicine", "offering medicine")],
    "Hello again, lab.": [],
    "It's me, Alfredo, from Austin. I still have the truck.": [("name", "Alfredo"), ("austin", "in Austin"),
                                                               ("truck", "with the truck")],
    "Where should I drive?": [("drive", "asking where to drive")],
}


def caller(words):
    """A contact's name (the first given) and its facts, merged by key, the first wording kept."""
    name, facts = None, {}
    for sentence in words:
        for key, text in FACTS.get(sentence, []):
            if key == "name":
                name = name or text
            else:
                facts.setdefault(key, text)
    return name, facts


def described(name, facts):
    return ", ".join([name] + list(facts.values()))


def restatement(run, show):
    """A's conclusions about the voice, in place of B's restatement."""
    opened = _receiver_period(run)[0].n if run.rounds else None
    contacts = _contacts(run)
    now = next((words for n, words in contacts if n == opened), []) + ([CURRENT] if CURRENT else [])
    known = {}
    for n, words in [c for c in contacts if c[0] != opened][-show.restatement_contacts:]:
        name, facts = caller(words)
        if name:
            merged = known.setdefault(name, {})
            for key, text in facts.items():
                merged.setdefault(key, text)
    name, facts = caller(now)
    others = [described(k, v) for k, v in known.items() if k != name]
    if name is None:
        text = "This voice has not said who they are."
        if facts:
            text += f" They told you: {', '.join(facts.values())}."
        if known:
            text += f" Callers you know: {'; '.join(others)}. Do not guess which one this is."
    elif name not in known:
        text = f"This is {name}, a new caller" + (f": {', '.join(facts.values())}." if facts else ".")
        if others:
            text += f" Callers you knew before: {'; '.join(others)}."
    else:
        before = known[name]
        text = f"This is {name}, who called before" + (f": {', '.join(before.values())}." if before else ".")
        text += " Greet them as a returning friend, by name."
        new = [t for k, t in facts.items() if k not in before]
        if new:
            text += f" New in this contact: {', '.join(new)}."
    return text + " "
