"""Language evidence for the estate pack (owner order 2026-10-02): the non-English, non-music audio and the written text the estate
holds, by language, with hours, quality signals and the hourly news-script record — read from the completed GPU readings and the
aggregate-only database job, never estimated here. Exact file paths are joined locally from the worker's results map; they appear in
the owner's workbook and never in any model prompt."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

LANGUAGE_NAMES = {'guz': 'Ekegusii (Kisii)', 'kam': 'Kikamba (Kamba)', 'kik': 'Gikuyu (Kikuyu)', 'kln': 'Kalenjin', 'luo': 'Dholuo (Luo)', 'lwg': 'Wanga (Luhya)',
                  'swa': 'Kiswahili', 'bxk': 'Bukusu (Luhya)', 'ebu': 'Kiembu (Embu)', 'mer': 'Kimeru (Meru)', 'mrg': 'Maragoli (Luhya)', 'mas': 'Maa (Maasai)', 'eng': 'English'}
STATION_DECLARED = {'Hot 96': ('English', 'eng', 'declared: urban English-language station; not in the estate language table')}


def name_of(code: Optional[str]) -> str:
    return LANGUAGE_NAMES.get((code or '').lower(), code or 'unlabelled')


def _pct(n, d):
    return round(n / d, 4) if d else 0.0


def _results_map(job_id: str) -> Dict[str, str]:
    """ref → relative path inside the staged corpus; fetched once over the seam and cached beside the job record (control plane only)."""
    from services.training_runner import m9_dispatch
    cache = m9_dispatch._jobs_dir() / f'{job_id}.results_map.json'
    if cache.exists():
        return json.loads(cache.read_text())
    try:
        text = m9_dispatch.fetch_artifact(job_id, 'results_map.json', max_bytes=6_000_000)
        mapping = json.loads(text)
    except Exception:
        return {}
    cache.write_text(json.dumps(mapping, sort_keys=True))
    return mapping


def gather(tenant: str) -> Optional[Dict[str, Any]]:
    """Everything the producer needs, or None when no completed audio reading exists for the tenant."""
    from services.census_autonomy import text_estate_evidence
    from services.training_lab import estate_language
    audio_jobs = estate_language.completed(tenant, 'audio')
    if not audio_jobs:
        return None
    audio_doc, audio_rows = audio_jobs[0]
    text_jobs = estate_language.completed(tenant, 'text')
    text_rows = [r for _, rows in text_jobs for r in rows]
    db_doc = text_estate_evidence.latest(tenant)
    db = db_doc.get('summary') if db_doc and db_doc.get('status') == 'completed' else None
    return {'audio_doc': audio_doc, 'audio_rows': audio_rows, 'text_docs': [d for d, _ in text_jobs], 'text_rows': text_rows, 'db_doc': db_doc if db else None, 'db': db,
            'paths': _results_map(audio_doc['job_id'])}


def station_languages(db: Optional[Dict[str, Any]]) -> Dict[str, Dict[str, str]]:
    """Station → broadcast language, read from the estate's own folder_languages table where it names the station; Hot 96 is declared."""
    out = dict(STATION_DECLARED)
    for language, spec in (((db or {}).get('transcription_workbench') or {}).get('folder_languages') or {}).items():
        for station in spec.get('stations') or []:
            key = station.strip().lower().replace(' ', '')
            out[key] = (language.strip().capitalize() if language.islower() else language.strip(), (spec.get('codes') or [''])[0], 'estate table local.folder_languages')
    resolved = {}
    for station in ((db or {}).get('news_scripts') or {}).get('stations') or []:
        key = station.lower().replace(' fm', '').replace(' ', '')
        hit = out.get(station) or out.get(key) or next((v for k, v in out.items() if k.replace(' fm', '').replace(' ', '').lower() in (key, key.replace('radio', ''))), None)
        resolved[station] = {'language': hit[0], 'code': hit[1], 'basis': hit[2]} if hit else {'language': 'not recorded', 'code': '', 'basis': 'no estate row names this station'}
    return resolved


