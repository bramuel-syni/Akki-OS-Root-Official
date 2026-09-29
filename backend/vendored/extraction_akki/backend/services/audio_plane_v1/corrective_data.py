"""Host-only corrective corpus view. Never reassign a baseline held-out presenter to training."""
import hashlib
import json
import random
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from services.audio_plane_v1 import language_cognition_worker as w


def corrective_assignments(items, legacy, seed=31):
    """Keep the original held set, reserve ALL archive presenters, derive dev from train only.

    Unknown/unlinked presenters are excluded, not guessed into a training split.
    Legacy test results have already been observed; they are not a new blind test.
    """
    archive = {presenter for _, presenter, origin in items if origin == 'archive'}
    held = {p for p, split in legacy.items() if split == 'held'}
    pool = {}
    for code, presenter, _ in items:
        if presenter not in archive | held and legacy.get(presenter) == 'train':
            pool.setdefault(code, set()).add(presenter)
    dev = set()
    for code in sorted(pool):
        ids = sorted(pool[code]); random.Random(f'{seed}:{code}').shuffle(ids)
        dev.update(ids[:max(1, len(ids) // 10)])
    return [('archive_test' if p in archive else 'held' if p in held else 'dev' if p in dev
             else 'train' if legacy.get(p) == 'train' else 'excluded') for _, p, _ in items]


def prepare(control, state):
    """Reuse the baseline's exact windowing/split, then increase TRAIN coverage only."""
    import numpy as np
    root = Path(control['root'])
    clusters, origins, conditions = w._clusters(root), w._origins(root), w._conditions(root)
    if not clusters:
        raise ValueError('PRESENTER_LINKAGE_REQUIRED')
    files = w._corpus_files(root)
    codes = sorted(files)
    state.update(progress={'stage': 'reconstructing protected baseline split', 'files': sum(map(len, files.values()))})

    def read(item):
        code, path = item
        if not w._transcript(path).exists():
            return code, path, [], None
        audio = w._load_audio(path, 900)
        segs = w.read_segments(w._transcript(path))
        cap = min(60, max(1, 30000 // len(files[code])))
        seed = int(hashlib.sha256(path.stem.encode()).hexdigest()[:8], 16)
        sampled = w.speech_windows(segs, len(audio), cap, seed=seed)
        session = w._session(path)
        def presenter(spk):
            return f"{code}:{clusters.get(code, {}).get(f'{session}|{spk}', f'{session}|{spk}')}"
        origin = origins.get(f'{code}/{session}', 'folder')
        old = [(code, presenter(spk), origin) for _, spk in sampled]
        # More complete coverage, especially the 60-file Luhya class. No artificial duplicate rows.
        candidates = w.speech_windows(segs, len(audio), control['max_windows_per_file'], seed=seed)
        condition = conditions.get((code, session, path.stem), 'unmeasured')
        rows, seen = [], set()
        for start, spk in candidates:
            if f'{session}|{spk}' not in clusters.get(code, {}):
                continue
            if start in seen:
                continue  # overlapping transcript turns must not duplicate a clip in DP sampling
            seen.add(start)
            pcm = (audio[start:start + int(w.WINDOW_SECONDS * w.SAMPLE_RATE)] * 32767).astype(np.int16)
            rows.append((pcm, codes.index(code), presenter(spk), origin, str(path), start / w.SAMPLE_RATE, condition))
        return code, path, old, rows

    old_items, windows, failures = [], [], []
    plan = [(code, path) for code, paths in files.items() for path in paths]
    with ThreadPoolExecutor(max_workers=control['parallelism']) as pool:
        for n, (code, path, old, rows) in enumerate(pool.map(read, plan)):
            old_items.extend(old)
            if rows is not None:
                windows.extend(rows)
            else:
                failures.append(str(path))
            if n % 100 == 0:
                state.update(progress={'stage': 'windowing authorised local corpus', 'files_done': n,
                                       'files': len(plan), 'windows': len(windows)})
    old_assignment, _ = w.split_by_presenter(old_items)
    legacy = {}
    for i, (_, p, _) in enumerate(old_items):
        split = old_assignment[i]
        if split == 'held' or p not in legacy:
            legacy[p] = split
    assigned = corrective_assignments([(codes[r[1]], r[2], r[3]) for r in windows], legacy)
    sets = {s: [] for s in ('train', 'dev', 'held', 'archive_test', 'excluded')}
    for row, split in zip(windows, assigned):
        sets[split].append(row)
    del windows
    # Remove audio-identical duplicates across splits, protecting test/dev first.
    seen, duplicates = set(), 0
    for split in ('archive_test', 'held', 'dev', 'train'):
        keep = []
        for row in sets[split]:
            h = hashlib.sha256(row[0].tobytes()).digest()
            if h in seen:
                duplicates += 1
            else:
                seen.add(h); keep.append(row)
        sets[split] = keep
    del seen
    if any(not sets[s] for s in ('train', 'dev', 'held')):
        raise ValueError('CORRECTIVE_SPLIT_EMPTY')
    counts = {s: len(rows) for s, rows in sets.items()}
    per = {c: {f'{s}_presenters': len({r[2] for r in rows if codes[r[1]] == c})
               for s, rows in sets.items() if s != 'excluded'} for c in codes}
    for c, row in per.items():
        row['meets_presenter_minimum_n'] = row['train_presenters'] >= w.PRESENTER_MINIMUM_N
    presenter_sets = {s: {r[2] for r in sets[s]} for s in ('train', 'dev', 'held', 'archive_test')}
    if any(presenter_sets[a] & presenter_sets[b] for a in presenter_sets for b in presenter_sets if a < b):
        raise ValueError('SPEAKER_OVERLAP_REFUSED')
    manifest = {'baseline_job_id': control['baseline_job_id'], 'baseline_params': {'max_windows_per_file': 60,
        'max_windows_per_language': 30000, 'max_audio_seconds': 900, 'split_seed': 11},
        'splits': {s: [{'file': r[4], 'start': r[5], 'presenter': r[2], 'language': codes[r[1]], 'condition': r[6]}
                      for r in rows] for s, rows in sets.items() if s != 'excluded'},
        'windows': counts, 'per_language': per, 'duplicate_clips_removed': duplicates,
        'files_without_transcript': len(failures), 'test_reading': 'legacy held-out already observed; not blind independent M9 acceptance',
        'limitations': ['presenter linkage inferred within language, not ground truth or cross-language biometric linkage',
                        'folder language labels, no labelled code-switched spans', 'English/Sheng absent',
                        'DP applies to fixed window dataset; corpus selection/linkage and evaluation are not DP-certified']}
    art = root / 'artefacts' / control['job_id']; art.mkdir(parents=True, exist_ok=True)
    text = json.dumps(manifest, sort_keys=True)
    (art / 'training_manifest.json').write_text(text)
    summary = {k: v for k, v in manifest.items() if k != 'splits'}
    summary['kind'] = 'protected legacy holdout + training-only development; archive presenters excluded from all training'
    summary['speaker_linkage_used'] = True
    summary['files'] = {s: len({r[4] for r in rows}) for s, rows in sets.items()}
    if control['smoke_steps']:
        for s in ('train', 'dev', 'held', 'archive_test'):
            random.Random(control['seed']).shuffle(sets[s])
            sets[s] = sets[s][:1024 if s == 'train' else 128]
        summary['pipeline_smoke_only'] = True
        summary['smoke_windows'] = {s: len(rows) for s, rows in sets.items()}
    return codes, sets, summary, hashlib.sha256(text.encode()).hexdigest(), art