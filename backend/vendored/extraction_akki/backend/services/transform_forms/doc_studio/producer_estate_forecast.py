"""Whole-estate forecast chapter of the estate pack (owner order 3 Oct 2026: "i need estimates of the whole estate … if x = m for the part we
read, what is m for the whole estate … Monte Carlo principles … lead with answers"). Reads `stores.content_forecast` (services.census_autonomy.
estate_forecast) and adds receipt R11, facts F130–F159, series S030–S032, tables T047–T050, claims C060–C068, the planning decision and the
plain-English terms. Forecast figures are the simulation medians; every table carries the 95 % forecast interval beside them."""
from __future__ import annotations

from typing import Any, Dict, List

from services.transform_forms.doc_studio.producer_estate_language import name_of

TIB = 2 ** 40
BASIS_WORDS = {'measured': 'read and judged', 'header_measured': 'hours measured on headers; content forecast', 'forecast_unsampled': 'readable, not yet sampled (forecast)',
               'forecast_denied': 'key refused (forecast)', 'forecast_archived': 'archive class (forecast)'}
CONVERTS = {'measured': 'nothing — measured', 'header_measured': 'finish the planned folder sample', 'forecast_unsampled': 'the running listing, probes and sample',
            'forecast_denied': 'one object-read grant to the census key', 'forecast_archived': 'an owner decision to restore sample files'}
ACCESS_WORDS = {'readable': 'readable', 'denied': 'key refused (403)', 'archived': 'archive · restore needed', 'no_media': 'no media'}


def _tib(value) -> float:
    return round((value or 0) / TIB, 2)


def _hours(value) -> float:
    return round(float(value or 0), 1)


def _iv(e: Dict[str, Any] | None) -> str:
    if not e or e.get('est') is None:
        return '—'
    return f"{e['est']:,.0f} ({e['lo']:,.0f}–{e['hi']:,.0f})"


def _langs(m: Dict[str, Any] | None, n: int = 3) -> str:
    ranked = sorted(((code, e) for code, e in (m or {}).items() if e and e.get('est')), key=lambda kv: -kv[1]['est'])
    return '; '.join(f"{name_of(code)} {e['est']:,.0f} h" for code, e in ranked[:n]) or '—'


