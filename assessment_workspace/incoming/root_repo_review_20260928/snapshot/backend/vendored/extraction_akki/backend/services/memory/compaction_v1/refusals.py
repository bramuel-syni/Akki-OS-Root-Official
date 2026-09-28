"""services.memory.compaction_v1.refusals · fail-closed refusal types.

MEM-7 (reload) and MEM-6 (ledger-row-precedes-artefact-readability)
refusals are the ONLY two failure surfaces the compaction v1 layer
raises at the reload boundary.  Both are fail-closed: caller receives
an exception, NEVER best-effort bytes.

Refusal-message discipline: counts-only.  NO leaked identifiers
(matches M9 preventive-charter shape + M11-W1 CrossTenantAccessRefused
counts-only reason string).
"""
from __future__ import annotations


class MemoryReloadRefusalError(Exception):
    """MEM-7 · MEM-R-016 · reload hash-verify or fail closed.

    Raised by services.memory.compaction_v1.reload when the artefact
    bytes on storage do not verify against the expected hash carried
    on the caller-supplied CompactionArtefactRef.

    Refusal-code (bare string constant per SO §3.10 Option alpha ·
    no enum.Enum subclass · matches M11-W1 AKKI_DATA_001 pattern):
    """

    code: str = "AKKI-MEM-COMPACT-001"


class MemoryLedgerRowMissingRefusalError(Exception):
    """MEM-6 · MEM-R-012 + MEM-R-013 · ledger row BEFORE artefact readable.

    Raised by services.memory.compaction_v1.reload when the ledger row
    for the artefact_hash is absent from storage (partial-write path or
    row-write failure that did NOT abort the compaction properly).
    """

    code: str = "AKKI-MEM-COMPACT-002"


__all__: tuple[str, ...] = (
    "MemoryReloadRefusalError",
    "MemoryLedgerRowMissingRefusalError",
)
