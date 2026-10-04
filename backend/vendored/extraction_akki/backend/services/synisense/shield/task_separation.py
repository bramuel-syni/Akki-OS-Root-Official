"""Data/task separation (owner Mα order §2): a workflow triggered by a confidential document lets an external planner or designer participate
without any access to the privileged data — from any angle. The document is classified and reconstructed inside the Shield; the external
model receives only the abstract task and structure; every outbound byte is inspected against the bound values before dispatch through the sole
chokepoint; the returned plan is bound back to the real values by the internal worker, locally. A task that itself asks for protected meaning
is refused before any call. Receipts carry digests, categories and inspection results — never the values."""
import hashlib
import json
import logging
import re
import uuid

from services.synisense.shield import semantic_register as reg
from services.training_lab import store as lab

log = logging.getLogger(__name__)
PURPOSE = 'doc_studio.plan'
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


def build_outbound(document, task, tenant):
    """Abstract brief for the external participant: structure + safe text + task. Returns payload (dict), bindings (kept inside) and the inspection."""
    recon = reg.reconstruct(document, tenant, mode='abstract')
    payload = {'task': task, 'document_structure': _structure(document), 'abstract_document': recon['safe_text'], 'placeholders': {k: v['hint'] for k, v in recon['bindings'].items()},
               'constraints': ['no underlying records are available', 'placeholders must remain verbatim', 'no tool calls, fetches or rehydration', 'return structure and instructions only']}
    protected = [b['value'] for b in recon['bindings'].values()] + [s.get('text') for s in reg.classify(document, tenant) if s.get('action') == 'remove']
    inspection = reg.inspect_outbound(json.dumps(payload, ensure_ascii=False) + ' ' + SYSTEM, protected)
    return payload, recon, inspection


def bind(plan_json, bindings):
    """Internal worker binds placeholders back to actual values; this never leaves the tenant boundary."""
    text = json.dumps(plan_json, ensure_ascii=False)
    for token, b in bindings.items(): text = text.replace(token, b['value'])
    return json.loads(text)


async def separate(document, task, tenant, actor, dry_run=False):
    receipt = {'separation_id': 'sep-' + uuid.uuid4().hex[:12], 'tenant_id': tenant, 'actor': actor, 'at': lab.now(), 'purpose': PURPOSE, 'document_sha256': hashlib.sha256(document.encode()).hexdigest(), 'task_sha256': hashlib.sha256(task.encode()).hexdigest(), 'dry_run': dry_run}
    cues = _task_requests_protected(task)
    if cues:
        receipt.update(status='refused', reason='task requests protected meaning', cues=cues, external_call=False)
        db().shield_separations.insert_one(dict(receipt)); receipt.pop('_id', None); return receipt
    payload, recon, inspection = build_outbound(document, task, tenant)
    receipt.update(categories_applied=recon['categories_applied'], placeholders=len(recon['bindings']), joint_disclosure=recon['joint_disclosure'], outbound_sha256=hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest(), inspection=inspection)
    if not inspection['clean'] or not recon['joint_disclosure']['passes']:
        receipt.update(status='refused', reason='outbound payload would carry protected values or a reconstructive combination', external_call=False)
        db().shield_separations.insert_one(dict(receipt)); receipt.pop('_id', None); return receipt
    if dry_run:
        receipt.update(status='inspected', external_call=False, outbound_payload=payload)
        db().shield_separations.insert_one({k: v for k, v in receipt.items() if k != 'outbound_payload'}); receipt.pop('_id', None)
        receipt['internal_binding_available'] = bool(recon['bindings']); return receipt
    from services.chokepoint.llm import invoke
    from services.chokepoint.model_roles import resolve
    planner = resolve('planner')
    response = await invoke(purpose=PURPOSE, prompt=json.dumps(payload, ensure_ascii=False), masking_tier='llm_prompt_governed_text', actor=actor, model=planner['model'], provider=planner['connection'],
                            tenant_id=tenant, custody_class='tenant_estate', system_message=SYSTEM, session_id=receipt['separation_id'])
    raw = response.text.strip()
    if raw.startswith('```'): raw = raw.split('\n', 1)[1].rsplit('```', 1)[0].strip()
    start, end = raw.find('{'), raw.rfind('}')
    try: plan = json.loads(raw[start:end + 1])
    except ValueError: plan = {'milestones': [], 'risks': ['planner response was not valid JSON'], 'assumptions': [], 'raw_excerpt_sha256': hashlib.sha256(raw.encode()).hexdigest()}
    inbound = reg.inspect_outbound(json.dumps(plan, ensure_ascii=False), [b['value'] for b in recon['bindings'].values()])
    bound = bind(plan, recon['bindings'])
    receipt.update(status='delivered', external_call=True, model=response.model_id, provider=response.provider, chokepoint_receipt_id=response.receipt_id, tokens_in=response.tokens_in, tokens_out=response.tokens_out, latency_ms=response.latency_ms,
                   plan_returned_contains_protected_values=not inbound['clean'], plan_milestones=len(plan.get('milestones') or []), bound_plan_sha256=hashlib.sha256(json.dumps(bound, sort_keys=True, ensure_ascii=False).encode()).hexdigest())
    db().shield_separations.insert_one(dict(receipt)); receipt.pop('_id', None)
    receipt['external_plan'] = plan; receipt['internal_bound_plan'] = bound; receipt['outbound_payload'] = payload
    return receipt


def receipts(tenant, limit=30):
    return list(db().shield_separations.find({'tenant_id': tenant}, {'_id': 0}, sort=[('at', -1)], limit=limit))
