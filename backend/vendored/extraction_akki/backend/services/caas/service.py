"""Context-as-a-Service (Mα MA-27 / MA-28). An external customer application is admitted as a client, licensed for named context products under a
purpose and immutable terms, and calls with its own key. It receives governed, derived context — aggregates and authored deliverables — never a
raw-estate copy; the frontier planner sees only the licensed aggregates and the client's brief (Shield chokepoint, Mode B). Every delivery is
metered before it is returned (DAP-21), remembered only within the client's own licence scope, and revocation stops future access, derived
use and the client's memory at once. Tenant-scoped to the licensing estate."""
import hashlib
import json
import logging
import re
import secrets
import uuid

from services.training_lab import store as lab

log = logging.getLogger(__name__)
PURPOSE = 'caas.domain_deliverable'
PRODUCTS = {
    'estate.language_inventory': {'kind': 'aggregate', 'title': 'Language inventory of the licensed audio estate', 'unit': 'delivery',
                                  'deliverable': 'per-language files, hours, speech/music shares, model confidence and abstention — model readings on the authorised staged corpus, not human labels'},
    'estate.content_forecast': {'kind': 'aggregate', 'title': 'Whole-estate content forecast', 'unit': 'delivery',
                                'deliverable': 'estate-level hours (speech/music) with 95% intervals by store and basis — the Monte Carlo forecast as released, aggregates only'},
    'brand.mention_inventory': {'kind': 'aggregate', 'title': 'Brand mention inventory (radio corpus)', 'unit': 'delivery',
                                'deliverable': 'how often each catalogue brand is heard per language in the training corpus (segment counts by split); no transcripts, no timestamps'},
    'domain.marketing_brief': {'kind': 'authored', 'title': 'Marketing brief', 'unit': 'delivery', 'sections': ['objective', 'audience', 'channel_rationale', 'language_mix', 'key_messages', 'measurement_plan', 'risks'],
                               'deliverable': 'a decision-ready marketing brief grounded in the licensed aggregates'},
    'domain.media_plan': {'kind': 'authored', 'title': 'Media plan', 'unit': 'delivery', 'sections': ['objective', 'station_language_allocation', 'dayparts', 'flighting', 'budget_split', 'kpis', 'assumptions'],
                          'deliverable': 'a radio media plan whose allocation reasons from the licensed language and brand aggregates'},
    'domain.campaign_strategy': {'kind': 'authored', 'title': 'Campaign strategy', 'unit': 'delivery', 'sections': ['situation', 'strategic_choice', 'phases', 'creative_direction', 'competitive_context', 'success_metrics', 'open_questions'],
                                 'deliverable': 'a campaign strategy for the client brand in the licensed languages'},
    'domain.content_mining': {'kind': 'authored', 'title': 'Content mining brief', 'unit': 'delivery', 'sections': ['content_opportunities', 'language_coverage', 'formats', 'rights_and_custody_notes', 'production_steps', 'acceptance_checks'],
                              'deliverable': 'what content can be mined from the licensed estate for creation, by language and format, within custody rules'},
}
CLIENT_STATUSES = ('active', 'suspended', 'revoked')


def db():
    database = lab.db()
    database.caas_clients.create_index([('tenant_id', 1), ('client_id', 1)], unique=True)
    database.caas_licences.create_index([('tenant_id', 1), ('licence_id', 1)], unique=True)
    database.caas_keys.create_index('key_hash', unique=True)
    database.caas_keys.create_index([('tenant_id', 1), ('key_id', 1)], unique=True)
    database.caas_deliveries.create_index([('tenant_id', 1), ('client_id', 1), ('at', -1)])
    database.caas_meter.create_index([('tenant_id', 1), ('licence_id', 1), ('at', -1)])
    database.caas_memory.create_index([('tenant_id', 1), ('licence_id', 1)], unique=True)
    return database


def now():
    return lab.now()


def _hash(secret):
    return hashlib.sha256(secret.encode()).hexdigest()


