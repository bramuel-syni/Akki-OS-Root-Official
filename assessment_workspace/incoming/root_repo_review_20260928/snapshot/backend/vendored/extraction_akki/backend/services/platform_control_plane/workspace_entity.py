"""services.platform_control_plane.workspace_entity — CP-P1-CP3 · M9.

Freezes the control-plane `workspace` record shape per Akki OS Pilot
Platform Reference v0.2 (17 September 2026) §10 verbatim:

    workspace(id, tenant_id, name, is_default)

§2 definition: "Workspace — division inside a tenant used to scope
users and outputs. Every tenant has at least one."

Pure carrier · no refusal wrapper · no I/O · no data-plane imports.
Ownership isolation invariant is anchored by the top-level
`tenant_id: str` field at exact-order position 2 (index 1) —
composition surface for CP-P1-CP1 cross-tenant refusal.
"""
from __future__ import annotations

import dataclasses


WORKSPACE_ENTITY_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §10 "
    "verbatim control-plane data model: "
    "workspace(id, tenant_id, name, is_default). "
    "§2 definition: 'Workspace — division inside a tenant used to "
    "scope users and outputs. Every tenant has at least one.'"
)


@dataclasses.dataclass(frozen=True)
class WorkspaceEntity:
    """Frozen carrier for the control-plane `workspace` record.

    Ownership isolation invariant is anchored by the top-level
    `tenant_id: str` field at exact-order position 2 (index 1).
    `is_default: bool` is the sole non-str field (§10 boolean semantics
    by domain).
    """
    id: str
    tenant_id: str
    name: str
    is_default: bool


WORKSPACE_ENTITY_FIELDS = tuple(f.name for f in dataclasses.fields(WorkspaceEntity))


__all__ = [
    "WORKSPACE_ENTITY_ANCHOR",
    "WORKSPACE_ENTITY_FIELDS",
    "WorkspaceEntity",
]
