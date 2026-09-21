"""Value-blind structural inspection of the CURRENT custody NAS-creds sheet.

Emits ONLY:
    * sheet names
    * per row on 'NAS creds': col-count + per-cell (kind, len, first2_chars_letter_bucket)
    * per row on 'NAS Guide + Cred': same, but only for rows likely to have creds
    * detected {nas_url, user, password} shape as the loader would parse them
    * plus a 'candidate password rows' scan (anything after 'password' label)
    * plus a 'multiple candidates' warning if we see >1 password-shaped cell

NEVER emits raw cell text; only length and a coarse "starts_with_upper /
starts_with_lower / starts_with_digit / starts_with_symbol" bucket + a
SHA256 first-8 hex of the (utf-8 encoded) cell for cross-run comparison.

This is used ONE-shot to answer 'is the loader picking the wrong cell?'
It bank output as a state-hygiene receipt.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import openpyxl

SRC = Path("/app/backend/estate_keys/data_sources/RMS_Connection_Creds.xlsx")
OUT = Path("/app/assessment_workspace/phase0/connectivity_receipts")

def _hash8(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="ignore")).hexdigest()[:8]

def _bucket(s: str) -> str:
    if not s:
        return "EMPTY"
    c = s[0]
    if c.isupper():
        return "UPPER"
    if c.islower():
        return "LOWER"
    if c.isdigit():
        return "DIGIT"
    return "SYM"

def _kind(s: str) -> str:
    if not s:
        return "EMPTY"
    low = s.lower()
    if low.startswith(("http://", "https://")):
        return "URL"
    if low.startswith("username:"):
        return "USERNAME_LABEL_ROW"
    if low.startswith("password:"):
        return "PASSWORD_LABEL_ROW"
    if re.match(r"^\d+\.", s):
        return "NUMBERED_STEP"
    if re.match(r"^\s*\d{1,3}(\.\d{1,3}){3}\s*$", s):
        return "IPV4"
    if re.match(r"^\s*\d{1,5}\s*$", s):
        return "SHORT_NUMBER"
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

def main():
    wb = openpyxl.load_workbook(SRC, data_only=True)
    out = {
        "captured_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "src": str(SRC),
        "src_sha256_first_16": hashlib.sha256(SRC.read_bytes()).hexdigest()[:16],
        "sheet_names": wb.sheetnames,
    }

    ns_map: dict = {}
    for sheet_name in ("NAS creds", "NAS Guide + Cred"):
        if sheet_name not in wb.sheetnames:
            ns_map[sheet_name] = {"missing": True}
            continue
        ws = wb[sheet_name]
        rows = []
        for i, r in enumerate(ws.iter_rows(values_only=True)):
            cells = [_cell_shape(c) for c in r]
            # only bank rows with at least one non-empty cell
            if any(c["kind"] != "EMPTY" for c in cells):
                rows.append({"row": i, "cells": cells})
        ns_map[sheet_name] = {
            "rows_shape": rows,
        }
    out["sheets"] = ns_map

    # Loader-parse candidates
    ns = out["sheets"].get("NAS creds", {})
    ns_rows = ns.get("rows_shape", [])
    # first URL, first USERNAME_LABEL_ROW, first PASSWORD_LABEL_ROW
    url_hits, user_hits, pass_hits = [], [], []
    for r in ns_rows:
        for j, c in enumerate(r["cells"]):
            if c["kind"] == "URL":
                url_hits.append({"row": r["row"], "col": j, **c})
            if c["kind"] == "USERNAME_LABEL_ROW":
                user_hits.append({"row": r["row"], "col": j, **c})
            if c["kind"] == "PASSWORD_LABEL_ROW":
                pass_hits.append({"row": r["row"], "col": j, **c})
    out["loader_hit_map"] = {
        "url_hits_count": len(url_hits),
        "url_hits": url_hits[:6],
        "username_label_hits_count": len(user_hits),
        "username_label_hits": user_hits[:6],
        "password_label_hits_count": len(pass_hits),
        "password_label_hits": pass_hits[:6],
    }

    # What the loader would extract (using its regex-y approach)
    # Emulate loader logic in shape:
    guessed_user_len = None
    guessed_pass_len = None
    for r in ns_rows:
        for c in r["cells"]:
            if c["kind"] == "USERNAME_LABEL_ROW" and guessed_user_len is None:
                # loader does: first.split(":",1)[1].strip() — we can only
                # measure the SHA/length of the full "username:xxx" line
                guessed_user_len = c["len"] - len("username:")
            if c["kind"] == "PASSWORD_LABEL_ROW" and guessed_pass_len is None:
                guessed_pass_len = c["len"] - len("password:")
    out["loader_expected_extraction"] = {
        "user_len_derived_from_username_label_row": guessed_user_len,
        "pass_len_derived_from_password_label_row": guessed_pass_len,
    }

    # Bank
    OUT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = OUT / f"{stamp}_NAS_creds_structure_probe_S2_v3.json"
    path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"receipt_path: {path}")

if __name__ == "__main__":
    main()
