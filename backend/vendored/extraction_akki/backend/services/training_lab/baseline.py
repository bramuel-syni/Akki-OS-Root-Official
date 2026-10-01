"""Music-identification baseline: the numbers a trained detector must beat. Deterministic; cue reading + shallow learned model
on measured observables; file-level leave-one-out and window-level grouped folds; honest small-sample intervals."""
import numpy as np

from services.audio_plane_v1 import acoustic_observables as ao
from services.media_library import acoustics, store
from services.training_lab import corpus_measurement
from services.training_lab import statistics as stats
from services.training_lab import store as lab

SEED = 41
POSITIVE = {'music', 'mixed'}


def _label(row, policy):
    if row['label_status'] == 'human_reviewed' and row['event_label'] in ('speech', 'music', 'mixed'):
        return row['event_label'], 'human_reviewed'
    if row.get('reference'):
        return row['event_label'], 'source_catalogue'
    if row['event_label'] in ('speech', 'music', 'mixed'):
        return row['event_label'], 'owner_declared'
    if policy == 'music' and row['kind'] == 'audio':
        return 'music', 'owner_music_library'
    return None, 'unlabelled'


def _synthetic_items():
    import tempfile
    import wave
    rng = np.random.default_rng(SEED); sr = ao.SR; items = []
    signals = {'white noise': ('noise', 0.2 * rng.standard_normal(sr * 10)), 'pink noise': ('noise', np.cumsum(rng.standard_normal(sr * 10)) * 0.002),
               'digital silence': ('silence', np.zeros(sr * 8)), 'room tone −60 dBFS': ('silence', 0.001 * rng.standard_normal(sr * 8))}
    with tempfile.TemporaryDirectory() as folder:
        for index, (name, (label, x)) in enumerate(signals.items()):
            path = f'{folder}/synthetic_{index}.wav'
            with wave.open(path, 'wb') as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())
            items.append({'item_id': 'synthetic:' + name, 'title': f'Generated {name}', 'label': label, 'label_source': 'synthetic_generated', 'profile': ao.measure_file(path)})
    return items


def reference_set(tenant, request):
    rows = store.db().media_files.find({'tenant_id': tenant, 'kind': 'audio', 'is_deleted': False, 'status': 'available', 'rights_status': {'$ne': 'withdrawn'}}, {'_id': 0})
    items, excluded, pending = [], [], []
    for row in rows:
        label, source = _label(row, request['unlabelled_library_audio'])
        if label is None:
            excluded.append({'file_id': row['file_id'], 'title': row['title'], 'reason': 'No speech/music label; not counted'}); continue
        job = acoustics.get(tenant, row['file_id'])
        if not job or job['status'] != 'measured':
            pending.append({'file_id': row['file_id'], 'title': row['title'], 'status': (job or {}).get('status', 'unmeasured')}); continue
        items.append({'item_id': row['file_id'], 'title': row['title'], 'label': label, 'label_source': source, 'profile': job['profile'], 'reference': bool(row.get('reference'))})
    if request.get('include_synthetic', True):
        items.extend(_synthetic_items())
    return items, excluded, pending


def _matrix(dicts):
    names = list(dicts[0].keys()); X = np.array([[d[k] if d[k] is not None else np.nan for k in names] for d in dicts], dtype=float)
    return names, X


def _standardize(train, test):
    median = np.nanmedian(train, axis=0); median = np.where(np.isfinite(median), median, 0.0)
    train = np.where(np.isnan(train), median, train); test = np.where(np.isnan(test), median, test)
    mu, sd = train.mean(axis=0), train.std(axis=0); sd = np.where(sd > 1e-9, sd, 1.0)
    return (train - mu) / sd, (test - mu) / sd


def logistic_fit(X, y, l2=1.0, iterations=30):
    """L2-regularised logistic regression by Newton steps; deterministic, no randomness."""
    Xb = np.hstack([np.ones((len(X), 1)), X]); w = np.zeros(Xb.shape[1]); reg = np.full(Xb.shape[1], l2); reg[0] = 0.0
    for _ in range(iterations):
        p = 1 / (1 + np.exp(-Xb @ w)); grad = Xb.T @ (p - y) + reg * w
        hess = (Xb * (p * (1 - p))[:, None]).T @ Xb + np.diag(reg)
        step = np.linalg.solve(hess, grad); w -= step
        if np.max(np.abs(step)) < 1e-8: break
    return w


def logistic_predict(w, X):
    return 1 / (1 + np.exp(-(np.hstack([np.ones((len(X), 1)), X]) @ w)))


def _counts(y, pred):
    y, pred = np.asarray(y, bool), np.asarray(pred, bool)
    return {'tp': int((y & pred).sum()), 'fp': int((~y & pred).sum()), 'fn': int((y & ~pred).sum()), 'tn': int((~y & ~pred).sum())}


def _rate(successes, n):
    return stats.wilson_interval(int(successes), int(n)) if n > 0 else None


