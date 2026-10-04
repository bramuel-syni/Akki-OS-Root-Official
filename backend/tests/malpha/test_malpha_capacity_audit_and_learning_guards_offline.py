"""Mα guardrail offline tests: larger-base trial controls, worker-audit gating, lease lock, learning schema wire contract."""

import asyncio
import os
import sys
from types import SimpleNamespace

import pytest
from dotenv import load_dotenv

load_dotenv("/app/backend/.env")
sys.path.insert(0, "/app/backend/vendored/extraction_akki/backend")

from services.training_lab import malpha  # noqa: E402
from services.training_lab import malpha_comparisons as mc  # noqa: E402
from services.training_lab import malpha_learning as ml  # noqa: E402
from services.training_runner import m9_dispatch  # noqa: E402
from services.training_runner import m9_serving  # noqa: E402


def test_launch_larger_trial_builds_research_only_recipe_from_registered_base(monkeypatch):
    captured = {}

    monkeypatch.setattr(malpha, "jobs", lambda **q: [])
    monkeypatch.setattr(malpha, "HOST_ALLOCATION", {"malpha_story_text_train": [("host-a", 0)]})
    monkeypatch.setattr(malpha, "worker_audit_ready", lambda host: host == "host-a")
    monkeypatch.setattr(malpha, "gpu_snapshot", lambda: {"devices": {("host-a", 1): {"memory_used_mib": 512}}})
    monkeypatch.setattr(malpha, "_busy_devices", lambda: set())
    monkeypatch.setattr(
        malpha,
        "_qwen_base_path",
        lambda host, base_id: (
            "/models/qwen3-8b-base",
            {"repo": "Qwen/Qwen3-8B-Base", "licence_verified": "apache-2.0"},
        ),
    )

    def fake_recipe(iteration, history, base_path):
        captured["recipe_call"] = (iteration, history, base_path)
        return {"lr": 2e-4}

    monkeypatch.setattr(malpha, "story_text_recipe", fake_recipe)

    def fake_submit(cid, lane, phase, params, host, gpu_index, iteration, actor="akki-autopilot"):
        captured["submit"] = {
            "cid": cid,
            "lane": lane,
            "phase": phase,
            "params": params,
            "host": host,
            "gpu_index": gpu_index,
            "iteration": iteration,
        }
        return {"status": "running", "job_id": "m9j-aaaaaaaaaaaa"}

    monkeypatch.setattr(malpha, "_submit", fake_submit)

    out = mc.launch_larger_text_trial()
    assert out["status"] == "running"
    assert captured["recipe_call"] == (1, [], "/models/qwen3-8b-base")
    assert captured["submit"]["phase"] == "malpha_story_text_train"
    recipe = captured["submit"]["params"]["recipe"]
    assert recipe["max_steps"] == 3000
    assert recipe["init_adapter"] is None
    assert recipe["comparison"]["product_admission_allowed"] is False


def test_launch_larger_trial_preflight_refuses_without_native_audit(monkeypatch):
    monkeypatch.setattr(malpha, "jobs", lambda **q: [])
    monkeypatch.setattr(malpha, "HOST_ALLOCATION", {"malpha_story_text_train": [("host-a", 0)]})
    monkeypatch.setattr(malpha, "worker_audit_ready", lambda host: False)
    with pytest.raises(ValueError, match="NATIVE_WORKER_AUDIT_REQUIRED"):
        mc.launch_larger_text_trial()


def test_launch_larger_trial_preflight_refuses_busy_or_protected_gpu(monkeypatch):
    monkeypatch.setattr(malpha, "jobs", lambda **q: [])
    monkeypatch.setattr(malpha, "HOST_ALLOCATION", {"malpha_story_text_train": [("host-a", 0)]})
    monkeypatch.setattr(malpha, "worker_audit_ready", lambda host: True)
    monkeypatch.setattr(malpha, "gpu_snapshot", lambda: {"devices": {("host-a", 1): {"memory_used_mib": malpha.RESIDENT_PROTECTED_MIB + 1}}})
    monkeypatch.setattr(malpha, "_busy_devices", lambda: set())
    with pytest.raises(ValueError, match="RESEARCH_GPU_NOT_FREE"):
        mc.launch_larger_text_trial()


