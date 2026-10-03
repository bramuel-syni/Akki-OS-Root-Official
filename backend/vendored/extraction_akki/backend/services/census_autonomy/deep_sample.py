"""Tiered content census (owner ruling 2026-10-02: "sample per folder, a bigger sample, be surgical so we have a high probability of truth").

Tier 1 — facts for every media object: the resumable listing (deep_content) plus a header probe — ranged reads of the head (and, for
containers that keep their index at the end, the tail) placed in a sparse file of the object's exact size and read by ffprobe — giving
duration, codec, sample rate and channels. Every audio file is probed; video files are probed per folder and the rest extrapolated with
the folder's measured seconds-per-byte, with a standard error.
Tier 2 — a deterministic, nested, stratified random sample of files per folder, read byte for byte and judged window by window on the
GPUs (deep_content.run_device). Ratio estimators with finite-population correction give per-folder and per-store speech, music, silence
and language hours with 95 % intervals; folders small enough are read in full and carry no sampling error.
Mtafiti contract: bytes, counts and header durations are FACT signals; model readings and interval estimates are DETECTED signals.
"""
import hashlib
import json
import math
import os
import subprocess
import tempfile
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SEED = 'akki-content-census-sample-v1'
HEAD_BYTES = 96 * 1024
TAIL_BYTES = 384 * 1024
TAIL_EXTS = {'.mp4', '.m4a', '.m4v', '.mov', '.3gp', '.ogg', '.oga', '.opus', '.ts', '.m2ts', '.mts', '.mxf', '.flv', '.webm', '.mkv'}
MOOV_EXTS = {'.mp4', '.m4a', '.m4v', '.mov', '.3gp'}
MOOV_TAIL = 8 << 20
BITRATE_EXTS = {'.mp3', '.mp2', '.aac'}
Z = 1.96
DEFAULT_RATE = 1 / 16000.0   # seconds per byte before any header is read (128 kbit/s); replaced by measured rates at once


def order_key(ref):
    return hashlib.sha256(f'{SEED}|{ref}'.encode()).hexdigest()


def year_of(stamp):
    return (stamp or '')[:4] or 'undated'


def _syncsafe(b):
    return (b[0] << 21) | (b[1] << 14) | (b[2] << 7) | b[3]


# ----------------------------------------------------------------------------------------------------------------- strata
def stratify(items, cap, split_min):
    """Folder strata for one store. items: (key, size, etag, modified, storage_class, kind). Returns names aligned with items and the mode.
    Folders are the first path level; a folder holding more than split_min media files is split into its sub-folders (to depth 4) while the
    store keeps at most `cap` strata, otherwise by year of last write; a store with more than `cap` top-level folders (hash-named uploads)
    is stratified by media kind and year instead. Mixed folders are separated into audio and video strata."""
    level1 = Counter()
    for it in items:
        parts = it[0].split('/')
        level1[parts[0] if len(parts) > 1 else '(root)'] += 1
    if len(level1) > cap:
        return [f'({len(level1):,} folders) · {it[5]} · {year_of(it[3])}' for it in items], 'kind_year'
    counts = defaultdict(Counter)
    for it in items:
        parts = it[0].split('/')
        for d in range(2, min(4, len(parts) - 1) + 1):
            counts[d]['/'.join(parts[:d])] += 1
    strata = dict(level1)
    splits, year_splits = set(), set()
    while True:
        candidates = [(n, p) for p, n in strata.items() if n > split_min and p != '(root)' and p not in year_splits and not p.endswith('/(files)') and p.count('/') < 3]
        if not candidates:
            break
        n, p = max(candidates)
        children = {q: m for q, m in counts[p.count('/') + 2].items() if q.startswith(p + '/')}
        direct = n - sum(children.values())
        if len(children) == 1 and not direct:                 # a single-child chain: descend instead of splitting
            del strata[p]
            splits.add(p)
            strata.update(children)
        elif len(children) > 1 and len(strata) - 1 + len(children) + (1 if direct else 0) <= cap:
            del strata[p]
            splits.add(p)
            strata.update(children)
            if direct:
                strata[p + '/(files)'] = direct
        else:
            year_splits.add(p)
    assign = []
    for it in items:
        parts = it[0].split('/')
        p, d = (parts[0] if len(parts) > 1 else '(root)'), 1
        while p in splits:
            if len(parts) - 1 > d:
                d += 1
                p = '/'.join(parts[:d])
            else:
                p = p + '/(files)'
                break
        if p in year_splits:
            p = f'{p} · {year_of(it[3])}'
        assign.append(p)
    kinds = defaultdict(set)
    for it, s in zip(items, assign):
        kinds[s].add(it[5])
    return [f'{s} · {it[5]}' if len(kinds[s]) > 1 else s for it, s in zip(items, assign)], 'folders'