# ----------------------------------------------------------------------------- clients, licences, keys (licensor side)
def admit_client(tenant, actor, body):
    client_id = 'cl-' + uuid.uuid4().hex[:10]
    doc = {'client_id': client_id, 'tenant_id': tenant, 'name': body['name'], 'application': body['application'], 'contact': body.get('contact'), 'status': 'active', 'admitted_by': actor, 'admitted_at': now(),
           'lifecycle': [{'at': now(), 'action': 'admitted', 'by': actor, 'note': body.get('note')}]}
    db().caas_clients.insert_one(dict(doc)); return doc


def list_clients(tenant):
    return list(db().caas_clients.find({'tenant_id': tenant}, {'_id': 0}, sort=[('admitted_at', -1)]))


def client(tenant, client_id):
    doc = db().caas_clients.find_one({'tenant_id': tenant, 'client_id': client_id}, {'_id': 0})
    if doc:
        doc['licences'] = list(db().caas_licences.find({'tenant_id': tenant, 'client_id': client_id}, {'_id': 0}, sort=[('issued_at', -1)]))
        doc['keys'] = list(db().caas_keys.find({'tenant_id': tenant, 'client_id': client_id}, {'_id': 0, 'key_hash': 0}, sort=[('issued_at', -1)]))
        doc['deliveries'] = db().caas_deliveries.count_documents({'tenant_id': tenant, 'client_id': client_id})
    return doc


def grant_licence(tenant, actor, client_id, body):
    """Terms are frozen at grant; a change of purpose or scope is a NEW licence (ENT-7: prospective only, receipts keep their terms identifier)."""
    cl = db().caas_clients.find_one({'tenant_id': tenant, 'client_id': client_id})
    if not cl: raise LookupError('No client with that identity in this estate')
    if cl['status'] != 'active': raise ValueError(f"A client that is {cl['status']} cannot be licensed")
    unknown = [p for p in body['products'] if p not in PRODUCTS]
    if unknown: raise ValueError('Unknown context products: ' + ', '.join(unknown))
    terms = {'purpose': body['purpose'], 'products': sorted(set(body['products'])), 'allowance': {'deliveries_per_period': int(body.get('deliveries_per_period', 100)), 'period': body.get('period', 'month')},
             'estate_custody': 'raw estate stays under estate custody; the client receives derived, governed context only', 'frontier_exposure': 'Mode B — licensed aggregates and the client brief only; privileged originals never leave',
             'memory': 'per-licence; frozen and unserved on revocation', 'withdrawal': 'revocation stops future access and derived use immediately; receipts already issued keep their terms identifier'}
    terms_identifier = 'terms-' + hashlib.sha256(json.dumps(terms, sort_keys=True).encode()).hexdigest()[:16]
    doc = {'licence_id': 'lic-' + uuid.uuid4().hex[:10], 'tenant_id': tenant, 'client_id': client_id, 'status': 'active', 'terms': terms, 'terms_identifier': terms_identifier, 'issued_by': actor, 'issued_at': now(),
           'supersedes': body.get('supersedes'), 'lifecycle': [{'at': now(), 'action': 'granted', 'by': actor}]}
    if body.get('supersedes'):
        prev = db().caas_licences.find_one({'tenant_id': tenant, 'licence_id': body['supersedes'], 'client_id': client_id})
        if not prev: raise LookupError('The licence to supersede is not on record for this client')
        if prev['status'] == 'active': _retire_licence(tenant, actor, prev['licence_id'], 'superseded', f"superseded by {doc['licence_id']}")
    db().caas_licences.insert_one(dict(doc)); return doc


def _retire_licence(tenant, actor, licence_id, status, reason):
    db().caas_licences.update_one({'tenant_id': tenant, 'licence_id': licence_id}, {'$set': {'status': status, 'retired_at': now(), 'retired_reason': reason}, '$push': {'lifecycle': {'at': now(), 'action': status, 'by': actor, 'note': reason}}})
    db().caas_keys.update_many({'tenant_id': tenant, 'licence_id': licence_id, 'status': 'active'}, {'$set': {'status': 'revoked', 'revoked_at': now(), 'revoked_reason': f'licence {status}: {reason}'}})
    db().caas_memory.update_one({'tenant_id': tenant, 'licence_id': licence_id}, {'$set': {'frozen': True, 'frozen_at': now(), 'frozen_reason': f'licence {status}'}})


