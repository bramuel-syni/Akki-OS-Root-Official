"""Non-GPU custody delivery contracts using real signatures + fake provider (SYNTHETIC only)."""

from __future__ import annotations

import asyncio
import hashlib
import json
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import pytest
from pydantic import SecretStr

sys.path.insert(0, "/app/backend/vendored/extraction_akki/backend")
sys.path.insert(0, "/app/backend/tests/activation_controls")
sys.path.insert(0, "/app/backend/tests/portal_operational")

import test_native_control_ledger as native_helpers
from test_w1_control_record_contract_red import _FakeDb

from services.activation.receipts import NativeReceipts
from services.custody_delivery.models import DeliveryProof, DeliveryRequest
from services.custody_delivery.ports import CustodyBinding, ProviderState, origin_of
from services.custody_delivery.service import CustodyDelivery
from services.enforce.control_scope import bind_control_scope
from services.enforce.principal_context_adapter import principal_context
from services.ledger_writer.mongo_control import digest
from services.northena.execution_journal import LedgerJournal
from services.northena.execution_models import Artifact, Authority, Held, Request, RunView
from services.activation.native_evidence import Observation


@contextmanager
def scope(principal: str = "operator", tenant: str = "tenant-SYNTHETIC"):
    with principal_context(principal), bind_control_scope({"principal_id": principal, "tenant_id": tenant}):
        yield


class FakeProvider:
    def __init__(self):
        self.prepare_calls = 0
        self.status_calls = 0
        self.prepare_state = ProviderState()
        self.status_state = ProviderState()
        self.prepare_error = None
        self.status_error = None

    async def prepare(self, _descriptor, _authority):
        self.prepare_calls += 1
        if self.prepare_error:
            raise self.prepare_error
        return self.prepare_state

    async def status(self, _descriptor, _authority):
        self.status_calls += 1
        if self.status_error:
            raise self.status_error
        return self.status_state


class FakeCoordinator:
    def __init__(self, db, request: Request, artifact: Artifact, *, now_epoch: int):
        self._request = request
        self._artifact = artifact
        self._now = now_epoch
        self._deny_after_first = False
        self._retrieve_calls = 0
        self.journal = LedgerJournal(db)
        self.authority = SimpleNamespace(authorize=self._authorize)

    async def seed_registry(self):
        await self.journal.append(self._request, "request", {
            "request_sha256": self._request.digest(),
            "request": self._request.model_dump(mode="json"),
        })
        await self.journal.append(self._request, "registry", {
            "evidence_mode": "measured",
            "artifacts": [self._artifact.model_dump(mode="json")],
        })

    async def retrieve(self, _request):
        self._retrieve_calls += 1
        if self._deny_after_first and self._retrieve_calls > 1:
            return RunView(request_id=self._request.request_id, phase="held", reason_code="RIGHTS_WITHDRAWN")
        return RunView(
            request_id=self._request.request_id,
            phase="ready",
            reason_code="VERIFIED_RESULT_RECORDED",
            artifact_refs=(self._artifact.ref,),
            evidence_mode="measured",
        )

    async def _authorize(self, request: Request, _operation: str):
        return Authority(
            authority_ref="auth://custody",
            request_sha256=request.digest(),
            tenant_id=request.tenant_id,
            principal_id=request.principal_id,
            scope_refs=request.scope_refs,
            engine=request.engine,
            expires_epoch=self._now + 120,
            terms_ref="terms://synthetic",
            policy_epoch=1,
        )


def _request(now_epoch: int) -> Request:
    return Request(
        request_id="request-custody-synthetic",
        tenant_id="tenant-SYNTHETIC",
        principal_id="operator",
        kind="source",
        engine="mtafiti",
        objective_sha256="a" * 64,
        input_refs=("akki://source/descriptor",),
        scope_refs=("source-scope",),
        deadline_epoch=now_epoch + 600,
    )


def _artifact() -> Artifact:
    return Artifact(
        ref="akki://TEST/source-artifact",
        sha256="b" * 64,
        size_bytes=5,
        tenant_id="tenant-SYNTHETIC",
        class_label="non_factual",
    )