def metrics(y, pred, groups=None):
    c = _counts(y, pred); n = len(y); correct = (np.asarray(y, bool) == np.asarray(pred, bool)).astype(float)
    out = {'n': n, 'confusion': c, 'accuracy': _rate(c['tp'] + c['tn'], n), 'precision': _rate(c['tp'], c['tp'] + c['fp']), 'recall': _rate(c['tp'], c['tp'] + c['fn']),
           'specificity': _rate(c['tn'], c['tn'] + c['fp'])}
    if n >= 2 and (groups is None or len(set(groups)) >= 2):
        out['accuracy_bootstrap'] = stats.bootstrap_interval(correct, seed=SEED, groups=groups)
    return out


def _windows(items):
    rows, labels, groups = [], [], []
    for item in items:
        for w in item['profile']['signature']['timeline']:
            if w['reads_as'] == 'silence' and item['label'] != 'silence': continue
            cues = w.get('cues') or {}
            rows.append({k: cues.get(k) for k in ao.WINDOW_CUES}); labels.append(item['label'] in POSITIVE); groups.append(item['item_id'])
    return rows, np.array(labels, bool), groups


def compute(items, corpus_rows=None):
    if len(items) < 4 or len({i['label'] in POSITIVE for i in items}) < 2:
        return {'status': 'insufficient_reference_set', 'reason': 'At least four measured recordings with both music and non-music labels are required'}
    y = np.array([i['label'] in POSITIVE for i in items], bool)
    heuristic = np.array([i['profile']['signature']['reads_as'] in POSITIVE for i in items], bool)
    names, X = _matrix([ao.features(i['profile']) for i in items])
    learned = np.zeros(len(items), bool); probabilities = np.zeros(len(items))
    for k in range(len(items)):
        mask = np.arange(len(items)) != k
        if len(set(y[mask])) < 2: learned[k] = heuristic[k]; probabilities[k] = float(heuristic[k]); continue
        train, test = _standardize(X[mask], X[k:k + 1]); w = logistic_fit(train, y[mask].astype(float))
        probabilities[k] = logistic_predict(w, test)[0]; learned[k] = probabilities[k] >= 0.5
    full_train, _ = _standardize(X, X); w_full = logistic_fit(full_train, y.astype(float))
    order = np.argsort(-np.abs(w_full[1:]))[:10]
    drivers = [{'feature': names[i], 'weight': round(float(w_full[1 + i]), 3), 'direction': 'music' if w_full[1 + i] > 0 else 'not music'} for i in order]
    per_item = [{'item_id': i['item_id'], 'title': i['title'], 'label': i['label'], 'label_source': i['label_source'], 'reads_as': i['profile']['signature']['reads_as'],
                 'reading_correct': bool(heuristic[k] == y[k]), 'learned_probability_music': round(float(probabilities[k]), 3), 'learned_correct': bool(learned[k] == y[k])}
                for k, i in enumerate(items)]
    win_rows, win_y, win_groups = _windows(items)
    window = None
    if len(win_rows) >= 20 and len(set(win_y)) == 2 and len(set(win_groups)) >= 5:
        _, WX = _matrix(win_rows); pred = np.zeros(len(win_rows), bool); files = sorted(set(win_groups)); rng = np.random.default_rng(SEED); rng.shuffle(files)
        folds = [set(files[f::5]) for f in range(5)]
        for fold in folds:
            test_idx = np.array([g in fold for g in win_groups]); train_idx = ~test_idx
            if not test_idx.any() or len(set(win_y[train_idx])) < 2: continue
            train, test = _standardize(WX[train_idx], WX[test_idx]); w = logistic_fit(train, win_y[train_idx].astype(float), l2=3.0)
            pred[test_idx] = logistic_predict(w, test) >= 0.5
        window_heuristic = np.array([False] * len(win_rows), bool)
        k = 0
        for item in items:
            for w in item['profile']['signature']['timeline']:
                if w['reads_as'] == 'silence' and item['label'] != 'silence': continue
                window_heuristic[k] = w['reads_as'] == 'music'; k += 1
        window = {'windows': len(win_rows), 'files': len(files), 'reading': metrics(win_y, window_heuristic, groups=win_groups), 'learned_grouped_5fold': metrics(win_y, pred, groups=win_groups),
                  'note': 'Windows from one recording are correlated; intervals resample whole recordings.'}
    corpus = None
    if corpus_rows:
        CX = np.array([[r['features'].get(k) if r['features'].get(k) is not None else np.nan for k in names] for r in corpus_rows], dtype=float)
        _, ctest = _standardize(X, CX); cprob = logistic_predict(w_full, ctest)
        per_language = {}
        for language in sorted({r['language'] for r in corpus_rows}):
            idx = [k for k, r in enumerate(corpus_rows) if r['language'] == language]; group = [corpus_rows[k] for k in idx]
            read_music = sum(r['reads_as'] in POSITIVE for r in group); learned_music = int((cprob[idx] >= 0.5).sum())
            per_language[language] = {'files': len(group), 'read_as_music_or_mixed': read_music, 'read_share': _rate(read_music, len(group)),
                                      'learned_music': learned_music, 'learned_share': _rate(learned_music, len(group)),
                                      'music_window_share': round(float(np.mean([r['music_windows'] / max(r['windows'], 1) for r in group])), 4),
                                      'files_with_music_windows': sum(r['music_windows'] >= 2 for r in group), 'hours': round(sum(r['duration_s'] for r in group) / 3600, 2)}
        total_read = sum(r['reads_as'] in POSITIVE for r in corpus_rows)
        corpus = {'files': len(corpus_rows), 'per_language': per_language, 'read_as_music_or_mixed': _rate(total_read, len(corpus_rows)),
                  'learned_music': _rate(int((cprob >= 0.5).sum()), len(corpus_rows)),
                  'reading': 'Unlabelled: the staged corpus is radio speech with no music annotation. Shares are readings, and an upper bound on the false-music rate only if the corpus holds no music.',
                  'review_candidates': int(sum(r['music_windows'] >= 2 for r in corpus_rows))}
    composition = {}
    for item in items:
        key = f"{item['label']}·{item['label_source']}"; composition[key] = composition.get(key, 0) + 1
    return {'status': 'complete', 'target': 'contains music (music or speech-over-music) versus not', 'items': len(items), 'positives': int(y.sum()), 'negatives': int((~y).sum()),
            'composition': composition, 'features': len(names),
            'baseline_reading': {'method': 'cue reading of the measured profile (no training)', **metrics(y, heuristic)},
            'baseline_learned': {'method': 'L2 logistic regression on measured observables; leave-one-recording-out', **metrics(y, learned)},
            'drivers': drivers, 'per_item': per_item, 'window_level': window, 'corpus_test': corpus,
            'limitations': ['Small reference set: intervals are wide and the owner library is one genre and one source',
                            'Owner recordings counted as music on the owner declaration unless labelled; no human-reviewed labels yet' if any(i['label_source'] == 'owner_music_library' for i in items) else 'Labels come from human review, source catalogues or owner declarations',
                            'Synthetic noise and silence are generated, not recorded' if any(i['label_source'] == 'synthetic_generated' for i in items) else 'No synthetic items',
                            'Reading and learned baseline are not a trained cognition model; nothing here authorizes training']}


