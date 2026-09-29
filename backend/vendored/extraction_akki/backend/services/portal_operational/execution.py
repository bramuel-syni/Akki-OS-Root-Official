"""Authenticated control seam over an existing frozen DAP request; no data path."""
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field
from fastapi import HTTPException

from services.northena import portal_work
from services.northena.execution_models import Request, Held
from services.northena.execution_composition import build_coordinator
from services.ledger_writer.mongo_control import digest
from services.portal_operational import execution_records


class ExecutionBudget(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    deadline_epoch: Annotated[int, Field(gt=0)]


async def frozen_request(db, scope, request_id, budget, receipts=None):
    events = await portal_work.events_for(db, scope, request_id)
    if not events:
        raise HTTPException(404, "Request not found.")
    frozen = events[0]["payload"]
    recorded = await execution_records.events_for(db, scope, request_id)
    saved = execution_records.snapshot(recorded, scope)
    if saved is not None:
        if saved.deadline_epoch != budget.deadline_epoch:
            raise HTTPException(409, "The recorded execution deadline cannot be changed on replay.")
        if saved.objective_sha256 != digest(frozen["objective_text"]) or saved.scope_refs != tuple(frozen["units"]):
            raise HTTPException(409, "Execution descriptor does not match the frozen request.")
        return saved
    # Model/skill descriptors must come from their native builders and admitted
    # recipe/provisioning records; never fabricate training inputs from source IDs.
    mapping = {"browse_estate": ("source", "mtafiti"), "connect_workspace": ("source", "synisense")}
    if frozen["operation"] not in mapping:
        from services.activation.portal_plans import MODEL_OPERATIONS, recover_plan
        from services.work_orders.kind_profiles import engines_for_operation
        # A commissioned work order names its kind through the registered profile and the signed Plan.
        allowed = engines_for_operation(frozen["operation"])
        if frozen["operation"] in MODEL_OPERATIONS:
            allowed.add(MODEL_OPERATIONS[frozen["operation"]])
        if not allowed:
            raise Held("NATIVE_SKILL_PROVISIONING_BINDING_REQUIRED" if frozen["operation"] == "develop_skills"
                       else "NATIVE_CUSTODY_DELIVERY_REQUIRED")
        return await recover_plan(receipts, scope, frozen, budget.deadline_epoch, allowed)
    kind, engine = mapping[frozen["operation"]]
    return Request(request_id=request_id, tenant_id=scope["tenant_id"], principal_id=scope["principal_id"],
                   kind=kind, engine=engine, objective_sha256=digest(frozen["objective_text"]),
                   input_refs=tuple("akki://source/" + unit for unit in frozen["units"]),
                   scope_refs=tuple(frozen["units"]), deadline_epoch=budget.deadline_epoch)


async def advance(db, scope, request_id, budget, bindings=None, receipts=None):
    work = await portal_work.detail(db, scope, request_id)
    if work.lifecycle_state in {"Blocked", "Refused", "Expired", "Stopped"}:
        raise HTTPException(409, "This request is closed; any new commission requires a fresh request.")
    try:
        request = await frozen_request(db, scope, request_id, budget, receipts=receipts)
    except Held as exc:
        await portal_work.record_descriptor_hold(db, scope, request_id, exc.reason_code)
        from services.portal_operational.hold_reasons import disclosure
        raise HTTPException(409, disclosure(exc.reason_code)) from None
    view = await build_coordinator(db, bindings).advance(request)
    await execution_records.remember_view(db, request, view)
    return view