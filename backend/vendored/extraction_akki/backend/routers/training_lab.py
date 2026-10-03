"""Callable lab skills under existing tenant/operator identity and Watch boundaries."""
import asyncio
import hmac
import os
import re
import uuid
from typing import Literal

from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException, Request
from pydantic import Field
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


@router.post('/baselines/music',status_code=202,response_model=c.Envelope)
def music_baseline(body:c.MusicBaseline,idempotency_key:str=Header(...,min_length=8,max_length=100),actor=Depends(census_identity)):
    operator(actor)
    from services.training_lab import baseline
    try: previous=store.replay(actor['tenant_id'],idempotency_key,body.model_dump())
    except ValueError as exc: raise HTTPException(409,str(exc)) from exc
    if previous: return {'tenant_id':actor['tenant_id'],'run':store.public(previous),'created':False}
    with commission_gate.crossing(actor,'training_lab.baseline',body.model_dump()):
        try: row,new=baseline.submit(actor,idempotency_key,body.model_dump())
        except ValueError as exc: raise HTTPException(409,str(exc)) from exc
    return {'tenant_id':actor['tenant_id'],'run':store.public(row),'created':new}


@router.get('/baselines/music',response_model=c.Envelope)
def music_baselines(actor=Depends(census_identity)):
    rows=store.db().training_lab_runs.find({'tenant_id':actor['tenant_id'],'kind':'music_baseline'},{'_id':0}).sort('created_at',-1).limit(20)
    return {'tenant_id':actor['tenant_id'],'runs':[store.public(row) for row in rows]}


@router.post('/corpus-measurements',status_code=202,response_model=c.Envelope)
def corpus_measurement_dispatch(body:c.CorpusMeasurement,actor=Depends(census_identity)):
    operator(actor)
    if actor['tenant_id']!='RMS': raise HTTPException(403,'The staged corpus is RMS custody')
    from services.training_lab import corpus_measurement
    with commission_gate.crossing(actor,'training_lab.corpus_measurement',body.model_dump()):
        try: doc=corpus_measurement.dispatch(actor,body.model_dump())
        except ValueError as exc: raise HTTPException(409,str(exc)) from exc
    return {'tenant_id':actor['tenant_id'],'measurement':doc}


@router.get('/corpus-measurements',response_model=c.Envelope)
async def corpus_measurement_status(actor=Depends(census_identity)):
    from services.training_lab import corpus_measurement
    doc=corpus_measurement.latest(actor['tenant_id'])
    if doc and doc['status']=='running': doc=await corpus_measurement.refresh_async(doc)
    return {'tenant_id':actor['tenant_id'],'measurement':corpus_measurement.public(doc) if doc else None}


class EstateLanguageDispatch(c.Closed):
    compute_cap_gpu_hours:float=Field(default=6.0,gt=0,le=12)
    max_windows_per_file:int=Field(default=900,ge=1,le=5000)
    kind:Literal['audio','text']|None=None
    skip_completed:bool=False
    interleave:bool|None=None


@router.post('/estate-language',status_code=202,response_model=c.Envelope)
def estate_language_dispatch(body:EstateLanguageDispatch,actor=Depends(census_identity)):
    operator(actor)
    if actor['tenant_id']!='RMS': raise HTTPException(403,'The staged corpus is RMS custody')
    from services.training_lab import estate_language
    with commission_gate.crossing(actor,'training_lab.corpus_measurement',body.model_dump()):
        try: docs=estate_language.dispatch(actor,body.model_dump())
        except ValueError as exc: raise HTTPException(409,str(exc)) from exc
    return {'tenant_id':actor['tenant_id'],'jobs':docs}


@router.get('/estate-language',response_model=c.Envelope)
async def estate_language_status(actor=Depends(census_identity)):
    from services.census_autonomy import text_estate_evidence
    from services.training_lab import estate_language
    await asyncio.to_thread(estate_language.refresh_all,actor['tenant_id'])
    text_estate=await asyncio.to_thread(lambda: text_estate_evidence.refresh(text_estate_evidence.latest(actor['tenant_id'])))
    return {'tenant_id':actor['tenant_id'],**estate_language.status(actor['tenant_id']),'text_estate':text_estate}


