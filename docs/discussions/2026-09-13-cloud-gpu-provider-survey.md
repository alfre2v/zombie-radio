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

  **Owner-verified while registering (2026-09-13):** the
  container-default reality is confirmed and worse than it
  sounds in the UI — what the marketplace rents is almost always
  a Docker container, and **creating a VM through the plain UI
  is effectively impossible**: there is no obvious "give me a
  VM" control. The page that matters (save-worthy, owner's
  words): <https://docs.vast.ai/guides/instances/virtual-machines>
  — it explains what their VMs can do over their Docker
  instances AND carries the only practical entry point: template
  links that auto-filter for VM-capable machines and launch a VM
  on rent (tracking parameters stripped):
  - Ubuntu 22.04 VM:
    <https://cloud.vast.ai/?ref_id=62897&creator_id=62897&name=Ubuntu%2022.04%20VM>
  - Ubuntu Desktop (VM):
    <https://cloud.vast.ai/?ref_id=62897&creator_id=62897&name=Ubuntu%20Desktop%20(VM)>

  For our automation this UI pain matters less than it seems:
  the CLI/API can filter offers with `vms_enabled=true` and
  launch from the KVM templates directly, which is the path the
  Ansible provisioning would use anyway — but for manual
  spike-day work, use the template links above, never the
  default rental flow.

  **Owner-verified VM-mode pricing snapshot (2026-09-13,
  screenshot from the Ubuntu 22.04 VM template listing;
  filters: disk ≥130 GB, ≥2 open ports, ≤$0.783/hr;
  marketplace-dynamic — will drift):**

  | Offer | VRAM | $/hr (VM mode) | Host location | CPU / RAM share | Reliability | Max duration |
  |---|---|---|---|---|---|---|
  | **1× RTX PRO 4000** (verified) | **24 GB** | **$0.330** | Switzerland | 24/24 cores · 32/32 GB | 97.6% | 24 days |
  | 1× RTX 4000 Ada (context: only 20 GB) | 20 GB | $0.237 | Hungary | 6/24 cores · 32/129 GB | 99.82% | ~52 days |
  | **1× RTX 3090** (verified, datacenter) | **24 GB** | **$0.645** | Czechia | 12/96 cores · 32/258 GB | 99.37% | 17 days |

  **The finding that matters (owner's discovery): VM-mode
  prices are MUCH higher than container-mode prices.** The
  survey's earlier "~$0.13/hr RTX 3090" figure was
  container-mode pricing; VM-capable hosts are a smaller,
  pricier subset — the same 3090 costs ~$0.645/hr as a VM,
  ~5× the container rate. Consequences for the verdict math:
  (a) Vast's "dev workhorse: nearly free compute" role is
  **weakened** — at $0.645/hr a Vast VM 3090 is *more*
  expensive than Hyperstack's 48 GB A6000 at $0.50/hr, for
  half the VRAM; (b) the budget option on Vast VM-mode is the
  **RTX PRO 4000 24 GB at ~$0.33/hr**; (c) sub-$1 VM offers
  with ≥24 GB were exactly two in this snapshot — thin
  inventory, consistent with "smaller subset of hosts support
  VMs". Net: Hyperstack's primacy strengthens; Vast remains
  useful as the fallback marketplace and for the odd cheap
  RTX PRO 4000, not as the default cheap-burn tier.
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
  does NOT). **Hibernation caveat, owner-verified 2026-09-16
  (their own pre-hibernate warning, verbatim): "Hardware is not
  reserved during hibernation. Restoring requires the same
  flavor to be in stock. If unavailable, the VM cannot be
  restored until resources become available."** So hibernate =
  cheap pause with a restore-lottery attached — the same
  stop-is-not-safe pattern as everywhere else, joining the S1.3
  warning list. **Restore tested 2026-09-16 (lottery won): disk
  intact, but NO process survives — not even tmux.** Their
  "hibernation" is operationally stop+boot-with-disk-kept, not a
  suspend-to-RAM-image resume: budget a full service restart on
  every resume. Demo-week consequence: NEVER hibernate the show
  box; provision-the-evening-before-and-leave-running is now
  triply justified. Youngest of the tier (~2023-24); reports of GPU
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
  | NVIDIA A4000 | 16 | 6 | 24 | $0.15 (below the 24 GB target; becomes interesting only if the aspirational 16 GB goal — [spec §4] — is ever proven) |

  Reading for our purposes: the **A6000 at $0.50/hr** remains
  the value pick (48 GB VRAM, 28 pCPUs; its 58 GB RAM is the
  thinnest spec in the lineup but ample for our stack); the
  L40 at $1.00/hr offers the same VRAM with more system RAM as
  the stock-out fallback; everything A100-and-up is overkill
  for this project.

  **Stock-out reports upgraded to owner-confirmed
  (2026-09-13):** while creating the account, the owner watched
  A6000 availability fluctuate in and out of stock several
  times on the pricing page alone. Practical consequences: the
  L40 fallback is not theoretical; grab-and-hold applies on
  demo week (the demo-day protocol's provision-the-evening-
  before rule earns its keep); and the two-provider
  smoke-test hedge stays mandatory.

  **Box-birth ritual (owner-verified 2026-09-19; repeat on EVERY
  rental):** a freshly created Hyperstack VM is not reachable
  until these manual console steps are done in
  `console.hyperstack.cloud`, on the VM's page:

  1. **Networking → "Attach a public IP"** — the VM has no
     public address until you do; note the assigned IP (wired
     into `inventories/cloud/hosts.yml` via
     `make ans-set ENV=cloud IP=<ip>`, reverted with
     `make ans-unset`; NEVER committed).
  2. **Firewall → "Enable SSH Access"** — default-deny security
     groups mean port 22 is closed until clicked.
  3. **Firewall → "Enable ICMP Access"** — nice-to-have so the
     box answers ping (network-latency measurement; CANADA-1
     from the owner's laptop ≈ 58 ms, NORWAY-1 ≈ 215 ms).
  4. From the laptop: ping the IP and (optional but cheap)
     eyeball the hardware over SSH (`nvidia-smi`, `nproc`,
     `free -h`, `df -h`) before pointing the playbook at it. No
     manual host-key acceptance is needed — the deployment
     accepts unknown hosts automatically (TOFU; shape doc §15).

  **GPU↔region mapping (owner-found 2026-09-15, during the
  remote-split experiment):** Hyperstack documents which
  regions host which GPU families —
  <https://docs.hyperstack.cloud/docs/hardware/flavors/> —
  and the split matters: **A6000 and better live in CANADA-1;
  A4000s live in NORWAY-1.** Consequences: (a) region is
  chosen FOR you by the GPU you pick — plan network latency
  accordingly (the experiment's A4000 box in Norway put a
  transatlantic hop inside every measurement); (b) for demo
  day, the A6000-in-Canada-1 geometry should be verified
  against the venue's location as part of the
  provision-the-evening-before protocol.
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
3. **Vast.ai (VM mode)** — *budget/dev pick, DEMOTED 2026-09-13
   by owner field data (see the VM-mode pricing snapshot in
   S2):* the ~$0.13/hr 3090 figure was container-mode pricing;
   VM-mode 3090s run ~$0.645/hr — pricier than Hyperstack's
   48 GB A6000 — and sub-$1 24 GB VM offers are thin (best
   found: RTX PRO 4000 24 GB at ~$0.33/hr). Vast stays on the
   list as the fallback marketplace, not the cheap-burn tier.
   VM mode + destroy-nightly still fits idempotent Ansible
   naturally; random external ports and host variance still
   make it a dev machine, not a demo-day host.
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

## S5. The driver ↔ CUDA ↔ wheel compatibility rule, and the OS-image dimension (added 2026-09-19)

*Provenance: the rule was learned live 2026-09-18 (PyPI's default
torch, a cu130 build, crash-looped on the R570 box — arc-plan
journal, pothole 1) and generalized 2026-09-19 during the owner's
PR #4 review, when he asked the two questions this section
answers: what happens on a VM with an OLDER driver, and how
portable is the deployment across providers? The survey's original
axes (price, billing, automation) lacked this one: **which OS
image / driver branch to pick**, and what the choice commits us
to. This section closes that gap.*

### S5.1 The rule (what actually happens)

The driver's `CUDA Version` reported by `nvidia-smi` is the
**maximum** CUDA runtime generation that driver supports — it is a
capability ceiling, not the version of anything installed. Three
cases for a torch-family wheel built for CUDA `X.Y` (e.g. our
`cu128` pins, [arc journal 2026-09-18]):

| Box driver vs the wheel's CUDA build | Example | Result |
|---|---|---|
| Driver **newer** than the wheel, any amount, even across majors | R595 (CUDA 13.2) running cu128 wheels | **Works.** Drivers run applications built against older CUDA unconditionally — backward compatibility is the driver's contract. |
| **Same major, driver minor older** | R550 (12.4) or R535 (12.2) running cu128 wheels | **PROVEN 2026-09-19 (upgraded from "expected"):** the full stack converged from zero on an R550/CUDA 12.4 box and served REAL inference (TTS synthesis + STT) on cu128 wheels — see the arc journal. Mechanism: CUDA 12 "minor version compatibility" — the pip wheels bundle their own CUDA 12.8 runtime libraries (the `nvidia-*-cu12` wheel dependencies), and the driver-side ABI is stable within a major version; NVIDIA's stated floor for any CUDA 12.x app is the R525 branch (CUDA 12.0). Caveat stands in principle (features needing newer kernel-mode support *can* fail under minor-compat) but did not bite a full inference workload at 12.4; R535 remains untested. |
| Driver **major older** than the wheel's major | R570 (12.8) running **cu130** wheels | **Hard fail** — the exact `"driver too old"` crash loop we ate live on 2026-09-18. CUDA 13 wheels need an R580-family driver or newer. There is no forward compatibility across majors for these wheels. |

Two corollaries that keep the rule honest:

1. **The failure we debugged was not "the pin is fragile"** — it
   was PyPI's *default* being the newest major (cu130 at the
   time). A deliberately pinned, one-major-behind variant like
   cu128 is close to the most portable choice available: it runs
   on every CUDA 12.x driver (exactly or via minor-compat) AND on
   every CUDA 13.x driver (backward compat). The floating default
   is the fragile choice — it hard-fails on every box whose
   driver hasn't caught up to the newest major yet, which near a
   major transition is *most* boxes.
