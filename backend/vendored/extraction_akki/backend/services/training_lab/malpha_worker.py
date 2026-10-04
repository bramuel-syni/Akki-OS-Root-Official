"""Mα worker — runs on the admitted GPU host, never on E1. Audio is a database: every staged recording of a commissioned language becomes
provenance-paired segment rows (content, timing, speaker-local label, cluster, condition, discoverable-spectrum columns), a 16 kHz PCM store
addressable by segment, and Mimi codec tokens (content stream = codebook 0, character stream = codebooks 1–7). Splits are sealed by speaker
cluster before any training. The listener lane fine-tunes Whisper on the train split and measures words, mentions and timing per language on
the dev split; the sealed admission split is only read by the separate `malpha_evaluate` phase. Only aggregates leave the host."""
import hashlib
import json
import math
import os
import random
import re
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path

SR16 = 16000
SR24 = 24000
LANG_NAMES = {'kik': 'Kikuyu', 'kam': 'Kikamba', 'swa': 'Kiswahili'}
FEATURES = ('duration_s', 'chars_per_s', 'energy_db_mean', 'energy_db_std', 'pause_ratio', 'f0_mean_hz', 'f0_std_semitones', 'f0_range_hz', 'voiced_ratio',
            'spectral_centroid_hz', 'spectral_bandwidth_hz', 'spectral_rolloff_hz', 'spectral_flatness', 'zcr')
MIMI_REPO = 'kyutai/mimi'
MIMI_CODEBOOKS = 8
MIMI_FRAME_HZ = 12.5
CODE_PAD, CODE_BOS, CODE_EOS = 2048, 2049, 2050
CODE_VOCAB = 2051


def now():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def _ref(corpus, path):
    return hashlib.sha256(str(Path(path).relative_to(corpus)).encode()).hexdigest()[:16]


def _sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def decode_audio(path, sr, start=None, duration=None, max_seconds=None):
    import numpy as np
    cmd = ['ffmpeg', '-v', 'error']
    if start is not None: cmd += ['-ss', f'{start:.3f}']
    cmd += ['-i', str(path), '-f', 'f32le', '-ac', '1', '-ar', str(sr)]
    if duration is not None: cmd += ['-t', f'{duration:.3f}']
    elif max_seconds is not None: cmd += ['-t', str(max_seconds)]
    raw = subprocess.run(cmd + ['-'], capture_output=True, timeout=1800, check=False).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def parse_transcript(path):
    out = []
    for line in Path(path).read_text(errors='ignore').splitlines():
        parts = line.split('\t')
        if len(parts) < 4: continue
        try: start, end = float(parts[0]), float(parts[1])
        except ValueError: continue
        text = ' '.join(parts[3].split())
        if end > start and text: out.append((start, end, parts[2].strip(), text))
    return out


def normalise_text(text):
    return ' '.join(re.sub(r"[^\w\s'’-]", ' ', text.lower()).split())


def enumerate_language(corpus, lang):
    out = []
    for audio in sorted((corpus / lang).glob('*/audio/*')):
        if audio.suffix.lower() not in {'.wav', '.flac', '.mp3', '.ogg', '.m4a'} or audio.is_symlink(): continue
        transcript = audio.parent.parent / 'transcript' / (audio.stem + '.txt')
        if not transcript.exists(): continue
        out.append({'ref': _ref(corpus, audio), 'language': lang, 'session': audio.parent.parent.name, 'file': audio.stem, 'path': str(audio), 'transcript': str(transcript), 'bytes': audio.stat().st_size})
    return out


# ----------------------------------------------------------------------------- discoverable spectrum: the queryable columns of one segment
def estimate_f0(y, sr, fmin=60.0, fmax=450.0, frame=0.04, hop=0.01):
    """Frame-wise normalised autocorrelation pitch (numpy only — the numba path in librosa.yin segfaults on the hosts). Returns f0 per frame, 0 where unvoiced."""
    import numpy as np
    n, h = int(frame * sr), int(hop * sr)
    if len(y) < n: return np.zeros(0), np.zeros(0, dtype=bool)
    idx = np.arange(0, len(y) - n + 1, h)[:, None] + np.arange(n)[None, :]
    frames = y[idx] * np.hanning(n)[None, :]
    spec = np.fft.rfft(frames, n=2 * n, axis=1); acf = np.fft.irfft(np.abs(spec) ** 2, axis=1)[:, :n]
    acf = acf / np.maximum(acf[:, :1], 1e-9)
    lo, hi = int(sr / fmax), int(sr / fmin)
    window = acf[:, lo:hi]; lag = window.argmax(1) + lo; peak = window.max(1)
    energy = np.sqrt((frames ** 2).mean(1))
    voiced = (peak > 0.45) & (energy > max(1e-4, 0.1 * np.median(energy) if energy.size else 1e-4))
    f0 = np.where(voiced, sr / np.maximum(lag, 1), 0.0)
    return f0, voiced


def resample(y, src, dst):
    from math import gcd

    from scipy.signal import resample_poly
    g = gcd(int(src), int(dst))
    return resample_poly(y, int(dst) // g, int(src) // g).astype('float32')


def spectrum_features(y, sr, chars=None):
    import librosa
    import numpy as np
    dur = len(y) / sr
    if dur < 0.3: return None
    hop, frame = 160, 400
    rms = librosa.feature.rms(y=y, frame_length=frame, hop_length=hop)[0]
    db = 20 * np.log10(np.maximum(rms, 1e-6))
    active = db > (db.max() - 35)
    f0, voiced = estimate_f0(y, sr)
    f0v = f0[voiced]
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop)[0]
    bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr, hop_length=hop)[0]
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, hop_length=hop)[0]
    flatness = librosa.feature.spectral_flatness(y=y, hop_length=hop)[0]
    zcr = librosa.feature.zero_crossing_rate(y, frame_length=frame, hop_length=hop)[0]
    semis = 12 * np.log2(f0v / 100.0) if len(f0v) > 2 else np.zeros(0)
    return {'duration_s': round(dur, 3), 'chars_per_s': round(chars / dur, 3) if chars else None,
            'energy_db_mean': round(float(db[active].mean()) if active.any() else float(db.mean()), 2), 'energy_db_std': round(float(db[active].std()) if active.any() else 0.0, 2),
            'pause_ratio': round(float(1 - active.mean()), 4), 'f0_mean_hz': round(float(f0v.mean()), 1) if len(f0v) > 2 else None,
            'f0_std_semitones': round(float(semis.std()), 3) if len(semis) > 2 else None, 'f0_range_hz': round(float(np.percentile(f0v, 90) - np.percentile(f0v, 10)), 1) if len(f0v) > 2 else None,
            'voiced_ratio': round(float(voiced.mean()), 4) if len(voiced) else 0.0, 'spectral_centroid_hz': round(float(centroid.mean()), 1), 'spectral_bandwidth_hz': round(float(bandwidth.mean()), 1),
            'spectral_rolloff_hz': round(float(rolloff.mean()), 1), 'spectral_flatness': round(float(flatness.mean()), 5), 'zcr': round(float(zcr.mean()), 5)}


