"""routers.canon_rules_registry · R-99 CP-LIFECYCLE-ENTITLEMENT-HTTP-SURFACE.

Wave R-99 (COMPLETION SPRINT step 4 of 6). Additive-only per SO §3.8:
authors a NEW read-only HTTP surface exposing the sealed R-96..R-98
canonical rule vocabularies as `GET /api/canon/rules/*` endpoints.

Consumes (identity import · zero sealed edit):
- `services.canon_dap_lifecycle.dap_tier_a_vocabulary` (DAP-1..30 · Tier A)
- `services.canon_dap_lifecycle.dap_tier_b_vocabulary` (DAP-31..38 · Tier B)
- `services.canon_rules_service.rbm_roc_vocabulary` (RBM-1..23 + ROC-1..11)

## RBM-8 endpoint (R-91 live evidence receipt)

Owner directive 2026-09-21T~06:35Z verbatim: "when you author RBM-8, its
invariant should reflect exactly that: ceremony windows are rigid, no
shortening path exists in code, and the R-91 window you are currently
honoring is the live evidence receipt." The `rbm-8-ceremony-mechanic`
endpoint surfaces all three sub-invariants byte-verbatim from the sealed
vocabulary. Any FE surface showing an R-91 ceremony countdown MUST
consume this endpoint verbatim to preserve owner's "countdown that cannot
be shortened" invariant (SO §6.6 · owner NO-EXPEDITE ruling 2026-09-21T~06:15Z).

Standing bounds: additive-only per SO §3.8 · zero external I/O · zero
subprocess · deterministic pure-read surface.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from services.canon_dap_lifecycle import (
    dap_tier_a_vocabulary as DAP_A,
    dap_tier_b_vocabulary as DAP_B,
)
from services.canon_rules_service import rbm_roc_vocabulary as V


router = APIRouter(prefix="/api/canon/rules", tags=["canon-rules-registry"])


# ═══════════════════════════════════════════════════════════════════════════
# Helpers · closed-vocab reflection over sealed Final[...] constants
# ═══════════════════════════════════════════════════════════════════════════


def _dap_rules() -> list[dict[str, Any]]:
    """Materialise DAP-1..38 registry from sealed Tier A + Tier B vocabularies."""
    rules: list[dict[str, Any]] = []
    tier_a_meta = DAP_A.DAP_TIER_A_ROW_SHARED_METADATA
    for rule_id in DAP_A.DAP_TIER_A_RULE_IDS:
        idx = int(rule_id.split("-")[1])
        rules.append({
            "rule_id": rule_id,
            "tier": "A",
            "srr_row": getattr(DAP_A, f"DAP_{idx}_SRR_ROW"),
            "statement": getattr(DAP_A, f"DAP_{idx}_STATEMENT"),
            "metadata": tier_a_meta,
        })
    for rule_id in DAP_B.DAP_TIER_B_RULE_IDS:
        idx = int(rule_id.split("-")[1])
        # Tier B rules share the same statement/srr_row lookup shape but split into 2 sub-metadata groups
        meta = DAP_B.DAP_TIER_B_SECURITY_AMENDMENT_METADATA if idx <= 36 else DAP_B.DAP_TIER_B_PRUNING_UNLEARNING_METADATA
        rules.append({
            "rule_id": rule_id,
            "tier": "B",
            "srr_row": getattr(DAP_B, f"DAP_{idx}_SRR_ROW"),
            "statement": getattr(DAP_B, f"DAP_{idx}_STATEMENT"),
            "metadata": meta,
        })
    return rules


def _rbm_rules() -> list[dict[str, Any]]:
    """Materialise RBM-1..23 registry from sealed Tier A + Tier B vocabulary."""
    rules: list[dict[str, Any]] = []
    for rule_id in V.RBM_TIER_A_RULE_IDS:
        idx = int(rule_id.split("-")[1])
        rules.append({
            "rule_id": rule_id,
            "tier": "A",
            "srr_row": getattr(V, f"RBM_{idx}_SRR_ROW"),
            "statement": getattr(V, f"RBM_{idx}_STATEMENT"),
            "metadata": V.RBM_TIER_A_METADATA,
        })
    for rule_id in V.RBM_TIER_B_RULE_IDS:
        idx = int(rule_id.split("-")[1])
        rules.append({
            "rule_id": rule_id,
            "tier": "B",
            "srr_row": getattr(V, f"RBM_{idx}_SRR_ROW"),
            "statement": getattr(V, f"RBM_{idx}_STATEMENT"),
            "metadata": V.RBM_TIER_B_METADATA,
        })
    return rules


def _roc_rules() -> list[dict[str, Any]]:
    """Materialise ROC-1..11 registry from sealed vocabulary."""
    rules: list[dict[str, Any]] = []
    for rule_id in V.ROC_RULE_IDS:
        idx = int(rule_id.split("-")[1])
        rules.append({
            "rule_id": rule_id,
            "srr_row": getattr(V, f"ROC_{idx}_SRR_ROW"),
            "statement": getattr(V, f"ROC_{idx}_STATEMENT"),
            "metadata": V.ROC_METADATA,
        })
    return rules


# ═══════════════════════════════════════════════════════════════════════════
# Endpoints
# ═══════════════════════════════════════════════════════════════════════════


@router.get("/dap")
def get_dap_registry() -> dict[str, Any]:
    """GET /api/canon/rules/dap · returns DAP-1..38 registry (Tier A + Tier B)."""
    rules = _dap_rules()
    return {
        "rule_count": len(rules),
        "tier_a_count": DAP_A.DAP_TIER_A_RULE_COUNT,
        "tier_b_count": 8,
        "tier_a_srr_row_start": DAP_A.DAP_TIER_A_SRR_ROW_START,
        "tier_a_srr_row_end": DAP_A.DAP_TIER_A_SRR_ROW_END,
        "authority": "Master Requirements Registry v5 SRR sheet · Ruling 5",
        "rules": rules,
    }


@router.get("/dap/{rule_id}")
def get_dap_rule(rule_id: str) -> dict[str, Any]:
    """GET /api/canon/rules/dap/{rule_id} · returns single DAP rule (404 on unknown)."""
    for rule in _dap_rules():
        if rule["rule_id"] == rule_id:
            return rule
    raise HTTPException(status_code=404, detail=f"Unknown DAP rule: {rule_id}")


@router.get("/rbm")
def get_rbm_registry() -> dict[str, Any]:
    """GET /api/canon/rules/rbm · returns RBM-1..23 registry (Tier A + Tier B)."""
    return {
        "rule_count": V.RBM_RULE_COUNT,
        "tier_a_count": V.RBM_TIER_A_RULE_COUNT,
        "tier_b_count": 1,
        "tier_a_srr_row_start": V.RBM_TIER_A_ROW_START,
        "tier_a_srr_row_end": V.RBM_TIER_A_ROW_END,
        "authority": "Master Requirements Registry v5 SRR sheet · Ruling 5",
        "rules": _rbm_rules(),
    }


@router.get("/roc")
def get_roc_registry() -> dict[str, Any]:
    """GET /api/canon/rules/roc · returns ROC-1..11 registry."""
    return {
        "rule_count": V.ROC_RULE_COUNT,
        "srr_row_start": V.ROC_ROW_START,
        "srr_row_end": V.ROC_ROW_END,
        "authority": "Master Requirements Registry v5 SRR sheet · Ruling 5",
        "rules": _roc_rules(),
    }


@router.get("/rbm-8-ceremony-mechanic")
def get_rbm_8_ceremony_mechanic() -> dict[str, Any]:
    """GET /api/canon/rules/rbm-8-ceremony-mechanic · R-91 live evidence receipt.

    Owner directive 2026-09-21T~06:35Z verbatim: "ceremony windows are rigid,
    no shortening path exists in code, and the R-91 window you are currently
    honoring is the live evidence receipt". FE surfaces displaying an R-91
    countdown MUST consume this endpoint byte-verbatim.
    """
    return {
        "rule_id": "RBM-8",
        "srr_row": V.RBM_8_SRR_ROW,
        "statement": V.RBM_8_STATEMENT,
        "is_r91_ceremony_anchor": V.RBM_8_IS_R91_CEREMONY_ANCHOR,
        "ceremony_window_is_rigid": V.RBM_8_CEREMONY_WINDOW_IS_RIGID,
        "no_shortening_path_in_code": V.RBM_8_NO_SHORTENING_PATH_IN_CODE,
        "r91_live_evidence_horizon_utc": V.RBM_8_R91_LIVE_EVIDENCE_HORIZON_UTC,
        "r91_is_live_evidence_receipt": V.RBM_8_R91_IS_LIVE_EVIDENCE_RECEIPT,
        "ceremony_shortening_watched_patterns": list(V.RBM_8_CEREMONY_SHORTENING_WATCHED_PATTERNS),
        "ceremony_shortening_watched_pattern_count": V.RBM_8_CEREMONY_SHORTENING_WATCHED_PATTERN_COUNT,
        "owner_directive_utc": "2026-09-21T06:35:00Z",
        "owner_no_expedite_ruling_utc": "2026-09-21T06:15:00Z",
        "owner_directive_verbatim": (
            "when you author RBM-8, its invariant should reflect exactly that: "
            "ceremony windows are rigid, no shortening path exists in code, and "
            "the R-91 window you are currently honoring is the live evidence receipt."
        ),
        "so_reference": "SO §6.6 · 'a countdown cut short is what FAIL looks like'",
    }
