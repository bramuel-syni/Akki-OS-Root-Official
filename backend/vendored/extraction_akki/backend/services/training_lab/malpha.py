"""Mα control plane: two commissioned three-language products (STORY-KIK-KAM-SWA, LISTEN-KIK-KAM-SWA) run as autonomous, uncapped-until-billing
improvement loops on the admitted GPU hosts. Every lane job is an m9 governed job (hashed worker bundle, host receipt, bounded status RPC);
this module decides what runs next from measured dev results, meters GPU hours, keeps the sealed admission split for the independent
evaluation phase only, and writes every transition to the White Paper Wizard notebook. Uncapped is a recorded authority, never a number."""
import hashlib
import json
import logging
import math
import os
import re

from services.training_lab import brand_catalogue
from services.training_lab import store as lab
from services.wpw import tier1_notebook as wpw

log = logging.getLogger(__name__)
TENANT = 'RMS'
LANGUAGES = ('kik', 'kam', 'swa')
AIP_DB_NAME = 'aip_db_v1'
BUDGET_MODE = 'uncapped_until_billing'
OWNER_ORDER_REF = ('owner order 2026-10-04 (Mα): no GPU cap and no iteration ceiling until billing data; two three-language products — expressive spoken storyteller and '
                   'radio brand listener (kik, kam, swa); audio as a database; admission target 90%; Spending A: existing hardware only')
INTERNET_DATA_ORDER_REF = 'owner order 2026-10-04: "Attached is the brand list the media mention model needs to track. You can also train from the internet data."'
RESIDENT_PROTECTED_MIB = 4096
HOST_ALLOCATION = {'malpha_aip_build': [('akki-vm', 0), ('akki-vm-ii', 0)], 'malpha_aip_requalify': [('akki-vm', 0), ('akki-vm-ii', 0)], 'malpha_listener_train': [('akki-vm', 0)], 'malpha_voice_train': [('akki-vm', 1)],
                   'malpha_story_text_train': [('akki-vm-ii', 0)], 'malpha_baseline_render': [('akki-vm-ii', 0), ('akki-vm', 0), ('akki-vm', 1)], 'malpha_evaluate': [('akki-vm', 0), ('akki-vm', 1), ('akki-vm-ii', 0)],
                   'malpha_aip_relabel': [('akki-vm', 0), ('akki-vm-ii', 0)], 'malpha_internet_corpus': [('akki-vm', 0), ('akki-vm-ii', 0)]}
CPU_PHASES = ('malpha_aip_requalify', 'malpha_aip_relabel', 'malpha_internet_corpus', 'malpha_worker_audit')  # no GPU lock; they run beside a training job on the same host
MIN_DEV_SEGMENTS, MIN_DEV_MENTION_SEGMENTS = 300, 30
SEED = 20261004
INTERNET_MAX_HOURS_PER_DATASET = None  # owner expansion: source exhaustion, rights or physical backpressure, never an arbitrary hours ceiling
INTERNET_DATA_REVISION = 2
INTERNET_DATASETS = [  # public speech corpora in the commissioned languages; licence/access are checked on the host before any bytes move, refusals are recorded
    {'repo': 'thiomi/thiomi-5k', 'config': 'kik_Latn', 'language': 'kik'}, {'repo': 'thiomi/thiomi-5k', 'config': 'kam_Latn', 'language': 'kam'},
    {'repo': 'Professor/kikuyu-speech-data', 'config': None, 'language': 'kik', 'format': 'manifest_tar'},
    {'repo': 'Digital-Divide-Data/Kamba-ASR-Data-Subset-484H', 'config': None, 'language': 'kam', 'text_column': 'transcripts', 'speaker_column': 'speaker_name'},
    {'repo': 'google/fleurs', 'config': 'sw_ke', 'language': 'swa', 'text_column': 'raw_transcription'},
    {'repo': 'mozilla-foundation/common_voice_17_0', 'config': 'sw', 'language': 'swa', 'text_column': 'sentence'},
]


def brand_lexicon():
    """The active owner lexicon (version, compact brand/alias list, hash). Version 1 is the pre-catalogue seed list."""
    return brand_catalogue.active()


BRAND_LEXICON = brand_catalogue.LEGACY_V1  # version-1 seed list, kept for the record; dispatch uses brand_lexicon()

COMMISSIONS = {
    'LISTEN-KIK-KAM-SWA': {
        'title': 'Multilingual radio brand listener (Kikuyu, Kamba, Kiswahili)',
        'product': 'recognition plus brand/entity detection with evidence: brand, span, language, recording/time, confidence/abstention, context, permitted playback',
        'lanes': ['listener'],
        'target_outcome': {'task': 'spoken brand-mention monitoring on radio audio', 'domain': 'radio broadcast speech, three languages, code-switching',
                           'admission': {lang: {'mention_precision': 0.90, 'mention_recall': 0.90} for lang in LANGUAGES}, 'gate_policy': 'every language meets both bars on the sealed admission split; no averaging',
                           'reported_separately': ['WER', 'CER', 'false positives per hour', 'timestamp tolerance', 'abstention', 'latency (RTF)', 'per-brand counts'],
                           'metric_contract_status': 'DERIVED from the owner 90% admission target: operationalised as mention precision AND recall ≥ 0.90 per language; MOAC90/switch85 remain the LID criteria, not substituted',
                           'sealed_split': 'speaker-cluster-disjoint admission split sealed in the AIP database manifest before any training'},
    },
    'STORY-KIK-KAM-SWA': {
        'title': 'Expressive spoken storyteller with an invented voice (Kikuyu, Kamba, Kiswahili)',
        'product': 'one agent that invents coherent stories and speaks them with the language character of each language in a voice that is no corpus presenter',
        'lanes': ['story_text', 'story_voice'],
        'target_outcome': {'task': 'story generation and expressive multilingual speech rendering', 'domain': 'radio storytelling register, three languages',
                           'admission': {'story_text': {lang: {'language_fidelity_rate': 1.0, 'dev_perplexity_below_base': True} for lang in LANGUAGES},
                                         'story_voice': {lang: {'spectral_behaviour_similarity': 0.90, 'identity_gate_max_cosine_below': 0.40, 'native_listener_rating': 'human evaluation required — not automatable'} for lang in LANGUAGES}},
                           'gate_policy': 'every language meets every automatable bar; native-listener judgement is recorded as pending until humans rate unseen stories',
                           'metric_contract_status': 'DERIVED/PROPOSED mapping of the owner 90% target onto measured spectral-behaviour similarity; naturalness itself is a human judgement and is not claimed from similarity',
                           'identity_rule': 'AIP §§6-7: inherit group language character, invent organic identity; every corpus-derived speaker comparator must stay below the cosine threshold'},
    },
}


def db():
    database = lab.db()
    database.malpha_commissions.create_index('commission_id', unique=True)
    database.malpha_jobs.create_index('job_id', unique=True)
    database.malpha_jobs.create_index([('commission_id', 1), ('lane', 1), ('iteration', 1)])
    database.malpha_log.create_index([('at', -1)])
    return database


def now():
    return lab.now()


def _log(commission_id, kind, text, **extra):
    db().malpha_log.insert_one({'at': now(), 'commission_id': commission_id, 'kind': kind, 'text': text[:600], **extra})
    log.info('malpha %s %s: %s', commission_id, kind, text[:200])


