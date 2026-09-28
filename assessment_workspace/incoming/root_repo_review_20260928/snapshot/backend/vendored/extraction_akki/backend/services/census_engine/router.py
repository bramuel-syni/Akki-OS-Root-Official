"""services.census_engine.router — Wave-G5c-CENSUS wire path.

Endpoints (product-shaped, plain sentences on failure):
  - GET  /api/census/records
  - GET  /api/census/latest
  - POST /api/census/run

Owner ruling F (banked in DECISIONS.md 2026-08-28T~14:30Z): product
language only. Never IPs, never auth vocab, never engineering vocab.
"""
from __future__ import annotations

import json
import logging
import os
import pathlib
import re
from typing import Any, Dict, List, Optional

from fastapi import APIRouter

from services.census_engine.engine import (
    CensusEstateNotConnected,
    run_census as _engine_run_census,
    _estate_creds,
)

log = logging.getLogger(__name__)

router = APIRouter()


# ---------------------------------------------------------------------------
# Records directory resolver — monkeypatchable for hermetic tests
# ---------------------------------------------------------------------------


def _records_dir() -> pathlib.Path:
    return pathlib.Path(os.environ.get(
        "CENSUS_RECORDS_DIR",
        "/app/assessment_workspace/phase0/census",
    ))


def _iter_run_dirs(records_dir: pathlib.Path) -> List[pathlib.Path]:
    if not records_dir.is_dir():
        return []
    out = []
    pat = re.compile(r"^census_(\d{4,})$")
    for p in records_dir.iterdir():
        if p.is_dir() and pat.match(p.name):
            out.append(p)
    # Newest first.
    out.sort(key=lambda p: int(pat.match(p.name).group(1)), reverse=True)
    return out


def _load_manifest(run_dir: pathlib.Path) -> Optional[Dict[str, Any]]:
    mf = run_dir / "manifest.json"
    if not mf.is_file():
        return None
    try:
        return json.loads(mf.read_text())
    except (OSError, json.JSONDecodeError):
        return None


# ---------------------------------------------------------------------------
# Live-run entrypoint indirection (monkeypatched by tests)
# ---------------------------------------------------------------------------


def _run_census_or_raise() -> Dict[str, Any]:
    """Resolve estate credentials + build a real boto3 rds-data client +
    delegate to the engine. Raises CensusEstateNotConnected when the
    estate has not been commissioned.

    In hermetic tests, the router monkeypatches this whole function to
    a fake — so no boto3 client is constructed there.

    Live-run env discipline (mirrors services.connect.rds_data_submit):
      1. Snapshot prior AWS_* env vars.
      2. Set AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_DEFAULT_REGION
         from the estate credentials file for the duration of the call.
      3. Build client through the chokepoint-exempted seam helper.
      4. Restore prior env on `finally` — either back to snapshot or unset.

    Wave-G5c-CENSUS · owner ruling 2026-08-28T~15:00Z (banked in DECISIONS.md).
    The boto3 client is obtained through services.connect.rds_data_submit
    (the only chokepoint-exempted boto3 seam per Doc 01 §A5.5 — see
    tests/invariants/test_chokepoint_registers_all_crossings.py).
    """
    import os as _os
    triple = _estate_creds()
    # Import lazily inside the function AND go through the exempted seam
    # helper so census_engine never carries a boto3 import at module scope.
    from services.connect.rds_data_submit import get_rds_data_client

    prior = {
        k: _os.environ.get(k)
        for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY",
                  "AWS_DEFAULT_REGION")
    }
    try:
        if triple.get("aws_access_key_id"):
            _os.environ["AWS_ACCESS_KEY_ID"] = triple["aws_access_key_id"]
        if triple.get("aws_secret_access_key"):
            _os.environ["AWS_SECRET_ACCESS_KEY"] = triple["aws_secret_access_key"]
        _os.environ["AWS_DEFAULT_REGION"] = triple["region"]

        client = get_rds_data_client(triple["region"])
        return _engine_run_census(
            client=client,
            cluster_arn=triple["cluster_arn"],
            secret_arn=triple["secret_arn"],
            region=triple["region"],
            records_dir=_records_dir(),
            initiator="owner",
            database_hint=triple.get("database", "") or "",
        )
    finally:
        for k, v in prior.items():
            if v is None:
                _os.environ.pop(k, None)
            else:
                _os.environ[k] = v


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/api/census/latest")
async def get_census_latest() -> Dict[str, Any]:
    """Return the most recent census manifest, or an honest-empty reason.

    Numbering starts at 1 (owner ruling 3). If no census has been run
    yet, the response is `{"census": null, "reason": "..."}`.
    """
    runs = _iter_run_dirs(_records_dir())
    for r in runs:
        m = _load_manifest(r)
        if m is not None:
            return {"census": m, "reason": ""}
    return {
        "census": None,
        "reason": (
            "No census has been run yet. The census walker will read the "
            "estate at the seam and record what it holds; until then the "
            "Registry surface stays honest-empty."
        ),
    }


@router.get("/api/census/records")
async def get_census_records() -> Dict[str, Any]:
    """Return a list of persisted census run summaries, newest first."""
    runs = _iter_run_dirs(_records_dir())
    records: List[Dict[str, Any]] = []
    for r in runs:
        m = _load_manifest(r)
        if m is None:
            continue
        records.append({
            "census_id": m.get("census_id"),
            "started_at_utc": m.get("started_at_utc"),
            "finished_at_utc": m.get("finished_at_utc"),
            "database_count": (m.get("rollup") or {}).get("database_count", 0),
            "table_count": (m.get("rollup") or {}).get("table_count", 0),
        })
    reason = "" if records else (
        "No census has been run yet. The census walker will record its "
        "reads under phase0/census/ and this list will fill in from there."
    )
    return {"records": records, "reason": reason}


@router.post("/api/census/run")
async def post_census_run() -> Dict[str, Any]:
    """Trigger a live census run.

    On success: `{census_id, database_count, table_count, reason: ""}`.
    On honest failure (estate not connected yet): `{census_id: null,
    database_count: 0, table_count: 0, reason: "<plain sentence>"}`.
    Never returns a stack trace; product language only.
    """
    try:
        manifest = _run_census_or_raise()
    except CensusEstateNotConnected:
        return {
            "census_id": None,
            "database_count": 0,
            "table_count": 0,
            "reason": (
                "The estate is not yet connected for a live census. "
                "Register a data source through Connect first; the "
                "Registry will pick up the run automatically once it lands."
            ),
        }
    except Exception:  # pragma: no cover — never surfaces the trace
        log.exception("census run failed")
        return {
            "census_id": None,
            "database_count": 0,
            "table_count": 0,
            "reason": (
                "The census run did not complete. The Registry stays on "
                "its last recorded reading; an operator can retry the run."
            ),
        }
    rollup = manifest.get("rollup") or {}
    return {
        "census_id": manifest.get("census_id"),
        "database_count": rollup.get("database_count", 0),
        "table_count": rollup.get("table_count", 0),
        "reason": "",
    }
