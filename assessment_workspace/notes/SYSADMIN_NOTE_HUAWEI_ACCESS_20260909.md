# Note to the System Administrator — Unblocking Huawei Access for Extraction / mtafiti

**From:** Programme delivery (via Bramwel Mwalo · Huawei domain `hid_mroq3ef3gos5pjp` / `3f9d29266af74046bfb637cabb995c39`)
**Date:** 2026-09-09
**Scope:** Huawei Cloud, af-south-1 (Johannesburg) + ap-southeast-1 (Singapore)
**Reader:** system administrator with owner-console rights on the Huawei account above.

---

## 1 · To resolve the network connection we need to…

**Stand up a small jump-host (bastion) inside the RDS estate's own VPC.**

### Why

The pod that runs our extraction workload (mtafiti / discovery / census) sits in a Google Cloud Kubernetes cluster. Its outbound public IP is **not stable** — it has already changed once during this engagement (from `34.170.12.145` → `34.16.56.64` inside ~2 hours). Any Huawei security-group whitelist we add against a single pod IP is stale by the next redeploy, and we've already observed the drift silently break reach to 5 databases even after the SG whitelist was applied.

Two other problems compound this:
- **Two databases have no public IP at all** — `weego-replica-d536` (private `10.10.150.115`) and `rms-ai-pg` (private `192.168.1.30`, ap-southeast-1). No amount of SG whitelisting will ever reach them from the public internet.
- **Every extraction pull today crosses per-GB egress billing** on the RDS EIPs (`charge_mode=traffic`, ~$0.08–$0.13 / GB in af-south-1). This scales linearly with the number of DBs we census — the estate we've already inventoried is ~24 GB on ONE reachable host alone.

A bastion inside the same VPC as the RDSs solves all three at once:
- Its **private VPC IP is stable forever** — the DB security groups whitelist it once, never again. Pod-IP drift stops mattering.
- It has **VPC-internal routing to every RDS**, including the two private-only instances — no public IP required on those databases.
- All bastion↔RDS traffic stays inside the VPC and **does not touch the EIP meters**. Only the pod-to-bastion leg is metered — and we can put that on a shared bandwidth plan later so it's fixed cost.

### It will cost

On the owner's Huawei account (not ours), in af-south-1:

| Line item | Config | Monthly |
|---|---|---|
| ECS `s6.xlarge.2` (4 vCPU / 8 GiB, x86 general-compute), yearly/monthly 1-yr commit | Growth-headroom size | **~$28–$34** |
| System disk 100 GiB General-Purpose SSD | Continuous | **~$13.20** ($0.132/GiB/mo × 100) |
| EIP, pay-per-use traffic-mode, 100 Mbps cap, bound to ECS | Fixed portion = $0 when bound | **$0 fixed** |
| Egress traffic (pod → bastion only; bastion → RDS is intra-VPC and free) | 50 GB typical / 200 GB peak | **$4–$16** |
| **Typical monthly** | | **~$45–$55** |
| **Peak-census month** | | **~$65** |
| **If deallocated when idle** (pay-per-use ECS stopped; disk keeps billing) | | **~$18–$20** |

Trim option: swap ECS for `s6.large.2` (2 vCPU / 4 GiB) — drops the ECS line to ~$18–$22/month at the cost of headroom. Recommend the xlarge given the owner's stated intent to keep integrating more databases.

**Fixed regardless of DB count.** ECS + disk + EIP-reservation don't change when we add databases. Each additional database adds only marginal egress dollars (cents per census; a few dollars for a full multi-GB pull), and only when a census actually runs. The bastion is a fixed shared cost across every DB it fronts.

**Whose account bears it:** owner's Huawei account (`hid_mroq3ef3gos5pjp` / `3f9d29266af74046bfb637cabb995c39`), af-south-1 project (`517a45cac3994683abcf0cc155b3c01b`). Not ours.

---

## 2 · We are connected to… we are not connected to… this is why…

