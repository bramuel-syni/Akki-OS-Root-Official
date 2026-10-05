"""WP-C7 — residency register and terms of reference (owner D7, OWNER_ORDERS §12).

Unit, no SSH: an injected snapshot shaped like the two H200 hosts (a training lane on vm-ii GPU0, a serving resident on GPU1) and fake
running jobs. Every class has a TOR; a placement that would evict a running lane is refused; an admitted model is never recorded as an
idle resident; a serving resident needs a demand lease; unaccounted residents become findings, never register entries."""
import sys
import uuid

import pytest
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')

from services.model_registry import residency  # noqa: E402

OWNER = {'model_id': f'test-{uuid.uuid4().hex[:6]}', 'principal_id': 'test:c7'}
GIB = 1024 * residency.MIB


@pytest.fixture(autouse=True)
def cleanup():
    yield
    residency.db().residency_register.delete_many({'owner.principal_id': 'test:c7'})


def _snapshot():
    return {'at': '2026-10-05T12:00:00Z', 'receipts': ['gpurcp-test'], 'gaps': [], 'devices': [
        {'host': 'akki-vm-ii', 'gpu_index': 0, 'uuid': 'GPU-0', 'used_mib': 13359, 'total_mib': 143771, 'utilization_pct': 87, 'processes': [{'pid': 3449505, 'used_mib': 13394}]},
        {'host': 'akki-vm-ii', 'gpu_index': 1, 'uuid': 'GPU-1', 'used_mib': 16719, 'total_mib': 143771, 'utilization_pct': 0, 'processes': [{'pid': 3439022, 'used_mib': 16710}]},
        {'host': 'akki-vm', 'gpu_index': 0, 'uuid': 'GPU-2', 'used_mib': 61183, 'total_mib': 143771, 'utilization_pct': 60, 'processes': [{'pid': 11, 'used_mib': 61000}, {'pid': 12, 'used_mib': 100}]},
        {'host': 'akki-vm', 'gpu_index': 1, 'uuid': 'GPU-3', 'used_mib': 2048, 'total_mib': 143771, 'utilization_pct': 0, 'processes': []}]}


def _jobs():
    return [{'job_id': 'm9j-text', 'host': 'akki-vm-ii', 'phase': 'malpha_story_text_train', 'status': 'running', 'remote': {'pid': 3449505}},
            {'job_id': 'm9j-lid', 'host': 'akki-vm-ii', 'phase': 'serve', 'status': 'running', 'remote': {'pid': 3439022}},
            {'job_id': 'm9j-listener', 'host': 'akki-vm', 'phase': 'malpha_listener_train', 'status': 'running', 'remote': {'pid': 11}}]


def test_every_class_has_terms_of_reference_and_none_permits_idle_gpu_residency():
    terms = residency.terms()
    assert set(terms) == {'active_run_data', 'checkpoint', 'admitted_model', 'serving_resident', 'derived_register', 'raw_material'}
    for name, spec in terms.items():
        assert len(spec['tor']) > 60 and spec['release'] and spec['where'] and spec['coresidence'], name
        assert spec['idle_resident'] is False, f'{name}: nothing may sit idle on a GPU'
    assert 'never resident idle' in terms['admitted_model']['tor'] and 'demand lease' in terms['serving_resident']['tor'] and 'never evicts' in terms['serving_resident']['tor']


def test_attribution_maps_known_pids_to_classes_and_reports_the_rest_as_findings():
    residents, findings = residency.attribute(_snapshot(), _jobs())
    by_job = {r['job_id']: r for r in residents}
    assert by_job['m9j-text']['class'] == 'active_run_data' and by_job['m9j-lid']['class'] == 'serving_resident' and by_job['m9j-listener']['class'] == 'active_run_data'
    kinds = [(f['kind'], f.get('pid')) for f in findings]
    assert ('unaccounted_resident', 12) in kinds, 'a pid no running job records is a finding, not an entry'
    assert ('memory_without_process', None) in kinds, 'memory without a listed process is reported, not attributed'


def test_serving_resident_fits_beside_the_lid_server_and_is_recorded_with_its_reason():
    entry = residency.place('serving_resident', 'akki-vm-ii', 1, 17 * GIB, OWNER, 'contained reader beside the LID server', lease={'kind': 'demand', 'granted_by': 'test:c7', 'renew_on': 'read request', 'lapse_after_idle_hours': 72}, snap=_snapshot(), jobs=_jobs())
    assert entry['status'] == 'placed' and entry['class'] == 'serving_resident' and entry['measured']['coresidents'][0]['job_id'] == 'm9j-lid'
    assert entry['measured']['free_mib_before'] == 143771 - 16719 and entry['tor'] and entry['release'] and entry['reason']
    assert residency.touch_lease(entry['entry_id']) == 1
    released = residency.release(entry['entry_id'], 'test done')
    assert released['status'] == 'released'


def test_placement_that_would_evict_a_running_lane_is_refused():
    with pytest.raises(residency.PlacementRefused, match='evict'):
        residency.place('serving_resident', 'akki-vm-ii', 1, 130 * GIB, OWNER, 'too big', lease={'kind': 'demand'}, snap=_snapshot(), jobs=_jobs())
    with pytest.raises(residency.PlacementRefused, match='exclusively'):
        residency.place('active_run_data', 'akki-vm-ii', 0, 10 * GIB, OWNER, 'second trainer on a busy GPU', snap=_snapshot(), jobs=_jobs())
    assert residency.db().residency_register.count_documents({'owner.principal_id': 'test:c7'}) == 0, 'refusals record nothing'


def test_admitted_model_is_never_placed_idle_and_a_serving_resident_needs_a_demand_lease():
    with pytest.raises(residency.PlacementRefused, match='not placed on a GPU'):
        residency.place('admitted_model', 'akki-vm', 1, 16 * GIB, OWNER, 'park the LID weights on the free GPU', snap=_snapshot(), jobs=_jobs())
    with pytest.raises(residency.PlacementRefused, match='demand lease'):
        residency.place('serving_resident', 'akki-vm', 1, 16 * GIB, OWNER, 'serve without a lease', snap=_snapshot(), jobs=_jobs())
    with pytest.raises(residency.PlacementRefused, match='not in the measured snapshot'):
        residency.place('serving_resident', 'akki-vm-iii', 0, 1 * GIB, OWNER, 'unknown host', lease={'kind': 'demand'}, snap=_snapshot(), jobs=_jobs())


def test_reconcile_flags_placed_entries_without_a_live_process():
    entry = residency.place('serving_resident', 'akki-vm', 1, 16 * GIB, OWNER, 'ghost', lease={'kind': 'demand'}, snap=_snapshot(), jobs=_jobs())
    residency.db().residency_register.update_one({'entry_id': entry['entry_id']}, {'$set': {'owner.job_id': 'm9j-ghost'}})
    out = residency.reconcile(snap=_snapshot(), jobs=_jobs())
    ghosts = [f for f in out['findings'] if f['kind'] == 'placed_without_live_process' and f['entry_id'] == entry['entry_id']]
    assert ghosts and ghosts[0]['job_id'] == 'm9j-ghost' and set(out['terms']) == set(residency.CLASSES)
