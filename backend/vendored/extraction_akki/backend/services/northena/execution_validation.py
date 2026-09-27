"""Cross-port checks: descriptors never grant themselves authority."""
from pydantic import ValidationError
from services.northena.execution_models import Authority, Held, WorkerResult, Artifact


def authority_for(request, grant, now, phase):
    if not isinstance(grant, Authority):
        raise Held("AUTHORITY_RECEIPT_INVALID")
    try:
        grant = Authority.model_validate_json(grant.model_dump_json())
    except (ValidationError, ValueError, TypeError) as exc:
        raise Held("AUTHORITY_RECEIPT_INVALID") from exc
    if (grant.request_sha256 != request.digest() or grant.tenant_id != request.tenant_id
            or grant.principal_id != request.principal_id or grant.engine != request.engine
            or grant.scope_refs != request.scope_refs):
        raise Held("AUTHORITY_SCOPE_MISMATCH")
    if grant.expires_epoch <= now:
        raise Held("AUTHORITY_EXPIRED")
    if phase == "dispatch" and request.deadline_epoch <= now:
        raise Held("EXECUTION_DEADLINE_EXPIRED")
    return grant


def result_for(request, result, dispatch):
    if not isinstance(result, WorkerResult):
        raise Held("EXECUTOR_RECEIPT_INVALID")
    try:
        result = WorkerResult.model_validate_json(result.model_dump_json())
    except (ValidationError, ValueError, TypeError) as exc:
        raise Held("EXECUTOR_RECEIPT_INVALID") from exc
    if (result.request_sha256 != request.digest()
            or result.operation_key != dispatch["data"]["operation_key"]
            or result.fence != dispatch["seq"]):
        raise Held("EXECUTOR_RECEIPT_BINDING_INVALID")
    if any(artifact.tenant_id != request.tenant_id for artifact in result.artifacts):
        raise Held("ARTIFACT_TENANT_MISMATCH")
    if len({item.ref for item in result.artifacts}) != len(result.artifacts):
        raise Held("DUPLICATE_ARTIFACT")
    if result.usage is not None and len({item.unit for item in result.usage}) != len(result.usage):
        raise Held("DUPLICATE_USAGE_UNIT")
    return result


def checked_artifacts(request, result, verified):
    if (not isinstance(verified, tuple) or not verified
            or any(not isinstance(item, Artifact) for item in verified)
            or verified != result.artifacts):
        raise Held("ARTIFACT_MANIFEST_NOT_VERIFIED")
    try:
        verified = tuple(Artifact.model_validate_json(item.model_dump_json()) for item in verified)
    except (ValidationError, ValueError, TypeError) as exc:
        raise Held("ARTIFACT_MANIFEST_NOT_VERIFIED") from exc
    rank = {"non_factual": 0, "utterance": 1, "fact": 2}
    if request.result_floor and any(rank[a.class_label] < rank[request.result_floor] for a in verified):
        raise Held("DEFENSIBILITY_BELOW_FLOOR")
    return verified