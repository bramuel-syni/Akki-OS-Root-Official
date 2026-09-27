"""Permitted sidecar backoff; sealed Mongo writer bytes and CAS stay unchanged."""
import asyncio
import secrets
from pymongo.errors import DuplicateKeyError
from services.ledger_writer.mongo_control import COLLECTION


class _Collection:
    def __init__(self, collection):
        self.collection, self.conflicts = collection, 0

    def __getattr__(self, name):
        return getattr(self.collection, name)

    async def insert_one(self, document):
        try:
            return await self.collection.insert_one(document)
        except DuplicateKeyError:
            self.conflicts += 1
            if self.conflicts < 64:
                await asyncio.sleep(min(0.001 * (2 ** min(self.conflicts - 1, 6)), 0.05)
                                    + secrets.randbelow(1000) / 1_000_000)
            # The original writer re-reads the winning command/current head.
            # Conditional-control guards still reject stale budget decisions.
            raise


class ContentionDB:
    def __init__(self, db):
        self.db = db

    def __getitem__(self, collection):
        if collection != COLLECTION:
            raise ValueError('Only the canonical control ledger is allowed.')
        return _Collection(self.db[collection])