"""services.reliable_time_source.clock — G-8 mechanism · W-M2-SW5.

Produces AU-3(b)-defensible timestamps via a monotonic-plus-anchored
clock.  A TimeAnchor is required; drift beyond budget refuses.

The clock retires the R-C2 marker's "not defensible" default for any
caller that constructs records USING this clock's defensible stamp.
Module-level R-C2 marker constants across `services/mtafiti/`,
`services/dap/metering.py`, and `services/solva_v2/trace.py` remain
as lineage anchors (silent flip forbidden by their own invariants);
individual writes can now opt-in to `au_3b_defensible=True` by using
`au_3b_defensible_now()`.
"""
from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Final

from pydantic import BaseModel, ConfigDict


AU_3B_DEFENSIBLE_DRIFT_BUDGET_MS: Final[int] = 100  # SP 800-53 AU-3(b)


class DriftExceededError(RuntimeError):
    """Wall-time drift from anchor exceeds the drift budget."""


class AnchorMissingError(RuntimeError):
    """No TimeAnchor supplied — a bare clock is not defensible."""


class TimeAnchor(BaseModel):
    """Reference-source anchor for defensible timestamps.

    * `source_id`: opaque handle for the reference source (e.g. NTP
      peer id · ROC-1 ratified time-source).
    * `anchor_wall_time`: the reference time captured at anchor.
    * `drift_budget_ms`: maximum acceptable drift from anchor in ms.
    """
    model_config = ConfigDict(frozen=True, extra="forbid")

    source_id: str
    anchor_wall_time: datetime
    drift_budget_ms: int = AU_3B_DEFENSIBLE_DRIFT_BUDGET_MS


class ReliableClock:
    """Monotonic + anchored clock.

    `now_ns()` reads `time.monotonic_ns()` (host-monotonic).
    `au_3b_defensible_stamp()` returns a defensible wall-time record
    that composes anchor id + drift measurement + defensible flag.
    """

    def __init__(self, anchor: TimeAnchor | None) -> None:
        self._anchor = anchor
        self._last_ns = 0

    def now_ns(self) -> int:
        n = time.monotonic_ns()
        if n < self._last_ns:
            n = self._last_ns  # defend monotonic contract
        self._last_ns = n
        return n

    def au_3b_defensible_stamp(self) -> dict:
        if self._anchor is None:
            raise AnchorMissingError(
                "au_3b_defensible_stamp requires a TimeAnchor; "
                "a bare clock is not AU-3(b) defensible"
            )
        now = datetime.now(timezone.utc)
        drift = (now - self._anchor.anchor_wall_time).total_seconds() * 1000.0
        if abs(drift) > self._anchor.drift_budget_ms:
            raise DriftExceededError(
                f"drift {abs(drift):.1f}ms exceeds budget "
                f"{self._anchor.drift_budget_ms}ms (anchor "
                f"source_id={self._anchor.source_id!r})"
            )
        return {
            "wall_time_iso": now.isoformat(),
            "anchor_source_id": self._anchor.source_id,
            "drift_from_anchor_ms": drift,
            "drift_budget_ms": self._anchor.drift_budget_ms,
            "au_3b_defensible": True,
        }


# --- process-wide default anchor + convenience --------------------------
# The default anchor is refreshed at import time to "now" against a
# nominal source id.  Callers that need production-grade anchoring
# construct their own TimeAnchor tied to a ratified source id (owner
# ruling · R-15/R-16 lineage) and pass it to a fresh ReliableClock.

_DEFAULT_ANCHOR = TimeAnchor(
    source_id="process_local_default",
    anchor_wall_time=datetime.now(timezone.utc),
    # Generous budget for the process-local default anchor — real
    # production anchors bind to a ratified source with tight budgets.
    drift_budget_ms=86_400_000,  # 24 hours
)
_DEFAULT_CLOCK = ReliableClock(anchor=_DEFAULT_ANCHOR)


def au_3b_defensible_now() -> dict:
    """Convenience: emit a defensible stamp using the process-wide
    default anchor.  For production ceremonies, callers should
    construct their own TimeAnchor + ReliableClock instead."""
    return _DEFAULT_CLOCK.au_3b_defensible_stamp()


__all__ = [
    "AU_3B_DEFENSIBLE_DRIFT_BUDGET_MS",
    "TIGHT_DRIFT_BUDGET_MAX_MS",
    "DriftExceededError",
    "AnchorMissingError",
    "LooseAnchorRefused",
    "TimeAnchor",
    "ReliableClock",
    "au_3b_defensible_now",
    "assert_defensible_for_governed_write",
]


# ---------------------------------------------------------------------
# W-M3-SW1 · FLAG-2 · tight-budget guard on governed defensible writes
# ---------------------------------------------------------------------
# Owner directive 2026-09-13: any record emitted with
# au_3b_defensible=True MUST bind a TIGHT drift budget; the loose 24h
# process-local default MUST NOT be able to reach a governed write.
TIGHT_DRIFT_BUDGET_MAX_MS: Final[int] = 5_000  # 5s production floor


class LooseAnchorRefused(RuntimeError):
    """A defensible-write attempt cited a stamp whose anchor drift
    budget exceeds TIGHT_DRIFT_BUDGET_MAX_MS or whose defensible flag
    is False.  Fail-closed per Flag-2 guard."""


def assert_defensible_for_governed_write(stamp: dict) -> None:
    """Refuse if the stamp is not tight-anchored + defensible.

    Callers writing metered/audit records with au_3b_defensible=True
    MUST call this immediately before the write; failure to do so is
    a Flag-2 discipline violation.
    """
    if not stamp.get("au_3b_defensible"):
        raise LooseAnchorRefused(
            "stamp is not au_3b_defensible; refusing governed write"
        )
    budget = stamp.get("drift_budget_ms")
    if budget is None or not isinstance(budget, int):
        raise LooseAnchorRefused(
            "stamp missing integer drift_budget_ms; refusing"
        )
    if budget > TIGHT_DRIFT_BUDGET_MAX_MS:
        raise LooseAnchorRefused(
            f"stamp drift budget {budget}ms exceeds tight write "
            f"budget {TIGHT_DRIFT_BUDGET_MAX_MS}ms — the loose process-"
            f"local default cannot reach a governed defensible write"
        )
