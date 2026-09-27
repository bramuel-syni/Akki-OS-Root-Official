"""Request-lifetime insert guard around the unchanged canonical Mongo writer."""
from services.enforce.control_scope import require_control_scope
from services.ledger_writer.mongo_control import COLLECTION
from services.ledger_writer.control_commands import check_attribution
from services.ledger_writer.control_integrity import checked_event
from services.ledger_writer.contention_control import ContentionDB


class _Collection:
    def __init__(self, collection, scope):
        self._collection, self._scope = collection, scope

    def __getattr__(self, name):
        return getattr(self._collection, name)

    async def insert_one(self, document):
        scope = require_control_scope()
        if scope is not self._scope:
            raise ValueError("Control request lifetime changed before insert.")
        event = checked_event(document)
        if (event["row"]["actor_id"], event["row"]["tenant_id"]) != (
                scope.principal_id, scope.tenant_id):
            raise ValueError("Ledger attribution changed before insert.")
        check_attribution(event["payload"], scope.principal_id, scope.tenant_id)
        return await self._collection.insert_one(document)


class InsertGuard:
    def __init__(self, db, scope):
        self._db, self._scope = ContentionDB(db), scope

    def __getitem__(self, collection):
        if collection != COLLECTION:
            raise ValueError("Unexpected control writer collection.")
        return _Collection(self._db[collection], self._scope)