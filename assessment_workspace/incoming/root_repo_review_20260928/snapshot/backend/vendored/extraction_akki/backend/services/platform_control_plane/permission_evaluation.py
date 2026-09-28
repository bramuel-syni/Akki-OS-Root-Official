"""services.platform_control_plane.permission_evaluation — CP-P2-CP3 · M9.

Deny-by-default permission evaluator per Akki OS Pilot Platform
Reference v0.2 §7.4 M-A-2 verbatim:

    Permissions are evaluated as action × resource_type × scope,
    deny-by-default. Evaluation happens at the API gateway and again
    inside the data plane.

Thin-kernel evaluator: given a `PermissionRequest` (actor + action +
resource_type + scope) and the actor's `assignments`, plus an OPEN
`authorized_role_action_refs` matrix of `(role, action, resource_type)`
tuples authorised by external policy, return an `allow` or `deny`
verdict.

The role → (action, resource_type) matrix is CONTRACT-MODELED —
concrete authorisation policy is a downstream binding (real OPA
policy engine, hand-coded matrix, or K8s RBAC translation). The
carrier here only fixes the shape and enforces deny-by-default.

Standing-line proof:
- No `bytes` field · all str + tuple.
- No enforcement hard-gate · pure data-in/data-out.
- Zero closed enums · zero domain tokens · zero data-plane imports.
- Deny-by-default: absent any match, verdict is `deny`.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple

from services.platform_control_plane.role_assignment import RoleAssignment


PERMISSION_EVALUATION_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §7.4 "
    "M-A-2 verbatim: Permissions are evaluated as action × "
    "resource_type × scope, deny-by-default. Evaluation happens at "
    "the API gateway and again inside the data plane."
)


# Verdict tokens · OPEN str per case-agnostic doctrine · these are the
# canonical values the caller interprets; the evaluator returns them
# via `PermissionVerdict.verdict_ref`.
VERDICT_ALLOW: str = "allow"
VERDICT_DENY: str = "deny"


# Reason refs · OPEN str · caller composes richer reasons at higher
# layer. These are the minimum-content strings returned by the pure
# evaluator so that downstream audit (P6 audit_event) has a stable
# ref-token to attach.
REASON_NO_SCOPE_MATCH: str = "no_scope_match"
REASON_ROLE_ACTION_NOT_AUTHORISED: str = "role_action_not_authorised"
REASON_MATCH: str = "match"


@dataclasses.dataclass(frozen=True)
class PermissionRequest:
    """Frozen carrier for a permission-evaluation request.

    Exact-order 6 str OPEN fields per §7.4 (action × resource_type ×
    scope · plus actor + resource identity for audit trace):
    - actor_id · the user_id or service_account.id requesting.
    - action · OPEN str action ref (e.g., read, write, admit).
    - resource_type · OPEN str resource_type ref.
    - resource_id · OPEN str specific resource id (opaque · not
      matched at this layer · reserved for downstream audit).
    - scope_type · OPEN str · scope kind (tenant, workspace, …).
    - scope_id · OPEN str · specific scope resource id.
    """
    actor_id: str
    action: str
    resource_type: str
    resource_id: str
    scope_type: str
    scope_id: str


@dataclasses.dataclass(frozen=True)
class PermissionVerdict:
    """Frozen carrier for a permission-evaluation verdict.

    - `verdict_ref` OPEN str · canonical values VERDICT_ALLOW /
      VERDICT_DENY at platform tier · caller composes.
    - `reason_ref` OPEN str · minimum-content stable ref-token for
      downstream audit.
    """
    verdict_ref: str
    reason_ref: str


def assess_permission_grant(
    *,
    request: PermissionRequest,
    assignments: Tuple[RoleAssignment, ...],
    authorized_role_action_refs: Tuple[Tuple[str, str, str], ...],
) -> PermissionVerdict:
    """Deny-by-default permission evaluator · pure data-in/data-out.

    Rule:
    1. Find assignments where `user_id == request.actor_id` AND
       `scope_type == request.scope_type` AND
       `scope_id == request.scope_id`. Call these `in_scope`.
    2. If `in_scope` is empty → deny (reason `no_scope_match`).
    3. Else for each `a` in `in_scope`, if `(a.role, request.action,
       request.resource_type)` ∈ `authorized_role_action_refs`
       → allow (reason `match`).
    4. Else → deny (reason `role_action_not_authorised`).

    No side effects · deterministic · caller composes."""
    actor = request.actor_id
    scope_type = request.scope_type
    scope_id = request.scope_id

    in_scope: Tuple[RoleAssignment, ...] = tuple(
        a for a in assignments
        if a.user_id == actor
        and a.scope_type == scope_type
        and a.scope_id == scope_id
    )

    if not in_scope:
        return PermissionVerdict(
            verdict_ref=VERDICT_DENY,
            reason_ref=REASON_NO_SCOPE_MATCH,
        )

    authorized = frozenset(authorized_role_action_refs)
    for a in in_scope:
        triple = (a.role, request.action, request.resource_type)
        if triple in authorized:
            return PermissionVerdict(
                verdict_ref=VERDICT_ALLOW,
                reason_ref=REASON_MATCH,
            )

    return PermissionVerdict(
        verdict_ref=VERDICT_DENY,
        reason_ref=REASON_ROLE_ACTION_NOT_AUTHORISED,
    )


__all__ = [
    "PERMISSION_EVALUATION_ANCHOR",
    "VERDICT_ALLOW",
    "VERDICT_DENY",
    "REASON_NO_SCOPE_MATCH",
    "REASON_ROLE_ACTION_NOT_AUTHORISED",
    "REASON_MATCH",
    "PermissionRequest",
    "PermissionVerdict",
    "assess_permission_grant",
]
