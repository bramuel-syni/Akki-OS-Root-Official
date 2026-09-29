"""Runner cadence: a scope still enumerating remotely re-enters after a back-off and
keeps its shovel scope tags; the chain is never broken by a control-plane restart."""
import time

from services.census_autonomy import operational_runner as runner


def _stub_store(monkeypatch):
    saved, enqueued = {}, []

    def enqueue(tenant, principal, sources, key, lawful_ref, worker_id=None, source_refs=None):
        enqueued.append(key)
        row = {"census_run_id": "cr-" + f"{len(enqueued):012x}", "tenant_id": tenant, "principal_id": principal,
               "source_ids": sources, "idempotency_key": key, "status": "PENDING", "outcomes": [],
               "lawful_basis_admit_ref": lawful_ref, "worker_id": worker_id, "source_refs": source_refs}
        saved[row["census_run_id"]] = row
        return row, True
    monkeypatch.setattr(runner.store, "enqueue", enqueue)
    monkeypatch.setattr(runner.store, "save", lambda doc: saved.__setitem__(doc["census_run_id"], dict(doc)))
    return saved, enqueued


def _busy_run(attempt=None):
    row = {"census_run_id": "cr-aaaaaaaaaaaa", "tenant_id": "RMS", "principal_id": "p1", "source_ids": ["rms_obs"],
           "status": "REFUSED", "lawful_basis_admit_ref": "/tmp/admit.json", "worker_id": "akki-vm", "source_refs": None,
           "scoop_plan_id": "plan_x", "scoop_index": 0, "northena_run_id": "run-x",
           "outcomes": [{"source_id": "rms_obs", "status": "blocked", "reason_code": "ENUMERATION_ALREADY_RUNNING"}]}
    if attempt is not None:
        row["busy_retry_attempt"] = attempt
    return row


def test_busy_scope_reenters_with_backoff_and_scope_tags(monkeypatch):
    saved, enqueued = _stub_store(monkeypatch)
    monkeypatch.setenv("CENSUS_BUSY_RETRY_SECONDS", "900")
    current = _busy_run()
    before = time.time()
    successor_id = runner.defer_if_scope_busy(current)
    assert enqueued == ["cr-aaaaaaaaaaaa-busy1"]
    successor = saved[successor_id]
    assert successor["continues_run_id"] == "cr-aaaaaaaaaaaa" and successor["busy_retry_attempt"] == 1
    assert successor["not_before"] >= before + 900
    assert (successor["scoop_plan_id"], successor["scoop_index"], successor["northena_run_id"]) == ("plan_x", 0, "run-x")
    assert saved["cr-aaaaaaaaaaaa"]["continuation_run_id"] == successor_id


def test_busy_reentry_is_bounded_and_ignores_other_refusals(monkeypatch):
    saved, enqueued = _stub_store(monkeypatch)
    monkeypatch.setenv("CENSUS_BUSY_RETRY_MAX", "6")
    assert runner.defer_if_scope_busy(_busy_run(attempt=6)) is None
    other = dict(_busy_run(), outcomes=[{"source_id": "rms_obs", "status": "blocked", "reason_code": "NAS_ROOT_ABSENT"}])
    assert runner.defer_if_scope_busy(other) is None
    assert runner.defer_if_scope_busy(dict(_busy_run(), outcomes=[])) is None
    assert enqueued == []
