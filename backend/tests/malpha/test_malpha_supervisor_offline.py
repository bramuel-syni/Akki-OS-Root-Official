"""Mα training supervisor (offline, scratch DB): Solva reading over the sealed faculties, CIF acceptance point, selection, hypothesis tests, absorption → refusal envelope, coach seat."""
import os
import sys

import pytest
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv('/app/backend/.env')
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')

from services.training_lab import malpha_supervisor as sup  # noqa: E402
from services.cif import output_routing  # noqa: E402


def _listener_job(job_id, iteration, kam_recall, kam_precision=0.85, recipe=None):
    dev = {'mentions': {'kik': {'precision': 0.94, 'recall': 0.58}, 'kam': {'precision': kam_precision, 'recall': kam_recall}, 'swa': {'precision': 0.66, 'recall': 0.78}},
           'words': {l: {'wer': 0.5} for l in ('kik', 'kam', 'swa')}}
    return {'job_id': job_id, 'lane': 'listener', 'commission_id': 'LISTEN-KIK-KAM-SWA', 'iteration': iteration, 'status': 'completed', 'result': {'dev': dev, 'recipe': recipe or {'base': 'openai/whisper-large-v3-turbo', 'lr': 3e-5}}}


LADDER = {'base': 'openai/whisper-large-v3-turbo', 'lr': 3e-5, 'max_steps': 8000, 'batch_size': 16, 'grad_accum': 4, 'init_from': '/host/artefact', 'contextual_bias': True, 'rationale': 'continue from the artefact for 8000 steps'}


@pytest.fixture
def scratch(monkeypatch):
    client = MongoClient(os.environ['MONGO_URL']); name = os.environ['DB_NAME'] + '_pytest_supervisor'
    client.drop_database(name); database = client[name]
    monkeypatch.setattr(sup, 'db', lambda: database)
    events = []
    monkeypatch.setattr(sup.wpw, 'record_event', lambda run_id, kind, cls, ref, payload=None: events.append({'run_id': run_id, 'kind': kind, 'class': cls, 'ref': ref, 'payload': payload}) or 'sha')
    monkeypatch.setattr(sup, '_schedule_naivety_pass', lambda lane, hyp, finding: events.append({'kind': 'naivety_pass_scheduled', 'lane': lane}))
    output_routing._reset_research_loop_sink_for_tests()
    yield database, events
    client.drop_database(name)


def test_gap_reads_load_bearing_units_at_utterance_class(scratch):
    g = sup.gap('listener', [_listener_job('m9j-aaaaaaaaaaa1', 1, kam_recall=0.46)])
    assert g['worst_language'] == 'kam' and g['target_field'] == 'recall' and g['direction'] == 'up'
    assert g['class'] == 'utterance' and 'was stated' in g['conclusion'] and 'kam' in g['conclusion']
    assert set(g['load_bearing']) == {'m9j-aaaaaaaaaaa1#dev.precision.kam', 'm9j-aaaaaaaaaaa1#dev.recall.kam'}
    assert len(g['tensions']) == 1  # precision vs recall for the worst language
    assert g['shortfall']['kam']['recall'] == pytest.approx(0.44)
    assert sup.gap('listener', [])['class'] == 'non_factual'


def test_acceptance_point_is_deterministic_and_floors_are_read_only(scratch):
    base = {'hypothesis_id': 'hyp-test00000001', 'lane': 'listener', 'origin': 'owner', 'correction_class': 'owner:x', 'statement': 'lower the lr', 'citations': ['owner://coach-seat/t'], 'created_at': sup.now()}
    assert sup.accept({**base, 'recipe_delta': {'lr': 1e-5}}, route=False)['accepted'] is True
    refused = sup.accept({**base, 'recipe_delta': {'identity_cosine_threshold': 0.6}}, route=False)
    assert not refused['accepted'] and 'protected' in refused['reasons'][0]
    assert not sup.accept({**base, 'recipe_delta': {'lr': 5.0}}, route=False)['accepted']
    assert not sup.accept({**base, 'recipe_delta': {'conditioning_dropout': 0.1}}, route=False)['accepted']
    assert not sup.accept({**base, 'recipe_delta': {'lr': 1e-5}, 'citations': []}, route=False)['accepted']
    routed = sup.accept({**base, 'recipe_delta': {'lr': 1e-5}})
    assert routed['routed'] == 'research_loop_appended' and routed['proposal_id'] == 'cif_hyp_test00000001'
    assert len(output_routing.get_research_loop_items()) == 1


