"""contracts/ledger_v1.py · M10-W1 · Ledger row schema v1 · frozen.

Owner-ratified 17-field row schema per B-M10-Q1 conformance confirmation
(EXTENDED AUTOPILOT ruling 2026-09-18T~12:30Z · disposition ratifies
conformance-check-as-ratification).

Canon anchors (verbatim):
  v1.0 B.4 · Ledger row 17-field schema owner-anchored via B-M10-Q1.
  Canon 3 §9.2 · Ledger records everything · row shape rules BR-13/BR-14.
  DAP-21 · every metered event carries its metering-context by hash.
  A5.19 · every verdict Grey Mirror passes to Mkono carries a certificate
          — Watch-action rows MUST have A5.19-conformant certificate ref.
  R-C1 · controlled_determination_basis marker (deterministic-vs-hybrid
         classification per determinism_inventory_v1).
  R-C2 · au_3b_defensible marker (defaults False until reliable time source
         exists).  Coupled invariant: at.source == "reliable" ⟺ au_3b_defensible=True.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional


LEDGER_SCHEMA_VERSION: str = "v1"


# --- The 17 fields per B-M10-Q1 conformance -----------------------------

LEDGER_ROW_FIELDS: tuple[str, ...] = (
    "seq",                        # 1: monotonic per-tenant sequence int
    "prev_hash",                  # 2: 64-hex sha256 of prior row hash (or 64 zeros at genesis)
    "hash",                       # 3: 64-hex sha256(prev_hash || canonical(row))
    "schema_version",             # 4: str · currently "v1"
    "tenant_id",                  # 5: OPEN str
    "run_id",                     # 6: OPEN str
    "task_id",                    # 7: OPEN str
    "actor_id",                   # 8: OPEN str
    "actor_type",                 # 9: OPEN str · e.g. "principal", "service", "system"
    "event_type",                 # 10: OPEN str · e.g. "admit", "gate", "converge", "refuse"
    "resource_type",              # 11: OPEN str
    "resource_id",                # 12: OPEN str
    "decision",                   # 13: OPEN str · e.g. "admitted", "refused", "converged"
    "reason_code",                # 14: OPEN str · refusal-family-registry code or empty
    "payload_ref",                # 15: sha256 of the payload document · str
    "at",                         # 16: dict · {"epoch_s": int, "source": str} · reliable time source coupling
    "break_glass_session_id",     # 17: OPEN str or None
)


@dataclass(frozen=True)
class LedgerRowAt:
    """Time carrier per B-M10-Q1 · coupling gate with au_3b_defensible."""
    epoch_s: int
    source: str  # "wall_clock" or "reliable" — coupling invariant enforced at write


@dataclass(frozen=True)
class LedgerRow:
    """The 17-field ledger row per B-M10-Q1.

    All identifier fields are OPEN str per SO §3.10 Option α (no closed enum).
    """
    # Chain identity
    seq: int
    prev_hash: str
    hash: str
    schema_version: str
    # Provenance
    tenant_id: str
    run_id: str
    task_id: str
    actor_id: str
    actor_type: str
    # Event
    event_type: str
    resource_type: str
    resource_id: str
    decision: str
    reason_code: str
    payload_ref: str
    # Time
    at: LedgerRowAt
    # Break-glass
    break_glass_session_id: Optional[str] = None


# --- Genesis & canonical serialisation ----------------------------------

GENESIS_PREV_HASH: str = "0" * 64


def canonical_row_bytes(row: LedgerRow) -> bytes:
    """Deterministic canonical UTF-8 JSON for hashing.

    NOTE: hash field is EXCLUDED from canonical bytes (a row hashes over
    everything EXCEPT its own hash).
    """
    import json

    payload = {
        "seq": row.seq,
        "prev_hash": row.prev_hash,
        "schema_version": row.schema_version,
        "tenant_id": row.tenant_id,
        "run_id": row.run_id,
        "task_id": row.task_id,
        "actor_id": row.actor_id,
        "actor_type": row.actor_type,
        "event_type": row.event_type,
        "resource_type": row.resource_type,
        "resource_id": row.resource_id,
        "decision": row.decision,
        "reason_code": row.reason_code,
        "payload_ref": row.payload_ref,
        "at": {"epoch_s": row.at.epoch_s, "source": row.at.source},
        "break_glass_session_id": row.break_glass_session_id,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()


def au_3b_defensible(row: LedgerRow) -> bool:
    """R-C2 coupling: at.source == 'reliable' ⟺ au_3b_defensible=True."""
    return row.at.source == "reliable"


# --- Pydantic schema-freeze mirror (additive · parity-domain surface) ------
#
# `LedgerRow` above is a `@dataclass(frozen=True)` because the hash-chain
# canonical bytes function needs deterministic dataclass semantics.  The
# frozen-contract-snapshot parity domain (see
# `tests/invariants/test_frozen_contract_snapshot_parity.py`) is pydantic
# `model_json_schema()` output — so this module additively exposes a
# `LedgerRow_v1` pydantic mirror whose sole purpose is to be the
# schema-freeze surface for the parity invariant.  The mirror is BYTE-
# FAITHFUL to the 17 B-M10-Q1 fields (owner ratification banked in
# `STATE/DECISIONS.md § "B-M10-Q1 conformance confirmation"`).  Consumers
# use the dataclass form; the mirror is a shape declaration only.
#
# The mirror is NEVER used to construct rows at write time (that would
# introduce a second serialisation path that diverges from
# `canonical_row_bytes`).  It exists solely so `LedgerRow_v1.model_json_schema()`
# renders the frozen contract JSON at `tests/invariants/ledger_v1.contract_snapshot.json`.
from pydantic import BaseModel, ConfigDict, Field  # noqa: E402
from typing import Literal  # noqa: E402


class LedgerRowAt_v1(BaseModel):
    """Time carrier mirror (pydantic parity surface for LedgerRowAt)."""
    model_config = ConfigDict(extra="forbid")

    epoch_s: int = Field(..., description="Unix epoch seconds.")
    source: Literal["wall_clock", "reliable"] = Field(
        ...,
        description="Time source · coupling gate with au_3b_defensible.",
    )


class LedgerRow_v1(BaseModel):
    """The 17 owner-ratified B-M10-Q1 fields · pydantic parity surface.

    Field enumeration is IDENTICAL to `LedgerRow` (the runtime dataclass);
    only the base class differs.  Any B-M10-Q1 schema change requires the
    dataclass AND this mirror AND the snapshot to move together
    (frozen-contract+snapshot same-commit DoD).
    """

    model_config = ConfigDict(extra="forbid")

    # Chain identity
    seq: int = Field(..., description="Monotonic per-tenant sequence integer.")
    prev_hash: str = Field(..., description="64-hex sha256 of prior row hash · genesis is 64 zeros.")
    hash: str = Field(..., description="64-hex sha256(prev_hash || canonical(row)).")
    schema_version: str = Field(..., description="Currently 'v1'.")
    # Provenance
    tenant_id: str = Field(..., description="Tenant identifier.")
    run_id: str = Field(..., description="Run identifier.")
    task_id: str = Field(..., description="Task identifier.")
    actor_id: str = Field(..., description="Acting principal / service / system identifier.")
    actor_type: str = Field(..., description="OPEN str · e.g. principal / service / system.")
    # Event
    event_type: str = Field(..., description="OPEN str · e.g. admit / gate / converge / refuse / watch.*.")
    resource_type: str = Field(..., description="OPEN str.")
    resource_id: str = Field(..., description="OPEN str.")
    decision: str = Field(..., description="OPEN str · e.g. admitted / refused / converged.")
    reason_code: str = Field(..., description="Refusal-family-registry code or empty.")
    payload_ref: str = Field(
        ...,
        description=(
            "sha256 of the payload document · hash-binds DAP-21 metered fields "
            "(quantity_natural_unit, terms_identifier, party_principal), A5.19 "
            "certificate on watch.* rows, R-C1 controlled_determination_basis, "
            "and R-C2 au_3b_defensible sub-fields (all documented per "
            "B-M10-Q1 conformance confirmation)."
        ),
    )
    # Time
    at: LedgerRowAt_v1 = Field(..., description="Time carrier · coupling with au_3b_defensible.")
    # Break-glass
    break_glass_session_id: Optional[str] = Field(
        default=None,
        description="Break-glass session id · optional.",
    )
