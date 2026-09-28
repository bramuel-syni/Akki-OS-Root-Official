"""TrainingParamsV0 · Doc 17 §A17.3-A17.4 · training_params@v0 recipe seat.

Owner-verbatim spec anchors (from notes/waveB_grounding_brief.md):

    A17.3 [CANON] Lineage extends to configuration.
    Every trained model's registry entry MUST cite the recipe_version
    that trained it. MOAC's lineage criterion (M-d) extends by this
    field, so 'which configuration produced this model' is answered
    by reading the registry, never by asking whoever happened to run
    the job.

    A17.4 [CANON] Revision is DEFAULT-class, but never unevidenced.

    Empty recipe seat (grounding brief line 58):
    'No default recipe exists until the first training run fills it
    through the §3 optimizer-selection protocol (A17.5-A17.6).
    Nothing may pre-populate training_params@v0 by convention,
    template, or engineer judgement — the first value ever written
    to it must carry the measured comparison that produced it.'

Same-commit DoD:
  * ConfigDict(extra='forbid', frozen=True) — in-memory hardening.
  * tests/invariants/training_params_v0.contract_snapshot.json
    is the frozen JSON Schema snapshot at CP5 landing.
  * Parity map bump 60 -> 61 in test_frozen_contract_snapshot_parity.py.

Field shape (per Doc 17 §A17.5-A17.6 four-measured-outputs discipline
and §A17.3 lineage-extends-to-configuration):
  * recipe_version    · unique registry key of the form
                        'training_params@v0/<name>'.
  * base_model_id     · registry id of the base model (Doc 17 §A17.2).
  * optimizer_kind    · 'baseline' or 'muon' (closed grammar as of CP5;
                        A17.5 names Muon as 'the first' candidate).
  * hyperparams       · frozen dict (Any values) of the recipe's
                        configuration; opaque to this contract but
                        recorded verbatim on write.
  * evaluation_sets   · list of eval-set identifiers used by MOAC.
  * budget_cap        · dict with 'wallclock_seconds' + 'gpu_hours';
                        A17.5 'identical compute-budget cap'.
  * comparison_ref    · optimizer_comparison_id that produced this
                        recipe (write-once linkage to A17.5 harness).
  * ratified_at       · ISO-8601 UTC timestamp of owner ruling.
"""
from __future__ import annotations

from typing import Any, Dict, List, Literal

from pydantic import BaseModel, ConfigDict, Field


OPTIMIZER_KINDS: tuple = ("baseline", "muon")


class BudgetCap(BaseModel):
    """Identical compute-budget cap for both arms (A17.5)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    wallclock_seconds: int = Field(..., ge=1)
    gpu_hours: float = Field(..., ge=0.0)


class TrainingParamsV0(BaseModel):
    """Doc 17 §A17.3 · training_params@v0 recipe seat entry.

    Ratified by owner ruling on optimizer_comparison verdict; written
    exactly once per adopted comparison. Never pre-populated.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    recipe_version: str = Field(
        ...,
        min_length=1,
        description="Unique key of the form 'training_params@v0/<name>'.",
    )
    base_model_id: str = Field(
        ...,
        min_length=1,
        description="Registry id of the base model (Doc 17 §A17.2).",
    )
    optimizer_kind: Literal["baseline", "muon"] = Field(
        ...,
        description="Named optimizer that produced this recipe (A17.5 · "
                    "Muon named as 'the first' candidate; grammar closed).",
    )
    hyperparams: Dict[str, Any] = Field(
        default_factory=dict,
        description="Opaque configuration dict; recorded verbatim.",
    )
    evaluation_sets: List[str] = Field(
        ...,
        min_length=1,
        description="Eval-set identifiers used by MOAC for M-a/M-b/M-e.",
    )
    budget_cap: BudgetCap = Field(
        ...,
        description="Compute-budget cap (identical across arms · A17.5).",
    )
    comparison_ref: str = Field(
        ...,
        min_length=1,
        description="optimizer_comparison_id that produced this recipe; "
                    "write-once linkage to A17.5 two-arm harness.",
    )
    ratified_at: str = Field(
        ...,
        min_length=1,
        description="ISO-8601 UTC timestamp of owner ruling adoption.",
    )
