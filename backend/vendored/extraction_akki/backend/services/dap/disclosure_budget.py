"""W-DAP-STACK 2E · DAP-26 per-party ceiling + S-25 estate release
budget marker.

Verbatim DAP-26 (partial · this sub-wave): 'per-party overrides, and
per-party ceilings.'

S-25 (per MILESTONE_PROMISE_BINDING §M1): estate-wide release budget
number is BLOCKED on Security R-7 owner ruling.  Under R-C1/R-C2
markers, 2E lands the mechanism tests-first with
`DEFAULT_RELEASE_BUDGET = 'DEFAULT-PENDING-OVERRIDE'`; silent flip
forbidden until an owner ruling replaces the marker.
"""

from __future__ import annotations

from typing import Dict, Tuple

from pydantic import BaseModel, ConfigDict


# S-25 estate-wide release budget marker — silent flip forbidden.
DEFAULT_RELEASE_BUDGET: str = "DEFAULT-PENDING-OVERRIDE"


class CeilingCheck(BaseModel):
    """DAP-26 per-party ceiling check result."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    party_id: str
    proposed_quantity: float
    used_so_far: float
    ceiling: float
    within_ceiling: bool


_ceilings: Dict[Tuple[str, str], float] = {}     # (estate_id, party_id)
_usage: Dict[Tuple[str, str], float] = {}        # (estate_id, party_id)


def set_party_ceiling(
    *, estate_id: str, party_id: str, ceiling: float,
) -> None:
    _ceilings[(estate_id, party_id)] = ceiling


def record_disclosure(
    *, estate_id: str, party_id: str, quantity: float,
) -> None:
    """DAP-26 cumulative accumulator — feeds A5 slow-play detection."""
    key = (estate_id, party_id)
    _usage[key] = _usage.get(key, 0.0) + quantity


def check_disclosure_ceiling(
    *, estate_id: str, party_id: str, proposed_quantity: float,
) -> CeilingCheck:
    """DAP-26 per-party ceiling — fail-closed on cumulative overflow."""
    key = (estate_id, party_id)
    used = _usage.get(key, 0.0)
    ceiling = _ceilings.get(key, float("inf"))
    projected = used + proposed_quantity
    return CeilingCheck(
        party_id=party_id,
        proposed_quantity=proposed_quantity,
        used_so_far=used,
        ceiling=ceiling,
        within_ceiling=(projected <= ceiling),
    )


def reset_state() -> None:
    """Test-only helper."""
    _ceilings.clear()
    _usage.clear()
