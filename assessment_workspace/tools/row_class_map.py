#!/usr/bin/env python3
"""Enumerate every canon row (C1-001 through C9-050 plus C7-D01..D26 plus C4-037a..f)
and determine which have been assigned a class in the 10 domain tables.
Output a CSV of row_id / domain / raw_class_hint so I can hand-audit the mapping.

This is throwaway analysis under tools/ per owner rules.
"""
import re
from pathlib import Path
from collections import defaultdict

NOTES = Path("/app/assessment_workspace/notes")

# All canon rows from the requirement files
def enumerate_rows():
    rows = {}
    # C1..C9 numeric
    for i, n in enumerate([75, 66, 61, 68, 70, 62, 35, 72, 50], start=1):
        for k in range(1, n + 1):
            row_id = f"C{i}-{k:03d}"
            rows[row_id] = None
    # MOAC sub-rows
    for letter in "abcdef":
        rows[f"C4-037{letter}"] = None
    # Defect taxonomy
    for k in range(1, 27):
        rows[f"C7-D{k:02d}"] = None
    return rows

rows = enumerate_rows()
print(f"Total row universe: {len(rows)}")

# For each domain file, find every row_id mention with its class hint
# We look for patterns like "**C3-008**" or "C4-037a" and capture the surrounding
# class hint (REUSE, MODIFY, PARTIAL, RE-POINT, BUILD, HARVEST, RETIRE, N/A-DOCTRINE)
CLASS_KEYWORDS = ["REUSE", "MODIFY", "PARTIAL", "RE-POINT", "REPOINT", "REBUILD",
                  "BUILD", "HARVEST", "RETIRE", "N/A-DOCTRINE", "N/A", "DOCTRINE",
                  "CONTRADICTION", "RESERVED", "WIRING"]

ROW_ID_RE = re.compile(r"\b(C[1-9]-\d{3}[a-f]?|C7-D\d{2})\b")

# Track: row_id -> list of (domain_file, class_hint) mentions
mentions = defaultdict(list)

for domain_file in sorted(NOTES.glob("domain_5_*.md")):
    text = domain_file.read_text(encoding="utf-8")
    for m in ROW_ID_RE.finditer(text):
        row_id = m.group(1)
        # normalise (in case C7-D01 matched but we stored C7-D01)
        # Look-around ±150 chars for the class keyword
        window_start = max(0, m.start() - 200)
        window_end = min(len(text), m.end() + 200)
        window = text[window_start:window_end].upper()
        found_classes = set()
        for cls in CLASS_KEYWORDS:
            if cls in window:
                found_classes.add(cls)
        # Prefer the closest one
        mentions[row_id].append((domain_file.name, found_classes))

# Print rows with NO mention (unassigned)
unassigned = [r for r in rows if r not in mentions]
print(f"\nRows with no domain-file mention: {len(unassigned)}")
if unassigned:
    for r in unassigned[:50]:
        print(f"  UNASSIGNED: {r}")

# Print rows appearing in MULTIPLE domain files (potential double-count)
multi = [r for r in mentions if len({m[0] for m in mentions[r]}) > 1]
print(f"\nRows mentioned in multiple domain files: {len(multi)}")
for r in multi[:30]:
    files = sorted({m[0] for m in mentions[r]})
    print(f"  MULTI: {r} in {files}")

# Class-hint summary per row
print(f"\n\n=== Per-row class-hint summary ===")
by_class = defaultdict(list)
for r, ms in mentions.items():
    # Take union of class hints across all mentions
    all_hints = set()
    for _, hs in ms:
        all_hints.update(hs)
    by_class_key = ",".join(sorted(all_hints)) if all_hints else "(none)"
    by_class[by_class_key].append(r)

# Report class-hint distribution
print("Class-hint clusters (row count):")
for k, rs in sorted(by_class.items(), key=lambda x: -len(x[1]))[:40]:
    print(f"  [{len(rs):>3}]  {k}")
