"""Prospective DAP control records: propagated actor, verified prefix, no grants.

Legacy writer and sealed canonical kernels remain untouched. This adapter does
not certify global writer coverage, principal admission or independent witnessing.
"""
from copy import deepcopy

from services.enforce.control_scope import require_control_scope
from services.request_context.ledger_actor_binding import write_ledger_row
from services.ledger_writer import mongo_control
from services.ledger_writer.control_commands import (
    COMMAND_KEY, CommandConflict, fingerprint, check_attribution,
)
from services.ledger_writer.control_integrity import checked_event, load_verified_prefix
from services.ledger_writer.control_insert_guard import InsertGuard


def _scope(tenant_id):
    scope = require_control_scope()
    if not isinstance(tenant_id, str) or tenant_id != scope.tenant_id:
        raise ValueError("Ledger tenant does not match the control request scope.")
    return scope


async def append_event(db, *, tenant_id, run_id, command_id, event_type,
                       resource_type, decision, reason_code, payload):
    scope = _scope(tenant_id)
    actor = write_ledger_row(data_class="control_event")["actor"]
    if not isinstance(payload, dict) or COMMAND_KEY in payload:
        raise ValueError("Invalid or caller-supplied command metadata.")
    payload = deepcopy(payload)
    check_attribution(payload, actor, tenant_id)
    row_fields = dict(tenant_id=tenant_id, actor_id=actor, run_id=run_id,
                      event_type=event_type, resource_type=resource_type,
                      decision=decision, reason_code=reason_code)
    if any(not isinstance(value, str) or not value.strip() for value in (
            command_id, tenant_id, actor, run_id, event_type, resource_type, decision)):
        raise ValueError("Nonblank control command fields are required.")
    if not isinstance(reason_code, str):
        raise ValueError("A textual reason code is required.")
    expected = fingerprint(row_fields, payload)
    # Validate all JSON data even where command identity uses the frozen body hash.
    mongo_control.digest(payload)
    payload[COMMAND_KEY] = {"id": command_id, "fingerprint": expected}
    await load_verified_prefix(db, tenant_id)
    _scope(tenant_id)
    event = await mongo_control.append_event(
        InsertGuard(db, scope), **row_fields, command_id=command_id, payload=payload)
    event = checked_event(event)
    _scope(tenant_id)
    if event["command_id"] != command_id or fingerprint(event["row"], event["payload"]) != expected:
        raise CommandConflict("This request key already belongs to a different frozen command.")
    # An acknowledged event must also occur in the verified durable prefix.
    prefix = await load_verified_prefix(db, tenant_id)
    _scope(tenant_id)
    if not any(item["row"]["hash"] == event["row"]["hash"] for item in prefix):
        raise ValueError("Ledger acknowledgement is not in the durable prefix.")
    return event


async def read_events(db, query):
    allowed = {"row.tenant_id", "row.resource_type", "row.run_id", "payload.principal_id"}
    if not isinstance(query, dict) or set(query) - allowed or "row.tenant_id" not in query:
        raise ValueError("An explicit scoped control-event query is required.")
    scope = _scope(query["row.tenant_id"])
    if "payload.principal_id" in query and query["payload.principal_id"] != scope.principal_id:
        raise ValueError("Control read principal does not match request scope.")
    for key, value in query.items():
        if isinstance(value, dict):
            if (key != "row.resource_type" or set(value) != {"$in"}
                    or not isinstance(value["$in"], list)
                    or any(not isinstance(item, str) for item in value["$in"])):
                raise ValueError("Unsupported control-event filter.")
        elif not isinstance(value, str):
            raise ValueError("Invalid control-event filter.")
    events = await load_verified_prefix(db, scope.tenant_id)
    _scope(scope.tenant_id)
    def matches(event):
        for key, value in query.items():
            group, name = key.split(".")
            actual = event[group].get(name)
            if actual not in value["$in"] if isinstance(value, dict) else actual != value:
                return False
        return True
    return [event for event in events if matches(event)]