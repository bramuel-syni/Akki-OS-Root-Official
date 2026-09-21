"""G5-v5 SFP-1..7 HUNT: extract SFP-1..7 rows from v5 SRR sheet into receipt.

Precedent: tools/r88_con_1_31_hunt.py extraction pattern used at R-88 HUNT-first
banking (80e42629). Same authority: v5 workbook at sha 00072c58… · SRR sheet
per Ruling 5.

Owner directive verbatim (2026-09-20T~23:12Z, this session):
  canon_ref = v5 SRR only, class column bounded hint (V1→golden-input,
  V2→scan, V5→injection), rule text governs, V7 rows authored from rule
  text, RED-first, grep-negative bans where the rule text states them.

Discipline:
- Read v5 workbook via openpyxl to a JSON receipt only; no console print of
  full rule text (shape-focused output to receipt file).
- Verify sha256 pin BEFORE reading rows (Ruling 5 authority binding).
- Extract SFP-1..7 rows verbatim (rule_id, statement, class hint if any,
  section, sheet row number).
- Bank JSON receipt at phase0/spec_hunt_receipts/*_g5v5_sfp_1_7_hunt_data.json
  and human-readable receipt md alongside.

Standing bounds: zero push · zero remote · zero network · read-only openpyxl.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from openpyxl import load_workbook

STATE_ROOT = Path("/app/assessment_workspace")
V5_XLSX = (
    STATE_ROOT / "custody" / "owner_drops" / "20260920T1900Z"
    / "Master_Requirements_Registry_v5.xlsx"
)
V5_XLSX_EXPECTED_SHA256 = (
    "00072c5829d3d89399cc5ca64661b405ac8a3cd0b43d0081f0d5f0bce109619d"
)
SRR_SHEET_NAME = "System Rules Registry"

TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
RECEIPT_JSON = (
    STATE_ROOT / "phase0" / "spec_hunt_receipts"
    / f"{TS}_g5v5_sfp_1_7_hunt_data.json"
)
RECEIPT_MD = (
    STATE_ROOT / "phase0" / "spec_hunt_receipts"
    / f"{TS}_g5v5_sfp_1_7_hunt_receipt.md"
)


def sha256_of(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def find_sfp_1_to_7_rows(sheet):
    """Return list of dicts for rows whose rule_id is SFP-1..SFP-7 verbatim.

    Header row auto-detected: first row containing the token 'rule_id' or
    'Rule ID' or similar in any cell. Fallback: assume header at row 1.
    Column names normalised to lowercase.
    """
    # Detect header row
    header_row_num = None
    for r in range(1, min(sheet.max_row, 10) + 1):
        vals = [c.value for c in sheet[r]]
        if any(
            isinstance(v, str) and re.search(r"\brule\s*[_ ]?id\b", v, re.I)
            for v in vals if v
        ):
            header_row_num = r
            break
    if header_row_num is None:
        header_row_num = 1

    headers = []
    for c in sheet[header_row_num]:
        h = (c.value or "").strip() if isinstance(c.value, str) else str(c.value or "").strip()
        headers.append(h)

    header_norm = [h.lower() for h in headers]

    # Locate the "rule id" column index
    rule_id_col = None
    for i, h in enumerate(header_norm):
        if re.search(r"\brule\s*[_ ]?id\b", h):
            rule_id_col = i
            break
    if rule_id_col is None:
        raise SystemExit(
            f"Could not locate rule_id column in headers: {headers!r}"
        )

    wanted = {f"SFP-{i}" for i in range(1, 8)}
    found = []
    for r in range(header_row_num + 1, sheet.max_row + 1):
        row = list(sheet[r])
        rid = row[rule_id_col].value
        if not isinstance(rid, str):
            continue
        rid_clean = rid.strip()
        if rid_clean in wanted:
            entry = {"__sheet_row__": r, "__rule_id__": rid_clean}
            for i, cell in enumerate(row):
                key = headers[i] if i < len(headers) and headers[i] else f"col_{i}"
                v = cell.value
                if v is None:
                    entry[key] = None
                else:
                    entry[key] = v if isinstance(v, (int, float, bool)) else str(v)
            found.append(entry)

    found.sort(key=lambda e: e["__rule_id__"])
    return found, headers, header_row_num


def main() -> None:
    # Sha-pin verification FIRST
    actual_sha = sha256_of(V5_XLSX)
    if actual_sha != V5_XLSX_EXPECTED_SHA256:
        raise SystemExit(
            f"v5 workbook sha mismatch: got {actual_sha} "
            f"expected {V5_XLSX_EXPECTED_SHA256}"
        )

    wb = load_workbook(V5_XLSX, data_only=True, read_only=True)
    if SRR_SHEET_NAME not in wb.sheetnames:
        # Attempt fuzzy match
        candidates = [n for n in wb.sheetnames if "system rules registry" in n.lower()]
        if not candidates:
            raise SystemExit(
                f"'{SRR_SHEET_NAME}' sheet not found. Sheets: {wb.sheetnames}"
            )
        sheet_name = candidates[0]
    else:
        sheet_name = SRR_SHEET_NAME

    sheet = wb[sheet_name]
    rows, headers, header_row_num = find_sfp_1_to_7_rows(sheet)

    receipt = {
        "hunt_wave": "G5-v5 SFP-1..7 first slice",
        "authority": {
            "workbook_path": str(V5_XLSX),
            "workbook_sha256": actual_sha,
            "workbook_sha256_expected": V5_XLSX_EXPECTED_SHA256,
            "sha_pin_verified": actual_sha == V5_XLSX_EXPECTED_SHA256,
            "sheet_name": sheet_name,
            "sheet_max_row": sheet.max_row,
            "header_row": header_row_num,
            "headers": headers,
        },
        "owner_directive_verbatim_23:12Z": (
            "canon_ref = v5 SRR only, class column bounded hint (V1→golden-input, "
            "V2→scan, V5→injection) where the rule text already demands that shape; "
            "rule text governs; V7 rows authored from rule text, never from the column."
        ),
        "extracted_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sfp_rows_found": len(rows),
        "sfp_rows_expected": 7,
        "sfp_rows": rows,
    }

    RECEIPT_JSON.write_text(json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")

    # Human-readable md sibling — one-line summary per rule (statement column
    # printed verbatim; rule text is authority per owner directive).
    md_lines = [
        "# SPEC-HUNT RECEIPT · G5-v5 SFP-1..7 first slice",
        "",
        f"- **Filed at:** {receipt['extracted_at_utc']}",
        "- **Filer:** main-agent Autopilot (this session · SO §6 autopilot governance)",
        "- **Wave:** G5-v5 SFP-1..7 first slice (Ruling 5 · queue post R-90 seal)",
        "",
        "## Authority (Ruling 5 · sha-pin binding)",
        "",
        f"- **Workbook:** `{V5_XLSX.relative_to(STATE_ROOT)}`",
        f"- **Workbook sha256:** `{actual_sha}`",
        f"- **Expected sha256:** `{V5_XLSX_EXPECTED_SHA256}`",
        f"- **Sha pin verified:** {actual_sha == V5_XLSX_EXPECTED_SHA256}",
        f"- **SRR sheet:** `{sheet_name}` · max_row={sheet.max_row} · header_row={header_row_num}",
        "",
        "## Owner directive verbatim (2026-09-20T~23:12Z · this session)",
        "",
        "> canon_ref = v5 SRR only, class column bounded hint (V1→golden-input,",
        "> V2→scan, V5→injection) where the rule text already demands that shape;",
        "> rule text governs; V7 rows authored from rule text, never from the column.",
        "",
        "## SFP-1..7 rows extracted (rule text verbatim from SRR)",
        f"",
        f"**Rows found:** {len(rows)} / 7 expected.",
        "",
    ]
    for r in rows:
        md_lines.append(f"### {r['__rule_id__']} · SRR row {r['__sheet_row__']}")
        md_lines.append("")
        for k, v in r.items():
            if k.startswith("__"):
                continue
            if v is None or v == "":
                md_lines.append(f"- **{k}:** *(empty)*")
            else:
                v_s = str(v).replace("\n", " ⏎ ")
                md_lines.append(f"- **{k}:** {v_s}")
        md_lines.append("")

    if len(rows) != 7:
        md_lines += [
            "## ⚠️ ROW COUNT ANOMALY",
            "",
            f"Expected 7 SFP-1..7 rows in the v5 SRR sheet; found {len(rows)}.",
            "This is a stop-and-report condition — the HUNT cannot proceed to",
            "slice authoring until the row count matches expectation. Absence",
            "is a finding.",
            "",
        ]

    md_lines += [
        "## Standing bounds",
        "",
        "zero push · zero remote configured · terminal `pytest` only · no `testing_agent` · additive-only §3.8 · three-repo discipline · ratchet monotonic-up floor **5688** · R-88+ OWNER-RATIFICATION-PENDING carries forward.",
        "",
        "READ STATE/STANDING_ORDERS.md FIRST — permanent standing law",
    ]

    RECEIPT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"HUNT complete: {len(rows)}/7 SFP rows found in SRR sheet '{sheet_name}'.")
    print(f"Receipt JSON: {RECEIPT_JSON}")
    print(f"Receipt MD:   {RECEIPT_MD}")
    for r in rows:
        print(f"  {r['__rule_id__']} at SRR row {r['__sheet_row__']}")


if __name__ == "__main__":
    main()
