"""Public-domain reference recordings (archive.org) imported into the library as reference audio, never training data."""
import hashlib
import json
import logging
import tempfile
import threading
import urllib.parse
import urllib.request
from functools import lru_cache

from services.media_library import acoustics, formats, storage, store
from services.training_lab import store as lab

log = logging.getLogger('media.reference')
USER_AGENT = 'Akki/1.0 (public-domain reference import)'
MIN_BYTES, MAX_BYTES = 900_000, 12_000_000
CATALOGUE = [
    {'identifier': 'heartofamystery_2005_librivox', 'label': 'speech', 'language': 'English', 'take': 2, 'source_title': 'LibriVox · The Heart of a Mystery'},
    {'identifier': 'williamagain_1902_librivox', 'label': 'speech', 'language': 'English', 'take': 2, 'source_title': 'LibriVox · William Again'},
    {'identifier': 'famouspoems_2207_librivox', 'label': 'speech', 'language': 'English', 'take': 1, 'source_title': 'LibriVox · Famous Poems'},
    {'identifier': 'totheruralmuseandotherpoems_2505_librivox', 'label': 'speech', 'language': 'English', 'take': 1, 'source_title': 'LibriVox · To the Rural Muse'},
    {'identifier': 'les_anciens_canadiens_2203_librivox', 'label': 'speech', 'language': 'French', 'take': 1, 'source_title': 'LibriVox · Les anciens Canadiens'},
    {'identifier': 'guerraylapaz1_2412_librivox', 'label': 'speech', 'language': 'Spanish', 'take': 1, 'source_title': 'LibriVox · La guerra y la paz'},
    {'identifier': 'tschun_1504_librivox', 'label': 'speech', 'language': 'German', 'take': 1, 'source_title': 'LibriVox · Tschun'},
    {'identifier': 'musopen-chopin', 'label': 'music', 'language': '', 'take': 6, 'source_title': 'Musopen · Chopin (solo piano)'},
]
_lock = threading.Lock()


@lru_cache(maxsize=1)
def db():
    database = store.db()
    database.media_reference_imports.create_index([('tenant_id', 1), ('started_at', -1)])
    return database


def _fetch(url, timeout=60):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': USER_AGENT}), timeout=timeout)


def plan(item):
    meta = json.load(_fetch(f"https://archive.org/metadata/{item['identifier']}", 30))
    files = [f for f in meta.get('files', []) if f['name'].lower().endswith(('.mp3', '.ogg', '.flac')) and MIN_BYTES <= int(f.get('size', 0)) <= MAX_BYTES]
    files.sort(key=lambda f: (int(f['size']), f['name']))
    chosen, seen = [], set()
    for f in files:
        stem = f['name'].rsplit('.', 1)[0]
        if stem in seen: continue
        seen.add(stem); chosen.append(f)
        if len(chosen) >= item['take']: break
    return [{'identifier': item['identifier'], 'name': f['name'], 'size_bytes': int(f['size']), 'label': item['label'], 'language': item['language'],
             'title': f"{item['source_title']} · {f['name'].rsplit('.', 1)[0][:60]}", 'url': f"https://archive.org/download/{item['identifier']}/{urllib.parse.quote(f['name'])}",
             'licence': meta.get('metadata', {}).get('licenseurl') or 'public domain (archive.org item metadata)'} for f in chosen]


