"""Commission-gate Watch: observation feed → deterministic Macho verdicts → Mkono actions → REAL gate
effects (contain suspends commissioning, shape throttles) → effect receipts → honest release.
Isolated tmp record dirs; synthetic principals only."""
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException

from services.watch import commission_gate as gate


@pytest.fixture
def isolated(monkeypatch, tmp_path):
    for key, sub in (("WATCH_OBSERVATIONS_DIR", "obs"), ("WATCH_VERDICTS_DIR", "verdicts"), ("WATCH_ACTIONS_DIR", "actions"),
                     ("WATCH_MARKS_DIR", "marks"), ("WATCH_SEVER_SIGNALS_DIR", "signals"), ("MIRAGES_DIR", "mirages"),
                     ("MIRAGE_TOUCHES_DIR", "touches"), ("WATCH_MIRAGE_ARTIFACTS_DIR", "mirage_artifacts"),
                     ("WITNESS_IDENTITIES_DIR", "wi"), ("WITNESS_ATTESTATIONS_DIR", "wa"), ("WITNESS_TAMPER_ALARMS_DIR", "ta"),
                     ("WATCH_NOTICES_DIR", "notices"), ("WATCH_DECISIONS_DIR", "decisions"), ("WATCH_REQUIREMENTS_DIR", "requirements")):
        monkeypatch.setenv(key, str(tmp_path / sub))
    monkeypatch.setenv("WATCH_CONTAIN_DEFAULT_TTL_SECONDS", "3600")
    return tmp_path


ACTOR = {"tenant_id": "RMS", "principal_id": "p-analyst", "roles": ["analyst"]}
OPERATOR = {"tenant_id": "RMS", "principal_id": "p-operator", "roles": ["operator"]}
T0 = datetime(2026, 9, 29, 12, 0, tzinfo=timezone.utc)


def test_crossings_are_observed_admitted_and_refused(isolated, monkeypatch):
    monkeypatch.setattr(gate, "_now", lambda: T0)
    with gate.crossing(OPERATOR, "census.commission", {"source_ids": ["a"]}):
        pass
    with pytest.raises(HTTPException), gate.crossing(ACTOR, "census.commission", {"source_ids": ["a"]}):
        raise HTTPException(403, "no")
    rows = gate.rows("RMS")
    assert [(r["kind"], r["outcome"], r["status"], r["principal_id"]) for r in rows] == \
        [("crossing", "admitted", 202, "p-operator"), ("crossing", "refused", 403, "p-analyst")]
    assert len(rows[0]["digest"]) == 64 and rows[0]["boundary"] == "census.commission"
    with pytest.raises(ValueError):
        with gate.crossing(OPERATOR, "not.a.boundary", {}):
            pass


def test_fast_violation_mints_shape_and_gate_throttles(isolated, monkeypatch):
    clock = [T0]
    monkeypatch.setattr(gate, "_now", lambda: clock[0])
    for n in range(3):
        clock[0] = T0 + timedelta(seconds=n)
        with pytest.raises(HTTPException) as exc, gate.crossing(ACTOR, "language_cognition.commission", {"phase": "x"}):
            raise HTTPException(403, "only operators")
        assert exc.value.status_code == 403
    detections = [r for r in gate.rows("RMS") if r["kind"] == "detection"]
    assert [(d["detector"], d["action_class"]) for d in detections] == [("fast_violation", "shape")]
    from services.watch.persistence import get_action, get_verdict
    verdict = get_verdict(detections[0]["verdict_id"])
    assert verdict.verdict_class == "externally_steerable" and verdict.intensity == "elevated"
    assert "DEFAULT_PENDING_OWNER_RULING" in verdict.evidence_ref and verdict.subject_ref == "principal:p-analyst"
    action = get_action(detections[0]["action_id"])
    assert action.action_class == "shape" and action.reversible is True and action.verdict_ref == verdict.verdict_id
    # Shape = friction: the next attempt inside the minimum interval is throttled (429) before the handler runs,
    # with an effect receipt; a spaced attempt passes through to the handler again.
    clock[0] = T0 + timedelta(seconds=12)
    with pytest.raises(HTTPException) as exc, gate.crossing(ACTOR, "census.commission", {"a": 2}):
        pytest.fail("handler must not run while throttled")
    assert exc.value.status_code == 429 and action.action_id in exc.value.detail
    effects = [r for r in gate.rows("RMS") if r["kind"] == "effect"]
    assert effects[-1]["effect"] == "throttled_by_shape" and effects[-1]["action_ref"] == action.action_id
    clock[0] = T0 + timedelta(seconds=45)
    with gate.crossing(ACTOR, "census.commission", {"a": 3}):
        pass
    # One verdict per detector per window — no re-minting on a further refusal inside the window.
    clock[0] = T0 + timedelta(seconds=58)
    with pytest.raises(HTTPException) as exc, gate.crossing(ACTOR, "census.plan", {}):
        pytest.fail("throttled again: 13 s after the last attempt")
    assert exc.value.status_code == 429
    assert sum(1 for r in gate.rows("RMS") if r["kind"] == "detection") == 1


