# S2 · SCHEMA-SURVEY-NAS — state note (2026-09-21)

**Wave**: CP-ESTATE-INGESTION.
**Slice**: S2 · SCHEMA-SURVEY-NAS (read-only, no downloads).
**Owner GO**: 2026-09-21T~13:35Z (verbatim: "OWNER GO → S2 · SCHEMA-SURVEY-NAS
(read-only), to answer the owner's direct question: 'can we read the NAS
contents entirely?' Non-interrupting to the R-91 hold; strict read-only,
no downloads.").
**R-91 hold**: unchanged (~38h away). **Ratchet floor**: 5858 (unchanged).
**S1 / S3**: still gated pending separate owner GO.

## Receipts banked (state repo)

* `phase0/connectivity_receipts/20260921T132205Z_NAS_schema_survey_S2_owner_authorized_20260921.json` — v1: vantage sweep + DSM API map + DSM auth probe (rejected 400).
* `phase0/connectivity_receipts/20260921T132533Z_NAS_schema_survey_S2_v2_auth_matrix_and_smb_enum_20260921.json` — v2: DSM POST auth matrix (v2/v3/v6/v7) + SMB via JUMP.
* `phase0/connectivity_receipts/20260921T132733Z_NAS_creds_structure_probe_S2_v3.json` — value-blind loader-parse sanity (loader is correct; user_len=7, pass_len=8 match the sheet).
* `phase0/connectivity_receipts/20260921T132947Z_NAS_smb_final_layer_pin_S2_20260921.json` — SMB2/native/anon final matrix + DSM unauth banner ping.

## Vantage

| step | vantage | outcome |
|---|---|---|
| A · direct egress from sandbox pod | attempted first | **TCP_TIMEOUT** on all of 5000/5001/445 (LAN-only NAS, as expected) |
| B · via JUMP paramiko direct-tcpip | used | **OK**; SSH connect 1.98s; host key `ssh-ed25519 SHA256:W45xvjhsARJOcFj9U/bcWC3KDte30T+Amu3eCx4UrwU` matches T3 handshake (no drift) |

DSM HTTP 5000, DSM HTTPS 5001, and SMB 445 ALL reachable through the JUMP tunnel.
DSM 5001 TLS 1.3, cert SHA `4c3f7700feb06995ee8f4cdb7be82e5b682f76da503c556f8170ff8c3cc7c4a9`.
DSM HTTP 5000 is fronted by nginx and answers `/`, `/webman/login.cgi`, and
the full `SYNO.API.Info` map (74.5KB) without auth.

## The owner's explicit question: "can we read the NAS contents entirely?"

**ANSWER (2026-09-21T13:30Z): CANNOT ANSWER TODAY — banked NAS credentials
are STALE.** The credentials in
`/app/backend/estate_keys/data_sources/RMS_Connection_Creds.xlsx` (sha256
`d778eb1eb2cbe94a7f994eec8d5b6584108b85a7522426ec057dc3613d9b72db`, "NAS
creds" sheet, user_len=7 / pass_len=8) are REJECTED by:

* SMB service on 10.10.55.55:445 → `NT_STATUS_LOGON_FAILURE` (across `-m SMB2` / `-m SMB3` / native negotiation).
* SMB anonymous `-L` → `NT_STATUS_LOGON_FAILURE` (guest disabled).
* DSM 7 HTTP on 10.10.55.55:5000 → `SYNO.API.Auth` error 400 (`NO_SUCH_ACCOUNT_OR_WRONG_PASSWORD`) across POST/GET × versions 2, 3, 6, 7.

Every OSI layer above them is HEALTHY:
* JUMP SSH: OK, host key un-drifted.
* JUMP → 10.10.55.55:5000 TCP: OPEN.
* JUMP → 10.10.55.55:5001 TCP + TLS 1.3 handshake: OK.
* JUMP → 10.10.55.55:445 TCP: OPEN (server responds to SMB session-setup,
  it just rejects auth).
* DSM API surface: fully responsive to unauth GETs.

**Root-cause hypothesis (verifiable by admin)**: the NAS password was
rotated at some point after the 2026-09-14 T3 handshake (when THIS
same sheet-shape read files successfully off share `OFFAIRRECS`) and
either (a) the 2026-09-16 sheet delta-drop transcribed the new NAS
password incorrectly, or (b) a subsequent rotation has not been
propagated to this sheet. The loader is not at fault — the value-blind
structure probe (v3 receipt) confirms it is reading the correct row
and computing the correct lengths. This is a credentials-hygiene event,
not a network or code event.

**Distinction (owner-requested)**: because auth fails, we cannot
separate "share not visible to this account" from "visible but
read-denied" today. Both classes collapse into "unknown pending
credential restore".

## Admin-flag / scope classification

Cannot be computed today. `SYNO.FileStation.Info.is_manager` and
`SYNO.Core.Desktop.Initdata.is_admin` both require a valid `_sid`.

## Historical baseline (from 2026-09-14 T3 receipts — CITED, not re-derived)

For the RMS admin's reference, the LAST KNOWN-GOOD enumeration under
the (now-superseded) pre-rotation credentials:

* **Visible shares (`smbclient -L`)**: `ADS`, `ATTENDANCE`, `BACKUP1`,
  `COMMERCIALS`, `GRAPHICS`, `HRMIS`, `NetBackup`, `NEWSCLIPS`,
  `PROMOS`, `video`, `web`, `web_packages`, plus `IPC$` (12 disk + 1 IPC).
* **Readable at the time (bounded probe)**: `OFFAIRRECS` (`offairrecs`
  case-normalized — note: not present in the browse list; accessible
  via direct connect only, suggesting `Hide from My Network Places` set
  on that share).
* **Visible-but-read-denied at the time**: `ATTENDANCE`, `HRMIS`,
  `video`, `web`, `web_packages`, `BACKUP1`, `NetBackup`, `GRAPHICS`.
* **Volume scale**: `52,437,524,156` blocks of 1024B (~48.85 TiB) with
  ~3.9 TB free.

**Classification of the 2026-09-14 scope (post-hoc summary of the
banked matrix)**: `PARTIAL — visible: 12 disk + 1 hidden (OFFAIRRECS);
readable: 1 (OFFAIRRECS only); denied on read: 8. NO admin scope.`

This is very much NOT "full NAS read". Even under the historical
credentials the answer to "can we read the NAS entirely?" was **NO;
partial, single content share** — likely a service-account-scoped role.

## Security-posture observations (for the record; not blockers)

* All traffic in this drill traversed the SSH-encrypted paramiko
  `direct-tcpip` channel; **no credential material transited any public
  wire in cleartext**. The DSM HTTP auth call itself is HTTP (port
  5000) but the *entire* wire path from this pod to DSM was inside SSH.
* DSM offers HTTPS on port 5001 (TLS 1.3 with AEAD suite
  `TLS_AES_256_GCM_SHA384`). A tightening ask for the admin: once
  credentials are refreshed, prefer 5001 for any future automated auth.
* JUMP host key un-drifted since T3 (2026-09-14).

## Action items surfaced (not executed — for the owner)

1. **Ask the RMS admin** to confirm the current NAS user + password.
   Provide the drop back via the standard custody channel with a new
   sha256 pin (per SO §4.1 §F).
2. **When re-dropped**, this same tool (`tools/nas_schema_survey_20260921.py`
   for DSM HTTP path, plus the SMB fallback in the v2 tool) will run
   the full read-only enumeration without modification.
3. **Optional scope-grant**: even under refreshed credentials, if the
   2026-09-14 scope holds (1 readable share out of 13 visible), an
   admin scope-grant would be required to answer the "entirely?"
   question with a YES.
4. **NO change to R-91 hold, ratchet floor (5858), or S1/S3 gates.**

## Hygiene tally

* Read-only across every probe. **ZERO downloads**. **ZERO writes**.
* All secrets held in memory only; passwords passed to `smbclient` via
  an authentication file staged in JUMP tmpfs (`/dev/shm/nas_auth.*`),
  `shred -uz`'d after use — confirmed by receipt.
* No secret value entered stdout, no log, no receipt.
* DSM `_sid` was never issued (auth failed) so no logout was needed
  (v1 still called `dsm.logout()` as a defensive no-op).
* `paramiko` `SSHClient` and `Transport` closed cleanly in each run.
* JUMP host key fingerprint bank-comparable across runs (matches T3).

— end of state note.
