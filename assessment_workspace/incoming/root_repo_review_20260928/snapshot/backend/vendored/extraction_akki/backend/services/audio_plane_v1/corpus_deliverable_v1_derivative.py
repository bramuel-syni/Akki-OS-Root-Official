"""services.audio_plane_v1.corpus_deliverable_v1_derivative — Path B upgrade derivative carrier.

CP-M7-W9-UPGRADE-1 · authored 2026-09-16 · under Ruling #5 owner-verbatim triple
banked at STATE/DECISIONS.md master `a04c65a8` (2026-09-16T~17:43Z):
    "Ruling #5: kdpa = compliant-under-pilot, named-persons = tokenized,
     transfer-basis = derivative-only"

Shape ruling banked at STATE/DECISIONS.md 2026-09-16T~19:22Z (owner verbatim):
    "Shape ruling: β — the 6-carrier segment with `derivative_kind_ref: str`
     (open string, no closed enum). Rationale: multiple derivative kinds
     already exist in the estate (transcript text, embeddings, attribute
     bundles, diarized timelines); without a kind discriminator the carrier
     would force an append-only extension almost immediately, and an OPEN-str
     field is exactly the case-agnostic pattern the 2026-09-13 correction
     mandates. Everything else per your α/β common spec: append-only new
     module, zero closed enums, zero release_gate/ruling_5_tier_lift imports,
     caller-side composition, preventive-charter refusal wrapper, defensive
     symmetry."

Case-agnostic. Zero closed enums. Zero domain tokens (21-token grep-negative
verified by invariant #7). All identifier discriminators — INCLUDING
`derivative_kind_ref` — are OPEN str.

Composition surface:
- `tier_admission_ref` is a caller-supplied opaque str referencing a
  `services.release_gate.ruling_5_tier_lift.Ruling5AdmissionCheck` payload
  (that module was sealed at CP-M7-W8-LIFT-1). This module does NOT import
  that surface (case-agnostic decoupling).
- `derivative_content_ref` is opaque; caller-side composition binds it to a
  governed derivative in the estate (transcript text · embedding · attribute
  bundle · diarized timeline · etc.).
- `derivative_kind_ref` is opaque; owner ruling verbatim mandates OPEN str.
- `retention_policy_ref` is opaque; caller composes with
  `services.governance_plane.retention_policy` — not imported here.

Standing-line proof (enforced by tests):
- No `bytes` type-hint on any field.
- No field name reads as audio-bytes / voiceprint / embedding / raw-audio.
- Runtime enforcement fires only when caller invokes; no global gate
  (preventive-charter · matches CP-M7-W8-LIFT-1 + CP-M7-W9-CONTRACT-1 +
  CP-M7-W2-CONTRACT-1 + CP-M8-CTCC-1).

Path A (raw-audio retention) STAYS BLOCKED per Ruling #5's
`transfer_basis=derivative-only` — this module intentionally does not
model a raw-audio deliverable shape.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


# Verbatim anchor required for gating invariant. Quotes Ruling #5 verbatim
# triple and the shape-ruling rationale.
PATH_B_UPGRADE_RULING_5_ANCHOR = (
    "Ruling #5 (owner verbatim · 2026-09-16T~17:43Z): "
    "'kdpa = compliant-under-pilot, named-persons = tokenized, "
    "transfer-basis = derivative-only'. "
    "Path B upgrade discharges the derivative-only crossing shape via a "
    "6-carrier segment carrying a derivative_content_ref, a tier_admission_ref, "
    "and an OPEN-str derivative_kind_ref discriminator per owner ruling "
    "shape-β verbatim 2026-09-16T~19:22Z."
)


class DerivativeCorpusDeliverableRefused(Exception):
    """Root refusal class for derivative-path deliverable schema violations.

    Deliberately NOT inheriting from
    `services.audio_plane_v1.corpus_deliverable_v1.CorpusDeliverableRefused`
    to preserve case-agnostic decoupling (zero imports of the peer module).
    The derivative path is a peer carrier, not a subclass.
    """


class DerivativeAudioBytesPayloadRefused(DerivativeCorpusDeliverableRefused):
    """Defensive-symmetry refusal (§6.2 pattern) — raised if a caller
    composes a raw-audio-bytes payload against this carrier. The schema
    is unrepresentable-by-construction for raw audio (no `bytes` type-hint
    on any field · no audio-bytes-shaped field name); this exception exists
    to catch legacy callers that hand-wrap a bytes payload."""


class MissingTierAdmissionRefError(DerivativeCorpusDeliverableRefused):
    """Refusal raised by `assert_derivative_admissible` when any segment's
    `tier_admission_ref` is empty. Empty `tier_admission_ref` means the
    segment has no bound Ruling #5 tier-lift admission carrier · which
    would allow non-admitted derivative crossings."""


class MissingRuling5AdmissionRefError(DerivativeCorpusDeliverableRefused):
    """Refusal raised by `assert_derivative_admissible` when the
    deliverable's `ruling_5_admission_ref` is empty. Empty
    `ruling_5_admission_ref` means the manifest has no bound Ruling #5
    admission carrier."""


class MissingDerivativeContentRefError(DerivativeCorpusDeliverableRefused):
    """Refusal raised by `assert_derivative_admissible` when any segment's
    `derivative_content_ref` is empty. Empty `derivative_content_ref` means
    the segment has no bound derivative content (defeats the purpose of the
    derivative-path carrier)."""


@dataclasses.dataclass(frozen=True)
class DerivativeSegment_v1:
    """Path B upgrade segment · Shape β · exact-order 6 carriers · frozen.

    - `source_file_pointer` (str) — opaque ref to a source-plane file.
    - `segment_offsets_ms` (Tuple[Tuple[int, int], ...]) — start/end ms pairs.
    - `transcript` (str) — the transcript-only content for this segment.
    - `derivative_content_ref` (str) — opaque ref to a governed derivative
      (transcript text · embedding · attribute bundle · diarized timeline
      · etc.). Empty string refused at admit-time.
    - `tier_admission_ref` (str) — opaque ref to a
      `services.release_gate.ruling_5_tier_lift.Ruling5AdmissionCheck`
      payload (that module was sealed at CP-M7-W8-LIFT-1). Empty string
      refused at admit-time.
    - `derivative_kind_ref` (str) — OPEN str discriminator for the
      derivative kind (per owner ruling shape-β 2026-09-16T~19:22Z; no
      closed enum; case-agnostic).
    """
    source_file_pointer: str
    segment_offsets_ms: Tuple[Tuple[int, int], ...]
    transcript: str
    derivative_content_ref: str
    tier_admission_ref: str
    derivative_kind_ref: str


@dataclasses.dataclass(frozen=True)
class DerivativeCorpusDeliverable_v1:
    """Path B upgrade deliverable manifest · exact-order 4 carriers · frozen.

    - `deliverable_id` (str) — opaque caller-supplied id.
    - `retention_policy_ref` (str) — opaque ref to a RetentionPolicy binding
      (caller composes with `services.governance_plane.retention_policy` ·
      not imported here).
    - `segments` (Tuple[DerivativeSegment_v1, ...]) — the derivative-path
      segments that constitute the corpus.
    - `ruling_5_admission_ref` (str) — opaque ref to a Ruling5AdmissionCheck
      payload for the manifest-level admission (peer of segment-level
      `tier_admission_ref`). Empty string refused at admit-time.
    """
    deliverable_id: str
    retention_policy_ref: str
    segments: Tuple[DerivativeSegment_v1, ...]
    ruling_5_admission_ref: str


def assert_derivative_admissible(*, deliverable: DerivativeCorpusDeliverable_v1) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Fires only when a caller explicitly invokes this function; there is no
    global gate. Matches the preventive-charter pattern banked at CP-M8-CTCC-1
    + CP-M7-W9-CONTRACT-1 + CP-M7-W2-CONTRACT-1 + CP-M7-W8-LIFT-1.

    Refuses when:
    - `deliverable.ruling_5_admission_ref` is empty
      -> raises `MissingRuling5AdmissionRefError`.
    - any `segment.tier_admission_ref` is empty
      -> raises `MissingTierAdmissionRefError`.
    - any `segment.derivative_content_ref` is empty
      -> raises `MissingDerivativeContentRefError`.

    Returns None on admit.
    """
    if not deliverable.ruling_5_admission_ref:
        raise MissingRuling5AdmissionRefError(
            "deliverable.ruling_5_admission_ref is empty; "
            "the manifest has no bound Ruling #5 admission carrier."
        )
    for i, segment in enumerate(deliverable.segments):
        if not segment.tier_admission_ref:
            raise MissingTierAdmissionRefError(
                f"segment[{i}].tier_admission_ref is empty; "
                f"the segment has no bound Ruling #5 tier-lift admission carrier."
            )
        if not segment.derivative_content_ref:
            raise MissingDerivativeContentRefError(
                f"segment[{i}].derivative_content_ref is empty; "
                f"the segment has no bound derivative content."
            )
    return None


__all__ = [
    "PATH_B_UPGRADE_RULING_5_ANCHOR",
    "DerivativeSegment_v1",
    "DerivativeCorpusDeliverable_v1",
    "DerivativeCorpusDeliverableRefused",
    "DerivativeAudioBytesPayloadRefused",
    "MissingTierAdmissionRefError",
    "MissingRuling5AdmissionRefError",
    "MissingDerivativeContentRefError",
    "assert_derivative_admissible",
]
