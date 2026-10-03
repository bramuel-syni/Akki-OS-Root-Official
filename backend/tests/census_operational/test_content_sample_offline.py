"""Offline tests of the tiered content census estimator (deep_sample) after the owner's 3 Oct direction: stores the key cannot read take no
sample budget and are counted, never estimated; a stratum is a census only when every file was read; shares not yet listed are `listing`;
hours are stated only where a header was probed. Synthetic items, no estate, no GPU."""
from services.census_autonomy import deep_sample as ds

SETTINGS = {'sample_files': 1000, 'sample_topup_files': 500, 'folder_min': 60, 'folder_floor': 30, 'folder_cap': 600, 'folder_cap_topup': 1500, 'header_sample': 300, 'target_halfwidth': 0.05}


def _items(n, prefix, kind='audio', size=5_000_000):
    return [(f'{prefix}/f{i}.{"mp3" if kind == "audio" else "mp4"}', size + i, f'e{i}', '2024-01-01T00:00:00', 'GLACIER', kind) for i in range(n)]


def _scope():
    scope = {}
    for label, access, n in (('readable-big', 'readable', 3000), ('denied-big', 'denied', 5000), ('small', 'readable', 10)):
        its = _items(n, 'folder')
        assign, _mode = ds.stratify(its, 160, 1500)
        groups = ds.grouped(label, its, assign)
        hdr = {ref: {'duration_s': 300.0, 'size': it[1], 'basis': 'container'} for g in groups.values() for _, ref, it in g[:50]} if access == 'readable' else {}
        rows = {}
        if access == 'readable':
            for g in groups.values():
                for _, ref, it in g[:5]:
                    rows[ref] = {'duration_s': 300.0, 'speech_windows': 100, 'music_windows': 40, 'silence_windows': 10, 'bytes_read': it[1], 'by_language': {'swa': 60, 'kik': 40}, 'size_match': True, 'etag_match': True}
        scope[label] = {'groups': groups, 'headers': hdr, 'rows': rows, 'access': access}
    return scope


def test_denied_stores_take_no_budget_and_readable_strata_absorb_it():
    scope = _scope()
    plan, stats, hdr_targets = ds.plan_scope(scope, SETTINGS)
    denied = {k: v for k, v in plan['targets'].items() if k.startswith('denied-big|')}
    assert denied and all(v == 0 for v in denied.values())
    assert all(v == 0 for (label, _), v in hdr_targets.items() if label == 'denied-big')
    readable = {k: v for k, v in plan['targets'].items() if k.startswith('readable-big|')}
    assert sum(readable.values()) == 600  # the per-folder cap, not a share diluted by the unreadable store
    assert plan['census_files'] == 10
    assert all(st['sample']['status'] == 'unreadable' for (label, _), st in stats.items() if label == 'denied-big')


def test_census_requires_every_file_read_else_ratio_estimate():
    scope = _scope()
    _plan, stats, _ = ds.plan_scope(scope, SETTINGS)
    small = next(st for (label, _), st in stats.items() if label == 'small')
    assert small['files'] == 10 and small['sample']['read'] == 5 and small['sample']['target'] == 10
    assert small['sample']['status'] == 'reading'
    assert small['estimates']['speech']['est'] is not None  # ratio from the five read files over the folder's header hours
    # every planned file resolved → complete, still not a census because two failed for a final reason
    label = 'small'
    group = next(iter(scope[label]['groups'].values()))
    for _, ref, it in group[5:8]:
        scope[label]['rows'][ref] = dict(next(iter(scope[label]['rows'].values())))
    for _, ref, it in group[8:]:
        scope[label]['rows'][ref] = {'error': 'DECODE_FAILED:no audio stream decoded', 'size': it[1]}
    _plan, stats, _ = ds.plan_scope(scope, SETTINGS)
    small = next(st for (lab, _), st in stats.items() if lab == 'small')
    assert small['sample']['status'] == 'sampled' and small['sample']['resolved'] == 10 and small['sample']['read'] == 8


def test_summarize_label_states():
    scope = _scope()
    _plan, stats, _ = ds.plan_scope(scope, SETTINGS)
    items = lambda label: [t[2] for g in scope[label]['groups'].values() for t in g]  # noqa: E731
    denied = ds.summarize_label('denied-big', stats, {'state': 'denied', 'probed': {'AccessDenied': 6}, 'since': '2026-10-02T17:50:00+00:00'}, {'complete': True}, items('denied-big'), {}, SETTINGS)
    assert denied['measurement'] == 'denied' and denied['headers']['hours_est'] is None and denied['estimates']['speech']['est'] is None
    assert denied['objects_denied'] == 5000 and denied['files_hours_unmeasured'] == 5000 and denied['access_since'] == '2026-10-02T17:50:00+00:00'
    assert not any(s['signal_name'].startswith('media_hours.estimate') for s in ds.detections('rms_obs', 'denied-big', denied, {}))
    unlisted = ds.summarize_label('channel01', stats, {'state': 'no_media', 'probed': None}, {'complete': False, 'objects': 0}, [], {}, SETTINGS)
    assert unlisted['measurement'] == 'listing'
    empty = ds.summarize_label('channel01', stats, {'state': 'no_media', 'probed': None}, {'complete': True, 'objects': 12}, [], {}, SETTINGS)
    assert empty['measurement'] == 'no_media'
    readable = ds.summarize_label('readable-big', stats, {'state': 'readable', 'probed': {'readable': 6}}, {'complete': True}, items('readable-big'), scope['readable-big']['rows'], SETTINGS)
    assert readable['measurement'] == 'partial' and readable['headers']['hours_est'] == 250.0 and readable['estimates']['speech']['est'] is not None
