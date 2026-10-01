"""The owner's Train Models board, read from live records only. Statuses use the owner's vocabulary; no raw identifiers
are surfaced in display fields. Nothing here starts, stops or approves training."""
from services.training_lab import store as lab
from services.training_lab.evidence import number

NAMES = {'guz': 'Ekegusii', 'kam': 'Kikamba', 'kik': 'Gikuyu', 'kln': 'Kalenjin', 'luo': 'Dholuo', 'lwg': 'Luhya (Wanga)', 'swa': 'Kiswahili',
         'eng': 'English', 'sheng': 'Sheng', 'bxk': 'Bukusu'}
BASES = {'qwen3-8b-base': '8B', 'qwen3-1.7b-base': '1.7B'}
BASE_NAMES = {'qwen3-8b-base': 'Qwen3 8B base', 'qwen3-1.7b-base': 'Qwen3 1.7B base'}
FINISHED = ('In service', 'Refused', 'Retired')


def pct(value, digits=1):
    return '—' if number(value) is None else f'{value * 100:.{digits}f}%'


def _n(value):
    return '—' if number(value) is None else f'{value:,.0f}' if float(value).is_integer() else f'{value:,.2f}'


def _duration(seconds):
    seconds = number(seconds)
    if seconds is None: return '—'
    minutes = int(round(seconds / 60))
    return f'{minutes} min' if minutes < 90 else f'{minutes // 60} h {minutes % 60:02d} min'


def _base_label(base):
    return BASES.get(base, base or 'base model')


def _run(**fields):
    base = {'kind': 'run', 'messages': [], 'checks': [], 'record_rows': [], 'reflect_rows': [], 'sources': [], 'learnings': '', 'reason': '',
            'baseline_card': None, 'approval': None, 'progress': None, 'eta': '', 'meta': '', 'actions': [], 'evidence': {}, 'whitepaper': None,
            'health': None, 'started_at': None, 'finished_at': None, 'deletable': False, 'ready': False}
    base.update(fields)
    return base


def _msg(at, text, **extra):
    return {'role': 'akki', 'origin': 'record', 'at': at, 'text': text, **extra}


