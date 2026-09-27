"""Commit result evidence before publication; usage is not an invoice or grant."""
from services.ledger_writer.principal_control import CommandConflict
from services.northena.execution_models import Held, RunView, Usage
from services.northena.execution_validation import checked_artifacts


async def meter(coordinator, request, result, dispatch):
    if result.usage is None or not result.usage:
        raise Held("ACTUAL_USAGE_UNAVAILABLE")
    return await coordinator.journal.append(request, "metered", {
        "terms_ref": dispatch["data"]["authority"]["terms_ref"],
        "worker_receipt_ref": result.receipt_ref,
        "usage": [item.model_dump(mode="json") for item in result.usage],
        "evidence_mode": result.evidence_mode,
    })


async def terminal(coordinator, request, phase, reason, mode, artifacts=()):
    rows = await coordinator.journal.read(request)
    metered = next((row["data"] for row in rows if row["slot"] == "metered"), None)
    data = {"phase": phase, "reason_code": reason, "evidence_mode": mode,
            "artifact_refs": list(artifacts), "usage": metered["usage"] if metered else None,
            "terms_ref": metered["terms_ref"] if metered else None}
    try:
        event = await coordinator.journal.append(request, "terminal", data)
    except CommandConflict:
        event = next(item for item in await coordinator.journal.read(request) if item["slot"] == "terminal")
    value = event["data"]
    if value["phase"] == "ready":
        await coordinator.authorize(request, "retrieve")
    return RunView(request_id=request.request_id, phase=value["phase"],
                   reason_code=value["reason_code"], evidence_mode=value["evidence_mode"],
                   artifact_refs=tuple(value["artifact_refs"]), terms_ref=value.get("terms_ref"),
                   usage=tuple(Usage(**item) for item in value["usage"]) if value.get("usage") is not None else None)


async def complete(coordinator, request, result, dispatch):
    key = dispatch["data"]["operation_key"]
    try:
        await coordinator.authorize(request, "verify")
        verified = checked_artifacts(request, result, await coordinator.artifacts.verify(request, result, key))
    except (Held, ValueError) as exc:
        # Failed eligibility/validation does not erase actual already-consumed work.
        if result.usage:
            await meter(coordinator, request, result, dispatch)
        raise exc if isinstance(exc, Held) else Held("ARTIFACT_VERIFICATION_FAILED")
    await coordinator.journal.append(request, "verify_artifact", {
        "artifacts": [item.model_dump(mode="json") for item in verified],
        "worker_receipt_ref": result.receipt_ref, "evidence_mode": result.evidence_mode,
    })
    await meter(coordinator, request, result, dispatch)
    await coordinator.authorize(request, "publish")
    return await terminal(coordinator, request, "ready", "VERIFIED_RESULT_RECORDED",
                          result.evidence_mode, tuple(item.ref for item in verified))