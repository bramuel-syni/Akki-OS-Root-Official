"""Insert-only durable adapter for canonical v1 control-plane events.

One Mongo document atomically commits the 17-field row and hash-bound payload.
No best-effort mirror, mutable head, state cache, or counter. Unique indexes
provide cross-process compare-and-append, including idempotent commands.
"""
import hashlib
import json
from dataclasses import asdict
from datetime import datetime, timezone

from pymongo import ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError
from contracts.ledger_v1 import LedgerRow, LedgerRowAt
from services.ledger_emitter.emit_intent import emit_control_intent
from services.ledger_writer.main import append_intent, compute_row_hash

COLLECTION = "ledger_v1_control_events"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=True, allow_nan=False).encode()).hexdigest()


def decode_row(doc):
    data = dict(doc)
    data["at"] = LedgerRowAt(**data["at"])
    return LedgerRow(**data)


def verify_event(event):
    row = decode_row(event["row"])
    if digest(event["payload"]) != row.payload_ref or compute_row_hash(row.prev_hash, row) != row.hash:
        raise ValueError("Ledger integrity check failed.")
    return event


async def ensure_indexes(db):
    coll = db[COLLECTION]
    await coll.create_index([("row.tenant_id", ASCENDING), ("row.seq", ASCENDING)], unique=True)
    await coll.create_index([("row.tenant_id", ASCENDING), ("command_id", ASCENDING)], unique=True)
    await coll.create_index([("row.tenant_id", ASCENDING), ("row.run_id", ASCENDING)])


async def append_event(db, *, tenant_id, run_id, actor_id, command_id, event_type,
                       resource_type, decision, reason_code, payload):
    await ensure_indexes(db)
    coll = db[COLLECTION]
    for _ in range(64):
        existing = await coll.find_one({"row.tenant_id": tenant_id, "command_id": command_id}, {"_id": 0})
        if existing:
            return verify_event(existing)
        head = await coll.find_one({"row.tenant_id": tenant_id}, {"_id": 0}, sort=[("row.seq", DESCENDING)])
        if head:
            verify_event(head)
        prev = decode_row(head["row"]) if head else None
        intent = emit_control_intent(
            tenant_id=tenant_id, run_id=run_id, actor_id=actor_id,
            event_type=event_type, resource_type=resource_type, resource_id=run_id,
            decision=decision, reason_code=reason_code, payload_ref=digest(payload),
            epoch_s=int(datetime.now(timezone.utc).timestamp()),
        )
        row = append_intent(intent=intent, prev_row=prev, tenant_seq_next=prev.seq + 1 if prev else 1)
        doc = {"command_id": command_id, "row": asdict(row), "payload": payload}
        try:
            await coll.insert_one(dict(doc))  # Motor's _id mutation never enters returned data.
            return doc
        except DuplicateKeyError:
            continue  # Race lost: read the winner or recompute against the next head.
    raise RuntimeError("Ledger is busy; retry the same idempotency key.")


async def read_events(db, query):
    rows = await db[COLLECTION].find(query, {"_id": 0}).sort("row.seq", ASCENDING).to_list(None)
    return [verify_event(row) for row in rows]