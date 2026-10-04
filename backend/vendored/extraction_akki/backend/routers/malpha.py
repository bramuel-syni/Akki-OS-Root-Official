"""Mα programme surface: the two commissioned three-language products, their autonomous lanes, GPU metering under the uncapped-until-billing
authority, the WPW notebook state and the owner-readable log. Reads are tenant-scoped; dispatch stays with the autopilot and the operator."""
import asyncio

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from services.enforce.census_identity import census_identity
from services.training_lab import contracts as c

router = APIRouter(prefix='/api/training/malpha', tags=['m-alpha'])


def _operator(actor):
    if actor['tenant_id'] != 'RMS': raise HTTPException(403, 'The Mα commissions are RMS custody')
    if not {'operator', 'master_admin'}.intersection(actor['roles']): raise HTTPException(403, 'An admitted operator is required')


@router.get('/status', response_model=c.Envelope)
async def status(actor=Depends(census_identity)):
    _operator(actor)
    from services.training_lab import malpha
    return {'tenant_id': actor['tenant_id'], **await asyncio.to_thread(malpha.status)}


@router.get('/jobs/{job_id}', response_model=c.Envelope)
async def job(job_id: str, actor=Depends(census_identity)):
    _operator(actor)
    from services.training_lab import malpha
    doc = await asyncio.to_thread(malpha.job_detail, job_id)
    if not doc: raise HTTPException(404, 'No Mα job with that reference')
    return {'tenant_id': actor['tenant_id'], 'job': doc}


@router.post('/commission', status_code=202, response_model=c.Envelope)
async def commission(background: BackgroundTasks, actor=Depends(census_identity)):
    """Idempotent: records both commissions (WPW attached first) and runs one autonomous tick in the background."""
    _operator(actor)
    from services.training_lab import malpha
    created = await asyncio.to_thread(malpha.ensure_commissions, actor['principal_id'])
    background.add_task(asyncio.to_thread, malpha.tick)
    return {'tenant_id': actor['tenant_id'], 'created': created, 'commissions': [c_['commission_id'] for c_ in malpha.commissions()], 'tick': 'scheduled'}


@router.post('/tick', response_model=c.Envelope)
async def tick(actor=Depends(census_identity)):
    _operator(actor)
    from services.training_lab import malpha
    return {'tenant_id': actor['tenant_id'], 'result': await asyncio.to_thread(malpha.tick)}


@router.get('/wpw/{commission_id}', response_model=c.Envelope)
async def notebook(commission_id: str, actor=Depends(census_identity)):
    _operator(actor)
    from services.training_lab import malpha
    from services.wpw import tier1_notebook as wpw
    if commission_id not in malpha.COMMISSIONS: raise HTTPException(404, 'Unknown commission')
    return {'tenant_id': actor['tenant_id'], 'commission_id': commission_id, 'attached': wpw.is_attached_to_run(commission_id), 'chain': wpw.verify_hash_chain(commission_id), 'entries': wpw.list_entries(commission_id)}


@router.get('/tier2', response_model=c.Envelope)
async def tier2_reports(commission_id: str | None = None, actor=Depends(census_identity)):
    """WPW Tier 2 technical reports drafted at settlement (accepted and refused). Internal — WPW-10; served to admitted operators only, never published."""
    _operator(actor)
    from services.wpw import tier2_malpha
    return {'tenant_id': actor['tenant_id'], 'internal_only': True, 'reports': await asyncio.to_thread(tier2_malpha.list_reports, commission_id)}


@router.get('/tier2/{job_id}', response_model=c.Envelope)
async def tier2_report(job_id: str, actor=Depends(census_identity)):
    _operator(actor)
    from services.wpw import tier2_malpha
    doc = await asyncio.to_thread(tier2_malpha.get_report, job_id)
    if not doc: raise HTTPException(404, 'No Tier 2 report for that run')
    return {'tenant_id': actor['tenant_id'], **doc}
