"""Atomic outbox send claim, separate from a recoverable dispatch reservation."""
from uuid import uuid4
from services.ledger_writer.principal_control import CommandConflict
from services.northena.execution_models import Held

PROTOCOL = "acknowledged_v1"


async def claim_send(coordinator, request, executor, dispatch):
    rows = {r["slot"]: r for r in await coordinator.journal.read(request)}
    if "send" in rows:
        if rows["send"]["data"]["action"] == "cancel":
            raise Held("CANCELLED_BEFORE_SEND")
        return False, None
    if dispatch["data"].get("protocol") != PROTOCOL:
        return False, None  # Historical dispatch may already have executed.
    if "cancel_intent" in rows or "terminal" in rows:
        raise Held("CANCEL_OR_TERMINAL_BEFORE_DISPATCH")
    grant, commercial = await coordinator.prepare(request)
    if grant.model_dump(mode="json") != dispatch["data"]["authority"]:
        raise Held("AUTHORITY_CHANGED_BEFORE_DISPATCH")
    if commercial != dispatch["data"].get("commercial_snapshot"):
        raise Held("COMMERCIAL_TERMS_CHANGED_BEFORE_DISPATCH")
    eligibility = await coordinator.check_inputs(request, "dispatch")
    prepared = None
    if request.kind != "source" and coordinator.handoffs is not None:
        if getattr(executor, "delivery_rpc", None) is None:
            raise Held("DELIVERY_RPC_NOT_BOUND")
        prepared = await coordinator.handoffs.prepare(request, grant, dispatch)
    # Calls above can yield. Recheck current gates before claiming the effect.
    fresh_grant, fresh_commercial = await coordinator.prepare(request)
    if fresh_grant != grant or fresh_commercial != commercial:
        raise Held("AUTHORITY_OR_TERMS_CHANGED_BEFORE_SEND")
    eligibility = await coordinator.check_inputs(request, "send")
    if prepared:
        await coordinator.handoffs.revalidate(request, grant)
        if min(prepared[1].expires_epoch, prepared[2].expires_epoch) <= coordinator.clock():
            raise Held("HANDOFF_EXPIRED_BEFORE_SEND")
    if min(grant.expires_epoch, request.deadline_epoch) <= coordinator.clock():
        raise Held("AUTHORITY_EXPIRED_BEFORE_SEND")
    if eligibility and eligibility["data"]["receipt"]["expires_epoch"] <= coordinator.clock():
        raise Held("INPUT_ELIGIBILITY_EXPIRED")
    rows = await coordinator.journal.read(request)
    if any(r["slot"] in {"cancel_intent", "terminal"} for r in rows):
        raise Held("CANCEL_OR_TERMINAL_BEFORE_DISPATCH")
    data = {"action": "submit", "operation_key": dispatch["data"]["operation_key"],
            "fence": dispatch["seq"], "nonce": uuid4().hex}
    if prepared:
        if eligibility is None:
            raise Held("INPUT_ELIGIBILITY_NOT_RECORDED")
        data.update(handoff_ref=prepared[3]["hash"], ack_ref=prepared[4]["hash"],
                    eligibility_ref=eligibility["hash"])
    try:
        send = await coordinator.journal.append(request, "send", data)
    except CommandConflict:
        winner = next(r for r in await coordinator.journal.read(request) if r["slot"] == "send")
        if winner["data"]["action"] == "cancel":
            raise Held("CANCELLED_BEFORE_SEND")
        return False, None  # Losing caller only observes; never repeats initial submit.
    packet = None
    if prepared:
        packet = coordinator.handoffs.packet(request, grant, dispatch, *prepared[:3],
                                             data["handoff_ref"], data["ack_ref"], send["hash"],
                                             data["eligibility_ref"])
    return True, packet


async def cancel_unsent(coordinator, request, dispatch):
    if dispatch["data"].get("protocol") != PROTOCOL:
        return False
    try:
        row = await coordinator.journal.append(request, "send", {
            "action": "cancel", "operation_key": dispatch["data"]["operation_key"], "fence": dispatch["seq"]})
    except CommandConflict:
        row = next(r for r in await coordinator.journal.read(request) if r["slot"] == "send")
    return row["data"]["action"] == "cancel"