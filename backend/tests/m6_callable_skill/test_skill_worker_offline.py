"""Offline proof of the deterministic grounded-retrieval skill worker over a SYNTHETIC five-ring corpus in a temporary
shared-filesystem store: commission-time measurements (quality population → register → context window) validate under
the control plane's strict native models, the sealed answer is a subset of the corpus, every anchor is a whole unit present
in both, the inspector-side attestation and the worker's grounding receipt reproduce the exact digests `query_evidence`
verifies, and every receipt verifies under `SignedReceipt.signing_bytes` with the on-runtime key. No host, no network."""
import hashlib
import json
import time

import pytest

from services.activation.native_evidence import Observation
from services.activation.receipts import SignedReceipt
from services.extraction_runtime import skill_worker, worker_identity
from services.extraction_runtime.structured_records_worker import admit_limits, execute, unit_terms
from services.ledger_writer.mongo_control import digest
from services.non_gpu_governance.context import ContextWindow
from services.non_gpu_governance.quality import QualityRegister
from services.northena.execution_models import Artifact
from services.activation.model_proofs import Grounding
from services.watch.signature_primitive import watch_verify

TENANT = 'TEST-SYNTHETIC'
CORPUS_REF = f'akki://artifact/{TENANT}/req-synthetic/qualified-units'
QUERY_REF = f'akki://query/{TENANT}/skill-query-synthetic'
REQUEST_SHA = hashlib.sha256(b'synthetic-request').hexdigest()


def unit(i, topic):
    record = {'id': i, 'question': f'How does {topic} affect dairy output on farm {i}?', 'farmer_id': 100 + (i % 5)}
    return {'unit_id': f'u-{i}', 'record': record,
            'provenance': {'source_ref': 'source_synthetic', 'locator': {'database': 'db', 'table': 'questions', 'primary_key': 'id', 'key_value': str(i)}, 'context': topic},
            'signal': {'dimensions': {'completeness': 0.9, 'redaction_ratio': 0.0}},
            'relational': {'edges': [{'target_unit_ref': 'db.farmers.farmer_id'}]},
            'reextraction_handle': {'ref': f'akki://source/source_synthetic/{i}'}, 'defensibility': {'class': 'utterance'}}


@pytest.fixture(scope='module')
def world(tmp_path_factory):
    root = tmp_path_factory.mktemp('store')
    state = tmp_path_factory.mktemp('state')
    topics = ['milk yield', 'milk yield', 'feed cost', 'vaccination', 'milk yield', 'water access'] * 5
    body = b''.join(json.dumps(unit(i, t), sort_keys=True).encode() + b'\n' for i, t in enumerate(topics))
    key = 'akki/deliveries/req-synthetic/op/units.jsonl'
    (root / 'akki/deliveries/req-synthetic/op').mkdir(parents=True)
    (root / key).write_bytes(body)
    identity = worker_identity.ensure(str(state))
    corpus = {'ref': CORPUS_REF, 'sha256': hashlib.sha256(body).hexdigest(), 'size_bytes': len(body), 'tenant_id': TENANT, 'key': key}
    base = {'tenant_id': TENANT, 'request_id': 'skill-query-synthetic', 'request_sha256': REQUEST_SHA, 'fence': 1,
            'scope_refs': ['synthetic_scope'], 'state_dir': str(state), 'signer_id': 'runtime:synthetic', 'key_id': identity['key_id'],
            'runtime_id': 'synthetic', 'code_sha256': hashlib.sha256(b'bundle').hexdigest(), 'job_kind': 'skill.unit_retrieval',
            'secrets': {'object_store': {'provider': 'shared_filesystem', 'bucket': str(root), 'prefix': 'akki/deliveries/'}}}
    return {'corpus': corpus, 'base': base, 'public': bytes.fromhex(identity['public_key_hex']), 'body': body, 'root': root}


