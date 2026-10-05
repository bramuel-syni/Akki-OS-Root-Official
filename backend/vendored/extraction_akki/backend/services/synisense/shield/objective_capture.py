"""Pre-redaction objective capture (WP-A3 · Doc 1 B5.1–B5.5 [B82–B87], B6 [B89–B93]).

For a question-bearing request the fixed sequence is extract-intent → de-identify → invoke → re-identify (B82). The contained reader (WP-A2)
reads the WHOLE un-redacted question inside the perimeter and yields ONE frozen objective artefact — intent, bounded objective, meaning — that
survives redaction (B83), is immutable for the life of the request (B84: a changed question is a new request, never an edit), records the
declared intent and accumulates demonstrated-intent observations separately (B85), and is consumed downstream BY REFERENCE (B91). Extraction
failure has a defined, non-fabricating outcome — `ask` for a human in the loop, `refuse` for a system caller (B86/B87); reader unavailability
refuses before any external client exists (A2 d). Nothing here calls an external model."""
import hashlib
import json
import uuid

from pymongo.errors import DuplicateKeyError

from services.solva_v2.intent_audit import open_intent_audit, update_intent_audit_demonstrated
from services.synisense.shield import contained_reader as reader
from services.synisense.shield import semantic_register as reg
from services.training_lab import store as lab

FROZEN_FIELDS = ('artifact_id', 'request_id', 'tenant_id', 'caller', 'intent', 'bounded_objective', 'meaning', 'declared_intent', 'coherent', 'question_sha256', 'captured_at', 'reader')
CLAUSES = ('Doc1 B82 extraction precedes de-identification', 'Doc1 B83 meaning not tokens', 'Doc1 B84 frozen', 'Doc1 B85 declared and demonstrated', 'Doc1 B86/B87 refuse or ask, never guess', 'Doc1 B91 one artefact consumed downstream')
# demonstrated conduct that diverges from the declared objective (B85): tracked, never assumed absent
DIVERGENCE_RULES = {'grounding_outside_window': 'the answer cited outside the pinned window or in an unverifiable form', 'scope_drift': 'a follow-up left the declared objective’s scope (gate: out of scope)',
                    'protected_meaning_requested': 'the conduct asked for protected meaning the declared objective did not'}


class ObjectiveNotCaptured(Exception):
    """B86/B87: no coherent objective could be captured; `outcome` is `ask` (human in the loop) or `refuse` (system caller). Never a guess."""
    def __init__(self, outcome, kind, reason):
        super().__init__(f'{outcome}:{kind}: {reason}'); self.outcome, self.kind, self.reason = outcome, kind, reason


class ObjectiveFrozen(Exception):
    """B84: the artefact is immutable; a change in what is asked is a new request."""


class ObjectiveTampered(Exception):
    """B92: the stored artefact no longer matches its own hash; nothing downstream may consume it."""


def db():
    database = lab.db()
    database.shield_objectives.create_index('request_id', unique=True)
    database.shield_objectives.create_index('artifact_id', unique=True)
    database.shield_objective_observations.create_index([('artifact_id', 1), ('at', 1)])
    return database


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def _digest(doc):
    return sha(json.dumps({k: doc.get(k) for k in FROZEN_FIELDS}, sort_keys=True, ensure_ascii=False, default=str))


def _public(doc):
    doc = dict(doc or {}); doc.pop('_id', None); return doc


def for_request(request_id):
    return _public(db().shield_objectives.find_one({'request_id': request_id})) or None


def get(artifact_id):
    doc = db().shield_objectives.find_one({'artifact_id': artifact_id})
    if not doc: raise LookupError(f'no objective artefact {artifact_id}')
    return _public(doc)


def declared_categories(tenant_id):
    return [{'name': c['name'], 'description': (c.get('description') or '')[:200]} for c in reg.categories(tenant_id)]