2. **The same rule governs the Docker containers.** The llama.cpp
   and whisper-fastapi images carry their own CUDA builds inside;
   the host driver must support *their* CUDA major too. Wheels
   and images sit on the same side of the line; the driver is the
   only thing on the other side.

### S5.2 The Hyperstack image menu, mapped (console snapshot 2026-09-19)

Against our cu128 pins and CUDA-12-built containers:

- **Server 24.04 LTS R570 CUDA 12.8 with Docker** — our pinned
  image ([spec §6]); exact match, proven live 2026-09-18.
- **Server 22.04 LTS R570 CUDA 12.8 with Docker** — same driver
  branch, older Ubuntu LTS; the base role asserts Ubuntu but not
  the release, and the per-engine-venv rule makes system Python
  irrelevant, so this should converge identically. Untested.
- **Server 24.04 LTS R595 CUDA 13.2 with Docker** — newer-driver
  case: cu128 works (backward compat). Also the only image on the
  menu where PyPI's floating cu130 default would have worked —
  and the natural candidate when we someday cross the CUDA-13
  line deliberately.
- **Server 22.04 LTS R550 CUDA 12.4 with Docker** — minor-compat
  territory, **PROVEN 2026-09-19**: from-zero converge,
  changed=0 idempotency, and a real TalkWithMe session on this
  exact image (which also proved the 22.04/Python 3.10 side —
  the engine venv is version-agnostic in practice).
