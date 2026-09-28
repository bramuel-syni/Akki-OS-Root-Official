"""CP-AIP-1-INGEST-CAPTURE · AIP v1.0 §4.6 gate + §4.1 station-prior composer.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-1-INGEST-CAPTURE and nothing else.

Spec anchor (AIP v1.0):
- §4.1 station-prior discipline: 'the station axis recorded in provenance
  as the prior'; per-segment `languages[]` signal from actual identifier.
  Retired plumbing value NEVER reappears (owner GO reminder 2).
- §4.2 code-switch points as first-class facts composed into provenance.
- §4.3 condition profile composed into provenance.
- §4.4 GROUP-LEVEL synthesis attribute ref composed (custody-conditioned).
- §4.6 (a) full-triple gate + (c) baseline-tier gate.
- §1.2 modality extension, not parallel machinery - sealed AudioSegment +
  LanguageIDResult carriers composed via import.

Owner HONESTY RULE verbatim (banked at
backend/services/rms_station_language_axis.py line 68 · sealed
MODEL_CORROBORATION_POLICY constant):
    'whisper-class models do NOT reliably distinguish Kikuyu/Luo/Kalenjin/
     Kamba etc. - where the model cant corroborate, the attribution is
     "station-prior (cited), model-corroboration: unavailable" - never
     present model output as confirming a language it cant detect. Where
     model says Swahili/English it corroborates those stations only.'

Composition (§1.2 modality extension):
- `compose_segment_provenance` invokes sealed `attribution_for_asset`
  from the RMS station-language-axis service and produces a
  well-formed IngestionSegmentProvenance_v1 carrying detected +
  station_prior LanguageEvidence entries plus condition + switch-points +
  optional synthesis-group ref.
- The composer NEVER writes model-output as station corroboration for a
  vernacular station (Kikuyu/Dholuo/Kalenjin/Kamba/etc.); the sealed
  HONESTY RULE dictates that.

The §4.6 gate `assert_provenance_meets_section_4_6` is fail-closed per
§1.5 unrepresentable-not-policed - it accepts a well-formed provenance
and refuses (a) empty languages, (b) missing condition profile, (c)
baseline_tier_captured=False for admitted material. (§4.6 (b) dedup-map
branch lands in CP-AIP-2.)
"""
from __future__ import annotations

from typing import Optional, Tuple

from backend.services.audio_plane_v1.ingestion_provenance_v1 import (
    ConditionProfileRef_v1,
    IngestionProvenanceIncomplete,
    IngestionSegmentProvenance_v1,
    LanguageEvidence_v1,
    SwitchPointFact_v1,
    SynthesisGroupAttributesRef_v1,
)
from backend.services.audio_plane_v1.language_identifier import (
    AudioSegment,
    LanguageIDResult,
)
from backend.services.rms_station_language_axis import (
    WHISPER_CORROBORATABLE_LANGUAGES,
    _lookup_station,
    attribution_for_asset,
)


# =============================================================================
# Refusal class
# =============================================================================


class IngestionProvenanceRefused(Exception):
    """§4.6 gate refusal · a fully-constructed provenance record fails the
    §4.6 gate. Distinct from IngestionProvenanceIncomplete which fires at
    construction time; this fires at the gate for §4.6 (c) baseline-tier
    admitted-material check (or any downstream policy check).
    """


# =============================================================================
# §4.1 station-prior composer + HONESTY RULE application
# =============================================================================


def _station_prior_evidence_from_axis(
    station_name: str,
) -> Optional[LanguageEvidence_v1]:
    """Compose a LanguageEvidence_v1 with source='station_prior' from the
    sealed RMS station-language axis, or None if station unknown.

    Cites station record fields verbatim per owner 'all research with
    title' directive.
    """
    record = _lookup_station(station_name)
    if record is None:
        return None
    station_lang = str(record["primary_language"])
    citation_title = str(record["research_citation_title"])
    citation_url = str(record["research_citation_url"])
    return LanguageEvidence_v1(
        language_tag=station_lang,
        confidence=1.0,
        source="station_prior",
        research_citation_title=citation_title,
        research_citation_url=citation_url,
    )


