---
card_id: CP_TENANT_SEPARATION_20260223
title: Tenant separation with named authorities (Fred Afune / Muthoni Kiarie / Samuel Kibacia [RMS] + Vincent Kimani / Peninah Wanja [DigiCow]) · any-one decision rule · isolation sweep as exit evidence · Item 5.11.d
ratified_at_utc: 2026-02-23T14:20:00Z
ratified_by: Owner drop verbatim 2026-02-23 SO §6.9 amendment §6 item 7 — 'tenant separation with named authorities Fred Afune / Muthoni Kiarie / Samuel Kibacia [RMS] + Vincent Kimani / Peninah Wanja [DigiCow], any-one decision rule, isolation sweep as exit evidence.' + Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23 (E1 wires the seam INTO Census Autonomy Service; pod NEVER data path).
card_sha256: 6c1676580466e334ea76e25c5e61c26f4d64e487ed90a09d244092be3a5cbb35
milestone_status: OPEN (Item 5.11.d · opens immediately post CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY seal · 4th item of Item 5.11 wave · REPORT-AND-CONTINUE not idle-halt · RUN-TO-COMPLETION mandate ACTIVE)
---

# CP-TENANT-SEPARATION-20260223 · tenant separation any-one decision rule + isolation sweep exit evidence

## OBJECTIVE

Land the additive tenant-separation boundary as pure §1.2 modality-extension composing sealed CP-ENT-16 `services/entitlement_service_v1/pilot_licence_seeds_v1.py` tenant identifiers (RMS + DigiCow + AKKI-TEST). Bind the 5 named approving authorities verbatim across 2 tenants (Fred Afune / Muthoni Kiarie / Samuel Kibacia for RMS; Vincent Kimani / Peninah Wanja for DigiCow). Bind the any-one decision rule structurally at boundary: exactly one named authority from the correct tenant approves; cross-tenant authorities are refused; unknown authorities are refused; unknown tenants are refused. Emit the isolation-sweep receipt as EXIT EVIDENCE proving RMS + DigiCow authority sets are disjoint (overlap_count = 0). Bank AKKI-TEST HONEST-GAP explicitly — the empty tuple is never silently accepted because any `tenant_name="AKKI-TEST"` boundary call raises `UnknownAuthorityRefused`. Zero sealed-carrier edit per SO §3.8. Ruling (b) AKKI-RUNS-IT verbatim honored structurally: E1 wires the seam; pod is never a data path.

`canon_ref: SO §6.9 amendment 2026-02-23 §6 item 7 verbatim + Entitlement Service Spec v1 §6 ENT-16..19 anchor (tenant identifiers) + Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23 + §1.2 modality-extension + §1.5 unrepresentable-not-policed (refusal exceptions rather than silent bypass).`

## MUST DO

