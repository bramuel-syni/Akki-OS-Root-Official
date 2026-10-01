"""Roll an admitted monthly licence into the current period — an estate ceremony step, never over HTTP.

    python m3_roll_licence_period.py --tenant DIGICOW [--tenant RMS] [--receipt out.json]

The licence, its admission receipt and its terms are restated unchanged; only the period moves. A licence that
is inactive, past renewal, not monthly, or already banked for this period is left alone (idempotent).
"""
import argparse
import asyncio
import json
import sys
from datetime import datetime, timezone

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import load_dotenv  # noqa: E402

load_dotenv('/app/backend/.env')
from core import db  # noqa: E402
from services.enforce.control_scope import bind_control_scope  # noqa: E402
from services.enforce.principal_context_adapter import principal_context  # noqa: E402
from services.estate_admission import ceremony  # noqa: E402
from services.estate_admission.records import latest  # noqa: E402


async def organisation(tenant):
    bootstrap = f'ceremony:{tenant}'
    with principal_context(bootstrap), bind_control_scope({'principal_id': bootstrap, 'tenant_id': tenant}):
        admissions = await latest(db, tenant, 'principal_admission')
    for event in admissions.values():
        record = event['payload']['record']
        if record.get('kind') == 'organisation':
            return record['principal_id']
    raise SystemExit(f'ORGANISATION_NOT_ADMITTED:{tenant}')


async def roll(tenant):
    org = await organisation(tenant)
    with principal_context(org), bind_control_scope({'principal_id': org, 'tenant_id': tenant}):
        return {'tenant': tenant, 'organisation_principal_id': org, **await ceremony.roll_licence_period(db, tenant)}


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tenant', action='append', required=True)
    parser.add_argument('--receipt')
    args = parser.parse_args()
    out = {'at': datetime.now(timezone.utc).isoformat(), 'results': [await roll(t) for t in args.tenant]}
    text = json.dumps(out, indent=1, sort_keys=True)
    print(text)
    if args.receipt:
        with open(args.receipt, 'w') as handle:
            handle.write(text)


if __name__ == '__main__':
    asyncio.run(main())