def grouped(label, items, assign):
    """stratum → items in the seeded sample order (nested: a bigger sample always extends a smaller one)."""
    from services.census_autonomy.deep_content import ref_of
    groups = defaultdict(list)
    for it, s in zip(items, assign):
        ref = ref_of(label, it[0])
        groups[s].append((order_key(ref), ref, it))
    for lst in groups.values():
        lst.sort(key=lambda t: t[0])
    return groups


# ----------------------------------------------------------------------------------------------------------------- header probe
def _ffprobe(path):
    try:
        p = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,bit_rate,format_name:stream=codec_type,codec_name,sample_rate,channels,duration', '-of', 'json', str(path)],
                           capture_output=True, text=True, timeout=60)
        probe = json.loads(p.stdout or '{}')
    except Exception:
        return {}
    streams = probe.get('streams', [])
    audio = next((s for s in streams if s.get('codec_type') == 'audio'), {})
    fmt = probe.get('format', {})
    duration = fmt.get('duration') or audio.get('duration') or next((s.get('duration') for s in streams if s.get('duration')), None)
    return {'duration_s': round(float(duration), 2) if duration else None, 'codec': audio.get('codec_name'), 'sample_rate': int(audio['sample_rate']) if audio.get('sample_rate') else None,
            'channels': audio.get('channels'), 'bit_rate': int(fmt['bit_rate']) if fmt.get('bit_rate') else None, 'container': fmt.get('format_name'),
            'audio_streams': sum(1 for s in streams if s.get('codec_type') == 'audio'), 'video_streams': sum(1 for s in streams if s.get('codec_type') == 'video')}


def _sparse(path, size, head, tail):
    with open(path, 'wb') as out:
        out.truncate(size)
        out.write(head)
        if tail:
            out.seek(size - len(tail))
            out.write(tail)


def probe_header(fetch, item, scratch):
    """Head (+ tail) ranged reads → sparse file of the exact object size → ffprobe. Returns the header row and the bytes fetched."""
    key, size, _etag, _modified, _sc, kind = item
    ext = Path(key).suffix.lower()
    fetched = 0
    whole = size <= HEAD_BYTES + TAIL_BYTES

    def get(a, b):
        nonlocal fetched
        data = fetch(a, b)
        fetched += len(data)
        return data
    if size == 0:
        return {'error': 'EMPTY_OBJECT', 'basis': 'none'}, 0
    if whole:
        head, tail = get(0, size - 1), b''
    else:
        head = get(0, HEAD_BYTES - 1)
        if head[:3] == b'ID3' and len(head) >= 10:
            id3 = _syncsafe(head[6:10]) + 10
            if id3 + 65536 > len(head) and id3 < size:
                head += get(len(head), min(size - 1, id3 + 65536))
        tail = get(max(0, size - TAIL_BYTES), size - 1) if ext in TAIL_EXTS else b''
    path = Path(scratch) / f'hdr-{os.getpid()}-{hashlib.sha1(key.encode()).hexdigest()[:12]}{ext[:8]}'
    try:
        _sparse(path, size, head, tail)
        row = _ffprobe(path)
        basis = 'container'
        if row.get('duration_s') is None and ext in MOOV_EXTS and not whole and size > MOOV_TAIL:
            tail = get(size - MOOV_TAIL, size - 1)
            _sparse(path, size, head, tail)
            row = _ffprobe(path)
            basis = 'container+moov_tail'
    finally:
        try:
            path.unlink()
        except OSError:
            pass
    if whole:
        basis = 'whole_file'
    elif ext in BITRATE_EXTS:
        basis = 'vbr_header' if any(tag in head for tag in (b'Xing', b'Info', b'VBRI')) else 'bitrate_extrapolated'
    if row.get('duration_s') is None:
        row['error'] = 'NO_DURATION'
    row['basis'] = basis
    return row, fetched


