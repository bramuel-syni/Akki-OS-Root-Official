"""services.platform_control_plane.role_registry — CP-P2-CP1 · M9.

Fixed 7-role registry per Akki OS Pilot Platform Reference v0.2 §7.3
M-A-1 verbatim:

    7 roles ONLY: platform_operator, tenant_owner, tenant_admin,
    data_steward, analyst, viewer, service. "Custom roles are recorded
    as requirements, not built."

Preventive-charter refusal wrapper `assert_role_known` refuses on any
role_ref not in the frozen 7-role tuple. Roles are surfaced as OPEN
str per case-agnostic doctrine.

The registry is a closed SET-OF-VALUES at the platform layer (§7.3
explicitly bans custom roles), but the exposure shape stays OPEN str
so downstream role-assignment / permission-evaluation compose without
schema coupling. Adding an 8th role at the platform tier is a §3.2
clause 5 schema change owner ruling, not a runtime override.

Standing-line proof:
- No `bytes` field · no closed enum type · pure str + tuple.
- No enforcement hard-gate · caller composes.
- Zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

from typing import Tuple


ROLE_REGISTRY_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §7.3 "
    "M-A-1 verbatim: 7 roles ONLY: platform_operator, tenant_owner, "
    "tenant_admin, data_steward, analyst, viewer, service. Custom "
    "roles are recorded as requirements, not built."
)


# §7.3 M-A-1 verbatim 7-role tuple in the source-doc listing order.
PLATFORM_ROLES: Tuple[str, ...] = (
    "platform_operator",
    "tenant_owner",
    "tenant_admin",
    "data_steward",
    "analyst",
    "viewer",
    "service",
)


class RoleRegistryRefused(Exception):
    """Root refusal for role-registry invariants.

    Preventive-charter · caller-invoked only. Message reports COUNTS
    and positional indices only (never role values in the exception
    body)."""


class UnknownRoleRefused(RoleRegistryRefused):
    """Refused: role_ref is not in PLATFORM_ROLES (§7.3 M-A-1
    verbatim ban on custom roles at the platform tier)."""


def assert_role_known(*, role_ref: str) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refuses when `role_ref` is not in the §7.3 M-A-1 verbatim
    PLATFORM_ROLES tuple. Returns None on admit.

    Message reports COUNTS only (never role values)."""
    if role_ref not in frozenset(PLATFORM_ROLES):
        raise UnknownRoleRefused(
            f"unknown-role refused: role_ref not among "
            f"{len(PLATFORM_ROLES)} platform roles per §7.3 M-A-1."
        )
    return None


__all__ = [
    "ROLE_REGISTRY_ANCHOR",
    "PLATFORM_ROLES",
    "RoleRegistryRefused",
    "UnknownRoleRefused",
    "assert_role_known",
]