# ----------------------------------------------------------------------------- text language identification (M9)
def _text_runs():
    from services.training_runner import m9_dispatch, m9_serving, m9_readjudication
    adapters = {a['training_job_id']: [] for a in m9_serving.models_view()['trained_adapters']}
    for adapter in m9_serving.models_view()['trained_adapters']:
        adapters.setdefault(adapter['training_job_id'], []).append(adapter)
    readj = {}
    for record in m9_readjudication.list_records():
        readj.setdefault(record['job_id'], record)
    out = []
    for job in m9_dispatch.list_jobs():
        if job.get('phase') != 'train': continue
        result = ((job.get('receipt') or {}).get('result')) or {}
        cert = job.get('run_certificate') or {}
        if not cert and job['status'] != 'running': continue  # smoke and recovery drills are recorded under Model Approval, not as models
        params = job.get('params') or {}
        base = _base_label(params.get('base'))
        name = f'Language identification · {base} text model'
        objective = 'Identify the language of RMS transcript text across seven languages on a sealed held-out set, with abstention reported beside accuracy.'
        training = result.get('training') or cert.get('compute') or {}
        held = ((result.get('adapter_eval') or {}).get('held') or {})
        strata = held.get('per_stratum') or {}
        base_held = (((result.get('base_eval') or {}).get('held') or {}).get('per_stratum') or {})
        admission = cert.get('admission_current') or cert.get('admission') or {}
        decision = readj.get(job['job_id'])
        own = adapters.get(job['job_id'], [])
        served = [a for a in own if (a.get('serving') or {}).get('status') == 'running']
        status, reason = 'Retired', ''
        if job['status'] == 'completed' and cert:
            if admission.get('outcome') == 'admitted': status = 'In service'
            elif admission.get('outcome') == 'refused':
                status = 'Refused'; failing = [NAMES.get(k, k) for k, v in ((decision or {}).get('per_stratum') or {}).items() if not v.get('passes')]
                reason = ('Admission refused: ' + (', '.join(failing) + ' regressed below the base model on the sealed held-out set.' if failing else (admission.get('refusal_note') or 'a measured criterion fell below its floor.')))
            else: reason = 'Completed without seeking admission.'
        elif job['status'] == 'completed': reason = 'Completed as a drill; no certificate or admission was sought.'
        elif job['status'] == 'interrupted': reason = 'Interrupted on purpose as a recovery drill; resumed work is recorded on the parent run.'
        elif job['status'] == 'failed': reason = 'The run stopped before producing a result.'
        elif job['status'] == 'cancelled': reason = 'Cancelled before completion.'
        elif job['status'] == 'running': status = 'In training'
        checks = []
        floor = (decision or {}).get('outcome_floor', 0.9)
        for code in sorted(strata):
            row = strata[code]; per = ((decision or {}).get('per_stratum') or {}).get(code) or {}
            base_acc = per.get('base_accuracy', (base_held.get(code) or {}).get('accuracy'))
            checks.append({'n': NAMES.get(code, code), 'v': f"{pct(row.get('accuracy'))} · floor {pct(floor, 0)} · base {pct(base_acc)} · abstained {pct(row.get('abstention_rate'))}", 's': 'settled',
                           'passes': per.get('passes', (number(row.get('accuracy')) or 0) >= floor)})
        recipe = training.get('recipe') or params.get('recipe') or {}
        record_rows = []
        if training:
            record_rows = [['Baseline', f"{BASE_NAMES.get(params.get('base'), params.get('base') or 'base model')} · licence verified at acquisition"],
                           ['Recipe', f"LoRA r{recipe.get('lora_r', '—')} · {training.get('epochs_completed', recipe.get('epochs', '—'))} epochs · {recipe.get('optimizer', '—')} · learning rate {recipe.get('lr', '—')}"],
                           ['Data', f"RMS transcripts · {_n(training.get('train_units'))} training units · {_n(training.get('train_tokens'))} tokens · sealed held-out {_n(held.get('units'))} units"],
                           ['Compute & time', f"{training.get('gpu_hours', '—')} GPU-hours on one {training.get('device', 'GPU')} · {_duration(training.get('wallclock_seconds'))}"]]
            passing = sum(1 for c in checks if c['passes'])
            if checks: record_rows.append(['Checks', f'{passing} of {len(checks)} languages at or above the floor with no regression below the base'])
            moac = result.get('moac') or {}
            if number(moac.get('m_a_improvement')) is not None:
                record_rows.append(['Improvement over the base', f"{moac['m_a_improvement'] * 100:+.1f} points macro accuracy · calibration error {moac.get('m_e_calibration_ece', '—')}"])
            if admission: record_rows.append(['Admission', f"{admission.get('outcome', 'not sought')}" + (f" · {admission.get('refusal_note')}" if admission.get('refusal_note') else '')])
            if own: record_rows.append(['Serving', ', '.join(f"{a['variant']} adapter {'served on ' + a['serving']['host'] if a.get('serving') and a['serving'].get('status') == 'running' else 'admitted, not served'}" for a in own)])
        learnings = ''
        if checks:
            weakest = min(checks, key=lambda c: number(strata.get(next(k for k in strata if NAMES.get(k, k) == c['n']), {}).get('accuracy')) or 0)
            learnings = (f"{sum(c['passes'] for c in checks)} of {len(checks)} measured language strata met the recorded accuracy/no-regression criteria. {weakest['n']} had the lowest measured accuracy. "
                         + ('The owner\'s per-stratum ruling admitted the adapter after re-reading each language against the base. ' if admission.get('outcome') == 'admitted' else '')
                         + 'These observations describe this run; they do not establish general cognition or causation.')
        messages = [_msg(job.get('submitted_at'), f"Training started on {job.get('host', 'the GPU host')} from {BASE_NAMES.get(params.get('base'), params.get('base') or 'the base model')}: {recipe.get('epochs', '—')} epochs over the RMS transcript corpus, held-out set sealed before the first step.",
                        think=['The held-out set was sealed before training and never re-drawn.', 'Rights reference recorded with the corpus; no new source was read.'])]
        for event in ((job.get('remote_state') or {}).get('events') or [])[:3]:
            messages.append(_msg(event.get('at'), event.get('message', '').capitalize() + '.'))
        if job.get('finished_at') and training:
            messages.append(_msg(job['finished_at'], f"Training compute finished — {_duration(training.get('wallclock_seconds'))} on one {training.get('device', 'GPU')}. The per-language checks ran against the sealed held-out set; nobody can override the result, including me.", widget='checks'))
        if status == 'Refused':
            messages.append(_msg(cert.get('certified_at') or job.get('finished_at'), reason or 'The recorded acceptance decision refused this candidate.', widget='refused'))
        elif status == 'In service':
            messages.append(_msg(admission.get('computed_at') or job.get('finished_at'), f"Admitted under the owner's per-stratum ruling. Here is the full record.", widget='record'))
            if (cert.get('whitepaper') or {}).get('drafted'):
                messages.append(_msg(admission.get('computed_at') or job.get('finished_at'), 'A white paper was drafted from this run\'s own record; it cites the admission and the baseline line.', widget='suggest'))
            messages.append(_msg(admission.get('computed_at') or job.get('finished_at'), 'To improve on it, open the next version. This one keeps its record, its status and its calls.', widget='remodel'))
        elif reason:
            messages.append(_msg(job.get('finished_at') or job.get('submitted_at'), reason))
        out.append(_run(run_id=job['job_id'], family='text', name=name, status=status, objective=objective, reason=reason, checks=checks, record_rows=record_rows, learnings=learnings, messages=messages,
                        meta=f"{base} base · {job.get('host', '')}" + (f" · admitted {admission.get('computed_at', '')[:10]}" if admission.get('outcome') == 'admitted' else ''),
                        started_at=job.get('started_at') or job.get('submitted_at'), finished_at=job.get('finished_at'), eta=_eta(status, reason),
                        whitepaper=cert.get('whitepaper') if (cert.get('whitepaper') or {}).get('drafted') else None,
                        health={'model_id': served[0]['model_id']} if served else None,
                        evidence={'task': 'text language identification', 'base': params.get('base'), 'per_language_held_out': {NAMES.get(k, k): {'accuracy': v.get('accuracy'), 'abstention_rate': v.get('abstention_rate'), 'judged': v.get('judged')} for k, v in strata.items()},
                                  'training': {k: training.get(k) for k in ('train_units', 'train_tokens', 'epochs_completed', 'gpu_hours', 'wallclock_seconds', 'device')}, 'admission': admission.get('outcome'), 'status': status}))
    return out


