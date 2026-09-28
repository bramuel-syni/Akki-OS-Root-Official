"""services.platform_control_plane.session_binder — CP-P2-CP4 · M9.

Session→tenant_id binding + expiry/revocation refusal wrapper per
Akki OS Pilot Platform Reference v0.2 §7.2 M-A-6 verbatim:

    Sessions: 12h absolute lifetime · 1h idle timeout · revocable by
    tenant admin. Data-plane agents auth via short-lived certs bound
    to tenant_id.

§4.3 verbatim: The API gateway resolves tenant_id from the
authenticated session and injects it into every request. Clients
cannot supply it.

Thin-kernel carrier + preventive-charter refusal:
- `Session` frozen carrier (8 fields · all str OPEN).
- Timestamps are ISO-8601 str OPEN · comparison is lexicographic
  (caller supplies normalised UTC 'Z' format · no datetime parsing
  at carrier layer · matches case-agnostic doctrine).
- `assert_session_valid` refuses on: unbound tenant_id, revoked,
  past absolute-expiry, past idle-timeout.

CONTRACT-MODELED items enabled (from §8):
- Item 5 · Live OIDC/SAML SSO per tenant — auth method rides on the
  user entity; session ONLY carries the resolved tenant_id + timing.
  The IdP wiring is a downstream bind-only change.
- Item 7 · Real 12-hour absolute / 1-hour idle session lifecycle —
  wall-clock comparison happens at the caller (`at_iso` supplied);
  real session-store wiring is a downstream bind-only change.

Standing-line proof:
- No `bytes` field · all str · 8 exact-order fields.
- No enforcement hard-gate · caller invokes with `at_iso`.
- Zero closed enums · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


SESSION_BINDER_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §7.2 "
    "M-A-6 verbatim: Sessions: 12h absolute lifetime · 1h idle "
    "timeout · revocable by tenant admin. Data-plane agents auth via "
    "short-lived certs bound to tenant_id. §4.3: The API gateway "
    "resolves tenant_id from the authenticated session and injects "
    "it into every request. Clients cannot supply it."
)


# §7.2 M-A-6 verbatim lifetime constants · hours as int.
SESSION_ABSOLUTE_LIFETIME_HOURS: int = 12
SESSION_IDLE_TIMEOUT_HOURS: int = 1


@dataclasses.dataclass(frozen=True)
class Session:
    """Frozen carrier for a control-plane session.

    Exact-order 8 str OPEN fields:
    - session_id · OPEN opaque.
    - tenant_id · OPEN opaque · bound at issue-time by API gateway
      per §4.3 · MUST be non-empty for a bound session.
    - user_id · OPEN opaque · grantee.
    - issued_at · ISO-8601 UTC 'Z' str (OPEN).
    - last_activity_at · ISO-8601 UTC 'Z' str (OPEN) · updated by
      caller on every request; used for 1h idle-timeout.
    - absolute_expires_at · ISO-8601 UTC 'Z' str (OPEN) · caller
      composes issued_at + 12h.
    - idle_timeout_at · ISO-8601 UTC 'Z' str (OPEN) · caller composes
      last_activity_at + 1h.
    - revoked_at · ISO-8601 UTC 'Z' str (OPEN) OR "" when not
      revoked (empty-string convention · avoids Optional at carrier
      layer per no-speculative-shape rule).
    """
    session_id: str
    tenant_id: str
    user_id: str
    issued_at: str
    last_activity_at: str
    absolute_expires_at: str
    idle_timeout_at: str
    revoked_at: str


SESSION_FIELDS: Tuple[str, ...] = (
    "session_id",
    "tenant_id",
    "user_id",
    "issued_at",
    "last_activity_at",
    "absolute_expires_at",
    "idle_timeout_at",
    "revoked_at",
)


class SessionRefused(Exception):
    """Root refusal for session-binder invariants.

    Preventive-charter · caller-invoked only. Message reports COUNTS
    and positional indices only (never session_id / tenant_id /
    user_id / timestamps in the exception body)."""


class SessionUnboundRefused(SessionRefused):
    """Refused: session.tenant_id is empty (client-supplied tenant_id
    is forbidden per §4.3; a valid session ALWAYS carries a resolved
    tenant_id injected by the API gateway)."""


class SessionRevokedRefused(SessionRefused):
    """Refused: session.revoked_at is not empty (revoked by tenant
    admin per §7.2 M-A-6)."""


class SessionAbsoluteExpiredRefused(SessionRefused):
    """Refused: at_iso > absolute_expires_at (past 12h absolute
    lifetime per §7.2 M-A-6)."""


class SessionIdleTimeoutRefused(SessionRefused):
    """Refused: at_iso > idle_timeout_at (past 1h idle timeout per
    §7.2 M-A-6)."""


def assert_session_valid(*, session: Session, at_iso: str) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refusal order (fail fast on the more fundamental violation):
    1. tenant_id empty → SessionUnboundRefused.
    2. revoked_at not empty → SessionRevokedRefused.
    3. at_iso > absolute_expires_at → SessionAbsoluteExpiredRefused.
    4. at_iso > idle_timeout_at → SessionIdleTimeoutRefused.

    Returns None on admit.

    Comparison is lexicographic on ISO-8601 UTC 'Z' str · caller
    supplies normalised timestamps. No datetime parsing at carrier
    layer. Message reports COUNTS/positional index only."""
    if session.tenant_id == "":
        raise SessionUnboundRefused(
            f"session-unbound refused: tenant_id empty at positional "
            f"index {SESSION_FIELDS.index('tenant_id')} · client-"
            f"supplied tenant_id is forbidden per §4.3."
        )
    if session.revoked_at != "":
        raise SessionRevokedRefused(
            f"session-revoked refused: revoked_at non-empty at "
            f"positional index {SESSION_FIELDS.index('revoked_at')}."
        )
    if at_iso > session.absolute_expires_at:
        raise SessionAbsoluteExpiredRefused(
            f"session-absolute-expired refused: at_iso > "
            f"absolute_expires_at at positional index "
            f"{SESSION_FIELDS.index('absolute_expires_at')} · "
            f"§7.2 M-A-6 · {SESSION_ABSOLUTE_LIFETIME_HOURS}h."
        )
    if at_iso > session.idle_timeout_at:
        raise SessionIdleTimeoutRefused(
            f"session-idle-timeout refused: at_iso > idle_timeout_at "
            f"at positional index "
            f"{SESSION_FIELDS.index('idle_timeout_at')} · §7.2 M-A-6 · "
            f"{SESSION_IDLE_TIMEOUT_HOURS}h."
        )
    return None


__all__ = [
    "SESSION_BINDER_ANCHOR",
    "SESSION_ABSOLUTE_LIFETIME_HOURS",
    "SESSION_IDLE_TIMEOUT_HOURS",
    "SESSION_FIELDS",
    "Session",
    "SessionRefused",
    "SessionUnboundRefused",
    "SessionRevokedRefused",
    "SessionAbsoluteExpiredRefused",
    "SessionIdleTimeoutRefused",
    "assert_session_valid",
]