def _grant_receipt(keys, request: Request, descriptor_digest: str, delivery_id: str, endpoint: str, *, expires: int):
    details = DeliveryProof(
        delivery_id=delivery_id,
        principal_id=request.principal_id,
        artifact_sha256="b" * 64,
        artifact_size_bytes=5,
        stage="grant",
        provider_event_id="grant-evt-1",
        current_rights_at_redemption=True,
        workspace_touched_bytes=False,
        origin=origin_of(endpoint),
        endpoint_sha256=hashlib.sha256(endpoint.encode()).hexdigest(),
    )
    claims = Observation(
        category="delivery_grant",
        context_sha256=descriptor_digest,
        claim_sha256=digest(details.model_dump(mode="json")),
        evidence_mode="measured",
        delivery=details,
    ).model_dump(mode="json")
    return keys.receipt(
        "observation",
        claims,
        signer="custodian",
        request=request,
        issued_epoch=keys.now - 1,
        expires_epoch=expires,
    )


def _completion_receipt(keys, request: Request, descriptor_digest: str, delivery_id: str, grant_ref: str, *, redeemed: int, completed: int):
    details = DeliveryProof(
        delivery_id=delivery_id,
        principal_id=request.principal_id,
        artifact_sha256="b" * 64,
        artifact_size_bytes=5,
        stage="completed",
        provider_event_id="complete-evt-1",
        current_rights_at_redemption=True,
        workspace_touched_bytes=False,
        grant_receipt_ref=grant_ref,
        redeemed_epoch=redeemed,
        completed_epoch=completed,
        delivered_bytes=5,
        observed_sha256="b" * 64,
    )
    claims = Observation(
        category="delivery_completion",
        context_sha256=descriptor_digest,
        claim_sha256=digest(details.model_dump(mode="json")),
        evidence_mode="measured",
        terminal=True,
        delivery=details,
    ).model_dump(mode="json")
    return keys.receipt(
        "observation",
        claims,
        signer="custodian",
        request=request,
        issued_epoch=keys.now - 1,
        expires_epoch=keys.now + 300,
    )


@pytest.fixture
def estate_and_request():
    keys = native_helpers.Keys()
    keys.permission_override = (
        "activation:observation:delivery_grant",
        "activation:observation:delivery_completion",
    )
    db = _FakeDb(ledger_v1_control_events=native_helpers.ConcurrentCollection())
    receipts = NativeReceipts(db, keys, timeout_seconds=2, clock=lambda: keys.now)
    request = _request(keys.now)
    return keys, db, receipts, request


# Module/feature: positive OFFER->COMPLETED custody flow with real signature verification and URL secrecy.
def test_custody_offer_then_completed_positive(estate_and_request):
    async def run():
        keys, db, receipts, request = estate_and_request
        artifact = _artifact()
        coordinator = FakeCoordinator(db, request, artifact, now_epoch=keys.now)
        await coordinator.seed_registry()
        provider = FakeProvider()
        binding = CustodyBinding(
            receipts=receipts,
            provider=provider,
            custodian_principal_id="custodian",
            allowed_origins=("https://custody.example.invalid",),
            max_grant_seconds=120,
            timeout_seconds=1.0,
            clock=lambda: keys.now,
        )
        svc = CustodyDelivery(binding, coordinator)
        body = DeliveryRequest(artifact_ref=artifact.ref, idempotency_key="delivery-key-001")

        delivery_id = digest({"request": request.digest(), "key": body.idempotency_key})
        endpoint = "https://custody.example.invalid/opaque?token=SYNTHETIC"
        grant = _grant_receipt(keys, request, digest({
            "delivery_id": delivery_id,
            "request_id": request.request_id,
            "request_sha256": request.digest(),
            "tenant_id": request.tenant_id,
            "principal_id": request.principal_id,
            "scope_refs": list(request.scope_refs),
            "artifact": artifact.model_dump(mode="json"),
            "registry_receipt_ref": (await coordinator.journal.read(request))[1]["hash"],
        }), delivery_id, endpoint, expires=keys.now + 30)
        provider.prepare_state = ProviderState(grant=grant, url=SecretStr(endpoint))

        offered = await svc.prepare(request, body)
        assert offered.state == "offered"
        assert offered.url is not None
        assert offered.delivery_verified is False

        grant_ref = offered.receipt_ref
        completion = _completion_receipt(
            keys,
            request,
            digest({
                "delivery_id": delivery_id,
                "request_id": request.request_id,
                "request_sha256": request.digest(),
                "tenant_id": request.tenant_id,
                "principal_id": request.principal_id,
                "scope_refs": list(request.scope_refs),
                "artifact": artifact.model_dump(mode="json"),
                "registry_receipt_ref": (await coordinator.journal.read(request))[1]["hash"],
            }),
            delivery_id,
            grant_ref,
            redeemed=keys.now - 1,
            completed=keys.now - 1,
        )
        provider.status_state = ProviderState(completion=completion)
        done = await svc.status(request, offered.delivery_id)
        assert done.state == "completed"
        assert done.delivery_verified is True
        assert done.url is None

        events_json = json.dumps(await receipts.events())
        assert endpoint not in events_json
        assert "token=SYNTHETIC" not in events_json
        assert "opaque?token" not in repr(offered)

    with scope():
        asyncio.run(run())


