"""Owner order 2026-10-02: build the estate + language report pack (Astra plan → Sonnet write → Fable review → deterministic build)
and publish the exact released bytes as static downloads. Idempotent on content; `--force` authors a new version when new evidence landed."""
import asyncio
import hashlib
import json
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import load_dotenv
load_dotenv('/app/backend/.env')

from services.census_autonomy import estate_intelligence_report as eir  # noqa: E402
from services.transform_forms.doc_studio import service as studio, store  # noqa: E402

PUBLIC = Path('/app/frontend/public/downloads')
NAME = 'RMS_Estate_and_Language_Review'
MANIFEST = Path('/app/assessment_workspace/deliverables/estate_language_20261002/static_download_manifest.json')


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
    bdir = store.build_dir('RMS', record['commission_id'], build['build_id']) / 'a' / 'out'
    PUBLIC.mkdir(parents=True, exist_ok=True)
    published = {'commission_id': record['commission_id'], 'build_id': build['build_id'], 'content_version': record['current_content_version'], 'files': {}}
    for out in build['outputs']:
        if out['format'] not in ('docx', 'pptx', 'xlsx'):
            continue
        src = bdir / out['name']
        dst = PUBLIC / f"{NAME}.{out['format']}"
        shutil.copyfile(src, dst)
        published['files'][out['format']] = {'file': dst.name, 'bytes': dst.stat().st_size, 'sha256': hashlib.sha256(dst.read_bytes()).hexdigest(), 'source_sha256': out['sha256']}
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(published, indent=2) + '\n')
    print(json.dumps(published, indent=2))
    return 0


sys.exit(asyncio.run(main()))
