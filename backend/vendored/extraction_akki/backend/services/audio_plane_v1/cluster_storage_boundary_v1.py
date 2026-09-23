"""CP-AIP-5-CLUSTERING · cluster storage boundary · additive §1.2 modality-extension.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-5-CLUSTERING and nothing else.

Spec anchor: AIP v1.0 §5.3 (character-register clustering acceptance).

§5.3 P089 verbatim (V59):
    "Unsupervised clustering over the character stream yields candidate
    strata. A cluster asserts that a distinct variant exists — not what
    it is called. Naming and validation are human work applied to a
    sample, commissioned like any other qualified work with quoted cost."

Custody invariant tie-in (§6.3 P100 four-leakage-path harness from CP-AIP-3):
  - Storage refuses clusters with fewer than N distinct speakers (§6.2 cond-2).
  - Storage refuses per-utterance identifiers in the payload (§6.2 cond-4).
  - Storage refuses proposed names at storage time (§5.3 clause 2 verbatim).

§1.2 modality-extension: this module COMPOSES sealed carriers:
  - CP-M6-5-1 CandidateStratum + cluster_character_register (clustering.py).
  - CP-M6-5-3 assert_cluster_carries_no_human_name (cluster_stability.py).
  - CP-AIP-3 WriteBoundaryConfig_v1 governed seam (character_register_write_boundary_v1.py).

Sealed carriers are IMPORTED, NEVER REDECLARED.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final, Optional, Tuple

from backend.services.audio_plane_v1.clustering import (
    CandidateStratum,
)
from backend.services.audio_plane_v1.cluster_stability import (
    assert_cluster_carries_no_human_name,
)
from backend.services.audio_plane_v1.character_register_write_boundary_v1 import (
    DEFAULT_CONFIG,
    WriteBoundaryConfig_v1,
)


HONEST_GAP_V1_POSTURE: Final[str] = (
    "AIP v1.0 §5.3 clause 2 verbatim: a cluster asserts that a distinct "
    "variant exists - not what it is called. Naming and validation are "
    "human work applied to a sample, commissioned like any other "
    "qualified work with quoted cost."
)


class ClusterStorageRefused(Exception):
    """Base class for cluster storage refusals at the CP-AIP-5 boundary."""


class SmallClusterRefused(ClusterStorageRefused):
    """Raised when a candidate stratum's distinct-speaker count falls
    below the governed CP-AIP-3 WriteBoundaryConfig_v1 minimum_group_size
    (§6.2 cond-2 verbatim).
    """


class NamedAtStorageRefused(ClusterStorageRefused):
    """Raised when the caller passes a `proposed_name_at_storage_time`.
    §5.3 clause 2 verbatim: 'a cluster asserts that a distinct variant
    exists - not what it is called'. The only path to a name is the
    commission wrapper post-storage (`cluster_naming_commission_v1`).
    """


class ClusterHumanNameLeakAtStorageRefused(ClusterStorageRefused):
    """Raised when the sealed CP-M6-5-3 assert_cluster_carries_no_human_name
    gate refuses the candidate stratum at storage time.
    """


@dataclass(frozen=True)
class StoredClusterCandidate_v1:
    """Storage-side payload for a candidate stratum.

    Four carriers - description-shape only per §5.3 clause 2 + §6.2 cond-4:
      - `stratum_id` - opaque identifier from the backend (§5.3 clause 1
        verbatim: 'not what it is called'; a stable id, not a name).
      - `member_attribute_names` - immutable tuple of attribute names on
        the CharacterRegister (description-shape only).
      - `backend_name` - clustering backend provenance (§6.2 P098:
        provenance points to material, not to speaker identity).
      - `name` - MUST be None until the human naming commission
        completes. §5.3 clause 2 verbatim + acceptance criterion 4.

    Structural discipline (§6.2 cond-4 verbatim + §1.5 unrepresentable-
    not-policed): this dataclass carries NO per-utterance-identifier
    fields. No `utterance_id` / `utterance_bytes` / `audio_ bytes` /
    `raw_ audio` / `per_utterance_embedding` / `speaker_id` /
    `speaker_embedding` / `voiceprint`.
    """

    stratum_id: str
    member_attribute_names: Tuple[str, ...]
    backend_name: str
    name: Optional[str] = None


def store_cluster_candidate(
    *,
    stratum: CandidateStratum,
    n_distinct_speakers: int,
    config: Optional[WriteBoundaryConfig_v1] = None,
    proposed_name_at_storage_time: Optional[str] = None,
) -> StoredClusterCandidate_v1:
    """Store a candidate stratum with fail-closed §5.3 / §6.2 refusals.

    Refusals (order matters - fails at the first tripped guard):
      1. `NamedAtStorageRefused` when `proposed_name_at_storage_time` is
         non-None (§5.3 clause 2 verbatim).
      2. `SmallClusterRefused` when `n_distinct_speakers <
         cfg.minimum_group_size` (§6.2 cond-2 verbatim · governed seam).
      3. `ClusterHumanNameLeakAtStorageRefused` when the sealed
         CP-M6-5-3 assert_cluster_carries_no_human_name gate refuses
         the stratum carrier (§5.3 clause 2 end-to-end).

    Returns a frozen StoredClusterCandidate_v1 with `name=None` on pass.
    """
    if proposed_name_at_storage_time is not None:
        raise NamedAtStorageRefused(
            f"CP-AIP-5: proposed_name_at_storage_time="
            f"{proposed_name_at_storage_time!r} refused; §5.3 clause 2 "
            f"verbatim - a cluster asserts a distinct variant exists, "
            f"not what it is called. Use cluster_naming_commission_v1 "
            f"post-storage."
        )

    cfg = config if config is not None else DEFAULT_CONFIG
    if n_distinct_speakers < cfg.minimum_group_size:
        raise SmallClusterRefused(
            f"CP-AIP-5: n_distinct_speakers={n_distinct_speakers} < "
            f"minimum_group_size={cfg.minimum_group_size} (governed seam "
            f"WriteBoundaryConfig_v1 · §6.2 cond-2 verbatim); refusing "
            f"to store candidate stratum {stratum.stratum_id!r}."
        )

    # §5.3 clause 2 end-to-end: sealed CP-M6-5-3 gate on the stratum.
    try:
        assert_cluster_carries_no_human_name(cluster=stratum)
    except Exception as ex:  # ClusterHumanNameLeakError from sealed CP-M6-5-3
        raise ClusterHumanNameLeakAtStorageRefused(
            f"CP-AIP-5: sealed CP-M6-5-3 gate refused stratum "
            f"{stratum.stratum_id!r}: {ex}"
        ) from ex

    return StoredClusterCandidate_v1(
        stratum_id=stratum.stratum_id,
        member_attribute_names=stratum.member_attribute_names,
        backend_name=stratum.backend_name,
        name=None,  # §5.3 clause 2 verbatim + acceptance criterion 4.
    )
