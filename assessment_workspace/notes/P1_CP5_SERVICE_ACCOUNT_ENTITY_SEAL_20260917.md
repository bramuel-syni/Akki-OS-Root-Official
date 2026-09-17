READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-P1-CP5 · M9 · Platform-layer service-account entity carrier · seal note · 2026-09-17T~04:45Z

**Milestone:** M9 · P1 · Foundation. **CP:** P1-CP5.
**Track-a HEAD:** `a2857843fa8f80dde6330a926245ef02b930aeef` (Commit-A).
**Ratchet:** 4455 → **4460** (+5).

## Anchor
§10 verbatim: `service_account(id, tenant_id, name, cert_fingerprint, expires_at)`. §7.2: *"data-plane agents auth via short-lived certs bound to tenant_id."*

## Mechanism
Pure frozen `ServiceAccountEntity` at `services/platform_control_plane/service_account_entity.py` · 5 exact-order str OPEN fields · ownership isolation at `tenant_id` index 1 · `SERVICE_ACCOUNT_ENTITY_FIELDS` tuple.

`cert_fingerprint` OPEN str · algorithm-agnostic (admits sha-256, sha-1, ed25519-thumbprint without a closed enum). Downstream P4 CP will compose scheduler admission with `expires_at` freshness refusal (CONTRACT-MODELED item 6 · real PKI required).

## Invariants (5)
1. `test_module_fabric_present_and_all_exports_match`.
2. `test_service_account_entity_shape_frozen_5_carrier_exact_order`.
3. `test_service_account_entity_fields_constant_matches_dataclass_fields`.
4. `test_service_account_hashable_ownership_at_tenant_id_index_1_open_str_cert`.
5. `test_verbatim_anchor_case_agnostic_zero_data_plane_imports`.

## Double-green byte-match under `BASELINE_GUARD=1`
GREEN 1 `4460 passed / 1 skipped / 0 failed in 124.27s` + GREEN 2 `4460 passed / 1 skipped / 0 failed in 124.30s`.

## §3.3 3-commit protocol
- Commit A `a2857843fa8f80dde6330a926245ef02b930aeef` (track-a) ✅.
- Commit B `d0cdcb39ca74831c6d09494f17c99efe1d0d70e2` (master) ✅.
- Commit C on `master` this-turn (fixup · banks Commit-B SHA).

## CONTRACT-MODELED items enabled
- Item 6 · Real PKI cert issuance + tenant_id-bound CN/SAN validation.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
