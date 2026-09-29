"""Tenant-scoped admission records on the one canonical ledger; no HTTP producer."""
from services.enforce.control_scope import require_control_scope
from services.ledger_writer.mongo_control import digest
from services.ledger_writer.principal_control import append_event, read_events

RESOURCE = 'estate_admission'
KINDS = ('principal_admission', 'admitted_signer', 'admitted_runtime', 'approval_groups',
         'custody_descriptor', 'dials', 'allocation_binding', 'rights_anchor', 'runtime_attestation')


async def records(db, tenant, kind):
    events = await read_events(db, {'row.tenant_id': tenant, 'row.resource_type': RESOURCE})
    return [e for e in events if e['payload'].get('kind') == kind]


async def latest(db, tenant, kind, record_id=None):
    """Last record wins per record_id; a later ceremony supersedes, never edits."""
    current = {}
    for event in await records(db, tenant, kind):
        current[event['payload']['record_id']] = event
    if record_id is not None:
        return current.get(record_id)
    return current


async def admit(db, tenant, kind, record_id, record):
    if kind not in KINDS:
        raise ValueError('Unknown estate admission record kind.')
    scope = require_control_scope()
    event = await append_event(db, tenant_id=tenant, run_id=f'estate:{kind}:{record_id}',
        command_id=digest({'estate': tenant, 'kind': kind, 'record_id': record_id, 'record': record}),
        event_type='estate_admission.' + kind, resource_type=RESOURCE, decision='admitted',
        reason_code='ESTATE_CEREMONY', payload={'principal_id': scope.principal_id, 'kind': kind,
                                                'record_id': record_id, 'record': record})
    return event['row']['hash']
