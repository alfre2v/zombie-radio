# Cloud GPU provider survey

**Date:** 2026-09-13 · **Arc:** Product definition (Task 2)
**Type:** survey (candidate providers compared and adjudicated)
**Method:** three parallel research agents (marketplaces ·
developer GPU clouds · European/traditional hosts + big-cloud
baseline); all claims verified online 2026-09-13 against official
pricing/docs pages; unverified items labeled. Marketplace prices
are dynamic snapshots — re-confirm in the console before ordering.
**Trigger to revisit:** provider chosen and smoke-tested; revisit
only on a stock-out, a price shift, or when post-MVP scale changes
the requirements.

*Context for the cold reader: Zombie-Radio needs a rented Linux
GPU box (24 GB-VRAM class) to host its AI backend (llama.cpp LLM +
TTS engines + Whisper STT, each Dockerized) for ~3 weeks of
intermittent dev plus demo day 2026-10-08. The deployment doctrine
(brainstorm §4): Ansible-driven and idempotent, targeting a
**plain SSH-able Linux VM running our own Docker containers with
NVIDIA GPU access** (nvidia-container-toolkit).*

## S0. Acceptance criteria

Agreed with the owner 2026-09-13 (owner's list, extended by the
criteria the research itself proved decisive). **Hard
requirements** — failing any disqualifies:

1. **Own Docker containers with GPU/CUDA access** on the box (the
   criterion RunPod fails).
2. **Linux** (universal in practice; non-discriminating).
3. **SSH access with sudo capability** — Ansible needs a
   sudo-capable user; root login itself is optional. (Note:
   membership in the `docker` group is root-equivalent anyway —
   the docker socket can mount the host filesystem — so on a
   rented single-tenant VM there is no meaningful privilege
   distinction to preserve.)
