"""Actual usage handoff to native entitlement consumers; no prices are invented."""
import json
import math
from datetime import datetime, timezone
from decimal import Decimal
from contracts.dap import MeteredEvent
from services.ledger_writer.mongo_control import digest
from services.ledger_writer.principal_control import append_event
from services.northena.execution_models import Held, WorkerResult
from services.northena.execution_component_models import CommercialSnapshot


class LedgerUsagePublisher:
    def __init__(self, db, journal):
        self.db, self.journal = db, journal

    async def publish(self, request, result, dispatch, raw_meter):
        if not isinstance(result, WorkerResult):
            raise Held("USAGE_RECEIPT_INVALID")
        try:
            result = WorkerResult.model_validate_json(result.model_dump_json())
        except (ValueError, TypeError) as exc:
            raise Held("USAGE_RECEIPT_INVALID") from exc
        if result.evidence_mode != "measured":
            raise Held("MOCKED_USAGE_NOT_CHARGEABLE")
        if result.state not in {"complete", "cancelled", "failed"}:
            raise Held("FINAL_USAGE_NOT_AVAILABLE")
        saved = {row["slot"]: row for row in await self.journal.read(request)}
        for slot, supplied in (("dispatch", dispatch), ("metered", raw_meter)):
            if (slot not in saved or any(saved[slot][key] != supplied.get(key)
                                        for key in ("seq", "hash", "data"))):
                raise Held("USAGE_LEDGER_BINDING_INVALID")
        data = raw_meter["data"]
        if (result.request_sha256 != request.digest() or result.operation_key != dispatch["data"]["operation_key"]
                or result.fence != dispatch["seq"] or not result.usage
                or data["worker_receipt_ref"] != result.receipt_ref
                or data["usage"] != [item.model_dump(mode="json") for item in result.usage]
                or data["evidence_mode"] != "measured"):
            raise Held("USAGE_RECEIPT_BINDING_INVALID")
        if "commercial_snapshot" not in dispatch["data"]:
            raise Held("DISPATCH_COMMERCIAL_SNAPSHOT_MISSING")
        snapshot = CommercialSnapshot.model_validate_json(json.dumps(dispatch["data"]["commercial_snapshot"]))
        if (snapshot.principal_id != request.principal_id or snapshot.licence.terms_identifier != data["terms_ref"]
                or data["terms_ref"] != dispatch["data"]["authority"]["terms_ref"]):
            raise Held("USAGE_TERMS_MISMATCH")
        row = snapshot.catalog_row
        if snapshot.licence.status != "active":
            raise Held("DISPATCH_COMMERCIAL_SNAPSHOT_INVALID")
        if row is None:
            if request.kind != "source":
                raise Held("MODEL_USAGE_CATALOGUE_MISSING")
            return await self.journal.append(request, "usage_handoff", {
                "status": "non_model_consumption_only", "raw_meter_hash": raw_meter["hash"],
                "terms_ref": data["terms_ref"], "evidence_mode": "measured"})
        if (row.status != "listed" or (row.credit_rate is not None
                and (not math.isfinite(row.credit_rate) or row.credit_rate < 0))):
            raise Held("DISPATCH_COMMERCIAL_SNAPSHOT_INVALID")
        try:
            epoch = raw_meter["at_epoch"]
            if type(epoch) is not int:
                raise ValueError("Invalid recorded event time.")
            at = datetime.fromtimestamp(epoch, timezone.utc).isoformat()
        except (KeyError, ValueError, OverflowError, TypeError) as exc:
            raise Held("USAGE_EVENT_TIME_UNAVAILABLE") from exc
        prepared = []
        # Validate every unit before the first commercial effect.
        for item in result.usage:
            value = Decimal(item.quantity)
            quantity = float(value)
            if not math.isfinite(quantity) or Decimal(str(quantity)) != value:
                raise Held("USAGE_QUANTITY_NOT_REPRESENTABLE")
            if row.access_class == "reseller_frontier" and item.unit != "tokens":
                raise Held("CATALOGUE_PRICE_UNIT_MISMATCH")
            prepared.append(MeteredEvent(operation_type=request.kind, accessed_scope=digest(request.scope_refs),
                                        quantity=quantity, quantity_unit=item.unit, terms_id=data["terms_ref"],
                                        party_id=request.principal_id, timestamp_iso=at, au_3b_defensible=False))
        if len({item.quantity_unit for item in prepared}) != len(prepared):
            raise Held("DUPLICATE_USAGE_UNIT")
        receipts = []
        for event in prepared:
            command = digest({"execution": request.digest(), "usage_unit": event.quantity_unit,
                              "handoff": "native_metered_event"})
            saved = await append_event(
                self.db, tenant_id=request.tenant_id, run_id=request.request_id, command_id=command,
                event_type="execution.usage.recorded", resource_type="metered_event", decision="recorded",
                reason_code="ACTUAL_EXECUTION_USAGE", payload={
                    "principal_id": request.principal_id,
                    "organisation_principal_id": snapshot.licence.organisation_principal_id,
                    "metered_event": event.model_dump(mode="json"),
                    "catalog_row_at_event": row.model_dump(mode="json"),
                    "raw_meter_hash": raw_meter["hash"], "worker_receipt_ref": result.receipt_ref,
                    "execution_receipt_ref": result.receipt_ref,
                    "evidence_mode": "measured"},
            )
            receipts.append(saved["row"]["hash"])
        return await self.journal.append(request, "usage_handoff", {
            "status": "native_model_usage_recorded", "meter_receipt_hashes": receipts,
            "terms_ref": data["terms_ref"], "evidence_mode": "measured"})