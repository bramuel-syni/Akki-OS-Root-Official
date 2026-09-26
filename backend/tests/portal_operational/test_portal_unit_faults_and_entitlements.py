"""MOCKED/TEST-ONLY unit checks for portal work fail-closed + entitlement projection."""

from datetime import datetime, timedelta, timezone
import asyncio

import pytest
from fastapi import HTTPException

from services.northena import portal_work
from services.portal_operational import entitlements
from services.ledger_writer import mongo_control


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()


def _row(resource_type: str) -> dict:
    return {"resource_type": resource_type, "tenant_id": "DIGICOW"}


def _membership(*, principal_id="principal-1", status="active", org="org-1", admitted=True):
    payload = {
        "principal_id": principal_id,
        "status": status,
        "organisation_principal_id": org,
    }
    if admitted:
        payload["admission_receipt_ref"] = "receipt-membership"
    return {"row": _row("principal_membership"), "payload": payload}


def _licence_event(*, org="org-1", status="active", admitted=True, period_start=None, period_end=None, period_iso="2026-02"):
    now = datetime.now(timezone.utc)
    start = period_start or (now - timedelta(days=1))
    end = period_end or (now + timedelta(days=1))
    payload = {
        "licence": {
            "plan_identifier": "plan-a",
            "organisation_principal_id": org,
            "seat_count": 2,
            "compute_dial": "managed",
            "frontier_dial": "managed",
            "credits_per_seat_per_period": 100,
            "pooled_credits_flag": True,
            "seat_soft_limit": 2,
            "organisation_ceiling": 4,
            "period": "month",
            "renewal_date": _iso(now + timedelta(days=30)),
            "status": status,
            "terms_identifier": "terms-1",
            "agent_count": None,
        },
        "period_start": _iso(start),
        "period_end": _iso(end),
        "period_iso": period_iso,
    }
    if admitted:
        payload["admission_receipt_ref"] = "receipt-licence"
    return {"row": _row("entitlement_licence"), "payload": payload}


def _catalog_event(*, model="model-a", access_class="local_served", status="listed", ceremony=True, credit_rate=None):
    payload = {
        "catalog_row": {
            "model_identifier": model,
            "access_class": access_class,
            "status": status,
            "residency": "za",
            "credit_rate": credit_rate,
        }
    }
    if ceremony:
        payload["ceremony_receipt_ref"] = "receipt-catalog"
    return {"row": _row("entitlement_catalog"), "payload": payload}


def _metered_event(*, org="org-1", quantity=10.0, timestamp=None, access_class="reseller_frontier", credit_rate=2.0, execution_ref=True):
    now = datetime.now(timezone.utc)
    payload = {
        "organisation_principal_id": org,
        "metered_event": {
            "operation_type": "processed_intelligence",
            "accessed_scope": "scope-a",
            "quantity": quantity,
            "quantity_unit": "tokens",
            "terms_id": "terms-1",
            "party_id": "principal-1",
            "timestamp_iso": _iso(timestamp or now),
            "au_3b_defensible": False,
        },
        "catalog_row_at_event": {
            "model_identifier": "model-frontier",
            "access_class": access_class,
            "status": "listed",
            "residency": "za",
            "credit_rate": credit_rate,
        },
    }
    if execution_ref:
        payload["execution_receipt_ref"] = "receipt-exec"
    return {"row": _row("metered_event"), "payload": payload}


# Module/feature: fail closed when ledger writer insert/outage prevents receipt
def test_portal_submit_fails_closed_when_ledger_insert_unavailable(monkeypatch):
    scope = {"tenant_id": "DIGICOW", "principal_id": "principal-1"}
    body = type("SubmitBody", (), {
        "objective_text": "unit test objective",
        "operation": "processed_intelligence",
        "units": ["rms_mysql"],
        "idempotency_key": "unit-failclosed-123456",
        "model_dump": lambda self, exclude=None: {
            "objective_text": self.objective_text,
            "operation": self.operation,
            "units": self.units,
        },
    })()

    async def _raise_outage(*args, **kwargs):
        raise RuntimeError("ledger unavailable")

    monkeypatch.setattr(portal_work, "append_event", _raise_outage)
    with pytest.raises(RuntimeError):
        asyncio.run(portal_work.submit(db=object(), scope=scope, body=body))


