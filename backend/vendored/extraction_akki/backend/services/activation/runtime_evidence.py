"""Verify the admission ACK against its recorded pre-send envelope and fence."""
import json
from services.activation.runtime_limits import RuntimeEnvelope
from services.ledger_writer.mongo_control import digest
from services.northena.execution_models import Held


async def verify_runtime_ack(receipts, events, request, rows, worker_id):
    if not {"dispatch", "send", "runtime_limits"} <= rows.keys():
        raise Held("NATIVE_RUNTIME_ADMISSION_TRACE_MISSING")
    dispatch, send, record = (rows[k] for k in ("dispatch", "send", "runtime_limits"))
    envelope = RuntimeEnvelope.model_validate_json(json.dumps(record["payload"]["data"]["envelope"]))
    ack_ref = record["payload"]["data"]["ack_ref"]
    ack = await receipts.resolve(ack_ref, kind="observation", request_sha256=request.digest(), events=events)
    from services.activation.native_evidence import Observation
    proof = Observation.model_validate_json(json.dumps(ack.claims))
    ack_event = next(e for e in events if e["row"]["hash"] == ack_ref)
    if (ack.signer_id != worker_id or proof.category != "runtime" or proof.evidence_mode != "measured"
            or proof.context_sha256 != request.digest() or proof.claim_sha256 != digest(envelope.model_dump(mode="json"))
            or envelope.request_sha256 != request.digest() or envelope.fence != dispatch["row"]["seq"]
            or envelope.operation_key != dispatch["payload"]["data"]["operation_key"]
            or not dispatch["row"]["seq"] < record["row"]["seq"] < send["row"]["seq"]
            or ack_event["row"]["seq"] >= record["row"]["seq"] or ack.issued_epoch >= envelope.stop_work_by_epoch):
        raise Held("NATIVE_RUNTIME_ACK_NOT_PROVED")
    return ack_ref