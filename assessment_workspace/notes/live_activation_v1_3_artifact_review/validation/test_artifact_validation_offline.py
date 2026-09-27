import copy
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


VALIDATION_DIR = Path(__file__).resolve().parent
ORIGINALS_DIR = VALIDATION_DIR.parent / "originals"
COUNTEREXAMPLE_DIR = VALIDATION_DIR / "counterexamples"
MATRIX_PATH = VALIDATION_DIR / "results_matrix.json"
SYNTHETIC_FIXTURE_PATH = VALIDATION_DIR / "synthetic_review_fixture.json"

SCHEMA_PATH = ORIGINALS_DIR / "activation_certificate.schema.json"
POLICY_PATH = ORIGINALS_DIR / "crossing_decision_table.v1.json"

EXPECTED_SCHEMA_SHA256 = "6bebe79c4d5db17db3bcf047c0512c749193bd7cc081e83bdaf7e5f6bbe8f0fa"
EXPECTED_POLICY_SHA256 = "f90cf6d7c36f3d4b89bc8bf099c990c223b5836c5cbdf282f70d781b69ba74f3"


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _read_json_bytes(path: Path):
    raw = path.read_bytes()
    return raw, json.loads(raw.decode("utf-8"))


def _ptr(exc) -> str:
    if not exc.path:
        return "/"
    return "/" + "/".join(str(p) for p in exc.path)


def _validate(validator: Draft202012Validator, payload: dict):
    errors = sorted(validator.iter_errors(payload), key=lambda e: (_ptr(e), e.message))
    return {
        "accepted": len(errors) == 0,
        "errors": [
            {
                "path": _ptr(err),
                "validator": err.validator,
                "message": err.message,
            }
            for err in errors
        ],
    }


def _load_base_fixture() -> dict:
    return json.loads(SYNTHETIC_FIXTURE_PATH.read_text(encoding="utf-8"))


def _build_format_checker() -> FormatChecker:
    checker = FormatChecker()

    @checker.checks("date-time")
    def _strict_datetime(value):
        if not isinstance(value, str):
            return True  # JSON Schema format applies to strings; null is type-checked separately.
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})", value):
            return False
        candidate = value.upper().replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(candidate).utcoffset() is not None
        except ValueError:
            return False

    return checker


