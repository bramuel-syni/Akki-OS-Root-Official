"""Read owner policy; consume server-owned facts. No endpoint accepts these facts as authority."""
from decimal import Decimal
import math
from typing import Literal
from pydantic import Field, ValidationError
from services.activation.models import Frozen, Text, Hash
from services.activation.schema import owner_artifact, POLICY_SHA

POLICY = owner_artifact("owner_crossing_v1_1.json", POLICY_SHA)


class ExternalCrossing(Frozen):
    uncontrolled: Literal["refused", "masked_permitted"]
    controlled_exception: Literal["unavailable", "available_by_ceremony"]


class CrossingContext(Frozen):
    estate_id: Text
    request_sha256: Hash
    custody_class: Literal["uncontrolled", "controlled"]
    assessment_state: Literal["assessed", "unassessed"]
    destination: Literal["local", "frontier"]
    external_crossing: ExternalCrossing
    purpose_authority_ref: Text | None = None
    classification_ref: Text | None = None
    policy_ref: Text | None = None
    ceremony_ref: Text | None = None
    ceremony_estate_id: Text | None = None
    ceremony_class: Text | None = None
    call_authority_ref: Text | None = None
    call_request_sha256: Hash | None = None
    call_estate_id: Text | None = None
    call_class: Text | None = None
    disclosure_authority_ref: Text | None = None
    spend_authority_ref: Text | None = None
    expires_epoch: int = Field(gt=0)
    external_cost_usd: Decimal | None = None
    external_budget_usd: Decimal | None = None
    evidence_mode: Literal["measured", "MOCKED"]
    objective_kind: Literal["entity_knowledge", "other"] = "other"


class CrossingDecision(Frozen):
    allowed: bool = False
    reason_code: str
    mask_required: bool = False
    execution_authorized: Literal[False] = False
    effective_custody: Literal["uncontrolled", "controlled"]
    policy_sha256: Hash = POLICY_SHA


def decide_crossing(context, now_epoch):
    if type(now_epoch) not in (int, float) or not math.isfinite(now_epoch):
        raise ValueError("A finite server clock is required.")
    if not isinstance(context, CrossingContext):
        raise ValueError("Only a typed, server-owned crossing context is accepted.")
    try:
        c = CrossingContext.model_validate_json(context.model_dump_json())
    except (ValueError, TypeError, ValidationError):
        return CrossingDecision(reason_code="CROSSING_CONTEXT_INVALID", effective_custody="controlled")
    custody = "controlled" if c.assessment_state == "unassessed" else c.custody_class
    def deny(reason):
        return CrossingDecision(reason_code=reason, effective_custody=custody)
    if c.evidence_mode != "measured" or c.expires_epoch <= now_epoch:
        return deny("CROSSING_EVIDENCE_UNAVAILABLE")
    if c.assessment_state != "assessed":
        return deny("CLASSIFICATION_UNASSESSED")
    if not all((c.policy_ref, c.classification_ref, c.purpose_authority_ref)):
        return deny("CROSSING_AUTHORITY_INCOMPLETE")
    if c.destination == "frontier":
        # Canonical all-class refusal replaces the old scalar deny row. A single
        # subdial never implicitly widens the other independent class permission.
        if c.external_crossing.uncontrolled == "refused" and c.external_crossing.controlled_exception == "unavailable":
            return deny("EXTERNAL_CROSSING_REFUSED")
        if not c.disclosure_authority_ref or not c.spend_authority_ref:
            return deny("DISCLOSURE_OR_SPEND_AUTHORITY_MISSING")
        if (c.external_cost_usd is None or c.external_budget_usd is None
                or min(c.external_cost_usd, c.external_budget_usd) < 0
                or c.external_cost_usd > c.external_budget_usd):
            return deny("EXTERNAL_SPEND_NOT_ADMITTED")
    candidates = [r for r in POLICY["rows"] if r["material_class"] == custody
                  and r["destination"] == c.destination + "_model"]
    values = c.model_dump()
    for row in candidates:
        for path, expected in row.get("requires_dial", {}).items():
            value = values
            for key in path.split("."):
                value = value.get(key) if isinstance(value, dict) else None
            if value != expected:
                break
        else:
            exception = row.get("per_call_exception")
            if exception:
                if (exception["form"] != "unmasked_for_this_call_only" or exception["route"] != "same_crossing"
                        or exception["condition"] != "entity_knowledge_objective (CC-1)"
                        or c.objective_kind != "entity_knowledge"):
                    return deny("EXCEPTION_OBJECTIVE_NOT_ADMITTED")
                if not (c.ceremony_ref and c.ceremony_estate_id == c.estate_id and c.ceremony_class == custody):
                    return deny("CLASS_SCOPED_CEREMONY_MISSING")
                if not (c.call_authority_ref and c.call_request_sha256 == c.request_sha256
                        and c.call_estate_id == c.estate_id and c.call_class == custody):
                    return deny("PER_CALL_AUTHORITY_MISMATCH")
            elif row["masking"] not in {"none", "none_class_attributes_govern", "custody_sequence_identifiers_masked"}:
                return deny("POLICY_OBLIGATION_UNRECOGNISED")
            return CrossingDecision(allowed=True, reason_code="CROSSING_OBLIGATIONS_RESOLVED",
                                    effective_custody=custody,
                                    mask_required=row["masking"] == "custody_sequence_identifiers_masked")
    return deny("NO_ADMITTED_CROSSING_ROW")