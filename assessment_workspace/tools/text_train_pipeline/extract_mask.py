"""Extract + mask a slice of `digicow_live.ussd_question_response` for the
governed text-training run.

Authority: owner ruling 6 · 2026-08-31 (verbatim in DECISIONS.md).

Discipline:
  - Reads via AWS Data API using credentials from
    ESTATE_KEYS_DIR/data_sources/db-restore-603-cluster.json (mode-0600).
  - Column-exclusion happens at SQL level: SELECT only INCLUDED columns.
    This means PII columns never leave the RDS chokepoint at all — they
    are not read.
  - Regex scrub applied to each row's free text BEFORE writing anywhere.
  - Emits a governed crossing receipt kind='ruling6_bypass_row_extract'
    with shape-only fields (row count, column list, masking-step summary
    — NEVER content).
  - Deterministic sampling: ORDER BY id LIMIT <slice_size> OFFSET 0
    (first N rows by primary key — stable across re-runs).
  - Refuses to run if AKKI_ENV is not 'development'.
  - Written JSONL contains ONE dict per line; each dict has only the
    3 INCLUDED columns + the pre-composed training_text.
  - Sha256 of the JSONL is computed + logged (used for transport-verification).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

# The mask module lives in the same package.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mask import (
    DECISION_LEDGER, INCLUDED_COLUMNS, EXCLUDED_COLUMNS,
    mask_row, build_training_text,
)


CROSSING_RECEIPT_DIR = Path(os.environ.get(
    "CROSSING_RECEIPT_DIR",
    "/app/assessment_workspace/phase0/crossing_receipts",
))
CROSSING_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)


def _iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_aws_creds() -> Dict[str, str]:
    creds_path = Path(os.environ.get(
        "ESTATE_KEYS_DIR", "/app/backend/estate_keys",
    )) / "data_sources" / "db-restore-603-cluster.json"
    if not creds_path.exists():
        raise SystemExit(f"credentials not found: {creds_path}")
    j = json.loads(creds_path.read_text())
    return {
        "cluster_arn": j["cluster_arn"],
        "secret_arn": j["secret_arn"],
        "region": j["region"],
        "database": j["database"],
        "aws_access_key_id": j["aws_access_key_id"],
        "aws_secret_access_key": j["aws_secret_access_key"],
    }


def _execute_statement(client, *, cluster_arn: str, secret_arn: str,
                       database: str, sql: str) -> List[Dict[str, Any]]:
    """Run a paginated SELECT via Aurora Data API and return list of dicts.
    Data API caps each call at ~1MB response; page via LIMIT/OFFSET is the
    caller's job.
    """
    resp = client.execute_statement(
        resourceArn=cluster_arn,
        secretArn=secret_arn,
        database=database,
        sql=sql,
        includeResultMetadata=True,
    )
    cols = [c["name"] for c in resp["columnMetadata"]]
    rows = []
    for record in resp["records"]:
        row = {}
        for name, cell in zip(cols, record):
            row[name] = _cell_value(cell)
        rows.append(row)
    return rows


def _cell_value(cell: Dict[str, Any]) -> Any:
    if cell.get("isNull"):
        return None
    for k in ("stringValue", "longValue", "doubleValue", "booleanValue"):
        if k in cell:
            return cell[k]
    return None


def emit_crossing_receipt(*, run_id: str, slice_size: int, actual_rows: int,
                          jsonl_path: str, jsonl_sha256: str) -> Path:
    """Emit a governed crossing receipt with SHAPE-ONLY fields."""
    rid = f"rcp-txtxtr-{run_id}"
    receipt = {
        "receipt_id": rid,
        "kind": "ruling6_bypass_row_extract",
        "at_iso": _iso(),
        "actor": "tools.text_train_pipeline.extract_mask · ussd_question_response",
        "endpoint_cluster_arn_prefix": "arn:aws:rds:eu-west-1:*:cluster:db-restore-603-cluster",
        "residency_region": "eu-west-1",
        "masking_tier": "ruling6_bypass",
        "authority_verbatim": "owner ruling 6 · 2026-08-31 · estate-text training pivot (banked in DECISIONS.md)",
        "shielded_pipeline_status": "NOT_YET_BUILT · charter W-Shield-Train in SPRINT_PLAN.md · bypass applies to build gap only, PII rules upheld",
        "verb": "SELECT",
        "payload_shape": {
            "database": "digicow_live",
            "table": "ussd_question_response",
            "slice_size_requested": slice_size,
            "rows_extracted": actual_rows,
            "columns_included": INCLUDED_COLUMNS,
            "columns_excluded": EXCLUDED_COLUMNS,
            "decision_ledger_sha256": _decision_ledger_hash(),
            "sql_where_clause_none": True,
            "sql_order_by": "id ASC (deterministic)",
            "sql_limit": slice_size,
            "regex_scrub_categories": ["kenyan_phone_number", "id_shaped_numeric_7_to_10_digits"],
            "output_jsonl_sha256": jsonl_sha256,
            "output_jsonl_path": jsonl_path,
        },
    }
    p = CROSSING_RECEIPT_DIR / f"{rid}.json"
    p.write_text(json.dumps(receipt, indent=2, sort_keys=True))
    return p


def _decision_ledger_hash() -> str:
    """Hash of the current decision ledger (for audit-trail reproducibility)."""
    canonical = json.dumps(DECISION_LEDGER, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--slice-size", type=int, required=True,
                   help="Number of rows to extract (ORDER BY id LIMIT).")
    p.add_argument("--out-dir", type=str, required=True,
                   help="Where to write masked_corpus.jsonl.")
    p.add_argument("--run-id", type=str, required=True)
    p.add_argument("--page-size", type=int, default=1000,
                   help="Data API page size (rows per ExecuteStatement).")
    args = p.parse_args()

    akki_env = os.environ.get("AKKI_ENV", "development")
    if akki_env != "development":
        raise SystemExit(f"refuses to run under AKKI_ENV={akki_env!r}; owner bypass ruling 6 was authorized under development only")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Late import so tests can run without boto3 stack.
    try:
        import boto3
    except Exception as e:
        raise SystemExit(f"boto3 not available: {e}")

    creds = _load_aws_creds()

    # Load AWS creds into env for boto3 (matches services.connect pattern).
    os.environ["AWS_ACCESS_KEY_ID"] = creds["aws_access_key_id"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = creds["aws_secret_access_key"]

    client = boto3.client("rds-data", region_name=creds["region"])

    # Only INCLUDED columns are read.
    select_cols = ", ".join(INCLUDED_COLUMNS)

    total_rows = 0
    dropped_empty_qa = 0
    scrubs_applied = {"phone": 0, "id": 0}
    jsonl_path = out_dir / "masked_corpus.jsonl"

    print(f"[extract] slice_size={args.slice_size} page_size={args.page_size}", flush=True)
    print(f"[extract] included_cols={INCLUDED_COLUMNS}", flush=True)
    print(f"[extract] excluded_cols={EXCLUDED_COLUMNS}", flush=True)
    print(f"[extract] output={jsonl_path}", flush=True)

    with open(jsonl_path, "w") as fw:
        offset = 0
        while total_rows < args.slice_size:
            remaining = args.slice_size - total_rows
            page_limit = min(args.page_size, remaining)
            sql = (
                f"SELECT {select_cols} "
                f"FROM ussd_question_response "
                f"ORDER BY id ASC "
                f"LIMIT {page_limit} OFFSET {offset}"
            )
            rows = _execute_statement(
                client,
                cluster_arn=creds["cluster_arn"],
                secret_arn=creds["secret_arn"],
                database=creds["database"],
                sql=sql,
            )
            if not rows:
                print(f"[extract] no more rows at offset={offset}; stopping", flush=True)
                break
            for raw in rows:
                # NB: raw only has INCLUDED_COLUMNS keys (SQL filtered).
                # But mask_row expects ALL columns known to the ledger for
                # its unclassified-refusal invariant. We synthesize the
                # excluded keys as absent by passing only the included set.
                # To keep the refusal invariant sharp, we augment with the
                # excluded columns as None (auditor equivalent).
                augmented = {c: raw.get(c) for c in INCLUDED_COLUMNS}
                for c in EXCLUDED_COLUMNS:
                    augmented[c] = None
                masked = mask_row(augmented)
                # Count scrub applications by delta length (approximate).
                for c in INCLUDED_COLUMNS:
                    original = str(raw.get(c) or "")
                    scrubbed = masked[c]
                    if "[PHONE]" in scrubbed and "[PHONE]" not in original:
                        scrubs_applied["phone"] += scrubbed.count("[PHONE]")
                    if "[ID]" in scrubbed and "[ID]" not in original:
                        scrubs_applied["id"] += scrubbed.count("[ID]")
                training_text = build_training_text(masked)
                if not training_text:
                    dropped_empty_qa += 1
                    continue
                out = dict(masked)
                out["training_text"] = training_text
                fw.write(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
                fw.write("\n")
                total_rows += 1
                if total_rows >= args.slice_size:
                    break
            print(f"[extract] page offset={offset} → total_kept={total_rows} dropped_empty={dropped_empty_qa}", flush=True)
            offset += len(rows)

    jsonl_sha256 = _sha256_file(jsonl_path)
    print(f"[extract] wrote {total_rows} lines to {jsonl_path}", flush=True)
    print(f"[extract] sha256={jsonl_sha256}", flush=True)
    print(f"[extract] scrubs: phone_replacements={scrubs_applied['phone']} id_replacements={scrubs_applied['id']}", flush=True)
    print(f"[extract] dropped_empty_qa={dropped_empty_qa}", flush=True)

    receipt = emit_crossing_receipt(
        run_id=args.run_id,
        slice_size=args.slice_size,
        actual_rows=total_rows,
        jsonl_path=str(jsonl_path),
        jsonl_sha256=jsonl_sha256,
    )
    print(f"[extract] receipt: {receipt}", flush=True)

    # scrub AWS creds from env
    os.environ.pop("AWS_ACCESS_KEY_ID", None)
    os.environ.pop("AWS_SECRET_ACCESS_KEY", None)

    # Emit summary JSON alongside the JSONL
    summary = {
        "run_id": args.run_id,
        "at_iso": _iso(),
        "database": "digicow_live",
        "table": "ussd_question_response",
        "slice_size_requested": args.slice_size,
        "rows_extracted": total_rows,
        "dropped_empty_qa": dropped_empty_qa,
        "scrub_replacements": scrubs_applied,
        "included_columns": INCLUDED_COLUMNS,
        "excluded_columns": EXCLUDED_COLUMNS,
        "decision_ledger_sha256": _decision_ledger_hash(),
        "output_jsonl": str(jsonl_path),
        "output_jsonl_sha256": jsonl_sha256,
        "crossing_receipt": str(receipt),
    }
    (out_dir / "extract_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
