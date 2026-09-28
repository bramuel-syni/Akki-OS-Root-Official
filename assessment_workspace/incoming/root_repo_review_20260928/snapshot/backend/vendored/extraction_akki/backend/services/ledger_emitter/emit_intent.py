"""services/ledger_emitter/emit_intent.py · M10-W1 · sole intent-writer surface.

Canon anchors:
  v1.0 B.4 · Ledger records everything · single-writer discipline.
  Canon 3 §9.3 · append-only · no updates · no deletes.

This module is the ONLY file permitted to construct and publish a
LedgerIntent for consumption by services/ledger_writer/.  The intent
carries all fields except (seq, prev_hash, hash) which the writer
computes deterministically at append time.

TCB.yaml + akki.arch AST refuse any other file to write to `t_*.ledger`
collections directly — the writer is the SOLE surface at those
collections, and this emitter is the SOLE intent producer.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from contracts.ledger_v1 import LedgerRowAt


@dataclass(frozen=True)
class LedgerIntent:
    """Intent-to-append record.  The writer assigns (seq, prev_hash, hash)."""
    tenant_id: str
    run_id: str
    task_id: str
    actor_id: str
    actor_type: str
    event_type: str
    resource_type: str
    resource_id: str
    decision: str
    reason_code: str
    payload_ref: str
    at: LedgerRowAt
    break_glass_session_id: Optional[str] = None


def emit_intent(*, intent: LedgerIntent) -> LedgerIntent:
    """Sole intent-producer surface.  Returns the intent for the writer to
    pick up (durable-log wiring in W3 · Redis Streams per N-M10-Q3)."""
    # Validation: tenant_id + run_id required
    if not intent.tenant_id:
        raise ValueError("LEDGER-EMIT-001: tenant_id required")
    if not intent.run_id:
        raise ValueError("LEDGER-EMIT-002: run_id required")
    return intent
