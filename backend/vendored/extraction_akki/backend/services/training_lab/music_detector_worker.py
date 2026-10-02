"""Music detector trained on the GPU host. Labelled recordings are the owner's own library (music) and the public-domain reference
speech, shipped to the host and verified by digest; weak windows come from the staged corpus cue readings and are used for training only.
File-disjoint k-fold out-of-fold evaluation at file and window level, Wilson intervals, then one final fit on everything.
No media, transcript or path leaves the host; the receipt carries aggregates and the artefact digest."""
import hashlib
import json
import math
import random
import subprocess
import time
from pathlib import Path

SR = 16000
WINDOW_S = 2.0
N_FFT, HOP, N_MELS = 400, 160, 64
AUDIO = {'.wav', '.flac', '.mp3', '.ogg', '.m4a'}


def _sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(chunk), b''):
            h.update(block)
    return h.hexdigest()


def _decode(path, max_seconds):
    import numpy as np
    cmd = ['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-t', str(max_seconds), '-']
    raw = subprocess.run(cmd, capture_output=True, timeout=600, check=False).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def _windows(samples, cap, seed):
    import numpy as np
    win = int(WINDOW_S * SR)
    starts = list(range(0, len(samples) - win + 1, win))
    if not starts:
        return np.zeros((0, win), dtype=np.float32)
    if cap and len(starts) > cap:
        rng = random.Random(seed); starts = sorted(rng.sample(starts, cap))
    out = np.stack([samples[s:s + win] for s in starts])
    keep = np.sqrt((out ** 2).mean(1)) > 1e-4  # drop digital silence; silence is neither class
    return out[keep]


