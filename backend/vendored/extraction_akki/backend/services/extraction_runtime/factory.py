"""AKKI_NATIVE_RUNTIME_FACTORY target: compose the native runtime from estate admission records.

Nothing here names a tenant, a host or a key. Signers resolve from the ledger, runtimes from
their descriptors, custody from the tenant's registry entry mirrored into estate custody.
"""
import json
import logging
import os
from services.activation.decisions import LedgerActivationDecisions
from services.activation.receipts import NativeReceipts
from services.activation.runtime_binding import NativeExecutionBindings, NativeRuntime
from services.custody_delivery.ports import CustodyBinding
from services.estate_admission.resolver import LedgerAdmittedSigners, ledger_principal_lookup
from services.estate_admission.signing import custody_dir
from services.extraction_runtime.adapter import build_source_adapter
from services.extraction_runtime.custody_provider import ObjectStoreCustody
from services.extraction_runtime.inspector import IndependentInspector
from services.northena.execution_eligibility import InputEligibility

log = logging.getLogger(__name__)


def custody_mirrors():
    root = custody_dir()
    mirrors = []
    if root.exists():
        for path in sorted(root.glob('*/custody_descriptor.json')):
            mirrors.append((path.parent.name, json.loads(path.read_text())))
    return mirrors


async def build(db):
    from services.extraction_runtime.skill_adapter import build_skill_adapter
    from services.extraction_runtime.skill_providers import SkillEligibility, SkillHandoff
    from services.mkondo.execution_handoff import MkondoHandoff
    timeout = float(os.environ.get('AKKI_NATIVE_RUNTIME_TIMEOUT_SECONDS', '30'))
    receipts = NativeReceipts(db, LedgerAdmittedSigners(db), timeout_seconds=timeout)
    # The skill executor is the deterministic unit-retrieval worker (owner ruling 2026-10-01, 2a): eligibility reads the
    # worker-signed quality register, the handoff receiver is the admitted worker runtime acknowledging on its own host.
    bindings = NativeExecutionBindings(
        decisions=LedgerActivationDecisions(receipts), inspector=IndependentInspector(db, receipts),
        executors={'source': build_source_adapter(db, receipts), 'skill': build_skill_adapter(db, receipts)},
        eligibility=InputEligibility(None, SkillEligibility(db, receipts), timeout),
        handoffs=MkondoHandoff(None, None, SkillHandoff(db, receipts), timeout),
        gate_timeout_seconds=timeout, principal_lookup=ledger_principal_lookup(db))
    custody = None
    mirrors = [(tenant, record) for tenant, record in custody_mirrors() if record.get('endpoint_origin')]
    for tenant, record in custody_mirrors():
        if not record.get('endpoint_origin'):
            log.warning('CUSTODY_GRANT_ORIGIN_UNRULED tenant=%s provider=%s (artefacts rest in the store; grants held)', tenant, record.get('provider'))
    if mirrors:
        tenant, record = mirrors[0]
        if len(mirrors) > 1:
            log.warning('CUSTODY_BINDING_SINGLE_TENANT_LIMIT bound=%s others=%d', tenant, len(mirrors) - 1)
        max_grant = int(os.environ.get('AKKI_CUSTODY_MAX_GRANT_SECONDS', '900'))
        custody = CustodyBinding(receipts=receipts, provider=ObjectStoreCustody(db, receipts, max_grant),
                                 custodian_principal_id=record['custodian_principal_id'],
                                 allowed_origins=(record['endpoint_origin'],), max_grant_seconds=max_grant,
                                 timeout_seconds=timeout + 120)
    return NativeRuntime(receipts=receipts, bindings=bindings, evidence_timeout_seconds=timeout, custody=custody)
