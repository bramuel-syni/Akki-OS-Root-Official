"""Entire signed Path-A proof using SYNTHETIC native observations and FAKE ledger.

This verifies software composition, not a real source read, retrieval or trust root.
"""
import asyncio
from datetime import datetime, timezone
import pytest
import test_native_control_ledger as native_tests
from test_native_control_ledger import scope, prepare
from test_activation_validation_red import _base_document
from services.activation.native_evidence import NativeEvidence, claim_digest, certificate_signing_digest
from services.activation.validation import validate_certificate
from services.activation.issuance import issue_certificate
from services.activation.reservations import Reservations
from services.northena.execution_journal import LedgerJournal
from services.ledger_writer.mongo_control import digest
from services.northena.execution_models import Held


@pytest.fixture
def estate():
    return native_tests.estate.__wrapped__()


async def chain(estate):
    k,r,_=estate
    k.permission_override=("activation:plan","activation:allocation","activation:worker","activation:revocation",
        "activation:approval:scope-group","activation:approval:spend-group","activation:certificate",
        *tuple("activation:observation:"+name for name in ("inputs","measurements","manifest","runtime",
            "independence","retrieval","revalidation","acceptance")))
    plan,plan_ref,approvals=await prepare(estate)
    req=plan.request; journal=LedgerJournal(r.db)
    await journal.append(req,"request",{"request_sha256":req.digest(),"request":req.model_dump(mode="json")})
    reserved=await Reservations(r).reserve(plan,plan_ref)
    envelope={"protocol":"akki.runtime.limits/1","request_sha256":req.digest(),"plan_ref":plan_ref,
        "reservation_ref":reserved,"runtime_id":"worker-SYNTHETIC","operation_key":"TEST-operation","fence":1,
        "limits":[q.model_dump() for q in plan.limits],
        "starts_epoch":k.now,"stop_work_by_epoch":k.now+95,"terminate_by_epoch":k.now+100}
    ack=await r.record(k.receipt("observation",{"category":"runtime","context_sha256":req.digest(),
        "claim_sha256":digest(envelope),"evidence_mode":"measured"},signer="worker",request=req))
    await journal.append(req,"runtime_limits",{"envelope":envelope,"ack_ref":ack})
    await journal.append(req,"send",{"action":"submit","operation_key":"TEST-operation","fence":1})
    iso=lambda n:datetime.fromtimestamp(n,timezone.utc).isoformat()
    d=_base_document()
    d["identity"].update(estate_id=req.tenant_id,tenant_id=req.tenant_id,frozen_request_id=req.request_id,
        frozen_objective_hash=req.objective_sha256,run_started_at=iso(k.now),run_ended_at=iso(k.now))
    for key,g,ref in zip(("scope","expenditure"),plan.groups,approvals):
        d["authority"][key]={"group":g.group,"rule":"any_one","decisions":[{"principal_id":g.members[0],
            "decision":"approved","reason":"SYNTHETIC approval","recorded_at":iso(k.now-1),"receipt_ref":ref}]}
    d["inputs"]["dial_versions"]=plan.dial_versions; d["inputs"]["policy_versions"]=plan.policy_versions
    d["runtime"].update(admitted_runtime_id="worker-SYNTHETIC",executor_version="test-1")
    d["limits"]["dimensions"]=[{"dimension":q.dimension,"unit":q.unit,"effective_limit":float(q.quantity),
        "observed":10 if q.dimension=="scanned_records" else 0,"source":"owner_run_limit","enforced_by":"worker-SYNTHETIC"} for q in plan.limits]
    d["output"].update(manifest_row_count=10,denominator_count=10,
        reconciliation={"processed":10,"refused_with_reason":0,"unmeasured_with_reason":0,"unaccounted":0},
        registry_entry_id="SYNTHETIC-native-registry-entry")
    d["usage"].update(terms_identifier="terms-1",reservation_ref=reserved,
        measured_quantities=[{"unit":"GPU_hour","quantity":0,"measured_by":"worker-SYNTHETIC"}])
    d["release_acceptance"].update(recorded_at=iso(k.now),acceptance_standard_ref=None)
    d["evidence"]["retrieval"].update(principal_id="retriever",retrieved_at=iso(k.now))
    d["evidence"]["acceptance_script"]["written_before_run_at"]=iso(k.now-2)
    d["evidence"]["re_performance"].update(sample_size=1,agreements=1,disagreements=0,disagreement_refs=[])
    d["issuer"].update(principal_id="issuer",issued_at=iso(k.now))
    await journal.append(req,"registry",{"evidence_mode":"measured",
        "artifacts":[{"sha256":d["output"]["artefact_hash"]}],"records":[{"receipt_id":d["output"]["registry_entry_id"]}]})
    await journal.append(req,"metered",{"evidence_mode":"measured","usage":[{"unit":"GPU_hour","quantity":"0"}]})
    await journal.append(req,"terminal",{"evidence_mode":"measured","phase":"ready"})
    sections={"inputs":d["inputs"],"measurements":{"limits":d["limits"],"usage":d["usage"]},
        "manifest":d["output"],"runtime":d["runtime"],"independence":d["evidence"]["re_performance"],
        "retrieval":d["evidence"]["retrieval"],"revalidation":d["supersession"],"acceptance":d["evidence"]["acceptance_script"]}
    refs={}
    for name,value in sections.items():
        signer="worker" if name in {"runtime","measurements"} else "retriever" if name=="retrieval" else "inspector-"+name
        claims={"category":name,"context_sha256":digest(d["identity"]),"claim_sha256":claim_digest(value),
                "evidence_mode":"measured","terminal":name in {"runtime","measurements"}}
        if name=="measurements":
            claims.update(reservation_ref=reserved,quantities=[{**q.model_dump(),"quantity":"10" if q.dimension=="scanned_records" else "0"} for q in plan.limits])
        refs[name]=await r.record(k.receipt("observation",claims,signer=signer,request=req))
    d["evidence"]["receipt_refs"]=[ref for name,ref in refs.items() if name!="measurements"]
    d["evidence"]["retrieval"]["receipt_ref"]=refs["retrieval"]
    d["usage"]["metered_event_refs"]=[refs["measurements"]]
    await Reservations(r).settle(reserved,refs["measurements"])
    d["issuer"]["verifier_head_hash"]=(await r.events())[-1]["row"]["hash"]
    d["issuer"]["signature"]=await r.record(k.receipt("certificate",{
        "certificate_sha256":certificate_signing_digest(d)},signer="issuer",request=req,issued_epoch=k.now))
    return d,refs,req


