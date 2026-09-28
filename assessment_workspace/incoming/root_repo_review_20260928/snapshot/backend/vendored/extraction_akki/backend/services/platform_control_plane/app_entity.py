"""services.platform_control_plane.app_entity — CP-P5-CP1 · M9.

Pure frozen carrier for the control-plane app record per Akki OS
Pilot Platform Reference v0.2 §10 verbatim:

    app (id, name, version, required_connector_types,
         required_compute_classes, run_roles, view_roles,
         availability)

§9 M-Ac-1 anchor: required_connector_types carries min-mode per
type (tuple of (connector_type, min_mode) OPEN pairs).
required_compute_classes, run_roles, view_roles are OPEN str
tuples.

Pure carrier · no refusal wrapper · caller composes downstream
validation (CP-P5-CP2 APP-ENABLEMENT, CP-P5-CP3 revalidation).

Standing-line proof:
- 4 str + 4 tuple[str,...] variants · 8 fields exact-order.
- Zero closed enum type · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


APP_ENTITY_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §10 "
    "verbatim: app (id, name, version, required_connector_types, "
    "required_compute_classes, run_roles, view_roles, availability). "
    "§9 M-Ac-1 anchor: required_connector_types carries min-mode "
    "per type."
)


@dataclasses.dataclass(frozen=True)
class AppEntity:
    """Frozen carrier for the control-plane app record.

    Exact-order 8 fields:
    - id · str · app record id.
    - name · str · human-readable name (OPEN).
    - version · str · version string (OPEN).
    - required_connector_types · tuple of (connector_type, min_mode)
      OPEN pairs per §9 M-Ac-1.
    - required_compute_classes · tuple of class_ref OPEN str.
    - run_roles · tuple of role_ref OPEN str (composes with
      CP-P2-CP1 PLATFORM_ROLES).
    - view_roles · tuple of role_ref OPEN str.
    - availability · OPEN str (e.g., "public", "private", "beta").
    """
    id: str
    name: str
    version: str
    required_connector_types: Tuple[Tuple[str, str], ...]
    required_compute_classes: Tuple[str, ...]
    run_roles: Tuple[str, ...]
    view_roles: Tuple[str, ...]
    availability: str


APP_ENTITY_FIELDS: Tuple[str, ...] = (
    "id",
    "name",
    "version",
    "required_connector_types",
    "required_compute_classes",
    "run_roles",
    "view_roles",
    "availability",
)


__all__ = [
    "APP_ENTITY_ANCHOR",
    "APP_ENTITY_FIELDS",
    "AppEntity",
]
