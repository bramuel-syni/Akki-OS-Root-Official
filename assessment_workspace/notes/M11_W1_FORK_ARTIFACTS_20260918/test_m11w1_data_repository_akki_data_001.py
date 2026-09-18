"""tests/invariants/test_m11w1_data_repository_akki_data_001.py

M11-W1 · akki.data repository primitive · AKKI-DATA-001 refusal.

Canon anchors (verbatim quotes carried in-file per SO §3 grounding-brief
discipline):
  - v1.0 clause B.2 (partial): "Primary datastore is Mongo, one database
    per tenant, all access via `services.data.repository` — the sole
    Motor importer."
  - v1.0 clause D-01 (partial): "Tenant isolation invariant AKKI-DATA-001:
    a data-plane call whose document `tenant_id` mismatches the injected
    context tenant_id is refused."
  - R-18 (2026-09-18) Tension (a) Option C · thin adapter (agent-
    recommended, owner-ratified 2026-09-17T~15:45Z, SO §3.8 amended
    in-place): "M11-W1 lands `services/data/repository.py` as the sole
    Motor importer.  Adapters at `services/enforce/<entity>_gate.py`
    (W3+) call the paired M9 refuser first, then a Repository op."
  - SO §3.3 tests-first discipline: RED before GREEN, byte-match
    double-GREEN, ratchet monotonic-up, no silent rebaselining.
  - SO §3.8 additive-only (Option C ratification): no sealed M9 file
    modified this wave — enforced by
    `test_m11w1_m9_files_untouched.py`.

Test IDs (13):
  1. test_data_repository_module_exists
  2. test_repository_class_exists_with_ctx_and_collection_kwargs
  3. test_repository_refusal_error_is_defined
  4. test_repository_refusal_error_carries_akki_data_001_code
  5. test_repo_auto_injects_tenant_id_on_find
  6. test_repo_auto_injects_tenant_id_on_find_one
  7. test_repo_auto_injects_tenant_id_on_count_documents
  8. test_repo_refuses_cross_tenant_insert_one
  9. test_repo_admits_matching_tenant_insert_one
 10. test_repo_admits_missing_tenant_id_by_injecting_on_insert_one
 11. test_repo_refuses_cross_tenant_update_by_filter
 12. test_repo_refuses_cross_tenant_update_by_set_document
 13. test_repo_refuses_cross_tenant_delete_by_filter

All tests are RED at wave-open (ImportError · services.data.repository
does not yet exist) and GREEN after Repository primitive lands.
"""
from __future__ import annotations

import importlib

import pytest


# --- Test 1: module exists ----------------------------------------------------

def test_data_repository_module_exists():
    """R-18 Tension-a Option C: `services/data/repository.py` is the
    sole Motor importer.  This test asserts the module is importable
    at wave-open."""
    mod = importlib.import_module("services.data.repository")
    assert mod is not None


# --- Test 2: Repository class ------------------------------------------------

def test_repository_class_exists_with_ctx_and_collection_kwargs():
    """Repository(ctx=..., collection=...) constructs without I/O."""
    from services.data.repository import Repository, Context
    ctx = Context(tenant_id="t1")

    class _MockColl:
        pass

    repo = Repository(ctx=ctx, collection=_MockColl())
    assert repo is not None


# --- Test 3+4: RepositoryRefusalError ---------------------------------------

def test_repository_refusal_error_is_defined():
    from services.data.repository import RepositoryRefusalError
    assert issubclass(RepositoryRefusalError, Exception)


def test_repository_refusal_error_carries_akki_data_001_code():
    """AKKI-DATA-001 · verbatim refusal code exposed as class attribute
    on CrossTenantAccessRefused (M9 preventive-charter refusal-class
    hierarchy: root RepositoryRefusalError + named subclass)."""
    from services.data.repository import (
        RepositoryRefusalError,
        CrossTenantAccessRefused,
        AKKI_DATA_001,
    )
    assert AKKI_DATA_001 == "AKKI-DATA-001"
    assert issubclass(CrossTenantAccessRefused, RepositoryRefusalError)
    assert getattr(CrossTenantAccessRefused, "code", "") == AKKI_DATA_001


