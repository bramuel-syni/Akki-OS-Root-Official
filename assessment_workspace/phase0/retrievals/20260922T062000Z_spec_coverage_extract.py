#!/usr/bin/env python3
"""
Spec-coverage gap digest extraction script · 2026-09-22
========================================================

Reproduces every count in `STATE/notes/SPEC_COVERAGE_GAP_DIGEST_20260922.md`
from the Master Requirements Registry QA v2 workbook filled at
AUDIT-PREP-20260921 seal.

INPUT:
    /app/audit/inbox/Master_Requirements_Registry_QA_v2_builder_status.xlsx
    sha256 8fde06a682f55d65ea55d26776facaad5070e33293a65aface2ed31e63e14b75

USAGE:
    python3 phase0/retrievals/20260922T062000Z_spec_coverage_extract.py

Not committed to programme/track-a code branch; state master notes-only
sibling to the digest.
"""
import openpyxl
import re
from collections import Counter, defaultdict

WB = '/app/audit/inbox/Master_Requirements_Registry_QA_v2_builder_status.xlsx'
SHA_PIN = '8fde06a682f55d65ea55d26776facaad5070e33293a65aface2ed31e63e14b75'


def bs_cat(v):
    if v is None:
        return "MISSING"
    s = str(v).strip().upper()
    if s.startswith('BUILT'):
        return 'BUILT'
    if s.startswith('PARTIAL'):
        return 'PARTIAL'
    if s.startswith('NOT BUILT'):
        return 'NOT_BUILT'
    return f'OTHER({s[:30]})'


def prefix(rid):
    if not rid:
        return 'UNK'
    m = re.match(r'^([A-Za-z]+)', str(rid))
    return m.group(1) if m else str(rid)[:5]


def main():
    wb = openpyxl.load_workbook(WB, read_only=True, data_only=True)
    ws = wb['System Rules Registry']
    header = None
    rows = []
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            header = list(row)
            continue
        if all(v is None for v in row):
            continue
        rows.append(dict(zip(header, row)))

    print(f"Workbook sha256 (verify): {SHA_PIN}")
    print(f"Total rule rows: {len(rows)}")

    cat_counts = Counter(bs_cat(r.get('Builder Status')) for r in rows)
    print(f"BUILT: {cat_counts['BUILT']}")
    print(f"PARTIAL: {cat_counts['PARTIAL']}")
    print(f"NOT_BUILT: {cat_counts['NOT_BUILT']}")
    print()

    # Per Rule ID family prefix
    by_prefix = defaultdict(lambda: Counter())
    for r in rows:
        p = prefix(r.get('Rule ID'))
        by_prefix[p][bs_cat(r.get('Builder Status'))] += 1

    print(f"{'Family':>8}  total  BUILT  PART   NB")
    for p in sorted(by_prefix.keys(), key=lambda x: -sum(by_prefix[x].values())):
        c = by_prefix[p]
        total = sum(c.values())
        if total >= 4:  # skip tiny families
            print(f"{p:>8}  {total:5d}  {c['BUILT']:5d}  {c['PARTIAL']:5d}  {c['NOT_BUILT']:5d}")


if __name__ == '__main__':
    main()