@router.post('/text-estate',status_code=202,response_model=c.Envelope)
def text_estate_dispatch(kind:str='aggregates',actor=Depends(census_identity)):
    """Aggregate-only read of the written-word stores: `aggregates` (scripts per station, workbench text per language) or `profiles`
    (character-trigram profiles of the scripts per station and the transcripts per language, so each station's language is identified from its script)."""
    operator(actor)
    if actor['tenant_id']!='RMS': raise HTTPException(403,'The written-word stores are RMS custody')
    from services.census_autonomy import text_estate_evidence
    if kind not in text_estate_evidence.KINDS: raise HTTPException(422,'kind must be aggregates, profiles or locations')
    with commission_gate.crossing(actor,'training_lab.corpus_measurement',{'kind':kind,'targets':[t['database'] for t in text_estate_evidence.KINDS[kind][0]]}):
        try: doc=text_estate_evidence.dispatch(actor,kind)
        except ValueError as exc: raise HTTPException(409,str(exc)) from exc
    return {'tenant_id':actor['tenant_id'],'job':doc}


@router.get('/text-estate/profiles',response_model=c.Envelope)
async def text_estate_profiles(actor=Depends(census_identity)):
    from services.census_autonomy import text_estate_evidence
    doc=await asyncio.to_thread(lambda: text_estate_evidence.refresh(text_estate_evidence.latest(actor['tenant_id'],'profiles')))
    return {'tenant_id':actor['tenant_id'],'job':doc}



@router.get('/languages/weak',response_model=c.Envelope)
def weak_languages(floor:float=0.9,actor=Depends(census_identity)):
    from services.training_lab import languages
    if not 0.5<=floor<=0.999: raise HTTPException(422,'Floor must be between 0.5 and 0.999')
    data=languages.report(floor)
    return {'tenant_id':actor['tenant_id'],'report':data,'plan':languages.plan(data) if data['status']=='measured' else None,'training_authorized':False}


@router.post('/languages/reinforcement',status_code=202,response_model=c.Envelope)
def reinforcement(body:c.Reinforcement,background:BackgroundTasks,idempotency_key:str=Header(...,min_length=8,max_length=100),actor=Depends(census_identity)):
    operator(actor)
    if actor['tenant_id']!='RMS': raise HTTPException(403,'Audio cognition evidence is RMS custody')
    try: previous=store.replay(actor['tenant_id'],idempotency_key,body.model_dump())
    except ValueError as exc: raise HTTPException(409,str(exc)) from exc
    if previous: return {'tenant_id':actor['tenant_id'],'run':store.public(previous),'created':False}
    with commission_gate.crossing(actor,'training_lab.reinforcement_plan',body.model_dump()):
        try: row,new=store.enqueue(actor['tenant_id'],actor['principal_id'],idempotency_key,body.model_dump(),kind='weak_language_plan')
        except ValueError as exc: raise HTTPException(409,str(exc)) from exc
    background.add_task(service.tick)
    return {'tenant_id':actor['tenant_id'],'run':store.public(row),'created':new}


@router.get('/languages/reinforcement',response_model=c.Envelope)
def reinforcement_runs(actor=Depends(census_identity)):
    rows=store.db().training_lab_runs.find({'tenant_id':actor['tenant_id'],'kind':'weak_language_plan'},{'_id':0}).sort('created_at',-1).limit(10)
    return {'tenant_id':actor['tenant_id'],'runs':[store.public(row) for row in rows]}


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


# ----------------------------------------------------------------------------- the owner's Train Models studio
class BoardMessage(c.Closed):
    text:str=Field(min_length=1,max_length=2000)


class BoardAction(c.Closed):
    action:Literal['run_music_baseline','measure_staged_corpus','import_reference_recordings','ask_specialists','record_training_request','approve_plan','use_baseline','white_paper','retire']
    value:str|None=Field(default=None,max_length=120)


class BoardNew(c.Closed):
    from_run:str|None=Field(default=None,max_length=80)
    mode:Literal['new','next_version','adjust']='new'


def _board_run(tenant,run_id):
    from services.training_lab import board
    run=next((r for r in board.runs(tenant) if r['run_id']==run_id),None)
    if not run: raise HTTPException(404,'No training run with that reference is on your board')
    return run


