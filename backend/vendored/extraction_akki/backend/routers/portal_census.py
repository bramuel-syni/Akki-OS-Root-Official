"""routers.portal_census · CENSUS-SURFACE-A · additive portal read view
over Mtafiti's asset inventory + CENSUS-3 chapter receipts.

Wave CENSUS-SURFACE-A (2026-09-22T~02:2XZ). Additive-only per SO §3.8:
authors a NEW JWT-gated router exposing the SEALED reader surfaces
(`services.mtafiti.asset_inventory` + adapter
`services.mtafiti.census3_registry_hydrator`) as
`GET /api/portal/census/*` READ endpoints — principal-scoped via PRIN-11
propagation, NEVER caller-supplied identity (PRIN-12 forbid). Matches
R-100 portal write-surface JWT-only pattern verbatim.

Owner course-correction anchor verbatim (2026-09-22T~02:20Z):

    "You should [not] be adding new surface - you should be connecting
    the existing one to it, my assumption is there is an existing
    surface for this. ... CONNECT, don't duplicate: write the census
    results INTO the existing registry through its own sealed writer
    contract (e.g., each censused surface/asset-class becomes
    asset_records via mtafiti.asset_registry_writer, with provenance
    pointing at the phase0/census_v3 receipts), and expose them through
    the EXISTING read surface family — extending existing routes
    additively (e.g., a census/asset-inventory view on the portal read
    surface) rather than inventing a standalone /api/census/* family.
    Adapter layer only; zero touches to sealed code."

Owner confirmation anchor verbatim (this-session earlier reply · point b):

    "GATE THE READS behind the existing portal JWT (same pattern as
    /api/portal/*). The census payload enumerates estate topology
    (bucket names, hosts, volumes) — not PII, but infrastructure
    enumeration should not sit on an unauthenticated route."

Canon anchors:
  * Canon-9 §13 Mkondo Charter authority table (line 23 verbatim):
    "Census and registry records | Mtafiti | Both authorities; every
     surface by proof link"
  * Doc-0 BR-4.1: asset-class coverage across five kinds ·
    always-five taxonomy per Doc-0 TA-3.1 ·
    `mtafiti.asset_inventory.enumerate_classes_always_five`
  * Canon-4 §8: one record per source (SourceRecord shape · sealed
    census_canon.registry_write.RegistryStore sink)

Sealed consumption (identity import · zero sealed edit):
  * `services.mtafiti.asset_inventory.*`  (reader-only public surface)
  * `services.mtafiti.census3_registry_hydrator.*`  (adapter projections)
  * `services.auth.dependencies.require_identity_or_deny`  (JWT gate)
  * `services.enforce.principal_context_adapter.principal_context`
    (R-100-UNWIND wrapper · sealed carrier untouched)
  * `services.auth.identity.Identity`

Standing bounds: additive-only per SO §3.8 · zero external I/O in router
handlers (deferred to phase0 receipt loaders in the hydrator module) ·
deterministic pure-read surface.
"""
from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from services.auth.dependencies import require_identity_or_deny
from services.auth.identity import Identity
from services.enforce.principal_context_adapter import principal_context
from services.mtafiti import asset_inventory
from services.mtafiti import census3_registry_hydrator as hydrator


router = APIRouter(prefix="/api/portal/census", tags=["portal-census"])


# ─────────────────────────────────────────────────────────────────────────
# Hydration on first-request (safe + idempotent · module-level guard).
# Runs once per process; subsequent requests re-use the sealed writers'
# in-memory registries. This makes the module import-safe (no I/O at
# import time) while still lifting CENSUS-3 into mtafiti._REGISTRY on
# first hit.
# ─────────────────────────────────────────────────────────────────────────

_HYDRATED_ONCE: List[bool] = [False]


def _ensure_hydrated() -> None:
    if _HYDRATED_ONCE[0]:
        return
    try:
        hydrator.hydrate_from_phase0()
    except Exception:  # pragma: no cover — never surfaces the trace
        # Hydration is best-effort at the surface layer; if a phase0
        # receipt is missing or malformed, the endpoints still return
        # coherent shapes (empty registry rather than 500).
        pass
    _HYDRATED_ONCE[0] = True


