"""Independent artifact inspection on a separately controlled admitted runtime."""
from datetime import datetime, timezone
from contracts.asset_registry import AssetClass, AssetRegistryRecord, CustodyClass, NamedOwner
from contracts.mtafiti_registry import FreshnessStamp
from services.activation.approvals import approved_plan
from services.estate_admission import signing
from services.estate_admission.records import latest
from services.estate_admission.runtimes import select
from services.extraction_runtime import derived_rights, objects, remote
from services.extraction_runtime.adapter import CALL_SECONDS, object_store_secrets
from services.mtafiti.execution_record_models import InspectionEntry, InspectorReceipt
from services.northena.execution_models import Held
from services.portal_operational.entitlements import read_view


class IndependentInspector:
    def __init__(self, db, receipts):
        self.db, self.receipts = db, receipts

    async def _existing(self, request, events, expected, runtime_id):
        """A recorded, verified independence receipt for the same artifact facts is reused, not repeated."""
        from services.non_gpu_governance.proofs import observations
        from services.ledger_writer.mongo_control import digest
        claim = digest({'artifacts': expected, 'inspector_runtime_id': runtime_id, 'verified': True})
        for event in observations(events, 'independence', request):
            if event['payload']['receipt']['claims'].get('claim_sha256') == claim:
                await self.receipts.resolve(event['row']['hash'], kind='observation', request_sha256=request.digest(), events=events)
                return event['row']['hash']
        return None

    async def inspect(self, request, result, operation_key):
        sealed = await objects.lookup(self.db, request)
        if sealed is None or not sealed.get('object'):
            raise Held('SEALED_OBJECT_UNRESOLVED')
        plan, _, _, _, events = await approved_plan(self.receipts, request)
        worker = await self.receipts.resolve(plan.worker_ref, kind='worker', events=events)
        descriptor, basis = await select(self.db, request.tenant_id, 'inspector', request.kind, (),
                                         exclude=(worker.claims['runtime_id'],))
        if descriptor['principal_id'] == worker.signer_id:
            raise Held('INDEPENDENT_INSPECTOR_REQUIRED')
        expected = [{'ref': a.ref, 'sha256': a.sha256, 'size_bytes': a.size_bytes} for a in result.artifacts]
        ref = await self._existing(request, events, expected, descriptor['runtime_id'])
        if ref is None:
            custody = await latest(self.db, request.tenant_id, 'custody_descriptor', 'default')
            control = {'mode': 'inspect', 'tenant_id': request.tenant_id, 'request_sha256': request.digest(),
                       'operation_key': operation_key, 'fence': 0, 'scope_refs': list(request.scope_refs),
                       'artifacts': [{**e, 'bucket': sealed['object']['bucket'], 'key': sealed['object']['key']} for e in expected],
                       'secrets': {'object_store': object_store_secrets(request.tenant_id, custody['payload']['record'])}}
            value = await remote.call_async(descriptor, control, deadline_seconds=CALL_SECONDS)
            ref = await self.receipts.record(signing.runtime_receipt(value['receipt']))
            if not value.get('verified'):
                raise Held('ARTIFACT_INDEPENDENT_VERIFICATION_FAILED')
        # Independence established: the source grant now follows the worker-signed lineage to this artefact.
        await derived_rights.extend(self.db, self.receipts, request, result.artifacts, events)
        view = await read_view(self.db, {'tenant_id': request.tenant_id, 'principal_id': request.principal_id})
        owner = NamedOwner(owner_id=view.licence.organisation_principal_id, owner_class='organisation',
                           mandate_source=view.licence.terms_identifier)
        # Freshness is the recorded inspection time: a re-verification restates the same registration.
        observed = await self.receipts.resolve(ref, kind='observation')
        stamp = FreshnessStamp(logged_date=datetime.fromtimestamp(observed.issued_epoch, timezone.utc).isoformat(),
                               structural_signature=None)
        entries = tuple(InspectionEntry(artifact=a, record=AssetRegistryRecord(asset_ref=a.ref, asset_class=AssetClass.ARTIFACT,
                        named_owner=owner, custody_class=CustodyClass.SENSITIVE, freshness_stamp=stamp))
                        for a in result.artifacts)
        return InspectorReceipt(request_sha256=request.digest(), operation_key=operation_key,
                                worker_receipt_ref=result.receipt_ref, inspection_ref='inspection:' + ref,
                                evidence_mode='measured', entries=entries)
