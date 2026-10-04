"""Native-reviewer confirmation panel (MA-12/MA-31 evidence): independent double annotation of brand mentions on the sealed admission panel,
adjudication of disagreements, and the verified reference the sealed evaluation measures against. Reviewers hear the segment (bounded playback
from the estate host, never exported in bulk) and never see the transcript or the transcript-derived labels. No rating is ever fabricated."""
import base64
import hashlib
import io
import os
import wave

from services.training_lab import store as lab
from services.training_lab.malpha_evaluation import fingerprint

LANGUAGES = ('kik', 'kam', 'swa')
PUBLIC_TASK_FIELDS = ('task_id', 'panel_id', 'language', 'seg_id', 'session', 'duration_s', 'status', 'annotations_count', 'final_brands', 'created_at')


def db():
    d = lab.db()
    d.malpha_review_tasks.create_index('task_id', unique=True)
    d.malpha_review_tasks.create_index([('panel_id', 1), ('language', 1), ('status', 1)])
    d.malpha_review_panels.create_index('panel_id', unique=True)
    return d


def open_panel(result, host):
    """Settlement hook of the v2 reseal: one panel per seal set; idempotent."""
    seals = result['seals']; panel_id = fingerprint([seals[l]['admission_seg_ids_sha256'] for l in LANGUAGES])
    created = 0
    for lang, items in (result.get('confirmation_panel') or {}).items():
        for it in items:
            task_id = hashlib.sha256(f"{panel_id}:{it['seg_id']}".encode()).hexdigest()[:16]
            doc = {'task_id': task_id, 'panel_id': panel_id, 'language': lang, 'seg_id': it['seg_id'], 'session': it['session'], 'start': it['start'], 'end': it['end'], 'duration_s': it['duration_s'],
                   'pcm_offset': it['pcm_offset'], 'pcm_bytes': it['pcm_bytes'], 'host': host, 'aip_db_dir': result['aip_db_dir'], 'stratum': it['stratum'], 'transcript_mentions': it['transcript_mentions'],
                   'annotations': [], 'annotations_count': 0, 'status': 'open', 'final_brands': None, 'created_at': lab.now()}
            if db().malpha_review_tasks.update_one({'task_id': task_id}, {'$setOnInsert': doc}, upsert=True).upserted_id is not None: created += 1
    version = int(result.get('split_version') or 1)
    # only panels of an OLDER seal version are superseded; a panel for the same or a newer seal set is never demoted by a later open_panel call
    db().malpha_review_panels.update_many({'panel_id': {'$ne': panel_id}, 'status': {'$ne': 'superseded'}, 'split_version': {'$lt': version}}, {'$set': {'status': 'superseded', 'superseded_at': lab.now(), 'superseded_by': panel_id}})
    db().malpha_review_panels.update_one({'panel_id': panel_id}, {'$setOnInsert': {'panel_id': panel_id, 'seals': seals, 'split_version': version, 'host': host, 'opened_at': lab.now(), 'status': 'annotating', 'verified': False,
                                                                                    'protocol': {'annotators_per_task': 2, 'independent': True, 'adjudication': 'third identity on disagreement', 'transcript_hidden': True}}}, upsert=True)
    return refresh_panel(panel_id) | {'tasks_created': created}


def live_panel_id():
    """The panel that belongs to the commission's current seal set — derived from the sealed admission ids, never from a mutable status flag."""
    c = db().malpha_commissions.find_one({'commission_id': 'LISTEN-KIK-KAM-SWA'}, {'_id': 0, 'aip_seals': 1, 'reference_panel_id': 1})
    seals = (c or {}).get('aip_seals') or {}
    if all(isinstance((seals.get(l) or {}).get('admission_seg_ids_sha256'), str) for l in LANGUAGES): return fingerprint([seals[l]['admission_seg_ids_sha256'] for l in LANGUAGES])
    return (c or {}).get('reference_panel_id')


