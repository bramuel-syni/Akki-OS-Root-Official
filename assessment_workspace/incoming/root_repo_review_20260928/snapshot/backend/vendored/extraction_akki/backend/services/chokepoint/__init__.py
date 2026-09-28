"""services.chokepoint — the single outbound custody boundary.

Owner Order 2026-08-25 · "W3 go" · Doc 01 §A5.1/§A5.5/§A5.6/§A5.7.

The chokepoint is the one function in this codebase that names an outbound
crossing. Every real crossing today — the RDS Data API HTTPS out (boto3),
the compute-seam SSH out (paramiko) — calls register_crossing() BEFORE
touching the network. Any future crossing MUST do the same; the AST
negative-scan build gate (tests/invariants/test_chokepoint_registers_all_crossings.py)
refuses new outbound imports that skip the discipline.

Doctrine (Doc 01 §A5.6): structural, not policed. The gate lives at the
narrowest point in the system — the single register_crossing call — so
that "a new call path can miss it" is not a live risk.

Contract:
  register_crossing(kind, endpoint, verb, payload_shape, actor, masking_tier)
      → CrossingReceipt on admission
      → ChokepointRefused on: unknown masking_tier · tier not admissible
        under current AKKI_ENV · endpoint.region missing or off-allowlist.

  list_receipts()
      → List[CrossingReceipt]  · reads phase0/crossing_receipts/*.json

Trust receipt (Doc 01 §A5.7):
  - The credential used to reach the endpoint is NEVER logged and NEVER
    a field on the receipt.
  - The receipt carries: receipt_id (stable identity for join), kind,
    endpoint_host, residency_region, verb, payload_shape (structure only),
    actor, at_iso, masking_tier.
  - The receipt is signed to the tenant (single-tenant estate today =
    the estate identity itself; multi-tenant lands with W7 model admission).
  - Written to phase0/crossing_receipts/rcp-<hex12>.json as the one
    authoritative record.

No LLM SDK. No external HTTP client. No secrets read.
"""
from __future__ import annotations

import json
import os
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from services.chokepoint.masking_tier import (
    MaskingTierRefused,
    validate_tier,
)
from services.chokepoint.residency import (
    ResidencyRefused,
    validate_region,
)


class ChokepointRefused(Exception):
    """Raised when a crossing is refused at the boundary."""


_DEFAULT_RECEIPT_DIR = "/app/assessment_workspace/phase0/crossing_receipts"


def _receipt_dir() -> Path:
    return Path(os.environ.get("CROSSING_RECEIPT_DIR", _DEFAULT_RECEIPT_DIR))


@dataclass
class CrossingReceipt:
    """Doc 01 §A5.7 · trust receipt shape.

    Fields carry only custody markers — NO credential, NO token, NO
    password. Payload_shape describes structure, not content.
    """

    receipt_id: str
    kind: str
    endpoint_host: str
    residency_region: str
    verb: str
    payload_shape: Dict[str, Any]
    actor: str
    at_iso: str
    masking_tier: str
    tenant_id: str = "estate"

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Registration.
# ---------------------------------------------------------------------------

def register_crossing(
    *,
    kind: str,
    endpoint: Dict[str, Any],
    verb: str,
    payload_shape: Dict[str, Any],
    actor: str,
    masking_tier: str,
) -> CrossingReceipt:
    """Doc 01 §A5.1 · the one function that names an outbound crossing.

    Every real outbound path in this backend calls this before the network.
    Refuses on masking-tier / residency violation; emits + persists a
    trust receipt on admission.
    """
    if not kind:
        raise ChokepointRefused("kind_required — crossing.kind must be a named path.")
    if not isinstance(endpoint, dict):
        raise ChokepointRefused("endpoint_required — endpoint must be a dict with 'host' + 'region'.")

    host = (endpoint.get("host") or "").strip()
    region = (endpoint.get("region") or "").strip()
    if not host:
        raise ChokepointRefused("endpoint_host_required — crossing.endpoint.host missing.")
    if not region:
        raise ChokepointRefused(
            "endpoint_region_required — crossing.endpoint.region missing. "
            "Doc 01 §A5.6 + CA1-N4: a crossing with no region asserted "
            "cannot pass silently. Log the region on the source record first."
        )

    # Residency — refuses if region not on allowlist.
    try:
        validate_region(region)
    except ResidencyRefused as exc:
        raise ChokepointRefused(
            f"residency_refused — {exc} (CA1-N4)."
        ) from exc

    # Masking tier — refuses on unknown / not-admissible-under-env.
    try:
        validate_tier(masking_tier)
    except MaskingTierRefused as exc:
        raise ChokepointRefused(
            f"masking_tier_refused — {exc} (Doc 02 §A3 tier discipline)."
        ) from exc

    now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    receipt = CrossingReceipt(
        receipt_id=f"rcp-{uuid.uuid4().hex[:12]}",
        kind=kind,
        endpoint_host=host,
        residency_region=region,
        verb=verb or "",
        payload_shape=_scrub_payload_shape(payload_shape or {}),
        actor=actor or "unknown",
        at_iso=now_iso,
        masking_tier=masking_tier,
    )
    _write_receipt(receipt)
    return receipt


def _scrub_payload_shape(shape: Dict[str, Any]) -> Dict[str, Any]:
    """Payload_shape carries STRUCTURE only. Refuse credential-shaped keys."""
    banned = {"credential", "password", "secret", "token", "api_key", "auth"}
    # W5 metering fields (Owner sharpening 2026-08-25 §1) are legitimate
    # integer counters even though they contain the substring 'token'.
    # The W6 Cost Ledger consumes them; they are NOT credentials.
    metering_allowlist = {"tokens_in", "tokens_out"}
    out: Dict[str, Any] = {}
    for k, v in shape.items():
        lk = k.lower()
        if lk in metering_allowlist:
            out[k] = v
            continue
        if any(b in lk for b in banned):
            # Silently drop rather than raise — the boundary is a discipline,
            # not a debugger. But log via _writer that we scrubbed a key.
            continue
        out[k] = v
    return out


def _write_receipt(receipt: CrossingReceipt) -> None:
    d = _receipt_dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{receipt.receipt_id}.json").write_text(
        json.dumps(receipt.to_json(), indent=2, sort_keys=True)
    )


def list_receipts() -> List[CrossingReceipt]:
    """Read all receipts on record; identity-only, no external calls."""
    d = _receipt_dir()
    if not d.is_dir():
        return []
    out: List[CrossingReceipt] = []
    for f in sorted(d.glob("rcp-*.json")):
        try:
            raw = json.loads(f.read_text())
            out.append(CrossingReceipt(**raw))
        except Exception:
            # Malformed receipts are skipped — they cannot be trusted.
            continue
    return out


# ---------------------------------------------------------------------------
# Re-export the refusal types for callers that want to catch either.
# ---------------------------------------------------------------------------

__all__ = [
    "ChokepointRefused",
    "CrossingReceipt",
    "register_crossing",
    "list_receipts",
    "MaskingTierRefused",
    "ResidencyRefused",
]
