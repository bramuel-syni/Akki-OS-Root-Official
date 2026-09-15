READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# ADMIN_BINDS_20260915.md

**Purpose.** Durable ledger for admin-provided infrastructure bindings received 2026-09-15T~04:25Z. Supersedes prior ledger entries where noted; entries below remain authoritative going forward.

**Provenance.** Owner turn 2026-09-15T~04:25Z, delivering admin's response to prior admin-item queue (Admin-item 2 · Admin-item 3 partial · Admin-item 4 unchanged).

**Handling discipline.** Every entry redacted per position-redaction hard-lock. Credential values stored under `/app/backend/estate_keys/data_sources/` at mode 0600 · referenced here by storage path + length + sha256 only.

**Related bank:** `STATE/DECISIONS.md` 2026-09-15T~04:25Z (owner ruling verbatim with password redaction).

---

## §A · MySQL security group openings · Admin-item 2 (partial resolution)

Admin has opened/is opening TCP 3306 for JUMP-side probes from `159.138.173.250` on 2 of the 5 previously-blocked MySQL hosts:

| Host tag | IP (admin-authoritative 2026-09-15) | Port | Prior ledger IP (superseded) | Access pattern | Status |
|---|---|--:|---|---|---|
| `citizen_digital` | **`159.138.164.103`** | 3306 | `159.138.164.124` (scratch files under `tools/_scratch/`) | from JUMP · schema-only reads | Admin bind arriving 2026-09-15 · probe at 08:00 UTC egress open |
| `visitors` | **`110.238.75.83`** | 3306 | (no prior stale entry · scratch files already carried this IP) | from JUMP · schema-only reads | Admin bind arriving 2026-09-15 · probe at 08:00 UTC egress open |

**Shared credential** filed at:
- Path: `/app/backend/estate_keys/data_sources/admin_bind_20260915_bramuel_cd_visitors.json`
- Mode: `0600` (root:root · verified by `stat`)
- SHA256: `a7a616be4577319d10387f15e2e6302e508f1cddc035d017dda8bd7d8717f70d`
- Size: 1321 bytes
- Password length: 12
- Password class: alphanumeric mixed case
- **Never echoed** in transcript / receipt / note / commit-message going forward per owner directive.

**Remaining 3 MySQL hosts** still awaiting admin-side SG opening: (unnamed this turn — admin scoped this bind to CD + Visitors only). Carry as owner-desk item until admin binds the remaining 3.

## §B · RADIO routing · Admin-item 3 (partial · new approach)

Admin verbatim (2026-09-15T~04:25Z): *"We will provide you with 10.10.55.x based IPs for access to these services, this is being handled this morning."*

**Status:** **INBOUND-BIND-PENDING** — awaiting admin's IP-set delivery. Probe when IPs arrive.

**Supersedes:** prior `notes/TASK_CONNECTIVITY_REDO_ADMIN_GUIDED_CLOSE_20260914.md:31` HARD_GAP verdict on `10.10.19.0/24`. New approach uses `10.10.55.x` subnet (same subnet as NAS which is proven reachable via JUMP → simplifies routing path).

**Blocker status:** `BLOCKER-RADIO-ROUTING-01` SUPERSEDED (no longer blocking on 10.10.19.0/24 route). New transient blocker: admin's IP-set delivery. Not on the critical path for M5 completion; RADIO integration is downstream (post-M6 audio-plane work · not this session's next hard action).

## §C · Transcription server · Admin-item 4 (unchanged)

Admin has NOT dropped transcription-server host+creds this turn. Prior `SEC-BIND-01` state unchanged: pending owner drop-in for host + creds. Not on the critical path for M5 completion; the D12 POC uses the CI whisper-tiny fixture on GPU hosts akki-vm/akki-vm-ii per owner ruling 2026-09-15T~03:55Z (production model selection follows §A17.11 separately).

## §D · Standing bind-gap ledger after this turn

| # | Owner-desk item | State | Impact on M5 completion path |
|--:|---|---|---|
| 1 | MySQL SG opening · `citizen_digital` (`159.138.164.103:3306`) | ✅ **UNBLOCKED** by admin (this turn) · probe at 08:00 UTC | Expands census scope (Effect 6 in DECISIONS.md) |
| 2 | MySQL SG opening · `visitors` (`110.238.75.83:3306`) | ✅ **UNBLOCKED** by admin (this turn) · probe at 08:00 UTC | Expands census scope (Effect 6 in DECISIONS.md) |
| 3 | MySQL SG openings · other 3 hosts (Weego backup · Voter · third) | ⛔ still pending (admin scoped this turn to CD + Visitors only) | Not blocking M5 · unmeasured-with-reason A5.4 |
| 4 | RADIO routing (`10.10.55.x` IPs) | ⛔ INBOUND-BIND-PENDING (admin: "this morning") · former `10.10.19.0/24` approach SUPERSEDED | Not blocking M5 · downstream (post-M6) |
| 5 | Transcription server host + creds | ⛔ pending owner drop-in · unchanged | Not blocking M5 · D12 POC uses whisper-tiny CI fixture |
| 6 | `SEC-2026-09-15-05` rotation | ⛔ owner-side · post-connectivity-verification | Not blocking · SEC ledger state PENDING-OWNER-ROTATION-POST-VERIFICATION |

