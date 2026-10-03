"""Whole-estate forecast by Monte Carlo (owner order 3 Oct 2026: "if x = m for the part of the estate we read, what is m for the whole
estate … sample folder contents, scale by each folder's population, forecast with Monte Carlo principles").

Every folder stratum of every store is a population with a known file count and byte total (the listing). Strata the census read are
MEASURED: their hours and composition enter the simulation as normal draws around the estimator and its standard error (zero for whole-folder
reads). Strata the census could not read — buckets the key is refused on, Archive-class buckets, folders not yet probed or sampled — are
FORECAST: in every simulation each one borrows a donor folder of the same media kind, chosen with probability proportional to the donor's
file count and its similarity in mean file size, and takes the donor's seconds-per-megabyte (hours = bytes × rate), speech and music shares
and language mix. Summing the strata in each of the simulations gives the distribution of the whole estate's hours, speech, music and
hours per language; the 2.5th and 97.5th percentiles are the 95 % forecast interval. Deterministic (seeded) so a rebuild reproduces it."""
from __future__ import annotations

import hashlib
import math
from collections import defaultdict
from typing import Any, Dict, List

import numpy as np

SIMULATIONS = 2000
SEED = 'akki-estate-forecast-v1'
KERNEL_SIGMA = 1.0          # natural-log units of mean file size; doubled while fewer than MIN_EFFECTIVE donors carry weight
MIN_EFFECTIVE = 3.0
MIN_DONOR_READS = 5
LANGUAGES_KEPT = 12
FOLDERS_KEPT = 100
_CACHE: Dict[str, Dict[str, Any]] = {}

BASIS_LABEL = {'measured': 'read and judged', 'header_measured': 'hours on the headers, content forecast', 'forecast_unsampled': 'readable, not yet sampled — forecast',
               'forecast_denied': 'key refused — forecast', 'forecast_archived': 'archive class — forecast'}
# Station names carried by folder paths (owner order 3 Oct 2026: "each station carries a name … use it to identify the language"). The codes
# follow the transcription workbench's folder_languages register; Hot 96 declares English itself. Order matters: longer tokens first.
STATION_TOKENS = (('citizen radio', 'swa', 'Radio Citizen'), ('radio citizen', 'swa', 'Radio Citizen'), ('radiocitizen', 'swa', 'Radio Citizen'), ('inooro', 'kik', 'Inooro FM'),
                  ('chamgei', 'kln', 'Chamgei'), ('mulembe', 'lwg', 'Mulembe FM'), ('wimwaro', 'ebu', 'Wimwaro FM'), ('hot 96', 'eng', 'Hot 96'), ('hot96', 'eng', 'Hot 96'),
                  ('hot_96', 'eng', 'Hot 96'), ('egesa', 'guz', 'Egesa'), ('musyi', 'kam', 'Musyi FM'), ('sulwe', 'bxk', 'Sulwe FM'), ('bahari', 'swa', 'Bahari FM'),
                  ('vuuka', 'mrg', 'Vuuka'), ('ramogi', 'luo', 'Ramogi FM'), ('muuga', 'mer', 'Muuga FM'), ('enduata', 'mas', 'Enduata'))


def station_of(label: str, folder: str):
    path = f"{label or ''}/{folder or ''}".lower()
    return next(((code, name) for token, code, name in STATION_TOKENS if token in path), None)


def _summary(values: np.ndarray) -> Dict[str, float]:
    lo, med, hi = np.percentile(values, [2.5, 50, 97.5])
    return {'est': round(float(med), 1), 'mean': round(float(values.mean()), 1), 'lo': round(float(max(0.0, lo)), 1), 'hi': round(float(hi), 1)}


def _kind(folder: Dict[str, Any], content: Dict[str, Any]) -> str:
    kinds = folder.get('kinds') or {}
    if kinds:
        return max(kinds.items(), key=lambda kv: kv[1])[0]
    return 'video' if (content.get('media_video_objects') or 0) >= (content.get('media_audio_objects') or 0) else 'audio'


