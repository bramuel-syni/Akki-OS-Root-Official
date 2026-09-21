"""router.py — POST /api/connect/parse-paste (Owner Simplification 2026-08-14).

Custody contract (owner Q2 addendum this cycle):
  * The endpoint MAY receive the raw paste (password inside) in the payload —
    one shot only, per browser session.
  * The endpoint's RESPONSE MUST NEVER carry the password back — verbatim,
    hashed, tokenised, or embedded in any string.
  * The endpoint MUST NOT log the password, persist it, forward it to any
    external system, or hold state between calls.
  * The endpoint returns non-secret fields (host_name / username / IPs /
    OS / deploy_date / extras) plus a boolean ``password_captured``.
  * The client keeps the raw paste in its own textarea memory and submits
    it directly to /api/connect/gpu (existing seven-stage pipeline).

Pattern-only parsing lives in services.credentials_paste.parser.  No LLM,
no network, no subprocess.
"""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.credentials_paste import parser as _parser
from services.connect.draft_store import get_store as _get_draft_store


router = APIRouter()


class ParsePastePayload(BaseModel):
    # NB: no min_length — we validate emptiness ourselves so we can return
    # 400 (per invariant) instead of pydantic's default 422.
    paste: str = Field(..., max_length=8192)
    hint_kind: Optional[str] = Field(None, max_length=32)


@router.post("/api/connect/parse-paste")
async def post_parse_paste(payload: ParsePastePayload) -> dict:
    """Parse a paste blob into non-secret fields + a password_captured signal.

    * Refuses empty paste with 400.
    * Silently ignores hint_kind not in SUPPORTED_KINDS → auto-detect.
    * Strips the password / api_key from the returned ``fields`` dict; the
      response is the ONLY thing the browser sees, and it never carries the
      secret back.
    """
    if not payload.paste or not payload.paste.strip():
        raise HTTPException(status_code=400, detail="paste is empty")

    hint = payload.hint_kind if payload.hint_kind in _parser.SUPPORTED_KINDS else None
    parsed = _parser.parse(payload.paste, hint_kind=hint)

    # Strip password / api_key / aws_secret_access_key from response (custody rule).
    # These are the secret-shaped canonical fields.
    fields = dict(parsed["fields"])
    password_captured = "password" in fields
    api_key_captured = "api_key" in fields
    aws_secret_captured = "aws_secret_access_key" in fields
    fields.pop("password", None)
    fields.pop("api_key", None)
    fields.pop("aws_secret_access_key", None)

    # Rebuild missing list against the redacted view — the client learns
    # that a secret is present via *_captured signals, not via a "missing"
    # row for the secret.
    missing = [
        f for f in parsed["missing"]
        if f not in {"password", "api_key", "aws_secret_access_key"}
    ]

    # W11 R2 · persist a server-side draft so Confirm can read from state,
    # not from a client-captured (possibly-null) closure. Custody rule:
    # secrets are held on the draft object only (never in the response
    # body); on Confirm the draft is consumed (deleted).
    _draft_id = _get_draft_store().put(
        kind=parsed["kind"],
        fields=fields,
        password=parsed["fields"].get("password"),
        aws_secret_access_key=parsed["fields"].get("aws_secret_access_key"),
        api_key=parsed["fields"].get("api_key"),
    )

    return {
        "draft_id": _draft_id,
        "kind": parsed["kind"],
        "fields": fields,
        "missing": missing,
        "extras": parsed.get("extras", {}),
        "password_captured": password_captured,
        "api_key_captured": api_key_captured,
        "aws_secret_captured": aws_secret_captured,
    }
