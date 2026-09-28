"""W-DATA-SUITE-V2-LIFT · CP-D1 · Parameterless workspace-boundary signature.

Lands FIRST per Solva-V2 CP-S2 precedent.  Exactly one parameter.
Return type = SurfaceClass.  Signature-as-guard invariants: no
`confidence`, `strength`, `weight`, `evidence`, `score`, or `priors`.
"""

from __future__ import annotations

from contracts.data_suite_workspace import SurfaceClass, WorkspaceState


def compute_surface(workspace: WorkspaceState) -> SurfaceClass:
    """Map the workspace's `tab_hint` to a closed `SurfaceClass` value.

    If `tab_hint` is unrecognised, defaults to `RAPID` (safest / most
    permissive · matches prototype v8 §6.2 landing tab).
    """
    hint = (workspace.tab_hint or "RAPID").upper()
    try:
        return SurfaceClass(hint)
    except ValueError:
        return SurfaceClass.RAPID
