"""W-DATA-SUITE-V2-LIFT · CP-D1 · Parameterless workspace-boundary signature."""

from __future__ import annotations

from contracts.data_suite_workspace import SurfaceClass, WorkspaceState


def compute_surface(workspace: WorkspaceState) -> SurfaceClass:
    """Map the workspace's `tab_hint` to a closed `SurfaceClass` value."""
    hint = (workspace.tab_hint or "RAPID").upper()
    try:
        return SurfaceClass(hint)
    except ValueError:
        return SurfaceClass.RAPID
