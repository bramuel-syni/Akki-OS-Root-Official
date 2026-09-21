"""BaselineLine_v0 — Doc 14 §32 · CA1-004 (Addendum §1).

The training-run register row that names the licence-verified starting
model for a given training pass. Per Owner Order 2026-08-25 Addendum
§1 CA1-004: 'Baseline line names licence-verified starting model per
training run.'

Freeze contract: 39th frozen contract post-W7 CP5 landing. Snapshot
bijection enforced by test_frozen_contract_snapshot_parity.py +
test_composed_conclusion_snapshot_parity_at_18 (count 38 → 39).

Relationship to other contracts:
  * `starting_model_id` MUST reference a model already in model_registry
    (attest_model check fires at record construction · CP5 service).
  * `training_run_id` binds to admission records emitted by
    services/model_admission/ceremony.py — one baseline line per run.
  * License note on the baseline line MIRRORS the starting model's
    license_note field on record in model_registry (audit uniformity).

Registry-entry-shape drift on model_registry.re_check_due_at (CA1-011
W7 half) is documented separately in
services/model_recheck/status.py; not part of this contract.
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BaselineLine_v0(BaseModel):
    """Training-run baseline line · CA1-004."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    baseline_line_id: str = Field(
        ...,
        min_length=1,
        pattern=r"^bl_[a-z0-9_-]+$",
        description="Stable surrogate id for this line. Convention: "
                    "'bl_<training_run_id>' so retrieval joins with the "
                    "training-run record without a separate lookup table.",
    )
    training_run_id: str = Field(
        ...,
        min_length=1,
        description="Identifies the training run whose starting model this "
                    "line names. Must match a training-run record on file.",
    )
    starting_model_id: str = Field(
        ...,
        min_length=1,
        description="model_id of the licence-verified starting model — must "
                    "already be present in services/model_registry (attest_model "
                    "fires at BaselineLine construction · CP5 service).",
    )
    starting_model_license_note: str = Field(
        ...,
        min_length=1,
        description="License note verbatim from the model_registry entry at "
                    "the moment this line was authored (audit uniformity · "
                    "Canon 1 §4.9).",
    )
    authored_at: str = Field(
        ...,
        min_length=1,
        description="ISO-8601 UTC. When the baseline line was recorded.",
    )
    authored_by: str = Field(
        ...,
        min_length=1,
        description="Actor id (owner / operator / system) that authored the "
                    "line. Facts-not-claims (Canon 1 §4.4).",
    )
    notes: Optional[str] = Field(
        default=None,
        description="Optional free-text note. Never carries credentials "
                    "(Owner Order 2026-08-25 §4).",
    )
