---
card_id: CP_ENT_16_PILOT_LICENCE_SEEDS_20260223
title: ENT-16 pilot licence seeds · RMS + DigiCow + AKKI-TEST · Compute dial Managed + Frontier dial Your Keys · every model call resolves from day 1 · Item 5.11.b
ratified_at_utc: 2026-02-23T12:55:00Z
ratified_by: Owner drop verbatim 2026-02-23 SO §6.9 amendment §6 verbatim — 'ENT-16 keeps its rule and gains its seed: a pilot licence object created at tenant creation for RMS, DigiCow, and AKKI-TEST — Compute dial Managed, Frontier dial Your Keys — so every model call resolves from the first day.' + Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23 (ENT-16 Managed compute · Frontier Your Keys · training compute + model weights + labelled corpus never leave Akki boundary).
card_sha256: b50a64f0443e1260c94487aa80ac2495ff27478e487271d8fdf3e0058d0cc31d
milestone_status: QUEUED (Item 5.11.b · opens immediately post CP-SO-6.9-LID-WAVE seal · REPORT-AND-CONTINUE not idle-halt · RUN-TO-COMPLETION mandate ACTIVE)
---

# CP-ENT-16-PILOT-LICENCE-SEEDS-20260223 · pilot licence objects for RMS + DigiCow + AKKI-TEST

## OBJECTIVE

Land the additive ENT-16 pilot licence seed module as pure §1.2 modality-extension composing sealed CP-ENTITLEMENT-BUILD-WAVE `services/entitlement_service_v1/chokepoint_resolver.py` (R-82). Create three pilot licence seed objects — RMS, DigiCow, AKKI-TEST — each carrying Compute dial `Managed` + Frontier dial `Your Keys`, satisfying ENT-16's "every model call resolves from the first day" rule structurally. The seed objects are frozen dataclasses; the tenant-creation seam that consumes them lands as a boundary callable that refuses tenant creation without a pilot licence seed present. Zero sealed-carrier edit per SO §3.8.

`canon_ref: SO §6.9 amendment 2026-02-23 §6 verbatim + Entitlement Service Spec v1 §6 ENT-16..19 verbatim + Ruling (b) AKKI-RUNS-IT verbatim (ENT-16 Managed compute + Frontier Your Keys) + §1.2 modality-extension.`

## MUST DO

1. **`PilotLicenceSeed_v1` frozen 4-field shape** — `tenant_name: str`, `compute_dial: Literal["Managed"]`, `frontier_dial: Literal["Your Keys"]`, `created_at_utc: str`. Enforced by `test_pilot_licence_seed_v1_frozen_four_field_shape_ent_16`.
2. **`RMS_PILOT_LICENCE_SEED` Final constant** with `tenant_name="RMS"`. Enforced by `test_rms_pilot_licence_seed_managed_your_keys_so_6_9_amendment`.
3. **`DIGICOW_PILOT_LICENCE_SEED` Final constant** with `tenant_name="DigiCow"`. Enforced by `test_digicow_pilot_licence_seed_managed_your_keys_so_6_9_amendment`.
4. **`AKKI_TEST_PILOT_LICENCE_SEED` Final constant** with `tenant_name="AKKI-TEST"`. Enforced by `test_akki_test_pilot_licence_seed_managed_your_keys_so_6_9_amendment`.
5. **`THREE_TENANT_PILOT_LICENCE_SEEDS` Final tuple** of exactly the three seeds. Enforced by `test_three_tenant_pilot_licence_seeds_tuple_contains_exactly_rms_digicow_akki_test`.
6. **`create_tenant_with_pilot_licence_seed` boundary refuses tenant creation without a pilot licence seed present** — raises `TenantCreationRefusedWithoutPilotLicenceSeedError`. Enforced by `test_tenant_creation_refused_without_pilot_licence_seed_ent_16`.
7. **`EVERY_MODEL_CALL_RESOLVES_FROM_DAY_1_POSTURE` Final marker** verbatim of SO §6.9 amendment §6 line. Enforced by `test_every_model_call_resolves_from_day_1_posture_marker_present_so_6_9_amendment_6`.
8. **§1.2 no-redeclaration** of sealed CP-ENTITLEMENT-BUILD-WAVE symbols (`PrincipalV1`, `PrincipalKind`, `resolve` from `chokepoint_resolver.py`). Enforced by `test_no_redeclaration_of_sealed_entitlement_service_v1_symbols_1_2`.

