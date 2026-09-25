"""Idempotent owner-approved membership annotation of existing control-plane accounts only."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient


def main():
    load_dotenv('/app/backend/.env')
    db = MongoClient(os.environ['MONGO_URL'])[os.environ['DB_NAME']]
    approved = [f'demo.{name}@demo.rms.example.com' for name in ('master_admin', 'dpo', 'operator', 'analyst')]
    before = list(db.users.find({'email': {'$in': approved}}))
    if len(before) != 4 or any(r.get('tenant_id') not in (None, 'RMS') for r in before):
        raise RuntimeError('Existing account inventory differs from explicit approval; no changes applied.')
    rows = []
    for account in before:
        db.users.update_one({'_id': account['_id'], 'tenant_id': account.get('tenant_id')},
                            {'$set': {'tenant_id': 'RMS', 'tenant_admission_ref': 'CP-CENSUS-OPERATIONAL-V1-owner-approved-20260925'}})
        after = db.users.find_one({'_id': account['_id']})
        if after.get('tenant_id') != 'RMS' or after['password_hash'] != account['password_hash'] or after['roles'] != account['roles']:
            raise RuntimeError('Membership invariant failed.')
        rows.append({'email': account['email'], 'tenant_id': after['tenant_id'],
                     'roles_unchanged': True, 'password_unchanged': True, 'created_account': False})
    path = Path('/app/assessment_workspace/phase0/drill_receipts/census_operational_v1/membership_binding.json')
    path.write_text(json.dumps({'at_utc': datetime.now(timezone.utc).isoformat(),
                                'authority': 'Owner replied Approved to explicit four-account RMS admission',
                                'results': rows}, indent=2) + '\n')
    print(json.dumps({'verified_existing_accounts': len(rows), 'receipt': str(path)}))


if __name__ == '__main__':
    main()