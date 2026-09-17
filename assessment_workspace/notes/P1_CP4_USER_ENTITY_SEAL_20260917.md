READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-P1-CP4 · M9 · Platform-layer user entity carrier · seal note · 2026-09-17T~04:35Z

**Milestone:** M9 · P1 · Foundation. **CP:** P1-CP4.
**Track-a HEAD:** `711817de204aef74f78ca57a343658f50c26234f` (Commit-A).
**Ratchet:** 4450 → **4455** (+5).

## Anchor
§10 verbatim: `user(id, tenant_id, email, status, auth_method, mfa_enrolled, created_at)`. §7.2 anchors: users tenant-scoped · auth_method OPEN str (native + SSO OIDC + SSO SAML) · mfa_enrolled bool.

## Mechanism
Pure frozen `UserEntity` at `services/platform_control_plane/user_entity.py` · 7 exact-order fields (6 str + 1 bool `mfa_enrolled`). Ownership isolation at `tenant_id` index 1. `USER_ENTITY_FIELDS` tuple.

**Case-agnostic invariant:** `auth_method` is OPEN str · `sso_entra_id`, `sso_google`, `sso_okta`, `native` all admitted without a closed enum. Downstream CP (P4 or P5) may add a set-membership refusal.

## Invariants (5)
1. `test_module_fabric_present_and_all_exports_match`.
2. `test_user_entity_shape_frozen_7_carrier_exact_order`.
3. `test_user_entity_fields_constant_matches_dataclass_fields`.
4. `test_user_entity_hashable_immutable_ownership_at_tenant_id_index_1`.
5. `test_verbatim_anchor_case_agnostic_zero_data_plane_imports`.

## Double-green byte-match
GREEN 1 `4455 passed / 1 skipped / 0 failed in 124.18s` + GREEN 2 `4455 passed / 1 skipped / 0 failed in 124.14s` (BASELINE_GUARD=1).

## §3.3 3-commit protocol
- Commit A `711817de204aef74f78ca57a343658f50c26234f` (track-a) ✅.
- Commit B `2ec94b18caf5e638c220b4b8c5a897b953190a88` (master) ✅.
- Commit C on `master` this-turn (fixup · banks Commit-B SHA).

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
