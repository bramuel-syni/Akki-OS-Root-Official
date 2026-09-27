"""Metadata-only execution contracts. No source bytes, models, queries or secrets."""
from decimal import Decimal, InvalidOperation
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator, model_validator
from services.ledger_writer.mongo_control import digest

Name = Annotated[str, Field(min_length=1, max_length=512, pattern=r"^\S(?:.*\S)?$")]
Hash = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
Handle = Annotated[str, Field(max_length=512, pattern=r"^akki://[A-Za-z0-9][A-Za-z0-9._~:/-]*$")]
Kind = Literal["source", "skill", "training", "evaluation"]
Engine = Literal["mtafiti", "synisense", "solva", "targeta"]
Class = Literal["non_factual", "utterance", "fact"]


class Frozen(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)


class Held(Exception):
    def __init__(self, reason_code: str):
        if not isinstance(reason_code, str) or not reason_code.strip():
            raise ValueError("A hold must have a reason.")
        self.reason_code = reason_code
        super().__init__(reason_code)


class Request(Frozen):
    request_id: Name
    tenant_id: Name
    principal_id: Name
    kind: Kind
    engine: Engine
    objective_sha256: Hash
    input_refs: Annotated[tuple[Handle, ...], Field(min_length=1, max_length=1000)]
    scope_refs: Annotated[tuple[Name, ...], Field(min_length=1, max_length=1000)]
    deadline_epoch: Annotated[int, Field(gt=0)]
    result_floor: Class | None = None

    @model_validator(mode="after")
    def bound_engine(self):
        allowed = {"source": {"mtafiti", "synisense"}, "skill": {"solva"},
                   "training": {"targeta"}, "evaluation": {"targeta"}}
        if self.engine not in allowed[self.kind]:
            raise ValueError("Operation must use its governing engine.")
        if len(set(self.scope_refs)) != len(self.scope_refs) or len(set(self.input_refs)) != len(self.input_refs):
            raise ValueError("Duplicate scope/input members are not admitted.")
        if self.kind == "skill" and self.result_floor is None:
            raise ValueError("Skill floor must come from provisioning.")
        return self

    def digest(self):
        return digest(self.model_dump(mode="json"))


class Authority(Frozen):
    authority_ref: Name
    request_sha256: Hash
    tenant_id: Name
    principal_id: Name
    scope_refs: tuple[Name, ...]
    engine: Engine
    expires_epoch: Annotated[int, Field(gt=0)]
    terms_ref: Name
    policy_epoch: Annotated[int, Field(ge=0)]


class Artifact(Frozen):
    ref: Handle
    sha256: Hash
    size_bytes: Annotated[int, Field(ge=0)]
    tenant_id: Name
    class_label: Class


class Usage(Frozen):
    unit: Name
    quantity: Annotated[str, Field(min_length=1, max_length=100)]

    @field_validator("quantity")
    @classmethod
    def finite_quantity(cls, value):
        try:
            number = Decimal(value)
            if not number.is_finite() or number < 0 or value.strip() != value:
                raise ValueError("Measured quantity must be finite and nonnegative.")
        except InvalidOperation as exc:
            raise ValueError("Invalid measured quantity.") from exc
        return value


class WorkerResult(Frozen):
    operation_key: Name
    request_sha256: Hash
    executor_id: Name
    fence: Annotated[int, Field(gt=0)]
    state: Literal["accepted", "running", "complete", "failed", "cancelled", "unknown"]
    receipt_ref: Handle
    artifacts: tuple[Artifact, ...]
    usage: tuple[Usage, ...] | None
    evidence_mode: Literal["measured", "MOCKED"]


class RunView(Frozen):
    request_id: Name
    phase: Literal["held", "running", "unknown", "ready", "cancelled", "failed"]
    reason_code: Name
    artifact_refs: tuple[Handle, ...] = ()
    evidence_mode: Literal["unverified", "measured", "MOCKED"] = "unverified"
    usage: tuple[Usage, ...] | None = None
    terms_ref: Name | None = None

    @computed_field
    @property
    def execution_verified(self) -> bool:
        return self.phase == "ready" and self.evidence_mode == "measured"