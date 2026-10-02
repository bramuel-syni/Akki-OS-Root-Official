"""Owner order 2026-10-02: build the estate + language report pack (Astra plan → Sonnet write → Fable review → deterministic build)
and publish the exact released bytes as static downloads. Re-authors automatically when newer evidence exists; `--force` always re-authors."""
import asyncio
import json
import sys
import time

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import load_dotenv
load_dotenv('/app/backend/.env')

from services.census_autonomy import estate_intelligence_report as eir  # noqa: E402
from services.transform_forms.doc_studio import publish, service as studio  # noqa: E402


async def main():
    report = eir.latest_report(cached_only=True)
    force = '--force' in sys.argv
    actor = next((a for a in sys.argv[1:] if not a.startswith('--')), 'akki-autopilot')
    t = time.time()
    record, created = await studio.create_authored('estate-intelligence', report['job_id'], 'RMS', actor, force=force)
    print('commission', record['commission_id'], 'created', created, 'version', record['current_content_version'], 'in', round(time.time() - t), 's')
    print(json.dumps({k: record.get(k) for k in ('title', 'release', 'authoring')}, indent=1, default=str)[:4000])
    build = record['builds'][-1] if record.get('builds') else None
    if not build or build['status'] != 'released':
        print('NOT RELEASED', json.dumps(build, default=str)[:1500] if build else record['release'])
        return 1
    print(json.dumps(publish.publish('RMS', record), indent=2))
    return 0


sys.exit(asyncio.run(main()))
