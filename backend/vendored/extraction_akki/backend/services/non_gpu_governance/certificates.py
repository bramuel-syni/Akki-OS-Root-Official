"""Live certificate consumer includes the same current non-GPU release gates.

The original v1 verifier remains available for historical/LAB contract validation;
application startup and the issuance endpoint use this stricter live composition.
"""
import json
from services.activation.native_evidence import NativeEvidence
from services.non_gpu_governance.gate import NativeGovernance
from services.northena.execution_journal import LedgerJournal
from services.northena.execution_models import Request, Held


class GovernedNativeEvidence(NativeEvidence):
    async def verify(self, document, *, tenant_id, principal_id):
        verdict = await super().verify(document, tenant_id=tenant_id, principal_id=principal_id)
        events = await self.receipts.events()
        candidates = [e for e in events if e['row']['resource_type'] == 'execution_flow'
                      and e['row']['run_id'] == document['identity']['frozen_request_id']
                      and e['payload'].get('slot') == 'request'
                      and e['payload'].get('principal_id') == principal_id]
        if len(candidates) != 1:
            raise Held('CERTIFICATE_NATIVE_REQUEST_UNRESOLVED')
        request = Request.model_validate_json(json.dumps(candidates[0]['payload']['data']['request']))
        await NativeGovernance(self.receipts, LedgerJournal(self.receipts.db)).check(request, 'certificate')
        return verdict