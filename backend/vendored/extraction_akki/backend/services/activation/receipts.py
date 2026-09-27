"""Native Ledger receipt resolution and Ed25519 verification; no key store/issuer.

The admitted-key resolver is supplied by the owning estate, never HTTP. A Watch
signature primitive is NOT a trust root. An absent admitted resolver holds.
"""
import asyncio
import json
import time
from typing import Annotated, Literal
from pydantic import Field, model_validator
from services.northena.execution_models import Frozen, Name, Hash, Held
from services.enforce.control_scope import require_control_scope
from services.ledger_writer.principal_control import append_event, read_events
from services.ledger_writer.mongo_control import digest
from services.watch.signature_primitive import watch_verify

RESOURCE = "activation_receipt"
KINDS = Literal["plan", "approval", "allocation", "worker", "observation", "revocation", "certificate"]


class SignedReceipt(Frozen):
    version: Literal["akki.activation.receipt/1"]
    tenant_id: Name
    signer_id: Name
    key_id: Name
    kind: KINDS
    request_sha256: Hash | None
    scope_refs: Annotated[tuple[Name, ...], Field(min_length=1, max_length=1000)]
    issued_epoch: Annotated[int, Field(gt=0)]
    expires_epoch: Annotated[int, Field(gt=0)]
    claims: dict
    signature_hex: Annotated[str, Field(pattern=r"^[0-9a-f]{128}$")]

    @model_validator(mode="after")
    def window(self):
        if self.expires_epoch <= self.issued_epoch or len(set(self.scope_refs)) != len(self.scope_refs):
            raise ValueError("Invalid receipt window or duplicate scope.")
        if len(self.signing_bytes()) > 262144:
            raise ValueError("Receipt metadata exceeds envelope.")
        return self

    def signing_bytes(self):
        body = self.model_dump(mode="json", exclude={"signature_hex"})
        return b"akki.activation.receipt/1\n" + json.dumps(
            body, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


class AdmittedSigner(Frozen):
    """Returned by native admission resolution, NOT accepted in a receipt body."""
    tenant_id: Name
    principal_id: Name
    key_id: Name
    public_key_hex: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
    admission_ref: Name
    permissions: tuple[Name, ...]
    scope_refs: tuple[Name, ...]
    valid_from_epoch: int
    expires_epoch: int
    revoked: bool


class NativeReceipts:
    def __init__(self, db, admitted_keys=None, *, timeout_seconds=None, clock=time.time):
        self.db, self.admitted_keys, self.clock = db, admitted_keys, clock
        self.timeout = timeout_seconds
        if admitted_keys is not None:
            from services.northena.execution_gate_checks import finite_timeout
            finite_timeout(timeout_seconds)
            if not asyncio.iscoroutinefunction(getattr(admitted_keys, "resolve", None)):
                raise ValueError("Native admitted-key resolution must be async.")

    async def verify_signature(self, receipt):
        receipt = SignedReceipt.model_validate_json(receipt.model_dump_json())
        scope = require_control_scope()
        if scope.tenant_id != receipt.tenant_id:
            raise Held("RECEIPT_TENANT_MISMATCH")
        if self.admitted_keys is None:
            raise Held("ADMITTED_SIGNER_RESOLVER_UNBOUND")
        try:
            signer = await asyncio.wait_for(self.admitted_keys.resolve(
                receipt.tenant_id, receipt.signer_id, receipt.key_id), self.timeout)
        except (TimeoutError, ConnectionError, OSError):
            raise Held("ADMITTED_SIGNER_RESOLVER_UNAVAILABLE") from None
        if not isinstance(signer, AdmittedSigner):
            raise Held("SIGNER_ADMISSION_UNVERIFIED")
        signer = AdmittedSigner.model_validate_json(signer.model_dump_json())
        now = self.clock()
        if (signer.tenant_id, signer.principal_id, signer.key_id) != (
                receipt.tenant_id, receipt.signer_id, receipt.key_id):
            raise Held("SIGNER_ADMISSION_MISMATCH")
        if (signer.revoked or not signer.valid_from_epoch <= receipt.issued_epoch <= now
                or now >= min(signer.expires_epoch, receipt.expires_epoch)):
            raise Held("SIGNER_OR_RECEIPT_NOT_CURRENT")
        permission = "activation:" + receipt.kind
        if receipt.kind == "approval":
            permission += ":" + str(receipt.claims.get("group", ""))
        if receipt.kind == "observation":
            permission += ":" + str(receipt.claims.get("category", ""))
        if permission not in signer.permissions or not set(receipt.scope_refs) <= set(signer.scope_refs):
            raise Held("SIGNER_MANDATE_INSUFFICIENT")
        if not watch_verify(bytes.fromhex(signer.public_key_hex), receipt.signing_bytes(),
                            bytes.fromhex(receipt.signature_hex)):
            raise Held("RECEIPT_SIGNATURE_INVALID")
        return receipt

    async def events(self):
        scope = require_control_scope()
        try:
            return await read_events(self.db, {"row.tenant_id": scope.tenant_id})
        except (ValueError, KeyError, TypeError):
            raise Held("NATIVE_CONTROL_LEDGER_INTEGRITY_FAILURE") from None

    async def resolve(self, ref, *, kind=None, request_sha256=None, events=None):
        events = await self.events() if events is None else events
        event = next((e for e in events if e["row"]["hash"] == ref and
                      e["row"]["resource_type"] == RESOURCE), None)
        if event is None:
            raise Held("AUTHORITATIVE_RECEIPT_UNRESOLVED")
        receipt = SignedReceipt.model_validate_json(json.dumps(event["payload"]["receipt"]))
        if (event["payload"]["principal_id"] != event["row"]["actor_id"] or
                receipt.tenant_id != event["row"]["tenant_id"] or
                receipt.issued_epoch > event["row"]["at"]["epoch_s"]):
            raise Held("RECEIPT_PROVENANCE_MISMATCH")
        await self.verify_signature(receipt)
        if kind is not None and receipt.kind != kind:
            raise Held("RECEIPT_KIND_MISMATCH")
        if request_sha256 is not None and receipt.request_sha256 != request_sha256:
            raise Held("RECEIPT_REQUEST_MISMATCH")
        for row in events:
            candidate = row["payload"].get("receipt", {})
            if (row["row"]["resource_type"] == RESOURCE and candidate.get("kind") == "revocation"
                    and candidate.get("claims", {}).get("target_ref") == ref):
                # Invalid revocation evidence holds rather than silently restoring authority.
                await self.verify_signature(SignedReceipt.model_validate_json(json.dumps(candidate)))
                raise Held("RECEIPT_REVOKED")
        return receipt

    async def record(self, receipt):
        receipt = await self.verify_signature(receipt)
        scope = require_control_scope()
        # The current principal relays metadata; the signature proves the producer.
        # Neither the audit actor nor a claimed signer is substituted for the other.
        from services.activation.record_shapes import validate_claims
        validate_claims(receipt)
        if receipt.kind == "revocation":
            target = await self.resolve(receipt.claims["target_ref"])
            if not set(target.scope_refs) <= set(receipt.scope_refs):
                raise Held("REVOCATION_SCOPE_MISMATCH")
        event = await append_event(self.db, tenant_id=scope.tenant_id,
            run_id=receipt.request_sha256 or digest(receipt.model_dump(mode="json")),
            command_id=digest(receipt.model_dump(mode="json")), event_type="activation." + receipt.kind,
            resource_type=RESOURCE, decision="recorded", reason_code="SIGNED_NATIVE_CONTROL",
            payload={"principal_id": scope.principal_id, "receipt": receipt.model_dump(mode="json")})
        return event["row"]["hash"]