async def _perform(actor,run,action,value,background):
    """The control plane performs the bounded action itself and reports back in Akki's voice. Training is never performed."""
    from services.training_lab import conversation, board_runs
    tenant=actor['tenant_id']; key='train-models:'+uuid.uuid4().hex[:12]
    try:
        if action=='run_music_baseline':
            from services.training_lab import baseline
            body={'unlabelled_library_audio':'music','include_synthetic':True,'include_corpus_test':True}
            with commission_gate.crossing(actor,'training_lab.baseline',body): row,_=baseline.submit(actor,key,body)
            ref=row.get('reference_set') or {}; pending=len(ref.get('pending') or [])
            text=(f"Baseline requested on {ref.get('measured',0)} labelled recordings." + (f" {pending} still need their sound profile measured first; it completes on its own." if pending else ' It is being established now.'))
        elif action=='measure_staged_corpus':
            from services.training_lab import corpus_measurement
            if tenant!='RMS': raise ValueError('The staged corpus is RMS custody')
            body={'host':'akki-vm','workers':16,'max_seconds':5400,'max_files_per_language':0}
            with commission_gate.crossing(actor,'training_lab.corpus_measurement',body): corpus_measurement.dispatch(actor,body)
            text='Measuring the staged corpus on akki-vm — readings only, no training, no media leaves the host. I will report here as it progresses.'
        elif action=='import_reference_recordings':
            from services.media_library import reference_import as reference
            with commission_gate.crossing(actor,'media.reference_import',{'catalogue_items':len(reference.CATALOGUE)}): doc,created=reference.start(actor)
            text='Importing the public-domain reference recordings into the library; they stay apart from your music and are never counted as training data.' if created else 'The reference import is already running.'
        elif action=='ask_specialists':
            if tenant!='RMS': raise ValueError('Audio cognition evidence is RMS custody')
            body={'title':'Weak-language reinforcement plan','floor':0.9,'model_reviews':True}
            with commission_gate.crossing(actor,'training_lab.reinforcement_plan',body): store.enqueue(tenant,actor['principal_id'],key,body,kind='weak_language_plan')
            background.add_task(service.tick)
            text='Asked the five specialists to review the plan. Their advice is advisory and machine-checked for ungrounded figures; it arrives in this thread.'
        elif action=='record_training_request':
            if run.get('family')=='owner':
                if not run.get('ready'): raise ValueError('the target outcome and collection schema need their full population, acceptance, source and budget definitions')
                from services.training_lab import production
                doc = board_runs.get(tenant, run['run_id'])
                with commission_gate.crossing(actor,'training_lab.training_request',{'run_id':run['run_id']}):
                    production.compile_plan(tenant, actor, run['run_id'], doc.get('definition'))
                    board_runs.hold(tenant,run['run_id'])
            text='Recorded: you are asking for this training. The request stays held until the recipe, compute cap and evaluation contract are approved through Model Approval; nothing has started.'
        elif action=='approve_plan':
            from services.training_lab import signoff, autopilot
            if not value: raise ValueError('the plan digest shown on the run must accompany the approval')
            with commission_gate.crossing(actor,'training_lab.training_request',{'run_id':run['run_id'],'plan_sha256':value,'signoff':True}):
                record=signoff.sign(tenant,actor,run['run_id'],value)
            plan=record['plan']
            autopilot.kick(background)
            text=(f"Signed off by {signoff.signer_label(actor['principal_id'])} — digest {record['plan_sha256'][:12]}. That signature is the only thing that starts training here: "
                  f"I am dispatching it now to {plan['host']} GPU {plan['gpu_index']} with exactly the recipe, data and {plan['compute_cap_gpu_hours']} GPU-hour cap you approved, "
                  "and I will judge the result against the acceptance you signed, write the findings paper, and report back in this thread.")
            note=conversation.note(tenant,text,widget='action',action=action,signoff={'plan_sha256':record['plan_sha256'],'signed_by':record['signed_by'],'signed_at':record['signed_at']})
            conversation.record(tenant,run['run_id'],note)
            return note
        elif action=='use_baseline':
            text=f"Starting point recorded: {'the learned baseline on the measured observables' if value=='learned' else 'the acoustic reading'}. A detector only earns its place by beating it on recordings it has not seen."
        elif action=='retire':
            if run['status'] not in ('Refused','In service'): raise ValueError('only a refused or served run can be retired')
            if run.get('health'): raise ValueError('a served model is retired through Model Approval, where its calls are disabled first')
            with commission_gate.crossing(actor,'training_lab.retire',{'run_id':run['run_id']}): board_runs.retire(tenant,actor,run['run_id'])
            text='Retired. The record, the checks and the reason stay exactly as written; only the status changed.'
        else:
            from services.transform_forms.doc_studio import service as studio
            source=((run.get('approval') or {}).get('dispatch') or {}).get('job_id') or run['run_id']
            with commission_gate.crossing(actor,'training_lab.whitepaper',{'run_id':run['run_id'],'source':source}):
                document, created = await studio.create_authored('training-whitepaper', source, tenant, actor['principal_id'])
            gate=(document.get('authoring') or {}).get('gate') or {}
            text=('The findings paper is written in Documents from this run’s measured record — authored by the frontier writer, every figure by reference, gated by the content manager before its build.'
                  if gate.get('passed') else 'The frontier writer drafted the paper but the content manager rejected it, so no document was built; the rejection reasons are recorded on the commission in Documents.')
            note=conversation.note(tenant,text,widget='doc',action=action,commission_id=document['commission_id'])
            conversation.record(tenant,run['run_id'],note)
            return note
    except (ValueError, LookupError) as exc:
        if 'unknown protected boundary' in str(exc):
            text='The action could not be completed. No training or admission was started.'
        else:
            text=f"Not done: {exc}."
    note=conversation.note(tenant,text,widget='action',action=action)
    conversation.record(tenant,run['run_id'],note)
    return note


