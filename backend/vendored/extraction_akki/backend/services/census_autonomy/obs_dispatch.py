"""Huawei OBS census driver — object-store estate inventory.

Reads the RMS Huawei OBS estate via its S3-compatible endpoint (managed HTTPS
API). Aggregate-only inventory: the census reports the bucket count as
`database_count`; `table_count`/`row_count_estimate` stay 0 because a full
object-level walk is a separate bounded pass (bucket names are banked to custody,
never into the receipt). Credentials come from the 0600 estate-access custody.
"""
import hashlib
import json
import os
import time
from pathlib import Path

from services.census_autonomy.operational_validation import PROTOCOL
from services.census_autonomy import operational_store as store


def _access():
    path = os.environ.get("AKKI_ESTATE_ACCESS_CONFIG") or os.environ["AKKI_CENSUS_JUMP_CONFIG"]
    return json.loads(Path(path).read_text())["obs"]


def _blocked(run_id, tenant, source, reason_code, where="control_plane"):
    return {"protocol": PROTOCOL, "census_run_id": run_id, "tenant_id": tenant,
            "source_id": source, "execution_location": where, "observed_at": store.now(),
            "status": "blocked", "worker_receipt_id": None, "source_rows_returned": 0,
            "reason_code": reason_code}


def execute_source(run_id, tenant, source, lawful_hash, deadline):
    import boto3
    from botocore.client import Config
    if int(deadline - time.time()) <= 3:
        return _blocked(run_id, tenant, source, "BUDGET_EXHAUSTED")
    result = {"protocol": PROTOCOL, "census_run_id": run_id, "tenant_id": tenant,
              "source_id": source, "execution_location": "akki_host", "source_rows_returned": 0,
              "observed_at": store.now(), "status": "blocked"}
    bucket_names = []
    try:
        cfg = _access()
        s3 = boto3.client("s3", endpoint_url=cfg["endpoint"], region_name=cfg["region"],
                          aws_access_key_id=cfg["access_key_id"],
                          aws_secret_access_key=cfg["secret_access_key"],
                          config=Config(signature_version="s3v4", connect_timeout=10,
                                        read_timeout=20, retries={"max_attempts": 1}))
        buckets = s3.list_buckets().get("Buckets", [])
        bucket_names = [b["Name"] for b in buckets]
        result.update(status="complete", database_count=len(buckets), table_count=0, row_count_estimate=0)
    except Exception as exc:  # noqa: BLE001
        result["reason_code"] = "AKKI_OBS_" + type(exc).__name__
    result["worker_receipt_id"] = "cwr-" + hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
    _bank(run_id, source, {"stage": "obs_inventory", "route": "huawei_obs",
                           "worker_status": result["status"], "bucket_count": len(bucket_names),
                           "note": "database_count == bucket count; object-level census is a bounded follow-on",
                           "buckets": bucket_names})
    return result


def _bank(run_id, source, payload):
    path = store.cursor_dir() / f"transport-{run_id}-{source}.json"
    path.write_text(json.dumps({"census_run_id": run_id, "source_id": source, "at_utc": store.now(),
                                "execution_location": "obs_inventory", **payload}, indent=2))