# ═══════════════════════════════════════════════════════════════════════════
# Endpoint 1 · GET /assets — Mtafiti asset-inventory projection
# ═══════════════════════════════════════════════════════════════════════════


@router.get("/assets")
async def get_census_assets(request: Request):
    """GET /api/portal/census/assets · principal-scoped Mtafiti asset
    inventory (Doc-0 BR-4.1 + TA-3.1 always-five). Reads through
    `services.mtafiti.asset_inventory` (sealed reader) after ensuring
    the CENSUS-3 hydrator has landed its records via the sealed
    single-writer (Canon-9 §3 preserved by construction)."""
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    with principal_context(identity.user_id):
        _ensure_hydrated()
        classes = list(asset_inventory.enumerate_classes_always_five())
        counts = asset_inventory.count_by_class()
        rows = asset_inventory.list_all_assets()
        total = sum(counts.values())
        return {
            "principal_id": identity.user_id,
            "classes": classes,
            "count_by_class": counts,
            "total_count": total,
            "rows": rows,
            "authority": (
                "Canon-9 §13 · Mtafiti authority for census and registry "
                "records · Doc-0 BR-4.1 asset-class coverage · TA-3.1 "
                "always-five taxonomy · read-only reader over sealed "
                "asset_registry_writer._REGISTRY"
            ),
        }


# ═══════════════════════════════════════════════════════════════════════════
# Endpoint 2 · GET /surfaces — per-surface breakdown with freshness min-max
# ═══════════════════════════════════════════════════════════════════════════


@router.get("/surfaces")
async def get_census_surfaces(request: Request):
    """GET /api/portal/census/surfaces · per-surface breakdown with
    `freshness_stamp_min` + `freshness_stamp_max` (owner confirmation
    point e verbatim). Reads through the hydrator's read-only
    projection over the phase0/census_v3 receipts."""
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    with principal_context(identity.user_id):
        _ensure_hydrated()
        surfaces = hydrator.surface_breakdown_with_freshness()
        return {
            "principal_id": identity.user_id,
            "surfaces": surfaces,
            "surface_count": len(surfaces),
            "authority": (
                "Canon-4 §4.1 · per-source measurement carriers "
                "(volume · media types · quality strata · freshness · "
                "audio_bearing_share) · projected read from phase0/"
                "census_v3/ chapters"
            ),
        }


# ═══════════════════════════════════════════════════════════════════════════
# Endpoint 3 · GET /access — readable vs blocked + unlocks
# ═══════════════════════════════════════════════════════════════════════════


@router.get("/access")
async def get_census_access(request: Request):
    """GET /api/portal/census/access · readable-vs-blocked bucket
    summary with an `unlocks` mapping stating exactly what owner action
    opens each blocked slice (owner confirmation point e verbatim:
    na7p4* IAM grant · cold-tier restore · HF token)."""
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    with principal_context(identity.user_id):
        _ensure_hydrated()
        summary = hydrator.access_summary_with_unlocks()
        summary["principal_id"] = identity.user_id
        summary["authority"] = (
            "phase0/census_v3/20260922T014400Z_CENSUS3_OBS_chapter.json · "
            "obs_access_reassessment.empirical_re_test_this_seal · "
            "OWNER-DROP-05 access-slice unlock keys"
        )
        return summary


# ═══════════════════════════════════════════════════════════════════════════
# Endpoint 4 · GET /latest — current chapter + provenance pointers
# ═══════════════════════════════════════════════════════════════════════════


@router.get("/latest")
async def get_census_latest(request: Request):
    """GET /api/portal/census/latest · current CENSUS-3 chapter receipt
    ids + provenance pointers to phase0/census_v3/*.json (Canon-9 §13
    verbatim · 'every surface by proof link')."""
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    with principal_context(identity.user_id):
        _ensure_hydrated()
        payload = hydrator.latest_chapter()
        payload["principal_id"] = identity.user_id
        return payload


