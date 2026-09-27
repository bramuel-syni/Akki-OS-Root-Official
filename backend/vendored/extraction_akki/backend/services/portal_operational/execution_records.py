"""Allowlisted DAP projection of the same canonical execution stream, not a second jobs store."""
import json
from datetime import datetime, timezone
from uuid import uuid4
from fastapi import HTTPException
from services.ledger_writer.principal_control import read_events
from services.northena.execution_journal import LedgerJournal, RESOURCE
from services.northena.execution_models import Request
from services.portal_operational.models import HistoryEntry


async def events_for(db, scope, request_id=None):
    query = {"row.tenant_id": scope["tenant_id"], "row.resource_type": RESOURCE,
             "payload.principal_id": scope["principal_id"]}
    if request_id is not None:
        query["row.run_id"] = request_id
    return await read_events(db, query)


def snapshot(events, scope):
    event = next((e for e in events if e["payload"]["slot"] == "request"), None)
    if event is None:
        return None
    request = Request.model_validate_json(json.dumps(event["payload"]["data"]["request"]))
    if (request.tenant_id, request.principal_id, request.request_id) != (
            scope["tenant_id"], scope["principal_id"], event["row"]["run_id"]):
        raise ValueError("Execution snapshot scope mismatch.")
    if any(e["payload"]["request_sha256"] != request.digest() for e in events):
        raise ValueError("Execution snapshot identity mismatch.")
    return request


def _state(view, dispatched):
    phase, reason = view["phase"], view["reason_code"]
    if phase == "held":
        if not dispatched:
            return "Routing"
        transient = reason.endswith(("_UNBOUND", "_NOT_BOUND", "_UNAVAILABLE")) or "UNCERTAIN" in reason
        return "Interrupted" if transient else "Blocked"
    return {"running": "Executing", "unknown": "Interrupted", "ready": "Ready",
            "cancelled": "Stopped", "failed": "Blocked"}[phase]


def project(work, events):
    if not events:
        return work
    dispatched, state, reason = False, work.lifecycle_state, work.reason_code
    history = list(work.history)
    terminal = None
    for e in events:
        slot, data = e["payload"]["slot"], e["payload"]["data"]
        label = None
        if slot == "dispatch" and data.get("action") == "submit":
            dispatched, state, reason, label = True, "Executing", "EXECUTION_RESERVED", "execution_reserved"
        elif slot == "terminal" or slot.startswith("portal_view:"):
            state, reason, label = _state(data, dispatched), data["reason_code"], "execution_" + data["phase"]
            if slot == "terminal":
                terminal = data
            if state == "Ready" and data["evidence_mode"] != "measured":
                state, reason = "Blocked", "MOCKED_RESULT_NOT_RELEASABLE"
        elif slot.startswith("uncertain:"):
            state, reason, label = "Interrupted", data["reason_code"], "execution_uncertain"
        if label:
            history.append(HistoryEntry(at=datetime.fromtimestamp(e["row"]["at"]["epoch_s"], timezone.utc).isoformat(),
                state=state.lower(), event=label, reason_code=reason, receipt_hash=e["row"]["hash"]))
    actions = {"Executing": ["stop"], "Interrupted": ["retry", "stop"], "Ready": ["result"]}.get(state, [])
    if terminal and state != "Ready":
        actions = []
    return work.model_copy(update={"state": state.lower(), "lifecycle_state": state,
        "reason_code": reason, "reason": "Execution state is recorded; result access is checked separately.",
        "history": history, "permitted_actions": actions, "result": None,
        "execution_verified": bool(terminal and state == "Ready" and terminal["evidence_mode"] == "measured")})


async def remember_view(db, request, view):
    # Fresh observations may differ after revocation; never overwrite an earlier one.
    await LedgerJournal(db).append(request, "portal_view:" + uuid4().hex,
        view.model_dump(mode="json", exclude={"artifact_refs", "terms_ref", "usage", "execution_verified"}))


async def existing_request(db, scope, request_id):
    from services.northena.portal_work import events_for as dap_events
    if not await dap_events(db, scope, request_id):
        raise HTTPException(404, "Request not found.")
    events = await events_for(db, scope, request_id)
    request = snapshot(events, scope)
    if request is None:
        raise HTTPException(409, "A recorded execution descriptor is required.")
    return request, events