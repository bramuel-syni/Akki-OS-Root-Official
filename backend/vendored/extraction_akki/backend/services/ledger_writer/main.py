"""services/ledger_writer/main.py · M10-W2 · single-writer hash chain appender.

Canon anchors (verbatim):
  v1.0 B.4 · Ledger single-writer discipline · every row hash-chained.
  Canon 3 §9.3 · append-only · BR-15.
  BR-13/BR-14 · row shape rules.

Deterministic hash chain:
  hash_n = SHA256(prev_hash_n || canonical_row_bytes(row_n))
  hash_0 = SHA256("0"*64 || canonical_row_bytes(row_0))    # genesis

Per-tenant seq monotone increasing from 1.  seq=1 is genesis row.
"""
from __future__ import annotations

import hashlib
from typing import Any, Dict, Mapping

from contracts.ledger_v1 import (
    GENESIS_PREV_HASH,
    LEDGER_SCHEMA_VERSION,
    LedgerRow,
    canonical_row_bytes,
)
from services.ledger_emitter.emit_intent import LedgerIntent


class LedgerWriterRefusalError(Exception):
    """Root of ledger-writer refusals."""
    code: str = ""


class OutOfOrderSeqRefused(LedgerWriterRefusalError):
    """LEDGER-WRITER-001 · seq out of monotone order for this tenant."""
    code: str = "LEDGER-WRITER-001"


class InsertOnlyViolation(LedgerWriterRefusalError):
    """LEDGER-WRITER-002 · attempted non-insert operation."""
    code: str = "LEDGER-WRITER-002"


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compute_row_hash(prev_hash: str, row_without_hash: LedgerRow) -> str:
    """Deterministic: sha256(prev_hash || canonical(row_without_hash))."""
    body = canonical_row_bytes(row_without_hash)
    return _sha256_hex(prev_hash.encode() + body)


def append_intent(
    *, intent: LedgerIntent, prev_row: LedgerRow | None, tenant_seq_next: int
) -> LedgerRow:
    """Append a LedgerIntent to the per-tenant chain.

    Args:
        intent: caller-supplied intent (produced by emit_intent).
        prev_row: the previous LedgerRow for this tenant, or None for genesis.
        tenant_seq_next: the next monotone seq for this tenant (>=1).

    Raises:
        OutOfOrderSeqRefused if tenant_seq_next != prev_seq + 1 (or != 1 at genesis).
    """
    if prev_row is None:
        # Genesis case
        if tenant_seq_next != 1:
            raise OutOfOrderSeqRefused(
                f"LEDGER-WRITER-001: genesis requires seq=1, got {tenant_seq_next}"
            )
        prev_hash = GENESIS_PREV_HASH
    else:
        if tenant_seq_next != prev_row.seq + 1:
            raise OutOfOrderSeqRefused(
                f"LEDGER-WRITER-001: expected seq {prev_row.seq + 1}, got {tenant_seq_next}"
            )
        if prev_row.tenant_id != intent.tenant_id:
            raise OutOfOrderSeqRefused(
                "LEDGER-WRITER-001: tenant chain crossed (counts mismatch: 1)"
            )
        prev_hash = prev_row.hash

    # Build row without hash so we can hash over its canonical form
    tentative = LedgerRow(
        seq=tenant_seq_next,
        prev_hash=prev_hash,
        hash="",
        schema_version=LEDGER_SCHEMA_VERSION,
        tenant_id=intent.tenant_id,
        run_id=intent.run_id,
        task_id=intent.task_id,
        actor_id=intent.actor_id,
        actor_type=intent.actor_type,
        event_type=intent.event_type,
        resource_type=intent.resource_type,
        resource_id=intent.resource_id,
        decision=intent.decision,
        reason_code=intent.reason_code,
        payload_ref=intent.payload_ref,
        at=intent.at,
        break_glass_session_id=intent.break_glass_session_id,
    )
    row_hash = compute_row_hash(prev_hash, tentative)
    return LedgerRow(
        seq=tentative.seq,
        prev_hash=tentative.prev_hash,
        hash=row_hash,
        schema_version=tentative.schema_version,
        tenant_id=tentative.tenant_id,
        run_id=tentative.run_id,
        task_id=tentative.task_id,
        actor_id=tentative.actor_id,
        actor_type=tentative.actor_type,
        event_type=tentative.event_type,
        resource_type=tentative.resource_type,
        resource_id=tentative.resource_id,
        decision=tentative.decision,
        reason_code=tentative.reason_code,
        payload_ref=tentative.payload_ref,
        at=tentative.at,
        break_glass_session_id=tentative.break_glass_session_id,
    )
