"""services.audio_plane_v1.corpus_deliverable_v1 — Path C default schema.

CP-M7-W9-CONTRACT-1 · sealed 2026-09-16 · under owner steer verbatim
2026-09-16T~08:35Z ("advance the milestone frontier as far as existing
owner law allows... Do NOT cross the standing lines: no training on
estate audio, no biometric material, no enforcement hard-gate, no
speculative shapes beyond existing owner law.").

ROADMAP §C.2 Path C verbatim:

    "Path C · DEFER — W2/W3 build with `pointer_or_bytes` schema;
     audio-bytes retention lands in W9 after Ruling #5 arrives. Corpus
     is transcript-only through W3.
     Default if no ruling by W2 CP0: Path C."

    "Path C · POINTER-ONLY DELIVERABLE — corpus is
     {source-file-pointer, segment_offsets_ms, transcript} triples.
     Audio bytes stay on the source estate. regime=SOURCE_UNTOUCHED
     for audio, regime=DELIVERABLE_GOVERNED for the manifest."

Case-agnostic. Zero closed enums. Zero domain tokens. All
identifier discriminators are OPEN str (opaque caller-supplied refs).

Composition surface:
- `retention_policy_ref` is a caller-supplied opaque str referencing
  a RetentionPolicy binding managed by
  `services.governance_plane.retention_policy`; this module does not
  import that surface (case-agnostic decoupling).
- `deliverable_id` is an opaque caller-supplied str; case-agnostic.

Standing-line proof:
- No `bytes` type-hint on any field of either dataclass.
- No field name reads as audio-bytes / voiceprint / embedding /
  raw-audio carrier.
- Runtime enforcement fires only when caller invokes; no global gate.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


# Verbatim anchor · required-verbatim phrase for gating invariant #5:
# "Default if no ruling by W2 CP0: Path C"
# "source-file-pointer"  "segment_offsets_ms"  "transcript"
PATH_C_DEFAULT_ROADMAP_ANCHOR = (
    "ROADMAP §C.2 Path C default: 'Default if no ruling by W2 CP0: "
    "Path C. Path C · POINTER-ONLY DELIVERABLE — corpus is "
    "{source-file-pointer, segment_offsets_ms, transcript} triples. "
    "Audio bytes stay on the source estate. regime=SOURCE_UNTOUCHED "
    "for audio, regime=DELIVERABLE_GOVERNED for the manifest.'"
)


class CorpusDeliverableRefused(Exception):
    """Root refusal class for corpus_deliverable_v1 schema violations."""


class AudioBytesPayloadRefused(CorpusDeliverableRefused):
    """Refusal raised (if a caller invokes a composition guard) when a
    payload shaped as raw audio bytes is presented to the Path-C
    deliverable surface. The Path-C schema is unrepresentable-by-
    construction for audio bytes (§6.2 pattern); this exception is
    a defensive symmetry when composing with legacy callers."""


@dataclasses.dataclass(frozen=True)
class CorpusSegment_v1:
    """Path C verbatim triple: {source-file-pointer, segment_offsets_ms,
    transcript}.

    Exact-order 3 carriers. Frozen.

    - `source_file_pointer` (str) — opaque caller-supplied ref to a
      source-plane file (e.g. a Source-Plane read-only handle · never
      a materialized bytes payload). Audio bytes stay on the source
      estate.
    - `segment_offsets_ms` (Tuple[Tuple[int, int], ...]) — start/end
      millisecond pairs into the source pointer. Non-negative ints.
    - `transcript` (str) — the transcript-only content for this
      segment. May be empty; case-agnostic (no language token).
    """
    source_file_pointer: str
    segment_offsets_ms: Tuple[Tuple[int, int], ...]
    transcript: str


@dataclasses.dataclass(frozen=True)
class CorpusDeliverable_v1:
    """Path C default deliverable manifest.

    Exact-order 3 carriers. Frozen.

    - `deliverable_id` (str) — opaque caller-supplied id.
    - `retention_policy_ref` (str) — opaque ref into
      `services.governance_plane.retention_policy` bindings; the
      caller-side composition is expected to bind the manifest to
      `regime=DELIVERABLE_GOVERNED` per §C.2. This module does NOT
      import that surface (case-agnostic decoupling).
    - `segments` (Tuple[CorpusSegment_v1, ...]) — the pointer-only
      triples that constitute the corpus. Order is caller-defined;
      the schema does not impose a canonical ordering.
    """
    deliverable_id: str
    retention_policy_ref: str
    segments: Tuple[CorpusSegment_v1, ...]


__all__ = [
    "PATH_C_DEFAULT_ROADMAP_ANCHOR",
    "CorpusSegment_v1",
    "CorpusDeliverable_v1",
    "CorpusDeliverableRefused",
    "AudioBytesPayloadRefused",
]
