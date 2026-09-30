"""M8/M9 completion — offline checks (no network, no GPU, temp stores). Each test names the ruling or invariant it pins."""
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "vendored" / "extraction_akki" / "backend"))

from services.training_runner import m9_worker as W  # noqa: E402
from services.training_runner import m9_readjudication as RJ  # noqa: E402
from services.training_runner import m9_dispatch as D  # noqa: E402
from services.business_continuity import policy, anchors  # noqa: E402
from services.business_continuity import ledger_archive as LA  # noqa: E402
from services.model_registry import registry as REG  # noqa: E402


def _eval(per, macro, ppl=20.0):
    return {"held": {"per_stratum": {s: {"accuracy": a, "abstention_rate": 0.01} for s, a in per.items()}, "macro_accuracy": macro, "ece": 0.01, "seconds_per_unit_mean": 0.04, "mean_perplexity": ppl}}


def test_ruling_1a_swahili_ceiling_passes_on_outcome_floor_not_relative_margin():
    base = _eval({"swa": 0.984, "kam": 0.0}, 0.492, ppl=100.0)
    adapter = _eval({"swa": 0.9895, "kam": 0.913}, 0.951, ppl=98.0)
    card, extra = W.moac_card("m9j-x", base, adapter, base["held"], adapter["held"], True, 100.0, 800, "2026-09-30T00:00:00Z", 0.9)
    assert card["coverage_strata"]["measured_value"] == 1.0
    assert extra["per_stratum_pass"] == {"swa": True, "kam": True}
    assert "Outcome" in card["coverage_strata"]["method_of_measurement"]
    assert card["accuracy_uncurated"]["floor_value"] == round(0.492 + W.M_A_IMPROVEMENT_DEFAULT, 6)  # aggregate M-a stays global


def test_ruling_1a_regression_below_base_still_fails_the_stratum():
    base = _eval({"swa": 0.9975, "kam": 0.0}, 0.5)
    adapter = _eval({"swa": 0.9677, "kam": 0.92}, 0.94)
    card, extra = W.moac_card("m9j-y", base, adapter, base["held"], adapter["held"], True, 100.0, 800, "t", 0.9)
    assert extra["per_stratum_pass"] == {"swa": False, "kam": True}
    assert card["coverage_strata"]["measured_value"] == 0.5


def test_readjudication_verdict_reads_certificate_per_stratum():
    rows, coverage = RJ.per_stratum_verdict({"swa": {"accuracy": 0.9895, "base_accuracy": 0.98446}, "lwg": {"accuracy": 0.89, "base_accuracy": 0.04}}, 0.9)
    assert rows["swa"]["passes"] and not rows["lwg"]["passes"] and coverage == 0.5


def test_docs_17_19_train_refuses_without_outcome_floor(monkeypatch):
    monkeypatch.setenv("M9_TRAINING_HOSTS", "akki-vm-ii,akki-vm")
    with pytest.raises(ValueError, match="OUTCOME_PER_STRATUM_FLOOR_REQUIRED"):
        D.validate("train", {"gpu_index": 0, "recipe": {}}, "akki-vm-ii")
    D.validate("train", {"gpu_index": 0, "recipe": {}, "acceptance_floor": 0.9}, "akki-vm-ii")
    with pytest.raises(ValueError, match="M9_SERVE_REQUIRES"):
        D.validate("serve", {"gpu_index": 1}, "akki-vm-ii")
    with pytest.raises(ValueError, match="M9_LOAD_TEST_REQUIRES"):
        D.validate("load_test", {}, "akki-vm-ii")


def test_worker_five_carrier_names_and_rpo_bound():
    assert W.RESUME_CARRIERS == ("weights", "optimizer", "scheduler", "data_offset", "rng")
    assert W.RPO_GPU_COMPUTE_SECONDS == policy.TIERS["tier_1_gpu_training_runs"]["rpo"]["value_seconds"] == 900
    assert W.RECIPE_DEFAULTS["checkpoint_cadence"] == "young_daly"


def test_ratified_policy_supersedes_sentinels_without_silent_flip():
    view = policy.policy_view()
    assert set(view["tiers"]) == {"tier_1_gpu_training_runs", "tier_2_ledgers_registry", "tier_3_worm_artifacts", "tier_4_site_loss"}
    assert anchors.BC_3_PENDING_OVERRIDE == "DEFAULT-PENDING-OVERRIDE" and "tier_3" in view["sentinel_supersession"]["BC_3_PENDING_OVERRIDE"]
    assert view["canon_bounds"]["S-10 ledger continuity rto_seconds"] == 3600 and view["canon_bounds"]["S-11 breach window_hours"] == 72
    assert "deferred" in view["deferred_by_owner"]["M8-T4 site restore on an isolated replacement environment"]
    assert view["tiers"]["tier_3_worm_artifacts"]["mechanism"]["object_lock_mode"] == "COMPLIANCE"
    assert view["tiers"]["tier_4_site_loss"]["regime"] == "warm-standby"


