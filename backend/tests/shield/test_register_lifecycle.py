"""WP-A1 — confidentiality register lifecycle to canon (Doc 2 A4 B24–B31, A5.1 B34, A5.4 B37–B39, A5.5 B40, A6 B42–B45).

Unit against the live register store on a scratch tenant (removed at module end): adopt/author land `pending` and a pending declaration
never affects a crossing; `approve` is the gate to enforcement; revisions stay pending until approved and supersede on approval; removal is
a counter-signed countdown ceremony (C3 default 48 h) that can be cancelled, exposes nothing until applied and is re-verified; nothing is
deleted from the record. Catalogue parity: the old tenant catalogue lives in the register and the de-identifier's lookup reads that one set.
Vault intake: 1,000 SYNTHETIC rows → pending declarations with invalid/duplicate rows reported and reach stated over measured material only.
All values are SYNTHETIC."""
import asyncio
import csv
import io
import re
import sys
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')

from services.rules_service import ceremony  # noqa: E402
from services.synisense.shield import register_vault, semantic_register as reg, tenant_entities  # noqa: E402

TENANT = f'test-a1-{uuid.uuid4().hex[:8]}'
DPO1, DPO2 = 'test:dpo-one', 'test:dpo-two'
CODENAMES = {'name': 'secret_codenames', 'kind': 'exact', 'action': 'abstract', 'enforcement': 'enforced', 'description': 'SYNTHETIC unreleased code names', 'values': ['Papaya Comet']}


@pytest.fixture(scope='module', autouse=True)
def scratch_tenant():
    yield
    reg.db().shield_register.delete_many({'tenant_id': TENANT})


def _in_force():
    return {c['name'] for c in reg.categories(TENANT)}


# ----------------------------------------------------------------------------- adopt → pending → approve → active (B28, B29, B34, B43)
def test_author_lands_pending_and_pending_never_affects_a_crossing():
    doc = reg.author(TENANT, DPO1, CODENAMES)
    assert doc['status'] == 'pending' and doc['adopted_by'] == DPO1 and doc['version'] == 1 and 'approved_by' not in doc
    assert 'secret_codenames' not in _in_force()
    assert reg.classify('Papaya Comet ships on Tuesdays.', TENANT) == []
    assert reg.reconstruct('Papaya Comet ships on Tuesdays.', TENANT)['categories_applied'] == {}
    pending = [c for c in reg.categories(TENANT, include_pending=True) if c['status'] == 'pending']
    assert [c['name'] for c in pending] == ['secret_codenames']
    with pytest.raises(reg.Conflict):
        reg.author(TENANT, DPO1, CODENAMES)


def test_approve_is_the_gate_to_enforcement_and_records_provenance():
    doc = reg.approve(TENANT, DPO2, 'secret_codenames')
    assert doc['status'] == 'active' and doc['approved_by'] == DPO2 and doc['adopted_by'] == DPO1 and doc['approved_at'] >= doc['adopted_at']
    changes = [h['change'] for h in doc['history']]
    assert changes[0].startswith('declared') and changes[-1].startswith('approved')
    spans = reg.classify('Papaya Comet ships on Tuesdays.', TENANT)
    assert spans and spans[0]['category'] == 'secret_codenames' and spans[0]['kind'] == 'exact'
    assert '[SECRET_CODENAMES_1]' in reg.reconstruct('Papaya Comet ships on Tuesdays.', TENANT)['safe_text']
    with pytest.raises(LookupError):
        reg.approve(TENANT, DPO2, 'secret_codenames')


def test_revision_stays_pending_until_approved_then_supersedes():
    reg.author(TENANT, DPO1, {**CODENAMES, 'values': ['Papaya Comet', 'Mango Halo']})
    assert reg.classify('Mango Halo', TENANT) == [], 'a pending revision protects nothing yet'
    assert reg.classify('Papaya Comet', TENANT), 'the approved version keeps protecting meanwhile'
    doc = reg.approve(TENANT, DPO1, 'secret_codenames')
    assert doc['version'] == 2 and reg.classify('Mango Halo', TENANT)
    assert doc['history'][-1]['same_signatory'] is True, 'same adopter and approver is recorded, not hidden'
    on_record = [c for c in reg.categories(TENANT, include_removed=True) if c['name'] == 'secret_codenames']
    assert {(c['version'], c['status']) for c in on_record} == {(1, 'superseded'), (2, 'active')}
    assert all(c['history'] for c in on_record)


