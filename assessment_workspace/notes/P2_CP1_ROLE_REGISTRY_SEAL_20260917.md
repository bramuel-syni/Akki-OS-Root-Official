READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-P2-CP1 · M9 · Platform-layer fixed 7-role registry · seal note · 2026-09-17T~05:05Z

**Milestone:** M9 · P2 · RBAC. **CP:** P2-CP1 (first CP of P2).
**Track-a HEAD:** `1031ccd35aaa10619c669c7dd40b094e441968a6` (Commit-A).
**Ratchet:** 4468 → **4473** (+5).

## Anchor
§7.3 M-A-1 verbatim: *"7 roles ONLY: platform_operator, tenant_owner, tenant_admin, data_steward, analyst, viewer, service. Custom roles are recorded as requirements, not built."*

## Mechanism
`services/platform_control_plane/role_registry.py`:

- `ROLE_REGISTRY_ANCHOR` — verbatim §7.3 M-A-1 quote in module source.
- `PLATFORM_ROLES` — tuple of 7 OPEN str in the source-doc listing order.
- `assert_role_known(*, role_ref: str) -> None` — preventive-charter · raises `UnknownRoleRefused` when `role_ref not in PLATFORM_ROLES` · returns `None` on admit.
- `RoleRegistryRefused` (root) + `UnknownRoleRefused` (subclass). COUNTS-only messages. Case-sensitive (OPEN str · no case-fold).

## Invariants (5)
1. `test_module_fabric_present_and_all_exports_match`.
2. `test_platform_roles_is_frozen_tuple_of_7_open_str_verbatim`.
3. `test_assert_role_known_refuses_on_unknown_role`.
4. `test_assert_role_known_permits_all_7_verbatim_roles_deterministic`.
5. `test_verbatim_anchor_case_agnostic_zero_data_plane_imports`.

## Double-green under `BASELINE_GUARD=1`
GREEN 1 `4473 / 1 / 0 in 124.00s` + GREEN 2 `4473 / 1 / 0 in 124.72s`.

## §3.3 3-commit
- Commit A `1031ccd35aaa10619c669c7dd40b094e441968a6` (track-a) ✅.
- Commit B `21125b706d19112406adf2a1672c76a4c8057411` (master) ✅.
- Commit C on `master` this-turn (fixup banks Commit-B SHA).

## GPU util at seal boundary
Elapsed **24.47 h** · remaining **47.53 h**. Both hosts alive · in-perimeter.

## Foundation
Vocabulary carrier for CP-P2-CP2..CP5 (role assignment · permission evaluation · session binder · break-glass session) — every downstream P2 CP composes on `PLATFORM_ROLES` + `assert_role_known`.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