1. **`RMS_APPROVING_AUTHORITIES` Final 3-tuple verbatim** — `("Fred Afune", "Muthoni Kiarie", "Samuel Kibacia")`. Enforced by `test_named_authorities_verbatim_rms_and_digicow`.
2. **`DIGICOW_APPROVING_AUTHORITIES` Final 2-tuple verbatim** — `("Vincent Kimani", "Peninah Wanja")`. Enforced by `test_named_authorities_verbatim_rms_and_digicow`.
3. **`ALL_NAMED_APPROVING_AUTHORITIES` Final 5-tuple** across both tenants (RMS 3 + DigiCow 2). Enforced by `test_all_named_authorities_tuple_five_across_both_tenants`.
4. **`approve_by_any_one_named_authority(tenant_name, approving_authority)` any-one decision rule** — accepts iff exactly one named authority from the CORRECT tenant. Returns `TenantApprovalDecision_v1` frozen carrier. Enforced by `test_any_one_decision_rule_authority_from_correct_tenant_accepts`.
5. **Cross-tenant authority refusal** — `CrossTenantAuthorityRefused` when authority belongs to another tenant. Enforced by `test_any_one_decision_rule_cross_tenant_authority_refused`.
6. **Unknown authority refusal** — `UnknownAuthorityRefused` for any name not in `ALL_NAMED_APPROVING_AUTHORITIES`. Enforced by `test_unknown_authority_refused`.
7. **Unknown tenant refusal** — `UnknownTenantRefused` for any tenant not in the CP-ENT-16 3-tenant pilot licence seed set. Enforced by `test_unknown_tenant_refused`.
8. **`run_tenant_isolation_sweep()` returns `TenantIsolationSweepReceipt_v1`** with `rms_authorities_count=3`, `digicow_authorities_count=2`, `overlap_count=0`, `overlap=()`, `disjoint=True`. **This is the EXIT EVIDENCE per owner verbatim.** Enforced by `test_isolation_sweep_returns_disjoint_authority_sets`.
9. **`TENANT_SEPARATION_ANY_ONE_RULE_POSTURE` Final marker** verbatim citing SO §6.9 amendment §6 item 7; contains substrings `any-one`/`any one` + `tenant`. Enforced by `test_tenant_separation_posture_marker_present`.
10. **§1.2 no-redeclaration** of sealed CP-ENT-16 symbols (`PilotLicenceSeed_v1`, `RMS_PILOT_LICENCE_SEED`, `DIGICOW_PILOT_LICENCE_SEED`, `AKKI_TEST_PILOT_LICENCE_SEED`, `THREE_TENANT_PILOT_LICENCE_SEEDS`, `create_tenant_with_pilot_licence_seed`, `TenantCreationRefusedWithoutPilotLicenceSeedError`). Enforced by `test_no_redeclaration_of_sealed_ent_16_symbols_1_2`.

## MUST NOT DO

- No edit to sealed `services/entitlement_service_v1/pilot_licence_seeds_v1.py` (CP-ENT-16 closed).
- No edit to sealed `services/entitlement_service_v1/chokepoint_resolver.py` (CP-ENTITLEMENT-BUILD-WAVE R-82 closed).
- No permission of any authority outside `ALL_NAMED_APPROVING_AUTHORITIES` at approval boundary.
- No permission of any tenant name outside the CP-ENT-16 3-tenant set at approval boundary.
- No permission of a same-name authority approving on the WRONG tenant (cross-tenant refusal).
- No silent acceptance of AKKI-TEST approvals — the empty tuple must raise at boundary (HONEST-GAP posture explicit).
- No refactor per SO §3.8 additive-only.
- No `testing_agent` per SO §3.

## NEW ADDITIVE MODULES

`backend/services/entitlement_service_v1/tenant_separation_v1.py` (§1.2 modality-extension · ~178 lines · `RMS_APPROVING_AUTHORITIES` + `DIGICOW_APPROVING_AUTHORITIES` + `AKKI_TEST_APPROVING_AUTHORITIES` + `ALL_NAMED_APPROVING_AUTHORITIES` + `TENANT_SEPARATION_ANY_ONE_RULE_POSTURE` + `AKKI_TEST_HONEST_GAP_POSTURE` + `TenantSeparationBoundaryRefused` base + 3 refusal subclasses + `TenantApprovalDecision_v1` frozen + `TenantIsolationSweepReceipt_v1` frozen + `approve_by_any_one_named_authority` boundary callable + `run_tenant_isolation_sweep` exit-evidence callable).

Test file: `backend/tests/invariants/test_cp_tenant_separation_any_one_rule.py` (10 RED-first pins).

## SEALED CARRIERS TO NOT EDIT

- CP-ENT-16 `services/entitlement_service_v1/pilot_licence_seeds_v1.py` (Item 5.11.b sealed 2026-02-23 · `PilotLicenceSeed_v1` + `RMS_PILOT_LICENCE_SEED` + `DIGICOW_PILOT_LICENCE_SEED` + `AKKI_TEST_PILOT_LICENCE_SEED` + `THREE_TENANT_PILOT_LICENCE_SEEDS` + `create_tenant_with_pilot_licence_seed` + `TenantCreationRefusedWithoutPilotLicenceSeedError` + `EVERY_MODEL_CALL_RESOLVES_FROM_DAY_1_POSTURE`).
- CP-ENTITLEMENT-BUILD-WAVE (R-82) `services/entitlement_service_v1/chokepoint_resolver.py` + `contracts/principal_v1.py` (`PrincipalV1` + `PrincipalKind` + `resolve`).

