"""Skill executor adapter: the deterministic unit-retrieval worker runs on the admitted worker runtime over the
sealed corpus; every anchor is attested on the independent inspector runtime; the grounding receipt is signed by the
worker. The question's terms are offered in-process for one request and are never persisted in E1.
"""
import time
from services.activation.approvals import approved_plan
from services.activation.bounded_adapter import BoundedEngineAdapter
from services.estate_admission import signing
from services.estate_admission.records import latest
from services.estate_admission.runtimes import runtime_by_id, select
from services.extraction_runtime import objects, remote
from services.extraction_runtime.adapter import CALL_SECONDS, SourceRuntimeAdapter, object_store_secrets
from services.extraction_runtime.skill_worker import snapshot_sha256
from services.ledger_writer.mongo_control import digest
from services.ledger_writer.principal_control import read_events
from services.non_gpu_governance import proofs
from services.northena.execution_models import Held

JOB_KIND = 'skill.unit_retrieval'
_OFFERED = {}


def offer_terms(request_sha256, terms, intent_receipt_ref, ttl_seconds=900):
    now = time.time()
    for key in [k for k, v in _OFFERED.items() if v['expires'] <= now]:
        _OFFERED.pop(key, None)
    _OFFERED[request_sha256] = {'terms': sorted(terms), 'intent_receipt_ref': intent_receipt_ref, 'expires': now + ttl_seconds}


def offered(request_sha256):
    value = _OFFERED.get(request_sha256)
    if value is None or value['expires'] <= time.time():
        raise Held('SKILL_QUERY_TERMS_UNAVAILABLE')
    return value


async def corpus_object(db, tenant, corpus_ref):
    """The sealed object behind a provisioned corpus slice: its recorded store location and verified identity."""
    events = await read_events(db, {'row.tenant_id': tenant, 'row.resource_type': objects.RESOURCE})
    for event in reversed(events):
        payload = event['payload']
        if payload.get('state') != 'complete' or not payload.get('object'):
            continue
        for artifact in payload.get('artifacts') or []:
            if artifact['ref'] == corpus_ref:
                return {'ref': artifact['ref'], 'sha256': artifact['sha256'], 'size_bytes': int(artifact['size_bytes']),
                        'tenant_id': artifact['tenant_id'], 'key': payload['object']['key']}
    raise Held('SKILL_CORPUS_OBJECT_UNRESOLVED')


def anchor_claim(snapshot, anchor_sha256, answer_sha256, query_ref):
    return digest({'snapshot_sha256': snapshot, 'anchor_sha256': anchor_sha256, 'answer_sha256': answer_sha256, 'query_ref': query_ref})


