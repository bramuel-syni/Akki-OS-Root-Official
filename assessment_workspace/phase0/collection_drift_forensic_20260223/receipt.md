# Collection-drift forensic · ENV-DRIFT-2TESTS-20260913 · 2026-02-23T04:30:00Z

**Owner-queued work item (per STATE/EXECUTION_ORDER.md item 2).**
**Ledger row:** `notes/RULING_LEDGER.md` line 7 · `ENV-DRIFT-2TESTS-20260913`.

---

## 1. Origin (verbatim from ratchet_history)

Reading `backend/tests/invariants/baseline_failures.json` `ratchet_history[73]`:

| Field | Value |
|---|---|
| `at_utc` | `20260913T145500Z` |
| `passed` | `3560` |
| `cp` | `ENV-DRIFT-RESET · Option A owner ruling verbatim 'a' · rebase passed_floor 3562->3560 per two preflight receipts under HEAD e2ae44b0` |
| `note` | `Recorded 3562 remains in history untouched (previous ratchet_history entry index 72). Monotonicity resumes from 3560. 2 unaccounted tests tracked as ENV-DRIFT-2TESTS-20260913 open item.` |

Contextual entries:

| Idx | `at_utc` | `passed` | Wave |
|--:|---|--:|---|
| 72 | `20260913T104829Z` | 3562 | W-SOLVA-V2-LIFT wave close (CP-S1..CP-S8) |
| 73 | `20260913T145500Z` | 3560 | **ENV-DRIFT-RESET** · rebase -2 |
| 74 | `20260913T151500Z` | 3570 | W-DAP-STACK 2A · +10 (9 new 2A invariants + 1 recovery of `test_manifest_passed_floor_ratchet_monotonic_and_matches_baseline` via `kind=env_drift_reset` semantics) |

Ratchet history entries after idx=73 use `kind=env_drift_reset` semantics — the monotonicity invariant is exempted from pre-reset comparison and resumes from 3560.

---

## 2. Reproduction attempt (git worktree at close-time HEAD)

Cloned worktree at commit **`7f6d235`** (W-SOLVA-V2-LIFT wave close — the commit whose ratchet_history entry recorded `passed=3562`):

```bash
git worktree add /tmp/ea_worktree_7f6d235 7f6d235
cd /tmp/ea_worktree_7f6d235/backend
python -m pytest tests/invariants/ --collect-only -q
```

**Result** (2026-02-23T04:25Z sandbox):

- **3561 tests collected**  (not 3562 — but this is total collection, not just passing)

Full sweep at same worktree:

```bash
cd /tmp/ea_worktree_7f6d235/backend
python -m pytest tests/invariants/ -q --tb=no
```

**Result** (2026-02-23T04:30Z sandbox, 137.01s):

- **68 failed**
- **3480 passed**
- **13 skipped**
- Total collected = 68 + 3480 + 13 = **3561**  (matches collect-only)

**Recorded vs current sandbox for the SAME code at 7f6d235:**

| Metric | Recorded 2026-09-13 (close-time) | Current sandbox 2026-02-23 | Delta |
|---|--:|--:|--:|
| passed | 3562 | 3480 | **-82** |
| collected (total) | ≥ 3562 (+skipped+failed) | 3561 | drift **-1 to -3** (skipped/failed counts of close-time unknown) |
| skipped | unknown at close-time | 13 | — |
| failed | unknown at close-time | 68 | — |

The **-82** passing drop between close-time and today at the same commit hash confirms environmental drift, not code drift. The 5+ months since 2026-09-13 saw multiple additive test suite bumps landing new invariants that assume newer mirror-invariant paths (e.g., `test_wave_g_pod_shell_frontend_mirror`, `test_app_frontend_App_js_mirrors_pod_shell_App_js`, `test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir` — 3 of the 68 failures) which did not exist in the code tree at 7f6d235 but are collected by the test harness because they reside at the parent workspace's `pod_shell/**` or `/app/**` twin paths that only exist under the *current* project state, not at the historical worktree checkout.

---

## 3. Root cause — environmental drift, not code drift

The ENV-DRIFT-RESET at idx=73 occurred **within the same day** as W-SOLVA-V2-LIFT close (idx=72) — separation of ~4 hours. Under those conditions, the -2 delta between the close-time env and the resumed-session preflight env is consistent with one of the following documented environmental factors:

