"""W-RELEASE-GATE-PILOT-LIFT · CP-RG1 · Release-ledger append-only writer.

Discharge anchors (canon + owner rulings; verbatim quotes on single un-wrapped lines):

- R-7 · DECISIONS.md 2026-09-15T~03:55Z · Effect 1 (owner verbatim):
      "every release is still receipted AND debited into a running release ledger from day one — so when the pilot ends, the real budget number is set from measured usage, not guessed. The gate's refusal on unset-budget is replaced by pilot-mode admission WITH mandatory receipt+debit; a missing receipt still refuses (Pull Seam P7 unchanged)."

- Pull Seam §2 P7 · P036 (canon source-file:
  canon/drops/20260914_pull_seam/extracted/The_Pull_Seam_STRUCTURED.txt · P036):
      "The receipt is written before the result is returned. If it cannot be written, the operation is refused."

Behaviour:

    record_debit(*, receipt_id, budget_state, usage_quantity, usage_unit,
                 debited_by_party) -> ReleaseLedgerDebit

  Refusal branches (in order):
    1. `ReceiptMissingRefused` when `receipt_id` is empty (P036 anchor:
       "the receipt is written before the result is returned; if it cannot
       be written, the operation is refused"). Reinforces R-7 clause
       "a missing receipt still refuses (Pull Seam P7 unchanged)".
    2. `BudgetStateRefused` when `budget_state == DEFAULT_PENDING_OVERRIDE`
       (R-7 verbatim: "the gate's refusal on unset-budget is replaced by
       pilot-mode admission" — the replacement is CONDITIONAL on the state
       being explicitly non-default; the default refusal is NOT lifted).

  On admit: writes a deterministic-id `ReleaseLedgerDebit` to an append-only
  in-memory ledger; returns the debit. CP-RG5 will land `aggregate_usage_query`
  for the pilot-end owner-derivation of the real budget number.

Test-only fixture:

    _reset_for_tests() -> None
        Clears the ledger. Test fixtures call this; production code MUST NOT.
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import List, Tuple

from contracts.release_budget import ReleaseBudgetState, ReleaseLedgerDebit


class ReceiptMissingRefused(Exception):
    """P036 anchor: the receipt is written before the result is returned; if
    it cannot be written, the operation is refused.

    Reinforces R-7 clause "a missing receipt still refuses (Pull Seam P7
    unchanged)".
    """


class BudgetStateRefused(Exception):
    """R-7 anchor: the gate's refusal on unset-budget is REPLACED by pilot-mode
    admission — not universally lifted. `DEFAULT_PENDING_OVERRIDE` still refuses;
    only `PILOT_OPEN` (and later `ENFORCED_POST_PILOT`) admit.
    """


# Append-only in-memory ledger (module-scope singleton).
_LEDGER: List[ReleaseLedgerDebit] = []


def _iso_utc_now() -> str:
    """ISO-8601 UTC timestamp, second precision: YYYY-MM-DDThh:mm:ssZ."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _compute_debit_id(
    *,
    receipt_id: str,
    at_utc: str,
    usage_quantity: int,
    usage_unit: str,
    party: str,
) -> str:
    """Deterministic sha256-derived debit_id in `rd_<64-hex>` shape.

    Material: `receipt_id|at_utc|usage_quantity|usage_unit|party` UTF-8 encoded.
    Byte-identical material MUST produce the same debit_id (test-independence
    property — no run-time nonce).
    """
    material = f"{receipt_id}|{at_utc}|{usage_quantity}|{usage_unit}|{party}"
    return "rd_" + hashlib.sha256(material.encode("utf-8")).hexdigest()


def record_debit(
    *,
    receipt_id: str,
    budget_state: ReleaseBudgetState,
    usage_quantity: int,
    usage_unit: str,
    debited_by_party: str,
) -> ReleaseLedgerDebit:
    """Record one debit against the release ledger.

    Refuses on:
      - empty `receipt_id` (P036 receipt-before-result anchor).
      - `budget_state == DEFAULT_PENDING_OVERRIDE` (R-7 default-refusal anchor).

    Otherwise appends a new `ReleaseLedgerDebit` to the ledger and returns it.
    """
    if not receipt_id:
        raise ReceiptMissingRefused(
            "P036: the receipt is written before the result is returned; "
            "if it cannot be written, the operation is refused."
        )
    if budget_state == ReleaseBudgetState.DEFAULT_PENDING_OVERRIDE:
        raise BudgetStateRefused(
            "R-7: DEFAULT_PENDING_OVERRIDE refusal is not universally lifted; "
            "PILOT_OPEN admission is the specific replacement."
        )

    at_utc = _iso_utc_now()
    debit = ReleaseLedgerDebit(
        debit_id=_compute_debit_id(
            receipt_id=receipt_id,
            at_utc=at_utc,
            usage_quantity=usage_quantity,
            usage_unit=usage_unit,
            party=debited_by_party,
        ),
        receipt_id=receipt_id,
        debited_at_utc=at_utc,
        budget_state_at_debit=budget_state,
        usage_quantity=usage_quantity,
        usage_unit=usage_unit,
        debited_by_party=debited_by_party,
    )
    _LEDGER.append(debit)
    return debit


def list_debits() -> Tuple[ReleaseLedgerDebit, ...]:
    """Snapshot view of the append-only ledger.

    Returns an immutable tuple (not the list) so callers cannot mutate the
    ledger via the returned reference.
    """
    return tuple(_LEDGER)


def aggregate_usage_query(
    *,
    unit: "str | None" = None,
    budget_state: "ReleaseBudgetState | None" = None,
    debited_by_party: "str | None" = None,
) -> "dict[str, int]":
    """W-RELEASE-GATE-PILOT-LIFT · CP-RG5 · Aggregate usage across the ledger.

    R-7 verbatim (DECISIONS 2026-09-15T~03:55Z · Effect 1):
      "when the pilot ends, the real budget number is set from measured
       usage, not guessed."

    This is the owner-facing API for the pilot-end derivation.  Optional
    filters compose (AND semantics).  Returns:

        {"debit_count": int, "total_quantity": int}

    - `debit_count` = number of matching ReleaseLedgerDebit rows
    - `total_quantity` = sum of `usage_quantity` over matching rows
    """
    matching: list = []
    for d in _LEDGER:
        if unit is not None and d.usage_unit != unit:
            continue
        if budget_state is not None and d.budget_state_at_debit != budget_state:
            continue
        if debited_by_party is not None and d.debited_by_party != debited_by_party:
            continue
        matching.append(d)
    return {
        "debit_count": len(matching),
        "total_quantity": sum(d.usage_quantity for d in matching),
    }


def _reset_for_tests() -> None:
    """Test-only fixture: clear the ledger.

    Production code MUST NOT call this. Test files declare its use in-docstring
    per SO §3 test-hygiene discipline.
    """
    _LEDGER.clear()
