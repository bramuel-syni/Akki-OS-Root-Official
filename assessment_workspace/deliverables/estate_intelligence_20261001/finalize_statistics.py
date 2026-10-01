"""Deterministic Office metadata finalization; document body and slide content are untouched."""
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from zipfile import ZipFile
from lxml import etree

ROOT = Path(__file__).resolve().parent
NAME = 'rms-estate-and-local-language-opportunities'
PDF = ROOT / 'render/paper' / (NAME + '.pdf')
pages = int(re.search(r'^Pages:\s+(\d+)', subprocess.check_output(['pdfinfo', str(PDF)], text=True), re.M).group(1))
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
office = 'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties'
hashes = []
for branch in ['a', 'b']:
    path = ROOT / f'release/{branch}/out/{NAME}.docx'
    with ZipFile(path) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    body = etree.fromstring(dict((i.filename, data) for i, data in items)['word/document.xml'])
    paragraphs = [''.join(p.xpath('.//w:t/text()', namespaces=ns)) for p in body.xpath('.//w:p', namespaces=ns)]
    text = '\n'.join(paragraphs)
    stats = {'Pages': pages, 'Words': len(re.findall(r"\w+(?:['’\-]\w+)*", text)),
             'Characters': len(re.sub(r'\s', '', text)), 'CharactersWithSpaces': len(text), 'Paragraphs': len(paragraphs)}
    output = path.with_suffix('.tmp')
    with ZipFile(output, 'w') as z:
        for info, data in items:
            if info.filename == 'docProps/app.xml':
                app = etree.fromstring(data)
                for key, value in stats.items():
                    node = app.find(f'{{{office}}}{key}')
                    if node is None: node = etree.SubElement(app, f'{{{office}}}{key}')
                    node.text = str(value)
                # Wrapped physical lines are not measured by the source-text counter.
                lines = app.find(f'{{{office}}}Lines')
                if lines is not None: app.remove(lines)
                data = etree.tostring(app, xml_declaration=True, encoding='UTF-8', standalone=True)
            z.writestr(info, data)
    output.replace(path)
    hashes.append(hashlib.sha256(path.read_bytes()).hexdigest())
assert hashes[0] == hashes[1], 'Metadata finalization must remain reproducible.'
manifest = {'body_changed': False, 'statistics': stats,
            'statistics_note': 'Pages from LibreOffice rendering; words/characters/paragraphs from the OOXML body. Word may recalculate text statistics using its own tokenizer.', 'outputs': {}}
for ext in ['pptx', 'docx']:
    src = ROOT / f'release/a/out/{NAME}.{ext}'
    destination = Path('/app/backend/deliverables') / f'RMS_Estate_Intelligence_and_Language_Opportunities.{ext}'
    shutil.copy2(src, destination)
    manifest['outputs'][ext] = {'sha256': hashlib.sha256(src.read_bytes()).hexdigest(), 'bytes': src.stat().st_size, 'file': destination.name}
(ROOT / 'finalized_release_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps(manifest, indent=2))