"""tools/digicow_read_capability_20260921.py

DigiCow-scoped read-capability check via AWS RDS Data API.

Surface class established from drop probe:
    * region: eu-west-1
    * cluster arn: arn:aws:rds:eu-west-1:494452543252:cluster:db-restore-603-cluster
      (an Aurora cluster — Data API compatible)
    * secret arn: arn:aws:secretsmanager:eu-west-1:494452543252:secret:
      rds/data/api/user/secrets-8rZuVc (Data API service-account secret)
    * databases to survey: digicow_live, ndume

Vantage: DIRECT EGRESS from sandbox pod to AWS eu-west-1 (not via JUMP).

Discipline: read-only. Every SQL executes via ExecuteStatement with
transaction NOT started (auto-commit read-only). Shape-only row proof.
NEVER emit real row values or AWS secret material.

Emits: phase0/connectivity_receipts/{stamp}_DIGICOW_read_capability_
check_owner_authorized_20260921.json
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError, ReadTimeoutError

RECEIPT_DIR = Path("/app/assessment_workspace/phase0/connectivity_receipts")
DIGICOW_XLSX = Path("/app/assessment_workspace/custody/credentials/incoming_20260921/20260921T153705Z_DIGICOW_digicow_xlsx.xlsx")
DIGICOW_CSV = Path("/app/assessment_workspace/custody/credentials/incoming_20260921/20260921T153705Z_DIGICOW_digicow_access_keys_csv.csv")

# Values transcribed from custody probe (structural — safe to name):
AWS_REGION = "eu-west-1"
AWS_ACCOUNT = "494452543252"
CLUSTER_ARN = "arn:aws:rds:eu-west-1:494452543252:cluster:db-restore-603-cluster"
SECRET_ARN = "arn:aws:secretsmanager:eu-west-1:494452543252:secret:rds/data/api/user/secrets-8rZuVc"
DATABASES = ["digicow_live", "ndume"]

# Bounds
MAX_TABLES_PROBED_PER_DB = 25
MAX_COL_META_RETAINED = 40
PROOF_ROW_VALUE_MAX_BYTES = 512


def _now(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_file(p: Path) -> Optional[str]:
    if not p.is_file(): return None
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_ak_sk() -> dict:
    text = DIGICOW_CSV.read_text(encoding="utf-8-sig", errors="replace")
    reader = csv.DictReader(text.splitlines())
    for row in reader:
        ak = (row.get("Access key ID") or "").strip()
        sk = (row.get("Secret access key") or "").strip()
        if ak and sk:
            return {"ak": ak, "sk": sk,
                    "ak_len": len(ak), "sk_len": len(sk),
                    "ak_prefix4": ak[:4]}
    raise RuntimeError("No AK/SK in CSV")


def _redact_field(field: dict) -> dict:
    """RDS Data API returns each cell as a `Field` dict with one of:
    booleanValue, longValue, doubleValue, stringValue, blobValue, isNull.

    Shape-only redaction — never emits stringValue/blobValue content.
    """
    if not isinstance(field, dict):
        return {"unknown_shape": True}
    if field.get("isNull"):
        return {"kind": "NULL", "is_null": True}
    for k in ("booleanValue", "longValue", "doubleValue"):
        if k in field:
            v = field[k]
            entry = {"kind": k, "is_null": False}
            if k == "longValue" and isinstance(v, int):
                entry["int_bit_len"] = v.bit_length()
            return entry
    if "stringValue" in field:
        s = field["stringValue"]
        return {"kind": "stringValue", "is_null": False,
                "char_len": min(len(s), PROOF_ROW_VALUE_MAX_BYTES),
                "byte_len": min(len(s.encode("utf-8", errors="replace")),
                                PROOF_ROW_VALUE_MAX_BYTES)}
    if "blobValue" in field:
        b = field["blobValue"]
        return {"kind": "blobValue", "is_null": False,
                "byte_len": min(len(b), PROOF_ROW_VALUE_MAX_BYTES)}
    if "arrayValue" in field:
        arr = field["arrayValue"] or {}
        for k in ("stringValues", "longValues", "doubleValues", "booleanValues"):
            if k in arr:
                return {"kind": f"arrayValue.{k}", "is_null": False,
                        "n_items": len(arr[k])}
        return {"kind": "arrayValue.empty_or_unknown", "is_null": False}
    return {"kind": "unknown_field_shape", "is_null": None,
            "keys_present": sorted(field.keys())}


def _rds_data_execute(client, sql: str, database: Optional[str] = None,
                      timeout_s: float = 20.0) -> dict:
    """Wrap ExecuteStatement with timeout + error taxonomy."""
    t0 = time.monotonic()
    params = {
        "resourceArn": CLUSTER_ARN,
        "secretArn": SECRET_ARN,
        "sql": sql,
        "includeResultMetadata": True,
    }
    if database:
        params["database"] = database
    try:
        resp = client.execute_statement(**params)
        return {
            "ok": True,
            "elapsed_s": round(time.monotonic() - t0, 3),
            "response": resp,
        }
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code")
        msg = e.response.get("Error", {}).get("Message", "")
        http_status = e.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        # Failure-layer classification
        layer_map = {
            "AccessDeniedException":       "IAM_ACCESS_DENIED_ON_rds_data_ExecuteStatement",
            "BadRequestException":         "BAD_REQUEST_SEE_MESSAGE",
            "InvalidSecretException":      "INVALID_SECRET_ARN_OR_PERMISSION",
            "SecretsErrorException":       "SECRETSMANAGER_ERROR",
            "DatabaseErrorException":      "DATABASE_ERROR_(sql/perm/etc)",
            "DatabaseNotFoundException":   "DATABASE_NOT_FOUND",
            "DatabaseResumingException":   "DB_PAUSED_RESUMING",
            "DatabaseUnavailableException":"DB_UNAVAILABLE",
            "ForbiddenException":          "FORBIDDEN",
            "StatementTimeoutException":   "SQL_TIMEOUT",
            "InternalServerErrorException":"AWS_INTERNAL_ERROR",
        }
        return {
            "ok": False,
            "elapsed_s": round(time.monotonic() - t0, 3),
            "error_code": code,
            "error_message": (msg or "")[:400],
            "http_status": http_status,
            "failure_layer": layer_map.get(code, f"AWS_ERROR_{code}"),
        }
    except (EndpointConnectionError, ReadTimeoutError) as e:
        return {"ok": False,
                "elapsed_s": round(time.monotonic() - t0, 3),
                "error_class": e.__class__.__name__,
                "error_message": str(e)[:400],
                "failure_layer": "NETWORK"}
    except Exception as e:
        return {"ok": False,
                "elapsed_s": round(time.monotonic() - t0, 3),
                "error_class": e.__class__.__name__,
                "error_message": str(e)[:400],
                "failure_layer": "OTHER"}


def _extract_string_column(res: dict) -> list:
    """Extract single-column string results from ExecuteStatement.

    Table names / DB names etc. — these are STRUCTURAL, safe to emit.
    """
    if not res.get("ok"): return []
    body = res.get("response", {})
    records = body.get("records", []) or []
    names = []
    for row in records:
        if row and isinstance(row[0], dict):
            v = row[0].get("stringValue")
            if v is not None:
                names.append(v)
    return names


def _prove_read_of_table(rds_data, database: str, tbl: str) -> dict:
    """DESCRIBE + COUNT + LIMIT 1 shape-only."""
    entry = {"table": tbl}
    # DESCRIBE
    desc = _rds_data_execute(rds_data, f"DESCRIBE `{tbl}`", database=database)
    if desc.get("ok"):
        try:
            body = desc["response"]
            recs = body.get("records", []) or []
            cols = []
            for r in recs:
                # DESCRIBE returns 6 cols: Field, Type, Null, Key, Default, Extra
                if len(r) >= 6:
                    cols.append({
                        "field": r[0].get("stringValue") if isinstance(r[0], dict) else None,
                        "type":  r[1].get("stringValue") if isinstance(r[1], dict) else None,
                        "null":  r[2].get("stringValue") if isinstance(r[2], dict) else None,
                        "key":   r[3].get("stringValue") if isinstance(r[3], dict) else None,
                        "default_present": not r[4].get("isNull", True) if isinstance(r[4], dict) else None,
                        "extra": r[5].get("stringValue") if isinstance(r[5], dict) else None,
                    })
            entry["columns_meta"] = cols[:MAX_COL_META_RETAINED]
        except Exception as e:
            entry["describe_parse_err"] = f"{e.__class__.__name__}: {e}"
    else:
        entry["describe_err"] = desc

    # COUNT
    cnt = _rds_data_execute(rds_data, f"SELECT COUNT(*) FROM `{tbl}`",
                            database=database)
    if cnt.get("ok"):
        try:
            body = cnt["response"]
            recs = body.get("records", []) or []
            if recs and recs[0]:
                entry["count_star"] = recs[0][0].get("longValue")
        except Exception as e:
            entry["count_parse_err"] = f"{e.__class__.__name__}: {e}"
    else:
        entry["count_err"] = cnt

    # LIMIT 1 shape-only
    lim = _rds_data_execute(rds_data, f"SELECT * FROM `{tbl}` LIMIT 1",
                            database=database)
    if lim.get("ok"):
        try:
            body = lim["response"]
            recs = body.get("records", []) or []
            col_metadata = body.get("columnMetadata", []) or []
            col_names = [c.get("name") or c.get("label") for c in col_metadata]
            if not recs:
                entry["proof_of_read"] = {
                    "row_returned": False,
                    "reason": "TABLE_EMPTY_OR_LIMIT_NO_ROW",
                    "col_names": col_names,
                }
            else:
                row = recs[0]
                entry["proof_of_read"] = {
                    "row_returned": True,
                    "col_names": col_names,
                    "value_shape_by_col": {
                        (col_names[i] if i < len(col_names) else f"col_{i}"):
                            _redact_field(field)
                        for i, field in enumerate(row)
                    },
                }
        except Exception as e:
            entry["proof_of_read_parse_err"] = f"{e.__class__.__name__}: {e}"
    else:
        entry["proof_of_read_err"] = lim
    return entry


def main():
    receipt = {
        "task": "DIGICOW_read_capability_check_owner_authorized_20260921",
        "captured_at_utc": _now(),
        "authorization": (
            "Owner directive this-session 2026-09-21T~15:05Z: 'OWNER "
            "CREDENTIAL DROP DIGICOW estate, ingest under §E secret-"
            "hygiene then run a read-capability check STRICTLY scoped "
            "to DigiCow.' R-91 hold unchanged. Ratchet 5858 unchanged."
        ),
        "scope_discipline": (
            "DIGICOW ONLY: no touch to the 8 RMS MySQL clusters, the "
            "OFFAIRRECS/Record CIFS mount, or the RMS Huawei OBS estate."
        ),
        "hygiene": {
            "read_only": True,
            "no_bulk_pulls": True,
            "shape_only_row_proofs": True,
            "creds_by_shape_only": True,
            "aws_secrets_never_emitted": True,
        },
        "cred_source": {
            "digicow_xlsx": str(DIGICOW_XLSX),
            "digicow_xlsx_sha256": _sha256_file(DIGICOW_XLSX),
            "digicow_xlsx_size_bytes": DIGICOW_XLSX.stat().st_size if DIGICOW_XLSX.is_file() else None,
            "access_keys_csv": str(DIGICOW_CSV),
            "access_keys_csv_sha256": _sha256_file(DIGICOW_CSV),
            "access_keys_csv_size_bytes": DIGICOW_CSV.stat().st_size if DIGICOW_CSV.is_file() else None,
        },
        "surface_class": "AWS RDS Aurora via Data API + Secrets Manager",
        "surface_facts_from_drop_structural": {
            "aws_account_id": AWS_ACCOUNT,
            "aws_region": AWS_REGION,
            "cluster_arn": CLUSTER_ARN,
            "secret_arn": SECRET_ARN,
            "expected_databases": DATABASES,
        },
    }

    hw = _load_ak_sk()
    receipt["cred_shape"] = {
        "ak_len": hw["ak_len"], "sk_len": hw["sk_len"],
        "ak_prefix4": hw["ak_prefix4"],
    }

    session = boto3.session.Session(
        aws_access_key_id=hw["ak"],
        aws_secret_access_key=hw["sk"],
        region_name=AWS_REGION,
    )

    # ---- Sanity: STS GetCallerIdentity ------------------------------
    sts = session.client("sts")
    try:
        ident = sts.get_caller_identity()
        receipt["sts_identity"] = {
            "ok": True,
            "account": ident.get("Account"),
            "arn": ident.get("Arn"),
            "user_id": ident.get("UserId"),
        }
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code")
        receipt["sts_identity"] = {"ok": False,
                                   "error_code": code,
                                   "error_message": (e.response.get("Error",{}).get("Message") or "")[:400]}
        # If STS fails, none of the rest will work
        if code in ("InvalidClientTokenId", "SignatureDoesNotMatch"):
            receipt["verdict"] = {"binary_answer": "NO",
                                  "failure_layer": "IAM_CREDENTIAL_INVALID",
                                  "explicit": "Access keys rejected by STS."}
            _emit(receipt); return
    except Exception as e:
        receipt["sts_identity"] = {"ok": False,
                                   "error_class": e.__class__.__name__,
                                   "error_message": str(e)[:400]}

    # ---- Data API probe: SELECT 1 sanity ----------------------------
    rds_data = session.client("rds-data")
    sanity = _rds_data_execute(rds_data, "SELECT 1", database=DATABASES[0])
    receipt["data_api_sanity_select_1"] = {
        "ok": sanity.get("ok"),
        "elapsed_s": sanity.get("elapsed_s"),
        "failure_layer": sanity.get("failure_layer"),
        "error_code": sanity.get("error_code"),
        "error_message": sanity.get("error_message"),
        "http_status": sanity.get("http_status"),
    }
    if not sanity.get("ok"):
        receipt["verdict"] = {
            "binary_answer": "NO",
            "failure_layer": sanity.get("failure_layer"),
            "explicit": (
                f"Data API sanity 'SELECT 1' on database={DATABASES[0]} "
                f"failed: {sanity.get('error_code')} — "
                f"{(sanity.get('error_message') or '')[:200]}"
            ),
        }
        _emit(receipt); return

    # ---- Per-database enumeration + prove-read ----------------------
    receipt["per_database"] = []
    for db in DATABASES:
        db_entry = {"database": db}
        # SHOW TABLES
        show_res = _rds_data_execute(
            rds_data, "SHOW TABLES", database=db, timeout_s=30,
        )
        if not show_res.get("ok"):
            db_entry["show_tables_err"] = show_res
            receipt["per_database"].append(db_entry); continue
        tables = _extract_string_column(show_res)
        db_entry["table_count"] = len(tables)
        db_entry["table_names_first_50"] = tables[:50]

        # Per-table probe (bounded)
        per_table = []
        for tbl in tables[:MAX_TABLES_PROBED_PER_DB]:
            per_table.append(_prove_read_of_table(rds_data, db, tbl))
        db_entry["per_table_probe"] = per_table
        db_entry["tables_probed_of_total"] = f"{len(per_table)} of {len(tables)}"
        # Summary
        db_entry["readable_tables"] = [
            p["table"] for p in per_table
            if p.get("proof_of_read", {}).get("row_returned") is not None
        ]
        db_entry["read_error_tables"] = [
            p["table"] for p in per_table if "proof_of_read_err" in p
        ]
        db_entry["describe_error_tables"] = [
            p["table"] for p in per_table if "describe_err" in p
        ]
        receipt["per_database"].append(db_entry)

    # ---- Verdict ----------------------------------------------------
    total_tables = sum(d.get("table_count", 0) or 0 for d in receipt["per_database"])
    total_readable = sum(len(d.get("readable_tables", []) or [])
                         for d in receipt["per_database"])
    total_probed = sum(int(d.get("tables_probed_of_total", "0").split(" of ")[0])
                       for d in receipt["per_database"] if "tables_probed_of_total" in d)
    total_denied = sum(len(d.get("read_error_tables", []) or [])
                       for d in receipt["per_database"])

    verdict = {
        "surface_class": "AWS RDS Aurora via Data API + Secrets Manager",
        "databases": DATABASES,
        "total_tables_across_dbs": total_tables,
        "total_tables_probed": total_probed,
        "total_readable_of_probed": total_readable,
        "total_denied_of_probed": total_denied,
    }
    if total_readable == total_probed and total_probed > 0:
        verdict["binary_answer"] = "YES"
        verdict["explicit"] = (
            f"CAN READ. All {total_probed} probed tables succeeded on "
            f"SELECT-LIMIT-1 shape-proof (of {total_tables} total tables "
            f"across {len(DATABASES)} databases). Data API is fully "
            "operational; IAM AK/SK has the required rds-data:* + "
            "secretsmanager:GetSecretValue permissions."
        )
    elif total_readable > 0 and total_denied > 0:
        verdict["binary_answer"] = "PARTIAL"
        verdict["explicit"] = (
            f"PARTIAL. {total_readable}/{total_probed} probed tables "
            "read OK; some hit permission errors — see read_error_tables."
        )
    elif total_readable == 0 and total_probed > 0:
        verdict["binary_answer"] = "NO"
        verdict["explicit"] = (
            "Enumerate succeeded but no proof-of-read on any table."
        )
    else:
        verdict["binary_answer"] = "AMBIGUOUS"
        verdict["explicit"] = "Inspect per_database section."
    receipt["verdict"] = verdict

    _emit(receipt)


def _emit(receipt):
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    p = RECEIPT_DIR / f"{stamp}_DIGICOW_read_capability_check_owner_authorized_20260921.json"
    p.write_text(json.dumps(receipt, indent=2, default=str) + "\n",
                 encoding="utf-8")
    print(f"receipt_path: {p}")


if __name__ == "__main__":
    main()
