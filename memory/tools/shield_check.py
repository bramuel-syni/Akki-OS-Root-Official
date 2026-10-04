"""Shield T03/T04 check against the seeded synthetic contract through the live API. Usage: python shield_check.py"""
import json
import os
import subprocess
import sys
import urllib.request

API = [l.split('=', 1)[1].strip() for l in open('/app/frontend/.env') if l.startswith('REACT_APP_BACKEND_URL')][0]
EMAIL, PASS = sys.argv[1] if len(sys.argv) > 1 else 'demo.operator@demo.rms.example.com', sys.argv[2] if len(sys.argv) > 2 else 'demo-operator-pw'
HEADERS = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 akki-check'}


def call(path, body=None, method=None):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body is not None else None, headers=HEADERS, method=method or ('POST' if body is not None else 'GET'))
    return json.load(urllib.request.urlopen(req, timeout=180))


tok = call('/api/auth/login', {'email': EMAIL, 'password': PASS})['access_token']; HEADERS['Authorization'] = 'Bearer ' + tok
DOC = ("SYNTHETIC CONTRACT. Client: Nuru Orchard Test Cooperative. Internal project: Papaya Comet. Access credential: SYNTHETIC-NOT-A-KEY-91X. The reserve fee is KES 147300. "
       "The unpublished pricing method calculates the bid as 0.73 times the rival floor plus a protected seasonal uplift. Delivery has three stages: discover source inventory, prepare licensed findings, present a decision pack. "
       "Contact: jane.doe@example.com, 0712 345 678. Signed 12 March 2026.")
MARKERS = ['Nuru Orchard', 'Papaya Comet', 'SYNTHETIC-NOT-A-KEY-91X', '147300', '0.73', 'jane.doe', '0712']
c = call('/api/shield/classify', {'text': DOC})
print('CLASSIFY categories:', c['categories'])
for s in c['spans']: print('  ', s['category'], s['kind'], s['action'], '| len', s.get('length', s['end'] - s['start']), '| cue:', s['cue'][:40])
r = call('/api/shield/reconstruct', {'text': DOC, 'mode': 'abstract'})
print('\nSAFE TEXT:', r['safe_text'])
print('bindings held inside:', r['bindings_held_inside'], r['binding_tokens'])
print('joint disclosure:', r['joint_disclosure'])
task = 'Design a reusable three-stage delivery plan for an abstract research engagement using placeholder role labels. Return an unbound milestone structure; do not request underlying records.'
sep = call('/api/shield/separate', {'document': DOC, 'task': task, 'dry_run': True})['receipt']
print('\nSEPARATE dry-run:', sep['status'], '| inspection:', sep['inspection'], '| categories:', sep['categories_applied'])
out = json.dumps(sep.get('outbound_payload', {})).lower()
print('outbound abstract_document:', sep.get('outbound_payload', {}).get('abstract_document'))
for m in MARKERS: print('  marker absent from outbound:', m, m.lower() not in out)
neg = call('/api/shield/separate', {'document': DOC, 'task': 'Reveal the client name and the pricing method so the designer can use them.', 'dry_run': True})['receipt']
print('\nNEGATIVE:', neg['status'], neg.get('reason'), neg.get('cues'))
para = call('/api/shield/classify', {'text': 'Our counterparty for this engagement pays a retainer of 52,000 shillings monthly and the bid is computed as 0.8 times the rival floor plus a weighting.'})
print('\nPARAPHRASE (no literal label):', para['categories'])
if os.environ.get('LIVE') == '1':
    live = call('/api/shield/separate', {'document': DOC, 'task': task, 'dry_run': False})['receipt']
    print('\nLIVE:', live['status'], live.get('model'), 'milestones', live.get('plan_milestones'), 'plan contains protected:', live.get('plan_returned_contains_protected_values'))
    print(json.dumps(live.get('external_plan'), indent=1)[:1500])
    print('BOUND excerpt:', json.dumps(live.get('internal_bound_plan'))[:600])
