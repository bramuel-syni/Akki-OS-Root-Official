"""Native Path-B/C signed evidence chains (SYNTHETIC only, fake ledger, no live effects)."""

import asyncio
import json
from datetime import datetime, timezone

import pytest
import test_native_control_ledger as native_tests
from test_activation_validation_red import _base_document
from test_native_control_ledger import scope
from test_native_model_acceptance import evaluation_fixture

from services.activation.issuance import issue_certificate
from services.activation.model_proofs import Grounding, Refusal, Evaluation
from services.activation.native_evidence import NativeEvidence, claim_digest, certificate_signing_digest
from services.activation.record_shapes import Plan
from services.activation.reservations import Reservations
from services.activation.validation import validate_certificate
from services.ledger_writer.mongo_control import digest
from services.northena.execution_journal import LedgerJournal
from services.northena.execution_models import Artifact, Held, Request, Usage, WorkerResult


@pytest.fixture
def estate():
    return native_tests.estate.__wrapped__()


def _iso(epoch: int) -> str:
    return datetime.fromtimestamp(epoch, timezone.utc).isoformat()


def _permissions() -> tuple[str, ...]:
    categories = (
        "anchor",
        "release",
        "inputs",
        "measurements",
        "manifest",
        "runtime",
        "independence",
        "retrieval",
        "refusal",
        "revalidation",
        "acceptance",
        "skill",
        "training",
        "evaluation",
    )
    return (
        "activation:plan",
        "activation:allocation",
        "activation:worker",
        "activation:revocation",
        "activation:approval:scope-group",
        "activation:approval:spend-group",
        "activation:approval:answering-group",
        "activation:approval:training-group",
        "activation:approval:evaluation-group",
        "activation:certificate",
        *tuple("activation:observation:" + v for v in categories),
    )


async def _record_plan(estate, req: Request, *, purposes, purpose_groups, worker_kinds, evaluation_standard=None,
                       worker_signer="worker", allocation_capacity="100"):
    k, r, _ = estate
    limits = [
        {"dimension": "spend", "unit": "USD", "quantity": "7"},
        {"dimension": "wall_clock", "unit": "seconds", "quantity": "100"},
    ]
    allocation_ref = await r.record(k.receipt("allocation", {
        "terms_ref": "terms-1",
        "limits": [{**q, "quantity": allocation_capacity} for q in limits],
    }))
    worker_ref = await r.record(k.receipt("worker", {
        "runtime_id": worker_signer + "-SYNTHETIC",
        "executor_version": "test-1",
        "kinds": list(worker_kinds),
        "enforced_dimensions": [q["dimension"] for q in limits],
        "enforcement_protocol": "akki.runtime.limits/1",
        "implementation_workspace_touched_data": False,
    }, signer=worker_signer))
    groups = [
        {"group": "scope-group", "purpose": "scope", "members": ["scope-person"], "quorum": 1},
        {"group": "spend-group", "purpose": "expenditure", "members": ["finance-person"], "quorum": 1},
        *purpose_groups,
    ]
    body = {
        "request": req.model_dump(mode="json"),
        "groups": groups,
        "purposes": list(purposes),
        "acceptance_script_sha256": "1" * 64,
        "snapshot_hashes": ["b" * 64],
        "limits": limits,
        "allocation_ref": allocation_ref,
        "worker_ref": worker_ref,
        "terms_ref": "terms-1",
        "policy_epoch": 1,
        "termination_grace_seconds": 5,
        "dial_versions": {k: "v1" for k in (
            "custody_floor",
            "approving_authority",
            "external_crossing",
            "disclosure_counterparties",
        )},
        "policy_versions": {k: "v1" for k in (
            "crossing_decision_table",
            "acceptance_standard",
            "cleanliness_pack",
        )},
        "evaluation_standard": None if evaluation_standard is None else evaluation_standard.model_dump(mode="json"),
    }
    plan = Plan.model_validate_json(json.dumps(body))
    plan_ref = await r.record(k.receipt("plan", plan.model_dump(mode="json"), request=req))
    approval_refs = []
    for g in plan.groups:
        approval_refs.append(await r.record(k.receipt("approval", {
            "plan_ref": plan_ref,
            "group": g.group,
            "decision": "approved",
            "reason": "SYNTHETIC approval",
        }, signer=g.members[0], request=req)))
    return plan, plan_ref, tuple(approval_refs)


async def _approval_map(receipts, approvals, request_sha256):
    mapped = {}
    for ref in approvals:
        receipt = await receipts.resolve(ref, kind="approval", request_sha256=request_sha256)
        mapped[receipt.claims["group"]] = ref
    return mapped


def _base_doc(path: str, req: Request, now_epoch: int):
    d = _base_document()
    d["identity"].update(
        path=path,
        estate_id=req.tenant_id,
        tenant_id=req.tenant_id,
        frozen_request_id=req.request_id,
        frozen_objective_hash=req.objective_sha256,
        run_started_at=_iso(now_epoch),
        run_ended_at=_iso(now_epoch),
    )
    d["issuer"].update(principal_id="issuer", issued_at=_iso(now_epoch))
    return d


