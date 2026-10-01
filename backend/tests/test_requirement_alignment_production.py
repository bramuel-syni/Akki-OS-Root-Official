"""Internal regressions for the owner's artifact/evidence boundary. Fixtures never enter product stores."""
import copy
import sys
from pathlib import Path
from unittest.mock import MagicMock
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'vendored' / 'extraction_akki'))
sys.path.insert(0, str(ROOT / 'vendored' / 'extraction_akki' / 'backend'))
from services.training_lab import production as p
from services.training_lab.production_contracts import Definition, RecipeRevision
from services.training_lab.production_evidence import quote, measured_strata, measured_job
from services.census_autonomy.estate_skill import package


@pytest.fixture
def definition():
    return {'target_outcome': {'task': 'Language identification', 'domain': 'Text',
        'population_register_ref': 'm9j-123456789abc', 'stratum_refs': ['swa', 'luo'],
        'acceptance': {'swa': {'accuracy': .8, 'coverage': .9}, 'luo': {'accuracy': .85, 'coverage': .95}},
        'gate_policy': 'missed_stratum_gates_release', 'test_set_ref': 'a'*64,
        'constraints': {'latency': '1s', 'compute_budget': '3 GPU hours', 'deployment_target': 'Existing registered worker'}},
        'collection_schema': {'baseline_tier': ['SourceID', 'UnitID', 'LanguageID', 'RightsRef', 'Window'], 'objective_tier': [], 'provenance_refs': {}},
        'planned_epochs': 2, 'gpu_hour_cap': 3, 'legal_basis': 'Authorized source reference'}


@pytest.fixture
def register():
    return {'corpus_id': 'fixture-corpus', 'manifest_sha256': 'b'*64, 'per_stratum': {'swa': 100, 'luo': 100},
            'test_set_seal': {'held_ids_sha256': 'a'*64, 'sealed_at': '2026-01-01T00:00:00Z'}, 'splits': {'train': 180, 'held': 20}}


def test_compile_keeps_two_native_artifacts(monkeypatch, definition, register):
    monkeypatch.setattr(p, 'measured_job', lambda *a: ({'params': {'kind': 'transcript_text'}}, register))
    _, _, artifacts = p.validate_definition('RMS', definition)
    assert set(artifacts) == {'TargetOutcome', 'CollectionSchema'}
    assert artifacts['TargetOutcome']['population'] == definition['target_outcome']['population_register_ref']
    assert dict(artifacts['TargetOutcome']['acceptance'])['luo']['coverage'] == .95


@pytest.mark.parametrize('change', ['missing_stratum', 'missing_coverage', 'missing_constraint', 'unknown_column'])
def test_incomplete_contract_refused(monkeypatch, definition, register, change):
    monkeypatch.setattr(p, 'measured_job', lambda *a: ({'params': {'kind': 'transcript_text'}}, register))
    if change == 'missing_stratum': del definition['target_outcome']['acceptance']['luo']
    elif change == 'missing_coverage': del definition['target_outcome']['acceptance']['luo']['coverage']
    elif change == 'missing_constraint': del definition['target_outcome']['constraints']['compute_budget']
    else: definition['collection_schema']['objective_tier'] = ['InventedClinicalDiagnosis']
    with pytest.raises(ValueError): p.validate_definition('RMS', definition)


def test_no_substituted_population_or_seal(monkeypatch, definition, register):
    monkeypatch.setattr(p, 'measured_job', lambda *a: ({'params': {'kind': 'transcript_text'}}, register))
    definition['target_outcome']['test_set_ref'] = 'c'*64
    with pytest.raises(ValueError, match='sealed'): p.validate_definition('RMS', definition)
    definition['target_outcome']['test_set_ref'] = 'a'*64
    register['per_stratum']['uncovered'] = 30
    with pytest.raises(ValueError, match='strata'): p.validate_definition('RMS', definition)


def calibration():
    return {'runs': [{'base': 'fixture-base', 'fraction': f, 'tokens_per_second': rate,
                      'train_units': 100*f, 'train_tokens': 1000*f} for f, rate in [(0.2, 95), (0.5, 100), (1.0, 105)]]}


def test_quote_has_explicit_ci_and_assumptions():
    q = quote(calibration(), 'fixture-base', 1000, 2)
    low, high = q['confidence_interval_gpu_hours']
    assert 0 < low < q['estimate_gpu_hours'] < high
    assert q['confidence'] == .95 and q['assumptions'] and q['class'] == 'estimated'