def _mutated_cases(base: dict):
    cases = []

    c1 = copy.deepcopy(base)
    c1["mocked_components"] = [{"component": "peripheral-mock", "on_evidence_chain": False}]
    cases.append(("case_01_live_verified_peripheral_mock_nonempty", c1, True))

    c2 = copy.deepcopy(base)
    c2["supersession"]["revalidation"]["blocked"] = True
    c2["supersession"]["revalidation"]["triggers_fired"] = ["authority_revocation"]
    cases.append(("case_02_live_verified_blocked_true_with_revocation_trigger", c2, True))

    c3 = copy.deepcopy(base)
    c3["issuer"]["verification_status"] = "unverified"
    c3["issuer"]["signature"] = ""
    cases.append(("case_03_live_verified_issuer_unverified_empty_signature", c3, True))

    c4 = copy.deepcopy(base)
    c4["evidence"]["acceptance_script"]["result"] = "fail"
    cases.append(("case_04_live_verified_acceptance_script_fail", c4, True))

    c5 = copy.deepcopy(base)
    c5["identity"]["path"] = "C_training_with_evaluation"
    c5["release_acceptance"]["decision"] = "admitted"
    c5["release_acceptance"]["criteria"] = []
    c5["release_acceptance"]["acceptance_standard_ref"] = None
    c5["inputs"]["held_out_ref"] = None
    c5["runtime"]["recipe_ref"] = None
    c5["runtime"]["model_refs"] = []
    c5["authority"]["purposes_authorised"] = ["census"]
    cases.append(("case_05_path_c_release_admitted_minimal_semantics", c5, True))

    c6 = copy.deepcopy(base)
    c6["identity"]["path"] = "B_callable_skill"
    c6["evidence"]["refusal_demonstration"] = None
    cases.append(("case_06_path_b_refusal_demonstration_null", c6, True))

    c7a = copy.deepcopy(base)
    c7a["release_acceptance"]["criteria"] = [
        {
            "criterion_id": "hardcoded-criterion",
            "measured_value": "HARDCODED",
            "threshold": "expected",
            "outcome": "met",
            "measurement_ref": "",
        }
    ]
    cases.append(("case_07a_met_with_empty_measurement_ref", c7a, True))

    c7b = copy.deepcopy(base)
    c7b["release_acceptance"]["criteria"] = [
        {
            "criterion_id": "fabricated-criterion",
            "measured_value": "fabricated_value",
            "threshold": "fabricated_threshold",
            "outcome": "met",
            "measurement_ref": "fabricated://record/12345",
        }
    ]
    cases.append(("case_07b_met_with_fabricated_measurement_ref", c7b, True))

    c8 = copy.deepcopy(base)
    c8["release_acceptance"]["criteria"] = [
        {
            "criterion_id": "missing-measurement",
            "measured_value": None,
            "threshold": None,
            "outcome": "not_measured",
            "measurement_ref": "no-measurement",
        }
    ]
    cases.append(("case_08_not_measured_with_null_measured_value", c8, False))

    c9 = copy.deepcopy(base)
    c9["output"]["manifest_row_count"] = 100
    c9["output"]["denominator_count"] = 10
    c9["output"]["reconciliation"] = {
        "processed": -4,
        "refused_with_reason": 999,
        "unmeasured_with_reason": -3,
        "unaccounted": 0,
    }
    cases.append(("case_09_reconciliation_negative_and_mismatched_counts", c9, True))

    c10a = copy.deepcopy(base)
    c10a["usage"]["measured_quantities"][0]["quantity"] = -1
    cases.append(("case_10a_usage_negative_quantity", c10a, True))

    c10b = copy.deepcopy(base)
    c10b["limits"]["dimensions"][0]["effective_limit"] = -5
    cases.append(("case_10b_limits_negative_effective_limit", c10b, True))

    c10c = copy.deepcopy(base)
    c10c["limits"]["dimensions"][0]["effective_limit"] = 1
    c10c["limits"]["dimensions"][0]["observed"] = 99
    cases.append(("case_10c_limits_observed_beyond_limit", c10c, True))

    c11 = copy.deepcopy(base)
    c11["limits"]["dimensions"] = [
        {
            "dimension": "bytes_read",
            "effective_limit": 123,
            "unit": "bytes",
            "source": "estate_default",
            "observed": 100,
            "enforced_by": "limiter",
        }
    ]
    c11["usage"]["reservation_ref"] = None
    c11["usage"]["reconciled_against_reservation"] = False
    cases.append(("case_11_single_limit_dimension_no_spend_dimension", c11, True))

    c12 = copy.deepcopy(base)
    for k in ["scope", "expenditure"]:
        c12["authority"][k]["group"] = ""
        c12["authority"][k]["rule"] = "quorum"
        c12["authority"][k]["decisions"] = [
            {
                "principal_id": "",
                "decision": "refused",
                "reason": "",
                "recorded_at": "2026-02-01T09:55:00Z",
                "receipt_ref": "",
            }
        ]
    cases.append(("case_12_all_refused_empty_group_principal_quorum_without_threshold", c12, True))

    c13 = copy.deepcopy(base)
    c13["identity"]["run_started_at"] = "2026-02-01T10:00:00Z"
    c13["identity"]["run_ended_at"] = "2026-02-01T09:00:00Z"
    c13["authority"]["scope"]["decisions"][0]["recorded_at"] = "2026-02-01T11:00:00Z"
    c13["inputs"]["held_out_ref"]["fixed_before_training_at"] = "2026-02-01T10:15:00Z"
    cases.append(("case_13_chronologically_impossible_but_well_formatted_timestamps", c13, True))

    c14 = copy.deepcopy(base)
    c14["evidence"]["re_performance"]["different_model_family"] = False
    c14["evidence"]["re_performance"]["sample_size"] = 3
    c14["evidence"]["re_performance"]["agreements"] = -7
    c14["evidence"]["re_performance"]["disagreements"] = 12
    cases.append(("case_14_reperformance_negative_and_sum_disagree", c14, True))

    c15 = copy.deepcopy(base)
    c15["supersession"]["revalidation"]["blocked"] = False
    c15["supersession"]["revalidation"]["triggers_fired"] = ["dial_change"]
    cases.append(("case_15_triggers_nonempty_blocked_false", c15, True))

    ctrl1 = copy.deepcopy(base)
    ctrl1["mocked_components"] = [{"component": "evidence-mock", "on_evidence_chain": True}]
    cases.append(("control_reject_on_evidence_chain_true", ctrl1, False))

    ctrl2 = copy.deepcopy(base)
    ctrl2["output"]["reconciliation"]["unaccounted"] = 1
    cases.append(("control_reject_unaccounted_not_zero", ctrl2, False))

    ctrl3 = copy.deepcopy(base)
    ctrl3["runtime"]["implementation_workspace_touched_data"] = True
    cases.append(("control_reject_workspace_touched_data_true", ctrl3, False))

    ctrl4 = copy.deepcopy(base)
    ctrl4.pop("issuer")
    cases.append(("control_reject_required_field_missing", ctrl4, False))

    ctrl5 = copy.deepcopy(base)
    ctrl5["unexpected_root"] = "not allowed"
    cases.append(("control_reject_extra_root_property", ctrl5, False))

    ctrl6 = copy.deepcopy(base)
    ctrl6["identity"]["run_started_at"] = "not-a-date-time"
    cases.append(("control_reject_invalid_date_time_format", ctrl6, False))

    return cases


