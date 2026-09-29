"""M3-T5 live drill: a write verb sent to the admitted worker runtime is refused by the guard BEFORE any
connection is opened, and the refusal comes back signed by the runtime's own key; E1 banks the receipt.

    python m3_write_refusal_drill.py --tenant DIGICOW --principal <requester principal_id> --runtime akki-vm --unit digicow_rds
"""
import argparse
import asyncio
import hashlib
import json
import sys

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import load_dotenv  # noqa: E402

load_dotenv('/app/backend/.env')
from core import db  # noqa: E402
from services.enforce.control_scope import bind_control_scope  # noqa: E402
from services.enforce.principal_context_adapter import principal_context  # noqa: E402
from services.estate_admission import signing  # noqa: E402
from services.estate_admission.ceremony import receipts_for  # noqa: E402
from services.estate_admission.runtimes import runtime_by_id  # noqa: E402
from services.extraction_runtime import remote  # noqa: E402

WRITES = ('DELETE FROM digicow_live.training_questions WHERE id = 1',
          'UPDATE digicow_live.training_questions SET answer = NULL WHERE id = 1',
          'DROP TABLE digicow_live.training_questions',
          'INSERT INTO digicow_live.training_questions (id) VALUES (999999)')


async def main(a):
    scope = {'principal_id': a.principal, 'tenant_id': a.tenant, 'roles': ['operator']}
    out = {'tenant_id': a.tenant, 'runtime_id': a.runtime, 'attempts': []}
    with principal_context(a.principal), bind_control_scope(scope):
        descriptor = await runtime_by_id(db, a.tenant, a.runtime)
        receipts = receipts_for(db)
        context = hashlib.sha256(b'm3-t5-write-refusal-drill').hexdigest()
        for sql in WRITES:
            control = {'mode': 'write_attempt', 'tenant_id': a.tenant, 'request_sha256': context, 'operation_key': 'm3-t5',
                       'fence': 0, 'scope_refs': [a.unit], 'sql': sql, 'sign': True}
            value = await remote.call_async(descriptor, control, deadline_seconds=90)
            entry = {'sql_sha256': hashlib.sha256(sql.encode()).hexdigest(), 'verb': sql.split()[0], 'status': value.get('status'),
                     'reason_code': value.get('reason_code'), 'signer_id': value.get('receipt', {}).get('signer_id')}
            if value.get('status') == 'refused' and value.get('receipt'):
                entry['refusal_receipt_ref'] = await receipts.record(signing.runtime_receipt(value['receipt']))
            out['attempts'].append(entry)
    out['all_refused'] = all(e['status'] == 'refused' and e['reason_code'] == 'WRITE_VERB_REFUSED' and e.get('refusal_receipt_ref') for e in out['attempts'])
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tenant', required=True); parser.add_argument('--principal', required=True)
    parser.add_argument('--runtime', default='akki-vm'); parser.add_argument('--unit', required=True)
    print(json.dumps(asyncio.run(main(parser.parse_args())), indent=1))
