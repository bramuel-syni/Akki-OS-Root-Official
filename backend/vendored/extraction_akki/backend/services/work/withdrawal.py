"""Withdrawal and isolation (M5-T5). A source right is withdrawn by a signed revocation from the estate's rights
authority (key in estate custody) recorded on the one ledger; the spine then stops serving the artefact by
construction (`_active_rights`). Dependents — session turns, tasks and documents that cite units of that artefact —
are found and marked stale so they cannot be reused as if the right still stood. Eviction is not evidence deletion:
records stay, answers are re-derived only under valid rights (a fresh ask routes fresh or refused)."""
from fastapi import HTTPException

from services.activation.receipts import RESOURCE as RECEIPTS
from services.chat import sessions, spine
from services.estate_admission import signing
from services.estate_admission.ceremony import receipts_for
from services.estate_admission.records import latest
from services.ledger_writer.principal_control import read_events
from services.northena.execution_models import Held
from services.work import documents, records, tasks

REASON = 'SOURCE_RIGHT_WITHDRAWN'
YEAR = 365 * 86400


def _cites(refs, artefact_refs_by_request):
    return sorted({artefact_refs_by_request[r.split('/')[-2]] for r in refs if r.split('/')[-2] in artefact_refs_by_request})


async def dependents(db, scope, artifact_ref):
    """Everything in this estate that leans on the artefact: turns (by cited/selected units), tasks and documents (by source)."""
    request_id = artifact_ref.split('/')[-2]
    by_request = {request_id: artifact_ref}
    turns = []
    estate_wide = records.is_operator(scope)
    for session in await sessions.tenant_sessions(scope['tenant_id']):
        if not estate_wide and session['principal_id'] != scope['principal_id']:
            continue
        for turn in session.get('turns', []):
            ev = turn.get('evidence') or {}
            refs = list(ev.get('cited_refs') or []) or list((ev.get('window') or {}).get('selected_refs') or [])
            if _cites(refs, by_request):
                turns.append({'session_id': session['session_id'], 'turn_id': turn['turn_id'], 'principal_id': session['principal_id'],
                              'question': turn['question'] if session['principal_id'] == scope['principal_id'] else None, 'stale': turn.get('stale_rights')})
    task_rows = [t for t in await tasks.listing(db, scope) if any(s.get('artifact_ref') == artifact_ref for s in t['sources'])]
    doc_rows = [d for d in await documents.listing(db, scope) if any(s.get('artifact_ref') == artifact_ref for s in d['versions'][-1]['sources'])]
    return {'artifact_ref': artifact_ref, 'turns': turns, 'tasks': [{'task_id': t['task_id'], 'title': t['title'], 'stale': t['stale']} for t in task_rows],
            'documents': [{'doc_id': d['doc_id'], 'title': d['title'], 'version': d['version'], 'stale': d['stale']} for d in doc_rows]}


async def withdraw(db, scope, artifact_ref, reason_code=REASON):
    """Highest bar: master_admin signs through the estate's rights authority; nothing is deleted, everything dependent is marked."""
    if 'master_admin' not in scope['roles']:
        raise HTTPException(403, 'Withdrawing a source right needs the estate master administrator.')
    events = await read_events(db, {'row.tenant_id': scope['tenant_id'], 'row.resource_type': RECEIPTS})
    rights_ref = spine._active_rights(events).get(artifact_ref)
    if rights_ref is None:
        raise HTTPException(409, 'No current right names that artefact; nothing to withdraw.')
    anchor = await latest(db, scope['tenant_id'], 'rights_anchor', 'default')
    if anchor is None:
        raise Held('RIGHTS_ANCHOR_UNRESOLVED')
    receipts = receipts_for(db)
    authority = await receipts.resolve(anchor['payload']['record']['anchor_ref'], kind='observation', events=events)
    if not signing.has_key(scope['tenant_id'], authority.key_id):
        raise Held('RIGHTS_AUTHORITY_KEY_NOT_IN_CUSTODY')
    revocation = signing.sign_receipt(scope['tenant_id'], authority.signer_id, authority.key_id, 'revocation',
                                      {'target_ref': rights_ref, 'reason_code': reason_code}, scope_refs=authority.scope_refs, ttl_seconds=YEAR)
    revocation_ref = await receipts.record(revocation)
    found = await dependents(db, scope, artifact_ref)
    for t in found['turns']:
        await sessions.mark_turn_stale(scope['tenant_id'], t['session_id'], t['turn_id'], {'reason_code': reason_code, 'artifact_ref': artifact_ref, 'revocation_ref': revocation_ref, 'at': records.now()})
    for t in found['tasks']:
        await tasks.mark_stale(db, scope, await tasks.load(db, scope, t['task_id']), reason_code=reason_code, artifact_refs=[artifact_ref], revocation_ref=revocation_ref)
    for d in found['documents']:
        await documents.mark_stale(db, scope, await documents.load(db, scope, d['doc_id']), reason_code=reason_code, artifact_refs=[artifact_ref], revocation_ref=revocation_ref)
    return {'status': 'withdrawn', 'artifact_ref': artifact_ref, 'rights_receipt_ref': rights_ref, 'revocation_ref': revocation_ref, 'dependents': found}
