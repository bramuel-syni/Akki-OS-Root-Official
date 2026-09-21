"""services.chokepoint.llm — the SOLE LLM invocation seat in this backend.

Owner Order 2026-08-25 · "W5 go" §4:
    "Every model call crosses the W3 chokepoint: single invoke function,
     crossing receipt per call (model, purpose, masked-tier, tokens/
     metering, region of provider), egress allowlist extended ONLY for
     the provider host(s) at the chokepoint, AST gate updated so no LLM
     SDK import exists outside the chokepoint module."

Owner ruling 2026-08-25 · plan confirmation sharpening §1:
    "Receipt shape: make sure the crossing receipt carries METERING
     (input/output tokens, model id, latency) — it was in the W5 brief
     and is what makes the Shield's spend story real later (W6 Cost
     Ledger consumes it)."

Owner ruling 2026-08-25 · plan confirmation sharpening §2:
    "BYO-provider verification (2a): the one-shot verify call must
     itself transit the chokepoint, and the egress allowlist gains a
     provider host ONLY at the moment a key of that provider is
     actually connected."

Owner correction 2026-08-25 · canon vocabulary is Solva. Purpose IDs
    are `solva.frame_audit`, etc.

Doc 01 §A5.1 · The single chokepoint:
    "There is exactly one function in the entire codebase that invokes
     the external model client. Every outbound model call — from any
     engine, any application, any task — is made through that one
     function."

Doc 01 §A5.6 · Structural, not policed:
    The AST negative-scan (test_llm_chokepoint_sole_importer) refuses
    any file EXCEPT this one to import an LLM SDK.

Contract:
    invoke(*, purpose, prompt, masking_tier, actor, model, provider,
           system_message=None, session_id=None)
        → LLMResponse (text, receipt_id, model_id, provider, tokens_in,
                       tokens_out, latency_ms)
        raises: PurposeInvalid          (from llm_purpose_gate)
                MaskingTierRefused      (from masking_tier)
                LLMEndpointRefused      (from llm_endpoint_allowlist)
                ChokepointRefused       (from register_crossing on receipt write)
                LLMShieldFailure        (upstream provider error — non-canned)

Sequence per call:
    1. validate_purpose(purpose)              -- purpose gate
    2. validate_tier(masking_tier)            -- W3 tier discipline
    3. resolve_endpoint(provider)             -- connection-scoped egress
    4. _scrub_credential_shaped_prompt(prompt) -- standing rule: no
       credentials transit to the model (defense-in-depth on top of tier)
    5. START = perf_counter()                 -- boundary-wall latency
    6. client = _client_factory(...)          -- test-injectable seam
    7. response_text = await client.send_message(UserMessage(prompt))
    8. latency_ms = int((perf_counter - START) * 1000)
    9. tokens_in, tokens_out = _extract_metering(client, response_text)
    10. receipt = register_crossing(kind, endpoint, verb, payload_shape={
            model_id, provider, tokens_in, tokens_out, latency_ms,
            purpose_declared, ...}, actor, masking_tier)
    11. return LLMResponse(...)

THIS module is the ONE and ONLY location that may import
`emergentintegrations` or any other LLM SDK. The AST invariant refuses
any other file that carries an `emergentintegrations` import.
"""
from __future__ import annotations

import asyncio
import logging
import os
import re
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional

# THE SANCTIONED LLM SDK IMPORT.
from emergentintegrations.llm.chat import LlmChat, UserMessage  # noqa: WPS433

from services.chokepoint import register_crossing, ChokepointRefused
from services.chokepoint.llm_endpoint_allowlist import (
    LLMEndpointRefused,
    resolve_endpoint,
)
from services.chokepoint.llm_purpose_gate import (
    PurposeInvalid,
    validate_purpose,
)
from services.chokepoint.masking_tier import (
    MaskingTierRefused,
    validate_tier,
)

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Response contract.
# ---------------------------------------------------------------------------

@dataclass
class LLMResponse:
    """Return shape of `invoke()`.

    Carries model + provider + metering explicitly so surfaces can render
    provenance (Owner sharpening §4) without re-reading the receipt file.
    """

    text: str
    receipt_id: str
    model_id: str
    provider: str
    tokens_in: int
    tokens_out: int
    latency_ms: int
    purpose: str


class LLMShieldFailure(RuntimeError):
    """Raised when the LLM call itself fails upstream.

    The surface renders honest refusal from this — never a canned answer.
    """


# ---------------------------------------------------------------------------
# Credential-shaped prompt scrub (Owner Order §6 standing rule).
# ---------------------------------------------------------------------------