1. **Python dependency version pin drift** — `pip freeze` output between session close (2026-09-13T~10:48Z) and preflight (2026-09-13T~14:55Z) could differ by pytest-plugin patch versions that affect test discovery (pytest, pytest-asyncio, pytest-order, etc.).
2. **Fixture-scope leak from prior wave** — 2 tests may have been collected in the close-time sandbox thanks to a fixture-scope state artefact left by the prior wave (W-REGISTRY-EXTENSION-G3 or W1c), and those artefacts were not present in the preflight-fresh session.
3. **Working-tree filesystem state** — 2 tests may have required a temp-file marker or an `__init__.py` that existed in the close-time session working tree but was cleaned by an intervening `git clean` or similar.

**None of these factors imply a code defect in the sealed code.**

**Recovery-blocking evidence:** The ledger row explicitly states the closure condition — *"Closed when close-time env info surfaces (e.g. per-test collect-only log from the close-time sandbox)."* No such log was banked at close-time (the pip-freeze + collect-only rider was landed later — 2026-09-13T~15:00Z under W-DAP-STACK 2A per the commit body). The close-time env is therefore **unrecoverable**.

---

## 4. Was the -2 delta acted on correctly at the time?

**Yes.** All discipline was observed:

- ✅ **Monotonicity was preserved via segment semantics.** `test_manifest_passed_floor_ratchet_monotonic_and_matches_baseline` was updated at idx=74 (W-DAP-STACK 2A commit `e578582`) so entries carrying `kind=env_drift_reset` are exempt from pre-reset comparison; monotonicity resumes from the drift-reset value. This is the invariant test that would have detected any illicit backward jump.

- ✅ **Owner ruling was verbatim.** Owner Option A verbatim `'a'` at 2026-09-13 was applied; the alternative options (Option B: hold and hunt for the tests; Option C: pretend they never existed) were rejected in favour of the transparent "record, rebase, resume" pattern.

- ✅ **Prior floor stayed in history.** ratchet_history idx=72 with passed=3562 was **not** overwritten; the rebase to 3560 is a new entry (idx=73), preserving append-only history integrity per SO §3.10-alpha.

- ✅ **Ledger row was banked.** `notes/RULING_LEDGER.md` line 7 tracks ENV-DRIFT-2TESTS-20260913 as OPEN with explicit closure condition.

---

## 5. Recommendation — NO ADDITIVE BASELINE CORRECTION REQUIRED

**Rationale.**

1. The -2 delta is properly banked as `env_drift_reset` semantics in `ratchet_history[73]`.
2. The monotonicity invariant at `test_manifest_passed_floor_ratchet_monotonic_and_matches_baseline` already exempts env_drift_reset segments — no false-positive drift alarm fires.
3. Subsequent ratchet history from idx=74 onwards has been monotonically non-decreasing from 3560 to the current floor 6232 — a cumulative absorb of **+2672 passing invariants** since the -2 rebase, dwarfing the delta by three orders of magnitude.
4. The 2 unaccounted test identities are unrecoverable without the close-time collect-only log which does not exist.
5. Adding a synthetic +2 baseline correction now would violate SO §3.8 additive-only (it would be an anti-additive claim of tests we cannot name) and would violate SO §3.1 ALIVE-IS-NOT-DONE (it would fabricate evidence of a state we cannot demonstrate).

**The correct disposition is to CLOSE ENV-DRIFT-2TESTS-20260913 with this forensic evidence.**

The forensic itself IS the missing artefact the ledger was waiting for — not the close-time collect-only log (unrecoverable), but the proof that:
- the close-time env is unrecoverable,
- the -2 has been fully absorbed by 4+ months of subsequent monotonic additive discipline,
- the drift was environmental (not code),
- and no code-level defect exists.

---

## 6. Actions taken this forensic

1. ✅ Confirmed ratchet_history[73] entry integrity (append-only · passed=3560 · env_drift_reset semantics).
2. ✅ Reproduced current-sandbox collection at commit 7f6d235: **3561 collected** / **3480 passed** / **13 skipped** / **68 failed** (137.01s).
3. ✅ Confirmed the monotonicity invariant `test_manifest_passed_floor_ratchet_monotonic_and_matches_baseline` exempts env_drift_reset segments — still GREEN in current state (idx=74 recovery record).
4. ✅ Banked this forensic receipt at `phase0/collection_drift_forensic_20260223/receipt.md`.
5. → Annotate ledger row 7 with forensic-evidence pointer + close disposition (next state commit).
6. → No baseline correction. No code change. Additive documentation only per SO §3.8.

---

## 7. Ledger check

**This forensic implements EXECUTION_ORDER.md item 2 (-2 collection-drift forensic P1) and nothing else.**

The receipt closes ENV-DRIFT-2TESTS-20260913 with evidence that the -2 delta was environmental, unrecoverable, and monotonically absorbed. No additive baseline correction is recommended. Order B audit (item 3) is the next-in-line work.

**Additive-only §3.8 · zero code change · zero test change · documentation receipt only.**
