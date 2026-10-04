"""Mα programme surface: the two commissioned three-language products, their autonomous lanes, GPU metering under the uncapped-until-billing
authority, the WPW notebook state and the owner-readable log. Reads are tenant-scoped; dispatch stays with the autopilot and the operator."""
import asyncio
import tempfile

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, Response, UploadFile
from pydantic import BaseModel

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


@router.get('/learning', response_model=c.Envelope)
async def learning_reviews(actor=Depends(census_identity)):
    _operator(actor)
    from services.training_lab import malpha_learning
    return {'tenant_id': actor['tenant_id'], 'reviews': await asyncio.to_thread(malpha_learning.list_reviews)}


@router.get('/evaluation-evidence', response_model=c.Envelope)
async def evaluation_evidence(actor=Depends(census_identity)):
    _operator(actor)
    from services.training_lab.malpha_evaluation import admission_preflight
    from services.training_lab import malpha
    records = await asyncio.to_thread(malpha.jobs)
    audits = [{k: j.get(k) for k in ('job_id', 'host', 'status', 'finished_at', 'result')} for j in records if j['phase'] == 'malpha_corpus_audit']
    return {'tenant_id': actor['tenant_id'], 'listener_preflight': admission_preflight(records), 'corpus_audits': audits}


@router.post('/learning', status_code=202, response_model=c.Envelope)
async def learning_review(background: BackgroundTasks, actor=Depends(census_identity)):
    _operator(actor)
    from services.training_lab import malpha_learning
    background.add_task(malpha_learning.reconstruct, actor['principal_id'], retry_failed=True)
    return {'tenant_id': actor['tenant_id'], 'status': 'scheduled', 'training_interrupted': False}


# ----------------------------------------------------------------------------- native-reviewer confirmation panel (independent reference for the sealed read)
class Annotation(BaseModel):
    brands: list[str] = []
    no_mention: bool = False
    unsure: bool = False


@router.get('/review/panel', response_model=c.Envelope)
async def review_panel(actor=Depends(census_identity)):
    """The current confirmation panel: per-language annotation progress, agreement, and whether the sealed read is unlocked."""
    _operator(actor)
    from services.training_lab import malpha, malpha_review
    from services.training_lab.malpha_evaluation import admission_preflight
    panel = await asyncio.to_thread(malpha_review.current_panel)
    records = await asyncio.to_thread(malpha.jobs)
    return {'tenant_id': actor['tenant_id'], 'panel': panel, 'preflight': admission_preflight(records, reference_panel=panel), 'reviewer': actor['principal_id']}


@router.get('/review/brands', response_model=c.Envelope)
async def review_brands(actor=Depends(census_identity)):
    _operator(actor)
    from services.training_lab import brand_catalogue
    active = await asyncio.to_thread(brand_catalogue.active)
    return {'tenant_id': actor['tenant_id'], 'version': active['version'], 'brands': sorted(b['brand'] for b in active['lexicon'])}


@router.get('/review/tasks', response_model=c.Envelope)
async def review_tasks(language: str | None = None, status: str | None = None, actor=Depends(census_identity)):
    _operator(actor)
    from services.training_lab import malpha_review
    panel = await asyncio.to_thread(malpha_review.current_panel)
    if not panel: return {'tenant_id': actor['tenant_id'], 'tasks': [], 'panel': None}
    return {'tenant_id': actor['tenant_id'], 'panel_id': panel['panel_id'], 'tasks': await asyncio.to_thread(malpha_review.tasks, panel['panel_id'], language, status)}


@router.get('/review/next', response_model=c.Envelope)
async def review_next(language: str | None = None, actor=Depends(census_identity)):
    """The next segment this reviewer has not heard. Transcript and transcript-derived labels are never returned."""
    _operator(actor)
    from services.training_lab import malpha_review
    panel = await asyncio.to_thread(malpha_review.current_panel)
    if not panel: return {'tenant_id': actor['tenant_id'], 'task': None, 'panel': None}
    return {'tenant_id': actor['tenant_id'], 'panel_id': panel['panel_id'], 'task': await asyncio.to_thread(malpha_review.next_task, panel['panel_id'], actor['principal_id'], language)}


@router.get('/review/tasks/{task_id}/audio')
async def review_audio(task_id: str, actor=Depends(census_identity)):
    _operator(actor)
    from services.training_lab import malpha_review
    try: wav = await asyncio.to_thread(malpha_review.audio_wav, task_id)
    except LookupError: raise HTTPException(404, 'No review task with that reference')
    except (ValueError, RuntimeError) as exc: raise HTTPException(502, f'Segment playback unavailable: {exc}')
    return Response(content=wav, media_type='audio/wav', headers={'Cache-Control': 'private, max-age=600'})


@router.post('/review/tasks/{task_id}/annotate', response_model=c.Envelope)
async def review_annotate(task_id: str, body: Annotation, actor=Depends(census_identity)):
    _operator(actor)
    from services.training_lab import brand_catalogue, malpha_review
    names = {b['brand'] for b in (await asyncio.to_thread(brand_catalogue.active))['lexicon']}
    try: task = await asyncio.to_thread(malpha_review.annotate, task_id, actor['principal_id'], body.brands, body.no_mention, body.unsure, names)
    except LookupError: raise HTTPException(404, 'No review task with that reference')
    except ValueError as exc: raise HTTPException(409, str(exc))
    return {'tenant_id': actor['tenant_id'], 'task': task}


@router.post('/review/tasks/{task_id}/adjudicate', response_model=c.Envelope)
async def review_adjudicate(task_id: str, body: Annotation, actor=Depends(census_identity)):
    _operator(actor)
    from services.training_lab import brand_catalogue, malpha_review
    names = {b['brand'] for b in (await asyncio.to_thread(brand_catalogue.active))['lexicon']}
    try: task = await asyncio.to_thread(malpha_review.adjudicate, task_id, actor['principal_id'], body.brands, names)
    except LookupError: raise HTTPException(404, 'No review task with that reference')
    except ValueError as exc: raise HTTPException(409, str(exc))
    return {'tenant_id': actor['tenant_id'], 'task': task}
