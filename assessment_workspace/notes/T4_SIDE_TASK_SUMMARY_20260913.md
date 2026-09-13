READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# T4_SIDE_TASK_SUMMARY_20260913.md — RADIO deep-probe held-and-released outcome

**Filed by:** builder agent · session 2026-09-13.
**Trigger:** Admin ruling on the four bastion verification questions (session message) unblocked the held RADIO T4 side-task under the ratified block sequence. Executed at the natural sub-wave boundary between CP10 close (2026-09-13T16:34Z) and G-3 open.

---

## §1 Owner rulings ratified

**EAT window ruling (verbatim, owner 2026-09-13):** *"Timezone is EAT."*
The DEFAULT-PENDING-OVERRIDE from PRECHECK_BASTION_20260913.md §2 is
RESOLVED. Effective egress window against the on-prem estate =
**11:00–05:00 EAT (UTC+3) = 08:00–02:00 UTC**. All future T4-style
egress uses the EAT window; the earlier conservative-intersection
default (11:00–02:00 UTC) is superseded.

**Bastion Q&A rulings (admin, verbatim structure):**
1. HOST-KEY: TOFU authorised. JUMP fingerprints (T2 SHA256 · rsa/ecdsa/ed25519) pinned to `/app/backend/estate_keys/known_hosts` (0600). Same TOFU-pin discipline applied to RADIO on first-connect via `StrictHostKeyChecking=accept-new`.
2. EGRESS WINDOW TIMEZONE: EAT (see above); intersection default replaced.
3. RADIO CRED TYPE: classified at execution — 14 chars, OPAQUE_UNKNOWN by shape (not matching password regex nor filepath); driver treats as password.
4. IP WHITELISTING: none; port 22 public. Recorded as SEC-2026-09-13-T4-02 hardening observation for owner's later attention; NOT acted on.

## §2 Execution timeline

- 2026-09-13T16:41Z — pinned JUMP host keys to `/app/backend/estate_keys/known_hosts` (0600). 3/3 fingerprints match T2. `ssh-keygen -F` confirms all three keys findable.
- 2026-09-13T16:42Z — v1 T4 driver run (receipt `20260913T164231Z_T4_bastion_handshake.json`). Bug: pty tail re-match caused RADIO pw to be written after JUMP auth (RADIO had not prompted); ssh reported "Connection timed out during banner exchange" on the JUMP→RADIO channel. RADIO credential scrubbed in-memory before receipt write — never persisted to disk. Driver classified as buggy; SEC-2026-09-13-T4-03 filed.
- 2026-09-13T16:45Z — v2 T4 driver run (receipt `20260913T164513Z_T4_bastion_handshake.json`) with `consumed_bytes` buffer-burn fix. Clean run: 1 password prompt (JUMP only, fed successfully), no fingerprint prompt (JUMP already trusted via pinned known_hosts), same RADIO banner-exchange timeout.

## §3 Authoritative verdict

| Target | Status | Classification |
|---|---|---|
| **JUMP** (`ip: 159.138.173.250` · `user: root` · `cred: LIKELY_PASSWORD (12 chars)`) | **PASS** | Auth-handshake proven again (T3 result reproduces under strict TOFU pin). Host-key TOFU pin verified 3/3 vs T2. |
| **RADIO** (`ip: <IPv4 from CSV row 1 col 1>` · `user: ubuntu` · `cred: OPAQUE_UNKNOWN (14 chars)`) | **FAIL** | `NETWORK_TIMEOUT (post-TCP)` per `PRECHECK_BASTION_20260913.md §5`. ssh reported "Connection timed out during banner exchange" on the JUMP→RADIO channel; RADIO never emitted a password prompt. Auth VERIFICATION NOT COMPLETED. |

**Root-cause hypotheses (per precheck §5 legend, in order of plausibility):**
1. Stateful firewall between JUMP and RADIO dropping the mid-session forwarding channel.
2. RADIO listening on a port other than the assumed `tcp/22` (session assumption declared in precheck §1).
3. RADIO not currently up.

## §4 Security observations (filed; NOT acted on)

- **SEC-2026-09-12-01** (pre-existing): leaked HF token in prior session transcript. Owner-side rotation still pending.
- **SEC-2026-09-13-T4-01 (new)**: earlier session-cell in this session inadvertently echoed the JUMP password (12 chars, CSV row 3 col 0) into the transcript during a CSV structure-inspection code fragment. **Owner-side rotation required.** Alongside SEC-2026-09-12-01.
- **SEC-2026-09-13-T4-02 (new, admin note)**: public-internet root SSH with password auth is a hardening risk. Owner attention only; NOT acted on.
- **SEC-2026-09-13-T4-03 (new)**: v1 driver buffer-bug wrote the RADIO cred to the pty during JUMP-to-RADIO channel setup; scrubbed in-memory; no persist to disk. **Proximity-to-leak event.** Recommend rotating the RADIO credential alongside the JUMP rotation.

## §5 What T4 did NOT do

- Did **not** run any operational command on JUMP or RADIO. `id -un && uname -srm` was the ONLY remote command intended, and it did not execute on RADIO (channel timed out before RADIO handled the payload).
- Did **not** open any RADIO-plane work (per admin: "Auth-handshake ONLY").
- Did **not** change any config on JUMP or RADIO (per admin rule 4).
- Did **not** push anything to a remote git.

## §6 Effect on the ratified block

- **T4 side-task complete** — receipt banked, verdict recorded.
- **Does not block the build** per admin instruction "do not block the build on it".
- **Continue block**: next item per G-A ratified sequence is **G-3 full-closure remainder** (bind to Doc-0 G-3 / BR-4.1 in wave-open grounding brief).
- **W-DAP-STACK** and **W-REGISTRY-FULL-BUILD CP10** already closed this session (see rollups).

## §7 Handles to receipts + tools banked with this side-task

- `phase0/drill_receipts/20260913T164231Z_T4_bastion_handshake.json` (v1 driver, buggy — kept as honest history)
- `phase0/drill_receipts/20260913T164513Z_T4_bastion_handshake.json` (v2 driver, clean — authoritative)
- `tools/t4_bastion_handshake.py` (v2 driver source — stdlib-only, no pexpect/sshpass)
- `/app/backend/estate_keys/known_hosts` (0600, 3 JUMP host keys pinned)

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
