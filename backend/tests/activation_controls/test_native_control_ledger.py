"""Real crypto, SYNTHETIC admitted identities/receipts and FAKE Mongo. No worker RPCs."""
import asyncio
import copy
import json
import sys
import time
from contextlib import contextmanager
from pathlib import Path
import pytest
from pymongo.errors import DuplicateKeyError

sys.path.insert(0, str(Path(__file__).parents[1] / "portal_operational"))
from test_w1_control_record_contract_red import _FakeCollection, _FakeDb
from services.enforce.principal_context_adapter import principal_context
from services.enforce.control_scope import bind_control_scope
from services.activation.receipts import NativeReceipts, SignedReceipt, AdmittedSigner
from services.activation.record_shapes import Plan, Quantity
from services.activation.approvals import approved_plan
from services.activation.reservations import Reservations
from services.northena.execution_models import Request, Held
from services.watch.signature_primitive import watch_keygen, watch_sign


class ConcurrentCollection(_FakeCollection):
    async def insert_one(self, doc):
        await asyncio.sleep(0)
        for existing in self.docs:
            if existing["row"]["tenant_id"] == doc["row"]["tenant_id"] and (
                    existing["row"]["seq"] == doc["row"]["seq"] or existing["command_id"] == doc["command_id"]):
                raise DuplicateKeyError("TEST unique sequence/command")
        result = await super().insert_one(doc)
        doc["_id"] = "FAKE BSON mutation"
        return result


@contextmanager
def scope(principal="operator", tenant="tenant-SYNTHETIC"):
    with principal_context(principal), bind_control_scope({"principal_id": principal, "tenant_id": tenant}):
        yield


class Keys:
    def __init__(self):
        self.private, self.public = watch_keygen()
        self.revoked = set()
        self.permission_override = None
        self.now = int(time.time())

    async def resolve(self, tenant, principal, key_id):
        return AdmittedSigner(tenant_id=tenant, principal_id=principal, key_id=key_id,
            public_key_hex=self.public.hex(), admission_ref="SYNTHETIC-native-admission",
            permissions=self.permission_override if self.permission_override is not None else (
                "activation:plan", "activation:allocation", "activation:worker", "activation:revocation",
                "activation:approval:scope-group", "activation:approval:spend-group",
                "activation:observation:measurements", "activation:certificate", "activation:observation:runtime"),
            scope_refs=("source-scope",), valid_from_epoch=self.now-1000, expires_epoch=self.now+10000,
            revoked=principal in self.revoked)

    def receipt(self, kind, claims, *, signer="owner", request=None, **kw):
        r = SignedReceipt(version="akki.activation.receipt/1", tenant_id="tenant-SYNTHETIC", signer_id=signer,
            key_id="SYNTHETIC-key", kind=kind, request_sha256=request.digest() if request else None,
            scope_refs=("source-scope",), issued_epoch=self.now-1, expires_epoch=self.now+1000,
            claims=claims, signature_hex="0"*128)
        r = r.model_copy(update=kw)
        return r.model_copy(update={"signature_hex": watch_sign(self.private, r.signing_bytes()).hex()})


@pytest.fixture
def estate():
    keys = Keys()
    coll = ConcurrentCollection()
    return keys, NativeReceipts(_FakeDb(ledger_v1_control_events=coll), keys,
                               timeout_seconds=2, clock=lambda: keys.now), coll


def request(name="request-one"):
    return Request(request_id=name, tenant_id="tenant-SYNTHETIC", principal_id="operator", kind="source",
        engine="mtafiti", objective_sha256="a"*64, input_refs=("akki://source/descriptor",),
        scope_refs=("source-scope",), deadline_epoch=int(time.time())+900)


async def prepare(estate, req=None, *, allocation_ref=None, approve=True):
    keys, receipts, _ = estate
    req = req or request()
    limits = [{"dimension": "spend", "unit": "USD", "quantity": "7"},
              {"dimension": "wall_clock", "unit": "seconds", "quantity": "100"},
              {"dimension": "scanned_records", "unit": "records", "quantity": "10"}]
    if allocation_ref is None:
        allocation_ref = await receipts.record(keys.receipt("allocation", {"terms_ref": "terms-1", "limits": [
            {**q, "quantity": "10" if q["dimension"] == "spend" else "1000"} for q in limits]}))
    worker_ref = await receipts.record(keys.receipt("worker", {"runtime_id": "worker-SYNTHETIC",
        "executor_version": "test-1", "kinds": ["source"], "enforced_dimensions": [q["dimension"] for q in limits],
        "enforcement_protocol": "akki.runtime.limits/1", "implementation_workspace_touched_data": False}, signer="worker"))
    plan = Plan.model_validate_json(json.dumps({"request": req.model_dump(mode="json"),
        "groups": [{"group": "scope-group", "purpose": "scope", "members": ["scope-person"], "quorum": 1},
                   {"group": "spend-group", "purpose": "expenditure", "members": ["finance-person"], "quorum": 1}],
        "purposes": ["census"], "acceptance_script_sha256":"1"*64, "snapshot_hashes":["b"*64],
        "limits": limits, "allocation_ref": allocation_ref, "worker_ref": worker_ref, "terms_ref": "terms-1",
        "policy_epoch": 1, "termination_grace_seconds": 5,
        "dial_versions": {k: "v1" for k in ("custody_floor", "approving_authority", "external_crossing", "disclosure_counterparties")},
        "policy_versions": {k: "v1" for k in ("crossing_decision_table", "acceptance_standard", "cleanliness_pack")}}))
    ref = await receipts.record(keys.receipt("plan", plan.model_dump(mode="json"), request=req))
    approvals = []
    if approve:
        for group in plan.groups:
            approvals.append(await receipts.record(keys.receipt("approval", {"plan_ref": ref,
                "group": group.group, "decision": "approved", "reason": "SYNTHETIC approval"}, signer=group.members[0], request=req)))
    return plan, ref, approvals


