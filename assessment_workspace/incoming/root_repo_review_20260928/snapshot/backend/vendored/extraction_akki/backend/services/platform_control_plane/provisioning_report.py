"""services.platform_control_plane.provisioning_report — CP-P5-CP5 · M9.

Provisioning-report carrier + preventive-charter refusal wrapper
per Akki OS Pilot Platform Reference v0.2 §8.1 M-W-1:

    Wizard produces a provisioned sandbox tenant and a provisioning
    report.

Row 200 anchor: Refusal on missing sub-list (estates / connectors /
compute / apps / workspaces / users) or missing mou_task_ref
reconciliation.

Sub-lists (§8 wizard step outputs · §10 entity refs):
- estates_refs · connectors_refs · compute_integrations_refs
- apps_refs · workspaces_refs · users_refs

MoU-task-ref reconciliation: connectors carry mou_task_ref (CP-P3-CP2
§10 connector field) which must align with the tenant's provisioned
MoU set (mou_task_refs_expected). Reconciliation fails when the
observed set != expected set.

Refusals (fail-fast order):
1. any of the 6 sub-lists is empty → MissingSubListRefused
   (order: estates → connectors → compute → apps → workspaces →
   users).
2. mou_task_refs_reconciled tuple sorted != mou_task_refs_expected
   sorted → MouTaskRefReconciliationRefused.

Standing-line proof:
- 2 str + 8 tuple[str, ...] · 10 fields exact-order.
- Zero closed enum type · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


PROVISIONING_REPORT_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §8.1 "
    "M-W-1 verbatim: Wizard produces a provisioned sandbox tenant "
    "and a provisioning report. Row 200: Refusal on missing "
    "sub-list (estates / connectors / compute / apps / workspaces / "
    "users) or missing mou_task_ref reconciliation."
)


# §8/§10-verbatim ordered sub-list names.
PROVISIONING_REPORT_SUBLISTS: Tuple[str, ...] = (
    "estates",
    "connectors",
    "compute",
    "apps",
    "workspaces",
    "users",
)


@dataclasses.dataclass(frozen=True)
class ProvisioningReport:
    """Frozen carrier for a wizard provisioning report.

    Exact-order 10 fields (2 str + 8 tuple[str, ...]):
    - id · report record id.
    - tenant_id · owning tenant (ownership isolation index 1).
    - estates_refs · tuple of estate id refs (must have >= 1).
    - connectors_refs · tuple of connector id refs (>= 1).
    - compute_integrations_refs · tuple of ci id refs (>= 1).
    - apps_refs · tuple of app_enablement id refs (>= 1).
    - workspaces_refs · tuple of workspace id refs (>= 1).
    - users_refs · tuple of user id refs (>= 1).
    - mou_task_refs_expected · tuple of MoU task refs expected
      to be reconciled by connectors.
    - mou_task_refs_reconciled · tuple of MoU task refs actually
      reconciled (must equal expected as sorted set).
    """
    id: str
    tenant_id: str
    estates_refs: Tuple[str, ...]
    connectors_refs: Tuple[str, ...]
    compute_integrations_refs: Tuple[str, ...]
    apps_refs: Tuple[str, ...]
    workspaces_refs: Tuple[str, ...]
    users_refs: Tuple[str, ...]
    mou_task_refs_expected: Tuple[str, ...]
    mou_task_refs_reconciled: Tuple[str, ...]


PROVISIONING_REPORT_FIELDS: Tuple[str, ...] = (
    "id",
    "tenant_id",
    "estates_refs",
    "connectors_refs",
    "compute_integrations_refs",
    "apps_refs",
    "workspaces_refs",
    "users_refs",
    "mou_task_refs_expected",
    "mou_task_refs_reconciled",
)


class ProvisioningReportRefused(Exception):
    """Root refusal for provisioning-report invariants."""


class MissingSubListRefused(ProvisioningReportRefused):
    """Refused: at least one required sub-list is empty (Row 200)."""


class MouTaskRefReconciliationRefused(ProvisioningReportRefused):
    """Refused: mou_task_refs_reconciled does not equal
    mou_task_refs_expected as sorted set (Row 200)."""


def assert_provisioning_report_valid(
    *, report: ProvisioningReport,
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refusal order (fail-fast per sub-list order):
    1. estates_refs empty → MissingSubListRefused.
    2. connectors_refs empty → MissingSubListRefused.
    3. compute_integrations_refs empty → MissingSubListRefused.
    4. apps_refs empty → MissingSubListRefused.
    5. workspaces_refs empty → MissingSubListRefused.
    6. users_refs empty → MissingSubListRefused.
    7. sorted(mou_task_refs_reconciled) != sorted(mou_task_refs_expected)
       → MouTaskRefReconciliationRefused.

    Returns None on admit."""
    sublist_pairs = (
        ("estates", report.estates_refs),
        ("connectors", report.connectors_refs),
        ("compute", report.compute_integrations_refs),
        ("apps", report.apps_refs),
        ("workspaces", report.workspaces_refs),
        ("users", report.users_refs),
    )
    for name, refs in sublist_pairs:
        if len(refs) == 0:
            raise MissingSubListRefused(
                f"missing-sub-list refused: sub-list at position "
                f"{PROVISIONING_REPORT_SUBLISTS.index(name)} is "
                f"empty · Row 200."
            )
    if tuple(sorted(report.mou_task_refs_reconciled)) != tuple(
        sorted(report.mou_task_refs_expected)
    ):
        raise MouTaskRefReconciliationRefused(
            f"mou-task-ref-reconciliation refused: "
            f"{len(report.mou_task_refs_reconciled)} reconciled "
            f"refs vs {len(report.mou_task_refs_expected)} expected "
            f"· Row 200."
        )
    return None


__all__ = [
    "PROVISIONING_REPORT_ANCHOR",
    "PROVISIONING_REPORT_SUBLISTS",
    "PROVISIONING_REPORT_FIELDS",
    "ProvisioningReport",
    "ProvisioningReportRefused",
    "MissingSubListRefused",
    "MouTaskRefReconciliationRefused",
    "assert_provisioning_report_valid",
]
