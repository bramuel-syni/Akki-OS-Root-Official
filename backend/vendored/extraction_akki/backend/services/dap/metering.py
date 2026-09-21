"""W-DAP-STACK 2E · metering ledger + record-before-return.

Canon anchors: DAP-Spec DAP-21 [AU-3].

R-C2 marker (mirror from contracts/dap.py): MeteredEvent.au_3b_defensible
defaults to False until Doc-0 G-8 closes.  Silent flip forbidden.
"""

from __future__ import annotations

import datetime
from typing import List

from contracts.dap import MeteredEvent


class Ledger:
    """DAP-21 Ledger: append-only, read-visible.  Metered events are
    written here BEFORE the operation's result is returned."""

    def __init__(self) -> None:
        self._entries: List[MeteredEvent] = []

    def append(self, event: MeteredEvent) -> None:
        self._entries.append(event)

    def read_all(self) -> List[MeteredEvent]:
        return list(self._entries)

    def reset(self) -> None:
        self._entries.clear()


_ledger = Ledger()


def get_ledger() -> Ledger:
    return _ledger


def set_ledger(new_ledger: Ledger) -> None:
    """Test-only helper for injecting a busted ledger to exercise
    the DAP-21 write-before-return refusal path."""
    global _ledger
    _ledger = new_ledger


def record_metered_event(
    *,
    operation_type: str,
    accessed_scope: str,
    quantity: float,
    quantity_unit: str,
    terms_id: str,
    party_id: str,
) -> MeteredEvent:
    """DAP-21: build a MeteredEvent carrying all six required fields
    plus the R-C2 au_3b_defensible=False marker, write to the Ledger
    BEFORE returning the event.  If the ledger write fails, no result
    is returned (fail-closed)."""
    ev = MeteredEvent(
        operation_type=operation_type,
        accessed_scope=accessed_scope,
        quantity=quantity,
        quantity_unit=quantity_unit,
        terms_id=terms_id,
        party_id=party_id,
        timestamp_iso=datetime.datetime.now(datetime.UTC).isoformat(),
    )
    try:
        _ledger.append(ev)
    except Exception as exc:
        raise RuntimeError(
            f"DAP-21: ledger write failed ({exc!r}); operation result NOT "
            "returned (write-before-return fail-closed)."
        ) from exc
    return ev