## EXIT (RED-first invariant node IDs)

1. `backend/tests/invariants/test_cp_tenant_separation_any_one_rule.py::test_named_authorities_verbatim_rms_and_digicow`
2. `backend/tests/invariants/test_cp_tenant_separation_any_one_rule.py::test_all_named_authorities_tuple_five_across_both_tenants`
3. `backend/tests/invariants/test_cp_tenant_separation_any_one_rule.py::test_any_one_decision_rule_authority_from_correct_tenant_accepts`
4. `backend/tests/invariants/test_cp_tenant_separation_any_one_rule.py::test_any_one_decision_rule_cross_tenant_authority_refused`
5. `backend/tests/invariants/test_cp_tenant_separation_any_one_rule.py::test_unknown_authority_refused`
6. `backend/tests/invariants/test_cp_tenant_separation_any_one_rule.py::test_unknown_tenant_refused`
7. `backend/tests/invariants/test_cp_tenant_separation_any_one_rule.py::test_isolation_sweep_returns_disjoint_authority_sets`
8. `backend/tests/invariants/test_cp_tenant_separation_any_one_rule.py::test_tenant_separation_posture_marker_present`
9. `backend/tests/invariants/test_cp_tenant_separation_any_one_rule.py::test_no_redeclaration_of_sealed_ent_16_symbols_1_2`
10. `backend/tests/invariants/test_cp_tenant_separation_any_one_rule.py::test_akki_test_tenant_carries_akki_authorities_placeholder`

Ratchet: 6350 → 6360 (+10 canonical measured). Isolation-sweep receipt (Exit evidence) — `run_tenant_isolation_sweep()` returns `TenantIsolationSweepReceipt_v1(rms_authorities_count=3, digicow_authorities_count=2, overlap_count=0, overlap=(), disjoint=True)`.

## LEDGER CHECK

> **Ledger check — this seal implements EXECUTION_ORDER.md Item 5.11.d CP-TENANT-SEPARATION and nothing else.**

**Additive-only §3.8 · RED-first · 5-commit seal per SO §3.3 · terminal pytest only · BASELINE_GUARD=1 PYTHONHASHSEED=0 double-green byte-identical stripped_sha256 · milestone-seal continuity bundles per SO §6.9(5) AMENDED · GAPS_FIXED_LEDGER append at seal boundary.**

## STOP

- STOP on any `SPEC-CONFLICT-<n>` discovered mid-slice.
- STOP on hard custody/gate violation.
- STOP if any sealed carrier would need edit.
- STOP if RED_pre does not authentically fail with `ModuleNotFoundError`/`ImportError` right-reason on all 10 pins.
- STOP if double-green sweep stripped_sha256 differs between sweeps.

## ANCHORS

- **SO drop anchors (verbatim):**
  - `STATE/OWNER_DROPS/so_6_9_amendment_20260223/DROP.md §6 item 7` verbatim.
  - `STATE/OWNER_DROPS/na7p4_park_proceed_autonomously_mirror_probe_20260223/DROP.md` verbatim (tenant separation with named authorities).
  - `STATE/OWNER_DROPS/ruling_b_akki_runs_it_plus_standing_directives_20260223/DROP.md §1` verbatim.
- **Spec anchors (verbatim):**
  - Entitlement Service Spec v1 §6 ENT-16..19 (tenant identifiers) — anchor via CP-ENT-16 sealed carriers.
  - §1.2 modality-extension composes sealed symbols; no redeclaration.
  - §1.5 unrepresentable-not-policed — refusal exceptions rather than silent bypass.
- **Sealed-carrier anchors (composed UNCHANGED per SO §3.8):**
  - `backend/services/entitlement_service_v1/pilot_licence_seeds_v1.py` (CP-ENT-16 Item 5.11.b · 3-tenant pilot licence seeds).
  - `backend/services/entitlement_service_v1/chokepoint_resolver.py` (CP-ENTITLEMENT-BUILD-WAVE R-82).
