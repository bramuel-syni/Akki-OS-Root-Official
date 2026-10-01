"""Control-plane record of staged-corpus sound measurements run on the admitted GPU hosts (phase lab_measure)."""
import asyncio
import hashlib
import json
import os
import uuid
from functools import lru_cache

from services.training_lab import store as lab

OWNER_ORDER_REF = 'owner-direction-2026-10-01: measure staged corpus observables as the music-identification test set; no training'
HIDDEN = {'_id', 'actor'}


@lru_cache(maxsize=1)
def db():
    database = lab.db()
    database.training_lab_corpus_measurements.create_index([('tenant_id', 1), ('submitted_at', -1)])
    database.training_lab_corpus_profiles.create_index([('measurement_id', 1), ('ref', 1)], unique=True)
    database.training_lab_corpus_profiles.create_index([('tenant_id', 1), ('language', 1)])
    return database


def public(doc):
    return {k: v for k, v in doc.items() if k not in HIDDEN}


def latest(tenant):
    return db().training_lab_corpus_measurements.find_one({'tenant_id': tenant}, {'_id': 0}, sort=[('submitted_at', -1)])


def active(tenant):
    return db().training_lab_corpus_measurements.find_one({'tenant_id': tenant, 'status': {'$in': ['submitting', 'running']}}, {'_id': 0})


def dispatch(actor, body):
    from services.census_autonomy.operational_runner import admission_path
    from services.training_runner import m9_dispatch
    if active(actor['tenant_id']):
        raise ValueError('A corpus measurement is already running')
    host = body.get('host') or m9_dispatch.hosts()[0]
    params = {'lab_corpus_root': os.environ['LANGUAGE_COGNITION_REMOTE_ROOT'], 'workers': int(body.get('workers', 16)),
              'max_seconds': float(body.get('max_seconds', 5400)), 'max_files_per_language': int(body.get('max_files_per_language', 0)),
              'owner_order_ref': OWNER_ORDER_REF}
    lawful, _ = admission_path()
    doc = {'measurement_id': 'cm-' + uuid.uuid4().hex[:12], 'tenant_id': actor['tenant_id'], 'actor': actor['principal_id'], 'host': host,
           'params': params, 'submitted_at': lab.now(), 'updated_at': lab.now(), 'status': 'submitting', 'job_id': None, 'rows_stored': 0,
           'training_started': False, 'raw_media_exported': False}
    db().training_lab_corpus_measurements.insert_one(dict(doc))
    job = m9_dispatch.submit('lab_measure', params, host, actor['principal_id'], str(lawful))
    fields = {'job_id': job['job_id'], 'status': 'running' if job['status'] == 'running' else 'failed', 'updated_at': lab.now()}
    if job['status'] != 'running':
        fields['reason'] = 'Worker dispatch was refused; review dispatch evidence'
    db().training_lab_corpus_measurements.update_one({'measurement_id': doc['measurement_id']}, {'$set': fields})
    return {**public(doc), **fields}


def _store_rows(doc, text, expected_sha):
    if hashlib.sha256(text.encode()).hexdigest() != expected_sha:
        raise ValueError('Compact results digest did not match the worker receipt')
    rows = json.loads(text)
    collection = db().training_lab_corpus_profiles
    collection.delete_many({'measurement_id': doc['measurement_id']})
    batch = [{'measurement_id': doc['measurement_id'], 'tenant_id': doc['tenant_id'], **row} for row in rows]
    for start in range(0, len(batch), 500):
        collection.insert_many(batch[start:start + 500])
    return len(batch)


def refresh(doc):
    """One bounded status RPC; on a verified terminal receipt, fetch and store the compact rows."""
    from services.training_runner import m9_dispatch
    if doc['status'] != 'running' or not doc.get('job_id'):
        return doc
    job = m9_dispatch.refresh(doc['job_id'])
    progress = ((job or {}).get('remote_state') or {}).get('progress') or {}
    fields = {'updated_at': lab.now(), 'progress': {k: progress.get(k) for k in ('stage', 'files', 'of', 'elapsed_s')}}
    if job and job['status'] in ('running', 'submitting'):
        pass
    elif job and job['status'] == 'completed' and (job.get('receipt') or {}).get('digest_verified'):
        result = job['receipt']['result']
        try:
            text = m9_dispatch.fetch_artifact(doc['job_id'], 'results_compact.json', max_bytes=result['compact_rows_bytes'] + 16)
            fields.update(status='completed', result=result, rows_stored=_store_rows(doc, text, result['compact_rows_sha256']),
                          receipt_sha256=job['receipt']['receipt_sha256'], finished_at=job.get('finished_at'))
        except Exception as exc:
            fields.update(status='failed', reason=f'Results could not be retrieved: {type(exc).__name__}', result=result)
    else:
        fields.update(status='failed', reason=(job or {}).get('reason') or 'Worker did not produce a verified terminal receipt', finished_at=(job or {}).get('finished_at'))
    db().training_lab_corpus_measurements.update_one({'measurement_id': doc['measurement_id']}, {'$set': fields})
    return {**doc, **fields}


async def refresh_async(doc):
    return await asyncio.to_thread(refresh, doc)


def rows(tenant, measurement_id=None):
    doc = db().training_lab_corpus_measurements.find_one({'tenant_id': tenant, 'measurement_id': measurement_id} if measurement_id else {'tenant_id': tenant, 'status': 'completed'}, {'_id': 0}, sort=[('submitted_at', -1)])
    if not doc or doc['status'] != 'completed':
        return doc, []
    return doc, list(db().training_lab_corpus_profiles.find({'measurement_id': doc['measurement_id'], 'reads_as': {'$exists': True}}, {'_id': 0}))
