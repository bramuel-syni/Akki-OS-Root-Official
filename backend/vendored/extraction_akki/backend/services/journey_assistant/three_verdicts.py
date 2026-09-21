"""services.journey_assistant.three_verdicts — W-M4-SW4 · Canon-6 §12.

Every step resolves to answered / held / refused — never a fourth.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from services.journey_assistant.solva_explain import SolvaAction


CANON_6_S12_THREE_VERDICTS_VERBATIM: str = (
    "Three verdicts, never more. Every step in every journey above "
    "resolves to answered, held, or refused — never a fourth outcome "
    "invented to smooth over an awkward moment."
)


class JourneyVerdict(str, Enum):
    ANSWERED = "answered"
    HELD = "held"
    REFUSED = "refused"


class FourthVerdictForbidden(ValueError):
    """A verdict other than answered / held / refused was passed."""


class HeldWithoutReasonForbidden(ValueError):
    """A `held` verdict was passed without a `held_until_reason`."""


@dataclass(frozen=True)
class StepResolution:
    step_id: str
    verdict: JourneyVerdict
    answer_payload: Optional[dict] = None
    held_until_reason: Optional[str] = None
    refusal_action: Optional[SolvaAction] = None
    refusal_reason: Optional[str] = None


def _coerce_verdict(v: Any) -> JourneyVerdict:
    if isinstance(v, JourneyVerdict):
        return v
    if isinstance(v, str):
        try:
            return JourneyVerdict(v)
        except ValueError:
            pass
    raise FourthVerdictForbidden(
        f"Canon-6 §12 permits exactly three verdicts "
        f"(answered, held, refused); got {v!r}"
    )


def resolve_step(
    *,
    step_id: str,
    verdict: Any,
    answer_payload: Optional[dict] = None,
    held_until_reason: Optional[str] = None,
    refusal_action: Optional[SolvaAction] = None,
    refusal_reason: Optional[str] = None,
) -> StepResolution:
    """Resolve one journey step to exactly one canon verdict."""
    v = _coerce_verdict(verdict)
    if v == JourneyVerdict.HELD and not held_until_reason:
        raise HeldWithoutReasonForbidden(
            f"Canon-6 §12: `held` verdict on step {step_id!r} requires a "
            f"`held_until_reason`; held is not a fudge"
        )
    return StepResolution(
        step_id=step_id,
        verdict=v,
        answer_payload=answer_payload,
        held_until_reason=held_until_reason,
        refusal_action=refusal_action,
        refusal_reason=refusal_reason,
    )


__all__ = [
    "CANON_6_S12_THREE_VERDICTS_VERBATIM",
    "JourneyVerdict",
    "StepResolution",
    "FourthVerdictForbidden",
    "HeldWithoutReasonForbidden",
    "resolve_step",
]
