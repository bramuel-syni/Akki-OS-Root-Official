"""Reconstruct independent approval groups on every protected operation."""
import json
from services.activation.receipts import RESOURCE
from services.activation.record_shapes import Plan, Approval, Allocation, Worker
from services.northena.execution_models import Held


async def approved_plan(receipts, request):
    events = await receipts.events()
    candidates = [e for e in events if e["row"]["resource_type"] == RESOURCE and
                  e["payload"].get("receipt", {}).get("kind") == "plan" and
                  e["payload"]["receipt"].get("request_sha256") == request.digest()]
    if len(candidates) != 1:
        raise Held("ACTIVATION_PLAN_MISSING_OR_AMBIGUOUS")
    event = candidates[0]
    ref = event["row"]["hash"]
    receipt = await receipts.resolve(ref, kind="plan", request_sha256=request.digest(), events=events)
    plan = Plan.model_validate_json(json.dumps(receipt.claims))
    if plan.request != request:
        raise Held("ACTIVATION_REQUEST_MISMATCH")
    decisions, approval_refs, expiry = {}, [], receipt.expires_epoch
    groups = {g.group: g for g in plan.groups}
    for e in events:
        raw = e["payload"].get("receipt", {})
        if (e["row"]["resource_type"] != RESOURCE or raw.get("kind") != "approval"
                or raw.get("claims", {}).get("plan_ref") != ref):
            continue
        value = Approval.model_validate_json(json.dumps(raw["claims"]))
        group = groups.get(value.group)
        if group is None or raw.get("signer_id") not in group.members:
            raise Held("APPROVAL_GROUP_MEMBERSHIP_MISMATCH")
        # Only the latest decision by this principal in THIS group counts.
        decisions[(value.group, raw["signer_id"])] = (e, value)
    for group in plan.groups:
        approved = []
        for (name, principal), (e, value) in decisions.items():
            if name != group.group or value.decision != "approved":
                continue
            try:
                decision = await receipts.resolve(e["row"]["hash"], kind="approval",
                    request_sha256=request.digest(), events=events)
            except Held as exc:
                if exc.reason_code in {"RECEIPT_REVOKED", "SIGNER_OR_RECEIPT_NOT_CURRENT"}:
                    continue
                raise
            if decision.scope_refs != request.scope_refs or e["row"]["seq"] <= event["row"]["seq"]:
                raise Held("APPROVAL_SCOPE_OR_CHRONOLOGY_MISMATCH")
            approved.append((e["row"]["hash"], decision.expires_epoch))
        if len(approved) < group.quorum:
            raise Held("APPROVAL_GROUP_PENDING")
        approval_refs.extend(v[0] for v in approved)
        expiry = min(expiry, *(v[1] for v in approved))
    allocation_receipt = await receipts.resolve(plan.allocation_ref, kind="allocation", events=events)
    worker_receipt = await receipts.resolve(plan.worker_ref, kind="worker", events=events)
    allocation = Allocation.model_validate_json(json.dumps(allocation_receipt.claims))
    worker = Worker.model_validate_json(json.dumps(worker_receipt.claims))
    if (not set(request.scope_refs) <= set(allocation_receipt.scope_refs)
            or not set(request.scope_refs) <= set(worker_receipt.scope_refs)
            or allocation.terms_ref != plan.terms_ref):
        raise Held("ALLOCATION_OR_WORKER_SCOPE_MISMATCH")
    if (request.kind not in worker.kinds or
            not {q.dimension for q in plan.limits} <= set(worker.enforced_dimensions)):
        raise Held("RUNTIME_LIMITS_UNENFORCEABLE")
    return plan, ref, tuple(approval_refs), min(expiry, allocation_receipt.expires_epoch,
                                             worker_receipt.expires_epoch), events