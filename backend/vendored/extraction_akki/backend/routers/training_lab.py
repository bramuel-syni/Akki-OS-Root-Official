"""Callable lab skills under existing tenant/operator identity and Watch boundaries."""
import hmac
import os
import re

from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException, Request
from pymongo.errors import DuplicateKeyError

from services.enforce.census_identity import census_identity
from services.watch import commission_gate
from services.training_lab import contracts as c, statistics as stats, store, service
from services.training_lab.music import classify_events
from services.training_lab.economics import value_case, score_predictions
from services.training_lab.reviewers import CATALOGUE

router = APIRouter(prefix='/api/training/lab',tags=['training-laboratory'])


def operator(actor):
    if not {'operator','master_admin'}.intersection(actor['roles']):
        raise HTTPException(403,'An admitted operator is required')


@router.get('/skills',response_model=c.Envelope)
def skills(actor=Depends(census_identity)):
    return {'tenant_id':actor['tenant_id'],'version':CATALOGUE['version'],
            'skills':[{'name':role,'kind':'model_advisory','call':'POST /api/training/lab/runs','authority':'advisory_only'} for role in CATALOGUE['roles']]
                     +[{'name':'evaluation-statistics','kind':'deterministic','call':'POST /api/training/lab/skills/statistics/invoke'},
                       {'name':'speech-music-decision','kind':'deterministic','call':'POST /api/training/lab/skills/music/invoke'},
                       {'name':'investment-scenarios','kind':'deterministic','call':'POST /api/training/lab/skills/value/invoke'},
                       {'name':'forecast-postmortem','kind':'deterministic','call':'POST /api/training/lab/skills/postmortem/invoke'}],
            'playbooks':CATALOGUE['playbooks'],'training_authorized':False,'music_detector_admitted':False}


@router.post('/skills/statistics/invoke',response_model=c.Envelope)
def statistics(body:c.StatisticsRequest,actor=Depends(census_identity)):
    operator(actor)
    try:
        if body.operation=='wilson': result=stats.wilson_interval(body.successes,body.n,body.confidence)
        elif body.operation=='bootstrap': result=stats.bootstrap_interval(body.values,seed=body.seed,confidence=body.confidence,draws=body.draws,groups=body.groups,paired=body.paired)
        elif body.operation=='power_law': result=stats.power_law_scenarios(body.points,body.exponent_bounds,body.irreducible_bounds,body.floor,body.cap)
        else: result=stats.monitoring_threshold(body.values,false_alert_rate=body.false_alert_rate,calibration_ref=body.calibration_ref)
    except (ValueError,TypeError,OverflowError) as exc:
        raise HTTPException(422,str(exc)) from exc
    return {'tenant_id':actor['tenant_id'],'result':result,'evidence_origin':'caller_supplied','admission_authority':False}


@router.post('/skills/music/invoke',response_model=c.Envelope)
def music(body:c.MusicRequest,actor=Depends(census_identity)):
    operator(actor)
    return {'tenant_id':actor['tenant_id'],'result':classify_events(**body.model_dump()),'music_detector_admitted':False}


@router.post('/runs',status_code=202,response_model=c.Envelope)
def submit(body:c.Assessment,background:BackgroundTasks,idempotency_key:str=Header(...,min_length=8,max_length=100),actor=Depends(census_identity)):
    operator(actor)
    if actor['tenant_id']!='RMS':
        raise HTTPException(403,'This staged-corpus assessment is authorized for RMS only')
    # Replaying a completed submission is a tenant-scoped read, not a new commission.
    try: previous=store.replay(actor['tenant_id'],idempotency_key,body.model_dump())
    except ValueError as exc: raise HTTPException(409,str(exc)) from exc
    if previous:
        return {'tenant_id':actor['tenant_id'],'run':store.public(previous),'created':False}
    with commission_gate.crossing(actor,'training_lab.assessment',body.model_dump()):
        try: row,new=store.enqueue(actor['tenant_id'],actor['principal_id'],idempotency_key,body.model_dump())
        except ValueError as exc: raise HTTPException(409,str(exc)) from exc
    background.add_task(service.tick)
    return {'tenant_id':actor['tenant_id'],'run':store.public(row),'created':new}


@router.post('/skills/value/invoke',response_model=c.Envelope)
def value(body:c.ValueRequest,actor=Depends(census_identity)):
    operator(actor)
    try: result=value_case(**body.model_dump())
    except ValueError as exc: raise HTTPException(422,str(exc)) from exc
    return {'tenant_id':actor['tenant_id'],'result':result}


@router.post('/skills/postmortem/invoke',response_model=c.Envelope)
def postmortem(body:c.PostmortemRequest,actor=Depends(census_identity)):
    operator(actor)
    try: result=score_predictions([p.model_dump() for p in body.predictions])
    except ValueError as exc: raise HTTPException(422,str(exc)) from exc
    return {'tenant_id':actor['tenant_id'],'result':result}


