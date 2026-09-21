"""services.chokepoint.dry_run — CA1-007 · Doc 02 §A5.2/§A5.3 dry-run preview.

Owner Order 2026-08-25 · "W3 go" · Section D.

Contract:
  preview(candidate_declaration, sample_scope) → preview envelope
      Runs the candidate against the crossing-receipt log by identity
      (REFERENCE-NOT-COPY). Never mutates state; never emits a crossing;
      never adopts the declaration.

  DeclarationInvalid
      Raised when the candidate is not mechanically testable
      (Doc 02 §A5.2 · a free-text instruction is not adoptable).

Candidate declaration shapes (Doc 02 §A3 three levels of specificity):
  {"kind": "exact_value", "value": str}
  {"kind": "pattern",     "regex": str}
  {"kind": "category",    "category": str}    # symbolic — matches by name

Envelope:
  {
    "preview_id":      "prv-<hex12>",
    "sample_scope":    "crossing_receipts_recent",
    "sample_size":     int,                 # receipts walked
    "would_catch_refs": [receipt_id, ...],  # identity strings (rcp-*)
    "would_miss_refs":  [receipt_id, ...],  # identity strings (rcp-*)
    "honest_gap":      "plain sentence naming the unmeasured state",
    "generated_at_iso": iso timestamp,
    "candidate_declaration_kind": "exact_value" | "pattern" | "category"
  }

No side effects. No adoption. No LLM SDK.
"""
from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

from services.chokepoint import list_receipts


class DeclarationInvalid(ValueError):
    """Doc 02 §A5.2 · candidate is not mechanically testable."""


_TESTABLE_KINDS = frozenset({"exact_value", "pattern", "category"})


# Honest-gap grammar per owner (2026-08-25 · W2/W3 · plain sentence + provenance
# + drawn-not-blank; no wave names on user surface).
_HONEST_GAP_NO_ROW_BEARING_TRAFFIC = (
    "The estate has not yet run a row-bearing query — every crossing on "
    "record moved metadata only (information_schema, attested SSH commands, "
    "governance reads). This preview shows how the candidate would score "
    "against that traffic; it cannot yet show how it would score against "
    "row content. A row-bearing sample will populate here when the first "
    "query carrying row data is admitted."
)


def _validate_candidate(candidate: Dict[str, Any]) -> str:
    """Validate the candidate declaration; returns the kind string."""
    kind = (candidate or {}).get("kind")
    if kind not in _TESTABLE_KINDS:
        raise DeclarationInvalid(
            f"declaration_not_testable — kind={kind!r} is not a mechanically "
            f"testable declaration shape. Doc 02 §A3 admits: {sorted(_TESTABLE_KINDS)!r}. "
            "A free-text instruction is not adoptable."
        )
    if kind == "exact_value":
        if not (candidate.get("value") or "").strip():
            raise DeclarationInvalid("exact_value declaration requires a non-empty 'value'.")
    elif kind == "pattern":
        rx = candidate.get("regex") or ""
        if not rx:
            raise DeclarationInvalid("pattern declaration requires a non-empty 'regex'.")
        try:
            re.compile(rx)
        except re.error as exc:
            raise DeclarationInvalid(f"pattern declaration regex uncompilable: {exc}") from exc
    else:  # category
        if not (candidate.get("category") or "").strip():
            raise DeclarationInvalid("category declaration requires a non-empty 'category'.")
    return kind


def _receipt_haystack(receipt) -> str:
    """Build a haystack string from a receipt's non-credential fields.

    REFERENCE-NOT-COPY caveat: we synthesise a haystack in memory to run the
    match. We do NOT persist it. The preview envelope carries only the
    identity of the receipt, never this haystack.
    """
    payload = receipt.payload_shape or {}
    fields = [
        receipt.kind,
        receipt.endpoint_host,
        receipt.verb,
        receipt.actor,
        receipt.masking_tier,
    ]
    for v in payload.values():
        fields.append(str(v))
    return " ".join(str(f) for f in fields if f)


def _matches(candidate: Dict[str, Any], haystack: str) -> bool:
    kind = candidate["kind"]
    if kind == "exact_value":
        return candidate["value"] in haystack
    if kind == "pattern":
        return re.search(candidate["regex"], haystack) is not None
    if kind == "category":
        # Symbolic category match: the receipt haystack must literally name
        # the category (e.g. "unreleased_pricing" appears in verb or actor).
        # No reasoning-layer recogniser lives in this estate yet (Doc 02
        # §A3 category-level match requires the reasoning layer — awaits
        # a later wave). Honest state: symbolic-name match only for now.
        return candidate["category"].lower() in haystack.lower()
    return False


def preview(
    *,
    candidate_declaration: Dict[str, Any],
    sample_scope: str = "crossing_receipts_recent",
) -> Dict[str, Any]:
    """CA1-007 · dry-run preview.

    Walks the crossing-receipt log by identity and reports which receipts
    the candidate would (would_catch_refs) or would not (would_miss_refs)
    have matched — without adopting the declaration.
    """
    kind = _validate_candidate(candidate_declaration or {})

    receipts = list_receipts()
    catch: List[str] = []
    miss: List[str] = []
    row_bearing_count = 0
    for r in receipts:
        haystack = _receipt_haystack(r)
        if _matches(candidate_declaration, haystack):
            catch.append(r.receipt_id)
        else:
            miss.append(r.receipt_id)
        # Row-bearing tiers (t1_full_mask, t2_partial, t3_category) — none
        # in force today, but count honestly.
        if r.masking_tier in ("t1_full_mask", "t2_partial", "t3_category"):
            row_bearing_count += 1

    now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    envelope: Dict[str, Any] = {
        "preview_id": f"prv-{uuid.uuid4().hex[:12]}",
        "sample_scope": sample_scope,
        "sample_size": len(receipts),
        "would_catch_refs": catch,
        "would_miss_refs": miss,
        "honest_gap": (
            _HONEST_GAP_NO_ROW_BEARING_TRAFFIC
            if row_bearing_count == 0
            else ""
        ),
        "generated_at_iso": now_iso,
        "candidate_declaration_kind": kind,
    }
    return envelope
