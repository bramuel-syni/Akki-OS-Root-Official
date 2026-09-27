"""Offline JSON artifact validation for revision v1.1 (no runtime integration)."""

import copy
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


VALIDATION_DIR = Path(__file__).resolve().parent
ORIGINALS_DIR = VALIDATION_DIR.parent / "originals"

SCHEMA_PATH = ORIGINALS_DIR / "activation_certificate.schema.json"
POLICY_PATH = ORIGINALS_DIR / "crossing_decision_table.v1_1.json"

EXPECTED_SCHEMA_SHA256 = "ad848bd95e76dcf4ef71cd0e0688914632de33e68ceb4168e7ede4209ad256d2"
EXPECTED_POLICY_SHA256 = "472b6369ef7059f9b451504e329605f02a8918081dbf3d5438239853ba6c8830"

PAYLOADS_DIR = VALIDATION_DIR / "payloads"
MATRIX_PATH = VALIDATION_DIR / "results_matrix_v1_1.json"


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _read_json_bytes(path: Path):
    raw = path.read_bytes()
    return raw, json.loads(raw.decode("utf-8"))


def _ptr(path_parts) -> str:
    if not path_parts:
        return "/"
    return "/" + "/".join(str(p) for p in path_parts)


def _build_format_checker() -> FormatChecker:
    checker = FormatChecker()

    @checker.checks("date-time")
    def _strict_datetime(value):
        if not isinstance(value, str):
            return True
        pattern = r"\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})"
        if not re.fullmatch(pattern, value):
            return False
        candidate = value.upper().replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(candidate).utcoffset() is not None
        except ValueError:
            return False

    return checker


def _validate(validator: Draft202012Validator, payload: dict) -> dict:
    errors = sorted(validator.iter_errors(payload), key=lambda e: (_ptr(e.path), e.message))
    return {
        "accepted": len(errors) == 0,
        "errors": [
            {
                "instance_path": _ptr(err.path),
                "schema_path": _ptr(err.absolute_schema_path),
                "validator": err.validator,
                "message": err.message,
            }
            for err in errors
        ],
    }


