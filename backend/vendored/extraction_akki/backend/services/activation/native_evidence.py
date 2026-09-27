"""Concrete signature/receipt/native-journal verification, not client verdict flags."""
import json
from copy import deepcopy
from typing import Literal
from services.activation.evidence import EvidenceVerdict, CHECKS, reference_set
from services.activation.schema import canonical_document
from services.activation.approvals import approved_plan
from services.activation.record_shapes import Quantity, quantities
from services.northena.execution_models import Frozen, Hash, Request, Held
from services.ledger_writer.mongo_control import digest
from services.activation.model_proofs import Grounding, Evaluation, Refusal, verify_model_proofs


class Observation(Frozen):
    category: Literal["anchor", "release", "inputs", "measurements", "manifest", "independence", "retrieval", "refusal",
                      "revalidation", "acceptance", "runtime", "training", "evaluation", "skill"]
    context_sha256: Hash
    claim_sha256: Hash
    evidence_mode: Literal["measured", "MOCKED"]
    reservation_ref: Hash | None = None
    quantities: tuple[Quantity, ...] = ()
    terminal: bool = False
    source_receipt_refs: tuple[Hash, ...] = ()
    grounding: Grounding | None = None
    evaluation: Evaluation | None = None
    refusal: Refusal | None = None


class CertificateSeal(Frozen):
    certificate_sha256: Hash


def certificate_signing_digest(document):
    value = deepcopy(document)
    value["issuer"].pop("signature", None)
    return canonical_document(value)[1]


def claim_digest(value):
    """Exclude only receipt backlink fields to avoid a self-referential digest.

    All referenced receipts are independently resolved below. Other references,
    measurements, registry IDs, names and times remain in the commitment.
    """
    def clean(v):
        if isinstance(v, dict):
            return {k: clean(c) for k, c in v.items() if k not in {
                "receipt_ref", "receipt_refs", "metered_event_refs"}}
        return [clean(c) for c in v] if isinstance(v, list) else v
    return digest(clean(value))