def _analyse_file(args):
    """One recording → segment rows + 16 kHz int16 PCM blocks. Runs in a CPU pool; nothing touches the GPU here."""
    item, min_s, max_s = args
    import numpy as np
    try:
        pcm = decode_audio(item['path'], SR16)
    except Exception as exc:
        return item['ref'], {'error': type(exc).__name__[:60]}, [], []
    rows, blocks = [], []
    total = len(pcm) / SR16
    for start, end, speaker, text in parse_transcript(item['transcript']):
        if end - start < min_s or end - start > max_s or start >= total: continue
        y = pcm[int(start * SR16):int(min(end, total) * SR16)]
        if len(y) < int(min_s * SR16) or float(np.abs(y).max()) < 1e-4: continue
        feats = spectrum_features(y, SR16, len(text))
        if not feats: continue
        seg_id = _sha(f"{item['ref']}:{start:.3f}:{end:.3f}")[:16]
        rows.append({'seg_id': seg_id, 'ref': item['ref'], 'session': item['session'], 'file': item['file'], 'start': round(start, 3), 'end': round(end, 3), 'speaker': speaker,
                     'chars': len(text), 'words': len(text.split()), 'text_sha256': _sha(text), 'features': feats, 'text': text})
        blocks.append((seg_id, (np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()))
    return item['ref'], {'duration_s': round(total, 2), 'segments': len(rows)}, rows, blocks


def _split_bucket(seed, lang, key):
    return int(hashlib.sha256(f'{seed}:{lang}:{key}'.encode()).hexdigest()[:8], 16) % 100


def assign_splits(rows, clusters, seed, lang, admission_pct=10, dev_pct=10):
    """Speaker-cluster-disjoint sealing: a cluster (presenter heard across sessions) lands in one split; sessions whose speakers straddle splits
    fall back to train so dev/admission never hear a training voice."""
    def bucket(key):
        b = _split_bucket(seed, lang, key)
        return 'admission' if b < admission_pct else 'dev' if b < admission_pct + dev_pct else 'train'
    session_split = {}
    by_session = defaultdict(set)
    for r in rows:
        cid = clusters.get(f"{r['session']}|{r['speaker']}")
        by_session[r['session']].add(f'c{cid}' if cid is not None else f"s:{r['session']}")
    for session, keys in by_session.items():
        splits = {bucket(k) for k in keys}
        session_split[session] = splits.pop() if len(splits) == 1 else 'train'
    for r in rows: r['split'] = session_split[r['session']]
    return session_split


# ----------------------------------------------------------------------------- Mimi codec: content + character streams with provenance
def load_mimi(device):
    from transformers import AutoFeatureExtractor, MimiModel
    model = MimiModel.from_pretrained(MIMI_REPO).to(device).eval()
    fe = AutoFeatureExtractor.from_pretrained(MIMI_REPO)
    try:
        from huggingface_hub import model_info
        revision = model_info(MIMI_REPO).sha
    except Exception:
        revision = getattr(model.config, '_commit_hash', None)
    provenance = {'repo': MIMI_REPO, 'revision': revision, 'codebooks_used': MIMI_CODEBOOKS, 'codebook_size': int(model.config.codebook_size), 'frame_rate_hz': MIMI_FRAME_HZ,
                  'tokens_per_second': MIMI_CODEBOOKS * MIMI_FRAME_HZ, 'content_stream': 'codebook 0 (semantic, WavLM-distilled)', 'character_stream': 'codebooks 1-7 (acoustic residual)',
                  'sampling_rate': int(fe.sampling_rate), 'dtype': str(next(model.parameters()).dtype)}
    return model, fe, provenance


def mimi_encode(model, wav24, device):
    """wav24: list of float32 arrays at 24 kHz → list of LongTensor (8, T) on CPU."""
    import torch
    out = []
    for y in wav24:
        x = torch.from_numpy(y).to(device)[None, None, :]
        with torch.no_grad():
            codes = model.encode(x, num_quantizers=MIMI_CODEBOOKS).audio_codes[0]
        out.append(codes.cpu())
    return out


def mimi_decode(model, codes, device):
    import torch
    with torch.no_grad():
        audio = model.decode(codes.to(device)[None]).audio_values[0, 0]
    return audio.float().cpu().numpy()


def _log_mel(y, sr):
    import librosa
    import numpy as np
    m = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=1024, hop_length=256, n_mels=80)
    return np.log(np.maximum(m, 1e-5))


def _si_sdr(ref, est):
    import numpy as np
    n = min(len(ref), len(est)); ref, est = ref[:n], est[:n]
    alpha = float(np.dot(est, ref) / (np.dot(ref, ref) + 1e-9)); target = alpha * ref; noise = est - target
    return round(float(10 * np.log10((np.dot(target, target) + 1e-9) / (np.dot(noise, noise) + 1e-9))), 2)


def codec_qualification(model, fe, rows_by_lang, pcm_store, device, per_language, seed):
    """Measured round trip per language and condition: full 8-codebook reconstruction versus content-only (codebook 0) reconstruction."""
    import numpy as np
    rng = random.Random(seed); out = {}
    for lang, rows in rows_by_lang.items():
        candidates = [r for r in rows if r['split'] == 'train' and 2.0 <= r['features']['duration_s'] <= 12.0]
        sample = rng.sample(candidates, min(per_language, len(candidates)))
        by_condition = defaultdict(list)
        for r in sample:
            y16 = pcm_store.read(lang, r).astype(np.float32) / 32767.0
            y24 = resample(y16, SR16, SR24)
            codes = mimi_encode(model, [y24], device)[0]
            full = mimi_decode(model, codes, device); content = mimi_decode(model, codes[:1], device)
            n = min(len(y24), len(full), len(content)); y24, full, content = y24[:n], full[:n], content[:n]
            mel = _log_mel(y24, SR24); mel_full = _log_mel(full, SR24); mel_content = _log_mel(content, SR24)
            f0_o, v_o = estimate_f0(y24, SR24); f0_f, v_f = estimate_f0(full, SR24)
            k = min(len(f0_o), len(f0_f)); both = v_o[:k] & v_f[:k]
            corr = float(np.corrcoef(f0_o[:k][both], f0_f[:k][both])[0, 1]) if both.sum() > 4 else None
            cond = r.get('condition', 'unknown')
            by_condition[cond].append({'frames': int(codes.shape[1]), 'seconds': round(n / SR24, 3), 'mel_l1_full': round(float(np.abs(mel - mel_full).mean()), 4),
                                       'mel_l1_content_only': round(float(np.abs(mel - mel_content).mean()), 4), 'si_sdr_full': _si_sdr(y24, full), 'si_sdr_content_only': _si_sdr(y24, content),
                                       'f0_corr_full': round(corr, 4) if corr is not None and not math.isnan(corr) else None})
        summary = {}
        def agg(items, key):
            vals = [i[key] for i in items if i[key] is not None]
            return round(float(np.mean(vals)), 4) if vals else None
        for cond, items in by_condition.items():
            frames, seconds = sum(i['frames'] for i in items), sum(i['seconds'] for i in items)
            summary[cond] = {'segments': len(items), 'measured_tokens_per_second': round(MIMI_CODEBOOKS * frames / seconds, 2), 'measured_frame_rate_hz': round(frames / seconds, 3),
                             'mel_l1_full': agg(items, 'mel_l1_full'), 'mel_l1_content_only': agg(items, 'mel_l1_content_only'), 'si_sdr_full': agg(items, 'si_sdr_full'), 'si_sdr_content_only': agg(items, 'si_sdr_content_only'),
                             'f0_corr_full': agg(items, 'f0_corr_full'),
                             'content_character_separation_observed': bool(agg(items, 'mel_l1_content_only') and agg(items, 'mel_l1_full') and agg(items, 'mel_l1_content_only') > agg(items, 'mel_l1_full') * 1.15)}
        out[lang] = summary
    return out


class PcmStore:
    """Segment-addressable 16 kHz int16 store per language: `pcm16k_<lang>.bin` + offsets in the row (a row may name another store file, e.g. the
    internet-corpus dataset). Timestamp → source playback resolves here."""

    def __init__(self, root):
        self.root = Path(root); self.handles = {}

    def path(self, lang):
        return self.root / f'pcm16k_{lang}.bin'

    def read(self, lang, row):
        import numpy as np
        key = row.get('pcm_file') or f'pcm16k_{lang}.bin'
        if key not in self.handles: self.handles[key] = open(self.root / key, 'rb')
        h = self.handles[key]; h.seek(row['pcm_offset']); buf = h.read(row['pcm_bytes'])
        return np.frombuffer(buf, dtype=np.int16)


def load_rows(aip_dir, lang, with_text=False, dataset='radio'):
    """`dataset='radio'` is the staged estate corpus (sealed splits); `'internet'` is the separately provenance-tagged public corpus (train only)."""
    prefix = '' if dataset == 'radio' else f'{dataset}_'
    seg_path = Path(aip_dir) / f'segments_{prefix}{lang}.jsonl'
    if not seg_path.exists(): return []
    rows = [json.loads(l) for l in seg_path.read_text().splitlines() if l.strip()]
    if with_text:
        text = {}
        for l in (Path(aip_dir) / f'text_{prefix}{lang}.jsonl').read_text().splitlines():
            if l.strip(): d = json.loads(l); text[d['seg_id']] = d['text']
        for r in rows: r['text'] = text.get(r['seg_id'], '')
    return rows


def _write_rows_atomic(path, rows, key=lambda r: (r['session'], r['start'])):
    tmp = Path(str(path) + '.tmp')
    with open(tmp, 'w') as fh:
        for r in sorted(rows, key=key): fh.write(json.dumps({k: v for k, v in r.items() if k != 'text'}, sort_keys=True) + '\n')
    os.replace(tmp, path)


def brand_inventory(rows_by_lang, lexicon):
    """How often each brand/alias is said per language and split; exact mention set per segment is recorded on the row (sealed with it)."""
    compiled = [(b['brand'], re.compile(r'(?<!\w)(' + '|'.join(re.escape(normalise_text(a)) for a in [b['brand']] + b.get('aliases', [])) + r')(?!\w)')) for b in lexicon]
    inventory = {}
    for lang, rows in rows_by_lang.items():
        counts = defaultdict(Counter)
        for r in rows:
            text = normalise_text(r['text']); hits = sorted({brand for brand, rx in compiled if rx.search(text)})
            r['mentions'] = hits
            for h in hits: counts[h][r['split']] += 1
        inventory[lang] = {brand: dict(c) for brand, c in counts.items()}
    return inventory


def percentiles(values):
    import numpy as np
    v = np.array([x for x in values if x is not None], dtype=float)
    if not len(v): return None
    return {'n': int(len(v)), 'p10': round(float(np.percentile(v, 10)), 3), 'p50': round(float(np.percentile(v, 50)), 3), 'p90': round(float(np.percentile(v, 90)), 3),
            'mean': round(float(v.mean()), 3), 'std': round(float(v.std()), 3)}