## MUST NOT DO

- No edit to sealed `services/entitlement_service_v1/` modules (R-82 CP-ENTITLEMENT-BUILD-WAVE closed).
- No permission of a `compute_dial` other than `"Managed"` at seed construction.
- No permission of a `frontier_dial` other than `"Your Keys"` at seed construction.
- No refactor per SO §3.8 additive-only.
- No `testing_agent` per SO §3.

## NEW ADDITIVE MODULES

`backend/services/entitlement_service_v1/pilot_licence_seeds_v1.py` (§1.2 modality-extension).

Test file: `backend/tests/invariants/test_cp_ent_16_pilot_licence_seeds_rms_digicow_akki_test.py` (8 RED-first pins).

## SEALED CARRIERS TO NOT EDIT

- CP-ENTITLEMENT-BUILD-WAVE (R-82) `services/entitlement_service_v1/chokepoint_resolver.py` + `contracts/principal_v1.py` (`PrincipalV1` + `PrincipalKind`).

## EXIT (RED-first invariant node IDs)

1. `backend/tests/invariants/test_cp_ent_16_pilot_licence_seeds_rms_digicow_akki_test.py::test_pilot_licence_seed_v1_frozen_four_field_shape_ent_16`
2. `backend/tests/invariants/test_cp_ent_16_pilot_licence_seeds_rms_digicow_akki_test.py::test_rms_pilot_licence_seed_managed_your_keys_so_6_9_amendment`
3. `backend/tests/invariants/test_cp_ent_16_pilot_licence_seeds_rms_digicow_akki_test.py::test_digicow_pilot_licence_seed_managed_your_keys_so_6_9_amendment`
4. `backend/tests/invariants/test_cp_ent_16_pilot_licence_seeds_rms_digicow_akki_test.py::test_akki_test_pilot_licence_seed_managed_your_keys_so_6_9_amendment`
5. `backend/tests/invariants/test_cp_ent_16_pilot_licence_seeds_rms_digicow_akki_test.py::test_three_tenant_pilot_licence_seeds_tuple_contains_exactly_rms_digicow_akki_test`
6. `backend/tests/invariants/test_cp_ent_16_pilot_licence_seeds_rms_digicow_akki_test.py::test_tenant_creation_refused_without_pilot_licence_seed_ent_16`
7. `backend/tests/invariants/test_cp_ent_16_pilot_licence_seeds_rms_digicow_akki_test.py::test_every_model_call_resolves_from_day_1_posture_marker_present_so_6_9_amendment_6`
8. `backend/tests/invariants/test_cp_ent_16_pilot_licence_seeds_rms_digicow_akki_test.py::test_no_redeclaration_of_sealed_entitlement_service_v1_symbols_1_2`

## LEDGER CHECK

> **Ledger check — this seal implements EXECUTION_ORDER.md Item 5.11.b CP-ENT-16-PILOT-LICENCE-SEEDS and nothing else.**

**Additive-only §3.8 · RED-first · 5-commit seal per SO §3.3 · terminal pytest only · BASELINE_GUARD=1 PYTHONHASHSEED=0 double-green byte-identical stripped_sha256 · milestone-seal continuity bundles per SO §6.9(5) AMENDED · GAPS_FIXED_LEDGER append at seal boundary.**

## STOP

- STOP on any `SPEC-CONFLICT-<n>` discovered mid-slice.
- STOP on hard custody/gate violation.
- STOP if any sealed carrier would need edit.
- STOP if RED_pre does not authentically fail with `ModuleNotFoundError`/`ImportError` right-reason on all 8 pins.
- STOP if double-green sweep stripped_sha256 differs between sweeps.

## ANCHORS

- **SO drop anchors:**
  - `STATE/OWNER_DROPS/so_6_9_amendment_20260223/DROP.md §6` verbatim.
  - `STATE/OWNER_DROPS/ruling_b_akki_runs_it_plus_standing_directives_20260223/DROP.md §1` verbatim.
- **Spec anchors (verbatim):**
  - Entitlement Service Spec v1 §6 ENT-16..19 verbatim.
  - §1.2 modality-extension composes sealed symbols; no redeclaration.
- **Sealed-carrier anchors (composed UNCHANGED per SO §3.8):**
  - `backend/services/entitlement_service_v1/chokepoint_resolver.py` (CP-ENTITLEMENT-BUILD-WAVE R-82 · ENT-16 6-step ordered chain).
