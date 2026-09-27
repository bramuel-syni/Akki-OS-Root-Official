"""Native memory/release joins on signed SYNTHETIC authority and FAKE ledger."""
import asyncio
import json
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / 'activation_controls'))
sys.path.insert(0, str(Path(__file__).parents[1] / 'portal_operational'))
import test_native_control_ledger as helpers
import test_native_certificate_chain as certificate_helpers
from test_native_governance_gates import observation, seed_source
from test_governance_metadata import memory_dict
from services.activation.native_evidence import Observation
from services.activation.issuance import issue_certificate
from services.non_gpu_governance.certificates import GovernedNativeEvidence
from services.non_gpu_governance.gate import NativeGovernance
from services.non_gpu_governance.lineage import Rights, Lineage
from services.non_gpu_governance.context import ContextUnit
from services.non_gpu_governance.memory import MemoryEvidence
from services.northena.execution_journal import LedgerJournal
from services.northena.execution_models import Held
from services.ledger_writer.mongo_control import digest


@pytest.fixture
def estate():
    value = helpers.estate.__wrapped__()
    keys = value[0]
    keys.permission_override = tuple((asyncio.run(keys.resolve('tenant-SYNTHETIC', 'owner', 'key'))).permissions) + tuple(
        'activation:observation:'+c for c in ['rights', 'lineage', 'inputs', 'memory', 'memory_policy', 'memory_publication'])
    return value


async def memory_seed(estate, defect=None):
    keys, receipts, _ = estate
    request, rights_policy, _ = await seed_source(estate)
    journal = LedgerJournal(receipts.db)
    if defect != 'unclosed':
        await journal.append(request, 'terminal', {'phase': 'ready'})
    for ref, sha, parents in [('akki://TEST/unit', 'b'*64, request.input_refs),
                              ('akki://TEST/memory', 'a'*64, ('akki://TEST/unit',))]:
        await observation(estate, request, 'lineage', 'lineage', Lineage(version='akki.lineage.metadata/1',
            artifact_ref=ref, artifact_sha256=sha, parents=parents))
        await observation(estate, request, 'rights', 'rights', Rights(version='akki.rights.metadata/1',
            unit_ref=ref, status='active', policy_ref=rights_policy, reason_code='SYNTHETIC'))
    value = memory_dict()
    value['run_id'] = request.request_id
    value['retention_policy_ref'] = await observation(estate, request, 'memory_policy')
    if defect == 'source_hash': value['source_hashes'] = ['c'*64]
    if defect == 'principal': value['principal_id'] = 'other-principal'
    memory = MemoryEvidence.model_validate_json(json.dumps(value))
    value['publication_receipt_ref'] = await receipts.record(keys.receipt('observation', Observation(
        category='memory_publication', context_sha256=request.digest(), evidence_mode='measured',
        claim_sha256='0'*64 if defect == 'publication' else digest(memory.model_dump(mode='json', exclude={'publication_receipt_ref'}))
    ).model_dump(mode='json'), request=request))
    memory = MemoryEvidence.model_validate_json(json.dumps(value))
    ref = await observation(estate, request, 'memory', 'memory', memory)
    unit = ContextUnit(unit_ref=memory.artifact_ref, content_sha256=memory.artifact_sha256,
        reextraction_ref='akki://TEST/reextract', class_label='fact' if defect == 'class' else 'inference',
        tokens=10, proximity=0, source_position=1, memory_receipt_ref=ref)
    if defect == 'withdrawal':
        await observation(estate, request, 'rights', 'rights', Rights(version='akki.rights.metadata/1',
            unit_ref='akki://TEST/unit', status='withdrawn', policy_ref=rights_policy, reason_code='SYNTHETIC_WITHDRAWAL'))
    return request, unit


def test_memory_publication_source_versions_and_reload_class_join(estate):
    async def run():
        request, unit = await memory_seed(estate)
        gate = NativeGovernance(estate[1], LedgerJournal(estate[1].db))
        for _ in range(2):
            await gate.memory(request, await estate[1].events(), unit)
    with helpers.scope(): asyncio.run(run())


@pytest.mark.parametrize('defect,reason', [('source_hash', 'MEMORY_SOURCE_VERSION_MISMATCH'),
    ('principal', 'MEMORY_IDENTITY_OR_CLASS_MISMATCH'), ('class', 'MEMORY_IDENTITY_OR_CLASS_MISMATCH'),
    ('publication', 'MEMORY_PUBLICATION_MISMATCH'), ('unclosed', 'MEMORY_CLOSED_RUN_REQUIRED'),
    ('withdrawal', 'DESCENDANT_RIGHTS_WITHDRAWN')])
def test_memory_stale_or_uncommitted_context_is_refused(estate, defect, reason):
    async def run():
        request, unit = await memory_seed(estate, defect)
        gate = NativeGovernance(estate[1], LedgerJournal(estate[1].db))
        with pytest.raises(Held, match=reason): await gate.memory(request, await estate[1].events(), unit)
    with helpers.scope(): asyncio.run(run())


def test_historical_lab_certificate_is_not_live_governance_acceptance(estate):
    async def run():
        document, _, request = await certificate_helpers.chain(estate)
        receipts = estate[1]
        with pytest.raises(Held):
            await GovernedNativeEvidence(receipts).verify(document, tenant_id=request.tenant_id, principal_id=request.principal_id)
        with pytest.raises(Held):
            await issue_certificate(document, receipts, timeout_seconds=5, evidence=GovernedNativeEvidence(receipts))
        assert not any(e['row']['resource_type'] == 'activation_certificate' for e in await receipts.events())
    with helpers.scope(): asyncio.run(run())