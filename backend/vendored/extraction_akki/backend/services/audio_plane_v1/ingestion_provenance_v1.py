"""CP-AIP-1-INGEST-CAPTURE · AIP v1.0 §4.1-§4.4 + §4.6 ingestion provenance carriers.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-1-INGEST-CAPTURE and nothing else.

Spec anchor (AIP v1.0):
- §4.1 Language identification - `languages[]`, confidences, code-switch
  routing signal, written into provenance.
- §4.2 Code-switch points as facts (position, from-language, to-language,
  context class) with provenance - registered facts, not preprocessing
  metadata.
- §4.3 Condition profiling - studio / field / telephone band, transmission
  artefacts, background class - derived per segment at first ingestion.
- §4.4 Synthesis-relevant attribute capture - group-level acoustic
  attributes (pitch statistics, energy contours, duration patterns)
  subject to §6.4 custody conditions. GROUP-LEVEL only.
- §4.6 Acceptance criteria - full-triple gate at ingestion boundary.
- §1.2 Modality extension, not parallel machinery - sealed carriers
  composed via import; not redeclared.
- §1.5 Unrepresentable, not policed - provenance is unrepresentable
  without the three required carriers (languages, condition profile,
  baseline-tier flag); construction refuses instead of downstream
  policing.

Sealed carriers UNCHANGED per SO §3.8 (composed by ingestion_capture_v1.py):
- backend/services/audio_plane_v1/language_identifier.py (CP-M6-1-1 · sealed)
- backend/services/audio_plane_v1/channel_condition_profiler.py (CP-M6-1-3 · sealed)
- backend/services/audio_plane_v1/code_switch_detector.py (CP-M6-1-2 · sealed)
- backend/services/audio_plane_v1/synthesis_attribute_capturer.py (CP-M6-1-4 · sealed)
- backend/services/audio_plane_v1/instance_condition_map.py (CP-M6-2-1 · sealed · §4.5)
- backend/services/rms_station_language_axis.py (CP-CENSUS-RMS-STATION-LANGUAGE-AXIS · sealed)

§16.1 verification register (banked at phase0/aip_spec_verification_20260223/):
- Item (a) perception router contract - CLEAN (already first-class).
- Item (b) ingestion segment boundaries - CLEAN (canonical unit is
  AudioSegment; station-axis feed via additive wrapper this module composes).
- Item (c) wizard B-2/B-3 landing state - CLEAN (out-of-scope for §4).

Design (§1.5 unrepresentable-not-policed):
- IngestionSegmentProvenance_v1 is constructed only through its dataclass
  __init__ which invokes __post_init__ validation refusing a record
  missing any §4.6 (a) required carrier. Empty languages tuple, None
  condition_profile_ref -> IngestionProvenanceIncomplete.
- LanguageEvidence_v1 refuses construction of a station_prior evidence
  without both research_citation_title and research_citation_url.
- SwitchPointFact_v1 is frozen; its four §4.2 verbatim fields (position,
  from_language, to_language, context_class) plus provenance_ref are
  required at construction.
- SynthesisGroupAttributesRef_v1 declares GROUP-LEVEL fields only; the
  invariant test negative-scans field names against the §6.4 custody
  boundary token set.

The §4.6 gate `assert_provenance_meets_section_4_6` lives in the sibling
module ingestion_capture_v1.py so this module carries pure carriers only
(no orchestration coupling).
"""
from __future__ import annotations

import dataclasses
from typing import Literal, Optional, Tuple


# =============================================================================
# Refusal classes
# =============================================================================


class IngestionProvenanceIncomplete(Exception):
    """§4.6 (a) refusal · a provenance shape is unrepresentable if it
    lacks any of the §4.6 required carriers (non-empty languages tuple,
    non-None condition_profile_ref) OR if a station_prior LanguageEvidence
    is constructed without both citation fields.
    """


# =============================================================================
# §4.1 LanguageEvidence_v1 · plural per-segment evidence
# =============================================================================


_LANGUAGE_EVIDENCE_SOURCE = Literal["detected", "station_prior", "code_switch"]