There are **two independent problems** that anyone acting on this note must keep distinct: (i) NETWORK PATH (firewall + routing) and (ii) DATABASE CREDENTIALS (login). The bastion solves (i) for the owner's tenant only. It does **NOT** solve (ii) anywhere; DB usernames + passwords must be supplied separately.

### Currently LIVE (SQL data-layer reachable) — 2 of 12 hosts

| # | Instance | Region | Engine | Public IP | Working DB user |
|---|---|---|---|---|---|
| 1 | **Weego_and_marketing-analytics** | af-south-1 | MySQL 8.0.28 | 159.138.162.146 | `bramuel@%` |
| 2 | **3rd-party USSD host** | af-south-1 (different tenant) | MySQL 5.7.44 | 110.238.76.159 | `bramuel@%` |

### Currently NOT reachable — 10 of 12 hosts

**A · Owner-tenant, firewall-blocks-our-pod-IP (6 hosts).** Network path is closed because the current pod egress IP is not whitelisted on the RDS security-group. Bastion inside the VPC fixes this permanently (SGs whitelist the bastion private IP, one-time).

| # | Instance | Public IP | Attached SGs (id → name) | What's missing besides bastion |
|---|---|---|---|---|
| 3 | RDS-INTERACTIONS | 159.138.162.220 | `aed8d060-16fc-489d-8b62-1a2c3ea45cca` → **RMS-IPS**; `2cc0ad09-8d8f-464d-9d39-4fe1f3052b57` → **default** | **DB password** (network is already open from our pod but auth `bramuel` is denied 1045; user has SELECT permission on the `interactions` schema needed) |
| 4 | rds-shikisha | 203.123.83.144 | `803fb5f5-1f24-4d09-847d-e921a66b4e45` → **sg-shikisha**; `aed8d060-…` → **RMS-IPS** | DB password for `corporate` or `saa` (users known via API enum; passwords not) |
| 5 | election-prod-db2 | 110.238.77.61 | `92233ae5-f4d2-4ace-8685-023881e189f1` → **sg-Mysql**; `aed8d060-…` → **RMS-IPS** | DB **username + password** (no cred anywhere) |
| 6 | visitors-database-cluster | 110.238.75.83 | `92233ae5-…` → **sg-Mysql**; `aed8d060-…` → **RMS-IPS** | DB **username + password** (dbs `citizen_digital`, `db_visitors`, `db_visitors_old`, `db_visitors_v1`, `rembesha` — no cred) |
| 7 | dbms-trf-req-database-3 | 159.138.175.179 | `92233ae5-…` → **sg-Mysql** | DB **username + password** |
| 8 | citizen-digital-dev-db-cluster | 159.138.164.124 | `92233ae5-…` → **sg-Mysql**; `a6456cfb-696e-45c7-8147-13028a53dcea` → **sg-Citizen-Digital** | DB **username + password** (dbs `citizen_digital`, `db_visitors` — no cred) |

**B · Owner-tenant, no public IP (2 hosts).** These cannot be reached from the public internet under any SG rule change. Only a bastion inside their VPC can reach them.

| # | Instance | Region | Engine | Private IP | Subnet | What's missing besides bastion |
|---|---|---|---|---|---|---|
| 9 | weego-replica-d536 | af-south-1 | MySQL 8.0 (read replica) | `10.10.150.115` | `subnet-media-web` (`10.10.150.0/24`) | Inherits users from WEEGO primary — **primary DB password** unlocks this too |
| 10 | rms-ai-pg | ap-southeast-1 | PostgreSQL 16 | `192.168.1.30` | `rms-ai-private-subnet` (`192.168.1.0/24`) in VPC `rms-ai-vpc` | Needs a **second bastion in ap-southeast-1** (or VPC peering) + a **PostgreSQL user + password** |

**C · Third-party tenant (2 hosts).** These EIPs are not visible in the AK/SK's account inventory — they belong to a Huawei tenant the owner does not administer. **Our own bastion cannot help here; the other tenant must whitelist us on their side.** The `bramuel@%` credential we already hold would very likely authenticate, since it authenticates against the third-party tenant's other MySQL (110.238.76.159) with the same password.

