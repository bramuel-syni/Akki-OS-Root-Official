"""Project accepted custody events into existing work history, never bearer URLs.

These are historical verified facts, not a fresh right to download. The delivery
endpoint still revalidates current authority and signatures independently.
"""
from datetime import datetime, timezone
from services.ledger_writer.principal_control import read_events
from services.portal_operational.models import HistoryEntry


async def grouped(db, scope):
    events = await read_events(db, {'row.tenant_id': scope['tenant_id'], 'row.resource_type': 'custody_delivery',
                                    'payload.principal_id': scope['principal_id']})
    requests = {e['row']['run_id']: e['payload']['data']['descriptor']['request_id'] for e in events if e['payload'].get('slot') == 'intent'
           and e['payload']['data']['descriptor'].get('principal_id') == scope['principal_id']
           and e['payload']['data']['descriptor'].get('tenant_id') == scope['tenant_id']}
    grouped_events = {}
    for event in events:
        request_id = requests.get(event['row']['run_id'])
        if request_id is not None:
            grouped_events.setdefault(request_id, []).append(event)
    return grouped_events


def expected_artifacts(execution_events):
    terminal = next((e['payload']['data'] for e in execution_events if e['payload'].get('slot') == 'terminal'), None)
    return set(terminal.get('artifact_refs', ())) if terminal and terminal.get('phase') == 'ready' and terminal.get('evidence_mode') == 'measured' else set()


async def project(db, scope, work, selected=None, expected=()):
    if selected is None:
        selected = (await grouped(db, scope)).get(work.request_id, [])
    if not selected:
        return work
    codes = {'intent': 'CUSTODY_DELIVERY_REQUESTED', 'dispatch': 'CUSTODY_DELIVERY_REQUESTED',
             'grant': 'CUSTODY_CAPABILITY_ISSUED', 'uncertain': 'CUSTODY_PROVIDER_OUTCOME_UNCERTAIN',
             'completed': 'CUSTODY_COMPLETION_RECORDED'}
    history = list(work.history)
    per_delivery, completed_refs, delivered_artifacts = {}, [], set()
    artifacts = {e['row']['run_id']: e['payload']['data']['descriptor']['artifact']['ref']
                 for e in selected if e['payload']['slot'] == 'intent'}
    for event in selected:
        slot = event['payload']['slot']
        if slot not in codes:
            continue
        delivery_id = event['row']['run_id']
        if per_delivery.get(delivery_id) != 'completed':
            per_delivery[delivery_id] = slot
        if slot == 'completed':
            completed_refs.append(event['payload']['data']['receipt_ref'])
            delivered_artifacts.add(artifacts[event['row']['run_id']])
        if slot != 'dispatch':
            history.append(HistoryEntry(at=datetime.fromtimestamp(event['row']['at']['epoch_s'], timezone.utc).isoformat(),
                state=slot, event='custody_' + slot, reason_code=codes[slot], receipt_hash=event['row']['hash']))
    verified = bool(expected) and set(expected) <= delivered_artifacts
    last = selected[-1]
    last_stage = per_delivery[last['row']['run_id']]
    if completed_refs and not verified:
        last_stage = 'partial'
    return work.model_copy(update={'history': history, 'delivery_verified': verified,
        'delivery_state': last_stage, 'delivery_receipt_refs': list(dict.fromkeys(completed_refs))})