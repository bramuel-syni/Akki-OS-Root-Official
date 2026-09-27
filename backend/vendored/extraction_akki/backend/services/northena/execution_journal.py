"""Execution intents/observations on the SAME canonical Ledger, not a jobs store."""
from copy import deepcopy
from services.enforce.control_scope import require_control_scope
from services.ledger_writer.principal_control import append_event, read_events, CommandConflict
from services.ledger_writer.mongo_control import digest

RESOURCE = "execution_flow"


class LedgerJournal:
    def __init__(self, db):
        self.db = db

    def _scope(self, request):
        scope = require_control_scope()
        if (scope.tenant_id, scope.principal_id) != (request.tenant_id, request.principal_id):
            raise ValueError("Execution request scope does not match propagated principal.")

    async def read(self, request):
        self._scope(request)
        events = await read_events(self.db, {
            "row.tenant_id": request.tenant_id, "row.run_id": request.request_id,
            "row.resource_type": RESOURCE, "payload.principal_id": request.principal_id,
        })
        rows = []
        for event in events:
            payload = event["payload"]
            if payload["request_sha256"] != request.digest():
                raise CommandConflict("Execution request identity is frozen.")
            rows.append({"slot": payload["slot"], "data": deepcopy(payload["data"]),
                         "seq": event["row"]["seq"], "hash": event["row"]["hash"]})
        return rows

    async def append(self, request, slot, data):
        self._scope(request)
        if not isinstance(slot, str) or not slot.strip() or not isinstance(data, dict):
            raise ValueError("An execution slot and metadata record are required.")
        await self.read(request)  # Detect changed request before writing another slot.
        command = digest({"tenant": request.tenant_id, "principal": request.principal_id,
                          "request": request.request_id, "execution_slot": slot})
        event = await append_event(
            self.db, tenant_id=request.tenant_id, run_id=request.request_id,
            command_id=command, event_type="execution." + slot.split(":")[0],
            resource_type=RESOURCE, decision="recorded", reason_code="EXECUTION_METADATA",
            payload={"principal_id": request.principal_id, "request_sha256": request.digest(),
                     "slot": slot, "data": deepcopy(data)},
        )
        return {"slot": slot, "data": deepcopy(event["payload"]["data"]),
                "seq": event["row"]["seq"], "hash": event["row"]["hash"]}