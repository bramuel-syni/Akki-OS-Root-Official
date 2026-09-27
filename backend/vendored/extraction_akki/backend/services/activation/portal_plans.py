"""Recover an owning-engine signed descriptor; never derive model inputs from source IDs."""
import asyncio
import json
from services.activation.receipts import NativeReceipts, RESOURCE
from services.activation.record_shapes import Plan
from services.ledger_writer.mongo_control import digest
from services.northena.execution_models import Held

MODEL_OPERATIONS = {"processed_intelligence": ("skill", "solva"), "fine_tune_model": ("training", "targeta")}


async def recover_plan(receipts, scope, frozen, deadline_epoch):
    if not isinstance(receipts, NativeReceipts) or receipts.admitted_keys is None:
        raise Held("ADMITTED_SIGNER_RESOLVER_UNBOUND")
    async def resolve():
        events = await receipts.events()
        candidates = [e for e in events if e["row"]["resource_type"] == RESOURCE and
                      e["payload"].get("receipt", {}).get("kind") == "plan" and
                      e["payload"]["receipt"].get("claims", {}).get("request", {}).get("request_id") == frozen["request_id"] and
                      e["payload"]["receipt"]["claims"]["request"].get("principal_id") == scope["principal_id"]]
        if len(candidates) != 1:
            raise Held("ACTIVATION_PLAN_MISSING_OR_AMBIGUOUS")
        receipt = await receipts.resolve(candidates[0]["row"]["hash"], kind="plan", events=events)
        plan = Plan.model_validate_json(json.dumps(receipt.claims))
        request = plan.request
        if ((request.tenant_id, request.principal_id) != (scope["tenant_id"], scope["principal_id"])
                or request.request_id != frozen["request_id"] or request.objective_sha256 != digest(frozen["objective_text"])
                or request.scope_refs != tuple(frozen["units"]) or request.deadline_epoch != deadline_epoch
                or receipt.request_sha256 != request.digest()
                or receipt.scope_refs != request.scope_refs):
            raise Held("ACTIVATION_PORTAL_DESCRIPTOR_MISMATCH")
        if (request.kind, request.engine) != MODEL_OPERATIONS.get(frozen["operation"]):
            raise Held("ACTIVATION_PORTAL_OPERATION_MISMATCH")
        return request
    try:
        return await asyncio.wait_for(resolve(), receipts.timeout)
    except (TimeoutError, ConnectionError, OSError):
        raise Held("ACTIVATION_PLAN_LOOKUP_UNAVAILABLE") from None
    except (ValueError, KeyError, TypeError, AttributeError):
        raise Held("ACTIVATION_PLAN_RECORD_INVALID") from None