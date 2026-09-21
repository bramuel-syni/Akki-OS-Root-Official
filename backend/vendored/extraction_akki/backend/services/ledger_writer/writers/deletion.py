"""services.ledger_writer.writers.deletion — M10-W4d · deletion writer
consolidation replay adapter (fourth sub-wave of Milestone 2).

Owner Run Order 2026-09-18T~21:15Z (verbatim, banked in STATE/DECISIONS.md):
    "Milestone 2 · M10-W4 · writer consolidation: refusal → countersign
     → northena → deletion → memory. Per-writer replay test PASSING is
     precondition to landing that writer (legacy row-hash reproduction ·
     zero rows lost). Legacy stores go read-only at cutover · never
     rewritten."

This module folds the legacy `contracts.northena_ledger.LedgerRow`
authorized_deletion row shape — emitted by
`services.compliance.deletion_ledger.emit_deletion_ledger_row` when
called with `data_class="authorized_deletion"` from
`services.retention.authorized_deletion.execute_authorized_deletion` —
into the unified `contracts.ledger_v1.LedgerRow_v1` 17-field
hash-chained row emitted via `services.ledger_writer.main.append_intent`.

Data-class scope: exactly `stamp_audit["data_class"] == "authorized_deletion"`.
Rows with any other data_class value are refused via `ValueError`
(structural role separation — countersign belongs to W4b, memory to W4e).

Contract:

  `legacy_deletion_canonical_bytes(legacy_row) -> bytes`:
      Deterministic canonical UTF-8 JSON.

  `legacy_deletion_payload_ref(legacy_row) -> str`:
      `sha256(legacy_deletion_canonical_bytes(row)).hexdigest()`.

  `replay_legacy_deletion_to_intent(legacy_row, tenant_id) -> LedgerIntent`:
      Maps a legacy authorized_deletion row to a unified `LedgerIntent`:
        - `tenant_id`:           caller-supplied
        - `run_id`:              legacy_row.run_id
        - `task_id`:             legacy_row.trace_id
        - `actor_id`:            "service:deletion_ledger"
        - `actor_type`:          "service"
        - `event_type`:          "delete"
        - `resource_type`:       legacy_row.artifact_ref.artifact_type
        - `resource_id`:         legacy_row.artifact_ref.artifact_id
        - `decision`:            "continue"  (mirrors legacy neutral placeholder)
        - `reason_code`:         legacy_row.stamp_audit["held_class"]
        - `payload_ref`:         legacy_deletion_payload_ref(legacy_row)
        - `at`:                  LedgerRowAt(epoch_s=int(row.at.timestamp()),
                                             source="wall_clock")
        - `break_glass_session_id`: None

      Refuses (ValueError) if stamp_audit['data_class'] != 'authorized_deletion'.

Structural discipline (AST-enforced): does NOT import
`services.compliance.deletion_ledger` (the legacy emitter/write surface)
nor `services.retention.authorized_deletion` (upstream caller). DOES
import `LedgerIntent` from `services.ledger_emitter.emit_intent`.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from contracts.ledger_v1 import LedgerRowAt
from contracts.northena_ledger import LedgerRow as LegacyDeletionLedgerRow
from services.ledger_emitter.emit_intent import LedgerIntent


_LEGACY_DELETION_EMITTER_ACTOR_ID = "service:deletion_ledger"
_DELETION_EVENT_TYPE = "delete"
_DELETION_DECISION = "continue"
_AUTHORIZED_DELETION_DATA_CLASS = "authorized_deletion"


def _artifact_ref_to_dict(ref) -> dict:
    return {
        "artifact_type": ref.artifact_type,
        "artifact_id": ref.artifact_id,
        "version": ref.version,
    }


def _stamp_audit_to_deterministic(stamp_audit: Any) -> Any:
    if stamp_audit is None:
        return None
    if isinstance(stamp_audit, Mapping):
        return {k: stamp_audit[k] for k in sorted(stamp_audit.keys())}
    return stamp_audit


def legacy_deletion_canonical_bytes(
    legacy_row: LegacyDeletionLedgerRow,
) -> bytes:
    """Deterministic canonical UTF-8 JSON over every field of the legacy
    authorized_deletion row."""
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


def legacy_deletion_payload_ref(legacy_row: LegacyDeletionLedgerRow) -> str:
    return hashlib.sha256(legacy_deletion_canonical_bytes(legacy_row)).hexdigest()


def replay_legacy_deletion_to_intent(
    *,
    legacy_row: LegacyDeletionLedgerRow,
    tenant_id: str,
) -> LedgerIntent:
    """Map a legacy authorized_deletion `LedgerRow` to a unified
    `LedgerIntent`. Refuses rows whose data_class is not
    'authorized_deletion' (routes them away for structural role
    separation)."""
    stamp = legacy_row.stamp_audit or {}
    if not isinstance(stamp, Mapping):
        raise ValueError(
            f"LEDGER-W4D-001: deletion adapter refuses row {legacy_row.row_id!r} "
            f"with non-mapping stamp_audit."
        )
    data_class = stamp.get("data_class", "")
    if data_class != _AUTHORIZED_DELETION_DATA_CLASS:
        raise ValueError(
            f"LEDGER-W4D-002: deletion adapter refuses to replay row "
            f"(row_id={legacy_row.row_id!r}, data_class={data_class!r}); "
            f"only 'authorized_deletion' is in W4d scope. Route other "
            f"data_classes to their sub-wave adapter (countersign → W4b, "
            f"memory → W4e, etc.)."
        )
    held_class = stamp.get("held_class", "")
    return LedgerIntent(
        tenant_id=tenant_id,
        run_id=legacy_row.run_id,
        task_id=legacy_row.trace_id,
        actor_id=_LEGACY_DELETION_EMITTER_ACTOR_ID,
        actor_type="service",
        event_type=_DELETION_EVENT_TYPE,
        resource_type=legacy_row.artifact_ref.artifact_type,
        resource_id=legacy_row.artifact_ref.artifact_id,
        decision=_DELETION_DECISION,
        reason_code=held_class,
        payload_ref=legacy_deletion_payload_ref(legacy_row),
        at=LedgerRowAt(epoch_s=int(legacy_row.at.timestamp()), source="wall_clock"),
        break_glass_session_id=None,
    )


__all__ = [
    "legacy_deletion_canonical_bytes",
    "legacy_deletion_payload_ref",
    "replay_legacy_deletion_to_intent",
]
