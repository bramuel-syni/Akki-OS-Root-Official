# Order B · Q-1 preflight receipt · 2026-09-21T~18:40Z

**Annotation** (per DQ-01): *auditor=builder instance, independence waived pending desk.*

Audit target: `audit/code-20260921` @ `283524d89dd337d79014b114d575ced7baab6dfc`
Isolated workspace: `/app/audit/scratch/audit_target_code/` — cloned read-only from `/app/audit/inbox/akki_audit_20260921_code.bundle`; `git config remote.origin.url` = the bundle file, not the live tree; `git status --porcelain` = 0 files.

## Q-1 · Build and run · procedure and result

Standards v2 §8.1: *"Say what commands are used and record the exact output."*

```
python3 --version                                                           → Python 3.11.16
PYTHONPATH=. python3 -c 'import services.ledger_writer.main'                → OK
PYTHONPATH=. python3 -m pytest tests/invariants --collect-only -q           → 5857 tests collected, 1 error in 9.67s
```

**Rating**: **DEFECT · Moderate** (collection error blocks a portion of the suite from being counted).

## Q-1 · Finding B-FIND-001

Path: `backend/tests/invariants/test_w10_cp9_composite_lock.py`
Line: 59.

```
E   ModuleNotFoundError: No module named 'w10_cp9_composite_recompute'
```

The test tries `from w10_cp9_composite_recompute import (...)` as a top-level import; no such module is on `sys.path` at the audit tag. Prior seal's ratchet manifest asserts `passed: 5858`; this collection error means **either** (a) the seal counted 5858 including this collection-error item as "passed" incorrectly, **or** (b) the sibling module was on `sys.path` at seal time via a mechanism not preserved by the audit-target clone.

Severity: Moderate (blocks aggregation of a single test; total remaining 5857 collectable). Not a blocker for the audit itself — but this is a **Q-1 build-and-run DEFECT** and a **Q-2.6 collection-integrity finding**, and a candidate line-item for **RD-14 register** (pending re-open by desk).

## Q-2 · Test-suite integrity (partial, pending full sweep)

Q-2.1 test count vs seal manifest: **DEFECT** — actual collectable = 5857; seal counts_at_baseline.passed = 5858. Delta = 1 (the collection-error test).
Q-2.2 pytest exit code on `--collect-only`: 2 (interrupted collection) — a full sweep run will need to `--ignore` or `--continue-on-collection-errors` to complete; both approaches are noted per Standards §8.2.

## Non-actions

- The suite was NOT run to completion this pass (collection error blocks vanilla `pytest`); a next pass will run with `--continue-on-collection-errors -k "not test_w10_cp9_composite_lock"` to obtain a real run rating.
- No file in the audit-target clone was modified.
- No file in the LIVE Extraction-Akki tree was modified.

## Autopilot next on this audit thread (per §6.8 — no GO waited on)

- Next pass: full run with `--continue-on-collection-errors`; record actual pass/fail counts, compare to `counts_at_baseline`.
- Then Q-3 (static quality), Q-6 (secrets scan on the whole history via the bundle).
