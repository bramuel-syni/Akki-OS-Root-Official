"""Compare-and-append without modifying the sealed canonical writer or its indexes.

Unique tenant/sequence arbitrates processes. If a competing event wins, the
canonical retry meets this guard again and MUST NOT reuse stale budget arithmetic.
"""
from contracts.ledger_v1 import GENESIS_PREV_HASH
from services.ledger_writer.mongo_control import COLLECTION
from services.ledger_writer.principal_control import append_event


class HeadChanged(ValueError):
    pass


class _ConditionalCollection:
    def __init__(self, collection, expected_head):
        self.collection, self.expected_head = collection, expected_head

    def __getattr__(self, name):
        return getattr(self.collection, name)

    async def insert_one(self, document):
        if document["row"]["prev_hash"] != self.expected_head:
            raise HeadChanged("Control prefix changed; re-evaluate the decision.")
        return await self.collection.insert_one(document)


class _ConditionalDB:
    def __init__(self, db, head):
        self.db, self.head = db, head

    def __getitem__(self, collection):
        if collection != COLLECTION:
            raise ValueError("Only the canonical control ledger is allowed.")
        return _ConditionalCollection(self.db[collection], self.head)


async def append_at_head(db, events, **kwargs):
    head = events[-1]["row"]["hash"] if events else GENESIS_PREV_HASH
    return await append_event(_ConditionalDB(db, head), **kwargs)