## §E · Position-redaction acknowledgement

Every field above:
- Cites disk-file paths + line numbers where relevant.
- Does not echo the credential value (12-char alphanumeric mixed case · referenced by storage path + length + sha256 only).
- Preserves admin verbatim quotes.
- Uses host tags + IPs at the granularity admin provided (IPs are network-address values, not credentials · not subject to position-redaction).

---

## §G · EXTERNAL-RESEARCH · Huawei-Viusasa migration reframe (2026-09-15T~15:52Z · owner-passed research · NOT canon)

**Provenance:** owner-passed public-web research summary 2026-09-15T~15:52Z. Marked **EXTERNAL-RESEARCH not canon** per owner directive. Verbatim owner note banked at receipt time.

### G.1 · Findings (verbatim from owner)

1. Viusasa (operated by Content Aggregation Limited, RMS ecosystem) MIGRATED from private cloud to Huawei Cloud — one-stop OTT stack (VOD, Media Processing Center transcoding HLS/DASH/MP4, CDN, live streaming), availability now 99.99%. Source: `huaweicloud.com/intl/en-us/cases/royalmediaservices.html`.
2. Data layer: **GaussDB(for MySQL) on Huawei Cloud** is used for user-behavior analysis — the live Viusasa database is likely a Huawei Cloud GaussDB(for MySQL) instance, NOT the on-prem host in the current ledger (viusasa `203.123.86.10`, port closed, tagged on-prem).
3. App stack per public sources: Angular frontend, Flutter mobile, Laravel/PHP backend, MySQL + PostgreSQL + Redis, M-PESA billing.
4. May 2024: RMS + Huawei + Mango TV MoU on AI-powered media.

### G.2 · Implication for the bind-gap ledger

The `viusasa 203.123.86.10` on-prem IP may be legacy/stale.

**Revised admin ask (preferred bind path — bank as the preferred item):**

> Viusasa GaussDB(for MySQL) endpoint hostname + read-only creds + security-group opening for JUMP `159.138.173.250` — same pattern as the working weego/ussd Huawei RDS binds.

**Fallback:** keep the on-prem IP `203.123.86.10` as a fallback probe target in case the migration is not 100% complete.

**Shikisha reframe (parallel unknown):** same logic MAY apply to `shikisha 203.123.83.144` (currently tagged on-prem). Flag as **UNKNOWN — needs admin confirmation** whether shikisha has also migrated to a Huawei Cloud GaussDB(for MySQL) instance.

### G.3 · Ledger update — Standing bind-gap table (append)

| # | Owner-desk item | State | Impact on M5 completion path |
|--:|---|---|---|
| 7 | **Viusasa GaussDB(for MySQL) endpoint + creds + SG opening for JUMP** (revised preferred path per §G.2 · EXTERNAL-RESEARCH) | ⛔ ADMIN-BIND-PENDING · fallback: `viusasa 203.123.86.10` on-prem | Not blocking M5 · unmeasured-with-reason A5.4 · candidate M6 census expansion |
| 8 | **Shikisha bind-status confirmation** (`shikisha 203.123.83.144` may be migrated to Huawei Cloud GaussDB · admin to confirm on-prem vs cloud) | ⛔ UNKNOWN · admin confirmation required | Not blocking M5 · unmeasured-with-reason A5.4 · candidate M6 census expansion |

### G.4 · Provenance discipline (banked · EXTERNAL-RESEARCH class)

- Item 7 + Item 8 are EXTERNAL-RESEARCH-SOURCED per owner directive; they are not canon anchors.
- No mechanism is landed on the basis of this research this session — the code and invariants remain unchanged.
- The reframe surfaces the revised admin ask; ratification of the reframe (and any follow-on registry-writer walk if binds land) awaits owner ruling + admin action.

---

## §F · Next action pin (post-this-turn)

**AT 08:00 UTC egress re-open** — sequenced per `STATE/NEXT.md` refreshed pin 2026-09-15T~04:25Z:

1. Probe `citizen_digital` (`159.138.164.103:3306`) from JUMP `159.138.173.250` using filed credentials — redacted receipt (host tag · PASS/FAIL · schema/table counts only · zero data values).
2. Probe `visitors` (`110.238.75.83:3306`) from JUMP `159.138.173.250` using filed credentials — same receipt shape.
3. Fold PASS-verdict connectors into the Item-3 census scope (Effect 6). FAIL-verdict connectors recorded `unmeasured-with-reason` per Canon-4 §5.1 + Doc-9 A5.4.
4. Fire Item-3 live census run at expanded scope (NAS 16ch + OBS + weego + ussd + citizen_digital-if-pass + visitors-if-pass).
5. Report at census completion in wave-close END-OF-WAVE format (SO §2) with connector probe verdicts + registry counts + owner-desk items outstanding.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
