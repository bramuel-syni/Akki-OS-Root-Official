"""SyniSense semantic confidentiality register and reconstruction.

The register holds three category kinds per tenant: `exact` (literal values), `pattern` (regular expressions) and `contextual` (meanings
recognised from surrounding cues — a price method, a client's identity, a penalty clause — whatever the literal label). `classify` finds
protected spans with their category and the cue that fired; `reconstruct` rewrites the text so an external model receives the structure and
the task but none of the privileged values, keeping typed placeholders that an internal worker can bind back. The joint-disclosure check
refuses outputs where the surviving quasi-identifiers in one passage could still re-identify the protected party. Deterministic; the
existing deidentifier (NER + regex) is the first layer, the register is the second, context is the third."""
import hashlib
import re
import uuid
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from services.training_lab import store as lab

KINDS = ('exact', 'pattern', 'contextual')
ACTIONS = ('remove', 'abstract', 'generalise')
ENFORCEMENT = ('enforced', 'advisory')
# Doc 2 A4/A5: draft (proposed) → pending (adopted, not yet live) → active (approved; the only status the crossing consumes) → superseded |
# removed (through the counter-signed countdown ceremony). `withdrawn` keeps a pending declaration the DPO abandoned on the record (A5.5).
STATUSES = ('draft', 'pending', 'active', 'superseded', 'removed', 'withdrawn')
RETIRED = ('superseded', 'removed', 'withdrawn')
REMOVAL_BUSINESS_TYPE = 'system_ordinary'
# WP-A4 (Doc 2 B21/B35): Category-3 (contextual) declarations are recognised by the contained reader; cue words are the draft proposer and
# advisory receipts only — never a rewrite or refusal cause
RECOGNISER = 'contained_reader'
CUE_MODES = ('advisory', 'propose', 'off')


class Conflict(Exception):
    """The requested transition is not available from the declaration's current state."""
CONFIDENTIALITY_MARKERS = ('confidential', 'trade secret', 'proprietary', 'internal only', 'not for disclosure', 'nda', 'privileged', 'restricted', 'embargo', 'siri', 'faragha')

