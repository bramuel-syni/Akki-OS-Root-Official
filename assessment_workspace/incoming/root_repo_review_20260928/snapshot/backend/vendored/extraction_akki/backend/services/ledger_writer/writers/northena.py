"""services.ledger_writer.writers.northena — M10-W4c · northena
(non-refusal) writer consolidation replay adapter (third sub-wave of
Milestone 2).

Owner Run Order 2026-09-18T~21:15Z (verbatim, banked in STATE/DECISIONS.md):
    "Milestone 2 · M10-W4 · writer consolidation: refusal → countersign
     → northena → deletion → memory. Per-writer replay test PASSING is
     precondition to landing that writer (legacy row-hash reproduction ·
     zero rows lost). Legacy stores go read-only at cutover · never
     rewritten."

This module folds the legacy `contracts.northena_ledger.LedgerRow`
non-refusal row shape — persisted by `services.northena.ledger.record`
into `phase0/northena_ledger/<row_id>.json` and mirrored to Mongo
`NORTHENA_LEDGER_COLLECTION` — into the unified
`contracts.ledger_v1.LedgerRow_v1` 17-field hash-chained row emitted
via `services.ledger_writer.main.append_intent`.

Non-refusal scope: rows whose `decision != "refused"` (admit / gate /
converge and any future non-refusal decision). Refusal-class rows are
routed to `services.ledger_writer.writers.refusal` (W4a); this module
raises `ValueError` on them for structural role separation.

Contract:

  `legacy_northena_canonical_bytes(legacy_row) -> bytes`:
      Deterministic canonical UTF-8 JSON.

  `legacy_northena_payload_ref(legacy_row) -> str`:
      `sha256(legacy_northena_canonical_bytes(row)).hexdigest()`.

  `replay_legacy_northena_to_intent(legacy_row, tenant_id) -> LedgerIntent`:
      Maps a legacy Northena non-refusal row to a unified `LedgerIntent`:
        - `tenant_id`:           caller-supplied
        - `run_id`:              legacy_row.run_id
        - `task_id`:             legacy_row.trace_id
        - `actor_id`:            "service:northena_ledger"
        - `actor_type`:          "service"
        - `event_type`:          legacy_row.stage
        - `resource_type`:       legacy_row.artifact_ref.artifact_type
        - `resource_id`:         legacy_row.artifact_ref.artifact_id
        - `decision`:            legacy_row.decision
        - `reason_code`:         legacy_row.reason
        - `payload_ref`:         legacy_northena_payload_ref(legacy_row)
        - `at`:                  LedgerRowAt(epoch_s=int(row.at.timestamp()),
                                             source="wall_clock")
        - `break_glass_session_id`: None

      Refuses (raises `ValueError`) on rows with `decision == "refused"`
      — those belong to W4a's refusal adapter.

Structural discipline (owner mandate 'Legacy stores go read-only at
cutover · never rewritten'), AST-enforced by the invariant suite:

  * This module does NOT import `services.northena.ledger` (the legacy
    JSON + Mongo write surface).
  * This module DOES import `LedgerIntent` from
    `services.ledger_emitter.emit_intent`.

M3 forward-compat: the `LedgerIntent` produced by this adapter carries
NO `confidence` / `score` / `strength` / `probability` field.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from contracts.ledger_v1 import LedgerRowAt
from contracts.northena_ledger import LedgerRow as LegacyNorthenaLedgerRow
from services.ledger_emitter.emit_intent import LedgerIntent


_LEGACY_NORTHENA_EMITTER_ACTOR_ID = "service:northena_ledger"
_REFUSAL_DECISION = "refused"


def _artifact_ref_to_dict(ref) -> dict:
    """Deterministic dict form of `LedgerArtifactRef`."""
    return {
        "artifact_type": ref.artifact_type,
        "artifact_id": ref.artifact_id,
        "version": ref.version,
    }


def _stamp_audit_to_deterministic(stamp_audit: Any) -> Any:
    """Deterministic form of `stamp_audit` (dict-sorted or the None
    sentinel unchanged)."""
    if stamp_audit is None:
        return None
    if isinstance(stamp_audit, Mapping):
        return {k: stamp_audit[k] for k in sorted(stamp_audit.keys())}
    return stamp_audit


def legacy_northena_canonical_bytes(
    legacy_row: LegacyNorthenaLedgerRow,
) -> bytes:
    """Deterministic canonical UTF-8 JSON over every field of the legacy
    Northena row (row-hash reproduction primitive)."""
    payload = {
        "row_id": legacy_row.row_id,
        "run_id": legacy_row.run_id,
        "trace_id": legacy_row.trace_id,
        "stage": legacy_row.stage,
        "decision": legacy_row.decision,
        "reason": legacy_row.reason,
        "artifact_ref": _artifact_ref_to_dict(legacy_row.artifact_ref),
        "lawful_basis_ref": legacy_row.lawful_basis_ref,
        "stamp_audit": _stamp_audit_to_deterministic(legacy_row.stamp_audit),
        "at": legacy_row.at.isoformat(),
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def legacy_northena_payload_ref(legacy_row: LegacyNorthenaLedgerRow) -> str:
    """sha256_hex of `legacy_northena_canonical_bytes(legacy_row)`."""
    return hashlib.sha256(legacy_northena_canonical_bytes(legacy_row)).hexdigest()


def replay_legacy_northena_to_intent(
    *,
    legacy_row: LegacyNorthenaLedgerRow,
    tenant_id: str,
) -> LedgerIntent:
    """Map a legacy Northena non-refusal `LedgerRow` to a unified
    `LedgerIntent`.

    Refuses rows with `decision == "refused"` (routes them to W4a
    refusal adapter for structural role separation)."""
    if legacy_row.decision == _REFUSAL_DECISION:
        raise ValueError(
            f"LEDGER-W4C-001: northena adapter refuses to replay refusal-"
            f"class row (row_id={legacy_row.row_id!r}, decision='refused'); "
            f"route via services.ledger_writer.writers.refusal."
            f"replay_legacy_refusal_to_intent (W4a) instead."
        )
    return LedgerIntent(
        tenant_id=tenant_id,
        run_id=legacy_row.run_id,
        task_id=legacy_row.trace_id,
        actor_id=_LEGACY_NORTHENA_EMITTER_ACTOR_ID,
        actor_type="service",
        event_type=legacy_row.stage,
        resource_type=legacy_row.artifact_ref.artifact_type,
        resource_id=legacy_row.artifact_ref.artifact_id,
        decision=legacy_row.decision,
        reason_code=legacy_row.reason,
        payload_ref=legacy_northena_payload_ref(legacy_row),
        at=LedgerRowAt(epoch_s=int(legacy_row.at.timestamp()), source="wall_clock"),
        break_glass_session_id=None,
    )


__all__ = [
    "legacy_northena_canonical_bytes",
    "legacy_northena_payload_ref",
    "replay_legacy_northena_to_intent",
]