def probe_many(fetch_for, todo, out_path, scratch, threads, stop_at, progress=None):
    """Probe headers for (stratum, ref, item) tasks with a thread pool until stop_at; rows append to out_path. Returns (count, bytes)."""
    done = fetched_total = 0
    with out_path.open('a') as out, ThreadPoolExecutor(max_workers=threads) as pool:
        def task(entry):
            stratum, ref, item = entry
            try:
                row, fetched = probe_header(fetch_for(item), item, scratch)
            except Exception as exc:
                code = (getattr(exc, 'response', {}) or {}).get('Error', {}).get('Code') if hasattr(exc, 'response') else None
                row, fetched = {'error': (code or type(exc).__name__)[:60], 'basis': 'none'}, 0
            key, size, _e, modified, _s, kind = item
            row.update(ref=ref, stratum=stratum, kind=kind, ext=Path(key).suffix.lower(), size=size, modified=(modified or '')[:10], bytes_fetched=fetched)
            return row
        chunk = max(threads * 4, 32)
        for start in range(0, len(todo), chunk):
            if time.time() >= stop_at:
                break
            for row in pool.map(task, todo[start:start + chunk]):
                out.write(json.dumps(row, sort_keys=True) + '\n')
                done += 1
                fetched_total += row['bytes_fetched']
            out.flush()
            if progress:
                progress(done, fetched_total)
    return done, fetched_total


def headers(folder):
    """ref → newest header row of a store (a probe with a duration supersedes an earlier failure)."""
    by_ref = {}
    for path in sorted(Path(folder).glob('headers_*.jsonl')):
        try:
            with path.open() as handle:
                for line in handle:
                    try:
                        row = json.loads(line)
                    except ValueError:
                        continue
                    previous = by_ref.get(row['ref'])
                    if previous is None or previous.get('error') or not row.get('error'):
                        by_ref[row['ref']] = row
        except OSError:
            continue
    return by_ref


# ----------------------------------------------------------------------------------------------------------------- estimation
def _ratio(pairs, n_total):
    """Ratio estimator Σq/Σh over sampled files with Taylor-linearised standard error and finite-population correction."""
    n = len(pairs)
    sq, sh = sum(q for q, _ in pairs), sum(h for _, h in pairs)
    if n == 0 or sh <= 0:
        return 0.0, None
    r = sq / sh
    if n < 2:
        return r, None
    resid = sum((q - r * h) ** 2 for q, h in pairs) / (n - 1)
    fpc = max(0.0, 1 - n / max(n, n_total))
    return r, math.sqrt(fpc / n) * math.sqrt(resid) / (sh / n)


