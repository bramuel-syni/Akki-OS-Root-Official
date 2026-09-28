"""Extract owner source as data. No prototype/demo JavaScript is ever executed."""
from pathlib import Path
import hashlib
import json
import re
from compile_owner_prototypes import Markup, walk, clean
from inventory_owner_actions import inventory

ROOT = Path('/app')
SOURCE = ROOT / 'assessment_workspace/canon/prototypes/20260928_owner_nexus'


def main():
    raw = (SOURCE / 'nexus.html').read_bytes()
    match = re.search(r'<script type="__bundler/template">(.*?)</script>', raw.decode(), re.S)
    text = json.loads(match.group(1))
    (SOURCE / 'decoded.html').write_text(text)
    parser = Markup()
    parser.feed(text)
    component = next(n for n in walk(parser.root['children']) if n['tag'] == 'x-dc')
    nodes = clean(component['children'])
    payload = {'method': 'HTMLParser: original markup, no prototype script execution',
               'source_sha256': hashlib.sha256(raw).hexdigest(), 'nodes': nodes}
    (SOURCE / 'markup.json').write_text(json.dumps(payload, separators=(',', ':'), ensure_ascii=False) + '\n')
    scripts = re.findall(r'<script\b[^>]*type="text/x-dc"[^>]*>(.*?)</script>', text, re.S)
    for index, script in enumerate(scripts):
        (SOURCE / f'reference_model_{index}.js').write_text(script)
    actions = inventory(payload, 'nexus')
    (SOURCE / 'action_inventory.json').write_text(json.dumps(actions, indent=2))
    intake = {'source': 'nexus.html', 'sha256': payload['source_sha256'], 'byte_count': len(raw),
              'node_count': len(list(walk(nodes))), 'event_sites': len(actions),
              'reference_scripts': len(scripts), 'prototype_script_executed': False,
              'functional_completion_denominator': False}
    (SOURCE / 'intake.json').write_text(json.dumps(intake, indent=2) + '\n')
    all_nodes = list(walk(nodes))
    gates = {'work': 'isTasksActive', 'company': 'isMonPerformance', 'board': 'isBoard360',
             'mirror': 'isGreyMirror', 'mirrorRecord': 'gmIsFullRecord', 'watch': 'isWatchGroup', 'drawer': 'dwOpen',
             'registry':'isRegEstate', 'censusHistory':'measuredPageOpen', 'sourceCatalogue':'estateFullOpen',
             'connectDrawer':'connectOpen', 'modelFull':'mrFullOpen', 'sourceProfile':'efProfileOpen', 'modelDetail':'mrDetailDrawer', 'censusResponse':'censusPauseOpen', 'computeDetail':'loadOpen'}
    fragments = {key: next(n for n in all_nodes if n['tag'] == 'sc-if' and n['attributes'].get('value') == '{{ ' + gate + ' }}')
                 for key, gate in gates.items()}
    fragments['header'] = next(n for n in all_nodes if n['line'] == 31 and n['tag'] == 'div')
    fragments['headerActions'] = next(n for n in all_nodes if n['line'] == 36 and n['tag'] == 'div')
    fragments['pageHeader'] = next(n for n in all_nodes if n['line'] == 205 and n['tag'] == 'div')
    target = ROOT / 'frontend/src/components/prototype/generated/nexus-fragments.json'
    target.write_text(json.dumps({'source_sha256': payload['source_sha256'], 'fragments': fragments}, ensure_ascii=False, separators=(',', ':')) + '\n')
    print(json.dumps(intake, indent=2))


if __name__ == '__main__':
    main()