def _eta(status, reason=''):
    return {'In service': 'complete', 'Refused': 'stopped at acceptance', 'Retired': 'stopped' if reason else 'retired', 'In training': 'training', 'Testing': 'checks running',
            'Queued': 'waiting for a slot', 'In Approval': 'waiting on your approval', 'Shaping': 'not started — no training compute spent'}.get(status, '')


# ----------------------------------------------------------------------------- audio language cognition (LC)
def _audio_runs():
    from services.audio_plane_v1 import language_cognition_dispatch as lc
    out = []
    for job in lc.list_jobs():
        if job.get('phase') not in ('train_baseline', 'train_corrective'): continue
        cert = job.get('run_certificate') or {}
        if not cert and job['status'] not in ('running', 'submitting', 'queued'): continue
        params = job.get('params') or {}; recipe = params.get('recipe') if isinstance(params.get('recipe'), dict) else params
        compute = cert.get('compute') or {}
        epochs = compute.get('epochs_completed') or recipe.get('epochs')
        arm = 'baseline' if job['phase'] == 'train_baseline' else ('differentially private corrective' if cert.get('dp_sgd') else 'corrective')
        name = f"Audio language model · {arm}" + (f" · {epochs} epochs" if epochs else '')
        verdict = cert.get('verdict') or ''
        if job['status'] == 'completed' and cert:
            status = 'Refused' if verdict.upper().startswith('NOT ADMISSIBLE') else 'Retired'
            reason = verdict.split('—', 1)[-1].strip().rstrip('.') + '.' if '—' in verdict else (verdict or 'Completed; admission was not sought.')
            reason = 'Not admissible: ' + reason[0].lower() + reason[1:] if status == 'Refused' else reason
        elif job['status'] == 'running': status, reason = 'In training', ''
        elif job['status'] in ('submitting', 'queued'): status, reason = 'Queued', ''
        else: status, reason = 'Retired', {'failed': 'The run stopped before producing a result.', 'cancelled': 'Cancelled before completion.'}.get(job['status'], 'Stopped.')
        strata = cert.get('per_stratum') or {}
        checks = [{'n': NAMES.get(k, k), 'v': f"{pct(v.get('accuracy'))} · floor 90% · abstained {pct(v.get('abstention_rate'))}", 's': 'settled', 'passes': (number(v.get('accuracy')) or 0) >= 0.9}
                  for k, v in sorted(strata.items()) if isinstance(v, dict)]
        touched = ((cert.get('data_touched') or {}).get('per_language') or {})
        windows = sum(number(v.get('windows_train')) or 0 for v in touched.values() if isinstance(v, dict))
        record_rows = []
        if compute:
            record_rows = [['Recipe', f"{epochs or '—'} epochs · batch {compute.get('batch_size', recipe.get('batch_size', '—'))} · learning rate {compute.get('lr', recipe.get('lr', '—'))}" + (' · differential privacy' if cert.get('dp_sgd') else '')],
                           ['Data', f"{_n(windows)} four-second training windows across {len(touched)} languages · staged authorized audio"],
                           ['Compute', f"{_duration(compute.get('elapsed_seconds'))}" + (f" · {_n(compute.get('windows_per_second'))} windows/s" if compute.get('windows_per_second') else '') + (f" · peak {compute.get('gpu_max_memory_gb')} GB GPU memory" if compute.get('gpu_max_memory_gb') else '')],
                           ['Checks', f"{sum(c['passes'] for c in checks)} of {len(checks)} languages at or above the floor"]]
            if (cert.get('dp_sgd') or {}).get('epsilon') is not None: record_rows.append(['Privacy budget', f"ε {cert['dp_sgd']['epsilon']}"])
            privacy = (cert.get('sealed_contract_check') or {}).get('no_speaker_id_probe') or {}
            if privacy:
                reading = privacy.get('strict_chance_met')
                record_rows.append(['Speaker privacy', 'Chance-level criterion met' if reading is True else 'Speaker recovery remained above the required chance level' if reading is False else 'Not established by this record'])
        messages = [_msg(job.get('submitted_at'), f"{'Baseline' if job['phase'] == 'train_baseline' else 'Corrective'} audio run started on the GPU host over the staged corpus" + (f" · {epochs} epochs" if epochs else '') + '.')]
        if job.get('finished_at') and checks:
            messages.append(_msg(job['finished_at'], 'Training finished; per-language accuracy on the sealed held-out set, abstention beside it.', widget='checks'))
        if reason: messages.append(_msg(job.get('finished_at') or job.get('submitted_at'), reason if status != 'Refused' else 'The verdict is recorded with the run and travels with it.', widget='refused' if status == 'Refused' else None))
        out.append(_run(run_id=job['job_id'], family='audio', name=name, status=status, objective='Identify the spoken language of four-second windows of staged RMS audio, with abstention; speaker identity must stay unrecoverable.',
                        reason=reason, checks=checks, record_rows=record_rows, messages=messages, meta=f"{job.get('host', 'GPU host')} · {arm}", started_at=job.get('started_at') or job.get('submitted_at'), finished_at=job.get('finished_at'), eta=_eta(status, reason),
                        evidence={'task': 'audio language identification', 'arm': arm, 'per_language_held_out': {NAMES.get(k, k): {'accuracy': v.get('accuracy'), 'abstention_rate': v.get('abstention_rate')} for k, v in strata.items() if isinstance(v, dict)},
                                  'compute': {k: compute.get(k) for k in ('epochs_completed', 'steps', 'elapsed_seconds', 'windows_per_second')}, 'verdict': verdict, 'status': status}))
    return out


