"""M6 · Audio-Plane v1.0 · CP-M6-4-3 · census-visibility invariant.

Discharge anchors (verbatim on single un-wrapped lines):

- Audio-Plane §3.2 P045 (V33 · service path · N4 anchor · census-visible clause):
      "perception/audio_codec/ — registered like any other perception model; census-visible; runs in-perimeter on tenant compute."

- M6 grounding brief §Sub-wave 4 CP breakdown (verbatim):
      "CP-M6-4-3 · census-visibility invariant — TESTS-FIRST · codec service appears in Mtafiti census surface as a registered perception capability."

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - Pure predicate + refusal · no coupling to a specific census-surface
    schema implementation (case-agnostic).
  - §3.1 P038 tokens-not-waveforms discipline preserved.

Contract:

    is_audio_codec_census_visible(*, perception_census_records) -> bool
      Pure predicate over an iterable of perception census records.
      True iff at least one record carries the verbatim
      `perception/audio_codec/` service_path.

    assert_audio_codec_census_visible(*, perception_census_records) -> None
      Refuses (AudioCodecCensusInvisibleError) when the predicate is
      False.

    AudioCodecCensusInvisibleError — subclass of
    `PerceptionRegistrationError` (from CP-M6-4-1 `service.py`) for
    refusal-family cohesion.

Refusals:
    AudioCodecCensusInvisibleError
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping, Optional

from services.perception.audio_codec.service import (
    AUDIO_CODEC_SERVICE_PATH,
    PerceptionRegistrationError,
)


class AudioCodecCensusInvisibleError(PerceptionRegistrationError):
    """Raised when the perception census surface does not carry a
    record with the §3.2 P045 verbatim `perception/audio_codec/`
    service_path.

    Subclass of `PerceptionRegistrationError` (CP-M6-4-1) so the
    perception-registration refusal family remains single-catch."""


def _extract_service_path(record: Any) -> Optional[str]:
    """Duck-typed helper: extract a `service_path` from either a
    mapping-shaped census record (via `.get`) or an object with a
    `service_path` attribute (e.g. `AudioCodecServiceDescriptor`).

    Returns None when neither shape carries a `service_path` reference.
    Case-agnostic — no coupling to a specific census schema."""
    if isinstance(record, Mapping):
        value = record.get("service_path")
    else:
        value = getattr(record, "service_path", None)
    if isinstance(value, str):
        return value
    return None


def is_audio_codec_census_visible(
    *,
    perception_census_records: Iterable[Any],
) -> bool:
    """Return True iff the perception census carries at least one
    record whose `service_path` matches the §3.2 P045 verbatim
    `perception/audio_codec/`.

    Pure predicate.  No side effects.  Case-agnostic.
    """
    for record in perception_census_records:
        if _extract_service_path(record) == AUDIO_CODEC_SERVICE_PATH:
            return True
    return False


def assert_audio_codec_census_visible(
    *,
    perception_census_records: Iterable[Any],
) -> None:
    """Assert the §3.2 P045 verbatim 'census-visible' invariant:
    the perception census carries a record whose service_path is
    `perception/audio_codec/`.

    Refuses with `AudioCodecCensusInvisibleError` on absence.
    """
    # Materialise once so both the predicate and the refusal message
    # can inspect the same records without exhausting a one-shot
    # iterator.
    records = list(perception_census_records)
    if is_audio_codec_census_visible(perception_census_records=records):
        return None
    raise AudioCodecCensusInvisibleError(
        f"perception census does not carry {AUDIO_CODEC_SERVICE_PATH!r} "
        f"(§3.2 P045 verbatim 'census-visible'); "
        f"records seen: {len(records)}"
    )
