"""Shared signed-proof joins; no caller verdict, synthetic provider or key factory."""
import json
from services.activation.receipts import RESOURCE
from services.ledger_writer.mongo_control import digest
from services.northena.execution_models import Held


def observations(events, category, request=None):
    return [e for e in events if e['row']['resource_type'] == RESOURCE
            and e['payload'].get('receipt', {}).get('kind') == 'observation'
            and e['payload']['receipt'].get('claims', {}).get('category') == category
            and (request is None or e['payload']['receipt'].get('request_sha256') == request.digest())]


async def resolve(receipts, request, events, ref, category, *, request_bound=True):
    from services.activation.native_evidence import Observation
    receipt = await receipts.resolve(ref, kind='observation', events=events,
                                     request_sha256=request.digest() if request_bound else None)
    proof = Observation.model_validate_json(json.dumps(receipt.claims))
    if (proof.category != category or proof.evidence_mode != 'measured'
            or not set(request.scope_refs) <= set(receipt.scope_refs)
            or request_bound and proof.context_sha256 != request.digest()):
        raise Held('GOVERNANCE_PROOF_BINDING_INVALID')
    return receipt, proof


async def one(receipts, request, events, category, field):
    candidates = observations(events, category, request)
    if len(candidates) != 1:
        raise Held(category.upper() + '_PROOF_REQUIRED')
    ref = candidates[0]['row']['hash']
    receipt, proof = await resolve(receipts, request, events, ref, category)
    value = getattr(proof, field)
    if value is None or proof.claim_sha256 != digest(value.model_dump(mode='json')):
        raise Held('GOVERNANCE_CLAIM_MISMATCH')
    return ref, receipt, value


async def unchanged(receipts, events):
    latest = await receipts.events()
    if [e['row']['hash'] for e in latest] != [e['row']['hash'] for e in events]:
        raise Held('GOVERNANCE_EVIDENCE_PREFIX_CHANGED')


def precedes(events, *refs):
    positions = {e['row']['hash']: e['row']['seq'] for e in events}
    try:
        order = [positions[ref] for ref in refs]
    except KeyError:
        raise Held('GOVERNANCE_CHRONOLOGY_UNRESOLVED') from None
    if any(a >= b for a, b in zip(order, order[1:])):
        raise Held('GOVERNANCE_CHRONOLOGY_INVALID')