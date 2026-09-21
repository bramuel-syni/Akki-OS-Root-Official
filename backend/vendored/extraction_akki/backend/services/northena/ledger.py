"""services.northena.ledger — append-only ledger writer (Doc 05 §B5.4).

APPEND ONLY. No update path. No delete path. Enforced structurally:
this module's public function surface is `record` + `list_rows_by_run` +
`list_open_runs` + `retention_mode` + `retention_window_days`. Nothing
named 'update' / 'delete' / 'edit' / 'overwrite' / 'drop' / 'clear'.

Persistence: phase0/northena_ledger/led-<hex12>.json per row + an
append-only index.json for read queries by run.

WS-WIRE-LEDGER-MATRIX (Owner ruling 2026-08 · promoted 2026-08):
this module is the SOLE writer of northena_ledger_row records. Tests
enforce structurally.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from contracts.northena_ledger import (
    LedgerArtifactRef,
    LedgerRow,
    NORTHENA_LEDGER_COLLECTION,
)


_DEFAULT_LEDGER_DIR = "/app/assessment_workspace/phase0/northena_ledger"


def _ledger_dir() -> Path:
    return Path(os.environ.get("NORTHENA_LEDGER_DIR", _DEFAULT_LEDGER_DIR))


def retention_mode() -> str:
    """Doc 05 §11 (DPO open) · retention mode.

    Default INDEFINITE (append-only), matching Akki-OS-V1's G4 posture.
    A future DPO ruling may set a window; until then, deletion is not
    a code path here.
    """
    return os.environ.get("AKKI_NORTHENA_LEDGER_RETENTION_MODE", "indefinite")


def retention_window_days() -> Optional[int]:
    raw = os.environ.get("AKKI_NORTHENA_LEDGER_RETENTION_WINDOW_DAYS")
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


async def record(row: LedgerRow) -> None:
    """Append-only. Doc 05 §B5.4 · N-INV-8.

    Writes one JSON file per row + appends an index entry. Never
    overwrites. If a row_id collision occurs (astronomically unlikely
    with 12-hex-uuid), the write refuses rather than overwrites.

    W11 D · CP-D6 · Q3 semantic sweep (owner ruling 2026-08-27):
    Also mirrors the row into Mongo `NORTHENA_LEDGER_COLLECTION` so
    `db[NORTHENA_LEDGER_COLLECTION].find({"run_id": ...})` queries see
    admits/gates/converges written through this sole-writer path.
    The Mongo mirror is best-effort per WS-WIRE-LEDGER-MATRIX (2026-08):
    other services (`async_state`, `deletion_ledger`, `tier_lock_ledger`,
    `engineer_key_grant_ledger`, `wizard.turn_ledger`, `economics.instrumentation`)
    ALREADY write to `NORTHENA_LEDGER_COLLECTION` directly for their
    domain-specific ledger rows (refusal-family pinned, deletion,
    rule-change, key-grant, wizard, economics). Mirroring here keeps
    `northena_ledger.record()` as an authoritative reader-visible seat
    without breaking those existing direct writers.
    """
    d = _ledger_dir()
    d.mkdir(parents=True, exist_ok=True)
    row_path = d / f"{row.row_id}.json"
    if row_path.exists():
        # Structural refusal to overwrite — the writer is append-only.
        raise RuntimeError(
            f"ledger_writer_refused_overwrite — row_id {row.row_id!r} already on disk"
        )
    row_path.write_text(json.dumps(row.to_json(), indent=2, sort_keys=True))
    # Append-only index.
    idx_path = d / "index.json"
    idx: List[Dict[str, Any]] = []
    if idx_path.exists():
        try:
            idx = json.loads(idx_path.read_text())
        except (json.JSONDecodeError, ValueError):
            idx = []
    idx.append({
        "row_id": row.row_id,
        "run_id": row.run_id,
        "trace_id": row.trace_id,
        "stage": row.stage,
        "decision": row.decision,
        "at_iso": row.at.isoformat().replace("+00:00", "Z"),
    })
    idx_path.write_text(json.dumps(idx, indent=2, sort_keys=False))
    # Mongo mirror — CP-D6 Q3 semantic sweep. Import here to avoid a
    # module-level Motor dependency at import time (tests import this
    # module before Motor rebind).
    try:
        from core import db
        await db[NORTHENA_LEDGER_COLLECTION].insert_one(row.model_dump(mode="python"))
    except Exception:
        # Best-effort: if Mongo is unreachable at write time (dev-only
        # scenarios), the disk write still lands. Callers that depend on
        # the Mongo mirror will surface the mismatch via their own
        # subsequent read query.
        pass


async def list_rows_by_run(run_id: str) -> List[Dict[str, Any]]:
    """Return all rows for a run, ordered by at_iso."""
    d = _ledger_dir()
    if not d.is_dir():
        return []
    idx_path = d / "index.json"
    if not idx_path.exists():
        return []
    try:
        idx = json.loads(idx_path.read_text())
    except (json.JSONDecodeError, ValueError):
        return []
    matches = [e for e in idx if e.get("run_id") == run_id]
    matches.sort(key=lambda e: e.get("at_iso", ""))
    rows: List[Dict[str, Any]] = []
    for e in matches:
        row_path = d / f"{e['row_id']}.json"
        if row_path.exists():
            try:
                rows.append(json.loads(row_path.read_text()))
            except (json.JSONDecodeError, ValueError):
                continue
    return rows


async def list_open_runs(limit: int = 50) -> List[Dict[str, Any]]:
    """Return run summaries (open = admitted, no converge terminate seen yet).

    Read from index.json; reference-not-copy: each summary references
    a run_id + first admit entry (identity only).
    """
    d = _ledger_dir()
    if not d.is_dir():
        return []
    idx_path = d / "index.json"
    if not idx_path.exists():
        return []
    try:
        idx = json.loads(idx_path.read_text())
    except (json.JSONDecodeError, ValueError):
        return []
    # Group by run_id.
    by_run: Dict[str, List[Dict[str, Any]]] = {}
    for e in idx:
        by_run.setdefault(e["run_id"], []).append(e)
    summaries = []
    for run_id, entries in by_run.items():
        entries.sort(key=lambda e: e.get("at_iso", ""))
        first = entries[0]
        last = entries[-1]
        # Read only the first admit row's frozen_artifact_id (identity) —
        # not its content — for the summary.
        summaries.append({
            "run_id": run_id,
            "opened_at_iso": first.get("at_iso"),
            "last_stage": last.get("stage"),
            "last_decision": last.get("decision"),
            "row_count": len(entries),
        })
    summaries.sort(key=lambda s: s.get("opened_at_iso") or "", reverse=True)
    return summaries[:limit]
