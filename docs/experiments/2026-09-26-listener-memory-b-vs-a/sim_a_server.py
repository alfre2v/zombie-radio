"""Starts the fork's app on 127.0.0.1:8010 with option A's restatement swapped in, in memory only (scratch tool).

Run from the fork's root with the fork's .venv/bin/python, so app imports and settings.yaml is found.
"""
import os
import sys

sys.path.insert(0, os.getcwd())
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))

import uvicorn  # noqa: E402

import app.routers.show as route  # noqa: E402
import app.show.director as director  # noqa: E402
import sim_a  # noqa: E402
from app.main import app  # noqa: E402

original = route.plan_round


def plan_round(run, story, show, played_s=0.0, transcript=None):
    sim_a.CURRENT = (transcript or "").strip()
    return original(run, story, show, played_s, transcript)


route.plan_round = plan_round
director._restatement = sim_a.restatement
uvicorn.run(app, host="127.0.0.1", port=8010)
