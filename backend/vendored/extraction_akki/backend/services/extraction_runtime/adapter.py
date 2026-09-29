"""Source executor adapter: Coordinator RPCs → descriptor-bound admitted runtime calls.

Selection was recorded at commission (Plan.worker_ref → Worker receipt → runtime_id). This
adapter resolves that descriptor, ships the reviewed bundle plus the frozen work order, and
maps the runtime's metadata receipt back into a `WorkerResult`. Terminal results bank the
worker's signed measurements/lineage receipts and settle the reservation, idempotently.
"""
import hashlib
import json
import os
from pathlib import Path
from services.activation.approvals import approved_plan
from services.activation.bounded_adapter import BoundedEngineAdapter
from services.estate_admission import signing
from services.activation.reservations import Reservations
from services.estate_admission.records import latest
from services.estate_admission.runtimes import runtime_by_id
from services.extraction_runtime import objects, remote
from services.northena.execution_journal import LedgerJournal
from services.northena.execution_models import Artifact, Held, Usage, WorkerResult
from services.work_orders import packaging, sizing

CALL_SECONDS = 90


def lawful_basis_sha256():
    return hashlib.sha256(Path(os.environ['CENSUS_LAWFUL_BASIS_PATH']).read_bytes()).hexdigest()


def object_store_secrets(tenant, custody):
    """What the runtime needs to reach the tenant's store. A shared filesystem needs no secret at all."""
    provider = custody.get('provider')
    if provider == 'shared_filesystem':
        return {'provider': provider, 'bucket': custody['bucket'], 'prefix': custody['prefix']}
    if provider == 'huawei_obs':
        access = json.loads(Path(os.environ['AKKI_CENSUS_JUMP_CONFIG']).read_text())['obs']
        return {'provider': provider, 'endpoint': access['endpoint'], 'region': access['region'], 'access_key_id': access['access_key_id'],
                'secret_access_key': access['secret_access_key'], 'bucket': custody['bucket']}
    raise Held('CUSTODY_PROVIDER_NOT_BOUND')


def source_secrets(request, order, descriptor):
    from services.census_autonomy import deep_dispatch
    selection = order['selection']
    config = deep_dispatch.connector_for(request.request_id, request.tenant_id, selection['source_id'], lawful_basis_sha256())
    if config['driver'] == 'rds_data':
        # One connection per database; the census named each by its database (deep_sql.run).
        expected = 'source_' + hashlib.sha256((selection['source_id'] + '|' + selection['database']).encode()).hexdigest()[:24]
        if expected != selection['source_ref'] or selection['database'] not in config['databases']:
            raise Held('SOURCE_CONNECTION_UNRESOLVED')
        secrets = {'connection': {'driver': 'rds_data', **{k: config[k] for k in ('region', 'cluster_arn', 'secret_arn',
                                                                                    'aws_access_key_id', 'aws_secret_access_key')}}}
    else:
        connection = next((c for c in config['connections'] if 'source_' + hashlib.sha256(
            (selection['source_id'] + '|' + c['label']).encode()).hexdigest()[:24] == selection['source_ref']), None)
        if connection is None:
            raise Held('SOURCE_CONNECTION_UNRESOLVED')
        secrets = {'connection': {'driver': 'mysql', **{k: connection[k] for k in ('host', 'port', 'user', 'password')}}}
    if selection['source_id'] in descriptor['reach'].get('pull_seam', []):
        secrets['pull_via'] = deep_dispatch.pull_seam_hop()
    return secrets