# ----------------------------------------------------------------------------- held reinforcement request
def _reinforcement_run(tenant):
    from services.training_lab import languages
    data, bundle = languages.evidence(0.9)
    if bundle is None: return None
    plan = bundle['plan']; request = plan['held_training_request']
    targets = [NAMES.get(t, t) for t in request['target_languages']]
    if not targets: return None
    first = plan['targets'][0]; lang = data['languages'][first['language']]
    reviews = list(lab.db().training_lab_runs.find({'tenant_id': tenant, 'kind': 'weak_language_plan'}, {'_id': 0}).sort('created_at', -1).limit(3))
    latest = reviews[0] if reviews else None
    checks = [{'n': NAMES.get(k, k), 'v': f"{pct(v['accuracy'])} ({pct(v['interval']['low'], 0)}–{pct(v['interval']['high'], 0)}) · floor {pct(data['floor'], 0)} · abstained {pct(v['abstention_rate'])}", 's': 'settled', 'passes': v['verdict'] == 'meets_floor'}
              for k, v in data['languages'].items() if v.get('interval')]
    changes = request['proposed_recipe_changes']
    reflect = [{'k': 'What it does', 'v': f"Lifts {', '.join(targets)} to the {pct(data['floor'], 0)} floor on the sealed held-out set without regressing the other languages", 't': 'measured gap'},
               {'k': 'Where it stands', 'v': f"{pct(lang['accuracy'])} today on {lang['judged_windows']:,} judged windows · trained on {lang['training_windows']:,} windows" + (f" · strong languages trained on {first['volume_ratio_to_strong_median']}× more" if first.get('volume_ratio_to_strong_median') else ''), 't': 'measured'},
               {'k': 'What it reads', 'v': f"Existing staged recordings first — about {first['windows_available_estimate']:,} windows available, {first['unused_headroom_windows']:,} unused — then newly authorized sessions" if first.get('windows_available_estimate') else 'Existing staged recordings; new sessions only when authorized', 't': 'estimate'},
               {'k': 'Recipe changes', 'v': f"{changes['max_windows_per_file']} windows per file (one global value today) · {changes['epochs']} epochs · class-prior adjustment τ {changes['logit_adjustment_tau']} · language sampling weights proposed for code review", 't': 'proposal'},
               {'k': 'Compute cap', 'v': f"{request['compute_cap_gpu_hours']} GPU-hours on the admitted host · non-private arm", 't': 'proposal'},
               {'k': 'Stop rule', 'v': request['stop_rule'][0].upper() + request['stop_rule'][1:], 't': 'proposal'},
               {'k': 'How we\'ll know', 'v': request['acceptance'][0].upper() + request['acceptance'][1:], 't': 'contract'}]
    scaling = plan.get('scaling_scenarios') or {}
    if scaling and not scaling.get('unavailable'):
        reflect.append({'k': 'Windows to the floor', 'v': f"About {scaling['low']:,}–{scaling['high']:,} (middle {scaling['mid']:,}), from the cross-language scaling of the reference run — prior sensitivity, not a forecast", 't': 'estimate'})
    messages = [_msg(None, f"Read from the measured baseline certificate: {', '.join(targets)} {'sits' if len(targets) == 1 else 'sit'} below the {pct(data['floor'], 0)} floor; every other language clears it.", widget='checks',
                     think=['Accuracy is on judged windows; abstention is shown beside it.', 'Intervals are Wilson scores on the held-out windows.', data['corrective_runs_note']]),
                _msg(None, 'Here is what the reinforcement commits to. It is a plan, not an order.', widget='reflect'),
                _msg(None, 'Training stays held until you approve the recipe, compute cap and evaluation contract through Model Approval.', widget='approval'),
                _msg(None, 'When you want this trained, say so here. It is recorded as your request and travels to Model Approval; nothing starts from this page.', widget='begin')]
    if latest:
        for review in latest.get('reviews') or []:
            if review.get('status') in ('complete', 'review_required') and review.get('review'):
                findings = review['review'].get('findings') or []
                text = ' '.join(f"{f['observation']} {f['recommendation']}" for f in findings[:2])
                messages.append(_msg(latest.get('finished_at') or latest.get('updated_at'), f"{review['role'].replace('_', ' ').capitalize()}: {text}", think=['Advisory only, machine-checked for ungrounded numbers; not independent expert validation.'] + ([f"{len(review.get('quality_flags') or [])} flag(s) for figures stated in prose."] if review.get('quality_flags') else [])))
            elif review.get('status') == 'unavailable':
                messages.append(_msg(latest.get('finished_at') or latest.get('updated_at'), f"{review['role'].replace('_', ' ').capitalize()}: advice unavailable; no substitute opinion was generated."))
    return _run(run_id='reinforcement-lwg', family='reinforcement', name=f"{', '.join(targets)} reinforcement · audio language model", status='In Approval',
                objective=f"Bring {', '.join(targets)} to the {pct(data['floor'], 0)} floor on the sealed held-out set with no regression elsewhere and speaker identity at chance.",
                checks=checks, reflect_rows=reflect, messages=messages, meta='held training request · recipe and cap recorded', eta='waiting on your approval',
                approval={'line': 'Held for your approval · recipe, data, compute cap and acceptance recorded', 'reviews': 'reviewing' if latest and latest.get('status') in ('queued', 'reviewing') else ('reviewed' if latest else 'not yet asked')},
                actions=['ask_specialists'], evidence=bundle['aggregate'] | {'status': 'In Approval', 'held': True})