def current_panel():
    live = live_panel_id()
    p = db().malpha_review_panels.find_one({'panel_id': live}, {'_id': 0}) if live else None
    if p:
        if p.get('status') == 'superseded':  # a stray supersession of the commission's own panel is corrected on read, never silently served
            db().malpha_review_panels.update_one({'panel_id': live}, {'$set': {'status': 'verified' if p.get('verified') else 'annotating', 'reinstated_at': lab.now(), 'reinstated_reason': 'panel matches the current admission seal set'}, '$unset': {'superseded_at': '', 'superseded_by': ''}})
            p = db().malpha_review_panels.find_one({'panel_id': live}, {'_id': 0})
        return p
    return db().malpha_review_panels.find_one({'status': {'$ne': 'superseded'}}, {'_id': 0}, sort=[('opened_at', -1)]) or db().malpha_review_panels.find_one({}, {'_id': 0}, sort=[('opened_at', -1)])


def panel(panel_id):
    return db().malpha_review_panels.find_one({'panel_id': panel_id}, {'_id': 0})


def _public(t):
    return {k: t.get(k) for k in PUBLIC_TASK_FIELDS}


def tasks(panel_id, language=None, status=None, limit=200):
    q = {'panel_id': panel_id}
    if language: q['language'] = language
    if status: q['status'] = status
    return [_public(t) for t in db().malpha_review_tasks.find(q, {'_id': 0}, sort=[('language', 1), ('seg_id', 1)], limit=limit)]


def next_task(panel_id, annotator_id, language=None):
    """The next segment this reviewer has not heard: open tasks first, never one they already annotated, never the transcript."""
    q = {'panel_id': panel_id, 'status': {'$in': ['open', 'partial']}, 'annotations.annotator_id': {'$ne': annotator_id}}
    if language: q['language'] = language
    t = db().malpha_review_tasks.find_one(q, {'_id': 0}, sort=[('annotations_count', -1), ('seg_id', 1)])
    return _public(t) if t else None


def annotate(task_id, annotator_id, brands, no_mention=False, unsure=False, lexicon_brands=None):
    t = db().malpha_review_tasks.find_one({'task_id': task_id}, {'_id': 0})
    if not t: raise LookupError('NO_SUCH_TASK')
    if t['status'] in ('agreed', 'adjudicated'): raise ValueError('TASK_ALREADY_FINAL')
    if any(a['annotator_id'] == annotator_id for a in t['annotations']): raise ValueError('ANNOTATOR_ALREADY_RATED_THIS_SEGMENT')
    brands = sorted({str(b).strip() for b in (brands or []) if str(b).strip()})
    if no_mention and brands: raise ValueError('NO_MENTION_CONFLICTS_WITH_BRANDS')
    if not no_mention and not brands and not unsure: raise ValueError('EMPTY_ANNOTATION')
    if lexicon_brands is not None and not set(brands) <= set(lexicon_brands): raise ValueError('UNKNOWN_BRAND:' + ','.join(sorted(set(brands) - set(lexicon_brands))))
    ann = {'annotator_id': annotator_id, 'brands': brands, 'no_mention': bool(no_mention), 'unsure': bool(unsure), 'at': lab.now()}
    anns = t['annotations'] + [ann]
    status, final = 'partial', None
    if len(anns) >= 2:
        decided = [a for a in anns if not a['unsure']]
        if len(decided) >= 2 and len({tuple(a['brands']) for a in decided[:2]}) == 1: status, final = 'agreed', decided[0]['brands']
        else: status = 'disagreement'
    db().malpha_review_tasks.update_one({'task_id': task_id}, {'$set': {'annotations': anns, 'annotations_count': len(anns), 'status': status, 'final_brands': final, 'updated_at': lab.now()}})
    refresh_panel(t['panel_id'])
    return _public(db().malpha_review_tasks.find_one({'task_id': task_id}, {'_id': 0}))


def adjudicate(task_id, adjudicator_id, brands, lexicon_brands=None):
    t = db().malpha_review_tasks.find_one({'task_id': task_id}, {'_id': 0})
    if not t: raise LookupError('NO_SUCH_TASK')
    if t['status'] != 'disagreement': raise ValueError('ADJUDICATION_ONLY_ON_DISAGREEMENT')
    if any(a['annotator_id'] == adjudicator_id for a in t['annotations']): raise ValueError('ADJUDICATOR_MUST_BE_INDEPENDENT')
    brands = sorted({str(b).strip() for b in (brands or []) if str(b).strip()})
    if lexicon_brands is not None and not set(brands) <= set(lexicon_brands): raise ValueError('UNKNOWN_BRAND')
    db().malpha_review_tasks.update_one({'task_id': task_id}, {'$set': {'adjudication': {'adjudicator_id': adjudicator_id, 'brands': brands, 'at': lab.now()}, 'status': 'adjudicated', 'final_brands': brands, 'updated_at': lab.now()}})
    refresh_panel(t['panel_id'])
    return _public(db().malpha_review_tasks.find_one({'task_id': task_id}, {'_id': 0}))


