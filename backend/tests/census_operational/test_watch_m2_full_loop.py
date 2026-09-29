"""M2 full loop, offline on isolated stores: tripwire → structural sever → mark checked at every gate →
dual-control release (restoration) · mirage isolation measured · expiry release + notice · witness
attestation + break-in measurement · console acknowledgement leaves protection · learning loop
lands a versioned requirement only after two operators ratify. Synthetic principals only."""
import json
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException

from services.watch import commission_gate as gate
from services.watch import decisions, learning_loop, notices, tripwire, witness_binding

STORES = (("WATCH_OBSERVATIONS_DIR", "obs"), ("WATCH_VERDICTS_DIR", "verdicts"), ("WATCH_ACTIONS_DIR", "actions"), ("WATCH_MARKS_DIR", "marks"),
          ("WATCH_SEVER_SIGNALS_DIR", "signals"), ("MIRAGES_DIR", "mirages"), ("MIRAGE_TOUCHES_DIR", "touches"),
          ("WATCH_MIRAGE_ARTIFACTS_DIR", "mirage_artifacts"), ("WITNESS_IDENTITIES_DIR", "wi"), ("WITNESS_ATTESTATIONS_DIR", "wa"),
          ("WITNESS_TAMPER_ALARMS_DIR", "ta"), ("WATCH_NOTICES_DIR", "notices"), ("WATCH_DECISIONS_DIR", "decisions"), ("WATCH_REQUIREMENTS_DIR", "requirements"))
SUBJECT = {"tenant_id": "RMS", "principal_id": "p-drill", "roles": ["operator"], "session_ref": "sha256:sess", "device_ref": "sha256:dev"}
OP_A = {"tenant_id": "RMS", "principal_id": "p-op-a", "roles": ["operator"]}
OP_B = {"tenant_id": "RMS", "principal_id": "p-op-b", "roles": ["master_admin"]}
T0 = datetime(2026, 9, 29, 12, 0, tzinfo=timezone.utc)


@pytest.fixture
def isolated(monkeypatch, tmp_path):
    for key, sub in STORES:
        monkeypatch.setenv(key, str(tmp_path / sub))
    monkeypatch.setenv("WATCH_CONTAIN_DEFAULT_TTL_SECONDS", "3600")
    monkeypatch.setattr(gate, "_now", lambda: T0)
    return tmp_path


def _sever_drill(now=T0):
    planted = tripwire.plant("RMS", "rms-finance-backup-2019", 86400, "p-op-a", now)
    with pytest.raises(HTTPException) as exc, gate.crossing(SUBJECT, "census.commission", {"source_ids": ["rms-finance-backup-2019"]}):
        pytest.fail("handler must not run on a tripwire touch")
    return planted, exc.value


def test_tripwire_touch_convicts_marks_and_holds_every_gate(isolated):
    planted, refusal = _sever_drill()
    assert planted["isolation_check"]["passed"] is True and planted["isolation_check"]["stores_compared"] == 7
    assert refusal.status_code == 403 and "dual-control" in refusal.detail and "sha256" not in refusal.detail
    rows = gate.rows("RMS")
    detection = next(r for r in rows if r["kind"] == "detection")
    assert detection["detector"] == "mirage_incrimination" and detection["action_class"] == "sever" and detection["mark_id"].startswith("mark_gate_")
    from services.watch.persistence import get_action, get_verdict
    from services.watch.sever_signals import get_sever_signal
    verdict = get_verdict(detection["verdict_id"])
    assert verdict.verdict_class == "structural_certainty" and get_sever_signal(verdict.sever_certainty_signal_id).signal_kind == "mirage_incrimination"
    action = get_action(detection["action_id"])
    assert action.action_class == "sever" and action.reversible is False and action.ttl_seconds is None
    # Mark state is evaluated on EVERY protected boundary; the message never exposes mark dimensions.
    for boundary in ("census.plan", "language_cognition.commission", "census.commission"):
        with pytest.raises(HTTPException) as exc, gate.crossing(SUBJECT, boundary, {"x": boundary}):
            pytest.fail("severed subject must not reach the handler")
        assert exc.value.status_code == 403 and action.action_id in exc.value.detail and "sess" not in exc.value.detail
    assert sum(1 for r in gate.rows("RMS") if r["kind"] == "effect" and r["effect"] == "refused_by_sever") == 4
    # The panel item was pre-opened, the subject was told, the witness attested the digest.
    items = list(decisions.fold("RMS").values())
    assert len(items) == 1 and items[0]["klass"] == "demark_release" and items[0]["state"] == "open"
    assert [n["kind"] for n in notices.for_principal("RMS", "p-drill")] == ["sever"]
    assert detection["witness_attestation"].startswith("wa_gate_")
    # Mirage records stayed truthful and isolated: the touch is on record, the artefact store is a peer of production.
    from services.watch.mirage import load_touches
    from services.watch.mirage_artifacts import read_mirage_artifacts
    assert load_touches()[0].touch_kind == "guilty_use" and read_mirage_artifacts()[0].is_synthetic is True
    assert tripwire.isolation_check()["passed"] is True


