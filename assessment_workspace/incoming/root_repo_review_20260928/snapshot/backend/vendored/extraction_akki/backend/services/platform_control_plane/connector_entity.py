"""services.platform_control_plane.connector_entity — CP-P3-CP2 · M9.

Pure frozen carrier for the control-plane `connector` record per
Akki OS Pilot Platform Reference v0.2 §10 verbatim:

    connector (id, tenant_id, estate_id, type, location,
               credential_ref, scope, mode, mou_task_ref, status)

§5.2 M-C-1 verbatim: "Every connector carries: type, location,
credential_ref, scope, mode, mou_task_ref, status. Empty scope is
invalid."

Preventive-charter refusals:
- empty `scope` → EmptyScopeRefused.
- empty `mou_task_ref` → MissingMouTaskRefRefused.

Standing-line proof:
- All 10 str · exact-order.
- No enforcement hard-gate · caller composes.
- Zero closed enums (type/mode/status/scope surfaced as OPEN str).
- Zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


CONNECTOR_ENTITY_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §10 "
    "verbatim: connector (id, tenant_id, estate_id, type, location, "
    "credential_ref, scope, mode, mou_task_ref, status). §5.2 M-C-1 "
    "verbatim: Every connector carries: type, location, "
    "credential_ref, scope, mode, mou_task_ref, status. Empty scope "
    "is invalid."
)


@dataclasses.dataclass(frozen=True)
class ConnectorEntity:
    """Frozen carrier for a control-plane connector per §10.

    Exact-order 10 str OPEN fields:
    - id · OPEN opaque.
    - tenant_id · OPEN opaque (§3.1 M-T-2 ownership).
    - estate_id · OPEN opaque (references §10 estate).
    - type · OPEN str · connector type (e.g., mysql, obs, nas).
    - location · OPEN str · network location ref.
    - credential_ref · OPEN opaque · reference to secret store.
    - scope · OPEN str · scope of what the connector may see.
      MUST be non-empty per §5.2 M-C-1.
    - mode · OPEN str · one of connector_mode_lattice values
      (composed at CP-P3-CP3).
    - mou_task_ref · OPEN opaque · MoU task ref binding.
      MUST be non-empty per §5.2 M-C-1.
    - status · OPEN str · connector operational status.
    """
    id: str
    tenant_id: str
    estate_id: str
    type: str
    location: str
    credential_ref: str
    scope: str
    mode: str
    mou_task_ref: str
    status: str


CONNECTOR_ENTITY_FIELDS: Tuple[str, ...] = (
    "id",
    "tenant_id",
    "estate_id",
    "type",
    "location",
    "credential_ref",
    "scope",
    "mode",
    "mou_task_ref",
    "status",
)


class ConnectorEntityRefused(Exception):
    """Root refusal for connector-entity invariants.

    Preventive-charter · caller-invoked only. Message reports COUNTS
    and positional indices only (never id / tenant_id / scope / mode
    values in the exception body)."""


class EmptyScopeRefused(ConnectorEntityRefused):
    """Refused: connector.scope is empty (§5.2 M-C-1 verbatim
    'Empty scope is invalid.')."""


class MissingMouTaskRefRefused(ConnectorEntityRefused):
    """Refused: connector.mou_task_ref is empty (§5.2 M-C-1
    mou_task_ref required)."""


def assert_connector_carrier_valid(*, connector: ConnectorEntity) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refusal order (fail fast):
    1. scope empty → EmptyScopeRefused.
    2. mou_task_ref empty → MissingMouTaskRefRefused.

    Returns None on admit. Message reports COUNTS/positional index."""
    if connector.scope == "":
        raise EmptyScopeRefused(
            f"empty-scope refused: scope at positional index "
            f"{CONNECTOR_ENTITY_FIELDS.index('scope')} is empty · "
            f"§5.2 M-C-1 'Empty scope is invalid.'"
        )
    if connector.mou_task_ref == "":
        raise MissingMouTaskRefRefused(
            f"missing-mou-task-ref refused: mou_task_ref at "
            f"positional index "
            f"{CONNECTOR_ENTITY_FIELDS.index('mou_task_ref')} is empty · "
            f"§5.2 M-C-1 mou_task_ref required."
        )
    return None


__all__ = [
    "CONNECTOR_ENTITY_ANCHOR",
    "CONNECTOR_ENTITY_FIELDS",
    "ConnectorEntity",
    "ConnectorEntityRefused",
    "EmptyScopeRefused",
    "MissingMouTaskRefRefused",
    "assert_connector_carrier_valid",
]
