"""Synisense Shield — tenant entity lookup consumed by the de-identifier (Doc 1 §A5.4 · Doc 2 A5.1 B34, A6 B45).

One entity set per tenant: approved exact declarations in the confidentiality register that carry an `entity_type`. The seed
`tenant_catalogue.v0.json` (P1-R1, owner ruling 2026-07-30) is now a migration source only — `semantic_register._migrate_catalogue`
moves its surface forms into the register as `catalogue_<group>` declarations the first time a tenant's set is read, so the list the DPO
authors and the set the crossing consults can no longer diverge (WP-A1, 2026-10-05).

Contract preserved:
    async def lookup_in_text(text: str, *, tenant_id: str) -> list[dict]
    Each returned dict shape: {"start": int, "end": int, "type": str, "match": str}
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List

_CATALOGUE_PATH = Path(__file__).resolve().parent / "tenant_catalogue.v0.json"

ENTITY_TYPE_MAP = {
    "presenters": "PRESENTER",
    "stations": "STATION",
    "programmes": "PROGRAMME",
    "advertisers": "ADVERTISER",
}


def _load_catalogue() -> Dict[str, Any]:
    if not _CATALOGUE_PATH.exists():
        return {"tenants": {}}
    try:
        return json.loads(_CATALOGUE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"tenants": {}}


def catalogue_groups(tenant_id: str) -> Dict[str, list]:
    """Migration source: the catalogue's entries for one tenant, by group (only groups with a known entity type)."""
    entries = _load_catalogue().get("tenants", {}).get(tenant_id, {})
    return {group: entries.get(group, []) for group in ENTITY_TYPE_MAP if entries.get(group)}


def _scan(text: str, surfaces: List[tuple]) -> List[Dict[str, Any]]:
    text_lower = text.lower()
    hits: List[Dict[str, Any]] = []
    for surface, entity_type in surfaces:
        surface_lower = surface.lower()
        start = 0
        while True:
            idx = text_lower.find(surface_lower, start)
            if idx < 0:
                break
            end = idx + len(surface)
            left_ok = idx == 0 or not text[idx - 1].isalnum()
            right_ok = end == len(text) or not text[end].isalnum()
            if left_ok and right_ok:
                hits.append({"start": idx, "end": end, "type": entity_type, "match": text[idx:end]})
            start = end
    hits.sort(key=lambda h: (h["start"], -(h["end"] - h["start"])))
    deduped: List[Dict[str, Any]] = []
    last_end = -1
    for h in hits:
        if h["start"] >= last_end:
            deduped.append(h)
            last_end = h["end"]
    return deduped


async def lookup_in_text(text: str, *, tenant_id: str) -> List[Dict[str, Any]]:
    """Scan `text` for the tenant's approved entity declarations (case-insensitive, word-bounded, leftmost-longest).

    Isolation: only declarations under `tenant_id` are consulted. A pending or draft declaration is never in this set (B43).
    """
    from services.synisense.shield import semantic_register as reg

    declarations = await asyncio.to_thread(reg.entity_declarations, tenant_id)
    surfaces = [(value, d["entity_type"]) for d in declarations for value in (d.get("values") or []) if value]
    if not surfaces:
        return []
    return _scan(text, surfaces)


def load_catalogue_for_test() -> Dict[str, Any]:
    """Test-only hook — returns the raw migration-source catalogue for parity checks."""
    return _load_catalogue()
