"""Residency register routes (owner D7 · WP-C7): what lives on GPU/host storage, in which class, under which terms of reference."""
import asyncio

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from services.enforce.census_identity import census_identity
from services.training_lab import contracts as c

router = APIRouter(prefix='/api/training/residency', tags=['residency'])


def _operator(actor):
    if not {'operator', 'master_admin', 'dpo'}.intersection(actor['roles']): raise HTTPException(403, 'An admitted operator is required')


class Release(BaseModel):
    reason: str = Field(min_length=3, max_length=300)


@router.get('', response_model=c.Envelope)
async def view(actor=Depends(census_identity)):
    """Terms of reference per class, placed entries, and the latest measured snapshot with attribution and findings (live SSH read, both hosts)."""
    _operator(actor)
    from services.model_registry import residency
    return {'tenant_id': actor['tenant_id'], **await asyncio.to_thread(residency.reconcile)}


@router.get('/terms', response_model=c.Envelope)
async def terms(actor=Depends(census_identity)):
    _operator(actor)
    from services.model_registry import residency
    return {'tenant_id': actor['tenant_id'], 'terms': residency.terms(), 'entries': await asyncio.to_thread(residency.entries)}


@router.post('/{entry_id}/release', response_model=c.Envelope)
async def release(entry_id: str, body: Release, actor=Depends(census_identity)):
    if 'master_admin' not in actor['roles']: raise HTTPException(403, 'Releasing a residency entry is a master-admin act')
    from services.model_registry import residency
    try: doc = await asyncio.to_thread(residency.release, entry_id, body.reason)
    except LookupError as exc: raise HTTPException(404, str(exc)) from exc
    return {'tenant_id': actor['tenant_id'], 'entry': doc}
