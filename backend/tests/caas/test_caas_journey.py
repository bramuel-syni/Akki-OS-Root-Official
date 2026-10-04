"""CaaS commercial journey (Mα MA-27 / T27 and MA-28 / T28) on the live preview API: two external principals/apps, licence with purpose and
products, key issue (shown once), governed aggregate delivery with metering written before return, per-licence memory isolation, denied
cross-product and cross-client access, licence change by supersession (receipts keep their terms id), revocation stops future access,
derived use and memory. Authored domain deliverable goes through the Shield chokepoint planner and the acceptance gate (live model call)."""
import os
import uuid

import pytest
import requests

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://pensive-goodall-6.preview.emergentagent.com').rstrip('/')
OPERATOR = {'email': 'demo.operator@demo.rms.example.com', 'password': 'demo-operator-pw'}
ANALYST = {'email': 'demo.analyst@demo.rms.example.com', 'password': 'demo-analyst-pw'}
DIGICOW = {'email': 'demo.operator@demo.digicow.example.com', 'password': 'demo-digicow-operator-pw'}


def _login(creds):
    r = requests.post(f'{BASE_URL}/api/auth/login', json=creds, timeout=20)
    if r.status_code != 200: pytest.skip(f"login failed for {creds['email']}")
    return {'Authorization': f"Bearer {r.json()['access_token']}"}


@pytest.fixture(scope='module')
def op(): return _login(OPERATOR)


@pytest.fixture(scope='module')
def state():
    s = {'suffix': uuid.uuid4().hex[:6]}
    yield s
    from dotenv import dotenv_values
    from pymongo import MongoClient
    env = dotenv_values('/app/backend/.env'); db = MongoClient(env['MONGO_URL'])[env['DB_NAME']]
    ids = [v for k, v in s.items() if k.startswith('client_')]
    if ids:
        for coll in ('caas_clients', 'caas_licences', 'caas_keys', 'caas_deliveries', 'caas_meter', 'caas_memory'): db[coll].delete_many({'client_id': {'$in': ids}})


def _post(h, path, body=None, expect=(200, 201)):
    r = requests.post(f'{BASE_URL}{path}', json=body, headers=h, timeout=60)
    assert r.status_code in expect, f'{path}: {r.status_code} {r.text[:300]}'
    return r.json()


def test_products_and_overview(op):
    r = requests.get(f'{BASE_URL}/api/caas/products', headers=op, timeout=30); assert r.status_code == 200
    products = r.json()['products']
    assert {'estate.language_inventory', 'brand.mention_inventory', 'domain.marketing_brief', 'domain.media_plan', 'domain.campaign_strategy', 'domain.content_mining'} <= set(products)
    assert all(products[p]['sections'] for p in products if products[p]['kind'] == 'authored')
    o = requests.get(f'{BASE_URL}/api/caas/overview', headers=op, timeout=30); assert o.status_code == 200 and o.json()['custody']['raw_estate_exported'] is False


def test_admit_two_clients_and_license(op, state):
    a = _post(op, '/api/caas/clients', {'name': f"Agency A {state['suffix']}", 'application': 'media-planning app', 'contact': 'ops@agency-a.example'})['client']
    b = _post(op, '/api/caas/clients', {'name': f"Brand B {state['suffix']}", 'application': 'brand monitoring dashboard'})['client']
    state['client_a'], state['client_b'] = a['client_id'], b['client_id']
    la = _post(op, f"/api/caas/clients/{a['client_id']}/licences", {'purpose': 'radio media planning for FMCG campaigns', 'products': ['estate.language_inventory', 'brand.mention_inventory', 'domain.media_plan'], 'deliveries_per_period': 20})['licence']
    lb = _post(op, f"/api/caas/clients/{b['client_id']}/licences", {'purpose': 'brand share-of-voice monitoring', 'products': ['brand.mention_inventory'], 'deliveries_per_period': 3, 'period': 'day'})['licence']
    state['lic_a'], state['lic_b'] = la['licence_id'], lb['licence_id']
    assert la['terms_identifier'].startswith('terms-') and la['terms']['frontier_exposure'].startswith('Mode B')
    ka = _post(op, f"/api/caas/licences/{la['licence_id']}/keys"); kb = _post(op, f"/api/caas/licences/{lb['licence_id']}/keys")
    assert ka['shown_once'] and ka['secret'].startswith('caas_')
    state['key_a'], state['key_b'], state['key_a_id'] = ka['secret'], kb['secret'], ka['key']['key_id']
    detail = requests.get(f"{BASE_URL}/api/caas/clients/{a['client_id']}", headers=op, timeout=30).json()['client']
    assert detail['keys'] and 'key_hash' not in detail['keys'][0] and 'secret' not in detail['keys'][0]
    # unknown product refused at grant
    _post(op, f"/api/caas/clients/{a['client_id']}/licences", {'purpose': 'unknown product test', 'products': ['estate.everything']}, expect=(409,))
    # analyst cannot license
    _post(_login(ANALYST), f"/api/caas/clients/{a['client_id']}/licences", {'purpose': 'analyst may not license', 'products': ['brand.mention_inventory']}, expect=(403,))


