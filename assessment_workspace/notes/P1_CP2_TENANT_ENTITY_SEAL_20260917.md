READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-P1-CP2 · M9 · Platform-layer tenant entity carrier · seal note · 2026-09-17T~04:15Z

**Milestone:** M9 · Akki OS pilot platform layer.
**Phase:** P1 · Foundation.
**CP:** P1-CP2 · Tenant entity carrier (pure frozen carrier · analog of CP-P1-CP1 minus refusal wrapper).
**Track-a HEAD:** `95fbd8ebcd9f785927c4237363ec052ff6960678` (Commit-A).
**Master HEAD:** (Commit-B this-turn · Commit-C fixup banks).
**Ratchet:** 4440 → **4445** (+5).

## Anchor
Akki OS Pilot Platform Reference v0.2 §10 verbatim: `tenant(id, legal_name, short_name, jurisdiction, status, mou_ref, created_at)`. §3.1 anchor: *"A tenant maps one-to-one to a legal entity."*

## Mechanism
Pure frozen `TenantEntity` dataclass at `services/platform_control_plane/tenant_entity.py` · 7 exact-order `str` (all OPEN) fields. `TENANT_ENTITY_FIELDS` tuple for composition-surface access.

**Validation composed by downstream CPs:**
- CP-P1-CP1 · `assert_tenant_context_valid` (cross-tenant refusal on refs whose `tenant_id ≠ TenantEntity.id`).
- CP-P1-CP6 · lifecycle FSM validates `status` transitions against §4.7 vocabulary `{provisioning, sandbox_active, production_active, suspended, offboarded}`.

## Invariants (5)
Frozen at `tests/invariants/test_p1_cp2_tenant_entity.py`.
1. `test_module_fabric_present_and_all_exports_match` — 3-name `__all__`.
2. `test_tenant_entity_shape_frozen_7_carrier_exact_order` — frozen · 7 fields exact order · all str.
3. `test_tenant_entity_fields_constant_matches_dataclass_fields` — `TENANT_ENTITY_FIELDS` tuple.
4. `test_tenant_entity_is_hashable_immutable_case_agnostic_open_str` — hashable · immutable · empty & non-canonical values admitted at carrier layer.
5. `test_verbatim_anchor_case_agnostic_zero_data_plane_imports` — anchor + 21-token grep-negative + no data-plane imports.

## Double-green byte-match under `BASELINE_GUARD=1`
- GREEN 1: `4445 passed, 1 skipped, 438 warnings in 124.13s`.
- GREEN 2: `4445 passed, 1 skipped, 438 warnings in 124.11s`.

## §3.3 3-commit protocol
- Commit A `95fbd8ebcd9f785927c4237363ec052ff6960678` (track-a) ✅.
- Commit B `a14e668dbe0b8d7bb3118882432a2ff63bf2a90e` (master) ✅.
- Commit C on `master` this-turn (fixup · banks Commit-B SHA).

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
