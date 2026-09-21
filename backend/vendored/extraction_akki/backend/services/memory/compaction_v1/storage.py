"""services.memory.compaction_v1.storage · in-memory compaction storage.

Enforces MEM-R-012 + MEM-R-013 at the storage boundary:
  - ledger row is written FIRST (write_ledger_row) then artefact bytes
    (write_artefact_bytes) · reader-side check verifies BOTH exist.
  - drop_ledger_row() simulates the MEM-R-013 partial-write failure
    mode for test 7.
  - tamper_artefact_bytes() simulates the MEM-R-016 hash-mismatch mode
    for test 5.

Read boundary (read_artefact_bytes) delegates the hash-verify to
ReloadVerifier per MEM-7 discipline.

MEM-R-050 grep-negative surface is satisfied structurally: the
write_artefact_bytes method REFUSES if no ledger row precedes it.

Ledger row indexing enables MEM-R-019 (erasure_query · MEM-9): a
provenance-ref -> artefact_hash index is maintained on write.

Additive-only per SO §3.8: this is a new in-package storage adapter,
NOT integrated with the sealed M10-W4e services.memory.ledger yet
(that integration lands at the next compaction wave · owner MEMORY GO
ruling: 'compaction rows on the ONE chain' names M10-W4e ledger as
the destination · this v1 in-package storage is the deterministic
test surface + shape validation · integration wave lands post-seal).
"""
from __future__ import annotations

from typing import Optional

from services.memory.compaction_v1.carriers import (
    CompactionArtefactRef,
    CompactionLedgerRow,
)
from services.memory.compaction_v1.refusals import (
    MemoryLedgerRowMissingRefusalError,
    MemoryReloadRefusalError,
)
from services.memory.compaction_v1.verifier import ReloadVerifier


class InMemoryCompactionStorage:
    """Deterministic in-memory storage for compaction v1.

    Enforces MEM-R-012 (ledger row BEFORE artefact readable) +
    MEM-R-013 (row-write failure aborts compaction) at the storage
    boundary structurally: write_artefact_bytes() refuses if no
    ledger row precedes it; read_artefact_bytes() refuses if the
    ledger row is missing at read time.
    """

    __slots__ = (
        "_ledger_rows",
        "_artefact_bytes",
        "_artefact_refs",
        "_provenance_index",
    )

    def __init__(self) -> None:
        # artefact_hash -> CompactionLedgerRow
        self._ledger_rows: dict[str, CompactionLedgerRow] = {}
        # artefact_hash -> bytes
        self._artefact_bytes: dict[str, bytes] = {}
        # artefact_hash -> CompactionArtefactRef (kept for erasure_query O(1))
        self._artefact_refs: dict[str, CompactionArtefactRef] = {}
        # provenance_ref (unit) -> set of artefact_hash citing it
        self._provenance_index: dict[str, set[str]] = {}

    # --- Write path ---------------------------------------------------------

    def write_ledger_row(self, *, row: CompactionLedgerRow) -> None:
        """MEM-R-012 · ledger row FIRST · idempotent per artefact_hash."""
        self._ledger_rows[row.artefact_hash] = row

    def write_artefact_bytes(
        self, *, artefact_hash: str, artefact_bytes: bytes
    ) -> None:
        """MEM-R-012 · REFUSES if no ledger row precedes.

        Structural enforcement of ledger-row-precedes-artefact-readability.
        """
        if artefact_hash not in self._ledger_rows:
            raise MemoryLedgerRowMissingRefusalError(
                f"AKKI-MEM-COMPACT-002: artefact write refused - ledger row "
                f"absent (MEM-R-013 · counts-only: 1)"
            )
        self._artefact_bytes[artefact_hash] = artefact_bytes

    def register_artefact_ref(
        self, *, artefact_ref: CompactionArtefactRef
    ) -> None:
        """Register the artefact_ref for erasure_query indexing.

        MEM-9 · MEM-R-019 · builds the provenance-ref -> artefact_hash
        index used by erasure_query.
        """
        h = artefact_ref.artefact_hash
        self._artefact_refs[h] = artefact_ref
        for pref in artefact_ref.provenance_refs:
            self._provenance_index.setdefault(pref, set()).add(h)

    # --- Read path ----------------------------------------------------------

    def read_ledger_row(
        self, *, artefact_hash: str
    ) -> Optional[CompactionLedgerRow]:
        """Return the ledger row or None if absent."""
        return self._ledger_rows.get(artefact_hash)

    def read_artefact_bytes(
        self, *, artefact_hash: str, verifier: ReloadVerifier
    ) -> bytes:
        """MEM-7 · MEM-R-015 + MEM-R-016 · hash-verify or fail closed.

        Also enforces MEM-R-050 (ledger row present) at read time.
        """
        if artefact_hash not in self._ledger_rows:
            raise MemoryLedgerRowMissingRefusalError(
                f"AKKI-MEM-COMPACT-002: artefact read refused - ledger row "
                f"absent (MEM-R-050 · counts-only: 1)"
            )
        if artefact_hash not in self._artefact_bytes:
            raise MemoryLedgerRowMissingRefusalError(
                f"AKKI-MEM-COMPACT-002: artefact read refused - artefact "
                f"bytes absent under a ledger row (partial-write recovery · "
                f"counts-only: 1)"
            )
        payload = self._artefact_bytes[artefact_hash]
        if not verifier.verify(
            bytes_payload=payload, expected_hash=artefact_hash
        ):
            raise MemoryReloadRefusalError(
                f"AKKI-MEM-COMPACT-001: reload refused - hash verify failed "
                f"(MEM-R-016 · counts-only: 1)"
            )
        return payload

    def iter_artefact_refs_citing(
        self, *, unit_ref: str
    ) -> tuple[CompactionArtefactRef, ...]:
        """MEM-9 · MEM-R-019 · return all artefact refs citing unit_ref.

        Deterministic ordering (sorted by artefact_hash for reproducibility).
        """
        hashes = self._provenance_index.get(unit_ref, set())
        return tuple(
            self._artefact_refs[h] for h in sorted(hashes)
        )

    # --- Test-support surface (documented failure modes) --------------------

    def tamper_artefact_bytes(
        self, *, artefact_hash: str, new_bytes: bytes
    ) -> None:
        """Test hook · simulates MEM-R-016 mode (artefact bytes tampered
        on storage after write · hash-verify SHOULD refuse at read).

        Present as an explicit test-support surface, NOT a production
        code path.  Consumers outside tests SHOULD NOT call this.
        """
        # Note: bypasses the ledger-row check because the ledger row
        # exists from the initial write; this simulates on-disk tamper
        # only, not a ledger-row-absent state.
        self._artefact_bytes[artefact_hash] = new_bytes

    def drop_ledger_row(self, *, artefact_hash: str) -> None:
        """Test hook · simulates MEM-R-013 mode (row-write failure OR
        row deletion between write and read · reload SHOULD refuse
        with MemoryLedgerRowMissingRefusalError).
        """
        self._ledger_rows.pop(artefact_hash, None)


__all__: tuple[str, ...] = ("InMemoryCompactionStorage",)
