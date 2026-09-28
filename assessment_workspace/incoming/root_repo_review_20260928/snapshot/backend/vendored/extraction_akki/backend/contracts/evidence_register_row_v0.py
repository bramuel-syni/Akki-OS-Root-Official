"""EvidenceRegisterRowV0 · Doc 19B §19B.5 · evidence-register row shape.

Owner-verbatim spec (canon/text/Akki_Canon_Documents_17_19.txt line 235-238):
    'Evidence register row (proposed)
       { figure, method, judges: [..], judge_versions: [..],
         rubric_version, kappa, date, source_rows: [..] }
       Standing rule: no figure quoted externally without
       resolving to a register row.'

STATUS-CLASS DISCIPLINE (Owner Condition 1):
Doc 19B is PROPOSED, not CANON — 'never confirmed adopted' (line 218).
Every evidence-register row therefore carries `status_class='PROPOSED'`
and a `proposal_source_ref` citation. The row exists so the register can
harden the custody-recall and Model Acceptance sites (EP-1), but the
register itself is PROPOSED until Owner ratification.

§19B.4 named application sites (verbatim from lines 225-229):
  1. terminal_test              — highest priority; human-qualified
                                  benchmark slice, published kappa.
  2. per_language_custody_recall — 'the claim most exposed under
                                    diligence, currently single-scored
                                    by design'.
  3. model_acceptance_moac       — Doc 17 MOAC six checks;
                                    'canon already mandates human
                                     quality judgement over the six
                                     checks'.
  4. refusal_correctness         — Doc 8 refusal-health surface;
                                    'sampled dual-judge audit would
                                    give the refusal grammar a
                                    measured integrity figure'.
  5. existing_verification_loop  — 'builder verification versus
                                    independent tester is already de
                                    facto dual-judge'.

Same-commit DoD:
  * ConfigDict(extra='forbid', frozen=True) — buyer-facing hardening.
  * tests/invariants/evidence_register_row_v0.contract_snapshot.json.
  * Parity map bump 62 -> 63.
"""
from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


NAMED_SITES: tuple = (
    "terminal_test",
    "per_language_custody_recall",
    "model_acceptance_moac",
    "refusal_correctness",
    "existing_verification_loop",
)


class EvidenceRegisterRowV0(BaseModel):
    """Doc 19B §19B.5 · evidence-register row.

    EP-2 verbatim: 'Dual-judge scoring (A-2) applies at every named
    site in §19B.4, plus any future site where a judgement call
    becomes a published number.' → at least 2 judges required, and
    judge_versions must match count with judges.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    figure_id: str = Field(
        ...,
        min_length=1,
        description="Unique key: '<site>/<figure_name>@<date>'.",
    )
    figure: str = Field(
        ...,
        min_length=1,
        description="The number itself as it will be quoted (e.g. '0.87 kappa').",
    )
    method: str = Field(
        ...,
        min_length=1,
        description="How the figure was produced (spec/protocol name).",
    )
    named_site: Literal[
        "terminal_test",
        "per_language_custody_recall",
        "model_acceptance_moac",
        "refusal_correctness",
        "existing_verification_loop",
    ] = Field(
        ...,
        description="§19B.4 site the figure attaches to (closed grammar).",
    )
    judges: List[str] = Field(
        ...,
        min_length=2,
        description="Judge identifiers · MIN 2 (dual-judge A-2 · EP-2).",
    )
    judge_versions: List[str] = Field(
        ...,
        min_length=2,
        description="Judge version tags · same count as judges.",
    )
    rubric_version: str = Field(..., min_length=1)
    kappa: float = Field(
        ...,
        ge=-1.0,
        le=1.0,
        description="Inter-rater agreement (Cohen's or Fleiss' kappa).",
    )
    date: str = Field(..., min_length=1)
    source_rows: List[str] = Field(
        ...,
        min_length=1,
        description="Register rows / receipts / seals the figure resolves to.",
    )
    status_class: Literal["PROPOSED", "CANON"] = Field(
        default="PROPOSED",
        description="Doc 19B PROPOSED status carried on the row itself; "
                    "flips to CANON only on Owner ratification (never by "
                    "convention). Default PROPOSED honors §19B.1 verbatim.",
    )
    proposal_source_ref: str = Field(
        default="Doc 19B §19B.5",
        min_length=1,
        description="Doc/section citation the row's authority comes from.",
    )

    @model_validator(mode="after")
    def _judges_count_matches_versions(self):
        if len(self.judges) != len(self.judge_versions):
            raise ValueError(
                "EP-2 verbatim: dual-judge scoring — judges and "
                f"judge_versions must be the same length; "
                f"got {len(self.judges)} vs {len(self.judge_versions)}."
            )
        return self