# ----------------------------------------------------------------------------- music identification (shaping)
def _music_run(tenant):
    from services.training_lab import corpus_measurement, languages
    from services.media_library import reference_import
    baselines = list(lab.db().training_lab_runs.find({'tenant_id': tenant, 'kind': 'music_baseline'}, {'_id': 0}).sort('created_at', -1).limit(5))
    latest = baselines[0] if baselines else None
    measurement = corpus_measurement.latest(tenant)
    reference = reference_import.latest(tenant)
    result = (latest or {}).get('result') if latest and latest.get('status') == 'complete' else None
    messages = [_msg(None, 'Objective: tell music from speech, and mixed from both, in the recordings the estate holds — measured first, trained only if the measured baseline is not enough.',
                     think=['Every recording is reduced to measured sound observables; no audio leaves its host.', 'A baseline is the number a trained detector must beat.'])]
    card = None; checks = []
    if result and result.get('status') == 'complete':
        learned, reading = result['baseline_learned'], result['baseline_reading']
        card = {'name': 'Learned on the measured observables', 'because': 'It is fitted to the recordings you labelled and tested file by file, leaving one out each time.',
                'evidence': f"Accuracy {pct(learned['accuracy'])} · finds music {pct(learned['recall'])} · right when it says music {pct(learned['precision'])} · on {result['items']} labelled recordings",
                'alts': [{'name': 'The acoustic reading', 'because': 'Cue scoring over the measured observables — no fitting, so nothing to overfit.', 'evidence': f"Accuracy {pct(reading['accuracy'])} · finds music {pct(reading['recall'])} · right when it says music {pct(reading['precision'])}"}]}
        checks = [{'n': 'Accuracy', 'v': f"{pct(learned['accuracy'])} learned · {pct(reading['accuracy'])} reading", 's': 'settled', 'passes': True},
                  {'n': 'Finds music (recall)', 'v': f"{pct(learned['recall'])} learned · {pct(reading['recall'])} reading", 's': 'settled', 'passes': True},
                  {'n': 'Right when it says music (precision)', 'v': f"{pct(learned['precision'])} learned · {pct(reading['precision'])} reading", 's': 'settled', 'passes': True},
                  {'n': 'Clears non-music (specificity)', 'v': f"{pct(learned['specificity'])} learned · {pct(reading['specificity'])} reading", 's': 'settled', 'passes': True}]
        window = result.get('window_level')
        if window:
            checks.append({'n': 'Per four-second window', 'v': f"{pct(window['reading']['accuracy'])} reading · {pct(window['learned_grouped_5fold']['accuracy'])} learned · {window['windows']:,} windows", 's': 'settled', 'passes': True})
        corpus_test = result.get('corpus_test')
        if corpus_test:
            share = sum(v.get('files_with_music_windows', 0) for v in corpus_test['per_language'].values())
            checks.append({'n': 'Staged corpus test', 'v': f"{corpus_test['files']:,} recordings · {share:,} with music-like windows for review", 's': 'settled', 'passes': True})
        messages.append(_msg(latest.get('finished_at'), f"Baseline established on {result['items']} labelled recordings — {result['positives']} with music, {result['negatives']} without. Here is where I'd start.", widget='baseline'))
        messages.append(_msg(latest.get('finished_at'), 'The checks a trained detector would have to beat.', widget='checks'))
    elif latest and latest.get('status') == 'waiting_measurements':
        pending = (latest.get('reference_set') or {}).get('pending') or []
        messages.append(_msg(latest.get('created_at'), f"Baseline requested; still measuring {len(pending)} recording{'s' if len(pending) != 1 else ''} in the library before it can be established.", widget='status', status_label='Measuring', status_line=f"{len(pending)} recordings still being measured · the baseline completes on its own"))
    elif latest and latest.get('result') and latest['result'].get('status') != 'complete':
        messages.append(_msg(latest.get('finished_at'), latest['result'].get('reason', 'The baseline could not be established yet.')))
    else:
        messages.append(_msg(None, 'No baseline yet. Say "run the baseline" and I\'ll measure it on the labelled recordings in the library — reference speech and your music, kept apart.'))
    sources = []
    hours = languages._corpus_hours()
    per_language = ((measurement or {}).get('result') or {}).get('per_language') or {}
    for code in sorted(set(hours) | set(per_language)):
        m = per_language.get(code) or {}
        detail = f"{m['measured']:,} recordings · {m['hours']} h · {m['files_with_music_windows']:,} with music-like windows" if m else f"{round(hours[code], 1) if number(hours.get(code)) is not None else '—'} h of staged audio · not yet measured for music"
        sources.append({'n': f"Staged corpus · {NAMES.get(code, code)}", 'v': detail, 'cls': 'Internal'})
    items = ((reference or {}).get('import') or {}).get('items') or []
    stored = [i for i in items if i.get('status') in ('imported', 'already_imported')]
    if stored:
        sources.append({'n': 'Public-domain reference recordings', 'v': f"{sum(1 for i in stored if i.get('label') == 'speech')} speech · {sum(1 for i in stored if i.get('label') == 'music')} music · LibriVox and Musopen, never counted as training data", 'cls': 'Licensable'})
    if sources: messages.append(_msg(None, 'What it reads — staged RMS audio and the public-domain references, each with its rights class.', widget='sources'))
    progress = None
    if measurement and measurement.get('status') == 'running':
        p = measurement.get('progress') or {}
        progress = {'files': p.get('files'), 'of': p.get('of'), 'elapsed_s': p.get('elapsed_s')}
        messages.append(_msg(measurement.get('submitted_at'), f"Measuring the staged corpus on {measurement.get('host', 'the GPU host')} — readings only; no training and no media leaves the host.", widget='status', status_label='Measuring',
                             status_line=f"{(p.get('files') or 0):,} of {(p.get('of') or 0):,} recordings · {int((p.get('elapsed_s') or 0) // 60)} min so far"))
    elif measurement and measurement.get('status') == 'completed':
        r = measurement['result']
        messages.append(_msg(measurement.get('finished_at'), f"Staged corpus measured: {r['measured']:,} of {r['files']:,} recordings in {_duration(r.get('compute_seconds'))} on {measurement.get('host', 'the GPU host')}."))
    elif measurement and measurement.get('status') == 'failed':
        messages.append(_msg(measurement.get('finished_at'), f"The corpus measurement did not finish: {measurement.get('reason', 'no verified receipt')}."))
    if (reference or {}).get('import', {}).get('status') == 'running':
        messages.append(_msg(None, f"Importing public-domain reference recordings · {len(stored)} stored so far."))
    actions = ['run_music_baseline', 'measure_staged_corpus', 'import_reference_recordings']
    eta = f"measuring the staged corpus · {progress['files'] or 0:,} of {progress['of'] or 0:,} recordings" if progress else 'not started — no training compute spent'
    return _run(run_id='music-identification', family='music', name='Music identification · staged audio', status='Shaping',
                objective='Tell music from speech, and mixed from both, in the recordings the estate holds; establish the measured baseline a trained detector must beat.',
                messages=messages, baseline_card=card, checks=checks, sources=sources, progress=progress, eta=eta, actions=actions,
                meta='measured baseline · staged corpus on akki-vm', started_at=(latest or {}).get('created_at'),
                evidence={'status': 'Shaping', 'baseline': {k: result[k] for k in ('items', 'positives', 'negatives', 'baseline_reading', 'baseline_learned', 'window_level', 'limitations') if k in result} if result else None,
                          'corpus_measurement': {'status': (measurement or {}).get('status'), 'progress': progress, 'per_language': {NAMES.get(k, k): {kk: v.get(kk) for kk in ('measured', 'hours', 'files_with_music_windows', 'music_windows', 'windows')} for k, v in per_language.items()}},
                          'corpus_hours_by_language': {NAMES.get(k, k): v for k, v in hours.items()}, 'reference_recordings': {'stored': len(stored), 'status': ((reference or {}).get('import') or {}).get('status')},
                          'music_detector_trained': False, 'training_authorized': False})


