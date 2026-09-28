"""services.audit_trail.overview — audit-trail Overview computation.

Reads REAL records with REFERENCE-NOT-COPY discipline (Design Law A8);
never fabricates data; every entry cites its on-disk `source_path`.

Sources (env-overridable per test seam):
  * CROSSING_RECEIPTS_DIR       → phase0/crossing_receipts/
  * NORTHENA_LEDGER_DIR         → phase0/northena_ledger/
  * DATA_CONNECTION_RECORDS_DIR → phase0/data_connection_records/
  * REGISTRY_FACTS_DIR          → phase0/registry_facts/
  * MEMORY_SERVICE_ROOT         → backend/services/memory/ (reference-only
                                  citation; the per-turn warm/fresh half
                                  lives here per owner ruling this session)

CA1 canon rows (verbatim from AKKI CANON — ADDENDUM 1 §1):
  * CA1-001 (Doc02-020a · Promise #4)
  * CA1-002 (Doc06-016 · Promise #17)
  * CA1-003 (Doc07-019 · Doc08-017 · Promises #19/#20/#21)

The strict "banned fields" set (Owner Order 2026-08-25 §4) filters
raw signing material out of every rendered entry.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List


# --- Verbatim canon text (Owner Standing Condition 1) -------------------

CA1_001_VERBATIM = (
    "Canon already fully specified the two-item custody split (Doc 2). "
    "Gap was build-only: no surface distinguished it. Closed by the "
    "audit trail Overview stating when an answer drew on 2+ "
    "independently-governed units."
)
CA1_002_VERBATIM = (
    "Canon already fully specified minimal-sufficient disclosure (Doc 6). "
    "Gap was build-only. Closed by the audit trail Overview stating how "
    "many available source units were actually served."
)
CA1_003_VERBATIM = (
    "Canon already fully specified the five-ring unit and warm/fresh "
    "fork (Docs 7-8). Gap was build-only. Closed by a Registry "
    "densification stat and a per-turn warm/fresh tag — flagged here "
    "as a partial closure, not a full one."
)


_DEFAULTS = {
    "crossing_receipts":        "/app/assessment_workspace/phase0/crossing_receipts",
    "northena_ledger":          "/app/assessment_workspace/phase0/northena_ledger",
    "data_connection_records":  "/app/assessment_workspace/phase0/data_connection_records",
    "registry_facts":           "/app/assessment_workspace/phase0/registry_facts",
}
_ENV_KEYS = {
    "crossing_receipts":        "CROSSING_RECEIPTS_DIR",
    "northena_ledger":          "NORTHENA_LEDGER_DIR",
    "data_connection_records":  "DATA_CONNECTION_RECORDS_DIR",
    "registry_facts":           "REGISTRY_FACTS_DIR",
}
_MEMORY_SERVICE_REFERENCE = (
    "backend/services/memory/ (per-turn warm/fresh tag half wires "
    "through by reference; owner ruling this session: 'the memory-"
    "service half already exists — wire it through')"
)

_BANNED_FIELDS = {
    "password", "secret", "signing_material", "aws_secret_access_key",
    "aws_secret", "api_key", "bearer", "token",
}


def _dir(kind: str) -> Path:
    return Path(os.environ.get(_ENV_KEYS[kind], _DEFAULTS[kind]))


def _sanitize(d: Dict[str, Any]) -> Dict[str, Any]:
    return {
        k: v for k, v in d.items()
        if k not in _BANNED_FIELDS and not k.endswith("_raw")
    }


def _load_json_dir(kind: str) -> List[Dict[str, Any]]:
    d = _dir(kind)
    if not d.is_dir():
        return []
    out: List[Dict[str, Any]] = []
    for p in sorted(d.glob("*.json")):
        try:
            body = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(body, dict):
            continue
        out.append({**_sanitize(body), "source_path": str(p)})
    return out


# --- CA1-001 · multi-unit answers (northena ledger group-by trace_id) ---

def _multi_unit_answers() -> Dict[str, Any]:
    """Answers that drew on 2+ independently-governed units.

    Group northena ledger rows by `trace_id`; count distinct
    `artifact_ref.artifact_id` per trace. A trace whose count ≥ 2 is
    an answer that drew on 2+ independently-governed units (CA1-001
    canon verbatim).
    """
    rows = _load_json_dir("northena_ledger")
    by_trace: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        tid = row.get("trace_id")
        if not tid:
            continue
        aref = row.get("artifact_ref") or {}
        aid = aref.get("artifact_id") if isinstance(aref, dict) else None
        if not aid:
            continue
        bucket = by_trace.setdefault(tid, {"units": set(), "first_at": None,
                                          "source_paths": []})
        bucket["units"].add(aid)
        at = row.get("at")
        if at and (bucket["first_at"] is None or at < bucket["first_at"]):
            bucket["first_at"] = at
        bucket["source_paths"].append(row["source_path"])

    entries: List[Dict[str, Any]] = []
    for tid, bucket in sorted(by_trace.items()):
        if len(bucket["units"]) < 2:
            continue
        entries.append({
            "trace_id": tid,
            "unit_count": len(bucket["units"]),
            "source_units": sorted(bucket["units"]),
            "first_at_iso": bucket["first_at"],
            "source_path": bucket["source_paths"][0],
        })

    return {
        "count": len(entries),
        "entries": entries,
        "canon_anchor": "Addendum §1 CA1-001 Promise #4 (Doc02-020a)",
        "canon_text": CA1_001_VERBATIM,
    }


# --- CA1-002 · units-served count (data-connection records vs crossing-receipts) ---

def _units_served() -> Dict[str, Any]:
    """How many available source units were actually served.

    * available = count of data-connection records on disk (each
      record is a declared, admissible source unit).
    * served   = distinct data sources touched by at least one
      crossing receipt (`payload_shape.database` or `resource.database`).
    * per-source served_receipts = touch count.
    """
    dcrs = _load_json_dir("data_connection_records")
    crs = _load_json_dir("crossing_receipts")

    # Available source units, keyed by database name (best available key
    # on data_connection_record shapes) with source_id + source_path.
    available_map: Dict[str, Dict[str, Any]] = {}
    for r in dcrs:
        res = r.get("resource") or {}
        db = (res.get("database") if isinstance(res, dict) else None) \
            or r.get("source_id")
        if not db:
            continue
        # Prefer the database sub-key when present so a single cluster
        # with N databases becomes N source units (Doc06 minimal-sufficient
        # grammar treats each database as a unit).
        key = db
        available_map.setdefault(key, {
            "source_id": r.get("source_id") or key,
            "database": key,
            "source_path": r["source_path"],
            "served_receipts": 0,
        })

    # Attribute each crossing receipt to its source unit (if present)
    # by matching `payload_shape.database` against the available map.
    for cr in crs:
        ps = cr.get("payload_shape") or {}
        db = ps.get("database") if isinstance(ps, dict) else None
        if not db or db not in available_map:
            continue
        available_map[db]["served_receipts"] += 1

    served_entries = [e for e in available_map.values()
                      if e["served_receipts"] > 0]
    return {
        "available": len(available_map),
        "served": len(served_entries),
        "entries": list(available_map.values()),
        "canon_anchor": "Addendum §1 CA1-002 Promise #17 (Doc06-016)",
        "canon_text": CA1_002_VERBATIM,
    }


# --- CA1-003 · Registry densification stat + warm/fresh reference ---

def _densification() -> Dict[str, Any]:
    """Registry densification stat + per-turn warm/fresh reference.

    Densification stat is the count of registered facts on disk.
    Warm/fresh tag is a reference-only wire-through per owner ruling
    ("the memory-service half already exists — wire it through").
    Canon flags this row as a partial closure, not a full one.
    """
    facts = _load_json_dir("registry_facts")
    return {
        "facts_registered": len(facts),
        "warm_fresh_reference": _MEMORY_SERVICE_REFERENCE,
        "partial_closure": True,
        "canon_anchor": (
            "Addendum §1 CA1-003 Promise #19/#20/#21 "
            "(Doc07-019 · Doc08-017)"
        ),
        "canon_text": CA1_003_VERBATIM,
    }


def compute_overview() -> Dict[str, Any]:
    """Assemble the audit-trail Overview body.

    REFERENCE-NOT-COPY posture: every entry carries `source_path` so
    an auditor walks back to the original record. The Overview itself
    renders IDs + short provenance + counts, never a record body.
    """
    return {
        "multi_unit_answers": _multi_unit_answers(),
        "units_served":       _units_served(),
        "densification":      _densification(),
        "sources": {
            "crossing_receipts":       str(_dir("crossing_receipts")),
            "northena_ledger":         str(_dir("northena_ledger")),
            "data_connection_records": str(_dir("data_connection_records")),
            "registry_facts":          str(_dir("registry_facts")),
            "memory_service":          _MEMORY_SERVICE_REFERENCE,
        },
        "reference_note": (
            "REFERENCE-NOT-COPY (Design Law A8) · every entry cites its "
            "on-disk source_path; the surface renders record ids + "
            "short provenance rather than embedding record bodies. "
            "Original records live under phase0/ where each producer "
            "wrote them. Canon anchors: Addendum §1 CA1-001 · CA1-002 · "
            "CA1-003 (partial-closure)."
        ),
    }
