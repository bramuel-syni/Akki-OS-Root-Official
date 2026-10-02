"""CP-CENSUS-OPERATIONAL-V1: identity/source gates, outside sealed kernels."""
from services.tenant_separation.tenant_registry import CANONICAL_TENANT_IDS

SOURCE_TENANTS = {"rms_mysql": "RMS", "rms_obs": "RMS", "rms_nas": "RMS",
                  "digicow_rds": "DIGICOW", "digicow_s3": "DIGICOW"}
SOURCE_LABELS = {"rms_mysql": "RMS relational estate", "rms_obs": "RMS object archive",
                 "rms_nas": "RMS broadcast archive", "digicow_rds": "DigiCow relational estate",
                 "digicow_s3": "DigiCow object archive"}


def sources_for(tenant):
    return [source for source,owner in SOURCE_TENANTS.items() if owner==tenant]


def tenant_from_account(account):
    tenant = account.get("tenant_id")
    if tenant not in CANONICAL_TENANT_IDS:
        raise ValueError("Your account has no admitted tenant membership. An estate administrator must record it.")
    return tenant


def validate_submission(body, tenant, roles):
    if not {"operator", "master_admin"}.intersection(roles):
        raise PermissionError("Only an admitted estate operator can commission a census.")
    allowed = {"source_ids", "tenant_id", "idempotency_key", "worker_id", "source_refs", "measurement"}
    if set(body) - allowed:
        raise ValueError("Only admitted source references can be submitted. Credentials and execution commands are not accepted.")
    if body.get("tenant_id", tenant) != tenant:
        raise ValueError("The requested tenant does not match your admitted membership.")
    if body.get('measurement') is not None:
        if body['measurement'] not in ('enumeration', 'content_full'):
            raise ValueError("Measurement must be 'enumeration' or 'content_full'.")
        if body['measurement'] == 'content_full' and (body.get('worker_id') in (None, 'non_gpu_jump') or any(s not in ('rms_obs', 'rms_nas') for s in body.get('source_ids') or [])):
            raise ValueError('Full-content measurement reads media on a GPU worker and applies to the object store and the NAS shares only.')
    if body.get('worker_id') is not None:
        from services.training_runner.ssh_seam import list_hosts
        if body['worker_id'] not in ['non_gpu_jump',*list_hosts()]:
            raise ValueError('Choose a registered external worker.')
    sources = body.get("source_ids")
    if not isinstance(sources, list) or not 1 <= len(sources) <= 5 or any(not isinstance(s, str) for s in sources) or len(set(sources)) != len(sources):
        raise ValueError("Select between one and five distinct admitted sources.")
    if any(not isinstance(s, str) or SOURCE_TENANTS.get(s) != tenant for s in sources):
        raise ValueError("One or more sources are not admitted to your tenant.")
    refs=body.get('source_refs')
    if refs is not None:
        import re
        if not isinstance(refs,list) or not 1<=len(refs)<=100 or any(not isinstance(r,str) or not re.fullmatch(r'source_[a-f0-9]{24}',r) for r in refs) or len(refs)!=len(set(refs)):
            raise ValueError('Select distinct retained source-region references.')
        from services.census_autonomy import operational_reads
        from services.census_autonomy.registry_surfaces import inventory
        known={r['source_ref']:r for r in inventory(tenant,operational_reads.records(tenant))['source_details']}
        if any(r not in known or known[r]['source_id'] not in sources for r in refs):
            raise ValueError('A source-region reference is outside the commissioned tenant/scope.')
        if any(not any(known[r]['source_id']==s for r in refs) for s in sources):
            raise ValueError('Each selected source group must have a selected region.')
    return sources