def revoke_licence(tenant, actor, licence_id, reason):
    lic = db().caas_licences.find_one({'tenant_id': tenant, 'licence_id': licence_id})
    if not lic: raise LookupError('No licence with that identity in this estate')
    if lic['status'] != 'active': raise ValueError(f"Licence is already {lic['status']}")
    _retire_licence(tenant, actor, licence_id, 'revoked', reason)
    return db().caas_licences.find_one({'tenant_id': tenant, 'licence_id': licence_id}, {'_id': 0})


def transition_client(tenant, actor, client_id, action, note=None):
    cl = db().caas_clients.find_one({'tenant_id': tenant, 'client_id': client_id})
    if not cl: raise LookupError('No client with that identity in this estate')
    target = {'suspend': 'suspended', 'reinstate': 'active', 'revoke': 'revoked'}[action]
    if cl['status'] == 'revoked': raise ValueError('A revoked client cannot change state; admit a new client identity')
    db().caas_clients.update_one({'tenant_id': tenant, 'client_id': client_id}, {'$set': {'status': target}, '$push': {'lifecycle': {'at': now(), 'action': action, 'by': actor, 'note': note}}})
    if action == 'revoke':
        for lic in db().caas_licences.find({'tenant_id': tenant, 'client_id': client_id, 'status': 'active'}): _retire_licence(tenant, actor, lic['licence_id'], 'revoked', note or 'client revoked')
    return client(tenant, client_id)


def issue_key(tenant, actor, licence_id):
    """One secret, shown once. Stored as a hash; bound to one licence and therefore one client, purpose and product set."""
    lic = db().caas_licences.find_one({'tenant_id': tenant, 'licence_id': licence_id})
    if not lic: raise LookupError('No licence with that identity in this estate')
    if lic['status'] != 'active': raise ValueError(f"Licence is {lic['status']}; no key can be issued under it")
    secret = 'caas_' + secrets.token_urlsafe(32)
    doc = {'key_id': 'key-' + uuid.uuid4().hex[:10], 'tenant_id': tenant, 'client_id': lic['client_id'], 'licence_id': licence_id, 'key_hash': _hash(secret), 'status': 'active', 'issued_by': actor, 'issued_at': now(), 'last_used_at': None, 'uses': 0}
    db().caas_keys.insert_one(dict(doc))
    return {k: v for k, v in doc.items() if k != 'key_hash'}, secret


def revoke_key(tenant, actor, key_id, reason):
    res = db().caas_keys.update_one({'tenant_id': tenant, 'key_id': key_id, 'status': 'active'}, {'$set': {'status': 'revoked', 'revoked_at': now(), 'revoked_by': actor, 'revoked_reason': reason}})
    if not res.matched_count: raise LookupError('No active key with that identity in this estate')
    return db().caas_keys.find_one({'tenant_id': tenant, 'key_id': key_id}, {'_id': 0, 'key_hash': 0})


# ----------------------------------------------------------------------------- client side: resolve key → licence → product; refuse on any broken link
class Refused(Exception):
    def __init__(self, code, text): super().__init__(text); self.code = code; self.text = text


def resolve(secret):
    if not secret or not secret.startswith('caas_'): raise Refused(401, 'A client key is required')
    key = db().caas_keys.find_one({'key_hash': _hash(secret)})
    if not key or key['status'] != 'active': raise Refused(401, 'Key is not active')
    lic = db().caas_licences.find_one({'tenant_id': key['tenant_id'], 'licence_id': key['licence_id']})
    cl = db().caas_clients.find_one({'tenant_id': key['tenant_id'], 'client_id': key['client_id']})
    if not lic or lic['status'] != 'active': raise Refused(403, f"Licence is {(lic or {}).get('status', 'missing')}; access withdrawn")
    if not cl or cl['status'] != 'active': raise Refused(403, f"Client is {(cl or {}).get('status', 'missing')}")
    period = _period(lic['terms']['allowance']['period'])
    used = db().caas_meter.count_documents({'tenant_id': key['tenant_id'], 'licence_id': lic['licence_id'], 'period': period})
    if used >= lic['terms']['allowance']['deliveries_per_period']: raise Refused(429, f"Allowance of {lic['terms']['allowance']['deliveries_per_period']} deliveries per {lic['terms']['allowance']['period']} is used")
    return key, lic, cl


