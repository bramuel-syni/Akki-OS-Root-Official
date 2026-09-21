"""services.platform_control_plane.cross_tenant_access_suite — CP-P6-CP3 · M9.

Refusal aggregator per Akki OS Pilot Platform Reference v0.2 Row 208:

    Joins tenant_context, task_scope, permission_evaluation,
    scheduler_admission, metering, audit visibility.

§6 acceptance criterion 2 verbatim: Cross-tenant access suite passes
— no request/job/queue/storage/log/metric can reach another tenant.

This CP is a meta-refusal wrapper that shape-freezes the composed
cross-tenant acceptance suite. Each named gate is a pre-computed
boolean from its owning CP:

- tenant_context_ok · CP-P1-CP1 tenant_context (verdict from
  assert_tenant_context_valid).
- task_scope_ok · CP-P4-CP4 task_scope_enforcement (verdict from
  assert_job_connector_admissible over all task connectors).
- permission_evaluation_ok · CP-P2-CP3 permission_evaluation
  (verdict==allow from assess_permission_grant).
- scheduler_admission_ok · CP-P4-CP6 scheduler_admission (verdict
  from assert_scheduler_admits).
- metering_ok · CP-P4-CP7 metering_ledger (verdict from
  assert_metering_ledger_reconciled).
- audit_visibility_ok · CP-P6-CP1 audit_event visibility invariant
  (verdict from caller-side tenant-scoping of audit_event reads).

Refusals (fail-fast order):
1. tenant_context_ok False → CrossTenantContextViolationRefused
2. task_scope_ok False → CrossTenantTaskScopeViolationRefused
3. permission_evaluation_ok False → CrossTenantPermissionViolationRefused
4. scheduler_admission_ok False → CrossTenantSchedulerViolationRefused
5. metering_ok False → CrossTenantMeteringViolationRefused
6. audit_visibility_ok False → CrossTenantAuditVisibilityViolationRefused

Standing-line proof:
- Pure function · no side effects · caller composes.
- Zero closed enum type · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

from typing import Tuple


CROSS_TENANT_ACCESS_SUITE_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) Row "
    "208: Refusal aggregator joins tenant_context, task_scope, "
    "permission_evaluation, scheduler_admission, metering, audit "
    "visibility (canonical planes: tenant_context, task_scope, "
    "permission_evaluation, scheduler_admission, metering, "
    "audit_visibility). §6 acceptance criterion 2 verbatim: "
    "Cross-tenant access suite passes — no request/job/queue/"
    "storage/log/metric can reach another tenant."
)


# Suite plane names in refusal order.
CROSS_TENANT_SUITE_PLANES: Tuple[str, ...] = (
    "tenant_context",
    "task_scope",
    "permission_evaluation",
    "scheduler_admission",
    "metering",
    "audit_visibility",
)


class CrossTenantAccessSuiteRefused(Exception):
    """Root refusal for cross-tenant access suite invariants."""


class CrossTenantContextViolationRefused(CrossTenantAccessSuiteRefused):
    """Refused: CP-P1-CP1 tenant_context gate reports violation."""


class CrossTenantTaskScopeViolationRefused(CrossTenantAccessSuiteRefused):
    """Refused: CP-P4-CP4 task_scope gate reports violation."""


class CrossTenantPermissionViolationRefused(CrossTenantAccessSuiteRefused):
    """Refused: CP-P2-CP3 permission_evaluation gate reports deny."""


class CrossTenantSchedulerViolationRefused(CrossTenantAccessSuiteRefused):
    """Refused: CP-P4-CP6 scheduler_admission gate reports violation."""


class CrossTenantMeteringViolationRefused(CrossTenantAccessSuiteRefused):
    """Refused: CP-P4-CP7 metering_ledger gate reports violation."""


class CrossTenantAuditVisibilityViolationRefused(CrossTenantAccessSuiteRefused):
    """Refused: CP-P6-CP1 audit_event visibility gate reports
    cross-tenant leakage."""


def assert_cross_tenant_suite_admits(
    *,
    tenant_context_ok: bool,
    task_scope_ok: bool,
    permission_evaluation_ok: bool,
    scheduler_admission_ok: bool,
    metering_ok: bool,
    audit_visibility_ok: bool,
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Fires the first False gate as its named subclass. Each boolean
    is a pre-computed verdict from the owning CP. Returns None on
    admit (all six gates True).
    """
    if not tenant_context_ok:
        raise CrossTenantContextViolationRefused(
            f"cross-tenant-context-violation refused: CP-P1-CP1 "
            f"tenant_context gate report=False."
        )
    if not task_scope_ok:
        raise CrossTenantTaskScopeViolationRefused(
            f"cross-tenant-task-scope-violation refused: CP-P4-CP4 "
            f"task_scope gate report=False."
        )
    if not permission_evaluation_ok:
        raise CrossTenantPermissionViolationRefused(
            f"cross-tenant-permission-violation refused: CP-P2-CP3 "
            f"permission_evaluation gate report=False."
        )
    if not scheduler_admission_ok:
        raise CrossTenantSchedulerViolationRefused(
            f"cross-tenant-scheduler-violation refused: CP-P4-CP6 "
            f"scheduler_admission gate report=False."
        )
    if not metering_ok:
        raise CrossTenantMeteringViolationRefused(
            f"cross-tenant-metering-violation refused: CP-P4-CP7 "
            f"metering_ledger gate report=False."
        )
    if not audit_visibility_ok:
        raise CrossTenantAuditVisibilityViolationRefused(
            f"cross-tenant-audit-visibility-violation refused: "
            f"CP-P6-CP1 audit_event visibility gate report=False."
        )
    return None


__all__ = [
    "CROSS_TENANT_ACCESS_SUITE_ANCHOR",
    "CROSS_TENANT_SUITE_PLANES",
    "CrossTenantAccessSuiteRefused",
    "CrossTenantContextViolationRefused",
    "CrossTenantTaskScopeViolationRefused",
    "CrossTenantPermissionViolationRefused",
    "CrossTenantSchedulerViolationRefused",
    "CrossTenantMeteringViolationRefused",
    "CrossTenantAuditVisibilityViolationRefused",
    "assert_cross_tenant_suite_admits",
]
