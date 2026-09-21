"""services.platform_control_plane.task_entity — CP-P4-CP3 · M9.

Pure frozen carrier for control-plane task record per Akki OS Pilot
Platform Reference v0.2 §10 verbatim:

    task (id, tenant_id, workspace_id, mou_task_ref, objective,
          connector_modes, compute_integration_id, status,
          approved_by, approved_at)

Row 186 anchor: connector_modes as tuple of (connector_id, mode)
OPEN pairs. All other fields are OPEN str per case-agnostic doctrine.

§7.5 anchors (M-A-3..M-A-5) enforced downstream:
- CP-P4-CP4 TASK-SCOPE-ENFORCEMENT — refusal on job-connector-not-on-task
  or job-mode-above-task-spec.
- CP-P4-CP5 TASK-APPROVAL-INVALIDATION — refusal on approved-state
  when connectors/modes/compute change without re-approval.

Pure carrier · no refusal wrapper · caller composes downstream
validation.

Standing-line proof:
- 9 str + 1 tuple[tuple[str, str], ...] · 10 fields exact-order.
- Zero closed enum type · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


TASK_ENTITY_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §10 "
    "verbatim: task (id, tenant_id, workspace_id, mou_task_ref, "
    "objective, connector_modes, compute_integration_id, status, "
    "approved_by, approved_at). Row 186 anchor: connector_modes as "
    "tuple of (connector_id, mode) OPEN pairs. §7.5 M-A-3..M-A-5 "
    "anchors enforced downstream at CP-P4-CP4/CP5."
)


@dataclasses.dataclass(frozen=True)
class TaskEntity:
    """Frozen carrier for the control-plane task record.

    Exact-order 10 fields (9 str + 1 tuple[tuple[str, str], ...]):
    - id · task record id.
    - tenant_id · owning tenant (ownership isolation index 1).
    - workspace_id · owning workspace (composes with CP-P1-CP3
      WorkspaceEntity via id).
    - mou_task_ref · MoU task reference (OPEN str).
    - objective · task objective descriptor (OPEN str).
    - connector_modes · tuple of (connector_id, mode) OPEN pairs
      per row 186 · empty tuple admits at carrier layer · downstream
      CP-P4-CP4 composes membership/mode-rank refusal.
    - compute_integration_id · target compute integration
      (composes with CP-P4-CP1 ComputeIntegrationEntity.id).
    - status · lifecycle status (OPEN str · e.g., pending_approval,
      approved, invalidated · concrete FSM CONTRACT-MODELED).
    - approved_by · user_id ref of approver (empty when
      pending_approval).
    - approved_at · ISO-8601 UTC 'Z' str (empty when
      pending_approval).
    """
    id: str
    tenant_id: str
    workspace_id: str
    mou_task_ref: str
    objective: str
    connector_modes: Tuple[Tuple[str, str], ...]
    compute_integration_id: str
    status: str
    approved_by: str
    approved_at: str


TASK_ENTITY_FIELDS: Tuple[str, ...] = (
    "id",
    "tenant_id",
    "workspace_id",
    "mou_task_ref",
    "objective",
    "connector_modes",
    "compute_integration_id",
    "status",
    "approved_by",
    "approved_at",
)


__all__ = [
    "TASK_ENTITY_ANCHOR",
    "TASK_ENTITY_FIELDS",
    "TaskEntity",
]
