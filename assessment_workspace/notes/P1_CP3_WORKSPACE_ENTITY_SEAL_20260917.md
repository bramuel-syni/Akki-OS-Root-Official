READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-P1-CP3 · M9 · Platform-layer workspace entity carrier · seal note · 2026-09-17T~04:25Z

**Milestone:** M9 · P1 · Foundation. **CP:** P1-CP3.
**Track-a HEAD:** `1f32d8d18dd1db73ad28978389b38c1cd61335cf` (Commit-A).
**Ratchet:** 4445 → **4450** (+5).

## Anchor
§10 verbatim: `workspace(id, tenant_id, name, is_default)`. §2: *"Workspace — division inside a tenant used to scope users and outputs. Every tenant has at least one."*

## Mechanism
Pure frozen `WorkspaceEntity` at `services/platform_control_plane/workspace_entity.py` · 4 exact-order fields (`id: str · tenant_id: str · name: str · is_default: bool`). Ownership isolation anchored at `tenant_id` (position 2 · index 1 · top-level). `WORKSPACE_ENTITY_FIELDS` tuple.

**Note on `is_default: bool`.** Sole non-str field in P1 carriers so far. §10 uses boolean semantics by domain nature (a workspace either IS or IS NOT the default per §M-H-7). Case-agnostic doctrine preserved — no closed enum introduced; the OPEN-str exception applies only to identifier-shaped fields. Standing law does not forbid `bool` fields for domain-inherent boolean semantics.

## Invariants (5)
1. `test_module_fabric_present_and_all_exports_match`.
2. `test_workspace_entity_shape_frozen_4_carrier_exact_order`.
3. `test_workspace_entity_fields_constant_matches_dataclass_fields`.
4. `test_workspace_entity_is_hashable_immutable_and_carries_tenant_id`.
5. `test_verbatim_anchor_case_agnostic_zero_data_plane_imports`.

## Double-green byte-match under `BASELINE_GUARD=1`
GREEN 1 `4450 passed / 1 skipped / 0 failed in 123.62s` + GREEN 2 `4450 passed / 1 skipped / 0 failed in 123.82s` (byte-identical outcome).

## §3.3 3-commit protocol
- Commit A `1f32d8d18dd1db73ad28978389b38c1cd61335cf` (track-a) ✅.
- Commit B `868c4af13dc8badd3ac866666b5ba9285a3c1a2c` (master) ✅.
- Commit C on `master` this-turn (fixup · banks Commit-B SHA).

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
