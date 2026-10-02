"""Estate language evidence on the GPU host. Every GPU the host exposes takes a balanced share of the staged recordings and reads
them window by window with the admitted music detector and the current audio language model; transcripts are measured
deterministically. Only aggregates and compact rows leave the host — media, transcript text and paths stay in the job directory."""
import hashlib
import json
import os
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

AUDIO = {'.wav', '.flac', '.mp3', '.ogg', '.m4a'}
SR = 16000
WIN_S = 2.0

DEVICE_MAIN = '''import sys, json
sys.path.insert(0, sys.argv[1])
from services.training_lab.estate_language_worker import run_device
run_device(json.load(open(sys.argv[2])), int(sys.argv[3]))
'''


def _ref(corpus, path):
    return hashlib.sha256(str(Path(path).relative_to(corpus)).encode()).hexdigest()[:16]


def enumerate_files(corpus):
    out = []
    for language in sorted(corpus.iterdir()):
        if not language.is_dir() or language.is_symlink(): continue
        for audio in sorted(language.glob('*/audio/*')):
            if audio.suffix.lower() not in AUDIO or audio.is_symlink() or not audio.resolve().is_relative_to(corpus): continue
            transcript = audio.parent.parent / 'transcript' / (audio.stem + '.txt')
            stat = audio.stat()
            out.append({'ref': _ref(corpus, audio), 'language': language.name, 'session': audio.parent.parent.name, 'path': str(audio),
                        'transcript': str(transcript) if transcript.exists() else None, 'bytes': stat.st_size, 'modified': time.strftime('%Y-%m-%d', time.gmtime(stat.st_mtime))})
    return out


def balance(files, devices):
    """Largest-first greedy split by bytes: every device gets the same work, not the same file count."""
    queues, load = [[] for _ in devices], [0] * len(devices)
    for item in sorted(files, key=lambda f: -f['bytes']):
        index = load.index(min(load)); queues[index].append(item); load[index] += item['bytes']
    return queues


def transcript_measures(path):
    segments, chars, words, speakers = 0, 0, 0, set()
    for line in Path(path).read_text(errors='ignore').splitlines():
        parts = line.split('\t')
        if len(parts) < 4: continue
        text = parts[3].strip()
        if not text: continue
        segments += 1; chars += len(text); words += len(text.split()); speakers.add(parts[2].strip())
    return {'segments': segments, 'chars': chars, 'words': words, 'speakers': len(speakers)}


def _decode(path, max_seconds):
    import numpy as np
    cmd = ['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-t', str(max_seconds), '-']
    raw = subprocess.run(cmd, capture_output=True, timeout=900, check=False).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def _starts(samples, cap):
    win = int(WIN_S * SR); total = samples // win
    if total <= cap: return [i * win for i in range(total)], total
    step = total / cap
    return [int(i * step) * win for i in range(cap)], total


