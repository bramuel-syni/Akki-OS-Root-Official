"""CP-AIP-2-DEDUP-CONDITION-MAP · AIP v1.0 §4.6 (b) gate + §4.5 composer.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-2-DEDUP-CONDITION-MAP and nothing else.

Spec anchor:
- §4.5 dedup as augmentation - composer composes sealed
  construct_instance_condition_map (CP-M6-2-1) + CP-AIP-1
  IngestionSegmentProvenance_v1 into DedupInstanceProvenance_v1.
- §4.6 (b) - gate callable using sealed
  dedup_item_has_instance_condition_map helper (CP-M6-2-1) to enforce
  'A deduplicated item without its instance condition map fails the
  ingestion invariant test.'
- §1.2 modality-extension - composition via imports; no parallel
  redeclaration of sealed carriers.

Sealed carriers UNCHANGED per SO §3.8 (composed by this module):
- backend/services/audio_plane_v1/instance_condition_map.py (CP-M6-2-1)
- backend/services/audio_plane_v1/ingestion_provenance_v1.py (CP-AIP-1)
- backend/services/audio_plane_v1/dedup_instance_provenance_v1.py (CP-AIP-2 sealed by this seal · dataclass carriers)
"""
from __future__ import annotations

from typing import Sequence

from backend.services.audio_plane_v1.dedup_instance_provenance_v1 import (
    DedupInstanceProvenance_v1,
    DedupInstanceProvenanceIncomplete,
    RobustnessStratumTag_v1,
)
from backend.services.audio_plane_v1.instance_condition_map import (
    InstanceConditionVariant,
    construct_instance_condition_map,
    dedup_item_has_instance_condition_map,
)
from backend.services.audio_plane_v1.ingestion_provenance_v1 import (
    IngestionSegmentProvenance_v1,
)


# =============================================================================
# Refusal class
# =============================================================================


class DedupInstanceProvenanceRefused(Exception):
    """§4.6 (b) gate refusal · a dedup item that fails the ingestion
    invariant. Distinct from DedupInstanceProvenanceIncomplete which
    fires at construction; this fires at the runtime gate.
    """


# =============================================================================
# §4.5 composer · uses sealed construct_instance_condition_map (§1.2)
# =============================================================================


_DEFAULT_STRATUM_NAME = "dedup_variant_channel_time_condition"


def compose_dedup_instance_provenance(
    *,
    base_provenance: IngestionSegmentProvenance_v1,
    canonical_extraction_ref: str,
    occurrence_index_ref: str,
    variants: Sequence[InstanceConditionVariant],
    dedup_role: str,
    stratum_name: str = _DEFAULT_STRATUM_NAME,
) -> DedupInstanceProvenance_v1:
    """§4.5 composer · produces DedupInstanceProvenance_v1.

    Invokes sealed construct_instance_condition_map (CP-M6-2-1) to build
    the InstanceConditionMap - empty/invalid variants raise sealed
    VariantsEmptyError / VariantInvalidError verbatim (§1.2 composition).

    Attaches a §4.5 RobustnessStratumTag_v1 with zero_acquisition_cost=
    True (verbatim from §4.5: 'the variant set enters training curricula
    as a designated robustness stratum at zero acquisition cost').

    §1.2 modality-extension: composes CP-AIP-1 base_provenance rather
    than redeclaring; wraps sealed InstanceConditionMap rather than
    re-implementing the map schema.
    """
    icm = construct_instance_condition_map(
        canonical_extraction_ref=canonical_extraction_ref,
        occurrence_index_ref=occurrence_index_ref,
        variants=variants,
    )
    stratum = RobustnessStratumTag_v1(
        stratum_name=stratum_name,
        zero_acquisition_cost=True,
    )
    return DedupInstanceProvenance_v1(
        base_provenance=base_provenance,
        instance_condition_map=icm,
        dedup_role=dedup_role,  # type: ignore[arg-type]
        robustness_stratum=stratum,
    )


# =============================================================================
# §4.6 (b) gate · uses sealed dedup_item_has_instance_condition_map
# =============================================================================


def assert_dedup_provenance_meets_section_4_6_b(item: object) -> None:
    """§4.6 (b) verbatim acceptance criterion gate.

    Uses sealed `dedup_item_has_instance_condition_map(item)` helper
    (CP-M6-2-1) rather than re-implementing the attribute check
    parallel-fashion (§1.2 modality-extension).

    §4.6 (b) verbatim: 'A deduplicated item without its instance
    condition map fails the ingestion invariant test.'

    Raises DedupInstanceProvenanceRefused if:
      - item has no `instance_condition_map` attribute,
      - the attribute is None,
      - the attribute is the wrong type, OR
      - the attribute's variants tuple is empty.
    """
    if not dedup_item_has_instance_condition_map(item):
        raise DedupInstanceProvenanceRefused(
            "§4.6 (b) gate refusal · a deduplicated item without its "
            "instance condition map fails the ingestion invariant test. "
            "The item lacks a valid `instance_condition_map` attribute "
            "(missing / None / wrong type / empty variants). Sealed "
            "helper `dedup_item_has_instance_condition_map` (CP-M6-2-1) "
            "returned False."
        )
    return None


__all__ = [
    "DedupInstanceProvenanceRefused",
    "compose_dedup_instance_provenance",
    "assert_dedup_provenance_meets_section_4_6_b",
]