def aip_db_dir():
    return f"{os.environ['LANGUAGE_COGNITION_REMOTE_ROOT']}/malpha/{AIP_DB_NAME}"


def _lawful():
    from services.census_autonomy.operational_runner import admission_path
    lawful, _ = admission_path()
    return str(lawful)


# ----------------------------------------------------------------------------- commissions
def ensure_commissions(actor_id='akki-autopilot'):
    created = []
    for cid, spec in COMMISSIONS.items():
        doc = {'commission_id': cid, 'tenant_id': TENANT, **spec, 'languages': list(LANGUAGES), 'budget': {'mode': BUDGET_MODE, 'numeric_cap': None, 'authority': OWNER_ORDER_REF, 'iteration_ceiling': None},
               'aip_db_dir': aip_db_dir(), 'status': 'commissioned', 'commissioned_at': now(), 'commissioned_by': actor_id, 'lane_state': {lane: {'status': 'waiting_for_database', 'iteration': 0} for lane in spec['lanes']},
               'evaluation_exposure': {}, 'admitted': {}, 'definition_sha256': hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()}
        res = db().malpha_commissions.update_one({'commission_id': cid}, {'$setOnInsert': doc}, upsert=True)
        if res.upserted_id is not None:
            created.append(cid)
            wpw.attach_to_run(cid)
            wpw.record_event(cid, 'commissioning_reflection', 'observed', f'malpha://commission/{cid}', {'title': spec['title'], 'target_outcome': spec['target_outcome'], 'budget_mode': BUDGET_MODE, 'languages': list(LANGUAGES), 'definition_sha256': doc['definition_sha256']})
            _log(cid, 'commissioned', f"{spec['title']} commissioned; budget {BUDGET_MODE}; WPW notebook attached before any calibration or training.")
    return created


def commissions():
    return list(db().malpha_commissions.find({}, {'_id': 0}))


def commission(cid):
    return db().malpha_commissions.find_one({'commission_id': cid}, {'_id': 0})


def jobs(**query):
    return list(db().malpha_jobs.find(query, {'_id': 0}, sort=[('submitted_at', 1)]))


# ----------------------------------------------------------------------------- GPU availability (fresh read, resident workload protected)
def gpu_snapshot():
    from services.census_autonomy.gpu_spend_capture import capture_gpu_spend
    cap = capture_gpu_spend()
    devices = {}
    if cap.get('status') != 'CAPTURED': return {'status': cap.get('status'), 'devices': devices}
    for host, raw in cap['per_host_raw'].items():
        for line in raw.strip().splitlines():
            parts = [p.strip() for p in line.split(',')]
            if len(parts) < 6: continue
            try: devices[(host, int(parts[2]))] = {'name': parts[1], 'utilization': parts[4], 'memory_used_mib': int(parts[5].split()[0])}
            except ValueError: continue
    return {'status': 'CAPTURED', 'devices': devices, 'at': cap['captured_at_utc']}


def _busy_devices():
    return {(j['host'], j['gpu_index']) for j in jobs(status={'$in': ['running', 'submitting']}) if j['phase'] not in CPU_PHASES}


def free_device(phase, snapshot):
    busy = _busy_devices()
    for host, index in HOST_ALLOCATION[phase]:
        if (host, index) in busy: continue
        dev = snapshot['devices'].get((host, index))
        if dev is None or dev['memory_used_mib'] > RESIDENT_PROTECTED_MIB: continue  # resident model or foreign process: never evicted
        return host, index
    return None


# ----------------------------------------------------------------------------- dispatch
def _submit(cid, lane, phase, params, host, gpu_index, iteration, actor='akki-autopilot'):
    from services.training_runner import m9_dispatch
    params = {**params, 'commission_id': cid, 'languages': list(LANGUAGES), 'gpu_index': gpu_index, 'budget_mode': BUDGET_MODE, 'owner_order_ref': OWNER_ORDER_REF, 'seed': SEED, 'iteration': iteration, 'aip_db_dir': aip_db_dir()}
    job = m9_dispatch.submit(phase, params, host, actor, _lawful())
    rec = {'job_id': job['job_id'], 'commission_id': cid, 'lane': lane, 'phase': phase, 'iteration': iteration, 'host': host, 'gpu_index': gpu_index, 'params': {k: v for k, v in params.items() if k != 'brand_lexicon'},
           'status': job['status'], 'reason': job.get('reason'), 'submitted_at': job['submitted_at'], 'started_at': job.get('started_at'), 'pid': (job.get('remote') or {}).get('pid'), 'code_sha256': job.get('code_sha256'), 'gpu_seconds': 0}
    if 'brand_lexicon' in params: rec['lexicon'] = {'version': params.get('brand_lexicon_version') or brand_lexicon()['version'], 'brands': len(params['brand_lexicon'])}
    db().malpha_jobs.insert_one(dict(rec))
    if job['status'] == 'running':
        wpw.record_event(cid, 'checkpoint', 'observed', f"m9_training://run_log/{job['job_id']}", {'transition': 'dispatched', 'lane': lane, 'phase': phase, 'iteration': iteration, 'host': host, 'gpu_index': gpu_index, 'pid': rec['pid'], 'recipe': params.get('recipe')})
        _log(cid, 'dispatched', f"{lane} iteration {iteration} running on {host} GPU {gpu_index} as {job['job_id']} (pid {rec['pid']}).", job_id=job['job_id'])
    else:
        _log(cid, 'dispatch_refused', f"{lane} iteration {iteration} not started on {host} GPU {gpu_index}: {job.get('reason')}", job_id=job['job_id'])
    return rec


def dispatch_aip_build(snapshot=None):
    """One database per host (each host has the staged corpus; the volumes are not shared). Same seed → identical seals, which is checked on completion."""
    snapshot = snapshot or gpu_snapshot()
    out = []
    for host, index in HOST_ALLOCATION['malpha_aip_build']:
        if any(j['status'] in ('running', 'submitting', 'completed') for j in jobs(phase='malpha_aip_build', host=host)): continue
        dev = snapshot['devices'].get((host, index))
        if dev is None or dev['memory_used_mib'] > RESIDENT_PROTECTED_MIB or (host, index) in _busy_devices(): continue
        params = {'lab_corpus_root': os.environ['LANGUAGE_COGNITION_REMOTE_ROOT'], 'max_files_per_language': 0, 'cpu_workers': 24, 'token_max_seconds': 12.0, 'codec_sample_per_language': 60, 'brand_lexicon': brand_lexicon()['lexicon']}
        out.append(_submit('LISTEN-KIK-KAM-SWA', 'aip_build', 'malpha_aip_build', params, host, index, 0))
    return out


def _host_done(phase, host, **match):
    return next((j for j in jobs(phase=phase, host=host, status='completed', **match)), None)


def _host_busy_or_exhausted(phase, host, **match):
    if any(j['status'] in ('running', 'submitting') for j in jobs(phase=phase, host=host, **match)): return True
    return sum(1 for j in jobs(phase=phase, host=host, **match) if j['status'] in ('failed', 'interrupted')) >= MAX_ATTEMPTS_PER_ITERATION