def stratum_stats(label, name, group, hdr, rows, settings, n_target, n_hdr_target, default_rate):
    """One stratum: Tier-1 hours (probed + extrapolated) and Tier-2 ratio estimates with standard errors (hours)."""
    from services.census_autonomy.deep_content import RETRY_ERRORS
    N = len(group)
    size_total = sum(t[2][1] for t in group)
    kinds = Counter(t[2][5] for t in group)
    probed = [(hdr[ref]['duration_s'], item[1]) for _, ref, item in group if ref in hdr and not hdr[ref].get('error')]
    basis = Counter(hdr[ref]['basis'] for _, ref, item in group if ref in hdr and not hdr[ref].get('error'))
    hdr_errors = sum(1 for _, ref, _i in group if ref in hdr and hdr[ref].get('error'))
    hdr_sec, hdr_bytes = sum(d for d, _ in probed), sum(b for _, b in probed)
    rate, se_rate = (_ratio(probed, N) if probed else (default_rate, None))
    unprobed = size_total - hdr_bytes
    # Hours are stated only where at least one header of the stratum was read; an unprobed stratum has unknown hours, not a guess.
    h_sec = (hdr_sec + unprobed * rate) if probed else None
    se_h = (unprobed * se_rate if (unprobed and se_rate is not None) else 0.0) if probed else None
    planned = group[:n_target]
    read = [(ref, rows[ref]) for _, ref, _i in planned if ref in rows and not rows[ref].get('error')]
    resolved = sum(1 for _, ref, _i in planned if ref in rows and (not rows[ref].get('error') or rows[ref]['error'] not in RETRY_ERRORS))
    n = len(read)
    h_of = lambda ref, row: (hdr[ref]['duration_s'] if ref in hdr and not hdr[ref].get('error') and hdr[ref].get('duration_s') else row['duration_s'])  # noqa: E731
    pairs = {'decoded': [], 'speech': [], 'music': [], 'silence': []}
    langs = defaultdict(list)
    codes = set()
    for ref, row in read:
        codes.update((row.get('by_language') or {}).keys())
    for ref, row in read:
        h = h_of(ref, row)
        pairs['decoded'].append((row['duration_s'], h))
        pairs['speech'].append((row['speech_windows'] * 2, h))
        pairs['music'].append((row['music_windows'] * 2, h))
        pairs['silence'].append((row['silence_windows'] * 2, h))
        by = row.get('by_language') or {}
        for code in codes:
            langs[code].append((by.get(code, 0) * 2, h))
    # A census is every file of the stratum read successfully; a stratum whose planned files all resolved (read, or failed for a
    # reason that will not change) is complete, and its unread files are estimated by ratio from the files that were read.
    census = N > 0 and n == N
    complete = resolved >= n_target > 0

    def estimate(p):
        if census:
            return {'est': round(sum(q for q, _ in p) / 3600, 3), 'se': 0.0}
        if not n or h_sec is None:
            return {'est': None, 'se': None}
        r, se_r = _ratio(p, N)
        var = (h_sec * (se_r or 0)) ** 2 + (r * se_h) ** 2
        return {'est': round(h_sec * r / 3600, 3), 'se': round(math.sqrt(var) / 3600, 3) if (se_r is not None) else None}
    est = {k: estimate(v) for k, v in pairs.items()}
    lang_est = {code: estimate(v) for code, v in langs.items()}
    lang_est = dict(sorted(lang_est.items(), key=lambda kv: -(kv[1]['est'] or 0))[:settings.get('languages_per_folder', 8)])
    speech_share_half = None
    if n >= 2 and not census:
        r, se_r = _ratio(pairs['speech'], N)
        speech_share_half = Z * se_r if se_r is not None else None
    bytes_read = sum(row['bytes_read'] for _, row in read)
    status = 'census' if census else 'sampled' if complete else 'reading' if resolved else 'planned' if n_target else 'unreadable'
    return {'label': label, 'folder': name, 'files': N, 'bytes': size_total, 'kinds': dict(kinds),
            'hours': {'est': round(h_sec / 3600, 2) if h_sec is not None else None, 'se': round(se_h / 3600, 2) if se_h is not None else None, 'probed_files': len(probed), 'probed_hours': round(hdr_sec / 3600, 2), 'probed_bytes': hdr_bytes,
                      'basis': dict(basis), 'header_errors': hdr_errors, 'seconds_per_mb': round(rate * 1e6, 2) if probed else None},
            'sample': {'target': n_target, 'read': n, 'resolved': resolved, 'bytes_read': bytes_read, 'hours_decoded': round(sum(q for q, _ in pairs['decoded']) / 3600, 2),
                       'header_target': n_hdr_target, 'speech_share_halfwidth': round(speech_share_half, 4) if speech_share_half is not None else None, 'status': status},
            'estimates': {**est, 'languages': lang_est}}


