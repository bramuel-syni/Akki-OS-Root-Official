"""Supplemental path-B/C activation certificate model-path coverage after RCA."""

from __future__ import annotations

import asyncio
import copy

from services.activation.validation import validate_certificate

from test_activation_validation_positive_unit import (
    PRINCIPAL_ID,
    TENANT_ID,
    _owner_aligned_document,
    _utc_now,
    _verdict_for,
)


class RecordingVerifier:
    """Synthetic server-owned verifier used only for code-orchestration coverage."""

    def __init__(self, verdict):
        self.verdict = verdict
        self.called = False

    async def verify(self, _document, *, tenant_id, principal_id):
        _ = (tenant_id, principal_id)
        self.called = True
        return self.verdict


def _valid_evidence_payload(document: dict, **overrides):
    return _verdict_for(document, **overrides)


def _path_b_document() -> dict:
    doc = _owner_aligned_document()
    doc["identity"]["path"] = "B_callable_skill"
    doc["authority"]["purposes_authorised"] = ["answering"]
    doc["release_acceptance"]["decision"] = "refused"
    doc["release_acceptance"]["recorded_at"] = "2026-02-01T10:40:00Z"
    doc["release_acceptance"]["criteria"] = [
        {
            "criterion_id": "criterion_b_1",
            "measured_value": "out-of-scope",
            "threshold": "in-scope-answer",
            "outcome": "failed",
            "measurement_ref": "measure_ref_b_criterion_1",
        }
    ]
    doc["release_acceptance"]["prerequisites"] = [
        {
            "prerequisite_id": "domain-policy-b",
            "extension_version": "ext-1.1",
            "outcome": "failed",
            "record_ref": "prereq_record_ref_b_1",
        }
    ]
    doc["runtime"]["model_refs"] = [
        {
            "registry_id": "registry_model_b_1",
            "hash": "3" * 64,
            "version": "v1.0.0",
            "licence_ref": "licence_ref_b_1",
        }
    ]
    doc["evidence"]["refusal_demonstration"] = {
        "kind": "out_of_scope_question",
        "request_ref": "request_ref_b_1",
        "reason_stated": "Question outside admitted scope",
        "receipt_ref": "refusal_receipt_ref_b_1",
    }
    return doc


def _path_c_document(*, decision: str = "admitted") -> dict:
    doc = _owner_aligned_document()
    doc["identity"]["path"] = "C_training_with_evaluation"
    doc["authority"]["purposes_authorised"] = ["training", "evaluation"]
    doc["release_acceptance"]["decision"] = decision
    doc["release_acceptance"]["recorded_at"] = "2026-02-01T10:40:00Z"
    doc["release_acceptance"]["acceptance_standard_ref"] = "acceptance-standard-v1.1"
    doc["release_acceptance"]["criteria"] = [
        {
            "criterion_id": "criterion_c_1",
            "measured_value": 0.991,
            "threshold": 0.95,
            "outcome": "met",
            "measurement_ref": "measure_ref_c_1",
        },
        {
            "criterion_id": "criterion_c_2",
            "measured_value": 0.978,
            "threshold": 0.95,
            "outcome": "met",
            "measurement_ref": "measure_ref_c_2",
        },
        {
            "criterion_id": "criterion_c_3",
            "measured_value": True,
            "threshold": True,
            "outcome": "met",
            "measurement_ref": "measure_ref_c_3",
        },
        {
            "criterion_id": "criterion_c_4",
            "measured_value": "pass",
            "threshold": "pass",
            "outcome": "met",
            "measurement_ref": "measure_ref_c_4",
        },
        {
            "criterion_id": "criterion_c_5",
            "measured_value": 9,
            "threshold": 6,
            "outcome": "met",
            "measurement_ref": "measure_ref_c_5",
        },
        {
            "criterion_id": "criterion_c_6",
            "measured_value": "ok",
            "threshold": "ok",
            "outcome": "met",
            "measurement_ref": "measure_ref_c_6",
        },
    ]
    doc["release_acceptance"]["prerequisites"] = [
        {
            "prerequisite_id": "domain-governance-c",
            "extension_version": "ext-2.3",
            "outcome": "met",
            "record_ref": "prereq_record_ref_c_1",
        }
    ]
    doc["runtime"]["model_refs"] = [
        {
            "registry_id": "registry_model_c_1",
            "hash": "4" * 64,
            "version": "v2.0.0",
            "licence_ref": "licence_ref_c_1",
        }
    ]
    doc["runtime"]["recipe_ref"] = "recipe_ref_c_1"
    doc["inputs"]["held_out_ref"] = {
        "custodian_principal_id": "custodian_c_1",
        "split_protocol": "chronological",
        "seed": "seed_c_1",
        "fixed_before_training_at": "2026-02-01T09:00:00Z",
        "selection_hash": "5" * 64,
    }
    doc["evidence"]["refusal_demonstration"] = {
        "kind": "unauthorised_manifest_unit",
        "request_ref": "request_ref_c_1",
        "reason_stated": "Synthetic refusal evidence",
        "receipt_ref": "refusal_receipt_ref_c_1",
    }
    return doc


