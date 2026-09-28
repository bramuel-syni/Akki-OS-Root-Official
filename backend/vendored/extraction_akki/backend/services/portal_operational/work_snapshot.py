"""One verified canonical prefix for a work view; no cache or alternate ledger.

Previously listing re-read/re-verified the entire prefix separately for DAP,
execution and custody. Reusing one immutable read also avoids mixed-head views.
The original per-record projection/redaction and current release gates remain.
"""
from services.ledger_writer.principal_control import read_events
from services.portal_operational.delivery_history import group_events, expected_artifacts, project as delivery_project
from services.portal_operational.execution_records import project as execution_project


async def read_snapshot(db, scope):
    events = await read_events(db, {'row.tenant_id': scope['tenant_id'],
                                  'payload.principal_id': scope['principal_id']})
    requests, executions = {}, {}
    for event in events:
        if (event['row']['tenant_id'] != scope['tenant_id']
                or event['payload'].get('principal_id') != scope['principal_id']):
            raise ValueError('Work snapshot identity mismatch.')
        target = {'dap_request': requests, 'execution_flow': executions}.get(event['row']['resource_type'])
        if target is not None:
            target.setdefault(event['row']['run_id'], []).append(event)
    return requests, executions, group_events(events, scope)


async def project_snapshot(db, scope, snapshot, request_id):
    from services.northena.portal_work import project
    requests, executions, deliveries = snapshot
    events = executions.get(request_id, [])
    work = execution_project(project(requests[request_id]), events)
    return await delivery_project(db, scope, work, deliveries.get(request_id, []), expected=expected_artifacts(events))