def plan_scope(scope, settings):
    """Sampling plan for every stratum of the host's scope. scope: {label: {'groups': {stratum: sorted [(key, ref, item)]}, 'headers': {...}, 'rows': {...}, 'access': state}}.
    Small folders are read in full; the rest share the file budget in proportion to the hours they hold (floor and cap per folder);
    folders whose speech-share interval is still wider than the target get a nested top-up within the top-up budget. Stores the key
    cannot read (denied, archived) take no budget: what can be read is sampled more deeply instead, and they are counted, not estimated."""
    budget, topup = int(settings['sample_files']), int(settings['sample_topup_files'])
    fmin, floor, cap, cap_topup = int(settings['folder_min']), int(settings['folder_floor']), int(settings['folder_cap']), int(settings['folder_cap_topup'])
    hdr_sample, target_half = int(settings['header_sample']), float(settings.get('target_halfwidth', 0.05))
    readable = lambda label: scope[label].get('access', 'readable') == 'readable'  # noqa: E731
    probed_sec = probed_bytes = 0
    for label, s in scope.items():
        for ref, h in s['headers'].items():
            if not h.get('error'):
                probed_sec += h['duration_s']
                probed_bytes += h['size']
    default_rate = probed_sec / probed_bytes if probed_bytes else DEFAULT_RATE
    strata = []
    for label, s in scope.items():
        for name, group in s['groups'].items():
            kinds = {t[2][5] for t in group}
            n_hdr = (len(group) if kinds == {'audio'} else min(len(group), max(hdr_sample, fmin))) if readable(label) else 0
            strata.append([label, name, group, n_hdr])
    weights = {}
    for label, name, group, _ in strata:
        hdr = scope[label]['headers']
        probed = [(hdr[ref]['duration_s'], item[1]) for _, ref, item in group if ref in hdr and not hdr[ref].get('error')]
        p_sec, p_bytes = sum(d for d, _ in probed), sum(b for _, b in probed)
        rate = p_sec / p_bytes if p_bytes else default_rate
        weights[(label, name)] = p_sec + (sum(item[1] for _, _, item in group) - p_bytes) * rate
    census_total = sum(len(g) for label, _, g, _ in strata if len(g) <= fmin and readable(label))
    remaining = max(0, budget - census_total)
    total_w = sum(w for (label, name), w in weights.items() if len(scope[label]['groups'][name]) > fmin and readable(label)) or 1.0
    targets = {}
    for label, name, group, _ in strata:
        N = len(group)
        targets[(label, name)] = 0 if not readable(label) else N if N <= fmin else min(N, max(floor, min(cap, round(remaining * weights[(label, name)] / total_w))))
    stats = {}
    for label, name, group, n_hdr in strata:
        n_hdr = max(n_hdr, targets[(label, name)])
        stats[(label, name)] = stratum_stats(label, name, group, scope[label]['headers'], scope[label]['rows'], settings, targets[(label, name)], n_hdr, default_rate)
    extra = 0
    for (label, name), st in sorted(stats.items(), key=lambda kv: -weights[kv[0]]):
        half = st['sample']['speech_share_halfwidth']
        share = weights[(label, name)] / (sum(w for (lab, _), w in weights.items() if readable(lab)) or 1)
        if half is not None and half > target_half and st['sample']['resolved'] >= targets[(label, name)] > 0 and targets[(label, name)] < st['files'] and share >= 0.005:
            new = min(st['files'], cap_topup, targets[(label, name)] * 2)
            if extra + (new - targets[(label, name)]) > topup:
                continue
            extra += new - targets[(label, name)]
            targets[(label, name)] = new
            group = scope[label]['groups'][name]
            stats[(label, name)] = stratum_stats(label, name, group, scope[label]['headers'], scope[label]['rows'], settings, new, max(n_hdr, new), default_rate)
    plan = {'budget_files': budget, 'topup_files': topup, 'topup_used': extra, 'census_files': census_total, 'default_seconds_per_mb': round(default_rate * 1e6, 2),
            'strata': len(strata), 'targets': {f'{label}|{name}': n for (label, name), n in targets.items()}}
    return plan, stats, {(label, name): max(n_hdr, targets[(label, name)]) for label, name, _g, n_hdr in strata}


def combine(parts):
    """Sum of independent stratum estimates: est adds, se adds in quadrature; None stays unknown only when nothing is estimated."""
    known = [p for p in parts if p and p.get('est') is not None]
    if not known:
        return {'est': None, 'se': None, 'lo': None, 'hi': None}
    est = sum(p['est'] for p in known)
    se = math.sqrt(sum((p['se'] or 0) ** 2 for p in known))
    return {'est': round(est, 2), 'se': round(se, 2), 'lo': round(max(0.0, est - Z * se), 2), 'hi': round(est + Z * se, 2), 'strata_estimated': len(known), 'strata_total': len(parts)}


