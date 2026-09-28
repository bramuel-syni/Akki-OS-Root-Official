"""ModelAcceptanceCard_v0 — Canon 4 §26 six-criterion MOAC.

Freeze contract: 38th frozen contract post-W7 CP4 landing. Snapshot
bijection enforced by `test_frozen_contract_snapshot_parity.py` +
`test_composed_conclusion_snapshot_parity_at_18` (count 37 → 38).

**Canon 4 §26 verbatim** — every accepted adapter carries a six-criterion
scorecard with real measured numbers:

  §26.1 · Accuracy on the tenant's uncurated measured composition
          (Doc 1 §4.10).
  §26.2 · Coverage across strata Mtafiti has measured.
  §26.3 · Refusal behaviour under Solva-pattern (§17) — measured
          refuse-rate on out-of-scope prompts.
  §26.4 · Provenance integrity of the training data (Doc 1 §4.9).
  §26.5 · Cost per operation, measured on real load.
  §26.6 · Time to answer at the 95th percentile, measured under the
          platform's load pattern.

**Canon 4 §27 (C4-038)**: MOAC evidence is drawn from an UNCURATED
sample of the tenant's material (Doc 1 §4.10). Curated benchmarks are
inadmissible for MOAC. Enforced by `evidence_source_kind` field —
only `uncurated_registry_sample` and `uncurated_estate_sample` are
admissible values.

**Canon 4 §28 (C4-039)**: Every adapter carries its full training
lineage back to rights-held source material. An adapter whose lineage
cannot be resolved is a defect and does not ship. Enforced by
`training_lineage_resolved` boolean field — admission refuses if False.

**Owner Ruling 2026-08-25T23:30Z (W7 GO · Q2)**: MOAC.1/§26.1 and
MOAC.2/§26.2 REUSE the Registry census facts (235 tables · 145
crossing receipts) as the uncurated sample where the letter permits.
Fresh record-content passes require a named purpose + structure-only
posture. If Doc 13's letter requires record-contents sampling without
a purpose on record, NAME THE GAP rather than sampling. This is
expressed by `evidence_source_kind` values `uncurated_registry_sample`
(structure-only pass over Registry census facts — the default and
purpose-safe path) vs `uncurated_estate_sample` (record-contents pass
under a named purpose · requires `evidence_purpose_id` populated).
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class MoacCriterion(BaseModel):
    """One of the six MOAC criteria. Real measured number + a stated
    method of measurement + the floor that this criterion is checked
    against.

    Owner-supplied floors live in the rates register / owner-ruling
    stream; the card ITSELF carries the measured number + method +
    floor value on record at measurement time (facts-not-claims per
    Canon 1 §4.4).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    measured_value: float = Field(
        ...,
        description="Real measured number for this criterion. Units are "
                    "criterion-specific; see canon_anchor for the letter.",
    )
    unit: str = Field(
        ...,
        min_length=1,
        description="Unit for measured_value (e.g., 'accuracy_fraction', "
                    "'coverage_fraction', 'refuse_rate_fraction', "
                    "'provenance_resolved_fraction', 'usd_per_million_tokens', "
                    "'seconds_at_p95').",
    )
    method_of_measurement: str = Field(
        ...,
        min_length=1,
        description="Plain-language sentence naming the pass that produced "
                    "measured_value. What sample, what harness, what date.",
    )
    floor_value: Optional[float] = Field(
        default=None,
        description="Owner-supplied floor for this criterion at measurement "
                    "time. If None, no floor is on record (honest gap · Canon "
                    "1 §4.4). Admission refuses if measured_value < floor_value "
                    "AND floor_value is not None.",
    )
    canon_anchor: str = Field(
        ...,
        min_length=1,
        description="Canon §26.N reference for this criterion (e.g., '§26.1').",
    )


class ModelAcceptanceCard_v0(BaseModel):
    """Canon 4 §26 MOAC — six-criterion scorecard.

    Every accepted adapter carries this. Admission ceremony (see
    `services/model_admission/ceremony.py`) reads MOAC + rights lineage
    + evidence-source-kind and admits / refuses / quarantines.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    candidate_model_id: str = Field(
        ...,
        min_length=1,
        description="Model id under admission. Passed to model_registry."
                    "register_model on success.",
    )
    evidence_source_kind: Literal[
        "uncurated_registry_sample",
        "uncurated_estate_sample",
    ] = Field(
        ...,
        description="Canon 4 §27 (C4-038): MOAC evidence must come from an "
                    "uncurated sample. Curated benchmarks are INADMISSIBLE — "
                    "the type refuses them at construction. Owner Ruling "
                    "2026-08-25T23:30Z Q2: 'uncurated_registry_sample' is the "
                    "purpose-safe default (Registry census facts, "
                    "structure-only); 'uncurated_estate_sample' requires "
                    "evidence_purpose_id populated.",
    )
    evidence_purpose_id: Optional[str] = Field(
        default=None,
        description="Required when evidence_source_kind == "
                    "'uncurated_estate_sample'. Named purpose on record that "
                    "permits record-content sampling under the chokepoint. If "
                    "no purpose exists for the pass, name the gap rather than "
                    "sampling (Owner Ruling 2026-08-25T23:30Z Q2).",
    )
    accuracy_uncurated: MoacCriterion = Field(
        ...,
        description="§26.1 · Accuracy on the tenant's uncurated measured "
                    "composition (Doc 1 §4.10).",
    )
    coverage_strata: MoacCriterion = Field(
        ...,
        description="§26.2 · Coverage across strata Mtafiti has measured.",
    )
    refusal_behaviour: MoacCriterion = Field(
        ...,
        description="§26.3 · Refusal behaviour under Solva-pattern (§17) — "
                    "measured refuse-rate on out-of-scope prompts.",
    )
    provenance_integrity: MoacCriterion = Field(
        ...,
        description="§26.4 · Provenance integrity of the training data "
                    "(Doc 1 §4.9).",
    )
    cost_per_operation: MoacCriterion = Field(
        ...,
        description="§26.5 · Cost per operation, measured on real load.",
    )
    time_to_answer_p95: MoacCriterion = Field(
        ...,
        description="§26.6 · Time to answer at 95th percentile, measured "
                    "under the platform's load pattern.",
    )
    training_lineage_resolved: bool = Field(
        ...,
        description="Canon 4 §28 (C4-039): every adapter carries its full "
                    "training lineage back to rights-held source material. "
                    "Unresolved lineage = defect, doesn't ship. Admission "
                    "refuses if this is False.",
    )
    training_lineage_note: str = Field(
        ...,
        min_length=1,
        description="Plain-language sentence naming the lineage's terminus "
                    "(the rights-held source material) OR why it can't be "
                    "resolved (in which case admission will refuse).",
    )
    computed_at: str = Field(
        ...,
        min_length=1,
        description="ISO-8601 UTC. When the MOAC was constructed (i.e., when "
                    "all six criteria had been measured on this candidate). "
                    "Convention-anchored to MiningPlan.generated_at + "
                    "AdmissionRefusal_v0.computed_at.",
    )
