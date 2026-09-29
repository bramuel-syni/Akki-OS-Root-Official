"""Object-store custody provider: grants and completions are signed on the custodian runtime.

Default per the M3 ruling: the sealed artefact already sits in the tenant's own object store;
completion is evidenced by the store receipt plus the requester's authorised-retrieval receipt.
E1 never fetches or streams the object.
"""
import time
from pydantic import SecretStr
from services.estate_admission import signing
from services.custody_delivery.ports import ProviderState
from services.enforce.control_scope import require_control_scope
from services.estate_admission.records import latest
from services.estate_admission.runtimes import runtime_by_id
from services.extraction_runtime import remote
from services.extraction_runtime.adapter import CALL_SECONDS, object_store_secrets
from services.extraction_runtime.objects import RESOURCE as OBJECTS
from services.ledger_writer.mongo_control import digest
from services.ledger_writer.principal_control import append_event, read_events
from services.northena.execution_models import Held

RETRIEVAL = 'custody_retrieval'


async def record_retrieval(db, delivery_id, request_id):
    scope = require_control_scope()
    now = int(time.time())
    event = await append_event(db, tenant_id=scope.tenant_id, run_id=delivery_id,
        command_id=digest({'retrieval': delivery_id}), event_type='custody.retrieval_authorised', resource_type=RETRIEVAL,
        decision='authorised', reason_code='AUTHORISED_RETRIEVAL_DECLARED',
        payload={'principal_id': scope.principal_id, 'delivery_id': delivery_id, 'request_id': request_id, 'redeemed_epoch': now})
    return event['payload']['redeemed_epoch'], event['row']['hash']


async def retrieval_for(db, delivery_id):
    scope = require_control_scope()
    events = await read_events(db, {'row.tenant_id': scope.tenant_id, 'row.resource_type': RETRIEVAL,
                                    'row.run_id': delivery_id, 'payload.principal_id': scope.principal_id})
    return events[0]['payload'] if events else None


class ObjectStoreCustody:
    def __init__(self, db, receipts, max_grant_seconds):
        self.db, self.receipts, self.max_grant_seconds = db, receipts, max_grant_seconds

    async def _sealed(self, descriptor):
        scope = require_control_scope()
        events = await read_events(self.db, {'row.tenant_id': descriptor.tenant_id, 'row.resource_type': OBJECTS,
                                             'row.run_id': descriptor.request_id, 'payload.principal_id': scope.principal_id})
        matches = [e['payload'] for e in events if e['payload']['request_sha256'] == descriptor.request_sha256
                   and any(a['ref'] == descriptor.artifact.ref for a in e['payload'].get('artifacts', []))]
        if not matches or not matches[-1].get('object'):
            raise Held('SEALED_OBJECT_UNRESOLVED')
        return matches[-1]['object']

    async def _custodian(self, tenant):
        custody = await latest(self.db, tenant, 'custody_descriptor', 'default')
        if custody is None:
            raise Held('CUSTODY_DESCRIPTOR_UNRESOLVED')
        record = custody['payload']['record']
        return record, await runtime_by_id(self.db, tenant, record['custodian_runtime_id'])

    def _control(self, descriptor, sealed, custody, mode):
        return {'mode': mode, 'tenant_id': descriptor.tenant_id, 'request_sha256': descriptor.request_sha256,
                'operation_key': 'custody', 'fence': 0, 'scope_refs': list(descriptor.scope_refs),
                'delivery_id': descriptor.delivery_id, 'principal_id': descriptor.principal_id,
                'descriptor_sha256': descriptor.digest(),
                'artifact': {'sha256': descriptor.artifact.sha256, 'size_bytes': descriptor.artifact.size_bytes,
                             'bucket': sealed['bucket'], 'key': sealed['key']},
                'origin': custody['endpoint_origin'],
                'secrets': {'object_store': object_store_secrets(descriptor.tenant_id, custody)}}

    async def prepare(self, descriptor, authority):
        sealed = await self._sealed(descriptor)
        custody, runtime = await self._custodian(descriptor.tenant_id)
        grant_seconds = min(self.max_grant_seconds, int(authority.expires_epoch - time.time()) - 5)
        if grant_seconds <= 0:
            raise Held('CUSTODY_AUTHORITY_WINDOW_TOO_SHORT')
        control = {**self._control(descriptor, sealed, custody, 'custody_prepare'), 'grant_seconds': grant_seconds}
        value = await remote.call_async(runtime, control, deadline_seconds=CALL_SECONDS)
        if value.get('status') != 'offered':
            raise Held(value.get('reason_code', 'CUSTODY_GRANT_REFUSED'))
        return ProviderState(grant=signing.runtime_receipt(value['receipt']), url=SecretStr(value['url']))

    async def status(self, descriptor, authority):
        retrieval = await retrieval_for(self.db, descriptor.delivery_id)
        if retrieval is None:
            return ProviderState()
        from services.custody_delivery import ledger
        rows = await ledger.rows(self.db, descriptor.delivery_id)
        grant = next((e for e in rows if e['payload']['slot'] == 'grant'), None)
        if grant is None:
            return ProviderState()
        sealed = await self._sealed(descriptor)
        custody, runtime = await self._custodian(descriptor.tenant_id)
        control = {**self._control(descriptor, sealed, custody, 'custody_status'),
                   'grant_receipt_ref': grant['payload']['data']['receipt_ref'], 'redeemed_epoch': retrieval['redeemed_epoch']}
        value = await remote.call_async(runtime, control, deadline_seconds=CALL_SECONDS)
        if value.get('status') != 'completed':
            raise Held(value.get('reason_code', 'CUSTODY_COMPLETION_REFUSED'))
        return ProviderState(completion=signing.runtime_receipt(value['receipt']))
