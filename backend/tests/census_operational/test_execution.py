"""Injected executor tests are MOCKED; they cannot satisfy live activation T14."""
import hashlib
import json
import time

import pytest

from services.census_autonomy import engine, operational_store as store
from services.census_autonomy.operational_runner import run_bounded_census
from services.census_autonomy.operational_reads import records, run_state
from services.mtafiti import asset_registry_writer


@pytest.fixture
def estate(tmp_path, monkeypatch):
    monkeypatch.setattr(engine, 'CENSUS_STATE_DIR', tmp_path / 'state')
    monkeypatch.setenv('CENSUS_RECORDS_DIR', str(tmp_path / 'census'))
    monkeypatch.setenv('CENSUS_JOB_MAX_SECONDS', '10')
    admission = tmp_path / 'admit.json'
    admission.write_text(json.dumps({'receipt_id': 'TEST-ONLY', 'scope': ['RMS MYSQL'], 'invariants': {'read_only': True}}))
    monkeypatch.setenv('CENSUS_LAWFUL_BASIS_PATH', str(admission))
    row, _ = store.enqueue('RMS', 'test-principal', ['rms_mysql'], 'test-idempotency-key-01', str(admission))
    job = engine.get_pending_scheduled_runs()[0]
    return row, job, admission


def good(run_id, tenant, source, *_):
    return {'protocol': 'akki-census-aggregate-v1', 'census_run_id': run_id, 'tenant_id': tenant,
            'source_id': source, 'execution_location': 'akki_host', 'observed_at': store.now(),
            'status': 'complete', 'database_count': 2, 'table_count': 5, 'row_count_estimate': 13,
            'worker_receipt_id': 'test-fixture-worker-only', 'source_rows_returned': 0}


def test_t10_duplicate_submission_has_one_queue_entry(estate):
    row, _, admission = estate
    again, fresh = store.enqueue('RMS', 'test-principal', ['rms_mysql'], 'test-idempotency-key-01', str(admission))
    assert not fresh and again['census_run_id'] == row['census_run_id']
    assert len(engine.get_pending_scheduled_runs()) == 1


def test_t10_same_key_different_selection_refused(estate):
    _, _, admission = estate
    with pytest.raises(ValueError):
        store.enqueue('RMS', 'test-principal', ['rms_obs'], 'test-idempotency-key-01', str(admission))


def test_t06_deadline_before_read(estate):
    _, job, _ = estate
    calls = []
    result = run_bounded_census(job, time.time() - 1, execute=lambda *a: calls.append(a))
    assert not calls and result['status'] == 'REFUSED'


def test_t06_missing_admission_before_read(estate):
    _, job, admission = estate
    admission.unlink()
    calls = []
    result = run_bounded_census(job, time.time() + 10, execute=lambda *a: calls.append(a))
    assert not calls and result['status'] == 'REFUSED'


def test_t06_foreign_descriptor_before_read(estate):
    _, job, _ = estate
    job['connect_source_descriptor']['source_ids'] = ['digicow_rds']
    calls = []
    result = run_bounded_census(job, time.time() + 10, execute=lambda *a: calls.append(a))
    assert not calls and result['status'] == 'REFUSED'


def test_t08_verified_result_survives_registry_restart(estate):
    _, job, _ = estate
    result = run_bounded_census(job, time.time() + 10, execute=good)
    assert result['status'] == 'COMPLETE'
    asset_registry_writer._REGISTRY.clear()  # Test-only process-restart simulation.
    visible = records('RMS')
    assert len(visible) == 1 and visible[0]['table_count'] == 5
    assert asset_registry_writer._REGISTRY
    assert records('DIGICOW') == []


def test_t03_foreign_run_not_visible(estate):
    row, _, _ = estate
    assert run_state(row['census_run_id'], 'DIGICOW') is None


def test_t08_placeholder_executor_cannot_complete(estate):
    _, job, _ = estate
    result = run_bounded_census(job, time.time() + 10, execute=lambda *_: {'note': 'Commit-A shape gate landed'})
    assert result['status'] == 'REFUSED' and not records('RMS')


def test_t09_blocked_slice_does_not_suppress_permitted_slice(estate):
    row, job, _ = estate
    row['source_ids'] = job['connect_source_descriptor']['source_ids'] = ['rms_obs', 'rms_mysql']
    store.save(row)
    calls = []
    def execute(run, tenant, source, *args):
        calls.append(source)
        if source == 'rms_obs': raise ConnectionError('test-only refusal')
        return good(run, tenant, source)
    result = run_bounded_census(job, time.time() + 10, execute=execute)
    assert calls == ['rms_obs', 'rms_mysql']
    assert result['status'] == 'REFUSED' and result['stage'] == 'partial'
    assert records('RMS')[0]['status'] == 'PARTIAL'


def test_t10_completed_run_not_reexecuted(estate):
    _, job, _ = estate
    calls = []
    def execute(*args):
        calls.append(args)
        return good(*args)
    first = run_bounded_census(job, time.time() + 10, execute=execute)
    second = run_bounded_census(job, time.time() + 10, execute=execute)
    assert first == second and len(calls) == 1


def test_t08_result_write_failure_never_reports_complete(estate, monkeypatch):
    _, job, _ = estate
    def fail(*_): raise OSError('test-only disk failure')
    monkeypatch.setattr(engine, '_write_result_receipt', fail)
    assert run_bounded_census(job, time.time() + 10, execute=good)['status'] == 'REFUSED'


def test_t07_remote_worker_not_executed_inside_control_plane():
    from services.census_autonomy import remote_dispatch
    source = __import__('inspect').getsource(remote_dispatch)
    assert 'exec(code)' not in source and 'pymysql' not in source
    assert 'RejectPolicy' in source and 'AutoAddPolicy' not in source