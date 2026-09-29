"""Estate admission ceremony: performed by the estate owner's named authority, never over HTTP.

Every step writes through the existing ledger writer and receipt API. Worker identities are
attested on their own runtime; E1-held keys (planner, approvers, stand-in, allocator, rights
authority) live in estate custody. Re-running a step with the same inputs is idempotent.
"""
import hashlib
import json
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from services.activation.receipts import NativeReceipts
from services.enforce.control_scope import bind_control_scope
from services.enforce.principal_context_adapter import principal_context
from services.estate_admission import signing
from services.estate_admission.records import admit, latest
from services.estate_admission.resolver import LedgerAdmittedSigners, signer_record_id
from services.ledger_writer.mongo_control import digest
from services.ledger_writer.principal_control import append_event

PLANNER_PERMISSIONS = ('activation:plan',)
RUNTIME_PERMISSIONS = {
    'worker': ('activation:worker', 'activation:observation:runtime', 'activation:observation:measurements',
               'activation:observation:lineage', 'activation:observation:refusal'),
    'inspector': ('activation:worker', 'activation:observation:independence'),
    'custodian': ('activation:worker', 'activation:observation:delivery_grant', 'activation:observation:delivery_completion'),
}
STAND_IN_SCOPE = 'pilot:interim-admission'
YEAR = 365 * 86400


def receipts_for(db):
    return NativeReceipts(db, LedgerAdmittedSigners(db), timeout_seconds=30)


def opaque(prefix, *parts):
    return prefix + '-' + hashlib.sha256('|'.join(parts).encode()).hexdigest()[:16]


async def admit_organisation(db, tenant, legal_identity, admitted_by):
    principal_id = opaque('org', tenant, legal_identity)
    record = {'principal_id': principal_id, 'kind': 'organisation', 'legal_identity': legal_identity,
              'trust_domain_identifier': opaque('td', tenant), 'admission_time_mandate': f'estate-owner:{admitted_by}',
              'behavioural_signature_state': 'watch:baseline@admission', 'parent_organisation_id': None,
              'autonomy_scope': None, 'admit_authority': True, 'suspended': False}
    return principal_id, await admit(db, tenant, 'principal_admission', principal_id, record)


async def admit_member(db, tenant, org_id, principal_id, name, admitted_by, kind='individual', autonomy_scope=None):
    org = await latest(db, tenant, 'principal_admission', org_id)
    if org is None:
        raise ValueError('ORGANISATION_NOT_ADMITTED')
    record = {'principal_id': principal_id, 'kind': kind, 'legal_identity': name,
              'trust_domain_identifier': org['payload']['record']['trust_domain_identifier'],
              'admission_time_mandate': f'admitted-by:{admitted_by}',
              'behavioural_signature_state': 'watch:agent-machine-speed@admission' if kind == 'agent' else 'watch:baseline@admission',
              'parent_organisation_id': org_id, 'autonomy_scope': autonomy_scope, 'admit_authority': False, 'suspended': False}
    return await admit(db, tenant, 'principal_admission', principal_id, record)


async def bank_membership(db, tenant, principal_id, org_id, admission_ref):
    """Written under the member's own propagated principal (the reader keys on payload.principal_id)."""
    with principal_context(principal_id), bind_control_scope({'principal_id': principal_id, 'tenant_id': tenant}):
        event = await append_event(db, tenant_id=tenant, run_id=f'membership:{principal_id}',
            command_id=digest({'membership': principal_id, 'org': org_id, 'ref': admission_ref}),
            event_type='principal_membership.admitted', resource_type='principal_membership', decision='active',
            reason_code='ESTATE_CEREMONY', payload={'principal_id': principal_id, 'organisation_principal_id': org_id,
                                                    'status': 'active', 'admission_receipt_ref': admission_ref})
    return event['row']['hash']


async def bank_licence(db, tenant, licence, admission_ref, period_start, period_end, period_iso):
    event = await append_event(db, tenant_id=tenant, run_id=f"licence:{licence['organisation_principal_id']}",
        command_id=digest({'licence': licence, 'period': period_iso}), event_type='entitlement_licence.admitted',
        resource_type='entitlement_licence', decision='active', reason_code='ESTATE_CEREMONY',
        payload={'licence': licence, 'admission_receipt_ref': admission_ref, 'period_start': period_start,
                 'period_end': period_end, 'period_iso': period_iso})
    return event['row']['hash']


