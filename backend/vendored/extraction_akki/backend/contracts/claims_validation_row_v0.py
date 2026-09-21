"""ClaimsValidationRowV0 · Doc 19B §19B.4 · EP-3 A-4 claims validation.

Owner-verbatim spec (canon/text/Akki_Canon_Documents_17_19.txt line 232):
    'A-4, proposed as a companion mechanism, never a build gate:
     claims validation functioning as the re-entry path for previously
     killed backlog (a parked idea returns only with a three-arm result
     behind it) and as the bake-off court for competing implementation
     choices.'

EP-3 verbatim (line 241):
    'EP-3 [PROPOSED] A-4 (claims validation) rides inside this
     capability, scoped explicitly as validation, never a build gate —
     its real experiments require real material and naturally sequence
     after the terminal test.'

§19B.6 verbatim (line 247):
    'A-4 never becomes a gate by drift — its scope is validation and
     re-entry, and staying there is a condition of adoption, not a
     detail.'

Same-commit DoD:
  * ConfigDict(extra='forbid', frozen=True).
  * tests/invariants/claims_validation_row_v0.contract_snapshot.json.
  * Parity map bump 63 -> 64.

Verdict grammar (closed):
  * awaiting_result   · shell open · three arms not yet reported.
  * killed_stays      · re-entry attempt did not produce a stronger
                        result; parked idea stays killed.
  * reentered         · three-arm result cleared the re-entry bar
                        (proposed idea re-enters the backlog).
  * bakeoff_verdict   · competing implementation choice ruled.
"""
from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


CLAIM_KINDS: tuple = ("reentry", "bakeoff")
VERDICT_KINDS: tuple = (
    "awaiting_result",
    "killed_stays",
    "reentered",
    "bakeoff_verdict",
)


class ClaimsValidationRowV0(BaseModel):
    """A-4 · claims validation ledger row.

    A companion to the evidence register (§19B.4). Records three-arm
    results for re-entry attempts and bake-off decisions for competing
    implementations. NEVER GATES: Owner ratification is the only
    consequence of a favorable verdict.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    claim_id: str = Field(..., min_length=1)
    claim_kind: Literal["reentry", "bakeoff"] = Field(
        ...,
        description="'reentry' = parked-idea revival; 'bakeoff' = "
                    "competing-implementation ruling.",
    )
    subject: str = Field(
        ...,
        min_length=1,
        description="What is being validated (backlog id / feature name).",
    )
    three_arms: List[str] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="'A parked idea returns only with a three-arm result "
                    "behind it.' Exactly three arms recorded.",
    )
    arm_results: List[float] = Field(
        default_factory=list,
        description="Optional numeric results per arm; empty until arms "
                    "complete. Length must match three_arms when set.",
    )
    verdict: Literal[
        "awaiting_result", "killed_stays", "reentered", "bakeoff_verdict"
    ] = Field(default="awaiting_result")
    verdict_note: str = Field(default="")
    ratified_at: Optional[str] = Field(default=None)
    opened_at: str = Field(..., min_length=1)
    status_class: Literal["PROPOSED", "CANON"] = Field(
        default="PROPOSED",
        description="Doc 19B PROPOSED · Owner ratification flips to CANON.",
    )
    proposal_source_ref: str = Field(
        default="Doc 19B §19B.4 A-4 + §19B.5 EP-3",
        min_length=1,
    )

    @model_validator(mode="after")
    def _arm_results_length_matches_arms(self):
        if self.arm_results and len(self.arm_results) != 3:
            raise ValueError(
                "A-4 three-arm result: arm_results must be either empty "
                "(pre-report) or length 3, one per arm."
            )
        return self
