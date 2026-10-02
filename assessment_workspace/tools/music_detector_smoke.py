"""Engineering smoke of the music detector worker on akki-vm GPU 1: ship the labelled library recordings (digest-verified), dispatch a
smoke run (3 steps, one fold), poll to the terminal receipt. Not an acceptance run; no sign-off is recorded by this script."""
import json
import os
import sys
import time

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import load_dotenv
load_dotenv('/app/backend/.env')

from services.census_autonomy.operational_runner import admission_path  # noqa: E402
from services.training_lab import corpus_measurement, music_shipping  # noqa: E402
from services.training_runner import m9_dispatch  # noqa: E402

items, pending = music_shipping.labelled_items('RMS')
print('labelled', len(items), 'pending', len(pending), 'bytes', sum(i['size_bytes'] for i in items))
t = time.time()
shipped = music_shipping.ship('akki-vm', items, progress=lambda d, o: print('  shipped', d, 'of', o, flush=True))
print('ship', shipped, round(time.time() - t), 's')
measurement = corpus_measurement.latest('RMS')
params = {'seed': 41, 'epochs': 1, 'folds': 2, 'batch_size': 128, 'lr': 0.001, 'max_seconds_per_file': 60.0, 'max_windows_per_file': 30,
          'weak_negatives_per_language': 3, 'weak_positive_files': 3, 'gpu_index': 1,
          'lab_corpus_root': os.environ['LANGUAGE_COGNITION_REMOTE_ROOT'], 'refs_dir': music_shipping.refs_dir(),
          'measurement_job_dir': f"{os.environ['M9_REMOTE_ROOT']}/jobs/{measurement['job_id']}",
          'labelled_manifest': [{k: m[k] for k in ('item_id', 'title', 'label', 'label_source', 'file', 'sha256')} for m in items],
          'baseline': {'accuracy': 0.5, 'recall': 0.5, 'precision': 0.5}, 'smoke': True,
          'owner_order_ref': 'engineering smoke 2026-10-02: music detector worker path on akki-vm GPU 1; not an acceptance run, no sign-off'}
lawful, _ = admission_path()
job = m9_dispatch.submit('lab_train_music', params, 'akki-vm', 'akki-engineering', str(lawful), timeout=120)
print('dispatch', job['job_id'], job['status'], job.get('reason'))
while job['status'] in ('running', 'submitting'):
    time.sleep(20)
    job = m9_dispatch.refresh(job['job_id'])
    print('  ', job['status'], json.dumps((job.get('remote_state') or {}).get('progress'))[:200], flush=True)
print('final', job['status'], job.get('reason'))
result = (job.get('receipt') or {}).get('result') or {}
print(json.dumps({k: result.get(k) for k in ('items', 'positives', 'negatives', 'folds', 'file_level', 'weak_supervision', 'training', 'artefact', 'label_sources')}, indent=1, default=str)[:3000])
if job['status'] != 'completed':
    print((job.get('receipt') or {}).get('error'))
    print(job.get('worker_log_tail'))
