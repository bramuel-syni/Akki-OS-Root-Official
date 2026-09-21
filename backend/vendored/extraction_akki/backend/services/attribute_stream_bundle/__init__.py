"""services.attribute_stream_bundle — W1b · CP5 (generic).

Generic bundle abstraction: a bundle of named attribute streams with
a declared schema. Domain-neutral by construction. Downstream waves
(e.g. any specific-domain job-mount) register their schema at mount
time via `register_schema` and reference it by `schema_id` on the
bundle.

Case-agnostic invariant: this module carries NO domain-specific
tokens (frozen by two anti-leak tests in the invariant suite —
generic-token check + column-name check).
"""
from __future__ import annotations

import re
from typing import Any, Dict, Tuple

from pydantic import BaseModel, Field, field_validator


class SchemaNotRegistered(ValueError):
    """Raised for lookups on unknown schema_ids OR conflicting rebinds."""


_KNOWN_KIND_HINTS = frozenset({"str", "int", "float", "bool", "json"})

_ISO_Z = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$")


class AttributeStreamSchema(BaseModel):
    """Frozen schema. `columns` is a tuple of (name, kind_hint) pairs
    where kind_hint is one of str/int/float/bool/json."""
    model_config = {"frozen": True, "extra": "forbid"}

    schema_id: str = Field(..., min_length=1)
    columns: Tuple[Tuple[str, str], ...] = Field(...)

    @field_validator("columns")
    @classmethod
    def _columns_shape(
        cls, v: Tuple[Tuple[str, str], ...],
    ) -> Tuple[Tuple[str, str], ...]:
        if not v:
            raise ValueError("columns must be non-empty")
        for col in v:
            if not (isinstance(col, tuple) and len(col) == 2):
                raise ValueError(
                    f"each column must be a (name, kind_hint) 2-tuple, "
                    f"got {col!r}"
                )
            name, hint = col
            if not isinstance(name, str) or not name:
                raise ValueError(f"column name must be non-empty str, got {name!r}")
            if hint not in _KNOWN_KIND_HINTS:
                raise ValueError(
                    f"column kind_hint {hint!r} not in known set "
                    f"{sorted(_KNOWN_KIND_HINTS)!r}"
                )
        return v


_SCHEMAS: Dict[str, AttributeStreamSchema] = {}


def register_schema(schema: AttributeStreamSchema) -> None:
    existing = _SCHEMAS.get(schema.schema_id)
    if existing is not None and existing != schema:
        raise SchemaNotRegistered(
            f"schema_id {schema.schema_id!r} is already bound to a "
            "different schema; refusing conflicting rebind"
        )
    _SCHEMAS[schema.schema_id] = schema


def get_schema(schema_id: str) -> AttributeStreamSchema:
    s = _SCHEMAS.get(schema_id)
    if s is None:
        raise SchemaNotRegistered(
            f"schema_id {schema_id!r} is not registered — bind at "
            "job-mount time via register_schema()"
        )
    return s


def _reset_schemas_for_tests() -> None:
    _SCHEMAS.clear()


class AttributeStreamBundle_v0(BaseModel):
    """Frozen v0 bundle. Binds a bundle_id to a registered schema and
    an opaque map of per-stream metadata. `sealed_at_utc` must be
    ISO-8601 with Z suffix."""
    model_config = {"frozen": True, "extra": "forbid"}

    bundle_id: str = Field(..., min_length=1)
    schema_id: str = Field(..., min_length=1)
    streams: Dict[str, Dict[str, Any]] = Field(...)
    sealed_at_utc: str = Field(..., min_length=1)

    @field_validator("sealed_at_utc")
    @classmethod
    def _iso_z(cls, v: str) -> str:
        if not _ISO_Z.match(v):
            raise ValueError(
                f"sealed_at_utc must match ISO-8601 Z pattern, got {v!r}"
            )
        return v

    @field_validator("schema_id")
    @classmethod
    def _schema_registered(cls, v: str) -> str:
        if v not in _SCHEMAS:
            raise ValueError(
                f"schema_id {v!r} is not registered — register at "
                "job-mount time before constructing bundles"
            )
        return v


__all__ = [
    "AttributeStreamSchema",
    "AttributeStreamBundle_v0",
    "register_schema",
    "get_schema",
    "SchemaNotRegistered",
    "_reset_schemas_for_tests",
]
