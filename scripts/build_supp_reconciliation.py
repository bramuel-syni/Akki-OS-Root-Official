import glob
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


BASE_DIR = Path("/app/assessment_workspace/notes/full_requirements_gap_20260926")
SUPP_PATH = BASE_DIR / "SUPPLEMENTAL_INVENTORY.json"
BASELINE_PATH = BASE_DIR / "BASELINE_648.json"
SOURCE_CORPUS_PATH = BASE_DIR / "SOURCE_CORPUS.json"
OUT_PATH = BASE_DIR / "SUPPLEMENTAL_RECONCILIATION.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalized_text(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def extract_ruling_id(text: str):
    m = re.match(r"^R-(\d+)\b", text.strip())
    return int(m.group(1)) if m else None


def build_anchor_to_composite_map(base_dir: Path):
    anchor_map = defaultdict(set)
    for fp in glob.glob(str(base_dir / "correction_*.json")):
        arr = load_json(Path(fp))
        for row in arr:
            se = row.get("source_evidence") or {}
            evidence_file = se.get("file")
            quote = se.get("quote", "") or ""
            m = re.search(r"\[(B\d+(?:R\d+)?)\]", quote)
            if evidence_file and m and row.get("composite_id"):
                anchor_map[(evidence_file, m.group(1))].add(row["composite_id"])
    return {k: sorted(v) for k, v in anchor_map.items()}


def build_statement_overlap_index(baseline_rows):
    out = []
    for row in baseline_rows:
        statement = (row.get("Statement") or "").strip()
        if len(statement) >= 80:
            out.append((row.get("composite_id"), statement.lower(), statement))
    return out


def ruling_specifics(text: str, ruling_num: int):
    base = {
        "obligation_effect": "Authority/parameter ruling required before dependent implementation or governance closure.",
        "gap_or_decision": "Ruling text states an open or resolved authority decision point.",
        "action": "Confirm ratifier/authority record and bind implementation/docs to the ruled value."
    }

    if ruling_num == 32:
        return {
            "obligation_effect": "Constrains Generated entries to owner-whitelisted surfaces only; blocks generated content on governance/status/budget/headline surfaces.",
            "gap_or_decision": "Owner product decision required; stale spreadsheet references are non-authoritative versus current code-governed whitelist.",
            "action": "Ratify owner whitelist in authority record and align docs to code as source-of-truth before broader rollout."
        }
    if ruling_num == 37:
        return {
            "obligation_effect": "Re-performance must use a different model family where available; same-family fallback must be explicitly recorded.",
            "gap_or_decision": "OWNER decision governs default; this ruling is distinct from other DEFAULT-class detector settings.",
            "action": "Record OWNER determination, enforce family-difference check in execution standard, and receipt fallback exceptions."
        }
    return base


