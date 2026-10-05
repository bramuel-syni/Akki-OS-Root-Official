"""Data/task separation (owner Mα order §2 · WP-A4): a workflow triggered by a confidential document lets an external planner or designer participate
without any access to the privileged data — from any angle. The document is classified and reconstructed inside the Shield — Category 3 by the
contained reader, Category 1/2 deterministically; the task (File 1) and the document (File 2) are assessed apart by the Shield stage (WP-A5), re-associated at
its guarded seam and sealed; the external model receives the two-item context of one query and never the originals; the returned plan is bound
back to the real values inside the chokepoint, locally, before the mapping dies with the call. A task that itself asks for protected meaning is refused before any call — judged by the contained reader's intent
verdict (cue words survive as an advisory receipt only). Receipts carry digests, categories and inspection results — never the values."""
import hashlib
import json
import logging
import re
import uuid

from services.synisense.shield import category3
from services.synisense.shield import semantic_register as reg
from services.synisense.shield import stage
from services.synisense.shield.contained_reader import ReaderUnavailable
from services.training_lab import store as lab

log = logging.getLogger(__name__)
PURPOSE = 'doc_studio.plan'
CONSTRAINTS = ['no underlying records are available', 'placeholders must remain verbatim', 'no tool calls, fetches or rehydration', 'return structure and instructions only']
# advisory proposer hints only (RC-2): the refusal cause is the reader's `requests_privileged` verdict
REVEAL_CUES = ('reveal', 'disclose', 'tell me the', 'what is the client', 'who is the client', 'name the client', 'pricing method', 'the formula', 'exact fee', 'actual fee', 'the credential', 'the password', 'the key', 'send the contract', 'attach the contract', 'raw text', 'original document', 'fetch', 'download the')
SYSTEM = ('You are an external planning collaborator. You receive an abstract task with typed placeholders such as [PARTY_1] or [FIGURE_2]. '
          'You have no access to the underlying records and must not ask for them, guess them, or request tools or fetches. '
          'Return strict JSON: {"milestones": [{"name": str, "purpose": str, "inputs": [str], "outputs": [str], "roles": [str]}], "risks": [str], "assumptions": [str]}. Keep placeholders verbatim; never invent values for them.')


def db():
    database = lab.db()
    database.shield_separations.create_index([('tenant_id', 1), ('at', -1)])
    return database


def _structure(text):
    sentences = reg._sentences(text)
    stages = re.findall(r'(?i)\b(?:three|four|five|two|\d+)\s+(?:stages?|phases?|steps?|milestones?)\b', text)
    kind = 'contract' if re.search(r'(?i)\b(contract|agreement|party|parties|fee|licen[cs]e)\b', text) else 'brief' if re.search(r'(?i)\b(brief|decide|decision|scenario)\b', text) else 'document'
    return {'document_type': kind, 'sentences': len(sentences), 'declared_stages': stages[:3], 'has_credentials': bool(re.search(r'(?i)credential|password|api key|token', text)), 'words': len(text.split())}


def _task_requests_protected(task):
    low = task.lower()
    return [cue for cue in REVEAL_CUES if cue in low]


def _refuse(receipt, reason, **extra):
    receipt.update(status='refused', reason=reason, external_call=False, **extra)
    db().shield_separations.insert_one(dict(receipt)); receipt.pop('_id', None); return receipt