- **Server 22.04 LTS R535 CUDA 12.2 with Docker** — same
  territory, still untested by us. (Historical note:
  the R535 generation is also the filter that killed half of
  tts-serve's engines in the remote-split experiment's ranking —
  driver age bites engines through more paths than torch wheels.)
- **All the non-Docker variants** (plain R570/R550/R535 CUDA
  images, vanilla 22.04/24.04 LTS) — excluded by design: the base
  role asserts docker/nvidia-smi/nvidia-ctk preexist and
  deliberately never installs them ([spec §6] posture: the image
  provides the platform, Ansible provides the stack).

### S5.3 The portability contract (any provider)

What the deployment actually requires of a rented VM, stated once:

> **Ubuntu + Docker + nvidia-container-toolkit + a CUDA-12-capable
> NVIDIA driver (R525 or newer)** — with a driver ≥ the
> wheels'/images' own CUDA minor preferred, and same-major
> minor-compat tolerated.

Every "with Docker" GPU image in the Hyperstack menu satisfies
this, and the mainstream providers (survey S2/S3) ship R535–R595
today. The contract breaks only on drivers older than R525
(CUDA < 12.0 — museum pieces on GPU clouds in 2026) or on the day
the ecosystem's default images go CUDA-13-only — at which point
the pin moves once, fleet-wide, per the [spec §6] never-cross-a-
major-casually posture.

### S5.4 What this changed in the machinery (2026-09-19)

The hardware dependency is now explicit and asserted, not implied
by hardcoded pins: the CUDA generation is a project variable
(`zr_cuda_variant: "cu128"`, with `zr_torch_version` beside it, in
`inventories/common_vars.yml`); every torch-family pin and its
index URL derive from it; and a base-role preflight parses the
driver's supported CUDA version from `nvidia-smi` and **asserts
the driver's major can run the pinned variant** — converting the
09-18 experience (crash loop discovered *after* a 5 GB model
download) into a seconds-fast, named failure at the top of the
run. Adapting to a different provider or driver branch is a
one-line `99-<env>.yml` override. Mechanics: shape doc §14
([discussion 2026-09-17]).

---

*Addendum 2026-09-13: the owner parked the Massed Compute
wildcard without verification ("not in our top 2, don't waste
time") — tracked in `follow-ups.md` with an
after-each-experiment-PR reminder trigger. The shortlist is
effectively Hyperstack (primary), Scaleway (EU alternate),
Vast.ai (dev workhorse).*
