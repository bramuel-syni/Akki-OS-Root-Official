import csv
import hashlib
import json
import random
import re
from pathlib import Path


ROOT = Path("/app")
BASE = ROOT / "assessment_workspace/notes/enhancement_specs_20260926"
CUSTODY = ROOT / "assessment_workspace/custody/owner_drops/enhancement_specs_20260926"
OUT_DIR = BASE / "verification"
ANCHOR_ROOTS = [
    ROOT,
    ROOT / "backend",
    ROOT / "backend/vendored/extraction_akki",
    ROOT / "backend/vendored/extraction_akki/backend",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_anchor(anchor: str):
    # e.g., services/x.py:12-15 or services/y.py:69
    m = re.match(r"^(?P<path>[^:]+):(\d+)(?:-(\d+))?$", anchor.strip())
    if not m:
        # path-only evidence (no line range)
        p = anchor.strip()
        if p:
            return p, None, None
        return None
    p = m.group("path")
    start = int(m.group(2))
    end = int(m.group(3) or m.group(2))
    return p, start, end


def get_lines(path: Path, start: int, end: int):
    if not path.exists():
        return {"exists": False, "snippet": None}
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    s = max(1, start)
    e = min(len(lines), end)
    snippet = []
    for i in range(s, e + 1):
        snippet.append(f"{i}:{lines[i-1]}")
    return {"exists": True, "snippet": "\n".join(snippet)}


def resolve_anchor_path(rel: str):
    rel_path = Path(rel)
    for base in ANCHOR_ROOTS:
        cand = (base / rel_path).resolve()
        if cand.exists():
            return cand
    return None


def block_lookup(json_blocks):
    return {int(x.get("block")): x for x in json_blocks if "block" in x}


def source_anchor_text(anchor: str, ex_lookup, dq_lookup, sec_rows):
    if "Execution_Standard_v1.docx" in anchor:
        m = re.search(r"B(\d+)", anchor)
        if not m:
            return None
        b = int(m.group(1))
        block = ex_lookup.get(b)
        if not block:
            return None
        return block.get("text") or block.get("rows")
    if "Data_Cleanliness_Spec_v1.docx" in anchor:
        m = re.search(r"B(\d+)", anchor)
        if not m:
            return None
        b = int(m.group(1))
        block = dq_lookup.get(b)
        if not block:
            return None
        return block.get("text") or block.get("rows")
    if "Security_Assurance_Promise_Set.xlsx" in anchor:
        m = re.search(r"row(\d+)", anchor)
        if not m:
            return None
        r = int(m.group(1))
        row = sec_rows.get(r)
        return row
    return None


def extract_rule_keys(registry_json):
    rows = registry_json["System Rules Registry"]
    header = None
    for row in rows:
        vals = row.get("values") or []
        if "Rule ID" in vals and ("Doc" in vals or "Promise / Source Document" in vals):
            header = vals
            break
    if not header:
        return {"count": None, "error": "header_not_found", "keys": []}
    doc_idx = header.index("Doc") if "Doc" in header else header.index("Promise / Source Document")
    rule_idx = header.index("Rule ID")
    keys = []
    for row in rows:
        vals = row.get("values") or []
        if len(vals) <= max(doc_idx, rule_idx):
            continue
        doc = vals[doc_idx]
        rid = vals[rule_idx]
        if not doc or not rid or rid == "Rule ID":
            continue
        keys.append((str(doc).strip(), str(rid).strip()))
    uniq = sorted(set(keys))
    return {"count": len(uniq), "keys": uniq}


def extract_qa_keys(registry_json):
    rows = registry_json["QA Verification"]
    header = None
    for row in rows:
        vals = row.get("values") or []
        if "Rule ID" in vals and ("Doc" in vals or "Promise / Source Document" in vals):
            header = vals
            break
    if not header:
        return {"count": None, "error": "header_not_found", "keys": []}
    doc_idx = header.index("Doc") if "Doc" in header else header.index("Promise / Source Document")
    rule_idx = header.index("Rule ID")
    keys = []
    for row in rows:
        vals = row.get("values") or []
        if len(vals) <= max(doc_idx, rule_idx):
            continue
        doc = vals[doc_idx]
        rid = vals[rule_idx]
        if not doc or not rid or rid == "Rule ID":
            continue
        keys.append((str(doc).strip(), str(rid).strip()))
    uniq = sorted(set(keys))
    return {"count": len(uniq), "keys": uniq}


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    contract = load_json(BASE / "REVIEW_CONTRACT.json")
    manifest = load_json(BASE / "DOCUMENT_MANIFEST.json")
    recon = load_json(BASE / "REGISTRY_RECONCILIATION.json")
    registry = load_json(BASE / "Master_Requirements_Registry.json")
    ex_json = load_json(BASE / "Execution_Standard_v1.json")
    dq_json = load_json(BASE / "Data_Cleanliness_Spec_v1.json")
    sec_json = load_json(BASE / "Security_Assurance_Promise_Set.json")

    csv_rows = []
    with (BASE / "CLAUSE_IMPACT.csv").open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            csv_rows.append(r)

    owner_members = sorted([p.name for p in CUSTODY.iterdir() if p.is_file() and p.suffix in {".docx", ".xlsx"}])
    expected_members = sorted([d["name"] for d in manifest["documents"]])
    member_hash_checks = []
    for d in manifest["documents"]:
        p = CUSTODY / d["name"]
        member_hash_checks.append(
            {
                "name": d["name"],
                "exists": p.exists(),
                "bytes_expected": d["bytes"],
                "bytes_actual": p.stat().st_size if p.exists() else None,
                "sha_expected": d["sha256"],
                "sha_actual": sha256_file(p) if p.exists() else None,
            }
        )

    rule_keys = extract_rule_keys(registry)
    qa_keys = extract_qa_keys(registry)
    missing = sorted(set(rule_keys["keys"]) - set(qa_keys["keys"])) if rule_keys.get("keys") else []

    exdq_expected = sorted(
        [("execution_standard_v1", f"EX-{i}") for i in range(1, 16)]
        + [("data_cleanliness_v1", f"DQ-{i}") for i in range(1, 16)]
    )

    baseline_path = ROOT / recon["baseline"]
    baseline_sha_actual = sha256_file(baseline_path) if baseline_path.exists() else None

    ids = sorted([r["id"] for r in csv_rows])
    rng = random.Random(int(manifest["archive_sha256"], 16))
    sampled_ids = sorted(rng.sample(ids, 20))
    by_id = {r["id"]: r for r in csv_rows}

    ex_lookup = block_lookup(ex_json)
    dq_lookup = block_lookup(dq_json)
    sec_rows = {r["row"]: r for r in sec_json.get("Security Assurance Set", [])}

    sampled = []
    for sid in sampled_ids:
        row = by_id[sid]
        anchors = [x.strip() for x in str(row["existing_evidence"]).split(";") if x.strip()]
        code_evidence = []
        for a in anchors:
            parsed = parse_anchor(a)
            if not parsed:
                code_evidence.append({"anchor": a, "parsed": False})
                continue
            rel, start, end = parsed
            full = resolve_anchor_path(rel)
            if full is None:
                code_evidence.append(
                    {
                        "anchor": a,
                        "parsed": True,
                        "path": None,
                        "exists": False,
                        "snippet": None,
                    }
                )
                continue
            if start is None:
                snippet = get_lines(full, 1, 40)
            else:
                snippet = get_lines(full, start, end)
            code_evidence.append(
                {
                    "anchor": a,
                    "parsed": True,
                    "path": str(full),
                    "exists": snippet["exists"],
                    "snippet": snippet["snippet"],
                }
            )
        sampled.append(
            {
                "id": sid,
                "source_anchor": row["source_anchor"],
                "source_anchor_text": source_anchor_text(row["source_anchor"], ex_lookup, dq_lookup, sec_rows),
                "assessment": row["assessment"],
                "implementation_required": row["implementation_required"],
                "code_evidence": code_evidence,
            }
        )

    checks = {
        "owner_archive_members": {
            "expected_count": 4,
            "actual_count": len(owner_members),
            "expected_members": expected_members,
            "actual_members": owner_members,
            "pass": len(owner_members) == 4 and owner_members == expected_members,
        },
        "member_hashes": member_hash_checks,
        "archive_sha_matches_manifest": {
            "archive_sha": manifest.get("archive_sha256"),
            "contract_seed": contract.get("independent_check", {}).get("sample_seed"),
            "pass": manifest.get("archive_sha256") == contract.get("independent_check", {}).get("sample_seed"),
        },
        "registry_vs_qa": {
            "registry_unique_doc_rule_keys": rule_keys.get("count"),
            "qa_unique_doc_rule_keys": qa_keys.get("count"),
            "missing_count": len(missing),
            "missing_keys": missing,
            "matches_expected_exdq_only": missing == exdq_expected,
            "pass": rule_keys.get("count") == 632 and qa_keys.get("count") == 602 and missing == exdq_expected,
        },
        "historical_baseline": {
            "baseline_path": str(baseline_path),
            "baseline_rules_claim": recon.get("baseline_rules"),
            "baseline_sha_claim": recon.get("baseline_sha256"),
            "baseline_sha_actual": baseline_sha_actual,
            "pass": baseline_path.exists() and recon.get("baseline_rules") == 595 and baseline_sha_actual == recon.get("baseline_sha256"),
        },
        "delta_counts": {
            "added": len(recon.get("added_since_available_baseline", [])),
            "removed": len(recon.get("removed_since_available_baseline", [])),
            "changed": len(recon.get("changed_since_available_baseline", [])),
            "pass": len(recon.get("added_since_available_baseline", [])) == 37 and len(recon.get("removed_since_available_baseline", [])) == 0 and len(recon.get("changed_since_available_baseline", [])) == 2,
        },
        "security_delta": {
            "added_ids": recon.get("security_added_ids", []),
            "removed_ids": recon.get("security_removed_ids", []),
            "changed_rows": recon.get("security_changed_rows", []),
            "pass": recon.get("security_added_ids") == ["S-34"] and recon.get("security_removed_ids") == [] and recon.get("security_changed_rows") == [],
        },
        "clause_impact_ids": {
            "row_count": len(csv_rows),
            "unique_count": len(set(ids)),
            "ids": ids,
            "pass": len(csv_rows) == 36 and len(set(ids)) == 36,
        },
        "cited_paths_exist": {
            "total_anchors": 0,
            "missing_paths": [],
        },
        "sample": {
            "seed": manifest.get("archive_sha256"),
            "size": 20,
            "sampled_ids": sampled_ids,
        },
    }

    missing_paths = []
    total_anchors = 0
    for r in csv_rows:
        anchors = [x.strip() for x in str(r["existing_evidence"]).split(";") if x.strip()]
        for a in anchors:
            total_anchors += 1
            p = parse_anchor(a)
            if not p:
                missing_paths.append({"id": r["id"], "anchor": a, "reason": "parse_failed"})
                continue
            rel, _, _ = p
            full = resolve_anchor_path(rel)
            if full is None:
                missing_paths.append({"id": r["id"], "anchor": a, "reason": "missing_file"})

    checks["cited_paths_exist"]["total_anchors"] = total_anchors
    checks["cited_paths_exist"]["missing_paths"] = missing_paths
    checks["cited_paths_exist"]["pass"] = len(missing_paths) == 0

    out = {
        "checks": checks,
        "sampled_rows_with_evidence": sampled,
    }

    (OUT_DIR / "verification_receipt.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(str(OUT_DIR / "verification_receipt.json"))


if __name__ == "__main__":
    main()
