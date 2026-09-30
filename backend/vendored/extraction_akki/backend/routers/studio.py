"""doc-studio routes (M6): the installed production skill, commissions, prove-builds, revisions, exports and downloads.
Tenant-bound through the same identity as the census surfaces; operators commission/build/revise, everyone in the tenant reads.
Routes /api/studio/* — the existing /api/decks/* engine stays read-only for its recorded deck (owner ruling 2026-09-30 (2))."""
import json
import re

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from pydantic import BaseModel, ConfigDict

from services.enforce.census_identity import census_identity
from services.transform_forms.doc_studio import service
from services.transform_forms.doc_studio.install import skill_state

router = APIRouter(prefix="/api/studio", tags=["doc-studio"])
REF = re.compile(r"[A-Za-z0-9_.-]{1,80}")


class Envelope(BaseModel):
    model_config = ConfigDict(extra="allow")
    tenant_id: str


def _operator(actor):
    if not {"operator", "master_admin"}.intersection(actor["roles"]):
        raise HTTPException(403, "Only an estate operator can commission, build or revise a document.")


def _full(actor, record):
    return {"tenant_id": actor["tenant_id"], "commission": service.get_commission(actor["tenant_id"], record["commission_id"]) or record}


def _guard(*refs):
    if not all(REF.fullmatch(r or "") for r in refs):
        raise HTTPException(404, "No commission with that reference is available in your tenant.")


@router.get("/skill", response_model=Envelope)
def get_skill(actor=Depends(census_identity)):
    return {"tenant_id": actor["tenant_id"], **skill_state()}


@router.get("/frames", response_model=Envelope)
def get_frames(actor=Depends(census_identity)):
    return {"tenant_id": actor["tenant_id"], **service.frames()}


@router.get("/commissions", response_model=Envelope)
def list_commissions(actor=Depends(census_identity)):
    return {"tenant_id": actor["tenant_id"], "commissions": service.list_commissions(actor["tenant_id"])}


@router.get("/commissions/{commission_id}", response_model=Envelope)
def get_commission(commission_id: str, actor=Depends(census_identity)):
    _guard(commission_id)
    record = service.get_commission(actor["tenant_id"], commission_id)
    if not record:
        raise HTTPException(404, "No commission with that reference is available in your tenant.")
    return _full(actor, record)


@router.post("/producers/estate-intelligence/{job_id}", status_code=201, response_model=Envelope)
def commission_estate(job_id: str, body: dict = Body(default={}), actor=Depends(census_identity)):
    _operator(actor)
    if actor["tenant_id"] != "RMS" or not re.fullmatch(r"eij-[a-f0-9]{12}", job_id):
        raise HTTPException(404, "No estate intelligence census with that reference is available in your tenant.")
    try:
        record, created = service.create_from_estate(job_id, actor["tenant_id"], actor["principal_id"])
    except LookupError as exc:
        raise HTTPException(404, str(exc)) from None
    if created and body.get("build", True):
        record = service.build(actor["tenant_id"], record["commission_id"], actor["principal_id"])
    return {**_full(actor, record), "created": created}


@router.post("/commissions/{commission_id}/build", status_code=201, response_model=Envelope)
def build(commission_id: str, actor=Depends(census_identity)):
    _operator(actor); _guard(commission_id)
    try:
        record = service.build(actor["tenant_id"], commission_id, actor["principal_id"])
    except LookupError as exc:
        raise HTTPException(404, str(exc)) from None
    return _full(actor, record)


@router.post("/commissions/{commission_id}/revise", status_code=201, response_model=Envelope)
def revise(commission_id: str, body: dict = Body(...), actor=Depends(census_identity)):
    _operator(actor); _guard(commission_id)
    changes = body.get("changes") or []
    if not isinstance(changes, list) or not all(isinstance(c, dict) and "path" in c and "value" in c for c in changes):
        raise HTTPException(422, "changes must be a list of {path, value}; paths address content.* or brief.*")
    try:
        record = service.revise(actor["tenant_id"], commission_id, actor["principal_id"], changes)
    except LookupError as exc:
        raise HTTPException(404, str(exc)) from None
    except (ValueError, FileExistsError) as exc:
        raise HTTPException(422, str(exc)) from None
    return _full(actor, record)


@router.post("/commissions/{commission_id}/reverdict", status_code=201, response_model=Envelope)
def reverdict(commission_id: str, actor=Depends(census_identity)):
    _operator(actor); _guard(commission_id)
    try:
        record = service.reverdict(actor["tenant_id"], commission_id, actor["principal_id"])
    except LookupError as exc:
        raise HTTPException(404, str(exc)) from None
    except (ValueError, FileExistsError) as exc:
        raise HTTPException(422, str(exc)) from None
    return _full(actor, record)


@router.post("/commissions/{commission_id}/builds/{build_id}/export-pdf", status_code=201, response_model=Envelope)
def export_pdf(commission_id: str, build_id: str, actor=Depends(census_identity)):
    _operator(actor); _guard(commission_id, build_id)
    try:
        record = service.export_pdf(actor["tenant_id"], commission_id, build_id, actor["principal_id"])
    except LookupError as exc:
        raise HTTPException(404, str(exc)) from None
    return _full(actor, record)


@router.get("/commissions/{commission_id}/builds/{build_id}/artifact/{name}")
def artifact(commission_id: str, build_id: str, name: str, actor=Depends(census_identity)):
    _guard(commission_id, build_id)
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,120}\.(pptx|docx|xlsx|html|pdf|json)", name):
        raise HTTPException(404, "That artefact is not on record for your tenant.")
    hit = service.artifact(actor["tenant_id"], commission_id, build_id, name)
    if not hit:
        raise HTTPException(404, "That artefact is not on record for your tenant.")
    data, media, filename = hit
    disposition = "inline" if media.startswith(("text/html", "application/pdf", "application/json")) else "attachment"
    return Response(content=data, media_type=media, headers={"Cache-Control": "private, no-store", "Content-Disposition": f'{disposition}; filename="{filename}"'})


@router.get("/commissions/{commission_id}/builds/{build_id}/log")
def build_log(commission_id: str, build_id: str, actor=Depends(census_identity)):
    _guard(commission_id, build_id)
    record = service.store.load_record(actor["tenant_id"], commission_id)
    entry = next((b for b in (record or {}).get("builds", []) if b["build_id"] == build_id), None)
    if not entry or not entry.get("log_path"):
        raise HTTPException(404, "No build log on record for that build.")
    path = service.Path(entry["log_path"])
    return Response(content=json.dumps({"tenant_id": actor["tenant_id"], "build_id": build_id, "log": path.read_text() if path.exists() else ""}), media_type="application/json")
