"""CP-AIP-6-OBJECTIVE-WIZARD · ObjectiveSession_v0 · additive §1.2 sibling contract of sealed WizardCommitState_v0.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-6-OBJECTIVE-WIZARD and nothing else.

Spec anchor: AIP v1.0 §8 Objective Wizard + §8.5 Record and handoff.

§8 verbatim: 'The Objective Wizard — a new variant of the existing
shaping wizard, reusing its agent interface, guards, session
persistence, and ledger sidecar — elicits an objective in plain
language and compiles two governed artifacts: TargetOutcome (§10) +
Collection Schema (§9).'

§8.5 verbatim: 'Every session stamps to the ledger via the existing
turn-ledger pattern under a distinct data class (objective_session),
including options considered and rejected — which is what makes a
later "why was the model built this way" answerable.'

§16.1 (c) CLEAN receipt (2026-02-23T05:00:00Z) verbatim: 'extend
existing state machine with additive `objective` variant on
WizardCommitState_v0.variant Literal · sibling machine explicitly
rejected per §1.2.'

This module lands the sibling CONTRACT carrying the ObjectiveSession_v0
data class per §8.5.  The variant extension of WizardCommitState_v0.
variant Literal is documented here but the actual Literal edit is a
FOLLOW-ON slice under §16.1 (c) recommendation VERIFIED - this sibling
contract does NOT edit the sealed WizardCommitState_v0 per SO §3.8.

Additive-only per SO §3.8.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final, Optional, Tuple


# §16.1 (c) CLEAN receipt · variant enum extension recommendation.
# Documented here for the sibling contract landing.
OBJECTIVE_VARIANT_NAME: Final[str] = "objective"


@dataclass(frozen=True)
class ObjectiveSession_v0:
    """§8.5 verbatim: 'a distinct data class (objective_session),
    including options considered and rejected'.

    Fields:
      - session_id · uuid-like unique wizard session id (mirrors sealed
        WizardCommitState_v0.session_id shape).
      - variant · Literal-shape ('objective') · sibling to sealed
        WizardCommitState_v0.variant (see §16.1 (c) verified).
      - options_considered · every option surfaced at any turn (§8.5).
      - options_rejected · subset of options_considered that were
        surfaced but not selected (§8.5 verbatim).
      - target_outcome_ref · post-compile pointer to the emitted
        TargetOutcome_v0.
      - collection_schema_ref · post-compile pointer to the emitted
        CollectionSchema_v0.
    """

    session_id: str
    variant: str
    options_considered: Tuple[str, ...]
    options_rejected: Tuple[str, ...]
    target_outcome_ref: str
    collection_schema_ref: str

    def __post_init__(self) -> None:
        if self.variant != OBJECTIVE_VARIANT_NAME:
            raise ValueError(
                f"ObjectiveSession_v0.variant={self.variant!r} · MUST "
                f"equal {OBJECTIVE_VARIANT_NAME!r} · §16.1 (c) verbatim: "
                f"sibling machine explicitly rejected per §1.2; this "
                f"sibling contract carries only the objective variant."
            )
        rejected_set = set(self.options_rejected)
        considered_set = set(self.options_considered)
        if not rejected_set.issubset(considered_set):
            missing = rejected_set - considered_set
            raise ValueError(
                f"ObjectiveSession_v0.options_rejected includes "
                f"{sorted(missing)!r} which are not in options_"
                f"considered · §8.5 verbatim requires rejected to be a "
                f"subset of considered."
            )
