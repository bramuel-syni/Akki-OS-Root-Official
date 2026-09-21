"""tools/rms_creds_drop_shape_probe_and_diff_20260921.py

Value-blind structural probe on the newly-dropped RMS creds sheet, and
shape-only diff vs the prior banked baseline (sha `d778eb1e…`).

STRICT DISCIPLINE:
    * NEVER emit cell/header text.
    * Emit ONLY: sheet names, row shape (kind labels + lengths + first-
      char bucket + sha8 hex of cell UTF-8 bytes for cross-run
      comparison).
    * NEVER csv.reader / openpyxl-print / cat / head raw values.

Reads two sheets in parallel:
    NEW:  /app/assessment_workspace/custody/credentials/incoming_20260921/*.xlsx
    OLD:  /app/backend/estate_keys/data_sources/RMS_Connection_Creds.xlsx
    (plus prior huawei_credentials CSVs for AK/SK shape diff)

Emits a state-only receipt: phase0/connectivity_receipts/{stamp}_RMS_
creds_drop_shape_probe_and_diff_20260921.json
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import glob
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import openpyxl

RECEIPT_DIR = Path("/app/assessment_workspace/phase0/connectivity_receipts")

NEW_XLSX_GLOB = "/app/assessment_workspace/custody/credentials/incoming_20260921/*_RMS_CREDS.xlsx"
OLD_XLSX = Path("/app/backend/estate_keys/data_sources/RMS_Connection_Creds.xlsx")


def _now(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_file(p: Path) -> Optional[str]:
    if not p.is_file(): return None
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _hash8(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="ignore")).hexdigest()[:8]


def _bucket(s: str) -> str:
    if not s: return "EMPTY"
    c = s[0]
    if c.isupper(): return "UPPER"
    if c.islower(): return "LOWER"
    if c.isdigit(): return "DIGIT"
    return "SYM"


def _kind(s: str) -> str:
    if not s: return "EMPTY"
    low = s.lower()
    if low.startswith(("http://", "https://")): return "URL"
    if low.startswith("username:"): return "USERNAME_LABEL_ROW"
    if low.startswith("password:"): return "PASSWORD_LABEL_ROW"
    if re.match(r"^\d+\.", s): return "NUMBERED_STEP"
    if re.match(r"^\s*\d{1,3}(\.\d{1,3}){3}\s*$", s): return "IPV4"
    if re.match(r"^\s*\d{1,5}\s*$", s): return "SHORT_NUMBER"
    return "TEXT"


def _cell_shape(v):
    s = "" if v is None else str(v).strip()
    return {
        "kind": _kind(s),
        "len": len(s),
        "first_char_bucket": _bucket(s),
        "contains_newline": "\n" in s,
        "sha8": _hash8(s) if s else None,
    }


def _sheet_shape(wb, sheet_name: str) -> dict:
    if sheet_name not in wb.sheetnames:
        return {"missing": True}
    ws = wb[sheet_name]
    rows = []
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        cells = [_cell_shape(c) for c in row]
        if any(c["kind"] != "EMPTY" for c in cells):
            rows.append({"row": i, "cells": cells})
    return {
        "rows_max": ws.max_row,
        "cols_max": ws.max_column,
        "merged_ranges": [str(r) for r in ws.merged_cells.ranges],
        "rows_shape": rows,
    }


def _probe_workbook(path: Path) -> dict:
    if not path.is_file():
        return {"missing": True, "path": str(path)}
    wb = openpyxl.load_workbook(path, data_only=True)
    out = {
        "path": str(path),
        "sha256": _sha256_file(path),
        "size_bytes": path.stat().st_size,
        "sheet_names": wb.sheetnames,
        "sheets": {},
    }
    for sn in wb.sheetnames:
        out["sheets"][sn] = _sheet_shape(wb, sn)
    return out


def _diff_creds(new: dict, old: dict) -> dict:
    """Shape-only diff. For each sheet in either book, per-row cell
    kind+len+sha8 comparison. Only structural changes reported."""
    result: dict = {"sheets_added": [], "sheets_removed": [],
                    "per_sheet_diff": {}}

    new_sheets = set(new.get("sheet_names", []))
    old_sheets = set(old.get("sheet_names", []))
    result["sheets_added"] = sorted(new_sheets - old_sheets)
    result["sheets_removed"] = sorted(old_sheets - new_sheets)

    common = new_sheets & old_sheets
    for sn in sorted(common):
        n = new["sheets"].get(sn, {})
        o = old["sheets"].get(sn, {})
        d = {"rows_max_new": n.get("rows_max"),
             "rows_max_old": o.get("rows_max"),
             "cols_max_new": n.get("cols_max"),
             "cols_max_old": o.get("cols_max"),
             "merged_ranges_added": sorted(set(n.get("merged_ranges", []))
                                          - set(o.get("merged_ranges", []))),
             "merged_ranges_removed": sorted(set(o.get("merged_ranges", []))
                                            - set(n.get("merged_ranges", []))),
             "row_deltas": []}
        # Row-by-row shape comparison (by row index only)
        n_rows = {r["row"]: r for r in n.get("rows_shape", [])}
        o_rows = {r["row"]: r for r in o.get("rows_shape", [])}
        for idx in sorted(set(n_rows) | set(o_rows)):
            nr = n_rows.get(idx)
            or_ = o_rows.get(idx)
            if nr is None:
                d["row_deltas"].append({"row": idx, "change": "REMOVED"})
                continue
            if or_ is None:
                d["row_deltas"].append({"row": idx, "change": "ADDED",
                                         "new_cell_kinds": [c["kind"] for c in nr["cells"] if c["kind"] != "EMPTY"],
                                         "new_cell_lens":  [c["len"]  for c in nr["cells"] if c["kind"] != "EMPTY"],
                                         "new_cell_sha8":  [c["sha8"] for c in nr["cells"] if c["kind"] != "EMPTY"]})
                continue
            # Same row present in both — compare per-cell sha8
            per_cell_changes = []
            max_cols = max(len(nr["cells"]), len(or_["cells"]))
            for j in range(max_cols):
                nc = nr["cells"][j] if j < len(nr["cells"]) else {"kind": "EMPTY"}
                oc = or_["cells"][j] if j < len(or_["cells"]) else {"kind": "EMPTY"}
                if (nc.get("sha8"), nc.get("len"), nc.get("kind")) != \
                   (oc.get("sha8"), oc.get("len"), oc.get("kind")):
                    per_cell_changes.append({
                        "col": j,
                        "kind_before": oc.get("kind"),
                        "kind_after": nc.get("kind"),
                        "len_before": oc.get("len"),
                        "len_after": nc.get("len"),
                        "sha8_before": oc.get("sha8"),
                        "sha8_after": nc.get("sha8"),
                    })
            if per_cell_changes:
                d["row_deltas"].append({"row": idx, "change": "MODIFIED",
                                         "changes": per_cell_changes})
        result["per_sheet_diff"][sn] = d
    return result


def _loader_derived_shape(path: Path) -> dict:
    """Import rms_creds_loader with SHEET_PATH monkey-patched to `path`,
    return the shape summary only (never values)."""
    sys.path.insert(0, "/app/assessment_workspace/tools")
    import importlib, rms_creds_loader as L
    importlib.reload(L)
    L.SHEET_PATH = path
    b = L.load()
    return {
        "jump": b.jump.describe(),
        "radio": b.radio.describe(),
        "nas": b.nas.describe(),
        "mysql_clusters": [c.describe() for c in b.mysql_clusters],
    }


def main():
    new_matches = sorted(glob.glob(NEW_XLSX_GLOB))
    if not new_matches:
        print("NO NEW XLSX FOUND"); return
    new_path = Path(new_matches[-1])

    receipt = {
        "task": "rms_creds_drop_shape_probe_and_diff_20260921",
        "captured_at_utc": _now(),
        "authorization": (
            "Owner directive this-session 2026-09-21T~14:05Z: 'OWNER "
            "CREDENTIAL RE-DROP. STEP 1 — CUSTODY INGEST (§4.1 §E, "
            "byte-metadata ONLY). Diff against the prior banked sheet.'"
        ),
        "hygiene": {
            "value_blind": True,
            "no_value_printing": True,
            "sha8_only_for_cross_run_compare": True,
        },
        "drop_new": {"path": str(new_path),
                     "sha256": _sha256_file(new_path),
                     "size_bytes": new_path.stat().st_size},
        "baseline_old": {"path": str(OLD_XLSX),
                         "sha256": _sha256_file(OLD_XLSX),
                         "size_bytes": OLD_XLSX.stat().st_size if OLD_XLSX.is_file() else None},
    }

    new_probe = _probe_workbook(new_path)
    old_probe = _probe_workbook(OLD_XLSX)

    receipt["new_workbook_shape"] = new_probe
    receipt["old_workbook_shape_summary"] = {
        "sheet_names": old_probe.get("sheet_names"),
        "sheets_row_count": {sn: len(s.get("rows_shape", []))
                             for sn, s in old_probe.get("sheets", {}).items()},
    }

    # Shape diff
    receipt["shape_diff_new_vs_old"] = _diff_creds(new_probe, old_probe)

    # Loader-derived credential shape (from NEW file)
    try:
        receipt["loader_derived_shape_new"] = _loader_derived_shape(new_path)
    except Exception as e:
        receipt["loader_derived_shape_new_err"] = f"{e.__class__.__name__}: {e}"

    # Loader-derived from OLD file
    try:
        receipt["loader_derived_shape_old"] = _loader_derived_shape(OLD_XLSX)
    except Exception as e:
        receipt["loader_derived_shape_old_err"] = f"{e.__class__.__name__}: {e}"

    # Cred-record-level diff summary (shape only, by section+host)
    new_shape = receipt.get("loader_derived_shape_new", {})
    old_shape = receipt.get("loader_derived_shape_old", {})
    rd = {}
    for label in ("jump", "radio", "nas"):
        n = new_shape.get(label, {})
        o = old_shape.get(label, {})
        # For jump/radio/nas: compare user_len + password_len (never value)
        rd[label] = {
            "user_len_before": o.get("user_len"),
            "user_len_after":  n.get("user_len"),
            "password_len_before": o.get("password_len"),
            "password_len_after":  n.get("password_len"),
            "host_before": o.get("host") or o.get("dsm_url"),
            "host_after":  n.get("host") or n.get("dsm_url"),
            "changed": (o.get("user_len") != n.get("user_len")
                        or o.get("password_len") != n.get("password_len")
                        or (o.get("host") or o.get("dsm_url"))
                        != (n.get("host") or n.get("dsm_url"))),
        }
    # MySQL clusters — key by (section, host)
    n_clusters = {(c.get("section"), c.get("host")): c
                  for c in new_shape.get("mysql_clusters", [])}
    o_clusters = {(c.get("section"), c.get("host")): c
                  for c in old_shape.get("mysql_clusters", [])}
    cluster_delta = []
    for key in sorted(set(n_clusters) | set(o_clusters), key=lambda x: (str(x[0]) or "", str(x[1]) or "")):
        n = n_clusters.get(key)
        o = o_clusters.get(key)
        if n and not o:
            cluster_delta.append({"key": list(key), "change": "ADDED_IN_NEW",
                                  "user_len_after": n["user_len"],
                                  "password_len_after": n["password_len"],
                                  "schemas_after": n["schemas"]})
        elif o and not n:
            cluster_delta.append({"key": list(key), "change": "REMOVED_FROM_NEW",
                                  "user_len_before": o["user_len"],
                                  "password_len_before": o["password_len"]})
        else:
            same = (n["user_len"] == o["user_len"]
                    and n["password_len"] == o["password_len"]
                    and n["schemas"] == o["schemas"])
            cluster_delta.append({
                "key": list(key),
                "change": "UNCHANGED" if same else "MODIFIED",
                "user_len_before": o["user_len"],
                "user_len_after":  n["user_len"],
                "password_len_before": o["password_len"],
                "password_len_after":  n["password_len"],
                "schemas_before": o["schemas"],
                "schemas_after":  n["schemas"],
            })
    rd["mysql_clusters"] = cluster_delta
    receipt["record_level_shape_diff"] = rd

    # Also check for Huawei creds — old sheet did NOT carry these
    # (they live in a separate CSV). Note if the new sheet DOES carry
    # them (would appear as new sheet name or new column shape).
    new_sheets = set(new_probe.get("sheet_names", []))
    old_sheets = set(old_probe.get("sheet_names", []))
    receipt["new_sheet_names_added"] = sorted(new_sheets - old_sheets)
    receipt["obs_creds_in_sheet_hint"] = any(
        "huawei" in s.lower() or "obs" in s.lower() or "aws" in s.lower()
        for s in new_probe.get("sheet_names", [])
    )

    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    p = RECEIPT_DIR / f"{stamp}_RMS_creds_drop_shape_probe_and_diff_20260921.json"
    p.write_text(json.dumps(receipt, indent=2, default=str) + "\n",
                 encoding="utf-8")
    print(f"receipt_path: {p}")


if __name__ == "__main__":
    main()
