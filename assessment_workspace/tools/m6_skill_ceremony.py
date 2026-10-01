"""M6-T4 · skill-mode estate ceremony for one admitted estate (owner rulings 2026-10-01: 1a · 2a · 3a · 4a).

    python m6_skill_ceremony.py --admission <estate.json> [--attest] [--receipt <out.json>]

Extends an already-admitted estate so the deterministic unit-retrieval executor may answer over its sealed artefacts:
  1. admits the estate quality authority (custody key; signs quality_policy / context_policy receipts);
  2. admits each declared runtime as a principal of record (the handoff receiver resolves through the ordinary gate);
  3. seats the `answering` approval group (unseated → the admitted interim stand-in, re-admitted with that seat);
  4. lists the executor in the entitlement catalogue (local_served) — the only writer of a catalogue row is this ceremony;
  5. with --attest, re-attests every declared runtime with kinds [source, skill] and the skill-mode signer permissions.
Every record goes through the existing ledger writer / receipt API (services.estate_admission.ceremony); re-running with
the same inputs is idempotent. No account, password, role or secret is created or changed.
"""
import argparse
import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import load_dotenv  # noqa: E402

load_dotenv('/app/backend/.env')
from core import db  # noqa: E402
from services.enforce.control_scope import bind_control_scope  # noqa: E402
from services.enforce.principal_context_adapter import principal_context  # noqa: E402
from services.estate_admission import ceremony  # noqa: E402
from services.estate_admission.records import latest  # noqa: E402
from services.extraction_runtime.skill_worker import MODEL_ID  # noqa: E402

ANSWERING_GROUP = {'group': 'answering.grounded', 'purpose': 'answering', 'quorum': 1, 'members': []}
RESIDENCY = 'gpu-environment'


class as_actor:
    def __init__(self, principal_id, tenant):
        self.p = principal_context(principal_id)
        self.c = bind_control_scope({'principal_id': principal_id, 'tenant_id': tenant})

    def __enter__(self):
        self.p.__enter__()
        self.c.__enter__()
        return self

    def __exit__(self, *exc):
        self.c.__exit__(*exc)
        self.p.__exit__(*exc)


async def run(admission, attest, receipt_path):
    tenant = admission['tenant_id']
    units = sorted(admission['rights']['units'])
    org = admission['organisation']
    org_id = ceremony.opaque('org', tenant, org['legal_identity'])
    out = {'tenant_id': tenant, 'started_at': datetime.now(timezone.utc).isoformat(), 'rulings': {
        'executor': '2a deterministic retrieval executor (lexical ranking over sealed units, no LLM)',
        'ceremony': '2a re-run with kinds=[source, skill]', 'provision_gate': '3a operator identity required'}, 'steps': {}}
    with as_actor(org_id, tenant):
        current = await latest(db, tenant, 'principal_admission', org_id)
        if current is None:
            raise SystemExit('ESTATE_NOT_ADMITTED: run the M3 estate ceremony first')
        org_ref = current['row']['hash']
        qa_id = ceremony.opaque('agent', tenant, ceremony.QUALITY_AUTHORITY_SCOPE)
        qa_ref = await ceremony.admit_member(db, tenant, org_id, qa_id, 'Estate quality authority (signs quality and context policy receipts)',
                                             org['admitted_by'], kind='agent', autonomy_scope=ceremony.QUALITY_AUTHORITY_SCOPE)
        qa_signer = await ceremony.admit_custody_signer(db, tenant, qa_id, ceremony.QUALITY_AUTHORITY_KEY,
                                                        list(ceremony.QUALITY_AUTHORITY_PERMISSIONS), units)
        out['steps']['quality_authority'] = {'principal_id': qa_id, 'admission_ref': qa_ref, 'signer_ref': qa_signer}
        out['steps']['runtime_principals'] = {d['runtime_id']: await ceremony.admit_runtime_principal(db, tenant, org_id, d['runtime_id'], org['admitted_by'])
                                              for d in admission['runtimes']}
        groups_record = (await latest(db, tenant, 'approval_groups', 'default'))['payload']['record']
        groups = [g for g in groups_record['groups'] if g['purpose'] != 'answering'] + [dict(ANSWERING_GROUP)]
        unseated = [g['group'] for g in groups if not g.get('members')]
        stand_in = groups_record.get('interim_stand_in')
        if unseated:
            basis = (stand_in or {}).get('basis') or admission.get('interim_stand_in', {}).get('basis')
            if not basis:
                raise SystemExit('STAND_IN_BASIS_REQUIRED')
            stand_in = await ceremony.admit_stand_in(db, tenant, org_id, org['admitted_by'], unseated, units, basis)
        out['steps']['approval_groups'] = {'ref': await ceremony.set_approval_groups(db, tenant, groups, stand_in), 'groups': groups,
                                           'interim_stand_in': stand_in}
        row = {'model_identifier': MODEL_ID, 'access_class': 'local_served', 'status': 'listed', 'residency': RESIDENCY}
        out['steps']['catalogue'] = {'row': row, 'ref': await ceremony.admit_catalogue_row(db, tenant, org_id, row, org_ref)}
        runtimes = {}
        if attest:
            for descriptor in admission['runtimes']:
                descriptor = {**descriptor, 'kinds': sorted(set(descriptor['kinds']) | {'skill'})}
                record, worker_ref = await ceremony.admit_runtime(db, tenant, descriptor, units)
                runtimes[descriptor['runtime_id']] = {'worker_receipt_ref': worker_ref, 'key_id': record['key_id'], 'kinds': record['kinds'],
                                                      'roles': record['roles'], 'attestation': record['attestation']}
            out['steps']['runtimes'] = runtimes
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
    receipt = args.receipt or f"/app/assessment_workspace/notes/m6_execution/skill_ceremony_{spec['tenant_id']}_{stamp}.json"
    result = asyncio.run(run(spec, args.attest, receipt))
    print(json.dumps({k: v for k, v in result.items() if k != 'steps'} | {'steps': list(result['steps'])}, indent=1))
    print('receipt', receipt)
