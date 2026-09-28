"""W-G3-REMAINDER · Mtafiti full asset-inventory generalisation.

Closes Doc-0 G-3 remainder (Mtafiti's full asset-inventory extension)
and lifts Doc-0 Component 4 BR-4.1 STATUS from "estate sources only"
to "generalised across the 5 AssetClass kinds already in schema".

Composes OVER `services.mtafiti.asset_registry_writer` (predecessor
wave W-REGISTRY-EXTENSION-G3, commit 33edf56); DOES NOT modify the
predecessor's schema or writer.  Per Canon-1 §4.6 extension-not-sibling
doctrine.

Canon-9 §3 verbatim: 'A second writer to any class is a defect on
sight.'  This module is a READER-ONLY surface.  Silent introduction of
any `write_*`, `append_*`, `update_*`, `delete_*`, `add_*`, `put_*` or
`set_*` public callable would break `test_gs_06_canon_9_single_writer_preserved`.
"""

from __future__ import annotations

from collections import Counter
from typing import Dict, List, Tuple

from contracts.asset_registry import AssetClass, CustodyClass
from services.mtafiti import asset_registry_writer


def _receipt_id_for(record) -> str:
    """Mirror asset_registry_writer._compute_receipt_id so the reader
    surface can report the same receipt_id the writer returned, without
    modifying the writer.  Same record ⇒ same id (idempotency)."""
    return asset_registry_writer._compute_receipt_id(record)


def list_all_assets() -> List[Dict]:
    """BR-4.1 verbatim target: every asset the writer accepted is
    retrievable through this generalised surface — no filter-by-default.

    Returns a list of dicts, each dict is a lightweight projection of a
    stored AssetRegistryRecord (asset_ref, asset_class, custody_class,
    owner_class, receipt_id).  The receipt_id is the same string that
    the canonical writer returned in its WriteReceipt.receipt_id
    (computed deterministically from record content).
    """
    out: List[Dict] = []
    for record in asset_registry_writer._REGISTRY.values():
        out.append({
            "receipt_id": _receipt_id_for(record),
            "asset_ref": record.asset_ref,
            "asset_class": record.asset_class.value,
            "custody_class": record.custody_class.value,
            "owner_class": record.named_owner.owner_class,
        })
    return out


def count_by_class() -> Dict[str, int]:
    """BR-4.1: give a coverage report across every AssetClass kind.
    Returns a dict keyed by AssetClass.value with the record count per
    class.  ALL 5 kinds appear as keys (missing kinds have count 0).
    """
    counter: Counter = Counter()
    for record in asset_registry_writer._REGISTRY.values():
        counter[record.asset_class.value] += 1
    return {c.value: counter.get(c.value, 0) for c in AssetClass}


def enumerate_classes_always_five() -> Tuple[str, ...]:
    """TA-3.1 verbatim: 'A finite, named list ... exists and can be
    produced on request.'  The list has FIVE names — one per
    AssetClass kind — regardless of record count.  Silent flip
    forbidden."""
    return tuple(sorted(c.value for c in AssetClass))


def cross_class_governance_query(
    *,
    custody_class: CustodyClass,
    asset_class: AssetClass,
    owner_class: str,
) -> List[Dict]:
    """BR-4.1 + Canon-3 §22.1: filter the inventory by
    `(custody_class, asset_class, owner_class)`.  Each filter is
    honored independently and their intersection is returned.  Only
    reads — never writes."""
    out: List[Dict] = []
    for record in asset_registry_writer._REGISTRY.values():
        if record.custody_class != custody_class:
            continue
        if record.asset_class != asset_class:
            continue
        if record.named_owner.owner_class != owner_class:
            continue
        out.append({
            "receipt_id": _receipt_id_for(record),
            "asset_ref": record.asset_ref,
            "asset_class": record.asset_class.value,
            "custody_class": record.custody_class.value,
            "owner_class": record.named_owner.owner_class,
        })
    return out


def single_writer_still_holds() -> bool:
    """Canon-9 §3 self-check: this module carries no writer verb on its
    own public surface.  Returns True if the invariant holds.

    Note: The single-writer *fact* is preserved structurally by NOT
    importing/re-exposing any writer symbol from asset_registry_writer
    on the public surface of this module.
    """
    import re
    banned = re.compile(r"^(write|append|update|delete|add|put|set)_")
    for name in globals().keys():
        if name.startswith("_"):
            continue
        if banned.match(name):
            return False
    return True
