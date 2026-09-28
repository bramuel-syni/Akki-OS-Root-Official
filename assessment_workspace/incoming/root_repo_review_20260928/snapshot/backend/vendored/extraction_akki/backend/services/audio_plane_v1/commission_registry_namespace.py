"""M6 · Audio-Plane v1.0 · CP-M6-6-3 · Per-commission registry namespace.

Discharge anchor (verbatim on single un-wrapped line):

- Audio-Plane §12.1 P195 (V121):
      "Per commission, a scoped namespace within the registry holds: the Collection Schema (versioned), collected data points mapped against it — with declared-but-not-yet-collected as first-class state — the strata referenced by the Outcome, and coverage state per stratum. Reads compose with the global registry; writes are namespace-scoped. On close, the namespace is sealed, not deleted: it is the record of what was collected and why, and the next objective's wizard session queries prior schemas and coverage so the second project starts from the first project's map."

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - Namespace-scoped writes; reads compose with the global registry
    (composition happens at query time, not at namespace-write time —
    that's a downstream reader concern beyond this CP's scope).
  - Sealed namespaces are IMMUTABLE queryable records (§12.1 P195
    verbatim: 'sealed, not deleted').
  - Case-agnostic; no executive-domain tokens.
  - Synthetic-fixtures-only in tests.
  - §3.1 P038 tokens-not-waveforms discipline preserved.

Contract:

    NAMESPACE_STATE_VALUES = frozenset({"open", "sealed"}).

    COLUMN_COLLECTION_STATE_VALUES = frozenset({
        "declared_not_yet_collected", "collected",
    }).

    NamespaceColumnEntry — frozen 3-carrier: column_ref ·
      collection_state · coverage_metric.

    NamespaceStratumCoverageEntry — frozen 2-carrier: stratum_id ·
      coverage_state.

    CommissionRegistryNamespace — frozen 6-carrier: commission_id ·
      state · collection_schema_versioned_ref · column_entries ·
      stratum_coverage_entries · sealed_at_utc.

    open_namespace(*, commission_id, collection_schema_versioned_ref)
        -> CommissionRegistryNamespace
      Constructs a namespace in state='open' with empty entries.

    record_declared_column(*, namespace, column_ref)
        -> CommissionRegistryNamespace
      Appends a NamespaceColumnEntry with
      state='declared_not_yet_collected' and coverage_metric=None.
      Refuses `NamespaceSealedError` on sealed namespace.

    record_column_collected(*, namespace, column_ref, coverage_metric)
        -> CommissionRegistryNamespace
      Flips the entry to state='collected' with the coverage_metric.
      Refuses `NamespaceColumnUnknownError` on unknown column_ref.
      Refuses `NamespaceSealedError` on sealed namespace.

    seal_namespace(*, namespace, sealed_at_utc)
        -> CommissionRegistryNamespace
      Flips state to 'sealed' and records sealed_at_utc.
      Refuses `NamespaceAlreadySealedError` on already-sealed namespace.
      Preserves column_entries and stratum_coverage_entries (§12.1
      P195 verbatim 'sealed, not deleted').

Refusals:
    NamespaceSealedError · NamespaceAlreadySealedError ·
    NamespaceColumnUnknownError.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import FrozenSet, Optional, Tuple


NAMESPACE_STATE_VALUES: FrozenSet[str] = frozenset({"open", "sealed"})
"""§12.1 P195 verbatim: 'On close, the namespace is sealed, not
deleted.'  Two-state discipline: open (writes allowed) or sealed
(writes refused; reads preserved)."""


COLUMN_COLLECTION_STATE_VALUES: FrozenSet[str] = frozenset({
    "declared_not_yet_collected",
    "collected",
})
"""§12.1 P195 verbatim: 'collected data points mapped against it —
with declared-but-not-yet-collected as first-class state.'"""


class NamespaceSealedError(Exception):
    """Raised when a write is attempted on a sealed namespace.

    §12.1 P195 verbatim: 'On close, the namespace is sealed, not
    deleted'.  Sealed namespaces refuse further writes; reads remain
    available (queryable by next-objective wizard session)."""


class NamespaceAlreadySealedError(Exception):
    """Raised when `seal_namespace` is invoked on an already-sealed
    namespace.  Sealing is a one-shot state transition (open → sealed)."""


class NamespaceColumnUnknownError(Exception):
    """Raised when `record_column_collected` is invoked on a
    column_ref that was never declared via `record_declared_column`.

    §12.1 P195 verbatim: 'declared-but-not-yet-collected as
    first-class state' — a column must be declared before it can be
    marked collected."""


@dataclass(frozen=True)
class NamespaceColumnEntry:
    """A single column entry within the per-commission registry
    namespace.

    Three carriers:
      - `column_ref` — reference to the column in the Collection
        Schema.
      - `collection_state` — one of `COLUMN_COLLECTION_STATE_VALUES`.
      - `coverage_metric` — Optional[float].  None when
        collection_state='declared_not_yet_collected'; concrete when
        collection_state='collected'.
    """

    column_ref: str
    collection_state: str
    coverage_metric: Optional[float]