# `enforced` categories are rewritten (or the crossing refused) on EVERY model call and rebound in the reply; `advisory` categories are
# found and receipted on every crossing but only rewritten in the confidential-document workflow — the DPO moves a category between the two.
DEFAULT_CATEGORIES = [
    {'name': 'client_identity', 'kind': 'contextual', 'recogniser': 'contained_reader', 'action': 'abstract', 'enforcement': 'enforced', 'description': 'who the counterparty, client or partner is — names, trading names, cooperative or company identifiers',
     'cues': ['client', 'customer', 'counterparty', 'partner', 'cooperative', 'co-operative', 'ltd', 'limited', 'plc', 'company', 'between', 'party', 'licensee', 'licensor', 'supplier', 'vendor', 'tenant', 'landlord', 'mteja', 'kampuni'], 'targets': ['PERSON', 'ORG', 'PROPER_NOUN']},
    {'name': 'private_project_name', 'kind': 'contextual', 'recogniser': 'contained_reader', 'action': 'abstract', 'enforcement': 'enforced', 'description': 'internal code names and unreleased project names', 'cues': ['project', 'codename', 'code name', 'internal', 'initiative', 'programme', 'program', 'workstream', 'mradi'], 'targets': ['PROPER_NOUN', 'ORG']},
    {'name': 'credentials', 'kind': 'pattern', 'action': 'remove', 'enforcement': 'enforced', 'description': 'keys, tokens, passwords, access credentials', 'patterns': [r'(?i)\b(?:api[-_ ]?key|secret|token|password|passcode|credential|nenosiri)s?\b\s*(?:[:=]\s*|\s+(?=[A-Za-z\-_./+]*\d))[A-Za-z0-9\-_./+]{6,}', r'\b[A-Z0-9]{3,}(?:-[A-Z0-9]{2,}){2,}\b', r'\bsk-[A-Za-z0-9]{8,}\b']},
    {'name': 'commercial_terms', 'kind': 'contextual', 'recogniser': 'contained_reader', 'action': 'abstract', 'enforcement': 'advisory', 'description': 'fees, prices, discounts, margins, payment terms, penalties, exclusivity and other negotiated figures', 'cues': ['fee', 'price', 'pricing', 'discount', 'margin', 'rate', 'payment', 'penalty', 'royalty', 'commission', 'retainer', 'deposit', 'reserve', 'bid', 'floor', 'uplift', 'cap', 'budget', 'cost', 'salary', 'kes', 'usd', 'eur', 'gbp', 'shilling', '%', 'bei', 'ada', 'malipo', 'mshahara'], 'targets': ['MONEY', 'NUMBER', 'PERCENT']},
    {'name': 'unpublished_pricing_method', 'kind': 'contextual', 'recogniser': 'contained_reader', 'action': 'remove', 'enforcement': 'advisory', 'description': 'how a price or bid is computed — formulas, multipliers, thresholds, seasonal adjustments', 'cues': ['method', 'formula', 'calculates', 'calculated', 'computed', 'times', 'multiplied', 'multiplier', 'plus', 'minus', 'threshold', 'coefficient', 'adjustment', 'uplift', 'weighting', 'algorithm', 'fomula', 'mara'], 'targets': ['SENTENCE']},
    {'name': 'personal_data', 'kind': 'pattern', 'action': 'remove', 'enforcement': 'enforced', 'description': 'direct identifiers: phone numbers, e-mail addresses, national ID / passport numbers, physical addresses',
     'patterns': [r'(?<![\w.+-])[\w.+-]+@[\w-]+(?:\.[\w-]+)+', r'(?<!\d)(?:\+?254|0)7\d{2}[ -]?\d{3}[ -]?\d{3}(?!\d)', r'(?<!\d)\+?\d{1,3}[ -]?\(?\d{2,4}\)?[ -]?\d{3}[ -]?\d{3,4}(?!\d)', r'(?i)\b(?:id|passport|national id|kra pin|kitambulisho)\s*(?:no\.?|number|nambari|:)?\s*[A-Z]?\d{6,9}\b', r'(?i)\bP\.?O\.?\s*Box\s*\d+[^\n,.]*']},
    {'name': 'dates_and_deadlines', 'kind': 'pattern', 'action': 'generalise', 'enforcement': 'advisory', 'description': 'calendar dates and deadlines that would identify the engagement', 'patterns': [r'\b\d{4}-\d{2}-\d{2}\b', r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?,?\s+\d{4}\b', r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4}\b']},
]
MONEY = re.compile(r'(?i)\b(?:kes|ksh|kshs|usd|eur|gbp|tzs|ugx|\$|€|£)\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:million|m|bn|billion|k))?\b|\b\d[\d,]*(?:\.\d+)?\s?(?:kes|ksh|kshs|usd|eur|gbp|shillings?|dollars?)\b')
NUMBER = re.compile(r'(?<![\w.])\d+(?:[.,]\d+)*(?![\w])')
PERCENT = re.compile(r'\d+(?:\.\d+)?\s?(?:%|percent|per cent)')
PROPER = re.compile(r"\b(?:[A-Z][a-zA-Z'’-]+(?:\s+(?:[A-Z][a-zA-Z'’-]+|of|and|&|the|de|du|la)){0,4})\b")
STOP = {'The', 'A', 'An', 'This', 'That', 'These', 'Those', 'It', 'We', 'You', 'They', 'Our', 'Your', 'Their', 'Client', 'Internal', 'Access', 'Delivery', 'Synthetic', 'Contract', 'Project', 'Stage', 'Section', 'Schedule', 'Party', 'Parties', 'Agreement', 'Services', 'Service', 'Monitor', 'Return', 'Decide', 'Scenario', 'Neither', 'Compare', 'If', 'In', 'On', 'For', 'By', 'To', 'With', 'From', 'At', 'As', 'Or', 'And', 'But', 'Is', 'Are', 'Was', 'Were', 'Be', 'Has', 'Have', 'Not', 'No', 'All', 'Any', 'Each', 'Every', 'Both', 'Such', 'Other', 'Same', 'Also', 'Then', 'There', 'Here', 'When', 'Where', 'Which', 'Who', 'What', 'How', 'Why', 'Please', 'Note', 'Design', 'Create', 'Produce', 'Deliver', 'Prepare', 'Present', 'Discover', 'Mr', 'Mrs', 'Ms', 'Dr'}
SENTENCE_SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z])')


def db():
    database = lab.db()
    database.shield_register.create_index([('tenant_id', 1), ('name', 1), ('version', -1)])
    return database


def now():
    return lab.now()


# ----------------------------------------------------------------------------- register authoring (DPO-governed, versioned, removable)
def ensure_defaults(tenant):
    coll = db().shield_register
    # the shipped defaults are detected by their own authorship, not by "any document exists": a tenant whose first act is a DPO declaration still receives them
    if coll.count_documents({'tenant_id': tenant, 'authored_by': 'shield.defaults'}):
        for cat in DEFAULT_CATEGORIES:
            # categories installed before enforcement scopes existed receive the default scope once; the DPO's later choice is never overwritten
            coll.update_many({'tenant_id': tenant, 'name': cat['name'], 'enforcement': {'$exists': False}}, {'$set': {'enforcement': cat['enforcement']}})
            # a default the DPO never revised tracks the shipped cue/pattern lists (multilingual cues added later); DPO-authored versions are untouched
            doc = coll.find_one({'tenant_id': tenant, 'name': cat['name'], 'status': 'active', 'authored_by': 'shield.defaults'})
            if doc and any(doc.get(k) != cat.get(k) for k in ('cues', 'patterns', 'targets', 'description', 'recogniser')):
                coll.update_one({'_id': doc['_id']}, {'$set': {k: cat.get(k) for k in ('cues', 'patterns', 'targets', 'description', 'recogniser')}, '$push': {'history': {'at': now(), 'by': 'shield.defaults', 'change': 'shipped default cues/patterns refreshed (never revised by the DPO)'}}})
        coll.update_many({'tenant_id': tenant, 'enforcement': {'$exists': False}}, {'$set': {'enforcement': 'enforced'}})
        return 0
    for cat in DEFAULT_CATEGORIES:
        coll.insert_one({**cat, 'tenant_id': tenant, 'category_id': 'cat-' + uuid.uuid4().hex[:10], 'version': 1, 'status': 'active', 'authored_by': 'shield.defaults', 'authored_at': now(), 'history': [{'at': now(), 'by': 'shield.defaults', 'change': 'default category installed; DPO may revise, re-scope or remove'}]})
    return len(DEFAULT_CATEGORIES)


