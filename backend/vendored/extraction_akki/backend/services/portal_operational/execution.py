"""Authenticated control seam over an existing frozen DAP request; no data path."""
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field
from fastapi import HTTPException

from services.northena import portal_work
from services.northena.execution_models import Request, RunView
from services.northena.execution_composition import build_coordinator
from services.ledger_writer.mongo_control import digest


class ExecutionBudget(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    deadline_epoch: Annotated[int, Field(gt=0)]


async def frozen_request(db, scope, request_id, budget):
    events = await portal_work.events_for(db, scope, request_id)
    if not events:
        raise HTTPException(404, "Request not found.")
    frozen = events[0]["payload"]
    mapping = {"browse_estate": ("source", "mtafiti"), "connect_workspace": ("source", "synisense"),
               "fine_tune_model": ("training", "targeta"), "develop_skills": ("training", "targeta")}
    if frozen["operation"] not in mapping:
        raise HTTPException(409, "This request needs its operation-specific artifact/input binding.")
    kind, engine = mapping[frozen["operation"]]
    return Request(request_id=request_id, tenant_id=scope["tenant_id"], principal_id=scope["principal_id"],
                   kind=kind, engine=engine, objective_sha256=digest(frozen["objective_text"]),
                   input_refs=tuple("akki://source/" + unit for unit in frozen["units"]),
                   scope_refs=tuple(frozen["units"]), deadline_epoch=budget.deadline_epoch)


async def advance(db, scope, request_id, budget):
    request = await frozen_request(db, scope, request_id, budget)
    return await build_coordinator(db).advance(request)