def character_register(rows):
    """Group-level learned character per language: distributions only, no per-speaker row, no anatomical identity."""
    return {f: percentiles([r['features'].get(f) for r in rows]) for f in FEATURES}


# ----------------------------------------------------------------------------- phase: build the audio database
SHARD_MAIN = '''import sys, json
sys.path.insert(0, sys.argv[1])
from services.training_lab.malpha_worker import run_shard
run_shard(sys.argv[2], int(sys.argv[3]))
'''


def run_shard(shard_dir, index):
    """One CPU shard process: reads its file list, writes rows + PCM blocks for its shard; the parent merges. Proven subprocess pattern, no fork after torch."""
    import faulthandler
    faulthandler.enable()
    shard = Path(shard_dir); files = json.loads((shard / f'files_{index}.json').read_text())
    min_s, max_s = 0.8, 30.0
    with open(shard / f'rows_{index}.jsonl', 'w') as rows_out, open(shard / f'pcm_{index}.bin', 'wb') as pcm:
        for item in files:
            ref, info, seg_rows, blocks = _analyse_file((item, min_s, max_s))
            for r, (seg_id, block) in zip(seg_rows, blocks):
                r['pcm_offset'] = pcm.tell(); r['pcm_bytes'] = len(block); pcm.write(block)
            rows_out.write(json.dumps({'ref': ref, 'info': info, 'rows': seg_rows}, ensure_ascii=False) + '\n'); rows_out.flush()
            (shard / f'progress_{index}.json').write_text(json.dumps({'done': files.index(item) + 1, 'of': len(files)}))


def _read_language(files, pcm_path, workers, shard_dir, on_progress):
    import subprocess
    import sys
    shard = Path(shard_dir); shard.mkdir(parents=True, exist_ok=True)
    workers = max(1, min(workers, len(files))) if files else 1
    shards = [[] for _ in range(workers)]
    for i, f in enumerate(sorted(files, key=lambda f: -f['bytes'])): shards[i % workers].append(f)
    for i, group in enumerate(shards): (shard / f'files_{i}.json').write_text(json.dumps(group))
    bundle = next(p for p in sys.path if p.endswith('worker.zip'))
    procs = [subprocess.Popen([sys.executable, '-c', SHARD_MAIN, bundle, str(shard), str(i)], env={**os.environ, 'OMP_NUM_THREADS': '2', 'CUDA_VISIBLE_DEVICES': ''}, stdout=open(shard / f'shard_{i}.log', 'ab'), stderr=subprocess.STDOUT) for i in range(workers)]
    while any(p.poll() is None for p in procs):
        time.sleep(5)
        done = 0
        for i in range(workers):
            try: done += json.loads((shard / f'progress_{i}.json').read_text())['done']
            except (OSError, ValueError): pass
        on_progress(done)
    failed = [i for i, p in enumerate(procs) if p.returncode != 0]
    results = {}
    with open(pcm_path, 'wb') as pcm:
        for i in range(workers):
            rows_path, pcm_shard = shard / f'rows_{i}.jsonl', shard / f'pcm_{i}.bin'
            if not rows_path.exists(): continue
            base = pcm.tell()
            if pcm_shard.exists():
                with open(pcm_shard, 'rb') as src:
                    for block in iter(lambda: src.read(1 << 24), b''): pcm.write(block)
            for line in rows_path.read_text().splitlines():
                if not line.strip(): continue
                d = json.loads(line)
                for r in d['rows']: r['pcm_offset'] += base
                results[d['ref']] = (d['info'], d['rows'])
            pcm_shard.unlink(missing_ok=True)
    return results, failed


def aip_build(control, state):
    root = Path(control['lab_corpus_root']).resolve(); corpus = root / 'corpus' / 'datasets'
    if not corpus.is_dir(): raise ValueError('AUTHORIZED_STAGED_CORPUS_NOT_FOUND')
    out = Path(control['aip_db_dir']); out.mkdir(parents=True, exist_ok=True)
    langs, seed = list(control['languages']), int(control['seed']); started = time.time()
    clusters_doc = json.loads((root / 'speaker_clusters.json').read_text()) if (root / 'speaker_clusters.json').exists() else {'clusters': {}}
    conditions = {}
    files_db = root / 'corpus_db' / 'files.jsonl'
    if files_db.exists():
        for l in files_db.read_text().splitlines():
            if not l.strip(): continue
            d = json.loads(l); a = d.get('audio') or {}
            conditions[(d['code'], d['session'], str(d['file']))] = f"{a.get('codec', '?')}/{a.get('sample_rate', '?')}Hz/{a.get('channels', '?')}ch"
    pcm_store = PcmStore(out); rows_by_lang = {}; files_summary = {}
    for lang in langs:
        files = enumerate_language(corpus, lang)
        limit = int(control.get('max_files_per_language') or 0)
        if limit: files = sorted(files, key=lambda f: f['ref'])[:limit]
        label = f'reading {LANG_NAMES.get(lang, lang)} recordings into the database'
        state.update(progress={'stage': label, 'language': lang, 'files': 0, 'of': len(files), 'elapsed_s': int(time.time() - started)})
        results, failed_shards = _read_language(files, pcm_store.path(lang), int(control.get('cpu_workers', 24)), Path(control['job_dir']) / f'shards_{lang}',
                                                lambda done: state.update(progress={'stage': label, 'language': lang, 'files': done, 'of': len(files), 'elapsed_s': int(time.time() - started)}))
        if failed_shards: state.event(f'{lang}: shard processes {failed_shards} exited non-zero; their unread files are recorded as errors')
        rows, file_rows = [], []
        for item in files:
            info, seg_rows = results.get(item['ref'], ({'error': 'NOT_READ'}, []))
            cond = conditions.get((lang, item['session'], item['file']), 'unknown')
            file_rows.append({'ref': item['ref'], 'session': item['session'], 'file': item['file'], 'bytes': item['bytes'], **info, 'condition': cond})
            for r in seg_rows: r['condition'] = cond; rows.append(r)
        session_split = assign_splits(rows, clusters_doc.get('clusters', {}).get(lang, {}), seed, lang)
        rows_by_lang[lang] = rows; files_summary[lang] = {'files': len(files), 'read': sum(1 for f in file_rows if 'error' not in f), 'errors': sum(1 for f in file_rows if 'error' in f),
                                                           'hours_recorded': round(sum(f.get('duration_s', 0) for f in file_rows) / 3600, 3), 'sessions_by_split': dict(Counter(session_split.values()))}
        with open(out / f'files_{lang}.jsonl', 'w') as fh:
            for f in file_rows: fh.write(json.dumps({**f, 'split': session_split.get(f['session'])}, sort_keys=True) + '\n')
    state.update(progress={'stage': 'brand inventory and character register', 'elapsed_s': int(time.time() - started)})
    inventory = brand_inventory(rows_by_lang, control.get('brand_lexicon') or [])
    register = {lang: character_register(rows) for lang, rows in rows_by_lang.items()}
    import numpy as np
    import torch
    # ---- Mimi tokens for every train/dev segment ≤ token_max_seconds (the voice lane trains on these; admission audio is never tokenised here)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    state.update(progress={'stage': 'loading the neural codec', 'elapsed_s': int(time.time() - started)})
    mimi, fe, codec_provenance = load_mimi(device)
    token_max = float(control.get('token_max_seconds', 12.0)); tokens_summary = {}
    for lang, rows in rows_by_lang.items():
        eligible = [r for r in rows if r['split'] in ('train', 'dev') and r['features']['duration_s'] <= token_max]
        codes_out, frames_total = {}, 0
        for i, r in enumerate(eligible):
            y16 = pcm_store.read(lang, r).astype(np.float32) / 32767.0
            codes = mimi_encode(mimi, [resample(y16, SR16, SR24)], device)[0].to(torch.int16)
            codes_out[r['seg_id']] = codes; frames_total += codes.shape[1]
            if i % 500 == 0: state.update(progress={'stage': f'tokenising {LANG_NAMES.get(lang, lang)} with the codec', 'segments': i, 'of': len(eligible), 'elapsed_s': int(time.time() - started)})
        torch.save(codes_out, out / f'tokens_{lang}.pt')
        tokens_summary[lang] = {'segments': len(eligible), 'frames': frames_total, 'hours': round(frames_total / MIMI_FRAME_HZ / 3600, 3), 'tokens': frames_total * MIMI_CODEBOOKS}
    state.update(progress={'stage': 'codec round-trip qualification', 'elapsed_s': int(time.time() - started)})
    codec = codec_qualification(mimi, fe, rows_by_lang, pcm_store, device, int(control.get('codec_sample_per_language', 60)), seed)
    # ---- write rows (text separate, stays on host), seals
    seals, splits = {}, {}
    for lang, rows in rows_by_lang.items():
        with open(out / f'segments_{lang}.jsonl', 'w') as fh, open(out / f'text_{lang}.jsonl', 'w') as th:
            for r in sorted(rows, key=lambda r: (r['session'], r['start'])):
                th.write(json.dumps({'seg_id': r['seg_id'], 'text': r['text']}, ensure_ascii=False) + '\n')
                fh.write(json.dumps({k: v for k, v in r.items() if k != 'text'}, sort_keys=True) + '\n')
        counts = Counter(r['split'] for r in rows); hours = defaultdict(float)
        for r in rows: hours[r['split']] += r['features']['duration_s'] / 3600
        splits[lang] = {s: {'segments': counts[s], 'hours': round(hours[s], 3)} for s in ('train', 'dev', 'admission')}
        seals[lang] = {'admission_seg_ids_sha256': _sha(json.dumps(sorted(r['seg_id'] for r in rows if r['split'] == 'admission'))), 'dev_seg_ids_sha256': _sha(json.dumps(sorted(r['seg_id'] for r in rows if r['split'] == 'dev'))), 'sealed_at': now()}
    manifest = {'protocol': 'akki-malpha-aip-db-v1', 'commission_id': control['commission_id'], 'built_at': now(), 'languages': langs, 'seed': seed, 'split_rule': 'speaker-cluster-disjoint; straddling sessions → train; admission 10% / dev 10% by cluster hash',
                'files': files_summary, 'segments': splits, 'seals': seals, 'codec_provenance': codec_provenance, 'codec_qualification': codec, 'tokens': tokens_summary, 'character_register': register,
                'brand_inventory': inventory, 'feature_columns': list(FEATURES), 'layers': ['content (transcript, sealed by sha)', 'timing (start/end, pcm offsets)', 'speaker-local label + corpus cluster id', 'condition (codec/rate/channels)', 'discoverable spectrum columns', 'codec tokens (content stream cb0, character stream cb1-7)']}
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=1, sort_keys=True))
    manifest_sha = hashlib.sha256((out / 'manifest.json').read_bytes()).hexdigest()
    return {**{k: manifest[k] for k in ('protocol', 'commission_id', 'languages', 'seed', 'split_rule', 'files', 'segments', 'seals', 'codec_provenance', 'codec_qualification', 'tokens', 'character_register', 'brand_inventory', 'feature_columns', 'layers')},
            'aip_db_dir': str(out), 'manifest_sha256': manifest_sha, 'compute': {'wall_seconds': round(time.time() - started, 1), 'gpu_seconds': round(time.time() - started, 1), 'device': device},
            'raw_media_exported': False, 'text_exported': False, 'paths_exported': False, 'training_started': False}


