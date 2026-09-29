"""services.memory.compaction_v1.chain_integration · W4 · one-chain adapter.

Thin additive adapter that binds compaction persistence to the sealed
M10 chain writer path (`services.compliance.deletion_ledger.emit_
deletion_ledger_row`), preserving the ordering invariant: **the ledger
row lands on the ONE chain BEFORE the compaction artefact becomes
readable**.

Owner MEMORY GO ruling verbatim (banked at STATE/DECISIONS.md
CP-MEMORY-COMPACTION-V1-BUILD-WAVE):
    "compaction rows on the ONE chain"

Owner OPTION 1 ratification 2026-09-19T~20:20Z verbatim:
    "W4 (M10-W4e ledger integration): thin adapter from compaction
     storage to sealed M10 chain writer path services.memory.ledger.
     Preserve ordering invariant: ledger row lands BEFORE compaction
     artifact becomes readable. InMemoryCompactionStorage becomes
     AST-banned from production imports (test-fixture only)."

Owner W4 EMPHASIS 2026-09-19T~21:00Z verbatim (this-session):
    1) "The ordering invariant must prove SEQUENCE, not co-existence
        — a test that observes both the ledger row and the readable
        artifact after the fact proves nothing; author it so a read
        attempted before the ledger write refuses (or the write path
        structurally cannot expose the artifact until the chain
        append returns)."
    2) "The AST ban on InMemoryCompactionStorage from production
        imports should mirror the negative-scan shape you used at
        M12-W1a (import-level + call-site level) — tests/** stays
        allowed."

Owner ruling 2a 2026-07-31 verbatim (banked at services/memory/
ledger.py docstring · authority for the ONE chain doctrine):
    "Reuse NorthenaLedgerRow_v1 with memory_* data_class values.
     Northena owns the one ledger; memory must be ledger-
     reconstructible through the same append-only record, one trace
     thread, no second ledger."

## Structural sequence proof (owner W4 EMPHASIS #1 verbatim)

The ordering invariant is enforced STRUCTURALLY, not by post-hoc
observation:

    ChainGatedReader.read(artefact_hash, verifier) refuses with
    MemoryLedgerRowMissingRefusalError iff no ChainAppendReceipt has
    been recorded for `artefact_hash`.  The receipt is the STRUCTURAL
    KEY the reader uses to look up bytes — absent the receipt, the
    bytes cannot be exposed.  The receipt is minted ONLY inside
    append_compaction_row_to_chain AFTER emit_deletion_ledger_row
    returns (chain-append complete).  Therefore: the write path
    structurally cannot expose the artefact until the chain append
    returns.

The combined helper `append_compaction_row_and_gate` bundles the two
steps into a single async call · if the chain-append raises, the
reader is NEVER touched · the artefact remains unreadable · this is
the strong form of the sequence proof.

## ONE chain routing (MEM-10 + owner ruling 2a verbatim)

`append_compaction_row_to_chain` routes through the sealed
`services.compliance.deletion_ledger.emit_deletion_ledger_row` writer
— the SAME writer sealed M10 `services.memory.ledger` uses for
`emit_plane_issued`, `emit_contribution_landed`, `emit_publication_
event`, `emit_plane_revoked`.  No second ledger.  No second trace
thread.

The data_class value routes to `memory_publication_landed` (an
existing registered memory_* class in `data_class_registry.v4.json`)
with stamp_audit disambiguation (`event_kind="compaction_v1_landed"`
+ full CompactionLedgerRow content preserved in stamp_audit).  A
dedicated `memory_compaction_landed` data_class would require a
sealed registry bump (v5) and is deferred; the semantic overload is
scoped and documented here for the W4 wave.

## Additive-only per SO §3.8

- New module in existing sub-package `services/memory/compaction_v1/`.
- Sealed W1 modules NOT edited: `carriers.py` (import-only) ·
  `refusals.py` (import-only · reuses MemoryLedgerRowMissingRefusal-
  Error) · `verifier.py` (import-only · reuses ReloadVerifier) ·
  `storage.py` (NOT touched · InMemoryCompactionStorage is now
  AST-banned from production imports by W4.5+W4.6 · this module does
  NOT import it) · `retention.py` (not touched) · `operations.py`
  (not touched · sealed W1 pre-integration scaffold retains its
  InMemoryCompactionStorage dependence per grandfathered exemption).
- Sealed M10 `services/memory/ledger.py` NOT edited.
- Sealed `services/compliance/deletion_ledger.py` NOT edited.
- Sealed `services/compliance/data_class_registry.v4.json` NOT edited
  (semantic overload of memory_publication_landed used instead of a
  registry bump).

## Canon anchors

- MEM-6 [B.4 · DAP-29] · ledger row BEFORE artefact readable
  (chain-level restatement).
- MEM-10 [C.13 · I-1] · compaction rows on the ONE chain.
- MEM-R-012 · MEM-R-013 · ledger-row-precedes-artefact-readability +
  row-write-failure-aborts-compaction (both lifted to chain level).
- MEM-R-050 (grep-negative surface) · no compaction without ledger
  row first · structurally satisfied by ChainGatedReader refusal.
- Canon 3 §13 · SyniSense · the ONE ledger doctrine.
- Canon 8 §W11 · structural role separation · this module carries
  ONLY thin binding (frozen receipt + async emitter + gated reader);
  determinism preserved · learned surface absent.
- SO §3.8 · thin-kernel additive-only · sealed modules NOT edited.
- SO §6.4 · NOTHING-BEYOND · scope frozen at four surfaces
  (ChainAppendReceipt + append_compaction_row_to_chain +
  ChainGatedReader + append_compaction_row_and_gate).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Final

from pydantic import BaseModel, ConfigDict, Field

from contracts.northena_ledger import LedgerArtifactRef
from services.compliance.deletion_ledger import emit_deletion_ledger_row
from services.memory.compaction_v1.carriers import CompactionLedgerRow
from services.memory.compaction_v1.refusals import (
    MemoryLedgerRowMissingRefusalError,
    MemoryReloadRefusalError,
)
from services.memory.compaction_v1.verifier import ReloadVerifier


# ---------------------------------------------------------------------------
# Data class value used to route compaction rows through the ONE chain.
# Existing registered memory_* value in data_class_registry.v4.json ·
# stamp_audit["event_kind"] carries the fine-grained compaction event kind.
# ---------------------------------------------------------------------------

_CHAIN_DATA_CLASS: Final[str] = "memory_publication_landed"
_CHAIN_HELD_CLASS: Final[str] = "memory_publication"
_CHAIN_EVENT_KIND: Final[str] = "compaction_v1_landed"
_CHAIN_RETENTION_RULE_REF: Final[str] = "memory:compaction_v1_lifecycle"
_CHAIN_LAWFUL_BASIS_REF: Final[str] = "memory:compaction_v1_landed"


# ---------------------------------------------------------------------------
# ChainAppendReceipt · frozen carrier · minted only after chain-append returns.
# ---------------------------------------------------------------------------


class ChainAppendReceipt(BaseModel):
    """Frozen receipt witnessing that a compaction ledger row has been
    appended to the ONE chain (Northena append-only ledger via
    `emit_deletion_ledger_row`).

    Only instances of this class permit the corresponding artefact
    bytes to be exposed by ChainGatedReader.read(...).  The receipt
    is minted at exactly one point: inside
    `append_compaction_row_to_chain` AFTER the awaited chain writer
    returns.  Therefore: no receipt exists until chain-append is
    complete; no bytes are exposable until a receipt exists.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    artefact_hash: str = Field(min_length=64, max_length=64)
    chain_row_id: str = Field(min_length=1)
    chain_appended_at_utc: str = Field(min_length=1)