def verify(world, raw):
    receipt = SignedReceipt.model_validate_json(json.dumps(raw))
    assert watch_verify(world['public'], receipt.signing_bytes(), bytes.fromhex(receipt.signature_hex))
    assert receipt.request_sha256 == REQUEST_SHA and receipt.tenant_id == TENANT
    proof = Observation.model_validate_json(json.dumps(receipt.claims))
    assert proof.evidence_mode == 'measured' and proof.context_sha256 == REQUEST_SHA
    return receipt, proof


class TestCommissionMeasurements:
    def test_prepare_register_window_validate_under_the_native_models(self, world):
        control = {**world['base'], 'operation_key': 'skill-commission-synthetic', 'corpus': world['corpus']}
        prepared = execute({**control, 'mode': 'skill_prepare'})
        assert prepared['status'] == 'complete' and prepared['facts']['units_total'] == 30 and prepared['facts']['broken_lines'] == 0
        assert prepared['outcomes']['five_rings_present'] == 'pass' and prepared['outcomes']['cross_source_corroboration'] == 'not_assessed'
        _, population = verify(world, prepared['receipt'])
        assert population.category == 'quality_population'
        assert population.claim_sha256 == digest({'snapshot_sha256': prepared['snapshot_sha256'], 'population_refs': [CORPUS_REF]})
        pack = skill_worker.quality_pack('v0')
        policy_ref, population_ref = 'a' * 64, 'b' * 64
        registered = execute({**control, 'mode': 'skill_register', 'quality_pack': pack, 'policy_receipt_ref': policy_ref,
                              'population_receipt_ref': population_ref})
        assert registered['status'] == 'complete' and registered['stratum'] == 'Suspect'  # corroboration not assessed → honest ceiling
        _, quality = verify(world, registered['receipt'])
        register = QualityRegister.model_validate(quality.quality_register.model_dump())
        assert register.pack.version == 'v0' and register.counts == {'Clean': 0, 'Repairable': 0, 'Suspect': 1, 'Junk': 0}
        assert quality.claim_sha256 == digest(register.model_dump(mode='json'))
        ranking_ref, quality_ref = 'c' * 64, 'd' * 64
        windowed = execute({**control, 'mode': 'skill_window', 'ranking_rule_ref': ranking_ref, 'qualified_set_receipt_ref': quality_ref,
                            'objective_sha256': 'e' * 64})
        _, context = verify(world, windowed['receipt'])
        window = ContextWindow.model_validate(context.context_window.model_dump())
        assert window.selected_refs == (CORPUS_REF,) and window.loss_disclosed is False and window.units[0].tokens == 30
        committed = window.model_dump(mode='json', include={'frame_ref', 'model_sha256', 'tokenizer_sha256', 'load_bearing_refs',
                                                              'window_tokens', 'reserved_tokens'})
        assert committed == skill_worker.context_policy_committed(world['base']['code_sha256'], CORPUS_REF)
        assert context.claim_sha256 == digest(window.model_dump(mode='json'))

    def test_register_without_prepare_is_a_named_failure(self, world):
        value = execute({**world['base'], 'operation_key': 'skill-commission-never-prepared', 'mode': 'skill_register',
                         'quality_pack': skill_worker.quality_pack('v0'), 'policy_receipt_ref': 'a' * 64, 'population_receipt_ref': 'b' * 64})
        assert value['status'] == 'failed' and value['reason_code'] == 'SKILL_PREPARE_MISSING'


def envelope(key):
    now = int(time.time())
    return {'protocol': 'akki.runtime.limits/1', 'request_sha256': REQUEST_SHA, 'plan_ref': 'f' * 64, 'reservation_ref': '0' * 64,
            'runtime_id': 'synthetic', 'operation_key': key, 'fence': 1, 'starts_epoch': now - 5, 'stop_work_by_epoch': now + 500,
            'terminate_by_epoch': now + 560, 'limits': [
                {'dimension': 'spend', 'unit': 'USD', 'quantity': '0'}, {'dimension': 'wall_clock', 'unit': 'seconds', 'quantity': '600'},
                {'dimension': 'bytes_read', 'unit': 'bytes', 'quantity': '4000000'},
                {'dimension': 'returned_records', 'unit': 'records', 'quantity': '100'},
                {'dimension': 'active_compute', 'unit': 'cpu_seconds', 'quantity': '120'}]}


