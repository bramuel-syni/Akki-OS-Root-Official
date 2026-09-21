"""services.rules_service.rule_enumeration_classifier — W-M2-SW4.

Enumeration-classifier for the 286-rule register.  Reads the canon
System Rules Registry (`Master_Requirements_Registry.xlsx` sheet
"System Rules Registry", 445 rows) and assigns each rule an
enforcement class per the classification rubric below.  Closes the
G-4 gap (enumeration classify).

Classification rubric (deterministic, canon-anchored):

* If the canon row's Enforcement Class column already carries a
  ratified value, use it verbatim.
* Doc-1 SyniSense chokepoint / custody-sequence rows (A5.1 · A5.2 ·
  Doc-1 chokepoint anchors) → 'blocking' (Canon-1 §4.1 fail-closed).
* AC-1..AC-N (agent-containment ceilings) → 'blocking'
  (Ratification_Record_v1 AC R-1 RATIFIED).
* RBM-2, RBM-8, RBM-20, RBM-23 (rulebook engine ceremonial) →
  'blocking' (RBM-8 slowest-countdown ceremony).
* BR-*.1 rows (Build Requirement first-line) → 'declaratory'.
* Everything else with empty Enforcement Class → 'pending_override'
  (DEFAULT-PENDING-OVERRIDE — awaits owner ruling per PHASE_C plan).

The pending_override count IS the size of the residual G-4 gap.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Final, Tuple

import openpyxl

from services.rules_service.rule_registry import (
    ENFORCEMENT_CLASSES,
    RuleRecord,
)


CANON_XLSX_PATH: Final[Path] = Path(
    "/app/assessment_workspace/canon/drops/20260910/extracted/"
    "files_15/Master_Requirements_Registry.xlsx"
)
SEED_JSONL_PATH: Final[Path] = Path(__file__).parent / "rule_book_seed.jsonl"


def classify_row(
    rule_id: str,
    statement: str,
    canon_enforcement: str | None,
    doc: str,
    domain: str,
) -> str:
    """Return one of ENFORCEMENT_CLASSES for a canon row."""
    # 1. Ratified canon-declared enforcement class wins.
    if canon_enforcement:
        val = canon_enforcement.strip().lower()
        if val in ENFORCEMENT_CLASSES:
            return val
        # Canon words that map to a class:
        if val in ("mandatory", "must", "block", "blocking",
                   "fail-closed", "hard-block"):
            return "blocking"
        if val in ("declaratory", "descriptive", "doctrine"):
            return "declaratory"
        if val in ("report", "reporting", "audit"):
            return "reporting"

    rid = (rule_id or "").strip()
    stmt = (statement or "").lower()

    # 2. Doc-1 chokepoint / custody-sequence rows.
    if rid in ("A5.1", "A5.2"):
        return "blocking"
    if "chokepoint" in stmt or "custody sequence" in stmt:
        if (doc or "").strip().lower().startswith("doc 1"):
            return "blocking"

    # 3. Agent-containment ceilings.
    if rid.startswith("AC-"):
        return "blocking"

    # 4. Rulebook-engine ceremonial rules.
    if rid.startswith("RBM-"):
        return "blocking"

    # 5. Build-requirement first-line rows.
    if rid.startswith("BR-") and rid.endswith(".1"):
        return "declaratory"

    # 6. Everything else -> pending_override marker.
    return "pending_override"


def generate_seed_from_canon(
    xlsx_path: Path = CANON_XLSX_PATH,
    out_path: Path = SEED_JSONL_PATH,
) -> dict:
    """Read the canon xlsx and write a seed jsonl.

    Returns a summary dict.  Non-destructive: overwrites the seed at
    `out_path` deterministically.
    """
    if not xlsx_path.exists():
        raise FileNotFoundError(f"canon xlsx missing: {xlsx_path!r}")
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    if "System Rules Registry" not in wb.sheetnames:
        raise ValueError(
            "canon xlsx missing 'System Rules Registry' sheet"
        )
    ws = wb["System Rules Registry"]
    rows = list(ws.iter_rows(values_only=True))
    header = rows[0]
    # header: ('Rule ID', 'Statement', 'Objective', 'Promise / Source
    # Document', 'Doc', 'Status', 'Enforcement Class', 'Domain')
    idx = {name: i for i, name in enumerate(header)}
    count_by_class = {c: 0 for c in ENFORCEMENT_CLASSES}
    written = 0
    out_path.parent.mkdir(parents=True, exist_ok=True)
    seen_ids: set[str] = set()
    with out_path.open("w", encoding="utf-8") as fh:
        for row in rows[1:]:
            rid = str(row[idx["Rule ID"]] or "").strip()
            if not rid:
                continue
            if rid in seen_ids:
                # Canon xlsx sometimes has duplicate ids (aliases);
                # SW4 dedupes by first-occurrence.  Duplicates are
                # counted but not written.
                continue
            seen_ids.add(rid)
            stmt = str(row[idx["Statement"]] or "").strip()
            canon_ec = row[idx["Enforcement Class"]]
            doc = str(row[idx["Doc"]] or "").strip()
            domain = str(row[idx["Domain"]] or "").strip()
            source_doc = str(row[idx["Promise / Source Document"]] or "").strip()
            ec = classify_row(rid, stmt, canon_ec, doc, domain)
            count_by_class[ec] += 1
            rec = {
                "rule_id": rid,
                "source_citation": f"{doc} · {source_doc}" if source_doc else doc or "canon System Rules Registry",
                "scope": domain or "canon",
                "enforcement_class": ec,
            }
            # Validate as RuleRecord before writing.
            _ = RuleRecord(**rec)
            fh.write(json.dumps(rec) + "\n")
            written += 1
    return {
        "written": written,
        "count_by_class": count_by_class,
        "seen_ids": len(seen_ids),
    }


def load_seed_summary(seed_path: Path = SEED_JSONL_PATH) -> dict:
    """Load and summarise the on-disk seed jsonl (no registry side-effects)."""
    if not seed_path.exists():
        raise FileNotFoundError(f"seed missing: {seed_path!r}")
    count_by_class = {c: 0 for c in ENFORCEMENT_CLASSES}
    total = 0
    with seed_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            ec = d.get("enforcement_class", "")
            if ec in count_by_class:
                count_by_class[ec] += 1
            total += 1
    return {"total": total, "count_by_class": count_by_class}


def g4_pending_override_count(seed_path: Path = SEED_JSONL_PATH) -> int:
    """Return the current residual G-4 gap size — the count of seed
    rules classified `pending_override` awaiting owner ratification.

    Any future wave that ratifies pending-override rules should
    regenerate the seed and drive this count monotonically toward zero.
    """
    return load_seed_summary(seed_path)["count_by_class"]["pending_override"]


__all__ = [
    "CANON_XLSX_PATH",
    "SEED_JSONL_PATH",
    "classify_row",
    "generate_seed_from_canon",
    "load_seed_summary",
    "g4_pending_override_count",
]
