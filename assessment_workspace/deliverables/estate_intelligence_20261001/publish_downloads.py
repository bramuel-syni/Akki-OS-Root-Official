"""Publish exact report bytes as static downloads, independent of the API upstream."""
import hashlib
import json
import shutil
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/app/backend/deliverables')
PUBLIC = Path('/app/frontend/public/downloads')
PUBLIC.mkdir(parents=True, exist_ok=True)
outputs = {}
for ext in ['pptx', 'docx']:
    source = SOURCE / f'RMS_Estate_Intelligence_and_Language_Opportunities.{ext}'
    destination = PUBLIC / f'RMS_Estate_Report.{ext}'
    shutil.copyfile(source, destination)
    outputs[ext] = {'file': destination.name, 'bytes': destination.stat().st_size,
                    'sha256': hashlib.sha256(destination.read_bytes()).hexdigest()}

bundle = PUBLIC / 'RMS_Estate_Reports.zip'
with ZipFile(bundle, 'w', compression=ZIP_DEFLATED, compresslevel=9) as archive:
    for ext in ['pptx', 'docx']:
        file = PUBLIC / outputs[ext]['file']
        entry = ZipInfo(file.name, date_time=(2026, 10, 1, 0, 0, 0))
        entry.compress_type = ZIP_DEFLATED
        entry.external_attr = 0o644 << 16
        archive.writestr(entry, file.read_bytes())
outputs['zip'] = {'file': bundle.name, 'bytes': bundle.stat().st_size,
                  'sha256': hashlib.sha256(bundle.read_bytes()).hexdigest()}
(ROOT / 'static_download_manifest.json').write_text(json.dumps(outputs, indent=2) + '\n')
print(json.dumps(outputs, indent=2))