class SkillRuntimeAdapter(SourceRuntimeAdapter):
    async def _context(self, request):
        plan, _, _, _, events = await approved_plan(self.receipts, request)
        worker = await self.receipts.resolve(plan.worker_ref, kind='worker', events=events)
        descriptor = await runtime_by_id(self.db, request.tenant_id, worker.claims['runtime_id'])
        if descriptor['principal_id'] != worker.signer_id:
            raise Held('WORKER_RUNTIME_SIGNER_MISMATCH')
        return plan, descriptor, {'job_kind': JOB_KIND}

    async def _custody(self, tenant):
        custody = await latest(self.db, tenant, 'custody_descriptor', 'default')
        if custody is None:
            raise Held('CUSTODY_DESCRIPTOR_UNRESOLVED')
        return custody['payload']['record']

    async def submit(self, request, operation_key, fence, authority):
        raise Held('DELIVERY_PACKET_REQUIRED')

    async def deliver(self, packet):
        request = packet.request
        plan, descriptor, order = await self._context(request)
        custody = await self._custody(request.tenant_id)
        corpus = await corpus_object(self.db, request.tenant_id, request.input_refs[0])
        offer = offered(request.digest())
        control = {**self._base(request, order, packet.operation_key, packet.fence, 'skill_submit'), 'corpus': corpus,
                   'terms': offer['terms'], 'intent_receipt_ref': offer['intent_receipt_ref'],
                   'artifact_ref': f'akki://artifact/{request.tenant_id}/{request.request_id}/grounded-units',
                   'object_key': f"{custody['prefix'].strip('/')}/{request.request_id}/{packet.operation_key}/grounded-units.jsonl",
                   'parent_refs': list(request.input_refs), 'principal_id': request.principal_id,
                   'secrets': {'object_store': object_store_secrets(request.tenant_id, custody)}}
        value = await remote.call_async(descriptor, control, deadline_seconds=CALL_SECONDS)
        return await self._observe(request, descriptor, value)

    async def status(self, request, operation_key, fence):
        plan, descriptor, order = await self._context(request)
        value = await remote.call_async(descriptor, self._base(request, order, operation_key, fence, 'status'), deadline_seconds=CALL_SECONDS)
        return await self._observe(request, descriptor, value)

    async def cancel(self, request, operation_key, fence):
        plan, descriptor, order = await self._context(request)
        value = await remote.call_async(descriptor, self._base(request, order, operation_key, fence, 'cancel'), deadline_seconds=CALL_SECONDS)
        return await self._observe(request, descriptor, value)

    async def _observe(self, request, descriptor, value):
        result = await super()._observe(request, descriptor, value)
        if value.get('state') == 'complete' and value.get('artifacts') and value.get('object'):
            await self._ground(request, descriptor, value)
        return result

    async def _ground(self, request, descriptor, value):
        """Anchors on the independent runtime, then the worker's grounding receipt; idempotent per request."""
        events = await self.receipts.events()
        if proofs.observations(events, 'skill_response', request):
            return
        plan, _, _, _, _ = await approved_plan(self.receipts, request)
        artifact = value['artifacts'][0]
        query_ref = request.input_refs[-1]
        corpus = await corpus_object(self.db, request.tenant_id, request.input_refs[0])
        snapshot = snapshot_sha256(corpus)
        if snapshot not in plan.snapshot_hashes:
            raise Held('SKILL_SNAPSHOT_NOT_IN_PLAN')
        inspector, _ = await select(self.db, request.tenant_id, 'inspector', request.kind, (), exclude=(descriptor['runtime_id'],))
        if inspector['principal_id'] == descriptor['principal_id']:
            raise Held('INDEPENDENT_INSPECTOR_REQUIRED')
        wanted = list((value.get('retrieval') or {}).get('anchor_sha256s') or [])
        if not wanted:
            raise Held('SKILL_ANCHORS_UNAVAILABLE')
        by_claim = {e['payload']['receipt']['claims']['claim_sha256']: e['row']['hash']
                    for e in proofs.observations(events, 'anchor', request) if e['payload']['receipt']['signer_id'] != descriptor['principal_id']}
        missing = [a for a in wanted if anchor_claim(snapshot, a, artifact['sha256'], query_ref) not in by_claim]
        if missing:
            custody = await self._custody(request.tenant_id)
            control = {'mode': 'anchor', 'tenant_id': request.tenant_id, 'request_sha256': request.digest(),
                       'operation_key': value['operation_key'], 'fence': 0, 'scope_refs': list(request.scope_refs),
                       'corpus': {'key': corpus['key'], 'sha256': corpus['sha256']},
                       'answer': {'key': value['object']['key'], 'sha256': artifact['sha256']},
                       'anchor_sha256s': missing, 'snapshot_sha256': snapshot, 'query_ref': query_ref,
                       'secrets': {'object_store': object_store_secrets(request.tenant_id, custody)}}
            attested = await remote.call_async(inspector, control, deadline_seconds=CALL_SECONDS)
            if not attested.get('verified') or not attested.get('answer_subset_of_corpus'):
                raise Held('SKILL_ANCHOR_ATTESTATION_FAILED')
            for item in attested['receipts']:
                receipt = signing.runtime_receipt(item['receipt'])
                by_claim[receipt.claims['claim_sha256']] = await self.receipts.record(receipt)
        anchors = [{'snapshot_sha256': snapshot, 'anchor_sha256': a,
                    'source_receipt_ref': by_claim[anchor_claim(snapshot, a, artifact['sha256'], query_ref)]} for a in wanted]
        control = {**self._base(request, {'job_kind': JOB_KIND}, value['operation_key'], value['fence'], 'skill_response'),
                   'query_ref': query_ref, 'anchors': anchors}
        response = await remote.call_async(descriptor, control, deadline_seconds=CALL_SECONDS)
        if response.get('status') != 'complete':
            raise Held('SKILL_RESPONSE_REFUSED')
        await self.receipts.record(signing.runtime_receipt(response['receipt']))


def build_skill_adapter(db, receipts):
    adapter = SkillRuntimeAdapter(db, receipts)
    return BoundedEngineAdapter(kind='skill', engine='solva', submit_rpc=adapter.submit, status_rpc=adapter.status,
                                cancel_rpc=adapter.cancel, timeout_seconds=float(CALL_SECONDS * 4 + 30),
                                admit_limits_rpc=adapter.admit_limits, delivery_rpc=adapter.deliver)
