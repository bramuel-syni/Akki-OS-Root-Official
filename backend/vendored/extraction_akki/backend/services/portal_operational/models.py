"""Strict user intent and explicit requester disclosure (DAP-15/18)."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator


class SubmitRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    objective_text: str = Field(min_length=1, max_length=8000)
    operation: Literal["browse_estate", "connect_workspace", "processed_intelligence",
                       "fine_tune_model", "develop_skills", "download_raw_data"]
    units: list[str] = Field(min_length=1, max_length=50)
    idempotency_key: str = Field(min_length=8, max_length=128)

    @field_validator("objective_text", "idempotency_key")
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError("A nonblank value is required.")
        return value  # Hash the exact frozen objective, not a normalised substitute.

    @field_validator("units")
    @classmethod
    def unique_units(cls, value):
        if len(set(value)) != len(value) or any(not x.strip() or len(x) > 128 for x in value):
            raise ValueError("Units must be distinct, nonblank admitted references.")
        return value


class HistoryEntry(BaseModel):
    at: str
    state: str
    event: str
    reason_code: str
    receipt_hash: str


class WorkView(BaseModel):
    request_id: str
    work_id: str
    objective_text: str
    objective_hash: str
    operation: str
    units: list[str]
    state: str
    lifecycle_state: str
    governing_engine: str
    created_at: str
    reason_code: str
    reason: str
    execution_verified: bool = False
    result: dict | None = None
    permitted_actions: list[str] = Field(default_factory=list)
    history: list[HistoryEntry]


class WorkList(BaseModel):
    principal_id: str
    rows: list[WorkView]
    count: int