# Module/feature: Path B real-shaped complete evidence can pass end-to-end orchestration.
def test_path_b_real_shape_complete_proof_valid_true_with_synthetic_verdict():
    document = _path_b_document()
    verifier = RecordingVerifier(_valid_evidence_payload(document))

    result = asyncio.run(
        validate_certificate(
            document,
            tenant_id=TENANT_ID,
            principal_id=PRINCIPAL_ID,
            evidence=verifier,
            timeout_seconds=1,
            now=_utc_now(),
        )
    )
    assert verifier.called is True
    assert result.valid is True
    assert result.schema_valid is True
    assert result.semantics_valid is True


# Module/feature: Path B without bound server verifier must hold despite passing shape+semantics.
def test_path_b_missing_bound_server_proof_is_hold_with_schema_and_semantics_true():
    document = _path_b_document()
    result = asyncio.run(
        validate_certificate(
            document,
            tenant_id=TENANT_ID,
            principal_id=PRINCIPAL_ID,
            now=_utc_now(),
        )
    )
    assert result.valid is False
    assert result.schema_valid is True
    assert result.semantics_valid is True
    assert any(i.code == "EVIDENCE_VERIFIER_NOT_BOUND" for i in result.issues)


# Module/feature: Path B refusal kind must follow authoritative shape constraints.
def test_path_b_wrong_refusal_kind_is_schema_refusal():
    document = _path_b_document()
    document["evidence"]["refusal_demonstration"]["kind"] = "junk_stratum_unit"
    result = asyncio.run(
        validate_certificate(
            document,
            tenant_id=TENANT_ID,
            principal_id=PRINCIPAL_ID,
            now=_utc_now(),
        )
    )
    assert result.valid is False
    assert result.schema_valid is False
    assert any(i.code.startswith("SCHEMA_") for i in result.issues)


# Module/feature: Path C admitted with six unique criteria and met domain prerequisite can be valid.
def test_path_c_admitted_six_unique_criteria_with_models_recipe_heldout_valid_true():
    document = _path_c_document(decision="admitted")
    verifier = RecordingVerifier(_valid_evidence_payload(document))
    result = asyncio.run(
        validate_certificate(
            document,
            tenant_id=TENANT_ID,
            principal_id=PRINCIPAL_ID,
            evidence=verifier,
            timeout_seconds=1,
            now=_utc_now(),
        )
    )
    assert verifier.called is True
    assert result.valid is True
    assert result.schema_valid is True
    assert result.semantics_valid is True


# Module/feature: Path C refused with one honest not_measured criterion remains shape-safe and semantically valid.
def test_path_c_refused_one_honest_not_measured_schema_semantics_true_without_proof():
    document = _path_c_document(decision="refused")
    document["release_acceptance"]["criteria"][0] = {
        "criterion_id": "criterion_c_honest_absence",
        "measured_value": None,
        "threshold": None,
        "outcome": "not_measured",
        "measurement_ref": None,
    }
    result = asyncio.run(
        validate_certificate(
            document,
            tenant_id=TENANT_ID,
            principal_id=PRINCIPAL_ID,
            now=_utc_now(),
        )
    )
    assert result.valid is False
    assert result.schema_valid is True
    assert result.semantics_valid is True
    assert any(i.code == "EVIDENCE_VERIFIER_NOT_BOUND" for i in result.issues)


# Module/feature: Path C refused can still pass verification under synthetic proof orchestration.
def test_path_c_refused_with_complete_synthetic_proof_valid_true_code_orchestration_only():
    document = _path_c_document(decision="refused")
    document["release_acceptance"]["criteria"][0] = {
        "criterion_id": "criterion_c_honest_absence",
        "measured_value": None,
        "threshold": None,
        "outcome": "not_measured",
        "measurement_ref": None,
    }
    verifier = RecordingVerifier(_valid_evidence_payload(document))
    result = asyncio.run(
        validate_certificate(
            document,
            tenant_id=TENANT_ID,
            principal_id=PRINCIPAL_ID,
            evidence=verifier,
            timeout_seconds=1,
            now=_utc_now(),
        )
    )
    assert verifier.called is True
    assert result.valid is True
    assert result.schema_valid is True
    assert result.semantics_valid is True


# Module/feature: held-out fixed timestamp after execution start must fail with structured chronology issue.
def test_path_c_heldout_fixed_after_training_is_structured_chronology_failure():
    document = _path_c_document(decision="admitted")
    document["inputs"]["held_out_ref"]["fixed_before_training_at"] = "2026-02-01T10:05:00Z"
    result = asyncio.run(
        validate_certificate(
            document,
            tenant_id=TENANT_ID,
            principal_id=PRINCIPAL_ID,
            now=_utc_now(),
        )
    )
    assert result.valid is False
    assert result.schema_valid is True
    assert result.semantics_valid is False
    assert any(i.code == "HELDOUT_NOT_FROZEN_BEFORE_RUN" for i in result.issues)


