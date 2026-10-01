"""Measured sound profiles for library audio: durable job rows, one in-process worker, pattern register."""
import logging
import os
import tempfile
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone
from functools import lru_cache

import numpy as np
from pymongo import ReturnDocument

from services.audio_plane_v1 import acoustic_observables as ao
from services.media_library import storage, store
from services.training_lab import store as lab

log = logging.getLogger('media.acoustics')
CLASSES = ('speech', 'music', 'mixed', 'noise', 'silence')
HIDDEN = {'_id', 'lease_token', 'lease_until', 'requested_by'}
PATTERN_KEYS = ('energy.modulation_4hz_ratio', 'wave.low_energy_frame_ratio', 'tone.sustained_tone_ratio', 'energy.pulse_clarity', 'energy.tempo_bpm',
                'tone.voiced_ratio', 'tone.f0_median_hz', 'tone.f0_range_semitones', 'tone.pitch_jump_semitones', 'frequency.spectral_centroid_hz.p50',
                'frequency.spectral_flatness.p50', 'frequency.spectral_flux.p50', 'wave.zero_crossing_rate_hz.std', 'wave.dynamic_range_db', 'wave.rms_dbfs',
                'wave.silence_ratio', 'energy.pause_rate_per_min', 'energy.syllable_rate_proxy_hz', 'timbre.brightness', 'frequency.effective_bandwidth_hz')
_worker_started = threading.Event()


@lru_cache(maxsize=1)
def db():
    database = store.db()
    database.media_acoustics.create_index([('tenant_id', 1), ('file_id', 1)], unique=True)
    database.media_acoustics.create_index([('status', 1), ('lease_until', 1)])
    return database


def public(job):
    return {k: v for k, v in job.items() if k not in HIDDEN}


def get(tenant, file_id):
    return db().media_acoustics.find_one({'tenant_id': tenant, 'file_id': file_id}, {'_id': 0})


def summary(job):
    sig = (job.get('profile') or {}).get('signature', {}); channel = (job.get('profile') or {}).get('observables', {}).get('channel', {})
    return {'file_id': job['file_id'], 'status': job['status'], 'reads_as': sig.get('reads_as'), 'confidence': sig.get('confidence'),
            'channel_condition': channel.get('channel_condition'), 'profile_version': (job.get('profile') or {}).get('profile_version'),
            'measured_at': job.get('measured_at'), 'error': job.get('error')}


def summaries(tenant):
    fields = {'_id': 0, 'file_id': 1, 'status': 1, 'error': 1, 'measured_at': 1, 'profile.profile_version': 1, 'profile.signature.reads_as': 1,
              'profile.signature.confidence': 1, 'profile.observables.channel.channel_condition': 1}
    return [summary(job) for job in db().media_acoustics.find({'tenant_id': tenant}, fields)]


def request(actor, row):
    """Queue a measurement; replay a current measurement of the same bytes."""
    tenant = actor['tenant_id']; existing = get(tenant, row['file_id'])
    if existing and existing['sha256'] == row['sha256']:
        if existing['status'] in ('queued', 'measuring'): return existing, False
        if existing['status'] == 'measured' and existing['profile'].get('profile_version') == ao.PROFILE_VERSION: return existing, False
    job = {'tenant_id': tenant, 'file_id': row['file_id'], 'title': row['title'], 'sha256': row['sha256'], 'extension': row['extension'],
           'status': 'queued', 'requested_by': actor['principal_id'], 'created_at': lab.now(), 'updated_at': lab.now(), 'attempts': 0,
           'profile': None, 'error': None, 'measured_at': None}
    saved = db().media_acoustics.find_one_and_update({'tenant_id': tenant, 'file_id': row['file_id']}, {'$set': job},
                                                     upsert=True, projection={'_id': 0}, return_document=ReturnDocument.AFTER)
    return saved, True


def claim():
    stamp = lab.now(); token = uuid.uuid4().hex
    return db().media_acoustics.find_one_and_update(
        {'$or': [{'status': 'queued'}, {'status': 'measuring', 'lease_until': {'$lt': stamp}}]},
        {'$set': {'status': 'measuring', 'lease_token': token, 'lease_until': (datetime.now(timezone.utc) + timedelta(minutes=15)).isoformat(), 'updated_at': stamp},
         '$inc': {'attempts': 1}}, sort=[('created_at', 1)], projection={'_id': 0}, return_document=ReturnDocument.AFTER)


def _finish(job, **fields):
    fields['updated_at'] = lab.now()
    db().media_acoustics.update_one({'tenant_id': job['tenant_id'], 'file_id': job['file_id'], 'lease_token': job['lease_token']},
                                    {'$set': fields, '$unset': {'lease_token': '', 'lease_until': ''}})


