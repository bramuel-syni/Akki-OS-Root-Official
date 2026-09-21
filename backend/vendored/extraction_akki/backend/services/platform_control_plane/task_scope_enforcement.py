"""services.platform_control_plane.task_scope_enforcement — CP-P4-CP4 · M9.

Preventive-charter refusal wrapper composing task-scope invariants
per Akki OS Pilot Platform Reference v0.2 §7.5:

    M-A-3: A job cannot read a connector not listed on its task.
    M-A-4: A job cannot use a connector at a higher mode than the
           task specifies or the connector permits.

Composes with:
- CP-P4-CP3 TaskEntity (task.connector_modes tuple of
  (connector_id, mode) OPEN pairs).
- CP-P3-CP3 connector_mode_lattice (mode_rank for M-A-4 comparison).

Refusals (fail-fast order):
1. connector_id not among task.connector_modes → ConnectorNotOnTaskRefused (M-A-3)
2. rank(job_mode) > rank(task_mode) → ModeAboveTaskSpecRefused (M-A-4)

Standing-line proof:
- Pure function · no side effects · caller composes.
- Zero closed enum type · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

from typing import Tuple

# Composition with connector_mode_lattice (control-plane peer · not a
# data-plane import). Deliberately narrow — only mode_rank.
from services.platform_control_plane.connector_mode_lattice import (
    mode_rank as _mode_rank,
    UnknownModeRefused as _UnknownModeRefused,
)


TASK_SCOPE_ENFORCEMENT_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §7.5 "
    "M-A-3 verbatim: A job cannot read a connector not listed on "
    "its task. M-A-4 verbatim: A job cannot use a connector at a "
    "higher mode than the task specifies or the connector permits."
)


class TaskScopeRefused(Exception):
    """Root refusal for task-scope-enforcement invariants."""


class ConnectorNotOnTaskRefused(TaskScopeRefused):
    """Refused: job connector_id not in task.connector_modes (M-A-3)."""


class ModeAboveTaskSpecRefused(TaskScopeRefused):
    """Refused: job mode rank exceeds the task-specified mode rank
    for the given connector (M-A-4)."""


def _find_task_mode(
    *,
    connector_modes: Tuple[Tuple[str, str], ...],
    connector_id: str,
) -> str:
    """Return the task-specified mode for connector_id · empty
    string when the connector is not on the task."""
    for cid, mode in connector_modes:
        if cid == connector_id:
            return mode
    return ""


def assert_job_connector_admissible(
    *,
    task_connector_modes: Tuple[Tuple[str, str], ...],
    job_connector_id: str,
    job_mode: str,
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refusal order (fail fast):
    1. job_connector_id not among task_connector_modes → ConnectorNotOnTaskRefused (M-A-3).
    2. rank(job_mode) > rank(task_mode) → ModeAboveTaskSpecRefused (M-A-4).

    task_connector_modes is TaskEntity.connector_modes from CP-P4-CP3.
    Mode comparison composes CP-P3-CP3 mode_rank (bubbles
    UnknownModeRefused when either mode is unknown).

    Returns None on admit."""
    task_mode = _find_task_mode(
        connector_modes=task_connector_modes,
        connector_id=job_connector_id,
    )
    if task_mode == "":
        raise ConnectorNotOnTaskRefused(
            f"connector-not-on-task refused: job connector not among "
            f"{len(task_connector_modes)} task connectors (M-A-3)."
        )
    # M-A-4: refuses when job-requested mode rank exceeds task-spec
    # rank · mode_rank refuses on unknown mode (case-sensitive) which
    # bubbles up unchanged for callers who want to detect that path.
    task_rank = _mode_rank(mode=task_mode)
    job_rank = _mode_rank(mode=job_mode)
    if job_rank > task_rank:
        raise ModeAboveTaskSpecRefused(
            f"mode-above-task-spec refused: job mode rank exceeds "
            f"task-spec mode rank (M-A-4)."
        )
    return None


__all__ = [
    "TASK_SCOPE_ENFORCEMENT_ANCHOR",
    "TaskScopeRefused",
    "ConnectorNotOnTaskRefused",
    "ModeAboveTaskSpecRefused",
    "assert_job_connector_admissible",
]
