"""services.journey_assistant.solva_explain — W-M4-SW1 · surface (c).

User-facing 'walk me through why the answer stopped here and what I
should do' wrapper for Solva refusals.  Every explanation binds to
exactly one of the three canon actions (Canon-4 §24) and carries the
DAP-20 boundary marker; a fourth action is refused at the type
boundary; gates cannot be decided from this surface.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


# ---------------------------------------------------------------------------
# Verbatim canon anchors
# ---------------------------------------------------------------------------

CANON_4_S24_THREE_ACTIONS_VERBATIM: str = (
    "accept the result as a recorded statement, narrow the "
    "objective, or lower the standard"
)

SOLVA_EXPLAIN_DAP20_BOUNDARY_MARKER: str = (
    "The portal's assistance chat MAY help a party shape an "
    "objective, identify relevant scope, or understand terms, "
    "before commission. It MUST NOT approve, widen scope after "
    "commission, or decide any gate. It proposes; the gates decide."
)


# ---------------------------------------------------------------------------
# Type boundary — three actions, no fourth
# ---------------------------------------------------------------------------


class SolvaAction(str, Enum):
    """Canon-4 §24 three-action refusal set — fourth action forbidden."""

    ACCEPT_AS_STATED = "accept_as_stated"
    NARROW_OBJECTIVE = "narrow_objective"
    LOWER_STANDARD = "lower_standard"


class FourthActionForbidden(ValueError):
    """Passed action is not one of the three canon actions."""


class SolvaExplainMustNotDecide(RuntimeError):
    """DAP-20 boundary: this surface may not decide a gate."""


# ---------------------------------------------------------------------------
# SolvaExplanation
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SolvaExplanation:
    """A user-facing explanation of a Solva refusal.

    * `action` is exactly one canon action.
    * `refusal_reason` is the internal reason code the user's answer
      card records (Canon-5 §29).
    * `user_facing_reason` is the plain-language explanation.
    * `dap_20_boundary_marker` rides on every explanation so callers
      cannot accidentally strip the boundary.
    """

    refusal_reason: str
    action: SolvaAction
    user_facing_reason: str
    dap_20_boundary_marker: str = SOLVA_EXPLAIN_DAP20_BOUNDARY_MARKER

    def decide_gate(self, *, gate_id: str, verdict: str) -> None:
        """DAP-20 · this surface may NOT decide a gate."""
        _ = (gate_id, verdict)
        raise SolvaExplainMustNotDecide(
            "DAP-20: Solva-explain surface MUST NOT decide a gate; "
            "it proposes; the gates decide."
        )

    def to_answer_card(self) -> dict:
        """Serialise into the Canon-5 §29 answer-card shape."""
        return {
            "action": self.action.value,
            "reason": self.refusal_reason,
            "user_facing_reason": self.user_facing_reason,
            "dap_20_boundary": self.dap_20_boundary_marker,
        }


def _coerce_action(action) -> SolvaAction:
    if isinstance(action, SolvaAction):
        return action
    if isinstance(action, str):
        try:
            return SolvaAction(action)
        except ValueError:
            pass
    raise FourthActionForbidden(
        f"Canon-4 §24 permits exactly three actions "
        f"({', '.join(a.value for a in SolvaAction)}); "
        f"got {action!r}"
    )


def explain_refusal(
    *,
    refusal_reason: str,
    action,
    user_facing_reason: str,
) -> SolvaExplanation:
    """Construct a user-facing SolvaExplanation.

    Canon-4 §24: only the three canon actions may bind here.  A fourth
    action raises `FourthActionForbidden` at the write boundary.
    """
    canon_action = _coerce_action(action)
    return SolvaExplanation(
        refusal_reason=refusal_reason,
        action=canon_action,
        user_facing_reason=user_facing_reason,
    )


__all__ = [
    "CANON_4_S24_THREE_ACTIONS_VERBATIM",
    "SOLVA_EXPLAIN_DAP20_BOUNDARY_MARKER",
    "SolvaAction",
    "SolvaExplanation",
    "explain_refusal",
    "FourthActionForbidden",
    "SolvaExplainMustNotDecide",
]
