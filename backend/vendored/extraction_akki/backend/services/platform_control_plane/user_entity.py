"""services.platform_control_plane.user_entity — CP-P1-CP4 · M9.

Freezes the control-plane `user` record shape per Akki OS Pilot
Platform Reference v0.2 (17 September 2026) §10 verbatim:

    user(id, tenant_id, email, status, auth_method, mfa_enrolled,
         created_at)

§7.2 anchors: users are tenant-scoped; `auth_method` supports native
+ SSO OIDC/SAML (OPEN str per case-agnostic doctrine); `mfa_enrolled`
is boolean by domain nature.

Pure carrier · caller composes validation (CP-P1-CP1 cross-tenant
· CP-P2-CP1 role validation via `role_assignment.user_id` ref).
"""
from __future__ import annotations

import dataclasses


USER_ENTITY_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §10 "
    "verbatim control-plane data model: "
    "user(id, tenant_id, email, status, auth_method, mfa_enrolled, "
    "created_at). §7.2 anchors: users are tenant-scoped · auth_method "
    "supports native + SSO OIDC + SSO SAML (OPEN str · case-agnostic) · "
    "mfa_enrolled boolean by domain nature."
)


@dataclasses.dataclass(frozen=True)
class UserEntity:
    """Frozen carrier for the control-plane `user` record.

    Ownership isolation anchored at `tenant_id` (position 2 · index 1).
    `mfa_enrolled: bool` is domain-inherent boolean; all other fields
    OPEN str per case-agnostic doctrine.
    """
    id: str
    tenant_id: str
    email: str
    status: str
    auth_method: str
    mfa_enrolled: bool
    created_at: str


USER_ENTITY_FIELDS = tuple(f.name for f in dataclasses.fields(UserEntity))


__all__ = [
    "USER_ENTITY_ANCHOR",
    "USER_ENTITY_FIELDS",
    "UserEntity",
]
