"""Extract unchanged owner markup for agent-built routes; never execute demo scripts."""
import hashlib
import json
import re
from pathlib import Path
from compile_owner_prototypes import Markup, clean, walk

ROOT = Path(__file__).resolve().parents[2]
source = ROOT / 'frontend/public/prototype/v2_os.html'
raw = source.read_bytes()
html = json.loads(re.search(r'<script type="__bundler/template">(.*?)</script>', raw.decode(), re.S).group(1))
parser = Markup()
parser.feed(html)
nodes = list(walk(clean(parser.root['children'])))
at = lambda line: next(n for n in nodes if n['line'] == line)
section = lambda name: next(n for n in nodes if n['attributes'].get('value') == '{{ ' + name + ' }}' and n['line'] > 200)
shell = {**at(29), 'children': [at(31), {**at(42), 'children': [{**at(96), 'children': []}]}]}
payload = {'source_sha256': hashlib.sha256(raw).hexdigest(), 'source': 'frontend/public/prototype/v2_os.html',
           'shell': {'nodes': [shell]}, 'header': {'nodes': [at(165), at(195)]},
           **{name: {'nodes': [section(flag)]} for name, flag in [('chat', 'isChatActive'), ('documents', 'isDocumentsActive'), ('approvals', 'isApprovalsGroup')]}}
target = ROOT / 'frontend/src/components/prototype/generated/owner-workspaces.json'
target.write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + '\n')
print('Extracted unchanged workspace markup. Source SHA256:', payload['source_sha256'])