def categories(tenant, include_removed=False, include_drafts=False, include_pending=False):
    """The crossing consumes `active` only (A5.1): a pending or draft declaration is returned solely when asked for, never to `classify`."""
    ensure_defaults(tenant); _migrate_catalogue(tenant)
    statuses = ['active'] + (['draft'] if include_drafts else []) + (['pending'] if include_pending else []) + (list(RETIRED) if include_removed else [])
    return list(db().shield_register.find({'tenant_id': tenant, 'status': {'$in': statuses}}, {'_id': 0}, sort=[('status', 1), ('name', 1), ('version', -1)]))


def entity_declarations(tenant):
    """The authored portion of the tenant entity set the de-identifier consults (A5.1): approved exact declarations carrying an entity type."""
    _migrate_catalogue(tenant)
    return list(db().shield_register.find({'tenant_id': tenant, 'status': 'active', 'kind': 'exact', 'entity_type': {'$type': 'string'}}, {'_id': 0}))


_migrated = set()


def _migrate_catalogue(tenant):
    """One entity set (B45): the seed tenant catalogue becomes authored exact declarations in the register; the file is a migration source only."""
    if tenant in _migrated: return 0
    from services.synisense.shield.tenant_entities import ENTITY_TYPE_MAP, catalogue_groups
    coll = db().shield_register; n = 0
    for group, entries in catalogue_groups(tenant).items():
        name = f'catalogue_{group}'; values = sorted({e.get('surface_form', '') for e in entries} | {v for e in entries for v in e.get('variant_forms', [])} - {''})
        if not values: continue
        current = coll.find_one({'tenant_id': tenant, 'name': name, 'status': 'active'})
        if current is None:
            coll.insert_one({'tenant_id': tenant, 'category_id': 'cat-' + uuid.uuid4().hex[:10], 'name': name, 'kind': 'exact', 'action': 'abstract', 'enforcement': 'enforced', 'entity_type': ENTITY_TYPE_MAP[group], 'values': values, 'cues': None, 'targets': None, 'patterns': None,
                             'description': f'{group} named in the tenant catalogue (estate vocabulary harvested at census); recognised on every crossing', 'provenance': 'migrated_from_catalogue', 'version': 1, 'status': 'active',
                             'authored_by': 'shield.catalogue_migration', 'authored_at': now(), 'adopted_by': 'shield.catalogue_migration', 'adopted_at': now(), 'approved_by': 'shield.catalogue_migration', 'approved_at': now(),
                             'history': [{'at': now(), 'by': 'shield.catalogue_migration', 'change': f'migrated from tenant_catalogue.v0.json: {len(values)} surface form(s) already in force at the crossing', 'version': 1}]}); n += 1
        elif set(values) - set(current.get('values') or []):
            coll.update_one({'_id': current['_id']}, {'$set': {'values': sorted(set(current.get('values') or []) | set(values))}, '$push': {'history': {'at': now(), 'by': 'shield.catalogue_migration', 'change': f'{len(set(values) - set(current.get("values") or []))} surface form(s) appended from the catalogue'}}}); n += 1
    _migrated.add(tenant); return n


def _validate(body):
    if body['kind'] not in KINDS or body['action'] not in ACTIONS: raise ValueError('kind must be exact|pattern|contextual and action remove|abstract|generalise')
    if body.get('enforcement', 'enforced') not in ENFORCEMENT: raise ValueError('enforcement must be enforced|advisory')
    if body['kind'] == 'exact' and not body.get('values'): raise ValueError('An exact category lists the literal values it protects')
    if body['kind'] == 'pattern':
        for p in body.get('patterns') or []: re.compile(p)
        if not body.get('patterns'): raise ValueError('A pattern category needs at least one regular expression')
    if body['kind'] == 'contextual':
        # Doc 2 A5.2 (B35): a category declaration is testable only when bound to the reasoning-layer recogniser — the DPO's description is what the
        # contained reader applies; cue words are optional proposer hints, never the enforcement mechanism
        if len(str(body.get('description') or '').strip()) < 3: raise ValueError('A contextual (Category-3) declaration describes the privileged meaning the contained reader must recognise')
        body['recogniser'] = RECOGNISER
    if body.get('entity_type') is not None and (body['kind'] != 'exact' or not re.fullmatch(r'[A-Z][A-Z0-9_]{1,30}', str(body['entity_type']))): raise ValueError('entity_type is an upper-case label on an exact declaration')


def _fields(body):
    return {k: body.get(k) for k in ('name', 'kind', 'action', 'description', 'cues', 'targets', 'patterns', 'values', 'entity_type', 'recogniser')} | {'enforcement': body.get('enforcement') or 'enforced'}


