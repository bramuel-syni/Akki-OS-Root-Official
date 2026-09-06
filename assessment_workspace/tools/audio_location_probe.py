"""Owner-authorized audio-location probe (BYPASS LINEAGE · one-off).

AUTHORITY (banked verbatim in this session):
    "the owner asserts audio access SHOULD exist. His assertion + this
     instruction constitute authorization for a NARROW governed probe
     beyond aggregates, scoped strictly to locating audio."

SCOPE (strict · refused if exceeded):
  * ONLY these column shapes are read (never any other column):
      - name matches ('audio','voice','recording','sound','clip','file',
                       'media','url','path','attachment')
      - excludes PII/aggregate columns entirely
  * Sample size: hard cap 30 rows per column (owner authorized 20-50)
  * WHERE filter: column IS NOT NULL AND column <> ''
  * Receipts are SHAPE-ONLY:
      - filename-extension histogram
      - URL scheme + hostname/bucket + first path-segment pattern
      - NEVER the raw URL (URLs can carry tokens)
      - NEVER any other column value
  * Bypass class: `owner_authorized_audio_location_probe`
  * Every SQL statement audited with (sql_shape, table, column, principal, at_utc)
  * NO PII columns touched
  * NO content downloads (HEAD/metadata only if URLs point at reachable storage)

USAGE:
  python3 tools/audio_location_probe.py --dry-run   # print plan only
  python3 tools/audio_location_probe.py             # execute + bank receipts

RECEIPT OUTPUT:
  phase0/audio_location_probe/<utc_stamp>/
    plan.json                     · the exact set of column reads planned
    audit_trail.json              · every SQL statement, shape-only
    per_column_shape_summary.json · extension histogram + URL scheme + host
                                     pattern per column
    combined_verdict.md           · owner-readable summary
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

# --- Guard rails --------------------------------------------------
ALLOWED_COLUMN_PATTERNS = {
    "audio", "voice", "recording", "sound", "clip",
    "file", "media", "url", "path", "attachment",
}
IGNORE_COLUMN_TOKENS = {
    "is_invoice", "service", "device_id", "profile",
}
# Columns known from Census #1/#2 to be PII-like — never read.
PII_COLUMNS_BANNED = {
    "email", "phone", "password", "occupation",
    "national_id", "id_number", "ssn",
}
HARD_CAP_ROWS_PER_COLUMN = 30
BYPASS_CLASS = "owner_authorized_audio_location_probe"


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _find_media_columns(census_dir: Path):
    """Read the latest census artefacts on disk and return the media-shaped
    columns (dict list) that survive the guard rails."""
    hits = []
    for db_file in census_dir.glob("*.json"):
        if db_file.name == "manifest.json":
            continue
        data = json.loads(db_file.read_text())
        dbname = data.get("database") or db_file.stem
        for t in data.get("tables", []):
            tname = t.get("table")
            row_count = t.get("row_count", 0)
            for c in t.get("columns", []):
                cname = c.get("name", "")
                ctype = c.get("type", "")
                low = cname.lower()
                if low in IGNORE_COLUMN_TOKENS:
                    continue
                if low in PII_COLUMNS_BANNED:
                    continue
                if not any(pat in low for pat in ALLOWED_COLUMN_PATTERNS):
                    continue
                if row_count == 0:
                    continue
                # Skip datetimes (rc_image_upload_datetime etc.)
                if ctype.lower() in {"datetime", "date", "timestamp", "int",
                                     "bigint", "tinyint", "smallint"}:
                    continue
                hits.append({
                    "database": dbname,
                    "table": tname,
                    "column": cname,
                    "type": ctype,
                    "row_count_at_census": row_count,
                    "matched_pattern": next(
                        p for p in ALLOWED_COLUMN_PATTERNS if p in low
                    ),
                })
    return hits


def _shape_of_url(raw: str):
    """Return SHAPE ONLY of a URL string: (extension_lower, url_scheme,
    host_pattern, first_path_segment). Never return the raw URL."""
    if raw is None:
        return None
    s = str(raw).strip()
    if not s:
        return None
    # If it looks like a bare filename (no scheme, no path), still get ext.
    try:
        p = urlparse(s if "://" in s else f"file:///{s.lstrip('/')}")
        scheme = p.scheme or "none"
        host = (p.hostname or "").lower() if p.hostname else "(no-host)"
        # Domain pattern: keep TLD structure, strip subdomains beyond 2 levels
        host_parts = host.split(".") if host and host != "(no-host)" else []
        if len(host_parts) >= 2:
            host_pattern = ".".join(host_parts[-3:] if len(host_parts) >= 3 else host_parts)
        else:
            host_pattern = host or "(no-host)"
        path = p.path or ""
        # Extension from last path segment
        m = re.search(r"\.([A-Za-z0-9]{2,6})(?:[?#]|$)", path)
        ext = m.group(1).lower() if m else "(no-ext)"
        # First path segment (for S3 bucket / GCS bucket / route hint)
        segs = [x for x in path.split("/") if x]
        first_seg = segs[0] if segs else "(no-path)"
        # Anonymize the first-seg if it looks like a token (long hex/base64)
        if len(first_seg) > 20 and re.fullmatch(r"[A-Za-z0-9\-_+/=]+", first_seg):
            first_seg = f"<long-token-{len(first_seg)}ch>"
        return {
            "ext": ext,
            "scheme": scheme,
            "host_pattern": host_pattern,
            "first_path_seg_pattern": first_seg,
        }
    except Exception:  # pragma: no cover
        return {"ext": "(parse-err)", "scheme": "(parse-err)",
                "host_pattern": "(parse-err)", "first_path_seg_pattern": "(parse-err)"}


def _load_estate_creds():
    p = Path(os.environ.get("ESTATE_KEYS_DIR",
                            "/app/backend/estate_keys")) / "data_sources"
    preferred = p / "db-restore-603-cluster.json"
    fp = preferred if preferred.is_file() else sorted(p.glob("*.json"))[0]
    body = json.loads(fp.read_text())
    return {
        "cluster_arn": body["cluster_arn"],
        "secret_arn":  body["secret_arn"],
        "region":      body["region"],
        "aws_access_key_id":     body.get("aws_access_key_id", ""),
        "aws_secret_access_key": body.get("aws_secret_access_key", ""),
    }


def _boto_client(creds):
    import boto3
    os.environ["AWS_ACCESS_KEY_ID"] = creds["aws_access_key_id"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = creds["aws_secret_access_key"]
    return boto3.client("rds-data", region_name=creds["region"])


def probe_column(client, creds, database, table, column,
                 hard_cap=HARD_CAP_ROWS_PER_COLUMN, audit_trail=None):
    """Execute ONE governed SELECT that reads up to `hard_cap` non-empty
    values from `database.table.column`. Return shape-only summary."""
    if audit_trail is None:
        audit_trail = []
    # Ident guard (identifier tokens only)
    for ident in (database, table, column):
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", ident):
            raise ValueError(f"identifier refused: {ident!r}")
    sql = (
        f"SELECT `{column}` FROM `{table}` "
        f"WHERE `{column}` IS NOT NULL AND `{column}` <> '' "
        f"LIMIT {int(hard_cap)}"
    )
    audit_trail.append({
        "at_utc": _iso_now(),
        "sql_shape": f"{BYPASS_CLASS}:sample_column",
        "database": database, "table": table, "column": column,
        "principal": "owner", "hard_cap": int(hard_cap),
    })
    r = client.execute_statement(
        resourceArn=creds["cluster_arn"],
        secretArn=creds["secret_arn"],
        database=database,
        sql=sql,
    )
    n_read = 0
    exts = Counter()
    schemes = Counter()
    hosts = Counter()
    first_segs = Counter()
    empty_count = 0
    non_url_shape_count = 0
    for row in (r.get("records") or []):
        if not row:
            continue
        cell = row[0]
        # boto rds-data cell can be {'stringValue': ...} etc.
        value = None
        for k in ("stringValue", "blobValue"):
            if k in cell:
                value = cell[k]
                break
        if value is None:
            empty_count += 1
            continue
        n_read += 1
        sh = _shape_of_url(value if isinstance(value, str) else str(value))
        if sh is None:
            empty_count += 1
            continue
        # Distinguish URL-shape from bare filename
        if sh["scheme"] not in ("http", "https", "s3", "gs", "file"):
            non_url_shape_count += 1
        exts[sh["ext"]] += 1
        schemes[sh["scheme"]] += 1
        hosts[sh["host_pattern"]] += 1
        first_segs[sh["first_path_seg_pattern"]] += 1
    return {
        "database": database, "table": table, "column": column,
        "sampled_rows": n_read,
        "empty_rows_skipped": empty_count,
        "extension_histogram": dict(exts.most_common()),
        "scheme_histogram": dict(schemes.most_common()),
        "host_pattern_histogram": dict(hosts.most_common()),
        "first_path_seg_histogram": dict(first_segs.most_common()),
        "non_url_shape_count": non_url_shape_count,
    }


AUDIO_EXTENSIONS = {"mp3", "wav", "amr", "ogg", "opus", "m4a", "aac", "flac", "wma", "3gp"}
IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp", "bmp", "svg", "tif", "tiff", "heic", "heif"}
VIDEO_EXTENSIONS = {"mp4", "mov", "avi", "mkv", "webm", "wmv", "flv"}
DOC_EXTENSIONS   = {"pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "csv"}


def classify_verdict(per_col):
    """Given the per-column shape summary, decide what's inside the column."""
    verdicts = []
    for c in per_col:
        exts = c["extension_histogram"]
        if not exts:
            verdicts.append({"col": f"{c['database']}.{c['table']}.{c['column']}",
                             "verdict": "no_readable_values"})
            continue
        n = sum(exts.values())
        aud = sum(v for k, v in exts.items() if k in AUDIO_EXTENSIONS)
        img = sum(v for k, v in exts.items() if k in IMAGE_EXTENSIONS)
        vid = sum(v for k, v in exts.items() if k in VIDEO_EXTENSIONS)
        doc = sum(v for k, v in exts.items() if k in DOC_EXTENSIONS)
        if aud / n >= 0.5:
            verdict = f"AUDIO ({aud}/{n} audio-ext)"
        elif img / n >= 0.5:
            verdict = f"IMAGE ({img}/{n} image-ext)"
        elif vid / n >= 0.5:
            verdict = f"VIDEO ({vid}/{n} video-ext)"
        elif doc / n >= 0.5:
            verdict = f"DOC ({doc}/{n} doc-ext)"
        elif aud > 0:
            verdict = f"MIXED with-audio (aud={aud} img={img} vid={vid} doc={doc} of {n})"
        else:
            verdict = f"MIXED (aud={aud} img={img} vid={vid} doc={doc} of {n})"
        verdicts.append({
            "col": f"{c['database']}.{c['table']}.{c['column']}",
            "verdict": verdict,
            "row_count_at_census": c.get("row_count_at_census"),
            "top_ext": list(exts.items())[:5],
            "top_host": list(c["host_pattern_histogram"].items())[:3],
            "top_scheme": list(c["scheme_histogram"].items())[:3],
        })
    return verdicts


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Print plan only, no SQL executed")
    ap.add_argument("--census-dir",
                    default="/app/assessment_workspace/phase0/census/census_0002",
                    help="Directory of the census to read schema from (default: census #2)")
    args = ap.parse_args(argv)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_root = Path(f"/app/assessment_workspace/phase0/audio_location_probe/{stamp}")
    out_root.mkdir(parents=True, exist_ok=True)

    cols = _find_media_columns(Path(args.census_dir))
    # Attach row_count_at_census
    plan = {
        "authority": "owner-authorized bounded probe · audio-location scope only",
        "bypass_class": BYPASS_CLASS,
        "census_source": str(Path(args.census_dir).name),
        "at_utc": _iso_now(),
        "columns_targeted": cols,
        "hard_cap_rows_per_column": HARD_CAP_ROWS_PER_COLUMN,
        "guard_rails": {
            "allowed_column_patterns": sorted(ALLOWED_COLUMN_PATTERNS),
            "pii_columns_banned": sorted(PII_COLUMNS_BANNED),
            "receipts_shape_only": True,
            "content_downloads": False,
        },
    }
    (out_root / "plan.json").write_text(json.dumps(plan, indent=2))
    print(f"[plan] {len(cols)} media-shaped columns targeted:")
    for c in cols:
        print(f"  · {c['database']}.{c['table']}.{c['column']} · type={c['type']} · rows={c['row_count_at_census']:,}")
    if args.dry_run:
        print(f"\n[dry-run] plan saved to {out_root/'plan.json'}")
        return 0

    creds = _load_estate_creds()
    client = _boto_client(creds)

    audit_trail = []
    per_col = []
    for c in cols:
        try:
            summary = probe_column(client, creds, c["database"], c["table"],
                                   c["column"], audit_trail=audit_trail)
            summary["row_count_at_census"] = c["row_count_at_census"]
            per_col.append(summary)
            print(f"  · {c['database']}.{c['table']}.{c['column']}: "
                  f"sampled {summary['sampled_rows']} rows · "
                  f"ext top: {list(summary['extension_histogram'].items())[:3]}")
        except Exception as exc:
            per_col.append({
                "database": c["database"], "table": c["table"], "column": c["column"],
                "sampled_rows": 0, "error": repr(exc),
            })
            print(f"  · {c['database']}.{c['table']}.{c['column']}: ERROR {exc!r}")

    (out_root / "audit_trail.json").write_text(json.dumps(audit_trail, indent=2))
    (out_root / "per_column_shape_summary.json").write_text(json.dumps(per_col, indent=2))

    verdicts = classify_verdict(per_col)
    lines = [
        f"# Owner-authorized audio-location probe · {stamp}",
        "",
        f"**Authority:** owner interject 2026-09-06 verbatim: *\"there should be access to the audion files\"* · bounded probe scoped strictly to locating audio · shape-only receipts · no content downloads.",
        f"**Bypass class:** `{BYPASS_CLASS}`",
        f"**Census source:** `{Path(args.census_dir).name}` (Census #2)",
        f"**Columns probed:** {len(cols)}  ·  **Hard cap per column:** {HARD_CAP_ROWS_PER_COLUMN} rows",
        "",
        "## Per-column verdict (shape-only)",
        "",
        "| Column | Row count (Census #2) | Sampled | Verdict | Top ext | Top scheme | Top host pattern |",
        "|---|---:|---:|---|---|---|---|",
    ]
    for v, pc in zip(verdicts, per_col):
        exts = ", ".join(f"{k}:{n}" for k, n in list(pc.get('extension_histogram', {}).items())[:3])
        schemes = ", ".join(f"{k}:{n}" for k, n in list(pc.get('scheme_histogram', {}).items())[:2])
        hosts = ", ".join(f"{k}:{n}" for k, n in list(pc.get('host_pattern_histogram', {}).items())[:2])
        lines.append(f"| `{v['col']}` | {pc.get('row_count_at_census', 0):,} | {pc.get('sampled_rows', 0)} | **{v['verdict']}** | {exts} | {schemes} | {hosts} |")
    (out_root / "combined_verdict.md").write_text("\n".join(lines) + "\n")
    print(f"\n[receipts banked at] {out_root}")
    print("\n" + "\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
