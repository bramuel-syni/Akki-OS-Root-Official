"""Actual-state refusals. No fake stop, retry, approval, or retrieval success."""
from fastapi import HTTPException
from services.northena.portal_work import detail
from services.dap_lifecycle.state_machine import RequestState, transition, IllegalTransition


async def stop(db, scope, request_id):
    work = await detail(db, scope, request_id)
    try:
        transition(RequestState(work.lifecycle_state), RequestState.Stopped)
    except IllegalTransition as exc:
        raise HTTPException(409, "Only an executing request can be stopped.") from exc
    # A terminal record alone cannot prove an executor stopped. No admitted
    # execution/cancellation seam is present in this slice; never acknowledge one.
    raise HTTPException(409, "Executor cancellation receipt is required before stop can be confirmed.")


async def retry(db, scope, request_id):
    work = await detail(db, scope, request_id)
    if work.lifecycle_state not in {"Blocked", "Interrupted"}:
        raise HTTPException(409, "This request is not eligible for retry.")
    raise HTTPException(409, "A surviving approval and an admitted gate/executor path are required for retry.")


async def result(db, scope, request_id):
    await detail(db, scope, request_id)
    raise HTTPException(409, "No verified, rights-admitted result receipt is available for this request.")