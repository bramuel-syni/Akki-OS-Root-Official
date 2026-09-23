# CP-AIP-5-CLUSTERING · objective card · 2026-02-23T05:05:00Z

**Spec anchor:** AIP v1.0 §5.3 · Build Sequence #5.

**Status:** ⚪ **QUEUED** (opens after CP-AIP-4 completes).

## Rationale for position (spec §15 verbatim)

> *"Requires 1–4."*

## Scope

Unsupervised clustering over the character stream (§5.3) yields candidate strata.

- **A cluster asserts that a distinct variant exists** — NOT what it is called.
- **Naming and validation** are human work applied to a sample, commissioned like any other qualified work with quoted cost.
- Clustering populates the four Character Register layers (§5.2): Phonetic, Prosodic, Condition, Code-switch.

## §16.2 open decision (banked as PENDING-OWNER-CONFIRMATION)

**Cluster naming validation** — commissioned internally (working default per owner approval 2026-02-23T04:15Z) OR delegated to external evaluation partner where one exists (§5.3).

## Custody invariant tie-in (§6.3 four leakage-path tests)

Clustering path MUST:

- Destroy per-utterance speaker embeddings after cluster assignment (§6.2 condition 4).
- Refuse clusters with fewer than N distinct speakers (§6.2 condition 2).
- Refuse cluster naming that reaches a single person (§6.2 condition 3 · narrowing combination).

## Acceptance criteria (become RED-first pytest invariants)

1. Cluster-count invariant: N speakers minimum per §6.2 condition 2.
2. Embedding-destruction invariant: post-cluster embeddings zeroed/discarded.
3. Cluster-carries-only-description invariant: no per-utterance identifiers in cluster payload (§6.2 condition 4).
4. Naming-commissioned-not-inferred invariant: cluster payload carries `name=null` until human naming ceremony completes.

## New additive modules (proposed shape)

- `services/character_register/unsupervised_clusterer.py`.
- `services/character_register/cluster_naming_commission.py` — commissioned-job wrapper for naming.
- Test file: `tests/invariants/test_cp_aip_5_clustering_aip_v1_0_section_5_3.py` (≥4 RED-first pins).

## Sealed carriers to NOT edit

- Character Register write path (CP-AIP-3) is a strict caller-only.

## Ledger check

> **Ledger check — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-5-CLUSTERING and nothing else.**

**Additive-only §3.8 · RED-first · 5-commit seal · BASELINE_GUARD.**