# ---------------------------------------------------------------------------
# ChainGatedReader · read surface · structural gate keyed by ChainAppendReceipt.
# ---------------------------------------------------------------------------


class ChainGatedReader:
    """Reader that exposes compaction artefact bytes ONLY for
    artefact_hashes whose ChainAppendReceipt has been recorded.

    The structural gate is a receipt-keyed lookup: absent a receipt
    for `artefact_hash`, read() refuses with
    MemoryLedgerRowMissingRefusalError · no fallback path · no
    "co-existence" observation window · the receipt IS the sequence
    proof.

    Not an InMemoryCompactionStorage.  Does not implement that
    class's write/query surface.  Does not import
    InMemoryCompactionStorage (W4.5/W4.6 AST bans hold).
    """

    __slots__ = ("_receipts", "_bytes")

    def __init__(self) -> None:
        # artefact_hash -> ChainAppendReceipt (structural gate key)
        self._receipts: Dict[str, ChainAppendReceipt] = {}
        # artefact_hash -> raw stored bytes (byte-identical MEM-R-015)
        self._bytes: Dict[str, bytes] = {}

    def record_appended(
        self, *, receipt: ChainAppendReceipt, artefact_bytes: bytes
    ) -> None:
        """Record a chain-appended receipt + its corresponding bytes.

        Called only from inside `append_compaction_row_and_gate`
        AFTER the chain writer returns.  Callers outside this module
        SHOULD only ever call this via the async helper — direct
        calls are permitted for test-fixture composition but are
        semantically equivalent to a test seam.
        """
        h = receipt.artefact_hash
        self._receipts[h] = receipt
        self._bytes[h] = artefact_bytes

    def read(
        self, *, artefact_hash: str, verifier: ReloadVerifier
    ) -> bytes:
        """MEM-7 · MEM-R-015 · MEM-R-016 · hash-verify or fail closed.

        Structural gate: refuses with MemoryLedgerRowMissingRefusalError
        if no ChainAppendReceipt has been recorded for `artefact_hash`.
        This is the SEQUENCE proof (owner W4 EMPHASIS #1) — the reader
        has no way to return bytes without the receipt.
        """
        if artefact_hash not in self._receipts:
            raise MemoryLedgerRowMissingRefusalError(
                "AKKI-MEM-COMPACT-W4-001: artefact read refused - "
                "no chain-append receipt for artefact_hash "
                "(structural sequence gate · MEM-R-050 counts-only: 1)"
            )
        if artefact_hash not in self._bytes:
            raise MemoryLedgerRowMissingRefusalError(
                "AKKI-MEM-COMPACT-W4-002: artefact read refused - "
                "receipt present but bytes absent (partial-write "
                "recovery · counts-only: 1)"
            )
        payload = self._bytes[artefact_hash]
        if not verifier.verify(
            bytes_payload=payload, expected_hash=artefact_hash
        ):
            raise MemoryReloadRefusalError(
                "AKKI-MEM-COMPACT-W4-003: reload refused - "
                "hash verify failed (MEM-R-016 counts-only: 1)"
            )
        return payload


