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


def _rms(actor):
    if actor["tenant_id"] != "RMS":
        raise HTTPException(404, "No M9 record with that reference is available in your tenant.")


def _lawful():
    from services.census_autonomy.operational_runner import admission_path
    path, _ = admission_path()
    return str(path)


@router.post("/api/training/m9/certificates/{job_id}/readjudicate", response_model=Envelope)
def m9_readjudicate(job_id: str, body: dict = Body(...), actor=Depends(census_identity)):
    """Owner ruling 2026-09-30 (1a): re-read the banked per-stratum results against the Outcome's recorded floor; admission re-runs by new record."""
    with commission_gate.crossing(actor, "m9_training.readjudicate", {**body, "job_id": job_id}):
        _operator(actor)
        if not JOB_ID.fullmatch(job_id):
            raise HTTPException(404, "No M9 training job with that reference is available in your tenant.")
        floor, source = body.get("outcome_floor"), str(body.get("floor_source") or "").strip()
        if not isinstance(floor, (int, float)) or not (0 < floor <= 1) or not source:
            raise HTTPException(422, "outcome_floor (0–1) and floor_source (where the Outcome recorded it) are required.")
        from services.training_runner import m9_readjudication
        try:
            record = m9_readjudication.readjudicate(job_id, float(floor), source, variant=body.get("variant", "full"), actor=actor["principal_id"])
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
    return {"tenant_id": actor["tenant_id"], "readjudication": record}


@router.get("/api/training/m9/readjudications", response_model=Envelope)
def m9_readjudications(actor=Depends(census_identity)):
    from services.training_runner import m9_readjudication
    return {"tenant_id": actor["tenant_id"], "records": m9_readjudication.list_records() if actor["tenant_id"] == "RMS" else []}


@router.get("/api/training/m9/models", response_model=Envelope)
def m9_models(actor=Depends(census_identity)):
    from services.training_runner import m9_serving
    view = m9_serving.models_view() if actor["tenant_id"] == "RMS" else {"registry_version": None, "trained_adapters": []}
    return {"tenant_id": actor["tenant_id"], **view}


@router.get("/api/training/m9/capabilities", response_model=Envelope)
def m9_capabilities(actor=Depends(census_identity)):
    from services.training_runner import m9_drills
    return {"tenant_id": actor["tenant_id"], **m9_drills.capabilities()}


@router.post("/api/training/m9/serving/{model_id}/start", status_code=202, response_model=Envelope)
def m9_serving_start(model_id: str, body: dict = Body(...), actor=Depends(census_identity)):
    with commission_gate.crossing(actor, "m9_serving.start", {**body, "model_id": model_id}):
        _operator(actor)
        from services.training_runner import m9_serving
        try:
            job = m9_serving.start(model_id, actor["principal_id"], _lawful(), gpu_index=int(body.get("gpu_index", 1)), host=body.get("host"))
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
        except (OSError, KeyError) as exc:
            raise HTTPException(409, "The serving host is unavailable; nothing was started.") from exc
    return {"tenant_id": actor["tenant_id"], "model_id": model_id, "job": job}


@router.get("/api/training/m9/serving/{model_id}/health", response_model=Envelope)
def m9_serving_health(model_id: str, actor=Depends(census_identity)):
    _rms(actor)
    from services.training_runner import m9_serving
    try:
        return {"tenant_id": actor["tenant_id"], **m9_serving.health(model_id)}
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.post("/api/training/m9/serving/{model_id}/classify", response_model=Envelope)
def m9_serving_classify(model_id: str, body: dict = Body(...), actor=Depends(census_identity)):
    """Governed answer from the served artefact: bounded texts in, labels + lineage out. E1 relays; it holds no weights or corpus."""
    _rms(actor)
    from services.training_runner import m9_serving
    texts = body.get("texts") or []
    if not isinstance(texts, list) or not texts:
        raise HTTPException(422, "texts (list of 1–16 strings) required.")
    try:
        return {"tenant_id": actor["tenant_id"], **m9_serving.classify(model_id, texts)}
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from exc


@router.post("/api/training/m9/serving/{model_id}/withdraw", response_model=Envelope)
def m9_serving_withdraw(model_id: str, body: dict = Body(...), actor=Depends(census_identity)):
    with commission_gate.crossing(actor, "m9_serving.withdraw", {**body, "model_id": model_id}):
        _operator(actor)
        reason = str(body.get("reason") or "").strip()
        if not reason:
            raise HTTPException(422, "A withdrawal needs a stated reason.")
        from services.training_runner import m9_serving
        try:
            record = m9_serving.withdraw(model_id, reason[:200], actor["principal_id"])
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
    return {"tenant_id": actor["tenant_id"], "withdrawal": record}