def relabel_ready(host):
    """True when the host database carries the active owner lexicon (version 1 needs no relabel: the database was built with it)."""
    active = brand_lexicon()
    return active['version'] == 1 or _host_done('malpha_aip_relabel', host, **{'lexicon.version': active['version']}) is not None


def internet_ready(host):
    return _host_done('malpha_internet_corpus', host) is not None


def aip_ready(host):
    built = _host_done('malpha_aip_build', host); requalified = _host_done('malpha_aip_requalify', host)
    return built if built and requalified and relabel_ready(host) else None


def dispatch_relabel(snapshot=None):
    """A new owner lexicon version re-labels each host database once (CPU, beside running training). Lanes wait for it so the next iteration is measured on the owner's brands."""
    active = brand_lexicon(); out = []
    if active['version'] == 1: return out
    for host, index in HOST_ALLOCATION['malpha_aip_relabel']:
        if not (_host_done('malpha_aip_build', host) and _host_done('malpha_aip_requalify', host)) or relabel_ready(host): continue
        if _host_busy_or_exhausted('malpha_aip_relabel', host, **{'lexicon.version': active['version']}): continue
        out.append(_submit('LISTEN-KIK-KAM-SWA', 'aip_relabel', 'malpha_aip_relabel', {'brand_lexicon': active['lexicon'], 'brand_lexicon_version': active['version']}, host, index, 0))
    return out


def dispatch_internet_corpus(snapshot=None):
    """Owner order: public internet speech corpora may be used. One CPU ingestion per host database; licence/access refusals are recorded by the worker."""
    out = []
    for host, index in HOST_ALLOCATION['malpha_internet_corpus']:
        if not (_host_done('malpha_aip_build', host) and _host_done('malpha_aip_requalify', host)): continue
        if _host_done('malpha_internet_corpus', host, **{'params.data_revision': INTERNET_DATA_REVISION}) or _host_busy_or_exhausted('malpha_internet_corpus', host, **{'params.data_revision': INTERNET_DATA_REVISION}): continue
        out.append(_submit('LISTEN-KIK-KAM-SWA', 'internet_corpus', 'malpha_internet_corpus', {'datasets': INTERNET_DATASETS, 'max_hours_per_dataset': INTERNET_MAX_HOURS_PER_DATASET, 'data_revision': INTERNET_DATA_REVISION, 'brand_lexicon': brand_lexicon()['lexicon']}, host, index, 0))
    return out


def dispatch_requalify(snapshot=None):
    """CPU-only dev-split correction on each host's database, once, after its build; lanes wait for it so every iteration is measured on a dev set that exists."""
    out = []
    for host, index in HOST_ALLOCATION['malpha_aip_requalify']:
        if not jobs(phase='malpha_aip_build', host=host, status='completed'): continue
        if any(j['status'] in ('running', 'submitting', 'completed') for j in jobs(phase='malpha_aip_requalify', host=host)): continue
        if sum(1 for j in jobs(phase='malpha_aip_requalify', host=host) if j['status'] in ('failed', 'interrupted')) >= MAX_ATTEMPTS_PER_ITERATION: continue
        out.append(_submit('LISTEN-KIK-KAM-SWA', 'aip_requalify', 'malpha_aip_requalify', {'min_dev_segments': MIN_DEV_SEGMENTS, 'min_dev_mention_segments': MIN_DEV_MENTION_SEGMENTS}, host, index, 0))
    return out


def supersede(job_id, reason, actor='E1 engineering agent'):
    """Stop a running lane job whose worker code is known faulty. The record stays; a superseded attempt is not a measured iteration and not a fault."""
    from services.training_runner import m9_dispatch
    rec = db().malpha_jobs.find_one({'job_id': job_id}, {'_id': 0})
    if not rec or rec['status'] != 'running': return rec
    job = m9_dispatch.cancel(job_id, f'superseded: {reason}'[:200])
    if job and job.get('status') == 'cancelled':
        db().malpha_jobs.update_one({'job_id': job_id}, {'$set': {'status': 'cancelled', 'reason': job.get('reason'), 'finished_at': job.get('finished_at'), 'updated_at': now()}})
        wpw.record_event(rec['commission_id'], 'human_contribution', 'observed', f"m9_training://run_log/{job_id}",
                         {'actor': {'role': 'engineering agent', 'identity': actor}, 'state_before': f"{rec['lane']} iteration {rec['iteration']} running under worker bundle {rec.get('code_sha256')}",
                          'change': f'stopped; corrected worker code is submitted on the next tick ({reason})', 'movement_after': 'pending — recorded at the next settlement of this lane'})
        _log(rec['commission_id'], 'superseded', f"{rec['lane']} iteration {rec['iteration']} ({job_id}) stopped: {reason}", job_id=job_id)
    return db().malpha_jobs.find_one({'job_id': job_id}, {'_id': 0})


# ----------------------------------------------------------------------------- recipes: the next qualified change, from measured results
def _listener_summary(res):
    dev = res.get('dev') or {}
    return {l: {'P': (dev.get('mentions') or {}).get(l, {}).get('precision'), 'R': (dev.get('mentions') or {}).get(l, {}).get('recall'), 'WER': (dev.get('words') or {}).get(l, {}).get('wer')} for l in LANGUAGES}


def worker_audit_ready(host):
    from services.training_runner import m9_dispatch
    _, digest = m9_dispatch.build_bundle()
    return bool(jobs(phase='malpha_worker_audit', host=host, code_sha256=digest, status='completed', **{'result.status': 'passed'}))


def dispatch_worker_audits():
    from services.training_runner import m9_dispatch
    _, digest = m9_dispatch.build_bundle(); out = []
    for host, index in HOST_ALLOCATION['malpha_aip_build']:
        attempts = jobs(phase='malpha_worker_audit', host=host, code_sha256=digest)
        if any(j['status'] in ('running', 'submitting', 'completed') for j in attempts) or len(attempts) >= MAX_ATTEMPTS_PER_ITERATION: continue
        out.append(_submit('STORY-KIK-KAM-SWA', 'worker_audit', 'malpha_worker_audit', {'worker_contract_version': 2}, host, index, 0))
    return out