def test_borrow_stops_serving_only_in_explicit_owner_operation(monkeypatch):
    stop_calls = []
    updates = []

    monkeypatch.setattr(malpha, "jobs", lambda **q: [])
    monkeypatch.setattr(malpha, "HOST_ALLOCATION", {"malpha_story_text_train": [("host-a", 0)]})
    monkeypatch.setattr(malpha, "_qwen_base_path", lambda host, base_id: ("/models/base", {"licence_verified": "apache-2.0"}))
    monkeypatch.setattr(malpha, "worker_audit_ready", lambda host: True)
    monkeypatch.setattr(malpha, "_busy_devices", lambda: set())
    monkeypatch.setattr(malpha, "now", lambda: "2026-10-04T00:00:00Z")
    monkeypatch.setattr(malpha, "db", lambda: SimpleNamespace(malpha_commissions=SimpleNamespace(update_one=lambda q, u: updates.append((q, u)))))
    monkeypatch.setattr(m9_dispatch, "list_jobs", lambda: [{"job_id": "legacy"}, {"phase": "serve", "status": "running", "host": "host-a", "job_id": "m9j-serve", "params": {"gpu_index": 1, "authority": {"model_id": "mdl-1"}}}])
    monkeypatch.setattr(m9_serving, "stop", lambda model_id, reason, principal_id: stop_calls.append((model_id, reason, principal_id)))
    monkeypatch.setattr(mc, "launch_larger_text_trial", lambda: {"status": "running", "job_id": "m9j-trial"})

    out = mc.borrow_serving_gpu_for_trial()
    assert out["status"] == "running"
    assert stop_calls and stop_calls[0][0] == "mdl-1"
    assert stop_calls[0][2] == "akki-autopilot"
    assert any("capacity_reallocation" in str(update) for update in updates)


def test_restore_serving_waits_for_terminal_trial_and_free_slot(monkeypatch):
    start_calls = []
    monkeypatch.setattr(
        malpha,
        "commission",
        lambda cid: {
            "capacity_reallocation": {
                "status": "borrowed",
                "serving_model_id": "mdl-1",
                "host": "host-a",
                "gpu_index": 1,
            }
        },
    )
    monkeypatch.setattr(malpha, "jobs", lambda **q: [{"status": "running"}] if q.get("lane") == "story_text_comparison" else [])
    monkeypatch.setattr(malpha, "_busy_devices", lambda: set())
    monkeypatch.setattr(m9_serving, "start", lambda *a, **k: start_calls.append((a, k)) or {"status": "running", "job_id": "m9j-restored"})

    snap = {"devices": {("host-a", 1): {"memory_used_mib": 128}}}
    assert mc.restore_serving_after_trial(snap) is None
    assert start_calls == []


def test_dispatch_worker_audits_idempotent_per_host_and_code_digest(monkeypatch):
    monkeypatch.setattr(malpha, "HOST_ALLOCATION", {"malpha_aip_build": [("host-a", 0), ("host-b", 0)]})
    monkeypatch.setattr(m9_dispatch, "build_bundle", lambda: ("b64", "digest-1"))

    def fake_jobs(**query):
        if query.get("phase") == "malpha_worker_audit" and query.get("host") == "host-a" and query.get("code_sha256") == "digest-1":
            return [{"status": "completed"}]
        return []

    submitted = []
    monkeypatch.setattr(malpha, "jobs", fake_jobs)
    monkeypatch.setattr(malpha, "_submit", lambda *a, **k: submitted.append((a, k)) or {"job_id": "m9j-sub", "status": "running"})

    out = malpha.dispatch_worker_audits()
    assert len(out) == 1
    assert submitted and submitted[0][0][4] == "host-b"


def test_dispatch_lane_is_gated_by_native_worker_audit_without_stopping_existing_jobs(monkeypatch):
    submit_calls = []
    monkeypatch.setattr(malpha, "free_device", lambda phase, snapshot: ("host-a", 0))
    monkeypatch.setattr(malpha, "aip_ready", lambda host: True)
    monkeypatch.setattr(malpha, "worker_audit_ready", lambda host: False)
    monkeypatch.setattr(malpha, "jobs", lambda **q: [])
    monkeypatch.setattr(malpha, "_submit", lambda *a, **k: submit_calls.append((a, k)))

    out = malpha.dispatch_lane("LISTEN-KIK-KAM-SWA", "listener", {"devices": {("host-a", 0): {"memory_used_mib": 128}}})
    assert out is None
    assert submit_calls == []


def test_tick_returns_already_running_when_lease_owned_elsewhere(monkeypatch):
    class _Lease:
        def find_one_and_update(self, *_a, **_k):
            return {"owner": "other-owner"}

        def delete_one(self, *_a, **_k):
            return None

    monkeypatch.setattr(malpha, "db", lambda: SimpleNamespace(malpha_dispatch_leases=_Lease()))
    out = malpha.tick()
    assert out["status"] == "already_running"


def test_tick_releases_lease_on_error(monkeypatch):
    calls = {"delete": 0}

    class _Lease:
        def find_one_and_update(self, _query, update, **_k):
            return {"owner": update["$set"]["owner"]}

        def delete_one(self, *_a, **_k):
            calls["delete"] += 1

    monkeypatch.setattr(malpha, "db", lambda: SimpleNamespace(malpha_dispatch_leases=_Lease()))
    monkeypatch.setattr(malpha, "_tick_unlocked", lambda: (_ for _ in ()).throw(RuntimeError("boom")))
    with pytest.raises(RuntimeError, match="boom"):
        malpha.tick()
    assert calls["delete"] == 1