async def _skill_chain(estate):
    k, r, _ = estate
    k.permission_override = _permissions()
    req = Request(
        request_id="REQ-SYNTHETIC-SKILL",
        tenant_id="tenant-SYNTHETIC",
        principal_id="operator",
        kind="skill",
        engine="solva",
        objective_sha256="a" * 64,
        input_refs=("akki://TEST/deployed-skill", "akki://TEST/grant", "akki://TEST/query"),
        scope_refs=("source-scope",),
        deadline_epoch=k.now + 900,
        result_floor="non_factual",
    )
    plan, plan_ref, approvals = await _record_plan(
        estate,
        req,
        purposes=("answering",),
        purpose_groups=({"group": "answering-group", "purpose": "answering", "members": ["answering-person"], "quorum": 1},),
        worker_kinds=("skill",),
    )
    journal = LedgerJournal(r.db)
    await journal.append(req, "request", {"request_sha256": req.digest(), "request": req.model_dump(mode="json")})
    reserved = await Reservations(r).reserve(plan, plan_ref)
    dispatch = await journal.append(req,"dispatch",{"action":"submit","operation_key":"TEST-operation-skill"})
    envelope = {
        "protocol": "akki.runtime.limits/1",
        "request_sha256": req.digest(),
        "plan_ref": plan_ref,
        "reservation_ref": reserved,
        "runtime_id": "worker-SYNTHETIC",
        "operation_key": "TEST-operation-skill",
        "fence": dispatch["seq"],
        "limits": [q.model_dump() for q in plan.limits],
        "starts_epoch": k.now - 1,
        "stop_work_by_epoch": k.now + 95,
        "terminate_by_epoch": k.now + 99,
    }
    ack = await r.record(k.receipt("observation", {
        "category": "runtime",
        "context_sha256": req.digest(),
        "claim_sha256": digest(envelope),
        "evidence_mode": "measured",
    }, signer="worker", request=req))
    await journal.append(req, "runtime_limits", {"envelope": envelope, "ack_ref": ack})
    await journal.append(req, "send", {"action": "submit", "operation_key": "TEST-operation-skill", "fence": dispatch["seq"]})

    artifact_hash = "e" * 64
    worker_result = WorkerResult(
        operation_key="TEST-operation-skill",
        fence=dispatch["seq"],
        request_sha256=req.digest(),
        executor_id="worker",
        state="complete",
        receipt_ref="akki://TEST/worker-terminal-skill",
        evidence_mode="measured",
        artifacts=(Artifact(ref="akki://TEST/skill-answer", sha256=artifact_hash, size_bytes=1,
                            tenant_id=req.tenant_id, class_label="non_factual"),),
        usage=(Usage(unit="GPU_hour", quantity="0"),),
    )
    await journal.append(req, "worker_outcome", {"result": worker_result.model_dump(mode="json")})
    await journal.append(req, "observation:" + digest(worker_result.model_dump(mode="json")), {"result": worker_result.model_dump(mode="json")})
    await journal.append(req, "registry", {
        "evidence_mode": "measured",
        "artifacts": [{"ref": "akki://TEST/skill-answer", "sha256": artifact_hash}],
        "records": [{"receipt_id": "SYNTHETIC-native-registry-skill"}],
    })
    await journal.append(req, "metered", {"evidence_mode": "measured", "terms_ref":plan.terms_ref, "usage": [{"unit": "GPU_hour", "quantity": "0"}]})
    await journal.append(req, "terminal", {"evidence_mode": "measured", "phase": "ready"})

    d = _base_doc("B_callable_skill", req, k.now)
    d["authority"]["purposes_authorised"] = ["answering"]
    approval_by_group = await _approval_map(r, approvals, req.digest())
    for key, group_name in (("scope", "scope-group"), ("expenditure", "spend-group")):
        g = next(v for v in plan.groups if v.group == group_name)
        approval_ref = approval_by_group[group_name]
        d["authority"][key] = {
            "group": g.group,
            "rule": "any_one",
            "decisions": [{
                "principal_id": g.members[0],
                "decision": "approved",
                "reason": "SYNTHETIC approval",
                "recorded_at": _iso(k.now - 1),
                "receipt_ref": approval_ref,
            }],
        }
    answering_group = next(v for v in plan.groups if v.group == "answering-group")
    answering_ref = approval_by_group["answering-group"]
    d["authority"]["purpose_specific"] = [{
        "group": answering_group.group,
        "rule": "any_one",
        "decisions": [{
            "principal_id": answering_group.members[0],
            "decision": "approved",
            "reason": "SYNTHETIC approval",
            "recorded_at": _iso(k.now - 1),
            "receipt_ref": answering_ref,
        }],
    }]
    d["release_acceptance"] = {
        "decision": "refused",
        "recorded_at": _iso(k.now),
        "acceptance_standard_ref": None,
        "criteria": [{
            "criterion_id": "skill_scope_gate",
            "measured_value": None,
            "threshold": None,
            "outcome": "not_measured",
            "measurement_ref": None,
        }],
        "prerequisites": [{
            "prerequisite_id": "domain-policy-b",
            "extension_version": "ext-1",
            "outcome": "not_measured",
            "record_ref": None,
        }],
    }
    d["inputs"].update(
        snapshot_hashes=list(plan.snapshot_hashes),
        dial_versions=plan.dial_versions,
        policy_versions=plan.policy_versions,
        custody_classes_in_scope=["uncontrolled"],
        held_out_ref=None,
    )
    d["limits"]["dimensions"] = [
        {"dimension": "spend", "unit": "USD", "effective_limit": 7.0, "observed": 0.0,
         "source": "owner_run_limit", "enforced_by": "worker-SYNTHETIC"},
        {"dimension": "wall_clock", "unit": "seconds", "effective_limit": 100.0, "observed": 0.0,
         "source": "owner_run_limit", "enforced_by": "worker-SYNTHETIC"},
    ]
    model_licence_ref = await r.record(k.receipt("observation", {
        "category": "inputs",
        "context_sha256": req.digest(),
        "claim_sha256": digest({"licence": "skill-model-licence"}),
        "evidence_mode": "measured",
    }, signer="licensor", request=req))
    d["runtime"].update(
        admitted_runtime_id="worker-SYNTHETIC",
        executor_version="test-1",
        model_refs=[{
            "registry_id": "registry_model_skill_1",
            "hash": "3" * 64,
            "version": "v1.0.0",
            "licence_ref": model_licence_ref,
        }],
        recipe_ref=None,
        implementation_workspace_touched_data=False,
    )
    d["output"].update(
        artefact_hash=artifact_hash,
        registry_entry_id="SYNTHETIC-native-registry-skill",
        manifest_hash="f" * 64,
        manifest_row_count=2,
        denominator_count=2,
        reconciliation={"processed": 1, "refused_with_reason": 1, "unmeasured_with_reason": 0, "unaccounted": 0},
    )
    d["usage"].update(
        terms_identifier=plan.terms_ref,
        measured_quantities=[{"unit": "GPU_hour", "quantity": 0.0, "measured_by": "worker-SYNTHETIC"}],
        reservation_ref=reserved,
        reconciled_against_reservation=True,
    )
    d["evidence"]["retrieval"].update(principal_id="retriever", retrieved_at=_iso(k.now), receipt_ref="")
    request_ref = await r.record(k.receipt("observation", {
        "category": "inputs",
        "context_sha256": req.digest(),
        "claim_sha256": digest({"refusal_request": "out-of-scope"}),
        "evidence_mode": "measured",
    }, signer="question-auditor", request=req))
    d["evidence"]["refusal_demonstration"] = {
        "kind": "out_of_scope_question",
        "request_ref": request_ref,
        "reason_stated": "Question outside admitted scope",
        "receipt_ref": "",
    }
    d["evidence"]["acceptance_script"].update(script_hash=plan.acceptance_script_sha256, written_before_run_at=_iso(k.now - 2), result="pass")
    d["evidence"]["re_performance"].update(second_instance_id="instance-b", different_model_family=True,
                                                 sample_seed="seed-b", sample_size=1, agreements=1, disagreements=0,
                                                 disagreement_refs=[])
    d["supersession"] = {"supersedes": None, "superseded_by": None, "revalidation": {"blocked": False, "triggers_fired": []}}

    identity_digest = digest(d["identity"])
    anchor_payload = {
        "snapshot_sha256": plan.snapshot_hashes[0],
        "anchor_sha256": "9" * 64,
        "answer_sha256": d["output"]["artefact_hash"],
        "query_ref": req.input_refs[-1],
    }
    anchor_source_ref = await r.record(k.receipt("observation", {
        "category": "anchor",
        "context_sha256": identity_digest,
        "claim_sha256": digest(anchor_payload),
        "evidence_mode": "measured",
    }, signer="anchorer", request=req))

    sections = {
        "inputs": d["inputs"],
        "measurements": {"limits": d["limits"], "usage": d["usage"]},
        "manifest": d["output"],
        "runtime": d["runtime"],
        "independence": d["evidence"]["re_performance"],
        "retrieval": d["evidence"]["retrieval"],
        "refusal": d["evidence"]["refusal_demonstration"],
        "revalidation": d["supersession"],
        "acceptance": d["evidence"]["acceptance_script"],
        "skill": {"inputs": d["inputs"], "output": d["output"]},
    }
    signers = {
        "runtime": "worker",
        "measurements": "worker",
        "retrieval": "retriever",
        "independence": "sampler",
        "refusal": "refusal-checker",
        "skill": "skill-inspector",
        "inputs": "inputs-inspector",
        "manifest": "manifest-inspector",
        "revalidation": "revalidation-inspector",
        "acceptance": "acceptance-inspector",
    }
    refs = {}
    for name, value in sections.items():
        claims = {
            "category": name,
            "context_sha256": identity_digest,
            "claim_sha256": claim_digest(value),
            "evidence_mode": "measured",
            "terminal": name in {"runtime", "measurements"},
        }
        if name == "measurements":
            claims.update(
                reservation_ref=reserved,
                quantities=[{**q.model_dump(), "quantity": "0"} for q in plan.limits],
            )
        if name == "skill":
            claims["grounding"] = Grounding(
                query_ref=req.input_refs[-1],
                answer_sha256=d["output"]["artefact_hash"],
                anchors=(
                    {
                        "snapshot_sha256": plan.snapshot_hashes[0],
                        "anchor_sha256": "9" * 64,
                        "source_receipt_ref": anchor_source_ref,
                    },
                ),
                context_lost=False,
                context_loss_disclosed=False,
            ).model_dump(mode="json")
        if name == "refusal":
            claims["refusal"] = Refusal(
                request_ref=request_ref,
                outcome="refused",
                reason_code="OUT_OF_SCOPE",
            ).model_dump(mode="json")
            claims["source_receipt_refs"] = (request_ref,)
        refs[name] = await r.record(k.receipt("observation", claims, signer=signers[name], request=req))

    d["evidence"]["receipt_refs"] = [refs[name] for name in refs if name != "measurements"]
    d["evidence"]["retrieval"]["receipt_ref"] = refs["retrieval"]
    d["evidence"]["refusal_demonstration"]["receipt_ref"] = refs["refusal"]
    d["usage"]["metered_event_refs"] = [refs["measurements"]]
    await Reservations(r).settle(reserved, refs["measurements"])
    d["issuer"]["verifier_head_hash"] = (await r.events())[-1]["row"]["hash"]
    d["issuer"]["signature"] = await r.record(k.receipt("certificate", {
        "certificate_sha256": certificate_signing_digest(d),
    }, signer="issuer", request=req, issued_epoch=k.now))
    return d, req