def test_draft_adoption_lands_pending_and_withdrawal_keeps_the_record():
    out = reg.propose(TENANT, DPO1, 'Client: Zinnia Grove Test Cooperative. The reserve fee is KES 1000. Signed 12 March 2026.')
    names = {d['name'] for d in out['drafts']}
    assert 'client_identity_values' in names
    doc = reg.adopt(TENANT, DPO1, 'client_identity_values')
    assert doc['status'] == 'pending' and 'client_identity_values' not in _in_force()
    assert not any(s['category'] == 'client_identity_values' for s in reg.classify('Zinnia Grove Test Cooperative opens on Monday.', TENANT)), 'the pending exact value is not in the crossing set (the contextual default may still fire on its cue)'
    gone = reg.withdraw(TENANT, DPO1, 'client_identity_values', 'SYNTHETIC: not wanted')
    assert gone['status'] == 'withdrawn' and gone['history'][-1]['change'].startswith('withdrawn')
    assert any(c['name'] == 'client_identity_values' and c['status'] == 'withdrawn' for c in reg.categories(TENANT, include_removed=True))
    for n in names - {'client_identity_values'}:
        reg.discard(TENANT, DPO1, n)


# ----------------------------------------------------------------------------- removal ceremony (B37–B39, B44)
def test_removal_needs_a_second_signature_and_a_countdown_and_exposes_nothing_meanwhile():
    doc = reg.remove(TENANT, DPO1, 'secret_codenames', 'SYNTHETIC: codenames announced')
    assert doc['status'] == 'active' and doc['removal']['state'] == 'proposed' and doc['removal']['proposed_by'] == DPO1
    assert reg.classify('Papaya Comet', TENANT), 'a proposed removal exposes nothing'
    with pytest.raises(reg.Conflict):
        reg.remove(TENANT, DPO1, 'secret_codenames', 'again')
    with pytest.raises(LookupError):
        reg.apply_removal(TENANT, DPO1, 'secret_codenames')
    with pytest.raises(ceremony.SecondSignatoryMissing):
        reg.countersign_removal(TENANT, DPO1, 'secret_codenames')
    doc = reg.countersign_removal(TENANT, DPO2, 'secret_codenames')
    rem = doc['removal']
    assert rem['state'] == 'countdown' and rem['counter_signed_by'] == DPO2 and rem['countdown_hours'] == ceremony.SYSTEM_ORDINARY_COUNTDOWN_HOURS == 48
    assert datetime.fromisoformat(rem['applies_at']) - datetime.fromisoformat(rem['counter_signed_at']) == timedelta(hours=48)
    with pytest.raises(ceremony.CountdownNotElapsed):
        reg.apply_removal(TENANT, DPO1, 'secret_codenames')
    assert reg.classify('Papaya Comet', TENANT), 'still protected during the countdown'


def test_removal_can_be_cancelled_during_the_countdown():
    doc = reg.cancel_removal(TENANT, DPO2, 'secret_codenames', 'SYNTHETIC: announcement postponed')
    assert doc['status'] == 'active' and 'removal' not in doc
    assert 'removal cancelled' in doc['history'][-1]['change'] and doc['history'][-1]['ceremony']['state'] == 'cancelled'
    assert reg.classify('Papaya Comet', TENANT)


def test_removal_applies_after_the_countdown_and_is_reverified():
    reg.remove(TENANT, DPO1, 'secret_codenames', 'SYNTHETIC: released publicly')
    reg.countersign_removal(TENANT, DPO2, 'secret_codenames')
    doc = reg.apply_removal(TENANT, DPO2, 'secret_codenames', now_utc=datetime.now(timezone.utc) + timedelta(hours=49))
    assert doc['status'] == 'removed' and doc['removal']['state'] == 'applied' and doc['removal']['applied_by'] == DPO2
    assert doc['removal']['re_verified']['clean'] is True and doc['removal']['re_verified']['values_checked'] == 2
    assert doc['removal']['witness_source'] == ceremony.WITNESS_IDENTITY_SOURCE
    assert reg.classify('Papaya Comet', TENANT) == [] and reg.classify('Mango Halo', TENANT) == []
    on_record = [c for c in reg.categories(TENANT, include_removed=True) if c['name'] == 'secret_codenames']
    assert {c['status'] for c in on_record} == {'superseded', 'removed'}, 'retired keeps its place in the record (B40)'


# ----------------------------------------------------------------------------- one entity set (B34, B45)
def test_catalogue_entities_live_in_the_register_and_the_lookup_reads_that_one_set():
    cat = tenant_entities.load_catalogue_for_test()
    assert cat['tenants'], 'fixture catalogue present'
    for tenant, groups in cat['tenants'].items():
        migrated = {c['name']: c for c in reg.entity_declarations(tenant)}
        surfaces = set()
        for group, entries in groups.items():
            name = f'catalogue_{group}'
            assert name in migrated and migrated[name]['provenance'] == 'migrated_from_catalogue' and migrated[name]['status'] == 'active'
            group_surfaces = {e['surface_form'] for e in entries} | {v for e in entries for v in e.get('variant_forms', [])}
            assert group_surfaces <= set(migrated[name]['values'])
            assert migrated[name]['entity_type'] == tenant_entities.ENTITY_TYPE_MAP[group]
            surfaces |= group_surfaces
        hits = asyncio.run(tenant_entities.lookup_in_text(' · '.join(sorted(surfaces)), tenant_id=tenant))
        assert {h['match'] for h in hits} == surfaces, 'parity: every catalogue surface form is still recognised'
        assert set(hits[0]) == {'start', 'end', 'type', 'match'} and {h['type'] for h in hits} <= set(tenant_entities.ENTITY_TYPE_MAP.values())
    assert asyncio.run(tenant_entities.lookup_in_text('John Smith', tenant_id=TENANT)) == [], 'tenant isolation'


