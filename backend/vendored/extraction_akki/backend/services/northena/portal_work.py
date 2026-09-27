"""Northena's durable DAP control-plane record; no extraction execution here."""
import hashlib
from datetime import datetime, timezone
from fastapi import HTTPException
from services.dap.commission import _OPERATION_TO_ENGINE, CommissionedJob
from services.dap_lifecycle.state_machine import RequestState, transition
from services.ledger_writer.principal_control import append_event, read_events
from services.ledger_writer.mongo_control import digest
from services.portal_operational.models import HistoryEntry, WorkView
from services.portal_operational.hold_reasons import public_reason, disclosure

RESOURCE = "dap_request"
REASONS = {
    "ADMISSION_UNRESOLVED": "Execution is held: operation rights, approval authority, terms and an admitted executor are not established.",
    "REQUEST_STOPPED": "This request was stopped. No party-wide halt was issued.",
}


async def events_for(db, scope, request_id=None):
    query = {"row.tenant_id": scope["tenant_id"], "row.resource_type": RESOURCE,
             "payload.principal_id": scope["principal_id"]}
    if request_id is not None:
        query["row.run_id"] = request_id
    return await read_events(db, query)


def project(events):
    first, last = events[0]["payload"], events[-1]["payload"]
    state = last["lifecycle_state"]
    public_state = {"InApproval": "in_approval"}.get(state, state.lower())
    history = []
    for event in events:
        for entry in event["payload"]["history"]:
            public_entry = {**entry, "reason_code": public_reason(entry["reason_code"]).code if entry["reason_code"] else ""}
            history.append(HistoryEntry(**public_entry, receipt_hash=event["row"]["hash"]))
    # Allowlist only; no approver fields, raw payloads, identity internals or budget hints.
    return WorkView(
        request_id=first["request_id"], work_id=first["request_id"],
        objective_text=first["objective_text"], objective_hash=first["objective_hash"],
        operation=first["operation"], units=first["units"], state=public_state,
        lifecycle_state=state, governing_engine=first["governing_engine"],
        created_at=first["created_at"], **disclosure(last["reason_code"], receipt_ref=events[-1]["row"]["hash"]),
        history=history, permitted_actions=["stop"] if state == "Executing" else [],
    )


async def record_descriptor_hold(db, scope, request_id, reason_code):
    """Append a failed descriptor lookup without inventing an execution request."""
    from uuid import uuid4
    events = await events_for(db, scope, request_id)
    if not events:
        raise HTTPException(404, "Request not found.")
    frozen = {key: events[0]["payload"][key] for key in ("request_id", "principal_id", "objective_text",
        "objective_hash", "body_hash", "units", "operation", "governing_engine", "created_at")}
    now = datetime.now(timezone.utc).isoformat()
    await append_event(db, tenant_id=scope["tenant_id"], run_id=request_id,
        command_id=digest([request_id, "descriptor_hold", uuid4().hex]),
        event_type="dap.request.execution_held", resource_type=RESOURCE, decision="held", reason_code=reason_code,
        payload={**frozen, "lifecycle_state": events[-1]["payload"]["lifecycle_state"], "reason_code": reason_code,
                 "history": [{"at": now, "state": "routing", "event": "descriptor_held", "reason_code": reason_code}]})


async def submit(db, scope, body):
    command_id = digest([scope["tenant_id"], scope["principal_id"], body.idempotency_key])
    request_id = f"req-{command_id[:32]}"
    body_hash = digest(body.model_dump(exclude={"idempotency_key"}))
    now = datetime.now(timezone.utc).isoformat()
    state = transition(RequestState.Compose, RequestState.Submitted)
    state = transition(state, RequestState.Routing)
    job = CommissionedJob(job_id=request_id, principal_id=scope["principal_id"],
                          objective=body.objective_text, operation=body.operation,
                          estate_id=scope["tenant_id"], frozen=True, commissioned_at_iso=now)
    payload = {
        "request_id": request_id, "principal_id": scope["principal_id"],
        "objective_text": job.objective,
        "objective_hash": hashlib.sha256(job.objective.encode()).hexdigest(),
        "body_hash": body_hash, "units": body.units, "operation": job.operation,
        "governing_engine": _OPERATION_TO_ENGINE[job.operation], "created_at": now,
        "lifecycle_state": state.value, "reason_code": "ADMISSION_UNRESOLVED",
        "history": [
            {"at": now, "state": "submitted", "event": "commissioned", "reason_code": ""},
            {"at": now, "state": "routing", "event": "execution_held", "reason_code": "ADMISSION_UNRESOLVED"},
        ],
    }
    event = await append_event(db, tenant_id=scope["tenant_id"], run_id=request_id,
                              command_id=command_id,
                              event_type="dap.request.commissioned", resource_type=RESOURCE,
                              decision="held", reason_code="ADMISSION_UNRESOLVED", payload=payload)
    if event["payload"]["body_hash"] != body_hash:
        raise HTTPException(409, "This idempotency key already belongs to a different frozen request.")
    return project(await events_for(db, scope, request_id))


async def detail(db, scope, request_id):
    events = await events_for(db, scope, request_id)
    if not events:
        raise HTTPException(404, "Request not found.")
    from services.portal_operational.execution_records import events_for as execution_events, project as project_execution
    from services.portal_operational.delivery_history import project as project_delivery, expected_artifacts
    executions = await execution_events(db, scope, request_id)
    work = project_execution(project(events), executions)
    return await project_delivery(db, scope, work, expected=expected_artifacts(executions))


async def listing(db, scope):
    from services.portal_operational.execution_records import events_for as execution_events, project as project_execution
    from services.portal_operational.delivery_history import grouped as delivery_groups, project as project_delivery, expected_artifacts
    grouped = {}
    for event in await events_for(db, scope):
        grouped.setdefault(event["row"]["run_id"], []).append(event)
    executions = {}
    for event in await execution_events(db, scope):
        executions.setdefault(event["row"]["run_id"], []).append(event)
    deliveries = await delivery_groups(db, scope)
    result = []
    for events in reversed(list(grouped.values())):
        request_id = events[0]['row']['run_id']
        work = project_execution(project(events), executions.get(request_id, []))
        result.append(await project_delivery(db, scope, work, deliveries.get(request_id, []),
                                            expected=expected_artifacts(executions.get(request_id, []))))
    return result