def content(tenant: str, receipts: Dict[str, Any], facts: Dict[str, Any], series: Dict[str, Any], calculations: Dict[str, Any], claims: Dict[str, Any],
            tables: Dict[str, Any], cannot_say: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Adds receipts R06–R08, facts F060–F094, series S010–S013, tables T020–T035 and the language chapters. Returns the chapters."""
    g = gather(tenant)
    if not g:
        cannot_say.append({'gap': 'Non-English, non-music audio and text by language', 'reason': 'no completed estate language reading is banked for this tenant', 'closes_with': 'the two-GPU estate language job (Train Models → estate language)'})
        return []
    audio_doc, rows, text_rows, db, paths = g['audio_doc'], g['audio_rows'], g['text_rows'], g['db'], g['paths']
    result = audio_doc['result']
    models = audio_doc.get('models') or {}
    receipts['R06'] = {'resolves_to': f"Estate language reading {audio_doc['job_id']} on {audio_doc['host']} ({result['devices']} GPUs, {result['compute']['gpu_hours_total']} GPU-h): audio language model {models.get('audio', {}).get('job_id')} "
                                      f"sha256 {str(models.get('audio', {}).get('sha256'))[:12]}…, music detector {models.get('music', {}).get('job_id')} sha256 {str(models.get('music', {}).get('sha256'))[:12]}…; model readings, not human labels", 'platform_ref': audio_doc['job_id']}
    text_docs = g['text_docs']
    if text_docs:
        receipts['R07'] = {'resolves_to': f"Served text language model {models.get('text', {}).get('job_id')} readings of the staged transcripts: jobs {', '.join(d['job_id'] for d in text_docs)} "
                                          f"({len(text_rows):,} transcripts read, {sum(1 for _ in rows if _.get('transcript'))} present)", 'platform_ref': text_docs[0]['job_id']}
    if db:
        receipts['R08'] = {'resolves_to': f"Aggregate-only database reading {g['db_doc']['job_id']}: {db['news_scripts']['receipt'] if db.get('news_scripts') else ''}; {db['transcription_workbench']['receipt'] if db.get('transcription_workbench') else ''}",
                           'platform_ref': g['db_doc']['job_id']}

    # ---------------------------------------------------------------- audio by language (staged corpus, both GPUs)
    per = result['per_language']
    languages = sorted(per, key=lambda k: -per[k]['hours_recorded'])
    hours = sum(p['hours_recorded'] for p in per.values()); speech = sum(p['hours_speech_estimate'] for p in per.values()); music = sum(p['hours_music_estimate'] for p in per.values())
    windows = sum(p['windows_read'] for p in per.values()); music_windows = sum(p['music_windows'] for p in per.values()); abstained = sum(p['abstained'] for p in per.values()); judged = sum(p['judged'] for p in per.values())
    agree = sum(p['agrees_with_folder_label'] * p['judged'] for p in per.values() if p['agrees_with_folder_label'] is not None)
    silence = sum(r.get('silence_windows', 0) for r in rows)
    facts.update({
        'F060': {'label': 'Staged audio recorded, hours (header duration as decoded)', 'value': round(hours, 1), 'unit': 'hours', 'class': 'measured', 'receipt': 'R06'},
        'F061': {'label': 'Speech hours after music windows are removed (estimate)', 'value': round(speech, 1), 'unit': 'hours', 'class': 'estimated', 'receipt': 'R06', 'measurement_scope': 'recorded hours × share of windows the music detector did not call music'},
        'F062': {'label': 'Music hours inside the staged audio (estimate)', 'value': round(music, 1), 'unit': 'hours', 'class': 'estimated', 'receipt': 'R06'},
        'F063': {'label': 'Audio files read', 'value': result['read'], 'unit': 'files', 'class': 'measured', 'receipt': 'R06'},
        'F064': {'label': 'Two-second windows read', 'value': round(windows / 1e6, 3), 'unit': 'm', 'class': 'measured', 'receipt': 'R06'},
        'F065': {'label': 'Windows the music detector called music', 'value': _pct(music_windows, windows), 'unit': 'pct', 'class': 'measured', 'receipt': 'R06'},
        'F066': {'label': 'Speech windows the language model declined to label', 'value': _pct(abstained, windows - music_windows), 'unit': 'pct', 'class': 'measured', 'receipt': 'R06'},
        'F067': {'label': 'GPU-hours spent on the audio reading', 'value': result['compute']['gpu_hours_total'], 'unit': 'GPU-h', 'class': 'measured', 'receipt': 'R06'},
        'F068': {'label': 'Language folders in the staged corpus', 'value': len(per), 'unit': 'languages', 'class': 'measured', 'receipt': 'R06'},
        'F069': {'label': 'Words in the staged transcripts', 'value': round(sum(p['transcripts']['words'] for p in per.values()) / 1e6, 2), 'unit': 'm', 'class': 'measured', 'receipt': 'R06'},
        'F072': {'label': 'Judged windows agreeing with the folder language', 'value': _pct(agree, judged), 'unit': 'pct', 'class': 'measured', 'receipt': 'R06'},
        'F073': {'label': 'Windows of digital silence', 'value': _pct(silence, windows + silence), 'unit': 'pct', 'class': 'measured', 'receipt': 'R06'},
        'F074': {'label': 'Files where music is the majority of windows', 'value': sum(p['files_with_music_majority'] for p in per.values()), 'unit': 'files', 'class': 'measured', 'receipt': 'R06'},
    })
    series['S010'] = {'label': 'Speech hours by language folder (estimate, music windows removed)', 'categories': [name_of(k) for k in languages], 'values': {'Hours': [round(per[k]['hours_speech_estimate'], 1) for k in languages]}, 'unit': 'hours', 'class': 'estimated', 'receipt': 'R06'}
    series['S011'] = {'label': 'Share of judged windows agreeing with the folder language', 'categories': [name_of(k) for k in languages], 'values': {'Share': [per[k]['agrees_with_folder_label'] or 0 for k in languages]}, 'unit': 'pct', 'class': 'measured', 'receipt': 'R06'}
    calculations['K010'] = {'label': 'Speech share of the staged audio', 'formula': 'F061 / F060', 'inputs': ['F060', 'F061'], 'unit': 'pct'}
    tables['T020'] = {'label': 'Audio held by language folder — what both GPUs read', 'class': 'measured', 'receipt': 'R06', 'right_align_from': 3,
                      'note': 'Hours are recorded duration; speech and music hours split those hours by the music detector; agreement is the share of labelled windows whose language matched the folder name. Model readings, not human labels.',
                      'columns': ['Language folder', 'Language', 'Files', 'Hours recorded', 'Speech hours (est.)', 'Music hours (est.)', 'Agrees with folder', 'Declined to label', 'Transcript words'],
                      'deck_columns': ['Language', 'Files', 'Hours recorded', 'Speech hours (est.)', 'Music hours (est.)', 'Agrees with folder'],
                      'rows': [[k, name_of(k), per[k]['files'], round(per[k]['hours_recorded'], 1), round(per[k]['hours_speech_estimate'], 1), round(per[k]['hours_music_estimate'], 1),
                                f"{(per[k]['agrees_with_folder_label'] or 0) * 100:.1f}%", f"{_pct(per[k]['abstained'], per[k]['windows_read'] - per[k]['music_windows']) * 100:.1f}%" if per[k]['windows_read'] - per[k]['music_windows'] else '—',
                                per[k]['transcripts']['words']] for k in languages]}
    quality_rows = []
    for k in languages:
        group = [r for r in rows if r['language'] == k]
        read = [r for r in group if 'windows_read' in r]
        sil = sum(r.get('silence_windows', 0) for r in group); tot = sum(r.get('windows_read', 0) for r in read) + sil
        low_conf = sum(1 for r in read if (r.get('mean_confidence') or 0) < 0.7)
        mixed = sum(1 for r in read if r.get('top_share') is not None and r['top_share'] < 0.6)
        quality_rows.append([name_of(k), len(group), len(group) - len(read), f"{_pct(sil, tot) * 100:.2f}%" if tot else '—', per[k]['files_with_music_majority'], mixed, low_conf,
                             f"{per[k]['mean_confidence']:.3f}" if per[k]['mean_confidence'] is not None else '—', round(sum(r['duration_s'] for r in read) / len(read) / 60, 1) if read else '—'])
    tables['T024'] = {'label': 'Audio quality signals by language folder', 'class': 'measured', 'receipt': 'R06', 'right_align_from': 1,
                      'note': 'Decode failures, digital silence, music-dominated files, mixed-language files (no language reaches sixty percent of labelled windows) and low-confidence files are the quality signals the reading can measure; noise and intelligibility were not scored.',
                      'columns': ['Language', 'Files', 'Decode failures', 'Silence (windows)', 'Music-majority files', 'Mixed-language files', 'Low-confidence files', 'Mean confidence', 'Mean length (min)'],
                      'deck_columns': ['Language', 'Files', 'Decode failures', 'Music-majority files', 'Mixed-language files', 'Low-confidence files', 'Mean confidence'], 'rows': quality_rows}
    claims['C040'] = {'text': 'The staged corpus holds {F060} hours of recorded audio in {F068} language folders; {F061} hours are speech once {F062} hours of music are set aside, read by both GPUs in {F067} GPU-hours', 'supports': ['F060', 'F061', 'F062', 'F067', 'F068']}
    claims['C041'] = {'text': 'Across every folder, {F072} of labelled windows agree with the folder language; the model declined to label {F066} of speech windows', 'supports': ['F072', 'F066']}

    # ---------------------------------------------------------------- transcripts through the served text model
    if text_rows:
        by_lang = defaultdict(lambda: {'files': 0, 'chars': 0, 'words': 0, 'units': 0, 'agree': 0, 'judged': 0, 'match': 0})
        for r in text_rows:
            b = by_lang[r['language']]; b['files'] += 1; b['chars'] += r['chars']; b['words'] += r['words']; b['units'] += r['units']
            j = sum(r['by_language'].values()); b['judged'] += j; b['agree'] += r['by_language'].get(r['language'], 0); b['match'] += 1 if r.get('top_language') == r['language'] else 0
        total_units = sum(b['judged'] for b in by_lang.values()); total_agree = sum(b['agree'] for b in by_lang.values())
        facts['F070'] = {'label': 'Transcripts read by the served text model', 'value': len(text_rows), 'unit': 'transcripts', 'class': 'measured', 'receipt': 'R07'}
        facts['F071'] = {'label': 'Transcript passages agreeing with the folder language', 'value': _pct(total_agree, total_units), 'unit': 'pct', 'class': 'measured', 'receipt': 'R07'}
        facts['F075'] = {'label': 'Transcripts not yet read by the text model', 'value': max(0, sum(1 for r in rows if r.get('transcript')) - len(text_rows)), 'unit': 'transcripts', 'class': 'measured', 'receipt': 'R07'}
        tables['T021'] = {'label': 'Transcripts by language folder — read by the served text language model', 'class': 'measured', 'receipt': 'R07', 'right_align_from': 2,
                          'note': 'Passages of up to fifteen hundred characters were labelled by the admitted text model; agreement is the share of passages whose label matched the folder language. Transcripts the capped pass did not reach are counted as not read.',
                          'columns': ['Language folder', 'Language', 'Transcripts read', 'Characters', 'Words', 'Passages labelled', 'Agrees with folder', 'Files whose top label matches'],
                          'deck_columns': ['Language', 'Transcripts read', 'Characters', 'Words', 'Agrees with folder', 'Files whose top label matches'],
                          'rows': [[k, name_of(k), b['files'], b['chars'], b['words'], b['judged'], f"{_pct(b['agree'], b['judged']) * 100:.1f}%" if b['judged'] else '—', b['match']] for k, b in sorted(by_lang.items(), key=lambda kv: -kv[1]['files'])]}
        claims['C042'] = {'text': 'Of {F070} transcripts read by the text model, {F071} of passages agree with the folder language; {F075} transcripts were not reached inside the compute cap', 'supports': ['F070', 'F071', 'F075']}

    # ---------------------------------------------------------------- hourly news scripts (news_vault) and the transcription workbench (local)
    if db and db.get('news_scripts'):
        ns = db['news_scripts']; o = ns['overall'] or {}
        stations = station_languages(db)
        per_station = ns['per_station']
        order = sorted((k for k in per_station if k != 'unassigned hour'), key=lambda k: -per_station[k]['live_scripts'])
        span_days = None
        try:
            from datetime import date
            a, b = o.get('first_date'), o.get('last_date')
            span_days = (date.fromisoformat(str(b)[:10]) - date.fromisoformat(str(a)[:10])).days if a and b else None
        except ValueError:
            span_days = None
        facts.update({
            'F080': {'label': 'News scripts held (live rows)', 'value': (o.get('scripts') or 0) - (o.get('deleted') or 0), 'unit': 'scripts', 'class': 'measured', 'receipt': 'R08'},
            'F081': {'label': 'Radio stations with scripts', 'value': len(order), 'unit': 'stations', 'class': 'measured', 'receipt': 'R08'},
            'F082': {'label': 'Calendar dates carrying at least one script', 'value': o.get('dates_with_scripts') or 0, 'unit': 'dates', 'class': 'measured', 'receipt': 'R08'},
            'F083': {'label': 'Days from the first script date to the last', 'value': span_days or 0, 'unit': 'days', 'class': 'measured', 'receipt': 'R08'},
            'F084': {'label': 'Characters of script text', 'value': round((o.get('chars') or 0) / 1e6, 1), 'unit': 'm', 'class': 'measured', 'receipt': 'R08'},
            'F085': {'label': 'Script rows that are revisions of an earlier script', 'value': _pct(o.get('revisions_of_a_parent') or 0, o.get('scripts') or 1), 'unit': 'pct', 'class': 'measured', 'receipt': 'R08'},
            'F086': {'label': 'Distinct script texts among live rows', 'value': o.get('distinct_script_texts') or 0, 'unit': 'scripts', 'class': 'measured', 'receipt': 'R08'},
            'F087': {'label': 'Scripts marked deleted', 'value': o.get('deleted') or 0, 'unit': 'scripts', 'class': 'measured', 'receipt': 'R08'},
            'F088': {'label': 'Mean characters per script', 'value': o.get('mean_chars') or 0, 'unit': 'characters', 'class': 'measured', 'receipt': 'R08'},
        })
        calculations['K011'] = {'label': 'Share of the span that carries scripts', 'formula': 'F082 / F083', 'inputs': ['F082', 'F083'], 'unit': 'pct'}
        calculations['K012'] = {'label': 'Distinct texts as a share of live scripts', 'formula': 'F086 / F080', 'inputs': ['F080', 'F086'], 'unit': 'pct'}
        series['S012'] = {'label': 'Live news scripts by station', 'categories': [f"{k} · {stations.get(k, {}).get('language', '')}" for k in order], 'values': {'Scripts': [per_station[k]['live_scripts'] for k in order]}, 'unit': 'scripts', 'class': 'measured', 'receipt': 'R08'}
        series['S013'] = {'label': 'Distinct bulletin hours per scripted day, by station (mean)', 'categories': [k for k in order], 'values': {'Hours': [per_station[k]['mean_distinct_hours_per_day'] or 0 for k in order]}, 'unit': 'hours', 'class': 'measured', 'receipt': 'R08'}
        tables['T022'] = {'label': 'Hourly news scripts by station (news_vault.stories)', 'class': 'measured', 'receipt': 'R08', 'right_align_from': 2,
                          'note': 'A scripted day is a calendar date with at least one script for the station; bulletin hours are the distinct hour slots scripted that day. The script texts themselves were not read; the language is the station\'s broadcast language as recorded in the estate.',
                          'columns': ['Station', 'Broadcast language', 'Live scripts', 'Deleted', 'Scripted days', 'First date', 'Last date', 'Scripts per scripted day', 'Bulletin hours per scripted day', 'Days with all twenty-four hours', 'Hour slots configured', 'Characters'],
                          'deck_columns': ['Station', 'Broadcast language', 'Live scripts', 'Scripted days', 'Scripts per scripted day', 'Bulletin hours per scripted day', 'Characters'],
                          'rows': [[k, stations.get(k, {}).get('language', ''), per_station[k]['live_scripts'], per_station[k]['deleted_scripts'], per_station[k]['dates'], str(per_station[k]['first_date'])[:10], str(per_station[k]['last_date'])[:10],
                                    per_station[k]['mean_scripts_per_day'], per_station[k]['mean_distinct_hours_per_day'], per_station[k]['days_with_24_slots'], per_station[k]['slots_configured'], per_station[k]['chars']] for k in order]
                                  + ([[ 'unassigned hour', '—', per_station['unassigned hour']['live_scripts'], per_station['unassigned hour']['deleted_scripts'], per_station['unassigned hour']['dates'], str(per_station['unassigned hour']['first_date'])[:10],
                                       str(per_station['unassigned hour']['last_date'])[:10], per_station['unassigned hour']['mean_scripts_per_day'], per_station['unassigned hour']['mean_distinct_hours_per_day'], 0, 0, per_station['unassigned hour']['chars']]] if 'unassigned hour' in per_station else [])}
        tables['T032'] = {'label': 'News scripts by station and date (every scripted day)', 'class': 'measured', 'receipt': 'R08', 'right_align_from': 3,
                          'note': 'One row per station per calendar date that carries a script: how many scripts, how many distinct hour slots, how many characters, how many rows later marked deleted.',
                          'columns': ['Station', 'Broadcast language', 'Date', 'Scripts', 'Distinct hour slots', 'Characters', 'Deleted'],
                          'rows': [[k, stations.get(k, {}).get('language', ''), str(d[0])[:10], d[1], d[2], d[3], d[4]] for k in order + (['unassigned hour'] if 'unassigned hour' in ns['by_station_date'] else []) for d in ns['by_station_date'].get(k, [])]}
        tables['T033'] = {'label': 'Bulletin hour slots by station (live scripts per slot, dates with that slot)', 'class': 'measured', 'receipt': 'R08', 'right_align_from': 2,
                          'note': 'Which hours of the day each station actually scripts, across all scripted days.',
                          'columns': ['Station', 'Hour slot', 'Live scripts', 'Dates with this slot'],
                          'rows': [[k, s['slot'], s['scripts'], s['dates']] for k in order for s in sorted(ns['slots_by_station'].get(k, []), key=lambda x: str(x['slot']))]}
        claims['C043'] = {'text': 'The news archive holds {F080} live scripts ({F084} million characters) from {F081} stations, but on {F082} calendar dates across a {F083}-day span ({K011} of days), not every day', 'supports': ['F080', 'F081', 'F082', 'F083', 'F084']}
        claims['C044'] = {'text': '{F085} of script rows are revisions of an earlier script and {F086} distinct texts remain among the live rows ({K012}); {F087} rows are marked deleted', 'supports': ['F085', 'F086', 'F087']}
        cannot_say.append({'gap': 'Language of each news script', 'reason': 'the scripts were counted and sized, not read; the language shown is the station\'s broadcast language from the estate\'s own table', 'closes_with': 'a text-model pass over the script column under the same aggregate-only seam'})
    if db and db.get('transcription_workbench'):
        tw = db['transcription_workbench']; files = tw.get('files_by_language') or {}; tr = tw.get('transcripts_by_language') or {}
        total_files = sum(v['files'] for v in files.values()); total_hours = sum(v['audio_seconds'] for v in files.values()) / 3600
        to = tw.get('transcripts_overall') or {}
        facts.update({
            'F090': {'label': 'Recordings registered in the transcription workbench', 'value': total_files, 'unit': 'recordings', 'class': 'measured', 'receipt': 'R08'},
            'F091': {'label': 'Audio hours registered in the transcription workbench', 'value': round(total_hours, 1), 'unit': 'hours', 'class': 'measured', 'receipt': 'R08'},
            'F092': {'label': 'Transcript segments in the workbench', 'value': to.get('segments') or 0, 'unit': 'segments', 'class': 'measured', 'receipt': 'R08'},
            'F093': {'label': 'Characters of workbench transcript text', 'value': round((to.get('chars') or 0) / 1e6, 2), 'unit': 'm', 'class': 'measured', 'receipt': 'R08'},
            'F094': {'label': 'Languages registered in the workbench', 'value': len({v.get('language') for v in files.values() if v.get('language')}), 'unit': 'languages', 'class': 'measured', 'receipt': 'R08'},
        })
        rows_tw = []
        for lid, v in sorted(files.items(), key=lambda kv: -kv[1]['audio_seconds']):
            t = tr.get(lid) or tr.get(str(lid)) or {}
            rows_tw.append([v.get('language') or f'language id {lid}', v.get('code') or '', v.get('station') or '', v['files'], round(v['audio_seconds'] / 3600, 1), v['transcribe_uploaded'], v['with_text_file'],
                            t.get('segments', 0), t.get('chars', 0), round(t.get('speech_seconds', 0) / 3600, 1), str(v.get('last_processed') or '')[:10]])
        tables['T023'] = {'label': 'Transcription workbench by language (local.uploaded_files, local.transcripts)', 'class': 'measured', 'receipt': 'R08', 'right_align_from': 3,
                          'note': 'The workbench registers recordings per language with their length and whether a transcript was produced; transcript hours are the summed segment spans. This is a separate inventory from the staged corpus and may overlap it — the two are not added together anywhere in this pack.',
                          'columns': ['Language', 'Code', 'Station', 'Recordings', 'Audio hours', 'Sent to transcription', 'With text file', 'Transcript segments', 'Transcript characters', 'Transcribed hours', 'Last processed'],
                          'deck_columns': ['Language', 'Station', 'Recordings', 'Audio hours', 'Transcript segments', 'Transcribed hours'], 'rows': rows_tw}
        claims['C045'] = {'text': 'The transcription workbench registers {F090} recordings ({F091} hours) in {F094} languages with {F092} transcript segments ({F093} million characters); it is a separate inventory from the staged corpus', 'supports': ['F090', 'F091', 'F092', 'F093', 'F094']}
        cannot_say.append({'gap': 'Overlap between the workbench recordings and the staged corpus', 'reason': 'both inventories were counted on their own; no file-level join was made', 'closes_with': 'a hash join of workbench file locations against the staged corpus paths'})

    # ---------------------------------------------------------------- workbook-only evidence rows (exact paths joined locally)
    tables['T030'] = {'label': 'Audio file evidence — every staged recording both GPUs read', 'class': 'measured', 'receipt': 'R06', 'right_align_from': 5,
                      'note': 'One row per recording: its path inside the staged corpus, folder language, duration, how many windows were read, the music share, the language the model gave most often and how often, its mean confidence, and the transcript measures. Paths are joined on the owner\'s side; no path left the estate for authoring.',
                      'columns': ['Reference', 'Path in staged corpus', 'Language folder', 'Session', 'GPU', 'Bytes', 'Duration (s)', 'Windows read', 'Silence windows', 'Music windows', 'Music share', 'Speech windows', 'Declined', 'Labelled', 'Top language', 'Top share', 'Mean confidence', 'Transcript segments', 'Transcript words', 'Transcript characters', 'Speakers', 'Error'],
                      'rows': [[r['ref'], paths.get(r['ref'], ''), r['language'], r['session'], r.get('device'), r['bytes'], r.get('duration_s'), r.get('windows_read'), r.get('silence_windows'), r.get('music_windows'), r.get('music_share'),
                                r.get('speech_windows'), r.get('abstained'), r.get('judged'), r.get('top_language'), r.get('top_share'), r.get('mean_confidence'),
                                (r.get('transcript') or {}).get('segments'), (r.get('transcript') or {}).get('words'), (r.get('transcript') or {}).get('chars'), (r.get('transcript') or {}).get('speakers'), r.get('error')]
                               for r in sorted(rows, key=lambda x: (x['language'], x['session'], x['ref']))]}
    if text_rows:
        tables['T031'] = {'label': 'Transcript evidence — every transcript the served text model read', 'class': 'measured', 'receipt': 'R07', 'right_align_from': 4,
                          'note': 'One row per transcript: path of its recording, folder language, size, passages labelled, the label given most often and the count per label.',
                          'columns': ['Reference', 'Path in staged corpus', 'Language folder', 'Session', 'Characters', 'Words', 'Passages', 'Label errors', 'Top label', 'Labels (code: passages)'],
                          'rows': [[r['ref'], paths.get(r['ref'], ''), r['language'], r['session'], r['chars'], r['words'], r['units'], r.get('errors'), r.get('top_language'), '; '.join(f'{k}: {v}' for k, v in sorted(r['by_language'].items(), key=lambda kv: -kv[1]))]
                                   for r in sorted(text_rows, key=lambda x: (x['language'], x['session'], x['ref']))]}
    tables['T034'] = {'label': 'Model and version provenance for every reading in this pack', 'class': 'measured', 'receipt': 'R06', 'right_align_from': 99,
                      'note': 'Which admitted model read what, from which host, under which checksum.',
                      'columns': ['Reading', 'Model', 'Job', 'Host', 'SHA-256', 'Scope'],
                      'rows': [['Audio language', 'Luhya v3 corrective checkpoint (admitted for Wanga; research-grade elsewhere)', models.get('audio', {}).get('job_id'), audio_doc['host'], models.get('audio', {}).get('sha256'), 'two-second windows of every staged recording'],
                               ['Music detection', 'Admitted music detector', models.get('music', {}).get('job_id'), audio_doc['host'], models.get('music', {}).get('sha256'), 'same windows'],
                               ['Text language', 'Admitted 8B text language-identification adapter (served)', models.get('text', {}).get('job_id'), (models.get('text', {}).get('serving') or {}).get('host'), ', '.join((text_docs[0]['result'].get('model') or {}).get('artefact_sha256_seen', [])) if text_docs else '', 'fifteen-hundred-character transcript passages'],
                               ['Database aggregates', 'No model — SQL aggregates through the pinned seam', g['db_doc']['job_id'] if g['db_doc'] else '—', 'jump host via akki-vm', g['db_doc'].get('detail_sha256') if g['db_doc'] else '', 'news_vault and local databases, counts and character sums only']]}
    tables['T035'] = {'label': 'Compute used by the estate language reading', 'class': 'measured', 'receipt': 'R06', 'right_align_from': 2,
                      'note': 'Both GPUs on the audio host took a balanced share of the recordings; the text model ran on its own serving GPU.',
                      'columns': ['Job', 'Device', 'Files', 'Windows', 'Seconds', 'GPU peak (GB)', 'Windows per second', 'Stage'],
                      'rows': [[audio_doc['job_id'], f"GPU {d['device']}", d['files'], d['windows'], d['elapsed_s'], d.get('gpu_peak_gb'), d.get('windows_per_second'), d.get('stage')] for d in result.get('per_device') or []]
                              + [[d['job_id'], 'served text GPU', d['result']['read'], d['result'].get('files'), d['result']['compute']['wall_seconds'], None, None, f"cap {d['result']['compute']['cap_gpu_hours']} GPU-h; {d['result']['not_reached']} not reached"] for d in text_docs]}

    chapters = [
        {'question': 'Which non-English, non-music audio does the estate hold, by language, and in what condition?',
         'answers_with': ['F060', 'F061', 'F062', 'F065', 'F066', 'F072', 'F073', 'F074', 'K010'], 'exhibits': ['S010', 'S011'], 'tables': ['T020', 'T024']},
    ]
    if 'F080' in facts or 'F090' in facts or 'F070' in facts:
        chapters.append({'question': 'What written text does the estate hold by language — the hourly news scripts, the transcripts and the transcription workbench?',
                         'answers_with': [t for t in ('F080', 'F081', 'F082', 'F083', 'F084', 'F085', 'F086', 'F070', 'F071', 'F090', 'F091', 'F092', 'K011', 'K012') if t in facts or t in calculations],
                         'exhibits': [s for s in ('S012', 'S013') if s in series], 'tables': [t for t in ('T022', 'T021', 'T023') if t in tables]})
    return chapters
