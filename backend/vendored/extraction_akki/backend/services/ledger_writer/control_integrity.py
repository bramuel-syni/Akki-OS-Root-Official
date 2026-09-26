"""Verified tenant prefix for control-plane consumers; no independent-head claim."""
import re
from copy import deepcopy

from contracts.ledger_v1 import LEDGER_ROW_FIELDS, LEDGER_SCHEMA_VERSION
from services.ledger_verifier.verify import verify_chain
from services.ledger_writer.mongo_control import COLLECTION, decode_row, verify_event
from services.ledger_writer.control_commands import verify_command


def checked_event(event):
    try:
        row, payload = event["row"], event["payload"]
        if (not isinstance(row, dict) or set(row) != set(LEDGER_ROW_FIELDS)
                or not isinstance(payload, dict)
                or not isinstance(event["command_id"], str) or not event["command_id"].strip()
                or row["schema_version"] != LEDGER_SCHEMA_VERSION
                or type(row["seq"]) is not int or row["seq"] < 1):
            raise ValueError("Invalid Ledger event shape.")
        for key in ("prev_hash", "hash", "payload_ref"):
            if not isinstance(row[key], str) or not re.fullmatch(r"[0-9a-f]{64}", row[key]):
                raise ValueError("Invalid Ledger hash field.")
        for key in ("tenant_id", "run_id", "task_id", "actor_id", "actor_type",
                    "event_type", "resource_type", "resource_id", "decision"):
            if not isinstance(row[key], str) or not row[key].strip():
                raise ValueError("Invalid Ledger identity field.")
        at = row["at"]
        if (not isinstance(at, dict) or set(at) != {"epoch_s", "source"}
                or type(at["epoch_s"]) is not int
                or at["source"] not in {"wall_clock", "reliable"}
                or not isinstance(row["reason_code"], str)
                or (row["break_glass_session_id"] is not None
                    and not isinstance(row["break_glass_session_id"], str))):
            raise ValueError("Invalid Ledger time or metadata field.")
        verify_event(event)
        verify_command(event)
        return deepcopy({key: event[key] for key in ("command_id", "row", "payload")})
    except (KeyError, TypeError, AttributeError, OverflowError) as exc:
        raise ValueError("Malformed authoritative Ledger event.") from exc


async def load_verified_prefix(db, tenant_id):
    try:
        documents = await db[COLLECTION].find(
            {"row.tenant_id": tenant_id}, {"_id": 0}).sort("row.seq", 1).to_list(None)
        events = [checked_event(doc) for doc in documents]
        if any(event["row"]["tenant_id"] != tenant_id for event in events):
            raise ValueError("Tenant chain crossed.")
        commands = [event["command_id"] for event in events]
        if len(set(commands)) != len(commands):
            raise ValueError("Duplicate authoritative command.")
        receipt = verify_chain(rows_in_seq_order=[decode_row(event["row"]) for event in events])
        if receipt.break_at_seq is not None:
            raise ValueError("Authoritative Ledger chain is incomplete or broken.")
        return events
    except (KeyError, TypeError, AttributeError, OverflowError) as exc:
        raise ValueError("Malformed authoritative Ledger prefix.") from exc