@router.get('/board',response_model=c.Envelope)
async def board_view(background:BackgroundTasks,actor=Depends(census_identity)):
    from services.training_lab import board, conversation, autopilot
    await asyncio.to_thread(autopilot.refresh_running, autopilot.REFRESH_AGE_S)
    data=await asyncio.to_thread(board.board,actor['tenant_id'])
    if any((run.get('approval') or {}).get('awaiting_judgement') for run in data['runs']): autopilot.kick(background)
    for run in data['runs']:
        run['messages']=run['messages']+conversation.messages(actor['tenant_id'],run['run_id'])
    return {'tenant_id':actor['tenant_id'],**data}


@router.post('/board/new',status_code=201,response_model=c.Envelope)
async def board_new(body:BoardNew,actor=Depends(census_identity)):
    operator(actor)
    from services.training_lab import board, board_runs, conversation
    tenant=actor['tenant_id']; parent=None; name=None
    rows=await asyncio.to_thread(board.runs,tenant)
    if body.from_run:
        parent=next((r for r in rows if r['run_id']==body.from_run),None)
        if not parent: raise HTTPException(404,'No training run with that reference is on your board')
        if body.mode=='new': raise HTTPException(422,'Choose next_version or adjust when opening from an earlier run')
        name=board_runs.next_version(parent['name'],[r['name'] for r in rows])
    with commission_gate.crossing(actor,'training_lab.shape_run',{'from_run':body.from_run,'mode':body.mode}):
        doc=board_runs.create(tenant,actor,parent=parent,mode=body.mode,name=name)
    opening=board_runs.OPENING if not parent else (board_runs.ADJUST if body.mode=='adjust' else board_runs.NEXT_VERSION).format(parent=parent['name'])
    conversation.record(tenant,doc['run_id'],conversation.note(tenant,opening,think=['The outcome and collection schema remain separate. Calibration must precede the full-run quote.'] + (['The earlier run keeps its own record and status.'] if parent else [])))
    return {'tenant_id':tenant,'run_id':doc['run_id'],'name':doc['name'],'status':doc['status'],'training_started':False}


@router.delete('/board/{run_id}',status_code=204)
async def board_delete(run_id:str,actor=Depends(census_identity)):
    operator(actor)
    from services.training_lab import board_runs
    if not board_runs.delete(actor['tenant_id'],run_id): raise HTTPException(409,'Only a run still being shaped here can be deleted; recorded runs keep their record')
    return None


@router.post('/board/{run_id}/messages',response_model=c.Envelope)
async def board_message(run_id:str,body:BoardMessage,background:BackgroundTasks,actor=Depends(census_identity)):
    operator(actor)
    from services.training_lab import conversation
    run=await asyncio.to_thread(_board_run,actor['tenant_id'],run_id)
    user,reply=await conversation.turn(actor['tenant_id'],actor,run,body.text)
    out=[user,reply]
    if reply.get('action'): out.append(await _perform(actor,run,reply['action'],None,background))
    return {'tenant_id':actor['tenant_id'],'messages':out,'training_started':False}


@router.post('/board/{run_id}/actions',response_model=c.Envelope)
async def board_action(run_id:str,body:BoardAction,background:BackgroundTasks,actor=Depends(census_identity)):
    operator(actor)
    from services.training_lab import conversation
    run=await asyncio.to_thread(_board_run,actor['tenant_id'],run_id)
    labels={'run_music_baseline':'Run the baseline','measure_staged_corpus':'Measure the staged corpus','import_reference_recordings':'Import the reference recordings','ask_specialists':'Ask the five specialists',
            'record_training_request':'Begin training','approve_plan':'Approve and start','use_baseline':'Start from this','white_paper':'Prepare white paper','retire':'Retire this attempt'}
    decided=conversation.decision(actor['tenant_id'],labels[body.action],action=body.action,value=body.value)
    conversation.record(actor['tenant_id'],run['run_id'],decided)
    return {'tenant_id':actor['tenant_id'],'messages':[decided,await _perform(actor,run,body.action,body.value,background)],'training_started':False}


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