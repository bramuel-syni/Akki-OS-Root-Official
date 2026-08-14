#!/usr/bin/env python3
"""Drift remediation tool.

For every `Cn-0MM (§XX)` row across canon_[3-9]_requirements.md, verify the §XX
against actual canon `[Heading]` numbering. If §XX exceeds the heading span
OR does not resolve to a real heading, look up the row's substance text and
propose the correct heading by TITLE match.

Emits a JSON mapping proposed corrections. Human-audited before propagation.
"""
import re
import json
from pathlib import Path

WORKSPACE = Path("/app/assessment_workspace")
CANON_TEXT_DIR = WORKSPACE / "canon" / "text"
NOTES = WORKSPACE / "notes"

# Canonical filename → number
CANON_FILES = {
    1: "Akki_Canon_1_Custody_Platform.txt",
    2: "Akki_Canon_2_CIF.txt",
    3: "Akki_Canon_3_Governance_Engines.txt",
    4: "Akki_Canon_4_Operating_Engines.txt",
    5: "Akki_Canon_5_Interface_Architecture.txt",
    6: "Akki_Canon_6_User_Journeys.txt",
    7: "Akki_Canon_7_Integration_and_Quality.txt",
    8: "Akki_Canon_8_The_Watch.txt",
    9: "Akki_Canon_9_Mkondo_Charter.txt",
}

# Extract every heading with its number and title text.
# Pattern: `[Heading N] MAJOR[.MINOR]  Title Text`
HEADING_RE = re.compile(
    r"\[Heading\s+(\d+)\]\s+(\d+(?:\.\d+)?)\s+([^\n]+)"
)

canon_headings = {}  # canon_num → list of (major_str, minor_str_or_none, title)
canon_text = {}
canon_max_top = {}
for n, fn in CANON_FILES.items():
    p = CANON_TEXT_DIR / fn
    if not p.exists():
        canon_headings[n] = []
        canon_max_top[n] = 0
        continue
    text = p.read_text(encoding="utf-8")
    canon_text[n] = text
    heads = []
    max_top = 0
    for m in HEADING_RE.finditer(text):
        num_str = m.group(2)  # e.g. "5" or "5.2"
        title = m.group(3).strip().rstrip("·").strip()
        if "." in num_str:
            major, minor = num_str.split(".")
            major_int = int(major)
        else:
            major_int = int(num_str)
        max_top = max(max_top, major_int)
        heads.append((num_str, title))
    canon_headings[n] = heads
    canon_max_top[n] = max_top

# Load every canon_N_requirements.md and extract rows: Cn-MMM (§XX Title clue)
ROW_RE = re.compile(
    r"C(\d)-(\d{3})\s*\((§(\d+(?:\.\d+)?)?(?:[^)]*))\)",
)

# More permissive:
ROW_RE2 = re.compile(
    r"C(\d)-(\d{3})\s*\((§(\d+(?:\.\d+)?)([^)]*)?)?\)"
)

drift = []
all_rows = []

for n in range(1, 10):
    p = NOTES / f"canon_{n}_requirements.md"
    if not p.exists():
        continue
    txt = p.read_text(encoding="utf-8")
    # match Cn-MMM (§S ...): capture row id, section number, and surrounding hint
    for m in re.finditer(r"C(\d)-(\d{3})\s*\((§(\d+(?:\.\d+)?)[^)]*)\)\**\s*:\s*(.{0,200})", txt):
        cn = int(m.group(1))
        mm = m.group(2)
        section = m.group(4)
        hint = m.group(5).strip().split("\n")[0]
        row = {"row_id": f"C{cn}-{mm}", "cn": cn, "cited_section": section, "hint": hint[:200]}
        all_rows.append(row)
        # Is this section within the actual heading span?
        cited_major = int(section.split(".")[0]) if section else 0
        if cited_major > canon_max_top.get(cn, 0):
            row["drift"] = True
            drift.append(row)
        else:
            # Also check the specific heading exists
            has_exact = any(hs == section for hs, _ in canon_headings.get(cn, []))
            if not has_exact:
                row["drift"] = "possibly"

print(f"Total rows scanned: {len(all_rows)}")
print(f"Drifted rows (§ exceeds max heading): {len(drift)}")

# Show drift breakdown per canon
from collections import Counter
c = Counter(r["cn"] for r in drift)
print(f"Per canon: {dict(c)}")

# For each drifted row, try to propose a correct heading by TITLE match against the hint.
# The row's hint typically contains a title-like phrase; we do a keyword-overlap match.

def score_title_match(title, hint):
    tl = title.lower()
    hl = hint.lower()
    # Score = count of significant words from title that appear in hint
    stop = {"the","a","an","of","and","or","to","in","on","for","by","is","are","that","this","its","not"}
    tw = set(w for w in re.findall(r"\w+", tl) if w not in stop and len(w) >= 3)
    if not tw:
        return 0
    hits = sum(1 for w in tw if w in hl)
    return hits

remediation = {}
for row in drift:
    cn = row["cn"]
    hint = row["hint"]
    candidates = []
    for num_str, title in canon_headings.get(cn, []):
        s = score_title_match(title, hint)
        if s > 0:
            candidates.append((s, num_str, title))
    candidates.sort(key=lambda x: -x[0])
    row["proposed"] = candidates[:3]
    remediation[row["row_id"]] = row

# Output the drift map
out_path = WORKSPACE / "tools" / "drift_map.json"
with open(out_path, "w") as f:
    json.dump({
        "canon_max_top": canon_max_top,
        "canon_headings": {n: canon_headings[n] for n in range(1,10)},
        "drift_rows": drift,
    }, f, indent=2)

print(f"\nWrote {out_path}")

# Show a summary for the drifted rows
print("\n=== DRIFT REMEDIATION PROPOSALS ===")
for row in drift[:80]:
    props = row.get("proposed", [])
    p_str = " | ".join(f"§{p[1]} ({p[2][:40]}) [score={p[0]}]" for p in props[:2])
    print(f"{row['row_id']} was §{row['cited_section']}: HINT={row['hint'][:80]}")
    print(f"  → PROPOSE: {p_str or 'no title-match found'}")
