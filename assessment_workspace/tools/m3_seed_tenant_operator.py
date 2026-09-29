"""Seed ONE tenant-bound operator account through the existing user store (idempotent).

    python m3_seed_tenant_operator.py --tenant DIGICOW --email demo.operator@demo.digicow.example.com \
        --password <demo-marked password> --name "Demo · DigiCow Operator" --admission-ref <ruling ref>

Reuses `services.auth.user_store.create_user` (bcrypt hash, same roles register); the account is
inserted only if absent, then bound to the tenant exactly as the 2026-09-25 RMS binding tool did.
No hashing, token or login logic is touched. Record the credential in /app/memory/test_credentials.md.
"""
import argparse
import asyncio
import json
import sys

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import load_dotenv  # noqa: E402

load_dotenv('/app/backend/.env')
from core import db  # noqa: E402
from services.auth.user_store import create_user, get_by_email  # noqa: E402
from services.tenant_separation.tenant_registry import CANONICAL_TENANT_IDS  # noqa: E402


async def run(args):
    if args.tenant not in CANONICAL_TENANT_IDS:
        raise SystemExit(f'TENANT_NOT_CANONICAL:{args.tenant}')
    email = args.email.lower().strip()
    existing = await get_by_email(email)
    created = False
    if existing is None:
        await create_user(email=email, password_plaintext=args.password, name=args.name,
                          roles=[r.strip() for r in args.roles.split(',') if r.strip()], key_grants=[])
        created = True
        existing = await get_by_email(email)
    if existing.get('tenant_id') not in (None, args.tenant):
        raise SystemExit(f"ACCOUNT_BOUND_TO_OTHER_TENANT:{existing.get('tenant_id')}")
    await db.users.update_one({'_id': existing['_id']}, {'$set': {'tenant_id': args.tenant, 'tenant_admission_ref': args.admission_ref}})
    after = await get_by_email(email)
    return {'email': email, 'created': created, 'tenant_id': after['tenant_id'], 'roles': after['roles'],
            'principal_id': str(after['_id']), 'tenant_admission_ref': after['tenant_admission_ref']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tenant', required=True)
    parser.add_argument('--email', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--roles', default='operator,ask_console_user')
    parser.add_argument('--admission-ref', required=True)
    print(json.dumps(asyncio.run(run(parser.parse_args())), indent=1))
