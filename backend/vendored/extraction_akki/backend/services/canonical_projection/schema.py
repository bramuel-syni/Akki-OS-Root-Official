"""services.canonical_projection.schema — pure canonicalizer.

Rules applied at every dict level (recursive):

  R1 · Single-member enum COMPANION strip
       If a schema has BOTH `const: X` AND `enum: [X]` (exactly one
       member matching const), drop the `enum` key. This is the
       pydantic 2.13.x Literal emitter idiom equivalent to earlier
       pydantic's `const` alone.

  R2 · Open-object `additionalProperties: true` strip
       If a schema is `{type: "object"}` with `additionalProperties:
       True` and no `properties` key AND no `required` key, drop the
       `additionalProperties` key. This is the pydantic 2.13.x
       Dict[str, Any] emitter idiom equivalent to earlier pydantic's
       open object with no additionalProperties.

Preserved untouched:
  * Multi-value enums (governed vocabulary).
  * `additionalProperties: false` (extra=forbid discipline).
  * `additionalProperties: {...typed schema...}` (governed value shape).
  * Every other schema field (title, description, type, properties,
    items, $defs, ref, etc.).

Idempotency and non-mutation are enforced by unit test
(test_w8_cp1_canonical_projection.py::test_canonicalize_is_idempotent
+ test_canonicalize_does_not_mutate_input).
"""
from __future__ import annotations

from typing import Any


def canonicalize(schema: Any) -> Any:
    """Return a canonical projection of `schema`. Pure function; does
    not mutate the input."""
    if isinstance(schema, list):
        return [canonicalize(item) for item in schema]
    if not isinstance(schema, dict):
        return schema

    # Recurse first, then apply rules on the recursed dict.
    out = {k: canonicalize(v) for k, v in schema.items()}

    # R1 · redundant single-member enum companion.
    if (
        "const" in out
        and "enum" in out
        and isinstance(out["enum"], list)
        and len(out["enum"]) == 1
        and out["enum"][0] == out["const"]
    ):
        out = {k: v for k, v in out.items() if k != "enum"}

    # R2 · open-object additionalProperties:true redundancy.
    if (
        out.get("type") == "object"
        and out.get("additionalProperties") is True
        and "properties" not in out
        and "required" not in out
    ):
        out = {k: v for k, v in out.items() if k != "additionalProperties"}

    return out
