"""services.governance_plane.retention_policy — W1b · CP1.

Contract per owner reframed roadmap §A.10:

    "The plane supports FOUR distinct retention regimes, each with its
    own governance surface. Any Artifact class binds to exactly one
    regime."

Four regimes (closed enum):
  SOURCE_UNTOUCHED       — source estate never modified (read-only)
  WORKER_SCRATCH_PURGED  — purge_attestation REQUIRED at close
  REGISTER_DESCRIPTIVE   — descriptive only; NO audio, NO per-utterance
                            embedding
  DELIVERABLE_GOVERNED   — governed retain-exception; release-gate
                            verdicts REQUIRED

Class↔payload allowed-mapping (v0, closed table):
  SOURCE_UNTOUCHED       -> {} (no payload class is admissible; the
                                regime is read-only by definition)
  WORKER_SCRATCH_PURGED  -> {audio_bytes, text_bytes, image_bytes,
                             binary_bytes}
  REGISTER_DESCRIPTIVE   -> {descriptive_row, attribute_stream_row}
  DELIVERABLE_GOVERNED   -> {audio_bytes, text_bytes, image_bytes,
                             descriptive_row, attribute_stream_row,
                             derived_bytes}

Zero-influence: all functions pure (no I/O).
"""
from __future__ import annotations

from enum import Enum
from typing import Dict, FrozenSet, Optional

from pydantic import BaseModel, Field, model_validator


class RetentionMismatch(ValueError):
    """Raised when a caller attempts a write whose payload class is not
    admissible for the artifact class's bound regime."""


class RetentionRegime(str, Enum):
    SOURCE_UNTOUCHED = "SOURCE_UNTOUCHED"
    WORKER_SCRATCH_PURGED = "WORKER_SCRATCH_PURGED"
    REGISTER_DESCRIPTIVE = "REGISTER_DESCRIPTIVE"
    DELIVERABLE_GOVERNED = "DELIVERABLE_GOVERNED"


_ALLOWED_PAYLOADS: Dict[RetentionRegime, FrozenSet[str]] = {
    RetentionRegime.SOURCE_UNTOUCHED: frozenset(),
    RetentionRegime.WORKER_SCRATCH_PURGED: frozenset({
        "audio_bytes", "text_bytes", "image_bytes", "binary_bytes",
    }),
    RetentionRegime.REGISTER_DESCRIPTIVE: frozenset({
        "descriptive_row", "attribute_stream_row",
    }),
    RetentionRegime.DELIVERABLE_GOVERNED: frozenset({
        "audio_bytes", "text_bytes", "image_bytes",
        "descriptive_row", "attribute_stream_row", "derived_bytes",
    }),
}


class RetentionPolicy(BaseModel):
    """Binding of an artifact class to a retention regime + policy
    knobs. Frozen and immutable at construction time.

    Construction invariants:
      - regime DELIVERABLE_GOVERNED MUST have release_gate_verdicts_required=True
      - regime SOURCE_UNTOUCHED MUST have ttl_days=None (source is
        never mutated, so a TTL is meaningless)
    """
    model_config = {"frozen": True, "extra": "forbid"}

    artifact_class: str = Field(..., min_length=1)
    regime: RetentionRegime
    ttl_days: Optional[int] = None
    release_gate_verdicts_required: bool = False

    @model_validator(mode="after")
    def _regime_shape_constraints(self) -> "RetentionPolicy":
        if self.regime is RetentionRegime.DELIVERABLE_GOVERNED:
            if not self.release_gate_verdicts_required:
                raise ValueError(
                    "regime DELIVERABLE_GOVERNED requires "
                    "release_gate_verdicts_required=True (governed "
                    "retain-exception must gate on release verdicts)"
                )
        if self.regime is RetentionRegime.SOURCE_UNTOUCHED:
            if self.ttl_days is not None:
                raise ValueError(
                    "regime SOURCE_UNTOUCHED has no TTL — the source "
                    "estate is never modified"
                )
        return self


# Process-scope policy registry — same singleton pattern as kind_registry.
_POLICIES: Dict[str, RetentionPolicy] = {}


def register_policy(policy: RetentionPolicy) -> None:
    """Register a policy binding for `policy.artifact_class`.
    Idempotent — registering the same (class, regime, ttl, gate) is a
    no-op; registering a DIFFERENT policy for the same class raises
    RetentionMismatch."""
    existing = _POLICIES.get(policy.artifact_class)
    if existing is not None and existing != policy:
        raise RetentionMismatch(
            f"artifact_class {policy.artifact_class!r} already bound to "
            f"a different policy (existing regime={existing.regime}, "
            f"new regime={policy.regime}); explicit unbind is required"
        )
    _POLICIES[policy.artifact_class] = policy


def get_policy(artifact_class: str) -> RetentionPolicy:
    p = _POLICIES.get(artifact_class)
    if p is None:
        raise RetentionMismatch(
            f"artifact_class {artifact_class!r} is not bound to any "
            "RetentionPolicy — register a policy before writing"
        )
    return p


def check_write_admissible(artifact_class: str, payload_class: str) -> None:
    """Refuse the write if `payload_class` is not in the allowed set
    for `artifact_class`'s bound regime. Silent success on admit."""
    policy = get_policy(artifact_class)
    allowed = _ALLOWED_PAYLOADS[policy.regime]
    if payload_class not in allowed:
        raise RetentionMismatch(
            f"artifact_class {artifact_class!r} is bound to regime "
            f"{policy.regime.value} which admits payload classes "
            f"{sorted(allowed)!r}; payload class {payload_class!r} "
            "is refused"
        )


def _reset_policies_for_tests() -> None:
    _POLICIES.clear()


__all__ = [
    "RetentionRegime",
    "RetentionPolicy",
    "RetentionMismatch",
    "register_policy",
    "get_policy",
    "check_write_admissible",
    "_reset_policies_for_tests",
]
