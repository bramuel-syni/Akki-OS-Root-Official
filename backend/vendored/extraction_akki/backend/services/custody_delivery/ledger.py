import json
import uuid
from services.ledger_writer.principal_control import append_event, read_events, CommandConflict
from services.ledger_writer.mongo_control import digest
from services.enforce.control_scope import require_control_scope
from services.northena.execution_models import Held
from services.custody_delivery.models import DeliveryDescriptor

RESOURCE = 'custody_delivery'


async def rows(db, delivery_id):
    scope = require_control_scope()
    events = await read_events(db, {'row.tenant_id': scope.tenant_id, 'row.resource_type': RESOURCE,
                                    'row.run_id': delivery_id, 'payload.principal_id': scope.principal_id})
    return events


async def append(db, descriptor, slot, data):
    scope = require_control_scope()
    if (scope.tenant_id, scope.principal_id) != (descriptor.tenant_id, descriptor.principal_id):
        raise Held('CUSTODY_SCOPE_MISMATCH')
    return await append_event(db, tenant_id=scope.tenant_id, run_id=descriptor.delivery_id,
        command_id=digest({'delivery': descriptor.delivery_id, 'slot': slot}), event_type='custody.' + slot,
        resource_type=RESOURCE, decision=slot, reason_code='CUSTODY_METADATA_RECORDED',
        payload={'principal_id': scope.principal_id, 'slot': slot, 'descriptor_sha256': descriptor.digest(), 'data': data})


async def create(db, descriptor):
    try:
        return await append(db, descriptor, 'intent', {'descriptor': descriptor.model_dump(mode='json')})
    except CommandConflict:
        raise Held('CUSTODY_IDEMPOTENCY_CONFLICT') from None


async def load(db, delivery_id, request_id):
    events = await rows(db, delivery_id)
    intent = next((e for e in events if e['payload']['slot'] == 'intent'), None)
    if intent is None:
        raise Held('CUSTODY_DELIVERY_NOT_FOUND')
    descriptor = DeliveryDescriptor.model_validate_json(json.dumps(intent['payload']['data']['descriptor']))
    if descriptor.request_id != request_id:
        raise Held('CUSTODY_DELIVERY_NOT_FOUND')
    return descriptor, events


async def claim(db, descriptor):
    try:
        await append(db, descriptor, 'dispatch', {'attempt_id': uuid.uuid4().hex})
        return True
    except CommandConflict:
        return False