def _strata(outcomes: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for store, outcome in outcomes.items():
        for source in (outcome or {}).get('sources') or []:
            content = source.get('content')
            if not content:
                continue
            access = content.get('access') or 'readable'
            for folder in content.get('folders') or []:
                files, size = int(folder.get('files') or 0), int(folder.get('bytes') or 0)
                if not files or not size:
                    continue
                hours, sample, est = folder.get('hours') or {}, folder.get('sample') or {}, folder.get('estimates') or {}
                speech = est.get('speech') or {}
                has_hours = hours.get('est') is not None and (hours.get('probed_files') or 0) > 0
                has_content = has_hours and speech.get('est') is not None and (sample.get('read') or 0) > 0
                if has_content:
                    basis = 'measured'
                elif has_hours:
                    basis = 'header_measured'
                else:
                    basis = {'denied': 'forecast_denied', 'archived': 'forecast_archived'}.get(access, 'forecast_unsampled')
                rows.append({'store': store, 'label': source.get('label'), 'access': access, 'folder': folder.get('folder'), 'files': files, 'bytes': size,
                             'kind': _kind(folder, content), 'log_size': math.log(size / files), 'basis': basis, 'status': sample.get('status'),
                             'hours': hours, 'sample': sample, 'estimates': est, 'rate': hours.get('seconds_per_mb')})
    return rows


def _donors(strata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for s in strata:
        if s['basis'] != 'measured' or not s['rate'] or (s['hours'].get('est') or 0) <= 0:
            continue
        if s['status'] not in ('census', 'sampled') and (s['sample'].get('read') or 0) < MIN_DONOR_READS:
            continue
        h = s['hours']['est']
        speech = max(0.0, (s['estimates'].get('speech') or {}).get('est') or 0.0)
        music = max(0.0, (s['estimates'].get('music') or {}).get('est') or 0.0)
        langs = {code: max(0.0, e.get('est') or 0.0) for code, e in (s['estimates'].get('languages') or {}).items() if e and e.get('est') is not None}
        out.append({**s, 'speech_share': min(1.0, speech / h), 'music_share': min(1.0, music / h),
                    'lang_share': {code: min(1.0, v / speech) for code, v in langs.items()} if speech > 0 else {}})
    return out


def _weights(target: Dict[str, Any], donors: List[Dict[str, Any]], sigma: float) -> np.ndarray | None:
    """Donor weights for one forecast stratum: every readable bucket is one witness (bucket weight ∝ √ of its files, so a well-read bucket
    counts for more but no single bucket speaks for the estate), its folders share that weight by file count, and a Gaussian kernel on
    log mean file size favours donors whose files look like the target's."""
    same = [i for i, d in enumerate(donors) if d['kind'] == target['kind']]
    pool = same or list(range(len(donors)))
    if not pool:
        return None
    bucket_files: Dict[str, int] = defaultdict(int)
    for i in pool:
        bucket_files[donors[i]['label']] += donors[i]['files']
    base = np.array([math.sqrt(bucket_files[donors[i]['label']]) * donors[i]['files'] / bucket_files[donors[i]['label']] for i in pool])
    delta = np.array([target['log_size'] - donors[i]['log_size'] for i in pool])
    for widen in range(3):
        w = base * np.exp(-(delta ** 2) / (2 * (sigma * 2 ** widen) ** 2))
        if w.sum() > 0 and (w.sum() ** 2) / (w ** 2).sum() >= MIN_EFFECTIVE:
            break
    else:
        w = base
    full = np.zeros(len(donors))
    full[pool] = w / w.sum()
    return full


def _normal(rng, est, se, n) -> np.ndarray:
    if not se:
        return np.full(n, float(est or 0.0))
    return np.clip(rng.normal(float(est), float(se), n), 0.0, None)


def forecast(outcomes: Dict[str, Dict[str, Any]], simulations: int = SIMULATIONS) -> Dict[str, Any] | None:
    """outcomes: {'obs': outcome, 'nas': outcome} as retained by the census. Returns the whole-estate forecast, or None without a measured donor."""
    key = hashlib.sha256(repr(sorted((k, (o or {}).get('result_receipt'), (o or {}).get('observed_at')) for k, o in outcomes.items())).encode()).hexdigest()
    if key in _CACHE:
        return _CACHE[key]
    strata = _strata(outcomes)
    donors = _donors(strata)
    if not donors:
        return None
    rng = np.random.default_rng(int(hashlib.sha256(f'{SEED}|{key}'.encode()).hexdigest()[:16], 16))
    n = simulations
    codes = sorted({c for d in donors for c in d['lang_share']}, key=lambda c: -sum((d['estimates']['languages'].get(c) or {}).get('est') or 0 for d in donors))[:LANGUAGES_KEPT]
    code_index = {c: i for i, c in enumerate(codes)}
    rates = np.array([d['rate'] for d in donors])
    speech_share = np.array([d['speech_share'] for d in donors])
    music_share = np.array([d['music_share'] for d in donors])
    lang_share = np.zeros((len(donors), len(codes)))
    for i, d in enumerate(donors):
        for c, v in d['lang_share'].items():
            if c in code_index:
                lang_share[i, code_index[c]] = v
    groups: Dict[str, Dict[str, Any]] = defaultdict(lambda: {'hours': np.zeros(n), 'speech': np.zeros(n), 'music': np.zeros(n), 'unlabelled': np.zeros(n), 'langs': np.zeros((n, len(codes))), 'files': 0, 'bytes': 0, 'strata': 0})
    stations: Dict[str, Dict[str, Any]] = {}
    folder_rows = []
    for s in strata:
        if s['basis'] == 'measured':
            hours = _normal(rng, s['hours']['est'], s['hours'].get('se'), n)
            speech = _normal(rng, (s['estimates'].get('speech') or {}).get('est'), (s['estimates'].get('speech') or {}).get('se'), n)
            music = _normal(rng, (s['estimates'].get('music') or {}).get('est'), (s['estimates'].get('music') or {}).get('se'), n)
            langs = np.zeros((n, len(codes)))
            for c, e in (s['estimates'].get('languages') or {}).items():
                if c in code_index and e and e.get('est') is not None:
                    langs[:, code_index[c]] = _normal(rng, e['est'], e.get('se'), n)
            donor_label = None
        else:
            w = _weights(s, donors, KERNEL_SIGMA)
            idx = rng.choice(len(donors), size=n, p=w)
            hours = _normal(rng, s['hours']['est'], s['hours'].get('se'), n) if s['basis'] == 'header_measured' else s['bytes'] / 1e6 * rates[idx] / 3600.0
            speech, music = hours * speech_share[idx], hours * music_share[idx]
            langs = speech[:, None] * lang_share[idx]
            donor_label = int(np.argmax(w))
        unlabelled = np.clip(speech - langs.sum(axis=1), 0.0, None)  # speech the language model could not assign (abstained or outside its classes)
        station = station_of(s['label'], s['folder'])
        names = ['total', f"store:{s['store']}", f"basis:{s['basis']}", f"source:{s['store']}|{s['label']}"] + ([f"station:{station[0]}"] if station else [])
        if station:
            stations.setdefault(station[0], {'code': station[0], 'station': station[1], 'bases': set(), 'labels': set()})
            stations[station[0]]['bases'].add(s['basis']); stations[station[0]]['labels'].add(s['label'])
        for name in names:
            g = groups[name]
            g['hours'] += hours; g['speech'] += speech; g['music'] += music; g['unlabelled'] += unlabelled; g['langs'] += langs
            g['files'] += s['files']; g['bytes'] += s['bytes']; g['strata'] += 1
        top = int(np.argmax(np.median(langs, axis=0))) if codes and langs.any() else None
        folder_rows.append({'store': s['store'], 'label': s['label'], 'folder': s['folder'], 'kind': s['kind'], 'files': s['files'], 'bytes': s['bytes'], 'basis': s['basis'],
                            'hours': _summary(hours), 'speech': _summary(speech), 'music': _summary(music), 'station': station[1] if station else None,
                            'top_language': codes[top] if top is not None else None, 'top_language_hours': _summary(langs[:, top]) if top is not None else None,
                            'donor': f"{donors[donor_label]['label']} / {donors[donor_label]['folder']}" if donor_label is not None else None})

    def block(g):
        return {'hours': _summary(g['hours']), 'speech': _summary(g['speech']), 'music': _summary(g['music']), 'unlabelled_speech': _summary(g['unlabelled']), 'files': g['files'], 'bytes': g['bytes'], 'strata': g['strata'],
                'languages': dict(sorted(((c, _summary(g['langs'][:, i])) for c, i in code_index.items()), key=lambda kv: -kv[1]['est']))}

    total = block(groups['total'])
    by_basis = {b: block(groups[f'basis:{b}']) for b in BASIS_LABEL if f'basis:{b}' in groups}
    sources = []
    for name, g in groups.items():
        if not name.startswith('source:'):
            continue
        store, label = name[len('source:'):].split('|', 1)
        bases = {s['basis'] for s in strata if s['store'] == store and s['label'] == label}
        sources.append({'store': store, 'label': label, 'access': next(s['access'] for s in strata if s['store'] == store and s['label'] == label),
                        'basis': 'measured' if bases == {'measured'} else 'forecast' if not (bases & {'measured', 'header_measured'}) else 'mixed', **block(g)})
    sources.sort(key=lambda s: -s['hours']['est'])
    folder_rows.sort(key=lambda f: -f['hours']['est'])
    kinds = {k: [d for d in donors if d['kind'] == k] for k in ('audio', 'video')}
    result = {
        'simulations': n, 'seed': SEED, 'strata': len(strata), 'languages': codes,
        'donors': {'strata': len(donors), 'files': sum(d['files'] for d in donors), 'bytes': sum(d['bytes'] for d in donors), 'files_read': sum(d['sample'].get('read') or 0 for d in donors),
                   'by_kind': {k: {'strata': len(v), 'files': sum(d['files'] for d in v),
                                   'seconds_per_mb_p10_p90': [round(float(x), 2) for x in np.percentile([d['rate'] for d in v], [10, 90])] if v else None,
                                   'speech_share_p10_p90': [round(float(x), 3) for x in np.percentile([d['speech_share'] for d in v], [10, 90])] if v else None} for k, v in kinds.items()}},
        'estate': total, 'by_store': {k: block(groups[f'store:{k}']) for k in outcomes if f'store:{k}' in groups}, 'by_basis': by_basis,
        'by_station': {code: {**info, 'bases': sorted(info['bases']), 'labels': sorted(info['labels']), **block(groups[f'station:{code}'])} for code, info in stations.items()},
        'measured_share_of_hours': round(by_basis['measured']['hours']['est'] / total['hours']['est'], 4) if 'measured' in by_basis and total['hours']['est'] else 0.0,
        'forecast_share_of_hours': round(sum(v['hours']['est'] for b, v in by_basis.items() if b.startswith('forecast')) / total['hours']['est'], 4) if total['hours']['est'] else 0.0,
        'sources': sources, 'folders': folder_rows[:FOLDERS_KEPT], 'folders_total': len(folder_rows),
        'method': (f"{n:,} seeded simulations over {len(strata):,} folder strata. Measured strata: normal draws around the census estimator and its standard error. "
                   f"Forecast strata: in each simulation a donor folder of the same media kind is drawn — every readable bucket is one witness (bucket weight ∝ √ of its files), its folders "
                   f"share that weight by file count, and a Gaussian kernel on log mean file size (σ = {KERNEL_SIGMA}, widened until at least {int(MIN_EFFECTIVE)} donors carry weight) favours "
                   f"donors whose files look like the target's; hours = bytes × the donor's seconds per megabyte; speech, music and language hours = hours × the donor's shares. Strata are "
                   f"summed in every simulation; est is the median, lo–hi the 2.5th–97.5th percentiles. Intervals carry sampling and between-folder variation, not model error or the chance "
                   f"that refused buckets differ in kind from every readable one."),
    }
    _CACHE.clear()
    _CACHE[key] = result
    return result
