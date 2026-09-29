"""Operator resolution for a NATIVE_RIGHTS_PROOF_REQUIRED hold on an already independently-verified artefact.

    python m3_extend_rights.py --tenant DIGICOW --principal <requester principal_id> --request <request_id> --deadline <deadline_epoch>

Reads the request's own `registry` slot (inspection already recorded), then asks the estate rights authority
(custody key) to extend the source grant along the worker-signed lineage — the same `derived_rights.extend`
the inspector runs. Idempotent; refuses when lineage or parent rights are missing or withdrawn.
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
from services.estate_admission.ceremony import receipts_for  # noqa: E402
from services.extraction_runtime import derived_rights  # noqa: E402
from services.northena.execution_journal import LedgerJournal  # noqa: E402
from services.northena.execution_models import Artifact  # noqa: E402
from services.portal_operational.execution import ExecutionBudget, frozen_request  # noqa: E402


async def main(a):
    scope = {'principal_id': a.principal, 'tenant_id': a.tenant, 'roles': ['operator']}
    with principal_context(a.principal), bind_control_scope(scope):
        receipts = receipts_for(db)
        request = await frozen_request(db, scope, a.request, ExecutionBudget(deadline_epoch=a.deadline), receipts=receipts)
        registry = next((r for r in await LedgerJournal(db).read(request) if r['slot'] == 'registry'), None)
        if registry is None:
            raise SystemExit('REGISTRY_SLOT_ABSENT: no independent inspection recorded; nothing to extend')
        artifacts = tuple(Artifact.model_validate(x) for x in registry['data']['artifacts'])
        refs = await derived_rights.extend(db, receipts, request, artifacts, await receipts.events())
        return {'request_id': a.request, 'inspection_ref': registry['data']['inspection_ref'], 'rights_refs': refs}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tenant', required=True); parser.add_argument('--principal', required=True)
    parser.add_argument('--request', required=True); parser.add_argument('--deadline', type=int, required=True)
    print(json.dumps(asyncio.run(main(parser.parse_args())), indent=1))
