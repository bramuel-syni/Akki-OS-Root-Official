"""Smoke the Planner → Worker → Content Manager → Frontier writer pipeline on the banked estate report, then build."""
import asyncio
import json
import sys
import time

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import load_dotenv
load_dotenv('/app/backend/.env')

from services.census_autonomy import estate_intelligence_report as eir  # noqa: E402
from services.transform_forms.doc_studio import service as studio  # noqa: E402


async def main():
    report = eir.latest_report(cached_only=True)
    job_id = report['job_id']
    print('estate report', job_id, 'measured', report.get('measured_at'))
    t = time.time()
    record, created = await studio.create_authored('estate-intelligence', job_id, 'RMS', 'demo.operator@demo.rms.example.com')
    print('created', created, 'in', round(time.time() - t), 's')
    print(json.dumps({k: record.get(k) for k in ('commission_id', 'title', 'release', 'authoring', 'current_content_version')}, indent=1, default=str)[:3000])
    if record['builds']:
        b = record['builds'][-1]
        print('build', b['status'], b.get('error'), [o.get('name') for o in b.get('outputs', [])])
        print('validate', json.dumps(b.get('validate'), default=str)[:800])
        print('qa', json.dumps(b.get('qa'), default=str)[:600])


asyncio.run(main())