def test_authored_entity_declaration_reaches_the_deidentifier_lookup_only_once_approved():
    reg.author(TENANT, DPO1, {'name': 'station_presenters', 'kind': 'exact', 'action': 'abstract', 'description': 'SYNTHETIC presenters', 'values': ['Wanjiru Test Host'], 'entity_type': 'PRESENTER'})
    assert asyncio.run(tenant_entities.lookup_in_text('Wanjiru Test Host opens the show.', tenant_id=TENANT)) == []
    reg.approve(TENANT, DPO2, 'station_presenters')
    hits = asyncio.run(tenant_entities.lookup_in_text('Wanjiru Test Host opens the show.', tenant_id=TENANT))
    assert hits == [{'start': 0, 'end': 17, 'type': 'PRESENTER', 'match': 'Wanjiru Test Host'}]


# ----------------------------------------------------------------------------- workbook vault intake (A5.3 reach on measured material only)
def _workbook_rows():
    rows = [('value', 'kind', 'category', 'description')]
    rows += [(f'Synthetic Party {i:04d}', 'exact', 'vault_parties', 'SYNTHETIC counterparties') for i in range(1000)]
    rows += [('', 'exact', 'vault_parties', 'empty'), ('Synthetic Party 0001', 'exact', 'vault_parties', 'duplicate'),
             ('[unclosed', 'pattern', 'vault_refs', 'bad regex'), (r'\bREF-\d{6}\b', 'pattern', 'vault_refs', 'SYNTHETIC reference numbers'), ('x', 'weird', 'vault_parties', 'unknown kind')]
    return rows


def test_vault_rows_become_pending_declarations_with_invalid_and_duplicate_rows_reported():
    measured = [('m-1', 'Synthetic Party 0007 called about REF-123456 yesterday.'), ('m-2', 'Nothing protected here.')]
    out = register_vault.intake_rows(TENANT, DPO1, _workbook_rows(), source_ref='SYNTHETIC workbook', measured=measured)
    assert out['rows'] == {'total': 1005, 'accepted': 1001, 'invalid': 3, 'duplicate': 1}
    assert {r['reason'] for r in out['invalid']} == {'empty value', 'invalid regular expression', 'unknown kind'}
    assert out['duplicates'] == [{'row': 1003, 'value': 'Synthetic Party 0001', 'category': 'vault_parties'}]
    pend = {d['name']: d for d in out['pending']}
    assert set(pend) == {'vault_parties', 'vault_refs'} and all(d['status'] == 'pending' and d['provenance'] == 'vault_intake' for d in pend.values())
    assert len(pend['vault_parties']['values']) == 1000 and pend['vault_refs']['patterns'] == [r'\bREF-\d{6}\b']
    assert 'vault_parties' not in _in_force() and reg.classify('Synthetic Party 0007', TENANT) == []
    reach = out['reach']
    assert reach['measured_documents'] == 2 and reach['by_declaration']['vault_parties'] == {'documents_matched': 1, 'matches': 1} and reach['by_declaration']['vault_refs'] == {'documents_matched': 1, 'matches': 1}
    assert 'not measured' in reach['unmeasured'].lower()


def test_vault_file_parsing_csv_and_xlsx_and_refusals():
    rows = _workbook_rows()[:4]
    buf = io.StringIO(); csv.writer(buf).writerows(rows)
    assert register_vault.rows_from_bytes(buf.getvalue().encode('utf-8-sig'), '.csv') == [list(r) for r in rows]
    import openpyxl
    wb = openpyxl.Workbook(); ws = wb.active
    for r in rows: ws.append(list(r))
    out = io.BytesIO(); wb.save(out)
    assert register_vault.rows_from_bytes(out.getvalue(), '.xlsx') == [list(r) for r in rows]
    with pytest.raises(ValueError):
        register_vault.rows_from_bytes(b'\x00\x01binary', '.csv')
    with pytest.raises(ValueError):
        register_vault.rows_from_bytes(b'hello', '.wav')
    with pytest.raises(ValueError):
        register_vault.intake_rows(TENANT, DPO1, [['name', 'something']], source_ref='no value column', measured=[])


def test_reach_states_the_unmeasured_honestly_when_nothing_is_measured():
    r = register_vault.reach([{'name': 'vault_parties', 'kind': 'exact', 'values': ['Synthetic Party 0001']}], [])
    assert r['measured_documents'] == 0 and r['by_declaration']['vault_parties'] == {'documents_matched': 0, 'matches': 0}
    assert re.search(r'no .*measured', r['unmeasured'].lower())
