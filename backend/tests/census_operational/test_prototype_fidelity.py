"""Source-level fidelity gates; visual/journey checks are separate, mandatory F06 evidence."""
import hashlib
import json
from pathlib import Path

ROOT = Path('/app')
PROTOTYPES = ROOT / 'assessment_workspace/canon/prototypes/20260925_owner_updated'
GENERATED = ROOT / 'frontend/src/components/prototype/generated'


def test_f01_original_artifacts_unchanged():
    for artifact in json.loads((PROTOTYPES / 'intake.json').read_text())['files']:
        assert hashlib.sha256((PROTOTYPES / artifact['name']).read_bytes()).hexdigest() == artifact['sha256']


def test_f01_operational_templates_derived_from_originals():
    for name in ('os', 'dap'):
        compiled = json.loads((GENERATED / f'{name}.json').read_text())
        assert compiled['source_sha256'] == hashlib.sha256((PROTOTYPES / f'{name}.html').read_bytes()).hexdigest()
        assert compiled['nodes']
        assert compiled['method'] == 'HTMLParser: original markup, no prototype script execution'


def test_f02_dap_shell_anchors_retained():
    source = (GENERATED / 'dap.json').read_text()
    for anchor in ('dap-nav', 'dap-body', 'dap-rail', 'landFigures', 'composition', 'availBar', 'notesTitle', 'historyRows'):
        assert anchor in source


def test_f03_os_registry_anchors_retained():
    source = (GENERATED / 'os.json').read_text()
    for anchor in ('navGroupsView', 'landingStats', 'regTabsView', 'censusReadOpen', 'censusCareOpen',
                   'censusMixOpen', 'reg-notes', 'runCensus', 'openMeasured', 'measuredPageOpen'):
        assert anchor in source


def test_f03_replacement_dashboard_is_unrouted():
    app = (ROOT / 'frontend/src/App.js').read_text()
    assert 'element={<CensusWorkspace' not in app
    assert '@/pages/os/CensusOSPage' not in app


def test_f04_no_prototype_mock_script_execution():
    for name in ('os', 'dap'):
        model = json.loads((GENERATED / f'{name}.json').read_text())
        def walk(nodes):
            for node in nodes:
                if isinstance(node, dict):
                    assert node['tag'] not in ('script', 'iframe')
                    yield from walk(node.get('children', []))
        list(walk(model['nodes']))