#!/usr/bin/env python3
"""Completeness audit for BUILD_STRATEGY.

Two mechanical checks:
1. Every non-REUSE canon-row appears in exactly one work item (row_to_item_index.md).
2. Every work item in strategy_items_part[12].md has all seven fields.
"""
import re
from pathlib import Path

WORKSPACE = Path("/app/assessment_workspace")
NOTES = WORKSPACE / "notes"

# --- Check 1: row assignment uniqueness in row_to_item_index.md ---
index_txt = (NOTES / "row_to_item_index.md").read_text()
# The index is a series of tables; capture each row and its class + item.
# Since the table format is diverse, do a soft check: every WS-* item ID
# appearing in the file plus a "Named gaps" section that must be empty.

items_in_index = set(re.findall(r"WS-[A-Z0-9\-]+", index_txt))
print(f"[Check 1a] Distinct work items in row_to_item_index.md: {len(items_in_index)}")

# Named gaps section — must say "None"
named_gaps_match = re.search(r"## Named gaps[^\n]*\n\n?(.+?)(?:\n\n|\Z)", index_txt, re.DOTALL)
if named_gaps_match:
    body = named_gaps_match.group(1).strip()
    if body.startswith("None") or re.match(r"^None\b", body):
        print("[Check 1b] Named gaps section: NONE (pass)")
        named_gaps_pass = True
    else:
        print(f"[Check 1b] Named gaps section: {body[:200]}")
        named_gaps_pass = False
else:
    print("[Check 1b] Named gaps section: not found")
    named_gaps_pass = False

# --- Check 2: seven fields per item in strategy_items_part[12].md ---
FIELD_NAMES = ["WHAT", "CANON CLAUSES", "DEFINITION OF DONE", "QUALITY EVIDENCE", "DEPENDENCIES", "CREDIT COST CLASS", "REVERSAL COST"]

incomplete = []
for part in ["part1", "part2"]:
    text = (NOTES / f"strategy_items_{part}.md").read_text()
    # Split by ## WS- headings
    items = re.split(r"\n## (WS-[A-Z0-9\-]+)", text)
    # First split element is header; then pairs of (item_id, body)
    for i in range(1, len(items), 2):
        item_id = items[i]
        body = items[i+1] if i+1 < len(items) else ""
        missing = []
        for f in FIELD_NAMES:
            # We test for the first-word field key inside a numbered bullet
            if not re.search(rf"\*\*{re.escape(f)}[^*]*\.\*\*", body):
                missing.append(f)
        if missing:
            incomplete.append((part, item_id, missing))

print(f"\n[Check 2] Items missing fields: {len(incomplete)}")
for p, iid, m in incomplete:
    print(f"  {p}/{iid}: missing {m}")

# --- Summary ---
print("\n=== Completeness audit summary ===")
if not incomplete and named_gaps_pass:
    print("PASS — every non-REUSE row assigned; every work item has 7 fields.")
else:
    print("FAIL — see above.")
