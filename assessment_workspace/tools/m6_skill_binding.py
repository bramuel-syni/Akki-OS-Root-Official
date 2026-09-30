"""M6-T4 · bind one callable skill to the DIGICOW sealed artefact for the existing DIGICOW operator (owner rulings 2026-09-30: 1a, 2b).

    python m6_skill_binding.py --receipt notes/m6_execution/skill_binding_DIGICOW_<stamp>.json

Idempotent. Step 1 registers ONE engineer key grant for the DIGICOW operator through the existing grant service
(class external · path governed_extract · floor utterance · scope digicow_rds; ledger row emitted by the service).
Step 2 provisions ONE callable skill (write-once, `callable_skills`) whose corpus slice is the verified M3 artefact
`akki://artifact/DIGICOW/req-97999a0b46d2f51564b85dcd05d871a2/qualified-units`. No account, password, role, runtime,
signer or ceremony record is created or changed; no ruling on the answering executor is inferred (owner 3b/4b hold).
"""
import argparse
import asyncio
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import load_dotenv  # noqa: E402

load_dotenv('/app/backend/.env')
from core import db  # noqa: E402
from services.auth.engineer_key_grant import EngineerKeyGrantRegistrationRequest  # noqa: E402
from services.auth.engineer_key_grant_service import COLLECTION as GRANTS, register_grant  # noqa: E402
from services.transform_forms.callable_skill_persistence import COLLECTION as SKILLS, provision_skill  # noqa: E402

TENANT = 'DIGICOW'
GRANTEE = 'demo.operator@demo.digicow.example.com'
GRANTOR = 'owner-ruling:M6-T4:2026-09-30:2b'
TUPLE = {'key_class': 'external', 'path': 'governed_extract', 'floor': 'utterance', 'scope': 'digicow_rds'}
CORPUS = 'akki://artifact/DIGICOW/req-97999a0b46d2f51564b85dcd05d871a2/qualified-units'
CORPUS_SHA256 = '64a6938aa34bce613b067fce38c3ad0cd4f1ab5621297171c4932c5d6ad436aa'
LAWFUL_BASIS_ANCHOR = '2d1bde6ef65c6ac826132546179f10b92687b177fc03c78d07f2d9bc11792952'  # DIGICOW ceremony rights anchor (2026-09-29)
JUSTIFICATION = ('M6-T4 skill really callable: the DIGICOW operator of record is the permitted external-style caller of the skill '
                 'bound to the verified M3 artefact req-97999a0b46d2f51564b85dcd05d871a2 (owner ruling 2026-09-30, 2b).')


async def grant():
    account = await db.users.find_one({'email': GRANTEE}, {'tenant_id': 1})
    if not account or account.get('tenant_id') != TENANT:
        raise SystemExit('GRANTEE_NOT_BOUND_TO_TENANT')
    existing = await db[GRANTS].find_one({'grantee_email': GRANTEE, 'revoked_at': None, **TUPLE}, {'_id': 0})
    if existing:
        return existing, False
    req = EngineerKeyGrantRegistrationRequest(grantee_email=GRANTEE, justification=JUSTIFICATION,
                                              lawful_basis_ref='activation_receipt:' + LAWFUL_BASIS_ANCHOR, **TUPLE)
    record = await register_grant(req, grantor_id=GRANTOR)
    return record.model_dump(mode='json'), True


async def provision(grant_id):
    existing = await db[SKILLS].find_one({'corpus_slice_ref': CORPUS, 'key_grant_id': grant_id, 'revoked_at': None}, {'_id': 0})
    if existing:
        return existing, False
    skill_id = uuid.uuid4().hex
    record = await provision_skill(db, skill_id=skill_id, corpus_slice_ref=CORPUS, key_grant_id=grant_id,
                                   floor=TUPLE['floor'], scope=TUPLE['scope'], endpoint_path=f'/api/callable_skill/{skill_id}/query')
    return record.model_dump(mode='json'), True


async def run(receipt_path):
    grant_record, grant_created = await grant()
    skill_record, skill_created = await provision(grant_record['grant_id'])
    receipt = {
        'at': datetime.now(timezone.utc).isoformat(), 'tenant_id': TENANT, 'rulings': {'target': '1a DIGICOW artefact', 'caller': '2b existing operator + key grant',
        'executor': '3b HELD until a QA model is admitted', 'ceremony': '4b not re-run'},
        'key_grant': {**grant_record, 'created_now': grant_created, 'grantor_id': grant_record.get('grantor_id', GRANTOR)},
        'skill': {**skill_record, 'created_now': skill_created, 'corpus_sha256': CORPUS_SHA256},
        'boundary': {'query': skill_record['endpoint_path'], 'query_intents': f"/api/callable_skill/{skill_record['skill_id']}/query-intents"},
        'not_claimed': 'No grounded result: the native runtime has no admitted skill executor, plan, worker skill_response or independent anchors (owner 3b/4b).',
    }
    for key in ('issued_at', 'revoked_at'):
        if isinstance(receipt['key_grant'].get(key), datetime):
            receipt['key_grant'][key] = receipt['key_grant'][key].isoformat()
    path = Path(receipt_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, indent=1, sort_keys=True, default=str))
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', required=True)
    print(json.dumps(asyncio.run(run(parser.parse_args().receipt)), indent=1, default=str))
