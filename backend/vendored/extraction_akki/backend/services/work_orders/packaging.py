"""Work-order packaging: frozen request + kind profile + selection → one durable manifest."""
from datetime import datetime, timezone
from services.enforce.control_scope import require_control_scope
from services.ledger_writer.mongo_control import digest
from services.ledger_writer.principal_control import append_event, read_events
from services.work_supervisor.job_manifest import parse_job_manifest

RESOURCE = 'work_order'


def build_manifest(profile, request, selection, worker_runtime_id, submitted_at=None):
    manifest = {
        'manifest_version': 0, 'job_id': request.request_id, 'job_kind': profile.job_kind,
        'submitter': request.principal_id,
        'submitted_at_utc': (submitted_at or datetime.now(timezone.utc)).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'scope': {'scope_refs': list(request.scope_refs), 'input_refs': list(request.input_refs),
                  'selection': selection},
        'output_contract': dict(profile.output_contract),
        'depends_on': [], 'dispatch_intent': 'runtime:' + worker_runtime_id, 'precondition_seals': [],
    }
    return parse_job_manifest(manifest).model_dump(mode='json')


async def record(db, request, order):
    scope = require_control_scope()
    event = await append_event(db, tenant_id=request.tenant_id, run_id=request.request_id,
        command_id=digest({'work_order': request.digest()}), event_type='work_order.frozen', resource_type=RESOURCE,
        decision='frozen', reason_code='WORK_ORDER_FROZEN',
        payload={'principal_id': scope.principal_id, 'request_sha256': request.digest(), 'order': order})
    return event['row']['hash']


async def load(db, request):
    scope = require_control_scope()
    events = await read_events(db, {'row.tenant_id': request.tenant_id, 'row.resource_type': RESOURCE,
                                    'row.run_id': request.request_id, 'payload.principal_id': scope.principal_id})
    matches = [e for e in events if e['payload']['request_sha256'] == request.digest()]
    return (matches[-1]['payload']['order'], matches[-1]['row']['hash']) if matches else (None, None)
