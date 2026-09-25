"""Canonical asset writer composition; durable evidence remains in census result receipts."""
from contracts.asset_registry import AssetRegistryRecord, AssetClass, CustodyClass, NamedOwner
from contracts.mtafiti_registry import FreshnessStamp
from services.mtafiti.asset_registry_writer import write_asset_record


def register_outcome(outcome):
    record = AssetRegistryRecord(
        asset_ref=f"census:{outcome['tenant_id']}:{outcome['census_run_id']}:{outcome['source_id']}",
        asset_class=AssetClass.RECEIPT,
        named_owner=NamedOwner(owner_id=outcome["tenant_id"], owner_class="organisation",
                               mandate_source="CP-CENSUS-OPERATIONAL-V1; Canon-9 §3"),
        custody_class=CustodyClass.SENSITIVE,
        freshness_stamp=FreshnessStamp(logged_date=outcome["observed_at"]),
    )
    receipt = write_asset_record(record)
    return {"record": record.model_dump(mode="json"), "receipt": receipt.model_dump(mode="json")}


def restore_registered(payload):
    for entry in payload.get("registry_receipts", []):
        record = AssetRegistryRecord.model_validate(entry["record"])
        receipt = write_asset_record(record)
        if receipt.receipt_id != entry["receipt"]["receipt_id"]:
            raise ValueError("Persisted registry evidence does not match its canonical write receipt.")