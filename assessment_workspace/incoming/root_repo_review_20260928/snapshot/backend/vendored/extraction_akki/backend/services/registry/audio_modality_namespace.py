"""CP-AIP-6-OBJECTIVE-WIZARD · audio_modality_namespace · §12.1 registry namespace scoping.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-6-OBJECTIVE-WIZARD and nothing else.

Spec anchor: AIP v1.0 §12.1 Registry (Mtafiti audio modality).

§12.1 verbatim: 'Per commission, a scoped namespace within the registry
holds: the Collection Schema (versioned), collected data points mapped
against it — with declared-but-not-yet-collected as first-class state
— the strata referenced by the Outcome, and coverage state per stratum.
Reads compose with the global registry; writes are namespace-scoped.
On close, the namespace is sealed, not deleted: it is the record of
what was collected and why, and the next objective's wizard session
queries prior schemas and coverage so the second project starts from
the first project's map.'

Structural discipline (§1.5 unrepresentable-not-policed):
  - `AudioModalityNamespace_v0` HAS NO `delete()` method.
  - `close()` transitions `namespace_state` from `'open'` to `'sealed'`.
  - `namespace_state` can ONLY be `'open'` or `'sealed'` · closed-set.
  - Writes are namespace-scoped · every scoped write carries the
    commission_id.
  - Reads compose with global · scoped-write helper does not touch a
    global writer surface.

Additive-only per SO §3.8.  Sealed services/registry/ carriers are
NOT edited.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final, List, Literal, Tuple


NamespaceState = Literal["open", "sealed"]


@dataclass(frozen=True)
class ScopedWrite_v0:
    """A namespace-scoped write record · every write carries the
    commission_id per §12.1 verbatim 'writes are namespace-scoped'.
    """

    commission_id: str
    column_name: str
    value_ref: str


@dataclass(frozen=True)
class AudioModalityNamespace_v0:
    """§12.1 verbatim per-commission scoped namespace.

    Fields:
      - commission_id · the namespace key.
      - collection_schema_version · versioned schema ref (§12.1).
      - namespace_state · Literal['open', 'sealed'] closed-set (§12.1
        verbatim: 'sealed, not deleted').
      - scoped_writes · append-only tuple of ScopedWrite_v0 records.
    """

    commission_id: str
    collection_schema_version: str
    namespace_state: NamespaceState = "open"
    scoped_writes: Tuple[ScopedWrite_v0, ...] = field(default_factory=tuple)

    @classmethod
    def open(
        cls,
        *,
        commission_id: str,
        collection_schema_version: str,
    ) -> "AudioModalityNamespace_v0":
        """Open a new per-commission namespace in state 'open'."""
        return cls(
            commission_id=commission_id,
            collection_schema_version=collection_schema_version,
            namespace_state="open",
            scoped_writes=(),
        )

    def close(self) -> "AudioModalityNamespace_v0":
        """§12.1 verbatim: 'On close, the namespace is sealed, not
        deleted.'  Returns a new frozen namespace with state 'sealed'.
        """
        if self.namespace_state == "sealed":
            return self  # idempotent close.
        return AudioModalityNamespace_v0(
            commission_id=self.commission_id,
            collection_schema_version=self.collection_schema_version,
            namespace_state="sealed",
            scoped_writes=self.scoped_writes,
        )

    def write_data_point(
        self,
        *,
        column_name: str,
        value_ref: str,
    ) -> "AudioModalityNamespace_v0":
        """§12.1 verbatim: 'writes are namespace-scoped'.  Returns a
        new frozen namespace with the append-only ScopedWrite added."""
        if self.namespace_state == "sealed":
            raise ValueError(
                f"§12.1: cannot write to sealed namespace "
                f"{self.commission_id!r}."
            )
        new_write = ScopedWrite_v0(
            commission_id=self.commission_id,
            column_name=column_name,
            value_ref=value_ref,
        )
        return AudioModalityNamespace_v0(
            commission_id=self.commission_id,
            collection_schema_version=self.collection_schema_version,
            namespace_state=self.namespace_state,
            scoped_writes=self.scoped_writes + (new_write,),
        )

    def list_scoped_writes(self) -> List[ScopedWrite_v0]:
        """Return the append-only scoped writes list · §12.1 verbatim."""
        return list(self.scoped_writes)
