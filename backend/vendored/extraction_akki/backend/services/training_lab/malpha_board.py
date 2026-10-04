"""M Alpha records composed into the ORIGINAL Train Models board; no new execution plane."""
from services.training_lab import malpha

LANES = {
    'listener': ('M Alpha · Brand listener', 'malpha_listener', 'Recognise spoken brand mentions in Kikuyu, Kamba and Kiswahili.'),
    'story_text': ('M Alpha · Story generation', 'malpha_text', 'Generate coherent stories in Kikuyu, Kamba and Kiswahili; native review required.'),
    'story_voice': ('M Alpha · Invented voice', 'malpha_voice', 'Speak with language character while remaining distinct from corpus presenters.'),
    'story_text_comparison': ('M Alpha · 8B research trial', 'malpha_comparison', 'Measure the registered larger text base; no product-admission authority.'),
}


def _checks(lane, job):
    from services.training_lab.board import NAMES, pct
    dev = (job.get('result') or {}).get('dev') or {}
    if not dev:
        candidates = [(int(k.rsplit('_', 1)[1]), v) for k, v in (job.get('stages') or {}).items() if k.startswith('dev_eval_step_') and k.rsplit('_', 1)[1].isdigit()]
        recent = max(candidates, default=(0, {}))[1]
        dev = recent if lane == 'listener' else {'per_language': recent}
    out = []
    for lang in malpha.LANGUAGES:
        row = (dev.get('mentions') or {}).get(lang) if lane == 'listener' else (dev.get('per_language') or {}).get(lang)
        if not row: continue
        if lane == 'listener': value = f"Precision {pct(row.get('precision'))} · recall {pct(row.get('recall'))} · transcript-derived labels"
        elif lane == 'story_voice':
            identity = row.get('identity_gate') or {}; cosine = identity.get('max_cosine_to_any_corpus_speaker', row.get('max_cosine'))
            similarity = (row.get('behaviour') or {}).get('overall_similarity', row.get('overall_similarity'))
            value = f"Acoustic similarity {pct(similarity)} · maximum identity cosine {cosine if cosine is not None else 'not measured'} · required <0.40"
        else: value = f"Perplexity {row.get('dev_perplexity', '—')} · base {row.get('base_perplexity', '—')} · language proxy {pct(row.get('language_fidelity_rate'))}"
        out.append({'n': NAMES.get(lang, lang), 'v': value, 's': 'diagnostic', 'passes': None, 'label': 'Development only'})
    return out


