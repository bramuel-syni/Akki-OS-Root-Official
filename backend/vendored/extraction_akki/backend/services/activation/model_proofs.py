"""Model proof consumers: metadata only, never train/evaluate/answer from E1."""
import json
from decimal import Decimal, InvalidOperation
from typing import Literal
from pydantic import field_validator, model_validator
from services.northena.execution_models import Frozen, Name, Hash, Request, Held
from services.ledger_writer.mongo_control import digest

FIELDS = ("accuracy_uncurated", "coverage_strata", "refusal_behaviour", "provenance_integrity",
          "cost_per_operation", "time_to_answer_p95")


class CriterionSpec(Frozen):
    criterion_id: Name
    native_field: Literal["accuracy_uncurated", "coverage_strata", "refusal_behaviour", "provenance_integrity",
                          "cost_per_operation", "time_to_answer_p95"]
    threshold: str
    unit: Name
    method: Name

    @field_validator("threshold")
    @classmethod
    def finite(cls, value):
        try:
            if not Decimal(value).is_finite() or len(value) > 100 or value.strip() != value:
                raise ValueError("A predeclared finite threshold is required.")
        except InvalidOperation:
            raise ValueError("Invalid threshold.") from None
        return value


class EvaluationStandard(Frozen):
    standard_ref: Hash
    held_out_manifest_sha256: Hash
    fixed_epoch: int
    criteria: tuple[CriterionSpec, ...]

    @model_validator(mode="after")
    def six(self):
        if (len(self.criteria) != 6 or {v.native_field for v in self.criteria} != set(FIELDS)
                or len({v.criterion_id for v in self.criteria}) != 6 or self.fixed_epoch <= 0):
            raise ValueError("Map the adopted six native criteria explicitly.")
        return self


class Anchor(Frozen):
    snapshot_sha256: Hash
    anchor_sha256: Hash
    source_receipt_ref: Hash


class Grounding(Frozen):
    query_ref: Name
    answer_sha256: Hash
    anchors: tuple[Anchor, ...]
    context_lost: bool
    context_loss_disclosed: bool


class Evaluation(Frozen):
    evaluation_request_id: Name
    training_request_sha256: Hash
    candidate_artifact_sha256: Hash
    held_out_manifest_sha256: Hash
    moac_card: dict


class Refusal(Frozen):
    request_ref: Hash
    outcome: Literal["refused"]
    reason_code: Literal["OUT_OF_SCOPE", "UNAUTHORISED_MANIFEST_UNIT", "JUNK_STRATUM_UNIT"]


def check_criteria(standard, certificate_acceptance, card):
    from contracts.model_acceptance_card import ModelAcceptanceCard_v0
    native = ModelAcceptanceCard_v0.model_validate(card)
    declared = {c["criterion_id"]: c for c in certificate_acceptance["criteria"]}
    if certificate_acceptance["acceptance_standard_ref"] != standard.standard_ref or set(declared) != {c.criterion_id for c in standard.criteria}:
        raise Held("EVALUATION_ADOPTED_STANDARD_MISMATCH")
    if not native.training_lineage_resolved or (native.evidence_source_kind == "uncurated_estate_sample" and not native.evidence_purpose_id):
        raise Held("EVALUATION_NATIVE_LINEAGE_OR_PURPOSE_MISSING")
    for spec in standard.criteria:
        measured = getattr(native, spec.native_field)
        row = declared[spec.criterion_id]
        values = (measured.measured_value, measured.floor_value, row["measured_value"], row["threshold"])
        if any(type(v) not in (int, float) or not Decimal(str(v)).is_finite() for v in values):
            raise Held("EVALUATION_MEASUREMENT_NOT_NUMERIC")
        actual, threshold = Decimal(str(measured.measured_value)), Decimal(spec.threshold)
        if (Decimal(str(measured.floor_value)) != threshold or Decimal(str(row["threshold"])) != threshold
                or Decimal(str(row["measured_value"])) != actual or measured.unit != spec.unit
                or measured.method_of_measurement != spec.method):
            raise Held("EVALUATION_MEASUREMENT_OR_THRESHOLD_MISMATCH")
        met = actual <= threshold if spec.native_field in FIELDS[-2:] else actual >= threshold
        if row["outcome"] != ("met" if met else "failed"):
            raise Held("EVALUATION_CRITERION_OUTCOME_MISMATCH")
        if certificate_acceptance["decision"] == "admitted" and not met:
            raise Held("EVALUATION_FAILED_CRITERION_RELEASED")