# Module/feature: admitted C path requires met prerequisites; failed prerequisite blocks admission.
def test_path_c_domain_prerequisite_failed_blocks_admission_structuredly():
    document = _path_c_document(decision="admitted")
    document["release_acceptance"]["prerequisites"][0]["outcome"] = "failed"
    document["release_acceptance"]["prerequisites"][0]["record_ref"] = "prereq_record_ref_c_failed"
    result = asyncio.run(
        validate_certificate(
            document,
            tenant_id=TENANT_ID,
            principal_id=PRINCIPAL_ID,
            now=_utc_now(),
        )
    )
    assert result.valid is False
    assert result.schema_valid is False
    assert result.semantics_valid is False
    assert any(i.code == "SCHEMA_CONST" and i.path.endswith("/prerequisites/0/outcome") for i in result.issues)


# Module/feature: not_measured domain prerequisite with null record is schema-safe for refused C path.
def test_path_c_prerequisite_not_measured_nullable_record_schema_safe():
    document = _path_c_document(decision="refused")
    document["release_acceptance"]["prerequisites"][0] = {
        "prerequisite_id": "domain-governance-c",
        "extension_version": "ext-2.3",
        "outcome": "not_measured",
        "record_ref": None,
    }
    result = asyncio.run(
        validate_certificate(
            document,
            tenant_id=TENANT_ID,
            principal_id=PRINCIPAL_ID,
            now=_utc_now(),
        )
    )
    assert result.valid is False
    assert result.schema_valid is True
    assert result.semantics_valid is True
    assert any(i.code == "EVIDENCE_VERIFIER_NOT_BOUND" for i in result.issues)


# Module/feature: duplicate/five criteria and wrong purpose produce structured semantic refusals.
def test_path_c_duplicate_criteria_ids_refused_with_structured_issue():
    document = _path_c_document(decision="admitted")
    document["release_acceptance"]["criteria"][1]["criterion_id"] = "criterion_c_1"
    result = asyncio.run(
        validate_certificate(
            document,
            tenant_id=TENANT_ID,
            principal_id=PRINCIPAL_ID,
            now=_utc_now(),
        )
    )
    assert result.valid is False
    assert result.schema_valid is True
    assert result.semantics_valid is False
    assert any(i.code == "ADOPTED_SIX_CRITERIA_REQUIRED" for i in result.issues)


# Module/feature: exactly six unique criteria are required for path C acceptance evaluation.
def test_path_c_only_five_criteria_refused_with_structured_issue():
    document = _path_c_document(decision="admitted")
    document["release_acceptance"]["criteria"] = document["release_acceptance"]["criteria"][:5]
    result = asyncio.run(
        validate_certificate(
            document,
            tenant_id=TENANT_ID,
            principal_id=PRINCIPAL_ID,
            now=_utc_now(),
        )
    )
    assert result.valid is False
    assert result.schema_valid is True
    assert result.semantics_valid is False
    assert any(i.code == "ADOPTED_SIX_CRITERIA_REQUIRED" for i in result.issues)


# Module/feature: path C needs both training and evaluation purposes.
def test_path_c_wrong_purpose_refused_with_structured_issue():
    document = _path_c_document(decision="admitted")
    document["authority"]["purposes_authorised"] = ["training"]
    result = asyncio.run(
        validate_certificate(
            document,
            tenant_id=TENANT_ID,
            principal_id=PRINCIPAL_ID,
            now=_utc_now(),
        )
    )
    assert result.valid is False
    assert result.schema_valid is True
    assert result.semantics_valid is False
    assert any(i.code == "PURPOSE_NOT_AUTHORISED" for i in result.issues)


# Module/feature: duplicate voters and collapsed approval groups must be caught as structured semantics issues.
def test_duplicate_voter_and_collapsed_approval_group_are_refused_structuredly():
    document = _path_c_document(decision="admitted")
    duplicate = copy.deepcopy(document["authority"]["scope"]["decisions"][0])
    duplicate["receipt_ref"] = "receipt_scope_000002_long"
    document["authority"]["scope"]["decisions"].append(duplicate)
    document["authority"]["expenditure"]["group"] = document["authority"]["scope"]["group"]
    result = asyncio.run(
        validate_certificate(
            document,
            tenant_id=TENANT_ID,
            principal_id=PRINCIPAL_ID,
            now=_utc_now(),
        )
    )
    codes = {i.code for i in result.issues}
    assert result.valid is False
    assert result.schema_valid is True
    assert result.semantics_valid is False
    assert "DUPLICATE_APPROVAL_VOTER" in codes
    assert "APPROVAL_GROUPS_COLLAPSED" in codes
