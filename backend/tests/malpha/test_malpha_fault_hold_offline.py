"""Mα lane continuity: a worker-fault hold counts only faults under the current worker bundle, is released once corrected code supersedes
every fault, and never releases a supervisor hold. The voice worker renders the unconditioned hypothesis (identity_conditioning=false)."""
import sys
from types import SimpleNamespace

import pytest
from dotenv import load_dotenv

load_dotenv("/app/backend/.env")
sys.path.insert(0, "/app/backend/vendored/extraction_akki/backend")

from services.training_lab import malpha  # noqa: E402
from services.training_runner import m9_dispatch  # noqa: E402

OLD, NEW = "old-bundle-sha", "new-bundle-sha"


def _faults(sha, n=3):
    return [{"job_id": f"m9j-f{i}", "status": "failed", "reason": "ValueError: Complete identity comparators required", "code_sha256": sha, "iteration": 13} for i in range(n)]


def _wire(monkeypatch, bundle_sha, jobs_fn, updates):
    monkeypatch.setattr(m9_dispatch, "build_bundle", lambda: (b"", bundle_sha))
    monkeypatch.setattr(malpha, "jobs", jobs_fn)
    monkeypatch.setattr(malpha, "free_device", lambda phase, snapshot: ("host-a", 1))
    monkeypatch.setattr(malpha, "aip_ready", lambda host: True)
    monkeypatch.setattr(malpha, "worker_audit_ready", lambda host: True)
    monkeypatch.setattr(malpha, "_log", lambda *a, **k: None)
    monkeypatch.setattr(malpha.wpw, "record_event", lambda *a, **k: None)
    monkeypatch.setattr(malpha, "db", lambda: SimpleNamespace(malpha_commissions=SimpleNamespace(update_one=lambda q, u: updates.append(u))))


def test_three_faults_under_the_current_bundle_hold_the_lane_as_worker_fault(monkeypatch):
    updates, submitted = [], []
    _wire(monkeypatch, OLD, lambda **q: _faults(OLD) if q.get("iteration") == 13 else ([{"status": "completed", "iteration": i, "job_id": f"m9j-c{i}", "result": {}} for i in range(1, 13)] if q.get("status") == "completed" else []), updates)
    monkeypatch.setattr(malpha, "_submit", lambda *a, **k: submitted.append(a) or {"job_id": "x", "status": "running"})
    assert malpha.dispatch_lane("STORY-KIK-KAM-SWA", "story_voice", {}) is None
    assert submitted == []
    held = updates[-1]["$set"]["lane_state.story_voice"]
    assert held["status"] == "held" and held["held_by"] == "worker_fault" and held["code_sha256"] == OLD and held["iteration"] == 13


def test_faults_under_a_superseded_bundle_do_not_exhaust_corrected_code(monkeypatch):
    updates, submitted = [], []
    history = [{"status": "completed", "iteration": i, "job_id": f"m9j-c{i}", "result": {"recipe": {"identity_conditioning": True}, "dev": {"per_language": {}}, "artefact": {"path": "/a/voice_lm.pt"}}, "params": {"split_version": 3}} for i in range(1, 13)]
    _wire(monkeypatch, NEW, lambda **q: _faults(OLD) if q.get("iteration") == 13 else (history if q.get("status") == "completed" else []), updates)
    adopted = {"hypothesis_id": "hyp-17ab101501fe", "recipe_delta": {"identity_noise": 2.0, "identity_conditioning": False}, "acceptance": {"proposal_id": "cif_x"}}
    from services.training_lab import malpha_supervisor
    monkeypatch.setattr(malpha_supervisor, "select", lambda *a, **k: pytest.fail("a faulted iteration retries its adopted recipe; the supervisor is not re-run"))
    monkeypatch.setattr(malpha_supervisor, "db", lambda: SimpleNamespace(malpha_hypotheses=SimpleNamespace(find_one=lambda q, p: adopted)))
    monkeypatch.setattr(malpha_supervisor, "bind_job", lambda *a, **k: None)
    monkeypatch.setattr(malpha, "_submit", lambda cid, lane, phase, params, host, index, iteration: submitted.append(params) or {"job_id": "m9j-new", "status": "running"})
    rec = malpha.dispatch_lane("STORY-KIK-KAM-SWA", "story_voice", {})
    assert rec["status"] == "running" and len(submitted) == 1
    assert submitted[0]["recipe"]["identity_conditioning"] is False and submitted[0]["hypothesis_id"] == "hyp-17ab101501fe"
    assert "resume_from" not in submitted[0]  # no checkpoint under the corrected bundle
    assert updates[-1]["$set"]["lane_state.story_voice"]["attempt"] == 4  # every attempt stays on the record


def test_fault_hold_release_rule(monkeypatch):
    monkeypatch.setattr(m9_dispatch, "build_bundle", lambda: (b"", NEW))
    monkeypatch.setattr(malpha, "jobs", lambda **q: _faults(OLD))
    assert malpha.fault_hold_superseded("STORY-KIK-KAM-SWA", "story_voice", {"status": "held", "iteration": 13, "reason": "faulted 3 times"})
    assert not malpha.fault_hold_superseded("STORY-KIK-KAM-SWA", "story_voice", {"status": "held", "held_by": "training_supervisor", "iteration": 13})
    assert not malpha.fault_hold_superseded("STORY-KIK-KAM-SWA", "story_voice", {"status": "iterating", "iteration": 13})
    monkeypatch.setattr(malpha, "jobs", lambda **q: _faults(OLD, 2) + _faults(NEW, 1))
    assert not malpha.fault_hold_superseded("STORY-KIK-KAM-SWA", "story_voice", {"status": "held", "iteration": 13})  # a fault under the current code keeps the hold
    monkeypatch.setattr(malpha, "jobs", lambda **q: [])
    assert not malpha.fault_hold_superseded("STORY-KIK-KAM-SWA", "story_voice", {"status": "held", "iteration": 13})


def test_voice_model_renders_without_an_identity_vector():
    torch = pytest.importorskip("torch", reason="worker tensor contracts run on the estate hosts (worker audit), not in the control plane")
    from services.training_lab.malpha_voice_worker import CODE_BOS, MIMI_CODEBOOKS, build_voice_model
    model = build_voice_model(16, 32, 1, 4, 32, identity_dim=0, dense_identity=True)
    out = model(torch.tensor([[2, 3, 0, 0]]), torch.full((1, MIMI_CODEBOOKS, 5), CODE_BOS, dtype=torch.long), None)
    assert out.shape[0] == MIMI_CODEBOOKS and bool(torch.isfinite(out).all())


def test_worker_audit_checks_the_unconditioned_path():
    pytest.importorskip("torch", reason="the native worker audit runs on the estate hosts; its result is read from malpha_jobs")
    from services.training_lab import malpha_worker_audit

    class State:
        doc = {}

        def update(self, **k): pass

        def stage(self, name, value): self.doc[name] = value

    state = State()
    out = malpha_worker_audit.audit({"worker_contract_version": 2}, state)
    assert out["status"] == "passed" and state.doc["worker_contract"]["unconditioned_finite_forward"] is True
