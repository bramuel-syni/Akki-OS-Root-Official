"""Commission the estate-wide intelligence pack through Planner → Worker → Content Manager → Frontier writer, then print the story as written."""
import asyncio
import json
import sys
import time

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import load_dotenv
load_dotenv('/app/backend/.env')

from services.census_autonomy import estate_intelligence_report as eir  # noqa: E402
from services.transform_forms.doc_studio import service as studio, store  # noqa: E402


async def main():
    report = eir.latest_report(cached_only=True)
    t = time.time()
    record, created = await studio.create_authored('estate-intelligence', report['job_id'], 'RMS', sys.argv[1] if len(sys.argv) > 1 else 'akki-autopilot')
    print('commission', record['commission_id'], 'created', created, 'in', round(time.time() - t), 's')
    print(json.dumps({k: record.get(k) for k in ('title', 'release', 'authoring', 'current_content_version')}, indent=1, default=str))
    vdir = store.version_dir('RMS', record['commission_id'], record['current_content_version'])
    draft = json.load(open(vdir / 'authored-draft.json'))['draft'] if (vdir / 'authored-draft.json').exists() else None
    if draft:
        print('\nTITLE:', draft.get('title'), '—', draft.get('subtitle'))
        for p in draft['paper']['summary']: print('SUMMARY:', p)
        for k, s in draft['slots'].items(): print(f'[{k}]', json.dumps(s, ensure_ascii=False))
    if record.get('builds'):
        b = record['builds'][-1]
        print('\nbuild', b.get('status'), [o.get('name') for o in b.get('outputs', [])], json.dumps(b.get('qa'), default=str)[:300])


asyncio.run(main())
