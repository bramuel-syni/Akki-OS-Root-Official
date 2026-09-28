"""services.ledger_writer.writers.memory — M10-W4e · memory writer
consolidation replay adapter (FINAL sub-wave of Milestone 2).

Owner Run Order 2026-09-18T~21:15Z (verbatim, banked in STATE/DECISIONS.md):
    "Milestone 2 · M10-W4 · writer consolidation: refusal → countersign
     → northena → deletion → memory. Per-writer replay test PASSING is
     precondition to landing that writer (legacy row-hash reproduction ·
     zero rows lost). Legacy stores go read-only at cutover · never
     rewritten."

This module folds the legacy `contracts.northena_ledger.LedgerRow`
memory_* row shape — emitted by the seven memory-ledger emitters in
`services.memory.ledger` (emit_plane_issued, emit_contribution_landed,
emit_contribution_refused, emit_publication_attempted,
emit_publication_landed, emit_publication_refused, emit_plane_revoked),
each wrapping `services.compliance.deletion_ledger.emit_deletion_ledger_row`
with a `memory_*` data_class from `data_class_registry.v4.json` (v4
governed registry version bump per Owner ruling 2026-07-30/31) — into
the unified `contracts.ledger_v1.LedgerRow_v1` 17-field hash-chained row
via `services.ledger_writer.main.append_intent`.

Data-class scope: any value with `memory_` prefix. Rows with non-memory
data_class raise `ValueError` (LEDGER-W4E-002) — structural role
separation with W4b (countersign) and W4d (authorized_deletion).

Contract:

  `legacy_memory_canonical_bytes(legacy_row) -> bytes`:
      Deterministic canonical UTF-8 JSON.

  `legacy_memory_payload_ref(legacy_row) -> str`:
      `sha256(legacy_memory_canonical_bytes(row)).hexdigest()`.

  `replay_legacy_memory_to_intent(legacy_row, tenant_id) -> LedgerIntent`:
      Maps a legacy memory_* row to a unified `LedgerIntent`:
        - `tenant_id`:           caller-supplied
        - `run_id`:              legacy_row.run_id
        - `task_id`:             legacy_row.trace_id
        - `actor_id`:            "service:memory_ledger"
        - `actor_type`:          "service"
        - `event_type`:          "memory"
        - `resource_type`:       legacy_row.artifact_ref.artifact_type
        - `resource_id`:         legacy_row.artifact_ref.artifact_id
        - `decision`:            "continue"  (mirrors legacy neutral placeholder)
        - `reason_code`:         legacy_row.stamp_audit["data_class"].removeprefix("memory_")
        - `payload_ref`:         legacy_memory_payload_ref(legacy_row)
        - `at`:                  LedgerRowAt(wall_clock · int(row.at.timestamp()))
        - `break_glass_session_id`: None

      Refuses (ValueError) if stamp_audit['data_class'] lacks 'memory_' prefix.

Structural discipline (AST-enforced): does NOT import
`services.memory.ledger` (memory emitter facade) nor
`services.compliance.deletion_ledger` (underlying Mongo write path).
DOES import `LedgerIntent` from `services.ledger_emitter.emit_intent`.

Canon anchors: Canon 1 §71 (data class not sibling ledger — memory
remains on the unified append-only ledger, plurality via data_class) +
Canon 3 §9.3 (append-only).
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from contracts.ledger_v1 import LedgerRowAt
from contracts.northena_ledger import LedgerRow as LegacyMemoryLedgerRow
from services.ledger_emitter.emit_intent import LedgerIntent


_LEGACY_MEMORY_EMITTER_ACTOR_ID = "service:memory_ledger"
_MEMORY_EVENT_TYPE = "memory"
_MEMORY_DECISION = "continue"
_MEMORY_DATA_CLASS_PREFIX = "memory_"


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


def legacy_memory_canonical_bytes(
    legacy_row: LegacyMemoryLedgerRow,
) -> bytes:
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


def legacy_memory_payload_ref(legacy_row: LegacyMemoryLedgerRow) -> str:
    return hashlib.sha256(legacy_memory_canonical_bytes(legacy_row)).hexdigest()


def replay_legacy_memory_to_intent(
    *,
    legacy_row: LegacyMemoryLedgerRow,
    tenant_id: str,
) -> LedgerIntent:
    """Map a legacy memory_* `LedgerRow` to a unified `LedgerIntent`.
    Refuses rows whose data_class lacks 'memory_' prefix."""
    stamp = legacy_row.stamp_audit or {}
    if not isinstance(stamp, Mapping):
        raise ValueError(
            f"LEDGER-W4E-001: memory adapter refuses row {legacy_row.row_id!r} "
            f"with non-mapping stamp_audit."
        )
    data_class = stamp.get("data_class", "")
    if not data_class.startswith(_MEMORY_DATA_CLASS_PREFIX):
        raise ValueError(
            f"LEDGER-W4E-002: memory adapter refuses to replay row "
            f"(row_id={legacy_row.row_id!r}, data_class={data_class!r}); "
            f"only 'memory_*' data_classes are in W4e scope. Route other "
            f"data_classes to their sub-wave adapter (authorized_deletion "
            f"→ W4d, countersigned_rule_change → W4b, etc.)."
        )
    reason_code = data_class[len(_MEMORY_DATA_CLASS_PREFIX):]
    return LedgerIntent(
        tenant_id=tenant_id,
        run_id=legacy_row.run_id,
        task_id=legacy_row.trace_id,
        actor_id=_LEGACY_MEMORY_EMITTER_ACTOR_ID,
        actor_type="service",
        event_type=_MEMORY_EVENT_TYPE,
        resource_type=legacy_row.artifact_ref.artifact_type,
        resource_id=legacy_row.artifact_ref.artifact_id,
        decision=_MEMORY_DECISION,
        reason_code=reason_code,
        payload_ref=legacy_memory_payload_ref(legacy_row),
        at=LedgerRowAt(epoch_s=int(legacy_row.at.timestamp()), source="wall_clock"),
        break_glass_session_id=None,
    )


__all__ = [
    "legacy_memory_canonical_bytes",
    "legacy_memory_payload_ref",
    "replay_legacy_memory_to_intent",
]
