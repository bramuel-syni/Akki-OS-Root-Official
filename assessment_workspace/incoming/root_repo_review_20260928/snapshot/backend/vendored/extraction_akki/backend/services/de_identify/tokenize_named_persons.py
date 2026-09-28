"""W-RELEASE-GATE-PILOT-LIFT · CP-RG2 · tokenize_named_persons + get_token_table.

Discharge anchors (verbatim on single un-wrapped lines):

- R-15(a) · DECISIONS.md 2026-09-15T~03:55Z · Effect 2 (owner verbatim):
      "People's names are tokenized before anything leaves — placeholder tokens per custody class (Pull Seam identity-never-crosses). named_persons_verdict resolves to TOKENIZED for release purposes; build/wire the tokenization step into the transcript release path (tests-first)."

- Pull Seam §2 P1 · P015.s6 (canon source-file:
  canon/drops/20260914_pull_seam/extracted/The_Pull_Seam_STRUCTURED.txt · P015.s6):
      "There is no configuration in which estate data is transferred to compute outside the perimeter."

Contract:

    tokenize_named_persons(*, transcript_id, transcript_text, named_persons,
                            algorithm_version="tokenize_named_persons_v1")
        -> Tuple[str, TokenizationReceipt]

    Returns:
      - `tokenized_text` (str): the transcript_text with every occurrence of
        each named-person replaced by a placeholder token of shape
        `<TOKEN_NP_NN>` (two-digit zero-padded ordinal within the transcript,
        widened if >99 tokens).
      - `receipt` (TokenizationReceipt): frozen carrier · references the
        token table by opaque id · NEVER carries the mapping.

    Determinism:
      - Token assignment order within a call is stable (input `named_persons`
        order is honoured after deduplication + preservation of first-appearance).
      - Two byte-identical calls produce byte-identical `tokenized_text`.

    The token-to-name mapping is stored SEPARATELY in the module-scope
    custody store `_TOKEN_TABLES: Dict[receipt_id, Dict[placeholder, name]]`,
    accessible only via `get_token_table(receipt_id)`.

    get_token_table(receipt_id) -> Mapping[str, str]

    Returns the placeholder → name mapping for the given receipt_id.
    Raises `TokenTableMissing` on unknown receipt_id (no silent empty-return).

Identity-never-crosses invariant (test enforced by CP-RG2 test file):
    - The receipt has NO attribute that IS or CONTAINS the mapping.
    - The mapping is accessible only via `get_token_table` (separate call).
    - Names in `named_persons` never appear in any receipt attribute.
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Dict, Mapping, Sequence, Tuple

from contracts.tokenization_receipt import TokenizationReceipt


class TokenTableMissing(Exception):
    """Raised by `get_token_table` on unknown receipt_id.

    Custody-boundary integrity: no silent empty-table returns that could mask
    a lookup bug into an over-permissive downstream.
    """


# Custody-side store: receipt_id → {placeholder → name}.
# Module-scope singleton (mirrors _LEDGER pattern in services.release_gate.release_ledger).
_TOKEN_TABLES: Dict[str, Dict[str, str]] = {}


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _compute_receipt_id(
    *,
    transcript_id: str,
    tokenized_at_utc: str,
    token_count: int,
    algorithm_version: str,
) -> str:
    """Deterministic sha256-derived receipt_id in `tr_<64-hex>` shape."""
    material = f"{transcript_id}|{tokenized_at_utc}|{token_count}|{algorithm_version}"
    return "tr_" + hashlib.sha256(material.encode("utf-8")).hexdigest()


def _compute_table_ref(receipt_id: str) -> str:
    """Deterministic opaque reference derived from receipt_id.

    Shape: `tt_<64-hex>`. Not-a-primary-key; it is a receipt-scoped pointer
    into the custody store. Distinct from `receipt_id` to make cross-scan
    detection easier at audit time.
    """
    return "tt_" + hashlib.sha256(("table_ref_of|" + receipt_id).encode("utf-8")).hexdigest()


def _dedup_preserve_order(names: Sequence[str]) -> Tuple[str, ...]:
    """Preserve first-appearance order, deduplicate."""
    seen: Dict[str, None] = {}
    for n in names:
        if n and n not in seen:
            seen[n] = None
    return tuple(seen.keys())


def tokenize_named_persons(
    *,
    transcript_id: str,
    transcript_text: str,
    named_persons: Sequence[str],
    algorithm_version: str = "tokenize_named_persons_v1",
) -> Tuple[str, TokenizationReceipt]:
    """Tokenize each named-person occurrence in `transcript_text`.

    Deterministic: within one call, tokens are assigned in `named_persons`
    first-appearance-after-dedup order as `<TOKEN_NP_00>`, `<TOKEN_NP_01>`, …
    (two-digit zero-padded; widened to three digits at 100+).

    Returns `(tokenized_text, receipt)`. The mapping is stored in
    `_TOKEN_TABLES[receipt.receipt_id]` and retrievable via `get_token_table`.
    """
    canonical_names = _dedup_preserve_order(named_persons)
    token_count = len(canonical_names)

    # Placeholder width: 2 digits for ≤99 tokens, 3 for ≥100.
    width = 3 if token_count >= 100 else 2

    placeholder_by_name: Dict[str, str] = {}
    for i, name in enumerate(canonical_names):
        placeholder_by_name[name] = f"<TOKEN_NP_{i:0{width}d}>"

    # Replace each name in the text. Longer names first (so 'Alice' does not
    # partial-match inside 'AliceB'); tie-break by first-appearance order.
    tokenized = transcript_text
    for name in sorted(canonical_names, key=lambda n: (-len(n), canonical_names.index(n))):
        tokenized = tokenized.replace(name, placeholder_by_name[name])

    at_utc = _iso_utc_now()
    receipt_id = _compute_receipt_id(
        transcript_id=transcript_id,
        tokenized_at_utc=at_utc,
        token_count=token_count,
        algorithm_version=algorithm_version,
    )
    table_ref = _compute_table_ref(receipt_id)

    # Reverse map: placeholder → name (custody-side store row).
    reverse_map: Dict[str, str] = {p: n for n, p in placeholder_by_name.items()}
    _TOKEN_TABLES[receipt_id] = reverse_map

    receipt = TokenizationReceipt(
        receipt_id=receipt_id,
        transcript_id=transcript_id,
        tokenized_at_utc=at_utc,
        token_count=token_count,
        token_table_ref=table_ref,
        custody_class="named_person",
        algorithm_version=algorithm_version,
    )
    return tokenized, receipt


def get_token_table(receipt_id: str) -> Mapping[str, str]:
    """Return the placeholder → name mapping for the given receipt_id.

    Custody-side accessor. Raises `TokenTableMissing` on unknown receipt_id
    (no silent empty-return).
    """
    if receipt_id not in _TOKEN_TABLES:
        raise TokenTableMissing(
            f"no token table for receipt_id={receipt_id!r} (custody-boundary integrity: "
            f"no silent empty-return; a lookup failure MUST refuse)."
        )
    # Return a shallow copy so callers cannot mutate the store via the reference.
    return dict(_TOKEN_TABLES[receipt_id])


def _reset_for_tests() -> None:
    """Test-only fixture: clear the custody store."""
    _TOKEN_TABLES.clear()
