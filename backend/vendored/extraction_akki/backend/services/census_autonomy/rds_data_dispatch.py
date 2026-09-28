"""DigiCow census driver — Aurora MySQL via the AWS RDS Data API.

DigiCow's Aurora cluster is read through the managed RDS Data API (an AWS HTTPS
endpoint, not a raw DB socket). Aggregate-only: table + estimated-row counts per
admitted database. Credentials + ARNs come from the 0600 estate-access custody
file, never from .env plaintext.
"""
import hashlib
import json
import os
import time
from pathlib import Path

from services.census_autonomy.operational_validation import PROTOCOL
from services.census_autonomy import operational_store as store

_AGG_SQL = ("SELECT COUNT(*), COALESCE(SUM(TABLE_ROWS), 0) FROM information_schema.TABLES "
            "WHERE TABLE_SCHEMA = DATABASE()")


def _access():
    path = os.environ.get("AKKI_ESTATE_ACCESS_CONFIG") or os.environ["AKKI_CENSUS_JUMP_CONFIG"]
    return json.loads(Path(path).read_text())["digicow"]


def _blocked(run_id, tenant, source, reason_code, where="control_plane"):
    return {"protocol": PROTOCOL, "census_run_id": run_id, "tenant_id": tenant,
            "source_id": source, "execution_location": where, "observed_at": store.now(),
            "status": "blocked", "worker_receipt_id": None, "source_rows_returned": 0,
            "reason_code": reason_code}


def execute_source(run_id, tenant, source, lawful_hash, deadline):
    import boto3
    if int(deadline - time.time()) <= 3:
        return _blocked(run_id, tenant, source, "BUDGET_EXHAUSTED")
    result = {"protocol": PROTOCOL, "census_run_id": run_id, "tenant_id": tenant,
              "source_id": source, "execution_location": "akki_host", "source_rows_returned": 0,
              "observed_at": store.now(), "status": "blocked"}
    details, dbs, tbls, rows, ok = [], 0, 0, 0, 0
    try:
        cfg = _access()
        client = boto3.client("rds-data", region_name=cfg["region"],
                              aws_access_key_id=cfg["aws_access_key_id"],
                              aws_secret_access_key=cfg["aws_secret_access_key"])
        max_db = int(os.environ["CENSUS_MAX_DATABASES"])
        for db in cfg["databases"][:max_db]:
            entry = {"label": db, "status": "blocked"}
            try:
                resp = client.execute_statement(resourceArn=cfg["cluster_arn"],
                                                secretArn=cfg["secret_arn"], database=db, sql=_AGG_SQL)
                rec = resp["records"][0]
                t = int(list(rec[0].values())[0]); r = int(list(rec[1].values())[0])
                dbs += 1; tbls += t; rows += r; ok += 1
                entry.update(status="complete", database_count=1, table_count=t, row_count_estimate=r)
            except Exception as exc:  # noqa: BLE001 per-database isolation
                entry["reason_code"] = type(exc).__name__
            details.append(entry)
        if ok:
            result.update(status="complete", database_count=dbs, table_count=tbls, row_count_estimate=rows)
        else:
            result["reason_code"] = "ALL_DATABASES_UNAVAILABLE"
    except Exception as exc:  # noqa: BLE001
        result["reason_code"] = "AKKI_RDS_" + type(exc).__name__
    result["worker_receipt_id"] = "cwr-" + hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
    _bank(run_id, source, {"stage": "rds_data", "route": "aws_rds_data",
                           "worker_status": result["status"], "connections": details})
    return result


def _bank(run_id, source, payload):
    path = store.cursor_dir() / f"transport-{run_id}-{source}.json"
    path.write_text(json.dumps({"census_run_id": run_id, "source_id": source, "at_utc": store.now(),
                                "execution_location": "rds_data", **payload}, indent=2))