def refresh_panel(panel_id):
    rows = list(db().malpha_review_tasks.find({'panel_id': panel_id}, {'_id': 0, 'language': 1, 'status': 1, 'final_brands': 1, 'annotations': 1, 'transcript_mentions': 1}))
    per = {}
    for lang in LANGUAGES:
        ts = [t for t in rows if t['language'] == lang]; final = [t for t in ts if t['status'] in ('agreed', 'adjudicated')]
        annotators = {a['annotator_id'] for t in ts for a in t['annotations']}
        two = [t for t in ts if len(t['annotations']) >= 2]
        per[lang] = {'tasks': len(ts), 'open': sum(t['status'] == 'open' for t in ts), 'partial': sum(t['status'] == 'partial' for t in ts), 'disagreement': sum(t['status'] == 'disagreement' for t in ts),
                     'agreed': sum(t['status'] == 'agreed' for t in ts), 'adjudicated': sum(t['status'] == 'adjudicated' for t in ts), 'distinct_annotators': len(annotators),
                     'agreement_rate': round(sum(t['status'] == 'agreed' for t in two) / len(two), 4) if two else None,
                     'final_positive_segments': sum(bool(t['final_brands']) for t in final), 'final_negative_segments': sum(t['final_brands'] == [] for t in final),
                     'transcript_label_agreement': round(sum(sorted(t['final_brands'] or []) == sorted(t['transcript_mentions'] or []) for t in final) / len(final), 4) if final else None,
                     'complete': bool(ts) and len(final) == len(ts) and len(annotators) >= 2}
    verified = all(v['complete'] for v in per.values())
    status = 'verified' if verified else 'annotating' if rows else 'empty'
    update = {'per_language': per, 'status': status, 'verified': verified, 'updated_at': lab.now()}
    if verified: update['verified_at'] = lab.now()
    db().malpha_review_panels.update_one({'panel_id': panel_id}, {'$set': update})
    return panel(panel_id) or {'panel_id': panel_id, **update}


def reference_labels(panel_id):
    """{seg_id: [brands]} for every final task — the only reference a confirmation read may use. Empty when the panel is not verified."""
    p = panel(panel_id)
    if not p or not p.get('verified'): return {}
    return {t['seg_id']: list(t['final_brands'] or []) for t in db().malpha_review_tasks.find({'panel_id': panel_id, 'status': {'$in': ['agreed', 'adjudicated']}}, {'_id': 0, 'seg_id': 1, 'final_brands': 1})}


def audio_wav(task_id):
    """Bounded playback of one admission segment: the exact PCM window is read on the estate host and returned as a 16 kHz mono WAV. Receipted crossing."""
    from services.training_runner.ssh_seam import execute_remote_command
    t = db().malpha_review_tasks.find_one({'task_id': task_id}, {'_id': 0})
    if not t: raise LookupError('NO_SUCH_TASK')
    if not 0 < int(t['pcm_bytes']) <= 16000 * 2 * 40: raise ValueError('SEGMENT_WINDOW_OUT_OF_BOUNDS')
    path = f"{t['aip_db_dir']}/pcm16k_{t['language']}.bin"
    if not path.startswith(os.environ['LANGUAGE_COGNITION_REMOTE_ROOT']): raise ValueError('PATH_OUTSIDE_ESTATE_ROOT')
    res = execute_remote_command(t['host'], f"tail -c +{int(t['pcm_offset']) + 1} '{path}' | head -c {int(t['pcm_bytes'])} | base64 -w0", purpose='malpha_review_playback', timeout=60)
    if res.rc != 0: raise RuntimeError('PLAYBACK_READ_FAILED')
    pcm = base64.b64decode(res.stdout_redacted.strip())
    if len(pcm) != int(t['pcm_bytes']): raise RuntimeError('PLAYBACK_LENGTH_MISMATCH')
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000); w.writeframes(pcm)
    db().malpha_review_tasks.update_one({'task_id': task_id}, {'$inc': {'playbacks': 1}})
    return buf.getvalue()
