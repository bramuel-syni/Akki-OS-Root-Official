"""Durable compaction storage on MongoDB — the same invariants as InMemoryCompactionStorage, surviving restarts.

Ledger row BEFORE artefact readable (MEM-R-012/013); hash-verify or refuse on read (MEM-R-015/016); ledger row
present at read (MEM-R-050). Synchronous pymongo surface so `operations.compact/reload` stay byte-identical.
"""
import os
from typing import Optional

from bson import Binary
from pymongo import MongoClient

from services.memory.compaction_v1.carriers import CompactionArtefactRef, CompactionLedgerRow
from services.memory.compaction_v1.refusals import MemoryLedgerRowMissingRefusalError, MemoryReloadRefusalError
from services.memory.compaction_v1.verifier import ReloadVerifier

LEDGER_ROWS = 'memory_compaction_ledger_rows'
ARTEFACTS = 'memory_compaction_artefacts'
REFS = 'memory_compaction_refs'


class MongoCompactionStorage:
    def __init__(self, tenant_id):
        self.tenant_id = tenant_id
        self._client = MongoClient(os.environ['MONGO_URL'])
        self._db = self._client[os.environ['DB_NAME']]

    def close(self):
        self._client.close()

    def write_ledger_row(self, *, row: CompactionLedgerRow) -> None:
        self._db[LEDGER_ROWS].update_one({'tenant_id': self.tenant_id, 'artefact_hash': row.artefact_hash},
                                         {'$setOnInsert': {'tenant_id': self.tenant_id, **row.model_dump(mode='json')}}, upsert=True)

    def write_artefact_bytes(self, *, artefact_hash: str, artefact_bytes: bytes) -> None:
        if self.read_ledger_row(artefact_hash=artefact_hash) is None:
            raise MemoryLedgerRowMissingRefusalError('AKKI-MEM-COMPACT-002: artefact write refused - ledger row absent (MEM-R-013 · counts-only: 1)')
        self._db[ARTEFACTS].update_one({'tenant_id': self.tenant_id, 'artefact_hash': artefact_hash},
                                       {'$setOnInsert': {'tenant_id': self.tenant_id, 'artefact_hash': artefact_hash, 'body': Binary(artefact_bytes)}}, upsert=True)

    def register_artefact_ref(self, *, artefact_ref: CompactionArtefactRef) -> None:
        self._db[REFS].update_one({'tenant_id': self.tenant_id, 'artefact_hash': artefact_ref.artefact_hash},
                                  {'$set': {'tenant_id': self.tenant_id, **artefact_ref.model_dump(mode='json')}}, upsert=True)

    def read_ledger_row(self, *, artefact_hash: str) -> Optional[CompactionLedgerRow]:
        doc = self._db[LEDGER_ROWS].find_one({'tenant_id': self.tenant_id, 'artefact_hash': artefact_hash}, {'_id': 0, 'tenant_id': 0})
        return CompactionLedgerRow.model_validate(doc) if doc else None

    def read_artefact_bytes(self, *, artefact_hash: str, verifier: ReloadVerifier) -> bytes:
        if self.read_ledger_row(artefact_hash=artefact_hash) is None:
            raise MemoryLedgerRowMissingRefusalError('AKKI-MEM-COMPACT-002: artefact read refused - ledger row absent (MEM-R-050 · counts-only: 1)')
        doc = self._db[ARTEFACTS].find_one({'tenant_id': self.tenant_id, 'artefact_hash': artefact_hash})
        if doc is None:
            raise MemoryLedgerRowMissingRefusalError('AKKI-MEM-COMPACT-002: artefact read refused - artefact bytes absent under a ledger row (counts-only: 1)')
        payload = bytes(doc['body'])
        if not verifier.verify(bytes_payload=payload, expected_hash=artefact_hash):
            raise MemoryReloadRefusalError('AKKI-MEM-COMPACT-001: reload refused - hash verify failed (MEM-R-016 · counts-only: 1)')
        return payload

    def read_artefact_ref(self, *, artefact_hash: str) -> Optional[CompactionArtefactRef]:
        doc = self._db[REFS].find_one({'tenant_id': self.tenant_id, 'artefact_hash': artefact_hash}, {'_id': 0, 'tenant_id': 0})
        return CompactionArtefactRef.model_validate(doc) if doc else None

    def iter_artefact_refs_citing(self, *, unit_ref: str) -> tuple:
        docs = self._db[REFS].find({'tenant_id': self.tenant_id, 'provenance_refs': unit_ref}, {'_id': 0, 'tenant_id': 0}).sort('artefact_hash', 1)
        return tuple(CompactionArtefactRef.model_validate(d) for d in docs)

    def tamper_artefact_bytes(self, *, artefact_hash: str, new_bytes: bytes) -> None:
        """Test hook only: simulates on-disk tamper so reload must refuse."""
        self._db[ARTEFACTS].update_one({'tenant_id': self.tenant_id, 'artefact_hash': artefact_hash}, {'$set': {'body': Binary(new_bytes)}})


__all__ = ('MongoCompactionStorage',)