def runs():
    from services.training_lab.board import _run, _msg, _duration, _n
    from services.training_lab.malpha_evaluation import admission_preflight
    rows = []; records = malpha.jobs(); commissions = {c['commission_id']: c for c in malpha.commissions()}
    support = admission_preflight(records)
    intake = [j for j in records if j['phase'] == 'malpha_internet_corpus' and j['status'] == 'running']
    for job in reversed(records):
        lane = job['lane']
        if lane not in LANES: continue
        name, family, objective = LANES[lane]; result = job.get('result') or {}; p = job.get('progress') or {}
        active = job['status'] in ('running', 'submitting'); completed = job['status'] == 'completed'
        status = 'In training' if job['status'] == 'running' else 'Queued' if active else 'Testing' if completed and malpha._dev_meets_target(lane, result) else 'Refused'
        comparison = lane == 'story_text_comparison'
        if comparison and completed: status = 'Retired'
        reason = '' if active else ('Research trial completed; not a product-admission decision.' if comparison and completed else
                 'Development criteria reached; independent acceptance remains outstanding.' if status == 'Testing' else
                 'Training finished without meeting all development criteria. No product admission.' if completed else 'The worker did not produce an accepted result; its recovery record is retained.')
        step, total = p.get('step'), p.get('of')
        progress = {'step': step, 'of': total, 'elapsed_s': p.get('elapsed_s'), 'basis': 'optimizer_steps'} if type(step) is int and type(total) is int and total > 0 else None
        line = f"{_n(step)} / {_n(total)} optimizer steps · {_duration(p.get('elapsed_s'))}" if progress else (p.get('stage') or job['status']).replace('_', ' ')
        checks = _checks(lane, job)
        compute = result.get('compute') or {}; recipe = job.get('params', {}).get('recipe') or {}
        learning_rate = f"{recipe['lr']:.6g}" if type(recipe.get('lr')) in (int, float) else '—'
        record = [['Recipe', f"Iteration {job['iteration']} · batch {recipe.get('batch_size', '—')} · learning rate {learning_rate}"],
                  ['Compute & time', f"{compute.get('gpu_hours', 'not yet settled')} GPU-hours · monetary GPU rate not recorded"],
                  ['Admission', 'Not admitted · ' + ('research-only comparison' if comparison else 'independent acceptance required')],
                  ['Checks', 'Development diagnostics only; not sealed acceptance or native-language judgement'],
                  ['Authority', 'Existing owner approval · no numeric GPU-hour or iteration ceiling']]
        if lane == 'listener':
            counts = ', '.join(f"{l}: {support['per_language'][l]['positive_segments']}" for l in malpha.LANGUAGES)
            record += [['Evaluation support', f"Sealed positive segments — {counts}. Independent annotation and statistical support remain incomplete."]]
            if support.get('audit_job_id'):
                record += [['Independence audit', 'Not qualified: corpus audit found overlap or incomplete speaker coverage. Existing seals are preserved; independent acceptance is blocked.']]
            if intake:
                amounts = [j.get('progress', {}) for j in intake]
                current_lang = amounts[0].get('language'); matching = [v.get('hours', 0) for v in amounts if v.get('language') == current_lang]
                record += [['Data expansion', f"{max(matching, default=0)} h {current_lang or ''} ingested on the leading host; duplicate host copies not summed. Intake continues."]]
        if lane == 'story_voice': record += [['Identity', 'Rendered voice must remain below 0.40 against complete corpus comparator coverage. No missing renders counted as passes.']]
        if lane in ('story_text', 'story_text_comparison'): record += [['Reference quality', 'Radio-transcript adaptation; qualified story instructions and native story judgements remain outstanding.']]
        borrowed = (commissions.get('STORY-KIK-KAM-SWA') or {}).get('capacity_reallocation') or {}
        if comparison: record += [['Serving', 'Resident LID temporarily unloaded; restoration pending after this trial.' if borrowed.get('status') == 'borrowed' else 'See the native serving record.']]
        messages = [_msg(job.get('started_at') or job.get('submitted_at'), f"Owner-authorised {name.split(' · ', 1)[1].lower()} iteration {job['iteration']}. No active training is interrupted.")]
        if active: messages.append(_msg((job.get('last_status_rpc') or {}).get('at'), line, widget='status', status_label=p.get('stage', 'Training'), status_line=line))
        if checks: messages.append(_msg(job.get('finished_at'), 'Latest recorded development measurements. These do not establish admission.', widget='checks'))
        messages.append(_msg(job.get('finished_at'), reason or 'Current run record and remaining acceptance conditions.', widget='record'))
        rows.append(_run(run_id=job['job_id'], family=family, name=f"{name} v{job['iteration']}", status=status, objective=objective,
            reason=reason, messages=messages, checks=checks, checks_title='Development diagnostics · not sealed acceptance',
            record_rows=record, progress=progress, eta=line if active else reason, meta=f"Iteration {job['iteration']} · {job['host']} GPU {job['gpu_index']}",
            started_at=job.get('started_at') or job.get('submitted_at'), finished_at=job.get('finished_at'),
            read_only_execution=True, learnings='Quality and identity gates remain unchanged. More training or lower loss alone does not establish success.',
            evidence={'status': status, 'training_authorized': True, 'product_admitted': False, 'research_only': comparison,
                      'iteration': job['iteration'], 'progress': progress, 'development_only': True}))
    return rows