def test_no_quote_without_multiple_volumes():
    d = calibration(); d['runs'][1]['fraction'] = d['runs'][0]['fraction']
    with pytest.raises(ValueError, match='three'): quote(d, 'fixture-base', 1000, 2)


def test_stratum_coverage_is_not_hidden_by_accuracy(definition):
    result = {'adapter_eval': {'held': {'per_stratum': {'swa': {'accuracy': 1., 'abstention_rate': .2, 'units': 100}}}}}
    strata = measured_strata(result, definition['target_outcome'])
    assert strata['swa']['passes'] is False
    assert strata['luo']['accuracy'] is None and strata['luo']['passes'] is None


def test_different_tenant_cannot_read_receipts():
    with pytest.raises(LookupError): measured_job('DIGICOW', 'm9j-123456789abc')


def test_attach_does_not_replace_completed_stage(monkeypatch):
    plan = {'manifest_sha256': 'a', 'stages': {'calibration': {'job_id': 'old'}}, 'revision': 2}
    monkeypatch.setattr(p, 'get', lambda *a: plan)
    monkeypatch.setattr(p, 'measured_job', lambda *a: ({}, {'manifest_sha256': 'a'}))
    with pytest.raises(ValueError, match='already bound'): p.attach('RMS', 'p', 'calibration', 'new')


def test_no_comparison_without_calibration(monkeypatch):
    monkeypatch.setattr(p, 'get', lambda *a: {'manifest_sha256': 'a', 'stages': {}, 'revision': 0})
    monkeypatch.setattr(p, 'measured_job', lambda *a: ({'receipt': {'receipt_sha256': 'hash'}}, {'manifest_sha256': 'a'}))
    with pytest.raises(ValueError, match='calibrated'): p.attach('RMS', 'p', 'comparison', 'j')


def test_estate_package_is_proposals_not_authority():
    report = {'job_id': 'eij-123456789abc', 'measured_at': '2026-01-01', 'cost_strategies': {'items': [{'title': 'Archive', 'bytes': 100, 'risk': 'Read demand unmeasured'}]}, 'data_products': []}
    original = copy.deepcopy(report)
    a, b = package(report), package(report)
    assert a['plan_id'] == b['plan_id'] and report == original
    assert a['execution_authorized'] is False
    assert a['manager']['actions'][0]['destructive_action_authorized'] is False
    assert all(x['class'] for x in a['manifest'])


def test_plan_reads_project_mongo_id_out(monkeypatch):
    coll = MagicMock(); monkeypatch.setattr(p, 'collection', lambda: coll)
    p.get('RMS', 'plan')
    coll.find_one.assert_called_once_with({'tenant_id': 'RMS', 'plan_id': 'plan'}, {'_id': 0})


def test_partial_recipe_cannot_become_a_run_contract(monkeypatch):
    plan = {'stages': {'comparison': {'job_id': 'j'}}, 'definition': {'planned_epochs': 2}}
    monkeypatch.setattr(p, 'get', lambda *a: plan)
    body = RecipeRevision(recipe={'optimizer': 'adamw'}, reason='Owner choice', evidence_refs=['j'], expected_revision=0)
    with pytest.raises(ValueError, match='complete optimizer'): p.revise_recipe('RMS', 'p', {'principal_id': 'owner'}, body)


def test_recipe_revision_uses_optimistic_concurrency(monkeypatch):
    plan = {'stages': {'comparison': {'job_id': 'j'}}, 'definition': {'planned_epochs': 2}}
    monkeypatch.setattr(p, 'get', lambda *a: plan)
    coll = MagicMock(); coll.find_one_and_update.return_value = None
    monkeypatch.setattr(p, 'collection', lambda: coll)
    body = RecipeRevision(recipe={'optimizer': 'adamw', 'lr': .0001, 'epochs': 2, 'batch_size': 256, 'grad_accum': 1, 'max_seq_len': 256}, reason='Owner choice', evidence_refs=['j'], expected_revision=4)
    with pytest.raises(ValueError, match='plan changed'): p.revise_recipe('RMS', 'p', {'principal_id': 'owner'}, body)
    assert coll.find_one_and_update.call_args.args[0]['revision'] == 4


def test_completed_recipe_is_immutable(monkeypatch):
    monkeypatch.setattr(p, 'get', lambda *a: {'stages': {'comparison': {'job_id': 'j'}, 'training': {'job_id': 't'}}})
    body = RecipeRevision(recipe={'optimizer': 'adamw'}, reason='Owner choice', evidence_refs=['j'], expected_revision=0)
    with pytest.raises(ValueError, match='immutable'): p.revise_recipe('RMS', 'p', {'principal_id': 'owner'}, body)