# Module/feature: provider timeout records uncertain dispatch and recovers through status without re-prepare.
def test_custody_timeout_then_status_only_recovery(estate_and_request):
    async def run():
        keys, db, receipts, request = estate_and_request
        artifact = _artifact()
        coordinator = FakeCoordinator(db, request, artifact, now_epoch=keys.now)
        await coordinator.seed_registry()
        provider = FakeProvider()
        provider.prepare_error = TimeoutError()
        binding = CustodyBinding(receipts, provider, "custodian", ("https://custody.example.invalid",), 120, 0.01, clock=lambda: keys.now)
        svc = CustodyDelivery(binding, coordinator)
        body = DeliveryRequest(artifact_ref=artifact.ref, idempotency_key="delivery-key-timeout")

        first = await svc.prepare(request, body)
        assert first.state == "uncertain"
        assert provider.prepare_calls == 1

        provider.status_state = ProviderState()
        second = await svc.status(request, first.delivery_id)
        assert second.state in {"pending", "offered", "expired", "uncertain"}
        assert provider.prepare_calls == 1
        assert provider.status_calls == 1

        events = await receipts.events()
        slots = [e["payload"].get("slot") for e in events if e["row"]["resource_type"] == "custody_delivery"]
        assert "dispatch" in slots and "uncertain" in slots

    with scope():
        asyncio.run(run())


# Module/feature: current-rights withdrawal before final status check must deny URL release.
def test_custody_rights_withdrawn_before_return_denies_url(estate_and_request):
    async def run():
        keys, db, receipts, request = estate_and_request
        artifact = _artifact()
        coordinator = FakeCoordinator(db, request, artifact, now_epoch=keys.now)
        await coordinator.seed_registry()
        coordinator._deny_after_first = True
        provider = FakeProvider()
        endpoint = "https://custody.example.invalid/opaque?token=SYNTHETIC"
        binding = CustodyBinding(receipts, provider, "custodian", ("https://custody.example.invalid",), 120, 1.0, clock=lambda: keys.now)
        svc = CustodyDelivery(binding, coordinator)
        body = DeliveryRequest(artifact_ref=artifact.ref, idempotency_key="delivery-key-withdrawn")
        delivery_id = digest({"request": request.digest(), "key": body.idempotency_key})
        descriptor_digest = digest({
            "delivery_id": delivery_id,
            "request_id": request.request_id,
            "request_sha256": request.digest(),
            "tenant_id": request.tenant_id,
            "principal_id": request.principal_id,
            "scope_refs": list(request.scope_refs),
            "artifact": artifact.model_dump(mode="json"),
            "registry_receipt_ref": (await coordinator.journal.read(request))[1]["hash"],
        })
        provider.prepare_state = ProviderState(
            grant=_grant_receipt(keys, request, descriptor_digest, delivery_id, endpoint, expires=keys.now + 30),
            url=SecretStr(endpoint),
        )

        with pytest.raises(Held, match="CUSTODY_RESULT_NOT_CURRENTLY_ADMITTED"):
            await svc.prepare(request, body)

    with scope():
        asyncio.run(run())


# Module/feature: strict URL/origin parser rejects spoofing and unsafe forms with no network access.
@pytest.mark.parametrize(
    "value",
    [
        "http://custody.example.invalid/path",
        "https://user:pass@custody.example.invalid/opaque",
        "https://custody.example.invalid#frag",
        "https://127.0.0.1/opaque",
        "https://[::1]/opaque",
        "https://localhost/opaque",
        "https://custody.example.invalid\\evil",
        "https://custody.example.invalid\r\nHeader:x",
        "https://custody.exämple.invalid/opaque",
        "https://custody.example.invalid:65536/opaque",
    ],
)
def test_custody_origin_validation_rejects_spoofing(value):
    with pytest.raises(Held, match="CUSTODY_ORIGIN_INVALID"):
        origin_of(value)
