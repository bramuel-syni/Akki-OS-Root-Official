"""services.watch.schema_verdict — M12b-W1 · MUST-DO 2 + MUST-DO 4.

Schema-conformant Verdict pydantic model — the certificate-carrying,
signature-guardable row shape that Grey Mirror passes to Mkono.

Design:
  * Frozen, extra='forbid' pydantic v2 model (fail-closed on smuggled
    fields).
  * `action_class` sourced from `services.enforce.watch_action_class_gate`
    (schema-derived caller-flip surface · SO §3.8 Option-C + SO §3.10-α).
  * `certificate` carries the A5.19 shape: {requirement_id, data_points,
    observation_refs}. Nested frozen model with its own extra='forbid'.
  * `severance_signal_ref` REQUIRED iff action_class == 'sever' (Canon 8
    §A5.2 closed signal registry keying · matches JSON schema intent).
  * NO field for `confidence` / `score` / `strength` / `probability`
    (owner run order 2026-09-18T~21:15Z verbatim + Canon 8 §Line 31
    closed-6-registry doctrine · signature-as-guard).
  * `.canonical_bytes()` — deterministic UTF-8 JSON encoding of the
    row (sorted keys, no whitespace). Signable payload.
  * `.payload_ref()` — sha256 hex of `.canonical_bytes()`. Hash-binds
    the entire row for on-chain M10 certificate-row storage (gate (i)
    of M12b-W1).

Canon anchors (from objective card):
  * Canon 8 §A5.19 (certificate on watch.* rows).
  * Canon 8 §A5.2 (closed severance signal registry).
  * Canon 8 §W11 (one-task-one-identity · caller-flip).
  * Canon 8 §Line 31 (closed-6-registry · scoring never enters).
  * Canon 1 §4.2 (structural-impossibility doctrine · unrepresentable,
    not policed).
  * SO §3.10 Option-α (schema enum authoritative · tuple mirror).
  * SO §3.8 Option-C (thin adapter layer · additive-only).
"""
from __future__ import annotations

import hashlib
import json
from typing import Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from services.enforce.watch_action_class_gate import (
    ACTION_CLASSES,
    UnknownActionClassRefused,
    assert_action_class_valid,
)


class VerdictCertificate(BaseModel):
    """The A5.19 certificate carried on the verdict row.

    Structurally excludes score-shaped fields via `extra='forbid'` +
    absence-by-construction of any banned field name."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    requirement_id: str = Field(min_length=1)
    data_points: Tuple[str, ...] = Field(min_length=1)
    observation_refs: Tuple[str, ...] = Field(min_length=1)

    @field_validator("data_points")
    @classmethod
    def _dp_nonempty_items(cls, v: Tuple[str, ...]) -> Tuple[str, ...]:
        if any(not s for s in v):
            raise ValueError("data_points entries must be non-empty strings")
        return v

    @field_validator("observation_refs")
    @classmethod
    def _obs_nonempty_items(cls, v: Tuple[str, ...]) -> Tuple[str, ...]:
        if any(not s for s in v):
            raise ValueError("observation_refs entries must be non-empty strings")
        return v


class SchemaVerdict(BaseModel):
    """Schema-conformant Verdict row.

    Certificate-carrying (Canon 8 §A5.19) and signature-guardable
    (Canon 8 §Line 31). Grey Mirror emits; Mkono consumes; the chain
    (M10 unified ledger) stores under `payload_ref` hash-binding.

    Fields are exactly the union of `contracts/watch_verdict.schema.json`'s
    top-level properties. `additionalProperties=false` in the JSON
    schema is mirrored here by `extra='forbid'`. Neither surface
    declares any banned property name.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    action_class: str = Field(min_length=1)
    certificate: VerdictCertificate
    severance_signal_ref: Optional[str] = Field(default=None)

    @field_validator("action_class")
    @classmethod
    def _action_class_in_schema_enum(cls, v: str) -> str:
        try:
            assert_action_class_valid(v)
        except UnknownActionClassRefused as e:
            # Convert to ValueError so pydantic wraps it into a
            # ValidationError with the field name.
            raise ValueError(str(e))
        return v

    @model_validator(mode="after")
    def _severance_signal_required_iff_sever(self) -> "SchemaVerdict":
        if self.action_class == "sever":
            if not self.severance_signal_ref:
                raise ValueError(
                    "action_class='sever' requires a non-empty "
                    "severance_signal_ref (Canon 8 §A5.2 closed "
                    "signal registry keying)"
                )
        else:
            if self.severance_signal_ref not in (None, ""):
                raise ValueError(
                    f"severance_signal_ref must be absent for "
                    f"action_class={self.action_class!r} (JSON schema "
                    f"intent + Canon 8 §A5.2)"
                )
        return self

    def canonical_bytes(self) -> bytes:
        """Deterministic UTF-8 JSON encoding.

        Ordering:
          * Top-level keys sorted.
          * Certificate sub-object serialized with sorted keys.
          * Tuple/list order preserved (data_points, observation_refs
            are semantically ordered).
          * `severance_signal_ref` omitted when None.
          * No whitespace (`separators=(",", ":")`).

        Suitable for `watch_sign()` and `watch_verify()` — a byte-
        identical canonicalization means signatures are reproducible.
        """
        cert = self.certificate
        payload: dict = {
            "action_class": self.action_class,
            "certificate": {
                "data_points": list(cert.data_points),
                "observation_refs": list(cert.observation_refs),
                "requirement_id": cert.requirement_id,
            },
        }
        if self.severance_signal_ref is not None:
            payload["severance_signal_ref"] = self.severance_signal_ref
        return json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")

    def payload_ref(self) -> str:
        """SHA-256 hex digest of `.canonical_bytes()`. Hash-binds the
        entire row for M10 certificate-row storage (gate (i) of M12b-W1
        · B-M10-Q1 17-field row · payload_ref hash-binding)."""
        return hashlib.sha256(self.canonical_bytes()).hexdigest()


__all__ = (
    "SchemaVerdict",
    "VerdictCertificate",
    "ACTION_CLASSES",
)