def _versioned(rows):
    """Owner lineage convention: same family name → v1, v2 … in the order the runs were submitted."""
    groups = {}
    for row in sorted(rows, key=lambda r: r.get('started_at') or ''):
        groups.setdefault(row['name'], []).append(row)
    for name, members in groups.items():
        if len(members) > 1:
            for index, row in enumerate(members, 1): row['name'] = f'{name} v{index}'
    return rows


# ----------------------------------------------------------------------------- runs the owner opened here
def _owner_runs(tenant):
    from services.training_lab import board_runs
    from services.training_lab import production
    out = []
    for doc in board_runs.list_runs(tenant):
        fields = doc.get('fields') or {}
        filled = [(label, fields[key]) for key, label in board_runs.FIELDS if fields.get(key)]
        ready = board_runs.ready(doc)
        status = doc['status']
        reflect = [{'k': label, 'v': value, 't': 'you said'} for label, value in filled]
        rows = [[label, value] for label, value in filled]
        plan = production.for_run(tenant, doc['run_id'])
        definition = doc.get('definition') or {}
        if definition:
            target = definition['target_outcome']
            artifact_rows = [['Target outcome', target['task']], ['Population', target['population_register_ref']],
                ['Per-stratum acceptance', '; '.join(f"{k}: accuracy {v['accuracy']:.1%}, coverage {v['coverage']:.1%}" for k, v in target['acceptance'].items())],
                ['Collection schema', ', '.join(definition['collection_schema']['baseline_tier'] + definition['collection_schema']['objective_tier'])]]
            rows.extend(artifact_rows)
            reflect.extend({'k': k, 'v': v, 't': 'you said'} for k, v in artifact_rows)
        if plan:
            rows.extend([['Production plan', plan['plan_id']], ['Next step', plan['status'].replace('_', ' ')]])
        if doc.get('lineage'): rows.append(['Lineage', 'Opened from an earlier run; that run keeps its own record'])
        messages = []
        if status == 'In Approval':
            messages.append(_msg(doc.get('held_at'), 'Held for your approval. Here is what you committed to.', widget='reflect'))
            messages.append(_msg(doc.get('held_at'), 'Training stays held until the recipe, compute cap and evaluation contract are approved through Model Approval.', widget='approval'))
        out.append(_run(run_id=doc['run_id'], family='owner', name=doc['name'], status=status, objective=fields.get('produces') or 'Objective still forming',
                        reflect_rows=reflect, record_rows=rows, messages=messages, meta='opened here · ' + (f'{len(filled)} of {len(board_runs.FIELDS)} fields set' if status == 'Shaping' else 'held training request'),
                        eta='ready to record' if ready and status == 'Shaping' else _eta(status), started_at=doc.get('created_at'),
                        actions=['record_training_request'] if ready and status == 'Shaping' else [],
                        approval={'line': 'Target outcome and collection schema recorded; calibration precedes the full-run quote.', 'reviews': 'not yet asked'} if status == 'In Approval' else None,
                        evidence={'status': status, 'fields': fields, 'fields_needed': [label for key, label in board_runs.FIELDS if not fields.get(key)], 'ready': ready, 'lineage': doc.get('lineage'),
                                  'definition': definition, 'production': plan, 'training_authorized': False, 'compute_spent': False}, deletable=status == 'Shaping', ready=ready))
    return out


