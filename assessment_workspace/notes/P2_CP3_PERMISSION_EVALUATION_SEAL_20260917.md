READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-P2-CP3 · M9 · Platform-layer deny-by-default permission evaluator · seal note · 2026-09-17T~04:35Z

**Track-a HEAD:** `f3c90a5aedf27f53869134aceccc6b31d844851a`. **Ratchet:** 4480 → **4490** (+10).

## Anchor
§7.4 M-A-2 verbatim: *"Permissions are evaluated as action × resource_type × scope, deny-by-default. Evaluation happens at the API gateway and again inside the data plane."*

## Mechanism
`services/platform_control_plane/permission_evaluation.py`:

- `PERMISSION_EVALUATION_ANCHOR` — verbatim §7.4 M-A-2 quote.
- `PermissionRequest` — frozen dataclass 6 str OPEN fields (`actor_id · action · resource_type · resource_id · scope_type · scope_id`).
- `PermissionVerdict` — frozen dataclass 2 str OPEN fields (`verdict_ref · reason_ref`).
- Canonical tokens (OPEN str): `VERDICT_ALLOW="allow"` · `VERDICT_DENY="deny"` · `REASON_NO_SCOPE_MATCH="no_scope_match"` · `REASON_ROLE_ACTION_NOT_AUTHORISED="role_action_not_authorised"` · `REASON_MATCH="match"`.
- `assess_permission_grant(*, request, assignments, authorized_role_action_refs) -> PermissionVerdict` — pure data-in/data-out · deterministic.

## Evaluation rule (deny-by-default)
1. Filter `assignments` to `in_scope = {a | a.user_id == request.actor_id AND a.scope_type == request.scope_type AND a.scope_id == request.scope_id}`.
2. If `in_scope` empty → `deny(reason=no_scope_match)`.
3. Else if any `a ∈ in_scope` has `(a.role, request.action, request.resource_type) ∈ authorized_role_action_refs` → `allow(reason=match)`.
4. Else → `deny(reason=role_action_not_authorised)`.

**Deny-by-default preserved when `authorized_role_action_refs` empty.**

## Invariants (10)
1. `test_module_fabric_present_and_all_exports_match`.
2. `test_verdict_and_reason_tokens_are_open_str_verbatim`.
3. `test_permission_request_frozen_shape_6_fields`.
4. `test_permission_verdict_frozen_shape_2_fields`.
5. `test_deny_by_default_when_no_scope_match`.
6. `test_deny_when_scope_matches_but_role_action_not_authorised`.
7. `test_allow_when_role_action_and_scope_match`.
8. `test_deny_by_default_when_authorized_matrix_empty`.
9. `test_multiple_assignments_pick_first_authorised`.
10. `test_verbatim_anchor_case_agnostic_zero_data_plane_imports`.

## Double-green under `BASELINE_GUARD=1` (post-harness-refresh)
GREEN 1 `4490 / 1 / 0 in 125.20s` + GREEN 2 `4490 / 1 / 0 in 124.47s`.

## Harness-receipt refresh drill (fired at CP-P2-CP3 seal boundary)
First double-green attempt showed `test_cp10_harness_receipt_is_still_recent` FAILED under `BASELINE_GUARD=1` — the CP10 real-Chromium proof harness receipt at `phase0/harness_ground_truth/latest.json` had aged **12.05 h** past the 12 h fresh threshold during this session (was refreshed at 16:26:53 Z on 2026-09-16).

Per owner ruling banked 2026-09-08T~06:15Z verbatim: *"refresh the harness, don't relax the threshold"*.

Fired `tools/wave_g5_realchrome_verification_harness.py` at 04:30:13 Z → new receipt at 04:30:41 Z · 0 dummies present · all 37 rules `bound_to_rendered_dom` · expected present · style-signature met (INTERRUPT 3: underline 3/3 · oxblood 1/1). Fresh receipt at `phase0/harness_ground_truth/latest.json`. Verification screenshots + log at `phase0/eyeball_proxies/20260917T043013Z_wave_g5_realchrome_run.{log,_portal.png,_registry.png,_compute.png}`. **Zero threshold relaxation.**

## CONTRACT-MODELED items enabled
The role → (action, resource_type) authorisation matrix is **CONTRACT-MODELED** — this CP fixes its shape (`authorized_role_action_refs: Tuple[Tuple[str, str, str], ...]`) so real-infra binding to an OPA policy engine, K8s RBAC translation layer, or hand-coded matrix becomes a bind-only change.

## §3.3 3-commit
- A `f3c90a5aedf27f53869134aceccc6b31d844851a` (track-a) ✅.
- B `b29317116e4010316ed076f5f6da76410a81f533` (master) ✅.
- C this-turn (fixup banks Commit-B SHA).

## GPU util at seal boundary
Elapsed **24.91 h** · remaining **47.09 h**. Both hosts alive.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