# Grammar aligned with the rest of the estate's credential detectors:
_CREDENTIAL_PATTERNS = [
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),                  # AWS access key
    re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}\b"),       # Anthropic key
    re.compile(r"\bsk-proj-[A-Za-z0-9_\-]{20,}\b"),      # OpenAI project key
    re.compile(r"\bsk-[A-Za-z0-9_\-]{40,}\b"),           # OpenAI classic key
    re.compile(r"\bAIza[A-Za-z0-9_\-]{35}\b"),           # Gemini/Google API key
    re.compile(r"\bxox[bpoa]-[A-Za-z0-9\-]{10,}\b"),     # Slack tokens
    re.compile(r"\bghp_[A-Za-z0-9]{36,}\b"),             # GitHub PAT
    re.compile(r"\bsk-emergent-[A-Za-z0-9]{16,}\b"),     # Emergent universal
]


class CredentialShapedPromptRefused(ChokepointRefused):
    """Raised when a prompt carries credential-shaped material.

    Owner Order §6: 'No raw credential/secret material may ever reach a
    model (standing rule; test it).'
    """


def _scrub_credential_shaped_prompt(prompt: str) -> None:
    """Refuse the crossing if the prompt carries credential-shaped material.

    Defense-in-depth: this is on TOP of the tier discipline. A tier can
    admit non-row-bearing text; a credential-shaped token within that
    text is still refused.
    """
    if not isinstance(prompt, str):
        raise CredentialShapedPromptRefused(
            f"prompt_not_string — got {type(prompt).__name__}"
        )
    for rx in _CREDENTIAL_PATTERNS:
        m = rx.search(prompt)
        if m:
            raise CredentialShapedPromptRefused(
                "prompt_carries_credential_shaped_material — refused at the "
                "chokepoint. Standing rule (Owner Order 2026-08-25 §6): no "
                "raw credential/secret material may ever reach a model. "
                f"Pattern matched: {rx.pattern[:40]}... — scrub before invoke."
            )


# ---------------------------------------------------------------------------
# Test-injectable LlmChat factory seam.
# ---------------------------------------------------------------------------

def _client_factory(**kwargs) -> Any:
    """Instantiate the emergentintegrations LlmChat.

    Tests replace this via monkeypatch to inject a fake client.
    """
    api_key = kwargs.pop("api_key")
    session_id = kwargs.pop("session_id")
    system_message = kwargs.pop("system_message")
    return LlmChat(
        api_key=api_key,
        session_id=session_id,
        system_message=system_message,
    )


def _extract_metering(prompt: str, response_text: Any, client: Any) -> tuple[int, int, str]:
    """Pull tokens_in / tokens_out via boundary-side counting.

    emergentintegrations.LlmChat.send_message() returns a bare string
    with NO usage metadata exposed on the client instance. So the
    chokepoint counts tokens itself using tiktoken (cl100k_base
    encoding) — accurate for OpenAI models, an honest approximation
    for Anthropic / Gemini until W6 wires provider-specific counters.

    Returns (tokens_in, tokens_out, metering_source).
    metering_source names the counter so the W6 Cost Ledger can weight
    receipts by counter fidelity (`tiktoken:cl100k_base` = approximate
    for non-OpenAI providers).
    """
    # First check the client for exposed usage (some SDK versions).
    for attr_name in ("_last_usage", "last_usage", "usage", "_usage"):
        usage = getattr(client, attr_name, None)
        if isinstance(usage, dict):
            tin = usage.get("input_tokens") or usage.get("prompt_tokens") or 0
            tout = usage.get("output_tokens") or usage.get("completion_tokens") or 0
            try:
                tin = int(tin)
                tout = int(tout)
                return max(0, tin), max(0, tout), "sdk_reported"
            except (TypeError, ValueError):
                pass

    # Fallback: boundary-side count via tiktoken.
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        tin = len(enc.encode(str(prompt))) if prompt else 0
        tout = len(enc.encode(str(response_text))) if response_text else 0
        return tin, tout, "tiktoken:cl100k_base"
    except Exception as exc:  # noqa: BLE001
        log.warning("tiktoken metering failed (%s) — returning zero", type(exc).__name__)
        return 0, 0, "unavailable"


