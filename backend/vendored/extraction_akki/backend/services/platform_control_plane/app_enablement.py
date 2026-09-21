"""services.platform_control_plane.app_enablement — CP-P5-CP2 · M9.

Frozen carrier + preventive-charter enablement-admission refusal
wrapper per Akki OS Pilot Platform Reference v0.2:

- §10 verbatim: app_enablement (id, tenant_id, app_id, status,
  enabled_by, enabled_at)
- §9 M-Ac-1 verbatim: required_connector_types (with min-mode per
  type), required_compute_classes.
- §9 M-Ac-2 verbatim: Enablement is validated against the tenant's
  connectors and compute integrations at enable time.
- §6.6 M-Cp-7 verbatim: Enabling an app for a tenant requires the
  tenant hold at least one healthy integration of each required
  compute class.

Refusals (fail-fast order):
1. required connector_type not held → MissingRequiredConnectorTypeRefused
2. held connector mode below required min_mode →
   InsufficientConnectorModeRefused
3. required compute_class not held healthy →
   MissingRequiredComputeClassRefused

Composes with CP-P3-CP3 mode_rank + UnknownModeRefused (bubbled).

Standing-line proof:
- 6 str · 6 fields exact-order.
- Zero closed enum type · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple

from services.platform_control_plane.connector_mode_lattice import (
    mode_rank as _mode_rank,
)


APP_ENABLEMENT_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §10 "
    "verbatim: app_enablement (id, tenant_id, app_id, status, "
    "enabled_by, enabled_at). §9 M-Ac-2 verbatim: Enablement is "
    "validated against the tenant's connectors and compute "
    "integrations at enable time. §6.6 M-Cp-7 verbatim: Enabling an "
    "app for a tenant requires the tenant hold at least one healthy "
    "integration of each required compute class."
)


@dataclasses.dataclass(frozen=True)
class AppEnablement:
    """Frozen carrier for the control-plane app_enablement record.

    Exact-order 6 str OPEN fields:
    - id · enablement record id.
    - tenant_id · owning tenant (ownership isolation index 1).
    - app_id · target app (composes with CP-P5-CP1 AppEntity.id).
    - status · lifecycle status (OPEN str · e.g., enabled, degraded,
      disabled).
    - enabled_by · user_id ref.
    - enabled_at · ISO-8601 UTC 'Z' str.
    """
    id: str
    tenant_id: str
    app_id: str
    status: str
    enabled_by: str
    enabled_at: str


APP_ENABLEMENT_FIELDS: Tuple[str, ...] = (
    "id",
    "tenant_id",
    "app_id",
    "status",
    "enabled_by",
    "enabled_at",
)


class AppEnablementRefused(Exception):
    """Root refusal for app-enablement invariants."""


class MissingRequiredConnectorTypeRefused(AppEnablementRefused):
    """Refused: tenant does not hold a required connector type
    (§9 M-Ac-2)."""


class InsufficientConnectorModeRefused(AppEnablementRefused):
    """Refused: tenant's held connector mode is below the required
    min_mode for that type (§9 M-Ac-1 "with min-mode per type")."""


class MissingRequiredComputeClassRefused(AppEnablementRefused):
    """Refused: tenant does not hold at least one healthy integration
    of a required compute class (§6.6 M-Cp-7)."""


def _find_held_mode(
    *,
    connector_type: str,
    tenant_connector_types_with_modes: Tuple[Tuple[str, str], ...],
) -> str:
    """Return the highest mode held for connector_type across the
    tenant's integrations, or empty string when not held."""
    best_rank = -1
    best_mode = ""
    for held_type, held_mode in tenant_connector_types_with_modes:
        if held_type != connector_type:
            continue
        r = _mode_rank(mode=held_mode)
        if r > best_rank:
            best_rank = r
            best_mode = held_mode
    return best_mode


def assert_app_enablement_admissible(
    *,
    required_connector_types: Tuple[Tuple[str, str], ...],
    required_compute_classes: Tuple[str, ...],
    tenant_connector_types_with_modes: Tuple[Tuple[str, str], ...],
    tenant_compute_classes_healthy: Tuple[str, ...],
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refusal order (fail fast):
    1. Any required connector_type not among tenant's held types →
       MissingRequiredConnectorTypeRefused (§9 M-Ac-2).
    2. Held connector mode rank below required min_mode rank →
       InsufficientConnectorModeRefused (§9 M-Ac-1).
    3. Any required compute_class not among tenant's healthy
       compute_classes → MissingRequiredComputeClassRefused (§6.6
       M-Cp-7).

    Mode-rank comparisons compose CP-P3-CP3 mode_rank.

    Returns None on admit."""
    held_types = frozenset(t for t, _ in tenant_connector_types_with_modes)
    for req_type, req_min_mode in required_connector_types:
        if req_type not in held_types:
            raise MissingRequiredConnectorTypeRefused(
                f"missing-required-connector-type refused: required "
                f"type not among {len(held_types)} held types · "
                f"§9 M-Ac-2."
            )
    for req_type, req_min_mode in required_connector_types:
        held_mode = _find_held_mode(
            connector_type=req_type,
            tenant_connector_types_with_modes=(
                tenant_connector_types_with_modes
            ),
        )
        # held_mode is non-empty because the previous loop admitted;
        # bubble UnknownModeRefused on invalid mode inputs.
        if _mode_rank(mode=held_mode) < _mode_rank(mode=req_min_mode):
            raise InsufficientConnectorModeRefused(
                f"insufficient-connector-mode refused: held mode "
                f"rank below required min_mode rank · §9 M-Ac-1."
            )
    held_classes = frozenset(tenant_compute_classes_healthy)
    for req_class in required_compute_classes:
        if req_class not in held_classes:
            raise MissingRequiredComputeClassRefused(
                f"missing-required-compute-class refused: required "
                f"class not among {len(held_classes)} healthy "
                f"classes · §6.6 M-Cp-7."
            )
    return None


__all__ = [
    "APP_ENABLEMENT_ANCHOR",
    "APP_ENABLEMENT_FIELDS",
    "AppEnablement",
    "AppEnablementRefused",
    "MissingRequiredConnectorTypeRefused",
    "InsufficientConnectorModeRefused",
    "MissingRequiredComputeClassRefused",
    "assert_app_enablement_admissible",
]
