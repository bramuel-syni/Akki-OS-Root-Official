"""CP-CENSUS-OPERATIONAL-V1: identity/source gates, outside sealed kernels."""
from services.tenant_separation.tenant_registry import CANONICAL_TENANT_IDS

SOURCE_TENANTS = {"rms_mysql": "RMS", "rms_obs": "RMS", "rms_nas": "RMS",
                  "digicow_rds": "DIGICOW", "digicow_s3": "DIGICOW"}
SOURCE_LABELS = {"rms_mysql": "RMS relational estate", "rms_obs": "RMS object archive",
                 "rms_nas": "RMS broadcast archive", "digicow_rds": "DigiCow relational estate",
                 "digicow_s3": "DigiCow object archive"}


def tenant_from_account(account):
    tenant = account.get("tenant_id")
    if tenant not in CANONICAL_TENANT_IDS:
        raise ValueError("Your account has no admitted tenant membership. An estate administrator must record it.")
    return tenant


def validate_submission(body, tenant, roles):
    if not {"operator", "master_admin"}.intersection(roles):
        raise PermissionError("Only an admitted estate operator can commission a census.")
    allowed = {"source_ids", "tenant_id", "idempotency_key"}
    if set(body) - allowed:
        raise ValueError("Only admitted source references can be submitted. Credentials and execution commands are not accepted.")
    if body.get("tenant_id", tenant) != tenant:
        raise ValueError("The requested tenant does not match your admitted membership.")
    sources = body.get("source_ids")
    if not isinstance(sources, list) or not 1 <= len(sources) <= 5 or any(not isinstance(s, str) for s in sources) or len(set(sources)) != len(sources):
        raise ValueError("Select between one and five distinct admitted sources.")
    if any(not isinstance(s, str) or SOURCE_TENANTS.get(s) != tenant for s in sources):
        raise ValueError("One or more sources are not admitted to your tenant.")
    return sources