def _mel_filters(device):
    import numpy as np
    import torch
    def hz_to_mel(f): return 2595.0 * np.log10(1.0 + f / 700.0)
    def mel_to_hz(m): return 700.0 * (10.0 ** (m / 2595.0) - 1.0)
    mels = np.linspace(hz_to_mel(0.0), hz_to_mel(SR / 2), N_MELS + 2)
    hz = mel_to_hz(mels); bins = np.floor((N_FFT + 1) * hz / SR).astype(int)
    fb = np.zeros((N_MELS, N_FFT // 2 + 1), dtype=np.float32)
    for m in range(1, N_MELS + 1):
        lo, c, hi = bins[m - 1], bins[m], bins[m + 1]
        for k in range(lo, c): fb[m - 1, k] = (k - lo) / max(1, c - lo)
        for k in range(c, hi): fb[m - 1, k] = (hi - k) / max(1, hi - c)
    return torch.from_numpy(fb).to(device)


class _Featurizer:
    def __init__(self, device):
        import torch
        self.device = device; self.window = torch.hann_window(N_FFT, device=device); self.filters = _mel_filters(device)

    def __call__(self, pcm):
        import torch
        wave = pcm.to(self.device, non_blocking=True)
        spec = torch.stft(wave, N_FFT, HOP, window=self.window, return_complex=True).abs() ** 2
        mel = torch.clamp(self.filters @ spec, min=1e-10).log10()
        mel = torch.maximum(mel, mel.amax(dim=(1, 2), keepdim=True) - 8.0)
        return ((mel + 4.0) / 4.0).unsqueeze(1)


def _model(device):
    from torch import nn
    def block(i, o): return nn.Sequential(nn.Conv2d(i, o, 3, padding=1), nn.BatchNorm2d(o), nn.ReLU(), nn.MaxPool2d(2))
    return nn.Sequential(block(1, 16), block(16, 32), block(32, 64), block(64, 128), nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Dropout(0.2), nn.Linear(128, 1)).to(device)


def _wilson(k, n, z=1.96):
    if n == 0: return None
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return {'estimate': round(p, 4), 'low': round(max(0.0, c - h), 4), 'high': round(min(1.0, c + h), 4), 'n': n}


def _metrics(y, pred):
    tp = sum(1 for a, b in zip(y, pred) if a and b); fp = sum(1 for a, b in zip(y, pred) if not a and b)
    fn = sum(1 for a, b in zip(y, pred) if a and not b); tn = sum(1 for a, b in zip(y, pred) if not a and not b)
    return {'n': len(y), 'confusion': {'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn}, 'accuracy': _wilson(tp + tn, len(y)),
            'precision': _wilson(tp, tp + fp), 'recall': _wilson(tp, tp + fn), 'specificity': _wilson(tn, tn + fp)}


def _fit(train_items, device, featurizer, control, seed, state, tag):
    import numpy as np
    import torch
    torch.manual_seed(seed)
    X = np.concatenate([it['windows'] for it in train_items]); y = np.concatenate([np.full(len(it['windows']), float(it['label'] == 'music')) for it in train_items])
    w = np.concatenate([np.full(len(it['windows']), 0.5 if it.get('weak') else 1.0) for it in train_items])
    pos = max(1.0, float((y == 1).sum())); neg = max(1.0, float((y == 0).sum()))
    pos_weight = torch.tensor([neg / pos], device=device)
    model = _model(device); opt = torch.optim.AdamW(model.parameters(), lr=control['lr'], weight_decay=1e-4)
    Xt, yt, wt = torch.from_numpy(X), torch.from_numpy(y).float(), torch.from_numpy(w).float()
    g = torch.Generator(); g.manual_seed(seed); steps = 0
    for epoch in range(control['epochs']):
        model.train(); order = torch.randperm(len(Xt), generator=g); losses = []
        for i in range(0, len(order), control['batch_size']):
            idx = order[i:i + control['batch_size']]
            mel = featurizer(Xt[idx]); target = yt[idx].to(device); weight = wt[idx].to(device)
            if control.get('augment', True):
                mel = mel + torch.randn_like(mel) * 0.02
            logits = model(mel).squeeze(1)
            loss = (torch.nn.functional.binary_cross_entropy_with_logits(logits, target, pos_weight=pos_weight, reduction='none') * weight).mean()
            opt.zero_grad(set_to_none=True); loss.backward(); opt.step(); steps += 1; losses.append(float(loss.detach()))
            if control.get('smoke') and steps >= 3: break
        state.update(progress={'stage': f'training {tag}', 'epoch': epoch + 1, 'epochs': control['epochs'], 'step': steps, 'loss': round(float(np.mean(losses)), 5) if losses else None,
                               'gpu_memory_gb': round(torch.cuda.max_memory_allocated() / 1e9, 2), 'train_windows': len(Xt)})
        if control.get('smoke'): break
    return model, steps


def _predict(model, items, device, featurizer, batch=512):
    import numpy as np
    import torch
    model.eval(); out = []
    with torch.no_grad():
        for it in items:
            probs = []
            for i in range(0, len(it['windows']), batch):
                probs.append(torch.sigmoid(model(featurizer(torch.from_numpy(it['windows'][i:i + batch]))).squeeze(1)).cpu().numpy())
            out.append(np.concatenate(probs) if probs else np.zeros(0))
    return out


def _weak_items(control, state, seed):
    """Staged-corpus files whose cue reading is unambiguous: training-only weak labels, never counted in evaluation."""
    job_dir = Path(control.get('measurement_job_dir') or '')
    if not job_dir.is_dir() or not (job_dir / 'results_compact.json').exists():
        return [], {'status': 'unavailable', 'reason': 'no completed corpus measurement on this host'}
    rows = json.loads((job_dir / 'results_compact.json').read_text()); mapping = json.loads((job_dir / 'results_map.json').read_text())
    corpus = Path(control['lab_corpus_root']).resolve() / 'corpus' / 'datasets'
    rng = random.Random(seed); negatives, positives = {}, []
    for r in rows:
        if 'reads_as' not in r or r['ref'] not in mapping: continue
        if r['reads_as'] == 'speech' and r['music_windows'] == 0 and r['windows'] >= 10 and r['confidence'] >= 0.6:
            negatives.setdefault(r['language'], []).append(r)
        elif r['reads_as'] == 'music' and r['windows'] >= 4 and r['music_windows'] / max(1, r['windows']) >= 0.6:
            positives.append(r)
    chosen = []
    for language, group in sorted(negatives.items()):
        rng.shuffle(group); chosen += [(r, 'speech') for r in group[:int(control['weak_negatives_per_language'])]]
    chosen += [(r, 'music') for r in positives[:int(control['weak_positive_files'])]]
    items, failures = [], 0
    for index, (r, label) in enumerate(chosen):
        path = corpus / mapping[r['ref']]
        try:
            samples = _decode(path, min(float(control['max_seconds_per_file']), 120.0))
            windows = _windows(samples, int(control['max_windows_per_file']) // 3, seed + index)
        except Exception:
            failures += 1; continue
        if len(windows) >= 4:
            items.append({'item_id': 'weak:' + r['ref'], 'label': label, 'weak': True, 'language': r['language'], 'windows': windows})
        if index % 25 == 0:
            state.update(progress={'stage': 'decoding weak staged windows', 'files': index + 1, 'of': len(chosen)})
    summary = {'status': 'used_for_training_only', 'files': len(items), 'decode_failures': failures,
               'speech_files': sum(it['label'] == 'speech' for it in items), 'music_files': sum(it['label'] == 'music' for it in items),
               'windows': int(sum(len(it['windows']) for it in items)), 'rule': 'speech: reads_as speech, zero music windows, confidence ≥ 0.6; music: reads_as music with ≥ 60% music windows'}
    return items, summary


def train_music_detector(control, state):
    import numpy as np
    import torch
    start = time.monotonic()
    if not torch.cuda.is_available():
        raise ValueError('MUSIC_DETECTOR_REQUIRES_GPU')
    torch.backends.cudnn.benchmark = True
    seed = int(control['seed']); random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    device = 'cuda'; featurizer = _Featurizer(device)
    refs = Path(control['refs_dir']).resolve()
    labelled, verification = [], []
    state.update(progress={'stage': 'verifying shipped labelled recordings', 'files': 0, 'of': len(control['labelled_manifest'])})
    for index, item in enumerate(control['labelled_manifest']):
        path = refs / item['file']
        ok = path.exists() and _sha256(path) == item['sha256']
        verification.append({'item_id': item['item_id'], 'digest_verified': ok})
        if not ok: continue
        samples = _decode(path, float(control['max_seconds_per_file']))
        windows = _windows(samples, int(control['max_windows_per_file']), seed + index)
        if len(windows) >= 2:
            labelled.append({'item_id': item['item_id'], 'title': item.get('title', ''), 'label': item['label'], 'label_source': item['label_source'], 'windows': windows})
        state.update(progress={'stage': 'decoding labelled recordings', 'files': index + 1, 'of': len(control['labelled_manifest'])})
    if sum(1 for v in verification if not v['digest_verified']):
        raise ValueError('SHIPPED_RECORDING_DIGEST_MISMATCH')
    positives = [it for it in labelled if it['label'] == 'music']; negatives = [it for it in labelled if it['label'] != 'music']
    if len(positives) < 2 or len(negatives) < 2:
        raise ValueError('LABELLED_SET_TOO_SMALL_FOR_FILE_DISJOINT_FOLDS')
    weak, weak_summary = _weak_items(control, state, seed)
    folds = max(2, min(int(control['folds']), len(positives), len(negatives)))
    rng = random.Random(seed); rng.shuffle(positives); rng.shuffle(negatives)
    assignment = {}
    for group in (positives, negatives):
        for i, it in enumerate(group): assignment[it['item_id']] = i % folds
    oof_file, oof_window, steps_total = {}, {'y': [], 'pred': [], 'group': []}, 0
    for fold in range(folds):
        test = [it for it in labelled if assignment[it['item_id']] == fold]; train = [it for it in labelled if assignment[it['item_id']] != fold] + weak
        model, steps = _fit(train, device, featurizer, control, seed + fold, state, f'fold {fold + 1} of {folds}'); steps_total += steps
        for it, probs in zip(test, _predict(model, test, device, featurizer)):
            oof_file[it['item_id']] = float(probs.mean()) if len(probs) else 0.0
            oof_window['y'] += [it['label'] == 'music'] * len(probs); oof_window['pred'] += [bool(p >= 0.5) for p in probs]; oof_window['group'] += [it['item_id']] * len(probs)
        del model; torch.cuda.empty_cache()
        if control.get('smoke'): break
    evaluated = [it for it in labelled if it['item_id'] in oof_file]
    y = [it['label'] == 'music' for it in evaluated]; pred = [oof_file[it['item_id']] >= 0.5 for it in evaluated]
    file_level = _metrics(y, pred)
    window_level = _metrics(oof_window['y'], oof_window['pred']) | {'files': len(set(oof_window['group'])), 'note': 'Windows from one recording are correlated; the file-level figures are the ones to compare with the baseline.'}
    per_item = [{'item_id': it['item_id'], 'title': it['title'], 'label': it['label'], 'label_source': it['label_source'], 'windows': int(len(it['windows'])),
                 'probability_music': round(oof_file[it['item_id']], 4), 'correct': bool((oof_file[it['item_id']] >= 0.5) == (it['label'] == 'music'))} for it in evaluated]
    state.update(progress={'stage': 'final fit on all labelled recordings', 'step': steps_total})
    final, steps = _fit(labelled + weak, device, featurizer, control, seed + 100, state, 'final model'); steps_total += steps
    weak_agreement = None
    if weak:
        agree = [bool((p.mean() >= 0.5) == (it['label'] == 'music')) for it, p in zip(weak, _predict(final, weak, device, featurizer)) if len(p)]
        weak_agreement = {'files': len(agree), 'agreement_with_cue_reading': _wilson(sum(agree), len(agree)), 'reading': 'Agreement with the cue reading on training-only weak files; not an accuracy figure.'}
    art = Path(control['job_dir']) / 'artefact'; art.mkdir(parents=True, exist_ok=True)
    torch.save({'state_dict': {k: v.detach().cpu() for k, v in final.state_dict().items()}, 'config': {'sr': SR, 'window_seconds': WINDOW_S, 'n_fft': N_FFT, 'hop': HOP, 'n_mels': N_MELS, 'threshold': 0.5},
                'classes': ['not music', 'music'], 'trained_on': {'labelled_files': len(labelled), 'weak_files': len(weak)}}, art / 'music_detector.pt')
    recipe = {k: control[k] for k in ('seed', 'epochs', 'folds', 'batch_size', 'lr', 'max_seconds_per_file', 'max_windows_per_file', 'weak_negatives_per_language', 'weak_positive_files', 'owner_order_ref')}
    recipe.update(model='4-block 2-D CNN over 64-band log-mel of the 2 s window; BCE with class-balanced positive weight; weak windows at half weight', precision='fp32', smoke=bool(control.get('smoke')))
    (art / 'recipe.json').write_text(json.dumps(recipe, sort_keys=True))
    digest = hashlib.sha256()
    for f in sorted(p for p in art.rglob('*') if p.is_file()):
        digest.update(str(f.relative_to(art)).encode()); digest.update(bytes.fromhex(_sha256(f)))
    baseline = control.get('baseline') or {}
    def beats(name, higher_is_better=True):
        ours = (file_level.get(name) or {}).get('estimate'); theirs = baseline.get(name)
        return None if ours is None or theirs is None else bool(ours >= theirs)
    return {'target': 'contains music (music or speech-over-music) versus not', 'items': len(evaluated), 'positives': sum(y), 'negatives': len(y) - sum(y),
            'label_sources': dict(sorted(((it['label_source'], sum(1 for j in labelled if j['label_source'] == it['label_source'])) for it in labelled))),
            'folds': folds, 'file_level': file_level, 'window_level': window_level, 'per_item': per_item, 'weak_supervision': weak_summary, 'weak_agreement': weak_agreement,
            'digest_verification': verification, 'recipe': recipe, 'recipe_sha256': hashlib.sha256(json.dumps(recipe, sort_keys=True).encode()).hexdigest(),
            'baseline_reference': baseline, 'against_baseline': {'accuracy': beats('accuracy'), 'recall': beats('recall'), 'precision': beats('precision'),
                                                                'rule': 'out-of-fold file-level estimate at or above the learned baseline point estimate on the same kind of labelled recordings'},
            'training': {'steps': steps_total, 'epochs': int(control['epochs']), 'elapsed_seconds': round(time.monotonic() - start), 'device': device, 'gpu_index': control.get('gpu_index'),
                         'gpu': torch.cuda.get_device_name(0), 'gpu_max_memory_gb': round(torch.cuda.max_memory_allocated() / 1e9, 2),
                         'labelled_windows': int(sum(len(it['windows']) for it in labelled)), 'weak_windows': weak_summary.get('windows', 0)},
            'artefact': {'path': str(art), 'sha256': digest.hexdigest(), 'custody': 'RMS tenant; stays on the GPU host; served only after the recorded admission'},
            'limitations': ['Small labelled set: file-level intervals are wide; the owner library is one genre and one source',
                            'Weak staged-corpus windows carry cue-reading labels, not human labels, and were used for training only',
                            'Mixed speech-over-music is scored as music; no separate mixed class is labelled yet'],
            'raw_media_exported': False, 'paths_exported': False}
