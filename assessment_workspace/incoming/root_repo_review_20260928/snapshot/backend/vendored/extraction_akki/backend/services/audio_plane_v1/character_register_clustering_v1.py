"""CP-AIP-3-CHARACTER-REGISTER · AIP v1.0 §6.2 cond-4 embedding-destruction after cluster assignment.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-3-CHARACTER-REGISTER and nothing else.

Spec anchor (AIP v1.0):
- §6.2 P098 cond-4 verbatim: 'Stored as description, not exemplar.
  Centroids, distributions, frequencies. Never stored audio; never
  per-utterance speaker embeddings. Embeddings used during clustering
  are destroyed after cluster assignment. Provenance points to
  material, not to speaker identity.'
- §1.2 Modality-extension · §1.5 Unrepresentable-not-policed.

Owner content anchor (b) 2026-02-23 (this seal):
    '§6.2.4 - clustering embeddings destroyed after cluster
    assignment; provenance points to material never speaker
    identity; the write-path schema must have NO field capable of
    representing an instance-level voiceprint (§6.3
    unrepresentable-not-policed).'

Design:
- `assign_clusters_destroy_embeddings` takes a MUTABLE list of
  per-utterance embeddings, performs cluster assignment, and DESTROYS
  the input list in place (list.clear()) before returning. The return
  type carries ONLY group-level centroid tuples - no per-utterance
  embeddings surface. Structural evidence of destruction: the input
  list is emptied, and the return type signature cannot represent
  per-utterance embeddings.
- Clustering algorithm: minimal-viable K-means-like iterative
  assignment (SO §3.8 additive-only, no numpy dep). Deterministic
  under PYTHONHASHSEED=0; results are group-level centroids per
  §6.2 P098 verbatim.

Wave-honest limits:
- No LLM invocation. No HTTP call. No filesystem write.
- Case-agnostic; no executive-domain tokens.
- SYNTHETIC fixtures only per owner HALT-trigger; this module is
  algorithm-only and does not ingest real biometric material.

Sealed carriers UNCHANGED per SO §3.8:
- backend/services/audio_plane_v1/character_register.py (CP-M6-3-1).
- backend/services/audio_plane_v1/leakage_path_harness.py (CP-M6-3-2).
"""
from __future__ import annotations

from typing import List, Sequence, Tuple


def _euclidean_distance_sq(a: Sequence[float], b: Sequence[float]) -> float:
    return sum((x - y) * (x - y) for x, y in zip(a, b))


def _mean_vector(vectors: Sequence[Sequence[float]]) -> Tuple[float, ...]:
    if not vectors:
        raise ValueError(
            "_mean_vector: empty vector list has no centroid. Caller must "
            "ensure at least one embedding per cluster before invoking."
        )
    dim = len(vectors[0])
    sums = [0.0] * dim
    for v in vectors:
        for i, x in enumerate(v):
            sums[i] += x
    n = len(vectors)
    return tuple(s / n for s in sums)


def assign_clusters_destroy_embeddings(
    *,
    utterance_embeddings: List[List[float]],
    n_clusters: int,
    max_iterations: int = 25,
) -> Tuple[Tuple[float, ...], ...]:
    """§6.2 P098 cond-4 clustering + embedding destruction.

    Args:
      utterance_embeddings: MUTABLE list of per-utterance embedding
        vectors. MUST be a list (destruction happens via list.clear()).
        Each inner sequence is a per-utterance embedding vector.
      n_clusters: number of centroid clusters to assign. Must be >=1
        and <= len(utterance_embeddings) (structural precondition;
        callers with fewer utterances than clusters must handle
        upstream).
      max_iterations: max K-means-like iteration bound. Default 25.

    Returns:
      A tuple of group-level centroid tuples. NO per-utterance
      embeddings surface in the return type or shape (§6.2 P098
      verbatim 'centroids, distributions, frequencies').

    Post-condition:
      `utterance_embeddings` is EMPTY after this call. §6.2 P098
      verbatim 'Embeddings used during clustering are destroyed after
      cluster assignment' - destruction is structural / in-place.

    Refusals:
      - Empty input -> ValueError (upstream caller mistake, not a
        leakage-path).
      - n_clusters < 1 or > len(utterance_embeddings) -> ValueError.
    """
    if not utterance_embeddings:
        raise ValueError(
            "assign_clusters_destroy_embeddings: input embeddings list "
            "is empty. §6.2 P098 clustering requires at least one "
            "per-utterance embedding."
        )
    if n_clusters < 1:
        raise ValueError(
            f"assign_clusters_destroy_embeddings: n_clusters must be "
            f">= 1; got {n_clusters}."
        )
    if n_clusters > len(utterance_embeddings):
        raise ValueError(
            f"assign_clusters_destroy_embeddings: n_clusters "
            f"{n_clusters} exceeds len(embeddings) "
            f"{len(utterance_embeddings)}. §6.2 requires at least one "
            f"embedding per cluster."
        )

    dim = len(utterance_embeddings[0])
    for i, emb in enumerate(utterance_embeddings):
        if len(emb) != dim:
            raise ValueError(
                f"assign_clusters_destroy_embeddings: embedding {i} has "
                f"dim {len(emb)}; expected {dim}. All utterance "
                f"embeddings must share dim for centroid computation."
            )

    # Deterministic seed initialisation: pick the first n_clusters
    # embeddings as initial centroids (PYTHONHASHSEED=0 reproducibility).
    centroids: List[List[float]] = [
        list(utterance_embeddings[i]) for i in range(n_clusters)
    ]

    for _iteration in range(max_iterations):
        # Assign each embedding to the nearest centroid.
        buckets: List[List[List[float]]] = [[] for _ in range(n_clusters)]
        for emb in utterance_embeddings:
            best_c = 0
            best_d = _euclidean_distance_sq(emb, centroids[0])
            for c in range(1, n_clusters):
                d = _euclidean_distance_sq(emb, centroids[c])
                if d < best_d:
                    best_d = d
                    best_c = c
            buckets[best_c].append(emb)

        # Recompute centroids from bucket means. Empty buckets keep
        # their previous centroid (avoids ValueError from _mean_vector).
        new_centroids: List[List[float]] = []
        moved = False
        for c in range(n_clusters):
            if buckets[c]:
                new_c = list(_mean_vector(buckets[c]))
            else:
                new_c = list(centroids[c])
            if new_c != centroids[c]:
                moved = True
            new_centroids.append(new_c)

        centroids = new_centroids
        if not moved:
            break

    # §6.2 P098 verbatim: 'Embeddings used during clustering are
    # destroyed after cluster assignment.' Structural destruction:
    # empty the input list in place.
    utterance_embeddings.clear()

    return tuple(tuple(c) for c in centroids)
