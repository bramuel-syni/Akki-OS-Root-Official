"""Control-plane record of the text-estate evidence job (owner order 2026-10-02): aggregate-only reads of the written-word
stores — the hourly radio news scripts (news_vault.stories → hours → stations) and the transcription workbench (local.transcripts,
uploaded_files, folder_languages) — through the same pinned seam as the estate census. Station names are business labels;
no script, transcript or person value is selected."""
import json
from collections import defaultdict

from services.census_autonomy import estate_intelligence_dispatch as eid
from services.training_lab import store as lab

OWNER_ORDER_REF = ('owner order 2026-10-02: evidence for the written news scripts per language per hour held in the database, and the text held per language; '
                   'aggregates only; no training')
TARGETS = [{'connection_label': 'Razuna (Library Content) & Newsvault (Radio News content)', 'database': 'news_vault', 'query_set': 'news_vault'},
           {'connection_label': 'citizen_digital', 'database': 'local', 'query_set': 'local'}]
PROFILE_TARGETS = [{**t, 'mode': 'text_profiles'} for t in TARGETS]
PROFILE_ORDER_REF = ('owner order 2026-10-03: each station carries a name and a script that identify its language; character-trigram profiles of the scripts '
                     'per station and of the workbench transcripts per language, compared; no text retained')
LOCATION_TARGETS = [{'connection_label': 'citizen_digital', 'database': 'local', 'query_set': 'local_media_locations'}]
LOCATION_ORDER_REF = 'owner order 2026-10-03: retrain the language model for the six unmodelled languages — where the workbench\'s labelled recordings live, per language (hosts and path roots only)'
KINDS = {'aggregates': (TARGETS, OWNER_ORDER_REF), 'profiles': (PROFILE_TARGETS, PROFILE_ORDER_REF), 'locations': (LOCATION_TARGETS, LOCATION_ORDER_REF)}
NEWS_RECEIPT = 'news_vault.stories (script, title, date, hour_id) → news_vault.hours (station_id, time, type_id) → news_vault.stations (name); news_vault.news (2022 bulletins)'
LOCAL_RECEIPT = 'local.uploaded_files (language_id, audio_length, status) ← local.transcripts (file_id, start_time, end_time, transcript) ; local.folder_languages (Language, code, station)'


def db():
    database = lab.db()
    database.training_lab_text_estate.create_index([('tenant_id', 1), ('submitted_at', -1)])
    return database


def latest(tenant, kind='aggregates'):
    query = {'tenant_id': tenant, 'kind': kind} if kind != 'aggregates' else {'tenant_id': tenant, 'kind': {'$in': [None, 'aggregates']}}
    return db().training_lab_text_estate.find_one(query, {'_id': 0}, sort=[('submitted_at', -1)])


def dispatch(actor, kind='aggregates'):
    from services.census_autonomy.operational_runner import admission_path
    targets, order_ref = KINDS[kind]
    current = latest(actor['tenant_id'], kind)
    if current and current['status'] in ('submitting', 'running'): raise ValueError('A text-estate evidence job is already running')
    lawful, _ = admission_path()
    job = eid.submit('rms_mysql', {'targets': targets, 'max_seconds': 3600, 'database_seconds': 900}, actor['principal_id'], str(lawful), phase='text_estate')
    doc = {'text_estate_id': 'te-' + job['job_id'].split('-', 1)[1], 'tenant_id': actor['tenant_id'], 'actor': actor['principal_id'], 'job_id': job['job_id'], 'host': job['host'],
           'phase': 'text_estate', 'kind': kind, 'targets': targets, 'owner_order_ref': order_ref, 'submitted_at': lab.now(), 'updated_at': lab.now(),
           'status': 'running' if job['status'] == 'running' else 'failed', **({'reason': job.get('reason')} if job['status'] != 'running' else {})}
    db().training_lab_text_estate.insert_one(dict(doc))
    return {k: v for k, v in doc.items() if k != 'actor'}