async def verify_model_proofs(receipts, events, request, plan, d, proofs):
    if request.kind == "source":
        return set()
    refusal = proofs.get("refusal")
    expected = {"out_of_scope_question":"OUT_OF_SCOPE", "unauthorised_manifest_unit":"UNAUTHORISED_MANIFEST_UNIT",
                "junk_stratum_unit":"JUNK_STRATUM_UNIT"}[d["evidence"]["refusal_demonstration"]["kind"]]
    if (refusal is None or refusal[0].refusal is None or refusal[0].refusal.reason_code != expected
            or refusal[0].refusal.request_ref != d["evidence"]["refusal_demonstration"]["request_ref"]):
        raise Held("NATIVE_OUT_OF_SCOPE_REFUSAL_NOT_PROVED")
    if request.kind == "skill":
        ground = proofs["skill"][0].grounding
        if (ground is None or not ground.anchors or ground.query_ref != request.input_refs[-1]
                or ground.answer_sha256 != d["output"]["artefact_hash"]
                or ground.context_lost and not ground.context_loss_disclosed):
            raise Held("GROUNDED_SKILL_ANCHORS_OR_CONTEXT_PROOF_MISSING")
        for anchor in ground.anchors:
            source = await receipts.resolve(anchor.source_receipt_ref, kind="observation", events=events)
            if (source.claims.get("category") != "anchor" or anchor.snapshot_sha256 not in plan.snapshot_hashes
                    or source.claims.get("evidence_mode") != "measured"
                    or source.request_sha256 != request.digest()
                    or source.claims.get("claim_sha256") != digest({"snapshot_sha256":anchor.snapshot_sha256,
                        "anchor_sha256":anchor.anchor_sha256,"answer_sha256":ground.answer_sha256,"query_ref":ground.query_ref})):
                raise Held("GROUNDED_SKILL_ANCHOR_SOURCE_MISMATCH")
        if "refusal" not in proofs or not proofs["refusal"][0].source_receipt_refs:
            raise Held("GROUNDED_SKILL_RECEIPTED_REFUSAL_MISSING")
        return {v.source_receipt_ref for v in ground.anchors} | set(proofs["refusal"][0].source_receipt_refs)
    standard, proof = plan.evaluation_standard, proofs["evaluation"][0].evaluation
    if standard is None or proof is None:
        raise Held("INDEPENDENT_EVALUATION_RECORD_MISSING")
    if (proof.training_request_sha256 != request.digest() or proof.candidate_artifact_sha256 != d["output"]["artefact_hash"]
            or proof.held_out_manifest_sha256 != standard.held_out_manifest_sha256):
        raise Held("EVALUATION_ARTIFACT_OR_SPLIT_MISMATCH")
    from datetime import datetime
    if standard.fixed_epoch >= datetime.fromisoformat(d["identity"]["run_started_at"].replace("Z", "+00:00")).timestamp():
        raise Held("EVALUATION_SPLIT_NOT_PREDECLARED")
    rows = {e["payload"].get("slot"): e["payload"].get("data") for e in events if
            e["row"]["resource_type"] == "execution_flow" and e["row"]["run_id"] == proof.evaluation_request_id}
    if not {"request", "registry", "terminal"} <= rows.keys():
        raise Held("INDEPENDENT_EVALUATION_NATIVE_COMPLETION_MISSING")
    evaluation_request = Request.model_validate_json(json.dumps(rows["request"]["request"]))
    if (evaluation_request.kind != "evaluation" or evaluation_request.request_id == request.request_id
            or rows["terminal"].get("phase") != "ready" or rows["terminal"].get("evidence_mode") != "measured"):
        raise Held("INDEPENDENT_EVALUATION_NOT_COMPLETED")
    trained = [e["payload"]["data"] for e in events if e["row"]["resource_type"] == "execution_flow"
               and e["payload"].get("request_sha256") == request.digest() and e["payload"].get("slot") == "registry"]
    artifact_refs = {a["ref"] for row in trained for a in row["artifacts"] if a["sha256"] == proof.candidate_artifact_sha256}
    observations = [v["result"] for key,v in rows.items() if key and key.startswith("observation:") and v.get("result",{}).get("state")=="complete"]
    if (evaluation_request.input_refs[0] not in artifact_refs or not observations or
            observations[-1]["executor_id"] != proofs["evaluation"][1].signer_id):
        raise Held("INDEPENDENT_EVALUATION_NATIVE_ARTIFACT_OR_EXECUTOR_MISMATCH")
    from services.activation.evaluation_joins import verify_evaluation_operation
    evaluation_refs = await verify_evaluation_operation(receipts, events, evaluation_request, plan, proofs["evaluation"][1].signer_id)
    check_criteria(standard, d["release_acceptance"], proof.moac_card)
    release = proofs.get("release")
    if release is None or release[1].signer_id in {proofs["evaluation"][1].signer_id, proofs["training"][1].signer_id}:
        raise Held("SEPARATE_MODEL_RELEASE_DECISION_REQUIRED")
    return evaluation_refs