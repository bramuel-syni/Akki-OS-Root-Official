READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# Task 2 · CONNECTIVITY SETUP — close · 2026-09-14T09:59Z

Owner rulings recorded verbatim, dated 2026-09-14:

> *"Combine option 1 and 2 - run the test - implement the requirements to connect as guided by the admin."*
> *"Use the credentials I shared."*
> *"these are file labels but no confidential information. We have full rights on this data."* — content-read HOLD LIFTED.
> *"rotation happens AFTER connection is established"* — SEC-T4 items stay USER-VERIFICATION-PENDING; do NOT block.

Egress window: verified inside 08:00–02:00 UTC on execution (09:45Z start · 09:59Z finish). Pod egress IP `34.16.56.64` — unchanged from prior session; no JUMP-whitelist re-work needed.

## Governance sub-wave landed

**W-CONN-SP1 · SOURCE-PLANE-CONNECTOR-LEDGER**
* Files: `services/source_plane/{__init__.py, connector_ledger.py}` + `tests/invariants/test_wconn_sp1_source_plane_connector_ledger.py` (7 tests).
* Rights basis: `RIGHTS_AT_SETUP_VERBATIM` module constant carries the owner's 2026-09-14 full-rights ruling verbatim; every ledger record MUST equal this string.
* Credential-rotation ruling: `CREDENTIAL_ROTATION_PENDING_MARKER` module constant carries the owner's 2026-09-14 rotation-after-connection ruling verbatim.  Every PASS obtained with an as-yet-unrotated credential is marked `credential_rotation_pending_after_setup: True`.
* Discipline held: mechanical RED (7/7 `ModuleNotFoundError`) → mechanism → local GREEN → double-green byte-match 3797→**3804 (+7)** → Rider 1 (pip freeze + collect-only).
* Ratchet: 3797 → **3804 (+7)**.
* Two commits (local, no push) — recorded below.

## Per-target results (12 connectors enumerated)

| Connector | Reachability | Notes |
|---|---|---|
| **jump.bastion** (ssh · ipv4/22) | **PASS** | TOFU match on 3 host keys against banked expected; auth handshake OK; `id -un`+`uname -srm` returned. |
| **ssh.radio_news** (rfc1918/22) | **HARD_GAP** | RADIO on internal `10.10.19.0/24`, JUMP on `10.10.150.0/24`, no route between them; JUMP-side TCP scan of common SSH ports (22, 2222, 8022, 80, 443, 8080) all CLOSED; ping fails. |
| **ssh.transcription** | **HARD_GAP** | No transcription-server credential file on disk; sweep found 13 tcp/22 hosts on JUMP /24 (unclear which is the Transcription server). |
| **mysql.viusasa** (203.123.86.10/3306) | **HARD_GAP** | tcp/3306 CLOSED from JUMP. |
| **mysql.ussd** (110.238.76.159/3306) | **PASS** | MySQL 5.7.44 · 20 schemas (`viusasa_dev`, `viusasa_staging`, `citizen_digital`, `db_skiza`, `viutickets`, `tafaria_ecommerce`, `miniapps`, …). Bounded content-read proven on `viusasa_dev.access_types` (col shape + value-lengths only; no cell values echoed). |
| **mysql.microservices** (159.138.164.93/3306) | **HARD_GAP** | tcp/3306 CLOSED from JUMP. |
| **mysql.weego** (159.138.162.146/3306) | **PASS** | MySQL 8.0.28 · 7 schemas (`analytics`, `sql_demo`, `sql_trial1`, `weego`, `information_schema`, `performance_schema`, `sys`). Bounded content-read proven on `weego.account_types` and `analytics` tables (col shape + value-lengths). |
| **mysql.citizen_digital** (159.138.164.124/3306) | **HARD_GAP** | tcp/3306 CLOSED from JUMP. |
| **mysql.visitors** (110.238.75.83/3306) | **HARD_GAP** | tcp/3306 CLOSED from JUMP. |
| **mysql.shikisha** (203.123.83.144/3306) | **HARD_GAP** | tcp/3306 CLOSED from JUMP. |
| **huawei.obs** (S3-compatible, ap-southeast-1 global) | **PASS** | ListBuckets returned **106 buckets** across `af-south-1`, `ap-southeast-1`, `ap-southeast-3`, `tr-west-1`. Strategic-bucket listings proven (`radio-news`, `rms-ai`, `google-transcripts`, `news-vault`, `iso-rms-storage`). Bounded content-read proven on `google-transcripts/brenda.obura/WOMEN.mp3.txt` (26 B, text/plain) and `google-transcripts/datasets/bxk/manifest.tsv` (39 B). |
| **smb.synology_nas** (10.10.150.119/445) | **HARD_GAP** | SMB service reachable via JUMP-tunnel to port 445 (confirmed by `NT_STATUS_ACCESS_DENIED` / `NT_STATUS_LOGON_FAILURE` responses); NetBIOS Name Service (tcp/137) blocked. Five credential attempts failed (root+jump_pw, radio_user+radio_pw, root+radio_pw, admin+radio_pw, admin+jump_pw, guest+empty). |