def summarize_label(label, strata_stats, access, meta, items, rows, settings):
    """Store-level roll-up: Tier-1 facts, header coverage, the sample's progress, combined estimates and the folder table."""
    from services.census_autonomy.deep_content import RETRY_ERRORS
    sts = [st for (lab, _), st in strata_stats.items() if lab == label]
    read_rows = [r for r in rows.values() if not r.get('error')]
    failed = [r for r in rows.values() if r.get('error')]
    errors = Counter(r['error'] for r in failed)
    langs = defaultdict(list)
    for st in sts:
        for code, e in st['estimates']['languages'].items():
            langs[code].append(e)
    languages = {code: combine(parts) for code, parts in langs.items()}
    languages = dict(sorted(languages.items(), key=lambda kv: -(kv[1]['est'] or 0))[:16])
    measured_h = [st for st in sts if st['hours']['est'] is not None]
    hours_est = sum(st['hours']['est'] for st in measured_h) if measured_h else None
    hours_se = math.sqrt(sum((st['hours']['se'] or 0) ** 2 for st in measured_h)) if measured_h else None
    files_unmeasured = sum(st['files'] for st in sts if st['hours']['est'] is None)
    basis = Counter()
    for st in sts:
        basis.update(st['hours']['basis'])
    probed_files = sum(st['hours']['probed_files'] for st in sts)
    planned = sum(st['sample']['target'] for st in sts)
    read_in_sample = sum(st['sample']['read'] for st in sts)
    folders = sorted(sts, key=lambda st: -((st['estimates']['speech']['est'] or 0) if st['sample']['read'] else (st['hours']['est'] or 0)))
    limit = int(settings.get('folders_in_receipt', 120))
    shown, rest = folders[:limit], folders[limit:]
    if rest:
        rest_h = [s for s in rest if s['hours']['est'] is not None]
        shown.append({'label': label, 'folder': f'({len(rest)} further folders)', 'files': sum(s['files'] for s in rest), 'bytes': sum(s['bytes'] for s in rest), 'kinds': {},
                      'hours': {'est': round(sum(s['hours']['est'] for s in rest_h), 2) if rest_h else None, 'se': round(math.sqrt(sum((s['hours']['se'] or 0) ** 2 for s in rest_h)), 2) if rest_h else None,
                                'probed_files': sum(s['hours']['probed_files'] for s in rest), 'basis': {}},
                      'sample': {'target': sum(s['sample']['target'] for s in rest), 'read': sum(s['sample']['read'] for s in rest), 'resolved': sum(s['sample']['resolved'] for s in rest), 'status': 'merged'},
                      'estimates': {k: combine([s['estimates'][k] for s in rest]) for k in ('speech', 'music', 'silence', 'decoded')} | {'languages': {}}})
    for st in shown:
        for k in ('speech', 'music', 'silence', 'decoded'):
            e = st['estimates'][k]
            if e.get('est') is not None and e.get('se') is not None and 'lo' not in e:
                e['lo'], e['hi'] = round(max(0.0, e['est'] - Z * e['se']), 3), round(e['est'] + Z * e['se'], 3)
    media_bytes = sum(it[1] for it in items)
    sampled_complete = all(st['sample']['status'] in ('census', 'sampled') for st in sts) if sts else False
    headers_complete = all(st['hours']['probed_files'] + st['hours']['header_errors'] >= min(st['files'], st['sample']['header_target']) for st in sts) if sts else True
    if access['state'] in ('denied', 'archived'):
        measurement = access['state']
    elif not meta.get('complete'):
        measurement = 'listing'
    elif not items:
        measurement = 'no_media'
    elif sampled_complete and headers_complete:
        measurement = 'census' if all(st['sample']['status'] == 'census' for st in sts) else 'estimated'
    else:
        measurement = 'partial'
    pending = sum(max(0, st['sample']['target'] - st['sample']['read']) for st in sts) if access['state'] == 'readable' else 0
    return {
        'measurement': measurement, 'access': access['state'], 'access_probe': access.get('probed'), 'access_since': access.get('since'), 'inventory_complete': bool(meta.get('complete')), 'strata_mode': meta.get('strata_mode'),
        'media_objects': len(items), 'media_bytes': media_bytes, 'media_audio_objects': sum(1 for it in items if it[5] == 'audio'), 'media_video_objects': sum(1 for it in items if it[5] == 'video'),
        'files_hours_unmeasured': files_unmeasured,
        'objects_read': len(read_rows), 'bytes_read': sum(r['bytes_read'] for r in read_rows), 'bytes_verified': sum(r['bytes_read'] for r in read_rows if r.get('size_match') and r.get('etag_match') in (True, None)),
        'objects_failed': len(failed), 'failures': dict(errors), 'objects_pending': pending,
        'objects_denied': sum(1 for r in failed if r['error'] in ('AccessDenied', 'Forbidden')) if access['state'] != 'denied' else len(items),
        'bytes_denied': sum(r['size'] for r in failed if r['error'] in ('AccessDenied', 'Forbidden')) if access['state'] != 'denied' else media_bytes,
        'objects_archived': sum(1 for r in failed if r['error'] == 'InvalidObjectState') if access['state'] != 'archived' else len(items),
        'bytes_archived': sum(r['size'] for r in failed if r['error'] == 'InvalidObjectState') if access['state'] != 'archived' else media_bytes,
        'retryable_failures': sum(1 for r in failed if r['error'] in RETRY_ERRORS),
        'headers': {'probed_files': probed_files, 'probed_hours': round(sum(st['hours']['probed_hours'] for st in sts), 2), 'basis': dict(basis), 'errors': sum(st['hours']['header_errors'] for st in sts),
                    'hours_est': round(hours_est, 2) if hours_est is not None else None, 'hours_se': round(hours_se, 2) if hours_se is not None else None,
                    'hours_lo': round(max(0.0, hours_est - Z * hours_se), 2) if hours_est is not None else None, 'hours_hi': round(hours_est + Z * hours_se, 2) if hours_est is not None else None, 'complete': headers_complete},
        'sample': {'strata': len(sts), 'planned_files': planned, 'read_files': read_in_sample, 'census_strata': sum(1 for st in sts if st['sample']['status'] == 'census'),
                   'sampled_strata': sum(1 for st in sts if st['sample']['status'] in ('census', 'sampled')), 'hours_decoded': round(sum(st['sample']['hours_decoded'] for st in sts), 2), 'complete': sampled_complete},
        'estimates': {'speech': combine([st['estimates']['speech'] for st in sts]), 'music': combine([st['estimates']['music'] for st in sts]), 'silence': combine([st['estimates']['silence'] for st in sts]),
                      'decoded': combine([st['estimates']['decoded'] for st in sts]), 'languages': languages},
        'folders': shown,
        'hours_decoded': round(sum(r['duration_s'] for r in read_rows) / 3600, 3),
    }


