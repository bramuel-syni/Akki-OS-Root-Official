"""services.memory.compaction_v1.operations · compact/reload/erasure_query
entrypoints.

compact()      · MEM-R-011 · returns (CompactionArtefactRef, CompactionLedgerRow).
reload()       · MEM-7 · MEM-R-015 · MEM-R-016 · hash-verify or fail closed.
erasure_query() · MEM-9 · MEM-R-019 · DAP-38 mechanism.

Canon anchors verbatim:
  * MEM-2 (Doc 4 A2; A5.5; C.19 I-2) · compacted artefact is derived ·
    fact class NEVER paraphrased · pointer-by-hash or drop.
  * MEM-5 (DAP-37 new-hash precedent) · NEW artefact hash + lineage.
  * MEM-6 (B.4 · DAP-29) · ledger row BEFORE artefact readable.
  * MEM-R-014 · loss statement counts-by-class · 8-class taxonomy.
  * MEM-R-051 (grep-negative surface) · no re-summarisation on read.
  * MEM-R-052 (grep-negative surface) · no compaction of Ledger,
    receipts, provenance, reasoning audit log (out-of-scope for THIS
    layer · enforced upstream by callers · MEM-1 boundary).
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

from services.memory.compaction_v1.carriers import (
    _ALLOWED_CLASSES,
    Claim,
    ClassAnchor,
    CompactionArtefactRef,
    CompactionLedgerRow,
    RunScopedContext,
)
from services.memory.compaction_v1.refusals import (
    MemoryLedgerRowMissingRefusalError,
    MemoryReloadRefusalError,
)
from services.memory.compaction_v1.retention import (
    DraftingComponent,
    RetentionEngine,
)
from services.memory.compaction_v1.storage import InMemoryCompactionStorage
from services.memory.compaction_v1.verifier import ReloadVerifier


# Fact-class + receipt_ref-class carry NO text on the artefact body
# (pointer-only per MEM-R-005 + MEM-R-004).  All other classes carry
# verbatim text in v1 default (no summarisation).
_POINTER_ONLY_CLASSES: frozenset[str] = frozenset({"fact", "receipt_ref"})


def _canonical_artefact_body(
    *, key: str, retained: tuple[Claim, ...]
) -> bytes:
    """Deterministic canonicalisation of a compaction artefact body.

    JSON with sorted keys, no whitespace.  Fact-class + receipt_ref
    entries carry {class, provenance_ref, text_hash} ONLY (pointer-only
    per MEM-R-004 + MEM-R-005 + MEM-R-049 hard ban).  All other
    classes carry {class, provenance_ref, text_hash, text} verbatim
    (v1 default: no summarisation · MEM-R-009 permits summarise on
    inference/utterance ONLY but v1 rule set keeps them verbatim per
    MEMORY GO DEFAULT-class).
    """
    entries: list[dict[str, str]] = []
    for c in retained:
        if c.class_ in _POINTER_ONLY_CLASSES:
            entries.append(
                {
                    "class": c.class_,
                    "provenance_ref": c.provenance_ref,
                    "text_hash": c.text_hash,
                }
            )
        else:
            entries.append(
                {
                    "class": c.class_,
                    "provenance_ref": c.provenance_ref,
                    "text_hash": c.text_hash,
                    "text": c.text,
                }
            )
    body = {
        "schema_version": 1,
        "key": key,
        "entries": entries,
    }
    return json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _canonical_source_version_hash(*, ctx: RunScopedContext) -> str:
    """MEM-R-011 · deterministic source-version hash of the run-scoped
    context (used for lineage + idempotency per MEM-R-027)."""
    payload = {
        "key": ctx.key,
        "claims": [
            {
                "class": c.class_,
                "provenance_ref": c.provenance_ref,
                "text_hash": c.text_hash,
            }
            for c in ctx.claims
        ],
    }
    b = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(b).hexdigest()


def _artefact_class(*, retained: tuple[Claim, ...]) -> str:
    """MEM-2 · artefact class is 'inference' or 'utterance' · NEVER 'fact'.

    Default: 'inference'.  Upgrades to 'utterance' if any utterance
    claim is retained AND no non-utterance verbatim claim is present.
    In v1 default (keep-all), class is deterministically 'inference'
    (matches MEM-2 default derived class).
    """
    _ = retained  # unused in v1 · placeholder for future class-derivation
    return "inference"


def compact(
    *,
    ctx: RunScopedContext,
    engine: RetentionEngine,
    drafting: DraftingComponent,
    storage: InMemoryCompactionStorage,
) -> tuple[CompactionArtefactRef, CompactionLedgerRow]:
    """MEM-R-011 · compact a run-scoped context.

    Returns (CompactionArtefactRef, CompactionLedgerRow).  Ledger row
    is written to storage BEFORE the artefact bytes (MEM-R-012 · MEM-R-013).

    Idempotent per (key, source_version_hash) per MEM-R-027.
    """
    # DraftingComponent is present as an interface point per MEM-2 /
    # MEM-3 role separation but is NOT invoked in v1 default path
    # (MEM-R-009 permits summarise on inference/utterance ONLY; v1
    # rule set keeps them verbatim).  Reference-only assignment here
    # documents the dependency without invoking learned surface.
    _ = drafting

    retained, dropped = engine.decide(ctx=ctx)

    # Loss statement counts-by-class (MEM-R-014) · deterministic.
    loss_statement: dict[str, int] = {cls: 0 for cls in _ALLOWED_CLASSES}
    for d in dropped:
        loss_statement[d.class_] = loss_statement.get(d.class_, 0) + 1
    total_drops = sum(loss_statement.values())

    # Deterministic artefact body + hash.
    artefact_body = _canonical_artefact_body(key=ctx.key, retained=retained)
    artefact_hash = hashlib.sha256(artefact_body).hexdigest()

    # Class anchors (MEM-R-005 · pointer-by-hash for ALL retained claims).
    class_anchors = engine.build_class_anchors(claims=retained)

    # Provenance refs superset (MEM-R-002 · SUPERSET rule).
    provenance_refs = tuple(c.provenance_ref for c in retained)

    # Source version hash (MEM-R-011 · lineage).
    source_version_hash = _canonical_source_version_hash(ctx=ctx)

    artefact_ref = CompactionArtefactRef(
        artefact_hash=artefact_hash,
        key=ctx.key,
        lineage_key=ctx.key,
        source_version_hashes=(source_version_hash,),
        provenance_refs=provenance_refs,
        class_anchors=class_anchors,
        class_=_artefact_class(retained=retained),
    )

    ledger_row = CompactionLedgerRow(
        source_key=ctx.key,
        source_version_hashes=(source_version_hash,),
        retention_rule_set_version=engine.rule_set_version.version,
        artefact_hash=artefact_hash,
        loss_statement=loss_statement,
        total_drops=total_drops,
        written_at_utc=datetime.now(timezone.utc).isoformat(),
    )

    # MEM-R-012 · ledger row FIRST · then artefact bytes · then index.
    storage.write_ledger_row(row=ledger_row)
    storage.write_artefact_bytes(
        artefact_hash=artefact_hash, artefact_bytes=artefact_body,
    )
    storage.register_artefact_ref(artefact_ref=artefact_ref)

    return artefact_ref, ledger_row


def reload(
    *,
    artefact_ref: CompactionArtefactRef,
    verifier: ReloadVerifier,
    storage: InMemoryCompactionStorage,
) -> bytes:
    """MEM-7 · MEM-R-015 + MEM-R-016 · hash-verify or fail closed.

    Delegates to storage.read_artefact_bytes which enforces:
      - ledger row present (MEM-R-050 · MemoryLedgerRowMissingRefusalError)
      - hash-verify or refuse (MEM-R-016 · MemoryReloadRefusalError)

    Returns raw stored bytes byte-identical across calls (MEM-R-015 ·
    NO re-summarisation on read · MEM-R-051 grep-negative surface
    satisfied structurally).
    """
    return storage.read_artefact_bytes(
        artefact_hash=artefact_ref.artefact_hash, verifier=verifier,
    )


def erasure_query(
    *, unit: str, storage: InMemoryCompactionStorage
) -> tuple[CompactionArtefactRef, ...]:
    """MEM-9 · MEM-R-019 · DAP-38 mechanism · deterministic.

    Returns all artefact refs whose provenance_refs cite `unit`.
    Deterministic order (sorted by artefact_hash).  Kenya DPA 2019
    s.40 breach class if this returns an incomplete set.
    """
    return storage.iter_artefact_refs_citing(unit_ref=unit)


__all__: tuple[str, ...] = (
    "MemoryLedgerRowMissingRefusalError",
    "MemoryReloadRefusalError",
    "compact",
    "reload",
    "erasure_query",
)