async def separate(document, task, tenant, actor, dry_run=False):
    import asyncio
    receipt = {'separation_id': 'sep-' + uuid.uuid4().hex[:12], 'tenant_id': tenant, 'actor': actor, 'at': lab.now(), 'purpose': PURPOSE, 'document_sha256': hashlib.sha256(document.encode()).hexdigest(), 'task_sha256': hashlib.sha256(task.encode()).hexdigest(), 'dry_run': dry_run}
    cues = _task_requests_protected(task)
    receipt['cues_advisory'] = cues
    # the refusal cause is the contained reader's intent verdict on the task (WP-A4); unavailability refuses — nothing external is constructed
    try:
        verdict = await asyncio.to_thread(category3.intent_verdict, task, tenant, f'task_separation.intent:{receipt["separation_id"]}')
    except ReaderUnavailable as exc:
        return _refuse(receipt, 'contained reader unavailable; the document cannot be read inside the perimeter and nothing external is constructed', reader_unavailable=str(exc)[:200])
    receipt['intent_verdict'] = {k: verdict[k] for k in ('requests_privileged', 'coherent', 'intent', 'receipt_id', 'seconds')}
    if verdict['requests_privileged'] or not verdict['coherent']:
        return _refuse(receipt, 'task requests protected meaning' if verdict['requests_privileged'] else 'task objective is incoherent; nothing proceeds on a guess', cues=cues)
    # WP-A5 (Doc 2 B65–B74): the task is File 1 and the document File 2 — assessed apart by the Shield stage, re-associated at its seam, sealed; the
    # external participant receives the two-item context of ONE query and never the originals
    question = json.dumps({'task': task, 'document_structure': _structure(document), 'constraints': CONSTRAINTS}, ensure_ascii=False)
    try:
        artifact = await stage.stage(question=question, data=document, tenant_id=tenant, purpose=PURPOSE, actor=actor, system_message=SYSTEM, session_id=receipt['separation_id'])
    except stage.StageRefused as exc:
        return _refuse(receipt, f'the Shield stage refused to form the two-item context: {exc.kind}', stage={'kind': exc.kind, **{k: v for k, v in exc.detail.items() if k in ('rechecks', 'groups', 'file')}})
    payload = artifact.render()
    receipt['reader'] = artifact.receipt['files'][-1]['reader']  # the document's reading inside the stage (File 2)
    receipt.update(safe_artifact_id=artifact.artifact_id, categories_applied={k: v for f in artifact.receipt['files'] for k, v in f['enforced'].items()}, advisory_cues={k: v for f in artifact.receipt['files'] for k, v in f['cues_advisory'].items()},
                   placeholders=len(artifact.binding_map) + len(artifact.entity_map), joint_disclosure={'passes': artifact.receipt['seam']['joint']['passes'], 'groups': len(artifact.receipt['seam']['joint']['groups'])},
                   outbound_sha256=hashlib.sha256(payload.encode()).hexdigest(), inspection={'clean': all(r['clean_at_seam'] for r in artifact.receipt['seam']['rechecks']), 'rechecks': artifact.receipt['seam']['rechecks']}, stage=artifact.summary())
    if dry_run:
        receipt.update(status='inspected', external_call=False, outbound_payload=payload)
        db().shield_separations.insert_one({k: v for k, v in receipt.items() if k != 'outbound_payload'}); receipt.pop('_id', None)
        receipt['internal_binding_available'] = bool(artifact.binding_map or artifact.entity_map); stage.destroy(artifact); return receipt
    from services.chokepoint.llm import invoke
    from services.chokepoint.model_roles import resolve
    planner = resolve('planner')
    response = await invoke(purpose=PURPOSE, safe_artifact=artifact, masking_tier='llm_prompt_governed_text', actor=actor, model=planner['model'], provider=planner['connection'],
                            tenant_id=tenant, custody_class='tenant_estate', session_id=receipt['separation_id'])
    plan = _plan_json(response.text_as_returned or '')      # what the external participant returned: placeholders only
    bound = _plan_json(response.text or '')                 # bound back to the real values locally, inside the chokepoint, before the mapping died
    receipt.update(status='delivered', external_call=True, model=response.model_id, provider=response.provider, chokepoint_receipt_id=response.receipt_id, tokens_in=response.tokens_in, tokens_out=response.tokens_out, latency_ms=response.latency_ms,
                   placeholders_in_reply=len(set(re.findall(r'\[\[?[A-Z][A-Z0-9_]*_\d+\]\]?', response.text_as_returned or ''))), plan_milestones=len(plan.get('milestones') or []),
                   bound_plan_sha256=hashlib.sha256(json.dumps(bound, sort_keys=True, ensure_ascii=False).encode()).hexdigest())
    db().shield_separations.insert_one(dict(receipt)); receipt.pop('_id', None)
    receipt['external_plan'] = plan; receipt['internal_bound_plan'] = bound; receipt['outbound_payload'] = payload
    return receipt


def _plan_json(raw):
    raw = raw.strip()
    if raw.startswith('```'): raw = raw.split('\n', 1)[1].rsplit('```', 1)[0].strip()
    start, end = raw.find('{'), raw.rfind('}')
    try: return json.loads(raw[start:end + 1])
    except ValueError: return {'milestones': [], 'risks': ['planner response was not valid JSON'], 'assumptions': [], 'raw_excerpt_sha256': hashlib.sha256(raw.encode()).hexdigest()}


def receipts(tenant, limit=30):
    return list(db().shield_separations.find({'tenant_id': tenant}, {'_id': 0}, sort=[('at', -1)], limit=limit))
