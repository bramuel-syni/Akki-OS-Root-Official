"""Independent inspector metadata; not bytes or a replacement asset registry."""
from typing import Literal
from contracts.asset_registry import AssetRegistryRecord
from services.northena.execution_models import Artifact, Frozen, Hash, Name, Handle


class InspectionEntry(Frozen):
    artifact: Artifact
    record: AssetRegistryRecord


class InspectorReceipt(Frozen):
    request_sha256: Hash
    operation_key: Name
    worker_receipt_ref: Handle
    inspection_ref: Name
    evidence_mode: Literal["measured", "MOCKED"]
    entries: tuple[InspectionEntry, ...]