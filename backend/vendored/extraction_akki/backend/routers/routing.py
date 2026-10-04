"""Measured routing routes (Mα MA-08): run a fixed-task trial over eligible candidate models, read trials, adopt or revert a decision.
Reads are open to signed-in estate members; a trial spends metered model calls and adoption changes production routing, so both need an operator."""
import asyncio
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from services.enforce.census_identity import census_identity
from services.training_lab import contracts as c

router = APIRouter(prefix='/api/routing', tags=['routing'])


def _operator(actor):
    if not {'operator', 'master_admin'}.intersection(actor['roles']): raise HTTPException(403, 'An admitted operator is required')


class Trial(BaseModel):
    role: Literal['planner', 'writer', 'reviewer', 'assistant'] = 'planner'


class Adopt(BaseModel):
    model: str = Field(min_length=1, max_length=120)
    note: str | None = Field(default=None, max_length=600)


class Revert(BaseModel):
    role: Literal['planner', 'writer', 'reviewer', 'assistant']
    note: str | None = Field(default=None, max_length=600)


@router.get('/assignments', response_model=c.Envelope)
async def assignments(actor=Depends(census_identity)):
    from services.chokepoint import routing
    return {'tenant_id': actor['tenant_id'], **await asyncio.to_thread(routing.assignments, actor['tenant_id'])}


@router.get('/trials', response_model=c.Envelope)
async def trials(role: str | None = None, actor=Depends(census_identity)):
    from services.chokepoint import routing
    return {'tenant_id': actor['tenant_id'], 'trials': await asyncio.to_thread(routing.trials, actor['tenant_id'], role)}


@router.get('/trials/{trial_id}', response_model=c.Envelope)
async def trial(trial_id: str, actor=Depends(census_identity)):
    from services.chokepoint import routing
    doc = await asyncio.to_thread(routing.trial, actor['tenant_id'], trial_id)
    if not doc: raise HTTPException(404, 'No routing trial with that reference in this estate')
    return {'tenant_id': actor['tenant_id'], 'trial': doc}


@router.post('/trials', status_code=201, response_model=c.Envelope)
async def run_trial(body: Trial, actor=Depends(census_identity)):
    _operator(actor)
    from services.chokepoint import routing
    try: doc = await routing.run_trial(actor['tenant_id'], actor['principal_id'], body.role)
    except ValueError as exc: raise HTTPException(409, str(exc)) from exc
    return {'tenant_id': actor['tenant_id'], 'trial': doc}


@router.post('/trials/{trial_id}/adopt', response_model=c.Envelope)
async def adopt(trial_id: str, body: Adopt, actor=Depends(census_identity)):
    _operator(actor)
    from services.chokepoint import routing
    try: d = await asyncio.to_thread(routing.adopt, actor['tenant_id'], actor['principal_id'], trial_id, body.model, body.note)
    except LookupError as exc: raise HTTPException(404, str(exc)) from exc
    except ValueError as exc: raise HTTPException(409, str(exc)) from exc
    return {'tenant_id': actor['tenant_id'], 'decision': d}


@router.post('/revert', response_model=c.Envelope)
async def revert(body: Revert, actor=Depends(census_identity)):
    _operator(actor)
    from services.chokepoint import routing
    try: d = await asyncio.to_thread(routing.revert, actor['tenant_id'], actor['principal_id'], body.role, body.note)
    except LookupError as exc: raise HTTPException(404, str(exc)) from exc
    return {'tenant_id': actor['tenant_id'], 'reverted': d}