def test_slow_play_contains_then_releases_clean_at_ttl(isolated, monkeypatch):
    clock = [T0]
    monkeypatch.setattr(gate, "_now", lambda: clock[0])
    monkeypatch.setenv("WATCH_GATE_SHAPE_WINDOW_S", "1")            # keep the fast_violation shape out of the way
    for n in range(8):
        clock[0] = T0 + timedelta(minutes=30 * n)
        with pytest.raises(HTTPException), gate.crossing(ACTOR, "census.commission", {"n": n}):
            raise HTTPException(422, "bad")
    detections = {r["detector"]: r for r in gate.rows("RMS") if r["kind"] == "detection"}
    assert detections["slow_play"]["action_class"] == "contain" and detections["slow_play"]["ttl_seconds"] == 3600
    contain_id = detections["slow_play"]["action_id"]
    # Contain = commissioning suspended (409) with an effect receipt; the handler never runs.
    clock[0] = clock[0] + timedelta(minutes=5)
    with pytest.raises(HTTPException) as exc, gate.crossing(ACTOR, "language_cognition.commission", {}):
        pytest.fail("handler must not run under containment")
    assert exc.value.status_code == 409 and contain_id in exc.value.detail and "unaffected" in exc.value.detail
    assert [r["effect"] for r in gate.rows("RMS") if r["kind"] == "effect"] == ["refused_by_containment"]
    assert not any(r["kind"] == "crossing" and r["at"] == gate._iso(clock[0]) for r in gate.rows("RMS"))  # effects are not crossings
    # Sever is unreachable from these detectors.
    assert all(r["action_class"] != "sever" for r in gate.rows("RMS") if r["kind"] == "detection")
    # TTL passes → containment reconciled once as expired_clean; the actor is released.
    clock[0] = clock[0] + timedelta(hours=2)
    live = gate.active_effects("RMS", "p-analyst")
    assert live["contain"] == []
    releases = [r for r in gate.rows("RMS") if r["kind"] == "release"]
    assert len(releases) == 1 and releases[0]["outcome"] == "expired_clean" and releases[0]["action_ref"] == contain_id
    gate.active_effects("RMS", "p-analyst")
    assert sum(1 for r in gate.rows("RMS") if r["kind"] == "release") == 1
    with gate.crossing(ACTOR, "census.commission", {"after": "release"}):
        pass


def test_permitted_but_misused_duplicate_admits_annotate_without_effect(isolated, monkeypatch):
    clock = [T0]
    monkeypatch.setattr(gate, "_now", lambda: clock[0])
    for n in range(3):
        clock[0] = T0 + timedelta(seconds=n)
        with gate.crossing(OPERATOR, "language_cognition.commission", {"phase": "train_baseline"}):
            pass
    detections = [r for r in gate.rows("RMS") if r["kind"] == "detection"]
    assert [(d["detector"], d["action_class"]) for d in detections] == [("permitted_but_misused", "annotate")]
    clock[0] = T0 + timedelta(seconds=5)
    with gate.crossing(OPERATOR, "language_cognition.commission", {"phase": "train_baseline"}):
        pass                                                   # annotate changes nothing at the gate
    assert not any(r["kind"] == "effect" for r in gate.rows("RMS"))
    owned = gate.owned_records("RMS")
    assert {k: owned["counts"][k] for k in ("crossings", "refusals", "detections", "effects", "releases")} == \
        {"crossings": 4, "refusals": 0, "detections": 1, "effects": 0, "releases": 0}
    assert set(owned["action_ids"]) == {detections[0]["action_id"]}
    # The record witness attested the action digest at mint time (Canon 8 §16 sentence 1).
    from services.watch.witness import load_attestations
    assert [a.subject_ref for a in load_attestations()] == [f"action:{detections[0]['action_id']}"]
    assert detections[0]["witness_attestation"] == load_attestations()[0].attestation_id


def test_benign_operator_traffic_stays_within_friction_budget(isolated, monkeypatch):
    clock = [T0]
    monkeypatch.setattr(gate, "_now", lambda: clock[0])
    for n in range(6):
        clock[0] = T0 + timedelta(minutes=n)
        with gate.crossing(OPERATOR, "census.commission", {"source_ids": [f"s{n}"]}):
            pass
    assert not any(r["kind"] in ("detection", "effect") for r in gate.rows("RMS"))
    assert gate.owned_records("OTHER")["counts"]["crossings"] == 0                # tenant-scoped feed


def test_unobservable_crossing_fails_closed(isolated, monkeypatch):
    def broken(tenant_id, row):
        raise gate.GateUnobservable("disk")
    monkeypatch.setattr(gate, "_append", broken)
    with pytest.raises(HTTPException) as exc, gate.crossing(OPERATOR, "census.commission", {}):
        pass
    assert exc.value.status_code == 503 and "not landed" in exc.value.detail
    assert [b["boundary"] for b in gate.boundary_register()] == ["census.commission", "census.plan", "language_cognition.commission"]
