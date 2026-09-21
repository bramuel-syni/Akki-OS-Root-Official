"""M6 · Audio-Plane v1.0 · CP-M6-5-3 · Cluster-stability invariants.

Discharge anchors (verbatim on single un-wrapped lines):

- Audio-Plane §5.3 P089 (V59 · clause 2 discipline gate end-to-end):
      "A cluster asserts that a distinct variant exists — not what it is called."

- M6 Sub-wave 5 grounding brief §C · CP-M6-5-3 (verbatim):
      "Cluster stability invariants. §5.3 clause 2 end-to-end: no cluster carrier carries a human-readable name across sample→bind lifecycle · clustering determinism gate on synthetic deterministic backend · clustering non-determinism refusal gate on synthetic non-deterministic reference backend."

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - Pure invariants + refusals over CP-M6-5-1 (`CandidateStratum` ·
    `ClusteringBackend`) and CP-M6-5-2 (`ValidatedStratum`) carriers.
  - Case-agnostic; no executive-domain tokens.
  - Synthetic fixtures only in tests.
  - §3.1 P038 tokens-not-waveforms discipline preserved.

Contract:

    HUMAN_NAME_ATTRIBUTE_NAMES = (
        "human_name", "label", "display_name", "speaker_name",
        "cluster_name",
    )
      Frozen negative-scan attribute set for §5.3 clause 2 discipline.

    assert_cluster_carries_no_human_name(*, cluster) -> None
      §5.3 clause 2 verbatim gate.  Refuses
      `ClusterHumanNameLeakError` when any attribute in
      HUMAN_NAME_ATTRIBUTE_NAMES is present on `cluster` with a
      non-None value.  None-valued attributes pass — None is the
      canonical "not what it is called" value.

    assert_clustering_is_deterministic(*, backend, character_register)
        -> None
      Calls `backend.cluster(entries=character_register.entries)`
      twice back-to-back and compares stratum_id sequences.  Refuses
      `ClusteringNonDeterministicError` when the two runs emit
      different stratum_id sequences.

    assert_validated_stratum_preserves_candidate(
        *, validated, original_candidate,
    ) -> None
      Refuses `ValidatedStratumMutatedError` when the
      `ValidatedStratum.candidate_stratum` has drifted from the
      original `CandidateStratum` (compared by value equality on the
      frozen dataclass — identity-preserving in-lifecycle usage
      trivially satisfies value equality).

Refusals:
    ClusterHumanNameLeakError · ClusteringNonDeterministicError ·
    ValidatedStratumMutatedError.
"""

from __future__ import annotations

from typing import Any, Tuple

from services.audio_plane_v1.character_register import CharacterRegister
from services.audio_plane_v1.clustering import ClusteringBackend
from services.audio_plane_v1.human_validation import ValidatedStratum


HUMAN_NAME_ATTRIBUTE_NAMES: Tuple[str, ...] = (
    "human_name",
    "label",
    "display_name",
    "speaker_name",
    "cluster_name",
)
"""Frozen negative-scan attribute set for §5.3 clause 2 verbatim
discipline: any cluster-like carrier that surfaces a human-readable
name via any of these attribute names violates
'not what it is called'."""


class ClusterHumanNameLeakError(Exception):
    """Raised when a cluster-like carrier exposes a human-readable name.

    §5.3 clause 2 verbatim: "A cluster asserts that a distinct variant
    exists — not what it is called".  Any attribute in
    `HUMAN_NAME_ATTRIBUTE_NAMES` carrying a non-None value violates the
    discipline."""


class ClusteringNonDeterministicError(Exception):
    """Raised when a clustering backend emits different stratum_id
    sequences across two consecutive `cluster(entries=...)` calls.

    Determinism is a §5.3 clause 1 stability property: the clustering
    seam re-run on the same character stream MUST emit the same
    stratum_id sequence, or downstream sample/verdict/bind receipts
    lose their binding to a stable stratum identity."""


class ValidatedStratumMutatedError(Exception):
    """Raised when a `ValidatedStratum.candidate_stratum` has drifted
    from the original `CandidateStratum`.

    Preserves the CP-M6-5-2 bind invariant: the `ValidatedStratum`
    frozen carrier MUST retain the original `CandidateStratum` (by
    value equality) across the bind path — no in-flight mutation of
    the candidate is permitted."""


def assert_cluster_carries_no_human_name(*, cluster: Any) -> None:
    """§5.3 clause 2 verbatim gate: no cluster carrier carries a
    human-readable name.

    Refuses `ClusterHumanNameLeakError` when any attribute in
    `HUMAN_NAME_ATTRIBUTE_NAMES` is present on `cluster` with a
    non-None value.  None-valued attributes pass — None is the
    canonical "not what it is called" value (matches the CP-M6-5-2
    `HumanValidationVerdict.named_by_human` Optional default).

    Returns None on pass (per §5.3 clause 2: clean carriers stay
    silent).
    """
    for attr_name in HUMAN_NAME_ATTRIBUTE_NAMES:
        if not hasattr(cluster, attr_name):
            continue
        value = getattr(cluster, attr_name)
        if value is None:
            # None is the canonical "not what it is called" value.
            continue
        raise ClusterHumanNameLeakError(
            f"cluster carrier exposes human-readable name via "
            f"attribute {attr_name!r} with value {value!r}; §5.3 "
            f"clause 2 verbatim: a cluster asserts that a distinct "
            f"variant exists — not what it is called"
        )
    return None


def assert_clustering_is_deterministic(
    *,
    backend: ClusteringBackend,
    character_register: CharacterRegister,
) -> None:
    """§5.3 clause 1 stability gate: two consecutive
    `backend.cluster(entries=...)` calls on the same character stream
    MUST emit the same stratum_id sequence.

    Refuses `ClusteringNonDeterministicError` when the stratum_id
    sequences differ across the two runs.

    Returns None on pass.
    """
    entries = character_register.entries
    first = backend.cluster(entries=entries)
    second = backend.cluster(entries=entries)
    first_ids = tuple(s.stratum_id for s in first)
    second_ids = tuple(s.stratum_id for s in second)
    if first_ids != second_ids:
        raise ClusteringNonDeterministicError(
            f"clustering backend {backend.name!r} emitted different "
            f"stratum_id sequences across two consecutive runs on "
            f"identical entries: first={first_ids!r} second="
            f"{second_ids!r}; §5.3 clause 1 stability discipline "
            f"requires deterministic stratum_id emission"
        )
    return None


def assert_validated_stratum_preserves_candidate(
    *,
    validated: ValidatedStratum,
    original_candidate: Any,
) -> None:
    """§5.3 clause 2 end-to-end bind gate: the `ValidatedStratum`
    MUST preserve the original `CandidateStratum` across the bind
    path (no in-flight mutation).

    Refuses `ValidatedStratumMutatedError` when
    `validated.candidate_stratum != original_candidate` (frozen
    dataclass value equality — identity-preserving in-lifecycle
    usage trivially satisfies value equality).

    Returns None on pass.
    """
    if validated.candidate_stratum != original_candidate:
        raise ValidatedStratumMutatedError(
            f"validated.candidate_stratum has drifted from original "
            f"candidate: got {validated.candidate_stratum!r} expected "
            f"{original_candidate!r}; CP-M6-5-2 bind path MUST preserve "
            f"the original CandidateStratum by value equality"
        )
    return None
