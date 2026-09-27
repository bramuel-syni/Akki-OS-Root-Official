"""Positive/negative native metadata joins use signed SYNTHETIC lab evidence."""
import asyncio
import json
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parents[1] / 'activation_controls'))
sys.path.insert(0, str(Path(__file__).parents[1] / 'portal_operational'))
import test_native_control_ledger as helpers
from test_governance_metadata import quality_dict
from test_native_governance_gates import observation
from services.activation.record_shapes import Plan
from services.activation.native_evidence import Observation
from services.non_gpu_governance.gate import NativeGovernance
from services.non_gpu_governance.quality import QualityPack, QualityRegister
from services.non_gpu_governance.context import ContextWindow
from services.non_gpu_governance.lineage import Rights
from services.northena.execution_journal import LedgerJournal
from services.northena.execution_models import Request, Held
from services.ledger_writer.mongo_control import digest


@pytest.fixture
def estate():
    value = helpers.estate.__wrapped__()
    keys = value[0]
    keys.permission_override = tuple((asyncio.run(keys.resolve('tenant-SYNTHETIC', 'owner', 'key'))).permissions) + tuple(
        'activation:observation:'+c for c in ['rights', 'lineage', 'inputs', 'quality_policy', 'quality_population',
                                            'quality_register', 'context_policy', 'context_window']) + ('activation:approval:answering-group',)
    return value


async def seed(estate, defect=None):
    keys, receipts, _ = estate
    parent, _, _ = await helpers.prepare(estate)
    request = Request(request_id='skill-SYNTHETIC', tenant_id='tenant-SYNTHETIC', principal_id='operator',
        kind='skill', engine='solva', objective_sha256='a'*64, input_refs=('akki://TEST/unit', 'akki://TEST/query'),
        scope_refs=('source-scope',), deadline_epoch=keys.now+900, result_floor='non_factual')
    worker_ref = await receipts.record(keys.receipt('worker', dict(runtime_id='skill-worker-SYNTHETIC', executor_version='v1',
        kinds=['skill'], enforced_dimensions=['spend', 'wall_clock', 'scanned_records'],
        enforcement_protocol='akki.runtime.limits/1', implementation_workspace_touched_data=False), signer='worker'))
    data = parent.model_dump(mode='json')
    data.update(request=request.model_dump(mode='json'), purposes=['answering'], worker_ref=worker_ref)
    data['groups'].append(dict(group='answering-group', purpose='answering', members=['answer-owner'], quorum=1))
    plan = Plan.model_validate_json(json.dumps(data))
    plan_ref = await receipts.record(keys.receipt('plan', plan.model_dump(mode='json'), request=request))
    for group in plan.groups:
        await receipts.record(keys.receipt('approval', dict(plan_ref=plan_ref, group=group.group, decision='approved',
            reason='SYNTHETIC_APPROVAL'), signer=group.members[0], request=request))
    policy = await observation(estate, request, 'inputs')
    for unit in request.input_refs:
        rights = Rights(version='akki.rights.metadata/1', unit_ref=unit, status='active', policy_ref=policy, reason_code='SYNTHETIC')
        await observation(estate, request, 'rights', 'rights', rights)
    q = quality_dict()
    if defect == 'changed_pack': q['pack']['version'] = 'different-pack'
    if defect == 'changed_snapshot': q['snapshot_sha256'] = '0'*64
    if defect in {'suspect_fact', 'junk'}:
        q['records'][0]['stratum'] = 'Junk' if defect == 'junk' else 'Suspect'
        if defect == 'junk':
            next(c for c in q['records'][0]['checks'] if c['rule_id'] == 'structural')['outcome'] = 'fail'
        else: q['records'][0]['provenance_known'] = False
        q['counts']['Clean'] = 0; q['counts'][q['records'][0]['stratum']] = 1
    pack = QualityPack.model_validate_json(json.dumps(q['pack']))
    q['policy_receipt_ref'] = await observation(estate, request, 'quality_policy', 'quality_pack', pack)
    pop_hash = digest({'snapshot_sha256': q['snapshot_sha256'], 'population_refs': q['population_refs']})
    q['population_receipt_ref'] = await receipts.record(keys.receipt('observation', Observation(category='quality_population',
        context_sha256=request.digest(), claim_sha256='0'*64 if defect == 'population' else pop_hash,
        evidence_mode='measured').model_dump(mode='json'), request=request))
    quality = QualityRegister.model_validate_json(json.dumps(q))
    quality_ref = await observation(estate, request, 'quality_register', 'quality_register', quality)
    if defect == 'missing_context': return request
    w = dict(version='akki.context.metadata/1', objective_sha256=request.objective_sha256,
        frame_ref='akki://TEST/frame', model_sha256='b'*64, tokenizer_sha256='c'*64,
        ranking_rule_ref='d'*64, qualified_set_receipt_ref=quality_ref, load_bearing_refs=['akki://TEST/unit'],
        window_tokens=10, reserved_tokens=2, units=[dict(unit_ref='akki://TEST/unit', content_sha256='f'*64,
            reextraction_ref='akki://TEST/reextract', class_label='fact', tokens=2, proximity=0, source_position=1)],
        selected_refs=['akki://TEST/unit'], excluded_counts={'fact': 0, 'inference': 0, 'utterance': 0, 'non_factual': 0},
        top_excluded_handles=[], loss_disclosed=False)
    if defect == 'context_hash': w['units'][0]['content_sha256'] = '0'*64
    if defect == 'objective': w['objective_sha256'] = '0'*64
    if defect == 'quality_link': w['qualified_set_receipt_ref'] = policy
    window = ContextWindow.model_validate_json(json.dumps(w))
    commitment = window.model_dump(mode='json', include={'frame_ref', 'model_sha256', 'tokenizer_sha256',
                                                        'load_bearing_refs', 'window_tokens', 'reserved_tokens'})
    w['ranking_rule_ref'] = await receipts.record(keys.receipt('observation', Observation(category='context_policy',
        context_sha256=request.digest(), claim_sha256='0'*64 if defect == 'policy' else digest(commitment),
        evidence_mode='measured').model_dump(mode='json'), request=request))
    window = ContextWindow.model_validate_json(json.dumps(w))
    await observation(estate, request, 'context_window', 'context_window', window)
    return request


