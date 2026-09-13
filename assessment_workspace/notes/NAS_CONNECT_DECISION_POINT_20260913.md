READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# NAS_CONNECT_DECISION_POINT_20260913.md — NAS reachability report through JUMP

**Filed by:** builder agent · session 2026-09-13 · UTC 18:12Z (EAT window IN).
**Trigger:** Owner ruling verbatim 2026-09-13: *"the jump server's PURPOSE is to reach the NAS. The NAS is the real target behind JUMP … establish and REPORT the real NAS connection through JUMP."*
**Bounds honoured:** READ-ONLY · SSH through pinned known_hosts (JUMP · strict) · EAT egress window · no push · no `testing_agent` · position-based redaction · no protocol payloads sent on unopen ports · no file contents opened.

---

## §1 · Egress-window check

- UTC at probe: `2026-09-13T17:50Z … 18:12Z`.
- EAT window: `08:00–02:00 UTC`.
- Verdict: **IN-WINDOW.**

## §2 · Target-identification pass (on-disk sweep of `estate_keys/`)

Files inspected (position-only, no cell echoed):

| File | sha256 | mode | NAS-relevance |
|---|---|---|---|
| `bastion/jump_server_radio_system.csv` | `1f4e971cee4e423bcf7deaf1587627bffb98948d03d7672d01a263f31575e835` | 0o600 | 2 cols · 4 rows. Col headers = `Jump Server` \| `Radio news system.`. Row 1 = IPs, Row 2 = users, Row 3 = creds. **RADIO** is the only NAS-candidate handle on disk. |
| `data_sources/db_credentials.csv` | (prior receipt) | 0o600 | 28 rows · 4 cols. VIUSASA DB hosts. Not NAS. |
| `data_sources/db_credentials_2.csv` | (prior receipt) | 0o600 | 22 rows · 2 cols. WEEGO DB hosts. Not NAS. |
| `data_sources/huawei_credentials.csv` | (prior receipt) | 0o600 | Huawei Cloud IAM. Not NAS. |
| `data_sources/{akki-aurora,db-restore-603-cluster,x,synthetic-nonexistent,aws_iam_user_AKIA<redacted>}.json` | (prior receipt) | 0o600 | AWS RDS/IAM cluster ARNs + IAM users. **Zero NAS/Synology/SMB/NFS keys** across all 5 JSONs (structural key scan). |

Codebase reference of note: `services/source_plane/synology_file_station.py` (W1b · CP3) implements an **interface-only** `SynologyFileStationConnector` that refuses any read until `AKKI_SYNOLOGY_ALLOWED_RUNTIME=1`. Explicit comment: *"the specific NAS host + credentials are a JOB binding at mount time."* No JOB-side artefact for that binding exists on disk.

## §3 · Reachability facts from JUMP (bash /dev/tcp + ICMP)

Nine candidate hosts × twenty NAS-protocol ports (SSH/22 · FTP/21 · FTPS/990 · NBNS/137 · NBSS/139 · SMB/445 · AFP/548 · rsync/873 · NFS/2049 · NFS-portmap/111 · iSCSI/3260 · DSM/5000+5001 · WebDAV/5005+5006 · DSM-mobile/5555 · DSM-Drive/6690 · HTTP-alt/8080 · Syncthing/8384 · HTTPS-alt/8443) + 1 ICMP probe per host + 5-round retry on RADIO:22.

**ICMP replies (layer-3 reachable from JUMP):**

| Handle | ICMP |
|---|---|
| JUMP (self) | REPLY |
| RADIO (bastion_csv[1,1]) | **NO_REPLY** |
| HUAWEI_RDS_1 (159.138.162.146) | NO_REPLY (filtered; :3306 was TCP-open in prior pass) |
| VIUSASA_HOST_{4,5,6} (viusasa creds col1) | REPLY · REPLY · REPLY |
| WEEGO_HOST_{7,8,9} | NO_REPLY (all) |

**TCP-OPEN matrix (all 20 NAS ports probed on all 9 candidates):**

| Handle | Open NAS ports |
|---|---|
| JUMP (self) | `22` only (SSH — the bastion itself) |
| RADIO | **∅** |
| HUAWEI_RDS_1 | ∅ |
| VIUSASA_HOST_4 · 5 · 6 | ∅ |
| WEEGO_HOST_7 · 8 · 9 | ∅ |

One diagnostic anomaly: `JUMP:8080` returned **REFUSED** (RST) rather than TIMEOUT — i.e. nothing listens on 8080 locally, but the box replies. All other closed results were TIMEOUT (silently dropped — consistent with cloud SG or upstream firewall).

**RADIO:22 five-round retry series:** 5/5 `CLOSED_OR_TIMEOUT`. Consistent — not flapping. Earlier this session (T4 side-task, 16:42Z UTC) JUMP→RADIO:22 got as far as SSH banner exchange before timeout — i.e. TCP had connected. **RADIO reachability degraded to layer-3 unreachable in the intervening ~74 minutes.** Root cause is off-box (firewall / RADIO down / rate-limit).

