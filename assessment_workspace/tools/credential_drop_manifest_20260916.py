"""§E-compliant credential-drop manifest builder · 2026-09-16T~19:10Z.

Discipline (SO §4.1 §E):
- Reads ONLY file-level metadata (byte-length, sha256 of raw bytes, mtime,
  mode, line-count-for-text). NEVER reads cell values, CSV columns, or
  workbook sheets.
- Never uses csv.reader, openpyxl.load_workbook, or any parser that touches
  field values.
- Never prints raw file contents to stdout; only shape/hash metadata.
- Uses hashlib on raw bytes (file-level content-address); no cell parsing.

Output: JSON drop manifest at phase0/credential_drop_manifests/
20260916T1910Z_drop_manifest.json.

Bind-delta reconciliation is against notes/ADMIN_BINDS_20260915.md's
§A sha256 pin for `admin_bind_20260915_bramuel_cd_visitors.json`. Other
files have no prior sha pin recorded in the durable ledger; they land as
NEW-ENTRY rows, not rotation.
"""
from __future__ import annotations

import hashlib
import json
import os
import stat as stat_mod
from datetime import datetime, timezone
from pathlib import Path

CUSTODY_DIR = Path("/app/backend/estate_keys/data_sources")
MANIFEST_OUT = Path(
    "/app/assessment_workspace/phase0/credential_drop_manifests/"
    "20260916T1910Z_drop_manifest.json"
)

# Prior sha256 pins recorded in the durable ledger
# (notes/ADMIN_BINDS_20260915.md §A). Any file NOT in this map lands as
# NEW-ENTRY (no rotation reconciliation possible without a prior pin).
PRIOR_PINS = {
    "admin_bind_20260915_bramuel_cd_visitors.json": (
        "a7a616be4577319d10387f15e2e6302e508f1cddc035d017dda8bd7d8717f70d"
    ),
}


def _sha256_file(path: Path) -> str:
    """Content-address a file at raw-byte level. No cell parsing. No prints."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _line_count(path: Path) -> int:
    """Count newlines in a text file. No content emitted; only the count."""
    n = 0
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(65536)
            if not chunk:
                break
            n += chunk.count(b"\n")
    return n


def _classify(name: str) -> str:
    lower = name.lower()
    if lower.endswith(".xlsx"):
        return "xlsx_binary_zip"
    if lower.endswith(".json"):
        return "json_text"
    if lower.endswith(".csv"):
        return "csv_text"
    return "unknown"


def _delta(name: str, current_sha: str) -> dict:
    prior = PRIOR_PINS.get(name)
    if prior is None:
        return {"class": "NEW-ENTRY", "prior_sha256": None, "rotated": False}
    if prior == current_sha:
        return {"class": "UNCHANGED", "prior_sha256": prior, "rotated": False}
    return {"class": "ROTATED", "prior_sha256": prior, "rotated": True}


def build_manifest() -> dict:
    if not CUSTODY_DIR.is_dir():
        raise SystemExit(f"custody dir missing: {CUSTODY_DIR}")

    rows = []
    for entry in sorted(CUSTODY_DIR.iterdir()):
        if not entry.is_file():
            continue
        st = entry.stat()
        # Only compute line-count for text kinds; binary xlsx/json get None
        # (avoids implying a false "record count" on a zip archive).
        kind = _classify(entry.name)
        line_count = _line_count(entry) if kind == "csv_text" else None
        sha = _sha256_file(entry)
        rows.append({
            "name": entry.name,
            "kind": kind,
            "size_bytes": st.st_size,
            "sha256": sha,
            "mtime_iso": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat(),
            "mode_octal": oct(stat_mod.S_IMODE(st.st_mode)),
            "line_count": line_count,
            "bind_delta": _delta(entry.name, sha),
        })

    return {
        "at_utc": datetime.now(timezone.utc).isoformat(),
        "custody_dir": str(CUSTODY_DIR),
        "row_count": len(rows),
        "discipline": (
            "SO §4.1 §E · file-level metadata only · no csv.reader · no "
            "openpyxl · no print of raw values · sha256sum/stat/wc-class "
            "primitives via hashlib+os.stat"
        ),
        "prior_pin_source": "notes/ADMIN_BINDS_20260915.md §A",
        "rows": rows,
    }


def main() -> int:
    MANIFEST_OUT.parent.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest()
    with open(MANIFEST_OUT, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=False)
    # Emit ONLY a shape-level summary; no raw values.
    n = manifest["row_count"]
    rotated = sum(1 for r in manifest["rows"] if r["bind_delta"]["rotated"])
    new_entry = sum(1 for r in manifest["rows"] if r["bind_delta"]["class"] == "NEW-ENTRY")
    unchanged = sum(1 for r in manifest["rows"] if r["bind_delta"]["class"] == "UNCHANGED")
    print(f"MANIFEST_OUT={MANIFEST_OUT}")
    print(f"rows={n} unchanged={unchanged} rotated={rotated} new_entry={new_entry}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