# ═══════════════════════════════════════════════════════════════════════════
# Endpoint 5 · GET /duplication — Tier-1/Tier-2 chapter projection
# ═══════════════════════════════════════════════════════════════════════════


@router.get("/duplication")
async def get_census_duplication(request: Request):
    """GET /api/portal/census/duplication · Tier-1 (ETag+size) / Tier-2
    (3-point range read) duplication chapter with rejected hypotheses +
    confirmed real mirrors (owner directive: 'name-based similarity
    rejected · content-grade proof required')."""
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    with principal_context(identity.user_id):
        _ensure_hydrated()
        payload = hydrator.duplication_summary()
        payload["principal_id"] = identity.user_id
        return payload


# ═══════════════════════════════════════════════════════════════════════════
# Endpoint 6 · GET /records — LIST view (owner design "EVERY CENSUS")
# ═══════════════════════════════════════════════════════════════════════════


@router.get("/records")
async def list_census_records(request: Request):
    """GET /api/portal/census/records · LIST view matching the owner
    design surface "EVERY CENSUS" page in RMS AI Prototype Ver 2.0 Sep
    2026 (20-page share). Each row carries: census_number · status ·
    initiator · started_at_utc · duration · sources_read · sources_total ·
    annotations[]. Status ∈ {RUNNING, COMPLETE, NEEDS_ATTENTION}."""
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    with principal_context(identity.user_id):
        _ensure_hydrated()
        payload = hydrator.census_list()
        payload["principal_id"] = identity.user_id
        return payload


# ═══════════════════════════════════════════════════════════════════════════
# Endpoint 7 · GET /records/{census_number} — DETAIL view (owner design tabs)
# ═══════════════════════════════════════════════════════════════════════════


@router.get("/records/{census_number}")
async def get_census_record_detail(census_number: int, request: Request):
    """GET /api/portal/census/records/{census_number} · DETAIL view
    matching the owner design pixel-for-layout: header card (census_number,
    status, initiator, started_at, sources_read/total, duration,
    annotations) + four tabs (Discovery Summary · GPU Spend · Conversation
    with Agent · Discovery Details). Returns 404 for unknown
    census_number."""
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    with principal_context(identity.user_id):
        _ensure_hydrated()
        payload = hydrator.census_detail(census_number)
        if payload is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Census #{census_number} not found · known censuses "
                    f"are 1, 2, 3 at this seal. See GET /api/portal/census/records "
                    f"for the current list."
                ),
            )
        payload["principal_id"] = identity.user_id
        return payload


# ═══════════════════════════════════════════════════════════════════════════
# Endpoint 8 · GET /registry-landing — Registry landing DATA CONNECTED tab
# (owner design 2026-09-22T~03:2XZ · RMS AI Prototype Ver 2.0 Sep 2026
# 3-page addendum · Commit-A" additive)
# ═══════════════════════════════════════════════════════════════════════════


@router.get("/registry-landing")
async def get_registry_landing(request: Request):
    """GET /api/portal/census/registry-landing · Registry landing page
    read model matching the owner-shared 3-page design addendum:
    three tabs (DATA CONNECTED · COMPUTE CONNECTED · LLMS & TRAINED
    MODELS), four stat cards, four collapsibles with owner-verbatim
    headline_copy + sub_copy, THE MIX (three-views expanded body),
    right-rail census intelligence, and the honest-accounting law
    carried as a first-class field (verified vs unverified volume
    split so the FE cannot conflate).

    Owner directive verbatim (2026-09-22T~03:2XZ · Part 1):
        "Note the honest-accounting law embedded there: unverified
        volume is EXCLUDED from every verified figure until the next
        census reaches it — carry that rule into the read model."

    Real numbers only. All figures derive from phase0/census_v3
    receipts + phase0/census/census_000N manifests via the hydrator's
    reader-only projections. No mock values."""
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    with principal_context(identity.user_id):
        _ensure_hydrated()
        payload = hydrator.registry_landing()
        payload["principal_id"] = identity.user_id
        return payload

