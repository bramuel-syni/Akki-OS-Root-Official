"""Hash-bound command identity without changing the frozen Ledger row."""
from services.ledger_writer.mongo_control import digest

COMMAND_KEY = "_control_command"
IDENTITY_FIELDS = ("tenant_id", "actor_id", "run_id", "event_type", "resource_type",
                   "decision", "reason_code")


class CommandConflict(ValueError):
    """A command key cannot authorize a different immutable operation."""


def fingerprint(row, payload):
    intent = {key: value for key, value in payload.items() if key != COMMAND_KEY}
    # DAP's producer hashes exact frozen user intent; timestamps are not intent.
    if (row["resource_type"] == "dap_request"
            and row["event_type"] == "dap.request.commissioned" and "body_hash" in intent):
        intent = {"body_hash": intent["body_hash"]}
    return digest({"row": {key: row[key] for key in IDENTITY_FIELDS}, "intent": intent})


def verify_command(event):
    marker = event["payload"].get(COMMAND_KEY)
    if marker is None:
        if COMMAND_KEY in event["payload"]:
            raise ValueError("Invalid command identity metadata.")
        return  # Historical records are read unchanged, never retrofitted.
    if (not isinstance(marker, dict) or set(marker) != {"id", "fingerprint"}
            or marker["id"] != event["command_id"]
            or marker["fingerprint"] != fingerprint(event["row"], event["payload"])):
        raise ValueError("Command identity integrity check failed.")


def check_attribution(payload, principal, tenant):
    for key in ("principal_id", "actor_id", "actor"):
        if key in payload and payload[key] != principal:
            raise ValueError("Payload principal conflicts with propagated context.")
    if "tenant_id" in payload and payload["tenant_id"] != tenant:
        raise ValueError("Payload tenant conflicts with request scope.")