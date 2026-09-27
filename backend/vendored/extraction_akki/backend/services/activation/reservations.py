"""Atomic allocation accounting, append-only on the existing tenant Ledger.

Unknown/stopped-without-usage work keeps its full reservation. Only a signed,
request-bound terminal measurement can settle; actual overrun is never erased.
"""
import json
from decimal import Decimal
from services.enforce.control_scope import require_control_scope
from services.ledger_writer.mongo_control import digest
from services.ledger_writer.conditional_control import append_at_head, HeadChanged
from services.activation.record_shapes import Allocation, quantities
from services.northena.execution_models import Held

RESOURCE = "activation_reservation"


class Reservations:
    def __init__(self, receipts):
        self.receipts = receipts

    async def reserve(self, plan, plan_ref):
        request, wanted = plan.request, quantities(plan.limits)
        scope = require_control_scope()
        if (scope.tenant_id, scope.principal_id) != (request.tenant_id, request.principal_id):
            raise Held("RESERVATION_SCOPE_MISMATCH")
        command = digest({"activation_reservation": request.digest()})
        for _ in range(16):
            from services.activation.approvals import approved_plan
            current, current_ref, _, _, events = await approved_plan(self.receipts, request)
            if current != plan or current_ref != plan_ref:
                raise Held("RESERVATION_PLAN_CHANGED")
            allocation_receipt = await self.receipts.resolve(plan.allocation_ref, kind="allocation", events=events)
            allocation = Allocation.model_validate_json(json.dumps(allocation_receipt.claims))
            limits = quantities(allocation.limits)
            if (not set(request.scope_refs) <= set(allocation_receipt.scope_refs)
                    or allocation.terms_ref != plan.terms_ref or not set(wanted) <= set(limits)):
                raise Held("RESERVATION_ALLOCATION_MISMATCH")
            existing = next((e for e in events if e["command_id"] == command), None)
            if existing:
                p = existing["payload"]
                if p.get("plan_ref") != plan_ref or p.get("amounts") != [v.model_dump() for v in plan.limits]:
                    raise Held("RESERVATION_REPLAY_CONFLICT")
                return existing["row"]["hash"]
            used = {k: Decimal(0) for k in limits}
            settled = {e["payload"]["reservation_ref"]: e["payload"]["amounts"] for e in events
                       if e["row"]["resource_type"] == RESOURCE and e["row"]["event_type"] == "activation.settled"}
            for e in events:
                if (e["row"]["resource_type"] == RESOURCE and e["row"]["event_type"] == "activation.reserved"
                        and e["payload"]["allocation_ref"] == plan.allocation_ref):
                    for q in settled.get(e["row"]["hash"], e["payload"]["amounts"]):
                        key = (q["dimension"], q["unit"])
                        if key not in used:
                            raise Held("ALLOCATION_UNIT_DRIFT")
                        used[key] += Decimal(q["quantity"])
            if any(used[k] + v > limits[k] for k, v in wanted.items()):
                raise Held("ALLOCATION_CAPACITY_EXCEEDED")
            try:
                event = await append_at_head(self.receipts.db, events, tenant_id=scope.tenant_id,
                    run_id=request.request_id, command_id=command, event_type="activation.reserved",
                    resource_type=RESOURCE, decision="reserved", reason_code="ALLOCATION_RESERVED",
                    payload={"principal_id": scope.principal_id, "request_sha256": request.digest(),
                             "plan_ref": plan_ref, "allocation_ref": plan.allocation_ref,
                             "amounts": [v.model_dump() for v in plan.limits]})
                return event["row"]["hash"]
            except HeadChanged:
                continue
        raise Held("ALLOCATION_LEDGER_BUSY")

    async def settle(self, reservation_ref, observation_ref):
        events = await self.receipts.events()
        e = next((e for e in events if e["row"]["hash"] == reservation_ref and
                  e["row"]["event_type"] == "activation.reserved"), None)
        if e is None or e["payload"]["principal_id"] != require_control_scope().principal_id:
            raise Held("RESERVATION_NOT_OWNED")
        observation = await self.receipts.resolve(observation_ref, kind="observation",
            request_sha256=e["payload"]["request_sha256"], events=events)
        from services.activation.native_evidence import Observation
        proof = Observation.model_validate_json(json.dumps(observation.claims))
        if (proof.category != "measurements" or proof.reservation_ref != reservation_ref
                or not proof.terminal or proof.evidence_mode != "measured"):
            raise Held("RESERVATION_TERMINAL_MEASUREMENT_REQUIRED")
        original = {(q["dimension"], q["unit"]): Decimal(q["quantity"]) for q in e["payload"]["amounts"]}
        measured = quantities(proof.quantities)
        if set(original) != set(measured):
            raise Held("RESERVATION_MEASUREMENT_DIMENSIONS_MISMATCH")
        from services.activation.record_shapes import Plan
        plan_receipt = await self.receipts.resolve(e["payload"]["plan_ref"], kind="plan", events=events)
        plan = Plan.model_validate_json(json.dumps(plan_receipt.claims))
        worker = await self.receipts.resolve(plan.worker_ref, kind="worker", events=events)
        if observation.signer_id != worker.signer_id:
            raise Held("MEASUREMENT_WORKER_MISMATCH")
        from services.ledger_writer.principal_control import append_event
        row = await append_event(self.receipts.db, tenant_id=require_control_scope().tenant_id,
            run_id=e["row"]["run_id"], command_id=digest({"settlement": reservation_ref}),
            event_type="activation.settled", resource_type=RESOURCE, decision="settled",
            reason_code="LIMIT_EXCEEDED" if any(measured[k] > original[k] for k in measured) else "USAGE_RECONCILED",
            payload={"principal_id": require_control_scope().principal_id, "reservation_ref": reservation_ref,
                     "observation_ref": observation_ref, "amounts": [q.model_dump() for q in proof.quantities]})
        return row["row"]["hash"]