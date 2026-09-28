"""northena_ledger_row@v0 — the contract-grade Ledger row (Doc 05 §7.2).

Adapted for Extraction-Akki from `Akki-OS-V1/backend/contracts/northena_ledger.py`.
Persistence in this estate is phase0/ JSON (not MongoDB); the row's shape
and stage/decision consistency rule are the SAME as the donor's — the
contract is preserved verbatim; only the collection name references
the phase0 directory path.

W4 addition: `thinklab_objective` is admitted as a valid artifact_type
alongside donor's `portfolio_mandate` and `objective_request`, because
ThinkLab session objectives freeze here.

Stage / decision consistency (Doc 05 §7.2 verbatim):
  * admit     ∈ { admitted, refused }
  * gate      ∈ { warm, fresh, refused }
  * converge  ∈ { terminate_success, terminate_budget, continue }
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


NORTHENA_LEDGER_COLLECTION = "northena_ledger_rows"


class LedgerArtifactRef(BaseModel):
    """§7.2: { artifact_type, artifact_id, version }."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    artifact_type: Literal[
        "portfolio_mandate",
        "objective_request",
        "thinklab_objective",
    ]
    artifact_id: str
    version: str


_ALLOWED: Dict[str, set] = {
    "admit":    {"admitted", "refused"},
    "gate":     {"warm", "fresh", "refused"},
    "converge": {"terminate_success", "terminate_budget", "continue"},
}


class LedgerRow(BaseModel):
    """§7.2 · the contract-grade Ledger row."""

    model_config = ConfigDict(extra="forbid")

    row_id: str = Field(default_factory=lambda: f"led-{uuid.uuid4().hex[:12]}",
                        description="Stable identity for the ledger row (identity-join key).")
    run_id: str = Field(..., description="uuid — one run has one closed Ledger.")
    trace_id: str = Field(..., description="Joins ledger to unit-level intelligence.")
    stage: Literal["admit", "gate", "converge"]
    decision: Literal[
        "admitted", "refused",
        "warm", "fresh",
        "terminate_success", "terminate_budget", "continue",
    ]
    reason: str = Field(..., description="Deterministic reason string.")
    artifact_ref: LedgerArtifactRef
    lawful_basis_ref: str
    stamp_audit: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Permissive side-channel per §7.3 · absorbs Solva traces, "
                    "gate receipts, refusal envelopes without mutating the "
                    "frozen row contract.",
    )
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @model_validator(mode="after")
    def _stage_decision_consistent(self) -> "LedgerRow":
        allowed = _ALLOWED[self.stage]
        if self.decision not in allowed:
            raise ValueError(
                f"stage={self.stage!r} does not admit decision={self.decision!r}; "
                f"allowed for this stage: {sorted(allowed)}"
            )
        return self

    @classmethod
    def new(cls, **kwargs) -> "LedgerRow":
        """Construct with `row_id` and `at` auto-populated."""
        return cls(**kwargs)

    def to_json(self) -> Dict[str, Any]:
        """JSON-serializable form for phase0/ persistence."""
        return self.model_dump(mode="json")
