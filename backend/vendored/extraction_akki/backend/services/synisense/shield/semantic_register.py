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

from services.training_lab import store as lab

KINDS = ('exact', 'pattern', 'contextual')
ACTIONS = ('remove', 'abstract', 'generalise')
ENFORCEMENT = ('enforced', 'advisory')
STATUSES = ('draft', 'active', 'superseded', 'removed')
CONFIDENTIALITY_MARKERS = ('confidential', 'trade secret', 'proprietary', 'internal only', 'not for disclosure', 'nda', 'privileged', 'restricted', 'embargo', 'siri', 'faragha')

# `enforced` categories are rewritten (or the crossing refused) on EVERY model call and rebound in the reply; `advisory` categories are
# found and receipted on every crossing but only rewritten in the confidential-document workflow — the DPO moves a category between the two.
DEFAULT_CATEGORIES = [
    {'name': 'client_identity', 'kind': 'contextual', 'action': 'abstract', 'enforcement': 'enforced', 'description': 'who the counterparty, client or partner is — names, trading names, cooperative or company identifiers',
     'cues': ['client', 'customer', 'counterparty', 'partner', 'cooperative', 'co-operative', 'ltd', 'limited', 'plc', 'company', 'between', 'party', 'licensee', 'licensor', 'supplier', 'vendor', 'tenant', 'landlord', 'mteja', 'kampuni'], 'targets': ['PERSON', 'ORG', 'PROPER_NOUN']},
    {'name': 'private_project_name', 'kind': 'contextual', 'action': 'abstract', 'enforcement': 'enforced', 'description': 'internal code names and unreleased project names', 'cues': ['project', 'codename', 'code name', 'internal', 'initiative', 'programme', 'program', 'workstream', 'mradi'], 'targets': ['PROPER_NOUN', 'ORG']},
    {'name': 'credentials', 'kind': 'pattern', 'action': 'remove', 'enforcement': 'enforced', 'description': 'keys, tokens, passwords, access credentials', 'patterns': [r'(?i)\b(?:api[-_ ]?key|secret|token|password|passcode|credential|nenosiri)s?\s*[:=]?\s*[A-Za-z0-9\-_./+]{6,}', r'\b[A-Z0-9]{3,}(?:-[A-Z0-9]{2,}){2,}\b', r'\bsk-[A-Za-z0-9]{8,}\b']},
    {'name': 'commercial_terms', 'kind': 'contextual', 'action': 'abstract', 'enforcement': 'advisory', 'description': 'fees, prices, discounts, margins, payment terms, penalties, exclusivity and other negotiated figures', 'cues': ['fee', 'price', 'pricing', 'discount', 'margin', 'rate', 'payment', 'penalty', 'royalty', 'commission', 'retainer', 'deposit', 'reserve', 'bid', 'floor', 'uplift', 'cap', 'budget', 'cost', 'salary', 'kes', 'usd', 'eur', 'gbp', 'shilling', '%', 'bei', 'ada', 'malipo', 'mshahara'], 'targets': ['MONEY', 'NUMBER', 'PERCENT']},
    {'name': 'unpublished_pricing_method', 'kind': 'contextual', 'action': 'remove', 'enforcement': 'advisory', 'description': 'how a price or bid is computed — formulas, multipliers, thresholds, seasonal adjustments', 'cues': ['method', 'formula', 'calculates', 'calculated', 'computed', 'times', 'multiplied', 'multiplier', 'plus', 'minus', 'threshold', 'coefficient', 'adjustment', 'uplift', 'weighting', 'algorithm', 'fomula', 'mara'], 'targets': ['SENTENCE']},
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
    if coll.count_documents({'tenant_id': tenant}):
        for cat in DEFAULT_CATEGORIES:
            # categories installed before enforcement scopes existed receive the default scope once; the DPO's later choice is never overwritten
            coll.update_many({'tenant_id': tenant, 'name': cat['name'], 'enforcement': {'$exists': False}}, {'$set': {'enforcement': cat['enforcement']}})
            # a default the DPO never revised tracks the shipped cue/pattern lists (multilingual cues added later); DPO-authored versions are untouched
            doc = coll.find_one({'tenant_id': tenant, 'name': cat['name'], 'status': 'active', 'authored_by': 'shield.defaults'})
            if doc and any(doc.get(k) != cat.get(k) for k in ('cues', 'patterns', 'targets', 'description')):
                coll.update_one({'_id': doc['_id']}, {'$set': {k: cat.get(k) for k in ('cues', 'patterns', 'targets', 'description')}, '$push': {'history': {'at': now(), 'by': 'shield.defaults', 'change': 'shipped default cues/patterns refreshed (never revised by the DPO)'}}})
        coll.update_many({'tenant_id': tenant, 'enforcement': {'$exists': False}}, {'$set': {'enforcement': 'enforced'}})
        return 0
    for cat in DEFAULT_CATEGORIES:
        coll.insert_one({**cat, 'tenant_id': tenant, 'category_id': 'cat-' + uuid.uuid4().hex[:10], 'version': 1, 'status': 'active', 'authored_by': 'shield.defaults', 'authored_at': now(), 'history': [{'at': now(), 'by': 'shield.defaults', 'change': 'default category installed; DPO may revise, re-scope or remove'}]})
    return len(DEFAULT_CATEGORIES)


def categories(tenant, include_removed=False, include_drafts=False):
    ensure_defaults(tenant)
    statuses = ['active'] + (['draft'] if include_drafts else []) + (['removed', 'superseded'] if include_removed else [])
    return list(db().shield_register.find({'tenant_id': tenant, 'status': {'$in': statuses}}, {'_id': 0}, sort=[('status', 1), ('name', 1)]))


def _validate(body):
    if body['kind'] not in KINDS or body['action'] not in ACTIONS: raise ValueError('kind must be exact|pattern|contextual and action remove|abstract|generalise')
    if body.get('enforcement', 'enforced') not in ENFORCEMENT: raise ValueError('enforcement must be enforced|advisory')
    if body['kind'] == 'exact' and not body.get('values'): raise ValueError('An exact category lists the literal values it protects')
    if body['kind'] == 'pattern':
        for p in body.get('patterns') or []: re.compile(p)
        if not body.get('patterns'): raise ValueError('A pattern category needs at least one regular expression')
    if body['kind'] == 'contextual' and not body.get('cues'): raise ValueError('A contextual category names the cues that signal the protected meaning')


def _fields(body):
    return {k: body.get(k) for k in ('name', 'kind', 'action', 'description', 'cues', 'targets', 'patterns', 'values')} | {'enforcement': body.get('enforcement') or 'enforced'}


def author(tenant, actor, body):
    """DPO authors or revises a category directly into force (the DPO act IS the adoption); a draft of the same name is consumed."""
    _validate(body)
    coll = db().shield_register; prior = coll.find_one({'tenant_id': tenant, 'name': body['name'], 'status': 'active'})
    version = (prior['version'] + 1) if prior else 1
    doc = _fields(body)
    doc.update(tenant_id=tenant, category_id=prior['category_id'] if prior else 'cat-' + uuid.uuid4().hex[:10], version=version, status='active', authored_by=actor, authored_at=now(),
               history=(prior.get('history') if prior else []) + [{'at': now(), 'by': actor, 'change': 'revised' if prior else 'authored', 'version': version}])
    if prior: coll.update_one({'_id': prior['_id']}, {'$set': {'status': 'superseded', 'superseded_at': now()}})
    coll.delete_many({'tenant_id': tenant, 'name': body['name'], 'status': 'draft'})
    coll.insert_one(dict(doc)); doc.pop('_id', None); return doc


def set_enforcement(tenant, actor, name, enforcement):
    if enforcement not in ENFORCEMENT: raise ValueError('enforcement must be enforced|advisory')
    res = db().shield_register.update_many({'tenant_id': tenant, 'name': name, 'status': 'active'}, {'$set': {'enforcement': enforcement}, '$push': {'history': {'at': now(), 'by': actor, 'change': f'enforcement set to {enforcement}'}}})
    if not res.matched_count: raise LookupError('No active category with that name')
    return db().shield_register.find_one({'tenant_id': tenant, 'name': name, 'status': 'active'}, {'_id': 0})


def propose(tenant, actor, text, source_ref=None):
    """Generate draft declarations from a document read INSIDE the boundary: the exact values each contextual category found (so the same value is
    protected later even without its cue), and a contextual draft for passages carrying confidentiality markers that no category covered.
    Drafts do nothing until the DPO adopts them."""
    coll = db().shield_register; spans = classify(text, tenant); drafts = []
    by_cat = defaultdict(set)
    for s in spans:
        if s['kind'] == 'contextual' and s['action'] != 'remove' and len(s['text']) >= 3 and not re.fullmatch(r'[\d.,%\s]+', s['text']): by_cat[s['category']].add(s['text'].strip())
    for cat, values in sorted(by_cat.items()):
        name = f'{cat}_values'
        existing = coll.find_one({'tenant_id': tenant, 'name': name, 'status': {'$in': ['active', 'draft']}})
        merged = sorted(set(existing.get('values') or []) | values) if existing else sorted(values)
        drafts.append({'name': name, 'kind': 'exact', 'action': 'abstract', 'enforcement': 'enforced', 'values': merged[:500], 'description': f'literal values the register found under {cat}; protected wherever they appear, with or without a cue', 'basis': f'{len(values)} value(s) classified under {cat}'})
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


def adopt(tenant, actor, name, edits=None):
    """DPO adopts a draft (optionally edited) into force; the draft's own history is retained."""
    coll = db().shield_register; draft = coll.find_one({'tenant_id': tenant, 'name': name, 'status': 'draft'})
    if not draft: raise LookupError('No draft with that name awaits adoption')
    body = {k: draft.get(k) for k in ('name', 'kind', 'action', 'description', 'cues', 'targets', 'patterns', 'values', 'enforcement')} | {k: v for k, v in (edits or {}).items() if v is not None}
    _validate(body)
    prior = coll.find_one({'tenant_id': tenant, 'name': name, 'status': 'active'})
    doc = _fields(body); version = (prior['version'] + 1) if prior else 1
    doc.update(tenant_id=tenant, category_id=prior['category_id'] if prior else draft['category_id'], version=version, status='active', authored_by=actor, authored_at=now(),
               history=((prior.get('history') if prior else []) + draft.get('history', []) + [{'at': now(), 'by': actor, 'change': 'adopted' + (' with edits' if edits else ''), 'version': version}]))
    if prior: coll.update_one({'_id': prior['_id']}, {'$set': {'status': 'superseded', 'superseded_at': now()}})
    coll.delete_one({'_id': draft['_id']}); coll.insert_one(dict(doc)); doc.pop('_id', None); return doc


def discard(tenant, actor, name):
    res = db().shield_register.delete_many({'tenant_id': tenant, 'name': name, 'status': 'draft'})
    if not res.deleted_count: raise LookupError('No draft with that name')
    return res.deleted_count


def remove(tenant, actor, name, reason):
    res = db().shield_register.update_many({'tenant_id': tenant, 'name': name, 'status': 'active'}, {'$set': {'status': 'removed', 'removed_at': now(), 'removed_by': actor, 'removal_reason': reason}, '$push': {'history': {'at': now(), 'by': actor, 'change': f'removed: {reason}'}}})
    if not res.matched_count: raise LookupError('No active category with that name')
    return res.matched_count


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
        if words[0] in STOP or (len(words) == 1 and (m.start() == 0 or sentence[max(0, m.start() - 2):m.start()].strip() in ('.', '!', '?', ''))): continue
        if any(a <= start + m.start() < b for _, a, b, _ in found): continue
        found.append(('PROPER_NOUN', start + m.start(), start + m.end(), m.group()))
    return found


def classify(text, tenant, enforcement=None):
    """Protected spans with category, kind, enforcement scope and the cue or pattern that fired. Contextual categories fire on candidates inside a
    sentence carrying their cues. `enforcement='enforced'` restricts to the categories rewritten on every crossing."""
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
    for s_start, s_end, sentence in _sentences(text):
        low = sentence.lower()
        active = [(c, [cue for cue in c.get('cues') or [] if cue in low]) for c in cats if c['kind'] == 'contextual']
        active = [(c, cues) for c, cues in active if cues]
        if not active: continue
        cands = _candidates(sentence, s_start)
        for cat, cues in active:
            targets = set(cat.get('targets') or [])
            if 'SENTENCE' in targets and len(cues) >= 2:
                spans.append(span(cat, s_start, s_end, sentence, ', '.join(cues[:4]))); continue
            for label, a, b, value in cands:
                if label in targets or (label == 'PROPER_NOUN' and {'PERSON', 'ORG'} & targets):
                    spans.append(span(cat, a, b, value, ', '.join(cues[:3])))
    spans.sort(key=lambda s: (s['start'], -(s['end'] - s['start'])))
    merged = []
    for s in spans:
        if merged and s['start'] < merged[-1]['end']:
            if s['action'] == 'remove' and merged[-1]['action'] != 'remove': merged[-1]['action'] = 'remove'
            if s['enforcement'] == 'enforced': merged[-1]['enforcement'] = 'enforced'
            if s['end'] > merged[-1]['end']: merged[-1]['end'] = s['end']; merged[-1]['text'] = text[merged[-1]['start']:s['end']]
            merged[-1].setdefault('also', []).append(s['category']); continue
        merged.append(s)
    return merged


def _placeholder(span, counters):
    base = span['category'][:-7] if span['category'].endswith('_values') else span['category']
    kind = {'client_identity': 'PARTY', 'private_project_name': 'PROJECT', 'credentials': 'CREDENTIAL', 'commercial_terms': 'FIGURE', 'unpublished_pricing_method': 'METHOD', 'personal_data': 'CONTACT', 'dates_and_deadlines': 'DATE'}.get(base, re.sub(r'[^A-Z0-9]+', '_', base.upper()).strip('_') or 'PROTECTED')
    counters[kind] += 1
    hint = {'FIGURE': 'a negotiated figure', 'PARTY': 'a named party', 'PROJECT': 'an internal project name', 'DATE': 'a date', 'CONTACT': 'a direct identifier', 'METHOD': 'a protected calculation', 'CREDENTIAL': 'a credential'}.get(kind, 'protected')
    return f'[{kind}_{counters[kind]}]', hint


def reconstruct(text, tenant, mode='abstract'):
    """Shield reconstruction: protected spans become typed placeholders (abstract) or are dropped (remove); the binding map never leaves the tenant.
    Returns the safe text, the binding map, the categories applied and the joint-disclosure check."""
    spans = classify(text, tenant); counters = defaultdict(int); out, pos, bindings, applied = [], 0, {}, defaultdict(int)
    for s in spans:
        out.append(text[pos:s['start']]); applied[s['category']] += 1
        if s['action'] == 'remove' or mode == 'remove':
            kind = 'METHOD' if s['category'] == 'unpublished_pricing_method' else 'REDACTED'
            out.append(f'[{kind}_WITHHELD]')
        else:
            token, hint = _placeholder(s, counters); bindings[token] = {'value': s['text'], 'category': s['category'], 'hint': hint}; out.append(token if mode == 'abstract' else f'[{hint}]')
        pos = s['end']
    out.append(text[pos:]); safe = re.sub(r'[ \t]{2,}', ' ', ''.join(out))
    check = joint_disclosure_check(safe, text, bindings)
    if not check['passes']:
        safe = check['generalised_text']
    return {'safe_text': safe, 'bindings': bindings, 'categories_applied': dict(applied), 'spans': [{k: v for k, v in s.items() if k != 'text'} | {'length': s['end'] - s['start']} for s in spans], 'joint_disclosure': {k: v for k, v in check.items() if k != 'generalised_text'},
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
    """Egress inspection for ANY outbound message: literal values, digit-run variants and lower-cased forms of protected values must be absent."""
    low = payload_text.lower(); hits = []
    for v in protected_values:
        if not v or len(v.strip()) < 3: continue
        forms = {v.lower(), re.sub(r'[^0-9a-z]', '', v.lower())}
        digits = re.sub(r'\D', '', v)
        if len(digits) >= 5: forms.add(digits)
        compact = re.sub(r'[^0-9a-z]', '', low)
        if any(f and (f in low or f in compact) for f in forms): hits.append(v[:40])
    return {'clean': not hits, 'protected_values_found': hits, 'checked': len([v for v in protected_values if v and len(v.strip()) >= 3])}
