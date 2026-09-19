# Docker networking: why host mode is load-bearing for this stack

**Date:** 2026-09-17 · **Arc:** MVP prototype (Task 1 design
input)
**Type:** technical analysis + decision record (owner asked for
the connectivity diagnostic between the bare-metal tts-serve and
the two containerized services; the analysis showed the chosen
mode is not merely convenient but security-posture-critical).
**Companion:** [discussion 2026-09-17] Ansible deployment shape.

## 1. The question

The stack mixes deployment styles: `llama-server` and
`whisper-fastapi` run in Docker containers, while the tts-serve
engine runs as a bare venv process on the host. Docker containers
normally live in their own network namespace behind NAT — so how
do these services reach each other, and does the bare↔container
boundary hide complications (the docker-proxy, published ports,
`host.docker.internal`)?

## 2. The answer for OUR stack: no complications — because of one flag

Both containers run with **`--network host`**. Under host
networking a container gets NO network namespace of its own — its
processes share the host's network stack outright. llama's
`--host 127.0.0.1 --port 8080` binds *the host's* loopback
exactly the way the bare tts-serve process does with
`FASTER_QWEN3TTS_HOST=127.0.0.1`. There is no bridge, no NAT, no
veth pair, no docker-proxy anywhere in this picture:

```
              VM (Ubuntu) — with --network host there is ONE network
              namespace: everything below shares the host's stack
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   eth0 (public IP) ◄── ONLY :22 exposed (provider sec. group)   │
│        │                                                        │
│      sshd ◄════ laptop's `ssh -N -L 8080/8001/8002 ...`         │
│        │        (tunnel exits land on host loopback)            │
│        ▼                                                        │
│   lo 127.0.0.1                                                  │
│    ├── :8080  llama-server      docker, --network host          │
│    ├── :8001  tts-serve         bare venv, systemd unit         │
│    └── :8002  whisper-fastapi   docker, --network host          │
│                                                                 │
│   East-west between the three: NONE — by architecture, each     │
│   is called only by TalkWithMe (on the laptop) via the tunnel.  │
└─────────────────────────────────────────────────────────────────┘
```

Two facts make this trivially safe:

1. **One namespace.** Host networking erases the container/host
   network boundary; bare process and containers bind the same
   loopback interface as peers. The bare↔container axis the
   question worried about does not exist as a *boundary* at all.
2. **No east-west traffic.** The architecture is a star whose
   center is TalkWithMe on the laptop: each service is called
   only through the SSH tunnel; the three services never call
   each other. Even if a future component needed to call another
   (say, a containerized engine calling whisper), under host
   networking that is a plain `127.0.0.1:<port>` call — still
   trivial. (Note: LuxTTS's wrapper transcribes reference audio
   with its OWN internal Whisper model, not our :8002 service —
   no hidden east-west there either.)

## 3. The complications are real — they live in bridge mode (which we avoid)

Docker's DEFAULT is bridge networking, and that world is where
the remembered pain lives. For contrast — the world we are NOT
in:

```
        BRIDGE MODE (what we do NOT do) — two namespaces, NAT between
┌─────────────────────────────────────────────────────────────────┐
│  host netns                        container netns              │
│   lo 127.0.0.1:8001 tts-serve       lo (its own, isolated!)     │
│   docker0 172.17.0.1 ───veth─────── eth0 172.17.0.2             │
│      ▲                                                          │
│      │ published ports need -p → docker-proxy / iptables DNAT   │
│      │ container→host-service needs 172.17.0.1 or               │
│      │   --add-host=host.docker.internal:host-gateway           │
│      │   AND tts-serve would have to bind 0.0.0.0 or docker0 ◄──┼── breaks
│      │ container cannot reach host's 127.0.0.1 at all           │   our §10
│      └──────────────────────────────────────────────────────────┘   posture!
└─────────────────────────────────────────────────────────────────┘
```

Reading that diagram bottom-up:

- A bridge-mode container has its own loopback — the host's
  `127.0.0.1` is unreachable from inside it, period.
- For the *laptop* to reach a bridged container, ports must be
  published (`-p 127.0.0.1:8080:8080`), which conscripts the
  userland docker-proxy or iptables DNAT rules — the "proxy
  listener" the owner half-remembered.
- For a *container* to reach a host-side bare service (our
  tts-serve), it must target the bridge gateway (`172.17.0.1`) or
  use `--add-host=host.docker.internal:host-gateway` — AND the
  bare service must stop binding loopback-only, widening to
  `0.0.0.0` or the docker0 interface.

That last point is the decision-grade finding: **bridge mode
would force tts-serve off loopback-only binding, violating the
spec §10 security posture** ("model APIs bound to the box's
loopback; the tunnel is the only door"). Host networking is
therefore not a convenience — it is what keeps the security model
true. This is also, in hindsight, part of why the remote-split
spike worked with zero networking surprises.

## 4. The decision and its honest costs

**DECIDED: `--network host` for all containers in this stack**,
carried as an explicit, commented choice in the playbook (never
an accident someone "fixes" back to bridge). Costs, accepted:

- **No port isolation between services** — all three share the
  host's single port space. Mitigation: the port assignments
  (8080 llama · 8001 tts · 8002 whisper) live in
  `inventories/common_vars.yml` as the single, collision-free
  registry.
- **Linux-only** — host networking does not behave this way on
  macOS/Windows Docker. Irrelevant here: the deployment targets
  are Ubuntu by the ratified portability bet, and the Mac laptop
  runs only the client, outside Ansible scope.
- **No container-level network sandboxing** — a compromised
  container sees the host network. Accepted under the §10
  threat model (single-operator box, loopback-only services,
  :22-only exposure, ephemeral instances).

## 5. Related deviation recorded

The supervision design (`--restart unless-stopped`, see the
deployment-shape doc §4) is mutually exclusive with the sealed
recipe's `--rm` flag — the playbook drops `--rm` and names the
containers. Noted in both docs so neither reads as a
transcription error of the other.
