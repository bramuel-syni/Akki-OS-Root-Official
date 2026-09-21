"""services.platform_control_plane.app_revalidation — CP-P5-CP3 · M9.

Pure assessment + preventive-charter refusal wrapper for app-
enablement revalidation per Akki OS Pilot Platform Reference v0.2
§9 M-Ac-2 verbatim:

    Enablement is validated against the tenant's connectors and
    compute integrations at enable time and re-validated when a
    connector is disabled or an integration goes offline; apps whose
    requirements lapse are marked degraded with the missing
    requirement named.

Composes with:
- CP-P5-CP1 AppEntity (required_connector_types +
  required_compute_classes).
- CP-P5-CP2 AppEnablement (status transitions to degraded).
- CP-P3-CP3 mode_rank (min-mode comparison).

Vocabulary:
- ENABLEMENT_STATUS = ("enabled", "degraded") · OPEN str · case-sensitive.

Refusals (on assessment record):
1. status not in ENABLEMENT_STATUS → UnknownEnablementStatusRefused
2. status == "degraded" AND missing_requirements empty →
   MissingRequirementNameRefused (§9 M-Ac-2 "with the missing
   requirement named")
3. status == "enabled" AND missing_requirements non-empty →
   InconsistentEnabledStatusRefused

Standing-line proof:
- Pure function · no side effects · deterministic sorted output.
- Zero closed enum type · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple

from services.platform_control_plane.connector_mode_lattice import (
    mode_rank as _mode_rank,
)


APP_REVALIDATION_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §9 "
    "M-Ac-2 verbatim: Enablement is validated against the tenant's "
    "connectors and compute integrations at enable time and re-"
    "validated when a connector is disabled or an integration goes "
    "offline; apps whose requirements lapse are marked degraded "
    "with the missing requirement named."
)


ENABLEMENT_STATUS: Tuple[str, ...] = (
    "enabled",
    "degraded",
)


@dataclasses.dataclass(frozen=True)
class EnablementHealthAssessment:
    """Frozen carrier for a revalidation assessment.

    Exact-order 2 fields:
    - status · OPEN str · one of ENABLEMENT_STATUS.
    - missing_requirements · sorted tuple of missing-requirement
      refs (empty when status == "enabled").

    Missing-requirement refs are canonical strings:
    - "connector_type:<type>" when a required connector type is
      not held.
    - "connector_mode:<type>:min=<mode>" when a required min-mode
      is not met.
    - "compute_class:<class>" when a required class is not
      healthy.
    """
    status: str
    missing_requirements: Tuple[str, ...]


class EnablementAssessmentRefused(Exception):
    """Root refusal for app-revalidation invariants."""


class UnknownEnablementStatusRefused(EnablementAssessmentRefused):
    """Refused: status not in ENABLEMENT_STATUS (case-sensitive)."""


class MissingRequirementNameRefused(EnablementAssessmentRefused):
    """Refused: degraded status without any named missing
    requirement (§9 M-Ac-2 "with the missing requirement named")."""


class InconsistentEnabledStatusRefused(EnablementAssessmentRefused):
    """Refused: enabled status carries named missing requirements —
    contradictory."""


def _find_held_mode(
    *,
    connector_type: str,
    tenant_connector_types_with_modes: Tuple[Tuple[str, str], ...],
) -> str:
    """Return the highest mode held for connector_type · empty
    string when not held."""
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


def assess_enablement_health(
    *,
    required_connector_types: Tuple[Tuple[str, str], ...],
    required_compute_classes: Tuple[str, ...],
    tenant_connector_types_with_modes_active: Tuple[Tuple[str, str], ...],
    tenant_compute_classes_healthy: Tuple[str, ...],
) -> EnablementHealthAssessment:
    """Pure re-validation computation per §9 M-Ac-2.

    Returns EnablementHealthAssessment where status is "enabled" iff
    every required connector type is held at min-mode-or-higher and
    every required compute_class is healthy; otherwise "degraded"
    with sorted missing-requirement refs.
    """
    missing = []
    held_types = frozenset(
        t for t, _ in tenant_connector_types_with_modes_active
    )
    for req_type, req_min_mode in required_connector_types:
        if req_type not in held_types:
            missing.append(f"connector_type:{req_type}")
            continue
        held_mode = _find_held_mode(
            connector_type=req_type,
            tenant_connector_types_with_modes=(
                tenant_connector_types_with_modes_active
            ),
        )
        if _mode_rank(mode=held_mode) < _mode_rank(mode=req_min_mode):
            missing.append(
                f"connector_mode:{req_type}:min={req_min_mode}"
            )
    held_classes = frozenset(tenant_compute_classes_healthy)
    for req_class in required_compute_classes:
        if req_class not in held_classes:
            missing.append(f"compute_class:{req_class}")
    if missing:
        return EnablementHealthAssessment(
            status="degraded",
            missing_requirements=tuple(sorted(missing)),
        )
    return EnablementHealthAssessment(
        status="enabled",
        missing_requirements=(),
    )


def assert_assessment_valid(
    *, assessment: EnablementHealthAssessment,
) -> None:
    """Preventive-charter refusal wrapper.

    Refusal order (fail fast):
    1. status not in ENABLEMENT_STATUS → UnknownEnablementStatusRefused.
    2. degraded + empty missing_requirements → MissingRequirementNameRefused.
    3. enabled + non-empty missing_requirements → InconsistentEnabledStatusRefused.

    Returns None on admit."""
    if assessment.status not in frozenset(ENABLEMENT_STATUS):
        raise UnknownEnablementStatusRefused(
            f"unknown-enablement-status refused: status not among "
            f"{len(ENABLEMENT_STATUS)} vocabulary values (case-sensitive)."
        )
    if (
        assessment.status == "degraded"
        and len(assessment.missing_requirements) == 0
    ):
        raise MissingRequirementNameRefused(
            f"missing-requirement-name refused: degraded assessment "
            f"has zero named missing requirements · §9 M-Ac-2."
        )
    if (
        assessment.status == "enabled"
        and len(assessment.missing_requirements) > 0
    ):
        raise InconsistentEnabledStatusRefused(
            f"inconsistent-enabled-status refused: enabled assessment "
            f"has {len(assessment.missing_requirements)} named missing "
            f"requirements."
        )
    return None


__all__ = [
    "APP_REVALIDATION_ANCHOR",
    "ENABLEMENT_STATUS",
    "EnablementHealthAssessment",
    "EnablementAssessmentRefused",
    "UnknownEnablementStatusRefused",
    "MissingRequirementNameRefused",
    "InconsistentEnabledStatusRefused",
    "assess_enablement_health",
    "assert_assessment_valid",
]