def listener_recipe(iteration, history):
    """Planned ladder (small → small longer → large-v3-turbo), then measurement-driven continuation. Contextual brand biasing through Whisper's
    previous-text channel is standard from the first recipe after the owner's catalogue arrived; the artefact is chosen by worst-language mention F1."""
    base = [{'base': 'openai/whisper-small', 'lr': 1e-4, 'batch_size': 32, 'grad_accum': 1, 'max_steps': 6000, 'warmup_steps': 300, 'eval_every': 1500, 'checkpoint_every': 500, 'dev_per_language': 300},
            {'base': 'openai/whisper-small', 'lr': 6e-5, 'batch_size': 32, 'grad_accum': 2, 'max_steps': 14000, 'warmup_steps': 500, 'eval_every': 2000, 'checkpoint_every': 500, 'dev_per_language': 300},
            {'base': 'openai/whisper-large-v3-turbo', 'lr': 3e-5, 'batch_size': 16, 'grad_accum': 4, 'max_steps': 12000, 'warmup_steps': 500, 'eval_every': 2000, 'checkpoint_every': 500, 'dev_per_language': 300}]
    recipe = dict(base[min(iteration - 1, len(base) - 1)])
    recipe.update(contextual_bias=True, bias_prob=0.5, bias_distractors=6, bias_terms_per_language=40,
                  language_balance=True, mention_oversample=True, selection_policy='minimum_precision_and_recall')
    if not history: recipe['rationale'] = 'planned ladder step 1: whisper-small, contextual brand biasing trained from the start'; return recipe
    last = history[-1]; res = last.get('result') or {}; last_recipe = res.get('recipe') or {}; summary = _listener_summary(res)
    bias_note = 'contextual bias kept' if last_recipe.get('contextual_bias') else 'contextual brand biasing newly on (expectation list of the 40 most-heard brands per language through <|startofprev|>; trained with true brands among distractors on half the segments)'
    if iteration <= len(base):
        recipe['rationale'] = f"planned ladder step {iteration} ({recipe['base']}, {recipe['max_steps']} steps) after iteration {last['iteration']} read {summary}; {bias_note}"
        return recipe
    # beyond the planned ladder: keep the strongest base, continue from the last artefact, shorter schedule; halve the learning rate only once biasing is already learned
    recipe.update(max_steps=8000, lr=recipe['lr'] if not last_recipe.get('contextual_bias') else recipe['lr'] * 0.5 ** (iteration - len(base)))
    if (res.get('artefact') or {}).get('path') and last_recipe.get('base') == recipe['base']: recipe['init_from'] = str(res['artefact']['path']).rsplit('/', 1)[0]
    recipe['rationale'] = f"beyond the planned ladder: continue {recipe['base']} from iteration {last['iteration']}'s artefact ({'carried' if recipe.get('init_from') else 'base changed, fresh start'}) for 8000 steps at lr {recipe['lr']:.1e}; last reading {summary}; {bias_note}"
    return recipe


def _story_text_best(history):
    """Best measured evaluation across completed iterations: lowest geometric-mean dev perplexity. Returns None when no iteration measured one."""
    from services.training_lab.malpha_worker_policy import story_score
    best = None
    for j in history:
        for h in ((j.get('result') or {}).get('history') or []):
            per = h.get('per_language') or {}
            if any(l not in per for l in LANGUAGES): continue
            vals = [per[l].get('dev_perplexity') for l in LANGUAGES]
            rank = story_score(h)
            if rank is None: continue
            score = math.exp(sum(math.log(v) for v in vals) / len(vals))
            if best is None or rank > best['rank']: best = {'rank': rank, 'score': round(score, 3), 'step': h['step'], 'job_id': j['job_id'], 'iteration': j['iteration'], 'lr': (j['result'].get('recipe') or {}).get('lr')}
    return best


def story_text_recipe(iteration, history, base_path):
    """Measurement-driven: the next change answers the last dev curve. Early stopping on dev perplexity and the best-adapter artefact are standard from here."""
    recipe = {'base_path': base_path, 'lr': 2e-4, 'batch_size': 4, 'grad_accum': 4, 'max_steps': 1500, 'warmup_steps': 100, 'eval_every': 250, 'checkpoint_every': 250, 'max_seq_len': 1024, 'lora_r': 32, 'lora_alpha': 64,
              'lora_dropout': 0.05, 'weight_decay': 0.0, 'eval_samples_per_language': 16, 'patience_evaluations': 4,
              'language_balance': True, 'selection_policy': 'base_floor_then_worst_language_fidelity'}
    if not history: recipe['rationale'] = 'first measured pass from the registered base; dev perplexity and language fidelity (8 samples per language) every 250 steps, stop after 3 evaluations without improvement'; return recipe
    last = history[-1]; res = last.get('result') or {}; best = _story_text_best(history); in_run = _story_text_best([last])
    final = res.get('dev') or {}; final_vals = [v.get('dev_perplexity') for v in (final.get('per_language') or {}).values() if v.get('dev_perplexity')]
    final_score = math.exp(sum(math.log(v) for v in final_vals) / len(final_vals)) if final_vals else None
    turned = bool(in_run and final_score and final_score > in_run['score'] * 1.1)  # the curve turned inside the run: the reported adapter sits past the minimum
    stale = bool(best and best['iteration'] != last['iteration'])  # an earlier iteration measured lower than anything in the last one
    if turned or stale:
        lr = float(best['lr'] or res.get('recipe', {}).get('lr') or 1e-4) * 0.5
        recipe.update(lr=max(lr, 2e-5), max_steps=3000, lora_dropout=0.1, weight_decay=0.01)
        recipe['rationale'] = (f"dev perplexity {'rose within' if turned else 'did not improve on earlier iterations in'} iteration {last['iteration']} (best measured {best['score']} at step {best['step']} of iteration {best['iteration']}; "
                               f"iteration {last['iteration']} ended at {round(final_score, 3) if final_score else 'n/a'}): the over-fitted adapter is not carried forward — restart from the registered base at half that iteration's learning rate "
                               f"({recipe['lr']:.1e}), dropout 0.1, weight decay 0.01, early stopping (patience 3) with the best-adapter artefact")
    else:
        recipe.update(lr=float(res.get('recipe', {}).get('lr') or 1e-4), init_adapter=(res.get('artefact') or {}).get('path'))
        recipe['rationale'] = f"dev perplexity still improving at the end of iteration {last['iteration']} (best {in_run['score'] if in_run else 'n/a'} at step {in_run['step'] if in_run else 'n/a'}): continue from its best adapter under the same learning rate with early stopping"
    weak = [l for l, v in (final.get('per_language') or {}).items() if (v.get('language_fidelity_rate') or 0) < 1.0]
    if weak:  # a language whose samples drift into a sister language is under-represented in the mix: balance the sampling by language
        recipe['language_balance'] = True
        recipe['rationale'] += f"; language fidelity below 1.0 for {', '.join(weak)} ({', '.join(str(final['per_language'][l].get('language_fidelity_rate')) for l in weak)}) → each micro-batch now drawn from one language chosen uniformly, so the small language is not out-voted"
    return recipe


