"""Real deterministic checks with explicitly SYNTHETIC metadata; no estate bytes."""
import copy
import json
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parents[2] / 'vendored/extraction_akki/backend'))
from services.non_gpu_governance.quality import QualityRegister, FAMILIES
from services.non_gpu_governance.context import ContextWindow
from services.non_gpu_governance.lineage import ancestors, descendants
from services.non_gpu_governance.memory import MemoryEvidence
from services.northena.execution_models import Held


def quality_dict():
    return {'version': 'akki.quality.metadata/1', 'snapshot_sha256': 'b'*64,
        'pack': {'version': 'v1', 'rules': [dict(rule_id=f, family=f, definition_sha256='c'*64,
            failure_stratum='Junk' if f == 'structural' else 'Suspect') for f in sorted(FAMILIES)],
            'media_applicable': False, 'media_rule_ids': []},
        'policy_receipt_ref': 'd'*64, 'population_receipt_ref': 'e'*64,
        'population_refs': ['akki://TEST/unit'], 'records': [{'unit_ref': 'akki://TEST/unit',
            'content_sha256': 'f'*64, 'checks': [dict(rule_id=f, outcome='pass', evidence_ref='akki://TEST/check/'+f)
            for f in sorted(FAMILIES)], 'stratum': 'Clean', 'provenance_known': True}],
        'counts': {'Clean': 1, 'Repairable': 0, 'Suspect': 0, 'Junk': 0}, 'accuracy': 'not_measured'}


def validate(value):
    return QualityRegister.model_validate_json(json.dumps(value))


def test_seven_family_population_reconstructs_without_accuracy_claim():
    value = validate(quality_dict())
    assert len(value.pack.rules) == 7 and sum(value.counts.values()) == 1
    assert value.accuracy == 'not_measured'


@pytest.mark.parametrize('family', sorted(FAMILIES))
def test_missing_family_or_bitmap_cannot_be_clean(family):
    value = quality_dict()
    value['pack']['rules'] = [r for r in value['pack']['rules'] if r['family'] != family]
    with pytest.raises(ValueError):
        validate(value)
    value = quality_dict()
    value['records'][0]['checks'] = [r for r in value['records'][0]['checks'] if r['rule_id'] != family]
    with pytest.raises(ValueError):
        validate(value)


@pytest.mark.parametrize('outcome', ['fail', 'not_assessed', 'flag'])
def test_nonpassing_outcome_cannot_claim_clean(outcome):
    value = quality_dict()
    value['records'][0]['checks'][0]['outcome'] = outcome
    with pytest.raises(ValueError):
        validate(value)


@pytest.mark.parametrize('defect', ['unknown_provenance', 'duplicate_record', 'missing_record', 'wrong_count', 'duplicate_check', 'zero_checks', 'media_missing', 'accuracy'])
def test_malformed_register_is_not_published(defect):
    value = quality_dict()
    if defect == 'unknown_provenance': value['records'][0]['provenance_known'] = False
    if defect == 'duplicate_record': value['records'].append(copy.deepcopy(value['records'][0]))
    if defect == 'missing_record': value['population_refs'].append('akki://TEST/absent')
    if defect == 'wrong_count': value['counts']['Clean'] = 2
    if defect == 'duplicate_check': value['records'][0]['checks'].append(copy.deepcopy(value['records'][0]['checks'][0]))
    if defect == 'zero_checks': value['pack']['rules'] = []
    if defect == 'media_missing': value['pack']['media_applicable'] = True
    if defect == 'accuracy': value['accuracy'] = '100%'
    with pytest.raises(ValueError): validate(value)