def _load_models(control, device):
    import torch
    from torch import nn
    from peft import PeftModel
    from transformers import WhisperModel, WhisperProcessor
    from services.audio_plane_v1.corrective_model import FRAMES, Featurizer
    from services.training_lab import music_detector_worker as md
    reg = json.loads((Path(control['lab_corpus_root']) / 'base_registration.json').read_text())
    local = reg['whisper-lid-v1-mit']['local_path']
    base = WhisperModel.from_pretrained(local, local_files_only=True).encoder
    base.config.max_source_positions = FRAMES // 2
    base.embed_positions = nn.Embedding.from_pretrained(base.embed_positions.weight[:FRAMES // 2].detach().clone(), freeze=True)
    art = Path(control['audio_model_dir'])
    encoder = PeftModel.from_pretrained(base, str(art / 'lora_adapter')).to(device).eval()
    head = torch.load(art / 'language_head.pt', map_location=device)
    dim = head['projection']['1.weight'].shape[0]
    project = nn.Sequential(nn.LayerNorm(base.config.d_model), nn.Linear(base.config.d_model, dim), nn.GELU()).to(device); project.load_state_dict(head['projection']); project.eval()
    language_head = nn.Linear(dim, len(head['classes'])).to(device); language_head.load_state_dict(head['language_head']); language_head.eval()
    music_ckpt = torch.load(Path(control['music_model_path']), map_location=device)
    music = md._model(device); music.load_state_dict(music_ckpt['state_dict']); music.eval()
    return {'encoder': encoder, 'project': project, 'language_head': language_head, 'classes': list(head['classes']), 'threshold': float(head.get('threshold', 0.6)),
            'featurizer': Featurizer(WhisperProcessor.from_pretrained(local, local_files_only=True), device), 'music': music, 'music_featurizer': md._Featurizer(device),
            'music_threshold': float(music_ckpt['config']['threshold'])}


def _read_file(models, item, control, device):
    import numpy as np
    import torch
    pcm = _decode(item['path'], float(control['max_seconds_per_file']))
    starts, total_windows = _starts(pcm.shape[0], int(control['max_windows_per_file']))
    if not starts: return {'error': 'NO_FULL_WINDOW', 'duration_s': round(pcm.shape[0] / SR, 2)}
    win = int(WIN_S * SR)
    windows = np.stack([pcm[s:s + win] for s in starts])
    loud = np.sqrt((windows ** 2).mean(1)) > 1e-4  # digital silence is neither music nor a language
    silence = int((~loud).sum()); windows = windows[loud]
    if not len(windows): return {'error': 'ALL_SILENCE', 'duration_s': round(pcm.shape[0] / SR, 2), 'silence_windows': silence}
    labels, confidences, music_p = [], [], []
    batch = int(control['batch_size'])
    with torch.no_grad():
        for i in range(0, len(windows), batch):
            chunk = torch.from_numpy(windows[i:i + batch]).to(device)
            pcm16 = (chunk * 32767.0).to(torch.int16)
            with torch.autocast('cuda', dtype=torch.bfloat16):
                enc = models['encoder'](input_features=models['featurizer'](pcm16)).last_hidden_state.mean(1)
            probs = torch.softmax(models['language_head'](models['project'](enc.float())), dim=-1)
            conf, idx = probs.max(dim=-1)
            labels.extend(idx.tolist()); confidences.extend(conf.tolist())
            music_p.extend(torch.sigmoid(models['music'](models['music_featurizer'](chunk)).squeeze(1)).tolist())
    classes, threshold = models['classes'], models['threshold']
    by_language, abstained, music_windows = Counter(), 0, 0
    for label, conf, mp in zip(labels, confidences, music_p):
        if mp >= models['music_threshold']: music_windows += 1
        elif conf >= threshold: by_language[classes[label]] += 1
        else: abstained += 1
    judged = sum(by_language.values()); top = by_language.most_common(1)[0] if judged else (None, 0)
    return {'duration_s': round(pcm.shape[0] / SR, 2), 'windows_total': total_windows, 'windows_read': len(windows), 'silence_windows': silence, 'music_windows': music_windows,
            'speech_windows': len(windows) - music_windows, 'abstained': abstained, 'judged': judged, 'by_language': dict(by_language),
            'top_language': top[0], 'top_share': round(top[1] / judged, 4) if judged else None, 'mean_confidence': round(float(np.mean(confidences)), 4),
            'music_share': round(music_windows / len(windows), 4)}


def run_device(control, index):
    """One GPU process: its queue, the two models, a hard elapsed-time share of the signed compute cap, progress to its own file."""
    import torch
    torch.backends.cuda.matmul.allow_tf32 = True; torch.backends.cudnn.allow_tf32 = True
    job_dir = Path(control['job_dir']); device = 'cuda'
    queue = json.loads((job_dir / f'queue_{index}.json').read_text())
    cap_s = float(control['compute_cap_gpu_hours']) * 3600 / max(1, int(control['device_count']))
    started = time.time(); models = _load_models(control, device)
    progress = {'device': index, 'files': 0, 'of': len(queue), 'windows': 0, 'elapsed_s': 0, 'stage': 'reading', 'cap_s': int(cap_s)}
    out = open(job_dir / f'rows_{index}.jsonl', 'w')
    for position, item in enumerate(queue):
        elapsed = time.time() - started
        if elapsed >= cap_s:
            progress.update(stage='stopped at the compute cap', not_reached=len(queue) - position); break
        try: reading = _read_file(models, item, control, device)
        except Exception as exc: reading = {'error': type(exc).__name__[:60]}
        row = {'ref': item['ref'], 'language': item['language'], 'session': item['session'], 'bytes': item['bytes'], 'modified': item['modified'], 'device': index, **reading}
        if item.get('transcript'):
            try: row['transcript'] = transcript_measures(item['transcript'])
            except Exception as exc: row['transcript'] = {'error': type(exc).__name__[:60]}
        out.write(json.dumps(row, sort_keys=True) + '\n'); out.flush()
        progress.update(files=position + 1, windows=progress['windows'] + int(reading.get('windows_read') or 0), elapsed_s=int(time.time() - started),
                        gpu_peak_gb=round(torch.cuda.max_memory_allocated() / 2 ** 30, 2))
        (job_dir / f'progress_{index}.json').write_text(json.dumps(progress))
    else:
        progress['stage'] = 'queue complete'
    progress.update(elapsed_s=int(time.time() - started), finished=True, windows_per_second=round(progress['windows'] / max(1e-6, time.time() - started), 1))
    (job_dir / f'progress_{index}.json').write_text(json.dumps(progress))
    out.close()


def _aggregate(rows):
    per = {}
    for language in sorted({r['language'] for r in rows}):
        group = [r for r in rows if r['language'] == language]; read = [r for r in group if 'windows_read' in r]
        total_read = sum(r['windows_read'] for r in read) or 1
        by_language = Counter()
        for r in read: by_language.update(r['by_language'])
        judged = sum(by_language.values())
        transcripts = [r['transcript'] for r in group if isinstance(r.get('transcript'), dict) and 'chars' in r['transcript']]
        music_share = sum(r['music_windows'] for r in read) / total_read
        hours = sum(r['duration_s'] for r in read) / 3600
        per[language] = {'files': len(group), 'read': len(read), 'errors': len(group) - len(read), 'hours_recorded': round(hours, 4),
                         'hours_music_estimate': round(hours * music_share, 4), 'hours_speech_estimate': round(hours * (1 - music_share), 4),
                         'windows_read': total_read if read else 0, 'music_windows': sum(r['music_windows'] for r in read), 'abstained': sum(r['abstained'] for r in read), 'judged': judged,
                         'predicted_language_share': {k: round(v / judged, 4) for k, v in by_language.most_common()} if judged else {},
                         'agrees_with_folder_label': round(by_language.get(language, 0) / judged, 4) if judged else None,
                         'files_top_language_matches_folder': sum(1 for r in read if r.get('top_language') == language),
                         'files_with_music_majority': sum(1 for r in read if (r.get('music_share') or 0) >= 0.5),
                         'transcripts': {'files': len(transcripts), 'segments': sum(t['segments'] for t in transcripts), 'chars': sum(t['chars'] for t in transcripts), 'words': sum(t['words'] for t in transcripts)},
                         'mean_confidence': round(sum(r['mean_confidence'] for r in read) / len(read), 4) if read else None}
    return per


def classify_estate(control, state):
    import torch
    root = Path(control['lab_corpus_root']).resolve(); corpus = root / 'corpus' / 'datasets'
    if not corpus.is_dir(): raise ValueError('AUTHORIZED_STAGED_CORPUS_NOT_FOUND')
    device_count = torch.cuda.device_count()
    if device_count < 1: raise ValueError('NO_GPU_VISIBLE')
    devices = list(range(device_count)); control = {**control, 'device_count': device_count}
    files = enumerate_files(corpus)
    job_dir = Path(control['job_dir']); started = time.time()
    (job_dir / 'results_map.json').write_text(json.dumps({f['ref']: str(Path(f['path']).relative_to(corpus)) for f in files}, indent=0, sort_keys=True))
    queues = balance(files, devices)
    for index, queue in zip(devices, queues): (job_dir / f'queue_{index}.json').write_text(json.dumps(queue))
    (job_dir / 'device_control.json').write_text(json.dumps({k: v for k, v in control.items() if k != 'bundle'}))
    bundle = next(p for p in sys.path if p.endswith('worker.zip'))
    procs = {index: subprocess.Popen([sys.executable, '-c', DEVICE_MAIN, bundle, str(job_dir / 'device_control.json'), str(index)],
                                     env={**os.environ, 'CUDA_VISIBLE_DEVICES': str(index), 'OMP_NUM_THREADS': '8'}, stdout=open(job_dir / f'device_{index}.log', 'ab'), stderr=subprocess.STDOUT)
             for index in devices}
    state.update(progress={'stage': 'reading staged audio on every GPU', 'devices': device_count, 'files': 0, 'of': len(files), 'elapsed_s': 0})
    while any(p.poll() is None for p in procs.values()):
        time.sleep(15)
        per_device = [json.loads((job_dir / f'progress_{i}.json').read_text()) for i in devices if (job_dir / f'progress_{i}.json').exists()]
        state.update(progress={'stage': 'reading staged audio on every GPU', 'devices': device_count, 'files': sum(p['files'] for p in per_device), 'of': len(files),
                               'windows': sum(p['windows'] for p in per_device), 'elapsed_s': int(time.time() - started), 'per_device': per_device})
    per_device = [json.loads((job_dir / f'progress_{i}.json').read_text()) for i in devices if (job_dir / f'progress_{i}.json').exists()]
    failed = [i for i, p in procs.items() if p.returncode != 0]
    rows = []
    for index in devices:
        path = job_dir / f'rows_{index}.jsonl'
        if path.exists(): rows.extend(json.loads(line) for line in path.read_text().splitlines() if line.strip())
    if not rows: raise ValueError('NO_DEVICE_PRODUCED_ROWS:' + ','.join(str(i) for i in failed))
    compact = json.dumps(rows, separators=(',', ':'), sort_keys=True)
    (job_dir / 'results_compact.json').write_text(compact)
    reached = {r['ref'] for r in rows}
    gpu_seconds = sum(p.get('elapsed_s', 0) for p in per_device)
    state.update(progress={'stage': 'complete', 'files': len(rows), 'of': len(files), 'elapsed_s': int(time.time() - started)})
    return {'scope': 'authorized staged language-cognition corpus on this host; not the whole RMS estate', 'evidence_class': 'model_readings_not_human_labels',
            'models': {'audio_language': {'artefact_dir': str(Path(control['audio_model_dir']).name), 'sha256': control.get('audio_model_sha256'), 'classes': sorted({k for r in rows for k in (r.get('by_language') or {})})},
                       'music_detector': {'artefact_path': str(Path(control['music_model_path']).parent.name), 'sha256': control.get('music_model_sha256')}},
            'files': len(files), 'read': len(rows), 'not_reached': len(files) - len(reached), 'errors': sum(1 for r in rows if 'error' in r),
            'per_language': _aggregate(rows), 'devices': device_count, 'per_device': per_device, 'device_failures': failed,
            'compute': {'wall_seconds': round(time.time() - started, 1), 'gpu_seconds_total': gpu_seconds, 'gpu_hours_total': round(gpu_seconds / 3600, 3),
                        'cap_gpu_hours': control['compute_cap_gpu_hours'], 'windows_per_second_per_device': [p.get('windows_per_second') for p in per_device]},
            'compact_rows_sha256': hashlib.sha256(compact.encode()).hexdigest(), 'compact_rows_bytes': len(compact),
            'training_started': False, 'raw_media_exported': False, 'paths_exported': False}


# ----------------------------------------------------------------------------- transcripts through the served text model (loopback on its host)
def classify_text(control, state):
    import urllib.request
    root = Path(control['lab_corpus_root']).resolve(); corpus = root / 'corpus' / 'datasets'
    if not corpus.is_dir(): raise ValueError('AUTHORIZED_STAGED_CORPUS_NOT_FOUND')
    skip = set(control.get('skip_refs') or [])
    files = [f for f in enumerate_files(corpus) if f.get('transcript') and f['ref'] not in skip]
    if control.get('interleave'):
        # Round-robin across the language folders so a capped pass still reads every language rather than the alphabetically first one.
        by_language = {}
        for f in files: by_language.setdefault(f['language'], []).append(f)
        files = [f for i in range(max(len(v) for v in by_language.values())) for v in by_language.values() for f in v[i:i + 1]]
    url = f"http://127.0.0.1:{int(control['port'])}/classify"; started = time.time(); rows = []; shas = set()
    cap_s = float(control['compute_cap_gpu_hours']) * 3600; chunk_chars = int(control['chunk_chars']); batch = int(control['batch_size'])
    state.update(progress={'stage': 'classifying transcripts through the served text model', 'files': 0, 'of': len(files)})
    for position, item in enumerate(files):
        if time.time() - started >= cap_s: break
        text = ' '.join(p.split('\t')[3].strip() for p in Path(item['transcript']).read_text(errors='ignore').splitlines() if len(p.split('\t')) >= 4)
        units = [text[i:i + chunk_chars] for i in range(0, len(text), chunk_chars) if text[i:i + chunk_chars].strip()]
        labels = []
        for i in range(0, len(units), batch):
            req = urllib.request.Request(url, data=json.dumps({'texts': units[i:i + batch]}).encode(), headers={'Content-Type': 'application/json'}, method='POST')
            try:
                with urllib.request.urlopen(req, timeout=300) as r: body = json.loads(r.read())
                labels.extend(res.get('label') for res in body.get('results', [])); shas.add((body.get('lineage') or {}).get('artefact_sha256'))
            except Exception as exc:
                labels.extend([f'error:{type(exc).__name__}'] * len(units[i:i + batch]))
        by_language = Counter(l for l in labels if l and not str(l).startswith('error'))
        rows.append({'ref': item['ref'], 'language': item['language'], 'session': item['session'], 'chars': len(text), 'words': len(text.split()), 'units': len(units),
                     'by_language': dict(by_language), 'errors': sum(1 for l in labels if not l or str(l).startswith('error')),
                     'top_language': by_language.most_common(1)[0][0] if by_language else None})
        if position % 25 == 0: state.update(progress={'stage': 'classifying transcripts through the served text model', 'files': position + 1, 'of': len(files), 'elapsed_s': int(time.time() - started)})
    per = {}
    for language in sorted({r['language'] for r in rows}):
        group = [r for r in rows if r['language'] == language]; by_language = Counter()
        for r in group: by_language.update(r['by_language'])
        judged = sum(by_language.values())
        per[language] = {'files': len(group), 'chars': sum(r['chars'] for r in group), 'words': sum(r['words'] for r in group), 'units': sum(r['units'] for r in group), 'judged_units': judged,
                         'predicted_language_share': {k: round(v / judged, 4) for k, v in by_language.most_common()} if judged else {},
                         'agrees_with_folder_label': round(by_language.get(language, 0) / judged, 4) if judged else None, 'files_top_language_matches_folder': sum(1 for r in group if r.get('top_language') == language)}
    compact = json.dumps(rows, separators=(',', ':'), sort_keys=True)
    (Path(control['job_dir']) / 'results_compact.json').write_text(compact)
    (Path(control['job_dir']) / 'results_map.json').write_text(json.dumps({f['ref']: str(Path(f['path']).relative_to(corpus)) for f in files}, indent=0, sort_keys=True))
    return {'scope': 'transcripts of the authorized staged corpus on this host', 'evidence_class': 'served_text_model_readings', 'model': {'served_port': int(control['port']), 'artefact_sha256_seen': sorted(s for s in shas if s)},
            'files': len(files), 'read': len(rows), 'not_reached': len(files) - len(rows), 'skipped_already_read': len(skip), 'interleaved': bool(control.get('interleave')), 'per_language': per,
            'compute': {'wall_seconds': round(time.time() - started, 1), 'cap_gpu_hours': control['compute_cap_gpu_hours'], 'note': 'served adapter already resident on its GPU; this job adds inference load only'},
            'compact_rows_sha256': hashlib.sha256(compact.encode()).hexdigest(), 'compact_rows_bytes': len(compact), 'training_started': False, 'raw_media_exported': False, 'paths_exported': False}