def voice_recipe(iteration, history):
    """Measurement-driven: identity-conditioned rendering with an invented identity (MA-15) and loudness matched to the language baseline are standard from here;
    later iterations continue the same architecture from its artefact and answer the last gate/similarity reading."""
    recipe = {'lr': 3e-4, 'batch_size': 48, 'max_steps': 40000, 'warmup_steps': 1000, 'eval_every': 2500, 'checkpoint_every': 500, 'd_model': 768, 'layers': 12, 'heads': 12, 'max_segment_seconds': 12.0,
              'spectral_feedback': True, 'eval_prompts_per_language': 12, 'identity_cosine_threshold': 0.40,
              'identity_conditioning': True, 'identity_candidates': 200, 'identity_noise': 0.5, 'identity_margin': 0.05, 'loudness_match': True,
              'language_balance': True, 'dense_identity': True, 'worker_design_version': 2}
    if not history: recipe['rationale'] = 'first pass: speaker-conditioned codec LM with an invented identity under the corpus-distance gate; output loudness set to the language baseline median'; return recipe
    last = history[-1]; res = last.get('result') or {}; last_recipe = res.get('recipe') or {}; per = (res.get('dev') or {}).get('per_language') or {}
    gate_fail = [l for l, v in per.items() if not (v.get('identity_gate') or {}).get('passes')]
    sims = {l: ((v.get('behaviour') or {}).get('overall_similarity')) for l, v in per.items()}
    if not last_recipe.get('identity_conditioning'):
        cosines = ', '.join(f"{l} {(v.get('identity_gate') or {}).get('max_cosine_to_any_corpus_speaker')}" for l, v in per.items())
        recipe['rationale'] = (f"iterations 1–{last['iteration']} rendered an unconditioned corpus-average voice: max cosine to corpus speakers {cosines} against the 0.40 gate, similarity {sims} — "
                               'more steps cannot pass an identity gate without an identity mechanism. '
                               'Change: speaker-conditioned training; an invented identity (mean of 8 corpus representations + isotropic noise, resampled under the gate with a 0.05 margin) is the only voice rendered; output loudness matched to the language baseline median')
        return recipe
    recipe.update(init_from=(res.get('artefact') or {}).get('path'), lr=float(last_recipe.get('lr', 3e-4)) * 0.7, identity_noise=float(last_recipe.get('identity_noise', 0.5)), identity_margin=float(last_recipe.get('identity_margin', 0.05)))
    if gate_fail: recipe.update(identity_noise=round(recipe['identity_noise'] + 0.25, 2), identity_margin=min(0.15, round(recipe['identity_margin'] + 0.05, 2)))
    gate_text = f"failed for {', '.join(gate_fail)} → identity resampled with more noise ({recipe['identity_noise']}) and a wider construction margin ({recipe['identity_margin']})" if gate_fail else 'passed for every language → identity kept'
    recipe['rationale'] = f"continue iteration {last['iteration']}'s compatible weights at 0.7× learning rate; similarity {sims}; identity gate {gate_text}. Design v2: language-balanced curriculum, dense identity conditioning hypothesis, padded-text masking, delayed-codebook flush and complete cross-language rendered checks; no claim of convergence."
    return recipe


def _qwen_base_path(host, base_id='qwen3-1.7b-base'):
    from services.training_runner.ssh_seam import execute_remote_command
    result = execute_remote_command(host, f"cat {os.environ['M9_REMOTE_ROOT']}/base_registration.json", purpose='malpha_base_registration', timeout=30)
    reg = json.loads(result.stdout_redacted) if result.rc == 0 and result.stdout_redacted.strip() else {}
    entry = reg.get(base_id) or {}
    return entry.get('local_path'), entry


def lane_phase(lane):
    return {'listener': 'malpha_listener_train', 'story_text': 'malpha_story_text_train', 'story_voice': 'malpha_voice_train'}[lane]


MAX_ATTEMPTS_PER_ITERATION = 3  # a worker fault is retried under the same recipe (every attempt on the record); a third fault holds the lane for the owner


def dispatch_lane(cid, lane, snapshot):
    phase = lane_phase(lane); slot = free_device(phase, snapshot)
    if not slot: return None
    host, index = slot
    if not aip_ready(host): return None
    if not worker_audit_ready(host): return None
    history = [j for j in jobs(commission_id=cid, lane=lane, status='completed')]
    iteration = len(history) + 1  # a measured result advances the ladder; a faulted attempt does not
    faults = [j for j in jobs(commission_id=cid, lane=lane, iteration=iteration) if j['status'] in ('failed', 'interrupted')]
    if len(faults) >= MAX_ATTEMPTS_PER_ITERATION:
        reason = f"{lane} iteration {iteration} faulted {len(faults)} times ({str(faults[-1].get('reason'))[:120]}); lane held for the owner, not looped"
        db().malpha_commissions.update_one({'commission_id': cid}, {'$set': {f'lane_state.{lane}': {'status': 'held', 'iteration': iteration, 'reason': reason}}})
        wpw.record_event(cid, 'anomaly', 'observed', f"malpha://lane_state/{cid}/{lane}", {'lane': lane, 'iteration': iteration, 'held': True, 'faults': [f['job_id'] for f in faults]})
        _log(cid, 'lane_held', reason); return None
    if lane == 'listener':
        active = brand_lexicon(); recipe = listener_recipe(iteration, history)
        if internet_ready(host): recipe['include_internet_corpus'] = True  # qualified change: public corpora join the train split once ingested (never dev/admission)
        params = {'recipe': recipe, 'brand_lexicon': active['lexicon'], 'brand_lexicon_version': active['version']}
    elif lane == 'story_text':
        base_path, entry = _qwen_base_path(host)
        if not base_path: _log(cid, 'blocked', 'story_text: no registered Qwen3 base on the host; lane held'); return None
        params = {'recipe': story_text_recipe(iteration, history, base_path), 'base_registration': {k: entry.get(k) for k in ('repo', 'revision', 'licence_verified', 'weight_sha256')}}
    else: params = {'recipe': voice_recipe(iteration, history)}
    from services.training_runner import m9_dispatch
    _, code_sha = m9_dispatch.build_bundle()
    latest = next((j for j in reversed(faults) if j.get('last_checkpoint') and j.get('code_sha256') == code_sha), None)  # resume only under unchanged worker code
    if latest: params['resume_from'] = latest['last_checkpoint']
    rec = _submit(cid, lane, phase, params, host, index, iteration)
    if rec['status'] == 'running':
        if params['recipe'].get('rationale'): _log(cid, 'recipe', f"{lane} iteration {iteration} — why this recipe: {params['recipe']['rationale']}", job_id=rec['job_id'])
        # WPW-6: the recipe choice is an ideation record mirrored by reference — the idea lives in the job params, its conditions in the measured result it answered
        conditions = f"malpha://job/{history[-1]['job_id']}#result.dev" if history else f"malpha://commission/{cid}#target_outcome"
        wpw.record_event(cid, 'cif_ideation', 'observed', f"m9_training://run_log/{rec['job_id']}", {'cif_event_ref': f"malpha://job/{rec['job_id']}#params.recipe", 'idea_ref': f"malpha.{lane}_recipe#iteration{iteration}", 'conditions_ref': conditions,
                                                                                                    'adoption_status': 'adopted', 'attempt': len(faults) + 1, 'resumed_from_checkpoint': bool(latest)})
    db().malpha_commissions.update_one({'commission_id': cid}, {'$set': {f'lane_state.{lane}': {'status': 'running' if rec['status'] == 'running' else 'dispatch_refused', 'iteration': iteration, 'attempt': len(faults) + 1, 'job_id': rec['job_id']}, 'status': 'running'}})
    return rec


def dispatch_evaluation(cid, lane, trained, snapshot):
    slot = next(((h, i) for h, i in HOST_ALLOCATION['malpha_evaluate'] if h == trained['host'] and (h, i) not in _busy_devices() and (snapshot['devices'].get((h, i)) or {}).get('memory_used_mib', 1e9) <= RESIDENT_PROTECTED_MIB), None)
    if not slot: return None
    art = trained['result']['artefact']; active = brand_lexicon()
    params = {'artefact_path': art['path'], 'artefact_sha256': art['sha256'], 'brand_lexicon': active['lexicon'], 'brand_lexicon_version': active['version'], 'admission_target': 0.9, 'trained_job_id': trained['job_id']}
    rec = _submit(cid, f'{lane}_evaluate', 'malpha_evaluate', params, slot[0], slot[1], trained['iteration'])
    db().malpha_commissions.update_one({'commission_id': cid}, {'$inc': {f"evaluation_exposure.{art['sha256'][:12]}": 1}})
    return rec