def test_worm_write_refuses_overwrite_and_pins_receipt(tmp_path, monkeypatch):
    monkeypatch.setenv("BC_WORM_DIR", str(tmp_path))
    receipt = LA.worm_write("a.json.gz", b"payload", {"row_count": 1})
    assert receipt["immutable"] and receipt["object_lock_mode"] == "COMPLIANCE" and receipt["bytes"] == 7
    assert oct(os.stat(tmp_path / LA.mongo_control.COLLECTION / "a.json.gz").st_mode)[-3:] == "444"
    with pytest.raises(FileExistsError):
        LA.worm_write("a.json.gz", b"other", {})
    assert [r["key"] for r in LA.worm_list()] == ["a.json.gz"]


def test_verify_chain_detects_prev_hash_break():
    from dataclasses import asdict
    from services.ledger_emitter.emit_intent import emit_control_intent
    from services.ledger_writer.main import append_intent
    from services.ledger_writer.mongo_control import digest
    events, prev = [], None
    for i in range(3):
        payload = {"n": i}
        intent = emit_control_intent(tenant_id="T", run_id="run-1", actor_id="a", event_type="execution.accepted", resource_type="request", resource_id="run-1",
                                     decision="admitted", reason_code="ok", payload_ref=digest(payload), epoch_s=1700000000 + i)
        row = append_intent(intent=intent, prev_row=prev, tenant_seq_next=(prev.seq + 1) if prev else 1)
        events.append({"command_id": f"c{i}", "row": asdict(row), "payload": payload}); prev = row
    assert LA.verify_chain(events)["intact"]
    broken = json.loads(json.dumps(events)); broken[2]["row"]["prev_hash"] = "0" * 64
    with pytest.raises(ValueError):
        LA.verify_chain(broken)


def test_registry_annotate_is_additive_and_refuses_unknown(tmp_path, monkeypatch):
    monkeypatch.setattr(REG, "_REGISTRY_DIR", tmp_path)
    (tmp_path / "models_registry.v0.json").write_text(json.dumps({"version": "v0", "models": {}}))
    n = REG.register_adapter("m9j-abc", {"role": "trained_adapter", "recipe_version": "recipe-sha256:x", "status": "admitted"})
    assert n == 1
    seed_bytes = (tmp_path / "models_registry.v1.json").read_bytes()
    n2 = REG.annotate_model("m9j-abc", {"status": "recalled"}, "M9-T5 test")
    assert n2 == 2 and (tmp_path / "models_registry.v1.json").read_bytes() == seed_bytes
    assert REG.load_registry()["m9j-abc"]["status"] == "recalled" and REG.load_registry()["m9j-abc"]["annotations"][0]["authority_source"] == "M9-T5 test"
    with pytest.raises(ValueError):
        REG.annotate_model("nope", {}, "x")
    with pytest.raises(REG.RecipeVersionMissingError):
        REG.register_adapter("m9j-def", {"role": "trained_adapter"})


def test_interruption_receipt_measures_loss_against_rpo(tmp_path, monkeypatch):
    from services.training_runner import m9_drills
    monkeypatch.setattr(D, "_jobs_dir", lambda: tmp_path)
    monkeypatch.setenv("BC_DRILL_RECEIPTS_DIR", str(tmp_path / "receipts"))
    killed = {"job_id": "m9j-aaaaaaaaaaaa", "host": "akki-vm-ii", "status": "interrupted", "remote": {"pid": 1}, "interrupt_rpc": {"signal": "SIGKILL", "observed_step_at_kill": 160, "observation_granularity_steps": 10, "receipt_id": "r1"},
              "remote_state": {"progress": {"recent_step_seconds": 0.6}}}
    resumed = {"job_id": "m9j-bbbbbbbbbbbb", "host": "akki-vm-ii", "status": "completed", "params": {"resume_from_job_id": "m9j-aaaaaaaaaaaa"},
               "run_certificate": {"checkpoint": {"resume_proof": {"resumed_from_step": 100, "carriers_restored": {k: True for k in W.RESUME_CARRIERS}, "checkpoint_sha256": "c", "resumed_adapter_sha256": "a"}, "cadence": {"rule": "young_daly", "receipts": 3}},
                                   "compute": {"steps": 320, "total_steps_planned": 320}, "artefact_sha256": "s", "receipt_sha256": "r"}, "track4_run_receipt": {"run_id": "m9j-bbbbbbbbbbbb"}}
    for j in (killed, resumed):
        (tmp_path / f"{j['job_id']}.json").write_text(json.dumps(j))
    receipt = m9_drills.compose_interruption_receipt("m9j-aaaaaaaaaaaa", "m9j-bbbbbbbbbbbb")
    assert receipt["measured"]["work_lost_steps"] == 60 and receipt["measured"]["work_lost_seconds"] == 36.0 and receipt["measured"]["within_rpo"]
    assert receipt["verdict"] == "PASS" and Path(receipt["receipt_path"]).exists()
    with pytest.raises(ValueError):
        m9_drills.compose_interruption_receipt("m9j-bbbbbbbbbbbb", "m9j-aaaaaaaaaaaa")
