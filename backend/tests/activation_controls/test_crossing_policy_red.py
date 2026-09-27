"""RED-first contracts for activation crossing-policy typed context and decision rules."""

from __future__ import annotations

import copy
import importlib
from decimal import Decimal

import pytest


def _module(name: str):
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing expected RED target module {name}: {exc}")


def _valid_context_payload() -> dict:
    return {
        "estate_id": "tenant_SYNTHETIC_blue",
        "request_sha256": "a" * 64,
        "custody_class": "uncontrolled",
        "assessment_state": "assessed",
        "destination": "local",
        "external_crossing": {
            "uncontrolled": "masked_permitted",
            "controlled_exception": "unavailable",
        },
        "purpose_authority_ref": "purpose://auth/1",
        "classification_ref": "class://a/1",
        "policy_ref": "policy://crossing/1.1",
        "ceremony_ref": None,
        "ceremony_estate_id": None,
        "ceremony_class": None,
        "call_authority_ref": None,
        "call_request_sha256": None,
        "call_estate_id": None,
        "call_class": None,
        "disclosure_authority_ref": "disclosure://auth/1",
        "spend_authority_ref": "spend://auth/1",
        "expires_epoch": 4_102_444_800,
        "external_cost_usd": Decimal("0"),
        "external_budget_usd": Decimal("0"),
        "evidence_mode": "measured",
    }


# Module/feature: strict typed/frozen CrossingContext + decision response surface.
def test_crossing_module_surface_and_frozen_typed_context_contract():
    crossing_mod = _module("services.activation.crossing")
    assert hasattr(crossing_mod, "CrossingContext")
    assert hasattr(crossing_mod, "decide_crossing")

    context = crossing_mod.CrossingContext(**_valid_context_payload())
    with pytest.raises(Exception):
        context.estate_id = "other"

    decision = crossing_mod.decide_crossing(context, now_epoch=1_800_000_000)
    for field_name in ("allowed", "reason_code", "mask_required", "execution_authorized", "effective_custody"):
        assert hasattr(decision, field_name)
    assert decision.execution_authorized is False


# Module/feature: typed schema rejects extra keys and legacy scalar external_crossing dial.
def test_crossing_context_rejects_extras_and_legacy_scalar_dial_shape():
    crossing_mod = _module("services.activation.crossing")

    bad_extra = _valid_context_payload()
    bad_extra["unexpected"] = "x"
    with pytest.raises(Exception):
        crossing_mod.CrossingContext(**bad_extra)

    bad_scalar = _valid_context_payload()
    bad_scalar["external_crossing"] = "refused"
    with pytest.raises(Exception):
        crossing_mod.CrossingContext(**bad_scalar)


