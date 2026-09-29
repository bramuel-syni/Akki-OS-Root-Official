"""One dispatch, bounded reconciliation, current rights; no source-byte transport."""
import asyncio
import json
from services.custody_delivery import ledger
from services.custody_delivery.models import DeliveryDescriptor, DeliveryView
from services.custody_delivery.ports import ProviderState, CustodyBinding
from services.custody_delivery.evidence import check, historical_grant
from services.northena.execution_models import Artifact, Held
from services.ledger_writer.principal_control import CommandConflict
from services.ledger_writer.mongo_control import digest


class CustodyDelivery:
    def __init__(self, binding, coordinator):
        if not isinstance(binding, CustodyBinding):
            raise Held('CUSTODY_PROVIDER_UNBOUND')
        self.binding, self.coordinator, self.db = binding, coordinator, binding.receipts.db

    async def current(self, request, artifact_ref):
        view = await self.coordinator.retrieve(request)
        if not view.execution_verified or artifact_ref not in view.artifact_refs:
            raise Held('CUSTODY_RESULT_NOT_CURRENTLY_ADMITTED')
        authority = await self.coordinator.authority.authorize(request, 'retrieve')
        rows = await self.coordinator.journal.read(request)
        registry = next((r for r in rows if r['slot'] == 'registry'), None)
        if registry is None or registry['data'].get('evidence_mode') != 'measured':
            raise Held('CUSTODY_REGISTRY_NOT_VERIFIED')
        matches = [a for a in registry['data']['artifacts'] if a['ref'] == artifact_ref]
        if len(matches) != 1:
            raise Held('CUSTODY_ARTIFACT_NOT_REGISTERED')
        return Artifact.model_validate_json(json.dumps(matches[0])), registry['hash'], authority

    async def prepare(self, request, body):
        artifact, registry_ref, authority = await self.current(request, body.artifact_ref)
        descriptor = DeliveryDescriptor(delivery_id=digest({'request': request.digest(), 'key': body.idempotency_key}),
            request_id=request.request_id, request_sha256=request.digest(), tenant_id=request.tenant_id,
            principal_id=request.principal_id, scope_refs=request.scope_refs, artifact=artifact, registry_receipt_ref=registry_ref)
        await ledger.create(self.db, descriptor)
        first = await ledger.claim(self.db, descriptor)
        return await self.reconcile(request, descriptor, authority, issue=first, reveal_url=True)

    async def status(self, request, delivery_id):
        descriptor, _ = await ledger.load(self.db, delivery_id, request.request_id)
        artifact, registry_ref, authority = await self.current(request, descriptor.artifact.ref)
        if artifact != descriptor.artifact or registry_ref != descriptor.registry_receipt_ref:
            raise Held('CUSTODY_REGISTERED_ARTIFACT_CHANGED')
        return await self.reconcile(request, descriptor, authority, issue=False, reveal_url=False)

    async def reconcile(self, request, descriptor, authority, *, issue, reveal_url):
        recorded = await ledger.rows(self.db, descriptor.delivery_id)
        slots = {e['payload']['slot']: e for e in recorded}
        grant, grant_ref = None, None
        grant_expired = False
        if 'grant' in slots:
            grant_ref = slots['grant']['payload']['data']['receipt_ref']
        if 'completed' in slots:
            ref = slots['completed']['payload']['data']['receipt_ref']
            completed = await self.binding.receipts.resolve(ref, kind='observation', request_sha256=request.digest())
            grant = await historical_grant(self.binding, descriptor, grant_ref, completed)
            await check(self.binding, descriptor, completed, stage='completed', authority=authority, grant=grant, grant_ref=grant_ref)
            return self.view(descriptor, 'completed', grant_ref, grant, completion=ref)
        if grant_ref is not None:
            try:
                grant = await self.binding.receipts.resolve(grant_ref, kind='observation', request_sha256=request.digest())
            except Held as exc:
                if exc.reason_code != 'SIGNER_OR_RECEIPT_NOT_CURRENT':
                    raise
                grant_expired = True
        method = self.binding.provider.prepare if issue else self.binding.provider.status
        try:
            state = await asyncio.wait_for(method(descriptor, authority), self.binding.timeout_seconds)
        except (TimeoutError, ConnectionError, OSError):
            await ledger.append(self.db, descriptor, 'uncertain', {'reason_code': 'CUSTODY_PROVIDER_OUTCOME_UNCERTAIN'})
            return self.view(descriptor, 'uncertain', grant_ref, grant)
        except Held:
            raise  # the admitted custodian's own classified hold is a verdict, not an invalid response
        except Exception:
            raise Held('CUSTODY_PROVIDER_RESPONSE_INVALID') from None
        if not isinstance(state, ProviderState):
            raise Held('CUSTODY_PROVIDER_RESPONSE_INVALID')
        state = ProviderState.model_validate(state.model_dump(mode='python'))
        if state.grant is not None:
            if grant_expired and state.completion is not None:
                # Existing grant only: a status provider cannot turn an expired
                # response into a new URL or a different permission.
                recovered = await historical_grant(self.binding, descriptor, grant_ref, state.completion)
                if recovered != state.grant:
                    raise Held('CUSTODY_GRANT_CHANGED')
                grant = recovered
                state = state.model_copy(update={'grant': None, 'url': None})
        if state.grant is not None:
            checked = await check(self.binding, descriptor, state.grant, stage='grant', authority=authority, url=state.url)
            fresh_ref = await self.binding.receipts.record(checked)
            if grant_ref is not None and fresh_ref != grant_ref:
                raise Held('CUSTODY_GRANT_CHANGED')
            try:
                await ledger.append(self.db, descriptor, 'grant', {'receipt_ref': fresh_ref})
            except CommandConflict:
                raise Held('CUSTODY_GRANT_CHANGED') from None
            grant, grant_ref = checked, fresh_ref
        elif state.url is not None:
            raise Held('CUSTODY_UNSIGNED_CAPABILITY')
        if state.completion is not None:
            if grant is None and grant_ref is not None:
                grant = await historical_grant(self.binding, descriptor, grant_ref, state.completion)
            completed = await check(self.binding, descriptor, state.completion, stage='completed', authority=authority, grant=grant, grant_ref=grant_ref)
            ref = await self.binding.receipts.record(completed)
            try:
                await ledger.append(self.db, descriptor, 'completed', {'receipt_ref': ref})
            except CommandConflict:
                raise Held('CUSTODY_COMPLETION_CONFLICT') from None
            await self.current(request, descriptor.artifact.ref)
            return self.view(descriptor, 'completed', grant_ref, grant, completion=ref)
        current_artifact, current_registry, current_authority = await self.current(request, descriptor.artifact.ref)
        if current_artifact != descriptor.artifact or current_registry != descriptor.registry_receipt_ref:
            raise Held('CUSTODY_REGISTERED_ARTIFACT_CHANGED')
        if grant is not None and state.url is not None and reveal_url:
            await check(self.binding, descriptor, grant, stage='grant', authority=current_authority, url=state.url)
        return self.view(descriptor, 'expired' if grant_expired else 'offered' if grant else 'pending', grant_ref, grant,
                         url=state.url if reveal_url else None)

    @staticmethod
    def view(descriptor, state, ref=None, grant=None, *, completion=None, url=None):
        return DeliveryView(delivery_id=descriptor.delivery_id, request_id=descriptor.request_id, state=state,
            receipt_ref=ref, completion_receipt_ref=completion, artifact_ref=descriptor.artifact.ref,
            artifact_sha256=descriptor.artifact.sha256, artifact_size_bytes=descriptor.artifact.size_bytes,
            expires_epoch=grant.expires_epoch if grant else None, url=url, delivery_verified=completion is not None)