def _one(coll, tenant, name, status):
    return coll.find_one({'tenant_id': tenant, 'name': name, 'status': status})


def _pending_from(tenant, actor, body, lineage, change, provenance=None, source=None):
    """Adopt (B28): the shaped declaration enters `pending`. It is not in the crossing set until approved (B29, B43)."""
    _validate(body)
    coll = db().shield_register
    if _one(coll, tenant, body['name'], 'pending'): raise Conflict('A pending declaration of that name awaits approval; approve or withdraw it first')
    prior = _one(coll, tenant, body['name'], 'active')
    doc = _fields(body)
    doc.update(tenant_id=tenant, category_id=prior['category_id'] if prior else (lineage or {}).get('category_id') or 'cat-' + uuid.uuid4().hex[:10], version=(prior['version'] + 1) if prior else 1, status='pending',
               authored_by=actor, authored_at=now(), adopted_by=actor, adopted_at=now(), history=((lineage or {}).get('history') or []) + [{'at': now(), 'by': actor, 'change': change, 'version': (prior['version'] + 1) if prior else 1}])
    if provenance: doc['provenance'] = provenance
    if source: doc.update(source)
    coll.insert_one(dict(doc)); doc.pop('_id', None); return doc


def author(tenant, actor, body):
    """DPO declares a category in their own terms (Generate + Adopt in one act, B25/B28): it lands `pending`; approval puts it in force."""
    coll = db().shield_register
    doc = _pending_from(tenant, actor, body, None, 'declared by the DPO and adopted; awaits approval' + (' (revision)' if _one(coll, tenant, body['name'], 'active') else ''))
    coll.delete_many({'tenant_id': tenant, 'name': body['name'], 'status': 'draft'})
    return doc


def adopt(tenant, actor, name, edits=None):
    """DPO adopts a proposed draft (optionally edited) → pending; the draft's own history is retained (B40)."""
    coll = db().shield_register; draft = _one(coll, tenant, name, 'draft')
    if not draft: raise LookupError('No draft with that name awaits adoption')
    body = {k: draft.get(k) for k in ('name', 'kind', 'action', 'description', 'cues', 'targets', 'patterns', 'values', 'enforcement', 'entity_type')} | {k: v for k, v in (edits or {}).items() if v is not None}
    doc = _pending_from(tenant, actor, body, {'category_id': draft['category_id'], 'history': draft.get('history', [])}, 'adopted' + (' with edits' if edits else '') + '; awaits approval',
                        source={k: draft[k] for k in ('source_ref', 'source_sha256') if k in draft})
    coll.delete_one({'_id': draft['_id']}); return doc


def approve(tenant, actor, name):
    """Approve (B29, A5.4): the governed act that commits a pending declaration into force; the prior version is superseded, its history carried."""
    coll = db().shield_register; pend = _one(coll, tenant, name, 'pending')
    if not pend: raise LookupError('No pending declaration with that name awaits approval')
    prior = _one(coll, tenant, name, 'active')
    history = (prior.get('history', []) if prior else []) + pend.get('history', []) + [{'at': now(), 'by': actor, 'change': 'approved into force', 'version': pend['version'], 'same_signatory': actor == pend.get('adopted_by')}]
    if prior: coll.update_one({'_id': prior['_id']}, {'$set': {'status': 'superseded', 'superseded_at': now(), 'superseded_by_version': pend['version']}})
    coll.update_one({'_id': pend['_id']}, {'$set': {'status': 'active', 'approved_by': actor, 'approved_at': now(), 'history': history}})
    return coll.find_one({'_id': pend['_id']}, {'_id': 0})


def withdraw(tenant, actor, name, reason):
    """DPO abandons a pending declaration; it stays on the record as withdrawn (A5.5)."""
    coll = db().shield_register; pend = _one(coll, tenant, name, 'pending')
    if not pend: raise LookupError('No pending declaration with that name')
    coll.update_one({'_id': pend['_id']}, {'$set': {'status': 'withdrawn', 'withdrawn_at': now(), 'withdrawn_by': actor}, '$push': {'history': {'at': now(), 'by': actor, 'change': f'withdrawn before approval: {reason}'}}})
    return coll.find_one({'_id': pend['_id']}, {'_id': 0})


def discard(tenant, actor, name):
    res = db().shield_register.delete_many({'tenant_id': tenant, 'name': name, 'status': 'draft'})
    if not res.deleted_count: raise LookupError('No draft with that name')
    return res.deleted_count


# ----------------------------------------------------------------------------- removal: the consequential direction runs the governed change ceremony (A5.4 B39; Doc 14 case)
def _active_with_removal(tenant, name, state):
    doc = db().shield_register.find_one({'tenant_id': tenant, 'name': name, 'status': 'active', 'removal.state': state})
    if not doc: raise LookupError(f'No active declaration named {name!r} with a removal in state {state!r}')
    return doc