def test_select_adopts_measurement_rule_and_records_trace(scratch):
    database, events = scratch
    history = [_listener_job('m9j-aaaaaaaaaaa1', 1, kam_recall=0.46)]
    chosen = sup.select('LISTEN-KIK-KAM-SWA', 'listener', 2, history, LADDER)
    assert chosen['recipe'] == LADDER  # without a competing bound idea the measurement rule runs unchanged
    hyp = chosen['hypothesis']
    assert hyp['origin'] == 'measurement_rule' and hyp['archive_state'] == 'adopted' and hyp['correction_class'] == 'continue_from_artefact'
    assert hyp['prediction'] == {'field': 'recall', 'language': 'kam', 'direction': 'up', 'min_delta': 0.02} and hyp['baseline']['value'] == 0.46
    assert all(k in hyp['manifest'][0] for k in ('assumption', 'class', 'flips_if'))
    assert 'reflection:HALTED' in ' '.join(chosen['trace']['reasoning_path']) and chosen['trace']['au_3b_defensible'] is False
    cycle = database.malpha_supervisor_cycles.find_one({'lane': 'listener'})
    assert cycle['outcome'] == 'adopted' and cycle['intent_audit']['declared_situation_class'] == sup.DECLARED_SITUATION
    sup.bind_job(hyp['hypothesis_id'], 'm9j-bbbbbbbbbbb2')
    assert database.malpha_hypotheses.find_one({'job_id': 'm9j-bbbbbbbbbbb2'})['test']['verdict'] == 'pending'


def test_frontier_idea_with_bounded_delta_outranks_ladder_and_unbound_ideas_wait(scratch):
    database, events = scratch
    database.malpha_learning_reviews.insert_one({'review_id': 'r1', 'status': 'reviewed', 'review': {'verdict': 'accept', 'required_changes': []}, 'proposal': {'experiments': [
        {'lane': 'listener', 'hypothesis': 'balanced mention oversampling lifts kam recall', 'evidence_refs': ['listener-result-1'], 'change': 'oversample', 'measurement': 'kam recall', 'failure_condition': 'recall flat', 'recipe_delta': {'bias_prob': 0.8, 'lr': 2e-5}},
        {'lane': 'listener', 'hypothesis': 'audit the labels', 'evidence_refs': ['listener-result-1'], 'change': 'label audit', 'measurement': 'agreement', 'failure_condition': 'n/a'},
        {'lane': 'story_voice', 'hypothesis': 'other lane', 'evidence_refs': ['story_voice-result-1'], 'change': 'x', 'measurement': 'y', 'failure_condition': 'z', 'recipe_delta': {'identity_noise': 0.9}}]}})
    chosen = sup.select('LISTEN-KIK-KAM-SWA', 'listener', 2, [_listener_job('m9j-aaaaaaaaaaa1', 1, kam_recall=0.46)], LADDER)
    assert chosen['hypothesis']['origin'] == 'frontier_cif' and chosen['recipe']['bias_prob'] == 0.8 and chosen['recipe']['lr'] == 2e-5 and chosen['recipe']['max_steps'] == 8000
    assert 'supervisor adopted' in chosen['recipe']['rationale']
    rows = {r['origin']: r for r in database.malpha_hypotheses.find({'lane': 'listener'})}
    assert rows['measurement_rule']['archive_state'] == 'not_yet_conditioned' and rows['measurement_rule']['missing_condition'] == sup.FREE_DEVICE and rows['measurement_rule']['watch']['bindable']
    unbound = database.malpha_hypotheses.find_one({'statement': 'audit the labels'})
    assert unbound['archive_state'] == 'not_yet_conditioned' and 'engineering binding' in unbound['missing_condition'] and unbound['watch']['bindable'] is False and unbound['review_by']
    assert not database.malpha_hypotheses.find_one({'lane': 'story_voice'})  # other lanes untouched by this cycle