async def _training_chain(estate, invalid_eval_ack=False, eval_meter_mode="valid"):
    k, r, _ = estate
    k.permission_override = _permissions()
    standard, acceptance, card = evaluation_fixture()
    req = Request(
        request_id="REQ-SYNTHETIC-TRAINING",
        tenant_id="tenant-SYNTHETIC",
        principal_id="operator",
        kind="training",
        engine="targeta",
        objective_sha256="c" * 64,
        input_refs=("akki://TEST/training-set", "akki://TEST/labels"),
        scope_refs=("source-scope",),
        deadline_epoch=k.now + 900,
    )
    standard_ref = await r.record(k.receipt("observation", {
        "category": "evaluation",
        "context_sha256": req.digest(),
        "claim_sha256": digest({"standard": "moac-six-criterion"}),
        "evidence_mode": "measured",
    }, signer="criterion-store", request=req))
    standard = standard.model_copy(update={"standard_ref": standard_ref})
    acceptance["acceptance_standard_ref"] = standard_ref
    plan, plan_ref, approvals = await _record_plan(
        estate,
        req,
        purposes=("training", "evaluation"),
        purpose_groups=(
            {"group": "training-group", "purpose": "training", "members": ["training-person"], "quorum": 1},
            {"group": "evaluation-group", "purpose": "evaluation", "members": ["evaluation-person"], "quorum": 1},
        ),
        worker_kinds=("training",),
        evaluation_standard=standard,
    )

    journal = LedgerJournal(r.db)
    await journal.append(req, "request", {"request_sha256": req.digest(), "request": req.model_dump(mode="json")})
    reserved = await Reservations(r).reserve(plan, plan_ref)
    dispatch = await journal.append(req,"dispatch",{"action":"submit","operation_key":"TEST-operation-training"})
    envelope = {
        "protocol": "akki.runtime.limits/1",
        "request_sha256": req.digest(),
        "plan_ref": plan_ref,
        "reservation_ref": reserved,
        "runtime_id": "worker-SYNTHETIC",
        "operation_key": "TEST-operation-training",
        "fence": dispatch["seq"],
        "limits": [q.model_dump() for q in plan.limits],
        "starts_epoch": k.now - 1,
        "stop_work_by_epoch": k.now + 95,
        "terminate_by_epoch": k.now + 99,
    }
    ack = await r.record(k.receipt("observation", {
        "category": "runtime",
        "context_sha256": req.digest(),
        "claim_sha256": digest(envelope),
        "evidence_mode": "measured",
    }, signer="worker", request=req))
    await journal.append(req, "runtime_limits", {"envelope": envelope, "ack_ref": ack})
    await journal.append(req, "send", {"action": "submit", "operation_key": "TEST-operation-training", "fence": dispatch["seq"]})

    artifact_hash = "d" * 64
    artifact_ref = "akki://TEST/trained-model"
    worker_result = WorkerResult(
        operation_key="TEST-operation-training",
        fence=dispatch["seq"],
        request_sha256=req.digest(),
        executor_id="worker",
        state="complete",
        receipt_ref="akki://TEST/worker-terminal-training",
        evidence_mode="measured",
        artifacts=(Artifact(ref=artifact_ref, sha256=artifact_hash, size_bytes=1,
                            tenant_id=req.tenant_id, class_label="non_factual"),),
        usage=(Usage(unit="GPU_hour", quantity="0"),),
    )
    await journal.append(req, "worker_outcome", {"result": worker_result.model_dump(mode="json")})
    await journal.append(req, "observation:" + digest(worker_result.model_dump(mode="json")), {"result": worker_result.model_dump(mode="json")})
    await journal.append(req, "registry", {
        "evidence_mode": "measured",
        "artifacts": [{"ref": artifact_ref, "sha256": artifact_hash}],
        "records": [{"receipt_id": "SYNTHETIC-native-registry-training"}],
    })
    await journal.append(req, "metered", {"evidence_mode": "measured", "terms_ref":plan.terms_ref, "usage": [{"unit": "GPU_hour", "quantity": "0"}]})
    await journal.append(req, "terminal", {"evidence_mode": "measured", "phase": "ready"})

    eval_req = Request(
        request_id="REQ-SYNTHETIC-EVALUATION",
        tenant_id="tenant-SYNTHETIC",
        principal_id="operator",
        kind="evaluation",
        engine="targeta",
        objective_sha256="9" * 64,
        input_refs=(artifact_ref, "akki://TEST/heldout"),
        scope_refs=("source-scope",),
        deadline_epoch=k.now + 900,
    )
    eval_journal = LedgerJournal(r.db)
    await eval_journal.append(eval_req, "request", {"request_sha256": eval_req.digest(), "request": eval_req.model_dump(mode="json")})
    eval_plan, eval_plan_ref, _ = await _record_plan(estate, eval_req, purposes=("evaluation",),
        purpose_groups=({"group":"evaluation-group","purpose":"evaluation","members":["evaluation-person"],"quorum":1},),
        worker_kinds=("evaluation",), evaluation_standard=standard, worker_signer="evaluator", allocation_capacity="200")
    eval_reservation = await Reservations(r).reserve(eval_plan, eval_plan_ref)
    eval_dispatch = await eval_journal.append(eval_req, "dispatch", {"action":"submit","operation_key":"TEST-operation-eval"})
    eval_envelope = {"protocol":"akki.runtime.limits/1","request_sha256":eval_req.digest(),"plan_ref":eval_plan_ref,
        "reservation_ref":eval_reservation,"runtime_id":"evaluator-SYNTHETIC","operation_key":"TEST-operation-eval",
        "fence":eval_dispatch["seq"],"limits":[q.model_dump() for q in eval_plan.limits],"starts_epoch":k.now,
        "stop_work_by_epoch":k.now+95,"terminate_by_epoch":k.now+100}
    eval_ack = await r.record(k.receipt("observation",{"category":"runtime","context_sha256":eval_req.digest(),
        "claim_sha256":"0"*64 if invalid_eval_ack else digest(eval_envelope),"evidence_mode":"measured"},signer="evaluator",request=eval_req))
    await eval_journal.append(eval_req,"runtime_limits",{"envelope":eval_envelope,"ack_ref":eval_ack})
    await eval_journal.append(eval_req,"send",{"action":"submit","operation_key":"TEST-operation-eval","fence":eval_dispatch["seq"]})
    evaluation_result = WorkerResult(
        operation_key="TEST-operation-eval",
        fence=eval_dispatch["seq"],
        request_sha256=eval_req.digest(),
        executor_id="evaluator",
        state="complete",
        receipt_ref="akki://TEST/evaluation-terminal",
        evidence_mode="measured",
        artifacts=(Artifact(ref="akki://TEST/evaluation-report", sha256="8" * 64, size_bytes=1,
                            tenant_id=req.tenant_id, class_label="non_factual"),),
        usage=(Usage(unit="GPU_hour", quantity="0"),),
    )
    await eval_journal.append(eval_req, "observation:" + digest(evaluation_result.model_dump(mode="json")), {"result": evaluation_result.model_dump(mode="json")})
    await eval_journal.append(eval_req,"worker_outcome",{"result":evaluation_result.model_dump(mode="json")})
    await eval_journal.append(eval_req, "registry", {
        "evidence_mode": "measured",
        "artifacts": [{"ref": "akki://TEST/evaluation-report", "sha256": "8" * 64}],
        "records": [{"receipt_id": "SYNTHETIC-native-registry-evaluation"}],
    })
    if eval_meter_mode != "missing":
        await eval_journal.append(eval_req,"metered",{"evidence_mode":"measured",
            "terms_ref":"wrong-terms" if eval_meter_mode=="wrong_terms" else eval_plan.terms_ref,
            "usage":[v.model_dump() for v in evaluation_result.usage]})
    eval_measurement = await r.record(k.receipt("observation",{"category":"measurements","context_sha256":eval_req.digest(),
        "claim_sha256":digest({"evaluation_usage":"SYNTHETIC"}),"evidence_mode":"measured","terminal":True,
        "reservation_ref":eval_reservation,"quantities":[{**q.model_dump(),"quantity":"0"} for q in eval_plan.limits]},
        signer="evaluator",request=eval_req))
    await Reservations(r).settle(eval_reservation,eval_measurement)
    await eval_journal.append(eval_req, "terminal", {"evidence_mode": "measured", "phase": "ready"})

    d = _base_doc("C_training_with_evaluation", req, k.now)
    d["authority"]["purposes_authorised"] = ["training", "evaluation"]
    approval_by_group = await _approval_map(r, approvals, req.digest())
    for key, group_name in (("scope", "scope-group"), ("expenditure", "spend-group")):
        g = next(v for v in plan.groups if v.group == group_name)
        approval_ref = approval_by_group[group_name]
        d["authority"][key] = {
            "group": g.group,
            "rule": "any_one",
            "decisions": [{
                "principal_id": g.members[0],
                "decision": "approved",
                "reason": "SYNTHETIC approval",
                "recorded_at": _iso(k.now - 1),
                "receipt_ref": approval_ref,
            }],
        }
    d["authority"]["purpose_specific"] = []
    for purpose_group in ("training-group", "evaluation-group"):
        g = next(v for v in plan.groups if v.group == purpose_group)
        approval_ref = approval_by_group[purpose_group]
        d["authority"]["purpose_specific"].append({
            "group": g.group,
            "rule": "any_one",
            "decisions": [{
                "principal_id": g.members[0],
                "decision": "approved",
                "reason": "SYNTHETIC approval",
                "recorded_at": _iso(k.now - 1),
                "receipt_ref": approval_ref,
            }],
        })

    criterion_ref = await r.record(k.receipt("observation", {
        "category": "evaluation",
        "context_sha256": req.digest(),
        "claim_sha256": digest({"criterion": "native-measurements"}),
        "evidence_mode": "measured",
    }, signer="criterion-store", request=req))
    prereq_ref = await r.record(k.receipt("observation", {
        "category": "evaluation",
        "context_sha256": req.digest(),
        "claim_sha256": digest({"prerequisite": "domain-governance"}),
        "evidence_mode": "measured",
    }, signer="criterion-store", request=req))

    d["release_acceptance"] = {
        "decision": "admitted",
        "recorded_at": _iso(k.now),
        "acceptance_standard_ref": acceptance["acceptance_standard_ref"],
        "criteria": [{**row, "measurement_ref": criterion_ref} for row in acceptance["criteria"]],
        "prerequisites": [{
            "prerequisite_id": "domain-governance-c",
            "extension_version": "ext-2.3",
            "outcome": "met",
            "record_ref": prereq_ref,
        }],
    }
    d["inputs"].update(
        snapshot_hashes=list(plan.snapshot_hashes),
        dial_versions=plan.dial_versions,
        policy_versions=plan.policy_versions,
        custody_classes_in_scope=["uncontrolled"],
        held_out_ref={
            "custodian_principal_id": "custodian-c",
            "split_protocol": "chronological",
            "seed": "seed-c",
            "fixed_before_training_at": _iso(standard.fixed_epoch),
            "selection_hash": standard.held_out_manifest_sha256,
        },
    )
    d["limits"]["dimensions"] = [
        {"dimension": "spend", "unit": "USD", "effective_limit": 7.0, "observed": 0.0,
         "source": "owner_run_limit", "enforced_by": "worker-SYNTHETIC"},
        {"dimension": "wall_clock", "unit": "seconds", "effective_limit": 100.0, "observed": 0.0,
         "source": "owner_run_limit", "enforced_by": "worker-SYNTHETIC"},
    ]
    model_licence_ref = await r.record(k.receipt("observation", {
        "category": "inputs",
        "context_sha256": req.digest(),
        "claim_sha256": digest({"licence": "training-model-licence"}),
        "evidence_mode": "measured",
    }, signer="licensor", request=req))
    recipe_ref = await r.record(k.receipt("observation", {
        "category": "inputs",
        "context_sha256": req.digest(),
        "claim_sha256": digest({"recipe": "training-recipe"}),
        "evidence_mode": "measured",
    }, signer="licensor", request=req))
    d["runtime"].update(
        admitted_runtime_id="worker-SYNTHETIC",
        executor_version="test-1",
        model_refs=[{
            "registry_id": "registry_model_training_1",
            "hash": "4" * 64,
            "version": "v2.0.0",
            "licence_ref": model_licence_ref,
        }],
        recipe_ref=recipe_ref,
        implementation_workspace_touched_data=False,
    )
    d["output"].update(
        artefact_hash=artifact_hash,
        registry_entry_id="SYNTHETIC-native-registry-training",
        manifest_hash="7" * 64,
        manifest_row_count=2,
        denominator_count=2,
        reconciliation={"processed": 1, "refused_with_reason": 1, "unmeasured_with_reason": 0, "unaccounted": 0},
    )
    d["usage"].update(
        terms_identifier=plan.terms_ref,
        measured_quantities=[{"unit": "GPU_hour", "quantity": 0.0, "measured_by": "worker-SYNTHETIC"}],
        reservation_ref=reserved,
        reconciled_against_reservation=True,
    )
    d["evidence"]["retrieval"].update(principal_id="retriever", retrieved_at=_iso(k.now), receipt_ref="")
    d["evidence"]["refusal_demonstration"] = {
        "kind": "unauthorised_manifest_unit",
        "request_ref": criterion_ref,
        "reason_stated": "Synthetic refusal proof",
        "receipt_ref": "",
    }
    d["evidence"]["acceptance_script"].update(script_hash=plan.acceptance_script_sha256, written_before_run_at=_iso(k.now - 2), result="pass")
    d["evidence"]["re_performance"].update(second_instance_id="instance-c", different_model_family=True,
                                                 sample_seed="seed-c", sample_size=1, agreements=1, disagreements=0,
                                                 disagreement_refs=[])
    d["supersession"] = {"supersedes": None, "superseded_by": None, "revalidation": {"blocked": False, "triggers_fired": []}}

    identity_digest = digest(d["identity"])
    sections = {
        "inputs": d["inputs"],
        "measurements": {"limits": d["limits"], "usage": d["usage"]},
        "manifest": d["output"],
        "runtime": d["runtime"],
        "independence": d["evidence"]["re_performance"],
        "retrieval": d["evidence"]["retrieval"],
        "refusal": d["evidence"]["refusal_demonstration"],
        "revalidation": d["supersession"],
        "acceptance": d["evidence"]["acceptance_script"],
        "training": {"inputs": d["inputs"], "output": d["output"]},
        "evaluation": d["release_acceptance"],
        "release": d["release_acceptance"],
    }
    signers = {
        "runtime": "worker",
        "measurements": "worker",
        "training": "worker",
        "retrieval": "retriever",
        "independence": "sampler",
        "evaluation": "evaluator",
        "release": "release-board",
        "refusal": "refusal-checker",
        "inputs": "inputs-inspector",
        "manifest": "manifest-inspector",
        "revalidation": "revalidation-inspector",
        "acceptance": "acceptance-inspector",
    }
    refs = {}
    for name, value in sections.items():
        claims = {
            "category": name,
            "context_sha256": identity_digest,
            "claim_sha256": claim_digest(value),
            "evidence_mode": "measured",
            "terminal": name in {"runtime", "measurements"},
        }
        if name == "measurements":
            claims.update(
                reservation_ref=reserved,
                quantities=[{**q.model_dump(), "quantity": "0"} for q in plan.limits],
            )
        if name == "refusal":
            claims["refusal"] = Refusal(
                request_ref=criterion_ref,
                outcome="refused",
                reason_code="UNAUTHORISED_MANIFEST_UNIT",
            ).model_dump(mode="json")
            claims["source_receipt_refs"] = (criterion_ref,)
        if name == "evaluation":
            claims["evaluation"] = Evaluation(
                evaluation_request_id=eval_req.request_id,
                training_request_sha256=req.digest(),
                candidate_artifact_sha256=d["output"]["artefact_hash"],
                held_out_manifest_sha256=standard.held_out_manifest_sha256,
                moac_card=card,
            ).model_dump(mode="json")
        refs[name] = await r.record(k.receipt("observation", claims, signer=signers[name], request=req))

    d["evidence"]["receipt_refs"] = [refs[name] for name in refs if name != "measurements"]
    d["evidence"]["retrieval"]["receipt_ref"] = refs["retrieval"]
    d["evidence"]["refusal_demonstration"]["receipt_ref"] = refs["refusal"]
    d["usage"]["metered_event_refs"] = [refs["measurements"]]
    await Reservations(r).settle(reserved, refs["measurements"])
    d["issuer"]["verifier_head_hash"] = (await r.events())[-1]["row"]["hash"]
    d["issuer"]["signature"] = await r.record(k.receipt("certificate", {
        "certificate_sha256": certificate_signing_digest(d),
    }, signer="issuer", request=req, issued_epoch=k.now))
    return d, req


