"""services.platform_control_plane.mode_change_approval — CP-P3-CP4 · M9.

Preventive-charter mode-change approval carrier per Akki OS Pilot
Platform Reference v0.2 §5.3 M-C-4 verbatim:

    Raising a connector's mode requires approval by a data_steward
    or tenant_admin, is logged, and invalidates any task that
    referenced the connector until the task is re-approved.

Carrier shape (10 fields · not in §10 — this is an approval record
which composes downstream audit_event refs):
- id · connector_id · from_mode · to_mode
- approver_id · approver_role_ref (must be data_steward or
  tenant_admin)
- log_ref (audit log entry ref · non-empty)
- dependent_task_scan_ref (scan-was-performed marker · non-empty)
- invalidated_task_refs (tuple of task ids per §5.3 M-C-4 · may be
  empty if scan showed no dependent tasks)
- approved_at

Refusals:
- approver_id empty OR approver_role_ref empty → MissingApproverRefused
- approver_role_ref not in APPROVER_ROLES → InvalidApproverRoleRefused
- log_ref empty → MissingLogRefRefused
- dependent_task_scan_ref empty → MissingDependentTaskInvalidationSetRefused

Composes with CP-P3-CP3 `assert_downgrade_only`: caller invokes this
CP's assert only when CP-P3-CP3 refused an upgrade (approval path).

Standing-line proof:
- 9 str + 1 tuple[str, ...] · 10 fields exact-order.
- No enforcement hard-gate · caller composes.
- APPROVER_ROLES surfaced as OPEN str tuple (composition on CP-P2-CP1
  PLATFORM_ROLES · not a duplicate closed enum).
- Zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


MODE_CHANGE_APPROVAL_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §5.3 "
    "M-C-4 verbatim: Raising a connector's mode requires approval "
    "by a data_steward or tenant_admin, is logged, and invalidates "
    "any task that referenced the connector until the task is "
    "re-approved."
)


# §5.3 M-C-4 verbatim: approver role must be one of these two.
# OPEN str · these values MUST appear in CP-P2-CP1 PLATFORM_ROLES
# tuple; the platform-role list is authoritative there.
APPROVER_ROLES: Tuple[str, ...] = (
    "data_steward",
    "tenant_admin",
)


@dataclasses.dataclass(frozen=True)
class ModeChangeApproval:
    """Frozen carrier for a connector mode-change approval record.

    Exact-order 10 fields (9 str + 1 tuple[str, ...]):
    - id · approval record id.
    - connector_id · id of the connector being changed.
    - from_mode / to_mode · connector mode refs (composed with
      CP-P3-CP3 lattice).
    - approver_id · user_id of the approver.
    - approver_role_ref · MUST be in APPROVER_ROLES per §5.3 M-C-4.
    - log_ref · audit log entry ref · non-empty per §5.3 M-C-4
      "is logged".
    - dependent_task_scan_ref · non-empty marker that the caller has
      performed the dependent-task scan · empty means scan missing.
    - invalidated_task_refs · tuple of task-id refs invalidated per
      §5.3 M-C-4 · may be empty tuple when scan showed no dependents.
    - approved_at · ISO-8601 UTC 'Z' str.
    """
    id: str
    connector_id: str
    from_mode: str
    to_mode: str
    approver_id: str
    approver_role_ref: str
    log_ref: str
    dependent_task_scan_ref: str
    invalidated_task_refs: Tuple[str, ...]
    approved_at: str


MODE_CHANGE_APPROVAL_FIELDS: Tuple[str, ...] = (
    "id",
    "connector_id",
    "from_mode",
    "to_mode",
    "approver_id",
    "approver_role_ref",
    "log_ref",
    "dependent_task_scan_ref",
    "invalidated_task_refs",
    "approved_at",
)


class ModeChangeApprovalRefused(Exception):
    """Root refusal for mode-change-approval invariants."""


class MissingApproverRefused(ModeChangeApprovalRefused):
    """Refused: approver_id or approver_role_ref is empty."""


class InvalidApproverRoleRefused(ModeChangeApprovalRefused):
    """Refused: approver_role_ref not in APPROVER_ROLES (§5.3 M-C-4
    requires data_steward or tenant_admin)."""


class MissingLogRefRefused(ModeChangeApprovalRefused):
    """Refused: log_ref is empty (§5.3 M-C-4 "is logged")."""


class MissingDependentTaskInvalidationSetRefused(ModeChangeApprovalRefused):
    """Refused: dependent_task_scan_ref is empty · caller has not
    performed the dependent-task scan per §5.3 M-C-4."""


def assert_mode_change_approval_valid(
    *, approval: ModeChangeApproval,
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refusal order (fail fast):
    1. approver_id or approver_role_ref empty → MissingApproverRefused.
    2. approver_role_ref not in APPROVER_ROLES →
       InvalidApproverRoleRefused.
    3. log_ref empty → MissingLogRefRefused.
    4. dependent_task_scan_ref empty →
       MissingDependentTaskInvalidationSetRefused.

    Returns None on admit."""
    if approval.approver_id == "" or approval.approver_role_ref == "":
        raise MissingApproverRefused(
            f"missing-approver refused: approver_id or "
            f"approver_role_ref empty at positional indices "
            f"{MODE_CHANGE_APPROVAL_FIELDS.index('approver_id')} / "
            f"{MODE_CHANGE_APPROVAL_FIELDS.index('approver_role_ref')}."
        )
    if approval.approver_role_ref not in frozenset(APPROVER_ROLES):
        raise InvalidApproverRoleRefused(
            f"invalid-approver-role refused: approver_role_ref not "
            f"among {len(APPROVER_ROLES)} §5.3 M-C-4 roles."
        )
    if approval.log_ref == "":
        raise MissingLogRefRefused(
            f"missing-log-ref refused: log_ref at positional index "
            f"{MODE_CHANGE_APPROVAL_FIELDS.index('log_ref')} empty · "
            f"§5.3 M-C-4 'is logged'."
        )
    if approval.dependent_task_scan_ref == "":
        raise MissingDependentTaskInvalidationSetRefused(
            f"missing-dependent-task-invalidation-set refused: "
            f"dependent_task_scan_ref at positional index "
            f"{MODE_CHANGE_APPROVAL_FIELDS.index('dependent_task_scan_ref')} "
            f"empty · §5.3 M-C-4 dependent-task scan required."
        )
    return None


__all__ = [
    "MODE_CHANGE_APPROVAL_ANCHOR",
    "APPROVER_ROLES",
    "MODE_CHANGE_APPROVAL_FIELDS",
    "ModeChangeApproval",
    "ModeChangeApprovalRefused",
    "MissingApproverRefused",
    "InvalidApproverRoleRefused",
    "MissingLogRefRefused",
    "MissingDependentTaskInvalidationSetRefused",
    "assert_mode_change_approval_valid",
]