def context_dict():
    units = [{'unit_ref': 'akki://TEST/'+name, 'content_sha256': letter*64,
        'reextraction_ref': 'akki://TEST/reextract/'+name, 'class_label': cls,
        'tokens': size, 'proximity': 0, 'source_position': position}
        for name, letter, cls, size, position in [('a', 'a', 'fact', 5, 2), ('b', 'b', 'inference', 5, 1), ('c', 'c', 'fact', 8, 3)]]
    return dict(version='akki.context.metadata/1', objective_sha256='a'*64,
        frame_ref='akki://TEST/frame', model_sha256='b'*64, tokenizer_sha256='c'*64,
        ranking_rule_ref='d'*64, qualified_set_receipt_ref='e'*64, load_bearing_refs=['akki://TEST/b'],
        window_tokens=12, reserved_tokens=2, units=units,
        selected_refs=['akki://TEST/b', 'akki://TEST/a'],
        excluded_counts={'fact': 1, 'inference': 0, 'utterance': 0, 'non_factual': 0},
        top_excluded_handles=['akki://TEST/reextract/c'], loss_disclosed=True)


def test_window_reconstructs_whole_units_even_when_input_order_changes():
    value = context_dict()
    original = ContextWindow.model_validate_json(json.dumps(value))
    value['units'].reverse()
    reversed_window = ContextWindow.model_validate_json(json.dumps(value))
    assert original.selected_refs == reversed_window.selected_refs


@pytest.mark.parametrize('defect', ['reorder', 'undisclosed', 'lost_handle', 'counts', 'budget', 'duplicate', 'missing_frame_unit', 'empty'])
def test_window_rejects_unreproducible_selection_and_loss(defect):
    value = context_dict()
    if defect == 'reorder': value['selected_refs'].reverse()
    if defect == 'undisclosed': value['loss_disclosed'] = False
    if defect == 'lost_handle': value['top_excluded_handles'] = []
    if defect == 'counts': value['excluded_counts']['fact'] = 0
    if defect == 'budget': value['window_tokens'] = 2
    if defect == 'duplicate': value['units'].append(copy.deepcopy(value['units'][0]))
    if defect == 'missing_frame_unit': value['load_bearing_refs'].append('akki://TEST/missing')
    if defect == 'empty': value['selected_refs'] = []
    with pytest.raises(ValueError): ContextWindow.model_validate_json(json.dumps(value))


def test_transitive_withdrawal_finds_memory_report_and_model_without_mutation():
    graph = {'unit': ('source',), 'memory': ('unit',), 'report': ('memory', 'unit'), 'model': ('report',)}
    before = copy.deepcopy(graph)
    assert descendants('source', graph) == ('memory', 'model', 'report', 'unit')
    assert ancestors(('model',), graph) == {'source', 'unit', 'memory', 'report', 'model'}
    assert graph == before


def test_lineage_cycles_fail_without_recursive_overflow():
    with pytest.raises(Held, match='LINEAGE_CYCLE'):
        ancestors(('a',), {'a': ('b',), 'b': ('a',)})


def memory_dict():
    return dict(version='akki.memory.metadata/1', artifact_ref='akki://TEST/memory', artifact_sha256='a'*64,
        source_refs=['akki://TEST/unit'], source_hashes=['b'*64], principal_id='operator', run_id='closed-run',
        key='run-scoped-key', retention_policy_ref='c'*64, publication_receipt_ref='d'*64,
        class_label='inference', dropped_counts={'fact': 0}, summarised_counts={'inference': 1},
        context_only=True, hash_verified_on_reload=True, user_memory=False)


@pytest.mark.parametrize('defect', ['fact', 'user_memory', 'source_hashes', 'summarise_fact', 'evidence', 'hash'])
def test_memory_never_inflates_class_or_compacts_evidence(defect):
    value = memory_dict()
    if defect == 'fact': value['class_label'] = 'fact'
    if defect == 'user_memory': value['user_memory'] = True
    if defect == 'source_hashes': value['source_hashes'] = []
    if defect == 'summarise_fact': value['summarised_counts']['fact'] = 1
    if defect == 'evidence': value['context_only'] = False
    if defect == 'hash': value['hash_verified_on_reload'] = False
    with pytest.raises(ValueError): MemoryEvidence.model_validate_json(json.dumps(value))