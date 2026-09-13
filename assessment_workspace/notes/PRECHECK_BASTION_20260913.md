READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# PRECHECK_BASTION_20260913.md — connection-credential precheck receipt

**Purpose.** Non-secret, handle-only record of the bastion/radio connection-credential precheck ordered by the owner as a HARD GATE before `W-REGISTRY-EXTENSION-G3` (owner-ruled label 2026-09-13; distinct from the prior `W-REGISTRY-FULL-BUILD` wave of 2026-09-09).

**Standing.** Read-only, notes/-only. No code, no ratchet touch, no push. Secret material referenced by handle only; never echoed to this file, to logs, to git tree, or to any surface.

**Date.** 2026-09-13T09:07Z (UTC clock at test time).

---

## §0 Source of record

- **CSV file**: `/app/backend/estate_keys/bastion/jump_server_radio_system.csv`
- **file_sha256**: `1f4e971cee4e423bcf7deaf1587627bffb98948d03d7672d01a263f31575e835`
- **file_size_bytes**: 101
- **file_mode**: `0o600`
- Retrieved from `https://customer-assets-cm19k8pv.emergentagent.net/job_amazing-gates-8/artifacts/mx17ewcv_Jump%20Server%20%2B%20Radio%20System.csv` per owner directive this session.

## §1 Connection matrix (handle-only)

| Field | JUMP | RADIO |
|---|---|---|
| role | Jump Server | Radio news system. |
| host-handle | `ip_handle_d13a2633` | `ip_handle_26563d0d` |
| host-family | IPv4 | IPv4 |
| user-label | `root` | `ubuntu` |
| cred-kind | `LIKELY_PASSWORD` | `OPAQUE_UNKNOWN` |
| assumed proto | SSH tcp/22 [session assumption; CSV has no explicit port/protocol column] | SSH tcp/22 [same assumption] |
| reached via | direct | through JUMP (bastion pattern, owner note) |

**Session assumption declared explicitly**: CSV had no port/protocol column, so SSH tcp/22 was assumed for both targets. If either target speaks something other than SSH-on-22 (e.g., a management port, custom SSH port, or an application-layer protocol like MQTT/RTSP for the Radio system), owner rules and this precheck extends.

**cred-kind classification rules used** (no secret content leaked; classification uses shape only):
- `INLINE_PRIVATE_KEY` = contains "-----BEGIN … PRIVATE KEY-----"
- `FILEPATH_TO_KEY` = starts with `/` and path exists
- `LIKELY_PASSWORD` = matches `[A-Za-z0-9!@#$%^&*()_+\-=.,]{4,32}`
- `LIKELY_INLINE_KEY_MATERIAL` = length > 100
- `OPAQUE_UNKNOWN` = none of the above

## §2 Egress-window timezone reasoning (SO §3, no-silence)

Owner window rule: **11:00–05:00 (open) / 05:00–11:00 (closed)**. Owner did NOT specify timezone. Three plausible operator zones considered:

| Zone | Local time at test | Hour | Window verdict |
|---|---|---|---|
| UTC (as-is) | 09:06 | 09 | **OUTSIDE** (deep probes HOLD; ~1h54m to 11:00 UTC) |
| EAT / Africa/Nairobi (UTC+3) | 12:06 | 12 | **INSIDE** (open until 05:00 EAT tomorrow) |
| CAT/SAST (UTC+2) | 11:06 | 11 | **INSIDE** (5 min past open) |

Fork-context inference (Canon-4 §50.1 lists Swahili, Sheng, KenCorpus, Kenyan/East African corpora as speech de-risking strata) points to **Africa/Nairobi (EAT)** as the most operationally-plausible zone. But this is inference, not owner ruling. **I do not know which timezone the 11:00–05:00 rule refers to. Requesting owner ruling.**

Conservative posture applied while ambiguity stands: treat as OUTSIDE for anything that would touch the Radio operational plane. Lightweight non-disruptive checks against the JUMP server proceed under owner's own carve-out.

## §3 Pod egress fingerprint (Issue-4 diagnostic)

Fork context: "Issue-4 was egress-IP drift breaking security-group whitelists — if you see a timeout that looks like whitelist/IP drift, say so distinctly from an auth rejection."

- **Pod public egress today**: `34.16.56.64` (per `https://ipinfo.io/ip`, non-secret — this is the source IP as the internet sees us).
- **Diagnostic outcome**: TCP reach to JUMP:22 succeeded (T1 PASS below). Whitelist/IP-drift is NOT a blocker for JUMP today with pod egress `34.16.56.64`.

## §4 Test results (per target, handle-only evidence)

### T1 · TCP reach to JUMP:22 (safe, no auth, no work) — **PASS**
- Method: python `socket.create_connection((host, 22), timeout=12)`, read up to 200 bytes of banner.
- Evidence: `banner_bytes=43  banner_prefix_ascii='SSH-2.0-OpenSSH_9.6p'`
- Verdict: JUMP is reachable from `34.16.56.64` on tcp/22 today. IP-drift ruled out for JUMP.

### T2 · JUMP SSH host-key fingerprints (public, non-secret) — **PASS**
- Method: `ssh-keyscan -T 5 -p 22 <jump-handle>`, SHA256 fingerprint per public host key.
- Received 3 host keys. Fingerprints banked here for chain-of-custody:

