"""M6 · Audio-Plane v1.0 · CP-M6-1-3 · Channel condition profile derivation.

Pluggable-seam mechanism per D10-family open ruling.  The seam is real
(accepts any owner-ratified backend); the placeholder
`UnratifiedChannelConditionInferredBackend` refuses to derive with an
`[INFERRED-pending-ratification]` marker until owner ratifies a specific
model.

Discharge anchors (verbatim on single un-wrapped lines):

- Audio-Plane §4.3 P067 (notes/AUDIO_PLANE_SPEC_V1_REQUIREMENTS_VERBATIM_20260914.md V48):
      "Channel condition — studio / field / telephone band, transmission artefacts, background class — is derived per segment at first ingestion. It is cheap to compute, directly predictive of extraction error, and required for training stratification. It is captured at first ingestion because re-ingesting an estate to recover it is the unaffordable mistake."

- Audio-Plane §15 P232 (build sequence · verbatim):
      "Ingestion capture — language ID, code-switch points, condition profile, synthesis attributes (§4.1–§4.4)"

- Pull-seam discipline (via CP-RG3/RG4 substrate):
      only derivatives cross seam boundaries; audio bytes never cross the
      ChannelConditionProfilerBackend seam · only `segment_ref` + `duration_s` do.

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - No audio bytes cross the seam.
  - Case-agnostic; no executive-domain tokens.

Vocabulary discipline:
  - `channel_condition` values are constrained to the §4.3 P067 verbatim
    three-set `{"studio", "field", "telephone_band"}` (Python identifier
    form of "telephone band"). The orchestrator refuses backend returns
    outside this set with `ChannelConditionInvalidError`.

Contract:

    derive_channel_condition_profile(
        *,
        segments: Sequence[AudioSegment],
        backend: ChannelConditionProfilerBackend,
    ) -> List[ChannelConditionProfile]

    ChannelConditionProfilerBackend protocol:
      - attribute: backend_name: str
      - method:    derive(segment_ref: str, duration_s: float)
                     -> Mapping[str, Any]
        with required keys:
          "channel_condition"       : str in CHANNEL_CONDITION_VALUES
          "transmission_artefacts"  : Sequence[str]
          "background_class"        : str

Refusals:
    SegmentsEmptyError            on empty segments        (re-exported)
    SegmentInvalidError           on non-AudioSegment       (re-exported)
    BackendUnratifiedError        raised by the placeholder backend
                                  `UnratifiedChannelConditionInferredBackend`
                                  when invoked (D10-family discipline ·
                                  CP-M6-1-3-local class)
    ChannelConditionInvalidError  raised by the orchestrator when the
                                  backend emits a `channel_condition`
                                  outside CHANNEL_CONDITION_VALUES
                                  (§4.3 vocabulary discipline)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, FrozenSet, List, Mapping, Protocol, Sequence, Tuple, runtime_checkable

# CP-M6-1-1 single-source-of-truth reuse: `AudioSegment` +
# `SegmentsEmptyError` + `SegmentInvalidError` come from the language
# identifier module.  CP-M6-1-3 does not refactor CP-M6-1-1 — it only
# imports the shared contract types so §4.1 + §4.2 + §4.3 speak the same
# per-segment shape.
from services.audio_plane_v1.language_identifier import (
    AudioSegment,
    SegmentsEmptyError,
    SegmentInvalidError,
)


# §4.3 P067 verbatim three-way partition of channel conditions.
# "telephone_band" is the Python-identifier-safe form of the verbatim
# "telephone band" (space-separated). Case-agnostic; no executive-domain
# tokens.  Frozen so the vocabulary cannot silently mutate at runtime.
CHANNEL_CONDITION_VALUES: FrozenSet[str] = frozenset({
    "studio",
    "field",
    "telephone_band",
})


class BackendUnratifiedError(Exception):
    """Raised by the placeholder
    `UnratifiedChannelConditionInferredBackend.derive` to surface the
    D10-family open ruling: the seam is real but the backend awaits
    owner ratification.  Marker `[INFERRED-pending-ratification]` is
    carried in the message.

    CP-M6-1-3-local class (does NOT subclass or alias CP-M6-1-1/2's
    homonyms): each backend's ratification story is tracked
    independently, so a single-catch across audio-plane backends is
    deliberately not offered."""


class ChannelConditionInvalidError(Exception):
    """Raised when a backend emits a `channel_condition` value outside
    the §4.3 P067 verbatim three-set `CHANNEL_CONDITION_VALUES`.

    §4.3 vocabulary discipline: backend freedom on the language-tag
    axis (§4.1 unconstrained) does NOT extend to the channel-condition
    axis (§4.3 constrained)."""


@dataclass(frozen=True)
class ChannelConditionProfile:
    """A single per-segment channel-condition profile.

    Five carriers per Audio-Plane §4.3 P067 verbatim + D10 attribution:
      - `segment_ref` — the segment this profile applies to.
      - `channel_condition` — backend-emitted value ∈
        `CHANNEL_CONDITION_VALUES` (studio / field / telephone_band).
      - `transmission_artefacts` — immutable tuple of backend-emitted
        artefact tags (may be empty when the backend detects none).
      - `background_class` — backend-emitted background-class tag.
      - `backend_name` — the name of the backend that produced this
        profile (D10 pluggable-seam-until-ratified attribution).
    """

    segment_ref: str
    channel_condition: str
    transmission_artefacts: Tuple[str, ...]
    background_class: str
    backend_name: str


@runtime_checkable
class ChannelConditionProfilerBackend(Protocol):
    """Protocol for a pluggable channel-condition profiler backend.

    Any owner-ratified concrete backend implements this protocol.
    The mechanism invokes `backend.derive(...)` once per segment and
    wraps the return in a `ChannelConditionProfile` attributed to
    `backend.backend_name`.
    """

    backend_name: str

    def derive(
        self,
        segment_ref: str,
        duration_s: float,
    ) -> Mapping[str, Any]:
        ...


class UnratifiedChannelConditionInferredBackend:
    """Placeholder backend that refuses to derive until owner ratifies.

    Satisfies the `ChannelConditionProfilerBackend` protocol structurally
    (has `backend_name` + `derive`), so the seam is exercisable by tests
    + downstream integrations, but any invocation raises
    `BackendUnratifiedError` with the `[INFERRED-pending-ratification]`
    marker per D10-family open ruling.

    Replace at owner ratification: import an owner-ratified concrete
    backend and pass its instance in to `derive_channel_condition_profile`.
    The mechanism does not depend on which concrete backend is passed.
    """

    backend_name = "unratified_inferred_channel_condition_backend"

    def derive(
        self,
        segment_ref: str,
        duration_s: float,
    ) -> Mapping[str, Any]:
        raise BackendUnratifiedError(
            "[INFERRED-pending-ratification] · "
            "UnratifiedChannelConditionInferredBackend refuses to derive "
            "channel condition profile per D10-family open ruling. "
            "Owner ratification required for concrete backend before "
            "channel-condition profiling runs on live estate content."
        )


def _validate_segments(
    segments: Sequence[AudioSegment],
) -> Tuple[AudioSegment, ...]:
    if not segments:
        raise SegmentsEmptyError(
            "channel condition profiler: segments must be non-empty; "
            "got 0 segments"
        )
    coerced = tuple(segments)
    for i, s in enumerate(coerced):
        if not isinstance(s, AudioSegment):
            raise SegmentInvalidError(
                f"channel condition profiler: segments[{i}] must be an "
                f"AudioSegment; got {type(s).__name__}"
            )
    return coerced


def _validate_channel_condition(value: Any) -> str:
    if not isinstance(value, str) or value not in CHANNEL_CONDITION_VALUES:
        raise ChannelConditionInvalidError(
            f"channel condition profiler: channel_condition {value!r} "
            f"outside §4.3 P067 verbatim vocabulary "
            f"{sorted(CHANNEL_CONDITION_VALUES)!r}"
        )
    return value


def derive_channel_condition_profile(
    *,
    segments: Sequence[AudioSegment],
    backend: ChannelConditionProfilerBackend,
) -> List[ChannelConditionProfile]:
    """Derive channel-condition profile per segment via the pluggable
    backend seam.

    Invokes `backend.derive(segment_ref, duration_s)` once per segment
    (in segment order) and wraps the return in a
    `ChannelConditionProfile` attributed to `backend.backend_name`.

    See module docstring for refusals + discharge anchors.  Pure
    orchestration; no LLM/HTTP/filesystem; no audio bytes cross the seam.
    """
    validated = _validate_segments(segments)

    results: List[ChannelConditionProfile] = []
    backend_name = getattr(backend, "backend_name", type(backend).__name__)
    for segment in validated:
        raw = backend.derive(segment.segment_ref, segment.duration_s)
        channel_condition = _validate_channel_condition(
            raw.get("channel_condition")
        )
        transmission_artefacts = tuple(raw.get("transmission_artefacts", ()))
        background_class = raw.get("background_class", "")
        results.append(
            ChannelConditionProfile(
                segment_ref=segment.segment_ref,
                channel_condition=channel_condition,
                transmission_artefacts=transmission_artefacts,
                background_class=background_class,
                backend_name=backend_name,
            )
        )
    return results
