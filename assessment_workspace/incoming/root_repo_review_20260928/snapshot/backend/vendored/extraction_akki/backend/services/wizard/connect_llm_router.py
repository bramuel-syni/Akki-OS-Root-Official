"""services.wizard.connect_llm_router — Connect-LLM chip wizard (W5 CP4).

Owner sharpening §2: BYO-provider verification transits the chokepoint;
egress allowlist gains the provider host ONLY on successful verify.

Owner sharpening §3: custody file is .json (not .pem) — same shape as
estate_keys/aws_*.json (0600, gitignored, NEVER in responses).

Flow:
    POST /api/wizard/connect-llm/parse-paste  {paste}
      → detects provider by shape (sk-ant-* / sk-proj-* / sk-* / AIza*)
      → holds key in-process by connection_id (module-local dict)
      → response: {detected_provider, key_captured, preview_shape,
                   connection_id}
      → response NEVER carries the raw key ("•••• captured" only)

    POST /api/wizard/connect-llm/verify {connection_id}
      → invokes chokepoint.llm.invoke(purpose=llm.connect_verify) with
        a minimal governed prompt using the pasted key
      → on success:
          * writes estate_keys/llm_<provider>_<id>.json (0600)
          * writes data_connection_records/data_source_llm_<provider>_<id>_FINAL.json
          * removes the in-process key holder
      → on refusal: no persistence, connection_id retained for retry
      → response NEVER carries the raw key
"""
from __future__ import annotations

import json
import os
import re
import stat
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field


router = APIRouter()


# ---------------------------------------------------------------------------
# In-process key holder (transient — cleared on verify success/retry).
# ---------------------------------------------------------------------------

_KEY_HOLDER: Dict[str, Dict[str, str]] = {}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# ---------------------------------------------------------------------------
# Provider detection.
# ---------------------------------------------------------------------------

_PROVIDER_PATTERNS = [
    ("anthropic", re.compile(r"\b(sk-ant-[A-Za-z0-9_\-]{20,})\b")),
    ("openai",    re.compile(r"\b(sk-proj-[A-Za-z0-9_\-]{20,})\b")),
    ("openai",    re.compile(r"\b(sk-[A-Za-z0-9_\-]{40,})\b")),
    ("gemini",    re.compile(r"\b(AIza[A-Za-z0-9_\-]{20,})\b")),
]


def _detect_provider_and_key(paste: str) -> tuple[Optional[str], Optional[str]]:
    """Return (provider, key) or (None, None) if no key shape found."""
    if not isinstance(paste, str) or not paste.strip():
        return None, None
    for provider, rx in _PROVIDER_PATTERNS:
        m = rx.search(paste)
        if m:
            return provider, m.group(1)
    return None, None


# ---------------------------------------------------------------------------
# Custody.
# ---------------------------------------------------------------------------

def _estate_keys_dir() -> Path:
    return Path(os.environ.get("ESTATE_KEYS_DIR", "/app/backend/estate_keys"))


def _dcr_dir() -> Path:
    return Path(os.environ.get(
        "DATA_CONNECTION_RECORD_DIR",
        "/app/assessment_workspace/phase0/data_connection_records",
    ))


def _write_custody(provider: str, connection_id: str, key: str, verified_receipt_id: str) -> Path:
    d = _estate_keys_dir()
    d.mkdir(parents=True, exist_ok=True)
    fp = d / f"llm_{provider}_{connection_id}.json"
    fp.write_text(json.dumps({
        "provider": provider,
        "connection_id": connection_id,
        "key": key,
        "connected_at": _now_iso(),
        "verified_at": _now_iso(),
        "verified_receipt_id": verified_receipt_id,
    }, indent=2, sort_keys=True))
    os.chmod(fp, stat.S_IRUSR | stat.S_IWUSR)  # 0600
    return fp


def _write_connection_record(provider: str, connection_id: str,
                              verified_receipt_id: str,
                              model_id: str) -> Path:
    d = _dcr_dir()
    d.mkdir(parents=True, exist_ok=True)
    now = _now_iso()
    record = {
        "source_id": f"llm-{provider}-{connection_id}",
        "engine": "llm",
        "provider": provider,
        "name": f"{provider.capitalize()} (byo-key)",
        "resource": {
            "region": {"anthropic": "us-east-1", "openai": "us-east-1",
                       "gemini": "us-central1"}.get(provider, "unknown"),
        },
        "channel": "byo-key",
        "link_working": True,
        "at": now,
        "connected_at": now,
        "verified_at": now,
        "verified_receipt_id": verified_receipt_id,
        "custody_kind": "estate_keys_file",
    }
    fp = d / f"data_source_llm_{provider}_{connection_id}_FINAL.json"
    fp.write_text(json.dumps(record, indent=2, sort_keys=True))
    return fp