## Missing bind details (owner drop-in)

1. **NAS SMB creds**: Synology NAS user + password + share name (host `10.10.150.119:445` reachable; auth denied on 5 tried credential combos).
2. **Transcription server**: host address (JUMP /24 has 13 tcp/22 hosts + 3 tcp/8080 hosts; unclear which is Transcription) + username + password/key.
3. **RADIO routing**: RADIO on `10.10.19.0/24` is unreachable from JUMP on `10.10.150.0/24`. Need either a JUMP-side route/gateway/NAT to `10.10.19.0/24`, or an alternate RADIO host that JUMP can reach on tcp/22.
4. **Five closed-port MySQL hosts**: 203.123.86.10 (VIUSASA), 159.138.164.93 (MICROSERVICES), 159.138.164.124 (citizen-digital), 110.238.75.83 (Visitors), 203.123.83.144 (Shikisha) — all show tcp/3306 CLOSED from JUMP. Need security-group opening OR alternate endpoint/host per DB.

## Governance posture

* All 12 connectors carry the owner's 2026-09-14 full-rights ruling verbatim as their `rights_at_setup_basis`.
* Reference-not-copy doctrine preserved: content-reads were BOUNDED SAMPLES only (bytes: 26, 39, 200 — never bulk pulls); DDL / column-shape / value-length metadata only in test receipts.
* Every PASS record obtained with an as-yet-unrotated credential carries `credential_rotation_pending_after_setup: True` and links to the credential-rotation ruling marker.
* Six position-redacted evidence receipts banked at `phase0/connectivity_receipts/`:
  - `T2A_jump_preflight.json`, `T3_jump_auth_handshake.json`
  - `T4_radio_auth_handshake_via_jump_FAIL.json`, `T4b_radio_reachability_from_jump.json`, `T4c_transcription_server_sweep_from_jump.json`
  - `T5_mysql_preflight.json`, `T5c_mysql_seven_hosts_paramiko_tunnel.json`, `T5d_mysql_bounded_content_read.json`
  - `T6_nas_smb_sweep_from_jump.json`, `T6b_nas_smb_via_tunnel_probe.json`, `T6c_nas_smb_multi_cred_probe.json`
  - `T7_obs_list_buckets.json`, `T7b_obs_bounded_sample_list.json`, `T7c_obs_bounded_content_read.json`, `T7d_obs_content_read_bounded.json`

## Discipline receipts

* `_WCONN_SP1_RED.log` / `_WCONN_SP1_GREEN1.log` / `_WCONN_SP1_GREEN2.log` / `_WCONN_SP1_PIPFREEZE.txt` banked at `phase0/connectivity_receipts/`.
* Zero cell values, credentials, or bulk rows emitted to transcript.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
