"""services.chat.router — Chat surface router.

POST /api/chat/ask — one question / one answer through the LLM
chokepoint. Refusals surface verbatim (A8-Q3).
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from services.chokepoint import llm as _chokepoint_llm
from services.chokepoint.llm import LLMShieldFailure, PurposeInvalid
# W11 R4.8 · Doc19A-005 verbatim: 'every worker output passes through the
# Critic Seam; shipped-without-seam is a defect'.
from services.critic_pass import producer_seam as _critic_seam


router = APIRouter()


class AskRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    question: str = Field(..., min_length=1, max_length=4000)
    actor: str = Field(default="operator@estate", max_length=200)
    model: str = Field(default="gpt-5-mini", max_length=64)
    provider: str = Field(default="emergent", max_length=32)


@router.post("/api/chat/ask")
async def post_chat_ask(body: AskRequest) -> Dict[str, Any]:
    """One-question / one-answer chat. Every submit transits the LLM
    chokepoint.

    Response shape:
      {
        "answer":         str,  # empty on refusal
        "receipt_id":     str,  # rcp-<hex12>
        "model_id":       str,
        "provider":       str,
        "tokens_in":      int,
        "tokens_out":     int,
        "latency_ms":     int,
        "refused":        bool,
        "refusal_reason": str,  # verbatim (A8-Q3)
      }
    """
    try:
        resp = await _chokepoint_llm.invoke(
            purpose="chat.governed_answer",
            prompt=body.question,
            masking_tier="llm_prompt_governed_text",
            actor=body.actor,
            model=body.model,
            provider=body.provider,
            tenant_id=body.actor or "unknown",  # M12-W1e: actor as tenant scope
            custody_class="tenant_estate",  # M12-W1e: real estate work
        )
    except (LLMShieldFailure, PurposeInvalid) as exc:
        # A8-Q3 · surface the refusal verbatim.
        return {
            "answer": "",
            "receipt_id": "",
            "model_id": "",
            "provider": "",
            "tokens_in": 0,
            "tokens_out": 0,
            "latency_ms": 0,
            "refused": True,
            "refusal_reason": str(exc)[:400],
        }

    return {
        "answer": resp.text,
        "receipt_id": resp.receipt_id,
        "model_id": resp.model_id,
        "provider": resp.provider,
        "tokens_in": resp.tokens_in,
        "tokens_out": resp.tokens_out,
        "latency_ms": resp.latency_ms,
        "refused": False,
        "refusal_reason": "",
        # W11 R4.8 · Doc19A-005 producer-side seam attestation.
        # QA-1 preserves execution; findings are DATA, never a gate.
        "critic_verdict": _critic_seam.verdict_summary(
            _critic_seam.route_through_seam(
                artifact_ref=f"chat:{resp.receipt_id}",
                artifact_content=resp.text,
                producing_instance_id=f"chat.{body.provider}.{body.model}",
            )
        ),
    }