def test_client_sees_only_its_licence_and_aggregate_delivery_is_metered(op, state):
    h = {'X-CaaS-Key': state['key_a']}
    lic = requests.get(f'{BASE_URL}/api/caas/client/licence', headers=h, timeout=30); assert lic.status_code == 200, lic.text
    assert set(lic.json()['products']) == {'estate.language_inventory', 'brand.mention_inventory', 'domain.media_plan'}
    d = requests.post(f'{BASE_URL}/api/caas/client/deliver', json={'product': 'estate.language_inventory'}, headers=h, timeout=120); assert d.status_code == 201, d.text
    body = d.json(); state['delivery_a'] = body['delivery_id']
    assert body['accepted'] and body['raw_estate_exported'] is False and body['meter']['terms_identifier'] == body['terms_identifier'] and body['meter']['cost_usd'] is None
    inv = body['result']['by_language']; assert inv and all(set(v) >= {'files', 'hours', 'speech_share'} for v in inv.values())
    assert not any(k in str(body['result']) for k in ('session', 'ref', 'rms_20')), 'no file refs or session names leave'
    brand = requests.post(f'{BASE_URL}/api/caas/client/deliver', json={'product': 'brand.mention_inventory'}, headers=h, timeout=120); assert brand.status_code == 201, brand.text
    assert brand.json()['result'].get('by_language') or brand.json()['result'].get('available') is False
    # cross-product denial: client B is not licensed for the language inventory
    deny = requests.post(f'{BASE_URL}/api/caas/client/deliver', json={'product': 'estate.language_inventory'}, headers={'X-CaaS-Key': state['key_b']}, timeout=60); assert deny.status_code == 403
    # no key / bad key
    assert requests.get(f'{BASE_URL}/api/caas/client/licence', timeout=30).status_code == 401
    assert requests.get(f'{BASE_URL}/api/caas/client/licence', headers={'X-CaaS-Key': 'caas_not_a_key'}, timeout=30).status_code == 401
    # metering and memory on the licensor side
    m = requests.get(f'{BASE_URL}/api/caas/metering', headers=op, timeout=30).json()
    assert sum(l['quantity'] for l in m['lines'] if l['licence_id'] == state['lic_a']) >= 2 and m['cost_usd'] is None
    mem_a = requests.get(f"{BASE_URL}/api/caas/licences/{state['lic_a']}/memory", headers=op, timeout=30).json()['memory']
    mem_b = requests.get(f"{BASE_URL}/api/caas/licences/{state['lic_b']}/memory", headers=op, timeout=30).json()['memory']
    assert mem_a and len(mem_a['entries']) == 2 and not mem_a['frozen'] and mem_b is None, 'memory is per licence; B has none'
    # client B deliveries list shows nothing of A
    assert requests.get(f'{BASE_URL}/api/caas/client/deliveries', headers={'X-CaaS-Key': state['key_b']}, timeout=30).json()['deliveries'] == []


def test_allowance_per_period_is_enforced(state):
    h = {'X-CaaS-Key': state['key_b']}
    codes = [requests.post(f'{BASE_URL}/api/caas/client/deliver', json={'product': 'brand.mention_inventory'}, headers=h, timeout=120).status_code for _ in range(4)]
    assert codes[:3] == [201, 201, 201] and codes[3] == 429