def test_hypothesis_test_absorption_refusal_envelope_and_owner_release(scratch):
    database, events = scratch
    history = [_listener_job('m9j-aaaaaaaaaaa1', 1, kam_recall=0.46)]
    for n, (job, recall) in enumerate([('m9j-ccccccccccc1', 0.47), ('m9j-ccccccccccc2', 0.45)], start=2):
        chosen = sup.select('LISTEN-KIK-KAM-SWA', 'listener', n, history, LADDER)
        assert chosen, f'iteration {n} should still be admissible'
        sup.bind_job(chosen['hypothesis']['hypothesis_id'], job)
        out = sup.on_settled(_listener_job(job, n, kam_recall=recall))
        assert out['test']['verdict'] == 'refuted' and out['test']['before'] == 0.46
        history = history + [_listener_job(job, n, kam_recall=recall)]
        history[-1]['result']['dev']['mentions']['kam']['recall'] = 0.46  # the gap stays where it was for the next baseline
    assert out['finding'] and out['finding']['signature'] == 'absorption' and any(e['kind'] == 'naivety_pass_scheduled' for e in events)
    assert database.malpha_supervisor_findings.count_documents({}) == 1
    held = sup.select('LISTEN-KIK-KAM-SWA', 'listener', 4, history, LADDER)
    assert held is None
    cycle = database.malpha_supervisor_cycles.find_one({'lane': 'listener', 'outcome': 'refused'})
    assert cycle['refusal_envelope']['actions_offered'] == ['narrow_objective'] and 'lower_standard' not in cycle['refusal_envelope']['actions_offered']
    assert 'never relaxes' in cycle['refusal_envelope']['lower_standard_not_offered']
    assert any(e['kind'] == 'anomaly' and 'refusal envelope' in e['payload']['what'] for e in events)
    # supported test path
    owner = sup.originate('owner-1', 'listener', 'halve the learning rate and widen the brand expectation list', {'lr': 1.5e-5, 'bias_terms_per_language': 80})
    assert owner['archive_state'] == 'unverified_provisional' and owner['acceptance']['accepted']
    chosen = sup.select('LISTEN-KIK-KAM-SWA', 'listener', 4, history, LADDER)
    assert chosen['hypothesis']['hypothesis_id'] == owner['hypothesis_id'] and chosen['recipe']['lr'] == 1.5e-5
    sup.bind_job(owner['hypothesis_id'], 'm9j-ddddddddddd1')
    out = sup.on_settled(_listener_job('m9j-ddddddddddd1', 4, kam_recall=0.61))
    assert out['test']['verdict'] == 'supported' and out['test']['movement'] == pytest.approx(0.15) and out['finding'] is None
    assert any(e['kind'] == 'cif_ideation' and e['class'] == 'measured' and e['payload']['adoption_status'] == 'adopted; tested: supported' for e in events)
    assert any(e['kind'] == 'human_contribution' and set(e['payload']) >= {'actor', 'state_before', 'change', 'movement_after'} for e in events)


def test_coach_seat_verdicts_and_binding(scratch):
    database, events = scratch
    refused = sup.originate('owner-1', 'story_voice', 'relax the identity gate', {'identity_cosine_threshold': 0.6})
    assert refused['archive_state'] == 'not_yet_conditioned' and 'protected' in refused['missing_condition']
    database.malpha_learning_reviews.insert_one({'review_id': 'r2', 'status': 'reviewed', 'review': {'verdict': 'revise', 'required_changes': ['list the conditioning speakers']}, 'proposal': {'experiments': [
        {'lane': 'story_voice', 'hypothesis': 'more identity noise clears the gate', 'evidence_refs': ['story_voice-result-1'], 'change': 'noise up', 'measurement': 'max cosine', 'failure_condition': 'cosine flat'}]}})
    voice_history = [{'job_id': 'm9j-eeeeeeeeeee1', 'lane': 'story_voice', 'iteration': 1, 'status': 'completed', 'result': {'dev': {'per_language': {l: {'behaviour': {'overall_similarity': 0.5}, 'identity_gate': {'max_cosine_to_any_corpus_speaker': 0.57}} for l in ('kik', 'kam', 'swa')}}, 'recipe': {'identity_conditioning': True, 'identity_noise': 0.5}}}]
    ladder = {'lr': 2e-4, 'identity_noise': 0.75, 'identity_conditioning': True, 'init_from': '/x', 'rationale': 'resample'}
    chosen = sup.select('STORY-KIK-KAM-SWA', 'story_voice', 2, voice_history, ladder)
    assert chosen['hypothesis']['origin'] == 'measurement_rule' and chosen['hypothesis']['prediction']['field'] == 'max_cosine' and chosen['hypothesis']['prediction']['direction'] == 'down'
    frontier = database.malpha_hypotheses.find_one({'origin': 'frontier_cif', 'lane': 'story_voice'})
    assert 'required_changes' in frontier['missing_condition'] and 'engineering binding' in frontier['missing_condition']
    with pytest.raises(ValueError): sup.verdict('owner-1', frontier['hypothesis_id'], 'defer', 'later')  # a deferral must name its condition
    bound = sup.bind('eng-1', frontier['hypothesis_id'], {'identity_noise': 1.2})
    assert bound['archive_state'] == 'not_yet_conditioned'  # the reviewer's revise verdict still conditions it
    adopted = sup.verdict('owner-1', frontier['hypothesis_id'], 'adopt', 'the coach ratifies the idea despite the revise verdict')
    assert adopted['archive_state'] == 'unverified_provisional' and adopted['owner_verdict'] == 'adopt'
    rejected = sup.verdict('owner-1', refused['hypothesis_id'], 'reject', 'not a lawful change')
    assert rejected['archive_state'] == 'superseded'
    sup.bind_job(chosen['hypothesis']['hypothesis_id'], 'm9j-fffffffffff1')
    with pytest.raises(ValueError): sup.verdict('owner-1', chosen['hypothesis']['hypothesis_id'], 'reject', 'too late')  # a dispatched idea keeps its record
    summary_lane = sup.ledger('story_voice')
    assert {h['archive_state'] for h in summary_lane['hypotheses']} >= {'adopted', 'unverified_provisional', 'superseded'}
