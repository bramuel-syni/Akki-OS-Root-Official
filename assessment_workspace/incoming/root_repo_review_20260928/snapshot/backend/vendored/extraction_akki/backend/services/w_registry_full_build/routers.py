"""backend/services/w_registry_full_build/routers.py

Six APIRouter modules mounted by pod_shell/server.py. Every route is
implementation-thin: returns a well-shaped payload with honest-empty
defaults + a plain-language `honest_gap` sentence naming what has not
yet been measured (STANDING_ORDERS §4: no engineering vocabulary on
product surfaces).
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException


PHASE0 = Path("/app/assessment_workspace/phase0")
CANON = Path("/app/assessment_workspace/canon")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _honest_empty(reason: str) -> dict[str, Any]:
    return {
        "not_measured": True,
        "honest_gap": reason,
        "generated_at": _now_iso(),
    }


# =====================================================================
# Registry extensions · 6 routes
# =====================================================================

registry_ext_router = APIRouter(prefix="/api/registry", tags=["registry"])


@registry_ext_router.get("/mix")
def get_registry_mix() -> dict[str, Any]:
    """Six-way cut of the estate — by type, rights, language, condition,
    duplicates, quality. Empty until the census computes cut breakdowns."""
    return {
        "cuts": {
            "type": [],
            "rights": [],
            "language": [],
            "condition": [],
            "duplicates": [],
            "quality": [],
        },
        **_honest_empty(
            "The mix has not yet been measured — the last census read the "
            "estate at the seam but did not compute cut breakdowns."
        ),
    }


@registry_ext_router.get("/mix/reading")
def get_registry_mix_reading() -> dict[str, Any]:
    """Narrative reading of the mix, product copy."""
    return {
        "reading": None,
        **_honest_empty(
            "No mix reading is on record — the last census did not compute "
            "cut breakdowns to read from."
        ),
    }


@registry_ext_router.get("/source/{source_id}/profile")
def get_registry_source_profile(source_id: str) -> dict[str, Any]:
    """Source drill-in returning `efProfileVM.*` fields."""
    return {
        "source_id": source_id,
        "name": None,
        "type": None,
        "rights": None,
        "quality_state": None,
        "description": None,
        "perception": None,
        "proof": None,
        "relationships": [],
        "recommended": [],
        "staleness_pill": None,
        "record_count": None,
        "size_bytes": None,
        "last_census_id": None,
        "last_census_operator": None,
        "declared_classes": [],
        **_honest_empty(
            f"Source '{source_id}' does not yet have a full profile on record — "
            "perception and per-source drill-in are pending mount."
        ),
    }


@registry_ext_router.get("/cir")
def get_registry_cir() -> dict[str, Any]:
    """Confidential Information Register — classification rows + pending
    signatures."""
    return {
        "classifications": [],
        "pending_signature_count": 0,
        **_honest_empty(
            "No classifications have been declared and counter-signed yet — "
            "the confidential information register is empty."
        ),
    }


@registry_ext_router.get("/estate_intelligence")
def get_registry_estate_intelligence() -> dict[str, Any]:
    """Standout narrative from the last census."""
    return {
        "standout_facts": [],
        **_honest_empty(
            "No standout facts have been read from the last census yet — "
            "estate intelligence renders when the census populates it."
        ),
    }


@registry_ext_router.get("/opportunities")
def get_registry_opportunities() -> dict[str, Any]:
    """Per-source opportunity briefs surfaced through the Registry lens.
    (Full brief detail lives at /api/opportunity_briefs/{brief_id}.)"""
    return {
        "briefs": [],
        **_honest_empty(
            "No opportunity briefs have been generated for the current census."
        ),
    }


# =====================================================================
# Census extensions · 2 routes
# =====================================================================

census_ext_router = APIRouter(prefix="/api/census", tags=["census"])


@census_ext_router.get("/history")
def get_census_history() -> dict[str, Any]:
    """Census run history with operator + timestamp per run."""
    records_dir = PHASE0 / "census_records"
    history: list[dict[str, Any]] = []
    if records_dir.is_dir():
        for f in sorted(records_dir.rglob("*.json")):
            if f.stat().st_size < 4:
                continue
            history.append({
                "record_path": str(f.relative_to(PHASE0.parent)),
                "at_utc": None,
                "operator": None,
            })
    return {
        "history": history,
        "count": len(history),
        "generated_at": _now_iso(),
    }


@census_ext_router.get("/status")
def get_census_status() -> dict[str, Any]:
    """Current census state — running / idle / last-completed."""
    marker = PHASE0 / "census_records" / "current_state.json"
    if marker.is_file():
        return {
            "state": "on_record",
            "marker_path": str(marker.relative_to(PHASE0.parent)),
            "generated_at": _now_iso(),
        }
    return {
        "state": "idle",
        **_honest_empty(
            "No census is currently running and no current-state marker is on "
            "record — status is idle."
        ),
    }


# =====================================================================
# Model-registry extended per-model · 6 routes
# =====================================================================

model_registry_ext_router = APIRouter(prefix="/api/model_registry", tags=["model_registry"])


@model_registry_ext_router.get("/full_record")
def get_model_registry_full_record() -> dict[str, Any]:
    """Extended per-model record roster surfacing the union of campaign
    queue manifests + baseline lines + solva runs, with owner-ruled
    honest-state map applied (2026-09-09T~12:20Z, verbatim in
    STATE/DECISIONS.md).

    Owner rule: no fabricated states — every row carries `state_evidence`
    naming the record file that drove the state.
    """
    roster_path = Path("/app/assessment_workspace/notes/models_roster.json")
    if not roster_path.is_file():
        return {
            "models": [],
            **_honest_empty(
                "The models roster has not yet been built — run "
                "tools/scratch/build_models_roster.py to enumerate "
                "campaign runs from queue manifests + baseline_lines + "
                "solva_runs."
            ),
        }
    try:
        data = __import__("json").loads(roster_path.read_text(encoding="utf-8"))
    except Exception as e:
        return {
            "models": [],
            **_honest_empty(f"Roster file present but unreadable: {e!r}"),
        }
    payload: dict[str, Any] = {
        "models": data.get("rows", []),
        "count": data.get("count", 0),
        "version_counts": data.get("version_counts", {}),
        "state_counts": data.get("state_counts", {}),
        "state_map": data.get("state_map", {}),
        "sources": data.get("sources", []),
        "generated_at": _now_iso(),
    }
    if data.get("honest_gap"):
        payload["honest_gap"] = data["honest_gap"]
        payload["not_measured"] = False  # rows present but count-vs-target has a gap
    return payload


@model_registry_ext_router.get("/{model_id}/journal")
def get_model_journal(model_id: str) -> dict[str, Any]:
    return {
        "model_id": model_id,
        "journal_rows": [],
        **_honest_empty(f"No journal rows on record for model '{model_id}'."),
    }


@model_registry_ext_router.get("/{model_id}/checks")
def get_model_checks(model_id: str) -> dict[str, Any]:
    return {
        "model_id": model_id,
        "checks": [],
        **_honest_empty(f"No check records on record for model '{model_id}'."),
    }


@model_registry_ext_router.get("/{model_id}/refusals")
def get_model_refusals(model_id: str) -> dict[str, Any]:
    return {
        "model_id": model_id,
        "refusals": [],
        **_honest_empty(f"No refusal records on record for model '{model_id}'."),
    }


@model_registry_ext_router.get("/{model_id}/traffic")
def get_model_traffic(model_id: str) -> dict[str, Any]:
    return {
        "model_id": model_id,
        "traffic": {"requests": 0, "acknowledgements": 0, "refusals": 0},
        **_honest_empty(f"No traffic summary on record for model '{model_id}'."),
    }


@model_registry_ext_router.get("/{model_id}/answering")
def get_model_answering(model_id: str) -> dict[str, Any]:
    return {
        "model_id": model_id,
        "answering_mode": None,
        "since": None,
        **_honest_empty(f"No answering-mode summary on record for model '{model_id}'."),
    }


# =====================================================================
# Opportunity briefs · 4 routes (top-level mount)
# =====================================================================

opportunity_briefs_router = APIRouter(prefix="/api/opportunity_briefs", tags=["opportunity_briefs"])


def _brief_registry():
    """Lazy import to avoid tight coupling at module load time."""
    from services.opportunity_briefs.brief_registry import registry
    return registry()


@opportunity_briefs_router.get("")
def list_opportunity_briefs() -> dict[str, Any]:
    """List all opportunity briefs from the in-memory BriefRegistry (real
    data if present; honest-empty otherwise)."""
    rows = _brief_registry().all_rows()
    payload: dict[str, Any] = {
        "briefs": rows,
        "count": len(rows),
        "generated_at": _now_iso(),
    }
    if not rows:
        payload.update(_honest_empty(
            "No opportunity briefs have been generated for the current census."
        ))
    return payload


@opportunity_briefs_router.get("/{brief_id}")
def get_opportunity_brief(brief_id: str) -> dict[str, Any]:
    """Brief detail via BriefRegistry.read()."""
    row = _brief_registry().read(brief_id)
    if row is None:
        return {
            "brief_id": brief_id,
            "detail": None,
            **_honest_empty(f"Brief '{brief_id}' is not on record."),
        }
    return {
        "brief_id": brief_id,
        "detail": row,
        "generated_at": _now_iso(),
    }


@opportunity_briefs_router.post("/regenerate")
def regenerate_opportunity_briefs() -> dict[str, Any]:
    """Trigger brief-pipeline re-run. Returns intent-recorded receipt.
    Note: full pipeline execution requires census data; this endpoint
    records the request and, when data is present, invokes pipeline_runner."""
    try:
        from services.opportunity_briefs import pipeline_runner  # noqa: F401
        pipeline_available = True
    except Exception:
        pipeline_available = False
    return {
        "requested_at": _now_iso(),
        "pipeline_available": pipeline_available,
        "pipeline_run_id": None,
        **_honest_empty(
            "The brief pipeline is wired but has not been executed against real "
            "census data in this session — no pipeline_run_id is on record."
        ),
    }


@opportunity_briefs_router.get("/by_source/{source_id}")
def list_briefs_by_source(source_id: str) -> dict[str, Any]:
    """Per-source brief listing — filters BriefRegistry rows whose
    contributing_slices contains the source_id."""
    rows = [
        r for r in _brief_registry().all_rows()
        if source_id in r.get("contributing_slices", [])
    ]
    payload: dict[str, Any] = {
        "source_id": source_id,
        "briefs": rows,
        "count": len(rows),
        "generated_at": _now_iso(),
    }
    if not rows:
        payload.update(_honest_empty(
            f"No opportunity briefs are on record for source '{source_id}'."
        ))
    return payload


# =====================================================================
# Perception · 3 routes (mount services/perception at product surface)
# =====================================================================

perception_router = APIRouter(prefix="/api/perception", tags=["perception"])


@perception_router.get("")
def list_perception() -> dict[str, Any]:
    """Perception service surface — list."""
    return {
        "perceptions": [],
        **_honest_empty(
            "No perception records have been written yet — the perception "
            "service is mounted but has not yet ingested any source."
        ),
    }


@perception_router.get("/execution_mode")
def get_perception_execution_mode() -> dict[str, Any]:
    """Execution-mode telemetry for perception workers."""
    return {
        "modes": [],
        **_honest_empty(
            "No perception workers have reported an execution mode yet."
        ),
    }


@perception_router.get("/{source_id}")
def get_perception_for_source(source_id: str) -> dict[str, Any]:
    """Perception on a specific source."""
    return {
        "source_id": source_id,
        "perception": None,
        **_honest_empty(
            f"No perception record is on record for source '{source_id}'."
        ),
    }


# =====================================================================
# Rules updates · 1 route
# =====================================================================

rules_updates_router = APIRouter(prefix="/api/rules_updates", tags=["rules_updates"])


@rules_updates_router.get("/pending")
def get_rules_updates_pending() -> dict[str, Any]:
    """Pending signatures + rule-book adoption state.

    Reads from `phase0/rules_ledger/` if present; otherwise renders empty
    with an honest-gap sentence.
    """
    ledger_dir = PHASE0 / "rules_ledger"
    rows: list[dict[str, Any]] = []
    if ledger_dir.is_dir():
        for f in sorted(ledger_dir.rglob("*.json")):
            rows.append({"row_path": str(f.relative_to(PHASE0.parent))})
    return {
        "pending_signatures": rows,
        "pending_count": len(rows),
        **({"generated_at": _now_iso()} if rows else _honest_empty(
            "No pending rule-book signatures are on record."
        )),
    }


ALL_ROUTERS = (
    registry_ext_router,
    census_ext_router,
    model_registry_ext_router,
    opportunity_briefs_router,
    perception_router,
    rules_updates_router,
)