def content(report: Dict[str, Any], receipts: Dict[str, Any], facts: Dict[str, Any], series: Dict[str, Any], calculations: Dict[str, Any], claims: Dict[str, Any],
            tables: Dict[str, Any], cannot_say: List[Dict[str, str]]) -> bool:
    fc = (report.get('stores') or {}).get('content_forecast')
    if not fc:
        cannot_say.append({'gap': 'A whole-estate forecast of hours, speech, music and languages', 'reason': 'no folder stratum has yet been read and judged, so there is no donor to scale from', 'closes_with': 'the first completed folder samples of the content census'})
        return False
    estate, basis, stores = fc['estate'], fc['by_basis'], fc['by_store']
    runs = sorted({r for s in ((report.get('stores') or {}).get('obs'), (report.get('stores') or {}).get('nas')) if s for r in (s.get('census_run_ids') or [])})
    receipts['R11'] = {'resolves_to': f"Whole-estate Monte Carlo forecast over the retained content-census receipts ({', '.join(runs[-4:])}): {fc['method']}", 'platform_ref': runs[-1] if runs else None}
    denied, unsampled, archived = basis.get('forecast_denied') or {}, basis.get('forecast_unsampled') or {}, basis.get('forecast_archived') or {}
    measured = basis.get('measured') or {}
    top_source = fc['sources'][0] if fc.get('sources') else None
    f: Dict[str, Any] = {
        'F130': {'label': 'Whole estate: hours of media held (forecast, every listed folder)', 'value': _hours(estate['hours']['est']), 'unit': 'hours', 'class': 'estimated', 'receipt': 'R11',
                 'measurement_scope': f"95 % forecast interval {estate['hours']['lo']:,.0f}–{estate['hours']['hi']:,.0f} h; median of {fc['simulations']:,} simulations over {fc['strata']:,} folder strata"},
        'F131': {'label': 'Whole estate: speech hours (forecast)', 'value': _hours(estate['speech']['est']), 'unit': 'hours', 'class': 'estimated', 'receipt': 'R11', 'measurement_scope': f"95 % forecast interval {estate['speech']['lo']:,.0f}–{estate['speech']['hi']:,.0f} h"},
        'F132': {'label': 'Whole estate: music hours (forecast)', 'value': _hours(estate['music']['est']), 'unit': 'hours', 'class': 'estimated', 'receipt': 'R11', 'measurement_scope': f"95 % forecast interval {estate['music']['lo']:,.0f}–{estate['music']['hi']:,.0f} h"},
        'F133': {'label': 'Share of the forecast hours that rest on files read and judged', 'value': fc['measured_share_of_hours'], 'unit': 'pct', 'class': 'measured', 'receipt': 'R11'},
        'F134': {'label': 'Share of the forecast hours sitting in buckets the census key cannot read', 'value': round((denied.get('hours') or {}).get('est', 0) / estate['hours']['est'], 4) if estate['hours']['est'] else 0.0, 'unit': 'pct', 'class': 'estimated', 'receipt': 'R11'},
        'F142': {'label': 'Folder strata in the simulation (every listed folder of every store)', 'value': fc['strata'], 'unit': 'strata', 'class': 'measured', 'receipt': 'R11'},
        'F143': {'label': 'Donor strata read and judged', 'value': fc['donors']['strata'], 'unit': 'strata', 'class': 'measured', 'receipt': 'R11'},
        'F144': {'label': 'Files read byte for byte behind the donors', 'value': fc['donors']['files_read'], 'unit': 'files', 'class': 'measured', 'receipt': 'R11'},
        'F145': {'label': 'Simulations run', 'value': fc['simulations'], 'unit': 'simulations', 'class': 'measured', 'receipt': 'R11'},
        'F148': {'label': 'Width of the 95 % forecast interval on estate hours', 'value': _hours(estate['hours']['hi'] - estate['hours']['lo']), 'unit': 'hours', 'class': 'estimated', 'receipt': 'R11'},
    }
    if stores.get('obs'):
        f['F135'] = {'label': 'Object store: hours held (forecast)', 'value': _hours(stores['obs']['hours']['est']), 'unit': 'hours', 'class': 'estimated', 'receipt': 'R11', 'measurement_scope': f"95 % forecast interval {_iv(stores['obs']['hours'])}"}
        f['F136'] = {'label': 'Object store: speech hours (forecast)', 'value': _hours(stores['obs']['speech']['est']), 'unit': 'hours', 'class': 'estimated', 'receipt': 'R11', 'measurement_scope': f"95 % forecast interval {_iv(stores['obs']['speech'])}"}
    if stores.get('nas'):
        f['F137'] = {'label': 'File shares: hours held (forecast)', 'value': _hours(stores['nas']['hours']['est']), 'unit': 'hours', 'class': 'estimated', 'receipt': 'R11', 'measurement_scope': f"95 % forecast interval {_iv(stores['nas']['hours'])}"}
        f['F138'] = {'label': 'File shares: speech hours (forecast)', 'value': _hours(stores['nas']['speech']['est']), 'unit': 'hours', 'class': 'estimated', 'receipt': 'R11', 'measurement_scope': f"95 % forecast interval {_iv(stores['nas']['speech'])}"}
    if denied:
        f['F139'] = {'label': 'Hours in the buckets the key cannot read (forecast)', 'value': _hours(denied['hours']['est']), 'unit': 'hours', 'class': 'estimated', 'receipt': 'R11', 'measurement_scope': f"95 % forecast interval {_iv(denied['hours'])}; {denied['files']:,} files, {_tib(denied['bytes'])} TiB"}
        f['F140'] = {'label': 'Speech hours in the buckets the key cannot read (forecast)', 'value': _hours(denied['speech']['est']), 'unit': 'hours', 'class': 'estimated', 'receipt': 'R11', 'measurement_scope': f"95 % forecast interval {_iv(denied['speech'])}"}
    if unsampled:
        f['F141'] = {'label': 'Hours in readable folders not yet sampled (forecast)', 'value': _hours(unsampled['hours']['est']), 'unit': 'hours', 'class': 'estimated', 'receipt': 'R11', 'measurement_scope': f"95 % forecast interval {_iv(unsampled['hours'])}; {unsampled['files']:,} files"}
    if measured:
        f['F147'] = {'label': 'Hours measured directly (folders read and judged)', 'value': _hours(measured['hours']['est']), 'unit': 'hours', 'class': 'estimated', 'receipt': 'R11', 'measurement_scope': f"95 % interval {_iv(measured['hours'])}; {measured['files']:,} files in {measured['strata']:,} strata"}
    if top_source:
        f['F146'] = {'label': f"Hours forecast in the single largest bucket ({top_source['label']})", 'value': _hours(top_source['hours']['est']), 'unit': 'hours', 'class': 'estimated', 'receipt': 'R11',
                     'measurement_scope': f"95 % forecast interval {_iv(top_source['hours'])}; {top_source['files']:,} files, {_tib(top_source['bytes'])} TiB, {ACCESS_WORDS.get(top_source['access'], top_source['access'])}"}
    lang_ids = []
    for i, (code, e) in enumerate(list(estate['languages'].items())[:8]):
        fid = f'F15{i}'
        f[fid] = {'label': f'{name_of(code)} speech hours, whole estate (forecast)', 'value': _hours(e['est']), 'unit': 'hours', 'class': 'estimated', 'receipt': 'R11', 'measurement_scope': f"95 % forecast interval {e['lo']:,.0f}–{e['hi']:,.0f} h"}
        lang_ids.append(fid)
    facts.update(f)
    calculations['K030'] = {'label': 'Speech share of the estate\'s hours (forecast)', 'formula': 'F131 / F130', 'inputs': ['F130', 'F131'], 'unit': 'pct'}
    calculations['K031'] = {'label': 'Music share of the estate\'s hours (forecast)', 'formula': 'F132 / F130', 'inputs': ['F130', 'F132'], 'unit': 'pct'}
    calculations['K032'] = {'label': 'Interval width as a share of the estate forecast', 'formula': 'F148 / F130', 'inputs': ['F130', 'F148'], 'unit': 'pct'}
    if 'F146' in facts:
        calculations['K033'] = {'label': 'Largest bucket\'s share of the estate\'s forecast hours', 'formula': 'F146 / F130', 'inputs': ['F130', 'F146'], 'unit': 'pct'}
    if 'F147' in facts:
        calculations['K034'] = {'label': 'Forecast hours per hour measured directly', 'formula': 'F130 / F147', 'inputs': ['F130', 'F147'], 'unit': 'ratio'}
    series['S030'] = {'label': 'Whole-estate hours by evidence basis (forecast medians)', 'categories': [BASIS_WORDS[b] for b in basis], 'values': {'Hours': [_hours(v['hours']['est']) for v in basis.values()]}, 'unit': 'hours', 'class': 'estimated', 'receipt': 'R11'}
    series['S031'] = {'label': 'Speech hours by language, whole estate (forecast medians)', 'categories': [name_of(c) for c in estate['languages']], 'values': {'Hours': [_hours(e['est']) for e in estate['languages'].values()]}, 'unit': 'hours', 'class': 'estimated', 'receipt': 'R11'}
    top = fc['sources'][:10]
    series['S032'] = {'label': 'Forecast hours by bucket and share, largest ten', 'categories': [f"{s['label']}{' (refused)' if s['access'] == 'denied' else ''}" for s in top], 'values': {'Hours': [_hours(s['hours']['est']) for s in top]}, 'unit': 'hours', 'class': 'estimated', 'receipt': 'R11'}
    _tables(fc, tables)
    claims.update({
        'C060': {'text': 'Scaling what was read to every listed folder, the whole estate holds about {F130} hours of media: {F131} hours of speech and {F132} hours of music', 'supports': ['F130', 'F131', 'F132']},
        'C061': {'text': '{F133} of the forecast hours rest on files read and judged; {F134} sit in buckets the census key is refused on, where the forecast is widest and one access grant turns it into measurement', 'supports': ['F133', 'F134']},
        'C065': {'text': 'The forecast rests on {F143} folder strata read and judged ({F144} files read byte for byte), replayed in {F145} simulations over {F142} folder strata', 'supports': ['F142', 'F143', 'F144', 'F145']},
        'C066': {'text': 'Speech is {K030} of the estate\'s hours and music {K031}; the 95 % interval on the estate total spans {F148} hours ({K032} of the forecast)', 'supports': ['F130', 'F131', 'F132', 'F148']},
    })
    if lang_ids:
        names = [name_of(c) for c in estate['languages']]
        claims['C062'] = {'text': f"By language the estate is forecast to hold {{{lang_ids[0]}}} hours of {names[0]} speech" + (f", {{{lang_ids[1]}}} of {names[1]}" if len(lang_ids) > 1 else '') + (f" and {{{lang_ids[2]}}} of {names[2]}" if len(lang_ids) > 2 else ''), 'supports': lang_ids[:3]}
    if 'F135' in facts and 'F137' in facts:
        claims['C063'] = {'text': 'The object store accounts for {F135} hours ({F136} speech) and the file shares for {F137} hours ({F138} speech)', 'supports': ['F135', 'F136', 'F137', 'F138']}
    if 'F146' in facts and top_source:
        claims['C064'] = {'text': f"One bucket, {top_source['label']}, carries {{F146}} forecast hours — {{K033}} of the estate — and is {ACCESS_WORDS.get(top_source['access'], top_source['access'])}", 'supports': ['F146', 'F130']}
    if 'F147' in facts:
        claims['C067'] = {'text': 'Every hour measured directly stands for {K034} hours of the whole-estate forecast', 'supports': ['F130', 'F147']}
    cannot_say.append({'gap': 'That refused buckets resemble the readable folders standing in for them',
                       'reason': 'forecast rows borrow seconds per megabyte, speech share and language mix from readable folders of the same media kind and file size',
                       'closes_with': 'the object-read grant: measured rows then replace forecast rows'})
    return True