class SourceRuntimeAdapter:
    def __init__(self, db, receipts):
        self.db, self.receipts = db, receipts

    async def _context(self, request):
        plan, plan_ref, _, _, events = await approved_plan(self.receipts, request)
        worker = await self.receipts.resolve(plan.worker_ref, kind='worker', events=events)
        descriptor = await runtime_by_id(self.db, request.tenant_id, worker.claims['runtime_id'])
        if descriptor['principal_id'] != worker.signer_id:
            raise Held('WORKER_RUNTIME_SIGNER_MISMATCH')
        order, order_ref = await packaging.load(self.db, request)
        if order is None:
            raise Held('WORK_ORDER_NOT_FROZEN')
        return plan, descriptor, order

    def _base(self, request, order, operation_key, fence, mode):
        return {'mode': mode, 'tenant_id': request.tenant_id, 'request_id': request.request_id,
                'request_sha256': request.digest(), 'operation_key': operation_key, 'fence': fence,
                'scope_refs': list(request.scope_refs), 'job_kind': order['job_kind']}

    def _result(self, request, descriptor, value):
        receipt_id = value.get('worker_receipt_id') or 'ewr-unreceipted'
        artifacts = tuple(Artifact.model_validate(a) for a in value.get('artifacts', []))
        usage = value.get('usage')
        return WorkerResult(operation_key=value['operation_key'], request_sha256=value['request_sha256'],
            executor_id=descriptor['principal_id'], fence=int(value['fence']), state=value['state'],
            receipt_ref=f"akki://runtime/{descriptor['runtime_id']}/{value['operation_key']}/{receipt_id}",
            artifacts=artifacts, usage=tuple(Usage.model_validate(u) for u in usage) if usage is not None else None,
            evidence_mode='measured')

    async def admit_limits(self, request, operation_key, fence, envelope):
        plan, descriptor, order = await self._context(request)
        control = {**self._base(request, order, operation_key, fence, 'admit_limits'),
                   'envelope': envelope.model_dump(mode='json')}
        value = await remote.call_async(descriptor, control, deadline_seconds=CALL_SECONDS)
        if value.get('status') != 'acknowledged':
            raise Held('WORKER_LIMIT_ACK_REFUSED')
        return signing.runtime_receipt(value['receipt'])

    async def submit(self, request, operation_key, fence, authority):
        plan, descriptor, order = await self._context(request)
        return await self._deliver(request, descriptor, order, operation_key, fence)

    async def _deliver(self, request, descriptor, order, operation_key, fence):
        custody = await latest(self.db, request.tenant_id, 'custody_descriptor', 'default')
        if custody is None:
            raise Held('CUSTODY_DESCRIPTOR_UNRESOLVED')
        custody = custody['payload']['record']
        secrets = source_secrets(request, order, descriptor)
        secrets['object_store'] = object_store_secrets(request.tenant_id, custody)
        control = {**self._base(request, order, operation_key, fence, 'submit'), 'selection': order['selection'],
                   'floor': order['floor'], 'artifact_ref': order['artifact_ref'], 'parent_refs': list(request.input_refs),
                   'object_key': f"{custody['prefix'].strip('/')}/{request.request_id}/{operation_key}/units.jsonl",
                   'principal_id': request.principal_id, 'secrets': secrets}
        value = await remote.call_async(descriptor, control, deadline_seconds=CALL_SECONDS)
        return await self._observe(request, descriptor, value)

    async def status(self, request, operation_key, fence):
        plan, descriptor, order = await self._context(request)
        value = await remote.call_async(descriptor, self._base(request, order, operation_key, fence, 'status'),
                                        deadline_seconds=CALL_SECONDS)
        if value.get('state') == 'unknown' and value.get('reason_code') == 'JOB_NOT_SUBMITTED':
            # The send was claimed once but never reached the runtime: resume by the same stable key.
            # The runtime refuses a second acceptance of the same key, so the effect stays at-most-once.
            return await self._deliver(request, descriptor, order, operation_key, fence)
        return await self._observe(request, descriptor, value)

    async def cancel(self, request, operation_key, fence):
        plan, descriptor, order = await self._context(request)
        value = await remote.call_async(descriptor, self._base(request, order, operation_key, fence, 'cancel'),
                                        deadline_seconds=CALL_SECONDS)
        return await self._observe(request, descriptor, value)

    async def _observe(self, request, descriptor, value):
        """Bank signed worker receipts on terminal facts; idempotent by receipt digest. The metering
        record carries the sizing estimate and the runtime's own actual side by side."""
        if value.get('state') in {'complete', 'failed', 'cancelled'} and value.get('receipts'):
            refs = {}
            for name, raw in value['receipts'].items():
                refs[name] = await self.receipts.record(signing.runtime_receipt(raw))
            rows = await LedgerJournal(self.db).read(request)
            limits = next((r for r in rows if r['slot'] == 'runtime_limits'), None)
            settled = None
            if limits is not None and 'measurements' in refs:
                try:
                    settled = await Reservations(self.receipts).settle(limits['data']['envelope']['reservation_ref'], refs['measurements'])
                except Held as exc:
                    if exc.reason_code != 'RESERVATION_MEASUREMENT_DIMENSIONS_MISMATCH':
                        raise
            order, _ = await packaging.load(self.db, request)
            progress = value.get('progress') or {}
            scale_actual = {'scanned_records': progress.get('scanned'), 'bytes_read': progress.get('bytes_read')}
            value = {**value, 'receipt_refs': refs, 'settlement_ref': settled,
                     'sizing_settlement': sizing.settlement(order['job_kind'], order['sizing'],
                                                            value['receipts']['measurements']['claims'].get('quantities', []), scale_actual)
                     if order and order.get('sizing') and 'measurements' in value['receipts'] else None}
            await objects.record(self.db, request, value)
        return self._result(request, descriptor, value)


def build_source_adapter(db, receipts):
    adapter = SourceRuntimeAdapter(db, receipts)
    return BoundedEngineAdapter(kind='source', engine='mtafiti', submit_rpc=adapter.submit, status_rpc=adapter.status,
                                cancel_rpc=adapter.cancel, timeout_seconds=float(CALL_SECONDS + 30),
                                admit_limits_rpc=adapter.admit_limits)