def submit(world, key, question, artifact='grounded-units'):
    control = {**world['base'], 'operation_key': key, 'corpus': world['corpus'], 'terms': sorted(unit_terms(question)),
               'intent_receipt_ref': '1' * 64, 'artifact_ref': f'akki://artifact/{TENANT}/skill-query-synthetic/{artifact}',
               'object_key': f'akki/deliveries/skill-query-synthetic/{key}/grounded-units.jsonl', 'parent_refs': [CORPUS_REF, QUERY_REF],
               'principal_id': 'p-synthetic'}
    assert admit_limits({**control, 'envelope': envelope(key)})['status'] == 'acknowledged'
    return control, execute({**control, 'mode': 'skill_submit'})


class TestGroundedExecution:
    def test_answer_is_whole_units_from_the_sealed_corpus_with_anchors_attested_independently(self, world):
        control, result = submit(world, 'op-milk', 'Which training questions mention milk yield?')
        assert result['state'] == 'complete' and result['reason_code'] == 'GROUNDED_UNITS_SEALED'
        retrieval = result['retrieval']
        assert retrieval['matched_total'] == 15 and retrieval['returned'] >= 15 and 'terms' not in retrieval
        answer = (world['root'] / control['object_key']).read_bytes()
        artifact = result['artifacts'][0]
        assert hashlib.sha256(answer).hexdigest() == artifact['sha256'] and len(answer) == artifact['size_bytes']
        corpus_lines = {l for l in world['body'].split(b'\n') if l.strip()}
        answer_lines = [l for l in answer.split(b'\n') if l.strip()]
        assert set(answer_lines) <= corpus_lines and len(answer_lines) == retrieval['returned']
        assert all(b'milk yield' in l for l in answer_lines[:15])
        anchors = retrieval['anchor_sha256s']
        assert 1 <= len(anchors) <= skill_worker.MAX_ANCHORS and all(a in {hashlib.sha256(l).hexdigest() for l in answer_lines} for a in anchors)
        _, measurements = verify(world, result['receipts']['measurements'])
        assert measurements.category == 'measurements' and measurements.terminal is True
        _, lineage = verify(world, result['receipts']['lineage'])
        assert lineage.lineage.parents == (CORPUS_REF, QUERY_REF) and lineage.lineage.artifact_sha256 == artifact['sha256']
        # same key → the sealed result is replayed, not recomputed
        again = execute({**control, 'mode': 'skill_submit'})
        assert again['worker_receipt_id'] == result['worker_receipt_id']
        # independent attestation of the anchors
        snapshot = skill_worker.snapshot_sha256(world['corpus'])
        attest = execute({**world['base'], 'operation_key': 'op-milk', 'mode': 'anchor', 'corpus': {'key': world['corpus']['key'], 'sha256': world['corpus']['sha256']},
                          'answer': {'key': control['object_key'], 'sha256': artifact['sha256']}, 'anchor_sha256s': anchors,
                          'snapshot_sha256': snapshot, 'query_ref': QUERY_REF})
        assert attest['verified'] is True and attest['answer_subset_of_corpus'] is True and len(attest['receipts']) == len(anchors)
        refs = {}
        for item in attest['receipts']:
            _, proof = verify(world, item['receipt'])
            assert proof.category == 'anchor'
            assert proof.claim_sha256 == digest({'snapshot_sha256': snapshot, 'anchor_sha256': item['anchor_sha256'],
                                                 'answer_sha256': artifact['sha256'], 'query_ref': QUERY_REF})
            refs[item['anchor_sha256']] = hashlib.sha256(json.dumps(item['receipt'], sort_keys=True).encode()).hexdigest()
        response = execute({**control, 'mode': 'skill_response', 'query_ref': QUERY_REF,
                            'anchors': [{'snapshot_sha256': snapshot, 'anchor_sha256': a, 'source_receipt_ref': refs[a]} for a in anchors]})
        assert response['status'] == 'complete'
        _, grounding = verify(world, response['receipt'])
        ground = Grounding.model_validate(grounding.grounding.model_dump())
        assert ground.answer_sha256 == artifact['sha256'] and ground.query_ref == QUERY_REF and len(ground.anchors) == len(anchors)
        assert grounding.claim_sha256 == digest({'request_sha256': REQUEST_SHA, 'artifact': Artifact.model_validate(artifact).model_dump(mode='json'),
                                                 'grounding': ground.model_dump(mode='json')})

    def test_tampered_anchor_set_is_refused_by_the_worker(self, world):
        control, result = submit(world, 'op-milk', 'Which training questions mention milk yield?')
        snapshot = skill_worker.snapshot_sha256(world['corpus'])
        bad = execute({**control, 'mode': 'skill_response', 'query_ref': QUERY_REF,
                       'anchors': [{'snapshot_sha256': snapshot, 'anchor_sha256': 'f' * 64, 'source_receipt_ref': '2' * 64}]})
        assert bad['status'] == 'failed' and bad['reason_code'] == 'ANCHOR_SET_MISMATCH'

    def test_inspector_refuses_an_anchor_that_is_not_in_the_answer(self, world):
        control, result = submit(world, 'op-milk', 'Which training questions mention milk yield?')
        answer = (world['root'] / control['object_key']).read_bytes()
        in_answer = {hashlib.sha256(l).hexdigest() for l in answer.split(b'\n') if l.strip()}
        foreign = next((hashlib.sha256(l).hexdigest() for l in world['body'].split(b'\n') if l.strip() and hashlib.sha256(l).hexdigest() not in in_answer),
                       hashlib.sha256(json.dumps(unit(99, 'feed cost'), sort_keys=True).encode()).hexdigest())  # a unit outside the answer (and, when the answer spans the corpus, outside the corpus)
        attest = execute({**world['base'], 'operation_key': 'op-milk', 'mode': 'anchor', 'corpus': {'key': world['corpus']['key'], 'sha256': world['corpus']['sha256']},
                          'answer': {'key': control['object_key'], 'sha256': result['artifacts'][0]['sha256']}, 'anchor_sha256s': [foreign],
                          'snapshot_sha256': skill_worker.snapshot_sha256(world['corpus']), 'query_ref': QUERY_REF})
        assert attest['verified'] is False and attest['receipts'] == []

    def test_out_of_scope_question_is_a_receipted_refusal_not_an_answer(self, world):
        control, result = submit(world, 'op-quantum', 'Explain quantum chromodynamics lattices', artifact='never')
        assert result['state'] == 'failed' and result['reason_code'] == 'OUT_OF_SCOPE' and result['artifacts'] == []
        _, refusal = verify(world, result['receipts']['refusal'])
        assert refusal.refusal.reason_code == 'OUT_OF_SCOPE' and refusal.refusal.request_ref == '1' * 64
        assert refusal.claim_sha256 == digest(refusal.refusal.model_dump(mode='json'))
        assert not (world['root'] / control['object_key']).exists()

    def test_digest_mismatch_against_the_sealed_corpus_fails_closed(self, world):
        control = {**world['base'], 'operation_key': 'op-tamper', 'corpus': {**world['corpus'], 'sha256': '9' * 64},
                   'terms': ['milk'], 'intent_receipt_ref': '1' * 64, 'artifact_ref': f'akki://artifact/{TENANT}/x/y',
                   'object_key': 'akki/deliveries/x/op-tamper/grounded-units.jsonl', 'parent_refs': [CORPUS_REF, QUERY_REF], 'principal_id': 'p'}
        assert admit_limits({**control, 'envelope': envelope('op-tamper')})['status'] == 'acknowledged'
        result = execute({**control, 'mode': 'skill_submit'})
        assert result['state'] == 'failed' and result['reason_code'] == 'ARTIFACT_DIGEST_MISMATCH'
