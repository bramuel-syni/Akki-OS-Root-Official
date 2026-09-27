"""Server-owned evidence verification port. Client booleans never satisfy this boundary."""
import asyncio
import inspect
import math
from copy import deepcopy
from typing import Literal
from services.activation.models import Frozen, Text, Hash, issue
from pydantic import Field, ValidationError

CHECKS = ("signature_verified", "request_verified", "policy_verified", "approvals_verified",
          "measurements_verified", "manifest_verified", "independence_verified",
          "retrieval_verified", "refusal_verified", "revalidation_verified")


class EvidenceVerdict(Frozen):
    certificate_sha256: Hash
    tenant_id: Text
    principal_id: Text
    verified_refs: tuple[Text, ...]
    signature_verified: bool
    request_verified: bool
    policy_verified: bool
    approvals_verified: bool
    measurements_verified: bool
    manifest_verified: bool
    independence_verified: bool
    retrieval_verified: bool
    refusal_verified: bool
    revalidation_verified: bool
    evidence_mode: Literal["measured", "MOCKED"]
    expires_epoch: int = Field(gt=0)


def reference_set(document):
    refs = set()
    def walk(value, key=""):
        if isinstance(value, dict):
            for name, child in value.items():
                walk(child, name)
        elif isinstance(value, list):
            for child in value:
                walk(child, key[:-1] if key.endswith("_refs") else key)
        elif isinstance(value, str) and (key.endswith("_ref") or key in {"registry_entry_id", "terms_identifier"}):
            refs.add(value)
    walk(document)
    return frozenset(refs)


def check_provider(evidence, timeout_seconds):
    if evidence is None:
        return
    if (not inspect.iscoroutinefunction(getattr(evidence, "verify", None))
            or type(timeout_seconds) not in (int, float)
            or not math.isfinite(timeout_seconds) or timeout_seconds <= 0):
        raise ValueError("An async server-owned verifier and explicit finite timeout are required.")


async def evidence_issues(document, digest, *, tenant_id, principal_id, evidence, timeout_seconds, now):
    if evidence is None:
        return (issue("EVIDENCE_VERIFIER_NOT_BOUND"),)
    try:
        started = asyncio.get_running_loop().time()
        result = await asyncio.wait_for(evidence.verify(deepcopy(document), tenant_id=tenant_id,
                                                        principal_id=principal_id), timeout_seconds)
        if not isinstance(result, EvidenceVerdict):
            return (issue("EVIDENCE_VERDICT_NOT_TYPED"),)
        result = EvidenceVerdict.model_validate_json(result.model_dump_json())
    except (TimeoutError, ConnectionError, OSError):
        return (issue("EVIDENCE_VERIFIER_UNAVAILABLE"),)
    except (ValidationError, ValueError, TypeError):
        return (issue("EVIDENCE_VERDICT_MALFORMED"),)
    if (result.certificate_sha256, result.tenant_id, result.principal_id) != (digest, tenant_id, principal_id):
        return (issue("EVIDENCE_BINDING_MISMATCH"),)
    if result.expires_epoch <= now.timestamp() + asyncio.get_running_loop().time() - started:
        return (issue("EVIDENCE_EXPIRED"),)
    if result.evidence_mode != "measured" or not all(getattr(result, k) for k in CHECKS):
        return (issue("EVIDENCE_NOT_VERIFIED"),)
    if not reference_set(document) <= set(result.verified_refs):
        return (issue("EVIDENCE_REFERENCES_UNRESOLVED"),)
    return ()