# ----------------------------------------------------------------------------- settlement
def _dev_meets_target(lane, result):
    dev = result.get('dev') or {}
    if lane == 'listener':
        return all(((dev.get('mentions') or {}).get(l) or {}).get('precision') is not None and dev['mentions'][l]['precision'] >= 0.9 and dev['mentions'][l]['recall'] >= 0.9 for l in LANGUAGES)
    if lane == 'story_text':
        return all(((dev.get('per_language') or {}).get(l) or {}).get('language_fidelity_rate') == 1.0 and ((dev.get('per_language') or {}).get(l) or {}).get('dev_perplexity_below_base') is True for l in LANGUAGES)
    if lane == 'story_voice':
        return all((((dev.get('per_language') or {}).get(l) or {}).get('behaviour') or {}).get('overall_similarity', 0) >= 0.9 and (dev['per_language'][l].get('identity_gate') or {}).get('passes') for l in LANGUAGES)
    return False


def _summary(lane, result):
    dev = result.get('dev') or {}
    if lane == 'listener': return {l: {'wer': (dev.get('words') or {}).get(l, {}).get('wer'), 'mention_precision': (dev.get('mentions') or {}).get(l, {}).get('precision'), 'mention_recall': (dev.get('mentions') or {}).get(l, {}).get('recall')} for l in LANGUAGES}
    if lane == 'story_text': return {l: {k: (dev.get('per_language') or {}).get(l, {}).get(k) for k in ('dev_perplexity', 'base_perplexity', 'language_fidelity_rate')} for l in LANGUAGES}
    if lane == 'story_voice': return {l: {'similarity': ((dev.get('per_language') or {}).get(l, {}).get('behaviour') or {}).get('overall_similarity'), 'identity_gate': ((dev.get('per_language') or {}).get(l, {}).get('identity_gate') or {}).get('passes')} for l in LANGUAGES}
    return {}


def refresh_jobs():
    from services.training_runner import m9_dispatch
    settled = []
    for rec in jobs(status={'$in': ['running', 'submitting']}):
        job = m9_dispatch.refresh(rec['job_id'])
        if not job: continue
        progress = ((job.get('remote_state') or {}).get('progress') or {})
        fields = {'status': job['status'], 'progress': progress, 'process_alive': job.get('process_alive'), 'last_status_rpc': job.get('last_status_rpc'), 'updated_at': now(), 'gpu_seconds': 0 if rec['phase'] in CPU_PHASES else int(progress.get('elapsed_s') or rec.get('gpu_seconds') or 0),
                  'stages': {k: v for k, v in ((job.get('remote_state') or {}).get('stages') or {}).items()}, 'worker_log_tail': (job.get('worker_log_tail') or '')[-600:]}
        if progress.get('last_checkpoint_step'): fields['last_checkpoint'] = f"{job['remote']['job_dir']}/checkpoints/latest.pt"
        if job['status'] == 'completed' and (job.get('receipt') or {}).get('digest_verified'):
            result = job['receipt']['result']; fields.update(result=result, finished_at=job.get('finished_at'), receipt_sha256=job['receipt']['receipt_sha256'], gpu_seconds=int((result.get('compute') or {}).get('gpu_seconds') or fields['gpu_seconds']))
        elif job['status'] not in ('running', 'submitting'):
            fields.update(reason=job.get('reason') or ((job.get('receipt') or {}).get('error') or {}).get('message'), finished_at=job.get('finished_at'))
        db().malpha_jobs.update_one({'job_id': rec['job_id']}, {'$set': fields})
        if job['status'] not in ('running', 'submitting'): settled.append({**rec, **fields})
    return settled


def _tier2(rec):
    """WPW-8: a technical report drafts automatically when a run settles, accepted or refused. Zero-influence: a report failure never touches the lane."""
    try:
        from services.wpw import tier2_malpha
        out = tier2_malpha.settle_report(rec['job_id'])
        _log(rec['commission_id'], 'tier2_report', f"{rec['lane']} iteration {rec['iteration']}: Tier 2 technical report drafted ({out['metadata']['settlement']}; {len(out['figures'])} figures resolve, {len(out['refused_figures'])} refused); Documents commission {out.get('documents', {}).get('commission_id') or 'not created'}.", job_id=rec['job_id'])
    except Exception as exc:  # WPW-2: the wizard must be unobservable to the run
        log.exception('tier2 settlement failed for %s', rec.get('job_id'))
        _log(rec['commission_id'], 'tier2_report_failed', f"{rec['lane']} iteration {rec['iteration']}: Tier 2 report could not be drafted: {exc!r}"[:600], job_id=rec['job_id'])


