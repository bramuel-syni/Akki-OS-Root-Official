"""Native census route composition. Replaces unsafe bindings, not sealed engine bodies."""
import os
import time
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Request
from pydantic import BaseModel, ConfigDict

from services.enforce.census_identity import census_identity
from services.enforce.principal_context_adapter import principal_context
from services.census_autonomy import engine, operational_store as store, operational_reads as reads
from services.census_autonomy.operational_scope import SOURCE_TENANTS, SOURCE_LABELS, validate_submission
from services.census_autonomy.operational_runner import admission_path, run_bounded_census

router = APIRouter(tags=["tenant-scoped-census"])


class CensusEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")
    tenant_id: str


@router.get("/api/portal/census/overview", response_model=CensusEnvelope)
@router.get("/api/registry/facts", response_model=CensusEnvelope)
def overview(actor=Depends(census_identity)):
    with principal_context(actor["principal_id"]):
        values = reads.records(actor["tenant_id"])
        from services.census_autonomy.registry_surfaces import inventory,conversations,source_summary,record_summary,run_summary
        surfaces=inventory(actor['tenant_id'],values)
        surfaces['source_details']=[source_summary(s) for s in surfaces['source_details']]
        values=[record_summary(r) for r in values]
        return {**actor, "records": values, "latest": values[0] if values else None,
                "runs": [run_summary(reads.run_view(r)) for r in store.runs(actor["tenant_id"])],
                "can_run": bool({"operator", "master_admin"}.intersection(actor["roles"])),
                "sources": [{"source_id": s, "label": SOURCE_LABELS[s], "scope": "External read-only enumeration and declared sampled checks"}
                            for s, t in SOURCE_TENANTS.items() if t == actor["tenant_id"]],
                "measurement_note": "Census evidence does not grant extraction or external-release rights.",
                "omission_note": "Mixed-tenant or unassigned historical records are withheld until ownership is established.",
                "schedule": {"mode": "on_demand", "automatic_schedule_active": False},
                "data_sources": [], "storage_backends": [], 'conversations':conversations(actor['tenant_id']), **surfaces}


@router.get("/api/portal/census/records", response_model=CensusEnvelope)
@router.get("/api/census/records", response_model=CensusEnvelope)
@router.get("/api/census/history", response_model=CensusEnvelope)
def records(actor=Depends(census_identity)):
    return {"tenant_id": actor["tenant_id"], "records": reads.records(actor["tenant_id"])}


@router.get("/api/portal/census/records/{record_id}", response_model=CensusEnvelope)
def record(record_id: str, actor=Depends(census_identity)):
    row = next((r for r in reads.records(actor["tenant_id"])
                if record_id in {r["record_id"], str(r.get("census_number"))}), None)
    if not row:
        raise HTTPException(404, "No census record with that reference is available in your tenant.")
    return {"tenant_id": actor["tenant_id"], "record": row}


@router.get("/api/portal/census/latest", response_model=CensusEnvelope)
@router.get("/api/census/latest", response_model=CensusEnvelope)
def latest(actor=Depends(census_identity)):
    values = reads.records(actor["tenant_id"])
    return {"tenant_id": actor["tenant_id"], "census": values[0] if values else None,
            "reason": "" if values else "No tenant-attributed census evidence is available yet."}


@router.get("/api/portal/census/runs/{census_run_id}/state", response_model=CensusEnvelope)
def state(census_run_id: str, actor=Depends(census_identity)):
    result = reads.run_state(census_run_id, actor["tenant_id"])
    if result is None:
        raise HTTPException(404, "No census run with that reference is available in your tenant.")
    return result


@router.post("/api/portal/census/run", status_code=202, response_model=CensusEnvelope)
@router.post("/api/census/run", status_code=202, response_model=CensusEnvelope)
def submit(background: BackgroundTasks, body: dict = Body(...), actor=Depends(census_identity)):
    try:
        body = {**body, 'worker_id': body.get('worker_id') or os.environ['CENSUS_PRIMARY_WORKER']}
        sources = validate_submission(body, actor["tenant_id"], actor["roles"])
        budget = int(os.environ["CENSUS_JOB_MAX_SECONDS"])
        if budget <= 0:
            raise ValueError("The current census budget does not permit a run.")
        path, _ = admission_path()
        row, fresh = store.enqueue(actor["tenant_id"], actor["principal_id"], sources,
                                   body.get("idempotency_key", ""), str(path), body.get('worker_id'), body.get('source_refs'))
    except PermissionError as exc:
        raise HTTPException(403, str(exc)) from exc
    except (ValueError, TypeError) as exc:
        raise HTTPException(422, str(exc)) from exc
    except (OSError, KeyError) as exc:
        raise HTTPException(409, "The existing census admission or execution budget is unavailable. No source read was started.") from exc
    # Execution belongs to the existing supervised worker and durable queue,
    # not an ASGI BackgroundTask that prevents app reloads from completing.
    return {**reads.run_view(row), "duplicate": not fresh}


