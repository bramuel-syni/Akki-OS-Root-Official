# NEXT.md — Exact next actions

**Last updated:** 2026-08-14, at BUILD_STRATEGY.md v1.1 self-contained assembly.

## Chunk-4 status: COMPLETE AT v1.1 SELF-CONTAINED ASSEMBLY

- **`BUILD_STRATEGY.md`** — 2442 lines / 244 KB, SELF-CONTAINED at `/app/assessment_workspace/BUILD_STRATEGY.md`.
- Working papers in `notes/` remain on disk as review trail (5 files, 2242 lines total).
- STATE/ current across CONTEXT · PINS · DECISIONS · NEXT.
- Audit at v1.1: citation 104/104 file · 1778/1778 canon · 0 failed; completeness PASS.
- Assembly tool: `tools/assemble_build_strategy.py` (idempotent).

## Cold-reader-executable next actions

Anyone reading STATE/ without memory executes:

### 1. Verify audits clean at HEAD

```bash
cd /app/assessment_workspace
python3 tools/citation_audit.py 2>&1 | grep -A1 "^File citations\|^Canon citations"
python3 tools/completeness_audit.py 2>&1 | tail -5
```

Expected: 104/104 file · 1778/1778 canon · 0 failed; PASS.

### 2. Read the deliverable

```bash
less /app/assessment_workspace/BUILD_STRATEGY.md
```

The document is self-contained: no external references required for review.

### 3. Await owner response on the 27 open fidelity-ledger items

Every open item is answerable by owner in one sentence. On answer, update the ledger row → open a corresponding entry in `STATE/DECISIONS.md` as a new Ruling → propagate the effect to the working papers → re-run `tools/assemble_build_strategy.py` → re-run audits → commit.

### 4. Local git commit is at v1.1

```bash
cd /app/assessment_workspace
git log --oneline | head -3
```

Push waits on owner's remote + token.

### 5. Post-owner-review remediation cycle

For every ruling received:
1. Append Ruling verbatim to `STATE/DECISIONS.md`.
2. Update affected working-paper item field(s).
3. Re-run `tools/assemble_build_strategy.py`.
4. Re-run `citation_audit.py` + `completeness_audit.py` — must remain zero-failure.
5. Update `CONTEXT.md` posture.
6. New local commit with message referencing the Ruling ID.

### 6. When rulings arrive on FL-P1-14 (reference screenshot)

- Read the screenshot.
- Update every interface item's `FIXTURE PENDING` field with a specific grammar note.
- Reassemble, re-audit, commit.

### 7. When rulings arrive on FL-P1-10, FL-P1-11 (Use-Data / Verdict-Demo placement)

- Update `WS-MODIFY-USE-DATA-PLACEMENT` and `WS-MODIFY-VERDICT-DEMO`.
- Rerun the inventory audit.
- Reassemble, commit.

### Beyond Chunk 4

Any downstream chunk (execution planning, credit budget) is Owner territory and happens against the frozen `BUILD_STRATEGY.md` under Canon 3 §24 ceremony discipline.
