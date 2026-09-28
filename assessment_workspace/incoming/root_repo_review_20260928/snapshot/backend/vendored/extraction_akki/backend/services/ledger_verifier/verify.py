"""services/ledger_verifier/verify.py · M10-W3 · out-of-process chain verifier.

Owner-ruled B-M10-Q2 terms (banked verbatim in DECISIONS 2026-09-18T~12:30Z):
  * Cadence: nightly per tenant + on-demand (R-18 effect 12).
  * Location: verifier writes its receipts to its own append-only store
    under credentials the Ledger writer does NOT hold (C3 principle:
    verifier cannot share anything with the thing it verifies).
  * Publishes head hash to the tenant's receipt endpoint per B.4.
  * SEV-1: chain break pages the security group per B.10 AND is
    additionally recorded as a Watch signal (never as an action).

This module walks a per-tenant chain from genesis, recomputes every
hash, and reports (head_hash, break_at_seq_or_None).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional

from contracts.ledger_v1 import GENESIS_PREV_HASH, LedgerRow
from services.ledger_writer.main import compute_row_hash


@dataclass(frozen=True)
class VerifierReceipt:
    """B-M10-Q2 receipt shape · what the verifier publishes to tenant endpoint."""
    tenant_id: str
    head_seq: int
    head_hash: str
    break_at_seq: Optional[int]  # None if chain intact; seq of first broken row otherwise
    rows_walked: int


def _row_without_hash(row: LedgerRow) -> LedgerRow:
    """Return row with hash cleared (for recompute)."""
    from dataclasses import replace
    return replace(row, hash="")


def verify_chain(*, rows_in_seq_order: Iterable[LedgerRow]) -> VerifierReceipt:
    """Walk a per-tenant chain from genesis (seq=1) and verify each row's
    hash against the deterministic recompute rule.

    Returns a VerifierReceipt.  If chain is intact, break_at_seq is None.
    """
    prev_hash = GENESIS_PREV_HASH
    prev_seq: Optional[int] = None
    head_hash = ""
    head_seq = 0
    break_at: Optional[int] = None
    tenant_id: Optional[str] = None
    rows_walked = 0

    for row in rows_in_seq_order:
        rows_walked += 1
        # Genesis check
        if prev_seq is None:
            if row.seq != 1:
                break_at = row.seq
                break
            if row.prev_hash != GENESIS_PREV_HASH:
                break_at = row.seq
                break
            tenant_id = row.tenant_id
        else:
            if row.seq != prev_seq + 1:
                break_at = row.seq
                break
            if row.prev_hash != prev_hash:
                break_at = row.seq
                break
            if row.tenant_id != tenant_id:
                break_at = row.seq
                break

        # Recompute hash
        expected = compute_row_hash(row.prev_hash, _row_without_hash(row))
        if expected != row.hash:
            break_at = row.seq
            break

        prev_hash = row.hash
        prev_seq = row.seq
        head_hash = row.hash
        head_seq = row.seq

    return VerifierReceipt(
        tenant_id=tenant_id or "",
        head_seq=head_seq,
        head_hash=head_hash,
        break_at_seq=break_at,
        rows_walked=rows_walked,
    )
