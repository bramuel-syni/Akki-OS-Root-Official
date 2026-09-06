"""Extract all .docx and .xlsx artifacts under
/app/assessment_workspace/canon/drops/20260907/ into readable text/JSON
under a parallel extracted/text/ tree. Preserves paragraph order for
.docx; preserves sheet+row+column for .xlsx (openpyxl). No summarisation.
"""
from __future__ import annotations
import json
import pathlib
import sys

import docx  # python-docx
from openpyxl import load_workbook

RAW = pathlib.Path("/app/assessment_workspace/canon/drops/20260907/raw")
EXTRACTED = pathlib.Path("/app/assessment_workspace/canon/drops/20260907/extracted")
TEXT = EXTRACTED / "text"
TEXT.mkdir(parents=True, exist_ok=True)


def _docx_to_text(src: pathlib.Path, dst: pathlib.Path) -> dict:
    """Emit paragraphs + table cells preserving order. Docstring-quotes
    verbatim. Returns provenance record for the manifest."""
    d = docx.Document(str(src))
    lines: list[str] = []
    paragraph_count = 0
    for p in d.paragraphs:
        style = (p.style.name if p.style else "") or ""
        text = p.text
        lines.append(f"[P style={style!r}] {text}")
        paragraph_count += 1
    table_count = 0
    for t_idx, table in enumerate(d.tables):
        lines.append(f"\n=== TABLE {t_idx} · rows={len(table.rows)} cols={len(table.columns)} ===")
        for r_idx, row in enumerate(table.rows):
            for c_idx, cell in enumerate(row.cells):
                cell_text = cell.text.replace("\n", " \\n ")
                lines.append(f"[T{t_idx}·R{r_idx}·C{c_idx}] {cell_text}")
        table_count += 1
    dst.write_text("\n".join(lines))
    return {"paragraphs": paragraph_count, "tables": table_count, "bytes": dst.stat().st_size}


def _xlsx_to_json_and_md(src: pathlib.Path, dst_json: pathlib.Path, dst_md: pathlib.Path) -> dict:
    """Load every sheet + every non-empty row. Emit both JSON (structured)
    and markdown table (readable). Preserves cell order left-to-right,
    top-to-bottom."""
    wb = load_workbook(str(src), data_only=True)
    all_sheets: dict = {}
    md_lines: list[str] = []
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        rows: list[list] = []
        max_col = 0
        for row in ws.iter_rows(values_only=True):
            cells = [("" if v is None else str(v)) for v in row]
            # trim trailing empties
            while cells and cells[-1] == "":
                cells.pop()
            if not cells:
                continue
            rows.append(cells)
            max_col = max(max_col, len(cells))
        all_sheets[sheet_name] = {"rows": rows, "row_count": len(rows), "max_col": max_col}
        md_lines.append(f"## sheet: `{sheet_name}` · rows={len(rows)} · max_col={max_col}\n")
        if rows:
            hdr = rows[0]
            hdr_padded = hdr + [""] * (max_col - len(hdr))
            md_lines.append("| " + " | ".join(str(c).replace("|", "\\|") for c in hdr_padded) + " |")
            md_lines.append("|" + "---|" * max_col)
            for r in rows[1:]:
                r_padded = r + [""] * (max_col - len(r))
                md_lines.append("| " + " | ".join(str(c).replace("|", "\\|").replace("\n", " \\n ") for c in r_padded) + " |")
            md_lines.append("")
    dst_json.write_text(json.dumps(all_sheets, indent=2))
    dst_md.write_text("\n".join(md_lines))
    return {"sheets": len(wb.sheetnames), "sheet_names": wb.sheetnames}


def process(src: pathlib.Path) -> dict:
    rel = src.name
    stem = src.stem
    provenance = {"src": str(src), "size_bytes": src.stat().st_size}
    if src.suffix.lower() == ".docx":
        dst = TEXT / f"{stem}.txt"
        provenance.update(_docx_to_text(src, dst))
        provenance["text_path"] = str(dst)
    elif src.suffix.lower() == ".xlsx":
        dst_json = TEXT / f"{stem}.json"
        dst_md = TEXT / f"{stem}.md"
        provenance.update(_xlsx_to_json_and_md(src, dst_json, dst_md))
        provenance["json_path"] = str(dst_json)
        provenance["md_path"] = str(dst_md)
    else:
        raise ValueError(f"unsupported: {src.suffix}")
    return provenance


if __name__ == "__main__":
    targets = [
        RAW / "doc0_governance_architecture.docx",
        RAW / "security_assurance_promise_set.xlsx",
        EXTRACTED / "files_11" / "Rules_Service_Spec_v1.docx",
        EXTRACTED / "files_11" / "Rule_Book_Library_v1.xlsx",
        EXTRACTED / "files_11" / "System_Rules_Registry.xlsx",
        EXTRACTED / "files_12" / "Security_Promise_Set_Amendments.docx",
        EXTRACTED / "files_13" / "Security_Amendments_Trojan_Whisper.docx",
    ]
    manifest = []
    for t in targets:
        assert t.exists(), t
        r = process(t)
        r["name"] = t.name
        manifest.append(r)
        print(f"[ok] {t.name}: {r}")
    (EXTRACTED / "extraction_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"\nManifest: {EXTRACTED / 'extraction_manifest.json'}")
