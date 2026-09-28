"""W-DAP-STACK 2B · API key kernel.

Canon anchor · DAP-Spec DAP-13 (verbatim): 'API keys are issued per party
principal, never per organisation, and carry the principal's mandate.  A
key MUST be revocable in a single act with immediate effect, MUST expire
on a stated lifetime (§10 R-4), and MUST NOT be transferable between
principals.  Key material is never written to any record, including
receipts and metered events.'

R-4 lifetime default: RATIFIED 2026-09-13 (C3 batch) — 90 days.
"""

from __future__ import annotations

import datetime
import secrets
from typing import Dict, Tuple

from contracts.dap import ApiKeyIssueReceipt
from services.dap.admission import get_party_principal


_KEYS: Dict[str, Dict] = {}  # key_id -> {principal_id, active, mandate, ...}


def issue_key(*, principal_id: str, lifetime_days: int = 90) -> Tuple[ApiKeyIssueReceipt, str]:
    """Issue an API key to a **party principal** (individual or agent).

    Raises ``ValueError`` if the id names an organisation-level principal —
    DAP-13 (per-principal, never per-organisation).

    Returns (receipt, key_material). The receipt is safe to record; the
    key material is returned OUT-OF-BAND and MUST NOT be written to any
    persistent record.
    """
    principal = get_party_principal(principal_id)
    if principal is None:
        raise ValueError(
            f"DAP-13 refusal: {principal_id!r} is not a per-principal id "
            f"(organisation ids cannot receive keys; per-principal required)"
        )
    key_id = f"apik_{secrets.token_hex(8)}"
    key_material = secrets.token_urlsafe(32)  # OUT-OF-BAND · not persisted here
    _KEYS[key_id] = {
        "principal_id": principal_id,
        "active": True,
        "mandate": principal.mandate,
        "lifetime_days": lifetime_days,
    }
    return (
        ApiKeyIssueReceipt(
            key_id=key_id,
            principal_id=principal_id,
            lifetime_seconds=lifetime_days * 86400,
        ),
        key_material,
    )


def revoke_key(key_id: str) -> None:
    """Single act, immediate effect. DAP-13."""
    if key_id in _KEYS:
        _KEYS[key_id]["active"] = False


def is_valid(key_id: str) -> bool:
    return _KEYS.get(key_id, {}).get("active", False)


def is_transferable(key_id: str) -> bool:
    """Constant False.  DAP-13: 'MUST NOT be transferable between principals.'"""
    return False


def reset_state() -> None:
    """Test-only helper."""
    _KEYS.clear()