def _tables(fc: Dict[str, Any], tables: Dict[str, Any]) -> None:
    rows = []
    for s in fc['sources']:
        rows.append(['OBS' if s['store'] == 'obs' else 'NAS', s['label'], ACCESS_WORDS.get(s['access'], s['access']), {'measured': 'measured', 'forecast': 'forecast', 'mixed': 'part measured, part forecast'}[s['basis']],
                     f"{s['files']:,}", _tib(s['bytes']), _iv(s['hours']), _iv(s['speech']), _iv(s['music']), _langs(s['languages']),
                     'nothing — measured' if s['basis'] == 'measured' else CONVERTS['forecast_denied'] if s['access'] == 'denied' else CONVERTS['forecast_archived'] if s['access'] == 'archived' else CONVERTS['forecast_unsampled']])
    tables['T047'] = {'label': 'Whole-estate forecast by bucket and share — hours, speech, music and languages with 95 % forecast intervals (largest first)', 'class': 'estimated', 'receipt': 'R11', 'right_align_from': 4,
                      'note': 'Every listed bucket and share, measured or forecast, so the estate adds up. Parentheses are 95 % forecast intervals from the simulation; a measured row\'s interval is its sampling interval. Forecast rows borrow from readable folders of the same media kind and file size and are replaced by measurement as soon as the store can be read.',
                      'columns': ['Store', 'Bucket / share', 'Access', 'Basis', 'Media files', 'Media bytes (TiB)', 'Hours (95 %)', 'Speech hours (95 %)', 'Music hours (95 %)', 'Top languages (speech hours)', 'What converts the forecast into measurement'],
                      'deck_columns': ['Bucket / share', 'Access', 'Basis', 'Media files', 'Hours (95 %)', 'Speech hours (95 %)', 'Top languages (speech hours)'], 'rows': rows}
    tables['T050'] = {'label': 'Whole estate by evidence basis — how much is measured and how much is forecast', 'class': 'estimated', 'receipt': 'R11', 'right_align_from': 2,
                      'note': 'Read-and-judged strata are measured; everything else is forecast from them. The rows add up to the whole estate; the last column names the one step that turns each forecast row into a measured one.',
                      'columns': ['Evidence basis', 'Folder strata', 'Media files', 'Media bytes (TiB)', 'Hours (95 %)', 'Speech hours (95 %)', 'Music hours (95 %)', 'What converts it into measurement'],
                      'deck_columns': ['Evidence basis', 'Folder strata', 'Media files', 'Hours (95 %)', 'Speech hours (95 %)', 'What converts it into measurement'],
                      'rows': [[BASIS_WORDS[b], f"{v['strata']:,}", f"{v['files']:,}", _tib(v['bytes']), _iv(v['hours']), _iv(v['speech']), _iv(v['music']), CONVERTS[b]] for b, v in fc['by_basis'].items()]}
    folders = fc['folders'][:60]
    tables['T048'] = {'label': 'Folder-level forecast — the largest folders of the estate with 95 % forecast intervals (ranked by forecast hours)', 'class': 'estimated', 'receipt': 'R11', 'right_align_from': 3,
                      'note': 'Each row is one folder stratum with its listed population scaled by the sample. Measured folders carry their own sample; forecast folders name the donor folder that most often stood in for them in the simulation.',
                      'columns': ['Bucket / share', 'Folder', 'Kind', 'Files', 'Bytes (TiB)', 'Basis', 'Hours (95 %)', 'Speech hours (95 %)', 'Music hours (95 %)', 'Leading language (speech hours)', 'Donor folder (forecast rows)'],
                      'deck_columns': ['Bucket / share', 'Folder', 'Files', 'Basis', 'Hours (95 %)', 'Speech hours (95 %)', 'Leading language (speech hours)'],
                      'rows': [[fo['label'], fo['folder'], fo['kind'], f"{fo['files']:,}", _tib(fo['bytes']), BASIS_WORDS[fo['basis']], _iv(fo['hours']), _iv(fo['speech']), _iv(fo['music']),
                                f"{name_of(fo['top_language'])} {fo['top_language_hours']['est']:,.0f} h" if fo.get('top_language') else '—', fo.get('donor') or '—'] for fo in folders]}
    kinds = fc['donors']['by_kind']
    tables['T049'] = {'label': 'How the forecast was built — the donor folders by media kind', 'class': 'measured', 'receipt': 'R11', 'right_align_from': 1,
                      'note': fc['method'],
                      'columns': ['Media kind', 'Donor strata', 'Donor files', 'Seconds per MB (10th–90th pct)', 'Speech share (10th–90th pct)'],
                      'rows': [[k, f"{v['strata']:,}", f"{v['files']:,}", f"{v['seconds_per_mb_p10_p90'][0]:,.2f}–{v['seconds_per_mb_p10_p90'][1]:,.2f}" if v.get('seconds_per_mb_p10_p90') else '—',
                                f"{v['speech_share_p10_p90'][0]:.1%}–{v['speech_share_p10_p90'][1]:.1%}" if v.get('speech_share_p10_p90') else '—'] for k, v in kinds.items() if v['strata']]}


