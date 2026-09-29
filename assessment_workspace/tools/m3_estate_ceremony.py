"""M3 estate admission ceremony — performed by the estate owner's named authority from an admission file.

    python m3_estate_ceremony.py --admission <estate.json> [--attest] [--receipt <out.json>]

The tool admits ANY estate from its file; no tenant, host, bucket or principal is named in code.
Every record goes through the existing ledger writer / receipt API (services.estate_admission.ceremony).
`--attest` reaches each declared runtime over its admitted seam: the runtime generates its own key,
observes its own capacity and signs its own Worker receipt; only the descriptor is admitted here.
Approver/planner/allocator/stand-in keys are generated once into AKKI_ESTATE_CUSTODY_DIR (0600).
"""
import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import load_dotenv  # noqa: E402

load_dotenv('/app/backend/.env')
from bson import ObjectId  # noqa: E402
from core import db  # noqa: E402
from services.enforce.control_scope import bind_control_scope  # noqa: E402
from services.enforce.principal_context_adapter import principal_context  # noqa: E402
from services.estate_admission import ceremony  # noqa: E402

SCOPE_GROUP = 'scope.requester'


def as_actor(principal_id, tenant):
    class _Scope:
        def __enter__(self):
            self.p = principal_context(principal_id); self.p.__enter__()
            self.c = bind_control_scope({'principal_id': principal_id, 'tenant_id': tenant}); self.c.__enter__()
            return self

        def __exit__(self, *exc):
            self.c.__exit__(*exc); self.p.__exit__(*exc)
    return _Scope()


async def resolve_members(spec, tenant):
    """Members are existing accounts: named by e-mail, or every account already bound to this tenant."""
    rows = []
    if spec.get('from_account_bindings'):
        cursor = db.users.find({'tenant_id': tenant}, {'email': 1, 'name': 1, 'roles': 1, 'tenant_admission_ref': 1})
        async for account in cursor:
            rows.append(account)
    for email in spec.get('accounts', []):
        account = await db.users.find_one({'email': email}, {'email': 1, 'name': 1, 'roles': 1, 'tenant_id': 1, 'tenant_admission_ref': 1})
        if account is None:
            raise SystemExit(f'ACCOUNT_NOT_FOUND:{email}')
        rows.append(account)
    return [{'principal_id': str(a['_id']), 'name': a.get('name') or a['email'], 'email': a['email'], 'roles': a.get('roles', []),
             'account_tenant': a.get('tenant_id'), 'binding_ref': a.get('tenant_admission_ref')} for a in rows]


def group_members(group, members_by_email, agents):
    out = []
    for ref in group.get('members', []):
        kind, _, name = ref.partition(':')
        if kind == 'account':
            out.append(members_by_email[name]['principal_id'])
        elif kind == 'agent':
            out.append(agents[name]['principal_id'])
        else:
            raise SystemExit(f'UNRESOLVED_GROUP_MEMBER:{ref}')
    return out


