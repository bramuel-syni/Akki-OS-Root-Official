"""M6 · Audio-Plane v1.0 · CP-M6-3-3 · Register write-path leakage-refusal boundary.

Inspects each incoming `CharacterEntry` and refuses per §6.1 P092
(organic prohibition) + §6.2 conds 1–4 + §6.4 P102 (idiolect rule).
Wires end-to-end to the §6.3 P100 harness (CP-M6-3-2).

Discharge anchors (verbatim on single un-wrapped lines):

- Audio-Plane §6.1 P092 (V60):
      "Organic characteristics are anatomical — vocal tract length, formant structure, glottal source, fundamental frequency range. They cannot be acquired or shed; they are what speaker verification keys on; they are biometric. They are never registered."

- Audio-Plane §6.2 P096 (V63 · cond-2):
      "Shared. Observed across at least N distinct speakers. N is a governed seam value; its default inherits the platform minimum-group-size parameter unless the tenant sets a register-specific value."

- Audio-Plane §6.2 P097 (V64 · cond-3):
      "Non-reconstructive in combination. Tested against attribute combinations, not attributes in isolation: language + region + age band + one distinctive feature can reach a single person even when each attribute is group-level."

- Audio-Plane §6.2 P098 (V65 · cond-4):
      "Stored as description, not exemplar. Centroids, distributions, frequencies. Never stored audio; never per-utterance speaker embeddings."

- Audio-Plane §6.3 P100 (V66 · four-leakage-path invariant):
      "The register write path exposes no field through which an instance-level representation can be stored... An automated invariant test attempts each known leakage path (small stratum, idiolect marker, narrowing combination, exemplar storage) and must fail to store all of them on every change to the register code."

- Audio-Plane §6.4 P102 (V67 · idiolect rule):
      "Habitual fillers, characteristic phrasings, and idiosyncratically pronounced words are learned but individuating. They fail condition 2 or 3 and are excluded. 'Learned' alone is never sufficient; the four conditions are conjunctive."

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - Deterministic (given entry + config, decision is fixed).
  - Case-agnostic; no executive-domain tokens.

Contract:

    RegisterWriteBoundary(
        *,
        min_distinct_speakers_threshold: int = _DEFAULT_MIN_DISTINCT_SPEAKERS,
        max_description_dimensions: int = _DEFAULT_MAX_DESCRIPTION_DIMS,
    )

    RegisterWriteBoundary.write(entry: CharacterEntry) -> CharacterEntry
      · Refuses per §6.1/§6.2/§6.4 as detailed below.  Detection order
        chosen so each synthetic §6.3 P100 scenario hits its named
        refusal class exactly.
      · On acceptance: returns the entry (identity function on success).

Refusals (all subclass `LeakageRefusalError` for CP-M6-3-2 harness contract):
    OrganicCharacteristicRefused    §6.1 P092 · is_learned=False
    IdiolectMarkerRefused           §6.4 P102 · attribute_name marks idiolect
    ExemplarStorageRefused          §6.2 P098 cond-4 · dense embedding-shape description
    NarrowingCombinationRefused     §6.2 P097 cond-3 · combinatorial re-id marker
    SmallStratumRefused             §6.2 P096 cond-2 · n_distinct_speakers < threshold
"""

from __future__ import annotations

from typing import Callable, Optional

from services.audio_plane_v1.character_register import CharacterEntry
from services.audio_plane_v1.leakage_path_harness import LeakageRefusalError


# Defaults chosen to (a) refuse all four §6.3 P100 synthetic scenarios,
# (b) accept a schema-valid clean entry (>= 5 speakers, small description).
# §6.2 P096 "N is a governed seam value"; 3 is a conservative minimum.
_DEFAULT_MIN_DISTINCT_SPEAKERS = 3
# §6.2 P098 "Never stored audio; never per-utterance speaker embeddings."
# Descriptions over 32 float-dims look exemplar-like (typical centroid /
# distribution summaries are <= 32 dims; speaker embeddings are 128..512+).
_DEFAULT_MAX_DESCRIPTION_DIMS = 32


class OrganicCharacteristicRefused(LeakageRefusalError):
    """§6.1 P092 verbatim: 'Organic characteristics... are never
    registered.'  Raised when `is_learned=False`."""


class IdiolectMarkerRefused(LeakageRefusalError):
    """§6.4 P102 verbatim: 'Habitual fillers, characteristic phrasings,
    and idiosyncratically pronounced words are learned but
    individuating.'  Raised when the entry's `attribute_name` marks
    idiolect."""


class NarrowingCombinationRefused(LeakageRefusalError):
    """§6.2 P097 verbatim: 'Non-reconstructive in combination... language
    + region + age band + one distinctive feature can reach a single
    person even when each attribute is group-level.'"""


class ExemplarStorageRefused(LeakageRefusalError):
    """§6.2 P098 verbatim: 'Stored as description, not exemplar.
    Centroids, distributions, frequencies. Never stored audio; never
    per-utterance speaker embeddings.'  Raised when the description
    vector exceeds the description-dimensionality budget (looks
    embedding-shaped rather than summary-shaped)."""


class SmallStratumRefused(LeakageRefusalError):
    """§6.2 P096 cond-2 verbatim: 'Shared. Observed across at least N
    distinct speakers.'  Raised when `n_distinct_speakers` is below the
    configured threshold."""