@dataclass(frozen=True)
class NamespaceStratumCoverageEntry:
    """Coverage state for a single stratum referenced by the Outcome.

    Two carriers:
      - `stratum_id` — reference to the register stratum.
      - `coverage_state` — free-form label for the current coverage
        state (concrete taxonomy is a downstream CP concern).
    """

    stratum_id: str
    coverage_state: str


@dataclass(frozen=True)
class CommissionRegistryNamespace:
    """The per-commission scoped registry namespace.

    Six carriers per §12.1 P195 verbatim:
      - `commission_id` — the commission this namespace binds to.
      - `state` — one of `NAMESPACE_STATE_VALUES` (open / sealed).
      - `collection_schema_versioned_ref` — reference to the versioned
        Collection Schema (§9).
      - `column_entries` — immutable tuple of `NamespaceColumnEntry`.
      - `stratum_coverage_entries` — immutable tuple of
        `NamespaceStratumCoverageEntry`.
      - `sealed_at_utc` — Optional[str] (ISO-8601 UTC).  None when
        state='open'; concrete when state='sealed'.
    """

    commission_id: str
    state: str
    collection_schema_versioned_ref: str
    column_entries: Tuple[NamespaceColumnEntry, ...]
    stratum_coverage_entries: Tuple[NamespaceStratumCoverageEntry, ...]
    sealed_at_utc: Optional[str]


def open_namespace(
    *,
    commission_id: str,
    collection_schema_versioned_ref: str,
) -> CommissionRegistryNamespace:
    """Construct a per-commission registry namespace in state='open'
    with empty entries.

    §12.1 P195 verbatim: 'Per commission, a scoped namespace within
    the registry holds: the Collection Schema (versioned)...'.
    """
    return CommissionRegistryNamespace(
        commission_id=commission_id,
        state="open",
        collection_schema_versioned_ref=collection_schema_versioned_ref,
        column_entries=(),
        stratum_coverage_entries=(),
        sealed_at_utc=None,
    )


def record_declared_column(
    *,
    namespace: CommissionRegistryNamespace,
    column_ref: str,
) -> CommissionRegistryNamespace:
    """Append a `NamespaceColumnEntry` with
    collection_state='declared_not_yet_collected' and
    coverage_metric=None.

    Refuses `NamespaceSealedError` on sealed namespace.
    """
    if namespace.state == "sealed":
        raise NamespaceSealedError(
            f"record_declared_column: namespace "
            f"{namespace.commission_id!r} is sealed; §12.1 P195 "
            f"verbatim: 'On close, the namespace is sealed, not "
            f"deleted' — further writes refused."
        )
    new_entry = NamespaceColumnEntry(
        column_ref=column_ref,
        collection_state="declared_not_yet_collected",
        coverage_metric=None,
    )
    return replace(
        namespace,
        column_entries=namespace.column_entries + (new_entry,),
    )


def record_column_collected(
    *,
    namespace: CommissionRegistryNamespace,
    column_ref: str,
    coverage_metric: float,
) -> CommissionRegistryNamespace:
    """Flip the entry with matching column_ref to
    collection_state='collected' with the provided coverage_metric.

    Refuses:
      - `NamespaceSealedError` on sealed namespace.
      - `NamespaceColumnUnknownError` on unknown column_ref.
    """
    if namespace.state == "sealed":
        raise NamespaceSealedError(
            f"record_column_collected: namespace "
            f"{namespace.commission_id!r} is sealed; §12.1 P195 "
            f"verbatim: 'On close, the namespace is sealed, not "
            f"deleted' — further writes refused."
        )
    matched = False
    new_entries = []
    for entry in namespace.column_entries:
        if entry.column_ref == column_ref:
            matched = True
            new_entries.append(replace(
                entry,
                collection_state="collected",
                coverage_metric=coverage_metric,
            ))
        else:
            new_entries.append(entry)
    if not matched:
        raise NamespaceColumnUnknownError(
            f"record_column_collected: column_ref {column_ref!r} not "
            f"declared in namespace {namespace.commission_id!r}; "
            f"§12.1 P195 verbatim discipline requires declared-but-"
            f"not-yet-collected as first-class state — declare via "
            f"record_declared_column before marking collected."
        )
    return replace(namespace, column_entries=tuple(new_entries))


def seal_namespace(
    *,
    namespace: CommissionRegistryNamespace,
    sealed_at_utc: str,
) -> CommissionRegistryNamespace:
    """Flip the namespace state to 'sealed' and record sealed_at_utc.

    Refuses `NamespaceAlreadySealedError` on already-sealed namespace.

    Preserves column_entries and stratum_coverage_entries (§12.1
    P195 verbatim: 'sealed, not deleted').  The sealed namespace
    remains queryable by the next objective's wizard session per
    §12.1 P195 verbatim: 'the next objective's wizard session queries
    prior schemas and coverage so the second project starts from the
    first project's map.'
    """
    if namespace.state == "sealed":
        raise NamespaceAlreadySealedError(
            f"seal_namespace: namespace "
            f"{namespace.commission_id!r} is already sealed at "
            f"{namespace.sealed_at_utc!r}; sealing is a one-shot "
            f"state transition (open \u2192 sealed)."
        )
    return replace(
        namespace,
        state="sealed",
        sealed_at_utc=sealed_at_utc,
    )