def remove(tenant, actor, name, reason):
    """Propose removal. The declaration keeps protecting until the ceremony applies: proposed → second signature → countdown → applied → re-verified."""
    from services.rules_service import ceremony
    coll = db().shield_register; doc = _one(coll, tenant, name, 'active')
    if not doc: raise LookupError('No active category with that name')
    if doc.get('removal'): raise Conflict(f"A removal ceremony is already {doc['removal']['state']} for this declaration")
    removal = {'state': 'proposed', 'reason': reason, 'proposed_by': actor, 'proposed_at': now(), 'business_type': REMOVAL_BUSINESS_TYPE, 'countdown_hours': ceremony.SYSTEM_ORDINARY_COUNTDOWN_HOURS, 'witness_source': ceremony.WITNESS_IDENTITY_SOURCE}
    coll.update_one({'_id': doc['_id']}, {'$set': {'removal': removal}, '$push': {'history': {'at': now(), 'by': actor, 'change': f'removal proposed: {reason}; awaits a second signature'}}})
    return coll.find_one({'_id': doc['_id']}, {'_id': 0})


def countersign_removal(tenant, actor, name):
    from services.rules_service import ceremony
    doc = _active_with_removal(tenant, name, 'proposed')
    if actor == doc['removal']['proposed_by']: raise ceremony.SecondSignatoryMissing('The second signature must come from a different DPO or master admin than the proposer')
    signed = now(); applies_at = (datetime.fromisoformat(signed) + timedelta(hours=doc['removal']['countdown_hours'])).isoformat()
    db().shield_register.update_one({'_id': doc['_id']}, {'$set': {'removal.state': 'countdown', 'removal.counter_signed_by': actor, 'removal.counter_signed_at': signed, 'removal.applies_at': applies_at},
                                                           '$push': {'history': {'at': now(), 'by': actor, 'change': f"removal counter-signed; countdown of {doc['removal']['countdown_hours']} h runs until {applies_at}; cancellable until then"}}})
    return db().shield_register.find_one({'_id': doc['_id']}, {'_id': 0})


def cancel_removal(tenant, actor, name, reason):
    coll = db().shield_register; doc = coll.find_one({'tenant_id': tenant, 'name': name, 'status': 'active', 'removal.state': {'$in': ['proposed', 'countdown']}})
    if not doc: raise LookupError('No removal in flight for that declaration')
    ceremony_record = {**doc['removal'], 'state': 'cancelled', 'cancelled_by': actor, 'cancelled_at': now(), 'cancel_reason': reason}
    coll.update_one({'_id': doc['_id']}, {'$unset': {'removal': ''}, '$push': {'history': {'at': now(), 'by': actor, 'change': f'removal cancelled during the ceremony: {reason}', 'ceremony': ceremony_record}}})
    return coll.find_one({'_id': doc['_id']}, {'_id': 0})


def apply_removal(tenant, actor, name, now_utc=None):
    """Apply after the countdown has elapsed, then re-verify that the crossing no longer recognises the declaration's values."""
    from services.rules_service import ceremony
    doc = _active_with_removal(tenant, name, 'countdown'); current = now_utc or datetime.now(timezone.utc)
    applies_at = datetime.fromisoformat(doc['removal']['applies_at'])
    if current < applies_at: raise ceremony.CountdownNotElapsed(f'countdown runs until {applies_at.isoformat()}; {applies_at - current} remaining')
    coll = db().shield_register
    coll.update_one({'_id': doc['_id']}, {'$set': {'status': 'removed', 'removed_at': now(), 'removed_by': actor, 'removal_reason': doc['removal']['reason'], 'removal.state': 'applied', 'removal.applied_by': actor, 'removal.applied_at': now()},
                                          '$push': {'history': {'at': now(), 'by': actor, 'change': f"removed after the ceremony: {doc['removal']['reason']}"}}})
    values = [v for v in (doc.get('values') or []) if v]
    survivors = [v for v in values if any(s['category'] == name for s in classify(v, tenant))]
    still_listed = any(c['name'] == name for c in categories(tenant))
    verified = {'at': now(), 'clean': not survivors and not still_listed, 'values_checked': len(values), 'survivors': len(survivors), 'still_in_crossing_set': still_listed}
    coll.update_one({'_id': doc['_id']}, {'$set': {'removal.re_verified': verified}, '$push': {'history': {'at': now(), 'by': 'shield.register', 'change': 'removal re-verified at the crossing: ' + ('clean' if verified['clean'] else 'NOT clean')}}})
    return coll.find_one({'_id': doc['_id']}, {'_id': 0})


def set_enforcement(tenant, actor, name, enforcement):
    if enforcement not in ENFORCEMENT: raise ValueError('enforcement must be enforced|advisory')
    res = db().shield_register.update_many({'tenant_id': tenant, 'name': name, 'status': 'active'}, {'$set': {'enforcement': enforcement}, '$push': {'history': {'at': now(), 'by': actor, 'change': f'enforcement set to {enforcement}'}}})
    if not res.matched_count: raise LookupError('No active category with that name')
    return db().shield_register.find_one({'tenant_id': tenant, 'name': name, 'status': 'active'}, {'_id': 0})