def _period(kind):
    import datetime
    d = datetime.datetime.now(datetime.timezone.utc)
    return d.strftime('%Y-%m') if kind == 'month' else d.strftime('%Y-%m-%d')


# ----------------------------------------------------------------------------- context products: aggregates derived from native records (no raw rows leave)
def _language_inventory(tenant):
    from services.training_lab import estate_language
    per = {}
    for doc, rows in estate_language.completed(tenant, 'audio'):
        for r in rows:
            lang = r.get('top_language') or r.get('language') or 'unknown'
            p = per.setdefault(lang, {'files': 0, 'hours': 0.0, 'speech_windows': 0, 'music_windows': 0, 'windows': 0, 'confidence_sum': 0.0, 'abstained': 0})
            p['files'] += 1; p['hours'] += (r.get('duration_s') or 0) / 3600; p['speech_windows'] += r.get('speech_windows') or 0; p['music_windows'] += r.get('music_windows') or 0
            p['windows'] += r.get('windows_read') or 0; p['confidence_sum'] += r.get('mean_confidence') or 0; p['abstained'] += r.get('abstained') or 0
    out = {}
    for lang, p in sorted(per.items(), key=lambda kv: -kv[1]['hours']):
        out[lang] = {'files': p['files'], 'hours': round(p['hours'], 2), 'speech_share': round(p['speech_windows'] / p['windows'], 4) if p['windows'] else None, 'music_share': round(p['music_windows'] / p['windows'], 4) if p['windows'] else None,
                     'mean_confidence': round(p['confidence_sum'] / p['files'], 4) if p['files'] else None, 'abstention_share': round(p['abstained'] / p['windows'], 4) if p['windows'] else None}
    return {'by_language': out, 'files_total': sum(p['files'] for p in per.values()), 'hours_total': round(sum(p['hours'] for p in per.values()), 2),
            'evidence_class': 'model readings on the authorised staged corpus; not human labels; not the whole estate', 'source': 'training_lab.estate_language (audio readings)'}


def _content_forecast(tenant):
    from services.census_autonomy import estate_intelligence_report as eir
    report = eir.latest_report(cached_only=True) or {}
    fc = ((report.get('stores') or {}).get('content_forecast')) or {}
    if not fc: return {'available': False, 'reason': 'no cached estate forecast; the census report has not been read in this process yet'}
    keep = {k: fc.get(k) for k in ('estate', 'by_store', 'by_basis', 'method') if k in fc}
    keep['folders_top'] = [{k: f.get(k) for k in ('store', 'bucket', 'hours_est', 'hours_lo', 'hours_hi', 'basis')} for f in (fc.get('folders') or [])[:15]]
    return {**keep, 'evidence_class': 'Monte Carlo forecast over listed strata; measured share stated in method', 'source': 'census_autonomy.estate_forecast'}


def _brand_inventory(tenant):
    from services.training_lab import malpha
    relabel = next((j for j in reversed(malpha.jobs(phase='malpha_aip_relabel', status='completed')) if (j.get('result') or {}).get('brand_inventory')), None)
    if relabel: inv, version = relabel['result']['brand_inventory'], relabel['result'].get('lexicon_version')
    else:
        build = next((j for j in malpha.jobs(phase='malpha_aip_build', status='completed')), None)
        if not build: return {'available': False, 'reason': 'audio database not built yet'}
        inv, version = build['result']['brand_inventory'], 1
    out = {lang: sorted([{'brand': b, 'segments': sum(c.values()), 'train': c.get('train', 0), 'dev': c.get('dev', 0), 'admission': c.get('admission', 0)} for b, c in brands.items()], key=lambda d: -d['segments'])[:60] for lang, brands in inv.items()}
    return {'by_language': out, 'lexicon_version': version, 'evidence_class': 'exact alias matches on corpus transcripts (segment counts); recognition quality is measured separately by the listener model', 'source': 'malpha audio database brand inventory'}


