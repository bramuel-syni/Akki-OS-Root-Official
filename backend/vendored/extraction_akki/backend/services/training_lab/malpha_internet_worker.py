"""Versioned, resumable public speech intake on estate hosts only.

No dataset-hour ceiling under the owner order. Existing rows stay immutable;
new rows commit after PCM and text are durable. Held-out text hashes are used
only to reject exact overlap, never as learning targets. Near-duplicate and
speaker overlap with external sources remain separate qualification work.
"""
import fcntl
import hashlib
import json
import os
import shutil
import tarfile
import time
from collections import Counter
from pathlib import Path


def atomic_json(path, value):
    tmp = path.with_suffix(path.suffix + '.tmp')
    with open(tmp, 'w') as fh:
        json.dump(value, fh, sort_keys=True); fh.flush(); os.fsync(fh.fileno())
    os.replace(tmp, path)


def source_rows(spec, revision):
    """Explicit manifest-tar join; generic HF auto-loader cannot join this layout."""
    from huggingface_hub import hf_hub_download
    if spec.get('format') == 'manifest_tar':
        manifest = hf_hub_download(spec['repo'], 'manifest.jsonl', repo_type='dataset', revision=revision)
        shards = {}
        with open(manifest) as fh:
            for line in fh:
                row = json.loads(line)
                if row.get('split') != 'train': continue
                shard = str(row['shard'])
                if Path(shard).name != shard or not shard.endswith('.tar'): raise ValueError('Unsafe shard name')
                shards.setdefault(shard, {})[str(row['key']) + '.flac'] = row
        for shard, entries in sorted(shards.items()):
            path = hf_hub_download(spec['repo'], 'shards/' + shard, repo_type='dataset', revision=revision)
            with tarfile.open(path) as archive:
                for member in archive:
                    if not member.isfile() or member.name not in entries: continue
                    if member.size > 64 * 1024 * 1024: raise ValueError('Unexpected audio member size')
                    row = entries[member.name]
                    with archive.extractfile(member) as fh:
                        yield {'text': row['text'], 'blob': fh.read(), 'speaker': row.get('speaker_id'), 'source_key': row['key']}
        return
    from datasets import Audio, load_dataset
    from itertools import chain
    ds = load_dataset(spec['repo'], spec.get('config'), split=spec.get('split', 'train'), streaming=True, revision=revision)
    features = ds.features or {}
    audio_col = spec.get('audio_column') or next((k for k, v in features.items() if isinstance(v, Audio)), 'audio')
    ds = ds.cast_column(audio_col, Audio(decode=False))
    iterator = iter(ds); first = next(iterator, None)
    if first is None: return
    from services.training_lab.malpha_worker import TEXT_COLUMNS
    text_col = spec.get('text_column') or next((k for k in TEXT_COLUMNS if k in first), None)
    if text_col is None: raise ValueError('Transcript column absent')
    for item in chain([first], iterator):
        yield {'text': item.get(text_col), 'blob': (item.get(audio_col) or {}).get('bytes'),
               'speaker': item.get(spec.get('speaker_column') or 'speaker_name') or item.get('speaker_id')}