def _import_one(actor, entry):
    key = f"reference:{entry['identifier']}:{entry['name']}"
    existing = db().media_files.find_one({'tenant_id': actor['tenant_id'], 'upload_key': key}, {'_id': 0})
    if existing and existing['status'] == 'available':
        return existing['file_id'], 'already_imported'
    extension = '.' + entry['name'].rsplit('.', 1)[1].lower()
    with tempfile.SpooledTemporaryFile(max_size=1 << 20, mode='w+b') as temp:
        digest = hashlib.sha256(); count = 0
        with _fetch(entry['url'], 120) as response:
            while True:
                chunk = response.read(1 << 16)
                if not chunk: break
                digest.update(chunk); temp.write(chunk); count += len(chunk)
        temp.seek(0); validation = formats.validate(temp, extension)
        body = {'filename': entry['name'], 'size_bytes': count, 'sha256': digest.hexdigest(), 'storage_permission_confirmed': True}
        info = {**formats.describe(entry['name'], count), 'title': entry['title'][:140]}
        row = existing
        if not row:
            row, _ = store.create(actor, key, body, info, hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest())
        temp.seek(0); result = storage.put(row['storage_path'], temp, info['content_type'])
        if int(result['size']) != count: raise ValueError('Storage did not confirm the expected file size')
    fields = {'status': 'available', 'storage_path': result['path'], 'format_validation': validation, 'stored_at': lab.now(), 'updated_at': lab.now(),
              'reference': True, 'label_source': 'source_catalogue', 'source': {'provider': 'archive.org', 'identifier': entry['identifier'], 'file': entry['name']},
              'language': entry['language'], 'event_label': entry['label'], 'label_status': 'unreviewed', 'rights_status': 'declared', 'rights_basis': 'public_domain',
              'rights_reference': entry['url'], 'training_permission_confirmed': False, 'rights_independently_verified': False}
    store.db().media_files.update_one({'file_id': row['file_id']}, {'$set': fields})
    store.audit(actor, 'reference_imported', row['file_id'], row['revision'], {'identifier': entry['identifier'], 'label': entry['label'], 'bytes': count})
    acoustics.request(actor, store.get(actor['tenant_id'], row['file_id']))
    return row['file_id'], 'imported'


def _run(actor, import_id):
    collection = db().media_reference_imports
    for item in CATALOGUE:
        try:
            entries = plan(item)
        except Exception as exc:
            collection.update_one({'import_id': import_id}, {'$push': {'items': {'identifier': item['identifier'], 'status': 'unavailable', 'reason': type(exc).__name__}}, '$set': {'updated_at': lab.now()}})
            continue
        for entry in entries:
            try:
                file_id, outcome = _import_one(actor, entry)
                record = {'identifier': entry['identifier'], 'name': entry['name'], 'title': entry['title'], 'label': entry['label'], 'status': outcome, 'file_id': file_id, 'bytes': entry['size_bytes']}
            except Exception as exc:
                log.warning('reference import failed for %s: %s', entry['name'], type(exc).__name__)
                record = {'identifier': entry['identifier'], 'name': entry['name'], 'title': entry['title'], 'label': entry['label'], 'status': 'failed', 'reason': str(exc)[:160]}
            collection.update_one({'import_id': import_id}, {'$push': {'items': record}, '$set': {'updated_at': lab.now()}})
    collection.update_one({'import_id': import_id}, {'$set': {'status': 'complete', 'finished_at': lab.now(), 'updated_at': lab.now()}})
    acoustics.start_worker()


def start(actor):
    with _lock:
        running = db().media_reference_imports.find_one({'tenant_id': actor['tenant_id'], 'status': 'running'}, {'_id': 0})
        if running:
            return running, False
        doc = {'import_id': 'ri-' + hashlib.sha256(lab.now().encode()).hexdigest()[:12], 'tenant_id': actor['tenant_id'], 'status': 'running', 'items': [],
               'catalogue_items': len(CATALOGUE), 'started_at': lab.now(), 'updated_at': lab.now(), 'policy': 'Public-domain reference audio; rights basis public_domain; never counted as training data'}
        db().media_reference_imports.insert_one(dict(doc))
    threading.Thread(target=_run, args=(actor, doc['import_id']), name='media-reference-import', daemon=True).start()
    return doc, True


def latest(tenant):
    return db().media_reference_imports.find_one({'tenant_id': tenant}, {'_id': 0}, sort=[('started_at', -1)])