AGGREGATES = {'estate.language_inventory': _language_inventory, 'estate.content_forecast': _content_forecast, 'brand.mention_inventory': _brand_inventory}


def _numbers(obj):
    """Figures in a JSON payload, normalised numerically (0.8740 ≡ 0.874); clock times such as 06:00 are not figures."""
    found = set()
    text = re.sub(r'\b\d{1,2}:\d{2}(?::\d{2})?\b', ' ', json.dumps(obj, default=str))
    for m in re.finditer(r'(?<![\w.])\d+(?:[.,]\d+)?(?![\w.])', text):
        try: found.add(repr(float(m.group(0).replace(',', ''))))
        except ValueError: continue
    return found


def accept(product, deliverable, context):
    """Acceptance for authored deliverables: every required section present and non-empty; every number in the text appears in the licensed context or the brief (no invented figures)."""
    spec = PRODUCTS[product]; findings = []
    if not isinstance(deliverable, dict): return {'accepted': False, 'findings': ['deliverable is not a JSON object']}
    for s in spec['sections']:
        v = deliverable.get(s)
        if v in (None, '', [], {}): findings.append(f'section missing or empty: {s}')
    extra = _numbers(deliverable) - _numbers(context) - {repr(float(i)) for i in range(0, 101)}
    if extra: findings.append('figures not present in the licensed context or brief: ' + ', '.join(sorted(x.rstrip('0').rstrip('.') if '.' in x else x for x in extra)[:12]))
    return {'accepted': not findings, 'findings': findings, 'sections_required': spec['sections']}


async def author(product, brief, context, tenant, actor, session):
    from services.chokepoint.llm import invoke
    from services.chokepoint.model_roles import resolve as role
    planner = role('planner'); spec = PRODUCTS[product]
    from services.synisense.shield import stage
    system = ('You produce a ' + spec['title'] + ' for a radio advertiser. Answer as strict JSON with exactly these top-level keys: ' + ', '.join(spec['sections']) +
              '. Each value is a short British-English paragraph or a list of short items. Use ONLY the figures given in context; if a figure is not given, say so rather than estimate. '
              'Never name an individual presenter or quote any recording. Answer with the JSON object only.')
    # WP-A5: File 1 = the brief and required sections; File 2 = the licensed context — sealed by the Shield stage, one query
    artifact = await stage.stage(question=json.dumps({'brief': brief, 'required_sections': spec['sections']}, default=str), data=json.dumps({'licensed_context': context}, default=str), tenant_id=tenant, purpose=PURPOSE, actor=actor, system_message=system, session_id=session)
    response = await invoke(purpose=PURPOSE, safe_artifact=artifact, masking_tier='llm_prompt_governed_text', actor=actor, model=planner['model'], provider=planner['connection'], tenant_id=tenant, custody_class='tenant_estate', session_id=session)
    raw = response.text.strip()
    if raw.startswith('```'): raw = raw.split('\n', 1)[1].rsplit('```', 1)[0].strip()
    start, end = raw.find('{'), raw.rfind('}')
    try: deliverable = json.loads(raw[start:end + 1])
    except ValueError:
        from json_repair import repair_json
        try: deliverable = json.loads(repair_json(raw[start:end + 1]))
        except Exception: deliverable = None
    return deliverable, {'model': response.model_id, 'provider': response.provider, 'receipt_id': response.receipt_id, 'tokens_in': response.tokens_in, 'tokens_out': response.tokens_out, 'latency_ms': response.latency_ms}


