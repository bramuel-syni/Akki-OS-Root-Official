"""Re-issue the owner report pair through Planner → Worker → Content Manager → Frontier writer. The pinned evidence and content model from
build_report.py are the worker's output; the writer authors every sentence; the gate decides whether the deterministic studio may build.
Publishes the released bytes to the same download paths the owner already uses."""
import asyncio
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path('/app/backend/vendored/extraction_akki/backend')
sys.path.insert(0, str(ROOT))
from dotenv import load_dotenv  # noqa: E402
load_dotenv('/app/backend/.env')
from services.transform_forms.doc_studio import author  # noqa: E402
from services.transform_forms.doc_studio.skill_env import build_env  # noqa: E402

SCRIPTS = ROOT / 'services/transform_forms/doc_studio/skill/scripts'
SOURCE, TARGET, RELEASE = HERE / 'commission', HERE / 'commission_authored', HERE / 'release_authored'
DOWNLOADS = Path('/app/frontend/public/downloads')
DELIVERABLES = Path('/app/backend/deliverables')


async def main():
    files = {name: json.loads((SOURCE / name).read_text()) for name in ('brief.json', 'content.json', 'verdict.json', 'deck.json', 'paper.json')}
    files['content.json']['claims'] = {}  # the deterministic claims were the gibberish; the writer authors every claim the reader sees
    bound, meta, issues = await author.compose(files, 'RMS', 'owner', 'author:estate-deliverable-20261002')
    print('writer', meta.get('model'), 'tokens', meta.get('tokens_in'), '+', meta.get('tokens_out'), 'gate', meta.get('gate'))
    if issues:
        (HERE / 'authored-draft.rejected.json').write_text(json.dumps({'draft': meta.get('draft'), 'issues': issues}, indent=1))
        raise SystemExit('content manager rejected the draft: ' + '; '.join(issues[:8]))
    if TARGET.exists(): shutil.rmtree(TARGET)
    TARGET.mkdir()
    for name, doc in bound.items(): (TARGET / name).write_text(json.dumps(doc, indent=1, ensure_ascii=False))
    (TARGET / 'authored-draft.json').write_text(json.dumps({'draft': meta.get('draft'), 'meta': {k: v for k, v in meta.items() if k != 'draft'}}, indent=1, ensure_ascii=False))
    if RELEASE.exists(): shutil.rmtree(RELEASE)
    run = subprocess.run([sys.executable, str(SCRIPTS / 'build.py'), str(TARGET), str(RELEASE), '--prove'], capture_output=True, text=True, timeout=900, env=build_env(), cwd=str(SCRIPTS.parent))
    (HERE / 'release_authored-build.log').write_text(run.stdout + '\n--- stderr ---\n' + run.stderr)
    print('build rc', run.returncode); print(run.stdout[-1500:])
    if run.returncode != 0:
        raise SystemExit('build failed')
    out = RELEASE / 'a' / 'out'
    pptx = next(out.glob('*.pptx')); docx = next(out.glob('*.docx'))
    DOWNLOADS.mkdir(parents=True, exist_ok=True); DELIVERABLES.mkdir(parents=True, exist_ok=True)
    shutil.copy(pptx, DOWNLOADS / 'RMS_Estate_Report.pptx'); shutil.copy(docx, DOWNLOADS / 'RMS_Estate_Report.docx')
    shutil.copy(pptx, DELIVERABLES / 'RMS_Estate_Intelligence_and_Language_Opportunities.pptx'); shutil.copy(docx, DELIVERABLES / 'RMS_Estate_Intelligence_and_Language_Opportunities.docx')
    with zipfile.ZipFile(DOWNLOADS / 'RMS_Estate_Reports.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(DOWNLOADS / 'RMS_Estate_Report.pptx', 'RMS_Estate_Report.pptx'); z.write(DOWNLOADS / 'RMS_Estate_Report.docx', 'RMS_Estate_Report.docx')
    manifest = {name: {'sha256': hashlib.sha256((DOWNLOADS / name).read_bytes()).hexdigest(), 'bytes': (DOWNLOADS / name).stat().st_size} for name in ('RMS_Estate_Report.pptx', 'RMS_Estate_Report.docx', 'RMS_Estate_Reports.zip')}
    manifest['authoring'] = {k: v for k, v in meta.items() if k != 'draft'}
    (HERE / 'authored_release_manifest.json').write_text(json.dumps(manifest, indent=1))
    print(json.dumps(manifest, indent=1))


asyncio.run(main())