def settle(rec, snapshot):
    cid, lane, phase = rec['commission_id'], rec['lane'], rec['phase']
    ref = f"m9_training://run_log/{rec['job_id']}"
    priced = price_gpu([rec])
    wpw.record_event(cid, 'cost_checkpoint', 'measured', ref, {'lane': lane, 'iteration': rec['iteration'], 'gpu_seconds': rec.get('gpu_seconds'), 'host': rec['host'], 'gpu_index': rec['gpu_index'], 'status': rec['status'],
                                                              'rate_usd_per_gpu_hour': (priced['rate_usd_per_gpu_hour'] or {}).get(rec['host']), 'cost_usd': priced['cost_usd'], 'note': priced['cost_note']})
    if rec['status'] != 'completed':
        wpw.record_event(cid, 'anomaly', 'observed', ref, {'lane': lane, 'iteration': rec['iteration'], 'status': rec['status'], 'reason': rec.get('reason'), 'last_checkpoint': rec.get('last_checkpoint')})
        _log(cid, 'job_failed', f"{lane} iteration {rec['iteration']} ({rec['job_id']}) ended {rec['status']}: {str(rec.get('reason'))[:200]}. Retained checkpoint: {rec.get('last_checkpoint') or 'none'}.", job_id=rec['job_id'])
        if phase not in ('malpha_aip_build', 'malpha_aip_requalify', 'malpha_aip_relabel', 'malpha_internet_corpus'): _tier2(rec)
        return
    result = rec['result']
    if phase == 'malpha_worker_audit':
        _log(cid, 'worker_audit', f"Worker contracts verified on {rec['host']}: {len(result['checks'])} synthetic-tensor checks; NOT quality evidence.", job_id=rec['job_id'])
        return
    if lane == 'story_text_comparison':
        _log(cid, 'comparison', 'Larger-base capacity trial completed; research only, not product admission or a matched causal benchmark.', job_id=rec['job_id'])
        _tier2(rec)
        return
    if phase == 'malpha_aip_build':
        wpw.record_event(cid, 'baseline_selection', 'measured', ref, {'what': 'audio database built; codec qualified; splits sealed', 'seals': result['seals'], 'codec': result['codec_provenance'], 'segments': result['segments'], 'host': rec['host']})
        others = [j for j in jobs(phase='malpha_aip_build', status='completed') if j['job_id'] != rec['job_id']]
        agree = all(j['result']['seals'] == result['seals'] for j in others)
        _log(cid, 'database_built', f"AIP database on {rec['host']}: {sum(v['train']['segments'] + v['dev']['segments'] + v['admission']['segments'] for v in result['segments'].values())} segments; seals {'match the other host' if others and agree else 'recorded'}.", job_id=rec['job_id'])
        if others and not agree: wpw.record_event(cid, 'anomaly', 'observed', ref, {'what': 'admission seals differ between hosts', 'hosts': [rec['host']] + [j['host'] for j in others]})
        db().malpha_commissions.update_many({}, {'$set': {'aip_manifest_sha256': result['manifest_sha256'], 'aip_seals': result['seals']}})
        return
    if phase == 'malpha_aip_requalify':
        rq = result['requalification']['report']
        wpw.record_event(cid, 'anomaly', 'observed', ref, {'what': 'absent dev strata under the cluster-disjoint rule (MA-12)', 'dev_before': {l: v['before'] for l, v in rq.items()}, 'host': rec['host']})
        wpw.record_event(cid, 'baseline_selection', 'measured', ref, {'what': 'dev split requalified; admission seals unchanged', 'dev_after': {l: v['after'] for l, v in rq.items()}, 'promoted_sessions': {l: v['promoted_sessions'] for l, v in rq.items()},
                                                                      'dev_by_basis': {l: result['segments'][l].get('dev_by_basis') for l in result['segments']}, 'seals': result['seals'], 'host': rec['host']})
        _log(cid, 'dev_requalified', f"AIP dev split on {rec['host']} requalified: " + '; '.join(f"{l}: {v['before']['segments']}→{v['after']['segments']} segments ({v['after']['mention_segments']} with mentions, {v['promoted_sessions']} sessions promoted)" for l, v in rq.items()) + '. Admission seals unchanged.', job_id=rec['job_id'])
        db().malpha_commissions.update_many({}, {'$set': {'aip_manifest_sha256': result['manifest_sha256'], 'aip_seals': result['seals'], 'aip_dev_requalified': True}})
        return
    if phase == 'malpha_aip_relabel':
        rq = result['report']
        wpw.record_event(cid, 'human_contribution', 'observed', ref, {'actor': {'role': 'owner', 'identity': 'commissioning owner'}, 'state_before': 'brand mentions labelled from the version-1 seed lexicon',
                                                                   'change': f"owner brand catalogue registered as lexicon version {result.get('lexicon_version')} ({result['brands']} matchable brands); database re-labelled on {rec['host']}; admission seals unchanged",
                                                                   'movement_after': {l: {'mention_segments_before': v['mention_segments_before'], 'mention_segments_after': v['mention_segments_after'], 'by_split': v['by_split']} for l, v in rq.items()}})
        flagged = {l: v[:8] for l, v in (result.get('frequent_brands_flagged') or {}).items() if v}
        if flagged: wpw.record_event(cid, 'anomaly', 'observed', ref, {'what': 'brand names that are frequent words in the corpus (>1% of segments) — product-level disambiguation needed; not dropped', 'flagged': flagged})
        _log(cid, 'database_relabelled', f"AIP database on {rec['host']} re-labelled under lexicon v{result.get('lexicon_version')} ({result['brands']} brands): " + '; '.join(f"{l}: {v['mention_segments_before']}→{v['mention_segments_after']} mention segments (dev {v['by_split']['dev']}, admission {v['by_split']['admission']})" for l, v in rq.items()) + '. Admission seals unchanged.', job_id=rec['job_id'])
        db().malpha_commissions.update_many({}, {'$set': {'aip_manifest_sha256': result['manifest_sha256'], 'brand_lexicon': {'version': result.get('lexicon_version'), 'sha256': result['lexicon_sha256'], 'brands': result['brands'], 'frequent_brands_flagged': result.get('frequent_brands_flagged')}}})
        return
    if phase == 'malpha_internet_corpus':
        ingested = [d for d in result['datasets'] if d['status'] == 'ingested']; refused = [d for d in result['datasets'] if d['status'] == 'refused']
        partial = [d for d in result['datasets'] if d['status'] == 'partial']
        if partial:
            wpw.record_event(cid, 'anomaly', 'observed', ref, {'what': 'Public intake is incomplete and resumable; do not count as exhausted source',
                'partial': [{k: d.get(k) for k in ('repo', 'language', 'rows', 'hours', 'revision', 'stop_reason')} for d in partial]})
        wpw.record_event(cid, 'baseline_selection', 'measured', ref, {'what': 'public internet speech corpora ingested as a separate train-only dataset of the audio database (owner order)', 'authority': INTERNET_DATA_ORDER_REF, 'host': rec['host'],
                                                                     'ingested': [{k: d.get(k) for k in ('repo', 'config', 'language', 'licence', 'rows', 'hours')} for d in ingested], 'refused': [{k: d.get(k) for k in ('repo', 'config', 'language', 'reason')} for d in refused], 'totals': result['totals']})
        if refused: wpw.record_event(cid, 'anomaly', 'observed', ref, {'what': 'public datasets refused by the rights/access check (licence not admitted, gated without token, or not loadable)', 'refused': [{k: d.get(k) for k in ('repo', 'config', 'reason')} for d in refused]})
        _log(cid, 'internet_corpus', f"Internet corpus on {rec['host']}: " + '; '.join(f"{l}: {v['rows']} rows / {v['hours']} h" for l, v in result['totals'].items()) + f". Ingested {len(ingested)}, refused {len(refused)}" + (': ' + '; '.join(f"{d['repo']} ({d['reason'][:60]})" for d in refused) if refused else '') + '.', job_id=rec['job_id'])
        db().malpha_commissions.update_many({}, {'$set': {f"internet_corpus.{rec['host'].replace('.', '_')}": {'totals': result['totals'], 'ingested': len(ingested), 'refused': [{k: d.get(k) for k in ('repo', 'config', 'reason')} for d in refused], 'at': now()}}})
        return
    if phase == 'malpha_evaluate':
        verdict = result['verdict']; admitted = result.get('admitted_all_languages')
        wpw.record_event(cid, 'acceptance_criterion_transition', 'measured', ref, {'lane': lane, 'iteration': rec['iteration'], 'verdict': verdict, 'admitted_all_languages': admitted, 'sealed_admission_read': True})
        _log(cid, 'admission_evaluated', f"{lane}: sealed-split verdict {'ADMITTED' if admitted else 'REFUSED'} — " + '; '.join(f"{l}: P {v['mention_precision']} R {v['mention_recall']} WER {v['wer']}" for l, v in verdict.items()), job_id=rec['job_id'])
        if admitted:
            db().malpha_commissions.update_one({'commission_id': cid}, {'$set': {f"admitted.{lane.replace('_evaluate', '')}": {'job_id': rec['params']['trained_job_id'], 'artefact_sha256': rec['params']['artefact_sha256'], 'verdict': verdict, 'at': now()},
                                                                                 f"lane_state.{lane.replace('_evaluate', '')}.status": 'admitted'}})
        _tier2(rec)
        return
    summary = _summary(lane, result); meets = _dev_meets_target(lane, result)
    wpw.record_event(cid, 'acceptance_criterion_transition', 'measured', ref, {'lane': lane, 'iteration': rec['iteration'], 'dev_summary': summary, 'dev_meets_target': meets, 'steps': result.get('steps'), 'sealed_admission_read': result.get('sealed_admission_read', False)})
    _log(cid, 'iteration_settled', f"{lane} iteration {rec['iteration']} settled after {result.get('steps')} steps, {round((rec.get('gpu_seconds') or 0) / 3600, 2)} GPU-h: {json.dumps(summary)}. Dev target {'met → independent sealed evaluation next' if meets else 'not met → next qualified change'}.", job_id=rec['job_id'])
    db().malpha_commissions.update_one({'commission_id': cid}, {'$set': {f'lane_state.{lane}': {'status': 'dev_target_met' if meets else 'iterating', 'iteration': rec['iteration'], 'job_id': rec['job_id'], 'summary': summary}}})
    _tier2(rec)
    if meets and lane == 'listener': dispatch_evaluation(cid, lane, rec, snapshot)


