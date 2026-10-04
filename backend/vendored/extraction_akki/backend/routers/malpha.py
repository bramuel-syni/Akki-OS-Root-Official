"""Mα programme surface: the two commissioned three-language products, their autonomous lanes, GPU metering under the uncapped-until-billing
authority, the WPW notebook state and the owner-readable log. Reads are tenant-scoped; dispatch stays with the autopilot and the operator."""
import asyncio
import tempfile

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile

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


@router.get('/brand-lexicon', response_model=c.Envelope)
async def brand_lexicon(actor=Depends(census_identity)):
    """The active brand lexicon the listener is measured against, every registered version and which host databases carry it."""
    _operator(actor)
    from services.training_lab import brand_catalogue, malpha
    active = await asyncio.to_thread(brand_catalogue.active)
    return {'tenant_id': actor['tenant_id'], 'active': {k: v for k, v in active.items() if k != 'lexicon'} | {'brands': len(active['lexicon'])}, 'versions': await asyncio.to_thread(brand_catalogue.versions),
            'relabel_ready': {h: malpha.relabel_ready(h) for h, _ in malpha.HOST_ALLOCATION['malpha_aip_relabel']}}


@router.get('/brand-lexicon/{version}', response_model=c.Envelope)
async def brand_lexicon_version(version: int, actor=Depends(census_identity)):
    _operator(actor)
    from services.training_lab import brand_catalogue
    doc = await asyncio.to_thread(brand_catalogue.version_detail, version)
    if not doc: raise HTTPException(404, 'No brand lexicon with that version')
    return {'tenant_id': actor['tenant_id'], **doc}


@router.post('/brand-catalogue', status_code=201, response_model=c.Envelope)
async def register_brand_catalogue(background: BackgroundTasks, file: UploadFile = File(...), actor=Depends(census_identity)):
    """Owner workbook → new lexicon version (idempotent on the file hash). The autopilot re-labels each host database on its next tick; running jobs are untouched."""
    _operator(actor)
    if not (file.filename or '').lower().endswith('.xlsx'): raise HTTPException(422, 'The brand catalogue must be an .xlsx workbook')
    data = await file.read()
    if len(data) > 25_000_000: raise HTTPException(413, 'Workbook larger than 25 MB')
    from services.training_lab import brand_catalogue, malpha
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=True) as tmp:  # parsed and recorded in Mongo (hash, counts, brands); the workbook bytes are not kept on the pod
        tmp.write(data); tmp.flush()
        doc = await asyncio.to_thread(brand_catalogue.register, tmp.name, file.filename, actor['principal_id'])
    background.add_task(asyncio.to_thread, malpha.tick)
    return {'tenant_id': actor['tenant_id'], **{k: v for k, v in doc.items() if k != 'brands'}, 'excluded': [{'brand': b['brand'], 'reason': b['excluded_reason']} for b in doc['brands'] if not b.get('matchable')], 'tick': 'scheduled'}


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
