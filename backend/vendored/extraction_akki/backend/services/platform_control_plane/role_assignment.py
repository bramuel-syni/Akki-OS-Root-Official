"""services.platform_control_plane.role_assignment — CP-P2-CP2 · M9.

Pure frozen carrier for the control-plane `role_assignment` record per
Akki OS Pilot Platform Reference v0.2 §10 verbatim:

    role_assignment (id, user_id, role, scope_type, scope_id,
                     granted_by, granted_at)

§7.4 verbatim: "Permissions are evaluated as action × resource_type ×
scope, deny-by-default. Evaluation happens at the API gateway and
again inside the data plane."

`role` is an OPEN str ref that downstream evaluation composes with
CP-P2-CP1 `assert_role_known`. `scope_type` / `scope_id` are OPEN str
per case-agnostic doctrine (scope_type ∈ {tenant, workspace, task, …}
but no closed enum at the carrier layer).

Granter/grantee refusal semantics (preventive-charter):
- self-grant refused (granted_by == user_id) — no operator can grant
  a role to themselves without a second authoriser; the second-
  authoriser mechanism is a downstream CP (break-glass P2-CP5 or
  higher-authority chain) that composes on top of this refusal.

Standing-line proof:
- No `bytes` field · all str · 7 exact-order fields.
- No enforcement hard-gate · pure data · caller composes.
- Zero closed enums · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


ROLE_ASSIGNMENT_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §10 "
    "verbatim: role_assignment (id, user_id, role, scope_type, "
    "scope_id, granted_by, granted_at). §7.4: Permissions are "
    "evaluated as action × resource_type × scope, deny-by-default. "
    "Evaluation happens at the API gateway and again inside the "
    "data plane."
)


@dataclasses.dataclass(frozen=True)
class RoleAssignment:
    """Frozen carrier for a control-plane role_assignment record.

    Exact-order 7 str OPEN fields per §10:
    - id · assignment record id (OPEN opaque).
    - user_id · grantee user id (OPEN opaque · references §10 user).
    - role · role_ref (OPEN str · composed with CP-P2-CP1
      assert_role_known at the caller side).
    - scope_type · OPEN str · scope kind (tenant, workspace, task, …).
    - scope_id · OPEN str · specific scope resource id.
    - granted_by · granter user_id (OPEN opaque).
    - granted_at · ISO-8601 timestamp str (OPEN str).
    """
    id: str
    user_id: str
    role: str
    scope_type: str
    scope_id: str
    granted_by: str
    granted_at: str


ROLE_ASSIGNMENT_FIELDS: Tuple[str, ...] = (
    "id",
    "user_id",
    "role",
    "scope_type",
    "scope_id",
    "granted_by",
    "granted_at",
)


class RoleAssignmentRefused(Exception):
    """Root refusal for role-assignment invariants.

    Preventive-charter · caller-invoked only. Message reports COUNTS
    and positional indices only (never id / user_id / role values in
    the exception body)."""


class SelfGrantRefused(RoleAssignmentRefused):
    """Refused: granted_by == user_id (self-grant not permitted at
    the platform tier · second-authoriser mechanism is a downstream
    CP)."""


def assert_role_assignment_valid(*, assignment: RoleAssignment) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refuses when `granted_by == user_id` (self-grant). Returns None on
    admit.

    Message reports COUNTS only (never id / user_id / role values)."""
    if assignment.granted_by == assignment.user_id:
        raise SelfGrantRefused(
            f"self-grant refused: granted_by matches user_id at "
            f"positional index {ROLE_ASSIGNMENT_FIELDS.index('user_id')} "
            f"and {ROLE_ASSIGNMENT_FIELDS.index('granted_by')}."
        )
    return None


__all__ = [
    "ROLE_ASSIGNMENT_ANCHOR",
    "ROLE_ASSIGNMENT_FIELDS",
    "RoleAssignment",
    "RoleAssignmentRefused",
    "SelfGrantRefused",
    "assert_role_assignment_valid",
]