def _kind_from_purpose(purpose: str) -> str:
    """Map purpose → receipt kind (used by Reasoning Shield filters).

    Owner correction 2026-08-25 · Solva vocabulary.
    """
    if purpose == "solva.frame_audit":
        return "solva_frame_audit"
    if purpose == "solva.candidate_generation":
        return "solva_candidate_generation"
    if purpose == "solva.synthesis":
        return "solva_synthesis"
    if purpose == "thinklab.direct_answer":
        return "thinklab_direct_answer"
    if purpose == "chat.governed_answer":
        return "chat_governed_answer"
    if purpose == "llm.connect_verify":
        return "llm_connect_verify"
    return "llm_synthesis"


def _emergent_api_key() -> str:
    """Read the Emergent universal key from env.

    Custody: env-var only; never returned to callers, never logged.
    """
    key = os.environ.get("EMERGENT_LLM_KEY", "").strip()
    if not key:
        raise LLMShieldFailure(
            "emergent_key_absent — EMERGENT_LLM_KEY not in environment. "
            "The Emergent-universal LLM connection is not on record."
        )
    return key


# ---------------------------------------------------------------------------
# THE INVOKE FUNCTION — one function, one seat, one crossing.
# ---------------------------------------------------------------------------

async def invoke(
    *,
    purpose: str,
    prompt: str,
    masking_tier: str,
    actor: str,
    model: str,
    provider: str,
    tenant_id: str,
    custody_class: str,
    system_message: Optional[str] = None,
    session_id: Optional[str] = None,
) -> LLMResponse:
    """The one function that invokes an external model client.

    Doc 01 §A5.1 · exactly one function invokes the external model client.
    Doc 01 §A5.6 · structural impossibility, not policed prohibition.

    M12-W1d (2026-09-18) · Option D per Owner R-25:
      * `tenant_id` is REQUIRED (no Optional, no default). An empty
        tenant_id refuses per FP-2 (unresolvable gate refuses).
      * `custody_class` is REQUIRED. Accepted values: `"tenant_estate"`
        (real estate work) and `"synthetic"` (connectivity self-check;
        payload carries no estate content). Any other value refuses.
      * No bypass parameter exists. No conditional guards the custody
        call. The custody sequence ALWAYS runs; for synthetic payloads
        it runs as a verified no-op.
      * The Watch input-seat emit (W1f emitter) fires on every crossing
        BEFORE dispatch. A crossing that cannot be observed does not
        happen (fail-closed).
    """
    # M12-W1d · Option D pre-flight: tenant_id + custody_class REQUIRED.
    if not tenant_id or not isinstance(tenant_id, str):
        raise ChokepointRefused(
            "tenant_id_required — invoke() refuses without a tenant scope. "
            "A crossing with no tenant scope cannot resolve custody class "
            "or terms (canon 3 §14 · FP-2 unresolvable gate refuses)."
        )
    _ACCEPTED_CUSTODY_CLASSES = {"tenant_estate", "synthetic"}
    if custody_class not in _ACCEPTED_CUSTODY_CLASSES:
        raise ChokepointRefused(
            f"custody_class_invalid — got {custody_class!r}, "
            f"expected one of {sorted(_ACCEPTED_CUSTODY_CLASSES)}. "
            "Every crossing must declare a custody class (Option D · R-25)."
        )

    # 1. Purpose gate (Owner Order §5 · Ruling 1).
    validate_purpose(purpose)  # raises PurposeInvalid

    # 2. Credential scrub (Owner Order §6 standing rule) — moved BEFORE
    # tier / endpoint resolution because credential-shaped material must
    # never reach the network path regardless of provider or tier state.
    _scrub_credential_shaped_prompt(prompt)

    # 3. Masking tier (Owner Order §6 · W3 discipline carried forward).
    try:
        validate_tier(masking_tier)  # raises MaskingTierRefused
    except MaskingTierRefused as exc:
        raise ChokepointRefused(
            f"masking_tier_refused — {exc} (LLM crossing)."
        ) from exc

    # 4. Endpoint / provider (Owner sharpening §2 · connection-scoped).
    endpoint = resolve_endpoint(provider)  # raises LLMEndpointRefused
    # M12-W1g · closed-outbound belt-and-suspenders: even after
    # resolve_endpoint returns, verify the resolved host is on the
    # live allowlist.  Guards against future drift where a policy
    # entry could survive resolve_endpoint's checks but not
    # allowlisted_hosts()' membership.
    from services.chokepoint.llm_endpoint_allowlist import allowlisted_hosts
    _resolved_host = endpoint["host"]
    if _resolved_host not in allowlisted_hosts():
        raise LLMEndpointRefused(
            f"resolved_host_not_in_allowlist — resolved host "
            f"{_resolved_host!r} for provider {provider!r} is not in "
            f"allowlisted_hosts() live set (Canon 1 §A5.5 network-layer "
            f"allowlist)."
        )

    # M12-W1d · Option D · DAP-7 custody sequence: DE-IDENTIFY the
    # prompt BEFORE any dispatch.  No conditional guards this call —
    # the sequence ALWAYS runs.  For custody_class="synthetic" the
    # payload has no estate content; the deidentifier runs as a
    # verified no-op returning the unchanged text with an empty
    # token_map.
    from services.synisense.shield.deidentifier import deidentify
    de_id_result = await deidentify(
        prompt, tenant_id=tenant_id, purpose=purpose,
    )
    redacted_prompt = de_id_result.redacted_text

    # M12-W1d · Option D · WATCH INPUT-SEAT EMIT before dispatch.  A
    # crossing that cannot be observed does not happen (fail-closed
    # per R-26).
    # M12-W1f · Lango scoring (Canon 3 §13.1 + Canon 8 §5): score
    # hostility + provenance BEFORE persisting the crossing record,
    # so the verdict lands in the record like every other emission
    # at this boundary.  hold/block verdicts fail-close BEFORE the
    # outbound call is made (Canon 3 §13.1 'graded gate under the
    # Watch's own authority').
    import hashlib as _hashlib
    from services.watch.input_seat import (
        CrossingEvent,
        WatchInputSeatVerdictRefused,
        emit_crossing,
        score_input_seat,
    )
    from datetime import datetime as _datetime, timezone as _timezone
    _hostility, _provenance, _verdict = score_input_seat(
        purpose, custody_class, tenant_id, provider,
    )
    _prompt_hash = _hashlib.sha256(redacted_prompt.encode("utf-8")).hexdigest()
    emit_crossing(CrossingEvent(
        at_utc=_datetime.now(_timezone.utc).isoformat(),
        tenant_id=tenant_id,
        purpose=purpose,
        custody_class=custody_class,
        prompt_sha256=_prompt_hash,
        provider=provider,
        model=model,
        actor=actor,
        hostility_score=_hostility,
        provenance_score=_provenance,
        verdict=_verdict,
        egress_host=_resolved_host,
        session_id=session_id or "",
    ))
    # W1f graded-gate: hold and block refuse the outbound call.  The
    # crossing is already persisted with the refusal verdict — so the
    # seat record carries the full history the Watch consuming half
    # (Grey Mirror + Mkono) will read.
    if _verdict in ("hold", "block"):
        raise WatchInputSeatVerdictRefused(
            f"watch_input_seat_verdict_refused — verdict={_verdict!r} "
            f"(hostility={_hostility!r}, provenance={_provenance!r}); "
            f"outbound model call refused per Canon 3 §13.1 graded-gate "
            f"authority."
        )

    # 5. Instantiate client (test-injectable via _client_factory).
    session = session_id or f"sid-{uuid.uuid4().hex[:12]}"
    sysmsg = system_message or (
        "You are Akki — a governed reasoning faculty. Answer directly, "
        "cite the receipt kind, refuse when evidence is thin."
    )
    api_key = _emergent_api_key() if provider == "emergent" else _byo_provider_key(provider)

    t_start = time.perf_counter()
    client = _client_factory(
        api_key=api_key,
        session_id=session,
        system_message=sysmsg,
        model=model,
        provider=provider,
    )
    # Optional model selection — emergentintegrations LlmChat exposes .with_model()
    if hasattr(client, "with_model") and provider and model:
        try:
            client = client.with_model(provider, model)
        except Exception:  # noqa: BLE001
            # If provider/model combo is not selectable, fall back to defaults.
            pass

    # 6. Send + measure.  The prompt sent is the REDACTED prompt — raw
    # estate content never leaves under a query (DAP-7).
    try:
        response_text = await client.send_message(UserMessage(text=redacted_prompt))
    except Exception as exc:  # noqa: BLE001
        latency_ms = int((time.perf_counter() - t_start) * 1000)
        log.warning(
            "chokepoint.llm.invoke failed (%s) after %d ms",
            type(exc).__name__,
            latency_ms,
        )
        # Register a REFUSED-crossing receipt so the failure is on record.
        _register_llm_crossing(
            kind=f"{_kind_from_purpose(purpose)}_refused",
            endpoint=endpoint,
            verb="send_message",
            model=model,
            provider=provider,
            tokens_in=0,
            tokens_out=0,
            latency_ms=latency_ms,
            purpose=purpose,
            actor=actor,
            masking_tier=masking_tier,
            metering_source="upstream_failure",
        )
        raise LLMShieldFailure(
            f"upstream_llm_failed — {type(exc).__name__}: {str(exc)[:200]}"
        ) from exc

    latency_ms = int((time.perf_counter() - t_start) * 1000)

    # M12-W1d · Option D · RE-IDENTIFY the response using the same
    # token_map produced by de-identification.  Unmatched token in
    # response raises (fail-closed per canon 3 §13.1).
    from services.synisense.shield.reidentifier import reidentify
    reidentified_response = reidentify(str(response_text), de_id_result.token_map)

    # 7. Metering.
    tokens_in, tokens_out, metering_source = _extract_metering(redacted_prompt, reidentified_response, client)

    # 8. Register the crossing receipt with metering.
    receipt = _register_llm_crossing(
        kind=_kind_from_purpose(purpose),
        endpoint=endpoint,
        verb="send_message",
        model=model,
        provider=provider,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        latency_ms=latency_ms,
        purpose=purpose,
        actor=actor,
        masking_tier=masking_tier,
        metering_source=metering_source,
    )

    return LLMResponse(
        text=reidentified_response,  # M12-W1d · re-identified text · never raw redacted
        receipt_id=receipt.receipt_id,
        model_id=model,
        provider=provider,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        latency_ms=latency_ms,
        purpose=purpose,
    )


