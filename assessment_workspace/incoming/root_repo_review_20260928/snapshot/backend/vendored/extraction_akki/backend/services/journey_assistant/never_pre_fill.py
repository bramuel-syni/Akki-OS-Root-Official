"""services.journey_assistant.never_pre_fill — W-M4-SW2 · surface (a).

Canon-5 §14 Shaping-Wizard 'never propose on mandatory fields' invariant.

The agent MAY ask about a mandatory field; the agent MUST NOT propose
a value for one.  Suggested-value drift into a mandatory-field slot
fires here as a mechanical RED.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional


CANON_5_S14_NEVER_PRE_FILL_VERBATIM: str = (
    "Layout: a chat pane on one side, an objective draft rail on the "
    "other … The operator states intent; the agent asks for "
    "mandatory fields and never proposes on them.  An estate-check "
    "chip renders inline before any feasibility-dependent question "
    "is asked … Every turn is grounded in a real estate read; no "
    "fabricated availability, ever, under any circumstance."
)


SlotState = Literal["empty", "filled_by_user", "agent_assumed"]


class AgentPreFillForbidden(RuntimeError):
    """Canon-5 §14: the agent MUST NOT propose a value for a mandatory field."""


@dataclass(frozen=True)
class MandatoryFieldSlot:
    """A mandatory-field slot on the objective draft-rail.

    Structural invariants:

      * Default `state='empty'` and `value=None`.
      * `agent_proposed_value` MUST always be None on a MANDATORY slot;
        setting it raises `AgentPreFillForbidden`.
      * `state='agent_assumed'` is FORBIDDEN on a mandatory slot (that
        state is for optional fields only).
      * The user MAY fill a mandatory slot (`value`, `state='filled_by_user'`).
    """

    field_name: str
    value: Optional[str] = None
    state: SlotState = "empty"
    agent_proposed_value: Optional[str] = None

    def __post_init__(self) -> None:
        # Mandatory field: agent may not propose.
        if self.agent_proposed_value is not None:
            raise AgentPreFillForbidden(
                f"Canon-5 §14: agent MUST NOT propose a value for "
                f"mandatory field {self.field_name!r}; got "
                f"agent_proposed_value=<redacted len="
                f"{len(self.agent_proposed_value)}>"
            )
        if self.state == "agent_assumed":
            raise AgentPreFillForbidden(
                f"Canon-5 §14: state='agent_assumed' is FORBIDDEN on "
                f"mandatory field {self.field_name!r}; agent-assumed "
                f"state is for OPTIONAL fields only"
            )


@dataclass(frozen=True)
class AgentAskOnly:
    """A Shaping-Wizard turn that is an ASK, not a PROPOSAL.

    Structural invariant: `AgentAskOnly` carries only a question and a
    reference to the slot; no proposed value can ride on it.  If a
    future refactor tries to add a `proposed_value` field, the
    corresponding SW2 invariant test breaks (hasattr check fires).
    """

    slot: MandatoryFieldSlot
    question_text: str


def build_ask_turn(*, slot: MandatoryFieldSlot, question_text: str) -> AgentAskOnly:
    """Build the ONE-turn ask that the Shaping-Wizard emits for a
    mandatory field.  This is the only way to ask; there is no
    complementary `propose_turn` for mandatory fields.
    """
    return AgentAskOnly(slot=slot, question_text=question_text)


def assert_no_prefill_on_mandatory_field(slot: MandatoryFieldSlot) -> None:
    """Downstream re-check: fail closed if a slot ever bypasses the
    constructor guard and carries an agent-proposed value."""
    if slot.agent_proposed_value is not None:
        raise AgentPreFillForbidden(
            f"Canon-5 §14 drift: mandatory slot {slot.field_name!r} "
            f"carries an agent-proposed value"
        )
    if slot.state == "agent_assumed":
        raise AgentPreFillForbidden(
            f"Canon-5 §14 drift: mandatory slot {slot.field_name!r} "
            f"is in state='agent_assumed'"
        )


__all__ = [
    "CANON_5_S14_NEVER_PRE_FILL_VERBATIM",
    "SlotState",
    "MandatoryFieldSlot",
    "AgentAskOnly",
    "AgentPreFillForbidden",
    "build_ask_turn",
    "assert_no_prefill_on_mandatory_field",
]
