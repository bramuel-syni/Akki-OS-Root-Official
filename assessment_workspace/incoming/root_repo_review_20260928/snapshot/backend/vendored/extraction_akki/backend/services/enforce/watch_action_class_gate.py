"""services.enforce.watch_action_class_gate — M12b-W1 · MUST-DO 1.

Schema-derived adapter surface for the Watch action-class vocabulary.

Per SO §3.10 Option-α (R-18 Tension (b) verbatim):
  "The authoritative closed set is the enum in the akki-contracts
   JSON Schema for that contract version (B.3), NOT the Python tuple;
   every fixed-vocabulary `Final[tuple[str, ...]]` carries a test
   asserting equality with the schema enum; vocabulary changes are
   contract-version changes."

Per SO §3.8 Option-C (R-18 Tension (a) verbatim):
  "hybrid adapter layer `services/enforce/<entity>_gate.py`; §3.8 held
   verbatim, no M9 changes ... routers reach persistence only via
   Depends(<entity>_gate)."

This gate is the schema-derived caller-flip surface for the Watch
action-class vocabulary. M9 Watch callers reach the closed vocabulary
through this module, not through the Python-side `ACTION_CLASSES`
tuple in `contracts.watch_action_v0` (which itself was authored
before SO §3.10-α landed).

Fail-closed refusal: `assert_action_class_valid` raises
`UnknownActionClassRefused` on any value not in the schema enum.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Final, Tuple


# Locate the authoritative JSON schema. The schema is the SOURCE OF
# TRUTH (SO §3.10-α); this module MIRRORS its enum.
_SCHEMA_PATH: Final[Path] = (
    Path(__file__).resolve().parents[3]
    / "contracts"
    / "watch_action_class.schema.json"
)


def _load_action_classes_from_schema() -> Tuple[str, ...]:
    """Load the schema's `enum` at module-import time. Vocabulary
    changes are contract-version changes — this function is called
    exactly once at import, deterministically."""
    with _SCHEMA_PATH.open("r", encoding="utf-8") as fh:
        schema = json.load(fh)
    enum_values = schema.get("enum")
    if not isinstance(enum_values, list) or not enum_values:
        raise RuntimeError(
            f"watch_action_class.schema.json missing or invalid `enum` field "
            f"at {_SCHEMA_PATH}"
        )
    return tuple(str(v) for v in enum_values)


# Schema-derived tuple mirror (SO §3.10-α compliance).
ACTION_CLASSES: Final[Tuple[str, ...]] = _load_action_classes_from_schema()


class UnknownActionClassRefused(ValueError):
    """Preventive-charter refusal: value not in the schema-derived
    closed vocabulary. Fail-closed. Refusal message names the failing
    key (its role, not its value)."""


def assert_action_class_valid(value: str) -> None:
    """Preventive-charter validator: refuse if `value` is not one of
    the schema-derived action classes. Returns None on pass (SO §3.8
    preventive-charter shape · caller invokes).

    Case-sensitive: `"ANNOTATE"` is not equal to `"annotate"` and is
    refused (matches JSON Schema enum matching semantics).
    """
    if value not in ACTION_CLASSES:
        raise UnknownActionClassRefused(
            f"action_class refused: value not in schema-derived "
            f"vocabulary (positional index only; value redacted; "
            f"|ACTION_CLASSES|={len(ACTION_CLASSES)})"
        )


__all__ = (
    "ACTION_CLASSES",
    "UnknownActionClassRefused",
    "assert_action_class_valid",
)