class NativeEvidence:
    def __init__(self, receipts):
        self.receipts = receipts

    async def verify(self, d, *, tenant_id, principal_id):
        events = await self.receipts.events()
        identity = d["identity"]
        issued = [e for e in events if e["row"]["resource_type"] == "activation_certificate"]
        if any(e["payload"]["certificate"]["supersession"]["supersedes"] == d["certificate_id"] for e in issued):
            raise Held("CERTIFICATE_SUPERSEDED")
        if d["supersession"]["supersedes"]:
            prior = [e for e in issued if e["payload"]["certificate"]["certificate_id"] == d["supersession"]["supersedes"]
                     and e["payload"].get("principal_id") == principal_id]
            if len(prior) != 1 or prior[0]["payload"]["certificate"]["identity"]["path"] != identity["path"]:
                raise Held("CERTIFICATE_SUPERSESSION_TARGET_UNRESOLVED")
        requests = [e for e in events if e["row"]["resource_type"] == "execution_flow" and
                    e["payload"].get("slot") == "request" and
                    e["row"]["run_id"] == identity["frozen_request_id"] and
                    e["payload"].get("principal_id") == principal_id]
        if len(requests) != 1:
            raise Held("CERTIFICATE_NATIVE_REQUEST_UNRESOLVED")
        request = Request.model_validate_json(json.dumps(requests[0]["payload"]["data"]["request"]))
        path_kind = {"A_source_to_registry": "source", "B_callable_skill": "skill", "C_training_with_evaluation": "training"}
        if (request.objective_sha256 != identity["frozen_objective_hash"] or request.tenant_id != tenant_id
                or request.kind != path_kind[identity["path"]]):
            raise Held("CERTIFICATE_NATIVE_REQUEST_MISMATCH")
        plan, plan_ref, approval_refs, expiry, _ = await approved_plan(self.receipts, request)
        # Correct owner mappings: these are INPUTS, never policy_and_dials.
        if (d["inputs"]["dial_versions"] != plan.dial_versions or
                d["inputs"]["policy_versions"] != plan.policy_versions or
                d["usage"]["terms_identifier"] != plan.terms_ref):
            raise Held("CERTIFICATE_EFFECTIVE_POLICY_MISMATCH")
        if (tuple(d["inputs"]["snapshot_hashes"]) != plan.snapshot_hashes or
                d["evidence"]["acceptance_script"]["script_hash"] != plan.acceptance_script_sha256):
            raise Held("CERTIFICATE_PREDECLARED_INPUT_OR_ACCEPTANCE_MISMATCH")
        if (set(d["authority"]["purposes_authorised"]) != set(plan.purposes)
                or d["authority"]["standing_approval_ref"] is not None):
            raise Held("CERTIFICATE_PURPOSE_AUTHORITY_MISMATCH")
        groups = [d["authority"]["scope"], d["authority"]["expenditure"], *d["authority"]["purpose_specific"]]
        declared = {g["group"] for g in groups}
        if declared != {g.group for g in plan.groups}:
            raise Held("CERTIFICATE_APPROVAL_GROUP_MISMATCH")
        from datetime import datetime
        for group in groups:
            effective = next(g for g in plan.groups if g.group == group["group"])
            if group["rule"] != ("any_one" if effective.quorum == 1 else "quorum"):
                raise Held("CERTIFICATE_APPROVAL_RULE_MISMATCH")
            for decision in group["decisions"]:
                original = await self.receipts.resolve(decision["receipt_ref"], kind="approval",
                    request_sha256=request.digest(), events=events)
                if (original.signer_id != decision["principal_id"] or
                        original.claims["decision"] != decision["decision"] or
                        original.claims["reason"] != decision["reason"] or
                        original.claims["group"] != group["group"] or
                        datetime.fromisoformat(decision["recorded_at"].replace("Z", "+00:00")).timestamp() != original.issued_epoch):
                    raise Held("CERTIFICATE_APPROVAL_ATTRIBUTION_MISMATCH")
        declared_refs = {v["receipt_ref"] for g in groups for v in g["decisions"] if v["decision"] == "approved"}
        if declared_refs != set(approval_refs):
            raise Held("CERTIFICATE_APPROVAL_RECEIPTS_MISMATCH")
        expected_limits = quantities(plan.limits)
        from decimal import Decimal
        actual_limits = {(q["dimension"], q["unit"]): Decimal(str(q["effective_limit"])) for q in d["limits"]["dimensions"]}
        if expected_limits != actual_limits:
            raise Held("CERTIFICATE_EFFECTIVE_LIMIT_MISMATCH")
        seal = await self.receipts.resolve(d["issuer"]["signature"], kind="certificate",
            request_sha256=request.digest(), events=events)
        if (seal.signer_id != d["issuer"]["principal_id"] or
                CertificateSeal.model_validate(seal.claims).certificate_sha256 != certificate_signing_digest(d)):
            raise Held("CERTIFICATE_SIGNATURE_BINDING_MISMATCH")
        if d["issuer"]["verifier_head_hash"] not in {e["row"]["hash"] for e in events}:
            raise Held("CERTIFICATE_VERIFIER_HEAD_UNRESOLVED")
        seal_event = next(e for e in events if e["row"]["hash"] == d["issuer"]["signature"])
        head_event = next(e for e in events if e["row"]["hash"] == d["issuer"]["verifier_head_hash"])
        if (head_event["row"]["seq"] >= seal_event["row"]["seq"] or
                datetime.fromisoformat(d["issuer"]["issued_at"].replace("Z", "+00:00")).timestamp() != seal.issued_epoch):
            raise Held("CERTIFICATE_SIGNING_CHRONOLOGY_MISMATCH")
        sections = {
            "inputs": d["inputs"],
            "measurements": {"limits": d["limits"], "usage": d["usage"]},
            "manifest": d["output"], "runtime": d["runtime"],
            "independence": d["evidence"]["re_performance"],
            "retrieval": d["evidence"]["retrieval"],
            "revalidation": d["supersession"], "acceptance": d["evidence"]["acceptance_script"],
        }
        if d["evidence"]["refusal_demonstration"] is not None:
            sections["refusal"] = d["evidence"]["refusal_demonstration"]
        if request.kind in {"skill", "training"}:
            sections["skill" if request.kind == "skill" else "training"] = {"inputs": d["inputs"], "output": d["output"]}
        if request.kind == "training":
            sections["evaluation"] = d["release_acceptance"]
            sections["release"] = d["release_acceptance"]
        proof_refs = set(d["evidence"]["receipt_refs"]) | set(d["usage"]["metered_event_refs"])
        proofs = {}
        for ref in proof_refs:
            receipt = await self.receipts.resolve(ref, kind="observation", request_sha256=request.digest(), events=events)
            proof = Observation.model_validate_json(json.dumps(receipt.claims))
            if proof.evidence_mode != "measured" or proof.context_sha256 != digest(identity):
                raise Held("CERTIFICATE_OBSERVATION_UNMEASURED_OR_WRONG_RUN")
            if proof.category in proofs:
                raise Held("CERTIFICATE_OBSERVATION_AMBIGUOUS")
            proofs[proof.category] = (proof, receipt)
            for source_ref in proof.source_receipt_refs:
                await self.receipts.resolve(source_ref, events=events)
            expiry = min(expiry, receipt.expires_epoch)
        for category, section in sections.items():
            if category not in proofs or proofs[category][0].claim_sha256 != claim_digest(section):
                raise Held("CERTIFICATE_" + category.upper() + "_PROOF_MISMATCH")
        worker = await self.receipts.resolve(plan.worker_ref, kind="worker", events=events)
        if (worker.claims["runtime_id"] != d["runtime"]["admitted_runtime_id"] or
                worker.claims["executor_version"] != d["runtime"]["executor_version"]):
            raise Held("CERTIFICATE_RUNTIME_ADMISSION_MISMATCH")
        for category in ("runtime", "measurements"):
            if proofs[category][1].signer_id != worker.signer_id:
                raise Held("CERTIFICATE_WORKER_PROVENANCE_MISMATCH")
        if request.kind == "training" and proofs["training"][1].signer_id != worker.signer_id:
            raise Held("CERTIFICATE_TRAINER_PROVENANCE_MISMATCH")
        if not proofs["runtime"][0].terminal:
            raise Held("CERTIFICATE_RUNTIME_TERMINATION_UNPROVED")
        if proofs["independence"][1].signer_id in {worker.signer_id, request.principal_id}:
            raise Held("CERTIFICATE_INDEPENDENT_PRODUCER_REQUIRED")
        if proofs["retrieval"][1].signer_id != d["evidence"]["retrieval"]["principal_id"]:
            raise Held("CERTIFICATE_RETRIEVER_PROVENANCE_MISMATCH")
        if "evaluation" in proofs and proofs["evaluation"][1].signer_id == proofs["training"][1].signer_id:
            raise Held("CERTIFICATE_INDEPENDENT_EVALUATION_REQUIRED")
        from services.activation.native_joins import verify_native_completion
        native_refs = verify_native_completion(events, request, d, proofs)
        await verify_model_proofs(self.receipts, events, request, plan, d, proofs)
        verified = set(approval_refs) | native_refs | {plan_ref, plan.terms_ref}
        for ref in reference_set(d) - verified:
            referenced = await self.receipts.resolve(ref, events=events)
            if referenced.request_sha256 not in (None, request.digest()) or not set(request.scope_refs) <= set(referenced.scope_refs):
                raise Held("CERTIFICATE_REFERENCE_SCOPE_MISMATCH")
            verified.add(ref)
        proof_events = [e for e in events if e["row"]["hash"] in verified]
        if any(e["row"]["seq"] > head_event["row"]["seq"] for e in proof_events):
            raise Held("CERTIFICATE_PROOF_AFTER_VERIFIER_HEAD")
        latest = await self.receipts.events()
        if [e["row"]["hash"] for e in latest] != [e["row"]["hash"] for e in events]:
            raise Held("CERTIFICATE_EVIDENCE_PREFIX_CHANGED")
        return EvidenceVerdict(certificate_sha256=canonical_document(d)[1], tenant_id=tenant_id,
            principal_id=principal_id, verified_refs=tuple(sorted(verified)), evidence_mode="measured",
            expires_epoch=min(expiry, seal.expires_epoch), **{k: True for k in CHECKS})