# Module/feature: corruption on returned payload/body hash must refuse acknowledgement
def test_portal_submit_rejects_corrupt_payload_on_idempotent_return(monkeypatch):
    scope = {"tenant_id": "DIGICOW", "principal_id": "principal-1"}
    body = type("SubmitBody", (), {
        "objective_text": "hash check objective",
        "operation": "processed_intelligence",
        "units": ["rms_mysql"],
        "idempotency_key": "unit-corrupt-123456",
        "model_dump": lambda self, exclude=None: {
            "objective_text": self.objective_text,
            "operation": self.operation,
            "units": self.units,
        },
    })()

    async def _corrupt_append(*args, **kwargs):
        return {
            "row": {"hash": "abc"},
            "payload": {
                "request_id": "req-1",
                "principal_id": "principal-1",
                "objective_text": "hash check objective",
                "objective_hash": "x",
                "body_hash": "different-hash",
                "units": ["rms_mysql"],
                "operation": "processed_intelligence",
                "governing_engine": "Synthesizer",
                "created_at": _iso(datetime.now(timezone.utc)),
                "lifecycle_state": "Routing",
                "reason_code": "ADMISSION_UNRESOLVED",
                "history": [],
            },
        }

    async def _events_for(*args, **kwargs):
        return [await _corrupt_append()]

    monkeypatch.setattr(portal_work, "append_event", _corrupt_append)
    monkeypatch.setattr(portal_work, "events_for", _events_for)

    with pytest.raises(HTTPException) as exc:
        asyncio.run(portal_work.submit(db=object(), scope=scope, body=body))
    assert exc.value.status_code == 409


# Module/feature: canonical adapter remains insert-only (no state mutation path)
def test_mongo_control_append_event_uses_insert_only_adapter():
    class FakeCollection:
        def __init__(self):
            self.docs = []
            self.update_called = False

        async def create_index(self, *args, **kwargs):
            return None

        async def find_one(self, query, projection=None, sort=None):
            tenant = query.get("row.tenant_id")
            command = query.get("command_id")
            if command is not None:
                for doc in self.docs:
                    if doc["row"]["tenant_id"] == tenant and doc["command_id"] == command:
                        return doc
                return None
            tenant_docs = [d for d in self.docs if d["row"]["tenant_id"] == tenant]
            if not tenant_docs:
                return None
            return sorted(tenant_docs, key=lambda d: d["row"]["seq"], reverse=True)[0]

        async def insert_one(self, doc):
            self.docs.append(doc)
            return type("InsertResult", (), {"inserted_id": "x"})()

        async def update_one(self, *args, **kwargs):
            self.update_called = True
            return None

    class FakeDb(dict):
        def __getitem__(self, item):
            return super().__getitem__(item)

    coll = FakeCollection()
    db = FakeDb({mongo_control.COLLECTION: coll})

    event = asyncio.run(mongo_control.append_event(
        db,
        tenant_id="DIGICOW",
        run_id="req-1",
        actor_id="principal-1",
        command_id="cmd-1",
        event_type="dap.request.commissioned",
        resource_type="dap_request",
        decision="held",
        reason_code="ADMISSION_UNRESOLVED",
        payload={"a": 1},
    ))

    assert event["row"]["resource_type"] == "dap_request"
    assert coll.update_called is False
    assert len(coll.docs) == 1


# Module/feature: missing membership/licence unresolved with null allowance
def test_entitlement_unresolved_when_membership_or_licence_missing(monkeypatch):
    scope = {"tenant_id": "DIGICOW", "principal_id": "principal-1"}
    async def _read_events(*args, **kwargs):
        return []

    monkeypatch.setattr(entitlements, "read_events", _read_events)
    view = asyncio.run(entitlements.read_view(db=object(), scope=scope))
    assert view.status == "unresolved"
    assert view.allowance_state is None
    assert view.licence is None


# Module/feature: admitted active entitlement resolves with listed rows and allowance
def test_entitlement_active_membership_and_licence_resolve(monkeypatch):
    scope = {"tenant_id": "DIGICOW", "principal_id": "principal-1"}
    events = [
        _membership(),
        _licence_event(),
        _catalog_event(model="model-listed", access_class="local_served", status="listed", credit_rate=None),
    ]
    async def _read_events(*args, **kwargs):
        return events

    monkeypatch.setattr(entitlements, "read_events", _read_events)
    view = asyncio.run(entitlements.read_view(db=object(), scope=scope))
    assert view.status == "resolved"
    assert view.licence is not None
    assert view.count == 1
    assert view.allowance_state is not None


