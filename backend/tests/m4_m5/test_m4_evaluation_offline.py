"""M4 offline proofs on SYNTHETIC units — no model call, no estate bytes, no SSH, no Mongo write.

1. Subject-match rule `chat.subject_match.v1`: a single shared generic word does not make an unrelated question
   warm; naming the region or sharing two terms does; short questions keep their one-term match.
2. Stale/withdrawn support: a rights revocation removes the unit from the active set, so the artefact disappears
   from the answerer's view and the previously-warm question can no longer be answered from it.
3. Severe context reduction: when no whole unit fits the budget the window is refused whole, never split.
4. Evaluation accounting: every task lands in exactly one bucket; grading reasons are explicit.
"""
import hashlib
import json
import sys

import pytest

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')

from services.chat import decision, evaluation, spine, window as windowing  # noqa: E402

TENANT, REQUEST = 'tenant-SYNTHETIC-m4', 'req-synthetic-m4'


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def candidate(i, *, overlap, kind='matched', words=12, region='digicow_live.training_questions'):
    body = ' '.join(f'w{i}_{k}' for k in range(words))
    unit = {'unit_id': f'unit-{i:04d}', 'record': {'id': i, 'question': body},
            'provenance': {'locator': {'database': region.split('.')[0], 'table': region.split('.')[1], 'primary_key': 'id', 'key_value': str(i)}},
            'defensibility': {'defensibility_class': 'utterance'}}
    return {'ref': f'akki://unit/{TENANT}/{REQUEST}/unit-{i:04d}', 'unit_id': unit['unit_id'], 'unit': unit, 'position': i, 'overlap': overlap,
            'kind': kind, 'rel_keys': [], 'content_sha256': sha(json.dumps(unit, sort_keys=True)), 'region': region,
            'artifact_ref': f'akki://artifact/{TENANT}/{REQUEST}/qualified-units', 'request_id': REQUEST, 'class_label': 'utterance',
            'reextraction_ref': f'akki://reextract/{TENANT}/{REQUEST}/unit-{i:04d}'}


ARTEFACTS = [{'region': 'digicow_live.training_questions', 'columns': ['id', 'question', 'answer', 'created_at']}]


class TestSubjectRule:
    def test_one_shared_generic_word_is_set_aside(self):
        result = decision.subject_match(['best', 'laptop', 'price', 'used'], [candidate(1, overlap=1)], ARTEFACTS)
        assert result['on_subject'] is False and result['weak_regions'] == ['digicow_live.training_questions']
        assert result['rule'] == 'chat.subject_match.v1' and result['best_overlap'] == 1 and result['matched_units'] == 1

    def test_naming_the_region_or_a_column_is_on_subject(self):
        result = decision.subject_match(['training', 'questions', 'minerals', 'feeding'], [candidate(1, overlap=1)], ARTEFACTS)
        assert result['on_subject'] is True and result['regions_named_by_question'] == ['digicow_live.training_questions'] and result['weak_regions'] == []

    def test_two_shared_terms_are_on_subject(self):
        result = decision.subject_match(['milk', 'yield', 'calf', 'feed'], [candidate(1, overlap=2)], ARTEFACTS)
        assert result['on_subject'] is True and result['basis'].startswith('best unit shares 2')

    def test_short_question_keeps_its_single_match(self):
        assert decision.subject_match(['minerals', 'cost'], [candidate(1, overlap=1)], ARTEFACTS)['on_subject'] is True

    def test_no_match_is_not_on_subject(self):
        result = decision.subject_match(['weather', 'paris'], [candidate(1, overlap=0, kind='neighbour')], ARTEFACTS)
        assert result['on_subject'] is False and result['matched_units'] == 0 and result['weak_regions'] == []


def rights_event(ref, status, row_hash):
    return {'row': {'hash': row_hash}, 'payload': {'receipt': {'kind': 'observation', 'claims': {'category': 'rights', 'rights': {'unit_ref': ref, 'status': status}}}}}


def revocation_event(target_hash):
    return {'row': {'hash': 'rev-' + target_hash}, 'payload': {'receipt': {'kind': 'revocation', 'claims': {'target_ref': target_hash}}}}


