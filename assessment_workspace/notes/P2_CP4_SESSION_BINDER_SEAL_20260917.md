READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-P2-CP4 · M9 · Platform-layer session binder · seal note · 2026-09-17T~04:50Z

**Track-a HEAD:** `a5af53fa088ae8a016b38effe5f32b982467192a`. **Ratchet:** 4490 → **4502** (+12).

## Anchor
§7.2 M-A-6 verbatim: *"Sessions: 12h absolute lifetime · 1h idle timeout · revocable by tenant admin. Data-plane agents auth via short-lived certs bound to tenant_id."*
§4.3 verbatim: *"The API gateway resolves tenant_id from the authenticated session and injects it into every request. Clients cannot supply it."*

## Mechanism
`services/platform_control_plane/session_binder.py`:

- `Session` frozen dataclass · 8 exact-order str OPEN fields (`session_id · tenant_id · user_id · issued_at · last_activity_at · absolute_expires_at · idle_timeout_at · revoked_at`).
- `SESSION_FIELDS` tuple.
- Constants: `SESSION_ABSOLUTE_LIFETIME_HOURS = 12` · `SESSION_IDLE_TIMEOUT_HOURS = 1` (verbatim §7.2 M-A-6).
- Empty-string convention for `revoked_at` (avoid Optional at carrier layer per no-speculative-shape rule).
- `assert_session_valid(*, session, at_iso) -> None` — preventive-charter · fail-fast refusal order:
  1. `tenant_id == ""` → `SessionUnboundRefused` (§4.3 clients cannot supply tenant_id).
  2. `revoked_at != ""` → `SessionRevokedRefused`.
  3. `at_iso > absolute_expires_at` → `SessionAbsoluteExpiredRefused` (§7.2 12h).
  4. `at_iso > idle_timeout_at` → `SessionIdleTimeoutRefused` (§7.2 1h).
- 5 refusal classes (`SessionRefused` root + 4 subclasses). COUNTS-only messages. Lexicographic ISO-8601 UTC 'Z' str comparison — no datetime parsing at carrier.

## Invariants (12)
1. Module fabric present + `__all__` match (11-name set).
2. `Session` frozen 8 exact-order fields.
3. `SESSION_FIELDS` matches dataclass fields.
4. `SESSION_ABSOLUTE_LIFETIME_HOURS == 12 · SESSION_IDLE_TIMEOUT_HOURS == 1`.
5. Refusal hierarchy (root + 4 subclasses).
6. Refuses on unbound tenant_id.
7. Refuses on revoked session.
8. Refuses on absolute-expired.
9. Refuses on idle-timeout (not yet absolute-expired).
10. Admits when bound + unrevoked + not-expired (incl. boundary at_iso == idle_timeout_at).
11. Refusal-order: absolute-expired fires BEFORE idle-timeout when both trip.
12. Verbatim anchor + 21-token grep-negative + data-plane import-negative.

## Double-green under `BASELINE_GUARD=1`
GREEN 1 `4502 / 1 / 0 in 124.68s` + GREEN 2 `4502 / 1 / 0 in 125.31s`.

## §3.3 3-commit
- A `a5af53fa088ae8a016b38effe5f32b982467192a` ✅.
- B `e1681becb0731710d93d9f1ce82ee7fe08561c96` (master) ✅.
- C this-turn (fixup banks Commit-B SHA).

## GPU util at seal boundary
Elapsed **25.10 h** · remaining **46.90 h**.

## CONTRACT-MODELED items enabled
- **Item 5** · Live OIDC/SAML SSO per tenant. Session carries resolved `tenant_id + timing` only; `auth_method` rides on the user entity (CP-P1-CP4). Real IdP wiring is a downstream bind-only change (JIT session-to-tenant_id resolution).
- **Item 7** · Real 12-hour absolute / 1-hour idle session lifecycle. Wall-clock lives at the caller (`at_iso` supplied). Real session-store binding (Redis/DB) is a downstream bind-only change.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
