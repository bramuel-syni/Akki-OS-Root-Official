"""routers.portal_census_autonomy_producer — PHASE 3 continuation A''''-cont-A
· producer-bridge + synchronous-run + GPU-spend endpoints (all additive).

Owner directive 2026-09-22T~19:58Z verbatim: END-TO-END EXIT PROOF for
Phase 3 · curl-drivable · one sequence on AKKI-TEST covering
run → poll → response-required item → resolve → GPU-spend CAPTURED →
registry read surface.

This router is ADDITIVE per SO §3.8. Zero edits to sealed carriers:
- `services.auth.dependencies.require_identity_or_deny` (READ-ONLY)
- `services.auth.identity.Identity` (READ-ONLY)
- `services.census_autonomy.engine.run_bounded_census`/
  `enqueue_on_demand_run` (READ-ONLY public callables · PHASE 3 A)
- `services.census_autonomy.tenant_scope.is_census_admitted_tenant`
  (READ-ONLY · PHASE 3 A' adapter)
- `services.census_autonomy.producer_bridge.bank_refusal_rows_via_adapter`
  (READ-ONLY · A''''-cont-A carrier)
- `services.census_autonomy.gpu_spend_capture.capture_gpu_spend` (A''')

## Endpoints

- `POST /api/portal/census/runs/synchronous` — enqueue + run engine
  synchronously in-request + auto-bridge refusals to queue. JWT-gated,
  tenant-scoped. Body carries an optional `budget_seconds_offset`
  (default +3600s). Negative values engage the sealed engine's
  `DEFERRED_BUDGET_EXCEEDED` refusal path for exit-proof coverage.
- `POST /api/portal/census/runs/{census_run_id}/bank-refusals` —
  manual bridge invocation for an already-completed run. JWT-gated,
  tenant-scoped.
- `GET /api/portal/census/gpu-spend` — return live-telemetry GPU-spend
  capture verbatim per A'''. JWT-gated.
"""

from __future__ import annotations

import time
from typing import Any, Dict, Final

from fastapi import APIRouter, Body, HTTPException, Path, Request
from fastapi.responses import JSONResponse

from services.auth.dependencies import require_identity_or_deny
from services.auth.identity import Identity
from services.census_autonomy.data_source_adapter import (
    DATA_SOURCE_ADAPTER_DRIVER_CODES,
)
from services.census_autonomy.engine import (
    enqueue_on_demand_run,
    run_bounded_census,
)
from services.census_autonomy.gpu_spend_capture import capture_gpu_spend
from services.census_autonomy.producer_bridge import (
    bank_refusal_rows_via_adapter,
)
from services.census_autonomy.service_shape import REFUSAL_PATH_CLOSED_VOCAB
from services.census_autonomy.state_reader import read_census_run_state
from services.census_autonomy.tenant_scope import is_census_admitted_tenant


# ---------------------------------------------------------------------------
# Route path pins (SO §3.10-α · Final str · paired-equality by invariant)
# ---------------------------------------------------------------------------

SYNCHRONOUS_RUN_ROUTE_PATH: Final[str] = "/api/portal/census/runs/synchronous"
BANK_REFUSALS_ROUTE_PATH_TEMPLATE: Final[str] = (
    "/api/portal/census/runs/{census_run_id}/bank-refusals"
)
GPU_SPEND_ROUTE_PATH: Final[str] = "/api/portal/census/gpu-spend"

# Producer path uses obs_huawei_audio as the default driver for the
# synchronous-run exit-proof lane. Real driver inference from the
# `connect_source_descriptor` fold-in is deferred to a subsequent
# sub-slice (real driver rows land next).
_DEFAULT_PRODUCER_DRIVER: Final[str] = "obs_huawei_audio"

# Default budget for the synchronous-run endpoint (seconds beyond
# time.time()). Negative offset engages the sealed engine's
# DEFERRED_BUDGET_EXCEEDED refusal path for exit-proof coverage.
_DEFAULT_BUDGET_OFFSET_SEC: Final[int] = 3600


