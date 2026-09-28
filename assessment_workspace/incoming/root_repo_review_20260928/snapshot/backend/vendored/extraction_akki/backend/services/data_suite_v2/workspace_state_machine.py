"""W-DATA-SUITE-V2-LIFT · CP-D2 · Workspace state machine.

Case-agnostic 4-state linear pipeline: DRAFT → PROCESSING → READY →
ARCHIVED.  No back-edges, no skip-edges.  ARCHIVED terminal.
"""

from __future__ import annotations

from enum import Enum


class WorkspaceLifecycleState(str, Enum):
    DRAFT = "DRAFT"
    PROCESSING = "PROCESSING"
    READY = "READY"
    ARCHIVED = "ARCHIVED"


TRANSITIONS: frozenset = frozenset({
    (WorkspaceLifecycleState.DRAFT, WorkspaceLifecycleState.PROCESSING),
    (WorkspaceLifecycleState.PROCESSING, WorkspaceLifecycleState.READY),
    (WorkspaceLifecycleState.READY, WorkspaceLifecycleState.ARCHIVED),
})


TERMINAL_STATES: frozenset = frozenset({WorkspaceLifecycleState.ARCHIVED})


class IllegalWorkspaceTransition(Exception):
    """Raised when a caller attempts a transition not in `TRANSITIONS`."""


def assert_transition_legal(
    src: WorkspaceLifecycleState,
    dst: WorkspaceLifecycleState,
) -> None:
    """Refuse via `IllegalWorkspaceTransition` if (src, dst) not declared."""
    if (src, dst) not in TRANSITIONS:
        raise IllegalWorkspaceTransition(
            f"illegal transition: {src.value!r} -> {dst.value!r} · legal "
            f"transitions: {sorted((a.value, b.value) for a, b in TRANSITIONS)}"
        )