def aip_requalify(control, state):
    """MA-12 absent-strata correction, CPU only. The cluster-disjoint rule left the dev split too small to measure (Kamba: 2 segments) because radio
    sessions carry many voices and straddling sessions fall back to train. Admission stays sealed and untouched (seal re-verified here); whole train
    sessions are promoted to dev in seeded hash order until every language has min_dev_segments and min_dev_mention_segments. Promoted rows carry
    dev_basis='session_holdout' — presenter overlap with train is possible and is disclosed as a selection effect; it never feeds admission."""
    out = Path(control['aip_db_dir']); started = time.time(); seed = int(control['seed']); langs = list(control['languages'])
    manifest = json.loads((out / 'manifest.json').read_text())
    min_segs, min_mentions = int(control.get('min_dev_segments', 300)), int(control.get('min_dev_mention_segments', 30))
    report, seals, splits = {}, dict(manifest['seals']), dict(manifest['segments'])
    for lang in langs:
        rows = load_rows(out, lang)
        admission_seal = _sha(json.dumps(sorted(r['seg_id'] for r in rows if r['split'] == 'admission')))
        if admission_seal != manifest['seals'][lang]['admission_seg_ids_sha256']: raise ValueError(f'ADMISSION_SEAL_MISMATCH:{lang}')
        for r in rows:
            if r['split'] == 'dev' and not r.get('dev_basis'): r['dev_basis'] = 'cluster_disjoint'
        before = {'segments': sum(1 for r in rows if r['split'] == 'dev'), 'mention_segments': sum(1 for r in rows if r['split'] == 'dev' and r.get('mentions'))}
        by_session = defaultdict(list)
        for r in rows:
            if r['split'] == 'train': by_session[r['session']].append(r)
        promoted = []
        for session in sorted(by_session, key=lambda s: _split_bucket(seed, lang, 'dev-holdout:' + s)):
            dev = [r for r in rows if r['split'] == 'dev']
            if len(dev) >= min_segs and sum(1 for r in dev if r.get('mentions')) >= min_mentions: break
            if len(by_session[session]) > max(80, min_segs): continue  # a very large session stays in train; dev is assembled from ordinary ones
            for r in by_session[session]: r['split'] = 'dev'; r['dev_basis'] = 'session_holdout'
            promoted.append(session)
        with open(out / f'segments_{lang}.jsonl', 'w') as fh:
            for r in sorted(rows, key=lambda r: (r['session'], r['start'])): fh.write(json.dumps({k: v for k, v in r.items() if k != 'text'}, sort_keys=True) + '\n')
        files = [json.loads(l) for l in (out / f'files_{lang}.jsonl').read_text().splitlines() if l.strip()]
        with open(out / f'files_{lang}.jsonl', 'w') as fh:
            for f in files: fh.write(json.dumps({**f, 'split': 'dev' if f['session'] in promoted else f.get('split')}, sort_keys=True) + '\n')
        counts = Counter(r['split'] for r in rows); hours = defaultdict(float)
        for r in rows: hours[r['split']] += r['features']['duration_s'] / 3600
        splits[lang] = {s: {'segments': counts[s], 'hours': round(hours[s], 3)} for s in ('train', 'dev', 'admission')}
        splits[lang]['dev_by_basis'] = dict(Counter(r.get('dev_basis') for r in rows if r['split'] == 'dev'))
        seals[lang] = {**manifest['seals'][lang], 'dev_seg_ids_sha256': _sha(json.dumps(sorted(r['seg_id'] for r in rows if r['split'] == 'dev'))), 'dev_resealed_at': now(), 'admission_seal_unchanged': True}
        import torch
        token_keys = set(torch.load(out / f'tokens_{lang}.pt', map_location='cpu').keys())
        report[lang] = {'before': before, 'after': {'segments': counts['dev'], 'mention_segments': sum(1 for r in rows if r['split'] == 'dev' and r.get('mentions'))}, 'promoted_sessions': len(promoted),
                        'promoted_segments_without_codec_tokens': sum(1 for r in rows if r.get('dev_basis') == 'session_holdout' and r['features']['duration_s'] <= 12.0 and r['seg_id'] not in token_keys)}
    manifest.update(segments=splits, seals=seals, split_rule=manifest['split_rule'] + '; dev requalified: train sessions promoted in seeded hash order until ≥ min_dev_segments and ≥ min_dev_mention_segments (dev_basis recorded; admission untouched)',
                    requalification={'at': now(), 'min_dev_segments': min_segs, 'min_dev_mention_segments': min_mentions, 'report': report, 'authority': 'MA-12 absent-strata refusal → correction; selection effect disclosed'})
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=1, sort_keys=True))
    return {'protocol': manifest['protocol'], 'commission_id': control['commission_id'], 'languages': langs, 'seed': seed, 'segments': splits, 'seals': seals, 'requalification': manifest['requalification'], 'aip_db_dir': str(out),
            'manifest_sha256': hashlib.sha256((out / 'manifest.json').read_bytes()).hexdigest(), 'compute': {'wall_seconds': round(time.time() - started, 1), 'gpu_seconds': 0, 'device': 'cpu'},
            'raw_media_exported': False, 'text_exported': False, 'paths_exported': False, 'training_started': False}