def propose(tenant, actor, text, source_ref=None, reader_findings=None):
    """Generate draft declarations from a document read INSIDE the boundary: the exact values each contextual category's cues found (the proposer's
    heuristics), the privileged values the contained reader marked that no declaration covers (`reader_findings`, WP-A4), and a contextual draft
    for passages carrying confidentiality markers that no category covered. Drafts do nothing until the DPO adopts them."""
    coll = db().shield_register; spans = classify(text, tenant, cues='propose'); drafts = []
    by_cat = defaultdict(set)
    for s in spans:
        if s['kind'] == 'contextual' and s['action'] != 'remove' and len(s['text']) >= 3 and not re.fullmatch(r'[\d.,%\s]+', s['text']): by_cat[s['category']].add(s['text'].strip())
    for cat, values in sorted(by_cat.items()):
        name = f'{cat}_values'
        existing = coll.find_one({'tenant_id': tenant, 'name': name, 'status': {'$in': ['active', 'draft']}})
        merged = sorted(set(existing.get('values') or []) | values) if existing else sorted(values)
        drafts.append({'name': name, 'kind': 'exact', 'action': 'abstract', 'enforcement': 'enforced', 'values': merged[:500], 'description': f'literal values the register found under {cat}; protected wherever they appear, with or without a cue', 'basis': f'{len(values)} value(s) classified under {cat}'})
    found = sorted({f['value'] for f in reader_findings or [] if len(f.get('value') or '') >= 3 and not re.fullmatch(r'[\d.,%\s]+', f['value'])})
    if found:
        existing = coll.find_one({'tenant_id': tenant, 'name': 'reader_privileged_values', 'status': {'$in': ['active', 'draft']}})
        merged = sorted(set(existing.get('values') or []) | set(found)) if existing else found
        drafts.append({'name': 'reader_privileged_values', 'kind': 'exact', 'action': 'abstract', 'enforcement': 'enforced', 'values': merged[:500], 'description': 'values the contained reader judged privileged that no declaration covers; adopt to protect them wherever they appear', 'basis': f'{len(found)} value(s) marked privileged by the contained reader outside every declared category'})
    covered = [(s['start'], s['end']) for s in spans]
    marked = []
    for a, b, sentence in _sentences(text):
        low = sentence.lower(); hits = [m for m in CONFIDENTIALITY_MARKERS if re.search(r'(?<![a-z])' + re.escape(m) + r'(?![a-z])', low)]
        if hits and not any(x < b and y > a for x, y in covered):
            terms = [w for w in re.findall(r"\b[a-z]{5,}\b", low) if w not in {m for m in CONFIDENTIALITY_MARKERS} and w not in {'which', 'their', 'there', 'these', 'those', 'shall', 'would', 'could', 'should', 'about', 'under', 'where', 'while', 'after', 'before'}]
            marked.append({'hits': hits, 'terms': terms[:6], 'excerpt_sha256': hashlib.sha256(sentence.encode()).hexdigest()[:16]})
    if marked:
        cues = sorted({h for m in marked for h in m['hits']} | {t for m in marked for t in m['terms'][:3]})
        drafts.append({'name': 'marked_confidential_passages', 'kind': 'contextual', 'action': 'remove', 'enforcement': 'enforced', 'cues': cues[:40], 'targets': ['SENTENCE'], 'description': 'passages the document itself marks confidential, proprietary or restricted and no category covered', 'basis': f'{len(marked)} marked passage(s) uncovered'})
    out = []
    for d in drafts:
        coll.delete_many({'tenant_id': tenant, 'name': d['name'], 'status': 'draft'})
        if coll.find_one({'tenant_id': tenant, 'name': d['name'], 'status': 'active'}) and d['kind'] != 'exact': continue
        doc = {**d, 'tenant_id': tenant, 'category_id': 'cat-' + uuid.uuid4().hex[:10], 'version': 0, 'status': 'draft', 'proposed_by': actor, 'proposed_at': now(), 'source_ref': source_ref, 'source_sha256': hashlib.sha256(text.encode()).hexdigest(),
               'history': [{'at': now(), 'by': actor, 'change': f"proposed from a document read inside the boundary: {d.pop('basis')}"}]}
        coll.insert_one(dict(doc)); doc.pop('_id', None); out.append(doc)
    return {'drafts': out, 'spans_classified': len(spans), 'marked_passages': len(marked)}


# ----------------------------------------------------------------------------- classification: exact → pattern → contextual, span-level
def _sentences(text):
    out, pos = [], 0
    for sentence in SENTENCE_SPLIT.split(text):
        start = text.find(sentence, pos); out.append((start, start + len(sentence), sentence)); pos = start + len(sentence)
    return out


def _candidates(sentence, start):
    found = []
    for m in MONEY.finditer(sentence): found.append(('MONEY', start + m.start(), start + m.end(), m.group()))
    for m in PERCENT.finditer(sentence): found.append(('PERCENT', start + m.start(), start + m.end(), m.group()))
    for m in NUMBER.finditer(sentence):
        if not any(a <= start + m.start() < b for _, a, b, _ in found): found.append(('NUMBER', start + m.start(), start + m.end(), m.group()))
    for m in PROPER.finditer(sentence):
        words = m.group().split()
        # a lone capitalised word that opens a sentence or a quoted string is capitalised by position, not by being a name
        if words[0] in STOP or (len(words) == 1 and (m.start() == 0 or sentence[max(0, m.start() - 2):m.start()].strip() in ('.', '!', '?', '"', "'", ''))): continue
        if any(a <= start + m.start() < b for _, a, b, _ in found): continue
        found.append(('PROPER_NOUN', start + m.start(), start + m.end(), m.group()))
    return found


