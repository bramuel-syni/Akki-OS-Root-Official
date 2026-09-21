"""M6 · Audio-Plane v1.0 · CP-M6-1-2 · Code-switch point detection.

Pluggable-seam mechanism per owner ratified D10 open ruling.  The seam is
real (accepts any owner-ratified backend); the placeholder
`UnratifiedCodeSwitchInferredBackend` refuses to detect with an
`[INFERRED-pending-ratification]` marker until owner ratifies a specific
model.

Discharge anchors (verbatim on single un-wrapped lines):

- Audio-Plane §4.1 P061 (notes/AUDIO_PLANE_SPEC_V1_REQUIREMENTS_VERBATIM_20260914.md V44):
      "Recorded per segment: languages[], confidences, and code-switch points where multiple languages occur in one utterance."

- Audio-Plane §4.1 P062 (V45):
      "The signal routes downstream model selection (ASR path, NER path, de-identification path) and is written into provenance."

- Audio-Plane §4.2 P065 (V47 · four switch-point fields · facts-not-metadata):
      "Switch points (position, from-language, to-language, context class) are registered facts with provenance — not preprocessing metadata. They populate the register's code-switch layer and stratify test sets."

- Audio-Plane §15 P232 (build sequence · verbatim):
      "Ingestion capture — language ID, code-switch points, condition profile, synthesis attributes (§4.1–§4.4)"

- Pull-seam discipline (via CP-RG3/RG4 substrate):
      only derivatives cross seam boundaries; audio bytes never cross the
      CodeSwitchDetectorBackend seam · only `segment_ref` (opaque
      caller-scoped handle) + `duration_s` do.

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - No audio bytes cross the seam.  Real backend implementations wrap the
    audio-byte reading under `readonly_nas_guard` externally.
  - Case-agnostic; no executive-domain tokens.

Contract:

    detect_code_switch_points(
        *,
        segments: Sequence[AudioSegment],
        backend: CodeSwitchDetectorBackend,
    ) -> List[CodeSwitchPointDetection]

    CodeSwitchDetectorBackend protocol:
      - attribute: backend_name: str
      - method:    detect(segment_ref: str, duration_s: float)
                     -> Tuple[CodeSwitchPoint, ...]

Refusals:
    SegmentsEmptyError    on empty segments   (re-exported from CP-M6-1-1)
    SegmentInvalidError   on non-AudioSegment (re-exported from CP-M6-1-1)
    BackendUnratifiedError raised by the placeholder backend
                          `UnratifiedCodeSwitchInferredBackend` when
                          invoked (D10 discipline · CP-M6-1-2-local
                          class · separate from CP-M6-1-1's homonym so
                          each backend's ratification story is tracked
                          independently).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Protocol, Sequence, Tuple, runtime_checkable

# CP-M6-1-1 single-source-of-truth reuse: `AudioSegment` +
# `SegmentsEmptyError` + `SegmentInvalidError` come from the language
# identifier module.  CP-M6-1-2 does not refactor CP-M6-1-1 — it only
# imports the shared contract types so §4.1 + §4.2 speak the same
# per-segment shape.
from services.audio_plane_v1.language_identifier import (
    AudioSegment,
    SegmentsEmptyError,
    SegmentInvalidError,
)


class BackendUnratifiedError(Exception):
    """Raised by the placeholder `UnratifiedCodeSwitchInferredBackend.detect`
    to surface the D10 open ruling: the seam is real but the backend awaits
    owner ratification.  Marker `[INFERRED-pending-ratification]` is carried
    in the message.

    CP-M6-1-2-local class (does NOT subclass or alias CP-M6-1-1's
    `BackendUnratifiedError`): each backend's ratification story is tracked
    independently under D10, so a single-catch across audio-plane backends
    is deliberately not offered."""


@dataclass(frozen=True)
class CodeSwitchPoint:
    """A single code-switch point per Audio-Plane §4.2 P065 verbatim.

    Five carriers:
      - `position` — integer offset within the segment (backend-attributed;
        the seam does not prescribe a unit · a concrete backend may emit
        sample offsets, tenths-of-second offsets, tokens, etc.  The unit
        is fixed at the backend's ratification, and carried in the
        detection's `backend_name` provenance).
      - `from_language` — the backend-emitted language tag on the LEFT
        side of the switch (e.g. "swa").
      - `to_language` — the backend-emitted language tag on the RIGHT
        side of the switch (e.g. "eng").
      - `context_class` — the backend-emitted context class per §4.2
        P065 verbatim (e.g. "utterance", "clause", "phrase").
      - `confidence` — the backend-emitted confidence in [0.0, 1.0]
        (CP-M6-1-2 charter: code-switch points annotated with
        confidence + language-pair)."""

    position: int
    from_language: str
    to_language: str
    context_class: str
    confidence: float


@dataclass(frozen=True)
class CodeSwitchPointDetection:
    """A single per-segment code-switch detection result.

    Three carriers:
      - `segment_ref` — the segment this result applies to.
      - `switch_points` — an immutable tuple of `CodeSwitchPoint`
        (possibly empty when the backend detects no code-switches
        for this segment; §4.1 P061 verbatim: "code-switch points
        where multiple languages occur in one utterance" — a
        single-language segment produces an empty tuple).
      - `backend_name` — the name of the backend that produced this
        detection (D10 pluggable-seam-until-ratified attribution).
    """

    segment_ref: str
    switch_points: Tuple[CodeSwitchPoint, ...]
    backend_name: str


@runtime_checkable
class CodeSwitchDetectorBackend(Protocol):
    """Protocol for a pluggable code-switch detector backend.

    Any owner-ratified concrete backend implements this protocol.
    The mechanism invokes `backend.detect(...)` once per segment and
    wraps the return in a `CodeSwitchPointDetection` attributed to
    `backend.backend_name`.
    """

    backend_name: str

    def detect(
        self,
        segment_ref: str,
        duration_s: float,
    ) -> Tuple[CodeSwitchPoint, ...]:
        ...


class UnratifiedCodeSwitchInferredBackend:
    """Placeholder backend that refuses to detect until owner ratifies.

    Satisfies the `CodeSwitchDetectorBackend` protocol structurally (has
    `backend_name` + `detect`), so the seam is exercisable by tests +
    downstream integrations, but any invocation raises
    `BackendUnratifiedError` with the `[INFERRED-pending-ratification]`
    marker per D10 open ruling.

    Replace at owner ratification: import an owner-ratified concrete
    backend and pass its instance in to `detect_code_switch_points`.
    The mechanism does not depend on which concrete backend is passed.
    """

    backend_name = "unratified_inferred_code_switch_backend"

    def detect(
        self,
        segment_ref: str,
        duration_s: float,
    ) -> Tuple[CodeSwitchPoint, ...]:
        raise BackendUnratifiedError(
            "[INFERRED-pending-ratification] · "
            "UnratifiedCodeSwitchInferredBackend refuses to detect "
            "code-switch points per D10 open ruling (RULING_LEDGER row 13). "
            "Owner ratification required for concrete backend before "
            "code-switch detection runs on live estate content."
        )


def _validate_segments(
    segments: Sequence[AudioSegment],
) -> Tuple[AudioSegment, ...]:
    if not segments:
        raise SegmentsEmptyError(
            "code-switch detector: segments must be non-empty; got 0 segments"
        )
    coerced = tuple(segments)
    for i, s in enumerate(coerced):
        if not isinstance(s, AudioSegment):
            raise SegmentInvalidError(
                f"code-switch detector: segments[{i}] must be an "
                f"AudioSegment; got {type(s).__name__}"
            )
    return coerced


def detect_code_switch_points(
    *,
    segments: Sequence[AudioSegment],
    backend: CodeSwitchDetectorBackend,
) -> List[CodeSwitchPointDetection]:
    """Detect code-switch points per segment via the pluggable backend seam.

    Invokes `backend.detect(segment_ref, duration_s)` once per segment
    (in segment order) and wraps the return in a
    `CodeSwitchPointDetection` attributed to `backend.backend_name`.

    See module docstring for refusals + discharge anchors.  Pure
    orchestration; no LLM/HTTP/filesystem; no audio bytes cross the seam.
    """
    validated = _validate_segments(segments)

    results: List[CodeSwitchPointDetection] = []
    backend_name = getattr(backend, "backend_name", type(backend).__name__)
    for segment in validated:
        switch_points = backend.detect(
            segment.segment_ref,
            segment.duration_s,
        )
        switch_points_t: Tuple[CodeSwitchPoint, ...] = tuple(switch_points)
        results.append(
            CodeSwitchPointDetection(
                segment_ref=segment.segment_ref,
                switch_points=switch_points_t,
                backend_name=backend_name,
            )
        )
    return results