def _register_llm_crossing(
    *,
    kind: str,
    endpoint: Dict[str, str],
    verb: str,
    model: str,
    provider: str,
    tokens_in: int,
    tokens_out: int,
    latency_ms: int,
    purpose: str,
    actor: str,
    masking_tier: str,
    metering_source: str = "unavailable",
):
    """Write the crossing receipt with W5 metering."""
    if not isinstance(tokens_in, int) or tokens_in < 0:
        raise ChokepointRefused(
            f"metering_refused — tokens_in must be non-negative int, got {tokens_in!r}. "
            "Owner sharpening §1: W6 Cost Ledger cannot invent tokens."
        )
    if not isinstance(tokens_out, int) or tokens_out < 0:
        raise ChokepointRefused(
            f"metering_refused — tokens_out must be non-negative int, got {tokens_out!r}."
        )
    if not isinstance(latency_ms, int) or latency_ms < 0:
        raise ChokepointRefused(
            f"metering_refused — latency_ms must be non-negative int, got {latency_ms!r}."
        )
    if not model or not isinstance(model, str):
        raise ChokepointRefused(
            f"metering_refused — model_id required, got {model!r}."
        )
    if not provider or not isinstance(provider, str):
        raise ChokepointRefused(
            f"metering_refused — provider required, got {provider!r}."
        )

    return register_crossing(
        kind=kind,
        endpoint=endpoint,
        verb=verb,
        payload_shape={
            "model_id": model,
            "provider": provider,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "latency_ms": latency_ms,
            "purpose_declared": purpose,
            "metering_source": metering_source,
        },
        actor=actor,
        masking_tier=masking_tier,
    )