@router.post("/api/training/m9/serving/{model_id}/stop", response_model=Envelope)
def m9_serving_stop(model_id: str, body: dict = Body(...), actor=Depends(census_identity)):
    with commission_gate.crossing(actor, "m9_serving.stop", {**body, "model_id": model_id}):
        _operator(actor)
        from services.training_runner import m9_serving
        try:
            record = m9_serving.stop(model_id, str(body.get("reason") or "operator stop")[:200], actor["principal_id"])
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
    return {"tenant_id": actor["tenant_id"], **record}


@router.post("/api/training/m9/serving/{model_id}/load-test", status_code=202, response_model=Envelope)
def m9_serving_load_test(model_id: str, body: dict = Body(...), actor=Depends(census_identity)):
    with commission_gate.crossing(actor, "m9_serving.load_test", {**body, "model_id": model_id}):
        _operator(actor)
        from services.training_runner import m9_serving
        try:
            job = m9_serving.load_test(model_id, actor["principal_id"], _lawful(), concurrency=body.get("concurrency", 8), requests_per_thread=body.get("requests_per_thread", 20),
                                       batch=body.get("batch", 8), per_stratum=body.get("per_stratum", 30))
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
    return {"tenant_id": actor["tenant_id"], "model_id": model_id, "job": job}


@router.post("/api/training/m9/jobs/{job_id}/interrupt", response_model=Envelope)
def m9_interrupt(job_id: str, body: dict = Body(...), actor=Depends(census_identity)):
    """M8-T1 / M9-T3 drill: SIGKILL the worker process on the host (physical process loss); the job is recorded as interrupted."""
    with commission_gate.crossing(actor, "m9_training.interrupt", {**body, "job_id": job_id}):
        _operator(actor)
        if not JOB_ID.fullmatch(job_id):
            raise HTTPException(404, "No M9 training job with that reference is available in your tenant.")
        reason = str(body.get("reason") or "").strip()
        if not reason:
            raise HTTPException(422, "An interruption drill needs a stated reason.")
        from services.training_runner import m9_dispatch as m9
        try:
            job = m9.interrupt(job_id, reason[:200])
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
        except (OSError, KeyError) as exc:
            raise HTTPException(409, "The training host is unavailable; the worker was not interrupted.") from exc
        if not job:
            raise HTTPException(404, "No M9 training job with that reference is available in your tenant.")
    return {"tenant_id": actor["tenant_id"], "job": job}


@router.post("/api/training/m9/drills/interruption", response_model=Envelope)
def m9_interruption_receipt(body: dict = Body(...), actor=Depends(census_identity)):
    with commission_gate.crossing(actor, "m9_training.drill_receipt", body):
        _operator(actor)
        from services.training_runner import m9_drills
        try:
            receipt = m9_drills.compose_interruption_receipt(str(body.get("killed_job_id")), str(body.get("resumed_job_id")), actor=actor["principal_id"])
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
    return {"tenant_id": actor["tenant_id"], "receipt": receipt}


@router.get("/api/training/m9/drills", response_model=Envelope)
def m9_drill_receipts(actor=Depends(census_identity)):
    from services.training_runner import m9_drills
    return {"tenant_id": actor["tenant_id"], "receipts": m9_drills.list_receipts() if actor["tenant_id"] == "RMS" else []}


@router.post("/api/training/m9/rights/revoke-unit", response_model=Envelope)
def m9_revoke_unit(body: dict = Body(...), actor=Depends(census_identity)):
    """M9-T5: withdraw one training dependency; every descendant adapter is recalled (serving refused) and a lawful re-derivation is commissioned."""
    with commission_gate.crossing(actor, "m9_training.revoke_unit", body):
        _operator(actor)
        unit_id, reason = str(body.get("unit_id") or "").strip(), str(body.get("reason") or "").strip()
        if not unit_id or not reason:
            raise HTTPException(422, "unit_id and reason are required.")
        from services.training_runner import m9_recall
        try:
            record = m9_recall.revoke_unit(unit_id, reason[:200], actor["principal_id"], _lawful(), rederive=bool(body.get("rederive", True)), gpu_index=int(body.get("gpu_index", 0)))
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
        except (OSError, KeyError) as exc:
            raise HTTPException(409, "A custody host is unavailable; the revocation was not completed.") from exc
    return {"tenant_id": actor["tenant_id"], "revocation": record}


@router.get("/api/training/m9/rights/revocations", response_model=Envelope)
def m9_revocations(actor=Depends(census_identity)):
    from services.training_runner import m9_recall
    return {"tenant_id": actor["tenant_id"], "revocations": m9_recall.list_records() if actor["tenant_id"] == "RMS" else []}
