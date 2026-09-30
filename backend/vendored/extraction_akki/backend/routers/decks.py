"""Deck Rendering Engine routes (M6.1): validate, render, list, read, download; DR-R10 producer for the estate intelligence census.
Tenant-bound through the same identity as the census surfaces; operators render, everyone in the tenant reads."""
import re

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from pydantic import BaseModel, ConfigDict

from services.enforce.census_identity import census_identity
from services.transform_forms.deck_engine import service
from services.transform_forms.deck_engine.render import ENGINE_VERSION, TOKEN_VERSION, pdf_capability
from services.transform_forms.deck_engine.tokens import DEFAULT_REGISTER, LIVE_MOTION, REGISTERS
from services.transform_forms.deck_engine.validate import DeckValidationError, default_resolver, lint, validate

router = APIRouter(prefix="/api/decks", tags=["deck-engine"])
DECK_ID = re.compile(r"[A-Za-z0-9_.-]{1,80}")


class DeckEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")
    tenant_id: str


def _operator(actor):
    if not {"operator", "master_admin"}.intersection(actor["roles"]):
        raise HTTPException(403, "Only an estate operator can render a deck.")


def _refuse(exc: DeckValidationError):
    raise HTTPException(422, {"outcome": "refused", "rule_set": "DR-R5 fail-closed; every violation enumerated in one pass", "errors": exc.errors})


@router.get("/engine", response_model=DeckEnvelope)
def engine_state(actor=Depends(census_identity)):
    return {"tenant_id": actor["tenant_id"], "engine_version": ENGINE_VERSION, "token_version": TOKEN_VERSION, "registers": REGISTERS,
            "default_register": DEFAULT_REGISTER, "live_motion": LIVE_MOTION, "pdf": pdf_capability(),
            "owner_slots": {"O-D1 default register": f"{DEFAULT_REGISTER} (DEFAULT, not ratified)", "O-D2 live motion": "off (DEFAULT)", "PPTX": "not built; DR-R9 fallback posture recorded", "contract name": "DeckSpec_v1 carries the DR-R4 shape (v0 shell frozen)"}}


@router.post("/validate", response_model=DeckEnvelope)
def validate_spec(body: dict = Body(...), actor=Depends(census_identity)):
    try:
        checked = validate(body, default_resolver)
    except DeckValidationError as exc:
        return {"tenant_id": actor["tenant_id"], "outcome": "refused", "errors": exc.errors}
    return {"tenant_id": actor["tenant_id"], "outcome": "valid", "errors": [], "lint": lint(checked["spec"]), "receipts_resolved": sorted(checked["receipts"])}


@router.post("/render", status_code=201, response_model=DeckEnvelope)
def render_spec(body: dict = Body(...), actor=Depends(census_identity)):
    _operator(actor)
    want_pdf = bool(body.pop("export_pdf", False)) if isinstance(body, dict) else False
    try:
        record = service.render_deck(body, actor["tenant_id"], actor["principal_id"], want_pdf=want_pdf)
    except DeckValidationError as exc:
        _refuse(exc)
    return {"tenant_id": actor["tenant_id"], "deck": record}


@router.post("/producers/estate-intelligence/{job_id}", status_code=201, response_model=DeckEnvelope)
def produce_from_estate_intelligence(job_id: str, body: dict = Body(default={}), actor=Depends(census_identity)):
    _operator(actor)
    if actor["tenant_id"] != "RMS" or not re.fullmatch(r"eij-[a-f0-9]{12}", job_id):
        raise HTTPException(404, "No estate intelligence census with that reference is available in your tenant.")
    from services.census_autonomy import estate_intelligence_report as eir
    from services.transform_forms.deck_engine.producers import estate_intelligence_deck
    report = eir.report_for(job_id, cached_only=True)
    if not report:
        raise HTTPException(404, "No verified estate intelligence report is banked for that census.")
    spec = estate_intelligence_deck(report, deck_id=f"deck-estate-{job_id}")
    try:
        record = service.render_deck(spec, actor["tenant_id"], actor["principal_id"], want_pdf=bool(body.get("export_pdf", False)),
                                     authoring={"tokens": 0, "source": "deterministic producer estate_intelligence_deck; no model authored the spec"},
                                     producer="estate_intelligence")
    except DeckValidationError as exc:
        _refuse(exc)
    return {"tenant_id": actor["tenant_id"], "deck": record, "spec": spec}


@router.get("", response_model=DeckEnvelope)
def list_decks(actor=Depends(census_identity)):
    return {"tenant_id": actor["tenant_id"], "decks": service.list_decks(actor["tenant_id"])}


@router.get("/{deck_id}", response_model=DeckEnvelope)
def get_deck(deck_id: str, actor=Depends(census_identity)):
    record = service.load(actor["tenant_id"], deck_id) if DECK_ID.fullmatch(deck_id) else None
    if not record:
        raise HTTPException(404, "No deck with that reference is available in your tenant.")
    return {"tenant_id": actor["tenant_id"], "deck": record}


@router.get("/{deck_id}/artifact.{ext}")
def get_artifact(deck_id: str, ext: str, spec_hash: str = None, actor=Depends(census_identity)):
    if ext not in ("html", "pdf") or not DECK_ID.fullmatch(deck_id):
        raise HTTPException(404, "Only the HTML artifact of record and its PDF export are served.")
    data = service.artifact_bytes(actor["tenant_id"], deck_id, spec_hash, ext)
    if data is None:
        raise HTTPException(404, "That artifact version is not on record for your tenant.")
    media = "text/html; charset=utf-8" if ext == "html" else "application/pdf"
    return Response(content=data, media_type=media, headers={"Cache-Control": "private, no-store", "Content-Disposition": f'inline; filename="{deck_id}.{ext}"'})
