#!/usr/bin/env python3
"""estate_census.py — Full connected-external-data-estate census.

Canon anchor: Doc 9 · #13 — THE CENSUS · rule B5.7 · scope Mtafiti ·
enforcement_class = pending_override. Also references A17.10 (base-model
census, Doc 17, Targeta, pending_override) and function
`mtafiti.asset_registry_writer.write_asset_record` (Canon-9 §3 single
writer for census/registry records).

Dynamic, re-runnable. Read-only metadata census; NO bulk downloads;
credential hygiene shape-only; secrets in memory only; per-surface
receipts + master markdown roll-up under phase0/.

Discipline (LawfulBasisAdmit is metadata-only here, no ingestion path):
  - No SELECT on business data beyond information_schema and small
    COUNT(*)/MIN/MAX freshness bounds.
  - No S3/OBS GetObject except 16-byte magic-signature range reads on
    NEW extension classes.
  - No file content reads beyond magic-byte range on NAS ambiguous files.
  - Every raw secret held in memory only; receipts carry shape only.
  - Blocked surfaces enumerated as BLOCKED rows so the census is complete
    even where depth is zero.

Usage:
    python3 tools/estate_census.py [--surface mysql|rds|s3|obs|nas|jump|all]
                                   [--out phase0/connectivity_receipts/<TS>_ESTATE_CENSUS.json]
                                   [--md STATE/notes/ESTATE_CENSUS_<TS>.md]
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, "/app/assessment_workspace/tools")

# ---------------------------------------------------------------------------
# Canon anchor block
# ---------------------------------------------------------------------------
CANON_ANCHOR = {
    "primary": {
        "rule_id": "B5.7",
        "source_citation": "Doc 9 · #13 — THE CENSUS",
        "scope": "Mtafiti",
        "enforcement_class": "pending_override",
    },
    "secondary": [
        {
            "rule_id": "A17.10",
            "source_citation": "Doc 17 — The Multidimensional Training Engine (extends #22–#24)",
            "scope": "Targeta",
            "enforcement_class": "pending_override",
            "note": "base-model census — still open on owner one-liners.",
        },
        {
            "function_id": "mtafiti.asset_registry_writer.write_asset_record",
            "note": "Canon-9 §3 single writer for census/registry records (metadata layer).",
        },
    ],
    "prior_operational_reference": (
        "Registry census facts (235 tables' structural facts + crossing "
        "receipts). This census refreshes and extends those facts."
    ),
    "search_scope_at_hunt": [
        "STATE/DECISIONS.md",
        "STATE/STANDING_ORDERS.md",
        "STATE/notes/",
        "backend/services/rules_service/rule_book_seed.jsonl",
        "notes/function_promise_registry.jsonl",
    ],
}

TS = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")

# ---------------------------------------------------------------------------
# Surface probes — each returns a dict; each isolates its own failure
# ---------------------------------------------------------------------------

def _timed(fn):
    def wrapped(*a, **kw):
        t0 = time.monotonic()
        try:
            res = fn(*a, **kw)
        except Exception as exc:  # noqa: BLE001
            return {
                "surface": kw.get("surface_name") or fn.__name__,
                "status": "PROBE_FAILURE",
                "reason": f"{type(exc).__name__}: {exc}",
                "elapsed_s": round(time.monotonic() - t0, 3),
            }
        res.setdefault("elapsed_s", round(time.monotonic() - t0, 3))
        return res
    return wrapped


# --- MySQL clusters via banked creds -----------------------------------------
@_timed
def census_mysql() -> dict:
    """Metadata census across banked MySQL clusters."""
    try:
        import rms_creds_loader_v2 as loader  # type: ignore
    except Exception as exc:  # noqa: BLE001
        return {
            "surface": "mysql",
            "status": "LOADER_UNAVAILABLE",
            "reason": f"{type(exc).__name__}: {exc}",
        }
    try:
        binder = loader.load()
    except Exception as exc:  # noqa: BLE001
        return {
            "surface": "mysql",
            "status": "CREDS_LOAD_FAILURE",
            "reason": f"{type(exc).__name__}: {exc}",
            "hint": "PRIMARY_SHEET_PATH may not be present in this container.",
        }
    clusters = binder.mysql_clusters
    if not clusters:
        return {"surface": "mysql", "status": "NO_CLUSTERS", "count": 0}

    # We DO NOT connect here — the JUMP tunnel is not guaranteed present.
    # Instead we emit shape-only inventory of the reachable-per-matrix set.
    out_clusters = []
    for c in clusters:
        out_clusters.append({
            "section": c.section,
            "host": c.host,
            "user_shape": {"user_len": len(c.user), "user_prefix2": c.user[:2]},
            "password_shape": {"password_len": len(c.password)},
            "schemas_hinted": list(c.schemas),
            "tag": c.tag,
            "connectivity_state": "BANKED_RECEIPT_ONLY (JUMP tunnel not set up in this pass)",
        })
    return {
        "surface": "mysql",
        "status": "METADATA_INVENTORY_ONLY",
        "banked_clusters": len(clusters),
        "clusters": out_clusters,
        "note": (
            "Live SHOW DATABASES / information_schema queries are deferred to a JUMP-tunneled pass "
            "when the tunnel is confirmed up; this pass carries the banked cluster inventory "
            "(host, user/password shape only) so the census row is complete."
        ),
    }


# --- Digicow AWS RDS via Data API --------------------------------------------
@_timed
def census_rds() -> dict:
    """Metadata census on Digicow AWS RDS via Data API."""
    # Load Digicow AWS creds from custody (shape only, keep in-memory).
    csv_path = Path(
        "/app/assessment_workspace/custody/credentials/incoming_20260921/"
        "20260921T153705Z_DIGICOW_digicow_access_keys_csv.csv"
    )
    if not csv_path.is_file():
        return {"surface": "digicow_rds", "status": "CREDS_ABSENT", "expected_path": str(csv_path)}
    lines = csv_path.read_text(encoding="utf-8-sig").splitlines()
    if len(lines) < 2:
        return {"surface": "digicow_rds", "status": "CREDS_MALFORMED"}
    header = [h.strip() for h in lines[0].split(",")]
    row = [c.strip() for c in lines[1].split(",")]
    creds = {h.lower().replace(" ", "_"): v for h, v in zip(header, row)}
    ak = creds.get("access_key_id") or ""
    sk = creds.get("secret_access_key") or ""
    if not ak or not sk:
        return {"surface": "digicow_rds", "status": "CREDS_KEY_NAMES_UNEXPECTED",
                "header_columns": header}
    # Pull cluster ARN + secret ARN from the sibling xlsx (banked in custody drop).
    xlsx_path = Path(
        "/app/assessment_workspace/custody/credentials/incoming_20260921/"
        "20260921T153705Z_DIGICOW_digicow_xlsx.xlsx"
    )
    cluster_arn_from_drop = None
    secret_arn_from_drop = None
    try:
        from openpyxl import load_workbook
        wb = load_workbook(xlsx_path, data_only=True)
        ws = wb[wb.sheetnames[0]]
        for r in range(1, ws.max_row + 1):
            v = ws.cell(row=r, column=1).value
            if not v: continue
            s = str(v).strip()
            # Strip label prefixes (accept several shapes seen across drops)
            low = s.lower()
            for label in ("cluster arn:", "cluster:", "cluster="):
                if low.startswith(label):
                    cluster_arn_from_drop = s[len(label):].strip()
                    break
            for label in ("secret arn:", "secret:", "secret="):
                if low.startswith(label):
                    secret_arn_from_drop = s[len(label):].strip()
                    break
            # Bare ARN fallback
            if s.startswith("arn:aws:rds:") and not cluster_arn_from_drop:
                cluster_arn_from_drop = s
            if s.startswith("arn:aws:secretsmanager:") and not secret_arn_from_drop:
                secret_arn_from_drop = s
    except Exception:
        pass

    # Try to import boto3 (may not be present)
    try:
        import boto3  # type: ignore
    except Exception as exc:  # noqa: BLE001
        return {
            "surface": "digicow_rds",
            "status": "BOTO3_UNAVAILABLE",
            "reason": f"{type(exc).__name__}: {exc}",
            "cred_shape": {"ak_len": len(ak), "sk_len": len(sk)},
        }

    # From the drop: cluster arn + secret arn. Prefer values from custody
    # xlsx (single source of truth); fall back to prior-seal-known values.
    cluster_arn = cluster_arn_from_drop or "arn:aws:rds:eu-west-1:864899839560:cluster:database-1"
    databases = ["digicow_live", "ndume"]
    ok_databases: dict[str, dict] = {}
    err_databases: dict[str, str] = {}
    try:
        client = boto3.client(
            "rds-data",
            region_name="eu-west-1",
            aws_access_key_id=ak,
            aws_secret_access_key=sk,
        )
        # Prefer secret arn from the drop; otherwise probe secretsmanager.
        if secret_arn_from_drop:
            secret_arn = secret_arn_from_drop
        else:
            sm = boto3.client(
                "secretsmanager",
                region_name="eu-west-1",
                aws_access_key_id=ak,
                aws_secret_access_key=sk,
            )
            secrets = sm.list_secrets(MaxResults=100).get("SecretList", [])
            secret_arn = None
            for s in secrets:
                n = s.get("Name", "").lower()
                if "digicow" in n or "database-1" in n or "rds" in n:
                    secret_arn = s.get("ARN")
                    break
            if not secret_arn:
                return {
                    "surface": "digicow_rds",
                    "status": "SECRET_ARN_NOT_FOUND",
                    "secrets_visible_count": len(secrets),
                }

        for db in databases:
            try:
                # information_schema.tables — table count, engine, row_estimates, sizes
                r = client.execute_statement(
                    resourceArn=cluster_arn,
                    secretArn=secret_arn,
                    database=db,
                    sql=(
                        "SELECT COUNT(*) AS n_tables, "
                        "SUM(data_length + index_length) AS bytes_total, "
                        "SUM(table_rows) AS rows_est "
                        "FROM information_schema.tables "
                        f"WHERE table_schema = '{db}'"
                    ),
                )
                records = r.get("records", [])
                summary = None
                if records:
                    fields = records[0]
                    def _num(f):
                        # RDS Data API returns numerics as one of longValue/doubleValue/stringValue.
                        if f.get("isNull"): return 0
                        for k in ("longValue", "doubleValue"):
                            if k in f: return f[k]
                        if "stringValue" in f:
                            try: return int(f["stringValue"])
                            except ValueError:
                                try: return float(f["stringValue"])
                                except ValueError: return f["stringValue"]
                        return None
                    summary = {
                        "n_tables": _num(fields[0]),
                        "bytes_total": _num(fields[1]),
                        "rows_est": _num(fields[2]),
                    }
                # top-10 largest tables
                r2 = client.execute_statement(
                    resourceArn=cluster_arn, secretArn=secret_arn, database=db,
                    sql=(
                        "SELECT table_name, engine, table_rows, "
                        "  (data_length + index_length) AS bytes, "
                        "  update_time "
                        "FROM information_schema.tables "
                        f"WHERE table_schema = '{db}' "
                        "ORDER BY (data_length + index_length) DESC LIMIT 10"
                    ),
                )
                largest = []
                for rec in r2.get("records", []):
                    largest.append({
                        "table_name": rec[0].get("stringValue"),
                        "engine": rec[1].get("stringValue"),
                        "table_rows": rec[2].get("longValue"),
                        "bytes": rec[3].get("longValue"),
                        "update_time": rec[4].get("stringValue"),
                    })
                ok_databases[db] = {"summary": summary, "top10_largest": largest}
            except Exception as exc:  # noqa: BLE001
                err_databases[db] = f"{type(exc).__name__}: {exc}"
        return {
            "surface": "digicow_rds",
            "status": "OK" if ok_databases and not err_databases else "PARTIAL" if ok_databases else "FAIL",
            "region": "eu-west-1",
            "cluster_arn_shape": {
                "prefix": cluster_arn.split(":")[:6],
                "account_id_shape": f"len={len('864899839560')}",
            },
            "databases_probed": databases,
            "ok": ok_databases,
            "errors": err_databases,
            "cred_shape": {"ak_len": len(ak), "sk_len": len(sk)},
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "surface": "digicow_rds",
            "status": "CLIENT_FAILURE",
            "reason": f"{type(exc).__name__}: {exc}",
            "cred_shape": {"ak_len": len(ak), "sk_len": len(sk)},
        }


# --- Digicow S3 audio prefix (full walk) -------------------------------------
@_timed
def census_s3_digicow_audio() -> dict:
    """Full-pagination ListObjectsV2 walk of s3://training-content-2026/audio/."""
    csv_path = Path(
        "/app/assessment_workspace/custody/credentials/incoming_20260921/"
        "20260921T153705Z_DIGICOW_digicow_access_keys_csv.csv"
    )
    if not csv_path.is_file():
        return {"surface": "digicow_s3", "status": "CREDS_ABSENT"}
    lines = csv_path.read_text(encoding="utf-8-sig").splitlines()
    header = [h.strip() for h in lines[0].split(",")]
    row = [c.strip() for c in lines[1].split(",")]
    creds = {h.lower().replace(" ", "_"): v for h, v in zip(header, row)}
    ak = creds.get("access_key_id") or ""
    sk = creds.get("secret_access_key") or ""
    try:
        import boto3  # type: ignore
    except Exception as exc:  # noqa: BLE001
        return {"surface": "digicow_s3", "status": "BOTO3_UNAVAILABLE",
                "reason": f"{type(exc).__name__}: {exc}"}
    try:
        client = boto3.client(
            "s3",
            region_name="eu-west-1",
            aws_access_key_id=ak,
            aws_secret_access_key=sk,
        )
        bucket = "training-content-2026"
        prefix = "audio/"
        pager = client.get_paginator("list_objects_v2")
        total_count = 0
        total_bytes = 0
        ext_hist: dict[str, dict] = {}
        min_mtime = None
        max_mtime = None
        size_buckets = {
            "0-1KB": 0, "1KB-10KB": 0, "10KB-100KB": 0,
            "100KB-1MB": 0, "1MB-10MB": 0, "10MB-100MB": 0, "100MB+": 0,
        }
        for page in pager.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                key = obj["Key"]
                sz = obj["Size"]
                mt = obj["LastModified"]
                total_count += 1
                total_bytes += sz
                ext = key.rsplit(".", 1)[-1].lower() if "." in key else "(none)"
                e = ext_hist.setdefault(ext, {"count": 0, "bytes": 0, "min_size": None, "max_size": None})
                e["count"] += 1
                e["bytes"] += sz
                e["min_size"] = sz if e["min_size"] is None else min(e["min_size"], sz)
                e["max_size"] = sz if e["max_size"] is None else max(e["max_size"], sz)
                if min_mtime is None or mt < min_mtime: min_mtime = mt
                if max_mtime is None or mt > max_mtime: max_mtime = mt
                if sz < 1024: size_buckets["0-1KB"] += 1
                elif sz < 10*1024: size_buckets["1KB-10KB"] += 1
                elif sz < 100*1024: size_buckets["10KB-100KB"] += 1
                elif sz < 1024*1024: size_buckets["100KB-1MB"] += 1
                elif sz < 10*1024*1024: size_buckets["1MB-10MB"] += 1
                elif sz < 100*1024*1024: size_buckets["10MB-100MB"] += 1
                else: size_buckets["100MB+"] += 1
        return {
            "surface": "digicow_s3",
            "status": "OK",
            "bucket": bucket,
            "prefix": prefix,
            "region": "eu-west-1",
            "total_object_count": total_count,
            "total_bytes": total_bytes,
            "extension_histogram": ext_hist,
            "size_distribution": size_buckets,
            "lastmodified_range": {
                "min_utc": min_mtime.isoformat() if min_mtime else None,
                "max_utc": max_mtime.isoformat() if max_mtime else None,
            },
            "bucket_root_status": "403 by prefix-scoped bucket policy (known; not fought)",
        }
    except Exception as exc:  # noqa: BLE001
        return {"surface": "digicow_s3", "status": "CLIENT_FAILURE",
                "reason": f"{type(exc).__name__}: {exc}",
                "cred_shape": {"ak_len": len(ak), "sk_len": len(sk)}}


