"""Read-only probe: DIGICOW admitted runtimes/signers/catalogue state and live seam reachability (hostname only)."""
import asyncio
import json
import sys

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import load_dotenv  # noqa: E402

load_dotenv('/app/backend/.env')
from core import db  # noqa: E402
from services.estate_admission.records import latest  # noqa: E402
from services.ledger_writer.principal_control import read_events  # noqa: E402


async def main():
    from services.enforce.control_scope import bind_control_scope
    from services.enforce.principal_context_adapter import principal_context
    from services.estate_admission.ceremony import opaque
    org = opaque('org', 'DIGICOW', 'DigiCow — estate owner of record (legal name as supplied in the owner estate intake, digicow.xlsx)')
    with principal_context(org), bind_control_scope({'principal_id': org, 'tenant_id': 'DIGICOW'}):
        await _main()


async def _main():
    out = {}
    runtimes = await latest(db, 'DIGICOW', 'admitted_runtime')
    out['runtimes'] = {rid: {k: e['payload']['record'][k] for k in ('kinds', 'roles', 'principal_id', 'key_id', 'status', 'worker_receipt_ref')}
                       for rid, e in runtimes.items()}
    signers = await latest(db, 'DIGICOW', 'admitted_signer')
    out['signers'] = {sid: e['payload']['record']['permissions'] for sid, e in signers.items()}
    groups = await latest(db, 'DIGICOW', 'approval_groups', 'default')
    out['approval_groups'] = groups['payload']['record'] if groups else None
    principals = await latest(db, 'DIGICOW', 'principal_admission')
    out['principals'] = {pid: (e['payload']['record']['kind'], e['payload']['record'].get('autonomy_scope')) for pid, e in principals.items()}
    out['catalogue_rows'] = len(await read_events(db, {'row.tenant_id': 'DIGICOW', 'row.resource_type': 'entitlement_catalog'}))
    custody = await latest(db, 'DIGICOW', 'custody_descriptor', 'default')
    out['custody'] = {k: v for k, v in custody['payload']['record'].items() if k in ('provider', 'bucket', 'prefix', 'custodian_runtime_id')} if custody else None
    objects = await read_events(db, {'row.tenant_id': 'DIGICOW', 'row.resource_type': 'extraction_object',
                                     'row.run_id': 'req-97999a0b46d2f51564b85dcd05d871a2'})
    out['corpus_object'] = objects[-1]['payload']['object'] if objects else None
    out['corpus_artifacts'] = objects[-1]['payload']['artifacts'] if objects else None
    if '--live' in sys.argv:
        from services.census_autonomy.remote_dispatch import _connect
        for slug in ('akki-vm', 'akki-vm-ii'):
            try:
                client, config = _connect(slug, 20)
                _, stdout, _ = client.exec_command('hostname && ls ~/.akki-extraction/identity 2>/dev/null | head -2')
                out['live:' + slug] = stdout.read().decode().split()
                client.close()
            except Exception as exc:  # probe only
                out['live:' + slug] = 'UNREACHABLE:' + type(exc).__name__
    print(json.dumps(out, indent=1, default=str))


asyncio.run(main())
