"""Read local documentary/source evidence; write audit copies only. No estate I/O."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path('/app')
OUT = ROOT / 'assessment_workspace/notes/canon_code_audit_20260925'
CANON = ROOT / 'assessment_workspace/canon'
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def docx_lines(path):
    with zipfile.ZipFile(path) as z:
        body = ET.fromstring(z.read('word/document.xml')).find(W + 'body')
        return [''.join(t.text or '' for t in n.iter(W + 't'))
                for n in body.iter(W + 'p')]

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows, corpus = [], []
    for path in sorted(CANON.rglob('*')):
        if not path.is_file():
            continue
        raw = path.read_bytes()
        item = {'path': str(path.relative_to(ROOT)), 'bytes': len(raw),
                'sha256': hashlib.sha256(raw).hexdigest(), 'semantic_review': 'not_claimed_by_inventory'}
        lines = None
        if path.suffix in ('.txt', '.md'):
            lines = raw.decode('utf-8', errors='replace').splitlines()
            item['coordinate'] = 'source line'
        elif path.suffix == '.docx':
            lines = docx_lines(path)
            item['coordinate'] = 'document.xml paragraph in body order, tables included'
        if lines is not None:
            item['lines_or_paragraphs'] = len(lines)
            corpus.append('\n# SOURCE: ' + item['path'] + '\nCoordinate: ' + item['coordinate'] + '\n')
            corpus.extend(f'{i}: {line}' for i, line in enumerate(lines, 1))
        rows.append(item)
    frontend = []
    paths = [ROOT/'frontend/src/App.js']
    for base in ['pages', 'hooks', 'lib']:
        paths.extend(sorted((ROOT/'frontend/src'/base).rglob('*')))
    paths.extend(sorted((ROOT/'frontend/src/components').glob('*.jsx')))
    for path in paths:
        if path.is_file() and path.suffix in ('.js', '.jsx', '.ts', '.tsx'):
            frontend.append('\n# SOURCE: ' + str(path.relative_to(ROOT)) + '\n')
            frontend.extend(f'{i}: {line}' for i, line in enumerate(path.read_text().splitlines(), 1))
    snapshot = {'observed_at_utc': datetime.now(timezone.utc).isoformat(),
                'app_head': subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip(),
                'method': 'filesystem inventory and deterministic extraction; NOT semantic conformance review',
                'canon_files': rows}
    (OUT/'source_inventory.json').write_text(json.dumps(snapshot, indent=2)+'\n')
    (OUT/'canon_source_corpus.md').write_text('\n'.join(corpus)+'\n')
    (OUT/'frontend_source_corpus.md').write_text('\n'.join(frontend)+'\n')
    print(json.dumps({'canon_files':len(rows), 'canon_corpus_lines':len(corpus), 'frontend_corpus_lines':len(frontend),
                      'output':str(OUT), 'app_head':snapshot['app_head']}, indent=2))

if __name__ == '__main__':
    main()