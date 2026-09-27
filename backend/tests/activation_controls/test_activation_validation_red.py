"""RED-first contracts for activation validation + schema/semantic fail-closed behavior."""

from __future__ import annotations

import asyncio
import copy
import hashlib
import importlib
from datetime import datetime, timedelta, timezone

import pytest


def _module(name: str):
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing expected RED target module {name}: {exc}")


def _utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def _sha256_doc(document: dict) -> str:
    encoded = __import__("json").dumps(document, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _base_document() -> dict:
    return {
        "certificate_id": "cert_0123456789abcdef0123456789abcdef",
        "schema_version": "1.1",
        "state": "LIVE-VERIFIED",
        "identity": {
            "estate_id": "tenant_SYNTHETIC_blue",
            "tenant_id": "tenant_SYNTHETIC_blue",
            "path": "A_source_to_registry",
            "frozen_request_id": "REQ-SYNTHETIC-0001",
            "frozen_objective_hash": "a" * 64,
            "run_id": "run-SYNTHETIC-0001",
            "run_started_at": "2026-02-01T10:00:00Z",
            "run_ended_at": "2026-02-01T10:30:00Z",
            "clock_source": "disciplined",
        },
        "authority": {
            "scope": {
                "group": "ops-council",
                "rule": "any_one",
                "decisions": [{
                    "principal_id": "principal_scope_1",
                    "decision": "approved",
                    "reason": "SYNTHETIC approval",
                    "recorded_at": "2026-02-01T09:50:00Z",
                    "receipt_ref": "receipt_scope_000001_long",
                }],
            },
            "expenditure": {
                "group": "finance-council",
                "rule": "any_one",
                "decisions": [{
                    "principal_id": "principal_exp_1",
                    "decision": "approved",
                    "reason": "SYNTHETIC approval",
                    "recorded_at": "2026-02-01T09:51:00Z",
                    "receipt_ref": "receipt_expenditure_000001_long",
                }],
            },
            "purpose_specific": [],
            "purposes_authorised": ["census"],
            "standing_approval_ref": None,
        },
        "release_acceptance": {
            "decision": "not_applicable",
            "recorded_at": "2026-02-01T10:40:00Z",
            "acceptance_standard_ref": "acceptance-standard-v1_1-SYNTHETIC",
            "criteria": [],
            "prerequisites": [],
        },
        "inputs": {
            "snapshot_hashes": ["b" * 64],
            "dial_versions": {
                "custody_floor": "dial-custody-v1.1",
                "approving_authority": "dial-authority-v1.1",
                "external_crossing": "dial-crossing-v1.1",
                "disclosure_counterparties": "dial-disclosure-v1.1",
            },
            "policy_versions": {
                "crossing_decision_table": "crossing-1.1",
                "acceptance_standard": "acceptance-standard-v1.1",
                "cleanliness_pack": "cleanliness-pack-v1.1",
            },
            "custody_classes_in_scope": ["uncontrolled"],
            "held_out_ref": None,
        },
        "limits": {
            "dimensions": [{
                "dimension": "spend",
                "effective_limit": 20,
                "unit": "USD",
                "source": "owner_run_limit",
                "observed": 0,
                "enforced_by": "runtime-limiter",
            }]
        },
        "runtime": {
            "admitted_runtime_id": "runtime-synthetic-1",
            "executor_version": "executor-1.1",
            "model_refs": [],
            "recipe_ref": None,
            "implementation_workspace_touched_data": False,
        },
        "output": {
            "artefact_hash": "e" * 64,
            "registry_entry_id": "registry-entry-SYNTHETIC-1",
            "manifest_hash": "f" * 64,
            "manifest_row_count": 100,
            "denominator_count": 100,
            "reconciliation": {
                "processed": 95,
                "refused_with_reason": 3,
                "unmeasured_with_reason": 2,
                "unaccounted": 0,
            },
        },
        "usage": {
            "metered_event_refs": ["metered_event_ref_000001_long"],
            "terms_identifier": "terms-synthetic-v1.1",
            "measured_quantities": [{"unit": "GPU_hour", "quantity": 1.5, "measured_by": "meter-service"}],
            "reservation_ref": "reservation_ref_000001_long",
            "reconciled_against_reservation": True,
        },
        "evidence": {
            "receipt_refs": ["evidence_receipt_ref_000001_long"],
            "retrieval": {
                "principal_id": "principal_retrieval_1",
                "retrieved_at": "2026-02-01T10:35:00Z",
                "receipt_ref": "retrieval_receipt_ref_000001_long",
            },
            "refusal_demonstration": None,
            "acceptance_script": {
                "script_hash": "1" * 64,
                "written_before_run_at": "2026-01-31T09:00:00Z",
                "held_outside_task_scope": True,
                "result": "pass",
            },
            "re_performance": {
                "second_instance_id": "instance-2",
                "different_model_family": True,
                "sample_seed": "seed-2",
                "sample_size": 10,
                "agreements": 8,
                "disagreements": 2,
                "disagreement_refs": ["disagree_ref_1_long", "disagree_ref_2_long"],
            },
        },
        "mocked_components": [],
        "issuer": {
            "principal_id": "issuer-1",
            "issued_at": "2026-02-01T10:45:00Z",
            "signature": "fictional_signature_ref_000001_long",
            "verification_status": "verified",
            "verifier_head_hash": "2" * 64,
        },
        "supersession": {
            "supersedes": None,
            "superseded_by": None,
            "revalidation": {"blocked": False, "triggers_fired": []},
        },
    }


def _build_60_defect_cases():
    cases = []

    def add(name: str, mutator):
        cases.append((name, mutator))

    add("partial_live_failed_script", lambda d: (d.__setitem__("state", "PARTIALLY LIVE"), d["evidence"]["acceptance_script"].__setitem__("result", "fail")))
    add("partial_live_trigger_with_blocked_false", lambda d: (d.__setitem__("state", "PARTIALLY LIVE"), d["supersession"]["revalidation"].__setitem__("triggers_fired", ["dial_change"])))
    add("path_b_wrong_refusal_kind", lambda d: (d["identity"].__setitem__("path", "B_callable_skill"), d["release_acceptance"].__setitem__("decision", "refused"), d["evidence"].__setitem__("refusal_demonstration", {"kind": "junk_stratum_unit", "request_ref": "x", "reason_stated": "x", "receipt_ref": "x"})))
    add("path_c_admitted_one_criterion", lambda d: (d["identity"].__setitem__("path", "C_training_with_evaluation"), d["release_acceptance"].__setitem__("decision", "admitted"), d["release_acceptance"].__setitem__("criteria", [{"criterion_id": "criterion_1", "measured_value": 0.96, "threshold": 0.95, "outcome": "met", "measurement_ref": "m1"}])))
    add("path_c_duplicate_criterion_ids", lambda d: (d["identity"].__setitem__("path", "C_training_with_evaluation"), d["release_acceptance"].__setitem__("decision", "admitted"), d["release_acceptance"].__setitem__("criteria", [{"criterion_id": "dup", "measured_value": 0.96, "threshold": 0.95, "outcome": "met", "measurement_ref": "m1"}, {"criterion_id": "dup", "measured_value": 0.97, "threshold": 0.95, "outcome": "met", "measurement_ref": "m2"}])))
    add("shape_honest_absence_fabricated_value", lambda d: (d["identity"].__setitem__("path", "C_training_with_evaluation"), d["release_acceptance"].__setitem__("decision", "refused"), d["release_acceptance"].__setitem__("criteria", [{"criterion_id": "n1", "measured_value": "fabricated", "threshold": None, "outcome": "not_measured", "measurement_ref": None}])))
    add("negative_reperformance_agreements", lambda d: d["evidence"]["re_performance"].__setitem__("agreements", -1))
    add("negative_reperformance_disagreements", lambda d: d["evidence"]["re_performance"].__setitem__("disagreements", -2))
    add("negative_reconciliation_processed", lambda d: d["output"]["reconciliation"].__setitem__("processed", -1))
    add("negative_reconciliation_refused", lambda d: d["output"]["reconciliation"].__setitem__("refused_with_reason", -1))
    add("negative_reconciliation_unmeasured", lambda d: d["output"]["reconciliation"].__setitem__("unmeasured_with_reason", -1))
    add("negative_reconciliation_unaccounted", lambda d: d["output"]["reconciliation"].__setitem__("unaccounted", -1))
    add("arithmetic_mismatch_manifest_denominator", lambda d: d["output"].__setitem__("denominator_count", 80))
    add("arithmetic_mismatch_reconciliation_sum", lambda d: d["output"]["reconciliation"].__setitem__("processed", 50))
    add("invalid_issuer_signature", lambda d: d["issuer"].__setitem__("signature", ""))
    add("invalid_issuer_verification_state", lambda d: d["issuer"].__setitem__("verification_status", "unverified"))
    add("invalid_scope_estate_mismatch", lambda d: d["identity"].__setitem__("estate_id", "other_estate"))
    add("forbidden_client_principal_field", lambda d: d["identity"].__setitem__("proposing_principal_id", "other_principal"))
    add("future_run_started", lambda d: d["identity"].__setitem__("run_started_at", "2099-01-01T00:00:00Z"))
    add("future_run_ended", lambda d: d["identity"].__setitem__("run_ended_at", "2099-01-01T00:00:00Z"))
    add("ended_before_started", lambda d: (d["identity"].__setitem__("run_started_at", "2026-02-01T10:00:00Z"), d["identity"].__setitem__("run_ended_at", "2026-02-01T09:00:00Z")))
    add("issued_before_run_end", lambda d: d["issuer"].__setitem__("issued_at", "2026-02-01T10:20:00Z"))
    add("approval_recorded_after_issuer_issue", lambda d: d["authority"]["scope"]["decisions"][0].__setitem__("recorded_at", "2026-02-01T11:00:00Z"))
    add("workspace_touched_true", lambda d: d["runtime"].__setitem__("implementation_workspace_touched_data", True))
    add("unaccounted_nonzero", lambda d: d["output"]["reconciliation"].__setitem__("unaccounted", 1))
    add("acceptance_script_missing", lambda d: d["evidence"].__setitem__("acceptance_script", None))
    add("acceptance_script_fail_live", lambda d: d["evidence"]["acceptance_script"].__setitem__("result", "fail"))
    add("path_b_missing_refusal", lambda d: (d["identity"].__setitem__("path", "B_callable_skill"), d["release_acceptance"].__setitem__("decision", "refused"), d["evidence"].__setitem__("refusal_demonstration", None)))
    add("path_c_missing_heldout_ref", lambda d: (d["identity"].__setitem__("path", "C_training_with_evaluation"), d["inputs"].__setitem__("held_out_ref", None)))
    add("path_c_missing_recipe", lambda d: (d["identity"].__setitem__("path", "C_training_with_evaluation"), d["runtime"].__setitem__("recipe_ref", None)))
    add("path_c_missing_model_refs", lambda d: (d["identity"].__setitem__("path", "C_training_with_evaluation"), d["runtime"].__setitem__("model_refs", [])))
    add("path_a_admitted_forbidden", lambda d: (d["identity"].__setitem__("path", "A_source_to_registry"), d["release_acceptance"].__setitem__("decision", "admitted")))
    add("reconciled_against_reservation_false", lambda d: d["usage"].__setitem__("reconciled_against_reservation", False))
    add("reservation_ref_missing", lambda d: d["usage"].__setitem__("reservation_ref", None))
    add("limit_observed_exceeds_effective", lambda d: d["limits"]["dimensions"][0].__setitem__("observed", 999))
    add("negative_limit_effective", lambda d: d["limits"]["dimensions"][0].__setitem__("effective_limit", -5))
    add("negative_usage_quantity", lambda d: d["usage"]["measured_quantities"][0].__setitem__("quantity", -1))
    add("scope_all_refused", lambda d: d["authority"]["scope"].__setitem__("decisions", [{"principal_id": "x", "decision": "refused", "reason": "r", "recorded_at": "2026-02-01T09:50:00Z", "receipt_ref": "ref"}]))
    add("expenditure_all_refused", lambda d: d["authority"]["expenditure"].__setitem__("decisions", [{"principal_id": "x", "decision": "refused", "reason": "r", "recorded_at": "2026-02-01T09:51:00Z", "receipt_ref": "ref"}]))
    add("invalid_datetime_format", lambda d: d["identity"].__setitem__("run_started_at", "not-a-date"))
    add("extra_root_property", lambda d: d.__setitem__("unexpected_root", "extra"))

    # Reach key-60 target with additional timestamp/ref integrity defects.
    fields = [
        ("scope_decision_missing_receipt", lambda d: d["authority"]["scope"]["decisions"][0].__setitem__("receipt_ref", "")),
        ("expenditure_decision_missing_receipt", lambda d: d["authority"]["expenditure"]["decisions"][0].__setitem__("receipt_ref", "")),
        ("retrieval_receipt_missing", lambda d: d["evidence"]["retrieval"].__setitem__("receipt_ref", "")),
        ("retrieval_after_issue", lambda d: d["evidence"]["retrieval"].__setitem__("retrieved_at", "2026-02-01T11:00:00Z")),
        ("issuer_future", lambda d: d["issuer"].__setitem__("issued_at", "2099-01-01T00:00:00Z")),
        ("frozen_objective_hash_wrong_shape", lambda d: d["identity"].__setitem__("frozen_objective_hash", "abcd")),
        ("artefact_hash_wrong_shape", lambda d: d["output"].__setitem__("artefact_hash", "abcd")),
        ("manifest_hash_wrong_shape", lambda d: d["output"].__setitem__("manifest_hash", "abcd")),
        ("verifier_head_hash_wrong_shape", lambda d: d["issuer"].__setitem__("verifier_head_hash", "abcd")),
        ("empty_receipt_refs", lambda d: d["evidence"].__setitem__("receipt_refs", [])),
        ("no_custody_scope", lambda d: d["inputs"].__setitem__("custody_classes_in_scope", [])),
        ("unknown_pathkind", lambda d: d["identity"].__setitem__("path", "Z_unknown")),
        ("no_authorised_purpose", lambda d: d["authority"].__setitem__("purposes_authorised", [])),
        ("path_c_failed_criterion", lambda d: (d["identity"].__setitem__("path", "C_training_with_evaluation"), d["release_acceptance"].__setitem__("decision", "admitted"), d["release_acceptance"].__setitem__("criteria", [{"criterion_id": "c1", "measured_value": 0.90, "threshold": 0.95, "outcome": "failed", "measurement_ref": "m"}]))),
        ("path_c_not_measured_admitted", lambda d: (d["identity"].__setitem__("path", "C_training_with_evaluation"), d["release_acceptance"].__setitem__("decision", "admitted"), d["release_acceptance"].__setitem__("criteria", [{"criterion_id": "c2", "measured_value": None, "threshold": None, "outcome": "not_measured", "measurement_ref": None}]))),
        ("c_manifest_rows_negative", lambda d: d["output"].__setitem__("manifest_row_count", -1)),
        ("c_denominator_negative", lambda d: d["output"].__setitem__("denominator_count", -1)),
        ("criteria_ref_forged_like_uri", lambda d: (d["identity"].__setitem__("path", "C_training_with_evaluation"), d["release_acceptance"].__setitem__("decision", "admitted"), d["release_acceptance"].__setitem__("criteria", [{"criterion_id": "c3", "measured_value": 0.96, "threshold": 0.95, "outcome": "met", "measurement_ref": "forged://receipt"}]))),
        ("release_recorded_in_future", lambda d: d["release_acceptance"].__setitem__("recorded_at", "2099-01-01T00:00:00Z")),
    ]
    for item in fields:
        add(item[0], item[1])

    assert len(cases) == 60
    return cases


# Module/feature: activation module surface + fail-closed baseline contract.
def test_activation_modules_and_validation_result_contract_surface():
    validation_mod = _module("services.activation.validation")
    _module("services.activation.schema")
    _module("services.activation.semantics")
    evidence_mod = _module("services.activation.evidence")

    assert hasattr(validation_mod, "validate_certificate")
    assert hasattr(validation_mod, "ValidationResult")
    assert hasattr(evidence_mod, "EvidenceVerdict")

    result = asyncio.run(
        validation_mod.validate_certificate(
            _base_document(),
            tenant_id="tenant_SYNTHETIC_blue",
            principal_id="principal_SYNTHETIC_1",
            now=_utc_now(),
        )
    )
    for field_name in (
        "valid",
        "schema_valid",
        "semantics_valid",
        "evidence_verified",
        "derived_state",
        "profile_id",
        "certificate_sha256",
        "issues",
    ):
        assert hasattr(result, field_name)
    assert isinstance(result.certificate_sha256, str) and len(result.certificate_sha256) == 64
    for issue in getattr(result, "issues", []):
        assert set(issue.keys()) <= {"code", "path"}


# Module/feature: no live issuance merely from shape — server evidence is mandatory.
def test_valid_shape_without_server_owned_evidence_stays_non_live_and_unverified():
    validation_mod = _module("services.activation.validation")
    result = asyncio.run(
        validation_mod.validate_certificate(
            _base_document(),
            tenant_id="tenant_SYNTHETIC_blue",
            principal_id="principal_SYNTHETIC_1",
            now=_utc_now(),
        )
    )
    assert result.valid is False
    assert result.evidence_verified is False
    assert result.derived_state is None


# Module/feature: evidence input is server-owned typed verdict only; client JSON forbidden.
def test_client_json_evidence_is_forbidden_and_explicit_timeout_required_when_evidence_supplied():
    validation_mod = _module("services.activation.validation")
    document = _base_document()
    fake_json_evidence = {
        "certificate_sha256": _sha256_doc(document),
        "tenant_id": "tenant_SYNTHETIC_blue",
        "principal_id": "principal_SYNTHETIC_1",
        "verified_refs": ["ref://synthetic"],
        "signature_verified": True,
        "request_verified": True,
        "policy_verified": True,
        "approvals_verified": True,
        "measurements_verified": True,
        "manifest_verified": True,
        "independence_verified": True,
        "retrieval_verified": True,
        "refusal_verified": True,
        "revalidation_verified": True,
        "evidence_mode": "measured",
        "expires_epoch": int((_utc_now() + timedelta(hours=1)).timestamp()),
    }

    with pytest.raises(Exception):
        asyncio.run(
            validation_mod.validate_certificate(
                document,
                tenant_id="tenant_SYNTHETIC_blue",
                principal_id="principal_SYNTHETIC_1",
                evidence=fake_json_evidence,
                now=_utc_now(),
            )
        )


# Module/feature: key 60 review defects must be rejected by schema or semantics (fail-closed).
@pytest.mark.parametrize(
    "case_name,mutator",
    [pytest.param(name, mutator, id=name) for name, mutator in _build_60_defect_cases()],
)
def test_key_60_review_cases_reject_shape_or_semantic_defects(case_name, mutator):
    # Rejecting an already-invalid baseline is not proof of the target guard.
    schema_mod = importlib.import_module("services.activation.schema")
    sem_mod = importlib.import_module("services.activation.semantics")
    assert not schema_mod.schema_issues(_base_document())
    assert not sem_mod.semantic_issues(_base_document(), now=_utc_now())
    _ = case_name
    validation_mod = _module("services.activation.validation")
    document = copy.deepcopy(_base_document())
    mutator(document)

    result = asyncio.run(
        validation_mod.validate_certificate(
            document,
            tenant_id="tenant_SYNTHETIC_blue",
            principal_id="principal_SYNTHETIC_1",
            now=_utc_now(),
        )
    )
    assert result.valid is False
    assert (result.schema_valid is False) or (result.semantics_valid is False)
    assert len(result.issues) > 0
    for issue in result.issues:
        assert set(issue.keys()) <= {"code", "path"}