def _base_fixture() -> dict:
    return {
        "certificate_id": "cert_0123456789abcdef0123456789abcdef",
        "schema_version": "1.1",
        "state": "LIVE-VERIFIED",
        "identity": {
            "estate_id": "estate_SYNTHETIC_alpha",
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
                "decisions": [
                    {
                        "principal_id": "principal_scope_1",
                        "decision": "approved",
                        "reason": "SYNTHETIC approval",
                        "recorded_at": "2026-02-01T09:50:00Z",
                        "receipt_ref": "receipt_scope_000001_long",
                    }
                ],
            },
            "expenditure": {
                "group": "finance-council",
                "rule": "any_one",
                "decisions": [
                    {
                        "principal_id": "principal_exp_1",
                        "decision": "approved",
                        "reason": "SYNTHETIC approval",
                        "recorded_at": "2026-02-01T09:51:00Z",
                        "receipt_ref": "receipt_expenditure_000001_long",
                    }
                ],
            },
            "purpose_specific": [
                {
                    "group": "ethics-council",
                    "rule": "any_one",
                    "decisions": [
                        {
                            "principal_id": "principal_purpose_1",
                            "decision": "approved",
                            "reason": "SYNTHETIC approval",
                            "recorded_at": "2026-02-01T09:52:00Z",
                            "receipt_ref": "receipt_purpose_000001_long",
                        }
                    ],
                }
            ],
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
            "dimensions": [
                {
                    "dimension": "spend",
                    "effective_limit": 20,
                    "unit": "USD",
                    "source": "owner_run_limit",
                    "observed": 0,
                    "enforced_by": "runtime-limiter",
                }
            ]
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


def _path_b_fixture() -> dict:
    payload = copy.deepcopy(_base_fixture())
    payload["identity"]["path"] = "B_callable_skill"
    payload["release_acceptance"]["decision"] = "refused"
    payload["release_acceptance"]["criteria"] = [
        {
            "criterion_id": "criterion_scope_guard",
            "measured_value": "outside_scope",
            "threshold": "in_scope",
            "outcome": "failed",
            "measurement_ref": "measurement_ref_scope_0001_long",
        }
    ]
    payload["evidence"]["refusal_demonstration"] = {
        "kind": "out_of_scope_question",
        "request_ref": "request_ref_scope_0001_long",
        "reason_stated": "SYNTHETIC out-of-scope refusal",
        "receipt_ref": "refusal_receipt_ref_0001_long",
    }
    payload["runtime"]["model_refs"] = [
        {"registry_id": "model-reg-1", "hash": "d" * 64, "version": "1.0", "licence_ref": "licence_ref_0001_long"}
    ]
    return payload


def _path_c_admitted_fixture() -> dict:
    payload = copy.deepcopy(_base_fixture())
    payload["identity"]["path"] = "C_training_with_evaluation"
    payload["authority"]["purposes_authorised"] = ["training", "evaluation"]
    payload["release_acceptance"]["decision"] = "admitted"
    payload["release_acceptance"]["recorded_at"] = "2026-02-01T10:45:30Z"
    payload["release_acceptance"]["acceptance_standard_ref"] = "acceptance-standard-v1.1-SYNTHETIC-c-training"
    payload["release_acceptance"]["criteria"] = [
        {
            "criterion_id": f"criterion_{idx}",
            "measured_value": 0.95 + idx / 1000,
            "threshold": 0.95,
            "outcome": "met",
            "measurement_ref": f"measurement_ref_criterion_{idx}_long",
        }
        for idx in range(1, 7)
    ]
    payload["release_acceptance"]["prerequisites"] = [
        {
            "prerequisite_id": "prereq_1",
            "extension_version": "ext-1.1",
            "outcome": "met",
            "record_ref": "prereq_record_ref_0001_long",
        }
    ]
    payload["evidence"]["refusal_demonstration"] = {
        "kind": "unauthorised_manifest_unit",
        "request_ref": "request_ref_training_0001_long",
        "reason_stated": "SYNTHETIC refusal evidence artifact for C path",
        "receipt_ref": "refusal_receipt_training_0001_long",
    }
    payload["inputs"]["held_out_ref"] = {
        "custodian_principal_id": "principal_holdout_1",
        "split_protocol": "entity_disjoint",
        "seed": "seed-fiction-1",
        "fixed_before_training_at": "2026-01-20T10:00:00Z",
        "selection_hash": "c" * 64,
    }
    payload["runtime"]["model_refs"] = [
        {"registry_id": "model-reg-1", "hash": "d" * 64, "version": "1.0", "licence_ref": "licence_ref_0001_long"}
    ]
    payload["runtime"]["recipe_ref"] = "recipe_ref_training_0001_long"
    return payload


def _path_c_refused_not_measured_fixture() -> dict:
    payload = copy.deepcopy(_path_c_admitted_fixture())
    payload["release_acceptance"]["decision"] = "refused"
    payload["release_acceptance"]["criteria"] = [
        {
            "criterion_id": "criterion_not_measured_1",
            "measured_value": None,
            "threshold": None,
            "outcome": "not_measured",
            "measurement_ref": None,
        }
    ]
    payload["release_acceptance"]["prerequisites"][0]["outcome"] = "not_measured"
    payload["release_acceptance"]["prerequisites"][0]["record_ref"] = None
    return payload


def _partially_live_fixture() -> dict:
    payload = copy.deepcopy(_base_fixture())
    payload["state"] = "PARTIALLY LIVE"
    payload["mocked_components"] = [{"component": "peripheral-mock", "on_evidence_chain": False}]
    return payload


def _live_blocked_fixture() -> dict:
    payload = copy.deepcopy(_base_fixture())
    payload["state"] = "LIVE-BLOCKED"
    payload["supersession"]["revalidation"] = {"blocked": True, "triggers_fired": ["authority_revocation"]}
    return payload


def _save_payload(subdir: str, name: str, payload: dict) -> str:
    target_dir = PAYLOADS_DIR / subdir
    target_dir.mkdir(parents=True, exist_ok=True)
    out_path = target_dir / f"{name}.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return str(out_path)


def _run_case(validator: Draft202012Validator, section: str, name: str, payload: dict, expected: bool, results: list):
    payload_path = _save_payload(section, name, payload)
    result = _validate(validator, payload)
    entry = {
        "case": name,
        "expected_accepted": expected,
        "accepted": result["accepted"],
        "payload_path": payload_path,
        "errors": result["errors"],
    }
    results.append(entry)
    assert result["accepted"] == expected, (
        f"Case {name} expected accepted={expected} got accepted={result['accepted']} errors={result['errors']}"
    )


def test_offline_revision_v1_1_validation_suite():
    raw_schema_before, schema = _read_json_bytes(SCHEMA_PATH)
    raw_policy_before, policy = _read_json_bytes(POLICY_PATH)

    schema_sha_before = _sha256_bytes(raw_schema_before)
    policy_sha_before = _sha256_bytes(raw_policy_before)
    assert schema_sha_before == EXPECTED_SCHEMA_SHA256
    assert policy_sha_before == EXPECTED_POLICY_SHA256

    Draft202012Validator.check_schema(schema)
    checker = _build_format_checker()
    assert checker.conforms(None, "date-time")
    assert not checker.conforms("2026-02-01", "date-time")
    validator = Draft202012Validator(schema, format_checker=checker)

    matrix = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "label": "OFFLINE SYNTHETIC VALIDATION ONLY (not issued certificates; no runtime/API calls)",
        "artifact_hashes_before": {
            "activation_certificate.schema.json": schema_sha_before,
            "crossing_decision_table.v1_1.json": policy_sha_before,
        },
        "fixture_migration_note": "Legacy mutations re-based onto schema_version=1.1 synthetic baselines to avoid counting old-version invalidity as repair success.",
        "sections": {},
    }

    # Positive fixtures requested by reviewer.
    positive_results = []
    positive_cases = [
        ("path_a_valid_not_applicable", _base_fixture(), True),
        ("path_b_valid_model_and_out_of_scope_refusal", _path_b_fixture(), True),
        ("path_c_valid_admitted_six_met_criteria", _path_c_admitted_fixture(), True),
        ("path_c_valid_refused_not_measured_nulls", _path_c_refused_not_measured_fixture(), True),
        ("partially_live_valid_peripheral_mock", _partially_live_fixture(), True),
        ("live_blocked_valid_with_trigger", _live_blocked_fixture(), True),
    ]
    for name, payload, expected in positive_cases:
        _run_case(validator, "positives", name, payload, expected, positive_results)
    matrix["sections"]["positives"] = positive_results

    # Claimed shape repairs (should reject now).
    claimed_results = []

    c1 = _base_fixture()
    c1["supersession"]["revalidation"] = {"blocked": True, "triggers_fired": ["authority_revocation"]}
    _run_case(validator, "claimed_repairs", "live_verified_with_trigger_blocked_true", c1, False, claimed_results)

    c2 = _base_fixture()
    c2["issuer"]["verification_status"] = "unverified"
    _run_case(validator, "claimed_repairs", "live_verified_issuer_unverified", c2, False, claimed_results)

    c3 = _base_fixture()
    c3["issuer"]["signature"] = ""
    _run_case(validator, "claimed_repairs", "empty_signature", c3, False, claimed_results)

    c4 = _base_fixture()
    c4["mocked_components"] = [{"component": "peripheral-mock", "on_evidence_chain": False}]
    _run_case(validator, "claimed_repairs", "live_verified_peripheral_mock_nonempty", c4, False, claimed_results)

    c5 = _path_c_admitted_fixture()
    c5["release_acceptance"]["criteria"] = []
    _run_case(validator, "claimed_repairs", "path_c_admitted_empty_criteria", c5, False, claimed_results)

    c6 = _path_c_admitted_fixture()
    c6["inputs"]["held_out_ref"] = None
    _run_case(validator, "claimed_repairs", "path_c_null_held_out_ref", c6, False, claimed_results)

    c7 = _path_c_admitted_fixture()
    c7["runtime"]["recipe_ref"] = None
    _run_case(validator, "claimed_repairs", "path_c_null_recipe_ref", c7, False, claimed_results)

    c8 = _path_c_admitted_fixture()
    c8["runtime"]["model_refs"] = []
    _run_case(validator, "claimed_repairs", "path_c_empty_model_refs", c8, False, claimed_results)

    c9 = _path_b_fixture()
    c9["evidence"]["refusal_demonstration"] = None
    _run_case(validator, "claimed_repairs", "path_b_null_refusal_demonstration", c9, False, claimed_results)

    c10 = _path_c_admitted_fixture()
    c10["release_acceptance"]["criteria"][0]["measurement_ref"] = ""
    _run_case(validator, "claimed_repairs", "criterion_met_empty_measurement_ref", c10, False, claimed_results)

    c11 = _path_c_admitted_fixture()
    c11["release_acceptance"]["criteria"][0]["outcome"] = "not_measured"
    c11["release_acceptance"]["criteria"][0]["measured_value"] = None
    c11["release_acceptance"]["criteria"][0]["measurement_ref"] = None
    _run_case(validator, "claimed_repairs", "admitted_with_not_measured_criterion", c11, False, claimed_results)

    c12 = _path_c_admitted_fixture()
    c12["release_acceptance"]["criteria"][0]["outcome"] = "failed"
    _run_case(validator, "claimed_repairs", "admitted_with_failed_criterion", c12, False, claimed_results)

    c13 = _base_fixture()
    c13["output"]["reconciliation"]["processed"] = -1
    _run_case(validator, "claimed_repairs", "negative_reconciliation_count", c13, False, claimed_results)

    c14 = _base_fixture()
    c14["usage"]["measured_quantities"][0]["quantity"] = -1
    _run_case(validator, "claimed_repairs", "negative_usage_quantity", c14, False, claimed_results)

    c15 = _base_fixture()
    c15["limits"]["dimensions"][0]["effective_limit"] = -5
    _run_case(validator, "claimed_repairs", "negative_limit_effective_limit", c15, False, claimed_results)

    c16 = _base_fixture()
    c16["authority"]["scope"]["decisions"] = [
        {
            "principal_id": "principal_scope_1",
            "decision": "refused",
            "reason": "SYNTHETIC refusal",
            "recorded_at": "2026-02-01T09:50:00Z",
            "receipt_ref": "receipt_scope_refused_000001",
        }
    ]
    _run_case(validator, "claimed_repairs", "scope_all_refused", c16, False, claimed_results)

    c17 = _base_fixture()
    c17["authority"]["expenditure"]["decisions"] = [
        {
            "principal_id": "principal_exp_1",
            "decision": "refused",
            "reason": "SYNTHETIC refusal",
            "recorded_at": "2026-02-01T09:51:00Z",
            "receipt_ref": "receipt_expenditure_refused_000001",
        }
    ]
    _run_case(validator, "claimed_repairs", "expenditure_all_refused", c17, False, claimed_results)

    c18 = _base_fixture()
    c18["release_acceptance"]["decision"] = "admitted"
    c18["release_acceptance"]["criteria"] = [
        {
            "criterion_id": "criterion_bad_a",
            "measured_value": 0.91,
            "threshold": 0.95,
            "outcome": "met",
            "measurement_ref": "measurement_ref_bad_a_000001",
        }
    ]
    c18["release_acceptance"]["prerequisites"] = [
        {
            "prerequisite_id": "prereq_a",
            "extension_version": "ext-1.1",
            "outcome": "met",
            "record_ref": "prereq_record_ref_bad_a_000001",
        }
    ]
    _run_case(validator, "claimed_repairs", "path_a_admitted_should_reject", c18, False, claimed_results)

    c19 = _path_c_refused_not_measured_fixture()
    _run_case(validator, "claimed_repairs", "refused_c_not_measured_honest_absence_accept", c19, True, claimed_results)

    c20 = _path_c_refused_not_measured_fixture()
    c20["release_acceptance"]["criteria"][0]["measured_value"] = "fabricated"
    _run_case(validator, "claimed_repairs", "not_measured_with_fabricated_value_reject", c20, False, claimed_results)

    c21 = _path_c_refused_not_measured_fixture()
    c21["release_acceptance"]["criteria"][0]["measurement_ref"] = "measurement_ref_should_be_null"
    _run_case(validator, "claimed_repairs", "not_measured_with_nonnull_measurement_ref_reject", c21, False, claimed_results)

    # Old controls should still reject.
    c22 = _base_fixture()
    c22["runtime"]["implementation_workspace_touched_data"] = True
    _run_case(validator, "claimed_repairs", "control_workspace_touched_true", c22, False, claimed_results)

    c23 = _base_fixture()
    c23["output"]["reconciliation"]["unaccounted"] = 1
    _run_case(validator, "claimed_repairs", "control_unaccounted_nonzero", c23, False, claimed_results)

    c24 = _base_fixture()
    c24["unexpected_root"] = "extra"
    _run_case(validator, "claimed_repairs", "control_extra_root_property", c24, False, claimed_results)

    c25 = _base_fixture()
    c25["identity"]["run_started_at"] = "not-a-date-time"
    _run_case(validator, "claimed_repairs", "control_invalid_datetime", c25, False, claimed_results)

    matrix["sections"]["claimed_repairs_and_controls"] = claimed_results

    # Legacy 24 mutation replay, migrated onto v1.1 baselines.
    legacy_results = []
    legacy_cases = []

    l1 = _base_fixture()
    l1["mocked_components"] = [{"component": "peripheral-mock", "on_evidence_chain": False}]
    legacy_cases.append(("case_01_live_verified_peripheral_mock_nonempty", l1, False))

    l2 = _base_fixture()
    l2["supersession"]["revalidation"] = {"blocked": True, "triggers_fired": ["authority_revocation"]}
    legacy_cases.append(("case_02_live_verified_blocked_true_with_revocation_trigger", l2, False))

    l3 = _base_fixture()
    l3["issuer"]["verification_status"] = "unverified"
    l3["issuer"]["signature"] = ""
    legacy_cases.append(("case_03_live_verified_issuer_unverified_empty_signature", l3, False))

    l4 = _base_fixture()
    l4["evidence"]["acceptance_script"]["result"] = "fail"
    legacy_cases.append(("case_04_live_verified_acceptance_script_fail", l4, False))

    l5 = _path_c_admitted_fixture()
    l5["release_acceptance"]["criteria"] = []
    l5["release_acceptance"]["acceptance_standard_ref"] = None
    l5["inputs"]["held_out_ref"] = None
    l5["runtime"]["recipe_ref"] = None
    l5["runtime"]["model_refs"] = []
    legacy_cases.append(("case_05_path_c_release_admitted_minimal_semantics", l5, False))

    l6 = _path_b_fixture()
    l6["evidence"]["refusal_demonstration"] = None
    legacy_cases.append(("case_06_path_b_refusal_demonstration_null", l6, False))

    l7a = _path_c_admitted_fixture()
    l7a["release_acceptance"]["criteria"] = [
        {
            "criterion_id": "hardcoded-criterion",
            "measured_value": "HARDCODED",
            "threshold": "expected",
            "outcome": "met",
            "measurement_ref": "",
        }
    ]
    legacy_cases.append(("case_07a_met_with_empty_measurement_ref", l7a, False))

    l7b = _path_c_admitted_fixture()
    l7b["release_acceptance"]["criteria"] = [
        {
            "criterion_id": "fabricated-criterion",
            "measured_value": "fabricated_value",
            "threshold": "fabricated_threshold",
            "outcome": "met",
            "measurement_ref": "fabricated://record/12345",
        }
    ]
    legacy_cases.append(("case_07b_met_with_fabricated_measurement_ref", l7b, True))

    l8 = _path_c_refused_not_measured_fixture()
    legacy_cases.append(("case_08_not_measured_with_null_measured_value", l8, True))

    l9 = _base_fixture()
    l9["output"]["manifest_row_count"] = 100
    l9["output"]["denominator_count"] = 10
    l9["output"]["reconciliation"] = {
        "processed": -4,
        "refused_with_reason": 999,
        "unmeasured_with_reason": -3,
        "unaccounted": 0,
    }
    legacy_cases.append(("case_09_reconciliation_negative_and_mismatched_counts", l9, False))

    l10a = _base_fixture()
    l10a["usage"]["measured_quantities"][0]["quantity"] = -1
    legacy_cases.append(("case_10a_usage_negative_quantity", l10a, False))

    l10b = _base_fixture()
    l10b["limits"]["dimensions"][0]["effective_limit"] = -5
    legacy_cases.append(("case_10b_limits_negative_effective_limit", l10b, False))

    l10c = _base_fixture()
    l10c["limits"]["dimensions"][0]["effective_limit"] = 1
    l10c["limits"]["dimensions"][0]["observed"] = 99
    legacy_cases.append(("case_10c_limits_observed_beyond_limit", l10c, True))

    l11 = _base_fixture()
    l11["limits"]["dimensions"] = [
        {
            "dimension": "bytes_read",
            "effective_limit": 123,
            "unit": "bytes",
            "source": "estate_default",
            "observed": 100,
            "enforced_by": "limiter",
        }
    ]
    l11["usage"]["reservation_ref"] = None
    l11["usage"]["reconciled_against_reservation"] = False
    legacy_cases.append(("case_11_single_limit_dimension_no_spend_dimension", l11, True))

    l12 = _base_fixture()
    for k in ["scope", "expenditure"]:
        l12["authority"][k]["group"] = ""
        l12["authority"][k]["rule"] = "quorum"
        l12["authority"][k]["decisions"] = [
            {
                "principal_id": "",
                "decision": "refused",
                "reason": "",
                "recorded_at": "2026-02-01T09:55:00Z",
                "receipt_ref": "",
            }
        ]
    legacy_cases.append(("case_12_all_refused_empty_group_principal_quorum_without_threshold", l12, False))

    l13 = _base_fixture()
    l13["identity"]["run_started_at"] = "2026-02-01T10:00:00Z"
    l13["identity"]["run_ended_at"] = "2026-02-01T09:00:00Z"
    l13["authority"]["scope"]["decisions"][0]["recorded_at"] = "2026-02-01T11:00:00Z"
    legacy_cases.append(("case_13_chronologically_impossible_but_well_formatted_timestamps", l13, True))

    l14 = _base_fixture()
    l14["evidence"]["re_performance"]["different_model_family"] = False
    l14["evidence"]["re_performance"]["sample_size"] = 3
    l14["evidence"]["re_performance"]["agreements"] = -7
    l14["evidence"]["re_performance"]["disagreements"] = 12
    legacy_cases.append(("case_14_reperformance_negative_and_sum_disagree", l14, True))

    l15 = _base_fixture()
    l15["supersession"]["revalidation"]["blocked"] = False
    l15["supersession"]["revalidation"]["triggers_fired"] = ["dial_change"]
    legacy_cases.append(("case_15_triggers_nonempty_blocked_false", l15, False))

    l16 = _base_fixture()
    l16["mocked_components"] = [{"component": "evidence-mock", "on_evidence_chain": True}]
    legacy_cases.append(("control_reject_on_evidence_chain_true", l16, False))

    l17 = _base_fixture()
    l17["output"]["reconciliation"]["unaccounted"] = 1
    legacy_cases.append(("control_reject_unaccounted_not_zero", l17, False))

    l18 = _base_fixture()
    l18["runtime"]["implementation_workspace_touched_data"] = True
    legacy_cases.append(("control_reject_workspace_touched_data_true", l18, False))

    l19 = _base_fixture()
    l19.pop("issuer")
    legacy_cases.append(("control_reject_required_field_missing", l19, False))

    l20 = _base_fixture()
    l20["unexpected_root"] = "not allowed"
    legacy_cases.append(("control_reject_extra_root_property", l20, False))

    l21 = _base_fixture()
    l21["identity"]["run_started_at"] = "not-a-date-time"
    legacy_cases.append(("control_reject_invalid_date_time_format", l21, False))

    assert len(legacy_cases) == 24
    for name, payload, expected in legacy_cases:
        _run_case(validator, "legacy24_rerun", name, payload, expected, legacy_results)
    matrix["sections"]["legacy24_rerun"] = legacy_results

    # Focused residual edge tests from request.
    residual_results = []

    r1 = _partially_live_fixture()
    r1["supersession"]["revalidation"]["triggers_fired"] = ["dial_change"]
    _run_case(
        validator,
        "residual_edges",
        "partial_live_peripheral_mock_blocked_false_nonempty_triggers",
        r1,
        True,
        residual_results,
    )

    r2 = _partially_live_fixture()
    r2["evidence"]["acceptance_script"]["result"] = "fail"
    _run_case(validator, "residual_edges", "partial_live_acceptance_script_fail", r2, True, residual_results)

    r3 = _base_fixture()
    r3["evidence"]["re_performance"]["agreements"] = -1
    r3["evidence"]["re_performance"]["disagreements"] = -2
    _run_case(validator, "residual_edges", "reperformance_negative_agreements_disagreements", r3, True, residual_results)

    r4 = _path_b_fixture()
    r4["evidence"]["refusal_demonstration"]["kind"] = "junk_stratum_unit"
    _run_case(validator, "residual_edges", "path_b_refusal_junk_stratum_kind", r4, True, residual_results)

    r5 = _path_c_admitted_fixture()
    r5["release_acceptance"]["criteria"] = [
        {
            "criterion_id": "criterion_dup",
            "measured_value": 0.99,
            "threshold": 0.95,
            "outcome": "met",
            "measurement_ref": "measurement_ref_dup_1_long",
        }
    ]
    _run_case(
        validator,
        "residual_edges",
        "path_c_admitted_one_metcriterion_duplicate_ids_semantic_only",
        r5,
        True,
        residual_results,
    )

    matrix["sections"]["focused_residual_edges"] = residual_results

    # Policy static checks (do not claim runtime policy enforcement).
    rows = policy.get("rows", [])
    assert policy.get("version") == "1.1"
    assert policy.get("default_when_no_row_matches") == "REFUSE"
    assert len(rows) == 5

    row_uncontrolled_frontier = next(
        r for r in rows if r.get("material_class") == "uncontrolled" and r.get("destination") == "frontier_model"
    )
    row_controlled_frontier = next(
        r for r in rows if r.get("material_class") == "controlled" and r.get("destination") == "frontier_model"
    )
    row_catchall = next(r for r in rows if r.get("material_class") == "any")

    assert row_uncontrolled_frontier.get("requires_dial", {}).get("external_crossing.uncontrolled") == "masked_permitted"
    assert row_controlled_frontier.get("requires_dial", {}).get("external_crossing.controlled_exception") == "available_by_ceremony"
    assert isinstance(row_controlled_frontier.get("per_call_exception", {}).get("requires_both"), list)
    assert len(row_controlled_frontier.get("per_call_exception", {}).get("requires_both", [])) == 2
    assert policy.get("pilot_setting", {}).get("external_crossing", {}).get("uncontrolled") == "masked_permitted"
    assert policy.get("pilot_setting", {}).get("external_crossing", {}).get("controlled_exception") == "unavailable"
    assert policy.get("unassessed_material", {}).get("routing") == "resolve as controlled for crossing decisions only"
    assert "eligibility" in policy.get("unassessed_material", {}).get("never_grants", [])

    stale_catchall_scalar = row_catchall.get("requires_dial", {}).get("external_crossing") == "refused"
    matrix["policy_static_checks"] = {
        "version": policy.get("version"),
        "default_when_no_row_matches": policy.get("default_when_no_row_matches"),
        "uncontrolled_masked_split_present": True,
        "controlled_exception_split_present": True,
        "requires_both_in_controlled_exception": row_controlled_frontier.get("per_call_exception", {}).get("requires_both", []),
        "pilot_setting_uncontrolled": policy.get("pilot_setting", {}).get("external_crossing", {}).get("uncontrolled"),
        "pilot_setting_controlled_exception": policy.get("pilot_setting", {}).get("external_crossing", {}).get("controlled_exception"),
        "unassessed_material_never_grants": policy.get("unassessed_material", {}).get("never_grants", []),
        "stale_catchall_scalar_external_crossing_refused_detected": stale_catchall_scalar,
        "note": "Static consistency finding only: default REFUSE still present; no resolver invoked; no runtime leak claim.",
    }

    # Hashes unchanged after all offline validation outputs.
    raw_schema_after = SCHEMA_PATH.read_bytes()
    raw_policy_after = POLICY_PATH.read_bytes()
    schema_sha_after = _sha256_bytes(raw_schema_after)
    policy_sha_after = _sha256_bytes(raw_policy_after)
    assert schema_sha_after == EXPECTED_SCHEMA_SHA256
    assert policy_sha_after == EXPECTED_POLICY_SHA256
    matrix["artifact_hashes_after"] = {
        "activation_certificate.schema.json": schema_sha_after,
        "crossing_decision_table.v1_1.json": policy_sha_after,
    }

    matrix["summary_counts"] = {
        "positives": len(positive_results),
        "claimed_repairs_and_controls": len(claimed_results),
        "legacy24_rerun": len(legacy_results),
        "focused_residual_edges": len(residual_results),
        "total_cases": len(positive_results) + len(claimed_results) + len(legacy_results) + len(residual_results),
    }

    matrix["classification"] = {
        "shape_repairs_verified": [
            "state-conditioned checks for LIVE-VERIFIED/PARTIALLY LIVE/LIVE-BLOCKED",
            "path-conditioned requirements for A/B/C",
            "admitted requires >=1 criteria and all met outcomes",
            "honest absence branch for not_measured",
            "minimum constraints on usage/limits/output counters",
            "approval groups require at least one approved decision",
        ],
        "residual_semantic_hardening_owned_by_E1": [
            "observed <= effective_limit",
            "manifest/denominator arithmetic invariants",
            "chronology ordering",
            "receipt/reference authenticity and authority resolution",
            "criterion identity quorum and duplicate-ID semantics",
            "re_performance non-negative agreements/disagreements",
            "canonical normalization for catch-all external_crossing scalar vs split object",
        ],
    }

    MATRIX_PATH.write_text(json.dumps(matrix, indent=2), encoding="utf-8")
