"""services.tenant_separation.platform_operator · control-plane-only principal.

Owner card §6 verbatim (STATE/OBJECTIVES/TENANT_SEPARATION.md):

    "Admin account for systems testing — a principal, not a bypass.
    AKKI-TEST owner and seats hold full rights inside AKKI-TEST only.
    A platform-operator principal holds control-plane visibility —
    metadata, identity, scheduling, metering (D-18) — and:
    - no read of any tenant's source content
    - no write to any tenant's Ledger
    - no ability to approve any tenant's request
    Its actions are receipted like any principal's. Any admin capability
    that would read RMS or DigiCow content is out of spec."

Refusal contract: `PRIN-OP-001` refuses any capability outside the
control-plane scope against any customer tenant. Additive-only per SO
§3.8; closed-vocab per SO §3.10-α.
"""

from __future__ import annotations

import dataclasses
import datetime
import json
import pathlib
from typing import Any, Dict, Final, Tuple


# ═══════════════════════════════════════════════════════════════════════════
# Closed capability vocabulary per D-18 verbatim (control-plane scope)
# ═══════════════════════════════════════════════════════════════════════════

PLATFORM_OPERATOR_SCOPE_ALLOWED: Final[Tuple[str, ...]] = (
    "metadata",
    "identity",
    "scheduling",
    "metering",
)

PLATFORM_OPERATOR_SCOPE_DENIED: Final[Tuple[str, ...]] = (
    "content_read",
    "ledger_write",
    "request_approve",
)

PLATFORM_OPERATOR_REFUSAL_CODE: Final[str] = "PRIN-OP-001"


# ═══════════════════════════════════════════════════════════════════════════
# Evaluation contract
# ═══════════════════════════════════════════════════════════════════════════

@dataclasses.dataclass(frozen=True)
class PlatformOperatorVerdict:
    refused: bool
    refusal_code: str
    tenant_id: str
    capability: str
    rationale: str


def evaluate_platform_operator_capability(
    *, tenant_id: str, capability: str
) -> PlatformOperatorVerdict:
    """Evaluate a platform-operator capability against a customer tenant.

    Returns REFUSED with `PRIN-OP-001` if capability is not in the
    control-plane allowlist (owner card §6 verbatim).
    """
    allowed = set(PLATFORM_OPERATOR_SCOPE_ALLOWED)
    denied = set(PLATFORM_OPERATOR_SCOPE_DENIED)

    if capability in denied:
        return PlatformOperatorVerdict(
            refused=True,
            refusal_code=PLATFORM_OPERATOR_REFUSAL_CODE,
            tenant_id=tenant_id,
            capability=capability,
            rationale=(
                f"platform-operator scope forbids {capability!r} on tenant "
                f"{tenant_id!r} per owner card §6 verbatim + D-18 · control-plane "
                f"scope is {PLATFORM_OPERATOR_SCOPE_ALLOWED}"
            ),
        )
    if capability in allowed:
        return PlatformOperatorVerdict(
            refused=False,
            refusal_code="",
            tenant_id=tenant_id,
            capability=capability,
            rationale=(
                f"platform-operator scope admits {capability!r} on tenant "
                f"{tenant_id!r} (control-plane visibility per D-18)"
            ),
        )
    # Unknown capability → refuse-closed by construction (fail-CLOSED).
    return PlatformOperatorVerdict(
        refused=True,
        refusal_code=PLATFORM_OPERATOR_REFUSAL_CODE,
        tenant_id=tenant_id,
        capability=capability,
        rationale=(
            f"unknown platform-operator capability {capability!r} · fail-closed "
            f"per SO §3.8 · allowlist is {PLATFORM_OPERATOR_SCOPE_ALLOWED} · "
            f"denylist is {PLATFORM_OPERATOR_SCOPE_DENIED}"
        ),
    )


# ═══════════════════════════════════════════════════════════════════════════
# Receipt writer — owner card §6 verbatim "Its actions are receipted
# like any principal's."
# ═══════════════════════════════════════════════════════════════════════════

_RECEIPT_DIR = (
    pathlib.Path(__file__).resolve().parents[2]
    / "phase0"
    / "platform_operator_receipts"
)


def emit_platform_operator_action_receipt(
    *,
    tenant_id: str,
    capability: str,
    verdict: PlatformOperatorVerdict,
    action_utc: str = "",
) -> Dict[str, Any]:
    """Emit a receipt for a platform-operator action against a tenant.

    Receipt is disk-only; writer is safe under `Canon-9 §3 single-writer`
    (this is a metadata-plane observation, not an event on any tenant's
    Ledger). Returns the receipt dict.
    """
    when = action_utc or datetime.datetime.now(datetime.timezone.utc).isoformat(
        timespec="seconds"
    )
    receipt = {
        "receipt_kind": "platform_operator_action",
        "tenant_id": tenant_id,
        "capability": capability,
        "action_utc": when,
        "refused": verdict.refused,
        "refusal_code": verdict.refusal_code,
        "rationale": verdict.rationale,
    }
    _RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    fname = f"{when.replace(':', '')}_platform_operator_{tenant_id}_{capability}.json"
    (_RECEIPT_DIR / fname).write_text(json.dumps(receipt, indent=2, sort_keys=True))
    return receipt


__all__ = (
    "PLATFORM_OPERATOR_REFUSAL_CODE",
    "PLATFORM_OPERATOR_SCOPE_ALLOWED",
    "PLATFORM_OPERATOR_SCOPE_DENIED",
    "PlatformOperatorVerdict",
    "emit_platform_operator_action_receipt",
    "evaluate_platform_operator_capability",
)
