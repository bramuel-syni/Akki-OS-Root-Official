# NEXT.md — Exact next actions

**Last updated:** 2026-08-14, at BUILD_STRATEGY.md assembly.

## Chunk-4 status: COMPLETE AT ASSEMBLY

- Part 1: `notes/strategy_items_part1.md` (838 lines, 47 items).
- Part 2: `notes/strategy_items_part2.md` (628 lines, 55 items).
- Strategy sections: `notes/strategy_sections.md` (269 lines).
- Fidelity ledger: `notes/fidelity_ledger.md` (102 lines, 27 entries, frozen at assembly).
- Row-to-item index: `notes/row_to_item_index.md` (405 lines, 0 named gaps).
- BUILD_STRATEGY.md: `/app/assessment_workspace/BUILD_STRATEGY.md` (assembled).
- Audit: citation 102/102 · 1118/1118 · 0 failed; completeness PASS.

## Cold-reader-executable next actions

Anyone reading STATE/ without memory executes:

### 1. Verify audit clean

```bash
cd /app/assessment_workspace
python3 tools/citation_audit.py 2>&1 | grep -A1 "^File citations\|^Canon citations"
python3 tools/completeness_audit.py 2>&1 | tail -5
```

Expected: 0 failed citations · PASS on completeness.

### 2. Read the deliverable

```bash
less /app/assessment_workspace/BUILD_STRATEGY.md
```

### 3. Await owner response on the 27 open fidelity-ledger items

Every open item answerable in one sentence. On answer, update fidelity_ledger.md → open a corresponding entry in `STATE/DECISIONS.md` as a new Ruling → propagate the effect to the strategy items file.

### 4. Local git commit

```bash
cd /app/assessment_workspace
git init -q  # if not already
git add BUILD_STRATEGY.md REUSE_ASSESSMENT.md notes/ STATE/ tools/
git commit -m "chunk 4: BUILD_STRATEGY.md — 102 items, 591 rows, 0 gaps, audits clean"
```

Push waits on owner's remote + token.

### 5. Post-owner-review remediation cycle

When owner returns rulings on the 27 open items, each becomes:
- A new Ruling entry in `STATE/DECISIONS.md` (verbatim).
- An update to the affected item field(s).
- A re-run of `citation_audit.py` + `completeness_audit.py`.
- Ledger row closed with a citation to the Ruling.

### 6. When rulings arrive on FL-P1-14 (reference screenshot)

- Read the screenshot.
- Update every interface item's `FIXTURE PENDING` field with a specific grammar note.
- Re-audit.
- Close FL-P1-14.

### 7. When rulings arrive on FL-P1-10, FL-P1-11 (Use-Data / Verdict-Demo placement)

- Update `WS-MODIFY-USE-DATA-PLACEMENT` and `WS-MODIFY-VERDICT-DEMO`.
- Re-run inventory audit.
- Close both rows.

### Beyond Chunk 4

Chunk 5 (execution planning + credit budget from Owner) is out of the assessment scope. Any downstream planning happens against the frozen `BUILD_STRATEGY.md` under Canon 3 §24 ceremony discipline.
