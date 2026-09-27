"""RED-first contract tests for services.northena.execution_models.

These tests encode architecture contracts before runtime implementation.
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest


DENOMINATOR_KINDS = ("source", "skill", "training", "evaluation")
BASELINE_MANIFEST = Path(
    "/app/assessment_workspace/notes/consolidated_fix_plan_20260926/"
    "architecture_verification/execution_spine_baseline_hash_manifest.json"
)


def _models_module():
    try:
        return importlib.import_module("services.northena.execution_models")
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing expected RED target module services.northena.execution_models: {exc}")


# Module/feature: denominator pin and baseline hash evidence artifact.
def test_denominator_kinds_and_baseline_manifest_are_pinned():
    assert set(DENOMINATOR_KINDS) == {"source", "skill", "training", "evaluation"}
    assert BASELINE_MANIFEST.exists(), "Missing execution spine baseline hash manifest"
    manifest = json.loads(BASELINE_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["denominator"] == list(DENOMINATOR_KINDS)
    assert manifest["hash_algorithm"] == "sha256"
    assert len(manifest["sealed_hashes"]) >= 3


# Module/feature: Request strict schema, mapping, and immutable digest contract.
def test_request_contract_enforces_kind_engine_mapping_and_digest_shape():
    mod = _models_module()
    req = mod.Request(
        request_id="req-1",
        tenant_id="DIGICOW",
        principal_id="principal-1",
        kind="source",
        engine="mtafiti",
        objective_sha256="a" * 64,
        input_refs=("akki://input/a",),
        scope_refs=("scope://x",),
        deadline_epoch=1,
    )
    digest = req.digest()
    assert isinstance(digest, str)
    assert len(digest) == 64

    with pytest.raises(Exception):
        mod.Request(
            request_id="req-2",
            tenant_id="DIGICOW",
            principal_id="principal-1",
            kind="skill",
            engine="mtafiti",  # strict kind/engine mismatch
            objective_sha256="b" * 64,
            input_refs=("akki://input/b",),
            scope_refs=("scope://x",),
            deadline_epoch=2,
        )


# Module/feature: Request must reject forbidden raw fields and non-Akki handles.
def test_request_forbids_raw_fields_and_non_akki_input_refs():
    mod = _models_module()

    with pytest.raises(Exception):
        mod.Request(
            request_id="req-raw",
            tenant_id="DIGICOW",
            principal_id="principal-1",
            kind="training",
            engine="targeta",
            objective_sha256="c" * 64,
            input_refs=("s3://bucket/key",),
            scope_refs=("scope://x",),
            deadline_epoch=3,
        )

    with pytest.raises(Exception):
        mod.Request(
            request_id="req-extra",
            tenant_id="DIGICOW",
            principal_id="principal-1",
            kind="evaluation",
            engine="targeta",
            objective_sha256="d" * 64,
            input_refs=("akki://input/d",),
            scope_refs=("scope://x",),
            deadline_epoch=4,
            raw_bytes="forbidden",
        )


# Module/feature: Authority binding contract and Held error surface.
def test_authority_contract_requires_exact_binding_and_future_expiry():
    mod = _models_module()
    authority = mod.Authority(
        authority_ref="auth-1",
        request_sha256="e" * 64,
        tenant_id="DIGICOW",
        principal_id="principal-1",
        scope_refs=("scope://x",),
        engine="solva",
        expires_epoch=9999999999,
        terms_ref="terms://dispatch/v1",
        policy_epoch=1,
    )
    assert authority.engine == "solva"

    with pytest.raises(Exception):
        mod.Held(reason_code="")


# Module/feature: Artifact + Usage lexical contracts and tenant/floor-safe labels.
def test_artifact_and_usage_contracts_enforce_labels_hashes_and_decimal_lexical():
    mod = _models_module()
    artifact = mod.Artifact(
        ref="akki://artifact/1",
        sha256="f" * 64,
        size_bytes=0,
        tenant_id="DIGICOW",
        class_label="non_factual",
    )
    assert artifact.ref.startswith("akki://")

    usage = mod.Usage(unit="gpu_seconds", quantity="1.25")
    assert usage.quantity == "1.25"

    with pytest.raises(Exception):
        mod.Usage(unit="gpu_seconds", quantity="-1")

    with pytest.raises(Exception):
        mod.Artifact(
            ref="akki://artifact/2",
            sha256="short",
            size_bytes=-1,
            tenant_id="DIGICOW",
            class_label="fact",
        )


# Module/feature: WorkerResult strict enums and evidence mode propagation shape.
def test_worker_result_contract_enforces_state_and_evidence_mode():
    mod = _models_module()
    artifact = mod.Artifact(
        ref="akki://artifact/ok",
        sha256="1" * 64,
        size_bytes=10,
        tenant_id="DIGICOW",
        class_label="utterance",
    )
    result = mod.WorkerResult(
        operation_key="op-1",
        request_sha256="2" * 64,
        executor_id="exec-1",
        fence=1,
        state="complete",
        receipt_ref="akki://receipt/1",
        artifacts=(artifact,),
        usage=(mod.Usage(unit="tokens", quantity="10"),),
        evidence_mode="MOCKED",
    )
    assert result.state == "complete"

    with pytest.raises(Exception):
        mod.WorkerResult(
            operation_key="op-2",
            request_sha256="3" * 64,
            executor_id="exec-1",
            fence=1,
            state="done",  # forbidden literal
            receipt_ref="akki://receipt/1",
            artifacts=(),
            usage=None,
            evidence_mode="measured",
        )