class TestWithdrawnSupport:
    def test_revocation_removes_the_unit_from_the_active_set(self):
        ref = f'akki://artifact/{TENANT}/{REQUEST}/qualified-units'
        active = spine._active_rights([rights_event(ref, 'active', 'h1')])
        assert active == {ref: 'h1'}
        assert spine._active_rights([rights_event(ref, 'active', 'h1'), revocation_event('h1')]) == {}

    def test_later_withdrawal_status_wins_over_earlier_grant(self):
        ref = f'akki://artifact/{TENANT}/{REQUEST}/qualified-units'
        assert spine._active_rights([rights_event(ref, 'active', 'h1'), rights_event(ref, 'withdrawn', 'h2')]) == {}

    def test_unrelated_revocation_leaves_the_right_standing(self):
        ref = f'akki://artifact/{TENANT}/{REQUEST}/qualified-units'
        assert spine._active_rights([rights_event(ref, 'active', 'h1'), revocation_event('other')]) == {ref: 'h1'}


class TestSevereContextReduction:
    def test_no_whole_unit_fits_refuses_whole(self):
        candidates = [candidate(i, overlap=2, words=400) for i in range(3)]
        with pytest.raises(ValueError):
            windowing.build(objective_text='o', frame_ref='akki://chat/session/s', model='m', qualified_set_receipt_ref=sha('q'), candidates=candidates,
                            reserved_tokens=windowing.WINDOW_TOKENS - 20)

    def test_heavy_reduction_keeps_whole_units_and_discloses_loss(self):
        candidates = [candidate(i, overlap=3 - (i % 3), words=40) for i in range(40)]
        window, selected, excluded = windowing.build(objective_text='o', frame_ref='akki://chat/session/s', model='m', qualified_set_receipt_ref=sha('q'),
                                                     candidates=candidates, reserved_tokens=windowing.WINDOW_TOKENS - 600)
        assert selected and excluded and sum(c['tokens'] for c in selected) <= 600
        assert window.loss_disclosed is True and sum(window.excluded_counts.values()) == len(excluded)
        assert all(c['text'] == windowing.render_unit(c) for c in selected)


def turn(decision_, *, refused=False, sufficient=None, grounding=None, cited=(), selected=(), draft=None, weak=(), unsupported=''):
    return {'turn_id': 't', 'decision': decision_, 'refused': refused, 'refusal_reason': 'r' if refused else '', 'sufficient': sufficient,
            'decision_detail': {'ledger_row_id': 'led-x', 'draft': draft, 'subject_match': {'weak_regions': list(weak)}},
            'evidence': {'cited_refs': list(cited), 'grounding': {'grounding': grounding, 'unsupported': unsupported} if grounding else {},
                         'window': {'selected': list(selected)}, 'reads': {'source_dispatches': 0, 'source_rows_read': 0, 'qualified_store_calls': 1, 'candidates_returned': len(selected)},
                         'memory': {'hits': 1, 'misses': 2}},
            'latency_ms_total': 1200, 'tokens_in': 100, 'tokens_out': 20}