def submit(actor, key, body):
    items, excluded, pending = reference_set(actor['tenant_id'], body)
    request = dict(body); row, created = lab.enqueue(actor['tenant_id'], actor['principal_id'], key, request, kind='music_baseline')
    if not created:
        return row, False
    update = {'reference_set': {'measured': len(items), 'excluded': excluded, 'pending': pending}}
    for item in pending:
        file_row = store.get(actor['tenant_id'], item['file_id'])
        if file_row: acoustics.request(actor, file_row)
    if pending:
        update.update(status='waiting_measurements', hold_reason=f"{len(pending)} recordings still being measured")
        acoustics.start_worker()
    else:
        corpus_doc, corpus_rows = corpus_measurement.rows(actor['tenant_id']) if request.get('include_corpus_test', True) else (None, [])
        update.update(status='complete', result=compute(items, corpus_rows), corpus_measurement_id=(corpus_doc or {}).get('measurement_id'), finished_at=lab.now(), outcome='baseline_established')
    lab.db().training_lab_runs.update_one({'run_id': row['run_id']}, {'$set': {**update, 'updated_at': lab.now()}})
    return lab.get(actor['tenant_id'], row['run_id']), True


def advance(tenant):
    """Complete waiting baseline runs once their measurements exist (called by the acoustics worker)."""
    for row in lab.db().training_lab_runs.find({'tenant_id': tenant, 'kind': 'music_baseline', 'status': 'waiting_measurements'}, {'_id': 0}):
        items, excluded, pending = reference_set(tenant, row['request'])
        if pending:
            lab.db().training_lab_runs.update_one({'run_id': row['run_id']}, {'$set': {'reference_set.pending': pending, 'hold_reason': f"{len(pending)} recordings still being measured", 'updated_at': lab.now()}})
            continue
        corpus_doc, corpus_rows = corpus_measurement.rows(tenant) if row['request'].get('include_corpus_test', True) else (None, [])
        lab.db().training_lab_runs.update_one({'run_id': row['run_id']}, {'$set': {'status': 'complete', 'result': compute(items, corpus_rows), 'reference_set': {'measured': len(items), 'excluded': excluded, 'pending': []},
                                                                            'corpus_measurement_id': (corpus_doc or {}).get('measurement_id'), 'finished_at': lab.now(), 'outcome': 'baseline_established', 'updated_at': lab.now()},
                                                                   '$unset': {'hold_reason': ''}})
