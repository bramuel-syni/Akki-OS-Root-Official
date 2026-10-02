"""Autonomous executor behind the sign-off register. Every tick: refresh every running GPU job so the record is live, advance the music
chain (baseline once the corpus is measured), dispatch signed plans, evaluate finished runs against the signed acceptance, and commission
the written report. Deterministic throughout; the only authoring happens in the document studio's frontier writer."""
import asyncio
import logging
import os

from services.training_lab import conversation, signoff, store as lab

log = logging.getLogger(__name__)
TENANT = 'RMS'
REFRESH_AGE_S = 120


def _age(stamp):
    from datetime import datetime, timezone
    if not stamp: return 1e9
    try: return (datetime.now(timezone.utc) - datetime.fromisoformat(stamp.replace('Z', '+00:00'))).total_seconds()
    except ValueError: return 1e9


def refresh_running(max_age_s=0):
    """Bring every running job's control-plane record up to date; stale progress is never shown as live."""
    from services.audio_plane_v1 import language_cognition_dispatch as lc
    from services.training_lab import corpus_measurement
    from services.training_runner import m9_dispatch
    touched = []
    for module in (m9_dispatch, lc):
        for job in module.list_jobs():
            if job.get('status') not in ('running', 'submitting'): continue
            if _age((job.get('last_status_rpc') or {}).get('at')) < max_age_s: continue
            try: module.refresh(job['job_id']); touched.append(job['job_id'])
            except Exception as exc: log.warning('refresh %s failed: %s', job['job_id'], type(exc).__name__)
    doc = corpus_measurement.latest(TENANT)
    if doc and doc['status'] == 'running' and _age(doc.get('updated_at')) >= max_age_s:
        try: corpus_measurement.refresh(doc); touched.append(doc['measurement_id'])
        except Exception as exc: log.warning('measurement refresh failed: %s', type(exc).__name__)
    return touched


def advance_music(tenant=TENANT):
    """Measured corpus and no baseline yet → establish the baseline (readings and a shallow fit; no GPU, no sign-off needed).
    A baseline still waiting on library measurements keeps its worker alive across restarts."""
    from services.media_library import acoustics
    from services.training_lab import baseline, corpus_measurement
    if lab.db().training_lab_runs.count_documents({'tenant_id': tenant, 'kind': 'music_baseline', 'status': 'waiting_measurements'}):
        acoustics.start_worker(); baseline.advance(tenant)
    measurement = corpus_measurement.latest(tenant)
    if not measurement or measurement['status'] != 'completed': return None
    if lab.db().training_lab_runs.count_documents({'tenant_id': tenant, 'kind': 'music_baseline', 'status': {'$in': ('complete', 'waiting_measurements', 'queued')}}): return None
    row, created = baseline.submit(signoff.SYSTEM_ACTOR, f"autopilot:music-baseline:{measurement['measurement_id']}", {'unlabelled_library_audio': 'music', 'include_synthetic': True, 'include_corpus_test': True})
    if created:
        ref = row.get('reference_set') or {}
        text = (f"Corpus measured, so I established the baseline on {ref.get('measured', 0)} labelled recordings without waiting to be asked." +
                (f" {len(ref.get('pending') or [])} recordings are still being measured; it completes on its own." if ref.get('pending') else ' The checks a trained detector must beat are now on the record.'))
        conversation.record(tenant, 'music-identification', conversation.note(tenant, text, widget='action', action='run_music_baseline', origin='autopilot'))
    return row


def _lawful():
    from services.census_autonomy.operational_runner import admission_path
    lawful, _ = admission_path()
    return str(lawful)


