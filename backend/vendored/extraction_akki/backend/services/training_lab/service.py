"""Durable assessment and development-checkpoint review; never dispatches training."""
import asyncio
import os

from services.training_lab import evidence, store
from services.training_lab.reviewers import reviews


def plan_findings(data):
    return {'status':'held_before_retraining','training_started':False,
            'blockers':[
                {'ref':'music_labels','title':'Verified speech, music and mixed-audio labels are required'},
                {'ref':'evaluation_contract','title':'Music precision/recall floors and coverage targets need owner review'},
                {'ref':'independent_test','title':'Reserve a new independent test set; historical test results are already known'},
                {'ref':'recipe_approval','title':'Approve the data, recipe and evaluation plan before GPU retraining'}],
            'proposed_sequence':['Verify annotation rights and agreement by language and recording condition',
                'Calibrate speech/music thresholds; keep mixed and uncertain audio explicit',
                'Compare a separate music head with joint training using development-only feedback',
                'Review weaker-language accuracy, coverage and speaker leakage at checkpoints',
                'Evaluate once on the sealed final set; admission and serving remain separate'],
            'unsupported_models':'Other task families require their own qualified adapter and evaluation contract; not universally trainable.'}


async def process(row):
    try:
        request = row['request']
        if row['kind'] == 'weak_language_plan':
            from services.training_lab import languages
            data, bundle = languages.evidence(request.get('floor', 0.9))
            if bundle is None:
                store.update(row,status='held',hold_reason='No measured audio baseline certificate is available to read',report=data); return
            store.update(row,status='reviewing',evidence=bundle['aggregate'],report=bundle['report'],plan=bundle['plan'],deterministic={'status':'held_before_retraining','training_started':False,'below_floor':data['below_floor'],'at_risk':data['at_risk']})
            outcomes = await reviews(bundle['aggregate'],tenant=row['tenant_id'],actor=row['actor'],run_id=row['run_id']) if request.get('model_reviews',True) else []
            complete = sum(r['status']=='complete' for r in outcomes)
            store.update(row,status='complete' if not outcomes or complete==5 else 'partial',reviews=outcomes,specialist_reviews_complete=complete,finished_at=store.now(),outcome='held_before_retraining')
            return
        if row['kind']=='assessment' and request['inspect_existing_data'] and not row.get('inspection_job_id'):
            from services.training_runner import m9_dispatch
            from services.census_autonomy.operational_runner import admission_path
            store.update(row,status='dispatching')
            lawful,_ = admission_path()
            job = await asyncio.to_thread(m9_dispatch.submit,'lab_inspect',
                {'lab_corpus_root':os.environ['LANGUAGE_COGNITION_REMOTE_ROOT'],'gpu_index':0,
                 'owner_order_ref':'owner-training-lab-20260930-inspection-only'},
                request['host'],row['actor'],str(lawful))
            if job['status'] != 'running':
                store.update(row,status='held',hold_reason='Worker inspection was not started; review dispatch evidence',inspection_job_id=job['job_id'])
                return
            store.update(row,status='inspecting',inspection_job_id=job['job_id'])
            return
        data = row.get('evidence') or evidence.historical_evidence()
        if row.get('inspection_job_id'):
            from services.training_runner import m9_dispatch
            job = await asyncio.to_thread(m9_dispatch.refresh,row['inspection_job_id'])
            if job['status'] in ('running','submitting'):
                store.update(row,status='inspecting')
                return
            if job['status']!='completed' or not (job.get('receipt') or {}).get('digest_verified'):
                store.update(row,status='held',hold_reason='Inspection did not produce a verified terminal receipt')
                return
            result = job['receipt']['result']
            data['inspection'] = evidence.inspection_evidence(result)
            store.update(row,inspection=result,inspection_receipt_sha256=job['receipt']['receipt_sha256'])
        store.update(row,status='reviewing',evidence=data,deterministic=plan_findings(data))
        outcomes = await reviews(data,tenant=row['tenant_id'],actor=row['actor'],run_id=row['run_id']) if request.get('model_reviews',True) else []
        complete = sum(r['status']=='complete' for r in outcomes)
        store.update(row,status='complete' if not outcomes or complete==5 else 'partial',reviews=outcomes,
                     specialist_reviews_complete=complete,finished_at=store.now(),outcome='held_before_retraining')
    except Exception as exc:
        # No exception text (paths/credentials/provider payloads) exposed to the API.
        status = 'held' if row.get('status')=='dispatching' else 'failed'
        store.update(row,status=status,error_type=type(exc).__name__,
                     hold_reason='Assessment could not finish; no training or admission authorized')
    finally:
        store.release(row)


async def collect_checkpoints():
    settings = store.db().training_lab_watch.find_one({'tenant_id':'RMS','enabled':True},{'_id':0})
    if not settings:
        return
    from services.audio_plane_v1 import language_cognition_dispatch as lc
    for job in lc.list_jobs():
        if job.get('phase')!='train_corrective' or job.get('status')!='running':
            continue
        job = await asyncio.to_thread(lc.refresh,job['job_id'])
        data = evidence.checkpoint_evidence(job)
        if not data:
            continue
        key = f"checkpoint:{job['job_id']}:{data['checkpoint']['step']}"
        count = store.db().training_lab_runs.count_documents({'tenant_id':'RMS','source_job_id':job['job_id']})
        if count >= settings['max_checkpoints_per_job']:
            continue
        record,new = store.enqueue('RMS',settings['actor'],key,{'title':'Audio development checkpoint','model_reviews':True},kind='checkpoint',evidence=data)
        if new:
            store.db().training_lab_runs.update_one({'run_id':record['run_id'],'tenant_id':'RMS'},{'$set':{'source_job_id':job['job_id']}})


async def tick():
    await collect_checkpoints()
    # Bounded queue drain, not a persistent loop or scheduler. Work resumes next webhook.
    rows = []
    for _ in range(2):
        row = store.claim()
        if not row:
            break
        rows.append(row)
    await asyncio.gather(*(process(row) for row in rows))
    from services.training_lab import autopilot
    await autopilot.tick()