# ---------------------------------------------------------------------------
# append_compaction_row_to_chain · awaits the sealed M10 chain writer.
# ---------------------------------------------------------------------------


async def append_compaction_row_to_chain(
    *,
    row: CompactionLedgerRow,
    tenant_id: str,
    actor: str,
    trace_id: str,
) -> ChainAppendReceipt:
    """Append a compaction ledger row to the ONE chain (Northena
    append-only ledger via emit_deletion_ledger_row) and mint a
    ChainAppendReceipt witnessing the append.

    Owner ruling 2a 2026-07-31 verbatim (banked at
    services/memory/ledger.py docstring): "Northena owns the one
    ledger; memory must be ledger-reconstructible through the same
    append-only record, one trace thread, no second ledger."

    The receipt is the STRUCTURAL KEY that
    `ChainGatedReader.read(...)` uses to expose bytes.  The receipt
    is minted here AFTER `emit_deletion_ledger_row` returns —
    therefore: no receipt exists until chain-append is complete.
    """
    stamp_audit_extras = {
        "event_kind": _CHAIN_EVENT_KIND,
        "tenant_id": tenant_id,
        "source_key": row.source_key,
        "source_version_hashes": list(row.source_version_hashes),
        "retention_rule_set_version": row.retention_rule_set_version,
        "artefact_hash": row.artefact_hash,
        "loss_statement": dict(row.loss_statement),
        "total_drops": row.total_drops,
        "compaction_written_at_utc": row.written_at_utc,
    }
    chain_row_id = f"memory-compaction-v1-{row.artefact_hash}"
    await emit_deletion_ledger_row(
        run_id=chain_row_id,
        trace_id=trace_id,
        data_class=_CHAIN_DATA_CLASS,
        held_class=_CHAIN_HELD_CLASS,
        keys_deleted=0,  # honest zero · not a deletion event.
        retention_rule_ref=_CHAIN_RETENTION_RULE_REF,
        actor=actor,
        # The compacted run is the objective the row names; emit_deletion_ledger_row has no default.
        artifact_ref=LedgerArtifactRef(artifact_type="objective_request", artifact_id=row.source_key,
                                       version=row.retention_rule_set_version),
        lawful_basis_ref=_CHAIN_LAWFUL_BASIS_REF,
        extra_stamp_audit=stamp_audit_extras,
    )
    return ChainAppendReceipt(
        artefact_hash=row.artefact_hash,
        chain_row_id=chain_row_id,
        chain_appended_at_utc=datetime.now(timezone.utc).isoformat(),
    )


# ---------------------------------------------------------------------------
# append_compaction_row_and_gate · combined write path · structural gate.
# ---------------------------------------------------------------------------


async def append_compaction_row_and_gate(
    *,
    row: CompactionLedgerRow,
    artefact_bytes: bytes,
    reader: ChainGatedReader,
    tenant_id: str,
    actor: str,
    trace_id: str,
) -> ChainAppendReceipt:
    """Owner W4 EMPHASIS #1 · strong-form sequence proof.

    Awaits chain-append, THEN records the receipt-bound bytes to
    the reader.  If the chain-append raises, the reader is NEVER
    touched · the artefact remains unreadable.  This is the "write
    path structurally cannot expose the artifact until the chain
    append returns" clause of the owner emphasis, made literal.
    """
    receipt = await append_compaction_row_to_chain(
        row=row,
        tenant_id=tenant_id,
        actor=actor,
        trace_id=trace_id,
    )
    reader.record_appended(receipt=receipt, artefact_bytes=artefact_bytes)
    return receipt


__all__: tuple[str, ...] = (
    "ChainAppendReceipt",
    "ChainGatedReader",
    "append_compaction_row_to_chain",
    "append_compaction_row_and_gate",
)