def dispatch_signed(tenant=TENANT):
    for record in signoff.with_status(tenant, 'signed', 'shipping'):
        plan, run_id = record['plan'], record['run_id']
        try:
            if plan['kind'] == 'audio_language_corrective':
                from services.audio_plane_v1 import language_cognition_dispatch as lc
                params = {**plan['recipe'], 'gpu_index': plan['gpu_index'], 'host': plan['host'],
                          'owner_order_ref': f"owner sign-off {record['plan_sha256'][:12]} by {record['signed_by']} at {record['signed_at'][:19]}Z: {', '.join(plan['target_languages'])} reinforcement, non-DP corrective arm, cap {plan['compute_cap_gpu_hours']} GPU-h"}
                job = lc.submit('train_corrective', params, record['signed_by'], _lawful())
            else:
                from services.training_lab import music_shipping
                from services.training_runner import m9_dispatch
                items, _ = music_shipping.labelled_items(tenant)
                by_id = {it['item_id']: it for it in items}
                manifest = [{**by_id[p['item_id']], 'label': p['label'], 'label_source': p['label_source']} for p in plan['labelled_items'] if p['item_id'] in by_id and by_id[p['item_id']]['sha256'] == p['sha256']]
                if len(manifest) != len(plan['labelled_items']):
                    raise ValueError('a signed recording is no longer available with the same digest; the plan must be re-read and re-signed')
                signoff.update(tenant, run_id, status='shipping')
                shipped = music_shipping.ship(plan['host'], manifest, progress=lambda done, of: signoff.update(tenant, run_id, shipping={'done': done, 'of': of}))
                signoff.update(tenant, run_id, shipping={**shipped, 'done': shipped['shipped'], 'of': shipped['shipped']})
                measurement_dir = f"{os.environ['M9_REMOTE_ROOT']}/jobs/{plan['measurement_job_id']}" if plan.get('measurement_job_id') else ''
                params = {**plan['recipe'], 'gpu_index': plan['gpu_index'], 'lab_corpus_root': os.environ['LANGUAGE_COGNITION_REMOTE_ROOT'], 'refs_dir': music_shipping.refs_dir(),
                          'measurement_job_dir': measurement_dir, 'labelled_manifest': [{k: m[k] for k in ('item_id', 'title', 'label', 'label_source', 'file', 'sha256')} for m in manifest],
                          'baseline': plan['acceptance']['baseline'], 'smoke': False,
                          'owner_order_ref': f"owner sign-off {record['plan_sha256'][:12]} by {record['signed_by']} at {record['signed_at'][:19]}Z: music detector, cap {plan['compute_cap_gpu_hours']} GPU-h"}
                job = m9_dispatch.submit('lab_train_music', params, plan['host'], record['signed_by'], _lawful())
            if job['status'] != 'running':
                signoff.update(tenant, run_id, status='failed', dispatch={'job_id': job['job_id'], 'at': lab.now(), 'host': plan['host'], 'gpu_index': plan['gpu_index'], 'status': job['status'], 'reason': job.get('reason')})
                conversation.record(tenant, run_id, conversation.note(tenant, f"The GPU host did not accept the signed run ({job.get('reason') or job['status']}). Nothing is training; the signature stays on record.", origin='autopilot'))
                continue
            signoff.update(tenant, run_id, status='dispatched', dispatch={'job_id': job['job_id'], 'at': lab.now(), 'host': plan['host'], 'gpu_index': plan['gpu_index'], 'status': 'running'})
            conversation.record(tenant, run_id, conversation.note(tenant, f"Signed off, so training started on {plan['host']} GPU {plan['gpu_index']} as run {job['job_id']} — exactly the recipe, data and cap you approved (digest {record['plan_sha256'][:12]}). I will report here as it progresses and when the checks are in.",
                                                                 widget='status', status_label='Training', status_line=f"{job['job_id']} · {plan['host']} GPU {plan['gpu_index']} · started", origin='autopilot'))
        except Exception as exc:
            log.exception('dispatch for %s failed', run_id)
            signoff.update(tenant, run_id, status='failed', dispatch={'at': lab.now(), 'status': 'not_started', 'reason': f"{type(exc).__name__}: {str(exc)[:200]}"})
            conversation.record(tenant, run_id, conversation.note(tenant, f"I could not start the signed run: {str(exc)[:200]}. Nothing is training; the signature stays on record.", origin='autopilot'))


# ----------------------------------------------------------------------------- acceptance against the signed contract
def _audio_outcome(plan, job):
    cert = job.get('run_certificate') or {}; strata = cert.get('per_stratum') or {}; floor = plan['acceptance']['floor']
    reasons, passes = [], True
    for code in plan['target_languages']:
        acc = (strata.get(code) or {}).get('accuracy')
        if acc is None: reasons.append(f'{code}: not measured on the held-out set'); passes = False
        elif acc < floor: reasons.append(f'{code}: {acc:.1%} below the {floor:.0%} floor'); passes = False
        else: reasons.append(f'{code}: {acc:.1%} at or above the {floor:.0%} floor')
    for code, before in (plan.get('reference_accuracy') or {}).items():
        after = (strata.get(code) or {}).get('accuracy')
        if before is not None and after is not None and after < before - 0.02:
            reasons.append(f'{code}: regressed from {before:.1%} to {after:.1%}'); passes = False
    probe = ((cert.get('sealed_contract_check') or {}).get('no_speaker_id_probe') or {})
    egress = (probe.get('egress_surface') or {}).get('at_chance_all_languages')
    if probe.get('measured') and egress is False: reasons.append('speaker probe on the served output above chance'); passes = False
    elif probe.get('measured'): reasons.append('speaker probe on the served output at chance')
    metrics = {code: {'accuracy': v.get('accuracy'), 'abstention_rate': v.get('abstention_rate')} for code, v in strata.items() if isinstance(v, dict)}
    return {'decision': 'admitted' if passes else 'refused', 'reasons': reasons, 'metrics': metrics, 'compute': cert.get('compute'), 'artefact_sha256': cert.get('artefact_sha256'), 'at': lab.now()}