router = APIRouter(prefix="", tags=["portal-census-autonomy-producer"])


def _refusal(status_code: int, refusal_code: str, detail: str) -> JSONResponse:
    """Build a refusal response body carrying a sealed-vocab code."""
    if refusal_code not in REFUSAL_PATH_CLOSED_VOCAB:
        raise RuntimeError(
            f"Router attempted to emit refusal_code {refusal_code!r} "
            f"not in sealed REFUSAL_PATH_CLOSED_VOCAB "
            f"{REFUSAL_PATH_CLOSED_VOCAB}"
        )
    return JSONResponse(
        status_code=status_code,
        content={"refusal_code": refusal_code, "detail": detail},
    )


@router.post(SYNCHRONOUS_RUN_ROUTE_PATH)
async def post_synchronous_run(
    request: Request,
    body: Dict[str, Any] = Body(...),
):
    """POST /api/portal/census/runs/synchronous.

    Body:
      {
        "tenant_id": str,                     # must be admitted
        "connect_source_descriptor": dict,    # source descriptor
        "lawful_basis_admit_ref": str,        # pre-first-byte
        "budget_seconds_offset": int,         # optional (default +3600s)
        "producer_driver": str,               # optional (default obs_huawei_audio)
      }

    Runs the sealed engine synchronously with `job_deadline =
    time.time() + budget_seconds_offset`. After the engine returns,
    the router auto-bridges any refusal rows for the run into the
    A'''-cont-A response-required queue via the A'''' adapter.

    Returns:
      { "census_run_id": str,
        "engine_status": str,        # COMPLETE | DEFERRED_* | BLOCKED_*
        "banked_item_ids": list[str],
        "state": <read_census_run_state(census_run_id)>,
        "tenant_id": str,
        "principal_id": str,
      }
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result

    tenant_id = body.get("tenant_id")
    connect_source_descriptor = body.get("connect_source_descriptor")
    lawful_basis_admit_ref = body.get("lawful_basis_admit_ref")
    budget_seconds_offset = body.get(
        "budget_seconds_offset", _DEFAULT_BUDGET_OFFSET_SEC
    )
    producer_driver = body.get("producer_driver", _DEFAULT_PRODUCER_DRIVER)

    if not tenant_id or not isinstance(tenant_id, str):
        return _refusal(
            400, "BLOCKED_TENANT_SCOPE_MISMATCH", "tenant_id missing or not str"
        )
    if not isinstance(connect_source_descriptor, dict):
        return _refusal(
            400,
            "BLOCKED_LAWFUL_BASIS_MISSING",
            "connect_source_descriptor missing or not an object",
        )
    if not lawful_basis_admit_ref or not isinstance(
        lawful_basis_admit_ref, str
    ):
        return _refusal(
            400,
            "BLOCKED_LAWFUL_BASIS_MISSING",
            "lawful_basis_admit_ref missing or not a str · Doc-5 B5.2",
        )
    if not isinstance(budget_seconds_offset, int):
        return _refusal(
            400,
            "BLOCKED_LAWFUL_BASIS_MISSING",
            "budget_seconds_offset must be an int",
        )
    if producer_driver not in DATA_SOURCE_ADAPTER_DRIVER_CODES:
        return _refusal(
            400,
            "BLOCKED_LAWFUL_BASIS_MISSING",
            f"producer_driver {producer_driver!r} not in "
            f"{DATA_SOURCE_ADAPTER_DRIVER_CODES!r}",
        )
    if not is_census_admitted_tenant(tenant_id):
        return _refusal(
            403,
            "BLOCKED_TENANT_SCOPE_MISMATCH",
            f"tenant_id {tenant_id!r} not in CENSUS_ADMITTED_TENANT_IDS",
        )

    # Enqueue (persistent cursor entry per PHASE 3 A engine contract).
    census_run_id = enqueue_on_demand_run(
        tenant_id=tenant_id,
        connect_source_descriptor=connect_source_descriptor,
        lawful_basis_admit_ref=lawful_basis_admit_ref,
    )

    # Reconstruct the same job payload the scheduler would consume and
    # invoke the sealed engine synchronously in-request. This bypasses
    # the scheduler's poll-interval sleep so the exit-proof curl chain
    # can observe state progression without waiting up to 60s.
    job = {
        "census_run_id": census_run_id,
        "tenant_id": tenant_id,
        "trigger": "on_demand_synchronous",
        "connect_source_descriptor": dict(connect_source_descriptor),
        "lawful_basis_admit_ref": lawful_basis_admit_ref,
    }
    job_deadline = time.time() + budget_seconds_offset
    engine_result = run_bounded_census(job, job_deadline=job_deadline)

    # Auto-bridge refusal rows via the sealed A'''' adapter.
    banked_item_ids = bank_refusal_rows_via_adapter(
        census_run_id=census_run_id,
        tenant_id=tenant_id,
        driver=producer_driver,
    )

    # Return the current real state so the exit-proof curl can render
    # the running-card path (or the refused-with-actionable-items path).
    state = read_census_run_state(census_run_id)

    return {
        "census_run_id": census_run_id,
        "engine_status": engine_result.get("status"),
        "banked_item_ids": list(banked_item_ids),
        "state": state,
        "tenant_id": tenant_id,
        "principal_id": identity.user_id,
    }


@router.post(BANK_REFUSALS_ROUTE_PATH_TEMPLATE)
async def post_bank_refusals(
    request: Request,
    body: Dict[str, Any] = Body(default={}),
    census_run_id: str = Path(..., min_length=1, max_length=128),
):
    """POST /api/portal/census/runs/{census_run_id}/bank-refusals.

    Body:
      { "tenant_id": str, "producer_driver": str (optional) }

    Manual bridge invocation for an already-completed run: scans the
    sealed engine's refusal cursor for `census_run_id` and banks each
    row into the A'''-cont-A queue via the A'''' adapter.
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result

    tenant_id = body.get("tenant_id")
    producer_driver = body.get("producer_driver", _DEFAULT_PRODUCER_DRIVER)

    if not tenant_id or not isinstance(tenant_id, str):
        return _refusal(
            400, "BLOCKED_TENANT_SCOPE_MISMATCH", "tenant_id missing"
        )
    if not is_census_admitted_tenant(tenant_id):
        return _refusal(
            403, "BLOCKED_TENANT_SCOPE_MISMATCH",
            f"tenant_id {tenant_id!r} not admitted",
        )
    if producer_driver not in DATA_SOURCE_ADAPTER_DRIVER_CODES:
        return _refusal(
            400, "BLOCKED_LAWFUL_BASIS_MISSING",
            f"producer_driver {producer_driver!r} not in "
            f"{DATA_SOURCE_ADAPTER_DRIVER_CODES!r}",
        )

    banked_item_ids = bank_refusal_rows_via_adapter(
        census_run_id=census_run_id,
        tenant_id=tenant_id,
        driver=producer_driver,
    )
    return {
        "census_run_id": census_run_id,
        "tenant_id": tenant_id,
        "banked_item_ids": list(banked_item_ids),
        "principal_id": identity.user_id,
    }


@router.get(GPU_SPEND_ROUTE_PATH)
async def get_gpu_spend(request: Request):
    """GET /api/portal/census/gpu-spend.

    Returns verbatim `services.census_autonomy.gpu_spend_capture.
    capture_gpu_spend()` output. Never fabricates numbers per the
    sealed A''' contract.
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result

    payload = capture_gpu_spend()
    return {
        "principal_id": identity.user_id,
        "capture": payload,
    }
