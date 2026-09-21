"""DAP Request Lifecycle · Q5 Escrow.

Owner ruling verbatim (STATE/DECISIONS.md R-78 · 2026-09-20T~13:00Z):
    "Q5 escrow — approve, one clause. Output held in escrow on suspension;
    Ready on lift; on termination, destruction is a receipted Ledger event
    that retains the artefact hash. The artefact goes; the record stays
    whole."

DAP-Spec §6 (Failure Posture):
    - DAP-29: "A metered event that cannot be written to the Ledger refuses
      the operation it meters."

Additive-only per SO §3.8.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict


class LedgerWriteRefused(Exception):
    """DAP-29: a Ledger write failure refuses the operation it meters."""


def hold_in_escrow_on_suspension(
    *,
    request_id: str,
    artefact_hash: str,
) -> Dict[str, Any]:
    """Hold the output in escrow when a suspension lands on Ready.

    Owner verbatim: "Output held in escrow on suspension".
    """
    return {
        "request_id": request_id,
        "artefact_hash": artefact_hash,
        "escrowed": True,
        "state_marker": "Ready-under-escrow",
        "escrowed_at_utc": datetime.now(tz=timezone.utc).isoformat(),
    }


def lift_suspension(
    *,
    request_id: str,
    artefact_hash: str,
) -> Dict[str, Any]:
    """Lift the suspension: back to Ready with the same artefact hash.

    Owner verbatim: "Ready on lift".
    """
    return {
        "request_id": request_id,
        "artefact_hash": artefact_hash,
        "new_state": "Ready",
        "escrowed": False,
        "lifted_at_utc": datetime.now(tz=timezone.utc).isoformat(),
    }


def terminate_and_destroy(
    *,
    request_id: str,
    artefact_hash: str,
    ledger_writer_stub_status: str = "ok",
) -> Dict[str, Any]:
    """Terminate and destroy the artefact.

    Owner verbatim: "on termination, destruction is a receipted Ledger event
    that retains the artefact hash. The artefact goes; the record stays
    whole." DAP-29: a Ledger write failure refuses the destruction.
    """
    if ledger_writer_stub_status == "unreachable":
        raise LedgerWriteRefused(
            f"DAP-29 · destruction Ledger write refused for request "
            f"{request_id} · unrecorded destruction is not permitted to have happened"
        )

    return {
        "request_id": request_id,
        "operation_type": "destruction",
        "artefact_hash": artefact_hash,       # HASH RETAINED (record stays whole)
        "artefact_present": False,            # ARTEFACT GONE
        "ledger_receipted": True,
        "destroyed_at_utc": datetime.now(tz=timezone.utc).isoformat(),
    }