async def _resign(estate, req: Request, d: dict):
    k, r, _ = estate
    d["issuer"]["verifier_head_hash"] = (await r.events())[-1]["row"]["hash"]
    d["issuer"]["issued_at"] = _iso(k.now)
    d["issuer"]["signature"] = await r.record(k.receipt("certificate", {
        "certificate_sha256": certificate_signing_digest(d),
    }, signer="issuer", request=req, issued_epoch=k.now))


# Module/feature: native path-B skill chain verifies and issues from signed measured evidence.
def test_native_path_b_skill_positive_verify_and_issue(estate):
    async def run():
        d, _ = await _skill_chain(estate)
        _, r, _ = estate
        verdict = await NativeEvidence(r).verify(d, tenant_id=d["identity"]["tenant_id"], principal_id="operator")
        assert verdict.evidence_mode == "measured"
        result = await validate_certificate(
            d,
            tenant_id=d["identity"]["tenant_id"],
            principal_id="operator",
            evidence=NativeEvidence(r),
            timeout_seconds=5,
        )
        assert result.valid, result.issues
        _, ref = await issue_certificate(d, r, timeout_seconds=5)
        assert ref == (await issue_certificate(d, r, timeout_seconds=5))[1]

    with scope():
        asyncio.run(run())


@pytest.mark.parametrize('defect,expected',[
    ('ack','NATIVE_RUNTIME_ACK_NOT_PROVED'),
    ('missing_meter','EVALUATION_GOVERNED_EXECUTION_INCOMPLETE'),
    ('wrong_terms','EVALUATION_RESULT_OR_METERING_MISMATCH'),
    ('withdrawal','APPROVAL_GROUP_PENDING'),
])
def test_parent_certificate_requires_separately_governed_evaluation(estate,defect,expected):
    async def run():
        d,req=await _training_chain(estate,invalid_eval_ack=defect=='ack',
            eval_meter_mode='missing' if defect=='missing_meter' else 'wrong_terms' if defect=='wrong_terms' else 'valid')
        k,r,_=estate
        if defect=='withdrawal':
            rows=await r.events()
            target=next(e for e in rows if e['payload'].get('receipt',{}).get('kind')=='approval'
                and e['payload']['receipt'].get('request_sha256')!=req.digest()
                and e['payload']['receipt']['claims']['group']=='evaluation-group')
            await r.record(k.receipt('revocation',{'target_ref':target['row']['hash'],'reason_code':'SYNTHETIC_WITHDRAWAL'}))
            await _resign(estate,req,d)
        result=await validate_certificate(d,tenant_id=req.tenant_id,principal_id='operator',evidence=NativeEvidence(r),timeout_seconds=5)
        assert not result.valid and any(v.code==expected for v in result.issues),result.issues
        with pytest.raises(Held): await issue_certificate(d,r,timeout_seconds=5)
    with scope(): asyncio.run(run())


