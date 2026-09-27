"""An independent evaluation is a governed run, not just a second ready label."""
import json
from services.activation.approvals import approved_plan
from services.activation.record_shapes import quantities
from services.activation.runtime_limits import RuntimeEnvelope
from services.northena.execution_models import WorkerResult, Held
from services.northena.execution_observations import facts, TERMINAL_STATES


async def verify_evaluation_operation(receipts, events, request, parent_plan, evaluator_id):
    rows = {e["payload"].get("slot"): e for e in events if e["row"]["resource_type"] == "execution_flow"
            and e["row"]["run_id"] == request.request_id}
    required = {"request", "dispatch", "send", "runtime_limits", "registry", "metered", "terminal"}
    if not required <= rows.keys() or any(e["payload"].get("request_sha256") != request.digest() for e in rows.values()):
        raise Held("EVALUATION_GOVERNED_EXECUTION_INCOMPLETE")
    if request.tenant_id != parent_plan.request.tenant_id or not set(request.scope_refs) <= set(parent_plan.request.scope_refs):
        raise Held("EVALUATION_SCOPE_NOT_ADMITTED")
    plan, plan_ref, approvals, _, _ = await approved_plan(receipts, request)
    if plan.evaluation_standard != parent_plan.evaluation_standard:
        raise Held("EVALUATION_ADOPTED_STANDARD_MISMATCH")
    worker = await receipts.resolve(plan.worker_ref, kind="worker", events=events)
    parent_worker = await receipts.resolve(parent_plan.worker_ref, kind="worker", events=events)
    if (worker.signer_id != evaluator_id or worker.signer_id == parent_worker.signer_id
            or worker.claims["runtime_id"] == parent_worker.claims["runtime_id"]):
        raise Held("EVALUATION_INDEPENDENT_WORKER_NOT_ADMITTED")
    from services.activation.runtime_evidence import verify_runtime_ack
    ack_ref = await verify_runtime_ack(receipts, events, request, rows, evaluator_id)
    envelope = RuntimeEnvelope.model_validate_json(json.dumps(rows["runtime_limits"]["payload"]["data"]["envelope"]))
    dispatch, send = rows["dispatch"], rows["send"]
    if (envelope.request_sha256 != request.digest() or envelope.plan_ref != plan_ref or envelope.limits != plan.limits
            or envelope.runtime_id != worker.claims["runtime_id"] or envelope.operation_key != dispatch["payload"]["data"]["operation_key"]
            or envelope.fence != dispatch["row"]["seq"] or envelope.operation_key != send["payload"]["data"].get("operation_key")
            or envelope.fence != send["payload"]["data"].get("fence")):
        raise Held("EVALUATION_RUNTIME_ADMISSION_MISMATCH")
    reservation = next((e for e in events if e["row"]["hash"] == envelope.reservation_ref
                        and e["row"]["event_type"] == "activation.reserved"), None)
    if (reservation is None or reservation["payload"]["request_sha256"] != request.digest()
            or reservation["payload"]["plan_ref"] != plan_ref or reservation["row"]["seq"] >= send["row"]["seq"]):
        raise Held("EVALUATION_RESERVATION_NOT_PROVED")
    if any(e["row"]["seq"] >= send["row"]["seq"] for e in events if e["row"]["hash"] in {*approvals, plan_ref}):
        raise Held("EVALUATION_APPROVAL_RECORDED_AFTER_EFFECT")
    definitive = [e["payload"]["data"]["result"] for key,e in rows.items()
                  if key in {"worker_outcome", "worker_terminal"} or key.startswith("observation:")
                  and e["payload"]["data"]["result"]["state"] in TERMINAL_STATES]
    if not definitive or any(facts(v) != facts(definitive[0]) for v in definitive):
        raise Held("EVALUATION_WORKER_OUTCOME_CONFLICT")
    result = WorkerResult.model_validate_json(json.dumps(definitive[0]))
    meter = rows["metered"]["payload"]["data"]
    registry = rows["registry"]["payload"]["data"]
    if (result.state != "complete" or result.evidence_mode != "measured" or result.executor_id != evaluator_id
            or result.request_sha256 != request.digest() or result.operation_key != envelope.operation_key or result.fence != envelope.fence
            or meter.get("evidence_mode") != "measured" or meter.get("terms_ref") != plan.terms_ref
            or meter.get("usage") != [v.model_dump() for v in result.usage]):
        raise Held("EVALUATION_RESULT_OR_METERING_MISMATCH")
    if (registry.get("evidence_mode") != "measured" or not registry.get("records")
            or {(v.ref, v.sha256) for v in result.artifacts} != {(v["ref"], v["sha256"]) for v in registry["artifacts"]}):
        raise Held("EVALUATION_REGISTERED_REPORT_MISMATCH")
    settled = next((e for e in events if e["row"]["event_type"] == "activation.settled"
                    and e["payload"]["reservation_ref"] == envelope.reservation_ref), None)
    if settled is None or settled["row"]["reason_code"] != "USAGE_RECONCILED":
        raise Held("EVALUATION_USAGE_NOT_RECONCILED")
    observation = await receipts.resolve(settled["payload"]["observation_ref"], kind="observation",
                                        request_sha256=request.digest(), events=events)
    from services.activation.native_evidence import Observation
    proof = Observation.model_validate_json(json.dumps(observation.claims))
    if (observation.signer_id != evaluator_id or proof.category != "measurements" or not proof.terminal
            or proof.evidence_mode != "measured" or proof.reservation_ref != envelope.reservation_ref
            or [v.model_dump() for v in proof.quantities] != settled["payload"]["amounts"]):
        raise Held("EVALUATION_MEASUREMENT_PROVENANCE_MISMATCH")
    limits, measured = quantities(plan.limits), quantities(proof.quantities)
    if set(limits) != set(measured) or any(measured[k] > limits[k] for k in limits):
        raise Held("EVALUATION_LIMIT_EXCEEDED")
    return {plan_ref, *approvals, plan.worker_ref, plan.allocation_ref, ack_ref,
            reservation["row"]["hash"], settled["row"]["hash"], settled["payload"]["observation_ref"],
            *[e["row"]["hash"] for e in rows.values()]}