def _music_outcome(plan, job):
    result = (job.get('receipt') or {}).get('result') or {}; against = result.get('against_baseline') or {}; fl = result.get('file_level') or {}
    reasons, passes = [], True
    for name in ('accuracy', 'recall', 'precision'):
        verdict = against.get(name); ours = (fl.get(name) or {}).get('estimate'); theirs = (plan['acceptance']['baseline'] or {}).get(name)
        if verdict is None: reasons.append(f'{name}: not comparable'); passes = False
        elif verdict: reasons.append(f'{name}: {ours:.1%} versus baseline {theirs:.1%}')
        else: reasons.append(f'{name}: {ours:.1%} below baseline {theirs:.1%}'); passes = False
    if result.get('recipe', {}).get('smoke'): reasons.append('smoke run — not an acceptance run'); passes = False
    return {'decision': 'admitted' if passes else 'refused', 'reasons': reasons, 'metrics': {k: (fl.get(k) or {}) for k in ('accuracy', 'recall', 'precision', 'specificity')},
            'items': result.get('items'), 'compute': result.get('training'), 'artefact_sha256': (result.get('artefact') or {}).get('sha256'), 'at': lab.now()}


MAX_ATTEMPTS = 3


async def evaluate_finished(tenant=TENANT):
    from services.audio_plane_v1 import language_cognition_dispatch as lc
    from services.training_runner import m9_dispatch
    for record in signoff.with_status(tenant, 'dispatched'):
        plan, run_id, job_id = record['plan'], record['run_id'], record['dispatch']['job_id']
        job = (lc if plan['kind'] == 'audio_language_corrective' else m9_dispatch).load_job(job_id)
        if not job or job['status'] in ('running', 'submitting'): continue
        if job['status'] != 'completed':
            reason = ((job.get('receipt') or {}).get('error') or {}).get('message') or job.get('reason') or job['status']
            attempts = len(record.get('attempts') or []) + 1
            attempt_log = (record.get('attempts') or []) + [{**record['dispatch'], 'status': job['status'], 'reason': reason, 'ended_at': lab.now()}]
            if job['status'] == 'failed' and attempts < MAX_ATTEMPTS:
                # A fault before any result does not change what was signed; the same digest is dispatched again, on the record.
                signoff.update(tenant, run_id, status='signed', dispatch=None, attempts=attempt_log)
                conversation.record(tenant, run_id, conversation.note(tenant, f"Run {job_id} stopped before a result ({str(reason)[:160]}). The signed plan is unchanged, so I am starting it again — attempt {attempts + 1} of {MAX_ATTEMPTS}; every attempt stays on the record.", origin='autopilot'))
                continue
            signoff.update(tenant, run_id, status='failed', attempts=attempt_log, dispatch={**record['dispatch'], 'status': job['status'], 'reason': reason})
            conversation.record(tenant, run_id, conversation.note(tenant, f"Run {job_id} stopped without a result ({str(reason)[:160]}). The signature and the record stay as written; open the next version to try again.", widget='refused', origin='autopilot'))
            continue
        outcome = _audio_outcome(plan, job) if plan['kind'] == 'audio_language_corrective' else _music_outcome(plan, job)
        signoff.update(tenant, run_id, status='completed', outcome=outcome, dispatch={**record['dispatch'], 'status': 'completed'})
        verdict = 'Admitted' if outcome['decision'] == 'admitted' else 'Refused'
        conversation.record(tenant, run_id, conversation.note(tenant, f"{verdict} against the acceptance you signed: " + '; '.join(outcome['reasons']) + '.', widget='checks' if outcome['decision'] == 'admitted' else 'refused', origin='autopilot'))
        try:
            from services.transform_forms.doc_studio import service as studio
            document, _ = await studio.create_authored('training-whitepaper', job_id, tenant, record['signed_by'])
            conversation.record(tenant, run_id, conversation.note(tenant, 'The findings paper is written in Documents from this run\'s record — authored by the frontier writer, every figure by reference, gated before release.', widget='doc', commission_id=document['commission_id'], origin='autopilot'))
        except Exception as exc:
            log.exception('authored report for %s failed', run_id)
            conversation.record(tenant, run_id, conversation.note(tenant, f"The findings paper could not be commissioned yet ({type(exc).__name__}); the run record itself is complete.", origin='autopilot'))


async def tick(tenant=TENANT):
    await asyncio.to_thread(refresh_running)
    try: await asyncio.to_thread(advance_music, tenant)
    except Exception: log.exception('advance_music failed')
    await evaluate_finished(tenant)
    await asyncio.to_thread(dispatch_signed, tenant)


def kick(background):
    """Run one tick in the request's background; the 15-minute cron is the floor, not the ceiling."""
    background.add_task(tick)
