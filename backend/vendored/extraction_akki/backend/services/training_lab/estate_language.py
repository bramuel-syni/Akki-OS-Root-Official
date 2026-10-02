"""Control-plane record of the estate language evidence jobs: both GPUs on the admitted host read the staged corpus with the
admitted music detector and the current audio language model (phase lab_classify_estate); the served text model reads the
transcripts on its own host (phase lab_text_lid). Owner order 2026-10-02; aggregate cap counted across every device."""
import hashlib
import json
import os
import uuid

from services.training_lab import store as lab

OWNER_ORDER_REF = ('owner order 2026-10-02: measure estate-held non-English, non-music audio and text by language, hours and quality on both GPUs '
                   'with the current cognition models; 6 GPU-hours aggregate across both devices; evidence for the estate report; no training')
AUDIO_MODEL_JOB = 'lcj-7128593897d4'        # Luhya v3 corrective checkpoint, admitted for Wanga on 2026-10-02 (owner order); research-grade elsewhere
MUSIC_MODEL_JOB = 'm9j-686de001bfe7'        # admitted music detector
TEXT_MODEL_JOB = 'm9j-74af7cef0a85'         # admitted 8B text language identification adapter (served)
CAP_GPU_HOURS = 6.0
HIDDEN = {'_id', 'actor'}


def db():
    database = lab.db()
    database.training_lab_estate_language.create_index([('tenant_id', 1), ('submitted_at', -1)])
    database.training_lab_estate_language_rows.create_index([('job_id', 1), ('ref', 1)], unique=True)
    return database


def public(doc):
    return {k: v for k, v in doc.items() if k not in HIDDEN}


def latest(tenant, kind=None):
    query = {'tenant_id': tenant, **({'kind': kind} if kind else {})}
    return db().training_lab_estate_language.find_one(query, {'_id': 0}, sort=[('submitted_at', -1)])


def active(tenant):
    return list(db().training_lab_estate_language.find({'tenant_id': tenant, 'status': {'$in': ['submitting', 'running']}}, {'_id': 0}))


def _models():
    from services.audio_plane_v1 import language_cognition_dispatch as lc
    from services.training_runner import m9_dispatch, m9_serving
    audio = lc.load_job(AUDIO_MODEL_JOB) or {}
    music = m9_dispatch.load_job(MUSIC_MODEL_JOB) or {}
    served = next((a for a in m9_serving.models_view()['trained_adapters'] if a['training_job_id'] == TEXT_MODEL_JOB and (a.get('serving') or {}).get('status') == 'running'), None)
    return {'audio': {'job_id': AUDIO_MODEL_JOB, 'host': audio.get('host'), 'sha256': (audio.get('run_certificate') or {}).get('artefact_sha256'),
                      'dir': f"{os.environ['LANGUAGE_COGNITION_REMOTE_ROOT']}/artefacts/{AUDIO_MODEL_JOB}"},
            'music': {'job_id': MUSIC_MODEL_JOB, 'host': music.get('host'), 'sha256': (((music.get('receipt') or {}).get('result') or {}).get('artefact') or {}).get('sha256'),
                      'path': f"{os.environ['M9_REMOTE_ROOT']}/jobs/{MUSIC_MODEL_JOB}/artefact/music_detector.pt"},
            'text': {'job_id': TEXT_MODEL_JOB, 'serving': {k: served['serving'].get(k) for k in ('job_id', 'host', 'port', 'gpu_index')} if served else None}}


def dispatch(actor, body=None):
    """Two jobs: every GPU on the audio host, and the served text model on its host. One record each; the cap is shared."""
    from services.census_autonomy.operational_runner import admission_path
    body = body or {}
    if active(actor['tenant_id']): raise ValueError('An estate language job is already running')
    models = _models(); lawful, _ = admission_path(); out = []
    kinds = {body.get('kind')} if body.get('kind') in ('audio', 'text') else {'audio', 'text'}
    cap = float(body.get('compute_cap_gpu_hours', CAP_GPU_HOURS))
    if 'audio' in kinds:
        audio_host = body.get('host') or models['audio']['host'] or 'akki-vm'
        audio_params = {'lab_corpus_root': os.environ['LANGUAGE_COGNITION_REMOTE_ROOT'], 'audio_model_dir': models['audio']['dir'], 'audio_model_sha256': models['audio']['sha256'],
                        'music_model_path': models['music']['path'], 'music_model_sha256': models['music']['sha256'], 'compute_cap_gpu_hours': cap - 0.5 if 'text' in kinds else cap,
                        'max_seconds_per_file': float(body.get('max_seconds_per_file', 5400)), 'max_windows_per_file': int(body.get('max_windows_per_file', 900)),
                        'batch_size': int(body.get('batch_size', 256)), 'owner_order_ref': OWNER_ORDER_REF}
        out.append(_submit(actor, 'audio', 'lab_classify_estate', audio_params, audio_host, lawful, models))
    serving = models['text']['serving']
    if 'text' in kinds and serving:
        text_params = {'lab_corpus_root': os.environ['LANGUAGE_COGNITION_REMOTE_ROOT'], 'port': int(serving['port']), 'chunk_chars': 1500, 'batch_size': 32,
                       'compute_cap_gpu_hours': 0.5 if 'audio' in kinds else cap, 'owner_order_ref': OWNER_ORDER_REF, 'interleave': bool(body['interleave']) if body.get('interleave') is not None else kinds == {'text'}}
        if body.get('skip_completed'):
            # A continuation pass: every transcript already read by a completed text job stays read; this pass takes the rest.
            text_params['skip_refs'] = sorted(db().training_lab_estate_language_rows.distinct('ref', {'tenant_id': actor['tenant_id'], 'kind': 'text'}))
        out.append(_submit(actor, 'text', 'lab_text_lid', text_params, serving['host'], lawful, models))
    return out