def test_planting_refuses_when_mirage_store_overlaps_production(isolated, monkeypatch, tmp_path):
    monkeypatch.setenv("WATCH_MIRAGE_ARTIFACTS_DIR", str(tmp_path / "actions" / "inside"))
    with pytest.raises(RuntimeError) as exc:
        tripwire.plant("RMS", "decoy-inside-production", 60, "p-op-a", T0)
    assert "overlaps" in str(exc.value) and tripwire.isolation_check()["overlaps"] == ["actions"]
    assert not any(r["kind"] == "mirage_planted" for r in gate.rows("RMS"))


def test_severance_release_needs_two_distinct_operators_and_restores(isolated):
    _sever_drill()
    item = next(iter(decisions.fold("RMS").values()))
    acknowledged = decisions.act("RMS", item["decision_id"], "p-op-a", "acknowledge", "", T0)
    assert acknowledged["state"] == "open" and acknowledged["protection_changed"] is False and gate.sever_state("RMS", "p-drill")
    first = decisions.act("RMS", item["decision_id"], "p-op-a", "approve", "Drill subject; release after review.", T0)
    assert first["state"] == "open" and first["approvers"] == ["p-op-a"] and gate.sever_state("RMS", "p-drill")
    with pytest.raises(ValueError, match="different estate operator"):
        decisions.act("RMS", item["decision_id"], "p-op-a", "approve", "again", T0)
    with pytest.raises(ValueError, match="One line is required"):
        decisions.act("RMS", item["decision_id"], "p-op-b", "approve", "  ", T0)
    second = decisions.act("RMS", item["decision_id"], "p-op-b", "approve", "Concur.", T0 + timedelta(minutes=1))
    assert second["state"] == "executed" and second["protection_changed"] is True and gate.sever_state("RMS", "p-drill") is None
    release = next(r for r in gate.rows("RMS") if r["kind"] == "release")
    assert release["outcome"] == "released_by_dual_control" and release["released_by"] == ["p-op-a", "p-op-b"] and release["mark_ref"].startswith("mark_gate_")
    with gate.crossing(SUBJECT, "census.commission", {"source_ids": ["legit"]}):
        pass                                                   # real restoration: the gate admits again
    assert [n["kind"] for n in notices.for_principal("RMS", "p-drill")] == ["release", "sever"]
    with pytest.raises(ValueError, match="already executed"):
        decisions.act("RMS", item["decision_id"], "p-op-b", "decline", "late", T0)


def test_declined_release_keeps_protection(isolated):
    _sever_drill()
    item = next(iter(decisions.fold("RMS").values()))
    declined = decisions.act("RMS", item["decision_id"], "p-op-b", "decline", "Evidence stands.", T0)
    assert declined["state"] == "declined" and gate.sever_state("RMS", "p-drill") is not None


def test_expired_containment_releases_on_read_and_notifies(isolated, monkeypatch):
    clock = [T0]
    monkeypatch.setattr(gate, "_now", lambda: clock[0])
    monkeypatch.setenv("WATCH_GATE_SHAPE_WINDOW_S", "1")
    for n in range(8):
        clock[0] = T0 + timedelta(minutes=30 * n)
        with pytest.raises(HTTPException), gate.crossing(SUBJECT, "census.commission", {"n": n}):
            raise HTTPException(422, "bad")
    clock[0] = clock[0] + timedelta(minutes=5)
    with pytest.raises(HTTPException) as exc, gate.crossing(SUBJECT, "census.plan", {}):
        pytest.fail("contained")
    assert exc.value.status_code == 409
    clock[0] = clock[0] + timedelta(hours=2)
    released = gate.reconcile_expired("RMS", clock[0])       # a READ reconciles; the subject need not cross
    assert len(released) == 1 and gate.reconcile_expired("RMS", clock[0]) == []
    release = next(r for r in gate.rows("RMS") if r["kind"] == "release")
    assert release["outcome"] == "expired_clean" and release["attempts_not_landed"] == 1 and release["reconciliation"] == "notify"
    notice = notices.for_principal("RMS", "p-drill")[0]
    assert notice["kind"] == "release" and "1 commission attempt(s)" in notice["text"] and "not replayed" in notice["text"]