def capture(question, tenant_id, request_id, caller='human', categories=None, purpose='objective_capture'):
    """Read the whole un-redacted question with the contained reader and freeze ONE artefact for this request (idempotent for the same question)."""
    text = str(question or '')
    if not text.strip(): raise ObjectiveNotCaptured('refuse' if caller == 'system' else 'ask', 'empty', 'no question was asked')
    question_sha = sha(text)
    existing = for_request(request_id)
    if existing:
        if existing['question_sha256'] == question_sha: return verify(existing['artifact_id'])
        raise ObjectiveFrozen(f'request {request_id} already carries objective {existing["artifact_id"]}; a change in what is asked is a new request (Doc 1 B84)')
    cats = categories if categories is not None else declared_categories(tenant_id)
    try:
        read = reader.read(text, cats, f'{purpose}:{request_id}')
    except reader.ReaderUnavailable as exc:
        raise ObjectiveNotCaptured('refuse', 'reader_unavailable', f'the contained reader is not available ({str(exc)[:160]}); no external model may read the original to decide for it') from exc
    reading = read['reading']; objective = reading.get('objective') or {}
    bounded = str(objective.get('bounded_objective') or '').strip(); meaning = str(reading.get('meaning') or '').strip()
    if objective.get('coherent') is not True or not bounded:
        raise ObjectiveNotCaptured('refuse' if caller == 'system' else 'ask', 'incoherent', bounded or 'the reader could not bound the question to one coherent objective')
    protected = [s['text'] for s in reg.classify(text, tenant_id, enforcement='enforced', cues='off')] + [p['span'] for p in reading.get('privileged') or [] if isinstance(p, dict) and isinstance(p.get('span'), str)]
    inspection = reg.inspect_outbound(bounded + ' ' + meaning, protected)
    if not inspection['clean']:
        raise ObjectiveNotCaptured('refuse', 'unsafe_reading', f"the extracted objective repeats {len(inspection['protected_values_found'])} protected value(s); it cannot cross")
    intent = str(objective.get('intent') or 'unspecified')[:80]
    doc = {'artifact_id': 'obj-' + uuid.uuid4().hex[:12], 'request_id': request_id, 'tenant_id': tenant_id, 'caller': caller, 'intent': intent, 'bounded_objective': bounded[:2000], 'meaning': meaning[:2000], 'declared_intent': intent,
           'coherent': True, 'question_sha256': question_sha, 'question_chars': len(text), 'privileged_spans': len(reading.get('privileged') or []), 'indirect_disclosures': len(reading.get('indirect_disclosures') or []), 'categories_declared': len(cats),
           'reader': {'model_id': (read.get('lineage') or {}).get('model_id'), 'weight_sha256': (read.get('lineage') or {}).get('weight_sha256'), 'host': (read.get('lineage') or {}).get('host'), 'receipt_id': read.get('receipt_id'), 'seconds': read.get('seconds')},
           'captured_at': lab.now(), 'sequence_position': 'before_deidentify', 'clause_refs': list(CLAUSES), 'inspection': inspection}
    doc['sha256'] = _digest(doc)
    try: db().shield_objectives.insert_one(dict(doc))
    except DuplicateKeyError:
        return capture(question, tenant_id, request_id, caller, categories, purpose)
    return _public(doc)


def verify(artifact_id):
    """Consume by reference (B91): the stored artefact must still match its own hash (B92)."""
    doc = get(artifact_id)
    if _digest(doc) != doc.get('sha256'): raise ObjectiveTampered(f'objective artefact {artifact_id} fails its hash; the record no longer proves what was asked (Doc 1 B92)')
    return doc


def revise(artifact_id, **_):
    """The explicit non-path (B84/B92): there is no edit of a live objective."""
    raise ObjectiveFrozen(f'objective artefact {artifact_id} is frozen for the life of its request; ask again as a new request (Doc 1 B84)')


def observe(artifact_id, kind, detail):
    """B85: append one demonstrated-intent observation (append-only; the artefact itself is untouched)."""
    artefact = verify(artifact_id)
    flags = _flags(kind, detail)
    row = {'artifact_id': artifact_id, 'request_id': artefact['request_id'], 'tenant_id': artefact['tenant_id'], 'at': lab.now(), 'kind': kind, 'detail': detail, 'divergence': flags}
    db().shield_objective_observations.insert_one(dict(row)); row.pop('_id', None)
    record = open_intent_audit(session_id=artefact['request_id'], declared_situation_class=artefact['declared_intent'])
    for prior in db().shield_objective_observations.find({'artifact_id': artifact_id}, {'_id': 0}, sort=[('at', 1)]):
        record = update_intent_audit_demonstrated(record, json.dumps({'kind': prior['kind'], 'divergence': prior['divergence']}, sort_keys=True))
    return {'observation': row, 'intent_audit': record.model_dump()}


def _flags(kind, detail):
    detail = detail or {}; flags = []
    if kind == 'turn':
        if detail.get('grounding') in ('uncited', 'partially_cited', 'unverified_format') or (detail.get('citations_dropped') or 0) > 0: flags.append('grounding_outside_window')
        if detail.get('decision') == 'refused' and detail.get('reason') == 'out_of_scope' and detail.get('follow_up'): flags.append('scope_drift')
        if detail.get('requests_protected_meaning'): flags.append('protected_meaning_requested')
    return flags


def divergence(artifact_id):
    """Declared vs demonstrated (B85): both fields on one record; divergence is reported, never assumed absent."""
    artefact = verify(artifact_id)
    rows = list(db().shield_objective_observations.find({'artifact_id': artifact_id}, {'_id': 0}, sort=[('at', 1)]))
    hit = sorted({f for r in rows for f in r.get('divergence') or []})
    return {'artifact_id': artifact_id, 'declared_intent': artefact['declared_intent'], 'bounded_objective': artefact['bounded_objective'], 'observations': len(rows), 'divergent': [{'flag': f, 'meaning': DIVERGENCE_RULES[f]} for f in hit], 'diverged': bool(hit),
            'last_observed_at': rows[-1]['at'] if rows else None}


__all__ = ['ObjectiveNotCaptured', 'ObjectiveFrozen', 'ObjectiveTampered', 'capture', 'verify', 'revise', 'observe', 'divergence', 'get', 'for_request', 'declared_categories', 'FROZEN_FIELDS', 'DIVERGENCE_RULES']