def _meter(tenant, key, lic, product, units, delivery_id):
    """DAP-21 write-before-return: the metered event exists before the client sees the result. The rate in force at delivery time is frozen on the row."""
    from services.cost_ledger.rates import rate_for_caas_product
    rate = rate_for_caas_product(product) or {}
    per = float(rate['rate_per_delivery']) if rate.get('rate_per_delivery') else None
    row = {'meter_id': 'mtr-' + uuid.uuid4().hex[:10], 'tenant_id': tenant, 'client_id': key['client_id'], 'licence_id': lic['licence_id'], 'key_id': key['key_id'], 'terms_identifier': lic['terms_identifier'], 'operation_type': f'caas.{product}',
           'accessed_scope': product, 'quantity': units, 'quantity_unit': PRODUCTS[product]['unit'], 'period': _period(lic['terms']['allowance']['period']), 'delivery_id': delivery_id, 'at': now(), 'rate_usd': per, 'cost_usd': round(per * units, 2) if per else None,
           'rate_note': f"owner-supplied rate ({rate.get('source')}) applied at delivery" if per else 'no governed CaaS rate card yet; usage is metered, money is not invented'}
    db().caas_meter.insert_one(dict(row)); return {k: v for k, v in row.items() if k != '_id'}


def memory(tenant, licence_id):
    return db().caas_memory.find_one({'tenant_id': tenant, 'licence_id': licence_id}, {'_id': 0})


def _remember(tenant, lic, entry):
    db().caas_memory.update_one({'tenant_id': tenant, 'licence_id': lic['licence_id']}, {'$setOnInsert': {'client_id': lic['client_id'], 'created_at': now(), 'frozen': False}, '$push': {'entries': {'$each': [entry], '$slice': -50}}, '$set': {'updated_at': now()}}, upsert=True)


async def deliver(secret, product, brief, llm_enabled=True):
    key, lic, cl = resolve(secret); tenant = key['tenant_id']
    if product not in PRODUCTS: raise Refused(404, 'Unknown context product')
    if product not in lic['terms']['products']: raise Refused(403, f"Licence {lic['licence_id']} does not cover {product}")
    spec = PRODUCTS[product]; delivery_id = 'dlv-' + uuid.uuid4().hex[:10]
    mem = memory(tenant, lic['licence_id']); prior = [e for e in ((mem or {}).get('entries') or []) if not (mem or {}).get('frozen')][-5:]
    if spec['kind'] == 'aggregate':
        result = AGGREGATES[product](tenant); authored = None; acceptance = {'accepted': True, 'findings': [], 'basis': 'deterministic aggregate from native records'}
    else:
        if not brief: raise Refused(422, 'An authored deliverable needs a brief')
        context = {'estate_language_inventory': _language_inventory(tenant), 'brand_mention_inventory': _brand_inventory(tenant), 'prior_deliveries': [{'product': p['product'], 'at': p['at'], 'summary': p.get('summary')} for p in prior]}
        if not llm_enabled: raise Refused(503, 'Authoring is disabled in this environment')
        deliverable, authored = await author(product, brief, context, tenant, f"caas:{cl['client_id']}", f"caas:{lic['licence_id']}")
        acceptance = accept(product, deliverable, {'brief': brief, 'context': context})
        result = {'deliverable': deliverable, 'acceptance': acceptance, 'context_basis': {k: v.get('source') if isinstance(v, dict) else None for k, v in context.items() if k != 'prior_deliveries'}}
    meter = _meter(tenant, key, lic, product, 1, delivery_id)
    record = {'delivery_id': delivery_id, 'tenant_id': tenant, 'client_id': cl['client_id'], 'licence_id': lic['licence_id'], 'key_id': key['key_id'], 'terms_identifier': lic['terms_identifier'], 'product': product, 'brief': brief, 'accepted': acceptance['accepted'],
              'result': result, 'authored': authored, 'meter_id': meter['meter_id'], 'at': now(), 'raw_estate_exported': False}
    db().caas_deliveries.insert_one(dict(record))
    db().caas_keys.update_one({'key_id': key['key_id']}, {'$set': {'last_used_at': now()}, '$inc': {'uses': 1}})
    _remember(tenant, lic, {'delivery_id': delivery_id, 'product': product, 'at': record['at'], 'summary': (brief or {}).get('objective') if isinstance(brief, dict) else None})
    return {k: v for k, v in record.items() if k not in ('_id', 'tenant_id')} | {'client': cl['name'], 'terms_identifier': lic['terms_identifier'], 'meter': meter}


