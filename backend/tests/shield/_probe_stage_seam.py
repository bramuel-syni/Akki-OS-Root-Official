"""Diagnostic (SYNTHETIC text): show per-file protected values and the seam outcome for the live stage test pair."""
import asyncio, json, sys
from dotenv import load_dotenv
load_dotenv('/app/backend/.env'); sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend'); sys.path.insert(0, '/app/backend/tests/shield')
from services.synisense.shield import stage as st
import test_shield_stage as t

async def main():
    items = []
    for label, text in [(st.FILE_1, t.QUESTION), (st.FILE_2, t.DOC)]:
        it = await st._assess(label, t.SYSTEM if label == st.FILE_1 else None, text, 'RMS', t.PURPOSE, 'tenant_estate')
        items.append(it)
        print('=====', label); print('protected:', it['protected']); print('binding:', it['binding']); print('entities:', it['entities']); print('safe:', it['safe'][:600]); print('markers:', json.dumps({k: v for k, v in it['markers'].items() if k != 'reader'}, default=str)[:600]); print('reader:', json.dumps(it['markers']['reader'], default=str)[:900])
    try:
        seam, protected = st._reassociate(items); print('SEAM OK', seam)
    except st.StageRefused as exc:
        print('SEAM REFUSED', exc, getattr(exc, 'detail', None), exc.__dict__)

asyncio.run(main())