def _byo_provider_key(provider: str) -> str:
    """Load a BYO-provider key from the estate_keys/ custody file.

    Owner sharpening §3: keys land in `estate_keys/llm_<provider>_<connection_id>.json`.
    The file mode is 0600; the key value is NEVER returned in any API
    response body — it is only read into this in-process invoke path.
    """
    estate_keys_dir = os.environ.get("ESTATE_KEYS_DIR", "/app/backend/estate_keys")
    from pathlib import Path
    import json as _json

    d = Path(estate_keys_dir)
    if not d.is_dir():
        raise LLMShieldFailure(
            f"estate_keys_dir_missing — {estate_keys_dir!r} is not a directory. "
            f"Cannot resolve BYO key for provider {provider!r}."
        )
    candidates = sorted(d.glob(f"llm_{provider}_*.json"))
    if not candidates:
        raise LLMShieldFailure(
            f"byo_key_absent — no estate_keys/llm_{provider}_*.json on record. "
            "Paste a key via ConnectDrawerChat's 'An LLM' chip and verify."
        )
    # Newest wins (a re-verify overwrites).
    latest = candidates[-1]
    try:
        record = _json.loads(latest.read_text())
    except Exception as exc:  # noqa: BLE001
        raise LLMShieldFailure(
            f"byo_key_unreadable — {latest.name} malformed: {type(exc).__name__}"
        )
    key = record.get("key", "")
    if not key:
        raise LLMShieldFailure(
            f"byo_key_empty — {latest.name} carries no 'key' field."
        )
    return key


__all__ = [
    "invoke",
    "LLMResponse",
    "LLMShieldFailure",
    "PurposeInvalid",
    "CredentialShapedPromptRefused",
]