def decisions(report: Dict[str, Any], tables: Dict[str, Any]) -> None:
    """Puts the forecast decision first: adopt it as the planning baseline and convert its widest rows into measurement."""
    fc = (report.get('stores') or {}).get('content_forecast')
    t013 = tables.get('T013')
    if not fc or not t013:
        return
    widest = sorted((s for s in fc['sources'] if s['basis'] != 'measured'), key=lambda s: -(s['hours']['hi'] - s['hours']['lo']))[:3]
    estate = fc['estate']
    t013['rows'].insert(0, ['D0', 'Adopt the whole-estate forecast as the planning baseline for hours, speech and languages',
                            f"every listed folder of the object store and the file shares ({fc['strata']:,} strata; {estate['hours']['est']:,.0f} h, 95 % {estate['hours']['lo']:,.0f}–{estate['hours']['hi']:,.0f} h)",
                            'plan products, storage and compute on the forecast medians; convert the widest forecast rows into measurement in the order of their interval width: ' + ', '.join(f"{s['label']} ({s['hours']['hi'] - s['hours']['lo']:,.0f} h wide)" for s in widest),
                            'forecast replaced by measurement bucket by bucket; no data moves (proposed)', 'Head of Data with the cloud account owner',
                            'one defensible number for the estate today, narrowing every census run', 'R11 · T047 · T050', 'that each converted bucket lands inside its forecast interval; a miss means the donors did not represent it'])


GLOSSARY = [
    {'term': 'Whole-estate forecast', 'meaning': 'What the entire estate most likely holds, found by scaling what the census read in each folder up to that folder\'s full population and adding every folder together — the part that could not be read included, each one standing in for a readable folder of the same kind and file size.'},
    {'term': 'Monte Carlo simulation', 'meaning': 'The estate was added up thousands of times, each time letting every uncertain folder take a different plausible value. The middle result is the forecast; the range that holds 95 % of the results is the forecast interval.'},
    {'term': 'Donor folder', 'meaning': 'A folder the census read and judged that stands in for a folder it could not read: same media kind, similar file size. Its seconds per megabyte, speech share and language mix are borrowed, so the forecast is only as representative as its donors.'},
    {'term': 'Forecast versus measured', 'meaning': 'Measured rows come from files actually read and judged, with a sampling interval. Forecast rows are borrowed from donors and carry a wider interval. Every table says which is which; an access grant or a finished sample turns a forecast row into a measured one.'},
]