def refresh(doc):
    if not doc or doc['status'] != 'running': return doc
    job = eid.refresh(doc['job_id'])
    fields = {'updated_at': lab.now(), 'progress': ((job or {}).get('remote_state') or {}).get('progress')}
    if job and job['status'] == 'running': pass
    elif job and job['status'] in ('completed', 'partial') and (job.get('receipt') or {}).get('digest_verified'):
        try:
            detail = eid.fetch_detail(doc['job_id'])
            summary = summarise_profiles(detail) if doc.get('kind') == 'profiles' else summarise_locations(detail) if doc.get('kind') == 'locations' else summarise(detail)
            fields.update(status='completed', result=job['receipt']['result'], receipt_sha256=job['receipt']['receipt_sha256'], finished_at=job.get('finished_at'),
                          summary=summary, detail_sha256=job['receipt']['result']['detail_sha256'])
        except Exception as exc:
            fields.update(status='failed', reason=f'Aggregates could not be retrieved: {type(exc).__name__}')
    else:
        fields.update(status='failed', reason=((job or {}).get('receipt') or {}).get('error', {}).get('message') or (job or {}).get('reason') or 'Worker did not produce a verified terminal receipt')
    db().training_lab_text_estate.update_one({'text_estate_id': doc['text_estate_id']}, {'$set': fields})
    return {**doc, **fields}


def detail(tenant):
    doc = latest(tenant)
    if not doc or doc['status'] != 'completed': return doc, None
    return doc, eid.fetch_detail(doc['job_id'])


def resummarise(tenant, kind='profiles'):
    """Re-reads the retained aggregates of the latest completed job of a kind and rewrites its summary (after a summariser change)."""
    doc = latest(tenant, kind)
    if not doc or doc['status'] != 'completed': return doc
    detail_ = eid.fetch_detail(doc['job_id'])
    summary = summarise_profiles(detail_) if kind == 'profiles' else summarise(detail_)
    db().training_lab_text_estate.update_one({'text_estate_id': doc['text_estate_id']}, {'$set': {'summary': summary, 'updated_at': lab.now()}})
    return {**doc, 'summary': summary}


def _n(value):
    """Aggregates arrive as int, float or (from SUM/AVG over the seam) numeric strings; never let a string reach arithmetic."""
    if value is None or isinstance(value, (int, float)): return value or 0
    try: return int(value)
    except (TypeError, ValueError):
        try: return float(value)
        except (TypeError, ValueError): return 0


def _target(detail_, database):
    return next((t for t in (detail_ or {}).get('targets', []) if t['database'] == database), None)


