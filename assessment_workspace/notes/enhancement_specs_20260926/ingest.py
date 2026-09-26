"""Read-only document ingestion: source hashes, ordered extracts, registry reconciliation."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CUSTODY = ROOT / "assessment_workspace/custody/owner_drops/enhancement_specs_20260926"
BASELINE = CUSTODY / "comparison_baselines/Master_Requirements_Registry_v4.xlsx"


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def workbook(path):
    wb = load_workbook(path, read_only=True, data_only=False)
    result = {}
    for sheet in wb:
        result[sheet.title] = [{"row": i, "values": list(row)} for i, row in enumerate(sheet.iter_rows(values_only=True), 1) if any(v is not None for v in row)]
    wb.close()
    return result


def keyed(rows, header_row=1):
    header = next(r["values"] for r in rows if r["row"] == header_row)
    records = [{**dict(zip(header, r["values"])), "_row": r["row"]} for r in rows if r["row"] > header_row and r["values"][0]]
    return records


docs = []
for path in sorted(CUSTODY.iterdir()):
    if path.suffix not in {".docx", ".xlsx"}:
        continue
    doc = {"name": path.name, "bytes": path.stat().st_size, "sha256": sha(path), "outcome": "processed"}
    if path.suffix == ".docx":
        source = Document(path)
        blocks = []
        for index, child in enumerate(source.element.body.iterchildren(), 1):
            if child.tag == qn("w:p"):
                p = Paragraph(child, source)
                if p.text.strip():
                    blocks.append({"block": index, "kind": "paragraph", "style": p.style.name if p.style else None, "text": p.text})
            elif child.tag == qn("w:tbl"):
                table = Table(child, source)
                blocks.append({"block": index, "kind": "table", "rows": [[c.text for c in r.cells] for r in table.rows]})
        dump(path.stem + ".json", blocks)
        lines = []
        for block in blocks:
            if block["kind"] == "paragraph":
                lines.append(f"[B{block['block']}] {block['text']}")
            else:
                lines.extend(f"[B{block['block']}R{i}] " + " | ".join(row) for i, row in enumerate(block["rows"], 1))
        (HERE / (path.stem + ".md")).write_text("\n\n".join(lines) + "\n")
        doc["nonempty_blocks"] = len(blocks)
        doc["tracked_insertions"] = len(source.element.xpath(".//w:ins"))
        doc["tracked_deletions"] = len(source.element.xpath(".//w:del"))
    else:
        data = workbook(path)
        dump(path.stem + ".json", data)
        doc["sheets"] = {name: len(rows) for name, rows in data.items()}
    docs.append(doc)
dump("DOCUMENT_MANIFEST.json", {"recorded_at": datetime.now(timezone.utc).isoformat(), "archive_sha256": sha(CUSTODY / "files_17.zip"), "count": len(docs), "documents": docs})

new = workbook(CUSTODY / "Master_Requirements_Registry.xlsx")
old = workbook(BASELINE)
rules = keyed(new["System Rules Registry"])
old_rules = keyed(old["System Rules Registry"])
qa = keyed(new["QA Verification"])
key = lambda row: (str(row.get("Doc", "")), str(row["Rule ID"]))
old_map, new_map = {key(r): r for r in old_rules}, {key(r): r for r in rules}
new_ids, qa_ids = set(new_map), {key(r) for r in qa}
changed = []
for item in sorted(new_ids & set(old_map)):
    delta = {col: {"previous": old_map[item].get(col), "incoming": new_map[item].get(col)}
             for col in set(old_map[item]) | set(new_map[item])
             if col != "_row" and old_map[item].get(col) != new_map[item].get(col)}
    if delta:
        changed.append({"key": item, "columns": delta})
new_norms = [r for r in rules if re.fullmatch(r"(?:EX|DQ)-\d+", str(r["Rule ID"]))]
security = workbook(CUSTODY / "Security_Assurance_Promise_Set.xlsx")
promises = keyed(security["Security Assurance Set"])
new_promises = [r for r in promises if r.get("#") in {"S-33", "S-34"}]
old_security = workbook(CUSTODY / "comparison_baselines/Security_Assurance_Promise_Set_v6.xlsx")
old_promises = {r["#"]: r for r in keyed(old_security["Security Assurance Set"])}
dump("NEW_NORMATIVE_ROWS.json", {"rules": new_norms, "promises": new_promises})
dump("REGISTRY_RECONCILIATION.json", {
    "baseline": str(BASELINE.relative_to(ROOT)), "baseline_sha256": sha(BASELINE),
    "baseline_warning": "20 September v4 baseline re-fetched from the prior custody manifest URL and SHA-verified. Deltas are relative to that595-row file, not to an unlocated602-row intermediate workbook.",
    "baseline_rules": len(old_rules), "incoming_rules": len(rules), "incoming_unique_doc_rule_keys": len(new_ids),
    "incoming_qa_rows": len(qa), "missing_qa_keys": sorted(new_ids - qa_ids), "extra_qa_keys": sorted(qa_ids - new_ids),
    "duplicate_rule_keys": [list(k) + [v] for k, v in Counter(key(r) for r in rules).items() if v > 1],
    "added_since_available_baseline": [new_map[k] for k in sorted(new_ids - set(old_map))],
    "removed_since_available_baseline": [old_map[k] for k in sorted(set(old_map) - new_ids)],
    "changed_since_available_baseline": changed,
    "ex_rule_count": sum(str(r["Rule ID"]).startswith("EX-") for r in rules),
    "dq_rule_count": sum(str(r["Rule ID"]).startswith("DQ-") for r in rules),
    "security_ids": [r["#"] for r in promises],
    "security_added_ids": [r["#"] for r in promises if r["#"] not in old_promises],
    "security_removed_ids": sorted(set(old_promises) - {r["#"] for r in promises}),
    "security_changed_rows": [{"id": r["#"], "columns": {k: {"previous": old_promises[r["#"]].get(k), "incoming": v}
                              for k, v in r.items() if k != "_row" and old_promises[r["#"]].get(k) != v}}
                              for r in promises if r["#"] in old_promises and any(k != "_row" and old_promises[r["#"]].get(k) != v for k,v in r.items())],
})
print(json.dumps({"documents": len(docs), "rules": len(rules), "qa_rows": len(qa), "missing_qa": sorted(new_ids-qa_ids), "added_vs_20260920_v4": len(new_ids-set(old_map)), "changed_vs_20260920_v4": len(changed)}, indent=2))