async def run(admission, attest, receipt_path):
    tenant = admission['tenant_id']
    units = sorted(admission['rights']['units'])
    out = {'tenant_id': tenant, 'started_at': datetime.now(timezone.utc).isoformat(), 'steps': {}}
    org = admission['organisation']
    org_id = ceremony.opaque('org', tenant, org['legal_identity'])
    with as_actor(org_id, tenant):
        _, ref = await ceremony.admit_organisation(db, tenant, org['legal_identity'], org['admitted_by'])
        out['steps']['organisation'] = {'principal_id': org_id, 'ref': ref}
        agents = {}
        for spec in admission['agents']:
            pid = ceremony.opaque('agent', tenant, spec['autonomy_scope'])
            aref = await ceremony.admit_member(db, tenant, org_id, pid, spec['name'], org['admitted_by'], kind='agent',
                                               autonomy_scope=spec['autonomy_scope'])
            sref = await ceremony.admit_custody_signer(db, tenant, pid, spec['key_id'], spec['permissions'], units)
            agents[spec['autonomy_scope']] = {'principal_id': pid, 'admission_ref': aref, 'signer_ref': sref, 'key_id': spec['key_id']}
        out['steps']['agents'] = agents
    members = await resolve_members(admission['members'], tenant)
    members_by_email = {m['email']: m for m in members}
    admitted_members = []
    for m in members:
        with as_actor(org_id, tenant):
            aref = await ceremony.admit_member(db, tenant, org_id, m['principal_id'], m['name'], org['admitted_by'])
            seats = [SCOPE_GROUP] + [g['group'] for g in admission['approval_groups'] if f"account:{m['email']}" in g.get('members', [])]
            sref = await ceremony.admit_custody_signer(db, tenant, m['principal_id'], 'approver-' + m['principal_id'],
                                                       ['activation:approval:' + s for s in seats], units)
        mref = await ceremony.bank_membership(db, tenant, m['principal_id'], org_id, aref)
        admitted_members.append({'principal_id': m['principal_id'], 'name': m['name'], 'admission_ref': aref, 'signer_ref': sref,
                                 'membership_ref': mref, 'seats': seats, 'account_tenant': m['account_tenant'], 'binding_ref': m['binding_ref']})
    out['steps']['members'] = admitted_members
    with as_actor(org_id, tenant):
        stand_in = None
        if admission.get('interim_stand_in'):
            spec = admission['interim_stand_in']
            unseated = [g['group'] for g in admission['approval_groups'] if not g.get('members')]
            stand_in = await ceremony.admit_stand_in(db, tenant, org_id, org['admitted_by'], unseated, units, spec['basis'])
        groups = [{'group': g['group'], 'purpose': g['purpose'], 'quorum': int(g['quorum']),
                   'members': group_members(g, members_by_email, agents)} for g in admission['approval_groups']]
        out['steps']['approval_groups'] = {'ref': await ceremony.set_approval_groups(db, tenant, groups, stand_in),
                                           'groups': groups, 'interim_stand_in': stand_in}
        lic = admission['licence']
        licence = {**lic['fields'], 'organisation_principal_id': org_id, 'terms_identifier': lic['terms_identifier']}
        start, end, iso = ceremony.period_bounds()
        out['steps']['licence'] = {'ref': await ceremony.bank_licence(db, tenant, licence, ref, start, end, iso), 'period': iso,
                                   'terms_identifier': lic['terms_identifier']}
        d = admission['dials']
        out['steps']['dials'] = await ceremony.set_dials(db, tenant, d['dial_versions'], d['policy_versions'], d['policy_epoch'])
        allocator = agents['estate:allocator']
        out['steps']['allocation'] = await ceremony.bank_allocation(db, tenant, allocator['principal_id'], allocator['key_id'],
                                                                    admission['allocation']['limits'], lic['terms_identifier'], units)
        rights = agents['estate:rights-authority']
        anchor, refs = await ceremony.bank_rights(db, tenant, rights['principal_id'], rights['key_id'], units,
                                                  os.environ[admission['rights']['lawful_basis_path_env']])
        out['steps']['rights'] = {'anchor_ref': anchor, 'rights_refs': refs}
        runtimes = {}
        if attest:
            for descriptor in admission['runtimes']:
                record, worker_ref = await ceremony.admit_runtime(db, tenant, descriptor, units)
                runtimes[descriptor['runtime_id']] = {'worker_receipt_ref': worker_ref, 'key_id': record['key_id'],
                                                      'compute_classes': record['compute_classes'], 'capacity': record['capacity'],
                                                      'attestation': record['attestation']}
            out['steps']['runtimes'] = runtimes
            if admission.get('custody'):
                custody = admission['custody']
                record = {**custody, 'custodian_principal_id': 'runtime:' + custody['custodian_runtime_id']}
                out['steps']['custody_descriptor'] = await ceremony.set_custody_descriptor(db, tenant, record)
            else:
                out['steps']['custody_descriptor'] = 'none declared for this estate'
        else:
            out['steps']['runtimes'] = 'skipped (--attest not given)'
    out['finished_at'] = datetime.now(timezone.utc).isoformat()
    Path(receipt_path).parent.mkdir(parents=True, exist_ok=True)
    Path(receipt_path).write_text(json.dumps(out, indent=1, sort_keys=True, default=str))
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--admission', required=True)
    parser.add_argument('--attest', action='store_true')
    parser.add_argument('--receipt', default=None)
    args = parser.parse_args()
    spec = json.loads(Path(args.admission).read_text())
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    receipt = args.receipt or f"/app/assessment_workspace/notes/m3_execution/ceremony_{spec['tenant_id']}_{stamp}.json"
    result = asyncio.run(run(spec, args.attest, receipt))
    print(json.dumps({k: v for k, v in result.items() if k != 'steps'} | {'steps': list(result['steps'])}, indent=1))
    print('receipt', receipt)