def test_signature_roundtrip_and_ledger_mutation_is_excluded(estate):
    async def run():
        k, r, coll = estate
        value = k.receipt("allocation", {"terms_ref": "terms-1", "limits": [{"dimension":"spend","unit":"USD","quantity":"0"}]})
        ref = await r.record(value)
        assert ref == await r.record(value)
        assert (await r.resolve(ref, kind="allocation")).claims == value.claims
        assert "_id" not in coll.docs[0]
    with scope():
        asyncio.run(run())


@pytest.mark.parametrize("defect", ["tamper", "unbound", "expired", "revoked", "mandate", "tenant"])
def test_signature_refusals(estate, defect):
    async def run():
        k, r, _ = estate
        v = k.receipt("allocation", {"terms_ref": "terms-1", "limits": [{"dimension":"spend","unit":"USD","quantity":"0"}]})
        if defect == "tamper": v = v.model_copy(update={"claims": {**v.claims, "terms_ref": "forged"}})
        if defect == "unbound": r.admitted_keys = None
        if defect == "expired": k.now += 1001
        if defect == "revoked": k.revoked.add("owner")
        if defect == "mandate": k.permission_override = ()
        if defect == "tenant": v = v.model_copy(update={"tenant_id": "another-tenant"})
        with pytest.raises(Held): await r.record(v)
    with scope(): asyncio.run(run())


def test_approval_groups_survive_new_projection_and_revoke(estate):
    async def run():
        k, r, _ = estate
        plan, ref, approvals = await prepare(estate)
        assert (await approved_plan(NativeReceipts(r.db, k, timeout_seconds=2, clock=lambda:k.now), plan.request))[1] == ref
        await r.record(k.receipt("revocation", {"target_ref": approvals[1], "reason_code": "TEST_WITHDRAWAL"}))
        with pytest.raises(Held, match="APPROVAL_GROUP_PENDING"): await approved_plan(r, plan.request)
    with scope(): asyncio.run(run())


def test_one_group_does_not_satisfy_another(estate):
    async def run():
        k, r, _ = estate
        plan, ref, _ = await prepare(estate, approve=False)
        await r.record(k.receipt("approval", {"plan_ref": ref,"group":"scope-group","decision":"approved","reason":"SYNTHETIC approval"}, signer="scope-person",request=plan.request))
        with pytest.raises(Held, match="APPROVAL_GROUP_PENDING"): await approved_plan(r,plan.request)
    with scope(): asyncio.run(run())


def test_reservations_are_atomic_across_concurrent_runs_and_idempotent(estate):
    async def run():
        _, r, coll = estate
        first, fref, _ = await prepare(estate)
        second, sref, _ = await prepare(estate, request("request-two"), allocation_ref=first.allocation_ref)
        outcomes = await asyncio.gather(Reservations(r).reserve(first,fref), Reservations(r).reserve(second,sref), return_exceptions=True)
        assert sum(isinstance(v,str) for v in outcomes) == 1
        assert sum(isinstance(v,Held) and v.reason_code=="ALLOCATION_CAPACITY_EXCEEDED" for v in outcomes) == 1
        winner, ref = (first,fref) if isinstance(outcomes[0],str) else (second,sref)
        assert await Reservations(r).reserve(winner,ref) in outcomes
        assert sum(e["row"]["event_type"]=="activation.reserved" for e in coll.docs) == 1
    with scope(): asyncio.run(run())


def test_terminal_measurement_required_to_release_reservation(estate):
    async def run():
        k,r,_ = estate
        plan,ref,_ = await prepare(estate)
        reserved = await Reservations(r).reserve(plan,ref)
        claim = {"category":"measurements", "context_sha256":"b"*64, "claim_sha256":"c"*64,
                 "evidence_mode":"measured", "reservation_ref":reserved,
                 "quantities":[{**q.model_dump(),"quantity":"0"} for q in plan.limits], "terminal":False}
        observation = await r.record(k.receipt("observation",claim,signer="worker",request=plan.request))
        with pytest.raises(Held,match="TERMINAL_MEASUREMENT"): await Reservations(r).settle(reserved,observation)
        claim["terminal"] = True
        observation = await r.record(k.receipt("observation",claim,signer="worker",request=plan.request))
        assert await Reservations(r).settle(reserved,observation)
        second,sref,_ = await prepare(estate,request("request-two"),allocation_ref=plan.allocation_ref)
        assert await Reservations(r).reserve(second,sref)
    with scope(): asyncio.run(run())


@pytest.mark.parametrize("quantity", ["NaN","Infinity","-1"," 2","bad"])
def test_quantities_fail_closed(quantity):
    with pytest.raises(ValueError): Quantity(dimension="spend",unit="USD",quantity=quantity)


def test_owner_policy_mapping_exact(estate):
    async def run():
        plan,_,_ = await prepare(estate)
        d=plan.model_dump(mode="json")
        d["policy_and_dials"]={}
        with pytest.raises(ValueError): Plan.model_validate_json(json.dumps(d))
        assert set(plan.dial_versions)=={"custody_floor","approving_authority","external_crossing","disclosure_counterparties"}
    with scope(): asyncio.run(run())