# Module/feature: suspended/expired and malformed rate refs fail closed (no fabricated zero)
def test_entitlement_suspended_and_invalid_metering_fail_closed(monkeypatch):
    scope = {"tenant_id": "DIGICOW", "principal_id": "principal-1"}

    suspended_events = [_membership(), _licence_event(status="suspended"), _catalog_event(model="model-listed")]
    async def _read_suspended(*args, **kwargs):
        return suspended_events

    monkeypatch.setattr(entitlements, "read_events", _read_suspended)
    suspended = asyncio.run(entitlements.read_view(db=object(), scope=scope))
    assert suspended.status == "suspended"
    assert suspended.count == 0

    now = datetime.now(timezone.utc)
    invalid_meter_events = [
        _membership(),
        _licence_event(),
        _catalog_event(model="model-frontier", access_class="reseller_frontier", status="listed", credit_rate=2.0),
        _metered_event(org="wrong-org", quantity=100.0, timestamp=now),
        _metered_event(quantity=10.0, timestamp=now - timedelta(days=10)),
        _metered_event(quantity=10.0, timestamp=now, credit_rate=None),
    ]
    async def _read_invalid(*args, **kwargs):
        return invalid_meter_events

    monkeypatch.setattr(entitlements, "read_events", _read_invalid)
    invalid = asyncio.run(entitlements.read_view(db=object(), scope=scope))
    assert invalid.status == "unresolved"
    assert invalid.reason_code == "ENTITLEMENT_RECORD_INVALID"
    assert invalid.allowance_state is None


@pytest.mark.parametrize("pooled,expected_allowance,expected_debit", [(True, 200, 57), (False, 100, 50)])
def test_event_time_rates_and_seat_pool_scope(monkeypatch, pooled, expected_allowance, expected_debit):
    """TEST-ONLY: real pure derivation, injected events; no production licence."""
    licence = _licence_event()
    licence["payload"]["licence"]["pooled_credits_flag"] = pooled
    own_a = _metered_event(quantity=10, credit_rate=2)
    own_b = _metered_event(quantity=10, credit_rate=3)
    own_b["payload"]["catalog_row_at_event"]["model_identifier"] = "model-b"
    other_seat = _metered_event(quantity=7, credit_rate=1)
    other_seat["payload"]["metered_event"]["party_id"] = "principal-2"
    events = [_membership(), licence, own_a, own_b, other_seat,
              _metered_event(org="foreign-org", quantity=999),
              _metered_event(timestamp=datetime.now(timezone.utc) - timedelta(days=10)),
              _catalog_event(access_class="reseller_frontier", credit_rate=100)]

    async def reads(db, query):
        assert query["row.tenant_id"] == "DIGICOW"
        return events

    monkeypatch.setattr(entitlements, "read_events", reads)
    view = asyncio.run(entitlements.read_view(object(), {"tenant_id": "DIGICOW", "principal_id": "principal-1"}))
    assert view.status == "resolved"
    assert view.allowance_state.credits_allowance == expected_allowance
    assert view.allowance_state.credits_debited == expected_debit
    assert view.allowance_state.credits_remaining == expected_allowance - expected_debit


def test_catalog_dials_retirement_and_customer_model_ownership(monkeypatch):
    licence = _licence_event()
    licence["payload"]["licence"]["frontier_dial"] = "your_keys"
    own_model = _catalog_event(model="own", access_class="customer_model")
    own_model["payload"]["organisation_principal_id"] = "org-1"
    foreign_model = _catalog_event(model="foreign", access_class="customer_model")
    foreign_model["payload"]["organisation_principal_id"] = "org-2"
    events = [_membership(), licence, own_model, foreign_model,
              _catalog_event(model="keys", access_class="customer_key"),
              _catalog_event(model="frontier", access_class="reseller_frontier", credit_rate=2),
              _catalog_event(model="paused", status="paused"),
              _catalog_event(model="retired"), _catalog_event(model="retired", status="retired")]

    async def reads(*args):
        return events

    monkeypatch.setattr(entitlements, "read_events", reads)
    view = asyncio.run(entitlements.read_view(object(), {"tenant_id": "DIGICOW", "principal_id": "principal-1"}))
    assert view.status == "resolved"
    assert {row.model_identifier for row in view.rows} == {"own", "keys"}


@pytest.mark.parametrize("status,date_expired", [("expired", False), ("active", True)])
def test_expired_licence_has_no_allowance_or_picker(monkeypatch, status, date_expired):
    licence = _licence_event(status=status)
    if date_expired:
        licence["payload"]["licence"]["renewal_date"] = _iso(datetime.now(timezone.utc) - timedelta(days=1))

    async def reads(*args):
        return [_membership(), licence, _catalog_event()]

    monkeypatch.setattr(entitlements, "read_events", reads)
    view = asyncio.run(entitlements.read_view(object(), {"tenant_id": "DIGICOW", "principal_id": "principal-1"}))
    assert view.status == "expired"
    assert view.allowance_state is None and view.rows == []