| # | Public IP | What's missing |
|---|---|---|
| 11 | 203.123.86.10 | **The other tenant's admin must add our bastion's EIP to their SG on TCP/3306**. Owner's admin cannot do this alone. |
| 12 | 159.138.164.93 | Same as above. |

### How we resolve it

- **Network path (i):** stand up the bastion in af-south-1 (see §3.A) and add its private VPC IP `10.10.150.<x>/32` to the 5 unique SGs listed above. That opens 6 own-tenant instances at the network layer in one pass. For rms-ai-pg (#10), a second small bastion in ap-southeast-1 or a VPC peering between `vpc-media-web` and `rms-ai-vpc` — either works.
- **Third-party (C):** owner-to-owner conversation with the other tenant's administrator, asking them to whitelist the bastion's public EIP (which will be stable after §3.A). Nothing on this side unblocks that side.
- **Credentials (ii):** supplied outside this note by the owner. See §3.B.

---

## 3 · Do the following to resolve both…

Actions grouped by who does what. **A + B + D can start immediately in parallel.** **C is a separate conversation with the third-party tenant.**

### A · IAM grants — attach these Huawei-managed policies to user `BramwelMwalo`

Scope every grant to the **af-south-1 project** (for the primary bastion) and the **ap-southeast-1 project** (if the owner authorises a second bastion for `rms-ai-pg`).

Project IDs (for scoping the policy attachment in the IAM console):

- **af-south-1**: project id `517a45cac3994683abcf0cc155b3c01b` — this is where the bastion lands.
- **ap-southeast-1**: project id `b2c3b9b1ef6346ab9e45818f8a6714ba` — needed only if we do a second bastion instead of VPC peering.

Attach the following **system-defined policies** (exact Huawei display names — confirmed against Huawei's SMS reference doc `https://support.huaweicloud.com/intl/en-us/productdesc-sms/sms_01_0015.html`):

1. **`ECS FullAccess`**
2. **`VPC FullAccess`**
3. **`EVS FullAccess`**
4. **`EIP FullAccess`**

(Note: `EVS KMSAccess` only if the owner wants encrypted disks — not required for the base bastion.)

**Verification the admin should run once policies are attached** (from the Huawei console → IAM → Users → BramwelMwalo → Permissions): the user should now see `ecs:cloudServers:*`, `evs:volumes:*`, `vpc:*`, and `eip:*` on both projects. Once visible, the delivery team's read probe will start returning 200s on `list_flavors` / `list_servers_details` (currently 403 `Pdp.0001`) — that is the objective signal that we can proceed to provision.

Minimal per-action list (if the admin prefers least-privilege over the four FullAccess policies) is in the appendix.

### B · DB logins — supplied by the owner, one row per instance

The bastion opens the network path but never provides credentials. Please supply the following **at 0600 permissions in the same secure hand-off channel used for the earlier AK/SK CSV**. Do NOT paste in chat.

| # | Instance | What we need |
|---|---|---|
| 3 | RDS-INTERACTIONS | **DB password only** (bastion not required — network is already open from our pod). Any user with SELECT on schema `interactions` — root or a purpose-built read-only user is ideal. |
| 4 | rds-shikisha | DB user + password. Users `corporate` and `saa` are known (from API enum); passwords not. |
| 5 | election-prod-db2 | DB user + password. |
| 6 | visitors-database-cluster | DB user + password (schemas `citizen_digital`, `db_visitors`, `db_visitors_old`, `db_visitors_v1`, `rembesha`). |
| 7 | dbms-trf-req-database-3 | DB user + password. |
| 8 | citizen-digital-dev-db-cluster | DB user + password. |
| 9 | weego-replica-d536 | Inherits users from the WEEGO primary — a WEEGO primary read-only password unlocks both hosts 1 and 9. |
| 10 | rms-ai-pg | PostgreSQL user + password. Owner also picks the reach path: (a) second bastion in ap-southeast-1 OR (b) VPC peering `vpc-media-web` ↔ `rms-ai-vpc` OR (c) defer. |

**Discipline on our side:** all credentials remain at `/app/backend/estate_keys/data_sources/*.csv` at `0600` perms, git-ignored on both repos, never committed, never echoed to logs. Only sha256-fingerprint + length is written into any report.

### C · Third-party tenant coordination (hosts #11 and #12)

Two hosts (`203.123.86.10`, `159.138.164.93`) sit in a Huawei tenant the owner does not administer. Owner should reach out to that tenant's administrator and ask for **one SG inbound rule**: the bastion's public EIP (which the owner's admin will know once §3.A + provisioning completes), TCP/3306, source `<bastion_eip>/32`.

The `bramuel@%` credential the owner has already supplied is likely to authenticate on those hosts too (same password fingerprint works on other hosts in the estate). Once the third-party SG is opened, we test.

### D · Rotate the shared wildcard credential — recommendation, not a blocker

The `bramuel@%` DB user currently authenticates from **any host on the internet** with a single password across at least two Huawei tenants. Same password on 3+ hosts. This is a shared admin-scoped credential — not an app-scoped one. Recommend the owner:

- **Issue app-scoped, least-privilege, per-DB users** for the mtafiti / extraction workload. Read-only on the specific schemas we need, sourced from `<bastion_private_ip>/32` (once bastion exists), rate-limit-appropriate.
- **Rotate the current `bramuel@%` password** on all instances where it is set, since it appeared in this session's terminal transcript during the earlier CSV parse.

This is a hygiene action, not a gate — the mtafiti engine work can proceed on the least-privilege users the moment they exist.

---

## Bastion Spec (owner-approved 2026-09-09, with growth headroom)

```
NAME:           akki-mtafiti-bastion-af-south-1
REGION:         af-south-1 (Johannesburg)
PROJECT ID:     517a45cac3994683abcf0cc155b3c01b
VPC:            de3ba6f7-d0e7-4228-8da2-19bd33a07ff2  (name: vpc-media-web,  CIDR: 10.10.150.0/24)
SUBNET:         c7fef874-8aef-4b91-9d3b-7e84ce53104d  (name: subnet-media-web, CIDR: 10.10.150.0/24, gw 10.10.150.1)
                — same VPC/subnet as the RDS estate, so bastion↔DB traffic stays intra-VPC and is not metered.

FLAVOUR:        s6.xlarge.2  (4 vCPU / 8 GiB · x86 general-compute) — growth-headroom recommendation
                Trim option: s6.large.2 (2 vCPU / 4 GiB) if the owner wants to cut ~$10/month;
                              adequate for now, less headroom for concurrent census workloads later.
IMAGE:          Ubuntu 22.04 LTS or 24.04 LTS (matches our existing GPU hosts)
SYSTEM DISK:    100 GiB · General-Purpose SSD (ext4)
DATA DISK:      none required at inception (add later if we cache anything on the bastion — we don't intend to)
BILLING MODE:   Pay-per-use for the first month (verify sizing), convert to Yearly/Monthly on month 2
                (yearly commit saves ~30% on the ECS line)

EIP:            1 reserved EIP, pay-per-use traffic-mode, 100 Mbps cap, bound-at-create
                (fixed portion $0 when bound; only outbound GB is metered)
                Migrate to shared-bandwidth plan later if concurrent census volume grows.

BASTION SG:     new SG (name: sg-akki-mtafiti-bastion)
                INBOUND:  TCP/22 from <delivery-team-supplied CIDR set> — SSH only, nothing else
                OUTBOUND: default allow-all (bastion needs to reach RDS 3306 and PG 5432 internally,
                          plus package repositories over HTTPS)

DB SGs to modify (add one inbound rule each):
                — Whitelist  <bastion_private_ip>/32  on  TCP/3306  in each of these SGs:
                    * aed8d060-16fc-489d-8b62-1a2c3ea45cca   (RMS-IPS)
                    * 2cc0ad09-8d8f-464d-9d39-4fe1f3052b57   (default)
                    * 803fb5f5-1f24-4d09-847d-e921a66b4e45   (sg-shikisha)
                    * 92233ae5-f4d2-4ace-8685-023881e189f1   (sg-Mysql)
                    * a6456cfb-696e-45c7-8147-13028a53dcea   (sg-Citizen-Digital)
                — After the bastion is provisioned, the delivery team supplies the exact
                  <bastion_private_ip>/32 to add.

KEYPAIR:        Delivery team generates ed25519 locally (private key never leaves our pod at 0600);
                admin injects the PUBLIC key at ECS create-time.

SECOND BASTION (optional — only if rms-ai-pg is in scope):
                NAME:      akki-mtafiti-bastion-ap-southeast-1
                REGION:    ap-southeast-1 (Singapore)
                PROJECT:   b2c3b9b1ef6346ab9e45818f8a6714ba
                VPC:       35528a18-8076-41a2-9796-e2334503c193   (name: rms-ai-vpc,  CIDR: 192.168.0.0/16)
                SUBNET:    bd97d46a-e4c7-4d9f-b2c4-b15444986a41   (name: rms-ai-private-subnet, CIDR: 192.168.1.0/24)
                              — same subnet as rms-ai-pg (192.168.1.30) so route is one-hop.
                FLAVOUR:   s6.large.2 (smaller; only reaches one instance)
                DISK:      40 GiB SSD
                EIP:       1 · same billing pattern as af-south-1 bastion.

                Alternative to a second bastion: enable VPC peering between:
                    peer-a: de3ba6f7-d0e7-4228-8da2-19bd33a07ff2  (af-south-1, vpc-media-web, 10.10.150.0/24)
                    peer-b: 35528a18-8076-41a2-9796-e2334503c193  (ap-southeast-1, rms-ai-vpc,  192.168.0.0/16)
                CIDRs do not overlap (10.10.150.0/24 vs 192.168.0.0/16), so peering is feasible.
                Peering + route-table updates in both VPCs are cheaper long-term but touchier to set up.
```

---

## Appendix · Minimal per-action IAM list (least-privilege alternative to the four FullAccess policies)

If the admin prefers least-privilege over `ECS/VPC/EVS/EIP FullAccess`, the minimum action set below is what the delivery team's provisioning script actually calls. Scope every action to the project IDs in §3.A.

**ECS (Elastic Cloud Server):**
```
ecs:cloudServers:list          ecs:cloudServers:get           ecs:cloudServers:create
ecs:cloudServers:delete        ecs:cloudServers:start         ecs:cloudServers:stop
ecs:cloudServers:reboot        ecs:cloudServerFlavors:get     ecs:cloudServerKeypairs:list
ecs:cloudServerKeypairs:create ecs:serverVolumes:use
```

**EVS (Elastic Volume Service — the system disk):**
```
evs:volumes:list   evs:volumes:get   evs:volumes:create   evs:volumes:delete
```

**VPC + Security Groups (only WRITES needed; READS are already granted):**
```
vpc:securityGroups:create        vpc:securityGroups:delete
vpc:securityGroupRules:create    vpc:securityGroupRules:delete
vpc:ports:create                 vpc:ports:delete
vpc:routes:create                (only if VPC peering is chosen for the ap-southeast-1 path)
```

**EIP + Bandwidth:**
```
eip:publicips:list       eip:publicips:get        eip:publicips:create       eip:publicips:delete
eip:publicIpTags:create
eip:bandwidths:list      eip:bandwidths:get       eip:bandwidths:create      eip:bandwidths:update      eip:bandwidths:delete
```

The `ECS/VPC/EVS/EIP FullAccess` policies are a strict superset of the above and are one click each in the IAM console. Least-privilege is 30-40 individual action grants. Either works; the delivery team is not sensitive to which the admin picks.

---

## Reference — full authoritative inventory (pulled read-only from the AK/SK this session)

```
DOMAIN:            3f9d29266af74046bfb637cabb995c39   (name: hid_mroq3ef3gos5pjp, enabled: True)
PROJECTS:
  af-south-1:      517a45cac3994683abcf0cc155b3c01b   (enabled: True)
  ap-southeast-1:  b2c3b9b1ef6346ab9e45818f8a6714ba   (enabled: True)

VPC/SUBNET (RDS estate · af-south-1):
  VPC id:          de3ba6f7-d0e7-4228-8da2-19bd33a07ff2
  VPC name:        vpc-media-web
  VPC CIDR:        10.10.150.0/24
  Subnet id:       c7fef874-8aef-4b91-9d3b-7e84ce53104d
  Subnet name:     subnet-media-web
  Subnet CIDR:     10.10.150.0/24
  Gateway:         10.10.150.1
  DNS:             100.125.1.250, 100.125.1.14

VPC/SUBNET (rms-ai-pg estate · ap-southeast-1):
  VPC id:          35528a18-8076-41a2-9796-e2334503c193
  VPC name:        rms-ai-vpc
  VPC CIDR:        192.168.0.0/16
  Subnet id:       bd97d46a-e4c7-4d9f-b2c4-b15444986a41
  Subnet name:     rms-ai-private-subnet
  Subnet CIDR:     192.168.1.0/24
  Gateway:         192.168.1.1

RDS INSTANCES · af-south-1 · owner tenant:
  RDS-INTERACTIONS                MySQL 8.0.28  public 159.138.162.220   private 10.10.150.3    SGs: RMS-IPS + default
  weego-replica-d536              MySQL 8.0     no public                private 10.10.150.115  SGs: default
  rds-shikisha                    MySQL 8.0     public 203.123.83.144    private 10.10.150.82   SGs: sg-shikisha + RMS-IPS
  Weego_and_marketing-analytics   MySQL 8.0.28  public 159.138.162.146   private 10.10.150.54   SGs: default
  election-prod-db2               MySQL 5.7     public 110.238.77.61     private 10.10.150.48   SGs: sg-Mysql + RMS-IPS
  visitors-database-cluster       MySQL 5.7     public 110.238.75.83     private 10.10.150.168  SGs: sg-Mysql + RMS-IPS
  dbms-trf-req-database-3         MySQL 5.7     public 159.138.175.179   private 10.10.150.121  SGs: sg-Mysql
  citizen-digital-dev-db-cluster  MySQL 5.7     public 159.138.164.124   private 10.10.150.206  SGs: sg-Mysql + sg-Citizen-Digital

RDS INSTANCES · ap-southeast-1 · owner tenant:
  rms-ai-pg                       PostgreSQL 16 no public                private 192.168.1.30   (SG lookup blocked by RDS API 403 in this region — admin should note the SG when granting)

RDS INSTANCES · af-south-1 · THIRD-PARTY TENANT (owner does not administer):
  USSD host                       MySQL 5.7.44  public 110.238.76.159    (currently reachable + authenticates; already LIVE)
  VIUSASA host                    MySQL 8.0     public 203.123.86.10     (SG blocks us today; other tenant's admin must whitelist)
  MICROSERVICES host              MySQL 5.7     public 159.138.164.93    (SG blocks us today; other tenant's admin must whitelist)

UNIQUE SECURITY GROUPS TO WHITELIST BASTION (5 IDs, af-south-1):
  aed8d060-16fc-489d-8b62-1a2c3ea45cca   name: RMS-IPS               (9 rules, 3 currently on 3306)
  2cc0ad09-8d8f-464d-9d39-4fe1f3052b57   name: default               (30 rules, 4 currently on 3306)
  803fb5f5-1f24-4d09-847d-e921a66b4e45   name: sg-shikisha           (5 rules, 0 currently on 3306 — hence rds-shikisha is unreachable to any external IP through this SG)
  92233ae5-f4d2-4ace-8685-023881e189f1   name: sg-Mysql              (15 rules, 12 currently on 3306)
  a6456cfb-696e-45c7-8147-13028a53dcea   name: sg-Citizen-Digital    (6 rules, 2 currently on 3306)
```

---

## Contact / hand-off

Once §3.A is complete (four policies attached at the two project scopes), please ping the delivery team. Provisioning of the bastion is ~5–8 minutes wall-clock and is fully automated on our side. §3.B (credentials) can be supplied in parallel or after — the bastion is not blocked by credentials arriving.

End of note.
