from typing import Annotated, Literal
from pydantic import Field, SecretStr, model_validator
from services.northena.execution_models import Frozen, Name, Hash, Artifact
from services.ledger_writer.mongo_control import digest


class DeliveryDescriptor(Frozen):
    delivery_id: Hash
    request_id: Name
    request_sha256: Hash
    tenant_id: Name
    principal_id: Name
    scope_refs: tuple[Name, ...]
    artifact: Artifact
    registry_receipt_ref: Hash

    def digest(self):
        return digest(self.model_dump(mode='json'))


class DeliveryProof(Frozen):
    delivery_id: Hash
    principal_id: Name
    artifact_sha256: Hash
    artifact_size_bytes: Annotated[int, Field(ge=0)]
    stage: Literal['grant', 'completed']
    provider_event_id: Annotated[str, Field(min_length=1, max_length=256, pattern=r'^[A-Za-z0-9._:/-]+$')]
    current_rights_at_redemption: Literal[True]
    workspace_touched_bytes: Literal[False]
    origin: Name | None = None
    endpoint_sha256: Hash | None = None
    grant_receipt_ref: Hash | None = None
    redeemed_epoch: int | None = None
    completed_epoch: int | None = None
    delivered_bytes: int | None = None
    observed_sha256: Hash | None = None

    @model_validator(mode='after')
    def stages(self):
        completion = (self.grant_receipt_ref, self.redeemed_epoch, self.completed_epoch,
                      self.delivered_bytes, self.observed_sha256)
        if self.stage == 'grant':
            if self.origin is None or self.endpoint_sha256 is None or any(v is not None for v in completion):
                raise ValueError('Grant is a capability, not completion evidence.')
        elif (any(v is None for v in completion) or self.origin is not None or self.endpoint_sha256 is not None
              or not 0 < self.redeemed_epoch <= self.completed_epoch or self.delivered_bytes < 0):
            raise ValueError('Complete measured delivery evidence is required.')
        return self


class DeliveryRequest(Frozen):
    artifact_ref: Annotated[str, Field(min_length=1, max_length=512)]
    idempotency_key: Annotated[str, Field(min_length=8, max_length=128, pattern=r'^[A-Za-z0-9._-]+$')]


class DeliveryView(Frozen):
    delivery_id: Hash
    request_id: Name
    state: Literal['pending', 'offered', 'uncertain', 'expired', 'completed']
    receipt_ref: Hash | None = None
    completion_receipt_ref: Hash | None = None
    artifact_ref: Name
    artifact_sha256: Hash
    artifact_size_bytes: int
    expires_epoch: int | None = None
    # Explicit serialization only in the authenticated no-store response.
    url: SecretStr | None = Field(default=None, repr=False)
    delivery_verified: bool = False