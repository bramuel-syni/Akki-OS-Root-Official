"""Read-only tenant projection of existing census manifests. No sibling registry."""
import hashlib
import json
import re
from pathlib import Path

from services.tenant_separation.tenant_registry import CANONICAL_TENANT_IDS


def _owner(doc, number):
    # Legacy assignment is owner-recorded in tenant_registry §3. Census 4 declares RMS scope.
    if "tenant_id" in doc:
        return doc["tenant_id"] if doc["tenant_id"] in CANONICAL_TENANT_IDS else None
    if number in (1, 2):
        return "DIGICOW"
    if number == 4 and doc.get("estate_scope", "").startswith("RMS MySQL estate"):
        return "RMS"
    return None  # Neither mixed-tenant nor unidentified records acquire a guessed owner.


def _count(rollup, key):
    value = rollup.get(key)
    return value if type(value) is int and value >= 0 else None


def list_records(root: Path, tenant: str):
    if tenant not in CANONICAL_TENANT_IDS:
        raise ValueError("Unadmitted tenant")
    rows = []
    for path in root.glob("census_*/manifest.json"):
        if not re.fullmatch(r"census_\d{4,}", path.parent.name) or path.is_symlink():
            continue
        try:
            raw = path.read_bytes()
            doc = json.loads(raw)
            number = int(path.parent.name.split("_")[1])
            if _owner(doc, number) != tenant:
                continue
            totals = doc.get("rollup", {})
            rows.append({
                "census_number": number, "census_id": number, "tenant_id": tenant,
                "record_id": f"census-{number}", "status": "RECORDED",
                "scope": "Metadata inventory" if "total_row_count_est" in totals else "Recorded census",
                "started_at": doc.get("started_at_utc"), "finished_at": doc.get("finished_at_utc"),
                "database_count": _count(totals, "database_count"), "table_count": _count(totals, "table_count"),
                "row_count_estimate": _count(totals, "total_row_count_est"),
                "row_count_measured": _count(totals, "total_row_count"),
                "volume_bytes": None, "quality_percent": None, "licensed_percent": None,
                "proof_ref": f"census/{path.parent.name}/manifest.json",
                "proof_sha256": hashlib.sha256(raw).hexdigest(),
                "execution_verified": False,
                "limitations": ["Historical record; not a fresh source verification.",
                                "Volume, quality, personal-data share and external-release rights are not measured here."]
                    + (["Row totals are database metadata estimates, not counted source rows.",
                        "This historical pass used a pod connection; it is not proof of current execution-boundary compliance."]
                       if number == 4 else []),
            })
        except (OSError, ValueError, TypeError, AttributeError):
            continue
    return sorted(rows, key=lambda x: x["census_number"], reverse=True)