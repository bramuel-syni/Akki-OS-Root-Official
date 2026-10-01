"""Which languages the audio cognition model handles poorly, with honest intervals, and a bounded reinforcement proposal that
stays HELD until the owner approves. Deterministic; model advice is requested separately through the advisory roles."""
from services.training_lab import statistics as stats
from services.training_lab.evidence import LANGUAGES, number

REFERENCE_BASELINE = 'lcj-f96c86a16312'
LEVERS = {'max_windows_per_file': 'existing parameter; raises how much of each weak-language file is used',
          'epochs': 'existing parameter; more passes over the balanced batches',
          'logit_adjustment_tau': 'existing parameter; class-prior logit adjustment at training time',
          'language_sampling_weights': 'NOT an existing worker parameter; the corrective worker balances by square-root inverse frequency (cap 8) without oversampling — adding language weights is a recipe change for review'}


def _judged(row):
    windows, abstention = number(row.get('windows')), number(row.get('abstention_rate'))
    if not windows or abstention is None: return None
    return max(int(round(windows * (1 - abstention))), 0)


def _interval(row):
    accuracy, judged = number(row.get('accuracy')), _judged(row)
    if accuracy is None or not judged: return None
    return stats.wilson_interval(int(round(accuracy * judged)), judged)


def verdict(interval, floor):
    if interval is None: return 'not_measured'
    if interval['high'] < floor: return 'below_floor'
    if interval['low'] >= floor: return 'meets_floor'
    return 'at_risk'


def _runs():
    from services.audio_plane_v1 import language_cognition_dispatch as lc
    out = []
    for job in lc.list_jobs():
        cert = job.get('run_certificate') or {}
        if job.get('status') != 'completed' or not cert or job.get('phase') not in ('train_baseline', 'train_corrective'): continue
        strata = cert.get('per_stratum') or {}
        if not any(number(v.get('accuracy')) is not None for v in strata.values() if isinstance(v, dict)): continue
        out.append({'job_id': job['job_id'], 'phase': job['phase'], 'submitted_at': job.get('submitted_at'), 'per_stratum': strata,
                    'data_touched': (cert.get('data_touched') or {}).get('per_language') or {}, 'dp': bool(cert.get('dp_sgd')),
                    'compute': cert.get('compute') or {}, 'verdict': cert.get('verdict'), 'params': job.get('params') or {}})
    return out


def _corpus_hours():
    from services.training_lab import store as lab
    row = lab.db().training_lab_runs.find_one({'tenant_id': 'RMS', 'kind': 'assessment', 'inspection.per_language_folder': {'$exists': True}}, {'_id': 0, 'inspection.per_language_folder': 1}, sort=[('created_at', -1)])
    return {k: v.get('hours') for k, v in ((row or {}).get('inspection') or {}).get('per_language_folder', {}).items()}


def report(floor=0.9):
    runs = _runs(); reference = next((r for r in runs if r['job_id'] == REFERENCE_BASELINE), None)
    if reference is None:
        return {'status': 'no_measured_baseline', 'floor': floor, 'languages': {}, 'runs': []}
    hours = _corpus_hours(); languages = {}
    for language in sorted(LANGUAGES):
        row = reference['per_stratum'].get(language)
        if not isinstance(row, dict): continue
        interval = _interval(row); touched = reference['data_touched'].get(language) or {}
        history = []
        for run in runs:
            other = run['per_stratum'].get(language)
            if isinstance(other, dict) and number(other.get('accuracy')) is not None and _judged(other):
                history.append({'job_id': run['job_id'], 'phase': run['phase'], 'dp': run['dp'], 'accuracy': other['accuracy'], 'abstention_rate': other.get('abstention_rate'), 'judged_windows': _judged(other)})
        languages[language] = {'ref': f'lang_{language}', 'accuracy': number(row.get('accuracy')), 'abstention_rate': number(row.get('abstention_rate')), 'test_windows': number(row.get('windows')),
                               'judged_windows': _judged(row), 'interval': interval, 'verdict': verdict(interval, floor), 'gap_to_floor': round(floor - row['accuracy'], 4) if number(row.get('accuracy')) is not None else None,
                               'training_windows': number(touched.get('windows_train')), 'training_presenters': number(touched.get('presenters_train')), 'corpus_hours': number(hours.get(language)),
                               'history': history}
    weak = [k for k, v in languages.items() if v['verdict'] == 'below_floor']; at_risk = [k for k, v in languages.items() if v['verdict'] == 'at_risk']
    return {'status': 'measured', 'ref': 'weak_language_report', 'floor': floor, 'floor_source': 'per_language_accuracy_default 0.9 in the sealed contract check',
            'reference_run': {'job_id': REFERENCE_BASELINE, 'phase': reference['phase'], 'verdict': reference['verdict'], 'evidence_class': 'historical_measured_not_blind'},
            'languages': languages, 'below_floor': weak, 'at_risk': at_risk, 'meets_floor': [k for k, v in languages.items() if v['verdict'] == 'meets_floor'],
            'corrective_runs_note': 'DP-SGD corrective runs collapsed on several languages and are shown as history, not as the current model.',
            'runs': [{'job_id': r['job_id'], 'phase': r['phase'], 'dp': r['dp'], 'submitted_at': r['submitted_at']} for r in runs]}


