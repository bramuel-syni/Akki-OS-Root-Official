"""Research-only larger-model trial, dispatched through the same native M9 plane."""
from services.training_lab import malpha


def launch_larger_text_trial():
    existing = malpha.jobs(lane='story_text_comparison')
    if existing: return {'status': 'existing', 'job_id': existing[-1]['job_id']}
    host, index = malpha.HOST_ALLOCATION['malpha_story_text_train'][0][0], 1
    if not malpha.worker_audit_ready(host): raise ValueError('NATIVE_WORKER_AUDIT_REQUIRED')
    snapshot = malpha.gpu_snapshot(); device = snapshot['devices'].get((host, index))
    if device is None or (host, index) in malpha._busy_devices() or device['memory_used_mib'] > malpha.RESIDENT_PROTECTED_MIB:
        raise ValueError('RESEARCH_GPU_NOT_FREE: serving must be released explicitly; active training must never be stopped')
    base, registration = malpha._qwen_base_path(host, 'qwen3-8b-base')
    if not base or registration.get('licence_verified') != 'apache-2.0':
        raise ValueError('LARGER_BASE_NOT_REGISTERED')
    iteration = 1
    recipe = malpha.story_text_recipe(iteration, [], base)
    recipe.update(init_adapter=None, max_steps=3000, language_balance=True,
                  rationale='Owner-authorised larger registered 8B base capacity trial, research only. Evaluate base and adapter on identical dev documents. Not a causal 8B-vs-1.7B comparison unless data/worker/eval versions match.',
                  comparison={'kind': 'larger_registered_base_capacity_trial', 'product_admission_allowed': False,
                              'historical_reference_lane': 'story_text', 'causal_model_size_claim_allowed': False})
    rec = malpha._submit('STORY-KIK-KAM-SWA', 'story_text_comparison', 'malpha_story_text_train',
                        {'recipe': recipe, 'base_registration': registration}, host, index, iteration)
    return {'status': rec['status'], 'job_id': rec['job_id'], 'host': host, 'gpu_index': index, 'model': registration['repo']}


def borrow_serving_gpu_for_trial():
    """Explicit owner-authorised operation, NOT called by the recurring task."""
    from services.training_runner import m9_dispatch, m9_serving
    if malpha.jobs(lane='story_text_comparison'): return launch_larger_text_trial()
    host, index = malpha.HOST_ALLOCATION['malpha_story_text_train'][0][0], 1
    base, reg = malpha._qwen_base_path(host, 'qwen3-8b-base')
    if not base or reg.get('licence_verified') != 'apache-2.0': raise ValueError('LARGER_BASE_NOT_REGISTERED')
    if not malpha.worker_audit_ready(host): raise ValueError('NATIVE_WORKER_AUDIT_REQUIRED')
    if (host, index) in malpha._busy_devices(): raise ValueError('ACTIVE_TRAINING_MUST_NOT_BE_STOPPED')
    serving = [j for j in m9_dispatch.list_jobs() if j.get('phase') == 'serve' and j.get('status') == 'running'
               and j.get('host') == host and (j.get('params') or {}).get('gpu_index') == index]
    if len(serving) > 1: raise ValueError('AMBIGUOUS_SERVING_RESERVATION')
    if serving:
        job = serving[0]; model_id = job['params']['authority']['model_id']
        record = {'status': 'borrowing', 'serving_model_id': model_id, 'original_serving_job': job['job_id'],
                  'host': host, 'gpu_index': index, 'authorised_at': malpha.now(),
                  'owner_order': '2026-10-04: unload if you need to; preserve active training and all checkpoints'}
        malpha.db().malpha_commissions.update_one({'commission_id': 'STORY-KIK-KAM-SWA'}, {'$set': {'capacity_reallocation': record}})
        m9_serving.stop(model_id, 'Owner-approved temporary GPU reallocation for M Alpha research trial', 'akki-autopilot')
    try:
        result = launch_larger_text_trial()
        if result['status'] not in ('running', 'submitting'): raise ValueError('LARGER_TRIAL_NOT_RUNNING')
        malpha.db().malpha_commissions.update_one({'commission_id': 'STORY-KIK-KAM-SWA'}, {'$set': {'capacity_reallocation.status': 'borrowed', 'capacity_reallocation.trial_job': result['job_id']}})
        return result
    except Exception:
        restore_serving_after_trial(malpha.gpu_snapshot())
        raise


def restore_serving_after_trial(snapshot):
    from services.training_runner import m9_serving
    rec = (malpha.commission('STORY-KIK-KAM-SWA') or {}).get('capacity_reallocation') or {}
    if rec.get('status') not in ('borrowing', 'borrowed') or not rec.get('serving_model_id'): return None
    trials = malpha.jobs(lane='story_text_comparison')
    if any(j['status'] in ('running', 'submitting') for j in trials): return None
    slot = (rec['host'], rec['gpu_index']); device = snapshot['devices'].get(slot)
    if slot in malpha._busy_devices() or not device or device['memory_used_mib'] > malpha.RESIDENT_PROTECTED_MIB: return None
    result = m9_serving.start(rec['serving_model_id'], 'akki-autopilot', malpha._lawful(), gpu_index=rec['gpu_index'], host=rec['host'])
    if result['status'] == 'running':
        malpha.db().malpha_commissions.update_one({'commission_id': 'STORY-KIK-KAM-SWA'}, {'$set': {'capacity_reallocation.status': 'restored', 'capacity_reallocation.restored_at': malpha.now(), 'capacity_reallocation.restored_job': result['job_id']}})
    return result