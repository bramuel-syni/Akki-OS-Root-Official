"""Deterministic markup-only adoption. Original artifact bytes and prototype JS stay untouched."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import re

ROOT = Path('/app')
SOURCE = ROOT / 'assessment_workspace/canon/prototypes/20260925_owner_updated'
TARGET = ROOT / 'frontend/src/components/prototype/generated'
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


class Markup(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = {'tag': 'root', 'children': []}
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = {'tag': tag, 'attributes': dict(attrs), 'line': self.getpos()[0], 'children': []}
        self.stack[-1]['children'].append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i]['tag'] == tag:
                del self.stack[i:]
                break

    def handle_data(self, text):
        if text.strip():
            self.stack[-1]['children'].append(text)


def walk(nodes):
    for node in nodes:
        if isinstance(node, dict):
            yield node
            yield from walk(node['children'])


def clean(nodes):
    return [({**node, 'children': clean(node['children'])} if isinstance(node, dict) else node)
            for node in nodes if not isinstance(node, dict) or node['tag'] not in {'script', 'iframe', 'link'}]


def main():
    TARGET.mkdir(parents=True, exist_ok=True)
    receipts = []
    for name in ('os', 'dap'):
        original = (SOURCE / f'{name}.html').read_bytes()
        html = original.decode()
        match = re.search(r'<script type="__bundler/template">(.*?)</script>', html, re.S)
        template = json.loads(match.group(1))
        parser = Markup()
        parser.feed(template)
        root = next(n for n in walk(parser.root['children']) if n['tag'] == 'x-dc')
        nodes = clean(root['children'])
        payload = {'method': 'HTMLParser: original markup, no prototype script execution',
                   'source_sha256': hashlib.sha256(original).hexdigest(), 'nodes': nodes}
        target = TARGET / f'{name}.json'
        target.write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + '\n')
        expressions = sorted(set(re.findall(r'{{\s*(.*?)\s*}}', json.dumps(nodes))))
        (SOURCE / f'{name}_binding_inventory.json').write_text(json.dumps(expressions, indent=2) + '\n')
        receipts.append({'surface': name, 'source_sha256': payload['source_sha256'],
                         'generated_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
                         'nodes': len(list(walk(nodes))), 'bindings': len(expressions)})
    (SOURCE / 'markup_adoption_receipt.json').write_text(json.dumps(receipts, indent=2) + '\n')
    print(json.dumps(receipts, indent=2))


if __name__ == '__main__':
    main()