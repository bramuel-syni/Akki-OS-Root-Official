READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-P2-CP2 · M9 · Platform-layer role_assignment carrier · seal note · 2026-09-17T~05:15Z

**Track-a HEAD:** `04eb3c753541f6b085c9df14b6b13679f4227160`. **Ratchet:** 4473 → **4480** (+7).

## Anchor
§10 verbatim: `role_assignment (id, user_id, role, scope_type, scope_id, granted_by, granted_at)`. §7.4: *"Permissions are evaluated as action × resource_type × scope, deny-by-default. Evaluation happens at the API gateway and again inside the data plane."*

## Mechanism
`services/platform_control_plane/role_assignment.py` · `RoleAssignment` frozen dataclass 7 exact-order str OPEN fields · `ROLE_ASSIGNMENT_FIELDS` tuple · preventive-charter `assert_role_assignment_valid` refuses `SelfGrantRefused` when `granted_by == user_id` · returns None on admit · 2 refusal classes.

## Invariants (7)
1. `test_module_fabric_present_and_all_exports_match`.
2. `test_role_assignment_shape_frozen_7_carrier_exact_order`.
3. `test_role_assignment_fields_constant_matches_dataclass_fields`.
4. `test_assert_refuses_self_grant`.
5. `test_assert_permits_when_granter_and_grantee_differ`.
6. `test_role_assignment_hashable_immutable_open_str`.
7. `test_verbatim_anchor_case_agnostic_zero_data_plane_imports`.

## Double-green
GREEN1 4480 · GREEN2 4480 (BASELINE_GUARD=1).

## §3.3 3-commit
- A `04eb3c753541f6b085c9df14b6b13679f4227160` ✅.
- B `e090d4c27d6801d44ae9fdd61e84e13f84ad8bab` ✅.
- C this-turn (fixup banks Commit-B SHA).

## GPU util
Elapsed **24.64 h** · remaining **47.36 h**.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
