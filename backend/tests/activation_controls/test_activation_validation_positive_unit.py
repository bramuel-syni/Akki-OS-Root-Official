"""Positive/negative evidence-port unit contracts for activation validation."""

from __future__ import annotations

import asyncio
import copy
from datetime import timedelta

import pytest

from services.activation.evidence import EvidenceVerdict, reference_set
from services.activation.validation import validate_certificate

from test_activation_validation_red import _base_document, _sha256_doc, _utc_now


TENANT_ID = "tenant_SYNTHETIC_blue"
PRINCIPAL_ID = "principal_SYNTHETIC_1"


class _Verifier:
    def __init__(self, verdict: EvidenceVerdict):
        self._verdict = verdict
        self.called = False

    async def verify(self, _document, *, tenant_id, principal_id):
        _ = (tenant_id, principal_id)
        self.called = True
        return self._verdict


class _SlowVerifier:
    def __init__(self, verdict: EvidenceVerdict, delay_seconds: float):
        self._verdict = verdict
        self._delay_seconds = delay_seconds

    async def verify(self, _document, *, tenant_id, principal_id):
        _ = (tenant_id, principal_id)
        await asyncio.sleep(self._delay_seconds)
        return self._verdict


def _owner_aligned_document() -> dict:
    doc = copy.deepcopy(_base_document())
    doc["identity"].pop("proposing_principal_id", None)
    doc["identity"]["tenant_id"] = TENANT_ID
    doc["identity"]["estate_id"] = TENANT_ID
    return doc


def _verdict_for(document: dict, **overrides) -> EvidenceVerdict:
    now = _utc_now()
    payload = {
        "certificate_sha256": _sha256_doc(document),
        "tenant_id": document["identity"]["estate_id"],
        "principal_id": PRINCIPAL_ID,
        "verified_refs": tuple(sorted(reference_set(document))),
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
        "expires_epoch": int((now + timedelta(hours=1)).timestamp()),
    }
    payload.update(overrides)
    return EvidenceVerdict(**payload)


# Module/feature: positive flow proves schema+semantics true before evidence and yields live-verified.
def test_validation_can_be_positive_with_typed_server_owned_evidence_verdict():
    document = _owner_aligned_document()
    verifier = _Verifier(_verdict_for(document))
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
    assert result.evidence_verified is True
    assert result.derived_state == "LIVE-VERIFIED"
    assert result.issues == ()


# Module/feature: evidence verifier is not called when schema gate fails.
def test_schema_failure_short_circuits_before_evidence_verifier_is_called():
    document = _owner_aligned_document()
    document["certificate_id"] = "bad"
    verifier = _Verifier(_verdict_for(_owner_aligned_document()))

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
    assert verifier.called is False
    assert result.schema_valid is False
    assert result.semantics_valid is False
    assert any(i.code.startswith("SCHEMA_") for i in result.issues)


# Module/feature: evidence verifier is not called when semantic gate fails.
def test_semantic_failure_short_circuits_before_evidence_verifier_is_called():
    document = _owner_aligned_document()
    document["output"]["denominator_count"] = 99
    verifier = _Verifier(_verdict_for(_owner_aligned_document()))

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
    assert verifier.called is False
    assert result.schema_valid is True
    assert result.semantics_valid is False
    assert any(i.code == "UNIT_RECONCILIATION_MISMATCH" for i in result.issues)


# Module/feature: derived state must bind to computed state and never trust submitted label.
def test_state_consistency_rejects_before_evidence_when_shape_already_contradicts_label():
    document = _owner_aligned_document()
    # The owner schema already enforces these combinations; do not weaken it
    # merely to reach a redundant later state-derivation defence.
    document["state"] = "PARTIALLY LIVE"
    verifier = _Verifier(_verdict_for(document))

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
    assert result.valid is False
    assert result.schema_valid is False
    assert result.semantics_valid is False
    assert verifier.called is False
    assert any(i.code == "SCHEMA_MINITEMS" and i.path == "/mocked_components" for i in result.issues)


# Module/feature: async evidence verifier obeys bounded timeout and fails closed.
def test_evidence_verifier_timeout_returns_unavailable_issue():
    document = _owner_aligned_document()
    verifier = _SlowVerifier(_verdict_for(document), delay_seconds=0.05)

    result = asyncio.run(
        validate_certificate(
            document,
            tenant_id=TENANT_ID,
            principal_id=PRINCIPAL_ID,
            evidence=verifier,
            timeout_seconds=0.01,
            now=_utc_now(),
        )
    )
    assert result.valid is False
    assert result.schema_valid is True
    assert result.semantics_valid is True
    assert any(i.code == "EVIDENCE_VERIFIER_UNAVAILABLE" for i in result.issues)


# Module/feature: any false/MOCKED proof and unresolved refs must fail closed.
@pytest.mark.parametrize(
    "name,override,expected_issue",
    [
        pytest.param("mocked_mode", {"evidence_mode": "MOCKED"}, "EVIDENCE_NOT_VERIFIED", id="mocked_mode"),
        pytest.param("one_false_check", {"request_verified": False}, "EVIDENCE_NOT_VERIFIED", id="one_false_check"),
        pytest.param("missing_refs", {"verified_refs": ()}, "EVIDENCE_REFERENCES_UNRESOLVED", id="missing_refs"),
        pytest.param("binding_mismatch", {"tenant_id": "OTHER"}, "EVIDENCE_BINDING_MISMATCH", id="binding_mismatch"),
        pytest.param("principal_mismatch", {"principal_id": "OTHER"}, "EVIDENCE_BINDING_MISMATCH", id="principal_mismatch"),
        pytest.param("digest_mismatch", {"certificate_sha256": "f" * 64}, "EVIDENCE_BINDING_MISMATCH", id="digest_mismatch"),
    ],
)
def test_evidence_fail_closed_variants(name, override, expected_issue):
    _ = name
    document = _owner_aligned_document()
    verifier = _Verifier(_verdict_for(document, **override))
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
    assert result.valid is False
    assert result.schema_valid is True
    assert result.semantics_valid is True
    assert any(i.code == expected_issue for i in result.issues)


# Module/feature: evidence expiry after await must fail closed.
def test_evidence_expired_after_await_is_rejected():
    document = _owner_aligned_document()
    expires_soon = int((_utc_now() + timedelta(milliseconds=20)).timestamp())
    verifier = _SlowVerifier(_verdict_for(document, expires_epoch=expires_soon), delay_seconds=0.05)

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
    assert result.valid is False
    assert result.schema_valid is True
    assert result.semantics_valid is True
    assert any(i.code == "EVIDENCE_EXPIRED" for i in result.issues)
