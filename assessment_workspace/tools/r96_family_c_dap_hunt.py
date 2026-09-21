"""HUNT script for R-96 Family C: DAP-1..38 rows from v5 Master Requirements Registry SRR sheet.

Pure-read, no mutation, no network. Reads v5 SRR workbook sha-pinned at
`00072c5829d3d89399cc5ca64661b405ac8a3cd0b43d0081f0d5f0bce109619d`.
Extracts all rows whose rule_id begins with 'DAP-' and outputs a JSON hunt-data
receipt mirroring the shape of R-94's family-b-doc5-northena-hunt-data.json.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from openpyxl import load_workbook

SRR_PATH = Path("/app/assessment_workspace/custody/owner_drops/20260920T1900Z/Master_Requirements_Registry_v5.xlsx")
EXPECTED_SHA = "00072c5829d3d89399cc5ca64661b405ac8a3cd0b43d0081f0d5f0bce109619d"

def verify_workbook_sha() -> str:
    sha = hashlib.sha256(SRR_PATH.read_bytes()).hexdigest()
    assert sha == EXPECTED_SHA, f"SRR sha mismatch: expected {EXPECTED_SHA}, got {sha}"
    return sha

def main() -> None:
    workbook_sha = verify_workbook_sha()
    wb = load_workbook(SRR_PATH, read_only=True, data_only=True)
    ws = wb["System Rules Registry"]

    # Inspect header row
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]
    print("HEADERS:", headers)

    # Find columns
    def col_idx(name_variants):
        for i, h in enumerate(headers):
            if h and isinstance(h, str):
                for v in name_variants:
                    if v.lower() in h.lower():
                        return i
        return None

    id_col = col_idx(["Rule ID", "ID", "rule_id"])
    stmt_col = col_idx(["Statement", "Rule text", "Text", "Statement of Rule"])
    obj_col = col_idx(["Objective"])
    prom_col = col_idx(["Promise"])
    doc_col = col_idx(["Doc", "Document"])
    status_col = col_idx(["Status"])
    class_col = col_idx(["Class", "Enforcement Class"])
    domain_col = col_idx(["Domain"])
    src_col = col_idx(["Source", "file", "line"])
    rel_col = col_idx(["Relationship"])

    print(f"Column indices: id={id_col} stmt={stmt_col} obj={obj_col} prom={prom_col} doc={doc_col} status={status_col} class={class_col} domain={domain_col} src={src_col} rel={rel_col}")

    dap_rows = []
    for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        if len(row) <= id_col:
            continue
        rid = row[id_col]
        if isinstance(rid, str) and rid.strip().upper().startswith("DAP-"):
            dap_rows.append({
                "srr_row": row_num,
                "rule_id": rid.strip(),
                "statement": row[stmt_col] if stmt_col is not None and len(row) > stmt_col else None,
                "objective": row[obj_col] if obj_col is not None and len(row) > obj_col else None,
                "promise": row[prom_col] if prom_col is not None and len(row) > prom_col else None,
                "doc": row[doc_col] if doc_col is not None and len(row) > doc_col else None,
                "status": row[status_col] if status_col is not None and len(row) > status_col else None,
                "enforcement_class": row[class_col] if class_col is not None and len(row) > class_col else None,
                "domain": row[domain_col] if domain_col is not None and len(row) > domain_col else None,
                "source_file_line": row[src_col] if src_col is not None and len(row) > src_col else None,
                "relationship": row[rel_col] if rel_col is not None and len(row) > rel_col else None,
            })
    wb.close()

    print(f"\nTotal DAP rows found: {len(dap_rows)}")
    for r in dap_rows[:5]:
        print(json.dumps(r, indent=2, default=str)[:500])
        print("---")

    out = {
        "wave": "R-96-CANDIDATE-CP-G5V5-DAP-FAMILY-C-HUNT",
        "family": "C",
        "authority_pins": {
            "v5_srr_workbook_sha256": workbook_sha,
            "v5_srr_workbook_path": "custody/owner_drops/20260920T1900Z/Master_Requirements_Registry_v5.xlsx",
        },
        "total_dap_rows": len(dap_rows),
        "rows": dap_rows,
        "hunt_at_utc": "2026-09-21T06:10:00Z",
    }
    out_path = Path("/app/assessment_workspace/phase0/spec_hunt_receipts/20260921T061000Z_r96_family_c_dap_1_38_hunt_data.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, default=str, ensure_ascii=False))
    print(f"\nHUNT data banked at: {out_path}")

if __name__ == "__main__":
    main()
