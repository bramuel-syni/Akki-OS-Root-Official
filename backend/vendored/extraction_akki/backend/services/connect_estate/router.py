"""services/connect_estate/router.py - wizard provisioning card + non-compute intent.

Two endpoints on one router:
  GET  /api/connect/estate-facts  -> the provisioning card: public key,
                                     fingerprint, pod egress IP, provenance
                                     sentences. Rendered by the wizard
                                     BEFORE credentials are keyed, so the
                                     operator can install the public key
                                     into the VM at creation and add both
                                     /32 rows (their IP + pod egress).
  POST /api/connect/intent        -> record a non-compute connection intent
                                     (kind in {data-source, llm, trained-model}).
                                     Writes a JSON receipt to INTENT_RECORDS_DIR.
                                     Compute (kind='compute') is refused: it
                                     uses the seven-stage /api/connect/gpu.

Owner course-correction 2026-08-14 (fixture-drop follow-on).
"""
from __future__ import annotations

import json
import os
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.estate_keys import keypair as _keypair


router = APIRouter(prefix="/api/connect", tags=["connect-estate"])


# -------------------------- GET /estate-facts --------------------------


def _pod_egress_ip() -> tuple[str, str]:
    """Return (egress_ip, provenance_sentence) for the provisioning card.

    Prefer env var POD_EGRESS_IP (test/deterministic); fall back to
    live-discovery via ifconfig.me (best-effort).
    """
    env = os.environ.get("POD_EGRESS_IP")
    if env:
        return env, f"declared from env: POD_EGRESS_IP={env}"
    try:
        out = subprocess.run(
            ["curl", "-sS", "--max-time", "5", "https://ifconfig.me"],
            capture_output=True, text=True, timeout=8, check=True,
        )
        ip = out.stdout.strip()
        return ip, f"live-discovered from ifconfig.me at {datetime.now(timezone.utc).isoformat()}"
    except Exception as e:
        return "unknown", f"could not discover live egress: {e!s}"


@router.get("/estate-facts")
def estate_facts() -> dict:
    kp = _keypair.ensure_keypair()
    egress_ip, egress_prov = _pod_egress_ip()
    provenance = [
        "The estate holds one ed25519 keypair; the private key never leaves the pod's key custody.",
        "The public key below is safe to paste into the VM's SSH Public Key field at creation.",
        f"Pod egress IP {egress_prov}.",
        "Add both your operator /32 and this pod egress /32 to the VM's Security Group SSH rules.",
    ]
    return {
        "estate_public_key": kp["public_openssh"],
        "estate_public_key_fingerprint": kp["fingerprint"],
        "pod_egress_ip": egress_ip,
        "provenance": provenance,
    }


# -------------------------- POST /intent --------------------------


ALLOWED_INTENT_KINDS = ("data-source", "llm", "trained-model")


class IntentRequest(BaseModel):
    kind: Literal["data-source", "llm", "trained-model", "compute"]
    name: str = Field(min_length=1)
    description: Optional[str] = ""


def _intent_dir() -> Path:
    raw = os.environ.get("INTENT_RECORDS_DIR", "/app/assessment_workspace/phase0/intent_records")
    d = Path(raw)
    d.mkdir(parents=True, exist_ok=True)
    return d


@router.post("/intent")
def record_intent(body: IntentRequest) -> dict:
    if body.kind == "compute":
        raise HTTPException(
            status_code=400,
            detail=(
                "Compute (GPU) connections do not record intent here; they run through "
                "the seven-stage pipeline at /api/connect/gpu."
            ),
        )
    if not body.name.strip():
        raise HTTPException(status_code=400, detail="Connection must be named (§5 Step 4).")

    now = datetime.now(timezone.utc)
    ts = now.strftime("%Y%m%dT%H%M%SZ")
    receipt = {
        "id": str(uuid.uuid4()),
        "kind": body.kind,
        "name": body.name.strip(),
        "description": (body.description or "").strip(),
        "status": "recorded",
        "message": "Recorded - this connection type goes live with its wave.",
        "created_at": now.isoformat(),
    }
    d = _intent_dir()
    path = d / f"intent_{body.kind}_{ts}_{receipt['id'][:8]}.json"
    path.write_text(json.dumps(receipt, indent=2))
    return {
        "intent_receipt_path": str(path),
        "status": "recorded",
        "message": receipt["message"],
        "ledger_entry": receipt,
    }