def summarise(detail_):
    """Plain aggregates the report and workbook consume: per station (language) script counts, dates, hour slots, gaps; per-language text."""
    out = {'news_scripts': None, 'transcription_workbench': None}
    news = _target(detail_, 'news_vault')
    if news and isinstance(news['results'].get('scripts_by_station_date'), list):
        r = news['results']
        stations = {row[0]: row[1] for row in r.get('stations', []) if isinstance(r.get('stations'), list)}
        hours = {row[0]: {'station_id': row[1], 'type_id': row[2], 'time': row[3], 'deleted': bool(row[4])} for row in r.get('hours', [])} if isinstance(r.get('hours'), list) else {}
        slots_per_station = defaultdict(set)
        for h in hours.values():
            if not h['deleted'] and h['station_id'] is not None: slots_per_station[h['station_id']].add(h['time'])
        per_station = {}
        for station_id, date, scripts, hour_ids, chars, deleted, top_level in r['scripts_by_station_date']:
            scripts, hour_ids, chars, deleted = _n(scripts), _n(hour_ids), _n(chars), _n(deleted)
            name = stations.get(station_id) or ('unassigned hour' if station_id is None else f'station #{station_id}')
            p = per_station.setdefault(name, {'station_id': station_id, 'scripts': 0, 'live_scripts': 0, 'deleted_scripts': 0, 'chars': 0, 'dates': 0, 'first_date': None, 'last_date': None,
                                              'hour_ids_max_on_a_day': 0, 'days_with_24_slots': 0, 'slots_configured': len(slots_per_station.get(station_id, ())), 'scripts_by_date': []})
            p['scripts'] += scripts; p['deleted_scripts'] += deleted; p['live_scripts'] += scripts - deleted; p['chars'] += chars; p['dates'] += 1
            p['first_date'] = min(p['first_date'] or date, date); p['last_date'] = max(p['last_date'] or date, date)
            p['hour_ids_max_on_a_day'] = max(p['hour_ids_max_on_a_day'], hour_ids)
            if hour_ids >= 24: p['days_with_24_slots'] += 1
            p['scripts_by_date'].append([date, scripts, hour_ids, chars, deleted])
        for name, p in per_station.items():
            p['scripts_by_date'].sort()
            p['mean_scripts_per_day'] = round(p['scripts'] / p['dates'], 2) if p['dates'] else None
            p['mean_distinct_hours_per_day'] = round(sum(d[2] for d in p['scripts_by_date']) / p['dates'], 2) if p['dates'] else None
        slots = defaultdict(list)
        if isinstance(r.get('scripts_by_station_slot'), list):
            for station_id, slot, scripts, dates in r['scripts_by_station_slot']:
                slots[stations.get(station_id) or ('unassigned hour' if station_id is None else f'station #{station_id}')].append({'slot': slot, 'scripts': _n(scripts), 'dates': _n(dates)})
        overall = r.get('scripts_overall')
        o = [(_n(v) if i not in (2, 3) else v) for i, v in enumerate(overall[0])] if isinstance(overall, list) and overall else None
        distinct = r.get('scripts_distinct')
        out['news_scripts'] = {
            'receipt': NEWS_RECEIPT, 'stations': sorted(stations.values()), 'station_count': len(stations), 'types': [row[1] for row in r.get('types', [])] if isinstance(r.get('types'), list) else [],
            'overall': {'scripts': o[0], 'deleted': o[1], 'first_date': o[2], 'last_date': o[3], 'dates_with_scripts': o[4], 'chars': o[5], 'min_chars': o[6], 'max_chars': o[7],
                        'mean_chars': round(float(o[8]), 1) if o[8] is not None else None, 'empty_scripts': o[9], 'revisions_of_a_parent': o[10], 'correspondents': o[11],
                        'distinct_script_texts': distinct[0][0] if isinstance(distinct, list) and distinct else None} if o else None,
            'per_station': {k: {kk: vv for kk, vv in v.items() if kk != 'scripts_by_date'} for k, v in per_station.items()},
            'by_station_date': {k: v['scripts_by_date'] for k, v in per_station.items()}, 'slots_by_station': dict(slots),
            'news_2022': {'dates': len(r['news_by_date']), 'bulletins': sum(_n(x[1]) for x in r['news_by_date']), 'chars': sum(_n(x[2]) for x in r['news_by_date'])} if isinstance(r.get('news_by_date'), list) else None,
            'uploads_by_month': r.get('uploads_by_month') if isinstance(r.get('uploads_by_month'), list) else None,
            'query_errors': {k: v for k, v in r.items() if isinstance(v, dict)}}
    local = _target(detail_, 'local')
    if local:
        r = local['results']
        folders = defaultdict(lambda: {'folders': 0, 'codes': set(), 'stations': set()})
        if isinstance(r.get('folder_languages'), list):
            for language, code, station, count in r['folder_languages']:
                f = folders[language or 'unlabelled']; f['folders'] += count; f['codes'].add(code); f['stations'].add(station)
        ids = {str(row[0]): {'language': row[1], 'code': row[2], 'station': row[3]} for row in r['folder_language_ids']} if isinstance(r.get('folder_language_ids'), list) else {}
        files = {row[0]: {**ids.get(str(row[0]), {'language': None, 'code': None, 'station': None}), 'files': _n(row[1]), 'audio_seconds': float(_n(row[2])), 'transcribe_uploaded': _n(row[3]), 'with_text_file': _n(row[4]), 'first_processed': row[5], 'last_processed': row[6]}
                 for row in r['files_by_language']} if isinstance(r.get('files_by_language'), list) else {}
        transcripts = {row[0]: {**ids.get(str(row[0]), {'language': None, 'code': None, 'station': None}), 'segments': _n(row[1]), 'chars': _n(row[2]), 'files': _n(row[3]), 'speech_seconds': float(_n(row[4]))} for row in r['transcripts_by_language']} if isinstance(r.get('transcripts_by_language'), list) else {}
        t = r.get('transcripts_overall'); t = [(_n(v) if i < 5 else v) for i, v in enumerate(t[0])] if isinstance(t, list) and t else None
        out['transcription_workbench'] = {
            'receipt': LOCAL_RECEIPT,
            'folder_languages': {k: {'folders': v['folders'], 'codes': sorted(c for c in v['codes'] if c), 'stations': sorted(s for s in v['stations'] if s)} for k, v in folders.items()},
            'files_by_language': files, 'transcripts_by_language': transcripts,
            'files_by_status': {row[0]: _n(row[1]) for row in r['files_by_status']} if isinstance(r.get('files_by_status'), list) else None,
            'transcripts_overall': {'segments': t[0], 'deleted': t[1], 'chars': t[2], 'files': t[3], 'speakers': t[4], 'first': t[5], 'last': t[6]} if t else None,
            'speakers': r['speakers'][0][0] if isinstance(r.get('speakers'), list) and r['speakers'] else None,
            'query_errors': {k: v for k, v in r.items() if isinstance(v, dict)}}
    out['errors'] = (detail_ or {}).get('errors', [])
    return json.loads(json.dumps(out, default=str))


