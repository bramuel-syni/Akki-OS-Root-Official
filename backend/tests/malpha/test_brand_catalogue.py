"""Owner brand catalogue → listener lexicon (Mα MA-17 data contract). Parses the real owner workbook in custody, checks matchability rules,
mention detection under the new lexicon, dispatcher validation of the relabel/internet-corpus phases, and the live API (operator only)."""
import json
import os
import sys

import pytest
import requests

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import load_dotenv  # noqa: E402

load_dotenv('/app/backend/.env')
from services.training_lab import brand_catalogue as bc  # noqa: E402
from services.training_lab import malpha_worker as mw  # noqa: E402
from services.training_runner import m9_dispatch  # noqa: E402

WORKBOOK = '/app/backend/estate_keys/owner_20261004/Kenyan_Brand_Catalogue.xlsx'
BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://pensive-goodall-6.preview.emergentagent.com').rstrip('/')
OPERATOR = {'email': 'demo.operator@demo.rms.example.com', 'password': 'demo-operator-pw'}
ANALYST = {'email': 'demo.analyst@demo.rms.example.com', 'password': 'demo-analyst-pw'}


@pytest.fixture(scope='module')
def parsed():
    if not os.path.exists(WORKBOOK): pytest.skip('owner workbook not in custody')
    return bc.parse_workbook(WORKBOOK)


def test_workbook_sheets_and_counts(parsed):
    entries, sheets = parsed
    assert sheets == {'Product brands': 205, 'Service brands': 18, 'Products': 1465, 'Services': 1157}
    kinds = {k: sum(1 for e in entries if e['kind'] == k) for k in ('family', 'product_label', 'service_provider', 'legacy_v1')}
    assert kinds['family'] == 223 and kinds['product_label'] > 300 and kinds['service_provider'] > 30
    assert len({bc.normalise(e['brand']) for e in entries}) == len(entries), 'brand names are unique after normalisation'


def test_short_and_numeric_labels_are_excluded_not_dropped(parsed):
    entries, _ = parsed
    excluded = {e['brand']: e['excluded_reason'] for e in entries if not e['matchable']}
    assert {'58', '210', 'K9', 'LG'} <= set(excluded)
    assert all('≥3' in r for r in excluded.values())
    assert all(e['matchable_aliases'] for e in entries if e['matchable'])
    assert all(len(a) >= 3 and not a.replace(' ', '').isdigit() for e in entries for a in e['matchable_aliases'])


def test_legacy_seed_merges_into_catalogue_brands(parsed):
    entries, _ = parsed
    saf = next(e for e in entries if bc.normalise(e['brand']) == 'safaricom')
    assert saf['kind'] == 'family' and 'saf' in saf['aliases']
    coop = next(e for e in entries if 'operative bank' in bc.normalise(e['brand']))
    assert 'coop bank' in coop['aliases'] and not any(a.startswith('-') for a in coop['aliases'])
    legacy = [e for e in entries if e['kind'] == 'legacy_v1']
    assert legacy and all(e['matchable'] for e in legacy)


def test_alias_variants_spoken_forms():
    assert bc.alias_variants('Co-operative Bank of Kenya Ltd')[0] == 'co-operative bank of kenya ltd'
    assert 'cooperative bank of kenya ltd' in bc.alias_variants('Co-operative Bank of Kenya Ltd')
    assert 'co-operative bank' in bc.alias_variants('Co-operative Bank of Kenya Ltd')
    assert not any(v.endswith(' of') for v in bc.alias_variants('Co-operative Bank of Kenya Ltd'))
    assert 'procter and gamble' in bc.alias_variants('Procter & Gamble')


def test_detect_mentions_under_catalogue_lexicon(parsed):
    entries, _ = parsed
    lexicon = bc.compact(entries)
    hits = mw.detect_mentions('Leo tunazungumzia Safaricom na M-Pesa, pia Brookside maziwa', lexicon)
    assert any(bc.normalise(h) == 'safaricom' for h in hits) and any('brookside' in bc.normalise(h) for h in hits)
    assert mw.detect_mentions('tulinunua bidhaa 58 jana', lexicon) == [] or '58' not in mw.detect_mentions('tulinunua bidhaa 58 jana', lexicon)
    assert bc.lexicon_sha(lexicon) == mw.lexicon_sha(lexicon)