# Module/feature: native path-C training+independent evaluation chain verifies and issues end-to-end.
def test_native_path_c_training_with_evaluation_positive_verify_and_issue(estate):
    async def run():
        d, _ = await _training_chain(estate)
        _, r, _ = estate
        verdict = await NativeEvidence(r).verify(d, tenant_id=d["identity"]["tenant_id"], principal_id="operator")
        assert verdict.evidence_mode == "measured"
        result = await validate_certificate(
            d,
            tenant_id=d["identity"]["tenant_id"],
            principal_id="operator",
            evidence=NativeEvidence(r),
            timeout_seconds=5,
        )
        assert result.valid, result.issues
        _, ref = await issue_certificate(d, r, timeout_seconds=5)
        assert ref == (await issue_certificate(d, r, timeout_seconds=5))[1]

    with scope():
        asyncio.run(run())


@pytest.mark.parametrize("path_name", ["B_callable_skill", "C_training_with_evaluation"])
def test_native_path_bc_freshly_resigned_semantic_negatives_fail_without_signature_staleness(estate, path_name):
    async def run():
        d, req = await (_skill_chain(estate) if path_name == "B_callable_skill" else _training_chain(estate))
        if path_name == "B_callable_skill":
            d["authority"]["purposes_authorised"] = ["training"]
            expected = "PURPOSE_NOT_AUTHORISED"
        else:
            now_epoch = int(datetime.now(timezone.utc).timestamp())
            d["inputs"]["held_out_ref"]["fixed_before_training_at"] = _iso(now_epoch)
            expected = "HELDOUT_NOT_FROZEN_BEFORE_RUN"
        await _resign(estate, req, d)
        _, r, _ = estate
        result = await validate_certificate(
            d,
            tenant_id=d["identity"]["tenant_id"],
            principal_id="operator",
            evidence=NativeEvidence(r),
            timeout_seconds=5,
        )
        assert not result.valid
        assert any(issue.code == expected for issue in result.issues)
        assert all(issue.code != "CERTIFICATE_SIGNATURE_BINDING_MISMATCH" for issue in result.issues)
        with pytest.raises(Held):
            await issue_certificate(d, r, timeout_seconds=5)

    with scope():
        asyncio.run(run())