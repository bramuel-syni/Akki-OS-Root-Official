"""services.ledger_writer.writers.countersign — M10-W4b · countersign
writer consolidation replay adapter (second sub-wave of Milestone 2).

Owner Run Order 2026-09-18T~21:15Z (verbatim, banked in STATE/DECISIONS.md):
    "Milestone 2 · M10-W4 · writer consolidation: refusal → countersign
     → northena → deletion → memory. Per-writer replay test PASSING is
     precondition to landing that writer (legacy row-hash reproduction ·
     zero rows lost). Legacy stores go read-only at cutover · never
     rewritten."

This module folds the legacy `contracts.northena_ledger.LedgerRow`
countersigned-rule-change row shape — emitted by
`services.checker.countersign_ledger.emit_countersign_ledger_row` via
`services.compliance.deletion_ledger.emit_deletion_ledger_row` (Mongo
`insert_one` into the Northena collection) — into the unified
`contracts.ledger_v1.LedgerRow_v1` 17-field hash-chained row emitted
via `services.ledger_writer.main.append_intent`.

Contract:

  `legacy_countersign_canonical_bytes(legacy_row) -> bytes`:
      Deterministic canonical UTF-8 JSON over every field of the legacy
      countersign row. Row-hash reproduction primitive.

  `legacy_countersign_payload_ref(legacy_row) -> str`:
      `sha256(legacy_countersign_canonical_bytes(row)).hexdigest()`.
      Anchors a unified `LedgerRow_v1` to its legacy source via
      `payload_ref` — zero information lost.

  `replay_legacy_countersign_to_intent(legacy_row, tenant_id) -> LedgerIntent`:
      Maps a legacy countersign row to a unified `LedgerIntent`:
        - `tenant_id`:           caller-supplied (legacy rows carry no tenant_id)
        - `run_id`:              legacy_row.run_id
        - `task_id`:             legacy_row.trace_id
        - `actor_id`:            "service:checker_countersign_ledger"
        - `actor_type`:          "service"
        - `event_type`:          "countersign"
        - `resource_type`:       legacy_row.artifact_ref.artifact_type
        - `resource_id`:         legacy_row.artifact_ref.artifact_id
        - `decision`:            "continue"  (mirrors legacy neutral placeholder · Amendment C)
        - `reason_code`:         legacy_row.stamp_audit["consequence_class"]
        - `payload_ref`:         legacy_countersign_payload_ref(legacy_row)
        - `at`:                  LedgerRowAt(epoch_s=int(row.at.timestamp()),
                                             source="wall_clock")
        - `break_glass_session_id`: None

      Deterministic and idempotent.

Structural discipline (owner mandate 'Legacy stores go read-only at
cutover · never rewritten'), AST-enforced by the invariant suite:

  * This module does NOT import `services.checker.countersign_ledger`
    (the legacy checker emitter surface).
  * This module does NOT import `services.compliance.deletion_ledger`
    (the legacy internal Mongo write surface that persists the row via
    `insert_one`).
  * This module DOES import `LedgerIntent` from
    `services.ledger_emitter.emit_intent` (the sole unified-writer
    intent-producer surface).

M3 forward-compat: the `LedgerIntent` produced by this adapter carries
NO `confidence` / `score` / `strength` / `probability` field (the
unified intent shape frozen at M10-CLOSE already structurally excludes
them per B-M10-Q1). The countersign writer inherits that discipline by
construction.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from contracts.ledger_v1 import LedgerRowAt
from contracts.northena_ledger import LedgerRow as LegacyCountersignLedgerRow
from services.ledger_emitter.emit_intent import LedgerIntent


_LEGACY_COUNTERSIGN_EMITTER_ACTOR_ID = "service:checker_countersign_ledger"
_COUNTERSIGN_EVENT_TYPE = "countersign"
_COUNTERSIGN_DECISION = "continue"  # mirrors legacy neutral placeholder · Amendment C


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


def legacy_countersign_canonical_bytes(
    legacy_row: LegacyCountersignLedgerRow,
) -> bytes:
    """Deterministic canonical UTF-8 JSON over every field of the legacy
    countersign row (row-hash reproduction primitive).

    Serialisation is `json.dumps(payload, sort_keys=True, separators=(",", ":"))`
    with fields sorted by key. Datetime `at` is serialised as ISO-8601
    with timezone (utc-normalised)."""
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


def legacy_countersign_payload_ref(legacy_row: LegacyCountersignLedgerRow) -> str:
    """sha256_hex of `legacy_countersign_canonical_bytes(legacy_row)`.

    Anchors a unified `LedgerRow_v1` to its legacy source via
    `payload_ref` — the row-hash reproduction property owner requires
    for M10-W4 admission.
    """
    return hashlib.sha256(legacy_countersign_canonical_bytes(legacy_row)).hexdigest()


def replay_legacy_countersign_to_intent(
    *,
    legacy_row: LegacyCountersignLedgerRow,
    tenant_id: str,
) -> LedgerIntent:
    """Map a legacy countersign `LedgerRow` to a unified `LedgerIntent`.

    Deterministic and idempotent (`replay(x) == replay(x)` for any x).

    `consequence_class` is read from
    `legacy_row.stamp_audit['consequence_class']` (the §8 consequence
    class · H/M/L). Absence yields empty `reason_code` (unified schema
    admits open str).
    """
    stamp = legacy_row.stamp_audit or {}
    consequence_class = (
        stamp.get("consequence_class", "") if isinstance(stamp, Mapping) else ""
    )
    return LedgerIntent(
        tenant_id=tenant_id,
        run_id=legacy_row.run_id,
        task_id=legacy_row.trace_id,
        actor_id=_LEGACY_COUNTERSIGN_EMITTER_ACTOR_ID,
        actor_type="service",
        event_type=_COUNTERSIGN_EVENT_TYPE,
        resource_type=legacy_row.artifact_ref.artifact_type,
        resource_id=legacy_row.artifact_ref.artifact_id,
        decision=_COUNTERSIGN_DECISION,
        reason_code=consequence_class,
        payload_ref=legacy_countersign_payload_ref(legacy_row),
        at=LedgerRowAt(epoch_s=int(legacy_row.at.timestamp()), source="wall_clock"),
        break_glass_session_id=None,
    )


__all__ = [
    "legacy_countersign_canonical_bytes",
    "legacy_countersign_payload_ref",
    "replay_legacy_countersign_to_intent",
]
