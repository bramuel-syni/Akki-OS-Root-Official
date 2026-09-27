"""Certificate assertions joined to actual execution/registry/reservation records."""
from decimal import Decimal, InvalidOperation
from services.northena.execution_models import Held
from services.activation.record_shapes import quantities


def usage_totals(values):
    totals = {}
    try:
        for value in values:
            unit, quantity = value["unit"], Decimal(str(value["quantity"]))
            if not isinstance(unit, str) or not unit or not quantity.is_finite() or quantity < 0:
                raise Held("CERTIFICATE_NATIVE_USAGE_INVALID")
            totals[unit] = totals.get(unit, Decimal(0)) + quantity
    except (InvalidOperation, KeyError, TypeError, ValueError):
        raise Held("CERTIFICATE_NATIVE_USAGE_INVALID") from None
    return totals


def verify_native_completion(events, request, d, proofs):
    rows = {e["payload"].get("slot"): e for e in events if
            e["row"]["resource_type"] == "execution_flow" and
            e["payload"].get("request_sha256") == request.digest()}
    if not {"registry", "metered", "terminal", "send", "runtime_limits"} <= rows.keys():
        raise Held("CERTIFICATE_NATIVE_COMPLETION_MISSING")
    from services.northena.execution_observations import facts, TERMINAL_STATES
    observed = [e["payload"]["data"]["result"] for key,e in rows.items()
                if key.startswith("observation:") and e["payload"]["data"]["result"]["state"] in TERMINAL_STATES]
    for slot in ("worker_outcome", "worker_terminal"):
        if slot in rows:
            observed.append(rows[slot]["payload"]["data"]["result"])
    if not observed or any(facts(value) != facts(observed[0]) for value in observed):
        raise Held("CERTIFICATE_NATIVE_TERMINAL_MISSING_OR_CONFLICTING")
    from services.northena.execution_models import WorkerResult
    import json
    worker_result = WorkerResult.model_validate_json(json.dumps(observed[0]))
    send = rows["send"]["payload"]["data"]
    if (worker_result.state != "complete" or worker_result.evidence_mode != "measured"
            or worker_result.request_sha256 != request.digest()
            or worker_result.operation_key != send.get("operation_key") or worker_result.fence != send.get("fence")
            or worker_result.executor_id != proofs["runtime"][1].signer_id
            or not any(a.sha256 == d["output"]["artefact_hash"] for a in worker_result.artifacts)):
        raise Held("CERTIFICATE_NATIVE_WORKER_RESULT_MISMATCH")
    registry, meter, final = (rows[k]["payload"]["data"] for k in ("registry", "metered", "terminal"))
    if meter.get("terms_ref") != d["usage"]["terms_identifier"]:
        raise Held("CERTIFICATE_NATIVE_METERING_TERMS_MISMATCH")
    if (final["phase"] != "ready" or any(v.get("evidence_mode") != "measured" for v in (registry, meter, final))
            or not any(a["sha256"] == d["output"]["artefact_hash"] for a in registry["artifacts"])):
        raise Held("CERTIFICATE_NATIVE_OUTPUT_MISMATCH")
    if d["output"]["registry_entry_id"] not in {r["receipt_id"] for r in registry["records"]}:
        raise Held("CERTIFICATE_NATIVE_REGISTRY_MISMATCH")
    if (usage_totals(meter["usage"]) != usage_totals(d["usage"]["measured_quantities"])
            or usage_totals(meter["usage"]) != usage_totals([v.model_dump() for v in worker_result.usage])):
        raise Held("CERTIFICATE_NATIVE_USAGE_MISMATCH")
    reservation = next((e for e in events if e["row"]["hash"] == d["usage"]["reservation_ref"]
                        and e["row"]["event_type"] == "activation.reserved"), None)
    if reservation is None or reservation["payload"]["request_sha256"] != request.digest():
        raise Held("CERTIFICATE_RESERVATION_UNRESOLVED")
    settlement = next((e for e in events if e["row"]["event_type"] == "activation.settled" and
                       e["payload"]["reservation_ref"] == reservation["row"]["hash"]), None)
    if settlement is None or settlement["row"]["reason_code"] != "USAGE_RECONCILED":
        raise Held("CERTIFICATE_RESERVATION_NOT_RECONCILED")
    measured = quantities(proofs["measurements"][0].quantities)
    if (not proofs["measurements"][0].terminal or
            proofs["measurements"][0].reservation_ref != reservation["row"]["hash"] or
            measured != {(q["dimension"], q["unit"]): Decimal(q["quantity"]) for q in settlement["payload"]["amounts"]} or
            measured != {(q["dimension"], q["unit"]): Decimal(str(q["observed"])) for q in d["limits"]["dimensions"]}):
        raise Held("CERTIFICATE_RESERVATION_MEASUREMENTS_MISMATCH")
    if reservation["row"]["seq"] >= rows["send"]["row"]["seq"]:
        raise Held("CERTIFICATE_RESERVATION_AFTER_EFFECT")
    approvals = [d["authority"]["scope"], d["authority"]["expenditure"], *d["authority"]["purpose_specific"]]
    before_effect = {v["receipt_ref"] for g in approvals for v in g["decisions"]}
    before_effect.add(reservation["payload"]["plan_ref"])
    if any(e["row"]["seq"] >= rows["send"]["row"]["seq"] for e in events if e["row"]["hash"] in before_effect):
        raise Held("CERTIFICATE_CONTROL_RECORDED_AFTER_EFFECT")
    if request.kind == "source" and measured.get(("scanned_records", "records"), Decimal(-1)) < d["output"]["denominator_count"]:
        raise Held("CERTIFICATE_SCANNED_DENOMINATOR_MISMATCH")
    from datetime import datetime
    from services.activation.runtime_limits import RuntimeEnvelope
    admission = RuntimeEnvelope.model_validate_json(json.dumps(rows["runtime_limits"]["payload"]["data"]["envelope"]))
    start = datetime.fromisoformat(d["identity"]["run_started_at"].replace("Z", "+00:00")).timestamp()
    end = datetime.fromisoformat(d["identity"]["run_ended_at"].replace("Z", "+00:00")).timestamp()
    if (admission.request_sha256 != request.digest() or admission.reservation_ref != reservation["row"]["hash"] or
            admission.operation_key != rows["send"]["payload"]["data"].get("operation_key") or
            admission.fence != rows["send"]["payload"]["data"].get("fence") or
            not admission.starts_epoch <= start <= end <= admission.terminate_by_epoch or
            measured.get(("wall_clock", "seconds"), Decimal(-1)) < Decimal(str(end-start))):
        raise Held("CERTIFICATE_RUNTIME_WINDOW_MISMATCH")
    return {reservation["row"]["hash"], settlement["row"]["hash"],
            d["output"]["registry_entry_id"], *[e["row"]["hash"] for e in rows.values()]}