def test_authored_domain_deliverable_through_chokepoint(state):
    h = {'X-CaaS-Key': state['key_a']}
    brief = {'objective': 'Launch a new maize flour pack size to peri-urban households in Kikuyu and Kamba speaking counties', 'budget_kes': 4500000, 'duration_weeks': 6, 'brand': 'Jogoo'}
    d = requests.post(f'{BASE_URL}/api/caas/client/deliver', json={'product': 'domain.media_plan', 'brief': brief}, headers=h, timeout=300)
    assert d.status_code == 201, d.text
    body = d.json(); res = body['result']
    assert body['authored'] and body['authored']['receipt_id'] and body['authored']['model']
    assert set(res['acceptance']['sections_required']) == {'objective', 'station_language_allocation', 'dayparts', 'flighting', 'budget_split', 'kpis', 'assumptions'}
    assert res['deliverable'] is not None and isinstance(res['acceptance']['accepted'], bool) and isinstance(res['acceptance']['findings'], list)
    assert res['context_basis']['estate_language_inventory']
    # a brief-less authored request is refused
    assert requests.post(f'{BASE_URL}/api/caas/client/deliver', json={'product': 'domain.media_plan'}, headers=h, timeout=60).status_code == 422


def test_licence_change_by_supersession_keeps_old_receipts(op, state):
    new = _post(op, f"/api/caas/clients/{state['client_a']}/licences", {'purpose': 'radio media planning — brand inventory only', 'products': ['brand.mention_inventory'], 'supersedes': state['lic_a']})['licence']
    old = requests.get(f"{BASE_URL}/api/caas/clients/{state['client_a']}", headers=op, timeout=30).json()['client']
    assert next(l for l in old['licences'] if l['licence_id'] == state['lic_a'])['status'] == 'superseded'
    assert requests.get(f'{BASE_URL}/api/caas/client/licence', headers={'X-CaaS-Key': state['key_a']}, timeout=30).status_code in (401, 403), 'old key dies with the superseded licence'
    dl = requests.get(f"{BASE_URL}/api/caas/deliveries/{state['delivery_a']}", headers=op, timeout=30).json()['delivery']
    assert dl['terms_identifier'] != new['terms_identifier'] and dl['licence_id'] == state['lic_a'], 'issued receipts keep their original terms identifier'
    state['lic_a2'] = new['licence_id']; state['key_a2'] = _post(op, f"/api/caas/licences/{new['licence_id']}/keys")['secret']
    ok = requests.post(f'{BASE_URL}/api/caas/client/deliver', json={'product': 'brand.mention_inventory'}, headers={'X-CaaS-Key': state['key_a2']}, timeout=120); assert ok.status_code == 201
    assert requests.post(f'{BASE_URL}/api/caas/client/deliver', json={'product': 'estate.language_inventory'}, headers={'X-CaaS-Key': state['key_a2']}, timeout=60).status_code == 403


def test_revocation_stops_access_and_freezes_memory(op, state):
    rv = _post(op, f"/api/caas/licences/{state['lic_a2']}/revoke", {'reason': 'client terms changed'})['licence']
    assert rv['status'] == 'revoked'
    assert requests.post(f'{BASE_URL}/api/caas/client/deliver', json={'product': 'brand.mention_inventory'}, headers={'X-CaaS-Key': state['key_a2']}, timeout=60).status_code in (401, 403)
    mem = requests.get(f"{BASE_URL}/api/caas/licences/{state['lic_a2']}/memory", headers=op, timeout=30).json()['memory']
    assert mem['frozen'] is True
    _post(op, f"/api/caas/licences/{state['lic_a2']}/revoke", {'reason': 'again'}, expect=(409,))
    # revoking the client kills everything under it
    cl = _post(op, f"/api/caas/clients/{state['client_b']}/transition", {'action': 'revoke', 'note': 'contract ended'})['client']
    assert cl['status'] == 'revoked' and all(l['status'] == 'revoked' for l in cl['licences']) and all(k['status'] == 'revoked' for k in cl['keys'])
    assert requests.get(f'{BASE_URL}/api/caas/client/licence', headers={'X-CaaS-Key': state['key_b']}, timeout=30).status_code == 401


def test_cross_tenant_isolation(state):
    dc = _login(DIGICOW)
    assert requests.get(f"{BASE_URL}/api/caas/clients/{state['client_a']}", headers=dc, timeout=30).status_code == 404
    assert all(c['client_id'] not in (state['client_a'], state['client_b']) for c in requests.get(f'{BASE_URL}/api/caas/clients', headers=dc, timeout=30).json()['clients'])