def detections(source_id, label, summary, content):
    """Mtafiti: facts for bytes/counts/header durations, detections for model readings and interval estimates (confidence shrinks with the interval)."""
    from contracts.mtafiti_detection_signal import DetectionSignal, EvidenceClass
    from services.census_autonomy.deep_files import source_ref
    ref = source_ref(source_id, label)
    audio_version = f"audio-language:{(content.get('audio_model_sha256') or 'unpinned')[:16]}"
    music_version = f"music-detector:{(content.get('music_model_sha256') or 'unpinned')[:16]}"
    signals = []
    for name in ('media_objects', 'media_bytes', 'objects_read', 'bytes_read', 'bytes_verified', 'bytes_denied', 'bytes_archived'):
        signals.append(DetectionSignal(signal_name=f'content.{name}={summary[name]}', evidence_class=EvidenceClass.FACT, confidence=1.0, source_ref=ref, detector_version='byte-read:sha256+size+etag'))
    h = summary['headers']
    signals.append(DetectionSignal(signal_name=f"media_hours.header_probed={h['probed_hours']}", evidence_class=EvidenceClass.FACT, confidence=1.0, source_ref=ref, detector_version='ffprobe:head+tail-sparse'))
    if h['hours_est'] is not None:
        conf_h = 1.0 if not h['hours_est'] else max(0.0, min(1.0, 1 - Z * h['hours_se'] / h['hours_est']))
        signals.append(DetectionSignal(signal_name=f"media_hours.estimate={h['hours_est']}", evidence_class=EvidenceClass.DETECTED, confidence=conf_h, source_ref=ref, detector_version='ratio-estimator:seconds-per-byte'))

    def add(name, e, version):
        if e.get('est') is None:
            return
        conf = 1.0 if not e['est'] else max(0.0, min(1.0, 1 - (e['hi'] - e['lo']) / (2 * e['est'])))
        signals.append(DetectionSignal(signal_name=f'{name}={e["est"]}', evidence_class=EvidenceClass.DETECTED, confidence=conf, source_ref=ref, detector_version=version))
    add('media_composition.speech_hours', summary['estimates']['speech'], music_version)
    add('media_composition.music_hours', summary['estimates']['music'], music_version)
    for code, e in list(summary['estimates']['languages'].items())[:12]:
        add(f'language.{code}.speech_hours', e, audio_version)
    return [s.model_dump(mode='json') for s in signals]