# ---------------------------------------------------------------------------
# Endpoint models.
# ---------------------------------------------------------------------------

class ParsePasteRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    paste: str = Field(..., min_length=1, max_length=8000)
    connection_hint: Optional[str] = None


class VerifyRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    connection_id: str = Field(..., min_length=1, max_length=64)


# ---------------------------------------------------------------------------
# Endpoints.
# ---------------------------------------------------------------------------

@router.post("/api/wizard/connect-llm/parse-paste")
async def parse_paste(body: ParsePasteRequest) -> Dict[str, Any]:
    """Deterministic paste parser · never returns the raw key."""
    provider, key = _detect_provider_and_key(body.paste)
    if not provider or not key:
        return {
            "detected_provider": None,
            "key_captured": False,
            "preview_shape": "",
            "connection_id": "",
            "note": "No provider key shape detected. Paste an Anthropic sk-ant-*, OpenAI sk-*, or Gemini AIza* key.",
        }

    connection_id = uuid.uuid4().hex[:12]
    _KEY_HOLDER[connection_id] = {"provider": provider, "key": key}
    return {
        "detected_provider": provider,
        "key_captured": True,
        "preview_shape": "•••• captured",  # v7 UX — masks from the first parse turn
        "connection_id": connection_id,
    }


@router.post("/api/wizard/connect-llm/verify")
async def verify_connection(body: VerifyRequest) -> Dict[str, Any]:
    """One-shot governed verify · transits the chokepoint · writes
    custody + connection record ONLY on success."""
    holder = _KEY_HOLDER.get(body.connection_id)
    if not holder:
        raise HTTPException(
            status_code=404,
            detail=f"connection_id {body.connection_id!r} not on the in-process key holder. "
                   "Re-paste to start a fresh verification.",
        )
    provider = holder["provider"]
    key = holder["key"]

    from services.chokepoint import llm as _chokepoint_llm
    from services.chokepoint.llm import LLMShieldFailure, PurposeInvalid

    # For BYO providers we need the key on-disk BEFORE the chokepoint can
    # resolve it (llm._byo_provider_key reads from estate_keys). We stage
    # the key in a temp custody file INSIDE this handler and remove it
    # if verify fails.
    #
    # NOTE: for the emergent provider, the chokepoint reads from env
    # (EMERGENT_LLM_KEY); we don't stage anything.
    staged_path: Optional[Path] = None
    if provider != "emergent":
        d = _estate_keys_dir()
        d.mkdir(parents=True, exist_ok=True)
        staged_path = d / f"llm_{provider}_{body.connection_id}.json"
        staged_path.write_text(json.dumps({
            "provider": provider,
            "connection_id": body.connection_id,
            "key": key,
            "connected_at": _now_iso(),
            "verified_at": None,
            "verified_receipt_id": None,
        }))
        os.chmod(staged_path, stat.S_IRUSR | stat.S_IWUSR)

    try:
        resp = await _chokepoint_llm.invoke(
            purpose="llm.connect_verify",
            prompt="Reply with a single word: ok.",
            masking_tier="llm_prompt_governed_text",
            actor="wizard@estate",
            model="claude-haiku-4-5-20251001" if provider == "anthropic" else (
                "gpt-5-mini" if provider == "openai" else (
                "gemini-2.5-flash" if provider == "gemini" else "gpt-5-mini")
            ),
            provider=provider,
            tenant_id="__connect_verify__",  # M12-W1e · synthetic tenant scope (R-25)
            custody_class="synthetic",  # M12-W1e · zero-content connectivity self-check
        )
    except (LLMShieldFailure, PurposeInvalid) as exc:
        # Clean up staged custody on refusal.
        if staged_path and staged_path.exists():
            staged_path.unlink()
        return {
            "verified": False,
            "receipt_id": "",
            "model_id": "",
            "provider": provider,
            "refused": True,
            "refusal_reason": str(exc)[:400],
        }

    # Success — finalise custody + connection record.
    if provider != "emergent":
        _write_custody(provider, body.connection_id, key, resp.receipt_id)  # overwrites the staged one with verified metadata
    _write_connection_record(provider, body.connection_id, resp.receipt_id, resp.model_id)

    # Clear the in-process holder — key is no longer needed there.
    _KEY_HOLDER.pop(body.connection_id, None)

    return {
        "verified": True,
        "receipt_id": resp.receipt_id,
        "model_id": resp.model_id,
        "provider": provider,
        "refused": False,
        "refusal_reason": "",
    }