@router.get('/runs',response_model=c.Envelope)
def runs(actor=Depends(census_identity)):
    rows=store.db().training_lab_runs.find({'tenant_id':actor['tenant_id']},{'_id':0}).sort('created_at',-1).limit(30)
    return {'tenant_id':actor['tenant_id'],'runs':[store.public(row) for row in rows]}


@router.post('/runs/{run_id}/review',status_code=202,response_model=c.Envelope)
def review_again(run_id:str,background:BackgroundTasks,idempotency_key:str=Header(...,min_length=8,max_length=100),actor=Depends(census_identity)):
    operator(actor)
    row=store.get(actor['tenant_id'],run_id)
    if not row: raise HTTPException(404,'Assessment not found')
    if actor['tenant_id']!='RMS' or row['status'] not in ('complete','partial') or not row.get('evidence'):
        raise HTTPException(409,'A completed aggregate assessment is required')
    body={'title':'Audio research follow-up','source_assessment':run_id,'model_reviews':True}
    try: previous=store.replay(actor['tenant_id'],idempotency_key,body)
    except ValueError as exc: raise HTTPException(409,str(exc)) from exc
    if previous: return {'tenant_id':actor['tenant_id'],'run':store.public(previous),'created':False}
    # One explicit correction pass per assessment. No self-improvement spending loop.
    if store.db().training_lab_runs.count_documents({'tenant_id':actor['tenant_id'],'request.source_assessment':run_id}):
        raise HTTPException(409,'Follow-up already exists; review its evidence before further work')
    if row['kind']=='research_followup': raise HTTPException(409,'Research follow-ups cannot recursively commission more reviews')
    with commission_gate.crossing(actor,'training_lab.assessment',body):
        try: child,new=store.enqueue(actor['tenant_id'],actor['principal_id'],idempotency_key,body,kind='research_followup',evidence=row['evidence'])
        except ValueError as exc: raise HTTPException(409,str(exc)) from exc
    background.add_task(service.tick)
    return {'tenant_id':actor['tenant_id'],'run':store.public(child),'created':new}


@router.get('/runs/{run_id}',response_model=c.Envelope)
def run(run_id:str,actor=Depends(census_identity)):
    row=store.get(actor['tenant_id'],run_id)
    if not row: raise HTTPException(404,'Assessment not found')
    return {'tenant_id':actor['tenant_id'],'run':store.public(row)}


@router.put('/watch',response_model=c.Envelope)
def watch(body:c.Watch,actor=Depends(census_identity)):
    operator(actor)
    if actor['tenant_id']!='RMS': raise HTTPException(403,'Audio checkpoint watch is RMS-scoped')
    with commission_gate.crossing(actor,'training_lab.watch',body.model_dump()):
        store.db().training_lab_watch.update_one({'tenant_id':'RMS'},{'$set':{**body.model_dump(),'actor':actor['principal_id'],'updated_at':store.now()}},upsert=True)
    return {'tenant_id':'RMS',**body.model_dump(),'cadence_minutes':15,'scope':'development_only','training_authorized':False}


@router.get('/watch',response_model=c.Envelope)
def watch_status(actor=Depends(census_identity)):
    row=store.db().training_lab_watch.find_one({'tenant_id':actor['tenant_id']},{'_id':0,'actor':0})
    return {'tenant_id':actor['tenant_id'],'watch':row or {'enabled':False}}


@router.post('/cron')
async def cron(request:Request,background:BackgroundTasks,authorization:str|None=Header(default=None),x_webhook_id:str|None=Header(default=None)):
    # Cron endpoints must ack 2xx immediately; enqueue/background the actual work.
    expected=os.environ['WEBHOOK_CRON_SECRET']
    supplied=authorization[7:] if authorization and authorization.startswith('Bearer ') else ''
    if not supplied or not hmac.compare_digest(supplied,expected): raise HTTPException(401,'Invalid scheduler authorization')
    try:
        body=await request.json()
        if not isinstance(body,dict) or body.get('event')!='schedule.triggered' or not isinstance(body.get('run_id'),str) or not body['run_id'] or body.get('data') is not None:
            raise ValueError()
        key=x_webhook_id or body['run_id']
        if not re.fullmatch(r'[a-zA-Z0-9_.:-]{1,150}',key): raise ValueError()
    except Exception as exc: raise HTTPException(400,'Invalid schedule envelope') from exc
    try: store.db().training_lab_webhooks.insert_one({'run_id':key,'received_at':store.now()})
    except DuplicateKeyError: return {'accepted':True,'duplicate':True}
    background.add_task(service.tick)
    return {'accepted':True,'duplicate':False}