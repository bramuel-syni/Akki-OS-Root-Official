"""services.journey_assistant.estate_check_chip — W-M4-SW3 · §14 second half.

Canon-5 §14: an estate-check chip renders inline before any
feasibility-dependent question is asked; every turn is grounded in a
real estate read; no fabricated availability, ever.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional


CANON_5_S14_ESTATE_CHECK_VERBATIM: str = (
    "An estate-check chip renders inline before any feasibility-"
    "dependent question is asked … Every turn is grounded in a real "
    "estate read; no fabricated availability, ever, under any "
    "circumstance."
)


ReadSource = Literal["live", "cached-fresh", "cached-stale"]


class FabricatedAvailabilityForbidden(RuntimeError):
    """Canon-5 §14: no fabricated availability, ever, under any circumstance."""


class EstateCheckChipMissing(RuntimeError):
    """A feasibility-dependent question was built without an estate-check chip."""


@dataclass(frozen=True)
class EstateCheckChip:
    """Inline chip carrying evidence that a real estate read backs the
    next question.

    Construction refuses:

      * `read_source == "fabricated"` (any variant) —
        `FabricatedAvailabilityForbidden`.
      * Empty `real_estate_read_receipt_id` — same.
    """

    real_estate_read_receipt_id: str
    read_source: str
    summary_text: str

    def __post_init__(self) -> None:
        if not self.real_estate_read_receipt_id:
            raise FabricatedAvailabilityForbidden(
                "Canon-5 §14: estate-check chip requires a non-empty "
                "`real_estate_read_receipt_id`; empty value refused"
            )
        if self.read_source not in ("live", "cached-fresh", "cached-stale"):
            raise FabricatedAvailabilityForbidden(
                f"Canon-5 §14: read_source={self.read_source!r} is not "
                f"a permitted grounded-read source; permitted values "
                f"are 'live', 'cached-fresh', 'cached-stale'"
            )

    def to_inline_dict(self) -> dict:
        return {
            "read_receipt_id": self.real_estate_read_receipt_id,
            "read_source": self.read_source,
            "summary_text": self.summary_text,
        }


@dataclass(frozen=True)
class FeasibilityQuestion:
    """A wizard-turn question, tagged as feasibility-dependent or not.

    Structural invariant (enforced by
    `build_feasibility_question_or_refuse`): if
    `is_feasibility_dependent=True`, `estate_check_chip` MUST NOT be
    None.
    """

    question_text: str
    is_feasibility_dependent: bool
    estate_check_chip: Optional[EstateCheckChip]


def build_feasibility_question_or_refuse(
    *,
    question_text: str,
    is_feasibility_dependent: bool,
    estate_check_chip: Optional[EstateCheckChip],
) -> FeasibilityQuestion:
    """Constructor that enforces the estate-check-inline rule."""
    if is_feasibility_dependent and estate_check_chip is None:
        raise EstateCheckChipMissing(
            "Canon-5 §14: feasibility-dependent question requires an "
            "inline estate-check chip; got None"
        )
    return FeasibilityQuestion(
        question_text=question_text,
        is_feasibility_dependent=is_feasibility_dependent,
        estate_check_chip=estate_check_chip,
    )


__all__ = [
    "CANON_5_S14_ESTATE_CHECK_VERBATIM",
    "ReadSource",
    "EstateCheckChip",
    "FeasibilityQuestion",
    "EstateCheckChipMissing",
    "FabricatedAvailabilityForbidden",
    "build_feasibility_question_or_refuse",
]