class TestEvaluationGrading:
    def test_task_mix_is_deterministic_and_bounded(self):
        pool = [{'ref': f'r{i}', 'content_sha256': f's{i}', 'region': 'db.t', 'text': 'a long enough farmer question ' + str(i), 'pk': 'id', 'key': str(i)} for i in range(30)]
        slices = [{'database': 'db', 'table': f't{i}', 'columns': ['a', 'b', 'c'], 'row_count': 10} for i in range(20)]
        a, b = evaluation.build_tasks(200, 7, pool, slices), evaluation.build_tasks(200, 7, pool, slices)
        assert [t['question'] for t in a] == [t['question'] for t in b] and len(a) == 200
        classes = {c: sum(1 for t in a if t['class'] == c) for c in ('reference', 'unanswerable', 'out_of_scope', 'weak_match', 'fresh')}
        assert classes['fresh'] == evaluation.MAX_FRESH and classes['out_of_scope'] == 30 and classes['weak_match'] == 20 and classes['unanswerable'] == 30
        assert classes['reference'] == 200 - 30 - 30 - 20 - evaluation.MAX_FRESH and len({t['task_id'] for t in a}) == 200

    def test_reference_grading_requires_the_exact_unit_to_be_cited(self):
        task = {'class': 'reference', 'reference_sha256': 'abc'}
        selected = [{'ref': 'u1', 'content_sha256': 'abc'}, {'ref': 'u2', 'content_sha256': 'zzz'}]
        assert evaluation.grade(task, turn('warm', sufficient=True, grounding='cited_in_window', cited=['u1'], selected=selected))[0] is True
        passed, reason, extra = evaluation.grade(task, turn('warm', sufficient=True, grounding='cited_in_window', cited=['u2'], selected=selected))
        assert passed is False and reason == 'reference in window but not cited' and extra['reference_in_window'] is True
        assert evaluation.grade(task, turn('warm', sufficient=True, grounding='cited_in_window', cited=['u2'], selected=selected[1:]))[1] == 'reference not retrieved into the window'
        assert evaluation.grade(task, turn('refused', refused=True))[0] is False

    def test_unanswerable_fails_only_when_invented_as_sufficient(self):
        task = {'class': 'unanswerable'}
        assert evaluation.grade(task, turn('warm', sufficient=False, grounding='cited_in_window'))[0] is True
        assert evaluation.grade(task, turn('warm', sufficient=True, grounding='cited_in_window', unsupported='no figure'))[0] is True
        assert evaluation.grade(task, turn('warm', sufficient=True, grounding='cited_in_window'))[0] is False
        assert evaluation.grade(task, turn('refused', refused=True))[0] is True

    def test_off_subject_and_fresh_grading(self):
        assert evaluation.grade({'class': 'weak_match'}, turn('refused', refused=True, weak=['db.t']))[1] == 'refused; 1 loose region(s) set aside'
        assert evaluation.grade({'class': 'out_of_scope'}, turn('warm', sufficient=True, grounding='cited_in_window'))[0] is False
        assert evaluation.grade({'class': 'fresh'}, turn('fresh', draft={'draft_id': 'd1'}))[0] is True
        assert evaluation.grade({'class': 'fresh'}, turn('refused', refused=True))[0] is False

    def test_every_task_lands_in_exactly_one_bucket(self):
        rows = [evaluation._row({'class': 'reference', 'reference_sha256': 'abc', 'task_id': 't1'}, turn('warm', sufficient=True, grounding='cited_in_window', cited=['u1'], selected=[{'ref': 'u1', 'content_sha256': 'abc'}]), 'now'),
                evaluation._row({'class': 'reference', 'reference_sha256': 'abc', 'task_id': 't2'}, turn('warm', sufficient=False, grounding='partially_cited'), 'now'),
                evaluation._row({'class': 'out_of_scope', 'task_id': 't3'}, turn('refused', refused=True), 'now'),
                evaluation._row({'class': 'fresh', 'task_id': 't4'}, turn('fresh', draft={'draft_id': 'd'}), 'now'),
                {'class': 'reference', 'task_id': 't5', 'outcome': 'timeout', 'passed': False},
                {'class': 'reference', 'task_id': 't6', 'outcome': 'error', 'passed': False},
                {'class': 'reference', 'task_id': 't7', 'outcome': 'held', 'passed': False}]
        summary = evaluation.summarize(rows)
        assert summary['accounted'] is True and summary['tasks'] == 7
        assert summary['buckets'] == {'answered': 1, 'narrow': 1, 'refused': 1, 'fresh': 1, 'held': 1, 'timeout': 1, 'error': 1}
        assert summary['paths'] == {'warm': 2, 'fresh_or_refused': 2} and summary['source_dispatches'] == 0
        assert summary['reference_hit_rate'] == 0.5 and summary['latency_ms']['p50'] == 1200 and summary['memory']['hit_ratio'] == 0.3333


class TestFreshSliceRule:
    ROW = {'database': 'digicow_live', 'table': 'cooperative_farmer', 'columns': ['id', 'cooperative_id', 'city', 'name'], 'row_count': 10}

    def test_one_column_word_is_not_a_subject(self):
        assert decision._table_score(self.ROW, ['capital', 'city', 'mongolia']) == (0, False)

    def test_two_column_words_are_a_subject_without_naming_the_table(self):
        assert decision._table_score(self.ROW, ['city', 'name', 'list']) == (2, False)

    def test_naming_the_table_outranks_columns(self):
        score, named = decision._table_score(self.ROW, ['cooperative_farmer', 'table', 'hold'])
        assert named is True and score >= 2
        assert decision._table_score(self.ROW, ['cooperative', 'farmer'])[1] is True

    def test_one_word_of_a_split_table_name_is_not_naming_it(self):
        home = {'database': 'digicow_live', 'table': 'home_consumption', 'columns': ['id', 'litres'], 'row_count': 5}
        assert decision._table_score(home, ['bake', 'sourdough', 'bread', 'home']) == (0, False)
        assert decision._table_score(home, ['home', 'consumption'])[1] is True