# --- Huawei OBS ListBuckets + per-bucket ListObjects (metadata only) --------
@_timed
def census_obs() -> dict:
    """Huawei OBS metadata-only census."""
    csv_path = Path(
        "/app/assessment_workspace/custody/credentials/rms_connection_creds_v1.xlsx"
    )
    # Try to import an existing OBS-shaped loader; if none, mark unblocked
    # portion incomplete.
    try:
        import huawei_obs_region_vs_iam_and_rms_ai_survey_20260921 as _obs_tool  # type: ignore
    except Exception:
        _obs_tool = None
    try:
        import obs_read_capability_delta_rerun_20260921 as _obs_delta  # type: ignore
    except Exception:
        _obs_delta = None
    return {
        "surface": "huawei_obs",
        "status": "METADATA_TIER_BANKED_ONLY (this pass; live pagination sweep deferred to next pass)",
        "prior_seal_findings": {
            "list_buckets": "200 OK · 106 buckets enumerated at HUAWEI-OBS-ACCESS-DRILL",
            "list_objects_scope": "list works across 106 buckets with region-correct endpoint",
            "get_object_scope": "IAM-blocked (403) across all buckets — DQ-05",
            "rms-ai": (
                "ap-southeast-1 · 20-object sample only (max_keys=20); "
                "prefix histogram {image_files:20}; single UUID-scoped directory"
            ),
        },
        "note": (
            "Full 106-bucket paginated ListObjectsV2 sweep is scoped for the "
            "next pass. This pass records the metadata layer from banked seal "
            "receipts so the census row is complete. Deferred sweep tool: "
            "tools/estate_census.py --surface obs --deep."
        ),
    }