async def resign(estate, req, d):
    k,r,_ = estate
    d["issuer"]["verifier_head_hash"] = (await r.events())[-1]["row"]["hash"]
    d["issuer"]["issued_at"] = datetime.fromtimestamp(k.now, timezone.utc).isoformat()
    d["issuer"]["signature"] = await r.record(k.receipt("certificate", {
        "certificate_sha256": certificate_signing_digest(d)
    }, signer="issuer", request=req, issued_epoch=k.now))


def test_native_signed_chain_verifies_and_issues_idempotently(estate):
    async def run():
        d,_,_=await chain(estate); _,r,_=estate
        result=await validate_certificate(d,tenant_id=d["identity"]["tenant_id"],principal_id="operator",
                                         evidence=NativeEvidence(r),timeout_seconds=5)
        assert result.valid, result.issues
        _,ref=await issue_certificate(d,r,timeout_seconds=5)
        assert ref==(await issue_certificate(d,r,timeout_seconds=5))[1]
    with scope(): asyncio.run(run())


@pytest.mark.parametrize("mutation",["policy","approval_actor","signature","termination","retriever","revocation"])
def test_native_signed_chain_rejects_changed_or_revoked_proof(estate,mutation):
    async def run():
        d,refs,_=await chain(estate); k,r,_=estate
        if mutation=="policy": d["inputs"]["dial_versions"]["custody_floor"]="wrong"
        if mutation=="approval_actor": d["authority"]["scope"]["decisions"][0]["principal_id"]="fake"
        if mutation=="signature": d["issuer"]["principal_id"]="fake"
        if mutation=="termination": d["runtime"]["executor_version"]="fake"
        if mutation=="retriever": d["evidence"]["retrieval"]["principal_id"]="fake"
        if mutation=="revocation":
            await r.record(k.receipt("revocation",{"target_ref":refs["runtime"],"reason_code":"TEST_REVOKED"}))
        result=await validate_certificate(d,tenant_id=d["identity"]["tenant_id"],principal_id="operator",
                                         evidence=NativeEvidence(r),timeout_seconds=5)
        assert not result.valid
        with pytest.raises(Held): await issue_certificate(d,r,timeout_seconds=5)
    with scope(): asyncio.run(run())


@pytest.mark.parametrize("mutation",[
    "changed_native_reference","wrong_purpose","mismatched_approval_actor","mismatched_approval_rule",
    "inconsistent_scan_denominator","independent_runtime_termination","missing_predeclared_script",
    "missing_predeclared_snapshot","supersession_unresolved",
])
def test_native_signed_chain_freshly_resigned_semantic_mutations_fail_without_signature_staleness(estate, mutation):
    async def run():
        d,_,req = await chain(estate)
        k,r,_ = estate
        if mutation == "changed_native_reference":
            d["output"]["registry_entry_id"] = "SYNTHETIC-native-registry-entry-tampered"
        if mutation == "wrong_purpose":
            d["authority"]["purposes_authorised"] = ["training"]
        if mutation == "mismatched_approval_actor":
            d["authority"]["scope"]["decisions"][0]["principal_id"] = "finance-person"
        if mutation == "mismatched_approval_rule":
            d["authority"]["scope"]["rule"] = "quorum"
        if mutation == "inconsistent_scan_denominator":
            d["output"]["denominator_count"] = 11
        if mutation == "independent_runtime_termination":
            d["identity"]["run_ended_at"] = datetime.fromtimestamp(k.now + 200, timezone.utc).isoformat()
        if mutation == "missing_predeclared_script":
            d["evidence"]["acceptance_script"]["script_hash"] = "f"*64
        if mutation == "missing_predeclared_snapshot":
            d["inputs"]["snapshot_hashes"] = []
        if mutation == "supersession_unresolved":
            d["supersession"]["supersedes"] = "e"*64

        # Fresh signer receipt avoids stale-signature false positives.
        await resign(estate, req, d)

        result = await validate_certificate(
            d,
            tenant_id=d["identity"]["tenant_id"],
            principal_id="operator",
            evidence=NativeEvidence(r),
            timeout_seconds=5,
        )
        assert not result.valid
        assert all(issue.code != "CERTIFICATE_SIGNATURE_BINDING_MISMATCH" for issue in result.issues)
        with pytest.raises(Held):
            await issue_certificate(d, r, timeout_seconds=5)
    with scope():
        asyncio.run(run())