def test_signed_quality_and_context_join_all_execution_gates(estate):
    async def run():
        request = await seed(estate)
        gate = NativeGovernance(estate[1], LedgerJournal(estate[1].db))
        for phase in ['reserve', 'dispatch', 'send', 'verify', 'publish', 'retrieve']:
            await gate.check(request, phase)
    with helpers.scope(): asyncio.run(run())


@pytest.mark.parametrize('defect,reason', [
    ('changed_pack', 'QUALITY_PLAN_BINDING_MISMATCH'), ('changed_snapshot', 'QUALITY_PLAN_BINDING_MISMATCH'),
    ('population', 'QUALITY_POPULATION_MISMATCH'), ('context_hash', 'CONTEXT_CONTENT_HASH_MISMATCH'),
    ('objective', 'CONTEXT_QUALITY_OR_OBJECTIVE_MISMATCH'), ('quality_link', 'CONTEXT_QUALITY_OR_OBJECTIVE_MISMATCH'),
    ('policy', 'CONTEXT_POLICY_MISMATCH'), ('suspect_fact', 'CONTEXT_QUALITY_CLASS_VIOLATION'),
    ('junk', 'CONTEXT_QUALITY_CLASS_VIOLATION'), ('missing_context', 'CONTEXT_WINDOW_PROOF_REQUIRED')])
def test_signed_but_wrong_quality_or_context_cannot_release(estate, defect, reason):
    async def run():
        request = await seed(estate, defect)
        gate = NativeGovernance(estate[1], LedgerJournal(estate[1].db))
        with pytest.raises(Held, match=reason): await gate.check(request, 'retrieve')
    with helpers.scope(): asyncio.run(run())