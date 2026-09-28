"""M6 · Audio-Plane v1.0 · CP-M6-8-2 · §11.3 Milestone-list contract · CLOSES SUB-WAVE 8.

Verbatim canon anchor (§11.3 P181..P182 · V114 · single-line for gating-test docstring parity):

  "Sampling & Reflection has two customers. It prices the real job, and it authors the accountability structure: its output to the objective owner is not a curve but a proposed milestone list — the checklist of what must be done, in what order, for the commission to succeed. Each milestone carries a done-condition and an owner. The objective owner reviews and agrees the list at commission; from that point, all reporting is against it. Accountability is set before spend, not discovered during."

This module lands the compile-time authoring surface for milestone lists:
`Milestone` (frozen 3-carrier · V114b done-condition + owner mandatory),
`MilestoneList` (frozen 3-carrier · V114a ordered milestones + commission
agreement ref + commission id), `construct_milestone_list` (V114a
factory · refuses empty), `agree_milestone_list` (V114c gate · returns a
new frozen list with agreement ref set; refuses re-agreement per V114d
"from that point, all reporting is against it"), and
`assert_commission_open_only_after_agreement` (V114c refusal).

Wave-honest limits (per M6 SW8 grounding brief §D):

- Compile-time authoring surface + agreement gate only.
- Runtime status (done / on-track / behind / missed) is §13.2
  Commission View concern — lands sub-wave 9.
- V114c agreement ref is opaque; ref-verification (signature /
  authenticator / receipt) is a Watch / Commission View concern.
- No LLM / HTTP / filesystem / network.  Case-agnostic.
- §3.1 P038 tokens-not-waveforms preserved.
- Synthetic-fixtures-only in tests.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Optional, Tuple

__all__ = (
    "Milestone",
    "MilestoneList",
    "construct_milestone_list",
    "agree_milestone_list",
    "assert_commission_open_only_after_agreement",
    "MilestoneMissingDoneConditionError",
    "MilestoneMissingOwnerError",
    "MilestoneListEmptyError",
    "MilestoneListAlreadyAgreedError",
    "CommissionOpenBeforeAgreementError",
)


# ---------------------------------------------------------------------------
# Refusals (V114 clause-anchored)
# ---------------------------------------------------------------------------


class MilestoneMissingDoneConditionError(Exception):
    """§11.3 V114b: 'Each milestone carries a done-condition and an
    owner.'  Raised at `Milestone.__post_init__` when done_condition
    is empty."""


class MilestoneMissingOwnerError(Exception):
    """§11.3 V114b: 'Each milestone carries a done-condition and an
    owner.'  Raised at `Milestone.__post_init__` when owner is empty."""


class MilestoneListEmptyError(Exception):
    """§11.3 V114a: 'a proposed milestone list — the checklist of
    what must be done, in what order'.  Raised at
    `construct_milestone_list` when milestones tuple is empty."""


class MilestoneListAlreadyAgreedError(Exception):
    """§11.3 V114d: 'from that point, all reporting is against it.'
    Once a MilestoneList carries an agreement ref, re-agreeing is
    refused."""


class CommissionOpenBeforeAgreementError(Exception):
    """§11.3 V114c: 'The objective owner reviews and agrees the list
    at commission; from that point, all reporting is against it.'
    Commission cannot open until agreement.  Raised by
    `assert_commission_open_only_after_agreement` when
    commission_agreement_ref is None."""


# ---------------------------------------------------------------------------
# Carriers (V114a + V114b)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Milestone:
    """§11.3 V114b: 'Each milestone carries a done-condition and an owner.'

    Frozen 3-carrier: milestone_id + done_condition + owner.  Both
    done_condition and owner are mandatory non-empty strings; empty
    values refuse at `__post_init__`.
    """

    milestone_id: str
    done_condition: str
    owner: str

    def __post_init__(self) -> None:
        if not self.done_condition:
            raise MilestoneMissingDoneConditionError(
                "Milestone requires a non-empty done-condition "
                "(V114b · P182 'Each milestone carries a "
                "done-condition and an owner')."
            )
        if not self.owner:
            raise MilestoneMissingOwnerError(
                "Milestone requires a non-empty owner "
                "(V114b · P182 'Each milestone carries a "
                "done-condition and an owner')."
            )


@dataclass(frozen=True)
class MilestoneList:
    """§11.3 V114a: 'a proposed milestone list — the checklist of
    what must be done, in what order, for the commission to succeed.'

    Frozen 3-carrier:
      - `milestones`: ordered tuple of `Milestone` (V114a ordering
        load-bearing).
      - `commission_agreement_ref`: Optional[str].  None until the
        objective owner agrees (V114c).
      - `commission_id`: opaque commission identifier.
    """

    milestones: Tuple[Milestone, ...]
    commission_agreement_ref: Optional[str]
    commission_id: str


# ---------------------------------------------------------------------------
# Factory + agreement gate (V114a + V114c + V114d)
# ---------------------------------------------------------------------------


def construct_milestone_list(
    *,
    milestones: Tuple[Milestone, ...],
    commission_id: str,
) -> MilestoneList:
    """§11.3 V114a factory.

    Refuses `MilestoneListEmptyError` on empty milestones.
    Constructs a MilestoneList with `commission_agreement_ref=None`
    (not yet agreed).
    """
    if not milestones:
        raise MilestoneListEmptyError(
            "MilestoneList must contain at least one Milestone "
            "(V114a · P181 'a proposed milestone list — the "
            "checklist of what must be done')."
        )
    return MilestoneList(
        milestones=milestones,
        commission_agreement_ref=None,
        commission_id=commission_id,
    )


def agree_milestone_list(
    *,
    milestone_list: MilestoneList,
    commission_agreement_ref: str,
) -> MilestoneList:
    """§11.3 V114c gate.

    Returns a NEW frozen MilestoneList with the agreement ref set;
    the original is untouched (frozen · immutable value semantics).
    Refuses `MilestoneListAlreadyAgreedError` if the passed list
    already carries an agreement ref (V114d "from that point, all
    reporting is against it" — once agreed, locked).
    """
    if milestone_list.commission_agreement_ref is not None:
        raise MilestoneListAlreadyAgreedError(
            "MilestoneList is already agreed; re-agreement is refused "
            "(V114d · P182 'from that point, all reporting is against it')."
        )
    return replace(
        milestone_list,
        commission_agreement_ref=commission_agreement_ref,
    )


def assert_commission_open_only_after_agreement(
    *,
    milestone_list: MilestoneList,
) -> None:
    """§11.3 V114c refusal.

    Refuses `CommissionOpenBeforeAgreementError` when the
    MilestoneList has no agreement ref (i.e., the objective owner
    has not yet reviewed and agreed the list).  V114e "Accountability
    is set before spend, not discovered during" — the refusal fires
    at the gate call, before any commission-open side-effect.
    """
    if milestone_list.commission_agreement_ref is None:
        raise CommissionOpenBeforeAgreementError(
            "commission cannot open before agreement "
            "(V114c · P182 'The objective owner reviews and agrees "
            "the list at commission; from that point, all reporting "
            "is against it')."
        )