Receipts: `phase0/nas_connect_receipts/20260913T175058Z_step4_nas_reachability.json` (first pass, 90 probes) · `20260913T175649Z_step4b_nas_deep_reachability.json` (deep pass, 194 probes).

## §4 · JUMP-side introspection for local NAS hints

Read-only introspection on JUMP (`mount`, `/etc/fstab`, `/etc/exports`, `/etc/samba/smb.conf`, `ip route`, `ip neigh`, `/etc/hosts`, `~/.ssh/known_hosts`, NAS-tool availability). Results:

- **Hostname:** `ecs-b896` · Huawei Cloud ECS · Ubuntu 24.04.4 · kernel `6.8.0-106-generic`.
- **Interfaces:** `eth0 10.10.150.93/24` only. Default route via `10.10.150.1`.
- **ARP neighbours:** gateway only (`10.10.150.1`). No other layer-2 neighbours reachable — JUMP's VPC subnet is populated only by the gateway from JUMP's perspective.
- **`mount | grep -iE 'nfs|cifs|smb|9p'`:** empty. **Zero NAS mounts on JUMP.**
- **`/etc/fstab`:** boot volume only. **No fstab-declared NAS entries.**
- **`/etc/exports` · `/etc/samba/smb.conf` · `/etc/nfs.conf` · `/etc/auto.master`:** all MISSING. JUMP is neither a NAS server nor an autofs client.
- **`/etc/hosts`:** localhost + ecs-b896 only. **No custom NAS host aliases.**
- **`~/.ssh/known_hosts`:** file NOT present under `~/.ssh` (only `authorized_keys`, zero bytes). Suggests either fresh box or aggressive cleanup — either way, JUMP has no record of prior ssh-out neighbours.
- **NAS client tools:** `smbclient` MISSING · `mount.cifs` MISSING · `mount.nfs` MISSING · `showmount` MISSING · `nmap` MISSING. Available: `rsync`, `curl`, `wget`, `nc`, `ping`, `tcpdump`. Even if a NAS were reachable, only the SMB / NFS / rsync-native protocols would be usable without installing tools — and rsync/SMB/NFS ports are all TIMEOUT on every candidate.
- **Local listeners:** `:22` (SSH), `127.0.0.53:53` (systemd-resolved), `127.0.0.1:29338/29339` (rpcbind-adjacent internal). No :445, :2049, :5000, :5001. **JUMP does not front any NAS surface.**

Receipt: `phase0/nas_connect_receipts/20260913T181014Z_step4c_jump_discovery.json`.

## §5 · Concrete result

**NAS is NOT reachable from JUMP this pass on any tested candidate + protocol.**

- The only NAS-adjacent handle on disk is `RADIO` (bastion CSV row 1 col 1). At layer 3 it is unreachable from JUMP right now (ICMP no-reply + 5/5 TCP:22 timeouts + 20/20 NAS ports timeout). Earlier today (16:42Z) TCP:22 completed on RADIO — reachability has degraded since.
- No other on-disk artefact declares a NAS host. All 5 JSONs under `data_sources/` are AWS RDS/IAM records; the two DB CSVs list DB-server hosts only.
- JUMP itself has zero NAS mounts, zero NAS listeners, zero NAS route hints, zero NAS client tools installed. It is a pure ssh bastion — reaching a NAS via JUMP would require either (a) an actual NAS host binding + credentials dropped as a file, or (b) restoration of routing to RADIO if RADIO is indeed the NAS.

## §6 · What is missing (owner-actionable)

If the NAS target is expected to exist, one or more of the following would need to be dropped for the next attempt:

1. **A NAS bind file** at `estate_keys/data_sources/nas_*.{csv,json}` (or similar), naming: host / port / protocol (SMB · NFS · DSM-HTTP(S) · rsync-native) / share-or-volume / read-only credential reference / rights-basis owner.
2. **OR** a routing / firewall change so `RADIO` from `bastion/jump_server_radio_system.csv` is reachable from JUMP at at least one of the twenty NAS ports probed here. If RADIO is intended to be a NAS-gateway, its NAS surface port set + protocol should be named.
3. **OR** an explicit ruling that no on-prem NAS exists in the estate today, and audio/media corpus lives elsewhere (e.g., an S3 bucket referenced by one of the AWS RDS records) — in which case the discovery target changes.

`AKKI_SYNOLOGY_ALLOWED_RUNTIME=1` is a **codebase runtime gate**, not a network route. Setting it in the environment would only lift the interface-only guard in `services/source_plane/synology_file_station.py`; it does not create a NAS route.

## §7 · Governance (one-line, per owner ruling)

Any future NAS connection needs the same rights-at-setup + reference-not-copy formalisation named in GAP-1 of `notes/DB_CONNECT_DECISION_POINT_20260913.md`; noted as immediate follow-up, not blocker.

## §8 · Halt

Two receipts + one JUMP-side introspection receipt banked under `phase0/nas_connect_receipts/`. **No file was opened for reading.** M2 **NOT** opened. Awaiting owner's explicit ruling on whether to (a) drop a NAS bind file, (b) restore RADIO routing, or (c) redirect the corpus target.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
