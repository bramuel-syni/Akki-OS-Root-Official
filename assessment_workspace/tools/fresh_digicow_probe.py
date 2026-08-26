"""One-shot fresh DigiCow verification probe (W11 CP2+CP3 interleave).

Owner directive 2026-08-26: 'run a FRESH DigiCow verification probe yourself
now via the existing owner-signed connection · the owner's rights approval +
connection signature from 2026-08-19 cover it; log the crossing receipt
through the chokepoint as usual.'

Reads stored credentials from ESTATE_KEYS_DIR/data_sources/aws_iam_user_*.json
(mode-0600, git-ignored, never in stdout), combines with the DigiCow resource
fields from the most recent data_connection_record, fires
services.connect.rds_data_submit.submit(), which:
  * Fires the declaration seat.
  * Registers the crossing at the chokepoint (residency-checked).
  * Runs SELECT 1 · engine probe · light inventory · writes a fresh record.

CREDENTIAL DISCIPLINE (Owner Order · this session):
  * aws_access_key_id and aws_secret_access_key are read into locals ONLY.
  * They are passed to submit() and never printed, logged, or committed.
  * The result dict has creds_path stripped before print.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


SPINE = Path("/app/assessment_workspace/repos/Extraction-Akki/backend")
if str(SPINE) not in sys.path:
    sys.path.insert(0, str(SPINE))


def _load_owner_signed_credentials() -> dict:
    """Read the stored AWS IAM user JSON. Never prints its contents."""
    creds_dir = Path("/app/backend/estate_keys/data_sources")
    # Owner-signed IAM user file — the one with aws_iam_user_ prefix that has
    # aws_access_key_id + aws_secret_access_key + STS-verified identity.
    candidates = sorted(creds_dir.glob("aws_iam_user_*.json"))
    if not candidates:
        raise SystemExit("no aws_iam_user_*.json found in estate_keys/data_sources/")
    body = json.loads(candidates[-1].read_text())
    if "aws_access_key_id" not in body or "aws_secret_access_key" not in body:
        raise SystemExit("stored credentials missing required fields")
    return body


def _load_latest_digicow_resource() -> dict:
    """Read the freshest existing data_connection_record for DigiCow to
    reuse the region + cluster_arn + secret_arn + database fields."""
    recs_dir = Path("/app/assessment_workspace/phase0/data_connection_records")
    best = None
    best_at = ""
    for p in recs_dir.glob("*.json"):
        try:
            r = json.loads(p.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if r.get("kind") != "data_connection_record":
            continue
        if r.get("source_id") != "aws.rds.db-restore-603-cluster.digicow_live":
            continue
        at = r.get("at", "")
        if at > best_at:
            best_at = at
            best = r
    if best is None:
        raise SystemExit("no prior DigiCow record found; owner signature needed")
    return best["resource"]


def main() -> int:
    creds = _load_owner_signed_credentials()
    resource = _load_latest_digicow_resource()
    # Compose the payload for submit() · aws_* fields never leave this scope.
    payload = {
        "aws_access_key_id":     creds["aws_access_key_id"],
        "aws_secret_access_key": creds["aws_secret_access_key"],
        "region":                resource["region"],
        "cluster_arn":           resource["cluster_arn"],
        "secret_arn":            resource["secret_arn"],
        "database":              resource.get("database"),
    }
    print(f"[probe] source_id=aws.rds.db-restore-603-cluster.digicow_live "
          f"region={payload['region']} database={payload['database']}", flush=True)

    from services.connect.rds_data_submit import submit
    result = submit(payload, actor="owner")

    # STRIP creds_path from the result print (per credential discipline).
    result_public = {k: v for k, v in result.items() if k != "creds_path"}
    # Redact any inventory row bodies further — we only print counts.
    inv = result_public.get("found") or {}
    if isinstance(inv, dict):
        result_public["found_summary"] = {
            "schemas_count": len(inv.get("schemas", [])),
            "tables_count": len(inv.get("tables", [])),
            "inventory_cap": inv.get("inventory_cap"),
        }
        result_public.pop("found", None)
    print(json.dumps(result_public, indent=2, sort_keys=True), flush=True)

    # Exit non-zero on failure so shell captures it.
    return 0 if result.get("link_working") else 1


if __name__ == "__main__":
    sys.exit(main())
