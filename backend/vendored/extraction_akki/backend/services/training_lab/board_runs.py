"""Runs the owner opens in the Train Models studio. A shaped run is a recorded intention: five fields, a name and a status.
It never carries compute, weights or an admission; the GPU jobs on the board come from their own records."""
import re
import uuid

from services.training_lab import store as lab

FIELDS = [('produces', 'What it produces'), ('material', 'What it reads'), ('acceptance', 'How we\'ll know'),
          ('spend_limit', 'Spend limit'), ('legal_basis', 'Legal basis')]
OPENING = ('What should the model do for the business? We will define its target outcome and collection schema, including the registered population, '
           'accuracy and coverage for each stratum, a sealed evaluation set, constraints and lawful sources. Calibration comes before the full-run quote. No training starts from this conversation.')
NEXT_VERSION = ('New run opened from {parent}. {parent} is untouched — it keeps its record, its status and its reason. '
                'Its objective carries over. What should change in this version?')
ADJUST = ('New run opened from {parent} so the refusal stays on record. Tell me what to adjust — recipe, data or acceptance — '
          'and I\'ll record it against this version before anything else is asked.')


def collection():
    coll = lab.db().training_lab_board_runs
    coll.create_index([('tenant_id', 1), ('run_id', 1)], unique=True)
    return coll


def overrides():
    coll = lab.db().training_lab_board_overrides
    coll.create_index([('tenant_id', 1), ('run_id', 1)], unique=True)
    return coll


def base_name(name):
    return re.sub(r'\s+v\d+$', '', name or '').strip()


def next_version(name, existing_names):
    base = base_name(name)
    versions = [int(m.group(1)) if m.group(1) else 1 for n in existing_names for m in [re.fullmatch(re.escape(base) + r'(?:\s+v(\d+))?', n or '')] if m]
    return f"{base} v{max(versions + [1]) + 1}"


def create(tenant, actor, *, parent=None, mode='new', name=None):
    run_id = 'shape-' + uuid.uuid4().hex[:12]
    fields = {}
    if parent:
        fields['produces'] = parent.get('objective') or ''
        if parent.get('family') in ('text', 'audio'): fields['material'] = 'RMS transcripts' if parent['family'] == 'text' else 'Staged authorized RMS audio'
    doc = {'run_id': run_id, 'tenant_id': tenant, 'actor': actor['principal_id'], 'status': 'Shaping', 'name': name or 'New model',
           'fields': fields, 'lineage': parent['run_id'] if parent else None, 'mode': mode, 'created_at': lab.now(), 'updated_at': lab.now(), 'held_at': None}
    collection().insert_one(doc)
    doc.pop('_id', None)
    return doc


def get(tenant, run_id):
    return collection().find_one({'tenant_id': tenant, 'run_id': run_id}, {'_id': 0})


def list_runs(tenant):
    return list(collection().find({'tenant_id': tenant}, {'_id': 0}).sort('created_at', -1))


def update(tenant, run_id, *, fields=None, name=None):
    patch = {'updated_at': lab.now()}
    for key, value in (fields or {}).items():
        if key in dict(FIELDS) and isinstance(value, str) and value.strip(): patch[f'fields.{key}'] = value.strip()[:400]
    if isinstance(name, str) and name.strip(): patch['name'] = name.strip()[:80]
    collection().update_one({'tenant_id': tenant, 'run_id': run_id}, {'$set': patch})


def ready(doc):
    from services.training_lab.production_contracts import Definition
    try:
        Definition.model_validate(doc.get('definition'))
        return True
    except ValueError:
        return False


def hold(tenant, run_id):
    collection().update_one({'tenant_id': tenant, 'run_id': run_id, 'status': 'Shaping'}, {'$set': {'status': 'In Approval', 'held_at': lab.now(), 'updated_at': lab.now()}})


def delete(tenant, run_id):
    result = collection().delete_one({'tenant_id': tenant, 'run_id': run_id, 'status': 'Shaping'})
    if result.deleted_count: lab.db().training_lab_conversations.delete_one({'tenant_id': tenant, 'run_id': run_id})
    return bool(result.deleted_count)


def retire(tenant, actor, run_id):
    overrides().update_one({'tenant_id': tenant, 'run_id': run_id}, {'$set': {'retired_at': lab.now(), 'actor': actor['principal_id']}}, upsert=True)


def retired(tenant):
    return {row['run_id']: row for row in overrides().find({'tenant_id': tenant}, {'_id': 0})}
