"""Mechanical original-source fidelity. Does not claim native feature completion."""
import hashlib
import json
from pathlib import Path
import pytest

ROOT=Path('/app')
SOURCE=ROOT/'assessment_workspace/canon/prototypes/20260928_owner_nexus'
EXPECTED='0330a1712aad3b76dfe6f5e97207707fa35a1ed774a134313635a59ba0a67d3d'


def walk(node):
    if isinstance(node,dict):
        yield node
        for child in node.get('children',[]):yield from walk(child)


def test_owner_attachment_is_preserved_without_runtime_execution():
    assert hashlib.sha256((SOURCE/'nexus.html').read_bytes()).hexdigest()==EXPECTED
    record=json.loads((SOURCE/'intake.json').read_text())
    assert record['prototype_script_executed'] is False
    assert record['node_count']==8649 and record['event_sites']==898
    assert record['functional_completion_denominator'] is False


@pytest.mark.parametrize('name',['work','company','board','mirror','mirrorRecord','watch','drawer','headerActions','pageHeader'])
def test_active_fragment_is_exact_original_subtree_not_a_replacement_shell(name):
    compiled=json.loads((ROOT/'frontend/src/components/prototype/generated/nexus-fragments.json').read_text())
    original=json.loads((SOURCE/'markup.json').read_text())
    fragment=compiled['fragments'][name]
    assert compiled['source_sha256']==EXPECTED
    assert any(node==fragment for root in original['nodes'] for node in walk(root))
    assert not any(node['tag'] in {'script','iframe'} for node in walk(fragment))


def test_custom_empty_feature_shells_are_removed():
    parent=(ROOT/'frontend/src/pages/os/OwnerOSPage.jsx').read_text()
    assert 'useNexusExperience' in parent and 'OSFeatureViews' not in parent
    assert not (ROOT/'frontend/src/components/prototype/OSFeatureViews.jsx').exists()