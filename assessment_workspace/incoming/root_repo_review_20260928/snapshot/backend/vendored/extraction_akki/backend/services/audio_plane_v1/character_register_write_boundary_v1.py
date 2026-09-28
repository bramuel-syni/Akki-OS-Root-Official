"""CP-AIP-3-CHARACTER-REGISTER · AIP v1.0 §6 write-path leakage-refusal boundary.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-3-CHARACTER-REGISTER and nothing else.

Spec anchor (AIP v1.0):
- §6.1 P092 verbatim: 'Organic characteristics are anatomical - vocal
  tract length, formant structure, glottal source, fundamental
  frequency range. They cannot be acquired or shed; they are what
  speaker verification keys on; they are biometric. They are never
  registered.'
- §6.1 P093 verbatim: 'Learned characteristics are acquired from a
  speech community - phonological inventory, pronunciation variants,
  prosody, code-switching habits. They are group properties by
  construction. Only learned characteristics may be registered.'
- §6.2 P095..P098 verbatim four conjunctive conditions (all must hold):
    P095 cond-1: acquired, not anatomical (learnable).
    P096 cond-2: shared - observed across at least N distinct speakers.
    P097 cond-3: non-reconstructive in combination.
    P098 cond-4: stored as description, not exemplar - centroids,
        distributions, frequencies; never audio; never per-utterance
        embeddings; embeddings destroyed after cluster assignment;
        provenance points to material, not to speaker identity.
- §6.3 P100 verbatim (V66 · four-leakage-path invariant): 'The register
  write path exposes no field through which an instance-level
  representation can be stored: the schema cannot represent a
  voiceprint. Unrepresentable, not policed (§1.5). An automated
  invariant test attempts each known leakage path (small stratum,
  idiolect marker, narrowing combination, exemplar storage) and must
  fail to store all of them on every change to the register code.'
- §6.4 P102 verbatim (V67 · idiolect exclusion): 'Habitual fillers,
  characteristic phrasings, and idiosyncratically pronounced words
  are learned but individuating. They fail condition 2 or 3 and are
  excluded.'
- §1.2 Modality-extension · §1.5 Unrepresentable-not-policed.
- §16.2 governed seam - platform minimum-group-size.

Owner reminder 4 verbatim (2026-02-23 · HARD GATE):
    "CP-AIP-3 is the hard gate: the custody invariant harness (four
    leakage paths - small stratum, idiolect marker, narrowing
    combination, exemplar storage - all must FAIL to store) must be
    GREEN before any CP-AIP-5 cluster is stored."

Owner content anchors (2026-02-23 · this seal):
    (a) §6.2 conditions are CONJUNCTIVE - 'learned' alone is never
        sufficient; the idiolect rule (§6.4) must be its own test case.
    (b) §6.2.4 - clustering embeddings destroyed after cluster
        assignment; provenance points to material never speaker
        identity; the write-path schema must have NO field capable of
        representing an instance-level voiceprint (§6.3
        unrepresentable-not-policed).

Sealed carriers composed by this module (UNCHANGED per SO §3.8):
- backend/services/audio_plane_v1/character_register.py (CP-M6-3-1 · schema-only frozen carriers).
- backend/services/audio_plane_v1/leakage_path_harness.py (CP-M6-3-2 · LeakageRefusalError base class + harness contract).

Design:
- Five typed refusal sentinels (SmallStratumRefused,
  IdiolectMarkerRefused, NarrowingCombinationRefused,
  ExemplarStorageRefused, NonLearnedRefused) all subclass sealed
  LeakageRefusalError per CP-M6-3-2 harness contract.
- WriteBoundaryConfig_v1 governed-seam bundle (frozen dataclass) - N
  minimum-group-size · idiolect marker registry · narrowing-combination
  detector · exemplar-storage detector - default constants encode the
  platform-minimum seam. §16.2 governed seam surface.
- write_character_entry(entry, *, config=DEFAULT_CONFIG) refuses
  leakage attempts BEFORE any persistence occurs. Persistence itself
  is NOT this seal's scope - this is the boundary that stops leakage
  before persistence would happen (§1.5 unrepresentable-not-policed).

Wave-honest limits:
- No LLM invocation. No HTTP call. No filesystem write.
- Case-agnostic; no executive-domain tokens.
- All inline detectors use SYNTHETIC / attribute-name-shape heuristics.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Optional

from backend.services.audio_plane_v1.character_register import (
    CharacterEntry,
)
from backend.services.audio_plane_v1.leakage_path_harness import (
    LeakageRefusalError,
)


# =============================================================================
# Five typed refusal sentinels · all subclass sealed LeakageRefusalError
# (CP-M6-3-2 harness contract · classifiable as protective refusals).
# =============================================================================


class SmallStratumRefused(LeakageRefusalError):
    """§6.2 P096 cond-2 refusal · `n_distinct_speakers` below the governed
    minimum-group-size seam value (§16.2)."""


class IdiolectMarkerRefused(LeakageRefusalError):
    """§6.4 P102 refusal · attribute matches a known idiolect marker
    (habitual filler / characteristic phrasing / idiosyncratically
    pronounced word) - individuating despite being learned."""


class NarrowingCombinationRefused(LeakageRefusalError):
    """§6.2 P097 cond-3 refusal · attribute encodes a narrowing
    combination (language + region + age-band + distinctive-feature)
    that reaches a single person in combination even if each attribute
    is group-level in isolation."""


class ExemplarStorageRefused(LeakageRefusalError):
    """§6.2 P098 cond-4 refusal · description vector is exemplar-shaped
    (dense per-utterance embedding · dim exceeds the governed
    description-dim seam) rather than a group-level centroid /
    distribution / frequency summary."""


class NonLearnedRefused(LeakageRefusalError):
    """§6.1 P092/P093 refusal · `is_learned=False` means the attribute is
    organic / anatomical / biometric and is NEVER registered.
    Conjunctive cond-1 (acquired, not anatomical) violation."""


# =============================================================================
# WriteBoundaryConfig_v1 · governed-seam bundle (§16.2 platform minimum)
# =============================================================================


# Idiolect-marker substrings (§6.4 P102) - attribute names carrying any
# of these markers are treated as idiolect / individuating.
_DEFAULT_IDIOLECT_MARKER_TOKENS: FrozenSet[str] = frozenset({
    "idiolect",
    "habitual_filler",
    "characteristic_phrasing",
    "idiosyncratic",
})


# Narrowing-combination markers (§6.2 cond-3) - attribute names carrying
# multiple facet-separators ('::') and simultaneously referencing
# region + age-band + distinctive-feature are treated as narrowing.
_DEFAULT_NARROWING_COMBO_FACET_TOKENS: FrozenSet[str] = frozenset({
    "region_",
    "age_band_",
    "distinctive_feature_",
})


@dataclass(frozen=True)
class WriteBoundaryConfig_v1:
    """Governed-seam bundle for the CP-AIP-3 write-path leakage-refusal
    boundary. §16.2 platform-minimum defaults; tenants may override per
    register (out of scope for this seal - defaults only).

    Six carriers:
      - `minimum_group_size` (§6.2 cond-2 · N) - default 5. Any entry
        with `n_distinct_speakers < minimum_group_size` refused with
        SmallStratumRefused.
      - `idiolect_marker_tokens` (§6.4 P102) - substrings that identify
        an idiolect / individuating attribute in `attribute_name`.
      - `narrowing_combo_facet_tokens` (§6.2 cond-3) - substrings that,
        when >=2 occur simultaneously in one attribute_name, identify a
        narrowing combination.
      - `narrowing_combo_min_facets` (§6.2 cond-3) - minimum facet count
        that triggers a narrowing refusal. Default 2.
      - `exemplar_description_dim_ceiling` (§6.2 cond-4) - max allowed
        length of the description tuple; anything longer is exemplar-
        shaped and refused.
      - `exemplar_forbidden_tokens` (§6.2 cond-4) - substrings in
        `attribute_name` that identify explicit exemplar-storage
        attempts (e.g. 'exemplar', 'utterance_embedding').
    """

    minimum_group_size: int = 5
    idiolect_marker_tokens: FrozenSet[str] = field(
        default_factory=lambda: _DEFAULT_IDIOLECT_MARKER_TOKENS,
    )
    narrowing_combo_facet_tokens: FrozenSet[str] = field(
        default_factory=lambda: _DEFAULT_NARROWING_COMBO_FACET_TOKENS,
    )
    narrowing_combo_min_facets: int = 2
    exemplar_description_dim_ceiling: int = 64
    exemplar_forbidden_tokens: FrozenSet[str] = field(
        default_factory=lambda: frozenset({
            "exemplar",
            "utterance_embedding",
            "per_utterance_embedding",
            "voiceprint",
        }),
    )


DEFAULT_CONFIG: WriteBoundaryConfig_v1 = WriteBoundaryConfig_v1()


# =============================================================================
# Internal detectors (case-agnostic · attribute-name-shape heuristics)
# =============================================================================


def _has_any_token(attribute_name: str, tokens: FrozenSet[str]) -> bool:
    lowered = attribute_name.lower()
    return any(t in lowered for t in tokens)


def _count_narrowing_facets(
    attribute_name: str,
    facet_tokens: FrozenSet[str],
) -> int:
    lowered = attribute_name.lower()
    return sum(1 for t in facet_tokens if t in lowered)


# =============================================================================
# Public write-path · four-leakage-path refusal boundary
# =============================================================================


def write_character_entry(
    entry: CharacterEntry,
    *,
    config: Optional[WriteBoundaryConfig_v1] = None,
) -> None:
    """§6.3 P100 write-path leakage-refusal boundary.

    Evaluates each of the four §6.3 P100 leakage paths (plus the §6.1
    P093 organic-exclusion) against `entry`. On any violation, raises
    the corresponding typed sentinel BEFORE any persistence occurs.
    Returns None on acceptance.

    Refusal order (fails-fast · owner content anchor (a) 2026-02-23
    'learned alone is never sufficient'):
      1. §6.1 P093 - is_learned=False -> NonLearnedRefused.
      2. §6.4 P102 - idiolect marker -> IdiolectMarkerRefused.
      3. §6.2 cond-3 - narrowing combination -> NarrowingCombinationRefused.
      4. §6.2 cond-4 - exemplar-shape description -> ExemplarStorageRefused.
      5. §6.2 cond-2 - small stratum -> SmallStratumRefused.

    Persistence itself is NOT this seal's scope - this is the boundary
    that stops leakage before persistence would happen (§1.5
    unrepresentable-not-policed).
    """
    cfg = config if config is not None else DEFAULT_CONFIG

    # §6.1 P093 · organic-exclusion (cond-1 conjunctive violation).
    if not entry.is_learned:
        raise NonLearnedRefused(
            "§6.1 P093 verbatim: 'Only learned characteristics may be "
            f"registered.' Entry {entry.attribute_name!r} has "
            f"is_learned=False - organic / anatomical / biometric "
            f"attributes are NEVER registered."
        )

    # §6.4 P102 · idiolect marker.
    if _has_any_token(entry.attribute_name, cfg.idiolect_marker_tokens):
        raise IdiolectMarkerRefused(
            "§6.4 P102 verbatim: 'Habitual fillers, characteristic "
            "phrasings, and idiosyncratically pronounced words are "
            "learned but individuating. They fail condition 2 or 3 and "
            f"are excluded.' Entry {entry.attribute_name!r} carries an "
            f"idiolect marker token."
        )

    # §6.2 cond-3 · narrowing combination.
    facet_count = _count_narrowing_facets(
        entry.attribute_name, cfg.narrowing_combo_facet_tokens,
    )
    if facet_count >= cfg.narrowing_combo_min_facets:
        raise NarrowingCombinationRefused(
            "§6.2 P097 cond-3 verbatim: 'Non-reconstructive in "
            "combination. Tested against attribute combinations, not "
            "attributes in isolation: language + region + age band + "
            "one distinctive feature can reach a single person even "
            f"when each attribute is group-level.' Entry "
            f"{entry.attribute_name!r} carries {facet_count} narrowing "
            f"facet tokens (>= {cfg.narrowing_combo_min_facets})."
        )

    # §6.2 cond-4 · exemplar-shape description (dim ceiling).
    if len(entry.description) > cfg.exemplar_description_dim_ceiling:
        raise ExemplarStorageRefused(
            "§6.2 P098 cond-4 verbatim: 'Stored as description, not "
            "exemplar. Centroids, distributions, frequencies. Never "
            "stored audio; never per-utterance speaker embeddings.' "
            f"Entry {entry.attribute_name!r} description dim "
            f"{len(entry.description)} exceeds ceiling "
            f"{cfg.exemplar_description_dim_ceiling} - exemplar-shaped."
        )

    # §6.2 cond-4 · exemplar attribute-name marker.
    if _has_any_token(entry.attribute_name, cfg.exemplar_forbidden_tokens):
        raise ExemplarStorageRefused(
            "§6.2 P098 cond-4 verbatim: exemplar-storage attempt "
            f"detected in attribute_name {entry.attribute_name!r} "
            f"(matches forbidden token). NEVER stored audio; NEVER "
            f"per-utterance speaker embeddings."
        )

    # §6.2 cond-2 · small stratum (final gate · owner content anchor (a)
    # 'conjunctive' - satisfying cond-1 alone does not grant admission).
    if entry.n_distinct_speakers < cfg.minimum_group_size:
        raise SmallStratumRefused(
            "§6.2 P096 cond-2 verbatim: 'Shared. Observed across at "
            f"least N distinct speakers.' Entry {entry.attribute_name!r} "
            f"has n_distinct_speakers={entry.n_distinct_speakers} < "
            f"minimum_group_size={cfg.minimum_group_size} (governed "
            f"seam §16.2 platform-minimum default)."
        )

    # All four §6.3 P100 leakage paths + §6.1 P093 organic-exclusion
    # cleared. Entry passes the write-path leakage-refusal boundary.
    # Persistence itself is out of scope for this seal.
    return None
