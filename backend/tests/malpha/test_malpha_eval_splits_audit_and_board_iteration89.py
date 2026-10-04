"""Mα evaluation/splits/corpus-audit safeguards + read-only board/evidence live checks."""

import copy
import os
import random
import sys

import pytest
import requests
from dotenv import load_dotenv

load_dotenv("/app/frontend/.env")
sys.path.insert(0, "/app/backend/vendored/extraction_akki/backend")

from services.training_lab import malpha_corpus_audit as audit  # noqa: E402
from services.training_lab import malpha_evaluation as me  # noqa: E402
from services.training_lab import malpha_splits as splits  # noqa: E402


BASE_URL = os.environ.get("REACT_APP_BACKEND_URL")
OPERATOR = {"email": "demo.operator@demo.rms.example.com", "password": "demo-operator-pw"}


def _op_headers():
    if not BASE_URL:
        pytest.skip("REACT_APP_BACKEND_URL is required")
    login = requests.post(f"{BASE_URL.rstrip('/')}/api/auth/login", json=OPERATOR, timeout=30)
    if login.status_code != 200:
        pytest.skip(f"operator login failed: {login.status_code}")
    token = login.json().get("access_token")
    if not token:
        pytest.skip("operator access_token missing")
    return {"Authorization": f"Bearer {token}"}


# Module/feature: truthful listener evidence guardrails (Wilson + grouped bootstrap + fail-closed support minimums).
def test_listener_evidence_never_accepts_with_too_few_positives_even_perfect_points():
    metrics = {
        "segments_with_mentions": 9,
        "segments_without_mentions": 200,
        "tp": 9,
        "fp": 0,
        "fn": 0,
    }
    groups = [(1, 0, 0)] * 20
    out = me.listener_evidence(metrics, group_counts=groups, seed=42, reference_verified=True)
    assert out["point_target_met"] is True
    assert out["acceptance_ready"] is False
    assert out["supported_target_met"] is False
    assert "positive_segments" in out["support"]["missing_support"]


def test_listener_evidence_bootstrap_is_deterministic_for_fixed_seed_and_groups():
    groups = [(5, 1, 2), (3, 0, 1), (4, 2, 1), (6, 1, 0)] * 8
    first = me.grouped_intervals(groups, seed=1206, draws=300)
    second = me.grouped_intervals(groups, seed=1206, draws=300)
    assert first == second
    assert first["valid_draws"] > 0


def test_listener_evidence_invalid_counts_fail_closed():
    out = me.listener_evidence(
        {
            "segments_with_mentions": 120,
            "segments_without_mentions": 130,
            "tp": -1,
            "fp": 0,
            "fn": 0,
        },
        group_counts=[(1, 0, 0)] * 20,
        reference_verified=True,
    )
    assert out["acceptance_ready"] is False
    assert "invalid_counts" in out["reasons"]


# Module/feature: admission preflight must be metadata-only and fail-closed on stale/missing audit.
def test_admission_preflight_fails_closed_when_latest_audit_seal_stale_or_missing():
    seal_a = "a" * 64
    seal_b = "b" * 64
    records = [
        {
            "job_id": "m9j-old",
            "phase": "malpha_aip_relabel",
            "status": "completed",
            "result": {
                "report": {
                    "kik": {"by_split": {"admission": 180}},
                    "kam": {"by_split": {"admission": 160}},
                    "swa": {"by_split": {"admission": 150}},
                },
                "seals": {
                    "kik": {"admission_seg_ids_sha256": seal_a},
                    "kam": {"admission_seg_ids_sha256": seal_a},
                    "swa": {"admission_seg_ids_sha256": seal_a},
                },
            },
        },
        {
            "job_id": "m9j-new",
            "phase": "malpha_aip_relabel",
            "status": "completed",
            "result": {
                "report": {
                    "kik": {"by_split": {"admission": 180}},
                    "kam": {"by_split": {"admission": 160}},
                    "swa": {"by_split": {"admission": 150}},
                },
                "seals": {
                    "kik": {"admission_seg_ids_sha256": seal_b},
                    "kam": {"admission_seg_ids_sha256": seal_b},
                    "swa": {"admission_seg_ids_sha256": seal_b},
                },
            },
        },
        {
            "job_id": "m9j-audit-stale",
            "phase": "malpha_corpus_audit",
            "status": "completed",
            "result": {
                "per_language": {
                    "kik": {"admission_seal_sha256": seal_a, "support": {"sufficient": True}},
                    "kam": {"admission_seal_sha256": seal_a, "support": {"sufficient": True}},
                    "swa": {"admission_seal_sha256": seal_a, "support": {"sufficient": True}},
                },
                "independence_verified": True,
                "reference_verified": True,
            },
        },
    ]
    out = me.admission_preflight(records)
    assert out["ready"] is False
    assert out["test_content_read"] is False
    assert out["independence_verified"] is False
    assert out["reference_verified"] is False