@router.post("/api/portal/census/plan", response_model=CensusEnvelope)
def plan(body: dict = Body(default={}), actor=Depends(census_identity)):
    """Shovel origination: Northena admits the census objective, Targeta orders the
    retained regions into a reproducible MiningPlan, the shovel cuts ~1 TiB scoops and
    scoop 0 is commissioned on the external worker; the supervised runner advances
    the cadence one scoop at a time. An active plan is returned, not duplicated,
    unless `replan=true`."""
    if not {"operator", "master_admin"}.intersection(actor["roles"]):
        raise HTTPException(403, "Only an admitted estate operator can shape a census plan.")
    from services.census_autonomy import census_scoop_origination as shovel
    try:
        worker_id = body.get("worker_id") or os.environ["CENSUS_PRIMARY_WORKER"]
        if worker_id != os.environ["CENSUS_PRIMARY_WORKER"]:
            from services.training_runner.ssh_seam import list_hosts
            if worker_id not in ["non_gpu_jump", *list_hosts()]:
                raise ValueError("Choose a registered external worker.")
        path, _ = admission_path()
        built = None if body.get("replan") is True else shovel.active_plan(actor["tenant_id"])
        reused = built is not None
        if built is None:
            built = shovel.originate(actor["tenant_id"], actor["principal_id"], str(path), worker_id,
                                     body.get("target_bytes"), body.get("objective_shape"))
        commissioned = None
        if built.get("state") == "active" and built["scoops"]:
            live = next((s for s in built["scoops"] if s.get("state") == "commissioned"), None)
            if live:
                commissioned = live["census_run_id"]
            elif built["scoops"][0].get("state") == "queued":
                row, _fresh = shovel.commission_scoop(built, 0, actor["principal_id"], str(path))
                commissioned = row["census_run_id"]
    except PermissionError as exc:
        raise HTTPException(403, str(exc)) from exc
    except (ValueError, TypeError) as exc:
        raise HTTPException(422, str(exc)) from exc
    except (OSError, KeyError) as exc:
        raise HTTPException(409, "The census admission or worker configuration is unavailable; no plan was commissioned.") from exc
    return {"tenant_id": actor["tenant_id"], "plan": built, "commissioned_run_id": commissioned, "reused_active_plan": reused}


@router.get("/api/portal/census/plan/{plan_id}", response_model=CensusEnvelope)
def plan_state(plan_id: str, actor=Depends(census_identity)):
    from services.census_autonomy import census_scoop_origination as shovel
    saved = shovel.load_plan(actor["tenant_id"], plan_id)
    if not saved:
        raise HTTPException(404, "No census plan with that reference is available in your tenant.")
    return {"tenant_id": actor["tenant_id"], "plan": saved}


async def unbound_surface(request: Request, actor=Depends(census_identity)):
    raise HTTPException(409, "This older census projection is not tenant-bound. Use the current Census records view; no unscoped data was returned.")


def install(app):
    """Redirect consumers at the unsealed assembler; no hidden alternate census path remains."""
    from services.census_autonomy.registry_durability import collection
    collection()
    prefixes = ("/api/census/", "/api/portal/census/", "/api/registry/")
    old = [r for r in app.routes if getattr(r, "path", "").startswith(prefixes)]
    app.router.routes[:] = [r for r in app.routes if r not in old]
    app.include_router(router)
    from routers.registry_integrated import router as integrated_router
    app.include_router(integrated_router)
    covered = {(r.path, m) for r in [*router.routes,*integrated_router.routes] for m in r.methods}
    for route in old:
        methods = sorted(m for m in route.methods if (route.path, m) not in covered)
        if methods:
            app.add_api_route(route.path, unbound_surface, methods=methods, tags=["census-legacy-boundary"])