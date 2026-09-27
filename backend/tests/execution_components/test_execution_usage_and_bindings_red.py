"""RED-first contracts for usage publisher and server-owned execution bindings."""

from __future__ import annotations

import importlib
import inspect

import pytest


def _usage_module():
    try:
        return importlib.import_module("services.northena.execution_usage")
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing expected RED target module services.northena.execution_usage: {exc}")


def _bindings_module():
    try:
        return importlib.import_module("services.northena.execution_bindings")
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing expected RED target module services.northena.execution_bindings: {exc}")


# Module/feature: Coordinator contract adds optional usage_publisher and authority.prepare-aware dispatch snapshot handling.
def test_coordinator_signature_exposes_usage_publisher_extension_point():
    coord_mod = importlib.import_module("services.northena.execution_coordinator")
    parameters = inspect.signature(coord_mod.Coordinator.__init__).parameters
    assert "usage_publisher" in parameters


# Module/feature: usage publisher API exists and enforces typed publish(request,result,dispatch,raw_meter).
def test_usage_publisher_contract_shape_exists():
    mod = _usage_module()
    assert hasattr(mod, "LedgerUsagePublisher")
    publish = getattr(mod.LedgerUsagePublisher, "publish", None)
    assert callable(publish)
    names = tuple(inspect.signature(publish).parameters.keys())
    assert names[:5] == ("self", "request", "result", "dispatch", "raw_meter")


# Module/feature: server-owned frozen bindings bundle and trusted builder surface.
def test_execution_bindings_bundle_and_build_coordinator_surface():
    mod = _bindings_module()
    assert hasattr(mod, "ExecutionBindings")
    assert hasattr(mod, "build_coordinator")

    binding_fields = tuple(getattr(mod.ExecutionBindings, "__dataclass_fields__", {}).keys())
    assert binding_fields == (
        "decisions",
        "inspector",
        "executors",
        "eligibility",
        "handoffs",
        "gate_timeout_seconds",
    )

    build_parameters = tuple(inspect.signature(mod.build_coordinator).parameters.keys())
    assert build_parameters[:2] == ("db", "bindings")
