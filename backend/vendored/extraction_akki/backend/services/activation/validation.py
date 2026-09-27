"""Shape → semantic consistency → authoritative proof. No implicit issue/admit/sign."""
from datetime import datetime, timezone
from services.activation.models import ValidationResult, issue
from services.activation.schema import PROFILE_ID, PROFILE_SHA, IMPLEMENTATION_SHA, canonical_document, schema_issues
from services.activation.semantics import semantic_issues
from services.activation.evidence import check_provider, evidence_issues


async def validate_certificate(document, *, tenant_id, principal_id, evidence=None, timeout_seconds=None, now=None):
    check_provider(evidence, timeout_seconds)
    now = now if now is not None else datetime.now(timezone.utc)
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("A timezone-aware validation instant is required.")
    d, sha = canonical_document(document)
    args = {"profile_id": PROFILE_ID, "profile_sha256": PROFILE_SHA,
            "implementation_sha256": IMPLEMENTATION_SHA, "certificate_sha256": sha}
    errors = schema_issues(d)
    if errors:
        return ValidationResult(**args, issues=errors)
    errors = semantic_issues(d, now=now)
    # The owner schema has tenant_id, not a caller-supplied principal field.
    # Request ownership is verified by the server-owned evidence port against
    # the authenticated principal, never inferred from issuer/approver strings.
    if (d["identity"]["estate_id"], d["identity"]["tenant_id"]) != (tenant_id, tenant_id):
        errors += (issue("CERTIFICATE_SCOPE_MISMATCH", "/identity"),)
    if errors:
        return ValidationResult(**args, schema_valid=True, issues=errors)
    errors = await evidence_issues(d, sha, tenant_id=tenant_id, principal_id=principal_id,
                                   evidence=evidence, timeout_seconds=timeout_seconds, now=now)
    if errors:
        return ValidationResult(**args, schema_valid=True, semantics_valid=True, issues=errors)
    # The submitted label is compared to the derived result, never taken as authority.
    blocked = bool(d["supersession"]["revalidation"]["triggers_fired"] or d["supersession"]["superseded_by"])
    state = "LIVE-BLOCKED" if blocked else "PARTIALLY LIVE" if d["mocked_components"] else "LIVE-VERIFIED"
    if d["state"] != state:
        return ValidationResult(**args, schema_valid=True, semantics_valid=True,
                                issues=(issue("DERIVED_STATE_MISMATCH", "/state"),))
    return ValidationResult(**args, valid=True, schema_valid=True, semantics_valid=True,
                            evidence_verified=True, derived_state=state)