def test_provider_schema_only_removes_unsupported_item_constraints_from_wire():
    schema = {
        "type": "array",
        "minItems": 1,
        "maxItems": 2,
        "items": {"type": "string", "minLength": 1, "maxLength": 8},
    }
    wire = ml.provider_schema(schema)
    assert "minItems" not in wire and "maxItems" not in wire
    assert "minLength" in wire["items"] and "maxLength" in wire["items"]


def test_learning_review_prompt_is_role_specific_and_not_proposer(monkeypatch):
    calls = []

    class _Collection:
        def __init__(self):
            self.row = None

        def create_index(self, *_a, **_k):
            return None

        def insert_one(self, row):
            self.row = dict(row)

        def find_one(self, *_a, **_k):
            return dict(self.row)

        def update_one(self, _query, update):
            if "$set" in update:
                self.row.update(update["$set"])
            if "$push" in update:
                self.row.setdefault("attempts", []).append(update["$push"]["attempts"])
            return SimpleNamespace(modified_count=1)

    class _Resp:
        def __init__(self, text):
            self.text = text
            self.model_id = "model"
            self.receipt_id = "r"
            self.tokens_in = 1
            self.tokens_out = 1
            self.latency_ms = 1

    async def fake_invoke(**kwargs):
        calls.append(kwargs)
        if kwargs["purpose"] == "malpha.learning_plan":
            return _Resp('{"findings":["f"],"experiments":[{"lane":"listener","hypothesis":"h","evidence_refs":["listener-result-1"],"change":"c","measurement":"m","failure_condition":"x"}],"limitations":["l"]}')
        return _Resp('{"verdict":"revise","findings":["ok"],"required_changes":["rc"]}')

    monkeypatch.setattr("services.chokepoint.llm.invoke", fake_invoke)
    monkeypatch.setattr("services.chokepoint.model_roles.resolve", lambda role: {"sdk_provider": "p1", "connection": "c", "model": "m1", "role": "planner"} if role == "planner" else {"sdk_provider": "p2", "connection": "c2", "model": "m2", "role": "reviewer"})
    monkeypatch.setattr(ml.store, "db", lambda: SimpleNamespace(malpha_learning_reviews=_Collection()))
    monkeypatch.setattr(
        "services.training_lab.malpha.jobs",
        lambda **_q: [{
            "lane": "listener",
            "status": "completed",
            "iteration": 1,
            "result": {
                "steps": 1,
                "dev": {
                    "mentions": {"kik": {"precision": 0.9, "recall": 0.9}, "kam": {"precision": 0.9, "recall": 0.9}, "swa": {"precision": 0.9, "recall": 0.9}},
                    "words": {"kik": {"wer": 0.1}, "kam": {"wer": 0.1}, "swa": {"wer": 0.1}},
                    "per_language": {
                        "kik": {"dev_perplexity": 1, "base_perplexity": 2, "language_fidelity_rate": 1, "behaviour": {"overall_similarity": 0.9}, "identity_gate": {"max_cosine_to_any_corpus_speaker": 0.1}},
                        "kam": {"dev_perplexity": 1, "base_perplexity": 2, "language_fidelity_rate": 1, "behaviour": {"overall_similarity": 0.9}, "identity_gate": {"max_cosine_to_any_corpus_speaker": 0.1}},
                        "swa": {"dev_perplexity": 1, "base_perplexity": 2, "language_fidelity_rate": 1, "behaviour": {"overall_similarity": 0.9}, "identity_gate": {"max_cosine_to_any_corpus_speaker": 0.1}},
                    },
                },
            },
        }],
    )
    monkeypatch.setattr("services.training_lab.malpha.COMMISSIONS", [])
    monkeypatch.setattr("services.training_lab.malpha.wpw.record_event", lambda *a, **k: None)

    result = asyncio.run(ml.reconstruct("tester"))
    assert result["status"] == "reviewed"
    review_call = next(c for c in calls if c["purpose"] == "malpha.learning_review")
    assert "NOT the proposer" in review_call["system_message"]


def test_m9_dispatch_accepts_native_worker_audit_phase_contract(monkeypatch):
    host = os.environ["M9_TRAINING_HOSTS"].split(",")[0].strip()
    params = {
        "commission_id": "STORY-KIK-KAM-SWA",
        "languages": ["kik", "kam", "swa"],
        "gpu_index": 0,
        "budget_mode": "uncapped_until_billing",
        "owner_order_ref": "owner",
        "seed": 1,
        "iteration": 0,
        "aip_db_dir": os.environ["LANGUAGE_COGNITION_REMOTE_ROOT"] + "/malpha/aip_db_v1",
        "worker_contract_version": 2,
    }
    # Module/feature: native m9 validator for worker-contract audit phase.
    m9_dispatch.validate("malpha_worker_audit", params, host)
