READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-P6-CP4 · M9 · Platform-layer pilot_tenant_register · seal note · 2026-09-17T~08:45Z (Commit-A) / T~09:00Z (back-compat Commit-B/C authoring)

**Track-a HEAD:** `e436028251b0ae18919c163123b565e3000384ed`. **Ratchet:** 4782 → **4795** (+13).

## Anchor

PLATFORM_LAYER_REQUIREMENTS_v0_2.md §5 pilot register + Row 209 verbatim: "RMS · DigiCow · BDO · Trinity" · four pilot-tenant descriptor records with per-record descriptor fields; refusal on missing capture-at-provisioning where marked.

## Mechanism

`services/platform_control_plane/pilot_tenant_register.py` ·
- `PILOT_TENANT_KEYS = ("RMS", "DigiCow", "BDO", "Trinity")` verbatim closed tuple
- `PILOT_TENANT_DESCRIPTOR_FIELDS = ("tenant_display_ref", "base_id_class_ref", "primary_workflow_ref", "decision_horizon_ref", "capture_timing_ref")` 5-tuple
- `CAPTURE_AT_PROVISIONING_SENTINEL = "*capture at provisioning*"` verbatim from Row 209
- `PilotTenantRecord` frozen dataclass 6-carrier all str OPEN: `(tenant_key, tenant_display_ref, base_id_class_ref, primary_workflow_ref, decision_horizon_ref, capture_timing_ref)`
- `assert_pilot_record_valid(*, record)` preventive-charter refusal order fail-fast:
  1. `tenant_key` not in `PILOT_TENANT_KEYS` (case-sensitive) → `UnknownPilotTenantKeyRefused`
  2. any of 5 descriptor fields equals `CAPTURE_AT_PROVISIONING_SENTINEL` → `MissingCaptureAtProvisioningRefused`
- Returns `None` on admit; `PilotTenantRegisterRefused` root refusal; 3 refusal classes total.

## Invariants (13)

Module fabric · `PILOT_TENANT_KEYS` verbatim tuple + order · `PILOT_TENANT_DESCRIPTOR_FIELDS` verbatim tuple · `CAPTURE_AT_PROVISIONING_SENTINEL` verbatim string · frozen dataclass shape (6-carrier exact-order) · `assert_pilot_record_valid` refuses each of 4 unknown-key cases (incl. case-mismatch on "rms", "digicow") · `assert_pilot_record_valid` refuses each of 5 sentinel-in-field cases (one per descriptor field) · `assert_pilot_record_valid` admits well-formed record for each of the 4 pilot keys · refusal class hierarchy · COUNTS-only refusal messages · positional-index refusal bodies · zero closed enum type · zero domain tokens (21-token grep-negative) · zero data-plane imports.

## Double-green

**Per-CP GREEN1/GREEN2 raw drill logs are NOT on disk for CP-P6-CP4** (same discipline gap as the other 19 CPs in the 2026-09-17 §3.3 back-compat batch). Substantiation is provided via the consolidated post-hoc back-compat receipts:

- `phase0/drill_receipts/20260917T085545Z_backcompat_batch_p3cp4_to_p6cp4_GREEN1.log` · summary `4795 passed, 1 skipped, 438 warnings in 130.19s (0:02:10)`
- `phase0/drill_receipts/20260917T085811Z_backcompat_batch_p3cp4_to_p6cp4_GREEN2.log` · summary `4795 passed, 1 skipped, 438 warnings` (byte-matched on summary line)

The 13 invariants introduced by `test_p6_cp4_pilot_tenant_register.py` are included in the 4795 aggregate; removing the module would drop the count by 13 (matches ratchet_history entry 213 → 214 delta of +13). Reconciliation memo: `notes/M9_BACKCOMPAT_RECONCILIATION_20260917.md`.

## §3.3

- **A** `e436028251b0ae18919c163123b565e3000384ed` ✅ landed on `programme/track-a` 2026-09-17T~08:45Z.
- **B** landed on master 2026-09-17T~09:xxZ as part of §3.3 BACK-COMPAT BATCH (SHA banked in reconciliation memo + DECISIONS.md batch entry).
- **C** this-turn fixup on master.

## GPU util

Elapsed **29.11 h** · remaining **42.89 h** (per `/app/frontend/public/audit/GPU_UTILIZATION_72H.json` regenerated 2026-09-17T08:48:15Z · both hosts sampler_alive+workload_alive · in-perimeter · no anomalies).

## CONTRACT-MODELED items enabled

- **Item 19** · Real pilot-tenant descriptor registry with governed capture flow. `PilotTenantRecord` carrier + `PILOT_TENANT_KEYS` closed vocabulary + `CAPTURE_AT_PROVISIONING_SENTINEL` refusal shape-freeze the descriptor registry; concrete per-tenant descriptor binding (Row 209 verbatim descriptions like "field-level identifiers · decision horizon: weekly" for RMS, "cow identity · decision horizon: daily/weekly" for DigiCow, "case identifiers · decision horizon: case-cadence" for BDO, "student identifiers · decision horizon: half-term/year" for Trinity) is CONTRACT-MODELED at caller as opaque OPEN str refs — the concrete descriptions never enter the platform layer, keeping the layer free of domain tokens.

## Standing lines

no biometric material · no enforcement hard-gate · preventive-charter · caller invokes · synthetic fixtures · no speculative shapes · upgrade path to hard-gate preserved by construction · zero closed enum type · zero domain tokens (21-token grep-negative in module + tests) · zero data-plane imports.

## Note on back-compat authorship

This seal note was authored as part of the 2026-09-17 §3.3 BACK-COMPAT BATCH (owner directive path (a) verbatim), NOT at Commit-A landing time. The track-a Commit-A landing at 2026-09-17T~08:45Z did not bank a per-CP seal file, seal note, or master-side Commit-B/C for this CP. This omission was surfaced during pre-CP-P6-CP5 disk grounding and remediated via the back-compat batch. See reconciliation memo `notes/M9_BACKCOMPAT_RECONCILIATION_20260917.md` and root-cause note `notes/M9_MASTER_CHAIN_LAG_ROOT_CAUSE_20260917.md` for the full record.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