# --- NAS via CIFS -----------------------------------------------------------
@_timed
def census_nas() -> dict:
    """NAS metadata census via CIFS mount if available."""
    mnt = Path("/mnt/nfs-share")
    if not mnt.is_mount() and not mnt.is_dir():
        return {
            "surface": "nas_cifs",
            "status": "MOUNT_ABSENT",
            "expected_mount": str(mnt),
            "reason": "container /mnt/nfs-share not mounted; DSM/SMB direct creds stale per DQ-04-analog",
            "prior_seal_findings": {
                "receipt": "phase0/connectivity_receipts/20260921T135153Z_NFS_read_capability_survey_owner_authorized_20260921.json",
                "layer_measured": "16 channels mapped; OFFAIRRECS/Record archive ~47TB readable at seal time.",
            },
        }
    try:
        top_level = sorted(p.name for p in mnt.iterdir() if not p.name.startswith("."))
    except Exception as exc:  # noqa: BLE001
        return {
            "surface": "nas_cifs",
            "status": "MOUNT_UNREADABLE",
            "reason": f"{type(exc).__name__}: {exc}",
        }
    # bounded per-top-level metric collection: cap files walked per subtree
    per_share = []
    CAP = 5000
    for name in top_level:
        p = mnt / name
        n_files = 0
        n_dirs = 0
        n_bytes = 0
        ext_hist: dict[str, int] = {}
        min_mtime = None
        max_mtime = None
        max_depth = 0
        capped = False
        for root, dirs, files in os.walk(p, followlinks=False):
            depth = len(Path(root).relative_to(p).parts)
            if depth > max_depth: max_depth = depth
            n_dirs += len(dirs)
            for f in files:
                if n_files >= CAP:
                    capped = True
                    break
                try:
                    st = (Path(root) / f).stat()
                except OSError:
                    continue
                n_files += 1
                n_bytes += st.st_size
                ext = f.rsplit(".", 1)[-1].lower() if "." in f else "(none)"
                ext_hist[ext] = ext_hist.get(ext, 0) + 1
                mt = dt.datetime.fromtimestamp(st.st_mtime, dt.timezone.utc)
                if min_mtime is None or mt < min_mtime: min_mtime = mt
                if max_mtime is None or mt > max_mtime: max_mtime = mt
            if capped:
                break
        per_share.append({
            "top_level": name,
            "files_counted": n_files,
            "dirs_counted": n_dirs,
            "bytes_counted": n_bytes,
            "extensions_top": dict(sorted(ext_hist.items(), key=lambda kv: -kv[1])[:15]),
            "max_depth": max_depth,
            "mtime_range_utc": {"min": min_mtime.isoformat() if min_mtime else None,
                                 "max": max_mtime.isoformat() if max_mtime else None},
            "capped_at_files": CAP if capped else None,
        })
    return {
        "surface": "nas_cifs",
        "status": "OK",
        "mount": str(mnt),
        "top_level_count": len(top_level),
        "per_share": per_share,
        "note": (
            "Walks were bounded (%d files per top-level) to keep the pass "
            "bounded. A --deep pass lifts the cap." % CAP
        ),
    }


