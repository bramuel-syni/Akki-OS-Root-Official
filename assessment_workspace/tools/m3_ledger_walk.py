"""Read one request's rows on the canonical ledger under the requester's own control scope (read-only).

    python m3_ledger_walk.py --tenant DIGICOW --principal <principal_id> --run <request_id> [--grep TEXT]
"""
import argparse
import asyncio
import json
import sys

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import load_dotenv  # noqa: E402

load_dotenv('/app/backend/.env')
from core import db  # noqa: E402
from services.enforce.control_scope import bind_control_scope  # noqa: E402
from services.enforce.principal_context_adapter import principal_context  # noqa: E402
from services.ledger_writer.principal_control import read_events  # noqa: E402


async def main(a):
    with principal_context(a.principal), bind_control_scope({'principal_id': a.principal, 'tenant_id': a.tenant}):
        query = {'row.tenant_id': a.tenant}
        if a.run:
            query['row.run_id'] = a.run
        if a.resource:
            query['row.resource_type'] = a.resource
        rows = await read_events(db, query)
    for e in rows:
        p, r = e['payload'], e['row']
        slot = p.get('slot') or p.get('kind') or r.get('event_type')
        body = json.dumps(p.get('data') if 'data' in p else {k: v for k, v in p.items() if k != 'principal_id'}, default=str)
        line = f"{r['resource_type']} | {slot} | {r.get('decision')} {r.get('reason_code')} | {body}"
        if not a.grep or a.grep in line:
            print(line[: a.width])
            print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tenant', required=True); parser.add_argument('--principal', required=True)
    parser.add_argument('--run'); parser.add_argument('--resource'); parser.add_argument('--grep'); parser.add_argument('--width', type=int, default=700)
    asyncio.run(main(parser.parse_args()))