def compose_segment_provenance(
    *,
    segment: AudioSegment,
    station_name: str,
    detected_language_result: LanguageIDResult,
    condition_profile_ref: ConditionProfileRef_v1,
    switch_points: Tuple[SwitchPointFact_v1, ...] = (),
    synthesis_group_attributes_ref: Optional[SynthesisGroupAttributesRef_v1] = None,
    baseline_tier_captured: bool = True,
) -> IngestionSegmentProvenance_v1:
    """§4.1 + owner GO reminder 2 composer.

    Produces a fully-formed IngestionSegmentProvenance_v1 carrying:
      - one LanguageEvidence with source='detected' (the actual identifier
        output), preserving `languages[]` plural discipline.
      - one LanguageEvidence with source='station_prior' (the RMS
        station-axis attribution, cited) when the station is known.
      - the §4.3 condition profile ref.
      - the §4.2 switch points (may be empty tuple).
      - the §4.4 group-level synthesis attribute ref (optional).
      - the §4.6 (c) baseline_tier_captured flag.
      - the owner HONESTY RULE artifact station_prior_corroborated flag
        set per sealed `attribution_for_asset` output.

    NEVER records model-output as station corroboration for a vernacular
    station (Kikuyu/Dholuo/Kalenjin/Kamba/etc.) per sealed HONESTY RULE.
    """
    # §4.1 detected evidence · sourced from the actual identifier
    # (owner reminder 2: 'the per-segment languages[] signal must come
    # from the actual identifier').
    detected_ev = LanguageEvidence_v1(
        language_tag=detected_language_result.language_tag,
        confidence=detected_language_result.confidence,
        source="detected",
        research_citation_title="",
        research_citation_url="",
    )

    # §4.1 station-prior evidence · cited attribution from sealed axis.
    station_prior_ev = _station_prior_evidence_from_axis(station_name)

    languages: Tuple[LanguageEvidence_v1, ...]
    if station_prior_ev is None:
        # Unknown station · only detected evidence lands.
        languages = (detected_ev,)
        station_prior_corroborated = False
    else:
        languages = (detected_ev, station_prior_ev)
        # Owner HONESTY RULE application via sealed attribution_for_asset.
        # `model_detected_language` is the detected language tag; we
        # compare model tag against WHISPER_CORROBORATABLE_LANGUAGES via
        # the sealed callable rather than duplicating the policy here.
        attribution = attribution_for_asset(
            station_name,
            detected_language_result.language_tag,
        )
        station_prior_corroborated = bool(attribution["corroborated"])

    return IngestionSegmentProvenance_v1(
        segment_ref=segment.segment_ref,
        languages=languages,
        condition_profile_ref=condition_profile_ref,
        switch_points=switch_points,
        synthesis_group_attributes_ref=synthesis_group_attributes_ref,
        baseline_tier_captured=baseline_tier_captured,
        station_prior_corroborated=station_prior_corroborated,
    )


# =============================================================================
# §4.6 gate · fail-closed per §1.5 unrepresentable-not-policed
# =============================================================================


def assert_provenance_meets_section_4_6(
    provenance: IngestionSegmentProvenance_v1,
) -> None:
    """§4.6 verbatim acceptance criteria gate.

    §4.6 (a) - languages non-empty + condition_profile_ref non-None: these
        two branches are already enforced at IngestionSegmentProvenance_v1
        construction time (see __post_init__). This gate re-checks
        defensively.

    §4.6 (c) - baseline-tier capture MUST run for all admitted material
        regardless of any active objective. Refuses provenance carrying
        baseline_tier_captured=False.

    §4.6 (b) - deduplicated item without its instance condition map fails
        the ingestion invariant test. This branch lands in CP-AIP-2 which
        wires the instance-condition-map field into the provenance shape.

    Returns None on pass. Raises IngestionProvenanceRefused on refusal.
    """
    # Defensive re-check of §4.6 (a) construction invariants:
    if len(provenance.languages) == 0:
        raise IngestionProvenanceRefused(
            "§4.6 (a) gate refusal · provenance has empty languages tuple "
            "(this should have been refused at construction time - "
            "defensive re-check)."
        )
    if provenance.condition_profile_ref is None:
        raise IngestionProvenanceRefused(
            "§4.6 (a) gate refusal · provenance has None "
            "condition_profile_ref (defensive re-check)."
        )
    # §4.6 (c) baseline-tier §9.2 admitted-material refusal:
    if not provenance.baseline_tier_captured:
        raise IngestionProvenanceRefused(
            "§4.6 (c) gate refusal · baseline-tier capture (§9.2) MUST "
            "run for all admitted material regardless of any active "
            "objective. baseline_tier_captured=False is a refusal at the "
            "ingestion boundary."
        )
    return None


__all__ = [
    "IngestionProvenanceRefused",
    "compose_segment_provenance",
    "assert_provenance_meets_section_4_6",
    # Re-exports for downstream composition convenience (§1.2 modality-
    # extension · not re-declarations):
    "AudioSegment",
    "LanguageIDResult",
    "WHISPER_CORROBORATABLE_LANGUAGES",
    "IngestionProvenanceIncomplete",
]
