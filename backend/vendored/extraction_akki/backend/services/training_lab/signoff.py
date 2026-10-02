"""Owner sign-off register. The only record that authorises training compute: one per run, bound by the digest of exactly what was
approved (recipe, data, host, compute cap, acceptance). The autopilot reads this register; nothing else starts training."""
import hashlib
import json

from services.training_lab import store as lab

REFERENCE_BASELINE = 'lcj-f96c86a16312'
SYSTEM_ACTOR = {'tenant_id': 'RMS', 'principal_id': 'akki-autopilot'}


def collection():
    coll = lab.db().training_lab_signoffs
    coll.create_index([('tenant_id', 1), ('run_id', 1)], unique=True)
    return coll


def digest(plan):
    return hashlib.sha256(json.dumps(plan, sort_keys=True, default=str).encode()).hexdigest()


def get(tenant, run_id):
    return collection().find_one({'tenant_id': tenant, 'run_id': run_id}, {'_id': 0})


def signer_label(principal_id):
    """The signer as a person reads it: account email, never the raw principal identifier."""
    from bson import ObjectId
    if principal_id == SYSTEM_ACTOR['principal_id']: return 'Akki autopilot'
    if not ObjectId.is_valid(str(principal_id)): return str(principal_id)
    user = lab.db().users.find_one({'_id': ObjectId(principal_id)}, {'_id': 0, 'email': 1, 'name': 1})
    return (user or {}).get('name') or (user or {}).get('email') or 'the admitted operator'


def all_for(tenant):
    return {row['run_id']: row for row in collection().find({'tenant_id': tenant}, {'_id': 0})}


def with_status(tenant, *statuses):
    return list(collection().find({'tenant_id': tenant, 'status': {'$in': list(statuses)}}, {'_id': 0}))


def update(tenant, run_id, **fields):
    collection().update_one({'tenant_id': tenant, 'run_id': run_id}, {'$set': {**fields, 'updated_at': lab.now()}})
    return get(tenant, run_id)


def note(tenant, run_id, text):
    collection().update_one({'tenant_id': tenant, 'run_id': run_id}, {'$push': {'notes': {'at': lab.now(), 'text': text}}})


# ----------------------------------------------------------------------------- the approvable plans
def reinforcement_plan(tenant):
    from services.training_lab import languages
    data, bundle = languages.evidence(0.9)
    if bundle is None: return None
    request = bundle['plan']['held_training_request']; changes = request['proposed_recipe_changes']
    recipe = {'baseline_job_id': REFERENCE_BASELINE, 'seed': 41, 'epochs': int(changes['epochs']), 'batch_size': 2048, 'physical_batch_size': 1024,
              'max_windows_per_file': int(changes['max_windows_per_file']), 'parallelism': 24, 'lr': 0.0003, 'max_grad_norm': 1.0, 'delta': 1e-06, 'smoke_steps': 0,
              'logit_adjustment_tau': float(changes['logit_adjustment_tau']), 'condition_loss_weight': 0.05, 'noise_multiplier': 0.7, 'adversary_strength': 0.5,
              'bottleneck_dim': 64, 'bottleneck_noise': 0.25, 'speaker_loss_weight': 0.5, 'dp_enabled': False}
    return {'kind': 'audio_language_corrective', 'phase': 'train_corrective', 'host': 'akki-vm', 'gpu_index': 0, 'recipe': recipe,
            'target_languages': request['target_languages'], 'compute_cap_gpu_hours': request['compute_cap_gpu_hours'], 'stop_rule': request['stop_rule'],
            'acceptance': {'floor': data['floor'], 'targets': request['target_languages'], 'no_regression_against': REFERENCE_BASELINE,
                           'speaker_probe': 'served-output speaker probe at chance', 'statement': request['acceptance']},
            'reference_accuracy': {k: v['accuracy'] for k, v in data['languages'].items()}}


def music_plan(tenant):
    from services.training_lab import corpus_measurement, music_shipping
    rows = list(lab.db().training_lab_runs.find({'tenant_id': tenant, 'kind': 'music_baseline', 'status': 'complete'}, {'_id': 0}).sort('created_at', -1).limit(1))
    if not rows or (rows[0].get('result') or {}).get('status') != 'complete': return None
    baseline = rows[0]; learned = baseline['result']['baseline_learned']
    measurement = corpus_measurement.latest(tenant)
    items, pending = music_shipping.labelled_items(tenant)
    if pending or len(items) < 4: return None
    return {'kind': 'music_detector', 'phase': 'lab_train_music', 'host': 'akki-vm', 'gpu_index': 1,
            'recipe': {'seed': 41, 'epochs': 12, 'folds': 5, 'batch_size': 256, 'lr': 0.001, 'max_seconds_per_file': 600.0, 'max_windows_per_file': 240,
                       'weak_negatives_per_language': 40, 'weak_positive_files': 30},
            'labelled_items': [{k: it[k] for k in ('item_id', 'label', 'label_source', 'sha256', 'size_bytes')} for it in items],
            'baseline_run_id': baseline['run_id'], 'measurement_job_id': (measurement or {}).get('job_id') if (measurement or {}).get('status') == 'completed' else None,
            'compute_cap_gpu_hours': 1.5,
            'acceptance': {'rule': 'out-of-fold file-level accuracy and recall at or above the learned baseline point estimates; precision not below it',
                           'baseline': {'accuracy': learned['accuracy']['estimate'], 'recall': learned['recall']['estimate'], 'precision': learned['precision']['estimate'], 'items': baseline['result']['items']}}}


PLANS = {'reinforcement-lwg': reinforcement_plan, 'music-identification': music_plan}


def plan_for(tenant, run_id):
    builder = PLANS.get(run_id)
    return builder(tenant) if builder else None


def approval_view(tenant, run_id, plan):
    """What the board shows next to the Approve control: the digest the owner signs and any existing signature."""
    record = get(tenant, run_id)
    view = {'plan_sha256': digest(plan) if plan else None, 'signed': None, 'dispatch': None, 'outcome': None, 'status': None}
    if record:
        view.update(signed={'by': signer_label(record['signed_by']), 'at': record['signed_at'], 'plan_sha256': record['plan_sha256']}, dispatch=record.get('dispatch'),
                    outcome=record.get('outcome'), status=record['status'], shipping=record.get('shipping'))
    return view


def sign(tenant, actor, run_id, plan_sha256):
    plan = plan_for(tenant, run_id)
    if plan is None:
        raise ValueError('no approvable plan is recorded for this run yet')
    expected = digest(plan)
    if plan_sha256 != expected:
        raise ValueError('the plan changed since it was shown; read it again before approving')
    if get(tenant, run_id):
        raise ValueError('this run already carries a signature')
    record = {'tenant_id': tenant, 'run_id': run_id, 'plan_sha256': expected, 'plan': plan, 'signed_by': actor['principal_id'], 'signed_at': lab.now(),
              'scope': 'recipe, data, host, compute cap and acceptance exactly as digested', 'status': 'signed', 'dispatch': None, 'outcome': None, 'notes': [],
              'created_at': lab.now(), 'updated_at': lab.now()}
    collection().insert_one(dict(record))
    return get(tenant, run_id)