def deliveries(tenant, client_id=None, limit=50):
    q = {'tenant_id': tenant, **({'client_id': client_id} if client_id else {})}
    return list(db().caas_deliveries.find(q, {'_id': 0, 'result': 0}, sort=[('at', -1)], limit=limit))


def delivery(tenant, delivery_id):
    return db().caas_deliveries.find_one({'tenant_id': tenant, 'delivery_id': delivery_id}, {'_id': 0})


def client_deliveries(secret, limit=20):
    key, lic, _ = resolve(secret)
    return list(db().caas_deliveries.find({'tenant_id': key['tenant_id'], 'licence_id': lic['licence_id']}, {'_id': 0, 'tenant_id': 0}, sort=[('at', -1)], limit=limit))


def metering(tenant, period=None):
    """Usage lines per client · licence · product · period. Amounts sum only rows that carried a rate when metered; unpriced rows are counted, never priced after the fact."""
    q = {'tenant_id': tenant, **({'period': period} if period else {})}
    rows = list(db().caas_meter.find(q, {'_id': 0}, sort=[('at', -1)]))
    by = {}
    for r in rows:
        k = (r['client_id'], r['licence_id'], r['terms_identifier'], r['accessed_scope'], r['period'])
        line = by.setdefault(k, {'quantity': 0, 'priced_quantity': 0, 'amount_usd': 0.0, 'rates': set()})
        line['quantity'] += r['quantity']
        if r.get('cost_usd') is not None: line['priced_quantity'] += r['quantity']; line['amount_usd'] += r['cost_usd']; line['rates'].add(r.get('rate_usd'))
    lines = [{'client_id': c, 'licence_id': l, 'terms_identifier': t, 'product': p, 'period': per, 'quantity': v['quantity'], 'unit': 'delivery', 'priced_quantity': v['priced_quantity'], 'unpriced_quantity': v['quantity'] - v['priced_quantity'],
              'rate_usd': (sorted(v['rates'])[0] if len(v['rates']) == 1 else None), 'amount_usd': round(v['amount_usd'], 2) if v['priced_quantity'] else None} for (c, l, t, p, per), v in sorted(by.items())]
    priced = [l for l in lines if l['amount_usd'] is not None]; unpriced = sum(l['unpriced_quantity'] for l in lines)
    note = ('amounts use the owner-supplied rate frozen on each metered event' + (f'; {unpriced} deliveries metered before a rate existed stay unpriced' if unpriced else '')) if priced else 'usage lines are metered and reconciled; no governed CaaS rate card yet, so no money is invented'
    return {'events': len(rows), 'lines': lines, 'cost_usd': round(sum(l['amount_usd'] for l in priced), 2) if priced else None, 'unpriced_deliveries': unpriced, 'cost_note': note, 'recent': rows[:50]}


def overview(tenant):
    clients = list_clients(tenant); lic = list(db().caas_licences.find({'tenant_id': tenant}, {'_id': 0}))
    return {'products': {k: {kk: vv for kk, vv in v.items()} for k, v in PRODUCTS.items()}, 'clients': len(clients), 'clients_by_status': {s: sum(1 for c in clients if c['status'] == s) for s in CLIENT_STATUSES},
            'licences': {'active': sum(1 for l in lic if l['status'] == 'active'), 'revoked': sum(1 for l in lic if l['status'] == 'revoked'), 'superseded': sum(1 for l in lic if l['status'] == 'superseded')},
            'deliveries': db().caas_deliveries.count_documents({'tenant_id': tenant}), 'metered_events': db().caas_meter.count_documents({'tenant_id': tenant}),
            'custody': {'raw_estate_exported': False, 'frontier_exposure': 'Mode B — licensed aggregates and client brief only', 'purpose': PURPOSE}}