| type | SHA256 fingerprint |
|---|---|
| `ssh-rsa` | `SHA256:qEUrMRNdP9rUzetuJ2qYMDKGFrUlLUeaVI6UHPaM/Xc` |
| `ecdsa-sha2-nistp256` | `SHA256:dMz9wmWATBTN1pfwmxvLpMvcdchm77aaVr3q0zIOmk8` |
| `ssh-ed25519` | `SHA256:W45xvjhsARJOcFj9U/bcWC3KDte30T+Amu3eCx4UrwU` |

These are public keys (safe to bank). Owner should verify at least one fingerprint against a known-good record on the operator side before permitting production traffic. If any of these fingerprints does NOT match what the operator expects, treat as an active MITM finding and halt (do not proceed with T3 evidence — the credential may already be compromised).

### T3 · JUMP SSH auth handshake (owner-carve-out: authenticates, does NO work) — **PASS**
- Method: `SSH_ASKPASS` + `setsid -w ssh -o BatchMode=no ...`. Secret placed in a `0600` tempfile in `/dev/shm/sshask_<random>/`, an askpass wrapper (`#!/bin/sh` `exec cat <secret_file>`) served the value once, entire workdir removed in `finally`. Secret never touched argv, env, stdout, stderr, log, or git tree.
- SSH options: `PubkeyAuthentication=no`, `PreferredAuthentications=password,keyboard-interactive`, `NumberOfPasswordPrompts=1`, `ConnectTimeout=10`, `LogLevel=ERROR`, `StrictHostKeyChecking=no`, `UserKnownHostsFile=/dev/null`.
- Remote command run (does no work): `echo AUTH_OK && id -un && uname -srm`.
- Evidence:
  - `rc=0`
  - stdout contains `AUTH_OK`
  - remote `id -un` = `'root'`  (matches CSV user-label)
  - remote `uname -srm` = `'Linux 6.8.0-106-generic x86_64'`
  - Secret cleanup verified: workdir removed, `workdir_exists=False`.
- Verdict: JUMP credential in the CSV is VALID. The bastion accepts our egress IP `34.16.56.64` and the stored credential.

### T4 · RADIO deep probe (auth handshake through JUMP to RADIO) — **HELD**
- Reason: Radio operational plane is touched by this test. Owner window rule 11:00–05:00 has ambiguous timezone (§2). Conservative posture: HOLD until owner rules on timezone.
- Not attempted at all — no TCP reach through the bastion to the radio-handle, no auth attempt. HELD entirely.
- Next window (per §2):
  - If **UTC**: opens 11:00 UTC today (approx 1h54m from test time).
  - If **EAT**: currently INSIDE (until 05:00 EAT tomorrow, i.e. 02:00 UTC on 2026-09-14).
  - If **CAT**: currently INSIDE (until 05:00 CAT tomorrow, i.e. 03:00 UTC on 2026-09-14).

## §5 Failure classification legend (for future runs)

If a future TCP or auth attempt fails, classify per this legend (matches owner's Issue-4 language):

| Symptom | Classification | Root cause hypothesis |
|---|---|---|
| TCP timeout, no banner | `NETWORK_TIMEOUT (likely whitelist/IP-drift)` | Pod egress IP not on the bastion's allowlist; Issue-4 pattern. |
| TCP connection refused | `CONNECTION_REFUSED` | Port not listening OR host firewall blocks after handshake. |
| TCP OK, ssh "Permission denied" | `AUTH_REJECTED_permission_denied` | Credential rejected; not a network problem. |
| TCP OK, ssh "Host key verification failed" | `HOST_KEY_ISSUE` | Host key drifted or MITM. Halt until fingerprint verified against §4 T2 table. |
| TCP OK, ssh hangs past ConnectTimeout | `NETWORK_TIMEOUT` (post-TCP) | Stateful firewall dropping mid-session. |

## §6 Standing operational constraint recorded

Per owner directive this session: **egress against the on-prem environment / additional data system is permitted ONLY within the window 11:00–05:00 (avoid interrupting daily operation). Operations that do not affect day-to-day system function may run anytime.**

Timezone for this window: **PENDING OWNER RULING** (see §2).

## §7 What this precheck does NOT do

- Does not verify Radio system reachability, credential validity, or protocol assumptions (T4 HELD).
- Does not confirm the CSV's port/protocol assumption for either target (session assumption in §1).
- Does not authorise `W-REGISTRY-EXTENSION-G3` to open. That authorisation is owner-gated per this session's ruling: "Do NOT write any W-REGISTRY code until the precheck result is reported and I relay owner go."

## §8 Ready for owner ruling

**Outcome**: JUMP-side precheck complete. JUMP credential VALID. Radio-side deep probe HELD.

**Owner rulings requested**:
1. **Timezone** for the 11:00–05:00 window (UTC / EAT / CAT / other) — unblocks T4.
2. **Go / no-go on `W-REGISTRY-EXTENSION-G3` open** now that JUMP-side is proven — since it does not itself depend on the Radio system (per Phase C plan §D), owner may open it before T4 completes if that sequencing suits.
3. **T4 execution mode** once window is inside: SSH auth handshake only (no radio-plane work), same `SSH_ASKPASS`+`setsid` discipline as T3, radio credential kind (`OPAQUE_UNKNOWN`) to be classified on inspection at test time.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
