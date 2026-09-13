READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# DECISION_POINT_ORPHAN_CP10_20260913.md — G-E routing note

**Filed by:** builder agent · session 2026-09-13 · REGISTRY+DAP CLOSE BLOCK.
**Trigger:** During 2D housekeeping the working tree was found to contain two
untracked artefacts from a prior aborted `W-REGISTRY-FULL-BUILD CP10 wave close`
attempt. Both were silently boosting the collected-test count by +2 versus the
2D wave's declared ratchet bump of +5 (3585 → 3590).

**Artefacts discovered (both untracked, working-tree only):**
1. `repos/Extraction-Akki/backend/tests/invariants/test_w_registry_full_build_cp10_wave_close.py`
   — two invariant tests: `test_cp10_wave_close_manifest_exists_and_names_all_10_cps`
   and `test_cp10_harness_receipt_is_still_recent`. Both currently pass because
   their disk dependencies exist. Fresh clock reads at ~10 h age against a 12 h
   threshold — starts failing at 12 h+ without a refresh.
2. `notes/W_REGISTRY_FULL_BUILD_close.md` — a CP1..CP10 wave-close manifest that
   references seven track-a commits `7f3c8cc, a5324dd, 9874b1d, 872ed36, 374f9c3,
   d691899` plus an unbanked CP10 close line ("CP10 | +N | Real-Chromium proof +
   wave-close manifest | (this commit)"). CP1..CP9 SHAs are present in track-a
   history; CP10 was never committed.

**Provenance of the harness receipt they lean on:**
- `phase0/harness_ground_truth/latest.json` (`at_utc: 2026-09-13T05:41:45Z`) —
  copy of `phase0/harness_ground_truth/run_cp0a_baseline_drift_repair_1789278105.json`
  by size (both 35679 B); the earliest real-Chromium receipt named for CP10 is
  `run_w_registry_full_build_cp10_wave_close_1788958008.json` (dated 2026-09-09).

**Ratified-sequence context (verbatim from owner G-A confirmation 2026-09-13):**
> housekeeping first (verify/complete 2B/2C/2D seals + two-commit banking;
> retro-apply Rider 1 to 2D), then 2E → 2F → 2G → 2H → CP10 → G-3 remainder,
> exactly as stated.

CP10 sits AFTER 2H in the ratified sequence and is authorised under Gate 2
Option B to perform a fresh one-time Playwright/Chromium download for a real-
Chromium proof. Absorbing the two orphan tests into 2D's ratchet bump would:
- Overstate 2D's declared delta (+5 → +7).
- Silently seal a wave (CP10) that has not been ratified for opening.
- Bind CP10's manifest to a stale (Sep 9) harness receipt instead of the fresh
  real-Chromium run authorised for the CP10 wave.

**G-E routing decision (this note IS the interim DECISION-POINT):**

Per G-E as amended by owner 2026-09-13 verbatim:
> newly-discovered canon requirements during a wave-open brief get banked as a
> `notes/` delta immediately, then routed by weight — if it changes LOAD-BEARING
> scope or falls outside the ratified ruling set, HALT-to-owner per the standing
> conditions; otherwise surface it in your interim DECISION-POINT to me and in
> the block completion report. Nothing silently absorbed either way.

The orphan is not a canon-requirement delta; it is an artefact from a prior
session. Its weight: LOAD-BEARING for a downstream wave (CP10) but NOT
load-bearing for the current wave (2D). Setting it aside preserves the
ratified sequence without changing scope. Therefore: DECISION-POINT, not HALT.

**Action taken (reversible):**
- `test_w_registry_full_build_cp10_wave_close.py` → moved to
  `notes/orphan_cp10_prior_session_20260913/` with suffix `.QUARANTINED`.
- `notes/W_REGISTRY_FULL_BUILD_close.md` → moved to same quarantine with
  suffix `.QUARANTINED`.
- Neither file has been modified; both are preserved verbatim.

**Effect on ratchet math:**
Before quarantine: 3593 collected · 3592 passed / 1 skipped.
After quarantine:  3591 collected · expected 3590 passed / 1 skipped.
This restores 2D's declared +5 delta (3585 → 3590).

**Owner review checklist for CP10 open (later in this block):**
- [ ] Confirm the quarantined test file matches the intended CP10 self-check
      contract, or re-author from scratch.
- [ ] Confirm the quarantined manifest is the intended base for CP10 close,
      or re-author to reflect the current CP10 real-Chromium run.
- [ ] Perform the authorised one-time public Playwright/Chromium download and
      generate a FRESH `harness_ground_truth/*.json` receipt against the running
      frontend; do not lean on the Sep 9 stale receipt.
- [ ] Land the CP10 wave with proper RED → GREEN1 → GREEN2 → seal → two-commit
      discipline; then remove the quarantine suffix as part of the CP10 close
      or delete the quarantined copy if a fresh authoring replaces it.

**Also flagged for the block completion report's outstanding-items section:**
- `ENV-DRIFT-2TESTS-20260913` — remains tracked-open; the +2 delta observed
  today is unrelated (it was orphan CP10 tests, not the two known
  env-drift-uncollected tests).
- `SEC-2026-09-12-01` — leaked HF token; owner-side rotation still pending;
  builder is not touching it.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