# ----------------------------------------------------------------------------- script language profiles → station language register
ENGLISH_STATIONS = {'hot 96': ('English', 'eng')}  # declared by the station itself; no workbench folder carries English


def _vector(profile):
    total = float(profile.get('trigram_total') or sum(profile['trigrams'].values()) or 1)
    return {g: c / total for g, c in profile['trigrams'].items()}


def _cosine(a, b):
    import math
    dot = sum(v * b[g] for g, v in a.items() if g in b)
    na, nb = math.sqrt(sum(v * v for v in a.values())), math.sqrt(sum(v * v for v in b.values()))
    return round(dot / (na * nb), 4) if na and nb else 0.0


def _station_key(name):
    return (name or '').lower().replace('radio ', '').replace(' fm', '').strip()


def summarise_profiles(detail_):
    """Each news station's script profile against every workbench language profile (transcripts): nearest language, margin to the second,
    the station's declared language from the workbench register, and the verdict. Station-to-station similarity shows which stations write
    the same language and how far the unmodelled languages (Meru, Embu, Bukusu, Maragoli) sit from their modelled relatives."""
    news, local = _target(detail_, 'news_vault'), _target(detail_, 'local')
    out = {'stations': [], 'languages': {}, 'station_similarity': {}, 'errors': (detail_ or {}).get('errors', [])}
    if not news or not isinstance(news['results'].get('profiles'), dict) or not local or not isinstance(local['results'].get('profiles'), dict):
        out['errors'].append({'code': 'PROFILES_MISSING'})
        return out
    station_names = {str(row[0]): row[1] for row in news['results'].get('names', [])}
    register = {str(row[0]): {'language': row[1], 'code': (row[2] or '').lower(), 'station': row[3]} for row in local['results'].get('names', [])}
    by_station_key = {}
    for entry in register.values():
        if entry['station']:
            by_station_key.setdefault(_station_key(entry['station']), entry)
    merged = {}
    for language_id, profile in local['results']['profiles'].items():
        entry = register.get(str(language_id))
        if not entry or not entry['code']:
            continue
        m = merged.setdefault(entry['code'], {'language': entry['language'].strip().title(), 'code': entry['code'], 'texts': 0, 'chars': 0, 'trigram_total': 0, 'trigrams': defaultdict(int)})
        m['texts'] += profile['texts']; m['chars'] += profile['chars']; m['trigram_total'] += profile['trigram_total']
        for g, c in profile['trigrams'].items():
            m['trigrams'][g] += c
    language_vectors = {code: _vector(m) for code, m in merged.items()}
    out['languages'] = {code: {'language': m['language'], 'transcript_segments': m['texts'], 'chars': m['chars']} for code, m in merged.items()}
    station_vectors = {}
    rows = []
    for station_id, profile in news['results']['profiles'].items():
        name = station_names.get(str(station_id)) or ('unassigned hour' if station_id in (None, 'None') else f'station #{station_id}')
        station_vectors[name] = _vector(profile)
        ranked = sorted(((code, _cosine(station_vectors[name], v)) for code, v in language_vectors.items()), key=lambda kv: -kv[1])
        declared = by_station_key.get(_station_key(name)) or ({'language': ENGLISH_STATIONS[_station_key(name)][0], 'code': ENGLISH_STATIONS[_station_key(name)][1], 'station': name} if _station_key(name) in ENGLISH_STATIONS else None)
        nearest, second = ranked[0] if ranked else (None, 0.0), ranked[1] if len(ranked) > 1 else (None, 0.0)
        rows.append({'station': name, 'scripts_profiled': profile['texts'], 'chars_profiled': profile['chars'], 'declared_language': declared['language'].strip().title() if declared else None,
                     'declared_code': declared['code'] if declared else None, 'nearest_code': nearest[0], 'nearest_language': merged[nearest[0]]['language'] if nearest[0] else None,
                     'nearest_similarity': nearest[1], 'second_code': second[0], 'second_similarity': second[1], 'margin': round(nearest[1] - second[1], 4),
                     'similarity_by_language': {code: s for code, s in ranked}})
    names = sorted(station_vectors)
    out['station_similarity'] = {a: {b: _cosine(station_vectors[a], station_vectors[b]) for b in names if b != a} for a in names}
    declared_by_name = {r['station']: r for r in rows}
    confirmed = [r['nearest_similarity'] for r in rows if r['declared_code'] in language_vectors and r['nearest_code'] == r['declared_code']]
    floor = min(confirmed) if confirmed else 0.0
    for r in rows:
        others = {b: v for b, v in out['station_similarity'].get(r['station'], {}).items() if b != 'unassigned hour'}
        closest = max(others.items(), key=lambda kv: kv[1]) if others else (None, 0.0)
        r['closest_station'], r['closest_station_similarity'] = closest[0], closest[1]
        r['closest_station_language'] = (declared_by_name.get(closest[0]) or {}).get('declared_language') if closest[0] else None
        if r['declared_code'] in language_vectors:
            r['verdict'] = ('confirmed: scripts match the workbench transcripts of the declared language' if r['nearest_code'] == r['declared_code']
                            else f"scripts nearest {r['nearest_language']} ({r['nearest_similarity']:.2f}) over declared {r['declared_language']} ({r['similarity_by_language'].get(r['declared_code'], 0):.2f}) — bilingual scripting or register to review")
        elif r['declared_code']:
            r['verdict'] = (f"{r['declared_language']}: no workbench transcripts to match; nearest modelled language {r['nearest_language']} at {r['nearest_similarity']:.2f} "
                            f"(confirmed stations score {floor:.2f} or more against their own language); scripts closest to {r['closest_station']} ({r['closest_station_language']}) at {r['closest_station_similarity']:.2f} — "
                            + ('a distinct language, related to ' + str(r['closest_station_language']) if r['closest_station_similarity'] >= 0.85 else 'a distinct language, declared by name'))
        else:
            r['verdict'] = 'no declared language; scripts nearest ' + str(r['nearest_language'])
    out['confirmation_floor'] = round(floor, 4)
    out['stations'] = sorted(rows, key=lambda s: s['station'])
    return json.loads(json.dumps(out, default=str))


