"""ARMI routes: tenant-scoped agent register, lifecycle and assignments. Reads are open to signed-in estate members; lifecycle changes need an operator."""
import asyncio
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from services.enforce.census_identity import census_identity
from services.training_lab import contracts as c

router = APIRouter(prefix='/api/armi', tags=['armi'])


def _operator(actor):
    if not {'operator', 'master_admin'}.intersection(actor['roles']): raise HTTPException(403, 'An admitted operator is required')


class JD(BaseModel):
    role: str = Field(min_length=1, max_length=120)
    job: str = Field(min_length=1, max_length=1200)
    strengths: list[str] = Field(default_factory=list, max_length=20)
    can_do: list[str] = Field(default_factory=list, max_length=30)
    cannot_do: list[str] = Field(default_factory=list, max_length=30)


class Onboard(BaseModel):
    kind: Literal['agent', 'llm', 'model', 'skill', 'worker']
    name: str = Field(min_length=1, max_length=160)
    agent_id: str | None = Field(default=None, pattern=r'^[a-z]+:[A-Za-z0-9:._-]{1,120}$')
    version: str | None = None
    jd: JD
    objectives: list[str] = Field(default_factory=list, max_length=20)
    capabilities: list[str] = Field(default_factory=list, max_length=40)
    limits: list[str] = Field(default_factory=list, max_length=40)
    admission_ref: str | None = None
    note: str | None = Field(default=None, max_length=600)


class Transition(BaseModel):
    action: Literal['activate', 'suspend', 'revoke', 'bind_version']
    note: str | None = Field(default=None, max_length=600)
    version: str | None = Field(default=None, max_length=200)


class Assign(BaseModel):
    task: str = Field(min_length=1, max_length=1200)
    objective_ref: str | None = None
    collaborators: list[str] = Field(default_factory=list, max_length=20)
    depends_on: list[str] = Field(default_factory=list, max_length=20)


class Complete(BaseModel):
    outcome: Literal['completed', 'failed'] = 'completed'
    result_ref: str | None = None
    resources: dict | None = None


class Score(BaseModel):
    quality: float = Field(ge=0, le=1)
    compliant: bool
    evidence_ref: str = Field(min_length=1, max_length=400)


@router.get('/overview', response_model=c.Envelope)
async def overview(actor=Depends(census_identity)):
    from services.armi import registry
    return {'tenant_id': actor['tenant_id'], **await asyncio.to_thread(registry.overview, actor['tenant_id'])}


@router.get('/agents', response_model=c.Envelope)
async def agents(actor=Depends(census_identity)):
    from services.armi import registry
    return {'tenant_id': actor['tenant_id'], 'agents': await asyncio.to_thread(registry.list_agents, actor['tenant_id'])}


@router.post('/sync', response_model=c.Envelope)
async def sync(actor=Depends(census_identity)):
    _operator(actor)
    from services.armi import registry
    n = await asyncio.to_thread(registry.sync, actor['tenant_id'])
    return {'tenant_id': actor['tenant_id'], 'derived': n}


@router.get('/agents/{agent_id:path}', response_model=c.Envelope)
async def agent(agent_id: str, actor=Depends(census_identity)):
    from services.armi import registry
    doc = await asyncio.to_thread(registry.get, actor['tenant_id'], agent_id)
    if not doc: raise HTTPException(404, 'No agent with that identity in this estate')
    return {'tenant_id': actor['tenant_id'], 'agent': doc}


@router.post('/agents', status_code=201, response_model=c.Envelope)
async def onboard(body: Onboard, actor=Depends(census_identity)):
    _operator(actor)
    from services.armi import registry
    try: doc = await asyncio.to_thread(registry.onboard, actor['tenant_id'], actor['principal_id'], body.model_dump())
    except ValueError as exc: raise HTTPException(409, str(exc)) from exc
    return {'tenant_id': actor['tenant_id'], 'agent': doc}


@router.post('/agents/{agent_id:path}/transition', response_model=c.Envelope)
async def transition(agent_id: str, body: Transition, actor=Depends(census_identity)):
    _operator(actor)
    from services.armi import registry
    try: doc = await asyncio.to_thread(registry.transition, actor['tenant_id'], actor['principal_id'], agent_id, body.action, body.note, body.version)
    except LookupError as exc: raise HTTPException(404, str(exc)) from exc
    except ValueError as exc: raise HTTPException(409, str(exc)) from exc
    return {'tenant_id': actor['tenant_id'], 'agent': doc}


@router.post('/agents/{agent_id:path}/assign', status_code=201, response_model=c.Envelope)
async def assign(agent_id: str, body: Assign, actor=Depends(census_identity)):
    _operator(actor)
    from services.armi import registry
    try: row = await asyncio.to_thread(registry.assign, actor['tenant_id'], actor['principal_id'], agent_id, body.model_dump())
    except LookupError as exc: raise HTTPException(404, str(exc)) from exc
    except ValueError as exc: raise HTTPException(409, str(exc)) from exc
    return {'tenant_id': actor['tenant_id'], 'assignment': row}


@router.post('/assignments/{assignment_id}/complete', response_model=c.Envelope)
async def complete(assignment_id: str, body: Complete, actor=Depends(census_identity)):
    _operator(actor)
    from services.armi import registry
    try: row = await asyncio.to_thread(registry.complete, actor['tenant_id'], actor['principal_id'], assignment_id, body.model_dump())
    except LookupError as exc: raise HTTPException(404, str(exc)) from exc
    except ValueError as exc: raise HTTPException(409, str(exc)) from exc
    return {'tenant_id': actor['tenant_id'], 'assignment': row}


@router.post('/assignments/{assignment_id}/score', response_model=c.Envelope)
async def score(assignment_id: str, body: Score, actor=Depends(census_identity)):
    _operator(actor)
    from services.armi import registry
    try: row = await asyncio.to_thread(registry.score, actor['tenant_id'], actor['principal_id'], assignment_id, body.model_dump())
    except LookupError as exc: raise HTTPException(404, str(exc)) from exc
    except ValueError as exc: raise HTTPException(409, str(exc)) from exc
    return {'tenant_id': actor['tenant_id'], 'assignment': row}