def tick():
    """One native dispatcher across manual, cron and concurrent web requests."""
    from datetime import datetime, timedelta, timezone
    from pymongo.errors import DuplicateKeyError
    import uuid
    owner = uuid.uuid4().hex; clock = datetime.now(timezone.utc); collection = db().malpha_dispatch_leases
    try:
        lock = collection.find_one_and_update({'_id': 'native-tick', '$or': [{'expires_at': {'$lte': clock}}, {'owner': owner}]},
            {'$set': {'owner': owner, 'expires_at': clock + timedelta(minutes=30)}}, upsert=True, return_document=True, projection={'_id': 0})
    except DuplicateKeyError:
        return {'status': 'already_running', 'dispatched': [], 'settled': []}
    if not lock or lock.get('owner') != owner: return {'status': 'already_running', 'dispatched': [], 'settled': []}
    try: return _tick_unlocked()
    finally: collection.delete_one({'_id': 'native-tick', 'owner': owner})


def _tick_unlocked():
    """One autonomous pass: refresh, settle, then fill every free admitted device with the next job its lane needs. Called by the autopilot."""
    if not commissions(): return {'skipped': 'no commissions'}
    snapshot = gpu_snapshot()
    from services.training_lab.malpha_comparisons import restore_serving_after_trial
    restore_serving_after_trial(snapshot)
    if snapshot.get('status') != 'CAPTURED':
        _log('*', 'hosts_unreachable', f"GPU snapshot {snapshot.get('status')}; nothing dispatched this tick"); return snapshot
    settled = refresh_jobs()
    for rec in settled: settle(rec, snapshot)
    dispatched = list(dispatch_worker_audits()) + list(dispatch_aip_build(snapshot)) + list(dispatch_requalify(snapshot)) + list(dispatch_relabel(snapshot)) + list(dispatch_internet_corpus(snapshot))
    for c in commissions():
        for lane in c['lanes']:
            state = (c.get('lane_state') or {}).get(lane) or {}
            if state.get('status') in ('admitted', 'held'): continue
            if any(j['status'] in ('running', 'submitting') for j in jobs(commission_id=c['commission_id'], lane=lane)): continue
            if state.get('status') == 'dev_target_met' and lane != 'listener': continue  # storyteller lanes wait for the human-rating gate; recorded, not looped
            if any(j['status'] in ('running', 'submitting') for j in jobs(commission_id=c['commission_id'], lane=f'{lane}_evaluate')): continue
            rec = dispatch_lane(c['commission_id'], lane, snapshot)
            if rec: dispatched.append(rec)
    return {'settled': [r['job_id'] for r in settled], 'dispatched': [r['job_id'] for r in dispatched], 'snapshot_at': snapshot.get('at')}


# ----------------------------------------------------------------------------- views
def price_gpu(rows):
    """Measured GPU-hours × the owner-supplied per-host rate (cost_ledger rates register). Hours without a rate stay unpriced and say so."""
    from services.cost_ledger import rates
    priced_h = unpriced_h = cost = 0.0; used = {}
    for j in rows:
        h = (j.get('gpu_seconds') or 0) / 3600
        rate = rates.rate_for_gpu_hour(j.get('host')) or {}
        if rate.get('rate_per_hour'):
            cost += h * float(rate['rate_per_hour']); priced_h += h; used[j['host']] = {'rate_per_hour': float(rate['rate_per_hour']), 'currency': rate.get('currency', 'USD'), 'source': rate.get('source')}
        else: unpriced_h += h
    return {'cost_usd': round(cost, 2) if priced_h else None, 'priced_gpu_hours': round(priced_h, 3), 'unpriced_gpu_hours': round(unpriced_h, 3), 'rate_usd_per_gpu_hour': used or None,
            'cost_note': ('owner-supplied GPU-hour rate applied to measured hours' + (f'; {round(unpriced_h, 2)} GPU-h on hosts without a rate stay unpriced' if unpriced_h else '')) if priced_h else 'no governed GPU rate card yet; hours are measured, money is not invented'}


def metering():
    rows = jobs()
    by_lane = {}
    for j in rows:
        by_lane.setdefault(j['lane'], {'jobs': 0, 'gpu_hours': 0.0, 'rows': []})
        by_lane[j['lane']]['jobs'] += 1; by_lane[j['lane']]['gpu_hours'] += (j.get('gpu_seconds') or 0) / 3600; by_lane[j['lane']]['rows'].append(j)
    return {'budget_mode': BUDGET_MODE, 'numeric_cap': None, 'authority': OWNER_ORDER_REF, 'gpu_hours_total': round(sum(v['gpu_hours'] for v in by_lane.values()), 3),
            'by_lane': {k: {'jobs': v['jobs'], 'gpu_hours': round(v['gpu_hours'], 3), 'cost_usd': price_gpu(v['rows'])['cost_usd']} for k, v in by_lane.items()}, **price_gpu(rows)}


def status():
    active = brand_lexicon()
    return {'commissions': commissions(), 'jobs': [{k: v for k, v in j.items() if k not in ('result',)} | {'result_summary': _summary(j['lane'], j['result']) if j.get('result') and j['lane'] in ('listener', 'story_text', 'story_voice') else None} for j in jobs()],
            'metering': metering(), 'brand_lexicon': {'version': active['version'], 'brands': len(active['lexicon']), 'lexicon_sha256': active['lexicon_sha256'], 'source': active['source'], 'relabel_ready': {h: relabel_ready(h) for h, _ in HOST_ALLOCATION['malpha_aip_relabel']}},
            'internet_corpus': {'datasets': INTERNET_DATASETS, 'max_hours_per_dataset': INTERNET_MAX_HOURS_PER_DATASET, 'authority': INTERNET_DATA_ORDER_REF, 'ready': {h: internet_ready(h) for h, _ in HOST_ALLOCATION['malpha_internet_corpus']}},
            'log': list(db().malpha_log.find({}, {'_id': 0}, sort=[('at', -1)], limit=60)), 'wpw': {cid: {'attached': wpw.is_attached_to_run(cid), 'entries': len(wpw.list_entries(cid)), 'chain': wpw.verify_hash_chain(cid)} for cid in COMMISSIONS}}


def job_detail(job_id):
    if not re.fullmatch(r'm9j-[a-f0-9]{12}', job_id or ''): return None
    return db().malpha_jobs.find_one({'job_id': job_id}, {'_id': 0})