# ----------------------------------------------------------------------------- phase: brand re-labelling under a new owner lexicon version (CPU)
def lexicon_sha(lexicon):
    return hashlib.sha256(json.dumps(lexicon, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def aip_relabel(control, state):
    """The owner's brand catalogue replaces the seed lexicon: every row's mention set is recomputed from its (unchanged) transcript. Segment ids,
    splits and the admission seal are untouched and re-verified; what changes is the measured quantity. Common-word brands are flagged from
    corpus frequency, never silently dropped — the owner decides."""
    out = Path(control['aip_db_dir']); started = time.time(); langs = list(control['languages']); lexicon = control['brand_lexicon']
    manifest = json.loads((out / 'manifest.json').read_text())
    sha = lexicon_sha(lexicon); report = {}; ambiguous = {}
    for lang in langs:
        rows = load_rows(out, lang, with_text=True)
        if _sha(json.dumps(sorted(r['seg_id'] for r in rows if r['split'] == 'admission'))) != manifest['seals'][lang]['admission_seg_ids_sha256']: raise ValueError(f'ADMISSION_SEAL_MISMATCH:{lang}')
        before = sum(1 for r in rows if r.get('mentions'))
        inventory = brand_inventory({lang: rows}, lexicon)[lang]
        _write_rows_atomic(out / f'segments_{lang}.jsonl', rows)
        internet = load_rows(out, lang, with_text=True, dataset='internet')
        if internet:
            brand_inventory({lang: internet}, lexicon); _write_rows_atomic(out / f'segments_internet_{lang}.jsonl', internet)
        total = len(rows) or 1
        ambiguous[lang] = sorted([{'brand': b, 'segments_per_1000': round(1000 * sum(c.values()) / total, 2)} for b, c in inventory.items() if sum(c.values()) / total > 0.01], key=lambda d: -d['segments_per_1000'])
        report[lang] = {'segments': len(rows), 'mention_segments_before': before, 'mention_segments_after': sum(1 for r in rows if r.get('mentions')),
                        'by_split': {s: sum(1 for r in rows if r['split'] == s and r.get('mentions')) for s in ('train', 'dev', 'admission')}, 'brands_heard': len(inventory), 'internet_rows_relabelled': len(internet)}
        manifest.setdefault('brand_inventory', {})[lang] = inventory
        state.update(progress={'stage': f'relabelled {LANG_NAMES.get(lang, lang)}', 'elapsed_s': int(time.time() - started)})
    manifest.update(brand_lexicon={'version': control.get('brand_lexicon_version'), 'lexicon_sha256': sha, 'brands': len(lexicon), 'relabelled_at': now(), 'frequent_brands_flagged': ambiguous},
                    seals={l: {**manifest['seals'][l], 'admission_seal_unchanged': True} for l in manifest['seals']})
    tmp = out / 'manifest.json.tmp'; tmp.write_text(json.dumps(manifest, indent=1, sort_keys=True)); os.replace(tmp, out / 'manifest.json')
    return {'protocol': manifest['protocol'], 'commission_id': control['commission_id'], 'languages': langs, 'lexicon_sha256': sha, 'lexicon_version': control.get('brand_lexicon_version'), 'brands': len(lexicon), 'report': report,
            'brand_inventory': manifest['brand_inventory'],
            'frequent_brands_flagged': ambiguous, 'seals': manifest['seals'], 'aip_db_dir': str(out), 'manifest_sha256': hashlib.sha256((out / 'manifest.json').read_bytes()).hexdigest(),
            'compute': {'wall_seconds': round(time.time() - started, 1), 'gpu_seconds': 0, 'device': 'cpu'}, 'raw_media_exported': False, 'text_exported': False, 'paths_exported': False, 'training_started': False}


# ----------------------------------------------------------------------------- phase: public internet corpus (owner order 2026-10-04: "You can also train from the internet data")
LICENCE_ALLOWLIST = ('cc-by-4.0', 'cc0-1.0', 'cc-by-sa-4.0', 'cc-by-3.0', 'cc-by-sa-3.0', 'apache-2.0', 'mit', 'odc-by', 'cdla-permissive-2.0')
TEXT_COLUMNS = ('transcription', 'transcript', 'transcripts', 'sentence', 'text', 'raw_transcription', 'normalized_text')


def _hf_qualify(repo, allowlist):
    """Rights check before any bytes: declared licence must be on the allowlist and the dataset must be readable with the host's credentials."""
    from huggingface_hub import HfApi
    try:
        info = HfApi().dataset_info(repo)
    except Exception as exc:
        return None, f'not_reachable:{type(exc).__name__}'
    licence = ((info.card_data or {}).get('license') if info.card_data else None)
    licence = licence[0] if isinstance(licence, list) and licence else licence
    if not licence or str(licence).lower() not in allowlist: return info, f'licence_not_admitted:{licence or "undeclared"}'
    if getattr(info, 'gated', False) and not os.environ.get('HF_TOKEN'): return info, 'gated_no_token'
    return info, None


def _decode_bytes(data, sr):
    import numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'pipe:0', '-f', 'f32le', '-ac', '1', '-ar', str(sr), '-'], input=data, capture_output=True, timeout=120, check=False).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def internet_corpus(control, state):
    """Public speech datasets become a second, separately provenance-tagged dataset of the audio database (`segments_internet_<lang>`): train
    only, never dev or admission, never mixed into the radio character register. Licence and access are checked before download; a dataset
    that fails is recorded as refused, not skipped silently. Hours per dataset are capped by the recipe, not by the owner."""
    import numpy as np
    from datasets import Audio, load_dataset
    out = Path(control['aip_db_dir']); started = time.time(); lexicon = control.get('brand_lexicon') or []
    manifest = json.loads((out / 'manifest.json').read_text()); registry = manifest.setdefault('internet_corpus', {})
    allow = tuple(control.get('licence_allowlist') or LICENCE_ALLOWLIST); max_hours = float(control.get('max_hours_per_dataset', 60)); max_s = float(control.get('max_segment_seconds', 30.0))
    results = []
    for spec in control['datasets']:
        key = f"{spec['repo']}:{spec.get('config') or 'default'}"; lang = spec['language']
        if key in registry and registry[key].get('status') == 'ingested': results.append({**registry[key], 'reused': True}); continue
        state.update(progress={'stage': f'qualifying {key}', 'elapsed_s': int(time.time() - started)})
        info, refusal = _hf_qualify(spec['repo'], allow)
        rec = {'repo': spec['repo'], 'config': spec.get('config'), 'language': lang, 'split': spec.get('split', 'train'), 'licence': ((info.card_data or {}).get('license') if info and info.card_data else None), 'checked_at': now()}
        if refusal:
            rec.update(status='refused', reason=refusal); registry[key] = rec; results.append(rec); continue
        try:
            ds = load_dataset(spec['repo'], spec.get('config'), split=spec.get('split', 'train'), streaming=True)
            audio_col = spec.get('audio_column') or next(k for k, v in ds.features.items() if type(v).__name__ == 'Audio')
            text_col = spec.get('text_column') or next(k for k in TEXT_COLUMNS if k in ds.features)
            ds = ds.cast_column(audio_col, Audio(decode=False))
        except Exception as exc:
            rec.update(status='refused', reason=f'not_loadable:{type(exc).__name__}:{str(exc)[:160]}'); registry[key] = rec; results.append(rec); continue
        existing = load_rows(out, lang, with_text=True, dataset='internet'); rows = []; texts = {}
        pcm_name = f'pcm16k_internet_{lang}.bin'; pcm_path = out / pcm_name
        hours = 0.0; skipped = Counter()
        with open(pcm_path, 'ab') as pcm:
            for i, item in enumerate(ds):
                if hours >= max_hours: break
                text = ' '.join(str(item.get(text_col) or '').split())
                blob = (item.get(audio_col) or {}).get('bytes')
                if not text or not blob: skipped['no_text_or_audio'] += 1; continue
                try: y = _decode_bytes(blob, SR16)
                except Exception: skipped['decode_error'] += 1; continue
                if len(y) < int(0.5 * SR16) or len(y) > int(max_s * SR16) or float(np.abs(y).max()) < 1e-4: skipped['duration_or_silence'] += 1; continue
                feats = spectrum_features(y, SR16, len(text))
                if not feats: skipped['no_features'] += 1; continue
                block = (np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes(); offset = pcm.tell(); pcm.write(block)
                speaker = str(item.get(spec.get('speaker_column') or 'speaker_name') or item.get('speaker_id') or 'unknown')[:40]
                seg_id = _sha(f'{key}:{i}')[:16]
                rows.append({'seg_id': seg_id, 'ref': _sha(key)[:16], 'session': f'internet:{key}:{speaker}', 'file': key, 'start': 0.0, 'end': feats['duration_s'], 'speaker': speaker, 'split': 'train', 'dataset': 'internet',
                             'source': {'repo': spec['repo'], 'config': spec.get('config'), 'licence': rec['licence'], 'row_index': i}, 'condition': 'read_speech/16000Hz/1ch', 'pcm_file': pcm_name, 'pcm_offset': offset, 'pcm_bytes': len(block),
                             'chars': len(text), 'words': len(text.split()), 'text_sha256': _sha(text), 'features': feats, 'text': text})
                texts[seg_id] = text; hours += feats['duration_s'] / 3600
                if len(rows) % 200 == 0: state.update(progress={'stage': f'reading {key}', 'rows': len(rows), 'hours': round(hours, 2), 'of_hours': max_hours, 'elapsed_s': int(time.time() - started)})
        brand_inventory({lang: rows}, lexicon)
        merged = existing + rows
        _write_rows_atomic(out / f'segments_internet_{lang}.jsonl', merged, key=lambda r: (r['session'], r['seg_id']))
        with open(out / f'text_internet_{lang}.jsonl', 'a') as th:
            for r in rows: th.write(json.dumps({'seg_id': r['seg_id'], 'text': r['text']}, ensure_ascii=False) + '\n')
        rec.update(status='ingested', rows=len(rows), hours=round(hours, 3), skipped=dict(skipped), mention_rows=sum(1 for r in rows if r.get('mentions')), text_column=text_col, audio_column=audio_col)
        registry[key] = rec; results.append(rec)
    manifest['internet_corpus'] = registry
    tmp = out / 'manifest.json.tmp'; tmp.write_text(json.dumps(manifest, indent=1, sort_keys=True)); os.replace(tmp, out / 'manifest.json')
    totals = {l: {'rows': sum(r.get('rows', 0) for r in results if r['language'] == l and r['status'] == 'ingested'), 'hours': round(sum(r.get('hours', 0) for r in results if r['language'] == l and r['status'] == 'ingested'), 3)} for l in control['languages']}
    return {'commission_id': control['commission_id'], 'datasets': results, 'totals': totals, 'aip_db_dir': str(out), 'manifest_sha256': hashlib.sha256((out / 'manifest.json').read_bytes()).hexdigest(),
            'compute': {'wall_seconds': round(time.time() - started, 1), 'gpu_seconds': 0, 'device': 'cpu'}, 'raw_media_exported': False, 'text_exported': False, 'paths_exported': False, 'training_started': False, 'sealed_admission_read': False}


# ----------------------------------------------------------------------------- shared training utilities
def gpu_lock(control):
    import fcntl
    lock = open(Path(control['root']) / f"gpu_{control['gpu_index']}.lock", 'w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    import torch
    torch.backends.cuda.matmul.allow_tf32 = True; torch.backends.cudnn.allow_tf32 = True
    if not torch.cuda.is_available(): raise ValueError('NO_GPU_VISIBLE')
    return lock


def lr_at(step, total, peak, warmup):
    if step < warmup: return peak * (step + 1) / warmup
    p = (step - warmup) / max(1, total - warmup)
    return peak * (0.05 + 0.95 * 0.5 * (1 + math.cos(math.pi * min(1.0, p))))


def wer_cer(refs, hyps):
    import jiwer
    refs = [normalise_text(r) or '<empty>' for r in refs]; hyps = [normalise_text(h) for h in hyps]
    return {'wer': round(float(jiwer.wer(refs, hyps)), 4), 'cer': round(float(jiwer.cer(refs, hyps)), 4), 'n': len(refs)}


def _levenshtein_leq1(a, b):
    if abs(len(a) - len(b)) > 1: return False
    i = j = edits = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]: i += 1; j += 1; continue
        edits += 1
        if edits > 1: return False
        if len(a) > len(b): i += 1
        elif len(a) < len(b): j += 1
        else: i += 1; j += 1
    return edits + (len(a) - i) + (len(b) - j) <= 1


def detect_mentions(text, lexicon):
    """Alias match on normalised text; one edit tolerated for aliases of six or more characters (radio ASR variants), never for short ones."""
    text = normalise_text(text); words = text.split(); hits = set()
    for b in lexicon:
        aliases = [normalise_text(a) for a in [b['brand']] + b.get('aliases', [])]
        for alias in aliases:
            if not alias: continue
            if re.search(r'(?<!\w)' + re.escape(alias) + r'(?!\w)', text): hits.add(b['brand']); break
            if len(alias) >= 6 and ' ' not in alias and any(_levenshtein_leq1(alias, w) for w in words): hits.add(b['brand']); break
    return sorted(hits)


def wilson(k, n, z=1.96):
    if not n: return None
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [round((c - h) / d, 4), round((c + h) / d, 4)]


def mention_metrics(rows, hyps, lexicon):
    """Per-language precision AND recall at the segment×brand level with 95% Wilson intervals (small n is visible, never averaged away),
    false positives per hour, abstention and timing tolerance recorded separately."""
    out = {}
    for lang in sorted({r['language'] for r in rows}):
        tp = fp = fn = 0; hours = 0.0; positives = 0; per_brand = defaultdict(lambda: Counter())
        for r, h in zip(rows, hyps):
            if r['language'] != lang: continue
            truth = set(r.get('mentions') or []); pred = set(detect_mentions(h, lexicon)) if h is not None else set()
            hours += r['features']['duration_s'] / 3600; positives += bool(truth)
            for b in truth & pred: tp += 1; per_brand[b]['tp'] += 1
            for b in pred - truth: fp += 1; per_brand[b]['fp'] += 1
            for b in truth - pred: fn += 1; per_brand[b]['fn'] += 1
        precision = tp / (tp + fp) if tp + fp else None; recall = tp / (tp + fn) if tp + fn else None
        f1 = 2 * precision * recall / (precision + recall) if precision and recall else (0.0 if (tp + fp and tp + fn) else None)
        out[lang] = {'segments': sum(1 for r in rows if r['language'] == lang), 'segments_with_mentions': positives, 'tp': tp, 'fp': fp, 'fn': fn,
                     'precision': round(precision, 4) if precision is not None else None, 'recall': round(recall, 4) if recall is not None else None, 'f1': round(f1, 4) if f1 is not None else None,
                     'precision_ci95': wilson(tp, tp + fp), 'recall_ci95': wilson(tp, tp + fn),
                     'false_positives_per_hour': round(fp / hours, 3) if hours else None, 'hours_evaluated': round(hours, 3), 'timestamp_tolerance': 'segment boundaries (mention attributed to its transcript segment)',
                     'abstained_segments': sum(1 for r, h in zip(rows, hyps) if r['language'] == lang and h is None), 'per_brand': {b: dict(c) for b, c in per_brand.items()}}
    return out


# ----------------------------------------------------------------------------- phase: listener (ASR + brand mentions) training
def _whisper_tokens(tokenizer, langs):
    ids = {'sot': tokenizer.convert_tokens_to_ids('<|startoftranscript|>'), 'transcribe': tokenizer.convert_tokens_to_ids('<|transcribe|>'),
           'notimestamps': tokenizer.convert_tokens_to_ids('<|notimestamps|>'), 'eot': tokenizer.eos_token_id, 'prev': tokenizer.convert_tokens_to_ids('<|startofprev|>')}
    ids['lang'] = {lang: tokenizer.convert_tokens_to_ids('<|sw|>' if lang == 'swa' else f'<|{lang}|>') for lang in langs}
    return ids


BIAS_PROMPT_MAX_TOKENS = 200  # Whisper's previous-text window is 224 tokens; the brand list that biases decoding must fit inside it


def bias_prompt_ids(tokenizer, ids, brands):
    """Contextual biasing through Whisper's own previous-text channel: the brand names a listener should expect are placed after <|startofprev|>, so
    decoding is pulled toward those spellings. Nothing is forced — a brand that is not heard is not written."""
    if not brands: return []
    return [ids['prev']] + tokenizer(' ' + ', '.join(brands), add_special_tokens=False).input_ids[:BIAS_PROMPT_MAX_TOKENS]


def bias_terms_by_language(train_rows, lexicon, per_language):
    """The brands heard most in each language's training split, in frequency order: the decode-time expectation list (recorded in the artefact)."""
    out = {}
    for lang in sorted({r['language'] for r in train_rows}):
        counts = Counter(b for r in train_rows if r['language'] == lang for b in (r.get('mentions') or []))
        out[lang] = [b for b, _ in counts.most_common(int(per_language))]
    return out


def _prepare_whisper(base, langs, device):
    import torch
    from transformers import WhisperForConditionalGeneration, WhisperProcessor
    processor = WhisperProcessor.from_pretrained(base)
    model = WhisperForConditionalGeneration.from_pretrained(base, torch_dtype=torch.float32)
    tok = processor.tokenizer
    new = [f'<|{l}|>' for l in langs if l != 'swa' and tok.convert_tokens_to_ids(f'<|{l}|>') in (tok.unk_token_id, None)]
    if new:
        tok.add_tokens(new, special_tokens=True)  # transformers 5 removed tokenizer.additional_special_tokens; add_tokens is stable across versions
        model.resize_token_embeddings(len(tok))
        sw = model.get_input_embeddings().weight.data[tok.convert_tokens_to_ids('<|sw|>')].clone()
        for t in new: model.get_input_embeddings().weight.data[tok.convert_tokens_to_ids(t)] = sw
    model.config.forced_decoder_ids = None; model.generation_config.forced_decoder_ids = None
    return processor, model.to(device), _whisper_tokens(tok, langs)


def _whisper_batch(processor, ids, pcm_store, rows, device, max_label=256, prompts=None):
    """prompts: optional per-row brand lists for contextual-bias training; prompt tokens (and the start token after them) are excluded from the loss."""
    import numpy as np
    import torch
    audio = [pcm_store.read(r['language'], r).astype(np.float32) / 32767.0 for r in rows]
    feats = processor.feature_extractor(audio, sampling_rate=SR16, return_tensors='pt').input_features.to(device)
    labels, masked = [], []
    for i, r in enumerate(rows):
        prefix = bias_prompt_ids(processor.tokenizer, ids, prompts[i]) if prompts and prompts[i] else []
        text_ids = processor.tokenizer(r['text'], add_special_tokens=False).input_ids[:max_label - 5 - len(prefix)]
        labels.append(prefix + [ids['sot'], ids['lang'][r['language']], ids['transcribe'], ids['notimestamps']] + text_ids + [ids['eot']]); masked.append(len(prefix))
    width = max(len(l) for l in labels)
    dec_in = torch.full((len(rows), width - 1), ids['eot'], dtype=torch.long); target = torch.full((len(rows), width - 1), -100, dtype=torch.long)
    for i, l in enumerate(labels):
        dec_in[i, :len(l) - 1] = torch.tensor(l[:-1]); target[i, :len(l) - 1] = torch.tensor(l[1:])
        if masked[i]: target[i, :masked[i]] = -100  # the model is not trained to produce the prompt or the start token after it
    return feats, dec_in.to(device), target.to(device)


def whisper_greedy(model, processor, ids, feats, langs_of_rows, max_new=180, prompt=None):
    """Own greedy loop with cached encoder output: language forced per segment, no dependence on generate() language tables. `prompt` is one brand list
    shared by the batch (contextual bias through <|startofprev|>)."""
    import torch
    from transformers.modeling_outputs import BaseModelOutput
    with torch.no_grad(), torch.autocast('cuda', dtype=torch.bfloat16):
        enc = BaseModelOutput(last_hidden_state=model.model.encoder(feats).last_hidden_state)
    B = feats.shape[0]; prefix = bias_prompt_ids(processor.tokenizer, ids, prompt) if prompt else []
    seq = torch.tensor([prefix + [ids['sot'], ids['lang'][l], ids['transcribe'], ids['notimestamps']] for l in langs_of_rows], device=feats.device); head = len(prefix) + 4
    done = torch.zeros(B, dtype=torch.bool, device=feats.device); past = None
    for _ in range(max_new):
        with torch.no_grad(), torch.autocast('cuda', dtype=torch.bfloat16):
            out = model(encoder_outputs=enc, decoder_input_ids=seq if past is None else seq[:, -1:], past_key_values=past, use_cache=True)
        past = out.past_key_values
        nxt = out.logits[:, -1].argmax(-1); nxt = torch.where(done, torch.full_like(nxt, ids['eot']), nxt)
        seq = torch.cat([seq, nxt[:, None]], 1); done |= nxt == ids['eot']
        if bool(done.all()): break
    hyps = []
    for row in seq[:, head:].tolist():
        cut = row.index(ids['eot']) if ids['eot'] in row else len(row)
        hyps.append(processor.tokenizer.decode(row[:cut], skip_special_tokens=True).strip())
    return hyps


def _sample_per_language(rows, per_lang, seed):
    """Dev sample stratified on the measured quantity: every mention-bearing segment (up to half the budget) plus seeded negatives — a plain random draw from a
    requalified dev split would carry two or three mentions and make precision/recall noise."""
    rng = random.Random(seed); out = []
    for lang in sorted({r['language'] for r in rows}):
        group = [r for r in rows if r['language'] == lang]
        positives = [r for r in group if r.get('mentions')]; negatives = [r for r in group if not r.get('mentions')]
        keep = positives if len(positives) <= per_lang // 2 else rng.sample(positives, per_lang // 2)
        out.extend(keep); out.extend(rng.sample(negatives, min(max(per_lang - len(keep), 0), len(negatives))))
    return out


def evaluate_listener(model, processor, ids, pcm_store, rows, lexicon, device, batch=48, bias_terms=None):
    """bias_terms: per-language brand lists shared by every batch of that language (decode-time expectation list); None = plain decoding."""
    hyps_by_id = {}; started = time.time(); audio_s = 0.0
    for lang in sorted({r['language'] for r in rows}):
        group = sorted([r for r in rows if r['language'] == lang], key=lambda r: r['features']['duration_s'])
        for i in range(0, len(group), batch):
            chunk = group[i:i + batch]
            feats, _, _ = _whisper_batch(processor, ids, pcm_store, chunk, device)
            for r, h in zip(chunk, whisper_greedy(model, processor, ids, feats, [r['language'] for r in chunk], prompt=(bias_terms or {}).get(lang))): hyps_by_id[r['seg_id']] = h
            audio_s += sum(r['features']['duration_s'] for r in chunk)
    rows = sorted(rows, key=lambda r: (r['language'], r['features']['duration_s'])); hyps = [hyps_by_id[r['seg_id']] for r in rows]
    per_lang = {}
    for lang in sorted({r['language'] for r in rows}):
        pairs = [(r['text'], h) for r, h in zip(rows, hyps) if r['language'] == lang]
        per_lang[lang] = wer_cer([p[0] for p in pairs], [p[1] for p in pairs])
    return {'words': per_lang, 'mentions': mention_metrics(rows, hyps, lexicon), 'latency': {'real_time_factor': round((time.time() - started) / max(1e-6, audio_s), 4), 'audio_seconds': round(audio_s, 1), 'wall_seconds': round(time.time() - started, 1)},
            'contextual_bias': {l: len(v) for l, v in (bias_terms or {}).items()} or None,
            'samples': [{'language': r['language'], 'ref_chars': len(r['text']), 'hyp_chars': len(h), 'mentions_truth': r.get('mentions') or [], 'mentions_hyp': detect_mentions(h, lexicon)} for r, h in list(zip(rows, hyps))[:12]]}


def _listener_score(ev):
    """Artefact choice follows the admission contract: the worst language's mention F1 first (no averaging across languages), lower mean WER breaks ties."""
    import numpy as np
    f1s = [(m.get('f1') if m.get('f1') is not None else 0.0) for m in ev['mentions'].values()]
    return (round(min(f1s), 4) if f1s else 0.0, -round(float(np.mean([v['wer'] for v in ev['words'].values()])), 4))


def _save_ckpt(path, model, optimizer, step, extra):
    import torch
    tmp = Path(str(path) + '.tmp'); torch.save({'model': model.state_dict(), 'optimizer': optimizer.state_dict(), 'step': step, **extra}, tmp); os.replace(tmp, path)


def listener_train(control, state):
    import numpy as np
    import torch
    lock = gpu_lock(control); device = 'cuda'; started = time.time()
    aip = Path(control['aip_db_dir']); langs = list(control['languages']); recipe = dict(control['recipe']); lexicon = control.get('brand_lexicon') or []
    job_dir = Path(control['job_dir']); ckpt_dir = job_dir / 'checkpoints'; ckpt_dir.mkdir(exist_ok=True)
    pcm_store = PcmStore(aip)
    rows = []
    for lang in langs:
        for r in load_rows(aip, lang, with_text=True): r['language'] = lang; rows.append(r)
    max_s = float(recipe.get('max_segment_seconds', 30.0))
    train = [r for r in rows if r['split'] == 'train' and r['features']['duration_s'] <= max_s and r['text']]
    internet = []
    if recipe.get('include_internet_corpus'):
        for lang in langs:
            for r in load_rows(aip, lang, with_text=True, dataset='internet'):
                if r['features']['duration_s'] <= max_s and r['text']: r['language'] = lang; internet.append(r)
        train = train + internet
    dev = _sample_per_language([r for r in rows if r['split'] == 'dev' and r['features']['duration_s'] <= max_s and r['text']], int(recipe.get('dev_per_language', 400)), int(control['seed']))
    state.stage('data', {'train_segments': len(train), 'dev_segments': len(dev), 'train_hours': round(sum(r['features']['duration_s'] for r in train) / 3600, 2), 'admission_read': False, 'lexicon_sha256': lexicon_sha(lexicon), 'brands': len(lexicon),
                         'internet_corpus': {'segments': len(internet), 'hours': round(sum(r['features']['duration_s'] for r in internet) / 3600, 2), 'per_language': {l: sum(1 for r in internet if r['language'] == l) for l in langs}} if internet else None})
    processor, model, ids = _prepare_whisper(recipe['base'], langs, device)
    if recipe.get('init_from'):
        sd = torch.load(Path(recipe['init_from']) / 'model.pt', map_location='cpu'); model.load_state_dict(sd['model'] if 'model' in sd else sd)
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(recipe['lr']), weight_decay=0.01, betas=(0.9, 0.98))
    batch, accum, max_steps = int(recipe['batch_size']), int(recipe.get('grad_accum', 1)), int(recipe['max_steps'])
    eval_every, ckpt_every, warmup = int(recipe.get('eval_every', 1000)), int(recipe.get('checkpoint_every', 500)), int(recipe.get('warmup_steps', 300))
    step, history, best = 0, [], None
    latest = ckpt_dir / 'latest.pt'
    if control.get('resume_from') and Path(control['resume_from']).exists():
        ck = torch.load(control['resume_from'], map_location='cpu'); model.load_state_dict(ck['model']); optimizer.load_state_dict(ck['optimizer']); step = int(ck['step']); history = ck.get('history', [])
        state.event(f'resumed from checkpoint at step {step}')
    rng = random.Random(int(control['seed']) + step)
    order = sorted(train, key=lambda r: r['features']['duration_s'])
    buckets = [order[i:i + batch] for i in range(0, len(order), batch)]
    bias_on = bool(recipe.get('contextual_bias', False)); bias_prob = float(recipe.get('bias_prob', 0.5)); distractors = int(recipe.get('bias_distractors', 6))
    bias_terms = bias_terms_by_language(train, lexicon, int(recipe.get('bias_terms_per_language', 40))) if bias_on else None
    brands_by_lang = {l: sorted({b for r in train if r['language'] == l for b in (r.get('mentions') or [])}) for l in langs}
    if bias_on: state.stage('contextual_bias', {'decode_expectation_terms': {l: len(v) for l, v in bias_terms.items()}, 'train_prompt_probability': bias_prob, 'distractors_per_prompt': distractors, 'prompt_channel': '<|startofprev|> brand list'})

    def train_prompts(rows_):
        """Half the segments see an expectation list holding their true brands among distractors (so the model learns to use the list, not to copy it); the rest see none."""
        out = []
        for r in rows_:
            if not bias_on or rng.random() >= bias_prob: out.append(None); continue
            pool = [b for b in brands_by_lang.get(r['language']) or [] if b not in (r.get('mentions') or [])]
            terms = list(r.get('mentions') or []) + rng.sample(pool, min(distractors, len(pool))); rng.shuffle(terms); out.append(terms or None)
        return out
    model.train(); losses = []
    while step < max_steps:
        rng.shuffle(buckets)
        for b in buckets:
            if step >= max_steps: break
            feats, dec_in, target = _whisper_batch(processor, ids, pcm_store, b, device, prompts=train_prompts(b))
            with torch.autocast('cuda', dtype=torch.bfloat16):
                logits = model(input_features=feats, decoder_input_ids=dec_in).logits
            loss = torch.nn.functional.cross_entropy(logits.float().view(-1, logits.shape[-1]), target.view(-1), ignore_index=-100) / accum
            loss.backward(); losses.append(float(loss) * accum)
            if len(losses) % accum: continue
            for g in optimizer.param_groups: g['lr'] = lr_at(step, max_steps, float(recipe['lr']), warmup)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step(); optimizer.zero_grad(set_to_none=True); step += 1
            if step % 25 == 0:
                state.update(progress={'stage': 'training', 'step': step, 'of': max_steps, 'loss': round(float(np.mean(losses[-100:])), 4), 'lr': optimizer.param_groups[0]['lr'], 'elapsed_s': int(time.time() - started),
                                       'gpu_peak_gb': round(torch.cuda.max_memory_allocated() / 2 ** 30, 2), 'last_checkpoint_step': (step // ckpt_every) * ckpt_every, 'next_checkpoint_step': (step // ckpt_every + 1) * ckpt_every})
            if step % ckpt_every == 0:
                _save_ckpt(latest, model, optimizer, step, {'history': history}); state.event(f'checkpoint at step {step}')
            if step % eval_every == 0 or step == max_steps:
                model.eval(); ev = evaluate_listener(model, processor, ids, pcm_store, dev, lexicon, device, bias_terms=bias_terms); model.train()
                ev['step'] = step; ev['train_loss'] = round(float(np.mean(losses[-200:])), 4); ev['at'] = now(); history.append(ev)
                mean_wer = float(np.mean([v['wer'] for v in ev['words'].values()])); score = _listener_score(ev)
                state.stage(f'dev_eval_step_{step}', {'mean_wer': round(mean_wer, 4), 'worst_language_f1': score[0], 'words': ev['words'], 'mentions': {l: {k: m[k] for k in ('precision', 'recall', 'f1')} for l, m in ev['mentions'].items()}})
                if best is None or score > best['score']:
                    best = {'step': step, 'mean_wer': round(mean_wer, 4), 'worst_language_f1': score[0], 'score': score, 'basis': 'worst-language mention F1, then mean WER'}; _save_ckpt(ckpt_dir / 'best.pt', model, optimizer, step, {'history': history})
    art = job_dir / 'artefact'; art.mkdir(exist_ok=True)
    src = ckpt_dir / 'best.pt' if (ckpt_dir / 'best.pt').exists() else latest
    if not src.exists(): _save_ckpt(latest, model, optimizer, step, {'history': history}); src = latest
    ck = torch.load(src, map_location='cpu'); torch.save({'model': ck['model'], 'base': recipe['base'], 'languages': langs, 'step': ck['step'], 'added_tokens': [f'<|{l}|>' for l in langs if l != 'swa'], 'bias_terms': bias_terms}, art / 'model.pt')
    processor.save_pretrained(art / 'processor')
    sha = hashlib.sha256((art / 'model.pt').read_bytes()).hexdigest()
    final = next((h for h in history if best and h['step'] == best['step']), history[-1] if history else None)  # the reported dev reading is the artefact's own
    lock.close()
    return {'commission_id': control['commission_id'], 'iteration': control['iteration'], 'recipe': recipe, 'languages': langs, 'data': state.doc['stages']['data'], 'steps': step,
            'dev': final, 'history': [{k: h[k] for k in ('step', 'train_loss', 'words', 'mentions', 'latency', 'at')} for h in history], 'best': {k: v for k, v in (best or {}).items() if k != 'score'} or None,
            'artefact': {'path': str(art / 'model.pt'), 'sha256': sha, 'bytes': (art / 'model.pt').stat().st_size, 'best_step': int(ck['step']), 'contextual_bias_terms': {l: len(v) for l, v in (bias_terms or {}).items()} or None},
            'compute': {'wall_seconds': round(time.time() - started, 1), 'gpu_seconds': round(time.time() - started, 1), 'gpu_hours': round((time.time() - started) / 3600, 4), 'gpu_peak_gb': round(torch.cuda.max_memory_allocated() / 2 ** 30, 2), 'device': torch.cuda.get_device_name(0)},
            'sealed_admission_read': False, 'training_started': True, 'raw_media_exported': False}


# ----------------------------------------------------------------------------- phase: independent admission evaluation on the sealed split
def evaluate_admission(control, state):
    import torch
    lock = gpu_lock(control); device = 'cuda'; started = time.time()
    aip = Path(control['aip_db_dir']); langs = list(control['languages']); lexicon = control.get('brand_lexicon') or []
    manifest = json.loads((aip / 'manifest.json').read_text())
    pcm_store = PcmStore(aip); rows = []
    for lang in langs:
        for r in load_rows(aip, lang, with_text=True): r['language'] = lang; rows.append(r)
    admission = [r for r in rows if r['split'] == 'admission' and r['text'] and r['features']['duration_s'] <= 30.0]
    for lang in langs:
        seal = _sha(json.dumps(sorted(r['seg_id'] for r in rows if r['language'] == lang and r['split'] == 'admission')))
        if seal != manifest['seals'][lang]['admission_seg_ids_sha256']: raise ValueError(f'ADMISSION_SEAL_MISMATCH:{lang}')
    art = torch.load(Path(control['artefact_path']), map_location='cpu')
    if hashlib.sha256(Path(control['artefact_path']).read_bytes()).hexdigest() != control['artefact_sha256']: raise ValueError('ARTEFACT_SHA_MISMATCH')
    processor, model, ids = _prepare_whisper(art['base'], langs, device); model.load_state_dict(art['model']); model.eval()
    state.stage('data', {'admission_segments': len(admission), 'seals_verified': True, 'contextual_bias_terms': {l: len(v) for l, v in (art.get('bias_terms') or {}).items()} or None})
    ev = evaluate_listener(model, processor, ids, pcm_store, admission, lexicon, device, bias_terms=art.get('bias_terms'))
    target = float(control.get('admission_target', 0.9)); verdict = {}
    for lang in langs:
        m, w = ev['mentions'].get(lang) or {}, ev['words'].get(lang) or {}
        ok = m.get('precision') is not None and m.get('recall') is not None and m['precision'] >= target and m['recall'] >= target
        verdict[lang] = {'mention_precision': m.get('precision'), 'mention_recall': m.get('recall'), 'mention_f1': m.get('f1'), 'precision_ci95': m.get('precision_ci95'), 'recall_ci95': m.get('recall_ci95'), 'wer': w.get('wer'), 'cer': w.get('cer'), 'segments_with_mentions': m.get('segments_with_mentions'),
                         'meets_target': bool(ok), 'target': target, 'measured_on': 'sealed admission split, speaker-cluster-disjoint from training'}
    lock.close()
    return {'commission_id': control['commission_id'], 'iteration': control['iteration'], 'artefact_sha256': control['artefact_sha256'], 'languages': langs, 'evaluation': ev, 'verdict': verdict, 'lexicon_sha256': lexicon_sha(lexicon), 'brands': len(lexicon),
            'admitted_all_languages': all(v['meets_target'] for v in verdict.values()), 'evaluation_exposure': 'one read of the sealed split for this artefact; recorded by the control plane',
            'compute': {'wall_seconds': round(time.time() - started, 1), 'gpu_seconds': round(time.time() - started, 1), 'gpu_hours': round((time.time() - started) / 3600, 4)}, 'sealed_admission_read': True, 'raw_media_exported': False}
