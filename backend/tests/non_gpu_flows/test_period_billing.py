"""Real bill derivation on SYNTHETIC ledger input; no customer charges created."""
import asyncio
import copy
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / 'portal_operational'))
from test_portal_unit_faults_and_entitlements import _licence_event, _membership, _metered_event
from services.portal_operational import billing


def chain():
    now = datetime.now(timezone.utc).replace(microsecond=0) - timedelta(minutes=1)
    licence = _licence_event(period_start=now-timedelta(days=1), period_end=now+timedelta(days=1), period_iso='TEST-period')
    event = _metered_event(timestamp=now, quantity=10, credit_rate=2)
    p = event['payload']
    p.update(evidence_mode='measured', principal_id='principal-1', raw_meter_hash='a'*64)
    event['row'].update(hash='b'*64, seq=3, run_id='TEST-run')
    raw = dict(row=dict(resource_type='execution_flow', hash='a'*64, seq=2, run_id='TEST-run', at={'epoch_s': int(now.timestamp())}),
        payload={'slot': 'metered', 'data': {'evidence_mode': 'measured', 'worker_receipt_ref': 'receipt-exec',
            'terms_ref': 'terms-1', 'usage': [{'unit': 'tokens', 'quantity': '10'}]}})
    dispatch = dict(row=dict(resource_type='execution_flow', hash='c'*64, seq=1, run_id='TEST-run'),
        payload={'slot': 'dispatch', 'data': {'commercial_snapshot': {'principal_id': 'principal-1',
            'licence': copy.deepcopy(licence['payload']['licence']), 'catalog_row': copy.deepcopy(p['catalog_row_at_event'])}}})
    membership = _membership()
    membership['row'].update(hash='d'*64, seq=-1, run_id='membership')
    licence['row'].update(hash='e'*64, seq=0, run_id='licence')
    return [membership, licence, dispatch, raw, event]


def read(events, monkeypatch):
    async def stored(db, query):
        assert query == {'row.tenant_id': 'DIGICOW'}
        return events
    monkeypatch.setattr(billing, 'read_events', stored)
    return asyncio.run(billing.read_invoice(object(), {'tenant_id': 'DIGICOW', 'principal_id': 'principal-1'}, 'TEST-period'))


def test_period_bill_is_reconstructible_and_does_not_rebill_on_read(monkeypatch):
    events = chain()
    before = copy.deepcopy(events)
    first = read(events, monkeypatch)
    assert first.status == 'resolved' and first.credits_total == 20
    assert first.lines[0].ledger_ref == 'b'*64
    assert first.model_dump() == read(events, monkeypatch).model_dump()
    assert events == before and first.financial_invoice_issued is False


@pytest.mark.parametrize('defect', ['mocked', 'unlabelled', 'missing_meter', 'wrong_unit', 'wrong_quantity',
    'reprice', 'wrong_owner', 'wrong_principal', 'changed_terms', 'changed_clock', 'out_of_order',
    'duplicate', 'changed_period', 'fractional_credit', 'fractional_tokens', 'paused_catalog'])
def test_unreconciled_events_hold_without_partial_totals(monkeypatch, defect):
    events = chain()
    event, raw, dispatch = events[-1], events[-2], events[-3]
    p = event['payload']
    if defect == 'mocked': p['evidence_mode'] = 'MOCKED'
    if defect == 'unlabelled': p.pop('evidence_mode')
    if defect == 'missing_meter': p['raw_meter_hash'] = 'missing'
    if defect == 'wrong_unit': p['metered_event']['quantity_unit'] = 'seconds'
    if defect == 'wrong_quantity': p['metered_event']['quantity'] = 11
    if defect == 'reprice': p['catalog_row_at_event']['credit_rate'] = 9
    if defect == 'wrong_owner': dispatch['payload']['data']['commercial_snapshot']['licence']['organisation_principal_id'] = 'other-org'
    if defect == 'wrong_principal': dispatch['payload']['data']['commercial_snapshot']['principal_id'] = 'other-seat'
    if defect == 'changed_terms': p['metered_event']['terms_id'] = 'new-terms'
    if defect == 'changed_clock': raw['row']['at']['epoch_s'] -= 1
    if defect == 'out_of_order': raw['row']['seq'] = 4
    if defect == 'duplicate': events.append(copy.deepcopy(event))
    if defect == 'changed_period':
        period = copy.deepcopy(events[1]); period['payload']['period_end'] = datetime.now(timezone.utc).isoformat(); events.append(period)
    if defect in {'fractional_credit', 'fractional_tokens'}:
        p['metered_event']['quantity'] = 1 if defect == 'fractional_credit' else 0.5
        raw['payload']['data']['usage'][0]['quantity'] = str(p['metered_event']['quantity'])
        p['catalog_row_at_event']['credit_rate'] = 0.1 if defect == 'fractional_credit' else 2
        dispatch['payload']['data']['commercial_snapshot']['catalog_row'] = copy.deepcopy(p['catalog_row_at_event'])
    if defect == 'paused_catalog':
        p['catalog_row_at_event']['status'] = 'paused'
        dispatch['payload']['data']['commercial_snapshot']['catalog_row']['status'] = 'paused'
    view = read(events, monkeypatch)
    assert view.status == 'unresolved' and view.reason_code == 'BILLING_EVIDENCE_INVALID'
    assert view.lines == [] and view.credits_total is None


def test_period_is_half_open_and_cannot_carry_previous_debit(monkeypatch):
    events = chain()
    time = events[-1]['payload']['metered_event']['timestamp_iso']
    events[1]['payload']['period_end'] = time
    view = read(events, monkeypatch)
    assert view.status == 'resolved' and view.credits_total == 0
    events[1]['payload']['period_start'] = time
    events[1]['payload']['period_end'] = (datetime.now(timezone.utc)+timedelta(days=1)).isoformat()
    assert read(events, monkeypatch).credits_total == 20


def test_billing_ignores_todays_rate_and_hides_other_seats(monkeypatch):
    events = chain()
    extra = copy.deepcopy(events[-1]); extra['payload']['metered_event']['party_id'] = 'other-seat'
    events.append(extra)
    events.append({'row': {'resource_type': 'entitlement_catalog', 'hash': 'f'*64, 'run_id': 'catalog'}, 'payload': {'credit_rate': 999}})
    view = read(events, monkeypatch)
    assert view.credits_total == 20 and len(view.lines) == 1 and view.scope == 'principal'


def test_missing_native_period_is_unknown_not_free(monkeypatch):
    events = chain(); events.pop(1)
    result = read(events, monkeypatch)
    assert result.reason_code == 'PERIOD_UNRESOLVED' and result.credits_total is None