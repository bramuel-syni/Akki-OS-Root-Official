"""RED contract tests for strict SubmitRequest model (services.portal_operational.models).

Note: this file has no live API calls. It validates the proposed model contract
in isolation once the module is implemented.
"""

from importlib import import_module

import pytest
from pydantic import ValidationError


def _load_submit_request_model():
    """Load SubmitRequest from the proposed module path.

    RED-first behavior: fail loudly while module/class is missing.
    """
    try:
        module = import_module("services.portal_operational.models")
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing module services.portal_operational.models: {exc}")

    SubmitRequest = getattr(module, "SubmitRequest", None)
    if SubmitRequest is None:
        pytest.fail("SubmitRequest class missing in services.portal_operational.models")
    return SubmitRequest


# Module/feature: strict model accepts exactly six DAP operations
def test_submit_request_accepts_only_canonical_six_operations():
    SubmitRequest = _load_submit_request_model()
    operations = [
        "browse_estate",
        "connect_workspace",
        "processed_intelligence",
        "fine_tune_model",
        "develop_skills",
        "download_raw_data",
    ]
    for op in operations:
        model = SubmitRequest(
            objective_text="Review retained RMS source scope",
            operation=op,
            units=["rms_mysql"],
            idempotency_key="red-unique-key-123456",
        )
        assert model.operation == op


# Module/feature: objective_text required
def test_submit_request_rejects_missing_or_empty_objective_text():
    SubmitRequest = _load_submit_request_model()
    with pytest.raises(ValidationError):
        SubmitRequest(
            operation="processed_intelligence",
            units=["rms_mysql"],
            idempotency_key="red-unique-key-123456",
        )
    with pytest.raises(ValidationError):
        SubmitRequest(
            objective_text="",
            operation="processed_intelligence",
            units=["rms_mysql"],
            idempotency_key="red-unique-key-123456",
        )


# Module/feature: units are distinct and bounded 1..50
def test_submit_request_rejects_units_outside_bounds_or_duplicates():
    SubmitRequest = _load_submit_request_model()
    with pytest.raises(ValidationError):
        SubmitRequest(
            objective_text="Review retained RMS source scope",
            operation="processed_intelligence",
            units=[],
            idempotency_key="red-unique-key-123456",
        )
    with pytest.raises(ValidationError):
        SubmitRequest(
            objective_text="Review retained RMS source scope",
            operation="processed_intelligence",
            units=["rms_mysql", "rms_mysql"],
            idempotency_key="red-unique-key-123456",
        )
    with pytest.raises(ValidationError):
        SubmitRequest(
            objective_text="Review retained RMS source scope",
            operation="processed_intelligence",
            units=[f"unit-{i}" for i in range(51)],
            idempotency_key="red-unique-key-123456",
        )


# Module/feature: idempotency key length 8..128
def test_submit_request_rejects_idempotency_key_outside_8_to_128():
    SubmitRequest = _load_submit_request_model()
    with pytest.raises(ValidationError):
        SubmitRequest(
            objective_text="Review retained RMS source scope",
            operation="processed_intelligence",
            units=["rms_mysql"],
            idempotency_key="short",
        )
    with pytest.raises(ValidationError):
        SubmitRequest(
            objective_text="Review retained RMS source scope",
            operation="processed_intelligence",
            units=["rms_mysql"],
            idempotency_key="k" * 129,
        )


# Module/feature: no caller identity/approval/result inputs allowed
def test_submit_request_forbids_identity_approval_and_result_fields():
    SubmitRequest = _load_submit_request_model()
    with pytest.raises(ValidationError):
        SubmitRequest(
            objective_text="Review retained RMS source scope",
            operation="processed_intelligence",
            units=["rms_mysql"],
            idempotency_key="red-unique-key-123456",
            principal_id="forged-principal",
            tenant_id="DIGICOW",
            approver_id="forged-approver",
            answer_stub="forged-answer",
            class_label="forged-class",
        )