@dataclasses.dataclass(frozen=True)
class LanguageEvidence_v1:
    """One §4.1 language-observation carrier per segment.

    Multiple evidence entries per segment express `languages[]` plural in
    §4.1 verbatim ('Recorded per segment: languages[], confidences, and
    code-switch points where multiple languages occur in one utterance').

    Fields:
      - language_tag (str): backend-emitted or station-attributed language.
      - confidence (float): backend-emitted confidence in [0.0, 1.0], or
        1.0 for station_prior (cited attribution).
      - source (Literal): 'detected' (LID backend), 'station_prior' (RMS
        station-language axis fold-in), or 'code_switch' (§4.2 derived).
      - research_citation_title (str): non-empty ONLY for source=
        'station_prior' - owner directive 'all research with title'.
      - research_citation_url (str): non-empty ONLY for source=
        'station_prior'.

    Refuses at __post_init__ if source='station_prior' has empty citation
    fields (§4.1 + owner directive verbatim + §1.5 unrepresentable-not-
    policed).
    """
    language_tag: str
    confidence: float
    source: _LANGUAGE_EVIDENCE_SOURCE
    research_citation_title: str
    research_citation_url: str

    def __post_init__(self) -> None:
        if self.source == "station_prior":
            if not self.research_citation_title:
                raise IngestionProvenanceIncomplete(
                    "LanguageEvidence_v1 source='station_prior' requires "
                    "non-empty research_citation_title (§4.1 + owner "
                    "directive 'all research with title')."
                )
            if not self.research_citation_url:
                raise IngestionProvenanceIncomplete(
                    "LanguageEvidence_v1 source='station_prior' requires "
                    "non-empty research_citation_url (§4.1 + owner "
                    "directive 'all research with title')."
                )


# =============================================================================
# §4.2 SwitchPointFact_v1 · first-class facts (position, from-language,
# to-language, context class · with provenance)
# =============================================================================


@dataclasses.dataclass(frozen=True)
class SwitchPointFact_v1:
    """§4.2 verbatim: 'Switch points (position, from-language, to-language,
    context class) are registered facts with provenance - not preprocessing
    metadata.'

    Frozen (facts-not-metadata). Five fields: the four §4.2 verbatim
    carriers + provenance_ref binding the fact to its originating
    segment/position.

    Fields:
      - position (int): offset within the segment (ms or sample index -
        caller-defined opaque scalar).
      - from_language (str): pre-switch language tag.
      - to_language (str): post-switch language tag.
      - context_class (str): §4.2 verbatim 'context class' (caller-defined
        classification e.g. 'phrase_switch' | 'word_switch' | 'sentence_
        boundary_switch').
      - provenance_ref (str): opaque handle binding the fact to its
        originating segment (e.g. 'seg-003:pos-1234').
    """
    position: int
    from_language: str
    to_language: str
    context_class: str
    provenance_ref: str


# =============================================================================
# §4.3 ConditionProfileRef_v1 · per-segment condition (studio / field /
# telephone band, transmission artefacts, background class)
# =============================================================================


@dataclasses.dataclass(frozen=True)
class ConditionProfileRef_v1:
    """§4.3 verbatim: 'Channel condition - studio / field / telephone band,
    transmission artefacts, background class - is derived per segment at
    first ingestion.'

    Reference-shape carrier (pull-seam discipline · audio bytes never
    cross). The full profile lives on the sealed
    `channel_condition_profiler.py` output; this ref binds a profile to
    a segment for §4.6 (a) provenance completeness.

    Fields:
      - segment_ref (str): the segment this condition profile applies to.
      - condition_class (str): §4.3 verbatim 'studio / field / telephone
        band' (open str · caller-defined).
      - profiler_backend_name (str): backend attribution (D10 pluggable-
        seam discipline · e.g. 'unratified_inferred_backend').
    """
    segment_ref: str
    condition_class: str
    profiler_backend_name: str


# =============================================================================
# §4.4 SynthesisGroupAttributesRef_v1 · GROUP-LEVEL only, §6.4 custody
# =============================================================================