def classify(text, tenant, enforcement=None, reader_spans=None, cues='advisory'):
    """Protected spans with category, kind, enforcement scope and the cue, pattern or reader reason that fired.
    Category 1/2 (`pattern`, `exact`) are deterministic. Category 3 (`contextual`) spans come from the contained reader (`reader_spans`, WP-A4);
    cue words fire only as `advisory` receipts (default), as the draft proposer (`cues='propose'`) or not at all (`cues='off'`) — never as a
    rewrite or refusal cause. `enforcement='enforced'` restricts to the categories rewritten on every crossing."""
    if cues not in CUE_MODES: raise ValueError('cues must be advisory|propose|off')
    cats = [c for c in categories(tenant) if enforcement is None or c.get('enforcement', 'enforced') == enforcement]; spans = []
    def span(cat, start, end, value, cue): return {'start': start, 'end': end, 'text': value, 'category': cat['name'], 'kind': cat['kind'], 'action': cat['action'], 'enforcement': cat.get('enforcement', 'enforced'), 'cue': cue}
    for cat in cats:
        if cat['kind'] == 'exact':
            for v in cat.get('values') or []:
                for m in re.finditer(re.escape(v), text, flags=re.IGNORECASE): spans.append(span(cat, m.start(), m.end(), m.group(), 'literal value'))
        elif cat['kind'] == 'pattern':
            for p in cat.get('patterns') or []:
                for m in re.finditer(p, text):
                    if m.group().strip(): spans.append(span(cat, m.start(), m.end(), m.group(), p[:40]))
    names = {c['name'] for c in cats}
    for s in reader_spans or []:
        if s['category'] in names or s['category'] == 'indirect_disclosure': spans.append({**s, 'source': RECOGNISER})
    if cues != 'off':
        for s in _cue_spans(text, cats):
            spans.append({**s, 'enforcement': 'advisory', 'proposer': True} if cues == 'advisory' else s)
    spans.sort(key=lambda s: (s['start'], -(s['end'] - s['start'])))
    merged = []
    for s in spans:
        if merged and s['start'] < merged[-1]['end']:
            if merged[-1].get('proposer') and not s.get('proposer'):
                # a cue (proposer) span never absorbs a declared/reader span: the real span takes the slot, the cue rides along as a receipt
                merged[-1] = {**s, 'also': (merged[-1].get('also') or []) + [merged[-1]['category']]}; continue
            if s.get('proposer'):
                merged[-1].setdefault('also', []).append(s['category']); continue
            if s['action'] == 'remove' and merged[-1]['action'] != 'remove' and s['enforcement'] == 'enforced': merged[-1]['action'] = 'remove'
            if s['enforcement'] == 'enforced': merged[-1]['enforcement'] = 'enforced'
            if s['end'] > merged[-1]['end'] and s['enforcement'] == 'enforced': merged[-1]['end'] = s['end']; merged[-1]['text'] = text[merged[-1]['start']:s['end']]
            merged[-1].setdefault('also', []).append(s['category']); continue
        merged.append(s)
    return merged


def _cue_spans(text, cats):
    """Cue-word detection for contextual categories — the proposer's heuristics (RC-2: regex is not reasoning)."""
    out = []
    def span(cat, start, end, value, cue): return {'start': start, 'end': end, 'text': value, 'category': cat['name'], 'kind': cat['kind'], 'action': cat['action'], 'enforcement': cat.get('enforcement', 'enforced'), 'cue': cue, 'source': 'cue'}
    for s_start, s_end, sentence in _sentences(text):
        low = sentence.lower()
        active = [(c, [cue for cue in c.get('cues') or [] if cue in low]) for c in cats if c['kind'] == 'contextual']
        active = [(c, cues) for c, cues in active if cues]
        if not active: continue
        cands = _candidates(sentence, s_start)
        for cat, cues in active:
            targets = set(cat.get('targets') or [])
            if 'SENTENCE' in targets and len(cues) >= 2:
                out.append(span(cat, s_start, s_end, sentence, ', '.join(cues[:4]))); continue
            for label, a, b, value in cands:
                if label in targets or (label == 'PROPER_NOUN' and {'PERSON', 'ORG'} & targets):
                    out.append(span(cat, a, b, value, ', '.join(cues[:3])))
    return out


