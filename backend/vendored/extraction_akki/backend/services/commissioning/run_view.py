"""Run view: one request's execution journal, budget, sealed object and deliveries — read-only projection."""
from datetime import datetime, timezone
from services.custody_delivery.ledger import RESOURCE as CUSTODY
from services.enforce.control_scope import require_control_scope
from services.extraction_runtime import objects
from services.ledger_writer.principal_control import read_events
from services.northena.execution_journal import LedgerJournal
from services.work_orders import packaging

PHASES = ['commissioned', 'reserved', 'limits_admitted', 'sent', 'observed', 'verified', 'metered', 'terminal']


def _at(row):
    return datetime.fromtimestamp(row['at_epoch'], timezone.utc).isoformat()


async def deliveries_for(db, request):
    scope = require_control_scope()
    events = await read_events(db, {'row.tenant_id': request.tenant_id, 'row.resource_type': CUSTODY,
                                    'payload.principal_id': scope.principal_id})
    by_id = {}
    for e in events:
        p = e['payload']
        if p['slot'] == 'intent' and p['data']['descriptor']['request_id'] != request.request_id:
            continue
        by_id.setdefault(e['row']['run_id'], []).append(e)
    rows = []
    for delivery_id, items in by_id.items():
        slots = {i['payload']['slot'] for i in items}
        intent = next((i for i in items if i['payload']['slot'] == 'intent'), None)
        if intent is None or intent['payload']['data']['descriptor']['request_id'] != request.request_id:
            continue
        state = 'completed' if 'completed' in slots else 'uncertain' if 'uncertain' in slots and 'grant' not in slots else 'offered' if 'grant' in slots else 'pending'
        rows.append({'delivery_id': delivery_id, 'state': state, 'artifact_ref': intent['payload']['data']['descriptor']['artifact']['ref'],
                     'receipt_refs': {i['payload']['slot']: i['row']['hash'] for i in items},
                     'at': datetime.fromtimestamp(items[-1]['row']['at']['epoch_s'], timezone.utc).isoformat()})
    return rows


async def run_view(db, request):
    rows = await LedgerJournal(db).read(request)
    order, order_ref = await packaging.load(db, request)
    sealed = await objects.lookup(db, request)
    timeline, reached = [], {'commissioned'} if order else set()
    envelope = usage = terminal = registry = None
    for row in rows:
        slot, data = row['slot'], row['data']
        entry = {'at': _at(row), 'slot': slot.split(':')[0], 'receipt_hash': row['hash']}
        if slot == 'dispatch' and data.get('action') == 'submit':
            reached.add('reserved'); entry['detail'] = 'Authority granted, reservation held against the estate allocation.'
        elif slot == 'runtime_limits':
            reached.add('limits_admitted'); envelope = data['envelope']
            entry['detail'] = 'Worker acknowledged the runtime envelope before any effect.'
        elif slot == 'send' and data.get('action') == 'submit':
            reached.add('sent'); entry['detail'] = 'Work order sent once to the admitted runtime.'
        elif slot.startswith('observation:'):
            reached.add('observed'); entry['detail'] = 'Worker state: ' + data['result']['state']
            entry['state'] = data['result']['state']
        elif slot == 'registry':
            reached.add('verified'); registry = data
            entry['detail'] = f"Independent inspection {data.get('inspection_ref', '')[:24]}…; {len(data.get('artifacts', []))} artifact(s) registered."
        elif slot == 'metered':
            reached.add('metered'); usage = data['usage']; entry['detail'] = 'Actual usage recorded before return.'
        elif slot == 'terminal':
            reached.add('terminal'); terminal = data; entry['detail'] = f"{data['phase']} · {data['reason_code']}"
        elif slot.startswith('uncertain:'):
            entry['detail'] = 'Outcome uncertain; reconciliation by stable key on the next advance.'
        elif slot.startswith('portal_view:') or slot == 'request' or slot == 'usage_handoff' or slot == 'verify_artifact' or slot.startswith('eligibility'):
            continue
        else:
            entry['detail'] = slot
        timeline.append(entry)
    budget = None
    if envelope:
        limits = {(q['dimension']): q for q in envelope['limits']}
        consumed = {u['unit']: u['quantity'] for u in (usage or [])}
        mapping = {'scanned_records': 'records_scanned', 'returned_records': 'records_returned', 'bytes_read': 'bytes_read',
                   'wall_clock': 'seconds', 'spend': 'usd_spend'}
        budget = [{'dimension': d, 'unit': q['unit'], 'limit': q['quantity'],
                   'consumed': consumed.get(mapping.get(d, d + ':' + q['unit']), None)}
                  for d, q in limits.items()]
        budget_window = {'starts_epoch': envelope['starts_epoch'], 'stop_work_by_epoch': envelope['stop_work_by_epoch'],
                         'terminate_by_epoch': envelope['terminate_by_epoch'], 'runtime_id': envelope['runtime_id']}
    else:
        budget_window = None
    return {'request_id': request.request_id, 'phases': [{'phase': p, 'reached': p in reached} for p in PHASES],
            'timeline': timeline, 'budget': budget, 'window': budget_window, 'terminal': terminal,
            'work_order': {k: v for k, v in (order or {}).items() if k not in ('manifest',)} | ({'dispatch_intent': order['manifest']['dispatch_intent']} if order else {}),
            'work_order_ref': order_ref,
            'sealed': {k: sealed.get(k) for k in ('object', 'artifacts', 'quality', 'progress', 'runtime_id', 'receipt_refs')} if sealed else None,
            'registry': {'artifacts': registry.get('artifacts'), 'records': [r['record'] for r in registry.get('records', [])],
                         'inspection_ref': registry.get('inspection_ref')} if registry else None,
            'deliveries': await deliveries_for(db, request)}
