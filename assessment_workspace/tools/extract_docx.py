#!/usr/bin/env python3
"""Extract text from every canon .docx into a parallel .txt (paragraphs preserved).
Also extract tables as pipe-separated rows so nothing is silently dropped."""
import os
import sys
from pathlib import Path
from docx import Document

SRC = Path("/app/assessment_workspace/canon/unpacked")
DST = Path("/app/assessment_workspace/canon/text")
DST.mkdir(parents=True, exist_ok=True)

def iter_block_items(parent):
    """Yield paragraphs and tables in document order."""
    from docx.oxml.ns import qn
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    parent_elm = parent.element.body
    for child in parent_elm.iterchildren():
        if child.tag == qn("w:p"):
            yield Paragraph(child, parent)
        elif child.tag == qn("w:tbl"):
            yield Table(child, parent)

def render_table(tbl):
    rows = []
    for row in tbl.rows:
        cells = [c.text.replace("\n", " ").strip() for c in row.cells]
        rows.append(" | ".join(cells))
    return "\n".join(rows)

for docx_path in sorted(SRC.glob("*.docx")):
    doc = Document(str(docx_path))
    out_lines = []
    out_lines.append(f"# SOURCE FILE: {docx_path.name}")
    out_lines.append("")
    for block in iter_block_items(doc):
        cls = block.__class__.__name__
        if cls == "Paragraph":
            text = block.text.rstrip()
            style = block.style.name if block.style else ""
            if text:
                if style and style.lower() != "normal":
                    out_lines.append(f"[{style}] {text}")
                else:
                    out_lines.append(text)
            else:
                out_lines.append("")
        elif cls == "Table":
            out_lines.append("<<TABLE>>")
            out_lines.append(render_table(block))
            out_lines.append("<<END TABLE>>")
    out_path = DST / (docx_path.stem + ".txt")
    out_path.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"WROTE {out_path}  ({out_path.stat().st_size} bytes, {len(out_lines)} lines)")
