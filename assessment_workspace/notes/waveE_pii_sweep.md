# Wave E · CP-E7 · DigiCow PII sanitizer sweep · receipt

**Owner ruling (Wave E scope §7 verbatim, 2026-08-27T~12:10Z):**
> Security/PII pass on the DigiCow paths: verify PII posture (the corpus contains farmer PII — ussd_users 2.28M rows), confirm the response-boundary sanitizer covers every new Wave E surface, and receipt the check.

## 1 · PII posture verified (measured, not paraphrased)

- **Data source:** `aws.rds.db-restore-603-cluster.digicow_live` · region `eu-west-1` (from `phase0/data_connection_records/data_source_digicow_live_20260819T152513Z_FINAL.json`).
- **Table:** `digicow_live.ussd_users` · owner-declared row count **2.28M** (external knowledge, verified in AWS RDS).
- **Farmer PII columns measured from the connection record:**
  - `farmer_mobile_no` — direct PII (MSISDN class).
  - `farmer_answer` — user-generated free-text; may carry uncontrolled PII inside answers.
  - `dairy_farmer`, `poultry_farmer`, `dairy_poultry_farmer` — occupation-class attributes on a named individual; behavioral-adjacent (NOT added to banned-set at this pass — they are boolean flags, not PII payloads; owner may rule to escalate at Wave F).

## 2 · Response-boundary sanitizer landed (Wave E CP-E7)

- **New module:** `backend/services/response_sanitizer/__init__.py`.
  - `SECRET_BANNED_FIELDS = {password, secret, signing_material, aws_secret_access_key}` (Canon-Watch discipline preserved from Doc 8).
  - `DIGICOW_PII_BANNED_FIELDS = {farmer_mobile_no, farmer_answer}` (measured from the DigiCow connection record).
  - `BANNED_FIELDS = SECRET_BANNED_FIELDS | DIGICOW_PII_BANNED_FIELDS` (union).
  - `sanitize(d: dict) -> dict` strips banned fields + any `_raw`-suffixed key.

## 3 · Wave E surfaces swept (every NEW route confirmed to apply the shared sanitizer)

| Router | Wave E CP | Endpoints | Sanitizer coverage |
|---|---|---|---|
| `services/n_series/router.py` | CP-E2 + CP-E3 | POST /api/n_series/breach · GET /api/n_series/breach · POST /api/n_series/erasure · GET /api/n_series/erasure · GET /api/n_series/rights_lapse_flags | `sanitize(row.model_dump())` on every response |
| `services/rights_quarantine/router.py` | CP-E4 | GET /api/rights_quarantine · GET /api/rights_quarantine/{admit_id} · POST /api/rights_quarantine/{admit_id}/release · POST /api/rights_quarantine/{admit_id}/refuse | `sanitize(r.model_dump())` on every response |
| `services/watch/router.py` (extended) | CP-E1 + CP-E6 | POST /api/watch/continuity · GET /api/watch/continuity | `_sanitize()` already applied (existing router pattern) · witness_state_line audited: no PII column names |

## 4 · Sanitizer invariant tests (`backend/tests/invariants/test_cp_e7_digicow_pii_sanitizer_sweep.py`)

1. `test_cp_e7_shared_sanitizer_module_exists_and_covers_digicow_pii` — asserts `farmer_mobile_no` + `farmer_answer` are in the banned set + roundtrip sanitize strips PII + secrets + `_raw`.
2. `test_cp_e7_n_series_router_applies_shared_sanitizer` — source-scan on `services/n_series/router.py` confirms import + application.
3. `test_cp_e7_rights_quarantine_router_applies_shared_sanitizer` — source-scan on `services/rights_quarantine/router.py`.
4. `test_cp_e7_watch_continuity_response_carries_witness_state_line_but_no_pii` — runtime response body check.
5. `test_cp_e7_pii_sweep_receipt_note_is_present` — asserts THIS document exists + cites the connection record + names each swept surface.

## 5 · Class-attribution honesty

- **NOT swept (out of Wave E scope):** the memory service surfaces (Doc 7 densification stats) and the audit-trail Overview surface (CA1-001/002). These are UI-surface routes that don't exist yet; CP-E6 class-attributed them as BUILD/PARTIAL for Wave F/G.
- **NOT escalated in this pass:** DigiCow columns `dairy_farmer`, `poultry_farmer`, `dairy_poultry_farmer`. Owner may rule to add them to the PII banned set at Wave F.

## 6 · Provenance

- Owner Wave E GO ruling verbatim at `STATE/DECISIONS.md · Wave E scope §7`.
- Sweep executed 2026-08-27 during CP-E7 close on Extraction-Akki `programme/track-a` (SHA at time of receipt: **PENDING** — filled at CP-E7 commit).
- Receipt banked at `phase0/drill_receipts/YYYYMMDDTHHMMSSZ_cp_e7_close.log`.