4. **Public IP with arbitrary TCP ports openable** — we serve our
   own WebSocket/HTTPS (proxy-only schemes with connection caps,
   like RunPod's 100 s proxy, fail this).
5. **Geography: Europe or USA** regions available (owner ruling).

**Ranking criteria** — the axes that separate qualifiers:

6. **Price** for a suitable GPU. Owner ruling: spot instances and
   ~$0.20–0.40/hr territory with some reliability risk are
   acceptable *for dev*; demo day is exempt from cost-cutting
   (see the demo-day protocol, S1.3).
7. **Pause/billing semantics** — what stopping actually costs and
   risks (the survey's biggest surprise: stop is neither free nor
   safe on most providers; prepaid balances can destroy data).
8. **Provisioning automation** (API/CLI/Terraform) for idempotent
   create/destroy from Ansible.
9. **VRAM per dollar** — 48 GB at $0.50/hr beats 24 GB at €0.79
   while our LLM+4×TTS+STT budget is unmeasured (brainstorm §8).
10. **Stock reliability + account friction lead time** (GPU
    quotas, ID verification, capacity droughts near demo day).
11. **UDP support** (future WebRTC; soft criterion for the MVP).
12. **Image quality** — drivers/Docker/toolkit preinstalled
    shrinks the playbook (never disqualifying: Ansible can
    install anything).

---

## S1. General findings

**1. The market has three tiers, and our doctrine survives in two
of them.** *Marketplaces* (RunPod, Vast.ai, TensorDock) are
cheapest but quirky; *developer GPU clouds* (Lambda, Paperspace,
Verda, Hyperstack) are real VMs at 2–4× marketplace prices;
*traditional/EU hosts* (Hetzner, OVH, Scaleway) are ordinary
infrastructure with GPUs attached. Ten of eleven candidates give
root-SSH machines where Ansible + Docker + nvidia-container-toolkit
works as-is. The one structural exception is RunPod.

**2. The owner's RunPod recollection: resolved, and inverted.**
On RunPod your workload *is* the container RunPod runs — it gets
the GPU just fine, but you **cannot run your own Docker daemon
inside** ("you cannot spin up your own Docker instance or use
Docker Compose on Pods" — [their docs](https://docs.runpod.io/pods/overview)).
The "recent change" memory is real but went the *wrong* direction:
the March 2025 CPU-pod migration removed the Docker-in-Docker that
the old Kata-based pods had. GPU pods never allowed it. RunPod is
a fine platform with the wrong shape for our doctrine.

**3. Universal warning: stop ≠ safe, stop ≠ free.** Recurring
foot-guns across providers, each of which could eat demo day:

- On every marketplace and several clouds, a **stopped instance
  may never reclaim a GPU** (RunPod, Vast, TensorDock documented;
  OVH shelving carries the same risk).
- On Hyperstack, a merely-*stopped* VM **keeps billing the full
  GPU price** (only hibernate stops the meter). On OVH you must
  *shelve*, not stop.
- Prepaid-balance providers **destroy resources at $0 balance**
  (TensorDock: servers auto-delete; Verda: instances discontinued,
  volumes deleted after 96 h grace).

**Demo-day protocol that falls out (candidate runbook):** never
spot/interruptible for the show; provision the demo instance the
evening before via the Ansible playbook, verify, and leave it
running (a full 24 h costs $3–19 anywhere on the shortlist); keep
prepaid balances topped; treat stop/resume as a dev-time
convenience only, with destroy-and-recreate as the reliable path —
which is exactly what idempotent Ansible is for.

**4. Price landscape for a suitable GPU (on-demand, 2026-09-13):**
from **$0.13/hr** (Vast.ai RTX 3090, marketplace) through
**$0.50–0.59/hr** (Hyperstack/Verda RTX A6000 48 GB — double our
VRAM floor) and **€0.75–0.79/hr** (OVH/Scaleway L4 24 GB), to
~$0.71–0.80/hr big-cloud L4 *plus quota purgatory*. Full-project
compute at ~130 intermittent hours: roughly **$17 (Vast) to €120
(Scaleway)** — money is not the deciding axis; operational shape
is.

**5. Big clouds disqualify themselves for a fresh account.**
AWS/GCP GPU quotas default to zero with slow/denied increases for
new accounts; Azure's cheapest true 24 GB is ~$3.20/hr. No price
advantage, pure friction. (Sensible only with an already-aged
account with quota.)

**6. Account lead times exist elsewhere too.** OVH gates GPU
quota on account seniority/credit; Scaleway requires payment +
government-ID verification for GPU quota. Whoever we pick:
**create and verify the account days before the GPU is needed.**

## S2. Per-provider findings (condensed; agents' full rubric answers preserved in the S3 table)

### Marketplaces

- **RunPod** — container platform, not VMs; no Docker-in-Docker on
  GPU pods (confirmed current); **no UDP**; HTTP proxy caps
  connections at 100 s (hostile to WebSockets — direct TCP mapping
  is the workaround). A5000 $0.16–0.27, 3090 $0.22–0.50/hr.
  Most mature marketplace operationally (per-second billing, API,
  CLI, Terraform via community). On its "leader" reputation
  (owner asked 2026-09-13): deserved — reported ~$120M ARR, the
  most polished ops in the tier — but it leads the *container
  platform* category (hand them an image, they run it with GPU),
  which is a different deployment style than our
  Ansible-over-SSH-VM doctrine, not a worse one. **Doctrine
  verdict: poor** — plan C only, with a restructured one-image
  deployment.
- **Vast.ai** — historically container-mode (same limitation), but
  now offers **true KVM VM rentals**: root SSH, "run Docker inside
  the instance" advertised ([VM docs](https://docs.vast.ai/documentation/instances/templates/virtual-machines)).
  Cheapest compute anywhere: 3090 ~$0.13/hr on-demand (~$0.03
  spot), 4090 ~$0.31. Per-second billing, CLI/API. Quirks: shared
  IP with **random external port mappings** (declared at create
  time, 64 max; UDP supported); fewer hosts support VM mode;
  stopped instances may wait indefinitely for a GPU →
  destroy-nightly pattern; host quality varies (pick
  high-reliability datacenter offers, not the floor price).
  **Doctrine verdict: good with modest adaptation.**
- **TensorDock** — KVM VMs, root SSH, "Docker included on all VM
  templates", **static-IP option with full port range** (Core
  Compute), cloud-init. 4090 ~$0.35–0.37/hr. The purest doctrine
  fit on paper — but acquired by Voltage Park (Mar 2025) with
  rough 2025 user reports (VMs unstartable, unresponsive support)
  and the auto-delete-at-$0-balance trap. Post-acquisition
  improvement: unverified. **Doctrine verdict: fits as-is;
  operational trust is the question.**

### Developer GPU clouds

- **Hyperstack** (NexGen Cloud) — real VMs; **RTX A6000 48 GB at
  $0.50/hr** (cheapest suitable GPU in the whole survey, with 2×
  our VRAM floor); Ubuntu images shipping **Docker +
  nvidia-container-toolkit preinstalled**; default-deny security
  groups with TCP/UDP; official (alpha) Terraform provider;
  **hibernate** stops compute billing (stopped-but-not-hibernated
  does NOT). Youngest of the tier (~2023-24); reports of GPU
  stock-outs and slow support. **Doctrine verdict: good; best
  price-to-fit ratio.**

  **Owner-verified on-demand pricing snapshot (2026-09-13,
  screenshot of hyperstack.cloud/gpu-pricing taken while
  creating the account)** — confirms the researched A6000
  figure. Owner's observation from the console: the create-VM
  page's GPU selection does not map cleanly to this price
  table (flavors vs. GPU models), so verify the chosen
  flavor's price in the console before launching.

  | GPU model | VRAM (GB) | Max pCPUs/GPU | Max RAM (GB)/GPU | $/hr |
  |---|---|---|---|---|
  | NVIDIA B300 | 288 | 28 | 240 | $7.40 |
  | NVIDIA B200 | 192 | 31 | 256 | $6.00 |
  | NVIDIA H200 SXM | 141 | 22 | 225 | $3.99 |
  | NVIDIA H100 SXM | 80 | 24 | 240 | $3.20 |
  | NVIDIA H100 NVLink | 80 | 31 | 180 | $2.60 |
  | NVIDIA H100 | 80 | 28 | 180 | $2.50 |
  | NVIDIA RTX Pro 6000 SE | 96 | 31 | 180 | $1.85 |
  | NVIDIA A100 SXM | 80 | 24 | 120 | $1.60 |
  | NVIDIA A100 NVLink | 80 | 31 | 240 | $1.40 |
  | NVIDIA A100 | 80 | 28 | 120 | $1.35 |
  | NVIDIA L40 | 48 | 28 | 120 | $1.00 |
  | **NVIDIA A6000** | **48** | **28** | **58** | **$0.50** ← our pick |
  | NVIDIA A4000 | 16 | 6 | 24 | $0.15 (fails our 24 GB floor) |

  Reading for our purposes: the **A6000 at $0.50/hr** remains
  the value pick (48 GB VRAM, 28 pCPUs; its 58 GB RAM is the
  thinnest spec in the lineup but ample for our stack); the
  L40 at $1.00/hr offers the same VRAM with more system RAM as
  the stock-out fallback; everything A100-and-up is overkill
  for this project.
- **Verda** (ex-DataCrunch, rebranded Nov 2025; Finnish, $180M+
  raised, SOC 2) — VMs with **root** SSH; A6000 48 GB
  $0.592/hr on-demand / **$0.296 spot**; Docker-preinstalled
  image variants; API/SDK/CLI; 10-minute billing increments;
  prepaid with the $0-balance destruction trap; pause = delete
  keeping volumes ($0.20/GiB-mo). **Doctrine verdict: good;
  strong second.**
- **Lambda** — real VMs, good firewall (TCP+UDP), Lambda Stack
  images; cheapest suitable is Quadro RTX 6000 24 GB $0.69/hr but
  **chronic capacity droughts on exactly the cheap single-GPU
  SKUs** (documented user reports + status incidents), and **no
  stop/resume at all** (terminate-only; persistence via paid
  filesystems). **Doctrine verdict: fits, but availability
  roulette vs a hard demo date.**
- **Paperspace** (DigitalOcean) — real VMs, genuinely good
  stop/resume, ML-in-a-Box image with NVIDIA Docker; but worst
  price in class (24 GB from $1.10/hr Pascal-era, $1.38 A5000),
  a possible $39/mo plan gate on the good GPUs, and credible
  platform-sunset-into-DigitalOcean reports. **Doctrine verdict:
  fits mechanically; avoid for this window.**
- **Massed Compute** (added 2026-09-13 at the owner's request —
  heard on an AI podcast, possible 50% discount code) — own
  hardware (not a marketplace), Tier III **US-only** datacenters
  (their FAQ's "UK datacenters" claim looks like AI-generated
  marketing — treat as false), founded 2021, Wichita KS. Real
  Ubuntu VMs: public IP, SSH + sudo confirmed, in-VM ufw
  firewalling (implies all ports open — verify on first boot),
  drivers/CUDA preinstalled, a documented Docker-deploy flow
  (GPU exposed via **vGPU**, works with the container toolkit
  but is not bare passthrough — verify hands-on), REST API with
  coupon support, no CLI/Terraform. List prices unremarkable:
  A30 24 GB $0.35/hr, A5000 $0.44, A6000 48 GB ~$0.55. **The
  podcast 50% codes are real** — affiliate creator codes entered
  at deploy time, applying to that instance's hourly rate, but
  often **restricted to specific GPU types** (one documented code
  was L40-only): coverage must be checked before counting on it.
  At 50%: A6000 48 GB ≈ **$0.275/hr** — best VRAM-per-dollar in
  the whole survey. Two sharp edges: **no user stop/pause at
  all** (terminate-and-lose-data or pay 24/7 — API-scripted
  teardown/rebuild is mandatory), and a prepaid **auto-recharge**
  wallet with a refund complaint on record; reputation footprint
  is very thin (2 Trustpilot reviews, both 1-star, both
  billing-related). **Doctrine verdict: good mechanically;
  conditional shortlist — only with a verified code and a passed
  smoke test.**

### European / traditional hosts

- **Scaleway** — L4-1-24G (L4 24 GB) **€0.79/hr, billed per
  minute of uptime; power-off genuinely stops compute billing**
  (friendliest stop/start economics in the survey). "Ubuntu GPU
  OS" images ship **drivers + Docker + NVIDIA runtime
  preinstalled** — the closest any provider comes to our doctrine
  out of the box. Official Terraform/CLI; instant delivery; GPU
  quota gated on payment + government-ID verification (do day 1).
  Known gotcha: blind `apt upgrade` can break the NVIDIA driver —
  pin driver packages in the playbook. Support reputation is the
  weak point. Intermittent ~130 h ≈ **€105–120**.
- **OVHcloud** — L4-90 (L4 24 GB + 22 vCPU/90 GB RAM — the
  beefiest CPU side on the shortlist, relevant for CPU-bound TTS
  helpers) **€0.75/hr**, no setup fee; OpenStack API/Terraform;
  drivers self-installed (fine — Ansible role). Gotcha: stopped
  instances keep billing — must *shelve*; unshelve carries
  capacity risk. GPU quota needs account seniority or upfront
  credit. Intermittent ≈ **€100**.
- **Hetzner** — no GPU cloud instances; dedicated GEX servers
  only. GEX45 (RTX PRO 4000 Blackwell 24 GB, launched days ago,
  Helsinki only): €214/mo + **€209 setup fee**, always-on billing,
  delivery hours-to-days. Bare-metal excellence, wrong economics
  for 3 weeks (~€380–425 total). **Wins only for a permanent
  always-on box** — i.e., possibly the *booth-era* answer, not the
  MVP one.

### Big-cloud baseline (one line each)

AWS g6.xlarge (L4) ~$0.80/hr + quota fight; GCP g2-standard-4
(L4) ~$0.71/hr + quota fight (blocked entirely on free trial);
Azure ~$3.20/hr for A10 — non-starter. None is sensible for a
fresh-account 3-week hobby project.

## S3. Master comparison table

| Provider | Model | Best-fit GPU | $/hr on-demand | Own Docker+GPU | Public IP / ports | UDP | Pause economics | Automation | Ansible fit |
|---|---|---|---|---|---|---|---|---|---|
| Vast.ai (VM mode) | KVM VM | RTX 3090 24 GB | **~$0.13** | Yes (advertised) | Shared IP, random ext. port map (64) | Yes | Stop risky → destroy/recreate | CLI/API, per-second | **Good** (adapt ports) |
| TensorDock | KVM VM | RTX 4090 24 GB | ~$0.35 | Yes | Port-forward or static IP full range | Static-IP: yes | Storage-only when stopped; $0 balance = deleted | API, cloud-init | **Best on paper**; trust concerns |
| RunPod | Container | A5000 24 GB | $0.16–0.27 | **No** (no DinD) | TCP NAT-mapped; proxy 100 s cap | **No** | Stop releases GPU | API/CLI/TF, per-second | **Poor** |
| Hyperstack | VM | A6000 **48 GB** | **$0.50** | Yes (preinstalled image) | Public IP + security groups | Yes | Hibernate = storage only; stop still bills! | API + official TF | **Good** |
| Verda | VM (root) | A6000 **48 GB** | $0.592 (spot $0.296) | Yes (image variant) | Dedicated public IP | Yes | Delete-keep-volumes; $0 balance trap | API/SDK/CLI, 10-min | **Good** |
| Lambda | VM | RTX 6000 24 GB | $0.69 | Yes | IP + firewall (TCP/UDP) | Yes | **None** (terminate only) | API, per-minute | Good; capacity roulette |
| Paperspace | VM | P6000/A5000 24 GB | $1.10–1.38 (+$39/mo gate?) | Yes (ML-in-a-Box) | IP $3/mo, ufw-managed | Yes | Good (off = storage only) | CLI/API/stale TF | Fits; avoid (sunset risk) |
| Massed Compute | VM (vGPU) | A30 24 GB / A6000 48 GB | $0.35 / $0.55 (**~$0.175 / $0.275 w/ 50% code**) | Yes (verify vGPU hands-on) | Public IP, in-VM ufw (likely all open) | Unverified (likely) | **Worst: no stop at all** — terminate or pay; prepaid auto-recharge | API only (coupons supported) | **Good** (US-only) |
| Scaleway | VM | L4 24 GB | **€0.79 (per-minute)** | Yes (preinstalled image) | Flexible IP + sec. groups | Yes | **Best**: off = compute stops | API/CLI/official TF | **Good, best image match** |
| OVHcloud | VM (OpenStack) | L4 24 GB (+90 GB RAM) | €0.75 | Yes (self-install) | IP included, sec. groups | Yes | Shelve, don't stop | OpenStack API/TF | **Good** |
| Hetzner | Dedicated | RTX PRO 4000 24 GB | €214/mo + €209 setup | Yes (bare metal) | IP incl., unlimited 1 Gbps | Yes | None (always-on) | Robot API, slow delivery | Excellent tech, wrong economics |
| AWS/GCP/Azure | VM | L4/A10 24 GB | $0.71–3.20 | Yes | Yes | Yes | Fine | Excellent | Quota friction disqualifies |

## S4. Verdict

**Shortlist of three, covering different bets:**

1. **Hyperstack** — *primary recommendation.* Cheapest suitable
   GPU ($0.50/hr for 48 GB — double our VRAM floor, which
   pre-buys headroom for the unmeasured LLM+4×TTS+STT budget,
   open question §8.5 of the brainstorm), images that match our
   doctrine exactly (Docker + toolkit preinstalled), real
   security groups with UDP (future WebRTC stays open), official
   Terraform. Risks: platform youth, stock-outs — mitigated by
   the hedge below.
2. **Scaleway** — *EU/boring-reliability pick.* Per-minute
   billing with genuine power-off savings, doctrine-matching GPU
   OS image, official tooling, EU jurisdiction. ~€120 for the
   project; the L4 is the least powerful GPU on the shortlist —
   fine unless the VRAM experiment says otherwise.
3. **Vast.ai (VM mode)** — *budget/dev pick.* ~$0.13/hr 3090s
   make it nearly free to burn hours during development; VM mode
   + destroy-nightly fits idempotent Ansible naturally. Random
   external ports and marketplace host variance make it a dev
   workhorse more than a demo-day host.
4. **Massed Compute** — *conditional wildcard (added
   2026-09-13).* Enters the shortlist ONLY if the owner's 50%
   code verifies: burn one hour on a $0.35 A30 checking (a) the
   code's GPU-type coverage, (b) `docker run --gpus all` under
   their vGPU setup, (c) ports actually open. If all three pass,
   an A6000 48 GB at ~$0.275/hr is the survey's best
   VRAM-per-dollar — but its no-pause billing makes API-scripted
   teardown/rebuild mandatory, its wallet auto-recharges, and its
   thin reputation argues against demo-day duty without a
   fallback provisioned.

**The hedge (recommended regardless of pick):** write the Ansible
inventory provider-agnostically (it targets "an Ubuntu box with an
NVIDIA GPU", nothing more) and smoke-test the full playbook on TWO
shortlist providers early — the cost is ~an hour of GPU time each
(<$2), and it converts a demo-day stock-out from crisis to
inventory-file edit. This hedge also de-risks the Task 3a spike:
the spike's remote box can be whichever shortlist provider
provisions first.

**Demo-day protocol** (S1.3): on-demand only, provision the
evening before, verify, leave running, balance topped up.

**Owner inputs (answered 2026-09-13, mid-survey):** geography =
Europe or USA (excludes nothing on the shortlist; adds a
host-location filter for Vast.ai offer-picking); budget = spot /
~$0.20–0.40/hr with reliability risk accepted for dev. Effect on
the verdict: the budget ruling *strengthens the dev/demo split* —
Vast.ai (on-demand 3090 at ~$0.13/hr is *below* the owner's spot
budget, i.e. on-demand reliability at spot prices) or Verda A6000
spot ($0.296/hr) become the dev workhorses, while the demo-day
instance runs on-demand on the smoke-tested primary (Hyperstack,
with Scaleway as EU alternate). The hedge stands unchanged.

**Graduation path:** provider choice + demo-day protocol become
an ADR + a runbook (`runbooks/deploy-gpu-instance.md`) once the
smoke test passes; this survey remains as provenance.

---

*Addendum 2026-09-13: the owner parked the Massed Compute
wildcard without verification ("not in our top 2, don't waste
time") — tracked in `follow-ups.md` with an
after-each-experiment-PR reminder trigger. The shortlist is
effectively Hyperstack (primary), Scaleway (EU alternate),
Vast.ai (dev workhorse).*
