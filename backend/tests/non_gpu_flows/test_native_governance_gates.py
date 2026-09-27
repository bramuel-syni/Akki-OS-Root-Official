"""Signed LAB receipts with SYNTHETIC native authority, no real source/provider."""
import asyncio
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / 'activation_controls'))
sys.path.insert(0, str(Path(__file__).parents[1] / 'portal_operational'))
import test_native_control_ledger as helpers
from services.non_gpu_governance.gate import NativeGovernance
from services.non_gpu_governance.lineage import Lineage, Rights
from services.non_gpu_governance.rights import RightsGate
from services.activation.native_evidence import Observation
from services.ledger_writer.mongo_control import digest
from services.northena.execution_journal import LedgerJournal
from services.northena.execution_models import Held, Artifact


@pytest.fixture
def estate():
    value = helpers.estate.__wrapped__()
    keys = value[0]
    keys.permission_override = tuple((asyncio.run(keys.resolve('tenant-SYNTHETIC', 'owner', 'key'))).permissions) + (
        'activation:observation:rights', 'activation:observation:lineage', 'activation:observation:inputs')
    return value


async def observation(estate, request, category, field=None, value=None, signer='native-observer'):
    keys, receipts, _ = estate
    claims = dict(category=category, context_sha256=request.digest(), evidence_mode='measured',
                  claim_sha256=digest(value.model_dump(mode='json')) if value else 'f'*64)
    if value is not None: claims[field] = value
    return await receipts.record(keys.receipt('observation', Observation(**claims).model_dump(mode='json'),
                                            request=request, signer=signer))


async def seed_source(estate):
    plan, _, _ = await helpers.prepare(estate)
    request = plan.request
    policy = await observation(estate, request, 'inputs')
    rights = Rights(version='akki.rights.metadata/1', unit_ref=request.input_refs[0], status='active',
                    policy_ref=policy, reason_code='SYNTHETIC_LAWFUL_SCOPE')
    await observation(estate, request, 'rights', 'rights', rights)
    return request, policy, rights


def test_source_missing_rights_holds_before_dispatch(estate):
    async def run():
        plan, _, _ = await helpers.prepare(estate)
        gate = NativeGovernance(estate[1], LedgerJournal(estate[1].db))
        with pytest.raises(Held, match='NATIVE_RIGHTS_PROOF_REQUIRED'):
            await gate.check(plan.request, 'reserve')
    with helpers.scope(): asyncio.run(run())


def test_source_signed_rights_current_on_every_gate_and_withdrawal_is_irreversible(estate):
    async def run():
        request, _, rights = await seed_source(estate)
        gate = NativeGovernance(estate[1], LedgerJournal(estate[1].db))
        for phase in ['reserve', 'send', 'verify', 'publish', 'retrieve']:
            await gate.check(request, phase)
        await observation(estate, request, 'rights', 'rights', rights.model_copy(update={'status': 'withdrawn'}))
        # Replaying the original active grant cannot revive an immutable version.
        await observation(estate, request, 'rights', 'rights', rights)
        for phase in ['reserve', 'publish', 'retrieve']:
            with pytest.raises(Held, match='DESCENDANT_RIGHTS_WITHDRAWN'):
                await gate.check(request, phase)
    with helpers.scope(): asyncio.run(run())


def test_transitive_native_lineage_and_current_release_hash(estate):
    async def run():
        request, policy, rights = await seed_source(estate)
        child = 'akki://TEST/result'
        node = Lineage(version='akki.lineage.metadata/1', artifact_ref=child, artifact_sha256='b'*64,
                       parents=request.input_refs)
        await observation(estate, request, 'lineage', 'lineage', node)
        await observation(estate, request, 'rights', 'rights', rights.model_copy(update={'unit_ref': child}))
        gate = RightsGate(estate[1])
        assert await gate.affected(request, request.input_refs[0]) == (child,)
        events = await estate[1].events()
        artifact = Artifact(ref=child, sha256='b'*64, size_bytes=2, tenant_id=request.tenant_id, class_label='non_factual')
        assert request.input_refs[0] in await gate.check(request, (child,), events, artifacts=(artifact,))
        with pytest.raises(Held, match='ARTIFACT_LINEAGE_REQUIRED'):
            await gate.check(request, (child,), events, artifacts=(artifact.model_copy(update={'sha256': 'c'*64}),))
        await observation(estate, request, 'rights', 'rights', rights.model_copy(update={'status': 'withdrawn'}))
        with pytest.raises(Held, match='DESCENDANT_RIGHTS_WITHDRAWN'):
            await gate.check(request, (child,), await estate[1].events(), artifacts=(artifact,))
    with helpers.scope(): asyncio.run(run())


def test_missing_mandate_and_expired_proof_never_grant_rights(estate):
    async def run():
        request, _, _ = await seed_source(estate)
        gate = NativeGovernance(estate[1], LedgerJournal(estate[1].db))
        estate[0].permission_override = tuple(p for p in estate[0].permission_override if not p.endswith(':rights'))
        with pytest.raises(Held, match='SIGNER_MANDATE_INSUFFICIENT'):
            await gate.check(request, 'retrieve')
    with helpers.scope(): asyncio.run(run())


def test_prefix_change_during_native_rights_check_holds(estate, monkeypatch):
    async def run():
        request, _, rights = await seed_source(estate)
        gate = NativeGovernance(estate[1], LedgerJournal(estate[1].db))
        check = gate.rights.check
        async def concurrent(*args, **kwargs):
            result = await check(*args, **kwargs)
            await observation(estate, request, 'rights', 'rights', rights.model_copy(update={'status': 'withdrawn'}))
            return result
        monkeypatch.setattr(gate.rights, 'check', concurrent)
        with pytest.raises(Held, match='GOVERNANCE_EVIDENCE_PREFIX_CHANGED'):
            await gate.check(request, 'publish')
    with helpers.scope(): asyncio.run(run())