def ingest(control, state):
    import numpy as np
    from services.training_lab.malpha_worker import (LICENCE_ALLOWLIST, SR16, _decode_bytes, _hf_qualify,
        _sha, _write_rows_atomic, brand_inventory, load_rows, now, spectrum_features)
    root = Path(control['aip_db_dir']); started = time.time(); results = []
    # One writer per corpus. GPU jobs already loaded their rows and keep running.
    with open(root / 'internet_intake.lock', 'a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for spec in control['datasets']:
            key = f"{spec['repo']}:{spec.get('config') or 'default'}"; lang = spec['language']
            journal_path = root / ('intake-' + _sha(key)[:16] + '.json')
            journal = json.loads(journal_path.read_text()) if journal_path.exists() else {}
            state.update(progress={'stage': 'qualifying public corpus', 'language': lang, 'elapsed_s': int(time.time() - started)})
            info, refusal = _hf_qualify(spec['repo'], LICENCE_ALLOWLIST)
            rec = {'repo': spec['repo'], 'config': spec.get('config'), 'language': lang, 'split': 'train',
                   'licence': (info.card_data or {}).get('license') if info and info.card_data else None,
                   'checked_at': now(), 'intake_version': 2, 'exhausted': False}
            if refusal:
                rec.update(status='refused', reason=refusal); results.append(rec); continue
            revision = journal.get('revision') or info.sha
            rec['revision'] = revision
            existing = load_rows(root, lang, with_text=True, dataset='internet')
            by_id = {r['seg_id']: r for r in existing}
            if journal.get('exhausted'):
                results.append({**journal['result'], 'reused': True}); continue
            held_hashes = {r.get('text_sha256') for r in load_rows(root, lang) if r['split'] in ('dev', 'admission')}
            content_hashes = {r.get('pcm_sha256') for r in existing if r.get('pcm_sha256')}
            pcm_name = f'pcm16k_internet_{lang}.bin'; pcm_path = root / pcm_name
            skipped = Counter(journal.get('skipped') or {}); cursor = int(journal.get('cursor', -1)); processed = cursor
            n_new = 0; hours_new = 0.0; new_rows = []; ended = 'source_exhausted'

            def commit(pcm, exhausted=False):
                nonlocal existing, new_rows
                pcm.flush(); os.fsync(pcm.fileno())
                if new_rows:
                    brand_inventory({lang: new_rows}, control['brand_lexicon'])
                    with open(root / f'text_internet_{lang}.jsonl', 'a') as th:
                        for row in new_rows: th.write(json.dumps({'seg_id': row['seg_id'], 'text': row['text']}, ensure_ascii=False) + '\n')
                        th.flush(); os.fsync(th.fileno())
                    existing.extend(new_rows); new_rows = []
                    _write_rows_atomic(root / f'segments_internet_{lang}.jsonl', existing, key=lambda r: r['seg_id'])
                dataset_rows = [r for r in existing if r.get('file') == key]
                rec.update(status='ingested' if exhausted else 'partial', rows=len(dataset_rows),
                           hours=round(sum(r['features']['duration_s'] for r in dataset_rows) / 3600, 3),
                           rows_added_this_run=n_new, hours_added_this_run=round(hours_new, 3),
                           skipped=dict(skipped), exhausted=exhausted, stop_reason=ended)
                atomic_json(journal_path, {'revision': revision, 'cursor': processed, 'exhausted': exhausted,
                                          'skipped': dict(skipped), 'result': rec})
                state.update(progress={'stage': 'expanding qualified public corpus', 'language': lang,
                    'rows': len(dataset_rows), 'rows_added': n_new, 'hours': rec['hours'], 'of_hours': None,
                    'elapsed_s': int(time.time() - started), 'source_revision': revision})

            with open(pcm_path, 'ab') as pcm:
                try:
                    for index, item in enumerate(source_rows(spec, revision)):
                        if index <= cursor: continue
                        disk = shutil.disk_usage(root)
                        if disk.free < max(5 * 1024 ** 3, disk.total * 0.01):
                            ended = 'disk_backpressure'; break
                        cap = control['max_hours_per_dataset']
                        if cap is not None and hours_new >= cap:
                            ended = 'explicit_recipe_volume'; break
                        text = ' '.join(str(item.get('text') or '').split()); blob = item.get('blob')
                        sid = _sha(f'{key}:{index}')[:16]
                        if sid in by_id:
                            if text and by_id[sid]['text_sha256'] != _sha(text): raise ValueError('Legacy source order changed; cannot append safely')
                            skipped['already_committed'] += 1; processed = index; continue
                        if not text or not blob:
                            skipped['no_text_or_audio'] += 1; processed = index; continue
                        if _sha(text) in held_hashes:
                            skipped['heldout_text_overlap'] += 1; processed = index; continue
                        try: y = _decode_bytes(blob, SR16)
                        except Exception:
                            skipped['decode_error'] += 1; processed = index; continue
                        if not (0.5 * SR16 <= len(y) <= 30 * SR16) or float(np.abs(y).max()) < 1e-4:
                            skipped['duration_or_silence'] += 1; processed = index; continue
                        block = (np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes(); pcm_sha = hashlib.sha256(block).hexdigest()
                        if pcm_sha in content_hashes:
                            skipped['duplicate_pcm'] += 1; processed = index; continue
                        feats = spectrum_features(y, SR16, len(text))
                        if not feats:
                            skipped['no_features'] += 1; processed = index; continue
                        offset = pcm.tell(); pcm.write(block)
                        speaker = _sha(str(item.get('speaker') or 'unknown'))[:20]
                        row = {'seg_id': sid, 'ref': _sha(key)[:16], 'session': f'internet:{key}:{speaker}', 'file': key,
                               'start': 0.0, 'end': feats['duration_s'], 'speaker': speaker, 'split': 'train', 'dataset': 'internet',
                               'source': {'repo': spec['repo'], 'config': spec.get('config'), 'revision': revision, 'licence': rec['licence'], 'row_index': index},
                               'condition': 'public_speech/16000Hz/1ch', 'pcm_file': pcm_name, 'pcm_offset': offset, 'pcm_bytes': len(block),
                               'pcm_sha256': pcm_sha, 'chars': len(text), 'words': len(text.split()), 'text_sha256': _sha(text), 'features': feats, 'text': text}
                        new_rows.append(row); by_id[sid] = row; content_hashes.add(pcm_sha)
                        n_new += 1; hours_new += feats['duration_s'] / 3600; processed = index
                        if n_new % 200 == 0: commit(pcm)
                    commit(pcm, exhausted=ended == 'source_exhausted')
                except Exception as exc:
                    ended = 'source_error:' + type(exc).__name__; commit(pcm)
                    rec['reason'] = ended
            results.append(dict(rec))
        # Merge with the CURRENT manifest to avoid overwriting a concurrent brand revision.
        with open(root / 'manifest.lock', 'a') as manifest_lock:
            fcntl.flock(manifest_lock, fcntl.LOCK_EX)
            manifest = json.loads((root / 'manifest.json').read_text())
            for rec in results: manifest.setdefault('internet_corpus', {})[f"{rec['repo']}:{rec.get('config') or 'default'}"] = rec
            atomic_json(root / 'manifest.json', manifest)
    totals = {l: {'rows': sum(r.get('rows', 0) for r in results if r['language'] == l),
                  'hours': round(sum(r.get('hours', 0) for r in results if r['language'] == l), 3)} for l in control['languages']}
    return {'commission_id': control['commission_id'], 'datasets': results, 'totals': totals, 'data_revision': 2,
            'manifest_sha256': hashlib.sha256((root / 'manifest.json').read_bytes()).hexdigest(),
            'qualification_limits': ['exact held-out transcript overlap rejected; independent cross-source speaker/near-duplicate qualification not yet established'],
            'compute': {'wall_seconds': round(time.time() - started, 1), 'gpu_seconds': 0, 'device': 'cpu'},
            'raw_media_exported': False, 'text_exported': False, 'paths_exported': False, 'training_started': False, 'sealed_admission_read': False}