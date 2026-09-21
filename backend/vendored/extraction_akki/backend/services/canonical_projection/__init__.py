"""services.canonical_projection — pydantic-version-independent
projection of JSON schemas for frozen snapshot comparison.

Owner Ruling 2026-08-25T22:55Z (W6 close Q1 · staged remediation):
canonical-projection lands as a W8 opener, complementing the
pydantic 2.13.4 load-bearing pin. Together they give
belt-and-braces stability: the pin makes the emitter deterministic,
the projection makes the comparison version-tolerant.

Historical anchor: FL-P4-W6-01/03/04/05/06/07 documented six frozen
contracts drifting under pydantic 2.13.x's emitter changes:
  * Literal[X] fields: `const:X` alone (older) vs `{const:X,
    enum:[X]}` (newer, redundant enum companion).
  * Dict[str, Any] fields: no `additionalProperties` key (older) vs
    explicit `additionalProperties: True` (newer, redundant).

The canonicalize() function normalizes these idioms out of the
schema BEFORE snapshot bytes are compared. Governed change classes
(new enum values, changed types, new fields) still surface as
diffs; only pydantic-emitter noise is stripped.
"""
from services.canonical_projection.schema import canonicalize

__all__ = ["canonicalize"]
