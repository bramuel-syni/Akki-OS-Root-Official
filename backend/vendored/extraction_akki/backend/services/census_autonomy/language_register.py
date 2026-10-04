"""Thirteen-language register (owner order 3 Oct 2026: "there are 13 languages … each station carries a name and a script you can use to
identify the language; complete the assessment of the forecast speech hours for the six you have not named").

Three registers agree on the stations and are joined here: the news vault's 13 stations (scripts), the transcription workbench's
folder_languages (station → language code → labelled recordings), and the folder paths of the media estate (station names in the
refused buckets). The census language model labels seven languages; the other six are assessed from the folders that carry their
station's name (a measured floor inside the whole-estate forecast), the related-language group they sit in (a ceiling), the pool of
speech the seven-class model could not label, and the script check that confirms each station's language from its own writing."""
from __future__ import annotations

from typing import Any, Dict, List

LANGUAGES: List[Dict[str, Any]] = [
    {'code': 'swa', 'language': 'Kiswahili', 'stations': ['Radio Citizen', 'Bahari FM'], 'group': None},
    {'code': 'kik', 'language': 'Gikuyu (Kikuyu)', 'stations': ['Inooro FM'], 'group': 'thagicu'},
    {'code': 'guz', 'language': 'Ekegusii (Kisii)', 'stations': ['Egesa'], 'group': None},
    {'code': 'kln', 'language': 'Kalenjin', 'stations': ['Chamgei'], 'group': None},
    {'code': 'luo', 'language': 'Dholuo (Luo)', 'stations': ['Ramogi FM'], 'group': None},
    {'code': 'lwg', 'language': 'Luhya (Wanga)', 'stations': ['Mulembe FM'], 'group': 'luhya'},
    {'code': 'kam', 'language': 'Kikamba (Kamba)', 'stations': ['Musyi FM'], 'group': None},
    {'code': 'mer', 'language': 'Kimeru (Meru)', 'stations': ['Muuga FM'], 'group': 'thagicu'},
    {'code': 'ebu', 'language': 'Kiembu (Embu)', 'stations': ['Wimwaro FM'], 'group': 'thagicu'},
    {'code': 'bxk', 'language': 'Bukusu (Luhya)', 'stations': ['Sulwe FM'], 'group': 'luhya'},
    {'code': 'mrg', 'language': 'Maragoli (Luhya)', 'stations': ['Vuuka'], 'group': 'luhya'},
    {'code': 'eng', 'language': 'English', 'stations': ['Hot 96'], 'group': None},
    {'code': 'mas', 'language': 'Maa (Maasai)', 'stations': [], 'group': None},
]
GROUPS = {'thagicu': 'Kikuyu–Embu–Meru (Thagicu)', 'luhya': 'Luhya: Wanga–Bukusu–Maragoli'}
LANGUAGES_KEPT = len(LANGUAGES)  # every consumer (forecast, report, retraining payloads) keeps all thirteen codes; never a twelve-code cap


def _classes(modelled) -> str:
    return f'{len(modelled)}-class'


def _station_key(name: str) -> str:
    return (name or '').lower().replace('radio ', '').replace(' fm', '').strip()


def _sum(entries: List[Dict[str, Any]]) -> Dict[str, float]:
    return {k: round(sum((e or {}).get(k) or 0.0 for e in entries), 1) for k in ('est', 'lo', 'hi')}


