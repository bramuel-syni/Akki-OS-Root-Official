"""Structure-only probe · v2 — REDACTING · never emits cell/header text.

Reads /app/assessment_workspace/custody/credentials/rms_connection_creds_v1.xlsx
and emits a JSON structural map containing ONLY:
  - workbook: sheet count.
  - per sheet: name (workbook metadata, safe), rows_total_incl_header,
    rows_with_any_data, header_kinds (list of KIND labels only — the raw
    header STRING is never emitted), column_count, per-column value
    profile (kind, present_count, empty_count, avg_len_band, has_multiline,
    has_nonascii, looks_like_ip4_count, looks_like_port_count),
    per-row cell KIND fingerprint (positional list of KIND labels, no
    values).

Also classifies free-form / multi-line cells as SUSPECTED_VALUE_IN_HEADER
regardless of whether they sit in row 0 (fixes the row-0-was-not-a-header
bug that caused the 2026-09-17T~15:37Z stdout echo incident).
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from openpyxl import load_workbook

SRC = Path("/app/assessment_workspace/custody/credentials/rms_connection_creds_v1.xlsx")
OUT_DIR = Path("/app/assessment_workspace/phase0/estate_reconciliation")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "rms_creds_structure_20260917.json"

# regex on header shape ONLY (not on values)
SECRET_H = re.compile(r"(?i)\b(password|passwd|pass|pwd|secret|token|api[_ ]?key|private[_ ]?key|pem|cert|hash|salt|otp)\b")
HOST_H   = re.compile(r"(?i)\b(host|hostname|address|ip|endpoint|url|fqdn|bastion|jump)\b")
PORT_H   = re.compile(r"(?i)\b(port|tcp|udp)\b")
USER_H   = re.compile(r"(?i)\b(user|username|login|account|principal|role)\b")
DB_H     = re.compile(r"(?i)\b(db|database|schema|catalog|tenant)\b")
SVC_H    = re.compile(r"(?i)\b(service|system|app|kind|type|purpose|resource|component)\b")
LABEL_H  = re.compile(r"(?i)\b(name|label|env|environment|region|notes?|remarks?|description)\b")

IP4_RX = re.compile(r"^\s*(?:\d{1,3}\.){3}\d{1,3}\s*$")
PORT_RX = re.compile(r"^\s*\d{1,5}\s*$")

MAX_HEADER_LEN = 40  # anything longer than 40 chars in the header row is not a header


def classify_header_text(h) -> str:
    """Classify the header STRING; the string itself is never emitted."""
    if h is None or str(h).strip() == "":
        return "UNKNOWN"
    s = str(h)
    if "\n" in s or len(s) > MAX_HEADER_LEN:
        return "SUSPECTED_VALUE_IN_HEADER"
    if SECRET_H.search(s): return "SECRET"
    if HOST_H.search(s):   return "HOST"
    if PORT_H.search(s):   return "PORT"
    if USER_H.search(s):   return "USER"
    if DB_H.search(s):     return "DB"
    if SVC_H.search(s):    return "SERVICE"
    if LABEL_H.search(s):  return "LABEL"
    return "OTHER"


def classify_cell(header_kind: str, v) -> str:
    if v is None or str(v).strip() == "":
        return "EMPTY"
    s = str(v)
    # if header signals SECRET, force SECRET
    if header_kind == "SECRET":
        return "SECRET"
    # if header is not a header at all, best-effort by shape (no value echoed)
    if header_kind == "SUSPECTED_VALUE_IN_HEADER" or header_kind in {"UNKNOWN", "OTHER"}:
        if "\n" in s:
            return "MULTILINE_FREEFORM"
        if IP4_RX.match(s):
            return "IPV4"
        if PORT_RX.match(s):
            return "PORT"
        # heuristic: if it contains any non-ascii punctuation like ! ? & @ #, it's a likely secret
        if re.search(r"[!@#\$%\^&\*\?\+=/]", s):
            return "SUSPECTED_SECRET"
        if len(s) <= 16 and re.fullmatch(r"[A-Za-z][A-Za-z0-9_\-\.]*", s):
            return "IDENTIFIER"
        return "FREEFORM"
    return header_kind


def length_band(v) -> str:
    if v is None:
        return "EMPTY"
    n = len(str(v))
    if n == 0:            return "EMPTY"
    if n <= 8:            return "1-8"
    if n <= 16:           return "9-16"
    if n <= 32:           return "17-32"
    if n <= 64:           return "33-64"
    return "65+"


def has_multiline(v) -> bool:
    return v is not None and "\n" in str(v)


def has_nonascii(v) -> bool:
    return v is not None and any(ord(c) > 127 for c in str(v))


def profile_column(cells: list) -> dict:
    band_counter = Counter()
    ml = 0
    na = 0
    ip4 = 0
    prt = 0
    present = 0
    empty = 0
    for v in cells:
        if v is None or str(v).strip() == "":
            empty += 1
            band_counter["EMPTY"] += 1
        else:
            present += 1
            band_counter[length_band(v)] += 1
            if has_multiline(v):
                ml += 1
            if has_nonascii(v):
                na += 1
            s = str(v)
            if IP4_RX.match(s):
                ip4 += 1
            if PORT_RX.match(s):
                prt += 1
    return {
        "present": present,
        "empty": empty,
        "len_band_hist": dict(band_counter),
        "multiline_count": ml,
        "nonascii_count": na,
        "looks_like_ipv4_count": ip4,
        "looks_like_port_count": prt,
    }


def main() -> None:
    wb = load_workbook(str(SRC), data_only=True, read_only=True)
    out = {
        "source_path": str(SRC),
        "sheet_count": len(wb.sheetnames),
        "sheets": [],
    }
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        rows = [tuple(r) for r in ws.iter_rows(values_only=True)]
        if not rows:
            out["sheets"].append({"name": sheet_name, "rows_total_incl_header": 0,
                                  "rows_with_any_data": 0, "header_kinds": [],
                                  "column_count": 0, "columns": [], "row_kind_fingerprints": []})
            continue
        headers_raw = rows[0]
        header_kinds = [classify_header_text(h) for h in headers_raw]
        col_count = len(headers_raw)

        # collect column-wise cells (all rows including header row, so profile
        # picks up the header-row misuse too)
        columns = [[] for _ in range(col_count)]
        for r in rows:
            for i in range(col_count):
                v = r[i] if i < len(r) else None
                columns[i].append(v)

        # profile each column BUT never emit cell values
        column_profiles = []
        for i, col_cells in enumerate(columns):
            column_profiles.append({
                "col_index": i,
                "header_kind": header_kinds[i] if i < len(header_kinds) else "UNKNOWN",
                "profile": profile_column(col_cells),
            })

        # per-row cell KIND fingerprints (positional, no values)
        row_kind_fps = []
        rows_with_data = 0
        for r in rows[1:]:  # skip declared header row
            kinds = []
            any_present = False
            for i in range(col_count):
                v = r[i] if i < len(r) else None
                hk = header_kinds[i] if i < len(header_kinds) else "UNKNOWN"
                k = classify_cell(hk, v)
                if k != "EMPTY":
                    any_present = True
                kinds.append(k)
            if any_present:
                rows_with_data += 1
                row_kind_fps.append(kinds)

        out["sheets"].append({
            "name": sheet_name,
            "rows_total_incl_header": len(rows),
            "rows_with_any_data": rows_with_data,
            "header_kinds": header_kinds,
            "column_count": col_count,
            "columns": column_profiles,
            "row_kind_fingerprints": row_kind_fps,
        })

    OUT.write_text(json.dumps(out, indent=2))
    # print ONLY structural metadata: sheet count, per-sheet row counts, header kinds
    print(f"WROTE {OUT}")
    print(f"SHEET_COUNT={out['sheet_count']}")
    for s in out["sheets"]:
        print(f"  sheet={s['name']!r} rows_total={s['rows_total_incl_header']} "
              f"rows_with_data={s['rows_with_any_data']} col_count={s['column_count']} "
              f"header_kinds={s['header_kinds']}")


if __name__ == "__main__":
    main()