def test_schema_policy_and_counterexamples_offline():
    raw_schema, schema = _read_json_bytes(SCHEMA_PATH)
    raw_policy, policy = _read_json_bytes(POLICY_PATH)

    schema_sha = _sha256_bytes(raw_schema)
    policy_sha = _sha256_bytes(raw_policy)

    assert schema_sha == EXPECTED_SCHEMA_SHA256
    assert policy_sha == EXPECTED_POLICY_SHA256

    Draft202012Validator.check_schema(schema)
    format_checker = _build_format_checker()
    assert format_checker.conforms(None, "date-time")
    assert not format_checker.conforms("2026-02-01", "date-time")
    validator = Draft202012Validator(schema, format_checker=format_checker)

    base_fixture = _load_base_fixture()
    base_result = _validate(validator, base_fixture)
    assert base_result["accepted"], f"Synthetic review fixture invalid: {base_result['errors']}"

    COUNTEREXAMPLE_DIR.mkdir(parents=True, exist_ok=True)

    cases = _mutated_cases(base_fixture)
    case_results = []

    for name, payload, expected_accepted in cases:
        payload_path = COUNTEREXAMPLE_DIR / f"{name}.json"
        payload_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

        result = _validate(validator, payload)
        case_results.append(
            {
                "case": name,
                "expected_accepted": expected_accepted,
                "accepted": result["accepted"],
                "payload_path": str(payload_path),
                "errors": result["errors"],
            }
        )

        assert result["accepted"] == expected_accepted, (
            f"Case {name} expected accepted={expected_accepted} got accepted={result['accepted']}"
        )

    rows = policy.get("rows", [])
    assert len(rows) == 5
    assert policy.get("default_when_no_row_matches") == "REFUSE"

    for key in ["row_id", "priority", "conditions", "scope"]:
        assert key not in policy

    forbidden_row_keys = {"row_id", "priority", "conditions", "scope"}
    for row in rows:
        assert not (forbidden_row_keys & set(row.keys()))

    uncontrolled_frontier = next(
        r for r in rows if r.get("material_class") == "uncontrolled" and r.get("destination") == "frontier_model"
    )
    controlled_frontier = next(
        r for r in rows if r.get("material_class") == "controlled" and r.get("destination") == "frontier_model"
    )

    assert uncontrolled_frontier.get("requires_dial", {}).get("external_crossing") == "masked_permitted"
    assert controlled_frontier.get("requires_dial", {}).get("external_crossing") == "masked_permitted"
    assert isinstance(controlled_frontier.get("ceremony"), str)

    for row in rows:
        per_call_exception = row.get("per_call_exception")
        if isinstance(per_call_exception, dict):
            assert "tenant_id" not in per_call_exception
            assert "class_id" not in per_call_exception

    matrix = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "method": {
            "schema_check": "Draft202012Validator.check_schema",
            "validator": "Draft202012Validator",
            "format_checker": "FormatChecker",
            "format_checker_note": "custom timezone-aware RFC3339-shaped date-time checker; not a full format-conformance suite; non-string format instances defer to type validation",
            "python_jsonschema_api": "jsonschema",
        },
        "artifact_hashes": {
            "activation_certificate.schema.json": schema_sha,
            "crossing_decision_table.v1.json": policy_sha,
        },
        "limits": [
            "Static artifact inspection only.",
            "Schema shape validation does not prove authenticity, existence, or runtime enforcement.",
            "No resolver/execution engine is present in these artifacts; matching behavior is not executed here.",
            "Boolean const checks are declaration constraints only, not real-world observation.",
        ],
        "synthetic_review_fixture": {
            "label": "SYNTHETIC REVIEW FIXTURE (fictional; not issued certificate; never app-ingested)",
            "path": str(SYNTHETIC_FIXTURE_PATH),
            "accepted": base_result["accepted"],
        },
        "policy_assertions": {
            "rows_count": len(rows),
            "default_when_no_row_matches": policy.get("default_when_no_row_matches"),
            "uncontrolled_frontier_external_crossing": uncontrolled_frontier.get("requires_dial", {}).get("external_crossing"),
            "controlled_frontier_external_crossing": controlled_frontier.get("requires_dial", {}).get("external_crossing"),
            "ceremony_field_type": type(controlled_frontier.get("ceremony")).__name__,
            "top_level_embellishment_keys_absent": True,
        },
        "cases": case_results,
    }

    MATRIX_PATH.write_text(json.dumps(matrix, indent=2), encoding="utf-8")