def _submit(actor, kind, phase, params, host, lawful, models):
    from services.training_runner import m9_dispatch
    doc = {'estate_language_id': 'el-' + uuid.uuid4().hex[:12], 'kind': kind, 'tenant_id': actor['tenant_id'], 'actor': actor['principal_id'], 'host': host, 'phase': phase,
           'params': params, 'models': models, 'submitted_at': lab.now(), 'updated_at': lab.now(), 'status': 'submitting', 'job_id': None, 'rows_stored': 0, 'training_started': False}
    db().training_lab_estate_language.insert_one(dict(doc))
    try:
        job = m9_dispatch.submit(phase, params, host, actor['principal_id'], str(lawful))
    except Exception as exc:
        db().training_lab_estate_language.update_one({'estate_language_id': doc['estate_language_id']}, {'$set': {'status': 'failed', 'reason': f'dispatch refused: {str(exc)[:200]}', 'updated_at': lab.now()}})
        raise
    fields = {'job_id': job['job_id'], 'status': 'running' if job['status'] == 'running' else 'failed', 'updated_at': lab.now()}
    if job['status'] != 'running': fields['reason'] = job.get('reason') or 'Worker dispatch was refused'
    db().training_lab_estate_language.update_one({'estate_language_id': doc['estate_language_id']}, {'$set': fields})
    return {**public(doc), **fields}


def _store_rows(doc, text, expected_sha):
    if hashlib.sha256(text.encode()).hexdigest() != expected_sha: raise ValueError('Compact results digest did not match the worker receipt')
    rows = json.loads(text); collection = db().training_lab_estate_language_rows
    collection.delete_many({'job_id': doc['job_id']})
    batch = [{'job_id': doc['job_id'], 'kind': doc['kind'], 'tenant_id': doc['tenant_id'], **row} for row in rows]
    for start in range(0, len(batch), 500): collection.insert_many(batch[start:start + 500])
    return len(batch)


def refresh(doc):
    from services.training_runner import m9_dispatch
    if doc['status'] != 'running' or not doc.get('job_id'): return doc
    job = m9_dispatch.refresh(doc['job_id'])
    progress = ((job or {}).get('remote_state') or {}).get('progress') or {}
    fields = {'updated_at': lab.now(), 'progress': {k: progress.get(k) for k in ('stage', 'files', 'of', 'windows', 'elapsed_s', 'per_device', 'devices')}}
    if job and job['status'] in ('running', 'submitting'): pass
    elif job and job['status'] == 'completed' and (job.get('receipt') or {}).get('digest_verified'):
        result = job['receipt']['result']
        try:
            text = m9_dispatch.fetch_artifact(doc['job_id'], 'results_compact.json', max_bytes=result['compact_rows_bytes'] + 16)
            fields.update(status='completed', result=result, rows_stored=_store_rows(doc, text, result['compact_rows_sha256']), receipt_sha256=job['receipt']['receipt_sha256'], finished_at=job.get('finished_at'))
        except Exception as exc:
            fields.update(status='failed', reason=f'Results could not be retrieved: {type(exc).__name__}', result=result)
    else:
        fields.update(status='failed', reason=((job or {}).get('receipt') or {}).get('error', {}).get('message') or (job or {}).get('reason') or 'Worker did not produce a verified terminal receipt', finished_at=(job or {}).get('finished_at'))
    db().training_lab_estate_language.update_one({'estate_language_id': doc['estate_language_id']}, {'$set': fields})
    return {**doc, **fields}


def refresh_all(tenant):
    return [refresh(doc) for doc in active(tenant)]


def status(tenant):
    audio, text = latest(tenant, 'audio'), latest(tenant, 'text')
    return {'audio': audio, 'text': text, 'cap_gpu_hours': CAP_GPU_HOURS, 'order': OWNER_ORDER_REF}


def rows(tenant, kind='audio'):
    doc = latest(tenant, kind)
    if not doc or doc['status'] != 'completed': return doc, []
    return doc, list(db().training_lab_estate_language_rows.find({'job_id': doc['job_id']}, {'_id': 0}))


def completed(tenant, kind):
    """Every completed job of a kind, newest first, with its rows — continuation passes add to the evidence rather than replace it."""
    docs = list(db().training_lab_estate_language.find({'tenant_id': tenant, 'kind': kind, 'status': 'completed'}, {'_id': 0}, sort=[('submitted_at', -1)]))
    seen, out = set(), []
    for doc in docs:
        fresh = [r for r in db().training_lab_estate_language_rows.find({'job_id': doc['job_id']}, {'_id': 0}) if r['ref'] not in seen]
        seen.update(r['ref'] for r in fresh); out.append((doc, fresh))
    return out
