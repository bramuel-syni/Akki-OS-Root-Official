"""Measure every already-authorized staged audio file on the host. Exports aggregates and compact feature rows;
never raw media, transcripts or file paths (the ref→path map stays on the host volume)."""
import hashlib
import json
import multiprocessing
import os
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

AUDIO = {'.wav', '.flac', '.mp3', '.ogg', '.m4a'}


def _one(args):
    path, max_seconds = args
    from services.audio_plane_v1 import acoustic_observables as ao
    try:
        return ao.compact(ao.measure_file(path, max_seconds=max_seconds)), None
    except Exception as exc:
        return None, type(exc).__name__


def _files(corpus, per_language_cap):
    files = []
    for language in sorted(corpus.iterdir()):
        if not language.is_dir() or language.is_symlink():
            continue
        count = 0
        for audio in sorted(language.glob('*/audio/*')):
            if audio.suffix.lower() not in AUDIO or audio.is_symlink() or not audio.resolve().is_relative_to(corpus):
                continue
            files.append((language.name, audio)); count += 1
            if per_language_cap and count >= per_language_cap:
                break
    return files


def measure_corpus(control, state):
    from services.audio_plane_v1 import acoustic_observables as ao
    root = Path(control['lab_corpus_root']).resolve(); corpus = root / 'corpus' / 'datasets'
    if not corpus.is_dir():
        raise ValueError('AUTHORIZED_STAGED_CORPUS_NOT_FOUND')
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
        os.environ[key] = '1'  # one BLAS thread per worker process; the pool supplies the parallelism
    files = _files(corpus, int(control.get('max_files_per_language') or 0))
    started = time.time(); rows = []; mapping = {}; failures = Counter()
    state.update(progress={'stage': 'measuring staged audio', 'files': 0, 'of': len(files)})
    with ProcessPoolExecutor(max_workers=int(control['workers']), mp_context=multiprocessing.get_context('fork')) as pool:
        results = pool.map(_one, [(str(audio), float(control['max_seconds'])) for _, audio in files], chunksize=2)
        for (language, audio), (record, error) in zip(files, results):
            ref = hashlib.sha256(str(audio.relative_to(corpus)).encode()).hexdigest()[:16]
            mapping[ref] = str(audio.relative_to(corpus))
            rows.append({'ref': ref, 'language': language, **(record or {'error': error})})
            if error: failures[error] += 1
            if len(rows) % 50 == 0:
                state.update(progress={'stage': 'measuring staged audio', 'files': len(rows), 'of': len(files), 'elapsed_s': int(time.time() - started)})
    job_dir = Path(control['job_dir'])
    compact_text = json.dumps(rows, separators=(',', ':'), sort_keys=True)
    (job_dir / 'results_compact.json').write_text(compact_text)
    (job_dir / 'results_map.json').write_text(json.dumps(mapping, indent=0, sort_keys=True))
    per_language = {}
    for language in sorted({r['language'] for r in rows}):
        group = [r for r in rows if r['language'] == language]; measured = [r for r in group if 'reads_as' in r]
        per_language[language] = {
            'files': len(group), 'measured': len(measured), 'decode_failures': len(group) - len(measured),
            'hours': round(sum(r['duration_s'] for r in measured) / 3600, 4),
            'reads_as': dict(Counter(r['reads_as'] for r in measured)),
            'windows': sum(r['windows'] for r in measured), 'music_windows': sum(r['music_windows'] for r in measured),
            'files_with_music_windows': sum(r['music_windows'] >= 2 for r in measured),
            'channel_condition': dict(Counter(r['channel_condition'] for r in measured)),
            'artefacts': dict(Counter(a for r in measured for a in r['artefacts']))}
    state.update(progress={'stage': 'measurement complete', 'files': len(rows), 'of': len(files), 'elapsed_s': int(time.time() - started)})
    return {'scope': 'authorized staged language-cognition corpus only; not the whole RMS estate', 'evidence_class': 'measured_observables_cue_readings',
            'profile_version': ao.PROFILE_VERSION, 'files': len(rows), 'measured': len(rows) - sum(failures.values()), 'decode_failures': dict(failures),
            'per_language': per_language, 'compact_rows_sha256': hashlib.sha256(compact_text.encode()).hexdigest(), 'compact_rows_bytes': len(compact_text),
            'compute_seconds': round(time.time() - started, 1), 'workers': int(control['workers']), 'max_seconds_per_file': float(control['max_seconds']),
            'music_labels': {'status': 'not_established', 'reason': 'Readings are cue scoring over measured observables, not human labels.'},
            'training_started': False, 'raw_media_exported': False, 'paths_exported': False}