def test_admission_preflight_uses_matched_audit_support_when_seal_matches():
    seal = "c" * 64
    support = {"sufficient": True, "missing_support": [], "positive_segments": 201, "negative_segments": 222, "recording_groups": 40}
    records = [
        {
            "job_id": "m9j-relabel",
            "phase": "malpha_aip_relabel",
            "status": "completed",
            "result": {
                "report": {
                    "kik": {"by_split": {"admission": 201}},
                    "kam": {"by_split": {"admission": 201}},
                    "swa": {"by_split": {"admission": 201}},
                },
                "seals": {k: {"admission_seg_ids_sha256": seal} for k in ("kik", "kam", "swa")},
            },
        },
        {
            "job_id": "m9j-audit",
            "phase": "malpha_corpus_audit",
            "status": "completed",
            "result": {
                "per_language": {k: {"admission_seal_sha256": seal, "support": support} for k in ("kik", "kam", "swa")},
                "independence_verified": True,
                "reference_verified": True,
            },
        },
    ]
    out = me.admission_preflight(records)
    assert out["ready"] is True
    assert all(out["per_language"][l]["sufficient"] for l in ("kik", "kam", "swa"))


# Module/feature: connected prospective sealer keeps transitive links together, unknown speakers train-only, order-invariant.
def test_connected_splits_transitive_links_unknown_train_only_and_input_order_invariant():
    rows = [
        {"session": "s1", "speaker": "A", "text_sha256": "t1"},
        {"session": "s2", "speaker": "B", "text_sha256": "t2"},
        {"session": "s3", "speaker": "A", "text_sha256": "t3"},  # speaker link to s1
        {"session": "s4", "speaker": "C", "text_sha256": "t2"},  # text link to s2
        {"session": "s5", "speaker": "U", "text_sha256": "tx"},  # unknown speaker component
    ]
    clusters = {
        "s1|A": 11,
        "s2|B": 22,
        "s3|A": 11,
        "s4|C": 33,
        "s5|U": None,
    }

    rows_a = copy.deepcopy(rows)
    map_a = splits.connected_splits(rows_a, clusters, seed=77, lang="kik", admission_pct=20, dev_pct=20)

    rows_b = copy.deepcopy(rows)
    random.Random(3).shuffle(rows_b)
    map_b = splits.connected_splits(rows_b, clusters, seed=77, lang="kik", admission_pct=20, dev_pct=20)

    assert map_a == map_b
    assert map_a["s1"] == map_a["s3"]
    assert map_a["s2"] == map_a["s4"]
    assert map_a["s5"] == "train"


def test_connected_splits_rejects_invalid_percentages():
    with pytest.raises(ValueError, match="Invalid split percentages"):
        splits.connected_splits([{"session": "s", "speaker": "p"}], {}, seed=1, lang="kik", admission_pct=60, dev_pct=50)


