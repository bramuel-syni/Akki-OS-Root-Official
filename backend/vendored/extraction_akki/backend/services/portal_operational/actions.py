"""Request-scoped controls through the canonical coordinator; no success without evidence."""
from fastapi import HTTPException
from services.northena import portal_work
from services.northena.execution_composition import build_coordinator
from services.portal_operational import execution_records


async def stop(db, scope, request_id, bindings=None):
    request, events = await execution_records.existing_request(db, scope, request_id)
    work = await portal_work.detail(db, scope, request_id)
    if work.lifecycle_state not in {"Executing", "Interrupted"}:
        raise HTTPException(409, "Only an executing or interrupted request can be stopped.")
    view = await build_coordinator(db, bindings).cancel(request)
    await execution_records.remember_view(db, request, view)
    if view.phase != "cancelled":
        raise HTTPException(409, "Executor cancellation is not confirmed: " + view.reason_code)
    return await portal_work.detail(db, scope, request_id)


async def retry(db, scope, request_id, bindings=None):
    request, events = await execution_records.existing_request(db, scope, request_id)
    work = await portal_work.detail(db, scope, request_id)
    if work.lifecycle_state != "Interrupted" or any(e["payload"]["slot"] in {"terminal", "cancel_intent"} for e in events):
        raise HTTPException(409, "Only an interrupted, non-terminal request can resume under its existing identity.")
    view = await build_coordinator(db, bindings).advance(request)
    await execution_records.remember_view(db, request, view)
    return await portal_work.detail(db, scope, request_id)


async def result(db, scope, request_id, bindings=None):
    request, _ = await execution_records.existing_request(db, scope, request_id)
    view = await build_coordinator(db, bindings).retrieve(request)
    await execution_records.remember_view(db, request, view)
    if not view.execution_verified or not view.artifact_refs:
        raise HTTPException(409, "No currently rights-admitted verified result: " + view.reason_code)
    work = await portal_work.detail(db, scope, request_id)
    # These are admitted references, not proof that downstream bytes were delivered.
    return {"request_id": request_id, "artifact_refs": list(view.artifact_refs),
            "execution_verified": True, "delivery_verified": work.delivery_verified}