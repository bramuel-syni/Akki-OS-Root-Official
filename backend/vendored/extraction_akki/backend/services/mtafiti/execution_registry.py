"""Commit registry envelope to Ledger BEFORE canonical in-process projection.

Only the existing Mtafiti writer publishes asset records. Restoring a committed
version is idempotent; no second collection/writer or unreceipted admission.
"""
import json
from datetime import datetime
from contracts.asset_registry import AssetRegistryRecord, CustodyClass
from services.mtafiti.asset_registry_writer import write_asset_record, _compute_receipt_id
from services.mtafiti.execution_record_models import InspectorReceipt
from services.ledger_writer.mongo_control import digest
from services.ledger_writer.principal_control import CommandConflict
from services.northena.execution_models import Held, WorkerResult
from services.northena.execution_validation import checked_artifacts


class CanonicalRegistry:
    def __init__(self, journal, authority, inspector=None):
        self.journal, self.authority, self.inspector = journal, authority, inspector

    async def verify(self, request, result, operation_key):
        if not isinstance(result, WorkerResult):
            raise Held("REGISTRY_WORKER_EVIDENCE_INVALID")
        try:
            result = WorkerResult.model_validate_json(result.model_dump_json())
        except (ValueError, TypeError) as exc:
            raise Held("REGISTRY_WORKER_EVIDENCE_INVALID") from exc
        if (result.evidence_mode != "measured" or result.request_sha256 != request.digest()
                or result.operation_key != operation_key or result.state != "complete"):
            raise Held("REGISTRY_WORKER_EVIDENCE_INVALID")
        if self.inspector is None:
            raise Held("ARTIFACT_INSPECTOR_NOT_BOUND")
        _, view = await self.authority.context(request)
        receipt = await self.inspector.inspect(request, result, operation_key)
        if not isinstance(receipt, InspectorReceipt):
            raise Held("ARTIFACT_INSPECTION_INVALID")
        receipt = InspectorReceipt.model_validate_json(receipt.model_dump_json())
        if (receipt.request_sha256 != request.digest() or receipt.operation_key != operation_key
                or receipt.worker_receipt_ref != result.receipt_ref or receipt.evidence_mode != "measured"):
            raise Held("ARTIFACT_INSPECTION_BINDING_INVALID")
        artifacts = checked_artifacts(request, result, tuple(entry.artifact for entry in receipt.entries))
        records = []
        for entry in receipt.entries:
            record = entry.record
            if (record.asset_ref != entry.artifact.ref
                    or record.named_owner.owner_id != view.licence.organisation_principal_id
                    or record.named_owner.owner_class != "organisation"
                    or not record.named_owner.mandate_source.strip()
                    or record.custody_class == CustodyClass.FORBIDDEN):
                raise Held("ARTIFACT_CUSTODY_OR_OWNER_INVALID")
            try:
                stamp = datetime.fromisoformat(record.freshness_stamp.logged_date.replace("Z", "+00:00"))
                if stamp.tzinfo is None:
                    raise ValueError("Freshness must carry timezone.")
            except (ValueError, TypeError, AttributeError) as exc:
                raise Held("ARTIFACT_FRESHNESS_UNRESOLVED") from exc
            version = digest({"record": record.model_dump(mode="json"), "artifact": entry.artifact.model_dump(mode="json")})
            frozen = AssetRegistryRecord.model_validate_json(record.model_dump_json())
            frozen.asset_ref = entry.artifact.ref + "@sha256:" + version
            records.append({"record": frozen.model_dump(mode="json"), "receipt_id": _compute_receipt_id(frozen)})
        payload = {"request_sha256": request.digest(), "operation_key": operation_key,
                   "worker_receipt_ref": result.receipt_ref, "inspection_ref": receipt.inspection_ref,
                   "artifacts": [item.model_dump(mode="json") for item in artifacts],
                   "records": records, "evidence_mode": "measured"}
        existing = next((row for row in await self.journal.read(request) if row["slot"] == "registry"), None)
        if existing is None:
            try:
                existing = await self.journal.append(request, "registry", payload)
            except CommandConflict:
                existing = next(row for row in await self.journal.read(request) if row["slot"] == "registry")
        # A fresh inspection may have a new receipt, but not changed admitted facts.
        if ({k: v for k, v in existing["data"].items() if k != "inspection_ref"}
                != {k: v for k, v in payload.items() if k != "inspection_ref"}):
            raise Held("ARTIFACT_REGISTRATION_CHANGED")
        for saved in existing["data"]["records"]:
            receipt = write_asset_record(AssetRegistryRecord.model_validate(saved["record"]))
            if receipt.receipt_id != saved["receipt_id"] or receipt.au_3b_defensible is not False:
                raise Held("CANONICAL_REGISTRY_RECEIPT_MISMATCH")
        return artifacts

    async def revalidate(self, request, artifact_refs):
        rows = await self.journal.read(request)
        dispatch = next((row for row in rows if row["slot"] == "dispatch"), None)
        observations = [row["data"]["result"] for row in rows if row["slot"].startswith("observation:")
                        and row["data"]["result"]["state"] == "complete"]
        if dispatch is None or not observations:
            raise Held("REGISTRY_RESULT_NOT_AVAILABLE")
        result = WorkerResult.model_validate_json(json.dumps(observations[-1]))
        checked = await self.verify(request, result, dispatch["data"]["operation_key"])
        if tuple(item.ref for item in checked) != tuple(artifact_refs):
            raise Held("REGISTRY_RETRIEVAL_IDENTITY_MISMATCH")