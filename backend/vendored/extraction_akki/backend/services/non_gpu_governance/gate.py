"""Native-only DQ/context/lineage gates at reserve, send, publish and retrieve.

The owning estate supplies signed measured metadata through the existing receipt
API. Missing records hold. Neither admission nor any data-plane effect is minted.
"""
import json
from services.activation.approvals import approved_plan
from services.non_gpu_governance import proofs
from services.non_gpu_governance.rights import RightsGate
from services.ledger_writer.mongo_control import digest
from services.northena.execution_models import Artifact, Held


class NativeGovernance:
    def __init__(self, receipts, journal):
        self.receipts, self.journal = receipts, journal
        self.rights = RightsGate(receipts)

    async def check(self, request, phase):
        try:
            await self._check(request, phase)
        except (ValueError, TypeError, KeyError):
            raise Held('GOVERNANCE_METADATA_INVALID') from None

    async def _check(self, request, phase):
        plan, _, _, _, events = await approved_plan(self.receipts, request)
        rows = await self.journal.read(request)
        registry = next((r for r in rows if r['slot'] == 'registry'), None)
        artifacts = tuple(Artifact.model_validate_json(json.dumps(a))
                          for a in registry['data']['artifacts']) if registry else ()
        refs = request.input_refs + tuple(a.ref for a in artifacts)
        reachable = await self.rights.check(request, refs, events, artifacts=artifacts)
        if request.kind != 'source':
            quality_ref, _, quality = await proofs.one(self.receipts, request, events,
                                                       'quality_register', 'quality_register')
            if (quality.snapshot_sha256 not in plan.snapshot_hashes
                    or quality.pack.version != plan.policy_versions['cleanliness_pack']
                    or not set(quality.population_refs) <= reachable):
                raise Held('QUALITY_PLAN_BINDING_MISMATCH')
            _, policy = await proofs.resolve(self.receipts, request, events,
                quality.policy_receipt_ref, 'quality_policy', request_bound=False)
            if policy.quality_pack != quality.pack or policy.claim_sha256 != digest(quality.pack.model_dump(mode='json')):
                raise Held('QUALITY_POLICY_NOT_CONFIRMED')
            _, population = await proofs.resolve(self.receipts, request, events,
                quality.population_receipt_ref, 'quality_population')
            if population.claim_sha256 != digest({'snapshot_sha256': quality.snapshot_sha256,
                                                  'population_refs': list(quality.population_refs)}):
                raise Held('QUALITY_POPULATION_MISMATCH')
            proofs.precedes(events, quality.policy_receipt_ref, quality.population_receipt_ref, quality_ref)
            await self.rights.check(request, quality.population_refs, events)
            if request.kind == 'skill':
                await self.context(request, events, quality_ref, quality)
            elif any(r.stratum not in {'Clean', 'Repairable'} for r in quality.records):
                raise Held('TRAINING_QUALITY_NOT_ELIGIBLE')
        await proofs.unchanged(self.receipts, events)

    async def context(self, request, events, quality_ref, quality):
        window_ref, _, window = await proofs.one(self.receipts, request, events, 'context_window', 'context_window')
        proofs.precedes(events, quality_ref, window_ref)
        proofs.precedes(events, window.ranking_rule_ref, window_ref)
        if window.objective_sha256 != request.objective_sha256 or window.qualified_set_receipt_ref != quality_ref:
            raise Held('CONTEXT_QUALITY_OR_OBJECTIVE_MISMATCH')
        _, policy = await proofs.resolve(self.receipts, request, events, window.ranking_rule_ref,
                                          'context_policy', request_bound=False)
        committed = window.model_dump(mode='json', include={'frame_ref', 'model_sha256', 'tokenizer_sha256',
            'load_bearing_refs', 'window_tokens', 'reserved_tokens'})
        if policy.claim_sha256 != digest(committed):
            raise Held('CONTEXT_POLICY_MISMATCH')
        records = {r.unit_ref: r for r in quality.records}
        qualified = {r.unit_ref for r in quality.records if r.stratum != 'Junk'}
        if qualified != {u.unit_ref for u in window.units}:
            if any(records.get(u.unit_ref) and records[u.unit_ref].stratum == 'Junk' for u in window.units):
                raise Held('CONTEXT_QUALITY_CLASS_VIOLATION')
            raise Held('CONTEXT_QUALIFIED_POPULATION_MISMATCH')
        for unit in window.units:
            record = records[unit.unit_ref]
            if unit.content_sha256 != record.content_sha256:
                raise Held('CONTEXT_CONTENT_HASH_MISMATCH')
            if unit.unit_ref not in window.selected_refs:
                continue
            if record.stratum == 'Junk' or record.stratum == 'Suspect' and unit.class_label == 'fact':
                raise Held('CONTEXT_QUALITY_CLASS_VIOLATION')
            if unit.memory_receipt_ref:
                await self.memory(request, events, unit)
        return window

    async def memory(self, request, events, unit):
        _, proof = await proofs.resolve(self.receipts, request, events, unit.memory_receipt_ref,
                                              'memory', request_bound=False)
        memory = proof.memory
        if (memory is None or memory.principal_id != request.principal_id
                or memory.artifact_ref != unit.unit_ref or memory.artifact_sha256 != unit.content_sha256
                or memory.class_label != unit.class_label
                or proof.claim_sha256 != digest(memory.model_dump(mode='json'))):
            raise Held('MEMORY_IDENTITY_OR_CLASS_MISMATCH')
        _, published = await proofs.resolve(self.receipts, request, events, memory.publication_receipt_ref,
                                             'memory_publication', request_bound=False)
        if published.claim_sha256 != digest(memory.model_dump(mode='json', exclude={'publication_receipt_ref'})):
            raise Held('MEMORY_PUBLICATION_MISMATCH')
        index = {e['row']['hash']: e['row']['seq'] for e in events}
        if index[memory.publication_receipt_ref] >= index[unit.memory_receipt_ref]:
            raise Held('MEMORY_PUBLICATION_ORDER_INVALID')
        await proofs.resolve(self.receipts, request, events, memory.retention_policy_ref,
                             'memory_policy', request_bound=False)
        proofs.precedes(events, memory.retention_policy_ref, memory.publication_receipt_ref, unit.memory_receipt_ref)
        graph, identities = await self.rights.graph(request, events)
        if graph.get(memory.artifact_ref) != memory.source_refs:
            raise Held('MEMORY_SOURCE_LINEAGE_MISMATCH')
        if any(identities.get(ref, (None,))[0] != sha for ref, sha in zip(memory.source_refs, memory.source_hashes)):
            raise Held('MEMORY_SOURCE_VERSION_MISMATCH')
        closed = [e for e in events if e['row']['resource_type'] == 'execution_flow'
                  and e['row']['run_id'] == memory.run_id and e['payload'].get('slot') == 'terminal'
                  and e['payload'].get('principal_id') == request.principal_id
                  and e['payload'].get('data', {}).get('phase') in {'ready', 'cancelled', 'failed'}]
        if len(closed) != 1:
            raise Held('MEMORY_CLOSED_RUN_REQUIRED')
        proofs.precedes(events, closed[0]['row']['hash'], memory.publication_receipt_ref)
        await self.rights.check(request, memory.source_refs, events)