async def admit_signer(db, tenant, principal_id, key_id, public_key_hex, permissions, scope_refs, valid_seconds=YEAR):
    """Idempotent on (principal, key, public key, mandate): an identical current admission is returned, not repeated."""
    now = int(time.time())
    existing = await latest(db, tenant, 'admitted_signer', signer_record_id(principal_id, key_id))
    if existing is not None:
        record = existing['payload']['record']
        if (record['public_key_hex'] == public_key_hex and record['permissions'] == sorted(set(permissions))
                and record['scope_refs'] == sorted(set(scope_refs)) and not record.get('revoked')
                and record['expires_epoch'] > now + 86400):
            return existing['row']['hash']
    record = {'tenant_id': tenant, 'principal_id': principal_id, 'key_id': key_id, 'public_key_hex': public_key_hex,
              'permissions': sorted(set(permissions)), 'scope_refs': sorted(set(scope_refs)),
              'valid_from_epoch': now - 300, 'expires_epoch': now + int(valid_seconds), 'revoked': False}
    return await admit(db, tenant, 'admitted_signer', signer_record_id(principal_id, key_id), record)


async def admit_custody_signer(db, tenant, principal_id, key_id, permissions, scope_refs):
    """An E1-held key: generated once in estate custody (0600), admitted by record."""
    public = signing.ensure_key(tenant, key_id)
    return await admit_signer(db, tenant, principal_id, key_id, public, permissions, scope_refs)


async def admit_stand_in(db, tenant, org_id, admitted_by, groups, units, basis):
    """The interim-pilot admission: an agent principal that stands in for unseated approval groups.
    Its key is estate custody; every approval it signs cites STAND_IN_SCOPE and the basis recorded here."""
    principal_id = opaque('agent', tenant, STAND_IN_SCOPE)
    await admit_member(db, tenant, org_id, principal_id, 'Interim pilot admission (stand-in for unseated approval groups)',
                       admitted_by, kind='agent', autonomy_scope=STAND_IN_SCOPE)
    permissions = ['activation:approval:' + g for g in groups]
    ref = await admit_custody_signer(db, tenant, principal_id, 'approver-' + principal_id, permissions, units)
    return {'principal_id': principal_id, 'signer_ref': ref, 'stands_in_for': sorted(groups), 'basis': basis,
            'autonomy_scope': STAND_IN_SCOPE}


async def set_approval_groups(db, tenant, groups, interim_stand_in=None):
    for group in groups:
        if not {'group', 'purpose', 'members', 'quorum'} <= set(group):
            raise ValueError('INCOMPLETE_APPROVAL_GROUP')
        if group['members'] and int(group['quorum']) > len(group['members']):
            raise ValueError('APPROVAL_GROUP_QUORUM_EXCEEDS_MEMBERS')
    return await admit(db, tenant, 'approval_groups', 'default', {'groups': groups, 'interim_stand_in': interim_stand_in})


async def set_dials(db, tenant, dial_versions, policy_versions, policy_epoch):
    return await admit(db, tenant, 'dials', 'default', {'dial_versions': dial_versions, 'policy_versions': policy_versions,
                                                        'policy_epoch': int(policy_epoch)})


async def set_custody_descriptor(db, tenant, record):
    required = {'provider', 'endpoint_origin', 'bucket', 'prefix', 'region', 'custodian_runtime_id', 'custodian_principal_id'}
    if not required <= set(record):
        raise ValueError('INCOMPLETE_CUSTODY_DESCRIPTOR')
    ref = await admit(db, tenant, 'custody_descriptor', 'default', record)
    mirror = signing.custody_dir() / tenant / 'custody_descriptor.json'
    mirror.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    mirror.write_text(json.dumps({**record, 'ledger_ref': ref}, indent=1, sort_keys=True))
    os.chmod(mirror, 0o600)
    return ref


async def bank_allocation(db, tenant, allocator_id, key_id, limits, terms_ref, scope_refs):
    receipts = receipts_for(db)
    current = await latest(db, tenant, 'allocation_binding', 'default')
    if current is not None:
        record = current['payload']['record']
        if record['limits'] == limits and record['terms_ref'] == terms_ref and record['scope_refs'] == sorted(scope_refs):
            return record['allocation_ref']
    claims = {'limits': limits, 'terms_ref': terms_ref}
    receipt = signing.sign_receipt(tenant, allocator_id, key_id, 'allocation', claims, scope_refs=scope_refs, ttl_seconds=YEAR)
    ref = await receipts.record(receipt)
    await admit(db, tenant, 'allocation_binding', 'default', {'allocation_ref': ref, 'terms_ref': terms_ref,
                                                              'scope_refs': sorted(scope_refs), 'limits': limits})
    return ref


