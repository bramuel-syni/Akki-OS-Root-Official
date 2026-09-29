"""Rights follow lineage. A sealed artefact whose recorded parents hold current rights receives its own
rights proof from the estate's rights authority (key in estate custody), once per artefact identity,
only after an independent runtime has verified the artefact. Nothing new is granted: the admitted
source grant is extended along the worker-signed lineage; a withdrawn parent holds the extension.
"""
from services.estate_admission import signing
from services.estate_admission.records import latest
from services.ledger_writer.mongo_control import digest
from services.non_gpu_governance import proofs
from services.non_gpu_governance.lineage import Rights
from services.non_gpu_governance.rights import RightsGate
from services.northena.execution_models import Held

REASON = 'RIGHTS_FOLLOW_ADMITTED_LINEAGE'
YEAR = 365 * 86400


def existing(events, unit_ref):
    for event in proofs.observations(events, 'rights'):
        rights = event['payload']['receipt']['claims'].get('rights') or {}
        if rights.get('unit_ref') == unit_ref and rights.get('status') == 'active':
            return event['row']['hash']
    return None


async def extend(db, receipts, request, artifacts, events):
    anchor = await latest(db, request.tenant_id, 'rights_anchor', 'default')
    if anchor is None:
        raise Held('RIGHTS_ANCHOR_UNRESOLVED')
    anchor_ref = anchor['payload']['record']['anchor_ref']
    authority = await receipts.resolve(anchor_ref, kind='observation', events=events)
    if not signing.has_key(request.tenant_id, authority.key_id):
        raise Held('RIGHTS_AUTHORITY_KEY_NOT_IN_CUSTODY')
    gate = RightsGate(receipts)
    graph, identities = await gate.graph(request, events)
    refs = {}
    for artifact in artifacts:
        identity = identities.get(artifact.ref)
        if identity is None or identity[0] != artifact.sha256:
            raise Held('ARTIFACT_LINEAGE_REQUIRED')
        await gate.check(request, graph[artifact.ref], events)
        ref = existing(events, artifact.ref)
        if ref is None:
            rights = Rights(version='akki.rights.metadata/1', unit_ref=artifact.ref, status='active',
                            policy_ref=anchor_ref, reason_code=REASON)
            claim = {'category': 'rights', 'context_sha256': request.digest(), 'evidence_mode': 'measured',
                     'claim_sha256': digest(rights.model_dump(mode='json')), 'rights': rights.model_dump(mode='json')}
            ref = await receipts.record(signing.sign_receipt(request.tenant_id, authority.signer_id, authority.key_id,
                                                             'observation', claim, scope_refs=authority.scope_refs,
                                                             request_sha256=request.digest(), ttl_seconds=YEAR))
        refs[artifact.ref] = ref
    return refs
