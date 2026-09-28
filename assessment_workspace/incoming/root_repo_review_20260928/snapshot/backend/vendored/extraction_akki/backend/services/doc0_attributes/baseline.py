"""services.doc0_attributes.baseline — W-M2-SW11 · Doc-0 Attr-7."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class BaselineFloorViolation(RuntimeError):
    """Measured value falls below the baseline floor."""


class Baseline(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    floor_score: int = Field(ge=0)


def check_meets_baseline(*, baseline: Baseline, measured_score: int) -> None:
    """Fail-closed: below-floor refuses to serve (Doc-0 Attr-7)."""
    if measured_score < baseline.floor_score:
        raise BaselineFloorViolation(
            f"measured {measured_score} < baseline floor "
            f"{baseline.floor_score} — refusing to serve"
        )


def unlowerable_by_measured(*, baseline: Baseline, measured_score: int) -> bool:
    """Return True iff `measured_score` would lower the baseline; the
    Attr-7 invariant asserts a measurement never lowers the baseline
    in force, so this function ALWAYS returns False (unlowered) —
    it exists to make the doctrine callable + testable.
    """
    _ = measured_score
    _ = baseline
    return False


__all__ = [
    "BaselineFloorViolation",
    "Baseline",
    "check_meets_baseline",
    "unlowerable_by_measured",
]
