"""M6 · Audio-Plane v1.0 · CP-M6-1-1 · Language ID at segment level.

Pluggable-seam mechanism per owner ratified D10 open ruling.  The seam is
real (accepts any owner-ratified backend); the placeholder
`UnratifiedInferredBackend` refuses to identify with an
`[INFERRED-pending-ratification]` marker until owner ratifies a specific
model (fastText LID.176 / Silero / etc.).

Discharge anchors (verbatim on single un-wrapped lines):

- Audio-Plane §4.1 N1 (notes/AUDIO_PLANE_SPEC_V1_REQUIREMENTS_VERBATIM_20260914.md line 92):
      "A lightweight offline language identifier (CPU-viable, in-perimeter) runs at segment level during ingestion."

- Audio-Plane §15 P232 (build sequence · verbatim):
      "Ingestion capture — language ID, code-switch points, condition profile, synthesis attributes (§4.1–§4.4)"

- Pull-seam discipline (via CP-RG3/RG4 substrate):
      only derivatives cross seam boundaries; audio bytes never cross the
      LanguageIDBackend seam · only `segment_ref` (opaque caller-scoped
      handle) + `duration_s` do.

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - No audio bytes cross the seam.  Real backend implementations wrap the
    audio-byte reading under `readonly_nas_guard` externally.
  - Case-agnostic; no executive-domain tokens.

Contract:

    identify_language_per_segment(*, segments: Sequence[AudioSegment],
                                  backend: LanguageIDBackend)
        -> List[LanguageIDResult]

    LanguageIDBackend protocol:
      - attribute: backend_name: str
      - method:    identify(segment_ref: str, duration_s: float) -> Tuple[str, float]
                   returns (language_tag, confidence)

Refusals:
    SegmentsEmptyError    on empty segments
    SegmentInvalidError   on non-AudioSegment element
    BackendUnratifiedError raised by the placeholder backend `UnratifiedInferredBackend`
                          when invoked (D10 discipline)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Protocol, Sequence, Tuple, runtime_checkable


class SegmentsEmptyError(Exception):
    """Raised when `segments` is empty.  Ingestion capture (§15 P232) is
    per-segment; an empty segment list is refused at the orchestrator
    boundary."""


class SegmentInvalidError(Exception):
    """Raised when a `segments` element is not an `AudioSegment` instance."""


class BackendUnratifiedError(Exception):
    """Raised by the placeholder `UnratifiedInferredBackend.identify` to
    surface the D10 open ruling: the seam is real but the backend awaits
    owner ratification (fastText LID.176 / Silero / etc.).  Marker
    `[INFERRED-pending-ratification]` is carried in the message."""


@dataclass(frozen=True)
class AudioSegment:
    """A single audio segment reference the LID orchestrator walks.

    Pull-seam discipline: audio bytes DO NOT cross this shape.  Only:
      - `segment_ref` — caller-scoped opaque handle (e.g. a NAS mount path,
        an ingestion job segment id, or any label the backend understands
        to fetch its own bytes under readonly_nas_guard).
      - `duration_s` — segment duration in seconds (float).

    Any audio-byte carrier (audio_bytes / waveform / samples) is banned
    by design.
    """

    segment_ref: str
    duration_s: float


@dataclass(frozen=True)
class LanguageIDResult:
    """A single per-segment language-ID result.

    Four carriers per Audio-Plane §4.1 N1 verbatim + D10 backend
    attribution:
      - `segment_ref` — the segment this result applies to.
      - `language_tag` — the backend-emitted language tag (e.g. "swa",
        "eng", "lug", "sheng", etc.).
      - `confidence` — the backend-emitted confidence in [0.0, 1.0].
      - `backend_name` — the name of the backend that produced this
        result (D10 pluggable-seam-until-ratified attribution).
    """

    segment_ref: str
    language_tag: str
    confidence: float
    backend_name: str


@runtime_checkable
class LanguageIDBackend(Protocol):
    """Protocol for a pluggable language-ID backend.

    Any owner-ratified concrete backend (fastText LID.176 / Silero /
    whisper-lang / etc.) implements this protocol.  The mechanism
    invokes `backend.identify(...)` once per segment and wraps the
    return in a `LanguageIDResult` attributed to `backend.backend_name`.
    """

    backend_name: str

    def identify(
        self,
        segment_ref: str,
        duration_s: float,
    ) -> Tuple[str, float]:
        ...


class UnratifiedInferredBackend:
    """Placeholder backend that refuses to identify until owner ratifies.

    Satisfies the `LanguageIDBackend` protocol structurally (has
    `backend_name` + `identify`), so the seam is exercisable by tests +
    downstream integrations, but any invocation raises
    `BackendUnratifiedError` with the `[INFERRED-pending-ratification]`
    marker per D10 open ruling.

    Replace at owner ratification: import an owner-ratified concrete
    backend and pass its instance in to `identify_language_per_segment`.
    The mechanism does not depend on which concrete backend is passed.
    """

    backend_name = "unratified_inferred_backend"

    def identify(
        self,
        segment_ref: str,
        duration_s: float,
    ) -> Tuple[str, float]:
        raise BackendUnratifiedError(
            "[INFERRED-pending-ratification] · UnratifiedInferredBackend "
            "refuses to identify per D10 open ruling (RULING_LEDGER row 13). "
            "Owner ratification required for concrete backend (fastText "
            "LID.176 / Silero / etc.) before language ID runs on live "
            "estate content."
        )


def _validate_segments(
    segments: Sequence[AudioSegment],
) -> Tuple[AudioSegment, ...]:
    if not segments:
        raise SegmentsEmptyError(
            "language identifier: segments must be non-empty; got 0 segments"
        )
    coerced = tuple(segments)
    for i, s in enumerate(coerced):
        if not isinstance(s, AudioSegment):
            raise SegmentInvalidError(
                f"language identifier: segments[{i}] must be an "
                f"AudioSegment; got {type(s).__name__}"
            )
    return coerced


def identify_language_per_segment(
    *,
    segments: Sequence[AudioSegment],
    backend: LanguageIDBackend,
) -> List[LanguageIDResult]:
    """Identify language per segment via the pluggable backend seam.

    Invokes `backend.identify(segment_ref, duration_s)` once per segment
    (in segment order) and wraps the return in a `LanguageIDResult`
    attributed to `backend.backend_name`.

    See module docstring for refusals + discharge anchors.  Pure
    orchestration; no LLM/HTTP/filesystem; no audio bytes cross the seam.
    """
    validated = _validate_segments(segments)

    results: List[LanguageIDResult] = []
    backend_name = getattr(backend, "backend_name", type(backend).__name__)
    for segment in validated:
        language_tag, confidence = backend.identify(
            segment.segment_ref,
            segment.duration_s,
        )
        results.append(
            LanguageIDResult(
                segment_ref=segment.segment_ref,
                language_tag=language_tag,
                confidence=confidence,
                backend_name=backend_name,
            )
        )
    return results
