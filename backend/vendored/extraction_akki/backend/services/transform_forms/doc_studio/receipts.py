"""Receipt binding: a content-model receipt (`R01: {resolves_to}`) may carry an optional `platform_ref` naming a retained Akki
record (eij-/m9j-/lcj-/cr-/rcp-/gpurcp-/cwr-). At build time every platform_ref must resolve through the Deck Rendering Engine's
default resolver (no network, no fabrication); an unresolvable ref is a blocker and the build does not run.
Receipts without a platform_ref are `declared` — allowed, and marked so on the record."""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from services.transform_forms.deck_engine.validate import default_resolver


def bind_receipts(content: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    bound, blockers = {}, []
    for rid, rec in sorted((content.get("receipts") or {}).items()):
        ref = rec.get("platform_ref")
        if not ref:
            bound[rid] = {"resolves_to": rec["resolves_to"], "binding": "declared"}
            continue
        hit = default_resolver(ref)
        if hit is None:
            blockers.append({"receipt": rid, "platform_ref": ref, "rule": "unreceipted_exhibit", "message": f"platform receipt {ref} does not resolve against retained records"})
            bound[rid] = {"resolves_to": rec["resolves_to"], "platform_ref": ref, "binding": "unresolved"}
        else:
            bound[rid] = {"resolves_to": rec["resolves_to"], "platform_ref": ref, "binding": "platform", "kind": hit.get("kind"), "status": hit.get("status"), "verified": hit.get("verified")}
    return bound, blockers
