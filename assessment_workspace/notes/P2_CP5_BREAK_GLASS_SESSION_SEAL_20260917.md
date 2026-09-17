READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-P2-CP5 · M9 · Platform-layer break_glass_session · seal note · 2026-09-17T~05:05Z

**Milestone:** M9 · P2 · RBAC. **CP:** P2-CP5 (**LAST CP of P2 · P2 COMPLETE**).
**Track-a HEAD:** `ec07fdb0924b3a076a62e52286c309749d2d2f30`.
**Ratchet:** 4502 → **4516** (+14).

## Anchor
§7.8 M-A-8 verbatim: *"Break-glass: stated reason · 2nd-operator approval · ≤4h · auto owner notification at open + close · flagged in both audit logs."*
§10 verbatim: `break_glass_session (id, tenant_id, operator_id, approver_id, reason, opened_at, expires_at, closed_at)`.

## Mechanism
`services/platform_control_plane/break_glass_session.py`:

- `BreakGlassSession` — frozen 8-carrier per §10 · all str OPEN.
- `BREAK_GLASS_MAX_DURATION_HOURS = 4` (§7.8 verbatim ceiling).
- Empty-string convention for `closed_at` (not-yet-closed) and for notification refs (absent).
- `assert_break_glass_valid(*, session, duration_hours, opened_notification_ref, close_notification_ref) -> None` — preventive-charter · fail-fast refusal order:
  1. `session.reason == ""` → `MissingReasonRefused` (§7.8 stated reason).
  2. `approver_id empty OR approver_id == operator_id` → `SecondApproverRefused` (§7.8 2nd-operator approval).
  3. `duration_hours > 4` → `ExceedsFourHoursRefused` (§7.8 ≤4h).
  4. `opened_notification_ref == ""` → `MissingOwnerNotificationRefused` (open).
  5. `session.closed_at != "" AND close_notification_ref == ""` → `MissingOwnerNotificationRefused` (close).
- 5 refusal classes (`BreakGlassSessionRefused` root + 4 subclasses). COUNTS-only messages · positional-index-only refusal bodies.

## Invariants (14)
1. Module fabric + `__all__` match (10-name set).
2. `BreakGlassSession` frozen 8 exact-order fields per §10.
3. `BREAK_GLASS_SESSION_FIELDS` matches dataclass.
4. `BREAK_GLASS_MAX_DURATION_HOURS == 4` verbatim.
5. Refusal hierarchy (root + 4 subclasses).
6. Refuses on missing reason.
7. Refuses on missing approver.
8. Refuses on self-approver (operator_id == approver_id).
9. Refuses on duration > 4h + admits at boundary duration == 4.
10. Refuses on missing opened_notification_ref.
11. Refuses on missing close_notification_ref when closed_at is set (+ admits when closed_at empty).
12. Admits when all constraints met (both open + closed shapes).
13. Fail-fast refusal order: reason → approver → duration → notification.
14. Verbatim anchor + 21-token grep-negative + import-negative.

## Double-green under `BASELINE_GUARD=1`
GREEN 1 `4516 / 1 / 0 in 125.80s` + GREEN 2 `4516 / 1 / 0 in 125.33s`.

## §3.3 3-commit
- A `ec07fdb0924b3a076a62e52286c309749d2d2f30` ✅.
- B `00309180714043e9b0b3fa19a7a8dff872cb1bdb` (master) ✅.
- C this-turn (fixup banks Commit-B SHA).

## GPU util at seal boundary
Elapsed **25.28 h** · remaining **46.72 h**.

## CONTRACT-MODELED items enabled
- **Item 8** · Break-glass owner notification via email/webhook. Shape-frozen: two notification refs MUST be supplied at open and at close (they are audit-event ids that record real webhook/email delivery). Real webhook binding (SendGrid / SES / Slack webhook) is a downstream bind-only change.
- **Duration computation** is CONTRACT-MODELED at the caller — they compute `duration_hours: int` from `opened_at` and `expires_at` (they own the datetime math). The 4h ceiling is enforced verbatim from §7.8.

## M9 Phase P2 COMPLETE — 5/5 CPs sealed
| CP | Module | Ratchet | Track-a Commit-A |
|----|--------|---------|------------------|
| CP-P2-CP1 · fixed 7-role registry | `services/platform_control_plane/role_registry.py` | 4468→4473 (+5) | `1031ccd35aaa10619c669c7dd40b094e441968a6` |
| CP-P2-CP2 · role_assignment carrier | `services/platform_control_plane/role_assignment.py` | 4473→4480 (+7) | `04eb3c753541f6b085c9df14b6b13679f4227160` |
| CP-P2-CP3 · deny-by-default permission evaluator | `services/platform_control_plane/permission_evaluation.py` | 4480→4490 (+10) | `f3c90a5aedf27f53869134aceccc6b31d844851a` |
| CP-P2-CP4 · session binder (12h absolute · 1h idle) | `services/platform_control_plane/session_binder.py` | 4490→4502 (+12) | `a5af53fa088ae8a016b38effe5f32b982467192a` |
| CP-P2-CP5 · break_glass_session | `services/platform_control_plane/break_glass_session.py` | 4502→4516 (+14) | `ec07fdb0924b3a076a62e52286c309749d2d2f30` |

**Cumulative P2 ratchet delta:** 4468 → 4516 = **+48 monotonic-up · zero rollback.**

**CONTRACT-MODELED items introduced in P2:**
- Item 5 · Live OIDC/SAML SSO per tenant (CP-P2-CP4)
- Item 7 · Real 12-hour absolute / 1-hour idle session lifecycle (CP-P2-CP4)
- Item 8 · Break-glass owner notification via email/webhook (CP-P2-CP5)
- Role → (action, resource_type) authorisation matrix shape (CP-P2-CP3) — this is a P2 net-new CONTRACT-MODELED shape not enumerated in §8's original 15; the concrete OPA/K8s-RBAC binding is a downstream bind-only change.

## Next
Continue autonomously into **P3 · Estate + connector modes + connection test + mode-change approval** per owner directive.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
