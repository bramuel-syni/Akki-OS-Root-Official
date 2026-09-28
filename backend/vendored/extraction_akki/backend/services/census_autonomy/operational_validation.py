"""Aggregate-only receipt contract. Unknown fields fail closed, never disappear silently."""
from datetime import datetime

PROTOCOL = "akki-census-aggregate-v1"
COMMON = {"protocol", "census_run_id", "tenant_id", "source_id", "execution_location",
          "observed_at", "status", "worker_receipt_id", "source_rows_returned"}
COUNTS = {"database_count", "table_count", "row_count_estimate"}


def validate_output(value, run_id, tenant, source):
    if isinstance(value,dict) and value.get('protocol')=='akki-census-deep-v1':
        from services.census_autonomy.deep_validation import validate_deep
        return validate_deep(value,run_id,tenant,source)
    if not isinstance(value, dict) or set(value) - COMMON - COUNTS - {"reason_code"}:
        raise ValueError("Unexpected worker output; aggregate-only contract refused.")
    expected = {"protocol": PROTOCOL, "census_run_id": run_id, "tenant_id": tenant,
                "source_id": source, "source_rows_returned": 0}
    if any(value.get(k) != v for k, v in expected.items()):
        raise ValueError("Worker output does not match the admitted commission.")
    if type(value.get("source_rows_returned")) is not int:
        raise ValueError("Invalid source-row attestation.")
    if value.get("status") not in {"complete", "blocked"}:
        raise ValueError("Worker outcome is not recognized.")
    stamp = datetime.fromisoformat(value.get("observed_at", "").replace("Z", "+00:00"))
    if stamp.tzinfo is None:
        raise ValueError("UTC timestamp absent.")
    if value["status"] == "complete":
        if value.get("execution_location") != "akki_host" or not isinstance(value.get("worker_receipt_id"), str) or not value["worker_receipt_id"]:
            raise ValueError("Akki-owned worker evidence absent.")
        for key in COUNTS:
            if type(value.get(key)) is not int or value[key] < 0:
                raise ValueError("Worker counts must be nonnegative integers.")
    elif not value.get("reason_code") or value.get("execution_location") not in {"akki_host", "control_plane"}:
        raise ValueError("Blocked worker must record a reason.")
    return dict(value)


def classify_payload(payload):
    if payload.get("protocol") != PROTOCOL or not payload.get("outcomes"):
        return "UNVERIFIED"
    good = [x for x in payload["outcomes"] if x.get("status") in {"complete", "partial"}]
    if good and len(payload.get("registry_receipts", [])) != len(good):
        return "UNVERIFIED"
    if not good:
        return "BLOCKED"
    return "COMPLETE" if all(x.get('status')=='complete' for x in payload['outcomes']) else "PARTIAL"