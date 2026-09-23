"""CP-AIP-4-CODEC-SERVICE · AIP v1.0 §3.3 (b) registry-boundary rejection of missing codec_version.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-4-CODEC-SERVICE and nothing else.

Spec anchor (AIP v1.0):
- §3.2 P048 verbatim: 'codec_version is a mandatory field of every
  downstream artifact's provenance. A transcript states which codec
  produced its tokens.'
- §3.3 (b) verbatim: 'A downstream artifact lacking codec_version in
  provenance is rejected at the registry boundary.'
- §1.2 modality-extension: this module composes sealed CP-M6-4-2
  `assert_downstream_carries_codec_version` via import - no parallel
  redeclaration.
- §1.5 unrepresentable-not-policed: the boundary raises before any
  registry write.

Design:
- `RegistryBoundaryRejection` raised when a downstream artifact's
  provenance is missing or empty `codec_version`.
- `enter_registry_boundary` invokes sealed CP-M6-4-2 helper. The
  sealed helper raises `MissingCodecVersionError` on any deviation;
  this seat re-raises as `RegistryBoundaryRejection` so callers can
  classify the refusal as a boundary-level rejection specifically.

Sealed carriers UNCHANGED per SO §3.8:
- backend/services/perception/audio_codec/artefact.py (CP-M6-4-2 ·
  assert_downstream_carries_codec_version · MissingCodecVersionError).

Wave-honest limits:
- No LLM invocation. No HTTP call. No filesystem write.
- Case-agnostic; no executive-domain tokens.
"""
from __future__ import annotations

from typing import Any, Mapping

from backend.services.perception.audio_codec.artefact import (
    MissingCodecVersionError,
    assert_downstream_carries_codec_version,
)


class RegistryBoundaryRejection(Exception):
    """§3.3 (b) verbatim boundary rejection · a downstream artifact
    lacking codec_version in provenance is rejected at the registry
    boundary. Classifiable as a boundary-level refusal (distinct from
    sealed CP-M6-4-2 `MissingCodecVersionError` which fires at the
    schema level)."""


def enter_registry_boundary(
    *,
    downstream_artifact_provenance: Mapping[str, Any],
) -> None:
    """§3.3 (b) verbatim: 'A downstream artifact lacking codec_version
    in provenance is rejected at the registry boundary.'

    Composes sealed CP-M6-4-2 `assert_downstream_carries_codec_version`
    (§1.2 modality-extension). Raises `RegistryBoundaryRejection`
    (chained from sealed `MissingCodecVersionError`) on any missing
    or empty `codec_version` key. Returns None on acceptance.
    """
    try:
        assert_downstream_carries_codec_version(
            provenance=downstream_artifact_provenance,
        )
    except MissingCodecVersionError as exc:
        raise RegistryBoundaryRejection(
            f"§3.3 (b) verbatim: downstream artifact rejected at the "
            f"registry boundary - provenance is missing or empty "
            f"codec_version. Chained from sealed CP-M6-4-2 refusal: "
            f"{exc}. §3.2 P048 verbatim: 'codec_version is a mandatory "
            f"field of every downstream artifact's provenance.'"
        ) from exc
    return None
