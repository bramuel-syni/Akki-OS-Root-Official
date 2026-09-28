"""W-DAP-STACK 2B · browse primitive + pull-seam.

Canon anchors:
    * DAP-Spec DAP-6 (verbatim): 'Browse MUST return aggregate composition
      only... and MUST NOT return, sample, or preview unit contents.
      Browsing an estate is not a crossing and MUST NOT be recorded as one.'
    * DAP-Spec DAP-7 (verbatim): 'A connected workspace's queries execute
      inside the estate's perimeter.  The party's query enters; de-identified
      results leave.  Estate data MUST NOT leave under this operation, and
      no code path may make it do so.'
"""

from __future__ import annotations

import datetime
from typing import Dict

from pydantic import BaseModel, ConfigDict, Field


class BrowseAggregate(BaseModel):
    """Aggregate-only estate summary — DAP-6."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    estate_id: str
    volume: int = Field(..., description="Total unit count across the estate.")
    type_counts: Dict[str, int] = Field(default_factory=dict)
    language_counts: Dict[str, int] = Field(default_factory=dict)
    period_from: str = Field(..., description="ISO date, earliest unit created.")
    period_to: str = Field(..., description="ISO date, latest unit created.")
    as_of_iso: str = Field(
        ...,
        description="Timestamp of the census this aggregate was drawn from. "
        "DAP-30 honesty grammar: stale-marked if the census is stale.",
    )


def browse_estate(estate_id: str) -> BrowseAggregate:
    """Return aggregate composition only.  No unit contents or samples.

    DAP-6.  A minimal fixture is returned here at kernel grade; the eventual
    census-plane integration lands with M1 mtafiti-composition wiring.
    """
    return BrowseAggregate(
        estate_id=estate_id,
        volume=0,
        type_counts={},
        language_counts={},
        period_from="",
        period_to="",
        as_of_iso=datetime.datetime.now(datetime.UTC).isoformat(),
    )


def browse_is_not_a_crossing() -> bool:
    """Explicit invariant surface — DAP-6 tail.  Browsing is deliberately NOT
    a crossing and is NOT recorded as one."""
    return True


def pull_seam_query(*, estate_id: str, party_query: Dict) -> Dict:
    """DAP-7 · party query enters; de-identified results leave.

    Estate-side query execution happens inside the perimeter; only aggregate
    results egress.  Source rows / unit ids / raw records are NEVER returned.
    """
    _ = party_query, estate_id  # accepted by contract; kernel-grade stub
    return {
        "aggregate": {"count": 0, "as_of_iso": datetime.datetime.now(datetime.UTC).isoformat()},
        "terms_id": "terms_v1",
    }
