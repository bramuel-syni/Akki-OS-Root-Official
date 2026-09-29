"""M9 governed training — tenant-scoped control-plane routes. E1 wires and steps back; the host does the work."""
import re

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel, ConfigDict

from services.enforce.census_identity import census_identity
from services.watch import commission_gate

router = APIRouter(tags=["m9-governed-training"])
JOB_ID = re.compile(r"m9j-[a-f0-9]{12}")


class Envelope(BaseModel):
    model_config = ConfigDict(extra="allow")
    tenant_id: str


def _operator(actor):
    if not {"operator", "master_admin"}.intersection(actor["roles"]):
        raise HTTPException(403, "Only an admitted estate operator can commission a governed training job.")
    if actor["tenant_id"] != "RMS":
        raise HTTPException(403, "M9 training material in this pilot is RMS tenant custody (transcripts) and DIGICOW sealed units; only the RMS operator seat commissions it.")


@router.post("/api/training/m9/jobs", status_code=202, response_model=Envelope)
def m9_submit(body: dict = Body(...), actor=Depends(census_identity)):
    """Commission one M9 phase (acquire_bases · assemble · calibrate · compare_optimizers · train · pipeline) on a named admitted GPU host."""
    with commission_gate.crossing(actor, "m9_training.commission", body):
        _operator(actor)
        from services.census_autonomy.operational_runner import admission_path
        from services.training_runner import m9_dispatch as m9
        try:
            path, _ = admission_path()
            params = {k: v for k, v in body.items() if k not in ("phase", "host", "tenant_id")}
            job = m9.submit(body.get("phase"), params, body.get("host"), actor["principal_id"], str(path))
        except (ValueError, TypeError) as exc:
            raise HTTPException(422, str(exc)) from exc
        except (OSError, KeyError) as exc:
            raise HTTPException(409, "The training host or census admission is unavailable; nothing was dispatched.") from exc
    return {"tenant_id": actor["tenant_id"], "job": job}


@router.get("/api/training/m9/jobs", response_model=Envelope)
def m9_jobs(actor=Depends(census_identity)):
    from services.training_runner import m9_dispatch as m9
    return {"tenant_id": actor["tenant_id"], "jobs": m9.list_jobs() if actor["tenant_id"] == "RMS" else [], "hosts": m9.hosts()}


@router.get("/api/training/m9/jobs/{job_id}", response_model=Envelope)
def m9_job(job_id: str, actor=Depends(census_identity)):
    """One bounded status RPC to the host; the receipt is verified by digest and banked on completion."""
    from services.training_runner import m9_dispatch as m9
    if actor["tenant_id"] != "RMS" or not JOB_ID.fullmatch(job_id):
        raise HTTPException(404, "No M9 training job with that reference is available in your tenant.")
    job = m9.refresh(job_id)
    if not job:
        raise HTTPException(404, "No M9 training job with that reference is available in your tenant.")
    return {"tenant_id": actor["tenant_id"], "job": job}


@router.post("/api/training/m9/jobs/{job_id}/cancel", response_model=Envelope)
def m9_cancel(job_id: str, body: dict = Body(...), actor=Depends(census_identity)):
    with commission_gate.crossing(actor, "m9_training.cancel", {**body, "job_id": job_id}):
        _operator(actor)
        if not JOB_ID.fullmatch(job_id):
            raise HTTPException(404, "No M9 training job with that reference is available in your tenant.")
        reason = str(body.get("reason") or "").strip()
        if not reason:
            raise HTTPException(422, "A stop needs a stated reason.")
        from services.training_runner import m9_dispatch as m9
        try:
            job = m9.cancel(job_id, reason[:200])
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
        except (OSError, KeyError) as exc:
            raise HTTPException(409, "The training host is unavailable; the worker was not stopped.") from exc
        if not job:
            raise HTTPException(404, "No M9 training job with that reference is available in your tenant.")
    return {"tenant_id": actor["tenant_id"], "job": job}


@router.get("/api/training/m9/certificates/{job_id}", response_model=Envelope)
def m9_certificate(job_id: str, actor=Depends(census_identity)):
    from services.training_runner import m9_dispatch as m9
    job = m9.load_job(job_id) if actor["tenant_id"] == "RMS" else None
    if not job or not job.get("run_certificate"):
        raise HTTPException(404, "No run certificate is on record for that M9 job in your tenant.")
    return {"tenant_id": actor["tenant_id"], "job_id": job_id, "certificate": job["run_certificate"]}
