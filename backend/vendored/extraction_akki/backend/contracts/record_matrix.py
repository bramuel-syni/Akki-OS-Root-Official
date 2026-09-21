"""Record Matrix (thin kernel) — Canon 9 §6-§18, Build Order 01 §4.A0.

Thin scope: only the record classes the live path touches. Full scope
completes in Track B per WS-BUILD-RECORD-MATRIX. Six thin-kernel classes:

    Ledger.Row              — Northena append-only ledger row.
    Receipt                 — trust receipts on outbound calls.
    Census.Snapshot         — Canon 5 §12 census-chip data snapshot.
    Actor.Declaration       — Canon 3 §6 declaration seat.
    Ingestion.Artifact      — data-source ingestion output (A2).
    Training.Artifact       — GPU training run output (A3).

Each entry lists the sole writer service + the reader-list. AST discipline
(a companion test) enforces exclusivity: no writer outside the matrix seat.
"""
from __future__ import annotations

from typing import Dict, FrozenSet, List, NamedTuple


class MatrixEntry(NamedTuple):
    record_class: str
    writer: str            # module path of the sole writer
    readers: FrozenSet[str]  # module paths / surfaces authorized to read
    contract_module: str   # contracts.<name> for the frozen shape
    contract_version: str  # e.g. "v0"


# THIN KERNEL — Build Order 01 §4.A0.
# Full-scope Track-B expansions land later; edits require Canon 3 §24
# rule-change ceremony against BUILD_STRATEGY.md.
THIN_KERNEL: Dict[str, MatrixEntry] = {
    "Ledger.Row": MatrixEntry(
        record_class="Ledger.Row",
        writer="services.northena.ledger",
        readers=frozenset({
            "routers.northena",
            "services.checker",
            "services.northena.prove_one_run",  # future Wave-9
        }),
        contract_module="contracts.northena_ledger",
        contract_version="v0",
    ),
    "Receipt": MatrixEntry(
        record_class="Receipt",
        writer="services.outer_gate",
        readers=frozenset({
            "routers.northena",
            "services.checker",
        }),
        contract_module="contracts.outer_gate_receipt",
        contract_version="v0",
    ),
    "Census.Snapshot": MatrixEntry(
        record_class="Census.Snapshot",
        writer="services.census_dimensions",
        readers=frozenset({
            "routers.registry",
            "routers.northena",
        }),
        contract_module="contracts.five_rings",  # census renders via five_rings
        contract_version="v0",
    ),
    "Actor.Declaration": MatrixEntry(
        record_class="Actor.Declaration",
        writer="services.declaration.seat",
        readers=frozenset({
            "services.northena.admit",
            "routers.northena",
            "services.checker",
        }),
        contract_module="contracts.actor_declaration",
        contract_version="v0",
    ),
    "Ingestion.Artifact": MatrixEntry(
        record_class="Ingestion.Artifact",
        writer="services.data_source.ingest",
        readers=frozenset({
            "services.northena.admit",
            "services.mtafiti",
            "routers.registry",
        }),
        contract_module="contracts.knowledge_artifact_v0",
        contract_version="v0",
    ),
    "Training.Artifact": MatrixEntry(
        record_class="Training.Artifact",
        writer="services.compute.training",
        readers=frozenset({
            "routers.registry",
            "services.mtafiti",
        }),
        contract_module="contracts.knowledge_artifact_v0",
        contract_version="v0",
    ),
}


def writer_for(record_class: str) -> str:
    """Return the sole writer's module path for `record_class`."""
    entry = THIN_KERNEL.get(record_class)
    if entry is None:
        raise KeyError(f"record_class {record_class!r} not in thin kernel")
    return entry.writer


def readers_for(record_class: str) -> FrozenSet[str]:
    entry = THIN_KERNEL.get(record_class)
    if entry is None:
        raise KeyError(f"record_class {record_class!r} not in thin kernel")
    return entry.readers


def is_writer_authorized(record_class: str, caller_module: str) -> bool:
    """True iff `caller_module` is the sole writer for `record_class`."""
    entry = THIN_KERNEL.get(record_class)
    if entry is None:
        return False
    return caller_module == entry.writer


def is_reader_authorized(record_class: str, caller_module: str) -> bool:
    entry = THIN_KERNEL.get(record_class)
    if entry is None:
        return False
    return caller_module in entry.readers or caller_module == entry.writer


def thin_kernel_classes() -> List[str]:
    return list(THIN_KERNEL.keys())