def summarise_locations(detail_):
    """Per language: where the workbench's recordings live (URL scheme+host and first path segment), formats, transcribed files and speakers."""
    local = _target(detail_, 'local')
    out = {'languages': {}, 'errors': (detail_ or {}).get('errors', [])}
    if not local:
        out['errors'].append({'code': 'LOCATIONS_MISSING'}); return out
    r = local['results']
    register = {str(row[0]): {'language': (row[1] or '').strip().title(), 'code': (row[2] or '').lower(), 'station': row[3]} for row in r.get('languages', []) if isinstance(r.get('languages'), list)}
    langs = out['languages']
    def entry(language_id):
        key = str(language_id)
        return langs.setdefault(key, {**register.get(key, {'language': None, 'code': None, 'station': None}), 'converted': [], 'original_hosts': {}, 'compressed_hosts': {}, 'file_location_roots': {}, 'status': {}, 'transcribed': None})
    for row in r.get('converted_hosts', []) if isinstance(r.get('converted_hosts'), list) else []:
        language_id, host, first, count, seconds, mp3, wav, m4a, ogg, flac = row
        entry(language_id)['converted'].append({'host': host, 'first_segment': first, 'files': _n(count), 'audio_hours': round(_n(seconds) / 3600, 1),
                                                 'formats': {'mp3': _n(mp3), 'wav': _n(wav), 'm4a_aac': _n(m4a), 'ogg_opus': _n(ogg), 'flac': _n(flac)}})
    for name in ('original_hosts', 'compressed_hosts'):
        for language_id, host, count in r.get(name, []) if isinstance(r.get(name), list) else []:
            entry(language_id)[name][str(host)] = _n(count)
    for language_id, depth, root, count in r.get('file_location_depth', []) if isinstance(r.get('file_location_depth'), list) else []:
        entry(language_id)['file_location_roots'][f'{root} (depth {_n(depth)})'] = _n(count)
    for language_id, status, count, seconds in r.get('status_by_language', []) if isinstance(r.get('status_by_language'), list) else []:
        entry(language_id)['status'][str(status)] = {'files': _n(count), 'audio_hours': round(_n(seconds) / 3600, 1)}
    for language_id, files, segments, seconds, speakers in r.get('transcribed_files_by_language', []) if isinstance(r.get('transcribed_files_by_language'), list) else []:
        entry(language_id)['transcribed'] = {'files': _n(files), 'segments': _n(segments), 'speech_hours': round(_n(seconds) / 3600, 1), 'speakers': _n(speakers)}
    out['query_errors'] = {k: v for k, v in r.items() if isinstance(v, dict)}
    return json.loads(json.dumps(out, default=str))