@dataclasses.dataclass(frozen=True)
class SynthesisGroupAttributesRef_v1:
    """§4.4 verbatim: 'group-level acoustic attributes required by any
    future synthesis capability (pitch statistics, energy contours,
    duration patterns) are captured, subject to the custody conditions
    of §6.4.'

    GROUP-LEVEL only. NO field name may reference an instance-identifying
    concept (idiolect marker, speaker id, character id, voiceprint,
    biometric embedding, exemplar). The §6.4 custody boundary is
    unrepresentable-by-construction on this ref shape per §1.5.

    Fields:
      - group_ref (str): opaque caller-scoped group handle (e.g. a cluster
        id, a station id, a modality id).
      - pitch_statistics_ref (str): §4.4 verbatim 'pitch statistics'
        opaque ref to the sealed synthesis_attribute_capturer output.
      - energy_contour_ref (str): §4.4 verbatim 'energy contours' opaque
        ref.
      - duration_pattern_ref (str): §4.4 verbatim 'duration patterns'
        opaque ref.
      - custody_boundary_class (str): the §6.4 custody-condition class
        this group's aggregation was assessed under (e.g. 'organic_
        aggregation' / 'unrepresentable_learned_boundary').
      - capturer_backend_name (str): backend attribution (D10).
    """
    group_ref: str
    pitch_statistics_ref: str
    energy_contour_ref: str
    duration_pattern_ref: str
    custody_boundary_class: str
    capturer_backend_name: str


# =============================================================================
# §4.6 (a)+(c) IngestionSegmentProvenance_v1 · full-triple provenance
# =============================================================================


@dataclasses.dataclass(frozen=True)
class IngestionSegmentProvenance_v1:
    """§4.6 (a) full-triple provenance carrier per segment.

    §4.6 (a) verbatim: 'No segment leaves ingestion without languages[],
    condition profile, and (where applicable) switch points in
    provenance.'

    §4.6 (c) verbatim: 'Baseline-tier capture (§9.2) runs for all
    admitted material regardless of any active objective.'

    Refuses at __post_init__ if §4.6 (a) required carriers are missing.
    (§4.6 (c) refusal lives at the gate callable
    `assert_provenance_meets_section_4_6` in ingestion_capture_v1.py so
    the constructor accepts False for legitimate not-yet-captured records
    that a downstream gate then refuses.)

    Fields:
      - segment_ref (str): binds this provenance to a specific segment.
      - languages (Tuple[LanguageEvidence_v1, ...]): non-empty per §4.1;
        multiple entries express plural `languages[]` when multiple
        languages occur in one utterance.
      - condition_profile_ref (Optional[ConditionProfileRef_v1]): non-
        None per §4.3 + §4.6 (a).
      - switch_points (Tuple[SwitchPointFact_v1, ...]): may be empty for
        single-language segments; §4.6 (a) '(where applicable)' clause.
      - synthesis_group_attributes_ref (Optional[
        SynthesisGroupAttributesRef_v1]): optional per §4.4 (custody-
        conditioned · GROUP-LEVEL only).
      - baseline_tier_captured (bool): §4.6 (c) baseline-tier §9.2
        capture flag. Constructor accepts False for records not yet
        captured; downstream gate refuses False at the ingestion
        boundary for admitted material.
      - station_prior_corroborated (bool): owner HONESTY RULE artifact ·
        True iff the composer determined station-prior + detected agree
        AND both are in WHISPER_CORROBORATABLE_LANGUAGES. Default False.
    """
    segment_ref: str
    languages: Tuple[LanguageEvidence_v1, ...]
    condition_profile_ref: Optional[ConditionProfileRef_v1]
    switch_points: Tuple[SwitchPointFact_v1, ...]
    synthesis_group_attributes_ref: Optional[SynthesisGroupAttributesRef_v1]
    baseline_tier_captured: bool
    station_prior_corroborated: bool = False

    def __post_init__(self) -> None:
        # §4.6 (a) refusal branch 1 · empty languages tuple.
        if len(self.languages) == 0:
            raise IngestionProvenanceIncomplete(
                "IngestionSegmentProvenance_v1 refuses empty languages "
                "tuple - §4.6 (a) requires non-empty `languages[]` per "
                "segment (§4.1 verbatim: 'every segment carries a real "
                "language signal')."
            )
        # §4.6 (a) refusal branch 2 · None condition_profile_ref.
        if self.condition_profile_ref is None:
            raise IngestionProvenanceIncomplete(
                "IngestionSegmentProvenance_v1 refuses None condition_"
                "profile_ref - §4.6 (a) + §4.3 require the condition "
                "profile derived per segment at first ingestion."
            )


__all__ = [
    "IngestionProvenanceIncomplete",
    "LanguageEvidence_v1",
    "SwitchPointFact_v1",
    "ConditionProfileRef_v1",
    "SynthesisGroupAttributesRef_v1",
    "IngestionSegmentProvenance_v1",
]