def _apply_retirements(tenant, rows):
    from services.training_lab import board_runs
    retired = board_runs.retired(tenant)
    for row in rows:
        mark = retired.get(row['run_id'])
        if mark and row['status'] in ('Refused', 'In service', 'Retired'):
            row['retired_from'] = row['status']
            row['status'] = 'Retired'; row['eta'] = 'retired'
            row['reason'] = f"Retired by the owner on {mark['retired_at'][:10]}. " + (row['reason'] if row.get('reason') else 'Its record stays as written.')
            row['messages'] = row['messages'] + [_msg(mark['retired_at'], 'Retired by the owner. The record, the checks and the reason stay exactly as written; only the status changed.')]
            row['evidence'] = (row.get('evidence') or {}) | {'status': 'Retired', 'retired_at': mark['retired_at']}
    return rows


def runs(tenant):
    rows = []
    if tenant == 'RMS':
        music = _music_run(tenant)
        if music: rows.append(music)
        held = _reinforcement_run(tenant)
        if held: rows.append(held)
        rows.extend(_versioned(_text_runs())); rows.extend(_versioned(_audio_runs()))
    rows = _owner_runs(tenant) + rows
    return _apply_retirements(tenant, rows)


def board(tenant):
    rows = runs(tenant)
    counts = {status: sum(1 for r in rows if r['status'] == status) for status in ('Shaping', 'In Approval', 'Queued', 'In training', 'Testing', 'In service', 'Refused', 'Retired')}
    return {'runs': rows, 'counts': counts, 'training_authorized': False, 'music_detector_admitted': False}
