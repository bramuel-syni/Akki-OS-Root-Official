"""services.platform_control_plane.task_invalidation — CP-P4-CP5 · M9.

Preventive-charter task-approval-invalidation refusal wrapper per
Akki OS Pilot Platform Reference v0.2 §7.5:

    M-A-5: Any change to a task's connectors, modes or compute
           invalidates its approval; the task returns to
           pending_approval.

Composes with CP-P4-CP3 TaskEntity (before-approved and after-
proposed snapshots) and the connector_modes tuple shape from row
186 (tuple of (connector_id, mode) pairs).

Refusals (fail-fast order):
1. connector_modes tuple differs AND after.status !=
   TASK_PENDING_APPROVAL → StaleApprovalOnConnectorModesChangeRefused
2. compute_integration_id differs AND after.status !=
   TASK_PENDING_APPROVAL → StaleApprovalOnComputeIntegrationChangeRefused

Standing-line proof:
- Pure function · no side effects · caller composes.
- Zero closed enum type · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

# Composition with TaskEntity (control-plane peer). Deliberately
# narrow — only the frozen carrier for shape access.
from services.platform_control_plane.task_entity import (
    TaskEntity as _TaskEntity,
)


TASK_INVALIDATION_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §7.5 "
    "M-A-5 verbatim: Any change to a task's connectors, modes or "
    "compute invalidates its approval; the task returns to "
    "pending_approval."
)


# §4.7 tenant-lifecycle vocabulary is separate from task-status
# vocabulary; §10 task.status is OPEN str. The verbatim M-A-5 phrase
# "returns to pending_approval" fixes the sentinel token as OPEN str.
TASK_PENDING_APPROVAL: str = "pending_approval"


class TaskApprovalRefused(Exception):
    """Root refusal for task-approval-invalidation invariants."""


class StaleApprovalOnConnectorModesChangeRefused(TaskApprovalRefused):
    """Refused: connector_modes tuple changed but after.status is
    not TASK_PENDING_APPROVAL (M-A-5)."""


class StaleApprovalOnComputeIntegrationChangeRefused(TaskApprovalRefused):
    """Refused: compute_integration_id changed but after.status is
    not TASK_PENDING_APPROVAL (M-A-5)."""


def assert_task_approval_valid(
    *,
    before_approved: _TaskEntity,
    after_proposed: _TaskEntity,
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Compares before_approved (last approved TaskEntity snapshot) to
    after_proposed (the proposed edit). Refusal order (fail fast):

    1. connector_modes tuple differs AND after.status !=
       TASK_PENDING_APPROVAL → StaleApprovalOnConnectorModesChangeRefused
       (§7.5 M-A-5 "connectors, modes" clause).
    2. compute_integration_id differs AND after.status !=
       TASK_PENDING_APPROVAL → StaleApprovalOnComputeIntegrationChangeRefused
       (§7.5 M-A-5 "compute" clause).

    Returns None on admit (no relevant change OR status returned to
    pending_approval as required by M-A-5).
    """
    if before_approved.connector_modes != after_proposed.connector_modes:
        if after_proposed.status != TASK_PENDING_APPROVAL:
            raise StaleApprovalOnConnectorModesChangeRefused(
                f"stale-approval-on-connector-modes-change refused: "
                f"connector_modes changed and after.status is not "
                f"TASK_PENDING_APPROVAL (§7.5 M-A-5)."
            )
    if (
        before_approved.compute_integration_id
        != after_proposed.compute_integration_id
    ):
        if after_proposed.status != TASK_PENDING_APPROVAL:
            raise StaleApprovalOnComputeIntegrationChangeRefused(
                f"stale-approval-on-compute-integration-change refused: "
                f"compute_integration_id changed and after.status is not "
                f"TASK_PENDING_APPROVAL (§7.5 M-A-5)."
            )
    return None


__all__ = [
    "TASK_INVALIDATION_ANCHOR",
    "TASK_PENDING_APPROVAL",
    "TaskApprovalRefused",
    "StaleApprovalOnConnectorModesChangeRefused",
    "StaleApprovalOnComputeIntegrationChangeRefused",
    "assert_task_approval_valid",
]
