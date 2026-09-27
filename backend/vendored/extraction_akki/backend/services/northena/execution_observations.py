"""Immutable terminal facts arbitrate concurrent observers on the canonical journal."""
import json
from services.ledger_writer.principal_control import CommandConflict
from services.northena.execution_models import Held, WorkerResult

TERMINAL_STATES = {"complete", "cancelled", "failed"}
OUTCOME_SLOTS = {"worker_outcome", "worker_terminal"}  # Read older checkpoints too.


def facts(result):
    return {key: value for key, value in result.items() if key != "receipt_ref"}


async def guard_terminal(journal, request, result, rows):
    value = result.model_dump(mode="json")
    previous = [r["data"]["result"] for r in rows if r["slot"].startswith("observation:")
                and r["data"]["result"]["state"] in TERMINAL_STATES]
    locked = next((r for r in rows if r["slot"] in OUTCOME_SLOTS), None)
    originals = ([locked["data"]["result"]] if locked else []) + previous
    # A delayed accepted/running response may arrive after a definitive result.
    # It is stale, not conflicting terminal evidence; keep the immutable outcome.
    if originals and value["state"] not in TERMINAL_STATES:
        value = originals[0]
    if originals and any(facts(v) != facts(value) for v in originals):
        raise Held("EXECUTOR_TERMINAL_OBSERVATION_CONFLICT")
    if value["state"] not in TERMINAL_STATES:
        return result
    original = originals[0] if originals else value
    try:
        if locked is None:
            await journal.append(request, "worker_outcome", {"result": original})
    except CommandConflict:
        winner = next(r for r in await journal.read(request) if r["slot"] in OUTCOME_SLOTS)
        if facts(winner["data"]["result"]) != facts(value):
            raise Held("EXECUTOR_TERMINAL_OBSERVATION_CONFLICT") from None
        original = winner["data"]["result"]
    return WorkerResult.model_validate_json(json.dumps(original))