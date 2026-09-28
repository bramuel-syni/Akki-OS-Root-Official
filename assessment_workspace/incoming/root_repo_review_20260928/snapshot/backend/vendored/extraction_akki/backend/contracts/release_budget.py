"""W-RELEASE-GATE-PILOT-LIFT · CP-RG1 · Release budget state + release-ledger debit carrier.

Discharge anchors (canon + owner rulings; verbatim quotes on single un-wrapped lines):

- R-7 · DECISIONS.md 2026-09-15T~03:55Z · Effect 1 (owner verbatim):
      "budget state = PILOT-OPEN (owner-ratified, supersedes DEFAULT-PENDING-OVERRIDE refusal), BUT every release is still receipted AND debited into a running release ledger from day one — so when the pilot ends, the real budget number is set from measured usage, not guessed. The gate's refusal on unset-budget is replaced by pilot-mode admission WITH mandatory receipt+debit; a missing receipt still refuses (Pull Seam P7 unchanged)."

- Pull Seam §2 P7 · P036 (canon source-file:
  canon/drops/20260914_pull_seam/extracted/The_Pull_Seam_STRUCTURED.txt · P036):
      "Each operation writes a receipt: what was accessed, in what quantity, under which terms, by which party, at what time."
      "The receipt is written before the result is returned. If it cannot be written, the operation is refused."

Shape (frozen · closed enum · exactly-seven-carrier data class):

- `ReleaseBudgetState`: closed three-value enum
  - `DEFAULT_PENDING_OVERRIDE` (pre-ratification default that R-7 supersedes)
  - `PILOT_OPEN` (owner-ratified current)
  - `ENFORCED_POST_PILOT` (owner sets real budget number from measured usage
    "when the pilot ends" per R-7 verbatim)

- `ReleaseLedgerDebit`: frozen dataclass, exact-ordered seven carriers:
  - `debit_id`               : `str` · deterministic sha256-derived (`rd_<64-hex>`)
  - `receipt_id`             : `str` · foreign-key reference to the release receipt
                                (P036 "what was accessed")
  - `debited_at_utc`         : `str` · ISO-8601 UTC (P036 "at what time")
  - `budget_state_at_debit`  : `ReleaseBudgetState` (P036 "under which terms")
  - `usage_quantity`         : `int` · quantity (P036 "in what quantity")
  - `usage_unit`             : `str` · unit for quantity (P036 "in what quantity")
  - `debited_by_party`       : `str` · party (P036 "by which party")

Landing in `NON_CONTRACT_UTILITY_MODULES` (test_frozen_contract_snapshot_parity.py):
this module holds a frozen `@dataclass` + closed `Enum` — no pydantic BaseModel; the
frozen-contract-parity domain does not apply.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ReleaseBudgetState(Enum):
    """Release-budget lifecycle state. Closed three-value enum.

    - `DEFAULT_PENDING_OVERRIDE`: pre-ratification default. Refuses admission.
      Superseded by R-7 owner ruling 2026-09-15T~03:55Z Effect 1 for pilot-mode.
    - `PILOT_OPEN`: owner-ratified pilot state (R-7 Effect 1). Admission proceeds
      WITH mandatory receipt+debit written to the release ledger.
    - `ENFORCED_POST_PILOT`: post-pilot state. Owner sets the real budget number
      from measured usage (R-7 Effect 1 verbatim: "when the pilot ends, the real
      budget number is set from measured usage, not guessed").
    """

    DEFAULT_PENDING_OVERRIDE = "DEFAULT_PENDING_OVERRIDE"
    PILOT_OPEN = "PILOT_OPEN"
    ENFORCED_POST_PILOT = "ENFORCED_POST_PILOT"


@dataclass(frozen=True)
class ReleaseLedgerDebit:
    """Frozen carrier for one debit row in the release ledger.

    Field order is fixed by P036 semantic mapping:
      what was accessed → receipt_id
      in what quantity  → usage_quantity + usage_unit
      under which terms → budget_state_at_debit
      by which party    → debited_by_party
      at what time      → debited_at_utc
    Plus `debit_id` (deterministic sha256-derived row identity).

    Mutation after construction raises `FrozenInstanceError`. Adding fields to
    this class is a snapshot-parity event even though `release_budget.py` is
    in NON_CONTRACT_UTILITY_MODULES — every wave adding a carrier must extend
    the corresponding CP tests in CP-RG* pattern.
    """

    debit_id: str
    receipt_id: str
    debited_at_utc: str
    budget_state_at_debit: ReleaseBudgetState
    usage_quantity: int
    usage_unit: str
    debited_by_party: str
