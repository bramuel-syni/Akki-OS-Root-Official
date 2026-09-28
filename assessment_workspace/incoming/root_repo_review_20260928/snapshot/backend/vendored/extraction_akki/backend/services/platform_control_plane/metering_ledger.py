"""services.platform_control_plane.metering_ledger — CP-P4-CP7 · M9.

Metering-record carrier + reconciliation refusal wrapper per Akki OS
Pilot Platform Reference v0.2 §6.5 M-Cp-6 verbatim:

    Metering records GPU-seconds + CPU-seconds + RAM-seconds +
    bytes-read + bytes-written per tenant_id + compute_integration_id.
    Reconciliation invariant:
    sum(job_gpu_seconds per tenant per period) == allocation_ledger.

Carrier shape (9 fields · all OPEN str · numeric parsing is
CONTRACT-MODELED at caller consistent with CP-P4-CP2/CP6):
- id · tenant_id · compute_integration_id · period_ref
- gpu_seconds · cpu_seconds · ram_seconds · bytes_read · bytes_written

Refusals (fail-fast order):
1. any record.tenant_id != tenant_id → MeteringRecordWrongTenantRefused
2. any record.period_ref != period_ref → MeteringRecordWrongPeriodRefused
3. ledger_matches_sum_of_gpu_seconds False → MeteringReconciliationRefused

Standing-line proof:
- 9 str · 9 fields exact-order.
- Numeric reconciliation is CONTRACT-MODELED at caller (single
  boolean).
- Zero closed enum type · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


METERING_LEDGER_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §6.5 "
    "M-Cp-6 verbatim: Metering records GPU-seconds + CPU-seconds + "
    "RAM-seconds + bytes-read + bytes-written per tenant_id + "
    "compute_integration_id. Reconciliation invariant: "
    "sum(job_gpu_seconds per tenant per period) == allocation_ledger."
)


@dataclasses.dataclass(frozen=True)
class MeteringRecord:
    """Frozen carrier for a metering record per §6.5 M-Cp-6.

    Exact-order 9 str OPEN fields (numeric parsing CONTRACT-MODELED
    at caller per CP-P4-CP2 note):
    - id · metering record id.
    - tenant_id · owning tenant (ownership isolation index 1).
    - compute_integration_id · target compute integration
      (composes with CP-P4-CP1 ComputeIntegrationEntity.id).
    - period_ref · reconciliation period identifier.
    - gpu_seconds · OPEN str numeric-parse-at-caller.
    - cpu_seconds · OPEN str.
    - ram_seconds · OPEN str.
    - bytes_read · OPEN str.
    - bytes_written · OPEN str.
    """
    id: str
    tenant_id: str
    compute_integration_id: str
    period_ref: str
    gpu_seconds: str
    cpu_seconds: str
    ram_seconds: str
    bytes_read: str
    bytes_written: str


METERING_RECORD_FIELDS: Tuple[str, ...] = (
    "id",
    "tenant_id",
    "compute_integration_id",
    "period_ref",
    "gpu_seconds",
    "cpu_seconds",
    "ram_seconds",
    "bytes_read",
    "bytes_written",
)


class MeteringLedgerRefused(Exception):
    """Root refusal for metering-ledger invariants."""


class MeteringRecordWrongTenantRefused(MeteringLedgerRefused):
    """Refused: a record's tenant_id does not match the scoped
    tenant_id (§4.3 tenant-scoped ownership isolation)."""


class MeteringRecordWrongPeriodRefused(MeteringLedgerRefused):
    """Refused: a record's period_ref does not match the scoped
    period_ref (records must be filtered by period before
    reconciliation)."""


class MeteringReconciliationRefused(MeteringLedgerRefused):
    """Refused: sum(job_gpu_seconds per tenant per period) does not
    match allocation_ledger (§6.5 M-Cp-6 reconciliation invariant)."""


def assert_metering_ledger_reconciled(
    *,
    records: Tuple[MeteringRecord, ...],
    tenant_id: str,
    period_ref: str,
    ledger_matches_sum_of_gpu_seconds: bool,
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refusal order (fail fast):
    1. any record.tenant_id != tenant_id → MeteringRecordWrongTenantRefused.
    2. any record.period_ref != period_ref → MeteringRecordWrongPeriodRefused.
    3. ledger_matches_sum_of_gpu_seconds False → MeteringReconciliationRefused.

    ledger_matches_sum_of_gpu_seconds is CONTRACT-MODELED at caller
    (numeric sum + allocation_ledger comparison performed there per
    CP-P4-CP2 note).

    Returns None on admit."""
    for rec in records:
        if rec.tenant_id != tenant_id:
            raise MeteringRecordWrongTenantRefused(
                f"metering-record-wrong-tenant refused: record "
                f"tenant_id at positional index "
                f"{METERING_RECORD_FIELDS.index('tenant_id')} does "
                f"not match scoped tenant · §4.3 ownership isolation."
            )
    for rec in records:
        if rec.period_ref != period_ref:
            raise MeteringRecordWrongPeriodRefused(
                f"metering-record-wrong-period refused: record "
                f"period_ref at positional index "
                f"{METERING_RECORD_FIELDS.index('period_ref')} does "
                f"not match scoped period."
            )
    if not ledger_matches_sum_of_gpu_seconds:
        raise MeteringReconciliationRefused(
            f"metering-reconciliation refused: sum of {len(records)} "
            f"records' gpu_seconds does not match allocation_ledger "
            f"· §6.5 M-Cp-6."
        )
    return None


__all__ = [
    "METERING_LEDGER_ANCHOR",
    "METERING_RECORD_FIELDS",
    "MeteringRecord",
    "MeteringLedgerRefused",
    "MeteringRecordWrongTenantRefused",
    "MeteringRecordWrongPeriodRefused",
    "MeteringReconciliationRefused",
    "assert_metering_ledger_reconciled",
]
