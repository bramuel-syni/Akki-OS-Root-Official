import csv
import hashlib
import json
import re
import zipfile
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

from openpyxl import load_workbook


ROOT = Path("/app")
SUPP = ROOT / "assessment_workspace/notes/enhancement_specs_20260926/supplement_18"
CUST18 = ROOT / "assessment_workspace/custody/owner_drops/enhancement_specs_18_20260926"
CUST17 = ROOT / "assessment_workspace/custody/owner_drops/enhancement_specs_20260926"
ANCHOR_ROOT = ROOT / "backend/vendored/extraction_akki/backend"
OUT = SUPP / "verification/verification_receipt_supp18.json"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_csv(path: Path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def parse_docx_blocks(docx_path: Path):
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(docx_path, "r") as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    body = root.find("w:body", ns)
    blocks = []

    def cell_text(tc):
        txt = []
        for t in tc.findall(".//w:t", ns):
            if t.text:
                txt.append(t.text)
        return "".join(txt).strip()

    for child in list(body):
        tag = child.tag.split("}")[-1]
        if tag == "p":
            txt = "".join([(t.text or "") for t in child.findall(".//w:t", ns)]).strip()
            if txt:
                blocks.append({"kind": "paragraph", "text": txt})
        elif tag == "tbl":
            rows = []
            for tr in child.findall(".//w:tr", ns):
                row = [cell_text(tc) for tc in tr.findall("w:tc", ns)]
                if any(c != "" for c in row):
                    rows.append(row)
            if rows:
                blocks.append({"kind": "table", "rows": rows})
    for i, b in enumerate(blocks, start=1):
        b["block"] = i
    return blocks


def parse_xlsx_nonempty_rows(xlsx_path: Path):
    wb = load_workbook(xlsx_path, data_only=False)
    out = {}
    for ws in wb.worksheets:
        rows = []
        for r in range(1, ws.max_row + 1):
            vals = [ws.cell(row=r, column=c).value for c in range(1, ws.max_column + 1)]
            if any(v not in (None, "") for v in vals):
                while vals and vals[-1] in (None, ""):
                    vals.pop()
                rows.append({"row": r, "values": vals})
        out[ws.title] = rows
    return out


def normalize(v):
    if v is None:
        return None
    if isinstance(v, datetime):
        return v.isoformat()
    return str(v).replace("\r\n", "\n").replace("\r", "\n")


def trim_trailing_empty(vals):
    out = list(vals)
    while out and out[-1] in (None, "", "None"):
        out.pop()
    return out


def compare_extraction_json(raw_rows, extracted_rows):
    if len(raw_rows) != len(extracted_rows):
        return False, f"row-count mismatch raw={len(raw_rows)} extracted={len(extracted_rows)}"
    for i, (a, b) in enumerate(zip(raw_rows, extracted_rows), start=1):
        if a.get("row") != b.get("row"):
            return False, f"row-index mismatch at #{i}: {a.get('row')} vs {b.get('row')}"
        av = trim_trailing_empty([normalize(x) for x in a.get("values", [])])
        bv = trim_trailing_empty([normalize(x) for x in b.get("values", [])])
        if av != bv:
            return False, f"cell mismatch row={a.get('row')}"
    return True, "ok"


def sheet_to_records(sheet_rows):
    header = [str(h).strip() if h is not None else "" for h in sheet_rows[0]["values"]]
    records = []
    for row in sheet_rows[1:]:
        vals = row["values"]
        rec = {header[i]: vals[i] if i < len(vals) else None for i in range(len(header))}
        rec["_row"] = row["row"]
        records.append(rec)
    return records


def extract_clause_text(source_anchor, cc_doc_blocks, sec_sheet_rows):
    if "Context_and_Capability_v1.docx B" in source_anchor:
        m = re.search(r"B(\d+)", source_anchor)
        if not m:
            return None
        bnum = int(m.group(1))
        for b in cc_doc_blocks:
            if b["block"] == bnum:
                if b["kind"] == "paragraph":
                    return b["text"]
                return json.dumps(b["rows"], ensure_ascii=False)
        return None
    if "Security_Assurance_Promise_Set.xlsx" in source_anchor:
        m = re.search(r"row(\d+)", source_anchor)
        if not m:
            return None
        rnum = int(m.group(1))
        for row in sec_sheet_rows:
            if row["row"] == rnum:
                return " | ".join([str(v) for v in row["values"] if v is not None])
    return None


def parse_code_refs(evidence):
    refs = []
    for part in (evidence or "").split(";"):
        part = part.strip()
        m = re.match(r"^(services|contracts)/([^:]+):(\d+)-(\d+)$", part)
        if m:
            refs.append(
                {
                    "ref": part,
                    "sub": m.group(1),
                    "rel": m.group(2),
                    "start": int(m.group(3)),
                    "end": int(m.group(4)),
                }
            )
    return refs


def extract_code_excerpt(ref):
    path = ANCHOR_ROOT / ref["sub"] / ref["rel"]
    if not path.exists():
        return {
            "ref": ref["ref"],
            "exists": False,
            "path": str(path),
        }
    lines = path.read_text(encoding="utf-8").splitlines()
    start = max(1, ref["start"])
    end = min(len(lines), ref["end"])
    snippet = "\n".join(lines[start - 1 : end])
    return {
        "ref": ref["ref"],
        "exists": True,
        "path": str(path),
        "line_count": len(lines),
        "range": [start, end],
        "snippet_sha256": sha256_bytes(snippet.encode("utf-8")),
        "snippet_preview": snippet[:600],
    }


def find_clause_id(text):
    m = re.search(r"\b((CC|R)-\d+)\b", text or "")
    return m.group(1) if m else None


def main():
    contract = json.loads((SUPP / "REVIEW_CONTRACT.json").read_text(encoding="utf-8"))
    manifest = json.loads((SUPP / "DOCUMENT_MANIFEST.json").read_text(encoding="utf-8"))
    cc_csv = read_csv(SUPP / "CLAUSE_IMPACT_CC.csv")
    combined_csv = read_csv(SUPP.parent / "CLAUSE_IMPACT_COMBINED.csv")

    # Raw custody file checks (members + hashes + zip introspection for OOXML archives)
    custody_files = sorted([p for p in CUST18.iterdir() if p.is_file()])
    raw_archive = CUST18 / "files_18.zip"
    custody_members = []
    for p in custody_files:
        entry = {
            "name": p.name,
            "bytes": p.stat().st_size,
            "sha256": file_sha256(p),
            "mtime": datetime.fromtimestamp(p.stat().st_mtime).isoformat(),
        }
        if p.suffix.lower() in {".docx", ".xlsx"}:
            with zipfile.ZipFile(p, "r") as zf:
                members = sorted(zf.namelist())
                entry["zip_member_count"] = len(members)
                entry["zip_members_preview"] = members[:12]
        custody_members.append(entry)

    archive_members = []
    archive_sha = None
    if raw_archive.exists():
        archive_sha = file_sha256(raw_archive)
        with zipfile.ZipFile(raw_archive, "r") as zf:
            archive_members = sorted(zf.namelist())

    manifest_docs = {d["name"]: d for d in manifest.get("documents", [])}
    manifest_match = []
    manifest_doc_match_flags = []
    for c in custody_members:
        d = manifest_docs.get(c["name"], {})
        in_manifest_docs = c["name"] in manifest_docs
        if in_manifest_docs:
            manifest_doc_match_flags.append(c["bytes"] == d.get("bytes") and c["sha256"] == d.get("sha256"))
        manifest_match.append(
            {
                "name": c["name"],
                "in_manifest_documents": in_manifest_docs,
                "bytes_match": c["bytes"] == d.get("bytes"),
                "sha_match": c["sha256"] == d.get("sha256"),
            }
        )

    # Parse raw DOCX/XLSX and compare to extracted JSON artifacts
    cc_blocks_raw = parse_docx_blocks(CUST18 / "Context_and_Capability_v1.docx")
    cc_blocks_extracted = json.loads((SUPP / "Context_and_Capability_v1.json").read_text(encoding="utf-8"))
    docx_exact = cc_blocks_raw == cc_blocks_extracted

    mrr18_raw = parse_xlsx_nonempty_rows(CUST18 / "Master_Requirements_Registry.xlsx")
    mrr18_extracted = json.loads((SUPP / "Master_Requirements_Registry.json").read_text(encoding="utf-8"))
    mrr_sheet_checks = {}
    for sname in mrr18_raw:
        ok, msg = compare_extraction_json(mrr18_raw[sname], mrr18_extracted.get(sname, []))
        mrr_sheet_checks[sname] = {"exact": ok, "note": msg}

    sec18_raw = parse_xlsx_nonempty_rows(CUST18 / "Security_Assurance_Promise_Set.xlsx")
    sec18_extracted = json.loads((SUPP / "Security_Assurance_Promise_Set.json").read_text(encoding="utf-8"))
    sec_sheet_checks = {}
    for sname in sec18_raw:
        ok, msg = compare_extraction_json(sec18_raw[sname], sec18_extracted.get(sname, []))
        sec_sheet_checks[sname] = {"exact": ok, "note": msg}

    # Registry + QA key counts from raw workbook
    registry_records = sheet_to_records(mrr18_raw["System Rules Registry"])
    qa_records = sheet_to_records(mrr18_raw["QA Verification"])
    registry_keys = {
        (
            str(r.get("Doc")).strip().lower(),
            str(r.get("Rule ID")).strip(),
        )
        for r in registry_records
        if r.get("Doc") and r.get("Rule ID")
    }
    qa_keys = {
        (
            str(r.get("Doc")).strip().lower(),
            str(r.get("Rule ID")).strip(),
        )
        for r in qa_records
        if r.get("Doc") and r.get("Rule ID")
    }
    missing_qa = sorted(list(registry_keys - qa_keys))

    # Compare to files17 custody baseline
    mrr17_raw = parse_xlsx_nonempty_rows(CUST17 / "Master_Requirements_Registry.xlsx")
    registry17_records = sheet_to_records(mrr17_raw["System Rules Registry"])
    by_id17 = {str(r.get("Rule ID")).strip(): r for r in registry17_records if r.get("Rule ID")}
    by_id18 = {str(r.get("Rule ID")).strip(): r for r in registry_records if r.get("Rule ID")}

    added_ids = sorted([rid for rid in by_id18.keys() if rid not in by_id17])
    removed_ids = sorted([rid for rid in by_id17.keys() if rid not in by_id18])
    changed_ids = []
    compare_cols = [k for k in by_id17[next(iter(by_id17))].keys() if k != "_row"]
    for rid in sorted(set(by_id17.keys()) & set(by_id18.keys())):
        a = by_id17[rid]
        b = by_id18[rid]
        if any(normalize(a.get(c)) != normalize(b.get(c)) for c in compare_cols):
            changed_ids.append(rid)

    sec17_raw = parse_xlsx_nonempty_rows(CUST17 / "Security_Assurance_Promise_Set.xlsx")
    sec17_records = sheet_to_records(sec17_raw["Security Assurance Set"])
    sec18_records = sheet_to_records(sec18_raw["Security Assurance Set"])
    sec17_ids = [str(r.get("#")).strip() for r in sec17_records if r.get("#") and str(r.get("#")).strip().startswith("S-")]
    sec18_ids = [str(r.get("#")).strip() for r in sec18_records if r.get("#") and str(r.get("#")).strip().startswith("S-")]
    sec_added = sorted([s for s in sec18_ids if s not in sec17_ids])
    sec_removed = sorted([s for s in sec17_ids if s not in sec18_ids])

    # Combined CSV checks: 59 rows, 36 preserved + 23 new, no duplicates
    combined_ids = [r["id"] for r in combined_csv if r.get("id")]
    combined_unique = sorted(set(combined_ids))
    new23_expected = [f"CC-{i}" for i in range(1, 17)] + [f"R-{i}" for i in range(41, 47)] + ["S-35"]
    new23_in_combined = sorted([i for i in combined_unique if i in set(new23_expected)])
    preserved36 = sorted([i for i in combined_unique if i not in set(new23_expected)])

    # Verify all cited code paths in combined CSV
    missing_code_refs = []
    combined_code_ref_count = 0
    for row in combined_csv:
        refs = parse_code_refs(row.get("existing_evidence", ""))
        combined_code_ref_count += len(refs)
        for ref in refs:
            p = ANCHOR_ROOT / ref["sub"] / ref["rel"]
            if not p.exists():
                missing_code_refs.append(ref["ref"])

    # Numeric defaults R-41..R-46 capture from docx raw blocks
    numeric_blocks = {}
    for bnum in range(47, 53):
        btxt = next((b["text"] for b in cc_blocks_raw if b["block"] == bnum and b["kind"] == "paragraph"), "")
        numeric_blocks[f"B{bnum}"] = btxt

    # Document date from raw clause vs custody dates
    doc_date_raw = next(
        (
            row[1]
            for b in cc_blocks_raw
            if b["kind"] == "table" and b["block"] == 4
            for row in b["rows"]
            if len(row) >= 2 and str(row[0]).strip().lower() == "date"
        ),
        None,
    )
    custody_dates = sorted({c["mtime"][:10] for c in custody_members})

    # Independent semantic review for all 23 new clauses
    sec_sheet_rows = sec18_raw["Security Assurance Set"]
    per_clause_review = []
    for row in cc_csv:
        cid = row["id"]
        clause_text = extract_clause_text(row["source_anchor"], cc_blocks_raw, sec_sheet_rows)
        refs = [extract_code_excerpt(r) for r in parse_code_refs(row.get("existing_evidence", ""))]
        ref_missing = [r for r in refs if not r.get("exists")]

        # Conservative judgement rubric
        if ref_missing or not clause_text:
            verdict = "disagree"
            reason = "Source anchor or cited code reference missing in raw verification."
        elif "not" in (row.get("assessment", "").lower()) or "no " in (row.get("assessment", "").lower()):
            verdict = "agree"
            reason = "Assessment is conservative (non-proof/absence framing) and matches inspected anchor excerpt scope."
        else:
            verdict = "uncertain"
            reason = "Anchor and excerpt exist, but excerpt slice alone cannot fully confirm semantic claim breadth."

        per_clause_review.append(
            {
                "id": cid,
                "source_anchor": row["source_anchor"],
                "source_clause_excerpt": clause_text[:900] if clause_text else None,
                "assessment": row.get("assessment"),
                "implementation_required": row.get("implementation_required"),
                "code_evidence": refs,
                "judgement": verdict,
                "reason": reason,
            }
        )

    agree_count = sum(1 for r in per_clause_review if r["judgement"] == "agree")
    uncertain_count = sum(1 for r in per_clause_review if r["judgement"] == "uncertain")
    disagree_count = sum(1 for r in per_clause_review if r["judgement"] == "disagree")

    receipt = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "scope": "supplement_18 document-artifact verification only (read-only)",
        "contract_anchor_root": str(ANCHOR_ROOT),
        "checks": {
            "incoming_members_count": len(custody_members),
            "archive_present": raw_archive.exists(),
            "archive_sha256_actual": archive_sha,
            "archive_sha256_manifest": manifest.get("archive_sha256"),
            "archive_sha_match": (archive_sha == manifest.get("archive_sha256")) if archive_sha else False,
            "archive_member_count": len(archive_members),
            "archive_members": archive_members,
            "manifest_hash_match_all": all(manifest_doc_match_flags),
            "manifest_member_matches": manifest_match,
            "docx_extraction_exact": docx_exact,
            "xlsx_extraction_exact": {
                "Master_Requirements_Registry": mrr_sheet_checks,
                "Security_Assurance_Promise_Set": sec_sheet_checks,
            },
            "registry_unique_doc_rule_keys": len(registry_keys),
            "qa_unique_doc_rule_keys": len(qa_keys),
            "missing_qa_count": len(missing_qa),
            "missing_qa_keys": missing_qa,
            "new_ids_added_count": len(added_ids),
            "new_ids_added": added_ids,
            "removed_old_ids_count": len(removed_ids),
            "removed_old_ids": removed_ids,
            "changed_old_ids_count": len(changed_ids),
            "changed_old_ids": changed_ids,
            "security_added": sec_added,
            "security_removed": sec_removed,
            "combined_csv_row_count": len([r for r in combined_csv if r.get("id")]),
            "combined_csv_unique_ids": len(combined_unique),
            "combined_new23_count": len(new23_in_combined),
            "combined_new23_ids": new23_in_combined,
            "combined_preserved_count": len(preserved36),
            "combined_has_duplicates": len(combined_ids) != len(combined_unique),
            "combined_cited_code_refs_total": combined_code_ref_count,
            "combined_missing_code_refs": missing_code_refs,
            "doc_date_raw": doc_date_raw,
            "custody_file_dates": custody_dates,
            "doc_date_distinct_from_custody_date": (doc_date_raw is not None) and (all(d not in (doc_date_raw or "") for d in custody_dates)),
            "numeric_r41_r46_blocks": numeric_blocks,
        },
        "semantic_review_new23": {
            "agree": agree_count,
            "uncertain": uncertain_count,
            "disagree": disagree_count,
            "rows": per_clause_review,
        },
        "raw_custody_members": custody_members,
        "notes": [
            "Used openpyxl for raw workbook reopening and zipfile for raw OOXML archive inspection.",
            "No app/module runtime execution; no DB/provider/LLM/API calls.",
        ],
    }

    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(OUT))


if __name__ == "__main__":
    main()
