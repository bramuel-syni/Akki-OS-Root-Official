"""Native grounding/refusal metadata only; the answer stays in admitted custody."""
import json
from services.activation.approvals import approved_plan
from services.activation.receipts import RESOURCE
from services.activation.native_evidence import Observation
from services.northena.execution_models import Held, Artifact
from services.ledger_writer.mongo_control import digest
from services.transform_forms.callable_skill_gate import ensure_response_carries_class, BelowFloorError


async def refusal(receipts, request, intent):
    plan, _, _, _, events = await approved_plan(receipts, request)
    matching = [e for e in events if e['row']['resource_type'] == RESOURCE
                and e['payload'].get('receipt', {}).get('request_sha256') == request.digest()
                and e['payload']['receipt'].get('claims', {}).get('category') == 'refusal'
                and e['payload']['receipt']['claims'].get('context_sha256') == request.digest()]
    if not matching:
        return None
    if len(matching) != 1:
        raise Held('SKILL_REFUSAL_AMBIGUOUS')
    ref = matching[0]['row']['hash']
    receipt = await receipts.resolve(ref, kind='observation', request_sha256=request.digest(), events=events)
    proof = Observation.model_validate_json(json.dumps(receipt.claims))
    worker = await receipts.resolve(plan.worker_ref, kind='worker', events=events)
    if (proof.evidence_mode != 'measured' or proof.refusal is None or proof.refusal.request_ref != intent['row']['hash']
            or receipt.signer_id != worker.signer_id
            or proof.refusal.reason_code != 'OUT_OF_SCOPE' or proof.claim_sha256 != digest(proof.refusal.model_dump(mode='json'))
            or not set(request.scope_refs) <= set(receipt.scope_refs)):
        raise Held('SKILL_REFUSAL_NOT_PROVED')
    return {'outcome': 'refused', 'reason_code': 'OUT_OF_SCOPE', 'receipt_ref': ref,
            'execution_verified': False, 'refusal_verified': True, 'delivery_verified': False}


async def grounding(runtime, coordinator, request):
    plan, _, _, _, events = await approved_plan(runtime.receipts, request)
    rows = await coordinator.journal.read(request)
    registry = next((r for r in rows if r['slot'] == 'registry'), None)
    if registry is None or registry['data'].get('evidence_mode') != 'measured':
        raise Held('SKILL_ANSWER_REGISTRY_UNVERIFIED')
    candidates = [e for e in events if e['row']['resource_type'] == RESOURCE
                  and e['payload'].get('receipt', {}).get('request_sha256') == request.digest()
                  and e['payload']['receipt'].get('claims', {}).get('category') == 'skill_response']
    if len(candidates) != 1:
        raise Held('SKILL_GROUNDING_RECEIPT_REQUIRED')
    ref = candidates[0]['row']['hash']
    receipt = await runtime.receipts.resolve(ref, kind='observation', request_sha256=request.digest(), events=events)
    proof = Observation.model_validate_json(json.dumps(receipt.claims))
    worker = await runtime.receipts.resolve(plan.worker_ref, kind='worker', events=events)
    ground = proof.grounding
    if (receipt.signer_id != worker.signer_id or proof.evidence_mode != 'measured'
            or not set(request.scope_refs) <= set(receipt.scope_refs)
            or proof.context_sha256 != request.digest() or ground is None or not ground.anchors
            or ground.query_ref != request.input_refs[-1] or ground.context_lost and not ground.context_loss_disclosed):
        raise Held('SKILL_GROUNDING_BINDING_MISMATCH')
    if len({a.anchor_sha256 for a in ground.anchors}) != len(ground.anchors):
        raise Held('SKILL_INDEPENDENT_ANCHOR_NOT_PROVED')
    matches = [a for a in registry['data']['artifacts'] if a['sha256'] == ground.answer_sha256]
    if len(matches) != 1:
        raise Held('SKILL_ANSWER_ARTIFACT_MISMATCH')
    artifact = Artifact.model_validate_json(json.dumps(matches[0]))
    if (artifact.tenant_id != request.tenant_id or proof.claim_sha256 != digest({
            'request_sha256': request.digest(), 'artifact': artifact.model_dump(mode='json'),
            'grounding': ground.model_dump(mode='json')})):
        raise Held('SKILL_ANSWER_CLASS_OR_HASH_MISMATCH')
    for anchor in ground.anchors:
        source = await runtime.receipts.resolve(anchor.source_receipt_ref, kind='observation', request_sha256=request.digest(), events=events)
        anchored = Observation.model_validate_json(json.dumps(source.claims))
        if (source.signer_id == worker.signer_id or not set(request.scope_refs) <= set(source.scope_refs)
                or anchored.category != 'anchor' or anchored.evidence_mode != 'measured'
                or anchor.snapshot_sha256 not in plan.snapshot_hashes
                or anchored.claim_sha256 != digest({'snapshot_sha256': anchor.snapshot_sha256,
                    'anchor_sha256': anchor.anchor_sha256, 'answer_sha256': ground.answer_sha256, 'query_ref': ground.query_ref})):
            raise Held('SKILL_INDEPENDENT_ANCHOR_NOT_PROVED')
    try:
        return ensure_response_carries_class({'outcome': 'ready', 'reason_code': 'GROUNDED_SKILL_RESULT_VERIFIED',
            'artifact_refs': [artifact.ref], 'grounding_receipt_ref': ref, 'anchor_count': len(ground.anchors),
            'context_loss_disclosed': ground.context_loss_disclosed, 'execution_verified': True,
            'delivery_verified': False}, class_label=artifact.class_label, floor=request.result_floor)
    except BelowFloorError:
        raise Held('SKILL_RESPONSE_BELOW_FLOOR') from None