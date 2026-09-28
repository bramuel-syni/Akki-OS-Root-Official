"""services.platform_control_plane.allocation_entity — CP-P4-CP2 · M9.

Pure frozen carrier for control-plane allocation record per Akki OS
Pilot Platform Reference v0.2 §10 verbatim:

    allocation (id, tenant_id, compute_integration_id, class,
                reserved, burst_ceiling, hours_per_period,
                max_concurrent_jobs, environment, granted_by,
                granted_at, expires_at)

Environment vocabulary (§4.4 + §10 environment field): OPEN str
{sandbox, production}.

§6.4 anchors:
- M-Cp-1: Every job names a compute_integration_id.
- M-Cp-2: Scheduler admits iff the named integration belongs to the
  job's tenant, has the class the job requires, and has capacity
  within its reservation, burst ceiling, hour budget and concurrency
  limit — enforced downstream at CP-P4-CP6 SCHEDULER-ADMISSION;
  reserved/burst_ceiling/hours_per_period/max_concurrent_jobs
  surfaced as OPEN str for numeric parsing at caller.

Python keyword note: §10 field `class` → dataclass attribute
`class_ref` (Python-safe shim, index-aligned in the SPEC_VERBATIM
tuple). Same convention as CP-P4-CP1.

Refusals:
- environment not in ALLOCATION_ENVIRONMENTS → UnknownAllocationEnvironmentRefused

Standing-line proof:
- 12 str · 12 fields exact-order.
- No enforcement hard-gate · caller composes.
- Zero closed enum type · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


ALLOCATION_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §10 "
    "verbatim: allocation (id, tenant_id, compute_integration_id, "
    "class, reserved, burst_ceiling, hours_per_period, "
    "max_concurrent_jobs, environment, granted_by, granted_at, "
    "expires_at). §4.4 + §10 environment ∈ {sandbox, production}. "
    "§6.4 M-Cp-2: scheduler admits iff tenant + class + capacity + "
    "reservation + burst + hours + concurrency."
)


# §4.4 + §10 environment vocabulary · OPEN str · case-sensitive.
ALLOCATION_ENVIRONMENTS: Tuple[str, ...] = (
    "sandbox",
    "production",
)


@dataclasses.dataclass(frozen=True)
class AllocationEntity:
    """Frozen carrier for the control-plane allocation record.

    Exact-order 12 str OPEN fields (Python-safe · §10 `class` →
    `class_ref` shim documented in module docstring):
    - id · allocation record id.
    - tenant_id · owning tenant (ownership isolation index 1).
    - compute_integration_id · target compute integration
      (composes with CP-P4-CP1 ComputeIntegrationEntity).
    - class_ref · compute-class this allocation is granted for
      (§10 `class` verbatim · OPEN str · Python-keyword shim).
    - reserved · reserved capacity descriptor (OPEN str; numeric
      parse is CONTRACT-MODELED at CP-P4-CP6 SCHEDULER-ADMISSION).
    - burst_ceiling · burst ceiling descriptor (OPEN str).
    - hours_per_period · hour budget descriptor (OPEN str).
    - max_concurrent_jobs · concurrency ceiling descriptor
      (OPEN str).
    - environment · §4.4 + §10 vocabulary (sandbox | production).
    - granted_by · user_id ref of granter.
    - granted_at · ISO-8601 UTC 'Z' str.
    - expires_at · ISO-8601 UTC 'Z' str.
    """
    id: str
    tenant_id: str
    compute_integration_id: str
    class_ref: str
    reserved: str
    burst_ceiling: str
    hours_per_period: str
    max_concurrent_jobs: str
    environment: str
    granted_by: str
    granted_at: str
    expires_at: str


ALLOCATION_ENTITY_FIELDS: Tuple[str, ...] = (
    "id",
    "tenant_id",
    "compute_integration_id",
    "class_ref",
    "reserved",
    "burst_ceiling",
    "hours_per_period",
    "max_concurrent_jobs",
    "environment",
    "granted_by",
    "granted_at",
    "expires_at",
)


# §10 verbatim field names (with `class` keyword · reference only).
ALLOCATION_ENTITY_FIELDS_SPEC_VERBATIM: Tuple[str, ...] = (
    "id",
    "tenant_id",
    "compute_integration_id",
    "class",
    "reserved",
    "burst_ceiling",
    "hours_per_period",
    "max_concurrent_jobs",
    "environment",
    "granted_by",
    "granted_at",
    "expires_at",
)


class AllocationEntityRefused(Exception):
    """Root refusal for allocation-entity invariants."""


class UnknownAllocationEnvironmentRefused(AllocationEntityRefused):
    """Refused: environment not in ALLOCATION_ENVIRONMENTS
    (case-sensitive). §4.4 + §10 verbatim: environment ∈
    {sandbox, production}."""


def assert_allocation_environment_valid(
    *, entity: AllocationEntity,
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refuses UnknownAllocationEnvironmentRefused when
    entity.environment not in ALLOCATION_ENVIRONMENTS
    (case-sensitive).

    Returns None on admit."""
    if entity.environment not in frozenset(ALLOCATION_ENVIRONMENTS):
        raise UnknownAllocationEnvironmentRefused(
            f"unknown-environment refused: environment not among "
            f"{len(ALLOCATION_ENVIRONMENTS)} §4.4 environments "
            f"(case-sensitive)."
        )
    return None


__all__ = [
    "ALLOCATION_ANCHOR",
    "ALLOCATION_ENVIRONMENTS",
    "ALLOCATION_ENTITY_FIELDS",
    "ALLOCATION_ENTITY_FIELDS_SPEC_VERBATIM",
    "AllocationEntity",
    "AllocationEntityRefused",
    "UnknownAllocationEnvironmentRefused",
    "assert_allocation_environment_valid",
]
