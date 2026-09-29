"""Sealed-object locations and worker receipts on the ledger; metadata only, never bytes."""
from services.enforce.control_scope import require_control_scope
from services.ledger_writer.mongo_control import digest
from services.ledger_writer.principal_control import append_event, read_events

RESOURCE = 'extraction_object'


async def record(db, request, result):
    scope = require_control_scope()
    payload = {'principal_id': scope.principal_id, 'request_sha256': request.digest(),
               'operation_key': result['operation_key'], 'state': result.get('state'), 'object': result.get('object'),
               'artifacts': result.get('artifacts', []), 'quality': result.get('quality'),
               'progress': result.get('progress'), 'worker_receipt_id': result.get('worker_receipt_id'),
               'runtime_id': result['runtime_id'], 'receipt_refs': result.get('receipt_refs', {}),
               'settlement_ref': result.get('settlement_ref'), 'sizing_settlement': result.get('sizing_settlement'),
               'reason_code': result.get('reason_code')}
    event = await append_event(db, tenant_id=request.tenant_id, run_id=request.request_id,
        command_id=digest({'extraction_object': request.digest(), 'key': result['operation_key']}),
        event_type='extraction.object_sealed', resource_type=RESOURCE, decision='recorded',
        reason_code='EXTRACTION_OBJECT_RECORDED', payload=payload)
    return event['row']['hash']


async def lookup(db, request):
    scope = require_control_scope()
    events = await read_events(db, {'row.tenant_id': request.tenant_id, 'row.resource_type': RESOURCE,
                                    'row.run_id': request.request_id, 'payload.principal_id': scope.principal_id})
    matches = [e for e in events if e['payload']['request_sha256'] == request.digest()]
    return matches[-1]['payload'] if matches else None