def test_dispatch_validates_relabel_and_internet_phases(parsed):
    entries, _ = parsed
    common = {'commission_id': 'LISTEN-KIK-KAM-SWA', 'languages': ['kik', 'kam', 'swa'], 'gpu_index': 0, 'budget_mode': 'uncapped_until_billing', 'owner_order_ref': 'x', 'seed': 1, 'iteration': 0,
              'aip_db_dir': os.environ['LANGUAGE_COGNITION_REMOTE_ROOT'] + '/malpha/aip_db_v1'}
    host = os.environ['M9_TRAINING_HOSTS'].split(',')[0].strip()
    m9_dispatch.validate('malpha_aip_relabel', {**common, 'brand_lexicon': bc.compact(entries), 'brand_lexicon_version': 2}, host)
    m9_dispatch.validate('malpha_internet_corpus', {**common, 'brand_lexicon': bc.compact(entries), 'datasets': [{'repo': 'google/fleurs', 'config': 'sw_ke', 'language': 'swa'}], 'max_hours_per_dataset': 60}, host)
    with pytest.raises(ValueError, match='MALPHA_LEXICON_INVALID'):
        m9_dispatch.validate('malpha_aip_relabel', {**common, 'brand_lexicon': [{'brand': 'X'}], 'brand_lexicon_version': 2}, host)
    with pytest.raises(ValueError, match='MALPHA_INTERNET_CORPUS_INVALID'):
        m9_dispatch.validate('malpha_internet_corpus', {**common, 'brand_lexicon': bc.compact(entries), 'datasets': [{'repo': 'not a repo', 'language': 'swa'}], 'max_hours_per_dataset': 60}, host)
    with pytest.raises(ValueError, match='MALPHA_INTERNET_CORPUS_INVALID'):
        m9_dispatch.validate('malpha_internet_corpus', {**common, 'brand_lexicon': bc.compact(entries), 'datasets': [{'repo': 'google/fleurs', 'language': 'eng'}], 'max_hours_per_dataset': 60}, host)


def _login(creds):
    r = requests.post(f'{BASE_URL}/api/auth/login', json=creds, timeout=20)
    if r.status_code != 200: pytest.skip(f"login failed for {creds['email']}")
    return {'Authorization': f"Bearer {r.json()['access_token']}"}


def test_api_lexicon_read_and_registration_is_idempotent():
    op = _login(OPERATOR)
    r = requests.get(f'{BASE_URL}/api/training/malpha/brand-lexicon', headers=op, timeout=30); assert r.status_code == 200, r.text
    body = r.json(); assert body['active']['version'] >= 2 and body['active']['brands'] > 600 and set(body['relabel_ready']) == {'akki-vm', 'akki-vm-ii'}
    with open(WORKBOOK, 'rb') as fh:
        r2 = requests.post(f'{BASE_URL}/api/training/malpha/brand-catalogue', headers=op, files={'file': ('Kenyan_Brand_Catalogue.xlsx', fh, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}, timeout=120)
    assert r2.status_code == 201, r2.text
    assert r2.json()['version'] == body['active']['version'], 'same workbook hash → same version, no new version minted'
    detail = requests.get(f"{BASE_URL}/api/training/malpha/brand-lexicon/{body['active']['version']}", headers=op, timeout=30)
    assert detail.status_code == 200 and len(detail.json()['brands']) == detail.json()['counts']['brands']
    assert requests.get(f'{BASE_URL}/api/training/malpha/brand-lexicon', headers=_login(ANALYST), timeout=30).status_code == 403
    status = requests.get(f'{BASE_URL}/api/training/malpha/status', headers=op, timeout=60); assert status.status_code == 200
    assert status.json()['brand_lexicon']['version'] == body['active']['version'] and status.json()['internet_corpus']['datasets']
    assert json.dumps(status.json()['metering'])