# Module/feature: key deny/allow matrix for local/frontier + assessed/unassessed + mock/expiry + budget/cost.
@pytest.mark.parametrize(
    "name,mutator,expected_allowed,expected_mask",
    [
        pytest.param(
            "assessed_local_real_refs_can_allow_no_mask",
            lambda d: None,
            True,
            False,
            id="assessed_local_real_refs_can_allow_no_mask",
        ),
        pytest.param(
            "expired_context_denies",
            lambda d: d.__setitem__("expires_epoch", 1),
            False,
            False,
            id="expired_context_denies",
        ),
        pytest.param(
            "mocked_evidence_denies",
            lambda d: d.__setitem__("evidence_mode", "MOCKED"),
            False,
            False,
            id="mocked_evidence_denies",
        ),
        pytest.param(
            "unassessed_always_deny_but_stays_controlled_effective",
            lambda d: d.__setitem__("assessment_state", "unassessed"),
            False,
            False,
            id="unassessed_always_deny_but_stays_controlled_effective",
        ),
        pytest.param(
            "frontier_uncontrolled_requires_mask_and_refs",
            lambda d: (
                d.__setitem__("destination", "frontier"),
                d.__setitem__("custody_class", "uncontrolled"),
                d.__setitem__("external_cost_usd", Decimal("1")),
                d.__setitem__("external_budget_usd", Decimal("2")),
            ),
            True,
            True,
            id="frontier_uncontrolled_requires_mask_and_refs",
        ),
        pytest.param(
            "frontier_uncontrolled_positive_cost_with_zero_budget_denies",
            lambda d: (
                d.__setitem__("destination", "frontier"),
                d.__setitem__("custody_class", "uncontrolled"),
                d.__setitem__("external_cost_usd", Decimal("1")),
                d.__setitem__("external_budget_usd", Decimal("0")),
            ),
            False,
            False,
            id="frontier_uncontrolled_positive_cost_with_zero_budget_denies",
        ),
        pytest.param(
            "frontier_uncontrolled_negative_cost_denies",
            lambda d: (
                d.__setitem__("destination", "frontier"),
                d.__setitem__("custody_class", "uncontrolled"),
                d.__setitem__("external_cost_usd", Decimal("-1")),
                d.__setitem__("external_budget_usd", Decimal("2")),
            ),
            False,
            False,
            id="frontier_uncontrolled_negative_cost_denies",
        ),
        pytest.param(
            "controlled_frontier_exception_unavailable_denies_even_with_call_refs",
            lambda d: (
                d.__setitem__("destination", "frontier"),
                d.__setitem__("custody_class", "controlled"),
                d["external_crossing"].__setitem__("controlled_exception", "unavailable"),
                d.__setitem__("call_authority_ref", "call://auth/1"),
                d.__setitem__("call_request_sha256", "b" * 64),
                d.__setitem__("call_estate_id", d["estate_id"]),
                d.__setitem__("call_class", "controlled"),
            ),
            False,
            False,
            id="controlled_frontier_exception_unavailable_denies_even_with_call_refs",
        ),
        pytest.param(
            "controlled_frontier_exception_available_requires_ceremony_and_call_alignment",
            lambda d: (
                d.__setitem__("objective_kind", "entity_knowledge"),
                d.__setitem__("destination", "frontier"),
                d.__setitem__("custody_class", "controlled"),
                d["external_crossing"].__setitem__("controlled_exception", "available_by_ceremony"),
                d.__setitem__("ceremony_ref", "ceremony://c/1"),
                d.__setitem__("ceremony_estate_id", d["estate_id"]),
                d.__setitem__("ceremony_class", "controlled"),
                d.__setitem__("call_authority_ref", "call://auth/1"),
                d.__setitem__("call_request_sha256", d["request_sha256"]),
                d.__setitem__("call_estate_id", d["estate_id"]),
                d.__setitem__("call_class", "controlled"),
            ),
            True,
            False,
            id="controlled_frontier_exception_available_requires_ceremony_and_call_alignment",
        ),
        pytest.param(
            "controlled_frontier_exception_available_mismatched_call_denies",
            lambda d: (
                d.__setitem__("destination", "frontier"),
                d.__setitem__("custody_class", "controlled"),
                d["external_crossing"].__setitem__("controlled_exception", "available_by_ceremony"),
                d.__setitem__("ceremony_ref", "ceremony://c/1"),
                d.__setitem__("ceremony_estate_id", d["estate_id"]),
                d.__setitem__("ceremony_class", "controlled"),
                d.__setitem__("call_authority_ref", "call://auth/1"),
                d.__setitem__("call_request_sha256", "f" * 64),
                d.__setitem__("call_estate_id", "other"),
                d.__setitem__("call_class", "uncontrolled"),
            ),
            False,
            False,
            id="controlled_frontier_exception_available_mismatched_call_denies",
        ),
    ],
)
def test_crossing_decision_policy_contract_matrix(name, mutator, expected_allowed, expected_mask):
    _ = name
    crossing_mod = _module("services.activation.crossing")
    payload = copy.deepcopy(_valid_context_payload())
    mutator(payload)

    context = crossing_mod.CrossingContext(**payload)
    decision = crossing_mod.decide_crossing(context, now_epoch=1_800_000_000)

    assert decision.allowed is expected_allowed
    assert decision.mask_required is expected_mask
    assert decision.execution_authorized is False
    if payload["assessment_state"] == "unassessed":
        assert decision.effective_custody == "controlled"
