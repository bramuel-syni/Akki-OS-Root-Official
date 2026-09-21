"""M6 · Audio-Plane v1.0 · CP-M6-1-4 · Synthesis-relevant attribute capture.

Pluggable-seam mechanism per D10-family open ruling.  The seam is real
(accepts any owner-ratified backend); the placeholder
`UnratifiedSynthesisInferredBackend` refuses to capture with an
`[INFERRED-pending-ratification]` marker until owner ratifies a specific
model.

Discharge anchors (verbatim on single un-wrapped lines):

- Audio-Plane §4.4 P069 (notes/AUDIO_PLANE_SPEC_V1_REQUIREMENTS_VERBATIM_20260914.md V49):
      "During the same ingestion pass, group-level acoustic attributes required by any future synthesis capability (pitch statistics, energy contours, duration patterns) are captured, subject to the custody conditions of §6.4. This forecloses nothing and costs little; omitting it forecloses the invention function or forces re-ingestion."

- Audio-Plane §15 P232 (build sequence · verbatim):
      "Ingestion capture — language ID, code-switch points, condition profile, synthesis attributes (§4.1–§4.4)"

- Pull-seam discipline: audio bytes never cross the
  SynthesisAttributeCapturerBackend seam · only `segment_ref` + `duration_s` do.

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - No audio bytes cross the seam.
  - Case-agnostic; no executive-domain tokens.

Custody discipline (§4.4 P069 cross-link to §6.4):
  - The seam captures synthesis-relevant acoustic attributes but §6.4
    custody-conditions apply downstream.  The enforcement of §6.4 lives
    in a downstream custody guard, NOT in this seam.  This CP lands the
    capture surface; downstream custody-guard hard-lock enforcement is
    out of scope for the seam.

N7 book-keeping (M6 grounding brief §Correction-1 verbatim 2026-09-15T~17:50Z):
  - Prior observation that N7 was skipped is RETRACTED.  All 10 N-items
    enumerated correctly.  N7 (§8.4 P139..P142 wizard compile-refusal
    machinery) rolls into sub-wave 6 CP-M6-6-1, NOT this CP.

Contract:

    capture_synthesis_attributes(
        *,
        segments: Sequence[AudioSegment],
        backend: SynthesisAttributeCapturerBackend,
    ) -> List[SynthesisAttributes]

    SynthesisAttributeCapturerBackend protocol:
      - attribute: backend_name: str
      - method:    capture(segment_ref: str, duration_s: float)
                     -> Mapping[str, Any]
        with required keys (§4.4 P069 verbatim three families):
          "pitch_statistics"    : Sequence[float]  (backend-defined summary)
          "energy_contours"     : Sequence[float]  (backend-defined summary)
          "duration_patterns"   : Sequence[float]  (backend-defined summary)
        The orchestrator coerces each family's Sequence to a tuple to
        satisfy the frozen dataclass immutability requirement.

Refusals:
    SegmentsEmptyError    on empty segments  (re-exported from CP-M6-1-1)
    SegmentInvalidError   on non-AudioSegment (re-exported from CP-M6-1-1)
    BackendUnratifiedError raised by the placeholder backend
                          `UnratifiedSynthesisInferredBackend` when
                          invoked (D10-family discipline · CP-M6-1-4-local
                          class · separate from CP-M6-1-1/2/3 homonyms).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Mapping, Protocol, Sequence, Tuple, runtime_checkable

# CP-M6-1-1 single-source-of-truth reuse.
from services.audio_plane_v1.language_identifier import (
    AudioSegment,
    SegmentsEmptyError,
    SegmentInvalidError,
)


class BackendUnratifiedError(Exception):
    """Raised by the placeholder `UnratifiedSynthesisInferredBackend.capture`
    to surface the D10-family open ruling: the seam is real but the backend
    awaits owner ratification.  Marker `[INFERRED-pending-ratification]` is
    carried in the message.

    CP-M6-1-4-local class (does NOT subclass or alias CP-M6-1-1/2/3
    homonyms): each backend's ratification story is tracked independently,
    so a single-catch across audio-plane backends is deliberately not
    offered."""


@dataclass(frozen=True)
class SynthesisAttributes:
    """A single per-segment synthesis-relevant attributes bundle.

    Five carriers per Audio-Plane §4.4 P069 verbatim + D10 attribution:
      - `segment_ref` — the segment this bundle applies to.
      - `pitch_statistics` — immutable tuple of backend-emitted pitch
        summary values (backend-defined interpretation).
      - `energy_contours` — immutable tuple of backend-emitted energy
        contour summary values (backend-defined interpretation).
      - `duration_patterns` — immutable tuple of backend-emitted
        duration pattern summary values (backend-defined interpretation).
      - `backend_name` — the name of the backend that produced this
        bundle (D10 pluggable-seam-until-ratified attribution).

    The three §4.4 P069 acoustic families are stored as tuples (not
    lists) so the frozen dataclass is genuinely immutable.  §6.4 custody
    conditions apply downstream — the enforcement lives in a downstream
    custody guard, not in this shape.
    """

    segment_ref: str
    pitch_statistics: Tuple[float, ...]
    energy_contours: Tuple[float, ...]
    duration_patterns: Tuple[float, ...]
    backend_name: str


@runtime_checkable
class SynthesisAttributeCapturerBackend(Protocol):
    """Protocol for a pluggable synthesis-attribute capturer backend.

    Any owner-ratified concrete backend implements this protocol.
    The mechanism invokes `backend.capture(...)` once per segment and
    wraps the return in a `SynthesisAttributes` attributed to
    `backend.backend_name`.
    """

    backend_name: str

    def capture(
        self,
        segment_ref: str,
        duration_s: float,
    ) -> Mapping[str, Any]:
        ...


class UnratifiedSynthesisInferredBackend:
    """Placeholder backend that refuses to capture until owner ratifies.

    Satisfies the `SynthesisAttributeCapturerBackend` protocol structurally
    (has `backend_name` + `capture`), so the seam is exercisable by tests
    + downstream integrations, but any invocation raises
    `BackendUnratifiedError` with the `[INFERRED-pending-ratification]`
    marker per D10-family open ruling.
    """

    backend_name = "unratified_inferred_synthesis_backend"

    def capture(
        self,
        segment_ref: str,
        duration_s: float,
    ) -> Mapping[str, Any]:
        raise BackendUnratifiedError(
            "[INFERRED-pending-ratification] · "
            "UnratifiedSynthesisInferredBackend refuses to capture "
            "synthesis attributes per D10-family open ruling. "
            "Owner ratification required for concrete backend before "
            "synthesis-attribute capture runs on live estate content."
        )


def _validate_segments(
    segments: Sequence[AudioSegment],
) -> Tuple[AudioSegment, ...]:
    if not segments:
        raise SegmentsEmptyError(
            "synthesis attribute capturer: segments must be non-empty; "
            "got 0 segments"
        )
    coerced = tuple(segments)
    for i, s in enumerate(coerced):
        if not isinstance(s, AudioSegment):
            raise SegmentInvalidError(
                f"synthesis attribute capturer: segments[{i}] must be an "
                f"AudioSegment; got {type(s).__name__}"
            )
    return coerced


def capture_synthesis_attributes(
    *,
    segments: Sequence[AudioSegment],
    backend: SynthesisAttributeCapturerBackend,
) -> List[SynthesisAttributes]:
    """Capture synthesis-relevant acoustic attributes per segment via the
    pluggable backend seam.

    Invokes `backend.capture(segment_ref, duration_s)` once per segment
    (in segment order) and wraps the return in a `SynthesisAttributes`
    attributed to `backend.backend_name`.  Each §4.4 P069 family
    (pitch_statistics · energy_contours · duration_patterns) is coerced
    from its backend-emitted Sequence to a tuple so the frozen dataclass
    stays immutable.

    See module docstring for refusals + discharge anchors.  Pure
    orchestration; no LLM/HTTP/filesystem; no audio bytes cross the seam.
    """
    validated = _validate_segments(segments)

    results: List[SynthesisAttributes] = []
    backend_name = getattr(backend, "backend_name", type(backend).__name__)
    for segment in validated:
        raw = backend.capture(segment.segment_ref, segment.duration_s)
        pitch_statistics = tuple(raw.get("pitch_statistics", ()))
        energy_contours = tuple(raw.get("energy_contours", ()))
        duration_patterns = tuple(raw.get("duration_patterns", ()))
        results.append(
            SynthesisAttributes(
                segment_ref=segment.segment_ref,
                pitch_statistics=pitch_statistics,
                energy_contours=energy_contours,
                duration_patterns=duration_patterns,
                backend_name=backend_name,
            )
        )
    return results
