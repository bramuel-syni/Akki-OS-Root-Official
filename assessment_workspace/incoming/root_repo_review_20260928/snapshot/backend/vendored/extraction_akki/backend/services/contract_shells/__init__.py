"""services.contract_shells — W1b · CP5 · L2/L4 generic contract shells.

Owner directive: "the L2/L4 contract shells (TargetOutcome_v0,
StratumAcceptance, CommissionSpec, Milestone, WorkerLane, WorkerJD)
is genuinely generic — keep as-is."

All shells are frozen pydantic v2 models. No behavior, no I/O, no
domain-specific fields. Downstream waves bind specific instances at
mount time.
"""
from __future__ import annotations

import re
from typing import Tuple

from pydantic import BaseModel, Field, field_validator


_ISO_Z = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$")


class TargetOutcome_v0(BaseModel):
    model_config = {"frozen": True, "extra": "forbid"}
    outcome_id: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    acceptance_ref: str = Field(..., min_length=1)


class StratumAcceptance(BaseModel):
    model_config = {"frozen": True, "extra": "forbid"}
    acceptance_id: str = Field(..., min_length=1)
    stratum_id: str = Field(..., min_length=1)
    evidence_class: str = Field(..., min_length=1)
    evidence_ref: str = Field(..., min_length=1)

    @field_validator("evidence_class")
    @classmethod
    def _closed_evidence_enum(cls, v: str) -> str:
        allowed = {"observed", "projected"}
        if v not in allowed:
            raise ValueError(
                f"evidence_class {v!r} must be one of {sorted(allowed)!r}"
            )
        return v


class CommissionSpec(BaseModel):
    model_config = {"frozen": True, "extra": "forbid"}
    commission_id: str = Field(..., min_length=1)
    target_ref: str = Field(..., min_length=1)
    plan_ref: str = Field(..., min_length=1)
    opened_at_utc: str = Field(..., min_length=1)

    @field_validator("opened_at_utc")
    @classmethod
    def _iso_z(cls, v: str) -> str:
        if not _ISO_Z.match(v):
            raise ValueError(
                f"opened_at_utc must be ISO-8601 Z, got {v!r}"
            )
        return v


class Milestone(BaseModel):
    model_config = {"frozen": True, "extra": "forbid"}
    milestone_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    expected_at_utc: str = Field(..., min_length=1)
    output_kind: str = Field(..., min_length=1)

    @field_validator("expected_at_utc")
    @classmethod
    def _iso_z(cls, v: str) -> str:
        if not _ISO_Z.match(v):
            raise ValueError(
                f"expected_at_utc must be ISO-8601 Z, got {v!r}"
            )
        return v


class WorkerLane(BaseModel):
    model_config = {"frozen": True, "extra": "forbid"}
    lane_id: str = Field(..., min_length=1)
    capacity: int = Field(..., gt=0)
    kinds: Tuple[str, ...] = Field(...)

    @field_validator("kinds")
    @classmethod
    def _kinds_shape(cls, v: Tuple[str, ...]) -> Tuple[str, ...]:
        if not v:
            raise ValueError("kinds must be non-empty")
        for k in v:
            if not isinstance(k, str) or not k:
                raise ValueError(f"kind {k!r} must be a non-empty str")
        return v


class WorkerJD(BaseModel):
    model_config = {"frozen": True, "extra": "forbid"}
    jd_id: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1)
    capabilities: Tuple[str, ...] = Field(...)

    @field_validator("capabilities")
    @classmethod
    def _caps_shape(cls, v: Tuple[str, ...]) -> Tuple[str, ...]:
        if not v:
            raise ValueError("capabilities must be non-empty")
        for c in v:
            if not isinstance(c, str) or not c:
                raise ValueError(f"capability {c!r} must be a non-empty str")
        return v


__all__ = [
    "TargetOutcome_v0",
    "StratumAcceptance",
    "CommissionSpec",
    "Milestone",
    "WorkerLane",
    "WorkerJD",
]