def test_break_in_measures_immutability_and_alarms_on_drift(isolated):
    _sever_drill()
    action_id = next(r for r in gate.rows("RMS") if r["kind"] == "detection")["action_id"]
    result = witness_binding.break_in(action_id, T0)
    assert result["immutability_measurement"] == "passed" and result["attempt_result"] == "refused" and "write_once" in result["refusal_reason"]
    from services.watch.persistence import _actions_dir
    path = _actions_dir() / f"{action_id}.json"
    body = json.loads(path.read_text())
    body["subject_ref"] = "principal:someone-else"
    path.write_text(json.dumps(body))
    drifted = witness_binding.break_in(action_id, T0 + timedelta(minutes=1))
    assert drifted["immutability_measurement"] == "FAILED"
    from services.watch.witness import load_alarms
    assert load_alarms()[0].evidence_ref == f"action:{action_id}"


def test_loss_of_watch_fails_closed_never_open(isolated, monkeypatch):
    calls = []
    def broken(tenant_id, row):
        raise gate.GateUnobservable("disk")
    monkeypatch.setattr(gate, "_append", broken)
    with pytest.raises(HTTPException) as exc, gate.crossing(OP_A, "census.commission", {"source_ids": ["a"]}):
        calls.append("handler ran")
    assert exc.value.status_code == 503 and calls == ["handler ran"] and "not landed" in exc.value.detail


def test_learning_loop_versions_requirements_only_after_dual_ratification(isolated, monkeypatch):
    clock = [T0]
    monkeypatch.setattr(gate, "_now", lambda: clock[0])
    with pytest.raises(ValueError, match="No gate finding"):
        learning_loop.propose("RMS", "p-op-a", T0)
    for n in range(3):
        clock[0] = T0 + timedelta(seconds=n)
        with pytest.raises(HTTPException), gate.crossing(SUBJECT, "language_cognition.commission", {"phase": "x"}):
            raise HTTPException(403, "only operators")
    before = next(r for r in gate.rows("RMS") if r["kind"] == "detection")
    assert "DEFAULT_PENDING_OWNER_RULING" in before["evidence_ref"]
    item = learning_loop.propose("RMS", "p-op-a", T0)
    assert item["klass"] == "requirement_ratification" and item["refs"]["routing"] == "research_loop_appended"
    assert item["refs"]["grounding_seam_id"] == learning_loop.GROUNDING_SEAM and learning_loop.current() is None
    from services.cif.output_routing import get_research_loop_items
    assert any(p.proposal_id == item["refs"]["proposal_id"] for p in get_research_loop_items())
    decisions.act("RMS", item["decision_id"], "p-op-a", "approve", "Pin v1.", T0)
    assert learning_loop.current() is None                       # one operator cannot ratify
    done = decisions.act("RMS", item["decision_id"], "p-op-b", "approve", "Concur.", T0)
    assert done["state"] == "executed" and learning_loop.current()["version"] == 1
    assert learning_loop.current()["thresholds"]["WATCH_GATE_FAST_REFUSALS"] == 3 and learning_loop.label() == "requirements=v1"
    # Replayed conduct is judged under v1; the earlier verdict keeps its DEFAULT label — history is not rewritten.
    clock[0] = T0 + timedelta(hours=1)
    for n in range(3):
        clock[0] = T0 + timedelta(hours=1, seconds=n)
        with pytest.raises(HTTPException), gate.crossing(SUBJECT, "language_cognition.commission", {"phase": "y"}):
            raise HTTPException(403, "only operators")
    after = [r for r in gate.rows("RMS") if r["kind"] == "detection"][-1]
    assert "requirements=v1" in after["evidence_ref"] and after["requirements"] == "requirements=v1"
    assert "DEFAULT_PENDING_OWNER_RULING" in next(r for r in gate.rows("RMS") if r["kind"] == "detection")["evidence_ref"]
    stages = [r["stage"] for r in gate.rows("RMS") if r["kind"] == "learning"]
    assert stages == ["proposed", "ratified"]