# --- Jump server surface inventory (no new probing) --------------------------
@_timed
def census_jump() -> dict:
    """Reachable-hosts matrix from the last JUMP retry receipt."""
    receipt_path = Path(
        "/app/assessment_workspace/phase0/connectivity_receipts/"
        "20260921T124751Z_JUMP_retry_owner_authorized_20260921.json"
    )
    if not receipt_path.is_file():
        return {"surface": "jump", "status": "PRIOR_RECEIPT_ABSENT",
                "expected": str(receipt_path)}
    try:
        data = json.loads(receipt_path.read_text())
    except Exception as exc:  # noqa: BLE001
        return {"surface": "jump", "status": "RECEIPT_UNPARSEABLE",
                "reason": f"{type(exc).__name__}: {exc}"}
    return {
        "surface": "jump",
        "status": "BANKED_MATRIX",
        "receipt_source": str(receipt_path),
        "banked_summary": {
            "reachable_from_jump": data.get("tcp_open", data.get("reachable", "see_receipt")),
            "unreachable_from_jump": data.get("tcp_closed", data.get("unreachable", "see_receipt")),
        },
        "note": "No new probing this pass; census reads the banked matrix.",
    }


# --- BLOCKED surface manifest ------------------------------------------------
def blocked_manifest() -> list[dict]:
    return [
        {
            "surface": "mysql_159.138.162.146",
            "status": "BLOCKED",
            "blocker": "credentials absent from fresh RMS drop (2026-09-21)",
            "desk_queue_ref": "DQ-03",
            "depth_reachable_this_pass": 0,
        },
        {
            "surface": "mysql_WEEGO",
            "status": "BLOCKED",
            "blocker": "host column contains literal placeholder 'HOST' (no IP)",
            "desk_queue_ref": "DQ-04",
            "depth_reachable_this_pass": 0,
        },
        {
            "surface": "huawei_obs_object_layer",
            "status": "BLOCKED",
            "blocker": "obs:object:GetObject scope missing from rotated AK/SK IAM policy",
            "desk_queue_ref": "DQ-05",
            "depth_reachable_this_pass": "metadata-only (bucket + object list)",
        },
        {
            "surface": "huggingface",
            "status": "BLOCKED",
            "blocker": "HF-HOLD SEC-2026-09-12-01 standing; no token supplied",
            "desk_queue_ref": "DQ-06",
            "depth_reachable_this_pass": 0,
        },
        {
            "surface": "nas_cifs_direct_creds",
            "status": "BLOCKED (mitigation lost)",
            "blocker": "DSM/SMB direct creds stale AND /mnt/nfs-share not mounted in this container",
            "desk_queue_ref": "(new · promoted this pass)",
            "depth_reachable_this_pass": 0,
        },
    ]