# --- Async mock collection helper --------------------------------------------

class _AsyncMockCollection:
    """A minimal shape-only stand-in for AsyncIOMotorCollection.  Records
    every call's args + kwargs on `self.calls` for assertion."""

    def __init__(self):
        self.calls: list = []

    def find(self, *args, **kwargs):
        self.calls.append(("find", args, kwargs))
        return _AsyncCursor()

    async def find_one(self, *args, **kwargs):
        self.calls.append(("find_one", args, kwargs))
        return None

    async def count_documents(self, *args, **kwargs):
        self.calls.append(("count_documents", args, kwargs))
        return 0

    async def insert_one(self, *args, **kwargs):
        self.calls.append(("insert_one", args, kwargs))
        return _InsertResult()

    async def update_one(self, *args, **kwargs):
        self.calls.append(("update_one", args, kwargs))
        return _UpdateResult()

    async def update_many(self, *args, **kwargs):
        self.calls.append(("update_many", args, kwargs))
        return _UpdateResult()

    async def delete_one(self, *args, **kwargs):
        self.calls.append(("delete_one", args, kwargs))
        return _DeleteResult()

    async def delete_many(self, *args, **kwargs):
        self.calls.append(("delete_many", args, kwargs))
        return _DeleteResult()


class _AsyncCursor:
    pass


class _InsertResult:
    inserted_id = "mock-id"


class _UpdateResult:
    matched_count = 0


class _DeleteResult:
    deleted_count = 0


# --- Test 5-7: auto-injection of tenant_id on read path ---------------------

@pytest.mark.asyncio
async def test_repo_auto_injects_tenant_id_on_find():
    """v1.0 D-01: every read must carry the ctx tenant_id in its
    outgoing Motor filter."""
    from services.data.repository import Repository, Context

    coll = _AsyncMockCollection()
    repo = Repository(ctx=Context(tenant_id="t1"), collection=coll)

    # Motor's `.find()` returns a cursor synchronously (not awaited).
    repo.find({"kind": "estate"})

    assert len(coll.calls) == 1
    op, args, kwargs = coll.calls[0]
    assert op == "find"
    outgoing_filter = args[0]
    assert outgoing_filter.get("tenant_id") == "t1"
    assert outgoing_filter.get("kind") == "estate"


@pytest.mark.asyncio
async def test_repo_auto_injects_tenant_id_on_find_one():
    from services.data.repository import Repository, Context

    coll = _AsyncMockCollection()
    repo = Repository(ctx=Context(tenant_id="t1"), collection=coll)

    await repo.find_one({"id": "abc"})

    assert len(coll.calls) == 1
    op, args, kwargs = coll.calls[0]
    assert op == "find_one"
    outgoing_filter = args[0]
    assert outgoing_filter.get("tenant_id") == "t1"
    assert outgoing_filter.get("id") == "abc"


@pytest.mark.asyncio
async def test_repo_auto_injects_tenant_id_on_count_documents():
    from services.data.repository import Repository, Context

    coll = _AsyncMockCollection()
    repo = Repository(ctx=Context(tenant_id="t1"), collection=coll)

    await repo.count_documents({"status": "active"})

    op, args, kwargs = coll.calls[0]
    assert op == "count_documents"
    outgoing_filter = args[0]
    assert outgoing_filter.get("tenant_id") == "t1"


# --- Test 8-10: write-path AKKI-DATA-001 -----------------------------------

