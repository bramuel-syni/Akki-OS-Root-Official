"""Read-only descriptor bridges to existing Census/skill/training contracts.

These are NOT admission producers. Opaque input handles must resolve inside
Akki through the element's existing registry; no file/network resolution here.
"""
import re
from services.ledger_writer.mongo_control import digest
from services.northena.execution_models import Held, Request


def source_request(job, *, principal_id, deadline_epoch):
    descriptor = job.get("connect_source_descriptor") or {}
    sources = descriptor.get("source_ids")
    if (descriptor.get("version") != "operational-v1" or not sources
            or not isinstance(descriptor.get("lawful_basis_sha256"), str)
            or not re.fullmatch(r"[0-9a-f]{64}", descriptor["lawful_basis_sha256"])):
        raise Held("CENSUS_DESCRIPTOR_NOT_BOUND")
    return Request(request_id=job["census_run_id"], tenant_id=job["tenant_id"],
                   principal_id=principal_id, kind="source", engine="mtafiti",
                   objective_sha256=digest({"source_ids": sources,
                                            "lawful_basis_sha256": descriptor["lawful_basis_sha256"]}),
                   input_refs=tuple("akki://source/" + item for item in sources),
                   scope_refs=tuple(sources), deadline_epoch=deadline_epoch)


def skill_request(provisioning, *, request_id, tenant_id, principal_id,
                  query_ref, query_sha256, deadline_epoch):
    if provisioning.revoked_at is not None:
        raise Held("SKILL_PROVISIONING_REVOKED")
    if not isinstance(query_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", query_sha256):
        raise Held("SKILL_QUERY_DESCRIPTOR_INVALID")
    if not provisioning.corpus_slice_ref.startswith("akki://"):
        raise Held("SKILL_CORPUS_REFERENCE_UNBOUND")
    return Request(request_id=request_id, tenant_id=tenant_id, principal_id=principal_id,
                   kind="skill", engine="solva", deadline_epoch=deadline_epoch,
                   objective_sha256=digest({"skill_id": provisioning.skill_id,
                                            "query_sha256": query_sha256,
                                            "key_grant_id": provisioning.key_grant_id}),
                   input_refs=(provisioning.corpus_slice_ref, query_ref),
                   scope_refs=(provisioning.scope,), result_floor=provisioning.floor)


def training_request(run, *, tenant_id, principal_id, corpus_manifest_ref,
                     moac_criteria_ref, scope_refs, deadline_epoch):
    # Mutable progress/status is deliberately not an input to frozen identity.
    frozen = {key: getattr(run, key) for key in (
        "run_id", "recipe_version", "base_model_id", "adapter_kind", "material_admit_ref", "ssh_mode")}
    frozen.update(corpus_manifest_ref=corpus_manifest_ref, moac_criteria_ref=moac_criteria_ref)
    return Request(request_id=run.run_id, tenant_id=tenant_id, principal_id=principal_id,
                   kind="training", engine="targeta", objective_sha256=digest(frozen),
                   input_refs=(corpus_manifest_ref, moac_criteria_ref), scope_refs=tuple(scope_refs),
                   deadline_epoch=deadline_epoch)


def evaluation_request(*, request_id, tenant_id, principal_id, model_artifact_ref,
                       heldout_manifest_ref, moac_criteria_ref, scope_refs, deadline_epoch):
    references = (model_artifact_ref, heldout_manifest_ref, moac_criteria_ref)
    return Request(request_id=request_id, tenant_id=tenant_id, principal_id=principal_id,
                   kind="evaluation", engine="targeta", objective_sha256=digest(references),
                   input_refs=references, scope_refs=tuple(scope_refs), deadline_epoch=deadline_epoch)