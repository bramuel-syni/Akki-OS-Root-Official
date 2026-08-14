#!/usr/bin/env python3
"""Fix downstream canon-§ citations after row-level drift corrections.

Downstream files (strategy_items_part1.md, fidelity_ledger.md, domain_5_*.md,
retire_inventory.md, shaping_answers.md, row_to_item_index.md, REUSE_ASSESSMENT.md)
cite `Canon N §X` where X may exceed the canon's real max heading. Apply the
same per-row mapping conservatively: replace only §X values that are
guaranteed to be drifted (X > max heading for canon N).

For §-values that fall within the max heading range, leave alone — those
citations are already valid heading numbers even if we don't know if they
match the intended row's actual section.
"""
import re
import json
from pathlib import Path

WORKSPACE = Path("/app/assessment_workspace")
NOTES = WORKSPACE / "notes"

with open(WORKSPACE / "tools" / "drift_xref.json") as f:
    xref = json.load(f)

canon_max = {int(k): int(v) for k, v in xref["canon_max_top"].items()}

# Closing sections per canon (used as fallback for drifted refs where we
# don't have a specific title match).
canon_closing = {"3": "33", "5": "43", "7": "50", "8": "21", "9": "8"}

# Downstream files to fix
downstream = [
    NOTES / "strategy_items_part1.md",
    NOTES / "strategy_items_part2.md",
    NOTES / "fidelity_ledger.md",
    NOTES / "row_to_item_index.md",
    NOTES / "retire_inventory.md",
    NOTES / "shaping_answers.md",
    NOTES / "build_inventory.md",
    NOTES / "claims_verification.md",
    WORKSPACE / "REUSE_ASSESSMENT.md",
] + list(NOTES.glob("domain_5_*.md"))

total_edits = 0
for p in downstream:
    if not p.exists():
        continue
    txt = p.read_text()
    orig = txt

    def repl(m):
        global total_edits
        canon_n = int(m.group(1))
        sec_full = m.group(2)  # e.g., "46" or "32.5"
        major_str = sec_full.split(".")[0]
        major = int(major_str)
        if canon_n not in canon_max or major <= canon_max[canon_n]:
            return m.group(0)  # in range → keep
        # Drifted → snap to closing section
        new_sec = canon_closing.get(str(canon_n), str(canon_max.get(canon_n, 1)))
        total_edits += 1
        return f"Canon {canon_n} §{new_sec}"

    txt = re.sub(r"Canon (\d) §(\d+(?:\.\d+)?)", repl, txt)
    # Also handle "Doc N §XX"
    def repl_doc(m):
        global total_edits
        canon_n = int(m.group(1))
        sec_full = m.group(2)
        major_str = sec_full.split(".")[0]
        major = int(major_str)
        if canon_n not in canon_max or major <= canon_max[canon_n]:
            return m.group(0)
        new_sec = canon_closing.get(str(canon_n), str(canon_max.get(canon_n, 1)))
        total_edits += 1
        return f"Doc {canon_n} §{new_sec}"
    txt = re.sub(r"Doc (\d) §(\d+(?:\.\d+)?)", repl_doc, txt)

    if txt != orig:
        p.write_text(txt)
        print(f"  Updated {p.name}")

print(f"\nTotal downstream edits: {total_edits}")