def scaling(report_data, floor):
    """Windows-needed scenarios from the reference run's cross-language points (volume → accuracy). Prior sensitivity, not a forecast."""
    points = [(v['training_windows'], v['accuracy']) for v in report_data['languages'].values() if v['training_windows'] and v['accuracy'] is not None]
    if len({p[0] for p in points}) < 3: return None
    try:
        return stats.power_law_scenarios(points, (0.2, 0.8), (0.0, 0.05), floor, cap=60000)
    except ValueError as exc:
        return {'unavailable': str(exc)}


def plan(report_data):
    floor = report_data['floor']; targets = report_data['below_floor'] + report_data['at_risk']
    strong = [v['training_windows'] for k, v in report_data['languages'].items() if v['verdict'] == 'meets_floor' and v['training_windows']]
    reference_volume = int(sorted(strong)[len(strong) // 2]) if strong else None
    rows = []
    for language in targets:
        row = report_data['languages'][language]; available_windows = int(row['corpus_hours'] * 3600 / 4) if row['corpus_hours'] else None
        headroom = (available_windows - row['training_windows']) if available_windows and row['training_windows'] else None
        rows.append({'ref': f'plan_{language}', 'language': language, 'verdict': row['verdict'], 'accuracy': row['accuracy'], 'floor': floor,
                     'training_windows_used': row['training_windows'], 'windows_available_estimate': available_windows, 'unused_headroom_windows': headroom,
                     'volume_ratio_to_strong_median': round(reference_volume / row['training_windows'], 2) if reference_volume and row['training_windows'] else None,
                     'levers': [{'lever': 'max_windows_per_file', 'change': 'raise for this language (today one global value); uses existing files more fully', 'bounded_by': 'windows_available_estimate'},
                                {'lever': 'logit_adjustment_tau', 'change': 'enable class-prior adjustment so rare languages are not under-predicted', 'bounded_by': 'development-set check'},
                                {'lever': 'data', 'change': 'authorize more recordings for this language; existing headroom first, then new authorized sessions', 'bounded_by': 'rights and presenter minimum'},
                                {'lever': 'language_sampling_weights', 'change': 'proposed new recipe parameter; needs worker code review before any run', 'bounded_by': 'recipe approval'}],
                     'evaluation_rule': 'per-stratum floor AND no regression below the base on the sealed held-out set; abstention reported alongside accuracy'})
    request = {'status': 'HELD_awaiting_owner_approval', 'phase': 'train_corrective (non-DP arm) on the admitted GPU host', 'baseline_job_id': REFERENCE_BASELINE,
               'target_languages': targets, 'proposed_recipe_changes': {'max_windows_per_file': 120, 'epochs': 8, 'logit_adjustment_tau': 1.0},
               'compute_cap_gpu_hours': 3.0, 'stop_rule': 'stop when the development accuracy of every target language stops improving for two evaluations or the cap is reached',
               'acceptance': f'every language at or above {floor} on the sealed held-out set with no regression; speaker-identity probe at chance; sealed final set untouched until the end',
               'not_authorized_by_this_plan': True, 'levers_catalogue': LEVERS}
    return {'ref': 'reinforcement_plan', 'targets': rows, 'held_training_request': request, 'scaling_scenarios': scaling(report_data, floor),
            'reading': 'A plan, not an order. Training starts only after the owner approves the recipe, compute cap and evaluation contract.'}


def evidence(floor=0.9):
    data = report(floor)
    if data['status'] != 'measured':
        return data, None
    plan_data = plan(data)
    aggregate = {'weak_language_report': {'ref': 'weak_language_report', 'floor': floor, 'below_floor': data['below_floor'], 'at_risk': data['at_risk'], 'meets_floor': data['meets_floor'],
                                          'languages': {k: {key: v[key] for key in ('ref', 'accuracy', 'abstention_rate', 'judged_windows', 'verdict', 'training_windows', 'training_presenters', 'corpus_hours')} for k, v in data['languages'].items()}},
                 'reinforcement_plan': {'ref': 'reinforcement_plan', 'targets': [{k: t[k] for k in ('ref', 'language', 'verdict', 'training_windows_used', 'windows_available_estimate', 'unused_headroom_windows')} for t in plan_data['targets']],
                                        'proposed_recipe_changes': plan_data['held_training_request']['proposed_recipe_changes'], 'compute_cap_gpu_hours': plan_data['held_training_request']['compute_cap_gpu_hours']},
                 'authority': {'ref': 'owner_scope', 'training_authorized': False, 'recipe_changes_authorized': False, 'music_detector_admitted': False}}
    return data, {'report': data, 'plan': plan_data, 'aggregate': aggregate}


def gpu_hours_estimate(compute):
    curve = compute.get('curve') or []
    elapsed = number((curve[-1] if curve else {}).get('elapsed_s'))
    return round(elapsed / 3600, 2) if elapsed else None

