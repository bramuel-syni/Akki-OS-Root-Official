"""services.platform_control_plane.scheduler_admission — CP-P4-CP6 · M9.

Preventive-charter scheduler-admission refusal wrapper per Akki OS
Pilot Platform Reference v0.2 §6.4:

    M-Cp-1: Every job names a compute_integration_id (an allocation
            or tenant-provided compute). Jobs without one are
            rejected at submission.
    M-Cp-2: The scheduler admits a job only if the named integration
            belongs to the job's tenant, has the class the job
            requires, and has capacity within its reservation, burst
            ceiling, hour budget and concurrency limit. Rejections
            state the reason.

Composes with:
- CP-P4-CP1 ComputeIntegrationEntity (integration.tenant_id +
  integration.class_ref).
- CP-P4-CP2 AllocationEntity (allocation.compute_integration_id +
  allocation.class_ref).

Numeric capacity comparison is CONTRACT-MODELED at caller (see
CP-P4-CP2 note): the caller computes 4 booleans indicating whether
current usage + this job stays within each limit and passes them
in as fixed gate parameters.

Refusals (fail-fast order per M-Cp-2 "Rejections state the reason"):
1. job_compute_integration_id empty → MissingComputeIntegrationIdRefused (M-Cp-1)
2. integration.tenant_id != job_tenant_id → WrongTenantRefused (M-Cp-2)
3. integration.class_ref != job_class_ref → WrongClassRefused (M-Cp-2)
4. usage_within_reservation False → ExceedsReservationRefused (M-Cp-2)
5. usage_within_burst_ceiling False → ExceedsBurstCeilingRefused (M-Cp-2)
6. usage_within_hour_budget False → ExceedsHourBudgetRefused (M-Cp-2)
7. usage_within_concurrency_limit False → ExceedsConcurrencyLimitRefused (M-Cp-2)

Standing-line proof:
- Pure function · no side effects · caller composes.
- Zero closed enum type · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

# Composition with CP-P4-CP1 ComputeIntegrationEntity + CP-P4-CP2
# AllocationEntity (control-plane peers · not data-plane imports).
from services.platform_control_plane.compute_integration import (
    ComputeIntegrationEntity as _ComputeIntegrationEntity,
)
from services.platform_control_plane.allocation_entity import (
    AllocationEntity as _AllocationEntity,
)


SCHEDULER_ADMISSION_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §6.4 "
    "M-Cp-1 verbatim: Every job names a compute_integration_id "
    "(an allocation or tenant-provided compute). Jobs without one "
    "are rejected at submission. §6.4 M-Cp-2 verbatim: The "
    "scheduler admits a job only if the named integration belongs "
    "to the job's tenant, has the class the job requires, and has "
    "capacity within its reservation, burst ceiling, hour budget "
    "and concurrency limit. Rejections state the reason."
)


class SchedulerAdmissionRefused(Exception):
    """Root refusal for scheduler-admission invariants."""


class MissingComputeIntegrationIdRefused(SchedulerAdmissionRefused):
    """Refused: job did not name a compute_integration_id (M-Cp-1)."""


class WrongTenantRefused(SchedulerAdmissionRefused):
    """Refused: integration.tenant_id != job_tenant_id (M-Cp-2
    'belongs to the job's tenant')."""


class WrongClassRefused(SchedulerAdmissionRefused):
    """Refused: integration.class_ref != job_class_ref (M-Cp-2
    'has the class the job requires')."""


class ExceedsReservationRefused(SchedulerAdmissionRefused):
    """Refused: usage_within_reservation is False (M-Cp-2)."""


class ExceedsBurstCeilingRefused(SchedulerAdmissionRefused):
    """Refused: usage_within_burst_ceiling is False (M-Cp-2)."""


class ExceedsHourBudgetRefused(SchedulerAdmissionRefused):
    """Refused: usage_within_hour_budget is False (M-Cp-2)."""


class ExceedsConcurrencyLimitRefused(SchedulerAdmissionRefused):
    """Refused: usage_within_concurrency_limit is False (M-Cp-2)."""


def assert_scheduler_admits(
    *,
    job_compute_integration_id: str,
    job_tenant_id: str,
    job_class_ref: str,
    integration: _ComputeIntegrationEntity,
    allocation: _AllocationEntity,
    usage_within_reservation: bool,
    usage_within_burst_ceiling: bool,
    usage_within_hour_budget: bool,
    usage_within_concurrency_limit: bool,
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refusal order (fail fast · M-Cp-2 'Rejections state the reason'):
    1. job_compute_integration_id empty → MissingComputeIntegrationIdRefused (M-Cp-1).
    2. integration.tenant_id != job_tenant_id → WrongTenantRefused.
    3. integration.class_ref != job_class_ref → WrongClassRefused.
    4. usage_within_reservation False → ExceedsReservationRefused.
    5. usage_within_burst_ceiling False → ExceedsBurstCeilingRefused.
    6. usage_within_hour_budget False → ExceedsHourBudgetRefused.
    7. usage_within_concurrency_limit False → ExceedsConcurrencyLimitRefused.

    Numeric capacity comparisons are CONTRACT-MODELED at caller
    (4 pre-computed booleans). allocation parameter is retained in
    the signature to compose reservation/burst/hours/concurrency
    identity refs at caller-side receipt time.

    Returns None on admit."""
    _ = allocation  # composition anchor · caller composes numerics
    if job_compute_integration_id == "":
        raise MissingComputeIntegrationIdRefused(
            f"missing-compute-integration-id refused: job did not "
            f"name a compute_integration_id · §6.4 M-Cp-1."
        )
    if integration.tenant_id != job_tenant_id:
        raise WrongTenantRefused(
            f"wrong-tenant refused: integration.tenant_id does not "
            f"match job_tenant_id · §6.4 M-Cp-2."
        )
    if integration.class_ref != job_class_ref:
        raise WrongClassRefused(
            f"wrong-class refused: integration.class_ref does not "
            f"match job_class_ref · §6.4 M-Cp-2."
        )
    if not usage_within_reservation:
        raise ExceedsReservationRefused(
            f"exceeds-reservation refused · §6.4 M-Cp-2."
        )
    if not usage_within_burst_ceiling:
        raise ExceedsBurstCeilingRefused(
            f"exceeds-burst-ceiling refused · §6.4 M-Cp-2."
        )
    if not usage_within_hour_budget:
        raise ExceedsHourBudgetRefused(
            f"exceeds-hour-budget refused · §6.4 M-Cp-2."
        )
    if not usage_within_concurrency_limit:
        raise ExceedsConcurrencyLimitRefused(
            f"exceeds-concurrency-limit refused · §6.4 M-Cp-2."
        )
    return None


__all__ = [
    "SCHEDULER_ADMISSION_ANCHOR",
    "SchedulerAdmissionRefused",
    "MissingComputeIntegrationIdRefused",
    "WrongTenantRefused",
    "WrongClassRefused",
    "ExceedsReservationRefused",
    "ExceedsBurstCeilingRefused",
    "ExceedsHourBudgetRefused",
    "ExceedsConcurrencyLimitRefused",
    "assert_scheduler_admits",
]
