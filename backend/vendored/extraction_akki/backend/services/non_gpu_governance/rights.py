"""Transitive current-rights gate over signed native registry lineage."""
import json
from services.non_gpu_governance import proofs
from services.non_gpu_governance.lineage import Lineage, Rights, ancestors, descendants
from services.ledger_writer.mongo_control import digest
from services.northena.execution_models import Held


class RightsGate:
    def __init__(self, receipts):
        self.receipts = receipts

    async def graph(self, request, events):
        graph, hashes = {}, {}
        for event in proofs.observations(events, 'lineage'):
            if not set(request.scope_refs) <= set(event['payload']['receipt']['scope_refs']):
                continue
            claims = event['payload']['receipt']['claims']
            node = Lineage.model_validate_json(json.dumps(claims.get('lineage')))
            ref = event['row']['hash']
            _, proof = await proofs.resolve(self.receipts, request, events, ref, 'lineage', request_bound=False)
            if proof.claim_sha256 != digest(node.model_dump(mode='json')):
                raise Held('LINEAGE_CLAIM_MISMATCH')
            identity = (node.artifact_sha256, node.parents)
            if node.artifact_ref in hashes and hashes[node.artifact_ref] != identity:
                raise Held('LINEAGE_IDENTITY_CONFLICT')
            hashes[node.artifact_ref] = identity
            graph[node.artifact_ref] = node.parents
        return graph, hashes

    async def check(self, request, refs, events, *, artifacts=()):
        graph, hashes = await self.graph(request, events)
        for artifact in artifacts:
            identity = hashes.get(artifact.ref)
            if identity is None or identity[0] != artifact.sha256:
                raise Held('ARTIFACT_LINEAGE_REQUIRED')
        required = ancestors(refs, graph)
        active = set()
        for event in proofs.observations(events, 'rights'):
            rights = Rights.model_validate_json(json.dumps(
                event['payload']['receipt']['claims'].get('rights')))
            if rights.unit_ref not in required:
                continue
            _, proof = await proofs.resolve(self.receipts, request, events, event['row']['hash'],
                                             'rights', request_bound=False)
            if proof.claim_sha256 != digest(rights.model_dump(mode='json')):
                raise Held('RIGHTS_CLAIM_MISMATCH')
            # Immutable source versions cannot be reactivated by a later grant.
            # A replacement must have a new reference and its own accepted lineage.
            if rights.status == 'withdrawn':
                raise Held('DESCENDANT_RIGHTS_WITHDRAWN')
            policy = await self.receipts.resolve(rights.policy_ref, events=events)
            if not set(request.scope_refs) <= set(policy.scope_refs):
                raise Held('RIGHTS_POLICY_SCOPE_MISMATCH')
            proofs.precedes(events, rights.policy_ref, event['row']['hash'])
            active.add(rights.unit_ref)
        if required - active:
            raise Held('NATIVE_RIGHTS_PROOF_REQUIRED')
        return required

    async def affected(self, request, unit_ref):
        events = await self.receipts.events()
        graph, _ = await self.graph(request, events)
        result = descendants(unit_ref, graph)
        await proofs.unchanged(self.receipts, events)
        return result