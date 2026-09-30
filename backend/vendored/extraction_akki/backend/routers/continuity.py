"""M8 continuity routes: ratified recovery policy, control-Ledger WORM archive, point-in-time restore drill with independent countersign."""
from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel, ConfigDict

from services.enforce.census_identity import census_identity
from services.watch import commission_gate

router = APIRouter(tags=["m8-continuity"])


class Envelope(BaseModel):
    model_config = ConfigDict(extra="allow")
    tenant_id: str


def _master_or_operator(actor):
    if not {"operator", "master_admin"}.intersection(actor["roles"]):
        raise HTTPException(403, "Only an admitted estate operator can run continuity drills.")


@router.get("/api/continuity/policy", response_model=Envelope)
def continuity_policy(actor=Depends(census_identity)):
    from services.business_continuity import policy
    return {"tenant_id": actor["tenant_id"], **policy.policy_view()}


@router.get("/api/continuity/ledger/head", response_model=Envelope)
async def ledger_head(actor=Depends(census_identity)):
    import core
    from services.business_continuity import ledger_archive
    return {"tenant_id": actor["tenant_id"], **(await ledger_archive.head(core.db, actor["tenant_id"]))}


@router.get("/api/continuity/ledger/archives", response_model=Envelope)
def ledger_archives(actor=Depends(census_identity)):
    from services.business_continuity import ledger_archive
    rows = ledger_archive.worm_list()
    return {"tenant_id": actor["tenant_id"], "archives": [{**r, "heads": {actor["tenant_id"]: (r.get("heads") or {}).get(actor["tenant_id"])}} for r in rows]}


@router.post("/api/continuity/ledger/archive", response_model=Envelope)
async def ledger_archive_now(body: dict = Body(default={}), actor=Depends(census_identity)):
    with commission_gate.crossing(actor, "continuity.ledger_archive", body):
        _master_or_operator(actor)
        import core
        from services.business_continuity import ledger_archive
        try:
            receipt = await ledger_archive.archive(core.db, replicate_host=body.get("replicate_host"))
        except FileExistsError as exc:
            raise HTTPException(409, str(exc)) from exc
    return {"tenant_id": actor["tenant_id"], "archive": receipt}


@router.post("/api/continuity/ledger/restore-drill", response_model=Envelope)
async def ledger_restore_drill(body: dict = Body(default={}), actor=Depends(census_identity)):
    """M8-T3: restore the latest (or named) WORM archive into an isolated drill database, verify the chain, measure loss/time, countersign independently."""
    with commission_gate.crossing(actor, "continuity.ledger_restore_drill", body):
        _master_or_operator(actor)
        import core
        from services.business_continuity import ledger_archive
        try:
            receipt = await ledger_archive.restore_drill(core.client, core.db, archive_key=body.get("archive_key"), witness_host=body.get("witness_host", "akki-vm"), actor=actor["principal_id"])
        except (FileNotFoundError, ValueError) as exc:
            raise HTTPException(422, str(exc)) from exc
        except (OSError, KeyError) as exc:
            raise HTTPException(409, "The witness host is unavailable; the drill was not countersigned.") from exc
    return {"tenant_id": actor["tenant_id"], "drill": receipt}


@router.get("/api/continuity/drills", response_model=Envelope)
def continuity_drills(actor=Depends(census_identity)):
    from services.training_runner import m9_drills
    return {"tenant_id": actor["tenant_id"], "receipts": m9_drills.list_receipts()}