async def bank_rights(db, tenant, authority_id, key_id, units, lawful_basis_path):
    """Anchor the lawful-basis document, then one active rights proof per admitted source unit."""
    receipts = receipts_for(db)
    doc_sha = hashlib.sha256(Path(lawful_basis_path).read_bytes()).hexdigest()
    current = await latest(db, tenant, 'rights_anchor', 'default')
    if current is not None and current['payload']['record']['lawful_basis_sha256'] == doc_sha \
            and set(current['payload']['record']['rights_refs']) == set(units):
        return current['payload']['record']['anchor_ref'], current['payload']['record']['rights_refs']
    anchor_claim = {'category': 'anchor', 'context_sha256': doc_sha, 'claim_sha256': doc_sha, 'evidence_mode': 'measured'}
    scope_refs = sorted(units)
    anchor_ref = await receipts.record(signing.sign_receipt(tenant, authority_id, key_id, 'observation', anchor_claim,
                                                            scope_refs=scope_refs, ttl_seconds=YEAR))
    refs = {}
    for unit in units:
        rights = {'version': 'akki.rights.metadata/1', 'unit_ref': 'akki://source/' + unit, 'status': 'active',
                  'policy_ref': anchor_ref, 'reason_code': 'LAWFUL_BASIS_ADMITTED'}
        claim = {'category': 'rights', 'context_sha256': doc_sha, 'claim_sha256': digest(rights), 'evidence_mode': 'measured',
                 'rights': rights}
        refs[unit] = await receipts.record(signing.sign_receipt(tenant, authority_id, key_id, 'observation', claim,
                                                                scope_refs=scope_refs, ttl_seconds=YEAR))
    await admit(db, tenant, 'rights_anchor', 'default', {'anchor_ref': anchor_ref, 'rights_refs': refs,
                                                         'lawful_basis_sha256': doc_sha})
    return anchor_ref, refs


async def admit_runtime(db, tenant, descriptor, units):
    """Attest on the runtime itself: key generated there, capacity observed there, Worker receipt signed
    there; only the descriptor is admitted here. The host is an instance; the descriptor is the runtime."""
    from services.extraction_runtime import remote
    from services.activation.record_shapes import Worker
    from services.estate_admission.runtimes import descriptor_valid
    probe = {**descriptor, 'principal_id': 'runtime:' + descriptor['runtime_id'], 'key_id': 'pending'}
    attested = await remote.call_async(probe, {'mode': 'attest', 'tenant_id': tenant, 'operation_key': 'attest',
                                               'fence': 0, 'scope_refs': sorted(units)}, deadline_seconds=90)
    principal_id, key_id = 'runtime:' + descriptor['runtime_id'], attested['key_id']
    permissions = set()
    for role in descriptor['roles']:
        permissions.update(RUNTIME_PERMISSIONS[role])
    await admit_signer(db, tenant, principal_id, key_id, attested['public_key_hex'], sorted(permissions), units)
    observed = attested['capacity_observed']
    full = {**descriptor, 'principal_id': principal_id, 'key_id': key_id, 'executor_version': attested['executor_version'],
            'compute_classes': observed['compute_classes'],
            'capacity': {k: observed[k] for k in ('cpu_cores', 'gpu_count', 'memory_gb')},
            'compute_accounting': observed['accounting']}
    worker = Worker(runtime_id=descriptor['runtime_id'], executor_version=attested['executor_version'],
                    kinds=tuple(descriptor['kinds']), enforced_dimensions=tuple(descriptor['enforced_dimensions']),
                    enforcement_protocol='akki.runtime.limits/1', implementation_workspace_touched_data=False)
    signed = await remote.call_async(full, {'mode': 'sign_worker', 'tenant_id': tenant, 'operation_key': 'attest', 'fence': 0,
                                            'scope_refs': sorted(units), 'claims': worker.model_dump(mode='json')}, deadline_seconds=90)
    receipts = receipts_for(db)
    worker_ref = await receipts.record(signing.runtime_receipt(signed['receipt']))
    record = descriptor_valid({**full, 'status': 'active', 'worker_receipt_ref': worker_ref,
                               'attestation': {'hostname': attested['hostname'], 'python': attested['python'],
                                               'modules': attested['modules'], 'capacity_observed': observed,
                                               'attested_at': datetime.now(timezone.utc).isoformat()}})
    ref = await admit(db, tenant, 'admitted_runtime', descriptor['runtime_id'], record)
    await admit(db, tenant, 'runtime_attestation', descriptor['runtime_id'] + ':' + key_id,
                {'runtime_id': descriptor['runtime_id'], 'key_id': key_id, 'worker_receipt_ref': worker_ref, 'descriptor_ref': ref})
    return record, worker_ref


def period_bounds(now=None):
    now = now or datetime.now(timezone.utc)
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end = (start + timedelta(days=32)).replace(day=1)
    return start.isoformat(), end.isoformat(), start.strftime('%Y-%m')
