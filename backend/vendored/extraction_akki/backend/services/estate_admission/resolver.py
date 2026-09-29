"""Admitted-signer and principal resolution from estate admission records only."""
from contracts.principal_v1 import PrincipalV1
from services.activation.receipts import AdmittedSigner
from services.enforce.control_scope import require_control_scope
from services.estate_admission.records import latest


def signer_record_id(principal_id, key_id):
    return f'{principal_id}:{key_id}'


class LedgerAdmittedSigners:
    def __init__(self, db):
        self.db = db

    async def resolve(self, tenant, principal, key_id):
        event = await latest(self.db, tenant, 'admitted_signer', signer_record_id(principal, key_id))
        if event is None:
            return None
        record = event['payload']['record']
        if record.get('tenant_id') != tenant:
            return None
        return AdmittedSigner(tenant_id=tenant, principal_id=principal, key_id=key_id,
            public_key_hex=record['public_key_hex'], admission_ref=event['row']['hash'],
            permissions=tuple(record['permissions']), scope_refs=tuple(record['scope_refs']),
            valid_from_epoch=int(record['valid_from_epoch']), expires_epoch=int(record['expires_epoch']),
            revoked=bool(record.get('revoked', False)))


def ledger_principal_lookup(db):
    async def lookup(principal_id):
        tenant = require_control_scope().tenant_id
        event = await latest(db, tenant, 'principal_admission', principal_id)
        if event is None:
            raise KeyError(principal_id)
        return PrincipalV1.model_validate(event['payload']['record'])
    return lookup
