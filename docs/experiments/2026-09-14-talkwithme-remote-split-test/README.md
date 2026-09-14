# TalkWithMe remote-split test ("the spike") — runlog

**Created:** 2026-09-14 (skeleton) · **Run started:** *(not yet)*
**Timebox:** 2 days from first provisioning command. Abort at end
of day 2 regardless of state — a partial observation recorded
honestly beats a heroic overrun.
**Provenance:** TODO Task 3a · [spec §3.3], [spec §7.1],
[spec §10.3] · [ADR-0001] (freeze gated on this spike) ·
foundation debate (brainstorm §9).

## The question

How deep do TalkWithMe's localhost assumptions go? Can the
modified-TalkWithMe app run on the demo laptop while its model
services (llama.cpp LLM, one TTS engine, whisper-fastapi) live on
a remote GPU box across the real internet — through the decided
SSH-tunnel transport — well enough to carry a 4-persona audio
session?

## Execution model

Pairing session: the owner drives every credentialed step
(provider console, SSH keys, payments); the agent navigates,
records, and keeps this runlog true. **Every command actually run
lands here, in order, with its output.** Placeholders in
copy-paste blocks must be un-pasteable or guarded — write
`<PASTE-BOX-IP-HERE>` style markers, never plausible-looking
values.

## Environment (fill at provision time)

- Provider / GPU / flavor: *(TBD — plan: Hyperstack A6000;
  alternate: Vast.ai RTX PRO 4000 VM if A6000s out of stock)*
- Box OS image: *(TBD)*
- Laptop: *(TBD — expected: owner's Mac)*
- TalkWithMe version: *(TBD — expected v7.0)*
- tts-serve engine chosen for the spike: *(TBD — any one engine;
  quality irrelevant here, only the plumbing)*
- LLM model file: *(TBD — any small GGUF; quality irrelevant)*
- Network path: laptop ⇄ internet ⇄ box, via `ssh -L` tunnel

## Step checklist

- [ ] 1. Provision the box (on-demand, never spot) via console;
      record flavor, price, region.
- [ ] 2. SSH in with the project keypair; baseline the box
      (GPU visible, driver, Docker if image ships it).
- [ ] 3. Stand up model services on the box, loopback-bound:
      llama.cpp server (small model), one tts-serve engine,
      whisper-fastapi.
- [ ] 4. Open the `ssh -L` tunnel from the laptop; verify each
      service answers through it (`curl` through the tunnel).
- [ ] 5. Run TalkWithMe on the laptop, configured to reach its
      LLM/TTS/STT through the tunnel endpoints.
- [ ] 6. Drive a 4-persona group session with distinct voices;
      record measures (a)–(f) below in the log.
- [ ] 7. (If time) Also test the plain `ws://`+token path for
      comparison, per TODO Task 3a setup note.
- [ ] 8. Tear down the box; record final cost.

## Measures to record

(a) audio delivery over WAN: buffering behavior, drops, stalls ·
(b) 4-persona session drivable end-to-end? · (c)
time-to-first-audio per dialog line, ≥10 consecutive lines,
rough numbers in a table · (d) effort estimate for a proper
tts-serve adapter · (e) architectural red flags (blocking calls,
hardcoded localhost, tight coupling) · (f) security observations
for [spec §10.1]: does anything in the stack provide auth? which
ports would need exposure without the tunnel?

---

## Runlog

*(empty — begins with the first provisioning command)*