def build(forecast: Dict[str, Any] | None, aggregates: Dict[str, Any] | None, profiles: Dict[str, Any] | None) -> Dict[str, Any] | None:
    if not forecast:
        return None
    modelled = set(forecast.get('languages') or [])
    estate, by_station = forecast['estate'], forecast.get('by_station') or {}
    news = ((aggregates or {}).get('news_scripts') or {}).get('per_station') or {}
    workbench = (aggregates or {}).get('transcription_workbench') or {}
    wb_audio: Dict[str, Dict[str, float]] = {}
    for v in (workbench.get('files_by_language') or {}).values():
        code = (v.get('code') or '').lower()
        if code:
            a = wb_audio.setdefault(code, {'hours': 0.0, 'files': 0})
            a['hours'] += (v.get('audio_seconds') or 0) / 3600; a['files'] += v.get('files') or 0
    wb_text: Dict[str, Dict[str, float]] = {}
    for v in (workbench.get('transcripts_by_language') or {}).values():
        code = (v.get('code') or '').lower()
        if code:
            t = wb_text.setdefault(code, {'segments': 0, 'chars': 0})
            t['segments'] += v.get('segments') or 0; t['chars'] += v.get('chars') or 0
    checks = {_station_key(s['station']): s for s in ((profiles or {}).get('stations') or [])}
    rows = []
    for spec in LANGUAGES:
        code = spec['code']
        labelled = estate['languages'].get(code) if code in modelled else None
        named = by_station.get(code)
        news_rows = [news[n] for n in spec['stations'] if n in news]
        station_checks = [checks[_station_key(n)] for n in spec['stations'] if _station_key(n) in checks]
        rows.append({
            **spec, 'group_name': GROUPS.get(spec['group']), 'modelled': code in modelled,
            'news_scripts': {'live': sum(r['live_scripts'] for r in news_rows), 'chars': sum(r['chars'] for r in news_rows), 'stations': len(news_rows)} if news_rows else None,
            'workbench': {'audio_hours': round(wb_audio[code]['hours'], 1), 'files': wb_audio[code]['files'], 'transcript_segments': wb_text.get(code, {}).get('segments', 0)} if code in wb_audio else None,
            'script_check': [{'station': c['station'], 'verdict': c['verdict'], 'nearest_language': c['nearest_language'], 'nearest_similarity': c['nearest_similarity'],
                              'closest_station': c['closest_station'], 'closest_station_language': c['closest_station_language'], 'closest_station_similarity': c['closest_station_similarity']} for c in station_checks] or None,
            'forecast_labelled_speech': labelled,
            'named_folder_speech': {'speech': named['speech'], 'hours': named['hours'], 'unlabelled_speech': named['unlabelled_speech'], 'files': named['files'], 'bytes': named['bytes'], 'strata': named['strata'],
                                    'bases': named['bases'], 'buckets': named['labels'], 'labelled_inside': {k: v['est'] for k, v in named['languages'].items() if v['est']}} if named else None,
        })
    by_code = {r['code']: r for r in rows}
    groups = {}
    for gid, gname in GROUPS.items():
        members = [r for r in rows if r['group'] == gid]
        core = _sum([r['forecast_labelled_speech'] for r in members if r['modelled']])
        named_unmodelled = [r['named_folder_speech']['speech'] for r in members if not r['modelled'] and r['named_folder_speech']]
        inside = sum(sum(v for k, v in r['named_folder_speech']['labelled_inside'].items() if k in {m['code'] for m in members}) for r in members if not r['modelled'] and r['named_folder_speech'])
        ceiling = {k: round(core[k] + _sum(named_unmodelled)[k] - (inside if k == 'est' else 0.0), 1) for k in ('est', 'lo', 'hi')}
        groups[gid] = {'name': gname, 'members': [r['code'] for r in members], 'modelled_core_speech': core, 'named_unmodelled_speech': _sum(named_unmodelled), 'group_speech': ceiling,
                       'note': f'The {_classes(modelled)} model files the unmodelled members under the modelled relative; the group total is robust, the split inside it is a floor (named folders) until the thirteen-class model runs.'}
    for r in rows:
        if r['modelled']:
            r['assessment'] = {'speech_hours': r['forecast_labelled_speech'], 'basis': 'labelled by the census language model, scaled to the whole estate (forecast)',
                               'caveat': f"includes speech of {', '.join(by_code[c]['language'] for c in groups[r['group']]['members'] if c != r['code'])} the model cannot separate yet" if r['group'] else None}
        else:
            floor = (r['named_folder_speech'] or {}).get('speech') or {'est': 0.0, 'lo': 0.0, 'hi': 0.0}
            ceiling = groups[r['group']]['group_speech'] if r['group'] else ({'est': estate['unlabelled_speech']['est'], 'lo': estate['unlabelled_speech']['lo'], 'hi': estate['unlabelled_speech']['hi']} if r['stations'] else {'est': 0.0, 'lo': 0.0, 'hi': 0.0})
            r['assessment'] = {'speech_hours_floor': floor, 'speech_hours_ceiling': ceiling,
                               'basis': ('folders carrying the station\'s name, scaled to their populations (forecast); ceiling = the related-language group' if r['group'] else
                                         f'no folder carries the station\'s name; ceiling = the speech the {_classes(modelled)} model could not label' if r['stations'] else
                                         'no news station and no named folder; present only in the workbench register'),
                               'converts_with': 'the thirteen-class language model trained on the workbench\'s labelled recordings, then one census pass over the existing sample'}
    labelled_total = _sum([estate['languages'][c] for c in modelled])
    unl = estate['unlabelled_speech']
    if 'eng' in modelled:
        eng = estate['languages'].get('eng') or {'est': 0.0, 'lo': 0.0, 'hi': 0.0}
        non_english = {'lo': round(estate['speech']['lo'] - eng['hi'], 1), 'hi': round(estate['speech']['hi'] - eng['lo'], 1), 'planning': round(estate['speech']['est'] - eng['est'], 1),
                       'note': f'English is labelled by the {_classes(modelled)} model; non-English speech = all speech minus labelled English (interval from the two forecasts).'}
    else:
        non_english = {'lo': round(labelled_total['est'], 1), 'hi': round(estate['speech']['est'], 1), 'planning': round(estate['speech']['est'] - 0.5 * unl['est'], 1),
                       'note': f'English cannot be labelled by the {_classes(modelled)} model: at most the unlabelled pool is English (lo), at least none of it is (hi); planning figure halves the pool.'}
    return {'languages': rows, 'groups': groups, 'modelled_codes': sorted(modelled), 'register_codes': [l['code'] for l in LANGUAGES], 'unmodelled_codes': sorted(c for c in (l['code'] for l in LANGUAGES) if c not in modelled),
            'totals': {'speech': estate['speech'], 'labelled_modelled': labelled_total, 'labelled_seven': labelled_total, 'unlabelled': unl, 'non_english_speech_hours': non_english},
            'script_check': {'confirmation_floor': (profiles or {}).get('confirmation_floor'), 'stations_profiled': len((profiles or {}).get('stations') or [])} if profiles else None,
            'method': (f'Stations from three registers (news vault, workbench folder_languages, folder paths). {len(modelled)} modelled languages: census model labels scaled in the whole-estate '
                       f'forecast. {len(LANGUAGES) - len(modelled)} unmodelled: floor = speech forecast in folders named after the station; ceiling = the related-language group (Thagicu, Luhya) or the '
                       'unlabelled pool (English); script check = character-trigram profile of each station\'s scripts against the workbench transcripts and the other stations.')}
