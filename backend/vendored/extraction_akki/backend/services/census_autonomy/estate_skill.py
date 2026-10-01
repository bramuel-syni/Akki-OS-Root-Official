"""Expert brief and production plan from the existing measured estate, not a second census."""
import hashlib
import json


def package(report):
    ref = report['job_id']
    strategies = (report.get('cost_strategies') or {}).get('items') or []
    products = report.get('data_products') or []
    actions = []
    for item in strategies:
        actions.append({'source_ref': ref, 'title': item['title'], 'class': 'estimated',
            'addressable_bytes': item.get('bytes'), 'monthly_saving': item.get('monthly_saving'),
            'conditions': [item.get('risk') or 'Validate operational impact and rights before acting.'],
            'execution': 'proposal_only', 'destructive_action_authorized': False})
    for item in products:
        actions.append({'source_ref': ref, 'title': item['title'], 'class': 'inferred',
            'purpose': 'Prepare a bounded dataset specification', 'dimensions': item.get('dimensions') or [],
            'conditions': item.get('blockers') or ['Independent rights, quality and intended-use review'],
            'execution': 'proposal_only', 'training_authorized': False})
    identity = {'source_ref': ref, 'measured_at': report.get('measured_at'), 'actions': actions}
    return {'plan_id': 'estate-' + hashlib.sha256(json.dumps(identity, sort_keys=True, default=str).encode()).hexdigest()[:20],
        'source_ref': ref, 'expert': {'objective': 'Identify bounded cost, quality and reuse opportunities',
            'basis': 'Retained aggregate measurements and explicitly labelled estimates',
            'judgment': (report.get('dossier') or {}).get('text') if isinstance(report.get('dossier'), dict) else None},
        'manager': {'actions': actions, 'document_producer': 'estate-intelligence',
            'dataset_handoff': 'An explicit TargetOutcome and CollectionSchema are required before preparation; candidates are not training permission.'},
        'manifest': [{'artifact': 'census_report', 'class': 'measured', 'source_ref': ref}]
            + [{'artifact': a['title'], 'class': a['class'], 'source_ref': ref} for a in actions],
        'limits': ['No new estate read or rights grant', 'Savings are estimates, not realised returns', 'Dataset candidates are not qualified or sealed datasets'],
        'execution_authorized': False}