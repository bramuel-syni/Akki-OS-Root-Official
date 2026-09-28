"""services.work_supervisor.job_manifest — case-agnostic JobManifest v0.

Contract:
  JobManifest (pydantic v2 model), v0 shape:
    manifest_version: int = 0                # frozen at 0 this wave
    job_id: str                              # non-empty
    job_kind: str                            # validated vs kind_registry
    submitter: str                           # non-empty
    submitted_at_utc: str                    # ISO-8601 with Z suffix
    scope: dict                              # opaque to platform
    output_contract: dict                    # names expected seal Kind
    depends_on: list[str]                    # job_ids
    dispatch_intent: str                     # 'local' | 'ssh_host_slug:X'
                                             #        | 'gpu_lane:Y'
    precondition_seals: list[dict]           # each {run_dir, expected_kind}

  JobManifestInvalid(ValueError)             # parse failure exception
  parse_job_manifest(payload: dict) -> JobManifest

Zero-influence on parse — pure validation, no I/O, no side effects.

See grounding brief §C-CP1 + §E for wave-honest limits.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List

from pydantic import BaseModel, Field, field_validator
from pydantic import ValidationError as _PydanticValidationError

from services.work_supervisor.kind_registry import is_registered


class JobManifestInvalid(ValueError):
    """Raised by parse_job_manifest when the payload does not conform
    to the v0 JobManifest contract."""


_ISO8601_Z_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$"
)

_DISPATCH_INTENT_PREFIXES = ("ssh_host_slug:", "gpu_lane:")


def _validate_dispatch_intent(value: str) -> str:
    if value == "local":
        return value
    for prefix in _DISPATCH_INTENT_PREFIXES:
        if value.startswith(prefix) and len(value) > len(prefix):
            return value
    raise ValueError(
        f"dispatch_intent {value!r} must be 'local' | "
        f"'ssh_host_slug:<slug>' | 'gpu_lane:<lane_id>'"
    )


def _validate_precondition_seal(entry: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(entry, dict):
        raise ValueError("precondition_seals entry must be a dict")
    for req in ("run_dir", "expected_kind"):
        if req not in entry:
            raise ValueError(
                f"precondition_seals entry missing required key {req!r}"
            )
        if not isinstance(entry[req], str) or not entry[req]:
            raise ValueError(
                f"precondition_seals entry field {req!r} must be a "
                "non-empty string"
            )
    return entry


class JobManifest(BaseModel):
    """v0 JobManifest.

    Registry lookup for `job_kind` happens at parse time (see
    parse_job_manifest). Constructing a JobManifest directly bypasses
    the registry check by design (unit tests may want to construct
    manifests bypassing the registry — but the wire contract's admission
    entry point is `parse_job_manifest`, which enforces it).
    """
    model_config = {"extra": "forbid"}

    manifest_version: int = Field(...)
    job_id: str = Field(..., min_length=1)
    job_kind: str = Field(..., min_length=1)
    submitter: str = Field(..., min_length=1)
    submitted_at_utc: str = Field(..., min_length=1)
    scope: Dict[str, Any] = Field(...)
    output_contract: Dict[str, Any] = Field(...)
    depends_on: List[str] = Field(...)
    dispatch_intent: str = Field(...)
    precondition_seals: List[Dict[str, Any]] = Field(...)

    @field_validator("manifest_version")
    @classmethod
    def _v0_only(cls, v: int) -> int:
        if v != 0:
            raise ValueError(
                f"manifest_version must be 0 (v0 wave), got {v!r}"
            )
        return v

    @field_validator("submitted_at_utc")
    @classmethod
    def _iso8601_z(cls, v: str) -> str:
        if not _ISO8601_Z_RE.match(v):
            raise ValueError(
                f"submitted_at_utc must match ISO-8601 with Z suffix "
                f"(YYYY-MM-DDTHH:MM:SS[.fff]Z), got {v!r}"
            )
        return v

    @field_validator("dispatch_intent")
    @classmethod
    def _dispatch_intent_grammar(cls, v: str) -> str:
        return _validate_dispatch_intent(v)

    @field_validator("precondition_seals")
    @classmethod
    def _precondition_seal_shape(
        cls, v: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        return [_validate_precondition_seal(e) for e in v]


def parse_job_manifest(payload: Dict[str, Any]) -> JobManifest:
    """Parse and validate a payload dict as a v0 JobManifest.

    Raises JobManifestInvalid on any failure — including missing
    fields, wrong types, wrong manifest_version, malformed ISO
    timestamp, malformed dispatch_intent, precondition_seals shape
    violation, and (critically) an unregistered `job_kind`.
    """
    if not isinstance(payload, dict):
        raise JobManifestInvalid(
            f"payload must be a dict, got {type(payload).__name__}"
        )

    try:
        manifest = JobManifest(**payload)
    except _PydanticValidationError as exc:
        raise JobManifestInvalid(
            f"payload failed schema validation: {exc}"
        ) from exc
    except TypeError as exc:
        # Missing required kwargs surface as TypeError from pydantic v2.
        raise JobManifestInvalid(
            f"payload failed schema validation: {exc}"
        ) from exc

    # Post-validation: job_kind must be registered.
    if not is_registered(manifest.job_kind):
        raise JobManifestInvalid(
            f"job_kind {manifest.job_kind!r} is not registered — "
            "downstream waves must call kind_registry.register_kind() "
            "at their mount time before submitting manifests"
        )

    return manifest


__all__ = [
    "JobManifest",
    "JobManifestInvalid",
    "parse_job_manifest",
]