def classify_rows():
    supp_rows = load_json(SUPP_PATH)
    baseline_rows = load_json(BASELINE_PATH)
    corpus_rows = load_json(SOURCE_CORPUS_PATH)

    source_to_extraction = {r["source"]: r["extraction"] for r in corpus_rows}
    anchor_composite_map = build_anchor_to_composite_map(BASE_DIR)
    statement_idx = build_statement_overlap_index(baseline_rows)

    text_clusters = defaultdict(list)
    for row in supp_rows:
        text_clusters[normalized_text(row["text"])].append(row["supplement_id"])
    duplicate_cluster = {
        sid: ids
        for ids in text_clusters.values()
        if len(ids) > 1
        for sid in ids
    }

    modal_re = re.compile(r"\b(MUST|SHALL|MUST NOT|MAY NOT|NEVER|REQUIRED|REFUSE|REFUSED)\b", re.IGNORECASE)
    id_prefix_re = re.compile(r"^[A-Z][A-Z0-9.-]*-\d+\b")

    reconciled = []
    unresolved = []

    for row in supp_rows:
        sid = row["supplement_id"]
        kind = row["kind"]
        text = row["text"]
        norm = normalized_text(text)

        base = {
            "supplement_id": sid,
            "source": row["source"],
            "source_sha256": row["source_sha256"],
            "anchor": row["anchor"],
            "kind": kind,
            "text": text,
        }

        # Explicit limitations
        if kind == "LIMITATION":
            rec = {
                **base,
                "classification": "EXPLICIT_LIMIT_OR_NONCLAIM",
                "primary_overlap": None,
                "rationale": "Explicit LIM statement defining non-claim boundary; not a registry obligation uplift.",
                "obligation_effect": "Constrains interpretation scope and prevents over-claiming capability or assurance.",
                "gap_or_decision": "No new requirement adoption; retain as disclosure/guardrail language.",
                "action": "Preserve in assurance and implementation notes; verify linked mechanisms remain consistent with this limit."
            }
            reconciled.append(rec)
            continue

        # Explicit rulings
        if kind == "RULING":
            ruling_num = extract_ruling_id(text)
            specifics = ruling_specifics(text, ruling_num) if ruling_num else {
                "obligation_effect": "Authority ruling affects implementation gates, ownership, or defaults.",
                "gap_or_decision": "Ruling item needs explicit ratification trail.",
                "action": "Capture decision in authority record and propagate to dependent controls."
            }

            if sid in duplicate_cluster:
                others = [x for x in duplicate_cluster[sid] if x != sid]
                rec = {
                    **base,
                    "classification": "SOURCE_VERSION_DUPLICATE",
                    "primary_overlap": None,
                    "rationale": f"Exact text duplicate across source versions ({', '.join(others)}); keep one authority chain, avoid duplicate adoption.",
                    **specifics,
                }
            else:
                rec = {
                    **base,
                    "classification": "RULING_OR_AUTHORITY_DEPENDENCY",
                    "primary_overlap": None,
                    "rationale": "Labelled R-* entry; authority decision/dependency rather than direct registry-row expansion.",
                    **specifics,
                }
            reconciled.append(rec)
            continue

        # Normative blocks first: source-version duplicate check
        if sid in duplicate_cluster:
            others = [x for x in duplicate_cluster[sid] if x != sid]
            rec = {
                **base,
                "classification": "SOURCE_VERSION_DUPLICATE",
                "primary_overlap": None,
                "rationale": f"Exact text duplicate across source versions ({', '.join(others)}); no new adopted requirement counted.",
                "obligation_effect": None,
                "gap_or_decision": "Track once under authoritative lineage.",
                "action": "Retain provenance and map only one canonical source-version instance for closure accounting."
            }
            reconciled.append(rec)
            continue

        # Normative overlap via correction anchor+evidence mapping
        extraction = source_to_extraction.get(row["source"])
        key = (extraction, row["anchor"])
        mapped = anchor_composite_map.get(key, [])
        if len(mapped) == 1:
            rec = {
                **base,
                "classification": "REGISTERED_OBLIGATION_OVERLAP",
                "primary_overlap": {
                    "composite_id": mapped[0],
                    "reason": "Anchor/file evidence in correction set maps this source block to an existing registered composite_id."
                },
                "rationale": "Credible overlap established by source anchor + correction evidence; does not increase adopted requirement count.",
                "obligation_effect": None,
                "gap_or_decision": "Already represented in baseline/correction registry chain.",
                "action": "Keep linkage; avoid duplicate requirement creation."
            }
            reconciled.append(rec)
            continue

        # Normative overlap via long unique exact-substring statement match
        lower_text = text.lower()
        hits = [
            (cid, stmt)
            for cid, stmt_low, stmt in statement_idx
            if cid and stmt_low in lower_text
        ]
        uniq_cids = sorted({cid for cid, _ in hits})
        if len(uniq_cids) == 1:
            rec = {
                **base,
                "classification": "REGISTERED_OBLIGATION_OVERLAP",
                "primary_overlap": {
                    "composite_id": uniq_cids[0],
                    "reason": "Long, unique statement substring match to baseline row; treated as represented obligation text."
                },
                "rationale": "Unique long-form textual inclusion supports overlap without relying on shared token or RuleID alone.",
                "obligation_effect": None,
                "gap_or_decision": "Represented in registry wording lineage.",
                "action": "Retain traceability link only; no new adopted row."
            }
            reconciled.append(rec)
            continue

        if len(uniq_cids) > 1:
            rec = {
                **base,
                "classification": "NEEDS_SEMANTIC_REVIEW",
                "primary_overlap": None,
                "rationale": f"Multiple potential overlaps ({', '.join(uniq_cids[:4])}{'...' if len(uniq_cids) > 4 else ''}); no single composite_id can be asserted safely.",
                "obligation_effect": None,
                "gap_or_decision": "Ambiguous overlap; needs adjudicated primary key.",
                "action": "Perform side-by-side semantic adjudication and record one authoritative composite mapping."
            }
            reconciled.append(rec)
            unresolved.append(sid)
            continue

        # No credible overlap found
        looks_normative = bool(modal_re.search(text) or id_prefix_re.match(text.strip()))
        if looks_normative:
            rec = {
                **base,
                "classification": "CROSSCUTTING_UNMAPPED_OBLIGATION",
                "primary_overlap": None,
                "rationale": "Normative/crosscutting obligation language present but no credible composite_id linkage found.",
                "obligation_effect": "Potential additional governed obligation affecting multiple components/docs.",
                "gap_or_decision": "Unmapped into baseline registry; cannot be counted as adopted without authority mapping.",
                "action": "Queue for owner adjudication: decide map-to-existing vs add-new through ceremony."
            }
        else:
            rec = {
                **base,
                "classification": "NEEDS_SEMANTIC_REVIEW",
                "primary_overlap": None,
                "rationale": "Descriptive/context text without definitive normative form or unique overlap evidence.",
                "obligation_effect": None,
                "gap_or_decision": "Insufficient basis for overlap or uplift.",
                "action": "Manual semantic review with surrounding source context before any registry action."
            }
            unresolved.append(sid)

        reconciled.append(rec)

    counts = Counter(r["classification"] for r in reconciled)
    output = {
        "meta": {
            "input_files": [
                str(SUPP_PATH),
                str(SOURCE_CORPUS_PATH),
                str(BASELINE_PATH),
                *sorted(glob.glob(str(BASE_DIR / "correction_*.json"))),
            ],
            "main_adjudications_present": False,
            "total_rows": len(reconciled),
            "category_counts": dict(counts),
            "unresolved_count": len(unresolved),
            "unresolved_ids": unresolved,
            "method": "Conservative evidence-first reconciliation: correction anchor map, long unique substring overlap, duplicate-source collapse, otherwise unmapped/review.",
        },
        "rows": reconciled,
    }

    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Wrote {OUT_PATH} with {len(reconciled)} rows")
    print("Category counts:", dict(counts))
    print("Unresolved:", len(unresolved))


if __name__ == "__main__":
    classify_rows()