# Module/feature: corpus audit overlap counting (speaker/text/session), missing assignments, and cluster-id 0 handling.
def test_inspect_language_counts_overlap_and_missing_speakers_with_cluster_zero_valid():
    rows = [
        {"seg_id": "a1", "split": "train", "session": "st", "speaker": "alice", "text_sha256": "x", "mentions": ["b"]},
        {"seg_id": "a2", "split": "dev", "session": "sd", "speaker": "alice", "text_sha256": "y", "mentions": []},
        {"seg_id": "a3", "split": "admission", "session": "sa", "speaker": "cora", "text_sha256": "x", "mentions": []},
        {"seg_id": "a4", "split": "admission", "session": "sa", "speaker": "dave", "text_sha256": "z", "mentions": ["b"]},
    ]
    clusters = {
        "st|alice": 0,
        "sd|alice": 0,
        "sa|cora": 7,
        # sa|dave intentionally missing
    }
    expected_seal = __import__("hashlib").sha256(__import__("json").dumps(sorted(["a3", "a4"])).encode()).hexdigest()
    out = audit.inspect_language(rows, clusters, expected_seal)
    assert out["seal_matches"] is True
    assert out["speaker_assignments_missing"] == 1
    assert out["overlap_counts"]["train_dev"]["speaker_clusters"] == 1
    assert out["overlap_counts"]["train_admission"]["exact_text_hashes"] == 1
    assert out["admission_independence_verified"] is False


# Module/feature: live read-only board + evaluation evidence contracts.
def test_live_board_malpha_rows_are_read_only_and_progress_based_when_training():
    headers = _op_headers()
    response = requests.get(f"{BASE_URL.rstrip('/')}/api/training/lab/board", headers=headers, timeout=60)
    assert response.status_code == 200, response.text
    runs = response.json().get("runs", [])
    malpha_rows = [r for r in runs if str(r.get("family", "")).startswith("malpha_")]
    assert malpha_rows, "No M Alpha rows found on board"
    for row in malpha_rows:
        assert row.get("read_only_execution") is True
    in_training = [r for r in malpha_rows if r.get("status") == "In training"]
    for row in in_training:
        progress = row.get("progress") or {}
        assert progress.get("basis") == "optimizer_steps"
        assert isinstance(progress.get("step"), int)
        assert isinstance(progress.get("of"), int)
        assert progress["of"] > 0


def test_live_evaluation_evidence_is_metadata_only_and_no_test_content_read():
    headers = _op_headers()
    response = requests.get(f"{BASE_URL.rstrip('/')}/api/training/malpha/evaluation-evidence", headers=headers, timeout=60)
    assert response.status_code == 200, response.text
    body = response.json()
    preflight = body.get("listener_preflight") or {}
    assert preflight.get("test_content_read") is False
    assert preflight.get("raw_data_exported") is False
    assert isinstance(body.get("corpus_audits"), list)


def test_listener_evidence_rejects_fabricated_group_totals():
    out = me.listener_evidence({'segments_with_mentions': 200, 'segments_without_mentions': 200,
                               'tp': 198, 'fp': 2, 'fn': 2}, group_counts=[(100, 0, 0)] * 20, reference_verified=True)
    assert out['acceptance_ready'] is False
    assert 'group_counts_do_not_match_observed_counts' in out['reasons']


def test_voice_board_understands_live_compact_stage():
    from services.training_lab.malpha_board import _checks
    checks = _checks('story_voice', {'stages': {'dev_eval_step_2000': {'kik': {
        'overall_similarity': .65, 'identity_gate_passes': False, 'max_cosine': .51, 'rendered': 12}}}})
    assert '65.0%' in checks[0]['v']
    assert '0.51' in checks[0]['v']
    assert checks[0]['passes'] is None


def test_live_offline_admitted_text_models_are_not_in_service():
    response = requests.get(f'{BASE_URL.rstrip("/")}/api/training/lab/board', headers=_op_headers(), timeout=60)
    assert response.status_code == 200
    for row in response.json()['runs']:
        if row['family'] == 'text' and row.get('evidence', {}).get('admission') == 'admitted':
            assert row['status'] in ('Retired', 'In service' if row.get('health') else 'Admitted')