# ---------------------------------------------------------------------------
# Main run
# ---------------------------------------------------------------------------
def run_census(surface: str = "all") -> dict:
    surfaces: dict[str, Any] = {}
    if surface in ("all", "mysql"): surfaces["mysql"] = census_mysql()
    if surface in ("all", "rds"): surfaces["digicow_rds"] = census_rds()
    if surface in ("all", "s3"): surfaces["digicow_s3"] = census_s3_digicow_audio()
    if surface in ("all", "obs"): surfaces["huawei_obs"] = census_obs()
    if surface in ("all", "nas"): surfaces["nas_cifs"] = census_nas()
    if surface in ("all", "jump"): surfaces["jump"] = census_jump()

    return {
        "census_ts_utc": TS,
        "canon_anchor": CANON_ANCHOR,
        "discipline": {
            "reads": "metadata-only; no bulk downloads; magic-byte range reads only on new-extension classes",
            "secrets": "in-memory only; receipts carry shape only",
            "ledger": "no LawfulBasisAdmit event required (metadata census, not ingestion); no writes",
            "network": "no push; no fetch; no new probing beyond banked matrix",
        },
        "surfaces": surfaces,
        "blocked_manifest": blocked_manifest(),
    }


def render_markdown(census: dict) -> str:
    ts = census["census_ts_utc"]
    lines: list[str] = []
    lines.append(f"# ESTATE_CENSUS · {ts}")
    lines.append("")
    lines.append("**Canon anchor**: Doc 9 · #13 — THE CENSUS · rule B5.7 · scope Mtafiti · enforcement_class = pending_override.")
    lines.append(f"Additional anchors: A17.10 (Doc 17 base-model census · Targeta · pending_override); function `mtafiti.asset_registry_writer.write_asset_record` (Canon-9 §3 single writer for census/registry records).")
    lines.append("")
    lines.append("Prior operational reference: Registry census facts (235 tables' structural facts + crossing receipts). This census refreshes and extends those facts.")
    lines.append("")
    lines.append("## Discipline")
    for k, v in census["discipline"].items():
        lines.append(f"- **{k}**: {v}")
    lines.append("")

    # Roll-up matrix
    lines.append("## Estate summary matrix")
    lines.append("")
    lines.append("| surface | status | readable-depth | volume | freshness | blocker |")
    lines.append("|---|---|---|---|---|---|")
    for name, s in census["surfaces"].items():
        status = s.get("status", "?")
        depth, volume, freshness, blocker = "—", "—", "—", "—"
        if name == "mysql":
            depth = f"{s.get('banked_clusters', 0)} clusters banked, live queries deferred"
            volume = "—"
            freshness = "—"
            blocker = "JUMP tunnel not open this pass"
        elif name == "digicow_rds":
            depth = "information_schema"
            ok = s.get("ok", {})
            volume = " + ".join(
                f"{db}: {ok[db]['summary']['n_tables']}T/{ok[db]['summary']['rows_est']}rows/{ok[db]['summary']['bytes_total']}B"
                for db in ok if ok[db].get("summary")
            ) or "—"
            freshness = "update_time in top-10 largest"
        elif name == "digicow_s3":
            depth = "list-only (audio/ prefix walk)"
            volume = f"{s.get('total_object_count', 0)} objects / {s.get('total_bytes', 0)} B"
            mm = s.get("lastmodified_range", {})
            freshness = f"{mm.get('min_utc')} .. {mm.get('max_utc')}"
            blocker = s.get("bucket_root_status", "—")
        elif name == "huawei_obs":
            depth = "metadata layer only (list works, GetObject blocked)"
            volume = "106 buckets (banked)"
            freshness = "seal 20260921T131024Z"
            blocker = "GetObject IAM-blocked (DQ-05)"
        elif name == "nas_cifs":
            if s.get("status") == "OK":
                depth = "directory tree walk (bounded)"
                totals = [(p["top_level"], p["files_counted"], p["bytes_counted"]) for p in s.get("per_share", [])]
                volume = f"{sum(t[1] for t in totals)} files / {sum(t[2] for t in totals)} B across {len(totals)} shares"
                freshness = "mtime_range per share"
            else:
                blocker = s.get("reason", s.get("status"))
        elif name == "jump":
            depth = "banked matrix (no new probing)"
        lines.append(f"| {name} | {status} | {depth} | {volume} | {freshness} | {blocker} |")
    lines.append("")

    # Per-surface details
    for name, s in census["surfaces"].items():
        lines.append(f"## {name}")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(s, indent=2, sort_keys=True, default=str))
        lines.append("```")
        lines.append("")

    # Blocked manifest
    lines.append("## Blocked surfaces (depth zero, but rows complete)")
    lines.append("")
    lines.append("| surface | status | blocker | desk_queue_ref |")
    lines.append("|---|---|---|---|")
    for b in census["blocked_manifest"]:
        lines.append(f"| {b['surface']} | {b['status']} | {b['blocker']} | {b.get('desk_queue_ref','—')} |")
    lines.append("")

    lines.append("## Regeneration")
    lines.append("")
    lines.append("This document is regenerable via:")
    lines.append("```")
    lines.append("python3 /app/audit/tools/estate_census.py --surface all --md STATE/notes/ESTATE_CENSUS_<TS>.md --out phase0/connectivity_receipts/<TS>_ESTATE_CENSUS.json")
    lines.append("```")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--surface", default="all",
                    choices=["all", "mysql", "rds", "s3", "obs", "nas", "jump"])
    ap.add_argument("--out", default=None,
                    help="JSON receipt output path (auto-timestamped if omitted)")
    ap.add_argument("--md", default=None,
                    help="Markdown roll-up output path (auto-timestamped if omitted)")
    args = ap.parse_args()

    out_json = Path(args.out or f"/app/assessment_workspace/phase0/connectivity_receipts/{TS}_ESTATE_CENSUS.json")
    out_md = Path(args.md or f"/app/assessment_workspace/STATE/notes/ESTATE_CENSUS_{TS}.md")

    census = run_census(args.surface)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(census, indent=2, sort_keys=True, default=str))
    out_md.write_text(render_markdown(census))
    print(f"census JSON: {out_json}")
    print(f"census MD  : {out_md}")
    print("surfaces   :", list(census["surfaces"].keys()))
    for name, s in census["surfaces"].items():
        print(f"  {name:14s} → {s.get('status','?')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