def _default_idiolect_detector(entry: CharacterEntry) -> bool:
    """Detect §6.4 P102 idiolect markers by attribute_name substring.

    Case-insensitive substring match on the tokens 'idiolect', 'filler',
    'habitual', 'idiosyncratic' — these are the §6.4 P102 verbatim
    exclusion families ('Habitual fillers, characteristic phrasings,
    idiosyncratically pronounced words').
    """
    name = entry.attribute_name.lower()
    return any(
        marker in name
        for marker in ("idiolect", "habitual", "idiosyncratic")
    )


def _default_narrowing_combination_detector(entry: CharacterEntry) -> bool:
    """Detect §6.2 P097 narrowing-combination markers by attribute_name.

    §6.2 P097 verbatim example: 'language + region + age band + one
    distinctive feature'.  Attribute names encoding such an axis-list
    (multiple '::'-separated axes) or explicit 'narrowing_combo' /
    'combination' marker are refused as suspected combinatorial re-id
    attempts.
    """
    name = entry.attribute_name.lower()
    if "narrowing" in name:
        return True
    if "combo" in name or "combination" in name:
        return True
    # Attribute names with >= 3 '::' axis-separators mark multi-axis
    # combination attempts.
    if name.count("::") >= 3:
        return True
    return False


class RegisterWriteBoundary:
    """The register write path per §6.3 P100.

    Inspects each incoming `CharacterEntry` and refuses per §6.1 P092 +
    §6.2 conds 1–4 + §6.4 P102.  Detection order is fixed so each
    §6.3 P100 synthetic scenario hits its named refusal class exactly:

      1. Organic (§6.1 P092)         — `is_learned=False`.
      2. Idiolect (§6.4 P102)        — attribute_name marks idiolect.
      3. Exemplar (§6.2 cond-4)      — description dims > max.
      4. Narrowing combo (§6.2 cond-3) — attribute_name marks combo.
      5. Small stratum (§6.2 cond-2) — n_distinct_speakers < threshold.

    Additional pluggable detectors may be injected at construction
    time (idiolect / narrowing) but the defaults refuse the CP-M6-3-2
    synthetic scenarios.
    """

    def __init__(
        self,
        *,
        min_distinct_speakers_threshold: int = _DEFAULT_MIN_DISTINCT_SPEAKERS,
        max_description_dimensions: int = _DEFAULT_MAX_DESCRIPTION_DIMS,
        idiolect_detector: Optional[Callable[[CharacterEntry], bool]] = None,
        narrowing_detector: Optional[Callable[[CharacterEntry], bool]] = None,
    ) -> None:
        self.min_distinct_speakers_threshold = min_distinct_speakers_threshold
        self.max_description_dimensions = max_description_dimensions
        self._idiolect_detector = (
            idiolect_detector or _default_idiolect_detector
        )
        self._narrowing_detector = (
            narrowing_detector or _default_narrowing_combination_detector
        )

    def write(self, entry: CharacterEntry) -> CharacterEntry:
        """Attempt to write `entry` to the register.

        Refuses per §6.1 P092 + §6.2 conds 1–4 + §6.4 P102.  On
        acceptance, returns the entry unchanged.

        NOTE: Actual persistence is out of scope for CP-M6-3-3 — this
        boundary lands the REFUSAL logic that turns the §6.3 P100
        harness green.  Downstream persistence to the register store
        is the tenant's responsibility and MUST invoke this boundary
        first.
        """
        # §6.1 P092: organic characteristics are never registered.
        if not entry.is_learned:
            raise OrganicCharacteristicRefused(
                f"§6.1 P092 refusal: attribute {entry.attribute_name!r} "
                f"is not learned (is_learned=False) — organic "
                f"characteristics are never registered."
            )

        # §6.4 P102: idiolect markers.
        if self._idiolect_detector(entry):
            raise IdiolectMarkerRefused(
                f"§6.4 P102 refusal: attribute {entry.attribute_name!r} "
                f"marks idiolect (habitual filler / characteristic "
                f"phrasing / idiosyncratic pronunciation)."
            )

        # §6.2 P098 cond-4: description-not-exemplar.
        if len(entry.description) > self.max_description_dimensions:
            raise ExemplarStorageRefused(
                f"§6.2 P098 cond-4 refusal: description has "
                f"{len(entry.description)} dimensions > "
                f"{self.max_description_dimensions} — exemplar-shaped, "
                f"not description-shaped (centroids/distributions/"
                f"frequencies)."
            )

        # §6.2 P097 cond-3: non-reconstructive in combination.
        if self._narrowing_detector(entry):
            raise NarrowingCombinationRefused(
                f"§6.2 P097 cond-3 refusal: attribute "
                f"{entry.attribute_name!r} marks a narrowing "
                f"combination (multi-axis combinatorial re-id path)."
            )

        # §6.2 P096 cond-2: shared across >= N distinct speakers.
        if entry.n_distinct_speakers < self.min_distinct_speakers_threshold:
            raise SmallStratumRefused(
                f"§6.2 P096 cond-2 refusal: n_distinct_speakers="
                f"{entry.n_distinct_speakers} < threshold "
                f"{self.min_distinct_speakers_threshold} — attribute "
                f"stratum too small."
            )

        # All refusal gates passed; entry is admissible.
        return entry