def _placeholder(span, counters):
    base = span['category'][:-7] if span['category'].endswith('_values') else span['category']
    kind = {'client_identity': 'PARTY', 'private_project_name': 'PROJECT', 'credentials': 'CREDENTIAL', 'commercial_terms': 'FIGURE', 'unpublished_pricing_method': 'METHOD', 'personal_data': 'CONTACT', 'dates_and_deadlines': 'DATE'}.get(base, re.sub(r'[^A-Z0-9]+', '_', base.upper()).strip('_') or 'PROTECTED')
    counters[kind] += 1
    hint = {'FIGURE': 'a negotiated figure', 'PARTY': 'a named party', 'PROJECT': 'an internal project name', 'DATE': 'a date', 'CONTACT': 'a direct identifier', 'METHOD': 'a protected calculation', 'CREDENTIAL': 'a credential'}.get(kind, 'protected')
    return f'[{kind}_{counters[kind]}]', hint


def reconstruct(text, tenant, mode='abstract', reader_spans=None):
    """Shield reconstruction: protected spans become typed placeholders (abstract) or are dropped (remove); the binding map never leaves the tenant.
    Category-3 spans come from the contained reader (`reader_spans`); cue words are receipted only. Returns the safe text, the binding map, the
    categories applied and the joint-disclosure check."""
    spans = [s for s in classify(text, tenant, reader_spans=reader_spans) if not s.get('proposer')]
    cue_only = [s for s in classify(text, tenant, reader_spans=reader_spans) if s.get('proposer')]
    counters = defaultdict(int); out, pos, bindings, applied = [], 0, {}, defaultdict(int)
    for s in spans:
        out.append(text[pos:s['start']]); applied[s['category']] += 1
        if s['action'] == 'remove' or mode == 'remove':
            kind = 'METHOD' if s['category'] == 'unpublished_pricing_method' else 'DISCLOSURE' if s['category'] == 'indirect_disclosure' else 'REDACTED'
            out.append(f'[{kind}_WITHHELD]')
        else:
            token, hint = _placeholder(s, counters); bindings[token] = {'value': s['text'], 'category': s['category'], 'hint': hint}; out.append(token if mode == 'abstract' else f'[{hint}]')
        pos = s['end']
    out.append(text[pos:]); safe = re.sub(r'[ \t]{2,}', ' ', ''.join(out))
    check = joint_disclosure_check(safe, text, bindings)
    if not check['passes']:
        safe = check['generalised_text']
    advisory_cues = defaultdict(int)
    for s in cue_only: advisory_cues[s['category']] += 1
    return {'safe_text': safe, 'bindings': bindings, 'categories_applied': dict(applied), 'advisory_cues': dict(advisory_cues), 'spans': [{k: v for k, v in s.items() if k != 'text'} | {'length': s['end'] - s['start']} for s in spans], 'joint_disclosure': {k: v for k, v in check.items() if k != 'generalised_text'},
            'binding_digest': hashlib.sha256(''.join(sorted(b['value'] for b in bindings.values())).encode()).hexdigest()}


def joint_disclosure_check(safe, original, bindings):
    """Two or more surviving quasi-identifiers in one sentence (a capitalised name plus a figure, or two proper nouns) can still point at the party: generalise them."""
    issues, generalised = [], safe
    for a, b, sentence in _sentences(safe):
        if '[' in sentence and ']' in sentence: residual = [c for c in _candidates(sentence, 0) if c[0] in ('PROPER_NOUN', 'MONEY')]
        else: residual = [c for c in _candidates(sentence, 0) if c[0] in ('PROPER_NOUN', 'MONEY')]
        kinds = {c[0] for c in residual}
        if len(residual) >= 2 and ('MONEY' in kinds or sum(1 for c in residual if c[0] == 'PROPER_NOUN') >= 2):
            issues.append({'sentence_excerpt_sha256': hashlib.sha256(sentence.encode()).hexdigest()[:16], 'residual': [c[0] for c in residual]})
            for label, _, _, value in residual: generalised = generalised.replace(value, '[a named entity]' if label == 'PROPER_NOUN' else '[a figure]')
    leaked = [t for t, b in bindings.items() if b['value'].lower() in safe.lower()]
    return {'passes': not issues and not leaked, 'residual_quasi_identifier_groups': issues, 'bound_values_present_in_safe_text': leaked, 'generalised_text': generalised}


def inspect_outbound(payload_text, protected_values):
    """Egress inspection for ANY outbound message: literal values, digit-run variants and lower-cased forms of protected values must be absent.
    A purely alphabetic value counts only where it stands as a word (letters on neither side): the rewrite places placeholders at word
    boundaries, so 'one' inside 'none' or 'review' inside 'reviewer' is not a surviving value; 'qwen' inside 'qwen3' still is."""
    low = payload_text.lower(); hits = []
    compact = re.sub(r'[^0-9a-z]', '', low)
    for v in protected_values:
        if not v or len(v.strip()) < 3: continue
        if v.strip().isalpha():
            if re.search(r'(?<![a-z])' + re.escape(v.strip().lower()) + r'(?![a-z])', low): hits.append(v[:40])
            continue
        forms = {v.lower(), re.sub(r'[^0-9a-z]', '', v.lower())}
        digits = re.sub(r'\D', '', v)
        if len(digits) >= 5: forms.add(digits)
        if any(f and (f in low or f in compact) for f in forms): hits.append(v[:40])
    return {'clean': not hits, 'protected_values_found': hits, 'checked': len([v for v in protected_values if v and len(v.strip()) >= 3])}
