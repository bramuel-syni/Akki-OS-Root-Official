"""Versioned activation sidecars; frozen Canon request and Ledger contracts unchanged."""
from decimal import Decimal, InvalidOperation
from typing import Annotated, Literal
from pydantic import Field, field_validator, model_validator
from services.northena.execution_models import Frozen, Name, Hash, Request
from services.activation.model_proofs import EvaluationStandard


class Quantity(Frozen):
    dimension: Literal["spend", "wall_clock", "scanned_records", "returned_records", "bytes_read", "active_compute", "media_duration"]
    unit: Name
    quantity: Annotated[str, Field(min_length=1, max_length=100)]

    @field_validator("quantity")
    @classmethod
    def finite(cls, v):
        try:
            if v.strip() != v or not Decimal(v).is_finite() or Decimal(v) < 0:
                raise ValueError("Quantity must be finite and nonnegative.")
        except InvalidOperation:
            raise ValueError("Invalid quantity.") from None
        return v


def quantities(values):
    keys = [(v.dimension, v.unit) for v in values]
    single = [v.dimension for v in values if v.dimension != "active_compute"]
    if not keys or len(set(keys)) != len(keys) or len(set(single)) != len(single):
        # active_compute is the one dimension whose unit names the compute class (cpu_seconds, gpu_seconds):
        # a mixed job reserves one entry per class; every other dimension carries exactly one unit.
        raise ValueError("One explicit unit per dimension is required.")
    return {(v.dimension, v.unit): Decimal(v.quantity) for v in values}


class Group(Frozen):
    group: Name
    purpose: Literal["scope", "expenditure", "census", "extraction", "answering", "training", "evaluation"]
    members: Annotated[tuple[Name, ...], Field(min_length=1, max_length=1000)]
    quorum: Annotated[int, Field(gt=0)]

    @model_validator(mode="after")
    def unique(self):
        if len(set(self.members)) != len(self.members) or self.quorum > len(self.members):
            raise ValueError("Invalid group membership/quorum.")
        return self


class Plan(Frozen):
    request: Request
    groups: Annotated[tuple[Group, ...], Field(min_length=2, max_length=100)]
    purposes: Annotated[tuple[Literal["census", "extraction", "answering", "training", "evaluation"], ...], Field(min_length=1)]
    acceptance_script_sha256: Hash
    snapshot_hashes: Annotated[tuple[Hash, ...], Field(min_length=1, max_length=1000)]
    limits: tuple[Quantity, ...]
    allocation_ref: Hash
    worker_ref: Hash
    terms_ref: Name
    policy_epoch: Annotated[int, Field(ge=0)]
    dial_versions: dict[str, Name]
    policy_versions: dict[str, Name]
    termination_grace_seconds: Annotated[int, Field(gt=0)]
    catalog_model_identifier: Name | None = None
    catalog_access_class: Literal["local_served", "customer_model", "customer_key", "reseller_frontier"] | None = None
    evaluation_standard: EvaluationStandard | None = None

    @model_validator(mode="after")
    def complete(self):
        bounds = quantities(self.limits)
        if len(set(self.snapshot_hashes)) != len(self.snapshot_hashes):
            raise ValueError("Snapshot commitments must be unique.")
        needed = {"source": {"census", "extraction"}, "skill": {"answering"},
                  "training": {"training", "evaluation"}, "evaluation": {"evaluation"}}[self.request.kind]
        if (len(set(self.purposes)) != len(self.purposes) or
                not (bool(set(self.purposes) & needed) if self.request.kind == "source" else needed <= set(self.purposes))):
            raise ValueError("Explicit operation purposes required.")
        required = {"scope", "expenditure"} | {
            "source": set(), "skill": {"answering"}, "training": {"training", "evaluation"},
            "evaluation": {"evaluation"}}[self.request.kind]
        if not required <= {g.purpose for g in self.groups} or len({g.group for g in self.groups}) != len(self.groups):
            raise ValueError("Independent scope/expenditure/purpose groups required.")
        if not {"spend", "wall_clock"} <= {k[0] for k in bounds} or ("wall_clock", "seconds") not in bounds:
            raise ValueError("Spend and inclusive runtime ceilings required.")
        if bounds[("wall_clock", "seconds")] <= self.termination_grace_seconds:
            raise ValueError("Termination must fit inside runtime ceiling.")
        if self.request.kind == "source" and ("scanned_records", "records") not in bounds:
            raise ValueError("Source scans must be bounded.")
        if set(self.dial_versions) != {"custody_floor", "approving_authority", "external_crossing", "disclosure_counterparties"}:
            raise ValueError("Owner input dial versions required.")
        if set(self.policy_versions) != {"crossing_decision_table", "acceptance_standard", "cleanliness_pack"}:
            raise ValueError("Owner input policy versions required.")
        if (self.catalog_model_identifier is None) != (self.catalog_access_class is None):
            raise ValueError("Catalogue selection must be paired.")
        if self.request.kind in {"training", "evaluation"} and self.evaluation_standard is None:
            raise ValueError("Training/evaluation requires the predeclared protected split and six-criterion mapping.")
        return self


class Approval(Frozen):
    plan_ref: Hash
    group: Name
    decision: Literal["approved", "refused"]
    reason: Name


class Allocation(Frozen):
    limits: tuple[Quantity, ...]
    terms_ref: Name

    @model_validator(mode="after")
    def checked(self):
        quantities(self.limits)
        return self


class Worker(Frozen):
    runtime_id: Name
    executor_version: Name
    kinds: tuple[Literal["source", "skill", "training", "evaluation"], ...]
    enforced_dimensions: tuple[Name, ...]
    enforcement_protocol: Literal["akki.runtime.limits/1"]
    implementation_workspace_touched_data: Literal[False]


class Revocation(Frozen):
    target_ref: Hash
    reason_code: Name


def validate_claims(receipt):
    import json
    model = {"plan": Plan, "approval": Approval, "allocation": Allocation,
             "worker": Worker, "revocation": Revocation}.get(receipt.kind)
    if model is not None:
        parsed = model.model_validate_json(json.dumps(receipt.claims))
        if receipt.kind == "plan" and (parsed.request.digest() != receipt.request_sha256 or
                parsed.request.tenant_id != receipt.tenant_id or parsed.request.scope_refs != receipt.scope_refs):
            raise ValueError("Plan receipt binding mismatch.")
        return parsed
    if receipt.kind == "observation":
        from services.activation.native_evidence import Observation
        return Observation.model_validate_json(json.dumps(receipt.claims))
    if receipt.kind == "certificate":
        from services.activation.native_evidence import CertificateSeal
        return CertificateSeal.model_validate(receipt.claims)
    return receipt.claims