@pytest.mark.asyncio
async def test_repo_refuses_cross_tenant_insert_one():
    """AKKI-DATA-001: insert_one({tenant_id: 't2', ...}) when
    ctx.tenant_id == 't1' raises CrossTenantAccessRefused."""
    from services.data.repository import (
        Repository, Context, CrossTenantAccessRefused, AKKI_DATA_001,
    )

    coll = _AsyncMockCollection()
    repo = Repository(ctx=Context(tenant_id="t1"), collection=coll)

    with pytest.raises(CrossTenantAccessRefused) as exc_info:
        await repo.insert_one({"tenant_id": "t2", "kind": "estate"})

    # Downstream collection was never called.
    assert len(coll.calls) == 0
    # Refusal message carries AKKI-DATA-001; COUNTS-only per M9 discipline.
    assert AKKI_DATA_001 in str(exc_info.value)


@pytest.mark.asyncio
async def test_repo_admits_matching_tenant_insert_one():
    """Matching tenant_id in document admits the write."""
    from services.data.repository import Repository, Context

    coll = _AsyncMockCollection()
    repo = Repository(ctx=Context(tenant_id="t1"), collection=coll)

    await repo.insert_one({"tenant_id": "t1", "kind": "estate"})

    assert len(coll.calls) == 1
    op, args, kwargs = coll.calls[0]
    assert op == "insert_one"
    outgoing_doc = args[0]
    assert outgoing_doc.get("tenant_id") == "t1"


@pytest.mark.asyncio
async def test_repo_admits_missing_tenant_id_by_injecting_on_insert_one():
    """Missing tenant_id in document is auto-injected from ctx (not
    refused); this is the auto-injection contract of B.2."""
    from services.data.repository import Repository, Context

    coll = _AsyncMockCollection()
    repo = Repository(ctx=Context(tenant_id="t1"), collection=coll)

    await repo.insert_one({"kind": "estate"})

    assert len(coll.calls) == 1
    op, args, kwargs = coll.calls[0]
    assert op == "insert_one"
    outgoing_doc = args[0]
    assert outgoing_doc.get("tenant_id") == "t1"


# --- Test 11-13: cross-tenant refusal on update/delete filters --------------

@pytest.mark.asyncio
async def test_repo_refuses_cross_tenant_update_by_filter():
    """AKKI-DATA-001: update_one filter carrying tenant_id ≠ ctx is refused."""
    from services.data.repository import (
        Repository, Context, CrossTenantAccessRefused,
    )

    coll = _AsyncMockCollection()
    repo = Repository(ctx=Context(tenant_id="t1"), collection=coll)

    with pytest.raises(CrossTenantAccessRefused):
        await repo.update_one(
            {"tenant_id": "t2", "id": "x"},
            {"$set": {"status": "active"}},
        )

    assert len(coll.calls) == 0


@pytest.mark.asyncio
async def test_repo_refuses_cross_tenant_update_by_set_document():
    """AKKI-DATA-001: update_one $set carrying tenant_id ≠ ctx is refused."""
    from services.data.repository import (
        Repository, Context, CrossTenantAccessRefused,
    )

    coll = _AsyncMockCollection()
    repo = Repository(ctx=Context(tenant_id="t1"), collection=coll)

    with pytest.raises(CrossTenantAccessRefused):
        await repo.update_one(
            {"id": "x"},
            {"$set": {"tenant_id": "t2", "status": "active"}},
        )

    assert len(coll.calls) == 0


@pytest.mark.asyncio
async def test_repo_refuses_cross_tenant_delete_by_filter():
    """AKKI-DATA-001: delete_one filter carrying tenant_id ≠ ctx is refused."""
    from services.data.repository import (
        Repository, Context, CrossTenantAccessRefused,
    )

    coll = _AsyncMockCollection()
    repo = Repository(ctx=Context(tenant_id="t1"), collection=coll)

    with pytest.raises(CrossTenantAccessRefused):
        await repo.delete_one({"tenant_id": "t2", "id": "x"})

    assert len(coll.calls) == 0
