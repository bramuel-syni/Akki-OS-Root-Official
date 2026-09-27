"""Purpose-bound DQ consumer. No classifier, thresholds, truth or admission grants."""
import time
from typing import Annotated, Literal
from pydantic import Field
from services.ledger_writer.mongo_control import digest
from services.ledger_writer.principal_control import CommandConflict
from services.northena.execution_models import Frozen, Hash, Handle, Name, Held
from services.northena.execution_gate_checks import async_provider, bounded, typed

Refs = Annotated[tuple[Handle, ...], Field(min_length=1, max_length=1000)]
PURPOSES = {"skill": "skill_context", "training": "training_material", "evaluation": "evaluation_material"}


class EligibilityReceipt(Frozen):
    request_sha256: Hash
    input_refs: Refs
    scope_refs: Annotated[tuple[Name, ...], Field(min_length=1, max_length=1000)]
    purpose: Literal["skill_context", "training_material", "evaluation_material"]
    policy_ref: Handle
    rule_pack_refs: Refs
    snapshot_refs: Refs
    decision_ref: Handle
    disposition: Literal["eligible", "ineligible", "not_assessed", "unknown"]
    reason_code: Name
    expires_epoch: Annotated[int, Field(gt=0)]
    evidence_mode: Literal["measured", "MOCKED"]


def basis(receipt):
    return receipt.model_dump(mode="json", include={"request_sha256", "input_refs", "scope_refs",
                                                   "purpose", "policy_ref", "rule_pack_refs", "snapshot_refs"})


class InputEligibility:
    def __init__(self, journal, provider=None, timeout_seconds=None, clock=time.time):
        async_provider(provider, ("evaluate",), timeout_seconds)
        self.journal, self.provider = journal, provider
        self.timeout_seconds, self.clock = timeout_seconds, clock

    def bind(self, journal, timeout_seconds):
        return InputEligibility(journal, self.provider, timeout_seconds, self.clock)

    async def check(self, request, phase):
        if request.kind == "source":
            return None
        if self.provider is None:
            raise Held("INPUT_ELIGIBILITY_NOT_BOUND")
        purpose = PURPOSES[request.kind]
        receipt = typed(await bounded(self.provider.evaluate, self.timeout_seconds, request, purpose, phase),
                        EligibilityReceipt, "INPUT_ELIGIBILITY_INVALID")
        if (receipt.request_sha256 != request.digest() or receipt.input_refs != request.input_refs
                or receipt.scope_refs != request.scope_refs or receipt.purpose != purpose
                or receipt.evidence_mode != "measured"
                or len(set(receipt.rule_pack_refs)) != len(receipt.rule_pack_refs)
                or len(set(receipt.snapshot_refs)) != len(receipt.snapshot_refs)):
            raise Held("INPUT_ELIGIBILITY_BINDING_INVALID")
        data = {"receipt": receipt.model_dump(mode="json"), "phase": phase}
        check = await self.journal.append(request, "eligibility_check:" + digest(data), data)
        if receipt.expires_epoch <= self.clock():
            raise Held("INPUT_ELIGIBILITY_EXPIRED")
        if receipt.disposition != "eligible":
            raise Held("INPUT_NOT_ELIGIBLE")
        rows = await self.journal.read(request)
        pinned = next((r for r in rows if r["slot"] == "eligibility"), None)
        if pinned is None:
            try:
                pinned = await self.journal.append(request, "eligibility", {"basis": basis(receipt)})
            except CommandConflict:
                pinned = next(r for r in await self.journal.read(request) if r["slot"] == "eligibility")
        if pinned["data"]["basis"] != basis(receipt):
            raise Held("INPUT_ELIGIBILITY_BASIS_CHANGED")
        return check