def measure(job):
    row = store.get(job['tenant_id'], job['file_id'])
    if not row or row['is_deleted'] or row['status'] != 'available' or row['rights_status'] == 'withdrawn':
        return _finish(job, status='failed', error='The file is archived, withdrawn or not fully uploaded')
    if row['sha256'] != job['sha256']:
        return _finish(job, status='failed', error='The stored file changed; request the measurement again')
    try:
        with tempfile.NamedTemporaryFile(suffix=row['extension'], delete=True) as temp:
            response = storage.download(row['storage_path'])
            try:
                for chunk in response.iter_content(1 << 16):
                    if chunk: temp.write(chunk)
            finally: response.close()
            temp.flush()
            profile = ao.measure_file(temp.name)
    except storage.StorageError:
        if job['attempts'] >= 3: return _finish(job, status='failed', error='Storage was unavailable three times; request the measurement again later')
        return _finish(job, status='queued', error='Storage was unavailable; retrying')
    except ao.DecodeError as exc:
        return _finish(job, status='failed', error=str(exc))
    except Exception as exc:
        log.exception('acoustic measurement failed for %s', job['file_id'])
        return _finish(job, status='failed', error=f'Measurement failed: {type(exc).__name__}')
    _finish(job, status='measured', profile=profile, error=None, measured_at=lab.now())
    db().media_events.insert_one({'tenant_id': job['tenant_id'], 'actor': job.get('requested_by'), 'action': 'acoustics_measured', 'file_id': job['file_id'],
                                  'revision': row['revision'], 'at': lab.now(), 'details': {'profile_version': profile['profile_version'], 'reads_as': profile['signature']['reads_as']}})
    try:
        from services.training_lab import baseline
        baseline.advance(job['tenant_id'])
    except Exception:
        log.exception('baseline advance failed after measuring %s', job['file_id'])


def _loop():
    while True:
        try:
            job = claim()
            if job is None:
                time.sleep(float(os.environ.get('MEDIA_ACOUSTICS_POLL_SECONDS', '3'))); continue
            measure(job)
        except Exception:
            log.exception('acoustics worker iteration failed'); time.sleep(5)


def start_worker():
    if _worker_started.is_set(): return
    _worker_started.set()
    threading.Thread(target=_loop, name='media-acoustics-worker', daemon=True).start()


def _dig(profile, path):
    node = profile.get('observables', {})
    for part in path.split('.'):
        if not isinstance(node, dict) or part not in node: return None
        node = node[part]
    return node if isinstance(node, (int, float)) else None


def patterns(tenant):
    """What the measured files say about each general classification, plus agreement with human-reviewed labels."""
    labels = {k: (l, u) for _, k, l, u, _ in ao.REGISTER}
    jobs = list(db().media_acoustics.find({'tenant_id': tenant, 'status': 'measured'}, {'_id': 0, 'profile.signature.timeline': 0, 'profile.observables.energy.energy_contour_1s_dbfs': 0}))
    files = {row['file_id']: row for row in db().media_files.find({'tenant_id': tenant, 'file_id': {'$in': [j['file_id'] for j in jobs]}}, {'_id': 0, 'file_id': 1, 'title': 1, 'event_label': 1, 'label_status': 1})}
    groups = {}
    for job in jobs:
        reads = job['profile']['signature']['reads_as']; group = groups.setdefault(reads, {'reads_as': reads, 'files': [], 'values': {k: [] for k in PATTERN_KEYS}})
        row = files.get(job['file_id'], {})
        group['files'].append({'file_id': job['file_id'], 'title': row.get('title', job['title']), 'confidence': job['profile']['signature']['confidence'],
                               'human_label': row.get('event_label') if row.get('label_status') == 'human_reviewed' else None})
        for key in PATTERN_KEYS:
            value = _dig(job['profile'], key)
            if value is not None: group['values'][key].append(value)
    classes = []
    for reads in CLASSES:
        group = groups.get(reads)
        if not group: continue
        rows = []
        for key in PATTERN_KEYS:
            values = np.array(group['values'][key], dtype=float)
            if not len(values): continue
            leaf = key.split('.')[1]; label, unit = labels.get(leaf, (leaf, ''))
            rows.append({'key': key, 'label': label + (' · spread' if key.endswith('.std') else ''), 'unit': unit, 'n': int(len(values)),
                         'median': round(float(np.median(values)), 3), 'p10': round(float(np.percentile(values, 10)), 3), 'p90': round(float(np.percentile(values, 90)), 3)})
        classes.append({'reads_as': reads, 'file_count': len(group['files']), 'files': group['files'], 'observables': rows})
    reviewed = [(f['human_label'], c['reads_as']) for c in classes for f in c['files'] if f['human_label'] in ('speech', 'music', 'mixed')]
    agreement = {'reviewed_files': len(reviewed), 'agreements': sum(h == r for h, r in reviewed),
                 'disagreements': [{'human_label': h, 'reads_as': r} for h, r in reviewed if h != r]}
    separations = []
    if len(classes) >= 2:
        for key in PATTERN_KEYS:
            medians = {c['reads_as']: next((o['median'] for o in c['observables'] if o['key'] == key), None) for c in classes}
            spreads = [abs(o['p90'] - o['p10']) for c in classes for o in c['observables'] if o['key'] == key]
            present = [v for v in medians.values() if v is not None]
            if len(present) >= 2 and spreads:
                score = (max(present) - min(present)) / (float(np.mean(spreads)) + 1e-9)
                leaf = key.split('.')[1]
                separations.append({'key': key, 'label': labels.get(leaf, (leaf, ''))[0], 'separation': round(float(score), 2), 'medians': medians})
        separations.sort(key=lambda s: -s['separation'])
    return {'measured_files': len(jobs), 'classes': classes, 'human_review': agreement, 'most_separating': separations[:8],
            'method': 'per-class medians and 10th–90th percentile ranges of measured observables; separation = median spread ÷ mean within-class range'}
